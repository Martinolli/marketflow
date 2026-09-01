"""Approve one module-grouping source-recovery package for future execution."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED_V1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_"
    "APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN"
)
SCHEMA_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_module_grouping_"
    "source_recovery_approval_v1"
)
SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE = source.source.RECOMMENDED_PACKAGE
SOURCE_OPERATOR_REVIEW_DIGEST = "f124b1bf3af19dbe722815d232f7e827af2373ceb449279d5ac80b4533f9b00e"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE MODULE GROUPING SOURCE RECOVERY "
    "PACKAGE_RECOVER_MODULE_GROUPING_DETAIL_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY "
    "MARKETFLOW RECOVER MODULE GROUPING DETAIL FROM REVIEWED DETACHED PYTEST CACHE READ ONLY "
    "NO CACHE READ NOW NO RETRY NO FULL PYTEST NO RESULTS REVIEW NO MAIN PUSH "
    "MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN"
)
OPERATOR_DECISION = "APPROVE_MODULE_GROUPING_SOURCE_RECOVERY"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_module_grouping_"
    "source_recovery_approval_attestation_v1"
)
APPROVED_ONLY = "APPROVED_FOR_FUTURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_EXECUTION_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts",
    "operator_confirms_classification_evidence_summary",
    "operator_confirms_module_count_29",
    "operator_confirms_largest_module_counts",
    "operator_confirms_known_missing_detail",
    "operator_confirms_unsupported_claims_boundary",
    "operator_confirms_approval_scope_only",
    "operator_confirms_no_source_recovery_execution",
    "operator_confirms_no_module_grouping_recovered",
    "operator_confirms_no_module_paths_recovered",
    "operator_confirms_no_per_module_counts_recovered",
    "operator_confirms_no_bounded_nodeid_samples_recovered",
    "operator_confirms_no_cache_read",
    "operator_confirms_no_cache_modification",
    "operator_confirms_no_retry",
    "operator_confirms_no_full_pytest",
    "operator_confirms_no_diagnostic_command",
    "operator_confirms_no_diagnostic_execution",
    "operator_confirms_no_remediation_execution",
    "operator_confirms_no_classification_execution",
    "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review",
    "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_integration_digest",
    "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push",
    "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete",
    "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation",
    "operator_confirms_no_evidence_regeneration",
    "operator_confirms_no_marketflow_commit",
    "operator_confirms_no_pytest_cache_commit",
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
    "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

APPROVED_REQUIREMENT_IDS = [
    "source_operator_review_must_be_ready",
    "source_candidate_must_be_ready",
    "source_blocked_after_v2_execution_must_be_ready",
    "source_blocked_execution_digest_must_be_bound",
    "source_blocked_manifest_digest_must_be_bound",
    "source_results_review_v2_must_be_ready",
    "source_module_grouping_digest_must_be_bound",
    "retry_failure_counts_must_be_bound",
    "module_count_and_largest_counts_must_be_bound",
    "known_missing_detail_must_be_bound",
    "unsupported_claims_boundary_must_be_preserved",
    "source_recovery_must_not_rerun_retry",
    "source_recovery_must_not_run_full_pytest",
    "source_recovery_must_not_run_diagnostic_commands",
    "source_recovery_must_not_treat_cache_as_retry_success_evidence",
    "source_recovery_must_not_infer_module_paths",
    "source_recovery_must_fail_closed_if_cache_hash_or_count_mismatches",
    "source_recovery_must_fail_closed_if_module_detail_unavailable",
    "source_recovery_must_not_commit_pytest_cache",
    "source_recovery_must_not_commit_marketflow_outputs",
    "source_recovery_must_preserve_origin_main",
    "source_recovery_must_preserve_integration_branch",
    "source_recovery_must_preserve_staged_evidence",
    "future_planning_reentry_requires_source_recovery_results_review",
    "future_retry_requires_separate_approval",
    "main_merge_requires_passing_retry_results_review",
]
APPROVED_FUTURE_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "requirement_value": True,
        "approval_status": APPROVED_ONLY,
    }
    for requirement_id in APPROVED_REQUIREMENT_IDS
]

FUTURE_PLAN_STEPS = [
    "Bind blocked after-v2 execution digest and blocked-manifest digest.",
    "Bind Classification Method Results Review v2 digest and module-grouping digest.",
    "Verify protected refs and untracked .marketflow / .pytest_cache boundaries.",
    "Use the approved source: reviewed detached pytest cache.",
    "Verify reviewed lastfailed and nodeids hashes and counts before parsing.",
    "Recover module paths, per-module counts, percentages, deterministic priority order, and bounded node-ID samples.",
    "Produce a bounded module grouping source recovery artifact.",
    "Preserve unsupported claims: no failure/error separation, first-order claim, traceback root cause, direct remediation, retry success, or main merge readiness.",
    "Require source-recovery results review before re-entering after-v2 planning execution.",
    "Keep new retry, main merge, runtime, and trading closed.",
]
APPROVED_FUTURE_PLAN = [
    {
        "step_id": f"future_source_recovery_step_{index:02d}",
        "source_step": step,
        "approval_status": APPROVED_ONLY,
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(FUTURE_PLAN_STEPS, 1)
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": item["output_id"], "authorization_status": "AUTHORIZED_NOT_GENERATED"}
    for item in source.REVIEWED_PLANNED_OUTPUTS
]
SUPPORTING_PACKAGE_STATUSES = {
    "PACKAGE_EXPOSE_MODULE_GROUPING_FROM_CLASSIFICATION_EXECUTION_V2_OUTPUT_IF_LOCATABLE": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_OPERATOR_PROVIDED_CLASSIFICATION_EXECUTION_V2_MODULE_GROUPING_REPORT_PATH": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CREATE_BOUNDED_COMMITTED_MODULE_GROUPING_SUMMARY_FROM_VERIFIED_CACHE": "AVAILABLE_NOT_SELECTED_HIGH_CONTROL",
    "PACKAGE_RECOVER_ONLY_TOP_MODULE_PATHS_FROM_VERIFIED_CACHE": "AVAILABLE_NOT_SELECTED",
}
SUPPORTING_PACKAGES = [
    {"package_id": package_id, "approval_status": status, "selected": False, "approved": False}
    for package_id, status in SUPPORTING_PACKAGE_STATUSES.items()
]
BLOCKED_PACKAGE_STATUSES = {
    "PACKAGE_USE_AGGREGATE_COUNTS_AND_TOP_COUNTS_WITHOUT_MODULE_PATHS": "BLOCKED_NOT_APPROVED_INSUFFICIENT",
    "PACKAGE_INFER_MODULE_NAMES_FROM_COUNTS_OR_DIGESTS": "BLOCKED_NOT_APPROVED",
    "PACKAGE_RERUN_AUTHORITATIVE_RETRY_TO_RECREATE_MODULE_GROUPING": "BLOCKED_NOT_APPROVED",
    "PACKAGE_DIRECT_REMEDIATION_OR_NEW_RETRY_WITHOUT_MODULE_GROUPING_SOURCE": "BLOCKED_NOT_APPROVED",
    "PACKAGE_MAIN_MERGE_DESPITE_MISSING_MODULE_GROUPING_SOURCE": "BLOCKED_NOT_APPROVED",
}
BLOCKED_PACKAGES = [
    {"package_id": package_id, "approval_status": status, "selected": False, "approved": False}
    for package_id, status in BLOCKED_PACKAGE_STATUSES.items()
]
NEXT_CHAIN = [
    "Module Grouping Source Recovery Execution v1, if approved.",
    "Module Grouping Source Recovery Results Review v1.",
    "Re-enter after-v2 planning execution, if source detail is recovered and reviewed.",
    "Remediation or Method Results Review After Classification v2 Review v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Approval / Execution / Results Review, if selected.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "module_grouping_source_recovery_execution_if_approved",
    "module_grouping_source_recovery_results_review",
    "after_v2_planning_reentry_if_source_recovered",
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "approval_source_recovery_does_not_execute_source_recovery",
    "approval_source_recovery_does_not_recover_module_grouping",
    "approval_source_recovery_does_not_expose_module_paths",
    "approval_source_recovery_does_not_read_cache",
    "approval_source_recovery_does_not_modify_cache",
    "approval_source_recovery_does_not_parse_operator_logs",
    "approval_source_recovery_does_not_run_diagnostic_commands",
    "approval_source_recovery_does_not_execute_diagnostics",
    "approval_source_recovery_does_not_execute_remediation",
    "approval_source_recovery_does_not_execute_classification",
    "approval_source_recovery_does_not_classify_modules_again",
    "approval_source_recovery_does_not_rerun_retry",
    "approval_source_recovery_does_not_run_full_pytest",
    "approval_source_recovery_does_not_create_new_retry_candidate",
    "approval_source_recovery_does_not_create_retry_results_review",
    "approval_source_recovery_does_not_create_integration_results_review",
    "approval_source_recovery_does_not_mark_integration_successful",
    "approval_source_recovery_does_not_generate_successful_integration_digest",
    "approval_source_recovery_does_not_claim_failure_error_separation",
    "approval_source_recovery_does_not_claim_first_failure",
    "approval_source_recovery_does_not_claim_first_error",
    "approval_source_recovery_does_not_claim_traceback_root_cause",
    "approval_source_recovery_does_not_recommend_direct_code_remediation",
    "approval_source_recovery_does_not_treat_cache_or_classification_as_retry_success",
    "approval_source_recovery_does_not_push_integration_branch",
    "approval_source_recovery_does_not_push_main",
    "approval_source_recovery_does_not_delete_integration_branch",
    "approval_source_recovery_does_not_delete_worktree",
    "approval_source_recovery_does_not_force_push",
    "approval_source_recovery_does_not_prune_remotes",
    "approval_source_recovery_does_not_modify_tags",
    "approval_source_recovery_does_not_commit_marketflow_outputs",
    "approval_source_recovery_does_not_commit_pytest_cache",
    "approval_source_recovery_does_not_modify_staged_evidence",
    "approval_source_recovery_does_not_regenerate_evidence",
    "approval_source_recovery_does_not_call_providers",
    "approval_source_recovery_does_not_acquire_market_data",
    "approval_source_recovery_does_not_regenerate_dataset",
    "approval_source_recovery_does_not_recompute_metrics",
    "approval_source_recovery_does_not_train_models",
    "approval_source_recovery_does_not_score_strategy",
    "approval_source_recovery_does_not_generate_recommendations",
    "approval_source_recovery_does_not_accept_predictive_usefulness",
    "approval_source_recovery_does_not_accept_profitability",
    "approval_source_recovery_does_not_authorize_runtime",
    "approval_source_recovery_does_not_authorize_broker_execution",
    "selected_source_recovery_package_approved_for_future_execution_only",
    "source_recovery_output_would_be_planning_source_not_root_cause",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_execution_required_before_source_recovery",
    "separate_results_review_required_after_source_recovery",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_operator_review_digest_bound", "source_candidate_digest_bound",
    "source_blocked_execution_digest_bound", "source_blocked_manifest_digest_bound",
    "source_blocked_reason_bound", "source_results_review_v2_digest_bound",
    "source_execution_v2_digest_bound", "source_module_grouping_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound",
    "classification_evidence_summary_bound", "module_count_29_bound",
    "largest_module_counts_bound", "known_missing_detail_bound",
    "unsupported_claims_boundary_bound", "operator_decision_matches",
    "operator_attestation_phrase_matches", "approval_scope_only",
    "selected_package_reviewed_cache_read_only_recovery", "approval_created_true",
    "source_recovery_selected_true", "source_recovery_approved_true",
    "source_recovery_authorized_true", "ready_for_source_recovery_execution_true",
    "source_recovery_executed_false", "module_grouping_detail_recovered_false",
    "module_grouping_detail_exposed_false", "module_paths_recovered_false",
    "per_module_counts_recovered_false", "bounded_nodeid_samples_recovered_false",
    "cache_read_false", "cache_modified_false", "retry_rerun_false",
    "full_pytest_false", "diagnostic_command_false", "diagnostic_execution_false",
    "remediation_execution_false", "classification_execution_false",
    "new_retry_candidate_created_false", "new_retry_executed_false",
    "new_retry_results_review_created_false", "main_merge_approval_created_false",
    "integration_success_false", "successful_integration_digest_false",
    "integration_branch_pushed_false", "main_push_false", "origin_main_modified_false",
    "marketflow_outputs_committed_false", "pytest_cache_committed_false",
    "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "requirements_approved_for_future_execution", "future_plan_approved_not_executed",
    "planned_outputs_authorized_not_generated", "supporting_packages_not_selected",
    "blocked_packages_not_approved", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(ValueError):
    """Raised when an attestation or approval crosses its authority boundary."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00").utcoffset() is not None
    except ValueError:
        return False


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_module_grouping_source_recovery_package": SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
        "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_blocked_execution_digest": source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "operator_confirms_source_blocked_manifest_digest": source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "operator_confirms_blocked_reason": source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "operator_confirms_source_results_review_v2_digest": source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "operator_confirms_source_execution_v2_digest": source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        "operator_confirms_source_module_grouping_digest": source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_source_recovery_package": SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
                f"{field} mismatch"
            )
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "operator attestation timestamp invalid"
        )
    reference = attestation.get("operator_reference")
    if not isinstance(reference, str) or not reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "operator reference missing"
        )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
                f"{field} must be true"
            )


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_blocked_execution_digest: str,
    operator_confirms_source_blocked_manifest_digest: str,
    operator_confirms_blocked_reason: str,
    operator_confirms_source_results_review_v2_digest: str,
    operator_confirms_source_execution_v2_digest: str,
    operator_confirms_source_module_grouping_digest: str,
    operator_confirms_retry_execution_commit: str,
    operator_confirms_retry_failure_counts: bool,
    operator_confirms_classification_evidence_summary: bool,
    operator_confirms_module_count_29: bool,
    operator_confirms_largest_module_counts: bool,
    operator_confirms_known_missing_detail: bool,
    operator_confirms_unsupported_claims_boundary: bool,
    operator_confirms_selected_source_recovery_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_source_recovery_execution: bool,
    operator_confirms_no_module_grouping_recovered: bool,
    operator_confirms_no_module_paths_recovered: bool,
    operator_confirms_no_per_module_counts_recovered: bool,
    operator_confirms_no_bounded_nodeid_samples_recovered: bool,
    operator_confirms_no_cache_read: bool,
    operator_confirms_no_cache_modification: bool,
    operator_confirms_no_retry: bool,
    operator_confirms_no_full_pytest: bool,
    operator_confirms_no_diagnostic_command: bool,
    operator_confirms_no_diagnostic_execution: bool,
    operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_classification_execution: bool,
    operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_integration_digest: bool,
    operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_evidence_regeneration: bool,
    operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_pytest_cache_commit: bool,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_module_grouping_source_recovery_package: str = SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    attestation = dict(locals())
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(attestation)
    return attestation


def _source_fields() -> dict[str, Any]:
    review = source._base()
    fields = [
        "source_module_grouping_source_recovery_candidate_digest",
        "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest",
        "blocked_reason", "source_after_v2_approval_digest", "source_after_v2_operator_review_digest",
        "source_after_v2_candidate_digest", "source_results_review_v2_digest",
        "source_review_manifest_digest", "source_execution_v2_digest", "source_module_grouping_digest",
        "source_digest_manifest_digest", "source_approval_v2_digest", "source_staged_inventory_digest",
        "retry_execution_branch", "retry_execution_commit", "retry_pytest_passed_count",
        "retry_pytest_failed_count", "retry_pytest_error_count", "retry_pytest_skipped_count",
        "retry_pytest_first_result_authoritative", "root_full_regression_is_retry_evidence",
        "classification_evidence_summary", "failed_or_errored_nodeids_count",
        "module_summary_module_count", "largest_module_nodeid_counts", "known_available_detail",
        "known_missing_detail", "unsupported_claims_boundary", "origin_main_commit",
        "integration_branch_name", "integration_branch_head_commit", "remote_integration_branch_exists",
        "detached_integration_worktree_path", "detached_integration_worktree_head_commit",
        "staged_evidence_manifest_digest", "staged_evidence_unchanged",
        "marketflow_outputs_tracked_in_repository", "marketflow_outputs_tracked_in_detached_worktree",
        "pytest_cache_tracked_in_repository", "pytest_cache_tracked_in_detached_worktree",
    ]
    return {
        "source_module_grouping_source_recovery_operator_review_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1,
        "source_module_grouping_source_recovery_operator_review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY,
        "source_module_grouping_source_recovery_operator_review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN,
        "source_module_grouping_source_recovery_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        **{field: deepcopy(review[field]) for field in fields},
    }


def _base(attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED_V1,
        "schema_version": SCHEMA_VERSION,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN,
        "selected_module_grouping_source_recovery_package": SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "operator_attestation_required": True,
        **_source_fields(),
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_package": {
            "package_id": SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
            "approval_status": APPROVED_ONLY,
            "selected": True,
            "approved": True,
            "authorized_for_future_execution": True,
            "executed": False,
        },
        "approved_future_requirements": deepcopy(APPROVED_FUTURE_REQUIREMENTS),
        "approved_future_plan": deepcopy(APPROVED_FUTURE_PLAN),
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "module_grouping_source_recovery_selected": True,
        "module_grouping_source_recovery_approved": True,
        "module_grouping_source_recovery_authorized": True,
        "module_grouping_source_recovery_approval_created": True,
        "ready_for_module_grouping_source_recovery_execution": True,
        "module_grouping_source_recovery_executed": False,
        "module_grouping_detail_recovered": False,
        "module_grouping_detail_exposed": False,
        "module_paths_recovered": False,
        "per_module_counts_recovered": False,
        "bounded_nodeid_samples_recovered": False,
        "cache_read": False,
        "cache_modified": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_execution_performed": False,
        "remediation_execution_performed": False,
        "classification_execution_performed": False,
        "remediation_or_method_after_v2_reentry_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


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
    attestation = approval.get("operator_attestation", {})
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_candidate_digest_bound": (source.SOURCE_CANDIDATE_DIGEST, approval.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_execution_digest_bound": (source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, approval.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_manifest_digest_bound": (source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, approval.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.source.source.BLOCKED_REASON_MODULE_DETAIL, approval.get("blocked_reason")),
        "source_results_review_v2_digest_bound": (source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, approval.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, approval.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, approval.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", approval.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [approval.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "classification_evidence_summary_bound": (source.source._classification_summary(), approval.get("classification_evidence_summary")),
        "module_count_29_bound": (29, approval.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], approval.get("largest_module_nodeid_counts")),
        "known_missing_detail_bound": (source.source.KNOWN_MISSING_DETAIL, approval.get("known_missing_detail")),
        "unsupported_claims_boundary_bound": (source.source.UNSUPPORTED_CLAIMS_BOUNDARY, approval.get("unsupported_claims_boundary")),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_reviewed_cache_read_only_recovery": (SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE, approval.get("selected_module_grouping_source_recovery_package")),
        "approval_created_true": (True, approval.get("module_grouping_source_recovery_approval_created")),
        "source_recovery_selected_true": (True, approval.get("module_grouping_source_recovery_selected")),
        "source_recovery_approved_true": (True, approval.get("module_grouping_source_recovery_approved")),
        "source_recovery_authorized_true": (True, approval.get("module_grouping_source_recovery_authorized")),
        "ready_for_source_recovery_execution_true": (True, approval.get("ready_for_module_grouping_source_recovery_execution")),
    }
    false_fields = {
        "source_recovery_executed_false": "module_grouping_source_recovery_executed",
        "module_grouping_detail_recovered_false": "module_grouping_detail_recovered",
        "module_grouping_detail_exposed_false": "module_grouping_detail_exposed",
        "module_paths_recovered_false": "module_paths_recovered",
        "per_module_counts_recovered_false": "per_module_counts_recovered",
        "bounded_nodeid_samples_recovered_false": "bounded_nodeid_samples_recovered",
        "cache_read_false": "cache_read", "cache_modified_false": "cache_modified",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed",
        "diagnostic_execution_false": "diagnostic_execution_performed",
        "remediation_execution_false": "remediation_execution_performed",
        "classification_execution_false": "classification_execution_performed",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_approval",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_approval",
        "dataset_generation_false": "dataset_generation_performed_in_approval",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, approval.get(field)) for check_id, field in false_fields.items()})
    values.update({
        "successful_integration_digest_false": ([False, False], [approval.get("successful_integration_execution_digest_generated"), approval.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_REQUIREMENTS, approval.get("approved_future_requirements")),
        "future_plan_approved_not_executed": (APPROVED_FUTURE_PLAN, approval.get("approved_future_plan")),
        "planned_outputs_authorized_not_generated": (AUTHORIZED_PLANNED_OUTPUTS, approval.get("authorized_planned_outputs")),
        "supporting_packages_not_selected": (SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        "blocked_packages_not_approved": (BLOCKED_PACKAGES, approval.get("blocked_packages")),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "no_tracked_marketflow_files": (False, approval.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, approval.get("pytest_cache_tracked_in_repository")),
    })
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(item["severity"] == BLOCKER for item in failed),
        "module_grouping_source_recovery_selected": True,
        "module_grouping_source_recovery_approved": True,
        "module_grouping_source_recovery_authorized": True,
        "module_grouping_source_recovery_approval_created": True,
        "selected_module_grouping_source_recovery_package": SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
        "ready_for_module_grouping_source_recovery_execution": True,
        "source_recovery_executed": False, "module_grouping_detail_recovered": False,
        "module_paths_recovered": False, "per_module_counts_recovered": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "integration_execution_successful": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict
) -> dict:
    _validate_attestation(operator_attestation)
    if source_review is not None:
        source.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(source_review)
        if source_review.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest") != SOURCE_OPERATOR_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
                "source operator-review digest mismatch"
            )
    approval = _base(operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest"] = marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest_v1(approval)
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(
    approval: dict,
) -> dict:
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "approval must be an object"
        )
    _validate_attestation(approval.get("operator_attestation", {}))
    expected = _base(approval["operator_attestation"])
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
                f"{field} mismatch"
            )
    checklist = _checklist(approval)
    if approval.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "checklist invalid"
        )
    summary = _summary(checklist)
    if approval.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "summary mismatch"
        )
    digest = approval.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "approval digest missing"
        )
    if digest != marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest_v1(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "approval digest mismatch"
        )
    return {
        "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(
    output_dir: str | Path, *, source_review: dict | None = None, operator_attestation: dict
) -> dict:
    approval = build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    path = Path(output_dir) / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError(
            "output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest": approval["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest"],
        "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_markdown_v1(
    approval: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(approval)
    sections = [
        ("Operator Attestation", [f"Decision: `{OPERATOR_DECISION}`."]),
        ("Source Operator Review", [f"Digest: `{SOURCE_OPERATOR_REVIEW_DIGEST}`."]),
        ("Source Module Grouping Source Recovery Candidate", [f"Digest: `{source.SOURCE_CANDIDATE_DIGEST}`."]),
        ("Source Blocked After-v2 Execution", [f"Reason: `{source.source.source.BLOCKED_REASON_MODULE_DETAIL}`."]),
        ("Source Classification Results Review v2", [f"Digest: `{approval['source_results_review_v2_digest']}`."]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; root regression is not retry evidence."]),
        ("Known Available and Missing Detail", [*[f"Available: {item}" for item in approval["known_available_detail"]], *[f"Missing: {item}" for item in approval["known_missing_detail"]]]),
        ("Approval Scope", ["Future module-grouping source-recovery execution only; no execution or cache read occurs here."]),
        ("Selected Source Recovery Package", [f"`{SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE}`."]),
        ("Approved Future Source Recovery Requirements", [item["requirement_id"] for item in APPROVED_FUTURE_REQUIREMENTS]),
        ("Approved Future Source Recovery Plan", [item["source_step"] for item in APPROVED_FUTURE_PLAN]),
        ("Planned Outputs", [item["output_id"] for item in AUTHORIZED_PLANNED_OUTPUTS]),
        ("Supporting Packages", [item["package_id"] for item in SUPPORTING_PACKAGES]),
        ("Blocked Packages", [item["package_id"] for item in BLOCKED_PACKAGES]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Execution, cache access, retry, main merge, runtime, and trading remain closed."]),
        ("Checklist Summary", [f"`{validation['passed_checks']}/{validation['total_checks']}` checks pass."]),
        ("Guardrails", ["Separate source-recovery execution and results review remain required."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Approval v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN",
    "SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE", "REQUIRED_OPERATOR_ATTESTATION_PHRASE",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1",
    "write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_markdown_v1",
]
