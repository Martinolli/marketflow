"""Review the captured detached pytest-cache classification source read-only."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED_CACHE_MISMATCH_OR_BOUNDARY_VIOLATION = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED_CACHE_MISMATCH_OR_BOUNDARY_VIOLATION"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN"
)

SOURCE_OUTPUT_CAPTURE_EXECUTION_DIGEST = (
    "b7c987e76b02a026bc118ae05801e4ba02c92bdadb81df9562e28a646b4f80bb"
)
SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST = (
    "9218bad7b0b176bd3b4398293304159f22c1772fad0fa91b6e1d275a770ebcca"
)
EXPECTED_LASTFAILED_SHA256 = "24fb8cf5ce237ae6c952c29c37acaea7d22205ca885659a196f0bc27c4b1f1b1"
EXPECTED_NODEIDS_SHA256 = "9d69140fd12f57de3c14060139bc4d50a3096c29b0262c5e482af5b78ea0206d"
EXPECTED_LASTFAILED_COUNT = 1404
EXPECTED_NODEIDS_COUNT = 26288
EXPECTED_MODULE_COUNT = 29
EXPECTED_LARGEST_MODULE_COUNTS = [136, 131, 122, 112, 111]
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CLASSIFICATION_SOURCE_LIMITATIONS = [
    "pytest lastfailed does not reliably distinguish assertion failures from setup/import/runtime errors",
    "pytest lastfailed may not preserve first-failure order",
    "classification source requires results review before classification-method reentry",
    "classification source does not replace the failed authoritative retry",
]
REVIEW_OBSERVATION_IDS = [
    "source_execution_digest_bound",
    "classification_manifest_digest_bound",
    "cache_hashes_verified",
    "lastfailed_cache_reviewed",
    "nodeids_cache_reviewed",
    "module_summary_reviewed",
    "limitations_reviewed",
    "no_failure_error_separation_claimed",
    "no_first_order_claimed",
    "root_regression_not_retry_evidence",
    "retry_failure_preserved",
    "no_retry_rerun",
    "no_full_pytest",
    "no_diagnostic_command",
    "no_results_review_beyond_this_review",
    "no_integration_success",
    "cache_not_tracked",
    "marketflow_not_tracked",
]
NEXT_CHAIN = [
    "Classification Method Reentry v1.",
    "New Classification Method Candidate v2, if reentry requires new method.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "classification_method_reentry_after_output_capture_review",
    "new_classification_method_candidate_if_needed",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_reads_cache_only_for_verification",
    "review_does_not_modify_pytest_cache",
    "review_does_not_commit_pytest_cache",
    "review_does_not_commit_marketflow_outputs",
    "review_does_not_parse_operator_logs",
    "review_does_not_run_diagnostic_commands",
    "review_does_not_capture_new_output",
    "review_does_not_rerun_retry",
    "review_does_not_run_full_pytest",
    "review_does_not_treat_cache_as_retry_evidence",
    "review_does_not_replace_failed_retry_result",
    "review_does_not_create_classification_reentry",
    "review_does_not_create_new_retry_candidate",
    "review_does_not_create_retry_results_review",
    "review_does_not_create_integration_results_review",
    "review_does_not_mark_integration_successful",
    "review_does_not_generate_successful_integration_execution_digest",
    "review_does_not_generate_successful_integration_validation_digest",
    "review_does_not_stage_additional_evidence",
    "review_does_not_modify_staged_evidence",
    "review_does_not_regenerate_evidence",
    "review_does_not_call_providers",
    "review_does_not_push_integration_branch",
    "review_does_not_push_main",
    "review_does_not_delete_integration_branch",
    "review_does_not_delete_worktree",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_tags",
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
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "classification_source_requires_results_review",
    "separate_classification_reentry_required",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_execution_digest_bound",
    "source_manifest_digest_bound",
    "source_approval_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "root_regression_boundary_bound",
    "lastfailed_cache_exists_true",
    "lastfailed_cache_hash_verified",
    "lastfailed_cache_parseable_true",
    "lastfailed_entry_count_1404",
    "nodeids_cache_exists_true",
    "nodeids_cache_hash_verified",
    "nodeids_cache_parseable_true",
    "nodeids_entry_count_26288",
    "classification_source_generated_true",
    "classification_source_reviewed_true",
    "module_summary_reviewed_true",
    "module_count_29",
    "largest_module_counts_reviewed",
    "limitations_reviewed_true",
    "failure_error_separation_not_claimed_true",
    "first_failure_not_claimed_true",
    "first_error_not_claimed_true",
    "origin_main_bound",
    "integration_branch_head_bound",
    "detached_worktree_head_bound",
    "staged_evidence_digest_bound",
    "marketflow_outputs_tracked_false",
    "pytest_cache_tracked_false",
    "results_review_created_true",
    "results_review_ready_true",
    "ready_for_classification_method_reentry_true",
    "classification_method_reentry_created_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "pytest_cache_committed_false",
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
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
    ValueError
):
    """Raised when results-review evidence or boundaries are invalid."""


def _record(record_id: str, expected: Any, actual: Any, *, observation: bool = False) -> dict[str, Any]:
    passed = expected == actual
    row = {
        "status": PASS if passed else FAIL,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "message": f"{record_id} {'passed' if passed else 'failed'}",
    }
    if observation:
        row["observation_id"] = record_id
    else:
        row["check_id"] = record_id
        row["severity"] = BLOCKER
    return row


def _fixture_or_live_snapshot(
    *, repo_root: str | Path | None,
    integration_worktree_path: str | Path | None,
    cache_snapshot: dict | None,
) -> dict[str, Any]:
    if cache_snapshot is not None:
        if not isinstance(cache_snapshot, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
                "cache_snapshot must be an object"
            )
        return deepcopy(cache_snapshot)
    root = Path(repo_root).resolve(strict=False) if repo_root is not None else source.EXPECTED_REPO_ROOT
    worktree = (
        Path(integration_worktree_path).resolve(strict=False)
        if integration_worktree_path is not None
        else source.EXPECTED_INTEGRATION_WORKTREE.resolve(strict=False)
    )
    before = source._snapshot(root, worktree)
    cache = source._cache_capture(worktree, allow_read=True)
    after = source._snapshot(root, worktree)
    root_cache = source._git(root, "ls-files", ".pytest_cache")
    worktree_cache = source._git(worktree, "ls-files", ".pytest_cache")
    snapshot = {
        **cache,
        "origin_main_commit": before.get("origin_main_commit"),
        "integration_branch_head_commit": before.get("integration_branch_head_commit"),
        "remote_integration_branch_exists": before.get("remote_integration_branch_exists"),
        "detached_integration_worktree_path": before.get("detached_integration_worktree_path"),
        "detached_integration_worktree_head_commit": before.get("detached_integration_worktree_head_commit"),
        "detached_integration_worktree_is_detached": before.get("detached_integration_worktree_is_detached"),
        "detached_integration_worktree_clean_at_review": before.get("detached_integration_worktree_clean") and after.get("detached_integration_worktree_clean"),
        "staged_evidence_manifest_digest": after.get("staged_evidence_manifest_digest"),
        "staged_evidence_unchanged": before.get("staged_evidence_manifest_digest") == after.get("staged_evidence_manifest_digest") == source.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "marketflow_outputs_tracked_in_repository": after.get("repository_tracked_marketflow_count") != 0,
        "marketflow_outputs_tracked_in_detached_worktree": after.get("worktree_tracked_marketflow_count") != 0,
        "pytest_cache_tracked_in_repository": root_cache.returncode != 0 or bool(root_cache.stdout.splitlines()),
        "pytest_cache_tracked_in_detached_worktree": worktree_cache.returncode != 0 or bool(worktree_cache.stdout.splitlines()),
    }
    source_execution_shape = {
        **snapshot,
        "classification_source_limitations": source.CLASSIFICATION_SOURCE_LIMITATIONS if hasattr(source, "CLASSIFICATION_SOURCE_LIMITATIONS") else [
            "pytest lastfailed does not distinguish assertion failure from error unless additional source supports it",
            "pytest lastfailed may not preserve first-failure order",
            "classification source requires results review before reentry",
        ],
    }
    snapshot["recomputed_source_classification_manifest_digest"] = (
        source.marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1(
            source_execution_shape
        )
    )
    return snapshot


def _source_fields() -> dict[str, Any]:
    fields = source._source_fields()
    return {
        "source_output_capture_execution_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED,
        "source_output_capture_execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED,
        "source_output_capture_execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_output_capture_execution_digest": SOURCE_OUTPUT_CAPTURE_EXECUTION_DIGEST,
        "source_classification_source_manifest_digest": SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST,
        **fields,
    }


def _review_passes(snapshot: Mapping[str, Any]) -> bool:
    module_counts = [row.get("nodeid_count") for row in snapshot.get("module_summary", [])[:5]]
    return all(
        (
            snapshot.get("lastfailed_cache_exists") is True,
            snapshot.get("lastfailed_cache_read") is True,
            snapshot.get("lastfailed_cache_parseable_json") is True,
            snapshot.get("lastfailed_cache_sha256") == EXPECTED_LASTFAILED_SHA256,
            snapshot.get("lastfailed_cache_entry_count") == EXPECTED_LASTFAILED_COUNT,
            snapshot.get("lastfailed_nodeids_extracted") is True,
            snapshot.get("nodeids_cache_exists") is True,
            snapshot.get("nodeids_cache_read") is True,
            snapshot.get("nodeids_cache_parseable_json") is True,
            snapshot.get("nodeids_cache_sha256") == EXPECTED_NODEIDS_SHA256,
            snapshot.get("nodeids_cache_entry_count") == EXPECTED_NODEIDS_COUNT,
            snapshot.get("module_summary_generated") is True,
            snapshot.get("module_summary_total_modules") == EXPECTED_MODULE_COUNT,
            snapshot.get("module_summary_truncated") is False,
            module_counts == EXPECTED_LARGEST_MODULE_COUNTS,
            snapshot.get("origin_main_commit") == source.EXPECTED_ORIGIN_MAIN_COMMIT,
            snapshot.get("integration_branch_head_commit") == source.INTEGRATION_HEAD_COMMIT,
            snapshot.get("remote_integration_branch_exists") is False,
            snapshot.get("detached_integration_worktree_head_commit") == source.INTEGRATION_HEAD_COMMIT,
            snapshot.get("detached_integration_worktree_is_detached") is True,
            snapshot.get("detached_integration_worktree_clean_at_review") is True,
            snapshot.get("staged_evidence_manifest_digest") == source.EXPECTED_STAGED_EVIDENCE_DIGEST,
            snapshot.get("staged_evidence_unchanged") is True,
            snapshot.get("marketflow_outputs_tracked_in_repository") is False,
            snapshot.get("marketflow_outputs_tracked_in_detached_worktree") is False,
            snapshot.get("pytest_cache_tracked_in_repository") is False,
            snapshot.get("pytest_cache_tracked_in_detached_worktree") is False,
            snapshot.get("recomputed_source_classification_manifest_digest", SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST) == SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST,
        )
    )


def _base_review(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    ready = _review_passes(snapshot)
    module_counts = [row.get("nodeid_count") for row in snapshot.get("module_summary", [])[:5]]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1
            if ready
            else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED
        ),
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1,
        "review_status": (
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY
            if ready
            else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED_CACHE_MISMATCH_OR_BOUNDARY_VIOLATION
        ),
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN,
        "created_offline_except_read_only_cache_and_file_inspection": True,
        "governance_only": True,
        "results_review_only": True,
        **_source_fields(),
        "retry_pytest_working_directory": str(source.EXPECTED_INTEGRATION_WORKTREE.resolve(strict=False)),
        "retry_pytest_ran_from_detached_worktree": True,
        "retry_pytest_performed": True,
        "retry_pytest_exit_code": 1,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_does_not_override_detached_retry_failure": True,
        "lastfailed_cache_path": snapshot.get("lastfailed_cache_path"),
        "lastfailed_cache_exists_at_review": snapshot.get("lastfailed_cache_exists"),
        "lastfailed_cache_read_for_review": snapshot.get("lastfailed_cache_read"),
        "lastfailed_cache_parseable_json_at_review": snapshot.get("lastfailed_cache_parseable_json"),
        "lastfailed_cache_sha256_at_review": snapshot.get("lastfailed_cache_sha256"),
        "lastfailed_cache_entry_count_at_review": snapshot.get("lastfailed_cache_entry_count"),
        "lastfailed_nodeids_reviewed": snapshot.get("lastfailed_nodeids_extracted") is True and ready,
        "nodeids_cache_path": snapshot.get("nodeids_cache_path"),
        "nodeids_cache_exists_at_review": snapshot.get("nodeids_cache_exists"),
        "nodeids_cache_read_for_review": snapshot.get("nodeids_cache_read"),
        "nodeids_cache_parseable_json_at_review": snapshot.get("nodeids_cache_parseable_json"),
        "nodeids_cache_sha256_at_review": snapshot.get("nodeids_cache_sha256"),
        "nodeids_cache_entry_count_at_review": snapshot.get("nodeids_cache_entry_count"),
        "classification_source_generated": ready,
        "classification_source_reviewed": ready,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED" if ready else None,
        "classification_source_contains_nodeids": ready,
        "cache_treated_as_retry_evidence": False,
        "failed_or_errored_nodeids_count_reviewed": snapshot.get("failed_or_errored_nodeids_count"),
        "module_summary_generated": snapshot.get("module_summary_generated"),
        "module_summary_reviewed": ready,
        "module_summary_module_count": snapshot.get("module_summary_total_modules"),
        "module_summary_untruncated": snapshot.get("module_summary_truncated") is False,
        "largest_module_nodeid_counts_reviewed": module_counts,
        "classification_source_can_distinguish_failures_from_errors": False,
        "failure_error_separation_not_claimed": True,
        "first_failure_identified": False,
        "first_error_identified": False,
        "first_failure_or_error_order_not_claimed": True,
        "ordering_limitation_reviewed": ready,
        "classification_source_limitations": list(CLASSIFICATION_SOURCE_LIMITATIONS),
        "classification_source_limitations_reviewed": ready,
        "origin_main_commit": snapshot.get("origin_main_commit"),
        "integration_branch_name": source.INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": snapshot.get("integration_branch_head_commit"),
        "remote_integration_branch_exists": snapshot.get("remote_integration_branch_exists"),
        "detached_integration_worktree_path": snapshot.get("detached_integration_worktree_path"),
        "detached_integration_worktree_head_commit": snapshot.get("detached_integration_worktree_head_commit"),
        "detached_integration_worktree_is_detached": snapshot.get("detached_integration_worktree_is_detached"),
        "detached_integration_worktree_clean_at_review": snapshot.get("detached_integration_worktree_clean_at_review"),
        "staged_evidence_manifest_digest": snapshot.get("staged_evidence_manifest_digest"),
        "staged_evidence_unchanged": snapshot.get("staged_evidence_unchanged"),
        "marketflow_outputs_tracked_in_repository": snapshot.get("marketflow_outputs_tracked_in_repository"),
        "marketflow_outputs_tracked_in_detached_worktree": snapshot.get("marketflow_outputs_tracked_in_detached_worktree"),
        "pytest_cache_tracked_in_repository": snapshot.get("pytest_cache_tracked_in_repository"),
        "pytest_cache_tracked_in_detached_worktree": snapshot.get("pytest_cache_tracked_in_detached_worktree"),
        "classification_source_results_review_created": True,
        "classification_source_results_review_ready": ready,
        "lastfailed_cache_reviewed": ready,
        "nodeids_cache_reviewed": ready,
        "ready_for_classification_method_reentry": ready,
        "classification_method_reentry_created": False,
        "new_classification_method_candidate_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "integration_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
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
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": snapshot.get("marketflow_outputs_tracked_in_repository") is False and snapshot.get("marketflow_outputs_tracked_in_detached_worktree") is False,
        "no_tracked_pytest_cache_files": snapshot.get("pytest_cache_tracked_in_repository") is False and snapshot.get("pytest_cache_tracked_in_detached_worktree") is False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK if ready else "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_REVIEW_REMEDIATION_V1",
    }


def _observations(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "source_execution_digest_bound": (SOURCE_OUTPUT_CAPTURE_EXECUTION_DIGEST, review.get("source_output_capture_execution_digest")),
        "classification_manifest_digest_bound": (SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST, review.get("source_classification_source_manifest_digest")),
        "cache_hashes_verified": ([EXPECTED_LASTFAILED_SHA256, EXPECTED_NODEIDS_SHA256], [review.get("lastfailed_cache_sha256_at_review"), review.get("nodeids_cache_sha256_at_review")]),
        "lastfailed_cache_reviewed": (True, review.get("lastfailed_cache_reviewed")),
        "nodeids_cache_reviewed": (True, review.get("nodeids_cache_reviewed")),
        "module_summary_reviewed": (True, review.get("module_summary_reviewed")),
        "limitations_reviewed": (True, review.get("classification_source_limitations_reviewed")),
        "no_failure_error_separation_claimed": (True, review.get("failure_error_separation_not_claimed")),
        "no_first_order_claimed": (True, review.get("first_failure_or_error_order_not_claimed")),
        "root_regression_not_retry_evidence": (False, review.get("root_full_regression_is_retry_evidence")),
        "retry_failure_preserved": ([False, True], [review.get("retry_pytest_passed"), review.get("retry_pytest_failed")]),
        "no_retry_rerun": (False, review.get("retry_rerun_performed")),
        "no_full_pytest": (False, review.get("full_pytest_performed")),
        "no_diagnostic_command": (False, review.get("diagnostic_command_executed")),
        "no_results_review_beyond_this_review": ([False, False], [review.get("new_retry_results_review_created"), review.get("integration_results_review_created")]),
        "no_integration_success": (False, review.get("integration_execution_successful")),
        "cache_not_tracked": (True, review.get("no_tracked_pytest_cache_files")),
        "marketflow_not_tracked": (True, review.get("no_tracked_marketflow_files")),
    }
    return [_record(observation_id, *values[observation_id], observation=True) for observation_id in REVIEW_OBSERVATION_IDS]


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    values: dict[str, tuple[Any, Any]] = {
        "source_execution_digest_bound": (SOURCE_OUTPUT_CAPTURE_EXECUTION_DIGEST, review.get("source_output_capture_execution_digest")),
        "source_manifest_digest_bound": (SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST, review.get("source_classification_source_manifest_digest")),
        "source_approval_digest_bound": (source.SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST, review.get("source_output_capture_approval_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], counts),
        "root_regression_boundary_bound": ([False, True], [review.get("root_full_regression_is_retry_evidence"), review.get("root_full_regression_does_not_override_detached_retry_failure")]),
        "lastfailed_cache_exists_true": (True, review.get("lastfailed_cache_exists_at_review")),
        "lastfailed_cache_hash_verified": (EXPECTED_LASTFAILED_SHA256, review.get("lastfailed_cache_sha256_at_review")),
        "lastfailed_cache_parseable_true": (True, review.get("lastfailed_cache_parseable_json_at_review")),
        "lastfailed_entry_count_1404": (EXPECTED_LASTFAILED_COUNT, review.get("lastfailed_cache_entry_count_at_review")),
        "nodeids_cache_exists_true": (True, review.get("nodeids_cache_exists_at_review")),
        "nodeids_cache_hash_verified": (EXPECTED_NODEIDS_SHA256, review.get("nodeids_cache_sha256_at_review")),
        "nodeids_cache_parseable_true": (True, review.get("nodeids_cache_parseable_json_at_review")),
        "nodeids_entry_count_26288": (EXPECTED_NODEIDS_COUNT, review.get("nodeids_cache_entry_count_at_review")),
        "classification_source_generated_true": (True, review.get("classification_source_generated")),
        "classification_source_reviewed_true": (True, review.get("classification_source_reviewed")),
        "module_summary_reviewed_true": (True, review.get("module_summary_reviewed")),
        "module_count_29": (EXPECTED_MODULE_COUNT, review.get("module_summary_module_count")),
        "largest_module_counts_reviewed": (EXPECTED_LARGEST_MODULE_COUNTS, review.get("largest_module_nodeid_counts_reviewed")),
        "limitations_reviewed_true": (True, review.get("classification_source_limitations_reviewed")),
        "failure_error_separation_not_claimed_true": ([False, True], [review.get("classification_source_can_distinguish_failures_from_errors"), review.get("failure_error_separation_not_claimed")]),
        "first_failure_not_claimed_true": (False, review.get("first_failure_identified")),
        "first_error_not_claimed_true": (False, review.get("first_error_identified")),
        "origin_main_bound": (source.EXPECTED_ORIGIN_MAIN_COMMIT, review.get("origin_main_commit")),
        "integration_branch_head_bound": (source.INTEGRATION_HEAD_COMMIT, review.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": (source.INTEGRATION_HEAD_COMMIT, review.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": (source.EXPECTED_STAGED_EVIDENCE_DIGEST, review.get("staged_evidence_manifest_digest")),
        "marketflow_outputs_tracked_false": ([False, False], [review.get("marketflow_outputs_tracked_in_repository"), review.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "pytest_cache_tracked_false": ([False, False], [review.get("pytest_cache_tracked_in_repository"), review.get("pytest_cache_tracked_in_detached_worktree")]),
        "results_review_created_true": (True, review.get("classification_source_results_review_created")),
        "results_review_ready_true": (True, review.get("classification_source_results_review_ready")),
        "ready_for_classification_method_reentry_true": (True, review.get("ready_for_classification_method_reentry")),
        "classification_method_reentry_created_false": (False, review.get("classification_method_reentry_created")),
        "new_retry_candidate_created_false": (False, review.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, review.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, review.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, review.get("main_merge_approval_created")),
        "retry_rerun_false": (False, review.get("retry_rerun_performed")),
        "full_pytest_false": (False, review.get("full_pytest_performed")),
        "diagnostic_command_false": (False, review.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, review.get("diagnostic_output_captured")),
        "integration_success_false": (False, review.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, review.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
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
        "no_tracked_pytest_cache_files": (True, review.get("no_tracked_pytest_cache_files")),
    }
    return [_record(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "classification_source_results_review_created": True,
        "classification_source_results_review_ready": review.get("classification_source_results_review_ready"),
        "classification_source_reviewed": review.get("classification_source_reviewed"),
        "lastfailed_cache_reviewed": review.get("lastfailed_cache_reviewed"),
        "nodeids_cache_reviewed": review.get("nodeids_cache_reviewed"),
        "module_summary_reviewed": review.get("module_summary_reviewed"),
        "ready_for_classification_method_reentry": review.get("ready_for_classification_method_reentry"),
        "classification_method_reentry_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": review.get("recommended_next_task"),
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest_v1(
    review: Mapping[str, Any],
) -> str:
    fields = {
        key: deepcopy(review.get(key))
        for key in (
            "lastfailed_cache_path", "lastfailed_cache_sha256_at_review",
            "lastfailed_cache_entry_count_at_review", "nodeids_cache_path",
            "nodeids_cache_sha256_at_review", "nodeids_cache_entry_count_at_review",
            "failed_or_errored_nodeids_count_reviewed", "module_summary_module_count",
            "largest_module_nodeid_counts_reviewed", "classification_source_limitations",
        )
    }
    return semantic_digest(fields)


def marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in (
        "review_observations",
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
    *, repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    cache_snapshot: dict | None = None,
) -> dict:
    """Build a review from a deterministic snapshot or live read-only verification."""
    snapshot = _fixture_or_live_snapshot(
        repo_root=repo_root,
        integration_worktree_path=integration_worktree_path,
        cache_snapshot=cache_snapshot,
    )
    review = _base_review(snapshot)
    review["review_observations"] = _observations(review)
    review[
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest"
    ] = marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest_v1(
        review
    )
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review[
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest"
    ] = marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        review
    )
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
    review: dict,
) -> dict:
    """Validate a ready review or a fail-closed blocked review."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "review must be an object"
        )
    ready = review.get("classification_source_results_review_ready") is True
    _expect(
        review.get("artifact_kind"),
        ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1
        if ready
        else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED,
        "artifact_kind",
    )
    _expect(
        review.get("review_status"),
        MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY
        if ready
        else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED_CACHE_MISMATCH_OR_BOUNDARY_VIOLATION,
        "review_status",
    )
    static = {
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN,
        **_source_fields(),
        "risk_controls": RISK_CONTROLS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
    }
    for field, expected in static.items():
        _expect(review.get(field), expected, field)
    for field in (
        "created_offline_except_read_only_cache_and_file_inspection",
        "governance_only",
        "results_review_only",
        "classification_source_results_review_created",
        "failure_error_separation_not_claimed",
        "first_failure_or_error_order_not_claimed",
        "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "root_full_regression_is_retry_evidence",
        "cache_treated_as_retry_evidence",
        "classification_source_can_distinguish_failures_from_errors",
        "first_failure_identified",
        "first_error_identified",
        "classification_method_reentry_created",
        "new_classification_method_candidate_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    if ready:
        ready_static = {
            "lastfailed_cache_exists_at_review": True,
            "lastfailed_cache_read_for_review": True,
            "lastfailed_cache_parseable_json_at_review": True,
            "lastfailed_cache_sha256_at_review": EXPECTED_LASTFAILED_SHA256,
            "lastfailed_cache_entry_count_at_review": EXPECTED_LASTFAILED_COUNT,
            "nodeids_cache_exists_at_review": True,
            "nodeids_cache_read_for_review": True,
            "nodeids_cache_parseable_json_at_review": True,
            "nodeids_cache_sha256_at_review": EXPECTED_NODEIDS_SHA256,
            "nodeids_cache_entry_count_at_review": EXPECTED_NODEIDS_COUNT,
            "classification_source_generated": True,
            "classification_source_reviewed": True,
            "module_summary_generated": True,
            "module_summary_reviewed": True,
            "module_summary_module_count": EXPECTED_MODULE_COUNT,
            "module_summary_untruncated": True,
            "largest_module_nodeid_counts_reviewed": EXPECTED_LARGEST_MODULE_COUNTS,
            "classification_source_limitations_reviewed": True,
            "lastfailed_cache_reviewed": True,
            "nodeids_cache_reviewed": True,
            "ready_for_classification_method_reentry": True,
        }
        for field, expected in ready_static.items():
            _expect(review.get(field), expected, field)
    observations = review.get("review_observations")
    if not isinstance(observations, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "review_observations missing"
        )
    _expect(observations, _observations(review), "review_observations")
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "checklist missing"
        )
    _expect(checklist, _checklist(review), "checklist")
    if ready and any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "ready review checklist failed"
        )
    _expect(review.get("summary"), _summary(review, checklist), "summary")
    cache_digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest"
    )
    if not isinstance(cache_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", cache_digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "cache manifest digest missing"
        )
    _expect(
        cache_digest,
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest_v1(
            review
        ),
        "cache manifest digest",
    )
    digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest_v1(
            review
        ),
        "review digest",
    )
    return {
        "artifact_kind": review["artifact_kind"],
        "status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest": digest,
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest": cache_digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated results review as Markdown."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        review
    )
    sections = [
        ("Source Execution", [f"Execution digest: `{review['source_output_capture_execution_digest']}`.", f"Classification-source manifest: `{review['source_classification_source_manifest_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry remains `24877 passed, 1292 failed, 112 errors, 7 skipped`."]),
        ("Cache Review", [f"Lastfailed hash/count: `{review['lastfailed_cache_sha256_at_review']}` / `{review['lastfailed_cache_entry_count_at_review']}`.", f"Nodeids hash/count: `{review['nodeids_cache_sha256_at_review']}` / `{review['nodeids_cache_entry_count_at_review']}`."]),
        ("Classification Source Review", [f"Reviewed: `{review['classification_source_reviewed']}`; modules: `{review['module_summary_module_count']}`; ready for reentry: `{review['ready_for_classification_method_reentry']}`."]),
        ("Limitations", review["classification_source_limitations"]),
        ("Authority Boundaries", ["No classification reentry, retry, results review beyond this artifact, integration success, runtime, or trading authority is created."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Cache verification is read-only and not retry evidence.", "Classification-method reentry requires a separate task."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Results Review v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
    output_dir: str | Path,
    *, repo_root: str | Path | None = None,
    integration_worktree_path: str | Path | None = None,
    cache_snapshot: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting existing output."""
    review = build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        repo_root=repo_root,
        integration_worktree_path=integration_worktree_path,
        cache_snapshot=cache_snapshot,
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError(
            "results-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
