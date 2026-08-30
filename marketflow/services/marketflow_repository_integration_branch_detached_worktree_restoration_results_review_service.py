"""Read-only review of the registered detached-worktree restoration result."""

from __future__ import annotations

import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_execution_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1 = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_BLOCKED"
)
BLOCKED_WORKTREE_MISMATCH_OR_DIRTY_STATE = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_BLOCKED_WORKTREE_MISMATCH_OR_DIRTY_STATE"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "b037b1f51df52570a63b417054276fb0bd867dc7a2750b2851a88934a104de0c"
)
EXPECTED_SOURCE_WORKTREE_MANIFEST_DIGEST = (
    "e55415c8abc798086760ce9e37001acd6c16b725213e73f83dbdd448f732a001"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = source.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST
EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND = source.EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND
EXPECTED_BLOCKED_EXECUTION_STATUS = source.EXPECTED_BLOCKED_EXECUTION_STATUS
EXPECTED_ORIGIN_MAIN_COMMIT = source.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_INTEGRATION_BRANCH_NAME = source.EXPECTED_INTEGRATION_BRANCH_NAME
EXPECTED_INTEGRATION_HEAD_COMMIT = source.EXPECTED_INTEGRATION_HEAD_COMMIT
DEFAULT_WORKTREE_PATH = source.DEFAULT_WORKTREE_PATH

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEW_OBSERVATION_IDS = [
    "origin_main_unchanged",
    "integration_branch_head_verified",
    "deterministic_worktree_path_exists",
    "worktree_registered",
    "worktree_head_verified",
    "worktree_detached",
    "worktree_clean",
    "remote_integration_branch_absent",
    "marketflow_outputs_not_tracked",
    "no_remediation_staging",
    "no_retry",
    "no_results_review_before_this_review",
]
NEXT_CHAIN = [
    "Remediation Execution v1 retry, now allowed after worktree restoration review.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1.",
    "Integration Branch Retry Approval v1.",
    "Integration Branch Retry Execution v1.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "remediation_execution_after_worktree_restoration_review",
    "remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_create_worktree",
    "review_does_not_delete_worktree",
    "review_does_not_reset_integration_branch",
    "review_does_not_delete_integration_branch",
    "review_does_not_stage_evidence",
    "review_does_not_copy_marketflow_outputs",
    "review_does_not_commit_marketflow_outputs",
    "review_does_not_run_pytest_retry",
    "review_does_not_create_remediation_execution",
    "review_does_not_create_integration_retry",
    "review_does_not_create_integration_results_review",
    "review_does_not_push_integration_branch",
    "review_does_not_push_main",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_tags",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset",
    "review_does_not_recompute_metrics",
    "review_does_not_train_models",
    "review_does_not_score_strategy",
    "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_broker_execution",
    "separate_remediation_execution_required_after_review",
    "separate_remediation_results_review_required",
    "separate_retry_approval_required_before_integration_retry",
    "protect_origin_main",
    "preserve_existing_integration_branch",
    "preserve_failed_gate",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_V1_RETRY_AFTER_WORKTREE_RESTORATION"
)

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_worktree_manifest_digest_bound",
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_remediation_approval_digest_bound",
    "source_diagnosis_digest_bound", "blocked_execution_status_recorded",
    "origin_main_at_review_bound", "integration_branch_head_at_review_bound",
    "integration_branch_exists_local_true", "integration_branch_matches_required_head_true",
    "integration_branch_deleted_or_reset_false", "worktree_path_exists_true",
    "registered_worktree_entries_present_true", "registered_worktree_path_verified_true",
    "registered_worktree_head_verified_true", "registered_worktree_detached_true",
    "registered_worktree_branch_checked_out_false", "registered_worktree_clean_true",
    "remote_integration_branch_exists_false", "integration_branch_pushed_false",
    "results_review_created_true", "results_review_ready_true",
    "registered_detached_worktree_reviewed_true", "worktree_head_reviewed_true",
    "worktree_detached_status_reviewed_true", "worktree_clean_status_reviewed_true",
    "ready_for_remediation_execution_after_worktree_restoration_true",
    "remediation_executed_false", "evidence_staged_false", "marketflow_outputs_copied_false",
    "marketflow_outputs_committed_false", "evidence_regenerated_false",
    "retry_candidate_created_false", "retry_executed_false",
    "integration_results_review_created_false", "integration_execution_successful_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_not_tracked",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]

EXPECTED_GIT_SNAPSHOT = {
    "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "integration_branch_head_commit": EXPECTED_INTEGRATION_HEAD_COMMIT,
    "integration_branch_exists_local": True,
    "worktree_path_exists": True,
    "registered_worktree_entries_present": True,
    "registered_worktree_path_verified": True,
    "registered_worktree_head_commit": EXPECTED_INTEGRATION_HEAD_COMMIT,
    "registered_worktree_is_detached": True,
    "registered_worktree_branch_checked_out": False,
    "registered_worktree_clean": True,
    "remote_integration_branch_exists": False,
    "tracked_marketflow_file_count": 0,
    "worktree_marketflow_path_exists": False,
}


class MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(ValueError):
    """Raised when read-only restoration review evidence fails closed."""

    def __init__(self, message: str, *, blocked: bool = False) -> None:
        super().__init__(message)
        self.artifact_kind = (
            ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_BLOCKED
            if blocked
            else None
        )
        self.blocked_status = BLOCKED_WORKTREE_MISMATCH_OR_DIRTY_STATE if blocked else None


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
                key = str(Path(current["worktree"]).resolve(strict=False)).casefold()
                rows[key] = current
                current = {}
            continue
        field, _, value = line.partition(" ")
        current[field] = value if value else True
    return rows


def _read_git_snapshot(repo_root: Path, worktree_path: Path) -> dict[str, Any]:
    target = worktree_path.resolve(strict=False)
    target_key = str(target).casefold()
    integration = _git(
        repo_root, "rev-parse", "--verify", EXPECTED_INTEGRATION_BRANCH_NAME, check=False
    )
    rows = _registered_worktrees(repo_root)
    row = rows.get(target_key, {})
    path_exists = target.is_dir()
    registered = target_key in rows
    worktree_head = _git(target, "rev-parse", "HEAD", check=False) if path_exists else None
    symbolic = _git(target, "symbolic-ref", "-q", "HEAD", check=False) if path_exists else None
    status = _git(target, "status", "--porcelain", check=False) if path_exists else None
    remote = _git(
        repo_root,
        "show-ref",
        "--verify",
        "--quiet",
        f"refs/remotes/origin/{EXPECTED_INTEGRATION_BRANCH_NAME}",
        check=False,
    )
    tracked = _git(repo_root, "ls-files", ".marketflow").stdout.splitlines()
    return {
        "origin_main_commit": _git(repo_root, "rev-parse", "origin/main").stdout.strip(),
        "integration_branch_head_commit": integration.stdout.strip(),
        "integration_branch_exists_local": integration.returncode == 0,
        "worktree_path_exists": path_exists,
        "registered_worktree_entries_present": registered,
        "registered_worktree_path_verified": registered and Path(row["worktree"]).resolve(strict=False) == target,
        "registered_worktree_head_commit": (
            worktree_head.stdout.strip() if worktree_head and worktree_head.returncode == 0 else None
        ),
        "registered_worktree_is_detached": bool(
            registered and row.get("detached") is True and symbolic and symbolic.returncode != 0
        ),
        "registered_worktree_branch_checked_out": bool(
            symbolic and symbolic.returncode == 0 and symbolic.stdout.strip()
        ),
        "registered_worktree_clean": bool(status and status.returncode == 0 and not status.stdout),
        "remote_integration_branch_exists": remote.returncode == 0,
        "tracked_marketflow_file_count": len(tracked),
        "worktree_marketflow_path_exists": (target / ".marketflow").exists() if path_exists else False,
    }


def _snapshot_or_raise(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, Mapping):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "git snapshot must be an object", blocked=True
        )
    normalized = {key: deepcopy(snapshot.get(key)) for key in EXPECTED_GIT_SNAPSHOT}
    if normalized != EXPECTED_GIT_SNAPSHOT:
        mismatches = [
            key for key, expected in EXPECTED_GIT_SNAPSHOT.items() if normalized.get(key) != expected
        ]
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            f"worktree review snapshot mismatch: {', '.join(mismatches)}", blocked=True
        )
    return normalized


def _observation(observation_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "observation_id": observation_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "message": f"{observation_id} {'passed' if status == PASS else 'failed'}",
    }


def _base_review(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN,
        "created_offline_except_read_only_git_inspection": True,
        "governance_only": True,
        "source_worktree_restoration_execution_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED,
        "source_worktree_restoration_execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTED_REGISTERED_DETACHED_WORKTREE_CREATED,
        "source_worktree_restoration_execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW,
        "source_worktree_restoration_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_worktree_manifest_digest": EXPECTED_SOURCE_WORKTREE_MANIFEST_DIGEST,
        "source_worktree_restoration_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_worktree_restoration_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_worktree_restoration_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "origin_main_commit_at_review": snapshot["origin_main_commit"],
        "blocked_remediation_execution_artifact_kind": EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND,
        "blocked_remediation_execution_status": EXPECTED_BLOCKED_EXECUTION_STATUS,
        "integration_branch_name": EXPECTED_INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_at_review": snapshot["integration_branch_head_commit"],
        "integration_branch_exists_local_at_review": snapshot["integration_branch_exists_local"],
        "integration_branch_matches_required_head_at_review": snapshot["integration_branch_head_commit"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "integration_branch_deleted_or_reset_by_review": False,
        "worktree_restoration_path": str(DEFAULT_WORKTREE_PATH.resolve(strict=False)),
        "worktree_restoration_path_exists_at_review": snapshot["worktree_path_exists"],
        "registered_worktree_entries_present_at_review": snapshot["registered_worktree_entries_present"],
        "registered_worktree_path_verified": snapshot["registered_worktree_path_verified"],
        "registered_worktree_head_commit": snapshot["registered_worktree_head_commit"],
        "registered_worktree_head_verified": snapshot["registered_worktree_head_commit"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "registered_worktree_is_detached": snapshot["registered_worktree_is_detached"],
        "registered_worktree_branch_checked_out": snapshot["registered_worktree_branch_checked_out"],
        "registered_worktree_clean": snapshot["registered_worktree_clean"],
        "remote_integration_branch_exists_at_review": snapshot["remote_integration_branch_exists"],
        "integration_branch_pushed": False,
        "worktree_restoration_results_review_created": True,
        "worktree_restoration_results_review_ready": True,
        "registered_detached_worktree_reviewed": True,
        "worktree_head_reviewed": True,
        "worktree_detached_status_reviewed": True,
        "worktree_clean_status_reviewed": True,
        "ready_for_remediation_execution_after_worktree_restoration": True,
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
        "tracked_marketflow_file_count": snapshot["tracked_marketflow_file_count"],
        "worktree_marketflow_path_exists_at_review": snapshot["worktree_marketflow_path_exists"],
        "marketflow_outputs_not_tracked": snapshot["tracked_marketflow_file_count"] == 0,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
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
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "no_tracked_marketflow_files": snapshot["tracked_marketflow_file_count"] == 0,
    }


def _review_observations(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = [
        (EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        (EXPECTED_INTEGRATION_HEAD_COMMIT, review.get("integration_branch_head_commit_at_review")),
        (True, review.get("worktree_restoration_path_exists_at_review")),
        (True, review.get("registered_worktree_entries_present_at_review")),
        (True, review.get("registered_worktree_head_verified")),
        (True, review.get("registered_worktree_is_detached")),
        (True, review.get("registered_worktree_clean")),
        (False, review.get("remote_integration_branch_exists_at_review")),
        (True, review.get("marketflow_outputs_not_tracked")),
        (False, review.get("evidence_staged")),
        (False, review.get("integration_retry_executed")),
        (False, review.get("integration_results_review_created")),
    ]
    return [
        _observation(observation_id, expected, actual)
        for observation_id, (expected, actual) in zip(REVIEW_OBSERVATION_IDS, values)
    ]


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_execution_digest_bound": (EXPECTED_SOURCE_EXECUTION_DIGEST, review.get("source_worktree_restoration_execution_digest")),
        "source_worktree_manifest_digest_bound": (EXPECTED_SOURCE_WORKTREE_MANIFEST_DIGEST, review.get("source_worktree_manifest_digest")),
        "source_approval_digest_bound": (EXPECTED_SOURCE_APPROVAL_DIGEST, review.get("source_worktree_restoration_approval_digest")),
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, review.get("source_worktree_restoration_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_worktree_restoration_candidate_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, review.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, review.get("source_failure_diagnosis_digest")),
        "blocked_execution_status_recorded": (EXPECTED_BLOCKED_EXECUTION_STATUS, review.get("blocked_remediation_execution_status")),
        "origin_main_at_review_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        "integration_branch_head_at_review_bound": (EXPECTED_INTEGRATION_HEAD_COMMIT, review.get("integration_branch_head_commit_at_review")),
        "integration_branch_exists_local_true": (True, review.get("integration_branch_exists_local_at_review")),
        "integration_branch_matches_required_head_true": (True, review.get("integration_branch_matches_required_head_at_review")),
        "integration_branch_deleted_or_reset_false": (False, review.get("integration_branch_deleted_or_reset_by_review")),
        "worktree_path_exists_true": (True, review.get("worktree_restoration_path_exists_at_review")),
        "registered_worktree_entries_present_true": (True, review.get("registered_worktree_entries_present_at_review")),
        "registered_worktree_path_verified_true": (True, review.get("registered_worktree_path_verified")),
        "registered_worktree_head_verified_true": (True, review.get("registered_worktree_head_verified")),
        "registered_worktree_detached_true": (True, review.get("registered_worktree_is_detached")),
        "registered_worktree_branch_checked_out_false": (False, review.get("registered_worktree_branch_checked_out")),
        "registered_worktree_clean_true": (True, review.get("registered_worktree_clean")),
        "remote_integration_branch_exists_false": (False, review.get("remote_integration_branch_exists_at_review")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "results_review_created_true": (True, review.get("worktree_restoration_results_review_created")),
        "results_review_ready_true": (True, review.get("worktree_restoration_results_review_ready")),
        "registered_detached_worktree_reviewed_true": (True, review.get("registered_detached_worktree_reviewed")),
        "worktree_head_reviewed_true": (True, review.get("worktree_head_reviewed")),
        "worktree_detached_status_reviewed_true": (True, review.get("worktree_detached_status_reviewed")),
        "worktree_clean_status_reviewed_true": (True, review.get("worktree_clean_status_reviewed")),
        "ready_for_remediation_execution_after_worktree_restoration_true": (True, review.get("ready_for_remediation_execution_after_worktree_restoration")),
        "remediation_executed_false": (False, review.get("remediation_executed")),
        "evidence_staged_false": (False, review.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, review.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
        "retry_candidate_created_false": (False, review.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, review.get("integration_retry_executed")),
        "integration_results_review_created_false": (False, review.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_not_tracked": (True, review.get("marketflow_outputs_not_tracked")),
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
        "worktree_restoration_results_review_created": True,
        "worktree_restoration_results_review_ready": True,
        "registered_detached_worktree_reviewed": True,
        "registered_worktree_head_verified": True,
        "registered_worktree_is_detached": True,
        "registered_worktree_clean": True,
        "ready_for_remediation_execution_after_worktree_restoration": True,
        "remediation_executed": False, "evidence_staged": False,
        "integration_retry_executed": False, "integration_results_review_created": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest_v1(
    review: Mapping[str, Any],
) -> str:
    fields = (
        "worktree_restoration_path", "worktree_restoration_path_exists_at_review",
        "registered_worktree_entries_present_at_review", "registered_worktree_path_verified",
        "registered_worktree_head_commit", "registered_worktree_head_verified",
        "registered_worktree_is_detached", "registered_worktree_branch_checked_out",
        "registered_worktree_clean", "worktree_marketflow_path_exists_at_review",
    )
    return semantic_digest({field: deepcopy(review.get(field)) for field in fields})


def marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
    *,
    repo_root: str | Path | None = None,
    worktree_path: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict:
    """Build the review from deterministic evidence or read-only Git inspection."""
    repository = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    target = Path(worktree_path) if worktree_path is not None else DEFAULT_WORKTREE_PATH
    if target.resolve(strict=False) != DEFAULT_WORKTREE_PATH.resolve(strict=False):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "worktree path is not the deterministic approved path", blocked=True
        )
    snapshot = _snapshot_or_raise(
        git_snapshot if git_snapshot is not None else _read_git_snapshot(repository.resolve(), target)
    )
    review = _base_review(snapshot)
    review["review_observations"] = _review_observations(review)
    review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest_v1(
        review
    )
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        review
    )
    return review


def validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
    review: dict,
) -> dict:
    """Validate the exact reviewed worktree state and closed authority boundaries."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review must be an object"
        )
    expected = _base_review(EXPECTED_GIT_SNAPSHOT)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
                f"{field} mismatch"
            )
    observations = review.get("review_observations")
    if observations != _review_observations(review) or any(
        row.get("status") != PASS for row in observations or []
    ):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review observations mismatch or failed"
        )
    manifest_digest = review.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest"
    )
    if manifest_digest != marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest_v1(review):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "worktree manifest review digest mismatch"
        )
    checklist = review.get("checklist")
    if checklist != _checklist(review) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review checklist mismatch or failed"
        )
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review summary mismatch"
        )
    digest = review.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review digest missing"
        )
    if digest != marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest_v1(review):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "review digest mismatch"
        )
    return {
        "status": review["review_status"], "artifact_kind": review["artifact_kind"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest": digest,
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest": manifest_digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated read-only restoration results review."""
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        review
    )
    sections = [
        ("Source Restoration Execution", [f"Execution/status: `{review['source_worktree_restoration_execution_artifact_kind']}` / `{review['source_worktree_restoration_execution_status']}`."]),
        ("Bound Evidence", [f"Execution digest: `{review['source_worktree_restoration_execution_digest']}`.", f"Source manifest digest: `{review['source_worktree_manifest_digest']}`."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Registered Worktree Review", [f"Path `{review['worktree_restoration_path']}` is present and registered."]),
        ("Worktree Head Verification", [f"HEAD `{review['registered_worktree_head_commit']}`; detached: `{review['registered_worktree_is_detached']}`."]),
        ("Worktree Cleanliness Review", [f"Clean: `{review['registered_worktree_clean']}`; `.marketflow` present: `{review['worktree_marketflow_path_exists_at_review']}`."]),
        ("Origin/Main Protection", [f"`origin/main` remained `{review['origin_main_commit_at_review']}`."]),
        ("Remote Integration Branch Check", ["The remote integration branch remains absent and was not pushed."]),
        ("Authority Boundaries", ["Review creates no remediation, staging, retry, integration success, predictive/profitability acceptance, runtime, or broker authority."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Only a separate remediation execution task may act on this readiness result; the prior blocked gate remains preserved."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Detached Worktree Restoration Results Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
    output_dir: str | Path,
    *,
    repo_root: str | Path | None = None,
    worktree_path: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        repo_root=repo_root, worktree_path=worktree_path, git_snapshot=git_snapshot
    )
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError(
            "results-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest": validation[
            "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
