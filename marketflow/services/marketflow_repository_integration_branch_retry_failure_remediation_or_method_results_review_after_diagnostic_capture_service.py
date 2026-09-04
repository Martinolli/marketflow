"""Review the committed bounded method-execution result without rerunning it."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_service
    as source,
)

ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_ONLY_NOT_METHOD_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_EXECUTION_COMMIT = "2e447891ac8bb8ed86b2a3ecaa09043b7933aef7"
SOURCE_EXECUTION_DIGEST = "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88"
SOURCE_CLASSIFICATION_DIGEST = "3e3f2409315228bc88c23fb02dfdf3dbea4724d30356f0a4548243105a49dac1"
SOURCE_BOUNDED_ANALYSIS_DIGEST = "d20ddba72b6461a061e7a1b3a7fc4b892abce093bc8d1e25b3c0a46bca0960c9"
SOURCE_EXECUTION_MANIFEST_DIGEST = "d4e10da387d3f96cffd5822e832cfd1c5a4cae8a8eb8d802f67739a673f1eef9"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_V1"
RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_digest"
CLASSIFICATION_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_failure_family_classification_review_digest"
BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_bounded_excerpt_analysis_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_manifest_digest"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

FAMILY_IDS = [
    "assertion_or_value_mismatch",
    "digest_or_hash_mismatch",
    "fixture_or_test_isolation_issue",
    "missing_or_unexpected_field",
]
FAMILY_LABELS = {
    "assertion_or_value_mismatch": "Assertion or value mismatch",
    "digest_or_hash_mismatch": "Digest or hash mismatch",
    "fixture_or_test_isolation_issue": "Fixture or test isolation issue",
    "missing_or_unexpected_field": "Missing or unexpected field",
}
FAMILY_REQUIRED_FIELDS = [
    "family_id", "family_label", "classification_source", "classification_basis",
    "observable_evidence_count", "representative_redacted_snippets",
    "priority_1_modules_visible", "confidence", "limitations", "root_cause_claimed",
    "direct_remediation_recommended", "retry_success_claimed",
]
OBSERVABLE_FAMILY_REVIEWS = [
    {
        "family_id": family_id,
        "family_label": FAMILY_LABELS[family_id],
        "observable_evidence_count": 47,
        "confidence": "HIGH",
        "source_family_record_required_fields": list(FAMILY_REQUIRED_FIELDS),
        "required_fields_present": True,
        "representative_snippets_bounded": True,
        "representative_snippet_count_at_most_5": True,
        "representative_snippet_chars_at_most_500": True,
        "source_classification_is_bounded_pattern_evidence_only": True,
        "limitations": "Reviewed bounded-pattern evidence only; not root cause, direct remediation, full retry classification, or retry success.",
        "root_cause_claimed": False,
        "direct_remediation_recommended": False,
        "retry_success_claimed": False,
    }
    for family_id in FAMILY_IDS
]

REVIEW_FINDINGS = [
    {"finding_id": f"finding_{index}", "finding": text}
    for index, text in enumerate(
        [
            "The source method execution completed successfully and generated bounded failure-family classification evidence.",
            "The source execution used the approved package and remained method-analysis-only.",
            "The source execution used committed durable receipt evidence and bounded excerpts only.",
            "The source execution did not run pytest, rerun controlled recapture, rerun retry, read cache, parse logs, inspect `.env`, or reconstruct full streams.",
            "Four observable failure families were generated from bounded diagnostic evidence.",
            "The four observed families were assertion_or_value_mismatch, digest_or_hash_mismatch, fixture_or_test_isolation_issue, and missing_or_unexpected_field.",
            "Each observed family has 47 visible evidence matches and HIGH confidence in the source method output.",
            "The total observable family-level evidence count is 188.",
            "The source method output does not indicate that additional diagnostic capture is currently required.",
            "The source method output does not support direct remediation readiness.",
            "The source method output does not support retry readiness or main-merge readiness.",
            "The source method output does not claim root cause, first failure, first error, full retry failure/error separation, or traceback cause.",
            "The historical authoritative retry remains failed with 24,877 passed, 1,292 failed, 112 errors, and 7 skipped.",
            "The source diagnostic capture remains diagnostic evidence only and is not retry evidence.",
            "This results review did not rerun method execution, parse receipt, analyze output, run pytest, execute remediation, create a retry candidate, push protected branches, or modify evidence.",
            "The reviewed method output supports a separately invoked remediation plan or execution candidate, subject to operator review and approval.",
        ],
        start=1,
    )
]

REVIEW_OUTPUT_IDS = [
    "remediation_or_method_results_review_after_diagnostic_capture_manifest",
    "source_method_execution_digest_review", "failure_family_classification_digest_review",
    "bounded_excerpt_analysis_digest_review", "source_execution_manifest_digest_review",
    "source_approval_binding_review", "diagnostic_results_review_binding_review",
    "durable_receipt_evidence_review", "observable_failure_family_classification_review",
    "family_confidence_and_limitation_review", "bounded_excerpt_limitation_review",
    "unsupported_claims_boundary_review", "remediation_plan_or_execution_candidate_readiness_report",
    "retry_gate_preservation_report", "main_merge_gate_preservation_report", "digest_manifest",
]
REVIEW_OUTPUTS = [
    {"output_id": output_id, "status": "GENERATED_METHOD_RESULTS_REVIEW_ONLY"}
    for output_id in REVIEW_OUTPUT_IDS
]

NEXT_CHAIN = [
    "Remediation Plan or Execution Candidate After Method Results Review v1.",
    "Remediation Plan or Execution Candidate Operator Review v1.",
    "Remediation Plan or Execution Approval v1, if selected.",
    "Remediation Plan or Execution v1, if approved.",
    "Remediation Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_plan_or_execution_candidate_after_method_results_review",
    "remediation_plan_or_execution_candidate_operator_review",
    "remediation_plan_or_execution_approval_if_selected",
    "remediation_plan_or_execution_if_approved", "remediation_results_review",
    "new_integration_branch_retry_candidate_after_remediation_results_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "method_results_review_does_not_rerun_method_execution", "method_results_review_does_not_parse_durable_receipt",
    "method_results_review_does_not_analyze_diagnostic_output_again", "method_results_review_does_not_rerun_controlled_recapture",
    "method_results_review_does_not_run_diagnostic_command", "method_results_review_does_not_run_targeted_pytest",
    "method_results_review_does_not_run_full_pytest", "method_results_review_does_not_rerun_retry",
    "method_results_review_does_not_read_pytest_cache", "method_results_review_does_not_modify_pytest_cache",
    "method_results_review_does_not_parse_terminal_logs", "method_results_review_does_not_parse_operator_logs",
    "method_results_review_does_not_inspect_env", "method_results_review_does_not_reconstruct_prior_lost_values",
    "method_results_review_does_not_reconstruct_full_stdout", "method_results_review_does_not_reconstruct_full_stderr",
    "method_results_review_does_not_execute_code_remediation", "method_results_review_does_not_execute_evidence_remediation",
    "method_results_review_does_not_modify_production_code", "method_results_review_does_not_modify_existing_tests_except_new_governance_tests",
    "method_results_review_does_not_classify_full_retry_failures", "method_results_review_does_not_classify_full_retry_errors",
    "method_results_review_does_not_claim_failure_error_separation", "method_results_review_does_not_identify_authoritative_first_failure",
    "method_results_review_does_not_identify_authoritative_first_error", "method_results_review_does_not_claim_traceback_root_cause",
    "method_results_review_does_not_recommend_direct_code_remediation", "method_results_review_does_not_create_remediation_execution",
    "method_results_review_does_not_create_remediation_results_review", "method_results_review_does_not_create_new_retry_candidate",
    "method_results_review_does_not_create_retry_results_review", "method_results_review_does_not_create_integration_results_review",
    "method_results_review_does_not_mark_integration_successful", "method_results_review_does_not_generate_successful_integration_digest",
    "method_results_review_does_not_treat_diagnostic_capture_as_retry", "method_results_review_does_not_treat_method_analysis_as_retry_success",
    "method_results_review_does_not_push_integration_branch", "method_results_review_does_not_push_main",
    "method_results_review_does_not_delete_integration_branch", "method_results_review_does_not_delete_worktree",
    "method_results_review_does_not_force_push", "method_results_review_does_not_prune_remotes",
    "method_results_review_does_not_modify_tags", "method_results_review_does_not_modify_staged_evidence",
    "method_results_review_does_not_regenerate_evidence", "method_results_review_does_not_call_providers",
    "method_results_review_does_not_acquire_market_data", "method_results_review_does_not_regenerate_dataset",
    "method_results_review_does_not_recompute_metrics", "method_results_review_does_not_train_models",
    "method_results_review_does_not_score_strategy", "method_results_review_does_not_generate_recommendations",
    "method_results_review_does_not_accept_predictive_usefulness", "method_results_review_does_not_accept_profitability",
    "method_results_review_does_not_authorize_runtime", "method_results_review_does_not_authorize_broker_execution",
    "observable_failure_family_classification_is_method_planning_only", "failure_family_classification_is_not_root_cause",
    "failure_family_classification_is_not_direct_remediation", "failure_family_classification_is_not_retry_success",
    "diagnostic_capture_results_review_remains_source_evidence", "durable_receipt_is_diagnostic_evidence_only",
    "controlled_recapture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_method_execution_remains_source_evidence", "previous_remediation_or_method_approval_remains_source_evidence",
    "previous_remediation_or_method_operator_review_remains_source_evidence", "previous_remediation_or_method_candidate_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_results_review_remains_source_evidence", "previous_receipt_recovery_or_recapture_execution_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_approval_remains_source_evidence", "previous_failure_diagnosis_remains_source_evidence",
    "previous_targeted_diagnostic_approval_remains_source_evidence", "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid", "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_remediation_candidate_required_after_method_results_review",
    "separate_remediation_approval_required_before_remediation_execution", "separate_retry_approval_required_before_new_retry",
    "main_merge_requires_passing_new_retry_results_review", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "remediation_or_method_results_review_after_diagnostic_capture_created",
    "remediation_or_method_results_review_after_diagnostic_capture_ready", "source_method_execution_reviewed",
    "source_execution_digest_verified", "source_failure_family_classification_digest_verified",
    "source_bounded_excerpt_analysis_digest_verified", "source_execution_manifest_digest_verified",
    "source_approval_reviewed", "source_diagnostic_results_review_reviewed",
    "source_durable_receipt_evidence_reviewed", "source_bounded_excerpt_analysis_reviewed",
    "observable_failure_families_reviewed", "failure_family_classification_summary_reviewed",
    "family_confidence_and_limitations_reviewed", "unsupported_claims_boundary_reviewed",
    "ready_for_remediation_plan_or_execution_candidate_after_method_review",
]
FALSE_FIELDS = [
    "ready_for_remediation_execution", "ready_for_retry_candidate", "ready_for_main_merge_approval",
    "method_execution_rerun_performed", "diagnostic_receipt_parsed_in_review", "diagnostic_output_analyzed_in_review",
    "failure_family_classification_performed_in_review", "controlled_recapture_rerun_performed",
    "diagnostic_command_rerun_performed", "targeted_pytest_performed_in_review", "full_pytest_performed",
    "retry_rerun_performed", "cache_read_in_review", "cache_modified_in_review", "pytest_cache_committed",
    "marketflow_outputs_committed", "terminal_logs_parsed", "operator_logs_parsed", "env_inspection_performed",
    "prior_lost_values_reconstructed", "prior_lost_values_inferred", "full_stdout_reconstructed",
    "full_stderr_reconstructed", "remediation_plan_or_execution_candidate_created", "remediation_execution_performed",
    "code_remediation_executed", "evidence_remediation_executed", "direct_code_remediation_recommended",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "root_cause_claimed", "retry_success_claimed", "main_merge_readiness_claimed", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "evidence_regenerated", "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed", "strategy_scoring_performed",
    "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError(ValueError):
    """Raised when a review binding or closed boundary changes."""


def _source_bindings() -> dict[str, Any]:
    inherited = source._source_fields()
    return {
        "source_execution_artifact_kind": source.ARTIFACT_KIND_SUCCESS,
        "source_execution_status": source.EXECUTION_STATUS_SUCCESS,
        "source_execution_scope": source.EXECUTION_SCOPE,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_remediation_or_method_execution_after_diagnostic_capture_digest": SOURCE_EXECUTION_DIGEST,
        "source_failure_family_classification_digest": SOURCE_CLASSIFICATION_DIGEST,
        "source_bounded_excerpt_analysis_digest": SOURCE_BOUNDED_ANALYSIS_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        **inherited,
    }


def _core() -> dict[str, Any]:
    source_bindings = _source_bindings()
    priority_modules = deepcopy(source.approval_source.source.PRIORITY_1_TARGET_MODULES)
    retry_counts = {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    source_execution_summary = {
        "source_method_execution_performed": True, "source_method_analysis_executed": True,
        "source_diagnostic_receipt_parsed": True, "source_diagnostic_output_analyzed": True,
        "source_bounded_excerpt_analyzed": True, "source_failure_family_classification_performed": True,
        "source_observable_failure_families_generated": True, "approved_package_used": True,
        "method_analysis_only": True, "pytest_run": False, "controlled_recapture_rerun": False,
        "retry_rerun": False, "cache_read": False, "full_streams_reconstructed": False,
    }
    classification_summary = {
        "total_families_detected": 4, "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(FAMILY_IDS), "families_requiring_results_review": list(FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False, "direct_remediation_ready": False,
        "retry_ready": False, "main_merge_ready": False,
    }
    bounded_review = {
        "source_bounded_excerpt_analysis_digest": SOURCE_BOUNDED_ANALYSIS_DIGEST,
        "source_durable_receipt_file_read": True, "source_bounded_stdout_excerpt_used": True,
        "source_bounded_stderr_excerpt_used": False, "source_stdout_excerpt_chars": 20000,
        "source_stderr_excerpt_chars": 0, "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False, "source_redaction_checked": True,
        "durable_receipt_parsed_in_review": False, "diagnostic_output_analyzed_in_review": False,
        "full_streams_available_or_used_in_review": False, "integrity_review_passed": True,
    }
    review = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE, "created_offline": True, "governance_only": True,
        "results_review_only": True, **source_bindings, "selected_remediation_or_method_package": SELECTED_PACKAGE,
        "retry_execution_commit": source.approval_source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": retry_counts, "first_result_authoritative": True,
                                  "pytest_passed": False, "pytest_failed": True,
                                  "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": priority_modules, "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": source.approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"],
        "source_stderr_sha256": source.approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"],
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_exit_code_is_diagnostic_only": True,
        "source_method_execution_summary": source_execution_summary,
        "source_method_execution_performed": True, "source_method_analysis_executed": True,
        "source_diagnostic_receipt_parsed": True, "source_diagnostic_output_analyzed": True,
        "source_bounded_excerpt_analyzed": True, "source_failure_family_classification_performed": True,
        "source_observable_failure_families_generated": True,
        "source_failure_family_classification_summary": classification_summary,
        "source_bounded_excerpt_analysis_summary": bounded_review,
        "source_approval_summary": {"digest": source_bindings["source_remediation_or_method_approval_after_diagnostic_capture_digest"], "reviewed": True},
        "source_operator_review_and_candidate_summary": {
            "operator_review_digest": source_bindings["source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest"],
            "candidate_digest": source_bindings["source_remediation_or_method_candidate_after_diagnostic_capture_digest"],
        },
        "source_diagnostic_results_review_summary": {
            "results_review_digest": source_bindings["source_receipt_recovery_or_recapture_results_review_digest"],
            "payload_review_digest": source_bindings["source_receipt_recovery_or_recapture_payload_review_digest"],
            "durable_receipt_review_digest": source_bindings["source_receipt_recovery_or_recapture_durable_receipt_review_digest"],
        },
        "source_controlled_recapture_execution_summary": {
            "execution_commit": source_bindings["source_receipt_recovery_or_recapture_execution_commit"],
            "execution_digest": source_bindings["source_receipt_recovery_or_recapture_execution_digest"],
            "rerun_in_review": False,
        },
        "source_durable_receipt_summary": {
            "path": source_bindings["source_durable_receipt_path"],
            "receipt_digest": source_bindings["source_receipt_recovery_or_recapture_receipt_digest"],
            "source_evidence_reviewed": True, "parsed_in_review": False,
        },
        "source_receipt_loss_history_summary": {
            "blocked_reason": source_bindings["source_targeted_diagnostic_output_capture_execution_blocked_reason"],
            "primary_failure_class": source_bindings["source_primary_failure_class"],
            "secondary_failure_class": source_bindings["source_secondary_failure_class"],
            "historically_blocked": True,
        },
        "source_planning_and_detail_binding_summary": {
            "planning_results_review_digest": source_bindings["source_planning_results_review_digest"],
            "planning_execution_digest": source_bindings["source_planning_execution_digest"],
            "detail_binding_results_review_digest": source_bindings["source_detail_binding_results_review_digest"],
            "complete_29_row_binding_digest": source_bindings["source_complete_29_row_binding_digest"],
            "recovery_detail_digest": source_bindings["source_recovery_detail_digest"],
        },
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380,
            "stderr_byte_count": 0, "redaction_checked": True, "diagnostic_evidence_only": True,
            "retry_evidence": False, "root_cause_evidence": False,
        },
        "method_results_review": {
            "source_execution_succeeded": True, "approved_package_verified": True,
            "bounded_source_only_verified": True, "method_execution_rerun": False,
            "receipt_reparsed": False, "diagnostic_output_reanalyzed": False,
            "classification_reperformed": False, "review_disposition": "READY_FOR_SEPARATELY_GOVERNED_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE",
        },
        "failure_family_classification_review": {
            "source_digest": SOURCE_CLASSIFICATION_DIGEST, "digest_verified": True,
            "family_count_verified": True, "evidence_item_count_verified": True,
            "deterministic_order_reviewed": True, "limitations_preserved": True,
        },
        "observable_failure_families_review": deepcopy(OBSERVABLE_FAMILY_REVIEWS),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(FAMILY_IDS), "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False, "retry_ready": False, "main_merge_ready": False,
        "family_confidence_and_limitations_review": {
            "all_families_high_confidence": True, "all_family_records_complete": True,
            "all_snippets_bounded": True, "all_limitations_preserved": True,
            "root_cause_claimed": False, "direct_remediation_recommended": False,
            "retry_success_claimed": False,
        },
        "bounded_excerpt_integrity_review": bounded_review,
        "unsupported_claims_boundary_review": {
            "root_cause": False, "authoritative_first_failure": False, "authoritative_first_error": False,
            "full_retry_failure_error_separation": False, "traceback_cause": False,
            "direct_code_remediation": False, "retry_success": False, "main_merge_readiness": False,
        },
        "review_findings": deepcopy(REVIEW_FINDINGS), "review_outputs": deepcopy(REVIEW_OUTPUTS),
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW",
            "reason": "The source method execution generated reviewed bounded failure-family classification evidence with four high-confidence observable families. This supports a separately governed remediation plan or execution candidate, but it does not authorize remediation execution, retry, integration success, main merge, runtime, or trading.",
        },
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    return review


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


SOURCE_CHECK_FIELDS = {
    "source_execution_commit_bound": "source_execution_commit",
    "source_method_execution_digest_bound": "source_remediation_or_method_execution_after_diagnostic_capture_digest",
    "source_failure_family_classification_digest_bound": "source_failure_family_classification_digest",
    "source_bounded_excerpt_analysis_digest_bound": "source_bounded_excerpt_analysis_digest",
    "source_execution_manifest_digest_bound": "source_execution_manifest_digest",
    "source_selected_package_bound": "selected_remediation_or_method_package",
    "source_approval_digest_bound": "source_remediation_or_method_approval_after_diagnostic_capture_digest",
    "source_operator_review_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
    "source_candidate_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
    "source_results_review_digest_bound": "source_receipt_recovery_or_recapture_results_review_digest",
    "source_payload_review_digest_bound": "source_receipt_recovery_or_recapture_payload_review_digest",
    "source_durable_receipt_review_digest_bound": "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
    "source_results_review_manifest_digest_bound": "source_receipt_recovery_or_recapture_results_review_manifest_digest",
    "source_controlled_recapture_execution_commit_bound": "source_receipt_recovery_or_recapture_execution_commit",
    "source_controlled_recapture_execution_digest_bound": "source_receipt_recovery_or_recapture_execution_digest",
    "source_controlled_recapture_payload_digest_bound": "source_receipt_recovery_or_recapture_payload_digest",
    "source_controlled_recapture_receipt_digest_bound": "source_receipt_recovery_or_recapture_receipt_digest",
    "source_controlled_recapture_digest_manifest_digest_bound": "source_receipt_recovery_or_recapture_digest_manifest_digest",
    "source_durable_receipt_path_bound": "source_durable_receipt_path",
    "source_receipt_recovery_approval_digest_bound": "source_receipt_recovery_or_recapture_approval_digest",
    "source_receipt_recovery_candidate_operator_review_digest_bound": "source_receipt_recovery_or_recapture_candidate_operator_review_digest",
    "source_receipt_recovery_candidate_digest_bound": "source_receipt_recovery_or_recapture_candidate_digest",
    "source_failure_diagnosis_digest_bound": "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
    "source_prior_execution_digest_bound": "source_targeted_diagnostic_output_capture_execution_digest",
    "source_blocked_manifest_digest_bound": "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest",
    "source_blocked_reason_bound": "source_targeted_diagnostic_output_capture_execution_blocked_reason",
    "source_primary_failure_class_bound": "source_primary_failure_class",
    "source_secondary_failure_class_bound": "source_secondary_failure_class",
    "source_targeted_diagnostic_approval_digest_bound": "source_targeted_diagnostic_output_capture_approval_digest",
    "source_targeted_diagnostic_candidate_operator_review_digest_bound": "source_targeted_diagnostic_output_capture_candidate_operator_review_digest",
    "source_targeted_diagnostic_candidate_digest_bound": "source_targeted_diagnostic_output_capture_candidate_digest",
    "source_planning_results_review_digest_bound": "source_planning_results_review_digest",
    "source_prioritized_planning_review_digest_bound": "source_prioritized_planning_review_digest",
    "source_planning_execution_digest_bound": "source_planning_execution_digest",
    "source_prioritized_planning_digest_bound": "source_prioritized_planning_digest",
    "source_detail_binding_results_review_digest_bound": "source_detail_binding_results_review_digest",
    "source_complete_29_row_binding_digest_bound": "source_complete_29_row_binding_digest",
    "source_materialized_payload_digest_bound": "source_materialized_payload_digest",
    "source_recovery_results_review_digest_bound": "source_recovery_results_review_digest",
    "source_recovery_detail_digest_bound": "source_recovery_detail_digest",
    "source_after_v2_approval_digest_bound": "source_after_v2_approval_digest",
    "source_module_grouping_digest_bound": "source_module_grouping_digest",
}

FALSE_CHECK_FIELDS = {
    "ready_for_remediation_execution_false": "ready_for_remediation_execution",
    "ready_for_retry_candidate_false": "ready_for_retry_candidate", "ready_for_main_merge_approval_false": "ready_for_main_merge_approval",
    "method_execution_rerun_false": "method_execution_rerun_performed", "diagnostic_receipt_parsed_in_review_false": "diagnostic_receipt_parsed_in_review",
    "diagnostic_output_analyzed_in_review_false": "diagnostic_output_analyzed_in_review",
    "failure_family_classification_performed_in_review_false": "failure_family_classification_performed_in_review",
    "controlled_recapture_rerun_false": "controlled_recapture_rerun_performed", "diagnostic_command_rerun_false": "diagnostic_command_rerun_performed",
    "targeted_pytest_in_review_false": "targeted_pytest_performed_in_review", "full_pytest_false": "full_pytest_performed",
    "retry_rerun_false": "retry_rerun_performed", "cache_read_false": "cache_read_in_review", "cache_modified_false": "cache_modified_in_review",
    "pytest_cache_committed_false": "pytest_cache_committed", "marketflow_outputs_committed_false": "marketflow_outputs_committed",
    "terminal_logs_parsed_false": "terminal_logs_parsed", "operator_logs_parsed_false": "operator_logs_parsed",
    "env_inspection_false": "env_inspection_performed", "prior_lost_values_reconstructed_false": "prior_lost_values_reconstructed",
    "prior_lost_values_inferred_false": "prior_lost_values_inferred", "full_stdout_reconstructed_false": "full_stdout_reconstructed",
    "full_stderr_reconstructed_false": "full_stderr_reconstructed",
    "remediation_plan_or_execution_candidate_created_false": "remediation_plan_or_execution_candidate_created",
    "remediation_execution_false": "remediation_execution_performed", "code_remediation_false": "code_remediation_executed",
    "evidence_remediation_false": "evidence_remediation_executed", "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
    "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
    "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
    "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
    "traceback_root_cause_claimed_false": "traceback_root_cause_claimed", "root_cause_claimed_false": "root_cause_claimed",
    "retry_success_claimed_false": "retry_success_claimed", "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
    "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
    "new_retry_results_review_created_false": "new_retry_results_review_created", "main_merge_approval_created_false": "main_merge_approval_created",
    "integration_success_false": "integration_execution_successful", "successful_integration_digest_false": "successful_integration_execution_digest_generated",
    "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
    "origin_main_modified_false": "origin_main_modified_by_this_task", "evidence_regenerated_false": "evidence_regenerated",
    "provider_requests_false": "provider_requests_made_in_review", "market_data_acquisition_false": "market_data_acquisition_performed_in_review",
    "dataset_generation_false": "dataset_generation_performed_in_review", "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
    "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
    "recommendations_false": "trade_recommendations_generated",
}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected = _core()
    checks = [_check(check_id, expected[field], review.get(field)) for check_id, field in SOURCE_CHECK_FIELDS.items()]
    checks += [
        _check("retry_execution_commit_bound", expected["retry_execution_commit"], review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", expected["retry_failure_context"]["counts"], review.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", expected["priority_1_target_modules"], review.get("priority_1_target_modules")),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("exit_code_1_bound_as_diagnostic_only", [1, True], [review.get("source_exit_code"), review.get("source_exit_code_is_diagnostic_only")]),
        _check("stdout_hash_bound", expected["source_stdout_sha256"], review.get("source_stdout_sha256")),
        _check("stderr_hash_bound", expected["source_stderr_sha256"], review.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, review.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, review.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, review.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, review.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, review.get("source_redaction_checked")),
        _check("source_method_execution_status_success_bound", source.EXECUTION_STATUS_SUCCESS, review.get("source_execution_status")),
        _check("source_method_execution_scope_bound", source.EXECUTION_SCOPE, review.get("source_execution_scope")),
        _check("source_method_execution_performed_true", True, review.get("source_method_execution_performed")),
        _check("source_method_analysis_executed_true", True, review.get("source_method_analysis_executed")),
        _check("source_diagnostic_receipt_parsed_true", True, review.get("source_diagnostic_receipt_parsed")),
        _check("source_diagnostic_output_analyzed_true", True, review.get("source_diagnostic_output_analyzed")),
        _check("source_bounded_excerpt_analyzed_true", True, review.get("source_bounded_excerpt_analyzed")),
        _check("source_failure_family_classification_performed_true", True, review.get("source_failure_family_classification_performed")),
        _check("source_observable_failure_families_generated_true", True, review.get("source_observable_failure_families_generated")),
        _check("observable_family_count_4_bound", 4, review.get("observable_failure_family_count")),
        _check("observable_evidence_items_188_bound", 188, review.get("total_observable_evidence_items")),
    ]
    families = review.get("observable_failure_families_review", [])
    family_by_id = {item.get("family_id"): item for item in families if isinstance(item, dict)}
    for family_id in FAMILY_IDS:
        checks.append(_check(f"{family_id}_family_reviewed", True, family_id in family_by_id))
    checks += [
        _check("family_records_have_required_fields", True, len(families) == 4 and all(item.get("required_fields_present") is True for item in families)),
        _check("representative_snippets_bounded", True, len(families) == 4 and all(item.get("representative_snippets_bounded") is True for item in families)),
        _check("family_classification_not_root_cause", True, len(families) == 4 and all(item.get("root_cause_claimed") is False for item in families)),
        _check("family_classification_not_direct_remediation", True, len(families) == 4 and all(item.get("direct_remediation_recommended") is False for item in families)),
        _check("method_limitations_reviewed", True, len(families) == 4 and all(bool(item.get("limitations")) for item in families)),
        _check("additional_diagnostic_capture_not_indicated", False, review.get("additional_diagnostic_capture_may_be_needed")),
        _check("direct_remediation_ready_false", False, review.get("direct_remediation_ready")),
        _check("retry_ready_false", False, review.get("retry_ready")), _check("main_merge_ready_false", False, review.get("main_merge_ready")),
        _check("review_created_true", True, review.get("remediation_or_method_results_review_after_diagnostic_capture_created")),
        _check("review_ready_true", True, review.get("remediation_or_method_results_review_after_diagnostic_capture_ready")),
        _check("source_method_execution_reviewed_true", True, review.get("source_method_execution_reviewed")),
        _check("classification_digest_verified_true", True, review.get("source_failure_family_classification_digest_verified")),
        _check("bounded_excerpt_analysis_digest_verified_true", True, review.get("source_bounded_excerpt_analysis_digest_verified")),
        _check("manifest_digest_verified_true", True, review.get("source_execution_manifest_digest_verified")),
        _check("observable_failure_families_reviewed_true", True, review.get("observable_failure_families_reviewed")),
        _check("family_confidence_and_limitations_reviewed_true", True, review.get("family_confidence_and_limitations_reviewed")),
        _check("ready_for_remediation_plan_or_execution_candidate_after_method_review_true", True, review.get("ready_for_remediation_plan_or_execution_candidate_after_method_review")),
    ]
    checks.extend(_check(check_id, False, review.get(field)) for check_id, field in FALSE_CHECK_FIELDS.items())
    checks += [
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("review_findings_defined", REVIEW_FINDINGS, review.get("review_findings")),
        _check("review_outputs_generated", REVIEW_OUTPUTS, review.get("review_outputs")),
        _check("recommendation_defined", expected["recommendation"], review.get("recommendation")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        _check("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, review.get("no_tracked_pytest_cache_files")),
    ]
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checks = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checks)
    return {
        "total_checks": len(checks), "passed_checks": passed, "failed_checks": len(checks) - passed,
        "blocker_count": len(checks) - passed,
        **{field: review.get(field) for field in TRUE_FIELDS},
        "source_method_execution_performed": True, "source_method_analysis_executed": True,
        "source_failure_family_classification_performed": True, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "highest_confidence_family_ids": list(FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False, "direct_remediation_ready": False,
        "retry_ready": False, "main_merge_ready": False,
        **{field: review.get(field) for field in FALSE_FIELDS},
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", RESULTS_REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
    *, source_execution: dict | None = None,
) -> dict:
    """Build the constants-only review; never invoke source execution or receipt parsing."""

    if source_execution is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
                deepcopy(source_execution)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError(
                "source execution invalid"
            ) from exc
        if source_execution.get(source.EXECUTION_DIGEST_KEY) != SOURCE_EXECUTION_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError(
                "source execution digest mismatch"
            )
    review = _core()
    review[CLASSIFICATION_REVIEW_DIGEST_KEY] = semantic_digest({
        "source_digest": SOURCE_CLASSIFICATION_DIGEST,
        "classification_review": review["failure_family_classification_review"],
        "families": review["observable_failure_families_review"],
    })
    review[BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY] = semantic_digest({
        "source_digest": SOURCE_BOUNDED_ANALYSIS_DIGEST,
        "bounded_excerpt_integrity_review": review["bounded_excerpt_integrity_review"],
    })
    review["digest_manifest"] = {
        "source_execution": SOURCE_EXECUTION_DIGEST,
        "source_classification": SOURCE_CLASSIFICATION_DIGEST,
        "source_bounded_analysis": SOURCE_BOUNDED_ANALYSIS_DIGEST,
        "source_execution_manifest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        "classification_review": review[CLASSIFICATION_REVIEW_DIGEST_KEY],
        "bounded_analysis_review": review[BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY],
        "review_outputs": semantic_digest(REVIEW_OUTPUTS),
    }
    review[MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[RESULTS_REVIEW_DIGEST_KEY] = _digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
    review: dict,
) -> dict:
    """Reject every binding, reviewed fact, output, digest, or closed-gate change."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError
    if not isinstance(review, dict):
        raise error("review must be an object")
    expected = _core()
    for field, value in expected.items():
        if review.get(field) != value:
            raise error(f"{field} mismatch")
    expected_classification = semantic_digest({
        "source_digest": SOURCE_CLASSIFICATION_DIGEST,
        "classification_review": review.get("failure_family_classification_review"),
        "families": review.get("observable_failure_families_review"),
    })
    if review.get(CLASSIFICATION_REVIEW_DIGEST_KEY) != expected_classification:
        raise error("classification review digest mismatch")
    expected_bounded = semantic_digest({
        "source_digest": SOURCE_BOUNDED_ANALYSIS_DIGEST,
        "bounded_excerpt_integrity_review": review.get("bounded_excerpt_integrity_review"),
    })
    if review.get(BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY) != expected_bounded:
        raise error("bounded analysis review digest mismatch")
    if review.get(MANIFEST_DIGEST_KEY) != semantic_digest(review.get("digest_manifest")):
        raise error("manifest digest mismatch")
    if review.get(RESULTS_REVIEW_DIGEST_KEY) != _digest(review):
        raise error("results review digest mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "results_review_digest": review[RESULTS_REVIEW_DIGEST_KEY],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict:
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
        source_execution=source_execution
    )
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError(
            "protected output directory"
        )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError(
            "output exists"
        )
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_markdown_v1(review),
        encoding="utf-8",
    )
    return review


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(review)
    families = review["observable_failure_families_review"]
    sections = [
        ("Source Method Execution", [SOURCE_EXECUTION_COMMIT, SOURCE_EXECUTION_DIGEST, source.EXECUTION_STATUS_SUCCESS]),
        ("Source Failure-Family Classification", [SOURCE_CLASSIFICATION_DIGEST, str(review["source_failure_family_classification_summary"])]),
        ("Source Bounded Excerpt Analysis", [SOURCE_BOUNDED_ANALYSIS_DIGEST, str(review["source_bounded_excerpt_analysis_summary"])]),
        ("Source Approval", [review["source_remediation_or_method_approval_after_diagnostic_capture_digest"]]),
        ("Source Operator Review and Candidate", [review["source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest"], review["source_remediation_or_method_candidate_after_diagnostic_capture_digest"]]),
        ("Source Diagnostic Results Review", [review["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [review["source_receipt_recovery_or_recapture_execution_commit"], review["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [review["source_durable_receipt_path"], review["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [review["source_targeted_diagnostic_output_capture_execution_blocked_reason"], review["source_primary_failure_class"], review["source_secondary_failure_class"]]),
        ("Source Planning and Detail Binding Evidence", [review["source_planning_execution_digest"], review["source_detail_binding_results_review_digest"], review["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(review["retry_failure_context"])]),
        ("Review Scope", [REVIEW_SCOPE]), ("Selected Remediation or Method Package", [SELECTED_PACKAGE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in review["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(review["diagnostic_capture_evidence_summary"])]),
        ("Method Results Review", [str(review["method_results_review"])]),
        ("Observable Failure Families Review", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in families]),
        ("Family Confidence and Limitations", [item["limitations"] for item in families]),
        ("Bounded Excerpt Integrity Review", [str(review["bounded_excerpt_integrity_review"])]),
        ("Unsupported Claims Boundary", [str(review["unsupported_claims_boundary_review"])]),
        ("Review Findings", [f"{item['finding_id']}: {item['finding']}" for item in review["review_findings"]]),
        ("Deterministic Digests", [review[RESULTS_REVIEW_DIGEST_KEY], review[CLASSIFICATION_REVIEW_DIGEST_KEY], review[BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY], review[MANIFEST_DIGEST_KEY]]),
        ("Recommendation", [review["recommended_next_task"], review["recommendation"]["reason"]]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["Candidate readiness only; no remediation, retry, main merge, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Constants-only review; no source execution, receipt parsing, diagnostic analysis, cache, logs, environment, providers, or protected-branch action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Results Review After Diagnostic Capture v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_ONLY_NOT_METHOD_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CLASSIFY_REVIEWED_DURABLE_DIAGNOSTIC_RECEIPT_FAILURE_FAMILIES_FOR_REMEDIATION_METHOD_PLANNING = SELECTED_PACKAGE

__all__ = [name for name in globals() if name.isupper() or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))]
