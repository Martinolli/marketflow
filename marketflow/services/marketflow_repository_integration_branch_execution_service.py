"""Execute the approved local integration-branch validation in an isolated worktree."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import os
import re
import subprocess
import tempfile
from typing import Any, Iterable, Mapping
from uuid import uuid4

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import marketflow_repository_merge_strategy_approval_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1 = (
    "marketflow_repository_integration_branch_execution_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED"
)
REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME = (
    "REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_VALID = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_VALID"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_BRANCH_EXISTS_OR_PRECHECK_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_BRANCH_EXISTS_OR_PRECHECK_FAILED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED"
)

PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION = (
    source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
)
EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c"
)
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST
EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_service.EXPECTED_ORIGIN_MAIN_COMMIT

INTEGRATION_BRANCH_NAME = source_service.INTEGRATION_BRANCH_NAME
INTEGRATION_BASE = source_service.INTEGRATION_BASE
INTEGRATION_SOURCE_BRANCH = source_service.INTEGRATION_SOURCE_BRANCH
INTEGRATION_SOURCE_COMMIT = source_service.INTEGRATION_SOURCE_COMMIT
INTEGRATION_MERGE_METHOD = "NO_FF_MERGE_COMMIT"
INTEGRATION_MERGE_MESSAGE = "Integrate MarketFlow terminal evidence stack for validation"
APPROVED_FUTURE_EXECUTION_TYPE = "CREATE_TEMPORARY_INTEGRATION_BRANCH_AND_VALIDATE_FULL_STACK_ONLY"
APPROVED_FUTURE_EXECUTION_SCOPE = "INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME"

EXPECTED_TERMINAL_TAGS = [
    "marketflow/expectancy-lab/archive-record-not-ready/v1",
    "marketflow/expectancy-lab/final-archive-not-ready/v1",
    "marketflow/expectancy-lab/operator-selection-option-a/v1",
    "marketflow/expectancy-lab/readiness-not-ready/v1",
]
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "Repository Integration Branch Results Review v1.",
    "Repository Main Merge Approval v1, only if integration branch review passes.",
    "Repository Main Merge Execution v1, only if separately approved.",
    "Repository Branch Cleanup Candidate v1, only after main integration strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
]
NEXT_GATES = [
    "repository_integration_branch_results_review",
    "repository_main_merge_approval_if_integration_passes",
    "repository_main_merge_execution_if_approved",
    "repository_branch_cleanup_candidate_after_merge_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
]
RISK_CONTROLS = [
    "execution_creates_only_approved_integration_branch",
    "execution_integrates_only_approved_source_commit",
    "execution_uses_origin_main_as_base",
    "execution_runs_full_pytest_on_integration_branch",
    "execution_does_not_push_integration_branch", "execution_does_not_push_main",
    "execution_does_not_merge_to_main", "execution_does_not_rebase",
    "execution_does_not_squash_merge", "execution_does_not_cherry_pick",
    "execution_does_not_delete_branches", "execution_does_not_delete_remote_branches",
    "execution_does_not_force_push", "execution_does_not_prune_remotes",
    "execution_does_not_modify_origin_main", "execution_does_not_modify_tags",
    "execution_does_not_push_additional_tags", "execution_does_not_modify_marketflow_outputs",
    "execution_does_not_call_providers", "execution_does_not_acquire_market_data",
    "execution_does_not_regenerate_dataset", "execution_does_not_rerun_merge_strategy_approval",
    "execution_does_not_rerun_merge_strategy_operator_review",
    "execution_does_not_rerun_tag_push_results_review", "execution_does_not_rerun_inventory",
    "execution_does_not_rerun_evidence", "execution_does_not_recompute_metrics",
    "execution_does_not_train_models", "execution_does_not_score_strategy",
    "execution_does_not_generate_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability", "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_broker_execution",
    "separate_results_review_required_after_integration",
    "separate_main_merge_approval_required", "protect_origin_main",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

PRECHECK_IDS = [
    "origin_main_verified", "source_commit_verified",
    "integration_branch_absent_before_execution",
    "remote_integration_branch_absent_before_execution",
    "working_tree_clean_before_execution", "published_terminal_tags_still_present",
]
EXECUTION_STEP_IDS = [
    "create_integration_branch_from_origin_main", "merge_source_commit_no_ff",
    "run_full_pytest_on_integration_branch", "switch_back_to_feature_branch",
    "confirm_origin_main_unchanged", "confirm_no_integration_branch_push",
    "confirm_no_main_push",
]
REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_tag_push_results_review_digest_bound",
    "source_remote_manifest_review_digest_bound", "source_tag_push_execution_digest_bound",
    "source_tag_push_approval_digest_bound", "source_inventory_plan_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_operator_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "records_digest_bound", "origin_main_before_bound", "origin_main_after_unchanged",
    "selected_package_integration_branch_validation", "strategy_selected_true",
    "strategy_approved_true", "strategy_authorized_true", "strategy_executed_true",
    "integration_branch_created_true", "integration_branch_name_matches",
    "integration_base_origin_main", "integration_base_commit_matches",
    "integration_source_commit_matches", "integration_merge_performed_true",
    "integration_branch_pushed_false", "remote_integration_branch_created_false",
    "integration_pytest_performed_true", "integration_pytest_passed_true",
    "integration_validation_completed_true", "ready_for_integration_branch_results_review_true",
    "main_merge_performed_false", "main_push_false", "rebase_performed_false",
    "squash_merge_performed_false", "cherry_pick_performed_false", "branch_delete_false",
    "remote_delete_false", "force_push_false", "remote_prune_false",
    "origin_main_modified_false", "tags_pushed_again_false", "additional_tags_created_false",
    "tags_modified_false", "tags_deleted_false", "cleanup_candidate_created_false",
    "marketflow_outputs_not_tracked", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchExecutionError(RuntimeError):
    """Raised when prechecks, integration, or validation fail closed."""

    def __init__(self, message: str, *, blocked_status: str) -> None:
        super().__init__(message)
        self.artifact_kind = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED
        self.blocked_status = blocked_status


def _run(
    repo_root: Path,
    *args: str,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
    check: bool = True,
) -> str:
    result = subprocess.run(
        ["git", *args], cwd=str(cwd or repo_root), env=dict(env) if env else None,
        text=True, capture_output=True, check=False,
    )
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            f"git {' '.join(args)} failed: {detail}",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    return result.stdout.strip()


def _ref_exists(repo_root: Path, ref: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", ref], cwd=str(repo_root), check=False,
    )
    return result.returncode == 0


def _record(record_id: str, actual: bool, *, noun: str) -> dict[str, Any]:
    return {
        f"{noun}_id": record_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual,
        "message": f"{record_id} passed" if actual else f"{record_id} failed",
    }


def _fixture_snapshot(run_timestamp_utc: str) -> dict[str, Any]:
    return {
        "run_timestamp_utc": run_timestamp_utc,
        "origin_main_before": EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_after": EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head": "1" * 40,
        "integration_merge_commit": "1" * 40,
        "merge_base_origin_main": EXPECTED_ORIGIN_MAIN_COMMIT,
        "merge_base_source": INTEGRATION_SOURCE_COMMIT,
        "diff_stat": "fixture integration diff",
        "diff_name_status": ["A\tfixture/integration-evidence.txt"],
        "diff_name_status_total": 1,
        "pytest_passed_count": 26706,
        "pytest_skipped_count": 7,
        "pytest_duration_seconds": None,
        "pytest_output_summary": "26706 passed, 7 skipped in 0.00s",
        "worktree_path": "FIXTURE_ISOLATED_WORKTREE",
        "worktree_removed_after_validation": True,
        "precheck_results": [_record(row, True, noun="precheck") for row in PRECHECK_IDS],
        "execution_steps": [_record(row, True, noun="step") for row in EXECUTION_STEP_IDS],
    }


def _precheck(repo_root: Path) -> list[dict[str, Any]]:
    origin_main = _run(repo_root, "rev-parse", "origin/main")
    source_commit = _run(repo_root, "rev-parse", INTEGRATION_SOURCE_COMMIT)
    local_absent = not _ref_exists(repo_root, f"refs/heads/{INTEGRATION_BRANCH_NAME}")
    remote_absent = not _ref_exists(repo_root, f"refs/remotes/origin/{INTEGRATION_BRANCH_NAME}")
    tree_clean = not _run(repo_root, "status", "--porcelain")
    tag_refs = _run(repo_root, "for-each-ref", "--format=%(refname:strip=2)", "refs/tags")
    tags = set(tag_refs.splitlines())
    tags_present = set(EXPECTED_TERMINAL_TAGS).issubset(tags)
    values = [
        origin_main == EXPECTED_ORIGIN_MAIN_COMMIT,
        source_commit == INTEGRATION_SOURCE_COMMIT,
        local_absent, remote_absent, tree_clean, tags_present,
    ]
    records = [_record(row, value, noun="precheck") for row, value in zip(PRECHECK_IDS, values)]
    if not all(values):
        failed = [row["precheck_id"] for row in records if row["status"] != PASS]
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            f"integration execution precheck failed: {', '.join(failed)}",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_BRANCH_EXISTS_OR_PRECHECK_FAILED,
        )
    return records


def _run_pytest_in_worktree(repo_root: Path, worktree: Path) -> dict[str, Any]:
    python = repo_root / "env" / "Scripts" / "python.exe"
    if not python.is_file():
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "repository virtualenv python is missing",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED,
        )
    process = subprocess.Popen(
        [str(python), "-m", "pytest", "-q"], cwd=str(worktree),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    output_lines: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
        output_lines.append(line)
    exit_code = process.wait()
    output = "".join(output_lines)
    matches = list(re.finditer(r"(\d+) passed(?:, (\d+) skipped)? in ([\d.]+)s", output))
    if exit_code or not matches:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            f"integration pytest failed with exit code {exit_code}",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED,
        )
    match = matches[-1]
    return {
        "pytest_passed_count": int(match.group(1)),
        "pytest_skipped_count": int(match.group(2) or 0),
        "pytest_duration_seconds": match.group(3),
        "pytest_output_summary": match.group(0),
    }


def _execute_real(repo_root: Path, run_timestamp_utc: str, run_pytest: bool) -> dict[str, Any]:
    if not run_pytest:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "full integration pytest is required",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED,
        )
    prechecks = _precheck(repo_root)
    temp_root = Path(tempfile.gettempdir()).resolve()
    worktree = (temp_root / f"marketflow-integration-validation-{uuid4().hex}").resolve()
    if worktree.parent != temp_root:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "temporary worktree path escaped the system temp directory",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_BRANCH_EXISTS_OR_PRECHECK_FAILED,
        )
    worktree_added = False
    worktree_removed = False
    try:
        _run(
            repo_root, "worktree", "add", "-b", INTEGRATION_BRANCH_NAME,
            str(worktree), "origin/main",
        )
        worktree_added = True
        merge_env = os.environ.copy()
        merge_env.update({
            "GIT_AUTHOR_NAME": "MarketFlow Integration Validation",
            "GIT_AUTHOR_EMAIL": "marketflow-integration@local.invalid",
            "GIT_COMMITTER_NAME": "MarketFlow Integration Validation",
            "GIT_COMMITTER_EMAIL": "marketflow-integration@local.invalid",
            "GIT_AUTHOR_DATE": run_timestamp_utc,
            "GIT_COMMITTER_DATE": run_timestamp_utc,
        })
        _run(
            repo_root, "merge", "--no-ff", INTEGRATION_SOURCE_COMMIT,
            "-m", INTEGRATION_MERGE_MESSAGE, cwd=worktree, env=merge_env,
        )
        head = _run(repo_root, "rev-parse", "HEAD", cwd=worktree)
        parents = _run(repo_root, "show", "-s", "--format=%P", "HEAD", cwd=worktree).split()
        if len(parents) != 2 or parents != [EXPECTED_ORIGIN_MAIN_COMMIT, INTEGRATION_SOURCE_COMMIT]:
            raise MarketFlowRepositoryIntegrationBranchExecutionError(
                "integration merge commit parents do not match approved base and source",
                blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
            )
        pytest_result = _run_pytest_in_worktree(repo_root, worktree)
        diff_lines = _run(
            repo_root, "diff", "--name-status", "origin/main...HEAD", cwd=worktree,
        ).splitlines()
        snapshot = {
            "run_timestamp_utc": run_timestamp_utc,
            "origin_main_before": EXPECTED_ORIGIN_MAIN_COMMIT,
            "origin_main_after": _run(repo_root, "rev-parse", "origin/main"),
            "integration_branch_head": head,
            "integration_merge_commit": head,
            "merge_base_origin_main": _run(repo_root, "merge-base", "origin/main", "HEAD", cwd=worktree),
            "merge_base_source": _run(repo_root, "merge-base", INTEGRATION_SOURCE_COMMIT, "HEAD", cwd=worktree),
            "diff_stat": _run(repo_root, "diff", "--stat", "origin/main...HEAD", cwd=worktree),
            "diff_name_status": diff_lines[:200],
            "diff_name_status_total": len(diff_lines),
            **pytest_result,
            "worktree_path": str(worktree),
            "worktree_removed_after_validation": True,
            "precheck_results": prechecks,
            "execution_steps": [],
        }
    except MarketFlowRepositoryIntegrationBranchExecutionError:
        if worktree_added and (worktree / ".git").exists():
            subprocess.run(["git", "merge", "--abort"], cwd=str(worktree), check=False, capture_output=True)
        raise
    finally:
        if worktree_added:
            result = subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree)],
                cwd=str(repo_root), text=True, capture_output=True, check=False,
            )
            worktree_removed = result.returncode == 0
    if not worktree_removed:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "isolated integration worktree could not be removed",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    origin_unchanged = _run(repo_root, "rev-parse", "origin/main") == EXPECTED_ORIGIN_MAIN_COMMIT
    branch_local = _run(repo_root, "rev-parse", INTEGRATION_BRANCH_NAME) == snapshot["integration_branch_head"]
    branch_remote_absent = not _ref_exists(repo_root, f"refs/remotes/origin/{INTEGRATION_BRANCH_NAME}")
    feature_worktree_unchanged = not _run(repo_root, "status", "--porcelain")
    step_values = [
        branch_local, True, True, feature_worktree_unchanged,
        origin_unchanged, branch_remote_absent, origin_unchanged,
    ]
    snapshot["execution_steps"] = [
        _record(row, value, noun="step") for row, value in zip(EXECUTION_STEP_IDS, step_values)
    ]
    if not all(step_values):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "post-execution validation failed",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    return snapshot


def _base_execution(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME,
        "selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "created_offline_except_local_git_integration_branch": True, "governance_only": True,
        "run_timestamp_utc": snapshot["run_timestamp_utc"],
        "source_merge_strategy_approval_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED,
        "source_merge_strategy_approval_status": source_service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED,
        "source_merge_strategy_approval_scope": source_service.REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_merge_strategy_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_merge_strategy_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tag_push_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest": EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_remote_manifest_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest": EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "origin_main_commit_before_execution": snapshot["origin_main_before"],
        "origin_main_commit_after_execution": snapshot["origin_main_after"],
        "integration_branch_name": INTEGRATION_BRANCH_NAME, "integration_base": INTEGRATION_BASE,
        "integration_base_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_source_branch": INTEGRATION_SOURCE_BRANCH,
        "integration_source_commit": INTEGRATION_SOURCE_COMMIT,
        "integration_merge_method": INTEGRATION_MERGE_METHOD,
        "integration_branch_created": True, "integration_merge_performed": True,
        "integration_branch_pushed": False, "remote_integration_branch_created": False,
        "integration_branch_head_commit": snapshot["integration_branch_head"],
        "integration_merge_commit": snapshot["integration_merge_commit"],
        "integration_merge_base_with_origin_main": snapshot["merge_base_origin_main"],
        "integration_merge_base_with_source_commit": snapshot["merge_base_source"],
        "integration_diff_stat_against_origin_main": snapshot["diff_stat"],
        "integration_diff_name_status_against_origin_main": list(snapshot["diff_name_status"]),
        "integration_diff_name_status_total": snapshot["diff_name_status_total"],
        "integration_pytest_performed": True,
        "integration_pytest_command": "env\\Scripts\\python.exe -m pytest -q",
        "integration_pytest_passed": True, "integration_pytest_exit_code": 0,
        "integration_pytest_passed_count": snapshot["pytest_passed_count"],
        "integration_pytest_skipped_count": snapshot["pytest_skipped_count"],
        "integration_pytest_duration_seconds": snapshot["pytest_duration_seconds"],
        "integration_pytest_output_summary": snapshot["pytest_output_summary"],
        "integration_validation_completed": True,
        "isolated_worktree_path": snapshot["worktree_path"],
        "isolated_worktree_removed_after_validation": snapshot["worktree_removed_after_validation"],
        "precheck_results": deepcopy(snapshot["precheck_results"]),
        "execution_steps": deepcopy(snapshot["execution_steps"]),
        "repository_merge_strategy_selected": True, "repository_merge_strategy_approved": True,
        "repository_merge_strategy_authorized": True, "repository_merge_strategy_executed": True,
        "repository_integration_branch_created": True,
        "ready_for_repository_integration_branch_results_review": True,
        "main_merge_performed": False, "main_push_performed": False,
        "git_main_push_performed": False, "origin_main_modified_by_this_task": False,
        "repository_cleanup_candidate_created": False, "repository_cleanup_executed": False,
        "git_rebase_performed": False, "git_squash_merge_performed": False,
        "git_cherry_pick_performed": False, "git_branch_delete_performed": False,
        "git_remote_delete_performed": False, "git_force_push_performed": False,
        "git_remote_prune_performed": False, "repository_tags_pushed_again": False,
        "additional_tag_push_performed": False, "additional_tags_created": False,
        "tags_modified": False, "tags_deleted": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RESULTS_REVIEW_V1",
    }


def _check_values(execution: Mapping[str, Any]) -> dict[str, bool]:
    return {
        "source_approval_digest_bound": execution.get("source_merge_strategy_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": execution.get("source_merge_strategy_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": execution.get("source_merge_strategy_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tag_push_results_review_digest_bound": execution.get("source_tag_push_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest_bound": execution.get("source_remote_manifest_review_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest_bound": execution.get("source_tag_push_execution_digest") == EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_approval_digest_bound": execution.get("source_tag_push_approval_digest") == EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_inventory_plan_digest_bound": execution.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": execution.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": execution.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": execution.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": execution.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": execution.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": execution.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest_bound": execution.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": execution.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": execution.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_before_bound": execution.get("origin_main_commit_before_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_after_unchanged": execution.get("origin_main_commit_after_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "selected_package_integration_branch_validation": execution.get("selected_merge_strategy_package") == PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "strategy_selected_true": execution.get("repository_merge_strategy_selected") is True,
        "strategy_approved_true": execution.get("repository_merge_strategy_approved") is True,
        "strategy_authorized_true": execution.get("repository_merge_strategy_authorized") is True,
        "strategy_executed_true": execution.get("repository_merge_strategy_executed") is True,
        "integration_branch_created_true": execution.get("repository_integration_branch_created") is True and execution.get("integration_branch_created") is True,
        "integration_branch_name_matches": execution.get("integration_branch_name") == INTEGRATION_BRANCH_NAME,
        "integration_base_origin_main": execution.get("integration_base") == INTEGRATION_BASE,
        "integration_base_commit_matches": execution.get("integration_base_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_source_commit_matches": execution.get("integration_source_commit") == INTEGRATION_SOURCE_COMMIT,
        "integration_merge_performed_true": execution.get("integration_merge_performed") is True,
        "integration_branch_pushed_false": execution.get("integration_branch_pushed") is False,
        "remote_integration_branch_created_false": execution.get("remote_integration_branch_created") is False,
        "integration_pytest_performed_true": execution.get("integration_pytest_performed") is True,
        "integration_pytest_passed_true": execution.get("integration_pytest_passed") is True and execution.get("integration_pytest_exit_code") == 0 and execution.get("integration_pytest_passed_count", 0) > 0,
        "integration_validation_completed_true": execution.get("integration_validation_completed") is True,
        "ready_for_integration_branch_results_review_true": execution.get("ready_for_repository_integration_branch_results_review") is True,
        "main_merge_performed_false": execution.get("main_merge_performed") is False,
        "main_push_false": execution.get("main_push_performed") is False and execution.get("git_main_push_performed") is False,
        "rebase_performed_false": execution.get("git_rebase_performed") is False,
        "squash_merge_performed_false": execution.get("git_squash_merge_performed") is False,
        "cherry_pick_performed_false": execution.get("git_cherry_pick_performed") is False,
        "branch_delete_false": execution.get("git_branch_delete_performed") is False,
        "remote_delete_false": execution.get("git_remote_delete_performed") is False,
        "force_push_false": execution.get("git_force_push_performed") is False,
        "remote_prune_false": execution.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": execution.get("origin_main_modified_by_this_task") is False,
        "tags_pushed_again_false": execution.get("repository_tags_pushed_again") is False and execution.get("additional_tag_push_performed") is False,
        "additional_tags_created_false": execution.get("additional_tags_created") is False,
        "tags_modified_false": execution.get("tags_modified") is False,
        "tags_deleted_false": execution.get("tags_deleted") is False,
        "cleanup_candidate_created_false": execution.get("repository_cleanup_candidate_created") is False,
        "marketflow_outputs_not_tracked": execution.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": execution.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": execution.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_generation_false": execution.get("dataset_generation_performed_in_execution") is False,
        "metric_recomputation_false": execution.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": execution.get("model_training_performed") is False,
        "strategy_scoring_false": execution.get("strategy_scoring_performed") is False,
        "recommendations_false": execution.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": execution.get("predictive_usefulness") == NOT_ACCEPTED and execution.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": execution.get("profitability") == NOT_ACCEPTED and execution.get("profitability_accepted") is False,
        "runtime_not_authorized": execution.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": execution.get("broker_execution") == NOT_AUTHORIZED,
        "next_chain_defined": execution.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": execution.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": execution.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": execution.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL, "expected": True,
        "actual": actual, "severity": BLOCKER,
        "message": "integration execution evidence matches" if actual else "integration execution evidence mismatch",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(execution)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_merge_strategy_executed": True,
        "repository_integration_branch_created": True, "integration_branch_created": True,
        "integration_merge_performed": True, "integration_pytest_performed": True,
        "integration_pytest_passed": True,
        "ready_for_repository_integration_branch_results_review": True,
        "integration_branch_pushed": False, "main_merge_performed": False,
        "main_pushed": False, "cleanup_candidate_created": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RESULTS_REVIEW_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_execution_validation_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    """Digest the integration-specific validation record."""
    fields = (
        "origin_main_commit_before_execution", "origin_main_commit_after_execution",
        "integration_branch_name", "integration_base_commit", "integration_source_commit",
        "integration_branch_head_commit", "integration_merge_commit",
        "integration_merge_base_with_origin_main", "integration_merge_base_with_source_commit",
        "integration_diff_stat_against_origin_main",
        "integration_diff_name_status_against_origin_main", "integration_diff_name_status_total",
        "integration_pytest_command", "integration_pytest_passed_count",
        "integration_pytest_skipped_count", "integration_pytest_duration_seconds",
        "integration_pytest_output_summary", "precheck_results", "execution_steps",
    )
    return semantic_digest({field: deepcopy(execution.get(field)) for field in fields})


def marketflow_repository_integration_branch_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the execution artifact."""
    payload = deepcopy(dict(execution))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_execution_digest", None)
    payload.pop("marketflow_repository_integration_branch_execution_validation_digest", None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_v1(
    *,
    repo_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    execute_git_operations: bool = True,
    run_pytest: bool = True,
) -> dict:
    """Create and validate the approved local integration branch, or build a fixture artifact."""
    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "run_timestamp_utc is required",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_BRANCH_EXISTS_OR_PRECHECK_FAILED,
        )
    root = Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[2]
    snapshot = (
        _execute_real(root, timestamp, run_pytest)
        if execute_git_operations
        else _fixture_snapshot(timestamp)
    )
    execution = _base_execution(snapshot)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution["checklist"])
    execution["marketflow_repository_integration_branch_execution_validation_digest"] = (
        marketflow_repository_integration_branch_execution_validation_digest_v1(execution)
    )
    execution["marketflow_repository_integration_branch_execution_digest"] = (
        marketflow_repository_integration_branch_execution_digest_v1(execution)
    )
    validate_marketflow_repository_integration_branch_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_execution_v1(execution: dict) -> dict:
    """Validate source bindings, actual integration evidence, and closed downstream gates."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution must be an object",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    static_expected = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME,
        "selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
    }
    for field, expected in static_expected.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchExecutionError(
                f"{field} mismatch",
                blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
            )
    sha_fields = (
        "integration_branch_head_commit", "integration_merge_commit",
        "integration_merge_base_with_origin_main", "integration_merge_base_with_source_commit",
    )
    if any(not re.fullmatch(r"[0-9a-f]{40}", str(execution.get(field, ""))) for field in sha_fields):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "integration commit evidence is invalid",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if execution.get("integration_branch_head_commit") != execution.get("integration_merge_commit"):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "integration head and merge commit mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if execution.get("integration_merge_base_with_origin_main") != EXPECTED_ORIGIN_MAIN_COMMIT:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "origin/main merge base mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if execution.get("integration_merge_base_with_source_commit") != INTEGRATION_SOURCE_COMMIT:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "source merge base mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if [row.get("precheck_id") for row in execution.get("precheck_results", [])] != PRECHECK_IDS:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "precheck records mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if [row.get("step_id") for row in execution.get("execution_steps", [])] != EXECUTION_STEP_IDS:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution step records mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if any(row.get("status") != PASS for row in execution["precheck_results"] + execution["execution_steps"]):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "precheck or execution step failed",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    checklist = execution.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(execution):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution checklist mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution checklist failed",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if execution.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution summary mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    validation_digest = execution.get("marketflow_repository_integration_branch_execution_validation_digest")
    if not isinstance(validation_digest, str) or len(validation_digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "validation digest missing",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if validation_digest != marketflow_repository_integration_branch_execution_validation_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "validation digest mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    digest = execution.get("marketflow_repository_integration_branch_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution digest missing",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    if digest != marketflow_repository_integration_branch_execution_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchExecutionError(
            "execution digest mismatch",
            blocked_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_MERGE_CONFLICT_OR_VALIDATION_FAILED,
        )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_VALID,
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "marketflow_repository_integration_branch_execution_digest": digest,
        "marketflow_repository_integration_branch_execution_validation_digest": validation_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_execution_markdown_v1(execution: dict) -> str:
    """Render a sanitized Markdown view of the validated integration execution."""
    validation = validate_marketflow_repository_integration_branch_execution_v1(execution)
    sections = [
        ("Title", ["MarketFlow Repository Integration Branch Execution v1"]),
        ("MarketFlow Repository Integration Branch Execution v1", [f"Artifact/status: `{execution['artifact_kind']}` / `{execution['execution_status']}`.", f"Execution digest: `{validation['marketflow_repository_integration_branch_execution_digest']}`.", f"Validation digest: `{validation['marketflow_repository_integration_branch_execution_validation_digest']}`."]),
        ("Source Merge Strategy Approval", [f"Source digest: `{execution['source_merge_strategy_approval_digest']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(execution['source_evidence'])}."]),
        ("Repository Context", [f"Origin main before/after: `{execution['origin_main_commit_before_execution']}` / `{execution['origin_main_commit_after_execution']}`."]),
        ("Execution Scope", [execution["execution_scope"]]),
        ("Integration Branch Creation", [f"`{execution['integration_branch_name']}` at `{execution['integration_branch_head_commit']}`; pushed: {execution['integration_branch_pushed']}."]),
        ("Integration Merge", [f"Method: `{execution['integration_merge_method']}`; source: `{execution['integration_source_commit']}`; merge commit: `{execution['integration_merge_commit']}`."]),
        ("Integration Pytest Validation", [execution["integration_pytest_output_summary"]]),
        ("Origin/Main Protection", ["Origin/main is unchanged; no main merge or main push occurred."]),
        ("Next Chain", list(execution["next_chain"])), ("Next Gates", list(execution["next_gates"])),
        ("Risk Controls", list(execution["risk_controls"])),
        ("Authority Boundaries", ["Execution validates only the local integration branch. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{execution['summary']['passed_checks']} / {execution['summary']['total_checks']} checks pass; {execution['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No integration-branch push, main merge/push, rebase, squash, cherry-pick, deletion, force push, tag mutation, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
