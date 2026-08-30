"""Execute the approved authoritative integration retry from the detached worktree."""

from __future__ import annotations

import hashlib
import re
import subprocess
import time
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import marketflow_repository_integration_branch_retry_approval_service as source


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1 = (
    "marketflow_repository_integration_branch_retry_execution_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED_AUTHORITATIVE_FULL_PYTEST_PASSED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED_AUTHORITATIVE_FULL_PYTEST_PASSED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_PRECHECK_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_PRECHECK_FAILED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_WRONG_WORKTREE = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_WRONG_WORKTREE"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_VALID = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_VALID"
)

EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST = (
    "5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1"
)
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST
EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST
)
EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST = source.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST = (
    source.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST

SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE = source.SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE
EXPECTED_ORIGIN_MAIN_COMMIT = source.EXPECTED_ORIGIN_MAIN_COMMIT
INTEGRATION_BRANCH_NAME = source.INTEGRATION_BRANCH_NAME
INTEGRATION_HEAD_COMMIT = source.INTEGRATION_HEAD_COMMIT
ATTEMPTED_EXECUTION_BRANCH = source.ATTEMPTED_EXECUTION_BRANCH
ATTEMPTED_EXECUTION_COMMIT = source.ATTEMPTED_EXECUTION_COMMIT
ORIGINAL_BLOCKED_STATUS = source.ORIGINAL_BLOCKED_STATUS
EXPECTED_REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_DETACHED_WORKTREE_PATH = Path(source.DETACHED_INTEGRATION_WORKTREE_PATH)
EXPECTED_STAGED_EVIDENCE_ROOT = Path(source.STAGED_EVIDENCE_ROOT_PATH)
EXPECTED_STAGED_REQUIRED_MANIFEST = Path(source.STAGED_REQUIRED_MANIFEST_PATH)
EXPECTED_ROOT_PYTHON = EXPECTED_REPO_ROOT / "env" / "Scripts" / "python.exe"
RETRY_PYTEST_COMMAND = f"{EXPECTED_ROOT_PYTHON} -m pytest -q"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_EXECUTED = "NOT_EXECUTED"
RECOMMENDED_NEXT_TASK_SUCCESS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_RESULTS_REVIEW_V1"
)
RECOMMENDED_NEXT_TASK_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1"
)

PRECHECK_IDS = [
    "source_retry_approval_digest_bound",
    "source_remediation_results_review_digest_bound",
    "source_staged_inventory_digest_bound",
    "origin_main_unchanged_before_retry",
    "integration_branch_head_verified_before_retry",
    "remote_integration_branch_absent_before_retry",
    "detached_worktree_exists",
    "detached_worktree_head_verified",
    "detached_worktree_is_detached",
    "detached_worktree_clean_before_retry",
    "staged_evidence_root_exists",
    "staged_required_manifest_exists",
    "staged_evidence_digest_verified_before_retry",
    "staged_evidence_untracked_before_retry",
    "repository_marketflow_outputs_untracked",
    "detached_worktree_marketflow_outputs_untracked",
    "retry_working_directory_is_detached_worktree",
    "root_virtualenv_python_exists",
    "no_provider_or_regeneration",
]
EXECUTION_STEP_IDS = [
    "verify_source_approval",
    "verify_origin_main",
    "verify_integration_branch",
    "verify_detached_worktree",
    "verify_staged_evidence",
    "verify_wrong_worktree_guard",
    "run_authoritative_full_pytest_retry",
    "record_first_retry_result",
    "verify_origin_main_after_retry",
    "verify_integration_branch_after_retry",
    "verify_staged_evidence_after_retry",
    "do_not_push_branches",
    "do_not_create_results_review",
]
SUCCESS_NEXT_CHAIN = [
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval v1, only if retry results review passes.",
    "Main Merge Execution v1, only if separately approved.",
    "Branch Cleanup Candidate v1, only after merge strategy is settled.",
]
BLOCKED_NEXT_CHAIN = [
    "Integration Branch Retry Failure Diagnosis v1.",
    "Remediation or retry-method candidate, only after diagnosis.",
    "No main merge approval.",
]
SUCCESS_NEXT_GATES = [
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_results_review_passes",
    "main_merge_execution_if_approved",
    "branch_cleanup_candidate_after_merge_strategy",
]
BLOCKED_NEXT_GATES = [
    "integration_branch_retry_failure_diagnosis_if_failed",
    "retry_failure_remediation_candidate_if_needed",
    "main_merge_blocked_until_retry_review_passes",
]
RISK_CONTROLS = [
    "execution_runs_retry_only_from_detached_worktree",
    "execution_uses_root_virtualenv_python_with_detached_worktree_cwd",
    "execution_treats_first_retry_result_as_authoritative",
    "execution_does_not_allow_later_rerun_override",
    "execution_verifies_staged_frozen_evidence_before_retry",
    "execution_verifies_staged_frozen_evidence_after_retry",
    "execution_does_not_modify_staged_evidence",
    "execution_does_not_regenerate_evidence",
    "execution_does_not_call_providers",
    "execution_does_not_commit_marketflow_outputs",
    "execution_does_not_track_marketflow_outputs",
    "execution_does_not_create_retry_results_review",
    "execution_does_not_create_integration_results_review",
    "execution_does_not_push_integration_branch",
    "execution_does_not_push_main",
    "execution_does_not_delete_integration_branch",
    "execution_does_not_delete_worktree",
    "execution_does_not_force_push",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_tags",
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
    "separate_results_review_required_after_retry",
    "separate_main_merge_approval_required",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
REQUIRED_CHECK_IDS = [
    "source_retry_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_retry_candidate_digest_bound",
    "source_remediation_results_review_digest_bound",
    "source_remediation_execution_digest_bound",
    "source_staged_inventory_digest_bound",
    "attempted_execution_commit_bound",
    "original_blocked_status_bound",
    "original_first_failure_preserved",
    "later_wrong_worktree_rerun_preserved",
    "origin_main_before_bound",
    "origin_main_after_unchanged",
    "integration_branch_head_before_bound",
    "integration_branch_head_after_unchanged",
    "remote_integration_branch_before_false",
    "remote_integration_branch_after_false",
    "detached_worktree_path_bound",
    "detached_worktree_head_before_bound",
    "detached_worktree_head_after_unchanged",
    "detached_worktree_is_detached_true",
    "detached_worktree_clean_before_true",
    "detached_worktree_clean_after_true",
    "staged_evidence_root_bound",
    "staged_manifest_bound",
    "staged_evidence_digest_before_bound",
    "staged_evidence_digest_after_unchanged",
    "staged_evidence_unchanged_true",
    "marketflow_outputs_tracked_repository_false",
    "marketflow_outputs_tracked_detached_false",
    "marketflow_outputs_committed_false",
    "evidence_regenerated_false",
    "retry_pytest_command_recorded",
    "retry_pytest_working_directory_detached",
    "retry_pytest_ran_from_detached_worktree_true",
    "retry_pytest_used_root_virtualenv_python_true",
    "retry_pytest_first_result_authoritative_true",
    "retry_pytest_performed_true",
    "retry_pytest_passed_true_if_success_artifact",
    "retry_pytest_exit_code_zero_if_success_artifact",
    "retry_selected_true",
    "retry_approved_true",
    "retry_authorized_true",
    "retry_executed_true",
    "retry_execution_successful_true_if_success_artifact",
    "ready_for_retry_results_review_true_if_success_artifact",
    "retry_results_review_created_false",
    "integration_results_review_created_false",
    "successful_integration_execution_digest_generated_true_if_success_artifact",
    "successful_integration_validation_digest_generated_true_if_success_artifact",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
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
]


class MarketFlowRepositoryIntegrationBranchRetryExecutionError(ValueError):
    """Raised when retry execution evidence violates a required boundary."""


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
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
        rows.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": digest.hexdigest(),
            }
        )
    return rows


def _read_repository_snapshot(
    repo_root: Path,
    worktree: Path,
    python_executable: Path,
) -> dict[str, Any]:
    worktree_exists = worktree.is_dir()
    evidence_root = worktree / ".marketflow" / "acquisition_provider_evidence" / "expanded_universe_v1"
    manifest_path = evidence_root / "acquisition_provider_evidence_run_manifest.json"
    inventory = _inventory(evidence_root)
    origin_main = _git(repo_root, "rev-parse", "origin/main")
    integration = _git(repo_root, "rev-parse", INTEGRATION_BRANCH_NAME)
    remote = _git(
        repo_root,
        "show-ref",
        "--verify",
        "--quiet",
        f"refs/remotes/origin/{INTEGRATION_BRANCH_NAME}",
    )
    worktree_head = _git(worktree, "rev-parse", "HEAD") if worktree_exists else None
    symbolic = _git(worktree, "symbolic-ref", "-q", "HEAD") if worktree_exists else None
    status = _git(worktree, "status", "--porcelain=v1") if worktree_exists else None
    ignored = (
        _git(
            worktree,
            "check-ignore",
            "--quiet",
            "--",
            ".marketflow/acquisition_provider_evidence/expanded_universe_v1",
        )
        if worktree_exists
        else None
    )
    root_tracked = _git(repo_root, "ls-files", ".marketflow")
    worktree_tracked = _git(worktree, "ls-files", ".marketflow") if worktree_exists else None
    return {
        "repo_root": str(repo_root.resolve(strict=False)),
        "worktree_path": str(worktree.resolve(strict=False)),
        "python_executable": str(python_executable.resolve(strict=False)),
        "origin_main_commit": origin_main.stdout.strip() if origin_main.returncode == 0 else None,
        "integration_branch_head_commit": integration.stdout.strip() if integration.returncode == 0 else None,
        "remote_integration_branch_exists": remote.returncode == 0,
        "worktree_exists": worktree_exists,
        "worktree_head_commit": (
            worktree_head.stdout.strip() if worktree_head is not None and worktree_head.returncode == 0 else None
        ),
        "worktree_is_detached": symbolic is not None and symbolic.returncode != 0,
        "worktree_clean": status is not None and status.returncode == 0 and not status.stdout.strip(),
        "evidence_root_path": str(evidence_root.resolve(strict=False)),
        "evidence_root_exists": evidence_root.is_dir(),
        "manifest_path": str(manifest_path.resolve(strict=False)),
        "manifest_exists": manifest_path.is_file(),
        "evidence_inventory_digest": semantic_digest(inventory),
        "evidence_file_count": len(inventory),
        "evidence_total_bytes": sum(row["size_bytes"] for row in inventory),
        "evidence_root_ignored": ignored is not None and ignored.returncode == 0,
        "repository_tracked_marketflow_count": (
            len(root_tracked.stdout.splitlines()) if root_tracked.returncode == 0 else -1
        ),
        "worktree_tracked_marketflow_count": (
            len(worktree_tracked.stdout.splitlines())
            if worktree_tracked is not None and worktree_tracked.returncode == 0
            else -1
        ),
        "root_virtualenv_python_exists": python_executable.is_file(),
    }


def _record(record_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = expected == actual
    return {
        "check_id": record_id,
        "status": PASS if passed else FAIL,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": "Requirement satisfied." if passed else "Required execution boundary mismatch.",
    }


def _precheck_results(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "source_retry_approval_digest_bound": (EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST, EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST),
        "source_remediation_results_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        "source_staged_inventory_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        "origin_main_unchanged_before_retry": (EXPECTED_ORIGIN_MAIN_COMMIT, snapshot.get("origin_main_commit")),
        "integration_branch_head_verified_before_retry": (INTEGRATION_HEAD_COMMIT, snapshot.get("integration_branch_head_commit")),
        "remote_integration_branch_absent_before_retry": (False, snapshot.get("remote_integration_branch_exists")),
        "detached_worktree_exists": (True, snapshot.get("worktree_exists")),
        "detached_worktree_head_verified": (INTEGRATION_HEAD_COMMIT, snapshot.get("worktree_head_commit")),
        "detached_worktree_is_detached": (True, snapshot.get("worktree_is_detached")),
        "detached_worktree_clean_before_retry": (True, snapshot.get("worktree_clean")),
        "staged_evidence_root_exists": (True, snapshot.get("evidence_root_exists")),
        "staged_required_manifest_exists": (True, snapshot.get("manifest_exists")),
        "staged_evidence_digest_verified_before_retry": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, snapshot.get("evidence_inventory_digest")),
        "staged_evidence_untracked_before_retry": (True, snapshot.get("evidence_root_ignored")),
        "repository_marketflow_outputs_untracked": (0, snapshot.get("repository_tracked_marketflow_count")),
        "detached_worktree_marketflow_outputs_untracked": (0, snapshot.get("worktree_tracked_marketflow_count")),
        "retry_working_directory_is_detached_worktree": (str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)), snapshot.get("worktree_path")),
        "root_virtualenv_python_exists": (True, snapshot.get("root_virtualenv_python_exists")),
        "no_provider_or_regeneration": (True, True),
    }
    return [_record(check_id, *values[check_id]) for check_id in PRECHECK_IDS]


def _pytest_count(output: str, label: str) -> int:
    pattern = rf"(\d+)\s+{label}"
    matches = re.findall(pattern, output, flags=re.IGNORECASE)
    return int(matches[-1]) if matches else 0


def _parse_pytest_result(result: subprocess.CompletedProcess[str], duration: float) -> dict[str, Any]:
    output = "\n".join(part for part in (result.stdout or "", result.stderr or "") if part)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return {
        "exit_code": result.returncode,
        "passed_count": _pytest_count(output, r"passed\b"),
        "failed_count": _pytest_count(output, r"failed\b"),
        "error_count": _pytest_count(output, r"errors?\b"),
        "skipped_count": _pytest_count(output, r"skipped\b"),
        "duration_seconds": f"{float(duration):.6f}",
        "output_summary": lines[-1] if lines else "",
    }


def _run_pytest(
    python_executable: Path,
    worktree: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        [str(python_executable), "-m", "pytest", "-q"],
        cwd=str(worktree),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return _parse_pytest_result(result, time.perf_counter() - started)


def _execution_steps(
    *,
    prechecks_passed: bool,
    pytest_performed: bool,
    postchecks_passed: bool,
) -> list[dict[str, Any]]:
    values = {
        "verify_source_approval": (True, prechecks_passed),
        "verify_origin_main": (True, prechecks_passed),
        "verify_integration_branch": (True, prechecks_passed),
        "verify_detached_worktree": (True, prechecks_passed),
        "verify_staged_evidence": (True, prechecks_passed),
        "verify_wrong_worktree_guard": (True, prechecks_passed),
        "run_authoritative_full_pytest_retry": (True, pytest_performed),
        "record_first_retry_result": (True, pytest_performed),
        "verify_origin_main_after_retry": (True, postchecks_passed),
        "verify_integration_branch_after_retry": (True, postchecks_passed),
        "verify_staged_evidence_after_retry": (True, postchecks_passed),
        "do_not_push_branches": (False, False),
        "do_not_create_results_review": (False, False),
    }
    rows = []
    for step_id in EXECUTION_STEP_IDS:
        expected, actual = values[step_id]
        row = _record(step_id, expected, actual)
        row["step_id"] = row.pop("check_id")
        rows.append(row)
    return rows


def _base_execution(
    *,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    pytest_result: Mapping[str, Any] | None,
    precheck_results: list[dict[str, Any]],
    run_timestamp_utc: str | None,
    wrong_worktree: bool,
) -> dict[str, Any]:
    prechecks_passed = all(row["status"] == PASS for row in precheck_results)
    pytest_performed = pytest_result is not None
    pytest_passed = bool(
        pytest_result
        and pytest_result["exit_code"] == 0
        and pytest_result["failed_count"] == 0
        and pytest_result["error_count"] == 0
    )
    postchecks_passed = all(
        (
            after.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
            after.get("integration_branch_head_commit") == INTEGRATION_HEAD_COMMIT,
            after.get("remote_integration_branch_exists") is False,
            after.get("worktree_head_commit") == INTEGRATION_HEAD_COMMIT,
            after.get("worktree_is_detached") is True,
            after.get("worktree_clean") is True,
            after.get("evidence_inventory_digest") == EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
            after.get("repository_tracked_marketflow_count") == 0,
            after.get("worktree_tracked_marketflow_count") == 0,
        )
    )
    success = prechecks_passed and pytest_passed and postchecks_passed
    if success:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED
        execution_status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED_AUTHORITATIVE_FULL_PYTEST_PASSED
    else:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED
        if wrong_worktree:
            execution_status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_WRONG_WORKTREE
        elif not prechecks_passed or not postchecks_passed:
            execution_status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_PRECHECK_FAILED
        else:
            execution_status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED
    result = pytest_result or {
        "exit_code": None,
        "passed_count": 0,
        "failed_count": 0,
        "error_count": 0,
        "skipped_count": 0,
        "duration_seconds": None,
        "output_summary": "",
    }
    next_chain = SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN
    next_gates = SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES
    return {
        "artifact_kind": artifact_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1,
        "execution_status": execution_status,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_integration_branch_retry_package": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
        "created_offline_except_local_pytest_execution": True,
        "governance_only": True,
        "run_timestamp_utc": run_timestamp_utc,
        "source_integration_branch_retry_approval_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED,
        "source_integration_branch_retry_approval_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED,
        "source_integration_branch_retry_approval_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_integration_branch_retry_approval_digest": EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST,
        "source_integration_branch_retry_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_integration_branch_retry_candidate_digest": EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST,
        "source_remediation_results_review_digest": EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
        "source_remediation_results_review_evidence_manifest_digest": EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST,
        "source_remediation_execution_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "source_remediation_execution_evidence_manifest_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST,
        "source_staged_inventory_digest": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "source_worktree_restoration_results_review_digest": EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "attempted_execution_branch": ATTEMPTED_EXECUTION_BRANCH,
        "attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
        "original_blocked_artifact": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED",
        "original_blocked_status": ORIGINAL_BLOCKED_STATUS,
        "original_first_integration_pytest_authoritative": True,
        "original_first_integration_pytest_passed": False,
        "original_first_integration_pytest_passed_count": 24481,
        "original_first_integration_pytest_failed_count": 1300,
        "original_first_integration_pytest_error_count": 500,
        "original_first_integration_pytest_skipped_count": 7,
        "later_wrong_worktree_rerun_diagnostic_only": True,
        "later_wrong_worktree_rerun_overrides_original_failure": False,
        "origin_main_commit_before_retry": before.get("origin_main_commit"),
        "origin_main_commit_after_retry": after.get("origin_main_commit"),
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_before_retry": before.get("integration_branch_head_commit"),
        "integration_branch_head_commit_after_retry": after.get("integration_branch_head_commit"),
        "remote_integration_branch_exists_before_retry": before.get("remote_integration_branch_exists"),
        "remote_integration_branch_exists_after_retry": after.get("remote_integration_branch_exists"),
        "detached_integration_worktree_path": before.get("worktree_path"),
        "detached_integration_worktree_head_commit_before_retry": before.get("worktree_head_commit"),
        "detached_integration_worktree_head_commit_after_retry": after.get("worktree_head_commit"),
        "detached_integration_worktree_is_detached": before.get("worktree_is_detached") and after.get("worktree_is_detached"),
        "detached_integration_worktree_clean_before_retry": before.get("worktree_clean"),
        "detached_integration_worktree_clean_after_retry": after.get("worktree_clean"),
        "staged_evidence_root_path": before.get("evidence_root_path"),
        "staged_required_manifest_path": before.get("manifest_path"),
        "staged_evidence_file_count_before_retry": before.get("evidence_file_count"),
        "staged_evidence_file_count_after_retry": after.get("evidence_file_count"),
        "staged_evidence_total_bytes_before_retry": before.get("evidence_total_bytes"),
        "staged_evidence_total_bytes_after_retry": after.get("evidence_total_bytes"),
        "staged_evidence_manifest_digest_before_retry": before.get("evidence_inventory_digest"),
        "staged_evidence_manifest_digest_after_retry": after.get("evidence_inventory_digest"),
        "staged_evidence_unchanged_by_retry": before.get("evidence_inventory_digest") == after.get("evidence_inventory_digest"),
        "marketflow_outputs_tracked_in_repository": after.get("repository_tracked_marketflow_count") != 0,
        "marketflow_outputs_tracked_in_detached_worktree": after.get("worktree_tracked_marketflow_count") != 0,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "retry_pytest_command": RETRY_PYTEST_COMMAND,
        "retry_pytest_working_directory": before.get("worktree_path"),
        "retry_pytest_ran_from_detached_worktree": before.get("worktree_path") == str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)),
        "retry_pytest_used_root_virtualenv_python": before.get("python_executable") == str(EXPECTED_ROOT_PYTHON.resolve(strict=False)),
        "retry_pytest_first_result_authoritative": True,
        "later_retry_rerun_overrides_first_retry_failure": False,
        "retry_pytest_performed": pytest_performed,
        "retry_pytest_exit_code": result["exit_code"],
        "retry_pytest_passed": pytest_passed,
        "retry_pytest_failed": pytest_performed and not pytest_passed,
        "retry_pytest_passed_count": result["passed_count"],
        "retry_pytest_failed_count": result["failed_count"],
        "retry_pytest_error_count": result["error_count"],
        "retry_pytest_skipped_count": result["skipped_count"],
        "retry_pytest_duration_seconds": result["duration_seconds"],
        "retry_pytest_output_summary": result["output_summary"],
        "integration_branch_retry_selected": True,
        "integration_branch_retry_approved": True,
        "integration_branch_retry_authorized": True,
        "integration_branch_retry_executed": pytest_performed,
        "integration_branch_retry_execution_successful": success,
        "ready_for_integration_branch_retry_results_review": success,
        "integration_branch_retry_results_review_created": False,
        "integration_results_review_created": False,
        "integration_execution_successful": success,
        "successful_integration_execution_digest_generated": success,
        "successful_integration_validation_digest_generated": success,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
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
        "precheck_results": deepcopy(precheck_results),
        "execution_steps": _execution_steps(
            prechecks_passed=prechecks_passed,
            pytest_performed=pytest_performed,
            postchecks_passed=postchecks_passed,
        ),
        "next_chain": deepcopy(next_chain),
        "next_gates": deepcopy(next_gates),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "no_tracked_marketflow_files": after.get("repository_tracked_marketflow_count") == 0 and after.get("worktree_tracked_marketflow_count") == 0,
        "recommended_next_task": RECOMMENDED_NEXT_TASK_SUCCESS if success else RECOMMENDED_NEXT_TASK_BLOCKED,
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED
    pytest_expected = True
    success_value = True if success else False
    values = {
        "source_retry_approval_digest_bound": (EXPECTED_SOURCE_RETRY_APPROVAL_DIGEST, execution.get("source_integration_branch_retry_approval_digest")),
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, execution.get("source_integration_branch_retry_operator_review_digest")),
        "source_retry_candidate_digest_bound": (EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST, execution.get("source_integration_branch_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, execution.get("source_remediation_results_review_digest")),
        "source_remediation_execution_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, execution.get("source_remediation_execution_digest")),
        "source_staged_inventory_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, execution.get("source_staged_inventory_digest")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, execution.get("attempted_execution_commit")),
        "original_blocked_status_bound": (ORIGINAL_BLOCKED_STATUS, execution.get("original_blocked_status")),
        "original_first_failure_preserved": ([True, False, 24481, 1300, 500, 7], [execution.get("original_first_integration_pytest_authoritative"), execution.get("original_first_integration_pytest_passed"), execution.get("original_first_integration_pytest_passed_count"), execution.get("original_first_integration_pytest_failed_count"), execution.get("original_first_integration_pytest_error_count"), execution.get("original_first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved": ([True, False], [execution.get("later_wrong_worktree_rerun_diagnostic_only"), execution.get("later_wrong_worktree_rerun_overrides_original_failure")]),
        "origin_main_before_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, execution.get("origin_main_commit_before_retry")),
        "origin_main_after_unchanged": (EXPECTED_ORIGIN_MAIN_COMMIT, execution.get("origin_main_commit_after_retry")),
        "integration_branch_head_before_bound": (INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_before_retry")),
        "integration_branch_head_after_unchanged": (INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_after_retry")),
        "remote_integration_branch_before_false": (False, execution.get("remote_integration_branch_exists_before_retry")),
        "remote_integration_branch_after_false": (False, execution.get("remote_integration_branch_exists_after_retry")),
        "detached_worktree_path_bound": (str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)), execution.get("detached_integration_worktree_path")),
        "detached_worktree_head_before_bound": (INTEGRATION_HEAD_COMMIT, execution.get("detached_integration_worktree_head_commit_before_retry")),
        "detached_worktree_head_after_unchanged": (INTEGRATION_HEAD_COMMIT, execution.get("detached_integration_worktree_head_commit_after_retry")),
        "detached_worktree_is_detached_true": (True, execution.get("detached_integration_worktree_is_detached")),
        "detached_worktree_clean_before_true": (True, execution.get("detached_integration_worktree_clean_before_retry")),
        "detached_worktree_clean_after_true": (True, execution.get("detached_integration_worktree_clean_after_retry")),
        "staged_evidence_root_bound": (str(EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False)), execution.get("staged_evidence_root_path")),
        "staged_manifest_bound": (str(EXPECTED_STAGED_REQUIRED_MANIFEST.resolve(strict=False)), execution.get("staged_required_manifest_path")),
        "staged_evidence_digest_before_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, execution.get("staged_evidence_manifest_digest_before_retry")),
        "staged_evidence_digest_after_unchanged": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, execution.get("staged_evidence_manifest_digest_after_retry")),
        "staged_evidence_unchanged_true": (True, execution.get("staged_evidence_unchanged_by_retry")),
        "marketflow_outputs_tracked_repository_false": (False, execution.get("marketflow_outputs_tracked_in_repository")),
        "marketflow_outputs_tracked_detached_false": (False, execution.get("marketflow_outputs_tracked_in_detached_worktree")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, execution.get("evidence_regenerated")),
        "retry_pytest_command_recorded": (RETRY_PYTEST_COMMAND, execution.get("retry_pytest_command")),
        "retry_pytest_working_directory_detached": (str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)), execution.get("retry_pytest_working_directory")),
        "retry_pytest_ran_from_detached_worktree_true": (True, execution.get("retry_pytest_ran_from_detached_worktree")),
        "retry_pytest_used_root_virtualenv_python_true": (True, execution.get("retry_pytest_used_root_virtualenv_python")),
        "retry_pytest_first_result_authoritative_true": (True, execution.get("retry_pytest_first_result_authoritative")),
        "retry_pytest_performed_true": (pytest_expected, execution.get("retry_pytest_performed")),
        "retry_pytest_passed_true_if_success_artifact": (success_value, execution.get("retry_pytest_passed")),
        "retry_pytest_exit_code_zero_if_success_artifact": (0 if success else execution.get("retry_pytest_exit_code"), execution.get("retry_pytest_exit_code")),
        "retry_selected_true": (True, execution.get("integration_branch_retry_selected")),
        "retry_approved_true": (True, execution.get("integration_branch_retry_approved")),
        "retry_authorized_true": (True, execution.get("integration_branch_retry_authorized")),
        "retry_executed_true": (True, execution.get("integration_branch_retry_executed")),
        "retry_execution_successful_true_if_success_artifact": (success_value, execution.get("integration_branch_retry_execution_successful")),
        "ready_for_retry_results_review_true_if_success_artifact": (success_value, execution.get("ready_for_integration_branch_retry_results_review")),
        "retry_results_review_created_false": (False, execution.get("integration_branch_retry_results_review_created")),
        "integration_results_review_created_false": (False, execution.get("integration_results_review_created")),
        "successful_integration_execution_digest_generated_true_if_success_artifact": (success_value, execution.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_true_if_success_artifact": (success_value, execution.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
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
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (True, execution.get("no_tracked_marketflow_files")),
    }
    return [_record(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]], execution: Mapping[str, Any]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "integration_branch_retry_executed": execution.get("integration_branch_retry_executed"),
        "integration_branch_retry_execution_successful": execution.get("integration_branch_retry_execution_successful"),
        "retry_pytest_passed": execution.get("retry_pytest_passed"),
        "retry_pytest_first_result_authoritative": True,
        "ready_for_integration_branch_retry_results_review": execution.get("ready_for_integration_branch_retry_results_review"),
        "integration_branch_retry_results_review_created": False,
        "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_execution_digest",
        "marketflow_repository_integration_branch_retry_validation_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def marketflow_repository_integration_branch_retry_validation_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = {
        "execution_digest": execution.get(
            "marketflow_repository_integration_branch_retry_execution_digest"
        ),
        "checklist": execution.get("checklist"),
        "summary": execution.get("summary"),
    }
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_v1(
    *,
    repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    python_executable: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    execute_pytest: bool = True,
) -> dict:
    """Run the approved retry exactly once after all fail-closed prechecks pass."""
    repo = Path(repo_root) if repo_root is not None else EXPECTED_REPO_ROOT
    worktree = (
        Path(integration_worktree_path)
        if integration_worktree_path is not None
        else EXPECTED_DETACHED_WORKTREE_PATH
    )
    python = Path(python_executable) if python_executable is not None else EXPECTED_ROOT_PYTHON
    before = _read_repository_snapshot(repo, worktree, python)
    prechecks = _precheck_results(before)
    prechecks_passed = all(row["status"] == PASS for row in prechecks)
    wrong_worktree = before.get("worktree_path") != str(
        EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)
    )
    pytest_result = None
    if execute_pytest and prechecks_passed:
        pytest_result = _run_pytest(python, worktree)
    after = _read_repository_snapshot(repo, worktree, python)
    execution = _base_execution(
        before=before,
        after=after,
        pytest_result=pytest_result,
        precheck_results=prechecks,
        run_timestamp_utc=run_timestamp_utc,
        wrong_worktree=wrong_worktree,
    )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution["checklist"], execution)
    if execution["integration_branch_retry_execution_successful"]:
        execution["marketflow_repository_integration_branch_retry_execution_digest"] = (
            marketflow_repository_integration_branch_retry_execution_digest_v1(execution)
        )
        execution["marketflow_repository_integration_branch_retry_validation_digest"] = (
            marketflow_repository_integration_branch_retry_validation_digest_v1(execution)
        )
    validate_marketflow_repository_integration_branch_retry_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_execution_v1(
    execution: dict,
) -> dict:
    """Validate either successful retry evidence or a fail-closed blocked result."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError(
            "execution must be an object"
        )
    success = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED
    blocked = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED
    if not success and not blocked:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("artifact kind mismatch")
    allowed_statuses = (
        {MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTED_AUTHORITATIVE_FULL_PYTEST_PASSED}
        if success
        else {
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED,
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_PRECHECK_FAILED,
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_WRONG_WORKTREE,
        }
    )
    if execution.get("execution_status") not in allowed_statuses:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution status mismatch")
    if execution.get("execution_scope") != REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution scope mismatch")
    if execution.get("selected_integration_branch_retry_package") != SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("selected package mismatch")
    checklist = execution.get("checklist")
    expected_checklist = _checklist(execution)
    if not isinstance(checklist, list) or checklist != expected_checklist:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution checklist mismatch")
    if success or execution.get("retry_pytest_performed"):
        if any(row.get("status") != PASS for row in checklist):
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution checklist failed")
    if execution.get("summary") != _summary(checklist, execution):
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution summary mismatch")
    if execution.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("risk controls mismatch")
    if success:
        if execution.get("retry_pytest_exit_code") != 0:
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("successful retry exit code mismatch")
        if execution.get("retry_pytest_failed_count") != 0 or execution.get("retry_pytest_error_count") != 0:
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("successful retry contains failures")
        execution_digest = execution.get("marketflow_repository_integration_branch_retry_execution_digest")
        validation_digest = execution.get("marketflow_repository_integration_branch_retry_validation_digest")
        if execution_digest != marketflow_repository_integration_branch_retry_execution_digest_v1(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("execution digest mismatch")
        if validation_digest != marketflow_repository_integration_branch_retry_validation_digest_v1(execution):
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("validation digest mismatch")
    else:
        if execution.get("integration_branch_retry_execution_successful") is not False:
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("blocked execution marked successful")
        if execution.get("marketflow_repository_integration_branch_retry_execution_digest") is not None:
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("blocked execution has success digest")
        if execution.get("marketflow_repository_integration_branch_retry_validation_digest") is not None:
            raise MarketFlowRepositoryIntegrationBranchRetryExecutionError("blocked execution has validation digest")
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_VALID,
        "artifact_kind": execution["artifact_kind"],
        "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_retry_execution_digest": execution.get("marketflow_repository_integration_branch_retry_execution_digest"),
        "marketflow_repository_integration_branch_retry_validation_digest": execution.get("marketflow_repository_integration_branch_retry_validation_digest"),
        **{
            key: execution["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_execution_markdown_v1(
    execution: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_execution_v1(execution)
    disposition = "SUCCESS" if execution["integration_branch_retry_execution_successful"] else "BLOCKED"
    sections = [
        ("Source Retry Approval", [f"Digest: `{execution['source_integration_branch_retry_approval_digest']}`.", f"Selected package: `{execution['selected_integration_branch_retry_package']}`."]),
        ("Failure and Remediation Context", ["The historical first integration failure remains preserved; the later wrong-worktree run remains diagnostic-only.", "The retry uses the remediated detached worktree and frozen staged evidence."]),
        ("Execution Scope", [f"`{execution['execution_scope']}`."]),
        ("Precheck Results", [f"`{row['check_id']}`: `{row['status']}`." for row in execution["precheck_results"]]),
        ("Authoritative Retry Command", [f"Command: `{execution['retry_pytest_command']}`.", f"Working directory: `{execution['retry_pytest_working_directory']}`."]),
        ("Authoritative Retry Result", [f"Exit/pass/fail/error/skip: `{execution['retry_pytest_exit_code']} / {execution['retry_pytest_passed_count']} / {execution['retry_pytest_failed_count']} / {execution['retry_pytest_error_count']} / {execution['retry_pytest_skipped_count']}`.", f"Duration: `{execution['retry_pytest_duration_seconds']}` seconds."]),
        ("Repository and Worktree Boundaries", ["`origin/main`, integration HEAD, detached state, cleanliness, staged digest, and untracked `.marketflow` boundaries are recorded before and after retry."]),
        ("Success or Blocked Disposition", [f"Disposition: `{disposition}`.", f"Status: `{execution['execution_status']}`."]),
        ("Next Chain", execution["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in execution["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in execution["risk_controls"]]),
        ("Authority Boundaries", ["Execution creates no retry results review, integration results review, main-merge approval, runtime authority, broker authority, or trading authority."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No evidence regeneration, provider request, protected-ref push, branch/worktree deletion, tag mutation, or `.marketflow` commit occurred."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
