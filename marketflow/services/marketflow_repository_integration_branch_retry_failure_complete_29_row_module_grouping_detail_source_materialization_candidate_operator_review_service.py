"""Review complete 29-row materialization packages without selecting one."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

SOURCE_CANDIDATE_DIGEST = "4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_V1_IF_SELECTED"
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_COMPLETE_29_ROW_MATERIALIZATION_OR_BINDING_EXECUTION"
REVIEWED_PLANNING_ONLY = "REVIEWED_PLANNING_ONLY"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_GENERATED = "NOT_GENERATED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


def _reviewed_packages() -> list[dict[str, Any]]:
    statuses = {
        RECOMMENDED_PACKAGE: "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "PACKAGE_MATERIALIZE_COMPLETE_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY": "REVIEWED_AVAILABLE_REQUIRES_SEPARATE_APPROVAL_NOT_SELECTED",
        "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE_FROM_EXISTING_RECOVERY_ARTIFACT_IF_LOCATABLE": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "PACKAGE_OPERATOR_PROVIDES_EXISTING_COMPLETE_RECOVERY_DETAIL_REPORT_PATH": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "PACKAGE_CREATE_HIGH_CONTROL_29_ROW_SOURCE_CONSTANT_FROM_REVIEWED_RECOVERY_EVIDENCE": "REVIEWED_AVAILABLE_HIGH_CONTROL_PACKAGE_NOT_SELECTED",
        "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING": "REVIEWED_AVAILABLE_NOT_RECOMMENDED_PACKAGE_NOT_SELECTED",
    }
    reviewed = []
    for package in source._packages():
        review_status = statuses.get(package["package"], "REVIEWED_BLOCKED_NOT_ALLOWED")
        reviewed.append({
            "package": package["package"], "source_status": package["status"], "review_status": review_status,
            "selected": False, "approved": False, "executed": False,
        })
    return reviewed


REVIEWED_REQUIREMENTS = [
    {"requirement_id": name, "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_COMPLETE_29_ROW_MATERIALIZATION_OR_BINDING", "execution_status": NOT_EXECUTED}
    for name in source.FUTURE_REQUIREMENTS
]
REVIEWED_PLAN = [
    {"step_id": f"step_{index}", "step": step, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": NOT_EXECUTED}
    for index, step in enumerate(source.FUTURE_PLAN, 1)
]
REVIEWED_OUTPUTS = [
    {"output_id": name, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": NOT_GENERATED}
    for name in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": name, "review_status": "REVIEWED_ACTIVE"} for name in source.NON_GOALS
]

NEXT_CHAIN = [
    "Complete 29-row Module Grouping Detail Source Materialization Approval v1, if selected.",
    "Complete 29-row Module Grouping Detail Source Materialization Execution v1, if approved.",
    "Complete 29-row Module Grouping Detail Source Materialization Results Review v1.",
    "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.", "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = source.NEXT_GATES[1:]

RISK_CONTROLS = [
    "review_materialization_does_not_select_package", "review_materialization_does_not_approve_package",
    "review_materialization_does_not_materialize_29_row_source", "review_materialization_does_not_expose_29_module_rows",
    "review_materialization_does_not_bind_complete_detail", "review_materialization_does_not_recover_module_grouping_again",
    "review_materialization_does_not_read_cache", "review_materialization_does_not_modify_cache",
    "review_materialization_does_not_parse_operator_logs", "review_materialization_does_not_run_diagnostic_commands",
    "review_materialization_does_not_execute_diagnostics", "review_materialization_does_not_execute_remediation",
    "review_materialization_does_not_execute_classification", "review_materialization_does_not_classify_modules_again",
    "review_materialization_does_not_execute_detail_binding", "review_materialization_does_not_execute_after_v2_planning_reentry",
    "review_materialization_does_not_rerun_retry", "review_materialization_does_not_run_full_pytest",
    "review_materialization_does_not_create_targeted_diagnostic_candidate", "review_materialization_does_not_create_new_retry_candidate",
    "review_materialization_does_not_create_retry_results_review", "review_materialization_does_not_create_integration_results_review",
    "review_materialization_does_not_mark_integration_successful", "review_materialization_does_not_generate_successful_integration_digest",
    "review_materialization_does_not_claim_failure_error_separation", "review_materialization_does_not_claim_first_failure",
    "review_materialization_does_not_claim_first_error", "review_materialization_does_not_claim_traceback_root_cause",
    "review_materialization_does_not_recommend_direct_code_remediation", "review_materialization_does_not_treat_digest_as_payload",
    "review_materialization_does_not_treat_detail_as_retry_success", "review_materialization_does_not_push_integration_branch",
    "review_materialization_does_not_push_main", "review_materialization_does_not_delete_integration_branch",
    "review_materialization_does_not_delete_worktree", "review_materialization_does_not_force_push",
    "review_materialization_does_not_prune_remotes", "review_materialization_does_not_modify_tags",
    "review_materialization_does_not_modify_staged_evidence", "review_materialization_does_not_regenerate_evidence",
    "review_materialization_does_not_call_providers", "review_materialization_does_not_acquire_market_data",
    "review_materialization_does_not_regenerate_dataset", "review_materialization_does_not_recompute_metrics",
    "review_materialization_does_not_train_models", "review_materialization_does_not_score_strategy",
    "review_materialization_does_not_generate_recommendations", "review_materialization_does_not_accept_predictive_usefulness",
    "review_materialization_does_not_accept_profitability", "review_materialization_does_not_authorize_runtime",
    "review_materialization_does_not_authorize_broker_execution",
    "complete_detail_materialization_output_would_be_planning_source_not_root_cause",
    "digest_only_is_not_complete_detail_payload", "top_five_only_is_not_complete_29_row_source",
    "complete_detail_gap_is_not_retry_success", "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_approval_required_before_materialization_execution", "separate_results_review_required_after_materialization",
    "separate_detail_binding_reattempt_required_after_materialization_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "ready_for_complete_29_row_materialization_approval", "materialization_package_selected",
    "materialization_package_approved", "materialization_package_authorized", "materialization_package_executed",
    "complete_29_row_detail_materialized", "complete_29_row_detail_exposed", "complete_29_row_detail_bound",
    "complete_29_row_detail_committed_source_created", "module_grouping_detail_materialized_by_review",
    "module_paths_recovered_by_review", "per_module_counts_recovered_by_review", "bounded_nodeid_samples_recovered_by_review",
    "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "source_recovery_rerun_performed", "cache_read_in_review", "module_grouping_recovered_in_review",
    "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
    "diagnostic_method_executed", "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_review", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError(ValueError):
    """Raised when the review violates its candidate-only boundary."""


def _committed_source_candidate() -> dict[str, Any]:
    return source.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1()


def _validate_source(candidate: Mapping[str, Any]) -> None:
    source.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(dict(candidate))
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest"
    if candidate.get(digest_key) != SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError("source candidate digest mismatch")


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = review.get("reviewed_materialization_or_binding_packages", [])
    blocked = [item for item in packages if item.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED"]
    pairs: dict[str, tuple[Any, Any]] = {
        "source_candidate_digest_bound": (SOURCE_CANDIDATE_DIGEST, review.get("source_complete_29_row_materialization_candidate_digest")),
        "source_diagnosis_digest_bound": (source.SOURCE_DIAGNOSIS_DIGEST, review.get("source_detail_exposure_or_binding_execution_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (source.PRIMARY_FAILURE_CLASS, review.get("primary_failure_class")),
        "source_detail_binding_execution_blocked_digest_bound": (source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, review.get("source_detail_exposure_or_binding_execution_blocked_digest")),
        "source_detail_binding_execution_blocked_manifest_digest_bound": (source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, review.get("source_detail_exposure_or_binding_execution_blocked_manifest_digest")),
        "source_detail_binding_execution_blocked_reason_bound": (source.source.SOURCE_BLOCKED_REASON, review.get("blocked_reason")),
        "source_detail_binding_approval_digest_bound": (source.source.SOURCE_APPROVAL_DIGEST, review.get("source_detail_exposure_or_binding_approval_digest")),
        "source_detail_binding_operator_review_digest_bound": (source.source.SOURCE_OPERATOR_REVIEW_DIGEST, review.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_detail_binding_candidate_digest_bound": (source.source.SOURCE_CANDIDATE_DIGEST, review.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_reentry_failure_diagnosis_digest_bound": (source.source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST, review.get("source_reentry_failure_diagnosis_digest")),
        "source_reentry_failure_primary_failure_class_bound": (source.source.SOURCE_PRIMARY_FAILURE_CLASS, review.get("source_primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (source.source.SOURCE_REENTRY_BLOCKED_DIGEST, review.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (source.source.SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST, review.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (source.source.SOURCE_REENTRY_BLOCKED_REASON, review.get("source_reentry_execution_blocked_reason")),
        "source_planning_reentry_digest_bound": (source.source.SOURCE_PLANNING_REENTRY_DIGEST, review.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, review.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.source.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST, review.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.source.SOURCE_RECOVERY_EXECUTION_DIGEST, review.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.source.SOURCE_RECOVERY_DETAIL_DIGEST, review.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST, review.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST, review.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST, review.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST, review.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, review.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.SOURCE_EXECUTION_V2_DIGEST, review.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.SOURCE_MODULE_GROUPING_DIGEST, review.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (source.source.RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": ({"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]}, review.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (source.TOP_FIVE, review.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, review.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, review.get("top_10_count_sum")),
        "available_data_recorded": (source.AVAILABLE_DATA, review.get("source_execution_available_data")),
        "missing_data_recorded": (source.MISSING_DATA, review.get("source_execution_missing_data")),
        "actual_live_detail_binding_source_lacks_complete_29_rows_true": (True, review.get("actual_live_detail_binding_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, review.get("detail_binding_success_path_tested_with_complete_29_row_snapshot")),
        "recommended_package_from_diagnosis_bound": (RECOMMENDED_PACKAGE, review.get("recommended_next_package_from_diagnosis")),
        "review_created_true": (True, review.get("complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_created")),
        "review_ready_true": (True, review.get("complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_ready")),
        "packages_reviewed_true": (True, review.get("materialization_packages_reviewed")),
        "future_requirements_reviewed_true": (True, review.get("future_materialization_or_binding_requirements_reviewed")),
        "future_plan_reviewed_true": (True, review.get("future_materialization_or_binding_plan_reviewed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "non_goals_reviewed_true": (True, review.get("non_goals_reviewed")),
        "ready_for_approval_false": (False, review.get("ready_for_complete_29_row_materialization_approval")),
        "recommended_package_reviewed_not_selected": (False, review.get("recommendation", {}).get("selected")),
        "packages_reviewed_12": (12, len(packages)), "blocked_packages_reviewed_6": (6, len(blocked)),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")), "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
    }
    pairs.update({f"{field}_false": (False, review.get(field)) for field in FALSE_BOUNDARIES})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    keys = [
        "complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_created",
        "complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_ready",
        "materialization_packages_reviewed", "recommended_complete_29_row_materialization_package",
        "ready_for_complete_29_row_materialization_approval", "materialization_package_selected",
        "materialization_package_approved", "materialization_package_executed", "complete_29_row_detail_materialized",
        "complete_29_row_detail_exposed", "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
        "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
        "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful", "recommended_next_task",
    ]
    result = {"total_checks": len(checklist), "passed_checks": len(checklist) - len(failed), "failed_checks": len(failed), "blocker_count": len(failed)}
    result.update({key: review.get(key) for key in keys})
    result["recommended_package_selected"] = review.get("recommendation", {}).get("selected")
    result.update({"predictive_usefulness_accepted": False, "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False})
    return result


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build an offline review without package selection or materialization."""

    candidate = deepcopy(source_candidate) if source_candidate is not None else _committed_source_candidate()
    _validate_source(candidate)
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest"
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_complete_29_row_materialization_candidate_artifact_kind": candidate["artifact_kind"],
        "source_complete_29_row_materialization_candidate_status": candidate["candidate_status"],
        "source_complete_29_row_materialization_candidate_scope": candidate["candidate_scope"],
        "source_complete_29_row_materialization_candidate_digest": candidate[digest_key],
        "source_detail_exposure_or_binding_execution_failure_diagnosis_digest": candidate["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"],
        "primary_failure_class": candidate["primary_failure_class"],
        "recommended_next_package_from_diagnosis": candidate["recommended_next_package_from_diagnosis"],
    }
    copied_fields = [
        "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_detail_exposure_or_binding_execution_blocked_manifest_digest", "blocked_reason",
        "source_detail_exposure_or_binding_approval_digest", "source_detail_exposure_or_binding_operator_review_digest",
        "source_detail_exposure_or_binding_candidate_digest", "source_reentry_failure_diagnosis_digest",
        "source_primary_failure_class", "source_reentry_execution_blocked_digest",
        "source_reentry_execution_blocked_manifest_digest", "source_reentry_execution_blocked_reason",
        "source_after_v2_planning_reentry_digest", "source_module_grouping_source_recovery_results_review_digest",
        "source_module_grouping_source_recovery_results_review_manifest_digest",
        "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest",
        "source_module_grouping_source_recovery_digest_manifest_digest",
        "source_module_grouping_source_recovery_approval_digest", "source_module_grouping_source_recovery_operator_review_digest",
        "source_module_grouping_source_recovery_candidate_digest", "source_blocked_after_v2_execution_digest",
        "source_blocked_after_v2_manifest_digest", "source_after_v2_approval_digest",
        "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest", "source_results_review_v2_digest",
        "source_execution_v2_digest", "source_module_grouping_digest", "source_approval_v2_digest",
        "source_staged_inventory_digest", "retry_execution_commit", "retry_failure_context",
        "recovered_module_grouping_source_summary", "top_module_summary", "top_5_count_sum", "top_10_count_sum",
        "source_execution_available_data", "source_execution_missing_data",
        "actual_live_detail_binding_source_lacks_complete_29_rows",
        "detail_binding_success_path_tested_with_complete_29_row_snapshot",
    ]
    review.update({key: deepcopy(candidate[key]) for key in copied_fields})
    review.update({
        "retry_execution_branch": candidate["retry_execution_branch"],
        "retry_pytest_working_directory": candidate["retry_pytest_working_directory"],
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
        "top_5_percentage_of_failed_or_errored_nodeids": candidate["top_5_percentage_of_failed_or_errored_nodeids"],
        "top_10_percentage_of_failed_or_errored_nodeids": candidate["top_10_percentage_of_failed_or_errored_nodeids"],
        "diagnosis_findings_summary": deepcopy(candidate["diagnosis_findings_summary"]),
        "reviewed_complete_29_row_materialization_candidate_philosophy": source.CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": "Candidate reviewed only; no materialization, detail exposure, cache read, source recovery, planning reentry, diagnostics, remediation, retry, results review, main merge, runtime, or trading authority is created.",
        "reviewed_candidate_goal": "Review safe future packages to materialize, expose, or bind the complete 29-row recovered module grouping source required for deterministic planning reentry.",
        "candidate_philosophy_review_status": REVIEWED_PLANNING_ONLY,
        "reviewed_materialization_or_binding_packages": _reviewed_packages(),
        "reviewed_future_materialization_or_binding_requirements": deepcopy(REVIEWED_REQUIREMENTS),
        "reviewed_future_materialization_or_binding_plan": deepcopy(REVIEWED_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": {
            "package": RECOMMENDED_PACKAGE, "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "selected": False,
            "reason": "The candidate is reviewed, but no materialization package has been selected or approved by this review.",
        },
        "recommended_complete_29_row_materialization_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_created": True,
        "complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_ready": True,
        "materialization_packages_reviewed": True, "future_materialization_or_binding_requirements_reviewed": True,
        "future_materialization_or_binding_plan_reviewed": True, "planned_outputs_reviewed": True,
        "non_goals_reviewed": True,
        "source_complete_29_row_materialization_candidate_created": True,
        "source_complete_29_row_materialization_candidate_ready_for_operator_review": True,
        "origin_main_commit": candidate["origin_main_commit"], "integration_branch_name": candidate["integration_branch_name"],
        "integration_branch_head_commit": candidate["integration_branch_head_commit"],
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": candidate["detached_integration_worktree_path"],
        "detached_integration_worktree_head_commit": candidate["detached_integration_worktree_head_commit"],
        "staged_evidence_manifest_digest": candidate["staged_evidence_manifest_digest"], "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False, "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False, "pytest_cache_tracked_in_detached_worktree": False,
        "failure_modules_classified": False, "error_modules_classified": False,
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "direct_code_remediation_recommended": False,
        "retry_success_claimed": False, "main_merge_readiness_claimed": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    })
    review.update({key: False for key in FALSE_BOUNDARIES})
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review_digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_digest"
    review[review_digest_key] = _review_digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(
    review: dict,
) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError("review must be object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "source_complete_29_row_materialization_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_complete_29_row_materialization_candidate_status": source.CANDIDATE_STATUS,
        "source_complete_29_row_materialization_candidate_scope": source.CANDIDATE_SCOPE,
    }
    for field, expected in fixed.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError(f"{field} mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError("checklist invalid")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError("summary invalid")
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_digest"
    digest = review.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _review_digest(review):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError("operator-review digest invalid")
    return {
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"], "operator_review_digest": digest,
        **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(review)
    sections = [
        ("Source Complete 29-row Materialization Candidate", [SOURCE_CANDIDATE_DIGEST, source.CANDIDATE_STATUS]),
        ("Source Execution Failure Diagnosis", [source.SOURCE_DIAGNOSIS_DIGEST, source.PRIMARY_FAILURE_CLASS]),
        ("Source Blocked Detail Exposure or Binding Execution", [source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, source.source.SOURCE_BLOCKED_REASON]),
        ("Source Approval and Operator Review", [source.source.SOURCE_APPROVAL_DIGEST, source.source.SOURCE_OPERATOR_REVIEW_DIGEST]),
        ("Source Reentry Failure Diagnosis", [source.source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST]),
        ("Source Recovery Results Review", [source.source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, source.source.SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; first retry result remains authoritative."]),
        ("Recovered Module Grouping Source Summary", [str(review["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Detail Source", [*source.AVAILABLE_DATA, *source.MISSING_DATA]),
        ("Review Scope", [REVIEW_SCOPE, review["reviewed_candidate_boundary"]]),
        ("Reviewed Candidate Philosophy", [review["reviewed_complete_29_row_materialization_candidate_philosophy"]]),
        ("Reviewed Materialization or Binding Packages", [f"{item['package']}: {item['review_status']}" for item in review["reviewed_materialization_or_binding_packages"]]),
        ("Reviewed Future Materialization or Binding Requirements", [item["requirement_id"] for item in review["reviewed_future_materialization_or_binding_requirements"]]),
        ("Reviewed Future Materialization or Binding Plan", [item["step"] for item in review["reviewed_future_materialization_or_binding_plan"]]),
        ("Reviewed Planned Outputs", [item["output_id"] for item in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [item["non_goal_id"] for item in review["reviewed_non_goals"]]),
        ("Recommendation", [RECOMMENDED_PACKAGE, RECOMMENDED_ACTION, RECOMMENDED_NEXT_TASK]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["Review only: no selection, approval, materialization, cache read, binding, planning, retry, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["A reviewed recommendation is not selection or approval; a digest is not row payload."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Candidate Operator Review v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    review = build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(source_candidate=source_candidate)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1.md"
    json_path.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_markdown_v1(review),
        encoding="utf-8",
    )
    return {"artifact": review, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_markdown_v1",
]
