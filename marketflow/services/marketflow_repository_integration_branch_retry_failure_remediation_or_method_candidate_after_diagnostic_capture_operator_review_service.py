"""Review candidate-only remediation or method options after diagnostic capture."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest"

SOURCE_CANDIDATE_COMMIT = "957a936d36b80841729ee98c2b8ab35140711d78"
SOURCE_CANDIDATE_DIGEST = "405fa30e32f2e71f77cd502cbd8ad0644f2f07d684de9a24b0d90ac0b3bab95d"
SOURCE_RESULTS_REVIEW_COMMIT = source.SOURCE_RESULTS_REVIEW_COMMIT
SOURCE_RESULTS_REVIEW_DIGEST = source.SOURCE_RESULTS_REVIEW_DIGEST
SOURCE_PAYLOAD_REVIEW_DIGEST = source.SOURCE_PAYLOAD_REVIEW_DIGEST
SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST = source.SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST
SOURCE_EXECUTION_COMMIT = source.SOURCE_EXECUTION_COMMIT
SOURCE_EXECUTION_DIGEST = source.SOURCE_EXECUTION_DIGEST
SOURCE_PAYLOAD_DIGEST = source.SOURCE_PAYLOAD_DIGEST
SOURCE_RECEIPT_DIGEST = source.SOURCE_RECEIPT_DIGEST
SOURCE_DIGEST_MANIFEST_DIGEST = source.SOURCE_DIGEST_MANIFEST_DIGEST
SOURCE_DURABLE_RECEIPT_PATH = source.SOURCE_DURABLE_RECEIPT_PATH
SOURCE_BINDINGS = deepcopy(source.SOURCE_BINDINGS)
RETRY_EXECUTION_COMMIT = source.RETRY_EXECUTION_COMMIT
PRIORITY_1_TARGET_MODULES = deepcopy(source.PRIORITY_1_TARGET_MODULES)

RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDATION_STATUS = "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_DIAGNOSTIC_CAPTURE_V1_IF_SELECTED"
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_APPROVAL_NOT_CREATED"
RECOMMENDED_ACTION = "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_OR_METHOD_EXECUTION"
RECOMMENDATION_REASON = (
    "The remediation-or-method candidate after diagnostic capture has been reviewed, but no remediation or "
    "method package has been selected or approved by this review. Any failure-family classification or "
    "remediation-planning method requires a separate approval ceremony."
)
PACKAGE_REASON = (
    "The durable diagnostic receipt has been reviewed and contains bounded diagnostic evidence for the approved "
    "Priority 1 modules. A future failure-family classification method can convert that evidence into a reviewed "
    "remediation-planning basis without jumping directly to code changes, retry, or main merge."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REVIEWED_PHILOSOPHY_TEXT = (
    "The controlled diagnostic recapture produced a finalized durable receipt with command identity, approved "
    "target modules, exit code, stdout/stderr hashes, byte counts, bounded output status, and redaction review. "
    "The candidate correctly defines governed method or remediation-planning options that may use the reviewed "
    "durable receipt evidence in a future approved execution. The operator review must not analyze diagnostic "
    "output, infer root cause, recommend direct code changes, execute remediation, or create retry readiness."
)
REVIEWED_CANDIDATE_BOUNDARY = (
    "Operator-review only; no method execution, remediation, diagnostic rerun, classification, retry, results "
    "review, main merge, runtime, or trading authority is created."
)
REVIEWED_CANDIDATE_GOAL = (
    "Review safe future remediation-or-method packages after diagnostic capture, preserving the diagnostic "
    "evidence as planning input only."
)


def _reviewed_packages() -> list[dict[str, Any]]:
    reviewed = []
    for item in source.PROPOSED_PACKAGES:
        status = (
            "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
            if item["package_id"] == RECOMMENDED_PACKAGE
            else "REVIEWED_BLOCKED_NOT_ALLOWED"
            if item["status"] == "BLOCKED_NOT_ALLOWED"
            else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        )
        record = {
            "package_id": item["package_id"], "source_status": item["status"], "review_status": status,
            "purpose": item["purpose"], "selected": False, "approved": False,
            "authorized": False, "executed": False,
        }
        if "recommended_reason" in item:
            record["recommended_reason"] = item["recommended_reason"]
        if "blocked_reason" in item:
            record["blocked_reason"] = item["blocked_reason"]
        reviewed.append(record)
    return reviewed


REVIEWED_PACKAGES = _reviewed_packages()
REVIEWED_FUTURE_METHOD_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION_OR_METHOD_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for requirement_id in source.FUTURE_METHOD_REQUIREMENTS
]
REVIEWED_FUTURE_METHOD_PLAN = [
    {
        "step_id": f"step_{index:02d}", "step": step,
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.FUTURE_METHOD_PLAN, start=1)
]
REVIEWED_PLANNED_OUTPUTS = [
    {"output_id": output_id, "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
    for output_id in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": non_goal_id, "review_status": "REVIEWED_ACTIVE"}
    for non_goal_id in source.NON_GOALS
]

NEXT_CHAIN = [
    "Remediation or Method Approval After Diagnostic Capture v1, if selected.",
    "Remediation or Method Execution After Diagnostic Capture v1, if approved.",
    "Remediation or Method Results Review After Diagnostic Capture v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_or_method_approval_after_diagnostic_capture_if_selected",
    "remediation_or_method_execution_after_diagnostic_capture_if_approved",
    "remediation_or_method_results_review_after_diagnostic_capture",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "operator_review_after_diagnostic_capture_does_not_select_package",
    "operator_review_after_diagnostic_capture_does_not_approve_package",
    "operator_review_after_diagnostic_capture_does_not_authorize_package",
    "operator_review_after_diagnostic_capture_does_not_execute_method_analysis",
    "operator_review_after_diagnostic_capture_does_not_execute_remediation",
    "operator_review_after_diagnostic_capture_does_not_parse_durable_receipt",
    "operator_review_after_diagnostic_capture_does_not_analyze_diagnostic_output",
    "operator_review_after_diagnostic_capture_does_not_rerun_controlled_recapture",
    "operator_review_after_diagnostic_capture_does_not_run_diagnostic_command",
    "operator_review_after_diagnostic_capture_does_not_run_targeted_pytest",
    "operator_review_after_diagnostic_capture_does_not_run_full_pytest",
    "operator_review_after_diagnostic_capture_does_not_rerun_retry",
    "operator_review_after_diagnostic_capture_does_not_read_pytest_cache",
    "operator_review_after_diagnostic_capture_does_not_modify_pytest_cache",
    "operator_review_after_diagnostic_capture_does_not_parse_terminal_logs",
    "operator_review_after_diagnostic_capture_does_not_parse_operator_logs",
    "operator_review_after_diagnostic_capture_does_not_inspect_env",
    "operator_review_after_diagnostic_capture_does_not_reconstruct_prior_lost_values",
    "operator_review_after_diagnostic_capture_does_not_reconstruct_full_streams",
    "operator_review_after_diagnostic_capture_does_not_classify_modules_again",
    "operator_review_after_diagnostic_capture_does_not_claim_failure_error_separation",
    "operator_review_after_diagnostic_capture_does_not_identify_first_failure",
    "operator_review_after_diagnostic_capture_does_not_identify_first_error",
    "operator_review_after_diagnostic_capture_does_not_claim_traceback_root_cause",
    "operator_review_after_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "operator_review_after_diagnostic_capture_does_not_create_remediation_approval",
    "operator_review_after_diagnostic_capture_does_not_create_remediation_execution",
    "operator_review_after_diagnostic_capture_does_not_create_remediation_results_review",
    "operator_review_after_diagnostic_capture_does_not_create_new_retry_candidate",
    "operator_review_after_diagnostic_capture_does_not_create_retry_results_review",
    "operator_review_after_diagnostic_capture_does_not_create_integration_results_review",
    "operator_review_after_diagnostic_capture_does_not_mark_integration_successful",
    "operator_review_after_diagnostic_capture_does_not_generate_successful_integration_digest",
    "operator_review_after_diagnostic_capture_does_not_treat_diagnostic_capture_as_retry",
    "operator_review_after_diagnostic_capture_does_not_treat_exit_code_as_retry_result",
    "operator_review_after_diagnostic_capture_does_not_push_integration_branch",
    "operator_review_after_diagnostic_capture_does_not_push_main",
    "operator_review_after_diagnostic_capture_does_not_delete_integration_branch",
    "operator_review_after_diagnostic_capture_does_not_delete_worktree",
    "operator_review_after_diagnostic_capture_does_not_force_push",
    "operator_review_after_diagnostic_capture_does_not_prune_remotes",
    "operator_review_after_diagnostic_capture_does_not_modify_tags",
    "operator_review_after_diagnostic_capture_does_not_modify_staged_evidence",
    "operator_review_after_diagnostic_capture_does_not_regenerate_evidence",
    "operator_review_after_diagnostic_capture_does_not_call_providers",
    "operator_review_after_diagnostic_capture_does_not_acquire_market_data",
    "operator_review_after_diagnostic_capture_does_not_regenerate_dataset",
    "operator_review_after_diagnostic_capture_does_not_recompute_metrics",
    "operator_review_after_diagnostic_capture_does_not_train_models",
    "operator_review_after_diagnostic_capture_does_not_score_strategy",
    "operator_review_after_diagnostic_capture_does_not_generate_recommendations",
    "operator_review_after_diagnostic_capture_does_not_accept_predictive_usefulness",
    "operator_review_after_diagnostic_capture_does_not_accept_profitability",
    "operator_review_after_diagnostic_capture_does_not_authorize_runtime",
    "operator_review_after_diagnostic_capture_does_not_authorize_broker_execution",
    "diagnostic_capture_results_review_remains_source_evidence", "durable_receipt_is_diagnostic_evidence_only",
    "controlled_recapture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation",
    "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_remediation_or_method_candidate_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_results_review_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_execution_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_approval_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence", "previous_targeted_diagnostic_approval_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_approval_required_before_method_execution",
    "separate_results_review_required_after_method_execution",
    "separate_retry_approval_required_before_new_retry", "main_merge_requires_passing_new_retry_results_review",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "remediation_or_method_candidate_after_diagnostic_capture_operator_review_created",
    "remediation_or_method_candidate_after_diagnostic_capture_operator_review_ready",
    "source_candidate_reviewed", "source_diagnostic_results_review_reviewed",
    "source_controlled_recapture_results_reviewed", "durable_receipt_evidence_reviewed",
    "diagnostic_capture_evidence_reviewed_for_future_method", "remediation_or_method_packages_reviewed",
    "future_method_requirements_reviewed", "future_method_plan_reviewed", "planned_outputs_reviewed",
    "non_goals_reviewed", "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]
FALSE_FIELDS = [
    "recommended_package_selected", "remediation_or_method_package_selected",
    "remediation_or_method_package_approved", "remediation_or_method_package_authorized",
    "remediation_or_method_execution_performed", "method_analysis_executed", "remediation_execution_performed",
    "code_remediation_executed", "evidence_remediation_executed", "diagnostic_receipt_parsed_in_review",
    "diagnostic_output_analyzed_in_review", "failure_family_classification_performed",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "controlled_recapture_rerun_performed", "diagnostic_command_rerun_performed",
    "targeted_pytest_performed_in_review", "full_pytest_performed", "retry_rerun_performed",
    "cache_read_in_review", "cache_modified_in_review", "pytest_cache_committed", "marketflow_outputs_committed",
    "terminal_logs_parsed", "operator_logs_parsed", "env_inspection_performed",
    "prior_lost_values_reconstructed", "prior_lost_values_inferred", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "ready_for_remediation_or_method_approval", "ready_for_remediation_or_method_execution",
    "ready_for_retry_candidate", "ready_for_main_merge_approval", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "evidence_regenerated", "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError(ValueError):
    """Raised when operator-review evidence or authority boundaries are invalid."""


def _source_fields(source_candidate: dict | None) -> dict[str, Any]:
    if source_candidate is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(
                deepcopy(source_candidate)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError(
                "source candidate validation failed"
            ) from exc
        if source_candidate.get(source.CANDIDATE_DIGEST_KEY) != SOURCE_CANDIDATE_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError(
                "source candidate digest mismatch"
            )
    return {
        "source_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_candidate_status": source.CANDIDATE_STATUS, "source_candidate_scope": source.CANDIDATE_SCOPE,
        "source_candidate_commit": SOURCE_CANDIDATE_COMMIT,
        "source_remediation_or_method_candidate_after_diagnostic_capture_digest": SOURCE_CANDIDATE_DIGEST,
        "source_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        "source_receipt_recovery_or_recapture_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_receipt_recovery_or_recapture_payload_review_digest": SOURCE_PAYLOAD_REVIEW_DIGEST,
        "source_receipt_recovery_or_recapture_durable_receipt_review_digest": SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST,
        "source_receipt_recovery_or_recapture_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_receipt_recovery_or_recapture_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_receipt_recovery_or_recapture_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_receipt_recovery_or_recapture_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "source_receipt_recovery_or_recapture_receipt_digest": SOURCE_RECEIPT_DIGEST,
        "source_receipt_recovery_or_recapture_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_durable_receipt_path": SOURCE_DURABLE_RECEIPT_PATH,
        **deepcopy(SOURCE_BINDINGS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    value = deepcopy(dict(review))
    for field in ("checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", expected, review.get(field)) for field, expected in _source_fields(None).items()]
    checks.extend([
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", source.source.source.TARGET_MODULES, [item.get("module_path") for item in review.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("controlled_recapture_execution_reviewed_true", True, review.get("source_controlled_recapture_execution_performed")),
        _check("durable_receipt_finalized_reviewed_true", True, review.get("source_durable_receipt_finalized")),
        _check("durable_receipt_retained_reviewed_true", True, review.get("source_durable_receipt_retained")),
        _check("exit_code_1_bound_as_diagnostic_only", 1, review.get("source_exit_code")),
        _check("stdout_hash_bound", "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a", review.get("source_stdout_sha256")),
        _check("stderr_hash_bound", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", review.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, review.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, review.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, review.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, review.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, review.get("source_redaction_checked")),
        _check("recommended_package_reviewed_not_selected", RECOMMENDED_PACKAGE, review.get("recommended_remediation_or_method_package")),
        _check("packages_reviewed_12", 12, len(review.get("reviewed_remediation_or_method_packages", []))),
        _check("blocked_packages_reviewed_6", 6, sum(item.get("source_status") == "BLOCKED_NOT_ALLOWED" for item in review.get("reviewed_remediation_or_method_packages", []))),
        _check("future_method_requirements_reviewed", REVIEWED_FUTURE_METHOD_REQUIREMENTS, review.get("reviewed_future_method_requirements")),
        _check("future_method_plan_reviewed", REVIEWED_FUTURE_METHOD_PLAN, review.get("reviewed_future_method_plan")),
        _check("planned_outputs_reviewed", REVIEWED_PLANNED_OUTPUTS, review.get("reviewed_planned_outputs")),
        _check("non_goals_reviewed", REVIEWED_NON_GOALS, review.get("reviewed_non_goals")),
        _check("recommendation_defined", RECOMMENDED_NEXT_TASK, review.get("recommendation", {}).get("recommended_next_task")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
    ])
    checks.extend(_check(f"{field}_true", True, review.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, review.get(field)) for field in FALSE_FIELDS)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
    ])
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: review.get(field) for field in TRUE_FIELDS[:12]},
        **{field: review.get(field) for field in (
            "recommended_remediation_or_method_package", "recommended_package_selected",
            "remediation_or_method_package_selected", "remediation_or_method_package_approved",
            "remediation_or_method_execution_performed", "method_analysis_executed", "remediation_execution_performed",
            "diagnostic_receipt_parsed_in_review", "diagnostic_output_analyzed_in_review",
            "failure_family_classification_performed", "targeted_pytest_performed_in_review",
            "retry_rerun_performed", "full_pytest_performed", "ready_for_remediation_or_method_approval",
            "ready_for_remediation_or_method_execution", "ready_for_retry_candidate", "ready_for_main_merge_approval",
            "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
            "source_exit_code", "source_stdout_byte_count", "source_stderr_byte_count",
            "failed_or_errored_nodeids_count", "module_summary_module_count", "priority_1_total_nodeids",
            "top_10_count_sum",
        )},
        "priority_1_top_module_count": 5,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _nested_source_summaries() -> dict[str, Any]:
    return {
        "source_candidate_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.CANDIDATE_STATUS,
            "scope": source.CANDIDATE_SCOPE, "commit": SOURCE_CANDIDATE_COMMIT,
            "candidate_digest": SOURCE_CANDIDATE_DIGEST,
        },
        "source_diagnostic_results_review_summary": {
            "commit": SOURCE_RESULTS_REVIEW_COMMIT, "results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "payload_review_digest": SOURCE_PAYLOAD_REVIEW_DIGEST,
            "durable_receipt_review_digest": SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST,
            "manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        },
        "source_controlled_recapture_execution_summary": {
            "commit": SOURCE_EXECUTION_COMMIT, "execution_digest": SOURCE_EXECUTION_DIGEST,
            "payload_digest": SOURCE_PAYLOAD_DIGEST, "exit_code": 1,
            "diagnostic_evidence_only": True, "retry_evidence": False,
        },
        "source_durable_receipt_summary": {
            "path": SOURCE_DURABLE_RECEIPT_PATH, "receipt_digest": SOURCE_RECEIPT_DIGEST,
            "scaffold_prewritten": True, "finalized": True, "retained": True,
            "parsed_in_review": False,
        },
        "source_receipt_loss_history_summary": {
            "prior_execution_digest": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"],
            "blocked_reason": SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
            "primary_failure_class": SOURCE_BINDINGS["source_primary_failure_class"],
            "secondary_failure_class": SOURCE_BINDINGS["source_secondary_failure_class"],
            "historical_outcome_changed": False,
        },
        "source_planning_and_detail_binding_summary": {
            key: SOURCE_BINDINGS[key] for key in (
                "source_results_review_digest", "source_prioritized_planning_review_digest",
                "source_planning_execution_digest", "source_prioritized_planning_digest",
                "source_detail_binding_results_review_digest", "source_complete_29_row_binding_digest",
                "source_materialized_payload_digest", "source_recovery_detail_digest",
                "source_module_grouping_digest",
            )
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build an offline operator review without calling source builders or reading diagnostic evidence."""

    source_fields = _source_fields(source_candidate)
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        **source_fields, **_nested_source_summaries(),
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_target_modules": deepcopy(PRIORITY_1_TARGET_MODULES),
        "source_controlled_recapture_execution_performed": True,
        "source_diagnostic_command_executed": True, "source_diagnostic_output_captured": True,
        "source_diagnostic_method_executed": True, "source_targeted_pytest_performed": True,
        "source_durable_receipt_scaffold_prewritten": True, "source_durable_receipt_finalized": True,
        "source_durable_receipt_retained": True,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "diagnostic_capture_evidence_summary": {
            "command_identity_reviewed": True, "priority_1_modules_reviewed": True,
            "exit_code": 1, "exit_code_is_diagnostic_only": True,
            "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
            "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "stdout_byte_count": 1231380, "stderr_byte_count": 0, "bounded_output": True,
            "redaction_checked": True, "receipt_parsed": False, "diagnostic_output_analyzed": False,
        },
        "reviewed_candidate_philosophy": {
            "reviewed_remediation_or_method_candidate_after_diagnostic_capture_philosophy": REVIEWED_PHILOSOPHY_TEXT,
            "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
            "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL, "review_status": "REVIEWED_PLANNING_ONLY",
        },
        "reviewed_remediation_or_method_packages": deepcopy(REVIEWED_PACKAGES),
        "recommended_remediation_or_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommended_package": {
            "package_id": RECOMMENDED_PACKAGE, "review_status": RECOMMENDATION_STATUS,
            "reason": PACKAGE_REASON, "selected": False, "approved": False,
            "authorized": False, "executed": False,
        },
        "reviewed_future_method_requirements": deepcopy(REVIEWED_FUTURE_METHOD_REQUIREMENTS),
        "reviewed_future_method_plan": deepcopy(REVIEWED_FUTURE_METHOD_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
            "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON,
        },
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _review_digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(
    review: dict,
) -> dict:
    """Validate all source bindings, reviewed records, and closed authority boundaries."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    exact = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        **_source_fields(None), **_nested_source_summaries(),
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_target_modules": PRIORITY_1_TARGET_MODULES,
        "source_controlled_recapture_execution_performed": True,
        "source_diagnostic_command_executed": True, "source_diagnostic_output_captured": True,
        "source_diagnostic_method_executed": True, "source_targeted_pytest_performed": True,
        "source_durable_receipt_scaffold_prewritten": True, "source_durable_receipt_finalized": True,
        "source_durable_receipt_retained": True,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "diagnostic_capture_evidence_summary": {
            "command_identity_reviewed": True, "priority_1_modules_reviewed": True,
            "exit_code": 1, "exit_code_is_diagnostic_only": True,
            "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
            "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "stdout_byte_count": 1231380, "stderr_byte_count": 0, "bounded_output": True,
            "redaction_checked": True, "receipt_parsed": False, "diagnostic_output_analyzed": False,
        },
        "reviewed_candidate_philosophy": {
            "reviewed_remediation_or_method_candidate_after_diagnostic_capture_philosophy": REVIEWED_PHILOSOPHY_TEXT,
            "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
            "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL, "review_status": "REVIEWED_PLANNING_ONLY",
        },
        "reviewed_remediation_or_method_packages": REVIEWED_PACKAGES,
        "recommended_remediation_or_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommended_package": {
            "package_id": RECOMMENDED_PACKAGE, "review_status": RECOMMENDATION_STATUS,
            "reason": PACKAGE_REASON, "selected": False, "approved": False,
            "authorized": False, "executed": False,
        },
        "reviewed_future_method_requirements": REVIEWED_FUTURE_METHOD_REQUIREMENTS,
        "reviewed_future_method_plan": REVIEWED_FUTURE_METHOD_PLAN,
        "reviewed_planned_outputs": REVIEWED_PLANNED_OUTPUTS, "reviewed_non_goals": REVIEWED_NON_GOALS,
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
            "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON,
        },
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected in exact.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    if review.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise error("retry failure counts mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise error("required operator-review fact missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed boundary opened")
    packages = review.get("reviewed_remediation_or_method_packages", [])
    if len(packages) != 12 or sum(item.get("source_status") == "BLOCKED_NOT_ALLOWED" for item in packages) != 6:
        raise error("reviewed package inventory mismatch")
    if any(item.get(field) is not False for item in packages for field in ("selected", "approved", "authorized", "executed")):
        raise error("reviewed package authority opened")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    digest = review.get(OPERATOR_REVIEW_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise error("operator-review digest missing")
    if digest != _review_digest(review):
        raise error("operator-review digest mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "operator_review_digest": digest,
        **{field: review["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    """Write deterministic review JSON outside protected runtime directories."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError(
            "protected output directory"
        )
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(
        source_candidate=source_candidate
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError(
            "output exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS,
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY], "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a bounded operator-review summary after validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)
    sections = [
        ("Source Candidate", [SOURCE_CANDIDATE_COMMIT, SOURCE_CANDIDATE_DIGEST]),
        ("Source Diagnostic Results Review", [SOURCE_RESULTS_REVIEW_COMMIT, SOURCE_RESULTS_REVIEW_DIGEST]),
        ("Source Controlled Recapture Execution", [SOURCE_EXECUTION_COMMIT, SOURCE_EXECUTION_DIGEST]),
        ("Source Durable Receipt", [SOURCE_DURABLE_RECEIPT_PATH, SOURCE_RECEIPT_DIGEST]),
        ("Source Receipt Loss History", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"], SOURCE_BINDINGS["source_primary_failure_class"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_planning_execution_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Review Scope", [REVIEW_SCOPE]), ("Priority 1 Target Modules", source.source.source.TARGET_MODULES),
        ("Diagnostic Capture Evidence Summary", [str(review["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Candidate Philosophy", [REVIEWED_PHILOSOPHY_TEXT, REVIEWED_CANDIDATE_BOUNDARY, REVIEWED_CANDIDATE_GOAL]),
        ("Reviewed Remediation or Method Packages", [f"{item['package_id']}: {item['review_status']}" for item in REVIEWED_PACKAGES]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, RECOMMENDATION_STATUS, PACKAGE_REASON]),
        ("Reviewed Future Method Requirements", [item["requirement_id"] for item in REVIEWED_FUTURE_METHOD_REQUIREMENTS]),
        ("Reviewed Future Method Plan", [item["step"] for item in REVIEWED_FUTURE_METHOD_PLAN]),
        ("Reviewed Planned Outputs", [item["output_id"] for item in REVIEWED_PLANNED_OUTPUTS]),
        ("Reviewed Non-Goals", [item["non_goal_id"] for item in REVIEWED_NON_GOALS]),
        ("Recommendation", [RECOMMENDED_NEXT_TASK, RECOMMENDED_ACTION, RECOMMENDATION_REASON]),
        ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Operator-review only; no selection, approval, execution, retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No receipt parsing, output analysis, command, pytest, cache, log, environment, provider, data, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Diagnostic Capture Operator Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "SCHEMA_VERSION", "OPERATOR_REVIEW_DIGEST_KEY",
    "SOURCE_CANDIDATE_COMMIT", "SOURCE_CANDIDATE_DIGEST", "SOURCE_RESULTS_REVIEW_COMMIT",
    "SOURCE_RESULTS_REVIEW_DIGEST", "SOURCE_PAYLOAD_REVIEW_DIGEST", "SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST",
    "SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST", "SOURCE_EXECUTION_COMMIT", "SOURCE_EXECUTION_DIGEST",
    "SOURCE_PAYLOAD_DIGEST", "SOURCE_RECEIPT_DIGEST", "SOURCE_DIGEST_MANIFEST_DIGEST",
    "SOURCE_DURABLE_RECEIPT_PATH", "SOURCE_BINDINGS", "RECOMMENDED_PACKAGE", "RECOMMENDATION_STATUS",
    "RECOMMENDED_NEXT_TASK", "REVIEWED_PACKAGES", "REVIEWED_FUTURE_METHOD_REQUIREMENTS",
    "REVIEWED_FUTURE_METHOD_PLAN", "REVIEWED_PLANNED_OUTPUTS", "REVIEWED_NON_GOALS", "NEXT_CHAIN",
    "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_markdown_v1",
]
