"""Approve one retry-failure classification method for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_operator_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SELECTED_RETRY_FAILURE_METHOD_PACKAGE = source.source.RECOMMENDED_PACKAGE
SOURCE_OPERATOR_REVIEW_DIGEST = "cf541e8681724e1018cf0c343daf718a3a50249e3bdf8640c54d88791427f0be"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE INTEGRATION BRANCH RETRY FAILURE "
    "METHOD PACKAGE_CLASSIFY_RETRY_FAILURE_DOMAINS_FROM_AUTHORITATIVE_OUTPUT "
    "MARKETFLOW CLASSIFY AUTHORITATIVE RETRY FAILURE DOMAINS NO RETRY NO FULL PYTEST "
    "NO RESULTS REVIEW NO MAIN PUSH "
    "RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
OPERATOR_DECISION = "APPROVE_INTEGRATION_BRANCH_RETRY_FAILURE_METHOD"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_attestation_v1"
)
APPROVED_FOR_FUTURE_EXECUTION_ONLY = "APPROVED_FOR_FUTURE_RETRY_FAILURE_METHOD_EXECUTION_ONLY"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts",
    "operator_confirms_root_regression_not_retry_evidence",
    "operator_confirms_approval_scope_only",
    "operator_confirms_no_method_execution",
    "operator_confirms_no_diagnostic_execution",
    "operator_confirms_no_retry",
    "operator_confirms_no_full_pytest",
    "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review",
    "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_integration_digest",
    "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push",
    "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete",
    "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation",
    "operator_confirms_no_evidence_regeneration",
    "operator_confirms_no_marketflow_commit",
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
    "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

APPROVED_FUTURE_METHOD_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "requirement_value": requirement_value,
        "approval_status": APPROVED_FOR_FUTURE_EXECUTION_ONLY,
    }
    for requirement_id, requirement_value in source.source.FUTURE_METHOD_REQUIREMENTS.items()
]
APPROVED_FUTURE_METHOD_PLAN = [
    {
        "step_id": f"step_{index:02d}",
        "source_step": step,
        "approval_status": APPROVED_FOR_FUTURE_EXECUTION_ONLY,
        "execution_status": "NOT_EXECUTED",
    }
    for index, step in enumerate(source.source.FUTURE_METHOD_PLAN, start=1)
]
AUTHORIZED_PLANNED_OUTPUTS = [
    {"output_id": row["output_id"], "authorization_status": "AUTHORIZED_NOT_GENERATED"}
    for row in source.source.PLANNED_OUTPUTS
]
SUPPORTING_PACKAGES = [
    {"package_id": row["package_id"], "approval_status": "AVAILABLE_NOT_SELECTED"}
    for row in source.source.METHOD_PACKAGES[1:5]
]
BLOCKED_PACKAGES = [
    {"package_id": row["package_id"], "approval_status": "BLOCKED_NOT_APPROVED"}
    for row in source.source.METHOD_PACKAGES[5:]
]

NEXT_CHAIN = [
    "Retry Failure Remediation or Method Execution v1, if separately invoked.",
    "Retry Failure Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "retry_failure_method_execution_if_approved", "retry_failure_method_results_review",
    "new_integration_branch_retry_candidate_after_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "approval_does_not_execute_method", "approval_does_not_run_diagnostic_commands",
    "approval_does_not_rerun_retry", "approval_does_not_run_full_pytest",
    "approval_does_not_treat_diagnostics_as_retry_evidence",
    "approval_does_not_create_retry_results_review", "approval_does_not_create_integration_results_review",
    "approval_does_not_mark_integration_successful",
    "approval_does_not_generate_successful_integration_execution_digest",
    "approval_does_not_generate_successful_integration_validation_digest",
    "approval_does_not_stage_additional_evidence", "approval_does_not_modify_staged_evidence",
    "approval_does_not_regenerate_evidence", "approval_does_not_call_providers",
    "approval_does_not_commit_marketflow_outputs", "approval_does_not_push_integration_branch",
    "approval_does_not_push_main", "approval_does_not_delete_integration_branch",
    "approval_does_not_delete_worktree", "approval_does_not_force_push",
    "approval_does_not_prune_remotes", "approval_does_not_modify_tags",
    "approval_does_not_acquire_market_data", "approval_does_not_regenerate_dataset",
    "approval_does_not_recompute_metrics", "approval_does_not_train_models",
    "approval_does_not_score_strategy", "approval_does_not_generate_recommendations",
    "approval_does_not_accept_predictive_usefulness", "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime", "approval_does_not_authorize_broker_execution",
    "selected_method_approved_for_future_execution_only", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_execution_required_before_method",
    "separate_results_review_required_after_method", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound", "source_method_candidate_digest_bound",
    "source_retry_failure_diagnosis_digest_bound", "source_retry_approval_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "root_regression_boundary_bound",
    "operator_decision_matches", "operator_attestation_phrase_matches", "approval_scope_only",
    "selected_package_classify_failure_domains", "approval_created_true", "method_selected_true",
    "method_approved_true", "method_authorized_true", "ready_for_method_execution_true",
    "method_executed_false", "diagnostic_method_executed_false",
    "failure_domain_classification_generated_false", "planned_outputs_generated_false",
    "new_remediation_candidate_created_false", "new_retry_candidate_created_false",
    "new_retry_executed_false", "new_retry_results_review_created_false",
    "main_merge_approval_created_false", "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "requirements_approved_for_future_execution", "future_plan_approved_not_executed",
    "planned_outputs_authorized_not_generated", "supporting_packages_not_selected",
    "blocked_packages_not_approved", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(ValueError):
    """Raised when approval evidence, attestation, or authority boundaries are invalid."""


def _iso_utc(value: str) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_method_candidate_digest": source.SOURCE_METHOD_CANDIDATE_DIGEST,
        "operator_confirms_source_retry_failure_diagnosis_digest": source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST,
        "operator_confirms_retry_execution_commit": source.source.source.RETRY_EXECUTION_COMMIT,
        "operator_confirms_selected_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
                f"{field} mismatch"
            )
    if not _iso_utc(attestation.get("operator_attestation_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "operator_attestation_timestamp_utc invalid"
        )
    reference = attestation.get("operator_reference")
    if not isinstance(reference, str) or not reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "operator_reference missing"
        )
    for field in ATTESTATION_BOOLEAN_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
                f"{field} must be true"
            )


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_method_candidate_digest: str,
    operator_confirms_source_retry_failure_diagnosis_digest: str,
    operator_confirms_retry_execution_commit: str,
    operator_confirms_retry_failure_counts: bool,
    operator_confirms_root_regression_not_retry_evidence: bool,
    operator_confirms_selected_method_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_method_execution: bool,
    operator_confirms_no_diagnostic_execution: bool,
    operator_confirms_no_retry: bool, operator_confirms_no_full_pytest: bool,
    operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_integration_digest: bool,
    operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool, operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_evidence_regeneration: bool,
    operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_retry_failure_method_package: str = SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the required non-secret operator attestation."""
    attestation = {name: value for name, value in locals().items()}
    attestation["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(attestation)
    return attestation


def _source_review() -> dict[str, Any]:
    return {
        "source_retry_failure_method_operator_review_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1,
        "source_retry_failure_method_operator_review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_READY,
        "source_retry_failure_method_operator_review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_retry_failure_method_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        **source._source_candidate(),
    }


def _base_approval(source_review: Mapping[str, Any], operator_attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "operator_attestation_digest": semantic_digest(operator_attestation),
        **deepcopy(dict(source_review)),
        "retry_failure_method_selected": True, "retry_failure_method_approved": True,
        "retry_failure_method_authorized": True, "retry_failure_method_approval_created": True,
        "ready_for_retry_failure_method_execution": True,
        "retry_failure_method_executed": False, "diagnostic_method_executed": False,
        "failure_domain_classification_generated": False, "planned_outputs_generated": False,
        "new_remediation_candidate_created": False, "new_retry_candidate_created": False,
        "new_retry_approved": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "main_merge_approval_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "evidence_regenerated": False, "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "selected_method_package": {
            "package_id": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
            "approval_status": APPROVED_FOR_FUTURE_EXECUTION_ONLY,
            "selected": True, "approved": True, "authorized_for_future_execution": True,
            "executed": False,
        },
        "approved_future_method_requirements": deepcopy(APPROVED_FUTURE_METHOD_REQUIREMENTS),
        "approved_future_method_plan": deepcopy(APPROVED_FUTURE_METHOD_PLAN),
        "future_method_plan_approval_status": APPROVED_FOR_FUTURE_EXECUTION_ONLY,
        "future_method_plan_execution_status": "NOT_EXECUTED",
        "planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation") if isinstance(approval.get("operator_attestation"), dict) else {}
    retry_counts = {"passed": approval.get("retry_pytest_passed_count"), "failed": approval.get("retry_pytest_failed_count"), "errors": approval.get("retry_pytest_error_count"), "skipped": approval.get("retry_pytest_skipped_count")}
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_retry_failure_method_operator_review_digest")),
        "source_method_candidate_digest_bound": (source.SOURCE_METHOD_CANDIDATE_DIGEST, approval.get("source_retry_failure_method_candidate_digest")),
        "source_retry_failure_diagnosis_digest_bound": (source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, approval.get("source_retry_failure_diagnosis_digest")),
        "source_retry_approval_digest_bound": (source.source.SOURCE_RETRY_APPROVAL_DIGEST, approval.get("source_retry_approval_digest")),
        "retry_execution_commit_bound": (source.source.source.RETRY_EXECUTION_COMMIT, approval.get("retry_execution_commit")),
        "retry_failure_counts_bound": (source.source.source.RETRY_FAILED_RUN, retry_counts),
        "root_regression_boundary_bound": ([29200, 7, False, True], [approval.get("root_full_regression_passed_count"), approval.get("root_full_regression_skipped_count"), approval.get("root_full_regression_is_retry_evidence"), approval.get("root_full_regression_does_not_override_detached_retry_failure")]),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_classify_failure_domains": (SELECTED_RETRY_FAILURE_METHOD_PACKAGE, approval.get("selected_retry_failure_method_package")),
        "approval_created_true": (True, approval.get("retry_failure_method_approval_created")),
        "method_selected_true": (True, approval.get("retry_failure_method_selected")),
        "method_approved_true": (True, approval.get("retry_failure_method_approved")),
        "method_authorized_true": (True, approval.get("retry_failure_method_authorized")),
        "ready_for_method_execution_true": (True, approval.get("ready_for_retry_failure_method_execution")),
        "method_executed_false": (False, approval.get("retry_failure_method_executed")),
        "diagnostic_method_executed_false": (False, approval.get("diagnostic_method_executed")),
        "failure_domain_classification_generated_false": (False, approval.get("failure_domain_classification_generated")),
        "planned_outputs_generated_false": (False, approval.get("planned_outputs_generated")),
        "new_remediation_candidate_created_false": (False, approval.get("new_remediation_candidate_created")),
        "new_retry_candidate_created_false": (False, approval.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, approval.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, approval.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, approval.get("main_merge_approval_created")),
        "integration_execution_successful_false": (False, approval.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, approval.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, approval.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, approval.get("integration_branch_pushed")),
        "main_push_false": (False, approval.get("main_push_performed")),
        "origin_main_modified_false": (False, approval.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, approval.get("marketflow_outputs_committed")),
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
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_METHOD_REQUIREMENTS, approval.get("approved_future_method_requirements")),
        "future_plan_approved_not_executed": ([APPROVED_FUTURE_METHOD_PLAN, "NOT_EXECUTED"], [approval.get("approved_future_method_plan"), approval.get("future_method_plan_execution_status")]),
        "planned_outputs_authorized_not_generated": (AUTHORIZED_PLANNED_OUTPUTS, approval.get("planned_outputs")),
        "supporting_packages_not_selected": (SUPPORTING_PACKAGES, approval.get("supporting_packages")),
        "blocked_packages_not_approved": (BLOCKED_PACKAGES, approval.get("blocked_packages")),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "no_tracked_marketflow_files": (True, approval.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "retry_failure_method_selected": True, "retry_failure_method_approved": True,
        "retry_failure_method_authorized": True, "retry_failure_method_approval_created": True,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        "ready_for_retry_failure_method_execution": True, "method_executed": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "main_merge_approval_created": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic approval digest."""
    payload = deepcopy(dict(approval))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build an approval only from exact source evidence and a complete attestation."""
    if not isinstance(operator_attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "operator_attestation must be an object"
        )
    _validate_attestation(operator_attestation)
    evidence = _source_review()
    if source_review is not None:
        if not isinstance(source_review, dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
                "source_review must be an object"
            )
        evidence.update(deepcopy(source_review))
    approval = _base_approval(evidence, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"] = (
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest_v1(approval)
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(approval)
    return approval


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
    approval: dict,
) -> dict:
    """Validate attested future-execution authority and reject any execution state."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "approval must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        **_source_review(), "approved_future_method_requirements": APPROVED_FUTURE_METHOD_REQUIREMENTS,
        "approved_future_method_plan": APPROVED_FUTURE_METHOD_PLAN,
        "future_method_plan_approval_status": APPROVED_FOR_FUTURE_EXECUTION_ONLY,
        "future_method_plan_execution_status": "NOT_EXECUTED",
        "planned_outputs": AUTHORIZED_PLANNED_OUTPUTS, "supporting_packages": SUPPORTING_PACKAGES,
        "blocked_packages": BLOCKED_PACKAGES, "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(approval.get(field), expected, field)
    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "operator_attestation missing"
        )
    _validate_attestation(attestation)
    _expect(approval.get("operator_attestation_digest"), semantic_digest(attestation), "operator_attestation_digest")
    required_true = (
        "created_offline", "governance_only", "operator_attestation_required",
        "retry_failure_method_selected", "retry_failure_method_approved",
        "retry_failure_method_authorized", "retry_failure_method_approval_created",
        "ready_for_retry_failure_method_execution", "no_tracked_marketflow_files",
    )
    required_false = (
        "root_full_regression_is_retry_evidence", "retry_failure_method_executed",
        "diagnostic_method_executed", "failure_domain_classification_generated",
        "planned_outputs_generated", "new_remediation_candidate_created", "new_retry_candidate_created",
        "new_retry_approved", "new_retry_executed", "new_retry_results_review_created",
        "main_merge_approval_created", "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed",
        "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
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
    selected = approval.get("selected_method_package")
    if not isinstance(selected, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "selected_method_package missing"
        )
    _expect(selected.get("package_id"), SELECTED_RETRY_FAILURE_METHOD_PACKAGE, "selected package")
    _expect([selected.get(key) for key in ("selected", "approved", "authorized_for_future_execution", "executed")], [True, True, True, False], "selected package states")
    checklist = approval.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(approval), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "checklist failed"
        )
    _expect(approval.get("summary"), _summary(checklist), "summary")
    digest = approval.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "approval digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest_v1(approval),
        "approval digest",
    )
    return {
        "status": approval["approval_status"], "artifact_kind": approval["artifact_kind"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest": digest,
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render the validated approval as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(approval)
    attestation = approval["operator_attestation"]
    sections = [
        ("Operator Attestation", [f"Reference/version: `{attestation['operator_reference']}` / `{attestation['operator_attestation_version']}`.", f"Decision: `{attestation['operator_decision']}`.", "The attestation is non-secret and digest-bound."]),
        ("Source Operator Review", [f"Digest: `{approval['source_retry_failure_method_operator_review_digest']}`."]),
        ("Source Method Candidate", [f"Digest: `{approval['source_retry_failure_method_candidate_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The failed retry remains authoritative."]),
        ("Approval Scope", ["Future method execution only; this artifact performs no execution, retry, or results review."]),
        ("Selected Method Package", [f"`{approval['selected_retry_failure_method_package']}`: `{APPROVED_FOR_FUTURE_EXECUTION_ONLY}`."]),
        ("Approved Future Method Requirements", [f"`{row['requirement_id']}`: `{row['approval_status']}`" for row in approval["approved_future_method_requirements"]]),
        ("Approved Future Method Plan", [f"`{row['step_id']}`: `{row['approval_status']}` / `{row['execution_status']}`" for row in approval["approved_future_method_plan"]]),
        ("Planned Outputs", [f"`{row['output_id']}`: `{row['authorization_status']}`" for row in approval["planned_outputs"]]),
        ("Supporting Packages", [f"`{row['package_id']}`: `{row['approval_status']}`" for row in approval["supporting_packages"]]),
        ("Blocked Packages", [f"`{row['package_id']}`: `{row['approval_status']}`" for row in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in approval["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in approval["risk_controls"]]),
        ("Authority Boundaries", ["No method execution, retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The root regression is not retry evidence.", "A separate execution task is required before any classification output may be generated."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
    output_dir: str | Path, *, source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
