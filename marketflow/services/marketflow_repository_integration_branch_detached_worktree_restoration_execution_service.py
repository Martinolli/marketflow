"""Execute the approved registered detached-worktree restoration."""

from __future__ import annotations

import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_approval_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_V1 = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED"
)
REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW = (
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED"
)
BLOCKED_WORKTREE_PATH_EXISTS_OR_MISMATCHED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED_WORKTREE_PATH_EXISTS_OR_MISMATCHED"
)
BLOCKED_INTEGRATION_HEAD_MISMATCH = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED_INTEGRATION_HEAD_MISMATCH"
)
BLOCKED_REMOTE_INTEGRATION_BRANCH_EXISTS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED_REMOTE_INTEGRATION_BRANCH_EXISTS"
)

SELECTED_WORKTREE_RESTORATION_PACKAGE = source.SELECTED_WORKTREE_RESTORATION_PACKAGE
EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "6ca8b958949667264419a1b5f59e08c7ae335c5e1b836e93541f87519a2b055d"
)
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = (
    "f32d7ded083256f4301903de41e1fdf06562b4af0e5bd0fc2c75685d4fd8a301"
)
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = (
    "2d45ef960b45d6a81b6e494b77a44f3dba482567e973e83999844ce9ce351fc2"
)
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = (
    "34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c"
)
EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_BLOCKED"
)
EXPECTED_BLOCKED_EXECUTION_STATUS = source.EXPECTED_BLOCKED_EXECUTION_STATUS
EXPECTED_INTEGRATION_BRANCH_NAME = source.EXPECTED_INTEGRATION_BRANCH_NAME
EXPECTED_INTEGRATION_HEAD_COMMIT = source.EXPECTED_INTEGRATION_HEAD_COMMIT
EXPECTED_ORIGIN_MAIN_COMMIT = source.EXPECTED_ORIGIN_MAIN_COMMIT
DEFAULT_WORKTREE_PATH = Path(
    r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1"
)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PRECHECK_IDS = [
    "source_approval_digest_bound",
    "origin_main_verified",
    "integration_branch_exists_local",
    "integration_branch_head_verified",
    "remote_integration_branch_absent",
    "deterministic_worktree_path_selected",
    "worktree_path_absent_or_matching",
    "marketflow_outputs_not_tracked",
    "no_provider_or_data_actions",
]
EXECUTION_STEP_IDS = [
    "verify_origin_main",
    "verify_integration_branch_head",
    "verify_remote_integration_branch_absent",
    "create_registered_detached_worktree",
    "verify_registered_worktree_present",
    "verify_worktree_head",
    "verify_worktree_detached",
    "verify_no_integration_branch_push",
    "verify_no_main_push",
    "do_not_stage_evidence",
    "do_not_run_retry",
    "do_not_create_results_review",
]
NEXT_CHAIN = [
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
    "worktree_restoration_results_review",
    "remediation_execution_after_worktree_restoration_review",
    "remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "execution_creates_only_approved_registered_detached_worktree",
    "execution_uses_exact_required_integration_head",
    "execution_uses_deterministic_worktree_path",
    "execution_does_not_checkout_integration_branch_in_worktree",
    "execution_does_not_reset_integration_branch",
    "execution_does_not_delete_integration_branch",
    "execution_does_not_push_integration_branch",
    "execution_does_not_push_main",
    "execution_does_not_delete_worktree",
    "execution_does_not_stage_evidence",
    "execution_does_not_copy_marketflow_outputs",
    "execution_does_not_commit_marketflow_outputs",
    "execution_does_not_run_pytest_retry",
    "execution_does_not_create_results_review",
    "execution_does_not_force_push",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_tags",
    "execution_does_not_push_additional_tags",
    "execution_does_not_call_providers",
    "execution_does_not_acquire_market_data",
    "execution_does_not_regenerate_dataset",
    "execution_does_not_recompute_metrics",
    "execution_does_not_train_models",
    "execution_does_not_score_strategy",
    "execution_does_not_generate_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability",
    "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_broker_execution",
    "separate_results_review_required_after_worktree_restoration",
    "separate_remediation_execution_required_after_worktree_restoration",
    "protect_origin_main",
    "preserve_existing_integration_branch",
    "preserve_failed_gate",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1"
)

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_remediation_approval_digest_bound",
    "source_diagnosis_digest_bound", "blocked_execution_status_recorded",
    "origin_main_before_bound", "origin_main_after_unchanged",
    "integration_branch_name_bound", "integration_head_before_bound",
    "integration_head_after_unchanged", "integration_branch_exists_local_true",
    "integration_branch_deleted_or_reset_false", "deterministic_worktree_path_bound",
    "worktree_path_existed_before_false", "worktree_path_exists_after_true",
    "registered_worktree_entries_before_false", "registered_worktree_entries_after_true",
    "detached_worktree_created_true", "detached_worktree_restored_true",
    "detached_worktree_deleted_false", "registered_detached_worktree_created_true",
    "worktree_head_verified_true", "worktree_is_detached_true",
    "worktree_branch_checked_out_false", "remote_integration_branch_before_false",
    "remote_integration_branch_after_false", "integration_branch_pushed_false",
    "restoration_selected_true", "restoration_approved_true",
    "restoration_authorized_true", "restoration_executed_true",
    "ready_for_results_review_true", "remediation_executed_false",
    "evidence_staged_false", "marketflow_outputs_copied_false",
    "marketflow_outputs_committed_false", "evidence_regenerated_false",
    "retry_candidate_created_false", "retry_executed_false", "results_review_created_false",
    "integration_execution_successful_false", "main_push_false", "origin_main_modified_false",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(ValueError):
    """Raised when restoration preconditions or execution evidence fail closed."""

    def __init__(self, message: str, *, blocked_status: str | None = None) -> None:
        super().__init__(message)
        self.artifact_kind = (
            ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_BLOCKED
            if blocked_status
            else None
        )
        self.blocked_status = blocked_status


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _registered_worktrees(repo_root: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] = {}
    for line in _git(repo_root, "worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if not line:
            if current:
                path = str(Path(current["worktree"]).resolve(strict=False)).casefold()
                rows[path] = current
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value if value else True
    return rows


def _remote_integration_exists(repo_root: Path) -> bool:
    result = _git(
        repo_root,
        "show-ref",
        "--verify",
        "--quiet",
        f"refs/remotes/origin/{EXPECTED_INTEGRATION_BRANCH_NAME}",
        check=False,
    )
    return result.returncode == 0


def _record(step_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "step_id": step_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "message": f"{step_id} {'passed' if status == PASS else 'failed'}",
    }


def _observations_fixture() -> dict[str, Any]:
    return {
        "origin_main_before": EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_after": EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_head_before": EXPECTED_INTEGRATION_HEAD_COMMIT,
        "integration_head_after": EXPECTED_INTEGRATION_HEAD_COMMIT,
        "integration_exists": True,
        "path_existed_before": False,
        "path_exists_after": True,
        "registered_before": False,
        "registered_after": True,
        "git_worktrees_before": False,
        "git_worktrees_after": True,
        "remote_before": False,
        "remote_after": False,
        "worktree_head": EXPECTED_INTEGRATION_HEAD_COMMIT,
        "detached": True,
        "tracked_marketflow_count": 0,
        "operation_mode": "DETERMINISTIC_OPERATION_FIXTURE",
    }


def _execute_git_restoration(repo_root: Path, worktree_path: Path) -> dict[str, Any]:
    expected_path = DEFAULT_WORKTREE_PATH.resolve(strict=False)
    actual_path = worktree_path.resolve(strict=False)
    if actual_path != expected_path:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "worktree restoration path is not the deterministic approved path",
            blocked_status=BLOCKED_WORKTREE_PATH_EXISTS_OR_MISMATCHED,
        )

    origin_before = _git(repo_root, "rev-parse", "origin/main").stdout.strip()
    if origin_before != EXPECTED_ORIGIN_MAIN_COMMIT:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "origin/main commit mismatch"
        )
    integration_result = _git(
        repo_root, "rev-parse", "--verify", EXPECTED_INTEGRATION_BRANCH_NAME, check=False
    )
    if integration_result.returncode != 0:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "local integration branch is missing",
            blocked_status=BLOCKED_INTEGRATION_HEAD_MISMATCH,
        )
    integration_before = integration_result.stdout.strip()
    if integration_before != EXPECTED_INTEGRATION_HEAD_COMMIT:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "local integration branch head mismatch",
            blocked_status=BLOCKED_INTEGRATION_HEAD_MISMATCH,
        )
    remote_before = _remote_integration_exists(repo_root)
    if remote_before:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "remote integration branch exists",
            blocked_status=BLOCKED_REMOTE_INTEGRATION_BRANCH_EXISTS,
        )

    registered_before_rows = _registered_worktrees(repo_root)
    path_key = str(actual_path).casefold()
    path_existed_before = actual_path.exists()
    registered_before = path_key in registered_before_rows
    if path_existed_before or registered_before:
        row = registered_before_rows.get(path_key, {})
        matching = (
            path_existed_before
            and registered_before
            and row.get("HEAD") == EXPECTED_INTEGRATION_HEAD_COMMIT
            and row.get("detached") is True
        )
        detail = "already restored" if matching else "exists or is registered with mismatched state"
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            f"worktree path {detail}; no overwrite or deletion performed",
            blocked_status=BLOCKED_WORKTREE_PATH_EXISTS_OR_MISMATCHED,
        )
    tracked_marketflow_count = len(_git(repo_root, "ls-files", ".marketflow").stdout.splitlines())
    if tracked_marketflow_count:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            ".marketflow contains tracked files"
        )

    git_worktrees_dir = repo_root / ".git" / "worktrees"
    git_worktrees_before = git_worktrees_dir.is_dir()
    _git(
        repo_root,
        "worktree",
        "add",
        "--detach",
        str(actual_path),
        EXPECTED_INTEGRATION_HEAD_COMMIT,
    )

    registered_after_rows = _registered_worktrees(repo_root)
    row = registered_after_rows.get(path_key, {})
    path_exists_after = actual_path.is_dir()
    registered_after = path_key in registered_after_rows
    worktree_head = _git(actual_path, "rev-parse", "HEAD").stdout.strip()
    detached = _git(actual_path, "symbolic-ref", "-q", "HEAD", check=False).returncode != 0
    origin_after = _git(repo_root, "rev-parse", "origin/main").stdout.strip()
    integration_after = _git(repo_root, "rev-parse", EXPECTED_INTEGRATION_BRANCH_NAME).stdout.strip()
    remote_after = _remote_integration_exists(repo_root)
    if not (
        path_exists_after
        and registered_after
        and row.get("HEAD") == EXPECTED_INTEGRATION_HEAD_COMMIT
        and row.get("detached") is True
        and worktree_head == EXPECTED_INTEGRATION_HEAD_COMMIT
        and detached
        and origin_after == origin_before
        and integration_after == integration_before
        and not remote_after
    ):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "post-execution registered detached-worktree verification failed"
        )
    return {
        "origin_main_before": origin_before,
        "origin_main_after": origin_after,
        "integration_head_before": integration_before,
        "integration_head_after": integration_after,
        "integration_exists": True,
        "path_existed_before": path_existed_before,
        "path_exists_after": path_exists_after,
        "registered_before": registered_before,
        "registered_after": registered_after,
        "git_worktrees_before": git_worktrees_before,
        "git_worktrees_after": git_worktrees_dir.is_dir(),
        "remote_before": remote_before,
        "remote_after": remote_after,
        "worktree_head": worktree_head,
        "detached": detached,
        "tracked_marketflow_count": tracked_marketflow_count,
        "operation_mode": "LOCAL_GIT_WORKTREE_EXECUTION",
    }


def _base_execution(
    *, worktree_path: Path, run_timestamp_utc: str, observations: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW,
        "selected_worktree_restoration_package": SELECTED_WORKTREE_RESTORATION_PACKAGE,
        "created_offline_except_local_git_worktree_creation": True,
        "governance_only": True,
        "run_timestamp_utc": run_timestamp_utc,
        "git_operation_mode": observations["operation_mode"],
        "source_worktree_restoration_approval_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED,
        "source_worktree_restoration_approval_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED,
        "source_worktree_restoration_approval_scope": source.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY,
        "source_worktree_restoration_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_worktree_restoration_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_worktree_restoration_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "blocked_remediation_execution_artifact_kind": EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND,
        "blocked_remediation_execution_status": EXPECTED_BLOCKED_EXECUTION_STATUS,
        "origin_main_commit_before_execution": observations["origin_main_before"],
        "origin_main_commit_after_execution": observations["origin_main_after"],
        "integration_branch_name": EXPECTED_INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_before_execution": observations["integration_head_before"],
        "integration_branch_head_commit_after_execution": observations["integration_head_after"],
        "integration_branch_exists_local": observations["integration_exists"],
        "integration_branch_matches_required_head": observations["integration_head_before"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "integration_branch_deleted_or_reset": False,
        "worktree_restoration_path": str(worktree_path.resolve(strict=False)),
        "worktree_restoration_path_deterministic": worktree_path.resolve(strict=False) == DEFAULT_WORKTREE_PATH.resolve(strict=False),
        "worktree_restoration_path_existed_before_execution": observations["path_existed_before"],
        "worktree_restoration_path_exists_after_execution": observations["path_exists_after"],
        "registered_worktree_entries_present_before_execution": observations["registered_before"],
        "registered_worktree_entries_present_after_execution": observations["registered_after"],
        "git_worktrees_directory_present_before_execution": observations["git_worktrees_before"],
        "git_worktrees_directory_present_after_execution": observations["git_worktrees_after"],
        "detached_worktree_created": True,
        "detached_worktree_restored": True,
        "detached_worktree_deleted": False,
        "registered_detached_worktree_created": True,
        "worktree_head_commit": observations["worktree_head"],
        "worktree_head_verified": observations["worktree_head"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "worktree_is_detached": observations["detached"],
        "worktree_branch_checked_out": not observations["detached"],
        "remote_integration_branch_exists_before_execution": observations["remote_before"],
        "remote_integration_branch_exists_after_execution": observations["remote_after"],
        "integration_branch_pushed": False,
        "worktree_restoration_selected": True,
        "worktree_restoration_approved": True,
        "worktree_restoration_authorized": True,
        "worktree_restoration_executed": True,
        "ready_for_worktree_restoration_results_review": True,
        "remediation_executed": False,
        "evidence_staged": False,
        "marketflow_outputs_copied": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "integration_retry_candidate_created": False,
        "integration_retry_executed": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
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
        "no_tracked_marketflow_files": observations["tracked_marketflow_count"] == 0,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (EXPECTED_SOURCE_APPROVAL_DIGEST, execution.get("source_worktree_restoration_approval_digest")),
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, execution.get("source_worktree_restoration_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, execution.get("source_worktree_restoration_candidate_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, execution.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, execution.get("source_failure_diagnosis_digest")),
        "blocked_execution_status_recorded": (EXPECTED_BLOCKED_EXECUTION_STATUS, execution.get("blocked_remediation_execution_status")),
        "origin_main_before_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, execution.get("origin_main_commit_before_execution")),
        "origin_main_after_unchanged": (EXPECTED_ORIGIN_MAIN_COMMIT, execution.get("origin_main_commit_after_execution")),
        "integration_branch_name_bound": (EXPECTED_INTEGRATION_BRANCH_NAME, execution.get("integration_branch_name")),
        "integration_head_before_bound": (EXPECTED_INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_before_execution")),
        "integration_head_after_unchanged": (EXPECTED_INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_after_execution")),
        "integration_branch_exists_local_true": (True, execution.get("integration_branch_exists_local")),
        "integration_branch_deleted_or_reset_false": (False, execution.get("integration_branch_deleted_or_reset")),
        "deterministic_worktree_path_bound": (str(DEFAULT_WORKTREE_PATH.resolve(strict=False)), execution.get("worktree_restoration_path")),
        "worktree_path_existed_before_false": (False, execution.get("worktree_restoration_path_existed_before_execution")),
        "worktree_path_exists_after_true": (True, execution.get("worktree_restoration_path_exists_after_execution")),
        "registered_worktree_entries_before_false": (False, execution.get("registered_worktree_entries_present_before_execution")),
        "registered_worktree_entries_after_true": (True, execution.get("registered_worktree_entries_present_after_execution")),
        "detached_worktree_created_true": (True, execution.get("detached_worktree_created")),
        "detached_worktree_restored_true": (True, execution.get("detached_worktree_restored")),
        "detached_worktree_deleted_false": (False, execution.get("detached_worktree_deleted")),
        "registered_detached_worktree_created_true": (True, execution.get("registered_detached_worktree_created")),
        "worktree_head_verified_true": (True, execution.get("worktree_head_verified")),
        "worktree_is_detached_true": (True, execution.get("worktree_is_detached")),
        "worktree_branch_checked_out_false": (False, execution.get("worktree_branch_checked_out")),
        "remote_integration_branch_before_false": (False, execution.get("remote_integration_branch_exists_before_execution")),
        "remote_integration_branch_after_false": (False, execution.get("remote_integration_branch_exists_after_execution")),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
        "restoration_selected_true": (True, execution.get("worktree_restoration_selected")),
        "restoration_approved_true": (True, execution.get("worktree_restoration_approved")),
        "restoration_authorized_true": (True, execution.get("worktree_restoration_authorized")),
        "restoration_executed_true": (True, execution.get("worktree_restoration_executed")),
        "ready_for_results_review_true": (True, execution.get("ready_for_worktree_restoration_results_review")),
        "remediation_executed_false": (False, execution.get("remediation_executed")),
        "evidence_staged_false": (False, execution.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, execution.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, execution.get("evidence_regenerated")),
        "retry_candidate_created_false": (False, execution.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, execution.get("integration_retry_executed")),
        "results_review_created_false": (False, execution.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, execution.get("integration_execution_successful")),
        "main_push_false": (False, execution.get("main_push_performed")),
        "origin_main_modified_false": (False, execution.get("origin_main_modified_by_this_task")),
        "provider_requests_false": (False, execution.get("provider_requests_made_in_execution")),
        "market_data_acquisition_false": (False, execution.get("market_data_acquisition_performed_in_execution")),
        "dataset_generation_false": (False, execution.get("dataset_generation_performed_in_execution")),
        "metric_recomputation_false": (False, execution.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, execution.get("model_training_performed")),
        "strategy_scoring_false": (False, execution.get("strategy_scoring_performed")),
        "recommendations_false": (False, execution.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, execution.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, execution.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, execution.get("broker_execution")),
        "next_chain_defined": (NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (True, execution.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "worktree_restoration_executed": True, "detached_worktree_created": True,
        "registered_detached_worktree_created": True, "worktree_head_verified": True,
        "ready_for_worktree_restoration_results_review": True,
        "remediation_executed": False, "evidence_staged": False,
        "integration_retry_executed": False, "integration_results_review_created": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    fields = (
        "integration_branch_name", "integration_branch_head_commit_before_execution",
        "integration_branch_head_commit_after_execution", "worktree_restoration_path",
        "worktree_restoration_path_existed_before_execution",
        "worktree_restoration_path_exists_after_execution",
        "registered_worktree_entries_present_before_execution",
        "registered_worktree_entries_present_after_execution", "worktree_head_commit",
        "worktree_head_verified", "worktree_is_detached", "worktree_branch_checked_out",
    )
    return semantic_digest({field: deepcopy(execution.get(field)) for field in fields})


def marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest",
        None,
    )
    return semantic_digest(payload)


def _records(execution: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    precheck_values = [
        (EXPECTED_SOURCE_APPROVAL_DIGEST, execution["source_worktree_restoration_approval_digest"]),
        (EXPECTED_ORIGIN_MAIN_COMMIT, execution["origin_main_commit_before_execution"]),
        (True, execution["integration_branch_exists_local"]),
        (EXPECTED_INTEGRATION_HEAD_COMMIT, execution["integration_branch_head_commit_before_execution"]),
        (False, execution["remote_integration_branch_exists_before_execution"]),
        (True, execution["worktree_restoration_path_deterministic"]),
        (False, execution["worktree_restoration_path_existed_before_execution"]),
        (True, execution["no_tracked_marketflow_files"]),
        (False, execution["provider_requests_made_in_execution"]),
    ]
    step_values = [
        (EXPECTED_ORIGIN_MAIN_COMMIT, execution["origin_main_commit_after_execution"]),
        (EXPECTED_INTEGRATION_HEAD_COMMIT, execution["integration_branch_head_commit_after_execution"]),
        (False, execution["remote_integration_branch_exists_after_execution"]),
        (True, execution["detached_worktree_created"]),
        (True, execution["registered_worktree_entries_present_after_execution"]),
        (EXPECTED_INTEGRATION_HEAD_COMMIT, execution["worktree_head_commit"]),
        (True, execution["worktree_is_detached"]),
        (False, execution["integration_branch_pushed"]),
        (False, execution["main_push_performed"]),
        (False, execution["evidence_staged"]),
        (False, execution["integration_retry_executed"]),
        (False, execution["integration_results_review_created"]),
    ]
    return (
        [_record(step_id, expected, actual) for step_id, (expected, actual) in zip(PRECHECK_IDS, precheck_values)],
        [_record(step_id, expected, actual) for step_id, (expected, actual) in zip(EXECUTION_STEP_IDS, step_values)],
    )


def execute_marketflow_repository_integration_branch_detached_worktree_restoration_v1(
    *,
    repo_root: str | Path | None = None,
    worktree_path: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    execute_git_operations: bool = True,
) -> dict:
    """Create and record the one approved registered detached worktree."""
    repository = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    target = Path(worktree_path) if worktree_path is not None else DEFAULT_WORKTREE_PATH
    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    observations = (
        _execute_git_restoration(repository.resolve(), target)
        if execute_git_operations
        else _observations_fixture()
    )
    execution = _base_execution(
        worktree_path=target, run_timestamp_utc=timestamp, observations=observations
    )
    prechecks, steps = _records(execution)
    execution["precheck_results"] = prechecks
    execution["execution_steps"] = steps
    execution[
        "marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest_v1(
        execution
    )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution["checklist"])
    execution[
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest_v1(
        execution
    )
    validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
        execution
    )
    return execution


def validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
    execution: dict,
) -> dict:
    """Validate exact refs, worktree state, digests, and closed authorities."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution must be an object"
        )
    timestamp = execution.get("run_timestamp_utc")
    mode = execution.get("git_operation_mode")
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "run timestamp missing"
        )
    if mode not in {"DETERMINISTIC_OPERATION_FIXTURE", "LOCAL_GIT_WORKTREE_EXECUTION"}:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "git operation mode mismatch"
        )
    expected = _base_execution(
        worktree_path=DEFAULT_WORKTREE_PATH,
        run_timestamp_utc=timestamp,
        observations={**_observations_fixture(), "operation_mode": mode},
    )
    for field, value in expected.items():
        if execution.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
                f"{field} mismatch"
            )
    prechecks, steps = _records(execution)
    if execution.get("precheck_results") != prechecks or any(row["status"] != PASS for row in prechecks):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "precheck results mismatch"
        )
    if execution.get("execution_steps") != steps or any(row["status"] != PASS for row in steps):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution steps mismatch"
        )
    manifest_digest = execution.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest"
    )
    if manifest_digest != marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "worktree manifest digest mismatch"
        )
    checklist = execution.get("checklist")
    if checklist != _checklist(execution) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution checklist mismatch or failed"
        )
    if execution.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution summary mismatch"
        )
    digest = execution.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution digest missing"
        )
    if digest != marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationExecutionError(
            "execution digest mismatch"
        )
    return {
        "status": execution["execution_status"],
        "artifact_kind": execution["artifact_kind"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_execution_digest": digest,
        "marketflow_repository_integration_branch_detached_worktree_restoration_worktree_manifest_digest": manifest_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_detached_worktree_restoration_execution_markdown_v1(
    execution: dict,
) -> str:
    """Render the validated restoration execution record."""
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_execution_v1(
        execution
    )
    sections = [
        ("Source Restoration Approval", [f"Digest: `{execution['source_worktree_restoration_approval_digest']}`."]),
        ("Blocked Remediation Execution Observation", [f"`{execution['blocked_remediation_execution_artifact_kind']}` / `{execution['blocked_remediation_execution_status']}`."]),
        ("Execution Scope", [f"`{execution['execution_scope']}`."]),
        ("Worktree Restoration Path", [f"`{execution['worktree_restoration_path']}`."]),
        ("Registered Worktree Creation", ["A registered detached worktree was created; no worktree was deleted or overwritten."]),
        ("Worktree Head Verification", [f"HEAD `{execution['worktree_head_commit']}`; detached: `{execution['worktree_is_detached']}`."]),
        ("Origin/Main Protection", [f"Before/after: `{execution['origin_main_commit_before_execution']}` / `{execution['origin_main_commit_after_execution']}`."]),
        ("Remote Integration Branch Check", ["The remote integration branch remained absent and was not pushed."]),
        ("Authority Boundaries", ["No remediation, evidence staging, retry, results review, predictive/profitability acceptance, runtime, or broker authority was created."]),
        ("Next Chain", execution["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in execution["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in execution["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The next task is the separate restoration results review. The failed integration gate remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Detached Worktree Restoration Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
