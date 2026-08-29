"""Read-only review of the four published repository governance tags."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_tag_push_execution_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1 = (
    "marketflow_repository_tag_push_results_review_v1"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED_REMOTE_TAG_MISMATCH_OR_ORIGIN_MAIN_CHANGE = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED_REMOTE_TAG_MISMATCH_OR_ORIGIN_MAIN_CHANGE"
)
REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_VALID"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "2c74d2c3e845836585aa680f97a248bfd9a80eca0a87ffb70956beebc2bd21d4"
)
EXPECTED_SOURCE_REMOTE_TAG_MANIFEST_DIGEST = (
    "b2679a3c2b8b2aad8ec3723a57500ad88434a011e7d28eb6d8a0934abb1864e2"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_TAGGING_EXECUTION_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST
EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST
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
EXPECTED_SOURCE_EXECUTION_COMMIT = "b247b82a6d1863dc127968f91dc6b91757fdbe51"
EXPECTED_TAGS = deepcopy(source_service.APPROVED_TAGS)
EXPECTED_REMOTE_REFS = [row["remote_ref"] for row in EXPECTED_TAGS]
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
MESSAGE_BOUNDARIES = [
    "MarketFlow research governance milestone",
    "Predictive usefulness: NOT_ACCEPTED",
    "Profitability: NOT_ACCEPTED",
    "Runtime: NOT_AUTHORIZED",
    "Trading/Broker: NOT_AUTHORIZED",
    "No trade recommendation is created by this tag",
]

NEXT_CHAIN = [
    "Repository Merge Strategy Candidate v1.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]
NEXT_GATES = [
    "repository_merge_strategy_candidate_after_tag_push_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]
RISK_CONTROLS = [
    "review_does_not_push_tags", "review_does_not_push_all_tags",
    "review_does_not_push_branches", "review_does_not_push_main",
    "review_does_not_force_push", "review_does_not_create_additional_tags",
    "review_does_not_modify_tags", "review_does_not_delete_tags",
    "review_does_not_delete_remote_tags", "review_does_not_merge",
    "review_does_not_rebase", "review_does_not_delete_branches",
    "review_does_not_delete_remote_branches", "review_does_not_prune_remotes",
    "review_does_not_modify_origin_main", "review_does_not_modify_marketflow_outputs",
    "review_does_not_call_providers", "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset", "review_does_not_rerun_tag_push_execution",
    "review_does_not_rerun_tag_push_approval", "review_does_not_rerun_tag_push_operator_review",
    "review_does_not_rerun_tag_push_candidate", "review_does_not_rerun_inventory",
    "review_does_not_rerun_evidence", "review_does_not_recompute_metrics",
    "review_does_not_train_models", "review_does_not_score_strategy",
    "review_does_not_generate_recommendations", "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability", "review_does_not_authorize_runtime",
    "review_does_not_authorize_broker_execution", "remote_mismatch_blocks_review",
    "extra_remote_namespace_tag_blocks_review", "protect_origin_main",
    "preserve_terminal_archive_evidence", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_remote_manifest_digest_bound",
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_tagging_results_review_digest_bound",
    "source_tag_manifest_review_digest_bound", "source_tagging_execution_digest_bound",
    "source_tagging_execution_manifest_digest_bound", "source_tagging_approval_digest_bound",
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound",
    "origin_main_before_bound", "origin_main_after_bound", "origin_main_review_unchanged",
    "source_execution_status_bound", "results_review_created_true",
    "results_review_ready_true", "remote_tags_reviewed_true",
    "remote_targets_reviewed_true", "remote_objects_reviewed_true",
    "remote_manifest_reviewed_true", "ready_for_merge_strategy_candidate_true",
    "remote_candidate_namespace_tag_count_at_review_4",
    "remote_approved_tag_count_at_review_4", "verified_remote_terminal_tag_count_4",
    "extra_remote_candidate_namespace_tag_count_zero", "remote_tag_names_match",
    "remote_tag_object_shas_match", "remote_peeled_target_commits_match",
    "local_tags_still_match_source", "local_tag_messages_verified",
    "remote_publication_complete", "explicit_refspec_push_confirmed",
    "push_all_tags_false", "branch_push_false", "main_push_false",
    "force_push_false", "additional_tag_push_false",
    "repository_tags_pushed_again_false", "additional_tags_created_false",
    "tags_modified_false", "tags_deleted_false", "merge_performed_false",
    "rebase_performed_false", "branch_delete_performed_false",
    "remote_delete_performed_false", "remote_prune_false",
    "origin_main_modified_false", "marketflow_outputs_not_tracked",
    "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryTagPushResultsReviewError(ValueError):
    """Raised when remote publication review evidence is invalid."""


def _local_tag_snapshot(repo_root: Path, expected: Mapping[str, str]) -> dict[str, Any]:
    ref = expected["remote_ref"]
    object_sha = source_service._git(repo_root, "rev-parse", "--verify", ref)
    raw = source_service._git(repo_root, "cat-file", "-p", object_sha)
    message = raw.split("\n\n", 1)[1].rstrip("\n") if "\n\n" in raw else ""
    return {
        "object_type": source_service._git(repo_root, "cat-file", "-t", object_sha),
        "object_sha": object_sha,
        "target_commit": source_service._git(repo_root, "rev-parse", f"{ref}^{{}}"),
        "message": message,
    }


def _read_git_snapshot(repo_root: Path) -> dict[str, Any]:
    return {
        "origin_main_commit": source_service._origin_main(repo_root),
        "tracked_marketflow_file_count": source_service._tracked_marketflow_count(repo_root),
        "local_tag_count": source_service._local_tag_count(repo_root),
        "remote_tags": source_service._remote_tags(repo_root),
        "local_tags": {
            row["tag_name"]: _local_tag_snapshot(repo_root, row) for row in EXPECTED_TAGS
        },
    }


def approved_marketflow_repository_tag_push_results_review_git_snapshot_v1() -> dict[str, Any]:
    """Return the deterministic approved snapshot used by offline tests."""
    return {
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "tracked_marketflow_file_count": 0,
        "local_tag_count": 32,
        "remote_tags": {
            row["remote_ref"]: {
                "object_sha": row["local_tag_object_sha"],
                "peeled_target": row["target_commit"],
            }
            for row in EXPECTED_TAGS
        },
        "local_tags": {
            row["tag_name"]: {
                "object_type": "tag", "object_sha": row["local_tag_object_sha"],
                "target_commit": row["target_commit"], "message": row["tag_message"],
            }
            for row in EXPECTED_TAGS
        },
    }


def _snapshot_problems(snapshot: Mapping[str, Any]) -> list[str]:
    problems = []
    if snapshot.get("origin_main_commit") != EXPECTED_ORIGIN_MAIN_COMMIT:
        problems.append("origin/main changed")
    remote = snapshot.get("remote_tags", {})
    if set(remote) != set(EXPECTED_REMOTE_REFS):
        problems.append("remote namespace differs from four approved refs")
    local = snapshot.get("local_tags", {})
    for expected in EXPECTED_TAGS:
        observed_remote = remote.get(expected["remote_ref"], {})
        if observed_remote.get("object_sha") != expected["local_tag_object_sha"]:
            problems.append(f"remote object mismatch: {expected['tag_name']}")
        if observed_remote.get("peeled_target") != expected["target_commit"]:
            problems.append(f"remote target mismatch: {expected['tag_name']}")
        observed_local = local.get(expected["tag_name"], {})
        if observed_local.get("object_type") != "tag":
            problems.append(f"local tag is not annotated: {expected['tag_name']}")
        if observed_local.get("object_sha") != expected["local_tag_object_sha"]:
            problems.append(f"local object mismatch: {expected['tag_name']}")
        if observed_local.get("target_commit") != expected["target_commit"]:
            problems.append(f"local target mismatch: {expected['tag_name']}")
        message = observed_local.get("message", "")
        if message != expected["tag_message"] or not all(boundary in message for boundary in MESSAGE_BOUNDARIES):
            problems.append(f"local tag message mismatch: {expected['tag_name']}")
    if snapshot.get("tracked_marketflow_file_count") != 0:
        problems.append("tracked .marketflow files detected")
    return problems


def _review_records(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    remote = snapshot["remote_tags"]
    local = snapshot["local_tags"]
    records = []
    for expected in EXPECTED_TAGS:
        remote_row = remote[expected["remote_ref"]]
        local_row = local[expected["tag_name"]]
        records.append({
            "tag_name": expected["tag_name"], "remote_ref": expected["remote_ref"],
            "expected_remote_tag_object_sha": expected["local_tag_object_sha"],
            "observed_remote_tag_object_sha": remote_row["object_sha"],
            "expected_remote_peeled_target_commit": expected["target_commit"],
            "observed_remote_peeled_target_commit": remote_row["peeled_target"],
            "local_tag_object_sha": local_row["object_sha"],
            "local_target_commit": local_row["target_commit"],
            "source_artifact_kind": expected["source_artifact_kind"],
            "source_digest": expected["source_digest"],
            "remote_ref_exists": True, "remote_tag_object_sha_verified": True,
            "remote_peeled_target_commit_verified": True,
            "local_tag_still_matches_source": True, "tag_message_verified_locally": True,
            "remote_review_status": "VERIFIED_REMOTE_TAG_PUBLISHED_TO_ORIGIN",
            "tag_pushed_by_source_execution": True,
            "additional_push_performed_by_review": False,
            "tag_modified_by_review": False, "tag_deleted_by_review": False,
            "predictive_usefulness_accepted": False, "profitability_accepted": False,
            "runtime_authority_created": False, "trade_recommendations_generated": False,
        })
    return records


def _base_review(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    records = _review_records(snapshot)
    messages = [snapshot["local_tags"][row["tag_name"]]["message"] for row in EXPECTED_TAGS]
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline_except_read_only_git_remote_inspection": True,
        "planning_only": True, "governance_only": True,
        "source_tag_push_execution_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED,
        "source_tag_push_execution_status": source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED,
        "source_tag_push_execution_scope": source_service.REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tag_push_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_remote_tag_manifest_digest": EXPECTED_SOURCE_REMOTE_TAG_MANIFEST_DIGEST,
        "source_tag_push_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_tag_push_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST,
        "source_tagging_execution_tag_manifest_digest": EXPECTED_SOURCE_TAGGING_EXECUTION_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST,
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
        "origin_main_commit_before_execution": EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_commit_after_execution": EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_commit_at_review": snapshot["origin_main_commit"],
        "source_execution_commit": EXPECTED_SOURCE_EXECUTION_COMMIT,
        "source_repository_context": {
            "before_execution_feature_push": {"local_branch_count": 299, "remote_branch_count": 271, "total_ref_count": 570},
            "after_execution_feature_push": {"local_branch_count": 300, "remote_branch_count": 272, "total_ref_count": 572},
            "local_tag_count": snapshot["local_tag_count"],
        },
        "repository_tag_push_results_review_created": True,
        "repository_tag_push_results_review_ready": True,
        "remote_tags_reviewed": True, "remote_tag_targets_reviewed": True,
        "remote_tag_objects_reviewed": True, "remote_tag_manifest_reviewed": True,
        "ready_for_repository_merge_strategy_candidate": True,
        "remote_tag_review_records": records,
        "remote_tag_count_review": {
            "remote_candidate_namespace_tag_count_before_source_push": 0,
            "remote_candidate_namespace_tag_count_after_source_push": 4,
            "remote_candidate_namespace_tag_count_at_review": len(snapshot["remote_tags"]),
            "remote_approved_tag_count_at_review": len(records),
            "verified_remote_terminal_tag_count": len(records),
            "extra_remote_candidate_namespace_tag_count_at_review": 0,
            "remote_tag_count_observation_note": "Four approved remote tags verified; no extra namespace tags observed.",
        },
        "tag_message_review": {
            "all_local_tag_messages_include_governance_milestone": all(MESSAGE_BOUNDARIES[0] in message for message in messages),
            "all_local_tag_messages_include_not_accepted_predictive_usefulness": all(MESSAGE_BOUNDARIES[1] in message for message in messages),
            "all_local_tag_messages_include_not_accepted_profitability": all(MESSAGE_BOUNDARIES[2] in message for message in messages),
            "all_local_tag_messages_include_not_authorized_runtime": all(MESSAGE_BOUNDARIES[3] in message for message in messages),
            "all_local_tag_messages_include_not_authorized_trading_broker": all(MESSAGE_BOUNDARIES[4] in message for message in messages),
            "all_local_tag_messages_include_no_trade_recommendation": all(MESSAGE_BOUNDARIES[5] in message for message in messages),
        },
        "remote_publication_review": {
            "remote_publication_review_status": "VERIFIED_REMOTE_PUBLICATION_COMPLETE",
            "explicit_refspec_push_confirmed_from_source": True,
            "push_all_tags_not_used": True, "branch_push_not_used": True,
            "main_push_not_used": True, "force_push_not_used": True,
            "origin_main_unchanged": True,
        },
        "additional_tag_push_performed": False, "repository_tags_pushed_again": False,
        "additional_tags_created": False, "tags_modified": False, "tags_deleted": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_main_push_performed": False, "git_force_push_performed": False,
        "git_remote_prune_performed": False, "origin_main_modified_by_this_task": False,
        "repository_merge_strategy_candidate_created": False,
        "repository_cleanup_candidate_created": False, "repository_cleanup_executed": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": snapshot["tracked_marketflow_file_count"],
        "no_tracked_marketflow_files": snapshot["tracked_marketflow_file_count"] == 0,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    records = review.get("remote_tag_review_records", [])
    counts = review.get("remote_tag_count_review", {})
    messages = review.get("tag_message_review", {})
    publication = review.get("remote_publication_review", {})
    pairs = list(zip(records, EXPECTED_TAGS)) if len(records) == 4 else []
    return {
        "source_execution_digest_bound": review.get("source_tag_push_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_remote_manifest_digest_bound": review.get("source_remote_tag_manifest_digest") == EXPECTED_SOURCE_REMOTE_TAG_MANIFEST_DIGEST,
        "source_approval_digest_bound": review.get("source_tag_push_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": review.get("source_tag_push_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": review.get("source_tag_push_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest_bound": review.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest_bound": review.get("source_tag_manifest_review_digest") == EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest_bound": review.get("source_tagging_execution_digest") == EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST,
        "source_tagging_execution_manifest_digest_bound": review.get("source_tagging_execution_tag_manifest_digest") == EXPECTED_SOURCE_TAGGING_EXECUTION_MANIFEST_DIGEST,
        "source_tagging_approval_digest_bound": review.get("source_tagging_approval_digest") == EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST,
        "source_inventory_plan_digest_bound": review.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": review.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": review.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": review.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": review.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": review.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": review.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest_bound": review.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": review.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_before_bound": review.get("origin_main_commit_before_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_after_bound": review.get("origin_main_commit_after_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_review_unchanged": review.get("origin_main_commit_at_review") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_execution_status_bound": review.get("source_tag_push_execution_status") == source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED,
        "results_review_created_true": review.get("repository_tag_push_results_review_created") is True,
        "results_review_ready_true": review.get("repository_tag_push_results_review_ready") is True,
        "remote_tags_reviewed_true": review.get("remote_tags_reviewed") is True,
        "remote_targets_reviewed_true": review.get("remote_tag_targets_reviewed") is True,
        "remote_objects_reviewed_true": review.get("remote_tag_objects_reviewed") is True,
        "remote_manifest_reviewed_true": review.get("remote_tag_manifest_reviewed") is True,
        "ready_for_merge_strategy_candidate_true": review.get("ready_for_repository_merge_strategy_candidate") is True,
        "remote_candidate_namespace_tag_count_at_review_4": counts.get("remote_candidate_namespace_tag_count_at_review") == 4,
        "remote_approved_tag_count_at_review_4": counts.get("remote_approved_tag_count_at_review") == 4,
        "verified_remote_terminal_tag_count_4": counts.get("verified_remote_terminal_tag_count") == 4,
        "extra_remote_candidate_namespace_tag_count_zero": counts.get("extra_remote_candidate_namespace_tag_count_at_review") == 0,
        "remote_tag_names_match": len(pairs) == 4 and all(a.get("tag_name") == b["tag_name"] for a, b in pairs),
        "remote_tag_object_shas_match": len(pairs) == 4 and all(a.get("observed_remote_tag_object_sha") == b["local_tag_object_sha"] and a.get("remote_tag_object_sha_verified") is True for a, b in pairs),
        "remote_peeled_target_commits_match": len(pairs) == 4 and all(a.get("observed_remote_peeled_target_commit") == b["target_commit"] and a.get("remote_peeled_target_commit_verified") is True for a, b in pairs),
        "local_tags_still_match_source": len(pairs) == 4 and all(a.get("local_tag_object_sha") == b["local_tag_object_sha"] and a.get("local_target_commit") == b["target_commit"] and a.get("local_tag_still_matches_source") is True for a, b in pairs),
        "local_tag_messages_verified": len(messages) == 6 and all(value is True for value in messages.values()) and all(a.get("tag_message_verified_locally") is True for a in records),
        "remote_publication_complete": publication.get("remote_publication_review_status") == "VERIFIED_REMOTE_PUBLICATION_COMPLETE",
        "explicit_refspec_push_confirmed": publication.get("explicit_refspec_push_confirmed_from_source") is True,
        "push_all_tags_false": publication.get("push_all_tags_not_used") is True,
        "branch_push_false": publication.get("branch_push_not_used") is True,
        "main_push_false": publication.get("main_push_not_used") is True and review.get("git_main_push_performed") is False,
        "force_push_false": publication.get("force_push_not_used") is True and review.get("git_force_push_performed") is False,
        "additional_tag_push_false": review.get("additional_tag_push_performed") is False,
        "repository_tags_pushed_again_false": review.get("repository_tags_pushed_again") is False,
        "additional_tags_created_false": review.get("additional_tags_created") is False,
        "tags_modified_false": review.get("tags_modified") is False,
        "tags_deleted_false": review.get("tags_deleted") is False,
        "merge_performed_false": review.get("git_merge_performed") is False,
        "rebase_performed_false": review.get("git_rebase_performed") is False,
        "branch_delete_performed_false": review.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": review.get("git_remote_delete_performed") is False,
        "remote_prune_false": review.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": review.get("origin_main_modified_by_this_task") is False,
        "marketflow_outputs_not_tracked": review.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_generation_false": review.get("dataset_generation_performed_in_review") is False,
        "metric_recomputation_false": review.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": review.get("model_training_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "recommendations_false": review.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED and review.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED and review.get("profitability_accepted") is False,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": PASS if actual else FAIL, "expected": True,
            "actual": actual, "severity": BLOCKER,
            "message": "review evidence matches" if actual else "review evidence mismatch"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_tag_push_results_review_created": True,
        "repository_tag_push_results_review_ready": True,
        "verified_remote_terminal_tag_count": 4, "remote_approved_tag_count_at_review": 4,
        "extra_remote_candidate_namespace_tag_count_at_review": 0,
        "additional_tag_push_performed": False, "repository_tags_pushed_again": False,
        "tags_modified": False, "tags_deleted": False, "merge_performed": False,
        "delete_performed": False, "main_pushed": False, "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_tag_push_results_review_remote_tag_manifest_digest_v1(review: Mapping[str, Any]) -> str:
    manifest = [{key: row[key] for key in (
        "tag_name", "remote_ref", "observed_remote_tag_object_sha",
        "observed_remote_peeled_target_commit", "local_tag_object_sha",
        "local_target_commit", "source_artifact_kind", "source_digest",
        "remote_review_status",
    )} for row in review.get("remote_tag_review_records", [])]
    return semantic_digest(manifest)


def marketflow_repository_tag_push_results_review_digest_v1(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tag_push_results_review_digest", None)
    return semantic_digest(payload)


def _finish(review: dict[str, Any]) -> dict[str, Any]:
    review["marketflow_repository_tag_push_results_review_remote_tag_manifest_digest"] = marketflow_repository_tag_push_results_review_remote_tag_manifest_digest_v1(review)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_tag_push_results_review_digest"] = marketflow_repository_tag_push_results_review_digest_v1(review)
    validate_marketflow_repository_tag_push_results_review_v1(review)
    return review


def _blocked(problems: list[str]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED_REMOTE_TAG_MISMATCH_OR_ORIGIN_MAIN_CHANGE,
        "review_scope": REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "blocked_reasons": list(problems), "additional_tag_push_performed": False,
        "repository_tags_pushed_again": False, "tags_modified": False, "tags_deleted": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }


def build_marketflow_repository_tag_push_results_review_v1(
    *, repo_root: str | Path | None = None, git_snapshot: dict | None = None,
) -> dict:
    """Build a deterministic review from injected or read-only Git evidence."""
    snapshot = deepcopy(git_snapshot) if git_snapshot is not None else _read_git_snapshot(
        Path(repo_root) if repo_root is not None else Path.cwd()
    )
    problems = _snapshot_problems(snapshot)
    if problems:
        return _blocked(problems)
    return _finish(_base_review(snapshot))


def validate_marketflow_repository_tag_push_results_review_v1(review: dict) -> dict:
    """Validate the exact publication evidence and every closed authority gate."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryTagPushResultsReviewError("review must be an object")
    required = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
    }
    for field, expected in required.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryTagPushResultsReviewError(f"{field} mismatch")
    values = _check_values(review)
    failed = [check_id for check_id in REQUIRED_CHECK_IDS if not values[check_id]]
    if failed:
        raise MarketFlowRepositoryTagPushResultsReviewError(f"review check failed: {failed[0]}")
    checklist = review.get("checklist")
    if checklist != _checklist(review) or any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTagPushResultsReviewError("review checklist mismatch")
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTagPushResultsReviewError("review summary mismatch")
    manifest = review.get("marketflow_repository_tag_push_results_review_remote_tag_manifest_digest")
    if not isinstance(manifest, str) or len(manifest) != 64:
        raise MarketFlowRepositoryTagPushResultsReviewError("remote tag manifest digest missing")
    if manifest != marketflow_repository_tag_push_results_review_remote_tag_manifest_digest_v1(review):
        raise MarketFlowRepositoryTagPushResultsReviewError("remote tag manifest digest mismatch")
    digest = review.get("marketflow_repository_tag_push_results_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTagPushResultsReviewError("review digest missing")
    if digest != marketflow_repository_tag_push_results_review_digest_v1(review):
        raise MarketFlowRepositoryTagPushResultsReviewError("review digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "marketflow_repository_tag_push_results_review_digest": digest,
        "marketflow_repository_tag_push_results_review_remote_tag_manifest_digest": manifest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_tag_push_results_review_markdown_v1(review: dict) -> str:
    """Render a sanitized Markdown view of the remote publication review."""
    validation = validate_marketflow_repository_tag_push_results_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Repository Tag Push Results Review v1"]),
        ("MarketFlow Repository Tag Push Results Review v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.", f"Digest: `{validation['marketflow_repository_tag_push_results_review_digest']}`."]),
        ("Source Tag Push Execution", [f"Execution digest: `{review['source_tag_push_execution_digest']}`.", f"Remote manifest: `{review['source_remote_tag_manifest_digest']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(review['source_evidence'])}."]),
        ("Repository Context", [f"Source execution commit: `{review['source_execution_commit']}`.", f"Context: `{review['source_repository_context']}`."]),
        ("Review Scope", [review["review_scope"]]),
        ("Remote Tag Review", [f"`{row['remote_ref']}`: `{row['observed_remote_tag_object_sha']}` -> `{row['observed_remote_peeled_target_commit']}`" for row in review["remote_tag_review_records"]]),
        ("Remote Tag Count Review", [f"{key}: {value}" for key, value in review["remote_tag_count_review"].items()]),
        ("Tag Message Review", [f"{key}: {value}" for key, value in review["tag_message_review"].items()]),
        ("Remote Publication Review", [f"{key}: {value}" for key, value in review["remote_publication_review"].items()]),
        ("Origin/Main Protection", [f"Before/after/review: `{review['origin_main_commit_before_execution']}` / `{review['origin_main_commit_after_execution']}` / `{review['origin_main_commit_at_review']}`."]),
        ("Next Chain", list(review["next_chain"])), ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["Predictive usefulness and profitability remain not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['summary']['passed_checks']} / {review['summary']['total_checks']} checks pass; {review['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["The review used read-only Git inspection and did not push, create, modify, delete, merge, rebase, prune, call providers, acquire data, train, score, recommend, authorize runtime, or trade."]),
    ]
    lines = ["# MarketFlow Repository Tag Push Results Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tag_push_results_review_v1(
    output_dir: str | Path, *, repo_root: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_tag_push_results_review_v1(
        repo_root=repo_root, git_snapshot=git_snapshot
    )
    if review.get("artifact_kind") != ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1:
        raise MarketFlowRepositoryTagPushResultsReviewError("cannot write blocked review")
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tag_push_results_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTagPushResultsReviewError("review output already exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": review["artifact_kind"],
            "review_status": review["review_status"],
            "marketflow_repository_tag_push_results_review_digest": review["marketflow_repository_tag_push_results_review_digest"],
            "payload_sha256": sha256_bytes(payload)}
