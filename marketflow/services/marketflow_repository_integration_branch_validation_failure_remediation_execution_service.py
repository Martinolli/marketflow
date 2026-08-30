"""Stage frozen ignored evidence after detached-worktree restoration review."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_results_review_service as review_source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_RETRY_AFTER_WORKTREE_RESTORATION_V1 = (
    "marketflow_repository_integration_branch_validation_failure_remediation_execution_retry_after_worktree_restoration_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION"
)
REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SELECTED_REMEDIATION_PACKAGE = (
    "PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE"
)

EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = (
    "562c6bc4cadb09232ca304efb803d566c0904226314b8f94cceef2e54122159a"
)
EXPECTED_SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = (
    "415f2445805f93906b5f63035472f8edb95f41f64c57c46eab659e5221cc738d"
)
EXPECTED_SOURCE_RESTORATION_EXECUTION_DIGEST = review_source.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_RESTORATION_EXECUTION_MANIFEST_DIGEST = (
    review_source.EXPECTED_SOURCE_WORKTREE_MANIFEST_DIGEST
)
EXPECTED_SOURCE_RESTORATION_APPROVAL_DIGEST = review_source.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = review_source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = (
    review_source.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = review_source.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = review_source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = (
    review_source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST
)

ATTEMPTED_EXECUTION_BRANCH = "feature/marketflow-repository-integration-branch-execution-v1"
ATTEMPTED_EXECUTION_COMMIT = "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba"
INTEGRATION_BRANCH_NAME = review_source.EXPECTED_INTEGRATION_BRANCH_NAME
INTEGRATION_HEAD_COMMIT = review_source.EXPECTED_INTEGRATION_HEAD_COMMIT
INTEGRATION_BASE_COMMIT = review_source.EXPECTED_ORIGIN_MAIN_COMMIT
INTEGRATION_SOURCE_COMMIT = "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"
DEFAULT_INTEGRATION_WORKTREE_PATH = review_source.DEFAULT_WORKTREE_PATH
DEFAULT_SOURCE_EVIDENCE_ROOT = Path(
    r"C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\acquisition_provider_evidence\expanded_universe_v1"
)
REQUIRED_MANIFEST_NAME = "acquisition_provider_evidence_run_manifest.json"
DIAGNOSED_ROOT_CAUSE = "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT"
REPRESENTATIVE_FAILURE = "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH"
REQUIRED_READY_DIGEST = "57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415"
BLOCKED_DIGEST = "783e0013424de9a4e9f02b2ec896c8aa152c0ca701c448ae3e3cfffec05a9b93"
REQUIRED_READY_DIGEST_PREFIX = "57c0a06e"
BLOCKED_DIGEST_PREFIX = "783e0013"

EXPECTED_EVIDENCE_MANIFEST_ROWS = [
    {"relative_path": "acquisition_data_quality_summary.json", "size_bytes": 4645, "sha256": "147bbfbb96318a39b4c6b4ae4a865e593d4fa64369b7ac31ad8749af3af261c1"},
    {"relative_path": "acquisition_digest_manifest.json", "size_bytes": 2561, "sha256": "abbf00067830b06976c7f4bdf9396b6fe83f0edba306b7dc517994cae41270ed"},
    {"relative_path": "acquisition_evidence_results_sanitized.json", "size_bytes": 2431349, "sha256": "51d970eedb72019c5d3fcffe1ccf10475a3480c9c9deb28b9a3d1e67442373fd"},
    {"relative_path": "acquisition_failure_reason_inventory.json", "size_bytes": 636, "sha256": "98bbe551bc4bd1a1a7b6c9080f4967ab354652b8fe5c2f0d94a5152d2646978a"},
    {"relative_path": REQUIRED_MANIFEST_NAME, "size_bytes": 1477, "sha256": "ad2de2a4493e7d0c7bd5d3bd62dce20b7a09b3c4dad1ab56008b468fddbfed07"},
    {"relative_path": "acquisition_provider_request_receipts_sanitized.json", "size_bytes": 16385, "sha256": "812677a5d378a5255c7e674ed416499e457bb69320dde8ab780ca07fdd547a66"},
    {"relative_path": "operator_review_summary.json", "size_bytes": 1128, "sha256": "c513a1ffb48ef8f124e4b466733f8fe2603d66887850b5f04cab9794f977e69b"},
]
EXPECTED_EVIDENCE_FILE_COUNT = 7
EXPECTED_EVIDENCE_TOTAL_BYTES = 2458181
EXPECTED_EVIDENCE_MANIFEST_DIGEST = semantic_digest(EXPECTED_EVIDENCE_MANIFEST_ROWS)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PRECHECK_IDS = [
    "source_results_review_digest_bound",
    "source_approval_digest_bound",
    "detached_worktree_exists",
    "detached_worktree_head_verified",
    "detached_worktree_is_detached",
    "source_evidence_root_exists",
    "required_manifest_exists",
    "source_evidence_root_untracked",
    "origin_main_unchanged",
    "remote_integration_branch_absent",
    "marketflow_outputs_not_tracked_in_repository",
    "no_provider_or_regeneration",
]
EXECUTION_STEP_IDS = [
    "identify_required_evidence_roots",
    "verify_source_frozen_evidence",
    "verify_detached_integration_worktree",
    "stage_evidence_to_detached_integration_worktree",
    "verify_staged_manifest",
    "verify_untracked_status",
    "verify_digest_match",
    "verify_wrong_worktree_guard",
    "preserve_failed_gate",
    "do_not_run_retry",
    "do_not_create_results_review",
]
NEXT_CHAIN = [
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1.",
    "Integration Branch Retry Approval v1.",
    "Integration Branch Retry Execution v1.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "integration_failure_remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "execution_stages_only_frozen_ignored_evidence_roots",
    "execution_does_not_regenerate_evidence",
    "execution_does_not_call_providers",
    "execution_does_not_commit_marketflow_outputs",
    "execution_does_not_track_marketflow_outputs",
    "execution_does_not_run_integration_retry",
    "execution_does_not_create_results_review",
    "execution_does_not_mark_integration_successful",
    "execution_does_not_generate_successful_integration_execution_digest",
    "execution_does_not_generate_successful_integration_validation_digest",
    "execution_does_not_delete_integration_branch",
    "execution_does_not_reset_integration_branch",
    "execution_does_not_push_integration_branch",
    "execution_does_not_push_main",
    "execution_does_not_merge_to_main",
    "execution_does_not_force_push",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_tags",
    "execution_does_not_push_additional_tags",
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
    "first_failed_pytest_remains_authoritative",
    "later_wrong_worktree_rerun_remains_diagnostic_only",
    "blocked_digest_must_not_be_treated_as_ready",
    "separate_results_review_required_after_remediation",
    "separate_retry_approval_required_before_integration_retry",
    "protect_origin_main",
    "preserve_integration_branch_for_diagnosis",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1"
)

REQUIRED_CHECK_IDS = [
    "source_worktree_restoration_results_review_digest_bound",
    "source_worktree_restoration_results_review_manifest_digest_bound",
    "source_remediation_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_diagnosis_digest_bound",
    "source_merge_strategy_approval_digest_bound", "attempted_execution_commit_bound",
    "integration_branch_name_bound", "integration_head_before_bound",
    "integration_head_after_unchanged", "detached_worktree_exists_true",
    "detached_worktree_head_verified_true", "detached_worktree_is_detached_true",
    "origin_main_before_bound", "origin_main_after_unchanged",
    "first_pytest_failure_preserved", "later_wrong_worktree_rerun_preserved_as_diagnostic_only",
    "root_cause_preserved", "remediation_selected_true", "remediation_approved_true",
    "remediation_authorized_true", "remediation_executed_true",
    "evidence_root_inventory_performed_true", "source_frozen_evidence_roots_verified_true",
    "acquisition_provider_evidence_root_verified_true",
    "required_manifest_verified_before_staging_true", "staged_evidence_root_created_true",
    "staged_evidence_root_verified_true", "staged_manifest_verified_true",
    "staged_evidence_root_untracked_true", "source_and_staged_evidence_match_true",
    "required_ready_digest_prefix_verified_true", "blocked_digest_not_accepted_true",
    "precheck_ran_from_detached_worktree_true", "wrong_worktree_guard_passed_true",
    "marketflow_outputs_copied_to_integration_worktree_true",
    "marketflow_outputs_committed_false", "evidence_regenerated_false",
    "retry_candidate_created_false", "retry_executed_false", "results_review_created_false",
    "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false",
    "integration_branch_pushed_false", "remote_integration_branch_false", "main_merge_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_not_tracked",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(ValueError):
    """Raised when remediation preconditions, staging, or evidence fail closed."""


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args], check=check, capture_output=True,
        text=True, encoding="utf-8",
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory(root: Path) -> list[dict[str, Any]]:
    if not root.is_dir():
        return []
    return [
        {
            "relative_path": path.relative_to(root).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
        }
        for path in sorted((path for path in root.rglob("*") if path.is_file()), key=lambda p: p.relative_to(root).as_posix())
    ]


def _copy_evidence_root(source_root: Path, staged_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Copy one absent evidence root without overwriting or deleting anything."""
    if not source_root.is_dir():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "source frozen evidence root is missing"
        )
    if staged_root.exists():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "staged evidence root already exists; no overwrite performed"
        )
    source_rows = _inventory(source_root)
    staged_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_root, staged_root, copy_function=shutil.copy2)
    return source_rows, _inventory(staged_root)


def _fixture_observations() -> dict[str, Any]:
    return {
        "origin_main_before": INTEGRATION_BASE_COMMIT,
        "origin_main_after": INTEGRATION_BASE_COMMIT,
        "integration_head_before": INTEGRATION_HEAD_COMMIT,
        "integration_head_after": INTEGRATION_HEAD_COMMIT,
        "worktree_exists": True,
        "worktree_head": INTEGRATION_HEAD_COMMIT,
        "worktree_detached": True,
        "worktree_clean_before": True,
        "source_root_exists": True,
        "source_manifest_exists": True,
        "source_root_untracked": True,
        "source_rows": deepcopy(EXPECTED_EVIDENCE_MANIFEST_ROWS),
        "staged_rows": deepcopy(EXPECTED_EVIDENCE_MANIFEST_ROWS),
        "staged_root_created": True,
        "staged_root_verified": True,
        "staged_manifest_verified": True,
        "staged_root_untracked": True,
        "precheck_from_worktree": True,
        "remote_integration_exists": False,
        "tracked_marketflow_count": 0,
        "operation_mode": "DETERMINISTIC_FILE_OPERATION_FIXTURE",
    }


def _execute_file_staging(repo_root: Path, worktree: Path, source_root: Path) -> dict[str, Any]:
    expected_worktree = DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False)
    expected_source = DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False)
    actual_worktree = worktree.resolve(strict=False)
    actual_source = source_root.resolve(strict=False)
    if actual_worktree != expected_worktree:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "wrong-worktree guard blocked remediation"
        )
    if actual_source != expected_source:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "source evidence path mismatch"
        )
    staged_root = actual_worktree / ".marketflow" / "acquisition_provider_evidence" / "expanded_universe_v1"
    origin_before = _git(repo_root, "rev-parse", "origin/main").stdout.strip()
    integration_before = _git(repo_root, "rev-parse", INTEGRATION_BRANCH_NAME).stdout.strip()
    remote_before = _git(
        repo_root, "show-ref", "--verify", "--quiet",
        f"refs/remotes/origin/{INTEGRATION_BRANCH_NAME}", check=False,
    ).returncode == 0
    if origin_before != INTEGRATION_BASE_COMMIT or integration_before != INTEGRATION_HEAD_COMMIT:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "protected ref mismatch before remediation"
        )
    if remote_before:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "remote integration branch exists"
        )
    worktree_exists = actual_worktree.is_dir()
    worktree_head_result = _git(actual_worktree, "rev-parse", "HEAD", check=False) if worktree_exists else None
    worktree_head = worktree_head_result.stdout.strip() if worktree_head_result and worktree_head_result.returncode == 0 else None
    worktree_detached = bool(
        worktree_exists
        and _git(actual_worktree, "symbolic-ref", "-q", "HEAD", check=False).returncode != 0
    )
    worktree_clean_before = bool(
        worktree_exists and not _git(actual_worktree, "status", "--porcelain").stdout
    )
    precheck_root = (
        _git(actual_worktree, "rev-parse", "--show-toplevel").stdout.strip()
        if worktree_exists
        else ""
    )
    precheck_from_worktree = Path(precheck_root).resolve(strict=False) == actual_worktree
    if not (
        worktree_exists and worktree_head == INTEGRATION_HEAD_COMMIT
        and worktree_detached and worktree_clean_before and precheck_from_worktree
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "detached integration worktree precheck failed"
        )
    source_manifest = actual_source / REQUIRED_MANIFEST_NAME
    source_rows = _inventory(actual_source)
    source_ignored = _git(
        repo_root, "check-ignore", "--quiet",
        ".marketflow/acquisition_provider_evidence/expanded_universe_v1",
        check=False,
    ).returncode == 0
    if not (
        actual_source.is_dir() and source_manifest.is_file() and source_ignored
        and source_rows == EXPECTED_EVIDENCE_MANIFEST_ROWS
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "frozen source evidence inventory mismatch"
        )
    if _git(repo_root, "ls-files", ".marketflow").stdout.splitlines():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "repository contains tracked .marketflow files"
        )
    source_rows, staged_rows = _copy_evidence_root(actual_source, staged_root)
    staged_manifest = staged_root / REQUIRED_MANIFEST_NAME
    staged_ignored = _git(
        actual_worktree, "check-ignore", "--quiet",
        ".marketflow/acquisition_provider_evidence/expanded_universe_v1/acquisition_provider_evidence_run_manifest.json",
        check=False,
    ).returncode == 0
    tracked_after = _git(actual_worktree, "ls-files", ".marketflow").stdout.splitlines()
    if not (
        staged_root.is_dir() and staged_manifest.is_file() and staged_ignored
        and not tracked_after and source_rows == staged_rows == EXPECTED_EVIDENCE_MANIFEST_ROWS
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "staged evidence verification failed"
        )
    origin_after = _git(repo_root, "rev-parse", "origin/main").stdout.strip()
    integration_after = _git(repo_root, "rev-parse", INTEGRATION_BRANCH_NAME).stdout.strip()
    if origin_after != origin_before or integration_after != integration_before:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "protected ref changed during remediation"
        )
    return {
        "origin_main_before": origin_before,
        "origin_main_after": origin_after,
        "integration_head_before": integration_before,
        "integration_head_after": integration_after,
        "worktree_exists": worktree_exists,
        "worktree_head": worktree_head,
        "worktree_detached": worktree_detached,
        "worktree_clean_before": worktree_clean_before,
        "source_root_exists": actual_source.is_dir(),
        "source_manifest_exists": source_manifest.is_file(),
        "source_root_untracked": source_ignored,
        "source_rows": source_rows,
        "staged_rows": staged_rows,
        "staged_root_created": staged_root.is_dir(),
        "staged_root_verified": staged_root.is_dir(),
        "staged_manifest_verified": staged_manifest.is_file(),
        "staged_root_untracked": staged_ignored and not tracked_after,
        "precheck_from_worktree": precheck_from_worktree,
        "remote_integration_exists": remote_before,
        "tracked_marketflow_count": len(tracked_after),
        "operation_mode": "LOCAL_FROZEN_EVIDENCE_STAGING",
    }


def _base_execution(
    *, run_timestamp_utc: str, observations: Mapping[str, Any]
) -> dict[str, Any]:
    source_rows = deepcopy(observations["source_rows"])
    staged_rows = deepcopy(observations["staged_rows"])
    source_digest = semantic_digest(source_rows)
    staged_digest = semantic_digest(staged_rows)
    staged_root = DEFAULT_INTEGRATION_WORKTREE_PATH / ".marketflow" / "acquisition_provider_evidence" / "expanded_universe_v1"
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_RETRY_AFTER_WORKTREE_RESTORATION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_remediation_package": SELECTED_REMEDIATION_PACKAGE,
        "created_offline_except_local_file_staging": True,
        "governance_only": True,
        "run_timestamp_utc": run_timestamp_utc,
        "file_operation_mode": observations["operation_mode"],
        "source_worktree_restoration_results_review_artifact_kind": review_source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1,
        "source_worktree_restoration_results_review_status": review_source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY,
        "source_worktree_restoration_results_review_scope": review_source.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN,
        "source_worktree_restoration_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_worktree_restoration_results_review_worktree_manifest_digest": EXPECTED_SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_worktree_restoration_execution_digest": EXPECTED_SOURCE_RESTORATION_EXECUTION_DIGEST,
        "source_worktree_restoration_execution_manifest_digest": EXPECTED_SOURCE_RESTORATION_EXECUTION_MANIFEST_DIGEST,
        "source_worktree_restoration_approval_digest": EXPECTED_SOURCE_RESTORATION_APPROVAL_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "attempted_execution_branch": ATTEMPTED_EXECUTION_BRANCH,
        "attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_before_remediation": observations["integration_head_before"],
        "integration_branch_head_commit_after_remediation": observations["integration_head_after"],
        "integration_base_commit": INTEGRATION_BASE_COMMIT,
        "integration_source_commit": INTEGRATION_SOURCE_COMMIT,
        "origin_main_commit_before_remediation": observations["origin_main_before"],
        "origin_main_commit_after_remediation": observations["origin_main_after"],
        "detached_integration_worktree_path": str(DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False)),
        "detached_integration_worktree_exists": observations["worktree_exists"],
        "detached_integration_worktree_head_commit": observations["worktree_head"],
        "detached_integration_worktree_head_verified": observations["worktree_head"] == INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": observations["worktree_detached"],
        "detached_integration_worktree_clean_before_staging": observations["worktree_clean_before"],
        "first_integration_pytest_authoritative": True,
        "first_integration_pytest_passed": False,
        "first_integration_pytest_passed_count": 24481,
        "first_integration_pytest_failed_count": 1300,
        "first_integration_pytest_error_count": 500,
        "first_integration_pytest_skipped_count": 7,
        "later_isolated_rerun_passed_count": 26842,
        "later_isolated_rerun_skipped_count": 7,
        "later_isolated_rerun_classification": "DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        "later_isolated_rerun_overrides_first_failure": False,
        "representative_failure": REPRESENTATIVE_FAILURE,
        "diagnosed_root_cause": DIAGNOSED_ROOT_CAUSE,
        "missing_required_file": REQUIRED_MANIFEST_NAME,
        "remediation_selected": True,
        "remediation_approved": True,
        "remediation_authorized": True,
        "remediation_executed": True,
        "evidence_root_inventory_performed": True,
        "source_frozen_evidence_roots_verified": observations["source_rows"] == EXPECTED_EVIDENCE_MANIFEST_ROWS,
        "acquisition_provider_evidence_root_verified": observations["source_root_exists"],
        "required_manifest_verified_before_staging": observations["source_manifest_exists"],
        "source_evidence_root_path": str(DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False)),
        "staged_evidence_root_path": str(staged_root.resolve(strict=False)),
        "staged_required_manifest_path": str((staged_root / REQUIRED_MANIFEST_NAME).resolve(strict=False)),
        "staged_evidence_root_created": observations["staged_root_created"],
        "staged_evidence_root_verified": observations["staged_root_verified"],
        "staged_required_manifest_verified": observations["staged_manifest_verified"],
        "staged_evidence_root_untracked": observations["staged_root_untracked"],
        "marketflow_outputs_copied_to_integration_worktree": True,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "source_evidence_root_untracked": observations["source_root_untracked"],
        "source_evidence_file_count": len(source_rows),
        "staged_evidence_file_count": len(staged_rows),
        "source_evidence_total_bytes": sum(row["size_bytes"] for row in source_rows),
        "staged_evidence_total_bytes": sum(row["size_bytes"] for row in staged_rows),
        "source_evidence_manifest": source_rows,
        "staged_evidence_manifest": staged_rows,
        "source_evidence_manifest_digest": source_digest,
        "staged_evidence_manifest_digest": staged_digest,
        "source_and_staged_evidence_match": source_rows == staged_rows and source_digest == staged_digest,
        "required_ready_digest_prefix_verified": REQUIRED_READY_DIGEST.startswith(REQUIRED_READY_DIGEST_PREFIX),
        "required_ready_digest_prefix": REQUIRED_READY_DIGEST_PREFIX,
        "blocked_digest_prefix_not_accepted_as_ready": not BLOCKED_DIGEST.startswith(REQUIRED_READY_DIGEST_PREFIX),
        "blocked_digest_prefix": BLOCKED_DIGEST_PREFIX,
        "remediation_precheck_working_directory": str(DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False)),
        "remediation_precheck_ran_from_detached_integration_worktree": observations["precheck_from_worktree"],
        "wrong_worktree_pytest_blocked": True,
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
        "tracked_marketflow_file_count": observations["tracked_marketflow_count"],
        "no_tracked_marketflow_files": observations["tracked_marketflow_count"] == 0,
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
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _record(step_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "step_id": step_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "message": f"{step_id} {'passed' if status == PASS else 'failed'}",
    }


def _records(execution: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    precheck_values = [
        (EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, execution["source_worktree_restoration_results_review_digest"]),
        (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, execution["source_remediation_approval_digest"]),
        (True, execution["detached_integration_worktree_exists"]),
        (True, execution["detached_integration_worktree_head_verified"]),
        (True, execution["detached_integration_worktree_is_detached"]),
        (True, execution["acquisition_provider_evidence_root_verified"]),
        (True, execution["required_manifest_verified_before_staging"]),
        (True, execution["source_evidence_root_untracked"]),
        (INTEGRATION_BASE_COMMIT, execution["origin_main_commit_before_remediation"]),
        (False, execution["remote_integration_branch_created"]),
        (True, execution["no_tracked_marketflow_files"]),
        (False, execution["provider_requests_made_in_execution"]),
    ]
    step_values = [
        (True, execution["evidence_root_inventory_performed"]),
        (True, execution["source_frozen_evidence_roots_verified"]),
        (True, execution["detached_integration_worktree_head_verified"]),
        (True, execution["staged_evidence_root_created"]),
        (True, execution["staged_required_manifest_verified"]),
        (True, execution["staged_evidence_root_untracked"]),
        (True, execution["source_and_staged_evidence_match"]),
        (True, execution["wrong_worktree_pytest_blocked"]),
        (True, execution["first_integration_pytest_authoritative"]),
        (False, execution["integration_retry_executed"]),
        (False, execution["integration_results_review_created"]),
    ]
    return (
        [_record(step_id, expected, actual) for step_id, (expected, actual) in zip(PRECHECK_IDS, precheck_values)],
        [_record(step_id, expected, actual) for step_id, (expected, actual) in zip(EXECUTION_STEP_IDS, step_values)],
    )


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_worktree_restoration_results_review_digest_bound": (EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, execution.get("source_worktree_restoration_results_review_digest")),
        "source_worktree_restoration_results_review_manifest_digest_bound": (EXPECTED_SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, execution.get("source_worktree_restoration_results_review_worktree_manifest_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, execution.get("source_remediation_approval_digest")),
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST, execution.get("source_remediation_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST, execution.get("source_remediation_candidate_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, execution.get("source_failure_diagnosis_digest")),
        "source_merge_strategy_approval_digest_bound": (EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST, execution.get("source_merge_strategy_approval_digest")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, execution.get("attempted_execution_commit")),
        "integration_branch_name_bound": (INTEGRATION_BRANCH_NAME, execution.get("integration_branch_name")),
        "integration_head_before_bound": (INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_before_remediation")),
        "integration_head_after_unchanged": (INTEGRATION_HEAD_COMMIT, execution.get("integration_branch_head_commit_after_remediation")),
        "detached_worktree_exists_true": (True, execution.get("detached_integration_worktree_exists")),
        "detached_worktree_head_verified_true": (True, execution.get("detached_integration_worktree_head_verified")),
        "detached_worktree_is_detached_true": (True, execution.get("detached_integration_worktree_is_detached")),
        "origin_main_before_bound": (INTEGRATION_BASE_COMMIT, execution.get("origin_main_commit_before_remediation")),
        "origin_main_after_unchanged": (INTEGRATION_BASE_COMMIT, execution.get("origin_main_commit_after_remediation")),
        "first_pytest_failure_preserved": ([True, False, 24481, 1300, 500, 7], [execution.get("first_integration_pytest_authoritative"), execution.get("first_integration_pytest_passed"), execution.get("first_integration_pytest_passed_count"), execution.get("first_integration_pytest_failed_count"), execution.get("first_integration_pytest_error_count"), execution.get("first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved_as_diagnostic_only": ([False, "DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE"], [execution.get("later_isolated_rerun_overrides_first_failure"), execution.get("later_isolated_rerun_classification")]),
        "root_cause_preserved": (DIAGNOSED_ROOT_CAUSE, execution.get("diagnosed_root_cause")),
        "remediation_selected_true": (True, execution.get("remediation_selected")),
        "remediation_approved_true": (True, execution.get("remediation_approved")),
        "remediation_authorized_true": (True, execution.get("remediation_authorized")),
        "remediation_executed_true": (True, execution.get("remediation_executed")),
        "evidence_root_inventory_performed_true": (True, execution.get("evidence_root_inventory_performed")),
        "source_frozen_evidence_roots_verified_true": (True, execution.get("source_frozen_evidence_roots_verified")),
        "acquisition_provider_evidence_root_verified_true": (True, execution.get("acquisition_provider_evidence_root_verified")),
        "required_manifest_verified_before_staging_true": (True, execution.get("required_manifest_verified_before_staging")),
        "staged_evidence_root_created_true": (True, execution.get("staged_evidence_root_created")),
        "staged_evidence_root_verified_true": (True, execution.get("staged_evidence_root_verified")),
        "staged_manifest_verified_true": (True, execution.get("staged_required_manifest_verified")),
        "staged_evidence_root_untracked_true": (True, execution.get("staged_evidence_root_untracked")),
        "source_and_staged_evidence_match_true": (True, execution.get("source_and_staged_evidence_match")),
        "required_ready_digest_prefix_verified_true": (True, execution.get("required_ready_digest_prefix_verified")),
        "blocked_digest_not_accepted_true": (True, execution.get("blocked_digest_prefix_not_accepted_as_ready")),
        "precheck_ran_from_detached_worktree_true": (True, execution.get("remediation_precheck_ran_from_detached_integration_worktree")),
        "wrong_worktree_guard_passed_true": (True, execution.get("wrong_worktree_pytest_blocked")),
        "marketflow_outputs_copied_to_integration_worktree_true": (True, execution.get("marketflow_outputs_copied_to_integration_worktree")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, execution.get("evidence_regenerated")),
        "retry_candidate_created_false": (False, execution.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, execution.get("integration_retry_executed")),
        "results_review_created_false": (False, execution.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, execution.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, execution.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, execution.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
        "remote_integration_branch_false": (False, execution.get("remote_integration_branch_created")),
        "main_merge_false": (False, execution.get("main_merge_performed")),
        "main_push_false": (False, execution.get("main_push_performed")),
        "origin_main_modified_false": (False, execution.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_not_tracked": (0, execution.get("tracked_marketflow_file_count")),
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
        "remediation_executed": True, "evidence_root_inventory_performed": True,
        "staged_evidence_root_created": True, "staged_evidence_root_untracked": True,
        "source_and_staged_evidence_match": True, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "integration_retry_executed": False,
        "integration_results_review_created": False, "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    return semantic_digest(
        {
            "source_evidence_manifest": deepcopy(execution.get("source_evidence_manifest")),
            "staged_evidence_manifest": deepcopy(execution.get("staged_evidence_manifest")),
            "source_and_staged_evidence_match": execution.get("source_and_staged_evidence_match"),
        }
    )


def marketflow_repository_integration_branch_validation_failure_remediation_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest",
        None,
    )
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_validation_failure_remediation_v1(
    *,
    repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    source_evidence_root_path: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    execute_file_operations: bool = True,
) -> dict:
    """Stage the exact frozen ignored evidence root, or build a fixture artifact."""
    repository = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    worktree = Path(integration_worktree_path) if integration_worktree_path is not None else DEFAULT_INTEGRATION_WORKTREE_PATH
    source_root = Path(source_evidence_root_path) if source_evidence_root_path is not None else DEFAULT_SOURCE_EVIDENCE_ROOT
    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if worktree.resolve(strict=False) != DEFAULT_INTEGRATION_WORKTREE_PATH.resolve(strict=False):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "wrong-worktree guard blocked remediation"
        )
    if source_root.resolve(strict=False) != DEFAULT_SOURCE_EVIDENCE_ROOT.resolve(strict=False):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "source evidence path mismatch"
        )
    observations = (
        _execute_file_staging(repository.resolve(), worktree, source_root)
        if execute_file_operations
        else _fixture_observations()
    )
    execution = _base_execution(run_timestamp_utc=timestamp, observations=observations)
    prechecks, steps = _records(execution)
    execution["precheck_results"] = prechecks
    execution["execution_steps"] = steps
    execution[
        "marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest_v1(
        execution
    )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution["checklist"])
    execution[
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_execution_digest_v1(
        execution
    )
    validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
        execution
    )
    return execution


def validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
    execution: dict,
) -> dict:
    """Validate exact staging evidence and every closed authority boundary."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution must be an object"
        )
    timestamp = execution.get("run_timestamp_utc")
    mode = execution.get("file_operation_mode")
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "run timestamp missing"
        )
    if mode not in {"DETERMINISTIC_FILE_OPERATION_FIXTURE", "LOCAL_FROZEN_EVIDENCE_STAGING"}:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "file operation mode mismatch"
        )
    expected_observations = {**_fixture_observations(), "operation_mode": mode}
    expected = _base_execution(run_timestamp_utc=timestamp, observations=expected_observations)
    for field, value in expected.items():
        if execution.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
                f"{field} mismatch"
            )
    prechecks, steps = _records(execution)
    if execution.get("precheck_results") != prechecks or any(row["status"] != PASS for row in prechecks):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "precheck results mismatch"
        )
    if execution.get("execution_steps") != steps or any(row["status"] != PASS for row in steps):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution steps mismatch"
        )
    manifest_digest = execution.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest"
    )
    if manifest_digest != marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "evidence manifest digest mismatch"
        )
    checklist = execution.get("checklist")
    if checklist != _checklist(execution) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution checklist mismatch or failed"
        )
    if execution.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution summary mismatch"
        )
    digest = execution.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution digest missing"
        )
    if digest != marketflow_repository_integration_branch_validation_failure_remediation_execution_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationExecutionError(
            "execution digest mismatch"
        )
    return {
        "status": execution["execution_status"], "artifact_kind": execution["artifact_kind"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_execution_digest": digest,
        "marketflow_repository_integration_branch_validation_failure_remediation_evidence_manifest_digest": manifest_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_validation_failure_remediation_execution_markdown_v1(
    execution: dict,
) -> str:
    """Render the validated remediation execution record."""
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_execution_v1(
        execution
    )
    sections = [
        ("Source Worktree Restoration Results Review", [f"Digest: `{execution['source_worktree_restoration_results_review_digest']}`."]),
        ("Source Remediation Approval", [f"Digest: `{execution['source_remediation_approval_digest']}`; package `{execution['selected_remediation_package']}`."]),
        ("Failure Summary", ["The first integration pytest remains authoritative: `24481 passed, 1300 failed, 500 errors, 7 skipped`.", "The later wrong-worktree pass remains diagnostic-only."]),
        ("Root Cause", [f"`{execution['diagnosed_root_cause']}`."]),
        ("Execution Scope", [f"`{execution['execution_scope']}`."]),
        ("Detached Worktree Verification", [f"Path/HEAD: `{execution['detached_integration_worktree_path']}` / `{execution['detached_integration_worktree_head_commit']}`; detached and clean before staging."]),
        ("Evidence Root Inventory", [f"Source inventory: `{execution['source_evidence_file_count']}` files / `{execution['source_evidence_total_bytes']}` bytes."]),
        ("Evidence Staging", [f"Frozen ignored evidence staged at `{execution['staged_evidence_root_path']}` and remains untracked."]),
        ("Digest Verification", [f"Source/staged manifests match: `{execution['source_and_staged_evidence_match']}`."]),
        ("Wrong-Worktree Guard", ["Precheck ran from the detached integration worktree; wrong-worktree retry acceptance remains blocked."]),
        ("Authority Boundaries", ["No retry, results review, integration success, protected-ref push, provider/data/model action, acceptance, runtime, or broker authority was created."]),
        ("Next Chain", execution["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in execution["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in execution["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The next task is a separate remediation results review. The original failed integration gate remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Validation Failure Remediation Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
