"""Review the targeted diagnostic-output capture candidate entirely offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_digest"
SOURCE_CANDIDATE_DIGEST = "6dbc98d7b1c796c16e2723508e5ab8cb9c895849844a3c37aeb843bbff0690be"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS = source.PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS
PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED = source.PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED
PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE = source.PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE
PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT = source.PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT
PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH = source.PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH
PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY = source.PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY
PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT = source.PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT
PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE = source.PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE
PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT = source.PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT
PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION = source.PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION
PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW = source.PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = source.PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY
RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE = PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS

REVIEWED_PHILOSOPHY = (
    "The reviewed after-v2 planning reentry identified Priority 1 top module groups as the highest-concentration "
    "diagnostic planning target. The next safe step is to review controlled diagnostic-output capture methods "
    "for those modules only, preserving the failed retry as authoritative while preparing bounded diagnostic "
    "information for later review. The operator review must not execute diagnostics, run pytest, infer root "
    "cause, recommend remediation, or create retry readiness."
)
REVIEWED_BOUNDARY = (
    "Operator-review only; no diagnostic command, diagnostic capture, remediation, classification, retry, "
    "results review, main merge, runtime, or trading authority is created."
)
REVIEWED_GOAL = "Review safe future packages for targeted diagnostic output capture from the reviewed Priority 1 top module groups."

NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_V1_IF_SELECTED"
RECOMMENDED_ACTION = "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION"
RECOMMENDATION_REASON = (
    "The targeted diagnostic output capture candidate has been reviewed, but no diagnostic package has been "
    "selected or approved by this review. Diagnostic capture execution requires a separate approval ceremony."
)

SOURCE_BINDINGS = {
    "source_targeted_diagnostic_output_capture_candidate_digest": SOURCE_CANDIDATE_DIGEST,
    "source_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
    "source_prioritized_planning_review_digest": source.SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
    "source_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    "source_planning_execution_digest": source.SOURCE_PLANNING_EXECUTION_DIGEST,
    "source_prioritized_planning_digest": source.SOURCE_PRIORITIZED_PLANNING_DIGEST,
    "source_planning_digest_manifest_digest": source.SOURCE_PLANNING_MANIFEST_DIGEST,
    "source_detail_binding_results_review_digest": source.SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"],
    "source_complete_29_row_binding_review_digest": source.SOURCE_BINDINGS["source_complete_29_row_binding_review_digest"],
    "source_detail_binding_results_review_manifest_digest": source.SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_manifest_digest"],
    "source_detail_binding_reattempt_digest": source.SOURCE_BINDINGS["source_detail_binding_reattempt_digest"],
    "source_complete_29_row_binding_digest": source.SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
    "source_detail_binding_reattempt_manifest_digest": source.SOURCE_BINDINGS["source_detail_binding_reattempt_digest_manifest_digest"],
    "source_materialization_results_review_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_results_review_digest"],
    "source_materialized_payload_review_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialized_payload_review_digest"],
    "source_materialization_results_review_manifest_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_results_review_manifest_digest"],
    "source_materialization_execution_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_execution_digest"],
    "source_materialized_payload_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialized_payload_digest"],
    "source_materialization_digest_manifest_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_digest_manifest_digest"],
    "source_detail_binding_approval_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_approval_digest"],
    "source_detail_binding_operator_review_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_operator_review_digest"],
    "source_detail_binding_candidate_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_candidate_digest"],
    "source_prior_blocked_detail_binding_execution_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_digest"],
    "source_prior_blocked_detail_binding_manifest_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_manifest_digest"],
    "source_prior_blocked_detail_binding_reason": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_blocked_reason"],
    "source_complete_29_row_materialization_approval_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_approval_digest"],
    "source_complete_29_row_materialization_operator_review_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_operator_review_digest"],
    "source_complete_29_row_materialization_candidate_digest": source.SOURCE_BINDINGS["source_complete_29_row_materialization_candidate_digest"],
    "source_execution_failure_diagnosis_digest": source.SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"],
    "primary_failure_class": source.SOURCE_BINDINGS["primary_failure_class"],
    "source_reentry_failure_diagnosis_digest": source.SOURCE_BINDINGS["source_reentry_failure_diagnosis_digest"],
    "source_reentry_failure_primary_failure_class": source.SOURCE_BINDINGS["source_reentry_failure_primary_failure_class"],
    "source_reentry_execution_blocked_digest": source.SOURCE_BINDINGS["source_reentry_execution_blocked_digest"],
    "source_reentry_execution_blocked_manifest_digest": source.SOURCE_BINDINGS["source_reentry_execution_blocked_manifest_digest"],
    "source_reentry_execution_blocked_reason": source.SOURCE_BINDINGS["source_reentry_execution_blocked_reason"],
    "source_recovery_results_review_digest": source.SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"],
    "source_recovery_results_review_manifest_digest": source.SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_manifest_digest"],
    "source_recovery_execution_digest": source.SOURCE_BINDINGS["source_module_grouping_source_recovery_execution_digest"],
    "source_recovery_detail_digest": source.SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"],
    "source_recovery_digest_manifest_digest": source.SOURCE_BINDINGS["source_module_grouping_source_recovery_digest_manifest_digest"],
    "source_blocked_after_v2_execution_digest": source.SOURCE_BINDINGS["source_blocked_after_v2_execution_digest"],
    "source_blocked_after_v2_manifest_digest": source.SOURCE_BINDINGS["source_blocked_after_v2_manifest_digest"],
    "blocked_reason_before_recovery": source.SOURCE_BINDINGS["blocked_reason_before_recovery"],
    "source_after_v2_approval_digest": source.SOURCE_BINDINGS["source_after_v2_approval_digest"],
    "source_after_v2_operator_review_digest": source.SOURCE_BINDINGS["source_after_v2_operator_review_digest"],
    "source_after_v2_candidate_digest": source.SOURCE_BINDINGS["source_after_v2_candidate_digest"],
    "source_results_review_v2_digest": source.SOURCE_BINDINGS["source_results_review_v2_digest"],
    "source_execution_v2_digest": source.SOURCE_BINDINGS["source_execution_v2_digest"],
    "source_module_grouping_digest": source.SOURCE_BINDINGS["source_module_grouping_digest"],
    "source_approval_v2_digest": source.SOURCE_BINDINGS["source_approval_v2_digest"],
    "source_staged_inventory_digest": source.SOURCE_BINDINGS["source_staged_inventory_digest"],
}

PACKAGE_REVIEW_STATUSES = [
    "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
    "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED",
    "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "REVIEWED_AVAILABLE_NOT_RECOMMENDED_FOR_FIRST_PASS_NOT_SELECTED",
    "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED", "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
    *(["REVIEWED_BLOCKED_NOT_ALLOWED"] * 6),
]
REVIEWED_PACKAGES = [
    {
        "package_id": package["package_id"], "source_status": package["status"],
        "review_status": review_status, "selected": False, "approved": False, "executed": False,
        **({"purpose": package["purpose"]} if "purpose" in package else {}),
        **({"blocked_reason": package["blocked_reason"]} if "blocked_reason" in package else {}),
        **({"not_recommended_reason": package["not_recommended_reason"]} if "not_recommended_reason" in package else {}),
    }
    for package, review_status in zip(source.PACKAGES, PACKAGE_REVIEW_STATUSES, strict=True)
]
REVIEWED_REQUIREMENTS = [
    {"requirement_id": requirement_id, "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_TARGETED_DIAGNOSTIC_CAPTURE", "execution_status": "NOT_EXECUTED"}
    for requirement_id in source.FUTURE_REQUIREMENTS
]
REVIEWED_PLAN = [
    {"step_id": index, "step": step, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": "NOT_EXECUTED"}
    for index, step in enumerate(source.FUTURE_PLAN, start=1)
]
REVIEWED_COMMAND_TEMPLATE = {
    "future_diagnostic_command_template_review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
    **deepcopy(source.FUTURE_COMMAND_TEMPLATE),
}
REVIEWED_OUTPUTS = [
    {"output_id": output_id, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
    for output_id in source.PLANNED_OUTPUT_IDS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal, "review_status": "REVIEWED_ACTIVE"}
    for non_goal in source.NON_GOALS
    if non_goal != "do_not_create_diagnostic_operator_review_now"
]

NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Approval v1, if selected.",
    "Targeted Diagnostic Output Capture Execution v1, if approved.",
    "Targeted Diagnostic Output Capture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if needed.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "targeted_diagnostic_output_capture_approval_if_selected", "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_needed",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_diagnostic_capture_does_not_select_package", "review_diagnostic_capture_does_not_approve_package",
    "review_diagnostic_capture_does_not_execute_diagnostic_capture", "review_diagnostic_capture_does_not_run_pytest",
    "review_diagnostic_capture_does_not_run_targeted_pytest", "review_diagnostic_capture_does_not_run_full_pytest",
    "review_diagnostic_capture_does_not_rerun_retry", "review_diagnostic_capture_does_not_read_cache",
    "review_diagnostic_capture_does_not_modify_cache", "review_diagnostic_capture_does_not_rerun_planning",
    "review_diagnostic_capture_does_not_rerun_detail_binding", "review_diagnostic_capture_does_not_rerun_materialization",
    "review_diagnostic_capture_does_not_rerun_source_recovery", "review_diagnostic_capture_does_not_execute_remediation",
    "review_diagnostic_capture_does_not_execute_classification", "review_diagnostic_capture_does_not_classify_modules_again",
    "review_diagnostic_capture_does_not_identify_first_failure", "review_diagnostic_capture_does_not_identify_first_error",
    "review_diagnostic_capture_does_not_claim_traceback_root_cause", "review_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "review_diagnostic_capture_does_not_create_diagnostic_approval", "review_diagnostic_capture_does_not_create_diagnostic_results_review",
    "review_diagnostic_capture_does_not_create_new_retry_candidate", "review_diagnostic_capture_does_not_create_retry_results_review",
    "review_diagnostic_capture_does_not_create_integration_results_review", "review_diagnostic_capture_does_not_mark_integration_successful",
    "review_diagnostic_capture_does_not_generate_successful_integration_digest", "review_diagnostic_capture_does_not_push_integration_branch",
    "review_diagnostic_capture_does_not_push_main", "review_diagnostic_capture_does_not_delete_integration_branch",
    "review_diagnostic_capture_does_not_delete_worktree", "review_diagnostic_capture_does_not_force_push",
    "review_diagnostic_capture_does_not_prune_remotes", "review_diagnostic_capture_does_not_modify_tags",
    "review_diagnostic_capture_does_not_modify_staged_evidence", "review_diagnostic_capture_does_not_regenerate_evidence",
    "review_diagnostic_capture_does_not_call_providers", "review_diagnostic_capture_does_not_inspect_env",
    "review_diagnostic_capture_does_not_acquire_market_data", "review_diagnostic_capture_does_not_regenerate_dataset",
    "review_diagnostic_capture_does_not_recompute_metrics", "review_diagnostic_capture_does_not_train_models",
    "review_diagnostic_capture_does_not_score_strategy", "review_diagnostic_capture_does_not_generate_recommendations",
    "review_diagnostic_capture_does_not_accept_predictive_usefulness", "review_diagnostic_capture_does_not_accept_profitability",
    "review_diagnostic_capture_does_not_authorize_runtime", "review_diagnostic_capture_does_not_authorize_broker_execution",
    "review_output_is_planning_only_not_diagnostic_execution", "future_diagnostic_capture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause", "module_concentration_is_not_failure_error_separation",
    "previous_targeted_diagnostic_candidate_remains_source_evidence", "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid", "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_approval_required_before_diagnostic_execution",
    "separate_results_review_required_after_diagnostic_capture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "targeted_diagnostic_output_capture_candidate_operator_review_created",
    "targeted_diagnostic_output_capture_candidate_operator_review_ready", "source_candidate_reviewed",
    "priority_1_top_module_groups_reviewed", "diagnostic_capture_packages_reviewed",
    "future_diagnostic_capture_requirements_reviewed", "future_diagnostic_capture_plan_reviewed",
    "future_diagnostic_command_template_reviewed", "planned_outputs_reviewed", "non_goals_reviewed",
]
FALSE_FIELDS = [
    "diagnostic_capture_package_selected", "diagnostic_capture_package_approved", "diagnostic_capture_package_authorized",
    "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created", "diagnostic_output_captured",
    "diagnostic_command_executed", "diagnostic_method_executed", "ready_for_targeted_diagnostic_output_capture_approval",
    "ready_for_diagnostic_capture_approval", "ready_for_diagnostic_capture_execution", "ready_for_retry_candidate",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "cache_read_in_review", "cache_modified_in_review", "planning_reentry_rerun_performed",
    "detail_binding_reattempt_rerun_performed", "materialization_execution_rerun_performed",
    "source_recovery_rerun_performed", "module_grouping_recovered_in_review", "retry_rerun_performed",
    "full_pytest_performed", "targeted_pytest_performed", "code_remediation_executed",
    "evidence_remediation_executed", "classification_execution_performed_in_review", "failure_modules_classified",
    "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified",
    "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError(ValueError):
    """Raised when the source candidate or operator review violates its contract."""


def _expected_source_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "candidate_status": source.CANDIDATE_STATUS,
        "candidate_scope": source.CANDIDATE_SCOPE, source.DIGEST_KEY: SOURCE_CANDIDATE_DIGEST,
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "targeted_diagnostic_output_capture_candidate_created": True,
        "targeted_diagnostic_output_capture_candidate_ready_for_operator_review": True,
        "priority_1_top_module_groups_bound_for_candidate": True, "diagnostic_capture_packages_defined": True,
        "future_diagnostic_capture_requirements_defined": True, "future_diagnostic_capture_plan_defined": True,
        "ready_for_targeted_diagnostic_output_capture_candidate_operator_review": True,
        "diagnostic_capture_package_selected": False, "diagnostic_capture_package_approved": False,
        "diagnostic_capture_package_authorized": False, "diagnostic_capture_execution_performed": False,
        "ready_for_retry_candidate": False, "priority_1_top_module_groups": source.TOP_MODULES,
        "planning_buckets_summary": source.PLANNING_BUCKETS,
        "proposed_diagnostic_capture_packages": source.PACKAGES,
        "future_diagnostic_capture_requirements": source.FUTURE_REQUIREMENTS,
        "future_diagnostic_capture_plan": {"status": source.PLANNED_NOT_EXECUTED, "steps": source.FUTURE_PLAN},
        "future_diagnostic_command_template": source.FUTURE_COMMAND_TEMPLATE,
        "planned_outputs": [{"output_id": item, "status": source.PLANNED_NOT_GENERATED} for item in source.PLANNED_OUTPUT_IDS],
        "non_goals": source.NON_GOALS,
    }


def _bind_source_candidate(value: dict | None) -> dict[str, Any]:
    expected = _expected_source_candidate()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("source candidate must be an object")
    for field, required in expected.items():
        if value.get(field) != required:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError(f"source candidate {field} mismatch")
    return deepcopy(dict(value))


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


SOURCE_CHECK_IDS = {
    "source_targeted_diagnostic_output_capture_candidate_digest": "source_candidate_digest_bound",
    "source_results_review_digest": "source_results_review_digest_bound",
    "source_prioritized_planning_review_digest": "source_prioritized_planning_review_digest_bound",
    "source_results_review_manifest_digest": "source_results_review_manifest_digest_bound",
    "source_planning_execution_digest": "source_planning_execution_digest_bound",
    "source_prioritized_planning_digest": "source_prioritized_planning_digest_bound",
    "source_planning_digest_manifest_digest": "source_planning_digest_manifest_digest_bound",
    "source_detail_binding_results_review_digest": "source_detail_binding_results_review_digest_bound",
    "source_complete_29_row_binding_review_digest": "source_complete_29_row_binding_review_digest_bound",
    "source_detail_binding_results_review_manifest_digest": "source_detail_binding_results_review_manifest_digest_bound",
    "source_detail_binding_reattempt_digest": "source_detail_binding_reattempt_digest_bound",
    "source_complete_29_row_binding_digest": "source_complete_29_row_binding_digest_bound",
    "source_detail_binding_reattempt_manifest_digest": "source_detail_binding_reattempt_manifest_digest_bound",
    "source_materialization_results_review_digest": "source_materialization_results_review_digest_bound",
    "source_materialized_payload_review_digest": "source_materialized_payload_review_digest_bound",
    "source_materialization_results_review_manifest_digest": "source_materialization_results_review_manifest_digest_bound",
    "source_materialization_execution_digest": "source_materialization_execution_digest_bound",
    "source_materialized_payload_digest": "source_materialized_payload_digest_bound",
    "source_materialization_digest_manifest_digest": "source_materialization_digest_manifest_digest_bound",
    "source_detail_binding_approval_digest": "source_detail_binding_approval_digest_bound",
    "source_prior_blocked_detail_binding_execution_digest": "source_prior_blocked_detail_binding_execution_digest_bound",
    "source_prior_blocked_detail_binding_reason": "source_prior_blocked_detail_binding_reason_bound",
    "source_complete_29_row_materialization_approval_digest": "source_materialization_approval_digest_bound",
    "source_complete_29_row_materialization_operator_review_digest": "source_materialization_operator_review_digest_bound",
    "source_complete_29_row_materialization_candidate_digest": "source_materialization_candidate_digest_bound",
    "source_execution_failure_diagnosis_digest": "source_execution_failure_diagnosis_digest_bound",
    "primary_failure_class": "source_primary_failure_class_bound",
    "source_reentry_failure_diagnosis_digest": "source_reentry_failure_diagnosis_digest_bound",
    "source_reentry_failure_primary_failure_class": "source_reentry_failure_primary_failure_class_bound",
    "source_reentry_execution_blocked_digest": "source_reentry_execution_blocked_digest_bound",
    "source_reentry_execution_blocked_manifest_digest": "source_reentry_execution_blocked_manifest_digest_bound",
    "source_reentry_execution_blocked_reason": "source_reentry_execution_blocked_reason_bound",
    "source_recovery_results_review_digest": "source_recovery_results_review_digest_bound",
    "source_recovery_detail_digest": "source_recovery_detail_digest_bound",
    "source_after_v2_approval_digest": "source_after_v2_approval_digest_bound",
    "source_results_review_v2_digest": "source_results_review_v2_digest_bound",
    "source_execution_v2_digest": "source_execution_v2_digest_bound",
    "source_module_grouping_digest": "source_module_grouping_digest_bound",
}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(check_id, SOURCE_BINDINGS[field], review.get(field)) for field, check_id in SOURCE_CHECK_IDS.items()]
    checks.extend([
        _check("source_selected_after_v2_planning_package_bound", source.SELECTED_AFTER_V2_PLANNING_PACKAGE, review.get("selected_after_v2_planning_package")),
        _check("retry_execution_commit_bound", source.RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        _check("source_candidate_ready_bound", source.CANDIDATE_STATUS, review.get("source_candidate_summary", {}).get("status")),
        _check("source_review_ready_bound", source.source.REVIEW_STATUS, review.get("source_results_review_summary", {}).get("status")),
        _check("ready_for_targeted_diagnostic_candidate_from_source_true", True, review.get("source_candidate_summary", {}).get("candidate_ready")),
        _check("ready_for_retry_candidate_from_source_false", False, review.get("source_candidate_summary", {}).get("ready_for_retry_candidate")),
        _check("priority_1_top_module_paths_reviewed", [x["module_path"] for x in source.TOP_MODULES], [x.get("module_path") for x in review.get("priority_1_top_module_groups", [])]),
        _check("priority_1_top_module_counts_reviewed", [136, 131, 122, 112, 111], [x.get("failed_or_errored_nodeid_count") for x in review.get("priority_1_top_module_groups", [])]),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("planning_buckets_reviewed", source.PLANNING_BUCKETS, review.get("planning_buckets_summary")),
        _check("operator_review_created_true", True, review.get("targeted_diagnostic_output_capture_candidate_operator_review_created")),
        _check("operator_review_ready_true", True, review.get("targeted_diagnostic_output_capture_candidate_operator_review_ready")),
        _check("source_candidate_reviewed_true", True, review.get("source_candidate_reviewed")),
        _check("diagnostic_capture_packages_reviewed_true", True, review.get("diagnostic_capture_packages_reviewed")),
        _check("future_requirements_reviewed_true", True, review.get("future_diagnostic_capture_requirements_reviewed")),
        _check("future_plan_reviewed_true", True, review.get("future_diagnostic_capture_plan_reviewed")),
        _check("future_command_template_reviewed_not_executed", "REVIEWED_PLANNED_NOT_EXECUTED", review.get("reviewed_future_diagnostic_command_template", {}).get("future_diagnostic_command_template_review_status")),
        _check("planned_outputs_reviewed_true", True, review.get("planned_outputs_reviewed")),
        _check("non_goals_reviewed_true", True, review.get("non_goals_reviewed")),
        _check("recommended_package_reviewed_not_selected", False, review.get("recommendation", {}).get("selected")),
        _check("packages_reviewed_12", 12, len(review.get("reviewed_diagnostic_capture_packages", []))),
        _check("blocked_packages_reviewed_6", 6, sum(x.get("source_status") == "BLOCKED_NOT_ALLOWED" for x in review.get("reviewed_diagnostic_capture_packages", []))),
    ])
    false_aliases = {
        "diagnostic_capture_execution_performed": "diagnostic_capture_execution_false",
        "diagnostic_capture_results_review_created": "diagnostic_capture_results_review_false",
        "planning_reentry_rerun_performed": "planning_reentry_rerun_false",
        "detail_binding_reattempt_rerun_performed": "detail_binding_reattempt_rerun_false",
        "materialization_execution_rerun_performed": "materialization_execution_rerun_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "targeted_pytest_performed": "targeted_pytest_false", "retry_rerun_performed": "retry_rerun_false",
        "full_pytest_performed": "full_pytest_false", "code_remediation_executed": "code_remediation_false",
        "evidence_remediation_executed": "evidence_remediation_false",
        "classification_execution_performed_in_review": "classification_execution_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "main_push_performed": "main_push_false", "origin_main_modified_by_this_task": "origin_main_modified_false",
        "provider_requests_made_in_review": "provider_requests_false",
        "market_data_acquisition_performed_in_review": "market_data_acquisition_false",
        "dataset_generation_performed_in_review": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    for field in FALSE_FIELDS:
        checks.append(_check(false_aliases.get(field, f"{field}_false"), False, review.get(field)))
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, review.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, review.get("pytest_cache_committed")),
    ])
    return checks


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(item["status"] == PASS for item in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed,
        **{field: review.get(field) for field in TRUE_FIELDS},
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "recommended_package_selected": False,
        **{field: review.get(field) for field in (
            "diagnostic_capture_package_selected", "diagnostic_capture_package_approved", "diagnostic_capture_package_authorized",
            "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created", "diagnostic_output_captured",
            "diagnostic_command_executed", "targeted_pytest_performed", "retry_rerun_performed", "full_pytest_performed",
            "ready_for_targeted_diagnostic_output_capture_approval", "ready_for_diagnostic_capture_execution",
            "ready_for_retry_candidate", "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        )},
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", DIGEST_KEY, "operator_review_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Review committed candidate structures without calling its builder or execution paths."""

    bound = _bind_source_candidate(source_candidate)
    recommendation = {
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION, "ready_for_targeted_diagnostic_output_capture_approval": False,
        "ready_for_diagnostic_capture_execution": False, "ready_for_retry_candidate": False,
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "selected": False, "reason": RECOMMENDATION_REASON,
    }
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_targeted_diagnostic_output_capture_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_targeted_diagnostic_output_capture_candidate_status": source.CANDIDATE_STATUS,
        "source_targeted_diagnostic_output_capture_candidate_scope": source.CANDIDATE_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "selected_after_v2_planning_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
            "working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "source_candidate_summary": {
            "artifact_kind": bound["artifact_kind"], "status": bound["candidate_status"], "scope": bound["candidate_scope"],
            "digest": SOURCE_CANDIDATE_DIGEST, "candidate_ready": True, "ready_for_retry_candidate": False,
        },
        "source_results_review_summary": {
            "status": source.source.REVIEW_STATUS, "digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
            "prioritized_planning_review_digest": source.SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
            "manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        },
        "source_planning_reentry_summary": {
            "execution_digest": source.SOURCE_PLANNING_EXECUTION_DIGEST,
            "prioritized_planning_digest": source.SOURCE_PRIORITIZED_PLANNING_DIGEST,
            "manifest_digest": source.SOURCE_PLANNING_MANIFEST_DIGEST,
            "selected_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        },
        "reviewed_priority_planning_facts": {
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
            "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
            "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
            "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_1_total_nodeids": 612, "priority_tier_1_count_sum": 612,
        "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        "priority_1_top_module_groups": deepcopy(source.TOP_MODULES),
        "priority_tier_summary": deepcopy(source.PRIORITY_TIERS),
        "planning_buckets_summary": deepcopy(source.PLANNING_BUCKETS),
        "reviewed_candidate_philosophy": {
            "reviewed_targeted_diagnostic_output_capture_candidate_philosophy": REVIEWED_PHILOSOPHY,
            "reviewed_candidate_boundary": REVIEWED_BOUNDARY, "reviewed_candidate_goal": REVIEWED_GOAL,
            "review_status": "REVIEWED_PLANNING_ONLY",
        },
        "reviewed_diagnostic_capture_packages": deepcopy(REVIEWED_PACKAGES),
        "reviewed_future_diagnostic_capture_requirements": deepcopy(REVIEWED_REQUIREMENTS),
        "reviewed_future_diagnostic_capture_plan": deepcopy(REVIEWED_PLAN),
        "reviewed_future_diagnostic_command_template": deepcopy(REVIEWED_COMMAND_TEMPLATE),
        "reviewed_planned_outputs": deepcopy(REVIEWED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": recommendation, "recommended_next_task": NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED", "recommended_action": RECOMMENDED_ACTION,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "reason": RECOMMENDATION_REASON, "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    review["digest_manifest"] = {
        "source_candidate": SOURCE_CANDIDATE_DIGEST, "source_results_review": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_planning_execution": source.SOURCE_PLANNING_EXECUTION_DIGEST,
        "reviewed_packages": semantic_digest(REVIEWED_PACKAGES),
        "reviewed_requirements": semantic_digest(REVIEWED_REQUIREMENTS), "reviewed_plan": semantic_digest(REVIEWED_PLAN),
        "reviewed_command_template": semantic_digest(REVIEWED_COMMAND_TEMPLATE),
        "reviewed_outputs": semantic_digest(REVIEWED_OUTPUTS), "reviewed_non_goals": semantic_digest(REVIEWED_NON_GOALS),
        "recommendation": semantic_digest(recommendation),
    }
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review[DIGEST_KEY] = _review_digest(review)
    review["operator_review_digest"] = review[DIGEST_KEY]
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Reject source drift, incomplete review content, or opened authority."""

    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("review must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_targeted_diagnostic_output_capture_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_targeted_diagnostic_output_capture_candidate_status": source.CANDIDATE_STATUS,
        "source_targeted_diagnostic_output_capture_candidate_scope": source.CANDIDATE_SCOPE,
        "selected_after_v2_planning_package": source.SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT, **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError(f"{field} mismatch")
    if review.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("retry failure counts mismatch")
    facts = review.get("reviewed_priority_planning_facts")
    expected_facts = {
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111], "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114", "priority_tier_1_count_sum": 612,
        "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
    }
    if facts != expected_facts:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("priority planning facts mismatch")
    scalars = {
        **expected_facts, "priority_1_total_nodeids": 612, "priority_1_top_module_groups": source.TOP_MODULES,
        "priority_tier_summary": source.PRIORITY_TIERS, "planning_buckets_summary": source.PLANNING_BUCKETS,
    }
    for field, expected in scalars.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError(f"{field} mismatch")
    if review.get("reviewed_candidate_philosophy") != {
        "reviewed_targeted_diagnostic_output_capture_candidate_philosophy": REVIEWED_PHILOSOPHY,
        "reviewed_candidate_boundary": REVIEWED_BOUNDARY, "reviewed_candidate_goal": REVIEWED_GOAL,
        "review_status": "REVIEWED_PLANNING_ONLY",
    }:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("reviewed philosophy mismatch")
    if review.get("reviewed_diagnostic_capture_packages") != REVIEWED_PACKAGES:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("package review mismatch")
    if len(REVIEWED_PACKAGES) != 12 or sum(x["source_status"] == "BLOCKED_NOT_ALLOWED" for x in REVIEWED_PACKAGES) != 6:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("package review counts mismatch")
    if any(x["selected"] or x["approved"] or x["executed"] for x in review["reviewed_diagnostic_capture_packages"]):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("package authority opened")
    if review.get("reviewed_future_diagnostic_capture_requirements") != REVIEWED_REQUIREMENTS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("future requirements review mismatch")
    if review.get("reviewed_future_diagnostic_capture_plan") != REVIEWED_PLAN:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("future plan review mismatch")
    if review.get("reviewed_future_diagnostic_command_template") != REVIEWED_COMMAND_TEMPLATE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("command template review mismatch")
    if review.get("reviewed_planned_outputs") != REVIEWED_OUTPUTS or review.get("reviewed_non_goals") != REVIEWED_NON_GOALS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("output or non-goal review mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("required review flag missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("closed boundary opened")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("acceptance boundary changed")
    if review.get("runtime_use") != NOT_AUTHORIZED or review.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("runtime boundary changed")
    expected_recommendation = {
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION, "ready_for_targeted_diagnostic_output_capture_approval": False,
        "ready_for_diagnostic_capture_execution": False, "ready_for_retry_candidate": False,
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "selected": False, "reason": RECOMMENDATION_REASON,
    }
    if review.get("recommendation") != expected_recommendation:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("recommendation mismatch")
    if review.get("recommended_next_task") != NEXT_TASK or review.get("recommended_action") != RECOMMENDED_ACTION:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("recommendation fields mismatch")
    if review.get("next_chain") != NEXT_CHAIN or review.get("next_gates") != NEXT_GATES or review.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("governance content mismatch")
    expected_manifest = {
        "source_candidate": SOURCE_CANDIDATE_DIGEST, "source_results_review": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_planning_execution": source.SOURCE_PLANNING_EXECUTION_DIGEST,
        "reviewed_packages": semantic_digest(REVIEWED_PACKAGES),
        "reviewed_requirements": semantic_digest(REVIEWED_REQUIREMENTS), "reviewed_plan": semantic_digest(REVIEWED_PLAN),
        "reviewed_command_template": semantic_digest(REVIEWED_COMMAND_TEMPLATE),
        "reviewed_outputs": semantic_digest(REVIEWED_OUTPUTS), "reviewed_non_goals": semantic_digest(REVIEWED_NON_GOALS),
        "recommendation": semantic_digest(expected_recommendation),
    }
    if review.get("digest_manifest") != expected_manifest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("digest manifest mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("checklist mismatch")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("summary mismatch")
    digest = review.get(DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _review_digest(review):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("operator review digest mismatch")
    if review.get("operator_review_digest") != digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("operator review digest alias mismatch")
    return {"artifact_kind": review["artifact_kind"], "review_status": review["review_status"], "review_scope": review["review_scope"], "operator_review_digest": digest, **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write deterministic JSON outside protected runtime directories."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(source_candidate=source_candidate)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": review["artifact_kind"], "review_status": review["review_status"], "operator_review_digest": review[DIGEST_KEY], "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated operator review as Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(review)
    sections = [
        ("Source Targeted Diagnostic Output Capture Candidate", [SOURCE_CANDIDATE_DIGEST, source.CANDIDATE_STATUS]),
        ("Source Remediation or Method Results Review", [source.SOURCE_RESULTS_REVIEW_DIGEST, source.SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST, source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST]),
        ("Source Planning Reentry with Complete Detail", [source.SOURCE_PLANNING_EXECUTION_DIGEST, source.SOURCE_PRIORITIZED_PLANNING_DIGEST, source.SOURCE_PLANNING_MANIFEST_DIGEST]),
        ("Source Detail Binding Results Review", [SOURCE_BINDINGS["source_detail_binding_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_binding_digest"]]),
        ("Source Materialization Results Review", [SOURCE_BINDINGS["source_materialization_results_review_digest"], SOURCE_BINDINGS["source_materialized_payload_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Reviewed Priority Planning Facts", ["29 modules; 1,404 failed-or-errored node IDs; Priority 1 contains 612 (43.58974359%)."]),
        ("Priority 1 Top Module Groups", [f"{x['rank']}. {x['module_path']}: {x['failed_or_errored_nodeid_count']}" for x in source.TOP_MODULES]),
        ("Planning Buckets", [f"{x['planning_bucket']}: {x['status']}" for x in source.PLANNING_BUCKETS]),
        ("Reviewed Candidate Philosophy", [REVIEWED_PHILOSOPHY, REVIEWED_BOUNDARY, REVIEWED_GOAL]),
        ("Reviewed Diagnostic Capture Packages", [f"{x['package_id']}: {x['review_status']}" for x in REVIEWED_PACKAGES]),
        ("Reviewed Future Diagnostic Capture Requirements", [x["requirement_id"] for x in REVIEWED_REQUIREMENTS]),
        ("Reviewed Future Diagnostic Capture Plan", [f"{x['step_id']}. {x['step']}" for x in REVIEWED_PLAN]),
        ("Reviewed Future Diagnostic Command Template", [REVIEWED_COMMAND_TEMPLATE["future_diagnostic_command_template_review_status"], REVIEWED_COMMAND_TEMPLATE["future_diagnostic_command_template"]]),
        ("Reviewed Planned Outputs", [x["output_id"] for x in REVIEWED_OUTPUTS]),
        ("Reviewed Non-Goals", [x["non_goal_id"] for x in REVIEWED_NON_GOALS]),
        ("Recommendation", [RECOMMENDED_ACTION, RECOMMENDATION_REASON]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", [REVIEWED_BOUNDARY, "No package is selected or approved; execution and downstream authority remain closed."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["This review performs no diagnostic, pytest, retry, remediation, provider, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Candidate Operator Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED",
    "PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE",
    "PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT",
    "PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH", "PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY",
    "PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT", "PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE",
    "PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT", "PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION",
    "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW", "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
    "RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_markdown_v1",
]
