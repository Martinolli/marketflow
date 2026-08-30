"""Offline operator review of the integration-branch retry candidate."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import marketflow_repository_integration_branch_retry_candidate_service as source


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_candidate_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN"
)

EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST = "35598851bf4bfec55385cd6e2559ebb933161d846302a3032861e72ed07985eb"
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST
EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST
EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST
EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST = source.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST = source.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_EXECUTED = "NOT_EXECUTED"
REVIEWED_PLANNING_ONLY = "REVIEWED_PLANNING_ONLY"
REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED = (
    "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
)
REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED = "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
REVIEWED_BLOCKED_NOT_ALLOWED = "REVIEWED_BLOCKED_NOT_ALLOWED"
REVIEWED_REQUIRED_FOR_FUTURE_RETRY = "REVIEWED_REQUIRED_FOR_FUTURE_RETRY"
REVIEWED_PLANNED_NOT_EXECUTED = "REVIEWED_PLANNED_NOT_EXECUTED"
REVIEWED_ACTIVE = "REVIEWED_ACTIVE"
FUTURE_APPROVAL_NOT_CREATED = "FUTURE_APPROVAL_NOT_CREATED"
OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_INTEGRATION_RETRY = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_INTEGRATION_RETRY"
)

NEXT_CHAIN = [
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval v1, only if retry results review passes.",
    "Main Merge Execution v1, only if separately approved.",
    "Branch Cleanup Candidate v1, only after merge strategy is settled.",
]
NEXT_GATES = [
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
    "main_merge_execution_if_approved",
    "branch_cleanup_candidate_after_merge_strategy",
]
RISK_CONTROLS = [
    "review_does_not_select_retry_package", "review_does_not_approve_retry",
    "review_does_not_run_retry", "review_does_not_run_pytest",
    "review_does_not_create_retry_execution", "review_does_not_create_retry_results_review",
    "review_does_not_create_integration_results_review", "review_does_not_mark_integration_successful",
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
    "staged_frozen_evidence_must_remain_untracked", "wrong_worktree_retry_must_fail_closed",
    "separate_approval_required_before_retry", "separate_results_review_required_after_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_V1_IF_SELECTED"

REQUIRED_CHECK_IDS = [
    "source_retry_candidate_digest_bound", "source_remediation_results_review_digest_bound",
    "source_remediation_results_review_evidence_manifest_digest_bound",
    "source_remediation_execution_digest_bound",
    "source_remediation_execution_evidence_manifest_digest_bound",
    "source_staged_inventory_digest_bound", "source_worktree_restoration_results_review_digest_bound",
    "source_remediation_approval_digest_bound", "source_diagnosis_digest_bound",
    "attempted_execution_commit_bound", "original_blocked_status_bound",
    "first_failed_pytest_preserved", "later_wrong_worktree_rerun_preserved",
    "origin_main_at_review_bound", "integration_branch_head_bound",
    "detached_worktree_path_bound", "detached_worktree_head_bound",
    "detached_worktree_clean_recorded", "staged_evidence_root_bound", "staged_manifest_bound",
    "staged_evidence_digest_bound", "review_created_true", "review_ready_true",
    "retry_packages_reviewed_true", "retry_requirements_reviewed_true",
    "future_retry_plan_reviewed_true", "retry_non_goals_reviewed_true",
    "ready_for_approval_false", "recommended_package_reviewed_not_selected",
    "retry_packages_reviewed_6", "blocked_retry_packages_reviewed_2",
    "retry_selected_false", "retry_approved_false", "retry_authorized_false",
    "retry_executed_false", "retry_results_review_created_false",
    "integration_results_review_created_false", "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "remote_integration_branch_created_false", "main_push_false", "origin_main_modified_false",
    "marketflow_outputs_committed_false", "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]

DEFAULT_SOURCE_CANDIDATE = source.build_marketflow_repository_integration_branch_retry_candidate_v1()


class MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError(ValueError):
    """Raised when operator-review evidence or authority boundaries are invalid."""


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    resolved = candidate if candidate is not None else DEFAULT_SOURCE_CANDIDATE
    source.validate_marketflow_repository_integration_branch_retry_candidate_v1(resolved)
    if resolved.get("marketflow_repository_integration_branch_retry_candidate_digest") != EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError(
            "source retry candidate digest mismatch"
        )
    return deepcopy(resolved)


def _reviewed_packages(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    status_map = {
        source.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED: REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED,
        source.AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED: REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED,
        source.BLOCKED_NOT_ALLOWED: REVIEWED_BLOCKED_NOT_ALLOWED,
    }
    rows = []
    for package in candidate["retry_packages"]:
        row = {
            "package_id": package["package_id"],
            "source_status": package["status"],
            "review_status": status_map[package["status"]],
            "selected": False, "approved": False, "executed": False,
        }
        if "blocked_reason" in package:
            row["blocked_reason"] = package["blocked_reason"]
        rows.append(row)
    return rows


def _reviewed_requirements(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": requirement_id,
            "required_value": deepcopy(required_value),
            "review_status": REVIEWED_REQUIRED_FOR_FUTURE_RETRY,
            "execution_status": NOT_EXECUTED,
        }
        for requirement_id, required_value in candidate["future_retry_requirements"].items()
    ]


def _reviewed_plan(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "step_id": f"retry_step_{index:02d}",
            "step": step,
            "review_status": REVIEWED_PLANNED_NOT_EXECUTED,
            "execution_status": NOT_EXECUTED,
        }
        for index, step in enumerate(candidate["future_retry_execution_plan"], start=1)
    ]


def _reviewed_non_goals(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"non_goal_id": non_goal, "review_status": REVIEWED_ACTIVE}
        for non_goal in candidate["retry_non_goals"]
    ]


def _base_review(candidate: Mapping[str, Any]) -> dict[str, Any]:
    packages = _reviewed_packages(candidate)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_integration_branch_retry_candidate_artifact_kind": candidate["artifact_kind"],
        "source_integration_branch_retry_candidate_status": candidate["candidate_status"],
        "source_integration_branch_retry_candidate_scope": candidate["candidate_scope"],
        "source_integration_branch_retry_candidate_digest": candidate["marketflow_repository_integration_branch_retry_candidate_digest"],
        "source_remediation_results_review_digest": candidate["source_remediation_results_review_digest"],
        "source_remediation_results_review_evidence_manifest_digest": candidate["source_remediation_results_review_evidence_manifest_digest"],
        "source_remediation_execution_digest": candidate["source_remediation_execution_digest"],
        "source_remediation_execution_evidence_manifest_digest": candidate["source_remediation_execution_evidence_manifest_digest"],
        "source_staged_inventory_digest": candidate["source_staged_inventory_digest"],
        "source_worktree_restoration_results_review_digest": candidate["source_worktree_restoration_results_review_digest"],
        "source_remediation_approval_digest": candidate["source_remediation_approval_digest"],
        "source_failure_diagnosis_digest": candidate["source_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": candidate["source_merge_strategy_approval_digest"],
        "attempted_execution_branch": candidate["attempted_execution_branch"],
        "attempted_execution_commit": candidate["attempted_execution_commit"],
        "original_blocked_artifact": candidate["original_blocked_artifact"],
        "original_blocked_status": candidate["original_blocked_status"],
        "first_integration_pytest_authoritative": True,
        "first_integration_pytest_passed": False,
        "first_integration_pytest_passed_count": 24481,
        "first_integration_pytest_failed_count": 1300,
        "first_integration_pytest_error_count": 500,
        "first_integration_pytest_skipped_count": 7,
        "later_wrong_worktree_rerun_diagnostic_only": True,
        "later_wrong_worktree_rerun_passed_count": 26842,
        "later_wrong_worktree_rerun_skipped_count": 7,
        "later_wrong_worktree_rerun_overrides_first_failure": False,
        "representative_failure_domain": "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH",
        "required_ready_digest_prefix": "57c0a06e", "blocked_digest_prefix": "783e0013",
        "diagnosed_root_cause": candidate["diagnosed_root_cause"],
        "origin_main_commit_at_review": candidate["origin_main_commit_at_review"],
        "integration_branch_name": candidate["integration_branch_name"],
        "integration_branch_head_commit_at_review": candidate["integration_branch_head_commit_at_review"],
        "integration_branch_matches_required_head_at_review": True,
        "remote_integration_branch_exists_at_review": False,
        "detached_integration_worktree_path": candidate["detached_integration_worktree_path"],
        "detached_integration_worktree_exists_at_review": True,
        "detached_integration_worktree_head_commit_at_review": candidate["detached_integration_worktree_head_commit_at_review"],
        "detached_integration_worktree_head_verified_at_review": True,
        "detached_integration_worktree_is_detached_at_review": True,
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_root_path": candidate["staged_evidence_root_path"],
        "staged_required_manifest_path": candidate["staged_required_manifest_path"],
        "staged_evidence_file_count_at_review": candidate["staged_evidence_file_count_at_review"],
        "staged_evidence_total_bytes_at_review": candidate["staged_evidence_total_bytes_at_review"],
        "staged_evidence_manifest_digest_at_review": candidate["staged_evidence_manifest_digest_at_review"],
        "staged_evidence_root_untracked_at_review": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "integration_branch_retry_candidate_created": True,
        "integration_branch_retry_candidate_ready_for_operator_review": True,
        "integration_branch_retry_candidate_operator_review_created": True,
        "integration_branch_retry_candidate_operator_review_ready": True,
        "retry_packages_reviewed": True, "retry_requirements_reviewed": True,
        "future_retry_plan_reviewed": True, "retry_non_goals_reviewed": True,
        "ready_for_integration_branch_retry_approval": False,
        "reviewed_retry_candidate_philosophy": candidate["retry_candidate_philosophy"],
        "reviewed_retry_candidate_boundary": "Candidate-only reviewed; no retry, approval, results review, success digest, main merge, or runtime authority is created by this artifact.",
        "reviewed_retry_candidate_goal": candidate["retry_candidate_goal"],
        "retry_philosophy_review_status": REVIEWED_PLANNING_ONLY,
        "reviewed_retry_packages": packages,
        "recommended_integration_branch_retry_package": candidate["recommended_integration_branch_retry_package"],
        "recommended_package_selected": False,
        "reviewed_future_retry_requirements": _reviewed_requirements(candidate),
        "reviewed_future_retry_plan": _reviewed_plan(candidate),
        "reviewed_retry_non_goals": _reviewed_non_goals(candidate),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": FUTURE_APPROVAL_NOT_CREATED,
        "recommended_action": OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_INTEGRATION_RETRY,
        "recommendation_reason": "The integration branch retry candidate has been reviewed, but no retry package has been selected or approved by this review.",
        "integration_branch_retry_selected": False, "integration_branch_retry_approved": False,
        "integration_branch_retry_authorized": False, "integration_branch_retry_executed": False,
        "integration_branch_retry_results_review_created": False,
        "integration_results_review_created": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "remote_integration_branch_created": False,
        "main_merge_performed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_retry_packages") or []
    blocked = [row for row in packages if row.get("review_status") == REVIEWED_BLOCKED_NOT_ALLOWED]
    recommended = next(
        (row for row in packages if row.get("package_id") == source.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE),
        {},
    )
    values: dict[str, tuple[Any, Any]] = {
        "source_retry_candidate_digest_bound": (EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST, review.get("source_integration_branch_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, review.get("source_remediation_results_review_digest")),
        "source_remediation_results_review_evidence_manifest_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST, review.get("source_remediation_results_review_evidence_manifest_digest")),
        "source_remediation_execution_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, review.get("source_remediation_execution_digest")),
        "source_remediation_execution_evidence_manifest_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST, review.get("source_remediation_execution_evidence_manifest_digest")),
        "source_staged_inventory_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, review.get("source_staged_inventory_digest")),
        "source_worktree_restoration_results_review_digest_bound": (EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST, review.get("source_worktree_restoration_results_review_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, review.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST, review.get("source_failure_diagnosis_digest")),
        "attempted_execution_commit_bound": (source.ATTEMPTED_EXECUTION_COMMIT, review.get("attempted_execution_commit")),
        "original_blocked_status_bound": ("MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED", review.get("original_blocked_status")),
        "first_failed_pytest_preserved": (True, review.get("first_integration_pytest_authoritative") and not review.get("first_integration_pytest_passed")),
        "later_wrong_worktree_rerun_preserved": (False, review.get("later_wrong_worktree_rerun_overrides_first_failure")),
        "origin_main_at_review_bound": (source.EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        "integration_branch_head_bound": (source.EXPECTED_INTEGRATION_HEAD_COMMIT, review.get("integration_branch_head_commit_at_review")),
        "detached_worktree_path_bound": (str(source.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)), review.get("detached_integration_worktree_path")),
        "detached_worktree_head_bound": (source.EXPECTED_INTEGRATION_HEAD_COMMIT, review.get("detached_integration_worktree_head_commit_at_review")),
        "detached_worktree_clean_recorded": (True, review.get("detached_integration_worktree_clean_at_review")),
        "staged_evidence_root_bound": (str(source.EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False)), review.get("staged_evidence_root_path")),
        "staged_manifest_bound": (str(source.EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False)), review.get("staged_required_manifest_path")),
        "staged_evidence_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, review.get("staged_evidence_manifest_digest_at_review")),
        "review_created_true": (True, review.get("integration_branch_retry_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("integration_branch_retry_candidate_operator_review_ready")),
        "retry_packages_reviewed_true": (True, review.get("retry_packages_reviewed")),
        "retry_requirements_reviewed_true": (True, review.get("retry_requirements_reviewed")),
        "future_retry_plan_reviewed_true": (True, review.get("future_retry_plan_reviewed")),
        "retry_non_goals_reviewed_true": (True, review.get("retry_non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_integration_branch_retry_approval")),
        "recommended_package_reviewed_not_selected": (False, recommended.get("selected")),
        "retry_packages_reviewed_6": (6, len(packages)),
        "blocked_retry_packages_reviewed_2": (2, len(blocked)),
        "retry_selected_false": (False, review.get("integration_branch_retry_selected")),
        "retry_approved_false": (False, review.get("integration_branch_retry_approved")),
        "retry_authorized_false": (False, review.get("integration_branch_retry_authorized")),
        "retry_executed_false": (False, review.get("integration_branch_retry_executed")),
        "retry_results_review_created_false": (False, review.get("integration_branch_retry_results_review_created")),
        "integration_results_review_created_false": (False, review.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, review.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, review.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, review.get("remote_integration_branch_created")),
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
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "integration_branch_retry_candidate_operator_review_created": True,
        "integration_branch_retry_candidate_operator_review_ready": True,
        "retry_packages_reviewed": True,
        "recommended_integration_branch_retry_package": source.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE,
        "recommended_package_selected": False,
        "ready_for_integration_branch_retry_approval": False,
        "retry_executed": False, "retry_results_review_created": False,
        "integration_execution_successful": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_retry_candidate_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build an offline review without selecting or approving a retry package."""
    review = _base_review(_source_candidate(source_candidate))
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_integration_branch_retry_candidate_operator_review_digest"] = (
        marketflow_repository_integration_branch_retry_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate the review and all non-selection, non-approval boundaries."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("review must be an object")
    expected = _base_review(_source_candidate(None))
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError(f"{field} mismatch")
    checklist = review.get("checklist")
    if checklist != _checklist(review) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("review checklist mismatch or failed")
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("review summary mismatch")
    digest = review.get("marketflow_repository_integration_branch_retry_candidate_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("operator-review digest missing")
    if digest != marketflow_repository_integration_branch_retry_candidate_operator_review_digest_v1(review):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("operator-review digest mismatch")
    return {
        "status": review["review_status"], "artifact_kind": review["artifact_kind"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_candidate_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review."""
    validation = validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(review)
    sections = [
        ("Source Retry Candidate", [f"Digest: `{review['source_integration_branch_retry_candidate_digest']}`."]),
        ("Source Remediation Results Review", [f"Digest: `{review['source_remediation_results_review_digest']}`."]),
        ("Failure Context", ["The first failed integration pytest remains authoritative; the wrong-worktree pass is diagnostic only."]),
        ("Remediation Context", ["Matching frozen ignored evidence remains staged and untracked in the detached integration worktree."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Reviewed Retry Philosophy", [review["reviewed_retry_candidate_philosophy"], review["reviewed_retry_candidate_boundary"]]),
        ("Reviewed Retry Packages", [f"`{row['package_id']}`: `{row['review_status']}`." for row in review["reviewed_retry_packages"]]),
        ("Reviewed Future Retry Requirements", [f"`{row['requirement_id']}`: `{row['review_status']}`." for row in review["reviewed_future_retry_requirements"]]),
        ("Reviewed Future Retry Plan", [f"`{row['step_id']}`: `{row['review_status']}`." for row in review["reviewed_future_retry_plan"]]),
        ("Reviewed Retry Non-Goals", [f"`{row['non_goal_id']}`: `{row['review_status']}`." for row in review["reviewed_retry_non_goals"]]),
        ("Recommendation", [review["recommendation_reason"], f"Next task status: `{review['recommended_next_task_status']}`."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No package was selected or approved; no retry, result, success, push, acceptance, runtime, or broker authority was created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Optional operator selection and a separate approval remain required before any retry."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
    output_dir: str | Path,
    *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_candidate_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError("operator-review output already exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {"path": str(path), "sha256": hashlib.sha256(payload).hexdigest(), **validation}
