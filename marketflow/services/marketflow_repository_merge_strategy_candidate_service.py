"""Offline candidate for a future repository integration strategy decision."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_tag_push_results_review_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1 = (
    "marketflow_repository_merge_strategy_candidate_v1"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_VALID = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_VALID"
)

EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = (
    "83ef5805ead9310494bbe3cb2122ffb8946861d36b3b20bcb81f2376ee9af0b4"
)
EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST = (
    "cf406bc974ebd88ffdfd1567b7e175fe17128e4e2adf770efbbf240df3819d5c"
)
EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_TAG_MANIFEST_DIGEST
EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
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
EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT = "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)

PACKAGE_NO_MAIN_MERGE_BRANCH_AND_TAG_TRACEABILITY_ONLY = (
    "PACKAGE_NO_MAIN_MERGE_BRANCH_AND_TAG_TRACEABILITY_ONLY"
)
PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION = (
    "PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION"
)
PACKAGE_SQUASH_MERGE_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW = (
    "PACKAGE_SQUASH_MERGE_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW"
)
PACKAGE_MERGE_COMMIT_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW = (
    "PACKAGE_MERGE_COMMIT_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW"
)
PACKAGE_SELECTIVE_DOCS_AND_STATUS_ONLY_INTEGRATION = (
    "PACKAGE_SELECTIVE_DOCS_AND_STATUS_ONLY_INTEGRATION"
)
PACKAGE_DEFER_MERGE_UNTIL_BRANCH_CLEANUP_PLAN = (
    "PACKAGE_DEFER_MERGE_UNTIL_BRANCH_CLEANUP_PLAN"
)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

MERGE_STRATEGY_PHILOSOPHY = (
    "Main integration should protect origin/main, preserve terminal evidence traceability, "
    "avoid destructive branch cleanup, and separate merge planning from merge execution."
)
MERGE_STRATEGY_BOUNDARY = (
    "Candidate-only; no merge, rebase, squash, cherry-pick, branch deletion, cleanup, or main push is performed."
)
MERGE_STRATEGY_GOAL = (
    "Prepare a conservative future decision on whether the terminal governance/evidence branch stack "
    "should remain branch-and-tag based, be integrated through a temporary integration branch, or "
    "later be merged to main after separate approval."
)

PROPOSED_MERGE_STRATEGY_PACKAGES = [
    {
        "package_id": PACKAGE_NO_MAIN_MERGE_BRANCH_AND_TAG_TRACEABILITY_ONLY,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Keep current evidence preserved through branches and published governance tags only; do not merge the stack to main.",
        "recommended_for": "Conservative archive-only governance posture.",
        "selected": False, "approved": False, "executed": False, "main_push_required": False,
    },
    {
        "package_id": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Create a future temporary integration branch from protected main and attempt the terminal stack integration there before any main merge is considered.",
        "recommended_for": "Safest engineering approach before any main integration decision.",
        "selected": False, "approved": False, "executed": False, "main_push_required": False,
    },
    {
        "package_id": PACKAGE_SQUASH_MERGE_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Plan a future squash merge of the terminal governance stack to main after operator review, full validation, and explicit approval.",
        "selected": False, "approved": False, "executed": False, "main_push_required": True,
    },
    {
        "package_id": PACKAGE_MERGE_COMMIT_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Plan a future merge commit preserving branch history into main after operator review, full validation, and explicit approval.",
        "selected": False, "approved": False, "executed": False, "main_push_required": True,
    },
    {
        "package_id": PACKAGE_SELECTIVE_DOCS_AND_STATUS_ONLY_INTEGRATION,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Plan future selective integration of documentation/status/plan artifacts only, excluding runtime services unless separately approved.",
        "selected": False, "approved": False, "executed": False, "main_push_required": True,
    },
    {
        "package_id": PACKAGE_DEFER_MERGE_UNTIL_BRANCH_CLEANUP_PLAN,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Delay any merge decision until branch cleanup and backup/bundle planning are completed.",
        "selected": False, "approved": False, "executed": False, "main_push_required": False,
    },
]

MERGE_PREREQUISITES = {
    "operator_review_of_merge_strategy_candidate_required": True,
    "operator_approval_required_before_integration_branch": True,
    "operator_approval_required_before_main_merge": True,
    "working_tree_clean_required_before_any_merge": True,
    "origin_main_protection_required": True,
    "backup_or_bundle_required_before_cleanup": True,
    "published_tags_verified_before_merge": True,
    "full_pytest_required_on_integration_branch": True,
    "diff_review_required_before_main_merge": True,
    "main_push_requires_separate_approval": True,
    "force_push_forbidden": True,
    "branch_delete_forbidden_until_cleanup_approval": True,
}

CANDIDATE_INTEGRATION_BRANCH_PLAN = {
    "candidate_integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
    "candidate_integration_base": "origin/main",
    "candidate_integration_source_branch": "feature/marketflow-repository-tag-push-results-review-v1",
    "candidate_integration_source_commit": EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT,
    "candidate_integration_status": "PLANNED_NOT_CREATED",
    "integration_branch_created": False, "integration_merge_performed": False,
    "integration_pytest_performed": False, "main_merge_performed": False,
    "main_push_performed": False,
}

MERGE_NON_GOALS = [
    "do_not_merge_now", "do_not_create_integration_branch_now", "do_not_push_main_now",
    "do_not_rebase_now", "do_not_squash_now", "do_not_cherry_pick_now",
    "do_not_delete_branches_now", "do_not_cleanup_now", "do_not_modify_tags",
    "do_not_push_additional_tags", "do_not_modify_origin_main",
    "do_not_imply_predictive_usefulness_acceptance", "do_not_imply_profitability_acceptance",
    "do_not_imply_runtime_authority", "do_not_imply_trading_authority",
]

CHAIN_IDS = [
    "CHAIN_EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH",
    "CHAIN_TAGGING_AND_TAG_PUSH_GOVERNANCE", "CHAIN_VPA_WYCKOFF_RULE_BASELINE",
    "CHAIN_FEATURE_LABEL_MATRIX", "CHAIN_SIGNAL_FEATURE_GENERATION",
    "CHAIN_OBJECTIVE_LABEL_TARGET_GENERATION", "CHAIN_EXPECTANCY_OBJECTIVE_DESIGN",
    "CHAIN_ALGORITHM_STRATEGY_CHARTER", "CHAIN_PRIOR_IMPROVED_EVIDENCE_ARCHIVE",
    "CHAIN_MISCELLANEOUS_OTHER_FEATURES",
]

NEXT_CHAIN = [
    "Repository Merge Strategy Operator Review v1.",
    "Repository Merge Strategy Approval v1, if selected.",
    "Repository Integration Branch Execution v1, if approved.",
    "Repository Integration Branch Results Review v1.",
    "Repository Main Merge Approval v1, only if integration branch review passes.",
    "Repository Main Merge Execution v1, only if separately approved.",
    "Repository Branch Cleanup Candidate v1, only after main integration strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
]
NEXT_GATES = [
    "repository_merge_strategy_operator_review", "repository_merge_strategy_approval_if_selected",
    "repository_integration_branch_execution_if_approved", "repository_integration_branch_results_review",
    "repository_main_merge_approval_if_integration_passes", "repository_main_merge_execution_if_approved",
    "repository_branch_cleanup_candidate_after_merge_strategy", "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
]
RISK_CONTROLS = [
    "candidate_does_not_merge", "candidate_does_not_create_integration_branch",
    "candidate_does_not_rebase", "candidate_does_not_squash_merge",
    "candidate_does_not_cherry_pick", "candidate_does_not_push_main",
    "candidate_does_not_force_push", "candidate_does_not_delete_branches",
    "candidate_does_not_delete_remote_branches", "candidate_does_not_prune_remotes",
    "candidate_does_not_modify_origin_main", "candidate_does_not_modify_tags",
    "candidate_does_not_push_additional_tags", "candidate_does_not_modify_marketflow_outputs",
    "candidate_does_not_call_providers", "candidate_does_not_acquire_market_data",
    "candidate_does_not_regenerate_dataset", "candidate_does_not_rerun_tag_push_results_review",
    "candidate_does_not_rerun_tag_push_execution", "candidate_does_not_rerun_inventory",
    "candidate_does_not_rerun_evidence", "candidate_does_not_recompute_metrics",
    "candidate_does_not_train_models", "candidate_does_not_score_strategy",
    "candidate_does_not_generate_recommendations", "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability", "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_broker_execution", "main_push_requires_separate_approval",
    "integration_branch_requires_separate_approval", "cleanup_requires_separate_approval",
    "protect_origin_main", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_results_review_digest_bound", "source_remote_manifest_review_digest_bound",
    "source_tag_push_execution_digest_bound", "source_remote_manifest_digest_bound",
    "source_tag_push_approval_digest_bound", "source_operator_review_digest_bound",
    "source_candidate_digest_bound", "source_tagging_results_review_digest_bound",
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound", "origin_main_commit_bound",
    "source_tag_push_review_ready_true", "candidate_created_true", "candidate_ready_true",
    "recommended_merge_strategy_present", "merge_packages_present_6",
    "integration_branch_plan_present", "integration_branch_created_false",
    "merge_strategy_selected_false", "merge_strategy_approved_false",
    "merge_strategy_authorized_false", "merge_strategy_executed_false",
    "merge_performed_false", "rebase_performed_false", "squash_merge_performed_false",
    "cherry_pick_performed_false", "main_push_false", "force_push_false",
    "branch_delete_false", "remote_delete_false", "remote_prune_false",
    "origin_main_modified_false", "tags_pushed_again_false",
    "additional_tags_created_false", "tags_modified_false", "tags_deleted_false",
    "cleanup_candidate_created_false", "marketflow_outputs_not_tracked",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "chain_merge_impact_summary_present", "merge_prerequisites_defined",
    "merge_non_goals_defined", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryMergeStrategyCandidateError(ValueError):
    """Raised when merge-strategy candidate evidence violates its boundary."""


def approved_marketflow_repository_merge_strategy_git_snapshot_v1() -> dict[str, Any]:
    return {
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "local_branch_count": 301, "remote_ref_count": 273, "total_ref_count": 574,
        "local_tag_count": 32, "remote_candidate_namespace_tag_count": 4,
        "remote_approved_tag_count": 4, "verified_remote_terminal_tag_count": 4,
        "extra_remote_candidate_namespace_tag_count": 0,
        "tracked_marketflow_file_count": 0,
    }


def _git_snapshot(repo_root: Path) -> dict[str, Any]:
    git = source_service.source_service._git
    local = git(repo_root, "for-each-ref", "--format=%(refname)", "refs/heads")
    remote = git(repo_root, "for-each-ref", "--format=%(refname)", "refs/remotes")
    tags = git(repo_root, "for-each-ref", "--format=%(refname)", "refs/tags")
    namespace = source_service.source_service._remote_tags(repo_root)
    local_count = len(local.splitlines()) if local else 0
    remote_count = len(remote.splitlines()) if remote else 0
    return {
        "origin_main_commit": source_service.source_service._origin_main(repo_root),
        "local_branch_count": local_count, "remote_ref_count": remote_count,
        "total_ref_count": local_count + remote_count,
        "local_tag_count": len(tags.splitlines()) if tags else 0,
        "remote_candidate_namespace_tag_count": len(namespace),
        "remote_approved_tag_count": len(set(namespace) & set(source_service.EXPECTED_REMOTE_REFS)),
        "verified_remote_terminal_tag_count": len(set(namespace) & set(source_service.EXPECTED_REMOTE_REFS)),
        "extra_remote_candidate_namespace_tag_count": len(set(namespace) - set(source_service.EXPECTED_REMOTE_REFS)),
        "tracked_marketflow_file_count": source_service.source_service._tracked_marketflow_count(repo_root),
    }


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if source_review.get("marketflow_repository_tag_push_results_review_digest") != EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST:
        raise MarketFlowRepositoryMergeStrategyCandidateError("source results-review digest mismatch")
    if source_review.get("marketflow_repository_tag_push_results_review_remote_tag_manifest_digest") != EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST:
        raise MarketFlowRepositoryMergeStrategyCandidateError("source remote manifest review digest mismatch")
    return deepcopy(source_review.get("source_evidence", {}))


def _chain_summary() -> list[dict[str, Any]]:
    return [{
        "chain_id": chain_id, "chain_name": chain_id.removeprefix("CHAIN_").replace("_", " ").title(),
        "source_status": "COMMITTED_EVIDENCE_CHAIN_PRESERVED",
        "published_tag_status": "TERMINAL_TAG_PUBLISHED" if index < 2 else "COVERED_BY_TERMINAL_GOVERNANCE_STACK",
        "merge_relevance": "REVIEW_ON_FUTURE_INTEGRATION_BRANCH",
        "candidate_merge_handling": "PRESERVE_AND_VALIDATE_WITHOUT_MAIN_MUTATION",
        "merge_required_now": False, "operator_review_required": True,
        "main_push_required_now": False,
    } for index, chain_id in enumerate(CHAIN_IDS)]


def _base_candidate(source_review: Mapping[str, Any] | None, snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True, "planning_only": True, "governance_only": True,
        "operator_review_required": True,
        "source_tag_push_results_review_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1,
        "source_tag_push_results_review_status": source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY,
        "source_tag_push_results_review_scope": source_service.REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tag_push_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_tag_manifest_review_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest": EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_remote_manifest_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest": EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_tag_push_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
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
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": snapshot["origin_main_commit"],
        "source_tag_push_results_review_commit": EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT,
        "source_repository_context": deepcopy(dict(snapshot)),
        "repository_merge_strategy_candidate_created": True,
        "repository_merge_strategy_candidate_ready_for_operator_review": True,
        "ready_for_repository_merge_strategy_operator_review": True,
        "repository_merge_strategy_selected": False, "repository_merge_strategy_approved": False,
        "repository_merge_strategy_authorized": False, "repository_merge_strategy_executed": False,
        "repository_integration_branch_created": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_squash_merge_performed": False, "git_cherry_pick_performed": False,
        "git_main_push_performed": False, "origin_main_modified_by_this_task": False,
        "repository_cleanup_candidate_created": False, "repository_cleanup_approved": False,
        "repository_cleanup_executed": False, "git_branch_delete_performed": False,
        "git_remote_delete_performed": False, "git_force_push_performed": False,
        "git_remote_prune_performed": False, "repository_tags_pushed_again": False,
        "additional_tag_push_performed": False, "additional_tags_created": False,
        "tags_modified": False, "tags_deleted": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "merge_strategy_philosophy": MERGE_STRATEGY_PHILOSOPHY,
        "merge_strategy_boundary": MERGE_STRATEGY_BOUNDARY,
        "merge_strategy_goal": MERGE_STRATEGY_GOAL,
        "proposed_merge_strategy_packages": deepcopy(PROPOSED_MERGE_STRATEGY_PACKAGES),
        "recommended_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": "The repository contains a large stacked governance/evidence chain and many branches; a temporary integration branch provides the safest non-main validation path before any merge-to-main decision.",
        "merge_prerequisites": deepcopy(MERGE_PREREQUISITES),
        "candidate_integration_branch_plan": deepcopy(CANDIDATE_INTEGRATION_BRANCH_PLAN),
        "merge_non_goals": list(MERGE_NON_GOALS),
        "chain_merge_impact_summary": _chain_summary(),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": snapshot["tracked_marketflow_file_count"],
        "no_tracked_marketflow_files": snapshot["tracked_marketflow_file_count"] == 0,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1",
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    plan = candidate.get("candidate_integration_branch_plan", {})
    snapshot = candidate.get("source_repository_context", {})
    return {
        "source_results_review_digest_bound": candidate.get("source_tag_push_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest_bound": candidate.get("source_remote_tag_manifest_review_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest_bound": candidate.get("source_tag_push_execution_digest") == EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_remote_manifest_digest_bound": candidate.get("source_tag_push_remote_manifest_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest_bound": candidate.get("source_tag_push_approval_digest") == EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_operator_review_digest_bound": candidate.get("source_tag_push_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": candidate.get("source_tag_push_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest_bound": candidate.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST,
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
        "source_tag_push_review_ready_true": candidate.get("source_tag_push_results_review_status") == source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY,
        "candidate_created_true": candidate.get("repository_merge_strategy_candidate_created") is True,
        "candidate_ready_true": candidate.get("repository_merge_strategy_candidate_ready_for_operator_review") is True,
        "recommended_merge_strategy_present": candidate.get("recommended_merge_strategy_package") == PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION and candidate.get("recommendation_status") == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "merge_packages_present_6": candidate.get("proposed_merge_strategy_packages") == PROPOSED_MERGE_STRATEGY_PACKAGES,
        "integration_branch_plan_present": plan == CANDIDATE_INTEGRATION_BRANCH_PLAN,
        "integration_branch_created_false": candidate.get("repository_integration_branch_created") is False and plan.get("integration_branch_created") is False,
        "merge_strategy_selected_false": candidate.get("repository_merge_strategy_selected") is False,
        "merge_strategy_approved_false": candidate.get("repository_merge_strategy_approved") is False,
        "merge_strategy_authorized_false": candidate.get("repository_merge_strategy_authorized") is False,
        "merge_strategy_executed_false": candidate.get("repository_merge_strategy_executed") is False,
        "merge_performed_false": candidate.get("git_merge_performed") is False,
        "rebase_performed_false": candidate.get("git_rebase_performed") is False,
        "squash_merge_performed_false": candidate.get("git_squash_merge_performed") is False,
        "cherry_pick_performed_false": candidate.get("git_cherry_pick_performed") is False,
        "main_push_false": candidate.get("git_main_push_performed") is False,
        "force_push_false": candidate.get("git_force_push_performed") is False,
        "branch_delete_false": candidate.get("git_branch_delete_performed") is False,
        "remote_delete_false": candidate.get("git_remote_delete_performed") is False,
        "remote_prune_false": candidate.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": candidate.get("origin_main_modified_by_this_task") is False,
        "tags_pushed_again_false": candidate.get("repository_tags_pushed_again") is False and candidate.get("additional_tag_push_performed") is False,
        "additional_tags_created_false": candidate.get("additional_tags_created") is False,
        "tags_modified_false": candidate.get("tags_modified") is False,
        "tags_deleted_false": candidate.get("tags_deleted") is False,
        "cleanup_candidate_created_false": candidate.get("repository_cleanup_candidate_created") is False,
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
        "chain_merge_impact_summary_present": len(candidate.get("chain_merge_impact_summary", [])) == 10,
        "merge_prerequisites_defined": candidate.get("merge_prerequisites") == MERGE_PREREQUISITES,
        "merge_non_goals_defined": candidate.get("merge_non_goals") == MERGE_NON_GOALS,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files") is True and snapshot.get("tracked_marketflow_file_count") == 0,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": PASS if actual else FAIL, "expected": True,
            "actual": actual, "severity": BLOCKER,
            "message": "candidate evidence matches" if actual else "candidate evidence mismatch"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(candidate)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_merge_strategy_candidate_created": True,
        "repository_merge_strategy_candidate_ready_for_operator_review": True,
        "recommended_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "merge_strategy_selected": False, "merge_strategy_approved": False,
        "integration_branch_created": False, "merge_performed": False,
        "main_pushed": False, "cleanup_candidate_created": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_merge_strategy_candidate_digest_v1(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_merge_strategy_candidate_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_merge_strategy_candidate_v1(
    *, source_review: dict | None = None, repo_root: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict:
    """Build a non-authorizing candidate from committed evidence constants."""
    snapshot = deepcopy(git_snapshot) if git_snapshot is not None else (
        _git_snapshot(Path(repo_root)) if repo_root is not None
        else approved_marketflow_repository_merge_strategy_git_snapshot_v1()
    )
    if snapshot.get("origin_main_commit") != EXPECTED_ORIGIN_MAIN_COMMIT:
        raise MarketFlowRepositoryMergeStrategyCandidateError("origin/main commit mismatch")
    if snapshot.get("tracked_marketflow_file_count") != 0:
        raise MarketFlowRepositoryMergeStrategyCandidateError("tracked .marketflow files detected")
    candidate = _base_candidate(source_review, snapshot)
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_merge_strategy_candidate_digest"] = marketflow_repository_merge_strategy_candidate_digest_v1(candidate)
    validate_marketflow_repository_merge_strategy_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_merge_strategy_candidate_v1(candidate: dict) -> dict:
    """Validate exact evidence, packages, planning state, and closed Git gates."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate must be an object")
    required = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN,
    }
    for field, expected in required.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryMergeStrategyCandidateError(f"{field} mismatch")
    values = _check_values(candidate)
    failed = [check_id for check_id in REQUIRED_CHECK_IDS if not values[check_id]]
    if failed:
        raise MarketFlowRepositoryMergeStrategyCandidateError(f"candidate check failed: {failed[0]}")
    checklist = candidate.get("checklist")
    if checklist != _checklist(candidate) or any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate checklist mismatch")
    if candidate.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate summary mismatch")
    digest = candidate.get("marketflow_repository_merge_strategy_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate digest missing")
    if digest != marketflow_repository_merge_strategy_candidate_digest_v1(candidate):
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate digest mismatch")
    return {"status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_VALID,
            "artifact_kind": candidate["artifact_kind"], "candidate_status": candidate["candidate_status"],
            "marketflow_repository_merge_strategy_candidate_digest": digest,
            **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_marketflow_repository_merge_strategy_candidate_markdown_v1(candidate: dict) -> str:
    """Render a sanitized candidate plan without implying approval or execution."""
    validation = validate_marketflow_repository_merge_strategy_candidate_v1(candidate)
    sections = [
        ("Title", ["MarketFlow Repository Merge Strategy Candidate v1"]),
        ("MarketFlow Repository Merge Strategy Candidate v1", [f"Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.", f"Digest: `{validation['marketflow_repository_merge_strategy_candidate_digest']}`."]),
        ("Source Tag Push Results Review", [f"Review digest: `{candidate['source_tag_push_results_review_digest']}`.", f"Source commit: `{candidate['source_tag_push_results_review_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(candidate['source_evidence'])}."]),
        ("Repository Context", [str(candidate["source_repository_context"])]),
        ("Candidate Scope", [candidate["candidate_scope"]]),
        ("Merge Strategy Philosophy", [candidate["merge_strategy_philosophy"], candidate["merge_strategy_boundary"], candidate["merge_strategy_goal"]]),
        ("Recommended Merge Strategy", [candidate["recommended_merge_strategy_package"], candidate["recommendation_status"], candidate["recommendation_reason"]]),
        ("Proposed Merge Packages", [f"{row['package_id']}: {row['status']}" for row in candidate["proposed_merge_strategy_packages"]]),
        ("Merge Prerequisites", [f"{key}: {value}" for key, value in candidate["merge_prerequisites"].items()]),
        ("Candidate Integration Branch Plan", [f"{key}: {value}" for key, value in candidate["candidate_integration_branch_plan"].items()]),
        ("Merge Non-Goals", list(candidate["merge_non_goals"])),
        ("Chain Merge Impact Summary", [f"{row['chain_id']}: {row['candidate_merge_handling']}" for row in candidate["chain_merge_impact_summary"]]),
        ("Next Chain", list(candidate["next_chain"])), ("Next Gates", list(candidate["next_gates"])),
        ("Risk Controls", list(candidate["risk_controls"])),
        ("Authority Boundaries", ["No package is selected, approved, authorized, or executed. Predictive usefulness and profitability remain not accepted; runtime and trading remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{candidate['summary']['passed_checks']} / {candidate['summary']['total_checks']} checks pass; {candidate['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No integration branch, merge, rebase, squash, cherry-pick, deletion, main push, force push, tag mutation, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Merge Strategy Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_merge_strategy_candidate_v1(
    output_dir: str | Path, *, source_review: dict | None = None,
    repo_root: str | Path | None = None, git_snapshot: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting existing evidence."""
    candidate = build_marketflow_repository_merge_strategy_candidate_v1(
        source_review=source_review, repo_root=repo_root, git_snapshot=git_snapshot
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_merge_strategy_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryMergeStrategyCandidateError("candidate output already exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": candidate["artifact_kind"],
            "candidate_status": candidate["candidate_status"],
            "marketflow_repository_merge_strategy_candidate_digest": candidate["marketflow_repository_merge_strategy_candidate_digest"],
            "payload_sha256": sha256_bytes(payload)}
