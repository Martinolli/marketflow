"""Execute bounded failure-family classification over a committed diagnostic receipt."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_service
    as approval_source,
)

ARTIFACT_KIND_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_DIAGNOSTIC_CAPTURE_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_DIAGNOSTIC_CAPTURE_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1"
EXECUTION_STATUS_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_DIAGNOSTIC_CAPTURE_FAILURE_FAMILY_CLASSIFICATION_READY"
EXECUTION_STATUS_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_DIAGNOSTIC_CAPTURE_DURABLE_RECEIPT_OR_BOUNDED_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_ONLY_METHOD_ANALYSIS_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = approval_source.SELECTED_PACKAGE
SOURCE_APPROVAL_COMMIT = "486024f32efb50d9620ba26b950892295c5a660e"
SOURCE_APPROVAL_DIGEST = "7c4096364f1d1d5feb048bdbb7987c46e082947d75664f15976460590745b6e6"
DEFAULT_DURABLE_RECEIPT_PATH = Path(__file__).resolve().parents[2] / approval_source.source.SOURCE_DURABLE_RECEIPT_PATH
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_FAILURE_DIAGNOSIS_V1"
EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_digest"
CLASSIFICATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_failure_family_classification_digest"
BOUNDED_ANALYSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_bounded_excerpt_analysis_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_blocked_manifest_digest"
RECEIPT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_receipt_digest"
RECEIPT_PAYLOAD_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_payload_digest"
RECEIPT_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_digest_manifest_digest"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

FAMILY_DEFINITIONS = [
    ("assertion_or_value_mismatch", "Assertion or value mismatch", [r"\bassert\b", r"AssertionError", r"expected.{0,80}actual", r"\bmismatch\b"]),
    ("missing_or_unexpected_field", "Missing or unexpected field", [r"KeyError", r"missing (?:field|key)", r"unexpected (?:field|key|argument)", r"required (?:field|key)"]),
    ("digest_or_hash_mismatch", "Digest or hash mismatch", [r"(?:digest|sha256|hash).{0,100}(?:mismatch|changed|expected|actual)"]),
    ("artifact_status_scope_or_kind_mismatch", "Artifact status, scope, or kind mismatch", [r"(?:artifact.kind|status|scope).{0,100}(?:mismatch|wrong|expected|actual)"]),
    ("boundary_boolean_flag_mismatch", "Boundary boolean flag mismatch", [r"(?:true|false).{0,100}(?:expected|actual|mismatch)", r"(?:boundary|flag).{0,100}(?:mismatch|wrong)"]),
    ("fixture_or_test_isolation_issue", "Fixture or test isolation issue", [r"\bfixture\b", r"setup of test", r"isolation"]),
    ("import_or_collection_error", "Import or collection error", [r"ImportError", r"ModuleNotFoundError", r"collection error", r"error collecting"]),
    ("path_cwd_or_worktree_assumption", "Path, cwd, or worktree assumption", [r"\b(?:path|cwd|worktree)\b.{0,100}(?:missing|wrong|mismatch|not found)", r"FileNotFoundError"]),
    ("evidence_root_or_file_availability", "Evidence root or file availability", [r"(?:evidence root|source file|receipt file|artifact file).{0,100}(?:unavailable|missing|not found)"]),
    ("serialization_or_determinism_issue", "Serialization or determinism issue", [r"serializ", r"determin", r"JSONDecodeError"]),
    ("approval_attestation_or_confirmation_mismatch", "Approval attestation or confirmation mismatch", [r"(?:approval|attestation|confirmation).{0,100}(?:mismatch|missing|wrong)"]),
    ("runtime_exception_or_name_error", "Runtime exception or name error", [r"NameError", r"RuntimeError", r"UnboundLocalError"]),
]

SUCCESS_OUTPUT_IDS = [
    "remediation_or_method_execution_after_diagnostic_capture_manifest", "source_approval_binding_report",
    "source_diagnostic_results_review_binding_report", "durable_receipt_integrity_report",
    "bounded_excerpt_integrity_report", "observable_failure_family_classification_report",
    "family_confidence_and_limitation_report", "output_bounding_limitation_report",
    "unsupported_claims_boundary_report", "future_remediation_method_direction_report",
    "method_results_review_enablement_report", "retry_gate_preservation_report",
    "main_merge_gate_preservation_report", "digest_manifest",
]
SUCCESS_OUTPUTS = [{"output_id": item, "status": "GENERATED_METHOD_ANALYSIS_ONLY"} for item in SUCCESS_OUTPUT_IDS]
SUCCESS_NEXT_CHAIN = [
    "Remediation or Method Results Review After Diagnostic Capture v1.",
    "Remediation Plan or Execution Candidate v1, only if supported by method results review.",
    "Remediation Plan or Execution Candidate Operator Review v1, if needed.",
    "Remediation Plan or Execution Approval v1, if selected.", "Remediation Plan or Execution v1, if approved.",
    "Remediation Results Review v1.", "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Remediation or Method Execution After Diagnostic Capture Failure Diagnosis v1.",
    "Alternate method execution or source candidate, if needed.",
    "No remediation execution, retry, or main merge.",
]
NEXT_GATES = [
    "method_results_review_after_diagnostic_capture", "remediation_plan_or_execution_candidate_if_supported",
    "remediation_plan_or_execution_operator_review_if_needed", "remediation_plan_or_execution_approval_if_selected",
    "remediation_plan_or_execution_if_approved", "remediation_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
    "method_execution_after_diagnostic_capture_failure_diagnosis", "alternate_method_execution_or_source_candidate_if_needed",
    "remediation_execution_blocked_until_method_results_review_passes",
    "new_retry_blocked_until_remediation_or_method_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "method_execution_after_diagnostic_capture_uses_approved_package_only",
    "method_execution_after_diagnostic_capture_reads_committed_durable_receipt_only",
    "method_execution_after_diagnostic_capture_uses_bounded_excerpts_only",
    "method_execution_after_diagnostic_capture_preserves_output_bounding_limitations",
    "method_execution_after_diagnostic_capture_does_not_reconstruct_full_stdout",
    "method_execution_after_diagnostic_capture_does_not_reconstruct_full_stderr",
    "method_execution_after_diagnostic_capture_does_not_rerun_controlled_recapture",
    "method_execution_after_diagnostic_capture_does_not_run_diagnostic_command",
    "method_execution_after_diagnostic_capture_does_not_run_targeted_pytest",
    "method_execution_after_diagnostic_capture_does_not_run_full_pytest",
    "method_execution_after_diagnostic_capture_does_not_rerun_retry",
    "method_execution_after_diagnostic_capture_does_not_read_pytest_cache",
    "method_execution_after_diagnostic_capture_does_not_modify_pytest_cache",
    "method_execution_after_diagnostic_capture_does_not_parse_terminal_logs",
    "method_execution_after_diagnostic_capture_does_not_parse_operator_logs",
    "method_execution_after_diagnostic_capture_does_not_inspect_env",
    "method_execution_after_diagnostic_capture_does_not_reconstruct_prior_lost_values",
    "method_execution_after_diagnostic_capture_does_not_execute_code_remediation",
    "method_execution_after_diagnostic_capture_does_not_modify_production_code",
    "method_execution_after_diagnostic_capture_does_not_modify_existing_tests_except_new_governance_tests",
    "method_execution_after_diagnostic_capture_does_not_classify_full_retry_failures",
    "method_execution_after_diagnostic_capture_does_not_classify_full_retry_errors",
    "method_execution_after_diagnostic_capture_does_not_claim_failure_error_separation",
    "method_execution_after_diagnostic_capture_does_not_identify_authoritative_first_failure",
    "method_execution_after_diagnostic_capture_does_not_identify_authoritative_first_error",
    "method_execution_after_diagnostic_capture_does_not_claim_traceback_root_cause",
    "method_execution_after_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "method_execution_after_diagnostic_capture_does_not_create_remediation_execution",
    "method_execution_after_diagnostic_capture_does_not_create_remediation_results_review",
    "method_execution_after_diagnostic_capture_does_not_create_new_retry_candidate",
    "method_execution_after_diagnostic_capture_does_not_create_retry_results_review",
    "method_execution_after_diagnostic_capture_does_not_create_integration_results_review",
    "method_execution_after_diagnostic_capture_does_not_mark_integration_successful",
    "method_execution_after_diagnostic_capture_does_not_generate_successful_integration_digest",
    "method_execution_after_diagnostic_capture_does_not_treat_diagnostic_capture_as_retry",
    "method_execution_after_diagnostic_capture_does_not_treat_exit_code_as_retry_result",
    "method_execution_after_diagnostic_capture_does_not_push_integration_branch",
    "method_execution_after_diagnostic_capture_does_not_push_main",
    "method_execution_after_diagnostic_capture_does_not_delete_integration_branch",
    "method_execution_after_diagnostic_capture_does_not_delete_worktree",
    "method_execution_after_diagnostic_capture_does_not_force_push",
    "method_execution_after_diagnostic_capture_does_not_prune_remotes",
    "method_execution_after_diagnostic_capture_does_not_modify_tags",
    "method_execution_after_diagnostic_capture_does_not_modify_staged_evidence",
    "method_execution_after_diagnostic_capture_does_not_regenerate_evidence",
    "method_execution_after_diagnostic_capture_does_not_call_providers",
    "method_execution_after_diagnostic_capture_does_not_acquire_market_data",
    "method_execution_after_diagnostic_capture_does_not_regenerate_dataset",
    "method_execution_after_diagnostic_capture_does_not_recompute_metrics",
    "method_execution_after_diagnostic_capture_does_not_train_models",
    "method_execution_after_diagnostic_capture_does_not_score_strategy",
    "method_execution_after_diagnostic_capture_does_not_generate_recommendations",
    "method_execution_after_diagnostic_capture_does_not_accept_predictive_usefulness",
    "method_execution_after_diagnostic_capture_does_not_accept_profitability",
    "method_execution_after_diagnostic_capture_does_not_authorize_runtime",
    "method_execution_after_diagnostic_capture_does_not_authorize_broker_execution",
    "observable_failure_family_classification_is_method_planning_only",
    "failure_family_classification_is_not_root_cause", "failure_family_classification_is_not_direct_remediation",
    "failure_family_classification_is_not_retry_success", "diagnostic_capture_results_review_remains_source_evidence",
    "durable_receipt_is_diagnostic_evidence_only", "controlled_recapture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause", "module_concentration_is_not_failure_error_separation",
    "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_remediation_or_method_approval_remains_source_evidence",
    "previous_remediation_or_method_operator_review_remains_source_evidence",
    "previous_remediation_or_method_candidate_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_results_review_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_execution_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_approval_remains_source_evidence",
    "previous_failure_diagnosis_remains_source_evidence", "previous_targeted_diagnostic_approval_remains_source_evidence",
    "previous_planning_results_review_remains_valid", "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_results_review_required_after_method_execution",
    "separate_remediation_approval_required_before_remediation_execution",
    "separate_retry_approval_required_before_new_retry", "main_merge_requires_passing_new_retry_results_review",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

SUCCESS_TRUE_FIELDS = [
    "remediation_or_method_execution_after_diagnostic_capture_created", "remediation_or_method_execution_performed",
    "method_analysis_executed", "approved_method_package_executed", "diagnostic_receipt_parsed_in_execution",
    "diagnostic_output_analyzed_in_execution", "bounded_diagnostic_excerpt_analyzed",
    "failure_family_classification_performed", "observable_failure_families_generated",
    "source_durable_receipt_file_read", "source_durable_receipt_path_bound", "source_durable_receipt_digest_bound",
    "ready_for_method_results_review_after_diagnostic_capture",
]
COMMON_FALSE_FIELDS = [
    "remediation_execution_performed", "code_remediation_executed", "evidence_remediation_executed",
    "direct_code_remediation_recommended", "controlled_recapture_rerun_performed",
    "diagnostic_command_rerun_performed", "targeted_pytest_performed_in_execution", "full_pytest_performed",
    "retry_rerun_performed", "cache_read_in_execution", "cache_modified_in_execution", "pytest_cache_committed",
    "marketflow_outputs_committed", "terminal_logs_parsed", "operator_logs_parsed", "env_inspection_performed",
    "prior_lost_values_reconstructed", "prior_lost_values_inferred", "full_stdout_reconstructed",
    "full_stderr_reconstructed", "failure_modules_classified", "error_modules_classified",
    "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
    "first_order_claim_made", "traceback_root_cause_claimed", "root_cause_claimed", "retry_success_claimed",
    "main_merge_readiness_claimed", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "ready_for_remediation_execution",
    "ready_for_retry_candidate", "ready_for_main_merge_approval", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "evidence_regenerated", "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]

SOURCE_CHECK_ALIASES = {
    "source_approval_digest_bound": "source_remediation_or_method_approval_after_diagnostic_capture_digest",
    "source_operator_review_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
    "source_candidate_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
    "source_results_review_digest_bound": "source_receipt_recovery_or_recapture_results_review_digest",
    "source_payload_review_digest_bound": "source_receipt_recovery_or_recapture_payload_review_digest",
    "source_durable_receipt_review_digest_bound": "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
    "source_results_review_manifest_digest_bound": "source_receipt_recovery_or_recapture_results_review_manifest_digest",
    "source_execution_commit_bound": "source_receipt_recovery_or_recapture_execution_commit",
    "source_execution_digest_bound": "source_receipt_recovery_or_recapture_execution_digest",
    "source_payload_digest_bound": "source_receipt_recovery_or_recapture_payload_digest",
    "source_durable_receipt_digest_bound": "source_receipt_recovery_or_recapture_receipt_digest",
    "source_digest_manifest_digest_bound": "source_receipt_recovery_or_recapture_digest_manifest_digest",
    "source_failure_diagnosis_digest_bound": "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
    "source_prior_execution_digest_bound": "source_targeted_diagnostic_output_capture_execution_digest",
    "source_blocked_manifest_digest_bound": "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest",
    "source_blocked_reason_bound": "source_targeted_diagnostic_output_capture_execution_blocked_reason",
    "source_targeted_diagnostic_approval_digest_bound": "source_targeted_diagnostic_output_capture_approval_digest",
    "source_targeted_diagnostic_candidate_operator_review_digest_bound": "source_targeted_diagnostic_output_capture_candidate_operator_review_digest",
    "source_targeted_diagnostic_candidate_digest_bound": "source_targeted_diagnostic_output_capture_candidate_digest",
}


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError(ValueError):
    pass


def _source_fields(source_approval: dict | None = None) -> dict[str, Any]:
    if source_approval is not None:
        approval_source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(deepcopy(source_approval))
        if source_approval.get(approval_source.APPROVAL_DIGEST_KEY) != SOURCE_APPROVAL_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("source approval digest mismatch")
        if source_approval.get("ready_for_remediation_or_method_execution_after_diagnostic_capture") is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("source approval does not authorize execution")
    inherited = approval_source._source_fields()
    return {
        "source_approval_artifact_kind": approval_source.ARTIFACT_KIND,
        "source_approval_status": approval_source.APPROVAL_STATUS, "source_approval_scope": approval_source.APPROVAL_SCOPE,
        "source_approval_commit": SOURCE_APPROVAL_COMMIT,
        "source_remediation_or_method_approval_after_diagnostic_capture_digest": SOURCE_APPROVAL_DIGEST,
        **inherited,
        "source_planning_results_review_digest": inherited["source_results_review_digest"],
    }


def _receipt_digest(receipt: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(receipt))
    for field in (RECEIPT_DIGEST_KEY, RECEIPT_PAYLOAD_DIGEST_KEY, RECEIPT_MANIFEST_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _redact(value: str) -> str:
    text = re.sub(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", value)
    return re.sub(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", text)


def _classify(stdout: str, stderr: str, max_snippets: int, max_chars: int) -> list[dict[str, Any]]:
    lines = [("bounded_stdout_excerpt", line) for line in stdout.splitlines() if line.strip()]
    lines += [("bounded_stderr_excerpt", line) for line in stderr.splitlines() if line.strip()]
    modules = [item["module_path"] for item in approval_source.source.PRIORITY_1_TARGET_MODULES]
    families = []
    for family_id, label, patterns in FAMILY_DEFINITIONS:
        matches = [(origin, line) for origin, line in lines if any(re.search(pattern, line, re.I) for pattern in patterns)]
        if not matches:
            continue
        snippets = []
        for _, line in matches:
            snippet = _redact(line.strip())[:max_chars]
            if snippet not in snippets:
                snippets.append(snippet)
            if len(snippets) >= max_snippets:
                break
        visible = [path for path in modules if any(path in line or Path(path).name in line for _, line in matches)]
        count = len(matches)
        confidence = "HIGH" if count >= 5 else "MEDIUM" if count >= 2 else "LOW"
        families.append({
            "family_id": family_id, "family_label": label,
            "classification_source": "COMMITTED_DURABLE_RECEIPT_BOUNDED_EXCERPTS_ONLY",
            "classification_basis": "Deterministic rule matches in redaction-checked bounded diagnostic text.",
            "observable_evidence_count": count, "representative_redacted_snippets": snippets,
            "priority_1_modules_visible": visible, "confidence": confidence,
            "limitations": "Observable bounded-text pattern only; not a full retry classification and not a root-cause conclusion.",
            "root_cause_claimed": False, "direct_remediation_recommended": False, "retry_success_claimed": False,
        })
    if not families:
        families.append({
            "family_id": "insufficient_visible_pattern_detail", "family_label": "Insufficient visible pattern detail",
            "classification_source": "COMMITTED_DURABLE_RECEIPT_BOUNDED_EXCERPTS_ONLY",
            "classification_basis": "A bounded excerpt exists but no supported specific rule matched.",
            "observable_evidence_count": 1, "representative_redacted_snippets": [],
            "priority_1_modules_visible": [], "confidence": "LOW",
            "limitations": "The committed bounded excerpt exists but does not contain enough visible pattern detail for specific family classification. Additional separately governed diagnostic capture may be required after results review.",
            "root_cause_claimed": False, "direct_remediation_recommended": False, "retry_success_claimed": False,
        })
    return sorted(families, key=lambda item: (-item["observable_evidence_count"], item["family_id"]))


def _common(run_timestamp_utc: str, source_approval: dict | None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_remediation_or_method_package": SELECTED_PACKAGE, "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True, "method_execution_only": True, "remediation_execution_only": False,
        **_source_fields(source_approval), "retry_execution_commit": approval_source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
                                  "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": deepcopy(approval_source.source.PRIORITY_1_TARGET_MODULES),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404, "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0, "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"],
        "source_stderr_sha256": approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"],
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_exit_code_is_diagnostic_only": True,
        "remediation_or_method_approval_after_diagnostic_capture_created": True,
        "remediation_or_method_package_selected": True,
        "remediation_or_method_package_approved": True,
        "remediation_or_method_package_authorized": True,
        "ready_for_remediation_or_method_execution_after_diagnostic_capture": True,
        **{field: False for field in COMMON_FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }


def _timestamp(value: str | None) -> str:
    result = value or "1970-01-01T00:00:00Z"
    try:
        parsed = datetime.fromisoformat(result.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("run_timestamp_utc invalid") from exc
    if not result.endswith("Z") or parsed.utcoffset() is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("run_timestamp_utc invalid")
    return result


def _blocked(common: dict[str, Any], reason: str, available: list[str], missing: list[str]) -> dict[str, Any]:
    execution = {**common, "artifact_kind": ARTIFACT_KIND_BLOCKED, "execution_status": EXECUTION_STATUS_BLOCKED,
                 "governance_only": True, "blocked_reason": reason, "available_data": available, "missing_data": missing,
                 "recommended_next_task": BLOCKED_NEXT_TASK, "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
                 "recommendation": {"recommended_next_task": BLOCKED_NEXT_TASK,
                                    "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED"},
                 "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(NEXT_GATES), "outputs": [],
                 **{field: False for field in SUCCESS_TRUE_FIELDS}}
    execution["remediation_or_method_execution_after_diagnostic_capture_created"] = True
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest({"blocked_reason": reason, "available_data": available,
                                                               "missing_data": missing, "source_approval": SOURCE_APPROVAL_DIGEST,
                                                               "run_timestamp_utc": common["run_timestamp_utc"]})
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    return execution


def _success(common: dict[str, Any], receipt: dict[str, Any], raw: bytes, path: Path,
             stdout: str, stderr: str, max_snippets: int, max_chars: int) -> dict[str, Any]:
    families = _classify(stdout, stderr, max_snippets, max_chars)
    confidence_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    highest = max(confidence_rank[item["confidence"]] for item in families)
    summary = {
        "total_families_detected": len(families),
        "total_observable_evidence_items": sum(item["observable_evidence_count"] for item in families),
        "highest_confidence_family_ids": [item["family_id"] for item in families if confidence_rank[item["confidence"]] == highest],
        "families_requiring_results_review": [item["family_id"] for item in families],
        "additional_diagnostic_capture_may_be_needed": all(item["family_id"] == "insufficient_visible_pattern_detail" for item in families),
        "direct_remediation_ready": False, "retry_ready": False, "main_merge_ready": False,
    }
    stdout_used, stderr_used = bool(stdout.strip()), bool(stderr.strip())
    execution = {
        **common, "artifact_kind": ARTIFACT_KIND_SUCCESS, "execution_status": EXECUTION_STATUS_SUCCESS,
        "governance_only": False, "blocked_reason": None,
        **{field: True for field in SUCCESS_TRUE_FIELDS},
        "source_bounded_stdout_excerpt_used": stdout_used, "source_bounded_stderr_excerpt_used": stderr_used,
        "method_input_source_summary": {"durable_receipt_path": approval_source.source.SOURCE_DURABLE_RECEIPT_PATH,
                                        "stdout_excerpt_used": stdout_used, "stderr_excerpt_used": stderr_used,
                                        "full_streams_available_or_used": False},
        "durable_receipt_integrity_summary": {"path": str(path), "file_sha256": hashlib.sha256(raw).hexdigest(),
                                               "embedded_receipt_digest": receipt[RECEIPT_DIGEST_KEY],
                                               "receipt_digest_verified": True, "receipt_finalized": True},
        "bounded_excerpt_integrity_summary": {"stdout_chars": len(stdout), "stderr_chars": len(stderr),
                                               "stdout_excerpt_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
                                               "stderr_excerpt_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
                                               "source_stdout_is_truncated": True, "source_stderr_is_truncated": False,
                                               "redaction_checked": True},
        "failure_family_classification_method": {"method": "DETERMINISTIC_CONSERVATIVE_RULE_CLASSIFIER_V1",
                                                  "ordering": ["descending evidence count", "ascending family_id"],
                                                  "max_snippets_per_family": max_snippets, "max_snippet_chars": max_chars,
                                                  "input_scope": "BOUNDED_EXCERPTS_ONLY"},
        "observable_failure_families": families, "failure_family_classification_summary": summary,
        "family_confidence_summary": {item["family_id"]: item["confidence"] for item in families},
        "method_limitations": ["Only committed bounded excerpts were analyzed.",
                               "The output is not a full retry classification and makes no root-cause or first-order claim.",
                               "Every family requires a separately invoked method results review."],
        "future_remediation_method_direction": {"recommended_next_task": SUCCESS_NEXT_TASK,
                                                 "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE",
                                                 "method_results_review_required": True,
                                                 "remediation_execution_requires_separate_future_approval": True,
                                                 "new_retry_requires_separate_future_candidate_approval_execution_and_review": True,
                                                 "main_merge_requires_passing_future_retry_review": True},
        "unsupported_claims_boundary": {"root_cause": False, "authoritative_first_failure": False,
                                        "authoritative_first_error": False, "full_retry_classification": False,
                                        "direct_code_remediation": False, "retry_success": False, "main_merge_readiness": False},
        "post_execution_boundary_checks": {field: False for field in COMMON_FALSE_FIELDS},
        "outputs": deepcopy(SUCCESS_OUTPUTS), "recommendation": {"recommended_next_task": SUCCESS_NEXT_TASK,
                    "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
                    "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE"},
        "recommended_next_task": SUCCESS_NEXT_TASK, "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(NEXT_GATES),
    }
    execution[CLASSIFICATION_DIGEST_KEY] = semantic_digest(families)
    execution[BOUNDED_ANALYSIS_DIGEST_KEY] = semantic_digest({"integrity": execution["bounded_excerpt_integrity_summary"],
                                                              "classification_method": execution["failure_family_classification_method"]})
    manifest = {"source_approval": SOURCE_APPROVAL_DIGEST, "source_receipt": receipt[RECEIPT_DIGEST_KEY],
                "bounded_analysis": execution[BOUNDED_ANALYSIS_DIGEST_KEY],
                "classification": execution[CLASSIFICATION_DIGEST_KEY], "outputs": semantic_digest(SUCCESS_OUTPUTS)}
    execution["digest_manifest"] = manifest
    execution[MANIFEST_DIGEST_KEY] = semantic_digest(manifest)
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    return execution


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    source_fields = _source_fields()
    checks = [_check(f"{field}_bound", value, execution.get(field)) for field, value in source_fields.items()]
    checks.extend(
        _check(check_id, source_fields[field], execution.get(field))
        for check_id, field in SOURCE_CHECK_ALIASES.items()
    )
    checks += [
        _check("selected_package_bound", SELECTED_PACKAGE, execution.get("selected_remediation_or_method_package")),
        _check("retry_execution_commit_bound", approval_source.source.RETRY_EXECUTION_COMMIT, execution.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, execution.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", approval_source.source.PRIORITY_1_TARGET_MODULES, execution.get("priority_1_target_modules")),
        _check("priority_1_total_612_bound", 612, execution.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, execution.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, execution.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, execution.get("failed_or_errored_nodeids_count")),
        _check("exit_code_1_bound_as_diagnostic_only", [1, True], [execution.get("source_exit_code"), execution.get("source_exit_code_is_diagnostic_only")]),
        _check("stdout_hash_bound", approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"], execution.get("source_stdout_sha256")),
        _check("stderr_hash_bound", approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"], execution.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, execution.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, execution.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, execution.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, execution.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, execution.get("source_redaction_checked")),
        _check("approval_authorizes_method_execution_true", True, execution.get("ready_for_remediation_or_method_execution_after_diagnostic_capture")),
        _check("remediation_execution_false", False, execution.get("remediation_execution_performed")),
        _check("code_remediation_false", False, execution.get("code_remediation_executed")),
        _check("controlled_recapture_rerun_false", False, execution.get("controlled_recapture_rerun_performed")),
        _check("targeted_pytest_in_execution_false", False, execution.get("targeted_pytest_performed_in_execution")),
        _check("retry_rerun_false", False, execution.get("retry_rerun_performed")),
        _check("cache_read_false", False, execution.get("cache_read_in_execution")),
        _check("evidence_remediation_false", False, execution.get("evidence_remediation_executed")),
        _check("diagnostic_command_rerun_false", False, execution.get("diagnostic_command_rerun_performed")),
        _check("full_pytest_false", False, execution.get("full_pytest_performed")),
        _check("cache_modified_false", False, execution.get("cache_modified_in_execution")),
        _check("env_inspection_false", False, execution.get("env_inspection_performed")),
        _check("integration_success_false", False, execution.get("integration_execution_successful")),
        _check("successful_integration_digest_false", False, execution.get("successful_integration_execution_digest_generated")),
        _check("main_push_false", False, execution.get("main_push_performed")),
        _check("origin_main_modified_false", False, execution.get("origin_main_modified_by_this_task")),
        _check("provider_requests_false", False, execution.get("provider_requests_made_in_execution")),
        _check("market_data_acquisition_false", False, execution.get("market_data_acquisition_performed_in_execution")),
        _check("dataset_generation_false", False, execution.get("dataset_generation_performed_in_execution")),
        _check("metric_recomputation_false", False, execution.get("metric_recomputation_from_raw_rows_performed")),
        _check("model_training_false", False, execution.get("model_training_performed")),
        _check("strategy_scoring_false", False, execution.get("strategy_scoring_performed")),
        _check("recommendations_false", False, execution.get("trade_recommendations_generated")),
        _check("no_tracked_marketflow_files", True, execution.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, execution.get("no_tracked_pytest_cache_files")),
        _check("risk_controls_defined", RISK_CONTROLS, execution.get("risk_controls")),
        _check("next_gates_defined", NEXT_GATES, execution.get("next_gates")),
    ]
    checks.extend(_check(f"{field}_false", False, execution.get(field)) for field in COMMON_FALSE_FIELDS)
    checks.extend([
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, execution.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, execution.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, execution.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, execution.get("broker_execution")),
    ])
    if success:
        checks.extend(_check(f"{field}_true_if_success", True, execution.get(field)) for field in SUCCESS_TRUE_FIELDS)
        families = execution.get("observable_failure_families", [])
        required = {"family_id", "family_label", "classification_source", "classification_basis",
                    "observable_evidence_count", "representative_redacted_snippets", "priority_1_modules_visible",
                    "confidence", "limitations", "root_cause_claimed", "direct_remediation_recommended", "retry_success_claimed"}
        checks += [
            _check("bounded_excerpt_available_if_success", True, execution.get("source_bounded_stdout_excerpt_used") or execution.get("source_bounded_stderr_excerpt_used")),
            _check("durable_receipt_file_read_if_success", True, execution.get("source_durable_receipt_file_read")),
            _check("method_execution_created_true_if_success", True, execution.get("remediation_or_method_execution_after_diagnostic_capture_created")),
            _check("diagnostic_receipt_parsed_true_if_success", True, execution.get("diagnostic_receipt_parsed_in_execution")),
            _check("diagnostic_output_analyzed_true_if_success", True, execution.get("diagnostic_output_analyzed_in_execution")),
            _check("observable_failure_families_generated_if_success", True, execution.get("observable_failure_families_generated")),
            _check("family_records_have_required_fields_if_success", True, bool(families) and all(required <= set(item) for item in families)),
            _check("representative_snippets_bounded_if_success", True, all(len(item["representative_redacted_snippets"]) <= 5 and all(len(s) <= 500 for s in item["representative_redacted_snippets"]) for item in families)),
            _check("family_classification_not_root_cause", True, all(item["root_cause_claimed"] is False for item in families)),
            _check("method_limitations_recorded_if_success", True, bool(execution.get("method_limitations"))),
            _check("method_results_review_ready_if_success", True, execution.get("ready_for_method_results_review_after_diagnostic_capture")),
            _check("outputs_generated_if_success", SUCCESS_OUTPUTS, execution.get("outputs")),
            _check("recommendation_defined", SUCCESS_NEXT_TASK, execution.get("recommended_next_task")),
            _check("next_chain_defined", SUCCESS_NEXT_CHAIN, execution.get("next_chain")),
        ]
    else:
        checks += [_check("blocked_reason_recorded_if_blocked", True, bool(execution.get("blocked_reason"))),
                   _check("blocked_manifest_digest_generated_if_blocked", True, isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str)),
                   _check("recommendation_defined", BLOCKED_NEXT_TASK, execution.get("recommended_next_task")),
                   _check("next_chain_defined", BLOCKED_NEXT_CHAIN, execution.get("next_chain"))]
    return checks


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checks = execution.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checks)
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    family_summary = execution.get("failure_family_classification_summary", {})
    return {"total_checks": len(checks), "passed_checks": passed, "failed_checks": len(checks) - passed,
            "blocker_count": len(checks) - passed,
            "remediation_or_method_execution_after_diagnostic_capture_created": True,
            "remediation_or_method_execution_performed": success, "method_analysis_executed": success,
            "approved_method_package_executed": success, "selected_remediation_or_method_package": SELECTED_PACKAGE,
            "diagnostic_receipt_parsed_in_execution": success, "diagnostic_output_analyzed_in_execution": success,
            "bounded_diagnostic_excerpt_analyzed": success, "failure_family_classification_performed": success,
            "observable_failure_families_generated": success,
            "observable_failure_family_count": family_summary.get("total_families_detected", 0),
            "total_observable_evidence_items": family_summary.get("total_observable_evidence_items", 0),
            "highest_confidence_family_ids": family_summary.get("highest_confidence_family_ids", []),
            "additional_diagnostic_capture_may_be_needed": family_summary.get("additional_diagnostic_capture_may_be_needed"),
            "remediation_execution_performed": False, "code_remediation_executed": False,
            "direct_code_remediation_recommended": False,
            "targeted_pytest_performed_in_execution": False, "retry_rerun_performed": False,
            "full_pytest_performed": False, "cache_read_in_execution": False,
            "blocked_reason": execution.get("blocked_reason"), "ready_for_method_results_review_after_diagnostic_capture": success,
            "ready_for_remediation_execution": False, "ready_for_retry_candidate": False,
            "ready_for_main_merge_approval": False, "new_retry_candidate_created": False,
            "new_retry_executed": False, "integration_execution_successful": False,
            "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
            "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
            "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
            "predictive_usefulness_accepted": False, "profitability_accepted": False,
            "runtime_authorized": False, "broker_execution_authorized": False}


def execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
    *, source_approval: dict | None = None, durable_receipt_path: str | Path | None = None,
    run_timestamp_utc: str | None = None, max_snippets_per_family: int = 5, max_snippet_chars: int = 500,
) -> dict:
    """Read one committed-style receipt and classify only its bounded excerpts."""

    timestamp = _timestamp(run_timestamp_utc)
    try:
        common = _common(timestamp, source_approval)
    except (
        MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError,
        approval_source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError,
        KeyError,
        TypeError,
    ) as exc:
        common = _common(timestamp, None)
        execution = _blocked(common, f"SOURCE_APPROVAL_BOUNDARY_FAILURE: {type(exc).__name__}",
                             ["source approval digest"], ["valid source approval authorizing method execution"])
        validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(execution)
        return execution
    path = Path(durable_receipt_path) if durable_receipt_path is not None else DEFAULT_DURABLE_RECEIPT_PATH
    available = ["source approval digest", "source results review digest", "source execution digest", str(path)]
    if any(part.lower() in {".pytest_cache", ".env"} for part in path.parts):
        execution = _blocked(common, "PROTECTED_OR_UNAUTHORIZED_RECEIPT_PATH", available, ["authorized durable receipt path"])
    elif not path.is_file():
        execution = _blocked(common, "DURABLE_RECEIPT_FILE_UNAVAILABLE", available, ["committed durable receipt"])
    else:
        try:
            raw = path.read_bytes()
            receipt = json.loads(raw.decode("utf-8"))
            if not isinstance(receipt, dict):
                raise ValueError("receipt is not an object")
            result = receipt.get("controlled_recapture_execution_result", {})
            expected = {
                RECEIPT_DIGEST_KEY: approval_source.source.SOURCE_RECEIPT_DIGEST,
                "receipt_finalized": True, "receipt_status": "FINALIZED_AFTER_COMMAND",
                "retry_execution_commit": approval_source.source.RETRY_EXECUTION_COMMIT,
            }
            for field, value in expected.items():
                if receipt.get(field) != value:
                    raise ValueError(f"{field} mismatch")
            if _receipt_digest(receipt) != approval_source.source.SOURCE_RECEIPT_DIGEST:
                raise ValueError("receipt digest mismatch")
            result_expected = {"exit_code": 1, "stdout_byte_count": 1231380, "stderr_byte_count": 0,
                               "combined_output_byte_count": 1231380,
                               "stdout_sha256": approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"],
                               "stderr_sha256": approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"],
                               "stdout_excerpt_truncated": True, "stderr_excerpt_truncated": False}
            if any(result.get(field) != value for field, value in result_expected.items()):
                raise ValueError("controlled recapture facts mismatch")
            if receipt.get("redaction_summary", {}).get("redaction_checked") is not True:
                raise ValueError("redaction check missing")
            stdout, stderr = receipt.get("bounded_stdout_excerpt"), receipt.get("bounded_stderr_excerpt")
            if not isinstance(stdout, str) or not isinstance(stderr, str) or not (stdout.strip() or stderr.strip()):
                raise ValueError("bounded excerpts unavailable")
            max_snippets = min(5, max(1, int(max_snippets_per_family)))
            max_chars = min(500, max(1, int(max_snippet_chars)))
            execution = _success(common, receipt, raw, path, stdout, stderr, max_snippets, max_chars)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            execution = _blocked(common, f"DURABLE_RECEIPT_OR_BOUNDED_EVIDENCE_BOUNDARY_FAILURE: {exc}", available,
                                 ["valid digest-bound finalized receipt with at least one bounded excerpt"])
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(execution: dict) -> dict:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    blocked = execution.get("artifact_kind") == ARTIFACT_KIND_BLOCKED
    if not (success or blocked):
        raise error("artifact kind mismatch")
    expected_status = EXECUTION_STATUS_SUCCESS if success else EXECUTION_STATUS_BLOCKED
    if execution.get("execution_status") != expected_status or execution.get("execution_scope") != EXECUTION_SCOPE:
        raise error("artifact status or scope mismatch")
    expected_common = _common(execution.get("run_timestamp_utc"), None)
    for field, value in expected_common.items():
        if execution.get(field) != value:
            raise error(f"{field} mismatch")
    if execution.get("selected_remediation_or_method_package") != SELECTED_PACKAGE:
        raise error("selected package mismatch")
    if success:
        if any(execution.get(field) is not True for field in SUCCESS_TRUE_FIELDS):
            raise error("success fact missing")
        if not (execution.get("source_bounded_stdout_excerpt_used") or execution.get("source_bounded_stderr_excerpt_used")):
            raise error("bounded excerpt source missing")
        families = execution.get("observable_failure_families")
        if not isinstance(families, list) or not families:
            raise error("observable families missing")
        if execution.get("outputs") != SUCCESS_OUTPUTS or execution.get("recommended_next_task") != SUCCESS_NEXT_TASK:
            raise error("success outputs or recommendation missing")
        if execution.get(CLASSIFICATION_DIGEST_KEY) != semantic_digest(families):
            raise error("classification digest mismatch")
        expected_bounded = semantic_digest({"integrity": execution.get("bounded_excerpt_integrity_summary"),
                                            "classification_method": execution.get("failure_family_classification_method")})
        if execution.get(BOUNDED_ANALYSIS_DIGEST_KEY) != expected_bounded:
            raise error("bounded analysis digest mismatch")
        if execution.get(MANIFEST_DIGEST_KEY) != semantic_digest(execution.get("digest_manifest")):
            raise error("manifest digest mismatch")
        if execution.get(EXECUTION_DIGEST_KEY) != _execution_digest(execution):
            raise error("execution digest mismatch")
    else:
        if not execution.get("blocked_reason") or not isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str):
            raise error("blocked disposition incomplete")
        if execution.get("recommended_next_task") != BLOCKED_NEXT_TASK:
            raise error("blocked recommendation mismatch")
    checklist = _checklist(execution)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution):
        raise error("summary mismatch")
    return {"artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
            "execution_scope": EXECUTION_SCOPE, **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
    output_dir: str | Path, *, source_approval: dict | None = None, durable_receipt_path: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    execution = execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        source_approval=source_approval, durable_receipt_path=durable_receipt_path, run_timestamp_utc=run_timestamp_utc
    )
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("protected output directory")
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_markdown_v1(execution), encoding="utf-8")
    return execution


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_markdown_v1(execution: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(execution)
    families = execution.get("observable_failure_families", [])
    sections = [
        ("Source Approval", [SOURCE_APPROVAL_COMMIT, SOURCE_APPROVAL_DIGEST]),
        ("Source Operator Review and Candidate", [approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, approval_source.source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Diagnostic Results Review", [approval_source.source.SOURCE_RESULTS_REVIEW_DIGEST]),
        ("Source Controlled Recapture Execution", [approval_source.source.SOURCE_EXECUTION_COMMIT, approval_source.source.SOURCE_EXECUTION_DIGEST]),
        ("Source Durable Receipt", [approval_source.source.SOURCE_DURABLE_RECEIPT_PATH, approval_source.source.SOURCE_RECEIPT_DIGEST]),
        ("Source Receipt Loss History", [approval_source.source.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [approval_source.source.SOURCE_BINDINGS["source_planning_execution_digest"], approval_source.source.SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24877 passed; 1292 failed; 112 errors; 7 skipped; retry remains failed."]),
        ("Execution Scope", [EXECUTION_SCOPE]), ("Selected Remediation or Method Package", [SELECTED_PACKAGE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in approval_source.source.PRIORITY_1_TARGET_MODULES]),
        ("Diagnostic Capture Evidence Summary", ["Exit 1; bounded stdout/stderr only; diagnostic evidence, not retry evidence."]),
        ("Method Input Source", [str(execution.get("method_input_source_summary", execution.get("available_data")))]),
        ("Durable Receipt Integrity", [str(execution.get("durable_receipt_integrity_summary", execution.get("missing_data")))]),
        ("Bounded Excerpt Integrity", [str(execution.get("bounded_excerpt_integrity_summary", execution.get("blocked_reason")))]),
        ("Failure-Family Classification Method", [str(execution.get("failure_family_classification_method", "not executed"))]),
        ("Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in families] or ["none; execution blocked"]),
        ("Family Confidence and Limitations", [str(execution.get("family_confidence_summary", {})), *execution.get("method_limitations", [])]),
        ("Unsupported Claims Boundary", [str(execution.get("unsupported_claims_boundary", {"all unsupported claims remain false": True}))]),
        ("Success or Blocked Disposition", [execution["execution_status"], str(execution.get("blocked_reason"))]),
        ("Recommendation", [execution["recommended_next_task"]]), ("Next Chain", execution["next_chain"]),
        ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["No remediation, retry, main merge, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Committed receipt and bounded excerpts only; no cache, logs, environment, commands, providers, or full-stream reconstruction."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Diagnostic Capture v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_DIAGNOSTIC_CAPTURE_V1 = ARTIFACT_KIND_SUCCESS
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_DIAGNOSTIC_CAPTURE_V1 = ARTIFACT_KIND_BLOCKED
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_AFTER_DIAGNOSTIC_CAPTURE_FAILURE_FAMILY_CLASSIFICATION_READY = EXECUTION_STATUS_SUCCESS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AFTER_DIAGNOSTIC_CAPTURE_DURABLE_RECEIPT_OR_BOUNDED_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = EXECUTION_STATUS_BLOCKED
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_ONLY_METHOD_ANALYSIS_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CLASSIFY_REVIEWED_DURABLE_DIAGNOSTIC_RECEIPT_FAILURE_FAMILIES_FOR_REMEDIATION_METHOD_PLANNING = SELECTED_PACKAGE

__all__ = [name for name in globals() if name.isupper() or name.startswith(("execute_marketflow_", "write_marketflow_", "validate_marketflow_", "build_marketflow_", "MarketFlowRepository"))]
