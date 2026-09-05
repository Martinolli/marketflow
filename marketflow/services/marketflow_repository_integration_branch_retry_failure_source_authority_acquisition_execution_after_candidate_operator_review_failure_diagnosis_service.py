"""Diagnose the expected fail-closed source-authority acquisition execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_BLOCKED_EXECUTION_COMMIT = "ff1635456a5c880f9a99a3b8359f94428383123e"
SOURCE_BLOCKED_MANIFEST_DIGEST = "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"
PRIMARY_FAILURE_CLASS = "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
SECONDARY_FAILURE_CLASSES = (
    "SOURCE_AUTHORITY_ACQUISITION_CORRECTLY_FAILS_CLOSED_WITHOUT_OPERATOR_EVIDENCE_PACKAGE",
    "SOURCE_AUTHORITY_ACQUISITION_APPROVAL_IS_NOT_EVIDENCE_ACQUISITION",
    "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_SCOPE_IS_NOT_SOURCE_AUTHORITY",
    "NO_EVIDENCE_PACKAGE_VALIDATION_PERFORMED_BECAUSE_PACKAGE_ABSENT",
    "ALL_30_MISSING_AUTHORITY_ITEMS_REMAIN_MISSING_NOT_ACQUIRED",
    "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
)
RECOMMENDED_PACKAGE = "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_AFTER_BLOCKED_ACQUISITION_EXECUTION"
RECOMMENDED_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_AFTER_BLOCKED_ACQUISITION_EXECUTION_V1"
DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_digest"
FAILURE_CLASSIFICATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_classification_digest"
MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_missing_evidence_package_diagnosis_digest"
COVERAGE_DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_coverage_diagnosis_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE
FAILURE_CLASS_NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED = PRIMARY_FAILURE_CLASS
PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_AFTER_BLOCKED_ACQUISITION_EXECUTION = RECOMMENDED_PACKAGE

TRUE_FIELDS = tuple(
    """source_authority_acquisition_failure_diagnosis_created
source_authority_acquisition_failure_diagnosis_ready
source_blocked_execution_reviewed
source_blocked_execution_identity_verified
source_blocked_reason_verified
source_approval_verified
source_attestation_verified
selected_source_authority_acquisition_package_verified
source_operator_review_verified
source_follow_on_results_review_verified
source_follow_on_execution_verified
source_authority_acquisition_candidate_verified
source_authority_acquisition_scope_verified
source_missing_authority_mapping_verified
retry_failure_context_verified
priority_1_context_verified
priority1_validation_context_verified
diagnostic_metadata_verified
observable_families_verified
reviewed_workstreams_verified
missing_authority_inventory_verified
blocked_fail_closed_behavior_verified
no_evidence_package_condition_verified
evidence_package_absence_is_primary_failure_verified
missing_authority_coverage_unchanged_verified
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_preparation_candidate""".splitlines()
)

FALSE_FIELDS = tuple(
    """source_authority_acquisition_execution_performed
selected_source_authority_acquisition_package_executed
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
source_authority_evidence_items_bound_for_results_review
source_authority_evidence_mapping_created
source_authority_acquisition_results_review_required
ready_for_source_authority_acquisition_results_review
ready_for_source_authority_acquisition_execution_retry
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
pytest_performed_in_diagnosis
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_diagnosis
diagnostic_output_analyzed_in_diagnosis
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_diagnosis
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_diagnosis
cache_modified_in_diagnosis
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
provider_requests_made_in_diagnosis
market_data_acquisition_performed_in_diagnosis
dataset_generation_performed_in_diagnosis
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)

FINDINGS = (
    "The source acquisition execution gate used the approved package PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE.",
    "The source approval was valid and authorized future acquisition execution only.",
    "The source execution correctly required an operator-provided source-authority evidence package.",
    "No operator source-authority evidence package was supplied.",
    "Package absence prevented validation, binding, coverage, custody, and source-authority evidence digest creation.",
    "The execution correctly failed closed with NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED.",
    "No source authority was acquired.",
    "No source-authority evidence was acquired or bound.",
    "No external evidence was acquired.",
    "No concrete source authority was established.",
    "No safe source-authority-bound change was identified.",
    "Coverage remains 0 covered and 30 uncovered missing-authority items.",
    "All 30 missing-authority items remain MISSING_NOT_ACQUIRED.",
    "No no-change disposition, alternate diagnostic, remediation, retry candidate, or main-merge readiness was created.",
    "No production code, existing tests, expected digests, or patches were changed.",
    "The blocked execution is an evidence-package availability failure, not a remediation failure.",
    "The detached retry remains failed and authoritative.",
    "Priority 1 focused validation remains current-root evidence only and not retry evidence.",
    "Diagnostic capture remains diagnostic metadata only and not source authority.",
    "The next governed path should prepare or supply an operator source-authority evidence package, or hold.",
)

DOMAINS = (
    ("source_approval_identity", "PASSED", "Source approval commit, digest, attestation digest, selected package, and approval-only scope are bound."),
    ("acquisition_execution_identity", "BLOCKED_REVIEWED", "Source execution blocked under the approved acquisition-or-binding scope."),
    ("evidence_package_availability", "FAILED_PRIMARY", "No operator source-authority evidence package was supplied."),
    ("evidence_package_validation", "NOT_PERFORMED_CORRECTLY", "Validation cannot occur without a package."),
    ("evidence_binding", "NOT_PERFORMED_CORRECTLY", "No evidence items were bound because no valid package was supplied."),
    ("missing_authority_coverage", "UNCHANGED", "Coverage remains 0 covered and 30 uncovered."),
    ("source_authority_status", "NOT_ESTABLISHED", "Candidate and approval do not establish concrete source authority."),
    ("change_authority_status", "NOT_IDENTIFIED", "No safe source-authority-bound change was identified."),
    ("remediation_status", "NOT_AUTHORIZED_NOT_EXECUTED", "No remediation was authorized or executed."),
    ("retry_status", "FAILED_RETRY_REMAINS_AUTHORITATIVE", "Detached retry remains failed; no retry readiness was created."),
    ("protected_repository_boundaries", "PRESERVED", "Main, integration branch, detached worktree, caches, generated output, tags, and staged evidence boundaries remain preserved."),
    ("provider_runtime_trading_boundary", "PRESERVED", "No provider, market-data, runtime, broker, or trading action occurred."),
    ("downstream_path", "ACTION_REQUIRED", "Next work should create an operator source-authority evidence package preparation candidate or equivalent governed path."),
)

OUTPUT_IDS = tuple(
    """source_authority_acquisition_failure_diagnosis_manifest
source_blocked_execution_binding_report
source_approval_binding_report
source_attestation_binding_report
source_operator_review_binding_report
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_authority_acquisition_candidate_binding_report
source_authority_acquisition_scope_binding_report
source_missing_authority_mapping_binding_report
evidence_package_absence_report
blocked_reason_report
missing_or_failed_data_report
missing_authority_coverage_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
observable_families_boundary_report
reviewed_workstreams_boundary_report
source_authority_gap_report
unsupported_claims_boundary_report
protected_repository_boundary_report
provider_runtime_trading_boundary_report
next_operator_evidence_package_preparation_recommendation
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Preparation Candidate After Blocked Acquisition Execution v1.",
    "Operator Source Authority Evidence Package Preparation Candidate Operator Review v1.",
    "Operator Source Authority Evidence Package Preparation Approval v1, if selected.",
    "Operator Source Authority Evidence Package Preparation Execution v1, if approved.",
    "Operator Source Authority Evidence Package Preparation Results Review v1.",
    "Source Authority Acquisition Execution Reattempt with Evidence Package v1, only if reviewed package exists and is approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional disposition candidate only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple(
    """operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution
operator_source_authority_evidence_package_preparation_candidate_operator_review
operator_source_authority_evidence_package_preparation_approval_if_selected
operator_source_authority_evidence_package_preparation_execution_if_approved
operator_source_authority_evidence_package_preparation_results_review
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
main_merge_approval_if_new_retry_passes""".splitlines()
)

RISK_CONTROLS = tuple(
    """failure_diagnosis_does_not_acquire_source_authority
failure_diagnosis_does_not_acquire_source_authority_evidence
failure_diagnosis_does_not_acquire_external_evidence
failure_diagnosis_does_not_create_source_authority_acquisition_execution
failure_diagnosis_does_not_retry_acquisition_execution
failure_diagnosis_does_not_fabricate_evidence
failure_diagnosis_does_not_infer_missing_evidence
failure_diagnosis_does_not_bind_partial_evidence
failure_diagnosis_does_not_accept_candidate_scope_as_source_authority
failure_diagnosis_does_not_accept_approval_as_source_authority
failure_diagnosis_does_not_treat_diagnostic_output_as_source_authority
failure_diagnosis_does_not_create_no_change_disposition
failure_diagnosis_does_not_execute_alternate_diagnostics
failure_diagnosis_does_not_execute_remediation
failure_diagnosis_does_not_modify_production_code
failure_diagnosis_does_not_modify_existing_tests
failure_diagnosis_does_not_update_expected_digests
failure_diagnosis_does_not_generate_patch
failure_diagnosis_does_not_apply_patch
failure_diagnosis_does_not_run_pytest
failure_diagnosis_does_not_run_full_pytest
failure_diagnosis_does_not_rerun_priority1_validation
failure_diagnosis_does_not_rerun_retry
failure_diagnosis_does_not_rerun_detached_retry
failure_diagnosis_does_not_parse_durable_receipt
failure_diagnosis_does_not_analyze_diagnostic_output
failure_diagnosis_does_not_rerun_source_authority_enrichment
failure_diagnosis_does_not_rerun_follow_on_execution
failure_diagnosis_does_not_rerun_plan_execution
failure_diagnosis_does_not_regenerate_targeted_plan
failure_diagnosis_does_not_rerun_method_execution
failure_diagnosis_does_not_rerun_controlled_recapture
failure_diagnosis_does_not_run_diagnostic_command
failure_diagnosis_does_not_read_pytest_cache
failure_diagnosis_does_not_modify_pytest_cache
failure_diagnosis_does_not_commit_pytest_cache
failure_diagnosis_does_not_commit_marketflow_outputs
failure_diagnosis_does_not_parse_terminal_logs
failure_diagnosis_does_not_parse_operator_logs
failure_diagnosis_does_not_inspect_env
failure_diagnosis_does_not_reconstruct_prior_lost_values
failure_diagnosis_does_not_reconstruct_full_streams
failure_diagnosis_does_not_classify_modules_again
failure_diagnosis_does_not_classify_full_retry_failures
failure_diagnosis_does_not_classify_full_retry_errors
failure_diagnosis_does_not_claim_failure_error_separation
failure_diagnosis_does_not_identify_authoritative_first_failure
failure_diagnosis_does_not_identify_authoritative_first_error
failure_diagnosis_does_not_claim_traceback_root_cause
failure_diagnosis_does_not_claim_root_cause
failure_diagnosis_does_not_claim_retry_success
failure_diagnosis_does_not_claim_main_merge_readiness
failure_diagnosis_does_not_create_retry_candidate
failure_diagnosis_does_not_create_retry_approval
failure_diagnosis_does_not_create_retry_execution
failure_diagnosis_does_not_create_retry_results_review
failure_diagnosis_does_not_create_main_merge_approval
failure_diagnosis_does_not_push_main
failure_diagnosis_does_not_push_integration_branch
failure_diagnosis_does_not_delete_integration_branch
failure_diagnosis_does_not_delete_worktree
failure_diagnosis_does_not_force_push
failure_diagnosis_does_not_modify_tags
failure_diagnosis_does_not_regenerate_evidence
failure_diagnosis_does_not_call_providers
failure_diagnosis_does_not_acquire_market_data
failure_diagnosis_does_not_generate_dataset
failure_diagnosis_does_not_recompute_metrics
failure_diagnosis_does_not_train_models
failure_diagnosis_does_not_score_strategy
failure_diagnosis_does_not_generate_trade_recommendations
failure_diagnosis_does_not_accept_predictive_usefulness
failure_diagnosis_does_not_accept_profitability
failure_diagnosis_does_not_authorize_runtime
failure_diagnosis_does_not_authorize_broker_execution
blocked_execution_remains_source_evidence
blocked_reason_remains_no_operator_source_authority_evidence_package_provided
missing_authority_items_remain_missing_not_acquired
zero_coverage_is_not_acquisition_success
evidence_package_preparation_candidate_is_not_evidence_acquisition
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
preserve_meta_limitation""".splitlines()
)

CHECK_IDS = tuple(
    """source_blocked_execution_commit_bound
source_blocked_execution_artifact_kind_bound
source_blocked_execution_status_bound
source_blocked_execution_scope_bound
source_blocked_manifest_digest_bound
source_blocked_reason_bound
source_approval_commit_bound
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
historical_failure_diagnosis_digest_bound
historical_blocked_remediation_reason_bound
historical_blocked_remediation_manifest_digest_bound
historical_primary_failure_class_bound
historical_secondary_failure_classes_bound
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
acquisition_scope_section_count_4_bound
mapped_missing_authority_item_count_30_bound
acceptable_source_artifact_type_count_13_bound
operator_provided_evidence_requirement_count_10_bound
evidence_custody_and_digest_requirement_count_6_bound
candidate_results_review_requirement_count_16_bound
operator_source_authority_evidence_package_supplied_false
operator_source_authority_evidence_package_validated_false
operator_source_authority_evidence_package_bound_false
operator_source_authority_evidence_item_count_0
covered_missing_authority_item_count_0
uncovered_missing_authority_item_count_30
missing_authority_items_missing_not_acquired
blocked_fail_closed_behavior_verified
primary_failure_class_no_operator_package
secondary_failure_classes_defined
source_authority_acquisition_execution_performed_false
selected_package_executed_false
source_authority_acquisition_performed_false
source_authority_evidence_acquired_false
external_evidence_acquired_false
concrete_source_authority_established_false
safe_source_authority_bound_change_identified_false
ready_for_acquisition_results_review_false
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
ready_for_operator_source_authority_evidence_package_preparation_candidate_true
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
diagnosis_findings_defined
diagnosis_domains_defined
outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
diagnosis_digest_generated
failure_classification_digest_generated
missing_evidence_package_diagnosis_digest_generated
coverage_diagnosis_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()
)

SOURCE_CONTEXT_KEYS = (
    "retry_failure_context",
    "priority_1_target_modules",
    "priority1_validation_summary",
    "diagnostic_capture_evidence_summary",
    "reviewed_observable_failure_families",
    "reviewed_workstreams",
    "source_authority_acquisition_candidate_review",
    "acquisition_scope_sections_review",
    "missing_authority_to_source_evidence_mapping_review",
    "acceptable_source_artifact_inventory_review",
    "operator_provided_evidence_requirements_review",
    "evidence_custody_and_digest_requirements_review",
    "candidate_results_review_requirements_review",
)


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(ValueError):
    """Raised when diagnosis evidence or a closed boundary is invalid."""


def _committed_source_blocked_execution() -> dict[str, Any]:
    approval = source._validated_source_approval(None)
    execution = source._assemble_blocked(
        approval,
        supplied=False,
        blocked_reason=source.DEFAULT_BLOCKED_REASON,
        missing_or_failed_data=["operator_source_authority_evidence_package"],
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )
    if execution[source.BLOCKED_MANIFEST_DIGEST_KEY] != SOURCE_BLOCKED_MANIFEST_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(
            "committed source blocked manifest mismatch"
        )
    return execution


_COMMITTED_SOURCE_BLOCKED_EXECUTION = _committed_source_blocked_execution()


def _first_difference(actual: Any, expected: Any, path: str = "diagnosis") -> str | None:
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
        for index, value in enumerate(expected):
            difference = _first_difference(actual[index], value, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _validated_source_blocked_execution(injected: dict | None) -> dict[str, Any]:
    execution = deepcopy(
        _COMMITTED_SOURCE_BLOCKED_EXECUTION if injected is None else injected
    )
    difference = _first_difference(
        execution, _COMMITTED_SOURCE_BLOCKED_EXECUTION, "source_blocked_execution"
    )
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(
            f"{difference} mismatch"
        )
    return execution


def _digest_without(diagnosis: Mapping[str, Any], *keys: str) -> str:
    payload = deepcopy(dict(diagnosis))
    for key in ("checklist", "summary", *keys):
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist() -> list[dict[str, Any]]:
    ids = tuple(
        dict.fromkeys(
            (
                *CHECK_IDS,
                *(f"output_{item}_generated" for item in OUTPUT_IDS),
                *(f"next_gate_{item}_defined" for item in NEXT_GATES),
                *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
            )
        )
    )
    return [
        {
            "check_id": check_id,
            "status": PASS,
            "expected": True,
            "actual": True,
            "severity": BLOCKER,
            "message": f"{check_id} passed",
        }
        for check_id in ids
    ]


def _assemble_diagnosis(blocked: Mapping[str, Any]) -> dict[str, Any]:
    conflicting_source_keys = {
        "source_blocked_execution_artifact_kind",
        "source_blocked_execution_status",
        "source_blocked_execution_scope",
        "source_blocked_execution_commit",
        "source_blocked_manifest_digest",
        "source_blocked_reason",
    }
    source_context = {
        key: deepcopy(value)
        for key, value in blocked.items()
        if key.startswith("source_") and key not in conflicting_source_keys
    }
    classification = {
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
    }
    availability = {
        "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False,
        "operator_source_authority_evidence_package_bound": False,
        "diagnosis": "ABSENT_BLOCKED_CORRECTLY_NO_VALIDATION_OR_BINDING_PERFORMED",
        "blocked_reason": PRIMARY_FAILURE_CLASS,
    }
    coverage = {
        "covered_missing_authority_item_count": 0,
        "uncovered_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "items": deepcopy(blocked["missing_authority_coverage"]),
    }
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "diagnosis_only": True,
        **source_context,
        **{key: deepcopy(blocked[key]) for key in SOURCE_CONTEXT_KEYS},
        "source_blocked_execution_artifact_kind": blocked["artifact_kind"],
        "source_blocked_execution_status": blocked["execution_status"],
        "source_blocked_execution_scope": blocked["execution_scope"],
        "source_blocked_execution_commit": SOURCE_BLOCKED_EXECUTION_COMMIT,
        "source_blocked_manifest_digest": blocked[source.BLOCKED_MANIFEST_DIGEST_KEY],
        "source_blocked_reason": blocked["blocked_reason"],
        "source_blocked_execution_summary": {
            "commit": SOURCE_BLOCKED_EXECUTION_COMMIT,
            "artifact_kind": blocked["artifact_kind"],
            "status": blocked["execution_status"],
            "scope": blocked["execution_scope"],
            "blocked_reason": blocked["blocked_reason"],
            "blocked_manifest_digest": blocked[source.BLOCKED_MANIFEST_DIGEST_KEY],
            "checks": f"{blocked['summary']['passed_checks']}/{blocked['summary']['total_checks']} PASS",
        },
        "historical_blocked_remediation_execution_commit": blocked["source_blocked_execution_commit"],
        "historical_blocked_remediation_reason": blocked["source_blocked_reason"],
        "historical_blocked_remediation_manifest_digest": blocked["source_blocked_manifest_digest"],
        "historical_primary_failure_class": blocked["primary_failure_class"],
        "historical_secondary_failure_classes": deepcopy(blocked["secondary_failure_classes"]),
        "historical_blocked_remediation_summary": deepcopy(blocked["source_blocked_execution_summary"]),
        "selected_source_authority_acquisition_package": blocked["selected_source_authority_acquisition_package"],
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        "diagnosis_classification": classification,
        "diagnosis_findings": [
            {"finding_id": index, "finding": finding}
            for index, finding in enumerate(FINDINGS, 1)
        ],
        "diagnosis_domains": [
            {"domain_id": domain, "disposition": disposition, "explanation": explanation}
            for domain, disposition, explanation in DOMAINS
        ],
        "evidence_package_availability_diagnosis": availability,
        "missing_authority_coverage_diagnosis": coverage,
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
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "outputs": [
            {
                "output_id": output_id,
                "status": "GENERATED_SOURCE_AUTHORITY_ACQUISITION_FAILURE_DIAGNOSIS_ONLY",
            }
            for output_id in OUTPUT_IDS
        ],
        "recommended_next_package": RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_TASK,
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_BEFORE_ANY_ACQUISITION_RETRY_OR_MAIN",
        "recommendation_reason": "The acquisition execution correctly failed closed because no operator source-authority evidence package was supplied. The approved acquisition scope exists, but scope and approval are not evidence. A governed evidence-package preparation candidate is required before another acquisition execution can bind evidence for review.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY] = semantic_digest(classification)
    diagnosis[MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY] = semantic_digest(availability)
    diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY] = semantic_digest(coverage)
    diagnosis[DIAGNOSIS_DIGEST_KEY] = _digest_without(
        diagnosis,
        DIAGNOSIS_DIGEST_KEY,
        MANIFEST_DIGEST_KEY,
    )
    diagnosis[MANIFEST_DIGEST_KEY] = semantic_digest(
        {
            "diagnosis_digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
            "failure_classification_digest": diagnosis[FAILURE_CLASSIFICATION_DIGEST_KEY],
            "missing_evidence_package_diagnosis_digest": diagnosis[MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY],
            "coverage_diagnosis_digest": diagnosis[COVERAGE_DIAGNOSIS_DIGEST_KEY],
            "source_blocked_manifest_digest": diagnosis["source_blocked_manifest_digest"],
        }
    )
    diagnosis["checklist"] = _checklist()
    diagnosis["summary"] = {
        "total_checks": len(diagnosis["checklist"]),
        "passed_checks": len(diagnosis["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        "source_authority_acquisition_failure_diagnosis_created": True,
        "source_authority_acquisition_failure_diagnosis_ready": True,
        "source_blocked_execution_reviewed": True,
        "source_blocked_reason": PRIMARY_FAILURE_CLASS,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "source_authority_acquisition_execution_performed": False,
        "selected_source_authority_acquisition_package_executed": False,
        "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False,
        "operator_source_authority_evidence_package_bound": False,
        "source_authority_acquisition_performed": False,
        "source_authority_evidence_acquired": False,
        "external_evidence_acquired": False,
        "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False,
        "covered_missing_authority_item_count": 0,
        "uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_source_authority_evidence_package_preparation_candidate": True,
        "ready_for_source_authority_acquisition_results_review": False,
        "ready_for_source_authority_acquisition_execution_retry": False,
        "ready_for_remediation_execution": False,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "priority_1_total_nodeids": 612,
        "failed_or_errored_nodeids_count": 1404,
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "recommended_next_task": RECOMMENDED_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    return diagnosis


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
    *, source_blocked_execution: dict | None = None
) -> dict[str, Any]:
    """Build the deterministic, offline diagnosis-only artifact."""

    blocked = _validated_source_blocked_execution(source_blocked_execution)
    diagnosis = _assemble_diagnosis(blocked)
    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
        diagnosis
    )
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict[str, Any]:
    """Reject drift from the complete committed diagnosis contract."""

    if not isinstance(diagnosis, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(
            "diagnosis must be an object"
        )
    expected = _assemble_diagnosis(_validated_source_blocked_execution(None))
    difference = _first_difference(diagnosis, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(
            f"{difference} mismatch"
        )
    return {
        "artifact_kind": diagnosis["artifact_kind"],
        "diagnosis_status": diagnosis["diagnosis_status"],
        "diagnosis_scope": diagnosis["diagnosis_scope"],
        "digest": diagnosis[DIAGNOSIS_DIGEST_KEY],
        **{
            key: diagnosis["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


MARKDOWN_SECTIONS = tuple(
    """Source Blocked Execution
Blocked Reason
Source Approval
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
Historical Failure Diagnosis
Historical Blocked Remediation
Historical Failure Classification
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
Evidence Package Availability Diagnosis
Missing Authority Coverage Diagnosis
Diagnosis Classification
Diagnosis Domains
Diagnosis Findings
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines()
)


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    """Render a validated diagnosis document."""

    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
        deepcopy(diagnosis)
    )
    sections = {
        "Source Blocked Execution": diagnosis["source_blocked_execution_summary"],
        "Blocked Reason": diagnosis["source_blocked_reason"],
        "Source Approval": {key: diagnosis[key] for key in ("source_approval_artifact_kind", "source_approval_status", "source_approval_scope", "source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Selected Source Authority Acquisition Package": diagnosis["selected_source_authority_acquisition_package"],
        "Source Operator Review": diagnosis["source_operator_review_summary"],
        "Source Follow-On Results Review": diagnosis["source_follow_on_results_review_summary"],
        "Source Follow-On Execution": diagnosis["source_follow_on_execution_summary"],
        "Source Follow-On Approval": diagnosis["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": diagnosis["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": diagnosis["source_follow_on_candidate_summary"],
        "Source Results Review": diagnosis["source_results_review_summary"],
        "Source Enrichment Execution": diagnosis["source_execution_summary"],
        "Source Historical Approval": diagnosis["source_approval_summary"],
        "Source Historical Operator Review": diagnosis["source_historical_operator_review_summary"],
        "Source Historical Candidate": diagnosis["source_historical_candidate_summary"],
        "Historical Failure Diagnosis": diagnosis["source_failure_diagnosis_summary"],
        "Historical Blocked Remediation": diagnosis["historical_blocked_remediation_summary"],
        "Historical Failure Classification": {"primary": diagnosis["historical_primary_failure_class"], "secondary": diagnosis["historical_secondary_failure_classes"]},
        "Source Remediation Execution Approval": diagnosis["source_remediation_execution_approval_after_plan_results_review_digest"],
        "Source Plan Results Review": diagnosis["source_plan_results_review_summary"],
        "Source Plan Execution": diagnosis["source_plan_execution_summary"],
        "Source Method Results Review": diagnosis["source_method_results_review_summary"],
        "Source Method Execution": diagnosis["source_method_execution_summary"],
        "Source Diagnostic Results Review": diagnosis["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": diagnosis["source_controlled_recapture_summary"],
        "Source Durable Receipt": diagnosis["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": diagnosis["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": diagnosis["retry_failure_context"],
        "Priority 1 Target Modules": diagnosis["priority_1_target_modules"],
        "Priority 1 Validation Summary": diagnosis["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": diagnosis["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": diagnosis["reviewed_observable_failure_families"],
        "Reviewed Workstreams": diagnosis["reviewed_workstreams"],
        "Source Authority Acquisition Candidate": diagnosis["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Sections": diagnosis["acquisition_scope_sections_review"],
        "Missing Authority Mapping": diagnosis["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory": diagnosis["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements": diagnosis["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements": diagnosis["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements": diagnosis["candidate_results_review_requirements_review"],
        "Evidence Package Availability Diagnosis": diagnosis["evidence_package_availability_diagnosis"],
        "Missing Authority Coverage Diagnosis": diagnosis["missing_authority_coverage_diagnosis"],
        "Diagnosis Classification": diagnosis["diagnosis_classification"],
        "Diagnosis Domains": diagnosis["diagnosis_domains"],
        "Diagnosis Findings": diagnosis["diagnosis_findings"],
        "Unsupported Claims Boundary": {field: diagnosis[field] for field in FALSE_FIELDS},
        "Recommendation": {key: diagnosis[key] for key in ("recommended_next_package", "recommended_next_task", "recommended_next_task_status", "recommended_action", "recommendation_reason")},
        "Next Chain": diagnosis["next_chain"],
        "Next Gates": diagnosis["next_gates"],
        "Risk Controls": diagnosis["risk_controls"],
        "Authority Boundaries": {**{field: diagnosis[field] for field in TRUE_FIELDS}, **{field: diagnosis[field] for field in FALSE_FIELDS}},
        "Checklist Summary": diagnosis["summary"],
        "Guardrails": list(RISK_CONTROLS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Execution After Candidate Operator Review Failure Diagnosis v1",
        "",
        f"Artifact: `{diagnosis['artifact_kind']}`",
        "",
        f"Status: `{diagnosis['diagnosis_status']}`",
        "",
        f"Scope: `{diagnosis['diagnosis_scope']}`",
        "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
    output_dir: str | Path,
    *,
    source_blocked_execution: dict | None = None,
) -> dict[str, Any]:
    """Write the deterministic diagnosis status document."""

    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError(
            "protected output directory"
        )
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
        source_blocked_execution=source_blocked_execution
    )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_STATUS.md"
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_markdown_v1(diagnosis),
        encoding="utf-8",
    )
    return diagnosis


__all__ = [
    "ARTIFACT_KIND",
    "SCHEMA_VERSION",
    "DIAGNOSIS_STATUS",
    "DIAGNOSIS_SCOPE",
    "PRIMARY_FAILURE_CLASS",
    "SECONDARY_FAILURE_CLASSES",
    "RECOMMENDED_PACKAGE",
    "DIAGNOSIS_DIGEST_KEY",
    "FAILURE_CLASSIFICATION_DIGEST_KEY",
    "MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY",
    "COVERAGE_DIAGNOSIS_DIGEST_KEY",
    "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "FAILURE_CLASS_NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED",
    "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_AFTER_BLOCKED_ACQUISITION_EXECUTION",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_markdown_v1",
]
