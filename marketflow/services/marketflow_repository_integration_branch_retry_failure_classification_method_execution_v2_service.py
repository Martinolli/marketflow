"""Execute the approved cache-supported module-level classification method v2."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_CACHE_SOURCE_MISMATCH_OR_BOUNDARY_FAILURE = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_CACHE_SOURCE_MISMATCH_OR_BOUNDARY_FAILURE"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_PRECHECK_FAILED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_PRECHECK_FAILED"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE = source.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE
SOURCE_APPROVAL_V2_DIGEST = "a29132ad740c0e617fb438c154c4b5fed756f15bceed40ff132334d1c5e58412"
EXPECTED_LASTFAILED_SHA256 = "24fb8cf5ce237ae6c952c29c37acaea7d22205ca885659a196f0bc27c4b1f1b1"
EXPECTED_NODEIDS_SHA256 = "9d69140fd12f57de3c14060139bc4d50a3096c29b0262c5e482af5b78ea0206d"
EXPECTED_LASTFAILED_COUNT = 1404
EXPECTED_NODEIDS_COUNT = 26288
EXPECTED_MODULE_COUNT = 29
EXPECTED_LARGEST_MODULE_COUNTS = [136, 131, 122, 112, 111]
EXPECTED_ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
EXPECTED_INTEGRATION_HEAD = "220fbc220365fce9cae13ab4853cddff118c0187"
EXPECTED_STAGED_EVIDENCE_DIGEST = "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
DEFAULT_INTEGRATION_WORKTREE = Path(
    r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1"
)
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_FAILURE_DIAGNOSIS"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SUCCESS_NEXT_CHAIN = [
    "Classification Method Results Review v2.",
    "Remediation or Method Candidate after v2 review, if needed.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Classification Method Execution v2 Failure Diagnosis.",
    "Candidate or remediation path after diagnosis.",
    "No retry or main merge.",
]
SUCCESS_NEXT_GATES = [
    "classification_method_results_review_v2", "remediation_or_method_candidate_after_v2_review",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "classification_method_execution_v2_failure_diagnosis",
    "classification_method_execution_v2_remediation_candidate_if_needed",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "execution_v2_reads_cache_read_only", "execution_v2_does_not_modify_cache",
    "execution_v2_does_not_commit_pytest_cache", "execution_v2_does_not_commit_marketflow_outputs",
    "execution_v2_does_not_run_retry", "execution_v2_does_not_run_full_pytest",
    "execution_v2_does_not_run_diagnostic_commands", "execution_v2_does_not_claim_failure_error_separation",
    "execution_v2_does_not_claim_first_failure", "execution_v2_does_not_claim_first_error",
    "execution_v2_does_not_claim_traceback_root_cause", "execution_v2_does_not_use_cache_as_retry_success_evidence",
    "execution_v2_does_not_create_new_retry_candidate", "execution_v2_does_not_create_retry_results_review",
    "execution_v2_does_not_create_integration_results_review", "execution_v2_does_not_mark_integration_successful",
    "execution_v2_does_not_generate_successful_integration_digest", "execution_v2_does_not_push_integration_branch",
    "execution_v2_does_not_push_main", "execution_v2_does_not_delete_integration_branch",
    "execution_v2_does_not_delete_worktree", "execution_v2_does_not_force_push",
    "execution_v2_does_not_prune_remotes", "execution_v2_does_not_modify_tags",
    "execution_v2_does_not_modify_staged_evidence", "execution_v2_does_not_regenerate_evidence",
    "execution_v2_does_not_call_providers", "execution_v2_does_not_acquire_market_data",
    "execution_v2_does_not_regenerate_dataset", "execution_v2_does_not_recompute_metrics",
    "execution_v2_does_not_train_models", "execution_v2_does_not_score_strategy",
    "execution_v2_does_not_generate_recommendations", "execution_v2_does_not_accept_predictive_usefulness",
    "execution_v2_does_not_accept_profitability", "execution_v2_does_not_authorize_runtime",
    "execution_v2_does_not_authorize_broker_execution", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_v2_results_review_required",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
PRECHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_v2_digest_bound", "source_reentry_digest_bound",
    "source_results_review_digest_bound", "source_cache_manifest_digest_bound",
    "retry_failure_counts_bound", "origin_main_unchanged", "integration_branch_head_unchanged",
    "detached_worktree_head_verified", "detached_worktree_clean_before_execution",
    "staged_evidence_unchanged", "marketflow_outputs_not_tracked", "pytest_cache_not_tracked",
    "no_retry_rerun", "no_full_pytest",
]
EXECUTION_STEP_IDS = [
    "verify_source_approval", "verify_protected_refs", "verify_detached_worktree",
    "verify_cache_hashes", "parse_lastfailed_cache", "parse_nodeids_cache",
    "build_module_nodeid_grouping", "build_module_summary", "build_limitations_report",
    "build_unsupported_claims_exclusion_report", "preserve_failed_retry_authority",
    "do_not_create_results_review",
]
CHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound", "source_candidate_v2_digest_bound",
    "source_reentry_digest_bound", "source_results_review_digest_bound", "source_cache_manifest_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "cache_hashes_verified",
    "cache_counts_verified", "module_count_29", "largest_module_counts_verified",
    "classification_method_v2_executed_true", "classification_execution_created_true_if_success",
    "classification_execution_performed_true_if_success", "module_level_grouping_generated_true_if_success",
    "module_summary_generated_true_if_success", "failed_or_errored_nodeids_count_1404_if_success",
    "failure_modules_classified_false", "error_modules_classified_false",
    "failure_error_separation_claimed_false", "first_failure_identified_false",
    "first_error_identified_false", "first_order_claim_made_false", "traceback_root_cause_claimed_false",
    "retry_success_claimed_false", "main_merge_readiness_claimed_false",
    "limitations_report_generated_true_if_success", "unsupported_claims_exclusion_report_generated_true_if_success",
    "planned_outputs_generated_true_if_success", "new_retry_candidate_created_false",
    "new_retry_executed_false", "new_retry_results_review_created_false", "main_merge_approval_created_false",
    "retry_rerun_false", "full_pytest_false", "diagnostic_command_false", "diagnostic_output_false",
    "integration_success_false", "successful_integration_digest_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "pytest_cache_committed_false", "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error(ValueError):
    """Raised when execution evidence or authority boundaries are invalid."""


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=False, capture_output=True,
        text=True, encoding="utf-8",
    )


def _inventory(root: Path) -> list[dict[str, Any]]:
    if not root.is_dir():
        return []
    rows = []
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        payload = path.read_bytes()
        rows.append({
            "relative_path": path.relative_to(root).as_posix(),
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    return rows


def _state_snapshot(repo_root: Path, worktree: Path) -> dict[str, Any]:
    evidence_root = worktree / ".marketflow" / "acquisition_provider_evidence" / "expanded_universe_v1"
    origin_main = _git(repo_root, "rev-parse", "origin/main")
    integration = _git(repo_root, "rev-parse", INTEGRATION_BRANCH_NAME)
    remote = _git(repo_root, "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{INTEGRATION_BRANCH_NAME}")
    worktree_head = _git(worktree, "rev-parse", "HEAD")
    status = _git(worktree, "status", "--porcelain=v1")
    root_marketflow = _git(repo_root, "ls-files", ".marketflow")
    worktree_marketflow = _git(worktree, "ls-files", ".marketflow")
    root_pytest = _git(repo_root, "ls-files", ".pytest_cache")
    worktree_pytest = _git(worktree, "ls-files", ".pytest_cache")
    return {
        "origin_main_commit": origin_main.stdout.strip() if origin_main.returncode == 0 else None,
        "integration_branch_head_commit": integration.stdout.strip() if integration.returncode == 0 else None,
        "remote_integration_branch_exists": remote.returncode == 0,
        "detached_integration_worktree_path": str(worktree.resolve(strict=False)),
        "detached_integration_worktree_head_commit": worktree_head.stdout.strip() if worktree_head.returncode == 0 else None,
        "detached_integration_worktree_clean": status.returncode == 0 and not status.stdout.strip(),
        "staged_evidence_manifest_digest": semantic_digest(_inventory(evidence_root)),
        "marketflow_outputs_tracked_in_repository": bool(root_marketflow.stdout.strip()) if root_marketflow.returncode == 0 else True,
        "marketflow_outputs_tracked_in_detached_worktree": bool(worktree_marketflow.stdout.strip()) if worktree_marketflow.returncode == 0 else True,
        "pytest_cache_tracked_in_repository": bool(root_pytest.stdout.strip()) if root_pytest.returncode == 0 else True,
        "pytest_cache_tracked_in_detached_worktree": bool(worktree_pytest.stdout.strip()) if worktree_pytest.returncode == 0 else True,
    }


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _prechecks(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = source._committed_source_fields()
    values = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_V2_DIGEST, SOURCE_APPROVAL_V2_DIGEST),
        "source_operator_review_digest_bound": (source.SOURCE_OPERATOR_REVIEW_DIGEST, fields["source_classification_method_candidate_v2_operator_review_digest"]),
        "source_candidate_v2_digest_bound": (source.source.SOURCE_CANDIDATE_V2_DIGEST, fields["source_classification_method_candidate_v2_digest"]),
        "source_reentry_digest_bound": (source.source.source.SOURCE_REENTRY_DIGEST, fields["source_classification_method_reentry_digest"]),
        "source_results_review_digest_bound": (source.source.source.SOURCE_RESULTS_REVIEW_DIGEST, fields["source_classification_source_results_review_digest"]),
        "source_cache_manifest_digest_bound": (source.source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, fields["source_cache_manifest_review_digest"]),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [fields[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")]),
        "origin_main_unchanged": (EXPECTED_ORIGIN_MAIN_COMMIT, snapshot.get("origin_main_commit")),
        "integration_branch_head_unchanged": (EXPECTED_INTEGRATION_HEAD, snapshot.get("integration_branch_head_commit")),
        "detached_worktree_head_verified": (EXPECTED_INTEGRATION_HEAD, snapshot.get("detached_integration_worktree_head_commit")),
        "detached_worktree_clean_before_execution": (True, snapshot.get("detached_integration_worktree_clean")),
        "staged_evidence_unchanged": (EXPECTED_STAGED_EVIDENCE_DIGEST, snapshot.get("staged_evidence_manifest_digest")),
        "marketflow_outputs_not_tracked": ([False, False], [snapshot.get("marketflow_outputs_tracked_in_repository"), snapshot.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "pytest_cache_not_tracked": ([False, False], [snapshot.get("pytest_cache_tracked_in_repository"), snapshot.get("pytest_cache_tracked_in_detached_worktree")]),
        "no_retry_rerun": (False, False), "no_full_pytest": (False, False),
    }
    return [_record(check_id, *values[check_id]) for check_id in PRECHECK_IDS]


def _read_cache(worktree: Path) -> dict[str, Any]:
    lastfailed_path = worktree / ".pytest_cache" / "v" / "cache" / "lastfailed"
    nodeids_path = worktree / ".pytest_cache" / "v" / "cache" / "nodeids"
    result: dict[str, Any] = {
        "lastfailed_cache_path": str(lastfailed_path.resolve(strict=False)), "lastfailed_cache_read": False,
        "lastfailed_cache_sha256": None, "lastfailed_cache_entry_count": None,
        "lastfailed_cache_parseable": False, "failed_or_errored_nodeids": [],
        "nodeids_cache_path": str(nodeids_path.resolve(strict=False)), "nodeids_cache_read": False,
        "nodeids_cache_sha256": None, "nodeids_cache_entry_count": None,
        "nodeids_cache_parseable": False, "nodeids": [],
    }
    for prefix, path in (("lastfailed", lastfailed_path), ("nodeids", nodeids_path)):
        if not path.is_file():
            continue
        payload = path.read_bytes()
        result[f"{prefix}_cache_read"] = True
        result[f"{prefix}_cache_sha256"] = hashlib.sha256(payload).hexdigest()
        try:
            parsed = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        result[f"{prefix}_cache_parseable"] = True
        if prefix == "lastfailed" and isinstance(parsed, dict):
            result["failed_or_errored_nodeids"] = sorted(str(key) for key in parsed)
            result["lastfailed_cache_entry_count"] = len(parsed)
        elif prefix == "nodeids" and isinstance(parsed, list):
            result["nodeids"] = sorted(str(value) for value in parsed)
            result["nodeids_cache_entry_count"] = len(parsed)
        else:
            result[f"{prefix}_cache_parseable"] = False
    return result


def _empty_cache(worktree: Path) -> dict[str, Any]:
    return {
        "lastfailed_cache_path": str((worktree / ".pytest_cache" / "v" / "cache" / "lastfailed").resolve(strict=False)),
        "lastfailed_cache_read": False, "lastfailed_cache_sha256": None,
        "lastfailed_cache_entry_count": None, "lastfailed_cache_parseable": False,
        "failed_or_errored_nodeids": [],
        "nodeids_cache_path": str((worktree / ".pytest_cache" / "v" / "cache" / "nodeids").resolve(strict=False)),
        "nodeids_cache_read": False, "nodeids_cache_sha256": None,
        "nodeids_cache_entry_count": None, "nodeids_cache_parseable": False, "nodeids": [],
    }


def _module_grouping(nodeids: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for nodeid in sorted(nodeids):
        grouped[nodeid.split("::", 1)[0].replace("\\", "/")].append(nodeid)
    total = len(nodeids)
    rows = []
    for module_path, members in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        rows.append({
            "module_path": module_path,
            "failed_or_errored_nodeid_count": len(members),
            "sample_nodeids_bounded": members[:5],
            "percentage_of_failed_or_errored_nodeids": (
                format((Decimal(len(members)) * Decimal(100) / Decimal(total)), ".6f")
                if total else "0.000000"
            ),
            "classification_family": "MODULE_LEVEL_GROUPING_ONLY",
            "confidence": "HIGH_FOR_GROUPING_ONLY",
            "unsupported_claims": [
                "no_failure_error_separation", "no_first_order_claim", "no_traceback_root_cause",
            ],
        })
    return rows


def _source_fields() -> dict[str, Any]:
    fields = source._committed_source_fields()
    return {
        "source_classification_method_approval_v2_digest": SOURCE_APPROVAL_V2_DIGEST,
        "source_classification_method_candidate_v2_operator_review_digest": fields["source_classification_method_candidate_v2_operator_review_digest"],
        "source_classification_method_candidate_v2_digest": fields["source_classification_method_candidate_v2_digest"],
        "source_classification_method_reentry_digest": fields["source_classification_method_reentry_digest"],
        "source_classification_source_results_review_digest": fields["source_classification_source_results_review_digest"],
        "source_cache_manifest_review_digest": fields["source_cache_manifest_review_digest"],
        "source_output_capture_execution_digest": fields["source_output_capture_execution_digest"],
        "source_classification_source_manifest_digest": fields["source_classification_source_manifest_digest"],
        "source_retry_failure_diagnosis_digest": fields["source_retry_failure_diagnosis_digest"],
        "source_staged_inventory_digest": fields["source_staged_inventory_digest"],
        "retry_execution_branch": fields["retry_execution_branch"],
        "retry_execution_commit": fields["retry_execution_commit"],
        **{f"retry_pytest_{name}_count": fields[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")},
        "retry_pytest_first_result_authoritative": True, "root_full_regression_is_retry_evidence": False,
    }


def _cache_usable(cache: Mapping[str, Any]) -> bool:
    failed = cache.get("failed_or_errored_nodeids")
    all_nodeids = cache.get("nodeids")
    if not isinstance(failed, list) or not isinstance(all_nodeids, list):
        return False
    counts = Counter(nodeid.split("::", 1)[0].replace("\\", "/") for nodeid in failed)
    return bool(
        cache.get("lastfailed_cache_read") is True
        and cache.get("nodeids_cache_read") is True
        and cache.get("lastfailed_cache_parseable") is True
        and cache.get("nodeids_cache_parseable") is True
        and cache.get("lastfailed_cache_sha256") == EXPECTED_LASTFAILED_SHA256
        and cache.get("nodeids_cache_sha256") == EXPECTED_NODEIDS_SHA256
        and cache.get("lastfailed_cache_entry_count") == EXPECTED_LASTFAILED_COUNT
        and cache.get("nodeids_cache_entry_count") == EXPECTED_NODEIDS_COUNT
        and len(failed) == EXPECTED_LASTFAILED_COUNT
        and len(counts) == EXPECTED_MODULE_COUNT
        and sorted(counts.values(), reverse=True)[:5] == EXPECTED_LARGEST_MODULE_COUNTS
        and set(failed).issubset(set(all_nodeids))
    )


def _execution_steps(*, prechecks_passed: bool, success: bool, cache: Mapping[str, Any]) -> list[dict[str, Any]]:
    actuals = {
        "verify_source_approval": prechecks_passed, "verify_protected_refs": prechecks_passed,
        "verify_detached_worktree": prechecks_passed,
        "verify_cache_hashes": success,
        "parse_lastfailed_cache": cache.get("lastfailed_cache_parseable") is True,
        "parse_nodeids_cache": cache.get("nodeids_cache_parseable") is True,
        "build_module_nodeid_grouping": success, "build_module_summary": success,
        "build_limitations_report": success, "build_unsupported_claims_exclusion_report": success,
        "preserve_failed_retry_authority": True, "do_not_create_results_review": True,
    }
    rows = []
    for step_id in EXECUTION_STEP_IDS:
        actual = actuals[step_id]
        expected = actual if not success and step_id not in {
            "verify_source_approval", "verify_protected_refs", "verify_detached_worktree",
            "preserve_failed_retry_authority", "do_not_create_results_review",
        } else True
        rows.append({"step_id": step_id, "status": PASS if expected == actual else FAIL,
                     "expected": expected, "actual": actual,
                     "message": f"{step_id} {'completed' if actual else 'not completed'}"})
    return rows


def _base_execution(
    *, before: Mapping[str, Any], after: Mapping[str, Any], cache: Mapping[str, Any],
    prechecks: list[dict[str, Any]], run_timestamp_utc: str | None,
) -> dict[str, Any]:
    prechecks_passed = all(row["status"] == PASS for row in prechecks)
    success = prechecks_passed and _cache_usable(cache)
    grouping = _module_grouping(cache.get("failed_or_errored_nodeids", [])) if success else []
    counts = [row["failed_or_errored_nodeid_count"] for row in grouping]
    if success:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2
        status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY
        blocked_reason = None
        next_chain, next_gates, next_task = SUCCESS_NEXT_CHAIN, SUCCESS_NEXT_GATES, SUCCESS_NEXT_TASK
    else:
        artifact_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2
        status = (
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_PRECHECK_FAILED
            if not prechecks_passed
            else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_CACHE_SOURCE_MISMATCH_OR_BOUNDARY_FAILURE
        )
        failures = [row["check_id"] for row in prechecks if row["status"] != PASS]
        blocked_reason = "PRECHECK_FAILED: " + ", ".join(failures) if failures else "CACHE_SOURCE_HASH_COUNT_PARSE_OR_MODULE_BOUNDARY_MISMATCH"
        next_chain, next_gates, next_task = BLOCKED_NEXT_CHAIN, BLOCKED_NEXT_GATES, BLOCKED_NEXT_TASK
    module_summary = {
        "module_count": len(grouping), "total_nodeids": sum(counts),
        "largest_module_count": counts[0] if counts else 0,
        "top_modules_bounded": deepcopy(grouping[:10]),
    } if success else None
    planned_outputs = {
        "classification_v2_manifest": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "module_nodeid_grouping_report": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "module_summary_report": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "largest_module_summary": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "cache_source_limitation_report": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "low_confidence_root_cause_hint_report": "NOT_GENERATED_BY_SELECTED_PACKAGE",
        "unsupported_claims_exclusion_report": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "recommended_next_method_or_remediation_report": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
        "digest_manifest": "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED",
    }
    execution = {
        "artifact_kind": artifact_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2,
        "execution_status": status,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "created_offline_except_read_only_cache_inspection": True, "governance_only": True,
        "classification_execution_only": True, "run_timestamp_utc": run_timestamp_utc,
        **_source_fields(),
        "origin_main_commit_before_execution": before.get("origin_main_commit"),
        "origin_main_commit_after_execution": after.get("origin_main_commit"),
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_before_execution": before.get("integration_branch_head_commit"),
        "integration_branch_head_commit_after_execution": after.get("integration_branch_head_commit"),
        "remote_integration_branch_exists_before_execution": before.get("remote_integration_branch_exists"),
        "remote_integration_branch_exists_after_execution": after.get("remote_integration_branch_exists"),
        "detached_integration_worktree_path": before.get("detached_integration_worktree_path"),
        "detached_integration_worktree_head_commit_before_execution": before.get("detached_integration_worktree_head_commit"),
        "detached_integration_worktree_head_commit_after_execution": after.get("detached_integration_worktree_head_commit"),
        "detached_integration_worktree_clean_before_execution": before.get("detached_integration_worktree_clean"),
        "detached_integration_worktree_clean_after_execution": after.get("detached_integration_worktree_clean"),
        "staged_evidence_manifest_digest_before_execution": before.get("staged_evidence_manifest_digest"),
        "staged_evidence_manifest_digest_after_execution": after.get("staged_evidence_manifest_digest"),
        "staged_evidence_unchanged": before.get("staged_evidence_manifest_digest") == after.get("staged_evidence_manifest_digest") == EXPECTED_STAGED_EVIDENCE_DIGEST,
        "marketflow_outputs_tracked_in_repository": after.get("marketflow_outputs_tracked_in_repository"),
        "marketflow_outputs_tracked_in_detached_worktree": after.get("marketflow_outputs_tracked_in_detached_worktree"),
        "pytest_cache_tracked_in_repository": after.get("pytest_cache_tracked_in_repository"),
        "pytest_cache_tracked_in_detached_worktree": after.get("pytest_cache_tracked_in_detached_worktree"),
        **{key: deepcopy(cache.get(key)) for key in (
            "lastfailed_cache_path", "lastfailed_cache_read", "lastfailed_cache_sha256",
            "lastfailed_cache_entry_count", "lastfailed_cache_parseable", "nodeids_cache_path",
            "nodeids_cache_read", "nodeids_cache_sha256", "nodeids_cache_entry_count",
            "nodeids_cache_parseable",
        )},
        "classification_method_v2_executed": True,
        "classification_method_v2_selected": True, "classification_method_v2_approved": True,
        "classification_method_v2_authorized": True, "classification_method_v2_approval_created": True,
        "ready_for_classification_method_v2_execution": True,
        "classification_execution_created": success, "classification_execution_performed": success,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_used_for_module_level_only": success,
        "failed_or_errored_nodeids_classified": success,
        "failed_or_errored_nodeids_count": EXPECTED_LASTFAILED_COUNT if success else 0,
        "module_level_grouping_generated": success, "module_nodeid_grouping_report": grouping,
        "module_summary_generated": success, "module_summary_report": module_summary,
        "module_summary_module_count": len(grouping) if success else 0,
        "largest_module_summary_generated": success,
        "largest_module_nodeid_counts": counts[:5] if success else [],
        "failure_modules_classified": False, "error_modules_classified": False,
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "retry_success_claimed": False,
        "main_merge_readiness_claimed": False, "root_cause_family_hints_generated": False,
        "root_cause_family_hints_basis": "NOT_GENERATED_BY_SELECTED_PACKAGE",
        "limitations_report_generated": success,
        "cache_source_limitation_report": {
            "module_grouping_supported": True,
            "failure_error_separation_supported": False,
            "first_order_supported": False,
            "traceback_root_cause_supported": False,
            "retry_success_supported": False,
        } if success else None,
        "unsupported_claims_exclusion_report_generated": success,
        "unsupported_claims_exclusion_report": {
            "failure_error_separation_excluded": True, "first_failure_excluded": True,
            "first_error_excluded": True, "traceback_root_cause_excluded": True,
            "retry_success_excluded": True, "main_merge_readiness_excluded": True,
        } if success else None,
        "recommended_next_method_or_remediation_report": {
            "results_review_v2_required": True,
            "largest_modules_may_inform_future_candidate_after_review": True,
            "new_retry_blocked_until_classification_or_remediation_chain_complete": True,
        } if success else None,
        "planned_outputs_generated": success, "planned_outputs": planned_outputs,
        "blocked_reason": blocked_reason, "new_retry_candidate_created": False,
        "new_retry_executed": False, "new_retry_results_review_created": False,
        "integration_results_review_created": False, "main_merge_approval_created": False,
        "retry_rerun_performed": False, "full_pytest_performed": False,
        "diagnostic_command_executed": False, "diagnostic_output_captured": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "pytest_cache_committed": False, "evidence_regenerated": False,
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
        "next_chain": list(next_chain), "next_gates": list(next_gates),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": next_task,
        "precheck_results": deepcopy(prechecks),
        "execution_steps": _execution_steps(prechecks_passed=prechecks_passed, success=success, cache=cache),
    }
    if success:
        execution["marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest"] = semantic_digest(grouping)
        manifest = {
            "source_approval_v2_digest": SOURCE_APPROVAL_V2_DIGEST,
            "lastfailed_cache_sha256": cache.get("lastfailed_cache_sha256"),
            "nodeids_cache_sha256": cache.get("nodeids_cache_sha256"),
            "module_grouping_digest": execution["marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest"],
            "failed_or_errored_nodeids_count": EXPECTED_LASTFAILED_COUNT,
            "module_count": EXPECTED_MODULE_COUNT,
        }
        execution["digest_manifest"] = manifest
        execution["marketflow_repository_integration_branch_retry_failure_classification_method_v2_digest_manifest_digest"] = semantic_digest(manifest)
    else:
        execution["marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest"] = None
        execution["digest_manifest"] = None
        execution["marketflow_repository_integration_branch_retry_failure_classification_method_v2_digest_manifest_digest"] = None
    return execution


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2
    conditional = True if success else False
    expected_cache_hashes = [EXPECTED_LASTFAILED_SHA256, EXPECTED_NODEIDS_SHA256] if success else [execution.get("lastfailed_cache_sha256"), execution.get("nodeids_cache_sha256")]
    expected_cache_counts = [EXPECTED_LASTFAILED_COUNT, EXPECTED_NODEIDS_COUNT] if success else [execution.get("lastfailed_cache_entry_count"), execution.get("nodeids_cache_entry_count")]
    values = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_V2_DIGEST, execution.get("source_classification_method_approval_v2_digest")),
        "source_operator_review_digest_bound": (source.SOURCE_OPERATOR_REVIEW_DIGEST, execution.get("source_classification_method_candidate_v2_operator_review_digest")),
        "source_candidate_v2_digest_bound": (source.source.SOURCE_CANDIDATE_V2_DIGEST, execution.get("source_classification_method_candidate_v2_digest")),
        "source_reentry_digest_bound": (source.source.source.SOURCE_REENTRY_DIGEST, execution.get("source_classification_method_reentry_digest")),
        "source_results_review_digest_bound": (source.source.source.SOURCE_RESULTS_REVIEW_DIGEST, execution.get("source_classification_source_results_review_digest")),
        "source_cache_manifest_digest_bound": (source.source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, execution.get("source_cache_manifest_review_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [execution.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "cache_hashes_verified": (expected_cache_hashes, [execution.get("lastfailed_cache_sha256"), execution.get("nodeids_cache_sha256")]),
        "cache_counts_verified": (expected_cache_counts, [execution.get("lastfailed_cache_entry_count"), execution.get("nodeids_cache_entry_count")]),
        "module_count_29": (EXPECTED_MODULE_COUNT if success else execution.get("module_summary_module_count"), execution.get("module_summary_module_count")),
        "largest_module_counts_verified": (EXPECTED_LARGEST_MODULE_COUNTS if success else execution.get("largest_module_nodeid_counts"), execution.get("largest_module_nodeid_counts")),
        "classification_method_v2_executed_true": (True, execution.get("classification_method_v2_executed")),
        "classification_execution_created_true_if_success": (conditional, execution.get("classification_execution_created")),
        "classification_execution_performed_true_if_success": (conditional, execution.get("classification_execution_performed")),
        "module_level_grouping_generated_true_if_success": (conditional, execution.get("module_level_grouping_generated")),
        "module_summary_generated_true_if_success": (conditional, execution.get("module_summary_generated")),
        "failed_or_errored_nodeids_count_1404_if_success": (EXPECTED_LASTFAILED_COUNT if success else 0, execution.get("failed_or_errored_nodeids_count")),
        "failure_modules_classified_false": (False, execution.get("failure_modules_classified")),
        "error_modules_classified_false": (False, execution.get("error_modules_classified")),
        "failure_error_separation_claimed_false": (False, execution.get("failure_error_separation_claimed")),
        "first_failure_identified_false": (False, execution.get("first_failure_identified")),
        "first_error_identified_false": (False, execution.get("first_error_identified")),
        "first_order_claim_made_false": (False, execution.get("first_order_claim_made")),
        "traceback_root_cause_claimed_false": (False, execution.get("traceback_root_cause_claimed")),
        "retry_success_claimed_false": (False, execution.get("retry_success_claimed")),
        "main_merge_readiness_claimed_false": (False, execution.get("main_merge_readiness_claimed")),
        "limitations_report_generated_true_if_success": (conditional, execution.get("limitations_report_generated")),
        "unsupported_claims_exclusion_report_generated_true_if_success": (conditional, execution.get("unsupported_claims_exclusion_report_generated")),
        "planned_outputs_generated_true_if_success": (conditional, execution.get("planned_outputs_generated")),
        "new_retry_candidate_created_false": (False, execution.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, execution.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, execution.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, execution.get("main_merge_approval_created")),
        "retry_rerun_false": (False, execution.get("retry_rerun_performed")),
        "full_pytest_false": (False, execution.get("full_pytest_performed")),
        "diagnostic_command_false": (False, execution.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, execution.get("diagnostic_output_captured")),
        "integration_success_false": (False, execution.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
        "main_push_false": (False, execution.get("main_push_performed")),
        "origin_main_modified_false": (False, execution.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, execution.get("pytest_cache_committed")),
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
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": ([False, False], [execution.get("marketflow_outputs_tracked_in_repository"), execution.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "no_tracked_pytest_cache_files": ([False, False], [execution.get("pytest_cache_tracked_in_repository"), execution.get("pytest_cache_tracked_in_detached_worktree")]),
    }
    return [_record(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    success = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2
    summary = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "classification_method_v2_executed": True,
        "classification_execution_performed": success, "module_level_grouping_generated": success,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        summary.update({
            "failed_or_errored_nodeids_classified": True,
            "failed_or_errored_nodeids_count": EXPECTED_LASTFAILED_COUNT,
            "module_summary_module_count": EXPECTED_MODULE_COUNT,
            "failure_error_separation_claimed": False, "first_order_claim_made": False,
            "traceback_root_cause_claimed": False, "new_retry_candidate_created": False,
            "integration_execution_successful": False,
        })
    else:
        summary["blocked_reason"] = execution.get("blocked_reason")
    return summary


def marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
    *, repo_root: str | Path | None = None, integration_worktree_path: str | Path | None = None,
    cache_snapshot: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    """Execute read-only module grouping or return a deterministic blocked artifact."""
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    worktree = Path(integration_worktree_path) if integration_worktree_path is not None else DEFAULT_INTEGRATION_WORKTREE
    if cache_snapshot is None:
        before = _state_snapshot(root, worktree)
        prechecks = _prechecks(before)
        cache = _read_cache(worktree) if all(row["status"] == PASS for row in prechecks) else _empty_cache(worktree)
        after = _state_snapshot(root, worktree)
    else:
        if not isinstance(cache_snapshot, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error(
                "cache_snapshot must be an object"
            )
        before = deepcopy(cache_snapshot.get("before", cache_snapshot))
        after = deepcopy(cache_snapshot.get("after", before))
        cache = deepcopy(cache_snapshot.get("cache", cache_snapshot))
        prechecks = _prechecks(before)
    execution = _base_execution(before=before, after=after, cache=cache, prechecks=prechecks, run_timestamp_utc=run_timestamp_utc)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution, execution["checklist"])
    execution["marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest"] = (
        marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest_v1(execution)
    )
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(execution)
    return execution


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
    execution: dict,
) -> dict:
    """Validate success or blocked execution while enforcing closed authority boundaries."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error(
            "execution must be an object"
        )
    kind = execution.get("artifact_kind")
    success = kind == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2
    blocked = kind == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2
    if not (success or blocked):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("artifact_kind mismatch")
    valid_statuses = {
        ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2: {
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY
        },
        ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2: {
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_CACHE_SOURCE_MISMATCH_OR_BOUNDARY_FAILURE,
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_PRECHECK_FAILED,
        },
    }
    if execution.get("execution_status") not in valid_statuses[kind]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("execution_status mismatch")
    static = {
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        **_source_fields(), "risk_controls": RISK_CONTROLS,
        "next_chain": SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN,
        "next_gates": SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(execution.get(field), expected, field)
    for field in (
        "created_offline_except_read_only_cache_inspection", "governance_only",
        "classification_execution_only", "classification_method_v2_selected",
        "classification_method_v2_approved", "classification_method_v2_authorized",
        "classification_method_v2_approval_created", "ready_for_classification_method_v2_execution",
        "classification_method_v2_executed",
    ):
        _expect(execution.get(field), True, field)
    required_false = (
        "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
        "first_failure_identified", "first_error_identified", "first_order_claim_made",
        "traceback_root_cause_claimed", "retry_success_claimed", "main_merge_readiness_claimed",
        "root_cause_family_hints_generated", "new_retry_candidate_created", "new_retry_executed",
        "new_retry_results_review_created", "integration_results_review_created", "main_merge_approval_created",
        "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
        "diagnostic_output_captured", "integration_execution_successful",
        "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
        "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
        "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
        "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
        "marketflow_outputs_tracked_in_repository", "marketflow_outputs_tracked_in_detached_worktree",
        "pytest_cache_tracked_in_repository", "pytest_cache_tracked_in_detached_worktree",
    )
    for field in required_false:
        _expect(execution.get(field), False, field)
    _expect(execution.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(execution.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(execution.get(field), NOT_AUTHORIZED, field)
    if success:
        for field in (
            "classification_execution_created", "classification_execution_performed",
            "classification_source_used_for_module_level_only", "failed_or_errored_nodeids_classified",
            "module_level_grouping_generated", "module_summary_generated",
            "largest_module_summary_generated", "limitations_report_generated",
            "unsupported_claims_exclusion_report_generated", "planned_outputs_generated",
            "lastfailed_cache_read", "nodeids_cache_read", "lastfailed_cache_parseable", "nodeids_cache_parseable",
        ):
            _expect(execution.get(field), True, field)
        _expect(execution.get("lastfailed_cache_sha256"), EXPECTED_LASTFAILED_SHA256, "lastfailed_cache_sha256")
        _expect(execution.get("nodeids_cache_sha256"), EXPECTED_NODEIDS_SHA256, "nodeids_cache_sha256")
        _expect(execution.get("lastfailed_cache_entry_count"), EXPECTED_LASTFAILED_COUNT, "lastfailed_cache_entry_count")
        _expect(execution.get("nodeids_cache_entry_count"), EXPECTED_NODEIDS_COUNT, "nodeids_cache_entry_count")
        _expect(execution.get("failed_or_errored_nodeids_count"), EXPECTED_LASTFAILED_COUNT, "failed_or_errored_nodeids_count")
        _expect(execution.get("module_summary_module_count"), EXPECTED_MODULE_COUNT, "module_summary_module_count")
        _expect(execution.get("largest_module_nodeid_counts"), EXPECTED_LARGEST_MODULE_COUNTS, "largest_module_nodeid_counts")
        grouping = execution.get("module_nodeid_grouping_report")
        if not isinstance(grouping, list) or len(grouping) != EXPECTED_MODULE_COUNT:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("module grouping missing")
        grouping_digest = execution.get("marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest")
        _expect(grouping_digest, semantic_digest(grouping), "module grouping digest")
        manifest = execution.get("digest_manifest")
        if not isinstance(manifest, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("digest_manifest missing")
        _expect(execution.get("marketflow_repository_integration_branch_retry_failure_classification_method_v2_digest_manifest_digest"), semantic_digest(manifest), "digest manifest digest")
        if execution.get("cache_source_limitation_report") is None or execution.get("unsupported_claims_exclusion_report") is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("required report missing")
    else:
        for field in ("classification_execution_created", "classification_execution_performed", "module_level_grouping_generated", "module_summary_generated", "planned_outputs_generated"):
            _expect(execution.get(field), False, field)
        reason = execution.get("blocked_reason")
        if not isinstance(reason, str) or not reason:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("blocked_reason missing")
    checklist = execution.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("checklist missing")
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(execution), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("checklist failed")
    _expect(execution.get("summary"), _summary(execution, checklist), "summary")
    digest = execution.get("marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error("execution digest missing")
    _expect(digest, marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest_v1(execution), "execution digest")
    return {
        "artifact_kind": kind, "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest": digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_markdown_v1(
    execution: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(execution)
    success = execution["artifact_kind"] == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2
    sections = [
        ("Source Approval", [f"Approval-v2 digest: `{SOURCE_APPROVAL_V2_DIGEST}`.", f"Selected package: `{SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The root regression is not retry evidence."]),
        ("Cache Source Verification", [f"Lastfailed hash/count: `{execution['lastfailed_cache_sha256']}` / `{execution['lastfailed_cache_entry_count']}`.", f"Nodeids hash/count: `{execution['nodeids_cache_sha256']}` / `{execution['nodeids_cache_entry_count']}`."]),
        ("Execution Scope", ["Read-only cache-supported module-level node-ID grouping only."]),
        ("Module-Level Grouping", [f"Generated: `{execution['module_level_grouping_generated']}`; modules: `{execution['module_summary_module_count']}`; node IDs: `{execution['failed_or_errored_nodeids_count']}`."]),
        ("Limitations", ["No failure/error separation, first-order analysis, traceback root cause, or retry-success inference is supported."]),
        ("Unsupported Claims Exclusion", [f"Report generated: `{execution['unsupported_claims_exclusion_report_generated']}`."]),
        ("Success or Blocked Disposition", [f"Status: `{execution['execution_status']}`.", f"Blocked reason: `{execution['blocked_reason']}`." if not success else f"Next task: `{SUCCESS_NEXT_TASK}`."]),
        ("Authority Boundaries", ["No retry, results review, main merge, provider/data action, runtime, or trading authority is created."]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", [f"`{row}`" for row in execution["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in execution["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Cache is read-only and never committed.", "A separate results review is required before any remediation or retry path."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Classification Method Execution v2", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
