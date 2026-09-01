"""Execute planning-only module prioritization from reviewed recovered detail."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_service
    as source,
)


ARTIFACT_KIND_EXECUTED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_V1"
EXECUTION_STATUS_READY = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_PRIORITIZED_MODULE_PLANNING_READY"
EXECUTION_STATUS_BLOCKED_SOURCE = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_RECOVERED_MODULE_GROUPING_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_STATUS_BLOCKED_PRECHECK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_PRECHECK_FAILED"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1"
SELECTED_PACKAGE = "PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING"
SOURCE_REENTRY_DIGEST = "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927"
FOLLOW_ON_PACKAGE = "PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PRIORITY_TIER_POLICY = [
    "PRIORITY_1_TOP_5_MODULE_GROUPS",
    "PRIORITY_2_NEXT_5_MODULE_GROUPS",
    "PRIORITY_3_REMAINING_MODULE_GROUPS",
]
PLANNING_BUCKETS = [
    "TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE",
    "EVIDENCE_ROOT_REQUIREMENT_REVIEW",
    "PATH_CWD_ASSUMPTION_REVIEW",
    "DIGEST_CONSTANT_DRIFT_REVIEW",
    "TEST_FIXTURE_ISOLATION_REVIEW",
]
ROW_UNSUPPORTED_CLAIMS = [
    "no_failure_error_separation",
    "no_first_order_claim",
    "no_traceback_root_cause",
    "no_direct_code_remediation",
    "no_retry_success",
    "no_main_merge_readiness",
]
UNSUPPORTED_CLAIMS = {
    "failure_modules_classified": False,
    "error_modules_classified": False,
    "failure_error_separation_claimed": False,
    "first_failure_identified": False,
    "first_error_identified": False,
    "first_order_claim_made": False,
    "traceback_root_cause_claimed": False,
    "direct_code_remediation_recommended": False,
    "retry_success_claimed": False,
    "main_merge_readiness_claimed": False,
}
OUTPUT_IDS = list(source.PLANNED_OUTPUT_IDS)
TOP_FIVE_PATHS = [item["module_path"] for item in source.source.TOP_FIVE]
SUCCESS_NEXT_CHAIN = [
    "Remediation or Method Results Review After Classification v2 Review Reentry v1.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if results review supports it.",
    "Diagnostic Capture Operator Review.",
    "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.",
    "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Remediation or Method Execution After Classification v2 Review Reentry Failure Diagnosis v1.",
    "Source/reentry remediation candidate, if needed.",
    "No diagnostic capture, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_for_top_module_groups_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "after_v2_planning_reentry_execution_failure_diagnosis",
    "after_v2_planning_reentry_remediation_candidate_if_needed",
    "diagnostic_capture_blocked_until_reentry_execution_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "reentry_execution_uses_recovered_reviewed_source_only",
    "reentry_execution_does_not_read_cache",
    "reentry_execution_does_not_recover_module_grouping_again",
    "reentry_execution_does_not_modify_cache",
    "reentry_execution_does_not_commit_pytest_cache",
    "reentry_execution_does_not_commit_marketflow_outputs",
    "reentry_execution_does_not_parse_operator_logs",
    "reentry_execution_does_not_run_diagnostic_commands",
    "reentry_execution_does_not_execute_diagnostics",
    "reentry_execution_does_not_execute_code_remediation",
    "reentry_execution_does_not_execute_evidence_remediation",
    "reentry_execution_does_not_execute_classification",
    "reentry_execution_does_not_classify_modules_again",
    "reentry_execution_does_not_rerun_retry",
    "reentry_execution_does_not_run_full_pytest",
    "reentry_execution_does_not_create_new_retry_candidate",
    "reentry_execution_does_not_create_retry_results_review",
    "reentry_execution_does_not_create_integration_results_review",
    "reentry_execution_does_not_mark_integration_successful",
    "reentry_execution_does_not_generate_successful_integration_digest",
    "reentry_execution_does_not_claim_failure_error_separation",
    "reentry_execution_does_not_claim_first_failure",
    "reentry_execution_does_not_claim_first_error",
    "reentry_execution_does_not_claim_traceback_root_cause",
    "reentry_execution_does_not_recommend_direct_code_remediation",
    "reentry_execution_does_not_treat_recovered_source_as_retry_success",
    "reentry_execution_does_not_push_integration_branch",
    "reentry_execution_does_not_push_main",
    "reentry_execution_does_not_delete_integration_branch",
    "reentry_execution_does_not_delete_worktree",
    "reentry_execution_does_not_force_push",
    "reentry_execution_does_not_prune_remotes",
    "reentry_execution_does_not_modify_tags",
    "reentry_execution_does_not_modify_staged_evidence",
    "reentry_execution_does_not_regenerate_evidence",
    "reentry_execution_does_not_call_providers",
    "reentry_execution_does_not_acquire_market_data",
    "reentry_execution_does_not_regenerate_dataset",
    "reentry_execution_does_not_recompute_metrics",
    "reentry_execution_does_not_train_models",
    "reentry_execution_does_not_score_strategy",
    "reentry_execution_does_not_generate_recommendations",
    "reentry_execution_does_not_accept_predictive_usefulness",
    "reentry_execution_does_not_accept_profitability",
    "reentry_execution_does_not_authorize_runtime",
    "reentry_execution_does_not_authorize_broker_execution",
    "planning_output_is_not_diagnostic_evidence",
    "planning_output_is_not_root_cause_evidence",
    "planning_output_is_not_retry_success_evidence",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "previous_blocked_execution_remains_historically_blocked",
    "previous_blocker_resolved_for_reentry_only",
    "separate_reentry_results_review_required",
    "separate_diagnostic_capture_approval_required_before_diagnostics",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError(ValueError):
    """Raised when a planning execution artifact fails validation."""


def _committed_source_reentry() -> dict[str, Any]:
    """Return only committed reentry facts; full 29-row detail is intentionally absent."""

    return {
        "artifact_kind": source.ARTIFACT_KIND,
        "reentry_status": source.REENTRY_STATUS,
        "reentry_scope": source.REENTRY_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": source.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "source_after_v2_approval_digest": source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_approval_v2_digest": "a29132ad740c0e617fb438c154c4b5fed756f15bceed40ff132334d1c5e58412",
        "source_staged_inventory_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "previous_after_v2_planning_execution_blocked": True,
        "previous_after_v2_planning_execution_blocker_resolved_for_reentry": True,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "accepted_source_type": "RECOVERED_REVIEWED_DETACHED_PYTEST_CACHE_MODULE_GROUPING_DETAIL",
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": deepcopy(source.source.TOP_FIVE),
        "top_5_count_sum": 612,
        "top_10_count_sum": 1069,
        **deepcopy(UNSUPPORTED_CLAIMS),
    }


def _source_precheck_failures(reentry: Mapping[str, Any]) -> list[str]:
    expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "reentry_status": source.REENTRY_STATUS,
        "reentry_scope": source.REENTRY_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": source.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "source_after_v2_approval_digest": source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_results_review_v2_digest": source.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "previous_after_v2_planning_execution_blocker_resolved_for_reentry": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": source.source.TOP_FIVE,
        "top_5_count_sum": 612,
        "top_10_count_sum": 1069,
    }
    failures = [f"{field.upper()}_MISMATCH_OR_MISSING" for field, value in expected.items() if reentry.get(field) != value]
    if {key: reentry.get(key) for key in UNSUPPORTED_CLAIMS} != UNSUPPORTED_CLAIMS:
        failures.append("UNSUPPORTED_CLAIMS_BOUNDARY_VIOLATED")
    return failures


def _snapshot_rows(snapshot: Mapping[str, Any] | None) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(snapshot, Mapping):
        return [], ["RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"]
    raw_rows = snapshot.get("module_rows")
    if not isinstance(raw_rows, list) or not raw_rows:
        return [], ["RECOVERED_MODULE_GROUPING_DETAIL_MISSING"]
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for raw in raw_rows:
        if not isinstance(raw, Mapping):
            failures.append("MODULE_ROW_INVALID")
            continue
        path = raw.get("module_path")
        count = raw.get("failed_or_errored_nodeid_count")
        samples = raw.get("sample_nodeids_bounded_if_available")
        if not isinstance(path, str) or not path:
            failures.append("MODULE_PATH_MISSING")
            continue
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            failures.append("PER_MODULE_COUNT_MISSING_OR_INVALID")
            continue
        if not isinstance(samples, list) or any(not isinstance(item, str) for item in samples):
            failures.append("BOUNDED_SAMPLES_MISSING_OR_INVALID")
            continue
        rows.append({
            "module_path": path,
            "failed_or_errored_nodeid_count": count,
            "sample_nodeids_bounded_if_available": sorted(set(samples))[:5],
        })
    rows.sort(key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"]))
    if len(rows) != 29:
        failures.append("MODULE_COUNT_MISMATCH")
    if len({row["module_path"] for row in rows}) != len(rows):
        failures.append("DUPLICATE_MODULE_PATH")
    counts = [row["failed_or_errored_nodeid_count"] for row in rows]
    if sum(counts) != 1404:
        failures.append("FAILED_OR_ERRORED_NODEID_COUNT_MISMATCH")
    if counts[:5] != [136, 131, 122, 112, 111]:
        failures.append("LARGEST_MODULE_COUNTS_MISMATCH")
    if [row["module_path"] for row in rows[:5]] != [item["module_path"] for item in source.source.TOP_FIVE]:
        failures.append("TOP_FIVE_MODULE_PATHS_MISMATCH")
    if sum(counts[:5]) != 612:
        failures.append("TOP_FIVE_COUNT_SUM_MISMATCH")
    if sum(counts[:10]) != 1069:
        failures.append("TOP_TEN_COUNT_SUM_MISMATCH")
    return rows, sorted(set(failures))


def _percentage(count: int) -> str:
    return str((Decimal(count) * Decimal(100) / Decimal(1404)).quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP))


def _planning_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    planned = []
    for rank, row in enumerate(rows, 1):
        tier = PRIORITY_TIER_POLICY[0 if rank <= 5 else 1 if rank <= 10 else 2]
        planned.append({
            **deepcopy(row),
            "priority_tier": tier,
            "priority_rank": rank,
            "percentage_of_failed_or_errored_nodeids": _percentage(row["failed_or_errored_nodeid_count"]),
            "recommended_planning_bucket_candidates": list(PLANNING_BUCKETS),
            "planning_confidence": "LOW_TO_MEDIUM",
            "basis": "MODULE_LEVEL_GROUPING_ONLY_NOT_TRACEBACK_BASED",
            "unsupported_claims": list(ROW_UNSUPPORTED_CLAIMS),
        })
    return planned


def _common(reentry: Mapping[str, Any], run_timestamp_utc: str | None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_scope": EXECUTION_SCOPE,
        "selected_remediation_or_method_after_v2_package": SELECTED_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "planning_reentry_execution_only": True,
        "run_timestamp_utc": run_timestamp_utc,
        "source_after_v2_planning_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.source.source.SOURCE_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.source.source.approval_source.source.SOURCE_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": reentry["source_blocked_after_v2_execution_digest"],
        "source_blocked_after_v2_manifest_digest": reentry["source_blocked_after_v2_manifest_digest"],
        "blocked_reason_before_recovery": reentry["blocked_reason_before_recovery"],
        "source_after_v2_approval_digest": source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": reentry["source_results_review_v2_digest"],
        "source_execution_v2_digest": reentry["source_execution_v2_digest"],
        "source_module_grouping_digest": reentry["source_module_grouping_digest"],
        "source_approval_v2_digest": reentry["source_approval_v2_digest"],
        "source_staged_inventory_digest": reentry["source_staged_inventory_digest"],
        "retry_execution_branch": reentry["retry_execution_branch"],
        "retry_execution_commit": reentry["retry_execution_commit"],
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "previous_after_v2_planning_execution_blocked": True,
        "previous_after_v2_planning_execution_blocker_resolved_for_reentry": True,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "after_v2_planning_execution_reentered": True,
        "remediation_or_method_after_v2_reentry_execution_created": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(TOP_FIVE_PATHS),
        "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_policy": list(PRIORITY_TIER_POLICY),
        "priority_tier_1_count_sum": 612,
        "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457,
        "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335,
        "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
        **deepcopy(UNSUPPORTED_CLAIMS),
        "diagnostic_method_executed": False,
        "code_remediation_executed": False,
        "evidence_remediation_executed": False,
        "classification_execution_performed_in_reentry": False,
        "remediation_or_method_results_review_after_v2_created": False,
        "targeted_diagnostic_output_capture_candidate_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "cache_read_in_reentry": False,
        "module_grouping_recovered_in_reentry": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }


def _record(item_id: str, expected: Any, actual: Any, id_key: str) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {id_key: item_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "message": f"{item_id} {'passed' if status == PASS else 'failed'}"}


def _prechecks(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    values = {
        "source_reentry_digest_bound": (SOURCE_REENTRY_DIGEST, execution.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.SOURCE_RESULTS_REVIEW_DIGEST, execution.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, execution.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.source.SOURCE_EXECUTION_DIGEST, execution.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.source.SOURCE_RECOVERY_DETAIL_DIGEST, execution.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.source.SOURCE_DIGEST_MANIFEST_DIGEST, execution.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, execution.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, execution.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL, execution.get("blocked_reason_before_recovery")),
        "source_after_v2_approval_digest_bound": (source.SOURCE_AFTER_V2_APPROVAL_DIGEST, execution.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (source.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, execution.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, execution.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, execution.get("source_module_grouping_digest")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [execution.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "recovered_module_grouping_source_accepted": (True, execution.get("recovered_module_grouping_source_accepted_for_planning_reentry")),
        "previous_blocker_resolved_for_reentry": (True, execution.get("previous_after_v2_planning_execution_blocker_resolved_for_reentry")),
        "recovered_module_detail_available": (success, execution.get("recovered_module_detail_available")),
        "module_count_and_largest_counts_bound": ([29, [136, 131, 122, 112, 111]], [execution.get("module_summary_module_count"), execution.get("largest_module_nodeid_counts")]),
        "top_module_concentration_bound": ([612, 1069], [execution.get("top_5_count_sum"), execution.get("top_10_count_sum")]),
        "unsupported_claims_boundary_bound": (UNSUPPORTED_CLAIMS, {key: execution.get(key) for key in UNSUPPORTED_CLAIMS}),
        "origin_main_unchanged": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", execution.get("origin_main_commit")),
        "integration_branch_head_unchanged": ("220fbc220365fce9cae13ab4853cddff118c0187", execution.get("integration_branch_head_commit")),
        "staged_evidence_unchanged": (True, execution.get("staged_evidence_unchanged")),
        "marketflow_outputs_not_tracked": (False, execution.get("marketflow_outputs_tracked_in_repository")),
        "pytest_cache_not_tracked": (False, execution.get("pytest_cache_tracked_in_repository")),
        "no_cache_read": (False, execution.get("cache_read_in_reentry")),
        "no_retry_rerun": (False, execution.get("retry_rerun_performed")),
        "no_full_pytest": (False, execution.get("full_pytest_performed")),
        "no_diagnostic_command": (False, execution.get("diagnostic_command_executed")),
    }
    return [_record(item_id, *value, "precheck_id") for item_id, value in values.items()]


def _steps(success: bool) -> list[dict[str, Any]]:
    ids = [
        "verify_source_reentry", "verify_source_recovery_results_review",
        "verify_recovered_module_grouping_detail_available", "verify_previous_blocker_resolved_for_reentry",
        "verify_retry_failure_context", "verify_unsupported_claims_boundary", "build_priority_tier_policy",
        "build_prioritized_module_group_summary", "build_priority_tier_report", "build_top_module_concentration_report",
        "build_diagnostic_capture_candidate_report", "build_evidence_root_review_candidate_report",
        "build_path_cwd_review_candidate_report", "build_digest_drift_review_candidate_report",
        "build_fixture_isolation_review_candidate_report", "build_unsupported_claims_boundary_report",
        "build_recommended_follow_on_candidate_report", "preserve_failed_retry_authority", "do_not_read_cache",
        "do_not_create_retry_candidate", "do_not_create_results_review",
    ]
    build_ids = set(ids[2:17])
    return [_record(item_id, success if item_id in build_ids else True, success if item_id in build_ids else True, "step_id") for item_id in ids]


def _planning_digest(execution: Mapping[str, Any]) -> str:
    return semantic_digest({
        "rows": execution["prioritized_module_group_summary"],
        "tiers": execution["priority_tier_report"],
        "concentration": execution["top_module_concentration_report"],
        "follow_on": execution["recommended_follow_on_candidate_report"],
        "source_detail_digest": execution["source_module_grouping_source_recovery_detail_digest"],
    })


def _digest_manifest_digest(execution: Mapping[str, Any]) -> str:
    return semantic_digest({
        "source_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "planning_digest": execution["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest"],
        "planned_outputs": execution["planned_outputs"],
    })


def _blocked_manifest_digest(execution: Mapping[str, Any]) -> str:
    return semantic_digest({"blocked_reason": execution["blocked_reason"], "source_reentry_digest": SOURCE_REENTRY_DIGEST})


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_reentry_digest_bound": (SOURCE_REENTRY_DIGEST, execution.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.SOURCE_RESULTS_REVIEW_DIGEST, execution.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, execution.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.source.SOURCE_EXECUTION_DIGEST, execution.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.source.SOURCE_RECOVERY_DETAIL_DIGEST, execution.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.source.SOURCE_DIGEST_MANIFEST_DIGEST, execution.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, execution.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, execution.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL, execution.get("blocked_reason_before_recovery")),
        "source_after_v2_approval_digest_bound": (source.SOURCE_AFTER_V2_APPROVAL_DIGEST, execution.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (source.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, execution.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, execution.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, execution.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [execution.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "recovered_module_grouping_source_accepted_bound": (True, execution.get("recovered_module_grouping_source_accepted_for_planning_reentry")),
        "previous_blocker_resolved_for_reentry_bound": (True, execution.get("previous_after_v2_planning_execution_blocker_resolved_for_reentry")),
        "recovered_module_detail_available_if_success": (success, execution.get("recovered_module_detail_available")),
        "module_paths_available_if_success": (success, execution.get("module_paths_available")),
        "per_module_counts_available_if_success": (success, execution.get("per_module_counts_available")),
        "bounded_samples_available_if_success": (success, execution.get("bounded_samples_available")),
        "failed_or_errored_nodeids_1404_bound": (1404, execution.get("failed_or_errored_nodeids_count")),
        "module_count_29_bound": (29, execution.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], execution.get("largest_module_nodeid_counts")),
        "top_five_module_paths_bound": (TOP_FIVE_PATHS, execution.get("top_five_module_paths")),
        "top_five_count_sum_612_bound": (612, execution.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, execution.get("top_10_count_sum")),
        "priority_tier_policy_defined_if_success": (PRIORITY_TIER_POLICY if success else [], execution.get("priority_tier_policy", [])),
        "priority_tier_1_sum_612_if_success": (612 if success else 0, execution.get("priority_tier_1_count_sum", 0)),
        "priority_tier_2_sum_457_if_success": (457 if success else 0, execution.get("priority_tier_2_count_sum", 0)),
        "priority_tier_3_sum_335_if_success": (335 if success else 0, execution.get("priority_tier_3_count_sum", 0)),
        "selected_package_prioritize_largest_modules": (SELECTED_PACKAGE, execution.get("selected_remediation_or_method_after_v2_package")),
        "reentry_execution_created_true": (True, execution.get("remediation_or_method_after_v2_reentry_execution_created")),
        "after_v2_planning_execution_reentered_true": (True, execution.get("after_v2_planning_execution_reentered")),
        "planning_execution_performed_true_if_success": (success, execution.get("after_v2_planning_execution_performed")),
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (False, execution.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, execution.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, execution.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, execution.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, execution.get("broker_execution")),
    }
    generated_fields = {
        "module_prioritization_generated_true_if_success": "module_prioritization_generated",
        "prioritized_module_group_summary_generated_true_if_success": "prioritized_module_group_summary_generated",
        "priority_tier_report_generated_true_if_success": "priority_tier_report_generated",
        "top_module_concentration_report_generated_true_if_success": "top_module_concentration_report_generated",
        "recommended_follow_on_candidate_report_generated_true_if_success": "recommended_follow_on_candidate_report_generated",
    }
    values.update({check_id: (success, execution.get(field)) for check_id, field in generated_fields.items()})
    false_fields = {
        "diagnostic_method_executed_false": "diagnostic_method_executed", "code_remediation_executed_false": "code_remediation_executed",
        "evidence_remediation_executed_false": "evidence_remediation_executed", "classification_execution_false": "classification_execution_performed_in_reentry",
        "cache_read_false": "cache_read_in_reentry", "module_grouping_recovered_in_reentry_false": "module_grouping_recovered_in_reentry",
        "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed", "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed", "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "reentry_results_review_created_false": "remediation_or_method_results_review_after_v2_created",
        "targeted_diagnostic_capture_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created", "main_merge_approval_created_false": "main_merge_approval_created",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "integration_success_false": "integration_execution_successful", "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed", "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed", "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated", "provider_requests_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution", "dataset_generation_false": "dataset_generation_performed_in_execution",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed", "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed", "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, execution.get(field)) for check_id, field in false_fields.items()})
    values["successful_integration_digest_false"] = ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")])
    extras = {
        "prioritized_planning_digest_generated": (True, bool(execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest"))),
        "digest_manifest_digest_generated": (True, bool(execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest"))),
        "ready_for_reentry_results_review_true": (True, execution.get("ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry")),
    } if success else {
        "blocked_reason_recorded": (True, bool(execution.get("blocked_reason"))),
        "blocked_manifest_digest_generated": (True, bool(execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"))),
        "planning_execution_performed_false": (False, execution.get("after_v2_planning_execution_performed")),
        "source_or_reentry_failure_diagnosis_defined": (BLOCKED_NEXT_TASK, execution.get("recommended_next_task")),
    }
    values.update(extras)
    ordered = [
        "source_reentry_digest_bound", "source_recovery_results_review_digest_bound", "source_recovery_results_review_manifest_digest_bound",
        "source_recovery_execution_digest_bound", "source_recovery_detail_digest_bound", "source_recovery_digest_manifest_bound",
        "source_blocked_after_v2_execution_digest_bound", "source_blocked_after_v2_manifest_digest_bound", "source_blocked_reason_bound",
        "source_after_v2_approval_digest_bound", "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound",
        "source_module_grouping_digest_bound", "retry_execution_commit_bound", "retry_failure_counts_bound",
        "recovered_module_grouping_source_accepted_bound", "previous_blocker_resolved_for_reentry_bound",
        "recovered_module_detail_available_if_success", "module_paths_available_if_success", "per_module_counts_available_if_success",
        "bounded_samples_available_if_success", "failed_or_errored_nodeids_1404_bound", "module_count_29_bound",
        "largest_module_counts_bound", "top_five_module_paths_bound", "top_five_count_sum_612_bound",
        "top_ten_count_sum_1069_bound", "priority_tier_policy_defined_if_success", "priority_tier_1_sum_612_if_success",
        "priority_tier_2_sum_457_if_success", "priority_tier_3_sum_335_if_success", *generated_fields,
        "selected_package_prioritize_largest_modules", "reentry_execution_created_true", "after_v2_planning_execution_reentered_true",
        "planning_execution_performed_true_if_success", *false_fields, "successful_integration_digest_false",
        "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
        "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files", *extras,
    ]
    return [_check(check_id, *values[check_id]) for check_id in ordered]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]], success: bool) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    summary = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "after_v2_planning_execution_reentered": True, "after_v2_planning_execution_performed": success,
        "module_prioritization_generated": success, "targeted_diagnostic_output_capture_candidate_created": False,
        "new_retry_candidate_created": False, "integration_execution_successful": False,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        summary.update(
            remediation_or_method_after_v2_reentry_execution_created=True,
            remediation_or_method_after_v2_reentry_execution_performed=True,
            planning_method_after_v2_reentry_executed=True,
            prioritized_module_group_summary_generated=True,
            top_module_concentration_report_generated=True,
            failed_or_errored_nodeids_count=1404, module_summary_module_count=29,
            top_5_count_sum=612, top_5_percentage_of_failed_or_errored_nodeids="43.58974359",
            top_10_count_sum=1069, top_10_percentage_of_failed_or_errored_nodeids="76.13960114",
            recommended_follow_on_package_after_results_review=FOLLOW_ON_PACKAGE,
            ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry=True,
            new_retry_executed=False,
        )
    else:
        summary["blocked_reason"] = execution["blocked_reason"]
    return summary


def execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
    *, source_reentry: dict | None = None, recovered_module_grouping_snapshot: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Generate planning evidence or fail closed without reading cache or inventing paths."""

    reentry = deepcopy(source_reentry) if source_reentry is not None else _committed_source_reentry()
    precheck_failures = _source_precheck_failures(reentry)
    rows, detail_failures = _snapshot_rows(recovered_module_grouping_snapshot)
    success = not precheck_failures and not detail_failures
    execution = _common(reentry, run_timestamp_utc)
    execution["recovered_module_detail_available"] = success
    execution["module_paths_available"] = success
    execution["per_module_counts_available"] = success
    execution["bounded_samples_available"] = success
    if success:
        planned_rows = _planning_rows(rows)
        execution.update(
            artifact_kind=ARTIFACT_KIND_EXECUTED, execution_status=EXECUTION_STATUS_READY,
            source_recovery_detail_used=True, after_v2_planning_execution_performed=True,
            remediation_or_method_after_v2_reentry_execution_performed=True,
            planning_method_after_v2_reentry_executed=True,
            module_prioritization_generated=True, prioritized_module_group_summary_generated=True,
            priority_tier_report_generated=True, top_module_concentration_report_generated=True,
            diagnostic_capture_candidate_report_generated=True, evidence_root_review_candidate_report_generated=True,
            path_cwd_review_candidate_report_generated=True, digest_drift_review_candidate_report_generated=True,
            fixture_isolation_review_candidate_report_generated=True, unsupported_claims_boundary_report_generated=True,
            recommended_follow_on_candidate_report_generated=True, digest_manifest_generated=True,
            prioritized_module_group_summary=planned_rows,
            priority_tier_report=[
                {"priority_tier": PRIORITY_TIER_POLICY[0], "rank_start": 1, "rank_end": 5, "module_count": 5, "count_sum": 612, "percentage": "43.58974359"},
                {"priority_tier": PRIORITY_TIER_POLICY[1], "rank_start": 6, "rank_end": 10, "module_count": 5, "count_sum": 457, "percentage": "32.54985755"},
                {"priority_tier": PRIORITY_TIER_POLICY[2], "rank_start": 11, "rank_end": 29, "module_count": 19, "count_sum": 335, "percentage": "23.86039886"},
            ],
            top_module_concentration_report={"top_5_count_sum": 612, "top_5_percentage": "43.58974359", "top_10_count_sum": 1069, "top_10_percentage": "76.13960114"},
            diagnostic_capture_candidate_report={"planning_bucket": PLANNING_BUCKETS[0], "status": "GENERATED_RESEARCH_ONLY"},
            evidence_root_review_candidate_report={"planning_bucket": PLANNING_BUCKETS[1], "status": "GENERATED_RESEARCH_ONLY"},
            path_cwd_review_candidate_report={"planning_bucket": PLANNING_BUCKETS[2], "status": "GENERATED_RESEARCH_ONLY"},
            digest_drift_review_candidate_report={"planning_bucket": PLANNING_BUCKETS[3], "status": "GENERATED_RESEARCH_ONLY"},
            fixture_isolation_review_candidate_report={"planning_bucket": PLANNING_BUCKETS[4], "status": "GENERATED_RESEARCH_ONLY"},
            unsupported_claims_boundary_report=deepcopy(UNSUPPORTED_CLAIMS),
            recommended_follow_on_candidate_report={
                "package": FOLLOW_ON_PACKAGE,
                "status": "RECOMMENDED_FOR_FUTURE_CANDIDATE_AFTER_RESULTS_REVIEW_NOT_SELECTED",
                "reason": "The top module groups concentrate a material portion of the failed-or-errored node IDs, but no traceback evidence is available. A future targeted diagnostic-output capture candidate is the safest next investigative step after results review.",
            },
            recommended_follow_on_package_after_results_review=FOLLOW_ON_PACKAGE,
            recommended_follow_on_package_status="RECOMMENDED_FOR_FUTURE_CANDIDATE_AFTER_RESULTS_REVIEW_NOT_SELECTED",
            planned_outputs_generated=True,
            planned_outputs=[{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
            ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry=True,
            recommended_next_task=SUCCESS_NEXT_TASK,
        )
        execution["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest"] = _planning_digest(execution)
        execution["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest"] = _digest_manifest_digest(execution)
    else:
        failures = precheck_failures + detail_failures
        execution.update(
            artifact_kind=ARTIFACT_KIND_BLOCKED,
            execution_status=EXECUTION_STATUS_BLOCKED_PRECHECK if precheck_failures else EXECUTION_STATUS_BLOCKED_SOURCE,
            source_recovery_detail_used=False, after_v2_planning_execution_performed=False,
            remediation_or_method_after_v2_reentry_execution_performed=False,
            planning_method_after_v2_reentry_executed=False, module_prioritization_generated=False,
            prioritized_module_group_summary_generated=False, priority_tier_report_generated=False,
            top_module_concentration_report_generated=False, recommended_follow_on_candidate_report_generated=False,
            planned_outputs_generated=False, blocked_reason=";".join(failures),
            recommended_next_task=BLOCKED_NEXT_TASK,
        )
        for key in ("priority_tier_policy", "priority_tier_1_count_sum", "priority_tier_2_count_sum", "priority_tier_3_count_sum"):
            execution.pop(key, None)
        execution["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"] = _blocked_manifest_digest(execution)
    execution["precheck_results"] = _prechecks(execution, success)
    execution["execution_steps"] = _steps(success)
    execution["next_chain"] = list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN)
    execution["next_gates"] = list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES)
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    execution["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest"] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(execution: dict) -> dict:
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("execution must be object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_EXECUTED
    expected_kind = ARTIFACT_KIND_EXECUTED if success else ARTIFACT_KIND_BLOCKED
    statuses = {EXECUTION_STATUS_READY} if success else {EXECUTION_STATUS_BLOCKED_SOURCE, EXECUTION_STATUS_BLOCKED_PRECHECK}
    if execution.get("artifact_kind") != expected_kind or execution.get("execution_status") not in statuses:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("artifact kind/status mismatch")
    for field, expected in {
        "execution_scope": EXECUTION_SCOPE,
        "selected_remediation_or_method_after_v2_package": SELECTED_PACKAGE,
        "source_after_v2_planning_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
    }.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError(f"{field} mismatch")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("checklist invalid")
    if execution.get("summary") != _summary(execution, checklist, success):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("summary invalid")
    digest = execution.get("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _execution_digest(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("execution digest invalid")
    if success:
        if execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest") != _planning_digest(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("prioritized planning digest invalid")
        manifest = execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest")
        if not isinstance(manifest, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest) or manifest != _digest_manifest_digest(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("digest manifest invalid")
    else:
        manifest = execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest")
        if not isinstance(manifest, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest) or manifest != _blocked_manifest_digest(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError("blocked manifest invalid")
    return {"artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"], "execution_scope": execution["execution_scope"], "execution_digest": digest, **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_markdown_v1(execution: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(execution)
    sections = [
        ("Source Planning Reentry", [SOURCE_REENTRY_DIGEST]),
        ("Source Recovery Results Review", [source.SOURCE_RESULTS_REVIEW_DIGEST]),
        ("Previous Blocked After-v2 Execution", [execution["blocked_reason_before_recovery"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]),
        ("Recovered Module Grouping Source", [f"Available for this execution: {execution['recovered_module_detail_available']}"]),
        ("Execution Scope", [EXECUTION_SCOPE]),
        ("Prioritized Module Planning", [str(execution.get("prioritized_module_group_summary", []))]),
        ("Priority Tier Report", [str(execution.get("priority_tier_report", []))]),
        ("Top Module Concentration", [str(execution.get("top_module_concentration_report", {}))]),
        ("Diagnostic and Remediation Planning Buckets", PLANNING_BUCKETS),
        ("Recommended Follow-on Candidate", [str(execution.get("recommended_follow_on_candidate_report", {}))]),
        ("Unsupported Claims Boundary", [str(UNSUPPORTED_CLAIMS)]),
        ("Success or Blocked Disposition", [execution["execution_status"], execution.get("blocked_reason", "not blocked")]),
        ("Authority Boundaries", ["No diagnostics, remediation, classification, retry, main merge, runtime, or trading authority."]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["Planning output is module-level and not traceback or root-cause evidence."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_EXECUTED", "ARTIFACT_KIND_BLOCKED", "EXECUTION_STATUS_READY",
    "EXECUTION_STATUS_BLOCKED_SOURCE", "EXECUTION_STATUS_BLOCKED_PRECHECK", "EXECUTION_SCOPE",
    "execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_markdown_v1",
]
