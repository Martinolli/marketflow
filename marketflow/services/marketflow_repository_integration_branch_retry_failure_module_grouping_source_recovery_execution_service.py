"""Recover module grouping from the reviewed detached pytest cache, read-only."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_service
    as approval_source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1 = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1"
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1 = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_PRECHECK_FAILED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_PRECHECK_FAILED"
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1"
SOURCE_APPROVAL_DIGEST = "3b2e00be71e6aa209520bba347397bc12134566adfd30ff29e432ba0c7ce4b76"
EXPECTED_LASTFAILED_SHA256 = "24fb8cf5ce237ae6c952c29c37acaea7d22205ca885659a196f0bc27c4b1f1b1"
EXPECTED_NODEIDS_SHA256 = "9d69140fd12f57de3c14060139bc4d50a3096c29b0262c5e482af5b78ea0206d"
EXPECTED_LASTFAILED_COUNT = 1404
EXPECTED_NODEIDS_COUNT = 26288
EXPECTED_MODULE_COUNT = 29
EXPECTED_LARGEST_COUNTS = [136, 131, 122, 112, 111]
DEFAULT_WORKTREE = Path(r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1")
SELECTED_PACKAGE = approval_source.SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

UNSUPPORTED_CLAIMS = {
    "failure_modules_classified": False, "error_modules_classified": False,
    "failure_error_separation_claimed": False, "first_failure_identified": False,
    "first_error_identified": False, "first_order_claim_made": False,
    "traceback_root_cause_claimed": False, "direct_code_remediation_recommended": False,
    "retry_success_claimed": False, "main_merge_readiness_claimed": False,
}
UNSUPPORTED_ROW_CLAIMS = [
    "no_failure_error_separation", "no_first_order_claim", "no_traceback_root_cause",
    "no_direct_code_remediation", "no_retry_success", "no_main_merge_readiness",
]
OUTPUT_IDS = [item["output_id"] for item in approval_source.AUTHORIZED_PLANNED_OUTPUTS]
SUCCESS_NEXT_CHAIN = [
    "Module Grouping Source Recovery Results Review v1.",
    "Re-enter after-v2 planning execution, if source detail is recovered and reviewed.",
    "Remediation or Method Results Review After Classification v2 Review v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Approval / Execution / Results Review, if selected.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Module Grouping Source Recovery Execution Failure Diagnosis v1.",
    "Recovery remediation candidate, if needed.",
    "No planning re-entry, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "module_grouping_source_recovery_results_review",
    "after_v2_planning_reentry_if_source_recovered_and_reviewed",
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "module_grouping_source_recovery_execution_failure_diagnosis",
    "source_recovery_remediation_candidate_if_needed",
    "planning_reentry_blocked_until_source_recovery_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "source_recovery_execution_reads_reviewed_cache_read_only", "source_recovery_execution_does_not_modify_cache",
    "source_recovery_execution_does_not_commit_pytest_cache", "source_recovery_execution_does_not_commit_marketflow_outputs",
    "source_recovery_execution_does_not_parse_operator_logs", "source_recovery_execution_does_not_run_diagnostic_commands",
    "source_recovery_execution_does_not_execute_diagnostics", "source_recovery_execution_does_not_execute_remediation",
    "source_recovery_execution_does_not_execute_classification_again", "source_recovery_execution_does_not_rerun_retry",
    "source_recovery_execution_does_not_run_full_pytest", "source_recovery_execution_does_not_create_new_retry_candidate",
    "source_recovery_execution_does_not_create_retry_results_review", "source_recovery_execution_does_not_create_integration_results_review",
    "source_recovery_execution_does_not_mark_integration_successful", "source_recovery_execution_does_not_generate_successful_integration_digest",
    "source_recovery_execution_does_not_claim_failure_error_separation", "source_recovery_execution_does_not_claim_first_failure",
    "source_recovery_execution_does_not_claim_first_error", "source_recovery_execution_does_not_claim_traceback_root_cause",
    "source_recovery_execution_does_not_recommend_direct_code_remediation", "source_recovery_execution_does_not_treat_cache_or_classification_as_retry_success",
    "source_recovery_execution_does_not_push_integration_branch", "source_recovery_execution_does_not_push_main",
    "source_recovery_execution_does_not_delete_integration_branch", "source_recovery_execution_does_not_delete_worktree",
    "source_recovery_execution_does_not_force_push", "source_recovery_execution_does_not_prune_remotes",
    "source_recovery_execution_does_not_modify_tags", "source_recovery_execution_does_not_modify_staged_evidence",
    "source_recovery_execution_does_not_regenerate_evidence", "source_recovery_execution_does_not_call_providers",
    "source_recovery_execution_does_not_acquire_market_data", "source_recovery_execution_does_not_regenerate_dataset",
    "source_recovery_execution_does_not_recompute_metrics", "source_recovery_execution_does_not_train_models",
    "source_recovery_execution_does_not_score_strategy", "source_recovery_execution_does_not_generate_recommendations",
    "source_recovery_execution_does_not_accept_predictive_usefulness", "source_recovery_execution_does_not_accept_profitability",
    "source_recovery_execution_does_not_authorize_runtime", "source_recovery_execution_does_not_authorize_broker_execution",
    "source_recovery_output_is_planning_source_not_root_cause", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_results_review_required_after_source_recovery",
    "separate_planning_reentry_required_after_results_review", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]
COMMON_CHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound", "source_candidate_digest_bound",
    "source_blocked_execution_digest_bound", "source_blocked_manifest_digest_bound", "source_blocked_reason_bound",
    "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound", "source_module_grouping_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "cache_hashes_verified_if_success",
    "cache_counts_verified_if_success", "lastfailed_nodeids_subset_of_nodeids_if_success",
    "module_grouping_recovered_if_success", "module_paths_recovered_if_success", "per_module_counts_recovered_if_success",
    "bounded_nodeid_samples_recovered_if_success", "module_count_29_if_success", "largest_module_counts_if_success",
    "unsupported_claims_boundary_bound", "source_recovery_executed_true", "diagnostic_execution_false",
    "remediation_execution_false", "classification_again_false", "failure_modules_classified_false",
    "error_modules_classified_false", "failure_error_separation_claimed_false", "first_failure_identified_false",
    "first_error_identified_false", "first_order_claim_made_false", "traceback_root_cause_claimed_false",
    "direct_code_remediation_recommended_false", "retry_success_claimed_false", "main_merge_readiness_claimed_false",
    "planning_reentry_created_false", "new_retry_candidate_created_false", "new_retry_executed_false",
    "new_retry_results_review_created_false", "main_merge_approval_created_false", "retry_rerun_false",
    "full_pytest_false", "diagnostic_command_false", "diagnostic_output_false", "integration_success_false",
    "successful_integration_digest_false", "integration_branch_pushed_false", "main_push_false",
    "origin_main_modified_false", "marketflow_outputs_committed_false", "pytest_cache_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError(ValueError):
    pass


def _normalize(value: Any) -> list[str]:
    if isinstance(value, dict):
        values = value.keys()
    elif isinstance(value, list):
        values = value
    else:
        raise ValueError("cache JSON must be an object or list")
    result = sorted(str(item) for item in values)
    if not result:
        raise ValueError("cache JSON is empty")
    return result


def _read_cache(worktree: Path, snapshot: dict | None) -> dict[str, Any]:
    last_path = worktree / ".pytest_cache" / "v" / "cache" / "lastfailed"
    node_path = worktree / ".pytest_cache" / "v" / "cache" / "nodeids"
    if snapshot is not None:
        return {
            "last_path": str(last_path), "node_path": str(node_path),
            "last_hash": snapshot.get("lastfailed_sha256", EXPECTED_LASTFAILED_SHA256),
            "node_hash": snapshot.get("nodeids_sha256", EXPECTED_NODEIDS_SHA256),
            "last_ids": _normalize(snapshot["lastfailed"]), "node_ids": _normalize(snapshot["nodeids"]),
            "last_read": True, "node_read": True, "last_parseable": True, "node_parseable": True,
        }
    last_raw = last_path.read_bytes()
    node_raw = node_path.read_bytes()
    return {
        "last_path": str(last_path), "node_path": str(node_path),
        "last_hash": hashlib.sha256(last_raw).hexdigest(), "node_hash": hashlib.sha256(node_raw).hexdigest(),
        "last_ids": _normalize(json.loads(last_raw)), "node_ids": _normalize(json.loads(node_raw)),
        "last_read": True, "node_read": True, "last_parseable": True, "node_parseable": True,
    }


def _source_fields() -> dict[str, Any]:
    base = approval_source._source_fields()
    return {
        "source_module_grouping_source_recovery_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": approval_source.source.SOURCE_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": base["source_blocked_after_v2_execution_digest"],
        "source_blocked_after_v2_manifest_digest": base["source_blocked_after_v2_manifest_digest"],
        "blocked_reason_before_recovery": base["blocked_reason"],
        **{key: deepcopy(base[key]) for key in (
            "source_results_review_v2_digest", "source_review_manifest_digest", "source_execution_v2_digest",
            "source_module_grouping_digest", "source_digest_manifest_digest", "source_approval_v2_digest",
            "source_staged_inventory_digest", "retry_execution_branch", "retry_execution_commit",
            "retry_pytest_passed_count", "retry_pytest_failed_count", "retry_pytest_error_count",
            "retry_pytest_skipped_count", "retry_pytest_first_result_authoritative",
            "root_full_regression_is_retry_evidence", "classification_evidence_summary",
        )},
        "retry_pytest_working_directory": str(DEFAULT_WORKTREE),
    }


def _common(run_timestamp_utc: str | None, worktree: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN,
        "selected_module_grouping_source_recovery_package": SELECTED_PACKAGE,
        "created_offline_except_read_only_cache_inspection": True, "governance_only": True,
        "source_recovery_execution_only": True, "run_timestamp_utc": run_timestamp_utc,
        **_source_fields(),
        "module_grouping_source_recovery_executed": True,
        **deepcopy(UNSUPPORTED_CLAIMS),
        "diagnostic_method_executed": False, "code_remediation_executed": False,
        "evidence_remediation_executed": False, "classification_execution_performed": False,
        "remediation_or_method_after_v2_reentry_created": False, "new_retry_candidate_created": False,
        "new_retry_executed": False, "new_retry_results_review_created": False,
        "main_merge_approval_created": False, "retry_rerun_performed": False,
        "full_pytest_performed": False, "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "origin_main_commit_before_execution": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "origin_main_commit_after_execution": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit_before_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "integration_branch_head_commit_after_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists_before_execution": False, "remote_integration_branch_exists_after_execution": False,
        "detached_integration_worktree_path": str(worktree),
        "detached_integration_worktree_head_commit_before_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "detached_integration_worktree_head_commit_after_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "detached_integration_worktree_clean_before_execution": True, "detached_integration_worktree_clean_after_execution": True,
        "staged_evidence_manifest_digest_before_execution": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_manifest_digest_after_execution": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True, "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False, "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "pytest_cache_committed": False, "evidence_regenerated": False,
        "provider_requests_made_in_execution": False, "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False, "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }


def _verification(cache: Mapping[str, Any]) -> dict[str, Any]:
    node_set = set(cache["node_ids"])
    return {
        "lastfailed_cache_path": cache["last_path"], "lastfailed_cache_read": cache["last_read"],
        "lastfailed_cache_parseable_json": cache["last_parseable"],
        "lastfailed_cache_sha256_expected": EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_sha256_actual": cache["last_hash"],
        "lastfailed_cache_entry_count_expected": EXPECTED_LASTFAILED_COUNT,
        "lastfailed_cache_entry_count_actual": len(cache["last_ids"]),
        "nodeids_cache_path": cache["node_path"], "nodeids_cache_read": cache["node_read"],
        "nodeids_cache_parseable_json": cache["node_parseable"],
        "nodeids_cache_sha256_expected": EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_sha256_actual": cache["node_hash"],
        "nodeids_cache_entry_count_expected": EXPECTED_NODEIDS_COUNT,
        "nodeids_cache_entry_count_actual": len(cache["node_ids"]),
        "lastfailed_nodeids_subset_of_nodeids": all(item in node_set for item in cache["last_ids"]),
    }


def _rows(last_ids: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for nodeid in last_ids:
        grouped[nodeid.split("::", 1)[0]].append(nodeid)
    counts = Counter({path: len(ids) for path, ids in grouped.items()})
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{
        "module_path": path, "failed_or_errored_nodeid_count": count,
        "percentage_of_failed_or_errored_nodeids": f"{count * 100 / len(last_ids):.8f}",
        "priority_order": index, "sample_nodeids_bounded": sorted(grouped[path])[:5],
        "source": "REVIEWED_DETACHED_PYTEST_CACHE_LASTFAILED",
        "confidence": "HIGH_FOR_MODULE_GROUPING_ONLY", "basis": "CACHE_NODEID_MODULE_PATH_ONLY",
        "unsupported_claims": list(UNSUPPORTED_ROW_CLAIMS),
    } for index, (path, count) in enumerate(ordered, 1)]


def _record(item_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"step_id": item_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "message": f"{item_id} {'passed' if status == PASS else 'failed'}"}


def _records(ids: list[str]) -> list[dict[str, Any]]:
    return [_record(item_id, True, True) for item_id in ids]


def _finish(artifact: dict[str, Any], success: bool) -> dict[str, Any]:
    artifact["next_chain"] = list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN)
    artifact["next_gates"] = list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES)
    artifact["precheck_results"] = _records([
        "source_approval_digest_bound", "source_operator_review_digest_bound", "source_candidate_digest_bound",
        "source_blocked_execution_digest_bound", "source_blocked_manifest_digest_bound", "source_results_review_v2_digest_bound",
        "source_execution_v2_digest_bound", "source_module_grouping_digest_bound", "retry_failure_counts_bound",
        "module_count_and_largest_counts_bound", "unsupported_claims_boundary_bound", "origin_main_unchanged",
        "integration_branch_head_unchanged", "detached_worktree_head_verified", "detached_worktree_clean_before_execution",
        "staged_evidence_unchanged", "marketflow_outputs_not_tracked", "pytest_cache_not_tracked",
        "no_retry_rerun", "no_full_pytest", "no_diagnostic_command",
    ])
    artifact["execution_steps"] = _records([
        "verify_source_approval", "verify_source_operator_review", "verify_source_candidate", "verify_source_blocked_execution",
        "verify_classification_results_review_v2", "verify_protected_refs", "verify_detached_worktree",
        "verify_tracking_boundaries", "locate_reviewed_lastfailed_cache", "locate_reviewed_nodeids_cache",
        "verify_lastfailed_cache_hash_and_count", "verify_nodeids_cache_hash_and_count", "parse_lastfailed_cache",
        "parse_nodeids_cache", "verify_lastfailed_nodeids_subset_of_nodeids", "recover_module_paths_from_nodeids",
        "build_recovered_module_counts_by_path", "build_recovered_bounded_nodeid_samples",
        "verify_recovered_module_count_and_largest_counts", "build_source_recovery_reports",
        "preserve_unsupported_claims_boundary", "preserve_failed_retry_authority", "do_not_create_planning_reentry",
        "do_not_create_retry_candidate", "do_not_create_results_review",
    ])
    artifact["checklist"] = _checklist(artifact, success)
    failed = [item for item in artifact["checklist"] if item["status"] != PASS]
    artifact["summary"] = {
        "total_checks": len(artifact["checklist"]), "passed_checks": len(artifact["checklist"]) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "module_grouping_source_recovery_executed": True,
        "module_grouping_detail_recovered": success, "module_paths_recovered": success,
        "per_module_counts_recovered": success, "after_v2_planning_reentry_created": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        artifact["summary"].update(
            module_grouping_detail_exposed=True, bounded_nodeid_samples_recovered=True,
            failed_or_errored_nodeids_count=EXPECTED_LASTFAILED_COUNT,
            module_summary_module_count=EXPECTED_MODULE_COUNT,
            ready_for_module_grouping_source_recovery_results_review=True,
        )
    else:
        artifact["summary"]["blocked_reason"] = artifact["blocked_reason"]
    artifact["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest"] = _execution_digest(artifact)
    return artifact


def _checklist(x: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    v = x.get("cache_hash_and_count_verification_report", {})
    expected_if_success = True if success else False
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_DIGEST, x.get("source_module_grouping_source_recovery_approval_digest")),
        "source_operator_review_digest_bound": (approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, x.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_candidate_digest_bound": (approval_source.source.SOURCE_CANDIDATE_DIGEST, x.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_execution_digest_bound": (approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, x.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_manifest_digest_bound": (approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, x.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL, x.get("blocked_reason_before_recovery")),
        "source_results_review_v2_digest_bound": (approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, x.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, x.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, x.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", x.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877,1292,112,7], [x.get(f"retry_pytest_{n}_count") for n in ("passed","failed","error","skipped")]),
        "cache_hashes_verified_if_success": (expected_if_success, success and v.get("lastfailed_cache_sha256_actual") == EXPECTED_LASTFAILED_SHA256 and v.get("nodeids_cache_sha256_actual") == EXPECTED_NODEIDS_SHA256),
        "cache_counts_verified_if_success": (expected_if_success, success and v.get("lastfailed_cache_entry_count_actual") == EXPECTED_LASTFAILED_COUNT and v.get("nodeids_cache_entry_count_actual") == EXPECTED_NODEIDS_COUNT),
        "lastfailed_nodeids_subset_of_nodeids_if_success": (expected_if_success, success and v.get("lastfailed_nodeids_subset_of_nodeids") is True),
        "module_grouping_recovered_if_success": (success, x.get("module_grouping_detail_recovered")),
        "module_paths_recovered_if_success": (success, x.get("module_paths_recovered")),
        "per_module_counts_recovered_if_success": (success, x.get("per_module_counts_recovered")),
        "bounded_nodeid_samples_recovered_if_success": (success, x.get("bounded_nodeid_samples_recovered")),
        "module_count_29_if_success": (EXPECTED_MODULE_COUNT if success else 0, x.get("module_summary_module_count", 0)),
        "largest_module_counts_if_success": (EXPECTED_LARGEST_COUNTS if success else [], x.get("largest_module_nodeid_counts", [])),
        "unsupported_claims_boundary_bound": (UNSUPPORTED_CLAIMS, {key: x.get(key) for key in UNSUPPORTED_CLAIMS}),
        "source_recovery_executed_true": (True, x.get("module_grouping_source_recovery_executed")),
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, x.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, x.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, x.get("risk_controls")),
        "no_tracked_marketflow_files": (False, x.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, x.get("pytest_cache_tracked_in_repository")),
    }
    false_map = {
        "diagnostic_execution_false":"diagnostic_method_executed", "remediation_execution_false":"code_remediation_executed",
        "classification_again_false":"classification_execution_performed", "failure_modules_classified_false":"failure_modules_classified",
        "error_modules_classified_false":"error_modules_classified", "failure_error_separation_claimed_false":"failure_error_separation_claimed",
        "first_failure_identified_false":"first_failure_identified", "first_error_identified_false":"first_error_identified",
        "first_order_claim_made_false":"first_order_claim_made", "traceback_root_cause_claimed_false":"traceback_root_cause_claimed",
        "direct_code_remediation_recommended_false":"direct_code_remediation_recommended", "retry_success_claimed_false":"retry_success_claimed",
        "main_merge_readiness_claimed_false":"main_merge_readiness_claimed", "planning_reentry_created_false":"remediation_or_method_after_v2_reentry_created",
        "new_retry_candidate_created_false":"new_retry_candidate_created", "new_retry_executed_false":"new_retry_executed",
        "new_retry_results_review_created_false":"new_retry_results_review_created", "main_merge_approval_created_false":"main_merge_approval_created",
        "retry_rerun_false":"retry_rerun_performed", "full_pytest_false":"full_pytest_performed",
        "diagnostic_command_false":"diagnostic_command_executed", "diagnostic_output_false":"diagnostic_output_captured",
        "integration_success_false":"integration_execution_successful", "integration_branch_pushed_false":"integration_branch_pushed",
        "main_push_false":"main_push_performed", "origin_main_modified_false":"origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false":"marketflow_outputs_committed", "pytest_cache_committed_false":"pytest_cache_committed",
        "evidence_regenerated_false":"evidence_regenerated", "provider_requests_false":"provider_requests_made_in_execution",
        "market_data_acquisition_false":"market_data_acquisition_performed_in_execution", "dataset_generation_false":"dataset_generation_performed_in_execution",
        "metric_recomputation_false":"metric_recomputation_from_raw_rows_performed", "model_training_false":"model_training_performed",
        "strategy_scoring_false":"strategy_scoring_performed", "recommendations_false":"trade_recommendations_generated",
    }
    values.update({check_id:(False,x.get(field)) for check_id,field in false_map.items()})
    values.update({
        "successful_integration_digest_false":([False,False],[x.get("successful_integration_execution_digest_generated"),x.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted":(NOT_ACCEPTED,x.get("predictive_usefulness")),
        "profitability_not_accepted":(NOT_ACCEPTED,x.get("profitability")),
        "runtime_not_authorized":(NOT_AUTHORIZED,x.get("runtime_use")), "broker_not_authorized":(NOT_AUTHORIZED,x.get("broker_execution")),
    })
    extra = {
        "source_recovery_detail_digest_generated": (True, bool(x.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_detail_digest"))),
        "digest_manifest_digest_generated": (True, bool(x.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_digest_manifest_digest"))),
        "planning_reentry_readiness_report_generated": (True, x.get("planning_reentry_readiness_report_generated")),
        "ready_for_source_recovery_results_review_true": (True, x.get("ready_for_module_grouping_source_recovery_results_review")),
    } if success else {
        "blocked_reason_recorded": (True, bool(x.get("blocked_reason"))),
        "blocked_manifest_digest_generated": (True, bool(x.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_blocked_manifest_digest"))),
        "module_grouping_detail_recovered_false": (False, x.get("module_grouping_detail_recovered")),
        "source_recovery_failure_diagnosis_defined": (BLOCKED_NEXT_TASK, x.get("recommended_next_task")),
    }
    values.update(extra)
    ids = COMMON_CHECK_IDS + list(extra)
    return [{"check_id": check_id, "status": PASS if values[check_id][0] == values[check_id][1] else FAIL,
             "expected": deepcopy(values[check_id][0]), "actual": deepcopy(values[check_id][1]), "severity": BLOCKER,
             "message": f"{check_id} {'passed' if values[check_id][0] == values[check_id][1] else 'failed'}"} for check_id in ids]


def _execution_digest(x: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(x))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(
    *, repo_root: str | Path | None = None, integration_worktree_path: str | Path | None = None,
    cache_snapshot: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    del repo_root
    worktree = Path(integration_worktree_path) if integration_worktree_path else DEFAULT_WORKTREE
    common = _common(run_timestamp_utc, worktree)
    try:
        cache = _read_cache(worktree, cache_snapshot)
        verification = _verification(cache)
        rows = _rows(cache["last_ids"])
        counts = [row["failed_or_errored_nodeid_count"] for row in rows]
        reasons = []
        if cache["last_hash"] != EXPECTED_LASTFAILED_SHA256: reasons.append("LASTFAILED_CACHE_SHA256_MISMATCH")
        if cache["node_hash"] != EXPECTED_NODEIDS_SHA256: reasons.append("NODEIDS_CACHE_SHA256_MISMATCH")
        if len(cache["last_ids"]) != EXPECTED_LASTFAILED_COUNT: reasons.append("LASTFAILED_CACHE_ENTRY_COUNT_MISMATCH")
        if len(cache["node_ids"]) != EXPECTED_NODEIDS_COUNT: reasons.append("NODEIDS_CACHE_ENTRY_COUNT_MISMATCH")
        if not verification["lastfailed_nodeids_subset_of_nodeids"]: reasons.append("LASTFAILED_NODEIDS_NOT_SUBSET_OF_NODEIDS")
        if len(rows) != EXPECTED_MODULE_COUNT: reasons.append("RECOVERED_MODULE_COUNT_MISMATCH")
        if counts[:5] != EXPECTED_LARGEST_COUNTS: reasons.append("RECOVERED_LARGEST_MODULE_COUNTS_MISMATCH")
        if not rows or any(not row["module_path"] for row in rows): reasons.append("MODULE_PATHS_UNAVAILABLE")
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        cache = {"last_path": str(worktree / ".pytest_cache/v/cache/lastfailed"), "node_path": str(worktree / ".pytest_cache/v/cache/nodeids"), "last_hash": None, "node_hash": None, "last_ids": [], "node_ids": [], "last_read": False, "node_read": False, "last_parseable": False, "node_parseable": False}
        verification = _verification(cache)
        rows, reasons = [], [f"CACHE_SOURCE_UNAVAILABLE_OR_UNPARSEABLE:{type(exc).__name__}"]
    if reasons:
        artifact = {**common,
            "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1,
            "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE,
            "cache_hash_and_count_verification_report": verification,
            "module_grouping_detail_recovered": False, "module_grouping_detail_exposed": False,
            "module_paths_recovered": False, "per_module_counts_recovered": False,
            "bounded_nodeid_samples_recovered": False, "planned_outputs_generated": False,
            "blocked_reason": ";".join(reasons), "recommended_next_task": BLOCKED_NEXT_TASK,
            "module_summary_module_count": 0, "largest_module_nodeid_counts": [],
        }
        artifact["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_blocked_manifest_digest"] = semantic_digest({"blocked_reason":artifact["blocked_reason"],"verification":verification})
        return _finish(artifact, False)
    top5 = rows[:5]; top10 = rows[:10]
    top_report = {
        "top_5_module_paths": [row["module_path"] for row in top5],
        "top_5_counts": [row["failed_or_errored_nodeid_count"] for row in top5],
        "top_5_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in top5),
        "top_5_percentage_of_failed_or_errored_nodeids": f"{sum(row['failed_or_errored_nodeid_count'] for row in top5) * 100 / EXPECTED_LASTFAILED_COUNT:.8f}",
        "top_10_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in top10),
        "top_10_percentage_of_failed_or_errored_nodeids": f"{sum(row['failed_or_errored_nodeid_count'] for row in top10) * 100 / EXPECTED_LASTFAILED_COUNT:.8f}",
    }
    counts_report = {"module_count":len(rows),"total_failed_or_errored_nodeids":len(cache["last_ids"]),"deterministic_ordering":["descending failed_or_errored_nodeid_count","module_path ascending"],"module_count_rows":[{"module_path":r["module_path"],"failed_or_errored_nodeid_count":r["failed_or_errored_nodeid_count"]} for r in rows]}
    limitations = ["cache source does not distinguish assertion failures from errors","cache source does not preserve first-failure order","cache source does not provide tracebacks","recovered module grouping is planning source only","recovered detail does not prove root cause","recovered detail does not authorize retry or main merge"]
    readiness = {"recovered_detail_available_for_after_v2_planning_reentry":True,"source_recovery_results_review_required_before_reentry":True,"after_v2_planning_execution_remains_not_rerun":True,"new_retry_candidate_remains_blocked":True}
    detail_digest = semantic_digest(rows)
    manifest = {"module_grouping_detail":detail_digest,"module_counts":semantic_digest(counts_report),"top_module_source_detail":semantic_digest(top_report),"cache_verification":semantic_digest(verification),"limitations":semantic_digest(limitations),"planning_reentry_readiness":semantic_digest(readiness)}
    artifact = {**common,
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1,
        "execution_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE,
        "cache_hash_and_count_verification_report": verification,
        "module_grouping_detail_recovered": True, "module_grouping_detail_exposed": True,
        "module_paths_recovered": True, "per_module_counts_recovered": True,
        "bounded_nodeid_samples_recovered": True, "failed_or_errored_nodeids_count": len(cache["last_ids"]),
        "module_summary_module_count":len(rows), "largest_module_nodeid_counts":counts[:5],
        "deterministic_ordering":["descending failed_or_errored_nodeid_count","module_path ascending"],
        "sample_nodeids_bounded_per_module":5, "recovered_module_grouping_detail_report":rows,
        "recovered_module_counts_by_path_report":counts_report,
        "recovered_bounded_nodeid_samples_report":[{"module_path":r["module_path"],"sample_nodeids_bounded":r["sample_nodeids_bounded"]} for r in rows],
        "top_module_source_detail_report":top_report, "unsupported_claims_boundary_report":deepcopy(UNSUPPORTED_CLAIMS),
        "source_recovery_limitations_report":limitations, "planning_reentry_readiness_report":readiness,
        "module_grouping_source_recovery_manifest": {"source":"REVIEWED_DETACHED_PYTEST_CACHE_LASTFAILED","module_count":len(rows),"nodeid_count":len(cache["last_ids"])},
        "digest_manifest":manifest,
        **{f"{output_id}_generated": True for output_id in OUTPUT_IDS},
        "planned_outputs_generated":True,
        "planned_outputs":[{"output_id":output_id,"status":"GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
        "ready_for_module_grouping_source_recovery_results_review":True,
        "ready_for_after_v2_planning_reentry":False,
        "after_v2_planning_reentry_requires_results_review":True,
        "recommended_next_task":SUCCESS_NEXT_TASK,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_detail_digest":detail_digest,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_digest_manifest_digest":semantic_digest(manifest),
    }
    return _finish(artifact, True)


def validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(execution: dict) -> dict:
    if not isinstance(execution, dict): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError("execution must be object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1
    expected_kind = ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1 if success else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1
    expected_status = MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE if success else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE
    constants = {"artifact_kind":expected_kind,"execution_status":expected_status,"execution_scope":REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN,"selected_module_grouping_source_recovery_package":SELECTED_PACKAGE,"source_module_grouping_source_recovery_approval_digest":SOURCE_APPROVAL_DIGEST}
    for key,value in constants.items():
        if execution.get(key)!=value: raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError(f"{key} mismatch")
    checklist=_checklist(execution,success)
    if execution.get("checklist")!=checklist or any(item["status"]!=PASS for item in checklist): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError("checklist invalid")
    digest=execution.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest")
    if not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest) or digest!=_execution_digest(execution): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError("execution digest invalid")
    return {"artifact_kind":execution["artifact_kind"],"execution_status":execution["execution_status"],"execution_scope":execution["execution_scope"],"execution_digest":digest,**{key:execution["summary"][key] for key in ("total_checks","passed_checks","failed_checks","blocker_count")}}


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_markdown_v1(execution: dict) -> str:
    validation=validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(execution)
    sections=[("Source Approval",[SOURCE_APPROVAL_DIGEST]),("Source Blocked After-v2 Execution",[execution["blocked_reason_before_recovery"]]),("Source Classification Results Review v2",[execution["source_results_review_v2_digest"]]),("Retry Failure Context",["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]), ("Cache Verification",[str(execution["cache_hash_and_count_verification_report"])]),("Source Recovery Scope",[execution["execution_scope"]]),("Recovered Module Grouping Detail",[f"Recovered: {execution['module_grouping_detail_recovered']}"]),("Top Module Source Detail",[str(execution.get("top_module_source_detail_report",{}))]),("Unsupported Claims Boundary",[str(UNSUPPORTED_CLAIMS)]),("Success or Blocked Disposition",[execution["execution_status"]]),("Authority Boundaries",["No retry, diagnostics, remediation, integration, runtime, or trading authority."]),("Next Chain",execution["next_chain"]),("Next Gates",execution["next_gates"]),("Risk Controls",execution["risk_controls"]),("Checklist Summary",[f"{validation['passed_checks']}/{validation['total_checks']} pass."]),("Guardrails",["Cache is read-only and results review remains separate."])]
    lines=["# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Execution v1",""]
    for heading,rows in sections: lines += [f"## {heading}",*[f"- {row}" for row in rows],""]
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN",
    "execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_markdown_v1",
]
