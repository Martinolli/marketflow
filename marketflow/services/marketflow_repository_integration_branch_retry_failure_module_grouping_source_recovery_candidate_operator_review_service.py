"""Review module-grouping source-recovery packages without selecting one."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_"
    "CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN"
)
SCHEMA_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_module_grouping_"
    "source_recovery_candidate_operator_review_v1"
)
SOURCE_CANDIDATE_DIGEST = (
    "4c0542256406f1db4d86f32958d738f6c86dc83ea2dd2132e2d54bcf5afb8bcb"
)
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_APPROVAL_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_MODULE_GROUPING_"
    "SOURCE_RECOVERY_EXECUTION"
)
RECOMMENDATION_REASON = (
    "The module-grouping source-recovery candidate has been reviewed, but no "
    "package has been selected or approved by this review."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_PHILOSOPHY = (
    "The after-v2 planning execution failed closed because committed evidence did "
    "not expose module paths, per-module counts, or bounded node-ID samples. The "
    "next safe step is to choose a controlled source-recovery method that recovers "
    "or exposes module-grouping detail without inventing module identities and "
    "without rerunning the failed authoritative retry."
)
REVIEWED_BOUNDARY = (
    "Candidate-only reviewed; no cache read, source recovery, diagnostics, "
    "remediation, classification, retry, results review, main merge, or runtime "
    "authority is created by this artifact."
)
REVIEWED_GOAL = (
    "Define safe future packages to recover a module-grouping detail source "
    "sufficient for re-entering prioritized planning, while preserving all "
    "unsupported-claim and failed-retry boundaries."
)

PACKAGE_REVIEW_STATUS_BY_SOURCE_STATUS = {
    source.RECOMMENDATION_STATUS: "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
    "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL": "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED",
    "BLOCKED_NOT_SUFFICIENT": "REVIEWED_BLOCKED_NOT_SUFFICIENT",
    "BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
}
REVIEWED_PACKAGES = [
    {
        "package_id": package["package_id"],
        "source_status": package["status"],
        "review_status": PACKAGE_REVIEW_STATUS_BY_SOURCE_STATUS[package["status"]],
        "selected": False,
        "approved": False,
        "executed": False,
    }
    for package in source.PROPOSED_PACKAGES
]
REVIEWED_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_SOURCE_RECOVERY",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_REQUIREMENTS
]
REVIEWED_FUTURE_PLAN = [
    {
        "step_id": step["step_id"],
        "description": step["description"],
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for step in source.FUTURE_PLAN
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": output["output_id"],
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for output in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.NON_GOALS
]
NEXT_CHAIN = [
    "Module Grouping Source Recovery Approval v1, if selected.",
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
    "module_grouping_source_recovery_approval_if_selected",
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
    "review_source_recovery_does_not_select_package",
    "review_source_recovery_does_not_approve_package",
    *[
        control.replace("candidate_source_recovery", "review_source_recovery")
        for control in source.RISK_CONTROLS
        if control != "separate_operator_review_required"
    ],
]
CHECK_IDS = [
    "source_candidate_digest_bound",
    "source_blocked_after_v2_execution_digest_bound",
    "source_blocked_after_v2_manifest_digest_bound",
    "source_blocked_reason_bound",
    "source_after_v2_approval_digest_bound",
    "source_after_v2_operator_review_digest_bound",
    "source_after_v2_candidate_digest_bound",
    "source_results_review_v2_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "classification_evidence_summary_bound",
    "module_count_29_bound",
    "largest_module_counts_bound",
    "known_missing_detail_bound",
    "unsupported_claims_boundary_bound",
    "review_created_true",
    "review_ready_true",
    "packages_reviewed_true",
    "future_requirements_reviewed_true",
    "future_plan_reviewed_true",
    "planned_outputs_reviewed_true",
    "non_goals_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "packages_reviewed_10",
    "blocked_packages_reviewed_5",
    "source_recovery_selected_false",
    "source_recovery_approved_false",
    "source_recovery_authorized_false",
    "source_recovery_executed_false",
    "module_grouping_detail_recovered_false",
    "module_grouping_detail_exposed_false",
    "module_paths_recovered_false",
    "per_module_counts_recovered_false",
    "bounded_nodeid_samples_recovered_false",
    "remediation_or_method_reentry_created_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "cache_read_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "pytest_cache_committed_false",
    "evidence_regenerated_false",
    "provider_requests_false",
    "market_data_acquisition_false",
    "dataset_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "recommendations_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "broker_not_authorized",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
    ValueError
):
    """Raised when the operator review crosses its review-only boundary."""


def _source_fields() -> dict[str, Any]:
    fields = source._source_fields()
    return {
        "source_module_grouping_source_recovery_candidate_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1,
        "source_module_grouping_source_recovery_candidate_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_module_grouping_source_recovery_candidate_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN,
        "source_module_grouping_source_recovery_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        **deepcopy(fields),
    }


def _base() -> dict[str, Any]:
    common_source = source._base()
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **_source_fields(),
        "classification_evidence_summary": source._classification_summary(),
        "known_available_detail": list(source.KNOWN_AVAILABLE_DETAIL),
        "known_missing_detail": list(source.KNOWN_MISSING_DETAIL),
        "unsupported_claims_boundary": deepcopy(source.UNSUPPORTED_CLAIMS_BOUNDARY),
        "origin_main_commit": common_source["origin_main_commit"],
        "integration_branch_name": common_source["integration_branch_name"],
        "integration_branch_head_commit": common_source["integration_branch_head_commit"],
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": (
            "C:\\Users\\Aspire5 15 i7 4G2050\\marketflow_worktrees\\"
            "integration-terminal-evidence-stack-validation-v1"
        ),
        "detached_integration_worktree_head_commit": common_source["integration_branch_head_commit"],
        "staged_evidence_manifest_digest": common_source["staged_evidence_manifest_digest"],
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "module_grouping_source_recovery_candidate_created": True,
        "module_grouping_source_recovery_candidate_ready_for_operator_review": True,
        "ready_for_module_grouping_source_recovery_operator_review": True,
        "module_grouping_source_recovery_candidate_operator_review_created": True,
        "module_grouping_source_recovery_candidate_operator_review_ready": True,
        "source_recovery_packages_reviewed": True,
        "future_source_recovery_requirements_reviewed": True,
        "future_source_recovery_plan_reviewed": True,
        "planned_outputs_reviewed": True,
        "non_goals_reviewed": True,
        "ready_for_module_grouping_source_recovery_approval": False,
        "module_grouping_source_recovery_selected": False,
        "module_grouping_source_recovery_approved": False,
        "module_grouping_source_recovery_authorized": False,
        "module_grouping_source_recovery_executed": False,
        "module_grouping_detail_recovered": False,
        "module_grouping_detail_exposed": False,
        "module_paths_recovered": False,
        "per_module_counts_recovered": False,
        "bounded_nodeid_samples_recovered": False,
        "remediation_or_method_after_v2_reentry_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "cache_read": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
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
        "reviewed_module_grouping_source_recovery_candidate_philosophy": REVIEWED_PHILOSOPHY,
        "reviewed_candidate_boundary": REVIEWED_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_GOAL,
        "candidate_philosophy_review_status": "REVIEWED_PLANNING_ONLY",
        "reviewed_packages": deepcopy(REVIEWED_PACKAGES),
        "reviewed_future_source_recovery_requirements": deepcopy(REVIEWED_REQUIREMENTS),
        "reviewed_future_source_recovery_plan": deepcopy(REVIEWED_FUTURE_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommended_module_grouping_source_recovery_package": source.RECOMMENDED_PACKAGE,
        "recommended_package_source_status": source.RECOMMENDATION_STATUS,
        "recommended_package_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_package_selected": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
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


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    blocked_packages = [
        package
        for package in review.get("reviewed_packages", [])
        if "BLOCKED" in str(package.get("review_status", ""))
    ]
    false_fields = {
        "ready_for_approval_false": "ready_for_module_grouping_source_recovery_approval",
        "source_recovery_selected_false": "module_grouping_source_recovery_selected",
        "source_recovery_approved_false": "module_grouping_source_recovery_approved",
        "source_recovery_authorized_false": "module_grouping_source_recovery_authorized",
        "source_recovery_executed_false": "module_grouping_source_recovery_executed",
        "module_grouping_detail_recovered_false": "module_grouping_detail_recovered",
        "module_grouping_detail_exposed_false": "module_grouping_detail_exposed",
        "module_paths_recovered_false": "module_paths_recovered",
        "per_module_counts_recovered_false": "per_module_counts_recovered",
        "bounded_nodeid_samples_recovered_false": "bounded_nodeid_samples_recovered",
        "remediation_or_method_reentry_created_false": "remediation_or_method_after_v2_reentry_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "retry_rerun_false": "retry_rerun_performed",
        "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed",
        "diagnostic_output_false": "diagnostic_output_captured",
        "cache_read_false": "cache_read",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_review",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_false": "dataset_generation_performed_in_review",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values: dict[str, tuple[Any, Any]] = {
        "source_candidate_digest_bound": (SOURCE_CANDIDATE_DIGEST, review.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.SOURCE_BLOCKED_EXECUTION_DIGEST, review.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.SOURCE_BLOCKED_MANIFEST_DIGEST, review.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.source.BLOCKED_REASON_MODULE_DETAIL, review.get("blocked_reason")),
        "source_after_v2_approval_digest_bound": (source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST, review.get("source_after_v2_approval_digest")),
        "source_after_v2_operator_review_digest_bound": (source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, review.get("source_after_v2_operator_review_digest")),
        "source_after_v2_candidate_digest_bound": (source.source.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST, review.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, review.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, review.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, review.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "classification_evidence_summary_bound": (source._classification_summary(), review.get("classification_evidence_summary")),
        "module_count_29_bound": (29, review.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], review.get("largest_module_nodeid_counts")),
        "known_missing_detail_bound": (source.KNOWN_MISSING_DETAIL, review.get("known_missing_detail")),
        "unsupported_claims_boundary_bound": (source.UNSUPPORTED_CLAIMS_BOUNDARY, review.get("unsupported_claims_boundary")),
        "review_created_true": (True, review.get("module_grouping_source_recovery_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("module_grouping_source_recovery_candidate_operator_review_ready")),
        "packages_reviewed_true": (True, review.get("source_recovery_packages_reviewed")),
        "future_requirements_reviewed_true": (True, review.get("future_source_recovery_requirements_reviewed")),
        "future_plan_reviewed_true": (True, review.get("future_source_recovery_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "recommended_package_reviewed_not_selected": (False, review.get("recommended_package_selected")),
        "packages_reviewed_10": (10, len(review.get("reviewed_packages", []))),
        "blocked_packages_reviewed_5": (5, len(blocked_packages)),
        "successful_integration_digest_false": ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
    }
    values.update({check_id: (False, review.get(field)) for check_id, field in false_fields.items()})
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(item["severity"] == BLOCKER for item in failed),
        "module_grouping_source_recovery_candidate_operator_review_created": True,
        "module_grouping_source_recovery_candidate_operator_review_ready": True,
        "source_recovery_packages_reviewed": True,
        "recommended_module_grouping_source_recovery_package": source.RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "ready_for_module_grouping_source_recovery_approval": False,
        "source_recovery_executed": False,
        "module_grouping_detail_recovered": False,
        "module_paths_recovered": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(
    *, source_candidate: dict | None = None
) -> dict:
    """Build the deterministic operator review without selecting a package."""
    if source_candidate is not None:
        source.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(source_candidate)
        if source_candidate.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest") != SOURCE_CANDIDATE_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
                "source candidate digest mismatch"
            )
    review = _base()
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest"] = marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest_v1(review)
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings and all review-only authority boundaries."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
            "review must be an object"
        )
    expected = _base()
    for field, value in expected.items():
        _expect(review.get(field), value, field)
    checklist = _checklist(review)
    _expect(review.get("checklist"), checklist, "checklist")
    summary = _summary(checklist)
    _expect(review.get("summary"), summary, "summary")
    digest = review.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
            "operator-review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest_v1(review),
        "operator_review_digest",
    )
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError(
            f"operator review has {len(failed)} failed checks"
        )
    return deepcopy(summary)


def write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict:
    """Write the review JSON to an explicitly supplied output directory."""
    review = build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(source_candidate=source_candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1.json"
    path.write_bytes(canonical_json_bytes(review) + b"\n")
    return {"path": str(path), "review": review}


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review as Markdown."""
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(review)
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Candidate Operator Review v1",
        "",
        "## Source Module Grouping Source Recovery Candidate",
        "",
        f"- Candidate digest: `{review['source_module_grouping_source_recovery_candidate_digest']}`",
        "",
        "## Source Blocked After-v2 Execution",
        "",
        f"- Execution digest: `{review['source_blocked_after_v2_execution_digest']}`",
        f"- Blocked-manifest digest: `{review['source_blocked_after_v2_manifest_digest']}`",
        "",
        "## Source Classification Results Review v2",
        "",
        f"- Results-review digest: `{review['source_results_review_v2_digest']}`",
        f"- Module-grouping digest: `{review['source_module_grouping_digest']}`",
        "",
        "## Retry Failure Context",
        "",
        "The authoritative retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped.",
        "",
        "## Known Available and Missing Detail",
        "",
        *[f"- Available: {item}" for item in review["known_available_detail"]],
        *[f"- Missing: {item}" for item in review["known_missing_detail"]],
        "",
        "## Review Scope",
        "",
        f"`{review['review_scope']}`",
        "",
        "## Reviewed Candidate Philosophy",
        "",
        review["reviewed_module_grouping_source_recovery_candidate_philosophy"],
        "",
        "## Reviewed Module Grouping Source Recovery Packages",
        "",
        *[f"- `{package['package_id']}`: {package['review_status']}" for package in review["reviewed_packages"]],
        "",
        "## Reviewed Future Source Recovery Requirements",
        "",
        f"{len(REVIEWED_REQUIREMENTS)} requirements remain future-only and unexecuted.",
        "",
        "## Reviewed Future Source Recovery Plan",
        "",
        *[f"- {step['description']} ({step['review_status']})" for step in review["reviewed_future_source_recovery_plan"]],
        "",
        "## Reviewed Planned Outputs",
        "",
        *[f"- `{output['output_id']}`: {output['review_status']}" for output in review["reviewed_planned_outputs"]],
        "",
        "## Reviewed Non-Goals",
        "",
        f"{len(REVIEWED_NON_GOALS)} non-goals remain active.",
        "",
        "## Recommendation",
        "",
        f"- Package: `{review['recommended_module_grouping_source_recovery_package']}`",
        f"- Selected: `{review['recommended_package_selected']}`",
        f"- Next status: `{review['recommended_next_task_status']}`",
        "",
        "## Next Chain",
        "",
        *[f"- {item}" for item in review["next_chain"]],
        "",
        "## Next Gates",
        "",
        *[f"- `{item}`" for item in review["next_gates"]],
        "",
        "## Risk Controls",
        "",
        f"{len(RISK_CONTROLS)} controls preserve the review-only boundary.",
        "",
        "## Authority Boundaries",
        "",
        review["reviewed_candidate_boundary"],
        "",
        "## Checklist Summary",
        "",
        f"{review['summary']['passed_checks']}/{review['summary']['total_checks']} checks pass.",
        "",
        "## Guardrails",
        "",
        "No selection, approval, cache read, recovery, diagnostics, remediation, retry, runtime use, or trading is performed.",
        "",
    ]
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_markdown_v1",
]
