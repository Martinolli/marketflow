"""Offline operator review of the repository tagging/release strategy candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_tagging_release_strategy_candidate_service as source_candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_tagging_release_strategy_operator_review_v1"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_READY"
)
REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "277d05a4ab66450d2af883b7afb0f540b1af6068b3b912cc105bee585739a992"
)
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    source_candidate_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = (
    source_candidate_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
)
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_candidate_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_candidate_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = (
    source_candidate_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
)
EXPECTED_SOURCE_CLOSURE_DIGEST = source_candidate_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = (
    source_candidate_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
)
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_candidate_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_candidate_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_candidate_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_candidate_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_candidate_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT = (
    source_candidate_service.EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT
)
EXPECTED_SOURCE_CANDIDATE_COMMIT = "2fa1f512be659546d88a9c9604cac8c41f255941"
SOURCE_EVIDENCE = deepcopy(source_candidate_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_CATEGORY_SUMMARY = [
    {"category": "CATEGORY_MAIN_PROTECTED", "count": 2},
    {"category": "CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN", "count": 2},
    {"category": "CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN", "count": 20},
    {"category": "CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN", "count": 10},
    {"category": "CATEGORY_FEATURE_LABEL_MATRIX_CHAIN", "count": 10},
    {"category": "CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN", "count": 102},
    {"category": "CATEGORY_STRATEGY_CHARTER_CHAIN", "count": 6},
    {"category": "CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN", "count": 4},
    {"category": "CATEGORY_OTHER_FEATURE_BRANCH", "count": 389},
    {"category": "CATEGORY_REMOTE_TRACKING_ONLY", "count": 6},
    {"category": "CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW", "count": 0},
]

SOURCE_TERMINAL_CHAIN = {
    "chain_id": "CHAIN_EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH",
    "chain_status": "TERMINAL_ARCHIVED_NOT_READY",
    "terminal_branch": "feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1",
    "terminal_commit": "0be55dc8a65a586368c192d6bc13302b9830a0b4",
    "recommended_next_action": "NONE_FOR_CURRENT_ARCHIVED_PATH",
}


def _reviewed_packages() -> list[dict[str, Any]]:
    rows = []
    for package in source_candidate_service.TAGGING_PACKAGES:
        recommended = (
            package["package_id"]
            == source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS
        )
        rows.append(
            {
                "package_id": package["package_id"],
                "source_status": package["status"],
                "purpose": package["purpose"],
                "candidate_tags": list(package["candidate_tags"]),
                "review_status": (
                    "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
                    if recommended
                    else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
                ),
                "selected": False,
                "approved": False,
                "executed": False,
                "tags_created": False,
            }
        )
    return rows


REVIEWED_TAGGING_PACKAGES = _reviewed_packages()


def _reviewed_tag_definitions() -> list[dict[str, Any]]:
    return [
        {
            "tag_name": row["tag_name"],
            "tag_target_branch": row["tag_target_branch"],
            "tag_target_commit": row["tag_target_commit"],
            "tag_type": row["tag_type"],
            "source_tag_status": row["tag_status"],
            "review_status": "REVIEWED_CANDIDATE_TAG_NOT_CREATED",
            "tag_created": False,
            "tag_pushed": False,
            "operator_approval_required": True,
            "main_push_required": False,
            "runtime_authority_created": False,
            "predictive_usefulness_accepted": False,
            "profitability_accepted": False,
        }
        for row in source_candidate_service.CANDIDATE_TAG_DEFINITIONS
    ]


REVIEWED_CANDIDATE_TAG_DEFINITIONS = _reviewed_tag_definitions()

REVIEWED_PREREQUISITES = [
    {
        "prerequisite_id": prerequisite_id,
        "required": required,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_TAGGING",
        "execution_status": "NOT_EXECUTED",
    }
    for prerequisite_id, required in source_candidate_service.TAGGING_PREREQUISITES.items()
]

REVIEWED_TAG_MESSAGE_TEMPLATE = {
    "template": source_candidate_service.FUTURE_TAG_MESSAGE_TEMPLATE,
    "template_review_status": "REVIEWED_PLANNING_ONLY",
    "tag_message_template_present": True,
    "tag_message_includes_not_accepted_usefulness": True,
    "tag_message_includes_not_accepted_profitability": True,
    "tag_message_includes_runtime_not_authorized": True,
    "tag_message_includes_trading_not_authorized": True,
    "tag_message_includes_no_trade_recommendation": True,
}

REVIEWED_TAGGING_NON_GOALS = [
    {"non_goal": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source_candidate_service.TAGGING_NON_GOALS
]

PER_CHAIN_TAGGING_REVIEW_SUMMARY = [
    {
        "chain_id": row["chain_id"],
        "chain_name": row["chain_name"],
        "source_tagging_recommendation": row["tagging_recommendation"],
        "review_status": "REVIEWED_PLANNING_ONLY",
        "candidate_tags": list(row["candidate_tags"]),
        "tags_created": False,
        "approval_required": True,
        "operator_review_required": True,
        "merge_required": False,
        "main_push_required": False,
    }
    for row in source_candidate_service.PER_CHAIN_TAGGING_CANDIDATE_SUMMARY
]

NEXT_CHAIN = [
    "Repository Tagging / Release Strategy Approval v1, if selected.",
    "Repository Tagging Execution v1, if approved.",
    "Repository Merge Strategy Candidate v1, only after tagging strategy review or explicit skip decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tagging_release_strategy_approval_if_selected",
    "repository_tagging_execution_if_approved",
    "repository_merge_strategy_candidate_after_tag_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "review_does_not_select_tagging_package",
    "review_does_not_approve_tagging",
    "review_does_not_create_tags",
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
    "review_does_not_rerun_candidate",
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
    "all_tags_remain_candidate_only",
    "operator_approval_required_before_tagging",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound",
    "source_operator_review_digest_bound",
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
    "source_repository_counts_bound",
    "candidate_status_ready_bound",
    "review_created_true",
    "review_ready_true",
    "tagging_packages_reviewed_true",
    "tagging_candidates_reviewed_true",
    "tagging_prerequisites_reviewed_true",
    "tagging_policy_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "tagging_packages_reviewed_4",
    "candidate_tags_reviewed_14",
    "terminal_tags_reviewed_4",
    "governance_tags_reviewed_7",
    "protection_tags_reviewed_3",
    "tagging_strategy_selected_false",
    "tagging_strategy_approved_false",
    "tagging_strategy_authorized_false",
    "tagging_strategy_executed_false",
    "tags_created_false",
    "tags_pushed_false",
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
    "per_chain_review_present",
    "prerequisites_reviewed",
    "non_goals_reviewed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(ValueError):
    """Raised when the operator review violates evidence or authority boundaries."""


def _source_evidence(source_candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_candidate is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_candidate, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "source_candidate must be an object"
        )
    try:
        source_candidate_service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(
            source_candidate
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "source tagging candidate is invalid"
        ) from exc
    if source_candidate.get(
        "marketflow_repository_tagging_release_strategy_candidate_digest"
    ) != EXPECTED_SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "source tagging candidate digest mismatch"
        )
    return deepcopy(source_candidate["source_evidence"])


def _base_review(source_candidate: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True,
        "research_only": True,
        "planning_only": True,
        "operator_review_required": True,
        "source_tagging_candidate_artifact_kind": source_candidate_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1,
        "source_tagging_candidate_status": source_candidate_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_tagging_candidate_scope": source_candidate_service.REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_candidate),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_operator_review_commit": EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_candidate_commit": EXPECTED_SOURCE_CANDIDATE_COMMIT,
        "source_snapshot_local_branch_count": 290,
        "source_snapshot_remote_branch_count": 261,
        "source_snapshot_total_branch_ref_count": 551,
        "source_post_plan_push_live_local_branch_count": 290,
        "source_post_plan_push_live_remote_branch_count": 262,
        "source_post_plan_push_live_total_branch_ref_count": 552,
        "source_operator_review_live_local_branch_count": 291,
        "source_operator_review_live_remote_branch_count": 263,
        "source_operator_review_live_total_branch_ref_count": 554,
        "source_candidate_live_local_branch_count": 292,
        "source_candidate_live_remote_branch_count": 264,
        "source_candidate_live_total_branch_ref_count": 556,
        "source_existing_tag_count": 28,
        "source_candidate_namespace_tag_count": 0,
        "source_category_summary": deepcopy(SOURCE_CATEGORY_SUMMARY),
        "source_terminal_chain": deepcopy(SOURCE_TERMINAL_CHAIN),
        "repository_tagging_release_strategy_candidate_created": True,
        "repository_tagging_release_strategy_candidate_ready_for_operator_review": True,
        "repository_tagging_release_strategy_operator_review_created": True,
        "repository_tagging_release_strategy_operator_review_ready": True,
        "tagging_packages_reviewed": True,
        "tagging_candidates_reviewed": True,
        "tagging_prerequisites_reviewed": True,
        "tagging_policy_reviewed": True,
        "ready_for_repository_tagging_release_strategy_approval": False,
        "repository_tagging_release_strategy_selected": False,
        "repository_tagging_release_strategy_approved": False,
        "repository_tagging_release_strategy_authorized": False,
        "repository_tagging_release_strategy_executed": False,
        "git_tag_created": False,
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
        "reviewed_tagging_philosophy": source_candidate_service.TAGGING_PHILOSOPHY,
        "reviewed_tagging_boundary": (
            "Candidate-only reviewed; no tag is created, no tag is pushed, no branch is "
            "merged or deleted, and main remains untouched."
        ),
        "reviewed_tagging_goal": source_candidate_service.TAGGING_GOAL,
        "tagging_philosophy_review_status": "REVIEWED_PLANNING_ONLY",
        "recommended_tagging_package": source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "recommended_package_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "reviewed_tagging_packages": deepcopy(REVIEWED_TAGGING_PACKAGES),
        "reviewed_candidate_tag_count": 14,
        "terminal_candidate_tag_count": 4,
        "governance_candidate_tag_count": 7,
        "protection_candidate_tag_count": 3,
        "reviewed_candidate_tag_definitions": deepcopy(REVIEWED_CANDIDATE_TAG_DEFINITIONS),
        "reviewed_prerequisites": deepcopy(REVIEWED_PREREQUISITES),
        "reviewed_tag_message_template": deepcopy(REVIEWED_TAG_MESSAGE_TEMPLATE),
        "reviewed_tagging_non_goals": deepcopy(REVIEWED_TAGGING_NON_GOALS),
        "per_chain_tagging_review_summary": deepcopy(PER_CHAIN_TAGGING_REVIEW_SUMMARY),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_TAGGING",
        "recommendation_reason": (
            "The candidate has been reviewed, but no package has been selected or approved "
            "by this review."
        ),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    packages = review.get("reviewed_tagging_packages", [])
    tags = review.get("reviewed_candidate_tag_definitions", [])
    terminal_names = set(source_candidate_service.TERMINAL_TAG_NAMES)
    governance_names = set(source_candidate_service.GOVERNANCE_TAG_NAMES)
    protection_names = set(source_candidate_service.SOURCE_PROTECTION_TAG_NAMES)
    names = {row.get("tag_name") for row in tags if isinstance(row, dict)}
    return {
        "source_candidate_digest_bound": review.get("source_tagging_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_operator_review_digest_bound": review.get("source_inventory_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_inventory_plan_digest_bound": review.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": review.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": review.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": review.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": review.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": review.get("source_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": review.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": review.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": review.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": review.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": review.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": review.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_repository_counts_bound": (
            review.get("source_snapshot_local_branch_count"),
            review.get("source_snapshot_remote_branch_count"),
            review.get("source_snapshot_total_branch_ref_count"),
            review.get("source_post_plan_push_live_local_branch_count"),
            review.get("source_post_plan_push_live_remote_branch_count"),
            review.get("source_post_plan_push_live_total_branch_ref_count"),
            review.get("source_operator_review_live_local_branch_count"),
            review.get("source_operator_review_live_remote_branch_count"),
            review.get("source_operator_review_live_total_branch_ref_count"),
            review.get("source_candidate_live_local_branch_count"),
            review.get("source_candidate_live_remote_branch_count"),
            review.get("source_candidate_live_total_branch_ref_count"),
        ) == (290, 261, 551, 290, 262, 552, 291, 263, 554, 292, 264, 556),
        "candidate_status_ready_bound": review.get("source_tagging_candidate_status") == source_candidate_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "review_created_true": review.get("repository_tagging_release_strategy_operator_review_created") is True,
        "review_ready_true": review.get("repository_tagging_release_strategy_operator_review_ready") is True,
        "tagging_packages_reviewed_true": review.get("tagging_packages_reviewed") is True,
        "tagging_candidates_reviewed_true": review.get("tagging_candidates_reviewed") is True,
        "tagging_prerequisites_reviewed_true": review.get("tagging_prerequisites_reviewed") is True,
        "tagging_policy_reviewed_true": review.get("tagging_policy_reviewed") is True,
        "ready_for_approval_false": review.get("ready_for_repository_tagging_release_strategy_approval") is False,
        "recommended_package_reviewed_not_selected": review.get("recommended_tagging_package") == source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS and review.get("recommended_package_review_status") == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "tagging_packages_reviewed_4": packages == REVIEWED_TAGGING_PACKAGES and len(packages) == 4,
        "candidate_tags_reviewed_14": tags == REVIEWED_CANDIDATE_TAG_DEFINITIONS and len(tags) == 14,
        "terminal_tags_reviewed_4": terminal_names <= names and review.get("terminal_candidate_tag_count") == 4,
        "governance_tags_reviewed_7": governance_names <= names and review.get("governance_candidate_tag_count") == 7,
        "protection_tags_reviewed_3": protection_names <= names and review.get("protection_candidate_tag_count") == 3,
        "tagging_strategy_selected_false": review.get("repository_tagging_release_strategy_selected") is False,
        "tagging_strategy_approved_false": review.get("repository_tagging_release_strategy_approved") is False,
        "tagging_strategy_authorized_false": review.get("repository_tagging_release_strategy_authorized") is False,
        "tagging_strategy_executed_false": review.get("repository_tagging_release_strategy_executed") is False,
        "tags_created_false": review.get("git_tag_created") is False and all(row.get("tag_created") is False for row in tags) and all(row.get("tags_created") is False for row in packages),
        "tags_pushed_false": review.get("git_tag_push_performed") is False and all(row.get("tag_pushed") is False for row in tags),
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
        "per_chain_review_present": review.get("per_chain_tagging_review_summary") == PER_CHAIN_TAGGING_REVIEW_SUMMARY,
        "prerequisites_reviewed": review.get("reviewed_prerequisites") == REVIEWED_PREREQUISITES,
        "non_goals_reviewed": review.get("reviewed_tagging_non_goals") == REVIEWED_TAGGING_NON_GOALS,
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
            "tagging strategy review evidence matches"
            if actual
            else "tagging strategy review evidence mismatch"
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
        "repository_tagging_release_strategy_operator_review_created": True,
        "repository_tagging_release_strategy_operator_review_ready": True,
        "tagging_packages_reviewed": True,
        "tagging_candidates_reviewed": True,
        "recommended_tagging_package": source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "recommended_package_selected": False,
        "ready_for_repository_tagging_release_strategy_approval": False,
        "tags_created": False,
        "tags_pushed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1_IF_SELECTED",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tagging_release_strategy_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tagging_release_strategy_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tagging_release_strategy_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the review without rerunning the source tagging candidate."""
    review = _base_review(source_candidate)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_tagging_release_strategy_operator_review_digest"] = (
        marketflow_repository_tagging_release_strategy_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_tagging_release_strategy_operator_review_v1(review)
    return review


def validate_marketflow_repository_tagging_release_strategy_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings, complete review, and closed approval/execution gates."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "review must be an object"
        )
    expected = _base_review(None)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
                f"{field} mismatch"
            )
    checklist = review.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(review):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy review checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy review checklist failed"
        )
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy review summary mismatch"
        )
    digest = review.get(
        "marketflow_repository_tagging_release_strategy_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy review digest missing"
        )
    if digest != marketflow_repository_tagging_release_strategy_operator_review_digest_v1(
        review
    ):
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy review digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tagging_release_strategy_operator_review_digest": digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tagging_release_strategy_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated operator review."""
    validation = validate_marketflow_repository_tagging_release_strategy_operator_review_v1(
        review
    )
    sections = [
        ("Title", ["MarketFlow Repository Tagging / Release Strategy Operator Review v1"]),
        ("MarketFlow Repository Tagging / Release Strategy Operator Review v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.", f"Digest: `{validation['marketflow_repository_tagging_release_strategy_operator_review_digest']}`."]),
        ("Source Tagging Candidate", [f"Source digest: `{review['source_tagging_candidate_digest']}`.", f"Source commit: `{review['source_candidate_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(review['source_evidence'])}."]),
        ("Repository Context", [f"Origin main: `{review['origin_main_commit']}`.", "Frozen through candidate ref totals: 551 / 552 / 554 / 556.", "Existing/candidate-namespace tag counts: 28 / 0."]),
        ("Review Scope", [review["review_scope"]]),
        ("Reviewed Tagging Philosophy", [review["reviewed_tagging_philosophy"], review["reviewed_tagging_boundary"], review["reviewed_tagging_goal"]]),
        ("Reviewed Tagging Packages", [f"{row['package_id']}: {row['review_status']}" for row in review["reviewed_tagging_packages"]]),
        ("Reviewed Candidate Tags", [f"`{row['tag_name']}` -> `{row['tag_target_commit']}` ({row['review_status']})" for row in review["reviewed_candidate_tag_definitions"]]),
        ("Reviewed Prerequisites", [f"{row['prerequisite_id']}: {row['review_status']} / {row['execution_status']}" for row in review["reviewed_prerequisites"]]),
        ("Reviewed Tag Message Template", [review["reviewed_tag_message_template"]["template"]]),
        ("Reviewed Non-Goals", [f"{row['non_goal']}: {row['review_status']}" for row in review["reviewed_tagging_non_goals"]]),
        ("Per-Chain Review Summary", [f"{row['chain_id']}: {row['review_status']}" for row in review["per_chain_tagging_review_summary"]]),
        ("Recommendation", [f"`{review['recommended_next_task']}` remains `{review['recommended_next_task_status']}`.", review["recommendation_reason"]]),
        ("Next Chain", list(review["next_chain"])),
        ("Next Gates", list(review["next_gates"])),
        ("Risk Controls", list(review["risk_controls"])),
        ("Authority Boundaries", ["No package is selected or approved. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['summary']['passed_checks']} / {review['summary']['total_checks']} checks pass; {review['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag, tag push, merge, rebase, deletion, main push, force-push, prune, provider, data, metric, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tagging / Release Strategy Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tagging_release_strategy_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing review."""
    review = build_marketflow_repository_tagging_release_strategy_operator_review_v1(
        source_candidate=source_candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tagging_release_strategy_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError(
            "tagging strategy operator review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_tagging_release_strategy_operator_review_digest": review[
            "marketflow_repository_tagging_release_strategy_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
