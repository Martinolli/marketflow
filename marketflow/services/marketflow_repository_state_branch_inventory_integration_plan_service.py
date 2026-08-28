"""Read-only Git inventory and conservative integration planning for MarketFlow."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_service as final_archive,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1 = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_V1 = (
    "marketflow_repository_state_branch_inventory_integration_plan_v1"
)
MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY"
)
REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN = (
    "REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_VALID = (
    "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_VALID"
)

EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = "91320fd42e4dab0286c9250496278413ffd24a3f08669ea7a7344519942785ac"
EXPECTED_SOURCE_ARCHIVE_DIGEST = final_archive.EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = final_archive.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = final_archive.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = final_archive.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = final_archive.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = final_archive.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = final_archive.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = final_archive.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST = final_archive.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = final_archive.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = final_archive.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = final_archive.EXPECTED_SOURCE_RECORDS_DIGEST
SOURCE_EVIDENCE = final_archive.archive_service._source_evidence(None)
TARGET_UNIVERSE = list(final_archive.TARGET_UNIVERSE)
EXPECTED_ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
EXPECTED_INVENTORY_BASE_COMMIT = "0be55dc8a65a586368c192d6bc13302b9830a0b4"

TERMINAL_BRANCH = (
    "feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1"
)
PLAN_BRANCH = "feature/marketflow-repository-state-branch-inventory-integration-plan-v1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CATEGORY_MAIN_PROTECTED = "CATEGORY_MAIN_PROTECTED"
CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN = "CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN"
CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN = "CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN"
CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN = "CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN"
CATEGORY_FEATURE_LABEL_MATRIX_CHAIN = "CATEGORY_FEATURE_LABEL_MATRIX_CHAIN"
CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN = "CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN"
CATEGORY_STRATEGY_CHARTER_CHAIN = "CATEGORY_STRATEGY_CHARTER_CHAIN"
CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN = "CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN"
CATEGORY_IBKR_OR_BROKER_CHAIN = "CATEGORY_IBKR_OR_BROKER_CHAIN"
CATEGORY_OTHER_FEATURE_BRANCH = "CATEGORY_OTHER_FEATURE_BRANCH"
CATEGORY_REMOTE_TRACKING_ONLY = "CATEGORY_REMOTE_TRACKING_ONLY"
CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW = "CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW"

RISK_CONTROLS = [
    "inventory_does_not_merge", "inventory_does_not_rebase",
    "inventory_does_not_delete_branches", "inventory_does_not_delete_remote_branches",
    "inventory_does_not_create_tags", "inventory_does_not_push_main",
    "inventory_does_not_force_push", "inventory_does_not_prune_remotes",
    "inventory_does_not_modify_origin_main", "inventory_does_not_modify_marketflow_outputs",
    "inventory_does_not_call_providers", "inventory_does_not_acquire_market_data",
    "inventory_does_not_regenerate_dataset", "inventory_does_not_rerun_evidence",
    "inventory_does_not_recompute_metrics", "inventory_does_not_train_models",
    "inventory_does_not_score_strategy", "inventory_does_not_generate_recommendations",
    "inventory_does_not_accept_predictive_usefulness",
    "inventory_does_not_accept_profitability", "inventory_does_not_authorize_runtime",
    "inventory_does_not_authorize_broker_execution",
    "all_dispositions_are_recommendations_only", "operator_review_required_before_merge",
    "operator_review_required_before_delete", "operator_review_required_before_tagging",
    "protect_origin_main", "preserve_terminal_archive_evidence", "preserve_meta_limitation",
]

INTEGRATION_PHASES = [
    {
        "phase_number": 0, "phase_name": "Inventory and Freeze",
        "status": "COMPLETED_BY_THIS_ARTIFACT",
        "purpose": "Record branch refs, source digests, and categories without modifying main.",
        "execution_performed": True,
    },
    {
        "phase_number": 1, "phase_name": "Operator Review of Inventory",
        "status": "FUTURE_NOT_STARTED",
        "purpose": "Review categories, protected branches, and branches that must never be deleted.",
        "execution_performed": False,
    },
    {
        "phase_number": 2, "phase_name": "Tagging / Release Strategy Candidate",
        "status": "FUTURE_NOT_STARTED",
        "purpose": "Plan possible annotated tags for terminal evidence milestones.",
        "execution_performed": False,
    },
    {
        "phase_number": 3, "phase_name": "Merge Strategy Candidate",
        "status": "FUTURE_NOT_STARTED",
        "purpose": "Plan whether selected governance services and docs should merge, squash, or remain branch-only.",
        "execution_performed": False,
    },
    {
        "phase_number": 4, "phase_name": "Branch Archive / Cleanup Candidate",
        "status": "FUTURE_NOT_STARTED",
        "purpose": "Plan cleanup only after operator review, tags, backup, and merge decisions.",
        "execution_performed": False,
    },
    {
        "phase_number": 5, "phase_name": "Execution of Approved Cleanup",
        "status": "FUTURE_NOT_STARTED",
        "purpose": "Execute cleanup only if separately approved in a controlled future task.",
        "execution_performed": False,
    },
]

REQUIRED_CHECK_IDS = [
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_operator_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound",
    "current_head_commit_bound", "origin_main_commit_bound", "working_tree_clean_true",
    "branch_inventory_created_true", "integration_plan_created_true",
    "local_branch_count_recorded", "remote_branch_count_recorded",
    "total_branch_ref_count_recorded", "current_branch_recorded",
    "terminal_expectancy_lab_branch_identified", "origin_main_protected", "main_push_false",
    "merge_performed_false", "rebase_performed_false", "branch_delete_performed_false",
    "remote_delete_performed_false", "tag_created_false", "force_push_false",
    "remote_prune_false", "marketflow_outputs_not_tracked", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "risk_controls_defined",
    "integration_phases_defined", "recommended_policy_inventory_first",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(ValueError):
    """Raised when a repository inventory violates its planning-only contract."""


def _run_git(repo_root: Path, *args: str, allow_failure: bool = False) -> str:
    allowed = {"status", "branch", "for-each-ref", "rev-parse", "ls-files"}
    if not args or args[0] not in allowed:
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
            "only approved read-only git commands are allowed"
        )
    completed = subprocess.run(
        ["git", *args], cwd=repo_root, check=False, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if completed.returncode and not allow_failure:
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
            f"read-only git command failed: {args[0]}"
        )
    return completed.stdout.rstrip("\r\n") if completed.returncode == 0 else ""


def collect_marketflow_repository_git_snapshot_v1(repo_root: str | Path) -> dict[str, Any]:
    """Collect a point-in-time snapshot using only approved read-only Git commands."""
    root = Path(repo_root).resolve()
    if not (root / ".git").exists():
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
            "repo_root must be a Git worktree root"
        )
    current_branch = _run_git(root, "branch", "--show-current")
    current_head = _run_git(root, "rev-parse", "HEAD")
    origin_main = _run_git(root, "rev-parse", "origin/main")
    main_commit = _run_git(root, "rev-parse", "--verify", "main", allow_failure=True) or None
    status = _run_git(root, "status", "--porcelain")
    tracked_marketflow = _run_git(root, "ls-files", "--", ".marketflow")
    raw_refs = _run_git(
        root, "for-each-ref", "--sort=refname",
        "--format=%(refname)%09%(objectname)%09%(committerdate:iso8601-strict)%09%(subject)%09%(symref)",
        "refs/heads", "refs/remotes",
    )
    refs: list[dict[str, Any]] = []
    for line in raw_refs.splitlines():
        parts = line.split("\t", 4)
        if len(parts) != 5:
            raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
                "unexpected for-each-ref output"
            )
        ref_name, commit_sha, committer_date, subject, symbolic_target = parts
        ref_type = "LOCAL" if ref_name.startswith("refs/heads/") else "REMOTE"
        short_name = ref_name.removeprefix("refs/heads/").removeprefix("refs/remotes/")
        refs.append(
            {
                "ref_name": ref_name, "ref_type": ref_type, "short_name": short_name,
                "commit_sha": commit_sha, "subject": subject,
                "committer_date": committer_date, "symbolic_target": symbolic_target or None,
            }
        )
    return {
        "repo_root_name": root.name,
        "current_branch": current_branch,
        "current_head_commit": current_head,
        "origin_main_commit": origin_main,
        "main_commit_if_available": main_commit,
        "working_tree_clean": not bool(status),
        "tracked_marketflow_files": tracked_marketflow.splitlines() if tracked_marketflow else [],
        "refs": refs,
    }


def _normalized_branch_name(short_name: str, ref_type: str) -> str:
    return short_name.removeprefix("origin/") if ref_type == "REMOTE" else short_name


def _role_flags(name: str) -> dict[str, bool]:
    lower = name.lower()
    return {
        "is_terminal_archive_branch": name == TERMINAL_BRANCH,
        "is_candidate_branch": "candidate" in lower,
        "is_operator_review_branch": any(token in lower for token in ("operator-review", "candidate-review", "review-package")),
        "is_approval_branch": "approval" in lower,
        "is_execution_branch": "execution" in lower or "live-run" in lower,
        "is_results_review_branch": "results-review" in lower,
        "is_reassessment_branch": "reassessment" in lower,
        "is_readiness_branch": "readiness" in lower,
        "is_closure_branch": "closure" in lower,
        "is_selection_branch": "selection" in lower,
        "is_archive_branch": "archive" in lower,
        "is_final_summary_branch": "final-archive-summary" in lower,
        "is_strategy_or_charter_branch": "strategy-charter" in lower or "strategy_charter" in lower,
        "is_marketflow_governance_branch": lower.startswith("feature/") and any(
            token in lower for token in (
                "marketflow", "evidence", "candidate", "review", "approval", "freeze",
                "readiness", "archive", "charter", "dataset", "identity", "acquisition",
                "dividend", "split", "predictive", "research-applicability",
            )
        ),
        "is_ibkr_or_broker_branch": "ibkr" in lower or "broker" in lower,
    }


def _category(name: str, ref_type: str) -> str:
    lower = name.lower()
    if name == "main":
        return CATEGORY_MAIN_PROTECTED
    if name == TERMINAL_BRANCH:
        return CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN
    if "ibkr" in lower or "broker" in lower:
        return CATEGORY_IBKR_OR_BROKER_CHAIN
    if "improved-evidence" in lower and "archive" in lower:
        return CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN
    if "vpa-wyckoff" in lower:
        return CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN
    if "feature-label-matrix" in lower:
        return CATEGORY_FEATURE_LABEL_MATRIX_CHAIN
    if "strategy-charter" in lower:
        return CATEGORY_STRATEGY_CHARTER_CHAIN
    if any(token in lower for token in ("expectancy-backtest-lab", "expectancy-lab-evidence")):
        return CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN
    if any(token in lower for token in (
        "signal-or-feature", "feature-generation", "objective-label-or-target",
        "target-generation", "redesigned-label", "label-objective", "expectancy-objective",
    )):
        return CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN
    if lower.startswith(("feature/", "diagnostic/", "fix/", "chore/")):
        return CATEGORY_OTHER_FEATURE_BRANCH
    if ref_type == "REMOTE":
        return CATEGORY_REMOTE_TRACKING_ONLY
    return CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW


def _disposition(category: str) -> str:
    if category == CATEGORY_MAIN_PROTECTED:
        return "PROTECT_DO_NOT_TOUCH"
    if category == CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN:
        return "KEEP_TERMINAL_EVIDENCE"
    if category in {
        CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN, CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN,
        CATEGORY_FEATURE_LABEL_MATRIX_CHAIN, CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN,
        CATEGORY_STRATEGY_CHARTER_CHAIN, CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN,
    }:
        return "KEEP_FOR_TRACEABILITY"
    if category == CATEGORY_OTHER_FEATURE_BRANCH:
        return "CANDIDATE_FOR_FUTURE_ARCHIVE_AFTER_OPERATOR_CONFIRMATION"
    if category in {CATEGORY_REMOTE_TRACKING_ONLY, CATEGORY_IBKR_OR_BROKER_CHAIN}:
        return "REQUIRES_OPERATOR_REVIEW"
    return "UNKNOWN_DO_NOT_TOUCH"


def _classify_refs(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    current_branch = snapshot["current_branch"]
    rows: list[dict[str, Any]] = []
    for source in snapshot["refs"]:
        ref_type = source["ref_type"]
        short_name = source["short_name"]
        normalized = _normalized_branch_name(short_name, ref_type)
        flags = _role_flags(normalized)
        category = _category(normalized, ref_type)
        rows.append(
            {
                **deepcopy(source),
                "is_current_branch": ref_type == "LOCAL" and short_name == current_branch,
                "is_main": ref_type == "LOCAL" and short_name == "main",
                "is_origin_main": ref_type == "REMOTE" and short_name == "origin/main",
                **flags,
                "is_unknown_category": category == CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW,
                "category": category,
                "suggested_disposition": _disposition(category),
            }
        )
    return rows


def _category_summary(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    categories = sorted({row["category"] for row in inventory})
    return [
        {
            "category": category,
            "ref_count": sum(row["category"] == category for row in inventory),
            "local_ref_count": sum(row["category"] == category and row["ref_type"] == "LOCAL" for row in inventory),
            "remote_ref_count": sum(row["category"] == category and row["ref_type"] == "REMOTE" for row in inventory),
        }
        for category in categories
    ]


def _chain_summary(
    inventory: list[dict[str, Any]], *, chain_id: str, chain_name: str,
    predicate: Any, chain_status: str, terminal_branch: str | None = None,
    terminal_commit: str | None = None, source_digest: str | None = None,
    operator_action_required: bool = True, recommended_next_action: str = "OPERATOR_REVIEW_REQUIRED",
) -> dict[str, Any]:
    matches = [
        row["short_name"] for row in inventory
        if row["ref_type"] == "LOCAL" and predicate(_normalized_branch_name(row["short_name"], row["ref_type"]))
    ]
    return {
        "chain_id": chain_id, "chain_name": chain_name,
        "chain_status": chain_status if matches else "NOT_PRESENT",
        "representative_branches": sorted(matches)[:40],
        "matching_local_branch_count": len(matches),
        "terminal_branch_if_known": terminal_branch,
        "terminal_commit_if_known": terminal_commit,
        "source_digest_if_known": source_digest,
        "operator_action_required": operator_action_required if matches else False,
        "recommended_next_action": recommended_next_action if matches else "NONE_NOT_PRESENT",
        "merge_readiness": "NOT_EVALUATED_BY_THIS_TASK",
        "delete_readiness": "NOT_AUTHORIZED_BY_THIS_TASK",
        "archive_readiness": "PLANNING_ONLY",
    }


def _chain_summaries(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    low = lambda name: name.lower()
    known_categories = {
        CATEGORY_MAIN_PROTECTED, CATEGORY_TERMINAL_EXPECTANCY_LAB_ARCHIVE_CHAIN,
        CATEGORY_EXPECTANCY_LAB_EVIDENCE_CHAIN, CATEGORY_VPA_WYCKOFF_EVIDENCE_CHAIN,
        CATEGORY_FEATURE_LABEL_MATRIX_CHAIN, CATEGORY_SIGNAL_FEATURE_TARGET_CHAIN,
        CATEGORY_STRATEGY_CHARTER_CHAIN, CATEGORY_PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN,
        CATEGORY_IBKR_OR_BROKER_CHAIN,
    }
    return [
        _chain_summary(
            inventory, chain_id="EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH",
            chain_name="Expectancy Lab Predictive-Usefulness Path",
            predicate=lambda n: any(t in low(n) for t in ("expectancy-backtest-lab", "expectancy-lab-evidence")),
            chain_status="TERMINAL_ARCHIVED_NOT_READY", terminal_branch=TERMINAL_BRANCH,
            terminal_commit=EXPECTED_INVENTORY_BASE_COMMIT,
            source_digest=EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
            operator_action_required=False, recommended_next_action="NONE_FOR_CURRENT_ARCHIVED_PATH",
        ),
        _chain_summary(inventory, chain_id="VPA_WYCKOFF_RULE_BASELINE_CHAIN", chain_name="VPA/Wyckoff Rule Baseline Chain", predicate=lambda n: "vpa-wyckoff" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="FEATURE_LABEL_MATRIX_CHAIN", chain_name="Feature-Label Matrix Chain", predicate=lambda n: "feature-label-matrix" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="SIGNAL_FEATURE_GENERATION_CHAIN", chain_name="Signal/Feature Generation Chain", predicate=lambda n: "signal-or-feature-generation" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="OBJECTIVE_LABEL_TARGET_GENERATION_CHAIN", chain_name="Objective Label/Target Generation Chain", predicate=lambda n: "objective-label-or-target-generation" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="EXPECTANCY_OBJECTIVE_DESIGN_CHAIN", chain_name="Expectancy Objective Design Chain", predicate=lambda n: "expectancy-objective" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="STRATEGY_CHARTER_CHAIN", chain_name="Strategy Charter Chain", predicate=lambda n: "strategy-charter" in low(n), chain_status="COMPLETED_RESEARCH_ONLY"),
        _chain_summary(inventory, chain_id="PRIOR_IMPROVED_EVIDENCE_ARCHIVE_CHAIN", chain_name="Prior Improved Evidence Archive Chain", predicate=lambda n: "improved-evidence" in low(n) and "archive" in low(n), chain_status="TERMINAL_ARCHIVED_NOT_READY"),
        _chain_summary(inventory, chain_id="IBKR_BROKER_RELATED_BRANCHES", chain_name="IBKR / Broker-Related Branches", predicate=lambda n: "ibkr" in low(n) or "broker" in low(n), chain_status="PRESENT_REQUIRES_OPERATOR_REVIEW"),
        _chain_summary(
            inventory, chain_id="UNKNOWN_MISCELLANEOUS_BRANCHES",
            chain_name="Unknown / Miscellaneous Branches",
            predicate=lambda n: next(
                (row["category"] not in known_categories for row in inventory if row["ref_type"] == "LOCAL" and row["short_name"] == n),
                False,
            ),
            chain_status="PRESENT_REQUIRES_OPERATOR_REVIEW",
        ),
    ]


def _normalize_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "repo_root_name", "current_branch", "current_head_commit", "origin_main_commit",
        "main_commit_if_available", "working_tree_clean", "tracked_marketflow_files", "refs",
    }
    if not isinstance(snapshot, Mapping) or not required.issubset(snapshot):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("git snapshot is incomplete")
    normalized = deepcopy(dict(snapshot))
    if not isinstance(normalized["refs"], list) or not normalized["refs"]:
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("git snapshot refs are missing")
    normalized["refs"] = sorted(normalized["refs"], key=lambda row: row["ref_name"])
    return normalized


def _base_plan(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = _normalize_snapshot(snapshot)
    inventory = _classify_refs(snapshot)
    local_count = sum(row["ref_type"] == "LOCAL" for row in inventory)
    remote_count = sum(row["ref_type"] == "REMOTE" for row in inventory)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_V1,
        "artifact_status": MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY,
        "plan_scope": REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN,
        "created_offline": True, "research_only": True, "planning_only": True,
        "operator_review_required": True,
        "source_final_archive_artifact_kind": final_archive.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_final_archive_status": final_archive.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE,
        "source_final_archive_decision": final_archive.CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_acceptance_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        "source_feature_label_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12, "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "current_branch": snapshot["current_branch"],
        "current_head_commit": snapshot["current_head_commit"],
        "inventory_base_commit": EXPECTED_INVENTORY_BASE_COMMIT,
        "origin_main_commit": snapshot["origin_main_commit"],
        "main_commit_if_available": snapshot["main_commit_if_available"],
        "working_tree_clean": snapshot["working_tree_clean"],
        "main_modified": snapshot["main_commit_if_available"] != EXPECTED_ORIGIN_MAIN_COMMIT,
        "main_pushed": False, "origin_main_modified_by_this_task": False,
        "branch_inventory_created": True, "integration_plan_created": True,
        "merge_plan_created": False, "delete_plan_executed": False,
        "archive_plan_executed": False, "tag_plan_executed": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_tag_created": False, "git_main_push_performed": False,
        "git_force_push_performed": False, "git_remote_prune_performed": False,
        "provider_requests_made_in_inventory": False,
        "market_data_acquisition_performed_in_inventory": False,
        "dataset_generation_performed_in_inventory": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "final_archive_summary_created": True,
        "predictive_usefulness_chain_finalized": True,
        "current_expectancy_lab_evidence_path_finalized_archived_not_ready": True,
        "no_immediate_next_action_required_for_current_archived_path": True,
        "future_reopening_requires_new_operator_method_selection": True,
        "current_evidence_path_status": "FINALIZED_ARCHIVED_NOT_READY",
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "local_branch_count": local_count, "remote_branch_count": remote_count,
        "total_branch_ref_count": len(inventory),
        "tracked_marketflow_file_count": len(snapshot["tracked_marketflow_files"]),
        "tracked_marketflow_files": list(snapshot["tracked_marketflow_files"]),
        "branch_inventory": inventory,
        "branch_category_summary": _category_summary(inventory),
        "chain_summaries": _chain_summaries(inventory),
        "integration_phases": deepcopy(INTEGRATION_PHASES),
        "recommended_policy": "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG",
        "recommended_immediate_next_task": "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1",
        "main_protection": "ENABLED_BY_POLICY", "delete_protection": "ENABLED_BY_POLICY",
        "force_push_protection": "ENABLED_BY_POLICY",
        "runtime_authority": NOT_AUTHORIZED, "broker_authority": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check_values(plan: Mapping[str, Any]) -> dict[str, bool]:
    inventory = plan.get("branch_inventory", [])
    terminal = [row for row in inventory if isinstance(row, dict) and row.get("is_terminal_archive_branch")]
    return {
        "source_final_archive_digest_bound": plan.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": plan.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": plan.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": plan.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": plan.get("source_acceptance_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": plan.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": plan.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": plan.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": plan.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": plan.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "current_head_commit_bound": isinstance(plan.get("current_head_commit"), str) and len(plan["current_head_commit"]) == 40,
        "origin_main_commit_bound": plan.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "working_tree_clean_true": plan.get("working_tree_clean") is True,
        "branch_inventory_created_true": plan.get("branch_inventory_created") is True and isinstance(inventory, list) and bool(inventory),
        "integration_plan_created_true": plan.get("integration_plan_created") is True,
        "local_branch_count_recorded": plan.get("local_branch_count") == sum(row.get("ref_type") == "LOCAL" for row in inventory),
        "remote_branch_count_recorded": plan.get("remote_branch_count") == sum(row.get("ref_type") == "REMOTE" for row in inventory),
        "total_branch_ref_count_recorded": plan.get("total_branch_ref_count") == len(inventory),
        "current_branch_recorded": any(row.get("is_current_branch") and row.get("short_name") == plan.get("current_branch") for row in inventory),
        "terminal_expectancy_lab_branch_identified": bool(terminal),
        "origin_main_protected": any(row.get("is_origin_main") and row.get("suggested_disposition") == "PROTECT_DO_NOT_TOUCH" for row in inventory),
        "main_push_false": plan.get("git_main_push_performed") is False and plan.get("main_pushed") is False,
        "merge_performed_false": plan.get("git_merge_performed") is False,
        "rebase_performed_false": plan.get("git_rebase_performed") is False,
        "branch_delete_performed_false": plan.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": plan.get("git_remote_delete_performed") is False,
        "tag_created_false": plan.get("git_tag_created") is False,
        "force_push_false": plan.get("git_force_push_performed") is False,
        "remote_prune_false": plan.get("git_remote_prune_performed") is False,
        "marketflow_outputs_not_tracked": plan.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": plan.get("provider_requests_made_in_inventory") is False,
        "market_data_acquisition_false": plan.get("market_data_acquisition_performed_in_inventory") is False,
        "dataset_generation_false": plan.get("dataset_generation_performed_in_inventory") is False,
        "metric_recomputation_false": plan.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": plan.get("model_training_performed") is False,
        "strategy_scoring_false": plan.get("strategy_scoring_performed") is False,
        "recommendations_false": plan.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": plan.get("predictive_usefulness") == NOT_ACCEPTED and plan.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": plan.get("profitability") == NOT_ACCEPTED and plan.get("profitability_accepted") is False,
        "runtime_not_authorized": plan.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": plan.get("broker_execution") == NOT_AUTHORIZED,
        "risk_controls_defined": plan.get("risk_controls") == RISK_CONTROLS,
        "integration_phases_defined": plan.get("integration_phases") == INTEGRATION_PHASES,
        "recommended_policy_inventory_first": plan.get("recommended_policy") == "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG",
        "no_tracked_marketflow_files": plan.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL,
        "expected": True, "actual": actual, "severity": BLOCKER,
        "message": "repository inventory evidence matches" if actual else "repository inventory evidence mismatch",
    }


def _checklist(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(plan)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "branch_inventory_created": True, "integration_plan_created": True,
        "merge_performed": False, "delete_performed": False, "tag_created": False,
        "main_pushed": False, "origin_main_modified": False,
        "recommended_policy": "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG",
        "recommended_immediate_next_task": "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_state_branch_inventory_integration_plan_digest_v1(
    plan: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one repository snapshot plan."""
    payload = deepcopy(dict(plan))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_state_branch_inventory_integration_plan_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_state_branch_inventory_integration_plan_v1(
    *, repo_root: str | Path | None = None, git_snapshot: dict | None = None,
) -> dict:
    """Build a planning-only inventory from a supplied or read-only collected snapshot."""
    if git_snapshot is None:
        if repo_root is None:
            raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
                "repo_root is required when git_snapshot is not supplied"
            )
        git_snapshot = collect_marketflow_repository_git_snapshot_v1(repo_root)
    plan = _base_plan(git_snapshot)
    plan["checklist"] = _checklist(plan)
    plan["summary"] = _summary(plan["checklist"])
    plan["marketflow_repository_state_branch_inventory_integration_plan_digest"] = (
        marketflow_repository_state_branch_inventory_integration_plan_digest_v1(plan)
    )
    validate_marketflow_repository_state_branch_inventory_integration_plan_v1(plan)
    return plan


def validate_marketflow_repository_state_branch_inventory_integration_plan_v1(
    plan: dict,
) -> dict:
    """Validate repository bindings, inventory integrity, and non-execution gates."""
    if not isinstance(plan, dict):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("plan must be an object")
    expected_scalars = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_V1,
        "artifact_status": MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY,
        "plan_scope": REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "created_offline": True, "research_only": True, "planning_only": True,
        "operator_review_required": True, "working_tree_clean": True,
        "source_evidence": SOURCE_EVIDENCE,
        "target_universe": TARGET_UNIVERSE,
        "main_modified": False, "main_pushed": False,
        "origin_main_modified_by_this_task": False,
        "branch_inventory_created": True, "integration_plan_created": True,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_tag_created": False, "git_main_push_performed": False,
        "git_force_push_performed": False, "git_remote_prune_performed": False,
        "provider_requests_made_in_inventory": False,
        "market_data_acquisition_performed_in_inventory": False,
        "dataset_generation_performed_in_inventory": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "final_archive_summary_created": True,
        "predictive_usefulness_chain_finalized": True,
        "current_expectancy_lab_evidence_path_finalized_archived_not_ready": True,
        "no_immediate_next_action_required_for_current_archived_path": True,
        "future_reopening_requires_new_operator_method_selection": True,
        "current_evidence_path_status": "FINALIZED_ARCHIVED_NOT_READY",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": RISK_CONTROLS, "integration_phases": INTEGRATION_PHASES,
        "recommended_policy": "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG",
        "no_tracked_marketflow_files": True,
    }
    for field, expected in expected_scalars.items():
        if plan.get(field) != expected:
            raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(f"{field} mismatch")
    inventory = plan.get("branch_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("branch inventory missing")
    required_entry_fields = {
        "ref_name", "ref_type", "short_name", "commit_sha", "subject", "committer_date",
        "is_current_branch", "is_main", "is_origin_main", "is_terminal_archive_branch",
        "is_candidate_branch", "is_operator_review_branch", "is_approval_branch",
        "is_execution_branch", "is_results_review_branch", "is_reassessment_branch",
        "is_readiness_branch", "is_closure_branch", "is_selection_branch", "is_archive_branch",
        "is_final_summary_branch", "is_strategy_or_charter_branch",
        "is_marketflow_governance_branch", "is_ibkr_or_broker_branch",
        "is_unknown_category", "category", "suggested_disposition",
    }
    if any(not required_entry_fields.issubset(row) for row in inventory):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("branch inventory entry incomplete")
    for row in inventory:
        normalized = _normalized_branch_name(row["short_name"], row["ref_type"])
        expected_category = _category(normalized, row["ref_type"])
        if row["category"] != expected_category or row["suggested_disposition"] != _disposition(expected_category):
            raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("branch classification mismatch")
        if any(row.get(field) != value for field, value in _role_flags(normalized).items()):
            raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("branch role flags mismatch")
    if plan.get("branch_category_summary") != _category_summary(inventory):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("branch category summary mismatch")
    if plan.get("chain_summaries") != _chain_summaries(inventory):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("chain summaries mismatch")
    checklist = plan.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(plan):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("checklist failed")
    if plan.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("summary mismatch")
    digest = plan.get("marketflow_repository_state_branch_inventory_integration_plan_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("plan digest missing")
    if digest != marketflow_repository_state_branch_inventory_integration_plan_digest_v1(plan):
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError("plan digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_VALID,
        "artifact_kind": plan["artifact_kind"], "artifact_status": plan["artifact_status"],
        "marketflow_repository_state_branch_inventory_integration_plan_digest": digest,
        **{key: plan["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_state_branch_inventory_integration_plan_markdown_v1(
    plan: dict,
) -> str:
    """Render a sanitized Markdown view of the validated repository plan."""
    validation = validate_marketflow_repository_state_branch_inventory_integration_plan_v1(plan)
    protected = [row["short_name"] for row in plan["branch_inventory"] if row["suggested_disposition"] in {"PROTECT_DO_NOT_TOUCH", "KEEP_TERMINAL_EVIDENCE"}]
    review = [row["short_name"] for row in plan["branch_inventory"] if row["suggested_disposition"] in {"REQUIRES_OPERATOR_REVIEW", "UNKNOWN_DO_NOT_TOUCH"}]
    sections = [
        ("Title", ["MarketFlow Repository State, Branch Inventory, and Integration Plan v1"]),
        ("MarketFlow Repository State, Branch Inventory, and Integration Plan v1", [f"Artifact/status: `{plan['artifact_kind']}` / `{plan['artifact_status']}`.", f"Digest: `{validation['marketflow_repository_state_branch_inventory_integration_plan_digest']}`."]),
        ("Source Final Archive Summary", [f"`{plan['source_final_archive_artifact_kind']}` with digest `{plan['source_final_archive_digest']}`."]),
        ("Repository State", [f"Current branch/head: `{plan['current_branch']}` / `{plan['current_head_commit']}`.", f"`origin/main`: `{plan['origin_main_commit']}`; working tree clean: `{plan['working_tree_clean']}`."]),
        ("Branch Inventory Summary", [f"Local/remote/total refs: `{plan['local_branch_count']} / {plan['remote_branch_count']} / {plan['total_branch_ref_count']}`."]),
        ("Branch Category Summary", [f"`{row['category']}`: `{row['ref_count']}` refs (`{row['local_ref_count']}` local, `{row['remote_ref_count']}` remote)." for row in plan["branch_category_summary"]]),
        ("Terminal Evidence Chains", [f"`{row['chain_id']}`: `{row['chain_status']}`." for row in plan["chain_summaries"]]),
        ("Expectancy Lab Archive Chain", ["Terminal branch is preserved; the current archived path requires no immediate action and no merge readiness is inferred."]),
        ("Integration Plan", [f"Phase {row['phase_number']} `{row['phase_name']}`: `{row['status']}`." for row in plan["integration_phases"]]),
        ("Recommended Policy", [f"`{plan['recommended_policy']}`; next task `{plan['recommended_immediate_next_task']}`."]),
        ("Protected Branches", [f"`{name}`" for name in protected]),
        ("Branches Requiring Operator Review", [f"`{name}`" for name in review[:50]] or ["None identified."]),
        ("Future Cleanup Considerations", ["Any merge, tag, archive, or deletion requires a separate operator-reviewed and approved task."]),
        ("Risk Controls", plan["risk_controls"]),
        ("Authority Boundaries", ["Predictive usefulness and profitability remain not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{plan['summary']['total_checks']} / {plan['summary']['passed_checks']} / {plan['summary']['failed_checks']} / {plan['summary']['blocker_count']}`."]),
        ("Guardrails", ["No merge, rebase, deletion, tag, prune, main push, force push, provider, data, evidence, metric, training, scoring, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository State, Branch Inventory, and Integration Plan v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_state_branch_inventory_integration_plan_v1(
    output_dir: str | Path, *, repo_root: str | Path | None = None,
    git_snapshot: dict | None = None,
) -> dict:
    """Write canonical plan JSON without overwriting an existing inventory snapshot."""
    plan = build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        repo_root=repo_root, git_snapshot=git_snapshot
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_state_branch_inventory_integration_plan_v1.json"
    if path.exists():
        raise MarketFlowRepositoryStateBranchInventoryIntegrationPlanError(
            "repository inventory plan output already exists"
        )
    payload = canonical_json_bytes(plan)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": plan["artifact_kind"],
        "artifact_status": plan["artifact_status"],
        "marketflow_repository_state_branch_inventory_integration_plan_digest": plan["marketflow_repository_state_branch_inventory_integration_plan_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
