"""Plan safe sources for retry-failure classification without reading them."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1 = (
    "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_METHOD_EXECUTION_DIGEST = "522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562"
SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST = "3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f"
RECOMMENDED_PACKAGE = "PACKAGE_READ_EXISTING_DETACHED_PYTEST_CACHE_LASTFAILED_AS_CLASSIFICATION_SOURCE"
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
BLOCKER = "BLOCKER"

CANDIDATE_PHILOSOPHY = (
    "Because authoritative retry output details were not persisted, the next safe step is to "
    "identify or create a classification source without treating diagnostics as retry evidence "
    "and without overriding the failed authoritative retry."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no output capture, diagnostic command, retry rerun, classification, "
    "results review, integration success, main merge, or runtime authority is created by this artifact."
)
CANDIDATE_GOAL = (
    "Define controlled future methods to obtain failure-module, error-module, first-failure, "
    "first-error, and traceback-classification data for the failed authoritative retry."
)

SOURCE_PACKAGES = [
    {
        "package_id": RECOMMENDED_PACKAGE,
        "status": RECOMMENDATION_STATUS,
        "purpose": "Read existing pytest cache artifacts in the detached integration worktree, especially .pytest_cache/v/cache/lastfailed and related cache files, as a non-rerun source of failed/error test node IDs.",
        "recommended_for": "It may provide failure-node classification from the actual authoritative retry without rerunning pytest or treating root regression as evidence.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_OPERATOR_PROVIDED_AUTHORITATIVE_RETRY_STDOUT_STDERR_LOG_PATH",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Allow an operator to provide a path to the original authoritative retry stdout/stderr log if it exists outside committed files.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CAPTURE_DIAGNOSTIC_PYTEST_OUTPUT_FROM_DETACHED_WORKTREE_NOT_RETRY_EVIDENCE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL",
        "purpose": "Run a diagnostic-only pytest command from the detached worktree to capture failure details, explicitly not retry evidence and unable to override the failed authoritative retry.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_TARGETED_DIAGNOSTIC_COLLECTION_AND_NODEID_INVENTORY",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Run non-executing or minimally executing diagnostic commands such as collection/nodeid inventory to map modules and potential failure domains.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_COMMITTED_STATUS_ONLY_CLASSIFICATION",
        "status": "BLOCKED_NOT_SUFFICIENT",
        "purpose": "Classify failures using only committed status documents and aggregate counts.",
        "blocked_reason": "The previous method execution proved committed status records lack detailed failure modules, first failure, and first error traces.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_USE_ROOT_WORKTREE_REGRESSION_OUTPUT_AS_CLASSIFICATION_SOURCE",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Use the passing root-worktree regression as a proxy for detached retry classification.",
        "blocked_reason": "Root regression is not retry evidence and does not represent the failed detached integration worktree retry.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_RERUN_AUTHORITATIVE_RETRY_AND_REPLACE_FAILED_RESULT",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Rerun the retry and replace the failed authoritative retry result.",
        "blocked_reason": "The first retry result remains authoritative. Later reruns cannot override it.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_MAIN_MERGE_DESPITE_OUTPUT_UNAVAILABLE",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Proceed to main merge despite unavailable classification details.",
        "blocked_reason": "Main merge approval remains blocked until a future retry results review passes.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
]

FUTURE_OUTPUT_CAPTURE_REQUIREMENTS = {
    "source_method_execution_blocked_must_be_ready": True,
    "authoritative_retry_failure_counts_must_be_bound": True,
    "root_regression_must_not_be_treated_as_retry_evidence": True,
    "output_capture_must_not_rerun_authoritative_retry": True,
    "output_capture_must_not_replace_failed_retry_result": True,
    "output_capture_must_not_create_retry_results_review": True,
    "output_capture_must_not_mark_integration_successful": True,
    "detached_worktree_cache_read_must_be_read_only": True,
    "pytest_cache_source_must_be_from_detached_worktree": True,
    "pytest_cache_source_if_missing_must_fail_closed": True,
    "operator_log_path_if_used_must_be_explicitly_provided": True,
    "operator_log_path_if_used_must_not_contain_secrets": True,
    "diagnostic_pytest_if_selected_must_be_explicitly_not_retry_evidence": True,
    "diagnostic_pytest_if_selected_must_not_override_failed_retry": True,
    "classification_source_outputs_must_be_research_governance_only": True,
    "future_classification_requires_separate_review_or_reentry": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_OUTPUT_CAPTURE_PLAN = [
    "Verify source method execution blocked artifact and blocked-manifest digest.",
    "Verify detached worktree path and HEAD.",
    "Verify staged evidence remains unchanged and untracked.",
    "Inventory candidate classification sources: detached pytest cache lastfailed/nodeids, an explicitly operator-provided authoritative retry log path, and committed status records.",
    "If pytest cache exists, hash and parse it read-only.",
    "If an operator log path is provided, hash and parse it read-only.",
    "Produce a classification-source availability report.",
    "If no classification source exists, fail closed and recommend diagnostic-output capture approval.",
    "Do not rerun full pytest or treat diagnostics as retry evidence.",
    "Keep retry results review, new retry, main merge, runtime, and trading authority closed.",
]
FUTURE_OUTPUT_CAPTURE_PLAN_STATUS = "PLANNED_NOT_EXECUTED"
PLANNED_OUTPUT_NAMES = [
    "classification_source_inventory_manifest",
    "pytest_cache_lastfailed_report",
    "pytest_cache_nodeids_report",
    "operator_retry_log_source_report",
    "classification_source_availability_report",
    "missing_classification_source_report",
    "diagnostic_output_capture_recommendation",
    "authority_boundary_report",
    "digest_manifest",
]
PLANNED_OUTPUTS = [
    {"output_id": output_id, "status": "PLANNED_NOT_GENERATED"}
    for output_id in PLANNED_OUTPUT_NAMES
]
NON_GOALS = [
    "do_not_capture_output_now",
    "do_not_read_pytest_cache_now",
    "do_not_parse_operator_logs_now",
    "do_not_run_diagnostic_commands_now",
    "do_not_rerun_retry_now",
    "do_not_run_full_pytest_now",
    "do_not_treat_diagnostics_as_retry_evidence",
    "do_not_replace_failed_authoritative_retry",
    "do_not_create_retry_results_review",
    "do_not_create_integration_results_review",
    "do_not_mark_integration_successful",
    "do_not_stage_additional_evidence",
    "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence",
    "do_not_call_providers",
    "do_not_commit_marketflow_outputs",
    "do_not_push_integration_branch",
    "do_not_push_main",
    "do_not_delete_integration_branch",
    "do_not_delete_worktree",
    "do_not_force_push",
    "do_not_modify_tags",
    "do_not_create_main_merge_approval",
    "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability",
    "do_not_authorize_runtime",
    "do_not_authorize_trading",
]
NEXT_CHAIN = [
    "Output Capture or Classification Source Candidate Operator Review v1.",
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
    "output_capture_or_classification_source_operator_review",
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
    "candidate_does_not_capture_output",
    "candidate_does_not_read_pytest_cache",
    "candidate_does_not_parse_operator_logs",
    "candidate_does_not_run_diagnostic_commands",
    "candidate_does_not_rerun_retry",
    "candidate_does_not_run_full_pytest",
    "candidate_does_not_treat_diagnostics_as_retry_evidence",
    "candidate_does_not_replace_failed_retry_result",
    "candidate_does_not_create_retry_results_review",
    "candidate_does_not_create_integration_results_review",
    "candidate_does_not_mark_integration_successful",
    "candidate_does_not_generate_successful_integration_execution_digest",
    "candidate_does_not_generate_successful_integration_validation_digest",
    "candidate_does_not_stage_additional_evidence",
    "candidate_does_not_modify_staged_evidence",
    "candidate_does_not_regenerate_evidence",
    "candidate_does_not_call_providers",
    "candidate_does_not_commit_marketflow_outputs",
    "candidate_does_not_push_integration_branch",
    "candidate_does_not_push_main",
    "candidate_does_not_delete_integration_branch",
    "candidate_does_not_delete_worktree",
    "candidate_does_not_force_push",
    "candidate_does_not_prune_remotes",
    "candidate_does_not_modify_tags",
    "candidate_does_not_acquire_market_data",
    "candidate_does_not_regenerate_dataset",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_train_models",
    "candidate_does_not_score_strategy",
    "candidate_does_not_generate_recommendations",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_operator_review_required",
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
    "candidate_created_true",
    "candidate_ready_true",
    "recommended_package_present",
    "source_packages_present_8",
    "blocked_packages_present_4",
    "recommended_package_not_selected",
    "output_capture_selected_false",
    "output_capture_approved_false",
    "output_capture_executed_false",
    "classification_source_generated_false",
    "classification_source_review_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_executed_false",
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
    "future_output_capture_requirements_defined",
    "future_output_capture_plan_defined",
    "planned_outputs_defined",
    "non_goals_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(ValueError):
    """Raised when the candidate or its closed authority boundaries are invalid."""


def _source_execution() -> dict[str, Any]:
    evidence = source._source_evidence()
    return {
        "source_method_execution_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED,
        "source_method_execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE,
        "source_method_execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_method_execution_digest": SOURCE_METHOD_EXECUTION_DIGEST,
        "source_method_blocked_manifest_digest": SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST,
        "source_method_approval_digest": evidence["source_method_approval_digest"],
        "source_method_operator_review_digest": evidence["source_method_operator_review_digest"],
        "source_method_candidate_digest": evidence["source_method_candidate_digest"],
        "source_retry_failure_diagnosis_digest": evidence["source_retry_failure_diagnosis_digest"],
        "source_retry_approval_digest": evidence["source_retry_approval_digest"],
        "source_staged_inventory_digest": evidence["source_staged_inventory_digest"],
        "retry_execution_branch": evidence["retry_execution_branch"],
        "retry_execution_commit": evidence["retry_execution_commit"],
        "retry_pytest_command": evidence["retry_pytest_command"],
        "retry_pytest_working_directory": evidence["retry_pytest_working_directory"],
        "retry_pytest_duration_seconds": evidence["retry_pytest_duration_seconds"],
        "retry_pytest_ran_from_detached_worktree": True,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_performed": True,
        "retry_pytest_exit_code": 1,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "available_retry_data": source._available_retry_data(),
        "missing_retry_data": list(source.MISSING_RETRY_DATA),
        "classification_source_available": False,
        "classification_blocked_reason": source.CLASSIFICATION_BLOCKED_REASON,
        "root_full_regression_is_retry_evidence": False,
        "origin_main_commit": evidence["origin_main_commit"],
        "integration_branch_name": evidence["integration_branch_name"],
        "integration_branch_head_commit": evidence["integration_branch_head_commit"],
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": evidence["detached_integration_worktree_path"],
        "detached_integration_worktree_head_commit": evidence["detached_integration_worktree_head_commit"],
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean": True,
        "staged_evidence_manifest_digest": evidence["staged_evidence_manifest_digest"],
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
    }


def _base_candidate(source_execution: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        "operator_review_required": True,
        **deepcopy(dict(source_execution)),
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL,
        "proposed_output_capture_or_classification_source_packages": deepcopy(SOURCE_PACKAGES),
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": "Reading existing pytest cache artifacts may provide classification source data generated by the authoritative retry without rerunning pytest or creating new retry evidence.",
        "future_output_capture_requirements": deepcopy(FUTURE_OUTPUT_CAPTURE_REQUIREMENTS),
        "future_output_capture_plan": list(FUTURE_OUTPUT_CAPTURE_PLAN),
        "future_output_capture_plan_status": FUTURE_OUTPUT_CAPTURE_PLAN_STATUS,
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "non_goals": list(NON_GOALS),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "output_capture_candidate_created": True,
        "output_capture_candidate_ready_for_operator_review": True,
        "ready_for_output_capture_candidate_operator_review": True,
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
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
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
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
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


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = [candidate.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    packages = candidate.get("proposed_output_capture_or_classification_source_packages")
    package_rows = packages if isinstance(packages, list) else []
    recommended = next((row for row in package_rows if row.get("package_id") == RECOMMENDED_PACKAGE), None)
    blocked = [row for row in package_rows if str(row.get("status", "")).startswith("BLOCKED_")]
    values: dict[str, tuple[Any, Any]] = {
        "source_method_execution_digest_bound": (SOURCE_METHOD_EXECUTION_DIGEST, candidate.get("source_method_execution_digest")),
        "source_method_blocked_manifest_digest_bound": (SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST, candidate.get("source_method_blocked_manifest_digest")),
        "source_method_approval_digest_bound": (source.SOURCE_METHOD_APPROVAL_DIGEST, candidate.get("source_method_approval_digest")),
        "source_method_operator_review_digest_bound": (source.source.SOURCE_OPERATOR_REVIEW_DIGEST, candidate.get("source_method_operator_review_digest")),
        "source_method_candidate_digest_bound": (source.source.source.SOURCE_METHOD_CANDIDATE_DIGEST, candidate.get("source_method_candidate_digest")),
        "source_retry_failure_diagnosis_digest_bound": (source.source.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, candidate.get("source_retry_failure_diagnosis_digest")),
        "source_staged_inventory_digest_bound": ("06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0", candidate.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], counts),
        "classification_blocked_reason_bound": (source.CLASSIFICATION_BLOCKED_REASON, candidate.get("classification_blocked_reason")),
        "available_retry_data_bound": (source._available_retry_data(), candidate.get("available_retry_data")),
        "missing_retry_data_bound": (source.MISSING_RETRY_DATA, candidate.get("missing_retry_data")),
        "origin_main_bound": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", candidate.get("origin_main_commit")),
        "integration_branch_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", candidate.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", candidate.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": ("06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0", candidate.get("staged_evidence_manifest_digest")),
        "candidate_created_true": (True, candidate.get("output_capture_candidate_created")),
        "candidate_ready_true": (True, candidate.get("output_capture_candidate_ready_for_operator_review")),
        "recommended_package_present": (True, recommended is not None),
        "source_packages_present_8": (8, len(package_rows)),
        "blocked_packages_present_4": (4, len(blocked)),
        "recommended_package_not_selected": (False, recommended.get("selected") if recommended else None),
        "output_capture_selected_false": (False, candidate.get("output_capture_method_selected")),
        "output_capture_approved_false": (False, candidate.get("output_capture_method_approved")),
        "output_capture_executed_false": (False, candidate.get("output_capture_method_executed")),
        "classification_source_generated_false": (False, candidate.get("classification_source_generated")),
        "classification_source_review_created_false": (False, candidate.get("classification_source_review_created")),
        "retry_rerun_false": (False, candidate.get("retry_rerun_performed")),
        "full_pytest_false": (False, candidate.get("full_pytest_performed")),
        "diagnostic_command_executed_false": (False, candidate.get("diagnostic_command_executed")),
        "new_classification_method_candidate_created_false": (False, candidate.get("new_classification_method_candidate_created")),
        "new_retry_candidate_created_false": (False, candidate.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, candidate.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, candidate.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, candidate.get("main_merge_approval_created")),
        "integration_execution_successful_false": (False, candidate.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [candidate.get("successful_integration_execution_digest_generated"), candidate.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
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
        "future_output_capture_requirements_defined": (FUTURE_OUTPUT_CAPTURE_REQUIREMENTS, candidate.get("future_output_capture_requirements")),
        "future_output_capture_plan_defined": ([FUTURE_OUTPUT_CAPTURE_PLAN, FUTURE_OUTPUT_CAPTURE_PLAN_STATUS], [candidate.get("future_output_capture_plan"), candidate.get("future_output_capture_plan_status")]),
        "planned_outputs_defined": (PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "output_capture_candidate_created": True,
        "output_capture_candidate_ready_for_operator_review": True,
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "output_capture_selected": False,
        "output_capture_approved": False,
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


def marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
    *, source_execution: dict | None = None,
) -> dict:
    """Build the candidate from committed blocked-execution constants only."""
    evidence = _source_execution()
    if source_execution is not None:
        if not isinstance(source_execution, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
                "source_execution must be an object"
            )
        evidence.update(deepcopy(source_execution))
    candidate = _base_candidate(evidence)
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"] = (
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, candidate packages, and all closed boundaries."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            "candidate must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_source_execution(),
        "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL,
        "proposed_output_capture_or_classification_source_packages": SOURCE_PACKAGES,
        "recommended_output_capture_or_classification_source_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "future_output_capture_requirements": FUTURE_OUTPUT_CAPTURE_REQUIREMENTS,
        "future_output_capture_plan": FUTURE_OUTPUT_CAPTURE_PLAN,
        "future_output_capture_plan_status": FUTURE_OUTPUT_CAPTURE_PLAN_STATUS,
        "planned_outputs": PLANNED_OUTPUTS,
        "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(candidate.get(field), expected, field)
    for field in (
        "created_offline",
        "governance_only",
        "candidate_only",
        "operator_review_required",
        "output_capture_candidate_created",
        "output_capture_candidate_ready_for_operator_review",
        "ready_for_output_capture_candidate_operator_review",
        "staged_evidence_unchanged",
        "no_tracked_marketflow_files",
    ):
        _expect(candidate.get(field), True, field)
    for field in (
        "root_full_regression_is_retry_evidence",
        "classification_source_available",
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
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            "checklist missing"
        )
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            "checklist failed"
        )
    _expect(candidate.get("summary"), _summary(checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest": digest,
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated candidate as a planning-only governance record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(candidate)
    sections = [
        ("Source Method Execution", [f"Execution digest: `{candidate['source_method_execution_digest']}`.", f"Blocked manifest: `{candidate['source_method_blocked_manifest_digest']}`."]),
        ("Blocked Classification Context", [f"`{candidate['classification_blocked_reason']}`.", "Detailed authoritative retry output remains unavailable."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "Root regression is not retry evidence."]),
        ("Candidate Scope", [f"`{candidate['candidate_scope']}`."]),
        ("Candidate Philosophy", [candidate["candidate_philosophy"], candidate["candidate_boundary"], candidate["candidate_goal"]]),
        ("Proposed Output Capture or Classification Source Packages", [f"`{row['package_id']}`: `{row['status']}`" for row in candidate["proposed_output_capture_or_classification_source_packages"]]),
        ("Recommended Package", [f"`{candidate['recommended_output_capture_or_classification_source_package']}`: `{candidate['recommendation_status']}`."]),
        ("Future Output Capture Requirements", [f"`{key}`: `{value}`" for key, value in candidate["future_output_capture_requirements"].items()]),
        ("Future Output Capture Plan", candidate["future_output_capture_plan"]),
        ("Planned Outputs", [f"`{row['output_id']}`: `{row['status']}`" for row in candidate["planned_outputs"]]),
        ("Non-Goals", [f"`{row}`" for row in candidate["non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No cache read, log parse, output capture, diagnostic command, retry, results review, protected push, or runtime/trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The recommended package is not selected or approved.", "A separate operator review and approval are required before any source capture."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
    output_dir: str | Path,
    *,
    source_execution: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
        source_execution=source_execution
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest": candidate[
            "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
