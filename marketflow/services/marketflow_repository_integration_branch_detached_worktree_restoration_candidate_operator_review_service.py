"""Offline operator review of the detached-worktree restoration candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_candidate_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY = (
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "a782d45a62b9d589381c1c50d0312312ca059b389aa60d8a7bdd3f8902ab39d6"
)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
REVIEWED_PLANNING_ONLY = "REVIEWED_PLANNING_ONLY"

REVIEW_STATUS_BY_SOURCE_STATUS = {
    source.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED: (
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    ),
    source.AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED: "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    source.BLOCKED_NOT_RECOMMENDED: "REVIEWED_BLOCKED_NOT_RECOMMENDED",
    source.BLOCKED_NOT_ALLOWED: "REVIEWED_BLOCKED_NOT_ALLOWED",
}


def _reviewed_packages() -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    for package in source.WORKTREE_RESTORATION_PACKAGES:
        row = {
            "package_id": package["package_id"],
            "source_status": package["status"],
            "review_status": REVIEW_STATUS_BY_SOURCE_STATUS[package["status"]],
            "purpose": package["purpose"],
            "selected": False,
            "approved": False,
            "executed": False,
        }
        for optional in ("recommended_for", "blocked_reason"):
            if optional in package:
                row[optional] = package[optional]
        packages.append(row)
    return packages


REVIEWED_WORKTREE_RESTORATION_PACKAGES = _reviewed_packages()
REVIEWED_WORKTREE_RESTORATION_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "source_value": source_value,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_WORKTREE_RESTORATION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id, source_value in source.WORKTREE_RESTORATION_REQUIREMENTS.items()
]
REVIEWED_FUTURE_WORKTREE_RESTORATION_PLAN = [
    {
        "step_id": f"STEP_{index:02d}",
        "instruction": instruction,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, instruction in enumerate(source.FUTURE_WORKTREE_RESTORATION_PLAN, start=1)
]
REVIEWED_WORKTREE_RESTORATION_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.WORKTREE_RESTORATION_NON_GOALS
]

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_WORKTREE_RESTORATION"
)
RECOMMENDATION_REASON = (
    "The worktree restoration candidate has been reviewed, but no package has been selected or approved by this review."
)

NEXT_CHAIN = [
    "Worktree Restoration Approval v1, if selected.",
    "Worktree Restoration Execution v1, if approved.",
    "Worktree Restoration Results Review v1.",
    "Remediation Execution v1 retry, only after worktree restoration review passes.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1.",
    "Integration Branch Retry Approval v1.",
    "Integration Branch Retry Execution v1.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "worktree_restoration_approval_if_selected",
    "worktree_restoration_execution_if_approved",
    "worktree_restoration_results_review",
    "remediation_execution_after_worktree_restoration",
    "remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_select_worktree_restoration", "review_does_not_approve_worktree_restoration",
    "review_does_not_create_worktree", "review_does_not_restore_worktree",
    "review_does_not_delete_worktree", "review_does_not_reset_integration_branch",
    "review_does_not_delete_integration_branch", "review_does_not_recreate_integration_branch",
    "review_does_not_stage_evidence", "review_does_not_copy_marketflow_outputs",
    "review_does_not_commit_marketflow_outputs", "review_does_not_run_pytest_retry",
    "review_does_not_create_results_review", "review_does_not_push_integration_branch",
    "review_does_not_push_main", "review_does_not_force_push", "review_does_not_prune_remotes",
    "review_does_not_modify_tags", "review_does_not_call_providers",
    "review_does_not_acquire_market_data", "review_does_not_regenerate_dataset",
    "review_does_not_recompute_metrics", "review_does_not_train_models",
    "review_does_not_score_strategy", "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness", "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime", "review_does_not_authorize_broker_execution",
    "separate_approval_required_before_worktree_restoration",
    "separate_results_review_required_after_worktree_restoration",
    "separate_remediation_execution_required_after_worktree_restoration",
    "protect_origin_main", "preserve_existing_integration_branch", "preserve_failed_gate",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound", "source_remediation_approval_digest_bound",
    "source_operator_review_digest_bound", "source_remediation_candidate_digest_bound",
    "source_diagnosis_digest_bound", "blocked_execution_status_recorded",
    "integration_branch_exists_local_true", "integration_branch_head_bound",
    "detached_worktree_missing_recorded", "source_evidence_root_exists_recorded",
    "source_required_manifest_exists_recorded", "source_evidence_file_count_recorded",
    "marketflow_outputs_not_tracked", "origin_main_commit_bound", "review_created_true",
    "review_ready_true", "restoration_packages_reviewed_true",
    "restoration_requirements_reviewed_true", "future_restoration_plan_reviewed_true",
    "non_goals_reviewed_true", "ready_for_approval_false",
    "recommended_package_reviewed_not_selected", "restoration_packages_reviewed_6",
    "blocked_packages_reviewed_3", "worktree_restoration_selected_false",
    "worktree_restoration_approved_false", "worktree_restoration_executed_false",
    "detached_worktree_created_false", "detached_worktree_restored_false",
    "detached_worktree_deleted_false", "integration_branch_deleted_or_reset_false",
    "remediation_executed_false", "evidence_staged_false", "marketflow_outputs_copied_false",
    "marketflow_outputs_committed_false", "retry_candidate_created_false", "retry_executed_false",
    "results_review_created_false", "integration_execution_successful_false",
    "integration_branch_pushed_false", "main_push_false", "origin_main_modified_false",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
    ValueError
):
    """Raised when review evidence or review-only boundaries are invalid."""


def _source_candidate(source_candidate: dict | None) -> dict[str, Any]:
    candidate = (
        source.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1()
        if source_candidate is None
        else deepcopy(source_candidate)
    )
    validation = source.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
        candidate
    )
    if validation[
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"
    ] != EXPECTED_SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "source candidate digest mismatch"
        )
    return candidate


def _base_review(candidate: Mapping[str, Any]) -> dict[str, Any]:
    copied_fields = (
        "source_remediation_approval_digest", "source_remediation_operator_review_digest",
        "source_remediation_candidate_digest", "source_failure_diagnosis_digest",
        "source_merge_strategy_approval_digest", "blocked_remediation_execution_artifact_kind",
        "blocked_remediation_execution_status", "integration_branch_name",
        "integration_branch_head_commit", "integration_branch_exists_local",
        "integration_branch_matches_required_head", "detached_integration_worktree_exists",
        "registered_worktree_entries_present", "git_worktrees_directory_present",
        "remote_integration_branch_exists", "origin_main_commit", "source_evidence_root_path",
        "source_evidence_root_exists", "source_required_manifest_name",
        "source_required_manifest_exists", "source_evidence_file_count",
        "source_evidence_total_bytes", "source_evidence_ignored_by_gitignore",
        "marketflow_outputs_tracked", "tracked_marketflow_file_count", "no_tracked_marketflow_files",
        "worktree_restoration_candidate_created",
        "worktree_restoration_candidate_ready_for_operator_review",
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_worktree_restoration_candidate_artifact_kind": candidate["artifact_kind"],
        "source_worktree_restoration_candidate_status": candidate["candidate_status"],
        "source_worktree_restoration_candidate_scope": candidate["candidate_scope"],
        "source_worktree_restoration_candidate_digest": candidate[
            "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"
        ],
        **{field: deepcopy(candidate[field]) for field in copied_fields},
        "worktree_restoration_candidate_operator_review_created": True,
        "worktree_restoration_candidate_operator_review_ready": True,
        "restoration_packages_reviewed": True, "restoration_requirements_reviewed": True,
        "future_restoration_plan_reviewed": True, "restoration_non_goals_reviewed": True,
        "ready_for_worktree_restoration_approval": False,
        "worktree_restoration_selected": False, "worktree_restoration_approved": False,
        "worktree_restoration_authorized": False, "worktree_restoration_executed": False,
        "detached_worktree_created": False, "detached_worktree_restored": False,
        "detached_worktree_deleted": False, "integration_branch_deleted_or_reset": False,
        "remediation_executed": False, "evidence_staged": False,
        "marketflow_outputs_copied": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "integration_retry_candidate_created": False,
        "integration_retry_executed": False, "integration_results_review_created": False,
        "integration_execution_successful": False, "integration_branch_pushed": False,
        "main_push_performed": False, "origin_main_modified_by_this_task": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "reviewed_worktree_restoration_philosophy": source.WORKTREE_RESTORATION_PHILOSOPHY,
        "reviewed_worktree_restoration_boundary": "Candidate-only reviewed; no worktree is created, restored, deleted, reset, or used for remediation by this artifact.",
        "reviewed_worktree_restoration_goal": source.WORKTREE_RESTORATION_GOAL,
        "worktree_restoration_review_status": REVIEWED_PLANNING_ONLY,
        "reviewed_worktree_restoration_packages": deepcopy(REVIEWED_WORKTREE_RESTORATION_PACKAGES),
        "recommended_worktree_restoration_package": source.PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD,
        "recommended_package_selected": False,
        "reviewed_worktree_restoration_requirements": deepcopy(REVIEWED_WORKTREE_RESTORATION_REQUIREMENTS),
        "reviewed_future_worktree_restoration_plan": deepcopy(REVIEWED_FUTURE_WORKTREE_RESTORATION_PLAN),
        "reviewed_worktree_restoration_non_goals": deepcopy(REVIEWED_WORKTREE_RESTORATION_NON_GOALS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION, "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_worktree_restoration_packages", [])
    values: dict[str, tuple[Any, Any]] = {
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_worktree_restoration_candidate_digest")),
        "source_remediation_approval_digest_bound": (source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, review.get("source_remediation_approval_digest")),
        "source_operator_review_digest_bound": (source.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST, review.get("source_remediation_operator_review_digest")),
        "source_remediation_candidate_digest_bound": (source.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST, review.get("source_remediation_candidate_digest")),
        "source_diagnosis_digest_bound": (source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST, review.get("source_failure_diagnosis_digest")),
        "blocked_execution_status_recorded": (source.BLOCKED_REMEDIATION_EXECUTION_STATUS, review.get("blocked_remediation_execution_status")),
        "integration_branch_exists_local_true": (True, review.get("integration_branch_exists_local")),
        "integration_branch_head_bound": (source.INTEGRATION_BRANCH_HEAD_COMMIT, review.get("integration_branch_head_commit")),
        "detached_worktree_missing_recorded": (False, review.get("detached_integration_worktree_exists")),
        "source_evidence_root_exists_recorded": (True, review.get("source_evidence_root_exists")),
        "source_required_manifest_exists_recorded": (True, review.get("source_required_manifest_exists")),
        "source_evidence_file_count_recorded": (7, review.get("source_evidence_file_count")),
        "marketflow_outputs_not_tracked": (False, review.get("marketflow_outputs_tracked")),
        "origin_main_commit_bound": (source.ORIGIN_MAIN_COMMIT, review.get("origin_main_commit")),
        "review_created_true": (True, review.get("worktree_restoration_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("worktree_restoration_candidate_operator_review_ready")),
        "restoration_packages_reviewed_true": (True, review.get("restoration_packages_reviewed")),
        "restoration_requirements_reviewed_true": (True, review.get("restoration_requirements_reviewed")),
        "future_restoration_plan_reviewed_true": (True, review.get("future_restoration_plan_reviewed")),
        "non_goals_reviewed_true": (True, review.get("restoration_non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_worktree_restoration_approval")),
        "recommended_package_reviewed_not_selected": (False, review.get("recommended_package_selected")),
        "restoration_packages_reviewed_6": (6, len(packages)),
        "blocked_packages_reviewed_3": (3, sum(row.get("source_status", "").startswith("BLOCKED_") for row in packages)),
        "worktree_restoration_selected_false": (False, review.get("worktree_restoration_selected")),
        "worktree_restoration_approved_false": (False, review.get("worktree_restoration_approved")),
        "worktree_restoration_executed_false": (False, review.get("worktree_restoration_executed")),
        "detached_worktree_created_false": (False, review.get("detached_worktree_created")),
        "detached_worktree_restored_false": (False, review.get("detached_worktree_restored")),
        "detached_worktree_deleted_false": (False, review.get("detached_worktree_deleted")),
        "integration_branch_deleted_or_reset_false": (False, review.get("integration_branch_deleted_or_reset")),
        "remediation_executed_false": (False, review.get("remediation_executed")),
        "evidence_staged_false": (False, review.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, review.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "retry_candidate_created_false": (False, review.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, review.get("integration_retry_executed")),
        "results_review_created_false": (False, review.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
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
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "worktree_restoration_candidate_operator_review_created": True,
        "worktree_restoration_candidate_operator_review_ready": True,
        "restoration_packages_reviewed": True,
        "recommended_worktree_restoration_package": source.PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD,
        "recommended_package_selected": False, "ready_for_worktree_restoration_approval": False,
        "detached_worktree_created": False, "worktree_restoration_executed": False,
        "remediation_execution_ready_now": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic review digest."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the review offline without selecting or executing restoration."""
    review = _base_review(_source_candidate(source_candidate))
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
        review
    )
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings and every review-only boundary."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "review must be an object"
        )
    expected = _base_review(
        source.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1()
    )
    for field, value in expected.items():
        _expect(review.get(field), value, field)
    for field in ("integration_branch_head_commit", "origin_main_commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(review.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
                f"{field} invalid"
            )
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest_v1(review),
        "review digest",
    )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY,
        "artifact_kind": review["artifact_kind"], "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a validated governance-only operator review."""
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
        review
    )
    sections = [
        ("Source Restoration Candidate", [f"Artifact/status/digest: `{review['source_worktree_restoration_candidate_artifact_kind']}` / `{review['source_worktree_restoration_candidate_status']}` / `{review['source_worktree_restoration_candidate_digest']}`."]),
        ("Blocked Remediation Execution Observation", [f"`{review['blocked_remediation_execution_artifact_kind']}` / `{review['blocked_remediation_execution_status']}`.", f"Integration branch/head: `{review['integration_branch_name']}` / `{review['integration_branch_head_commit']}`."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Reviewed Worktree Restoration Philosophy", [review["reviewed_worktree_restoration_philosophy"], review["reviewed_worktree_restoration_boundary"], review["reviewed_worktree_restoration_goal"]]),
        ("Reviewed Restoration Packages", [f"`{row['package_id']}`: `{row['source_status']}` / `{row['review_status']}`; selected/approved/executed `{row['selected']} / {row['approved']} / {row['executed']}`." for row in review["reviewed_worktree_restoration_packages"]]),
        ("Reviewed Restoration Requirements", [f"`{row['requirement_id']}`: `{row['review_status']}` / `{row['execution_status']}`." for row in review["reviewed_worktree_restoration_requirements"]]),
        ("Reviewed Future Restoration Plan", [f"`{row['step_id']}`: {row['instruction']} (`{row['review_status']}` / `{row['execution_status']}`)" for row in review["reviewed_future_worktree_restoration_plan"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}`: `{row['review_status']}`." for row in review["reviewed_worktree_restoration_non_goals"]]),
        ("Recommendation", [f"`{review['recommended_action']}`.", review["recommendation_reason"], f"Next: `{review['recommended_next_task']}` / `{review['recommended_next_task_status']}`."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No restoration package is selected or approved; no worktree, remediation, retry, results review, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["A separate optional operator selection and approval is required before restoration.", "The failed integration gate remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
    output_dir: str | Path,
    *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError(
            "operator-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest": validation[
            "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
