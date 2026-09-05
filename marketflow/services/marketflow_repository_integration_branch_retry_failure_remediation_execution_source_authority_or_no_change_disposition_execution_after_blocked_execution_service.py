"""Execute approved source-authority enrichment planning after blocked remediation."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_service
    as source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTED_AFTER_BLOCKED_EXECUTION_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_BLOCKED_AFTER_BLOCKED_EXECUTION_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTED_AFTER_BLOCKED_EXECUTION_SOURCE_AUTHORITY_ENRICHMENT_PLAN_READY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_BLOCKED_AFTER_BLOCKED_EXECUTION_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_ONLY_SOURCE_AUTHORITY_ENRICHMENT_PLANNING_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
SOURCE_APPROVAL_COMMIT = "c88d4c238224a5c532d07374ab191e8b8b859af5"
SOURCE_APPROVAL_DIGEST = "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_FAILURE_DIAGNOSIS_V1"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"
GENERATED_PLANNING_ONLY = "GENERATED_SOURCE_AUTHORITY_ENRICHMENT_PLANNING_ONLY"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_digest"
ENRICHMENT_PLAN_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_enrichment_plan_digest"
MISSING_AUTHORITY_INVENTORY_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_missing_authority_inventory_digest"
WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_workstream_authority_mapping_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_blocked_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTED_AFTER_BLOCKED_EXECUTION_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_BLOCKED_AFTER_BLOCKED_EXECUTION_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTED_AFTER_BLOCKED_EXECUTION_SOURCE_AUTHORITY_ENRICHMENT_PLAN_READY = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_BLOCKED_AFTER_BLOCKED_EXECUTION_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_ONLY_SOURCE_AUTHORITY_ENRICHMENT_PLANNING_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION = SELECTED_PACKAGE


WORKSTREAM_REQUIREMENTS = {
    "assertion_value_mismatch_workstream": (
        "canonical source-of-truth for expected and actual values",
        "artifact contract proving which value is authoritative",
        "evidence needed to show a source value is wrong",
        "evidence needed to show a test expectation is wrong",
        "impacted files or artifact fields that would require future review",
        "backward-compatibility requirements",
        "focused verification required before any future change",
        "current evidence does not authorize direct value or assertion changes",
    ),
    "digest_hash_boundary_workstream": (
        "canonical payload source", "canonical serialization method",
        "digest input-boundary definition", "digest manifest field requirements",
        "proof required before any digest constant update",
        "proof required before any expected hash update",
        "old and new digest traceability requirements if future change is approved",
        "current evidence does not authorize digest updates",
    ),
    "fixture_isolation_determinism_workstream": (
        "evidence required to prove shared-state leakage", "fixture lifecycle and isolation authority",
        "deterministic timestamp, path, CWD, and seed authority",
        "temp path and worktree boundary requirements", "mutation and isolation verification requirements",
        "focused validation requirements", "current evidence does not authorize fixture or test rewrites",
    ),
    "schema_field_contract_workstream": (
        "canonical schema or artifact field contract", "required versus optional field authority",
        "export-surface authority", "backward-compatible alias requirements",
        "field addition or removal authority requirements", "validation requirements",
        "current evidence does not authorize schema or export redesign",
    ),
}

WORKSTREAM_SOURCES = (
    ("assertion_value_mismatch_workstream", "assertion_or_value_mismatch"),
    ("digest_hash_boundary_workstream", "digest_or_hash_mismatch"),
    ("fixture_isolation_determinism_workstream", "fixture_or_test_isolation_issue"),
    ("schema_field_contract_workstream", "missing_or_unexpected_field"),
)

NO_CHANGE_REQUIREMENTS = (
    "current-root Priority 1 passing state", "detached retry failed state",
    "explanation why current-root pass is not retry evidence",
    "confirmation that no source-authority-bound remediation exists",
    "evidence needed to decide whether no change is acceptable",
    "required results review before no-change retry criteria",
    "no-change disposition is not created by this task",
)
ALTERNATE_DIAGNOSTIC_REQUIREMENTS = (
    "diagnostic scope tied to detached retry failures or context mismatch", "command boundary",
    "cache boundary", "output capture requirements", "redaction requirements",
    "no full pytest unless separately approved", "no retry unless separately approved",
    "alternate diagnostics are not executed by this task",
)
RETRY_BASIS_REQUIREMENTS = (
    "reviewed source-authority enrichment results review",
    "approved remediation basis, approved no-change disposition, or approved alternate diagnostic result",
    "separate retry candidate", "separate retry approval", "separate retry execution",
    "separate retry results review", "main merge only after passing retry results review",
)

OUTPUT_IDS = tuple(
    """source_authority_or_no_change_disposition_execution_after_blocked_execution_manifest
source_approval_binding_report
source_operator_review_binding_report
source_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_report
priority1_validation_disposition_report
workstream_authority_gap_report
source_authority_enrichment_plan
missing_authority_inventory
workstream_to_missing_authority_mapping
canonical_serialization_authority_requirements
schema_field_contract_authority_requirements
fixture_isolation_authority_requirements
no_change_disposition_input_requirements
alternate_diagnostic_input_requirements
retry_basis_requirements
unsupported_claims_boundary_report
results_review_requirements_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)

SUCCESS_NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Results Review After Blocked Execution v1.",
    "Conditional source-authority acquisition, no-change disposition, alternate diagnostic, remediation execution, no-change retry criteria, or hold candidate only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
BLOCKED_NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Execution After Blocked Execution Failure Diagnosis v1.",
    "Alternate approved path only after review.", "No retry or main merge.",
)
SUCCESS_NEXT_GATES = tuple(
    """source_authority_or_no_change_disposition_results_review_after_blocked_execution
conditional_follow_on_candidate_if_results_review_supports
source_authority_acquisition_candidate_if_needed
no_change_disposition_candidate_if_needed
alternate_diagnostic_candidate_if_needed
remediation_execution_candidate_if_needed
no_change_retry_criteria_candidate_if_needed
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)
BLOCKED_NEXT_GATES = (
    "source_authority_or_no_change_disposition_execution_after_blocked_execution_failure_diagnosis",
    "alternate_approved_path_only_after_review", "retry_and_main_merge_remain_blocked",
)

RISK_CONTROLS = tuple(
    """execution_after_blocked_execution_uses_approved_package_only
execution_after_blocked_execution_is_source_authority_enrichment_planning_only
execution_after_blocked_execution_does_not_acquire_external_source_authority
execution_after_blocked_execution_does_not_execute_no_change_disposition
execution_after_blocked_execution_does_not_execute_alternate_diagnostics
execution_after_blocked_execution_does_not_execute_remediation
execution_after_blocked_execution_does_not_modify_production_code
execution_after_blocked_execution_does_not_modify_existing_tests
execution_after_blocked_execution_does_not_update_expected_digests
execution_after_blocked_execution_does_not_generate_patch
execution_after_blocked_execution_does_not_apply_patch
execution_after_blocked_execution_does_not_run_pytest
execution_after_blocked_execution_does_not_run_full_pytest
execution_after_blocked_execution_does_not_rerun_priority1_validation
execution_after_blocked_execution_does_not_rerun_retry
execution_after_blocked_execution_does_not_rerun_detached_retry
execution_after_blocked_execution_does_not_parse_durable_receipt
execution_after_blocked_execution_does_not_analyze_diagnostic_output
execution_after_blocked_execution_does_not_rerun_plan_execution
execution_after_blocked_execution_does_not_regenerate_targeted_plan
execution_after_blocked_execution_does_not_rerun_method_execution
execution_after_blocked_execution_does_not_rerun_controlled_recapture
execution_after_blocked_execution_does_not_run_diagnostic_command
execution_after_blocked_execution_does_not_read_pytest_cache
execution_after_blocked_execution_does_not_modify_pytest_cache
execution_after_blocked_execution_does_not_parse_terminal_logs
execution_after_blocked_execution_does_not_parse_operator_logs
execution_after_blocked_execution_does_not_inspect_env
execution_after_blocked_execution_does_not_reconstruct_prior_lost_values
execution_after_blocked_execution_does_not_reconstruct_full_streams
execution_after_blocked_execution_does_not_classify_modules_again
execution_after_blocked_execution_does_not_classify_full_retry_failures
execution_after_blocked_execution_does_not_classify_full_retry_errors
execution_after_blocked_execution_does_not_claim_failure_error_separation
execution_after_blocked_execution_does_not_identify_authoritative_first_failure
execution_after_blocked_execution_does_not_identify_authoritative_first_error
execution_after_blocked_execution_does_not_claim_traceback_root_cause
execution_after_blocked_execution_does_not_claim_root_cause
execution_after_blocked_execution_does_not_claim_retry_success
execution_after_blocked_execution_does_not_claim_main_merge_readiness
execution_after_blocked_execution_does_not_create_remediation_execution
execution_after_blocked_execution_does_not_create_remediation_execution_results_review
execution_after_blocked_execution_does_not_create_new_retry_candidate
execution_after_blocked_execution_does_not_create_retry_approval
execution_after_blocked_execution_does_not_create_retry_execution
execution_after_blocked_execution_does_not_create_retry_results_review
execution_after_blocked_execution_does_not_create_integration_results_review
execution_after_blocked_execution_does_not_mark_integration_successful
execution_after_blocked_execution_does_not_generate_successful_integration_digest
execution_after_blocked_execution_does_not_push_integration_branch
execution_after_blocked_execution_does_not_push_main
execution_after_blocked_execution_does_not_delete_integration_branch
execution_after_blocked_execution_does_not_delete_worktree
execution_after_blocked_execution_does_not_force_push
execution_after_blocked_execution_does_not_prune_remotes
execution_after_blocked_execution_does_not_modify_tags
execution_after_blocked_execution_does_not_modify_staged_evidence
execution_after_blocked_execution_does_not_regenerate_evidence
execution_after_blocked_execution_does_not_call_providers
execution_after_blocked_execution_does_not_acquire_market_data
execution_after_blocked_execution_does_not_generate_dataset
execution_after_blocked_execution_does_not_recompute_metrics
execution_after_blocked_execution_does_not_train_models
execution_after_blocked_execution_does_not_score_strategy
execution_after_blocked_execution_does_not_generate_trade_recommendations
execution_after_blocked_execution_does_not_accept_predictive_usefulness
execution_after_blocked_execution_does_not_accept_profitability
execution_after_blocked_execution_does_not_authorize_runtime
execution_after_blocked_execution_does_not_authorize_broker_execution
source_authority_enrichment_plan_is_not_remediation
source_authority_enrichment_plan_is_not_source_authority_acquisition
missing_authority_inventory_is_not_change_authority
no_change_inputs_are_not_no_change_disposition
alternate_diagnostic_inputs_are_not_diagnostic_execution
retry_basis_requirements_are_not_retry_readiness
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_approval_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_results_review_required_after_execution
separate_approval_required_before_any_follow_on_execution
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
    """source_authority_or_no_change_disposition_execution_after_blocked_execution_created
source_authority_or_no_change_disposition_execution_performed
selected_package_executed
source_authority_enrichment_plan_created
missing_authority_inventory_created
workstream_to_missing_authority_mapping_created
source_evidence_requirements_created
canonical_serialization_requirements_created
schema_field_contract_requirements_created
fixture_isolation_evidence_requirements_created
no_change_disposition_input_requirements_created
alternate_diagnostic_input_requirements_created
retry_basis_requirements_created
source_approval_verified
source_operator_review_verified
source_candidate_verified
source_failure_diagnosis_verified
source_blocked_execution_verified
source_blocked_reason_verified
source_workstreams_verified
priority1_validation_disposition_preserved
detached_retry_failed_status_preserved
ready_for_source_authority_or_no_change_disposition_results_review""".splitlines()
)
FALSE_FIELDS = tuple(
    """source_authority_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
retained_change_records_available
source_authority_enrichment_performed_as_evidence_acquisition
no_change_disposition_performed
alternate_diagnostic_execution_performed
remediation_execution_performed
controlled_plan_derived_remediation_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
pytest_performed_in_execution
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
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
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
retry_approval_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated
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
trade_recommendations_generated""".splitlines()
)

SOURCE_BINDINGS = {
    **deepcopy(source.SOURCE_BINDINGS),
    "source_approval_commit": SOURCE_APPROVAL_COMMIT,
    "source_approval_digest": SOURCE_APPROVAL_DIGEST,
}

PRIORITY_1_MODULES = (
    ("tests/test_marketflow_signal_or_feature_generation_results_review_service.py", 136),
    ("tests/test_post_identity_freeze_registry_inventory_approval_service.py", 131),
    ("tests/test_corporate_action_authority_plan_candidate_service.py", 122),
    ("tests/test_feature_generation_results_review_redesigned_labels_service.py", 112),
    ("tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", 111),
)


class MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityExecutionError(ValueError):
    """Raised when execution source or output violates the frozen contract."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _committed_source_approval() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        source.APPROVAL_DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        "source_authority_or_no_change_disposition_package_selected": True,
        "source_authority_or_no_change_disposition_package_approved": True,
        "source_authority_or_no_change_disposition_package_authorized": True,
        "ready_for_source_authority_or_no_change_disposition_execution_after_blocked_execution": True,
        "source_authority_or_no_change_disposition_execution_performed": False,
        "source_authority_enrichment_performed": False,
        **deepcopy(source.SOURCE_BINDINGS),
    }


def _source_reasons(candidate: Any) -> list[str]:
    if not isinstance(candidate, Mapping):
        return ["SOURCE_APPROVAL_NOT_AN_OBJECT"]
    expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "approval_status": source.APPROVAL_STATUS,
        "approval_scope": source.APPROVAL_SCOPE,
        source.APPROVAL_DIGEST_KEY: SOURCE_APPROVAL_DIGEST,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        **source.SOURCE_BINDINGS,
    }
    reasons = [f"SOURCE_APPROVAL_{field.upper()}_MISMATCH" for field, value in expected.items() if candidate.get(field) != value]
    for field in (
        "source_authority_or_no_change_disposition_package_selected",
        "source_authority_or_no_change_disposition_package_approved",
        "source_authority_or_no_change_disposition_package_authorized",
        "ready_for_source_authority_or_no_change_disposition_execution_after_blocked_execution",
    ):
        if candidate.get(field) is not True:
            reasons.append(f"SOURCE_APPROVAL_{field.upper()}_NOT_TRUE")
    for field in ("source_authority_or_no_change_disposition_execution_performed", "source_authority_enrichment_performed"):
        if candidate.get(field) is not False:
            reasons.append(f"SOURCE_APPROVAL_{field.upper()}_NOT_FALSE")
    return reasons


def _families() -> list[dict[str, Any]]:
    return [
        {"family_id": family, "observable_evidence_count": 47, "confidence": "HIGH", "planning_evidence_only": True}
        for _, family in WORKSTREAM_SOURCES
    ]


def _workstreams() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "source_family_id": family, "source_observable_evidence_count": 47,
         "source_family_confidence": "HIGH", "planning_evidence_only": True, "direct_change_authorized": False}
        for workstream, family in WORKSTREAM_SOURCES
    ]


def _inventory() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "authority_status": "MISSING_NOT_ACQUIRED",
         "missing_authority_items": list(requirements), "direct_change_authorized": False}
        for workstream, requirements in WORKSTREAM_REQUIREMENTS.items()
    ]


def _mapping() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "source_family_id": family,
         "missing_authority_items": list(WORKSTREAM_REQUIREMENTS[workstream]),
         "mapping_status": "PLANNED_NOT_EXECUTED", "source_authority_acquired": False}
        for workstream, family in WORKSTREAM_SOURCES
    ]


def _evidence_requirements() -> list[dict[str, Any]]:
    return [
        {"workstream_id": workstream, "required_evidence": list(requirements),
         "evidence_status": "REQUIRED_NOT_ACQUIRED", "future_review_required": True}
        for workstream, requirements in WORKSTREAM_REQUIREMENTS.items()
    ]


def _enrichment_plan() -> dict[str, Any]:
    return {
        "package_id": SELECTED_PACKAGE,
        "plan_status": "SOURCE_AUTHORITY_ENRICHMENT_PLAN_READY_FOR_RESULTS_REVIEW",
        "planning_only": True,
        "source_authority_acquisition_performed": False,
        "workstream_sections": list(WORKSTREAM_REQUIREMENTS),
        "execution_steps": [
            "Bind committed approval and reviewed source evidence.",
            "Inventory missing authority for each reviewed workstream.",
            "Map each workstream to explicit missing authority and evidence requirements.",
            "Define canonical serialization, schema, fixture, no-change, and alternate-diagnostic inputs.",
            "Define the reviewed basis required before any retry candidate.",
            "Require a separate results review before any follow-on candidate or execution.",
        ],
        "success_boundary": "PLANNING_OUTPUTS_CREATED_WITHOUT_ACQUIRING_SOURCE_AUTHORITY_OR_EXECUTING_REMEDIATION",
    }


def _common(timestamp: str) -> dict[str, Any]:
    source_core = source.source.source.SOURCE_CORE
    return {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
        "created_offline": True, "governance_only": True,
        "source_authority_enrichment_planning_only": True,
        "source_authority_or_no_change_disposition_results_review_required": True,
        "run_timestamp_utc": timestamp,
        "source_approval_artifact_kind": source.ARTIFACT_KIND,
        "source_approval_status": source.APPROVAL_STATUS,
        "source_approval_scope": source.APPROVAL_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "historical_selected_remediation_execution_package": source.source.source.source.source.SELECTED_PACKAGE,
        "primary_failure_class": source.source.source.SOURCE_BINDINGS["source_blocked_reason"],
        "secondary_failure_classes": list(source.source.source.source.SECONDARY_FAILURE_CLASSES),
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
                                  "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": [
            {"module_path": path, "failed_or_errored_nodeid_count": count} for path, count in PRIORITY_1_MODULES
        ],
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "priority1_validation_summary": {
            "pre_change_passed": True, "pre_change_passed_count": 675,
            "post_change_passed": True, "post_change_passed_count": 675,
            "post_change_duration_seconds": "41.88", "post_change_stdout_byte_count": 832,
            "post_change_stderr_byte_count": 0,
            "post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
            "post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "not_retry_evidence": True,
        },
        "diagnostic_capture_evidence_summary": {
            "exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380,
            "stderr_byte_count": 0, "combined_output_byte_count": 1231380,
            "stdout_sha256": source_core["source_stdout_sha256"], "stderr_sha256": source_core["source_stderr_sha256"],
            "stdout_excerpt_truncated": True, "stderr_excerpt_truncated": False,
            "redaction_checked": True, "diagnostic_only": True,
        },
        "reviewed_observable_failure_families": _families(),
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "reviewed_workstreams": _workstreams(), "source_workstream_count": 4,
        "risk_controls": list(RISK_CONTROLS),
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }


def _success(common: dict[str, Any]) -> dict[str, Any]:
    plan, inventory, mapping = _enrichment_plan(), _inventory(), _mapping()
    evidence = _evidence_requirements()
    execution = {
        **common, "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        **{field: True for field in TRUE_FIELDS},
        "source_authority_enrichment_plan": plan,
        "missing_authority_inventory": inventory,
        "workstream_to_missing_authority_mapping": mapping,
        "source_evidence_requirements": evidence,
        "canonical_serialization_authority_requirements": list(WORKSTREAM_REQUIREMENTS["digest_hash_boundary_workstream"]),
        "schema_field_contract_authority_requirements": list(WORKSTREAM_REQUIREMENTS["schema_field_contract_workstream"]),
        "fixture_isolation_authority_requirements": list(WORKSTREAM_REQUIREMENTS["fixture_isolation_determinism_workstream"]),
        "no_change_disposition_input_requirements": list(NO_CHANGE_REQUIREMENTS),
        "alternate_diagnostic_input_requirements": list(ALTERNATE_DIAGNOSTIC_REQUIREMENTS),
        "retry_basis_requirements": list(RETRY_BASIS_REQUIREMENTS),
        "unsupported_claims_boundary": [
            "No external source authority was acquired.", "No root cause was established.",
            "No remediation or no-change disposition was executed.", "No retry or main-merge readiness was created.",
        ],
        "results_review_requirements": [
            "validate all generated planning structures and digests",
            "review each missing-authority requirement before selecting a follow-on path",
            "preserve remediation, retry, and main-merge gates until separately approved",
        ],
        "outputs_generated": [{"output_id": output_id, "status": GENERATED_PLANNING_ONLY} for output_id in OUTPUT_IDS],
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION",
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "blocked_reason": None,
    }
    execution[ENRICHMENT_PLAN_DIGEST_KEY] = semantic_digest(plan)
    execution[MISSING_AUTHORITY_INVENTORY_DIGEST_KEY] = semantic_digest(inventory)
    execution[WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY] = semantic_digest(mapping)
    execution["digest_manifest"] = {
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        ENRICHMENT_PLAN_DIGEST_KEY: execution[ENRICHMENT_PLAN_DIGEST_KEY],
        MISSING_AUTHORITY_INVENTORY_DIGEST_KEY: execution[MISSING_AUTHORITY_INVENTORY_DIGEST_KEY],
        WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY: execution[WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    }
    execution[MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = None
    return execution


def _blocked(common: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    blocked_reason = ";".join(dict.fromkeys(reasons))
    execution = {
        **common, "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        **{field: False for field in TRUE_FIELDS},
        "source_authority_or_no_change_disposition_execution_after_blocked_execution_created": True,
        "source_authority_enrichment_plan": None, "missing_authority_inventory": [],
        "workstream_to_missing_authority_mapping": [], "source_evidence_requirements": [],
        "canonical_serialization_authority_requirements": [], "schema_field_contract_authority_requirements": [],
        "fixture_isolation_authority_requirements": [], "no_change_disposition_input_requirements": [],
        "alternate_diagnostic_input_requirements": [], "retry_basis_requirements": [],
        "unsupported_claims_boundary": [], "results_review_requirements": [], "outputs_generated": [],
        "available_data": ["committed source approval constants", "reviewed source bindings", "retry counts",
                           "Priority 1 validation facts", "reviewed workstream facts"],
        "missing_or_failed_data": list(dict.fromkeys(reasons)), "blocked_reason": blocked_reason,
        "recommended_next_task": BLOCKED_NEXT_TASK, "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "DIAGNOSE_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE_BEFORE_ANY_FOLLOW_ON",
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        ENRICHMENT_PLAN_DIGEST_KEY: None, MISSING_AUTHORITY_INVENTORY_DIGEST_KEY: None,
        WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY: None, MANIFEST_DIGEST_KEY: None,
        "digest_manifest": None,
    }
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest({
        "blocked_reason": blocked_reason, "source_approval_commit": SOURCE_APPROVAL_COMMIT,
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
        "missing_or_failed_data": execution["missing_or_failed_data"],
    })
    return execution


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", value, execution.get(field)) for field, value in SOURCE_BINDINGS.items()]
    fixed = {
        "artifact_kind": SUCCESS_ARTIFACT_KIND if success else BLOCKED_ARTIFACT_KIND,
        "execution_status": SUCCESS_STATUS if success else BLOCKED_STATUS, "execution_scope": EXECUTION_SCOPE,
        "schema_version": SCHEMA_VERSION, "selected_package": SELECTED_PACKAGE,
        "retry_failure_counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "priority_1_total_612": 612, "top_10_total_1069": 1069, "module_summary_count_29": 29,
        "failed_or_errored_nodeids_1404": 1404, "observable_family_count_4": 4,
        "observable_evidence_items_188": 188, "workstream_count_4": 4,
    }
    actual = {
        "artifact_kind": execution.get("artifact_kind"), "execution_status": execution.get("execution_status"),
        "execution_scope": execution.get("execution_scope"), "schema_version": execution.get("schema_version"),
        "selected_package": execution.get("selected_source_authority_or_no_change_disposition_package"),
        "retry_failure_counts": execution.get("retry_failure_context", {}).get("counts"),
        "priority_1_total_612": execution.get("priority_1_total_nodeids"),
        "top_10_total_1069": execution.get("top_10_count_sum"),
        "module_summary_count_29": execution.get("module_summary_module_count"),
        "failed_or_errored_nodeids_1404": execution.get("failed_or_errored_nodeids_count"),
        "observable_family_count_4": execution.get("observable_failure_family_count"),
        "observable_evidence_items_188": execution.get("total_observable_evidence_items"),
        "workstream_count_4": execution.get("source_workstream_count"),
    }
    checks.extend(_check(name, expected, actual[name]) for name, expected in fixed.items())
    checks.extend(_check(f"{field}_{'true' if success else 'false'}", success, execution.get(field)) for field in TRUE_FIELDS)
    if not success:
        checks[-len(TRUE_FIELDS)] = _check("execution_created_true_if_blocked", True, execution.get("source_authority_or_no_change_disposition_execution_after_blocked_execution_created"))
    checks.extend(_check(f"{field}_false", False, execution.get(field)) for field in FALSE_FIELDS)
    checks.extend((
        _check("families_bound", _families(), execution.get("reviewed_observable_failure_families")),
        _check("workstreams_bound", _workstreams(), execution.get("reviewed_workstreams")),
        _check("risk_controls_defined", list(RISK_CONTROLS), execution.get("risk_controls")),
        _check("next_chain_defined", list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN), execution.get("next_chain")),
        _check("next_gates_defined", list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES), execution.get("next_gates")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, execution.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, execution.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, execution.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, execution.get("broker_execution")),
        _check("no_tracked_marketflow_files", True, execution.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, execution.get("no_tracked_pytest_cache_files")),
    ))
    if success:
        checks.extend((
            _check("source_authority_enrichment_plan", _enrichment_plan(), execution.get("source_authority_enrichment_plan")),
            _check("missing_authority_inventory", _inventory(), execution.get("missing_authority_inventory")),
            _check("workstream_authority_mapping", _mapping(), execution.get("workstream_to_missing_authority_mapping")),
            _check("source_evidence_requirements", _evidence_requirements(), execution.get("source_evidence_requirements")),
            _check("no_change_inputs", list(NO_CHANGE_REQUIREMENTS), execution.get("no_change_disposition_input_requirements")),
            _check("alternate_diagnostic_inputs", list(ALTERNATE_DIAGNOSTIC_REQUIREMENTS), execution.get("alternate_diagnostic_input_requirements")),
            _check("retry_basis_requirements", list(RETRY_BASIS_REQUIREMENTS), execution.get("retry_basis_requirements")),
            _check("outputs_generated", [{"output_id": item, "status": GENERATED_PLANNING_ONLY} for item in OUTPUT_IDS], execution.get("outputs_generated")),
        ))
    else:
        checks.extend((
            _check("blocked_reason_recorded", True, bool(execution.get("blocked_reason"))),
            _check("blocked_manifest_digest_generated", True, isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str)),
            _check("blocked_outputs_empty", [], execution.get("outputs_generated")),
        ))
    return checks


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]], success: bool) -> dict[str, Any]:
    failed = sum(item["status"] != PASS for item in checklist)
    fields = TRUE_FIELDS + FALSE_FIELDS
    summary = {"total_checks": len(checklist), "passed_checks": len(checklist) - failed,
               "failed_checks": failed, "blocker_count": failed,
               **{field: execution.get(field) for field in fields},
               "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
               "source_workstream_count": 4, "observable_failure_family_count": 4,
               "total_observable_evidence_items": 188, "source_exit_code": 1,
               "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
               "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
               "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
               "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
               "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
               "predictive_usefulness_accepted": False, "profitability_accepted": False,
               "runtime_authorized": False, "broker_execution_authorized": False}
    if not success:
        summary["blocked_reason"] = execution.get("blocked_reason")
    return summary


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
    *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Create planning outputs only; never acquire authority or execute remediation."""

    timestamp = "2026-08-23T00:00:00Z" if run_timestamp_utc is None else run_timestamp_utc
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityExecutionError("run timestamp invalid")
    candidate = _committed_source_approval() if source_approval is None else deepcopy(source_approval)
    reasons = _source_reasons(candidate)
    execution = _success(_common(timestamp)) if not reasons else _blocked(_common(timestamp), reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
    execution: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityExecutionError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, status = False, BLOCKED_STATUS
    else:
        raise error("artifact kind invalid")
    fixed = {"execution_status": status, "execution_scope": EXECUTION_SCOPE, "schema_version": SCHEMA_VERSION,
             "selected_source_authority_or_no_change_disposition_package": SELECTED_PACKAGE,
             "source_approval_artifact_kind": source.ARTIFACT_KIND, "source_approval_status": source.APPROVAL_STATUS,
             "source_approval_scope": source.APPROVAL_SCOPE, **SOURCE_BINDINGS}
    for field, expected in fixed.items():
        if execution.get(field) != expected:
            raise error(f"{field} mismatch")
    for field in ("created_offline", "governance_only", "source_authority_enrichment_planning_only",
                  "source_authority_or_no_change_disposition_results_review_required"):
        if execution.get(field) is not True:
            raise error(f"{field} must be true")
    if any(execution.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed execution boundary opened")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(execution.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime or trading boundary changed")
    expected_evidence = _common(execution.get("run_timestamp_utc"))
    evidence_fields = (
        "retry_failure_context", "priority_1_target_modules", "priority_1_top_module_count",
        "priority_1_total_nodeids", "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "module_summary_module_count", "failed_or_errored_nodeids_count", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families",
        "observable_failure_family_count", "total_observable_evidence_items", "reviewed_workstreams",
        "source_workstream_count", "primary_failure_class", "secondary_failure_classes",
        "historical_selected_remediation_execution_package", "risk_controls",
    )
    for field in evidence_fields:
        if execution.get(field) != expected_evidence[field]:
            raise error(f"{field} mismatch")
    if success:
        if any(execution.get(field) is not True for field in TRUE_FIELDS):
            raise error("success fact missing")
        content = {
            "source_authority_enrichment_plan": _enrichment_plan(), "missing_authority_inventory": _inventory(),
            "workstream_to_missing_authority_mapping": _mapping(), "source_evidence_requirements": _evidence_requirements(),
            "canonical_serialization_authority_requirements": list(WORKSTREAM_REQUIREMENTS["digest_hash_boundary_workstream"]),
            "schema_field_contract_authority_requirements": list(WORKSTREAM_REQUIREMENTS["schema_field_contract_workstream"]),
            "fixture_isolation_authority_requirements": list(WORKSTREAM_REQUIREMENTS["fixture_isolation_determinism_workstream"]),
            "no_change_disposition_input_requirements": list(NO_CHANGE_REQUIREMENTS),
            "alternate_diagnostic_input_requirements": list(ALTERNATE_DIAGNOSTIC_REQUIREMENTS),
            "retry_basis_requirements": list(RETRY_BASIS_REQUIREMENTS),
            "outputs_generated": [{"output_id": item, "status": GENERATED_PLANNING_ONLY} for item in OUTPUT_IDS],
            "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
            "recommended_next_task": SUCCESS_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        }
        for field, expected in content.items():
            if execution.get(field) != expected:
                raise error(f"{field} mismatch")
        digest_checks = {
            ENRICHMENT_PLAN_DIGEST_KEY: semantic_digest(execution["source_authority_enrichment_plan"]),
            MISSING_AUTHORITY_INVENTORY_DIGEST_KEY: semantic_digest(execution["missing_authority_inventory"]),
            WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY: semantic_digest(execution["workstream_to_missing_authority_mapping"]),
            MANIFEST_DIGEST_KEY: semantic_digest(execution.get("digest_manifest")),
        }
        for field, expected in digest_checks.items():
            if execution.get(field) != expected or re.fullmatch(r"[0-9a-f]{64}", str(expected)) is None:
                raise error(f"{field} mismatch")
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) is not None or execution.get("blocked_reason") is not None:
            raise error("success carries blocked evidence")
    else:
        if execution.get("source_authority_or_no_change_disposition_execution_after_blocked_execution_created") is not True:
            raise error("blocked execution record not created")
        if any(execution.get(field) is not False for field in TRUE_FIELDS[1:]):
            raise error("blocked artifact claims execution success")
        if any(execution.get(field) not in (None, []) for field in (
            "source_authority_enrichment_plan", "missing_authority_inventory", "workstream_to_missing_authority_mapping",
            "source_evidence_requirements", "outputs_generated")):
            raise error("blocked artifact generated planning outputs")
        if not execution.get("blocked_reason") or not execution.get("missing_or_failed_data"):
            raise error("blocked reason missing")
        expected_blocked = semantic_digest({
            "blocked_reason": execution["blocked_reason"], "source_approval_commit": SOURCE_APPROVAL_COMMIT,
            "source_approval_digest": SOURCE_APPROVAL_DIGEST,
            "missing_or_failed_data": execution["missing_or_failed_data"],
        })
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) != expected_blocked:
            raise error("blocked manifest mismatch")
        if any(execution.get(field) is not None for field in (
            ENRICHMENT_PLAN_DIGEST_KEY, MISSING_AUTHORITY_INVENTORY_DIGEST_KEY,
            WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY, MANIFEST_DIGEST_KEY)):
            raise error("blocked artifact carries success digest")
        if execution.get("next_chain") != list(BLOCKED_NEXT_CHAIN) or execution.get("next_gates") != list(BLOCKED_NEXT_GATES):
            raise error("blocked next path mismatch")
        if execution.get("recommended_next_task") != BLOCKED_NEXT_TASK:
            raise error("blocked recommendation mismatch")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution, checklist, success):
        raise error("summary mismatch")
    digest = execution.get(EXECUTION_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _execution_digest(execution):
        raise error("execution digest mismatch")
    return {"artifact_kind": kind, "execution_status": status, "execution_scope": EXECUTION_SCOPE,
            "execution_digest": digest, **{key: execution["summary"][key] for key in
            ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


MARKDOWN_SECTIONS = (
    "Source Approval", "Source Operator Review", "Source Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Remediation Execution Approval",
    "Source Plan Results Review", "Source Plan Execution", "Source Targeted Remediation Plan",
    "Source Workstream Mapping", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Execution Scope", "Selected Source Authority Package",
    "Source Authority Enrichment Plan", "Missing Authority Inventory", "Workstream to Missing Authority Mapping",
    "Source Evidence Requirements", "No-Change Disposition Input Requirements",
    "Alternate Diagnostic Input Requirements", "Retry Basis Requirements", "Unsupported Claims Boundary",
    "Success or Blocked Disposition", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_markdown_v1(
    execution: dict,
) -> str:
    """Render a validated human-readable execution record."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(deepcopy(execution))
    source_sections = {
        "Source Approval": {"commit": execution["source_approval_commit"], "digest": execution["source_approval_digest"]},
        "Source Operator Review": {k: execution[k] for k in ("source_operator_review_commit", "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest")},
        "Source Candidate": {k: execution[k] for k in ("source_candidate_commit", "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest")},
        "Source Failure Diagnosis": {k: execution[k] for k in ("source_failure_diagnosis_commit", "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest")},
        "Source Blocked Execution": {k: execution[k] for k in ("source_blocked_execution_commit", "source_blocked_manifest_digest")},
        "Blocked Reason": execution["source_blocked_reason"],
        "Failure Classification": {"primary": execution["primary_failure_class"], "secondary": execution["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {k: execution[k] for k in ("source_remediation_execution_approval_after_plan_results_review_commit", "source_remediation_execution_approval_after_plan_results_review_digest")},
        "Source Plan Results Review": {k: v for k, v in execution.items() if "plan_results_review" in k},
        "Source Plan Execution": {k: v for k, v in execution.items() if "plan_execution" in k},
        "Source Targeted Remediation Plan": execution["source_targeted_remediation_plan_digest"],
        "Source Workstream Mapping": execution["source_workstream_mapping_digest"],
        "Source Method Results Review": {k: v for k, v in execution.items() if "method_results_review" in k},
        "Source Method Execution": {k: v for k, v in execution.items() if "method_execution" in k},
        "Source Diagnostic Results Review": {k: v for k, v in execution.items() if "recapture_results_review" in k or "payload_review" in k or "durable_receipt_review" in k},
        "Source Controlled Recapture": {k: v for k, v in execution.items() if "recapture_execution" in k or "recapture_payload_digest" in k or "recapture_receipt_digest" in k},
        "Source Durable Receipt": {"path": execution["source_durable_receipt_path"], "parsed": execution["diagnostic_receipt_parsed_in_execution"]},
        "Source Planning and Detail Binding Evidence": {k: v for k, v in execution.items() if any(token in k for token in ("planning_digest", "detail_binding", "complete_29", "materialized_payload", "recovery_detail", "module_grouping", "staged_inventory"))},
    }
    sections = {
        **source_sections, "Retry Failure Context": execution["retry_failure_context"],
        "Priority 1 Target Modules": execution["priority_1_target_modules"],
        "Priority 1 Validation Summary": execution["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": execution["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": execution["reviewed_observable_failure_families"],
        "Reviewed Workstreams": execution["reviewed_workstreams"], "Execution Scope": execution["execution_scope"],
        "Selected Source Authority Package": execution["selected_source_authority_or_no_change_disposition_package"],
        "Source Authority Enrichment Plan": execution["source_authority_enrichment_plan"],
        "Missing Authority Inventory": execution["missing_authority_inventory"],
        "Workstream to Missing Authority Mapping": execution["workstream_to_missing_authority_mapping"],
        "Source Evidence Requirements": execution["source_evidence_requirements"],
        "No-Change Disposition Input Requirements": execution["no_change_disposition_input_requirements"],
        "Alternate Diagnostic Input Requirements": execution["alternate_diagnostic_input_requirements"],
        "Retry Basis Requirements": execution["retry_basis_requirements"],
        "Unsupported Claims Boundary": execution["unsupported_claims_boundary"],
        "Success or Blocked Disposition": {"artifact_kind": execution["artifact_kind"], "status": execution["execution_status"], "blocked_reason": execution["blocked_reason"], "execution_digest": execution[EXECUTION_DIGEST_KEY]},
        "Recommendation": {"next_task": execution["recommended_next_task"], "status": execution["recommended_next_task_status"], "action": execution["recommended_action"]},
        "Next Chain": execution["next_chain"], "Next Gates": execution["next_gates"],
        "Risk Controls": execution["risk_controls"],
        "Authority Boundaries": {field: execution[field] for field in FALSE_FIELDS},
        "Checklist Summary": execution["summary"],
        "Guardrails": [field for field in FALSE_FIELDS if execution[field] is False],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Execution After Blocked Execution v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
    output_dir: str | Path, *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Write the deterministic execution status document."""

    execution = execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
        source_approval=source_approval, run_timestamp_utc=run_timestamp_utc
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_markdown_v1(execution), encoding="utf-8")
    return execution


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "SELECTED_PACKAGE", "EXECUTION_DIGEST_KEY", "ENRICHMENT_PLAN_DIGEST_KEY",
    "MISSING_AUTHORITY_INVENTORY_DIGEST_KEY", "WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "BLOCKED_MANIFEST_DIGEST_KEY", "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_markdown_v1",
]
