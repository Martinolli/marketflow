"""Review the diagnostic receipt recovery-or-recapture candidate offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_digest"
SOURCE_CANDIDATE_DIGEST = "a3312f96a90cb8cefdd826ac14aa2ff9d4335a4e9ed9869e3589227fb3711041"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

REVIEWED_PHILOSOPHY = {
    "reviewed_receipt_recovery_or_recapture_candidate_philosophy": (
        "The approved targeted diagnostic command executed once and transiently succeeded, but the durable "
        "success receipt was lost by a post-capture reporting wrapper failure. The candidate correctly defines "
        "governed future options for either recovering an already-existing durable receipt, binding a hash-verifiable "
        "operator-provided transcript, or approving a controlled single recapture with pre-command persistence "
        "safeguards. The operator review must not rerun diagnostics, reconstruct missing values, infer output hashes, "
        "or proceed to remediation or retry without reviewed diagnostic evidence."
    ),
    "reviewed_candidate_boundary": (
        "Operator-review only; no receipt recovery, recapture, diagnostic command, targeted pytest, remediation, "
        "classification, retry, results review, main merge, runtime, or trading authority is created."
    ),
    "reviewed_candidate_goal": "Review safe future packages to recover or recapture durable diagnostic evidence after receipt loss.",
    "review_status": "REVIEWED_PLANNING_ONLY",
}

PACKAGE_REVIEW_STATUSES = [
    "REVIEWED_AVAILABLE_LOW_CONFIDENCE_NOT_SELECTED",
    "REVIEWED_AVAILABLE_NOT_SELECTED",
    "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
    "REVIEWED_AVAILABLE_NOT_SELECTED",
    *("REVIEWED_BLOCKED_NOT_ALLOWED" for _ in range(7)),
]
REVIEWED_PACKAGES = [
    {
        "package_id": package["package_id"],
        "source_status": package["status"],
        "review_status": review_status,
        "selected": False,
        "approved": False,
        "executed": False,
        **({"purpose": package["purpose"]} if "purpose" in package else {}),
        **({"blocked_reason": package["blocked_reason"]} if "blocked_reason" in package else {}),
        **({"recommended_reason": package["recommended_reason"]} if "recommended_reason" in package else {}),
    }
    for package, review_status in zip(source.PROPOSED_PACKAGES, PACKAGE_REVIEW_STATUSES, strict=True)
]
REVIEWED_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_RECEIPT_RECOVERY_OR_RECAPTURE",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_REQUIREMENTS
]
REVIEWED_PLAN = [
    {
        "step_id": index,
        "step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_PLAN["steps"], start=1)
]
REVIEWED_COMMAND_TEMPLATE = {
    "future_recapture_command_template_review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
    **deepcopy(source.FUTURE_COMMAND_TEMPLATE),
}
REVIEWED_SAFEGUARDS = [
    {
        "safeguard_id": safeguard_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_CONTROLLED_RECAPTURE",
        "execution_status": "NOT_EXECUTED",
    }
    for safeguard_id in source.FUTURE_RECEIPT_SAFEGUARDS
]
REVIEWED_OUTPUTS = [
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

PACKAGE_RECOMMENDATION = {
    "recommended_receipt_recovery_or_recapture_package": RECOMMENDED_PACKAGE,
    "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
    "reason": (
        "The source diagnosis confirms a single permitted diagnostic run occurred and transiently succeeded, but "
        "durable output receipt fields were lost after capture. The reviewed candidate’s strongest mitigation is a "
        "controlled single recapture with a prewritten receipt scaffold, cacheprovider disabled, bounded output, "
        "stream hashes, redaction, and no retry-success claim."
    ),
}
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_V1_IF_SELECTED"
RECOMMENDATION = {
    "recommended_next_task": NEXT_TASK,
    "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
    "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_RECEIPT_RECOVERY_OR_CONTROLLED_RECAPTURE_EXECUTION",
    "ready_for_receipt_recovery_or_recapture_approval": False,
    "ready_for_receipt_recovery_or_recapture_execution": False,
    "ready_for_diagnostic_results_review": False,
    "ready_for_remediation_or_method_candidate": False,
    "ready_for_retry_candidate": False,
    "reason": (
        "The receipt recovery or recapture candidate has been reviewed, but no recovery or recapture package has "
        "been selected or approved by this review. Controlled recapture or receipt recovery requires a separate "
        "approval ceremony."
    ),
}

NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Receipt Recovery or Recapture Approval v1, if selected.",
    "Receipt Recovery or Controlled Recapture Execution v1, if approved.",
    "Receipt Recovery or Controlled Recapture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if supported by results review.",
    "Remediation or Method Operator Review v1, if needed.",
    "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.",
    "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_if_selected",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_if_approved",
    "targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_supported",
    "remediation_or_method_operator_review_if_needed",
    "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved",
    "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "operator_review_receipt_recovery_does_not_select_package",
    "operator_review_receipt_recovery_does_not_approve_package",
    "operator_review_receipt_recovery_does_not_authorize_package",
    "operator_review_receipt_recovery_does_not_recover_receipt",
    "operator_review_receipt_recovery_does_not_execute_recapture",
    "operator_review_receipt_recovery_does_not_run_diagnostic_command",
    "operator_review_receipt_recovery_does_not_run_targeted_pytest",
    "operator_review_receipt_recovery_does_not_run_full_pytest",
    "operator_review_receipt_recovery_does_not_rerun_retry",
    "operator_review_receipt_recovery_does_not_read_cache",
    "operator_review_receipt_recovery_does_not_modify_cache",
    "operator_review_receipt_recovery_does_not_search_transient_memory",
    "operator_review_receipt_recovery_does_not_parse_terminal_logs",
    "operator_review_receipt_recovery_does_not_parse_operator_logs",
    "operator_review_receipt_recovery_does_not_inspect_env",
    "operator_review_receipt_recovery_does_not_reconstruct_stdout_hash",
    "operator_review_receipt_recovery_does_not_reconstruct_stderr_hash",
    "operator_review_receipt_recovery_does_not_reconstruct_exit_code",
    "operator_review_receipt_recovery_does_not_reconstruct_excerpts",
    "operator_review_receipt_recovery_does_not_infer_missing_payload",
    "operator_review_receipt_recovery_does_not_execute_remediation",
    "operator_review_receipt_recovery_does_not_execute_classification",
    "operator_review_receipt_recovery_does_not_classify_modules_again",
    "operator_review_receipt_recovery_does_not_identify_first_failure",
    "operator_review_receipt_recovery_does_not_identify_first_error",
    "operator_review_receipt_recovery_does_not_claim_traceback_root_cause",
    "operator_review_receipt_recovery_does_not_recommend_direct_code_remediation",
    "operator_review_receipt_recovery_does_not_create_diagnostic_results_review",
    "operator_review_receipt_recovery_does_not_create_remediation_or_method_candidate",
    "operator_review_receipt_recovery_does_not_create_new_retry_candidate",
    "operator_review_receipt_recovery_does_not_create_retry_results_review",
    "operator_review_receipt_recovery_does_not_create_integration_results_review",
    "operator_review_receipt_recovery_does_not_mark_integration_successful",
    "operator_review_receipt_recovery_does_not_generate_successful_integration_digest",
    "operator_review_receipt_recovery_does_not_treat_transient_success_as_durable_success",
    "operator_review_receipt_recovery_does_not_treat_diagnostic_run_as_retry",
    "operator_review_receipt_recovery_does_not_push_integration_branch",
    "operator_review_receipt_recovery_does_not_push_main",
    "operator_review_receipt_recovery_does_not_delete_integration_branch",
    "operator_review_receipt_recovery_does_not_delete_worktree",
    "operator_review_receipt_recovery_does_not_force_push",
    "operator_review_receipt_recovery_does_not_prune_remotes",
    "operator_review_receipt_recovery_does_not_modify_tags",
    "operator_review_receipt_recovery_does_not_modify_staged_evidence",
    "operator_review_receipt_recovery_does_not_regenerate_evidence",
    "operator_review_receipt_recovery_does_not_call_providers",
    "operator_review_receipt_recovery_does_not_acquire_market_data",
    "operator_review_receipt_recovery_does_not_regenerate_dataset",
    "operator_review_receipt_recovery_does_not_recompute_metrics",
    "operator_review_receipt_recovery_does_not_train_models",
    "operator_review_receipt_recovery_does_not_score_strategy",
    "operator_review_receipt_recovery_does_not_generate_recommendations",
    "operator_review_receipt_recovery_does_not_accept_predictive_usefulness",
    "operator_review_receipt_recovery_does_not_accept_profitability",
    "operator_review_receipt_recovery_does_not_authorize_runtime",
    "operator_review_receipt_recovery_does_not_authorize_broker_execution",
    "operator_review_output_is_planning_only_not_recovery_execution",
    "future_recapture_requires_separate_approval",
    "future_recapture_must_prewrite_durable_receipt_before_command",
    "future_recapture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation",
    "blocked_execution_remains_historically_blocked",
    "single_permitted_diagnostic_run_acknowledged_but_not_accepted_as_durable_success",
    "previous_receipt_recovery_candidate_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence",
    "previous_approval_remains_source_evidence",
    "previous_operator_review_remains_source_evidence",
    "previous_candidate_remains_source_evidence",
    "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_approval_required_before_receipt_recovery_or_recapture",
    "separate_results_review_required_after_receipt_recovery_or_recapture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "receipt_recovery_or_recapture_candidate_operator_review_created",
    "receipt_recovery_or_recapture_candidate_operator_review_ready",
    "source_candidate_reviewed",
    "source_failure_diagnosis_reviewed",
    "receipt_loss_failure_class_reviewed",
    "unavailable_payload_fields_reviewed",
    "future_receipt_recovery_or_recapture_packages_reviewed",
    "future_receipt_recovery_requirements_reviewed",
    "future_controlled_recapture_requirements_reviewed",
    "future_recovery_or_recapture_plan_reviewed",
    "future_controlled_recapture_command_template_reviewed",
    "future_durable_receipt_safeguards_reviewed",
    "planned_outputs_reviewed",
    "non_goals_reviewed",
    "diagnostic_command_executed_once",
    "transient_success_artifact_returned",
]
FALSE_FIELDS = [
    "durable_success_receipt_retained",
    "diagnostic_exit_code_available", "diagnostic_duration_seconds_available", "stdout_hash_available",
    "stderr_hash_available", "stdout_byte_count_available", "stderr_byte_count_available",
    "combined_output_byte_count_available", "bounded_stdout_excerpt_available", "bounded_stderr_excerpt_available",
    "redaction_patterns_available", "success_payload_digest_available", "success_digest_manifest_digest_available",
    "diagnostic_command_rerun_to_recover_values",
    "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_package_authorized",
    "receipt_recovery_execution_performed", "receipt_recovered", "controlled_recapture_package_selected",
    "controlled_recapture_package_approved", "controlled_recapture_package_authorized",
    "controlled_recapture_execution_performed", "diagnostic_command_executed_in_review",
    "diagnostic_output_captured_in_review", "targeted_pytest_performed", "full_pytest_performed",
    "retry_rerun_performed", "ready_for_receipt_recovery_or_recapture_approval",
    "ready_for_receipt_recovery_or_recapture_execution", "ready_for_diagnostic_results_review",
    "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate", "diagnostic_results_review_created",
    "remediation_or_method_candidate_after_diagnostic_capture_created", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "cache_read_in_review", "cache_modified_in_review", "operator_logs_parsed", "terminal_logs_parsed",
    "env_inspection_performed", "unavailable_values_reconstructed", "unavailable_values_inferred",
    "classification_execution_performed_in_review", "remediation_execution_performed", "failure_modules_classified",
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

SOURCE_BINDINGS = {
    "source_receipt_recovery_or_recapture_candidate_digest": SOURCE_CANDIDATE_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError(ValueError):
    """Raised when the review drifts or opens prohibited authority."""


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


def _source_candidate_summary() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND,
        "candidate_status": source.CANDIDATE_STATUS,
        "candidate_scope": source.CANDIDATE_SCOPE,
        source.DIGEST_KEY: SOURCE_CANDIDATE_DIGEST,
        "recommended_receipt_recovery_or_recapture_package": RECOMMENDED_PACKAGE,
        "receipt_recovery_or_recapture_candidate_created": True,
        "receipt_recovery_or_recapture_candidate_ready_for_operator_review": True,
        "source_failure_diagnosis_reviewed": True,
        "receipt_loss_failure_class_bound": True,
        "future_receipt_recovery_or_recapture_packages_defined": True,
        "future_receipt_recovery_requirements_defined": True,
        "future_controlled_recapture_requirements_defined": True,
        "future_persistence_guard_plan_defined": True,
        "ready_for_receipt_recovery_or_recapture_candidate_operator_review": True,
        "receipt_recovery_package_selected": False, "receipt_recovery_package_approved": False,
        "receipt_recovery_package_authorized": False, "receipt_recovery_execution_performed": False,
        "receipt_recovered": False, "controlled_recapture_package_selected": False,
        "controlled_recapture_package_approved": False, "controlled_recapture_package_authorized": False,
        "controlled_recapture_execution_performed": False,
        "ready_for_receipt_recovery_or_recapture_approval": False,
        "ready_for_receipt_recovery_or_recapture_execution": False,
        "ready_for_diagnostic_results_review": False,
        "ready_for_remediation_or_method_candidate": False,
        "ready_for_retry_candidate": False,
    }


def _bind_source_candidate(value: Mapping[str, Any] | None) -> dict[str, Any]:
    expected = _source_candidate_summary()
    if value is None:
        return deepcopy(expected)
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError("source candidate must be an object")
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(dict(value))
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError("source candidate validation failed") from exc
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError(f"source candidate {field} mismatch")
    return deepcopy(expected)


def _retry_context() -> dict[str, Any]:
    return {
        "retry_execution_branch": source.source.RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": source.source.source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": source.source.RETRY_PYTEST_WORKING_DIRECTORY,
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
    }


def _source_failure_summary() -> dict[str, Any]:
    diagnosis = source.source
    return {
        "artifact_kind": diagnosis.ARTIFACT_KIND,
        "diagnosis_status": diagnosis.DIAGNOSIS_STATUS,
        "diagnosis_scope": diagnosis.DIAGNOSIS_SCOPE,
        diagnosis.DIGEST_KEY: source.SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": diagnosis.PRIMARY_FAILURE_CLASS,
        "secondary_failure_class": diagnosis.SECONDARY_FAILURE_CLASS,
        "diagnostic_command_executed_once": True,
        "transient_success_artifact_returned": True,
        "durable_success_receipt_retained": False,
        "diagnostic_exit_code_available": False, "diagnostic_duration_seconds_available": False,
        "stdout_hash_available": False, "stderr_hash_available": False,
        "stdout_byte_count_available": False, "stderr_byte_count_available": False,
        "combined_output_byte_count_available": False, "bounded_stdout_excerpt_available": False,
        "bounded_stderr_excerpt_available": False, "redaction_patterns_available": False,
        "success_payload_digest_available": False, "success_digest_manifest_digest_available": False,
        "unavailable_diagnostic_payload_fields": list(source.UNAVAILABLE_FIELDS),
        "unavailable_values_reconstructed": False, "unavailable_values_inferred": False,
        "diagnostic_command_rerun_to_recover_values": False,
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_check_ids = {
        "source_receipt_recovery_or_recapture_candidate_digest": "source_candidate_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest": "source_failure_diagnosis_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_digest": "source_execution_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest": "source_blocked_manifest_digest_bound",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason": "source_blocked_reason_bound",
        "source_primary_failure_class": "source_primary_failure_class_bound",
        "source_secondary_failure_class": "source_secondary_failure_class_bound",
        "source_targeted_diagnostic_output_capture_approval_digest": "source_approval_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_operator_review_digest": "source_operator_review_digest_bound",
        "source_targeted_diagnostic_output_capture_candidate_digest": "source_targeted_diagnostic_candidate_digest_bound",
        "source_results_review_digest": "source_results_review_digest_bound",
        "source_prioritized_planning_review_digest": "source_prioritized_planning_review_digest_bound",
        "source_results_review_manifest_digest": "source_results_review_manifest_digest_bound",
        "source_planning_execution_digest": "source_planning_execution_digest_bound",
        "source_prioritized_planning_digest": "source_prioritized_planning_digest_bound",
        "source_planning_digest_manifest_digest": "source_planning_manifest_digest_bound",
        "source_detail_binding_results_review_digest": "source_detail_binding_results_review_digest_bound",
        "source_complete_29_row_binding_digest": "source_complete_29_row_binding_digest_bound",
        "source_materialized_payload_digest": "source_materialized_payload_digest_bound",
        "source_detail_binding_approval_digest": "source_detail_binding_approval_digest_bound",
        "source_recovery_results_review_digest": "source_recovery_results_review_digest_bound",
        "source_recovery_detail_digest": "source_recovery_detail_digest_bound",
        "source_after_v2_approval_digest": "source_after_v2_approval_digest_bound",
        "source_module_grouping_digest": "source_module_grouping_digest_bound",
    }
    checks = [_check(check_id, SOURCE_BINDINGS[field], review.get(field)) for field, check_id in source_check_ids.items()]
    checks.extend([
        _check("retry_execution_commit_bound", source.source.source.RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", _retry_context()["counts"], review.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", [x["module_path"] for x in source.PRIORITY_1_TARGET_MODULES], [x.get("module_path") for x in review.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("diagnostic_command_executed_once_acknowledged", True, review.get("diagnostic_command_executed_once")),
        _check("transient_success_acknowledged", True, review.get("transient_success_artifact_returned")),
        _check("durable_success_receipt_missing", False, review.get("durable_success_receipt_retained")),
        _check("unavailable_fields_reviewed", source.UNAVAILABLE_FIELDS, review.get("reviewed_unavailable_diagnostic_payload_fields")),
        _check("missing_values_not_reconstructed", False, review.get("unavailable_values_reconstructed")),
        _check("missing_values_not_inferred", False, review.get("unavailable_values_inferred")),
        _check("operator_review_created_true", True, review.get("receipt_recovery_or_recapture_candidate_operator_review_created")),
        _check("operator_review_ready_true", True, review.get("receipt_recovery_or_recapture_candidate_operator_review_ready")),
        _check("source_candidate_reviewed_true", True, review.get("source_candidate_reviewed")),
        _check("source_failure_diagnosis_reviewed_true", True, review.get("source_failure_diagnosis_reviewed")),
        _check("receipt_loss_failure_class_reviewed_true", True, review.get("receipt_loss_failure_class_reviewed")),
        _check("future_packages_reviewed", REVIEWED_PACKAGES, review.get("reviewed_receipt_recovery_or_recapture_packages")),
        _check("recommended_package_reviewed_not_selected", False, review.get("recommended_package_selected")),
        _check("packages_reviewed_11", 11, len(review.get("reviewed_receipt_recovery_or_recapture_packages", []))),
        _check("blocked_packages_reviewed_7", 7, sum(x.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for x in review.get("reviewed_receipt_recovery_or_recapture_packages", []))),
        _check("future_requirements_reviewed", REVIEWED_REQUIREMENTS, review.get("reviewed_future_receipt_recovery_or_recapture_requirements")),
        _check("future_plan_reviewed", REVIEWED_PLAN, review.get("reviewed_future_recovery_or_recapture_plan")),
        _check("future_recapture_command_template_reviewed_not_executed", REVIEWED_COMMAND_TEMPLATE, review.get("reviewed_future_controlled_recapture_command_template")),
        _check("future_durable_receipt_safeguards_reviewed", REVIEWED_SAFEGUARDS, review.get("reviewed_future_durable_receipt_safeguards")),
        _check("planned_outputs_reviewed", REVIEWED_OUTPUTS, review.get("reviewed_planned_outputs")),
        _check("non_goals_reviewed", REVIEWED_NON_GOALS, review.get("reviewed_non_goals")),
    ])
    false_aliases = {
        "receipt_recovery_package_selected": "receipt_recovery_package_selected_false",
        "receipt_recovery_package_approved": "receipt_recovery_package_approved_false",
        "receipt_recovery_package_authorized": "receipt_recovery_package_authorized_false",
        "receipt_recovery_execution_performed": "receipt_recovery_execution_false",
        "receipt_recovered": "receipt_recovered_false",
        "controlled_recapture_package_selected": "controlled_recapture_package_selected_false",
        "controlled_recapture_package_approved": "controlled_recapture_package_approved_false",
        "controlled_recapture_package_authorized": "controlled_recapture_package_authorized_false",
        "controlled_recapture_execution_performed": "controlled_recapture_execution_false",
        "diagnostic_command_executed_in_review": "diagnostic_command_executed_in_review_false",
        "diagnostic_output_captured_in_review": "diagnostic_output_captured_in_review_false",
        "targeted_pytest_performed": "targeted_pytest_false", "full_pytest_performed": "full_pytest_false",
        "retry_rerun_performed": "retry_rerun_false", "cache_read_in_review": "cache_read_false",
        "cache_modified_in_review": "cache_modified_false", "terminal_logs_parsed": "terminal_logs_parsed_false",
        "operator_logs_parsed": "operator_logs_parsed_false", "env_inspection_performed": "env_inspection_false",
        "unavailable_values_reconstructed": "unavailable_values_reconstructed_false",
        "unavailable_values_inferred": "unavailable_values_inferred_false",
        "diagnostic_results_review_created": "diagnostic_results_review_created_false",
        "remediation_or_method_candidate_after_diagnostic_capture_created": "remediation_or_method_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false", "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false",
        "classification_execution_performed_in_review": "classification_execution_false",
        "remediation_execution_performed": "remediation_execution_false",
        "failure_modules_classified": "failure_modules_classified_false",
        "error_modules_classified": "error_modules_classified_false",
        "failure_error_separation_claimed": "failure_error_separation_claimed_false",
        "first_failure_identified": "first_failure_identified_false", "first_error_identified": "first_error_identified_false",
        "first_order_claim_made": "first_order_claim_made_false", "traceback_root_cause_claimed": "traceback_root_cause_claimed_false",
        "direct_code_remediation_recommended": "direct_code_remediation_recommended_false",
        "retry_success_claimed": "retry_success_claimed_false", "main_merge_readiness_claimed": "main_merge_readiness_claimed_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false",
        "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false", "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_review": "provider_requests_false",
        "market_data_acquisition_performed_in_review": "market_data_acquisition_false",
        "dataset_generation_performed_in_review": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    checks.extend(_check(check_id, False, review.get(field)) for field, check_id in false_aliases.items())
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("recommendation_defined", RECOMMENDATION, review.get("recommendation")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        _check("no_tracked_marketflow_files", False, review.get("marketflow_outputs_committed")),
        _check("no_tracked_pytest_cache_files", False, review.get("pytest_cache_committed")),
    ])
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    fields = [
        "receipt_recovery_or_recapture_candidate_operator_review_created",
        "receipt_recovery_or_recapture_candidate_operator_review_ready", "source_candidate_reviewed",
        "source_failure_diagnosis_reviewed", "receipt_loss_failure_class_reviewed", "unavailable_payload_fields_reviewed",
        "recommended_receipt_recovery_or_recapture_package", "recommended_package_selected",
        "receipt_recovery_package_selected", "receipt_recovery_package_approved", "receipt_recovery_execution_performed",
        "receipt_recovered", "controlled_recapture_package_selected", "controlled_recapture_package_approved",
        "controlled_recapture_execution_performed", "diagnostic_command_executed_in_review",
        "diagnostic_output_captured_in_review", "targeted_pytest_performed", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed_once", "transient_success_artifact_returned",
        "durable_success_receipt_retained", "unavailable_values_reconstructed", "unavailable_values_inferred",
        "ready_for_receipt_recovery_or_recapture_approval", "ready_for_receipt_recovery_or_recapture_execution",
        "ready_for_diagnostic_results_review", "ready_for_remediation_or_method_candidate", "ready_for_retry_candidate",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "priority_1_total_nodeids", "top_10_count_sum",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed, **{field: review.get(field) for field in fields},
        "priority_1_top_module_count": 5,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    value = deepcopy(dict(review))
    for field in ("checklist", "summary", DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build a review without selecting, approving, recovering, or recapturing."""

    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_receipt_recovery_or_recapture_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_receipt_recovery_or_recapture_candidate_status": source.CANDIDATE_STATUS,
        "source_receipt_recovery_or_recapture_candidate_scope": source.CANDIDATE_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "source_candidate_summary": _bind_source_candidate(source_candidate),
        "source_failure_diagnosis_summary": _source_failure_summary(),
        "source_execution_blocked_summary": {
            "execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
            "blocked_manifest_digest": source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
            "blocked_reason": source.source.SOURCE_BLOCKED_REASON,
        },
        "retry_execution_commit": source.source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": _retry_context(),
        "reviewed_receipt_loss_summary": {
            "primary_failure_class": source.source.PRIMARY_FAILURE_CLASS,
            "secondary_failure_class": source.source.SECONDARY_FAILURE_CLASS,
            "diagnostic_command_executed_once": True,
            "transient_success_artifact_returned": True,
            "durable_success_receipt_retained": False,
            "unavailable_values_reconstructed": False,
            "unavailable_values_inferred": False,
        },
        "reviewed_unavailable_diagnostic_payload_fields": list(source.UNAVAILABLE_FIELDS),
        "priority_1_target_modules": deepcopy(source.PRIORITY_1_TARGET_MODULES),
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "reviewed_candidate_philosophy": deepcopy(REVIEWED_PHILOSOPHY),
        "reviewed_receipt_recovery_or_recapture_packages": deepcopy(REVIEWED_PACKAGES),
        "recommended_package": deepcopy(PACKAGE_RECOMMENDATION),
        "recommended_receipt_recovery_or_recapture_package": RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
        "reviewed_future_receipt_recovery_or_recapture_requirements": deepcopy(REVIEWED_REQUIREMENTS),
        "reviewed_future_recovery_or_recapture_plan": deepcopy(REVIEWED_PLAN),
        "reviewed_future_controlled_recapture_command_template": deepcopy(REVIEWED_COMMAND_TEMPLATE),
        "reviewed_future_durable_receipt_safeguards": deepcopy(REVIEWED_SAFEGUARDS),
        "reviewed_planned_outputs": deepcopy(REVIEWED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": deepcopy(RECOMMENDATION),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[DIGEST_KEY] = _review_digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Reject source drift, missing review evidence, or authority expansion."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    constants = {
        **SOURCE_BINDINGS,
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_receipt_recovery_or_recapture_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_receipt_recovery_or_recapture_candidate_status": source.CANDIDATE_STATUS,
        "source_receipt_recovery_or_recapture_candidate_scope": source.CANDIDATE_SCOPE,
        "retry_execution_commit": source.source.source.RETRY_EXECUTION_COMMIT,
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "recommended_receipt_recovery_or_recapture_package": RECOMMENDED_PACKAGE,
        "recommended_package_selected": False,
    }
    for field, expected in constants.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    structures = {
        "source_candidate_summary": _source_candidate_summary(),
        "source_failure_diagnosis_summary": _source_failure_summary(),
        "source_execution_blocked_summary": {
            "execution_digest": source.source.SOURCE_EXECUTION_DIGEST,
            "blocked_manifest_digest": source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
            "blocked_reason": source.source.SOURCE_BLOCKED_REASON,
        },
        "retry_failure_context": _retry_context(),
        "reviewed_receipt_loss_summary": {
            "primary_failure_class": source.source.PRIMARY_FAILURE_CLASS,
            "secondary_failure_class": source.source.SECONDARY_FAILURE_CLASS,
            "diagnostic_command_executed_once": True, "transient_success_artifact_returned": True,
            "durable_success_receipt_retained": False, "unavailable_values_reconstructed": False,
            "unavailable_values_inferred": False,
        },
        "reviewed_unavailable_diagnostic_payload_fields": source.UNAVAILABLE_FIELDS,
        "priority_1_target_modules": source.PRIORITY_1_TARGET_MODULES,
        "reviewed_candidate_philosophy": REVIEWED_PHILOSOPHY,
        "reviewed_receipt_recovery_or_recapture_packages": REVIEWED_PACKAGES,
        "recommended_package": PACKAGE_RECOMMENDATION,
        "reviewed_future_receipt_recovery_or_recapture_requirements": REVIEWED_REQUIREMENTS,
        "reviewed_future_recovery_or_recapture_plan": REVIEWED_PLAN,
        "reviewed_future_controlled_recapture_command_template": REVIEWED_COMMAND_TEMPLATE,
        "reviewed_future_durable_receipt_safeguards": REVIEWED_SAFEGUARDS,
        "reviewed_planned_outputs": REVIEWED_OUTPUTS,
        "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommendation": RECOMMENDATION,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in structures.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise error("reviewed fact missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed boundary opened")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(review.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime boundary changed")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    digest = review.get(DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _review_digest(review):
        raise error("operator review digest mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write deterministic review JSON outside protected runtime paths."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(source_candidate=source_candidate)
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS,
        "operator_review_digest": review[DIGEST_KEY], "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized review summary after strict validation."""

    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(review)
    sections = [
        ("Source Receipt Recovery or Recapture Candidate", f"Digest: `{SOURCE_CANDIDATE_DIGEST}`; status: `{source.CANDIDATE_STATUS}`."),
        ("Source Failure Diagnosis", f"Digest: `{source.SOURCE_DIAGNOSIS_DIGEST}`; primary class: `{source.source.PRIMARY_FAILURE_CLASS}`."),
        ("Source Targeted Diagnostic Output Capture Execution", f"The source execution remains blocked: `{source.source.SOURCE_BLOCKED_REASON}`."),
        ("Source Approval and Operator Review", "The prior approval, operator-review, and candidate digests remain immutable source bindings."),
        ("Source Planning and Detail Binding Evidence", "Planning, detail-binding, materialization, and recovery evidence remain immutable source bindings."),
        ("Retry Failure Context", "24,877 passed; 1,292 failed; 112 errors; 7 skipped. The failed retry remains authoritative."),
        ("Review Scope", f"`{REVIEW_SCOPE}`"),
        ("Receipt Loss Summary", "One permitted diagnostic run transiently succeeded; its durable success receipt was not retained."),
        ("Unavailable Diagnostic Payload Fields", ", ".join(f"`{item}`" for item in source.UNAVAILABLE_FIELDS)),
        ("Priority 1 Target Modules", "\n".join(f"- `{item['module_path']}`: {item['failed_or_errored_nodeid_count']}" for item in source.PRIORITY_1_TARGET_MODULES)),
        ("Reviewed Candidate Philosophy", REVIEWED_PHILOSOPHY["reviewed_receipt_recovery_or_recapture_candidate_philosophy"]),
        ("Reviewed Receipt Recovery or Recapture Packages", "\n".join(f"- `{item['package_id']}`: `{item['review_status']}`" for item in REVIEWED_PACKAGES)),
        ("Recommended Package", f"`{RECOMMENDED_PACKAGE}` is reviewed and not selected."),
        ("Reviewed Future Recovery or Recapture Requirements", f"{len(REVIEWED_REQUIREMENTS)} requirements reviewed; none executed."),
        ("Reviewed Future Recovery or Recapture Plan", f"{len(REVIEWED_PLAN)} planning steps reviewed; none executed."),
        ("Reviewed Future Controlled Recapture Command Template", "The five-module command template is reviewed planning and was not executed."),
        ("Reviewed Future Durable Receipt Safeguards", f"{len(REVIEWED_SAFEGUARDS)} safeguards reviewed; none executed."),
        ("Reviewed Planned Outputs", f"{len(REVIEWED_OUTPUTS)} outputs reviewed; none generated."),
        ("Reviewed Non-Goals", ", ".join(f"`{item['non_goal_id']}`" for item in REVIEWED_NON_GOALS)),
        ("Recommendation", f"{RECOMMENDATION['reason']} Next task: `{NEXT_TASK}`."),
        ("Next Chain", "\n".join(f"{index}. {item}" for index, item in enumerate(NEXT_CHAIN, start=1))),
        ("Next Gates", "\n".join(f"- `{item}`" for item in NEXT_GATES)),
        ("Risk Controls", "\n".join(f"- `{item}`" for item in RISK_CONTROLS)),
        ("Authority Boundaries", "No selection, approval, recovery, recapture, diagnostic, retry, predictive, profitability, runtime, or trading authority is created."),
        ("Checklist Summary", f"{review['summary']['passed_checks']}/{review['summary']['total_checks']} checks passed."),
        ("Guardrails", "MarketFlow remains research and decision-support software, not execution software."),
    ]
    title = "# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Candidate Operator Review v1"
    return title + "\n\n" + "\n\n".join(f"## {heading}\n\n{body}" for heading, body in sections) + "\n"


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RECAPTURE_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER = RECOMMENDED_PACKAGE
