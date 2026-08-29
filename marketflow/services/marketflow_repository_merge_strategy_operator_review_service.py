"""Offline operator review of the repository merge-strategy candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_merge_strategy_candidate_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_merge_strategy_operator_review_v1"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_READY"
)
REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "392a3654f6d0723a03c794a69cecab401a37f2ce3c18469a4a5b5a6247e5932d"
)
EXPECTED_SOURCE_CANDIDATE_COMMIT = "be5701cd70e5cabdc590640370a89add9b32f8b5"
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST
EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_PUSH_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST
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
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)
SOURCE_REPOSITORY_CONTEXT = {
    "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "local_branch_count": 302,
    "remote_ref_count": 274,
    "total_ref_count": 576,
    "local_tag_count": 32,
    "remote_candidate_namespace_tag_count": 4,
    "remote_approved_tag_count": 4,
    "verified_remote_terminal_tag_count": 4,
    "extra_remote_candidate_namespace_tag_count": 0,
    "tracked_marketflow_file_count": 0,
}

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_MERGE_STRATEGY_PHILOSOPHY = source_service.MERGE_STRATEGY_PHILOSOPHY
REVIEWED_MERGE_STRATEGY_BOUNDARY = (
    "Candidate-only reviewed; no merge, rebase, squash, cherry-pick, branch deletion, "
    "cleanup, or main push is performed."
)
REVIEWED_MERGE_STRATEGY_GOAL = source_service.MERGE_STRATEGY_GOAL

REVIEWED_MERGE_STRATEGY_PACKAGES = [
    {
        **deepcopy(package),
        "source_status": package["status"],
        "review_status": (
            "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
            if package["package_id"]
            == source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
            else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        ),
    }
    for package in source_service.PROPOSED_MERGE_STRATEGY_PACKAGES
]
for _package in REVIEWED_MERGE_STRATEGY_PACKAGES:
    _package.pop("status")

REVIEWED_INTEGRATION_BRANCH_PLAN = {
    **deepcopy(source_service.CANDIDATE_INTEGRATION_BRANCH_PLAN),
    "candidate_integration_status": "REVIEWED_PLANNED_NOT_CREATED",
}
REVIEWED_MERGE_PREREQUISITES = [
    {
        "prerequisite_id": prerequisite_id,
        "required": required,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_MERGE_OR_INTEGRATION",
        "execution_status": "NOT_EXECUTED",
    }
    for prerequisite_id, required in source_service.MERGE_PREREQUISITES.items()
]
REVIEWED_MERGE_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source_service.MERGE_NON_GOALS
]
CHAIN_MERGE_IMPACT_REVIEW = [
    {
        "chain_id": chain_id,
        "review_status": "REVIEWED_PLANNING_ONLY",
        "merge_required_now": False,
        "operator_review_required": True,
        "main_push_required_now": False,
        "merge_readiness": "NOT_EVALUATED_BY_THIS_REVIEW",
        "delete_readiness": "NOT_AUTHORIZED_BY_THIS_REVIEW",
        "archive_readiness": "PLANNING_ONLY_OR_REQUIRES_OPERATOR_REVIEW",
    }
    for chain_id in source_service.CHAIN_IDS
]

NEXT_CHAIN = [
    "Repository Merge Strategy Approval v1, if selected.",
    "Repository Integration Branch Execution v1, if approved.",
    "Repository Integration Branch Results Review v1.",
    "Repository Main Merge Approval v1, only if integration branch review passes.",
    "Repository Main Merge Execution v1, only if separately approved.",
    "Repository Branch Cleanup Candidate v1, only after main integration strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
]
NEXT_GATES = [
    "repository_merge_strategy_approval_if_selected",
    "repository_integration_branch_execution_if_approved",
    "repository_integration_branch_results_review",
    "repository_main_merge_approval_if_integration_passes",
    "repository_main_merge_execution_if_approved",
    "repository_branch_cleanup_candidate_after_merge_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
]
RISK_CONTROLS = [
    "review_does_not_select_merge_strategy", "review_does_not_approve_merge_strategy",
    "review_does_not_create_integration_branch", "review_does_not_merge",
    "review_does_not_rebase", "review_does_not_squash_merge",
    "review_does_not_cherry_pick", "review_does_not_push_main",
    "review_does_not_force_push", "review_does_not_delete_branches",
    "review_does_not_delete_remote_branches", "review_does_not_prune_remotes",
    "review_does_not_modify_origin_main", "review_does_not_modify_tags",
    "review_does_not_push_additional_tags", "review_does_not_modify_marketflow_outputs",
    "review_does_not_call_providers", "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset", "review_does_not_rerun_merge_strategy_candidate",
    "review_does_not_rerun_tag_push_results_review", "review_does_not_rerun_tag_push_execution",
    "review_does_not_rerun_inventory", "review_does_not_rerun_evidence",
    "review_does_not_recompute_metrics", "review_does_not_train_models",
    "review_does_not_score_strategy", "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness", "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime", "review_does_not_authorize_broker_execution",
    "all_merge_actions_remain_candidate_only", "operator_approval_required_before_integration_branch",
    "operator_approval_required_before_main_merge", "main_push_requires_separate_approval",
    "protect_origin_main", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound", "source_results_review_digest_bound",
    "source_remote_manifest_review_digest_bound", "source_tag_push_execution_digest_bound",
    "source_remote_manifest_digest_bound", "source_tag_push_approval_digest_bound",
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound", "origin_main_commit_bound",
    "source_candidate_ready_true", "review_created_true", "review_ready_true",
    "merge_packages_reviewed_true", "merge_prerequisites_reviewed_true",
    "integration_branch_plan_reviewed_true", "chain_merge_impact_reviewed_true",
    "merge_policy_reviewed_true", "ready_for_approval_false",
    "recommended_package_reviewed_not_selected", "merge_packages_reviewed_6",
    "integration_branch_plan_reviewed_not_created", "merge_strategy_selected_false",
    "merge_strategy_approved_false", "merge_strategy_authorized_false",
    "merge_strategy_executed_false", "integration_branch_created_false",
    "merge_performed_false", "rebase_performed_false", "squash_merge_performed_false",
    "cherry_pick_performed_false", "main_push_false", "force_push_false",
    "branch_delete_false", "remote_delete_false", "remote_prune_false",
    "origin_main_modified_false", "tags_pushed_again_false", "additional_tags_created_false",
    "tags_modified_false", "tags_deleted_false", "cleanup_candidate_created_false",
    "marketflow_outputs_not_tracked", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "chain_merge_impact_review_present", "merge_non_goals_reviewed", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryMergeStrategyOperatorReviewError(ValueError):
    """Raised when the review violates evidence or authority boundaries."""


def _source_values(source_candidate: Mapping[str, Any] | None) -> tuple[dict[str, Any], dict[str, Any]]:
    if source_candidate is None:
        return deepcopy(SOURCE_EVIDENCE), deepcopy(SOURCE_REPOSITORY_CONTEXT)
    if not isinstance(source_candidate, dict):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("source_candidate must be an object")
    try:
        source_service.validate_marketflow_repository_merge_strategy_candidate_v1(source_candidate)
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError(
            "source merge-strategy candidate is invalid"
        ) from exc
    if source_candidate.get("marketflow_repository_merge_strategy_candidate_digest") != EXPECTED_SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError(
            "source merge-strategy candidate digest mismatch"
        )
    return deepcopy(source_candidate["source_evidence"]), deepcopy(SOURCE_REPOSITORY_CONTEXT)


def _base_review(source_candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    evidence, context = _source_values(source_candidate)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True, "planning_only": True, "governance_only": True,
        "operator_review_required": True,
        "source_merge_strategy_candidate_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1,
        "source_merge_strategy_candidate_status": source_service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_merge_strategy_candidate_scope": source_service.REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_merge_strategy_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tag_push_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_tag_manifest_review_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest": EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_remote_manifest_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest": EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_tag_push_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_TAG_PUSH_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST,
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
        "source_evidence": evidence,
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_candidate_commit": EXPECTED_SOURCE_CANDIDATE_COMMIT,
        "source_repository_context": context,
        "repository_merge_strategy_candidate_created": True,
        "repository_merge_strategy_candidate_ready_for_operator_review": True,
        "repository_merge_strategy_operator_review_created": True,
        "repository_merge_strategy_operator_review_ready": True,
        "merge_packages_reviewed": True, "merge_prerequisites_reviewed": True,
        "integration_branch_plan_reviewed": True, "chain_merge_impact_reviewed": True,
        "merge_policy_reviewed": True,
        "ready_for_repository_merge_strategy_approval": False,
        "repository_merge_strategy_selected": False, "repository_merge_strategy_approved": False,
        "repository_merge_strategy_authorized": False, "repository_merge_strategy_executed": False,
        "repository_integration_branch_created": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_squash_merge_performed": False, "git_cherry_pick_performed": False,
        "git_main_push_performed": False, "git_force_push_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_remote_prune_performed": False, "origin_main_modified_by_this_task": False,
        "repository_tags_pushed_again": False, "additional_tag_push_performed": False,
        "additional_tags_created": False, "tags_modified": False, "tags_deleted": False,
        "repository_cleanup_candidate_created": False,
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
        "reviewed_merge_strategy_philosophy": REVIEWED_MERGE_STRATEGY_PHILOSOPHY,
        "reviewed_merge_strategy_boundary": REVIEWED_MERGE_STRATEGY_BOUNDARY,
        "reviewed_merge_strategy_goal": REVIEWED_MERGE_STRATEGY_GOAL,
        "merge_strategy_philosophy_review_status": "REVIEWED_PLANNING_ONLY",
        "reviewed_merge_strategy_packages": deepcopy(REVIEWED_MERGE_STRATEGY_PACKAGES),
        "recommended_merge_strategy_package": source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "recommended_package_selected": False,
        "reviewed_integration_branch_plan": deepcopy(REVIEWED_INTEGRATION_BRANCH_PLAN),
        "reviewed_merge_prerequisites": deepcopy(REVIEWED_MERGE_PREREQUISITES),
        "reviewed_merge_non_goals": deepcopy(REVIEWED_MERGE_NON_GOALS),
        "chain_merge_impact_review": deepcopy(CHAIN_MERGE_IMPACT_REVIEW),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_INTEGRATION_BRANCH_OR_MERGE",
        "recommendation_reason": (
            "The merge strategy candidate has been reviewed, but no package has been "
            "selected or approved by this review."
        ),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    packages = review.get("reviewed_merge_strategy_packages", [])
    plan = review.get("reviewed_integration_branch_plan", {})
    return {
        "source_candidate_digest_bound": review.get("source_merge_strategy_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_results_review_digest_bound": review.get("source_tag_push_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest_bound": review.get("source_remote_tag_manifest_review_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest_bound": review.get("source_tag_push_execution_digest") == EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_remote_manifest_digest_bound": review.get("source_tag_push_remote_manifest_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest_bound": review.get("source_tag_push_approval_digest") == EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
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
        "source_candidate_ready_true": review.get("repository_merge_strategy_candidate_ready_for_operator_review") is True,
        "review_created_true": review.get("repository_merge_strategy_operator_review_created") is True,
        "review_ready_true": review.get("repository_merge_strategy_operator_review_ready") is True,
        "merge_packages_reviewed_true": review.get("merge_packages_reviewed") is True,
        "merge_prerequisites_reviewed_true": review.get("merge_prerequisites_reviewed") is True,
        "integration_branch_plan_reviewed_true": review.get("integration_branch_plan_reviewed") is True,
        "chain_merge_impact_reviewed_true": review.get("chain_merge_impact_reviewed") is True,
        "merge_policy_reviewed_true": review.get("merge_policy_reviewed") is True,
        "ready_for_approval_false": review.get("ready_for_repository_merge_strategy_approval") is False,
        "recommended_package_reviewed_not_selected": review.get("recommended_merge_strategy_package") == source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION and review.get("recommended_package_selected") is False,
        "merge_packages_reviewed_6": packages == REVIEWED_MERGE_STRATEGY_PACKAGES and len(packages) == 6,
        "integration_branch_plan_reviewed_not_created": plan == REVIEWED_INTEGRATION_BRANCH_PLAN and plan.get("integration_branch_created") is False,
        "merge_strategy_selected_false": review.get("repository_merge_strategy_selected") is False,
        "merge_strategy_approved_false": review.get("repository_merge_strategy_approved") is False,
        "merge_strategy_authorized_false": review.get("repository_merge_strategy_authorized") is False,
        "merge_strategy_executed_false": review.get("repository_merge_strategy_executed") is False,
        "integration_branch_created_false": review.get("repository_integration_branch_created") is False,
        "merge_performed_false": review.get("git_merge_performed") is False,
        "rebase_performed_false": review.get("git_rebase_performed") is False,
        "squash_merge_performed_false": review.get("git_squash_merge_performed") is False,
        "cherry_pick_performed_false": review.get("git_cherry_pick_performed") is False,
        "main_push_false": review.get("git_main_push_performed") is False,
        "force_push_false": review.get("git_force_push_performed") is False,
        "branch_delete_false": review.get("git_branch_delete_performed") is False,
        "remote_delete_false": review.get("git_remote_delete_performed") is False,
        "remote_prune_false": review.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": review.get("origin_main_modified_by_this_task") is False,
        "tags_pushed_again_false": review.get("repository_tags_pushed_again") is False and review.get("additional_tag_push_performed") is False,
        "additional_tags_created_false": review.get("additional_tags_created") is False,
        "tags_modified_false": review.get("tags_modified") is False,
        "tags_deleted_false": review.get("tags_deleted") is False,
        "cleanup_candidate_created_false": review.get("repository_cleanup_candidate_created") is False,
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
        "chain_merge_impact_review_present": review.get("chain_merge_impact_review") == CHAIN_MERGE_IMPACT_REVIEW,
        "merge_non_goals_reviewed": review.get("reviewed_merge_non_goals") == REVIEWED_MERGE_NON_GOALS,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL, "expected": True,
        "actual": actual, "severity": BLOCKER,
        "message": "merge-strategy operator review evidence matches" if actual else "merge-strategy operator review evidence mismatch",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_merge_strategy_operator_review_created": True,
        "repository_merge_strategy_operator_review_ready": True,
        "merge_packages_reviewed": True,
        "recommended_merge_strategy_package": source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "recommended_package_selected": False,
        "ready_for_repository_merge_strategy_approval": False,
        "integration_branch_created": False, "merge_performed": False, "main_pushed": False,
        "cleanup_candidate_created": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_merge_strategy_operator_review_digest_v1(review: Mapping[str, Any]) -> str:
    """Return the deterministic semantic digest for the operator review."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_merge_strategy_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_merge_strategy_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the review from committed constants without rerunning source workflows."""
    review = _base_review(source_candidate)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_merge_strategy_operator_review_digest"] = (
        marketflow_repository_merge_strategy_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_merge_strategy_operator_review_v1(review)
    return review


def validate_marketflow_repository_merge_strategy_operator_review_v1(review: dict) -> dict:
    """Validate exact source bindings and all closed approval/execution gates."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("review must be an object")
    expected = _base_review(None)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryMergeStrategyOperatorReviewError(f"{field} mismatch")
    checklist = review.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(review):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review checklist failed")
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review summary mismatch")
    digest = review.get("marketflow_repository_merge_strategy_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review digest missing")
    if digest != marketflow_repository_merge_strategy_operator_review_digest_v1(review):
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "marketflow_repository_merge_strategy_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_merge_strategy_operator_review_markdown_v1(review: dict) -> str:
    """Render a sanitized Markdown view of the validated operator review."""
    validation = validate_marketflow_repository_merge_strategy_operator_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Repository Merge Strategy Operator Review v1"]),
        ("MarketFlow Repository Merge Strategy Operator Review v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.", f"Digest: `{validation['marketflow_repository_merge_strategy_operator_review_digest']}`."]),
        ("Source Merge Strategy Candidate", [f"Source digest: `{review['source_merge_strategy_candidate_digest']}`.", f"Source commit: `{review['source_candidate_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(review['source_evidence'])}."]),
        ("Repository Context", [str(review["source_repository_context"])]),
        ("Review Scope", [review["review_scope"]]),
        ("Reviewed Merge Strategy Philosophy", [review["reviewed_merge_strategy_philosophy"], review["reviewed_merge_strategy_boundary"], review["reviewed_merge_strategy_goal"]]),
        ("Reviewed Merge Packages", [f"{row['package_id']}: {row['review_status']}" for row in review["reviewed_merge_strategy_packages"]]),
        ("Reviewed Integration Branch Plan", [str(review["reviewed_integration_branch_plan"])]),
        ("Reviewed Merge Prerequisites", [f"{row['prerequisite_id']}: {row['review_status']} / {row['execution_status']}" for row in review["reviewed_merge_prerequisites"]]),
        ("Reviewed Merge Non-Goals", [f"{row['non_goal_id']}: {row['review_status']}" for row in review["reviewed_merge_non_goals"]]),
        ("Chain Merge Impact Review", [f"{row['chain_id']}: {row['review_status']}" for row in review["chain_merge_impact_review"]]),
        ("Recommendation", [review["recommended_action"], review["recommendation_reason"], review["recommended_next_task_status"]]),
        ("Next Chain", list(review["next_chain"])), ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["No package is selected or approved. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['summary']['passed_checks']} / {review['summary']['total_checks']} checks pass; {review['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No integration branch, merge, rebase, squash, cherry-pick, deletion, main/force push, tag mutation, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Merge Strategy Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_merge_strategy_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_merge_strategy_operator_review_v1(source_candidate=source_candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_merge_strategy_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryMergeStrategyOperatorReviewError("operator review output already exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_merge_strategy_operator_review_digest": review["marketflow_repository_merge_strategy_operator_review_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
