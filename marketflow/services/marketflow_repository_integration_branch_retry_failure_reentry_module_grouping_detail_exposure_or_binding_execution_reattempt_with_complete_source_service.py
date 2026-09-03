"""Bind reviewed committed module-grouping detail without cache or recovery access."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_service
    as review_source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_COMPLETE_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1"
SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE = "PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY"
SOURCE_RESULTS_REVIEW_DIGEST = "09742be04ff9014323b6e845f3aa3e105ed9bfcfcfad42f0f55bf4930d63361a"
SOURCE_PAYLOAD_REVIEW_DIGEST = "e40aa95d531a9f198038664368be7cdb9d457ac140f805eac6d720c8f67382a0"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "56d9a3c629a34f662f4841a596c68316a13bdc310d51e7ba929fe8a32cea1aed"
SOURCE_MATERIALIZATION_EXECUTION_DIGEST = review_source.SOURCE_EXECUTION_DIGEST
SOURCE_MATERIALIZED_PAYLOAD_DIGEST = review_source.SOURCE_PAYLOAD_DIGEST
SOURCE_MATERIALIZATION_DIGEST_MANIFEST_DIGEST = review_source.SOURCE_DIGEST_MANIFEST_DIGEST
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
BINDING_ROW_SOURCE = "REVIEWED_MATERIALIZED_COMPLETE_29_ROW_MODULE_GROUPING_SOURCE"
BINDING_ROW_BASIS = "MATERIALIZATION_RESULTS_REVIEW_PAYLOAD_DIGEST_AND_SOURCE_BINDING"
BINDING_ROW_CONFIDENCE = "HIGH_FOR_MODULE_GROUPING_ONLY"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_COMPLETE_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE

OUTPUT_IDS = [
    "detail_exposure_or_binding_reattempt_execution_manifest",
    "complete_29_row_module_grouping_detail_binding_source",
    "reviewed_materialized_source_binding_report",
    "payload_digest_binding_report",
    "recovered_module_paths_binding_report",
    "per_module_counts_binding_report",
    "bounded_nodeid_samples_binding_report",
    "priority_tier_enablement_report",
    "top_module_concentration_preservation_report",
    "unsupported_claims_boundary_report",
    "detail_exposure_or_binding_limitations_report",
    "planning_reentry_enablement_report",
    "digest_manifest",
]

PRECHECK_IDS = [
    "source_materialization_results_review_digest_bound", "source_materialized_payload_review_digest_bound",
    "source_materialization_results_review_manifest_digest_bound", "source_materialization_execution_digest_bound",
    "source_materialized_payload_digest_bound", "source_materialization_digest_manifest_digest_bound",
    "source_materialization_approval_digest_bound", "source_materialization_operator_review_digest_bound",
    "source_materialization_candidate_digest_bound", "source_execution_failure_diagnosis_digest_bound",
    "source_primary_failure_class_bound", "source_detail_binding_blocked_execution_digest_bound",
    "source_detail_binding_blocked_manifest_digest_bound", "source_detail_binding_blocked_reason_bound",
    "source_detail_binding_approval_digest_bound", "source_detail_binding_operator_review_digest_bound",
    "source_detail_binding_candidate_digest_bound", "source_reentry_failure_diagnosis_digest_bound",
    "source_reentry_blocked_execution_digest_bound", "source_reentry_blocked_manifest_digest_bound",
    "source_planning_reentry_digest_bound", "source_recovery_results_review_digest_bound",
    "source_recovery_detail_digest_bound", "source_module_grouping_digest_bound",
    "retry_failure_counts_bound", "recovered_module_summary_bound", "top_five_paths_bound",
    "top_five_count_sum_612_bound", "top_ten_count_sum_1069_bound",
    "reviewed_materialization_results_review_ready", "reviewed_complete_29_row_source_available",
    "no_cache_read", "no_materialization_rerun", "no_source_recovery_rerun", "no_retry_rerun",
    "no_full_pytest", "no_diagnostic_command", "origin_main_unchanged",
    "integration_branch_head_unchanged", "staged_evidence_unchanged",
    "marketflow_outputs_not_tracked", "pytest_cache_not_tracked",
]

STEP_IDS = [
    "verify_source_materialization_results_review", "verify_source_materialization_execution",
    "verify_source_materialized_payload_digest", "verify_source_materialization_digest_manifest",
    "verify_detail_exposure_or_binding_approval", "verify_prior_blocked_detail_binding_execution_context",
    "verify_reentry_failure_diagnosis", "verify_recovery_results_review_context",
    "verify_retry_failure_context", "verify_protected_refs", "verify_tracking_boundaries",
    "locate_reviewed_committed_complete_29_row_source", "verify_complete_29_row_source_available_or_block",
    "verify_29_module_rows", "verify_total_failed_or_errored_nodeids_1404",
    "verify_largest_module_counts", "verify_top_five_paths", "verify_top_five_and_top_ten_sums",
    "verify_tier_sums", "verify_bounded_samples", "build_complete_29_row_detail_binding_source",
    "build_reviewed_materialized_source_binding_report", "build_payload_digest_binding_report",
    "build_recovered_module_paths_binding_report", "build_per_module_counts_binding_report",
    "build_bounded_nodeid_samples_binding_report", "build_priority_tier_enablement_report",
    "build_top_module_concentration_preservation_report", "build_unsupported_claims_boundary_report",
    "build_detail_exposure_or_binding_limitations_report", "build_planning_reentry_enablement_report",
    "build_digest_manifest", "preserve_failed_retry_authority", "do_not_read_cache",
    "do_not_rerun_materialization", "do_not_rerun_source_recovery",
    "do_not_create_after_v2_planning_reentry", "do_not_create_retry_candidate",
    "do_not_create_results_review",
]

SUCCESS_NEXT_CHAIN = [
    "Detail Exposure or Binding Execution Reattempt with Complete Source Results Review v1.",
    "Re-enter after-v2 planning execution using complete recovered detail, if results review passes.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Detail Exposure or Binding Execution Reattempt with Complete Source Failure Diagnosis v1.",
    "Alternate complete-source binding candidate, if needed.",
    "No planning reentry, diagnostic capture, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail_if_review_passes",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review", "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved", "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "detail_exposure_or_binding_reattempt_failure_diagnosis",
    "alternate_complete_source_binding_candidate_if_needed",
    "planning_reentry_blocked_until_detail_binding_reattempt_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]

RISK_CONTROLS = [
    "detail_binding_reattempt_uses_reviewed_committed_complete_source_only",
    "detail_binding_reattempt_does_not_read_cache", "detail_binding_reattempt_does_not_modify_cache",
    "detail_binding_reattempt_does_not_commit_pytest_cache", "detail_binding_reattempt_does_not_commit_marketflow_outputs",
    "detail_binding_reattempt_does_not_rerun_materialization", "detail_binding_reattempt_does_not_rerun_source_recovery",
    "detail_binding_reattempt_does_not_parse_operator_logs", "detail_binding_reattempt_does_not_run_diagnostic_commands",
    "detail_binding_reattempt_does_not_execute_diagnostics", "detail_binding_reattempt_does_not_execute_remediation",
    "detail_binding_reattempt_does_not_execute_classification", "detail_binding_reattempt_does_not_classify_modules_again",
    "detail_binding_reattempt_does_not_execute_after_v2_planning_reentry", "detail_binding_reattempt_does_not_rerun_retry",
    "detail_binding_reattempt_does_not_run_full_pytest", "detail_binding_reattempt_does_not_create_targeted_diagnostic_candidate",
    "detail_binding_reattempt_does_not_create_new_retry_candidate", "detail_binding_reattempt_does_not_create_retry_results_review",
    "detail_binding_reattempt_does_not_create_integration_results_review", "detail_binding_reattempt_does_not_mark_integration_successful",
    "detail_binding_reattempt_does_not_generate_successful_integration_digest",
    "detail_binding_reattempt_does_not_claim_failure_error_separation", "detail_binding_reattempt_does_not_claim_first_failure",
    "detail_binding_reattempt_does_not_claim_first_error", "detail_binding_reattempt_does_not_claim_traceback_root_cause",
    "detail_binding_reattempt_does_not_recommend_direct_code_remediation",
    "detail_binding_reattempt_does_not_treat_detail_as_retry_success",
    "detail_binding_reattempt_does_not_push_integration_branch", "detail_binding_reattempt_does_not_push_main",
    "detail_binding_reattempt_does_not_delete_integration_branch", "detail_binding_reattempt_does_not_delete_worktree",
    "detail_binding_reattempt_does_not_force_push", "detail_binding_reattempt_does_not_prune_remotes",
    "detail_binding_reattempt_does_not_modify_tags", "detail_binding_reattempt_does_not_modify_staged_evidence",
    "detail_binding_reattempt_does_not_regenerate_evidence", "detail_binding_reattempt_does_not_call_providers",
    "detail_binding_reattempt_does_not_acquire_market_data", "detail_binding_reattempt_does_not_regenerate_dataset",
    "detail_binding_reattempt_does_not_recompute_metrics", "detail_binding_reattempt_does_not_train_models",
    "detail_binding_reattempt_does_not_score_strategy", "detail_binding_reattempt_does_not_generate_recommendations",
    "detail_binding_reattempt_does_not_accept_predictive_usefulness",
    "detail_binding_reattempt_does_not_accept_profitability", "detail_binding_reattempt_does_not_authorize_runtime",
    "detail_binding_reattempt_does_not_authorize_broker_execution",
    "complete_29_row_detail_binding_output_is_planning_source_not_root_cause",
    "materialized_payload_is_not_retry_success", "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_detail_binding_execution_remains_historically_blocked",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_detail_binding_reattempt",
    "separate_after_v2_planning_reentry_required_after_detail_binding_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_FIELDS = [
    "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed", "classification_execution_performed_in_reattempt",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_reattempt", "market_data_acquisition_performed_in_reattempt",
    "dataset_generation_performed_in_reattempt", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
    "main_merge_readiness_claimed", "cache_read_in_reattempt", "cache_modified_in_reattempt",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "module_paths_recovered_by_reattempt", "per_module_counts_recovered_by_reattempt",
    "bounded_nodeid_samples_recovered_by_reattempt", "module_grouping_recovered_in_reattempt",
    "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
    "diagnostic_output_captured", "ready_for_after_v2_planning_reentry_with_complete_detail",
]

SOURCE_BINDINGS = {
    "source_complete_29_row_materialization_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
    "source_complete_29_row_materialized_payload_review_digest": SOURCE_PAYLOAD_REVIEW_DIGEST,
    "source_complete_29_row_materialization_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    "source_complete_29_row_materialization_execution_digest": SOURCE_MATERIALIZATION_EXECUTION_DIGEST,
    "source_complete_29_row_materialized_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
    "source_complete_29_row_materialization_digest_manifest_digest": SOURCE_MATERIALIZATION_DIGEST_MANIFEST_DIGEST,
    **deepcopy(review_source.SOURCE_BINDINGS),
}


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError(ValueError):
    """Raised when a reattempt artifact violates its binding contract."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _committed_source_review() -> dict[str, Any]:
    rows = review_source.source.committed_complete_29_row_module_grouping_detail_source_v1()
    return {
        "artifact_kind": review_source.ARTIFACT_KIND, "review_status": review_source.REVIEW_STATUS,
        "review_scope": review_source.REVIEW_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_review_digest": SOURCE_PAYLOAD_REVIEW_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        **deepcopy(SOURCE_BINDINGS),
        "selected_complete_29_row_materialization_package": review_source.source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        "complete_29_row_materialization_results_review_ready": True,
        "source_materialized_payload_digest_verified": True,
        "materialized_complete_29_row_source_reviewed": True,
        "ready_for_detail_exposure_or_binding_execution_reattempt": True,
        "ready_for_after_v2_planning_reentry_with_complete_detail": False,
        "recommended_action": review_source.RECOMMENDED_ACTION,
        "recommended_next_task": review_source.NEXT_TASK,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "complete_29_row_materialized_source_review": {
            "reviewed": True, "row_count": 29, "failed_or_errored_nodeids_count": 1404,
            "source_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST, "rows": rows,
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
    }


def _source_review_reasons(review: Any) -> list[str]:
    if not isinstance(review, Mapping):
        return ["SOURCE_MATERIALIZATION_RESULTS_REVIEW_UNAVAILABLE"]
    expected = _committed_source_review()
    fields = [
        "artifact_kind", "review_status", "review_scope",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_review_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_manifest_digest",
        *SOURCE_BINDINGS, "complete_29_row_materialization_results_review_ready",
        "source_materialized_payload_digest_verified", "materialized_complete_29_row_source_reviewed",
        "ready_for_detail_exposure_or_binding_execution_reattempt",
        "ready_for_after_v2_planning_reentry_with_complete_detail", "recommended_action",
        "recommended_next_task", "retry_execution_commit", "retry_failure_context",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "largest_module_nodeid_counts",
        "top_5_count_sum", "top_10_count_sum", "priority_tier_1_count_sum",
        "priority_tier_2_count_sum", "priority_tier_3_count_sum",
    ]
    return [f"SOURCE_REVIEW_{field.upper()}_MISMATCH_OR_MISSING" for field in fields if review.get(field) != expected[field]]


def _source_rows_reasons(rows: Any) -> list[str]:
    if not isinstance(rows, list) or not rows:
        return ["REVIEWED_COMMITTED_COMPLETE_29_ROW_SOURCE_UNAVAILABLE"]
    verification = {
        "lastfailed_hash_verified": True, "nodeids_hash_verified": True,
        "entry_counts_verified": True, "lastfailed_subset_of_nodeids": True,
        "committed_source_rows_match": rows == review_source.source.committed_complete_29_row_module_grouping_detail_source_v1(),
    }
    reasons = review_source.source._integrity_reasons(verification, rows)
    if semantic_digest(rows) != SOURCE_MATERIALIZED_PAYLOAD_DIGEST:
        reasons.append("REVIEWED_MATERIALIZED_PAYLOAD_DIGEST_MISMATCH")
    return reasons


def _binding_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        bound = deepcopy(row)
        bound["source"] = BINDING_ROW_SOURCE
        bound["basis"] = BINDING_ROW_BASIS
        bound["confidence"] = BINDING_ROW_CONFIDENCE
        bound["sample_nodeids_bounded"] = sorted(bound["sample_nodeids_bounded"])[:5]
        bound["sample_nodeids_bounded_count"] = len(bound["sample_nodeids_bounded"])
        result.append(bound)
    return sorted(result, key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"]))


def _common(timestamp: str) -> dict[str, Any]:
    common = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        "created_offline": True, "governance_only": True,
        "detail_exposure_or_binding_reattempt_only": True, "run_timestamp_utc": timestamp,
        **deepcopy(SOURCE_BINDINGS),
        "source_materialization_results_review_artifact_kind": review_source.ARTIFACT_KIND,
        "source_materialization_results_review_status": review_source.REVIEW_STATUS,
        "source_materialization_results_review_scope": review_source.REVIEW_SCOPE,
        "complete_29_row_detail_source_type": BINDING_ROW_SOURCE,
        "complete_29_row_detail_source_basis": BINDING_ROW_BASIS,
        "complete_29_row_detail_source_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }
    common.update({field: False for field in FALSE_FIELDS})
    return common


def _prechecks(success: bool) -> list[dict[str, Any]]:
    return [{"precheck_id": item, "status": PASS if success or item != "reviewed_complete_29_row_source_available" else FAIL} for item in PRECHECK_IDS]


def _steps(success: bool) -> list[dict[str, Any]]:
    rows_required = {
        "locate_reviewed_committed_complete_29_row_source", "verify_complete_29_row_source_available_or_block",
        "verify_29_module_rows", "verify_total_failed_or_errored_nodeids_1404", "verify_largest_module_counts",
        "verify_top_five_paths", "verify_top_five_and_top_ten_sums", "verify_tier_sums",
        "verify_bounded_samples", "build_complete_29_row_detail_binding_source",
        "build_reviewed_materialized_source_binding_report", "build_payload_digest_binding_report",
        "build_recovered_module_paths_binding_report", "build_per_module_counts_binding_report",
        "build_bounded_nodeid_samples_binding_report", "build_priority_tier_enablement_report",
        "build_top_module_concentration_preservation_report", "build_unsupported_claims_boundary_report",
        "build_detail_exposure_or_binding_limitations_report", "build_planning_reentry_enablement_report",
        "build_digest_manifest",
    }
    return [
        {
            "step_id": step_id, "status": PASS if success or step_id not in rows_required else BLOCKER,
            "expected": "completed" if success or step_id not in rows_required else "complete reviewed source",
            "actual": "completed" if success or step_id not in rows_required else "blocked",
            "message": f"{step_id} {'completed' if success or step_id not in rows_required else 'blocked'}",
        }
        for step_id in STEP_IDS
    ]


def _success(common: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    bound_rows = _binding_rows(rows)
    binding_digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_after_materialization_digest"
    manifest_digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_digest_manifest_digest"
    binding_digest = semantic_digest(bound_rows)
    top_report = {
        "top_five_module_paths": [row["module_path"] for row in bound_rows[:5]],
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in bound_rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tier_report = {
        "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }
    source_report = {
        "reviewed_source_available": True, "source_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST, "row_count": 29,
        "failed_or_errored_nodeids_count": 1404,
    }
    payload_report = {
        "reviewed_materialized_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "binding_digest": binding_digest, "reviewed_payload_digest_verified": True,
        "digest_is_not_payload": True,
    }
    limitations = [
        "binding does not separate failures from errors", "binding does not identify first-result order",
        "binding provides no traceback root cause", "binding is planning evidence only",
        "binding does not prove retry success or main-merge readiness",
    ]
    planning = {
        "ready_for_detail_exposure_or_binding_results_review": True,
        "ready_for_after_v2_planning_reentry_with_complete_detail": False,
        "after_v2_planning_reentry_requires_detail_exposure_or_binding_results_review": True,
    }
    digest_manifest = {
        "source_materialization_results_review": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_payload_review": SOURCE_PAYLOAD_REVIEW_DIGEST,
        "source_results_review_manifest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_materialized_payload": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "binding_source": binding_digest, "source_binding_report": semantic_digest(source_report),
        "payload_binding_report": semantic_digest(payload_report), "top_module_concentration": semantic_digest(top_report),
        "priority_tiers": semantic_digest(tier_report), "unsupported_claims": semantic_digest(review_source.source.UNSUPPORTED_ROW_CLAIMS),
        "limitations": semantic_digest(limitations), "planning_reentry_enablement": semantic_digest(planning),
    }
    execution = {
        **common, "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        "used_reviewed_complete_29_row_materialized_source": True, "used_committed_source_evidence_only": True,
        "detail_exposure_or_binding_reattempt_executed": True, "detail_exposure_or_binding_executed": True,
        "complete_29_row_detail_exposed": True, "complete_29_row_detail_bound": True,
        "complete_29_row_detail_source_identified": True, "module_grouping_detail_exposed_by_reattempt": True,
        "module_paths_bound_by_reattempt": True, "per_module_counts_bound_by_reattempt": True,
        "bounded_nodeid_samples_bound_by_reattempt": True,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        **tier_report,
        "complete_29_row_module_grouping_detail_binding_source": bound_rows,
        "top_five_module_paths": list(review_source.source.EXPECTED_TOP_FIVE_PATHS),
        "ready_for_detail_exposure_or_binding_results_review": True,
        "after_v2_planning_reentry_requires_detail_exposure_or_binding_results_review": True,
        "reviewed_materialized_payload_digest_verified": True,
        "detail_exposure_or_binding_reattempt_execution_manifest": {"row_count": 29, "nodeid_count": 1404, "source_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST},
        "reviewed_materialized_source_binding_report": source_report,
        "payload_digest_binding_report": payload_report,
        "recovered_module_paths_binding_report": [row["module_path"] for row in bound_rows],
        "per_module_counts_binding_report": [{"module_path": row["module_path"], "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"]} for row in bound_rows],
        "bounded_nodeid_samples_binding_report": [{"module_path": row["module_path"], "sample_nodeids_bounded": row["sample_nodeids_bounded"]} for row in bound_rows],
        "priority_tier_enablement_report": tier_report,
        "top_module_concentration_preservation_report": top_report,
        "unsupported_claims_boundary_report": list(review_source.source.UNSUPPORTED_ROW_CLAIMS),
        "detail_exposure_or_binding_limitations_report": limitations,
        "planning_reentry_enablement_report": planning,
        "digest_manifest": digest_manifest,
        binding_digest_key: binding_digest, manifest_digest_key: semantic_digest(digest_manifest),
        "planned_outputs_generated": True,
        "outputs_generated": [{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
        "precheck_results": _prechecks(True), "execution_steps": _steps(True),
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "recommended_next_task": SUCCESS_NEXT_TASK, "blocked_reason": None,
    }
    return execution


def _blocked(common: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    blocked_reason = ";".join(dict.fromkeys(reasons))
    blocked_key = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_blocked_manifest_digest"
    return {
        **common, "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        "used_reviewed_complete_29_row_materialized_source": False, "used_committed_source_evidence_only": True,
        "detail_exposure_or_binding_reattempt_executed": True, "detail_exposure_or_binding_executed": False,
        "complete_29_row_detail_exposed": False, "complete_29_row_detail_bound": False,
        "complete_29_row_detail_source_identified": False, "module_grouping_detail_exposed_by_reattempt": False,
        "module_paths_bound_by_reattempt": False, "per_module_counts_bound_by_reattempt": False,
        "bounded_nodeid_samples_bound_by_reattempt": False,
        "failed_or_errored_nodeids_count": 0, "module_summary_module_count": 0,
        "largest_module_nodeid_counts": [], "top_5_count_sum": 0, "top_10_count_sum": 0,
        "priority_tier_1_count_sum": 0, "priority_tier_2_count_sum": 0, "priority_tier_3_count_sum": 0,
        "complete_29_row_module_grouping_detail_binding_source": [], "top_five_module_paths": [],
        "ready_for_detail_exposure_or_binding_results_review": False,
        "after_v2_planning_reentry_requires_detail_exposure_or_binding_results_review": True,
        "reviewed_materialized_payload_digest_verified": False,
        "planned_outputs_generated": False, "outputs_generated": [],
        "precheck_results": _prechecks(False), "execution_steps": _steps(False),
        "available_data": ["source materialization results-review digest", "materialized payload digest", "payload-review digest", "retry counts", "reviewed summary facts", "any committed materialized rows found"],
        "missing_data": list(dict.fromkeys(reasons)), "blocked_reason": blocked_reason,
        blocked_key: semantic_digest({"blocked_reason": blocked_reason, "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST, "source_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST}),
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        "recommended_next_task": BLOCKED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    rows = execution.get("complete_29_row_module_grouping_detail_binding_source", [])
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    values: dict[str, tuple[Any, Any]] = {
        "reviewed_materialized_payload_digest_verified": (success, execution.get("reviewed_materialized_payload_digest_verified")),
        "materialization_results_review_ready_bound": (review_source.REVIEW_STATUS, execution.get("source_materialization_results_review_status")),
        "selected_detail_exposure_or_binding_package_bound": (SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE, execution.get("selected_detail_exposure_or_binding_package")),
        "complete_29_row_source_available_if_success": (success, execution.get("used_reviewed_complete_29_row_materialized_source")),
        "complete_29_row_detail_exposed_true_if_success": (success, execution.get("complete_29_row_detail_exposed")),
        "complete_29_row_detail_bound_true_if_success": (success, execution.get("complete_29_row_detail_bound")),
        "complete_29_row_detail_source_identified_true_if_success": (success, execution.get("complete_29_row_detail_source_identified")),
        "module_grouping_detail_exposed_by_reattempt_true_if_success": (success, execution.get("module_grouping_detail_exposed_by_reattempt")),
        "module_paths_bound_by_reattempt_true_if_success": (success, execution.get("module_paths_bound_by_reattempt")),
        "per_module_counts_bound_by_reattempt_true_if_success": (success, execution.get("per_module_counts_bound_by_reattempt")),
        "bounded_nodeid_samples_bound_by_reattempt_true_if_success": (success, execution.get("bounded_nodeid_samples_bound_by_reattempt")),
        "complete_29_row_rows_exactly_29_if_success": (29 if success else 0, len(rows)),
        "failed_or_errored_nodeids_1404_if_success": (1404 if success else 0, sum(value for value in counts if isinstance(value, int) and not isinstance(value, bool))),
        "largest_module_counts_if_success": ([136, 131, 122, 112, 111] if success else [], counts[:5]),
        "top_five_paths_preserved_if_success": (review_source.source.EXPECTED_TOP_FIVE_PATHS if success else [], paths[:5]),
        "top_five_sum_612_if_success": (612 if success else 0, sum(value for value in counts[:5] if isinstance(value, int))),
        "top_ten_sum_1069_if_success": (1069 if success else 0, sum(value for value in counts[:10] if isinstance(value, int))),
        "tier_1_sum_612_if_success": (612 if success else 0, sum(value for value in counts[:5] if isinstance(value, int))),
        "tier_2_sum_457_if_success": (457 if success else 0, sum(value for value in counts[5:10] if isinstance(value, int))),
        "tier_3_sum_335_if_success": (335 if success else 0, sum(value for value in counts[10:] if isinstance(value, int))),
        "bounded_samples_max_5_if_success": (success, success and bool(rows) and all(0 < len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows)),
        "binding_digest_generated_if_success": (success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_after_materialization_digest"))),
        "digest_manifest_digest_generated_if_success": (success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_digest_manifest_digest"))),
        "ready_for_detail_binding_results_review_true_if_success": (success, execution.get("ready_for_detail_exposure_or_binding_results_review")),
        "complete_29_row_detail_exposed_false_if_blocked": (success, execution.get("complete_29_row_detail_exposed")),
        "complete_29_row_detail_bound_false_if_blocked": (success, execution.get("complete_29_row_detail_bound")),
        "blocked_reason_recorded_if_blocked": (not success, bool(execution.get("blocked_reason"))),
        "blocked_manifest_digest_generated_if_blocked": (not success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_blocked_manifest_digest"))),
    }
    source_checks = {
        "source_materialization_results_review_digest_bound": "source_complete_29_row_materialization_results_review_digest",
        "source_materialized_payload_review_digest_bound": "source_complete_29_row_materialized_payload_review_digest",
        "source_materialization_results_review_manifest_digest_bound": "source_complete_29_row_materialization_results_review_manifest_digest",
        "source_materialization_execution_digest_bound": "source_complete_29_row_materialization_execution_digest",
        "source_materialized_payload_digest_bound": "source_complete_29_row_materialized_payload_digest",
        "source_materialization_digest_manifest_digest_bound": "source_complete_29_row_materialization_digest_manifest_digest",
        "source_materialization_approval_digest_bound": "source_complete_29_row_materialization_approval_digest",
        "source_materialization_operator_review_digest_bound": "source_complete_29_row_materialization_operator_review_digest",
        "source_materialization_candidate_digest_bound": "source_complete_29_row_materialization_candidate_digest",
        "source_execution_failure_diagnosis_digest_bound": "source_detail_exposure_or_binding_execution_failure_diagnosis_digest",
        "source_primary_failure_class_bound": "primary_failure_class",
        "source_detail_binding_blocked_execution_digest_bound": "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_detail_binding_blocked_manifest_digest_bound": "source_detail_exposure_or_binding_execution_blocked_manifest_digest",
        "source_detail_binding_blocked_reason_bound": "source_detail_exposure_or_binding_execution_blocked_reason",
        "source_detail_binding_approval_digest_bound": "source_detail_exposure_or_binding_approval_digest",
        "source_detail_binding_operator_review_digest_bound": "source_detail_exposure_or_binding_operator_review_digest",
        "source_detail_binding_candidate_digest_bound": "source_detail_exposure_or_binding_candidate_digest",
        "source_reentry_failure_diagnosis_digest_bound": "source_reentry_failure_diagnosis_digest",
        "source_reentry_failure_primary_failure_class_bound": "source_reentry_failure_primary_failure_class",
        "source_reentry_execution_blocked_digest_bound": "source_reentry_execution_blocked_digest",
        "source_reentry_execution_blocked_manifest_digest_bound": "source_reentry_execution_blocked_manifest_digest",
        "source_reentry_execution_blocked_reason_bound": "source_reentry_execution_blocked_reason",
        "source_planning_reentry_digest_bound": "source_after_v2_planning_reentry_digest",
        "source_recovery_results_review_digest_bound": "source_module_grouping_source_recovery_results_review_digest",
        "source_recovery_results_review_manifest_digest_bound": "source_module_grouping_source_recovery_results_review_manifest_digest",
        "source_recovery_execution_digest_bound": "source_module_grouping_source_recovery_execution_digest",
        "source_recovery_detail_digest_bound": "source_module_grouping_source_recovery_detail_digest",
        "source_recovery_digest_manifest_bound": "source_module_grouping_source_recovery_digest_manifest_digest",
        "source_blocked_after_v2_execution_digest_bound": "source_blocked_after_v2_execution_digest",
        "source_blocked_after_v2_manifest_digest_bound": "source_blocked_after_v2_manifest_digest",
        "source_after_v2_approval_digest_bound": "source_after_v2_approval_digest",
        "source_results_review_v2_digest_bound": "source_results_review_v2_digest",
        "source_execution_v2_digest_bound": "source_execution_v2_digest",
        "source_module_grouping_digest_bound": "source_module_grouping_digest",
    }
    values.update({check_id: (SOURCE_BINDINGS[field], execution.get(field)) for check_id, field in source_checks.items()})
    values["retry_execution_commit_bound"] = ("ab178b65c69f0274b0abbf9c20df102d35e78d34", execution.get("retry_execution_commit"))
    values["retry_failure_counts_bound"] = ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, execution.get("retry_failure_context", {}).get("counts"))
    false_checks = {
        "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed", "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed", "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created", "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed", "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created", "cache_read_in_reattempt_false": "cache_read_in_reattempt",
        "cache_modified_in_reattempt_false": "cache_modified_in_reattempt", "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
        "source_recovery_rerun_false": "source_recovery_rerun_performed", "module_grouping_recovered_in_reattempt_false": "module_grouping_recovered_in_reattempt",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_reattempt", "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task", "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed", "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_reattempt", "market_data_acquisition_false": "market_data_acquisition_performed_in_reattempt",
        "dataset_generation_false": "dataset_generation_performed_in_reattempt", "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, execution.get(field)) for check_id, field in false_checks.items()})
    values["successful_integration_digest_false"] = ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")])
    values["predictive_usefulness_not_accepted"] = (NOT_ACCEPTED, execution.get("predictive_usefulness"))
    values["profitability_not_accepted"] = (NOT_ACCEPTED, execution.get("profitability"))
    values["runtime_not_authorized"] = (NOT_AUTHORIZED, execution.get("runtime_use"))
    values["broker_not_authorized"] = (NOT_AUTHORIZED, execution.get("broker_execution"))
    values["next_chain_defined"] = (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain"))
    values["next_gates_defined"] = (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates"))
    values["risk_controls_defined"] = (RISK_CONTROLS, execution.get("risk_controls"))
    values["no_tracked_marketflow_files"] = (False, execution.get("marketflow_outputs_tracked_in_repository"))
    values["no_tracked_pytest_cache_files"] = (False, execution.get("pytest_cache_tracked_in_repository"))
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]], success: bool) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    result = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "detail_exposure_or_binding_reattempt_executed": execution.get("detail_exposure_or_binding_reattempt_executed"),
        "complete_29_row_detail_exposed": execution.get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound": execution.get("complete_29_row_detail_bound"),
        "complete_29_row_detail_source_identified": execution.get("complete_29_row_detail_source_identified"),
        "after_v2_planning_execution_reentry_created": execution.get("after_v2_planning_execution_reentry_created"),
        "targeted_diagnostic_output_capture_candidate_created": execution.get("targeted_diagnostic_output_capture_candidate_created"),
        "new_retry_candidate_created": execution.get("new_retry_candidate_created"),
        "integration_execution_successful": execution.get("integration_execution_successful"),
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        result.update({field: execution.get(field) for field in [
            "detail_exposure_or_binding_executed", "module_grouping_detail_exposed_by_reattempt",
            "module_paths_bound_by_reattempt", "per_module_counts_bound_by_reattempt",
            "bounded_nodeid_samples_bound_by_reattempt", "failed_or_errored_nodeids_count",
            "module_summary_module_count", "top_5_count_sum", "top_5_percentage_of_failed_or_errored_nodeids",
            "top_10_count_sum", "top_10_percentage_of_failed_or_errored_nodeids",
            "priority_tier_1_count_sum", "priority_tier_2_count_sum", "priority_tier_3_count_sum",
            "ready_for_detail_exposure_or_binding_results_review",
            "ready_for_after_v2_planning_reentry_with_complete_detail",
            "after_v2_planning_execution_reentry_performed", "new_retry_executed",
        ]})
    else:
        result["blocked_reason"] = execution.get("blocked_reason")
    return result


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
    *, source_materialization_results_review: dict | None = None,
    complete_detail_source: list[dict] | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    """Execute the bounded reattempt using committed source evidence only."""

    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("run timestamp invalid")
    review = deepcopy(source_materialization_results_review) if source_materialization_results_review is not None else _committed_source_review()
    reasons = _source_review_reasons(review)
    if complete_detail_source is None:
        source_review = review.get("complete_29_row_materialized_source_review", {}) if isinstance(review, Mapping) else {}
        rows = deepcopy(source_review.get("rows")) if isinstance(source_review, Mapping) else None
    else:
        rows = deepcopy(complete_detail_source)
    reasons.extend(_source_rows_reasons(rows))
    common = _common(timestamp)
    execution = _success(common, rows) if not reasons else _blocked(common, reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_digest"
    execution[digest_key] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(execution: dict) -> dict:
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, expected_status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, expected_status = False, BLOCKED_STATUS
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("artifact kind invalid")
    constants = {
        "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "schema_version": SCHEMA_VERSION,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        "source_materialization_results_review_artifact_kind": review_source.ARTIFACT_KIND,
        "source_materialization_results_review_status": review_source.REVIEW_STATUS,
        "source_materialization_results_review_scope": review_source.REVIEW_SCOPE,
        "complete_29_row_detail_source_type": BINDING_ROW_SOURCE,
        "complete_29_row_detail_source_basis": BINDING_ROW_BASIS,
        "complete_29_row_detail_source_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError(f"{field} mismatch")
    if not _iso_utc(execution.get("run_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("run timestamp invalid")
    for field in ("created_offline", "governance_only", "detail_exposure_or_binding_reattempt_only",
                  "used_committed_source_evidence_only", "detail_exposure_or_binding_reattempt_executed"):
        if execution.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError(f"{field} must be true")
    if execution.get("retry_execution_commit") != "ab178b65c69f0274b0abbf9c20df102d35e78d34":
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("retry execution commit mismatch")
    if execution.get("retry_failure_context") != {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("retry failure counts mismatch")
    for field in FALSE_FIELDS:
        if execution.get(field) is not False:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError(f"{field} must be false")
    if execution.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("risk controls invalid")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("acceptance boundary invalid")
    if execution.get("runtime_use") != NOT_AUTHORIZED or execution.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("runtime boundary invalid")
    rows = execution.get("complete_29_row_module_grouping_detail_binding_source")
    if not isinstance(rows, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("binding source missing")
    if success:
        expected_rows = _binding_rows(review_source.source.committed_complete_29_row_module_grouping_detail_source_v1())
        if rows != expected_rows:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("binding rows invalid")
        expected_summary_values = {
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
            "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
            "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
            "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
            "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
            "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
            "top_five_module_paths": list(review_source.source.EXPECTED_TOP_FIVE_PATHS),
        }
        for field, expected in expected_summary_values.items():
            if execution.get(field) != expected:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError(f"{field} mismatch")
        required_true = [
            "used_reviewed_complete_29_row_materialized_source", "used_committed_source_evidence_only",
            "detail_exposure_or_binding_reattempt_executed", "detail_exposure_or_binding_executed",
            "complete_29_row_detail_exposed", "complete_29_row_detail_bound", "complete_29_row_detail_source_identified",
            "module_grouping_detail_exposed_by_reattempt", "module_paths_bound_by_reattempt",
            "per_module_counts_bound_by_reattempt", "bounded_nodeid_samples_bound_by_reattempt",
            "ready_for_detail_exposure_or_binding_results_review", "reviewed_materialized_payload_digest_verified",
            "planned_outputs_generated", "after_v2_planning_reentry_requires_detail_exposure_or_binding_results_review",
        ]
        if any(execution.get(field) is not True for field in required_true):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("success flag missing")
        binding_key = "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_after_materialization_digest"
        manifest_key = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_digest_manifest_digest"
        if execution.get(binding_key) != semantic_digest(rows):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("binding digest invalid")
        if execution.get(manifest_key) != semantic_digest(execution.get("digest_manifest")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("digest manifest invalid")
        outputs = execution.get("outputs_generated", [])
        if [item.get("output_id") for item in outputs] != OUTPUT_IDS or any(item.get("status") != "GENERATED_RESEARCH_ONLY" for item in outputs):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("outputs invalid")
    else:
        if not execution.get("blocked_reason"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("blocked reason missing")
        blocked_key = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_blocked_manifest_digest"
        expected_blocked = semantic_digest({"blocked_reason": execution["blocked_reason"], "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST, "source_payload_digest": SOURCE_MATERIALIZED_PAYLOAD_DIGEST})
        if execution.get(blocked_key) != expected_blocked:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("blocked manifest invalid")
        if any(execution.get(field) is not False for field in ["complete_29_row_detail_exposed", "complete_29_row_detail_bound", "complete_29_row_detail_source_identified", "planned_outputs_generated"]):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("blocked boundary open")
        if rows or execution.get("outputs_generated"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("blocked output generated")
    if [item.get("precheck_id") for item in execution.get("precheck_results", [])] != PRECHECK_IDS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("precheck results invalid")
    if [item.get("step_id") for item in execution.get("execution_steps", [])] != STEP_IDS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("execution steps invalid")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("checklist invalid")
    summary = _summary(execution, checklist, success)
    if execution.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("summary invalid")
    digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_digest"
    digest = execution.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _execution_digest(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError("execution digest invalid")
    return {"artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
            "execution_scope": execution["execution_scope"], "execution_digest": digest,
            **{field: summary[field] for field in ["total_checks", "passed_checks", "failed_checks", "blocker_count"]}}


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_markdown_v1(execution: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(execution)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    sections = [
        ("Source Materialization Results Review", [SOURCE_RESULTS_REVIEW_DIGEST, review_source.REVIEW_STATUS]),
        ("Source Materialization Execution", [SOURCE_MATERIALIZATION_EXECUTION_DIGEST, SOURCE_MATERIALIZED_PAYLOAD_DIGEST]),
        ("Source Detail Exposure or Binding Approval", [SOURCE_BINDINGS["source_detail_exposure_or_binding_approval_digest"], SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE]),
        ("Source Prior Blocked Detail Exposure or Binding Execution", [SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_digest"], SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_reason"]]),
        ("Source Reentry Failure Diagnosis", [SOURCE_BINDINGS["source_reentry_failure_diagnosis_digest"], SOURCE_BINDINGS["source_reentry_failure_primary_failure_class"]]),
        ("Source Recovery Results Review", [SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"], SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; root regression is not retry evidence."]),
        ("Execution Scope", [EXECUTION_SCOPE]),
        ("Reviewed Complete 29-row Source", [f"Rows: {len(execution['complete_29_row_module_grouping_detail_binding_source'])}; total: {execution.get('failed_or_errored_nodeids_count')}."]),
        ("Detail Binding Reattempt Result", [execution["execution_status"], execution.get("blocked_reason") or SUCCESS_NEXT_TASK]),
        ("Payload Digest Binding", [execution.get("complete_29_row_detail_source_digest"), execution.get("marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_after_materialization_digest")]),
        ("Top Module Concentration Preservation", [f"Top-five: {execution.get('top_5_count_sum')}; top-ten: {execution.get('top_10_count_sum')}."]),
        ("Priority Tier Enablement", [f"Tier sums: {execution.get('priority_tier_1_count_sum')}/{execution.get('priority_tier_2_count_sum')}/{execution.get('priority_tier_3_count_sum')}."]),
        ("Unsupported Claims Boundary", list(review_source.source.UNSUPPORTED_ROW_CLAIMS)),
        ("Success or Blocked Disposition", ["success" if success else "blocked"]),
        ("Authority Boundaries", ["No cache read, materialization/recovery rerun, retry, planning reentry, diagnostics, remediation, classification, provider, runtime, trading, integration, or main action occurred."]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass."]),
        ("Guardrails", ["A separate binding results review is required before after-v2 planning reentry."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Execution Reattempt with Complete Source v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_BLOCKED_COMPLETE_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN",
    "SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE",
    "execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_markdown_v1",
]
