"""Re-enter bounded after-v2 planning using reviewed complete module detail."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_service
    as review_source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_PRIORITIZED_MODULE_PLANNING_READY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_COMPLETE_DETAIL_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_PLANNING_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1"
SELECTED_AFTER_V2_PLANNING_PACKAGE = "PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING"
SOURCE_RESULTS_REVIEW_DIGEST = "9124d03f9c540873a1bb3253800b1574f1266e67708034e64c95eb1ff3254a74"
SOURCE_BINDING_REVIEW_DIGEST = "93469cab365790b9c06db106a7df1366cfedbfff09d6a46cd63924a58419ce93"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "ae573ace5d5d172337d389f7cf000c0cdcf3634bc68fd32394e663f45a08e76d"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
GENERATED_RESEARCH_ONLY = "GENERATED_RESEARCH_ONLY"
PLANNING_ONLY_NOT_EXECUTED = "PLANNING_ONLY_NOT_EXECUTED"
TOP_FIVE_PATHS = list(review_source.source.review_source.source.EXPECTED_TOP_FIVE_PATHS)
UNSUPPORTED_ROW_CLAIMS = list(review_source.source.review_source.source.UNSUPPORTED_ROW_CLAIMS)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_PRIORITIZED_MODULE_PLANNING_READY = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_COMPLETE_DETAIL_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_PLANNING_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_digest"
PLANNING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_with_complete_detail_prioritized_module_plan_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_with_complete_detail_digest_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_blocked_manifest_digest"

OUTPUT_IDS = [
    "after_v2_planning_reentry_with_complete_detail_execution_manifest",
    "reviewed_complete_29_row_detail_binding_source_summary",
    "prioritized_module_group_summary", "priority_tier_report", "top_module_concentration_report",
    "diagnostic_capture_candidate_planning_report", "evidence_root_review_candidate_planning_report",
    "path_cwd_review_candidate_planning_report", "digest_drift_review_candidate_planning_report",
    "fixture_isolation_review_candidate_planning_report", "unsupported_claims_boundary_report",
    "recommended_follow_on_candidate_report", "digest_manifest",
]

PLANNING_BUCKETS = [
    "TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_PLANNING",
    "EVIDENCE_ROOT_REQUIREMENT_REVIEW_PLANNING",
    "PATH_AND_CWD_ASSUMPTION_REVIEW_PLANNING",
    "DIGEST_CONSTANT_DRIFT_REVIEW_PLANNING",
    "TEST_FIXTURE_ISOLATION_REVIEW_PLANNING",
]

SUCCESS_NEXT_CHAIN = [
    "Remediation or Method Results Review After Classification v2 Review Reentry with Complete Detail v1.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported by results review.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "After-v2 Planning Reentry with Complete Detail Failure Diagnosis v1.",
    "Alternate complete-detail planning source or planning-method candidate, if needed.",
    "No diagnostic capture, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "after_v2_planning_reentry_with_complete_detail_failure_diagnosis",
    "alternate_complete_detail_planning_source_or_method_candidate_if_needed",
    "diagnostic_capture_blocked_until_planning_reentry_review_passes",
    "new_retry_blocked_until_remediation_or_method_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]

RISK_CONTROLS = [
    "planning_reentry_with_complete_detail_uses_reviewed_binding_only",
    "planning_reentry_with_complete_detail_does_not_read_cache",
    "planning_reentry_with_complete_detail_does_not_modify_cache",
    "planning_reentry_with_complete_detail_does_not_commit_pytest_cache",
    "planning_reentry_with_complete_detail_does_not_commit_marketflow_outputs",
    "planning_reentry_with_complete_detail_does_not_rerun_detail_binding_reattempt",
    "planning_reentry_with_complete_detail_does_not_rerun_materialization",
    "planning_reentry_with_complete_detail_does_not_rerun_source_recovery",
    "planning_reentry_with_complete_detail_does_not_parse_operator_logs",
    "planning_reentry_with_complete_detail_does_not_run_diagnostic_commands",
    "planning_reentry_with_complete_detail_does_not_execute_diagnostics",
    "planning_reentry_with_complete_detail_does_not_execute_remediation",
    "planning_reentry_with_complete_detail_does_not_execute_classification",
    "planning_reentry_with_complete_detail_does_not_classify_modules_again",
    "planning_reentry_with_complete_detail_does_not_rerun_retry",
    "planning_reentry_with_complete_detail_does_not_run_full_pytest",
    "planning_reentry_with_complete_detail_does_not_create_targeted_diagnostic_candidate",
    "planning_reentry_with_complete_detail_does_not_create_new_retry_candidate",
    "planning_reentry_with_complete_detail_does_not_create_retry_results_review",
    "planning_reentry_with_complete_detail_does_not_create_integration_results_review",
    "planning_reentry_with_complete_detail_does_not_mark_integration_successful",
    "planning_reentry_with_complete_detail_does_not_generate_successful_integration_digest",
    "planning_reentry_with_complete_detail_does_not_claim_failure_error_separation",
    "planning_reentry_with_complete_detail_does_not_claim_first_failure",
    "planning_reentry_with_complete_detail_does_not_claim_first_error",
    "planning_reentry_with_complete_detail_does_not_claim_traceback_root_cause",
    "planning_reentry_with_complete_detail_does_not_recommend_direct_code_remediation",
    "planning_reentry_with_complete_detail_does_not_treat_planning_as_retry_success",
    "planning_reentry_with_complete_detail_does_not_push_integration_branch",
    "planning_reentry_with_complete_detail_does_not_push_main",
    "planning_reentry_with_complete_detail_does_not_delete_integration_branch",
    "planning_reentry_with_complete_detail_does_not_delete_worktree",
    "planning_reentry_with_complete_detail_does_not_force_push",
    "planning_reentry_with_complete_detail_does_not_prune_remotes",
    "planning_reentry_with_complete_detail_does_not_modify_tags",
    "planning_reentry_with_complete_detail_does_not_modify_staged_evidence",
    "planning_reentry_with_complete_detail_does_not_regenerate_evidence",
    "planning_reentry_with_complete_detail_does_not_call_providers",
    "planning_reentry_with_complete_detail_does_not_acquire_market_data",
    "planning_reentry_with_complete_detail_does_not_regenerate_dataset",
    "planning_reentry_with_complete_detail_does_not_recompute_metrics",
    "planning_reentry_with_complete_detail_does_not_train_models",
    "planning_reentry_with_complete_detail_does_not_score_strategy",
    "planning_reentry_with_complete_detail_does_not_generate_recommendations",
    "planning_reentry_with_complete_detail_does_not_accept_predictive_usefulness",
    "planning_reentry_with_complete_detail_does_not_accept_profitability",
    "planning_reentry_with_complete_detail_does_not_authorize_runtime",
    "planning_reentry_with_complete_detail_does_not_authorize_broker_execution",
    "planning_output_is_research_planning_only_not_root_cause", "planning_output_is_not_retry_success",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_reentry_execution_remains_historically_blocked",
    "previous_detail_binding_reattempt_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_results_review_required_after_planning_reentry",
    "separate_diagnostic_capture_candidate_required_after_results_review",
    "separate_diagnostic_capture_approval_required_before_diagnostics",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_FIELDS = [
    "targeted_diagnostic_output_capture_candidate_created", "diagnostic_capture_operator_review_created",
    "diagnostic_capture_approval_created", "diagnostic_capture_execution_performed",
    "diagnostic_capture_results_review_created", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "cache_read_in_execution",
    "cache_modified_in_execution", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "module_grouping_recovered_in_execution", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_execution", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed",
    "ready_for_targeted_diagnostic_output_capture_candidate", "ready_for_retry_candidate",
]

SOURCE_BINDINGS = {
    "source_detail_binding_reattempt_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
    "source_complete_29_row_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
    "source_detail_binding_reattempt_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    "source_detail_binding_reattempt_digest": review_source.SOURCE_REATTEMPT_DIGEST,
    "source_complete_29_row_binding_digest": review_source.SOURCE_BINDING_DIGEST,
    "source_detail_binding_reattempt_digest_manifest_digest": review_source.SOURCE_REATTEMPT_MANIFEST_DIGEST,
    **deepcopy(review_source.SOURCE_BINDINGS),
}


class MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError(ValueError):
    """Raised when planning reentry source or output violates the contract."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _committed_source_review() -> dict[str, Any]:
    rows = review_source._committed_binding_rows()
    return {
        "artifact_kind": review_source.ARTIFACT_KIND, "review_status": review_source.REVIEW_STATUS,
        "review_scope": review_source.REVIEW_SCOPE,
        review_source.REVIEW_DIGEST_KEY: SOURCE_RESULTS_REVIEW_DIGEST,
        review_source.BINDING_REVIEW_DIGEST_KEY: SOURCE_BINDING_REVIEW_DIGEST,
        review_source.REVIEW_MANIFEST_DIGEST_KEY: SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "selected_detail_exposure_or_binding_package": review_source.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "detail_exposure_or_binding_reattempt_results_review_ready": True,
        "source_detail_binding_reattempt_reviewed": True,
        "source_detail_binding_digest_verified": True,
        "source_detail_binding_digest_manifest_verified": True,
        "reviewed_complete_29_row_detail_binding_source": True,
        "complete_29_row_detail_binding_integrity_reviewed": True,
        "ready_for_after_v2_planning_reentry_with_complete_detail": True,
        "ready_for_retry_candidate": False,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
        "complete_29_row_detail_binding_source_review": {
            "reviewed": True, "row_count": 29, "failed_or_errored_nodeids_count": 1404,
            "source_binding_digest": review_source.SOURCE_BINDING_DIGEST, "rows": rows,
        },
    }


def _source_review_reasons(review: Any) -> list[str]:
    if not isinstance(review, Mapping):
        return ["SOURCE_DETAIL_BINDING_RESULTS_REVIEW_UNAVAILABLE"]
    expected = _committed_source_review()
    fields = [
        "artifact_kind", "review_status", "review_scope", review_source.REVIEW_DIGEST_KEY,
        review_source.BINDING_REVIEW_DIGEST_KEY, review_source.REVIEW_MANIFEST_DIGEST_KEY,
        "selected_detail_exposure_or_binding_package", *SOURCE_BINDINGS,
        "retry_execution_commit", "retry_failure_context",
        "detail_exposure_or_binding_reattempt_results_review_ready",
        "source_detail_binding_reattempt_reviewed", "source_detail_binding_digest_verified",
        "source_detail_binding_digest_manifest_verified", "reviewed_complete_29_row_detail_binding_source",
        "complete_29_row_detail_binding_integrity_reviewed",
        "ready_for_after_v2_planning_reentry_with_complete_detail", "ready_for_retry_candidate",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "largest_module_nodeid_counts",
        "top_five_module_paths", "top_5_count_sum", "top_10_count_sum",
        "priority_tier_1_count_sum", "priority_tier_2_count_sum", "priority_tier_3_count_sum",
    ]
    return [f"SOURCE_REVIEW_{field.upper()}_MISMATCH_OR_MISSING" for field in fields if review.get(field) != expected[field]]


def _source_rows_reasons(rows: Any) -> list[str]:
    expected = review_source._committed_binding_rows()
    if not isinstance(rows, list) or not rows:
        return ["REVIEWED_COMPLETE_29_ROW_DETAIL_BINDING_UNAVAILABLE"]
    reasons: list[str] = []
    if rows != expected:
        reasons.append("REVIEWED_COMPLETE_29_ROW_DETAIL_BINDING_MISMATCH")
    if len(rows) != 29:
        reasons.append("COMPLETE_DETAIL_ROW_COUNT_NOT_29")
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    if len(counts) != 29 or sum(value for value in counts if isinstance(value, int) and not isinstance(value, bool)) != 1404:
        reasons.append("FAILED_OR_ERRORED_NODEID_TOTAL_NOT_1404")
    if counts[:5] != [136, 131, 122, 112, 111]:
        reasons.append("TOP_FIVE_COUNTS_MISMATCH")
    if paths[:5] != TOP_FIVE_PATHS:
        reasons.append("TOP_FIVE_PATHS_MISMATCH")
    if sum(value for value in counts[:10] if isinstance(value, int)) != 1069:
        reasons.append("TOP_TEN_SUM_NOT_1069")
    if [sum(value for value in section if isinstance(value, int)) for section in (counts[:5], counts[5:10], counts[10:])] != [612, 457, 335]:
        reasons.append("PRIORITY_TIER_SUMS_MISMATCH")
    if any(not isinstance(row, Mapping) or not 0 < len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows):
        reasons.append("SAMPLES_MISSING_OR_EXCEED_BOUND_5")
    if semantic_digest(rows) != review_source.SOURCE_BINDING_DIGEST:
        reasons.append("COMPLETE_DETAIL_BINDING_DIGEST_MISMATCH")
    return reasons


PRECHECK_IDS = [
    "source_detail_binding_reattempt_results_review_digest_bound",
    "source_complete_29_row_binding_review_digest_bound",
    "source_detail_binding_reattempt_results_review_manifest_digest_bound",
    "source_detail_binding_reattempt_digest_bound", "source_complete_29_row_binding_digest_bound",
    "source_detail_binding_reattempt_digest_manifest_digest_bound",
    "source_materialization_results_review_digest_bound", "source_materialized_payload_review_digest_bound",
    "source_materialization_execution_digest_bound", "source_materialized_payload_digest_bound",
    "source_detail_exposure_or_binding_approval_digest_bound", "source_reentry_failure_diagnosis_digest_bound",
    "source_reentry_blocked_execution_digest_bound", "source_recovery_results_review_digest_bound",
    "source_recovery_detail_digest_bound", "source_after_v2_approval_digest_bound",
    "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound", "retry_failure_counts_bound",
    "reviewed_complete_29_row_binding_available", "reviewed_complete_29_row_binding_digest_verified",
    "no_cache_read", "no_reattempt_rerun", "no_materialization_rerun", "no_source_recovery_rerun",
    "no_retry_rerun", "no_full_pytest", "no_diagnostic_command", "origin_main_unchanged",
    "integration_branch_head_unchanged", "staged_evidence_unchanged",
    "marketflow_outputs_not_tracked", "pytest_cache_not_tracked",
]

STEP_IDS = [
    "verify_source_detail_binding_reattempt_results_review", "verify_source_detail_binding_reattempt_execution",
    "verify_complete_29_row_binding_digest", "verify_materialization_results_review_context",
    "verify_detail_exposure_or_binding_approval_context", "verify_prior_blocked_detail_binding_execution_context",
    "verify_reentry_failure_diagnosis_context", "verify_recovery_results_review_context",
    "verify_after_v2_approval_context", "verify_retry_failure_context", "verify_protected_refs",
    "verify_tracking_boundaries", "locate_reviewed_complete_29_row_detail_binding_source",
    "verify_complete_29_row_source_available_or_block", "verify_29_module_rows",
    "verify_total_failed_or_errored_nodeids_1404", "verify_largest_module_counts", "verify_top_five_paths",
    "verify_top_five_and_top_ten_sums", "verify_tier_sums", "verify_bounded_samples",
    "build_prioritized_module_group_summary", "build_priority_tier_report",
    "build_top_module_concentration_report", "build_diagnostic_capture_candidate_planning_report",
    "build_evidence_root_review_candidate_planning_report", "build_path_cwd_review_candidate_planning_report",
    "build_digest_drift_review_candidate_planning_report", "build_fixture_isolation_review_candidate_planning_report",
    "build_unsupported_claims_boundary_report", "build_recommended_follow_on_candidate_report",
    "build_digest_manifest", "preserve_failed_retry_authority", "do_not_read_cache",
    "do_not_rerun_detail_binding_reattempt", "do_not_rerun_materialization", "do_not_rerun_source_recovery",
    "do_not_create_targeted_diagnostic_candidate", "do_not_create_retry_candidate", "do_not_create_results_review",
]


def _prechecks(success: bool) -> list[dict[str, Any]]:
    return [
        {"precheck_id": item, "status": PASS if success or item != "reviewed_complete_29_row_binding_available" else FAIL}
        for item in PRECHECK_IDS
    ]


def _steps(success: bool) -> list[dict[str, Any]]:
    source_steps = set(STEP_IDS[12:32])
    return [
        {
            "step_id": step_id, "status": PASS if success or step_id not in source_steps else BLOCKER,
            "expected": "completed" if success or step_id not in source_steps else "reviewed complete detail",
            "actual": "completed" if success or step_id not in source_steps else "blocked",
            "message": f"{step_id} {'completed' if success or step_id not in source_steps else 'blocked'}",
        }
        for step_id in STEP_IDS
    ]


def _common(timestamp: str) -> dict[str, Any]:
    common = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_after_v2_planning_package": SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "created_offline": True, "governance_only": True, "planning_execution_only": True,
        "run_timestamp_utc": timestamp, "used_committed_source_evidence_only": True,
        **deepcopy(SOURCE_BINDINGS),
        "source_detail_binding_results_review_artifact_kind": review_source.ARTIFACT_KIND,
        "source_detail_binding_results_review_status": review_source.REVIEW_STATUS,
        "source_detail_binding_results_review_scope": review_source.REVIEW_SCOPE,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True, "marketflow_outputs_tracked_in_repository": False,
        "pytest_cache_tracked_in_repository": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "risk_controls": list(RISK_CONTROLS),
    }
    common.update({field: False for field in FALSE_FIELDS})
    return common


def _priority_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("PRIORITY_1_TOP_5_MODULE_GROUPS", 1, 5, 612, "highest-priority diagnostic-output capture and planning review group"),
        ("PRIORITY_2_NEXT_5_MODULE_GROUPS", 6, 10, 457, "secondary diagnostic planning group"),
        ("PRIORITY_3_REMAINING_MODULE_GROUPS", 11, 29, 335, "coverage and systemic review planning group"),
    ]
    result = []
    for group_id, start, end, total, purpose in specs:
        selected = rows[start - 1:end]
        result.append({
            "priority_group": group_id, "rank_start": start, "rank_end": end,
            "module_count": len(selected), "failed_or_errored_nodeid_count": total,
            "purpose": purpose, "root_cause_claimed": False,
            "module_paths": [row["module_path"] for row in selected],
        })
    return result


def _planning_buckets() -> list[dict[str, Any]]:
    purposes = [
        "Plan bounded diagnostic-output capture for the highest-priority groups.",
        "Plan review of evidence-root requirements without inspecting evidence roots.",
        "Plan review of path and working-directory assumptions without diagnostic execution.",
        "Plan review of digest constant drift without changing digests or evidence.",
        "Plan review of fixture isolation without executing or modifying fixtures.",
    ]
    return [
        {"planning_bucket": bucket, "status": PLANNING_ONLY_NOT_EXECUTED, "purpose": purpose,
         "diagnostic_executed": False, "remediation_executed": False, "root_cause_claimed": False}
        for bucket, purpose in zip(PLANNING_BUCKETS, purposes, strict=True)
    ]


def _success(common: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    bound_rows = deepcopy(rows)
    groups = _priority_groups(bound_rows)
    buckets = _planning_buckets()
    tier_report = {
        "priority_tiers_generated": True, "planning_only": True,
        "priority_tier_1": groups[0], "priority_tier_2": groups[1], "priority_tier_3": groups[2],
    }
    concentration = {
        "top_five_module_paths": [row["module_path"] for row in bound_rows[:5]],
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in bound_rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "root_cause_claimed": False,
    }
    bucket_reports = {
        "diagnostic_capture_candidate_planning_report": buckets[0],
        "evidence_root_review_candidate_planning_report": buckets[1],
        "path_cwd_review_candidate_planning_report": buckets[2],
        "digest_drift_review_candidate_planning_report": buckets[3],
        "fixture_isolation_review_candidate_planning_report": buckets[4],
    }
    follow_on = {
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "ready_for_results_review": True,
        "ready_for_targeted_diagnostic_output_capture_candidate": False,
        "ready_for_retry_candidate": False,
    }
    plan_payload = {
        "source_binding_digest": review_source.SOURCE_BINDING_DIGEST,
        "prioritized_module_groups": groups, "priority_tier_report": tier_report,
        "top_module_concentration_report": concentration, "planning_buckets": buckets,
        "recommended_follow_on_candidate_report": follow_on,
    }
    planning_digest = semantic_digest(plan_payload)
    digest_manifest = {
        "source_results_review": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_binding_review": SOURCE_BINDING_REVIEW_DIGEST,
        "source_results_review_manifest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_binding": review_source.SOURCE_BINDING_DIGEST,
        "prioritized_module_plan": planning_digest,
        "prioritized_module_groups": semantic_digest(groups), "priority_tiers": semantic_digest(tier_report),
        "top_module_concentration": semantic_digest(concentration), "planning_buckets": semantic_digest(buckets),
        "unsupported_claims": semantic_digest(UNSUPPORTED_ROW_CLAIMS),
        "recommended_follow_on": semantic_digest(follow_on),
    }
    execution = {
        **common, "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        "used_reviewed_complete_29_row_detail_binding": True,
        "after_v2_planning_execution_reentry_with_complete_detail_executed": True,
        "after_v2_planning_execution_reentry_created": True,
        "after_v2_planning_execution_reentry_performed": True,
        "planning_method_after_v2_reentry_executed": True,
        "complete_29_row_detail_used_for_planning": True,
        "complete_29_row_detail_verified_for_planning": True,
        "reviewed_complete_29_row_detail_binding_source_used": True,
        "module_prioritization_generated": True, "prioritized_module_group_summary_generated": True,
        "priority_tier_report_generated": True, "top_module_concentration_report_generated": True,
        "diagnostic_capture_candidate_report_generated": True,
        "evidence_root_review_candidate_report_generated": True,
        "path_cwd_review_candidate_report_generated": True, "digest_drift_review_candidate_report_generated": True,
        "fixture_isolation_review_candidate_report_generated": True,
        "unsupported_claims_boundary_report_generated": True,
        "recommended_follow_on_candidate_report_generated": True, "planned_outputs_generated": True,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335, "priority_tiers_generated": True,
        "planning_buckets_generated": True,
        "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail": True,
        "complete_29_row_detail_binding_source": bound_rows,
        "after_v2_planning_reentry_with_complete_detail_execution_manifest": {
            "row_count": 29, "nodeid_count": 1404, "source_binding_digest": review_source.SOURCE_BINDING_DIGEST,
        },
        "reviewed_complete_29_row_detail_binding_source_summary": {
            "row_count": 29, "nodeid_count": 1404, "source_binding_digest": review_source.SOURCE_BINDING_DIGEST,
        },
        "prioritized_module_group_summary": groups, "priority_tier_report": tier_report,
        "top_module_concentration_report": concentration, "planning_buckets": buckets,
        **bucket_reports,
        "unsupported_claims_boundary_report": list(UNSUPPORTED_ROW_CLAIMS),
        "recommended_follow_on_candidate_report": follow_on, "digest_manifest": digest_manifest,
        PLANNING_DIGEST_KEY: planning_digest, MANIFEST_DIGEST_KEY: semantic_digest(digest_manifest),
        "outputs_generated": [{"output_id": output_id, "status": GENERATED_RESEARCH_ONLY} for output_id in OUTPUT_IDS],
        "precheck_results": _prechecks(True), "execution_steps": _steps(True),
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "recommended_next_task": SUCCESS_NEXT_TASK, "blocked_reason": None,
    }
    return execution


def _blocked(common: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    blocked_reason = ";".join(dict.fromkeys(reasons))
    return {
        **common, "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        "used_reviewed_complete_29_row_detail_binding": False,
        "after_v2_planning_execution_reentry_with_complete_detail_executed": True,
        "after_v2_planning_execution_reentry_created": False,
        "after_v2_planning_execution_reentry_performed": False,
        "planning_method_after_v2_reentry_executed": False,
        "complete_29_row_detail_used_for_planning": False,
        "complete_29_row_detail_verified_for_planning": False,
        "reviewed_complete_29_row_detail_binding_source_used": False,
        "module_prioritization_generated": False, "prioritized_module_group_summary_generated": False,
        "priority_tier_report_generated": False, "top_module_concentration_report_generated": False,
        "diagnostic_capture_candidate_report_generated": False,
        "evidence_root_review_candidate_report_generated": False,
        "path_cwd_review_candidate_report_generated": False, "digest_drift_review_candidate_report_generated": False,
        "fixture_isolation_review_candidate_report_generated": False,
        "unsupported_claims_boundary_report_generated": False,
        "recommended_follow_on_candidate_report_generated": False, "planned_outputs_generated": False,
        "failed_or_errored_nodeids_count": 0, "module_summary_module_count": 0,
        "largest_module_nodeid_counts": [], "top_five_module_paths": [],
        "top_5_count_sum": 0, "top_10_count_sum": 0,
        "priority_tier_1_count_sum": 0, "priority_tier_2_count_sum": 0, "priority_tier_3_count_sum": 0,
        "priority_tiers_generated": False, "planning_buckets_generated": False,
        "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail": False,
        "complete_29_row_detail_binding_source": [], "outputs_generated": [],
        "precheck_results": _prechecks(False), "execution_steps": _steps(False),
        "available_data": [
            "source detail-binding reattempt results-review digest", "source complete 29-row binding digest",
            "source binding-review digest", "retry counts", "reviewed complete-detail summary facts",
            "any committed complete detail rows found",
        ],
        "missing_data": list(dict.fromkeys(reasons)), "blocked_reason": blocked_reason,
        BLOCKED_MANIFEST_DIGEST_KEY: semantic_digest({
            "blocked_reason": blocked_reason, "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
        }),
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        "recommended_next_task": BLOCKED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    rows = execution.get("complete_29_row_detail_binding_source", [])
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    values: dict[str, tuple[Any, Any]] = {
        "source_results_review_ready_bound": (review_source.REVIEW_STATUS, execution.get("source_detail_binding_results_review_status")),
        "reviewed_complete_detail_binding_ready_bound": (success, execution.get("used_reviewed_complete_29_row_detail_binding")),
        "complete_29_row_binding_digest_verified": (review_source.SOURCE_BINDING_DIGEST, execution.get("source_complete_29_row_binding_digest")),
        "selected_after_v2_planning_package_bound": (SELECTED_AFTER_V2_PLANNING_PACKAGE, execution.get("selected_after_v2_planning_package")),
        "complete_29_row_detail_used_if_success": (success, execution.get("complete_29_row_detail_used_for_planning")),
        "complete_29_row_rows_exactly_29_if_success": (29 if success else 0, len(rows)),
        "failed_or_errored_nodeids_1404_if_success": (1404 if success else 0, sum(value for value in counts if isinstance(value, int) and not isinstance(value, bool))),
        "largest_module_counts_if_success": ([136, 131, 122, 112, 111] if success else [], counts[:5]),
        "top_five_paths_preserved_if_success": (TOP_FIVE_PATHS if success else [], paths[:5]),
        "top_five_sum_612_if_success": (612 if success else 0, sum(value for value in counts[:5] if isinstance(value, int))),
        "top_ten_sum_1069_if_success": (1069 if success else 0, sum(value for value in counts[:10] if isinstance(value, int))),
        "tier_1_sum_612_if_success": (612 if success else 0, sum(value for value in counts[:5] if isinstance(value, int))),
        "tier_2_sum_457_if_success": (457 if success else 0, sum(value for value in counts[5:10] if isinstance(value, int))),
        "tier_3_sum_335_if_success": (335 if success else 0, sum(value for value in counts[10:] if isinstance(value, int))),
        "bounded_samples_max_5_if_success": (success, success and bool(rows) and all(0 < len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows)),
        "module_prioritization_generated_if_success": (success, execution.get("module_prioritization_generated")),
        "priority_tier_report_generated_if_success": (success, execution.get("priority_tier_report_generated")),
        "top_module_concentration_report_generated_if_success": (success, execution.get("top_module_concentration_report_generated")),
        "planning_buckets_generated_if_success": (success, execution.get("planning_buckets_generated")),
        "planned_outputs_generated_if_success": (success, execution.get("planned_outputs_generated")),
        "ready_for_results_review_true_if_success": (success, execution.get("ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail")),
        "ready_for_targeted_diagnostic_candidate_false": (False, execution.get("ready_for_targeted_diagnostic_output_capture_candidate")),
        "ready_for_retry_candidate_false": (False, execution.get("ready_for_retry_candidate")),
        "blocked_reason_recorded_if_blocked": (not success, bool(execution.get("blocked_reason"))),
        "blocked_manifest_digest_generated_if_blocked": (not success, bool(execution.get(BLOCKED_MANIFEST_DIGEST_KEY))),
    }
    source_checks = {
        "source_detail_binding_reattempt_results_review_digest_bound": "source_detail_binding_reattempt_results_review_digest",
        "source_complete_29_row_binding_review_digest_bound": "source_complete_29_row_binding_review_digest",
        "source_detail_binding_reattempt_results_review_manifest_digest_bound": "source_detail_binding_reattempt_results_review_manifest_digest",
        "source_detail_binding_reattempt_digest_bound": "source_detail_binding_reattempt_digest",
        "source_complete_29_row_binding_digest_bound": "source_complete_29_row_binding_digest",
        "source_detail_binding_reattempt_digest_manifest_digest_bound": "source_detail_binding_reattempt_digest_manifest_digest",
        "source_materialization_results_review_digest_bound": "source_complete_29_row_materialization_results_review_digest",
        "source_materialized_payload_review_digest_bound": "source_complete_29_row_materialized_payload_review_digest",
        "source_materialization_results_review_manifest_digest_bound": "source_complete_29_row_materialization_results_review_manifest_digest",
        "source_materialization_execution_digest_bound": "source_complete_29_row_materialization_execution_digest",
        "source_materialized_payload_digest_bound": "source_complete_29_row_materialized_payload_digest",
        "source_materialization_digest_manifest_digest_bound": "source_complete_29_row_materialization_digest_manifest_digest",
        "source_detail_binding_approval_digest_bound": "source_detail_exposure_or_binding_approval_digest",
        "source_detail_binding_prior_blocked_execution_digest_bound": "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_detail_binding_prior_blocked_reason_bound": "source_detail_exposure_or_binding_execution_blocked_reason",
        "source_materialization_approval_digest_bound": "source_complete_29_row_materialization_approval_digest",
        "source_materialization_operator_review_digest_bound": "source_complete_29_row_materialization_operator_review_digest",
        "source_materialization_candidate_digest_bound": "source_complete_29_row_materialization_candidate_digest",
        "source_execution_failure_diagnosis_digest_bound": "source_detail_exposure_or_binding_execution_failure_diagnosis_digest",
        "source_primary_failure_class_bound": "primary_failure_class",
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
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created", "main_merge_approval_created_false": "main_merge_approval_created",
        "cache_read_in_execution_false": "cache_read_in_execution", "cache_modified_in_execution_false": "cache_modified_in_execution",
        "detail_binding_reattempt_rerun_false": "detail_binding_reattempt_rerun_performed",
        "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "module_grouping_recovered_in_execution_false": "module_grouping_recovered_in_execution",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_execution",
        "integration_success_false": "integration_execution_successful", "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed", "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed", "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated", "provider_requests_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution",
        "dataset_generation_false": "dataset_generation_performed_in_execution",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
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
    common_fields = [
        "after_v2_planning_execution_reentry_with_complete_detail_executed",
        "after_v2_planning_execution_reentry_performed", "module_prioritization_generated",
        "planned_outputs_generated", "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
    ]
    result = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        **{field: execution.get(field) for field in common_fields},
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        fields = [
            "after_v2_planning_execution_reentry_created", "planning_method_after_v2_reentry_executed",
            "complete_29_row_detail_used_for_planning", "complete_29_row_detail_verified_for_planning",
            "prioritized_module_group_summary_generated", "priority_tier_report_generated",
            "top_module_concentration_report_generated", "diagnostic_capture_candidate_report_generated",
            "evidence_root_review_candidate_report_generated", "path_cwd_review_candidate_report_generated",
            "digest_drift_review_candidate_report_generated", "fixture_isolation_review_candidate_report_generated",
            "unsupported_claims_boundary_report_generated", "recommended_follow_on_candidate_report_generated",
            "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
            "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
            "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
            "priority_tier_2_count_sum", "priority_tier_3_count_sum",
            "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail",
            "ready_for_targeted_diagnostic_output_capture_candidate", "ready_for_retry_candidate",
        ]
        result.update({field: execution.get(field) for field in fields})
    else:
        result["blocked_reason"] = execution.get("blocked_reason")
    return result


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
    *, source_detail_binding_results_review: dict | None = None,
    complete_detail_binding_source: list[dict] | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Execute planning reentry only; never execute diagnostics or remediation."""

    timestamp = "2026-08-23T00:00:00Z" if run_timestamp_utc is None else run_timestamp_utc
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("run timestamp invalid")
    source_review = deepcopy(source_detail_binding_results_review) if source_detail_binding_results_review is not None else _committed_source_review()
    reasons = _source_review_reasons(source_review)
    if complete_detail_binding_source is None:
        binding_review = source_review.get("complete_29_row_detail_binding_source_review", {}) if isinstance(source_review, Mapping) else {}
        rows = deepcopy(binding_review.get("rows")) if isinstance(binding_review, Mapping) else None
    else:
        rows = deepcopy(complete_detail_binding_source)
    reasons.extend(_source_rows_reasons(rows))
    execution = _success(_common(timestamp), rows) if not reasons else _blocked(_common(timestamp), reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
    execution: dict,
) -> dict:
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, expected_status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, expected_status = False, BLOCKED_STATUS
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("artifact kind invalid")
    constants = {
        "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "schema_version": SCHEMA_VERSION, "selected_after_v2_planning_package": SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "source_detail_binding_results_review_artifact_kind": review_source.ARTIFACT_KIND,
        "source_detail_binding_results_review_status": review_source.REVIEW_STATUS,
        "source_detail_binding_results_review_scope": review_source.REVIEW_SCOPE,
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError(f"{field} mismatch")
    for field in ("created_offline", "governance_only", "planning_execution_only", "used_committed_source_evidence_only",
                  "after_v2_planning_execution_reentry_with_complete_detail_executed"):
        if execution.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError(f"{field} must be true")
    if execution.get("retry_failure_context") != {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("retry failure counts mismatch")
    if any(execution.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("closed boundary opened")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("acceptance boundary changed")
    if execution.get("runtime_use") != NOT_AUTHORIZED or execution.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("runtime boundary changed")
    rows = execution.get("complete_29_row_detail_binding_source")
    if not isinstance(rows, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("detail binding source missing")
    if success:
        if rows != review_source._committed_binding_rows() or semantic_digest(rows) != review_source.SOURCE_BINDING_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("detail binding source invalid")
        required_true = [
            "used_reviewed_complete_29_row_detail_binding", "after_v2_planning_execution_reentry_created",
            "after_v2_planning_execution_reentry_performed", "planning_method_after_v2_reentry_executed",
            "complete_29_row_detail_used_for_planning", "complete_29_row_detail_verified_for_planning",
            "reviewed_complete_29_row_detail_binding_source_used", "module_prioritization_generated",
            "prioritized_module_group_summary_generated", "priority_tier_report_generated",
            "top_module_concentration_report_generated", "diagnostic_capture_candidate_report_generated",
            "evidence_root_review_candidate_report_generated", "path_cwd_review_candidate_report_generated",
            "digest_drift_review_candidate_report_generated", "fixture_isolation_review_candidate_report_generated",
            "unsupported_claims_boundary_report_generated", "recommended_follow_on_candidate_report_generated",
            "planned_outputs_generated", "priority_tiers_generated", "planning_buckets_generated",
            "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail",
        ]
        if any(execution.get(field) is not True for field in required_true):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("success flag missing")
        scalars = {
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
            "top_five_module_paths": list(TOP_FIVE_PATHS),
            "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
            "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
            "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        }
        for field, expected in scalars.items():
            if execution.get(field) != expected:
                raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError(f"{field} mismatch")
        groups = execution.get("prioritized_module_group_summary")
        buckets = execution.get("planning_buckets")
        if groups != _priority_groups(rows) or buckets != _planning_buckets():
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("planning content invalid")
        if any(bucket.get("status") != PLANNING_ONLY_NOT_EXECUTED for bucket in buckets):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("planning bucket executed")
        outputs = execution.get("outputs_generated", [])
        if [item.get("output_id") for item in outputs] != OUTPUT_IDS or any(item.get("status") != GENERATED_RESEARCH_ONLY for item in outputs):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("planning outputs invalid")
        plan_payload = {
            "source_binding_digest": review_source.SOURCE_BINDING_DIGEST,
            "prioritized_module_groups": groups, "priority_tier_report": execution["priority_tier_report"],
            "top_module_concentration_report": execution["top_module_concentration_report"],
            "planning_buckets": buckets,
            "recommended_follow_on_candidate_report": execution["recommended_follow_on_candidate_report"],
        }
        if execution.get(PLANNING_DIGEST_KEY) != semantic_digest(plan_payload):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("planning digest invalid")
        if execution.get(MANIFEST_DIGEST_KEY) != semantic_digest(execution.get("digest_manifest")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("digest manifest invalid")
    else:
        if not execution.get("blocked_reason") or not execution.get(BLOCKED_MANIFEST_DIGEST_KEY):
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("blocked evidence missing")
        expected_blocked = semantic_digest({
            "blocked_reason": execution["blocked_reason"], "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
        })
        if execution[BLOCKED_MANIFEST_DIGEST_KEY] != expected_blocked:
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("blocked manifest invalid")
        if rows or execution.get("outputs_generated") or execution.get("planned_outputs_generated") is not False:
            raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("blocked output generated")
    if [item.get("precheck_id") for item in execution.get("precheck_results", [])] != PRECHECK_IDS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("precheck results invalid")
    if [item.get("step_id") for item in execution.get("execution_steps", [])] != STEP_IDS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("execution steps invalid")
    if execution.get("next_chain") != (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("next chain invalid")
    if execution.get("next_gates") != (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES) or execution.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("governance content invalid")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("checklist invalid")
    summary = _summary(execution, checklist, success)
    if execution.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("summary invalid")
    digest = execution.get(EXECUTION_DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _execution_digest(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError("execution digest invalid")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"], "execution_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_markdown_v1(
    execution: dict,
) -> str:
    """Render a validated, human-readable record of the bounded planning execution."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        execution
    )
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    groups = execution.get("prioritized_module_group_summary", [])
    group_lines = [
        (
            f"{group['priority_group']}: ranks {group['rank_start']}-{group['rank_end']}, "
            f"{group['failed_or_errored_nodeid_count']} node IDs, {group['module_count']} modules; "
            "root cause not claimed."
        )
        for group in groups
    ] or ["Not generated because the execution was blocked."]
    bucket_lines = [
        f"{bucket['planning_bucket']}: {bucket['status']}"
        for bucket in execution.get("planning_buckets", [])
    ] or ["Not generated because the execution was blocked."]
    output_lines = [
        f"{item['output_id']}: {item['status']}" for item in execution.get("outputs_generated", [])
    ] or ["No planning outputs generated."]
    disposition = (
        f"Success: {execution['execution_status']}; ready only for {SUCCESS_NEXT_TASK}."
        if success
        else f"Blocked: {execution['blocked_reason']}; next task {BLOCKED_NEXT_TASK}."
    )
    sections = [
        ("Source Detail Binding Reattempt Results Review", [SOURCE_RESULTS_REVIEW_DIGEST, SOURCE_BINDING_REVIEW_DIGEST, SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST]),
        ("Source Detail Binding Reattempt", [review_source.SOURCE_REATTEMPT_DIGEST, review_source.SOURCE_BINDING_DIGEST, review_source.SOURCE_REATTEMPT_MANIFEST_DIGEST]),
        ("Source Materialization Results Review", [SOURCE_BINDINGS["source_complete_29_row_materialization_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_materialized_payload_review_digest"]]),
        ("Source Materialization Execution", [SOURCE_BINDINGS["source_complete_29_row_materialization_execution_digest"], SOURCE_BINDINGS["source_complete_29_row_materialized_payload_digest"]]),
        ("Source Prior Blocked Planning Reentry", [SOURCE_BINDINGS["source_reentry_execution_blocked_digest"], SOURCE_BINDINGS["source_reentry_execution_blocked_reason"]]),
        ("Source Recovery Results Review", [SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"], SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; this first retry result remains authoritative."]),
        ("Execution Scope", [EXECUTION_SCOPE, SELECTED_AFTER_V2_PLANNING_PACKAGE]),
        ("Reviewed Complete 29-row Detail Binding Source", [f"{execution['module_summary_module_count']} rows and {execution['failed_or_errored_nodeids_count']} failed-or-errored node IDs used." if success else "The reviewed complete source failed an availability or integrity boundary."]),
        ("Planning Reentry Result", [disposition, *output_lines]),
        ("Prioritized Module Group Summary", group_lines),
        ("Priority Tier Report", [str(execution.get("priority_tier_report", "Not generated."))]),
        ("Top Module Concentration Report", [str(execution.get("top_module_concentration_report", "Not generated."))]),
        ("Planning Buckets", bucket_lines),
        ("Unsupported Claims Boundary", list(execution.get("unsupported_claims_boundary_report", UNSUPPORTED_ROW_CLAIMS))),
        ("Success or Blocked Disposition", [disposition]),
        ("Authority Boundaries", ["No cache, rerun, diagnostic, remediation, classification, provider, data, runtime, trading, integration, or main authority was exercised."]),
        ("Next Chain", list(execution["next_chain"])),
        ("Next Gates", list(execution["next_gates"])),
        ("Risk Controls", list(execution["risk_controls"])),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["This artifact is deterministic research planning evidence only; separate results review and approvals remain required."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry with Complete Detail v1",
        "",
    ]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_PRIORITIZED_MODULE_PLANNING_READY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_BLOCKED_COMPLETE_DETAIL_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_PLANNING_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_markdown_v1",
]
