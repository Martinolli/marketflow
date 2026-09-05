"""Diagnose the blocked plan-derived remediation execution, offline only."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
DIAGNOSIS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_digest"

SOURCE_BLOCKED_EXECUTION_COMMIT = "65aab2f4a5cc699cc630756c4142dee12f96c838"
SOURCE_BLOCKED_MANIFEST_DIGEST = "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"
SOURCE_BLOCKED_REASON = source.BLOCKED_NO_CHANGE_AUTHORITY
SELECTED_PACKAGE = source.SELECTED_PACKAGE
PRIMARY_FAILURE_CLASS = "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
SECONDARY_FAILURE_CLASSES = (
    "REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY",
    "PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT",
    "NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS",
    "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
)
RECOMMENDED_NEXT_PACKAGE = "PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_REMEDIATION_EXECUTION"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_V1"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

DIAGNOSIS_SUMMARY = (
    "The approved execution correctly failed closed because the reviewed plan and workstreams identified observable "
    "failure families but did not provide sufficient source authority to justify changing current source code, "
    "existing tests, expected digests, schemas, fixtures, or exports. Priority 1 focused validation passed before "
    "and after the blocked attempt, so the execution had no evidence-supported retained remediation change to make. "
    "The failed detached retry remains authoritative, but this blocked execution does not explain or remediate that "
    "retry failure and does not create retry readiness."
)

DIAGNOSIS_DOMAINS = (
    ("source_approval_and_package_authority", "PASSED", "Source approval and selected package were valid and bound."),
    ("source_plan_results_review_authority", "PASSED", "Plan results review, targeted plan review, workstream mapping review, and manifest digests were bound."),
    ("reviewed_workstream_evidence", "INSUFFICIENT_FOR_DIRECT_CHANGE_AUTHORITY", "Four reviewed workstreams exist, but they do not prove any current file must be changed."),
    ("current_root_priority1_validation", "PASSED_BUT_NOT_RETRY_EVIDENCE", "Priority 1 validation passed 675 tests before and after, but this is not detached retry evidence."),
    ("file_impact_inventory", "CREATED_UNCHANGED_CANDIDATES", "Ten Priority 1 test/service candidates were inventoried as unchanged."),
    ("retained_change_records", "ABSENT_BY_CORRECT_FAIL_CLOSED_DECISION", "No retained changes were recorded because no source-authority-bound remediation was identified."),
    ("remediation_execution_success", "BLOCKED", "Success digests were not generated because no controlled remediation was performed."),
    ("authoritative_retry_status", "STILL_FAILED", "The detached retry remains 24,877 passed, 1,292 failed, 112 errors, and 7 skipped."),
    ("branch_and_evidence_boundaries", "PRESERVED", "Main, integration branch, detached worktree, staged evidence, cache, and .marketflow boundaries remain preserved."),
    ("downstream_readiness", "CLOSED", "Ready for retry candidate and main merge remain false."),
    ("likely_next_direction", "ACTION_REQUIRED", "A separately governed source-authority enrichment, alternate diagnostic, or no-change disposition candidate is required before further remediation or retry planning."),
)

DIAGNOSIS_FINDINGS = (
    "The source execution selected the approved controlled plan-derived remediation package.",
    "The source execution correctly entered the controlled remediation gate after approval.",
    "The source execution created or reviewed a file-impact inventory for the Priority 1 candidate test/service files.",
    "The Priority 1 focused validation passed before and after the blocked attempt.",
    "The passing Priority 1 focused validation is not full pytest, detached retry evidence, integration success, or main-merge readiness.",
    "The reviewed workstreams provide planning categories and verification expectations but do not prove a current source, test, digest, fixture, schema, or export defect.",
    "No retained source-authority-bound remediation change was identified.",
    "The execution correctly generated a blocked artifact instead of inventing a remediation.",
    "No production code, existing tests, expected digests, patches, evidence, .marketflow, or .pytest_cache files were modified or committed.",
    "The authoritative detached retry remains failed and unchanged.",
    "No retry candidate, retry readiness, integration success, main-merge readiness, runtime authority, broker authority, or trading authority was created.",
    "The next step requires a separately governed candidate to decide between source-authority enrichment, alternate diagnostics, no-change disposition review, or another approved path.",
)

NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Candidate After Blocked Remediation Execution v1",
    "Candidate Operator Review v1",
    "Approval v1 if selected",
    "Execution v1 if approved",
    "Results Review v1",
    "Conditional remediation execution candidate, alternate diagnostic candidate, or no-change retry candidate only if review supports it",
    "New Integration Branch Retry Candidate v1 only after a reviewed approved basis exists",
    "New Integration Branch Retry Approval v1",
    "New Integration Branch Retry Execution v1",
    "New Integration Branch Retry Results Review v1",
    "Main Merge Approval only if new retry results review passes",
)
NEXT_GATES = tuple(
    """source_authority_or_no_change_disposition_candidate_after_blocked_execution
source_authority_or_no_change_disposition_candidate_operator_review
source_authority_or_no_change_disposition_approval_if_selected
source_authority_or_no_change_disposition_execution_if_approved
source_authority_or_no_change_disposition_results_review
conditional_follow_on_candidate_if_results_review_supports
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)
RISK_CONTROLS = tuple(
    """failure_diagnosis_does_not_execute_remediation
failure_diagnosis_does_not_modify_production_code
failure_diagnosis_does_not_modify_existing_tests
failure_diagnosis_does_not_update_expected_digests
failure_diagnosis_does_not_generate_patch
failure_diagnosis_does_not_apply_patch
failure_diagnosis_does_not_run_pytest
failure_diagnosis_does_not_run_full_pytest
failure_diagnosis_does_not_rerun_retry
failure_diagnosis_does_not_rerun_detached_retry
failure_diagnosis_does_not_parse_durable_receipt
failure_diagnosis_does_not_analyze_diagnostic_output
failure_diagnosis_does_not_rerun_plan_execution
failure_diagnosis_does_not_regenerate_targeted_plan
failure_diagnosis_does_not_rerun_method_execution
failure_diagnosis_does_not_rerun_controlled_recapture
failure_diagnosis_does_not_run_diagnostic_command
failure_diagnosis_does_not_read_pytest_cache
failure_diagnosis_does_not_modify_pytest_cache
failure_diagnosis_does_not_parse_terminal_logs
failure_diagnosis_does_not_parse_operator_logs
failure_diagnosis_does_not_inspect_env
failure_diagnosis_does_not_reconstruct_prior_lost_values
failure_diagnosis_does_not_reconstruct_full_streams
failure_diagnosis_does_not_classify_modules_again
failure_diagnosis_does_not_classify_full_retry_failures
failure_diagnosis_does_not_classify_full_retry_errors
failure_diagnosis_does_not_claim_failure_error_separation
failure_diagnosis_does_not_identify_authoritative_first_failure
failure_diagnosis_does_not_identify_authoritative_first_error
failure_diagnosis_does_not_claim_traceback_root_cause
failure_diagnosis_does_not_claim_root_cause
failure_diagnosis_does_not_claim_retry_success
failure_diagnosis_does_not_claim_main_merge_readiness
failure_diagnosis_does_not_create_remediation_execution
failure_diagnosis_does_not_create_remediation_execution_results_review
failure_diagnosis_does_not_create_new_retry_candidate
failure_diagnosis_does_not_create_retry_results_review
failure_diagnosis_does_not_create_integration_results_review
failure_diagnosis_does_not_mark_integration_successful
failure_diagnosis_does_not_generate_successful_integration_digest
failure_diagnosis_does_not_push_integration_branch
failure_diagnosis_does_not_push_main
failure_diagnosis_does_not_delete_integration_branch
failure_diagnosis_does_not_delete_worktree
failure_diagnosis_does_not_force_push
failure_diagnosis_does_not_prune_remotes
failure_diagnosis_does_not_modify_tags
failure_diagnosis_does_not_modify_staged_evidence
failure_diagnosis_does_not_regenerate_evidence
failure_diagnosis_does_not_call_providers
failure_diagnosis_does_not_acquire_market_data
failure_diagnosis_does_not_regenerate_dataset
failure_diagnosis_does_not_recompute_metrics_from_raw_rows
failure_diagnosis_does_not_train_models
failure_diagnosis_does_not_score_strategy
failure_diagnosis_does_not_generate_trade_recommendations
failure_diagnosis_does_not_accept_predictive_usefulness
failure_diagnosis_does_not_accept_profitability
failure_diagnosis_does_not_authorize_runtime
failure_diagnosis_does_not_authorize_broker_execution
blocked_remediation_execution_remains_source_evidence
blocked_reason_remains_authoritative_for_this_diagnosis
source_authority_gap_is_not_root_cause
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
no_change_records_means_no_remediation_success
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_candidate_required_before_alternate_path
separate_approval_required_before_any_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()
)

TRUE_FIELDS = tuple(
    """remediation_execution_after_plan_results_review_failure_diagnosis_created
source_blocked_execution_reviewed
source_blocked_manifest_digest_bound
source_blocked_reason_bound
source_approval_verified
source_operator_review_verified
source_candidate_verified
source_plan_results_review_verified
source_plan_execution_verified
source_workstream_mapping_verified
priority1_pre_change_validation_reviewed
priority1_post_change_validation_reviewed
priority1_validation_passed
file_impact_inventory_reviewed
file_impact_inventory_identified_only_unchanged_candidates
remediation_execution_correctly_blocked""".splitlines()
)
FALSE_FIELDS = tuple(
    """retained_change_records_available
safe_source_authority_bound_change_identified
success_digests_generated
remediation_execution_performed
controlled_plan_derived_remediation_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
diagnostic_receipt_parsed_in_diagnosis
diagnostic_output_analyzed_in_diagnosis
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_diagnosis
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_diagnosis
full_pytest_performed
retry_rerun_performed
detached_retry_rerun_performed
cache_read_in_diagnosis
cache_modified_in_diagnosis
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
prior_lost_values_reconstructed
prior_lost_values_inferred
full_stdout_reconstructed
full_stderr_reconstructed
failure_modules_classified
error_modules_classified
failure_error_separation_claimed
first_failure_identified
first_error_identified
first_order_claim_made
traceback_root_cause_claimed
root_cause_claimed
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_execution_results_review
ready_for_retry_candidate
ready_for_main_merge_approval
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated
integration_branch_pushed
main_push_performed
origin_main_modified_by_this_task
evidence_regenerated
provider_requests_made_in_diagnosis
market_data_acquisition_performed_in_diagnosis
dataset_generation_performed_in_diagnosis
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError(ValueError):
    """Raised when diagnosis evidence violates the fixed offline contract."""


def _source_bindings(source_blocked_execution: dict | None = None) -> dict[str, Any]:
    if source_blocked_execution is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
                deepcopy(source_blocked_execution)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError(
                "source blocked execution validation failed"
            ) from exc
        for field, expected in (
            ("artifact_kind", source.BLOCKED_ARTIFACT_KIND),
            ("execution_status", source.BLOCKED_STATUS),
            ("execution_scope", source.EXECUTION_SCOPE),
            ("blocked_reason", SOURCE_BLOCKED_REASON),
            (source.BLOCKED_MANIFEST_DIGEST_KEY, SOURCE_BLOCKED_MANIFEST_DIGEST),
        ):
            if source_blocked_execution.get(field) != expected:
                raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError(
                    f"source blocked execution {field} mismatch"
                )
    bindings = deepcopy(source.SOURCE_BINDINGS)
    bindings.update(
        {
            "source_blocked_execution_artifact_kind": source.BLOCKED_ARTIFACT_KIND,
            "source_blocked_execution_status": source.BLOCKED_STATUS,
            "source_blocked_execution_scope": source.EXECUTION_SCOPE,
            "source_blocked_execution_commit": SOURCE_BLOCKED_EXECUTION_COMMIT,
            "source_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
            "source_blocked_reason": SOURCE_BLOCKED_REASON,
            "source_planning_results_review_manifest_digest": "02d83a02ccdd0e67ccd13e36575b8a654617cce3190b98ec977fd829d8bc295d",
            "source_method_results_review_manifest_digest": "11e3ad0c24bd29684854b51efd13b4557d7aeab9e1e193b807a1aa3373e0f00b",
        }
    )
    return bindings


SOURCE_BINDINGS = _source_bindings()
SOURCE_CORE = source.SOURCE_CORE


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", expected, diagnosis.get(field)) for field, expected in SOURCE_BINDINGS.items()]
    checks.extend(
        [
            _check("selected_remediation_execution_package_bound", SELECTED_PACKAGE, diagnosis.get("selected_remediation_execution_package")),
            _check("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, diagnosis.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", list(SOURCE_CORE["priority_1_target_modules"]), diagnosis.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, diagnosis.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, diagnosis.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, diagnosis.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, diagnosis.get("failed_or_errored_nodeids_count")),
            _check("diagnostic_exit_code_1_bound_as_diagnostic_only", 1, diagnosis.get("source_exit_code")),
            _check("diagnostic_stdout_hash_bound", SOURCE_CORE["source_stdout_sha256"], diagnosis.get("source_stdout_sha256")),
            _check("diagnostic_stderr_hash_bound", SOURCE_CORE["source_stderr_sha256"], diagnosis.get("source_stderr_sha256")),
            _check("priority1_pre_change_validation_675_passed_bound", 675, diagnosis.get("priority1_pre_change_validation_passed_count")),
            _check("priority1_post_change_validation_675_passed_bound", 675, diagnosis.get("priority1_post_change_validation_passed_count")),
            _check("priority1_post_change_stdout_hash_bound", "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374", diagnosis.get("priority1_post_change_stdout_sha256")),
            _check("observable_family_count_4_bound", 4, diagnosis.get("observable_failure_family_count")),
            _check("observable_evidence_items_188_bound", 188, diagnosis.get("total_observable_evidence_items")),
            _check("observable_family_ids_bound", set(source.FAMILY_IDS), {item.get("family_id") for item in diagnosis.get("reviewed_observable_failure_families", [])}),
            _check("workstream_count_4_bound", 4, diagnosis.get("source_workstream_count")),
            _check("workstream_ids_bound", set(source.WORKSTREAM_IDS), {item.get("workstream_id") for item in diagnosis.get("reviewed_workstreams", [])}),
            _check("primary_failure_class_set", PRIMARY_FAILURE_CLASS, diagnosis.get("primary_failure_class")),
            _check("secondary_failure_classes_set", list(SECONDARY_FAILURE_CLASSES), diagnosis.get("secondary_failure_classes")),
            _check("diagnosis_domains_defined", True, bool(diagnosis.get("diagnosis_domains"))),
            _check("diagnosis_findings_defined", True, bool(diagnosis.get("diagnosis_findings"))),
            _check("recommendation_defined", True, bool(diagnosis.get("recommendation"))),
            _check("next_chain_defined", True, bool(diagnosis.get("next_chain"))),
            _check("next_gates_defined", True, bool(diagnosis.get("next_gates"))),
            _check("risk_controls_defined", True, bool(diagnosis.get("risk_controls"))),
            _check("no_tracked_marketflow_files", True, diagnosis.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, diagnosis.get("no_tracked_pytest_cache_files")),
        ]
    )
    checks.extend(_check(f"{field}_true", True, diagnosis.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, diagnosis.get(field)) for field in FALSE_FIELDS)
    return checks


def _summary(diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    checklist = diagnosis["checklist"]
    passed = sum(item["status"] == PASS for item in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed,
        "remediation_execution_after_plan_results_review_failure_diagnosis_created": True,
        "source_blocked_execution_reviewed": True, "source_blocked_reason": SOURCE_BLOCKED_REASON,
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_validation_duration_seconds": "41.88",
        "safe_source_authority_bound_change_identified": False, "retained_change_records_available": False,
        "remediation_execution_correctly_blocked": True, "remediation_execution_performed": False,
        "controlled_plan_derived_remediation_performed": False, "production_code_modified": False,
        "existing_tests_modified": False, "expected_digests_updated": False, "patch_generated": False,
        "patch_applied": False, "success_digests_generated": False,
        "ready_for_remediation_execution_results_review": False, "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False, "new_retry_candidate_created": False,
        "new_retry_executed": False, "integration_execution_successful": False,
        "source_workstream_count": 4, "workstream_family_ids": list(source.FAMILY_IDS),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _digest(diagnosis: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(diagnosis))
    for field in ("checklist", "summary", DIAGNOSIS_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(
    *, source_blocked_execution: dict | None = None,
) -> dict[str, Any]:
    """Build the fixed diagnosis without rerunning or reading execution evidence."""

    bindings = _source_bindings(source_blocked_execution)
    priority_validation = {
        "pre_change": {"passed": True, "passed_count": 675, "evidence_type": "SOURCE_BLOCKED_EXECUTION_RECORDED_FACT"},
        "post_change": {
            "passed": True, "passed_count": 675, "duration_seconds": "41.88", "stdout_byte_count": 832,
            "stderr_byte_count": 0, "stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
            "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "evidence_type": "SOURCE_BLOCKED_EXECUTION_RECORDED_FACT",
        },
        "not_retry_evidence": True, "not_full_pytest": True,
    }
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        **bindings, "selected_remediation_execution_package": SELECTED_PACKAGE,
        "retry_failure_context": deepcopy(SOURCE_CORE["retry_failure_context"]),
        "source_blocked_execution_summary": {
            "artifact_kind": source.BLOCKED_ARTIFACT_KIND, "status": source.BLOCKED_STATUS,
            "scope": source.EXECUTION_SCOPE, "commit": SOURCE_BLOCKED_EXECUTION_COMMIT,
            "blocked_reason": SOURCE_BLOCKED_REASON, "blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
            "checklist": "215/215 PASS", "success_digests_generated": False,
        },
        "source_approval_summary": {"commit": source.SOURCE_APPROVAL_COMMIT, "digest": source.SOURCE_APPROVAL_DIGEST, "selected_package": SELECTED_PACKAGE},
        "source_operator_review_and_candidate_summary": {
            "operator_review_commit": bindings["source_remediation_execution_candidate_after_plan_results_review_operator_review_commit"],
            "operator_review_digest": bindings["source_remediation_execution_candidate_after_plan_results_review_operator_review_digest"],
            "candidate_commit": bindings["source_remediation_execution_candidate_after_plan_results_review_commit"],
            "candidate_digest": bindings["source_remediation_execution_candidate_after_plan_results_review_digest"],
        },
        "source_plan_results_review_summary": deepcopy(SOURCE_CORE["source_plan_results_review_summary"]),
        "source_plan_execution_summary": deepcopy(SOURCE_CORE["source_plan_execution_summary"]),
        "source_targeted_remediation_plan_summary": deepcopy(SOURCE_CORE["source_targeted_remediation_plan_summary"]),
        "source_workstream_mapping_summary": deepcopy(SOURCE_CORE["source_workstream_mapping_summary"]),
        "source_method_results_review_summary": deepcopy(SOURCE_CORE["source_method_results_review_summary"]),
        "source_method_execution_summary": deepcopy(SOURCE_CORE["source_method_execution_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(SOURCE_CORE["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_summary": deepcopy(SOURCE_CORE["source_controlled_recapture_execution_summary"]),
        "source_durable_receipt_summary": deepcopy(SOURCE_CORE["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(SOURCE_CORE["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(SOURCE_CORE["source_planning_and_detail_binding_summary"]),
        "priority_1_target_modules": deepcopy(SOURCE_CORE["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404, "priority1_validation_summary": priority_validation,
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_validation_duration_seconds": "41.88",
        "priority1_post_change_stdout_byte_count": 832, "priority1_post_change_stderr_byte_count": 0,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380, "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"], "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False, "source_redaction_checked": True,
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380,
            "stderr_byte_count": 0, "stdout_sha256": SOURCE_CORE["source_stdout_sha256"],
            "stderr_sha256": SOURCE_CORE["source_stderr_sha256"], "diagnostic_only": True,
        },
        "reviewed_observable_failure_families": deepcopy(SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "reviewed_workstreams": deepcopy(SOURCE_CORE["reviewed_workstreams"]), "source_workstream_count": 4,
        "file_impact_inventory_summary": {
            "candidate_count": 10, "unchanged_candidate_count": 10, "changed_candidate_count": 0,
            "test_candidate_count": 5, "service_candidate_count": 5,
            "paths": list(source.PRIORITY_1_PATHS), "pre_change_hashes_recorded": True,
        },
        "blocked_execution_analysis": {
            "approval_and_package_valid": True, "plan_and_workstreams_bound": True,
            "workstreams_supply_direct_change_authority": False, "priority1_validation_passed": True,
            "retained_changes": 0, "blocked_decision_correct": True,
        },
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES), "diagnosis_summary": DIAGNOSIS_SUMMARY,
        "diagnosis_domains": [
            {"domain_id": domain, "disposition": disposition, "explanation": explanation}
            for domain, disposition, explanation in DIAGNOSIS_DOMAINS
        ],
        "diagnosis_findings": [{"finding_id": f"finding_{index}", "finding": text} for index, text in enumerate(DIAGNOSIS_FINDINGS, 1)],
        "unsupported_claims_boundary": {
            "root_cause": "NOT_CLAIMED", "retry_success": "NOT_CLAIMED",
            "integration_success": "NOT_CLAIMED", "main_merge_readiness": "NOT_CLAIMED",
            "source_authority_gap": "EXECUTION_BLOCKING_CONDITION_NOT_RETRY_ROOT_CAUSE",
        },
        "recommendation": {
            "recommended_next_package": RECOMMENDED_NEXT_PACKAGE, "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_REMEDIATION_EXECUTION",
            "reason": "The plan defined controls but not concrete change authority. A separate candidate must choose source-authority enrichment, alternate bounded diagnostics, no-change disposition review, or another approved path before retry or main merge.",
        },
        "recommended_next_package": RECOMMENDED_NEXT_PACKAGE, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_REMEDIATION_EXECUTION",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis)
    diagnosis[DIAGNOSIS_DIGEST_KEY] = _digest(diagnosis)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError
    if not isinstance(diagnosis, dict):
        raise error("diagnosis must be an object")
    for field, expected in (
        ("artifact_kind", ARTIFACT_KIND), ("schema_version", SCHEMA_VERSION),
        ("diagnosis_status", DIAGNOSIS_STATUS), ("diagnosis_scope", DIAGNOSIS_SCOPE),
        ("selected_remediation_execution_package", SELECTED_PACKAGE),
        ("primary_failure_class", PRIMARY_FAILURE_CLASS),
        ("secondary_failure_classes", list(SECONDARY_FAILURE_CLASSES)),
    ):
        if diagnosis.get(field) != expected:
            raise error(f"{field} mismatch")
    for field, expected in SOURCE_BINDINGS.items():
        if diagnosis.get(field) != expected:
            raise error(f"{field} mismatch")
    fixed = {
        "priority_1_target_modules": SOURCE_CORE["priority_1_target_modules"], "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "priority1_pre_change_validation_passed": True, "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True, "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188, "source_workstream_count": 4,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected in fixed.items():
        if diagnosis.get(field) != expected:
            raise error(f"{field} mismatch")
    if diagnosis.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise error("retry failure counts mismatch")
    families = diagnosis.get("reviewed_observable_failure_families", [])
    if {item.get("family_id") for item in families} != set(source.FAMILY_IDS):
        raise error("observable families mismatch")
    if any(item.get("confidence") != "HIGH" or item.get("observable_evidence_count") != 47 for item in families):
        raise error("observable family evidence mismatch")
    if {item.get("workstream_id") for item in diagnosis.get("reviewed_workstreams", [])} != set(source.WORKSTREAM_IDS):
        raise error("reviewed workstreams mismatch")
    if len(diagnosis.get("diagnosis_domains", [])) < 11 or len(diagnosis.get("diagnosis_findings", [])) < 12:
        raise error("diagnosis domains or findings missing")
    if not diagnosis.get("recommendation") or not diagnosis.get("next_chain") or not diagnosis.get("next_gates") or not diagnosis.get("risk_controls"):
        raise error("recommendation or governance path missing")
    for field in TRUE_FIELDS:
        if diagnosis.get(field) is not True:
            raise error(f"{field} must be true")
    for field in FALSE_FIELDS:
        if diagnosis.get(field) is not False:
            raise error(f"{field} must be false")
    checklist = _checklist(diagnosis)
    if diagnosis.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if diagnosis.get("summary") != _summary(diagnosis):
        raise error("summary mismatch")
    digest = diagnosis.get(DIAGNOSIS_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _digest(diagnosis):
        raise error("diagnosis digest missing or changed")
    return {
        "artifact_kind": ARTIFACT_KIND, "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE, "diagnosis_digest": digest,
        **{key: diagnosis["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Blocked Execution", "Blocked Reason", "Diagnosis Summary", "Diagnosis Classification", "Source Approval",
    "Source Operator Review and Candidate", "Source Plan Results Review", "Source Plan Execution",
    "Source Targeted Remediation Plan", "Source Workstream Mapping", "Source Method Results Review",
    "Source Method Execution", "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "File Impact Inventory Summary", "Blocked Execution Analysis", "Diagnosis Domains",
    "Diagnosis Findings", "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(deepcopy(diagnosis))
    sections: dict[str, Any] = {
        "Source Blocked Execution": diagnosis["source_blocked_execution_summary"], "Blocked Reason": diagnosis["source_blocked_reason"],
        "Diagnosis Summary": diagnosis["diagnosis_summary"],
        "Diagnosis Classification": {"primary": diagnosis["primary_failure_class"], "secondary": diagnosis["secondary_failure_classes"], "digest": diagnosis[DIAGNOSIS_DIGEST_KEY]},
        "Source Approval": diagnosis["source_approval_summary"],
        "Source Operator Review and Candidate": diagnosis["source_operator_review_and_candidate_summary"],
        "Source Plan Results Review": diagnosis["source_plan_results_review_summary"],
        "Source Plan Execution": diagnosis["source_plan_execution_summary"],
        "Source Targeted Remediation Plan": diagnosis["source_targeted_remediation_plan_summary"],
        "Source Workstream Mapping": diagnosis["source_workstream_mapping_summary"],
        "Source Method Results Review": diagnosis["source_method_results_review_summary"],
        "Source Method Execution": diagnosis["source_method_execution_summary"],
        "Source Diagnostic Results Review": diagnosis["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": diagnosis["source_controlled_recapture_summary"],
        "Source Durable Receipt": diagnosis["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": diagnosis["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": diagnosis["retry_failure_context"], "Priority 1 Target Modules": diagnosis["priority_1_target_modules"],
        "Priority 1 Validation Summary": diagnosis["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": diagnosis["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": diagnosis["reviewed_observable_failure_families"],
        "Reviewed Workstreams": diagnosis["reviewed_workstreams"], "File Impact Inventory Summary": diagnosis["file_impact_inventory_summary"],
        "Blocked Execution Analysis": diagnosis["blocked_execution_analysis"], "Diagnosis Domains": diagnosis["diagnosis_domains"],
        "Diagnosis Findings": diagnosis["diagnosis_findings"], "Unsupported Claims Boundary": diagnosis["unsupported_claims_boundary"],
        "Recommendation": diagnosis["recommendation"], "Next Chain": diagnosis["next_chain"], "Next Gates": diagnosis["next_gates"],
        "Risk Controls": diagnosis["risk_controls"],
        "Authority Boundaries": {"runtime_use": diagnosis["runtime_use"], "broker_execution": diagnosis["broker_execution"], "retry_ready": diagnosis["ready_for_retry_candidate"]},
        "Checklist Summary": diagnosis["summary"], "Guardrails": list(FALSE_FIELDS),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution After Plan Results Review Failure Diagnosis v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", f"```text\n{sections[title]!r}\n```", ""))
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(
    output_dir: str | Path, *, source_blocked_execution: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError("protected output directory")
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(
        source_blocked_execution=source_blocked_execution
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_markdown_v1(diagnosis), encoding="utf-8")
    return diagnosis


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE
NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED = PRIMARY_FAILURE_CLASS
REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY = SECONDARY_FAILURE_CLASSES[0]
PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT = SECONDARY_FAILURE_CLASSES[1]
NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS = SECONDARY_FAILURE_CLASSES[2]
DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED = SECONDARY_FAILURE_CLASSES[3]
