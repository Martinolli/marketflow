"""Review retry-failure classification-source candidates without selecting one."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_OUTPUT_CAPTURE_CANDIDATE_DIGEST = "fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
REVIEW_DISPOSITION = "REVIEWED_PLANNING_ONLY"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVAL_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
BLOCKER = "BLOCKER"

REVIEWED_PACKAGES = []
for package in source.SOURCE_PACKAGES:
    source_status = package["status"]
    if package["package_id"] == RECOMMENDED_PACKAGE:
        review_status = "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    elif source_status == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL":
        review_status = "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED"
    elif source_status == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED":
        review_status = "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
    elif source_status == "BLOCKED_NOT_SUFFICIENT":
        review_status = "REVIEWED_BLOCKED_NOT_SUFFICIENT"
    else:
        review_status = "REVIEWED_BLOCKED_NOT_ALLOWED"
    REVIEWED_PACKAGES.append(
        {
            "package_id": package["package_id"],
            "source_status": source_status,
            "review_status": review_status,
            "selected": False,
            "approved": False,
            "executed": False,
        }
    )

REVIEWED_FUTURE_OUTPUT_CAPTURE_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "requirement_value": requirement_value,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OUTPUT_CAPTURE",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id, requirement_value in source.FUTURE_OUTPUT_CAPTURE_REQUIREMENTS.items()
]
REVIEWED_FUTURE_OUTPUT_CAPTURE_PLAN = [
    {
        "step_id": f"step_{index:02d}",
        "source_step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_OUTPUT_CAPTURE_PLAN, start=1)
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": row["output_id"],
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for row in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.NON_GOALS
]
NEXT_CHAIN = [
    "Output Capture or Classification Source Approval v1, if selected.",
    "Output Capture or Classification Source Execution v1, if approved.",
    "Output Capture or Classification Source Results Review v1.",
    "Retry Failure Classification Method Reentry v1 or New Classification Method Candidate v2.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "output_capture_or_classification_source_approval_if_selected",
    "output_capture_or_classification_source_execution_if_approved",
    "output_capture_or_classification_source_results_review",
    "classification_method_reentry_after_output_capture",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_does_not_select_output_capture_package",
    "review_does_not_approve_output_capture",
    "review_does_not_execute_output_capture",
    "review_does_not_read_pytest_cache",
    "review_does_not_parse_operator_logs",
    "review_does_not_run_diagnostic_commands",
    "review_does_not_capture_output",
    "review_does_not_rerun_retry",
    "review_does_not_run_full_pytest",
    "review_does_not_treat_diagnostics_as_retry_evidence",
    "review_does_not_replace_failed_retry_result",
    "review_does_not_create_retry_results_review",
    "review_does_not_create_integration_results_review",
    "review_does_not_mark_integration_successful",
    "review_does_not_generate_successful_integration_execution_digest",
    "review_does_not_generate_successful_integration_validation_digest",
    "review_does_not_stage_additional_evidence",
    "review_does_not_modify_staged_evidence",
    "review_does_not_regenerate_evidence",
    "review_does_not_call_providers",
    "review_does_not_commit_marketflow_outputs",
    "review_does_not_push_integration_branch",
    "review_does_not_push_main",
    "review_does_not_delete_integration_branch",
    "review_does_not_delete_worktree",
    "review_does_not_force_push",
    "review_does_not_prune_remotes",
    "review_does_not_modify_tags",
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
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_approval_required_before_output_capture",
    "separate_results_review_required_after_output_capture",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_output_capture_candidate_digest_bound",
    "source_method_execution_digest_bound",
    "source_method_blocked_manifest_digest_bound",
    "source_method_approval_digest_bound",
    "source_method_operator_review_digest_bound",
    "source_method_candidate_digest_bound",
    "source_retry_failure_diagnosis_digest_bound",
    "source_staged_inventory_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "classification_blocked_reason_bound",
    "available_retry_data_bound",
    "missing_retry_data_bound",
    "origin_main_bound",
    "integration_branch_head_bound",
    "detached_worktree_head_bound",
    "staged_evidence_digest_bound",
    "review_created_true",
    "review_ready_true",
    "output_capture_packages_reviewed_true",
    "future_output_capture_requirements_reviewed_true",
    "future_output_capture_plan_reviewed_true",
    "planned_outputs_reviewed_true",
    "non_goals_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "source_packages_reviewed_8",
    "blocked_packages_reviewed_4",
    "output_capture_selected_false",
    "output_capture_approved_false",
    "output_capture_executed_false",
    "classification_source_generated_false",
    "classification_source_review_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_executed_false",
    "diagnostic_output_captured_false",
    "new_classification_method_candidate_created_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "integration_execution_successful_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
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
]


class MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(ValueError):
    """Raised when an operator-review record violates its source or authority boundary."""


def _source_candidate() -> dict[str, Any]:
    candidate = source.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1()
    fields = {
        "source_output_capture_candidate_artifact_kind": candidate["artifact_kind"],
        "source_output_capture_candidate_status": candidate["candidate_status"],
        "source_output_capture_candidate_scope": candidate["candidate_scope"],
        "source_output_capture_candidate_digest": SOURCE_OUTPUT_CAPTURE_CANDIDATE_DIGEST,
    }
    for name in (
        "source_method_execution_digest",
        "source_method_blocked_manifest_digest",
        "source_method_approval_digest",
        "source_method_operator_review_digest",
        "source_method_candidate_digest",
        "source_retry_failure_diagnosis_digest",
        "source_retry_approval_digest",
        "source_staged_inventory_digest",
        "retry_execution_branch",
        "retry_execution_commit",
        "retry_pytest_working_directory",
        "retry_pytest_ran_from_detached_worktree",
        "retry_pytest_first_result_authoritative",
        "retry_pytest_performed",
        "retry_pytest_exit_code",
        "retry_pytest_passed",
        "retry_pytest_failed",
        "retry_pytest_passed_count",
        "retry_pytest_failed_count",
        "retry_pytest_error_count",
        "retry_pytest_skipped_count",
        "available_retry_data",
        "missing_retry_data",
        "classification_source_available",
        "classification_blocked_reason",
        "root_full_regression_is_retry_evidence",
        "origin_main_commit",
        "integration_branch_name",
        "integration_branch_head_commit",
        "remote_integration_branch_exists",
        "detached_integration_worktree_path",
        "detached_integration_worktree_head_commit",
        "detached_integration_worktree_is_detached",
        "detached_integration_worktree_clean",
        "staged_evidence_manifest_digest",
        "staged_evidence_unchanged",
        "marketflow_outputs_tracked_in_repository",
        "marketflow_outputs_tracked_in_detached_worktree",
        "output_capture_candidate_created",
        "output_capture_candidate_ready_for_operator_review",
    ):
        fields[name] = deepcopy(candidate[name])
    return fields


def _base_review(source_candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **deepcopy(dict(source_candidate)),
        "reviewed_candidate_philosophy": source.CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": "Candidate-only reviewed; no output capture, diagnostic command, retry rerun, classification, results review, integration success, main merge, or runtime authority is created by this artifact.",
        "reviewed_candidate_goal": source.CANDIDATE_GOAL,
        "review_disposition": REVIEW_DISPOSITION,
        "reviewed_output_capture_or_classification_source_packages": deepcopy(REVIEWED_PACKAGES),
        "reviewed_future_output_capture_requirements": deepcopy(REVIEWED_FUTURE_OUTPUT_CAPTURE_REQUIREMENTS),
        "reviewed_future_output_capture_plan": deepcopy(REVIEWED_FUTURE_OUTPUT_CAPTURE_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "output_capture_candidate_operator_review_created": True,
        "output_capture_candidate_operator_review_ready": True,
        "output_capture_packages_reviewed": True,
        "future_output_capture_requirements_reviewed": True,
        "future_output_capture_plan_reviewed": True,
        "planned_outputs_reviewed": True,
        "non_goals_reviewed": True,
        "ready_for_output_capture_approval": False,
        "output_capture_method_selected": False,
        "output_capture_method_approved": False,
        "output_capture_method_authorized": False,
        "output_capture_method_executed": False,
        "classification_source_capture_executed": False,
        "classification_source_generated": False,
        "classification_source_review_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "new_classification_method_candidate_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
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
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": "The output-capture/classification-source candidate has been reviewed, but no package has been selected or approved by this review.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else "FAIL"
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    packages = review.get("reviewed_output_capture_or_classification_source_packages")
    package_rows = packages if isinstance(packages, list) else []
    recommended = next((row for row in package_rows if row.get("package_id") == RECOMMENDED_PACKAGE), None)
    blocked = [row for row in package_rows if str(row.get("source_status", "")).startswith("BLOCKED_")]
    values: dict[str, tuple[Any, Any]] = {
        "source_output_capture_candidate_digest_bound": (SOURCE_OUTPUT_CAPTURE_CANDIDATE_DIGEST, review.get("source_output_capture_candidate_digest")),
        "source_method_execution_digest_bound": (source.SOURCE_METHOD_EXECUTION_DIGEST, review.get("source_method_execution_digest")),
        "source_method_blocked_manifest_digest_bound": (source.SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST, review.get("source_method_blocked_manifest_digest")),
        "source_method_approval_digest_bound": (source.source.SOURCE_METHOD_APPROVAL_DIGEST, review.get("source_method_approval_digest")),
        "source_method_operator_review_digest_bound": (source.source.source.SOURCE_OPERATOR_REVIEW_DIGEST, review.get("source_method_operator_review_digest")),
        "source_method_candidate_digest_bound": (source.source.source.source.SOURCE_METHOD_CANDIDATE_DIGEST, review.get("source_method_candidate_digest")),
        "source_retry_failure_diagnosis_digest_bound": (source.source.source.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, review.get("source_retry_failure_diagnosis_digest")),
        "source_staged_inventory_digest_bound": ("06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0", review.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], counts),
        "classification_blocked_reason_bound": (source.source.CLASSIFICATION_BLOCKED_REASON, review.get("classification_blocked_reason")),
        "available_retry_data_bound": (source.source._available_retry_data(), review.get("available_retry_data")),
        "missing_retry_data_bound": (source.source.MISSING_RETRY_DATA, review.get("missing_retry_data")),
        "origin_main_bound": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", review.get("origin_main_commit")),
        "integration_branch_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", review.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", review.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": ("06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0", review.get("staged_evidence_manifest_digest")),
        "review_created_true": (True, review.get("output_capture_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("output_capture_candidate_operator_review_ready")),
        "output_capture_packages_reviewed_true": (True, review.get("output_capture_packages_reviewed")),
        "future_output_capture_requirements_reviewed_true": (True, review.get("future_output_capture_requirements_reviewed")),
        "future_output_capture_plan_reviewed_true": (True, review.get("future_output_capture_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_output_capture_approval")),
        "recommended_package_reviewed_not_selected": (["REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", False], [recommended.get("review_status") if recommended else None, recommended.get("selected") if recommended else None]),
        "source_packages_reviewed_8": (8, len(package_rows)),
        "blocked_packages_reviewed_4": (4, len(blocked)),
        "output_capture_selected_false": (False, review.get("output_capture_method_selected")),
        "output_capture_approved_false": (False, review.get("output_capture_method_approved")),
        "output_capture_executed_false": (False, review.get("output_capture_method_executed")),
        "classification_source_generated_false": (False, review.get("classification_source_generated")),
        "classification_source_review_created_false": (False, review.get("classification_source_review_created")),
        "retry_rerun_false": (False, review.get("retry_rerun_performed")),
        "full_pytest_false": (False, review.get("full_pytest_performed")),
        "diagnostic_command_executed_false": (False, review.get("diagnostic_command_executed")),
        "diagnostic_output_captured_false": (False, review.get("diagnostic_output_captured")),
        "new_classification_method_candidate_created_false": (False, review.get("new_classification_method_candidate_created")),
        "new_retry_candidate_created_false": (False, review.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, review.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, review.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, review.get("main_merge_approval_created")),
        "integration_execution_successful_false": (False, review.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
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
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "output_capture_candidate_operator_review_created": True,
        "output_capture_candidate_operator_review_ready": True,
        "output_capture_packages_reviewed": True,
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "ready_for_output_capture_approval": False,
        "output_capture_executed": False,
        "classification_source_generated": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "main_merge_approval_created": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build a review from committed candidate constants without selecting a package."""
    evidence = _source_candidate()
    if source_candidate is not None:
        if not isinstance(source_candidate, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
                "source_candidate must be an object"
            )
        evidence.update(deepcopy(source_candidate))
    review = _base_review(evidence)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review["checklist"])
    review["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"] = (
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings, reviewed states, and every closed boundary."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_source_candidate(),
        "reviewed_candidate_philosophy": source.CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": "Candidate-only reviewed; no output capture, diagnostic command, retry rerun, classification, results review, integration success, main merge, or runtime authority is created by this artifact.",
        "reviewed_candidate_goal": source.CANDIDATE_GOAL,
        "review_disposition": REVIEW_DISPOSITION,
        "reviewed_output_capture_or_classification_source_packages": REVIEWED_PACKAGES,
        "reviewed_future_output_capture_requirements": REVIEWED_FUTURE_OUTPUT_CAPTURE_REQUIREMENTS,
        "reviewed_future_output_capture_plan": REVIEWED_FUTURE_OUTPUT_CAPTURE_PLAN,
        "reviewed_planned_outputs": REVIEWED_PLANNED_OUTPUTS,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
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
        "output_capture_candidate_created",
        "output_capture_candidate_ready_for_operator_review",
        "output_capture_candidate_operator_review_created",
        "output_capture_candidate_operator_review_ready",
        "output_capture_packages_reviewed",
        "future_output_capture_requirements_reviewed",
        "future_output_capture_plan_reviewed",
        "planned_outputs_reviewed",
        "non_goals_reviewed",
        "staged_evidence_unchanged",
        "no_tracked_marketflow_files",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "root_full_regression_is_retry_evidence",
        "classification_source_available",
        "ready_for_output_capture_approval",
        "output_capture_method_selected",
        "output_capture_method_approved",
        "output_capture_method_authorized",
        "output_capture_method_executed",
        "classification_source_capture_executed",
        "classification_source_generated",
        "classification_source_review_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "new_classification_method_candidate_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
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
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            "checklist missing"
        )
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest_v1(review),
        "review digest",
    )
    return {
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated planning-only operator review."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(review)
    sections = [
        ("Source Output Capture Candidate", [f"Digest: `{review['source_output_capture_candidate_digest']}`."]),
        ("Source Method Execution", [f"Execution digest: `{review['source_method_execution_digest']}`.", f"Blocked manifest: `{review['source_method_blocked_manifest_digest']}`."]),
        ("Blocked Classification Context", [f"`{review['classification_blocked_reason']}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "Root regression is not retry evidence."]),
        ("Review Scope", [f"`{review['review_scope']}`."]),
        ("Reviewed Candidate Philosophy", [review["reviewed_candidate_philosophy"], review["reviewed_candidate_boundary"], review["reviewed_candidate_goal"]]),
        ("Reviewed Output Capture or Classification Source Packages", [f"`{row['package_id']}`: `{row['review_status']}`" for row in review["reviewed_output_capture_or_classification_source_packages"]]),
        ("Reviewed Future Output Capture Requirements", [f"`{row['requirement_id']}`: `{row['review_status']}` / `{row['execution_status']}`" for row in review["reviewed_future_output_capture_requirements"]]),
        ("Reviewed Future Output Capture Plan", [f"`{row['step_id']}`: `{row['review_status']}` / `{row['execution_status']}`" for row in review["reviewed_future_output_capture_plan"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_id']}`: `{row['review_status']}` / `{row['generation_status']}`" for row in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}`: `{row['review_status']}`" for row in review["reviewed_non_goals"]]),
        ("Recommendation", [f"Package: `{review['recommended_output_capture_or_classification_source_package']}` remains unselected.", f"Next task: `{review['recommended_next_task']}`."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No package selection, cache read, log parse, output capture, diagnostics, retry, results review, protected push, or runtime/trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Readiness for approval remains false.", "A separate selection and approval are required before execution."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
        source_candidate=source_candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError(
            "review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest": review[
            "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
