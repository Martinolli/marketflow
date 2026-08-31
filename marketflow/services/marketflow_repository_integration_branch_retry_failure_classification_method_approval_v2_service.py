"""Approve the cache-supported classification method v2 for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2 = (
    ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE = "PACKAGE_CACHE_SUPPORTED_MODULE_LEVEL_NODEID_CLASSIFICATION_V2"
SOURCE_OPERATOR_REVIEW_DIGEST = "07a3a022dadaaba332ccae3a433bbe22dc6a8c432c4b2044fe800397df34a7f0"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE CLASSIFICATION METHOD V2 PACKAGE_CACHE_SUPPORTED_MODULE_LEVEL_NODEID_CLASSIFICATION_V2 "
    "MARKETFLOW CACHE SUPPORTED MODULE LEVEL NODEID CLASSIFICATION ONLY NO FAILURE ERROR SEPARATION "
    "NO FIRST ORDER CLAIMS NO RETRY NO FULL PYTEST NO RESULTS REVIEW NO MAIN PUSH "
    "CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
OPERATOR_DECISION = "APPROVE_CLASSIFICATION_METHOD_V2"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_attestation_v1"
)
APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY = (
    "APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY"
)
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_cache_counts",
    "operator_confirms_module_summary", "operator_confirms_classification_source_limitations",
    "operator_confirms_approval_scope_only", "operator_confirms_no_v2_execution",
    "operator_confirms_no_classification_execution", "operator_confirms_no_failure_modules_classified",
    "operator_confirms_no_error_modules_classified", "operator_confirms_no_first_failure_claim",
    "operator_confirms_no_first_error_claim", "operator_confirms_no_failure_error_separation_claim",
    "operator_confirms_no_traceback_root_cause_claim", "operator_confirms_no_cache_read",
    "operator_confirms_no_retry", "operator_confirms_no_full_pytest",
    "operator_confirms_no_diagnostic_command", "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review", "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_integration_digest", "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push", "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete", "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation", "operator_confirms_no_evidence_regeneration",
    "operator_confirms_no_marketflow_commit", "operator_confirms_no_pytest_cache_commit",
    "operator_confirms_no_provider_requests", "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized", "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

APPROVED_FUTURE_V2_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "requirement_value": requirement_value,
        "approval_status": APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
    }
    for requirement_id, requirement_value in source.source.FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS.items()
]
APPROVED_FUTURE_V2_EXECUTION_PLAN = [
    {
        "step_id": f"future_v2_execution_step_{index:02d}",
        "source_step": step,
        "approval_status": APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.source.FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN, start=1)
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": output_id, "authorization_status": "AUTHORIZED_NOT_GENERATED"}
    for output_id in source.source.PLANNED_OUTPUT_NAMES
]
SUPPORTING_PACKAGE_STATUSES = {
    "PACKAGE_CACHE_SUPPORTED_MODULE_GROUPING_WITH_EVIDENCE_ROOT_HINTS_V2": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CACHE_SUPPORTED_PATH_CWD_AND_DIGEST_HINTS_V2": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CACHE_SUPPORTED_MODULE_GROUPING_PLUS_LIMITATION_REPORT_V2": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_CACHE_PLUS_DIAGNOSTIC_OUTPUT_ENRICHMENT_V2": "AVAILABLE_NOT_SELECTED_HIGH_CONTROL",
}
SUPPORTING_PACKAGES = [
    {"package_id": package_id, "approval_status": status}
    for package_id, status in SUPPORTING_PACKAGE_STATUSES.items()
]
BLOCKED_PACKAGES = [
    {"package_id": package_id, "approval_status": "BLOCKED_NOT_APPROVED"}
    for package_id in (
        "PACKAGE_FAILURE_ERROR_SEPARATION_FROM_CACHE_ONLY_V2",
        "PACKAGE_FIRST_ORDER_TRACE_ANALYSIS_FROM_CACHE_ONLY_V2",
        "PACKAGE_NEW_RETRY_WITHOUT_CLASSIFICATION_V2",
        "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY_V2",
    )
]
NEXT_CHAIN = [
    "Classification Method Execution v2, if separately invoked.",
    "Classification Method Results Review v2.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "classification_method_execution_v2_if_approved", "classification_method_results_review_v2",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "approval_v2_does_not_execute_classification", "approval_v2_does_not_read_cache",
    "approval_v2_does_not_run_retry", "approval_v2_does_not_run_full_pytest",
    "approval_v2_does_not_run_diagnostic_commands", "approval_v2_does_not_claim_failure_error_separation",
    "approval_v2_does_not_claim_first_failure", "approval_v2_does_not_claim_first_error",
    "approval_v2_does_not_claim_traceback_root_cause", "approval_v2_does_not_use_cache_as_retry_success_evidence",
    "approval_v2_does_not_create_new_retry_candidate", "approval_v2_does_not_create_retry_results_review",
    "approval_v2_does_not_create_integration_results_review", "approval_v2_does_not_mark_integration_successful",
    "approval_v2_does_not_generate_successful_integration_digest", "approval_v2_does_not_push_integration_branch",
    "approval_v2_does_not_push_main", "approval_v2_does_not_delete_integration_branch",
    "approval_v2_does_not_delete_worktree", "approval_v2_does_not_force_push",
    "approval_v2_does_not_prune_remotes", "approval_v2_does_not_modify_tags",
    "approval_v2_does_not_commit_marketflow_outputs", "approval_v2_does_not_commit_pytest_cache",
    "approval_v2_does_not_modify_staged_evidence", "approval_v2_does_not_regenerate_evidence",
    "approval_v2_does_not_call_providers", "approval_v2_does_not_acquire_market_data",
    "approval_v2_does_not_regenerate_dataset", "approval_v2_does_not_recompute_metrics",
    "approval_v2_does_not_train_models", "approval_v2_does_not_score_strategy",
    "approval_v2_does_not_generate_recommendations", "approval_v2_does_not_accept_predictive_usefulness",
    "approval_v2_does_not_accept_profitability", "approval_v2_does_not_authorize_runtime",
    "approval_v2_does_not_authorize_broker_execution", "selected_v2_package_approved_for_future_execution_only",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_v2_execution_required", "separate_v2_results_review_required",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound", "source_candidate_v2_digest_bound", "source_reentry_digest_bound",
    "source_results_review_digest_bound", "source_cache_manifest_digest_bound", "retry_execution_commit_bound",
    "retry_failure_counts_bound", "cache_source_counts_bound", "module_summary_bound",
    "classification_source_limits_bound", "operator_decision_matches", "operator_attestation_phrase_matches",
    "approval_scope_only", "selected_package_module_level_nodeid_v2", "approval_created_true",
    "method_v2_selected_true", "method_v2_approved_true", "method_v2_authorized_true",
    "ready_for_method_v2_execution_true", "method_v2_executed_false", "classification_execution_created_false",
    "classification_execution_performed_false", "failure_modules_classified_false", "error_modules_classified_false",
    "first_failure_identified_false", "first_error_identified_false", "failure_error_separation_claimed_false",
    "traceback_root_cause_claimed_false", "new_retry_candidate_created_false", "new_retry_executed_false",
    "new_retry_results_review_created_false", "main_merge_approval_created_false", "retry_rerun_false",
    "full_pytest_false", "diagnostic_command_false", "diagnostic_output_false", "integration_success_false",
    "successful_integration_digest_false", "integration_branch_pushed_false", "main_push_false",
    "origin_main_modified_false", "marketflow_outputs_committed_false", "pytest_cache_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "requirements_approved_for_future_execution",
    "future_plan_approved_not_executed", "planned_outputs_authorized_not_generated",
    "supporting_packages_not_selected", "blocked_packages_not_approved", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(ValueError):
    """Raised when approval evidence, attestation, or boundaries are invalid."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() is not None


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_v2_digest": source.SOURCE_CANDIDATE_V2_DIGEST,
        "operator_confirms_source_reentry_digest": source.source.SOURCE_REENTRY_DIGEST,
        "operator_confirms_source_results_review_digest": source.source.SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_source_cache_manifest_digest": source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST,
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
                f"{field} mismatch"
            )
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "operator_attestation_timestamp_utc invalid"
        )
    reference = attestation.get("operator_reference")
    if not isinstance(reference, str) or not reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "operator_reference missing"
        )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
                f"{field} must be true"
            )


def build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_attestation(
    *, operator_reference: str, operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str, operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_v2_digest: str, operator_confirms_source_reentry_digest: str,
    operator_confirms_source_results_review_digest: str, operator_confirms_source_cache_manifest_digest: str,
    operator_confirms_retry_execution_commit: str, operator_confirms_retry_failure_counts: bool,
    operator_confirms_cache_counts: bool, operator_confirms_module_summary: bool,
    operator_confirms_classification_source_limitations: bool,
    operator_confirms_selected_v2_package: str, operator_confirms_approval_scope_only: bool,
    operator_confirms_no_v2_execution: bool, operator_confirms_no_classification_execution: bool,
    operator_confirms_no_failure_modules_classified: bool, operator_confirms_no_error_modules_classified: bool,
    operator_confirms_no_first_failure_claim: bool, operator_confirms_no_first_error_claim: bool,
    operator_confirms_no_failure_error_separation_claim: bool, operator_confirms_no_traceback_root_cause_claim: bool,
    operator_confirms_no_cache_read: bool, operator_confirms_no_retry: bool,
    operator_confirms_no_full_pytest: bool, operator_confirms_no_diagnostic_command: bool,
    operator_confirms_no_retry_results_review: bool, operator_confirms_no_integration_results_review: bool,
    operator_confirms_no_integration_success: bool, operator_confirms_no_successful_integration_digest: bool,
    operator_confirms_no_integration_branch_push: bool, operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool, operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool, operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_evidence_regeneration: bool, operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_pytest_cache_commit: bool, operator_confirms_no_provider_requests: bool,
    operator_confirms_no_market_data_acquisition: bool, operator_confirms_no_dataset_generation: bool,
    operator_confirms_no_metric_recomputation: bool, operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool, operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool, operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool, operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_classification_method_v2_package: str = SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the exact non-secret operator attestation."""
    attestation = {name: value for name, value in locals().items()}
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(attestation)
    return attestation


def _committed_source_fields() -> dict[str, Any]:
    return {
        "source_classification_method_candidate_v2_operator_review_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_V1,
        "source_classification_method_candidate_v2_operator_review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_READY,
        "source_classification_method_candidate_v2_operator_review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_classification_method_candidate_v2_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        **source._committed_source_fields(),
    }


def _source_fields(source_review: dict | None) -> dict[str, Any]:
    if source_review is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review(
        source_review
    )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_method_candidate_v2_operator_review_artifact_kind": "artifact_kind",
        "source_classification_method_candidate_v2_operator_review_status": "review_status",
        "source_classification_method_candidate_v2_operator_review_scope": "review_scope",
        "source_classification_method_candidate_v2_operator_review_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_operator_review_digest",
    }
    for target, field in mapping.items():
        fields[target] = deepcopy(source_review.get(field))
    for field in set(fields) - set(mapping):
        if field in source_review:
            fields[field] = deepcopy(source_review[field])
    return fields


def _base_approval(source_fields: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "operator_attestation_digest": semantic_digest(attestation),
        **deepcopy(dict(source_fields)),
        "classification_source_valid_for_v2_candidate": True,
        "classification_source_accepted_for_module_level_only": True,
        "classification_source_not_accepted_for_failure_error_separation": True,
        "classification_source_not_accepted_for_first_order_failure_analysis": True,
        "classification_source_not_accepted_for_traceback_root_cause": True,
        "classification_source_not_retry_success_evidence": True,
        "classification_method_v2_selected": True, "classification_method_v2_approved": True,
        "classification_method_v2_authorized": True, "classification_method_v2_approval_created": True,
        "ready_for_classification_method_v2_execution": True,
        "classification_method_v2_executed": False, "classification_execution_created": False,
        "classification_execution_performed": False, "failure_modules_classified": False,
        "error_modules_classified": False, "first_failure_identified": False,
        "first_error_identified": False, "failure_error_separation_claimed": False,
        "first_order_failure_analysis_claimed": False, "traceback_root_cause_claimed": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "integration_results_review_created": False,
        "main_merge_approval_created": False, "retry_rerun_performed": False,
        "full_pytest_performed": False, "diagnostic_command_executed": False,
        "diagnostic_output_captured": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "pytest_cache_committed": False, "evidence_regenerated": False,
        "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "selected_v2_package": {
            "package_id": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
            "approval_status": APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
            "selected": True, "approved": True, "authorized_for_future_execution": True, "executed": False,
        },
        "approved_future_v2_requirements": deepcopy(APPROVED_FUTURE_V2_REQUIREMENTS),
        "approved_future_v2_execution_plan": deepcopy(APPROVED_FUTURE_V2_EXECUTION_PLAN),
        "future_v2_plan_approval_status": APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
        "future_v2_plan_execution_status": "NOT_EXECUTED",
        "planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES), "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True, "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation") if isinstance(approval.get("operator_attestation"), dict) else {}
    retry_counts = [approval.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    source_limits = [
        approval.get("classification_source_accepted_for_module_level_only"),
        approval.get("classification_source_not_accepted_for_failure_error_separation"),
        approval.get("classification_source_not_accepted_for_first_order_failure_analysis"),
        approval.get("classification_source_not_accepted_for_traceback_root_cause"),
        approval.get("classification_source_not_retry_success_evidence"),
    ]
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_classification_method_candidate_v2_operator_review_digest")),
        "source_candidate_v2_digest_bound": (source.SOURCE_CANDIDATE_V2_DIGEST, approval.get("source_classification_method_candidate_v2_digest")),
        "source_reentry_digest_bound": (source.source.SOURCE_REENTRY_DIGEST, approval.get("source_classification_method_reentry_digest")),
        "source_results_review_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_DIGEST, approval.get("source_classification_source_results_review_digest")),
        "source_cache_manifest_digest_bound": (source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, approval.get("source_cache_manifest_review_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", approval.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], retry_counts),
        "cache_source_counts_bound": ([1404, 26288], [approval.get("lastfailed_cache_entry_count"), approval.get("nodeids_cache_entry_count")]),
        "module_summary_bound": ([29, [136, 131, 122, 112, 111]], [approval.get("module_summary_module_count"), approval.get("largest_module_nodeid_counts")]),
        "classification_source_limits_bound": ([True] * 5, source_limits),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_module_level_nodeid_v2": (SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE, approval.get("selected_classification_method_v2_package")),
        "approval_created_true": (True, approval.get("classification_method_v2_approval_created")),
        "method_v2_selected_true": (True, approval.get("classification_method_v2_selected")),
        "method_v2_approved_true": (True, approval.get("classification_method_v2_approved")),
        "method_v2_authorized_true": (True, approval.get("classification_method_v2_authorized")),
        "ready_for_method_v2_execution_true": (True, approval.get("ready_for_classification_method_v2_execution")),
        "method_v2_executed_false": (False, approval.get("classification_method_v2_executed")),
        "classification_execution_created_false": (False, approval.get("classification_execution_created")),
        "classification_execution_performed_false": (False, approval.get("classification_execution_performed")),
        "failure_modules_classified_false": (False, approval.get("failure_modules_classified")),
        "error_modules_classified_false": (False, approval.get("error_modules_classified")),
        "first_failure_identified_false": (False, approval.get("first_failure_identified")),
        "first_error_identified_false": (False, approval.get("first_error_identified")),
        "failure_error_separation_claimed_false": (False, approval.get("failure_error_separation_claimed")),
        "traceback_root_cause_claimed_false": (False, approval.get("traceback_root_cause_claimed")),
        "new_retry_candidate_created_false": (False, approval.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, approval.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, approval.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, approval.get("main_merge_approval_created")),
        "retry_rerun_false": (False, approval.get("retry_rerun_performed")),
        "full_pytest_false": (False, approval.get("full_pytest_performed")),
        "diagnostic_command_false": (False, approval.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, approval.get("diagnostic_output_captured")),
        "integration_success_false": (False, approval.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [approval.get("successful_integration_execution_digest_generated"), approval.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, approval.get("integration_branch_pushed")),
        "main_push_false": (False, approval.get("main_push_performed")),
        "origin_main_modified_false": (False, approval.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, approval.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, approval.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, approval.get("evidence_regenerated")),
        "provider_requests_false": (False, approval.get("provider_requests_made_in_approval")),
        "market_data_acquisition_false": (False, approval.get("market_data_acquisition_performed_in_approval")),
        "dataset_generation_false": (False, approval.get("dataset_generation_performed_in_approval")),
        "metric_recomputation_false": (False, approval.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, approval.get("model_training_performed")),
        "strategy_scoring_false": (False, approval.get("strategy_scoring_performed")),
        "recommendations_false": (False, approval.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_V2_REQUIREMENTS, approval.get("approved_future_v2_requirements")),
        "future_plan_approved_not_executed": ([APPROVED_FUTURE_V2_EXECUTION_PLAN, "NOT_EXECUTED"], [approval.get("approved_future_v2_execution_plan"), approval.get("future_v2_plan_execution_status")]),
        "planned_outputs_authorized_not_generated": (AUTHORIZED_PLANNED_OUTPUTS, approval.get("planned_outputs")),
        "supporting_packages_not_selected": (SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        "blocked_packages_not_approved": (BLOCKED_PACKAGES, approval.get("blocked_packages")),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "no_tracked_marketflow_files": (True, approval.get("no_tracked_marketflow_files")),
        "no_tracked_pytest_cache_files": (True, approval.get("no_tracked_pytest_cache_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "classification_method_v2_selected": True, "classification_method_v2_approved": True,
        "classification_method_v2_authorized": True, "classification_method_v2_approval_created": True,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "ready_for_classification_method_v2_execution": True, "method_v2_executed": False,
        "classification_execution_performed": False, "new_retry_candidate_created": False,
        "new_retry_executed": False, "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic approval digest."""
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build future-only approval from committed evidence and an exact attestation."""
    if not isinstance(operator_attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "operator_attestation must be an object"
        )
    _validate_attestation(operator_attestation)
    approval = _base_approval(_source_fields(source_review), operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest"] = (
        marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest_v1(approval)
    )
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(approval)
    return approval


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
    approval: dict,
) -> dict:
    """Validate the exact approval while rejecting any execution or broader authority."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "approval must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_classification_method_v2_package": SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        **_committed_source_fields(),
        "approved_future_v2_requirements": APPROVED_FUTURE_V2_REQUIREMENTS,
        "approved_future_v2_execution_plan": APPROVED_FUTURE_V2_EXECUTION_PLAN,
        "future_v2_plan_approval_status": APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
        "future_v2_plan_execution_status": "NOT_EXECUTED", "planned_outputs": AUTHORIZED_PLANNED_OUTPUTS,
        "supporting_packages": SUPPORTING_PACKAGES, "blocked_packages": BLOCKED_PACKAGES,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(approval.get(field), expected, field)
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "operator_attestation missing"
        )
    _validate_attestation(attestation)
    _expect(approval.get("operator_attestation_digest"), semantic_digest(attestation), "operator_attestation_digest")
    required_true = (
        "created_offline", "governance_only", "operator_attestation_required",
        "classification_source_valid_for_v2_candidate", "classification_source_accepted_for_module_level_only",
        "classification_source_not_accepted_for_failure_error_separation",
        "classification_source_not_accepted_for_first_order_failure_analysis",
        "classification_source_not_accepted_for_traceback_root_cause",
        "classification_source_not_retry_success_evidence", "retry_pytest_first_result_authoritative",
        "root_full_regression_does_not_override_detached_retry_failure", "classification_method_v2_selected",
        "classification_method_v2_approved", "classification_method_v2_authorized",
        "classification_method_v2_approval_created", "ready_for_classification_method_v2_execution",
        "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
    )
    required_false = (
        "root_full_regression_is_retry_evidence", "classification_method_v2_executed",
        "classification_execution_created", "classification_execution_performed", "failure_modules_classified",
        "error_modules_classified", "first_failure_identified", "first_error_identified",
        "failure_error_separation_claimed", "first_order_failure_analysis_claimed", "traceback_root_cause_claimed",
        "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
        "integration_results_review_created", "main_merge_approval_created", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
        "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
        "evidence_regenerated", "provider_requests_made_in_approval",
        "market_data_acquisition_performed_in_approval", "dataset_generation_performed_in_approval",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
    )
    for field in required_true:
        _expect(approval.get(field), True, field)
    for field in required_false:
        _expect(approval.get(field), False, field)
    _expect(approval.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(approval.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approval.get(field), NOT_AUTHORIZED, field)
    selected = approval.get("selected_v2_package")
    if not isinstance(selected, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "selected_v2_package missing"
        )
    _expect(selected.get("package_id"), SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE, "selected package")
    _expect(selected.get("approval_status"), APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY, "selected package status")
    _expect([selected.get(field) for field in ("selected", "approved", "authorized_for_future_execution", "executed")], [True, True, True, False], "selected package states")
    checklist = approval.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(approval), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "checklist failed"
        )
    _expect(approval.get("summary"), _summary(checklist), "summary")
    digest = approval.get("marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "approval digest missing"
        )
    _expect(digest, marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest_v1(approval), "approval digest")
    return {
        "status": approval["approval_status"], "artifact_kind": approval["artifact_kind"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest": digest,
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_markdown_v1(
    approval: dict,
) -> str:
    """Render the validated approval as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(approval)
    attestation = approval["operator_attestation"]
    sections = [
        ("Operator Attestation", [f"Reference/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_version']}`.", f"Decision: `{attestation['operator_decision']}`.", "The non-secret attestation is digest-bound."]),
        ("Source Operator Review", [f"Digest: `{approval['source_classification_method_candidate_v2_operator_review_digest']}`."]),
        ("Source Candidate v2", [f"Digest: `{approval['source_classification_method_candidate_v2_digest']}`."]),
        ("Source Classification-Source Review", [f"Results-review digest: `{approval['source_classification_source_results_review_digest']}`.", f"Cache-manifest digest: `{approval['source_cache_manifest_review_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The failed retry remains authoritative."]),
        ("Approval Scope", ["Future Classification Method Execution v2 only; no execution, retry, results review, or main merge is created."]),
        ("Selected v2 Package", [f"`{SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE}`: `{APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY}`."]),
        ("Approved Future v2 Requirements", [f"`{row['requirement_id']}`: `{row['approval_status']}`" for row in approval["approved_future_v2_requirements"]]),
        ("Approved Future v2 Execution Plan", [f"`{row['step_id']}`: `{row['approval_status']}` / `{row['execution_status']}`" for row in approval["approved_future_v2_execution_plan"]]),
        ("Planned Outputs", [f"`{row['output_id']}`: `{row['authorization_status']}`" for row in approval["planned_outputs"]]),
        ("Supporting Packages", [f"`{row['package_id']}`: `{row['approval_status']}`" for row in approval["supporting_packages"]]),
        ("Blocked Packages", [f"`{row['package_id']}`: `{row['approval_status']}`" for row in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]), ("Next Gates", [f"`{row}`" for row in approval["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in approval["risk_controls"]]),
        ("Authority Boundaries", ["No cache read, classification, retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Cache evidence supports module/node grouping only.", "A separate execution task is required before any classification output may be generated."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Classification Method Approval v2", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
    output_dir: str | Path, *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
