"""Approve the reviewed payload-supply mechanism package for future execution.

This module is deterministic, offline, and governance-only.  Approval selects
one package but does not execute it or create payload, input, evidence, source
authority, remediation, retry, merge, runtime, broker, or trading authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_V1"

OPERATOR_ID = "TEST_OPERATOR"
APPROVAL_TIMESTAMP_UTC = "2026-09-06T00:00:00Z"
APPROVAL_DECISION = "APPROVE_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_PHRASE = "I approve PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY for future operator completion inputs reentry or payload supply mechanism execution only, with no current execution, no input preparation, no input supply, no operator payload creation, no evidence package completion, no source-authority acquisition, no evidence acquisition, no no-change disposition, no alternate diagnostic, no remediation, no retry, no main merge, no runtime, no broker, and no trading authority."

SOURCE_OPERATOR_REVIEW_COMMIT = "fc6d9d00ed95c19f0bf679cbf39b2f5acadcdb35"
SOURCE_OPERATOR_REVIEW_DIGEST = "1843d4563bdb729714a145e2756329088ad35b9f45096ea0d917e89651b2b266"
SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST = "62708cf8359f8d74510c5eabb55e528e06f091413b446420c94c0a10c85e546c"
SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST = "7b39125534be4c23afb3247c518cc45094f3b3cd47d9212762dde8812e92265f"
SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST = "89d15c8ee39010e2cb09ffea13f9546df3a55752cff2692fb2a41e45a10c2522"
SOURCE_BINDING_REVIEW_DIGEST = "43f54f1849f6041ef5e83d62684f3adda0d215a1eee457b19cc8c7981c36b05a"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "d1f4403c4c58b34701c6a562193e17cd6bb5132639cf3effe91f3a0012c2d7c2"

APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_attestation_digest"
PACKAGE_OPTIONS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_package_options_digest"
FUTURE_REQUIREMENTS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_future_requirements_digest"
FUTURE_CONTRACT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_future_contract_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_source_binding_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY = SELECTED_PACKAGE

PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD = source.PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD
PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY = source.PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY
PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY = source.PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY
PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY = source.PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY
PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY = source.PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY
PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY = source.PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY
PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS = source.PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS
PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV = source.PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV
PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD = source.PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS = source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS
PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS = source.PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS

DEFAULT_OPERATOR_ATTESTATION = {
    "operator_id": OPERATOR_ID,
    "approval_timestamp_utc": APPROVAL_TIMESTAMP_UTC,
    "approval_decision": APPROVAL_DECISION,
    "selected_package": SELECTED_PACKAGE,
    "approval_phrase": APPROVAL_PHRASE,
}

SOURCE_OPERATOR_REVIEW_BINDINGS = {
    "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
    "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
    "source_operator_review_status": source.OPERATOR_REVIEW_STATUS,
    "source_operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
    "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "source_future_requirements_review_digest": SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST,
    "source_future_contract_review_digest": SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST,
    "source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
    "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
}

PASS, BLOCKER, NOT_EXECUTED = "PASS", "BLOCKER", "NOT_EXECUTED"
GENERATED_APPROVAL_ONLY = "GENERATED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_ONLY"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError(ValueError):
    """Raised when an attestation, source binding, or approval boundary drifts."""


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
            return f"{path}.keys"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return path
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _validate_source_operator_review(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError("source_operator_review must be an object")
    artifact_keys = {
        "artifact_kind": source.ARTIFACT_KIND,
        "operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        source.OPERATOR_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
        source.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
        source.FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY: SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST,
        source.FUTURE_CONTRACT_REVIEW_DIGEST_KEY: SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST,
        source.SOURCE_BINDING_REVIEW_DIGEST_KEY: SOURCE_BINDING_REVIEW_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
    }
    expected = SOURCE_OPERATOR_REVIEW_BINDINGS if all(key in value for key in SOURCE_OPERATOR_REVIEW_BINDINGS) else artifact_keys
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError(f"source_operator_review.{key} mismatch")


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_attestation_v1(
    *, operator_id: str = OPERATOR_ID, approval_timestamp_utc: str = APPROVAL_TIMESTAMP_UTC,
    approval_decision: str = APPROVAL_DECISION, selected_package: str = SELECTED_PACKAGE,
    approval_phrase: str = APPROVAL_PHRASE,
) -> dict[str, str]:
    attestation = {
        "operator_id": operator_id,
        "approval_timestamp_utc": approval_timestamp_utc,
        "approval_decision": approval_decision,
        "selected_package": selected_package,
        "approval_phrase": approval_phrase,
    }
    _validate_attestation(attestation)
    return attestation


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError("operator_attestation must be an object")
    difference = _first_difference(dict(attestation), DEFAULT_OPERATOR_ATTESTATION, "operator_attestation")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError(f"{difference} mismatch or unexpected secret-like field")


def _source_projection() -> dict[str, Any]:
    context = deepcopy(source.SOURCE_CONTEXT)
    prior_keys = {
        "source_operator_review_commit": "source_prior_operator_review_commit",
        "source_operator_review_digest": "source_prior_operator_review_digest",
        "source_package_options_review_digest": "source_prior_package_options_review_digest",
        "source_input_contract_review_digest": "source_prior_input_contract_review_digest",
        "source_binding_review_digest_prior_operator_review": "source_prior_binding_review_digest",
        "source_coverage_review_digest": "source_prior_operator_review_coverage_digest",
        "source_operator_review_manifest_digest": "source_prior_operator_review_manifest_digest",
    }
    for old_key, new_key in prior_keys.items():
        if old_key in context:
            context[new_key] = deepcopy(context[old_key])
    context.update(deepcopy(SOURCE_OPERATOR_REVIEW_BINDINGS))
    context.update({
        "source_candidate_commit": source.SOURCE_CANDIDATE_COMMIT,
        "source_candidate_artifact_kind": source.source.ARTIFACT_KIND,
        "source_candidate_status": source.source.CANDIDATE_STATUS,
        "source_candidate_scope": source.source.CANDIDATE_SCOPE,
        "source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
        "source_candidate_package_options_digest": source.SOURCE_PACKAGE_OPTIONS_DIGEST,
        "source_candidate_future_requirements_digest": source.SOURCE_FUTURE_REQUIREMENTS_DIGEST,
        "source_candidate_future_contract_digest": source.SOURCE_FUTURE_CONTRACT_DIGEST,
        "source_candidate_source_binding_digest": source.SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
        "source_candidate_manifest_digest": source.SOURCE_CANDIDATE_MANIFEST_DIGEST,
        "source_failure_diagnosis_source_binding_review_digest": "f6afb43954adf7f30c8aaf440b1d6d9576f305c0e72f727438e3f10af938b49b",
    })
    return context


SOURCE_CONTEXT = _source_projection()


def _approved_packages() -> list[dict[str, Any]]:
    rows = []
    for index, reviewed in enumerate(source.REVIEWED_PACKAGE_OPTIONS):
        blocked = index >= 7
        selected = index == 0
        row = {
            "package_id": reviewed["package_id"],
            "source_review_status": reviewed["review_status"],
            "approval_status": "SELECTED_APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED" if selected else "BLOCKED_NOT_APPROVED" if blocked else "AVAILABLE_NOT_SELECTED",
            "selected": selected,
            "approved": selected,
            "authorized": selected,
            "executed": False,
        }
        if "blocked_reason" in reviewed:
            row["blocked_reason"] = reviewed["blocked_reason"]
        else:
            row["purpose"] = reviewed.get("purpose", "Preserved supporting option.")
        rows.append(row)
    return rows


APPROVED_PACKAGE_OPTIONS = tuple(_approved_packages())

FUTURE_PLAN = (
    "Bind source no-input failure diagnosis.",
    "Bind source blocked execution, source approval, source operator review, source candidate, completion execution, completion approval, completion candidate, template preparation, preparation/failure/acquisition, follow-on/enrichment, historical remediation, plan/method/diagnostic/recovery, module grouping, and staged inventory.",
    "Preserve blocked reason NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION.",
    "Preserve success/prepared-input/success-manifest digests as null or absent.",
    "Preserve actual coverage as 0/30 and all missing-authority rows as MISSING_NOT_ACQUIRED.",
    "Preserve re-entry or payload-supply package options.",
    "Select and approve the payload-supply mechanism package for future execution only.",
    "Preserve future explicit non-secret operator payload contract.",
    "Preserve allowed values and secret-screening boundaries.",
    "Preserve all direct-change, remediation, retry, acquisition, and main-merge flags as false.",
    "Require separate execution after approval.",
    "Require results review after any future payload-supply mechanism execution.",
    "Require separately approved input preparation/supply or completion reattempt after reviewed explicit non-secret payload exists.",
    "Preserve acquisition, disposition, remediation, retry, main, provider, runtime, broker, and trading gates.",
    "Preserve all source-digest and count-label distinctions without reconciliation.",
)

OUTPUT_IDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_approval_manifest
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_execution_binding_report
source_blocked_reason_report
source_success_digests_absence_report
source_approval_binding_report
source_prior_operator_review_binding_report
source_prior_candidate_binding_report
source_prior_completion_failure_diagnosis_binding_report
source_completion_execution_binding_report
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
selected_package_approval_report
attestation_report
future_payload_supply_contract_approval_report
future_requirements_approval_report
future_plan_approval_report
planned_outputs_authorization_report
supporting_and_blocked_packages_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Execution After Approval v1.",
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Execution Results Review v1.",
    "Operator Completion Inputs Preparation or Supply Execution Reattempt v1, only if explicit non-secret operator inputs are supplied and separately approved.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if explicit non-secret inputs are prepared or supplied.",
    "Operator Source Authority Evidence Package Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition, alternate diagnostic, remediation re-entry, no-change retry criteria, or hold only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_completion_inputs_reentry_or_payload_supply_execution_after_approval
operator_completion_inputs_reentry_or_payload_supply_execution_results_review
operator_completion_inputs_preparation_or_supply_execution_reattempt_with_explicit_non_secret_inputs_if_approved
operator_completion_inputs_preparation_or_supply_results_review_if_prepared_inputs_exist
operator_source_authority_evidence_package_completion_execution_reattempt_if_reviewed_inputs_exist_and_approved
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

TRUE_FIELDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_approval_created
operator_completion_inputs_reentry_or_payload_supply_approval_ready
source_operator_review_bound
source_operator_review_reviewed
source_candidate_bound
source_failure_diagnosis_bound
source_execution_bound
source_execution_blocked_reason_verified
source_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
selected_historical_package_bound
source_operator_review_digest_bound
source_package_options_review_digest_bound
source_future_requirements_review_digest_bound
source_future_contract_review_digest_bound
source_binding_review_digest_bound
source_operator_review_manifest_digest_bound
recommended_package_selected
recommended_package_approved
recommended_package_authorized_for_future_execution_only
operator_attestation_bound
operator_attestation_verified
future_payload_supply_contract_approved
future_requirements_approved
future_plan_approved
planned_outputs_authorized
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
approval_authorizes_future_execution_only_verified
operator_completion_inputs_absence_preserved
execution_correctly_failed_closed
no_input_inference_verified
approval_not_input_verified
template_placeholder_boundary_preserved
diagnostic_output_boundary_preserved
synthetic_success_path_test_only_verified
source_prior_operator_review_bound
source_prior_candidate_bound
source_prior_completion_failure_diagnosis_bound
source_completion_execution_bound
source_completion_approval_bound
source_completion_candidate_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_failure_acquisition_chain_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
priority1_validation_not_retry_evidence
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
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_reentry_or_payload_supply_execution_after_approval""".splitlines())

FALSE_FIELDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_package_executed
operator_payload_supply_mechanism_created
operator_payload_created
operator_completion_inputs_supplied_to_approval
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_shape_validated
operator_completion_inputs_secret_screened
operator_completion_inputs_validated_as_evidence
operator_completion_inputs_bound_as_evidence
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
prepared_operator_completion_inputs_for_results_review
operator_completion_inputs_preparation_or_supply_execution_reattempt_created
operator_completion_inputs_preparation_or_supply_execution_reattempt_performed
operator_completion_inputs_preparation_or_supply_results_review_created
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
template_execution_rerun_performed
completion_execution_rerun_performed
input_preparation_or_supply_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_approval
cache_modified_in_approval
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
provider_requests_made_in_approval
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
ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt
ready_for_operator_completion_inputs_preparation_or_supply_results_review
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
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

COUNTS = {
    **deepcopy(source.COUNTS),
    "supporting_package_count": 6,
    "operator_review_enumerated_non_goal_count": 90,
    "operator_review_enumerated_risk_control_count": 132,
}

_APPROVAL_SPECIFIC_RISK_CONTROLS = tuple("""approval_does_not_execute_package
approval_does_not_create_payload_supply_mechanism
approval_does_not_create_operator_payload
approval_does_not_prepare_inputs
approval_does_not_supply_inputs
approval_does_not_validate_inputs
approval_does_not_bind_inputs
approval_does_not_create_prepared_inputs
approval_does_not_create_completed_evidence_package
approval_does_not_create_evidence_package
approval_does_not_fill_actual_evidence_items
approval_does_not_validate_evidence
approval_does_not_bind_evidence
approval_does_not_accept_evidence_as_source_authority
approval_does_not_infer_inputs_from_template
approval_does_not_infer_inputs_from_placeholders
approval_does_not_infer_inputs_from_diagnostic_output
approval_does_not_infer_inputs_from_digests
approval_does_not_read_cache_for_inputs
approval_does_not_parse_logs_for_inputs
approval_does_not_inspect_env_for_inputs
approval_does_not_read_external_documents_for_inputs
approval_does_not_call_providers_for_inputs
approval_does_not_contact_source_owners_for_inputs
approval_does_not_acquire_source_authority
approval_does_not_acquire_source_authority_evidence
approval_does_not_acquire_external_evidence
approval_does_not_create_source_authority_acquisition_execution
approval_does_not_retry_source_authority_acquisition
approval_does_not_create_no_change_disposition
approval_does_not_execute_alternate_diagnostics
approval_does_not_execute_remediation
approval_does_not_modify_production_code
approval_does_not_modify_existing_tests
approval_does_not_update_expected_digests
approval_does_not_generate_patch
approval_does_not_apply_patch
approval_does_not_run_pytest
approval_does_not_run_full_pytest
approval_does_not_rerun_priority1_validation
approval_does_not_rerun_retry
approval_does_not_rerun_detached_retry
approval_does_not_parse_durable_receipt
approval_does_not_analyze_diagnostic_output
approval_does_not_rerun_source_authority_enrichment
approval_does_not_rerun_follow_on_execution
approval_does_not_rerun_plan_execution
approval_does_not_regenerate_targeted_plan
approval_does_not_rerun_method_execution
approval_does_not_rerun_controlled_recapture
approval_does_not_rerun_template_execution
approval_does_not_rerun_completion_execution
approval_does_not_rerun_input_preparation_execution
approval_does_not_run_diagnostic_command
approval_does_not_read_pytest_cache
approval_does_not_modify_pytest_cache
approval_does_not_commit_pytest_cache
approval_does_not_commit_marketflow_outputs
approval_does_not_parse_terminal_logs
approval_does_not_parse_operator_logs
approval_does_not_inspect_env
approval_does_not_contact_source_owners
approval_does_not_read_external_documents
approval_does_not_reconstruct_prior_lost_values
approval_does_not_reconstruct_full_streams
approval_does_not_classify_modules_again
approval_does_not_classify_full_retry_failures
approval_does_not_classify_full_retry_errors
approval_does_not_claim_failure_error_separation
approval_does_not_identify_authoritative_first_failure
approval_does_not_identify_authoritative_first_error
approval_does_not_claim_traceback_root_cause
approval_does_not_claim_root_cause
approval_does_not_claim_retry_success
approval_does_not_claim_main_merge_readiness
approval_does_not_create_retry_candidate
approval_does_not_create_retry_approval
approval_does_not_create_retry_execution
approval_does_not_create_retry_results_review
approval_does_not_create_main_merge_approval
approval_does_not_push_main
approval_does_not_push_integration_branch
approval_does_not_delete_integration_branch
approval_does_not_delete_worktree
approval_does_not_force_push
approval_does_not_modify_tags
approval_does_not_regenerate_evidence
approval_does_not_call_providers
approval_does_not_acquire_market_data
approval_does_not_generate_dataset
approval_does_not_recompute_metrics
approval_does_not_train_models
approval_does_not_score_strategy
approval_does_not_generate_trade_recommendations
approval_does_not_accept_predictive_usefulness
approval_does_not_accept_profitability
approval_does_not_authorize_runtime
approval_does_not_authorize_broker_execution
approval_is_not_operator_input
reviewed_candidate_is_not_operator_input
reviewed_contract_is_not_operator_input
reviewed_template_is_not_completed_evidence_package
template_placeholders_are_not_completion_inputs
synthetic_success_path_is_test_only
explicit_non_secret_payload_required_before_execution_reattempt
payload_supply_mechanism_execution_is_not_payload_supply
payload_supply_mechanism_execution_is_not_evidence_completion
prepared_inputs_require_results_review_before_completion_use
completed_package_requires_results_review_before_acquisition_use
evidence_binding_requires_separate_acquisition_execution
evidence_binding_requires_results_review
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_completion_reattempt_requires_reviewed_operator_inputs
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

# Carry every source-review control forward.  The three source-review controls
# about selection/approval/authorization remain historical source facts because
# this approval deliberately changes those three states; every other source
# control is promoted to the approval actor.  Ordered de-duplication retains the
# approval-specific vocabulary above while ensuring no source control is lost.
_CARRIED_SOURCE_REVIEW_CONTROLS = tuple(
    item
    if item in {
        "operator_review_does_not_select_package",
        "operator_review_does_not_approve_package",
        "operator_review_does_not_authorize_package",
    }
    else item.replace("operator_review_does_not_", "approval_does_not_", 1)
    for item in source.RISK_CONTROLS
)
RISK_CONTROLS = tuple(dict.fromkeys((*_APPROVAL_SPECIFIC_RISK_CONTROLS, *_CARRIED_SOURCE_REVIEW_CONTROLS)))


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": PASS if actual else BLOCKER, "expected": True, "actual": actual, "severity": BLOCKER, "message": "Boundary preserved." if actual else "Boundary drifted."}


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(value))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_approval(attestation: Mapping[str, Any]) -> dict[str, Any]:
    approval = deepcopy(SOURCE_CONTEXT)
    contract = deepcopy(source.source.FUTURE_PAYLOAD_SUPPLY_CONTRACT)
    contract.update({
        "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_ONLY",
        "execution_status": NOT_EXECUTED,
        "contract_status": "APPROVED_PLANNING_ONLY_NOT_SUPPLIED",
    })
    approval.update({
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "approval_philosophy": "The operator review found the reentry-or-payload-supply candidate suitable for possible selection. This approval selects only the governed payload-supply mechanism package for future execution. Approval is not payload, not input, not evidence, not source authority, not completion, not acquisition, not remediation, not retry, and not merge readiness.",
        "approval_boundary": "Approval only. This artifact selects and approves the recommended package for future execution but does not execute it or create payload, input, evidence, source authority, remediation, retry, merge, runtime, broker, or trading authority.",
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_operator_completion_inputs_reentry_or_payload_supply_package": SELECTED_PACKAGE,
        "selected_package_approved_for_future_execution_only": True,
        "selected_package_executed": False,
        "primary_failure_class": source.source.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(source.source.SECONDARY_FAILURE_CLASSES),
        "approved_package_options": deepcopy(list(APPROVED_PACKAGE_OPTIONS)),
        "approved_future_requirements": [{"requirement_id": item, "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_ONLY", "execution_status": NOT_EXECUTED} for item in source.source.FUTURE_REQUIREMENT_IDS],
        "approved_future_payload_supply_contract": contract,
        "approved_future_plan": [{"step": index, "description": item, "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_ONLY", "execution_status": NOT_EXECUTED} for index, item in enumerate(FUTURE_PLAN, 1)],
        "authorized_planned_outputs": [{"output_id": item, "authorization_status": "AUTHORIZED_NOT_GENERATED"} for item in source.source.PLANNED_OUTPUT_IDS],
        "outputs": [{"output_id": item, "status": GENERATED_APPROVAL_ONLY} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_EXECUTION_NOT_CREATED",
        "recommended_action": "PROCEED_ONLY_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_MECHANISM_EXECUTION_AFTER_APPROVAL",
        "recommendation_reason": "This approval selects and authorizes only future execution of a mechanism definition from the approved contract; it creates no payload, input, evidence, source authority, remediation, retry, merge, runtime, broker, or trading authority.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
    })
    approval.update({key: True for key in TRUE_FIELDS})
    approval.update({key: False for key in FALSE_FIELDS})
    approval.update(COUNTS)

    approval[ATTESTATION_DIGEST_KEY] = semantic_digest(approval["operator_attestation"])
    approval[PACKAGE_OPTIONS_DIGEST_KEY] = semantic_digest(approval["approved_package_options"])
    approval[FUTURE_REQUIREMENTS_DIGEST_KEY] = semantic_digest(approval["approved_future_requirements"])
    approval[FUTURE_CONTRACT_DIGEST_KEY] = semantic_digest(approval["approved_future_payload_supply_contract"])
    approval[SOURCE_BINDING_DIGEST_KEY] = semantic_digest({key: value for key, value in approval.items() if key.startswith(("source_", "retry_", "priority1_"))})
    digest_keys = (APPROVAL_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    approval[APPROVAL_DIGEST_KEY] = _digest_without(approval, *digest_keys)
    approval[MANIFEST_DIGEST_KEY] = semantic_digest({
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        "attestation_digest": approval[ATTESTATION_DIGEST_KEY],
        "package_options_digest": approval[PACKAGE_OPTIONS_DIGEST_KEY],
        "future_requirements_digest": approval[FUTURE_REQUIREMENTS_DIGEST_KEY],
        "future_contract_digest": approval[FUTURE_CONTRACT_DIGEST_KEY],
        "source_binding_digest": approval[SOURCE_BINDING_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    })

    checks = [
        _check("artifact_kind_correct", approval["artifact_kind"] == ARTIFACT_KIND),
        _check("approval_status_correct", approval["approval_status"] == APPROVAL_STATUS),
        _check("approval_scope_correct", approval["approval_scope"] == APPROVAL_SCOPE),
        _check("source_operator_review_commit_bound", approval["source_operator_review_commit"] == SOURCE_OPERATOR_REVIEW_COMMIT),
        _check("source_operator_review_digest_bound", approval["source_operator_review_digest"] == SOURCE_OPERATOR_REVIEW_DIGEST),
        _check("source_operator_review_digest_surface_bound", all(approval[key] == expected for key, expected in SOURCE_OPERATOR_REVIEW_BINDINGS.items())),
        _check("source_candidate_digest_surface_bound", approval["source_candidate_digest"] == source.SOURCE_CANDIDATE_DIGEST and approval["source_candidate_package_options_digest"] == source.SOURCE_PACKAGE_OPTIONS_DIGEST),
        _check("source_blocked_reason_bound", approval["source_blocked_reason"] == source.source.SOURCE_BLOCKED_REASON),
        _check("source_success_digests_absent", approval["source_success_digests_absent"] and approval["source_success_execution_digest"] is None and approval["source_prepared_operator_completion_inputs_digest"] is None and approval["source_prepared_operator_completion_inputs_manifest_digest"] is None),
        _check("primary_failure_class_bound", approval["primary_failure_class"] == source.source.PRIMARY_FAILURE_CLASS),
        _check("secondary_failure_classes_bound", tuple(approval["secondary_failure_classes"]) == source.source.SECONDARY_FAILURE_CLASSES),
        _check("operator_attestation_verified", approval["operator_attestation"] == DEFAULT_OPERATOR_ATTESTATION),
        _check("selected_package_correct", approval["selected_operator_completion_inputs_reentry_or_payload_supply_package"] == SELECTED_PACKAGE),
        _check("selected_package_approved_future_only", approval["selected_package_approved_for_future_execution_only"] and not approval["selected_package_executed"]),
        _check("package_options_preserved", len(approval["approved_package_options"]) == 12),
        _check("supporting_packages_unselected", all(not item["selected"] and not item["approved"] for item in approval["approved_package_options"][1:7])),
        _check("blocked_packages_blocked", all(item["approval_status"] == "BLOCKED_NOT_APPROVED" and not item["approved"] for item in approval["approved_package_options"][7:])),
        _check("future_requirements_approved", len(approval["approved_future_requirements"]) == 62 and all(item["execution_status"] == NOT_EXECUTED for item in approval["approved_future_requirements"])),
        _check("future_contract_approved", approval["approved_future_payload_supply_contract"]["operator_input_supplied"] is False and approval["approved_future_payload_supply_contract"]["execution_status"] == NOT_EXECUTED),
        _check("future_plan_approved", len(approval["approved_future_plan"]) == 15 and all(item["execution_status"] == NOT_EXECUTED for item in approval["approved_future_plan"])),
        _check("planned_outputs_authorized", len(approval["authorized_planned_outputs"]) == 34 and all(item["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["authorized_planned_outputs"])),
        _check("actual_coverage_zero", approval["actual_covered_missing_authority_item_count"] == 0 and approval["actual_uncovered_missing_authority_item_count"] == 30),
        _check("missing_authority_items_missing_not_acquired", approval["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"),
        _check("outputs_generated", [item["output_id"] for item in approval["outputs"]] == list(OUTPUT_IDS)),
        _check("recommendation_defined", approval["recommended_next_task"] == RECOMMENDED_NEXT_TASK),
        _check("next_chain_defined", approval["next_chain"] == list(NEXT_CHAIN)),
        _check("next_gates_defined", approval["next_gates"] == list(NEXT_GATES)),
    ]
    checks.extend(_check(f"{key}_true", approval[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", approval[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"package_{item['package_id']}_approved_correctly", item["executed"] is False and (item["selected"] is (index == 0))) for index, item in enumerate(approval["approved_package_options"]))
    checks.extend(_check(f"requirement_{item}_approved", any(row["requirement_id"] == item and row["execution_status"] == NOT_EXECUTED for row in approval["approved_future_requirements"])) for item in source.source.FUTURE_REQUIREMENT_IDS)
    checks.extend(_check(f"risk_control_{item}_defined", item in approval["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item and row["status"] == GENERATED_APPROVAL_ONLY for row in approval["outputs"])) for item in OUTPUT_IDS)
    for key in (APPROVAL_DIGEST_KEY, ATTESTATION_DIGEST_KEY, PACKAGE_OPTIONS_DIGEST_KEY, FUTURE_REQUIREMENTS_DIGEST_KEY, FUTURE_CONTRACT_DIGEST_KEY, SOURCE_BINDING_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", approval[key]) is not None))
    approval["checklist"] = checks
    approval["summary"] = {
        "total_checks": len(checks),
        "passed_checks": sum(item["status"] == PASS for item in checks),
        "failed_checks": sum(item["status"] != PASS for item in checks),
        "blocker_count": sum(item["status"] != PASS and item["severity"] == BLOCKER for item in checks),
        "selected_operator_completion_inputs_reentry_or_payload_supply_package": SELECTED_PACKAGE,
        "selected_package_approved_for_future_execution_only": True,
        "selected_package_executed": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_completion_inputs_reentry_or_payload_supply_execution_after_approval": True,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    return approval


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict | None = None,
) -> dict[str, Any]:
    """Build the approval from committed constants or validated injected values."""
    source_value = SOURCE_OPERATOR_REVIEW_BINDINGS if source_operator_review is None else source_operator_review
    _validate_source_operator_review(source_value)
    attestation = DEFAULT_OPERATOR_ATTESTATION if operator_attestation is None else operator_attestation
    _validate_attestation(attestation)
    approval = _assemble_approval(attestation)
    result = validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(approval)
    if result["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError("approval checklist contains blockers")
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(approval: dict) -> dict[str, Any]:
    """Reject any drift from the exact deterministic approval artifact."""
    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError("approval must be an object")
    canonical = _assemble_approval(DEFAULT_OPERATOR_ATTESTATION)
    difference = _first_difference(dict(approval), canonical)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError(f"{difference} mismatch")
    return deepcopy(canonical["summary"])


MARKDOWN_SECTIONS = (
    "Approval Disposition", "Source Operator Review", "Operator Review Digest Surface", "Selected Package", "Operator Attestation",
    "Source Candidate", "Source Failure Diagnosis", "Source Execution", "Blocked Reason", "Primary Failure Class", "Secondary Failure Classes",
    "Source Approval", "Selected Historical Input Preparation Package", "Source Prior Operator Review", "Source Prior Candidate",
    "Source Prior Completion-Failure Diagnosis", "Source Completion Execution", "Source Completion Approval",
    "Source Completion Candidate Operator Review", "Source Completion Candidate", "Source Template Preparation Results Review",
    "Source Template Preparation Execution", "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Reviewed Template Structure", "Actual Evidence Absence", "Actual Coverage Zero", "Count Label Distinction",
    "Future Payload Supply Contract Approval", "Approved Future Requirements", "Approved Future Plan", "Authorized Planned Outputs",
    "Supporting and Blocked Packages", "Source Authority Gap Preservation", "Unsupported Claims Boundary", "Recommendation", "Next Chain",
    "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_markdown_v1(approval: dict) -> str:
    """Render the approval as deterministic Markdown."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(approval)
    facts = {
        "Approval Disposition": f"`{APPROVAL_STATUS}` within `{APPROVAL_SCOPE}`. Approval `{approval[APPROVAL_DIGEST_KEY]}`; manifest `{approval[MANIFEST_DIGEST_KEY]}`.",
        "Source Operator Review": f"Commit `{SOURCE_OPERATOR_REVIEW_COMMIT}` and review `{SOURCE_OPERATOR_REVIEW_DIGEST}` are bound as source evidence.",
        "Operator Review Digest Surface": f"Packages `{SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST}`; requirements `{SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST}`; contract `{SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST}`; binding `{SOURCE_BINDING_REVIEW_DIGEST}`; manifest `{SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST}`.",
        "Selected Package": f"`{SELECTED_PACKAGE}` is selected and approved for future execution only; it is not executed.",
        "Operator Attestation": f"Exact deterministic non-secret attestation accepted; digest `{approval[ATTESTATION_DIGEST_KEY]}`.",
        "Source Candidate": f"Commit `{approval['source_candidate_commit']}` and candidate `{approval['source_candidate_digest']}` remain bound.",
        "Source Failure Diagnosis": f"Commit `{approval['source_failure_diagnosis_commit']}` and diagnosis `{approval['source_failure_diagnosis_digest']}` remain bound.",
        "Source Execution": f"Commit `{approval['source_execution_commit']}` remains blocked; no success digest exists.",
        "Blocked Reason": f"`{approval['source_blocked_reason']}`.",
        "Primary Failure Class": f"`{approval['primary_failure_class']}`.",
        "Source Approval": f"Historical approval `{approval['source_approval_digest']}` remains evidence only.",
        "Selected Historical Input Preparation Package": f"`{approval['selected_operator_completion_inputs_preparation_or_supply_package']}` remains historical and supplied no input.",
        "Source Prior Operator Review": f"Commit `{approval['source_prior_operator_review_commit']}` remains bound.",
        "Source Prior Candidate": f"Commit `{approval['source_prior_candidate_commit']}` remains bound.",
        "Source Prior Completion-Failure Diagnosis": f"Commit `{approval['source_prior_completion_failure_diagnosis_commit']}` remains bound.",
        "Source Completion Execution": f"Commit `{approval['source_completion_execution_commit']}` remains blocked by `{approval['source_completion_execution_blocked_reason']}`.",
        "Source Completion Approval": f"Commit `{approval['source_completion_approval_commit']}` remains bound.",
        "Source Completion Candidate Operator Review": f"Commit `{approval['source_completion_candidate_operator_review_commit']}` remains bound.",
        "Source Completion Candidate": f"Commit `{approval['source_completion_candidate_commit']}` remains bound.",
        "Source Template Preparation Results Review": f"Commit `{approval['source_template_preparation_results_review_commit']}` remains bound.",
        "Source Template Preparation Execution": f"Commit `{approval['source_template_preparation_execution_commit']}` remains bound.",
        "Source Preparation Failure Acquisition Chains": "All committed preparation, failure, blocked acquisition, and acquisition-approval constants remain bound; none was executed.",
        "Source Follow-On and Enrichment Chain": "All follow-on, enrichment, inventory, mapping, and historical digests remain bound without rerun.",
        "Historical Blocked Remediation": f"`{approval['historical_blocked_remediation_reason']}` remains authoritative.",
        "Plan Method Diagnostic Recovery Chain": "All plan, method, diagnostic, recapture, recovery, grouping, and staged-inventory digests remain bound.",
        "Durable Receipt": f"`{approval['source_durable_receipt_path']}` is bound opaquely and was not parsed.",
        "Retry Failure Context": "24,877 passed / 1,292 failed / 112 errors / 7 skipped remains authoritative retry evidence.",
        "Priority 1 Validation Summary": "675/675 before and after remains current-root evidence only, never retry evidence.",
        "Diagnostic Capture Evidence Summary": "Exit 1, 1,231,380 stdout bytes, zero stderr bytes, and source hashes remain diagnostic metadata only.",
        "Reviewed Template Structure": "Thirty template rows remain planning-only and are not actual evidence or source authority.",
        "Actual Evidence Absence": "No actual evidence item or completed evidence package exists.",
        "Actual Coverage Zero": "Coverage remains 0/30; all rows remain `MISSING_NOT_ACQUIRED`.",
        "Count Label Distinction": "Prescribed and enumerated source, candidate, review, non-goal, and risk-control counts remain distinct and unreconciled.",
        "Future Payload Supply Contract Approval": f"Approved for future mechanism execution only; not supplied or executed. Digest `{approval[FUTURE_CONTRACT_DIGEST_KEY]}`.",
        "Approved Future Requirements": f"All 62 requirements are approved for future mechanism execution only and remain `{NOT_EXECUTED}`.",
        "Approved Future Plan": f"All 15 steps are approved and remain `{NOT_EXECUTED}`.",
        "Authorized Planned Outputs": "All 34 planned outputs are authorized but not generated.",
        "Supporting and Blocked Packages": "Six supporting packages remain unselected; five unsafe packages remain blocked.",
        "Source Authority Gap Preservation": "No source authority, evidence, external evidence, concrete authority, or safe change was created.",
        "Unsupported Claims Boundary": "No root cause, retry success, predictive usefulness, profitability, or main readiness is claimed.",
        "Recommendation": f"`{approval['recommended_action']}`. Next task: `{RECOMMENDED_NEXT_TASK}`.",
        "Authority Boundaries": "Approval only; execution and every downstream evidence, acquisition, remediation, retry, merge, runtime, broker, and trading gate remain closed.",
        "Checklist Summary": f"{approval['summary']['passed_checks']}/{approval['summary']['total_checks']} PASS; blockers={approval['summary']['blocker_count']}.",
        "Guardrails": "Deterministic committed constants and validated injection only; no source builders, file reads, subprocesses, pytest, cache, logs, environment, external systems, providers, source owners, market data, models, runtime, broker, or trading actions.",
    }
    list_sections = {
        "Secondary Failure Classes": approval["secondary_failure_classes"],
        "Priority 1 Target Modules": [f"{item['path']}: {item['failed_or_errored_nodeid_count']}" for item in approval["priority_1_target_modules"]],
        "Reviewed Observable Families": [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in approval["reviewed_observable_failure_families"]],
        "Reviewed Workstreams": [f"{item['workstream_id']} <- {item['source_family_id']}" for item in approval["reviewed_workstreams"]],
        "Next Chain": approval["next_chain"],
        "Next Gates": approval["next_gates"],
        "Risk Controls": approval["risk_controls"],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Reentry or Payload Supply Approval Status", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", ""))
        if section in list_sections:
            lines.extend(f"{index}. `{item}`" for index, item in enumerate(list_sections[section], 1))
        else:
            lines.append(facts.get(section, "Preserved from committed source evidence; no new execution or downstream authority is created."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested approval status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation,
    )
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_markdown_v1(approval), encoding="utf-8")
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE", "RECOMMENDED_NEXT_TASK",
    "OPERATOR_ID", "APPROVAL_TIMESTAMP_UTC", "APPROVAL_DECISION", "APPROVAL_PHRASE", "DEFAULT_OPERATOR_ATTESTATION",
    "SOURCE_OPERATOR_REVIEW_COMMIT", "SOURCE_OPERATOR_REVIEW_DIGEST", "SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST",
    "SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST", "SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST", "SOURCE_BINDING_REVIEW_DIGEST",
    "SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST", "APPROVAL_DIGEST_KEY", "ATTESTATION_DIGEST_KEY", "PACKAGE_OPTIONS_DIGEST_KEY",
    "FUTURE_REQUIREMENTS_DIGEST_KEY", "FUTURE_CONTRACT_DIGEST_KEY", "SOURCE_BINDING_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY",
    "PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD", "PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY",
    "PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY", "PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY",
    "PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY", "PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY",
    "PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS", "PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV",
    "PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD", "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS",
    "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS", "APPROVED_PACKAGE_OPTIONS", "FUTURE_PLAN", "OUTPUT_IDS",
    "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_markdown_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1",
]
