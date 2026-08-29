"""Offline candidate for restoring the detached integration worktree."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_approval_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1 = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY = (
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY"
)

EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = (
    "681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded"
)
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = source.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_APPROVAL_DIGEST
BLOCKED_REMEDIATION_EXECUTION_ARTIFACT_KIND = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_BLOCKED"
)
BLOCKED_REMEDIATION_EXECUTION_STATUS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_BLOCKED_INTEGRATION_WORKTREE_MISSING_OR_MISMATCHED"
)
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_BRANCH_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"
ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
SOURCE_EVIDENCE_ROOT_PATH = (
    r"C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\acquisition_provider_evidence\expanded_universe_v1"
)
SOURCE_REQUIRED_MANIFEST_NAME = "acquisition_provider_evidence_run_manifest.json"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED = "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
BLOCKED_NOT_RECOMMENDED = "BLOCKED_NOT_RECOMMENDED"
BLOCKED_NOT_ALLOWED = "BLOCKED_NOT_ALLOWED"

PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD = (
    "PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD"
)
PACKAGE_CREATE_WORKTREE_ATTACHED_TO_EXISTING_INTEGRATION_BRANCH = (
    "PACKAGE_CREATE_WORKTREE_ATTACHED_TO_EXISTING_INTEGRATION_BRANCH"
)
PACKAGE_PARAMETERIZE_REMEDIATION_WITH_EXISTING_WORKTREE_PATH_AFTER_MANUAL_OPERATOR_RESTORE = (
    "PACKAGE_PARAMETERIZE_REMEDIATION_WITH_EXISTING_WORKTREE_PATH_AFTER_MANUAL_OPERATOR_RESTORE"
)
PACKAGE_RECREATE_INTEGRATION_BRANCH_FROM_APPROVED_PARENTS = (
    "PACKAGE_RECREATE_INTEGRATION_BRANCH_FROM_APPROVED_PARENTS"
)
PACKAGE_DELETE_AND_RECREATE_INTEGRATION_BRANCH_OR_WORKTREE = (
    "PACKAGE_DELETE_AND_RECREATE_INTEGRATION_BRANCH_OR_WORKTREE"
)
PACKAGE_USE_FEATURE_WORKTREE_AS_INTEGRATION_WORKTREE = (
    "PACKAGE_USE_FEATURE_WORKTREE_AS_INTEGRATION_WORKTREE"
)

WORKTREE_RESTORATION_PHILOSOPHY = (
    "The detached integration worktree must be restored or created as a registered local Git worktree at the exact approved integration head before remediation staging can proceed, without resetting the integration branch, pushing it remotely, deleting branches, or treating restoration as integration validation success."
)
WORKTREE_RESTORATION_BOUNDARY = (
    "Candidate-only; no worktree is created, restored, deleted, reset, or used for remediation by this artifact."
)
WORKTREE_RESTORATION_GOAL = (
    "Define a controlled future path to provide the remediation execution task with a valid detached integration worktree at the required merge commit."
)

WORKTREE_RESTORATION_PACKAGES = [
    {
        "package_id": PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD,
        "status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": f"Create a registered local Git worktree at a deterministic path, checked out detached at commit {INTEGRATION_BRANCH_HEAD_COMMIT}, without changing the existing integration branch.",
        "recommended_for": "Safest restoration because it avoids branch reset, avoids branch checkout conflicts, and provides a concrete detached worktree path for remediation staging.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_CREATE_WORKTREE_ATTACHED_TO_EXISTING_INTEGRATION_BRANCH,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Create a registered local Git worktree checked out on the existing local integration branch.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_PARAMETERIZE_REMEDIATION_WITH_EXISTING_WORKTREE_PATH_AFTER_MANUAL_OPERATOR_RESTORE,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Allow a future operator-provided existing worktree path if it is already registered and points to the exact integration head.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_RECREATE_INTEGRATION_BRANCH_FROM_APPROVED_PARENTS,
        "status": BLOCKED_NOT_RECOMMENDED,
        "purpose": "Recreate the integration branch from origin/main and source commit.",
        "blocked_reason": "Would overwrite or duplicate existing local integration branch state and risks losing diagnostic continuity.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_DELETE_AND_RECREATE_INTEGRATION_BRANCH_OR_WORKTREE,
        "status": BLOCKED_NOT_ALLOWED,
        "purpose": "Delete/reset the existing integration branch or worktree and recreate it.",
        "blocked_reason": "The failed execution contract explicitly prohibited deleting, resetting, or overwriting the integration branch/worktree.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_USE_FEATURE_WORKTREE_AS_INTEGRATION_WORKTREE,
        "status": BLOCKED_NOT_ALLOWED,
        "purpose": "Run remediation or retry from the feature worktree.",
        "blocked_reason": "The diagnosis identified wrong-worktree pytest execution as invalid diagnostic-only evidence.",
        "selected": False, "approved": False, "executed": False,
    },
]

WORKTREE_RESTORATION_REQUIREMENTS = {
    "origin_main_must_remain_unchanged": True,
    "integration_branch_must_exist_locally": True,
    "integration_branch_head_must_match_required_commit": True,
    "remote_integration_branch_must_remain_absent": True,
    "existing_worktree_must_not_be_overwritten": True,
    "worktree_path_must_be_deterministic": True,
    "worktree_path_must_not_already_exist_unless_matching_registered_worktree": True,
    "registered_git_worktree_required": True,
    "detached_head_at_required_commit_required": True,
    "worktree_head_must_equal_220fbc220365fce9cae13ab4853cddff118c0187": True,
    "worktree_branch_checkout_not_required_for_recommended_package": True,
    "no_branch_reset_allowed": True,
    "no_branch_deletion_allowed": True,
    "no_remote_push_allowed": True,
    "no_marketflow_copy_or_staging_in_restoration_task": True,
    "remediation_execution_must_stage_evidence_later": True,
    "integration_retry_must_remain_separate": True,
}

FUTURE_WORKTREE_RESTORATION_PLAN = [
    "Verify origin/main remains unchanged.",
    f"Verify the local integration branch exists and points to {INTEGRATION_BRANCH_HEAD_COMMIT}.",
    "Verify the remote integration branch remains absent.",
    r"Select the deterministic local path C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1.",
    "Verify the selected path does not already exist, or if it exists, it is a matching registered worktree.",
    f"Create a registered detached worktree with git worktree add --detach <path> {INTEGRATION_BRANCH_HEAD_COMMIT}.",
    "Verify git worktree list --porcelain includes the new path.",
    f"Verify worktree HEAD equals {INTEGRATION_BRANCH_HEAD_COMMIT}.",
    "Verify no remote integration branch was created.",
    "Do not copy .marketflow, run pytest, or retry integration in the restoration execution.",
]

WORKTREE_RESTORATION_NON_GOALS = [
    "do_not_create_worktree_now", "do_not_restore_worktree_now", "do_not_delete_worktree_now",
    "do_not_reset_integration_branch", "do_not_delete_integration_branch",
    "do_not_recreate_integration_branch_now", "do_not_stage_evidence_now",
    "do_not_copy_marketflow_now", "do_not_commit_marketflow_outputs",
    "do_not_run_pytest_retry_now", "do_not_create_results_review_now",
    "do_not_push_integration_branch", "do_not_push_main", "do_not_force_push",
    "do_not_prune_remotes", "do_not_modify_tags", "do_not_accept_wrong_worktree_execution",
    "do_not_accept_predictive_usefulness", "do_not_accept_profitability",
    "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Worktree Restoration Candidate Operator Review v1.",
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
    "worktree_restoration_candidate_operator_review",
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
    "candidate_does_not_create_worktree", "candidate_does_not_restore_worktree",
    "candidate_does_not_delete_worktree", "candidate_does_not_reset_integration_branch",
    "candidate_does_not_delete_integration_branch", "candidate_does_not_recreate_integration_branch",
    "candidate_does_not_stage_evidence", "candidate_does_not_copy_marketflow_outputs",
    "candidate_does_not_commit_marketflow_outputs", "candidate_does_not_run_pytest_retry",
    "candidate_does_not_create_results_review", "candidate_does_not_push_integration_branch",
    "candidate_does_not_push_main", "candidate_does_not_force_push", "candidate_does_not_prune_remotes",
    "candidate_does_not_modify_tags", "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data", "candidate_does_not_regenerate_dataset",
    "candidate_does_not_recompute_metrics", "candidate_does_not_train_models",
    "candidate_does_not_score_strategy", "candidate_does_not_generate_recommendations",
    "candidate_does_not_accept_predictive_usefulness", "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime", "candidate_does_not_authorize_broker_execution",
    "separate_operator_review_required", "separate_approval_required_before_worktree_restoration",
    "separate_results_review_required_after_worktree_restoration",
    "separate_remediation_execution_required_after_worktree_restoration", "protect_origin_main",
    "preserve_existing_integration_branch", "preserve_failed_gate", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1"
)

DEFAULT_SOURCE_APPROVAL = {
    "artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED,
    "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
    "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
    "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
    "source_failure_diagnosis_digest": EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
}
DEFAULT_WORKTREE_OBSERVATION = {
    "blocked_remediation_execution_artifact_kind": BLOCKED_REMEDIATION_EXECUTION_ARTIFACT_KIND,
    "blocked_remediation_execution_status": BLOCKED_REMEDIATION_EXECUTION_STATUS,
    "integration_branch_name": INTEGRATION_BRANCH_NAME,
    "integration_branch_head_commit": INTEGRATION_BRANCH_HEAD_COMMIT,
    "integration_branch_exists_local": True,
    "integration_branch_matches_required_head": True,
    "detached_integration_worktree_exists": False,
    "registered_worktree_entries_present": False,
    "git_worktrees_directory_present": False,
    "remote_integration_branch_exists": False,
    "origin_main_commit": ORIGIN_MAIN_COMMIT,
    "source_evidence_root_path": SOURCE_EVIDENCE_ROOT_PATH,
    "source_evidence_root_exists": True,
    "source_required_manifest_name": SOURCE_REQUIRED_MANIFEST_NAME,
    "source_required_manifest_exists": True,
    "source_evidence_file_count": 7,
    "source_evidence_total_bytes": 2458181,
    "source_evidence_ignored_by_gitignore": True,
    "marketflow_outputs_tracked": False,
}

REQUIRED_CHECK_IDS = [
    "source_remediation_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_diagnosis_digest_bound",
    "blocked_execution_status_recorded", "integration_branch_exists_local_true",
    "integration_branch_head_bound", "detached_worktree_missing_recorded",
    "source_evidence_root_exists_recorded", "source_required_manifest_exists_recorded",
    "source_evidence_file_count_recorded", "marketflow_outputs_not_tracked",
    "origin_main_commit_bound", "candidate_created_true", "candidate_ready_true",
    "recommended_package_present", "restoration_packages_present_6", "blocked_packages_present_3",
    "recommended_package_not_selected", "worktree_restoration_selected_false",
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
    "runtime_not_authorized", "broker_not_authorized", "restoration_requirements_defined",
    "future_restoration_plan_defined", "non_goals_defined", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(ValueError):
    """Raised when candidate facts or candidate-only boundaries are invalid."""


def _source_approval(source_approval: dict | None) -> dict[str, Any]:
    approval = deepcopy(DEFAULT_SOURCE_APPROVAL if source_approval is None else source_approval)
    if source_approval is not None:
        validation = source.validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
            approval
        )
        if validation["marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"] != EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
                "source remediation approval digest mismatch"
            )
    for field, expected in DEFAULT_SOURCE_APPROVAL.items():
        if approval.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
                f"source approval {field} mismatch"
            )
    return approval


def _worktree_observation(worktree_observation: dict | None) -> dict[str, Any]:
    observation = deepcopy(
        DEFAULT_WORKTREE_OBSERVATION if worktree_observation is None else worktree_observation
    )
    for field, expected in DEFAULT_WORKTREE_OBSERVATION.items():
        if observation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
                f"worktree observation {field} mismatch"
            )
    return observation


def _base_candidate(approval: Mapping[str, Any], observation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY,
        "created_offline": True, "governance_only": True,
        "worktree_restoration_candidate_only": True, "operator_review_required": True,
        "source_remediation_approval_artifact_kind": approval["artifact_kind"],
        "source_remediation_approval_digest": approval["marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"],
        "source_remediation_operator_review_digest": approval["source_remediation_operator_review_digest"],
        "source_remediation_candidate_digest": approval["source_remediation_candidate_digest"],
        "source_failure_diagnosis_digest": approval["source_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": approval["source_merge_strategy_approval_digest"],
        **deepcopy(dict(observation)),
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
        "worktree_restoration_candidate_created": True,
        "worktree_restoration_candidate_ready_for_operator_review": True,
        "ready_for_worktree_restoration_operator_review": True,
        "worktree_restoration_selected": False, "worktree_restoration_approved": False,
        "worktree_restoration_authorized": False, "worktree_restoration_executed": False,
        "detached_worktree_created": False, "detached_worktree_restored": False,
        "detached_worktree_deleted": False, "integration_branch_deleted_or_reset": False,
        "remediation_executed": False, "evidence_staged": False,
        "marketflow_outputs_copied": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "integration_retry_candidate_created": False,
        "integration_retry_executed": False, "integration_results_review_created": False,
        "integration_execution_successful": False, "successful_execution_digest_generated": False,
        "successful_validation_digest_generated": False, "integration_branch_pushed": False,
        "main_push_performed": False, "origin_main_modified_by_this_task": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "worktree_restoration_philosophy": WORKTREE_RESTORATION_PHILOSOPHY,
        "worktree_restoration_boundary": WORKTREE_RESTORATION_BOUNDARY,
        "worktree_restoration_goal": WORKTREE_RESTORATION_GOAL,
        "worktree_restoration_packages": deepcopy(WORKTREE_RESTORATION_PACKAGES),
        "recommended_worktree_restoration_package": PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD,
        "recommendation_status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "recommendation_reason": "A registered detached worktree at the exact integration merge commit restores the missing execution environment without resetting branches, deleting worktrees, pushing refs, or rerunning integration validation.",
        "worktree_restoration_requirements": deepcopy(WORKTREE_RESTORATION_REQUIREMENTS),
        "future_worktree_restoration_plan": list(FUTURE_WORKTREE_RESTORATION_PLAN),
        "future_worktree_restoration_plan_status": "PLANNED_NOT_EXECUTED",
        "worktree_restoration_non_goals": list(WORKTREE_RESTORATION_NON_GOALS),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = candidate.get("worktree_restoration_packages", [])
    values: dict[str, tuple[Any, Any]] = {
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, candidate.get("source_remediation_approval_digest")),
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST, candidate.get("source_remediation_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST, candidate.get("source_remediation_candidate_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST, candidate.get("source_failure_diagnosis_digest")),
        "blocked_execution_status_recorded": (BLOCKED_REMEDIATION_EXECUTION_STATUS, candidate.get("blocked_remediation_execution_status")),
        "integration_branch_exists_local_true": (True, candidate.get("integration_branch_exists_local")),
        "integration_branch_head_bound": (INTEGRATION_BRANCH_HEAD_COMMIT, candidate.get("integration_branch_head_commit")),
        "detached_worktree_missing_recorded": (False, candidate.get("detached_integration_worktree_exists")),
        "source_evidence_root_exists_recorded": (True, candidate.get("source_evidence_root_exists")),
        "source_required_manifest_exists_recorded": (True, candidate.get("source_required_manifest_exists")),
        "source_evidence_file_count_recorded": (7, candidate.get("source_evidence_file_count")),
        "marketflow_outputs_not_tracked": (False, candidate.get("marketflow_outputs_tracked")),
        "origin_main_commit_bound": (ORIGIN_MAIN_COMMIT, candidate.get("origin_main_commit")),
        "candidate_created_true": (True, candidate.get("worktree_restoration_candidate_created")),
        "candidate_ready_true": (True, candidate.get("worktree_restoration_candidate_ready_for_operator_review")),
        "recommended_package_present": (PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD, candidate.get("recommended_worktree_restoration_package")),
        "restoration_packages_present_6": (6, len(packages)),
        "blocked_packages_present_3": (3, sum(row.get("status", "").startswith("BLOCKED_") for row in packages)),
        "recommended_package_not_selected": (False, packages[0].get("selected") if packages else None),
        "worktree_restoration_selected_false": (False, candidate.get("worktree_restoration_selected")),
        "worktree_restoration_approved_false": (False, candidate.get("worktree_restoration_approved")),
        "worktree_restoration_executed_false": (False, candidate.get("worktree_restoration_executed")),
        "detached_worktree_created_false": (False, candidate.get("detached_worktree_created")),
        "detached_worktree_restored_false": (False, candidate.get("detached_worktree_restored")),
        "detached_worktree_deleted_false": (False, candidate.get("detached_worktree_deleted")),
        "integration_branch_deleted_or_reset_false": (False, candidate.get("integration_branch_deleted_or_reset")),
        "remediation_executed_false": (False, candidate.get("remediation_executed")),
        "evidence_staged_false": (False, candidate.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, candidate.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, candidate.get("marketflow_outputs_committed")),
        "retry_candidate_created_false": (False, candidate.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, candidate.get("integration_retry_executed")),
        "results_review_created_false": (False, candidate.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, candidate.get("integration_execution_successful")),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
        "main_push_false": (False, candidate.get("main_push_performed")),
        "origin_main_modified_false": (False, candidate.get("origin_main_modified_by_this_task")),
        "provider_requests_false": (False, candidate.get("provider_requests_made_in_candidate")),
        "market_data_acquisition_false": (False, candidate.get("market_data_acquisition_performed_in_candidate")),
        "dataset_generation_false": (False, candidate.get("dataset_generation_performed_in_candidate")),
        "metric_recomputation_false": (False, candidate.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, candidate.get("model_training_performed")),
        "strategy_scoring_false": (False, candidate.get("strategy_scoring_performed")),
        "recommendations_false": (False, candidate.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "restoration_requirements_defined": (WORKTREE_RESTORATION_REQUIREMENTS, candidate.get("worktree_restoration_requirements")),
        "future_restoration_plan_defined": (FUTURE_WORKTREE_RESTORATION_PLAN, candidate.get("future_worktree_restoration_plan")),
        "non_goals_defined": (WORKTREE_RESTORATION_NON_GOALS, candidate.get("worktree_restoration_non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "worktree_restoration_candidate_created": True,
        "worktree_restoration_candidate_ready_for_operator_review": True,
        "recommended_worktree_restoration_package": PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD,
        "worktree_restoration_selected": False, "worktree_restoration_approved": False,
        "worktree_restoration_executed": False, "detached_worktree_created": False,
        "remediation_execution_ready_now": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic candidate digest."""
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
    *, source_approval: dict | None = None, worktree_observation: dict | None = None,
) -> dict:
    """Build the candidate offline without creating or restoring a worktree."""
    candidate = _base_candidate(
        _source_approval(source_approval), _worktree_observation(worktree_observation)
    )
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"] = (
        marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, observations, and all candidate-only boundaries."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            "candidate must be an object"
        )
    expected = _base_candidate(DEFAULT_SOURCE_APPROVAL, DEFAULT_WORKTREE_OBSERVATION)
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    for field in ("integration_branch_head_commit", "origin_main_commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(candidate.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
                f"{field} invalid"
            )
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            "checklist failed"
        )
    _expect(candidate.get("summary"), _summary(checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "artifact_kind": candidate["artifact_kind"], "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest": digest,
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated governance-only restoration candidate."""
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
        candidate
    )
    sections = [
        ("Source Remediation Approval", [f"Artifact/digest: `{candidate['source_remediation_approval_artifact_kind']}` / `{candidate['source_remediation_approval_digest']}`."]),
        ("Blocked Remediation Execution Observation", [f"`{candidate['blocked_remediation_execution_artifact_kind']}` / `{candidate['blocked_remediation_execution_status']}`.", f"Integration branch/head: `{candidate['integration_branch_name']}` / `{candidate['integration_branch_head_commit']}`."]),
        ("Candidate Scope", [f"`{candidate['candidate_scope']}`."]),
        ("Worktree Restoration Philosophy", [candidate["worktree_restoration_philosophy"], candidate["worktree_restoration_boundary"], candidate["worktree_restoration_goal"]]),
        ("Proposed Restoration Packages", [f"`{row['package_id']}`: `{row['status']}`; selected/approved/executed `{row['selected']} / {row['approved']} / {row['executed']}`." for row in candidate["worktree_restoration_packages"]]),
        ("Recommended Restoration Package", [f"`{candidate['recommended_worktree_restoration_package']}` / `{candidate['recommendation_status']}`.", candidate["recommendation_reason"]]),
        ("Future Restoration Requirements", [f"`{key}`: `{value}`" for key, value in candidate["worktree_restoration_requirements"].items()]),
        ("Future Restoration Plan", candidate["future_worktree_restoration_plan"]),
        ("Restoration Non-Goals", [f"`{row}`" for row in candidate["worktree_restoration_non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No worktree creation, remediation, evidence staging, integration retry, results review, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Separate operator review and approval are required before restoration execution.", "The failed integration gate remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
    output_dir: str | Path,
    *, source_approval: dict | None = None, worktree_observation: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
        source_approval=source_approval, worktree_observation=worktree_observation
    )
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError(
            "restoration candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"], "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest": validation[
            "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
