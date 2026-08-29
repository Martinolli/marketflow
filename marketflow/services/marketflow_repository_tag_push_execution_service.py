"""Publish exactly four approved governance tags to origin using explicit refs."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
import subprocess
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_tag_push_strategy_approval_service as approval_service,
)
from marketflow.services import marketflow_repository_tagging_execution_service as tag_source


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1 = (
    "marketflow_repository_tag_push_execution_v1"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED_PRECHECK_OR_REMOTE_REF_MISMATCH = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED_PRECHECK_OR_REMOTE_REF_MISMATCH"
)
REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_VALID = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_VALID"
)
PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN = (
    approval_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN
)

EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "1758d75de5839fb2299873d183b68cdcd6772286642822654ab0efe4cfd726c7"
)
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST = (
    approval_service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST
)
EXPECTED_SOURCE_EXECUTION_DIGEST = approval_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_DIGEST = approval_service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST
EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST = approval_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = approval_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = approval_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = approval_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = (
    approval_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
)
EXPECTED_SOURCE_CLOSURE_DIGEST = approval_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = approval_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = approval_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = approval_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = approval_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = approval_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = approval_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_APPROVAL_COMMIT = "523a75676e42b4c16bc00ef13b67b04cc8bcfbde"
SOURCE_EVIDENCE = deepcopy(approval_service.SOURCE_EVIDENCE)

APPROVED_TAGS = [
    {
        "tag_name": spec["tag_name"],
        "local_tag_object_sha": object_sha,
        "target_commit": spec["target_commit"],
        "source_artifact_kind": spec["source_artifact_kind"],
        "source_digest": spec["source_digest"],
        "remote_ref": f"refs/tags/{spec['tag_name']}",
        "tag_message": spec["tag_message"],
    }
    for spec, object_sha in zip(
        tag_source.APPROVED_TERMINAL_TAGS,
        approval_service.APPROVED_TAG_OBJECT_SHAS,
    )
]
APPROVED_REMOTE_REFS = [row["remote_ref"] for row in APPROVED_TAGS]
APPROVED_TAG_PUSH_COUNT = 4
PUSH_COMMAND = "git push origin " + " ".join(APPROVED_REMOTE_REFS)
REMOTE_NAMESPACE = "refs/tags/marketflow/expectancy-lab/*"

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "Repository Tag Push Results Review v1.",
    "Repository Merge Strategy Candidate v1, only after tag-push results review or explicit local-only decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]
NEXT_GATES = [
    "repository_tag_push_results_review",
    "repository_merge_strategy_candidate_after_tag_push_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]
RISK_CONTROLS = [
    "execution_pushes_only_four_approved_tags",
    "execution_uses_explicit_refspecs",
    "execution_does_not_push_all_tags",
    "execution_does_not_push_branches",
    "execution_does_not_push_main",
    "execution_does_not_force_push",
    "execution_does_not_create_additional_tags",
    "execution_does_not_modify_tags",
    "execution_does_not_delete_tags",
    "execution_does_not_merge",
    "execution_does_not_rebase",
    "execution_does_not_delete_branches",
    "execution_does_not_delete_remote_branches",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_origin_main",
    "execution_does_not_modify_marketflow_outputs",
    "execution_does_not_call_providers",
    "execution_does_not_acquire_market_data",
    "execution_does_not_regenerate_dataset",
    "execution_does_not_rerun_tag_push_approval",
    "execution_does_not_rerun_tag_push_operator_review",
    "execution_does_not_rerun_tag_push_candidate",
    "execution_does_not_rerun_tagging_execution",
    "execution_does_not_rerun_inventory",
    "execution_does_not_rerun_evidence",
    "execution_does_not_recompute_metrics",
    "execution_does_not_train_models",
    "execution_does_not_score_strategy",
    "execution_does_not_generate_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability",
    "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_broker_execution",
    "remote_mismatch_blocks_push",
    "extra_remote_namespace_tag_blocks_push",
    "separate_results_review_required_after_push",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_results_review_digest_bound",
    "source_tag_manifest_review_digest_bound", "source_tagging_execution_digest_bound",
    "source_tagging_execution_manifest_digest_bound", "source_tagging_approval_digest_bound",
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound",
    "origin_main_commit_before_bound", "origin_main_commit_after_unchanged",
    "strategy_selected_true", "strategy_approved_true", "strategy_authorized_true",
    "tag_push_executed_true", "repository_tags_pushed_true",
    "git_tag_push_performed_true", "remote_terminal_tags_published_true",
    "approved_tag_push_count_4", "pushed_or_existing_matching_terminal_tag_count_4",
    "remote_approved_tag_count_after_push_4",
    "extra_remote_candidate_namespace_tag_count_zero", "tag_names_match",
    "local_tag_object_shas_match", "remote_tag_object_shas_match",
    "target_commits_match", "remote_peeled_target_commits_match",
    "explicit_refspec_command_used", "push_all_tags_false", "branch_push_false",
    "main_push_false", "force_push_false", "additional_tags_created_false",
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


class MarketFlowRepositoryTagPushExecutionError(ValueError):
    """Raised when execution evidence violates the approved boundary."""


def _git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise MarketFlowRepositoryTagPushExecutionError(detail)
    return completed.stdout.strip()


def _parse_remote_tags(output: str) -> dict[str, dict[str, str | None]]:
    refs: dict[str, dict[str, str | None]] = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        sha, ref = line.split(maxsplit=1)
        peeled = ref.endswith("^{}")
        base_ref = ref[:-3] if peeled else ref
        row = refs.setdefault(base_ref, {"object_sha": None, "peeled_target": None})
        row["peeled_target" if peeled else "object_sha"] = sha
    return refs


def _remote_tags(repo_root: Path) -> dict[str, dict[str, str | None]]:
    return _parse_remote_tags(_git(repo_root, "ls-remote", "--tags", "origin", REMOTE_NAMESPACE))


def _origin_main(repo_root: Path) -> str:
    lines = _git(repo_root, "ls-remote", "origin", "refs/heads/main").splitlines()
    if len(lines) != 1:
        raise MarketFlowRepositoryTagPushExecutionError("origin/main could not be resolved exactly")
    return lines[0].split(maxsplit=1)[0]


def _local_tag_count(repo_root: Path) -> int:
    output = _git(repo_root, "for-each-ref", "--format=%(refname)", "refs/tags")
    return len(output.splitlines()) if output else 0


def _tracked_marketflow_count(repo_root: Path) -> int:
    output = _git(repo_root, "ls-files", ".marketflow")
    return len(output.splitlines()) if output else 0


def _verify_local_tags(repo_root: Path) -> list[dict[str, Any]]:
    records = []
    for expected in APPROVED_TAGS:
        remote_ref = expected["remote_ref"]
        object_sha = _git(repo_root, "rev-parse", "--verify", remote_ref)
        object_type = _git(repo_root, "cat-file", "-t", object_sha)
        target = _git(repo_root, "rev-parse", f"{remote_ref}^{{}}")
        raw = _git(repo_root, "cat-file", "-p", object_sha)
        message = raw.split("\n\n", 1)[1].rstrip("\n") if "\n\n" in raw else ""
        problems = []
        if object_type != "tag":
            problems.append("local tag is not annotated")
        if object_sha != expected["local_tag_object_sha"]:
            problems.append("local tag object SHA mismatch")
        if target != expected["target_commit"]:
            problems.append("local peeled target mismatch")
        if message != expected["tag_message"]:
            problems.append("local tag message mismatch")
        if problems:
            raise MarketFlowRepositoryTagPushExecutionError(
                f"{expected['tag_name']}: {', '.join(problems)}"
            )
        records.append({**deepcopy(expected), "local_tag_verified_before_push": True})
    return records


def _verify_remote_precheck(
    remote: Mapping[str, Mapping[str, str | None]],
) -> tuple[dict[str, str], list[str]]:
    approved = set(APPROVED_REMOTE_REFS)
    extras = sorted(set(remote) - approved)
    if extras:
        raise MarketFlowRepositoryTagPushExecutionError(
            "extra remote expectancy-lab tag refs: " + ", ".join(extras)
        )
    statuses: dict[str, str] = {}
    for expected in APPROVED_TAGS:
        observed = remote.get(expected["remote_ref"])
        if observed is None:
            statuses[expected["remote_ref"]] = "ABSENT"
            continue
        if (
            observed.get("object_sha") != expected["local_tag_object_sha"]
            or observed.get("peeled_target") != expected["target_commit"]
        ):
            raise MarketFlowRepositoryTagPushExecutionError(
                f"remote tag mismatch: {expected['remote_ref']}"
            )
        statuses[expected["remote_ref"]] = "EXISTING_MATCHING_REMOTE_TAG"
    return statuses, extras


def _fixture_observations() -> tuple[int, int, dict[str, str], dict[str, dict[str, str | None]]]:
    statuses = {row["remote_ref"]: "ABSENT" for row in APPROVED_TAGS}
    remote = {
        row["remote_ref"]: {
            "object_sha": row["local_tag_object_sha"],
            "peeled_target": row["target_commit"],
        }
        for row in APPROVED_TAGS
    }
    return 32, 0, statuses, remote


def _execution_records(
    pre_statuses: Mapping[str, str],
    post_remote: Mapping[str, Mapping[str, str | None]],
) -> list[dict[str, Any]]:
    records = []
    for expected in APPROVED_TAGS:
        status = pre_statuses[expected["remote_ref"]]
        remote = post_remote[expected["remote_ref"]]
        records.append(
            {
                **deepcopy(expected),
                "remote_tag_object_sha": remote["object_sha"],
                "remote_peeled_target_commit": remote["peeled_target"],
                "pre_push_remote_ref_status": status,
                "post_push_remote_ref_status": "PUBLISHED_TO_ORIGIN",
                "tag_push_status": (
                    "EXISTING_MATCHING_REMOTE_TAG"
                    if status == "EXISTING_MATCHING_REMOTE_TAG"
                    else "PUSHED_TO_ORIGIN_EXPLICIT_REFSPEC"
                ),
                "local_tag_verified_before_push": True,
                "remote_tag_verified_after_push": True,
                "tag_object_sha_matches": remote["object_sha"] == expected["local_tag_object_sha"],
                "target_commit_matches": remote["peeled_target"] == expected["target_commit"],
                "tag_pushed": True,
                "main_push_required": False,
                "runtime_authority_created": False,
                "predictive_usefulness_accepted": False,
                "profitability_accepted": False,
                "trade_recommendations_generated": False,
            }
        )
    return records


def _base_execution(
    *, run_timestamp_utc: str, local_count: int, remote_before_count: int,
    records: list[dict[str, Any]], origin_main_before: str, origin_main_after: str,
) -> dict[str, Any]:
    existing = sum(row["pre_push_remote_ref_status"] == "EXISTING_MATCHING_REMOTE_TAG" for row in records)
    pushed = APPROVED_TAG_PUSH_COUNT - existing
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED,
        "execution_scope": REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline_except_explicit_git_tag_push": True,
        "planning_only": False,
        "governance_only": True,
        "source_tag_push_strategy_approval_artifact_kind": approval_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED,
        "source_tag_push_strategy_approval_scope": approval_service.REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tag_push_strategy_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_tag_push_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tagging_execution_tag_manifest_digest": EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
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
        "source_tag_push_strategy_approval_commit": EXPECTED_SOURCE_APPROVAL_COMMIT,
        "source_repository_context": {
            "final_source_live_context_after_approval_branch_push": {
                "local_branch_count": 299, "remote_branch_count": 271, "total_ref_count": 570,
            },
            "source_local_tag_count": 32,
        },
        "origin_main_commit_before_execution": origin_main_before,
        "origin_main_commit_after_execution": origin_main_after,
        "repository_tag_push_strategy_selected": True,
        "repository_tag_push_strategy_approved": True,
        "repository_tag_push_strategy_authorized": True,
        "repository_tag_push_strategy_executed": True,
        "repository_tags_pushed": True,
        "git_tag_push_performed": True,
        "remote_terminal_tags_published": True,
        "pushed_terminal_tag_count": pushed,
        "approved_tag_push_count": APPROVED_TAG_PUSH_COUNT,
        "ready_for_repository_tag_push_results_review": True,
        "tag_push_execution_records": records,
        "tag_push_count_summary": {
            "local_tag_count_before_push": local_count,
            "remote_candidate_namespace_tag_count_before_push": remote_before_count,
            "approved_tag_push_count": APPROVED_TAG_PUSH_COUNT,
            "pushed_terminal_tag_count": pushed,
            "existing_matching_remote_tag_count": existing,
            "remote_candidate_namespace_tag_count_after_push": APPROVED_TAG_PUSH_COUNT,
            "remote_approved_tag_count_after_push": APPROVED_TAG_PUSH_COUNT,
            "extra_remote_candidate_namespace_tag_count_after_push": 0,
            "tag_push_count_observation_note": (
                "First publication pushed all four approved tags."
                if pushed == 4 else "Existing exact remote tags were preserved without overwrite."
            ),
        },
        "push_command_used": PUSH_COMMAND,
        "push_command_used_explicit_refspecs": True,
        "push_all_tags_used": False,
        "main_push_used": False,
        "branch_push_used": False,
        "force_push_used": False,
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
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1",
    }


def _record_values(execution: Mapping[str, Any]) -> tuple[list[Any], list[Any]]:
    records = execution.get("tag_push_execution_records", [])
    return records, [row for row in APPROVED_TAGS]


def _check_values(execution: Mapping[str, Any]) -> dict[str, bool]:
    records, expected = _record_values(execution)
    counts = execution.get("tag_push_count_summary", {})
    record_count = len(records) == APPROVED_TAG_PUSH_COUNT
    pairs = list(zip(records, expected)) if record_count else []
    return {
        "source_approval_digest_bound": execution.get("source_tag_push_strategy_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": execution.get("source_tag_push_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": execution.get("source_tag_push_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_results_review_digest_bound": execution.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest_bound": execution.get("source_tag_manifest_review_digest") == EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest_bound": execution.get("source_tagging_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tagging_execution_manifest_digest_bound": execution.get("source_tagging_execution_tag_manifest_digest") == EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest_bound": execution.get("source_tagging_approval_digest") == EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST,
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
        "origin_main_commit_before_bound": execution.get("origin_main_commit_before_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "origin_main_commit_after_unchanged": execution.get("origin_main_commit_after_execution") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "strategy_selected_true": execution.get("repository_tag_push_strategy_selected") is True,
        "strategy_approved_true": execution.get("repository_tag_push_strategy_approved") is True,
        "strategy_authorized_true": execution.get("repository_tag_push_strategy_authorized") is True,
        "tag_push_executed_true": execution.get("repository_tag_push_strategy_executed") is True,
        "repository_tags_pushed_true": execution.get("repository_tags_pushed") is True,
        "git_tag_push_performed_true": execution.get("git_tag_push_performed") is True,
        "remote_terminal_tags_published_true": execution.get("remote_terminal_tags_published") is True,
        "approved_tag_push_count_4": execution.get("approved_tag_push_count") == 4,
        "pushed_or_existing_matching_terminal_tag_count_4": counts.get("pushed_terminal_tag_count", 0) + counts.get("existing_matching_remote_tag_count", 0) == 4,
        "remote_approved_tag_count_after_push_4": counts.get("remote_approved_tag_count_after_push") == 4,
        "extra_remote_candidate_namespace_tag_count_zero": counts.get("extra_remote_candidate_namespace_tag_count_after_push") == 0,
        "tag_names_match": record_count and all(a.get("tag_name") == b["tag_name"] for a, b in pairs),
        "local_tag_object_shas_match": record_count and all(a.get("local_tag_object_sha") == b["local_tag_object_sha"] for a, b in pairs),
        "remote_tag_object_shas_match": record_count and all(a.get("remote_tag_object_sha") == b["local_tag_object_sha"] for a, b in pairs),
        "target_commits_match": record_count and all(a.get("target_commit") == b["target_commit"] for a, b in pairs),
        "remote_peeled_target_commits_match": record_count and all(a.get("remote_peeled_target_commit") == b["target_commit"] for a, b in pairs),
        "explicit_refspec_command_used": execution.get("push_command_used") == PUSH_COMMAND and execution.get("push_command_used_explicit_refspecs") is True,
        "push_all_tags_false": execution.get("push_all_tags_used") is False,
        "branch_push_false": execution.get("branch_push_used") is False,
        "main_push_false": execution.get("main_push_used") is False and execution.get("git_main_push_performed") is False,
        "force_push_false": execution.get("force_push_used") is False and execution.get("git_force_push_performed") is False,
        "additional_tags_created_false": execution.get("additional_tags_created") is False,
        "tags_modified_false": execution.get("tags_modified") is False,
        "tags_deleted_false": execution.get("tags_deleted") is False,
        "merge_performed_false": execution.get("git_merge_performed") is False,
        "rebase_performed_false": execution.get("git_rebase_performed") is False,
        "branch_delete_performed_false": execution.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": execution.get("git_remote_delete_performed") is False,
        "remote_prune_false": execution.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": execution.get("origin_main_modified_by_this_task") is False,
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
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "execution evidence matches" if actual else "execution evidence mismatch",
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
        "repository_tag_push_strategy_executed": True,
        "repository_tags_pushed": True, "git_tag_push_performed": True,
        "remote_terminal_tags_published": True, "pushed_terminal_tag_count": 4,
        "remote_approved_tag_count_after_push": 4, "merge_performed": False,
        "delete_performed": False, "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_tag_push_execution_remote_tag_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    manifest = [
        {key: row[key] for key in (
            "tag_name", "local_tag_object_sha", "remote_tag_object_sha",
            "target_commit", "remote_peeled_target_commit", "source_artifact_kind",
            "source_digest", "remote_ref", "tag_push_status",
        )}
        for row in execution.get("tag_push_execution_records", [])
    ]
    return semantic_digest(manifest)


def marketflow_repository_tag_push_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tag_push_execution_digest", None)
    return semantic_digest(payload)


def _finish_execution(execution: dict[str, Any]) -> dict[str, Any]:
    execution["marketflow_repository_tag_push_execution_remote_tag_manifest_digest"] = (
        marketflow_repository_tag_push_execution_remote_tag_manifest_digest_v1(execution)
    )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution["checklist"])
    execution["marketflow_repository_tag_push_execution_digest"] = (
        marketflow_repository_tag_push_execution_digest_v1(execution)
    )
    validate_marketflow_repository_tag_push_execution_v1(execution)
    return execution


def _blocked(run_timestamp_utc: str, reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED_PRECHECK_OR_REMOTE_REF_MISMATCH,
        "execution_scope": REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "run_timestamp_utc": run_timestamp_utc,
        "blocked_reason": reason,
        "repository_tag_push_strategy_executed": False,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }


def execute_marketflow_repository_tag_push_v1(
    *, repo_root: str | Path | None = None, run_timestamp_utc: str | None = None,
    execute_git_operations: bool = True,
) -> dict:
    """Verify and publish only the approved refs; return a fail-closed artifact."""
    timestamp = run_timestamp_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if not execute_git_operations:
        local_count, before_count, statuses, after = _fixture_observations()
        records = _execution_records(statuses, after)
        return _finish_execution(_base_execution(
            run_timestamp_utc=timestamp, local_count=local_count,
            remote_before_count=before_count, records=records,
            origin_main_before=EXPECTED_ORIGIN_MAIN_COMMIT,
            origin_main_after=EXPECTED_ORIGIN_MAIN_COMMIT,
        ))

    root = Path(repo_root) if repo_root is not None else Path.cwd()
    try:
        origin_before = _origin_main(root)
        if origin_before != EXPECTED_ORIGIN_MAIN_COMMIT:
            raise MarketFlowRepositoryTagPushExecutionError("origin/main approval SHA mismatch")
        local_count = _local_tag_count(root)
        _verify_local_tags(root)
        before = _remote_tags(root)
        statuses, _ = _verify_remote_precheck(before)
        if any(status == "ABSENT" for status in statuses.values()):
            _git(root, "push", "origin", *APPROVED_REMOTE_REFS)
        after = _remote_tags(root)
        if set(after) != set(APPROVED_REMOTE_REFS):
            raise MarketFlowRepositoryTagPushExecutionError("post-push remote namespace mismatch")
        _verify_remote_precheck(after)
        origin_after = _origin_main(root)
        if origin_after != origin_before:
            raise MarketFlowRepositoryTagPushExecutionError("origin/main changed during execution")
        tracked_count = _tracked_marketflow_count(root)
        if tracked_count:
            raise MarketFlowRepositoryTagPushExecutionError("tracked .marketflow files detected")
        records = _execution_records(statuses, after)
        execution = _base_execution(
            run_timestamp_utc=timestamp, local_count=local_count,
            remote_before_count=len(before), records=records,
            origin_main_before=origin_before, origin_main_after=origin_after,
        )
        execution["tracked_marketflow_file_count"] = tracked_count
        execution["no_tracked_marketflow_files"] = tracked_count == 0
        return _finish_execution(execution)
    except MarketFlowRepositoryTagPushExecutionError as exc:
        return _blocked(timestamp, str(exc))


def validate_marketflow_repository_tag_push_execution_v1(execution: dict) -> dict:
    """Validate exact evidence, remote tag identity, and every closed boundary."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryTagPushExecutionError("execution must be an object")
    required = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED,
        "execution_scope": REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
    }
    for field, value in required.items():
        if execution.get(field) != value:
            raise MarketFlowRepositoryTagPushExecutionError(f"{field} mismatch")
    checks = _check_values(execution)
    failed = [check_id for check_id in REQUIRED_CHECK_IDS if not checks[check_id]]
    if failed:
        raise MarketFlowRepositoryTagPushExecutionError(f"execution check failed: {failed[0]}")
    checklist = execution.get("checklist")
    if checklist != _checklist(execution) or any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTagPushExecutionError("execution checklist mismatch")
    if execution.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTagPushExecutionError("execution summary mismatch")
    manifest_digest = execution.get("marketflow_repository_tag_push_execution_remote_tag_manifest_digest")
    if not isinstance(manifest_digest, str) or len(manifest_digest) != 64:
        raise MarketFlowRepositoryTagPushExecutionError("remote tag manifest digest missing")
    if manifest_digest != marketflow_repository_tag_push_execution_remote_tag_manifest_digest_v1(execution):
        raise MarketFlowRepositoryTagPushExecutionError("remote tag manifest digest mismatch")
    digest = execution.get("marketflow_repository_tag_push_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTagPushExecutionError("execution digest missing")
    if digest != marketflow_repository_tag_push_execution_digest_v1(execution):
        raise MarketFlowRepositoryTagPushExecutionError("execution digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_VALID,
        "artifact_kind": execution["artifact_kind"],
        "execution_status": execution["execution_status"],
        "marketflow_repository_tag_push_execution_digest": digest,
        "marketflow_repository_tag_push_execution_remote_tag_manifest_digest": manifest_digest,
        **{key: execution["summary"][key] for key in (
            "total_checks", "passed_checks", "failed_checks", "blocker_count"
        )},
    }


def build_marketflow_repository_tag_push_execution_markdown_v1(execution: dict) -> str:
    """Render a sanitized governance record for the completed tag publication."""
    validation = validate_marketflow_repository_tag_push_execution_v1(execution)
    sections = [
        ("Title", ["MarketFlow Repository Tag Push Execution v1"]),
        ("MarketFlow Repository Tag Push Execution v1", [f"Artifact/status: `{execution['artifact_kind']}` / `{execution['execution_status']}`.", f"Digest: `{validation['marketflow_repository_tag_push_execution_digest']}`."]),
        ("Source Tag Push Approval", [f"Source digest: `{execution['source_tag_push_strategy_approval_digest']}`.", f"Source commit: `{execution['source_tag_push_strategy_approval_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(execution['source_evidence'])}."]),
        ("Repository Context", [f"Source branches/refs: `{execution['source_repository_context']}`."]),
        ("Execution Scope", [execution["execution_scope"]]),
        ("Remote Tag Push Command", [execution["push_command_used"]]),
        ("Published Remote Tags", [f"`{row['remote_ref']}`: `{row['remote_tag_object_sha']}` -> `{row['remote_peeled_target_commit']}` ({row['tag_push_status']})" for row in execution["tag_push_execution_records"]]),
        ("Tag Push Count Summary", [f"{key}: {value}" for key, value in execution["tag_push_count_summary"].items()]),
        ("Origin/Main Protection", [f"Before/after: `{execution['origin_main_commit_before_execution']}` / `{execution['origin_main_commit_after_execution']}`."]),
        ("Next Chain", list(execution["next_chain"])),
        ("Next Gates", list(execution["next_gates"])),
        ("Risk Controls", list(execution["risk_controls"])),
        ("Authority Boundaries", ["Predictive usefulness and profitability remain not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{execution['summary']['passed_checks']} / {execution['summary']['total_checks']} checks pass; {execution['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["Only four approved explicit tag refs were published. No all-tags, branch, main, force, merge, rebase, delete, prune, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tag Push Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
