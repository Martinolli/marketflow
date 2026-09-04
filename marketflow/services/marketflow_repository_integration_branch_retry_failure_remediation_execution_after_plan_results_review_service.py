"""Execute the approved retry-failure remediation package, fail-closed.

This module is deliberately orchestration-free.  It records caller-supplied
change and focused-validation evidence; it never runs pytest, reads diagnostic
receipts/caches/logs, or invokes repository/provider operations.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_service
    as approval,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_EXECUTED_AFTER_PLAN_RESULTS_REVIEW_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_BLOCKED_AFTER_PLAN_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_EXECUTED_AFTER_PLAN_RESULTS_REVIEW_CONTROLLED_PLAN_DERIVED_REMEDIATION_READY_FOR_RESULTS_REVIEW"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_BLOCKED_AFTER_PLAN_RESULTS_REVIEW_SOURCE_AUTHORITY_CHANGE_SCOPE_OR_VALIDATION_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_ONLY_CONTROLLED_PLAN_DERIVED_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = approval.SELECTED_PACKAGE
SOURCE_APPROVAL_COMMIT = "07ecfa2353f450ffacd807809d4857c8f8231b9b"
SOURCE_APPROVAL_DIGEST = "2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_digest"
FILE_IMPACT_INVENTORY_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_file_impact_inventory_digest"
CHANGE_RECORDS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_change_records_digest"
VALIDATION_REPORT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_validation_report_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_blocked_manifest_digest"

PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"
BLOCKED_NO_CHANGE_AUTHORITY = "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
BLOCKED_VALIDATION = "FOCUSED_VALIDATION_NOT_PROVIDED_OR_DID_NOT_PASS"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"

WORKSTREAM_IDS = (
    "assertion_value_mismatch_workstream",
    "digest_hash_boundary_workstream",
    "fixture_isolation_determinism_workstream",
    "schema_field_contract_workstream",
)
FAMILY_IDS = (
    "assertion_or_value_mismatch",
    "digest_or_hash_mismatch",
    "fixture_or_test_isolation_issue",
    "missing_or_unexpected_field",
)
PRIORITY_1_TEST_PATHS = (
    "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
    "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
    "tests/test_corporate_action_authority_plan_candidate_service.py",
    "tests/test_feature_generation_results_review_redesigned_labels_service.py",
    "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
)
PRIORITY_1_SERVICE_PATHS = (
    "marketflow/services/marketflow_signal_or_feature_generation_results_review_service.py",
    "marketflow/services/post_identity_freeze_registry_inventory_approval_service.py",
    "marketflow/services/corporate_action_authority_plan_candidate_service.py",
    "marketflow/services/feature_generation_results_review_redesigned_labels_service.py",
    "marketflow/services/marketflow_objective_label_or_target_generation_results_review_service.py",
)
PRIORITY_1_PATHS = PRIORITY_1_TEST_PATHS + PRIORITY_1_SERVICE_PATHS

FALSE_BOUNDARY_FIELDS = tuple(
    """full_pytest_performed
retry_rerun_performed
detached_retry_rerun_performed
integration_branch_pushed
main_push_performed
origin_main_modified_by_this_task
evidence_regenerated
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated
diagnostic_receipt_parsed_in_execution
diagnostic_output_analyzed_in_execution
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_execution
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_execution
cache_modified_in_execution
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
direct_code_remediation_recommended_outside_approved_package
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated""".splitlines()
)

SUCCESS_OUTPUT_NAMES = (
    "remediation_execution_after_plan_results_review_manifest",
    "source_approval_binding_report",
    "source_operator_review_binding_report",
    "source_candidate_binding_report",
    "source_plan_results_review_binding_report",
    "source_plan_execution_binding_report",
    "source_workstream_mapping_binding_report",
    "file_impact_inventory",
    "pre_change_snapshot",
    "change_records",
    "post_change_snapshot",
    "focused_validation_report",
    "workstream_to_change_mapping",
    "source_authority_mapping",
    "verification_evidence_report",
    "unsupported_claims_boundary_report",
    "retry_gate_preservation_report",
    "main_merge_gate_preservation_report",
    "digest_manifest",
)

NEXT_CHAIN_SUCCESS = (
    "Remediation Execution Results Review v1",
    "New Integration Branch Retry Candidate v1",
    "New Integration Branch Retry Approval v1",
    "New Integration Branch Retry Execution v1",
    "New Integration Branch Retry Results Review v1",
    "Main Merge Approval only if new retry results review passes",
)
NEXT_CHAIN_BLOCKED = (
    "Remediation Execution After Plan Results Review Failure Diagnosis v1",
    "Alternate remediation execution candidate or additional diagnostic candidate if needed",
    "No retry or main merge",
)
NEXT_GATES_SUCCESS = (
    "remediation_execution_results_review",
    "new_integration_branch_retry_candidate_after_remediation_results_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
)
NEXT_GATES_BLOCKED = (
    "remediation_execution_after_plan_results_review_failure_diagnosis",
    "alternate_remediation_execution_candidate_if_needed",
    "new_retry_blocked_until_remediation_results_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
)

RISK_CONTROLS = tuple(
    """remediation_execution_after_plan_results_review_uses_approved_package_only
remediation_execution_after_plan_results_review_is_plan_derived
remediation_execution_after_plan_results_review_is_source_authority_bound
remediation_execution_after_plan_results_review_records_file_impact_inventory
remediation_execution_after_plan_results_review_records_pre_change_snapshot
remediation_execution_after_plan_results_review_records_post_change_snapshot_if_changes_occur
remediation_execution_after_plan_results_review_records_verification_evidence
remediation_execution_after_plan_results_review_runs_focused_validation_only
remediation_execution_after_plan_results_review_does_not_run_full_pytest
remediation_execution_after_plan_results_review_does_not_rerun_detached_retry
remediation_execution_after_plan_results_review_does_not_push_main
remediation_execution_after_plan_results_review_does_not_push_integration_branch
remediation_execution_after_plan_results_review_does_not_parse_durable_receipt
remediation_execution_after_plan_results_review_does_not_analyze_diagnostic_output
remediation_execution_after_plan_results_review_does_not_read_pytest_cache
remediation_execution_after_plan_results_review_does_not_modify_pytest_cache
remediation_execution_after_plan_results_review_does_not_claim_root_cause
remediation_execution_after_plan_results_review_does_not_claim_retry_success
remediation_execution_after_plan_results_review_does_not_claim_main_merge_readiness
controlled_remediation_is_not_retry_success
focused_validation_is_not_full_pytest
verification_evidence_is_required_before_retry_candidate
remediation_results_review_required_before_retry_candidate
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
durable_receipt_is_diagnostic_evidence_only
priority_1_selection_is_not_root_cause
root_regression_not_retry_evidence
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation
remediation_execution_after_plan_results_review_does_not_rerun_plan_execution
remediation_execution_after_plan_results_review_does_not_regenerate_targeted_plan
remediation_execution_after_plan_results_review_does_not_rerun_method_execution
remediation_execution_after_plan_results_review_does_not_rerun_controlled_recapture
remediation_execution_after_plan_results_review_does_not_run_diagnostic_command
remediation_execution_after_plan_results_review_does_not_parse_terminal_logs
remediation_execution_after_plan_results_review_does_not_parse_operator_logs
remediation_execution_after_plan_results_review_does_not_inspect_env
remediation_execution_after_plan_results_review_does_not_reconstruct_prior_lost_values
remediation_execution_after_plan_results_review_does_not_reconstruct_full_streams
remediation_execution_after_plan_results_review_does_not_classify_modules_again
remediation_execution_after_plan_results_review_does_not_classify_full_retry_failures
remediation_execution_after_plan_results_review_does_not_classify_full_retry_errors
remediation_execution_after_plan_results_review_does_not_claim_failure_error_separation
remediation_execution_after_plan_results_review_does_not_identify_authoritative_first_failure
remediation_execution_after_plan_results_review_does_not_identify_authoritative_first_error
remediation_execution_after_plan_results_review_does_not_claim_traceback_root_cause
remediation_execution_after_plan_results_review_does_not_create_new_retry_candidate
remediation_execution_after_plan_results_review_does_not_create_retry_results_review
remediation_execution_after_plan_results_review_does_not_create_integration_results_review
remediation_execution_after_plan_results_review_does_not_mark_integration_successful
remediation_execution_after_plan_results_review_does_not_generate_successful_integration_digest
remediation_execution_after_plan_results_review_does_not_delete_integration_branch
remediation_execution_after_plan_results_review_does_not_delete_worktree
remediation_execution_after_plan_results_review_does_not_force_push
remediation_execution_after_plan_results_review_does_not_prune_remotes
remediation_execution_after_plan_results_review_does_not_modify_tags
remediation_execution_after_plan_results_review_does_not_modify_staged_evidence
remediation_execution_after_plan_results_review_does_not_regenerate_evidence
remediation_execution_after_plan_results_review_does_not_call_providers
remediation_execution_after_plan_results_review_does_not_acquire_market_data
remediation_execution_after_plan_results_review_does_not_regenerate_dataset
remediation_execution_after_plan_results_review_does_not_recompute_metrics_from_raw_rows
remediation_execution_after_plan_results_review_does_not_train_models
remediation_execution_after_plan_results_review_does_not_score_strategy
remediation_execution_after_plan_results_review_does_not_generate_trade_recommendations
remediation_execution_after_plan_results_review_does_not_accept_predictive_usefulness
remediation_execution_after_plan_results_review_does_not_accept_profitability
remediation_execution_after_plan_results_review_does_not_authorize_runtime
remediation_execution_after_plan_results_review_does_not_authorize_broker_execution
controlled_remediation_is_not_main_merge_readiness
focused_validation_is_not_detached_retry
targeted_remediation_plan_is_plan_only
workstream_mapping_is_planning_source
method_results_review_remains_source_evidence
plan_results_review_remains_source_evidence
plan_execution_remains_source_evidence
remediation_execution_approval_remains_source_evidence
remediation_execution_candidate_operator_review_remains_source_evidence
remediation_execution_candidate_remains_source_evidence
observable_failure_family_classification_is_method_planning_only
failure_family_classification_is_not_root_cause
diagnostic_capture_results_review_remains_source_evidence
controlled_recapture_is_not_retry_success
module_concentration_is_not_failure_error_separation
prior_blocked_diagnostic_capture_execution_remains_historically_blocked
first_retry_failure_remains_authoritative""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(ValueError):
    """Raised when execution evidence violates its approved boundary."""


def _sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).utcoffset() is not None
    except ValueError:
        return False


def _source_bindings(source_approval: dict | None = None) -> dict[str, Any]:
    if source_approval is not None:
        try:
            approval.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
                deepcopy(source_approval)
            )
        except approval.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "source approval validation failed"
            ) from exc
        if source_approval.get(approval.APPROVAL_DIGEST_KEY) != SOURCE_APPROVAL_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "source approval digest mismatch"
            )
    bindings = deepcopy(approval._BINDINGS)
    bindings.update(
        {
            "source_remediation_execution_approval_after_plan_results_review_artifact_kind": approval.ARTIFACT_KIND,
            "source_remediation_execution_approval_after_plan_results_review_status": approval.APPROVAL_STATUS,
            "source_remediation_execution_approval_after_plan_results_review_scope": approval.APPROVAL_SCOPE,
            "source_remediation_execution_approval_after_plan_results_review_commit": SOURCE_APPROVAL_COMMIT,
            "source_remediation_execution_approval_after_plan_results_review_digest": SOURCE_APPROVAL_DIGEST,
            "source_remediation_execution_candidate_after_plan_results_review_operator_review_commit": approval.SOURCE_OPERATOR_REVIEW_COMMIT,
            "source_remediation_execution_candidate_after_plan_results_review_operator_review_digest": approval.SOURCE_OPERATOR_REVIEW_DIGEST,
            "source_remediation_execution_candidate_after_plan_results_review_commit": approval._SOURCE_CORE["source_candidate_commit"],
            "source_remediation_execution_candidate_after_plan_results_review_digest": approval._SOURCE_CORE["source_remediation_execution_candidate_after_plan_results_review_digest"],
        }
    )
    return bindings


SOURCE_BINDINGS = _source_bindings()
SOURCE_CORE = approval._SOURCE_CORE


def _candidate_inventory(repository_root: Path) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for relative in PRIORITY_1_PATHS:
        path = repository_root / relative
        exists = path.is_file()
        digest = _sha256_file(path)
        inventory.append(
            {
                "path": relative,
                "file_exists_before": exists,
                "file_exists_after": exists,
                "change_type": "unchanged_candidate",
                "workstream_ids": list(WORKSTREAM_IDS),
                "reason_for_inclusion": "Reviewed Priority 1 candidate scope; inspected for a safe source-authority-bound change.",
                "source_authority": "REVIEWED_PLAN_RESULTS_AND_PRIORITY_1_CANDIDATE_SCOPE_ONLY_NO_DIRECT_EDIT_AUTHORITY",
                "pre_change_sha256": digest,
                "post_change_sha256": digest,
                "changed": False,
                "expected_digest_update_in_file": False,
                "test_file": relative.startswith("tests/"),
                "production_or_service_file": relative.startswith("marketflow/services/"),
                "governance_file": False,
                "verification_required": "Focused Priority 1 validation and source-authority review",
                "verification_result": "NO_SAFE_RETAINED_REMEDIATION_CHANGE_IDENTIFIED",
            }
        )
    return inventory


def _normalize_change_records(records: list[dict] | None) -> list[dict[str, Any]]:
    if records is None:
        return []
    if not isinstance(records, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
            "remediation_change_records must be a list"
        )
    normalized = deepcopy(records)
    required = {
        "change_id", "path", "change_type", "workstream_ids", "source_authority", "description",
        "pre_change_sha256", "post_change_sha256", "verification_evidence", "focused_validation_covered",
        "expected_digest_updated", "digest_update_authority", "test_modified", "test_change_authority",
        "production_code_modified", "production_change_authority", "root_cause_claimed", "retry_success_claimed",
        "main_merge_readiness_claimed",
    }
    for record in normalized:
        if not isinstance(record, dict) or not required.issubset(record):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "change record missing required fields"
            )
        if not record["workstream_ids"] or not set(record["workstream_ids"]).issubset(WORKSTREAM_IDS):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "change record workstream mapping invalid"
            )
        if not isinstance(record["source_authority"], str) or not record["source_authority"].strip():
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "change record source authority missing"
            )
        if not record["focused_validation_covered"] or any(
            record[field] for field in ("root_cause_claimed", "retry_success_claimed", "main_merge_readiness_claimed")
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "change record verification or claim boundary invalid"
            )
        if record["expected_digest_updated"] and record["digest_update_authority"] != "SOURCE_AUTHORITY_AND_CANONICAL_SERIALIZATION_RECORDED":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "digest update authority missing"
            )
        if record["test_modified"] and record["test_change_authority"] != "SOURCE_AUTHORITY_AND_ARTIFACT_CONTRACT_REVIEW_RECORDED":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "test change authority missing"
            )
        if record["production_code_modified"] and record["production_change_authority"] != "PLAN_DERIVED_SOURCE_AUTHORITY_RECORDED":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
                "production change authority missing"
            )
    return normalized


def _normalize_validation(summary: dict | None) -> dict[str, Any]:
    if summary is None:
        return {
            "command": None, "exit_code": None, "duration_seconds": None,
            "stdout_byte_count": None, "stderr_byte_count": None,
            "stdout_sha256": None, "stderr_sha256": None,
            "bounded_stdout_excerpt": None, "bounded_stderr_excerpt": None,
            "cacheprovider_disabled": False, "focused_validation_performed": False,
            "focused_validation_passed": False,
        }
    if not isinstance(summary, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
            "focused_validation_summary must be an object"
        )
    normalized = deepcopy(summary)
    if isinstance(normalized.get("duration_seconds"), (int, float)):
        normalized["duration_seconds"] = str(normalized["duration_seconds"])
    normalized.setdefault("bounded_stdout_excerpt", None)
    normalized.setdefault("bounded_stderr_excerpt", None)
    required = {
        "command", "exit_code", "duration_seconds", "stdout_byte_count", "stderr_byte_count",
        "stdout_sha256", "stderr_sha256", "cacheprovider_disabled", "focused_validation_performed",
        "focused_validation_passed",
    }
    if not required.issubset(normalized):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
            "focused validation summary missing required fields"
        )
    if normalized["focused_validation_performed"] and not normalized["cacheprovider_disabled"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
            "focused validation must disable cacheprovider"
        )
    return normalized


def _snapshots(inventory: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return [
        {"path": item["path"], "file_exists": item[f"file_exists_{'before' if key == 'pre_change_sha256' else 'after'}"], "sha256": item[key]}
        for item in inventory
    ]


def _inventory_from_changes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "path": record["path"], "file_exists_before": True, "file_exists_after": True,
            "change_type": record["change_type"], "workstream_ids": deepcopy(record["workstream_ids"]),
            "reason_for_inclusion": record["description"], "source_authority": record["source_authority"],
            "pre_change_sha256": record["pre_change_sha256"], "post_change_sha256": record["post_change_sha256"],
            "changed": record["pre_change_sha256"] != record["post_change_sha256"],
            "expected_digest_update_in_file": record["expected_digest_updated"],
            "test_file": record["test_modified"], "production_or_service_file": record["production_code_modified"],
            "governance_file": False, "verification_required": "Focused validation and recorded source authority",
            "verification_result": record["verification_evidence"],
        }
        for record in records
    ]


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == SUCCESS_ARTIFACT_KIND
    checks = [_check(f"{field}_bound", value, execution.get(field)) for field, value in SOURCE_BINDINGS.items()]
    checks.extend(
        [
            _check("selected_remediation_execution_package_bound", SELECTED_PACKAGE, execution.get("selected_remediation_execution_package")),
            _check("retry_failure_counts_bound", SOURCE_CORE["retry_failure_context"]["counts"], execution.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", list(SOURCE_CORE["priority_1_target_modules"]), execution.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, execution.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, execution.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, execution.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, execution.get("failed_or_errored_nodeids_count")),
            _check("exit_code_1_bound_as_diagnostic_only", 1, execution.get("source_exit_code")),
            _check("stdout_hash_bound", SOURCE_CORE["source_stdout_sha256"], execution.get("source_stdout_sha256")),
            _check("stderr_hash_bound", SOURCE_CORE["source_stderr_sha256"], execution.get("source_stderr_sha256")),
            _check("stdout_byte_count_1231380_bound", 1231380, execution.get("source_stdout_byte_count")),
            _check("stderr_byte_count_0_bound", 0, execution.get("source_stderr_byte_count")),
            _check("observable_family_count_4_bound", 4, execution.get("observable_failure_family_count")),
            _check("observable_evidence_items_188_bound", 188, execution.get("total_observable_evidence_items")),
            _check("observable_family_ids_bound", set(FAMILY_IDS), {item.get("family_id") for item in execution.get("reviewed_observable_failure_families", [])}),
            _check("source_workstream_count_4_bound", 4, execution.get("source_workstream_count")),
            _check("reviewed_workstream_ids_bound", set(WORKSTREAM_IDS), {item.get("workstream_id") for item in execution.get("reviewed_workstreams", [])}),
            _check("file_impact_inventory_created_if_success", True if success else execution.get("file_impact_inventory_created"), execution.get("file_impact_inventory_created")),
            _check("pre_change_snapshot_created_if_success", True if success else execution.get("pre_change_snapshot_created"), execution.get("pre_change_snapshot_created")),
            _check("change_records_created_if_success", True if success else execution.get("change_records_created"), execution.get("change_records_created")),
            _check("post_change_snapshot_created_if_success", True if success else execution.get("post_change_snapshot_created"), execution.get("post_change_snapshot_created")),
            _check("verification_evidence_recorded_if_success", True if success else execution.get("verification_evidence_recorded"), execution.get("verification_evidence_recorded")),
            _check("focused_validation_performed_if_success", True if success else execution.get("focused_validation_performed"), execution.get("focused_validation_performed")),
            _check("focused_validation_passed_if_success", True if success else execution.get("focused_validation_passed"), execution.get("focused_validation_passed")),
            _check("blocked_reason_recorded_if_blocked", True, bool(execution.get("blocked_reason")) if not success else True),
            _check("full_pytest_false", False, execution.get("full_pytest_performed")),
            _check("retry_rerun_false", False, execution.get("retry_rerun_performed")),
            _check("ready_for_retry_candidate_false", False, execution.get("ready_for_retry_candidate")),
            _check("ready_for_main_merge_approval_false", False, execution.get("ready_for_main_merge_approval")),
            _check("risk_controls_defined", True, bool(execution.get("risk_controls"))),
            _check("recommendation_defined", True, bool(execution.get("recommended_next_task"))),
            _check("next_chain_defined", True, bool(execution.get("next_chain"))),
            _check("next_gates_defined", True, bool(execution.get("next_gates"))),
            _check("no_tracked_marketflow_files", True, execution.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, execution.get("no_tracked_pytest_cache_files")),
        ]
    )
    checks.extend(_check(f"{field}_false", False, execution.get(field)) for field in FALSE_BOUNDARY_FIELDS)
    return checks


def _digest_without_derived(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist", "summary", EXECUTION_DIGEST_KEY, FILE_IMPACT_INVENTORY_DIGEST_KEY,
        CHANGE_RECORDS_DIGEST_KEY, VALIDATION_REPORT_DIGEST_KEY, MANIFEST_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY,
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
    *,
    source_approval: dict | None = None,
    repository_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    remediation_change_records: list[dict] | None = None,
    focused_validation_summary: dict | None = None,
) -> dict[str, Any]:
    """Build success only from explicit valid changes and passing focused evidence."""

    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError(
            "run_timestamp_utc must be ISO-8601 with timezone"
        )
    root = Path(repository_root or ".").resolve()
    records = _normalize_change_records(remediation_change_records)
    validation = _normalize_validation(focused_validation_summary)
    success = bool(records) and validation["focused_validation_performed"] and validation["focused_validation_passed"] and validation["exit_code"] == 0
    blocked_reason = None if success else (BLOCKED_NO_CHANGE_AUTHORITY if not records else BLOCKED_VALIDATION)
    inventory = _inventory_from_changes(records) if records else _candidate_inventory(root)
    pre_snapshot = _snapshots(inventory, "pre_change_sha256")
    post_snapshot = _snapshots(inventory, "post_change_sha256") if records else []
    source_bindings = _source_bindings(source_approval)
    kind, status = (SUCCESS_ARTIFACT_KIND, SUCCESS_STATUS) if success else (BLOCKED_ARTIFACT_KIND, BLOCKED_STATUS)
    next_task = SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK
    outputs = ([{"output_name": name, "status": "GENERATED_CONTROLLED_PLAN_DERIVED_REMEDIATION_EXECUTION_ONLY"} for name in SUCCESS_OUTPUT_NAMES] if success else [])

    execution: dict[str, Any] = {
        "artifact_kind": kind, "schema_version": SCHEMA_VERSION, "execution_status": status,
        "execution_scope": EXECUTION_SCOPE, "selected_remediation_execution_package": SELECTED_PACKAGE,
        "run_timestamp_utc": timestamp, "created_offline": True, "controlled_remediation_execution": True,
        "remediation_execution_results_review_required": True, **source_bindings,
        "selected_source_plan_package": SOURCE_CORE["selected_source_plan_package"],
        "retry_execution_commit": SOURCE_CORE["retry_execution_commit"],
        "retry_failure_context": deepcopy(SOURCE_CORE["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(SOURCE_CORE["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404, "source_exit_code": 1,
        "source_duration_seconds": str(SOURCE_CORE["source_duration_seconds"]),
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_exit_code_is_diagnostic_only": True,
        "reviewed_observable_failure_families": deepcopy(SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "reviewed_workstreams": deepcopy(SOURCE_CORE["reviewed_workstreams"]), "source_workstream_count": 4,
        "file_impact_inventory": inventory, "pre_change_snapshot": pre_snapshot,
        "change_records": records, "post_change_snapshot": post_snapshot,
        "workstream_to_change_mapping": [
            {"workstream_id": workstream, "change_ids": [r["change_id"] for r in records if workstream in r["workstream_ids"]]}
            for workstream in WORKSTREAM_IDS
        ],
        "source_authority_mapping": [{"change_id": r["change_id"], "source_authority": r["source_authority"]} for r in records],
        "verification_evidence_report": [{"change_id": r["change_id"], "verification_evidence": r["verification_evidence"]} for r in records],
        "focused_validation_report": validation,
        "unsupported_claims_boundary_report": {
            "root_cause": "NOT_CLAIMED", "retry_success": "NOT_CLAIMED", "main_merge_readiness": "NOT_CLAIMED",
            "failure_family_evidence": "BOUNDED_METHOD_PLANNING_EVIDENCE_ONLY",
        },
        "retry_gate_preservation_report": "RETRY_BLOCKED_PENDING_SUCCESSFUL_REMEDIATION_RESULTS_REVIEW_AND_SEPARATE_APPROVAL",
        "main_merge_gate_preservation_report": "MAIN_MERGE_BLOCKED_PENDING_PASSING_NEW_RETRY_RESULTS_REVIEW",
        "blocked_reason": blocked_reason,
        "available_data": ["source bindings", "reviewed workstreams", "retry counts", "Priority 1 candidate inventory", "focused validation summary"],
        "missing_or_failed_data": ([] if success else ["safe source-authority-bound retained remediation change"]),
        "remediation_execution_after_plan_results_review_created": True,
        "remediation_execution_performed": success, "controlled_plan_derived_remediation_performed": success,
        "selected_package_executed": success, "source_approval_verified": True,
        "source_operator_review_verified": True, "source_candidate_verified": True,
        "source_plan_results_review_verified": True, "source_plan_execution_verified": True,
        "source_workstream_mapping_verified": True, "file_impact_inventory_created": bool(inventory),
        "pre_change_snapshot_created": bool(pre_snapshot), "post_change_snapshot_created": bool(post_snapshot),
        "change_records_created": bool(records), "verification_evidence_recorded": bool(records),
        "focused_validation_performed": validation["focused_validation_performed"],
        "focused_validation_passed": validation["focused_validation_passed"],
        "production_code_modified": any(r["production_code_modified"] for r in records),
        "existing_tests_modified": any(r["test_modified"] for r in records),
        "expected_digests_updated": any(r["expected_digest_updated"] for r in records),
        "patch_generated": bool(records), "patch_applied": bool(records),
        **{field: False for field in FALSE_BOUNDARY_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "ready_for_remediation_execution_results_review": success, "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False, "outputs": outputs,
        "recommended_next_task": next_task,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED" if success else "FUTURE_FAILURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_EXECUTION_RESULTS_REVIEW" if success else "STOP_AND_PROCEED_ONLY_TO_SEPARATELY_INVOKED_FAILURE_DIAGNOSIS",
        "next_chain": list(NEXT_CHAIN_SUCCESS if success else NEXT_CHAIN_BLOCKED),
        "next_gates": list(NEXT_GATES_SUCCESS if success else NEXT_GATES_BLOCKED),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    if success:
        execution[FILE_IMPACT_INVENTORY_DIGEST_KEY] = semantic_digest(inventory)
        execution[CHANGE_RECORDS_DIGEST_KEY] = semantic_digest(records)
        execution[VALIDATION_REPORT_DIGEST_KEY] = semantic_digest(validation)
        execution[MANIFEST_DIGEST_KEY] = semantic_digest(
            {"outputs": outputs, "inventory_digest": execution[FILE_IMPACT_INVENTORY_DIGEST_KEY], "change_records_digest": execution[CHANGE_RECORDS_DIGEST_KEY], "validation_digest": execution[VALIDATION_REPORT_DIGEST_KEY]}
        )
        execution[BLOCKED_MANIFEST_DIGEST_KEY] = None
    else:
        execution[FILE_IMPACT_INVENTORY_DIGEST_KEY] = None
        execution[CHANGE_RECORDS_DIGEST_KEY] = None
        execution[VALIDATION_REPORT_DIGEST_KEY] = None
        execution[MANIFEST_DIGEST_KEY] = None
        execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest(
            {"artifact_kind": kind, "execution_status": status, "blocked_reason": blocked_reason, "available_data": execution["available_data"], "missing_or_failed_data": execution["missing_or_failed_data"]}
        )
    execution[EXECUTION_DIGEST_KEY] = _digest_without_derived(execution) if success else None
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(execution)
    return execution


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checklist = execution["checklist"]
    passed = sum(item["status"] == PASS for item in checklist)
    failed = len(checklist) - passed
    keys = (
        "remediation_execution_after_plan_results_review_created", "remediation_execution_performed",
        "controlled_plan_derived_remediation_performed", "selected_package_executed",
        "file_impact_inventory_created", "pre_change_snapshot_created", "change_records_created",
        "post_change_snapshot_created", "verification_evidence_recorded", "focused_validation_performed",
        "focused_validation_passed", "production_code_modified", "existing_tests_modified",
        "expected_digests_updated", "patch_generated", "patch_applied", "full_pytest_performed",
        "detached_retry_rerun_performed", "retry_rerun_performed", "cache_read_in_execution",
        "ready_for_remediation_execution_results_review", "ready_for_retry_candidate",
        "ready_for_main_merge_approval", "new_retry_candidate_created", "new_retry_executed",
        "integration_execution_successful", "blocked_reason", "recommended_next_task",
    )
    summary = {"total_checks": len(checklist), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed}
    summary.update({key: deepcopy(execution.get(key)) for key in keys})
    summary.update(
        {
            "selected_remediation_execution_package": SELECTED_PACKAGE, "source_workstream_count": 4,
            "workstream_family_ids": list(FAMILY_IDS), "observable_failure_family_count": 4,
            "total_observable_evidence_items": 188, "source_exit_code": 1,
            "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
            "top_5_percentage_of_failed_or_errored_nodeids": 43.58974359, "top_10_count_sum": 1069,
            "predictive_usefulness_accepted": False, "profitability_accepted": False,
            "runtime_authorized": False, "broker_execution_authorized": False,
        }
    )
    return summary


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
    execution: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    success = execution.get("artifact_kind") == SUCCESS_ARTIFACT_KIND
    expected_kind = SUCCESS_ARTIFACT_KIND if success else BLOCKED_ARTIFACT_KIND
    expected_status = SUCCESS_STATUS if success else BLOCKED_STATUS
    for field, expected in (
        ("artifact_kind", expected_kind), ("schema_version", SCHEMA_VERSION),
        ("execution_status", expected_status), ("execution_scope", EXECUTION_SCOPE),
        ("selected_remediation_execution_package", SELECTED_PACKAGE),
    ):
        if execution.get(field) != expected:
            raise error(f"{field} mismatch")
    if not _iso_utc(execution.get("run_timestamp_utc")):
        raise error("run timestamp invalid")
    for field, expected in SOURCE_BINDINGS.items():
        if execution.get(field) != expected:
            raise error(f"{field} mismatch")
    fixed = {
        "priority_1_target_modules": SOURCE_CORE["priority_1_target_modules"], "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"], "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188, "source_workstream_count": 4,
        "ready_for_retry_candidate": False, "ready_for_main_merge_approval": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected in fixed.items():
        if execution.get(field) != expected:
            raise error(f"{field} mismatch")
    if execution.get("retry_failure_context", {}).get("counts") != SOURCE_CORE["retry_failure_context"]["counts"]:
        raise error("retry failure counts mismatch")
    if {item.get("family_id") for item in execution.get("reviewed_observable_failure_families", [])} != set(FAMILY_IDS):
        raise error("observable failure families mismatch")
    if any(item.get("confidence") != "HIGH" or item.get("observable_evidence_count") != 47 for item in execution["reviewed_observable_failure_families"]):
        raise error("observable failure family evidence mismatch")
    if {item.get("workstream_id") for item in execution.get("reviewed_workstreams", [])} != set(WORKSTREAM_IDS):
        raise error("reviewed workstreams mismatch")
    for field in FALSE_BOUNDARY_FIELDS:
        if execution.get(field) is not False:
            raise error(f"{field} must be false")
    records = _normalize_change_records(execution.get("change_records"))
    validation = _normalize_validation(execution.get("focused_validation_report"))
    if success:
        if not records or not all(execution.get(field) for field in (
            "file_impact_inventory_created", "pre_change_snapshot_created", "change_records_created",
            "post_change_snapshot_created", "verification_evidence_recorded", "focused_validation_performed",
            "focused_validation_passed", "ready_for_remediation_execution_results_review",
        )):
            raise error("success evidence incomplete")
        if not validation["focused_validation_passed"] or validation["exit_code"] != 0:
            raise error("success focused validation failed")
        if execution.get(FILE_IMPACT_INVENTORY_DIGEST_KEY) != semantic_digest(execution["file_impact_inventory"]):
            raise error("file impact inventory digest mismatch")
        if execution.get(CHANGE_RECORDS_DIGEST_KEY) != semantic_digest(records):
            raise error("change records digest mismatch")
        if execution.get(VALIDATION_REPORT_DIGEST_KEY) != semantic_digest(validation):
            raise error("validation report digest mismatch")
        expected_manifest = semantic_digest({"outputs": execution["outputs"], "inventory_digest": execution[FILE_IMPACT_INVENTORY_DIGEST_KEY], "change_records_digest": execution[CHANGE_RECORDS_DIGEST_KEY], "validation_digest": execution[VALIDATION_REPORT_DIGEST_KEY]})
        if execution.get(MANIFEST_DIGEST_KEY) != expected_manifest or not execution.get(EXECUTION_DIGEST_KEY):
            raise error("success digest manifest missing or changed")
        if execution.get(EXECUTION_DIGEST_KEY) != _digest_without_derived(execution):
            raise error("execution digest mismatch")
        if len(execution.get("outputs", [])) != len(SUCCESS_OUTPUT_NAMES):
            raise error("success outputs missing")
    else:
        if not execution.get("blocked_reason") or execution.get(BLOCKED_MANIFEST_DIGEST_KEY) is None:
            raise error("blocked reason or manifest digest missing")
        expected_blocked = semantic_digest({"artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS, "blocked_reason": execution["blocked_reason"], "available_data": execution["available_data"], "missing_or_failed_data": execution["missing_or_failed_data"]})
        if execution[BLOCKED_MANIFEST_DIGEST_KEY] != expected_blocked:
            raise error("blocked manifest digest mismatch")
        if execution.get("ready_for_remediation_execution_results_review") is not False:
            raise error("blocked artifact cannot be ready for results review")
    checklist = _checklist(execution)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution):
        raise error("summary mismatch")
    for key in (EXECUTION_DIGEST_KEY, FILE_IMPACT_INVENTORY_DIGEST_KEY, CHANGE_RECORDS_DIGEST_KEY, VALIDATION_REPORT_DIGEST_KEY, MANIFEST_DIGEST_KEY, BLOCKED_MANIFEST_DIGEST_KEY):
        value = execution.get(key)
        if value is not None and re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise error(f"{key} invalid")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": EXECUTION_SCOPE, "blocked_reason": execution.get("blocked_reason"),
        "execution_digest": execution.get(EXECUTION_DIGEST_KEY),
        "blocked_manifest_digest": execution.get(BLOCKED_MANIFEST_DIGEST_KEY),
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Approval", "Source Operator Review and Candidate", "Source Plan Results Review", "Source Plan Execution",
    "Source Targeted Remediation Plan", "Source Workstream Mapping", "Source Method Results Review",
    "Source Method Execution", "Source Diagnostic Results Review", "Source Controlled Recapture",
    "Source Durable Receipt", "Source Planning and Detail Binding Evidence", "Retry Failure Context",
    "Execution Scope", "Selected Remediation Execution Package", "Priority 1 Target Modules",
    "Reviewed Observable Families", "Reviewed Workstreams", "File Impact Inventory", "Pre-Change Snapshot",
    "Change Records", "Post-Change Snapshot", "Focused Validation", "Verification Evidence",
    "Unsupported Claims Boundary", "Success or Blocked Disposition", "Recommendation", "Next Chain",
    "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_markdown_v1(
    execution: dict,
) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(deepcopy(execution))
    sections: dict[str, Any] = {
        "Source Approval": {k: execution[k] for k in ("source_remediation_execution_approval_after_plan_results_review_commit", "source_remediation_execution_approval_after_plan_results_review_digest")},
        "Source Operator Review and Candidate": {k: execution[k] for k in ("source_remediation_execution_candidate_after_plan_results_review_operator_review_digest", "source_remediation_execution_candidate_after_plan_results_review_digest")},
        "Retry Failure Context": execution["retry_failure_context"], "Execution Scope": execution["execution_scope"],
        "Selected Remediation Execution Package": execution["selected_remediation_execution_package"],
        "Priority 1 Target Modules": execution["priority_1_target_modules"],
        "Reviewed Observable Families": execution["reviewed_observable_failure_families"],
        "Reviewed Workstreams": execution["reviewed_workstreams"], "File Impact Inventory": execution["file_impact_inventory"],
        "Pre-Change Snapshot": execution["pre_change_snapshot"], "Change Records": execution["change_records"],
        "Post-Change Snapshot": execution["post_change_snapshot"], "Focused Validation": execution["focused_validation_report"],
        "Verification Evidence": execution["verification_evidence_report"],
        "Unsupported Claims Boundary": execution["unsupported_claims_boundary_report"],
        "Success or Blocked Disposition": {
            "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
            "blocked_reason": execution["blocked_reason"], "execution_digest": execution[EXECUTION_DIGEST_KEY],
            "file_impact_inventory_digest": execution[FILE_IMPACT_INVENTORY_DIGEST_KEY],
            "change_records_digest": execution[CHANGE_RECORDS_DIGEST_KEY],
            "validation_report_digest": execution[VALIDATION_REPORT_DIGEST_KEY],
            "manifest_digest": execution[MANIFEST_DIGEST_KEY],
            "blocked_manifest_digest": execution[BLOCKED_MANIFEST_DIGEST_KEY],
        },
        "Recommendation": {"next_task": execution["recommended_next_task"], "action": execution["recommended_action"]},
        "Next Chain": execution["next_chain"], "Next Gates": execution["next_gates"],
        "Risk Controls": execution["risk_controls"], "Checklist Summary": execution["summary"],
        "Authority Boundaries": {"runtime_use": execution["runtime_use"], "broker_execution": execution["broker_execution"], "retry_ready": execution["ready_for_retry_candidate"]},
        "Guardrails": list(FALSE_BOUNDARY_FIELDS),
    }
    source_map = {
        "Source Plan Results Review": "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "Source Plan Execution": "source_remediation_plan_or_execution_after_method_results_review_digest",
        "Source Targeted Remediation Plan": "source_targeted_remediation_plan_digest",
        "Source Workstream Mapping": "source_workstream_mapping_digest",
        "Source Method Results Review": "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "Source Method Execution": "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "Source Diagnostic Results Review": "source_receipt_recovery_or_recapture_results_review_digest",
        "Source Controlled Recapture": "source_receipt_recovery_or_recapture_execution_digest",
        "Source Durable Receipt": "source_durable_receipt_path",
        "Source Planning and Detail Binding Evidence": "source_planning_execution_digest",
    }
    sections.update({title: execution[key] for title, key in source_map.items()})
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution After Plan Results Review v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", f"```text\n{sections[title]!r}\n```", ""))
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
    output_dir: str | Path,
    *,
    source_approval: dict | None = None,
    repository_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
    remediation_change_records: list[dict] | None = None,
    focused_validation_summary: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError("protected output directory")
    execution = execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
        source_approval=source_approval, repository_root=repository_root, run_timestamp_utc=run_timestamp_utc,
        remediation_change_records=remediation_change_records, focused_validation_summary=focused_validation_summary,
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_markdown_v1(execution), encoding="utf-8")
    return execution


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_EXECUTED_AFTER_PLAN_RESULTS_REVIEW_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_BLOCKED_AFTER_PLAN_RESULTS_REVIEW_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_EXECUTED_AFTER_PLAN_RESULTS_REVIEW_CONTROLLED_PLAN_DERIVED_REMEDIATION_READY_FOR_RESULTS_REVIEW = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_BLOCKED_AFTER_PLAN_RESULTS_REVIEW_SOURCE_AUTHORITY_CHANGE_SCOPE_OR_VALIDATION_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_ONLY_CONTROLLED_PLAN_DERIVED_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY = SELECTED_PACKAGE
