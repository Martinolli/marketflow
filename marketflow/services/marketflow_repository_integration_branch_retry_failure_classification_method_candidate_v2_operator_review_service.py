"""Review classification method candidate v2 packages without selection or approval."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_CANDIDATE_V2_DIGEST = "0681e9f06cc45a18683055695d3a45750af87ba04cfad3afb21a07c818deccf4"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_CLASSIFICATION_METHOD_V2_EXECUTION"
)
RECOMMENDATION_REASON = (
    "Classification Method Candidate v2 has been reviewed, but no v2 package has been selected or "
    "approved by this review."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_CANDIDATE_V2_PHILOSOPHY = source.CANDIDATE_V2_PHILOSOPHY
REVIEWED_CANDIDATE_V2_BOUNDARY = (
    "Candidate-only reviewed; no classification execution, no cache read, no retry, no results review, "
    "no main merge, and no runtime authority are created by this artifact."
)
REVIEWED_CANDIDATE_V2_GOAL = source.CANDIDATE_V2_GOAL
PHILOSOPHY_REVIEW_STATUS = "REVIEWED_PLANNING_ONLY"


def _reviewed_packages() -> list[dict[str, Any]]:
    status_map = {
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL": "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED",
        "BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
    }
    return [
        {
            "package_id": package["package_id"],
            "source_status": package["status"],
            "review_status": status_map[package["status"]],
            "selected": False,
            "approved": False,
            "executed": False,
        }
        for package in source.PROPOSED_V2_PACKAGES
    ]


REVIEWED_V2_PACKAGES = _reviewed_packages()
REVIEWED_FUTURE_V2_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_V2_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS
]
REVIEWED_FUTURE_V2_EXECUTION_PLAN = [
    {
        "step_id": f"future_v2_execution_step_{index:02d}",
        "source_step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN, start=1)
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": output_id,
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for output_id in source.PLANNED_OUTPUT_NAMES
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal_id, "review_status": "REVIEWED_ACTIVE"}
    for non_goal_id in source.NON_GOALS
]

NEXT_CHAIN = [
    "Classification Method Approval v2, if selected.",
    "Classification Method Execution v2, if approved.",
    "Classification Method Results Review v2.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "classification_method_approval_v2_if_selected",
    "classification_method_execution_v2_if_approved",
    "classification_method_results_review_v2",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_v2_does_not_select_package",
    "review_v2_does_not_approve_package",
    "review_v2_does_not_execute_classification",
    "review_v2_does_not_read_cache",
    "review_v2_does_not_run_retry",
    "review_v2_does_not_run_full_pytest",
    "review_v2_does_not_run_diagnostic_commands",
    "review_v2_does_not_claim_failure_error_separation",
    "review_v2_does_not_claim_first_failure",
    "review_v2_does_not_claim_first_error",
    "review_v2_does_not_claim_traceback_root_cause",
    "review_v2_does_not_use_cache_as_retry_success_evidence",
    "review_v2_does_not_create_new_retry_candidate",
    "review_v2_does_not_create_retry_results_review",
    "review_v2_does_not_create_integration_results_review",
    "review_v2_does_not_mark_integration_successful",
    "review_v2_does_not_generate_successful_integration_digest",
    "review_v2_does_not_push_integration_branch",
    "review_v2_does_not_push_main",
    "review_v2_does_not_delete_integration_branch",
    "review_v2_does_not_delete_worktree",
    "review_v2_does_not_force_push",
    "review_v2_does_not_prune_remotes",
    "review_v2_does_not_modify_tags",
    "review_v2_does_not_commit_marketflow_outputs",
    "review_v2_does_not_commit_pytest_cache",
    "review_v2_does_not_modify_staged_evidence",
    "review_v2_does_not_regenerate_evidence",
    "review_v2_does_not_call_providers",
    "review_v2_does_not_acquire_market_data",
    "review_v2_does_not_regenerate_dataset",
    "review_v2_does_not_recompute_metrics",
    "review_v2_does_not_train_models",
    "review_v2_does_not_score_strategy",
    "review_v2_does_not_generate_recommendations",
    "review_v2_does_not_accept_predictive_usefulness",
    "review_v2_does_not_accept_profitability",
    "review_v2_does_not_authorize_runtime",
    "review_v2_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_v2_approval_required_before_execution",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_candidate_v2_digest_bound",
    "source_reentry_digest_bound",
    "source_results_review_digest_bound",
    "source_cache_manifest_digest_bound",
    "source_execution_digest_bound",
    "source_classification_manifest_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "cache_source_counts_bound",
    "module_summary_bound",
    "classification_source_limits_bound",
    "review_created_true",
    "review_ready_true",
    "v2_packages_reviewed_true",
    "future_v2_requirements_reviewed_true",
    "future_v2_execution_plan_reviewed_true",
    "planned_outputs_reviewed_true",
    "non_goals_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "v2_packages_reviewed_9",
    "blocked_packages_reviewed_4",
    "method_v2_selected_false",
    "method_v2_approved_false",
    "method_v2_authorized_false",
    "method_v2_executed_false",
    "classification_execution_created_false",
    "classification_execution_performed_false",
    "failure_modules_classified_false",
    "error_modules_classified_false",
    "first_failure_identified_false",
    "first_error_identified_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "pytest_cache_committed_false",
    "evidence_regenerated_false",
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
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
    ValueError
):
    """Raised when the operator review or its authority boundaries are invalid."""


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = expected == actual
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _committed_source_fields() -> dict[str, Any]:
    return {
        "source_classification_method_candidate_v2_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2,
        "source_classification_method_candidate_v2_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW,
        "source_classification_method_candidate_v2_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_classification_method_candidate_v2_digest": SOURCE_CANDIDATE_V2_DIGEST,
        **source._committed_source_fields(),
    }


def _source_fields(source_candidate: dict | None) -> dict[str, Any]:
    if source_candidate is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
        source_candidate
    )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_method_candidate_v2_artifact_kind": "artifact_kind",
        "source_classification_method_candidate_v2_status": "candidate_status",
        "source_classification_method_candidate_v2_scope": "candidate_scope",
        "source_classification_method_candidate_v2_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest",
    }
    for target, source_field in mapping.items():
        fields[target] = deepcopy(source_candidate.get(source_field))
    for field in set(fields) - set(mapping):
        if field in source_candidate:
            fields[field] = deepcopy(source_candidate[field])
    return fields


def _reviewed_package(review: Mapping[str, Any], package_id: str) -> Mapping[str, Any]:
    for package in review.get("reviewed_v2_packages", []):
        if package.get("package_id") == package_id:
            return package
    return {}


def _base_review(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **deepcopy(dict(source_fields)),
        "classification_source_valid_for_v2_candidate": True,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_accepted_for_module_level_only": True,
        "classification_source_not_accepted_for_failure_error_separation": True,
        "classification_source_not_accepted_for_first_order_failure_analysis": True,
        "classification_source_not_accepted_for_traceback_root_cause": True,
        "classification_source_not_retry_success_evidence": True,
        "classification_source_limitations": list(source.CLASSIFICATION_SOURCE_LIMITATIONS),
        "classification_method_candidate_v2_created": True,
        "classification_method_candidate_v2_ready_for_operator_review": True,
        "classification_method_candidate_v2_operator_review_created": True,
        "classification_method_candidate_v2_operator_review_ready": True,
        "classification_method_v2_packages_reviewed": True,
        "future_v2_requirements_reviewed": True,
        "future_v2_execution_plan_reviewed": True,
        "planned_outputs_reviewed": True,
        "non_goals_reviewed": True,
        "reviewed_candidate_v2_philosophy": REVIEWED_CANDIDATE_V2_PHILOSOPHY,
        "reviewed_candidate_v2_boundary": REVIEWED_CANDIDATE_V2_BOUNDARY,
        "reviewed_candidate_v2_goal": REVIEWED_CANDIDATE_V2_GOAL,
        "candidate_v2_philosophy_review_status": PHILOSOPHY_REVIEW_STATUS,
        "reviewed_v2_packages": deepcopy(REVIEWED_V2_PACKAGES),
        "reviewed_future_v2_requirements": deepcopy(REVIEWED_FUTURE_V2_REQUIREMENTS),
        "reviewed_future_v2_execution_plan": deepcopy(REVIEWED_FUTURE_V2_EXECUTION_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommended_classification_method_v2_package": source.RECOMMENDED_PACKAGE,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "ready_for_classification_method_v2_approval": False,
        "classification_method_v2_selected": False,
        "classification_method_v2_approved": False,
        "classification_method_v2_authorized": False,
        "classification_method_v2_executed": False,
        "classification_execution_created": False,
        "classification_execution_performed": False,
        "failure_modules_classified": False,
        "error_modules_classified": False,
        "first_failure_identified": False,
        "first_error_identified": False,
        "failure_error_separation_claimed": False,
        "first_order_failure_analysis_claimed": False,
        "traceback_root_cause_claimed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "integration_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
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
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_v2_packages", [])
    recommended = _reviewed_package(review, source.RECOMMENDED_PACKAGE)
    retry_counts = [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    values: dict[str, tuple[Any, Any]] = {
        "source_candidate_v2_digest_bound": (SOURCE_CANDIDATE_V2_DIGEST, review.get("source_classification_method_candidate_v2_digest")),
        "source_reentry_digest_bound": (source.SOURCE_REENTRY_DIGEST, review.get("source_classification_method_reentry_digest")),
        "source_results_review_digest_bound": (source.SOURCE_RESULTS_REVIEW_DIGEST, review.get("source_classification_source_results_review_digest")),
        "source_cache_manifest_digest_bound": (source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, review.get("source_cache_manifest_review_digest")),
        "source_execution_digest_bound": (source.SOURCE_EXECUTION_DIGEST, review.get("source_output_capture_execution_digest")),
        "source_classification_manifest_digest_bound": (source.SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST, review.get("source_classification_source_manifest_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], retry_counts),
        "cache_source_counts_bound": ([1404, 26288], [review.get("lastfailed_cache_entry_count"), review.get("nodeids_cache_entry_count")]),
        "module_summary_bound": ([29, [136, 131, 122, 112, 111]], [review.get("module_summary_module_count"), review.get("largest_module_nodeid_counts")]),
        "classification_source_limits_bound": (source.CLASSIFICATION_SOURCE_LIMITATIONS, review.get("classification_source_limitations")),
        "review_created_true": (True, review.get("classification_method_candidate_v2_operator_review_created")),
        "review_ready_true": (True, review.get("classification_method_candidate_v2_operator_review_ready")),
        "v2_packages_reviewed_true": (True, review.get("classification_method_v2_packages_reviewed")),
        "future_v2_requirements_reviewed_true": (True, review.get("future_v2_requirements_reviewed")),
        "future_v2_execution_plan_reviewed_true": (True, review.get("future_v2_execution_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_classification_method_v2_approval")),
        "recommended_package_reviewed_not_selected": (["REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", False, False, False], [recommended.get("review_status"), recommended.get("selected"), recommended.get("approved"), recommended.get("executed")]),
        "v2_packages_reviewed_9": (9, len(packages)),
        "blocked_packages_reviewed_4": (4, sum(row.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for row in packages)),
        "method_v2_selected_false": (False, review.get("classification_method_v2_selected")),
        "method_v2_approved_false": (False, review.get("classification_method_v2_approved")),
        "method_v2_authorized_false": (False, review.get("classification_method_v2_authorized")),
        "method_v2_executed_false": (False, review.get("classification_method_v2_executed")),
        "classification_execution_created_false": (False, review.get("classification_execution_created")),
        "classification_execution_performed_false": (False, review.get("classification_execution_performed")),
        "failure_modules_classified_false": (False, review.get("failure_modules_classified")),
        "error_modules_classified_false": (False, review.get("error_modules_classified")),
        "first_failure_identified_false": (False, review.get("first_failure_identified")),
        "first_error_identified_false": (False, review.get("first_error_identified")),
        "new_retry_candidate_created_false": (False, review.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, review.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, review.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, review.get("main_merge_approval_created")),
        "retry_rerun_false": (False, review.get("retry_rerun_performed")),
        "full_pytest_false": (False, review.get("full_pytest_performed")),
        "diagnostic_command_false": (False, review.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, review.get("diagnostic_output_captured")),
        "integration_success_false": (False, review.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, review.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
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
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (True, review.get("no_tracked_marketflow_files")),
        "no_tracked_pytest_cache_files": (True, review.get("no_tracked_pytest_cache_files")),
    }
    return [_record(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    recommended = _reviewed_package(review, source.RECOMMENDED_PACKAGE)
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "classification_method_candidate_v2_operator_review_created": review.get("classification_method_candidate_v2_operator_review_created"),
        "classification_method_candidate_v2_operator_review_ready": review.get("classification_method_candidate_v2_operator_review_ready"),
        "classification_method_v2_packages_reviewed": review.get("classification_method_v2_packages_reviewed"),
        "recommended_classification_method_v2_package": review.get("recommended_classification_method_v2_package"),
        "recommended_package_selected": recommended.get("selected"),
        "ready_for_classification_method_v2_approval": review.get("ready_for_classification_method_v2_approval"),
        "method_v2_executed": review.get("classification_method_v2_executed"),
        "classification_execution_performed": review.get("classification_execution_performed"),
        "new_retry_candidate_created": review.get("new_retry_candidate_created"),
        "new_retry_executed": review.get("new_retry_executed"),
        "integration_execution_successful": review.get("integration_execution_successful"),
        "recommended_next_task": review.get("recommended_next_task"),
        "predictive_usefulness_accepted": review.get("predictive_usefulness_accepted"),
        "profitability_accepted": review.get("profitability_accepted"),
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the offline operator review without reading cache or selecting a package."""
    review = _base_review(_source_fields(source_candidate))
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review[
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest"
    ] = marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
        review
    )
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
    review: dict,
) -> dict:
    """Validate review completeness and reject selection, approval, or execution."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_committed_source_fields(),
        "classification_source_limitations": source.CLASSIFICATION_SOURCE_LIMITATIONS,
        "reviewed_candidate_v2_philosophy": REVIEWED_CANDIDATE_V2_PHILOSOPHY,
        "reviewed_candidate_v2_boundary": REVIEWED_CANDIDATE_V2_BOUNDARY,
        "reviewed_candidate_v2_goal": REVIEWED_CANDIDATE_V2_GOAL,
        "candidate_v2_philosophy_review_status": PHILOSOPHY_REVIEW_STATUS,
        "reviewed_v2_packages": REVIEWED_V2_PACKAGES,
        "reviewed_future_v2_requirements": REVIEWED_FUTURE_V2_REQUIREMENTS,
        "reviewed_future_v2_execution_plan": REVIEWED_FUTURE_V2_EXECUTION_PLAN,
        "reviewed_planned_outputs": REVIEWED_PLANNED_OUTPUTS,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommended_classification_method_v2_package": source.RECOMMENDED_PACKAGE,
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
        "created_offline",
        "governance_only",
        "operator_review_only",
        "classification_source_valid_for_v2_candidate",
        "classification_source_accepted_for_module_level_only",
        "classification_source_not_accepted_for_failure_error_separation",
        "classification_source_not_accepted_for_first_order_failure_analysis",
        "classification_source_not_accepted_for_traceback_root_cause",
        "classification_source_not_retry_success_evidence",
        "classification_method_candidate_v2_created",
        "classification_method_candidate_v2_ready_for_operator_review",
        "classification_method_candidate_v2_operator_review_created",
        "classification_method_candidate_v2_operator_review_ready",
        "classification_method_v2_packages_reviewed",
        "future_v2_requirements_reviewed",
        "future_v2_execution_plan_reviewed",
        "planned_outputs_reviewed",
        "non_goals_reviewed",
        "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "ready_for_classification_method_v2_approval",
        "classification_method_v2_selected",
        "classification_method_v2_approved",
        "classification_method_v2_authorized",
        "classification_method_v2_executed",
        "classification_execution_created",
        "classification_execution_performed",
        "failure_modules_classified",
        "error_modules_classified",
        "first_failure_identified",
        "first_error_identified",
        "failure_error_separation_claimed",
        "first_order_failure_analysis_claimed",
        "traceback_root_cause_claimed",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    packages = review.get("reviewed_v2_packages")
    if not isinstance(packages, list) or len(packages) != 9:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "package review missing"
        )
    if any(row.get("selected") or row.get("approved") or row.get("executed") for row in packages):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "operator review selected, approved, or executed a package"
        )
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "checklist missing"
        )
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "review checklist failed"
        )
    _expect(review.get("summary"), _summary(review, checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "operator-review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest_v1(
            review
        ),
        "operator-review digest",
    )
    return {
        "artifact_kind": review["artifact_kind"],
        "status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest": digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review as Markdown."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
        review
    )
    sections = [
        ("Source Candidate v2", [f"Candidate digest: `{review['source_classification_method_candidate_v2_digest']}`."]),
        ("Source Reentry", [f"Reentry digest: `{review['source_classification_method_reentry_digest']}`."]),
        ("Source Classification-Source Review", [f"Results-review digest: `{review['source_classification_source_results_review_digest']}`.", f"Cache-manifest review digest: `{review['source_cache_manifest_review_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry remains `24877 passed, 1292 failed, 112 errors, 7 skipped`."]),
        ("Review Scope", [REVIEWED_CANDIDATE_V2_BOUNDARY]),
        ("Reviewed Candidate v2 Philosophy", [review["reviewed_candidate_v2_philosophy"], review["reviewed_candidate_v2_goal"], f"Status: `{review['candidate_v2_philosophy_review_status']}`."]),
        ("Reviewed v2 Packages", [f"`{row['package_id']}` - `{row['review_status']}`." for row in review["reviewed_v2_packages"]]),
        ("Reviewed Future v2 Requirements", [f"`{row['requirement_id']}` - `{row['review_status']}` / `{row['execution_status']}`." for row in review["reviewed_future_v2_requirements"]]),
        ("Reviewed Future v2 Execution Plan", [f"`{row['step_id']}` - `{row['review_status']}` / `{row['execution_status']}`." for row in review["reviewed_future_v2_execution_plan"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_id']}` - `{row['review_status']}` / `{row['generation_status']}`." for row in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}` - `{row['review_status']}`." for row in review["reviewed_non_goals"]]),
        ("Recommendation", [f"`{review['recommended_action']}`. Next task: `{review['recommended_next_task']}` with status `{review['recommended_next_task_status']}`. {review['recommendation_reason']}"]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No package is selected or approved; classification, retry, main merge, runtime, and trading remain closed."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The review uses committed source constants and does not read cache.", "Optional operator selection and separate approval are required before any v2 execution."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Classification Method Candidate v2 Operator Review v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
    output_dir: str | Path,
    *, source_candidate: dict | None = None,
) -> dict:
    """Write canonical operator-review JSON without overwriting existing output."""
    review = build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2OperatorReviewError(
            "operator-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
