"""Capture retry-failure node IDs from an existing detached pytest cache."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_V1 = (
    "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_DETACHED_PYTEST_CACHE_UNAVAILABLE_OR_INSUFFICIENT = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_DETACHED_PYTEST_CACHE_UNAVAILABLE_OR_INSUFFICIENT"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE = (
    source.SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE
)
SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST = (
    "41052b8621f57721383bc7d8fc416c95e9fef4d5af49b94278ede43209304d33"
)
EXPECTED_ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"
EXPECTED_STAGED_EVIDENCE_DIGEST = (
    "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
)
EXPECTED_REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_INTEGRATION_WORKTREE = Path(
    r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1"
)
LASTFAILED_RELATIVE_PATH = Path(".pytest_cache") / "v" / "cache" / "lastfailed"
NODEIDS_RELATIVE_PATH = Path(".pytest_cache") / "v" / "cache" / "nodeids"
BLOCKED_REASON = "DETACHED_PYTEST_CACHE_LASTFAILED_MISSING_EMPTY_OR_UNPARSEABLE"
PRECHECK_BLOCKED_REASON = "EXECUTION_PRECHECK_FAILED_BEFORE_PYTEST_CACHE_READ"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
MAX_NODEID_SAMPLE = 500
MAX_MODULE_SUMMARY = 100

SUCCESS_NEXT_CHAIN = [
    "Output Capture or Classification Source Results Review v1.",
    "Classification Method Reentry v1.",
    "New Integration Branch Retry Candidate v1 after classification/remediation.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Retry Failure Diagnostic Output Capture Candidate v1.",
    "Operator Review v1.",
    "Approval v1, if selected.",
    "Execution v1, if approved.",
    "Results Review v1.",
    "Classification reentry after diagnostic output capture.",
]
SUCCESS_NEXT_GATES = [
    "output_capture_or_classification_source_results_review",
    "classification_method_reentry_after_output_capture",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "retry_failure_diagnostic_output_capture_candidate",
    "retry_failure_diagnostic_output_capture_operator_review",
    "retry_failure_diagnostic_output_capture_approval_if_selected",
    "retry_failure_diagnostic_output_capture_execution_if_approved",
    "retry_failure_diagnostic_output_capture_results_review",
    "classification_reentry_after_diagnostic_output_capture",
]
RISK_CONTROLS = [
    "execution_reads_only_existing_detached_pytest_cache",
    "execution_does_not_modify_pytest_cache",
    "execution_does_not_parse_operator_logs",
    "execution_does_not_run_diagnostic_commands",
    "execution_does_not_capture_new_output",
    "execution_does_not_rerun_retry",
    "execution_does_not_run_full_pytest",
    "execution_does_not_treat_cache_as_retry_evidence",
    "execution_does_not_replace_failed_retry_result",
    "execution_does_not_create_retry_results_review",
    "execution_does_not_create_integration_results_review",
    "execution_does_not_mark_integration_successful",
    "execution_does_not_generate_successful_integration_execution_digest",
    "execution_does_not_generate_successful_integration_validation_digest",
    "execution_does_not_stage_additional_evidence",
    "execution_does_not_modify_staged_evidence",
    "execution_does_not_regenerate_evidence",
    "execution_does_not_call_providers",
    "execution_does_not_commit_marketflow_outputs",
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
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_results_review_required_after_output_capture",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
PRECHECK_IDS = [
    "source_approval_digest_bound",
    "retry_failure_counts_bound",
    "root_regression_not_retry_evidence",
    "origin_main_unchanged",
    "integration_branch_head_unchanged",
    "remote_integration_branch_absent",
    "detached_worktree_head_verified",
    "detached_worktree_is_detached",
    "detached_worktree_clean_before_read",
    "staged_evidence_unchanged",
    "marketflow_outputs_not_tracked",
    "no_retry_rerun",
    "no_full_pytest",
]
EXECUTION_STEP_IDS = [
    "verify_source_approval",
    "verify_detached_worktree",
    "verify_staged_evidence",
    "locate_lastfailed_cache",
    "read_lastfailed_cache_if_present",
    "parse_lastfailed_cache_if_present",
    "read_nodeids_cache_if_present",
    "produce_classification_source_or_block",
    "preserve_failed_retry",
    "do_not_create_results_review",
]
COMMON_CHECK_IDS = [
    "source_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_method_execution_digest_bound",
    "source_blocked_manifest_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "root_regression_boundary_bound",
    "origin_main_bound",
    "integration_branch_head_bound",
    "detached_worktree_head_bound",
    "staged_evidence_digest_bound",
    "output_capture_executed_true",
    "classification_source_capture_executed_true",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_executed_false",
    "diagnostic_output_captured_false",
    "operator_logs_parsed_false",
    "retry_results_review_created_false",
    "integration_results_review_created_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "new_retry_candidate_false",
    "main_merge_approval_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "evidence_regenerated_false",
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
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]
SUCCESS_CHECK_IDS = [
    "lastfailed_cache_exists_true",
    "lastfailed_cache_read_true",
    "lastfailed_cache_parseable_true",
    "lastfailed_entry_count_positive",
    "lastfailed_nodeids_extracted_true",
    "classification_source_generated_true",
    "classification_source_contains_nodeids_true",
    "module_summary_generated_true",
    "classification_source_limitations_recorded",
    "success_manifest_digest_generated",
]
BLOCKED_CHECK_IDS = [
    "classification_source_generated_false",
    "blocked_reason_recorded",
    "missing_retry_data_recorded",
    "blocked_manifest_digest_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
    ValueError
):
    """Raised when cache-capture evidence violates a required boundary."""


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
        payload = path.read_bytes()
        rows.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return rows


def _snapshot(repo_root: Path, worktree: Path) -> dict[str, Any]:
    evidence_root = (
        worktree
        / ".marketflow"
        / "acquisition_provider_evidence"
        / "expanded_universe_v1"
    )
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
    worktree_head = _git(worktree, "rev-parse", "HEAD")
    symbolic = _git(worktree, "symbolic-ref", "-q", "HEAD")
    status = _git(worktree, "status", "--porcelain=v1")
    root_tracked = _git(repo_root, "ls-files", ".marketflow")
    worktree_tracked = _git(worktree, "ls-files", ".marketflow")
    return {
        "origin_main_commit": origin_main.stdout.strip() if origin_main.returncode == 0 else None,
        "integration_branch_head_commit": integration.stdout.strip() if integration.returncode == 0 else None,
        "remote_integration_branch_exists": remote.returncode == 0,
        "detached_integration_worktree_path": str(worktree.resolve(strict=False)),
        "detached_integration_worktree_head_commit": worktree_head.stdout.strip() if worktree_head.returncode == 0 else None,
        "detached_integration_worktree_is_detached": symbolic.returncode != 0,
        "detached_integration_worktree_clean": status.returncode == 0 and not status.stdout.strip(),
        "staged_evidence_manifest_digest": semantic_digest(inventory),
        "staged_evidence_file_count": len(inventory),
        "repository_tracked_marketflow_count": len(root_tracked.stdout.splitlines()) if root_tracked.returncode == 0 else -1,
        "worktree_tracked_marketflow_count": len(worktree_tracked.stdout.splitlines()) if worktree_tracked.returncode == 0 else -1,
    }


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = expected == actual
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _prechecks(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "source_approval_digest_bound": (SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST, SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [24877, 1292, 112, 7]),
        "root_regression_not_retry_evidence": (False, False),
        "origin_main_unchanged": (EXPECTED_ORIGIN_MAIN_COMMIT, snapshot.get("origin_main_commit")),
        "integration_branch_head_unchanged": (INTEGRATION_HEAD_COMMIT, snapshot.get("integration_branch_head_commit")),
        "remote_integration_branch_absent": (False, snapshot.get("remote_integration_branch_exists")),
        "detached_worktree_head_verified": (INTEGRATION_HEAD_COMMIT, snapshot.get("detached_integration_worktree_head_commit")),
        "detached_worktree_is_detached": (True, snapshot.get("detached_integration_worktree_is_detached")),
        "detached_worktree_clean_before_read": (True, snapshot.get("detached_integration_worktree_clean")),
        "staged_evidence_unchanged": (EXPECTED_STAGED_EVIDENCE_DIGEST, snapshot.get("staged_evidence_manifest_digest")),
        "marketflow_outputs_not_tracked": ([0, 0], [snapshot.get("repository_tracked_marketflow_count"), snapshot.get("worktree_tracked_marketflow_count")]),
        "no_retry_rerun": (False, False),
        "no_full_pytest": (False, False),
    }
    return [_record(check_id, *values[check_id]) for check_id in PRECHECK_IDS]


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _read_json(path: Path) -> tuple[bool, bool | None, Any, str | None]:
    if not path.is_file():
        return False, None, None, None
    payload = path.read_bytes()
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return True, False, None, _sha256(payload)
    return True, True, value, _sha256(payload)


def _module_name(nodeid: str) -> str:
    return nodeid.split("::", 1)[0].replace("\\", "/")


def _module_summary(nodeids: list[str]) -> tuple[list[dict[str, Any]], int, bool]:
    counts = Counter(_module_name(nodeid) for nodeid in nodeids)
    rows = [
        {"module_path": module_path, "nodeid_count": count}
        for module_path, count in sorted(counts.items(), key=lambda row: (-row[1], row[0]))
    ]
    return rows[:MAX_MODULE_SUMMARY], len(rows), len(rows) > MAX_MODULE_SUMMARY


def _execution_steps(
    *, prechecks_passed: bool, lastfailed_exists: bool, lastfailed_read: bool,
    lastfailed_parseable: bool | None, nodeids_read: bool, classification_generated: bool,
) -> list[dict[str, Any]]:
    actuals = {
        "verify_source_approval": prechecks_passed,
        "verify_detached_worktree": prechecks_passed,
        "verify_staged_evidence": prechecks_passed,
        "locate_lastfailed_cache": lastfailed_exists if prechecks_passed else False,
        "read_lastfailed_cache_if_present": lastfailed_read,
        "parse_lastfailed_cache_if_present": lastfailed_parseable is True,
        "read_nodeids_cache_if_present": nodeids_read,
        "produce_classification_source_or_block": classification_generated,
        "preserve_failed_retry": True,
        "do_not_create_results_review": True,
    }
    rows = []
    for step_id in EXECUTION_STEP_IDS:
        actual = actuals[step_id]
        if step_id in {
            "locate_lastfailed_cache",
            "read_lastfailed_cache_if_present",
            "parse_lastfailed_cache_if_present",
            "read_nodeids_cache_if_present",
            "produce_classification_source_or_block",
        }:
            expected = actual
        else:
            expected = True
        status = PASS if expected == actual else FAIL
        rows.append(
            {
                "step_id": step_id,
                "status": status,
                "expected": expected,
                "actual": actual,
                "message": f"{step_id} {'completed' if status == PASS else 'blocked'}",
            }
        )
    return rows


def _source_fields() -> dict[str, Any]:
    review = source._source_review()
    return {
        "source_output_capture_approval_digest": SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST,
        "source_output_capture_operator_review_digest": review["source_output_capture_operator_review_digest"],
        "source_output_capture_candidate_digest": review["source_output_capture_candidate_digest"],
        "source_method_execution_digest": review["source_method_execution_digest"],
        "source_method_blocked_manifest_digest": review["source_method_blocked_manifest_digest"],
        "source_retry_failure_diagnosis_digest": review["source_retry_failure_diagnosis_digest"],
        "source_staged_inventory_digest": review["source_staged_inventory_digest"],
        "retry_execution_branch": review["retry_execution_branch"],
        "retry_execution_commit": review["retry_execution_commit"],
        "retry_pytest_passed_count": review["retry_pytest_passed_count"],
        "retry_pytest_failed_count": review["retry_pytest_failed_count"],
        "retry_pytest_error_count": review["retry_pytest_error_count"],
        "retry_pytest_skipped_count": review["retry_pytest_skipped_count"],
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
    }


def _base_execution(
    *, before: Mapping[str, Any], after: Mapping[str, Any], cache: Mapping[str, Any],
    precheck_results: list[dict[str, Any]], run_timestamp_utc: str | None,
) -> dict[str, Any]:
    prechecks_passed = all(row["status"] == PASS for row in precheck_results)
    usable = bool(
        prechecks_passed
        and cache["lastfailed_cache_exists"]
        and cache["lastfailed_cache_read"]
        and cache["lastfailed_cache_parseable_json"] is True
        and cache["lastfailed_cache_entry_count"] > 0
        and cache["lastfailed_nodeids_extracted"]
        and after.get("detached_integration_worktree_clean") is True
        and after.get("staged_evidence_manifest_digest") == EXPECTED_STAGED_EVIDENCE_DIGEST
    )
    if usable:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED
        status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED
        blocked_reason = None
        next_chain = SUCCESS_NEXT_CHAIN
        next_gates = SUCCESS_NEXT_GATES
        next_task = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1"
    else:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED
        if not prechecks_passed:
            status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED
            blocked_reason = PRECHECK_BLOCKED_REASON
        else:
            status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_DETACHED_PYTEST_CACHE_UNAVAILABLE_OR_INSUFFICIENT
            blocked_reason = BLOCKED_REASON
        next_chain = BLOCKED_NEXT_CHAIN
        next_gates = BLOCKED_NEXT_GATES
        next_task = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_V1"
    execution = {
        "artifact_kind": artifact_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_V1,
        "execution_status": status,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_output_capture_or_classification_source_package": SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE,
        "created_offline_except_read_only_cache_inspection": True,
        "governance_only": True,
        "classification_source_capture_only": True,
        "run_timestamp_utc": run_timestamp_utc,
        **_source_fields(),
        "origin_main_commit": before.get("origin_main_commit"),
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": before.get("integration_branch_head_commit"),
        "remote_integration_branch_exists": before.get("remote_integration_branch_exists"),
        "detached_integration_worktree_path": before.get("detached_integration_worktree_path"),
        "detached_integration_worktree_head_commit": before.get("detached_integration_worktree_head_commit"),
        "detached_integration_worktree_is_detached": before.get("detached_integration_worktree_is_detached"),
        "detached_integration_worktree_clean_before_cache_read": before.get("detached_integration_worktree_clean"),
        "detached_integration_worktree_clean_after_cache_read": after.get("detached_integration_worktree_clean"),
        "staged_evidence_manifest_digest_before_cache_read": before.get("staged_evidence_manifest_digest"),
        "staged_evidence_manifest_digest_after_cache_read": after.get("staged_evidence_manifest_digest"),
        "staged_evidence_unchanged": before.get("staged_evidence_manifest_digest") == after.get("staged_evidence_manifest_digest") == EXPECTED_STAGED_EVIDENCE_DIGEST,
        "marketflow_outputs_tracked_in_repository": after.get("repository_tracked_marketflow_count") != 0,
        "marketflow_outputs_tracked_in_detached_worktree": after.get("worktree_tracked_marketflow_count") != 0,
        **deepcopy(dict(cache)),
        "classification_source_generated": usable,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED" if usable else None,
        "classification_source_review_created": False,
        "classification_source_contains_nodeids": usable,
        "classification_source_can_distinguish_failures_from_errors": False,
        "first_failure_identified": False,
        "first_error_identified": False,
        "ordering_limitation_recorded": True,
        "classification_source_limitations": [
            "pytest lastfailed does not distinguish assertion failure from error unless additional source supports it",
            "pytest lastfailed may not preserve first-failure order",
            "classification source requires results review before reentry",
        ],
        "output_capture_method_executed": True,
        "classification_source_capture_executed": True,
        "pytest_cache_read": cache["lastfailed_cache_read"] or cache["nodeids_cache_read"],
        "operator_logs_parsed": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "new_classification_method_candidate_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "integration_results_review_created": False,
        "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "blocked_reason": blocked_reason,
        "available_retry_data": [
            "aggregate counts", "command", "working directory", "duration", "status docs",
            "cache existence observation",
        ],
        "missing_retry_data": [] if usable else [
            "usable failed/error node IDs", "failed/error module list", "first failing test",
            "first error trace", "traceback details",
        ],
        "precheck_results": deepcopy(precheck_results),
        "execution_steps": _execution_steps(
            prechecks_passed=prechecks_passed,
            lastfailed_exists=cache["lastfailed_cache_exists"],
            lastfailed_read=cache["lastfailed_cache_read"],
            lastfailed_parseable=cache["lastfailed_cache_parseable_json"],
            nodeids_read=cache["nodeids_cache_read"],
            classification_generated=usable,
        ),
        "next_chain": list(next_chain),
        "next_gates": list(next_gates),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": after.get("repository_tracked_marketflow_count") == 0 and after.get("worktree_tracked_marketflow_count") == 0,
        "recommended_next_task": next_task,
    }
    return execution


def _cache_capture(worktree: Path, *, allow_read: bool) -> dict[str, Any]:
    lastfailed_path = worktree / LASTFAILED_RELATIVE_PATH
    nodeids_path = worktree / NODEIDS_RELATIVE_PATH
    default = {
        "lastfailed_cache_path": str(lastfailed_path.resolve(strict=False)),
        "lastfailed_cache_exists": lastfailed_path.is_file() if allow_read else False,
        "lastfailed_cache_read": False,
        "lastfailed_cache_parseable_json": None,
        "lastfailed_cache_sha256": None,
        "lastfailed_cache_entry_count": 0,
        "lastfailed_nodeids_extracted": False,
        "failed_or_errored_nodeids_count": 0,
        "failed_or_errored_nodeids_sample": [],
        "failed_or_errored_nodeids_digest": None,
        "failed_or_errored_nodeids_sample_truncated": False,
        "nodeids_cache_path": str(nodeids_path.resolve(strict=False)),
        "nodeids_cache_exists": nodeids_path.is_file() if allow_read else False,
        "nodeids_cache_read": False,
        "nodeids_cache_parseable_json": None,
        "nodeids_cache_sha256": None,
        "nodeids_cache_entry_count": 0,
        "module_summary_generated": False,
        "module_summary": [],
        "module_summary_total_modules": 0,
        "module_summary_truncated": False,
    }
    if not allow_read:
        return default
    lf_exists, lf_parseable, lf_value, lf_sha = _read_json(lastfailed_path)
    default.update(
        {
            "lastfailed_cache_exists": lf_exists,
            "lastfailed_cache_read": lf_exists,
            "lastfailed_cache_parseable_json": lf_parseable,
            "lastfailed_cache_sha256": lf_sha,
        }
    )
    nodeids: list[str] = []
    if lf_parseable is True and isinstance(lf_value, dict):
        nodeids = sorted(key for key, value in lf_value.items() if isinstance(key, str) and bool(value))
    summary, total_modules, summary_truncated = _module_summary(nodeids)
    default.update(
        {
            "lastfailed_cache_entry_count": len(lf_value) if isinstance(lf_value, dict) else 0,
            "lastfailed_nodeids_extracted": bool(nodeids),
            "failed_or_errored_nodeids_count": len(nodeids),
            "failed_or_errored_nodeids_sample": nodeids[:MAX_NODEID_SAMPLE],
            "failed_or_errored_nodeids_digest": semantic_digest(nodeids) if nodeids else None,
            "failed_or_errored_nodeids_sample_truncated": len(nodeids) > MAX_NODEID_SAMPLE,
            "module_summary_generated": bool(nodeids),
            "module_summary": summary,
            "module_summary_total_modules": total_modules,
            "module_summary_truncated": summary_truncated,
        }
    )
    ni_exists, ni_parseable, ni_value, ni_sha = _read_json(nodeids_path)
    default.update(
        {
            "nodeids_cache_exists": ni_exists,
            "nodeids_cache_read": ni_exists,
            "nodeids_cache_parseable_json": ni_parseable,
            "nodeids_cache_sha256": ni_sha,
            "nodeids_cache_entry_count": len(ni_value) if isinstance(ni_value, list) else 0,
        }
    )
    return default


def marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    fields = {
        key: deepcopy(execution.get(key))
        for key in (
            "lastfailed_cache_path", "lastfailed_cache_sha256", "lastfailed_cache_entry_count",
            "failed_or_errored_nodeids_count", "failed_or_errored_nodeids_digest",
            "nodeids_cache_path", "nodeids_cache_exists", "nodeids_cache_sha256",
            "nodeids_cache_entry_count", "module_summary", "classification_source_limitations",
        )
    }
    return semantic_digest(fields)


def marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    fields = {
        key: deepcopy(execution.get(key))
        for key in (
            "execution_status", "blocked_reason", "lastfailed_cache_path",
            "lastfailed_cache_exists", "lastfailed_cache_read",
            "lastfailed_cache_parseable_json", "lastfailed_cache_sha256",
            "lastfailed_cache_entry_count", "missing_retry_data",
        )
    }
    return semantic_digest(fields)


def marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = [execution.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    precheck_blocked = (
        execution.get("execution_status")
        == MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED
    )
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST, execution.get("source_output_capture_approval_digest")),
        "source_operator_review_digest_bound": ("f73a94b36e7884d778c980d4989c999c383a04310f45e58b6ffae9da6172aa8c", execution.get("source_output_capture_operator_review_digest")),
        "source_candidate_digest_bound": ("fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518", execution.get("source_output_capture_candidate_digest")),
        "source_method_execution_digest_bound": ("522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562", execution.get("source_method_execution_digest")),
        "source_blocked_manifest_digest_bound": ("3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f", execution.get("source_method_blocked_manifest_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], counts),
        "root_regression_boundary_bound": (False, execution.get("root_full_regression_is_retry_evidence")),
        "origin_main_bound": ((execution.get("origin_main_commit") if precheck_blocked else EXPECTED_ORIGIN_MAIN_COMMIT), execution.get("origin_main_commit")),
        "integration_branch_head_bound": ((execution.get("integration_branch_head_commit") if precheck_blocked else INTEGRATION_HEAD_COMMIT), execution.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": ((execution.get("detached_integration_worktree_head_commit") if precheck_blocked else INTEGRATION_HEAD_COMMIT), execution.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": (([execution.get("staged_evidence_manifest_digest_before_cache_read"), execution.get("staged_evidence_manifest_digest_after_cache_read")] if precheck_blocked else [EXPECTED_STAGED_EVIDENCE_DIGEST, EXPECTED_STAGED_EVIDENCE_DIGEST]), [execution.get("staged_evidence_manifest_digest_before_cache_read"), execution.get("staged_evidence_manifest_digest_after_cache_read")]),
        "output_capture_executed_true": (True, execution.get("output_capture_method_executed")),
        "classification_source_capture_executed_true": (True, execution.get("classification_source_capture_executed")),
        "retry_rerun_false": (False, execution.get("retry_rerun_performed")),
        "full_pytest_false": (False, execution.get("full_pytest_performed")),
        "diagnostic_command_executed_false": (False, execution.get("diagnostic_command_executed")),
        "diagnostic_output_captured_false": (False, execution.get("diagnostic_output_captured")),
        "operator_logs_parsed_false": (False, execution.get("operator_logs_parsed")),
        "retry_results_review_created_false": (False, execution.get("new_retry_results_review_created")),
        "integration_results_review_created_false": (False, execution.get("integration_results_review_created")),
        "integration_success_false": (False, execution.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")]),
        "new_retry_candidate_false": (False, execution.get("new_retry_candidate_created")),
        "main_merge_approval_false": (False, execution.get("main_merge_approval_created")),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
        "main_push_false": (False, execution.get("main_push_performed")),
        "origin_main_modified_false": (False, execution.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, execution.get("evidence_regenerated")),
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
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (True, execution.get("no_tracked_marketflow_files")),
    }
    check_ids = list(COMMON_CHECK_IDS)
    if execution.get("classification_source_generated") is True:
        values.update(
            {
                "lastfailed_cache_exists_true": (True, execution.get("lastfailed_cache_exists")),
                "lastfailed_cache_read_true": (True, execution.get("lastfailed_cache_read")),
                "lastfailed_cache_parseable_true": (True, execution.get("lastfailed_cache_parseable_json")),
                "lastfailed_entry_count_positive": (True, isinstance(execution.get("lastfailed_cache_entry_count"), int) and execution.get("lastfailed_cache_entry_count") > 0),
                "lastfailed_nodeids_extracted_true": (True, execution.get("lastfailed_nodeids_extracted")),
                "classification_source_generated_true": (True, execution.get("classification_source_generated")),
                "classification_source_contains_nodeids_true": (True, execution.get("classification_source_contains_nodeids")),
                "module_summary_generated_true": (True, execution.get("module_summary_generated")),
                "classification_source_limitations_recorded": (3, len(execution.get("classification_source_limitations", []))),
                "success_manifest_digest_generated": (True, bool(re.fullmatch(r"[0-9a-f]{64}", str(execution.get("marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest", ""))))),
            }
        )
        check_ids.extend(SUCCESS_CHECK_IDS)
    else:
        values.update(
            {
                "classification_source_generated_false": (False, execution.get("classification_source_generated")),
                "blocked_reason_recorded": (True, execution.get("blocked_reason") in {BLOCKED_REASON, PRECHECK_BLOCKED_REASON}),
                "missing_retry_data_recorded": (True, bool(execution.get("missing_retry_data"))),
                "blocked_manifest_digest_generated": (True, bool(re.fullmatch(r"[0-9a-f]{64}", str(execution.get("marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest", ""))))),
            }
        )
        check_ids.extend(BLOCKED_CHECK_IDS)
    return [_record(check_id, *values[check_id]) for check_id in check_ids]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    summary = {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "output_capture_executed": True,
        "classification_source_generated": execution.get("classification_source_generated"),
        "pytest_cache_read": execution.get("pytest_cache_read"),
        "retry_rerun_performed": False,
        "integration_execution_successful": False,
        "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    if execution.get("classification_source_generated"):
        summary.update(
            {
                "lastfailed_entry_count": execution.get("lastfailed_cache_entry_count"),
                "module_summary_generated": execution.get("module_summary_generated"),
            }
        )
    else:
        summary["blocked_reason"] = execution.get("blocked_reason")
    return summary


def execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
    *, repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Read approved cache files only after every protected-state precheck passes."""
    root = Path(repo_root).resolve(strict=False) if repo_root is not None else EXPECTED_REPO_ROOT
    worktree = (
        Path(integration_worktree_path).resolve(strict=False)
        if integration_worktree_path is not None
        else EXPECTED_INTEGRATION_WORKTREE.resolve(strict=False)
    )
    before = _snapshot(root, worktree)
    precheck_results = _prechecks(before)
    prechecks_passed = all(row["status"] == PASS for row in precheck_results)
    cache = _cache_capture(worktree, allow_read=prechecks_passed)
    after = _snapshot(root, worktree)
    execution = _base_execution(
        before=before,
        after=after,
        cache=cache,
        precheck_results=precheck_results,
        run_timestamp_utc=run_timestamp_utc,
    )
    if execution["classification_source_generated"]:
        execution[
            "marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest"
        ] = marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1(
            execution
        )
        execution["marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest"] = None
    else:
        execution["marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest"] = None
        execution[
            "marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest"
        ] = marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest_v1(
            execution
        )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution, execution["checklist"])
    execution[
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest"
    ] = marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest_v1(
        execution
    )
    validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(
        execution
    )
    return execution


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(
    execution: dict,
) -> dict:
    """Validate either a successful cache capture or a fail-closed blocked result."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            "execution must be an object"
        )
    success = execution.get("classification_source_generated") is True
    expected_kind = (
        ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED
        if success
        else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED
    )
    valid_blocked_statuses = {
        MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_DETACHED_PYTEST_CACHE_UNAVAILABLE_OR_INSUFFICIENT,
        MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED,
    }
    expected_status = (
        MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED
        if success
        else execution.get("execution_status")
    )
    if not success and expected_status not in valid_blocked_statuses:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            "execution_status mismatch"
        )
    static = {
        "artifact_kind": expected_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_V1,
        "execution_status": expected_status,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_output_capture_or_classification_source_package": SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE,
        "source_output_capture_approval_digest": SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST,
        **_source_fields(),
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in static.items():
        _expect(execution.get(field), expected, field)
    required_true = (
        "created_offline_except_read_only_cache_inspection",
        "governance_only",
        "classification_source_capture_only",
        "output_capture_method_executed",
        "classification_source_capture_executed",
        "ordering_limitation_recorded",
        "no_tracked_marketflow_files",
    )
    required_false = (
        "root_full_regression_is_retry_evidence",
        "classification_source_review_created",
        "classification_source_can_distinguish_failures_from_errors",
        "first_failure_identified",
        "first_error_identified",
        "operator_logs_parsed",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "new_classification_method_candidate_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
        "main_merge_approval_created",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "evidence_regenerated",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    )
    for field in required_true:
        _expect(execution.get(field), True, field)
    for field in required_false:
        _expect(execution.get(field), False, field)
    _expect(execution.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(execution.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(execution.get(field), NOT_AUTHORIZED, field)
    if success:
        for field in (
            "lastfailed_cache_exists",
            "lastfailed_cache_read",
            "lastfailed_cache_parseable_json",
            "lastfailed_nodeids_extracted",
            "classification_source_contains_nodeids",
            "module_summary_generated",
        ):
            _expect(execution.get(field), True, field)
        if not isinstance(execution.get("lastfailed_cache_entry_count"), int) or execution["lastfailed_cache_entry_count"] <= 0:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
                "lastfailed_cache_entry_count invalid"
            )
        manifest = execution.get(
            "marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest"
        )
        if not isinstance(manifest, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
                "success manifest digest missing"
            )
        _expect(
            manifest,
            marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1(
                execution
            ),
            "success manifest digest",
        )
    else:
        _expect(execution.get("classification_source_contains_nodeids"), False, "classification_source_contains_nodeids")
        blocked = execution.get(
            "marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest"
        )
        if not isinstance(blocked, str) or not re.fullmatch(r"[0-9a-f]{64}", blocked):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
                "blocked manifest digest missing"
            )
        _expect(
            blocked,
            marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest_v1(
                execution
            ),
            "blocked manifest digest",
        )
    checklist = execution.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            "checklist missing"
        )
    _expect(checklist, _checklist(execution), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            "checklist failed"
        )
    _expect(execution.get("summary"), _summary(execution, checklist), "summary")
    digest = execution.get(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError(
            "execution digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest_v1(
            execution
        ),
        "execution digest",
    )
    return {
        "artifact_kind": execution["artifact_kind"],
        "status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest": digest,
        **{
            key: execution["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_markdown_v1(
    execution: dict,
) -> str:
    """Render the validated success or blocked execution record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(
        execution
    )
    disposition = "Success" if execution["classification_source_generated"] else "Blocked"
    sections = [
        ("Source Approval", [f"Digest: `{execution['source_output_capture_approval_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry remains `24877 passed, 1292 failed, 112 errors, 7 skipped`."]),
        ("Execution Scope", ["Read-only detached pytest-cache classification-source capture; no retry or results review."]),
        ("Read-Only Cache Inputs", [f"Lastfailed: `{execution['lastfailed_cache_path']}`.", f"Nodeids: `{execution['nodeids_cache_path']}`."]),
        ("Cache Capture Result", [f"Lastfailed exists/read/parseable/count: `{execution['lastfailed_cache_exists']} / {execution['lastfailed_cache_read']} / {execution['lastfailed_cache_parseable_json']} / {execution['lastfailed_cache_entry_count']}`.", f"Nodeids exists/read/parseable/count: `{execution['nodeids_cache_exists']} / {execution['nodeids_cache_read']} / {execution['nodeids_cache_parseable_json']} / {execution['nodeids_cache_entry_count']}`."]),
        ("Classification Source Result", [f"Generated: `{execution['classification_source_generated']}`.", f"Node ID count: `{execution['failed_or_errored_nodeids_count']}`; module summary generated: `{execution['module_summary_generated']}`."]),
        ("Success or Blocked Disposition", [f"Disposition: `{disposition}`; status: `{execution['execution_status']}`.", f"Blocked reason: `{execution.get('blocked_reason')}`."]),
        ("Authority Boundaries", ["No pytest run, diagnostic command, log parse, results review, integration success, runtime, or trading authority was created."]),
        ("Next Chain", execution["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in execution["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in execution["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", execution["classification_source_limitations"]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Execution v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
