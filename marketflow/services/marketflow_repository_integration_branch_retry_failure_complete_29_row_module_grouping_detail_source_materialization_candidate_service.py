"""Plan complete 29-row detail materialization methods without executing them."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE

SOURCE_DIAGNOSIS_DIGEST = "8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41"
PRIMARY_FAILURE_CLASS = source.PRIMARY_FAILURE_CLASS
RECOMMENDED_PACKAGE = "PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

TOP_FIVE = deepcopy(source.TOP_FIVE)
AVAILABLE_DATA = list(source.AVAILABLE_DATA)
MISSING_DATA = list(source.MISSING_DATA)

CANDIDATE_PHILOSOPHY = (
    "The detail exposure/binding execution failed closed because the committed source chain contains a "
    "recovery-detail digest and summary evidence but not the complete 29-row module grouping payload. "
    "A digest proves evidence identity but is not itself the row-level payload needed for deterministic "
    "after-v2 planning. The next safe step is to choose a controlled materialization or binding method "
    "that creates a planning-ready complete 29-row source without inference, quiet pytest rerun, provider "
    "calls, runtime activation, or main-merge authority."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no materialization, detail exposure, cache read, source recovery, planning reentry, "
    "diagnostics, remediation, retry, results review, main merge, runtime, or trading authority is created."
)
CANDIDATE_GOAL = (
    "Define safe future packages to materialize, expose, or bind the complete 29-row recovered module "
    "grouping source required for deterministic planning reentry."
)


def _packages() -> list[dict[str, Any]]:
    common = {"selected": False, "approved": False, "executed": False}
    rows = [
        {"package": RECOMMENDED_PACKAGE, "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Create a future controlled path that materializes, exposes, or binds the complete 29-row recovered detail source without inference, retry rerun, provider calls, or main-merge authority.", "recommended_for": "The recovered detail identity exists, but the complete row payload is unavailable to live committed binding execution."},
        {"package": "PACKAGE_MATERIALIZE_COMPLETE_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_REQUIRES_SEPARATE_APPROVAL", "purpose": "Reconstruct and commit a bounded non-secret source from reviewed detached pytest cache while preserving hash/count constraints."},
        {"package": "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE_FROM_EXISTING_RECOVERY_ARTIFACT_IF_LOCATABLE", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Use an existing committed all-29-row recovery structure only if locatable and digest-verifiable."},
        {"package": "PACKAGE_OPERATOR_PROVIDES_EXISTING_COMPLETE_RECOVERY_DETAIL_REPORT_PATH", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "purpose": "Bind an operator-provided existing report only if hash-verifiable and consistent with reviewed digests."},
        {"package": "PACKAGE_CREATE_HIGH_CONTROL_29_ROW_SOURCE_CONSTANT_FROM_REVIEWED_RECOVERY_EVIDENCE", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_HIGH_CONTROL_NOT_SELECTED", "purpose": "Add exactly 29 bounded source rows, paths, counts, percentages, tiers, and samples without committing runtime outputs."},
        {"package": "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING", "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_RECOMMENDED", "purpose": "Proceed with top-five paths and aggregate concentration only.", "not_recommended_reason": "It changes the 29-row contract and cannot satisfy deterministic tier validation."},
        {"package": "PACKAGE_USE_RECOVERY_DETAIL_DIGEST_AS_PROXY_FOR_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "A digest proves identity, not the required row payload."},
        {"package": "PACKAGE_INFER_MISSING_24_MODULE_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Paths, counts, and samples must be source-derived."},
        {"package": "PACKAGE_RERUN_PYTEST_TO_RECREATE_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "The failed retry remains authoritative; pytest cannot be quiet source materialization."},
        {"package": "PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_COMPLETE_DETAIL_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Diagnostic capture remains separately gated after materialization review."},
        {"package": "PACKAGE_NEW_RETRY_DESPITE_BLOCKED_DETAIL_BINDING", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "A new retry remains blocked until remediation/method review."},
        {"package": "PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_DETAIL_BINDING_AND_FAILED_RETRY", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Main merge requires a passing future retry results review."},
    ]
    return [{**row, **common} for row in rows]


FUTURE_REQUIREMENTS = [
    "source_diagnosis_must_be_ready", "source_diagnosis_digest_must_be_bound",
    "source_primary_failure_class_must_be_bound", "source_detail_binding_blocked_execution_must_be_bound",
    "source_detail_binding_blocked_manifest_must_be_bound", "source_detail_binding_blocked_reason_must_be_bound",
    "source_detail_binding_approval_must_be_bound", "source_recovery_results_review_must_be_ready",
    "source_recovery_detail_digest_must_be_bound", "source_recovery_manifest_digest_must_be_bound",
    "retry_failure_counts_must_be_bound", "recovered_module_summary_must_be_bound",
    "top_five_paths_and_counts_must_be_bound", "top_five_and_top_ten_concentration_must_be_bound",
    "complete_29_row_payload_source_must_be_identified", "complete_29_row_payload_must_not_be_inferred",
    "complete_29_row_payload_must_include_exactly_29_rows", "complete_29_row_payload_must_sum_to_1404",
    "complete_29_row_payload_must_preserve_top_five_counts", "complete_29_row_payload_must_preserve_top_five_sum_612",
    "complete_29_row_payload_must_preserve_top_ten_sum_1069", "complete_29_row_payload_must_preserve_tier_sums_612_457_335",
    "module_paths_must_be_source_derived", "per_module_counts_must_be_source_derived",
    "bounded_nodeid_samples_must_be_source_derived", "bounded_nodeid_samples_must_not_exceed_5_per_module",
    "unsupported_claims_boundary_must_be_preserved", "materialization_must_not_treat_digest_as_payload",
    "materialization_must_not_infer_missing_rows", "materialization_must_not_rerun_retry",
    "materialization_must_not_run_full_pytest", "materialization_must_not_execute_diagnostics",
    "materialization_must_not_execute_remediation", "materialization_must_not_claim_root_cause",
    "materialization_must_not_recommend_direct_code_remediation", "materialization_must_not_treat_detail_as_retry_success",
    "materialization_must_not_commit_pytest_cache", "materialization_must_not_commit_marketflow_outputs",
    "materialization_must_preserve_origin_main", "materialization_must_preserve_integration_branch",
    "materialization_must_preserve_staged_evidence", "future_materialization_execution_requires_separate_approval",
    "future_materialization_results_review_required", "future_detail_binding_reattempt_requires_materialization_results_review",
    "future_after_v2_planning_reentry_requires_complete_detail_review", "future_retry_requires_separate_approval",
    "main_merge_requires_passing_retry_results_review",
]

FUTURE_PLAN = [
    "Bind this candidate source diagnosis, blocked detail-binding execution, and blocked reason.",
    "Bind source recovery results-review digest and recovered detail digest.",
    "Select one controlled complete-detail materialization or binding source.",
    "Verify the selected source contains exactly 29 module rows.",
    "Verify total failed-or-errored node IDs equals 1,404.",
    "Verify top-five counts, top-five sum, top-ten sum, and tier sums.",
    "Verify module paths, per-module counts, and bounded samples are source-derived.",
    "Produce a bounded complete 29-row source suitable for planning reentry.",
    "Preserve unsupported claims: no failure/error separation, first-order claim, traceback root cause, direct remediation, retry success, or main-merge readiness.",
    "Require materialization results review before detail-binding reattempt.",
    "Reattempt detail exposure/binding only after materialization results review.",
    "Keep diagnostic capture, retry, main merge, runtime, and trading closed.",
]

PLANNED_OUTPUTS = [
    "complete_29_row_materialization_candidate_manifest", "complete_29_row_payload_source_selection_report",
    "complete_29_row_payload_integrity_requirements", "source_derived_module_paths_requirement_report",
    "per_module_counts_requirement_report", "bounded_nodeid_samples_requirement_report",
    "top_module_concentration_preservation_plan", "tier_sum_preservation_plan", "digest_is_not_payload_report",
    "unsupported_claims_boundary_report", "materialization_limitations_report",
    "detail_binding_reattempt_enablement_report", "recommended_next_package_report", "digest_manifest",
]

NON_GOALS = [
    "do_not_materialize_29_row_source_now", "do_not_expose_29_module_rows_now", "do_not_bind_complete_detail_now",
    "do_not_recover_module_grouping_now", "do_not_read_cache_now", "do_not_modify_cache_now",
    "do_not_parse_operator_logs_now", "do_not_run_diagnostic_commands_now", "do_not_execute_diagnostics_now",
    "do_not_execute_remediation_now", "do_not_execute_classification_now", "do_not_classify_modules_again_now",
    "do_not_execute_detail_binding_now", "do_not_execute_after_v2_planning_reentry_now", "do_not_rerun_retry_now",
    "do_not_run_full_pytest_now", "do_not_create_targeted_diagnostic_candidate_now",
    "do_not_create_new_retry_candidate_now", "do_not_create_retry_results_review",
    "do_not_create_integration_results_review", "do_not_mark_integration_successful",
    "do_not_claim_failure_error_separation", "do_not_claim_first_failure", "do_not_claim_first_error",
    "do_not_claim_traceback_root_cause", "do_not_recommend_direct_code_remediation",
    "do_not_treat_digest_as_payload", "do_not_treat_materialization_as_retry_success",
    "do_not_push_integration_branch", "do_not_push_main", "do_not_commit_marketflow_outputs",
    "do_not_commit_pytest_cache", "do_not_modify_staged_evidence", "do_not_regenerate_evidence",
    "do_not_call_providers", "do_not_accept_predictive_usefulness", "do_not_accept_profitability",
    "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Complete 29-row Module Grouping Detail Source Materialization Candidate Operator Review v1.",
    "Materialization Approval v1, if selected.", "Materialization Execution v1, if approved.",
    "Materialization Results Review v1.", "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.", "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review",
    "complete_29_row_module_grouping_detail_source_materialization_approval_if_selected",
    "complete_29_row_module_grouping_detail_source_materialization_execution_if_approved",
    "complete_29_row_module_grouping_detail_source_materialization_results_review",
    "detail_exposure_or_binding_execution_reattempt_with_complete_source", "detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported", "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected", "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "candidate_materialization_does_not_materialize_29_row_source", "candidate_materialization_does_not_expose_29_module_rows",
    "candidate_materialization_does_not_bind_complete_detail", "candidate_materialization_does_not_recover_module_grouping_again",
    "candidate_materialization_does_not_read_cache", "candidate_materialization_does_not_modify_cache",
    "candidate_materialization_does_not_parse_operator_logs", "candidate_materialization_does_not_run_diagnostic_commands",
    "candidate_materialization_does_not_execute_diagnostics", "candidate_materialization_does_not_execute_remediation",
    "candidate_materialization_does_not_execute_classification", "candidate_materialization_does_not_classify_modules_again",
    "candidate_materialization_does_not_execute_detail_binding", "candidate_materialization_does_not_execute_after_v2_planning_reentry",
    "candidate_materialization_does_not_rerun_retry", "candidate_materialization_does_not_run_full_pytest",
    "candidate_materialization_does_not_create_targeted_diagnostic_candidate", "candidate_materialization_does_not_create_new_retry_candidate",
    "candidate_materialization_does_not_create_retry_results_review", "candidate_materialization_does_not_create_integration_results_review",
    "candidate_materialization_does_not_mark_integration_successful", "candidate_materialization_does_not_generate_successful_integration_digest",
    "candidate_materialization_does_not_claim_failure_error_separation", "candidate_materialization_does_not_claim_first_failure",
    "candidate_materialization_does_not_claim_first_error", "candidate_materialization_does_not_claim_traceback_root_cause",
    "candidate_materialization_does_not_recommend_direct_code_remediation", "candidate_materialization_does_not_treat_digest_as_payload",
    "candidate_materialization_does_not_treat_detail_as_retry_success", "candidate_materialization_does_not_push_integration_branch",
    "candidate_materialization_does_not_push_main", "candidate_materialization_does_not_delete_integration_branch",
    "candidate_materialization_does_not_delete_worktree", "candidate_materialization_does_not_force_push",
    "candidate_materialization_does_not_prune_remotes", "candidate_materialization_does_not_modify_tags",
    "candidate_materialization_does_not_modify_staged_evidence", "candidate_materialization_does_not_regenerate_evidence",
    "candidate_materialization_does_not_call_providers", "candidate_materialization_does_not_acquire_market_data",
    "candidate_materialization_does_not_regenerate_dataset", "candidate_materialization_does_not_recompute_metrics",
    "candidate_materialization_does_not_train_models", "candidate_materialization_does_not_score_strategy",
    "candidate_materialization_does_not_generate_recommendations", "candidate_materialization_does_not_accept_predictive_usefulness",
    "candidate_materialization_does_not_accept_profitability", "candidate_materialization_does_not_authorize_runtime",
    "candidate_materialization_does_not_authorize_broker_execution",
    "complete_detail_materialization_output_would_be_planning_source_not_root_cause",
    "digest_only_is_not_complete_detail_payload", "top_five_only_is_not_complete_29_row_source",
    "complete_detail_gap_is_not_retry_success", "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence", "separate_operator_review_required",
    "separate_approval_required_before_materialization_execution", "separate_results_review_required_after_materialization",
    "separate_detail_binding_reattempt_required_after_materialization_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "materialization_package_selected", "materialization_package_approved", "materialization_package_authorized",
    "materialization_package_executed", "complete_29_row_detail_materialized", "complete_29_row_detail_exposed",
    "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
    "module_grouping_detail_materialized_by_candidate", "module_paths_recovered_by_candidate",
    "per_module_counts_recovered_by_candidate", "bounded_nodeid_samples_recovered_by_candidate",
    "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "source_recovery_rerun_performed", "cache_read_in_candidate",
    "module_grouping_recovered_in_candidate", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed", "classification_execution_performed_in_candidate",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError(ValueError):
    """Raised when the candidate violates its committed-evidence boundary."""


def _committed_source_diagnosis() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "diagnosis_status": source.DIAGNOSIS_STATUS,
        "diagnosis_scope": source.DIAGNOSIS_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_digest": SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "recommended_next_package": RECOMMENDED_PACKAGE,
        "source_detail_exposure_or_binding_execution_blocked_digest": source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_detail_exposure_or_binding_execution_blocked_manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": source.SOURCE_BLOCKED_REASON,
        "source_detail_exposure_or_binding_approval_digest": source.SOURCE_APPROVAL_DIGEST,
        "source_detail_exposure_or_binding_operator_review_digest": source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_detail_exposure_or_binding_candidate_digest": source.SOURCE_CANDIDATE_DIGEST,
        "source_reentry_failure_diagnosis_digest": source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST,
        "source_primary_failure_class": source.SOURCE_PRIMARY_FAILURE_CLASS,
        "source_reentry_execution_blocked_digest": source.SOURCE_REENTRY_BLOCKED_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": source.SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST,
        "source_reentry_execution_blocked_reason": source.SOURCE_REENTRY_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": source.SOURCE_PLANNING_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_RECOVERY_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.SOURCE_RECOVERY_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.SOURCE_RECOVERY_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST,
        "source_after_v2_approval_digest": source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_approval_v2_digest": source.SOURCE_APPROVAL_V2_DIGEST,
        "source_staged_inventory_digest": source.SOURCE_STAGED_INVENTORY_DIGEST,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "recovered_module_grouping_source_summary": {"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]},
        "top_module_summary": deepcopy(TOP_FIVE), "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "source_execution_available_data": list(AVAILABLE_DATA), "source_execution_missing_data": list(MISSING_DATA),
        "actual_live_detail_binding_source_lacks_complete_29_rows": True,
        "detail_binding_success_path_tested_with_complete_29_row_snapshot": True,
    }


def _validate_source(diagnosis: Mapping[str, Any]) -> None:
    mismatches = [key for key, value in _committed_source_diagnosis().items() if diagnosis.get(key) != value]
    if mismatches:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError(
            f"source diagnosis mismatch: {', '.join(mismatches)}"
        )


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    blocked_packages = [item for item in candidate.get("proposed_packages", []) if item.get("status") == "BLOCKED_NOT_ALLOWED"]
    planned_outputs_ok = all(candidate.get("planned_outputs", {}).get(name) == PLANNED_NOT_GENERATED for name in PLANNED_OUTPUTS)
    requirements_ok = all(candidate.get("future_materialization_or_binding_requirements", {}).get(name) is True for name in FUTURE_REQUIREMENTS)
    pairs: dict[str, tuple[Any, Any]] = {
        "source_diagnosis_digest_bound": (SOURCE_DIAGNOSIS_DIGEST, candidate.get("source_detail_exposure_or_binding_execution_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (PRIMARY_FAILURE_CLASS, candidate.get("primary_failure_class")),
        "source_detail_binding_execution_blocked_digest_bound": (source.SOURCE_BLOCKED_EXECUTION_DIGEST, candidate.get("source_detail_exposure_or_binding_execution_blocked_digest")),
        "source_detail_binding_execution_blocked_manifest_digest_bound": (source.SOURCE_BLOCKED_MANIFEST_DIGEST, candidate.get("source_detail_exposure_or_binding_execution_blocked_manifest_digest")),
        "source_detail_binding_execution_blocked_reason_bound": (source.SOURCE_BLOCKED_REASON, candidate.get("blocked_reason")),
        "source_detail_binding_approval_digest_bound": (source.SOURCE_APPROVAL_DIGEST, candidate.get("source_detail_exposure_or_binding_approval_digest")),
        "source_detail_binding_operator_review_digest_bound": (source.SOURCE_OPERATOR_REVIEW_DIGEST, candidate.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_detail_binding_candidate_digest_bound": (source.SOURCE_CANDIDATE_DIGEST, candidate.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_reentry_failure_diagnosis_digest_bound": (source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST, candidate.get("source_reentry_failure_diagnosis_digest")),
        "source_reentry_failure_primary_failure_class_bound": (source.SOURCE_PRIMARY_FAILURE_CLASS, candidate.get("source_primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (source.SOURCE_REENTRY_BLOCKED_DIGEST, candidate.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (source.SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST, candidate.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (source.SOURCE_REENTRY_BLOCKED_REASON, candidate.get("source_reentry_execution_blocked_reason")),
        "source_planning_reentry_digest_bound": (source.SOURCE_PLANNING_REENTRY_DIGEST, candidate.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, candidate.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST, candidate.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.SOURCE_RECOVERY_EXECUTION_DIGEST, candidate.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.SOURCE_RECOVERY_DETAIL_DIGEST, candidate.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST, candidate.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST, candidate.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST, candidate.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (source.SOURCE_AFTER_V2_APPROVAL_DIGEST, candidate.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (source.SOURCE_RESULTS_REVIEW_V2_DIGEST, candidate.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.SOURCE_EXECUTION_V2_DIGEST, candidate.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.SOURCE_MODULE_GROUPING_DIGEST, candidate.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (source.RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": ({"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]}, candidate.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (TOP_FIVE, candidate.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, candidate.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, candidate.get("top_10_count_sum")),
        "available_data_recorded": (AVAILABLE_DATA, candidate.get("source_execution_available_data")),
        "missing_data_recorded": (MISSING_DATA, candidate.get("source_execution_missing_data")),
        "actual_live_detail_binding_source_lacks_complete_29_rows_true": (True, candidate.get("actual_live_detail_binding_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, candidate.get("detail_binding_success_path_tested_with_complete_29_row_snapshot")),
        "recommended_package_from_diagnosis_bound": (RECOMMENDED_PACKAGE, candidate.get("recommended_next_package_from_diagnosis")),
        "candidate_created_true": (True, candidate.get("complete_29_row_module_grouping_detail_source_materialization_candidate_created")),
        "candidate_ready_true": (True, candidate.get("complete_29_row_module_grouping_detail_source_materialization_candidate_ready_for_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, candidate.get("recommended_complete_29_row_materialization_package")),
        "packages_present_12": (12, len(candidate.get("proposed_packages", []))),
        "blocked_packages_present_6": (6, len(blocked_packages)),
        "recommended_package_not_selected": (False, candidate.get("recommended_package", {}).get("selected")),
        "future_requirements_defined": (True, requirements_ok),
        "future_plan_defined": (FUTURE_PLAN, candidate.get("future_materialization_or_binding_plan", {}).get("steps")),
        "planned_outputs_defined": (True, planned_outputs_ok),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (False, candidate.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, candidate.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
    }
    pairs.update({f"{field}_false": (False, candidate.get(field)) for field in FALSE_BOUNDARIES})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(candidate: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    keys = [
        "complete_29_row_module_grouping_detail_source_materialization_candidate_created",
        "complete_29_row_module_grouping_detail_source_materialization_candidate_ready_for_operator_review",
        "recommended_complete_29_row_materialization_package", "materialization_package_selected",
        "materialization_package_approved", "materialization_package_executed", "complete_29_row_detail_materialized",
        "complete_29_row_detail_exposed", "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
        "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
        "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful", "recommended_next_task",
    ]
    summary = {"total_checks": len(checklist), "passed_checks": len(checklist) - len(failed), "failed_checks": len(failed), "blocker_count": len(failed)}
    summary.update({key: candidate.get(key) for key in keys})
    summary.update({"predictive_usefulness_accepted": False, "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False})
    return summary


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(
    *, source_diagnosis: dict | None = None,
) -> dict:
    """Build a candidate that proposes source materialization but performs none."""

    diagnosis = deepcopy(source_diagnosis) if source_diagnosis is not None else _committed_source_diagnosis()
    _validate_source(diagnosis)
    packages = _packages()
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_detail_exposure_or_binding_execution_failure_diagnosis_artifact_kind": diagnosis["artifact_kind"],
        "source_detail_exposure_or_binding_execution_failure_diagnosis_status": diagnosis["diagnosis_status"],
        "source_detail_exposure_or_binding_execution_failure_diagnosis_scope": diagnosis["diagnosis_scope"],
        "source_detail_exposure_or_binding_execution_failure_diagnosis_digest": SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "recommended_next_package_from_diagnosis": RECOMMENDED_PACKAGE,
    }
    source_fields = _committed_source_diagnosis()
    for key, value in source_fields.items():
        if key not in {"artifact_kind", "diagnosis_status", "diagnosis_scope", "primary_failure_class", "recommended_next_package"}:
            candidate[key] = deepcopy(value)
    candidate.update({
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_pytest_working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False, "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "diagnosis_findings_summary": [
            "The approved detail-binding execution correctly failed closed.",
            "Committed evidence preserves the recovery-detail digest and aggregate summaries but not all 29 rows.",
            "A digest or top-five subset cannot substitute for a complete deterministic planning payload.",
            "A separately reviewed and approved materialization or binding method is the next safe step.",
        ],
        "candidate_philosophy": CANDIDATE_PHILOSOPHY, "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL, "proposed_packages": packages,
        "recommended_package": deepcopy(packages[0]),
        "recommended_complete_29_row_materialization_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": "The valid recovery chain lacks a live complete row payload. Controlled materialization or binding addresses that source-payload gap without inference, pytest rerun, gate bypass, or runtime authority.",
        "future_materialization_or_binding_requirements": {name: True for name in FUTURE_REQUIREMENTS},
        "future_materialization_or_binding_plan": {"status": PLANNED_NOT_EXECUTED, "steps": list(FUTURE_PLAN)},
        "planned_outputs": {name: PLANNED_NOT_GENERATED for name in PLANNED_OUTPUTS},
        "non_goals": list(NON_GOALS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "complete_29_row_module_grouping_detail_source_materialization_candidate_created": True,
        "complete_29_row_module_grouping_detail_source_materialization_candidate_ready_for_operator_review": True,
        "ready_for_complete_29_row_materialization_operator_review": True,
        "actual_live_detail_binding_source_lacks_complete_29_rows": True,
        "detail_binding_success_path_implemented_with_injected_snapshot": True,
        "detail_binding_success_path_tested_with_complete_29_row_snapshot": True,
        "success_path_expected_tier_sums": {"tier_1": 612, "tier_2": 457, "tier_3": 335},
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "staged_evidence_manifest_digest": source.SOURCE_STAGED_INVENTORY_DIGEST, "staged_evidence_unchanged": True,
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
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    })
    candidate.update({key: False for key in FALSE_BOUNDARIES})
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate, candidate["checklist"])
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest"
    candidate[digest_key] = _candidate_digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, package boundaries, plans, and candidate digest."""

    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError("candidate must be object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "source_detail_exposure_or_binding_execution_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_detail_exposure_or_binding_execution_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_detail_exposure_or_binding_execution_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
    }
    for field, expected in fixed.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError(f"{field} mismatch")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError("checklist invalid")
    summary = _summary(candidate, checklist)
    if candidate.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError("summary invalid")
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest"
    digest = candidate.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _candidate_digest(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError("candidate digest invalid")
    return {
        "artifact_kind": candidate["artifact_kind"], "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"], "candidate_digest": digest,
        **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_markdown_v1(
    candidate: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(candidate)
    sections = [
        ("Source Execution Failure Diagnosis", [SOURCE_DIAGNOSIS_DIGEST, PRIMARY_FAILURE_CLASS]),
        ("Source Blocked Detail Exposure or Binding Execution", [source.SOURCE_BLOCKED_EXECUTION_DIGEST, source.SOURCE_BLOCKED_MANIFEST_DIGEST, source.SOURCE_BLOCKED_REASON]),
        ("Source Approval and Operator Review", [source.SOURCE_APPROVAL_DIGEST, source.SOURCE_OPERATOR_REVIEW_DIGEST, source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Reentry Failure Diagnosis", [source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST, source.SOURCE_PRIMARY_FAILURE_CLASS]),
        ("Source Recovery Results Review", [source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, source.SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; first retry result remains authoritative."]),
        ("Recovered Module Grouping Source Summary", [str(candidate["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Detail Source", [*AVAILABLE_DATA, *MISSING_DATA]),
        ("Candidate Scope", [CANDIDATE_SCOPE, CANDIDATE_BOUNDARY]),
        ("Candidate Philosophy", [CANDIDATE_PHILOSOPHY, CANDIDATE_GOAL]),
        ("Proposed Materialization or Binding Packages", [f"{item['package']}: {item['status']}" for item in candidate["proposed_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, candidate["recommendation_reason"]]),
        ("Future Materialization or Binding Requirements", list(candidate["future_materialization_or_binding_requirements"])),
        ("Future Materialization or Binding Plan", candidate["future_materialization_or_binding_plan"]["steps"]),
        ("Planned Outputs", [f"{key}: {value}" for key, value in candidate["planned_outputs"].items()]),
        ("Non-Goals", candidate["non_goals"]), ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]), ("Risk Controls", candidate["risk_controls"]),
        ("Authority Boundaries", ["Candidate only: no materialization, cache read, recovery, binding, planning, retry, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["A digest is not row payload; the source gap is neither retry success nor original-failure root cause evidence."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Candidate v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(
    output_dir: str | Path, *, source_diagnosis: dict | None = None,
) -> dict:
    candidate = build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(source_diagnosis=source_diagnosis)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1.md"
    json_path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_markdown_v1(candidate),
        encoding="utf-8",
    )
    return {"artifact": candidate, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = [
    "ARTIFACT_KIND", "CANDIDATE_STATUS", "CANDIDATE_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_MATERIALIZATION_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1",
    "write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_markdown_v1",
]
