"""Propose offline methods for classifying the failed authoritative retry."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_diagnosis_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST = "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
SOURCE_RETRY_APPROVAL_DIGEST = source.SOURCE_RETRY_APPROVAL_DIGEST
SOURCE_RETRY_OPERATOR_REVIEW_DIGEST = source.SOURCE_RETRY_OPERATOR_REVIEW_DIGEST
SOURCE_RETRY_CANDIDATE_DIGEST = source.SOURCE_RETRY_CANDIDATE_DIGEST
SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = source.SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST
SOURCE_REMEDIATION_EXECUTION_DIGEST = source.SOURCE_REMEDIATION_EXECUTION_DIGEST
SOURCE_STAGED_INVENTORY_DIGEST = source.SOURCE_STAGED_INVENTORY_DIGEST
SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.SOURCE_FAILURE_DIAGNOSIS_DIGEST
SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST

RECOMMENDED_PACKAGE = "PACKAGE_CLASSIFY_RETRY_FAILURE_DOMAINS_FROM_AUTHORITATIVE_OUTPUT"
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDATION_REASON = (
    "The failed retry still has 1,292 failures and 112 errors. A domain classification "
    "step is safer than guessing a remediation path or rerunning the retry."
)
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1"
)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_PHILOSOPHY = (
    "The remaining retry failure must be handled as a failure-domain and method-selection "
    "problem before any further retry. The next step is to classify the residual 1,292 "
    "failures and 112 errors without treating diagnostics as retry evidence."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no diagnostic execution, remediation, retry, results review, "
    "integration success, main merge, or runtime authority is created by this artifact."
)
CANDIDATE_GOAL = (
    "Define safe future methods to identify whether remaining failures are caused by "
    "additional ignored evidence roots, path/cwd assumptions, digest-constant drift, "
    "branch-content mismatch, test isolation, or other integration-specific issues."
)

METHOD_PACKAGES = [
    {
        "package_id": RECOMMENDED_PACKAGE,
        "status": RECOMMENDATION_STATUS,
        "purpose": "Classify the 1,292 failures and 112 errors by module, first failing test, first error trace, likely root-cause family, and dependency on ignored evidence, path/cwd, digest constants, or integration branch content.",
        "recommended_for": "The failure volume is too large for safe immediate remediation; classification is needed before choosing a repair method.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_IDENTIFY_ADDITIONAL_IGNORED_EVIDENCE_ROOTS_REQUIRED_BY_DETACHED_RETRY",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Inventory additional ignored .marketflow evidence roots required by failed tests, without generating or copying them yet.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_PATH_AND_CWD_ASSUMPTION_REMEDIATION_CANDIDATE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Identify and prepare fixes for tests or services that incorrectly assume the root feature worktree path instead of the detached integration worktree path.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_DIGEST_CONSTANT_AND_HISTORICAL_ARTIFACT_DRIFT_REVIEW",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Trace failures caused by digest constants expected by later feature branches but absent, different, or unreachable in the integration merge stack.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_TEST_ISOLATION_CACHE_ENVIRONMENT_DIAGNOSTIC_METHOD",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Plan diagnostic commands to classify test order, import cache, environment, and root/detached worktree differences without treating results as retry evidence.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_REBUILD_INTEGRATION_BRANCH_WITH_UPDATED_SOURCE_STACK",
        "status": "BLOCKED_NOT_RECOMMENDED",
        "purpose": "Rebuild or recreate the integration branch with a different source stack.",
        "blocked_reason": "The current integration branch and retry failure must be diagnosed before any rebuild/recreate path is considered.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_ACCEPT_ROOT_WORKTREE_REGRESSION_AS_INTEGRATION_SUCCESS",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Treat the passing root-worktree regression as integration retry evidence.",
        "blocked_reason": "Root regression is explicitly not retry evidence and cannot override detached retry failure.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": "PACKAGE_MAIN_MERGE_DESPITE_RETRY_FAILURE",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Proceed to main merge despite failed authoritative retry.",
        "blocked_reason": "Main merge approval is blocked until a future retry results review passes.",
        "selected": False, "approved": False, "executed": False,
    },
]

FUTURE_METHOD_REQUIREMENTS = {
    "source_retry_failure_diagnosis_must_be_ready": True,
    "authoritative_retry_failure_counts_must_be_bound": True,
    "root_regression_must_not_be_treated_as_retry_evidence": True,
    "classification_must_not_rerun_full_retry": True,
    "classification_must_not_create_retry_results_review": True,
    "classification_must_not_mark_integration_successful": True,
    "classification_must_preserve_staged_evidence": True,
    "classification_must_not_regenerate_evidence": True,
    "classification_must_not_call_providers": True,
    "classification_must_record_failure_modules": True,
    "classification_must_record_first_failure_by_pytest_order": True,
    "classification_must_record_first_error_by_pytest_order": True,
    "classification_must_identify_likely_root_cause_families": True,
    "classification_must_separate_missing_evidence_from_path_cwd_digest_and_branch_content_issues": True,
    "classification_outputs_must_be_research_governance_only": True,
    "future_remediation_requires_separate_approval": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}

FUTURE_METHOD_PLAN = [
    "Locate persisted authoritative retry output or status records.",
    "Extract failure and error modules without rerunning full retry.",
    "Identify the first failing test and first error trace by pytest order.",
    "Classify failures into missing ignored evidence root, path/cwd assumption, digest constant drift, branch/content mismatch, import/cache/environment state, test fixture isolation, or unknown/unclassified.",
    "Produce a bounded module-count summary.",
    "Produce a first-order blocker summary.",
    "Identify whether any additional ignored evidence roots are required.",
    "Identify whether failures are test-harness issues or actual integration-content issues.",
    "Recommend one future remediation or method package.",
    "Keep retry, results review, main merge, runtime, and trading authority closed.",
]
FUTURE_METHOD_PLAN_STATUS = "PLANNED_NOT_EXECUTED"

PLANNED_OUTPUT_NAMES = [
    "retry_failure_domain_manifest", "retry_failure_module_summary",
    "first_failure_trace_summary", "first_error_trace_summary",
    "missing_evidence_root_candidate_report", "path_cwd_assumption_candidate_report",
    "digest_constant_drift_candidate_report", "branch_content_mismatch_candidate_report",
    "test_isolation_candidate_report", "recommended_remediation_or_method_summary",
    "digest_manifest",
]
PLANNED_OUTPUTS = [
    {"output_id": name, "status": "PLANNED_NOT_GENERATED"} for name in PLANNED_OUTPUT_NAMES
]

NON_GOALS = [
    "do_not_rerun_retry_now", "do_not_run_full_pytest_now",
    "do_not_treat_diagnostics_as_retry_evidence", "do_not_create_retry_results_review",
    "do_not_create_integration_results_review", "do_not_mark_integration_successful",
    "do_not_generate_successful_integration_digest", "do_not_stage_additional_evidence",
    "do_not_modify_staged_evidence", "do_not_regenerate_evidence", "do_not_call_providers",
    "do_not_commit_marketflow_outputs", "do_not_push_integration_branch", "do_not_push_main",
    "do_not_delete_integration_branch", "do_not_delete_worktree", "do_not_force_push",
    "do_not_modify_tags", "do_not_create_main_merge_approval",
    "do_not_accept_predictive_usefulness", "do_not_accept_profitability",
    "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Retry Failure Remediation or Method Candidate Operator Review v1.",
    "Retry Failure Remediation or Method Approval v1, if selected.",
    "Retry Failure Remediation or Method Execution v1, if approved.",
    "Retry Failure Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "retry_failure_method_operator_review", "retry_failure_method_approval_if_selected",
    "retry_failure_method_execution_if_approved", "retry_failure_method_results_review",
    "new_integration_branch_retry_candidate_after_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "candidate_does_not_rerun_retry", "candidate_does_not_run_full_pytest",
    "candidate_does_not_treat_diagnostics_as_retry_evidence",
    "candidate_does_not_create_retry_results_review", "candidate_does_not_create_integration_results_review",
    "candidate_does_not_mark_integration_successful",
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
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_operator_review_required", "separate_approval_required_before_method_execution",
    "separate_results_review_required_after_method_execution",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_retry_failure_diagnosis_digest_bound", "source_retry_approval_digest_bound",
    "source_retry_operator_review_digest_bound", "source_retry_candidate_digest_bound",
    "source_remediation_results_review_digest_bound", "source_remediation_execution_digest_bound",
    "source_staged_inventory_digest_bound", "retry_execution_commit_bound", "retry_failure_counts_bound",
    "original_failure_comparison_bound", "root_regression_boundary_bound", "origin_main_bound",
    "integration_branch_head_bound", "detached_worktree_head_bound", "staged_evidence_digest_bound",
    "candidate_created_true", "candidate_ready_true", "recommended_package_present",
    "method_packages_present_8", "blocked_packages_present_3", "recommended_package_not_selected",
    "method_selected_false", "method_approved_false", "method_authorized_false",
    "method_executed_false", "new_retry_candidate_created_false", "new_retry_approved_false",
    "new_retry_executed_false", "new_retry_results_review_created_false",
    "main_merge_approval_created_false", "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "future_method_requirements_defined", "future_method_plan_defined", "planned_outputs_defined",
    "non_goals_defined", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(ValueError):
    """Raised when candidate evidence or authority boundaries are invalid."""


def _source_diagnosis() -> dict[str, Any]:
    return {
        "source_retry_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1,
        "source_retry_failure_diagnosis_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY,
        "source_retry_failure_diagnosis_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_retry_failure_diagnosis_digest": SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST,
        "source_retry_approval_digest": SOURCE_RETRY_APPROVAL_DIGEST,
        "source_retry_operator_review_digest": SOURCE_RETRY_OPERATOR_REVIEW_DIGEST,
        "source_retry_candidate_digest": SOURCE_RETRY_CANDIDATE_DIGEST,
        "source_remediation_results_review_digest": SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
        "source_remediation_execution_digest": SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "source_staged_inventory_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "retry_execution_branch": source.RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_command": source.RETRY_PYTEST_COMMAND,
        "retry_pytest_working_directory": source.RETRY_PYTEST_WORKING_DIRECTORY,
        "retry_pytest_ran_from_detached_worktree": True,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_performed": True, "retry_pytest_exit_code": 1,
        "retry_pytest_passed": False, "retry_pytest_failed": True,
        "retry_pytest_passed_count": 24877, "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112, "retry_pytest_skipped_count": 7,
        "original_failed_run_passed_count": 24481, "original_failed_run_failed_count": 1300,
        "original_failed_run_error_count": 500, "original_failed_run_skipped_count": 7,
        "retry_delta_passed_count": 396, "retry_delta_failed_count": -8,
        "retry_delta_error_count": -388, "retry_delta_skipped_count": 0,
        "root_full_regression_passed_count": 29200, "root_full_regression_skipped_count": 7,
        "root_full_regression_is_retry_evidence": False,
        "root_full_regression_does_not_override_detached_retry_failure": True,
        "origin_main_commit": source.ORIGIN_MAIN_COMMIT,
        "integration_branch_name": source.INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": source.INTEGRATION_BRANCH_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": source.RETRY_PYTEST_WORKING_DIRECTORY,
        "detached_integration_worktree_head_commit": source.INTEGRATION_BRANCH_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean": True,
        "staged_evidence_manifest_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
    }


def _base_candidate(source_diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True, "governance_only": True, "candidate_only": True,
        "operator_review_required": True, **deepcopy(dict(source_diagnosis)),
        "retry_failure_candidate_created": True,
        "retry_failure_candidate_ready_for_operator_review": True,
        "ready_for_retry_failure_candidate_operator_review": True,
        "retry_failure_method_selected": False, "retry_failure_method_approved": False,
        "retry_failure_method_authorized": False, "retry_failure_method_executed": False,
        "new_remediation_candidate_created": False, "new_retry_candidate_created": False,
        "new_retry_approved": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "candidate_philosophy": CANDIDATE_PHILOSOPHY, "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL, "method_packages": deepcopy(METHOD_PACKAGES),
        "recommended_retry_failure_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS, "recommendation_reason": RECOMMENDATION_REASON,
        "future_method_requirements": deepcopy(FUTURE_METHOD_REQUIREMENTS),
        "future_method_plan": list(FUTURE_METHOD_PLAN),
        "future_method_plan_status": FUTURE_METHOD_PLAN_STATUS,
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "non_goals": list(NON_GOALS),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = candidate.get("method_packages") if isinstance(candidate.get("method_packages"), list) else []
    recommended = next((row for row in packages if row.get("package_id") == RECOMMENDED_PACKAGE), {})
    blocked = [row for row in packages if str(row.get("status", "")).startswith("BLOCKED_")]
    retry_counts = {"passed": candidate.get("retry_pytest_passed_count"), "failed": candidate.get("retry_pytest_failed_count"), "errors": candidate.get("retry_pytest_error_count"), "skipped": candidate.get("retry_pytest_skipped_count")}
    original_counts = {"passed": candidate.get("original_failed_run_passed_count"), "failed": candidate.get("original_failed_run_failed_count"), "errors": candidate.get("original_failed_run_error_count"), "skipped": candidate.get("original_failed_run_skipped_count")}
    values: dict[str, tuple[Any, Any]] = {
        "source_retry_failure_diagnosis_digest_bound": (SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, candidate.get("source_retry_failure_diagnosis_digest")),
        "source_retry_approval_digest_bound": (SOURCE_RETRY_APPROVAL_DIGEST, candidate.get("source_retry_approval_digest")),
        "source_retry_operator_review_digest_bound": (SOURCE_RETRY_OPERATOR_REVIEW_DIGEST, candidate.get("source_retry_operator_review_digest")),
        "source_retry_candidate_digest_bound": (SOURCE_RETRY_CANDIDATE_DIGEST, candidate.get("source_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, candidate.get("source_remediation_results_review_digest")),
        "source_remediation_execution_digest_bound": (SOURCE_REMEDIATION_EXECUTION_DIGEST, candidate.get("source_remediation_execution_digest")),
        "source_staged_inventory_digest_bound": (SOURCE_STAGED_INVENTORY_DIGEST, candidate.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": (source.RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": (source.RETRY_FAILED_RUN, retry_counts),
        "original_failure_comparison_bound": (source.ORIGINAL_FAILED_RUN, original_counts),
        "root_regression_boundary_bound": ([29200, 7, False, True], [candidate.get("root_full_regression_passed_count"), candidate.get("root_full_regression_skipped_count"), candidate.get("root_full_regression_is_retry_evidence"), candidate.get("root_full_regression_does_not_override_detached_retry_failure")]),
        "origin_main_bound": (source.ORIGIN_MAIN_COMMIT, candidate.get("origin_main_commit")),
        "integration_branch_head_bound": (source.INTEGRATION_BRANCH_HEAD_COMMIT, candidate.get("integration_branch_head_commit")),
        "detached_worktree_head_bound": (source.INTEGRATION_BRANCH_HEAD_COMMIT, candidate.get("detached_integration_worktree_head_commit")),
        "staged_evidence_digest_bound": (SOURCE_STAGED_INVENTORY_DIGEST, candidate.get("staged_evidence_manifest_digest")),
        "candidate_created_true": (True, candidate.get("retry_failure_candidate_created")),
        "candidate_ready_true": (True, candidate.get("retry_failure_candidate_ready_for_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, candidate.get("recommended_retry_failure_method_package")),
        "method_packages_present_8": (8, len(packages)), "blocked_packages_present_3": (3, len(blocked)),
        "recommended_package_not_selected": (False, recommended.get("selected")),
        "method_selected_false": (False, candidate.get("retry_failure_method_selected")),
        "method_approved_false": (False, candidate.get("retry_failure_method_approved")),
        "method_authorized_false": (False, candidate.get("retry_failure_method_authorized")),
        "method_executed_false": (False, candidate.get("retry_failure_method_executed")),
        "new_retry_candidate_created_false": (False, candidate.get("new_retry_candidate_created")),
        "new_retry_approved_false": (False, candidate.get("new_retry_approved")),
        "new_retry_executed_false": (False, candidate.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, candidate.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, candidate.get("main_merge_approval_created")),
        "integration_execution_successful_false": (False, candidate.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, candidate.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, candidate.get("successful_integration_validation_digest_generated")),
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
        "future_method_requirements_defined": (FUTURE_METHOD_REQUIREMENTS, candidate.get("future_method_requirements")),
        "future_method_plan_defined": (FUTURE_METHOD_PLAN, candidate.get("future_method_plan")),
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
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "retry_failure_candidate_created": True,
        "retry_failure_candidate_ready_for_operator_review": True,
        "recommended_retry_failure_method_package": RECOMMENDED_PACKAGE,
        "method_selected": False, "method_approved": False, "method_executed": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "main_merge_approval_created": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic candidate digest."""
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(
    *, source_diagnosis: dict | None = None,
) -> dict:
    """Build an offline candidate from committed retry-failure diagnosis constants."""
    evidence = _source_diagnosis()
    if source_diagnosis is not None:
        if not isinstance(source_diagnosis, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
                "source_diagnosis must be an object"
            )
        evidence.update(deepcopy(source_diagnosis))
    candidate = _base_candidate(evidence)
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"] = (
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate exact source evidence and reject selection, execution, or widened authority."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "candidate must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_source_diagnosis(), "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        "method_packages": METHOD_PACKAGES,
        "recommended_retry_failure_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS, "recommendation_reason": RECOMMENDATION_REASON,
        "future_method_requirements": FUTURE_METHOD_REQUIREMENTS,
        "future_method_plan": FUTURE_METHOD_PLAN, "future_method_plan_status": FUTURE_METHOD_PLAN_STATUS,
        "planned_outputs": PLANNED_OUTPUTS, "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(candidate.get(field), expected, field)
    if not re.fullmatch(r"[0-9a-f]{40}", str(candidate.get("retry_execution_commit", ""))):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "retry_execution_commit invalid"
        )
    required_true = (
        "created_offline", "governance_only", "candidate_only", "operator_review_required",
        "retry_failure_candidate_created", "retry_failure_candidate_ready_for_operator_review",
        "ready_for_retry_failure_candidate_operator_review", "no_tracked_marketflow_files",
    )
    required_false = (
        "root_full_regression_is_retry_evidence", "retry_failure_method_selected",
        "retry_failure_method_approved", "retry_failure_method_authorized", "retry_failure_method_executed",
        "new_remediation_candidate_created", "new_retry_candidate_created", "new_retry_approved",
        "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed",
        "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
        "evidence_regenerated", "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate", "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
    )
    for field in required_true:
        _expect(candidate.get(field), True, field)
    for field in required_false:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    packages = candidate.get("method_packages")
    if not isinstance(packages, list) or len(packages) != 8:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "method packages missing"
        )
    if any(row.get("selected") or row.get("approved") or row.get("executed") for row in packages):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "method package selected, approved, or executed"
        )
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "checklist failed"
        )
    _expect(candidate.get("summary"), _summary(checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": candidate["candidate_status"], "artifact_kind": candidate["artifact_kind"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest": digest,
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated candidate as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(candidate)
    sections = [
        ("Source Retry Failure Diagnosis", [f"Artifact/digest: `{candidate['source_retry_failure_diagnosis_artifact_kind']}` / `{candidate['source_retry_failure_diagnosis_digest']}`."]),
        ("Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The failed retry remains authoritative."]),
        ("Retry Environment", [f"Command: `{candidate['retry_pytest_command']}`.", f"Detached worktree: `{candidate['retry_pytest_working_directory']}`."]),
        ("Candidate Scope", [candidate["candidate_boundary"]]),
        ("Candidate Philosophy", [candidate["candidate_philosophy"], candidate["candidate_goal"]]),
        ("Proposed Method Packages", [f"`{row['package_id']}`: `{row['status']}` — {row['purpose']}" for row in candidate["method_packages"]]),
        ("Recommended Method Package", [f"Package: `{candidate['recommended_retry_failure_method_package']}`.", f"Status: `{candidate['recommendation_status']}`.", candidate["recommendation_reason"]]),
        ("Future Method Requirements", [f"`{key}`: `{value}`" for key, value in candidate["future_method_requirements"].items()]),
        ("Future Method Plan", [f"Status: `{candidate['future_method_plan_status']}`.", *candidate["future_method_plan"]]),
        ("Planned Outputs", [f"`{row['output_id']}`: `{row['status']}`" for row in candidate["planned_outputs"]]),
        ("Non-Goals", [f"`{row}`" for row in candidate["non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No method selection, approval, execution, retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The root regression is not retry evidence.", "Separate operator review and approval are required before any future method execution."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(
    output_dir: str | Path, *, source_diagnosis: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(
        source_diagnosis=source_diagnosis
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateError(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"], "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
