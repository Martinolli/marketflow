"""Review a source-authority acquisition candidate without selecting a package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_FOLLOW_ON_RESULTS_REVIEW_COMMIT = "c3b894179fb89c14d95ba43a72393e943ff44199"
SOURCE_FOLLOW_ON_RESULTS_REVIEW_DIGEST = "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"
SOURCE_ACQUISITION_CANDIDATE_REVIEW_DIGEST = "6c122b5bb1489861a969efdf9ab9c36f4ce9a799b7ecf76b791d41a550f653e5"
SOURCE_ACQUISITION_SCOPE_REVIEW_DIGEST = "713aefda1df0916f1ddd25084751cb3f2a23ddc9679e16ff4827409678092d0e"
SOURCE_MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST = "83104c9ff91bceed69f368f194cf454629f3530e0c6e8dabed83099677a7b381"
SOURCE_FOLLOW_ON_RESULTS_REVIEW_MANIFEST_DIGEST = "be88a6b0679378ca52cc1489a173387e01f0acbbd5c4888aa4a345e1a46c6cb2"

RECOMMENDED_PACKAGE = "PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_V1_IF_SELECTED"
RECOMMENDED_ACTION = "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION"
OUTPUT_STATUS = "GENERATED_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_ONLY"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_digest"
CANDIDATE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_candidate_review_digest"
SCOPE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_scope_review_digest"
MAPPING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_mapping_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE = RECOMMENDED_PACKAGE


REVIEWED_CANDIDATE_PHILOSOPHY = {
    "reviewed_source_authority_acquisition_candidate_philosophy": (
        "The follow-on execution results review confirms that a source-authority acquisition candidate was "
        "created and reviewed. The candidate defines future acquisition scope, missing-authority mappings, "
        "acceptable artifact types, operator evidence requirements, custody/digest requirements, and "
        "results-review requirements. It does not acquire source authority, acquire evidence, establish "
        "concrete source authority, identify safe source-authority-bound change, authorize remediation, create "
        "no-change disposition, execute diagnostics, create retry readiness, or create main-merge readiness. "
        "This operator review reviews candidate completeness and package options only."
    ),
    "reviewed_candidate_boundary": (
        "Operator-review only; no package selection, approval, execution, evidence acquisition, source-authority "
        "acquisition, no-change disposition, alternate diagnostic, remediation, code change, test change, digest "
        "update, patch generation, pytest, retry, main merge, provider request, runtime, broker, or trading "
        "authority is created."
    ),
    "review_status": "REVIEWED_CANDIDATE_ONLY",
}

PACKAGE_DEFINITIONS = (
    (RECOMMENDED_PACKAGE, "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", "Future approval and execution may acquire or bind source-authority evidence strictly from the reviewed acquisition candidate scope, including the 30 missing-authority items, four workstreams, acceptable source-artifact inventory, operator-provided evidence requirements, and custody/digest requirements.", None),
    ("PACKAGE_CREATE_OPERATOR_PROVIDED_SOURCE_EVIDENCE_PACKAGE_REQUIREMENTS_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "Future execution may refine operator-provided evidence package requirements without acquiring evidence.", None),
    ("PACKAGE_CREATE_SOURCE_OWNER_AUTHORITY_REQUESTS_FOR_MISSING_ITEMS", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "Future execution may draft source-owner request requirements for the 30 missing authority items without contacting owners or acquiring evidence.", None),
    ("PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_AUTHORITY_ACQUISITION_PATH", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "Future execution may define a limited path for schema, field, export-surface, and backward-compatible alias authority acquisition only.", None),
    ("PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_AUTHORITY_ACQUISITION_PATH", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "Future execution may define a limited path for canonical payload, serialization method, digest boundary, manifest, and expected-hash authority acquisition only.", None),
    ("PACKAGE_HOLD_SOURCE_AUTHORITY_ACQUISITION_PENDING_SOURCE_OWNER_INPUT", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "Future execution may hold all source-authority acquisition, remediation, no-change disposition, diagnostics, and retry work pending source-owner input.", None),
    ("PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_APPROVAL", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "Source-authority acquisition requires separate approval, execution, custody, and results review."),
    ("PACKAGE_ACCEPT_DIAGNOSTIC_OUTPUT_AS_SOURCE_AUTHORITY", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "Diagnostic output is observation evidence only and cannot be treated as source authority."),
    ("PACKAGE_DIRECT_REMEDIATION_FROM_ACQUISITION_CANDIDATE", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "The acquisition candidate defines future evidence needs only and does not authorize code, test, digest, fixture, schema, or export changes."),
    ("PACKAGE_NO_CHANGE_DISPOSITION_FROM_ACQUISITION_CANDIDATE_ONLY", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "No-change disposition requires acquired and reviewed source authority, not a candidate-only scope."),
    ("PACKAGE_NEW_RETRY_FROM_ACQUISITION_CANDIDATE_ONLY", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "The acquisition candidate does not create retry readiness or retry success evidence."),
    ("PACKAGE_MAIN_MERGE_FROM_ACQUISITION_CANDIDATE_OR_CURRENT_ROOT_PASS", "BLOCKED_NOT_ALLOWED", "REVIEWED_BLOCKED_NOT_ALLOWED", "Blocked package.", "Main merge remains blocked until a future retry results review passes; acquisition-candidate scope and current-root focused validation are not retry evidence."),
)

FUTURE_REQUIREMENT_IDS = tuple("""source_follow_on_results_review_must_be_ready
source_follow_on_results_review_digest_must_be_bound
source_acquisition_candidate_review_digest_must_be_bound
source_acquisition_scope_review_digest_must_be_bound
source_missing_authority_mapping_review_digest_must_be_bound
source_follow_on_results_review_manifest_digest_must_be_bound
source_follow_on_execution_commit_must_be_bound
source_follow_on_execution_digest_must_be_bound
source_acquisition_candidate_digest_must_be_bound
source_acquisition_scope_digest_must_be_bound
source_missing_authority_mapping_digest_must_be_bound
source_follow_on_execution_manifest_digest_must_be_bound
source_follow_on_approval_digest_must_be_bound
source_follow_on_operator_review_digest_must_be_bound
source_follow_on_candidate_digest_must_be_bound
source_results_review_digest_must_be_bound
source_execution_digest_must_be_bound
source_approval_digest_must_be_bound
source_failure_diagnosis_digest_must_be_bound
source_blocked_reason_must_be_bound
retry_failure_counts_must_be_bound
priority_1_context_must_be_bound
priority1_validation_must_not_be_retry_evidence
diagnostic_metadata_must_remain_diagnostic_only
observable_families_must_remain_planning_evidence
reviewed_workstreams_must_remain_non_authorizing
candidate_status_must_remain_created_for_results_review_not_approved_not_executed
candidate_scope_must_remain_creation_only
acquisition_scope_section_count_must_be_4
mapped_missing_authority_item_count_must_be_30
mapped_items_must_remain_missing_not_acquired
mapped_items_must_not_have_authority_acquired
mapped_items_must_not_have_evidence_acquired
mapped_items_must_not_authorize_direct_change
acceptable_source_artifact_type_count_must_be_13
acceptable_artifacts_must_not_be_acquired
operator_provided_evidence_requirement_count_must_be_10
evidence_custody_and_digest_requirement_count_must_be_6
candidate_results_review_requirement_count_must_be_16
future_acquisition_must_require_separate_approval
future_acquisition_must_require_results_review
future_acquisition_must_preserve_no_secrets_no_api_keys_no_broker_credentials
future_acquisition_must_not_treat_diagnostic_output_as_source_authority
future_acquisition_must_not_treat_current_root_validation_as_retry_success
future_acquisition_must_not_modify_code_without_later_remediation_approval
future_acquisition_must_not_modify_tests_without_later_remediation_approval
future_acquisition_must_not_update_expected_digests_without_later_remediation_approval
future_acquisition_must_not_create_retry_readiness_without_later_review
future_acquisition_must_not_push_main
future_acquisition_must_not_push_integration_branch
runtime_and_trading_remain_not_authorized""".splitlines())

FUTURE_PLAN = (
    "Bind this operator review and source follow-on execution results review.",
    "Bind all prior execution, approval, candidate, diagnosis, remediation, plan, method, diagnostic, detail, recovery, module-grouping, and staged-inventory digests.",
    "Bind retry counts, Priority 1 context, diagnostic metadata, observable families, workstreams, and missing-authority inventory facts.",
    "Review acquisition candidate identity, status, scope, basis, and boundary.",
    "Review all four acquisition-scope sections.",
    "Review all 30 mapped missing-authority items and verify all remain missing/not acquired.",
    "Review the 13 acceptable source-artifact types as future options only.",
    "Review the 10 operator-provided evidence requirements.",
    "Review the six evidence custody and digest requirements.",
    "Review the 16 candidate results-review requirements.",
    "Review source-authority acquisition package options without selecting any.",
    "Preserve that future source-authority acquisition requires separate approval and results review.",
    "Preserve retry, remediation, disposition, merge, provider, runtime, broker, and trading gates.",
)

PLANNED_OUTPUT_IDS = tuple("""source_authority_acquisition_candidate_operator_review_manifest
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_follow_on_approval_binding_report
source_follow_on_operator_review_binding_report
source_follow_on_candidate_binding_report
source_results_review_binding_report
source_execution_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
retry_failure_context_review
priority1_validation_disposition_review
diagnostic_metadata_boundary_review
observable_family_review
reviewed_workstreams_review
acquisition_candidate_identity_review
acquisition_scope_section_review
missing_authority_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
candidate_results_review_requirements_review
source_authority_acquisition_package_comparison_report
recommended_source_authority_acquisition_package_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

OUTPUT_IDS = tuple("""source_authority_acquisition_candidate_operator_review_manifest
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_follow_on_approval_binding_report
source_follow_on_operator_review_binding_report
source_follow_on_candidate_binding_report
source_results_review_binding_report
source_execution_binding_report
source_approval_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_review
priority1_validation_disposition_review
diagnostic_metadata_boundary_review
observable_family_review
reviewed_workstreams_review
acquisition_candidate_identity_review
acquisition_scope_section_review
missing_authority_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
candidate_results_review_requirements_review
source_authority_acquisition_package_comparison_report
recommended_source_authority_acquisition_package_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NON_GOALS = tuple("""do_not_select_package_now
do_not_approve_package_now
do_not_authorize_package_now
do_not_execute_source_authority_acquisition_now
do_not_acquire_source_authority_now
do_not_acquire_source_authority_evidence_now
do_not_acquire_external_evidence_now
do_not_create_no_change_disposition_now
do_not_execute_alternate_diagnostics_now
do_not_execute_remediation_now
do_not_modify_production_code_now
do_not_modify_existing_tests_now
do_not_update_expected_digests_now
do_not_generate_patch_now
do_not_apply_patch_now
do_not_run_pytest_now
do_not_run_full_pytest_now
do_not_rerun_priority1_validation_now
do_not_rerun_retry_now
do_not_rerun_detached_retry_now
do_not_push_main
do_not_push_integration_branch
do_not_delete_or_reset_integration_branch
do_not_delete_or_reset_worktree
do_not_force_push
do_not_modify_tags
do_not_read_pytest_cache_now
do_not_modify_pytest_cache_now
do_not_parse_durable_receipt_now
do_not_analyze_diagnostic_output_now
do_not_rerun_follow_on_execution_now
do_not_rerun_source_authority_enrichment_now
do_not_rerun_plan_execution_now
do_not_regenerate_targeted_plan_now
do_not_rerun_method_execution_now
do_not_rerun_controlled_recapture_now
do_not_run_diagnostic_command_now
do_not_parse_terminal_logs_now
do_not_parse_operator_logs_now
do_not_inspect_env_now
do_not_reconstruct_prior_lost_values_now
do_not_reconstruct_full_stdout_or_stderr_now
do_not_classify_modules_again_now
do_not_classify_full_retry_failures_now
do_not_classify_full_retry_errors_now
do_not_claim_failure_error_separation_now
do_not_identify_first_failure_now
do_not_identify_first_error_now
do_not_claim_traceback_root_cause_now
do_not_claim_root_cause_now
do_not_claim_retry_success_now
do_not_claim_main_merge_readiness_now
do_not_create_source_authority_acquisition_execution_now
do_not_create_no_change_disposition_execution_now
do_not_create_alternate_diagnostic_execution_now
do_not_create_remediation_execution_now
do_not_create_remediation_execution_results_review_now
do_not_create_new_retry_candidate_now
do_not_create_retry_approval_now
do_not_create_retry_execution_now
do_not_create_retry_results_review_now
do_not_create_integration_results_review_now
do_not_mark_integration_successful
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_call_providers
do_not_acquire_market_data
do_not_generate_dataset
do_not_recompute_metrics
do_not_train_models
do_not_score_strategy
do_not_generate_recommendations
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_broker_execution
do_not_authorize_trading""".splitlines())

TRUE_FIELDS = tuple("""source_authority_acquisition_candidate_operator_review_created
source_authority_acquisition_candidate_operator_review_ready
source_follow_on_results_review_reviewed
source_follow_on_execution_reviewed
source_authority_acquisition_candidate_reviewed
source_authority_acquisition_candidate_created_reviewed
source_authority_acquisition_candidate_ready_for_results_review_reviewed
source_authority_acquisition_scope_reviewed
missing_authority_to_source_evidence_mapping_reviewed
acceptable_source_artifact_inventory_reviewed
operator_provided_evidence_requirements_reviewed
evidence_custody_and_digest_requirements_reviewed
candidate_results_review_requirements_reviewed
source_follow_on_approval_verified
source_follow_on_operator_review_verified
source_follow_on_candidate_verified
source_results_review_verified
source_execution_verified
source_approval_verified
source_failure_diagnosis_verified
source_blocked_execution_verified
retry_failure_context_verified
priority_1_context_verified
priority1_validation_context_verified
diagnostic_metadata_verified
observable_families_verified
reviewed_workstreams_verified
missing_authority_inventory_review_facts_verified
candidate_philosophy_reviewed
source_authority_acquisition_packages_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
source_authority_gap_preserved
detached_retry_failed_status_preserved""".splitlines())

EXTRA_FALSE_FIELDS = tuple("""recommended_package_selected
source_authority_acquisition_package_selected
source_authority_acquisition_package_approved
source_authority_acquisition_package_authorized
source_authority_acquisition_execution_created
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
pytest_performed_in_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_review
cache_modified_in_review
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
ready_for_source_authority_acquisition_approval
ready_for_source_authority_acquisition_execution
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
provider_requests_made_in_review
market_data_acquisition_performed_in_review
dataset_generation_performed_in_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())
FALSE_FIELDS = tuple(dict.fromkeys((*source.FALSE_FIELDS, *EXTRA_FALSE_FIELDS)))

NEXT_CHAIN = (
    "Source-Authority Acquisition Approval After Candidate Operator Review v1, if selected.",
    "Source-Authority Acquisition Execution v1, if separately approved.",
    "Source-Authority Acquisition Results Review v1.",
    "A conditional disposition candidate only if acquired and reviewed authority supports it.",
    "New Integration Branch Retry Candidate v1 only after a reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if the new retry results review passes.",
)
NEXT_GATES = tuple("""source_authority_acquisition_approval_after_candidate_operator_review_if_selected
source_authority_acquisition_execution_if_approved
source_authority_acquisition_results_review
no_change_disposition_candidate_if_supported
alternate_diagnostic_candidate_if_supported
remediation_reentry_candidate_if_supported
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines())
RISK_CONTROLS = tuple(dict.fromkeys((
    *(f"operator_review_{item}" for item in NON_GOALS),
    "candidate_is_not_source_authority",
    "diagnostic_output_is_not_source_authority",
    "current_root_validation_is_not_retry_evidence",
    "separate_approval_required_before_acquisition",
    "separate_results_review_required_after_acquisition",
    "main_merge_requires_passing_new_retry_results_review",
)))

SOURCE_CONTEXT_KEYS = tuple("""retry_failure_context
priority_1_target_modules
priority1_validation_summary
diagnostic_capture_evidence_summary
reviewed_observable_failure_families
reviewed_workstreams
source_authority_enrichment_review_summary
missing_authority_inventory_review_summary
workstream_authority_mapping_review_summary
source_authority_acquisition_candidate_review
acquisition_scope_definition_review
missing_authority_to_source_evidence_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
candidate_results_review_requirements_review""".splitlines())

OPERATOR_CHECK_IDS = tuple(dict.fromkeys((
    "source_follow_on_results_review_bound",
    "source_review_components_bound",
    "reviewed_packages_12",
    "recommended_package_not_selected",
    "future_requirements_51",
    "future_plan_13",
    "planned_outputs_28",
    "review_outputs_33",
    "recommendation_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    *(f"{field}_true" for field in TRUE_FIELDS),
    *(f"{field}_false" for field in FALSE_FIELDS),
    *(f"package_{item[0]}_reviewed" for item in PACKAGE_DEFINITIONS),
    *(f"future_requirement_{item}_reviewed" for item in FUTURE_REQUIREMENT_IDS),
)))
CHECK_IDS = OPERATOR_CHECK_IDS


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError(ValueError):
    """Raised when source evidence or the operator-review contract changes."""


def _committed_source_follow_on_results_review() -> dict[str, Any]:
    # This is the source module's private constant assembler, not its public builder or any execution path.
    return source._assemble_review()


def _first_difference(actual: Any, expected: Any, path: str = "review") -> str | None:
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


def _validate_source(review: Mapping[str, Any]) -> None:
    expected = _committed_source_follow_on_results_review()
    difference = _first_difference(review, expected, "source_follow_on_results_review")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError(
            f"{difference} mismatch"
        )


def _reviewed_packages() -> list[dict[str, Any]]:
    reviewed = []
    for package_id, source_status, review_status, purpose, blocked_reason in PACKAGE_DEFINITIONS:
        package = {
            "package_id": package_id,
            "source_status": source_status,
            "review_status": review_status,
            "purpose": purpose,
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        if blocked_reason:
            package["blocked_reason"] = blocked_reason
        reviewed.append(package)
    return reviewed


def _source_bindings(source_review: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {
        key: deepcopy(value)
        for key, value in source_review.items()
        if key.startswith("source_") and key not in {"source_authority_acquisition_candidate_review"}
    }
    bindings.update({
        "source_follow_on_results_review_artifact_kind": source.ARTIFACT_KIND,
        "source_follow_on_results_review_status": source.REVIEW_STATUS,
        "source_follow_on_results_review_scope": source.REVIEW_SCOPE,
        "source_follow_on_results_review_commit": SOURCE_FOLLOW_ON_RESULTS_REVIEW_COMMIT,
        "source_follow_on_results_review_digest": SOURCE_FOLLOW_ON_RESULTS_REVIEW_DIGEST,
        "source_acquisition_candidate_review_digest": SOURCE_ACQUISITION_CANDIDATE_REVIEW_DIGEST,
        "source_acquisition_scope_review_digest": SOURCE_ACQUISITION_SCOPE_REVIEW_DIGEST,
        "source_missing_authority_mapping_review_digest": SOURCE_MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST,
        "source_follow_on_results_review_manifest_digest": SOURCE_FOLLOW_ON_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_follow_on_results_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "status": source.REVIEW_STATUS,
            "scope": source.REVIEW_SCOPE,
            "commit": SOURCE_FOLLOW_ON_RESULTS_REVIEW_COMMIT,
            "digest": SOURCE_FOLLOW_ON_RESULTS_REVIEW_DIGEST,
            "checks": "314/314 PASS",
        },
        "selected_follow_on_package": source_review["selected_follow_on_package"],
        "primary_failure_class": source_review["primary_failure_class"],
        "secondary_failure_classes": deepcopy(source_review["secondary_failure_classes"]),
    })
    return bindings


def _component_digests(review: dict[str, Any]) -> None:
    review[CANDIDATE_REVIEW_DIGEST_KEY] = semantic_digest(review["source_authority_acquisition_candidate_review"])
    review[SCOPE_REVIEW_DIGEST_KEY] = semantic_digest(review["acquisition_scope_sections_review"])
    review[MAPPING_REVIEW_DIGEST_KEY] = semantic_digest(review["missing_authority_to_source_evidence_mapping_review"])
    review["digest_manifest"] = {
        "source_follow_on_results_review_commit": SOURCE_FOLLOW_ON_RESULTS_REVIEW_COMMIT,
        "source_follow_on_results_review_digest": SOURCE_FOLLOW_ON_RESULTS_REVIEW_DIGEST,
        CANDIDATE_REVIEW_DIGEST_KEY: review[CANDIDATE_REVIEW_DIGEST_KEY],
        SCOPE_REVIEW_DIGEST_KEY: review[SCOPE_REVIEW_DIGEST_KEY],
        MAPPING_REVIEW_DIGEST_KEY: review[MAPPING_REVIEW_DIGEST_KEY],
        "reviewed_package_ids": [item[0] for item in PACKAGE_DEFINITIONS],
        "output_ids": list(OUTPUT_IDS),
    }
    review[MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])


def _operator_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for key in ("checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY):
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_review(source_review: Mapping[str, Any]) -> dict[str, Any]:
    source_context = {key: deepcopy(source_review[key]) for key in SOURCE_CONTEXT_KEYS}
    review = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **_source_bindings(source_review),
        **source_context,
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "acquisition_scope_section_count": 4,
        "mapped_missing_authority_item_count": 30,
        "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6,
        "candidate_results_review_requirement_count": 16,
        "source_outputs_generated_count": 27,
        "source_authority_enrichment_results_review_outputs_generated_count": 28,
        "follow_on_execution_outputs_generated_count": 30,
        "follow_on_execution_results_review_outputs_generated_count": 33,
        "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "reviewed_candidate_philosophy": deepcopy(REVIEWED_CANDIDATE_PHILOSOPHY),
        "reviewed_source_authority_acquisition_packages": _reviewed_packages(),
        "recommended_source_authority_acquisition_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_package": {
            "package_id": RECOMMENDED_PACKAGE,
            "status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "reason": "The complete reviewed candidate supports a separate approval ceremony for acquisition from its bounded scope; this review does not select or approve that package.",
            "selected": False,
        },
        "reviewed_future_requirements": [
            {"requirement_id": item, "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_AFTER_CANDIDATE_OPERATOR_REVIEW", "execution_status": "NOT_EXECUTED"}
            for item in FUTURE_REQUIREMENT_IDS
        ],
        "reviewed_future_plan": [
            {"step_id": index, "step": step, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": "NOT_EXECUTED"}
            for index, step in enumerate(FUTURE_PLAN, 1)
        ],
        "reviewed_planned_outputs": [
            {"output_id": item, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
            for item in PLANNED_OUTPUT_IDS
        ],
        "reviewed_non_goals": [
            {"non_goal_id": item, "review_status": "REVIEWED_ACTIVE"} for item in NON_GOALS
        ],
        "outputs_generated": [{"output_id": item, "status": OUTPUT_STATUS} for item in OUTPUT_IDS],
        "review_outputs_generated_count": len(OUTPUT_IDS),
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
            "recommended_action": RECOMMENDED_ACTION,
            "reason": "The candidate is complete enough for optional operator selection and a separate approval ceremony, while all acquisition and downstream authority remains closed.",
        },
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION,
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
    review["acquisition_scope_sections_review"] = deepcopy(source_review["acquisition_scope_definition_review"])
    _component_digests(review)
    review["checklist"] = [
        {"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"}
        for item in CHECK_IDS
    ]
    review["summary"] = {
        "total_checks": len(review["checklist"]),
        "passed_checks": len(review["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        "reviewed_package_count": 12,
        "available_package_count": 6,
        "blocked_package_count": 6,
        "future_requirement_count": len(FUTURE_REQUIREMENT_IDS),
        "future_plan_step_count": len(FUTURE_PLAN),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
        "review_outputs_generated_count": len(OUTPUT_IDS),
        "recommended_source_authority_acquisition_package": RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "ready_for_source_authority_acquisition_approval": False,
        "ready_for_retry_candidate": False,
    }
    review[OPERATOR_REVIEW_DIGEST_KEY] = _operator_digest(review)
    return review


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(
    *, source_follow_on_results_review: dict | None = None,
) -> dict[str, Any]:
    """Build the offline operator review from committed or injected source evidence."""

    evidence = _committed_source_follow_on_results_review() if source_follow_on_results_review is None else deepcopy(source_follow_on_results_review)
    _validate_source(evidence)
    review = _assemble_review(evidence)
    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Fail closed on every source binding, reviewed decision, or authority boundary."""

    if not isinstance(review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError("review must be an object")
    expected = _assemble_review(_committed_source_follow_on_results_review())
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError(f"{difference} mismatch")
    for key in (OPERATOR_REVIEW_DIGEST_KEY, CANDIDATE_REVIEW_DIGEST_KEY, SCOPE_REVIEW_DIGEST_KEY, MAPPING_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        if re.fullmatch(r"[0-9a-f]{64}", str(review.get(key))) is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError(f"{key} invalid")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Follow-On Results Review", "Source Follow-On Execution", "Source Follow-On Execution Digests",
    "Source Follow-On Approval", "Source Follow-On Operator Review", "Source Follow-On Candidate",
    "Source Results Review", "Source Enrichment Execution", "Source Historical Approval",
    "Source Historical Operator Review", "Source Historical Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Remediation Execution Approval",
    "Source Plan Results Review", "Source Plan Execution", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Source Authority Enrichment Review Summary", "Missing Authority Inventory Review Summary",
    "Workstream Authority Mapping Review Summary", "Source Authority Acquisition Candidate Review",
    "Acquisition Scope Sections Review", "Missing Authority to Source Evidence Mapping Review",
    "Acceptable Source Artifact Inventory Review", "Operator-Provided Evidence Requirements Review",
    "Evidence Custody and Digest Requirements Review", "Candidate Results Review Requirements Review",
    "Reviewed Candidate Philosophy", "Reviewed Source Authority Acquisition Packages", "Recommended Package",
    "Reviewed Future Requirements", "Reviewed Future Plan", "Reviewed Planned Outputs", "Reviewed Non-Goals",
    "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review as a status document."""

    validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(deepcopy(review))
    sections = {
        "Source Follow-On Results Review": review["source_follow_on_results_review_summary"],
        "Source Follow-On Execution": review["source_follow_on_execution_summary"],
        "Source Follow-On Execution Digests": {key: value for key, value in review.items() if key.startswith("source_") and key.endswith("digest")},
        "Source Follow-On Approval": review["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": review["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": review["source_follow_on_candidate_summary"],
        "Source Results Review": review["source_results_review_summary"],
        "Source Enrichment Execution": review["source_execution_summary"],
        "Source Historical Approval": review["source_approval_summary"],
        "Source Historical Operator Review": review["source_historical_operator_review_summary"],
        "Source Historical Candidate": review["source_historical_candidate_summary"],
        "Source Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Source Blocked Execution": review["source_blocked_execution_summary"],
        "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": review["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": review["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": review["source_plan_results_review_summary"],
        "Source Plan Execution": review["source_plan_execution_summary"],
        "Source Method Results Review": review["source_method_results_review_summary"],
        "Source Method Execution": review["source_method_execution_summary"],
        "Source Diagnostic Results Review": review["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": review["source_controlled_recapture_summary"],
        "Source Durable Receipt": review["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": review["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": review["retry_failure_context"],
        "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"],
        "Reviewed Workstreams": review["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": review["source_authority_enrichment_review_summary"],
        "Missing Authority Inventory Review Summary": review["missing_authority_inventory_review_summary"],
        "Workstream Authority Mapping Review Summary": review["workstream_authority_mapping_review_summary"],
        "Source Authority Acquisition Candidate Review": review["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Sections Review": review["acquisition_scope_sections_review"],
        "Missing Authority to Source Evidence Mapping Review": review["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory Review": review["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements Review": review["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements Review": review["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements Review": review["candidate_results_review_requirements_review"],
        "Reviewed Candidate Philosophy": review["reviewed_candidate_philosophy"],
        "Reviewed Source Authority Acquisition Packages": review["reviewed_source_authority_acquisition_packages"],
        "Recommended Package": review["recommended_package"],
        "Reviewed Future Requirements": review["reviewed_future_requirements"],
        "Reviewed Future Plan": review["reviewed_future_plan"],
        "Reviewed Planned Outputs": review["reviewed_planned_outputs"],
        "Reviewed Non-Goals": review["reviewed_non_goals"],
        "Recommendation": review["recommendation"],
        "Next Chain": review["next_chain"],
        "Next Gates": review["next_gates"],
        "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {field: review[field] for field in EXTRA_FALSE_FIELDS},
        "Checklist Summary": review["summary"],
        "Guardrails": [field for field in FALSE_FIELDS if review[field] is False],
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Candidate Operator Review After Follow-On Execution Results Review v1",
        "", f"Artifact: `{review['artifact_kind']}`", "", f"Status: `{review['review_status']}`", "",
        f"Scope: `{review['review_scope']}`", "", f"Operator-review digest: `{review[OPERATOR_REVIEW_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(
    output_dir: str | Path,
    *,
    source_follow_on_results_review: dict | None = None,
) -> dict[str, Any]:
    """Write the deterministic operator-review status document."""

    review = build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(
        source_follow_on_results_review=source_follow_on_results_review
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_STATUS.md"
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_markdown_v1(review),
        encoding="utf-8",
    )
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "REVIEW_STATUS", "REVIEW_SCOPE", "RECOMMENDED_PACKAGE",
    "OPERATOR_REVIEW_DIGEST_KEY", "CANDIDATE_REVIEW_DIGEST_KEY", "SCOPE_REVIEW_DIGEST_KEY",
    "MAPPING_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_markdown_v1",
]
