"""Approve future evidence-package template preparation without executing it."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY"
OPERATOR_DECISION = "APPROVE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_FOR_FUTURE_EXECUTION"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_V1"

SOURCE_OPERATOR_REVIEW_COMMIT = "139b03c87e9ce48b38435c7dcc0761c2300a7a4b"
SOURCE_OPERATOR_REVIEW_DIGEST = "36e75dec88c71cc2e73109254a5a37b3b8e6415b598b0b8b4f7a025c3911bc22"
SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST = "39aa0548562fd85763fc937fe3c306734a60749500b3607a75f42ad9b3e62ae8"
SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST = "ac2fff06d39bd4361a81b7a26fec8bc43f18c8da1169bc38cde3ede9476d5c18"
SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST = "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "30d2cba7243845b01df595ce922c07dae7a4d876345022e7d51046bf8b76c8df"

SOURCE_PREPARATION_CANDIDATE_COMMIT = "8d2944edfb7a54056f4a59c3d5817e823da80ce8"
SOURCE_PREPARATION_CANDIDATE_DIGEST = "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391"
SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST = "5eb1efe8ccb86f243c3db861b983c86fff9b9b868b146ae866da29975cfca400"
SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST = "3dd55cbdcf191c46c2bd5d314a20019c59b107029e6fd178754d79eddc06b2d7"
SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST = "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"
SOURCE_PREPARATION_MANIFEST_DIGEST = "c95671cf372c8bdf7f15c019bd994ae58f547d025117e12456fd780b5f9fd3d3"

SOURCE_FAILURE_DIAGNOSIS_DIGEST = "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c"
SOURCE_BLOCKED_REASON = "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
SOURCE_BLOCKED_MANIFEST_DIGEST = "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"
SOURCE_APPROVAL_DIGEST = "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"
SOURCE_ATTESTATION_DIGEST = "db079d7b71f141dafba8439eba51caa1bc663ddf1158d3ea34b1f102ce4fb879"

APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_digest"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY "
    "AFTER OPERATOR SOURCE AUTHORITY EVIDENCE PACKAGE PREPARATION CANDIDATE OPERATOR REVIEW FOR FUTURE TEMPLATE PREPARATION EXECUTION ONLY "
    "NO EVIDENCE PACKAGE CREATION NOW NO SOURCE AUTHORITY ACQUISITION NOW NO EVIDENCE ACQUISITION NOW NO EVIDENCE VALIDATION NOW NO EVIDENCE "
    "BINDING NOW NO ACQUISITION REATTEMPT NOW NO NO CHANGE DISPOSITION NOW NO ALTERNATE DIAGNOSTICS NOW NO REMEDIATION NOW NO CODE CHANGES NOW "
    "NO TEST CHANGES NOW NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_"
    "PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_"
    "NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY = SELECTED_PACKAGE


TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_preparation_approval_created
operator_source_authority_evidence_package_preparation_package_selected
operator_source_authority_evidence_package_preparation_package_approved
operator_source_authority_evidence_package_preparation_package_authorized_for_future_execution
selected_preparation_package_verified
source_operator_review_bound
source_preparation_candidate_bound
source_package_options_review_bound
source_template_requirements_review_bound
source_missing_authority_coverage_review_bound
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_approval_bound
source_acquisition_candidate_operator_review_bound
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
missing_authority_inventory_bound
zero_coverage_bound
evidence_package_absence_bound
candidate_philosophy_reviewed
preparation_package_options_reviewed
recommended_preparation_package_reviewed
future_requirements_approved
future_plan_approved
planned_outputs_authorized_not_generated
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_preparation_execution_after_approval""".splitlines())

FALSE_FIELDS = tuple("""operator_source_authority_evidence_package_preparation_execution_performed
operator_source_authority_evidence_package_preparation_package_executed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
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

FUTURE_PERMISSION_TRUE_FIELDS = tuple("""future_execution_may_create_non_secret_operator_fillable_template
future_execution_may_create_preparation_checklist
future_execution_may_preserve_reviewed_scope_and_missing_authority_mappings
future_execution_may_preserve_source_artifact_and_custody_requirements
future_execution_may_define_template_preparation_results_review_package""".splitlines())

FUTURE_PERMISSION_FALSE_FIELDS = tuple("""future_execution_may_create_real_evidence
future_execution_may_acquire_source_authority
future_execution_may_acquire_or_bind_source_authority_evidence
future_execution_may_validate_evidence_package
future_execution_may_retry_source_authority_acquisition
future_execution_may_execute_remediation
future_execution_may_modify_production_code
future_execution_may_modify_existing_tests
future_execution_may_update_expected_digests
future_execution_may_generate_or_apply_patch
future_execution_may_run_full_pytest
future_execution_may_run_retry
future_execution_may_create_retry_candidate
future_execution_may_create_no_change_disposition
future_execution_may_push_main
future_execution_may_push_integration_branch
future_template_preparation_execution_executed""".splitlines())

SUPPORTING_PACKAGE_IDS = (
    source.PACKAGE_CREATE_SOURCE_OWNER_REQUEST_REQUIREMENTS_FOR_30_MISSING_AUTHORITY_ITEMS,
    source.PACKAGE_CREATE_LIMITED_ASSERTION_VALUE_SOURCE_EVIDENCE_TEMPLATE,
    source.PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_SOURCE_EVIDENCE_TEMPLATE,
    source.PACKAGE_CREATE_LIMITED_FIXTURE_DETERMINISM_SOURCE_EVIDENCE_TEMPLATE,
    source.PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_SOURCE_EVIDENCE_TEMPLATE,
    source.PACKAGE_HOLD_PENDING_OPERATOR_SOURCE_AUTHORITY_EVIDENCE,
)
BLOCKED_PACKAGE_IDS = (
    source.PACKAGE_GENERATE_EVIDENCE_FROM_DIAGNOSTIC_OUTPUT,
    source.PACKAGE_ACCEPT_APPROVAL_AS_OPERATOR_EVIDENCE_PACKAGE,
    source.PACKAGE_FABRICATE_OR_INFER_MISSING_SOURCE_AUTHORITY_EVIDENCE,
    source.PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_WITHOUT_EVIDENCE_PACKAGE,
    source.PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_MISSING_EVIDENCE_DIAGNOSIS,
)


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(ValueError):
    """Raised when approval evidence or its authority boundary differs."""


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
candidate_results_review_requirements_review
evidence_package_absence
missing_authority_coverage
secondary_failure_classes
historical_secondary_failure_classes
historical_blocked_remediation_summary""".splitlines())


def _committed_source_operator_review() -> dict[str, Any]:
    """Reconstruct only from committed data constants; no upstream builder runs."""

    candidate = source._COMMITTED_SOURCE_PREPARATION_CANDIDATE
    review = {
        key: deepcopy(value)
        for key, value in candidate.items()
        if key.startswith("source_") or key in SOURCE_CONTEXT_KEYS
    }
    review.update({
        "artifact_kind": source.ARTIFACT_KIND,
        "operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        "source_preparation_candidate_commit": SOURCE_PREPARATION_CANDIDATE_COMMIT,
        "source_preparation_candidate_digest": SOURCE_PREPARATION_CANDIDATE_DIGEST,
        "source_preparation_package_options_digest": SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST,
        "source_preparation_template_requirements_digest": SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST,
        "source_preparation_missing_authority_coverage_digest": SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST,
        "source_preparation_manifest_digest": SOURCE_PREPARATION_MANIFEST_DIGEST,
        "source_blocked_acquisition_execution_reason": SOURCE_BLOCKED_REASON,
        "source_blocked_acquisition_execution_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "selected_source_authority_acquisition_package": candidate["selected_source_authority_acquisition_package"],
        "primary_failure_class": candidate["primary_failure_class"],
        "historical_blocked_remediation_execution_commit": candidate["historical_blocked_remediation_execution_commit"],
        "historical_blocked_remediation_reason": candidate["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": candidate["historical_blocked_remediation_manifest_digest"],
        "historical_primary_failure_class": candidate["historical_primary_failure_class"],
        "reviewed_candidate_philosophy": candidate["candidate_philosophy"],
        "reviewed_candidate_boundary": candidate["candidate_boundary"],
        "reviewed_package_options": deepcopy(candidate["reviewed_package_options"]),
        "reviewed_future_requirements": [
            {
                "requirement_id": item["requirement_id"],
                "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION",
                "execution_status": "NOT_EXECUTED",
            }
            for item in candidate["future_evidence_package_preparation_requirements"]
        ],
        "reviewed_future_plan": [
            {"step": index, "description": description, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED"}
            for index, description in enumerate(source.PLAN_STEPS, 1)
        ],
        "reviewed_planned_outputs": [
            {"output_id": item, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
            for item in source.source.OUTPUT_IDS
        ],
        "reviewed_non_goals": [
            {"non_goal_id": item, "review_status": "REVIEWED_ACTIVE", "active": True}
            for item in source.source.NON_GOAL_IDS
        ],
        "next_chain": list(source.NEXT_CHAIN),
        "next_gates": list(source.NEXT_GATES),
        "risk_controls": list(source.RISK_CONTROLS),
    })
    return review


SOURCE_REVIEW_DIGEST_FIELDS = {
    source.OPERATOR_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
    source.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    source.TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY: SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST,
    source.COVERAGE_REVIEW_DIGEST_KEY: SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST,
    source.MANIFEST_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
}


def _validate_source_operator_review(review: Mapping[str, Any]) -> None:
    committed = _committed_source_operator_review()
    for key, expected in committed.items():
        if key not in review or _first_difference(review[key], expected, f"source_operator_review.{key}"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(
                f"source_operator_review.{key} mismatch"
            )
    for key, expected in SOURCE_REVIEW_DIGEST_FIELDS.items():
        if review.get(key) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(
                f"source_operator_review.{key} mismatch"
            )


ATTESTATION_VALUE_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "operator_confirms_source_template_requirements_review_digest": SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST,
    "operator_confirms_source_missing_authority_coverage_review_digest": SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST,
    "operator_confirms_source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
    "operator_confirms_source_preparation_candidate_digest": SOURCE_PREPARATION_CANDIDATE_DIGEST,
    "operator_confirms_source_preparation_package_options_digest": SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST,
    "operator_confirms_source_preparation_template_requirements_digest": SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST,
    "operator_confirms_source_preparation_missing_authority_coverage_digest": SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST,
    "operator_confirms_source_preparation_manifest_digest": SOURCE_PREPARATION_MANIFEST_DIGEST,
    "operator_confirms_source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_blocked_reason": SOURCE_BLOCKED_REASON,
    "operator_confirms_source_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
    "operator_confirms_source_approval_digest": SOURCE_APPROVAL_DIGEST,
    "operator_confirms_source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
    "operator_confirms_selected_preparation_package": SELECTED_PACKAGE,
}

ATTESTATION_BOOLEAN_FIELDS = tuple("""operator_confirms_retry_failure_counts
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_workstream_count_4
operator_confirms_acquisition_scope_section_count_4
operator_confirms_mapped_missing_authority_item_count_30
operator_confirms_acceptable_source_artifact_type_count_13
operator_confirms_operator_provided_evidence_requirement_count_10
operator_confirms_evidence_custody_and_digest_requirement_count_6
operator_confirms_candidate_results_review_requirement_count_16
operator_confirms_package_option_count_12
operator_confirms_available_package_count_7
operator_confirms_blocked_package_count_5
operator_confirms_future_requirement_count_62
operator_confirms_future_plan_step_count_15
operator_confirms_planned_output_count_28
operator_confirms_non_goal_count_71
operator_confirms_risk_control_count_104
operator_confirms_missing_authority_items_missing_not_acquired
operator_confirms_zero_coverage
operator_confirms_approval_scope_only
operator_confirms_no_template_preparation_execution_now
operator_confirms_no_evidence_package_creation_now
operator_confirms_no_source_authority_acquisition_now
operator_confirms_no_source_authority_evidence_acquisition_now
operator_confirms_no_external_evidence_acquisition_now
operator_confirms_no_evidence_validation_now
operator_confirms_no_evidence_binding_now
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


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    selected_operator_source_authority_evidence_package_preparation_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
    operator_confirmations: dict,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    if not isinstance(operator_reference, str) or not operator_reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("operator_reference invalid")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(operator_attestation_timestamp_utc)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("operator_attestation_timestamp_utc invalid")
    if operator_attestation_phrase != REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("operator_attestation_phrase mismatch")
    if selected_operator_source_authority_evidence_package_preparation_package != SELECTED_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("selected preparation package mismatch")
    if operator_decision != OPERATOR_DECISION:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("operator_decision mismatch")
    expected_confirmations = {**ATTESTATION_VALUE_FIELDS, **{key: True for key in ATTESTATION_BOOLEAN_FIELDS}}
    difference = _first_difference(operator_confirmations, expected_confirmations, "operator_confirmations")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(f"{difference} mismatch")
    attestation = {
        "operator_decision": OPERATOR_DECISION,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": SCHEMA_VERSION,
        "operator_reference": operator_reference.strip(),
        **deepcopy(operator_confirmations),
    }
    attestation[ATTESTATION_DIGEST_KEY] = semantic_digest(attestation)
    return attestation


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("operator_attestation must be an object")
    digest = attestation.get(ATTESTATION_DIGEST_KEY)
    confirmations = {key: attestation.get(key) for key in (*ATTESTATION_VALUE_FIELDS, *ATTESTATION_BOOLEAN_FIELDS)}
    rebuilt = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1(
        operator_reference=attestation.get("operator_reference"),
        operator_attestation_timestamp_utc=attestation.get("operator_attestation_timestamp_utc"),
        operator_attestation_phrase=attestation.get("operator_attestation_phrase"),
        selected_operator_source_authority_evidence_package_preparation_package=attestation.get("selected_operator_source_authority_evidence_package_preparation_package"),
        operator_decision=attestation.get("operator_decision"),
        operator_confirmations=confirmations,
    )
    difference = _first_difference(dict(attestation), rebuilt, "operator_attestation")
    if difference or digest != rebuilt[ATTESTATION_DIGEST_KEY]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(f"{difference or ATTESTATION_DIGEST_KEY} mismatch")


def _source_bindings(review: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {key: deepcopy(value) for key, value in review.items() if key.startswith("source_")}
    bindings.update({
        "source_acquisition_candidate_operator_review_summary": deepcopy(review["source_operator_review_summary"]),
        "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "source_operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
        "source_template_requirements_review_digest": SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST,
        "source_missing_authority_coverage_review_digest": SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST,
        "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        "source_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "status": source.OPERATOR_REVIEW_STATUS,
            "scope": source.OPERATOR_REVIEW_SCOPE,
            "commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "digest": SOURCE_OPERATOR_REVIEW_DIGEST,
            "checks": "465/465 PASS",
        },
        "source_preparation_candidate_commit": SOURCE_PREPARATION_CANDIDATE_COMMIT,
        "source_preparation_candidate_digest": SOURCE_PREPARATION_CANDIDATE_DIGEST,
        "source_preparation_package_options_digest": SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST,
        "source_preparation_template_requirements_digest": SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST,
        "source_preparation_missing_authority_coverage_digest": SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST,
        "source_preparation_manifest_digest": SOURCE_PREPARATION_MANIFEST_DIGEST,
    })
    return bindings


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for key in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_approval(review: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    requirement_status = "APPROVED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_EXECUTION_ONLY"
    counts = {
        "operator_source_authority_evidence_item_count": 0,
        "covered_missing_authority_item_count": 0,
        "uncovered_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "acquisition_scope_section_count": 4,
        "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6,
        "candidate_results_review_requirement_count": 16,
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "package_option_count": 12,
        "available_package_count": 7,
        "blocked_package_count": 5,
        "future_requirement_count": 62,
        "future_plan_step_count": 15,
        "planned_output_count": 28,
        "non_goal_count": 71,
        "risk_control_count": 104,
    }
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
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "selected_source_authority_acquisition_package": review["selected_source_authority_acquisition_package"],
        **_source_bindings(review),
        **{key: deepcopy(review[key]) for key in SOURCE_CONTEXT_KEYS},
        "primary_failure_class": review["primary_failure_class"],
        "historical_primary_failure_class": review["historical_primary_failure_class"],
        "historical_blocked_remediation_execution_commit": review["historical_blocked_remediation_execution_commit"],
        "historical_blocked_remediation_reason": review["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": review["historical_blocked_remediation_manifest_digest"],
        **counts,
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "approved_package": {
            "package_id": SELECTED_PACKAGE,
            "source_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "approval_status": requirement_status,
            "selected": True,
            "approved": True,
            "authorized_for_future_execution": True,
            "executed": False,
            "purpose": "Future execution may create a non-secret, operator-fillable source-authority evidence package template and preparation checklist based only on reviewed acquisition scope, 30 missing-authority mappings, 13 acceptable source-artifact types, 10 operator-provided evidence requirements, six custody/digest requirements, and 16 candidate results-review requirements.",
            "future_execution_boundary": "Future execution may create a template and checklist only. It may not create real evidence, acquire source authority, bind evidence, validate an evidence package, retry acquisition, authorize remediation, authorize retry, create no-change disposition, modify code/tests/digests, generate/apply patches, push protected branches, call providers, inspect secrets, or authorize runtime/trading.",
        },
        "approved_future_requirements": [
            {"requirement_id": item["requirement_id"], "approval_status": requirement_status, "execution_status": "NOT_EXECUTED"}
            for item in review["reviewed_future_requirements"]
        ],
        "approved_future_plan": [
            {"step_id": index, "step": item["description"], "approval_status": requirement_status, "execution_status": "NOT_EXECUTED"}
            for index, item in enumerate(review["reviewed_future_plan"], 1)
        ],
        "future_execution_boundary": {
            "future_template_preparation_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
            "future_template_preparation_execution_input_source": "REVIEWED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW",
            "future_template_preparation_execution_type": "NON_SECRET_OPERATOR_FILLABLE_TEMPLATE_AND_PREPARATION_CHECKLIST_ONLY",
            **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
            **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        },
        **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
        **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        "future_template_preparation_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "planned_outputs": [{"output_id": item["output_id"], "status": "AUTHORIZED_NOT_GENERATED"} for item in review["reviewed_planned_outputs"]],
        "supporting_packages": [
            {"package_id": item, "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False, "authorized": False, "executed": False}
            for item in SUPPORTING_PACKAGE_IDS
        ],
        "blocked_packages": [
            {"package_id": item, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "authorized": False, "executed": False}
            for item in BLOCKED_PACKAGE_IDS
        ],
        "approved_non_goals": deepcopy(review["reviewed_non_goals"]),
        "next_chain": deepcopy(review["next_chain"]),
        "next_gates": deepcopy(review["next_gates"]),
        "risk_controls": deepcopy(review["risk_controls"]),
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
    source_binding_checks = tuple(
        f"{key}_bound" for key in sorted(approval)
        if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit"))
    )
    check_ids = tuple(dict.fromkeys((
        "attestation_valid", "source_operator_review_bound", "selected_package_approved_for_future_execution",
        "approved_future_requirements_62", "approved_future_plan_15", "planned_outputs_28",
        "supporting_packages_6", "blocked_packages_5", "non_goals_71", "risk_controls_104",
        "acquisition_scope_sections_4", "mapped_missing_authority_items_30",
        "acceptable_source_artifact_types_13", "operator_provided_evidence_requirements_10",
        "evidence_custody_and_digest_requirements_6", "candidate_results_review_requirements_16",
        "artifact_digest_deterministic", *source_binding_checks,
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"{field}_future_true" for field in FUTURE_PERMISSION_TRUE_FIELDS),
        *(f"{field}_future_false" for field in FUTURE_PERMISSION_FALSE_FIELDS),
        *(f"requirement_{item['requirement_id']}_approved" for item in review["reviewed_future_requirements"]),
        *(f"plan_step_{index}_approved" for index in range(1, 16)),
        *(f"output_{item['output_id']}_authorized" for item in review["reviewed_planned_outputs"]),
        *(f"supporting_package_{item}_preserved" for item in SUPPORTING_PACKAGE_IDS),
        *(f"blocked_package_{item}_blocked" for item in BLOCKED_PACKAGE_IDS),
        *(f"next_chain_step_{index}_defined" for index in range(1, len(review["next_chain"]) + 1)),
        *(f"next_gate_{item}_defined" for item in review["next_gates"]),
        *(f"risk_control_{item}_defined" for item in review["risk_controls"]),
    )))
    approval["checklist"] = [
        {"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"}
        for item in check_ids
    ]
    approval["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_preparation_approval_created": True,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "ready_for_operator_source_authority_evidence_package_preparation_execution_after_approval": True,
        **counts,
        **{field: False for field in FALSE_FIELDS},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    return approval


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict
) -> dict[str, Any]:
    """Build the attestation-bound future-execution approval offline."""

    review = _committed_source_operator_review() if source_operator_review is None else deepcopy(source_operator_review)
    if source_operator_review is None:
        review.update(SOURCE_REVIEW_DIGEST_FIELDS)
    _validate_source_operator_review(review)
    _validate_attestation(operator_attestation)
    approval = _assemble_approval(review, operator_attestation)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
    approval: dict,
) -> dict[str, Any]:
    """Reject any changed source binding, approval fact, or closed boundary."""

    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("approval must be an object")
    _validate_attestation(approval.get("operator_attestation", {}))
    review = _committed_source_operator_review()
    review.update(SOURCE_REVIEW_DIGEST_FIELDS)
    expected = _assemble_approval(review, approval["operator_attestation"])
    difference = _first_difference(approval, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError(f"{difference} mismatch")
    if re.fullmatch(r"[0-9a-f]{64}", str(approval.get(APPROVAL_DIGEST_KEY))) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("approval digest invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Operator Attestation
Source Operator Review
Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Blocked Reason
Failure Classification
Source Approval
Selected Source Authority Acquisition Package
Source Acquisition Candidate Operator Review
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
Historical Failure Diagnosis
Historical Blocked Remediation
Source Plan Results Review
Source Plan Execution
Source Method Results Review
Source Method Execution
Source Diagnostic Results Review
Source Controlled Recapture
Source Durable Receipt
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
Approved Package
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


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated approval status document."""

    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(deepcopy(approval))
    lookup = {
        "Operator Attestation": approval["operator_attestation"],
        "Source Operator Review": approval["source_operator_review_summary"],
        "Source Preparation Candidate": {key: approval[key] for key in ("source_preparation_candidate_commit", "source_preparation_candidate_digest", "source_preparation_manifest_digest")},
        "Source Failure Diagnosis": approval["source_failure_diagnosis_summary"],
        "Source Blocked Acquisition Execution": approval["source_blocked_acquisition_execution_summary"],
        "Blocked Reason": approval["source_blocked_reason"],
        "Failure Classification": {"primary": approval["primary_failure_class"], "secondary": approval["secondary_failure_classes"]},
        "Source Approval": approval["source_approval_summary"],
        "Selected Source Authority Acquisition Package": approval["selected_source_authority_acquisition_package"],
        "Source Acquisition Candidate Operator Review": approval["source_acquisition_candidate_operator_review_summary"],
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
        "Historical Failure Diagnosis": approval["source_failure_diagnosis_summary"],
        "Historical Blocked Remediation": approval["historical_blocked_remediation_summary"],
        "Source Plan Results Review": approval["source_plan_results_review_summary"],
        "Source Plan Execution": approval["source_plan_execution_summary"],
        "Source Method Results Review": approval["source_method_results_review_summary"],
        "Source Method Execution": approval["source_method_execution_summary"],
        "Source Diagnostic Results Review": approval["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": approval["source_controlled_recapture_summary"],
        "Source Durable Receipt": approval["source_durable_receipt_summary"],
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
        "Approved Package": approval["approved_package"],
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
        "# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Approval After Candidate Operator Review v1",
        "", f"Artifact: `{approval['artifact_kind']}`", "", f"Status: `{approval['approval_status']}`", "",
        f"Scope: `{approval['approval_scope']}`", "", f"Approval digest: `{approval[APPROVAL_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(lookup[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict
) -> dict[str, Any]:
    """Write the deterministic approval status document outside protected paths."""

    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation
    )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_markdown_v1(approval), encoding="utf-8")
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE",
    "APPROVAL_DIGEST_KEY", "ATTESTATION_DIGEST_KEY", "ATTESTATION_VALUE_FIELDS", "ATTESTATION_BOOLEAN_FIELDS",
    "REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_markdown_v1",
]
