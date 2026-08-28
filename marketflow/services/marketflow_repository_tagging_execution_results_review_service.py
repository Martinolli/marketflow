"""Offline, read-only review of the four local repository tagging results."""

from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_tagging_execution_service as source_execution_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1 = (
    "marketflow_repository_tagging_execution_results_review_v1"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY"
)
REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_VALID"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED_TAG_MISMATCH_OR_REMOTE_PUBLICATION_DETECTED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED_TAG_MISMATCH_OR_REMOTE_PUBLICATION_DETECTED"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "71a6853960c2d30ab53f5894fc2dd912dde8e75452cb942252d123e0bd5d5c40"
)
EXPECTED_SOURCE_TAG_MANIFEST_DIGEST = (
    "55674e0acd44977f2c700783cc6805f067fd96e1e200f001db075818b1729759"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = source_execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_execution_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_execution_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_execution_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_execution_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_execution_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_execution_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_execution_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_execution_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_execution_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_execution_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_execution_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_execution_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_execution_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_execution_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_EXECUTION_COMMIT = "738941a3a8906f29528686fa35c76f76e1fa90ee"
SOURCE_EVIDENCE = deepcopy(source_execution_service.SOURCE_EVIDENCE)

EXPECTED_TAG_OBJECT_SHAS = [
    "c349f647fa06ef7eeeaba5addfaa1486592e4130",
    "4321312337d93a147b66ef16948a0802cc6c3e2e",
    "1056c5e3217197270327da6e4a01182295fcd4d0",
    "728ce5b883480ea0d0f952ff881274fbf110a7b8",
]
EXPECTED_TAGS = [
    {**deepcopy(spec), "tag_object_sha": object_sha}
    for spec, object_sha in zip(
        source_execution_service.APPROVED_TERMINAL_TAGS, EXPECTED_TAG_OBJECT_SHAS
    )
]
APPROVED_TERMINAL_TAG_NAMES = [row["tag_name"] for row in EXPECTED_TAGS]

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

MESSAGE_BOUNDARIES = [
    "MarketFlow research governance milestone.",
    "Predictive usefulness: NOT_ACCEPTED",
    "Profitability: NOT_ACCEPTED",
    "Runtime: NOT_AUTHORIZED",
    "Trading/Broker: NOT_AUTHORIZED",
    "No trade recommendation is created by this tag.",
]

NEXT_CHAIN = [
    "Repository Tag Push Strategy Candidate v1, only if remote publication is desired.",
    "Repository Merge Strategy Candidate v1, only after tag-push decision or explicit local-only decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]
NEXT_GATES = [
    "repository_tag_push_strategy_candidate_if_remote_publication_selected",
    "repository_tag_push_approval_if_selected",
    "repository_tag_push_execution_if_approved",
    "repository_merge_strategy_candidate_after_tagging_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]
RISK_CONTROLS = [
    "review_does_not_create_tags",
    "review_does_not_modify_tags",
    "review_does_not_delete_tags",
    "review_does_not_push_tags",
    "review_does_not_merge",
    "review_does_not_rebase",
    "review_does_not_delete_branches",
    "review_does_not_delete_remote_branches",
    "review_does_not_push_main",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_origin_main",
    "review_does_not_modify_marketflow_outputs",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset",
    "review_does_not_rerun_tagging_execution",
    "review_does_not_rerun_tagging_approval",
    "review_does_not_rerun_tagging_review",
    "review_does_not_rerun_tagging_candidate",
    "review_does_not_rerun_inventory",
    "review_does_not_rerun_evidence",
    "review_does_not_recompute_metrics",
    "review_does_not_train_models",
    "review_does_not_score_strategy",
    "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_broker_execution",
    "all_reviewed_tags_remain_local_only",
    "separate_strategy_required_before_tag_push",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound",
    "source_tag_manifest_digest_bound",
    "source_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_inventory_plan_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_operator_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound",
    "records_digest_bound",
    "origin_main_commit_bound",
    "execution_status_bound",
    "local_tags_reviewed_true",
    "tag_messages_reviewed_true",
    "tag_targets_reviewed_true",
    "tag_objects_reviewed_true",
    "ready_for_tag_push_strategy_candidate_true",
    "tag_push_strategy_candidate_created_false",
    "approved_terminal_tag_count_4",
    "verified_terminal_tag_count_4",
    "terminal_tag_names_match",
    "terminal_tag_targets_match",
    "terminal_tag_object_shas_match",
    "terminal_tag_messages_verified",
    "tag_objects_are_annotated",
    "remote_approved_tag_count_zero",
    "extra_candidate_namespace_tag_count_zero",
    "tags_pushed_false",
    "git_tag_push_performed_false",
    "additional_tags_created_false",
    "tags_modified_false",
    "tags_deleted_false",
    "merge_performed_false",
    "rebase_performed_false",
    "branch_delete_performed_false",
    "remote_delete_performed_false",
    "main_push_false",
    "force_push_false",
    "remote_prune_false",
    "origin_main_modified_false",
    "marketflow_outputs_not_tracked",
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


class MarketFlowRepositoryTaggingExecutionResultsReviewError(ValueError):
    """Raised when local tag review evidence is invalid."""


class MarketFlowRepositoryTaggingExecutionResultsReviewBlockedError(
    MarketFlowRepositoryTaggingExecutionResultsReviewError
):
    """Raised when local or remote tag evidence violates the approved manifest."""

    def __init__(self, message: str, *, blocked_artifact: dict[str, Any]) -> None:
        super().__init__(message)
        self.blocked_artifact = blocked_artifact


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=os.environ.copy(),
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "read-only git command failed"
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(detail)
    return result


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED_TAG_MISMATCH_OR_REMOTE_PUBLICATION_DETECTED,
        "review_scope": REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "blocked_reason": reason,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "tags_modified": False,
        "tags_deleted": False,
        "git_merge_performed": False,
        "git_main_push_performed": False,
        "provider_requests_made_in_review": False,
        "predictive_usefulness_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }


def _collect_git_snapshot(repo_root: Path) -> dict[str, Any]:
    actual_root = Path(_run_git(repo_root, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if actual_root != repo_root.resolve():
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "repo_root is not a Git repository root"
        )
    all_tag_refs = [
        line.strip()
        for line in _run_git(repo_root, "for-each-ref", "--format=%(refname)", "refs/tags").stdout.splitlines()
        if line.strip()
    ]
    namespace_refs = [
        line.strip()
        for line in _run_git(
            repo_root,
            "for-each-ref",
            "--format=%(refname)",
            "refs/tags/marketflow/expectancy-lab/",
        ).stdout.splitlines()
        if line.strip()
    ]
    remote_lines = [
        line.strip()
        for line in _run_git(
            repo_root,
            "ls-remote",
            "--tags",
            "origin",
            "marketflow/expectancy-lab/*",
        ).stdout.splitlines()
        if line.strip()
    ]
    remote_names = {
        line.split("\t", 1)[1].removeprefix("refs/tags/").removesuffix("^{}")
        for line in remote_lines
        if "\t" in line
    }
    tags = []
    for expected in EXPECTED_TAGS:
        tag_name = expected["tag_name"]
        object_sha = _run_git(
            repo_root,
            "rev-parse",
            f"refs/tags/{tag_name}",
        ).stdout.strip()
        object_type = _run_git(repo_root, "cat-file", "-t", object_sha).stdout.strip()
        target_commit = _run_git(
            repo_root,
            "rev-parse",
            f"refs/tags/{tag_name}^{{commit}}",
        ).stdout.strip()
        message = _run_git(
            repo_root,
            "for-each-ref",
            "--format=%(contents)",
            f"refs/tags/{tag_name}",
        ).stdout.rstrip("\r\n")
        tags.append(
            {
                "tag_name": tag_name,
                "tag_object_sha": object_sha,
                "tag_object_type": object_type,
                "target_commit": target_commit,
                "tag_message": message,
                "remote_ref_exists": tag_name in remote_names,
            }
        )
    tracked = [
        line
        for line in _run_git(repo_root, "ls-files", "--", ".marketflow").stdout.splitlines()
        if line
    ]
    return {
        "origin_main_commit": _run_git(repo_root, "rev-parse", "origin/main").stdout.strip(),
        "observed_tag_count_at_review": len(all_tag_refs),
        "observed_candidate_namespace_tag_count_at_review": len(namespace_refs),
        "remote_approved_tag_count": len(remote_names & set(APPROVED_TERMINAL_TAG_NAMES)),
        "tracked_marketflow_file_count": len(tracked),
        "tags": tags,
    }


def deterministic_marketflow_repository_tagging_execution_results_review_snapshot_v1() -> dict[str, Any]:
    """Return the exact committed source-execution observations for offline tests."""
    return {
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "observed_tag_count_at_review": 32,
        "observed_candidate_namespace_tag_count_at_review": 4,
        "remote_approved_tag_count": 0,
        "tracked_marketflow_file_count": 0,
        "tags": [
            {
                "tag_name": row["tag_name"],
                "tag_object_sha": row["tag_object_sha"],
                "tag_object_type": "tag",
                "target_commit": row["target_commit"],
                "tag_message": row["tag_message"],
                "remote_ref_exists": False,
            }
            for row in EXPECTED_TAGS
        ],
    }


def _review_records(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    tags = snapshot.get("tags")
    if not isinstance(tags, list) or len(tags) != 4:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "exactly four tag observations are required"
        )
    observed_by_name = {
        row.get("tag_name"): row for row in tags if isinstance(row, Mapping)
    }
    if set(observed_by_name) != set(APPROVED_TERMINAL_TAG_NAMES):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "terminal tag names mismatch"
        )
    records = []
    for expected in EXPECTED_TAGS:
        observed = observed_by_name[expected["tag_name"]]
        message = observed.get("tag_message")
        message_verified = (
            isinstance(message, str)
            and message == expected["tag_message"]
            and all(boundary in message for boundary in MESSAGE_BOUNDARIES)
        )
        record = {
            "tag_name": expected["tag_name"],
            "source_artifact_kind": expected["source_artifact_kind"],
            "source_digest": expected["source_digest"],
            "expected_target_commit": expected["target_commit"],
            "observed_target_commit": observed.get("target_commit"),
            "expected_tag_object_sha": expected["tag_object_sha"],
            "observed_tag_object_sha": observed.get("tag_object_sha"),
            "tag_type_observed": "ANNOTATED" if observed.get("tag_object_type") == "tag" else observed.get("tag_object_type"),
            "tag_exists_locally": True,
            "tag_target_commit_verified": observed.get("target_commit") == expected["target_commit"],
            "tag_object_sha_verified": observed.get("tag_object_sha") == expected["tag_object_sha"],
            "tag_message": message,
            "tag_message_verified": message_verified,
            "tag_remote_ref_exists": observed.get("remote_ref_exists") is True,
            "tag_pushed": observed.get("remote_ref_exists") is True,
            "tag_modified": False,
            "tag_deleted": False,
            "review_status": "VERIFIED_LOCAL_ANNOTATED_TAG_NOT_PUSHED",
        }
        if not all(
            (
                record["tag_target_commit_verified"],
                record["tag_object_sha_verified"],
                record["tag_message_verified"],
                record["tag_type_observed"] == "ANNOTATED",
                record["tag_remote_ref_exists"] is False,
            )
        ):
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                f"tag evidence mismatch for {expected['tag_name']}"
            )
        records.append(record)
    return records


def _base_review(snapshot: Mapping[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    observed_total = snapshot.get("observed_tag_count_at_review")
    observed_namespace = snapshot.get("observed_candidate_namespace_tag_count_at_review")
    remote_count = snapshot.get("remote_approved_tag_count")
    tracked_count = snapshot.get("tracked_marketflow_file_count")
    if not all(isinstance(value, int) and value >= 0 for value in (observed_total, observed_namespace, remote_count, tracked_count)):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "snapshot counts must be non-negative integers"
        )
    extra_count = observed_namespace - 4
    observation_note = (
        "Observed source execution totals exactly: 32 local tags and 4 approved namespace tags."
        if (observed_total, observed_namespace) == (32, 4)
        else "Unrelated local tag count differs; the approved namespace remains reviewed separately."
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True,
        "planning_only": True,
        "governance_only": True,
        "source_tagging_execution_artifact_kind": source_execution_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED,
        "source_tagging_execution_status": source_execution_service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED,
        "source_tagging_execution_scope": source_execution_service.REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tag_manifest_digest": EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "origin_main_commit": snapshot.get("origin_main_commit"),
        "source_execution_commit": EXPECTED_SOURCE_EXECUTION_COMMIT,
        "post_push_local_branch_count": 295,
        "post_push_remote_branch_count": 267,
        "post_push_total_ref_count": 562,
        "repository_tagging_execution_results_review_created": True,
        "repository_tagging_execution_results_review_ready": True,
        "local_tags_reviewed": True,
        "tag_messages_reviewed": True,
        "tag_targets_reviewed": True,
        "tag_objects_reviewed": True,
        "ready_for_repository_tag_push_strategy_candidate": True,
        "repository_tag_push_strategy_candidate_created": False,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "additional_tags_created": False,
        "tags_modified": False,
        "tags_deleted": False,
        "git_merge_performed": False,
        "git_rebase_performed": False,
        "git_branch_delete_performed": False,
        "git_remote_delete_performed": False,
        "git_main_push_performed": False,
        "git_force_push_performed": False,
        "git_remote_prune_performed": False,
        "origin_main_modified_by_this_task": False,
        "repository_merge_strategy_candidate_created": False,
        "repository_cleanup_candidate_created": False,
        "repository_cleanup_executed": False,
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
        "approved_terminal_tag_count": 4,
        "verified_terminal_tag_count": len(records),
        "tag_review_records": deepcopy(records),
        "tag_count_review": {
            "tag_count_before_execution_from_source": 28,
            "candidate_namespace_tag_count_before_execution_from_source": 0,
            "tag_count_after_execution_from_source": 32,
            "candidate_namespace_tag_count_after_execution_from_source": 4,
            "observed_tag_count_at_review": observed_total,
            "observed_candidate_namespace_tag_count_at_review": observed_namespace,
            "approved_terminal_tag_count": 4,
            "verified_terminal_tag_count": len(records),
            "extra_candidate_namespace_tag_count": extra_count,
            "remote_approved_tag_count": remote_count,
            "tag_count_observation_note": observation_note,
        },
        "tag_message_review": {
            "all_tag_messages_include_governance_milestone": all(MESSAGE_BOUNDARIES[0] in row["tag_message"] for row in records),
            "all_tag_messages_include_not_accepted_predictive_usefulness": all(MESSAGE_BOUNDARIES[1] in row["tag_message"] for row in records),
            "all_tag_messages_include_not_accepted_profitability": all(MESSAGE_BOUNDARIES[2] in row["tag_message"] for row in records),
            "all_tag_messages_include_not_authorized_runtime": all(MESSAGE_BOUNDARIES[3] in row["tag_message"] for row in records),
            "all_tag_messages_include_not_authorized_trading_broker": all(MESSAGE_BOUNDARIES[4] in row["tag_message"] for row in records),
            "all_tag_messages_include_no_trade_recommendation": all(MESSAGE_BOUNDARIES[5] in row["tag_message"] for row in records),
        },
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": tracked_count,
        "no_tracked_marketflow_files": tracked_count == 0,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1_IF_REMOTE_PUBLICATION_SELECTED",
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    records = review.get("tag_review_records", [])
    counts = review.get("tag_count_review", {})
    messages = review.get("tag_message_review", {})
    return {
        "source_execution_digest_bound": review.get("source_tagging_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tag_manifest_digest_bound": review.get("source_tag_manifest_digest") == EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_approval_digest_bound": review.get("source_tagging_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": review.get("source_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": review.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest_bound": review.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": review.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": review.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": review.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": review.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": review.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": review.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": review.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": review.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": review.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": review.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "execution_status_bound": review.get("source_tagging_execution_status") == source_execution_service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED,
        "local_tags_reviewed_true": review.get("local_tags_reviewed") is True,
        "tag_messages_reviewed_true": review.get("tag_messages_reviewed") is True,
        "tag_targets_reviewed_true": review.get("tag_targets_reviewed") is True,
        "tag_objects_reviewed_true": review.get("tag_objects_reviewed") is True,
        "ready_for_tag_push_strategy_candidate_true": review.get("ready_for_repository_tag_push_strategy_candidate") is True,
        "tag_push_strategy_candidate_created_false": review.get("repository_tag_push_strategy_candidate_created") is False,
        "approved_terminal_tag_count_4": review.get("approved_terminal_tag_count") == 4,
        "verified_terminal_tag_count_4": review.get("verified_terminal_tag_count") == len(records) == 4,
        "terminal_tag_names_match": [row.get("tag_name") for row in records] == APPROVED_TERMINAL_TAG_NAMES,
        "terminal_tag_targets_match": all(row.get("tag_target_commit_verified") is True and row.get("expected_target_commit") == expected["target_commit"] and row.get("observed_target_commit") == expected["target_commit"] for row, expected in zip(records, EXPECTED_TAGS)),
        "terminal_tag_object_shas_match": all(row.get("tag_object_sha_verified") is True and row.get("expected_tag_object_sha") == expected["tag_object_sha"] and row.get("observed_tag_object_sha") == expected["tag_object_sha"] for row, expected in zip(records, EXPECTED_TAGS)),
        "terminal_tag_messages_verified": all(row.get("tag_message_verified") is True for row in records) and all(value is True for value in messages.values()),
        "tag_objects_are_annotated": all(row.get("tag_type_observed") == "ANNOTATED" for row in records),
        "remote_approved_tag_count_zero": counts.get("remote_approved_tag_count") == 0 and all(row.get("tag_remote_ref_exists") is False for row in records),
        "extra_candidate_namespace_tag_count_zero": counts.get("extra_candidate_namespace_tag_count") == 0,
        "tags_pushed_false": review.get("repository_tags_pushed") is False and all(row.get("tag_pushed") is False for row in records),
        "git_tag_push_performed_false": review.get("git_tag_push_performed") is False,
        "additional_tags_created_false": review.get("additional_tags_created") is False,
        "tags_modified_false": review.get("tags_modified") is False and all(row.get("tag_modified") is False for row in records),
        "tags_deleted_false": review.get("tags_deleted") is False and all(row.get("tag_deleted") is False for row in records),
        "merge_performed_false": review.get("git_merge_performed") is False,
        "rebase_performed_false": review.get("git_rebase_performed") is False,
        "branch_delete_performed_false": review.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": review.get("git_remote_delete_performed") is False,
        "main_push_false": review.get("git_main_push_performed") is False,
        "force_push_false": review.get("git_force_push_performed") is False,
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
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "review condition satisfied" if actual else "review condition failed",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(review: Mapping[str, Any], checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row.get("status") == PASS for row in rows)
    failed = len(rows) - passed
    counts = review["tag_count_review"]
    return {
        "total_checks": len(rows),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "repository_tagging_execution_results_review_created": True,
        "repository_tagging_execution_results_review_ready": True,
        "verified_terminal_tag_count": review["verified_terminal_tag_count"],
        "remote_approved_tag_count": counts["remote_approved_tag_count"],
        "extra_candidate_namespace_tag_count": counts["extra_candidate_namespace_tag_count"],
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "tags_modified": False,
        "tags_deleted": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1_IF_REMOTE_PUBLICATION_SELECTED",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tagging_execution_results_review_tag_manifest_digest_v1(
    review_or_records: Mapping[str, Any] | list[dict[str, Any]],
) -> str:
    records = (
        review_or_records["tag_review_records"]
        if isinstance(review_or_records, Mapping)
        else review_or_records
    )
    return semantic_digest({"tag_review_records": records})


def marketflow_repository_tagging_execution_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("marketflow_repository_tagging_execution_results_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tagging_execution_results_review_v1(
    *,
    repo_root: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict[str, Any]:
    """Review exact local tags and remote absence without mutating any refs."""
    try:
        if git_snapshot is None:
            root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
            snapshot = _collect_git_snapshot(root.resolve())
        else:
            snapshot = deepcopy(git_snapshot)
        if snapshot.get("origin_main_commit") != EXPECTED_ORIGIN_MAIN_COMMIT:
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                "origin/main commit mismatch"
            )
        records = _review_records(snapshot)
        review = _base_review(snapshot, records)
        if review["tag_count_review"]["remote_approved_tag_count"] != 0:
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                "approved tag remote publication detected"
            )
        if review["tag_count_review"]["extra_candidate_namespace_tag_count"] != 0:
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                "extra candidate namespace tag detected"
            )
    except (MarketFlowRepositoryTaggingExecutionResultsReviewError, KeyError, TypeError) as exc:
        blocked = _blocked(str(exc))
        raise MarketFlowRepositoryTaggingExecutionResultsReviewBlockedError(
            str(exc), blocked_artifact=blocked
        ) from exc
    review["marketflow_repository_tagging_execution_results_review_tag_manifest_digest"] = (
        marketflow_repository_tagging_execution_results_review_tag_manifest_digest_v1(review)
    )
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    if review["summary"]["blocker_count"]:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewBlockedError(
            "tagging execution results review contains blockers",
            blocked_artifact=_blocked("tagging execution results review contains blockers"),
        )
    review["marketflow_repository_tagging_execution_results_review_digest"] = (
        marketflow_repository_tagging_execution_results_review_digest_v1(review)
    )
    validate_marketflow_repository_tagging_execution_results_review_v1(review)
    return review


def validate_marketflow_repository_tagging_execution_results_review_v1(
    review: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "review must be an object"
        )
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY,
        "review_scope": REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tag_manifest_digest": EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_execution_commit": EXPECTED_SOURCE_EXECUTION_COMMIT,
        "repository_tagging_execution_results_review_created": True,
        "repository_tagging_execution_results_review_ready": True,
        "local_tags_reviewed": True,
        "tag_messages_reviewed": True,
        "tag_targets_reviewed": True,
        "tag_objects_reviewed": True,
        "ready_for_repository_tag_push_strategy_candidate": True,
        "repository_tag_push_strategy_candidate_created": False,
        "approved_terminal_tag_count": 4,
        "verified_terminal_tag_count": 4,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "additional_tags_created": False,
        "tags_modified": False,
        "tags_deleted": False,
        "git_merge_performed": False,
        "git_rebase_performed": False,
        "git_branch_delete_performed": False,
        "git_remote_delete_performed": False,
        "git_main_push_performed": False,
        "git_force_push_performed": False,
        "git_remote_prune_performed": False,
        "origin_main_modified_by_this_task": False,
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
        "broker_execution": NOT_AUTHORIZED,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                f"{field} mismatch"
            )
    records = review.get("tag_review_records")
    if not isinstance(records, list) or len(records) != 4:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "tag review records mismatch"
        )
    for record, expected in zip(records, EXPECTED_TAGS):
        expected_values = {
            "tag_name": expected["tag_name"],
            "expected_target_commit": expected["target_commit"],
            "observed_target_commit": expected["target_commit"],
            "expected_tag_object_sha": expected["tag_object_sha"],
            "observed_tag_object_sha": expected["tag_object_sha"],
            "tag_type_observed": "ANNOTATED",
            "tag_exists_locally": True,
            "tag_target_commit_verified": True,
            "tag_object_sha_verified": True,
            "tag_message": expected["tag_message"],
            "tag_message_verified": True,
            "tag_remote_ref_exists": False,
            "tag_pushed": False,
            "tag_modified": False,
            "tag_deleted": False,
            "review_status": "VERIFIED_LOCAL_ANNOTATED_TAG_NOT_PUSHED",
        }
        for field, value in expected_values.items():
            if record.get(field) != value:
                raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                    f"tag review {field} mismatch"
                )
        if not SHA_PATTERN.fullmatch(record["observed_tag_object_sha"]):
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                "tag object SHA format mismatch"
            )
        if not all(boundary in record["tag_message"] for boundary in MESSAGE_BOUNDARIES):
            raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
                "tag message boundary missing"
            )
    counts = review.get("tag_count_review")
    if not isinstance(counts, dict):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "tag count review missing"
        )
    if counts.get("verified_terminal_tag_count") != 4:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "verified tag count mismatch"
        )
    if counts.get("remote_approved_tag_count") != 0:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "remote approved tag count mismatch"
        )
    if counts.get("extra_candidate_namespace_tag_count") != 0:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "extra namespace tag count mismatch"
        )
    manifest_digest = review.get(
        "marketflow_repository_tagging_execution_results_review_tag_manifest_digest"
    )
    if manifest_digest != marketflow_repository_tagging_execution_results_review_tag_manifest_digest_v1(review):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "tag manifest review digest mismatch"
        )
    checklist = review.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(review):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "results review checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "results review checklist failed"
        )
    if review.get("summary") != _summary(review, checklist):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "results review summary mismatch"
        )
    digest = review.get("marketflow_repository_tagging_execution_results_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "results review digest missing"
        )
    if digest != marketflow_repository_tagging_execution_results_review_digest_v1(review):
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "results review digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tagging_execution_results_review_digest": digest,
        "marketflow_repository_tagging_execution_results_review_tag_manifest_digest": manifest_digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tagging_execution_results_review_markdown_v1(
    review: dict[str, Any],
) -> str:
    validation = validate_marketflow_repository_tagging_execution_results_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Repository Tagging Execution Results Review v1"]),
        ("MarketFlow Repository Tagging Execution Results Review v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.", f"Review digest: `{validation['marketflow_repository_tagging_execution_results_review_digest']}`.", f"Tag manifest review digest: `{validation['marketflow_repository_tagging_execution_results_review_tag_manifest_digest']}`."]),
        ("Source Tagging Execution", [f"Execution digest: `{review['source_tagging_execution_digest']}`.", f"Execution commit: `{review['source_execution_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(review['source_evidence'])}."]),
        ("Repository Context", [f"Frozen origin/main: `{review['origin_main_commit']}`.", "Source post-push branch inventory: 295 / 267 / 562."]),
        ("Review Scope", [review["review_scope"]]),
        ("Reviewed Local Annotated Tags", [f"`{row['tag_name']}` -> `{row['observed_target_commit']}` (object `{row['observed_tag_object_sha']}`)" for row in review["tag_review_records"]]),
        ("Tag Count Review", [f"Observed total/namespace: {review['tag_count_review']['observed_tag_count_at_review']} / {review['tag_count_review']['observed_candidate_namespace_tag_count_at_review']}.", f"Verified/extra: {review['verified_terminal_tag_count']} / {review['tag_count_review']['extra_candidate_namespace_tag_count']}. "]),
        ("Tag Message Review", [f"{key}: {value}" for key, value in review["tag_message_review"].items()]),
        ("Remote Tag Publication Review", [f"Remote approved tags: {review['tag_count_review']['remote_approved_tag_count']}.", "No tag-push strategy candidate or approval is created."]),
        ("Next Chain", list(review["next_chain"])),
        ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["Review only: no tag creation, modification, deletion, or push; no merge, cleanup, main, predictive, profitability, runtime, broker, or trading authority."]),
        ("Checklist Summary", [f"{review['summary']['passed_checks']} / {review['summary']['total_checks']} checks pass; {review['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No provider, data, metric, model, recommendation, runtime, tag mutation, tag push, merge, delete, main push, force push, prune, or .marketflow mutation occurred."]),
    ]
    lines = ["# MarketFlow Repository Tagging Execution Results Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tagging_execution_results_review_v1(
    output_dir: str | Path,
    *,
    repo_root: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON without overwriting an existing review."""
    review = build_marketflow_repository_tagging_execution_results_review_v1(
        repo_root=repo_root,
        git_snapshot=git_snapshot,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tagging_execution_results_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTaggingExecutionResultsReviewError(
            "tagging execution results review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tagging_execution_results_review_digest": review[
            "marketflow_repository_tagging_execution_results_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
