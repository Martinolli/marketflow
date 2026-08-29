"""Offline operator review of the integration validation remediation candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_candidate_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY = (
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "2d45ef960b45d6a81b6e494b77a44f3dba482567e973e83999844ce9ce351fc2"
)
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = source.EXPECTED_SOURCE_APPROVAL_DIGEST
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

REVIEWED_REMEDIATION_PHILOSOPHY = source.REMEDIATION_PHILOSOPHY
REVIEWED_REMEDIATION_BOUNDARY = (
    "Candidate-only reviewed; no evidence staging, copy, retry, pytest acceptance rerun, digest repair, source rerun, or results review is executed by this artifact."
)
REVIEWED_REMEDIATION_GOAL = source.REMEDIATION_GOAL
REVIEWED_PLANNING_ONLY = "REVIEWED_PLANNING_ONLY"

PACKAGE_REVIEW_STATUS_BY_SOURCE_STATUS = {
    source.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED: (
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    ),
    source.AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED: "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    source.BLOCKED_NOT_RECOMMENDED: "REVIEWED_BLOCKED_NOT_RECOMMENDED",
    source.BLOCKED_NOT_ALLOWED: "REVIEWED_BLOCKED_NOT_ALLOWED",
}


def _reviewed_packages() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package in source.REMEDIATION_PACKAGES:
        row = {
            "package_id": package["package_id"],
            "source_status": package["status"],
            "review_status": PACKAGE_REVIEW_STATUS_BY_SOURCE_STATUS[package["status"]],
            "purpose": package["purpose"],
            "selected": False,
            "approved": False,
            "executed": False,
        }
        for optional in ("recommended_for", "blocked_reason"):
            if optional in package:
                row[optional] = package[optional]
        rows.append(row)
    return rows


REVIEWED_REMEDIATION_PACKAGES = _reviewed_packages()
REVIEWED_REMEDIATION_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "source_value": source_value,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id, source_value in source.REMEDIATION_REQUIREMENTS.items()
]
REVIEWED_FUTURE_REMEDIATION_PLAN = [
    {
        "step_id": f"STEP_{index:02d}",
        "instruction": instruction,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, instruction in enumerate(source.FUTURE_REMEDIATION_EXECUTION_PLAN, start=1)
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.REMEDIATION_NON_GOALS
]
ROOT_CAUSE_QUESTION_REVIEW = {
    "answered_by_diagnosis": deepcopy(source.ROOT_CAUSE_QUESTION_STATUS["answered_by_diagnosis"]),
    "still_requires_remediation_execution_or_review": deepcopy(
        source.ROOT_CAUSE_QUESTION_STATUS["still_requires_remediation_execution_or_review"]
    ),
    "review_status": "REVIEWED_WITH_OPEN_ITEMS_FOR_FUTURE_REMEDIATION",
}

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_EXECUTION"
)
RECOMMENDATION_REASON = (
    "The remediation candidate has been reviewed, but no package has been selected or approved by this review."
)

NEXT_CHAIN = [
    "Remediation Approval v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1, only after remediation review.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "integration_failure_remediation_approval_if_selected",
    "integration_failure_remediation_execution_if_approved",
    "integration_failure_remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_select_remediation",
    "review_does_not_approve_remediation",
    "review_does_not_execute_remediation",
    "review_does_not_stage_evidence",
    "review_does_not_copy_marketflow_outputs",
    "review_does_not_retry_integration",
    "review_does_not_create_results_review",
    "review_does_not_mark_integration_successful",
    "review_does_not_generate_successful_execution_digest",
    "review_does_not_generate_successful_validation_digest",
    "review_does_not_delete_integration_branch",
    "review_does_not_reset_integration_branch",
    "review_does_not_push_integration_branch",
    "review_does_not_push_main",
    "review_does_not_merge_to_main",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_tags",
    "review_does_not_commit_marketflow_outputs",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_regenerate_dataset",
    "review_does_not_recompute_metrics",
    "review_does_not_train_models",
    "review_does_not_score_strategy",
    "review_does_not_generate_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_broker_execution",
    "first_failed_pytest_remains_authoritative",
    "later_wrong_worktree_rerun_remains_diagnostic_only",
    "blocked_digest_must_not_be_treated_as_ready",
    "separate_approval_required_before_remediation",
    "separate_retry_approval_required_before_integration_retry",
    "protect_origin_main",
    "preserve_integration_branch_for_diagnosis",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound",
    "source_diagnosis_digest_bound",
    "source_approval_digest_bound",
    "attempted_execution_commit_bound",
    "integration_branch_head_bound",
    "integration_base_commit_bound",
    "integration_source_commit_bound",
    "first_pytest_failure_preserved",
    "later_wrong_worktree_rerun_preserved_as_diagnostic_only",
    "representative_digest_mismatch_preserved",
    "missing_acquisition_manifest_recorded",
    "root_cause_recorded",
    "review_created_true",
    "review_ready_true",
    "remediation_packages_reviewed_true",
    "remediation_requirements_reviewed_true",
    "future_remediation_plan_reviewed_true",
    "root_cause_question_status_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "remediation_packages_reviewed_6",
    "blocked_packages_reviewed_2",
    "remediation_selected_false",
    "remediation_approved_false",
    "remediation_authorized_false",
    "remediation_executed_false",
    "retry_candidate_created_false",
    "retry_executed_false",
    "results_review_created_false",
    "integration_execution_successful_false",
    "successful_execution_digest_generated_false",
    "successful_validation_digest_generated_false",
    "integration_branch_pushed_false",
    "remote_integration_branch_false",
    "main_merge_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_not_tracked",
    "marketflow_outputs_not_committed",
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


class MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
    ValueError
):
    """Raised when the review or its review-only boundaries are invalid."""


def _source_candidate(source_candidate: dict | None) -> dict[str, Any]:
    candidate = (
        source.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1()
        if source_candidate is None
        else deepcopy(source_candidate)
    )
    validation = source.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
        candidate
    )
    if (
        validation[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"
        ]
        != EXPECTED_SOURCE_CANDIDATE_DIGEST
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "source remediation candidate digest mismatch"
        )
    return candidate


def _base_review(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        "source_remediation_candidate_artifact_kind": candidate["artifact_kind"],
        "source_remediation_candidate_status": candidate["candidate_status"],
        "source_remediation_candidate_scope": candidate["candidate_scope"],
        "source_remediation_candidate_digest": candidate[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"
        ],
        "source_failure_diagnosis_digest": candidate["source_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": candidate["source_merge_strategy_approval_digest"],
        **{
            key: candidate[key]
            for key in (
                "attempted_execution_branch",
                "attempted_execution_commit",
                "integration_branch_name",
                "integration_branch_head_commit",
                "integration_base_commit",
                "integration_source_commit",
                "first_integration_pytest_authoritative",
                "first_integration_pytest_passed",
                "first_integration_pytest_passed_count",
                "first_integration_pytest_failed_count",
                "first_integration_pytest_error_count",
                "first_integration_pytest_skipped_count",
                "later_isolated_rerun_passed",
                "later_isolated_rerun_passed_count",
                "later_isolated_rerun_skipped_count",
                "later_isolated_rerun_overrides_first_failure",
                "representative_failure_domain",
                "required_ready_digest_prefix",
                "actual_blocked_digest_prefix",
                "diagnosed_root_cause",
                "missing_required_file",
                "later_rerun_problem",
                "remediation_candidate_created",
                "remediation_candidate_ready_for_operator_review",
            )
        },
        "remediation_candidate_operator_review_created": True,
        "remediation_candidate_operator_review_ready": True,
        "remediation_packages_reviewed": True,
        "remediation_requirements_reviewed": True,
        "future_remediation_plan_reviewed": True,
        "root_cause_question_status_reviewed": True,
        "ready_for_remediation_approval": False,
        "remediation_selected": False,
        "remediation_approved": False,
        "remediation_authorized": False,
        "remediation_executed": False,
        "integration_retry_candidate_created": False,
        "integration_retry_approved": False,
        "integration_retry_executed": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_execution_digest_generated": False,
        "successful_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
        "marketflow_outputs_committed": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
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
        "reviewed_remediation_philosophy": REVIEWED_REMEDIATION_PHILOSOPHY,
        "reviewed_remediation_boundary": REVIEWED_REMEDIATION_BOUNDARY,
        "reviewed_remediation_goal": REVIEWED_REMEDIATION_GOAL,
        "reviewed_remediation_philosophy_status": REVIEWED_PLANNING_ONLY,
        "reviewed_remediation_packages": deepcopy(REVIEWED_REMEDIATION_PACKAGES),
        "reviewed_remediation_requirements": deepcopy(REVIEWED_REMEDIATION_REQUIREMENTS),
        "reviewed_future_remediation_plan": deepcopy(REVIEWED_FUTURE_REMEDIATION_PLAN),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "root_cause_question_review": deepcopy(ROOT_CAUSE_QUESTION_REVIEW),
        "recommended_remediation_package": source.PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "integration_retry_allowed_now": False,
        "integration_results_review_ready": False,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = actual == expected
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "Requirement satisfied." if passed else "Required review boundary mismatch.",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_remediation_packages", [])
    values = {
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_remediation_candidate_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, review.get("source_failure_diagnosis_digest")),
        "source_approval_digest_bound": (EXPECTED_SOURCE_APPROVAL_DIGEST, review.get("source_merge_strategy_approval_digest")),
        "attempted_execution_commit_bound": ("9d3dbc488747a0e17921bd4dcab7be2fadefc5ba", review.get("attempted_execution_commit")),
        "integration_branch_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", review.get("integration_branch_head_commit")),
        "integration_base_commit_bound": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", review.get("integration_base_commit")),
        "integration_source_commit_bound": ("71ed7fa63b27e1572fe7ccfd9b05f38b73a23416", review.get("integration_source_commit")),
        "first_pytest_failure_preserved": ([True, False, 24481, 1300, 500, 7], [review.get("first_integration_pytest_authoritative"), review.get("first_integration_pytest_passed"), review.get("first_integration_pytest_passed_count"), review.get("first_integration_pytest_failed_count"), review.get("first_integration_pytest_error_count"), review.get("first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved_as_diagnostic_only": ([True, False, "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE"], [review.get("later_isolated_rerun_passed"), review.get("later_isolated_rerun_overrides_first_failure"), review.get("later_rerun_problem")]),
        "representative_digest_mismatch_preserved": (["57c0a06e", "783e0013"], [review.get("required_ready_digest_prefix"), review.get("actual_blocked_digest_prefix")]),
        "missing_acquisition_manifest_recorded": ("acquisition_provider_evidence_run_manifest.json", review.get("missing_required_file")),
        "root_cause_recorded": ("DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT", review.get("diagnosed_root_cause")),
        "review_created_true": (True, review.get("remediation_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("remediation_candidate_operator_review_ready")),
        "remediation_packages_reviewed_true": (True, review.get("remediation_packages_reviewed")),
        "remediation_requirements_reviewed_true": (True, review.get("remediation_requirements_reviewed")),
        "future_remediation_plan_reviewed_true": (True, review.get("future_remediation_plan_reviewed")),
        "root_cause_question_status_reviewed_true": (True, review.get("root_cause_question_status_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_remediation_approval")),
        "recommended_package_reviewed_not_selected": (False, packages[0].get("selected") if packages else None),
        "remediation_packages_reviewed_6": (6, len(packages)),
        "blocked_packages_reviewed_2": (2, sum(row.get("review_status", "").startswith("REVIEWED_BLOCKED_") for row in packages)),
        "remediation_selected_false": (False, review.get("remediation_selected")),
        "remediation_approved_false": (False, review.get("remediation_approved")),
        "remediation_authorized_false": (False, review.get("remediation_authorized")),
        "remediation_executed_false": (False, review.get("remediation_executed")),
        "retry_candidate_created_false": (False, review.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, review.get("integration_retry_executed")),
        "results_review_created_false": (False, review.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "successful_execution_digest_generated_false": (False, review.get("successful_execution_digest_generated")),
        "successful_validation_digest_generated_false": (False, review.get("successful_validation_digest_generated")),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "remote_integration_branch_false": (False, review.get("remote_integration_branch_created")),
        "main_merge_false": (False, review.get("main_merge_performed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_not_tracked": (0, review.get("tracked_marketflow_file_count")),
        "marketflow_outputs_not_committed": (False, review.get("marketflow_outputs_committed")),
        "provider_requests_false": (False, review.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, review.get("market_data_acquisition_performed_in_review")),
        "dataset_generation_false": (False, review.get("dataset_generation_performed_in_review")),
        "metric_recomputation_false": (False, review.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, review.get("model_training_performed")),
        "strategy_scoring_false": (False, review.get("strategy_scoring_performed")),
        "recommendations_false": (False, review.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
        "non_goals_reviewed": (REVIEWED_NON_GOALS, review.get("reviewed_non_goals")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (True, review.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "remediation_candidate_operator_review_created": True,
        "remediation_candidate_operator_review_ready": True,
        "remediation_packages_reviewed": True,
        "recommended_remediation_package": source.PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "recommended_package_selected": False,
        "ready_for_remediation_approval": False,
        "remediation_executed": False,
        "integration_retry_allowed_now": False,
        "integration_results_review_ready": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic operator-review digest."""
    payload = deepcopy(dict(review))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the review offline without selecting or executing remediation."""
    review = _base_review(_source_candidate(source_candidate))
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review[
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
        review
    )
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact candidate bindings and all operator-review boundaries."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY,
        "source_remediation_candidate_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1,
        "source_remediation_candidate_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_remediation_candidate_scope": source.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY,
        "source_remediation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "attempted_execution_commit": "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "integration_base_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_source_commit": "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416",
        "representative_failure_domain": "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH",
        "required_ready_digest_prefix": "57c0a06e",
        "actual_blocked_digest_prefix": "783e0013",
        "diagnosed_root_cause": "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT",
        "missing_required_file": "acquisition_provider_evidence_run_manifest.json",
        "later_rerun_problem": "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE",
        "reviewed_remediation_philosophy": REVIEWED_REMEDIATION_PHILOSOPHY,
        "reviewed_remediation_boundary": REVIEWED_REMEDIATION_BOUNDARY,
        "reviewed_remediation_goal": REVIEWED_REMEDIATION_GOAL,
        "reviewed_remediation_philosophy_status": REVIEWED_PLANNING_ONLY,
        "reviewed_remediation_packages": REVIEWED_REMEDIATION_PACKAGES,
        "reviewed_remediation_requirements": REVIEWED_REMEDIATION_REQUIREMENTS,
        "reviewed_future_remediation_plan": REVIEWED_FUTURE_REMEDIATION_PLAN,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "root_cause_question_review": ROOT_CAUSE_QUESTION_REVIEW,
        "recommended_remediation_package": source.PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in static.items():
        _expect(review.get(field), expected, field)
    for field in (
        "attempted_execution_commit",
        "integration_branch_head_commit",
        "integration_base_commit",
        "integration_source_commit",
    ):
        if not re.fullmatch(r"[0-9a-f]{40}", str(review.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
                f"{field} invalid"
            )
    required_true = (
        "created_offline",
        "governance_only",
        "operator_review_only",
        "first_integration_pytest_authoritative",
        "later_isolated_rerun_passed",
        "remediation_candidate_created",
        "remediation_candidate_ready_for_operator_review",
        "remediation_candidate_operator_review_created",
        "remediation_candidate_operator_review_ready",
        "remediation_packages_reviewed",
        "remediation_requirements_reviewed",
        "future_remediation_plan_reviewed",
        "root_cause_question_status_reviewed",
        "no_tracked_marketflow_files",
    )
    required_false = (
        "first_integration_pytest_passed",
        "later_isolated_rerun_overrides_first_failure",
        "ready_for_remediation_approval",
        "remediation_selected",
        "remediation_approved",
        "remediation_authorized",
        "remediation_executed",
        "integration_retry_candidate_created",
        "integration_retry_approved",
        "integration_retry_executed",
        "integration_results_review_created",
        "integration_execution_successful",
        "successful_execution_digest_generated",
        "successful_validation_digest_generated",
        "integration_branch_pushed",
        "remote_integration_branch_created",
        "main_merge_performed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "integration_retry_allowed_now",
        "integration_results_review_ready",
    )
    for field in required_true:
        _expect(review.get(field), True, field)
    for field in required_false:
        _expect(review.get(field), False, field)
    _expect(review.get("tracked_marketflow_file_count"), 0, "tracked_marketflow_file_count")
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "operator-review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest_v1(
            review
        ),
        "operator-review digest",
    )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY,
        "artifact_kind": review["artifact_kind"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest": digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a validated, planning-only operator review."""
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
        review
    )
    sections = [
        ("Source Remediation Candidate", [f"Artifact/status/digest: `{review['source_remediation_candidate_artifact_kind']}` / `{review['source_remediation_candidate_status']}` / `{review['source_remediation_candidate_digest']}`."]),
        ("Failure Summary", ["The first integration pytest failure remains authoritative: `24481 passed, 1300 failed, 500 errors, 7 skipped`.", "The later passing rerun remains diagnostic-only."]),
        ("Root Cause Review", [f"`{review['diagnosed_root_cause']}`.", f"Missing manifest: `{review['missing_required_file']}`."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Reviewed Remediation Philosophy", [review["reviewed_remediation_philosophy"], review["reviewed_remediation_boundary"], review["reviewed_remediation_goal"]]),
        ("Reviewed Remediation Packages", [f"`{row['package_id']}`: `{row['source_status']}` -> `{row['review_status']}`; selected/approved/executed `{row['selected']} / {row['approved']} / {row['executed']}`." for row in review["reviewed_remediation_packages"]]),
        ("Reviewed Remediation Requirements", [f"`{row['requirement_id']}`: `{row['review_status']}` / `{row['execution_status']}`." for row in review["reviewed_remediation_requirements"]]),
        ("Reviewed Future Remediation Plan", [f"`{row['step_id']}`: {row['instruction']} (`{row['review_status']}`)." for row in review["reviewed_future_remediation_plan"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}`: `{row['review_status']}`." for row in review["reviewed_non_goals"]]),
        ("Root-Cause Question Review", [f"Status: `{review['root_cause_question_review']['review_status']}`."] + [f"Answered: {row}" for row in review["root_cause_question_review"]["answered_by_diagnosis"]] + [f"Open: {row}" for row in review["root_cause_question_review"]["still_requires_remediation_execution_or_review"]]),
        ("Recommendation", [f"Next task: `{review['recommended_next_task']}` / `{review['recommended_next_task_status']}`.", review["recommendation_reason"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No remediation is selected, approved, authorized, or executed. No integration retry or results review is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Separate selection and approval are required before remediation execution.", "The first failed pytest remains authoritative."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Validation Failure Remediation Candidate Operator Review v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1.json"
    )
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError(
            "operator-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest": validation[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
