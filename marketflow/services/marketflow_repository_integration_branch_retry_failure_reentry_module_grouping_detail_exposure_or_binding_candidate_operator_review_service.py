"""Review module-detail exposure or binding candidate packages without selection."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1"
SOURCE_CANDIDATE_DIGEST = "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_V1_IF_SELECTED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_GENERATED = "NOT_GENERATED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

PACKAGE_REVIEW_STATUSES = [
    "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
    "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED",
    "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    "REVIEWED_AVAILABLE_PACKAGE_REQUIRES_SEPARATE_APPROVAL_NOT_SELECTED",
    "REVIEWED_AVAILABLE_NOT_RECOMMENDED_PACKAGE_NOT_SELECTED",
    *(["REVIEWED_BLOCKED_NOT_ALLOWED"] * 5),
]

NEXT_CHAIN = [
    "Detail Exposure or Binding Approval v1, if selected.",
    "Detail Exposure or Binding Execution v1, if approved.",
    "Detail Exposure or Binding Results Review v1.",
    "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = list(source.NEXT_GATES[1:])

RISK_CONTROLS = [
    "review_detail_binding_does_not_select_package", "review_detail_binding_does_not_approve_package",
    *[
        item.replace("candidate_detail_binding", "review_detail_binding")
        for item in source.RISK_CONTROLS
        if item != "separate_operator_review_required"
    ],
]

FALSE_BOUNDARIES = [
    "ready_for_detail_exposure_or_binding_approval", "detail_exposure_or_binding_selected",
    "detail_exposure_or_binding_approved", "detail_exposure_or_binding_authorized",
    "detail_exposure_or_binding_executed", "complete_29_row_detail_exposed",
    "complete_29_row_detail_bound", "module_grouping_detail_exposed_by_review",
    "module_paths_recovered_by_review", "per_module_counts_recovered_by_review",
    "bounded_nodeid_samples_recovered_by_review", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "source_recovery_rerun_performed", "cache_read_in_review",
    "module_grouping_recovered_in_review", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed", "classification_execution_performed_in_review",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError(ValueError):
    """Raised when the operator-review contract is violated."""


def _committed_source_candidate() -> dict[str, Any]:
    diagnosis = source._committed_source_diagnosis()
    return {
        "artifact_kind": source.ARTIFACT_KIND, "candidate_status": source.CANDIDATE_STATUS,
        "candidate_scope": source.CANDIDATE_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "source_reentry_failure_diagnosis_digest": source.SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
        "recommended_next_package_from_diagnosis": source.RECOMMENDED_PACKAGE,
        "source_reentry_execution_blocked_digest": source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "source_reentry_execution_blocked_reason": source.source.SOURCE_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": source.source.SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.source.SOURCE_RECOVERY_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.source.SOURCE_RECOVERY_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.source.SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.source.SOURCE_RECOVERY_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST,
        "source_after_v2_approval_digest": source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": source.source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_approval_v2_digest": source.source.SOURCE_APPROVAL_V2_DIGEST,
        "source_staged_inventory_digest": source.source.SOURCE_STAGED_INVENTORY_DIGEST,
        "retry_execution_commit": source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": deepcopy(diagnosis["retry_failure_context"]),
        "recovered_module_grouping_source_summary": deepcopy(diagnosis["recovered_module_grouping_source_summary"]),
        "top_module_summary": deepcopy(diagnosis["top_module_summary"]),
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "available_committed_reentry_detail": list(source.source.AVAILABLE_COMMITTED_DETAIL),
        "missing_committed_reentry_detail": list(source.source.MISSING_COMMITTED_DETAIL),
        "actual_live_reentry_source_lacks_complete_29_rows": True,
        "reentry_success_path_tested_with_complete_29_row_snapshot": True,
        "candidate_philosophy": {"detail_exposure_or_binding_candidate_philosophy": source.CANDIDATE_PHILOSOPHY, "candidate_boundary": source.CANDIDATE_BOUNDARY, "candidate_goal": source.CANDIDATE_GOAL},
        "proposed_packages": deepcopy(source.PROPOSED_PACKAGES),
        "future_detail_exposure_or_binding_requirements": deepcopy(source.FUTURE_REQUIREMENTS),
        "future_detail_exposure_or_binding_plan": {"status": source.PLANNED_NOT_EXECUTED, "steps": list(source.FUTURE_PLAN)},
        "planned_outputs": [{"output_id": item, "status": source.PLANNED_NOT_GENERATED} for item in source.PLANNED_OUTPUT_IDS],
        "non_goals": list(source.NON_GOALS),
    }


def _validate_source_candidate(candidate: Mapping[str, Any]) -> None:
    mismatches = [key for key, expected in _committed_source_candidate().items() if candidate.get(key) != expected]
    if mismatches:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError(f"source candidate mismatch: {', '.join(mismatches)}")


def _reviewed_packages() -> list[dict[str, Any]]:
    return [
        {"package": item["package"], "source_status": item["status"], "review_status": PACKAGE_REVIEW_STATUSES[index], "selected": False, "approved": False, "executed": False}
        for index, item in enumerate(source.PROPOSED_PACKAGES)
    ]


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    pairs: dict[str, tuple[Any, Any]] = {
        "source_candidate_digest_bound": (SOURCE_CANDIDATE_DIGEST, review.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_diagnosis_digest_bound": (source.SOURCE_DIAGNOSIS_DIGEST, review.get("source_reentry_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (source.PRIMARY_FAILURE_CLASS, review.get("primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, review.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, review.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (source.source.SOURCE_BLOCKED_REASON, review.get("source_reentry_execution_blocked_reason")),
        "source_after_v2_planning_reentry_digest_bound": (source.source.SOURCE_REENTRY_DIGEST, review.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_DIGEST, review.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, review.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.source.SOURCE_RECOVERY_EXECUTION_DIGEST, review.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.source.SOURCE_RECOVERY_DETAIL_DIGEST, review.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST, review.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_recovery_approval_digest_bound": (source.source.SOURCE_RECOVERY_APPROVAL_DIGEST, review.get("source_module_grouping_source_recovery_approval_digest")),
        "source_recovery_operator_review_digest_bound": (source.source.SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST, review.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_recovery_candidate_digest_bound": (source.source.SOURCE_RECOVERY_CANDIDATE_DIGEST, review.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST, review.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST, review.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST, review.get("source_after_v2_approval_digest")),
        "source_after_v2_operator_review_digest_bound": (source.source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST, review.get("source_after_v2_operator_review_digest")),
        "source_after_v2_candidate_digest_bound": (source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST, review.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, review.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.SOURCE_EXECUTION_V2_DIGEST, review.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.SOURCE_MODULE_GROUPING_DIGEST, review.get("source_module_grouping_digest")),
        "source_approval_v2_digest_bound": (source.source.SOURCE_APPROVAL_V2_DIGEST, review.get("source_approval_v2_digest")),
        "source_staged_inventory_digest_bound": (source.source.SOURCE_STAGED_INVENTORY_DIGEST, review.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": (source.source.RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": ({"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]}, review.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (source.source.TOP_FIVE, review.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, review.get("top_5_count_sum")), "top_ten_count_sum_1069_bound": (1069, review.get("top_10_count_sum")),
        "available_committed_reentry_detail_recorded": (source.source.AVAILABLE_COMMITTED_DETAIL, review.get("available_committed_reentry_detail")),
        "missing_committed_reentry_detail_recorded": (source.source.MISSING_COMMITTED_DETAIL, review.get("missing_committed_reentry_detail")),
        "actual_live_reentry_source_lacks_complete_29_rows_true": (True, review.get("actual_live_reentry_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, review.get("reentry_success_path_tested_with_complete_29_row_snapshot")),
        "recommended_package_from_diagnosis_bound": (source.RECOMMENDED_PACKAGE, review.get("recommended_next_package_from_diagnosis")),
        "review_created_true": (True, review.get("reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_ready")),
        "packages_reviewed_true": (True, review.get("detail_exposure_or_binding_packages_reviewed")),
        "future_requirements_reviewed_true": (True, review.get("future_detail_exposure_or_binding_requirements_reviewed")),
        "future_plan_reviewed_true": (True, review.get("future_detail_exposure_or_binding_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_detail_exposure_or_binding_approval")),
        "recommended_package_reviewed_not_selected": (False, review.get("recommendation", {}).get("selected")),
        "packages_reviewed_11": (11, len(review.get("reviewed_packages", []))),
        "blocked_packages_reviewed_5": (5, sum(item.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review.get("reviewed_packages", []) if isinstance(item, Mapping))),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")), "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (source.NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (source.NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (source.NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (source.NOT_AUTHORIZED, review.get("broker_execution")),
    }
    names = {
        "detail_exposure_or_binding_selected": "detail_exposure_or_binding_selected_false", "detail_exposure_or_binding_approved": "detail_exposure_or_binding_approved_false",
        "detail_exposure_or_binding_authorized": "detail_exposure_or_binding_authorized_false", "detail_exposure_or_binding_executed": "detail_exposure_or_binding_executed_false",
        "complete_29_row_detail_exposed": "complete_29_row_detail_exposed_false", "complete_29_row_detail_bound": "complete_29_row_detail_bound_false",
        "module_grouping_detail_exposed_by_review": "module_grouping_detail_exposed_by_review_false", "module_paths_recovered_by_review": "module_paths_recovered_by_review_false",
        "per_module_counts_recovered_by_review": "per_module_counts_recovered_by_review_false", "bounded_nodeid_samples_recovered_by_review": "bounded_nodeid_samples_recovered_by_review_false",
        "after_v2_planning_execution_reentry_created": "after_v2_planning_reentry_created_false", "after_v2_planning_execution_reentry_performed": "after_v2_planning_reentry_performed_false",
        "targeted_diagnostic_output_capture_candidate_created": "targeted_diagnostic_candidate_created_false", "new_retry_candidate_created": "new_retry_candidate_created_false",
        "new_retry_executed": "new_retry_executed_false", "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false", "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "cache_read_in_review": "cache_read_in_review_false", "module_grouping_recovered_in_review": "module_grouping_recovered_in_review_false",
        "retry_rerun_performed": "retry_rerun_false", "full_pytest_performed": "full_pytest_false",
        "diagnostic_command_executed": "diagnostic_command_false", "diagnostic_output_captured": "diagnostic_output_false",
        "integration_execution_successful": "integration_success_false", "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false", "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false", "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_review": "provider_requests_false", "market_data_acquisition_performed_in_review": "market_data_acquisition_false",
        "dataset_generation_performed_in_review": "dataset_generation_false", "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    pairs.update({check_id: (False, review.get(field)) for field, check_id in names.items()})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {"total_checks": len(checklist), "passed_checks": len(checklist) - len(failed), "failed_checks": len(failed), "blocker_count": len(failed),
        "reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_created": review.get("reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_created"),
        "reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_ready": review.get("reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_ready"),
        "detail_exposure_or_binding_packages_reviewed": review.get("detail_exposure_or_binding_packages_reviewed"),
        "recommended_detail_exposure_or_binding_package": review.get("recommended_detail_exposure_or_binding_package"),
        "recommended_package_selected": review.get("recommendation", {}).get("selected"),
        "ready_for_detail_exposure_or_binding_approval": review.get("ready_for_detail_exposure_or_binding_approval"),
        "detail_exposure_or_binding_executed": review.get("detail_exposure_or_binding_executed"),
        "complete_29_row_detail_exposed": review.get("complete_29_row_detail_exposed"), "complete_29_row_detail_bound": review.get("complete_29_row_detail_bound"),
        "after_v2_planning_execution_reentry_created": review.get("after_v2_planning_execution_reentry_created"), "after_v2_planning_execution_reentry_performed": review.get("after_v2_planning_execution_reentry_performed"),
        "targeted_diagnostic_output_capture_candidate_created": review.get("targeted_diagnostic_output_capture_candidate_created"), "new_retry_candidate_created": review.get("new_retry_candidate_created"),
        "new_retry_executed": review.get("new_retry_executed"), "integration_execution_successful": review.get("integration_execution_successful"),
        "recommended_next_task": review.get("recommended_next_task"), "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False}


def _digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(*, source_candidate: dict | None = None) -> dict:
    candidate = deepcopy(source_candidate) if source_candidate is not None else _committed_source_candidate()
    _validate_source_candidate(candidate)
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_detail_exposure_or_binding_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_detail_exposure_or_binding_candidate_status": source.CANDIDATE_STATUS,
        "source_detail_exposure_or_binding_candidate_scope": source.CANDIDATE_SCOPE,
        "source_detail_exposure_or_binding_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "source_reentry_failure_diagnosis_digest": source.SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS, "recommended_next_package_from_diagnosis": source.RECOMMENDED_PACKAGE,
    }
    for key in ("source_reentry_execution_blocked_digest", "source_reentry_execution_blocked_manifest_digest", "source_reentry_execution_blocked_reason", "source_after_v2_planning_reentry_digest", "source_module_grouping_source_recovery_results_review_digest", "source_module_grouping_source_recovery_results_review_manifest_digest", "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest", "source_module_grouping_source_recovery_digest_manifest_digest", "source_module_grouping_source_recovery_approval_digest", "source_module_grouping_source_recovery_operator_review_digest", "source_module_grouping_source_recovery_candidate_digest", "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest", "source_after_v2_approval_digest", "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest", "source_results_review_v2_digest", "source_execution_v2_digest", "source_module_grouping_digest", "source_approval_v2_digest", "source_staged_inventory_digest", "retry_execution_commit", "retry_failure_context", "recovered_module_grouping_source_summary", "top_module_summary", "top_5_count_sum", "top_10_count_sum", "available_committed_reentry_detail", "missing_committed_reentry_detail", "actual_live_reentry_source_lacks_complete_29_rows", "reentry_success_path_tested_with_complete_29_row_snapshot"):
        review[key] = deepcopy(candidate[key])
    review.update({
        "diagnosis_findings_summary": {"primary_failure_class": source.PRIMARY_FAILURE_CLASS, "complete_29_row_detail_available_to_live_reentry_execution": False},
        "reviewed_candidate_philosophy": {"reviewed_detail_exposure_or_binding_candidate_philosophy": source.CANDIDATE_PHILOSOPHY, "reviewed_candidate_boundary": "Candidate reviewed only; no detail exposure, source recovery, cache read, planning execution, diagnostics, remediation, retry, results review, main merge, runtime, or trading authority is created.", "reviewed_candidate_goal": "Review safe future packages to expose, bind, or carry forward the complete recovered module grouping detail required for deterministic after-v2 planning reentry.", "review_status": "REVIEWED_PLANNING_ONLY"},
        "reviewed_packages": _reviewed_packages(),
        "reviewed_future_detail_exposure_or_binding_requirements": [{"requirement_id": key, "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_DETAIL_EXPOSURE_OR_BINDING", "execution_status": NOT_EXECUTED} for key in source.FUTURE_REQUIREMENTS],
        "reviewed_future_detail_exposure_or_binding_plan": [{"step_id": index, "step": step, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": NOT_EXECUTED} for index, step in enumerate(source.FUTURE_PLAN, 1)],
        "reviewed_planned_outputs": [{"output_id": key, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": NOT_GENERATED} for key in source.PLANNED_OUTPUT_IDS],
        "reviewed_non_goals": [{"non_goal_id": key, "review_status": "REVIEWED_ACTIVE"} for key in source.NON_GOALS],
        "recommendation": {"recommended_detail_exposure_or_binding_package": source.RECOMMENDED_PACKAGE, "recommendation_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", "selected": False, "approved": False, "executed": False, "reason": "The detail exposure/binding candidate has been reviewed, but no package has been selected or approved by this review."},
        "recommended_detail_exposure_or_binding_package": source.RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_DETAIL_EXPOSURE_OR_BINDING_EXECUTION",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_created": True,
        "reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_ready": True,
        "detail_exposure_or_binding_packages_reviewed": True, "future_detail_exposure_or_binding_requirements_reviewed": True,
        "future_detail_exposure_or_binding_plan_reviewed": True, "planned_outputs_reviewed": True, "non_goals_reviewed": True,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": source.NOT_ACCEPTED, "profitability": source.NOT_ACCEPTED,
        "runtime_use": source.NOT_AUTHORIZED, "strategy_use": source.NOT_AUTHORIZED,
        "paper_trading": source.NOT_AUTHORIZED, "broker_execution": source.NOT_AUTHORIZED,
        "failure_modules_classified": False, "error_modules_classified": False, "failure_error_separation_claimed": False,
        "first_failure_identified": False, "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "direct_code_remediation_recommended": False,
        "retry_success_claimed": False, "main_merge_readiness_claimed": False,
    })
    review.update({key: False for key in FALSE_BOUNDARIES})
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_digest"] = _digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(review: dict) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError("review must be object")
    for field, expected in {"artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE, "source_detail_exposure_or_binding_candidate_artifact_kind": source.ARTIFACT_KIND, "source_detail_exposure_or_binding_candidate_status": source.CANDIDATE_STATUS, "source_detail_exposure_or_binding_candidate_scope": source.CANDIDATE_SCOPE}.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError(f"{field} mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError("checklist invalid")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError("summary invalid")
    digest = review.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _digest(review):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateOperatorReviewError("review digest invalid")
    return {"artifact_kind": review["artifact_kind"], "review_status": review["review_status"], "review_scope": review["review_scope"], "operator_review_digest": digest, **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_markdown_v1(review: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(review)
    sections = [
        ("Source Detail Exposure or Binding Candidate", [SOURCE_CANDIDATE_DIGEST]),
        ("Source Reentry Failure Diagnosis", [source.SOURCE_DIAGNOSIS_DIGEST, source.PRIMARY_FAILURE_CLASS]),
        ("Source Blocked Reentry Execution", [source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, source.source.SOURCE_BLOCKED_REASON]),
        ("Source Recovery Results Review", [source.source.SOURCE_RESULTS_REVIEW_DIGEST, source.source.SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]),
        ("Recovered Module Grouping Source Summary", [str(review["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Committed Detail", [*review["available_committed_reentry_detail"], *review["missing_committed_reentry_detail"]]),
        ("Review Scope", [REVIEW_SCOPE]), ("Reviewed Candidate Philosophy", [str(review["reviewed_candidate_philosophy"])]),
        ("Reviewed Detail Exposure or Binding Packages", [f"{item['package']}: {item['review_status']}" for item in review["reviewed_packages"]]),
        ("Reviewed Future Detail Exposure or Binding Requirements", [item["requirement_id"] for item in review["reviewed_future_detail_exposure_or_binding_requirements"]]),
        ("Reviewed Future Detail Exposure or Binding Plan", [item["step"] for item in review["reviewed_future_detail_exposure_or_binding_plan"]]),
        ("Reviewed Planned Outputs", [item["output_id"] for item in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [item["non_goal_id"] for item in review["reviewed_non_goals"]]),
        ("Recommendation", [str(review["recommendation"])]), ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]), ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["Operator review only; no selection, approval, exposure, binding, execution, retry, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["Optional operator selection and separate approval are required before any exposure or binding execution."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Candidate Operator Review v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(output_dir: str | Path, *, source_candidate: dict | None = None) -> dict:
    review = build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1(source_candidate=source_candidate)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_V1.md"
    json_path.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_markdown_v1(review), encoding="utf-8")
    return {"artifact": review, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = ["ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_V1", "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_READY", "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN", "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1", "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1", "write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_v1", "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review_markdown_v1"]
