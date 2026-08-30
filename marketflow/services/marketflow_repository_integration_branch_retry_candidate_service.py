"""Offline candidate for a future authoritative integration-branch retry."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_results_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1 = (
    "marketflow_repository_integration_branch_retry_candidate_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN"
)

EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = "b3f86722e05d7692805e51ca86f125df79099a10e0f4bb4d39ea9c824472ec67"
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST = "c34407c83c97c64ad49ecc736ee1595629f6bc19b7e5ecb7b65850e4cbdc8cb6"
EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST
EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST
EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST = source.EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST = source.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_MANIFEST_DIGEST = source.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_MANIFEST_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_INTEGRATION_BRANCH_NAME = source.EXPECTED_INTEGRATION_BRANCH_NAME
EXPECTED_INTEGRATION_HEAD_COMMIT = source.EXPECTED_INTEGRATION_HEAD_COMMIT
EXPECTED_DETACHED_WORKTREE_PATH = source.DEFAULT_INTEGRATION_WORKTREE_PATH
EXPECTED_SOURCE_EVIDENCE_ROOT = source.DEFAULT_SOURCE_EVIDENCE_ROOT
EXPECTED_STAGED_EVIDENCE_ROOT = source.DEFAULT_STAGED_EVIDENCE_ROOT
EXPECTED_REQUIRED_MANIFEST_PATH = EXPECTED_STAGED_EVIDENCE_ROOT / source.REQUIRED_MANIFEST_NAME
ATTEMPTED_EXECUTION_BRANCH = source.ATTEMPTED_EXECUTION_BRANCH
ATTEMPTED_EXECUTION_COMMIT = source.ATTEMPTED_EXECUTION_COMMIT

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED = "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
BLOCKED_NOT_ALLOWED = "BLOCKED_NOT_ALLOWED"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"

PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE = (
    "PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE"
)
PACKAGE_PRECHECK_THEN_FULL_PYTEST_RETRY_FROM_DETACHED_WORKTREE = (
    "PACKAGE_PRECHECK_THEN_FULL_PYTEST_RETRY_FROM_DETACHED_WORKTREE"
)
PACKAGE_TARGETED_ACQUISITION_REVIEW_TESTS_THEN_FULL_PYTEST_RETRY = (
    "PACKAGE_TARGETED_ACQUISITION_REVIEW_TESTS_THEN_FULL_PYTEST_RETRY"
)
PACKAGE_FULL_PYTEST_RETRY_WITH_CACHE_AND_ENVIRONMENT_GUARD = (
    "PACKAGE_FULL_PYTEST_RETRY_WITH_CACHE_AND_ENVIRONMENT_GUARD"
)
PACKAGE_ACCEPT_REMEDIATION_RESULTS_WITHOUT_INTEGRATION_RETRY = (
    "PACKAGE_ACCEPT_REMEDIATION_RESULTS_WITHOUT_INTEGRATION_RETRY"
)
PACKAGE_RETRY_FROM_FEATURE_WORKTREE_OR_ROOT_WORKTREE = (
    "PACKAGE_RETRY_FROM_FEATURE_WORKTREE_OR_ROOT_WORKTREE"
)

RETRY_CANDIDATE_PHILOSOPHY = (
    "The integration retry must be an authoritative first retry executed from the remediated detached integration worktree, with the staged frozen evidence verified before execution, no regeneration, no provider calls, and no wrong-worktree acceptance."
)
RETRY_CANDIDATE_BOUNDARY = (
    "Candidate-only; no retry, approval, results review, success digest, main merge, or runtime authority is created by this artifact."
)
RETRY_CANDIDATE_GOAL = (
    "Prepare a controlled future retry path that tests the actual integration branch content with the restored detached worktree and staged frozen evidence."
)

RETRY_PACKAGES = [
    {
        "package_id": PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE,
        "status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Run the full pytest suite from the remediated detached integration worktree as the authoritative integration retry, after verifying staged frozen evidence and working directory guards.",
        "recommended_for": "Validating the actual integration branch content after the missing evidence-root remediation was completed and reviewed.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_PRECHECK_THEN_FULL_PYTEST_RETRY_FROM_DETACHED_WORKTREE,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Run a strict precheck package first, then full pytest from the detached worktree in the same approved retry execution.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_TARGETED_ACQUISITION_REVIEW_TESTS_THEN_FULL_PYTEST_RETRY,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Run targeted acquisition-review tests before full pytest, preserving full pytest as the only retry acceptance gate.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_FULL_PYTEST_RETRY_WITH_CACHE_AND_ENVIRONMENT_GUARD,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Run the full pytest retry from the detached worktree with explicit cache/env isolation and recorded environment snapshot.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_ACCEPT_REMEDIATION_RESULTS_WITHOUT_INTEGRATION_RETRY,
        "status": BLOCKED_NOT_ALLOWED,
        "purpose": "Treat the remediation results review as enough to unblock integration without running a retry.",
        "blocked_reason": "Remediation only staged missing evidence; it did not validate the full integrated stack.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_RETRY_FROM_FEATURE_WORKTREE_OR_ROOT_WORKTREE,
        "status": BLOCKED_NOT_ALLOWED,
        "purpose": "Run retry from the feature/root worktree instead of the detached integration worktree.",
        "blocked_reason": "The previous wrong-worktree rerun was explicitly classified as diagnostic-only and not acceptance evidence.",
        "selected": False, "approved": False, "executed": False,
    },
]

FUTURE_RETRY_REQUIREMENTS = {
    "source_remediation_results_review_must_be_ready": True,
    "detached_worktree_must_exist": True,
    "detached_worktree_head_must_equal_220fbc220365fce9cae13ab4853cddff118c0187": True,
    "detached_worktree_must_be_clean_before_retry": True,
    "detached_worktree_must_be_detached": True,
    "remote_integration_branch_must_remain_absent": True,
    "origin_main_must_remain_unchanged": True,
    "staged_evidence_root_must_exist": True,
    "staged_required_manifest_must_exist": True,
    "staged_evidence_must_remain_untracked": True,
    "source_and_staged_evidence_digest_must_match_06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0": True,
    "pytest_must_run_from_detached_integration_worktree": True,
    "wrong_worktree_retry_must_fail_closed": True,
    "full_pytest_required": True,
    "first_retry_result_is_authoritative": True,
    "later_retry_rerun_cannot_override_first_failed_retry": True,
    "retry_results_review_required_after_execution": True,
    "main_merge_requires_separate_approval_after_retry_review": True,
}
FUTURE_RETRY_EXECUTION_PLAN = [
    "Verify source remediation results-review digest and evidence-manifest review digest.",
    f"Verify detached worktree exists, is detached, and points to {EXPECTED_INTEGRATION_HEAD_COMMIT}.",
    "Verify origin/main remains unchanged.",
    "Verify remote integration branch remains absent.",
    "Verify staged evidence root and acquisition manifest exist in detached worktree.",
    "Verify staged evidence remains untracked.",
    f"Verify source/staged evidence digest remains {EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST}.",
    f"Run full pytest from {EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)}.",
    "Record command, working directory, exit code, pass/fail/skip counts, and duration.",
    "If the first retry fails, fail closed and do not create successful integration evidence.",
    "If the first retry passes, create retry execution artifact only; retry results review remains separate.",
    "Do not push integration branch or main.",
]
RETRY_NON_GOALS = [
    "do_not_retry_now", "do_not_run_pytest_now", "do_not_create_retry_approval_now",
    "do_not_create_retry_execution_now", "do_not_create_retry_results_review_now",
    "do_not_mark_integration_successful_now", "do_not_generate_successful_integration_digest_now",
    "do_not_stage_additional_evidence_now", "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_commit_marketflow_outputs",
    "do_not_push_integration_branch", "do_not_push_main",
    "do_not_delete_or_reset_integration_branch", "do_not_delete_worktree",
    "do_not_force_push", "do_not_modify_tags", "do_not_accept_wrong_worktree_retry",
    "do_not_accept_predictive_usefulness", "do_not_accept_profitability",
    "do_not_authorize_runtime", "do_not_authorize_trading",
]
NEXT_CHAIN = [
    "Integration Branch Retry Candidate Operator Review v1.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval v1, only if retry results review passes.",
    "Main Merge Execution v1, only if separately approved.",
    "Branch Cleanup Candidate v1, only after merge strategy is settled.",
]
NEXT_GATES = [
    "integration_branch_retry_candidate_operator_review",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
    "main_merge_execution_if_approved",
    "branch_cleanup_candidate_after_merge_strategy",
]
RISK_CONTROLS = [
    "candidate_does_not_run_retry", "candidate_does_not_run_pytest",
    "candidate_does_not_create_retry_approval", "candidate_does_not_create_retry_execution",
    "candidate_does_not_create_retry_results_review", "candidate_does_not_mark_integration_successful",
    "candidate_does_not_generate_successful_integration_execution_digest",
    "candidate_does_not_generate_successful_integration_validation_digest",
    "candidate_does_not_stage_additional_evidence", "candidate_does_not_modify_staged_evidence",
    "candidate_does_not_regenerate_evidence", "candidate_does_not_call_providers",
    "candidate_does_not_commit_marketflow_outputs", "candidate_does_not_push_integration_branch",
    "candidate_does_not_push_main", "candidate_does_not_delete_integration_branch",
    "candidate_does_not_delete_worktree", "candidate_does_not_force_push",
    "candidate_does_not_prune_remotes", "candidate_does_not_modify_tags",
    "candidate_does_not_acquire_market_data", "candidate_does_not_regenerate_dataset",
    "candidate_does_not_recompute_metrics", "candidate_does_not_train_models",
    "candidate_does_not_score_strategy", "candidate_does_not_generate_recommendations",
    "candidate_does_not_accept_predictive_usefulness", "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime", "candidate_does_not_authorize_broker_execution",
    "staged_frozen_evidence_must_remain_untracked", "wrong_worktree_retry_must_fail_closed",
    "separate_operator_review_required", "separate_approval_required_before_retry",
    "separate_results_review_required_after_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1"

REQUIRED_CHECK_IDS = [
    "source_remediation_results_review_digest_bound",
    "source_remediation_results_review_evidence_manifest_digest_bound",
    "source_remediation_execution_digest_bound", "source_remediation_execution_evidence_manifest_digest_bound",
    "source_staged_inventory_digest_bound", "source_worktree_restoration_results_review_digest_bound",
    "source_remediation_approval_digest_bound", "source_diagnosis_digest_bound",
    "attempted_execution_commit_bound", "origin_main_at_review_bound",
    "integration_branch_head_bound", "detached_worktree_path_bound", "detached_worktree_head_bound",
    "detached_worktree_clean_recorded", "staged_evidence_root_bound", "staged_manifest_bound",
    "source_staged_digest_match_bound", "candidate_created_true", "candidate_ready_true",
    "recommended_retry_package_present", "retry_packages_present_6", "blocked_retry_packages_present_2",
    "recommended_package_not_selected", "retry_selected_false", "retry_approved_false",
    "retry_authorized_false", "retry_executed_false", "retry_results_review_created_false",
    "integration_results_review_created_false", "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "remote_integration_branch_created_false", "main_push_false", "origin_main_modified_false",
    "marketflow_outputs_committed_false", "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "future_retry_requirements_defined", "future_retry_plan_defined",
    "retry_non_goals_defined", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryCandidateError(ValueError):
    """Raised when retry-candidate evidence or boundaries are invalid."""


def _source_review(source_review: dict | None) -> dict[str, Any]:
    if source_review is not None:
        source.validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
            source_review
        )
        return {
            "source_remediation_results_review_digest": source_review[
                "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest"
            ],
            "source_remediation_results_review_evidence_manifest_digest": source_review[
                "marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest"
            ],
        }
    return {
        "source_remediation_results_review_digest": EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
        "source_remediation_results_review_evidence_manifest_digest": EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST,
    }


def _base_candidate(review: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        **deepcopy(dict(review)),
        "source_remediation_execution_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "source_remediation_execution_evidence_manifest_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST,
        "source_staged_inventory_digest": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "source_worktree_restoration_results_review_digest": EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST,
        "source_worktree_restoration_results_review_manifest_digest": EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
        "source_remediation_operator_review_digest": EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "attempted_execution_branch": ATTEMPTED_EXECUTION_BRANCH,
        "attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
        "original_blocked_artifact": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED",
        "original_blocked_status": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED",
        "first_integration_pytest_result": "24481 passed, 1300 failed, 500 errors, 7 skipped",
        "later_wrong_worktree_rerun_result": "26842 passed, 7 skipped",
        "later_wrong_worktree_rerun_status": "DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        "diagnosed_root_cause": "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT",
        "selected_remediation_package": "PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE",
        "origin_main_commit_at_review": EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_name": EXPECTED_INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_at_review": EXPECTED_INTEGRATION_HEAD_COMMIT,
        "integration_branch_matches_required_head_at_review": True,
        "remote_integration_branch_exists_at_review": False,
        "detached_integration_worktree_path": str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)),
        "detached_integration_worktree_exists_at_review": True,
        "detached_integration_worktree_head_commit_at_review": EXPECTED_INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_head_verified_at_review": True,
        "detached_integration_worktree_is_detached_at_review": True,
        "detached_integration_worktree_clean_at_review": True,
        "source_evidence_root_path": str(EXPECTED_SOURCE_EVIDENCE_ROOT.resolve(strict=False)),
        "staged_evidence_root_path": str(EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False)),
        "staged_required_manifest_path": str(EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False)),
        "source_evidence_file_count_at_review": 7,
        "staged_evidence_file_count_at_review": 7,
        "source_evidence_total_bytes_at_review": 2458181,
        "staged_evidence_total_bytes_at_review": 2458181,
        "source_evidence_manifest_digest_at_review": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "staged_evidence_manifest_digest_at_review": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "source_and_staged_evidence_match_at_review": True,
        "staged_evidence_root_untracked_at_review": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "retry_candidate_philosophy": RETRY_CANDIDATE_PHILOSOPHY,
        "retry_candidate_boundary": RETRY_CANDIDATE_BOUNDARY,
        "retry_candidate_goal": RETRY_CANDIDATE_GOAL,
        "retry_packages": deepcopy(RETRY_PACKAGES),
        "recommended_integration_branch_retry_package": PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE,
        "recommendation_status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "recommendation_reason": "The remediation results review verified that the detached integration worktree now contains matching staged frozen evidence. The next valid integration evidence requires an authoritative retry from that exact detached worktree.",
        "future_retry_requirements": deepcopy(FUTURE_RETRY_REQUIREMENTS),
        "future_retry_execution_plan": list(FUTURE_RETRY_EXECUTION_PLAN),
        "future_retry_execution_plan_status": PLANNED_NOT_EXECUTED,
        "retry_non_goals": list(RETRY_NON_GOALS),
        "integration_branch_retry_candidate_created": True,
        "integration_branch_retry_candidate_ready_for_operator_review": True,
        "ready_for_integration_branch_retry_candidate_operator_review": True,
        "integration_branch_retry_selected": False,
        "integration_branch_retry_approved": False,
        "integration_branch_retry_authorized": False,
        "integration_branch_retry_executed": False,
        "integration_branch_retry_results_review_created": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = candidate.get("retry_packages") or []
    recommended = next(
        (row for row in packages if row.get("package_id") == PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE),
        {},
    )
    blocked = [row for row in packages if row.get("status") == BLOCKED_NOT_ALLOWED]
    values: dict[str, tuple[Any, Any]] = {
        "source_remediation_results_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, candidate.get("source_remediation_results_review_digest")),
        "source_remediation_results_review_evidence_manifest_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST, candidate.get("source_remediation_results_review_evidence_manifest_digest")),
        "source_remediation_execution_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, candidate.get("source_remediation_execution_digest")),
        "source_remediation_execution_evidence_manifest_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST, candidate.get("source_remediation_execution_evidence_manifest_digest")),
        "source_staged_inventory_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, candidate.get("source_staged_inventory_digest")),
        "source_worktree_restoration_results_review_digest_bound": (EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST, candidate.get("source_worktree_restoration_results_review_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, candidate.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST, candidate.get("source_failure_diagnosis_digest")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, candidate.get("attempted_execution_commit")),
        "origin_main_at_review_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, candidate.get("origin_main_commit_at_review")),
        "integration_branch_head_bound": (EXPECTED_INTEGRATION_HEAD_COMMIT, candidate.get("integration_branch_head_commit_at_review")),
        "detached_worktree_path_bound": (str(EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)), candidate.get("detached_integration_worktree_path")),
        "detached_worktree_head_bound": (EXPECTED_INTEGRATION_HEAD_COMMIT, candidate.get("detached_integration_worktree_head_commit_at_review")),
        "detached_worktree_clean_recorded": (True, candidate.get("detached_integration_worktree_clean_at_review")),
        "staged_evidence_root_bound": (str(EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False)), candidate.get("staged_evidence_root_path")),
        "staged_manifest_bound": (str(EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False)), candidate.get("staged_required_manifest_path")),
        "source_staged_digest_match_bound": (True, candidate.get("source_and_staged_evidence_match_at_review")),
        "candidate_created_true": (True, candidate.get("integration_branch_retry_candidate_created")),
        "candidate_ready_true": (True, candidate.get("integration_branch_retry_candidate_ready_for_operator_review")),
        "recommended_retry_package_present": (PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE, candidate.get("recommended_integration_branch_retry_package")),
        "retry_packages_present_6": (6, len(packages)),
        "blocked_retry_packages_present_2": (2, len(blocked)),
        "recommended_package_not_selected": (False, recommended.get("selected")),
        "retry_selected_false": (False, candidate.get("integration_branch_retry_selected")),
        "retry_approved_false": (False, candidate.get("integration_branch_retry_approved")),
        "retry_authorized_false": (False, candidate.get("integration_branch_retry_authorized")),
        "retry_executed_false": (False, candidate.get("integration_branch_retry_executed")),
        "retry_results_review_created_false": (False, candidate.get("integration_branch_retry_results_review_created")),
        "integration_results_review_created_false": (False, candidate.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, candidate.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, candidate.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, candidate.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, candidate.get("remote_integration_branch_created")),
        "main_push_false": (False, candidate.get("main_push_performed")),
        "origin_main_modified_false": (False, candidate.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, candidate.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, candidate.get("evidence_regenerated")),
        "provider_requests_false": (False, candidate.get("provider_requests_made_in_candidate")),
        "market_data_acquisition_false": (False, candidate.get("market_data_acquisition_performed_in_candidate")),
        "dataset_generation_false": (False, candidate.get("dataset_generation_performed_in_candidate")),
        "metric_recomputation_false": (False, candidate.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, candidate.get("model_training_performed")),
        "strategy_scoring_false": (False, candidate.get("strategy_scoring_performed")),
        "recommendations_false": (False, candidate.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "future_retry_requirements_defined": (FUTURE_RETRY_REQUIREMENTS, candidate.get("future_retry_requirements")),
        "future_retry_plan_defined": (FUTURE_RETRY_EXECUTION_PLAN, candidate.get("future_retry_execution_plan")),
        "retry_non_goals_defined": (RETRY_NON_GOALS, candidate.get("retry_non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "integration_branch_retry_candidate_created": True,
        "integration_branch_retry_candidate_ready_for_operator_review": True,
        "recommended_integration_branch_retry_package": PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE,
        "retry_selected": False, "retry_approved": False, "retry_executed": False,
        "retry_results_review_created": False, "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_retry_candidate_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_candidate_v1(
    *, source_review: dict | None = None,
) -> dict:
    """Build the candidate offline from committed constants or a valid source review."""
    candidate = _base_candidate(_source_review(source_review))
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_retry_candidate_digest"] = (
        marketflow_repository_integration_branch_retry_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_integration_branch_retry_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate the candidate and all non-authorizing boundaries."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate must be an object")
    expected = _base_candidate(_source_review(None))
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryCandidateError(f"{field} mismatch")
    checklist = candidate.get("checklist")
    if checklist != _checklist(candidate) or any(row.get("status") != PASS for row in checklist or []):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate checklist mismatch or failed")
    if candidate.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate summary mismatch")
    digest = candidate.get("marketflow_repository_integration_branch_retry_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate digest missing")
    if digest != marketflow_repository_integration_branch_retry_candidate_digest_v1(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate digest mismatch")
    return {
        "status": candidate["candidate_status"], "artifact_kind": candidate["artifact_kind"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_candidate_digest": digest,
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated retry candidate."""
    validation = validate_marketflow_repository_integration_branch_retry_candidate_v1(candidate)
    sections = [
        ("Source Remediation Results Review", [f"Digest: `{candidate['source_remediation_results_review_digest']}`; evidence digest: `{candidate['source_remediation_results_review_evidence_manifest_digest']}`."]),
        ("Failure Context", ["The first failed integration pytest remains authoritative; the later wrong-worktree run remains diagnostic only."]),
        ("Remediation Context", ["The detached integration worktree contains reviewed matching frozen ignored evidence."]),
        ("Candidate Scope", [f"`{candidate['candidate_scope']}`."]),
        ("Retry Philosophy", [candidate["retry_candidate_philosophy"], candidate["retry_candidate_boundary"], candidate["retry_candidate_goal"]]),
        ("Proposed Retry Packages", [f"`{row['package_id']}`: `{row['status']}`." for row in candidate["retry_packages"]]),
        ("Recommended Retry Package", [f"`{candidate['recommended_integration_branch_retry_package']}` remains unselected."]),
        ("Future Retry Requirements", [f"`{key}`: `{value}`" for key, value in candidate["future_retry_requirements"].items()]),
        ("Future Retry Execution Plan", candidate["future_retry_execution_plan"]),
        ("Retry Non-Goals", [f"`{row}`" for row in candidate["retry_non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No approval, retry, results review, integration success, push, acceptance, runtime, or broker authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["A separate operator review and approval are required before any authoritative retry."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_candidate_v1(
    output_dir: str | Path,
    *, source_review: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_retry_candidate_v1(
        source_review=source_review
    )
    validation = validate_marketflow_repository_integration_branch_retry_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryCandidateError("candidate output already exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "sha256": hashlib.sha256(payload).hexdigest(), **validation,
    }
