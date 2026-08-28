"""Offline operator review of the repository tag-push strategy candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_tag_push_strategy_candidate_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_tag_push_strategy_operator_review_v1"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_READY"
)
REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "7153f9c97c651fe817046d27a527d30ca2b8280c3d1555ff292a2b83416ac227"
)
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST = (
    source_service.EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST
)
EXPECTED_SOURCE_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_EXECUTION_TAG_MANIFEST_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_TAGGING_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
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
EXPECTED_SOURCE_CANDIDATE_COMMIT = "e960e8f0241d4ca4aeaffaab30fe98d54b206616"
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_TAG_PUSH_PHILOSOPHY = source_service.TAG_PUSH_PHILOSOPHY
REVIEWED_TAG_PUSH_BOUNDARY = (
    "Candidate-only reviewed; no tag is pushed, no tag is created, no tag is modified "
    "or deleted, no branch is merged or deleted, and main remains untouched."
)
REVIEWED_TAG_PUSH_GOAL = source_service.TAG_PUSH_GOAL

REVIEWED_PUSH_PACKAGES = [
    {
        **deepcopy(package),
        "source_status": package["status"],
        "review_status": (
            "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
            if package["package_id"]
            == source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN
            else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        ),
    }
    for package in source_service.TAG_PUSH_PACKAGES
]
for _package in REVIEWED_PUSH_PACKAGES:
    _package.pop("status")

REVIEWED_PUSH_RECORDS = [
    {
        **deepcopy(record),
        "candidate_push_status": "REVIEWED_CANDIDATE_NOT_PUSHED",
    }
    for record in source_service.TAG_PUSH_RECORDS
]

REVIEWED_TAG_PUSH_PREREQUISITES = [
    {
        "prerequisite_id": prerequisite_id,
        "required": required,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_TAG_PUSH",
        "execution_status": "NOT_EXECUTED",
    }
    for prerequisite_id, required in source_service.TAG_PUSH_PREREQUISITES.items()
]

REVIEWED_TAG_PUSH_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source_service.TAG_PUSH_NON_GOALS
]

NEXT_CHAIN = [
    "Repository Tag Push Strategy Approval v1, if selected.",
    "Repository Tag Push Execution v1, if approved.",
    "Repository Tag Push Results Review v1.",
    "Repository Merge Strategy Candidate v1, only after tag-push decision or explicit local-only decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tag_push_strategy_approval_if_selected",
    "repository_tag_push_execution_if_approved",
    "repository_tag_push_results_review",
    "repository_merge_strategy_candidate_after_tag_push_decision",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "review_does_not_select_tag_push_package",
    "review_does_not_approve_tag_push",
    "review_does_not_push_tags",
    "review_does_not_create_tags",
    "review_does_not_modify_tags",
    "review_does_not_delete_tags",
    "review_does_not_push_all_tags",
    "review_does_not_push_branches",
    "review_does_not_push_main",
    "review_does_not_force_push",
    "review_does_not_merge",
    "review_does_not_rebase",
    "review_does_not_delete_branches",
    "review_does_not_delete_remote_branches",
    "review_does_not_prune_remotes",
    "review_does_not_modify_origin_main",
    "review_does_not_modify_marketflow_outputs",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset",
    "review_does_not_rerun_tag_push_candidate",
    "review_does_not_rerun_tagging_results_review",
    "review_does_not_rerun_tagging_execution",
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
    "all_push_actions_remain_candidate_only",
    "operator_approval_required_before_tag_push",
    "explicit_refspec_required_for_future_push",
    "push_all_tags_forbidden",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound",
    "source_results_review_digest_bound",
    "source_tag_manifest_review_digest_bound",
    "source_execution_digest_bound",
    "source_tag_manifest_digest_bound",
    "source_approval_digest_bound",
    "source_operator_review_digest_bound",
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
    "source_candidate_ready_true",
    "review_created_true",
    "review_ready_true",
    "push_packages_reviewed_true",
    "push_records_reviewed_true",
    "push_prerequisites_reviewed_true",
    "push_policy_reviewed_true",
    "ready_for_approval_false",
    "recommended_push_package_reviewed_not_selected",
    "push_packages_reviewed_4",
    "candidate_push_records_reviewed_4",
    "candidate_remote_refs_reviewed_4",
    "local_tag_object_shas_bound",
    "target_commits_bound",
    "remote_refs_absent_in_source_review",
    "push_command_template_reviewed",
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
    "non_goals_reviewed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryTagPushStrategyOperatorReviewError(ValueError):
    """Raised when the review violates evidence or authority boundaries."""


def _source_evidence(source_candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_candidate is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_candidate, dict):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "source_candidate must be an object"
        )
    try:
        source_service.validate_marketflow_repository_tag_push_strategy_candidate_v1(
            source_candidate
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "source tag-push candidate is invalid"
        ) from exc
    if source_candidate.get(
        "marketflow_repository_tag_push_strategy_candidate_digest"
    ) != EXPECTED_SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "source tag-push candidate digest mismatch"
        )
    return deepcopy(source_candidate["source_evidence"])


def _base_review(source_candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True,
        "planning_only": True,
        "governance_only": True,
        "operator_review_required": True,
        "source_tag_push_candidate_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1,
        "source_tag_push_candidate_status": source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_tag_push_candidate_scope": source_service.REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tagging_execution_tag_manifest_digest": EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_TAGGING_CANDIDATE_DIGEST,
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
        "source_evidence": _source_evidence(source_candidate),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_candidate_commit": EXPECTED_SOURCE_CANDIDATE_COMMIT,
        "source_repository_context": {
            "local_branch_count": 296,
            "remote_branch_count": 268,
            "total_ref_count": 564,
            "source_local_tag_count": 32,
            "source_candidate_namespace_tag_count": 4,
            "source_remote_approved_tag_count": 0,
        },
        "repository_tag_push_strategy_candidate_created": True,
        "repository_tag_push_strategy_candidate_ready_for_operator_review": True,
        "repository_tag_push_strategy_operator_review_created": True,
        "repository_tag_push_strategy_operator_review_ready": True,
        "tag_push_packages_reviewed": True,
        "tag_push_records_reviewed": True,
        "tag_push_prerequisites_reviewed": True,
        "tag_push_policy_reviewed": True,
        "ready_for_repository_tag_push_strategy_approval": False,
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
        "reviewed_tag_push_philosophy": REVIEWED_TAG_PUSH_PHILOSOPHY,
        "reviewed_tag_push_boundary": REVIEWED_TAG_PUSH_BOUNDARY,
        "reviewed_tag_push_goal": REVIEWED_TAG_PUSH_GOAL,
        "tag_push_philosophy_review_status": "REVIEWED_PLANNING_ONLY",
        "reviewed_push_packages": deepcopy(REVIEWED_PUSH_PACKAGES),
        "recommended_tag_push_package": source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "recommended_package_selected": False,
        "reviewed_push_records": deepcopy(REVIEWED_PUSH_RECORDS),
        "reviewed_push_command_template": source_service.CANDIDATE_PUSH_COMMAND_TEMPLATE,
        "command_review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "remote_publication_status": "NOT_PUSHED",
        "remote_publication_approval_required": True,
        "remote_publication_execution_requires_separate_task": True,
        "reviewed_tag_push_prerequisites": deepcopy(REVIEWED_TAG_PUSH_PREREQUISITES),
        "reviewed_tag_push_non_goals": deepcopy(REVIEWED_TAG_PUSH_NON_GOALS),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_TAG_PUSH",
        "recommendation_reason": (
            "The tag-push strategy candidate has been reviewed, but no package has been "
            "selected or approved by this review."
        ),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    packages = review.get("reviewed_push_packages", [])
    records = review.get("reviewed_push_records", [])
    return {
        "source_candidate_digest_bound": review.get("source_tag_push_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_results_review_digest_bound": review.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest_bound": review.get("source_tag_manifest_review_digest") == EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_execution_digest_bound": review.get("source_tagging_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tag_manifest_digest_bound": review.get("source_tagging_execution_tag_manifest_digest") == EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_approval_digest_bound": review.get("source_tagging_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": review.get("source_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
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
        "origin_main_commit_bound": review.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_candidate_ready_true": review.get("repository_tag_push_strategy_candidate_ready_for_operator_review") is True,
        "review_created_true": review.get("repository_tag_push_strategy_operator_review_created") is True,
        "review_ready_true": review.get("repository_tag_push_strategy_operator_review_ready") is True,
        "push_packages_reviewed_true": review.get("tag_push_packages_reviewed") is True,
        "push_records_reviewed_true": review.get("tag_push_records_reviewed") is True,
        "push_prerequisites_reviewed_true": review.get("tag_push_prerequisites_reviewed") is True,
        "push_policy_reviewed_true": review.get("tag_push_policy_reviewed") is True,
        "ready_for_approval_false": review.get("ready_for_repository_tag_push_strategy_approval") is False,
        "recommended_push_package_reviewed_not_selected": review.get("recommended_tag_push_package") == source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN and review.get("recommended_package_selected") is False,
        "push_packages_reviewed_4": packages == REVIEWED_PUSH_PACKAGES and len(packages) == 4,
        "candidate_push_records_reviewed_4": records == REVIEWED_PUSH_RECORDS and len(records) == 4,
        "candidate_remote_refs_reviewed_4": [row.get("candidate_remote_ref") for row in records] == source_service.CANDIDATE_REMOTE_REFS,
        "local_tag_object_shas_bound": [row.get("local_tag_object_sha") for row in records] == source_service.source_review_service.EXPECTED_TAG_OBJECT_SHAS,
        "target_commits_bound": [row.get("target_commit") for row in records] == [row["target_commit"] for row in source_service.source_review_service.EXPECTED_TAGS],
        "remote_refs_absent_in_source_review": all(row.get("remote_ref_exists_in_source_review") is False for row in records),
        "push_command_template_reviewed": review.get("reviewed_push_command_template") == source_service.CANDIDATE_PUSH_COMMAND_TEMPLATE,
        "push_command_not_executed": review.get("command_review_status") == "REVIEWED_PLANNED_NOT_EXECUTED" and review.get("remote_publication_status") == "NOT_PUSHED",
        "tag_push_strategy_selected_false": review.get("repository_tag_push_strategy_selected") is False,
        "tag_push_strategy_approved_false": review.get("repository_tag_push_strategy_approved") is False,
        "tag_push_strategy_authorized_false": review.get("repository_tag_push_strategy_authorized") is False,
        "tag_push_strategy_executed_false": review.get("repository_tag_push_strategy_executed") is False,
        "tags_pushed_false": review.get("repository_tags_pushed") is False and all(row.get("pushed") is False for row in records),
        "git_tag_push_performed_false": review.get("git_tag_push_performed") is False,
        "additional_tags_created_false": review.get("additional_tags_created") is False,
        "tags_modified_false": review.get("tags_modified") is False,
        "tags_deleted_false": review.get("tags_deleted") is False,
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
        "non_goals_reviewed": review.get("reviewed_tag_push_non_goals") == REVIEWED_TAG_PUSH_NON_GOALS,
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
        "actual": actual,
        "severity": BLOCKER,
        "message": (
            "tag-push operator review evidence matches"
            if actual
            else "tag-push operator review evidence mismatch"
        ),
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_tag_push_strategy_operator_review_created": True,
        "repository_tag_push_strategy_operator_review_ready": True,
        "tag_push_packages_reviewed": True,
        "tag_push_records_reviewed": True,
        "recommended_tag_push_package": source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "recommended_package_selected": False,
        "ready_for_repository_tag_push_strategy_approval": False,
        "tags_pushed": False,
        "git_tag_push_performed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tag_push_strategy_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tag_push_strategy_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tag_push_strategy_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the review from committed constants without rerunning source workflows."""
    review = _base_review(source_candidate)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_tag_push_strategy_operator_review_digest"] = (
        marketflow_repository_tag_push_strategy_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_tag_push_strategy_operator_review_v1(review)
    return review


def validate_marketflow_repository_tag_push_strategy_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact source bindings and all closed approval/execution gates."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "review must be an object"
        )
    expected = _base_review(None)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
                f"{field} mismatch"
            )
    checklist = review.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(review):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review checklist failed"
        )
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review summary mismatch"
        )
    digest = review.get("marketflow_repository_tag_push_strategy_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review digest missing"
        )
    if digest != marketflow_repository_tag_push_strategy_operator_review_digest_v1(review):
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tag_push_strategy_operator_review_digest": digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tag_push_strategy_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated operator review."""
    validation = validate_marketflow_repository_tag_push_strategy_operator_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Repository Tag Push Strategy Operator Review v1"]),
        (
            "MarketFlow Repository Tag Push Strategy Operator Review v1",
            [
                f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.",
                f"Digest: `{validation['marketflow_repository_tag_push_strategy_operator_review_digest']}`.",
            ],
        ),
        ("Source Tag Push Candidate", [f"Source digest: `{review['source_tag_push_candidate_digest']}`.", f"Source commit: `{review['source_candidate_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(review['source_evidence'])}."]),
        ("Repository Context", [f"Origin main: `{review['origin_main_commit']}`.", "Source refs: 296 local / 268 remote / 564 total; source tags: 32 / 4 candidate namespace / 0 approved remote."]),
        ("Review Scope", [review["review_scope"]]),
        ("Reviewed Tag Push Philosophy", [review["reviewed_tag_push_philosophy"], review["reviewed_tag_push_boundary"], review["reviewed_tag_push_goal"]]),
        ("Reviewed Push Packages", [f"{row['package_id']}: {row['review_status']}" for row in review["reviewed_push_packages"]]),
        ("Reviewed Push Records", [f"`{row['tag_name']}` -> `{row['candidate_remote_ref']}` ({row['candidate_push_status']})" for row in review["reviewed_push_records"]]),
        ("Reviewed Remote Publication Plan", [review["reviewed_push_command_template"], review["command_review_status"], review["remote_publication_status"]]),
        ("Reviewed Tag Push Prerequisites", [f"{row['prerequisite_id']}: {row['review_status']} / {row['execution_status']}" for row in review["reviewed_tag_push_prerequisites"]]),
        ("Reviewed Tag Push Non-Goals", [f"{row['non_goal_id']}: {row['review_status']}" for row in review["reviewed_tag_push_non_goals"]]),
        ("Recommendation", [review["recommended_action"], review["recommendation_reason"], review["recommended_next_task_status"]]),
        ("Next Chain", list(review["next_chain"])),
        ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["No package is selected or approved. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['summary']['passed_checks']} / {review['summary']['total_checks']} checks pass; {review['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag push, tag creation/modification/deletion, merge, rebase, deletion, main/force push, prune, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tag Push Strategy Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tag_push_strategy_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_tag_push_strategy_operator_review_v1(
        source_candidate=source_candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tag_push_strategy_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTagPushStrategyOperatorReviewError(
            "operator review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tag_push_strategy_operator_review_digest": review[
            "marketflow_repository_tag_push_strategy_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
