"""Offline candidate for future publication of four verified governance tags."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_tagging_execution_results_review_service as source_review_service,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1 = (
    "marketflow_repository_tag_push_strategy_candidate_v1"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_VALID = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_VALID"
)

EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST = (
    "d63ce543d95b936cee8ec5fb8f85c17fc20a3cf66a73d7774e8f55d23f7fad4a"
)
EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST = (
    "cfcc8411902b65aa28e02d2987b4b180dbbb5e344228d31833243657a0c281e3"
)
EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST = source_review_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_TAGGING_EXECUTION_TAG_MANIFEST_DIGEST = (
    source_review_service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST
)
EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST = source_review_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_review_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_review_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_review_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_review_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_review_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_review_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_review_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_review_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_review_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_review_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_review_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT = "5daeecb556e4964eda623e5db89142f0e2e0db90"
SOURCE_EVIDENCE = deepcopy(source_review_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN = (
    "PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN"
)
PACKAGE_KEEP_TAGS_LOCAL_ONLY = "PACKAGE_KEEP_TAGS_LOCAL_ONLY"
PACKAGE_DELAY_REMOTE_TAG_PUBLICATION_UNTIL_MERGE_STRATEGY = (
    "PACKAGE_DELAY_REMOTE_TAG_PUBLICATION_UNTIL_MERGE_STRATEGY"
)
PACKAGE_CREATE_BACKUP_OR_BUNDLE_BEFORE_REMOTE_TAG_PUBLICATION = (
    "PACKAGE_CREATE_BACKUP_OR_BUNDLE_BEFORE_REMOTE_TAG_PUBLICATION"
)

TAG_PUSH_PHILOSOPHY = (
    "Remote tag publication should only publish verified local annotated governance "
    "tags after separate operator review and approval, without implying predictive "
    "usefulness, profitability, runtime readiness, or trading authority."
)
TAG_PUSH_BOUNDARY = (
    "Candidate-only; no tag is pushed, no tag is created, no branch is merged or "
    "deleted, and main remains untouched."
)
TAG_PUSH_GOAL = (
    "Prepare a future decision on whether the four local annotated expectancy-lab "
    "archive tags should be published to origin for remote governance traceability."
)


def _candidate_remote_ref(tag_name: str) -> str:
    return f"refs/tags/{tag_name}"


TAG_PUSH_RECORDS = [
    {
        "tag_name": row["tag_name"],
        "local_tag_object_sha": row["tag_object_sha"],
        "target_commit": row["target_commit"],
        "source_artifact_kind": row["source_artifact_kind"],
        "source_digest": row["source_digest"],
        "local_tag_verified_by_source_review": True,
        "remote_ref_exists_in_source_review": False,
        "candidate_remote_ref": _candidate_remote_ref(row["tag_name"]),
        "candidate_push_status": "CANDIDATE_NOT_PUSHED",
        "selected_for_push": False,
        "approved_for_push": False,
        "pushed": False,
        "push_approval_required": True,
        "main_push_required": False,
        "runtime_authority_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "trade_recommendations_generated": False,
    }
    for row in source_review_service.EXPECTED_TAGS
]
CANDIDATE_REMOTE_REFS = [row["candidate_remote_ref"] for row in TAG_PUSH_RECORDS]

TAG_PUSH_PACKAGES = [
    {
        "package_id": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Publish exactly the four verified local annotated expectancy-lab archive "
            "tags to origin."
        ),
        "candidate_remote_refs": list(CANDIDATE_REMOTE_REFS),
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_pushed": False,
        "main_push_required": False,
    },
    {
        "package_id": PACKAGE_KEEP_TAGS_LOCAL_ONLY,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Keep the four governance tags local and do not publish to origin.",
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_pushed": False,
    },
    {
        "package_id": PACKAGE_DELAY_REMOTE_TAG_PUBLICATION_UNTIL_MERGE_STRATEGY,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Delay tag publication until the merge strategy candidate has been reviewed.",
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_pushed": False,
    },
    {
        "package_id": PACKAGE_CREATE_BACKUP_OR_BUNDLE_BEFORE_REMOTE_TAG_PUBLICATION,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Require a repository backup or git bundle before remote tag publication.",
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_pushed": False,
    },
]

CANDIDATE_PUSH_COMMAND_TEMPLATE = """git push origin \\
  refs/tags/marketflow/expectancy-lab/final-archive-not-ready/v1 \\
  refs/tags/marketflow/expectancy-lab/archive-record-not-ready/v1 \\
  refs/tags/marketflow/expectancy-lab/operator-selection-option-a/v1 \\
  refs/tags/marketflow/expectancy-lab/readiness-not-ready/v1"""

TAG_PUSH_PREREQUISITES = {
    "operator_review_of_tag_push_candidate_required": True,
    "operator_approval_required_before_tag_push": True,
    "working_tree_clean_required_before_tag_push": True,
    "origin_main_protection_required": True,
    "local_tags_must_be_reverified_before_push": True,
    "remote_refs_must_be_absent_or_matching_before_push": True,
    "mismatched_remote_ref_blocks_push": True,
    "tag_push_must_use_explicit_refspecs": True,
    "tag_push_all_tags_forbidden": True,
    "main_push_forbidden": True,
    "branch_push_forbidden": True,
    "force_push_forbidden": True,
    "separate_results_review_required_after_tag_push": True,
}

TAG_PUSH_NON_GOALS = [
    "do_not_push_tags_now",
    "do_not_push_all_tags",
    "do_not_push_main",
    "do_not_push_branches",
    "do_not_force_push",
    "do_not_delete_remote_tags",
    "do_not_modify_local_tags",
    "do_not_create_new_tags",
    "do_not_merge_now",
    "do_not_delete_branches_now",
    "do_not_cleanup_now",
    "do_not_imply_predictive_usefulness_acceptance",
    "do_not_imply_profitability_acceptance",
    "do_not_imply_runtime_authority",
    "do_not_imply_trading_authority",
]

NEXT_CHAIN = [
    "Repository Tag Push Strategy Operator Review v1.",
    "Repository Tag Push Approval v1, if selected.",
    "Repository Tag Push Execution v1, if approved.",
    "Repository Tag Push Results Review v1.",
    "Repository Merge Strategy Candidate v1, only after tag-push decision or explicit local-only decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tag_push_strategy_operator_review",
    "repository_tag_push_approval_if_selected",
    "repository_tag_push_execution_if_approved",
    "repository_tag_push_results_review",
    "repository_merge_strategy_candidate_after_tag_push_decision",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "candidate_does_not_push_tags",
    "candidate_does_not_create_tags",
    "candidate_does_not_modify_tags",
    "candidate_does_not_delete_tags",
    "candidate_does_not_push_all_tags",
    "candidate_does_not_push_branches",
    "candidate_does_not_push_main",
    "candidate_does_not_force_push",
    "candidate_does_not_merge",
    "candidate_does_not_rebase",
    "candidate_does_not_delete_branches",
    "candidate_does_not_delete_remote_branches",
    "candidate_does_not_prune_remotes",
    "candidate_does_not_modify_origin_main",
    "candidate_does_not_modify_marketflow_outputs",
    "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data",
    "candidate_does_not_regenerate_dataset",
    "candidate_does_not_rerun_tagging_results_review",
    "candidate_does_not_rerun_tagging_execution",
    "candidate_does_not_rerun_tagging_approval",
    "candidate_does_not_rerun_inventory",
    "candidate_does_not_rerun_evidence",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_train_models",
    "candidate_does_not_score_strategy",
    "candidate_does_not_generate_recommendations",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_broker_execution",
    "all_push_actions_are_candidate_only",
    "operator_review_required_before_tag_push",
    "operator_approval_required_before_tag_push",
    "explicit_refspec_required_for_future_push",
    "push_all_tags_forbidden",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_results_review_digest_bound",
    "source_tag_manifest_review_digest_bound",
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
    "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound",
    "records_digest_bound",
    "origin_main_commit_bound",
    "source_tag_review_ready_true",
    "candidate_created_true",
    "candidate_ready_true",
    "recommended_push_package_present",
    "push_packages_present_4",
    "candidate_push_records_present_4",
    "candidate_remote_refs_present_4",
    "local_tag_object_shas_bound",
    "target_commits_bound",
    "remote_refs_absent_in_source_review",
    "push_command_template_present",
    "push_command_not_executed",
    "tag_push_strategy_selected_false",
    "tag_push_strategy_approved_false",
    "tag_push_strategy_authorized_false",
    "tag_push_strategy_executed_false",
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


class MarketFlowRepositoryTagPushStrategyCandidateError(ValueError):
    """Raised when the candidate violates evidence or authority boundaries."""


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_review, dict):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "source_review must be an object"
        )
    try:
        source_review_service.validate_marketflow_repository_tagging_execution_results_review_v1(
            source_review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "source tagging results review is invalid"
        ) from exc
    if source_review.get(
        "marketflow_repository_tagging_execution_results_review_digest"
    ) != EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST:
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "source tagging results review digest mismatch"
        )
    if source_review.get(
        "marketflow_repository_tagging_execution_results_review_tag_manifest_digest"
    ) != EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST:
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "source tagging results review tag manifest digest mismatch"
        )
    return deepcopy(source_review["source_evidence"])


def _base_candidate(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True,
        "planning_only": True,
        "governance_only": True,
        "operator_review_required": True,
        "source_tagging_results_review_artifact_kind": source_review_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1,
        "source_tagging_results_review_status": source_review_service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY,
        "source_tagging_results_review_scope": source_review_service.REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST,
        "source_tagging_results_review_tag_manifest_digest": EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST,
        "source_tagging_execution_tag_manifest_digest": EXPECTED_SOURCE_TAGGING_EXECUTION_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST,
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
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_results_review_commit": EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT,
        "source_branch_inventory": {
            "local_branch_count": 296,
            "remote_branch_count": 268,
            "total_ref_count": 564,
        },
        "source_tag_counts": {
            "tag_count_before_execution_from_source": 28,
            "candidate_namespace_tag_count_before_execution_from_source": 0,
            "tag_count_after_execution_from_source": 32,
            "candidate_namespace_tag_count_after_execution_from_source": 4,
            "observed_tag_count_at_review": 32,
            "observed_candidate_namespace_tag_count_at_review": 4,
            "approved_terminal_tag_count": 4,
            "verified_terminal_tag_count": 4,
            "extra_candidate_namespace_tag_count": 0,
            "remote_approved_tag_count": 0,
        },
        "source_tag_review_ready": True,
        "repository_tag_push_strategy_candidate_created": True,
        "repository_tag_push_strategy_candidate_ready_for_operator_review": True,
        "ready_for_repository_tag_push_strategy_operator_review": True,
        "repository_tag_push_strategy_selected": False,
        "repository_tag_push_strategy_approved": False,
        "repository_tag_push_strategy_authorized": False,
        "repository_tag_push_strategy_executed": False,
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
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
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
        "tag_push_philosophy": TAG_PUSH_PHILOSOPHY,
        "tag_push_boundary": TAG_PUSH_BOUNDARY,
        "tag_push_goal": TAG_PUSH_GOAL,
        "tag_push_packages": deepcopy(TAG_PUSH_PACKAGES),
        "recommended_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": (
            "The four tags have been verified as local annotated governance tags, remain "
            "unpublished on origin, and correspond to terminal archived-not-ready evidence milestones."
        ),
        "candidate_push_records": deepcopy(TAG_PUSH_RECORDS),
        "candidate_push_command_template": CANDIDATE_PUSH_COMMAND_TEMPLATE,
        "command_status": "PLANNED_NOT_EXECUTED",
        "remote_publication_status": "NOT_PUSHED",
        "remote_publication_approval_required": True,
        "remote_publication_execution_requires_separate_task": True,
        "tag_push_prerequisites": deepcopy(TAG_PUSH_PREREQUISITES),
        "tag_push_non_goals": list(TAG_PUSH_NON_GOALS),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1",
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    records = candidate.get("candidate_push_records", [])
    packages = candidate.get("tag_push_packages", [])
    return {
        "source_results_review_digest_bound": candidate.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest_bound": candidate.get("source_tagging_results_review_tag_manifest_digest") == EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST,
        "source_execution_digest_bound": candidate.get("source_tagging_execution_digest") == EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST,
        "source_tag_manifest_digest_bound": candidate.get("source_tagging_execution_tag_manifest_digest") == EXPECTED_SOURCE_TAGGING_EXECUTION_TAG_MANIFEST_DIGEST,
        "source_approval_digest_bound": candidate.get("source_tagging_approval_digest") == EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": candidate.get("source_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": candidate.get("source_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest_bound": candidate.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": candidate.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": candidate.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": candidate.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": candidate.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": candidate.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": candidate.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest_bound": candidate.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": candidate.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": candidate.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": candidate.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_tag_review_ready_true": candidate.get("source_tag_review_ready") is True,
        "candidate_created_true": candidate.get("repository_tag_push_strategy_candidate_created") is True,
        "candidate_ready_true": candidate.get("repository_tag_push_strategy_candidate_ready_for_operator_review") is True and candidate.get("ready_for_repository_tag_push_strategy_operator_review") is True,
        "recommended_push_package_present": candidate.get("recommended_tag_push_package") == PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "push_packages_present_4": packages == TAG_PUSH_PACKAGES and len(packages) == 4,
        "candidate_push_records_present_4": records == TAG_PUSH_RECORDS and len(records) == 4,
        "candidate_remote_refs_present_4": [row.get("candidate_remote_ref") for row in records] == CANDIDATE_REMOTE_REFS,
        "local_tag_object_shas_bound": [row.get("local_tag_object_sha") for row in records] == source_review_service.EXPECTED_TAG_OBJECT_SHAS,
        "target_commits_bound": [row.get("target_commit") for row in records] == [row["target_commit"] for row in source_review_service.EXPECTED_TAGS],
        "remote_refs_absent_in_source_review": all(row.get("remote_ref_exists_in_source_review") is False for row in records),
        "push_command_template_present": candidate.get("candidate_push_command_template") == CANDIDATE_PUSH_COMMAND_TEMPLATE,
        "push_command_not_executed": candidate.get("command_status") == "PLANNED_NOT_EXECUTED" and candidate.get("remote_publication_status") == "NOT_PUSHED",
        "tag_push_strategy_selected_false": candidate.get("repository_tag_push_strategy_selected") is False,
        "tag_push_strategy_approved_false": candidate.get("repository_tag_push_strategy_approved") is False,
        "tag_push_strategy_authorized_false": candidate.get("repository_tag_push_strategy_authorized") is False,
        "tag_push_strategy_executed_false": candidate.get("repository_tag_push_strategy_executed") is False,
        "tags_pushed_false": candidate.get("repository_tags_pushed") is False and all(row.get("pushed") is False for row in records),
        "git_tag_push_performed_false": candidate.get("git_tag_push_performed") is False,
        "additional_tags_created_false": candidate.get("additional_tags_created") is False,
        "tags_modified_false": candidate.get("tags_modified") is False,
        "tags_deleted_false": candidate.get("tags_deleted") is False,
        "merge_performed_false": candidate.get("git_merge_performed") is False,
        "rebase_performed_false": candidate.get("git_rebase_performed") is False,
        "branch_delete_performed_false": candidate.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": candidate.get("git_remote_delete_performed") is False,
        "main_push_false": candidate.get("git_main_push_performed") is False,
        "force_push_false": candidate.get("git_force_push_performed") is False,
        "remote_prune_false": candidate.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": candidate.get("origin_main_modified_by_this_task") is False,
        "marketflow_outputs_not_tracked": candidate.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": candidate.get("provider_requests_made_in_candidate") is False,
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed_in_candidate") is False,
        "dataset_generation_false": candidate.get("dataset_generation_performed_in_candidate") is False,
        "metric_recomputation_false": candidate.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": candidate.get("model_training_performed") is False,
        "strategy_scoring_false": candidate.get("strategy_scoring_performed") is False,
        "recommendations_false": candidate.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness") == NOT_ACCEPTED and candidate.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": candidate.get("profitability") == NOT_ACCEPTED and candidate.get("profitability_accepted") is False,
        "runtime_not_authorized": candidate.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": candidate.get("broker_execution") == NOT_AUTHORIZED,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": actual,
        "severity": BLOCKER,
        "message": (
            "tag push candidate evidence matches"
            if actual
            else "tag push candidate evidence mismatch"
        ),
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(candidate)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_tag_push_strategy_candidate_created": True,
        "repository_tag_push_strategy_candidate_ready_for_operator_review": True,
        "recommended_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "candidate_push_tag_count": 4,
        "tags_pushed": False,
        "git_tag_push_performed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tag_push_strategy_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tag_push_strategy_candidate_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tag_push_strategy_candidate_v1(
    *, source_review: dict | None = None,
) -> dict:
    """Build the candidate from committed constants without inspecting Git refs."""
    candidate = _base_candidate(source_review)
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_tag_push_strategy_candidate_digest"] = (
        marketflow_repository_tag_push_strategy_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_tag_push_strategy_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_tag_push_strategy_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate exact evidence bindings and all closed execution gates."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "candidate must be an object"
        )
    expected = _base_candidate(None)
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise MarketFlowRepositoryTagPushStrategyCandidateError(
                f"{field} mismatch"
            )
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(candidate):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate checklist failed"
        )
    if candidate.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate summary mismatch"
        )
    digest = candidate.get("marketflow_repository_tag_push_strategy_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate digest missing"
        )
    if digest != marketflow_repository_tag_push_strategy_candidate_digest_v1(candidate):
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_repository_tag_push_strategy_candidate_digest": digest,
        **{
            key: candidate["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tag_push_strategy_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_marketflow_repository_tag_push_strategy_candidate_v1(candidate)
    sections = [
        ("Title", ["MarketFlow Repository Tag Push Strategy Candidate v1"]),
        (
            "MarketFlow Repository Tag Push Strategy Candidate v1",
            [
                f"Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
                f"Digest: `{validation['marketflow_repository_tag_push_strategy_candidate_digest']}`.",
            ],
        ),
        (
            "Source Tagging Results Review",
            [
                f"Source digest: `{candidate['source_tagging_results_review_digest']}`.",
                f"Source commit: `{candidate['source_results_review_commit']}`.",
            ],
        ),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(candidate['source_evidence'])}."]),
        (
            "Repository Context",
            [
                f"Origin main: `{candidate['origin_main_commit']}`.",
                "Source branch refs: 296 local / 268 remote / 564 total.",
            ],
        ),
        ("Candidate Scope", [candidate["candidate_scope"]]),
        ("Tag Push Philosophy", [candidate["tag_push_philosophy"], candidate["tag_push_boundary"], candidate["tag_push_goal"]]),
        ("Recommended Push Package", [f"`{candidate['recommended_tag_push_package']}`: {candidate['recommendation_reason']}"]),
        ("Candidate Push Packages", [f"{row['package_id']}: {row['status']}" for row in candidate["tag_push_packages"]]),
        ("Candidate Push Records", [f"`{row['tag_name']}` -> `{row['candidate_remote_ref']}` ({row['candidate_push_status']})" for row in candidate["candidate_push_records"]]),
        ("Remote Publication Plan", [candidate["candidate_push_command_template"], candidate["command_status"], candidate["remote_publication_status"]]),
        ("Tag Push Prerequisites", list(candidate["tag_push_prerequisites"])),
        ("Tag Push Non-Goals", list(candidate["tag_push_non_goals"])),
        ("Next Chain", list(candidate["next_chain"])),
        ("Next Gates", list(candidate["next_gates"])),
        ("Risk Controls", list(candidate["risk_controls"])),
        ("Authority Boundaries", ["Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{candidate['summary']['passed_checks']} / {candidate['summary']['total_checks']} checks pass; {candidate['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag push, tag creation, tag modification, tag deletion, merge, rebase, deletion, main push, force-push, prune, provider, data, metric, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tag Push Strategy Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tag_push_strategy_candidate_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_tag_push_strategy_candidate_v1(
        source_review=source_review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tag_push_strategy_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTagPushStrategyCandidateError(
            "tag push candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_repository_tag_push_strategy_candidate_digest": candidate[
            "marketflow_repository_tag_push_strategy_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
