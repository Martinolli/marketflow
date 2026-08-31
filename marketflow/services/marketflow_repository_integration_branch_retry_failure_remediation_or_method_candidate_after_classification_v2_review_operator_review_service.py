"""Review the after-v2 remediation/method candidate without selecting a package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SOURCE_AFTER_V2_CANDIDATE_DIGEST = "c6e22aec87122675e9eb2ccf62af7e72756c471ebec81d89cabe1d800633d5e4"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_CLASSIFICATION_V2_REVIEW_V1_IF_SELECTED"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = (
    "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_AFTER_V2_REMEDIATION_OR_METHOD_EXECUTION"
)
RECOMMENDATION_REASON = (
    "The after-v2 remediation/method candidate has been reviewed, but no package has been selected or approved "
    "by this review."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_CANDIDATE_PHILOSOPHY = source.CANDIDATE_AFTER_V2_PHILOSOPHY
REVIEWED_CANDIDATE_BOUNDARY = (
    "Candidate-only reviewed; no remediation, diagnostic execution, classification execution, retry, results "
    "review, main merge, or runtime authority is created by this artifact."
)
REVIEWED_CANDIDATE_GOAL = source.CANDIDATE_AFTER_V2_GOAL
REVIEWED_CANDIDATE_PHILOSOPHY_STATUS = "REVIEWED_PLANNING_ONLY"


def _review_status_for_package(package: Mapping[str, Any]) -> str:
    status = package["status"]
    if package["package_id"] == source.RECOMMENDED_PACKAGE:
        return "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    if status == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL":
        return "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED"
    if status == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED":
        return "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
    return "REVIEWED_BLOCKED_NOT_ALLOWED"


REVIEWED_PACKAGES = [
    {
        "package_id": package["package_id"],
        "source_status": package["status"],
        "review_status": _review_status_for_package(package),
        "selected": False,
        "approved": False,
        "executed": False,
    }
    for package in source.PROPOSED_PACKAGES
]
REVIEWED_FUTURE_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_AFTER_V2_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_REQUIREMENTS
]
REVIEWED_FUTURE_PLAN = [
    {
        "step_id": f"future_plan_step_{index:02d}",
        "source_step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_PLAN_STEPS, start=1)
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": output_id,
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for output_id in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal_id, "review_status": "REVIEWED_ACTIVE"}
    for non_goal_id in source.NON_GOALS
]
NEXT_CHAIN = [
    "Remediation or Method Approval After Classification v2 Review, if selected.",
    "Remediation or Method Execution, if approved.",
    "Remediation or Method Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_or_method_approval_after_v2_review_if_selected",
    "remediation_or_method_execution_if_approved",
    "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_after_v2_does_not_select_package",
    "review_after_v2_does_not_approve_package",
    "review_after_v2_does_not_execute_remediation",
    "review_after_v2_does_not_execute_diagnostics",
    "review_after_v2_does_not_execute_classification",
    "review_after_v2_does_not_read_cache",
    "review_after_v2_does_not_run_retry",
    "review_after_v2_does_not_run_full_pytest",
    "review_after_v2_does_not_create_new_retry_candidate",
    "review_after_v2_does_not_create_retry_results_review",
    "review_after_v2_does_not_create_integration_results_review",
    "review_after_v2_does_not_mark_integration_successful",
    "review_after_v2_does_not_generate_successful_integration_digest",
    "review_after_v2_does_not_claim_failure_error_separation",
    "review_after_v2_does_not_claim_first_failure",
    "review_after_v2_does_not_claim_traceback_root_cause",
    "review_after_v2_does_not_treat_classification_as_retry_success",
    "review_after_v2_does_not_push_integration_branch",
    "review_after_v2_does_not_push_main",
    "review_after_v2_does_not_delete_integration_branch",
    "review_after_v2_does_not_delete_worktree",
    "review_after_v2_does_not_force_push",
    "review_after_v2_does_not_prune_remotes",
    "review_after_v2_does_not_modify_tags",
    "review_after_v2_does_not_commit_marketflow_outputs",
    "review_after_v2_does_not_commit_pytest_cache",
    "review_after_v2_does_not_modify_staged_evidence",
    "review_after_v2_does_not_regenerate_evidence",
    "review_after_v2_does_not_call_providers",
    "review_after_v2_does_not_acquire_market_data",
    "review_after_v2_does_not_regenerate_dataset",
    "review_after_v2_does_not_recompute_metrics",
    "review_after_v2_does_not_train_models",
    "review_after_v2_does_not_score_strategy",
    "review_after_v2_does_not_generate_recommendations",
    "review_after_v2_does_not_accept_predictive_usefulness",
    "review_after_v2_does_not_accept_profitability",
    "review_after_v2_does_not_authorize_runtime",
    "review_after_v2_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_approval_required_before_execution",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_after_v2_candidate_digest_bound",
    "source_results_review_v2_digest_bound",
    "source_review_manifest_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "source_digest_manifest_bound",
    "source_approval_v2_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "module_grouping_reviewed_bound",
    "module_count_29_bound",
    "largest_module_counts_bound",
    "unsupported_claims_bound",
    "review_created_true",
    "review_ready_true",
    "packages_reviewed_true",
    "future_requirements_reviewed_true",
    "future_plan_reviewed_true",
    "planned_outputs_reviewed_true",
    "non_goals_reviewed_true",
    "ready_for_approval_false",
    "recommended_package_reviewed_not_selected",
    "packages_reviewed_9",
    "blocked_packages_reviewed_3",
    "method_selected_false",
    "method_approved_false",
    "method_executed_false",
    "diagnostic_method_executed_false",
    "code_remediation_executed_false",
    "evidence_remediation_executed_false",
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


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
    ValueError
):
    """Raised when source bindings, reviewed packages, or boundaries are invalid."""


def _committed_source_fields() -> dict[str, Any]:
    candidate = source._committed_source_fields()
    return {
        "source_after_v2_candidate_artifact_kind": (
            source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1
        ),
        "source_after_v2_candidate_status": (
            source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW
        ),
        "source_after_v2_candidate_scope": (
            source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
        ),
        "source_after_v2_candidate_digest": SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        "source_execution_v2_digest": source.source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_digest_manifest_digest": source.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_approval_v2_digest": source.source.source.SOURCE_APPROVAL_V2_DIGEST,
        "source_candidate_v2_operator_review_digest": candidate["source_classification_method_candidate_v2_operator_review_digest"],
        "source_candidate_v2_digest": candidate["source_classification_method_candidate_v2_digest"],
        "source_reentry_digest": candidate["source_classification_method_reentry_digest"],
        "source_classification_source_results_review_digest": candidate["source_classification_source_results_review_digest"],
        "source_cache_manifest_review_digest": candidate["source_cache_manifest_review_digest"],
        "source_staged_inventory_digest": candidate["source_staged_inventory_digest"],
        **{
            field: deepcopy(candidate[field])
            for field in (
                "retry_execution_branch",
                "retry_execution_commit",
                "retry_pytest_passed_count",
                "retry_pytest_failed_count",
                "retry_pytest_error_count",
                "retry_pytest_skipped_count",
                "retry_pytest_first_result_authoritative",
                "root_full_regression_is_retry_evidence",
                "classification_method_v2_executed",
                "classification_execution_created",
                "classification_execution_performed",
                "classification_source_type",
                "classification_source_used_for_module_level_only",
                "failed_or_errored_nodeids_classified",
                "failed_or_errored_nodeids_count",
                "module_level_grouping_generated",
                "module_level_grouping_reviewed",
                "module_summary_generated",
                "module_summary_reviewed",
                "module_summary_module_count",
                "largest_module_summary_generated",
                "largest_module_summary_reviewed",
                "largest_module_nodeid_counts",
                "failure_modules_classified",
                "error_modules_classified",
                "failure_error_separation_claimed",
                "first_failure_identified",
                "first_error_identified",
                "first_order_claim_made",
                "traceback_root_cause_claimed",
                "retry_success_claimed",
                "main_merge_readiness_claimed",
                "root_cause_family_hints_generated",
                "root_cause_family_hints_basis",
                "limitations_report_generated",
                "limitations_reviewed",
                "unsupported_claims_exclusion_report_generated",
                "unsupported_claims_exclusion_reviewed",
                "ready_for_remediation_or_method_candidate_after_v2_review",
                "origin_main_commit",
                "integration_branch_name",
                "integration_branch_head_commit",
                "remote_integration_branch_exists",
                "detached_integration_worktree_path",
                "detached_integration_worktree_head_commit",
                "staged_evidence_manifest_digest",
                "staged_evidence_unchanged",
                "marketflow_outputs_tracked_in_repository",
                "marketflow_outputs_tracked_in_detached_worktree",
                "pytest_cache_tracked_in_repository",
                "pytest_cache_tracked_in_detached_worktree",
            )
        },
        "remediation_or_method_candidate_after_v2_review_created": True,
        "remediation_or_method_candidate_after_v2_review_ready_for_operator_review": True,
    }


def _source_fields(source_candidate: dict | None) -> dict[str, Any]:
    if source_candidate is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        source_candidate
    )
    fields = _committed_source_fields()
    mapping = {
        "source_after_v2_candidate_artifact_kind": "artifact_kind",
        "source_after_v2_candidate_status": "candidate_status",
        "source_after_v2_candidate_scope": "candidate_scope",
        "source_after_v2_candidate_digest": (
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest"
        ),
        "source_results_review_v2_digest": "source_classification_method_results_review_v2_digest",
        "source_review_manifest_digest": "source_classification_method_results_review_v2_manifest_digest",
        "source_execution_v2_digest": "source_classification_method_execution_v2_digest",
        "source_module_grouping_digest": "source_classification_method_v2_module_grouping_digest",
        "source_digest_manifest_digest": "source_classification_method_v2_digest_manifest_digest",
        "source_approval_v2_digest": "source_classification_method_approval_v2_digest",
        "source_staged_inventory_digest": "source_staged_inventory_digest",
    }
    for target, source_field in mapping.items():
        fields[target] = deepcopy(source_candidate.get(source_field))
    for field in set(fields) - set(mapping):
        if field in source_candidate:
            fields[field] = deepcopy(source_candidate[field])
    return fields


def _unsupported_claims_boundary() -> dict[str, bool]:
    return source._unsupported_claims_boundary()


def _base_review(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **deepcopy(dict(source_fields)),
        "unsupported_claims_boundary": _unsupported_claims_boundary(),
        "reviewed_candidate_after_v2_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_after_v2_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_after_v2_goal": REVIEWED_CANDIDATE_GOAL,
        "candidate_philosophy_review_status": REVIEWED_CANDIDATE_PHILOSOPHY_STATUS,
        "reviewed_packages": deepcopy(REVIEWED_PACKAGES),
        "reviewed_future_requirements": deepcopy(REVIEWED_FUTURE_REQUIREMENTS),
        "reviewed_future_plan": deepcopy(REVIEWED_FUTURE_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "remediation_or_method_candidate_after_v2_review_operator_review_created": True,
        "remediation_or_method_candidate_after_v2_review_operator_review_ready": True,
        "after_v2_packages_reviewed": True,
        "future_after_v2_requirements_reviewed": True,
        "future_after_v2_plan_reviewed": True,
        "planned_outputs_reviewed": True,
        "non_goals_reviewed": True,
        "ready_for_after_v2_remediation_or_method_approval": False,
        "remediation_or_method_after_v2_selected": False,
        "remediation_or_method_after_v2_approved": False,
        "remediation_or_method_after_v2_authorized": False,
        "remediation_or_method_after_v2_executed": False,
        "diagnostic_method_after_v2_executed": False,
        "code_remediation_after_v2_executed": False,
        "evidence_remediation_after_v2_executed": False,
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
        "recommended_remediation_or_method_after_v2_package": source.RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "recommendation_reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_packages")
    packages = packages if isinstance(packages, list) else []
    recommended = next((row for row in packages if row.get("package_id") == source.RECOMMENDED_PACKAGE), {})
    values = {
        "source_after_v2_candidate_digest_bound": (SOURCE_AFTER_V2_CANDIDATE_DIGEST, review.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.SOURCE_RESULTS_REVIEW_V2_DIGEST, review.get("source_results_review_v2_digest")),
        "source_review_manifest_digest_bound": (source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST, review.get("source_review_manifest_digest")),
        "source_execution_v2_digest_bound": (source.source.SOURCE_EXECUTION_V2_DIGEST, review.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.SOURCE_MODULE_GROUPING_DIGEST, review.get("source_module_grouping_digest")),
        "source_digest_manifest_bound": (source.source.SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_digest_manifest_digest")),
        "source_approval_v2_digest_bound": (source.source.source.SOURCE_APPROVAL_V2_DIGEST, review.get("source_approval_v2_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "module_grouping_reviewed_bound": (True, review.get("module_level_grouping_reviewed")),
        "module_count_29_bound": (29, review.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], review.get("largest_module_nodeid_counts")),
        "unsupported_claims_bound": (_unsupported_claims_boundary(), review.get("unsupported_claims_boundary")),
        "review_created_true": (True, review.get("remediation_or_method_candidate_after_v2_review_operator_review_created")),
        "review_ready_true": (True, review.get("remediation_or_method_candidate_after_v2_review_operator_review_ready")),
        "packages_reviewed_true": (True, review.get("after_v2_packages_reviewed")),
        "future_requirements_reviewed_true": (True, review.get("future_after_v2_requirements_reviewed")),
        "future_plan_reviewed_true": (True, review.get("future_after_v2_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_after_v2_remediation_or_method_approval")),
        "recommended_package_reviewed_not_selected": (["REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED", False], [recommended.get("review_status"), recommended.get("selected")]),
        "packages_reviewed_9": (9, len(packages)),
        "blocked_packages_reviewed_3": (3, sum(row.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for row in packages)),
        "method_selected_false": (False, review.get("remediation_or_method_after_v2_selected")),
        "method_approved_false": (False, review.get("remediation_or_method_after_v2_approved")),
        "method_executed_false": (False, review.get("remediation_or_method_after_v2_executed")),
        "diagnostic_method_executed_false": (False, review.get("diagnostic_method_after_v2_executed")),
        "code_remediation_executed_false": (False, review.get("code_remediation_after_v2_executed")),
        "evidence_remediation_executed_false": (False, review.get("evidence_remediation_after_v2_executed")),
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
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
    }
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "remediation_or_method_candidate_after_v2_review_operator_review_created": True,
        "remediation_or_method_candidate_after_v2_review_operator_review_ready": True,
        "after_v2_packages_reviewed": True,
        "recommended_remediation_or_method_after_v2_package": source.RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "ready_for_after_v2_remediation_or_method_approval": False,
        "method_executed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the deterministic operator review from committed candidate constants."""
    review = _base_review(_source_fields(source_candidate))
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review[
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest"
    ] = marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest_v1(
        review
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        review
    )
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings, complete review rows, and closed authority."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_committed_source_fields(),
        "unsupported_claims_boundary": _unsupported_claims_boundary(),
        "reviewed_candidate_after_v2_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_after_v2_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_after_v2_goal": REVIEWED_CANDIDATE_GOAL,
        "candidate_philosophy_review_status": REVIEWED_CANDIDATE_PHILOSOPHY_STATUS,
        "reviewed_packages": REVIEWED_PACKAGES,
        "reviewed_future_requirements": REVIEWED_FUTURE_REQUIREMENTS,
        "reviewed_future_plan": REVIEWED_FUTURE_PLAN,
        "reviewed_planned_outputs": REVIEWED_PLANNED_OUTPUTS,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommended_remediation_or_method_after_v2_package": source.RECOMMENDED_PACKAGE,
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
    required_true = (
        "created_offline",
        "governance_only",
        "operator_review_only",
        "remediation_or_method_candidate_after_v2_review_operator_review_created",
        "remediation_or_method_candidate_after_v2_review_operator_review_ready",
        "after_v2_packages_reviewed",
        "future_after_v2_requirements_reviewed",
        "future_after_v2_plan_reviewed",
        "planned_outputs_reviewed",
        "non_goals_reviewed",
    )
    required_false = (
        "ready_for_after_v2_remediation_or_method_approval",
        "recommended_package_selected",
        "remediation_or_method_after_v2_selected",
        "remediation_or_method_after_v2_approved",
        "remediation_or_method_after_v2_authorized",
        "remediation_or_method_after_v2_executed",
        "diagnostic_method_after_v2_executed",
        "code_remediation_after_v2_executed",
        "evidence_remediation_after_v2_executed",
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
        "marketflow_outputs_tracked_in_repository",
        "pytest_cache_tracked_in_repository",
    )
    for field in required_true:
        _expect(review.get(field), True, field)
    for field in required_false:
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(review, checklist), "summary")
    digest = review.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            "operator review digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest_v1(
            review
        ),
        "operator review digest",
    )
    return {
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest": digest,
        **{
            key: review["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        review
    )
    sections = [
        ("Source After-v2 Candidate", [f"Candidate digest: `{SOURCE_AFTER_V2_CANDIDATE_DIGEST}`."]),
        ("Source Results Review v2", [f"Results-review digest: `{source.SOURCE_RESULTS_REVIEW_V2_DIGEST}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The root regression is not retry evidence."]),
        ("Classification Evidence Summary", ["The reviewed 1,404 node IDs form 29 modules; grouping is prioritization evidence, not root-cause evidence."]),
        ("Review Scope", [REVIEWED_CANDIDATE_BOUNDARY]),
        ("Reviewed Candidate Philosophy", [REVIEWED_CANDIDATE_PHILOSOPHY, REVIEWED_CANDIDATE_GOAL]),
        ("Reviewed Packages", [f"`{row['package_id']}` — `{row['review_status']}`" for row in review["reviewed_packages"]]),
        ("Reviewed Future Requirements", [f"`{row['requirement_id']}` — `{row['review_status']}`" for row in review["reviewed_future_requirements"]]),
        ("Reviewed Future Plan", [f"`{row['step_id']}` — `{row['review_status']}`" for row in review["reviewed_future_plan"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_id']}` — `{row['review_status']}`" for row in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [f"`{row['non_goal_id']}` — `{row['review_status']}`" for row in review["reviewed_non_goals"]]),
        ("Recommendation", [f"`{RECOMMENDED_NEXT_TASK}` — `{RECOMMENDED_NEXT_TASK_STATUS}`.", RECOMMENDATION_REASON]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Authority Boundaries", ["No package is selected or approved; all execution, retry, main-merge, runtime, and trading authority remains closed."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["A separate optional selection and approval is required before execution.", "The failed retry remains authoritative."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Classification v2 Review Operator Review v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict:
    """Write canonical operator-review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        source_candidate=source_candidate
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_"
        "classification_v2_review_operator_review_v1.json"
    )
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError(
            "operator-review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
