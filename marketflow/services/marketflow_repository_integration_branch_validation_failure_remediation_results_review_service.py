"""Read-only review of validation-failure remediation evidence staging."""

from __future__ import annotations

import hashlib
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_execution_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1 = (
    "marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_ONLY_NOT_RETRY_NOT_INTEGRATION_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_ONLY_NOT_RETRY_NOT_INTEGRATION_RESULTS_REVIEW_NOT_MAIN"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED_STAGED_EVIDENCE_MISMATCH_OR_TRACKING_RISK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED_STAGED_EVIDENCE_MISMATCH_OR_TRACKING_RISK"
)

EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST = "4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346"
EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST = "ca97ebf04c84a3008e222e2fa16a15c18e2528a21bee67e0a43bd82990e99fae"
EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST = "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST = "562c6bc4cadb09232ca304efb803d566c0904226314b8f94cceef2e54122159a"
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_MANIFEST_DIGEST = "415f2445805f93906b5f63035472f8edb95f41f64c57c46eab659e5221cc738d"
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = "681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded"
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = "f32d7ded083256f4301903de41e1fdf06562b4af0e5bd0fc2c75685d4fd8a301"
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = "2d45ef960b45d6a81b6e494b77a44f3dba482567e973e83999844ce9ce351fc2"
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = "a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947"
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = "34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c"
EXPECTED_ORIGIN_MAIN_COMMIT = source.INTEGRATION_BASE_COMMIT
EXPECTED_INTEGRATION_BRANCH_NAME = source.INTEGRATION_BRANCH_NAME
EXPECTED_INTEGRATION_HEAD_COMMIT = source.INTEGRATION_HEAD_COMMIT
ATTEMPTED_EXECUTION_BRANCH = source.ATTEMPTED_EXECUTION_BRANCH
ATTEMPTED_EXECUTION_COMMIT = source.ATTEMPTED_EXECUTION_COMMIT
DEFAULT_INTEGRATION_WORKTREE_PATH = source.DEFAULT_INTEGRATION_WORKTREE_PATH
DEFAULT_SOURCE_EVIDENCE_ROOT = source.DEFAULT_SOURCE_EVIDENCE_ROOT
DEFAULT_STAGED_EVIDENCE_ROOT = (
    DEFAULT_INTEGRATION_WORKTREE_PATH
    / ".marketflow"
    / "acquisition_provider_evidence"
    / "expanded_universe_v1"
)
REQUIRED_MANIFEST_NAME = source.REQUIRED_MANIFEST_NAME
EXPECTED_EVIDENCE_MANIFEST_ROWS = deepcopy(source.EXPECTED_EVIDENCE_MANIFEST_ROWS)
EXPECTED_EVIDENCE_FILE_COUNT = source.EXPECTED_EVIDENCE_FILE_COUNT
EXPECTED_EVIDENCE_TOTAL_BYTES = source.EXPECTED_EVIDENCE_TOTAL_BYTES

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1"

REVIEW_OBSERVATION_IDS = [
    "source_remediation_execution_digest_bound",
    "evidence_manifest_digest_bound",
    "origin_main_unchanged",
    "integration_branch_head_verified",
    "detached_worktree_verified",
    "detached_worktree_clean",
    "staged_evidence_root_exists",
    "staged_manifest_exists",
    "source_staged_file_count_match",
    "source_staged_byte_count_match",
    "source_staged_digest_match",
    "staged_evidence_untracked",
    "marketflow_outputs_not_tracked",
    "no_evidence_regeneration",
    "no_integration_retry",
    "no_integration_results_review",
    "no_integration_success_claim",
    "no_provider_or_runtime_actions",
]

NEXT_CHAIN = [
    "Integration Branch Retry Candidate v1.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_run_integration_retry",
    "review_does_not_create_retry_candidate",
    "review_does_not_create_retry_execution",
    "review_does_not_create_integration_results_review",
    "review_does_not_mark_integration_successful",
    "review_does_not_generate_successful_integration_execution_digest",
    "review_does_not_generate_successful_integration_validation_digest",
    "review_does_not_stage_additional_evidence",
    "review_does_not_modify_staged_evidence",
    "review_does_not_regenerate_evidence",
    "review_does_not_call_providers",
    "review_does_not_commit_marketflow_outputs",
    "review_does_not_track_marketflow_outputs",
    "review_does_not_push_integration_branch",
    "review_does_not_push_main",
    "review_does_not_delete_integration_branch",
    "review_does_not_delete_worktree",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_tags",
    "review_does_not_push_additional_tags",
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
    "first_failed_pytest_remains_authoritative",
    "later_wrong_worktree_rerun_remains_diagnostic_only",
    "separate_retry_candidate_required_after_remediation_review",
    "separate_retry_approval_required_before_integration_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_evidence_manifest_digest_bound",
    "source_staged_inventory_manifest_digest_bound", "source_worktree_restoration_results_review_digest_bound",
    "source_remediation_approval_digest_bound", "source_diagnosis_digest_bound",
    "origin_main_at_review_bound", "origin_main_unchanged", "integration_branch_head_verified",
    "remote_integration_branch_absent", "detached_worktree_exists_true",
    "detached_worktree_head_verified", "detached_worktree_detached_true",
    "detached_worktree_clean_true", "source_evidence_root_exists_true",
    "staged_evidence_root_exists_true", "staged_manifest_exists_true",
    "source_evidence_file_count_7", "staged_evidence_file_count_7",
    "source_evidence_total_bytes_match", "staged_evidence_total_bytes_match",
    "source_staged_digest_match_true", "staged_evidence_untracked_true",
    "marketflow_outputs_tracked_repository_false", "marketflow_outputs_tracked_detached_false",
    "results_review_created_true", "results_review_ready_true", "staged_evidence_reviewed_true",
    "staged_manifest_reviewed_true", "source_staged_digest_match_reviewed_true",
    "staged_evidence_untracked_reviewed_true", "wrong_worktree_guard_reviewed_true",
    "ready_for_retry_candidate_true", "remediation_executed_true", "evidence_staged_true",
    "marketflow_outputs_copied_true", "marketflow_outputs_committed_false",
    "evidence_regenerated_false", "retry_candidate_created_false", "retry_executed_false",
    "integration_results_review_created_false", "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "remote_integration_branch_created_false", "main_merge_false", "main_push_false",
    "origin_main_modified_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]

EXPECTED_GIT_SNAPSHOT = {
    "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "integration_branch_head_commit": EXPECTED_INTEGRATION_HEAD_COMMIT,
    "remote_integration_branch_exists": False,
    "worktree_exists": True,
    "worktree_head_commit": EXPECTED_INTEGRATION_HEAD_COMMIT,
    "worktree_is_detached": True,
    "worktree_clean": True,
    "repository_tracked_marketflow_file_count": 0,
    "worktree_tracked_marketflow_file_count": 0,
    "staged_evidence_ignored": True,
}
EXPECTED_EVIDENCE_SNAPSHOT = {
    "source_root_exists": True,
    "staged_root_exists": True,
    "staged_manifest_exists": True,
    "source_manifest": deepcopy(EXPECTED_EVIDENCE_MANIFEST_ROWS),
    "staged_manifest": deepcopy(EXPECTED_EVIDENCE_MANIFEST_ROWS),
}


class MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(ValueError):
    """Raised when read-only remediation review evidence fails closed."""

    def __init__(self, message: str, *, blocked: bool = False) -> None:
        super().__init__(message)
        self.artifact_kind = (
            ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED
            if blocked else None
        )
        self.blocked_status = (
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED_STAGED_EVIDENCE_MISMATCH_OR_TRACKING_RISK
            if blocked else None
        )


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=check, capture_output=True,
        text=True, encoding="utf-8",
    )


def _inventory(root: Path) -> list[dict[str, Any]]:
    if not root.is_dir():
        return []
    rows = []
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix(),
    ):
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        rows.append({
            "relative_path": path.relative_to(root).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": digest.hexdigest(),
        })
    return rows


def _read_git_snapshot(repo_root: Path, worktree: Path) -> dict[str, Any]:
    worktree_exists = worktree.is_dir()
    worktree_head = _git(worktree, "rev-parse", "HEAD", check=False) if worktree_exists else None
    symbolic = _git(worktree, "symbolic-ref", "-q", "HEAD", check=False) if worktree_exists else None
    status = _git(worktree, "status", "--porcelain", check=False) if worktree_exists else None
    remote = _git(
        repo_root, "show-ref", "--verify", "--quiet",
        f"refs/remotes/origin/{EXPECTED_INTEGRATION_BRANCH_NAME}", check=False,
    )
    ignored = _git(
        worktree, "check-ignore", "--quiet", "--",
        ".marketflow/acquisition_provider_evidence/expanded_universe_v1", check=False,
    ) if worktree_exists else None
    return {
        "origin_main_commit": _git(repo_root, "rev-parse", "origin/main").stdout.strip(),
        "integration_branch_head_commit": _git(
            repo_root, "rev-parse", "--verify", EXPECTED_INTEGRATION_BRANCH_NAME
        ).stdout.strip(),
        "remote_integration_branch_exists": remote.returncode == 0,
        "worktree_exists": worktree_exists,
        "worktree_head_commit": (
            worktree_head.stdout.strip() if worktree_head and worktree_head.returncode == 0 else None
        ),
        "worktree_is_detached": bool(symbolic and symbolic.returncode != 0),
        "worktree_clean": bool(status and status.returncode == 0 and not status.stdout),
        "repository_tracked_marketflow_file_count": len(
            _git(repo_root, "ls-files", ".marketflow").stdout.splitlines()
        ),
        "worktree_tracked_marketflow_file_count": (
            len(_git(worktree, "ls-files", ".marketflow").stdout.splitlines()) if worktree_exists else -1
        ),
        "staged_evidence_ignored": bool(ignored and ignored.returncode == 0),
    }


def _read_evidence_snapshot(source_root: Path, staged_root: Path) -> dict[str, Any]:
    return {
        "source_root_exists": source_root.is_dir(),
        "staged_root_exists": staged_root.is_dir(),
        "staged_manifest_exists": (staged_root / REQUIRED_MANIFEST_NAME).is_file(),
        "source_manifest": _inventory(source_root),
        "staged_manifest": _inventory(staged_root),
    }


def _snapshot_or_raise(
    snapshot: Mapping[str, Any], expected: Mapping[str, Any], name: str,
) -> dict[str, Any]:
    if not isinstance(snapshot, Mapping):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            f"{name} snapshot must be an object", blocked=True
        )
    normalized = {key: deepcopy(snapshot.get(key)) for key in expected}
    if normalized != expected:
        mismatches = [key for key, value in expected.items() if normalized.get(key) != value]
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            f"{name} snapshot mismatch: {', '.join(mismatches)}", blocked=True
        )
    return normalized


def _observation(observation_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "observation_id": observation_id, "status": status,
        "expected": deepcopy(expected), "actual": deepcopy(actual),
        "message": f"{observation_id} {'passed' if status == PASS else 'failed'}",
    }


def _base_review(git_snapshot: Mapping[str, Any], evidence_snapshot: Mapping[str, Any]) -> dict[str, Any]:
    source_manifest = deepcopy(evidence_snapshot["source_manifest"])
    staged_manifest = deepcopy(evidence_snapshot["staged_manifest"])
    source_digest = semantic_digest(source_manifest)
    staged_digest = semantic_digest(staged_manifest)
    source_count = len(source_manifest)
    staged_count = len(staged_manifest)
    source_bytes = sum(row["size_bytes"] for row in source_manifest)
    staged_bytes = sum(row["size_bytes"] for row in staged_manifest)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_ONLY_NOT_RETRY_NOT_INTEGRATION_RESULTS_REVIEW_NOT_MAIN,
        "created_offline_except_read_only_file_and_git_inspection": True,
        "governance_only": True,
        "source_remediation_execution_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED,
        "source_remediation_execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION,
        "source_remediation_execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_remediation_execution_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "source_remediation_evidence_manifest_digest": EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST,
        "source_staged_inventory_manifest_digest": EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST,
        "source_worktree_restoration_results_review_digest": EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST,
        "source_worktree_restoration_results_review_manifest_digest": EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "attempted_execution_branch": ATTEMPTED_EXECUTION_BRANCH,
        "attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
        "origin_main_commit_at_review": git_snapshot["origin_main_commit"],
        "integration_branch_name": EXPECTED_INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_at_review": git_snapshot["integration_branch_head_commit"],
        "integration_branch_matches_required_head_at_review": git_snapshot["integration_branch_head_commit"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists_at_review": git_snapshot["remote_integration_branch_exists"],
        "detached_integration_worktree_path": str(DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False)),
        "detached_integration_worktree_exists_at_review": git_snapshot["worktree_exists"],
        "detached_integration_worktree_head_commit_at_review": git_snapshot["worktree_head_commit"],
        "detached_integration_worktree_head_verified_at_review": git_snapshot["worktree_head_commit"] == EXPECTED_INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_is_detached_at_review": git_snapshot["worktree_is_detached"],
        "detached_integration_worktree_clean_at_review": git_snapshot["worktree_clean"],
        "source_evidence_root_path": str(DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False)),
        "staged_evidence_root_path": str(DEFAULT_STAGED_EVIDENCE_ROOT.resolve(strict=False)),
        "staged_required_manifest_path": str((DEFAULT_STAGED_EVIDENCE_ROOT / REQUIRED_MANIFEST_NAME).resolve(strict=False)),
        "source_evidence_root_exists_at_review": evidence_snapshot["source_root_exists"],
        "staged_evidence_root_exists_at_review": evidence_snapshot["staged_root_exists"],
        "staged_required_manifest_exists_at_review": evidence_snapshot["staged_manifest_exists"],
        "source_evidence_manifest": source_manifest,
        "staged_evidence_manifest": staged_manifest,
        "source_evidence_file_count_at_review": source_count,
        "staged_evidence_file_count_at_review": staged_count,
        "source_evidence_total_bytes_at_review": source_bytes,
        "staged_evidence_total_bytes_at_review": staged_bytes,
        "source_evidence_manifest_digest_at_review": source_digest,
        "staged_evidence_manifest_digest_at_review": staged_digest,
        "source_and_staged_evidence_match_at_review": source_manifest == staged_manifest,
        "staged_evidence_root_untracked_at_review": git_snapshot["staged_evidence_ignored"] and git_snapshot["worktree_tracked_marketflow_file_count"] == 0,
        "marketflow_outputs_tracked_in_repository": git_snapshot["repository_tracked_marketflow_file_count"] != 0,
        "marketflow_outputs_tracked_in_detached_worktree": git_snapshot["worktree_tracked_marketflow_file_count"] != 0,
        "remediation_results_review_created": True,
        "remediation_results_review_ready": True,
        "staged_evidence_reviewed": True,
        "staged_manifest_reviewed": True,
        "source_staged_digest_match_reviewed": True,
        "staged_evidence_untracked_reviewed": True,
        "wrong_worktree_guard_reviewed": True,
        "ready_for_integration_branch_retry_candidate": True,
        "remediation_executed": True,
        "evidence_staged": True,
        "marketflow_outputs_copied_to_integration_worktree": True,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "integration_retry_candidate_created": False,
        "integration_retry_approved": False,
        "integration_retry_executed": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
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
        "no_tracked_marketflow_files": git_snapshot["repository_tracked_marketflow_file_count"] == 0 and git_snapshot["worktree_tracked_marketflow_file_count"] == 0,
    }


def _review_observations(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    provider_runtime_clear = all(
        review.get(field) is expected for field, expected in (
            ("provider_requests_made_in_review", False),
            ("market_data_acquisition_performed_in_review", False),
            ("model_training_performed", False),
        )
    ) and review.get("runtime_use") == NOT_AUTHORIZED
    values = [
        (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, review.get("source_remediation_execution_digest")),
        (EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST, review.get("source_remediation_evidence_manifest_digest")),
        (EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        (True, review.get("integration_branch_matches_required_head_at_review")),
        (True, review.get("detached_integration_worktree_head_verified_at_review")),
        (True, review.get("detached_integration_worktree_clean_at_review")),
        (True, review.get("staged_evidence_root_exists_at_review")),
        (True, review.get("staged_required_manifest_exists_at_review")),
        (review.get("source_evidence_file_count_at_review"), review.get("staged_evidence_file_count_at_review")),
        (review.get("source_evidence_total_bytes_at_review"), review.get("staged_evidence_total_bytes_at_review")),
        (True, review.get("source_and_staged_evidence_match_at_review")),
        (True, review.get("staged_evidence_root_untracked_at_review")),
        (True, review.get("no_tracked_marketflow_files")),
        (False, review.get("evidence_regenerated")),
        (False, review.get("integration_retry_executed")),
        (False, review.get("integration_results_review_created")),
        (False, review.get("integration_execution_successful")),
        (True, provider_runtime_clear),
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
        "source_execution_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, review.get("source_remediation_execution_digest")),
        "source_evidence_manifest_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST, review.get("source_remediation_evidence_manifest_digest")),
        "source_staged_inventory_manifest_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST, review.get("source_staged_inventory_manifest_digest")),
        "source_worktree_restoration_results_review_digest_bound": (EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST, review.get("source_worktree_restoration_results_review_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, review.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST, review.get("source_failure_diagnosis_digest")),
        "origin_main_at_review_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        "origin_main_unchanged": (EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit_at_review")),
        "integration_branch_head_verified": (True, review.get("integration_branch_matches_required_head_at_review")),
        "remote_integration_branch_absent": (False, review.get("remote_integration_branch_exists_at_review")),
        "detached_worktree_exists_true": (True, review.get("detached_integration_worktree_exists_at_review")),
        "detached_worktree_head_verified": (True, review.get("detached_integration_worktree_head_verified_at_review")),
        "detached_worktree_detached_true": (True, review.get("detached_integration_worktree_is_detached_at_review")),
        "detached_worktree_clean_true": (True, review.get("detached_integration_worktree_clean_at_review")),
        "source_evidence_root_exists_true": (True, review.get("source_evidence_root_exists_at_review")),
        "staged_evidence_root_exists_true": (True, review.get("staged_evidence_root_exists_at_review")),
        "staged_manifest_exists_true": (True, review.get("staged_required_manifest_exists_at_review")),
        "source_evidence_file_count_7": (EXPECTED_EVIDENCE_FILE_COUNT, review.get("source_evidence_file_count_at_review")),
        "staged_evidence_file_count_7": (EXPECTED_EVIDENCE_FILE_COUNT, review.get("staged_evidence_file_count_at_review")),
        "source_evidence_total_bytes_match": (EXPECTED_EVIDENCE_TOTAL_BYTES, review.get("source_evidence_total_bytes_at_review")),
        "staged_evidence_total_bytes_match": (EXPECTED_EVIDENCE_TOTAL_BYTES, review.get("staged_evidence_total_bytes_at_review")),
        "source_staged_digest_match_true": (True, review.get("source_and_staged_evidence_match_at_review")),
        "staged_evidence_untracked_true": (True, review.get("staged_evidence_root_untracked_at_review")),
        "marketflow_outputs_tracked_repository_false": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "marketflow_outputs_tracked_detached_false": (False, review.get("marketflow_outputs_tracked_in_detached_worktree")),
        "results_review_created_true": (True, review.get("remediation_results_review_created")),
        "results_review_ready_true": (True, review.get("remediation_results_review_ready")),
        "staged_evidence_reviewed_true": (True, review.get("staged_evidence_reviewed")),
        "staged_manifest_reviewed_true": (True, review.get("staged_manifest_reviewed")),
        "source_staged_digest_match_reviewed_true": (True, review.get("source_staged_digest_match_reviewed")),
        "staged_evidence_untracked_reviewed_true": (True, review.get("staged_evidence_untracked_reviewed")),
        "wrong_worktree_guard_reviewed_true": (True, review.get("wrong_worktree_guard_reviewed")),
        "ready_for_retry_candidate_true": (True, review.get("ready_for_integration_branch_retry_candidate")),
        "remediation_executed_true": (True, review.get("remediation_executed")),
        "evidence_staged_true": (True, review.get("evidence_staged")),
        "marketflow_outputs_copied_true": (True, review.get("marketflow_outputs_copied_to_integration_worktree")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
        "retry_candidate_created_false": (False, review.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, review.get("integration_retry_executed")),
        "integration_results_review_created_false": (False, review.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, review.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, review.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, review.get("remote_integration_branch_created")),
        "main_merge_false": (False, review.get("main_merge_performed")),
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
        "remediation_results_review_created": True,
        "remediation_results_review_ready": True,
        "staged_evidence_reviewed": True,
        "source_and_staged_evidence_match": True,
        "staged_evidence_root_untracked": True,
        "ready_for_integration_branch_retry_candidate": True,
        "integration_retry_candidate_created": False,
        "integration_retry_executed": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest_v1(
    review: Mapping[str, Any],
) -> str:
    return semantic_digest({
        "source_evidence_manifest": deepcopy(review.get("source_evidence_manifest")),
        "staged_evidence_manifest": deepcopy(review.get("staged_evidence_manifest")),
        "source_evidence_manifest_digest_at_review": review.get("source_evidence_manifest_digest_at_review"),
        "staged_evidence_manifest_digest_at_review": review.get("staged_evidence_manifest_digest_at_review"),
        "source_and_staged_evidence_match_at_review": review.get("source_and_staged_evidence_match_at_review"),
        "staged_evidence_root_untracked_at_review": review.get("staged_evidence_root_untracked_at_review"),
    })


def marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
    *,
    repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    source_evidence_root_path: str | Path | None = None,
    git_snapshot: dict | None = None,
    evidence_snapshot: dict | None = None,
) -> dict:
    """Build the review from deterministic snapshots or read-only inspection."""
    repository = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    worktree = Path(integration_worktree_path) if integration_worktree_path is not None else DEFAULT_INTEGRATION_WORKTREE_PATH
    source_root = Path(source_evidence_root_path) if source_evidence_root_path is not None else DEFAULT_SOURCE_EVIDENCE_ROOT
    if worktree.resolve(strict=False) != DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "wrong-worktree guard blocked results review", blocked=True
        )
    if source_root.resolve(strict=False) != DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "source evidence path mismatch", blocked=True
        )
    staged_root = worktree.resolve(strict=False) / ".marketflow" / "acquisition_provider_evidence" / "expanded_universe_v1"
    git_values = _snapshot_or_raise(
        git_snapshot if git_snapshot is not None else _read_git_snapshot(repository.resolve(), worktree.resolve(strict=False)),
        EXPECTED_GIT_SNAPSHOT, "git",
    )
    evidence_values = _snapshot_or_raise(
        evidence_snapshot if evidence_snapshot is not None else _read_evidence_snapshot(source_root.resolve(strict=False), staged_root),
        EXPECTED_EVIDENCE_SNAPSHOT, "evidence",
    )
    review = _base_review(git_values, evidence_values)
    review["review_observations"] = _review_observations(review)
    review[
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest_v1(review)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review[
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest_v1(review)
    validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
    review: dict,
) -> dict:
    """Validate exact evidence bindings and every closed authority boundary."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review must be an object"
        )
    expected = _base_review(EXPECTED_GIT_SNAPSHOT, EXPECTED_EVIDENCE_SNAPSHOT)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
                f"{field} mismatch"
            )
    observations = review.get("review_observations")
    if observations != _review_observations(review) or any(
        row.get("status") != PASS for row in observations or []
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review observations mismatch or failed"
        )
    evidence_digest = review.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest"
    )
    if evidence_digest != marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest_v1(review):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "evidence manifest review digest mismatch"
        )
    checklist = review.get("checklist")
    if checklist != _checklist(review) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review checklist mismatch or failed"
        )
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review summary mismatch"
        )
    digest = review.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review digest missing"
        )
    if digest != marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest_v1(review):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "review digest mismatch"
        )
    return {
        "status": review["review_status"], "artifact_kind": review["artifact_kind"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest": digest,
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest": evidence_digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated read-only remediation results review."""
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(review)
    sections = [
        ("Source Remediation Execution", [f"Artifact/status: `{review['source_remediation_execution_artifact_kind']}` / `{review['source_remediation_execution_status']}`."]),
        ("Source Worktree Restoration Review", [f"Digest: `{review['source_worktree_restoration_results_review_digest']}`."]),
        ("Failure Context", ["The first integration pytest remains authoritative; the later wrong-worktree pass is diagnostic only."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Detached Worktree Review", [f"`{review['detached_integration_worktree_path']}` at `{review['detached_integration_worktree_head_commit_at_review']}` is detached and clean."]),
        ("Staged Evidence Review", [f"`{review['staged_evidence_file_count_at_review']}` files / `{review['staged_evidence_total_bytes_at_review']}` bytes; required manifest exists."]),
        ("Digest Verification", [f"Source/staged digest `{review['source_evidence_manifest_digest_at_review']}` matches: `{review['source_and_staged_evidence_match_at_review']}`."]),
        ("Tracking and Commit Boundary", ["The staged root remains ignored and `.marketflow` remains untracked in both worktrees."]),
        ("Authority Boundaries", ["No retry, retry candidate, integration success, provider/data/model action, acceptance, runtime, or broker authority was created."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Only a separately approved retry chain may act on this readiness result."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Validation Failure Remediation Results Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
    output_dir: str | Path,
    *,
    repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    source_evidence_root_path: str | Path | None = None,
    git_snapshot: dict | None = None,
    evidence_snapshot: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        repo_root=repo_root,
        integration_worktree_path=integration_worktree_path,
        source_evidence_root_path=source_evidence_root_path,
        git_snapshot=git_snapshot,
        evidence_snapshot=evidence_snapshot,
    )
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError(
            "results-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "sha256": hashlib.sha256(payload).hexdigest(),
        **validation,
    }
