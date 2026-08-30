"""Review the retry-failure remediation-or-method candidate offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_METHOD_CANDIDATE_DIGEST = "414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_RETRY_FAILURE_METHOD_EXECUTION"
)
RECOMMENDATION_REASON = (
    "The remediation-or-method candidate has been reviewed, but no package has been "
    "selected or approved by this review."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_CANDIDATE_PHILOSOPHY = source.CANDIDATE_PHILOSOPHY
REVIEWED_CANDIDATE_BOUNDARY = (
    "Candidate-only reviewed; no diagnostic execution, remediation, retry, results "
    "review, integration success, main merge, or runtime authority is created by this artifact."
)
REVIEWED_CANDIDATE_GOAL = source.CANDIDATE_GOAL
REVIEW_DISPOSITION = "REVIEWED_PLANNING_ONLY"


def _review_status(source_status: str) -> str:
    if source_status == source.RECOMMENDATION_STATUS:
        return "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    if source_status == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED":
        return "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
    if source_status == "BLOCKED_NOT_RECOMMENDED":
        return "REVIEWED_BLOCKED_NOT_RECOMMENDED"
    if source_status == "BLOCKED_NOT_ALLOWED":
        return "REVIEWED_BLOCKED_NOT_ALLOWED"
    raise ValueError(f"unsupported source package status: {source_status}")


REVIEWED_METHOD_PACKAGES = [
    {
        "package_id": row["package_id"],
        "source_status": row["status"],
        "review_status": _review_status(row["status"]),
        "selected": False,
        "approved": False,
        "executed": False,
    }
    for row in source.METHOD_PACKAGES
]
REVIEWED_FUTURE_METHOD_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_METHOD_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_METHOD_REQUIREMENTS
]
REVIEWED_FUTURE_METHOD_PLAN = [
    {
        "step_id": f"step_{index:02d}",
        "source_step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_METHOD_PLAN, start=1)
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": row["output_id"],
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for row in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.NON_GOALS
]

NEXT_CHAIN = [
    "Retry Failure Remediation or Method Approval v1, if selected.",
    "Retry Failure Remediation or Method Execution v1, if approved.",
    "Retry Failure Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "retry_failure_method_approval_if_selected", "retry_failure_method_execution_if_approved",
    "retry_failure_method_results_review", "new_integration_branch_retry_candidate_after_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_select_method_package", "review_does_not_approve_method",
    "review_does_not_execute_method", "review_does_not_run_diagnostic_commands",
    "review_does_not_rerun_retry", "review_does_not_run_full_pytest",
    "review_does_not_treat_diagnostics_as_retry_evidence",
    "review_does_not_create_retry_results_review", "review_does_not_create_integration_results_review",
    "review_does_not_mark_integration_successful",
    "review_does_not_generate_successful_integration_execution_digest",
    "review_does_not_generate_successful_integration_validation_digest",
    "review_does_not_stage_additional_evidence", "review_does_not_modify_staged_evidence",
    "review_does_not_regenerate_evidence", "review_does_not_call_providers",
    "review_does_not_commit_marketflow_outputs", "review_does_not_push_integration_branch",
    "review_does_not_push_main", "review_does_not_delete_integration_branch",
    "review_does_not_delete_worktree", "review_does_not_force_push",
    "review_does_not_prune_remotes", "review_does_not_modify_tags",
    "review_does_not_acquire_market_data", "review_does_not_regenerate_dataset",
    "review_does_not_recompute_metrics", "review_does_not_train_models",
    "review_does_not_score_strategy", "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness", "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime", "review_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_approval_required_before_method_execution",
    "separate_results_review_required_after_method_execution",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_method_candidate_digest_bound", "source_retry_failure_diagnosis_digest_bound",
    "source_retry_approval_digest_bound", "source_retry_operator_review_digest_bound",
    "source_retry_candidate_digest_bound", "source_remediation_results_review_digest_bound",
    "source_remediation_execution_digest_bound", "source_staged_inventory_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "original_failure_comparison_bound",
    "root_regression_boundary_bound", "origin_main_bound", "integration_branch_head_bound",
    "detached_worktree_head_bound", "staged_evidence_digest_bound", "review_created_true",
    "review_ready_true", "method_packages_reviewed_true", "future_method_requirements_reviewed_true",
    "future_method_plan_reviewed_true", "planned_outputs_reviewed_true", "non_goals_reviewed_true",
    "ready_for_approval_false", "recommended_package_reviewed_not_selected",
    "method_packages_reviewed_8", "blocked_packages_reviewed_3", "method_selected_false",
    "method_approved_false", "method_authorized_false", "method_executed_false",
    "new_remediation_candidate_created_false", "new_retry_candidate_created_false",
    "new_retry_approved_false", "new_retry_executed_false",
    "new_retry_results_review_created_false", "main_merge_approval_created_false",
    "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(ValueError):
    """Raised when operator-review evidence or authority boundaries are invalid."""


def _source_candidate() -> dict[str, Any]:
    return {
        "source_retry_failure_method_candidate_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1,
        "source_retry_failure_method_candidate_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_retry_failure_method_candidate_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_retry_failure_method_candidate_digest": SOURCE_METHOD_CANDIDATE_DIGEST,
        **source._source_diagnosis(),
    }


def _base_review(source_candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        **deepcopy(dict(source_candidate)),
        "retry_failure_candidate_created": True,
        "retry_failure_candidate_ready_for_operator_review": True,
        "retry_failure_candidate_operator_review_created": True,
        "retry_failure_candidate_operator_review_ready": True,
        "method_packages_reviewed": True, "future_method_requirements_reviewed": True,
        "future_method_plan_reviewed": True, "planned_outputs_reviewed": True,
        "non_goals_reviewed": True, "ready_for_retry_failure_method_approval": False,
        "retry_failure_method_selected": False, "retry_failure_method_approved": False,
        "retry_failure_method_authorized": False, "retry_failure_method_executed": False,
        "new_remediation_candidate_created": False, "new_retry_candidate_created": False,
        "new_retry_approved": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "reviewed_candidate_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
        "review_disposition": REVIEW_DISPOSITION,
        "reviewed_method_packages": deepcopy(REVIEWED_METHOD_PACKAGES),
        "reviewed_future_method_requirements": deepcopy(REVIEWED_FUTURE_METHOD_REQUIREMENTS),
        "reviewed_future_method_plan": deepcopy(REVIEWED_FUTURE_METHOD_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommended_retry_failure_method_package": source.RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION, "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_method_packages") if isinstance(review.get("reviewed_method_packages"), list) else []
    recommended = next((row for row in packages if row.get("package_id") == source.RECOMMENDED_PACKAGE), {})
    blocked = [row for row in packages if str(row.get("source_status", "")).startswith("BLOCKED_")]
    retry_counts = {"passed": review.get("retry_pytest_passed_count"), "failed": review.get("retry_pytest_failed_count"), "errors": review.get("retry_pytest_error_count"), "skipped": review.get("retry_pytest_skipped_count")}
    original_counts = {"passed": review.get("original_failed_run_passed_count"), "failed": review.get("original_failed_run_failed_count"), "errors": review.get("original_failed_run_error_count"), "skipped": review.get("original_failed_run_skipped_count")}
    values: dict[str, tuple[Any, Any]] = {
        "source_method_candidate_digest_bound": (SOURCE_METHOD_CANDIDATE_DIGEST, review.get("source_retry_failure_method_candidate_digest")),
        "source_retry_failure_diagnosis_digest_bound": (source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, review.get("source_retry_failure_diagnosis_digest")),
        "source_retry_approval_digest_bound": (source.SOURCE_RETRY_APPROVAL_DIGEST, review.get("source_retry_approval_digest")),
        "source_retry_operator_review_digest_bound": (source.SOURCE_RETRY_OPERATOR_REVIEW_DIGEST, review.get("source_retry_operator_review_digest")),
        "source_retry_candidate_digest_bound": (source.SOURCE_RETRY_CANDIDATE_DIGEST, review.get("source_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (source.SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, review.get("source_remediation_results_review_digest")),
        "source_remediation_execution_digest_bound": (source.SOURCE_REMEDIATION_EXECUTION_DIGEST, review.get("source_remediation_execution_digest")),
        "source_staged_inventory_digest_bound": (source.SOURCE_STAGED_INVENTORY_DIGEST, review.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": (source.source.RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        "retry_failure_counts_bound": (source.source.RETRY_FAILED_RUN, retry_counts),
        "original_failure_comparison_bound": (source.source.ORIGINAL_FAILED_RUN, original_counts),
        "root_regression_boundary_bound": ([29200, 7, False, True], [review.get("root_full_regression_passed_count"), review.get("root_full_regression_skipped_count"), review.get("root_full_regression_is_retry_evidence"), review.get("root_full_regression_does_not_override_detached_retry_failure")]),
        "origin_main_bound": (source.source.ORIGIN_MAIN_COMMIT, review.get("origin_main_commit")),
        "integration_branch_head_bound": (source.source.INTEGRATION_BRANCH_HEAD_COMMIT, review.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": (source.source.INTEGRATION_BRANCH_HEAD_COMMIT, review.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": (source.SOURCE_STAGED_INVENTORY_DIGEST, review.get("staged_evidence_manifest_digest")),
        "review_created_true": (True, review.get("retry_failure_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("retry_failure_candidate_operator_review_ready")),
        "method_packages_reviewed_true": (True, review.get("method_packages_reviewed")),
        "future_method_requirements_reviewed_true": (True, review.get("future_method_requirements_reviewed")),
        "future_method_plan_reviewed_true": (True, review.get("future_method_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_retry_failure_method_approval")),
        "recommended_package_reviewed_not_selected": (["REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", False], [recommended.get("review_status"), recommended.get("selected")]),
        "method_packages_reviewed_8": (8, len(packages)), "blocked_packages_reviewed_3": (3, len(blocked)),
        "method_selected_false": (False, review.get("retry_failure_method_selected")),
        "method_approved_false": (False, review.get("retry_failure_method_approved")),
        "method_authorized_false": (False, review.get("retry_failure_method_authorized")),
        "method_executed_false": (False, review.get("retry_failure_method_executed")),
        "new_remediation_candidate_created_false": (False, review.get("new_remediation_candidate_created")),
        "new_retry_candidate_created_false": (False, review.get("new_retry_candidate_created")),
        "new_retry_approved_false": (False, review.get("new_retry_approved")),
        "new_retry_executed_false": (False, review.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, review.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, review.get("main_merge_approval_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, review.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, review.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
        "provider_requests_false": (False, review.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, review.get("market_data_acquisition_performed_in_review")),
        "dataset_generation_false": (False, review.get("dataset_generation_performed_in_review")),
        "metric_recomputation_false": (False, review.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, review.get("model_training_performed")),
        "strategy_scoring_false": (False, review.get("strategy_scoring_performed")),
        "recommendations_false": (False, review.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (True, review.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "retry_failure_candidate_operator_review_created": True,
        "retry_failure_candidate_operator_review_ready": True, "method_packages_reviewed": True,
        "recommended_retry_failure_method_package": source.RECOMMENDED_PACKAGE,
        "recommended_package_selected": False, "ready_for_retry_failure_method_approval": False,
        "method_executed": False, "new_retry_candidate_created": False,
        "new_retry_executed": False, "main_merge_approval_created": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic operator-review digest."""
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the operator review from committed candidate constants without external I/O."""
    evidence = _source_candidate()
    if source_candidate is not None:
        if not isinstance(source_candidate, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
                "source_candidate must be an object"
            )
        evidence.update(deepcopy(source_candidate))
    review = _base_review(evidence)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"] = (
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact source evidence and reject selection, approval, or execution."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_source_candidate(), "reviewed_candidate_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL, "review_disposition": REVIEW_DISPOSITION,
        "reviewed_method_packages": REVIEWED_METHOD_PACKAGES,
        "reviewed_future_method_requirements": REVIEWED_FUTURE_METHOD_REQUIREMENTS,
        "reviewed_future_method_plan": REVIEWED_FUTURE_METHOD_PLAN,
        "reviewed_planned_outputs": REVIEWED_PLANNED_OUTPUTS,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommended_retry_failure_method_package": source.RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION, "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in static.items():
        _expect(review.get(field), expected, field)
    if not re.fullmatch(r"[0-9a-f]{40}", str(review.get("retry_execution_commit", ""))):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "retry_execution_commit invalid"
        )
    required_true = (
        "created_offline", "governance_only", "operator_review_only",
        "retry_failure_candidate_created", "retry_failure_candidate_ready_for_operator_review",
        "retry_failure_candidate_operator_review_created", "retry_failure_candidate_operator_review_ready",
        "method_packages_reviewed", "future_method_requirements_reviewed", "future_method_plan_reviewed",
        "planned_outputs_reviewed", "non_goals_reviewed", "no_tracked_marketflow_files",
    )
    required_false = (
        "root_full_regression_is_retry_evidence", "ready_for_retry_failure_method_approval",
        "retry_failure_method_selected", "retry_failure_method_approved",
        "retry_failure_method_authorized", "retry_failure_method_executed",
        "new_remediation_candidate_created", "new_retry_candidate_created", "new_retry_approved",
        "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed",
        "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
        "evidence_regenerated", "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
    )
    for field in required_true:
        _expect(review.get(field), True, field)
    for field in required_false:
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    packages = review.get("reviewed_method_packages")
    if not isinstance(packages, list) or len(packages) != 8:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "package review missing"
        )
    if any(row.get("selected") or row.get("approved") or row.get("executed") for row in packages):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "method selected, approved, or executed"
        )
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "operator review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest_v1(review),
        "operator review digest",
    )
    return {
        "status": review["review_status"], "artifact_kind": review["artifact_kind"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(review)
    sections = [
        ("Source Method Candidate", [f"Artifact/digest: `{review['source_retry_failure_method_candidate_artifact_kind']}` / `{review['source_retry_failure_method_candidate_digest']}`."]),
        ("Source Retry Failure Diagnosis", [f"Digest: `{review['source_retry_failure_diagnosis_digest']}`."]),
        ("Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The failed retry remains authoritative."]),
        ("Retry Environment", [f"Detached worktree: `{review['retry_pytest_working_directory']}`."]),
        ("Review Scope", [review["reviewed_candidate_boundary"]]),
        ("Reviewed Candidate Philosophy", [review["reviewed_candidate_philosophy"], review["reviewed_candidate_goal"], f"Disposition: `{review['review_disposition']}`."]),
        ("Reviewed Method Packages", [f"`{row['package_id']}`: `{row['review_status']}`" for row in review["reviewed_method_packages"]]),
        ("Reviewed Future Method Requirements", [f"`{row['requirement_id']}`: `{row['review_status']}` / `{row['execution_status']}`" for row in review["reviewed_future_method_requirements"]]),
        ("Reviewed Future Method Plan", [f"`{row['step_id']}`: `{row['review_status']}` / `{row['execution_status']}`" for row in review["reviewed_future_method_plan"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_id']}`: `{row['review_status']}` / `{row['generation_status']}`" for row in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}`: `{row['review_status']}`" for row in review["reviewed_non_goals"]]),
        ("Recommendation", [f"Next task: `{review['recommended_next_task']}`.", review["recommendation_reason"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No method selection, approval, execution, retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The root regression is not retry evidence.", "Optional operator selection and separate approval are required before method execution."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical operator-review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateOperatorReviewError(
            "operator review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
