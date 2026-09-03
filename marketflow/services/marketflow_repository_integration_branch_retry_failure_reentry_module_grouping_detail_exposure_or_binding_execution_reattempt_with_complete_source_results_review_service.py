"""Review the committed complete-source detail-binding reattempt offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_MATERIALIZATION_RERUN_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1"
SOURCE_REATTEMPT_DIGEST = "c792e68906e8a84fbc5f47bb6df42c52d682502c188212c5800bc559a06367ab"
SOURCE_BINDING_DIGEST = "36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7"
SOURCE_REATTEMPT_MANIFEST_DIGEST = "f25138ceadf57629db4ff8ebb76ab146188140d33ea681ab9496b2c168951500"
SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE = source.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1"
NEXT_TASK_STATUS = "FUTURE_REENTRY_NOT_CREATED"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_AFTER_V2_PLANNING_REENTRY_USING_REVIEWED_COMPLETE_29_ROW_DETAIL_BINDING"
RECOMMENDATION_REASON = (
    "The complete 29-row detail binding has been reviewed and is ready to support a separately governed "
    "after-v2 planning reentry. Retry candidate creation remains blocked until planning reentry and its own "
    "review determine the next controlled diagnostic or remediation path."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_MATERIALIZATION_RERUN_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_digest"
BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_detail_binding_after_materialization_review_digest"
REVIEW_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_results_review_manifest_digest"
SOURCE_REATTEMPT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_after_materialization_digest"
SOURCE_REATTEMPT_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_reattempt_with_complete_source_digest_manifest_digest"

OUTPUT_IDS = [
    "detail_binding_reattempt_results_review_manifest",
    "source_detail_binding_reattempt_summary",
    "complete_29_row_binding_digest_review",
    "complete_29_row_binding_integrity_review",
    "reviewed_materialized_source_binding_summary",
    "complete_29_row_detail_binding_source_review",
    "top_module_concentration_review",
    "priority_tier_enablement_review",
    "bounded_samples_review",
    "unsupported_claims_boundary_review",
    "after_v2_planning_reentry_readiness_report",
    "digest_manifest",
]

REVIEW_FINDINGS = {
    "finding_1": "The source detail exposure/binding reattempt completed successfully using the reviewed committed complete 29-row source.",
    "finding_2": "The reattempt is bound by reattempt execution digest, complete 29-row binding digest, and digest-manifest digest.",
    "finding_3": "The bound source contains exactly 29 module rows.",
    "finding_4": "The bound source totals exactly 1,404 failed-or-errored node IDs.",
    "finding_5": "The top-five module paths and counts match the reviewed materialized source.",
    "finding_6": "The top-five sum remains 612 and the top-ten sum remains 1,069.",
    "finding_7": "The priority tier sums are 612, 457, and 335.",
    "finding_8": "Every bound row contains bounded samples with no more than five node IDs.",
    "finding_9": "Every row preserves the required source, basis, confidence, and unsupported-claims boundary.",
    "finding_10": "This results review did not read cache, rerun the reattempt, rerun materialization, rerun source recovery, run pytest, run retry, execute diagnostics, execute remediation, or execute classification.",
    "finding_11": "The complete 29-row detail binding is suitable for a separately invoked after-v2 planning reentry only after this review.",
    "finding_12": "The complete 29-row binding remains planning evidence only and does not prove failure/error separation, first failure, first error, traceback root cause, retry success, or main-merge readiness.",
}

NEXT_CHAIN = [
    "Re-enter after-v2 planning execution using reviewed complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
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

NEXT_GATES = [
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported",
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

RISK_CONTROLS = [
    "review_detail_binding_reattempt_results_does_not_read_cache",
    "review_detail_binding_reattempt_results_does_not_modify_cache",
    "review_detail_binding_reattempt_results_does_not_rerun_reattempt",
    "review_detail_binding_reattempt_results_does_not_rerun_materialization",
    "review_detail_binding_reattempt_results_does_not_rerun_source_recovery",
    "review_detail_binding_reattempt_results_does_not_run_pytest",
    "review_detail_binding_reattempt_results_does_not_rerun_retry",
    "review_detail_binding_reattempt_results_does_not_execute_after_v2_planning_reentry",
    "review_detail_binding_reattempt_results_does_not_execute_diagnostics",
    "review_detail_binding_reattempt_results_does_not_execute_remediation",
    "review_detail_binding_reattempt_results_does_not_execute_classification",
    "review_detail_binding_reattempt_results_does_not_classify_modules_again",
    "review_detail_binding_reattempt_results_does_not_create_targeted_diagnostic_candidate",
    "review_detail_binding_reattempt_results_does_not_create_new_retry_candidate",
    "review_detail_binding_reattempt_results_does_not_create_retry_results_review",
    "review_detail_binding_reattempt_results_does_not_create_integration_results_review",
    "review_detail_binding_reattempt_results_does_not_mark_integration_successful",
    "review_detail_binding_reattempt_results_does_not_generate_successful_integration_digest",
    "review_detail_binding_reattempt_results_does_not_claim_failure_error_separation",
    "review_detail_binding_reattempt_results_does_not_claim_first_failure",
    "review_detail_binding_reattempt_results_does_not_claim_first_error",
    "review_detail_binding_reattempt_results_does_not_claim_traceback_root_cause",
    "review_detail_binding_reattempt_results_does_not_recommend_direct_code_remediation",
    "review_detail_binding_reattempt_results_does_not_treat_binding_as_retry_success",
    "review_detail_binding_reattempt_results_does_not_push_integration_branch",
    "review_detail_binding_reattempt_results_does_not_push_main",
    "review_detail_binding_reattempt_results_does_not_delete_integration_branch",
    "review_detail_binding_reattempt_results_does_not_delete_worktree",
    "review_detail_binding_reattempt_results_does_not_force_push",
    "review_detail_binding_reattempt_results_does_not_prune_remotes",
    "review_detail_binding_reattempt_results_does_not_modify_tags",
    "review_detail_binding_reattempt_results_does_not_modify_staged_evidence",
    "review_detail_binding_reattempt_results_does_not_regenerate_evidence",
    "review_detail_binding_reattempt_results_does_not_call_providers",
    "review_detail_binding_reattempt_results_does_not_acquire_market_data",
    "review_detail_binding_reattempt_results_does_not_regenerate_dataset",
    "review_detail_binding_reattempt_results_does_not_recompute_metrics",
    "review_detail_binding_reattempt_results_does_not_train_models",
    "review_detail_binding_reattempt_results_does_not_score_strategy",
    "review_detail_binding_reattempt_results_does_not_generate_recommendations",
    "review_detail_binding_reattempt_results_does_not_accept_predictive_usefulness",
    "review_detail_binding_reattempt_results_does_not_accept_profitability",
    "review_detail_binding_reattempt_results_does_not_authorize_runtime",
    "review_detail_binding_reattempt_results_does_not_authorize_broker_execution",
    "complete_29_row_detail_binding_is_planning_source_not_root_cause",
    "complete_29_row_detail_binding_is_not_retry_success",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_detail_binding_execution_remains_historically_blocked",
    "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_after_v2_planning_reentry_required_after_detail_binding_review",
    "separate_results_review_required_after_after_v2_planning_reentry",
    "separate_diagnostic_capture_approval_required_before_diagnostics",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "detail_exposure_or_binding_reattempt_results_review_created",
    "detail_exposure_or_binding_reattempt_results_review_ready",
    "source_detail_binding_reattempt_reviewed",
    "source_detail_binding_reattempt_digest_verified",
    "source_detail_binding_digest_verified",
    "source_detail_binding_digest_manifest_verified",
    "reviewed_complete_29_row_detail_binding_source",
    "complete_29_row_detail_binding_integrity_reviewed",
    "top_module_concentration_reviewed",
    "priority_tier_enablement_reviewed",
    "bounded_samples_reviewed",
    "unsupported_claims_boundary_reviewed",
    "ready_for_after_v2_planning_reentry_with_complete_detail",
]

FALSE_FIELDS = [
    "cache_read_in_review", "cache_modified_in_review", "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
    "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
    "diagnostic_output_captured", "diagnostic_method_executed", "code_remediation_executed",
    "evidence_remediation_executed", "classification_execution_performed_in_review",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed",
    "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
    "pytest_cache_committed", "evidence_regenerated", "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed",
    "strategy_scoring_performed", "trade_recommendations_generated", "ready_for_retry_candidate",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed",
]

SOURCE_BINDINGS = {
    "source_complete_29_row_materialization_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
    "source_complete_29_row_materialized_payload_review_digest": source.SOURCE_PAYLOAD_REVIEW_DIGEST,
    "source_complete_29_row_materialization_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError(ValueError):
    """Raised when committed reattempt evidence or review content is invalid."""


def _committed_binding_rows() -> list[dict[str, Any]]:
    materialized_rows = source.review_source.source.committed_complete_29_row_module_grouping_detail_source_v1()
    return source._binding_rows(materialized_rows)


def _source_digest_manifest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    binding_digest = semantic_digest(rows)
    top_report = {
        "top_five_module_paths": [row["module_path"] for row in rows[:5]],
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tier_report = {
        "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }
    source_report = {
        "reviewed_source_available": True, "source_payload_digest": source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "source_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST, "row_count": 29,
        "failed_or_errored_nodeids_count": 1404,
    }
    payload_report = {
        "reviewed_materialized_payload_digest": source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
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
    return {
        "source_materialization_results_review": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_payload_review": source.SOURCE_PAYLOAD_REVIEW_DIGEST,
        "source_results_review_manifest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_materialized_payload": source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "binding_source": binding_digest, "source_binding_report": semantic_digest(source_report),
        "payload_binding_report": semantic_digest(payload_report),
        "top_module_concentration": semantic_digest(top_report),
        "priority_tiers": semantic_digest(tier_report),
        "unsupported_claims": semantic_digest(source.review_source.source.UNSUPPORTED_ROW_CLAIMS),
        "limitations": semantic_digest(limitations),
        "planning_reentry_enablement": semantic_digest(planning),
    }


def _committed_source_reattempt() -> dict[str, Any]:
    rows = _committed_binding_rows()
    return {
        "artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "execution_status": source.SUCCESS_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        SOURCE_REATTEMPT_DIGEST_KEY: SOURCE_REATTEMPT_DIGEST,
        SOURCE_BINDING_DIGEST_KEY: SOURCE_BINDING_DIGEST,
        SOURCE_REATTEMPT_MANIFEST_DIGEST_KEY: SOURCE_REATTEMPT_MANIFEST_DIGEST,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "used_reviewed_complete_29_row_materialized_source": True,
        "used_committed_source_evidence_only": True,
        "cache_read_in_reattempt": False,
        "materialization_execution_rerun_performed": False,
        "source_recovery_rerun_performed": False,
        "detail_exposure_or_binding_reattempt_executed": True,
        "detail_exposure_or_binding_executed": True,
        "complete_29_row_detail_exposed": True,
        "complete_29_row_detail_bound": True,
        "complete_29_row_detail_source_identified": True,
        "complete_29_row_module_grouping_detail_binding_source": rows,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.review_source.source.EXPECTED_TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
        "digest_manifest": _source_digest_manifest(rows),
    }


def _source_reasons(execution: Any) -> list[str]:
    if not isinstance(execution, Mapping):
        return ["SOURCE_DETAIL_BINDING_REATTEMPT_UNAVAILABLE"]
    expected = _committed_source_reattempt()
    fields = [
        "artifact_kind", "execution_status", "execution_scope", SOURCE_REATTEMPT_DIGEST_KEY,
        SOURCE_BINDING_DIGEST_KEY, SOURCE_REATTEMPT_MANIFEST_DIGEST_KEY,
        "selected_detail_exposure_or_binding_package", *SOURCE_BINDINGS,
        "retry_execution_commit", "retry_failure_context",
        "used_reviewed_complete_29_row_materialized_source", "used_committed_source_evidence_only",
        "cache_read_in_reattempt", "materialization_execution_rerun_performed",
        "source_recovery_rerun_performed", "detail_exposure_or_binding_reattempt_executed",
        "detail_exposure_or_binding_executed", "complete_29_row_detail_exposed",
        "complete_29_row_detail_bound", "complete_29_row_detail_source_identified",
        "failed_or_errored_nodeids_count", "module_summary_module_count",
        "largest_module_nodeid_counts", "top_five_module_paths", "top_5_count_sum", "top_10_count_sum",
        "priority_tier_1_count_sum", "priority_tier_2_count_sum", "priority_tier_3_count_sum",
    ]
    reasons = [f"SOURCE_REATTEMPT_{field.upper()}_MISMATCH_OR_MISSING" for field in fields if execution.get(field) != expected[field]]
    rows = execution.get("complete_29_row_module_grouping_detail_binding_source")
    if rows != expected["complete_29_row_module_grouping_detail_binding_source"]:
        reasons.append("SOURCE_REATTEMPT_COMPLETE_29_ROW_BINDING_MISMATCH_OR_MISSING")
    elif semantic_digest(rows) != SOURCE_BINDING_DIGEST:
        reasons.append("SOURCE_REATTEMPT_BINDING_DIGEST_MISMATCH")
    manifest = execution.get("digest_manifest")
    if manifest is not None and (manifest != expected["digest_manifest"] or semantic_digest(manifest) != SOURCE_REATTEMPT_MANIFEST_DIGEST):
        reasons.append("SOURCE_REATTEMPT_DIGEST_MANIFEST_MISMATCH")
    return reasons


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_review = review.get("complete_29_row_detail_binding_source_review", {})
    rows = source_review.get("rows", []) if isinstance(source_review, Mapping) else []
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    unsupported = source.review_source.source.UNSUPPORTED_ROW_CLAIMS
    values: dict[str, tuple[Any, Any]] = {
        "source_detail_binding_reattempt_digest_bound": (SOURCE_REATTEMPT_DIGEST, review.get("source_detail_binding_reattempt_digest")),
        "source_complete_29_row_binding_digest_bound": (SOURCE_BINDING_DIGEST, review.get("source_complete_29_row_binding_digest")),
        "source_detail_binding_reattempt_digest_manifest_digest_bound": (SOURCE_REATTEMPT_MANIFEST_DIGEST, review.get("source_detail_binding_reattempt_digest_manifest_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        "source_reattempt_success_status_bound": (source.SUCCESS_STATUS, review.get("source_detail_binding_reattempt_status")),
        "source_selected_package_bound": (SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE, review.get("selected_detail_exposure_or_binding_package")),
        "source_used_reviewed_complete_source_true": (True, review.get("source_detail_binding_reattempt_summary", {}).get("used_reviewed_complete_29_row_materialized_source")),
        "source_cache_not_read_by_reattempt": (False, review.get("source_detail_binding_reattempt_summary", {}).get("cache_read_in_reattempt")),
        "source_materialization_not_rerun_by_reattempt": (False, review.get("source_detail_binding_reattempt_summary", {}).get("materialization_execution_rerun_performed")),
        "source_recovery_not_rerun_by_reattempt": (False, review.get("source_detail_binding_reattempt_summary", {}).get("source_recovery_rerun_performed")),
        "binding_digest_verified": (True, review.get("source_detail_binding_digest_verified")),
        "digest_manifest_verified": (True, review.get("source_detail_binding_digest_manifest_verified")),
        "complete_29_row_binding_source_reviewed": (True, review.get("reviewed_complete_29_row_detail_binding_source")),
        "complete_29_row_rows_exactly_29": (29, len(rows)),
        "failed_or_errored_nodeids_1404": (1404, sum(value for value in counts if isinstance(value, int) and not isinstance(value, bool))),
        "largest_module_counts_verified": ([136, 131, 122, 112, 111], counts[:5]),
        "top_five_paths_preserved": (source.review_source.source.EXPECTED_TOP_FIVE_PATHS, paths[:5]),
        "top_five_sum_612": (612, sum(value for value in counts[:5] if isinstance(value, int))),
        "top_ten_sum_1069": (1069, sum(value for value in counts[:10] if isinstance(value, int))),
        "tier_1_sum_612": (612, sum(value for value in counts[:5] if isinstance(value, int))),
        "tier_2_sum_457": (457, sum(value for value in counts[5:10] if isinstance(value, int))),
        "tier_3_sum_335": (335, sum(value for value in counts[10:] if isinstance(value, int))),
        "bounded_samples_max_5": (True, bool(rows) and all(0 < len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows)),
        "row_sources_valid": (True, bool(rows) and all(row.get("source") == source.BINDING_ROW_SOURCE for row in rows)),
        "row_basis_valid": (True, bool(rows) and all(row.get("basis") == source.BINDING_ROW_BASIS for row in rows)),
        "row_confidence_valid": (True, bool(rows) and all(row.get("confidence") == source.BINDING_ROW_CONFIDENCE for row in rows)),
        "row_unsupported_claims_valid": (True, bool(rows) and all(row.get("unsupported_claims") == unsupported for row in rows)),
        "review_created_true": (True, review.get("detail_exposure_or_binding_reattempt_results_review_created")),
        "review_ready_true": (True, review.get("detail_exposure_or_binding_reattempt_results_review_ready")),
        "binding_integrity_reviewed_true": (True, review.get("complete_29_row_detail_binding_integrity_reviewed")),
        "top_module_concentration_reviewed_true": (True, review.get("top_module_concentration_reviewed")),
        "priority_tier_enablement_reviewed_true": (True, review.get("priority_tier_enablement_reviewed")),
        "bounded_samples_reviewed_true": (True, review.get("bounded_samples_reviewed")),
        "unsupported_claims_boundary_reviewed_true": (True, review.get("unsupported_claims_boundary_reviewed")),
        "ready_for_after_v2_planning_reentry_true": (True, review.get("ready_for_after_v2_planning_reentry_with_complete_detail")),
        "ready_for_retry_candidate_false": (False, review.get("ready_for_retry_candidate")),
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
    values.update({check_id: (SOURCE_BINDINGS[field], review.get(field)) for check_id, field in source_checks.items()})
    false_checks = {
        "failure_modules_classified_false": "failure_modules_classified",
        "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed",
        "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified",
        "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed",
        "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed",
        "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "detail_binding_reattempt_rerun_false": "detail_binding_reattempt_rerun_performed",
        "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "cache_read_in_review_false": "cache_read_in_review",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_review",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created",
        "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed", "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_review",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_false": "dataset_generation_performed_in_review",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, review.get(field)) for check_id, field in false_checks.items()})
    values["successful_integration_digest_false"] = ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")])
    values["predictive_usefulness_not_accepted"] = (NOT_ACCEPTED, review.get("predictive_usefulness"))
    values["profitability_not_accepted"] = (NOT_ACCEPTED, review.get("profitability"))
    values["runtime_not_authorized"] = (NOT_AUTHORIZED, review.get("runtime_use"))
    values["broker_not_authorized"] = (NOT_AUTHORIZED, review.get("broker_execution"))
    values["review_outputs_generated"] = (OUTPUT_IDS, [item.get("output_id") for item in review.get("review_outputs", [])])
    values["recommendation_defined"] = (RECOMMENDED_ACTION, review.get("recommended_action"))
    values["next_chain_defined"] = (NEXT_CHAIN, review.get("next_chain"))
    values["next_gates_defined"] = (NEXT_GATES, review.get("next_gates"))
    values["risk_controls_defined"] = (RISK_CONTROLS, review.get("risk_controls"))
    values["no_tracked_marketflow_files"] = (False, review.get("marketflow_outputs_tracked_in_repository"))
    values["no_tracked_pytest_cache_files"] = (False, review.get("pytest_cache_tracked_in_repository"))
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    fields = [
        "detail_exposure_or_binding_reattempt_results_review_created",
        "detail_exposure_or_binding_reattempt_results_review_ready", "source_detail_binding_reattempt_reviewed",
        "source_detail_binding_reattempt_digest_verified", "source_detail_binding_digest_verified",
        "source_detail_binding_digest_manifest_verified", "reviewed_complete_29_row_detail_binding_source",
        "complete_29_row_detail_binding_integrity_reviewed", "cache_read_in_review",
        "detail_binding_reattempt_rerun_performed", "materialization_execution_rerun_performed",
        "source_recovery_rerun_performed", "complete_29_row_detail_exposed_in_source_reattempt",
        "complete_29_row_detail_bound_in_source_reattempt", "complete_29_row_detail_source_identified_in_source_reattempt",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
        "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
        "priority_tier_2_count_sum", "priority_tier_3_count_sum",
        "ready_for_after_v2_planning_reentry_with_complete_detail", "ready_for_retry_candidate",
        "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created",
        "new_retry_executed", "integration_execution_successful",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        **{field: review.get(field) for field in fields},
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", REVIEW_DIGEST_KEY, "review_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(
    *, source_reattempt: dict | None = None,
) -> dict:
    """Review committed reattempt evidence without invoking any execution path."""

    execution = deepcopy(source_reattempt) if source_reattempt is not None else _committed_source_reattempt()
    reasons = _source_reasons(execution)
    if reasons:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError(";".join(reasons))
    rows = deepcopy(execution["complete_29_row_module_grouping_detail_binding_source"])
    source_summary = {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "detail_exposure_or_binding_reattempt_executed": True,
        "detail_exposure_or_binding_executed": True,
        "complete_29_row_detail_exposed": True, "complete_29_row_detail_bound": True,
        "complete_29_row_detail_source_identified": True,
        "used_reviewed_complete_29_row_materialized_source": True,
        "used_committed_source_evidence_only": True, "cache_read_in_reattempt": False,
        "materialization_execution_rerun_performed": False, "source_recovery_rerun_performed": False,
    }
    materialization_summary = {
        "results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "payload_review_digest": source.SOURCE_PAYLOAD_REVIEW_DIGEST,
        "results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "execution_digest": source.SOURCE_MATERIALIZATION_EXECUTION_DIGEST,
        "payload_digest": source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "execution_manifest_digest": source.SOURCE_MATERIALIZATION_DIGEST_MANIFEST_DIGEST,
    }
    binding_source_review = {
        "reviewed": True, "row_count": len(rows), "failed_or_errored_nodeids_count": 1404,
        "source_binding_digest": SOURCE_BINDING_DIGEST, "rows": rows,
    }
    binding_digest_review = {
        "expected": SOURCE_BINDING_DIGEST, "actual_from_committed_rows": semantic_digest(rows),
        "verified": True, "digest_is_not_payload": True,
    }
    binding_integrity_review = {
        "reviewed": True, "row_count": len(rows),
        "failed_or_errored_nodeids_count": sum(row["failed_or_errored_nodeid_count"] for row in rows),
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "required_row_fields_present": all(set([
            "module_path", "failed_or_errored_nodeid_count", "percentage_of_failed_or_errored_nodeids",
            "priority_order", "priority_tier", "sample_nodeids_bounded", "sample_nodeids_bounded_count",
            "source", "basis", "confidence", "unsupported_claims",
        ]).issubset(row) for row in rows),
    }
    materialized_binding_summary = {
        "source": source.BINDING_ROW_SOURCE, "basis": source.BINDING_ROW_BASIS,
        "confidence": source.BINDING_ROW_CONFIDENCE, "row_count": 29,
        "failed_or_errored_nodeids_count": 1404,
    }
    top_summary = [
        {"priority_order": row["priority_order"], "module_path": row["module_path"],
         "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"]}
        for row in rows[:5]
    ]
    concentration_review = {
        "reviewed": True, "top_5_module_paths": [row["module_path"] for row in rows[:5]],
        "top_5_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tier_review = {
        "reviewed": True,
        "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }
    samples_review = {
        "reviewed": True, "module_count": 29, "sample_limit_per_module": 5,
        "all_rows_have_bounded_samples": all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows),
        "all_sample_counts_match": all(row["sample_nodeids_bounded_count"] == len(row["sample_nodeids_bounded"]) for row in rows),
        "largest_sample_count": max(row["sample_nodeids_bounded_count"] for row in rows),
    }
    unsupported_review = {
        "reviewed": True,
        "required_unsupported_claims": list(source.review_source.source.UNSUPPORTED_ROW_CLAIMS),
        "all_rows_preserve_boundary": all(
            row["unsupported_claims"] == source.review_source.source.UNSUPPORTED_ROW_CLAIMS for row in rows
        ),
    }
    recommendation = {
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "ready_for_after_v2_planning_reentry_with_complete_detail": True,
        "ready_for_retry_candidate": False, "reason": RECOMMENDATION_REASON,
    }
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_detail_binding_reattempt_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_detail_binding_reattempt_status": source.SUCCESS_STATUS,
        "source_detail_binding_reattempt_scope": source.EXECUTION_SCOPE,
        "source_detail_binding_reattempt_digest": SOURCE_REATTEMPT_DIGEST,
        "source_complete_29_row_binding_digest": SOURCE_BINDING_DIGEST,
        "source_detail_binding_reattempt_digest_manifest_digest": SOURCE_REATTEMPT_MANIFEST_DIGEST,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": execution["retry_execution_commit"],
        "retry_failure_context": deepcopy(execution["retry_failure_context"]),
        "source_detail_binding_reattempt_summary": source_summary,
        "source_materialization_results_review_summary": materialization_summary,
        "complete_29_row_detail_binding_source_review": binding_source_review,
        "binding_digest_review": binding_digest_review,
        "complete_29_row_binding_integrity_review": binding_integrity_review,
        "reviewed_materialized_source_binding_summary": materialized_binding_summary,
        "top_module_summary": top_summary, "top_module_concentration_review": concentration_review,
        "priority_tier_enablement_review": tier_review, "bounded_samples_review": samples_review,
        "unsupported_claims_boundary_review": unsupported_review,
        "review_findings": deepcopy(REVIEW_FINDINGS),
        "review_outputs": [{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
        "recommendation": recommendation, "recommended_next_task": NEXT_TASK,
        "recommended_next_task_status": NEXT_TASK_STATUS, "recommended_action": RECOMMENDED_ACTION,
        "reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.review_source.source.EXPECTED_TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
        "complete_29_row_detail_exposed_in_source_reattempt": True,
        "complete_29_row_detail_bound_in_source_reattempt": True,
        "complete_29_row_detail_source_identified_in_source_reattempt": True,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    binding_review_digest = semantic_digest({
        "binding_digest_review": binding_digest_review,
        "binding_integrity_review": binding_integrity_review,
        "binding_source_review": binding_source_review,
        "bounded_samples_review": samples_review,
        "unsupported_claims_boundary_review": unsupported_review,
    })
    review[BINDING_REVIEW_DIGEST_KEY] = binding_review_digest
    review["binding_review_digest"] = binding_review_digest
    review["digest_manifest"] = {
        "source_reattempt": SOURCE_REATTEMPT_DIGEST,
        "source_binding": SOURCE_BINDING_DIGEST,
        "source_reattempt_manifest": SOURCE_REATTEMPT_MANIFEST_DIGEST,
        "source_materialization_results_review": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_materialized_payload": source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST,
        "binding_review": binding_review_digest,
        "source_reattempt_summary": semantic_digest(source_summary),
        "binding_integrity_review": semantic_digest(binding_integrity_review),
        "top_module_concentration_review": semantic_digest(concentration_review),
        "priority_tier_enablement_review": semantic_digest(tier_review),
        "bounded_samples_review": semantic_digest(samples_review),
        "unsupported_claims_boundary_review": semantic_digest(unsupported_review),
        "review_findings": semantic_digest(REVIEW_FINDINGS),
        "recommendation": semantic_digest(recommendation),
    }
    manifest_digest = semantic_digest(review["digest_manifest"])
    review[REVIEW_MANIFEST_DIGEST_KEY] = manifest_digest
    review["review_manifest_digest"] = manifest_digest
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    digest = _review_digest(review)
    review[REVIEW_DIGEST_KEY] = digest
    review["review_digest"] = digest
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(
    review: dict,
) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_detail_binding_reattempt_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_detail_binding_reattempt_status": source.SUCCESS_STATUS,
        "source_detail_binding_reattempt_scope": source.EXECUTION_SCOPE,
        "source_detail_binding_reattempt_digest": SOURCE_REATTEMPT_DIGEST,
        "source_complete_29_row_binding_digest": SOURCE_BINDING_DIGEST,
        "source_detail_binding_reattempt_digest_manifest_digest": SOURCE_REATTEMPT_MANIFEST_DIGEST,
        "selected_detail_exposure_or_binding_package": SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError(f"{field} mismatch")
    if review.get("retry_failure_context") != {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("retry failure counts mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("required review flag missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("closed boundary opened")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("acceptance boundary changed")
    if review.get("runtime_use") != NOT_AUTHORIZED or review.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("runtime boundary changed")
    source_summary = review.get("source_detail_binding_reattempt_summary")
    if not isinstance(source_summary, Mapping) or source_summary.get("execution_status") != source.SUCCESS_STATUS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("source reattempt summary invalid")
    if source_summary.get("used_reviewed_complete_29_row_materialized_source") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("reviewed source flag missing")
    if source_summary.get("cache_read_in_reattempt") is not False:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("source cache boundary invalid")
    rows_review = review.get("complete_29_row_detail_binding_source_review")
    if not isinstance(rows_review, Mapping) or not isinstance(rows_review.get("rows"), list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding source review missing")
    rows = rows_review["rows"]
    expected_rows = _committed_binding_rows()
    if rows != expected_rows or semantic_digest(rows) != SOURCE_BINDING_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding source integrity invalid")
    expected_scalars = {
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": list(source.review_source.source.EXPECTED_TOP_FIVE_PATHS),
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457,
        "priority_tier_3_count_sum": 335,
    }
    for field, expected in expected_scalars.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError(f"{field} mismatch")
    digest_review = review.get("binding_digest_review")
    if not isinstance(digest_review, Mapping) or digest_review.get("verified") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding digest review invalid")
    expected_digest_review = {
        "expected": SOURCE_BINDING_DIGEST, "actual_from_committed_rows": semantic_digest(rows),
        "verified": True, "digest_is_not_payload": True,
    }
    if digest_review != expected_digest_review:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding digest review mismatch")
    integrity = review.get("complete_29_row_binding_integrity_review")
    if not isinstance(integrity, Mapping) or integrity.get("row_count") != 29 or integrity.get("failed_or_errored_nodeids_count") != 1404:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding integrity review invalid")
    samples = review.get("bounded_samples_review")
    if not isinstance(samples, Mapping) or samples.get("all_rows_have_bounded_samples") is not True or samples.get("largest_sample_count", 6) > 5:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("bounded samples review invalid")
    unsupported = review.get("unsupported_claims_boundary_review")
    if not isinstance(unsupported, Mapping) or unsupported.get("all_rows_preserve_boundary") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("unsupported claims review invalid")
    if review.get("review_findings") != REVIEW_FINDINGS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review findings invalid")
    if review.get("next_chain") != NEXT_CHAIN or review.get("next_gates") != NEXT_GATES or review.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review governance content invalid")
    outputs = review.get("review_outputs", [])
    if [item.get("output_id") for item in outputs] != OUTPUT_IDS or any(item.get("status") != "GENERATED_RESEARCH_ONLY" for item in outputs):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review outputs invalid")
    if review.get("recommended_next_task") != NEXT_TASK or review.get("recommended_action") != RECOMMENDED_ACTION:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("recommendation invalid")
    recommendation = review.get("recommendation")
    if not isinstance(recommendation, Mapping) or recommendation.get("reason") != RECOMMENDATION_REASON:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("recommendation reason invalid")
    expected_binding_review_digest = semantic_digest({
        "binding_digest_review": review["binding_digest_review"],
        "binding_integrity_review": review["complete_29_row_binding_integrity_review"],
        "binding_source_review": rows_review,
        "bounded_samples_review": review["bounded_samples_review"],
        "unsupported_claims_boundary_review": review["unsupported_claims_boundary_review"],
    })
    if review.get(BINDING_REVIEW_DIGEST_KEY) != expected_binding_review_digest or review.get("binding_review_digest") != expected_binding_review_digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("binding review digest invalid")
    manifest_digest = semantic_digest(review.get("digest_manifest"))
    if review.get(REVIEW_MANIFEST_DIGEST_KEY) != manifest_digest or review.get("review_manifest_digest") != manifest_digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review manifest digest invalid")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("checklist invalid")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("summary invalid")
    digest = review.get(REVIEW_DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _review_digest(review) or review.get("review_digest") != digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("review digest invalid")
    return {
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"], "review_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(
    output_dir: str | Path, *, source_reattempt: dict | None = None,
) -> dict:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(
        source_reattempt=source_reattempt
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_digest": review[REVIEW_DIGEST_KEY],
        "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(review)
    sections = [
        ("Source Detail Binding Reattempt", [SOURCE_REATTEMPT_DIGEST, SOURCE_BINDING_DIGEST, source.SUCCESS_STATUS]),
        ("Source Materialization Results Review", [source.SOURCE_RESULTS_REVIEW_DIGEST, source.SOURCE_PAYLOAD_REVIEW_DIGEST]),
        ("Source Materialization Execution", [source.SOURCE_MATERIALIZATION_EXECUTION_DIGEST, source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST]),
        ("Source Detail Exposure or Binding Approval", [SOURCE_BINDINGS["source_detail_exposure_or_binding_approval_digest"], SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE]),
        ("Source Prior Blocked Detail Exposure or Binding Execution", [SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_digest"], SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_reason"]]),
        ("Source Reentry Failure Diagnosis", [SOURCE_BINDINGS["source_reentry_failure_diagnosis_digest"], SOURCE_BINDINGS["source_reentry_failure_primary_failure_class"]]),
        ("Source Recovery Results Review", [SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"], SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; root regression is not retry evidence."]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Reviewed Complete 29-row Detail Binding Source", ["29 rows and 1,404 failed-or-errored node IDs reviewed from committed binding evidence."]),
        ("Binding Digest Review", [str(review["binding_digest_review"])]),
        ("Top Module Concentration Review", [str(review["top_module_concentration_review"])]),
        ("Priority Tier Enablement Review", [str(review["priority_tier_enablement_review"])]),
        ("Bounded Samples Review", [str(review["bounded_samples_review"])]),
        ("Unsupported Claims Boundary", list(source.review_source.source.UNSUPPORTED_ROW_CLAIMS)),
        ("Review Findings", list(review["review_findings"].values())),
        ("Recommendation", [review["recommended_action"], review["reason"]]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["No cache read, execution rerun, retry, planning reentry, diagnostics, remediation, classification, provider, runtime, trading, integration, or main action occurred."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass."]),
        ("Guardrails", ["Only a separately invoked after-v2 planning reentry is prepared; retry and main-merge gates remain closed."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Execution Reattempt with Complete Source Results Review v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_MATERIALIZATION_RERUN_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_markdown_v1",
]
