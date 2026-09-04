"""Define candidate-only remediation or method options after diagnostic capture."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_V1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_digest"

SOURCE_RESULTS_REVIEW_COMMIT = "6ad5b9534f659a5b04595dd3e55800eced8c93c4"
SOURCE_RESULTS_REVIEW_DIGEST = "427d2a76afcec7c8b9647a0f0c19b6037e5a451b0f70fad1a5025afc266946ba"
SOURCE_PAYLOAD_REVIEW_DIGEST = "bdba29bcb8835cb3b06caa0b4028b5480af04b6ecc28bd01392784e549556ee3"
SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST = "2cd966d75bd70fc3bcb6d3f7b9ed33dacc47fde0d2697dfc24d0f7e0b1e4bdcd"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "c3394bb56e7c20ed46274dc270992011417f52c3174cf3094c50cea3be823ce4"
SOURCE_EXECUTION_COMMIT = source.SOURCE_EXECUTION_COMMIT
SOURCE_EXECUTION_DIGEST = source.SOURCE_EXECUTION_DIGEST
SOURCE_PAYLOAD_DIGEST = source.SOURCE_PAYLOAD_DIGEST
SOURCE_RECEIPT_DIGEST = source.SOURCE_RECEIPT_DIGEST
SOURCE_DIGEST_MANIFEST_DIGEST = source.SOURCE_DIGEST_MANIFEST_DIGEST
SOURCE_DURABLE_RECEIPT_PATH = source.SOURCE_DURABLE_RECEIPT_PATH
SOURCE_BINDINGS = deepcopy(source.SOURCE_BINDINGS)
RETRY_EXECUTION_COMMIT = source.RETRY_EXECUTION_COMMIT
PRIORITY_1_TARGET_MODULES = deepcopy(source.PRIORITY_1_TARGET_MODULES)

RECOMMENDED_PACKAGE = "PACKAGE_CLASSIFY_REVIEWED_DURABLE_DIAGNOSTIC_RECEIPT_FAILURE_FAMILIES_FOR_REMEDIATION_METHOD_PLANNING"
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_OPERATOR_REVIEW_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_PHILOSOPHY_TEXT = (
    "The controlled diagnostic recapture produced a finalized durable receipt with command identity, approved "
    "target modules, exit code, stdout/stderr hashes, byte counts, bounded output status, and redaction review. "
    "The next safe step is to define governed method or remediation-planning options that may use the reviewed "
    "durable receipt evidence in a future approved execution. This candidate must not analyze the diagnostic "
    "output, infer root cause, recommend direct code changes, execute remediation, or create retry readiness."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no method execution, remediation, diagnostic rerun, classification, retry, results review, "
    "main merge, runtime, or trading authority is created."
)
CANDIDATE_GOAL = (
    "Define safe future remediation-or-method packages after diagnostic capture, preserving the diagnostic "
    "evidence as planning input only."
)
RECOMMENDATION_REASON = (
    "The durable diagnostic receipt has been reviewed and contains bounded diagnostic evidence for the approved "
    "Priority 1 modules. A future failure-family classification method can convert that evidence into a reviewed "
    "remediation-planning basis without jumping directly to code changes, retry, or main merge."
)


def _package(package_id: str, status: str, purpose: str, *, blocked_reason: str | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "package_id": package_id,
        "status": status,
        "purpose": purpose,
        "selected": False,
        "approved": False,
        "executed": False,
    }
    if blocked_reason is not None:
        item["blocked_reason"] = blocked_reason
    return item


PROPOSED_PACKAGES = [
    {
        **_package(
            RECOMMENDED_PACKAGE,
            RECOMMENDATION_STATUS,
            "Future execution may read the committed durable receipt and reviewed bounded diagnostic excerpts to classify observable failure families and propose a remediation-method direction, without claiming root cause, first-failure order, retry success, or direct code remediation.",
        ),
        "recommended_reason": "The diagnostic receipt is now durable and reviewed. A bounded failure-family classification method is the safest next step before any remediation approval or retry candidate.",
    },
    _package(
        "PACKAGE_REVIEW_BOUNDED_STDOUT_EXCERPT_FOR_REPEATING_ASSERTION_OR_IMPORT_PATTERNS",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may inspect only the committed bounded stdout excerpt to identify repeated diagnostic patterns such as assertion mismatch families, import/setup failures, fixture assumptions, or path-sensitive failures.",
    ),
    _package(
        "PACKAGE_REVIEW_PRIORITY_1_MODULES_AGAINST_CAPTURED_OUTPUT_FOR_TEST_FIXTURE_ISOLATION",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may compare the five Priority 1 module identities with captured diagnostic output to identify whether failures appear concentrated around fixture isolation, shared constants, evidence-bound digests, or branch/worktree assumptions.",
    ),
    _package(
        "PACKAGE_REVIEW_EVIDENCE_AND_DIGEST_BOUNDARY_PATTERNS_FROM_DIAGNOSTIC_OUTPUT",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may inspect bounded diagnostic output for recurring evidence-root, digest, path, or artifact-boundary assertion patterns.",
    ),
    _package(
        "PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_CURRENT_RECEIPT_IS_INSUFFICIENT",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may recommend an additional separately approved diagnostic capture only if the reviewed durable receipt is insufficient for failure-family planning.",
    ),
    _package(
        "PACKAGE_CREATE_REMEDIATION_PLAN_ONLY_AFTER_FAILURE_FAMILY_CLASSIFICATION",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "Future execution may create a remediation plan after a reviewed failure-family classification result, without changing code or rerunning tests.",
    ),
    _package(
        "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_DIAGNOSTIC_CAPTURE",
        "BLOCKED_NOT_ALLOWED",
        "Apply code changes directly from diagnostic-capture metadata.",
        blocked_reason="The current evidence has not yet been analyzed or reviewed for failure families, root-cause mechanisms, or safe remediation scope.",
    ),
    _package(
        "PACKAGE_CLAIM_ROOT_CAUSE_FROM_BOUNDED_OUTPUT_ONLY",
        "BLOCKED_NOT_ALLOWED",
        "Claim root cause using bounded diagnostic output alone.",
        blocked_reason="Bounded diagnostic output may support failure-family planning, but it does not by itself establish root cause.",
    ),
    _package(
        "PACKAGE_USE_EXIT_CODE_OR_STDOUT_HASH_AS_REMEDIATION_BASIS",
        "BLOCKED_NOT_ALLOWED",
        "Use the exit code or stream hash as a direct remediation basis.",
        blocked_reason="Exit code and stream hashes verify diagnostic capture integrity, but they do not identify the failure mechanism.",
    ),
    _package(
        "PACKAGE_RERUN_CONTROLLED_RECAPTURE_FOR_METHOD_ANALYSIS",
        "BLOCKED_NOT_ALLOWED",
        "Rerun controlled recapture for method analysis.",
        blocked_reason="The controlled recapture has already produced durable diagnostic evidence; any further capture requires separate governance and justification.",
    ),
    _package(
        "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_OR_METHOD_RESULTS_REVIEW",
        "BLOCKED_NOT_ALLOWED",
        "Create a new retry without a remediation or method results review.",
        blocked_reason="A new retry remains blocked until remediation or method analysis is approved, executed, and reviewed.",
    ),
    _package(
        "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
        "BLOCKED_NOT_ALLOWED",
        "Proceed to main merge despite the failed retry.",
        blocked_reason="Main merge remains blocked until a future retry results review passes.",
    ),
]

FUTURE_METHOD_REQUIREMENTS = {
    key: True
    for key in (
        "source_results_review_must_be_ready",
        "source_results_review_digest_must_be_bound",
        "source_payload_review_digest_must_be_bound",
        "source_durable_receipt_review_digest_must_be_bound",
        "source_results_review_manifest_digest_must_be_bound",
        "source_execution_digest_must_be_bound",
        "source_payload_digest_must_be_bound",
        "source_durable_receipt_digest_must_be_bound",
        "source_digest_manifest_digest_must_be_bound",
        "source_durable_receipt_path_must_be_bound",
        "source_controlled_recapture_must_be_reviewed_successful",
        "source_exit_code_must_be_reviewed_as_diagnostic_only",
        "source_stdout_hash_must_be_bound",
        "source_stderr_hash_must_be_bound",
        "source_stdout_byte_count_must_be_1231380",
        "source_stderr_byte_count_must_be_0",
        "source_bounded_output_status_must_be_bound",
        "source_redaction_checked_must_be_true",
        "retry_failure_counts_must_be_bound",
        "priority_1_top_module_paths_must_be_bound",
        "priority_1_total_must_be_612",
        "top_10_total_must_be_1069",
        "module_summary_total_must_be_29",
        "failed_or_errored_nodeids_total_must_be_1404",
        "future_method_must_use_committed_durable_receipt_only_if_approved",
        "future_method_must_not_run_pytest",
        "future_method_must_not_rerun_recapture",
        "future_method_must_not_rerun_retry",
        "future_method_must_not_read_pytest_cache",
        "future_method_must_not_parse_terminal_or_operator_logs",
        "future_method_must_not_inspect_env",
        "future_method_must_not_reconstruct_full_streams",
        "future_method_must_preserve_output_bounding_limitations",
        "future_method_must_not_claim_first_failure",
        "future_method_must_not_claim_root_cause_without_review",
        "future_method_must_not_recommend_direct_code_remediation_without_results_review",
        "future_method_results_review_required_before_remediation_execution",
        "future_retry_requires_separate_candidate_approval_execution_and_review",
        "main_merge_requires_passing_retry_results_review",
    )
}

FUTURE_METHOD_PLAN = [
    "Bind this candidate and the source diagnostic results-review evidence.",
    "Bind the source execution, payload, durable receipt, and manifest digests.",
    "Bind the durable receipt path and reviewed diagnostic capture facts.",
    "Bind retry failure counts and Priority 1 module facts.",
    "Select one remediation-or-method package.",
    "If failure-family classification is selected, read only the committed durable receipt and bounded excerpts.",
    "Preserve the output-bounding limitation and do not claim full stdout/stderr reconstruction.",
    "Extract only observable diagnostic families, not root cause or first-failure order.",
    "Separate assertion, setup/import, fixture, digest, evidence-root, path/CWD, and governance-boundary families only if supported by the reviewed receipt.",
    "Generate a method-execution artifact with explicit limitations.",
    "Require method results review before any remediation execution or new retry candidate.",
    "Keep retry, main merge, runtime, broker, and trading closed.",
]

PLANNED_OUTPUTS = {
    name: "PLANNED_NOT_GENERATED"
    for name in (
        "remediation_or_method_candidate_after_diagnostic_capture_manifest",
        "source_diagnostic_results_review_binding_report",
        "durable_receipt_evidence_summary",
        "controlled_recapture_evidence_integrity_report",
        "priority_1_target_module_context_report",
        "proposed_method_package_comparison_report",
        "recommended_failure_family_classification_package_report",
        "future_method_requirements_report",
        "future_method_plan_report",
        "output_bounding_limitation_report",
        "unsupported_claims_boundary_report",
        "remediation_gate_preservation_report",
        "retry_gate_preservation_report",
        "digest_manifest",
    )
}

NON_GOALS = [
    "do_not_select_remediation_or_method_package_now", "do_not_approve_remediation_or_method_package_now",
    "do_not_execute_method_analysis_now", "do_not_execute_remediation_now", "do_not_parse_durable_receipt_now",
    "do_not_analyze_diagnostic_output_now", "do_not_rerun_controlled_recapture_now",
    "do_not_run_diagnostic_command_now", "do_not_run_targeted_pytest_now", "do_not_run_full_pytest_now",
    "do_not_rerun_retry_now", "do_not_read_cache_now", "do_not_modify_cache_now",
    "do_not_parse_terminal_logs_now", "do_not_parse_operator_logs_now", "do_not_inspect_env_now",
    "do_not_reconstruct_prior_lost_values_now", "do_not_reconstruct_full_stdout_or_stderr_now",
    "do_not_classify_modules_again_now", "do_not_claim_failure_error_separation_now",
    "do_not_identify_first_failure_now", "do_not_identify_first_error_now",
    "do_not_claim_traceback_root_cause_now", "do_not_recommend_direct_code_remediation_now",
    "do_not_create_remediation_approval_now", "do_not_create_remediation_execution_now",
    "do_not_create_remediation_results_review_now", "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review_now", "do_not_create_integration_results_review_now",
    "do_not_mark_integration_successful", "do_not_push_integration_branch", "do_not_push_main",
    "do_not_commit_marketflow_outputs", "do_not_commit_pytest_cache", "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability", "do_not_authorize_runtime", "do_not_authorize_trading",
]

NEXT_CHAIN = [
    "Remediation or Method Candidate After Diagnostic Capture Operator Review v1.",
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
    "remediation_or_method_candidate_after_diagnostic_capture_operator_review",
    "remediation_or_method_approval_if_selected", "remediation_or_method_execution_if_approved",
    "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "candidate_after_diagnostic_capture_does_not_select_package",
    "candidate_after_diagnostic_capture_does_not_approve_package",
    "candidate_after_diagnostic_capture_does_not_execute_method_analysis",
    "candidate_after_diagnostic_capture_does_not_execute_remediation",
    "candidate_after_diagnostic_capture_does_not_parse_durable_receipt",
    "candidate_after_diagnostic_capture_does_not_analyze_diagnostic_output",
    "candidate_after_diagnostic_capture_does_not_rerun_controlled_recapture",
    "candidate_after_diagnostic_capture_does_not_run_diagnostic_command",
    "candidate_after_diagnostic_capture_does_not_run_targeted_pytest",
    "candidate_after_diagnostic_capture_does_not_run_full_pytest",
    "candidate_after_diagnostic_capture_does_not_rerun_retry",
    "candidate_after_diagnostic_capture_does_not_read_pytest_cache",
    "candidate_after_diagnostic_capture_does_not_modify_pytest_cache",
    "candidate_after_diagnostic_capture_does_not_parse_terminal_logs",
    "candidate_after_diagnostic_capture_does_not_parse_operator_logs",
    "candidate_after_diagnostic_capture_does_not_inspect_env",
    "candidate_after_diagnostic_capture_does_not_reconstruct_prior_lost_values",
    "candidate_after_diagnostic_capture_does_not_reconstruct_full_streams",
    "candidate_after_diagnostic_capture_does_not_classify_modules_again",
    "candidate_after_diagnostic_capture_does_not_claim_failure_error_separation",
    "candidate_after_diagnostic_capture_does_not_identify_first_failure",
    "candidate_after_diagnostic_capture_does_not_identify_first_error",
    "candidate_after_diagnostic_capture_does_not_claim_traceback_root_cause",
    "candidate_after_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "candidate_after_diagnostic_capture_does_not_create_remediation_execution",
    "candidate_after_diagnostic_capture_does_not_create_remediation_results_review",
    "candidate_after_diagnostic_capture_does_not_create_new_retry_candidate",
    "candidate_after_diagnostic_capture_does_not_create_retry_results_review",
    "candidate_after_diagnostic_capture_does_not_create_integration_results_review",
    "candidate_after_diagnostic_capture_does_not_mark_integration_successful",
    "candidate_after_diagnostic_capture_does_not_generate_successful_integration_digest",
    "candidate_after_diagnostic_capture_does_not_treat_diagnostic_capture_as_retry",
    "candidate_after_diagnostic_capture_does_not_treat_exit_code_as_retry_result",
    "candidate_after_diagnostic_capture_does_not_push_integration_branch",
    "candidate_after_diagnostic_capture_does_not_push_main",
    "candidate_after_diagnostic_capture_does_not_delete_integration_branch",
    "candidate_after_diagnostic_capture_does_not_delete_worktree",
    "candidate_after_diagnostic_capture_does_not_force_push",
    "candidate_after_diagnostic_capture_does_not_prune_remotes",
    "candidate_after_diagnostic_capture_does_not_modify_tags",
    "candidate_after_diagnostic_capture_does_not_modify_staged_evidence",
    "candidate_after_diagnostic_capture_does_not_regenerate_evidence",
    "candidate_after_diagnostic_capture_does_not_call_providers",
    "candidate_after_diagnostic_capture_does_not_acquire_market_data",
    "candidate_after_diagnostic_capture_does_not_regenerate_dataset",
    "candidate_after_diagnostic_capture_does_not_recompute_metrics",
    "candidate_after_diagnostic_capture_does_not_train_models",
    "candidate_after_diagnostic_capture_does_not_score_strategy",
    "candidate_after_diagnostic_capture_does_not_generate_recommendations",
    "candidate_after_diagnostic_capture_does_not_accept_predictive_usefulness",
    "candidate_after_diagnostic_capture_does_not_accept_profitability",
    "candidate_after_diagnostic_capture_does_not_authorize_runtime",
    "candidate_after_diagnostic_capture_does_not_authorize_broker_execution",
    "diagnostic_capture_results_review_remains_source_evidence", "durable_receipt_is_diagnostic_evidence_only",
    "controlled_recapture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation",
    "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_receipt_recovery_or_recapture_results_review_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_execution_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_approval_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence",
    "previous_targeted_diagnostic_approval_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_operator_review_required_before_method_approval",
    "separate_approval_required_before_method_execution",
    "separate_results_review_required_after_method_execution",
    "separate_retry_approval_required_before_new_retry", "main_merge_requires_passing_new_retry_results_review",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "remediation_or_method_candidate_after_diagnostic_capture_created",
    "remediation_or_method_candidate_after_diagnostic_capture_ready_for_operator_review",
    "source_diagnostic_results_review_bound", "source_controlled_recapture_results_reviewed",
    "durable_receipt_evidence_bound", "diagnostic_capture_evidence_available_for_future_method",
    "remediation_or_method_packages_defined", "future_method_requirements_defined",
    "future_method_plan_defined", "ready_for_remediation_or_method_candidate_operator_review",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]

FALSE_FIELDS = [
    "remediation_or_method_package_selected", "remediation_or_method_package_approved",
    "remediation_or_method_package_authorized", "remediation_or_method_execution_performed",
    "method_analysis_executed", "remediation_execution_performed", "code_remediation_executed",
    "evidence_remediation_executed", "diagnostic_receipt_parsed_in_candidate",
    "diagnostic_output_analyzed_in_candidate", "failure_family_classification_performed",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "controlled_recapture_rerun_performed", "diagnostic_command_rerun_performed",
    "targeted_pytest_performed_in_candidate", "full_pytest_performed", "retry_rerun_performed",
    "cache_read_in_candidate", "cache_modified_in_candidate", "pytest_cache_committed",
    "marketflow_outputs_committed", "terminal_logs_parsed", "operator_logs_parsed",
    "env_inspection_performed", "prior_lost_values_reconstructed", "prior_lost_values_inferred",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "ready_for_remediation_or_method_approval",
    "ready_for_remediation_or_method_execution", "ready_for_retry_candidate",
    "ready_for_main_merge_approval", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "evidence_regenerated", "provider_requests_made_in_candidate",
    "market_data_acquisition_performed_in_candidate", "dataset_generation_performed_in_candidate",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed",
    "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError(ValueError):
    """Raised when candidate evidence or authority boundaries are invalid."""


def _source_fields(source_results_review: dict | None) -> dict[str, Any]:
    if source_results_review is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(
                deepcopy(source_results_review)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError(
                "source results review validation failed"
            ) from exc
        if source_results_review.get(source.RESULTS_REVIEW_DIGEST_KEY) != SOURCE_RESULTS_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError(
                "source results review digest mismatch"
            )
    return {
        "source_results_review_artifact_kind": source.ARTIFACT_KIND,
        "source_results_review_status": source.REVIEW_STATUS,
        "source_results_review_scope": source.REVIEW_SCOPE,
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


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    value = deepcopy(dict(candidate))
    for field in ("checklist", "summary", CANDIDATE_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_exact = _source_fields(None)
    checks = [_check(f"{field}_bound", expected, candidate.get(field)) for field, expected in source_exact.items()]
    checks.extend([
        _check("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", source.source.TARGET_MODULES, [item.get("module_path") for item in candidate.get("priority_1_target_modules", [])]),
        _check("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
        _check("controlled_recapture_execution_reviewed_true", True, candidate.get("source_controlled_recapture_execution_performed")),
        _check("durable_receipt_finalized_reviewed_true", True, candidate.get("source_durable_receipt_finalized")),
        _check("durable_receipt_retained_reviewed_true", True, candidate.get("source_durable_receipt_retained")),
        _check("exit_code_1_bound_as_diagnostic_only", 1, candidate.get("source_exit_code")),
        _check("stdout_hash_bound", "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a", candidate.get("source_stdout_sha256")),
        _check("stderr_hash_bound", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", candidate.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, candidate.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, candidate.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, candidate.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, candidate.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, candidate.get("source_redaction_checked")),
        _check("recommended_package_defined", RECOMMENDED_PACKAGE, candidate.get("recommended_remediation_or_method_package")),
        _check("recommended_package_not_selected", False, candidate.get("recommended_package", {}).get("selected")),
        _check("packages_present_12", 12, len(candidate.get("proposed_remediation_or_method_packages", []))),
        _check("blocked_packages_present_6", 6, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_remediation_or_method_packages", []))),
        _check("future_method_requirements_defined", FUTURE_METHOD_REQUIREMENTS, candidate.get("future_method_requirements")),
        _check("future_method_plan_defined", FUTURE_METHOD_PLAN, candidate.get("future_method_plan", {}).get("steps")),
        _check("planned_outputs_defined", PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        _check("non_goals_defined", NON_GOALS, candidate.get("non_goals")),
        _check("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
    ])
    checks.extend(_check(f"{field}_true", True, candidate.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, candidate.get(field)) for field in FALSE_FIELDS)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
    ])
    return checks


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checklist = candidate.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: candidate.get(field) for field in TRUE_FIELDS[:10]},
        **{field: candidate.get(field) for field in (
            "recommended_remediation_or_method_package", "remediation_or_method_package_selected",
            "remediation_or_method_package_approved", "remediation_or_method_execution_performed",
            "method_analysis_executed", "remediation_execution_performed", "diagnostic_receipt_parsed_in_candidate",
            "diagnostic_output_analyzed_in_candidate", "failure_family_classification_performed",
            "targeted_pytest_performed_in_candidate", "retry_rerun_performed", "full_pytest_performed",
            "ready_for_remediation_or_method_approval", "ready_for_remediation_or_method_execution",
            "ready_for_retry_candidate", "ready_for_main_merge_approval", "new_retry_candidate_created",
            "new_retry_executed", "integration_execution_successful", "source_exit_code",
            "source_stdout_byte_count", "source_stderr_byte_count", "failed_or_errored_nodeids_count",
            "module_summary_module_count", "priority_1_total_nodeids", "top_10_count_sum",
        )},
        "priority_1_top_module_count": 5,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(
    *, source_results_review: dict | None = None,
) -> dict:
    """Build the offline candidate without reading diagnostic evidence or running a source builder."""

    source_fields = _source_fields(source_results_review)
    recommended = deepcopy(PROPOSED_PACKAGES[0])
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True,
        "operator_review_required": True, **source_fields,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
            "working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
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
        "source_durable_receipt_retained": True, "source_controlled_recapture_command_is_retry": False,
        "source_controlled_recapture_command_is_full_pytest": False,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_diagnostic_results_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.REVIEW_STATUS,
            "scope": source.REVIEW_SCOPE, "commit": SOURCE_RESULTS_REVIEW_COMMIT,
            "results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "recommendation": source.RECOMMENDED_ACTION,
        },
        "source_controlled_recapture_execution_summary": {
            "commit": SOURCE_EXECUTION_COMMIT, "execution_digest": SOURCE_EXECUTION_DIGEST,
            "payload_digest": SOURCE_PAYLOAD_DIGEST, "exit_code": 1,
            "diagnostic_evidence_only": True, "retry_evidence": False,
        },
        "source_durable_receipt_summary": {
            "path": SOURCE_DURABLE_RECEIPT_PATH, "receipt_digest": SOURCE_RECEIPT_DIGEST,
            "scaffold_prewritten": True, "finalized": True, "retained": True,
            "parsed_in_candidate": False,
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
        "diagnostic_capture_evidence_summary": {
            "command_identity_reviewed": True, "priority_1_modules_reviewed": True,
            "exit_code": 1, "exit_code_is_diagnostic_only": True,
            "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
            "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "stdout_byte_count": 1231380, "stderr_byte_count": 0,
            "bounded_output": True, "redaction_checked": True,
            "receipt_parsed": False, "diagnostic_output_analyzed": False,
        },
        "candidate_philosophy": {
            "remediation_or_method_candidate_after_diagnostic_capture_philosophy": CANDIDATE_PHILOSOPHY_TEXT,
            "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        },
        "proposed_remediation_or_method_packages": deepcopy(PROPOSED_PACKAGES),
        "recommended_remediation_or_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommended_package": {**recommended, "reason": RECOMMENDATION_REASON},
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "future_method_requirements": deepcopy(FUTURE_METHOD_REQUIREMENTS),
        "future_method_plan": {"status": "PLANNED_NOT_EXECUTED", "steps": list(FUTURE_METHOD_PLAN)},
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "non_goals": list(NON_GOALS),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    candidate.update({field: True for field in TRUE_FIELDS})
    candidate.update({field: False for field in FALSE_FIELDS})
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    candidate[CANDIDATE_DIGEST_KEY] = _candidate_digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(
    candidate: dict,
) -> dict:
    """Validate the complete candidate and reject changed evidence or opened authority."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError
    if not isinstance(candidate, dict):
        raise error("candidate must be an object")
    exact = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True,
        "operator_review_required": True, **_source_fields(None),
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "priority_1_target_modules": PRIORITY_1_TARGET_MODULES,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
        "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_controlled_recapture_execution_performed": True,
        "source_diagnostic_command_executed": True, "source_diagnostic_output_captured": True,
        "source_diagnostic_method_executed": True, "source_targeted_pytest_performed": True,
        "source_durable_receipt_scaffold_prewritten": True, "source_durable_receipt_finalized": True,
        "source_durable_receipt_retained": True, "source_controlled_recapture_command_is_retry": False,
        "source_controlled_recapture_command_is_full_pytest": False,
        "source_diagnostic_results_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.REVIEW_STATUS,
            "scope": source.REVIEW_SCOPE, "commit": SOURCE_RESULTS_REVIEW_COMMIT,
            "results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "recommendation": source.RECOMMENDED_ACTION,
        },
        "source_controlled_recapture_execution_summary": {
            "commit": SOURCE_EXECUTION_COMMIT, "execution_digest": SOURCE_EXECUTION_DIGEST,
            "payload_digest": SOURCE_PAYLOAD_DIGEST, "exit_code": 1,
            "diagnostic_evidence_only": True, "retry_evidence": False,
        },
        "source_durable_receipt_summary": {
            "path": SOURCE_DURABLE_RECEIPT_PATH, "receipt_digest": SOURCE_RECEIPT_DIGEST,
            "scaffold_prewritten": True, "finalized": True, "retained": True,
            "parsed_in_candidate": False,
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
        "diagnostic_capture_evidence_summary": {
            "command_identity_reviewed": True, "priority_1_modules_reviewed": True,
            "exit_code": 1, "exit_code_is_diagnostic_only": True,
            "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
            "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "stdout_byte_count": 1231380, "stderr_byte_count": 0,
            "bounded_output": True, "redaction_checked": True,
            "receipt_parsed": False, "diagnostic_output_analyzed": False,
        },
        "candidate_philosophy": {
            "remediation_or_method_candidate_after_diagnostic_capture_philosophy": CANDIDATE_PHILOSOPHY_TEXT,
            "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        },
        "proposed_remediation_or_method_packages": PROPOSED_PACKAGES,
        "recommended_remediation_or_method_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_package": {**deepcopy(PROPOSED_PACKAGES[0]), "reason": RECOMMENDATION_REASON},
        "future_method_requirements": FUTURE_METHOD_REQUIREMENTS,
        "future_method_plan": {"status": "PLANNED_NOT_EXECUTED", "steps": FUTURE_METHOD_PLAN},
        "planned_outputs": PLANNED_OUTPUTS, "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected in exact.items():
        if candidate.get(field) != expected:
            raise error(f"{field} mismatch")
    if candidate.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise error("retry failure counts mismatch")
    if any(candidate.get(field) is not True for field in TRUE_FIELDS):
        raise error("required candidate fact missing")
    if any(candidate.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed boundary opened")
    recommended = candidate.get("recommended_package", {})
    if recommended.get("package_id") != RECOMMENDED_PACKAGE or recommended.get("status") != RECOMMENDATION_STATUS:
        raise error("recommended package mismatch")
    if any(recommended.get(field) is not False for field in ("selected", "approved", "executed")):
        raise error("recommended package authority opened")
    packages = candidate.get("proposed_remediation_or_method_packages", [])
    if len(packages) != 12 or sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in packages) != 6:
        raise error("package inventory mismatch")
    if any(item.get(field) is not False for item in packages for field in ("selected", "approved", "executed")):
        raise error("package authority opened")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if candidate.get("summary") != _summary(candidate):
        raise error("summary mismatch")
    digest = candidate.get(CANDIDATE_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise error("candidate digest missing")
    if digest != _candidate_digest(candidate):
        raise error("candidate digest mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE, "candidate_digest": digest,
        **{field: candidate["summary"][field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(
    output_dir: str | Path, *, source_results_review: dict | None = None,
) -> dict:
    """Write deterministic candidate JSON outside protected runtime directories."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError(
            "protected output directory"
        )
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(
        source_results_review=source_results_review
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError(
            "output exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS,
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY], "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_markdown_v1(
    candidate: dict,
) -> str:
    """Render a bounded candidate summary after validation."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)
    sections = [
        ("Source Diagnostic Results Review", [SOURCE_RESULTS_REVIEW_COMMIT, SOURCE_RESULTS_REVIEW_DIGEST]),
        ("Source Controlled Recapture Execution", [SOURCE_EXECUTION_COMMIT, SOURCE_EXECUTION_DIGEST]),
        ("Source Durable Receipt", [SOURCE_DURABLE_RECEIPT_PATH, SOURCE_RECEIPT_DIGEST]),
        ("Source Receipt Loss History", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"], SOURCE_BINDINGS["source_primary_failure_class"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_planning_execution_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Candidate Scope", [CANDIDATE_SCOPE]),
        ("Priority 1 Target Modules", source.source.TARGET_MODULES),
        ("Diagnostic Capture Evidence Summary", [str(candidate["diagnostic_capture_evidence_summary"])]),
        ("Candidate Philosophy", [CANDIDATE_PHILOSOPHY_TEXT, CANDIDATE_BOUNDARY, CANDIDATE_GOAL]),
        ("Proposed Remediation or Method Packages", [f"{item['package_id']}: {item['status']}" for item in PROPOSED_PACKAGES]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, RECOMMENDATION_STATUS, RECOMMENDATION_REASON]),
        ("Future Method Requirements", list(FUTURE_METHOD_REQUIREMENTS)),
        ("Future Method Plan", FUTURE_METHOD_PLAN),
        ("Planned Outputs", [f"{key}: {value}" for key, value in PLANNED_OUTPUTS.items()]),
        ("Non-Goals", NON_GOALS), ("Next Chain", NEXT_CHAIN), ("Next Gates", NEXT_GATES),
        ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["Candidate-only; no package selection, approval, execution, retry, main, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["No receipt parsing, output analysis, command, pytest, cache, log, environment, provider, data, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Diagnostic Capture v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE

__all__ = [
    "ARTIFACT_KIND", "CANDIDATE_STATUS", "CANDIDATE_SCOPE", "SCHEMA_VERSION", "CANDIDATE_DIGEST_KEY",
    "SOURCE_RESULTS_REVIEW_COMMIT", "SOURCE_RESULTS_REVIEW_DIGEST", "SOURCE_PAYLOAD_REVIEW_DIGEST",
    "SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST", "SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST",
    "SOURCE_EXECUTION_COMMIT", "SOURCE_EXECUTION_DIGEST", "SOURCE_PAYLOAD_DIGEST", "SOURCE_RECEIPT_DIGEST",
    "SOURCE_DIGEST_MANIFEST_DIGEST", "SOURCE_DURABLE_RECEIPT_PATH", "SOURCE_BINDINGS",
    "RECOMMENDED_PACKAGE", "RECOMMENDATION_STATUS", "RECOMMENDED_NEXT_TASK", "PROPOSED_PACKAGES",
    "FUTURE_METHOD_REQUIREMENTS", "FUTURE_METHOD_PLAN", "PLANNED_OUTPUTS", "NON_GOALS", "NEXT_CHAIN",
    "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_DIAGNOSTIC_CAPTURE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_markdown_v1",
]
