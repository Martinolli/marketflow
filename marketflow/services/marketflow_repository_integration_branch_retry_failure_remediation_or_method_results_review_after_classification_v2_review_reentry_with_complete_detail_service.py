"""Review the committed after-v2 complete-detail planning reentry offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1"
SOURCE_EXECUTION_DIGEST = "846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b"
SOURCE_PLANNING_DIGEST = "ef372ac66b165456241a53fdbe551c51fd4c9bfb65d2b6cdbc366cc464370c60"
SOURCE_MANIFEST_DIGEST = "cb0db6d23e2c206473f154e0ab91e7f098e37fcb524669f7c9a89af0b070ccac"
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_V1"
NEXT_TASK_STATUS = "FUTURE_CANDIDATE_NOT_CREATED"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS"
RECOMMENDATION_REASON = (
    "The after-v2 planning reentry with complete detail has been reviewed and supports creating a separately "
    "governed targeted diagnostic output capture candidate for the highest-priority module groups. Retry "
    "candidate creation remains blocked until diagnostic capture, any required remediation or method review, "
    "and their results reviews are completed."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
GENERATED_RESEARCH_ONLY = "GENERATED_RESEARCH_ONLY"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_digest"
PLANNING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_with_complete_detail_prioritized_module_plan_review_digest"
REVIEW_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_manifest_digest"

OUTPUT_IDS = [
    "remediation_or_method_results_review_after_classification_v2_reentry_with_complete_detail_manifest",
    "source_planning_reentry_execution_summary", "prioritized_planning_digest_review",
    "prioritized_module_group_summary_review", "priority_tier_report_review",
    "top_module_concentration_report_review", "planning_buckets_review",
    "diagnostic_capture_candidate_planning_review", "evidence_root_review_candidate_planning_review",
    "path_cwd_review_candidate_planning_review", "digest_drift_review_candidate_planning_review",
    "fixture_isolation_review_candidate_planning_review", "unsupported_claims_boundary_review",
    "targeted_diagnostic_output_capture_candidate_readiness_report", "digest_manifest",
]

REVIEW_FINDINGS = {
    "finding_1": "The source planning reentry with complete detail completed successfully using the reviewed complete 29-row detail binding.",
    "finding_2": "The source planning reentry is bound by execution digest, prioritized planning digest, and digest-manifest digest.",
    "finding_3": "The planning reentry used exactly 29 module rows totaling 1,404 failed-or-errored node IDs.",
    "finding_4": "The top-five module counts remain 136, 131, 122, 112, and 111.",
    "finding_5": "The top-five sum remains 612 and the top-ten sum remains 1,069.",
    "finding_6": "The priority tier sums remain 612, 457, and 335.",
    "finding_7": "The priority model separates the source into Priority 1, Priority 2, and Priority 3 planning groups only.",
    "finding_8": "All five planning buckets were generated as PLANNING_ONLY_NOT_EXECUTED.",
    "finding_9": "The diagnostic capture candidate report is planning evidence only and did not create or execute a diagnostic candidate.",
    "finding_10": "This results review did not read cache, rerun planning, rerun detail binding, rerun materialization, rerun source recovery, run pytest, run retry, execute diagnostics, execute remediation, or execute classification.",
    "finding_11": "The reviewed planning output supports a separately invoked targeted diagnostic output capture candidate for top module groups.",
    "finding_12": "The reviewed planning output does not support retry-candidate readiness yet.",
    "finding_13": "The reviewed planning output remains planning evidence only and does not prove failure/error separation, first failure, first error, traceback root cause, retry success, or main-merge readiness.",
}

NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1.",
    "Targeted Diagnostic Output Capture Candidate Operator Review v1.",
    "Targeted Diagnostic Output Capture Approval v1, if selected.",
    "Targeted Diagnostic Output Capture Execution v1, if approved.",
    "Targeted Diagnostic Output Capture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if needed.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]

NEXT_GATES = [
    "targeted_diagnostic_output_capture_candidate_for_top_module_groups",
    "targeted_diagnostic_output_capture_candidate_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_needed",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "review_after_v2_planning_reentry_with_complete_detail_does_not_read_cache",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_modify_cache",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_rerun_planning",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_rerun_detail_binding",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_rerun_materialization",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_rerun_source_recovery",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_run_pytest",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_rerun_retry",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_run_diagnostic_commands",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_execute_diagnostics",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_execute_remediation",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_execute_classification",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_classify_modules_again",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_targeted_diagnostic_candidate",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_diagnostic_operator_review",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_diagnostic_approval",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_execute_diagnostic_capture",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_diagnostic_results_review",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_new_retry_candidate",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_retry_results_review",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_create_integration_results_review",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_mark_integration_successful",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_generate_successful_integration_digest",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_claim_failure_error_separation",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_claim_first_failure",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_claim_first_error",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_claim_traceback_root_cause",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_recommend_direct_code_remediation",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_treat_planning_as_retry_success",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_push_integration_branch",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_push_main",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_delete_integration_branch",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_delete_worktree",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_force_push",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_prune_remotes",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_modify_tags",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_modify_staged_evidence",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_regenerate_evidence",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_call_providers",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_acquire_market_data",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_regenerate_dataset",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_recompute_metrics",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_train_models",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_score_strategy",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_generate_recommendations",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_accept_predictive_usefulness",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_accept_profitability",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_authorize_runtime",
    "review_after_v2_planning_reentry_with_complete_detail_does_not_authorize_broker_execution",
    "planning_review_output_is_research_planning_only_not_root_cause", "planning_review_output_is_not_retry_success",
    "diagnostic_candidate_readiness_is_not_diagnostic_execution", "targeted_diagnostic_candidate_must_be_separately_created",
    "targeted_diagnostic_capture_requires_separate_operator_review_and_approval",
    "new_retry_requires_separate_candidate_approval_execution_and_review",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_reentry_execution_remains_historically_blocked",
    "previous_detail_binding_results_review_remains_valid", "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_created",
    "remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_ready",
    "source_planning_reentry_with_complete_detail_reviewed", "source_planning_reentry_digest_verified",
    "source_prioritized_planning_digest_verified", "source_planning_digest_manifest_verified",
    "reviewed_complete_29_row_detail_used_for_planning", "prioritized_module_group_summary_reviewed",
    "priority_tier_report_reviewed", "top_module_concentration_report_reviewed", "planning_buckets_reviewed",
    "diagnostic_capture_planning_reviewed", "evidence_root_review_planning_reviewed",
    "path_cwd_review_planning_reviewed", "digest_drift_review_planning_reviewed",
    "fixture_isolation_review_planning_reviewed", "unsupported_claims_boundary_reviewed",
    "ready_for_targeted_diagnostic_output_capture_candidate",
]

FALSE_FIELDS = [
    "ready_for_retry_candidate", "targeted_diagnostic_output_capture_candidate_created",
    "diagnostic_capture_operator_review_created", "diagnostic_capture_approval_created",
    "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "cache_read_in_review", "cache_modified_in_review",
    "planning_reentry_rerun_performed", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "module_grouping_recovered_in_review", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_review", "failure_modules_classified", "error_modules_classified",
    "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
    "first_order_claim_made", "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]

SOURCE_BINDINGS = deepcopy(source.SOURCE_BINDINGS)


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError(ValueError):
    """Raised when source planning evidence or its review violates the contract."""


def _committed_rows() -> list[dict[str, Any]]:
    return source.review_source._committed_binding_rows()


def _priority_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("PRIORITY_1_TOP_5_MODULE_GROUPS", 1, 5, 612, "highest-priority diagnostic-output capture and planning review group"),
        ("PRIORITY_2_NEXT_5_MODULE_GROUPS", 6, 10, 457, "secondary diagnostic planning group"),
        ("PRIORITY_3_REMAINING_MODULE_GROUPS", 11, 29, 335, "coverage and systemic review planning group"),
    ]
    return [
        {
            "priority_group": group, "rank_start": start, "rank_end": end,
            "module_count": len(rows[start - 1:end]), "failed_or_errored_nodeid_count": total,
            "purpose": purpose, "root_cause_claimed": False,
            "module_paths": [row["module_path"] for row in rows[start - 1:end]],
        }
        for group, start, end, total, purpose in specs
    ]


def _planning_buckets() -> list[dict[str, Any]]:
    purposes = [
        "Plan bounded diagnostic-output capture for the highest-priority groups.",
        "Plan review of evidence-root requirements without inspecting evidence roots.",
        "Plan review of path and working-directory assumptions without diagnostic execution.",
        "Plan review of digest constant drift without changing digests or evidence.",
        "Plan review of fixture isolation without executing or modifying fixtures.",
    ]
    return [
        {"planning_bucket": bucket, "status": source.PLANNING_ONLY_NOT_EXECUTED, "purpose": purpose,
         "diagnostic_executed": False, "remediation_executed": False, "root_cause_claimed": False}
        for bucket, purpose in zip(source.PLANNING_BUCKETS, purposes, strict=True)
    ]


def _source_structures() -> dict[str, Any]:
    rows = _committed_rows()
    groups = _priority_groups(rows)
    buckets = _planning_buckets()
    tier_report = {
        "priority_tiers_generated": True, "planning_only": True,
        "priority_tier_1": groups[0], "priority_tier_2": groups[1], "priority_tier_3": groups[2],
    }
    concentration = {
        "top_five_module_paths": [row["module_path"] for row in rows[:5]],
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "root_cause_claimed": False,
    }
    follow_on = {
        "recommended_next_task": source.SUCCESS_NEXT_TASK,
        "status": "FUTURE_RESULTS_REVIEW_NOT_CREATED", "ready_for_results_review": True,
        "ready_for_targeted_diagnostic_output_capture_candidate": False, "ready_for_retry_candidate": False,
    }
    return {
        "rows": rows, "groups": groups, "buckets": buckets, "tier_report": tier_report,
        "concentration": concentration, "follow_on": follow_on,
        "bucket_reports": {
            "diagnostic_capture_candidate_planning_report": buckets[0],
            "evidence_root_review_candidate_planning_report": buckets[1],
            "path_cwd_review_candidate_planning_report": buckets[2],
            "digest_drift_review_candidate_planning_report": buckets[3],
            "fixture_isolation_review_candidate_planning_report": buckets[4],
        },
    }


def _committed_source_execution() -> dict[str, Any]:
    structures = _source_structures()
    return {
        "artifact_kind": source.SUCCESS_ARTIFACT_KIND, "execution_status": source.SUCCESS_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        source.EXECUTION_DIGEST_KEY: SOURCE_EXECUTION_DIGEST,
        source.PLANNING_DIGEST_KEY: SOURCE_PLANNING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_MANIFEST_DIGEST,
        "selected_after_v2_planning_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
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
        "top_five_module_paths": list(source.TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335, "priority_tiers_generated": True,
        "planning_buckets_generated": True,
        "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail": True,
        "ready_for_targeted_diagnostic_output_capture_candidate": False, "ready_for_retry_candidate": False,
        "complete_29_row_detail_binding_source": structures["rows"],
        "prioritized_module_group_summary": structures["groups"],
        "priority_tier_report": structures["tier_report"],
        "top_module_concentration_report": structures["concentration"],
        "planning_buckets": structures["buckets"],
        **structures["bucket_reports"],
        "unsupported_claims_boundary_report": list(source.UNSUPPORTED_ROW_CLAIMS),
        "recommended_follow_on_candidate_report": structures["follow_on"],
        "outputs_generated": [
            {"output_id": output_id, "status": source.GENERATED_RESEARCH_ONLY}
            for output_id in source.OUTPUT_IDS
        ],
    }


def _source_reasons(execution: Any) -> list[str]:
    if not isinstance(execution, Mapping):
        return ["SOURCE_PLANNING_REENTRY_EXECUTION_UNAVAILABLE"]
    expected = _committed_source_execution()
    fields = [
        "artifact_kind", "execution_status", "execution_scope", source.EXECUTION_DIGEST_KEY,
        source.PLANNING_DIGEST_KEY, source.MANIFEST_DIGEST_KEY, "selected_after_v2_planning_package",
        *SOURCE_BINDINGS, "retry_execution_commit", "retry_failure_context",
        "after_v2_planning_execution_reentry_with_complete_detail_executed",
        "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
        "planning_method_after_v2_reentry_executed", "complete_29_row_detail_used_for_planning",
        "complete_29_row_detail_verified_for_planning", "reviewed_complete_29_row_detail_binding_source_used",
        "module_prioritization_generated", "prioritized_module_group_summary_generated",
        "priority_tier_report_generated", "top_module_concentration_report_generated",
        "diagnostic_capture_candidate_report_generated", "evidence_root_review_candidate_report_generated",
        "path_cwd_review_candidate_report_generated", "digest_drift_review_candidate_report_generated",
        "fixture_isolation_review_candidate_report_generated", "unsupported_claims_boundary_report_generated",
        "recommended_follow_on_candidate_report_generated", "planned_outputs_generated",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "largest_module_nodeid_counts",
        "top_five_module_paths", "top_5_count_sum", "top_5_percentage_of_failed_or_errored_nodeids",
        "top_10_count_sum", "top_10_percentage_of_failed_or_errored_nodeids",
        "priority_tier_1_count_sum", "priority_tier_2_count_sum", "priority_tier_3_count_sum",
        "priority_tiers_generated", "planning_buckets_generated",
        "ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail",
        "ready_for_targeted_diagnostic_output_capture_candidate", "ready_for_retry_candidate",
        "complete_29_row_detail_binding_source", "prioritized_module_group_summary", "priority_tier_report",
        "top_module_concentration_report", "planning_buckets", "diagnostic_capture_candidate_planning_report",
        "evidence_root_review_candidate_planning_report", "path_cwd_review_candidate_planning_report",
        "digest_drift_review_candidate_planning_report", "fixture_isolation_review_candidate_planning_report",
        "unsupported_claims_boundary_report", "recommended_follow_on_candidate_report", "outputs_generated",
    ]
    return [
        f"SOURCE_PLANNING_REENTRY_{field.upper()}_MISMATCH_OR_MISSING"
        for field in fields if execution.get(field) != expected[field]
    ]


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_planning_reentry_execution_digest_bound": (SOURCE_EXECUTION_DIGEST, review.get("source_planning_reentry_execution_digest")),
        "source_prioritized_planning_digest_bound": (SOURCE_PLANNING_DIGEST, review.get("source_prioritized_planning_digest")),
        "source_planning_digest_manifest_digest_bound": (SOURCE_MANIFEST_DIGEST, review.get("source_planning_digest_manifest_digest")),
        "source_selected_after_v2_planning_package_bound": (source.SELECTED_AFTER_V2_PLANNING_PACKAGE, review.get("selected_after_v2_planning_package")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        "source_planning_reentry_success_status_bound": (source.SUCCESS_STATUS, review.get("source_planning_reentry_status")),
        "source_complete_detail_used_for_planning_true": (True, review.get("source_planning_reentry_summary", {}).get("complete_29_row_detail_used_for_planning")),
        "source_module_prioritization_generated_true": (True, review.get("source_planning_reentry_summary", {}).get("module_prioritization_generated")),
        "source_priority_tier_report_generated_true": (True, review.get("source_planning_reentry_summary", {}).get("priority_tier_report_generated")),
        "source_top_module_concentration_report_generated_true": (True, review.get("source_planning_reentry_summary", {}).get("top_module_concentration_report_generated")),
        "source_planning_buckets_generated_true": (True, review.get("source_planning_reentry_summary", {}).get("planning_buckets_generated")),
        "source_planned_outputs_generated_true": (True, review.get("source_planning_reentry_summary", {}).get("planned_outputs_generated")),
        "module_summary_module_count_29": (29, review.get("module_summary_module_count")),
        "failed_or_errored_nodeids_1404": (1404, review.get("failed_or_errored_nodeids_count")),
        "largest_module_counts_verified": ([136, 131, 122, 112, 111], review.get("largest_module_nodeid_counts")),
        "top_five_paths_preserved": (source.TOP_FIVE_PATHS, review.get("top_five_module_paths")),
        "top_five_sum_612": (612, review.get("top_5_count_sum")),
        "top_ten_sum_1069": (1069, review.get("top_10_count_sum")),
        "tier_1_sum_612": (612, review.get("priority_tier_1_count_sum")),
        "tier_2_sum_457": (457, review.get("priority_tier_2_count_sum")),
        "tier_3_sum_335": (335, review.get("priority_tier_3_count_sum")),
        "review_outputs_generated": (OUTPUT_IDS, [item.get("output_id") for item in review.get("review_outputs", [])]),
        "recommendation_defined": (RECOMMENDED_ACTION, review.get("recommended_action")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
    }
    source_checks = {
        "source_detail_binding_results_review_digest_bound": "source_detail_binding_reattempt_results_review_digest",
        "source_complete_29_row_binding_review_digest_bound": "source_complete_29_row_binding_review_digest",
        "source_detail_binding_results_review_manifest_digest_bound": "source_detail_binding_reattempt_results_review_manifest_digest",
        "source_detail_binding_reattempt_digest_bound": "source_detail_binding_reattempt_digest",
        "source_complete_29_row_binding_digest_bound": "source_complete_29_row_binding_digest",
        "source_detail_binding_reattempt_manifest_digest_bound": "source_detail_binding_reattempt_digest_manifest_digest",
        "source_materialization_results_review_digest_bound": "source_complete_29_row_materialization_results_review_digest",
        "source_materialized_payload_review_digest_bound": "source_complete_29_row_materialized_payload_review_digest",
        "source_materialization_results_review_manifest_digest_bound": "source_complete_29_row_materialization_results_review_manifest_digest",
        "source_materialization_execution_digest_bound": "source_complete_29_row_materialization_execution_digest",
        "source_materialized_payload_digest_bound": "source_complete_29_row_materialized_payload_digest",
        "source_materialization_digest_manifest_digest_bound": "source_complete_29_row_materialization_digest_manifest_digest",
        "source_detail_binding_approval_digest_bound": "source_detail_exposure_or_binding_approval_digest",
        "source_prior_blocked_detail_binding_execution_digest_bound": "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_prior_blocked_detail_binding_reason_bound": "source_detail_exposure_or_binding_execution_blocked_reason",
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
    values.update({check_id: (SOURCE_BINDINGS[field], review.get(field)) for check_id, field in source_checks.items()})
    true_checks = {
        "review_created_true": TRUE_FIELDS[0], "review_ready_true": TRUE_FIELDS[1],
        "source_planning_reentry_reviewed_true": "source_planning_reentry_with_complete_detail_reviewed",
        "source_planning_reentry_digest_verified_true": "source_planning_reentry_digest_verified",
        "source_prioritized_planning_digest_verified_true": "source_prioritized_planning_digest_verified",
        "source_planning_digest_manifest_verified_true": "source_planning_digest_manifest_verified",
        "complete_29_row_detail_used_for_planning_reviewed_true": "reviewed_complete_29_row_detail_used_for_planning",
        "prioritized_module_group_summary_reviewed_true": "prioritized_module_group_summary_reviewed",
        "priority_tier_report_reviewed_true": "priority_tier_report_reviewed",
        "top_module_concentration_reviewed_true": "top_module_concentration_report_reviewed",
        "planning_buckets_reviewed_true": "planning_buckets_reviewed",
        "diagnostic_capture_planning_reviewed_true": "diagnostic_capture_planning_reviewed",
        "evidence_root_review_planning_reviewed_true": "evidence_root_review_planning_reviewed",
        "path_cwd_review_planning_reviewed_true": "path_cwd_review_planning_reviewed",
        "digest_drift_review_planning_reviewed_true": "digest_drift_review_planning_reviewed",
        "fixture_isolation_review_planning_reviewed_true": "fixture_isolation_review_planning_reviewed",
        "unsupported_claims_boundary_reviewed_true": "unsupported_claims_boundary_reviewed",
        "ready_for_targeted_diagnostic_output_capture_candidate_true": "ready_for_targeted_diagnostic_output_capture_candidate",
    }
    values.update({check_id: (True, review.get(field)) for check_id, field in true_checks.items()})
    false_checks = {f"{field}_false": field for field in FALSE_FIELDS}
    renames = {
        "targeted_diagnostic_output_capture_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "planning_reentry_rerun_false": "planning_reentry_rerun_performed",
        "detail_binding_reattempt_rerun_false": "detail_binding_reattempt_rerun_performed",
        "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_review",
        "integration_success_false": "integration_execution_successful", "provider_requests_false": "provider_requests_made_in_review",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_false": "dataset_generation_performed_in_review",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    false_checks.update(renames)
    values.update({check_id: (False, review.get(field)) for check_id, field in false_checks.items()})
    values["successful_integration_digest_false"] = ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")])
    values["predictive_usefulness_not_accepted"] = (NOT_ACCEPTED, review.get("predictive_usefulness"))
    values["profitability_not_accepted"] = (NOT_ACCEPTED, review.get("profitability"))
    values["runtime_not_authorized"] = (NOT_AUTHORIZED, review.get("runtime_use"))
    values["broker_not_authorized"] = (NOT_AUTHORIZED, review.get("broker_execution"))
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    fields = [
        *TRUE_FIELDS[:11], "ready_for_targeted_diagnostic_output_capture_candidate", "ready_for_retry_candidate",
        "targeted_diagnostic_output_capture_candidate_created", "diagnostic_capture_execution_performed",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
        "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
        "priority_tier_2_count_sum", "priority_tier_3_count_sum",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        **{field: review.get(field) for field in fields},
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", REVIEW_DIGEST_KEY, "review_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
    *, source_execution: dict | None = None,
) -> dict:
    """Review committed planning evidence without invoking its execution path."""

    execution = deepcopy(source_execution) if source_execution is not None else _committed_source_execution()
    reasons = _source_reasons(execution)
    if reasons:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError(";".join(reasons))
    rows = deepcopy(execution["complete_29_row_detail_binding_source"])
    groups = deepcopy(execution["prioritized_module_group_summary"])
    tiers = deepcopy(execution["priority_tier_report"])
    concentration = deepcopy(execution["top_module_concentration_report"])
    buckets = deepcopy(execution["planning_buckets"])
    source_summary = {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "after_v2_planning_execution_reentry_with_complete_detail_executed": True,
        "after_v2_planning_execution_reentry_performed": True,
        "planning_method_after_v2_reentry_executed": True,
        "complete_29_row_detail_used_for_planning": True,
        "complete_29_row_detail_verified_for_planning": True,
        "module_prioritization_generated": True, "priority_tier_report_generated": True,
        "top_module_concentration_report_generated": True, "planning_buckets_generated": True,
        "planned_outputs_generated": True, "ready_for_results_review": True,
        "ready_for_targeted_diagnostic_output_capture_candidate": False, "ready_for_retry_candidate": False,
    }
    binding_results_summary = {
        "results_review_digest": SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"],
        "binding_review_digest": SOURCE_BINDINGS["source_complete_29_row_binding_review_digest"],
        "results_review_manifest_digest": SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_manifest_digest"],
        "binding_digest": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
        "reviewed_complete_29_row_detail_binding_source": True,
    }
    detail_summary = {
        "reviewed": True, "row_count": len(rows),
        "failed_or_errored_nodeids_count": sum(row["failed_or_errored_nodeid_count"] for row in rows),
        "source_binding_digest": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
        "used_for_planning": True, "rows": rows,
    }
    planning_digest_review = {
        "reviewed": True,
        "execution_digest": {"expected": SOURCE_EXECUTION_DIGEST, "actual": execution[source.EXECUTION_DIGEST_KEY], "verified": True},
        "prioritized_planning_digest": {"expected": SOURCE_PLANNING_DIGEST, "actual": execution[source.PLANNING_DIGEST_KEY], "verified": True},
        "digest_manifest_digest": {"expected": SOURCE_MANIFEST_DIGEST, "actual": execution[source.MANIFEST_DIGEST_KEY], "verified": True},
    }
    groups_review = {
        "reviewed": True, "planning_only": True, "priority_group_count": 3,
        "module_count": 29, "failed_or_errored_nodeid_count": 1404,
        "root_cause_claimed": False, "priority_groups": groups,
    }
    tiers_review = {
        "reviewed": True, "planning_only": True,
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335, "source_report": tiers,
    }
    concentration_review = {
        "reviewed": True, "root_cause_claimed": False,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "source_report": concentration,
    }
    buckets_review = {
        "reviewed": True, "planning_only": True, "bucket_count": 5,
        "all_planning_only_not_executed": all(
            bucket["status"] == source.PLANNING_ONLY_NOT_EXECUTED for bucket in buckets
        ),
        "planning_buckets": buckets,
    }
    planning_reviews = {
        "diagnostic_capture_planning_review": {
            "reviewed": True, "planning_bucket": buckets[0], "candidate_created": False,
            "diagnostic_executed": False, "remediation_executed": False,
        },
        "evidence_root_review_planning_review": {"reviewed": True, "planning_bucket": buckets[1], "executed": False},
        "path_cwd_review_planning_review": {"reviewed": True, "planning_bucket": buckets[2], "executed": False},
        "digest_drift_review_planning_review": {"reviewed": True, "planning_bucket": buckets[3], "executed": False},
        "fixture_isolation_review_planning_review": {"reviewed": True, "planning_bucket": buckets[4], "executed": False},
    }
    unsupported_review = {
        "reviewed": True, "required_unsupported_claims": list(source.UNSUPPORTED_ROW_CLAIMS),
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "traceback_root_cause_claimed": False,
        "direct_code_remediation_recommended": False, "retry_success_claimed": False,
        "main_merge_readiness_claimed": False,
    }
    recommendation = {
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "ready_for_targeted_diagnostic_output_capture_candidate": True,
        "ready_for_retry_candidate": False, "reason": RECOMMENDATION_REASON,
    }
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_planning_reentry_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_planning_reentry_status": source.SUCCESS_STATUS,
        "source_planning_reentry_scope": source.EXECUTION_SCOPE,
        "source_planning_reentry_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_prioritized_planning_digest": SOURCE_PLANNING_DIGEST,
        "source_planning_digest_manifest_digest": SOURCE_MANIFEST_DIGEST,
        "selected_after_v2_planning_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": execution["retry_execution_commit"],
        "retry_failure_context": deepcopy(execution["retry_failure_context"]),
        "source_planning_reentry_summary": source_summary,
        "source_detail_binding_results_review_summary": binding_results_summary,
        "reviewed_complete_29_row_detail_binding_summary": detail_summary,
        "planning_digest_review": planning_digest_review,
        "prioritized_module_group_summary_review": groups_review,
        "priority_tier_report_review": tiers_review,
        "top_module_concentration_report_review": concentration_review,
        "planning_buckets_review": buckets_review,
        **planning_reviews,
        "unsupported_claims_boundary_review": unsupported_review,
        "review_findings": deepcopy(REVIEW_FINDINGS),
        "review_outputs": [{"output_id": output_id, "status": GENERATED_RESEARCH_ONLY} for output_id in OUTPUT_IDS],
        "recommendation": recommendation, "recommended_next_task": NEXT_TASK,
        "recommended_next_task_status": NEXT_TASK_STATUS, "recommended_action": RECOMMENDED_ACTION,
        "reason": RECOMMENDATION_REASON, "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    planning_review_payload = {
        "source_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_prioritized_planning_digest": SOURCE_PLANNING_DIGEST,
        "source_manifest_digest": SOURCE_MANIFEST_DIGEST,
        "planning_digest_review": planning_digest_review,
        "prioritized_module_group_summary_review": groups_review,
        "priority_tier_report_review": tiers_review,
        "top_module_concentration_report_review": concentration_review,
        "planning_buckets_review": buckets_review,
        **planning_reviews,
        "unsupported_claims_boundary_review": unsupported_review,
    }
    review[PLANNING_REVIEW_DIGEST_KEY] = semantic_digest(planning_review_payload)
    review["prioritized_planning_review_digest"] = review[PLANNING_REVIEW_DIGEST_KEY]
    review["digest_manifest"] = {
        "source_planning_reentry_execution": SOURCE_EXECUTION_DIGEST,
        "source_prioritized_planning": SOURCE_PLANNING_DIGEST,
        "source_planning_manifest": SOURCE_MANIFEST_DIGEST,
        "source_detail_binding_results_review": SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"],
        "source_complete_29_row_binding": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
        "prioritized_planning_review": review[PLANNING_REVIEW_DIGEST_KEY],
        "review_findings": semantic_digest(REVIEW_FINDINGS), "recommendation": semantic_digest(recommendation),
        "review_outputs": semantic_digest(review["review_outputs"]),
    }
    review[REVIEW_MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["review_manifest_digest"] = review[REVIEW_MANIFEST_DIGEST_KEY]
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review[REVIEW_DIGEST_KEY] = _review_digest(review)
    review["review_digest"] = review[REVIEW_DIGEST_KEY]
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
    review: dict,
) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_planning_reentry_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_planning_reentry_status": source.SUCCESS_STATUS,
        "source_planning_reentry_scope": source.EXECUTION_SCOPE,
        "source_planning_reentry_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_prioritized_planning_digest": SOURCE_PLANNING_DIGEST,
        "source_planning_digest_manifest_digest": SOURCE_MANIFEST_DIGEST,
        "selected_after_v2_planning_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError(f"{field} mismatch")
    if review.get("retry_failure_context") != {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("retry failure counts mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("required review flag missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("closed boundary opened")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("acceptance boundary changed")
    if review.get("runtime_use") != NOT_AUTHORIZED or review.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("runtime boundary changed")
    expected_source = _committed_source_execution()
    source_summary = review.get("source_planning_reentry_summary")
    expected_source_summary = {
        "artifact_kind": source.SUCCESS_ARTIFACT_KIND, "execution_status": source.SUCCESS_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "after_v2_planning_execution_reentry_with_complete_detail_executed": True,
        "after_v2_planning_execution_reentry_performed": True, "planning_method_after_v2_reentry_executed": True,
        "complete_29_row_detail_used_for_planning": True, "complete_29_row_detail_verified_for_planning": True,
        "module_prioritization_generated": True, "priority_tier_report_generated": True,
        "top_module_concentration_report_generated": True, "planning_buckets_generated": True,
        "planned_outputs_generated": True, "ready_for_results_review": True,
        "ready_for_targeted_diagnostic_output_capture_candidate": False, "ready_for_retry_candidate": False,
    }
    if source_summary != expected_source_summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("source planning summary invalid")
    detail_summary = review.get("reviewed_complete_29_row_detail_binding_summary")
    if not isinstance(detail_summary, Mapping) or detail_summary.get("rows") != expected_source["complete_29_row_detail_binding_source"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("reviewed complete detail summary invalid")
    rows = detail_summary["rows"]
    if len(rows) != 29 or sum(row.get("failed_or_errored_nodeid_count", 0) for row in rows) != 1404:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("reviewed complete detail counts invalid")
    if semantic_digest(rows) != SOURCE_BINDINGS["source_complete_29_row_binding_digest"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("reviewed complete detail digest invalid")
    scalars = {
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
    }
    for field, expected in scalars.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError(f"{field} mismatch")
    digest_review = review.get("planning_digest_review")
    expected_digest_review = {
        "reviewed": True,
        "execution_digest": {"expected": SOURCE_EXECUTION_DIGEST, "actual": SOURCE_EXECUTION_DIGEST, "verified": True},
        "prioritized_planning_digest": {"expected": SOURCE_PLANNING_DIGEST, "actual": SOURCE_PLANNING_DIGEST, "verified": True},
        "digest_manifest_digest": {"expected": SOURCE_MANIFEST_DIGEST, "actual": SOURCE_MANIFEST_DIGEST, "verified": True},
    }
    if digest_review != expected_digest_review:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("planning digest review invalid")
    structures = _source_structures()
    groups_review = review.get("prioritized_module_group_summary_review")
    if not isinstance(groups_review, Mapping) or groups_review.get("priority_groups") != structures["groups"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("prioritized module review invalid")
    if groups_review.get("reviewed") is not True or groups_review.get("root_cause_claimed") is not False:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("prioritized module review boundary invalid")
    tiers_review = review.get("priority_tier_report_review")
    if not isinstance(tiers_review, Mapping) or tiers_review.get("source_report") != structures["tier_report"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("priority tier review invalid")
    concentration_review = review.get("top_module_concentration_report_review")
    if not isinstance(concentration_review, Mapping) or concentration_review.get("source_report") != structures["concentration"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("concentration review invalid")
    buckets_review = review.get("planning_buckets_review")
    if not isinstance(buckets_review, Mapping) or buckets_review.get("planning_buckets") != structures["buckets"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("planning buckets review invalid")
    if buckets_review.get("all_planning_only_not_executed") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("planning bucket execution boundary invalid")
    planning_review_fields = [
        "diagnostic_capture_planning_review", "evidence_root_review_planning_review",
        "path_cwd_review_planning_review", "digest_drift_review_planning_review",
        "fixture_isolation_review_planning_review",
    ]
    for index, field in enumerate(planning_review_fields):
        item = review.get(field)
        if not isinstance(item, Mapping) or item.get("reviewed") is not True or item.get("planning_bucket") != structures["buckets"][index]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError(f"{field} invalid")
    diagnostic_review = review["diagnostic_capture_planning_review"]
    if diagnostic_review.get("candidate_created") is not False or diagnostic_review.get("diagnostic_executed") is not False:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("diagnostic planning boundary invalid")
    unsupported = review.get("unsupported_claims_boundary_review")
    if not isinstance(unsupported, Mapping) or unsupported.get("required_unsupported_claims") != source.UNSUPPORTED_ROW_CLAIMS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("unsupported claims review invalid")
    unsupported_false = [
        "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
        "traceback_root_cause_claimed", "direct_code_remediation_recommended",
        "retry_success_claimed", "main_merge_readiness_claimed",
    ]
    if any(unsupported.get(field) is not False for field in unsupported_false):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("unsupported claim opened")
    if review.get("review_findings") != REVIEW_FINDINGS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review findings invalid")
    outputs = review.get("review_outputs", [])
    if [item.get("output_id") for item in outputs] != OUTPUT_IDS or any(item.get("status") != GENERATED_RESEARCH_ONLY for item in outputs):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review outputs invalid")
    recommendation = review.get("recommendation")
    expected_recommendation = {
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION, "ready_for_targeted_diagnostic_output_capture_candidate": True,
        "ready_for_retry_candidate": False, "reason": RECOMMENDATION_REASON,
    }
    if recommendation != expected_recommendation or review.get("recommended_next_task") != NEXT_TASK:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("recommendation invalid")
    if review.get("recommended_action") != RECOMMENDED_ACTION or review.get("reason") != RECOMMENDATION_REASON:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("recommendation fields invalid")
    if review.get("next_chain") != NEXT_CHAIN or review.get("next_gates") != NEXT_GATES or review.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("governance content invalid")
    planning_review_payload = {
        "source_execution_digest": SOURCE_EXECUTION_DIGEST, "source_prioritized_planning_digest": SOURCE_PLANNING_DIGEST,
        "source_manifest_digest": SOURCE_MANIFEST_DIGEST, "planning_digest_review": digest_review,
        "prioritized_module_group_summary_review": groups_review, "priority_tier_report_review": tiers_review,
        "top_module_concentration_report_review": concentration_review, "planning_buckets_review": buckets_review,
        **{field: review[field] for field in planning_review_fields},
        "unsupported_claims_boundary_review": unsupported,
    }
    planning_review_digest = semantic_digest(planning_review_payload)
    if review.get(PLANNING_REVIEW_DIGEST_KEY) != planning_review_digest or review.get("prioritized_planning_review_digest") != planning_review_digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("planning review digest invalid")
    expected_manifest = {
        "source_planning_reentry_execution": SOURCE_EXECUTION_DIGEST,
        "source_prioritized_planning": SOURCE_PLANNING_DIGEST, "source_planning_manifest": SOURCE_MANIFEST_DIGEST,
        "source_detail_binding_results_review": SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"],
        "source_complete_29_row_binding": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
        "prioritized_planning_review": planning_review_digest,
        "review_findings": semantic_digest(REVIEW_FINDINGS), "recommendation": semantic_digest(expected_recommendation),
        "review_outputs": semantic_digest(outputs),
    }
    if review.get("digest_manifest") != expected_manifest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("digest manifest invalid")
    manifest_digest = semantic_digest(expected_manifest)
    if review.get(REVIEW_MANIFEST_DIGEST_KEY) != manifest_digest or review.get("review_manifest_digest") != manifest_digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review manifest digest invalid")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("checklist invalid")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("summary invalid")
    digest = review.get(REVIEW_DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _review_digest(review):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review digest invalid")
    if review.get("review_digest") != digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("review digest alias invalid")
    return {
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"], "review_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
        source_execution=source_execution
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_digest": review[REVIEW_DIGEST_KEY],
        "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(review)
    groups = review["prioritized_module_group_summary_review"]["priority_groups"]
    group_lines = [
        f"{item['priority_group']}: ranks {item['rank_start']}-{item['rank_end']}, {item['module_count']} modules, {item['failed_or_errored_nodeid_count']} node IDs."
        for item in groups
    ]
    bucket_lines = [
        f"{item['planning_bucket']}: {item['status']}"
        for item in review["planning_buckets_review"]["planning_buckets"]
    ]
    sections = [
        ("Source Planning Reentry with Complete Detail", [SOURCE_EXECUTION_DIGEST, SOURCE_PLANNING_DIGEST, SOURCE_MANIFEST_DIGEST, source.SUCCESS_STATUS]),
        ("Source Detail Binding Reattempt Results Review", [SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_binding_review_digest"]]),
        ("Source Materialization Results Review", [SOURCE_BINDINGS["source_complete_29_row_materialization_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_materialized_payload_review_digest"]]),
        ("Source Detail Exposure or Binding Approval", [SOURCE_BINDINGS["source_detail_exposure_or_binding_approval_digest"]]),
        ("Source Prior Blocked Planning Reentry", [SOURCE_BINDINGS["source_reentry_execution_blocked_digest"], SOURCE_BINDINGS["source_reentry_execution_blocked_reason"]]),
        ("Source Recovery Results Review", [SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"], SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the first retry result remains authoritative."]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Reviewed Complete 29-row Planning Source", ["29 module rows and 1,404 failed-or-errored node IDs were reviewed from committed planning evidence."]),
        ("Planning Digest Review", [str(review["planning_digest_review"])]),
        ("Prioritized Module Group Summary Review", group_lines),
        ("Priority Tier Report Review", [str(review["priority_tier_report_review"])]),
        ("Top Module Concentration Review", [str(review["top_module_concentration_report_review"])]),
        ("Planning Buckets Review", bucket_lines),
        ("Diagnostic Capture Planning Review", [str(review["diagnostic_capture_planning_review"])]),
        ("Unsupported Claims Boundary", list(source.UNSUPPORTED_ROW_CLAIMS)),
        ("Review Findings", list(review["review_findings"].values())),
        ("Recommendation", [RECOMMENDED_ACTION, RECOMMENDATION_REASON]),
        ("Next Chain", list(review["next_chain"])), ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["Candidate readiness is not candidate creation or diagnostic execution; retry, integration, main, provider, data, runtime, and trading authority remain closed."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Only a separately invoked targeted diagnostic output capture candidate is prepared; no candidate was created by this review."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Results Review After Classification v2 Review Reentry with Complete Detail v1",
        "",
    ]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_markdown_v1",
]
