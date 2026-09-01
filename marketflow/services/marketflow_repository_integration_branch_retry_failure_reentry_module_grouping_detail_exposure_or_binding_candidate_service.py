"""Propose controlled module-detail exposure or binding methods without execution."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1"
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE

SOURCE_DIAGNOSIS_DIGEST = "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb"
PRIMARY_FAILURE_CLASS = source.PRIMARY_FAILURE_CLASS
RECOMMENDED_PACKAGE = source.RECOMMENDED_NEXT_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_OPERATOR_REVIEW_V1"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
NOT_ACCEPTED = source.NOT_ACCEPTED
NOT_AUTHORIZED = source.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_PHILOSOPHY = (
    "The reentry execution failed closed because the live committed reentry source did not expose the complete "
    "29-row recovered module grouping detail, even though source recovery execution and results review had "
    "recovered and accepted the detail. The next safe step is to select a controlled exposure or binding method "
    "that carries forward the complete recovered module grouping detail without cache reread, pytest rerun, "
    "inference, diagnostics, remediation, or retry."
)
CANDIDATE_BOUNDARY = "Candidate-only; no detail exposure, source recovery, cache read, planning execution, diagnostics, remediation, retry, results review, main merge, runtime, or trading authority is created."
CANDIDATE_GOAL = "Define safe future packages to expose, bind, or carry forward the complete recovered module grouping detail required for deterministic after-v2 planning reentry."


def _package(package: str, status: str, purpose: str, **extra: str) -> dict[str, Any]:
    return {"package": package, "status": status, "purpose": purpose, "selected": False, "approved": False, "executed": False, **extra}


PROPOSED_PACKAGES = [
    _package(RECOMMENDED_PACKAGE, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Create a future controlled execution path that exposes, binds, or carries forward the complete 29-row recovered module grouping detail so after-v2 planning reentry can execute without cache read, source recovery rerun, or invented module identities.", recommended_for="The diagnosis identified a committed reentry source-detail gap, not an invalid recovery. The safest next step is a controlled detail exposure or binding package."),
    _package("PACKAGE_EXPOSE_COMPLETE_29_ROW_DETAIL_FROM_SOURCE_RECOVERY_EXECUTION_ARTIFACT", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Expose the complete 29-row recovered module grouping detail directly from the existing source recovery execution artifact if the detail is already available in committed constants or source structures."),
    _package("PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL", "Create a bounded committed status/source artifact carrying the complete 29-row module paths, counts, percentages, and bounded samples, without committing `.pytest_cache` or `.marketflow`."),
    _package("PACKAGE_USE_OPERATOR_PROVIDED_RECOVERY_DETAIL_REPORT_PATH", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "Allow the operator to provide an explicit path to a previously generated recovered module grouping detail report, then expose it only if hash-verifiable and consistent with reviewed digests."),
    _package("PACKAGE_RECONSTRUCT_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_REQUIRES_SEPARATE_APPROVAL", "Reconstruct the full 29-row detail again from reviewed detached pytest cache only under separate approval, if existing committed recovery detail cannot be exposed or bound."),
    _package("PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING_REENTRY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_RECOMMENDED", "Proceed with only the top-five module paths and concentration facts already exposed.", not_recommended_reason="This would change the original 29-row planning contract and would not support full deterministic priority-tier planning."),
    _package("PACKAGE_INFER_MISSING_24_MODULES", "BLOCKED_NOT_ALLOWED", "Infer missing module identities from counts, digests, naming patterns, or intuition.", blocked_reason="Module paths and samples must come from verified source evidence, not inference or fabrication."),
    _package("PACKAGE_RERUN_PYTEST_TO_RECREATE_DETAIL", "BLOCKED_NOT_ALLOWED", "Rerun pytest to recreate cache or module grouping detail.", blocked_reason="The failed retry remains authoritative. Re-running pytest would create a new retry-like event and cannot be used as detail exposure under this candidate."),
    _package("PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_REENTRY_REVIEW", "BLOCKED_NOT_ALLOWED", "Skip detail exposure and proceed directly to diagnostic output capture.", blocked_reason="Diagnostic capture must remain separately gated and should not bypass the blocked planning reentry chain."),
    _package("PACKAGE_NEW_RETRY_DESPITE_BLOCKED_REENTRY", "BLOCKED_NOT_ALLOWED", "Create a new retry despite blocked planning reentry.", blocked_reason="A new retry remains blocked until the remediation/method planning path completes and is reviewed."),
    _package("PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_REENTRY_AND_FAILED_RETRY", "BLOCKED_NOT_ALLOWED", "Proceed to main merge despite failed retry and unresolved planning reentry.", blocked_reason="Main merge approval remains blocked until a future retry results review passes."),
]

FUTURE_REQUIREMENTS = {
    key: True for key in [
        "source_diagnosis_must_be_ready", "source_diagnosis_digest_must_be_bound",
        "source_blocked_reentry_execution_digest_must_be_bound", "source_blocked_reentry_manifest_digest_must_be_bound",
        "source_blocked_reentry_reason_must_be_bound", "source_recovery_results_review_must_be_ready",
        "source_recovery_detail_digest_must_be_bound", "source_recovery_manifest_digest_must_be_bound",
        "complete_29_row_detail_source_must_be_identified", "complete_29_row_detail_must_not_be_inferred",
        "module_paths_must_be_source_derived", "per_module_counts_must_be_source_derived",
        "bounded_nodeid_samples_must_be_source_derived", "top_five_and_top_ten_concentration_must_be_preserved",
        "unsupported_claims_boundary_must_be_preserved", "detail_exposure_must_not_rerun_retry",
        "detail_exposure_must_not_run_full_pytest", "detail_exposure_must_not_execute_diagnostics",
        "detail_exposure_must_not_execute_remediation", "detail_exposure_must_not_claim_root_cause",
        "detail_exposure_must_not_recommend_direct_code_remediation", "detail_exposure_must_not_treat_detail_as_retry_success",
        "detail_exposure_must_not_commit_pytest_cache", "detail_exposure_must_not_commit_marketflow_outputs",
        "detail_exposure_must_preserve_origin_main", "detail_exposure_must_preserve_integration_branch",
        "detail_exposure_must_preserve_staged_evidence", "future_detail_exposure_results_review_required",
        "future_after_v2_planning_reentry_requires_detail_exposure_results_review",
        "future_retry_requires_separate_approval", "main_merge_requires_passing_retry_results_review",
    ]
}

FUTURE_PLAN = [
    "Bind diagnosis digest, blocked reentry execution digest, and blocked reason.",
    "Bind source recovery results-review digest and recovered detail digest.",
    "Select one controlled exposure or binding source.", "Verify the selected source contains all 29 module rows.",
    "Verify module paths, per-module counts, bounded samples, top-five concentration, and top-ten concentration.",
    "Produce or expose a bounded complete 29-row module grouping source suitable for planning reentry.",
    "Preserve no failure/error separation, first-order, traceback-root-cause, direct-remediation, retry-success, or main-merge-readiness claims.",
    "Require detail exposure/binding results review.",
    "Re-enter after-v2 planning execution only after results review.",
    "Keep diagnostic capture, retry, main merge, runtime, and trading closed.",
]

PLANNED_OUTPUT_IDS = [
    "detail_exposure_or_binding_candidate_manifest", "complete_29_row_source_identification_report",
    "complete_module_grouping_detail_binding_plan", "recovered_module_paths_binding_plan",
    "per_module_counts_binding_plan", "bounded_nodeid_samples_binding_plan",
    "top_module_concentration_preservation_plan", "unsupported_claims_boundary_report",
    "detail_exposure_limitations_report", "planning_reentry_enablement_report",
    "recommended_next_package_report", "digest_manifest",
]

NON_GOALS = [
    "do_not_expose_29_module_rows_now", "do_not_bind_complete_detail_now",
    "do_not_recover_module_grouping_now", "do_not_read_cache_now", "do_not_modify_cache_now",
    "do_not_parse_operator_logs_now", "do_not_run_diagnostic_commands_now", "do_not_execute_diagnostics_now",
    "do_not_execute_remediation_now", "do_not_execute_classification_now", "do_not_classify_modules_again_now",
    "do_not_execute_after_v2_planning_reentry_now", "do_not_rerun_retry_now", "do_not_run_full_pytest_now",
    "do_not_create_new_retry_candidate_now", "do_not_create_retry_results_review",
    "do_not_create_integration_results_review", "do_not_mark_integration_successful",
    "do_not_claim_failure_error_separation", "do_not_claim_first_failure", "do_not_claim_first_error",
    "do_not_claim_traceback_root_cause", "do_not_recommend_direct_code_remediation",
    "do_not_treat_recovered_detail_as_retry_success", "do_not_push_integration_branch", "do_not_push_main",
    "do_not_commit_marketflow_outputs", "do_not_commit_pytest_cache", "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability", "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Reentry Module Grouping Detail Exposure or Binding Candidate Operator Review v1.",
    "Detail Exposure or Binding Approval v1, if selected.", "Detail Exposure or Binding Execution v1, if approved.",
    "Detail Exposure or Binding Results Review v1.", "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "reentry_module_grouping_detail_exposure_or_binding_candidate_operator_review",
    "reentry_module_grouping_detail_exposure_or_binding_approval_if_selected",
    "reentry_module_grouping_detail_exposure_or_binding_execution_if_approved",
    "reentry_module_grouping_detail_exposure_or_binding_results_review",
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
    "candidate_detail_binding_does_not_expose_29_module_rows", "candidate_detail_binding_does_not_bind_complete_detail",
    "candidate_detail_binding_does_not_recover_module_grouping_again", "candidate_detail_binding_does_not_read_cache",
    "candidate_detail_binding_does_not_modify_cache", "candidate_detail_binding_does_not_parse_operator_logs",
    "candidate_detail_binding_does_not_run_diagnostic_commands", "candidate_detail_binding_does_not_execute_diagnostics",
    "candidate_detail_binding_does_not_execute_remediation", "candidate_detail_binding_does_not_execute_classification",
    "candidate_detail_binding_does_not_classify_modules_again", "candidate_detail_binding_does_not_execute_after_v2_planning_reentry",
    "candidate_detail_binding_does_not_rerun_retry", "candidate_detail_binding_does_not_run_full_pytest",
    "candidate_detail_binding_does_not_create_new_retry_candidate", "candidate_detail_binding_does_not_create_retry_results_review",
    "candidate_detail_binding_does_not_create_integration_results_review", "candidate_detail_binding_does_not_mark_integration_successful",
    "candidate_detail_binding_does_not_generate_successful_integration_digest", "candidate_detail_binding_does_not_claim_failure_error_separation",
    "candidate_detail_binding_does_not_claim_first_failure", "candidate_detail_binding_does_not_claim_first_error",
    "candidate_detail_binding_does_not_claim_traceback_root_cause", "candidate_detail_binding_does_not_recommend_direct_code_remediation",
    "candidate_detail_binding_does_not_treat_recovered_detail_as_retry_success", "candidate_detail_binding_does_not_push_integration_branch",
    "candidate_detail_binding_does_not_push_main", "candidate_detail_binding_does_not_delete_integration_branch",
    "candidate_detail_binding_does_not_delete_worktree", "candidate_detail_binding_does_not_force_push",
    "candidate_detail_binding_does_not_prune_remotes", "candidate_detail_binding_does_not_modify_tags",
    "candidate_detail_binding_does_not_modify_staged_evidence", "candidate_detail_binding_does_not_regenerate_evidence",
    "candidate_detail_binding_does_not_call_providers", "candidate_detail_binding_does_not_acquire_market_data",
    "candidate_detail_binding_does_not_regenerate_dataset", "candidate_detail_binding_does_not_recompute_metrics",
    "candidate_detail_binding_does_not_train_models", "candidate_detail_binding_does_not_score_strategy",
    "candidate_detail_binding_does_not_generate_recommendations", "candidate_detail_binding_does_not_accept_predictive_usefulness",
    "candidate_detail_binding_does_not_accept_profitability", "candidate_detail_binding_does_not_authorize_runtime",
    "candidate_detail_binding_does_not_authorize_broker_execution", "detail_exposure_output_would_be_planning_source_not_root_cause",
    "source_detail_gap_is_not_retry_success", "source_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence", "separate_operator_review_required",
    "separate_approval_required_before_detail_exposure_execution", "separate_results_review_required_after_detail_exposure",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "detail_exposure_or_binding_selected", "detail_exposure_or_binding_approved",
    "detail_exposure_or_binding_authorized", "detail_exposure_or_binding_executed",
    "complete_29_row_detail_exposed", "complete_29_row_detail_bound",
    "module_grouping_detail_exposed_by_candidate", "module_paths_recovered_by_candidate",
    "per_module_counts_recovered_by_candidate", "bounded_nodeid_samples_recovered_by_candidate",
    "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "source_recovery_rerun_performed",
    "cache_read_in_candidate", "module_grouping_recovered_in_candidate", "retry_rerun_performed",
    "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
    "diagnostic_method_executed", "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_candidate", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError(ValueError):
    """Raised when a candidate violates its committed-evidence or authority contract."""


def _committed_source_diagnosis() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND, "diagnosis_status": source.DIAGNOSIS_STATUS,
        "diagnosis_scope": source.DIAGNOSIS_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest": SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "recommended_next_package": RECOMMENDED_PACKAGE,
        "source_reentry_execution_blocked_digest": source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": source.SOURCE_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": source.SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
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
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, "first_result_authoritative": True, "root_full_regression_is_retry_evidence": False},
        "recovered_module_grouping_source_summary": {"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]},
        "top_module_summary": deepcopy(source.TOP_FIVE), "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "available_committed_reentry_detail": list(source.AVAILABLE_COMMITTED_DETAIL),
        "missing_committed_reentry_detail": list(source.MISSING_COMMITTED_DETAIL),
        "actual_live_reentry_source_lacks_complete_29_rows": True,
        "reentry_success_path_tested_with_complete_29_row_snapshot": True,
    }


def _validate_source_diagnosis(diagnosis: Mapping[str, Any]) -> None:
    mismatches = [key for key, expected in _committed_source_diagnosis().items() if diagnosis.get(key) != expected]
    if mismatches:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError(
            f"source diagnosis mismatch: {', '.join(mismatches)}"
        )


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    pairs: dict[str, tuple[Any, Any]] = {
        "source_diagnosis_digest_bound": (SOURCE_DIAGNOSIS_DIGEST, candidate.get("source_reentry_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (PRIMARY_FAILURE_CLASS, candidate.get("primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (source.SOURCE_BLOCKED_EXECUTION_DIGEST, candidate.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (source.SOURCE_BLOCKED_MANIFEST_DIGEST, candidate.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (source.SOURCE_BLOCKED_REASON, candidate.get("source_reentry_execution_blocked_reason")),
        "source_after_v2_planning_reentry_digest_bound": (source.SOURCE_REENTRY_DIGEST, candidate.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (source.SOURCE_RESULTS_REVIEW_DIGEST, candidate.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, candidate.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.SOURCE_RECOVERY_EXECUTION_DIGEST, candidate.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.SOURCE_RECOVERY_DETAIL_DIGEST, candidate.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST, candidate.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_recovery_approval_digest_bound": (source.SOURCE_RECOVERY_APPROVAL_DIGEST, candidate.get("source_module_grouping_source_recovery_approval_digest")),
        "source_recovery_operator_review_digest_bound": (source.SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST, candidate.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_recovery_candidate_digest_bound": (source.SOURCE_RECOVERY_CANDIDATE_DIGEST, candidate.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST, candidate.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST, candidate.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (source.SOURCE_AFTER_V2_APPROVAL_DIGEST, candidate.get("source_after_v2_approval_digest")),
        "source_after_v2_operator_review_digest_bound": (source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST, candidate.get("source_after_v2_operator_review_digest")),
        "source_after_v2_candidate_digest_bound": (source.SOURCE_AFTER_V2_CANDIDATE_DIGEST, candidate.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.SOURCE_RESULTS_REVIEW_V2_DIGEST, candidate.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.SOURCE_EXECUTION_V2_DIGEST, candidate.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.SOURCE_MODULE_GROUPING_DIGEST, candidate.get("source_module_grouping_digest")),
        "source_approval_v2_digest_bound": (source.SOURCE_APPROVAL_V2_DIGEST, candidate.get("source_approval_v2_digest")),
        "source_staged_inventory_digest_bound": (source.SOURCE_STAGED_INVENTORY_DIGEST, candidate.get("source_staged_inventory_digest")),
        "retry_execution_commit_bound": (source.RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": ({"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]}, candidate.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (source.TOP_FIVE, candidate.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, candidate.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, candidate.get("top_10_count_sum")),
        "available_committed_reentry_detail_recorded": (source.AVAILABLE_COMMITTED_DETAIL, candidate.get("available_committed_reentry_detail")),
        "missing_committed_reentry_detail_recorded": (source.MISSING_COMMITTED_DETAIL, candidate.get("missing_committed_reentry_detail")),
        "actual_live_reentry_source_lacks_complete_29_rows_true": (True, candidate.get("actual_live_reentry_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, candidate.get("reentry_success_path_tested_with_complete_29_row_snapshot")),
        "recommended_package_from_diagnosis_bound": (RECOMMENDED_PACKAGE, candidate.get("recommended_next_package_from_diagnosis")),
        "candidate_created_true": (True, candidate.get("reentry_module_grouping_detail_exposure_or_binding_candidate_created")),
        "candidate_ready_true": (True, candidate.get("reentry_module_grouping_detail_exposure_or_binding_candidate_ready_for_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, candidate.get("recommended_detail_exposure_or_binding_package")),
        "packages_present_11": (11, len(candidate.get("proposed_packages", []))),
        "blocked_packages_present_5": (5, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_packages", []) if isinstance(item, Mapping))),
        "recommended_package_not_selected": (False, candidate.get("recommended_package", {}).get("selected")),
        "future_requirements_defined": (FUTURE_REQUIREMENTS, candidate.get("future_detail_exposure_or_binding_requirements")),
        "future_plan_defined": ({"status": PLANNED_NOT_EXECUTED, "steps": FUTURE_PLAN}, candidate.get("future_detail_exposure_or_binding_plan")),
        "planned_outputs_defined": ([{"output_id": output_id, "status": PLANNED_NOT_GENERATED} for output_id in PLANNED_OUTPUT_IDS], candidate.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")), "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (False, candidate.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, candidate.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
    }
    names = {
        "detail_exposure_or_binding_selected": "detail_exposure_or_binding_selected_false",
        "detail_exposure_or_binding_approved": "detail_exposure_or_binding_approved_false",
        "detail_exposure_or_binding_executed": "detail_exposure_or_binding_executed_false",
        "complete_29_row_detail_exposed": "complete_29_row_detail_exposed_false",
        "complete_29_row_detail_bound": "complete_29_row_detail_bound_false",
        "module_grouping_detail_exposed_by_candidate": "module_grouping_detail_exposed_by_candidate_false",
        "module_paths_recovered_by_candidate": "module_paths_recovered_by_candidate_false",
        "per_module_counts_recovered_by_candidate": "per_module_counts_recovered_by_candidate_false",
        "bounded_nodeid_samples_recovered_by_candidate": "bounded_nodeid_samples_recovered_by_candidate_false",
        "after_v2_planning_execution_reentry_created": "after_v2_planning_reentry_created_false",
        "after_v2_planning_execution_reentry_performed": "after_v2_planning_reentry_performed_false",
        "targeted_diagnostic_output_capture_candidate_created": "targeted_diagnostic_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false", "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false", "cache_read_in_candidate": "cache_read_in_candidate_false",
        "module_grouping_recovered_in_candidate": "module_grouping_recovered_in_candidate_false",
        "retry_rerun_performed": "retry_rerun_false", "full_pytest_performed": "full_pytest_false",
        "diagnostic_command_executed": "diagnostic_command_false", "diagnostic_output_captured": "diagnostic_output_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false",
        "marketflow_outputs_committed": "marketflow_outputs_committed_false", "pytest_cache_committed": "pytest_cache_committed_false",
        "evidence_regenerated": "evidence_regenerated_false", "provider_requests_made_in_candidate": "provider_requests_false",
        "market_data_acquisition_performed_in_candidate": "market_data_acquisition_false",
        "dataset_generation_performed_in_candidate": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    pairs.update({check_id: (False, candidate.get(field)) for field, check_id in names.items()})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(candidate: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "reentry_module_grouping_detail_exposure_or_binding_candidate_created": candidate.get("reentry_module_grouping_detail_exposure_or_binding_candidate_created"),
        "reentry_module_grouping_detail_exposure_or_binding_candidate_ready_for_operator_review": candidate.get("reentry_module_grouping_detail_exposure_or_binding_candidate_ready_for_operator_review"),
        "recommended_detail_exposure_or_binding_package": candidate.get("recommended_detail_exposure_or_binding_package"),
        "detail_exposure_or_binding_selected": candidate.get("detail_exposure_or_binding_selected"),
        "detail_exposure_or_binding_approved": candidate.get("detail_exposure_or_binding_approved"),
        "detail_exposure_or_binding_executed": candidate.get("detail_exposure_or_binding_executed"),
        "complete_29_row_detail_exposed": candidate.get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound": candidate.get("complete_29_row_detail_bound"),
        "after_v2_planning_execution_reentry_created": candidate.get("after_v2_planning_execution_reentry_created"),
        "after_v2_planning_execution_reentry_performed": candidate.get("after_v2_planning_execution_reentry_performed"),
        "targeted_diagnostic_output_capture_candidate_created": candidate.get("targeted_diagnostic_output_capture_candidate_created"),
        "new_retry_candidate_created": candidate.get("new_retry_candidate_created"),
        "new_retry_executed": candidate.get("new_retry_executed"),
        "integration_execution_successful": candidate.get("integration_execution_successful"),
        "recommended_next_task": candidate.get("recommended_next_task"),
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(
    *, source_diagnosis: dict | None = None,
) -> dict:
    """Build a candidate from committed diagnosis evidence without exposing detail."""

    diagnosis = deepcopy(source_diagnosis) if source_diagnosis is not None else _committed_source_diagnosis()
    _validate_source_diagnosis(diagnosis)
    recommended = deepcopy(PROPOSED_PACKAGES[0])
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_reentry_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_reentry_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_reentry_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
        "source_reentry_failure_diagnosis_digest": SOURCE_DIAGNOSIS_DIGEST,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "recommended_next_package_from_diagnosis": RECOMMENDED_PACKAGE,
        "source_reentry_execution_blocked_digest": source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "source_reentry_execution_blocked_reason": source.SOURCE_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": source.SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_RECOVERY_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.SOURCE_RECOVERY_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.SOURCE_RECOVERY_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": "MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS",
        "source_after_v2_approval_digest": source.SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": source.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_approval_v2_digest": source.SOURCE_APPROVAL_V2_DIGEST,
        "source_staged_inventory_digest": source.SOURCE_STAGED_INVENTORY_DIGEST,
        "retry_execution_commit": source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": deepcopy(diagnosis["retry_failure_context"]),
        "recovered_module_grouping_source_summary": deepcopy(diagnosis["recovered_module_grouping_source_summary"]),
        "top_module_summary": deepcopy(diagnosis["top_module_summary"]),
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "available_committed_reentry_detail": list(source.AVAILABLE_COMMITTED_DETAIL),
        "missing_committed_reentry_detail": list(source.MISSING_COMMITTED_DETAIL),
        "diagnosis_findings_summary": {"primary_failure_class": PRIMARY_FAILURE_CLASS, "root_cause_summary": "The live committed reentry source did not carry the complete reviewed 29-row detail required for deterministic prioritization.", "actual_live_reentry_source_lacks_complete_29_rows": True, "complete_29_row_detail_available_to_live_reentry_execution": False, "reentry_success_path_tested_with_complete_29_row_snapshot": True, "success_path_generates_tier_sums": {"tier_1": 612, "tier_2": 457, "tier_3": 335}, "not_root_causes": list(source.NOT_ROOT_CAUSES)},
        "actual_live_reentry_source_lacks_complete_29_rows": True,
        "reentry_success_path_tested_with_complete_29_row_snapshot": True,
        "detail_exposure_or_binding_candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        "candidate_philosophy": {"detail_exposure_or_binding_candidate_philosophy": CANDIDATE_PHILOSOPHY, "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL},
        "proposed_packages": deepcopy(PROPOSED_PACKAGES), "recommended_package": recommended,
        "recommended_detail_exposure_or_binding_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommendation_reason": "The diagnosis shows the recovery chain is valid, but complete 29-row detail is not carried forward into the committed reentry interface. A controlled exposure or binding package addresses the actual source-detail gap without inventing data, rereading cache, rerunning pytest, or bypassing planning/review gates.",
        "future_detail_exposure_or_binding_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_detail_exposure_or_binding_plan": {"status": PLANNED_NOT_EXECUTED, "steps": list(FUTURE_PLAN)},
        "plan_status": PLANNED_NOT_EXECUTED,
        "planned_outputs": [{"output_id": output_id, "status": PLANNED_NOT_GENERATED} for output_id in PLANNED_OUTPUT_IDS],
        "non_goals": list(NON_GOALS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "reentry_module_grouping_detail_exposure_or_binding_candidate_created": True,
        "reentry_module_grouping_detail_exposure_or_binding_candidate_ready_for_operator_review": True,
        "ready_for_reentry_module_grouping_detail_exposure_or_binding_operator_review": True,
        "source_recovery_review_facts": {"module_grouping_source_recovery_execution_reviewed": True, "module_grouping_detail_reviewed": True, "module_paths_reviewed": True, "per_module_counts_reviewed": True, "bounded_nodeid_samples_reviewed": True, "top_module_source_detail_reviewed": True, "cache_hash_and_count_verification_reviewed": True, "source_recovery_limitations_reviewed": True, "unsupported_claims_boundary_reviewed": True, "recovered_module_grouping_source_accepted_for_planning_reentry": True, "accepted_source_type": "RECOVERED_REVIEWED_DETACHED_PYTEST_CACHE_MODULE_GROUPING_DETAIL"},
        "source_blocked_reentry_execution_facts": {"after_v2_planning_execution_reentered": True, "after_v2_planning_execution_performed": False, "remediation_or_method_after_v2_reentry_execution_created": True, "remediation_or_method_after_v2_reentry_execution_performed": False, "planning_method_after_v2_reentry_executed": False},
        "source_diagnosis_boundaries": {"reentry_failure_diagnosis_created": True, "reentry_failure_diagnosis_ready": True, "source_detail_availability_diagnosed": True, "committed_reentry_detail_gap_identified": True, "module_grouping_detail_exposed_by_diagnosis": False, "cache_read_in_diagnosis": False, "source_recovery_rerun_performed": False},
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": "C:\\Users\\Aspire5 15 i7 4G2050\\marketflow_worktrees\\integration-terminal-evidence-stack-validation-v1",
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "staged_evidence_manifest_digest": source.SOURCE_STAGED_INVENTORY_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "failure_modules_classified": False, "error_modules_classified": False,
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "direct_code_remediation_recommended": False,
        "retry_success_claimed": False, "main_merge_readiness_claimed": False,
    }
    candidate.update({field: False for field in FALSE_BOUNDARIES})
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate, candidate["checklist"])
    candidate["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest"] = _candidate_digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(candidate: dict) -> dict:
    """Validate source bindings, candidate-only boundaries, checklist, and digest."""

    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError("candidate must be object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "source_reentry_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_reentry_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_reentry_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
    }
    for field, expected in fixed.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError(f"{field} mismatch")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError("checklist invalid")
    summary = _summary(candidate, checklist)
    if candidate.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError("summary invalid")
    digest = candidate.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _candidate_digest(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError("candidate digest invalid")
    return {"artifact_kind": candidate["artifact_kind"], "candidate_status": candidate["candidate_status"], "candidate_scope": candidate["candidate_scope"], "candidate_digest": digest, **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_markdown_v1(candidate: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(candidate)
    sections = [
        ("Source Reentry Failure Diagnosis", [SOURCE_DIAGNOSIS_DIGEST, PRIMARY_FAILURE_CLASS]),
        ("Source Blocked Reentry Execution", [source.SOURCE_BLOCKED_EXECUTION_DIGEST, source.SOURCE_BLOCKED_REASON]),
        ("Source Recovery Results Review", [source.SOURCE_RESULTS_REVIEW_DIGEST, source.SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]),
        ("Recovered Module Grouping Source Summary", [str(candidate["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Committed Detail", [*candidate["available_committed_reentry_detail"], *candidate["missing_committed_reentry_detail"]]),
        ("Candidate Scope", [CANDIDATE_SCOPE]), ("Candidate Philosophy", [CANDIDATE_PHILOSOPHY]),
        ("Proposed Detail Exposure or Binding Packages", [f"{item['package']}: {item['status']}" for item in candidate["proposed_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, candidate["recommendation_reason"]]),
        ("Future Detail Exposure or Binding Requirements", list(candidate["future_detail_exposure_or_binding_requirements"])),
        ("Future Detail Exposure or Binding Plan", candidate["future_detail_exposure_or_binding_plan"]["steps"]),
        ("Planned Outputs", [f"{item['output_id']}: {item['status']}" for item in candidate["planned_outputs"]]),
        ("Non-Goals", candidate["non_goals"]), ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]), ("Risk Controls", candidate["risk_controls"]),
        ("Authority Boundaries", [CANDIDATE_BOUNDARY]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["No option is selected or approved; complete detail remains unexposed and unbound."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Candidate v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(
    output_dir: str | Path, *, source_diagnosis: dict | None = None,
) -> dict:
    candidate = build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(source_diagnosis=source_diagnosis)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1.md"
    json_path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_markdown_v1(candidate), encoding="utf-8")
    return {"artifact": candidate, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = [
    "ARTIFACT_KIND", "CANDIDATE_STATUS", "CANDIDATE_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1",
    "write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_markdown_v1",
]
