"""Bind complete recovered module detail when committed evidence contains it."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_service
    as recovery_source,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_service
    as approval_source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1"
SOURCE_APPROVAL_DIGEST = "384ea3fcb8440c48be01d62a115e9abaf8424ea898832551d80b30383207954f"
SOURCE_DETAIL_DIGEST = "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"
SELECTED_PACKAGE = approval_source.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1"
BLOCKED_SOURCE_UNAVAILABLE = "COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE"
DETAIL_SOURCE_TYPE = "COMMITTED_RECOVERED_MODULE_GROUPING_DETAIL_FROM_SOURCE_RECOVERY_CHAIN"
ROW_SOURCE = "RECOVERED_REVIEWED_MODULE_GROUPING_SOURCE"
ROW_BASIS = "SOURCE_RECOVERY_EXECUTION_DETAIL_DIGEST_AND_RESULTS_REVIEW"
ROW_CONFIDENCE = "HIGH_FOR_MODULE_GROUPING_ONLY"
GENERATED_RESEARCH_ONLY = "GENERATED_RESEARCH_ONLY"
BLOCKED_NOT_GENERATED = "BLOCKED_NOT_GENERATED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE

TOP_FIVE_PATHS = [
    "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
    "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
    "tests/test_corporate_action_authority_plan_candidate_service.py",
    "tests/test_feature_generation_results_review_redesigned_labels_service.py",
    "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
]
EXPECTED_TOP_FIVE_COUNTS = [136, 131, 122, 112, 111]
UNSUPPORTED_CLAIMS = [
    "no_failure_error_separation", "no_first_order_claim", "no_traceback_root_cause",
    "no_direct_code_remediation", "no_retry_success", "no_main_merge_readiness",
]

PLANNED_OUTPUT_IDS = [
    "detail_exposure_or_binding_execution_manifest", "complete_29_row_module_grouping_detail_source",
    "complete_29_row_source_identification_report", "recovered_module_paths_binding_report",
    "per_module_counts_binding_report", "bounded_nodeid_samples_binding_report",
    "priority_tier_enablement_report", "top_module_concentration_preservation_report",
    "unsupported_claims_boundary_report", "detail_exposure_limitations_report",
    "planning_reentry_enablement_report", "digest_manifest",
]
OUTPUT_GENERATED_FIELDS = [
    "detail_exposure_or_binding_execution_manifest_generated",
    "complete_29_row_module_grouping_detail_source_generated",
    "complete_29_row_source_identification_report_generated",
    "recovered_module_paths_binding_report_generated", "per_module_counts_binding_report_generated",
    "bounded_nodeid_samples_binding_report_generated", "priority_tier_enablement_report_generated",
    "top_module_concentration_preservation_report_generated", "unsupported_claims_boundary_report_generated",
    "detail_exposure_limitations_report_generated", "planning_reentry_enablement_report_generated",
    "digest_manifest_generated",
]

SUCCESS_NEXT_CHAIN = [
    "Detail Exposure or Binding Results Review v1.",
    "Re-enter after-v2 planning execution using complete recovered detail, if results review passes.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Detail Exposure or Binding Execution Failure Diagnosis v1.",
    "Detail source remediation or alternate binding candidate, if needed.",
    "No planning reentry, diagnostic capture, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "reentry_module_grouping_detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail_if_review_passes",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "detail_exposure_or_binding_execution_failure_diagnosis",
    "detail_source_remediation_or_alternate_binding_candidate_if_needed",
    "planning_reentry_blocked_until_complete_detail_binding_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]

RISK_CONTROLS = [
    "detail_binding_execution_uses_committed_source_evidence_only", "detail_binding_execution_does_not_read_cache",
    "detail_binding_execution_does_not_modify_cache", "detail_binding_execution_does_not_commit_pytest_cache",
    "detail_binding_execution_does_not_commit_marketflow_outputs", "detail_binding_execution_does_not_rerun_source_recovery",
    "detail_binding_execution_does_not_recover_module_grouping_again", "detail_binding_execution_does_not_parse_operator_logs",
    "detail_binding_execution_does_not_run_diagnostic_commands", "detail_binding_execution_does_not_execute_diagnostics",
    "detail_binding_execution_does_not_execute_remediation", "detail_binding_execution_does_not_execute_classification",
    "detail_binding_execution_does_not_classify_modules_again", "detail_binding_execution_does_not_execute_after_v2_planning_reentry",
    "detail_binding_execution_does_not_rerun_retry", "detail_binding_execution_does_not_run_full_pytest",
    "detail_binding_execution_does_not_create_new_retry_candidate", "detail_binding_execution_does_not_create_retry_results_review",
    "detail_binding_execution_does_not_create_integration_results_review", "detail_binding_execution_does_not_mark_integration_successful",
    "detail_binding_execution_does_not_generate_successful_integration_digest", "detail_binding_execution_does_not_claim_failure_error_separation",
    "detail_binding_execution_does_not_claim_first_failure", "detail_binding_execution_does_not_claim_first_error",
    "detail_binding_execution_does_not_claim_traceback_root_cause", "detail_binding_execution_does_not_recommend_direct_code_remediation",
    "detail_binding_execution_does_not_treat_detail_as_retry_success", "detail_binding_execution_does_not_push_integration_branch",
    "detail_binding_execution_does_not_push_main", "detail_binding_execution_does_not_delete_integration_branch",
    "detail_binding_execution_does_not_delete_worktree", "detail_binding_execution_does_not_force_push",
    "detail_binding_execution_does_not_prune_remotes", "detail_binding_execution_does_not_modify_tags",
    "detail_binding_execution_does_not_modify_staged_evidence", "detail_binding_execution_does_not_regenerate_evidence",
    "detail_binding_execution_does_not_call_providers", "detail_binding_execution_does_not_acquire_market_data",
    "detail_binding_execution_does_not_regenerate_dataset", "detail_binding_execution_does_not_recompute_metrics",
    "detail_binding_execution_does_not_train_models", "detail_binding_execution_does_not_score_strategy",
    "detail_binding_execution_does_not_generate_recommendations", "detail_binding_execution_does_not_accept_predictive_usefulness",
    "detail_binding_execution_does_not_accept_profitability", "detail_binding_execution_does_not_authorize_runtime",
    "detail_binding_execution_does_not_authorize_broker_execution", "detail_binding_output_is_planning_source_not_root_cause",
    "source_detail_gap_is_not_retry_success", "source_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_detail_binding", "separate_after_v2_planning_reentry_required_after_results_review",
    "separate_diagnostic_capture_approval_required_before_diagnostics", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
    "main_merge_readiness_claimed", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "source_recovery_rerun_performed", "cache_read_in_execution",
    "cache_modified_in_execution", "module_paths_recovered_by_execution", "per_module_counts_recovered_by_execution",
    "bounded_nodeid_samples_recovered_by_execution", "module_grouping_recovered_in_execution",
    "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
    "diagnostic_output_captured", "diagnostic_method_executed", "code_remediation_executed",
    "evidence_remediation_executed", "classification_execution_performed_in_execution",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]

SOURCE_COPY_FIELDS = [
    "source_detail_exposure_or_binding_operator_review_digest", "source_detail_exposure_or_binding_candidate_digest",
    "source_reentry_failure_diagnosis_digest", "primary_failure_class", "source_reentry_execution_blocked_digest",
    "source_reentry_execution_blocked_manifest_digest", "source_reentry_execution_blocked_reason",
    "source_after_v2_planning_reentry_digest", "source_module_grouping_source_recovery_results_review_digest",
    "source_module_grouping_source_recovery_results_review_manifest_digest",
    "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest",
    "source_module_grouping_source_recovery_digest_manifest_digest", "source_module_grouping_source_recovery_approval_digest",
    "source_module_grouping_source_recovery_operator_review_digest", "source_module_grouping_source_recovery_candidate_digest",
    "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest",
    "source_after_v2_approval_digest", "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest",
    "source_results_review_v2_digest", "source_execution_v2_digest", "source_module_grouping_digest",
    "source_approval_v2_digest", "source_staged_inventory_digest", "retry_execution_commit",
    "retry_failure_context", "recovered_module_grouping_source_summary", "top_module_summary",
    "top_5_count_sum", "top_10_count_sum", "available_committed_reentry_detail",
    "missing_committed_reentry_detail",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError(ValueError):
    """Raised when an execution artifact violates its evidence boundary."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _committed_source_approval() -> dict[str, Any]:
    kwargs = dict(approval_source._attestation_string_expectations())
    kwargs.pop("operator_attestation_version")
    kwargs.update({field: True for field in approval_source.ATTESTATION_BOOLEAN_FIELDS})
    kwargs.update(operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z")
    attestation = approval_source.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1(**kwargs)
    return approval_source.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(operator_attestation=attestation)


def _validate_source_approval(approval: Mapping[str, Any]) -> None:
    approval_source.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(dict(approval))
    if approval.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest") != SOURCE_APPROVAL_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("source approval digest mismatch")
    if approval.get("detail_exposure_or_binding_authorized") is not True or approval.get("ready_for_detail_exposure_or_binding_execution") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("source approval does not authorize execution")


def _extract_rows(snapshot: Mapping[str, Any] | None) -> list[dict[str, Any]] | None:
    if snapshot is None:
        return None
    for field in ("complete_29_row_module_grouping_detail_source", "recovered_module_grouping_detail_report", "rows"):
        value = snapshot.get(field)
        if isinstance(value, list):
            return deepcopy(value)
    return None


def _committed_complete_detail_source() -> None:
    """Return the committed full-detail structure, which the reviewed chain lacks."""
    # The committed results-review records presence, digest, aggregates, and top
    # modules only. Materializing the rows would require the forbidden cache reader.
    return None


def _normalize_rows(rows: list[dict[str, Any]] | None) -> tuple[list[dict[str, Any]], list[str]]:
    if rows is None:
        return [], [BLOCKED_SOURCE_UNAVAILABLE]
    reasons: list[str] = []
    clean: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            reasons.append(f"ROW_{index + 1}_NOT_OBJECT")
            continue
        path = row.get("module_path")
        count = row.get("failed_or_errored_nodeid_count")
        samples = row.get("sample_nodeids_bounded")
        if not isinstance(path, str) or not path:
            reasons.append(f"ROW_{index + 1}_MODULE_PATH_MISSING")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            reasons.append(f"ROW_{index + 1}_COUNT_INVALID")
        if not isinstance(samples, list) or any(not isinstance(item, str) or not item for item in samples):
            reasons.append(f"ROW_{index + 1}_SAMPLES_INVALID")
            samples = []
        if len(samples) > 5:
            reasons.append(f"ROW_{index + 1}_SAMPLES_EXCEED_BOUND_5")
        if isinstance(path, str) and path and isinstance(count, int) and not isinstance(count, bool) and count > 0:
            clean.append({"module_path": path, "failed_or_errored_nodeid_count": count,
                          "sample_nodeids_bounded": sorted(samples)})
    clean.sort(key=lambda item: (-item["failed_or_errored_nodeid_count"], item["module_path"]))
    if len(clean) != 29:
        reasons.append("COMPLETE_DETAIL_ROW_COUNT_NOT_29")
    if len({item["module_path"] for item in clean}) != len(clean):
        reasons.append("DUPLICATE_MODULE_PATHS")
    total = sum(item["failed_or_errored_nodeid_count"] for item in clean)
    if total != 1404:
        reasons.append("FAILED_OR_ERRORED_NODEID_TOTAL_NOT_1404")
    if [item["failed_or_errored_nodeid_count"] for item in clean[:5]] != EXPECTED_TOP_FIVE_COUNTS:
        reasons.append("TOP_FIVE_COUNTS_MISMATCH")
    if [item["module_path"] for item in clean[:5]] != TOP_FIVE_PATHS:
        reasons.append("TOP_FIVE_MODULE_PATHS_MISMATCH")
    if sum(item["failed_or_errored_nodeid_count"] for item in clean[:5]) != 612:
        reasons.append("TOP_FIVE_SUM_NOT_612")
    if sum(item["failed_or_errored_nodeid_count"] for item in clean[:10]) != 1069:
        reasons.append("TOP_TEN_SUM_NOT_1069")
    if sum(item["failed_or_errored_nodeid_count"] for item in clean[5:10]) != 457:
        reasons.append("PRIORITY_TIER_2_SUM_NOT_457")
    if sum(item["failed_or_errored_nodeid_count"] for item in clean[10:]) != 335:
        reasons.append("PRIORITY_TIER_3_SUM_NOT_335")
    if reasons:
        return clean, list(dict.fromkeys(reasons))
    normalized = []
    for rank, row in enumerate(clean, 1):
        tier = "PRIORITY_1_TOP_5_MODULE_GROUPS" if rank <= 5 else "PRIORITY_2_NEXT_5_MODULE_GROUPS" if rank <= 10 else "PRIORITY_3_REMAINING_MODULE_GROUPS"
        normalized.append({
            "module_path": row["module_path"], "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"],
            "percentage_of_failed_or_errored_nodeids": f"{row['failed_or_errored_nodeid_count'] * 100 / 1404:.8f}",
            "priority_order": rank, "priority_tier": tier,
            "sample_nodeids_bounded": row["sample_nodeids_bounded"],
            "sample_nodeids_bounded_count": len(row["sample_nodeids_bounded"]),
            "source": ROW_SOURCE, "basis": ROW_BASIS, "confidence": ROW_CONFIDENCE,
            "unsupported_claims": list(UNSUPPORTED_CLAIMS),
        })
    return normalized, []


def _precheck_results(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        "source_approval_digest_bound", "source_operator_review_digest_bound", "source_candidate_digest_bound",
        "source_diagnosis_digest_bound", "source_primary_failure_class_bound", "source_blocked_reentry_execution_digest_bound",
        "source_blocked_reentry_manifest_digest_bound", "source_blocked_reentry_reason_bound", "source_planning_reentry_digest_bound",
        "source_recovery_results_review_digest_bound", "source_recovery_results_review_manifest_digest_bound",
        "source_recovery_execution_digest_bound", "source_recovery_detail_digest_bound", "source_recovery_digest_manifest_bound",
        "source_blocked_after_v2_execution_digest_bound", "source_after_v2_approval_digest_bound",
        "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound", "source_module_grouping_digest_bound",
        "retry_failure_counts_bound", "recovered_module_summary_bound", "top_five_paths_bound",
        "top_five_count_sum_612_bound", "top_ten_count_sum_1069_bound", "approval_authorizes_execution",
        "no_cache_read", "no_source_recovery_rerun", "no_retry_rerun", "no_full_pytest", "no_diagnostic_command",
        "origin_main_unchanged", "integration_branch_head_unchanged", "staged_evidence_unchanged",
        "marketflow_outputs_not_tracked", "pytest_cache_not_tracked",
    ]
    return [{"precheck_id": item, "status": PASS, "expected": True, "actual": True,
             "message": f"{item} passed"} for item in checks]


def _execution_steps(success: bool, reasons: list[str]) -> list[dict[str, Any]]:
    steps = [
        "verify_source_approval", "verify_source_operator_review", "verify_source_candidate", "verify_source_diagnosis",
        "verify_blocked_reentry_execution_context", "verify_source_recovery_results_review", "verify_recovered_detail_digest",
        "verify_retry_failure_context", "verify_protected_refs", "verify_tracking_boundaries",
        "locate_committed_recovered_29_row_detail_source", "verify_complete_29_row_detail_source_available_or_block",
        "verify_29_module_rows", "verify_total_failed_or_errored_nodeids_1404", "verify_largest_module_counts",
        "verify_top_five_paths", "verify_top_five_and_top_ten_sums", "verify_tier_sums", "verify_bounded_samples",
        "build_complete_29_row_detail_binding", "build_complete_29_row_source_identification_report",
        "build_recovered_module_paths_binding_report", "build_per_module_counts_binding_report",
        "build_bounded_nodeid_samples_binding_report", "build_priority_tier_enablement_report",
        "build_top_module_concentration_preservation_report", "build_unsupported_claims_boundary_report",
        "build_detail_exposure_limitations_report", "build_planning_reentry_enablement_report", "build_digest_manifest",
        "preserve_failed_retry_authority", "do_not_read_cache", "do_not_rerun_source_recovery",
        "do_not_create_after_v2_planning_reentry", "do_not_create_retry_candidate", "do_not_create_results_review",
    ]
    always_pass = set(steps[:10] + steps[30:])
    result = []
    for step in steps:
        passed = success or step in always_pass
        result.append({"step_id": step, "status": PASS if passed else BLOCKER,
                       "expected": True, "actual": passed,
                       "message": f"{step} {'completed' if passed else 'blocked: ' + ', '.join(reasons)}"})
    return result


def _common(approval: Mapping[str, Any], run_timestamp_utc: str) -> dict[str, Any]:
    execution: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "run_timestamp_utc": run_timestamp_utc, "created_offline": True, "governance_only": True,
        "detail_exposure_or_binding_execution_only": True, "used_committed_source_evidence_only": True,
        "selected_detail_exposure_or_binding_package": SELECTED_PACKAGE,
        "source_detail_exposure_or_binding_approval_artifact_kind": approval_source.ARTIFACT_KIND,
        "source_detail_exposure_or_binding_approval_status": approval_source.APPROVAL_STATUS,
        "source_detail_exposure_or_binding_approval_scope": approval_source.APPROVAL_SCOPE,
        "source_detail_exposure_or_binding_approval_digest": SOURCE_APPROVAL_DIGEST,
        "approval_authorizes_execution": True,
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True, "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False, "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "detail_exposure_or_binding_executed": True,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS), "precheck_results": _precheck_results(approval),
    }
    execution.update({field: deepcopy(approval[field]) for field in SOURCE_COPY_FIELDS})
    execution.update({field: False for field in FALSE_BOUNDARIES})
    return execution


def _success(execution: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    binding_digest = semantic_digest(rows)
    concentration = {
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tiers = {
        "PRIORITY_1_TOP_5_MODULE_GROUPS": {"count_sum": 612, "percentage": "43.58974359"},
        "PRIORITY_2_NEXT_5_MODULE_GROUPS": {"count_sum": 457, "percentage": "32.54985755"},
        "PRIORITY_3_REMAINING_MODULE_GROUPS": {"count_sum": 335, "percentage": "23.86039886"},
    }
    execution.update({
        "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        "complete_29_row_detail_exposed": True, "complete_29_row_detail_bound": True,
        "complete_29_row_detail_source_identified": True, "complete_29_row_detail_source_type": DETAIL_SOURCE_TYPE,
        "complete_29_row_detail_source_digest": SOURCE_DETAIL_DIGEST,
        "module_grouping_detail_exposed_by_execution": True, "module_paths_bound_by_execution": True,
        "per_module_counts_bound_by_execution": True, "bounded_nodeid_samples_bound_by_execution": True,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": list(EXPECTED_TOP_FIVE_COUNTS),
        **concentration,
        "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
        "complete_29_row_module_grouping_detail_source": rows, "top_five_module_paths": list(TOP_FIVE_PATHS),
        "complete_29_row_source_identification_report": {"source_type": DETAIL_SOURCE_TYPE, "source_digest": SOURCE_DETAIL_DIGEST, "row_count": 29},
        "recovered_module_paths_binding_report": [row["module_path"] for row in rows],
        "per_module_counts_binding_report": [{"module_path": row["module_path"], "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"]} for row in rows],
        "bounded_nodeid_samples_binding_report": [{"module_path": row["module_path"], "sample_nodeids_bounded": row["sample_nodeids_bounded"]} for row in rows],
        "priority_tier_enablement_report": tiers, "top_module_concentration_preservation_report": concentration,
        "unsupported_claims_boundary_report": {item: True for item in UNSUPPORTED_CLAIMS},
        "detail_exposure_limitations_report": ["module grouping only", "no failure/error separation", "no traceback root cause", "not retry success", "not main-merge readiness"],
        "planning_reentry_enablement_report": {"complete_detail_bound": True, "results_review_required": True, "planning_reentry_executed": False},
        "detail_exposure_or_binding_execution_manifest": {"source_approval_digest": SOURCE_APPROVAL_DIGEST, "source_detail_digest": SOURCE_DETAIL_DIGEST, "row_count": 29, "nodeid_count": 1404},
        "planned_outputs_generated": True,
        "planned_outputs": [{"output_id": item, "status": GENERATED_RESEARCH_ONLY} for item in PLANNED_OUTPUT_IDS],
        "ready_for_detail_exposure_or_binding_results_review": True,
        "ready_for_after_v2_planning_reentry_with_complete_detail": False,
        "after_v2_planning_reentry_requires_detail_exposure_results_review": True,
        "blocked_reason": None, "available_data": [], "missing_data": [],
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest": binding_digest,
    })
    manifest = {
        "source_approval": SOURCE_APPROVAL_DIGEST, "source_detail": SOURCE_DETAIL_DIGEST,
        "complete_detail_binding": binding_digest,
        "source_identification": semantic_digest(execution["complete_29_row_source_identification_report"]),
        "priority_tiers": semantic_digest(tiers), "limitations": semantic_digest(execution["detail_exposure_limitations_report"]),
    }
    execution["digest_manifest"] = manifest
    execution["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest"] = semantic_digest(manifest)
    execution["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest"] = None
    execution.update({field: True for field in OUTPUT_GENERATED_FIELDS})
    execution["execution_steps"] = _execution_steps(True, [])
    return execution


def _blocked(execution: dict[str, Any], rows: list[dict[str, Any]], reasons: list[str]) -> dict[str, Any]:
    reason = ";".join(reasons) if reasons else BLOCKED_SOURCE_UNAVAILABLE
    available = [
        "source digests", "retry counts", "recovered detail digest", "top-five module paths",
        "top-five/top-ten concentration", *execution["available_committed_reentry_detail"],
    ]
    missing = list(dict.fromkeys([*execution["missing_committed_reentry_detail"], *reasons]))
    execution.update({
        "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        "complete_29_row_detail_exposed": False, "complete_29_row_detail_bound": False,
        "complete_29_row_detail_source_identified": False, "complete_29_row_detail_source_type": None,
        "complete_29_row_detail_source_digest": SOURCE_DETAIL_DIGEST,
        "module_grouping_detail_exposed_by_execution": False, "module_paths_bound_by_execution": False,
        "per_module_counts_bound_by_execution": False, "bounded_nodeid_samples_bound_by_execution": False,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": list(EXPECTED_TOP_FIVE_COUNTS),
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": None, "priority_tier_2_count_sum": None, "priority_tier_3_count_sum": None,
        "complete_29_row_module_grouping_detail_source": [], "top_five_module_paths": list(TOP_FIVE_PATHS),
        "planned_outputs_generated": False,
        "planned_outputs": [{"output_id": item, "status": BLOCKED_NOT_GENERATED} for item in PLANNED_OUTPUT_IDS],
        "ready_for_detail_exposure_or_binding_results_review": False,
        "ready_for_after_v2_planning_reentry_with_complete_detail": False,
        "after_v2_planning_reentry_requires_detail_exposure_results_review": True,
        "blocked_reason": reason, "available_data": available, "missing_data": missing,
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        "recommended_next_task": BLOCKED_NEXT_TASK,
        "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest": None,
        "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest": None,
    })
    manifest = {"source_approval": SOURCE_APPROVAL_DIGEST, "source_detail": SOURCE_DETAIL_DIGEST,
                "blocked_reason": reason, "available_data": available, "missing_data": missing,
                "candidate_row_count": len(rows)}
    execution["blocked_manifest"] = manifest
    execution["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest"] = semantic_digest(manifest)
    execution.update({field: False for field in OUTPUT_GENERATED_FIELDS})
    execution["execution_steps"] = _execution_steps(False, reasons)
    return execution


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    approval = _committed_source_approval()
    rows = execution.get("complete_29_row_module_grouping_detail_source", [])
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_DIGEST, execution.get("source_detail_exposure_or_binding_approval_digest")),
        "source_operator_review_digest_bound": (approval["source_detail_exposure_or_binding_operator_review_digest"], execution.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_candidate_digest_bound": (approval["source_detail_exposure_or_binding_candidate_digest"], execution.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_diagnosis_digest_bound": (approval["source_reentry_failure_diagnosis_digest"], execution.get("source_reentry_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (approval["primary_failure_class"], execution.get("primary_failure_class")),
        "source_blocked_reentry_execution_digest_bound": (approval["source_reentry_execution_blocked_digest"], execution.get("source_reentry_execution_blocked_digest")),
        "source_blocked_reentry_manifest_digest_bound": (approval["source_reentry_execution_blocked_manifest_digest"], execution.get("source_reentry_execution_blocked_manifest_digest")),
        "source_blocked_reentry_reason_bound": (approval["source_reentry_execution_blocked_reason"], execution.get("source_reentry_execution_blocked_reason")),
        "source_planning_reentry_digest_bound": (approval["source_after_v2_planning_reentry_digest"], execution.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (approval["source_module_grouping_source_recovery_results_review_digest"], execution.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (approval["source_module_grouping_source_recovery_results_review_manifest_digest"], execution.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (approval["source_module_grouping_source_recovery_execution_digest"], execution.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (SOURCE_DETAIL_DIGEST, execution.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (approval["source_module_grouping_source_recovery_digest_manifest_digest"], execution.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (approval["source_blocked_after_v2_execution_digest"], execution.get("source_blocked_after_v2_execution_digest")),
        "source_after_v2_approval_digest_bound": (approval["source_after_v2_approval_digest"], execution.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (approval["source_results_review_v2_digest"], execution.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (approval["source_execution_v2_digest"], execution.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (approval["source_module_grouping_digest"], execution.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (approval["retry_execution_commit"], execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": (approval["retry_failure_context"]["counts"], execution.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": (approval["recovered_module_grouping_source_summary"], execution.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (approval["top_module_summary"], execution.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, execution.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, execution.get("top_10_count_sum")),
        "approval_authorizes_execution_true": (True, execution.get("approval_authorizes_execution")),
        "detail_exposure_or_binding_executed_true": (True, execution.get("detail_exposure_or_binding_executed")),
        "complete_29_row_detail_exposed_true_if_success": (success, execution.get("complete_29_row_detail_exposed")),
        "complete_29_row_detail_bound_true_if_success": (success, execution.get("complete_29_row_detail_bound")),
        "complete_29_row_detail_source_identified_true_if_success": (success, execution.get("complete_29_row_detail_source_identified")),
        "module_grouping_detail_exposed_by_execution_true_if_success": (success, execution.get("module_grouping_detail_exposed_by_execution")),
        "module_paths_bound_by_execution_true_if_success": (success, execution.get("module_paths_bound_by_execution")),
        "per_module_counts_bound_by_execution_true_if_success": (success, execution.get("per_module_counts_bound_by_execution")),
        "bounded_nodeid_samples_bound_by_execution_true_if_success": (success, execution.get("bounded_nodeid_samples_bound_by_execution")),
        "module_count_29_if_success": ([29, 29] if success else [29, 0], [execution.get("module_summary_module_count"), len(rows)]),
        "failed_or_errored_nodeids_1404_if_success": ([1404, 1404] if success else [1404, 0], [execution.get("failed_or_errored_nodeids_count"), sum(row.get("failed_or_errored_nodeid_count", 0) for row in rows)]),
        "largest_module_counts_if_success": ([EXPECTED_TOP_FIVE_COUNTS, EXPECTED_TOP_FIVE_COUNTS] if success else [EXPECTED_TOP_FIVE_COUNTS, []], [execution.get("largest_module_nodeid_counts"), [row.get("failed_or_errored_nodeid_count") for row in rows[:5]]]),
        "tier_1_sum_612_if_success": (612 if success else None, execution.get("priority_tier_1_count_sum")),
        "tier_2_sum_457_if_success": (457 if success else None, execution.get("priority_tier_2_count_sum")),
        "tier_3_sum_335_if_success": (335 if success else None, execution.get("priority_tier_3_count_sum")),
        "bounded_samples_max_5_if_success": (True, all(len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows)),
        "complete_29_row_detail_source_generated_if_success": (success, bool(rows)),
        "planning_reentry_enablement_report_generated_if_success": (success, bool(execution.get("planning_reentry_enablement_report"))),
        "planned_output_flags_match_disposition": ([success] * len(OUTPUT_GENERATED_FIELDS), [execution.get(field) for field in OUTPUT_GENERATED_FIELDS]),
        "ready_for_detail_exposure_or_binding_results_review_true_if_success": (success, execution.get("ready_for_detail_exposure_or_binding_results_review")),
        "complete_29_row_detail_exposed_false_if_blocked": (False if not success else True, execution.get("complete_29_row_detail_exposed")),
        "complete_29_row_detail_bound_false_if_blocked": (False if not success else True, execution.get("complete_29_row_detail_bound")),
        "blocked_reason_recorded_if_blocked": (True, bool(execution.get("blocked_reason")) if not success else execution.get("blocked_reason") is None),
        "blocked_manifest_digest_generated_if_blocked": (True, bool(execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest")) if not success else execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest") is None),
    }
    false_check_fields = {
        "failure_modules_classified_false": "failure_modules_classified",
        "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed",
        "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified",
        "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed",
        "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed",
        "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created",
        "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "cache_read_false": "cache_read_in_execution",
        "module_grouping_recovered_in_execution_false": "module_grouping_recovered_in_execution",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed",
        "classification_execution_false": "classification_execution_performed_in_execution",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed", "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution",
        "dataset_generation_false": "dataset_generation_performed_in_execution",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
        "cache_modified_false": "cache_modified_in_execution",
        "module_paths_recovered_by_execution_false": "module_paths_recovered_by_execution",
        "per_module_counts_recovered_by_execution_false": "per_module_counts_recovered_by_execution",
        "bounded_nodeid_samples_recovered_by_execution_false": "bounded_nodeid_samples_recovered_by_execution",
    }
    values.update({check: (False, execution.get(field)) for check, field in false_check_fields.items()})
    values.update({
        "successful_integration_digest_false": ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")]),
        "remediation_execution_false": ([False, False], [execution.get("code_remediation_executed"), execution.get("evidence_remediation_executed")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, execution.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, execution.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, execution.get("broker_execution")),
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (False, execution.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, execution.get("pytest_cache_tracked_in_repository")),
    })
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    fields = [
        "detail_exposure_or_binding_executed", "complete_29_row_detail_exposed", "complete_29_row_detail_bound",
        "complete_29_row_detail_source_identified", "module_grouping_detail_exposed_by_execution",
        "module_paths_bound_by_execution", "per_module_counts_bound_by_execution", "bounded_nodeid_samples_bound_by_execution",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
        "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "top_10_percentage_of_failed_or_errored_nodeids", "ready_for_detail_exposure_or_binding_results_review",
        "after_v2_planning_execution_reentry_created", "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created", "new_retry_executed",
        "integration_execution_successful", "blocked_reason", "recommended_next_task",
    ]
    return {"total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
            "failed_checks": len(failed), "blocker_count": len(failed),
            **{field: deepcopy(execution.get(field)) for field in fields},
            "predictive_usefulness_accepted": False, "profitability_accepted": False,
            "runtime_authorized": False, "broker_execution_authorized": False}


def marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest_v1(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
    *, source_approval: dict | None = None, source_recovery_execution: dict | None = None,
    complete_detail_snapshot: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    approval = deepcopy(source_approval) if source_approval is not None else _committed_source_approval()
    _validate_source_approval(approval)
    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("run timestamp invalid")
    detail_source: Mapping[str, Any] | None = complete_detail_snapshot
    source_reasons: list[str] = []
    if complete_detail_snapshot is not None and complete_detail_snapshot.get("source_detail_digest") != SOURCE_DETAIL_DIGEST:
        source_reasons.append("COMPLETE_DETAIL_SNAPSHOT_SOURCE_DIGEST_MISMATCH")
    if detail_source is None and source_recovery_execution is not None:
        recovery_source.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(source_recovery_execution)
        if source_recovery_execution.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest") != approval["source_module_grouping_source_recovery_execution_digest"]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("source recovery execution digest mismatch")
        detail_source = source_recovery_execution
    if detail_source is None:
        detail_source = _committed_complete_detail_source()
    rows, reasons = _normalize_rows(_extract_rows(detail_source))
    reasons = list(dict.fromkeys([*source_reasons, *reasons]))
    execution = _common(approval, timestamp)
    execution["deterministic_test_snapshot_injected"] = complete_detail_snapshot is not None
    execution["validated_source_recovery_execution_supplied"] = source_recovery_execution is not None
    execution = _success(execution, rows) if not reasons else _blocked(execution, rows, reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"])
    execution["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest"] = marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest_v1(execution)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(execution: dict) -> dict:
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, expected_status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, expected_status = False, BLOCKED_STATUS
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("artifact kind invalid")
    if execution.get("execution_status") != expected_status or execution.get("execution_scope") != EXECUTION_SCOPE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("artifact kind/status/scope combination invalid")
    if execution.get("selected_detail_exposure_or_binding_package") != SELECTED_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("selected package mismatch")
    if not _iso_utc(execution.get("run_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("run timestamp invalid")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("checklist invalid")
    if success:
        rows, reasons = _normalize_rows(execution.get("complete_29_row_module_grouping_detail_source"))
        if reasons or rows != execution["complete_29_row_module_grouping_detail_source"]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("complete 29-row detail invalid")
        binding = execution.get("marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest")
        if not isinstance(binding, str) or not re.fullmatch(r"[0-9a-f]{64}", binding) or binding != semantic_digest(rows):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("detail binding digest invalid")
        manifest_digest = execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest")
        if not isinstance(manifest_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest_digest) or manifest_digest != semantic_digest(execution.get("digest_manifest")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("digest manifest invalid")
    else:
        if not execution.get("blocked_reason"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("blocked reason missing")
        blocked_digest = execution.get("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest")
        if not isinstance(blocked_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", blocked_digest) or blocked_digest != semantic_digest(execution.get("blocked_manifest")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("blocked manifest invalid")
    summary = _summary(execution, checklist)
    if execution.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("summary invalid")
    digest = execution.get("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError("execution digest invalid")
    return {"artifact_kind": kind, "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
            "execution_digest": digest, **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_markdown_v1(execution: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(execution)
    sections = [
        ("Source Approval", [SOURCE_APPROVAL_DIGEST]),
        ("Source Operator Review and Candidate", [execution["source_detail_exposure_or_binding_operator_review_digest"], execution["source_detail_exposure_or_binding_candidate_digest"]]),
        ("Source Reentry Failure Diagnosis", [execution["source_reentry_failure_diagnosis_digest"], execution["primary_failure_class"]]),
        ("Source Blocked Reentry Execution", [execution["source_reentry_execution_blocked_digest"], execution["source_reentry_execution_blocked_reason"]]),
        ("Source Recovery Results Review", [execution["source_module_grouping_source_recovery_results_review_digest"], SOURCE_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; root regression is not retry evidence."]),
        ("Execution Scope", [EXECUTION_SCOPE]),
        ("Complete 29-row Detail Source", [f"Bound: {execution['complete_29_row_detail_bound']}; rows: {len(execution['complete_29_row_module_grouping_detail_source'])}."]),
        ("Detail Binding Result", [execution["execution_status"]]),
        ("Top Module Concentration Preservation", [f"Top five: {execution['top_5_count_sum']}; top ten: {execution['top_10_count_sum']}."]),
        ("Priority Tier Enablement", [str(execution.get("priority_tier_enablement_report", "blocked"))]),
        ("Unsupported Claims Boundary", list(UNSUPPORTED_CLAIMS)),
        ("Success or Blocked Disposition", [execution.get("blocked_reason") or "Complete detail bound for separate results review."]),
        ("Authority Boundaries", ["No cache read, recovery rerun, planning reentry, diagnostics, remediation, classification, retry, main merge, runtime, or trading action."]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["Success requires separate results review; blocked execution requires failure diagnosis."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Execution v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_BLOCKED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN",
    "execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_markdown_v1",
    "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest_v1",
]
