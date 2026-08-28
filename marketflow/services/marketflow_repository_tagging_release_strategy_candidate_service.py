"""Offline candidate for a future repository tagging and release strategy."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_state_branch_inventory_operator_review_service as source_review_service,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1 = (
    "marketflow_repository_tagging_release_strategy_candidate_v1"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_VALID = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_VALID"
)

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "c50b37ceb06597014056a739848da76b2da2923824ba48f85edea71a1e8fceb5"
)
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = (
    source_review_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
)
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = (
    source_review_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
)
EXPECTED_SOURCE_CLOSURE_DIGEST = source_review_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = (
    source_review_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
)
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_review_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_review_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_review_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_review_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_review_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_review_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_INVENTORY_PLAN_COMMIT = (
    source_review_service.EXPECTED_SOURCE_PLANNING_BRANCH_COMMIT
)
EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT = (
    "65cf8f129cfd49300a983401757e32f3fdc43570"
)
EXPECTED_TERMINAL_COMMIT = source_review_service.EXPECTED_SOURCE_SNAPSHOT_HEAD_COMMIT
SOURCE_EVIDENCE = deepcopy(source_review_service.SOURCE_EVIDENCE)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_BOUND_BY_THIS_CANDIDATE = "NOT_BOUND_BY_THIS_CANDIDATE"
REQUIRES_OPERATOR_SELECTION = "REQUIRES_OPERATOR_SELECTION"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS = (
    "PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS"
)
PACKAGE_GOVERNANCE_MILESTONE_TAGS = "PACKAGE_GOVERNANCE_MILESTONE_TAGS"
PACKAGE_SOURCE_PROTECTION_TAGS = "PACKAGE_SOURCE_PROTECTION_TAGS"
PACKAGE_NO_TAGGING_ARCHIVE_ONLY = "PACKAGE_NO_TAGGING_ARCHIVE_ONLY"

TERMINAL_TAG_NAMES = [
    "marketflow/expectancy-lab/final-archive-not-ready/v1",
    "marketflow/expectancy-lab/archive-record-not-ready/v1",
    "marketflow/expectancy-lab/operator-selection-option-a/v1",
    "marketflow/expectancy-lab/readiness-not-ready/v1",
]
GOVERNANCE_TAG_NAMES = [
    "marketflow/governance/strategy-charter/v1",
    "marketflow/governance/expectancy-objective/v1",
    "marketflow/governance/target-generation/v1",
    "marketflow/governance/signal-feature-generation/v1",
    "marketflow/governance/feature-label-matrix/v1",
    "marketflow/governance/vpa-wyckoff-baseline/v1",
    "marketflow/governance/expectancy-backtest-lab/v1",
]
SOURCE_PROTECTION_TAG_NAMES = [
    "marketflow/protected/origin-main/pre-integration",
    "marketflow/protected/terminal-expectancy-archive/pre-cleanup",
    "marketflow/protected/repository-inventory/pre-cleanup",
]

TAGGING_PHILOSOPHY = (
    "Preserve terminal evidence milestones with human-readable, non-runtime, "
    "non-trading, governance-only tags after separate operator review and approval."
)
TAGGING_BOUNDARY = (
    "Candidate-only; no tag is created, no tag is pushed, no branch is merged or "
    "deleted, and main remains untouched."
)
TAGGING_GOAL = (
    "Create a future release/tagging strategy that can mark terminal research evidence "
    "chains and protected governance milestones without implying predictive usefulness, "
    "profitability, runtime readiness, or trading authority."
)

TAGGING_PACKAGES = [
    {
        "package_id": PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Tag terminal expectancy-lab predictive-usefulness archive milestones.",
        "candidate_tags": list(TERMINAL_TAG_NAMES),
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_created": False,
    },
    {
        "package_id": PACKAGE_GOVERNANCE_MILESTONE_TAGS,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Tag strategy charter, objective design, target generation, feature generation, "
            "matrix generation, VPA/Wyckoff, and backtest-lab governance milestones."
        ),
        "candidate_tags": list(GOVERNANCE_TAG_NAMES),
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_created": False,
    },
    {
        "package_id": PACKAGE_SOURCE_PROTECTION_TAGS,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Tag protected origin/main, terminal branch tips, and selected source commits "
            "before any future cleanup."
        ),
        "candidate_tags": list(SOURCE_PROTECTION_TAG_NAMES),
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_created": False,
    },
    {
        "package_id": PACKAGE_NO_TAGGING_ARCHIVE_ONLY,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Skip tag creation and preserve branches only.",
        "candidate_tags": [],
        "selected": False,
        "approved": False,
        "executed": False,
        "tags_created": False,
    },
]

FUTURE_TAG_MESSAGE_TEMPLATE = """MarketFlow research governance milestone.

Artifact: <artifact_kind>
Status: <artifact_status>
Decision: <decision>
Scope: research-only / governance-only
Predictive usefulness: NOT_ACCEPTED
Profitability: NOT_ACCEPTED
Runtime: NOT_AUTHORIZED
Trading/Broker: NOT_AUTHORIZED
Source digest: <digest>
No trade recommendation is created by this tag."""


def _tag_definition(tag_name: str, target_branch: str, target_commit: str) -> dict[str, Any]:
    return {
        "tag_name": tag_name,
        "tag_target_branch": target_branch,
        "tag_target_commit": target_commit,
        "tag_type": "ANNOTATED_TAG_RECOMMENDED",
        "tag_message_template": FUTURE_TAG_MESSAGE_TEMPLATE,
        "tag_status": "CANDIDATE_TAG_NOT_CREATED",
        "tag_created": False,
        "tag_pushed": False,
        "operator_approval_required": True,
        "main_push_required": False,
        "runtime_authority_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
    }


CANDIDATE_TAG_DEFINITIONS = [
    _tag_definition(
        TERMINAL_TAG_NAMES[0],
        "feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1",
        EXPECTED_TERMINAL_COMMIT,
    ),
    _tag_definition(
        TERMINAL_TAG_NAMES[1],
        "feature/marketflow-predictive-usefulness-acceptance-path-archive-record-expectancy-lab-evidence-v1",
        "e2fcfb792ad14db8a2de69556c291529fda47a8e",
    ),
    _tag_definition(
        TERMINAL_TAG_NAMES[2],
        "feature/marketflow-operator-method-or-closure-selection-expectancy-lab-evidence-v1",
        "15c4fae495f88b54e30380f3d8b4aa54989fad39",
    ),
    _tag_definition(
        TERMINAL_TAG_NAMES[3],
        "feature/marketflow-predictive-usefulness-acceptance-readiness-review-expectancy-lab-evidence-v1",
        "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0",
    ),
    *[
        _tag_definition(name, REQUIRES_OPERATOR_SELECTION, NOT_BOUND_BY_THIS_CANDIDATE)
        for name in GOVERNANCE_TAG_NAMES
    ],
    _tag_definition(
        SOURCE_PROTECTION_TAG_NAMES[0], "origin/main", EXPECTED_ORIGIN_MAIN_COMMIT
    ),
    _tag_definition(
        SOURCE_PROTECTION_TAG_NAMES[1],
        "feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1",
        EXPECTED_TERMINAL_COMMIT,
    ),
    _tag_definition(
        SOURCE_PROTECTION_TAG_NAMES[2],
        "feature/marketflow-repository-state-branch-inventory-integration-plan-v1",
        EXPECTED_SOURCE_INVENTORY_PLAN_COMMIT,
    ),
]

TAGGING_PREREQUISITES = {
    "operator_review_of_tagging_candidate_required": True,
    "operator_approval_required_before_tagging": True,
    "working_tree_clean_required_before_tagging": True,
    "origin_main_protection_required": True,
    "backup_or_bundle_recommended_before_cleanup": True,
    "tag_message_must_include_not_ready_boundary": True,
    "tag_message_must_include_no_runtime_authority": True,
    "tag_message_must_include_no_trading_authority": True,
    "tag_creation_requires_separate_task": True,
    "tag_push_requires_separate_task": True,
}

TAGGING_NON_GOALS = [
    "do_not_tag_now",
    "do_not_push_tags_now",
    "do_not_merge_now",
    "do_not_delete_branches_now",
    "do_not_cleanup_now",
    "do_not_push_main_now",
    "do_not_change_origin_main",
    "do_not_create_release_package_now",
    "do_not_imply_predictive_usefulness_acceptance",
    "do_not_imply_profitability_acceptance",
    "do_not_imply_runtime_authority",
    "do_not_imply_trading_authority",
]


def _chain_summary(
    chain_id: str, chain_name: str, recommendation: str, candidate_tags: list[str]
) -> dict[str, Any]:
    return {
        "chain_id": chain_id,
        "chain_name": chain_name,
        "tagging_recommendation": recommendation,
        "candidate_tags": list(candidate_tags),
        "tags_created": False,
        "approval_required": True,
        "operator_review_required": True,
        "merge_required": False,
        "main_push_required": False,
    }


PER_CHAIN_TAGGING_CANDIDATE_SUMMARY = [
    _chain_summary(
        "CHAIN_EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH",
        "Expectancy Lab Predictive Usefulness Path",
        "RECOMMEND_TERMINAL_ARCHIVE_TAGS_FOR_OPERATOR_REVIEW",
        TERMINAL_TAG_NAMES,
    ),
    _chain_summary(
        "CHAIN_VPA_WYCKOFF_RULE_BASELINE",
        "VPA/Wyckoff Rule Baseline",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/vpa-wyckoff-baseline/v1"],
    ),
    _chain_summary(
        "CHAIN_FEATURE_LABEL_MATRIX",
        "Feature Label Matrix",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/feature-label-matrix/v1"],
    ),
    _chain_summary(
        "CHAIN_SIGNAL_FEATURE_GENERATION",
        "Signal Feature Generation",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/signal-feature-generation/v1"],
    ),
    _chain_summary(
        "CHAIN_OBJECTIVE_LABEL_TARGET_GENERATION",
        "Objective Label Target Generation",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/target-generation/v1"],
    ),
    _chain_summary(
        "CHAIN_EXPECTANCY_OBJECTIVE_DESIGN",
        "Expectancy Objective Design",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/expectancy-objective/v1"],
    ),
    _chain_summary(
        "CHAIN_ALGORITHM_STRATEGY_CHARTER",
        "Algorithm Strategy Charter",
        "AVAILABLE_GOVERNANCE_TAG_NOT_SELECTED",
        ["marketflow/governance/strategy-charter/v1"],
    ),
    _chain_summary(
        "CHAIN_PRIOR_IMPROVED_EVIDENCE_ARCHIVE",
        "Prior Improved Evidence Archive",
        "NO_TAG_PROPOSED_REQUIRES_OPERATOR_REVIEW",
        [],
    ),
    _chain_summary(
        "CHAIN_MISCELLANEOUS_OTHER_FEATURES",
        "Miscellaneous Other Features",
        "NO_TAG_PROPOSED_REQUIRES_OPERATOR_REVIEW",
        [],
    ),
]

NEXT_CHAIN = [
    "Repository Tagging / Release Strategy Operator Review v1.",
    "Repository Tagging Approval v1, if selected.",
    "Repository Tagging Execution v1, if approved.",
    "Repository Merge Strategy Candidate v1, only after tagging strategy review or explicit skip decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
]

NEXT_GATES = [
    "repository_tagging_release_strategy_operator_review",
    "repository_tagging_approval_if_selected",
    "repository_tagging_execution_if_approved",
    "repository_merge_strategy_candidate_after_tag_review",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "candidate_does_not_create_tags",
    "candidate_does_not_push_tags",
    "candidate_does_not_merge",
    "candidate_does_not_rebase",
    "candidate_does_not_delete_branches",
    "candidate_does_not_delete_remote_branches",
    "candidate_does_not_push_main",
    "candidate_does_not_force_push",
    "candidate_does_not_prune_remotes",
    "candidate_does_not_modify_origin_main",
    "candidate_does_not_modify_marketflow_outputs",
    "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data",
    "candidate_does_not_regenerate_dataset",
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
    "all_tags_are_candidate_only",
    "operator_review_required_before_tagging",
    "operator_approval_required_before_tagging",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
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
    "operator_review_ready_true",
    "candidate_created_true",
    "candidate_ready_true",
    "recommended_tagging_package_present",
    "terminal_tag_candidates_present_4",
    "tagging_packages_present_4",
    "candidate_tag_definitions_present",
    "tagging_prerequisites_defined",
    "tag_message_template_defined",
    "tagging_non_goals_defined",
    "per_chain_tagging_summary_present",
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
    "risk_controls_defined",
    "next_chain_defined",
    "next_gates_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryTaggingReleaseStrategyCandidateError(ValueError):
    """Raised when the candidate violates its evidence or authority contract."""


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_review, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "source_review must be an object"
        )
    try:
        source_review_service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(
            source_review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "source inventory operator review is invalid"
        ) from exc
    if source_review.get(
        "marketflow_repository_state_branch_inventory_operator_review_digest"
    ) != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "source inventory operator review digest mismatch"
        )
    return deepcopy(source_review["source_evidence"])


def _base_candidate(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "created_offline": True,
        "research_only": True,
        "planning_only": True,
        "operator_review_required": True,
        "source_inventory_operator_review_artifact_kind": source_review_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1,
        "source_inventory_operator_review_status": source_review_service.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_READY,
        "source_inventory_operator_review_scope": source_review_service.REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN,
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
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_inventory_plan_commit": EXPECTED_SOURCE_INVENTORY_PLAN_COMMIT,
        "source_operator_review_commit": EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_snapshot_local_branch_count": 290,
        "source_snapshot_remote_branch_count": 261,
        "source_snapshot_total_branch_ref_count": 551,
        "source_post_plan_push_live_local_branch_count": 290,
        "source_post_plan_push_live_remote_branch_count": 262,
        "source_post_plan_push_live_total_branch_ref_count": 552,
        "source_operator_review_live_local_branch_count": 291,
        "source_operator_review_live_remote_branch_count": 263,
        "source_operator_review_live_total_branch_ref_count": 554,
        "source_operator_review_ready": True,
        "repository_tagging_release_strategy_candidate_created": True,
        "repository_tagging_release_strategy_candidate_ready_for_operator_review": True,
        "ready_for_repository_tagging_release_strategy_operator_review": True,
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
        "tagging_philosophy": TAGGING_PHILOSOPHY,
        "tagging_boundary": TAGGING_BOUNDARY,
        "tagging_goal": TAGGING_GOAL,
        "tagging_packages": deepcopy(TAGGING_PACKAGES),
        "recommended_tagging_package": PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": (
            "The expectancy-lab path is terminal and archived not ready; tagging only "
            "terminal archive milestones is the narrowest, least destructive first release strategy."
        ),
        "candidate_tag_definitions": deepcopy(CANDIDATE_TAG_DEFINITIONS),
        "tagging_prerequisites": deepcopy(TAGGING_PREREQUISITES),
        "future_tag_message_template": FUTURE_TAG_MESSAGE_TEMPLATE,
        "tagging_non_goals": list(TAGGING_NON_GOALS),
        "per_chain_tagging_candidate_summary": deepcopy(PER_CHAIN_TAGGING_CANDIDATE_SUMMARY),
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
    }


def _check_values(candidate: Mapping[str, Any]) -> dict[str, bool]:
    tag_definitions = candidate.get("candidate_tag_definitions", [])
    packages = candidate.get("tagging_packages", [])
    return {
        "source_operator_review_digest_bound": candidate.get("source_inventory_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_inventory_plan_digest_bound": candidate.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": candidate.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": candidate.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": candidate.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": candidate.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": candidate.get("source_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": candidate.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": candidate.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": candidate.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": candidate.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": candidate.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": candidate.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_repository_counts_bound": (
            candidate.get("source_snapshot_local_branch_count"),
            candidate.get("source_snapshot_remote_branch_count"),
            candidate.get("source_snapshot_total_branch_ref_count"),
            candidate.get("source_post_plan_push_live_local_branch_count"),
            candidate.get("source_post_plan_push_live_remote_branch_count"),
            candidate.get("source_post_plan_push_live_total_branch_ref_count"),
            candidate.get("source_operator_review_live_local_branch_count"),
            candidate.get("source_operator_review_live_remote_branch_count"),
            candidate.get("source_operator_review_live_total_branch_ref_count"),
        ) == (290, 261, 551, 290, 262, 552, 291, 263, 554),
        "operator_review_ready_true": candidate.get("source_operator_review_ready") is True,
        "candidate_created_true": candidate.get("repository_tagging_release_strategy_candidate_created") is True,
        "candidate_ready_true": candidate.get("repository_tagging_release_strategy_candidate_ready_for_operator_review") is True and candidate.get("ready_for_repository_tagging_release_strategy_operator_review") is True,
        "recommended_tagging_package_present": candidate.get("recommended_tagging_package") == PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "terminal_tag_candidates_present_4": [row.get("tag_name") for row in tag_definitions[:4]] == TERMINAL_TAG_NAMES,
        "tagging_packages_present_4": packages == TAGGING_PACKAGES and len(packages) == 4,
        "candidate_tag_definitions_present": tag_definitions == CANDIDATE_TAG_DEFINITIONS and len(tag_definitions) == 14,
        "tagging_prerequisites_defined": candidate.get("tagging_prerequisites") == TAGGING_PREREQUISITES,
        "tag_message_template_defined": candidate.get("future_tag_message_template") == FUTURE_TAG_MESSAGE_TEMPLATE,
        "tagging_non_goals_defined": candidate.get("tagging_non_goals") == TAGGING_NON_GOALS,
        "per_chain_tagging_summary_present": candidate.get("per_chain_tagging_candidate_summary") == PER_CHAIN_TAGGING_CANDIDATE_SUMMARY,
        "tagging_strategy_selected_false": candidate.get("repository_tagging_release_strategy_selected") is False,
        "tagging_strategy_approved_false": candidate.get("repository_tagging_release_strategy_approved") is False,
        "tagging_strategy_authorized_false": candidate.get("repository_tagging_release_strategy_authorized") is False,
        "tagging_strategy_executed_false": candidate.get("repository_tagging_release_strategy_executed") is False,
        "tags_created_false": candidate.get("git_tag_created") is False and all(row.get("tag_created") is False for row in tag_definitions) and all(row.get("tags_created") is False for row in packages),
        "tags_pushed_false": candidate.get("git_tag_push_performed") is False and all(row.get("tag_pushed") is False for row in tag_definitions),
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
        "risk_controls_defined": candidate.get("risk_controls") == RISK_CONTROLS,
        "next_chain_defined": candidate.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": candidate.get("next_gates") == NEXT_GATES,
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
            "tagging candidate evidence matches"
            if actual
            else "tagging candidate evidence mismatch"
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
        "repository_tagging_release_strategy_candidate_created": True,
        "repository_tagging_release_strategy_candidate_ready_for_operator_review": True,
        "recommended_tagging_package": PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS,
        "candidate_tag_count": len(CANDIDATE_TAG_DEFINITIONS),
        "tags_created": False,
        "tags_pushed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tagging_release_strategy_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tagging_release_strategy_candidate_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tagging_release_strategy_candidate_v1(
    *, source_review: dict | None = None,
) -> dict:
    """Build the candidate without rerunning inventory or its operator review."""
    candidate = _base_candidate(source_review)
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_tagging_release_strategy_candidate_digest"] = (
        marketflow_repository_tagging_release_strategy_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_tagging_release_strategy_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_tagging_release_strategy_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, candidate content, and closed execution gates."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "candidate must be an object"
        )
    expected = _base_candidate(None)
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
                f"{field} mismatch"
            )
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(candidate):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate checklist failed"
        )
    if candidate.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate summary mismatch"
        )
    digest = candidate.get(
        "marketflow_repository_tagging_release_strategy_candidate_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate digest missing"
        )
    if digest != marketflow_repository_tagging_release_strategy_candidate_digest_v1(
        candidate
    ):
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_repository_tagging_release_strategy_candidate_digest": digest,
        **{
            key: candidate["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tagging_release_strategy_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_marketflow_repository_tagging_release_strategy_candidate_v1(
        candidate
    )
    sections = [
        ("Title", ["MarketFlow Repository Tagging / Release Strategy Candidate v1"]),
        (
            "MarketFlow Repository Tagging / Release Strategy Candidate v1",
            [
                f"Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
                f"Digest: `{validation['marketflow_repository_tagging_release_strategy_candidate_digest']}`.",
            ],
        ),
        (
            "Source Inventory Operator Review",
            [
                f"Source digest: `{candidate['source_inventory_operator_review_digest']}`.",
                f"Source commit: `{candidate['source_operator_review_commit']}`.",
            ],
        ),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(candidate['source_evidence'])}."]),
        (
            "Repository Context",
            [
                f"Origin main: `{candidate['origin_main_commit']}`.",
                "Frozen/source/post-review ref totals: 551 / 552 / 554.",
            ],
        ),
        ("Candidate Scope", [candidate["candidate_scope"]]),
        ("Tagging Philosophy", [candidate["tagging_philosophy"], candidate["tagging_boundary"], candidate["tagging_goal"]]),
        ("Recommended Tagging Package", [f"`{candidate['recommended_tagging_package']}`: {candidate['recommendation_reason']}"]),
        ("Candidate Tag Packages", [f"{row['package_id']}: {row['status']}" for row in candidate["tagging_packages"]]),
        ("Candidate Tag Definitions", [f"`{row['tag_name']}` -> `{row['tag_target_branch']}` @ `{row['tag_target_commit']}` ({row['tag_status']})" for row in candidate["candidate_tag_definitions"]]),
        ("Tagging Prerequisites", list(candidate["tagging_prerequisites"])),
        ("Future Tag Message Template", [candidate["future_tag_message_template"]]),
        ("Tagging Non-Goals", list(candidate["tagging_non_goals"])),
        ("Per-Chain Tagging Summary", [f"{row['chain_id']}: {row['tagging_recommendation']}" for row in candidate["per_chain_tagging_candidate_summary"]]),
        ("Next Chain", list(candidate["next_chain"])),
        ("Next Gates", list(candidate["next_gates"])),
        ("Risk Controls", list(candidate["risk_controls"])),
        ("Authority Boundaries", ["Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{candidate['summary']['passed_checks']} / {candidate['summary']['total_checks']} checks pass; {candidate['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag, tag push, merge, rebase, deletion, main push, force-push, prune, provider, data, metric, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tagging / Release Strategy Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tagging_release_strategy_candidate_v1(
    output_dir: str | Path, *, source_review: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing candidate."""
    candidate = build_marketflow_repository_tagging_release_strategy_candidate_v1(
        source_review=source_review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tagging_release_strategy_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTaggingReleaseStrategyCandidateError(
            "tagging candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "marketflow_repository_tagging_release_strategy_candidate_digest": candidate[
            "marketflow_repository_tagging_release_strategy_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
