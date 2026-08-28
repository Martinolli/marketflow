"""Create the four approved local annotated governance tags, without pushing them."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import hashlib
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_tagging_release_strategy_approval_service as source_approval_service,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1 = (
    "marketflow_repository_tagging_execution_v1"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED"
)
REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_VALID = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_VALID"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED"
)
MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED_TAG_CREATION_OR_VERIFICATION_FAILED = (
    "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED_TAG_CREATION_OR_VERIFICATION_FAILED"
)

SELECTED_TAGGING_PACKAGE = source_approval_service.SELECTED_TAGGING_PACKAGE
EXPECTED_SOURCE_APPROVAL_DIGEST = (
    "7955296dbbd3e218b7d860319707eb98dc15780fad44dcba189a584791e3214a"
)
EXPECTED_SOURCE_APPROVAL_COMMIT = "0c7e49ed839543109c39337f67038c8293f9e24f"
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    source_approval_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_approval_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_approval_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_approval_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_approval_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_approval_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_approval_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_approval_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_approval_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_approval_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_approval_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_approval_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_approval_service.EXPECTED_ORIGIN_MAIN_COMMIT
SOURCE_EVIDENCE = deepcopy(source_approval_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
TAG_STATUS_CREATED = "CREATED_LOCAL_ANNOTATED_TAG"
TAG_STATUS_EXISTING = "EXISTING_MATCHING_TAG"
TAG_OBJECT_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def _tag_message(artifact_kind: str, status: str, decision: str, digest: str) -> str:
    return f"""MarketFlow research governance milestone.

Artifact: {artifact_kind}
Status: {status}
Decision: {decision}
Scope: research-only / governance-only
Predictive usefulness: NOT_ACCEPTED
Profitability: NOT_ACCEPTED
Runtime: NOT_AUTHORIZED
Trading/Broker: NOT_AUTHORIZED
Source digest: {digest}
No trade recommendation is created by this tag."""


def _tag_spec(
    *,
    tag_name: str,
    target_branch: str,
    target_commit: str,
    artifact_kind: str,
    artifact_status: str,
    decision: str,
    source_digest: str,
) -> dict[str, Any]:
    return {
        "tag_name": tag_name,
        "target_branch": target_branch,
        "target_commit": target_commit,
        "source_artifact_kind": artifact_kind,
        "source_artifact_status": artifact_status,
        "source_decision": decision,
        "source_digest": source_digest,
        "tag_message": _tag_message(artifact_kind, artifact_status, decision, source_digest),
    }


APPROVED_TERMINAL_TAGS = [
    _tag_spec(
        tag_name="marketflow/expectancy-lab/final-archive-not-ready/v1",
        target_branch="feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1",
        target_commit="0be55dc8a65a586368c192d6bc13302b9830a0b4",
        artifact_kind="MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE",
        artifact_status="MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE",
        decision="CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED",
        source_digest=EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
    ),
    _tag_spec(
        tag_name="marketflow/expectancy-lab/archive-record-not-ready/v1",
        target_branch="feature/marketflow-predictive-usefulness-acceptance-path-archive-record-expectancy-lab-evidence-v1",
        target_commit="e2fcfb792ad14db8a2de69556c291529fda47a8e",
        artifact_kind="MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE",
        artifact_status="MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE",
        decision="ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY",
        source_digest=EXPECTED_SOURCE_ARCHIVE_DIGEST,
    ),
    _tag_spec(
        tag_name="marketflow/expectancy-lab/operator-selection-option-a/v1",
        target_branch="feature/marketflow-operator-method-or-closure-selection-expectancy-lab-evidence-v1",
        target_commit="15c4fae495f88b54e30380f3d8b4aa54989fad39",
        artifact_kind="MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE",
        artifact_status="MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE",
        decision="SELECT_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY",
        source_digest=EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
    ),
    _tag_spec(
        tag_name="marketflow/expectancy-lab/readiness-not-ready/v1",
        target_branch="feature/marketflow-predictive-usefulness-acceptance-readiness-review-expectancy-lab-evidence-v1",
        target_commit="611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0",
        artifact_kind="MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE",
        artifact_status="MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED",
        decision="MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE",
        source_digest=EXPECTED_SOURCE_READINESS_DIGEST,
    ),
]
APPROVED_TERMINAL_TAG_NAMES = [row["tag_name"] for row in APPROVED_TERMINAL_TAGS]

NEXT_CHAIN = [
    "Repository Tagging Execution Results Review v1.",
    "Repository Tag Push Strategy Candidate v1, only if operator wants remote tag publication.",
    "Repository Merge Strategy Candidate v1, only after tagging execution review and tag-push decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]
NEXT_GATES = [
    "repository_tagging_execution_results_review",
    "repository_tag_push_strategy_candidate_if_remote_publication_selected",
    "repository_merge_strategy_candidate_after_tagging_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]
RISK_CONTROLS = [
    "execution_creates_only_four_approved_local_annotated_tags",
    "execution_does_not_push_tags",
    "execution_does_not_merge",
    "execution_does_not_rebase",
    "execution_does_not_delete_branches",
    "execution_does_not_delete_remote_branches",
    "execution_does_not_push_main",
    "execution_does_not_force_push",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_origin_main",
    "execution_does_not_modify_marketflow_outputs",
    "execution_does_not_call_providers",
    "execution_does_not_acquire_market_data",
    "execution_does_not_regenerate_dataset",
    "execution_does_not_rerun_approval",
    "execution_does_not_rerun_operator_review",
    "execution_does_not_rerun_candidate",
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
    "only_approved_tag_names_allowed",
    "only_approved_target_commits_allowed",
    "existing_mismatched_tags_block_execution",
    "separate_review_required_after_tagging",
    "separate_strategy_required_before_tag_push",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]
REQUIRED_CHECK_IDS = [
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
    "selected_package_terminal_archive_tags",
    "approval_status_bound",
    "strategy_authorized_true",
    "tagging_execution_performed_true",
    "local_annotated_tags_created_true",
    "approved_terminal_tag_count_4",
    "created_or_existing_matching_terminal_tag_count_4",
    "terminal_tag_names_match",
    "terminal_tag_targets_match",
    "terminal_tag_messages_verified",
    "tag_objects_are_annotated",
    "tag_count_summary_recorded",
    "candidate_namespace_tag_count_after_execution_4",
    "tags_pushed_false",
    "git_tag_push_performed_false",
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


class MarketFlowRepositoryTaggingExecutionError(ValueError):
    """Raised when a tagging execution artifact is invalid."""


class MarketFlowRepositoryTaggingExecutionBlockedError(
    MarketFlowRepositoryTaggingExecutionError
):
    """Raised after a fail-closed Git preflight or creation failure."""

    def __init__(self, message: str, *, blocked_artifact: dict[str, Any]) -> None:
        super().__init__(message)
        self.blocked_artifact = blocked_artifact


def _run_git(
    repo_root: Path,
    *args: str,
    check: bool = True,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=command_env,
    )
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise MarketFlowRepositoryTaggingExecutionError(detail)
    return result


def _count_tag_refs(repo_root: Path, prefix: str | None = None) -> int:
    ref_prefix = "refs/tags" if prefix is None else f"refs/tags/{prefix}"
    output = _run_git(repo_root, "for-each-ref", "--format=%(refname)", ref_prefix).stdout
    return len([line for line in output.splitlines() if line.strip()])


def _tag_ref(repo_root: Path, tag_name: str) -> str | None:
    output = _run_git(
        repo_root,
        "for-each-ref",
        "--format=%(objectname)",
        f"refs/tags/{tag_name}",
    ).stdout.strip()
    return output or None


def _verify_target_commit(repo_root: Path, expected_commit: str) -> None:
    resolved = _run_git(repo_root, "rev-parse", f"{expected_commit}^{{commit}}").stdout.strip()
    if resolved != expected_commit:
        raise MarketFlowRepositoryTaggingExecutionError(
            f"target commit mismatch: expected {expected_commit}, got {resolved}"
        )


def _inspect_existing_tag(
    repo_root: Path, spec: Mapping[str, Any], tag_object_sha: str
) -> dict[str, Any]:
    object_type = _run_git(repo_root, "cat-file", "-t", tag_object_sha).stdout.strip()
    if object_type != "tag":
        raise MarketFlowRepositoryTaggingExecutionError(
            f"existing tag {spec['tag_name']} is not annotated"
        )
    target = _run_git(
        repo_root, "rev-parse", f"refs/tags/{spec['tag_name']}^{{commit}}"
    ).stdout.strip()
    if target != spec["target_commit"]:
        raise MarketFlowRepositoryTaggingExecutionError(
            f"existing tag {spec['tag_name']} target mismatch"
        )
    message = _run_git(
        repo_root,
        "for-each-ref",
        "--format=%(contents)",
        f"refs/tags/{spec['tag_name']}",
    ).stdout.rstrip("\r\n")
    if message != spec["tag_message"]:
        raise MarketFlowRepositoryTaggingExecutionError(
            f"existing tag {spec['tag_name']} message mismatch"
        )
    return _tag_record(
        spec,
        tag_status=TAG_STATUS_EXISTING,
        tag_object_sha=tag_object_sha,
    )


def _tag_record(
    spec: Mapping[str, Any], *, tag_status: str, tag_object_sha: str
) -> dict[str, Any]:
    return {
        **deepcopy(dict(spec)),
        "tag_status": tag_status,
        "tag_type": "ANNOTATED",
        "tag_object_sha": tag_object_sha,
        "tag_target_commit_verified": True,
        "tag_message_verified": True,
        "tag_created": True,
        "tag_pushed": False,
        "main_push_required": False,
        "runtime_authority_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "trade_recommendations_generated": False,
    }


def _fixture_records() -> list[dict[str, Any]]:
    records = []
    for spec in APPROVED_TERMINAL_TAGS:
        object_sha = hashlib.sha1(
            canonical_json_bytes({"fixture_annotated_tag": spec})
        ).hexdigest()
        records.append(
            _tag_record(spec, tag_status=TAG_STATUS_CREATED, tag_object_sha=object_sha)
        )
    return records


def _blocked_artifact(reason: str, created_tag_names: list[str]) -> dict[str, Any]:
    return {
        "artifact_kind": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED_TAG_CREATION_OR_VERIFICATION_FAILED,
        "execution_scope": REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "blocked_reason": reason,
        "created_tag_names_before_block": list(created_tag_names),
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "git_merge_performed": False,
        "git_branch_delete_performed": False,
        "git_main_push_performed": False,
        "git_force_push_performed": False,
        "provider_requests_made_in_execution": False,
        "predictive_usefulness_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }


def _execute_or_inspect_tags(
    repo_root: Path, run_timestamp_utc: str
) -> tuple[list[dict[str, Any]], int, int, int, int, int]:
    tag_count_before = _count_tag_refs(repo_root)
    namespace_before = _count_tag_refs(repo_root, "marketflow/expectancy-lab/")
    existing_records: dict[str, dict[str, Any]] = {}
    missing_specs: list[dict[str, Any]] = []
    created_names: list[str] = []
    try:
        for spec in APPROVED_TERMINAL_TAGS:
            _verify_target_commit(repo_root, spec["target_commit"])
            object_sha = _tag_ref(repo_root, spec["tag_name"])
            if object_sha is None:
                missing_specs.append(spec)
            else:
                existing_records[spec["tag_name"]] = _inspect_existing_tag(
                    repo_root, spec, object_sha
                )
        for spec in missing_specs:
            _run_git(
                repo_root,
                "tag",
                "-a",
                spec["tag_name"],
                spec["target_commit"],
                "-m",
                spec["tag_message"],
                env={"GIT_COMMITTER_DATE": run_timestamp_utc},
            )
            created_names.append(spec["tag_name"])
        records = []
        for spec in APPROVED_TERMINAL_TAGS:
            if spec["tag_name"] in existing_records:
                records.append(existing_records[spec["tag_name"]])
                continue
            object_sha = _tag_ref(repo_root, spec["tag_name"])
            if object_sha is None:
                raise MarketFlowRepositoryTaggingExecutionError(
                    f"created tag {spec['tag_name']} cannot be resolved"
                )
            record = _inspect_existing_tag(repo_root, spec, object_sha)
            record["tag_status"] = TAG_STATUS_CREATED
            records.append(record)
        tag_count_after = _count_tag_refs(repo_root)
        namespace_after = _count_tag_refs(repo_root, "marketflow/expectancy-lab/")
        return (
            records,
            tag_count_before,
            namespace_before,
            tag_count_after,
            namespace_after,
            len(created_names),
        )
    except (MarketFlowRepositoryTaggingExecutionError, OSError) as exc:
        blocked = _blocked_artifact(str(exc), created_names)
        raise MarketFlowRepositoryTaggingExecutionBlockedError(
            str(exc), blocked_artifact=blocked
        ) from exc


def _base_execution(
    *,
    run_timestamp_utc: str,
    records: list[dict[str, Any]],
    tag_count_before: int,
    namespace_before: int,
    tag_count_after: int,
    namespace_after: int,
    created_count: int,
    tracked_marketflow_file_count: int,
    fixture_mode: bool,
) -> dict[str, Any]:
    existing_count = len(records) - created_count
    observation_note = (
        "Observed expected 28/0 before and 32/4 after local tag creation."
        if (tag_count_before, namespace_before, tag_count_after, namespace_after)
        == (28, 0, 32, 4)
        else "Recorded actual live tag counts; they differ from the first-run expectation."
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED,
        "execution_scope": REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "planning_only": True,
        "governance_only": True,
        "deterministic_fixture_mode": fixture_mode,
        "source_tagging_approval_artifact_kind": source_approval_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED,
        "source_tagging_approval_status": source_approval_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED,
        "source_tagging_approval_scope": source_approval_service.REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
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
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_approval_commit": EXPECTED_SOURCE_APPROVAL_COMMIT,
        "source_snapshot_local_branch_count": 290,
        "source_snapshot_remote_branch_count": 261,
        "source_snapshot_total_branch_ref_count": 551,
        "source_post_plan_push_live_local_branch_count": 290,
        "source_post_plan_push_live_remote_branch_count": 262,
        "source_post_plan_push_live_total_branch_ref_count": 552,
        "source_inventory_operator_review_live_local_branch_count": 291,
        "source_inventory_operator_review_live_remote_branch_count": 263,
        "source_inventory_operator_review_live_total_branch_ref_count": 554,
        "source_tagging_candidate_live_local_branch_count": 292,
        "source_tagging_candidate_live_remote_branch_count": 264,
        "source_tagging_candidate_live_total_branch_ref_count": 556,
        "source_tagging_operator_review_live_local_branch_count": 293,
        "source_tagging_operator_review_live_remote_branch_count": 265,
        "source_tagging_operator_review_live_total_branch_ref_count": 558,
        "source_tagging_approval_live_local_branch_count": 294,
        "source_tagging_approval_live_remote_branch_count": 266,
        "source_tagging_approval_live_total_branch_ref_count": 560,
        "repository_tagging_release_strategy_selected": True,
        "repository_tagging_release_strategy_approved": True,
        "repository_tagging_release_strategy_authorized": True,
        "repository_tagging_release_strategy_executed": True,
        "repository_tags_created": True,
        "git_tag_created": True,
        "local_annotated_tags_created": True,
        "created_terminal_tag_count": created_count,
        "existing_matching_terminal_tag_count": existing_count,
        "approved_terminal_tag_count": 4,
        "ready_for_repository_tagging_execution_results_review": True,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
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
        "terminal_tag_execution_records": deepcopy(records),
        "tag_count_summary": {
            "tag_count_before_execution": tag_count_before,
            "candidate_namespace_tag_count_before_execution": namespace_before,
            "approved_terminal_tag_count": 4,
            "created_terminal_tag_count": created_count,
            "existing_matching_terminal_tag_count": existing_count,
            "tag_count_after_execution": tag_count_after,
            "candidate_namespace_tag_count_after_execution": namespace_after,
            "tag_count_observation_note": observation_note,
        },
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": tracked_marketflow_file_count,
        "no_tracked_marketflow_files": tracked_marketflow_file_count == 0,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1",
    }


def _check_values(execution: Mapping[str, Any]) -> dict[str, bool]:
    records = execution.get("terminal_tag_execution_records", [])
    summary = execution.get("tag_count_summary", {})
    names = [row.get("tag_name") for row in records] if isinstance(records, list) else []
    targets = [row.get("target_commit") for row in records] if isinstance(records, list) else []
    expected_targets = [row["target_commit"] for row in APPROVED_TERMINAL_TAGS]
    statuses = {TAG_STATUS_CREATED, TAG_STATUS_EXISTING}
    return {
        "source_approval_digest_bound": execution.get("source_tagging_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": execution.get("source_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": execution.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest_bound": execution.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": execution.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": execution.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": execution.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": execution.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": execution.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": execution.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": execution.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": execution.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": execution.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": execution.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": execution.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "selected_package_terminal_archive_tags": execution.get("selected_tagging_package") == SELECTED_TAGGING_PACKAGE,
        "approval_status_bound": execution.get("source_tagging_approval_status") == source_approval_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED,
        "strategy_authorized_true": execution.get("repository_tagging_release_strategy_authorized") is True,
        "tagging_execution_performed_true": execution.get("repository_tagging_release_strategy_executed") is True,
        "local_annotated_tags_created_true": execution.get("repository_tags_created") is True and execution.get("git_tag_created") is True and execution.get("local_annotated_tags_created") is True,
        "approved_terminal_tag_count_4": execution.get("approved_terminal_tag_count") == len(records) == 4,
        "created_or_existing_matching_terminal_tag_count_4": execution.get("created_terminal_tag_count", -1) + execution.get("existing_matching_terminal_tag_count", -1) == 4 and all(row.get("tag_status") in statuses for row in records),
        "terminal_tag_names_match": names == APPROVED_TERMINAL_TAG_NAMES,
        "terminal_tag_targets_match": targets == expected_targets and all(row.get("tag_target_commit_verified") is True for row in records),
        "terminal_tag_messages_verified": all(row.get("tag_message_verified") is True and row.get("tag_message") == spec["tag_message"] for row, spec in zip(records, APPROVED_TERMINAL_TAGS)),
        "tag_objects_are_annotated": all(row.get("tag_type") == "ANNOTATED" and isinstance(row.get("tag_object_sha"), str) and TAG_OBJECT_SHA_PATTERN.fullmatch(row["tag_object_sha"]) for row in records),
        "tag_count_summary_recorded": isinstance(summary, dict) and summary.get("approved_terminal_tag_count") == 4 and summary.get("created_terminal_tag_count") == execution.get("created_terminal_tag_count") and summary.get("existing_matching_terminal_tag_count") == execution.get("existing_matching_terminal_tag_count") and isinstance(summary.get("tag_count_before_execution"), int) and isinstance(summary.get("tag_count_after_execution"), int),
        "candidate_namespace_tag_count_after_execution_4": summary.get("candidate_namespace_tag_count_after_execution") == 4,
        "tags_pushed_false": execution.get("repository_tags_pushed") is False and all(row.get("tag_pushed") is False for row in records),
        "git_tag_push_performed_false": execution.get("git_tag_push_performed") is False,
        "merge_performed_false": execution.get("git_merge_performed") is False,
        "rebase_performed_false": execution.get("git_rebase_performed") is False,
        "branch_delete_performed_false": execution.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": execution.get("git_remote_delete_performed") is False,
        "main_push_false": execution.get("git_main_push_performed") is False,
        "force_push_false": execution.get("git_force_push_performed") is False,
        "remote_prune_false": execution.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": execution.get("origin_main_modified_by_this_task") is False,
        "marketflow_outputs_not_tracked": execution.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": execution.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": execution.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_generation_false": execution.get("dataset_generation_performed_in_execution") is False,
        "metric_recomputation_false": execution.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": execution.get("model_training_performed") is False,
        "strategy_scoring_false": execution.get("strategy_scoring_performed") is False,
        "recommendations_false": execution.get("trade_recommendations_generated") is False and all(row.get("trade_recommendations_generated") is False for row in records),
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
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "execution condition satisfied" if actual else "execution condition failed",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(execution)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(execution: Mapping[str, Any], checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row.get("status") == PASS for row in rows)
    failed = len(rows) - passed
    return {
        "total_checks": len(rows),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "repository_tagging_release_strategy_executed": True,
        "repository_tags_created": True,
        "local_annotated_tags_created": True,
        "created_terminal_tag_count": execution["created_terminal_tag_count"],
        "existing_matching_terminal_tag_count": execution["existing_matching_terminal_tag_count"],
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tagging_execution_tag_manifest_digest_v1(
    execution_or_records: Mapping[str, Any] | list[dict[str, Any]],
) -> str:
    """Digest the four exact annotated-tag execution records."""
    records = (
        execution_or_records["terminal_tag_execution_records"]
        if isinstance(execution_or_records, Mapping)
        else execution_or_records
    )
    return semantic_digest({"terminal_tag_execution_records": records})


def marketflow_repository_tagging_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for an execution artifact."""
    payload = deepcopy(dict(execution))
    payload.pop("marketflow_repository_tagging_execution_digest", None)
    return semantic_digest(payload)


def execute_marketflow_repository_tagging_v1(
    *,
    repo_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    execute_git_operations: bool = True,
) -> dict[str, Any]:
    """Create or verify only the four approved local annotated tags."""
    timestamp = run_timestamp_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise MarketFlowRepositoryTaggingExecutionError("run_timestamp_utc is required")
    if execute_git_operations:
        root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
        root = root.resolve()
        actual_root = Path(_run_git(root, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
        if actual_root != root:
            raise MarketFlowRepositoryTaggingExecutionError("repo_root is not a Git repository root")
        (
            records,
            tag_count_before,
            namespace_before,
            tag_count_after,
            namespace_after,
            created_count,
        ) = _execute_or_inspect_tags(root, timestamp)
        tracked_marketflow_file_count = len(
            [line for line in _run_git(root, "ls-files", "--", ".marketflow").stdout.splitlines() if line]
        )
    else:
        records = _fixture_records()
        tag_count_before, namespace_before = 28, 0
        tag_count_after, namespace_after = 32, 4
        created_count = 4
        tracked_marketflow_file_count = 0
    execution = _base_execution(
        run_timestamp_utc=timestamp,
        records=records,
        tag_count_before=tag_count_before,
        namespace_before=namespace_before,
        tag_count_after=tag_count_after,
        namespace_after=namespace_after,
        created_count=created_count,
        tracked_marketflow_file_count=tracked_marketflow_file_count,
        fixture_mode=not execute_git_operations,
    )
    execution["marketflow_repository_tagging_execution_tag_manifest_digest"] = (
        marketflow_repository_tagging_execution_tag_manifest_digest_v1(execution)
    )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution, execution["checklist"])
    if execution["summary"]["blocker_count"]:
        raise MarketFlowRepositoryTaggingExecutionError(
            "repository tagging execution contains blockers"
        )
    execution["marketflow_repository_tagging_execution_digest"] = (
        marketflow_repository_tagging_execution_digest_v1(execution)
    )
    validate_marketflow_repository_tagging_execution_v1(execution)
    return execution


def validate_marketflow_repository_tagging_execution_v1(
    execution: dict[str, Any],
) -> dict[str, Any]:
    """Validate exact tags, evidence, counts, and all closed authority boundaries."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryTaggingExecutionError("execution must be an object")
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1,
        "execution_status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED,
        "execution_scope": REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_approval_commit": EXPECTED_SOURCE_APPROVAL_COMMIT,
        "repository_tagging_release_strategy_authorized": True,
        "repository_tagging_release_strategy_executed": True,
        "repository_tags_created": True,
        "local_annotated_tags_created": True,
        "approved_terminal_tag_count": 4,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "git_merge_performed": False,
        "git_rebase_performed": False,
        "git_branch_delete_performed": False,
        "git_remote_delete_performed": False,
        "git_main_push_performed": False,
        "git_force_push_performed": False,
        "git_remote_prune_performed": False,
        "origin_main_modified_by_this_task": False,
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
        "broker_execution": NOT_AUTHORIZED,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryTaggingExecutionError(f"{field} mismatch")
    records = execution.get("terminal_tag_execution_records")
    if not isinstance(records, list) or len(records) != 4:
        raise MarketFlowRepositoryTaggingExecutionError("terminal tag records mismatch")
    for record, spec in zip(records, APPROVED_TERMINAL_TAGS):
        for field in (
            "tag_name",
            "target_branch",
            "target_commit",
            "source_artifact_kind",
            "source_artifact_status",
            "source_decision",
            "source_digest",
            "tag_message",
        ):
            if record.get(field) != spec[field]:
                raise MarketFlowRepositoryTaggingExecutionError(
                    f"terminal tag {field} mismatch"
                )
        if record.get("tag_status") not in {TAG_STATUS_CREATED, TAG_STATUS_EXISTING}:
            raise MarketFlowRepositoryTaggingExecutionError("terminal tag status mismatch")
        if record.get("tag_type") != "ANNOTATED":
            raise MarketFlowRepositoryTaggingExecutionError("terminal tag is not annotated")
        if not isinstance(record.get("tag_object_sha"), str) or not TAG_OBJECT_SHA_PATTERN.fullmatch(record["tag_object_sha"]):
            raise MarketFlowRepositoryTaggingExecutionError("terminal tag object SHA mismatch")
        for field in ("tag_target_commit_verified", "tag_message_verified", "tag_created"):
            if record.get(field) is not True:
                raise MarketFlowRepositoryTaggingExecutionError(f"{field} must be true")
        for field in (
            "tag_pushed",
            "main_push_required",
            "runtime_authority_created",
            "predictive_usefulness_accepted",
            "profitability_accepted",
            "trade_recommendations_generated",
        ):
            if record.get(field) is not False:
                raise MarketFlowRepositoryTaggingExecutionError(f"{field} must be false")
    if execution.get("created_terminal_tag_count", -1) + execution.get("existing_matching_terminal_tag_count", -1) != 4:
        raise MarketFlowRepositoryTaggingExecutionError("created/existing tag count mismatch")
    manifest_digest = execution.get(
        "marketflow_repository_tagging_execution_tag_manifest_digest"
    )
    if manifest_digest != marketflow_repository_tagging_execution_tag_manifest_digest_v1(execution):
        raise MarketFlowRepositoryTaggingExecutionError("tag manifest digest mismatch")
    checklist = execution.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(execution):
        raise MarketFlowRepositoryTaggingExecutionError("execution checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTaggingExecutionError("execution checklist failed")
    if execution.get("summary") != _summary(execution, checklist):
        raise MarketFlowRepositoryTaggingExecutionError("execution summary mismatch")
    digest = execution.get("marketflow_repository_tagging_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTaggingExecutionError("execution digest missing")
    if digest != marketflow_repository_tagging_execution_digest_v1(execution):
        raise MarketFlowRepositoryTaggingExecutionError("execution digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_VALID,
        "artifact_kind": execution["artifact_kind"],
        "execution_status": execution["execution_status"],
        "marketflow_repository_tagging_execution_digest": digest,
        "marketflow_repository_tagging_execution_tag_manifest_digest": manifest_digest,
        **{
            field: execution["summary"][field]
            for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tagging_execution_markdown_v1(
    execution: dict[str, Any],
) -> str:
    """Render a sanitized Markdown report for a validated local execution."""
    validation = validate_marketflow_repository_tagging_execution_v1(execution)
    sections = [
        ("Title", ["MarketFlow Repository Tagging Execution v1"]),
        ("MarketFlow Repository Tagging Execution v1", [f"Artifact/status: `{execution['artifact_kind']}` / `{execution['execution_status']}`.", f"Execution digest: `{validation['marketflow_repository_tagging_execution_digest']}`.", f"Tag manifest digest: `{validation['marketflow_repository_tagging_execution_tag_manifest_digest']}`."]),
        ("Source Approval", [f"Approval digest: `{execution['source_tagging_approval_digest']}`.", f"Approval commit: `{execution['source_approval_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(execution['source_evidence'])}."]),
        ("Repository Context", [f"Frozen origin/main: `{execution['origin_main_commit']}`.", "Source observations end at 294 local / 266 remote / 560 total branch refs."]),
        ("Execution Scope", [execution["execution_scope"]]),
        ("Created Local Annotated Tags", [f"`{row['tag_name']}` -> `{row['target_commit']}` (`{row['tag_status']}`, object `{row['tag_object_sha']}`)" for row in execution["terminal_tag_execution_records"]]),
        ("Tag Count Summary", [f"Before/after total: {execution['tag_count_summary']['tag_count_before_execution']} / {execution['tag_count_summary']['tag_count_after_execution']}.", f"Before/after namespace: {execution['tag_count_summary']['candidate_namespace_tag_count_before_execution']} / {execution['tag_count_summary']['candidate_namespace_tag_count_after_execution']}. "]),
        ("Tag Messages", [row["tag_message"] for row in execution["terminal_tag_execution_records"]]),
        ("Next Chain", list(execution["next_chain"])),
        ("Next Gates", list(execution["next_gates"])),
        ("Risk Controls", list(execution["risk_controls"])),
        ("Authority Boundaries", ["Tags exist only locally. No push, merge, deletion, main mutation, predictive/profitability acceptance, runtime, broker, or trading authority is created."]),
        ("Checklist Summary", [f"{execution['summary']['passed_checks']} / {execution['summary']['total_checks']} checks pass; {execution['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No provider, data, metric, model, recommendation, runtime, broker, tag-push, merge, delete, main-push, force-push, prune, or .marketflow mutation occurred."]),
    ]
    lines = ["# MarketFlow Repository Tagging Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
