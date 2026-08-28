"""Offline operator review of the frozen repository branch inventory plan."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_state_branch_inventory_integration_plan_service as inventory_plan,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_state_branch_inventory_operator_review_v1"
)
MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_READY"
)
REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN = (
    "REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = "e58cc279c1ec62fd2c24426ad71d35fc0edac41610769794bc71e5561add9896"
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = inventory_plan.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = inventory_plan.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = inventory_plan.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = inventory_plan.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = inventory_plan.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = inventory_plan.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = inventory_plan.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = inventory_plan.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = inventory_plan.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = inventory_plan.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = inventory_plan.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_SNAPSHOT_HEAD_COMMIT = inventory_plan.EXPECTED_INVENTORY_BASE_COMMIT
EXPECTED_SOURCE_PLANNING_BRANCH_COMMIT = "e49a4a3b14d2bb4fc721857cc1dfb42747e7b79e"
SOURCE_EVIDENCE = deepcopy(inventory_plan.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CATEGORY_REVIEWS = [
    {"category": inventory_plan.CATEGORY_MAIN_PROTECTED, "source_count": 2, "review_status": "REVIEWED_PROTECT_DO_NOT_TOUCH"},
    {"category": inventory_plan.CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN, "source_count": 2, "review_status": "REVIEWED_KEEP_TERMINAL_EVIDENCE"},
    {"category": inventory_plan.CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN, "source_count": 20, "review_status": "REVIEWED_KEEP_FOR_TRACEABILITY"},
    {"category": inventory_plan.CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN, "source_count": 10, "review_status": "REVIEWED_KEEP_FOR_TRACEABILITY"},
    {"category": inventory_plan.CATEGORY_FEATURE_LABEL_MATRIX_CHAIN, "source_count": 10, "review_status": "REVIEWED_KEEP_FOR_TRACEABILITY"},
    {"category": inventory_plan.CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN, "source_count": 102, "review_status": "REVIEWED_REQUIRES_FUTURE_OPERATOR_DECISION"},
    {"category": inventory_plan.CATEGORY_STRATEGY_CHARTER_CHAIN, "source_count": 6, "review_status": "REVIEWED_KEEP_FOR_TRACEABILITY"},
    {"category": inventory_plan.CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN, "source_count": 4, "review_status": "REVIEWED_KEEP_FOR_TRACEABILITY"},
    {"category": inventory_plan.CATEGORY_OTHER_FEATURE_BRANCH, "source_count": 389, "review_status": "REVIEWED_REQUIRES_OPERATOR_REVIEW_BEFORE_ANY_CLEANUP"},
    {"category": inventory_plan.CATEGORY_REMOTE_TRACKING_ONLY, "source_count": 6, "review_status": "REVIEWED_REQUIRES_OPERATOR_REVIEW_BEFORE_ANY_CLEANUP"},
    {"category": inventory_plan.CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW, "source_count": 0, "review_status": "REVIEWED_NONE_PRESENT_IN_SOURCE_SUMMARY"},
]

OTHER_CHAIN_REVIEWS = [
    {"chain_id": "CHAIN_VPA_WYCKOFF_RULE_BASELINE", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 5, "operator_action_required": True},
    {"chain_id": "CHAIN_FEATURE_LABEL_MATRIX", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 5, "operator_action_required": True},
    {"chain_id": "CHAIN_SIGNAL_FEATURE_GENERATION", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 5, "operator_action_required": True},
    {"chain_id": "CHAIN_OBJECTIVE_LABEL_TARGET_GENERATION", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 5, "operator_action_required": True},
    {"chain_id": "CHAIN_EXPECTANCY_OBJECTIVE_DESIGN", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 5, "operator_action_required": True},
    {"chain_id": "CHAIN_ALGORITHM_STRATEGY_CHARTER", "source_status": "COMPLETED_RESEARCH_ONLY", "source_local_branch_count": 3, "operator_action_required": True},
    {"chain_id": "CHAIN_PRIOR_IMPROVED_EVIDENCE_ARCHIVE", "source_status": "TERMINAL_ARCHIVED_NOT_READY", "source_local_branch_count": 2, "operator_action_required": True},
    {"chain_id": "CHAIN_IBKR_OR_BROKER", "source_status": "NOT_PRESENT", "source_local_branch_count": 0, "operator_action_required": False},
    {"chain_id": "CHAIN_MISCELLANEOUS_OTHER_FEATURES", "source_status": "PRESENT_REQUIRES_OPERATOR_REVIEW", "source_local_branch_count": 212, "operator_action_required": True},
]
for _chain_review in OTHER_CHAIN_REVIEWS:
    _chain_review.update(
        {
            "review_status": "REVIEWED_PLANNING_ONLY",
            "merge_readiness": "NOT_EVALUATED_BY_THIS_REVIEW",
            "delete_readiness": "NOT_AUTHORIZED_BY_THIS_REVIEW",
            "archive_readiness": "PLANNING_ONLY_OR_REQUIRES_OPERATOR_REVIEW",
        }
    )

INTEGRATION_PHASE_REVIEWS = [
    {"phase_number": 0, "phase_name": "Inventory and Freeze", "source_status": "COMPLETED_BY_SOURCE_ARTIFACT", "review_status": "REVIEWED_COMPLETE", "next_candidate_ready": False},
    {"phase_number": 1, "phase_name": "Operator Review of Inventory", "source_status": "FUTURE_NOT_STARTED", "review_status": "COMPLETED_BY_THIS_ARTIFACT", "next_candidate_ready": False},
    {"phase_number": 2, "phase_name": "Tagging / Release Strategy Candidate", "source_status": "FUTURE_NOT_STARTED", "review_status": "REVIEWED_FUTURE_NOT_STARTED", "next_candidate_ready": True},
    {"phase_number": 3, "phase_name": "Merge Strategy Candidate", "source_status": "FUTURE_NOT_STARTED", "review_status": "REVIEWED_FUTURE_NOT_STARTED", "next_candidate_ready": False},
    {"phase_number": 4, "phase_name": "Branch Archive / Cleanup Candidate", "source_status": "FUTURE_NOT_STARTED", "review_status": "REVIEWED_FUTURE_NOT_STARTED", "next_candidate_ready": False},
    {"phase_number": 5, "phase_name": "Execution of Approved Cleanup", "source_status": "FUTURE_NOT_STARTED", "review_status": "REVIEWED_FUTURE_NOT_STARTED", "next_candidate_ready": False},
]

NEXT_CHAIN = [
    "MarketFlow Repository Tagging / Release Strategy Candidate v1.",
    "Repository Tagging / Release Strategy Operator Review v1.",
    "Tagging approval only if separately selected.",
    "Merge Strategy Candidate only after tagging/release strategy review.",
    "Branch Cleanup Candidate only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval and backup/bundle confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tagging_release_strategy_candidate",
    "repository_tagging_release_strategy_operator_review",
    "repository_tagging_approval_if_selected",
    "repository_merge_strategy_candidate",
    "repository_branch_cleanup_candidate",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "review_does_not_merge", "review_does_not_rebase",
    "review_does_not_delete_branches", "review_does_not_delete_remote_branches",
    "review_does_not_create_tags", "review_does_not_push_main",
    "review_does_not_force_push", "review_does_not_prune_remotes",
    "review_does_not_modify_origin_main", "review_does_not_modify_marketflow_outputs",
    "review_does_not_call_providers", "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset", "review_does_not_rerun_evidence",
    "review_does_not_recompute_metrics", "review_does_not_train_models",
    "review_does_not_score_strategy", "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness", "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime", "review_does_not_authorize_broker_execution",
    "all_dispositions_are_recommendations_only", "operator_review_required_before_merge",
    "operator_review_required_before_delete", "operator_review_required_before_tagging",
    "protect_origin_main", "preserve_terminal_archive_evidence", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_results_review_digest_bound",
    "source_backtest_rows_digest_bound", "source_metric_report_digest_bound",
    "records_digest_bound", "origin_main_commit_bound", "source_snapshot_counts_bound",
    "post_push_delta_acknowledged", "repository_inventory_operator_review_created_true",
    "repository_inventory_operator_review_ready_true", "inventory_categories_reviewed_true",
    "integration_phases_reviewed_true", "recommended_policy_reviewed_true",
    "ready_for_tagging_release_strategy_candidate_true",
    "tagging_release_strategy_candidate_created_false", "merge_strategy_candidate_created_false",
    "cleanup_candidate_created_false", "cleanup_executed_false",
    "merge_approval_created_false", "delete_approval_created_false",
    "tag_approval_created_false", "main_protected", "origin_main_protected",
    "main_push_false", "merge_performed_false", "rebase_performed_false",
    "branch_delete_performed_false", "remote_delete_performed_false",
    "tag_created_false", "force_push_false", "remote_prune_false",
    "marketflow_outputs_not_tracked", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "category_review_present", "terminal_chain_reviewed", "integration_phase_review_present",
    "policy_review_status_accepted_for_planning",
    "recommended_next_task_tagging_release_strategy_candidate",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryStateBranchInventoryOperatorReviewError(ValueError):
    """Raised when the operator review violates its evidence or authority contract."""


def _source_evidence(source_plan: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_plan is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_plan, dict):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "source_plan must be an object"
        )
    try:
        inventory_plan.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(
            source_plan
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "source inventory plan is invalid"
        ) from exc
    if source_plan.get(
        "marketflow_repository_state_branch_inventory_integration_plan_digest"
    ) != EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST:
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "source inventory plan digest mismatch"
        )
    return deepcopy(source_plan["source_evidence"])


def _base_review(source_plan: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN,
        "created_offline": True, "research_only": True, "planning_only": True,
        "operator_review_required": True,
        "source_inventory_plan_artifact_kind": inventory_plan.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1,
        "source_inventory_plan_status": inventory_plan.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY,
        "source_inventory_plan_scope": inventory_plan.REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN,
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
        "source_evidence": _source_evidence(source_plan),
        "source_snapshot_head_commit": EXPECTED_SOURCE_SNAPSHOT_HEAD_COMMIT,
        "source_planning_branch_commit": EXPECTED_SOURCE_PLANNING_BRANCH_COMMIT,
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "main_commit_if_available": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_snapshot_local_branch_count": 290,
        "source_snapshot_remote_branch_count": 261,
        "source_snapshot_total_branch_ref_count": 551,
        "post_push_live_local_branch_count": 290,
        "post_push_live_remote_branch_count": 262,
        "post_push_live_total_branch_ref_count": 552,
        "inventory_count_review_finding": "INVENTORY_REVIEWED_WITH_EXPECTED_POST_PUSH_REMOTE_REF_DELTA",
        "inventory_count_delta_reason": "CURRENT_INVENTORY_BRANCH_PUSH_ADDS_ONE_REMOTE_TRACKING_REF_AFTER_SOURCE_SNAPSHOT",
        "inventory_review_status": "REVIEWED_PLANNING_ONLY",
        "repository_inventory_operator_review_created": True,
        "repository_inventory_operator_review_ready": True,
        "inventory_review_completed": True, "inventory_categories_reviewed": True,
        "integration_phases_reviewed": True, "recommended_policy_reviewed": True,
        "ready_for_repository_tagging_release_strategy_candidate": True,
        "repository_tagging_release_strategy_candidate_created": False,
        "repository_merge_strategy_candidate_created": False,
        "repository_cleanup_candidate_created": False,
        "repository_cleanup_approved": False, "repository_cleanup_executed": False,
        "merge_approval_created": False, "delete_approval_created": False,
        "tag_approval_created": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_tag_created": False, "git_main_push_performed": False,
        "git_force_push_performed": False, "git_remote_prune_performed": False,
        "origin_main_modified_by_this_task": False,
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
        "category_reviews": deepcopy(CATEGORY_REVIEWS),
        "terminal_chain_review": {
            "chain_id": "CHAIN_EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH",
            "chain_status": "TERMINAL_ARCHIVED_NOT_READY",
            "terminal_branch": inventory_plan.TERMINAL_BRANCH,
            "terminal_commit": EXPECTED_SOURCE_SNAPSHOT_HEAD_COMMIT,
            "review_status": "REVIEWED_TERMINAL_NO_IMMEDIATE_ACTION",
            "recommended_next_action": "NONE_FOR_CURRENT_ARCHIVED_PATH",
            "merge_readiness": "NOT_EVALUATED_BY_THIS_REVIEW",
            "delete_readiness": "NOT_AUTHORIZED_BY_THIS_REVIEW",
            "archive_readiness": "PLANNING_ONLY",
            "operator_action_required": False,
        },
        "other_chain_reviews": deepcopy(OTHER_CHAIN_REVIEWS),
        "integration_phase_reviews": deepcopy(INTEGRATION_PHASE_REVIEWS),
        "reviewed_policy": "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG",
        "policy_review_status": "REVIEWED_ACCEPTED_FOR_PLANNING",
        "main_protection_reviewed": True, "delete_protection_reviewed": True,
        "force_push_protection_reviewed": True,
        "terminal_evidence_preservation_reviewed": True,
        "operator_review_required_before_merge": True,
        "operator_review_required_before_delete": True,
        "operator_review_required_before_tagging": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1",
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "CREATE_TAGGING_RELEASE_STRATEGY_CANDIDATE_PLANNING_ONLY",
        "merge_or_delete_now_recommended": False, "main_push_now_recommended": False,
        "tag_now_recommended": False, "cleanup_now_recommended": False,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    terminal = review.get("terminal_chain_review", {})
    return {
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
        "source_snapshot_counts_bound": (review.get("source_snapshot_local_branch_count"), review.get("source_snapshot_remote_branch_count"), review.get("source_snapshot_total_branch_ref_count")) == (290, 261, 551),
        "post_push_delta_acknowledged": (review.get("post_push_live_local_branch_count"), review.get("post_push_live_remote_branch_count"), review.get("post_push_live_total_branch_ref_count")) == (290, 262, 552) and review.get("inventory_count_review_finding") == "INVENTORY_REVIEWED_WITH_EXPECTED_POST_PUSH_REMOTE_REF_DELTA",
        "repository_inventory_operator_review_created_true": review.get("repository_inventory_operator_review_created") is True,
        "repository_inventory_operator_review_ready_true": review.get("repository_inventory_operator_review_ready") is True,
        "inventory_categories_reviewed_true": review.get("inventory_categories_reviewed") is True,
        "integration_phases_reviewed_true": review.get("integration_phases_reviewed") is True,
        "recommended_policy_reviewed_true": review.get("recommended_policy_reviewed") is True,
        "ready_for_tagging_release_strategy_candidate_true": review.get("ready_for_repository_tagging_release_strategy_candidate") is True,
        "tagging_release_strategy_candidate_created_false": review.get("repository_tagging_release_strategy_candidate_created") is False,
        "merge_strategy_candidate_created_false": review.get("repository_merge_strategy_candidate_created") is False,
        "cleanup_candidate_created_false": review.get("repository_cleanup_candidate_created") is False,
        "cleanup_executed_false": review.get("repository_cleanup_executed") is False,
        "merge_approval_created_false": review.get("merge_approval_created") is False,
        "delete_approval_created_false": review.get("delete_approval_created") is False,
        "tag_approval_created_false": review.get("tag_approval_created") is False,
        "main_protected": review.get("main_protection_reviewed") is True,
        "origin_main_protected": review.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT and review.get("origin_main_modified_by_this_task") is False,
        "main_push_false": review.get("git_main_push_performed") is False,
        "merge_performed_false": review.get("git_merge_performed") is False,
        "rebase_performed_false": review.get("git_rebase_performed") is False,
        "branch_delete_performed_false": review.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": review.get("git_remote_delete_performed") is False,
        "tag_created_false": review.get("git_tag_created") is False,
        "force_push_false": review.get("git_force_push_performed") is False,
        "remote_prune_false": review.get("git_remote_prune_performed") is False,
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
        "category_review_present": review.get("category_reviews") == CATEGORY_REVIEWS,
        "terminal_chain_reviewed": terminal.get("review_status") == "REVIEWED_TERMINAL_NO_IMMEDIATE_ACTION" and terminal.get("recommended_next_action") == "NONE_FOR_CURRENT_ARCHIVED_PATH",
        "integration_phase_review_present": review.get("integration_phase_reviews") == INTEGRATION_PHASE_REVIEWS,
        "policy_review_status_accepted_for_planning": review.get("policy_review_status") == "REVIEWED_ACCEPTED_FOR_PLANNING",
        "recommended_next_task_tagging_release_strategy_candidate": review.get("recommended_next_task") == "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1",
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "operator review evidence matches" if actual else "operator review evidence mismatch",
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
        "repository_inventory_operator_review_created": True,
        "repository_inventory_operator_review_ready": True,
        "inventory_review_completed": True,
        "ready_for_repository_tagging_release_strategy_candidate": True,
        "repository_tagging_release_strategy_candidate_created": False,
        "merge_performed": False, "delete_performed": False, "tag_created": False,
        "main_pushed": False, "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_state_branch_inventory_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_state_branch_inventory_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_state_branch_inventory_operator_review_v1(
    *, source_plan: dict | None = None,
) -> dict:
    """Build the operator review without rerunning the source branch inventory."""
    review = _base_review(source_plan)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_state_branch_inventory_operator_review_digest"] = (
        marketflow_repository_state_branch_inventory_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_state_branch_inventory_operator_review_v1(review)
    return review


def validate_marketflow_repository_state_branch_inventory_operator_review_v1(
    review: dict,
) -> dict:
    """Validate evidence bindings, completed review, and closed execution gates."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "review must be an object"
        )
    expected = _base_review(None)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
                f"{field} mismatch"
            )
    checklist = review.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(review):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review checklist failed"
        )
    if review.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review summary mismatch"
        )
    digest = review.get("marketflow_repository_state_branch_inventory_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review digest missing"
        )
    if digest != marketflow_repository_state_branch_inventory_operator_review_digest_v1(review):
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "marketflow_repository_state_branch_inventory_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_state_branch_inventory_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated operator review."""
    validation = validate_marketflow_repository_state_branch_inventory_operator_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Repository State Branch Inventory Operator Review v1"]),
        ("MarketFlow Repository State Branch Inventory Operator Review v1", [f"Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`.", f"Digest: `{validation['marketflow_repository_state_branch_inventory_operator_review_digest']}`."]),
        ("Source Inventory Plan", [f"`{review['source_inventory_plan_artifact_kind']}` with digest `{review['source_inventory_plan_digest']}`."]),
        ("Repository State Review", [f"Source snapshot/planning commit: `{review['source_snapshot_head_commit']}` / `{review['source_planning_branch_commit']}`.", f"`origin/main`: `{review['origin_main_commit']}`."]),
        ("Inventory Count Review", [f"Source local/remote/total: `{review['source_snapshot_local_branch_count']} / {review['source_snapshot_remote_branch_count']} / {review['source_snapshot_total_branch_ref_count']}`.", f"Post-push local/remote/total: `{review['post_push_live_local_branch_count']} / {review['post_push_live_remote_branch_count']} / {review['post_push_live_total_branch_ref_count']}`; `{review['inventory_count_review_finding']}`."]),
        ("Category Review", [f"`{row['category']}`: `{row['source_count']}`; `{row['review_status']}`." for row in review["category_reviews"]]),
        ("Terminal Expectancy Lab Chain Review", [f"`{key}`: `{value}`." for key, value in review["terminal_chain_review"].items()]),
        ("Other Chain Reviews", [f"`{row['chain_id']}`: `{row['review_status']}`; operator action `{row['operator_action_required']}`." for row in review["other_chain_reviews"]]),
        ("Integration Phase Review", [f"Phase {row['phase_number']} `{row['phase_name']}`: `{row['review_status']}`." for row in review["integration_phase_reviews"]]),
        ("Policy Review", [f"`{review['reviewed_policy']}` is `{review['policy_review_status']}`."]),
        ("Recommended Next Task", [f"`{review['recommended_next_task']}` remains `{review['recommended_next_task_status']}`."]),
        ("Protected Branches", ["Local main, origin/main, and the terminal expectancy-lab evidence branch remain protected."]),
        ("Branches Requiring Operator Review", ["Signal/feature/target, other-feature, remote-only, and any future unknown branch require a separate operator decision before cleanup."]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["No merge, delete, tag, cleanup, main, predictive, profitability, runtime, broker, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{review['summary']['total_checks']} / {review['summary']['passed_checks']} / {review['summary']['failed_checks']} / {review['summary']['blocker_count']}`."]),
        ("Guardrails", ["No source inventory rerun, Git integration action, provider, data, metric, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository State Branch Inventory Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_state_branch_inventory_operator_review_v1(
    output_dir: str | Path, *, source_plan: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing review."""
    review = build_marketflow_repository_state_branch_inventory_operator_review_v1(
        source_plan=source_plan
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_state_branch_inventory_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryStateBranchInventoryOperatorReviewError(
            "operator review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_repository_state_branch_inventory_operator_review_digest": review["marketflow_repository_state_branch_inventory_operator_review_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
