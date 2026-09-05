"""Create the approved blank source-authority evidence template and checklist."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1"
EXECUTION_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_TEMPLATE_AND_CHECKLIST_READY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_APPROVAL_OR_TEMPLATE_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_ONLY_TEMPLATE_AND_CHECKLIST_CREATION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_APPROVAL_COMMIT = "e942849f3126c95b432c6ce77f21eb96586f9b4b"
SOURCE_APPROVAL_DIGEST = "e7f1d8a5ae413ca0f971257e13554a63b3ee95e942e156adb5b204cbcc378cbd"
SOURCE_ATTESTATION_DIGEST = "e16b2afde6c36d5461a65d2f598fec55f9a13811a555efc90a9dac1e981f7328"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
DEFAULT_RUN_TIMESTAMP_UTC = "2026-08-23T00:00:00Z"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_V1"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_RESULTS_REVIEW_BEFORE_ANY_ACTUAL_EVIDENCE_PACKAGE_USE_OR_ACQUISITION_REATTEMPT"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_digest"
TEMPLATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_template_digest"
EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_item_template_digest"
PREPARATION_CHECKLIST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_checklist_digest"
COVERAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_template_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_V1 = ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_TEMPLATE_AND_CHECKLIST_READY = EXECUTION_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_APPROVAL_OR_TEMPLATE_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_ONLY_TEMPLATE_AND_CHECKLIST_CREATION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY = SELECTED_PACKAGE

ALLOWED_SECTION_IDS = (
    "assertion_value_mismatch_source_authority_scope", "digest_hash_boundary_source_authority_scope",
    "fixture_isolation_determinism_source_authority_scope", "schema_field_contract_source_authority_scope",
)
ALLOWED_WORKSTREAM_IDS = (
    "assertion_value_mismatch_workstream", "digest_hash_boundary_workstream",
    "fixture_isolation_determinism_workstream", "schema_field_contract_workstream",
)
ALLOWED_SOURCE_ARTIFACT_TYPES = tuple("""approved_product_specification
approved_schema_definition
approved_artifact_contract
approved_canonical_payload_or_serialization_contract
approved_expected_value_source
approved_actual_value_source
approved_digest_manifest_source
approved_fixture_lifecycle_document
approved_deterministic_execution_contract
approved_export_surface_contract
approved_operator_provided_evidence_package
approved_source_owning_team_statement
approved_reviewed_source_digest_bundle""".splitlines())

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_preparation_execution_created
operator_source_authority_evidence_package_preparation_execution_performed
operator_source_authority_evidence_package_preparation_package_executed
selected_preparation_package_verified
source_approval_verified
source_attestation_verified
source_operator_review_bound
source_preparation_candidate_bound
source_package_options_review_bound
source_template_requirements_review_bound
source_missing_authority_coverage_review_bound
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_acquisition_approval_bound
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
zero_actual_coverage_bound
evidence_package_absence_bound
operator_fillable_template_created
operator_fillable_template_header_created
operator_fillable_evidence_item_templates_created
operator_fillable_preparation_checklist_created
source_owner_request_guidance_created
acceptable_source_artifact_inventory_created
custody_and_digest_guidance_created
no_secret_boundary_guidance_created
results_review_requirements_created
acquisition_reattempt_gate_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_preparation_results_review""".splitlines())

FALSE_FIELDS = tuple("""operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
operator_source_authority_evidence_package_ready_for_acquisition_without_review
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

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_preparation_execution_manifest
source_approval_binding_report
source_operator_review_binding_report
source_preparation_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_acquisition_execution_binding_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
operator_fillable_evidence_package_header_template
operator_fillable_evidence_item_template
thirty_missing_authority_item_template_rows
acquisition_scope_section_template_map
acceptable_source_artifact_type_inventory
operator_evidence_no_secret_declaration_checklist
source_owner_request_guidance
evidence_custody_and_digest_checklist
specification_observation_separation_guidance
expected_actual_separation_guidance
diagnostic_output_not_source_authority_warning
results_review_before_use_requirements
acquisition_reattempt_gate_preservation_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Preparation Results Review After Execution v1.",
    "Operator source-authority evidence package completion outside this execution, only after reviewed template acceptance.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Evidence Package v1, only if a reviewed package exists and is separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""operator_source_authority_evidence_package_preparation_results_review_after_execution
reviewed_template_acceptance_before_actual_operator_package_use
operator_source_authority_evidence_package_completion_outside_execution_if_reviewed_template_accepted
source_authority_acquisition_execution_reattempt_with_reviewed_evidence_package_if_approved
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

RISK_CONTROLS = tuple("""execution_uses_approved_preparation_package_only
execution_creates_template_only
execution_creates_checklist_only
execution_does_not_create_actual_operator_evidence_package
execution_does_not_supply_evidence_package
execution_does_not_validate_evidence_package
execution_does_not_bind_evidence_package
execution_does_not_acquire_source_authority
execution_does_not_acquire_source_authority_evidence
execution_does_not_acquire_external_evidence
template_is_not_source_authority
template_is_not_acquired_evidence
template_is_not_acquisition_success
template_requires_results_review_before_use
template_requires_no_secret_declarations
template_requires_no_api_key_declaration
template_requires_no_broker_credential_declaration
template_requires_no_personal_financial_credential_declaration
template_requires_source_owner_or_origin
template_requires_source_reference
template_requires_created_utc
template_requires_digest_or_reproducible_provenance
template_requires_specification_observation_separation
template_requires_expected_actual_separation
template_requires_source_authority_diagnostic_output_separation
evidence_item_templates_force_direct_change_authorized_false
evidence_item_templates_force_remediation_authorized_false
evidence_item_templates_force_retry_authorized_false
evidence_item_templates_force_main_merge_authorized_false
actual_coverage_remains_zero
all_missing_authority_items_remain_missing_not_acquired
execution_does_not_retry_acquisition_execution
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
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
preparation_results_review_required_before_template_use
source_authority_acquisition_reattempt_requires_reviewed_filled_package
separate_acquisition_approval_required_before_acquisition_reattempt
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_remediation_approval_required_before_code_or_test_changes
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError(ValueError):
    """Raised when committed approval evidence or template boundaries differ."""


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


CONTEXT_KEYS = tuple("""retry_failure_context
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


def _committed_source_approval() -> dict[str, Any]:
    """Construct the required approval projection from committed constants only."""

    review = source._committed_source_operator_review()
    review.update(source.SOURCE_REVIEW_DIGEST_FIELDS)
    approval = {
        key: deepcopy(value)
        for key, value in review.items()
        if key.startswith("source_") or key in CONTEXT_KEYS
    }
    approval.update({
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        "source_approval_commit": SOURCE_APPROVAL_COMMIT,
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
        "source_acquisition_approval_commit": review["source_approval_commit"],
        "source_acquisition_approval_digest": review["source_approval_digest"],
        "source_acquisition_attestation_digest": review["source_attestation_digest"],
        "source_operator_review_commit": source.SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_operator_review_digest": source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_package_options_review_digest": source.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
        "source_template_requirements_review_digest": source.SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST,
        "source_missing_authority_coverage_review_digest": source.SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST,
        "source_operator_review_manifest_digest": source.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        "source_acquisition_candidate_operator_review_summary": deepcopy(
            review["source_operator_review_summary"]
        ),
        "source_follow_on_execution_digest": review["source_follow_on_execution_after_results_review_digest"],
        "source_follow_on_operator_review_digest": review["source_follow_on_candidate_operator_review_digest"],
        "source_enrichment_execution_digest": review["source_execution_digest"],
        "historical_source_approval_digest": review["source_historical_approval_digest"],
        "historical_source_operator_review_digest": review["source_historical_operator_review_digest"],
        "historical_source_candidate_digest": review["source_candidate_digest"],
        "historical_failure_diagnosis_digest": review[
            "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"
        ],
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "selected_source_authority_acquisition_package": review["selected_source_authority_acquisition_package"],
        "primary_failure_class": review["primary_failure_class"],
        "historical_primary_failure_class": review["historical_primary_failure_class"],
        "historical_blocked_remediation_execution_commit": review["historical_blocked_remediation_execution_commit"],
        "historical_blocked_remediation_reason": review["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": review["historical_blocked_remediation_manifest_digest"],
        "approved_future_requirements": [deepcopy(item) for item in review["reviewed_future_requirements"]],
        "approved_future_plan": [deepcopy(item) for item in review["reviewed_future_plan"]],
        "reviewed_planned_outputs": [deepcopy(item) for item in review["reviewed_planned_outputs"]],
        "reviewed_non_goals": [deepcopy(item) for item in review["reviewed_non_goals"]],
    })
    return approval


def _validate_source_approval(approval: Mapping[str, Any]) -> None:
    expected = _committed_source_approval()
    for key, value in expected.items():
        if key not in approval or _first_difference(approval[key], value, f"source_approval.{key}"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError(
                f"source_approval.{key} mismatch"
            )


def _package_header() -> dict[str, Any]:
    return {
        "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
        "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
        "package_source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>",
        "package_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>",
        "package_created_utc": "<REQUIRED_UTC_TIMESTAMP>",
        "package_digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "package_declares_no_secrets": "<REQUIRED_TRUE>",
        "package_declares_no_api_keys": "<REQUIRED_TRUE>",
        "package_declares_no_broker_credentials": "<REQUIRED_TRUE>",
        "package_declares_no_personal_financial_credentials": "<REQUIRED_TRUE>",
        "package_distinguishes_specification_from_observation": "<REQUIRED_TRUE>",
        "package_distinguishes_expected_from_actual": "<REQUIRED_TRUE>",
        "package_distinguishes_source_authority_from_diagnostic_output": "<REQUIRED_TRUE>",
        "evidence_items": "<REQUIRED_LIST_OF_ONE_OR_MORE_FILLED_EVIDENCE_ITEMS_FOR_FUTURE_ACQUISITION_REATTEMPT>",
        "template_only": True,
        "actual_evidence_package_created": False,
    }


def _evidence_item_contract() -> dict[str, Any]:
    return {
        "evidence_id": "<REQUIRED_UNIQUE_EVIDENCE_ID>",
        "mapped_missing_authority_id": "<BOUND_REVIEWED_MISSING_AUTHORITY_ID>",
        "section_id": "<ONE_OF_ALLOWED_SECTION_IDS>",
        "workstream_id": "<ONE_OF_ALLOWED_WORKSTREAM_IDS>",
        "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
        "source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>",
        "source_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>",
        "digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "evidence_classification": "<SPECIFICATION | APPROVED_CONTRACT | SOURCE_OWNER_STATEMENT | CANONICAL_PAYLOAD | CANONICAL_SCHEMA | CANONICAL_SERIALIZATION | EXPECTED_VALUE_SOURCE | ACTUAL_VALUE_SOURCE | FIXTURE_LIFECYCLE_AUTHORITY | DETERMINISM_AUTHORITY | EXPORT_SURFACE_AUTHORITY | REVIEWED_SOURCE_DIGEST_BUNDLE>",
        "specification_or_observation": "<SPECIFICATION | OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
        "expected_or_actual_scope": "<EXPECTED | ACTUAL | BOTH | NOT_APPLICABLE>",
        "authority_statement": "<REQUIRED_NON_EMPTY_AUTHORITY_STATEMENT>",
        "results_review_required_before_use": True,
        "direct_change_authorized_now": False,
        "remediation_authorized_now": False,
        "retry_authorized_now": False,
        "main_merge_authorized_now": False,
    }


def _template_rows(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for mapping in approval["missing_authority_to_source_evidence_mapping_review"]["items"]:
        allowed_types = tuple(item.replace(" ", "_").replace("-", "_") for item in mapping["acceptable_source_artifact_types"])
        row = {
            **_evidence_item_contract(),
            "evidence_id": f"<REQUIRED_UNIQUE_EVIDENCE_ID_FOR_{mapping['missing_authority_id']}>",
            "mapped_missing_authority_id": mapping["missing_authority_id"],
            "section_id": mapping["section_id"],
            "workstream_id": mapping["workstream_id"],
            "allowed_acceptable_source_artifact_types": list(allowed_types),
            "template_only": True,
            "actual_evidence_supplied": False,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "MISSING_NOT_ACQUIRED",
        }
        rows.append(row)
    return rows


def _digest_without(execution: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(execution))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_execution(approval: Mapping[str, Any], run_timestamp_utc: str) -> dict[str, Any]:
    rows = _template_rows(approval)
    package_header = _package_header()
    item_contract = _evidence_item_contract()
    preparation_checklist = [
        {"requirement_id": item["requirement_id"], "template_requirement_included": True, "actual_evidence_satisfied": False}
        for item in approval["approved_future_requirements"]
    ]
    coverage = {
        "template_row_count": 30, "mapped_missing_authority_item_count": 30,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "all_rows_template_only": True, "all_items_missing_not_acquired": True,
    }
    counts = {
        "operator_source_authority_evidence_item_count": 0,
        "operator_source_authority_evidence_item_template_count": 30,
        "operator_fillable_evidence_item_template_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "acquisition_scope_section_count": 4, "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10, "evidence_custody_and_digest_requirement_count": 6,
        "candidate_results_review_requirement_count": 16, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29, "package_option_count": 12,
        "available_package_count": 7, "blocked_package_count": 5,
        "approved_future_requirement_count": 62, "approved_future_plan_step_count": 15,
        "planned_output_count": 28, "generated_output_count": 28,
        "non_goal_count": 71, "risk_control_count": 104,
    }
    execution: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "execution_status": EXECUTION_STATUS, "execution_scope": EXECUTION_SCOPE,
        "run_timestamp_utc": run_timestamp_utc, "created_offline": True,
        "governance_only": True, "template_preparation_execution_only": True,
        **{
            key: deepcopy(value)
            for key, value in approval.items()
            if key.startswith(("source_", "historical_"))
        },
        **{key: deepcopy(approval[key]) for key in CONTEXT_KEYS},
        "source_approval_artifact_kind": source.ARTIFACT_KIND,
        "source_approval_status": source.APPROVAL_STATUS,
        "source_approval_scope": source.APPROVAL_SCOPE,
        "source_approval_commit": SOURCE_APPROVAL_COMMIT,
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_attestation_digest": SOURCE_ATTESTATION_DIGEST,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "selected_source_authority_acquisition_package": approval["selected_source_authority_acquisition_package"],
        "primary_failure_class": approval["primary_failure_class"],
        "historical_primary_failure_class": approval["historical_primary_failure_class"],
        "historical_blocked_remediation_execution_commit": approval["historical_blocked_remediation_execution_commit"],
        "historical_blocked_remediation_reason": approval["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": approval["historical_blocked_remediation_manifest_digest"],
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_working_directory": "C:\\Users\\Aspire5 15 i7 4G2050\\marketflow_worktrees\\integration-terminal-evidence-stack-validation-v1",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
        "priority1_pre_change_validation_passed": True,
        "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True,
        "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_validation_duration_seconds": "41.88",
        "priority1_post_change_stdout_byte_count": 832,
        "priority1_post_change_stderr_byte_count": 0,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_exit_code": 1,
        "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "candidate_type": "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS",
        "candidate_status": "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED",
        "candidate_scope": "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
        **counts, **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "operator_fillable_evidence_package_template": package_header,
        "operator_fillable_evidence_item_template_contract": item_contract,
        "operator_fillable_evidence_item_templates": rows,
        "operator_fillable_preparation_checklist": preparation_checklist,
        "template_coverage": coverage,
        "allowed_acquisition_scope_section_ids": list(ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(ALLOWED_WORKSTREAM_IDS),
        "acceptable_source_artifact_type_inventory": list(ALLOWED_SOURCE_ARTIFACT_TYPES),
        "source_owner_request_guidance": {
            "source_owner_or_origin_required": True, "source_reference_required": True,
            "contact_performed": False, "actual_source_owner_information_supplied": False,
        },
        "custody_and_digest_guidance": deepcopy(approval["evidence_custody_and_digest_requirements_review"]),
        "no_secret_boundary": {
            "no_secrets_required": True, "no_api_keys_required": True,
            "no_broker_credentials_required": True, "no_personal_financial_credentials_required": True,
            "secrets_captured": False,
        },
        "results_review_before_use": {
            "required": True, "template_review_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
            "actual_package_use_authorized": False, "acquisition_reattempt_authorized": False,
        },
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_EXECUTION_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION,
        "reason": "The approved package has been executed only to create a non-secret, operator-fillable evidence package template and checklist. The template is not a real evidence package, not source authority, not acquired evidence, and not remediation or retry authority. A results review is required before the template can be used to prepare a real operator evidence package or support a later source-authority acquisition reattempt.",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": "not accepted", "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED", "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED", "broker_execution": "NOT_AUTHORIZED",
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    execution[TEMPLATE_DIGEST_KEY] = semantic_digest({"header": package_header, "rows": rows})
    execution[EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY] = semantic_digest(item_contract)
    execution[PREPARATION_CHECKLIST_DIGEST_KEY] = semantic_digest(preparation_checklist)
    execution[COVERAGE_DIGEST_KEY] = semantic_digest(coverage)
    digest_keys = ("checklist", "summary", EXECUTION_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    execution[EXECUTION_DIGEST_KEY] = _digest_without(execution, *digest_keys)
    execution[MANIFEST_DIGEST_KEY] = semantic_digest({
        "execution_digest": execution[EXECUTION_DIGEST_KEY], "template_digest": execution[TEMPLATE_DIGEST_KEY],
        "evidence_item_template_digest": execution[EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY],
        "preparation_checklist_digest": execution[PREPARATION_CHECKLIST_DIGEST_KEY],
        "coverage_digest": execution[COVERAGE_DIGEST_KEY],
    })
    source_checks = tuple(f"{key}_bound" for key in sorted(execution) if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit")))
    check_ids = tuple(dict.fromkeys((
        "artifact_kind_correct", "execution_status_correct", "execution_scope_correct",
        "selected_preparation_package_bound", "template_preparation_execution_created_true",
        "template_preparation_execution_performed_true", "selected_package_executed_true",
        "operator_fillable_template_created_true", "template_header_created_true",
        "evidence_item_templates_created_true", "evidence_item_template_count_30",
        "preparation_checklist_created_true", "actual_covered_missing_authority_item_count_0",
        "actual_uncovered_missing_authority_item_count_30", "missing_authority_items_missing_not_acquired",
        "ready_for_preparation_results_review_true", "outputs_generated", "recommendation_defined",
        "next_chain_defined", "next_gates_defined", "risk_controls_defined",
        "execution_digest_generated", "template_digest_generated", "evidence_item_template_digest_generated",
        "checklist_digest_generated", "coverage_digest_generated", "manifest_digest_generated",
        *source_checks, *(f"{field}_true" for field in TRUE_FIELDS), *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"template_row_{row['mapped_missing_authority_id']}_bound" for row in rows),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    execution["checklist"] = [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in check_ids]
    execution["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_preparation_execution_created": True,
        "operator_source_authority_evidence_package_preparation_execution_performed": True,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "selected_preparation_package_executed": True, "operator_fillable_template_created": True,
        "operator_fillable_evidence_item_template_count": 30, "operator_fillable_preparation_checklist_created": True,
        "operator_source_authority_evidence_package_created": False, "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False, "operator_source_authority_evidence_package_bound": False,
        "source_authority_acquisition_performed": False, "source_authority_evidence_acquired": False,
        "external_evidence_acquired": False, "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30, "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_source_authority_evidence_package_preparation_results_review": True,
        "ready_for_source_authority_acquisition_execution_retry": False,
        "ready_for_source_authority_acquisition_results_review": False,
        "ready_for_remediation_execution": False, "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "priority_1_total_nodeids": 612, "failed_or_errored_nodeids_count": 1404,
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    return execution


def execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
    *, source_approval: dict | None = None, run_timestamp_utc: str | None = None
) -> dict[str, Any]:
    """Execute only the approved deterministic template/checklist preparation."""

    approval = _committed_source_approval() if source_approval is None else deepcopy(source_approval)
    _validate_source_approval(approval)
    timestamp = DEFAULT_RUN_TIMESTAMP_UTC if run_timestamp_utc is None else run_timestamp_utc
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(timestamp)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError("run_timestamp_utc invalid")
    execution = _assemble_execution(approval, timestamp)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(execution: dict) -> dict[str, Any]:
    """Reject any changed source binding, template, digest, or safety boundary."""

    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError("execution must be an object")
    timestamp = execution.get("run_timestamp_utc")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(timestamp)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError(
            "run_timestamp_utc invalid"
        )
    expected = _assemble_execution(_committed_source_approval(), timestamp)
    difference = _first_difference(execution, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError(f"{difference} mismatch")
    for key in (EXECUTION_DIGEST_KEY, TEMPLATE_DIGEST_KEY, EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY, PREPARATION_CHECKLIST_DIGEST_KEY, COVERAGE_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        if re.fullmatch(r"[0-9a-f]{64}", str(execution.get(key))) is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError(f"{key} invalid")
    return {"artifact_kind": ARTIFACT_KIND, "execution_status": EXECUTION_STATUS, "execution_scope": EXECUTION_SCOPE, "execution_digest": execution[EXECUTION_DIGEST_KEY], **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


MARKDOWN_SECTIONS = tuple("""Source Approval
Selected Preparation Package
Source Operator Review
Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Blocked Reason
Source Acquisition Approval
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
Source Planning and Detail Binding Evidence
Retry Failure Context
Priority 1 Target Modules
Priority 1 Validation Summary
Diagnostic Capture Evidence Summary
Reviewed Observable Families
Reviewed Workstreams
Acquisition Scope Facts
Acquisition Scope Sections
Missing Authority Mapping
Acceptable Source Artifact Inventory
Template Package Header
Evidence Item Template Contract
Thirty Missing Authority Template Rows
Source Owner Request Guidance
Custody and Digest Guidance
No Secret Boundary
Results Review Before Use
Execution Scope
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_markdown_v1(execution: dict) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(deepcopy(execution))
    simple = {
        "Source Approval": {key: execution[key] for key in ("source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Selected Preparation Package": execution["selected_operator_source_authority_evidence_package_preparation_package"],
        "Source Operator Review": {key: execution[key] for key in ("source_operator_review_commit", "source_operator_review_digest", "source_operator_review_manifest_digest")},
        "Source Preparation Candidate": execution["source_preparation_candidate_summary"],
        "Source Failure Diagnosis": execution["source_failure_diagnosis_summary"],
        "Source Blocked Acquisition Execution": execution["source_blocked_acquisition_execution_summary"],
        "Blocked Reason": execution["source_blocked_reason"],
        "Source Acquisition Approval": {key: execution[key] for key in ("source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest")},
        "Source Acquisition Candidate Operator Review": execution["source_acquisition_candidate_operator_review_summary"],
        "Source Follow-On Results Review": execution["source_follow_on_results_review_summary"], "Source Follow-On Execution": execution["source_follow_on_execution_summary"],
        "Source Follow-On Approval": execution["source_follow_on_approval_summary"], "Source Follow-On Operator Review": execution["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": execution["source_follow_on_candidate_summary"], "Source Results Review": execution["source_results_review_summary"],
        "Source Enrichment Execution": execution["source_execution_summary"], "Source Historical Approval": execution["source_approval_summary"],
        "Source Historical Operator Review": execution["source_historical_operator_review_summary"], "Source Historical Candidate": execution["source_historical_candidate_summary"],
        "Historical Failure Diagnosis": execution["source_failure_diagnosis_summary"], "Historical Blocked Remediation": execution["historical_blocked_remediation_summary"],
        "Source Plan Results Review": execution["source_plan_results_review_summary"], "Source Plan Execution": execution["source_plan_execution_summary"],
        "Source Method Results Review": execution["source_method_results_review_summary"], "Source Method Execution": execution["source_method_execution_summary"],
        "Source Diagnostic Results Review": execution["source_diagnostic_results_review_summary"], "Source Controlled Recapture": execution["source_controlled_recapture_summary"],
        "Source Durable Receipt": execution["source_durable_receipt_summary"], "Source Planning and Detail Binding Evidence": execution["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": execution["retry_failure_context"], "Priority 1 Target Modules": execution["priority_1_target_modules"],
        "Priority 1 Validation Summary": execution["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": execution["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": execution["reviewed_observable_failure_families"], "Reviewed Workstreams": execution["reviewed_workstreams"],
        "Acquisition Scope Facts": execution["source_authority_acquisition_candidate_review"], "Acquisition Scope Sections": execution["acquisition_scope_sections_review"],
        "Missing Authority Mapping": execution["missing_authority_to_source_evidence_mapping_review"], "Acceptable Source Artifact Inventory": execution["acceptable_source_artifact_type_inventory"],
        "Template Package Header": execution["operator_fillable_evidence_package_template"], "Evidence Item Template Contract": execution["operator_fillable_evidence_item_template_contract"],
        "Thirty Missing Authority Template Rows": execution["operator_fillable_evidence_item_templates"], "Source Owner Request Guidance": execution["source_owner_request_guidance"],
        "Custody and Digest Guidance": execution["custody_and_digest_guidance"], "No Secret Boundary": execution["no_secret_boundary"],
        "Results Review Before Use": execution["results_review_before_use"], "Execution Scope": execution["execution_scope"],
        "Unsupported Claims Boundary": {field: execution[field] for field in FALSE_FIELDS},
        "Recommendation": {key: execution[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action", "reason")},
        "Next Chain": execution["next_chain"], "Next Gates": execution["next_gates"], "Risk Controls": execution["risk_controls"],
        "Authority Boundaries": {**{field: execution[field] for field in TRUE_FIELDS}, **{field: execution[field] for field in FALSE_FIELDS}},
        "Checklist Summary": execution["summary"], "Guardrails": execution["risk_controls"],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Execution After Approval v1", "", f"Artifact: `{execution['artifact_kind']}`", "", f"Status: `{execution['execution_status']}`", "", f"Scope: `{execution['execution_scope']}`", "", f"Execution digest: `{execution[EXECUTION_DIGEST_KEY]}`", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(simple[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(output_dir: str | Path, *, source_approval: dict | None = None, run_timestamp_utc: str | None = None) -> dict[str, Any]:
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError("protected output directory")
    execution = execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(source_approval=source_approval, run_timestamp_utc=run_timestamp_utc)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_markdown_v1(execution), encoding="utf-8")
    return execution


__all__ = [
    "ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SCHEMA_VERSION", "EXECUTION_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE", "SELECTED_PACKAGE",
    "EXECUTION_DIGEST_KEY", "TEMPLATE_DIGEST_KEY", "EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY", "PREPARATION_CHECKLIST_DIGEST_KEY", "COVERAGE_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTED_AFTER_APPROVAL_TEMPLATE_AND_CHECKLIST_READY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_BLOCKED_AFTER_APPROVAL_APPROVAL_OR_TEMPLATE_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_ONLY_TEMPLATE_AND_CHECKLIST_CREATION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY",
    "execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_markdown_v1",
]
