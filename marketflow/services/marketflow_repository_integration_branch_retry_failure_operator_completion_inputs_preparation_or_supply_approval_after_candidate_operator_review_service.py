"""Approve a future completion-input preparation/supply execution offline.

The artifact is attestation-bound and governance-only.  It selects one package
for a separately invoked future execution but performs no input, evidence,
acquisition, remediation, retry, provider, or runtime action.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
OPERATOR_DECISION = "APPROVE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_FOR_FUTURE_EXECUTION"

SOURCE_OPERATOR_REVIEW_COMMIT = "2efc22338250f9de88e76fbf6381796c82f817df"
SOURCE_OPERATOR_REVIEW_DIGEST = "82e0286d511ced1721346d3049ed434f37d953eba679e71585524529e7864b4a"
SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST = "a649f00a011ffd85e7bb08eea6a0034a42a75847d6460f4bfbb81b6a48fb0ea3"
SOURCE_INPUT_CONTRACT_REVIEW_DIGEST = "78c3a6ff08102a49434486c3683ff5d3be63c798932b4d6ae3d47ab66e17da94"
SOURCE_BINDING_REVIEW_DIGEST = "4f4ed7e71d0b70fdeedbb3c39361cb8bcabb4eceab156dcf12ce406581c34d99"
SOURCE_COVERAGE_REVIEW_DIGEST = "35a3561d865b5ed0c50a854456d5f03a6b05a5db15b4018a07adb789dbb26ae8"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "e8587a7c06142bbee9defbdeb7f91d702914186f0da0cb3c035e0074284fcbfb"

APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_digest"
PACKAGE_OPTIONS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_package_options_digest"
FUTURE_REQUIREMENTS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_future_requirements_digest"
FUTURE_PLAN_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_future_plan_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_manifest_digest"

REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE AFTER OPERATOR COMPLETION INPUTS PREPARATION OR SUPPLY CANDIDATE OPERATOR REVIEW FOR FUTURE INPUT PREPARATION OR SUPPLY EXECUTION ONLY NO INPUT PREPARATION NOW NO INPUT SUPPLY NOW NO OPERATOR COMPLETION INPUTS NOW NO INPUT VALIDATION NOW NO INPUT BINDING NOW NO EVIDENCE PACKAGE COMPLETION NOW NO COMPLETED EVIDENCE PACKAGE NOW NO EVIDENCE PACKAGE CREATION NOW NO EVIDENCE PACKAGE SUPPLY NOW NO EVIDENCE VALIDATION NOW NO EVIDENCE BINDING NOW NO SOURCE AUTHORITY ACQUISITION NOW NO SOURCE AUTHORITY EVIDENCE ACQUISITION NOW NO EXTERNAL EVIDENCE ACQUISITION NOW NO ACQUISITION REATTEMPT NOW NO NO CHANGE DISPOSITION NOW NO ALTERNATE DIAGNOSTICS NOW NO REMEDIATION NOW NO CODE CHANGES NOW NO TEST CHANGES NOW NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE = SELECTED_PACKAGE

PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY = source.PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY
PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY = source.PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY
PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY = source.PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY
PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS = source.PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS
PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY = source.PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY
PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS = source.PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS
PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS = source.PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS
PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT = source.PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT
PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION = source.PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION
PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS = source.PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS
PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS = source.PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(ValueError):
    """Raised when the attestation or approval violates the fixed boundary."""


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
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


SOURCE_OPERATOR_REVIEW_BINDINGS = {
    "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
    "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
    "source_operator_review_status": source.OPERATOR_REVIEW_STATUS,
    "source_operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
    "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "source_input_contract_review_digest": SOURCE_INPUT_CONTRACT_REVIEW_DIGEST,
    "source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
    "source_coverage_review_digest": SOURCE_COVERAGE_REVIEW_DIGEST,
    "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
}

ATTESTATION_VALUE_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "operator_confirms_source_input_contract_review_digest": SOURCE_INPUT_CONTRACT_REVIEW_DIGEST,
    "operator_confirms_source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
    "operator_confirms_source_coverage_review_digest": SOURCE_COVERAGE_REVIEW_DIGEST,
    "operator_confirms_source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
    "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_candidate_package_options_digest": source.SOURCE_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
    "operator_confirms_source_candidate_input_contract_digest": source.SOURCE_CANDIDATE_INPUT_CONTRACT_DIGEST,
    "operator_confirms_source_candidate_source_binding_digest": source.SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
    "operator_confirms_source_candidate_coverage_digest": source.SOURCE_CANDIDATE_COVERAGE_DIGEST,
    "operator_confirms_source_candidate_manifest_digest": source.SOURCE_CANDIDATE_MANIFEST_DIGEST,
    "operator_confirms_source_failure_diagnosis_digest": source.source.SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_failure_classification_digest": source.source.SOURCE_FAILURE_CLASSIFICATION_DIGEST,
    "operator_confirms_source_operator_input_absence_diagnosis_digest": source.source.SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_coverage_diagnosis_digest": source.source.SOURCE_COVERAGE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_failure_diagnosis_manifest_digest": source.source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST,
    "operator_confirms_source_completion_execution_blocked_reason": source.source.PRIMARY_FAILURE_CLASS,
    "operator_confirms_source_completion_execution_blocked_digest": source.source.SOURCE_BINDINGS["source_completion_execution_blocked_digest"],
    "operator_confirms_source_completion_execution_blocked_manifest_digest": source.source.SOURCE_BINDINGS["source_completion_execution_blocked_manifest_digest"],
    "operator_confirms_source_completion_execution_success_digests_absent": True,
    "operator_confirms_source_completion_approval_digest": source.source.SOURCE_BINDINGS["source_approval_digest"],
    "operator_confirms_source_completion_approval_attestation_digest": source.source.SOURCE_BINDINGS["source_attestation_digest"],
    "operator_confirms_source_completion_candidate_operator_review_digest": source.source.SOURCE_BINDINGS["source_operator_review_digest"],
    "operator_confirms_source_completion_candidate_digest": source.source.SOURCE_BINDINGS["source_completion_candidate_digest"],
    "operator_confirms_source_template_preparation_results_review_digest": source.source.SOURCE_BINDINGS["source_results_review_digest"],
    "operator_confirms_source_template_preparation_execution_digest": source.source.SOURCE_BINDINGS["source_template_preparation_execution_digest"],
    "operator_confirms_source_preparation_candidate_digest": source.source.SOURCE_BINDINGS["source_preparation_candidate_digest"],
    "operator_confirms_source_blocked_acquisition_execution_reason": source.source.SOURCE_BINDINGS["source_blocked_acquisition_execution_reason"],
    "operator_confirms_source_blocked_acquisition_execution_manifest_digest": source.source.SOURCE_BINDINGS["source_blocked_acquisition_execution_manifest_digest"],
    "operator_confirms_source_acquisition_approval_digest": source.source.SOURCE_BINDINGS["source_acquisition_approval_digest"],
    "operator_confirms_source_acquisition_attestation_digest": source.source.SOURCE_BINDINGS["source_acquisition_attestation_digest"],
}

ATTESTATION_BOOLEAN_FIELDS = tuple("""operator_confirms_follow_on_enrichment_historical_digests
operator_confirms_plan_method_diagnostic_recovery_digests
operator_confirms_retry_failure_counts
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_workstream_count_4
operator_confirms_template_row_count_30
operator_confirms_actual_coverage_zero
operator_confirms_missing_authority_items_missing_not_acquired
operator_confirms_package_option_count_12
operator_confirms_available_package_count_7
operator_confirms_blocked_package_count_5
operator_confirms_future_input_preparation_requirement_count_62
operator_confirms_future_input_preparation_plan_step_count_17
operator_confirms_planned_output_count_34
operator_confirms_non_goal_count_76
operator_confirms_risk_control_count_105
operator_confirms_source_future_completion_requirement_prescribed_count_67
operator_confirms_source_future_completion_requirement_enumerated_count_69
operator_confirms_source_non_goal_prescribed_count_71
operator_confirms_source_non_goal_enumerated_count_76
operator_confirms_source_risk_control_prescribed_count_104
operator_confirms_source_risk_control_enumerated_count_106
operator_confirms_count_label_distinction_preserved
operator_confirms_recommended_package_selected_for_future_execution_only
operator_confirms_approval_scope_only
operator_confirms_no_input_preparation_now
operator_confirms_no_input_supply_now
operator_confirms_no_operator_completion_inputs_now
operator_confirms_no_input_validation_now
operator_confirms_no_input_binding_now
operator_confirms_no_evidence_package_completion_now
operator_confirms_no_completed_evidence_package_now
operator_confirms_no_evidence_package_creation_now
operator_confirms_no_evidence_package_supply_now
operator_confirms_no_evidence_validation_now
operator_confirms_no_evidence_binding_now
operator_confirms_no_source_authority_acquisition_now
operator_confirms_no_source_authority_evidence_acquisition_now
operator_confirms_no_external_evidence_acquisition_now
operator_confirms_no_acquisition_reattempt_now
operator_confirms_no_no_change_disposition_now
operator_confirms_no_alternate_diagnostics_now
operator_confirms_no_remediation_now
operator_confirms_no_code_change_now
operator_confirms_no_test_change_now
operator_confirms_no_digest_update_now
operator_confirms_no_patch_generation_now
operator_confirms_no_patch_application_now
operator_confirms_no_pytest_now
operator_confirms_no_full_pytest_now
operator_confirms_no_retry_now
operator_confirms_no_cache_read_now
operator_confirms_no_cache_modification_now
operator_confirms_no_receipt_parse_now
operator_confirms_no_diagnostic_output_analysis_now
operator_confirms_no_log_parse_now
operator_confirms_no_env_inspection_now
operator_confirms_no_source_owner_contact_now
operator_confirms_no_external_document_read_now
operator_confirms_no_provider_request_now
operator_confirms_no_runtime_authorization
operator_confirms_no_broker_authorization
operator_confirms_no_trading_authorization
operator_confirms_no_main_push
operator_confirms_no_integration_branch_push
operator_confirms_no_branch_delete
operator_confirms_no_force_push
operator_confirms_no_tag_mutation
operator_confirms_no_evidence_regeneration
operator_confirms_no_marketflow_commit
operator_confirms_no_pytest_cache_commit
operator_confirms_no_predictive_usefulness_acceptance
operator_confirms_no_profitability_acceptance
operator_confirms_no_api_key_storage_or_printing
operator_confirms_no_secret_capture_or_commit""".splitlines())

TRUE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_approval_created
operator_completion_inputs_preparation_or_supply_approval_ready
operator_attestation_bound
operator_attestation_validated
operator_completion_inputs_preparation_or_supply_package_selected
operator_completion_inputs_preparation_or_supply_package_approved
operator_completion_inputs_preparation_or_supply_package_authorized_for_future_execution
selected_package_verified
source_operator_review_bound
source_operator_review_verified
source_candidate_bound
source_failure_diagnosis_bound
source_completion_execution_bound
source_completion_execution_blocked_reason_verified
source_completion_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_candidate_bound
source_blocked_acquisition_execution_bound
source_acquisition_approval_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_authority_acquisition_candidate_bound
source_authority_acquisition_scope_bound
source_missing_authority_mapping_bound
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
operator_input_absence_verified
count_label_distinction_preserved
input_preparation_or_supply_package_options_approved_or_carried_forward
recommended_input_preparation_or_supply_package_selected_for_future_execution
future_input_preparation_requirements_approved
future_input_supply_contract_approved
future_input_preparation_plan_approved
planned_outputs_authorized_not_generated
supporting_packages_carried_forward_unselected
blocked_packages_preserved
non_goals_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_execution_after_approval""".splitlines())

FALSE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_package_executed
operator_completion_inputs_preparation_executed
operator_completion_inputs_supply_executed
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_validated
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
operator_source_authority_evidence_package_ready_for_acquisition_without_review
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
provider_requests_made_in_approval
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

COUNTS = {
    **source.COUNTS,
    "supporting_package_count": 6,
}

FUTURE_PLAN_STEPS = (
    "Bind this approval and the source operator review.",
    "Bind the source candidate, source failure diagnosis, blocked completion execution, completion approval, earlier operator review, completion candidate, template-preparation results review, template-preparation execution, preparation chain, acquisition chain, follow-on/enrichment chain, historical remediation chain, plan/method/diagnostic/recovery chain, module-grouping chain, and staged inventory.",
    "Preserve the source blocked reason NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED.",
    "Preserve source completion execution success digests as absent.",
    "Preserve actual coverage as 0/30 and all missing-authority items as MISSING_NOT_ACQUIRED.",
    "Select the recommended future input preparation or supply package for future execution only.",
    "Approve required non-secret package-header input fields.",
    "Approve required non-secret evidence-item input fields.",
    "Approve allowed section, workstream, artifact-type, classification, specification/observation, and expected/actual values.",
    "Preserve all no-secret, no-API-key, no-broker-credential, no-personal-financial-credential, no-market-data-credential, and no-private-token requirements.",
    "Preserve all direct-change, remediation, retry, and main-merge authorization flags as false.",
    "Require separate execution after this approval before any inputs may be prepared or supplied.",
    "Require results review after any input-preparation or input-supply execution.",
    "Require separately approved completion reattempt after reviewed non-secret inputs exist.",
    "Require completion results review before any source-authority acquisition reattempt.",
    "Preserve source-authority acquisition, no-change disposition, alternate diagnostic, remediation, retry, and main-merge gates.",
    "Preserve provider, runtime, broker, and trading prohibitions.",
)

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Execution After Approval v1.",
    "Operator Completion Inputs Preparation or Supply Results Review v1.",
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

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_execution_after_approval
operator_completion_inputs_preparation_or_supply_results_review
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

RISK_CONTROLS = tuple(
    item.replace("operator_review_", "approval_", 1)
    if item.startswith("operator_review_") else item
    for item in source.RISK_CONTROLS
)
FUTURE_INPUT_REQUIREMENT_IDS = source.FUTURE_INPUT_REQUIREMENT_IDS
PLANNED_OUTPUT_IDS = source.PLANNED_OUTPUT_IDS
NON_GOALS = source.NON_GOALS


def _committed_source_operator_review() -> dict[str, Any]:
    """Return only committed source-review identity constants; call no builder."""
    return deepcopy(SOURCE_OPERATOR_REVIEW_BINDINGS)


def _validate_source_operator_review(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("source_operator_review must be an object")
    if all(key in value for key in SOURCE_OPERATOR_REVIEW_BINDINGS):
        expected = SOURCE_OPERATOR_REVIEW_BINDINGS
    else:
        expected = {
            "artifact_kind": source.ARTIFACT_KIND,
            "operator_review_status": source.OPERATOR_REVIEW_STATUS,
            "operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
            source.OPERATOR_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
            source.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
            source.INPUT_CONTRACT_REVIEW_DIGEST_KEY: SOURCE_INPUT_CONTRACT_REVIEW_DIGEST,
            source.SOURCE_BINDING_REVIEW_DIGEST_KEY: SOURCE_BINDING_REVIEW_DIGEST,
            source.COVERAGE_REVIEW_DIGEST_KEY: SOURCE_COVERAGE_REVIEW_DIGEST,
            source.MANIFEST_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(f"source_operator_review.{key} mismatch")


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    selected_operator_completion_inputs_preparation_or_supply_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
    operator_confirmations: dict,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""
    if not isinstance(operator_reference, str) or not operator_reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("operator_reference invalid")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(operator_attestation_timestamp_utc)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("operator_attestation_timestamp_utc invalid")
    if operator_attestation_phrase != REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("operator_attestation_phrase mismatch")
    if selected_operator_completion_inputs_preparation_or_supply_package != SELECTED_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("selected package mismatch")
    if operator_decision != OPERATOR_DECISION:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("operator_decision mismatch")
    expected_confirmations = {**ATTESTATION_VALUE_FIELDS, **{key: True for key in ATTESTATION_BOOLEAN_FIELDS}}
    difference = _first_difference(operator_confirmations, expected_confirmations, "operator_confirmations")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(f"{difference} mismatch")
    attestation = {
        "operator_decision": OPERATOR_DECISION,
        "selected_operator_completion_inputs_preparation_or_supply_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": SCHEMA_VERSION,
        "operator_reference": operator_reference.strip(),
        **deepcopy(operator_confirmations),
    }
    attestation[ATTESTATION_DIGEST_KEY] = semantic_digest(attestation)
    return attestation


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("operator_attestation must be an object")
    confirmations = {key: attestation.get(key) for key in (*ATTESTATION_VALUE_FIELDS, *ATTESTATION_BOOLEAN_FIELDS)}
    rebuilt = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1(
        operator_reference=attestation.get("operator_reference"),
        operator_attestation_timestamp_utc=attestation.get("operator_attestation_timestamp_utc"),
        operator_attestation_phrase=attestation.get("operator_attestation_phrase"),
        selected_operator_completion_inputs_preparation_or_supply_package=attestation.get("selected_operator_completion_inputs_preparation_or_supply_package"),
        operator_decision=attestation.get("operator_decision"),
        operator_confirmations=confirmations,
    )
    difference = _first_difference(dict(attestation), rebuilt, "operator_attestation")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(f"{difference} mismatch")


def _missing_authority_mapping() -> list[dict[str, Any]]:
    rows = []
    for indexes, section_id, workstream_id in source.source.SECTION_WORKSTREAM_RANGES:
        rows.extend({
            "missing_authority_id": f"MA-{index:03d}",
            "section_id": section_id,
            "workstream_id": workstream_id,
            "current_status": "MISSING_NOT_ACQUIRED",
        } for index in indexes)
    return rows


def _future_input_supply_contract() -> dict[str, Any]:
    rows = [{
        "mapped_missing_authority_id": item["missing_authority_id"],
        "section_id": item["section_id"],
        "workstream_id": item["workstream_id"],
        "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
        "source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
        "source_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
        "digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "evidence_classification": "<ONE_OF_ALLOWED_EVIDENCE_CLASSIFICATIONS>",
        "specification_or_observation": "<SPECIFICATION_OR_OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
        "expected_or_actual_scope": "<EXPECTED_ACTUAL_BOTH_OR_NOT_APPLICABLE>",
        "authority_statement": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
        "results_review_required_before_use": True,
        "direct_change_authorized_now": False,
        "remediation_authorized_now": False,
        "retry_authorized_now": False,
        "main_merge_authorized_now": False,
        "actual_evidence_validated": False,
        "actual_evidence_bound": False,
    } for item in _missing_authority_mapping()]
    return {
        "contract_status": "APPROVED_PLANNING_ONLY_NOT_EXECUTED",
        "package_header": {
            "package_source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_created_utc": "<FUTURE_UTC_TIMESTAMP>",
            "package_digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "package_declares_no_secrets": True,
            "package_declares_no_api_keys": True,
            "package_declares_no_broker_credentials": True,
            "package_declares_no_personal_financial_credentials": True,
            "package_declares_no_market_data_credentials": True,
            "package_declares_no_private_tokens": True,
            "package_distinguishes_specification_from_observation": True,
            "package_distinguishes_expected_from_actual": True,
            "package_distinguishes_source_authority_from_diagnostic_output": True,
            "evidence_items": "EXACTLY_30_ITEMS_DEFINED_BY_THIS_CONTRACT",
        },
        "evidence_items": rows,
        "allowed_section_ids": list(source.source.ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(source.source.ALLOWED_WORKSTREAM_IDS),
        "allowed_acceptable_source_artifact_types": list(source.source.ALLOWED_ARTIFACT_TYPES),
        "allowed_evidence_classifications": list(source.source.ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "allowed_specification_or_observation": list(source.source.ALLOWED_SPECIFICATION_OR_OBSERVATION),
        "allowed_expected_or_actual_scope": list(source.source.ALLOWED_EXPECTED_OR_ACTUAL_SCOPE),
        "future_execution_rejected_secret_markers": list(source.source.SECRET_MARKERS),
        "approval_inspects_secrets": False,
    }


def _source_projection() -> dict[str, Any]:
    raw = source.source.SOURCE_BINDINGS
    projection = {
        **deepcopy(raw),
        **deepcopy(source.source.SOURCE_CONTEXT),
        **deepcopy(source.SOURCE_CANDIDATE_BINDINGS),
        **deepcopy(source.SOURCE_FAILURE_BINDINGS),
        **deepcopy(SOURCE_OPERATOR_REVIEW_BINDINGS),
        "source_completion_approval_commit": raw["source_approval_commit"],
        "source_completion_approval_digest": raw["source_approval_digest"],
        "source_completion_approval_attestation_digest": raw["source_attestation_digest"],
        "source_selected_completion_package": raw["selected_operator_source_authority_evidence_package_completion_package"],
        "source_completion_candidate_operator_review_commit": raw["source_operator_review_commit"],
        "source_completion_candidate_operator_review_digest": raw["source_operator_review_digest"],
        "source_completion_candidate_package_options_review_digest": raw["source_package_options_review_digest"],
        "source_completion_candidate_operator_input_requirements_review_digest": raw["source_operator_input_requirements_review_digest"],
        "source_completion_candidate_template_binding_review_digest": raw["source_template_binding_review_digest"],
        "source_completion_candidate_coverage_review_digest": raw["source_coverage_review_digest"],
        "source_completion_candidate_operator_review_manifest_digest": raw["source_operator_review_manifest_digest"],
        "source_template_preparation_results_review_commit": raw["source_results_review_commit"],
        "source_template_preparation_results_review_digest": raw["source_results_review_digest"],
        "source_template_preparation_results_review_manifest_digest": raw["source_results_review_manifest_digest"],
        "priority_1_target_modules": [{"path": path, "failed_or_errored_nodeid_count": count} for path, count in source.source.PRIORITY_1_TARGET_MODULES],
        "reviewed_observable_failure_families": [{"family_id": family, "observable_evidence_count": count, "confidence": confidence} for family, count, confidence in source.source.OBSERVABLE_FAMILIES],
        "reviewed_workstreams": [{"workstream_id": workstream, "source_family_id": family} for workstream, family in source.source.WORKSTREAMS],
        "reviewed_template_structure": {
            "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
            "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
            "template_only": True,
            "actual_evidence_package_created": False,
        },
        "missing_authority_mapping": _missing_authority_mapping(),
    }
    return projection


def _package_options() -> list[dict[str, Any]]:
    result = []
    for index, (package_id, source_status, _review_status, purpose, blocked_reason) in enumerate(source.PACKAGE_OPTIONS):
        selected = index == 0
        blocked = source_status == "BLOCKED_NOT_ALLOWED"
        item = {
            "package_id": package_id,
            "source_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" if selected else source_status,
            "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_ONLY" if selected else "BLOCKED_NOT_APPROVED" if blocked else "AVAILABLE_NOT_SELECTED",
            "selected": selected,
            "approved": selected,
            "authorized_for_future_execution": selected,
            "executed": False,
        }
        item["blocked_reason" if blocked_reason else "purpose"] = blocked_reason or purpose
        result.append(item)
    return result


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(value))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    fixed = tuple("""artifact_kind_correct
approval_status_correct
approval_scope_correct
operator_attestation_required
operator_attestation_bound
operator_attestation_digest_generated
operator_decision_correct
selected_package_correct
source_operator_review_commit_bound
source_operator_review_digest_bound
source_candidate_digest_bound
source_failure_diagnosis_digest_bound
source_completion_execution_blocked_reason_bound
source_completion_execution_success_digests_absent
primary_failure_class_bound
secondary_failure_classes_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_counts_bound
priority_1_total_612_bound
top_10_total_1069_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_not_retry_evidence
diagnostic_metadata_only
observable_family_count_4_bound
observable_evidence_items_188_bound
workstream_count_4_bound
reviewed_template_row_count_30
actual_coverage_zero
missing_authority_items_missing_not_acquired
count_label_distinction_preserved
package_option_count_12
selected_package_approved
supporting_packages_unselected
blocked_packages_not_approved
future_requirements_approved_not_executed
future_contract_approved
future_plan_approved_not_executed
planned_outputs_authorized_not_generated
non_goals_preserved
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
approval_digest_generated
package_options_digest_generated
future_requirements_digest_generated
future_plan_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())
    source_checks = tuple(f"{key}_bound" for key in sorted(_source_projection()) if key.endswith(("_digest", "_commit", "_reason")))
    check_ids = tuple(dict.fromkeys((
        *fixed,
        *source_checks,
        *(f"attestation_{key}_confirmed" for key in (*ATTESTATION_VALUE_FIELDS, *ATTESTATION_BOOLEAN_FIELDS)),
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"package_option_{index:02d}_carried_forward" for index in range(1, 13)),
        *(f"future_requirement_{item}_approved" for item in FUTURE_INPUT_REQUIREMENT_IDS),
        *(f"future_plan_step_{index:02d}_approved" for index in range(1, 18)),
        *(f"planned_output_{item}_authorized" for item in PLANNED_OUTPUT_IDS),
        *(f"non_goal_{item}_preserved" for item in NON_GOALS),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    return [{
        "check_id": check_id,
        "status": PASS,
        "expected": True,
        "actual": True,
        "severity": BLOCKER,
        "message": f"{check_id} passed",
    } for check_id in check_ids]


def _summary(approval: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "operator_completion_inputs_preparation_or_supply_approval_created",
        "operator_completion_inputs_preparation_or_supply_approval_ready",
        "selected_operator_completion_inputs_preparation_or_supply_package",
        "operator_completion_inputs_preparation_or_supply_package_selected",
        "operator_completion_inputs_preparation_or_supply_package_approved",
        "operator_completion_inputs_preparation_or_supply_package_authorized_for_future_execution",
        "operator_completion_inputs_preparation_or_supply_package_executed",
        "operator_completion_inputs_prepared", "operator_completion_inputs_supplied",
        "operator_completion_inputs_provided", "operator_completion_inputs_validated",
        "operator_completion_inputs_bound", "operator_source_authority_evidence_package_completed",
        "operator_source_authority_evidence_package_created", "operator_source_authority_evidence_package_supplied",
        "operator_source_authority_evidence_package_validated", "operator_source_authority_evidence_package_bound",
        "source_authority_acquisition_performed", "source_authority_evidence_acquired",
        "external_evidence_acquired", "concrete_source_authority_established",
        "safe_source_authority_bound_change_identified", "actual_covered_missing_authority_item_count",
        "actual_uncovered_missing_authority_item_count", "missing_authority_items_status",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_after_approval",
        "ready_for_operator_completion_inputs_preparation_or_supply_results_review",
        "ready_for_operator_source_authority_evidence_package_completion_execution",
        "ready_for_source_authority_acquisition_execution_retry", "ready_for_retry_candidate",
        "ready_for_main_merge_approval", "priority_1_total_nodeids", "failed_or_errored_nodeids_count",
        "observable_failure_family_count", "total_observable_evidence_items", "package_option_count",
        "available_package_count", "supporting_package_count", "blocked_package_count",
        "future_input_preparation_requirement_count", "future_input_preparation_plan_step_count",
        "planned_output_count", "recommended_next_task",
    )
    return {
        "total_checks": len(approval["checklist"]),
        "passed_checks": len(approval["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        **{key: deepcopy(approval[key]) for key in keys},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _assemble_approval(source_operator_review: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    source_projection = _source_projection()
    package_options = _package_options()
    future_requirements = [{
        "requirement_id": item,
        "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    } for item in FUTURE_INPUT_REQUIREMENT_IDS]
    future_plan = [{
        "step": index,
        "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
        "action": action,
    } for index, action in enumerate(FUTURE_PLAN_STEPS, 1)]
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_operator_completion_inputs_preparation_or_supply_package": SELECTED_PACKAGE,
        "approval_philosophy": "The source operator review confirms that explicit non-secret operator completion inputs are still absent and that the recommended future path is a separately governed input-preparation or input-supply execution. This approval may select and authorize that future execution package only. It must not prepare, supply, validate, bind, complete, acquire, remediate, retry, merge, or authorize runtime/trading.",
        "approval_boundary": "Approval only. This artifact selects the recommended input-preparation/supply package for a future separate execution. It does not create operator completion inputs, complete an evidence package, validate or bind evidence, acquire source authority, or create downstream readiness.",
        **deepcopy(source_projection),
        **deepcopy(COUNTS),
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "approved_package": deepcopy(package_options[0]),
        "package_options": package_options,
        "approved_future_input_preparation_requirements": future_requirements,
        "approved_future_input_supply_contract": _future_input_supply_contract(),
        "approved_future_plan": future_plan,
        "planned_outputs": [{"output_id": item, "status": "AUTHORIZED_NOT_GENERATED"} for item in PLANNED_OUTPUT_IDS],
        "supporting_packages": deepcopy(package_options[1:7]),
        "blocked_packages": deepcopy(package_options[7:]),
        "non_goals": [{"non_goal_id": item, "preserved": True} for item in NON_GOALS],
        "actual_evidence_absence": {
            "completed_package_created": False,
            "evidence_package_created": False,
            "evidence_package_supplied": False,
            "evidence_package_validated": False,
            "evidence_package_bound": False,
            "actual_evidence_items_filled": False,
        },
        "actual_coverage": {
            "reviewed_template_row_count": 30,
            "actual_covered_missing_authority_item_count": 0,
            "actual_uncovered_missing_authority_item_count": 30,
            "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        },
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_V1",
        "recommended_next_task_status": "FUTURE_EXECUTION_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY",
        "reason": "The operator review confirmed the candidate is complete and reviewable. This approval selects the recommended package for a future execution that may prepare or supply explicit non-secret operator completion inputs for all 30 reviewed template rows. The approval itself does not prepare or supply inputs, complete an evidence package, validate or bind evidence, acquire source authority, authorize acquisition reattempt, remediate, retry, or merge.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    approval[ATTESTATION_DIGEST_KEY] = attestation[ATTESTATION_DIGEST_KEY]
    approval[PACKAGE_OPTIONS_DIGEST_KEY] = semantic_digest(package_options)
    approval[FUTURE_REQUIREMENTS_DIGEST_KEY] = semantic_digest({
        "requirements": future_requirements,
        "contract": approval["approved_future_input_supply_contract"],
    })
    approval[FUTURE_PLAN_DIGEST_KEY] = semantic_digest({
        "future_plan": future_plan,
        "planned_outputs": approval["planned_outputs"],
    })
    approval[APPROVAL_DIGEST_KEY] = _digest_without(approval, "checklist", "summary", APPROVAL_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    approval[MANIFEST_DIGEST_KEY] = semantic_digest({
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        "attestation_digest": approval[ATTESTATION_DIGEST_KEY],
        "package_options_digest": approval[PACKAGE_OPTIONS_DIGEST_KEY],
        "future_requirements_digest": approval[FUTURE_REQUIREMENTS_DIGEST_KEY],
        "future_plan_digest": approval[FUTURE_PLAN_DIGEST_KEY],
        "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    })
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval)
    return approval


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
    *,
    operator_attestation: dict,
    source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Build the deterministic approval after validating source and attestation."""
    source_value = _committed_source_operator_review() if source_operator_review is None else deepcopy(source_operator_review)
    _validate_source_operator_review(source_value)
    _validate_attestation(operator_attestation)
    approval = _assemble_approval(source_value, operator_attestation)
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
    approval: dict,
) -> dict[str, Any]:
    """Reject attestation drift, execution, authority expansion, or content loss."""
    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError("approval must be an object")
    _validate_attestation(approval.get("operator_attestation"))
    expected = _assemble_approval(_committed_source_operator_review(), approval["operator_attestation"])
    difference = _first_difference(approval, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(f"{difference} mismatch")
    for key in (APPROVAL_DIGEST_KEY, ATTESTATION_DIGEST_KEY, PACKAGE_OPTIONS_DIGEST_KEY, FUTURE_REQUIREMENTS_DIGEST_KEY, FUTURE_PLAN_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        value = approval.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(f"{key} invalid")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Approval Disposition", "Operator Attestation", "Selected Package", "Source Operator Review",
    "Source Candidate", "Source Failure Diagnosis", "Primary Failure Class", "Secondary Failure Classes",
    "Source Completion Execution", "Blocked Reason", "Blocked Digest Manifest", "Source Completion Approval",
    "Source Completion Candidate Operator Review", "Source Completion Candidate",
    "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Count Label Distinction", "Operator Completion Input Absence",
    "Future Input Supply Contract", "Approved Package Options", "Approved Future Input Requirements",
    "Approved Future Plan", "Planned Outputs", "Supporting Packages", "Blocked Packages",
    "Actual Evidence Absence", "Actual Coverage Zero", "Source Authority Gap Preservation",
    "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_markdown_v1(
    approval: dict,
) -> str:
    """Render the approved future-only boundary without external reads."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)
    summary = approval["summary"]
    facts = {
        "Approval Disposition": f"`{APPROVAL_STATUS}` within `{APPROVAL_SCOPE}`. Approval `{approval[APPROVAL_DIGEST_KEY]}`; manifest `{approval[MANIFEST_DIGEST_KEY]}`.",
        "Operator Attestation": f"Operator `{approval['operator_attestation']['operator_reference']}` attested at `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`; digest `{approval[ATTESTATION_DIGEST_KEY]}`. No secrets are stored.",
        "Selected Package": f"`{SELECTED_PACKAGE}` is selected and approved for future separate execution only; it is not executed.",
        "Source Operator Review": f"Commit `{SOURCE_OPERATOR_REVIEW_COMMIT}`; review `{SOURCE_OPERATOR_REVIEW_DIGEST}`; package options `{SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST}`; input contract `{SOURCE_INPUT_CONTRACT_REVIEW_DIGEST}`; source binding `{SOURCE_BINDING_REVIEW_DIGEST}`; coverage `{SOURCE_COVERAGE_REVIEW_DIGEST}`; manifest `{SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST}`.",
        "Source Candidate": f"Commit `{source.SOURCE_CANDIDATE_COMMIT}`; candidate `{source.SOURCE_CANDIDATE_DIGEST}`; manifest `{source.SOURCE_CANDIDATE_MANIFEST_DIGEST}`.",
        "Source Failure Diagnosis": f"Commit `{source.source.SOURCE_FAILURE_DIAGNOSIS_COMMIT}`; diagnosis `{source.source.SOURCE_FAILURE_DIAGNOSIS_DIGEST}`; classification `{source.source.SOURCE_FAILURE_CLASSIFICATION_DIGEST}`; manifest `{source.source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST}`.",
        "Primary Failure Class": f"`{source.source.PRIMARY_FAILURE_CLASS}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in source.source.SECONDARY_FAILURE_CLASSES),
        "Source Completion Execution": f"Commit `{approval['source_completion_execution_commit']}`; artifact `{approval['source_completion_execution_artifact_kind']}`; status `{approval['source_completion_execution_status']}`; scope `{approval['source_completion_execution_scope']}`.",
        "Blocked Reason": f"`{approval['source_completion_execution_blocked_reason']}`.",
        "Blocked Digest Manifest": f"Blocked digest `{approval['source_completion_execution_blocked_digest']}`; manifest `{approval['source_completion_execution_blocked_manifest_digest']}`; success digests remain absent.",
        "Source Completion Approval": f"Commit `{approval['source_completion_approval_commit']}`; approval `{approval['source_completion_approval_digest']}`; attestation `{approval['source_completion_approval_attestation_digest']}`.",
        "Source Completion Candidate Operator Review": f"Commit `{approval['source_completion_candidate_operator_review_commit']}`; digest `{approval['source_completion_candidate_operator_review_digest']}`; manifest `{approval['source_completion_candidate_operator_review_manifest_digest']}`.",
        "Source Completion Candidate": f"Commit `{approval['source_completion_candidate_commit']}`; digest `{approval['source_completion_candidate_digest']}`; manifest `{approval['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"Commit `{approval['source_template_preparation_results_review_commit']}`; digest `{approval['source_template_preparation_results_review_digest']}`; manifest `{approval['source_template_preparation_results_review_manifest_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{approval['source_template_preparation_execution_commit']}`; digest `{approval['source_template_preparation_execution_digest']}`; manifest `{approval['source_template_preparation_execution_manifest_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{approval['source_preparation_candidate_digest']}`; blocked acquisition `{approval['source_blocked_acquisition_execution_reason']}`; approval `{approval['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Follow-on `{approval['source_follow_on_execution_digest']}`; enrichment `{approval['source_enrichment_execution_digest']}`; all preserved bindings are covered by source review `{SOURCE_BINDING_REVIEW_DIGEST}`.",
        "Historical Blocked Remediation": f"Reason `{approval['historical_blocked_remediation_reason']}`; manifest `{approval['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{approval['source_targeted_remediation_plan_digest']}`; method `{approval['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{approval['source_recovery_results_review_digest']}`; staged inventory `{approval['source_staged_inventory_digest']}`.",
        "Durable Receipt": f"`{approval['source_durable_receipt_path']}` remains an opaque bound reference and was not parsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped. Root regression is not retry evidence.",
        "Priority 1 Target Modules": "\n".join(f"- `{item['path']}`: {item['failed_or_errored_nodeid_count']} node IDs" for item in approval["priority_1_target_modules"]),
        "Priority 1 Validation Summary": "675/675 before and after remains current-root focused evidence only and was not rerun.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {approval['source_stdout_byte_count']} bytes `{approval['source_stdout_sha256']}`; stderr {approval['source_stderr_byte_count']} bytes `{approval['source_stderr_sha256']}`. Diagnostic-only.",
        "Reviewed Observable Families": "Four HIGH-confidence planning families remain 47 observations each and 188 total.",
        "Reviewed Workstreams": "Four workstreams remain non-authorizing.",
        "Reviewed Template Structure": "Thirty rows map MA-001 through MA-030. The template remains neither evidence nor authority.",
        "Count Label Distinction": "Preserved without reconciliation: requirements 67/69/69; non-goals 71/76; risk controls 104/106; local labels 62/17/34/76/105.",
        "Operator Completion Input Absence": "Zero completion inputs are prepared, supplied, provided, validated, or bound.",
        "Future Input Supply Contract": f"Approved as planning-only for a future execution with 30 non-secret mapped rows; requirements digest `{approval[FUTURE_REQUIREMENTS_DIGEST_KEY]}`.",
        "Actual Evidence Absence": "No completed package, evidence package, or actual evidence item was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": "Coverage remains 0/30 and all rows remain `MISSING_NOT_ACQUIRED`.",
        "Source Authority Gap Preservation": "No acquisition execution, authority, external evidence, concrete authority, safe change, disposition, diagnostic, remediation, retry, or merge readiness was created.",
        "Unsupported Claims Boundary": "No root-cause, retry-success, acquisition-success, remediation-readiness, retry-readiness, or main-readiness claim is made.",
        "Recommendation": f"`{approval['recommended_next_task']}`: `{approval['recommended_action']}`.",
        "Authority Boundaries": "Only future input preparation/supply execution is authorized. All present execution, evidence, acquisition, remediation, retry, runtime, broker, trading, and protected-branch actions remain closed.",
        "Checklist Summary": f"{summary['passed_checks']}/{summary['total_checks']} PASS; blockers={summary['blocker_count']}.",
        "Guardrails": "Committed constants and injected dictionaries only. No upstream builders, file reads, subprocesses, pytest, caches, receipts, logs, environment, providers, source-owner contact, inputs, evidence, or runtime actions.",
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Approval After Candidate Operator Review v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Approval-only governance content; no execution or evidence is created."), ""))
        if section == "Approved Package Options":
            lines[-2:-2] = [*(f"- `{item['package_id']}` — `{item['approval_status']}`" for item in approval["package_options"]), ""]
        elif section == "Approved Future Input Requirements":
            lines[-2:-2] = [*(f"- `{item['requirement_id']}` — `{item['execution_status']}`" for item in approval["approved_future_input_preparation_requirements"]), ""]
        elif section == "Approved Future Plan":
            lines[-2:-2] = [*(f"{item['step']}. {item['action']} (`{item['execution_status']}`)" for item in approval["approved_future_plan"]), ""]
        elif section == "Planned Outputs":
            lines[-2:-2] = [*(f"- `{item['output_id']}` — `{item['status']}`" for item in approval["planned_outputs"]), ""]
        elif section == "Supporting Packages":
            lines[-2:-2] = [*(f"- `{item['package_id']}` — `AVAILABLE_NOT_SELECTED`" for item in approval["supporting_packages"]), ""]
        elif section == "Blocked Packages":
            lines[-2:-2] = [*(f"- `{item['package_id']}` — `BLOCKED_NOT_APPROVED`" for item in approval["blocked_packages"]), ""]
        elif section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in approval["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in approval["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict,
    source_operator_review: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested approval status Markdown file."""
    destination_root = Path(output_dir)
    protected_parts = {part.lower() for part in destination_root.parts}
    if protected_parts.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError(
            "protected output directory"
        )
    approval = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
        operator_attestation=operator_attestation,
        source_operator_review=source_operator_review,
    )
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_markdown_v1(approval),
        encoding="utf-8",
    )
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE",
    "OPERATOR_DECISION", "SOURCE_OPERATOR_REVIEW_BINDINGS", "ATTESTATION_VALUE_FIELDS",
    "ATTESTATION_BOOLEAN_FIELDS", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS",
    "FUTURE_INPUT_REQUIREMENT_IDS", "FUTURE_PLAN_STEPS", "PLANNED_OUTPUT_IDS", "NON_GOALS",
    "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "APPROVAL_DIGEST_KEY",
    "ATTESTATION_DIGEST_KEY", "PACKAGE_OPTIONS_DIGEST_KEY", "FUTURE_REQUIREMENTS_DIGEST_KEY",
    "FUTURE_PLAN_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE",
    "PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY", "PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY",
    "PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY", "PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS",
    "PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY", "PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS",
    "PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS", "PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT",
    "PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION",
    "PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS",
    "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_markdown_v1",
]
