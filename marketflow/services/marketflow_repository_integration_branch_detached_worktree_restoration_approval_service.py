"""Attestation-gated approval for future detached-worktree restoration."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1 = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED"
)
REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY = (
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY"
)

SELECTED_WORKTREE_RESTORATION_PACKAGE = (
    source.source.PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD
)
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE INTEGRATION BRANCH DETACHED WORKTREE RESTORATION "
    "PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD "
    "MARKETFLOW REGISTERED DETACHED WORKTREE EXACT INTEGRATION HEAD NO BRANCH RESET "
    "NO WORKTREE DELETE NO REMEDIATION NO RETRY "
    "REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY"
)
OPERATOR_DECISION = "APPROVE_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_detached_worktree_restoration_approval_attestation_v1"
)

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "e43dd78c5861e1bb0e8c8fe42c9dfeaf54c81f80943c521310ee20c6547cd0c1"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = source.source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST
EXPECTED_BLOCKED_EXECUTION_STATUS = source.source.BLOCKED_REMEDIATION_EXECUTION_STATUS
EXPECTED_INTEGRATION_BRANCH_NAME = source.source.INTEGRATION_BRANCH_NAME
EXPECTED_INTEGRATION_HEAD_COMMIT = source.source.INTEGRATION_BRANCH_HEAD_COMMIT
EXPECTED_ORIGIN_MAIN_COMMIT = source.source.ORIGIN_MAIN_COMMIT

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_STRING_FIELDS = {
    "operator_decision": OPERATOR_DECISION,
    "selected_worktree_restoration_package": SELECTED_WORKTREE_RESTORATION_PACKAGE,
    "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
    "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_remediation_approval_digest": EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST,
    "operator_confirms_source_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
    "operator_confirms_blocked_execution_status": EXPECTED_BLOCKED_EXECUTION_STATUS,
    "operator_confirms_integration_branch_name": EXPECTED_INTEGRATION_BRANCH_NAME,
    "operator_confirms_integration_head_commit": EXPECTED_INTEGRATION_HEAD_COMMIT,
    "operator_confirms_origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "operator_confirms_selected_worktree_restoration_package": SELECTED_WORKTREE_RESTORATION_PACKAGE,
}
ATTESTATION_TRUE_FIELDS = (
    "operator_confirms_source_evidence_root_exists",
    "operator_confirms_required_manifest_exists",
    "operator_confirms_approval_scope_only",
    "operator_confirms_no_worktree_creation",
    "operator_confirms_no_worktree_restore",
    "operator_confirms_no_worktree_delete",
    "operator_confirms_no_integration_branch_reset",
    "operator_confirms_no_remediation_execution",
    "operator_confirms_no_evidence_staging",
    "operator_confirms_no_marketflow_copy",
    "operator_confirms_no_marketflow_commit",
    "operator_confirms_no_retry",
    "operator_confirms_no_results_review",
    "operator_confirms_no_integration_success",
    "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push",
    "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete",
    "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation",
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
)

APPROVED_SELECTED_PACKAGE = {
    "package_id": SELECTED_WORKTREE_RESTORATION_PACKAGE,
    "approval_status": "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY",
    "selected": True,
    "approved": True,
    "authorized_for_future_execution": True,
    "executed": False,
}
APPROVED_FUTURE_WORKTREE_RESTORATION_REQUIREMENTS = [
    {
        "requirement_id": row["requirement_id"],
        "source_value": row["source_value"],
        "approval_status": "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY",
    }
    for row in source.REVIEWED_WORKTREE_RESTORATION_REQUIREMENTS
]
APPROVED_FUTURE_WORKTREE_RESTORATION_PLAN = [
    {
        "step_id": row["step_id"],
        "instruction": row["instruction"],
        "approval_status": "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    }
    for row in source.REVIEWED_FUTURE_WORKTREE_RESTORATION_PLAN
]
SUPPORTING_PACKAGES = [
    {
        "package_id": package_id,
        "approval_status": "AVAILABLE_NOT_SELECTED",
        "selected": False,
        "approved": False,
        "authorized_for_future_execution": False,
        "executed": False,
    }
    for package_id in (
        source.source.PACKAGE_CREATE_WORKTREE_ATTACHED_TO_EXISTING_INTEGRATION_BRANCH,
        source.source.PACKAGE_PARAMETERIZE_REMEDIATION_WITH_EXISTING_WORKTREE_PATH_AFTER_MANUAL_OPERATOR_RESTORE,
    )
]
BLOCKED_PACKAGES = [
    {
        "package_id": package_id,
        "approval_status": "BLOCKED_NOT_APPROVED",
        "selected": False,
        "approved": False,
        "authorized_for_future_execution": False,
        "executed": False,
    }
    for package_id in (
        source.source.PACKAGE_RECREATE_INTEGRATION_BRANCH_FROM_APPROVED_PARENTS,
        source.source.PACKAGE_DELETE_AND_RECREATE_INTEGRATION_BRANCH_OR_WORKTREE,
        source.source.PACKAGE_USE_FEATURE_WORKTREE_AS_INTEGRATION_WORKTREE,
    )
]

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_V1"
)
NEXT_CHAIN = [
    "Worktree Restoration Execution v1, if separately invoked.",
    "Worktree Restoration Results Review v1.",
    "Remediation Execution v1 retry, only after worktree restoration review passes.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1.",
    "Integration Branch Retry Approval v1.",
    "Integration Branch Retry Execution v1.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "worktree_restoration_execution_if_approved",
    "worktree_restoration_results_review",
    "remediation_execution_after_worktree_restoration",
    "remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "approval_does_not_create_worktree", "approval_does_not_restore_worktree",
    "approval_does_not_delete_worktree", "approval_does_not_reset_integration_branch",
    "approval_does_not_delete_integration_branch", "approval_does_not_recreate_integration_branch",
    "approval_does_not_stage_evidence", "approval_does_not_copy_marketflow_outputs",
    "approval_does_not_commit_marketflow_outputs", "approval_does_not_run_pytest_retry",
    "approval_does_not_create_results_review", "approval_does_not_push_integration_branch",
    "approval_does_not_push_main", "approval_does_not_force_push", "approval_does_not_prune_remotes",
    "approval_does_not_modify_tags", "approval_does_not_call_providers",
    "approval_does_not_acquire_market_data", "approval_does_not_regenerate_dataset",
    "approval_does_not_recompute_metrics", "approval_does_not_train_models",
    "approval_does_not_score_strategy", "approval_does_not_generate_recommendations",
    "approval_does_not_accept_predictive_usefulness", "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime", "approval_does_not_authorize_broker_execution",
    "selected_restoration_approved_for_future_execution_only",
    "separate_execution_required_before_worktree_restoration",
    "separate_results_review_required_after_worktree_restoration",
    "separate_remediation_execution_required_after_worktree_restoration",
    "protect_origin_main", "preserve_existing_integration_branch", "preserve_failed_gate",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound", "source_candidate_digest_bound",
    "source_remediation_approval_digest_bound", "source_diagnosis_digest_bound",
    "blocked_execution_status_recorded", "integration_branch_name_bound",
    "integration_head_commit_bound", "origin_main_commit_bound",
    "source_evidence_root_exists_recorded", "required_manifest_exists_recorded",
    "operator_decision_matches", "operator_attestation_phrase_matches", "approval_scope_only",
    "selected_package_registered_detached_worktree", "approval_created_true",
    "restoration_selected_true", "restoration_approved_true", "restoration_authorized_true",
    "ready_for_restoration_execution_true", "restoration_executed_false",
    "detached_worktree_created_false", "detached_worktree_restored_false",
    "detached_worktree_deleted_false", "integration_branch_deleted_or_reset_false",
    "remediation_executed_false", "evidence_staged_false", "marketflow_outputs_copied_false",
    "marketflow_outputs_committed_false", "retry_candidate_created_false", "retry_executed_false",
    "results_review_created_false", "integration_execution_successful_false",
    "integration_branch_pushed_false", "main_push_false", "origin_main_modified_false",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "requirements_approved_for_future_execution",
    "future_plan_approved_not_executed", "supporting_packages_not_selected",
    "blocked_packages_not_approved", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(ValueError):
    """Raised when approval evidence or attestation fails closed."""


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "operator_attestation must be an object"
        )
    for field, expected in ATTESTATION_STRING_FIELDS.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
                f"operator attestation {field} mismatch"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_TRUE_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
                f"operator attestation {field} must be true"
            )


def build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_remediation_approval_digest: str,
    operator_confirms_source_diagnosis_digest: str,
    operator_confirms_blocked_execution_status: str,
    operator_confirms_integration_branch_name: str,
    operator_confirms_integration_head_commit: str,
    operator_confirms_origin_main_commit: str,
    operator_confirms_source_evidence_root_exists: bool,
    operator_confirms_required_manifest_exists: bool,
    operator_confirms_selected_worktree_restoration_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_worktree_creation: bool,
    operator_confirms_no_worktree_restore: bool,
    operator_confirms_no_worktree_delete: bool,
    operator_confirms_no_integration_branch_reset: bool,
    operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_evidence_staging: bool,
    operator_confirms_no_marketflow_copy: bool,
    operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_retry: bool,
    operator_confirms_no_results_review: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool,
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
    selected_worktree_restoration_package: str = SELECTED_WORKTREE_RESTORATION_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the complete non-secret operator attestation."""
    supplied = locals().copy()
    attestation = {
        "operator_decision": operator_decision,
        "selected_worktree_restoration_package": selected_worktree_restoration_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        **{
            field: supplied[field]
            for field in ATTESTATION_STRING_FIELDS
            if field.startswith("operator_confirms_")
        },
        **{field: supplied[field] for field in ATTESTATION_TRUE_FIELDS},
    }
    _validate_attestation(attestation)
    return attestation


def _source_review(source_review: dict | None) -> dict[str, Any]:
    review = (
        source.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1()
        if source_review is None
        else deepcopy(source_review)
    )
    try:
        validation = source.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
            review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "source operator review is invalid"
        ) from exc
    if validation[
        "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"
    ] != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "source operator-review digest mismatch"
        )
    return review


def _base_approval(
    source_review: dict | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_attestation(operator_attestation)
    review = _source_review(source_review)
    copied_fields = (
        "source_worktree_restoration_candidate_digest", "source_remediation_approval_digest",
        "source_remediation_operator_review_digest", "source_remediation_candidate_digest",
        "source_failure_diagnosis_digest", "source_merge_strategy_approval_digest",
        "blocked_remediation_execution_artifact_kind", "blocked_remediation_execution_status",
        "integration_branch_name", "integration_branch_head_commit", "integration_branch_exists_local",
        "integration_branch_matches_required_head", "detached_integration_worktree_exists",
        "registered_worktree_entries_present", "git_worktrees_directory_present",
        "remote_integration_branch_exists", "origin_main_commit", "source_evidence_root_path",
        "source_evidence_root_exists", "source_required_manifest_name",
        "source_required_manifest_exists", "source_evidence_file_count",
        "source_evidence_total_bytes", "source_evidence_ignored_by_gitignore",
        "marketflow_outputs_tracked", "tracked_marketflow_file_count", "no_tracked_marketflow_files",
    )
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY,
        "selected_worktree_restoration_package": SELECTED_WORKTREE_RESTORATION_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_worktree_restoration_operator_review_artifact_kind": review["artifact_kind"],
        "source_worktree_restoration_operator_review_status": review["review_status"],
        "source_worktree_restoration_operator_review_scope": review["review_scope"],
        "source_worktree_restoration_operator_review_digest": review[
            "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"
        ],
        **{field: deepcopy(review[field]) for field in copied_fields},
        "worktree_restoration_selected": True, "worktree_restoration_approved": True,
        "worktree_restoration_authorized": True, "worktree_restoration_approval_created": True,
        "ready_for_worktree_restoration_execution": True,
        "worktree_restoration_executed": False, "detached_worktree_created": False,
        "detached_worktree_restored": False, "detached_worktree_deleted": False,
        "integration_branch_deleted_or_reset": False, "remediation_executed": False,
        "evidence_staged": False, "marketflow_outputs_copied": False,
        "marketflow_outputs_committed": False, "evidence_regenerated": False,
        "integration_retry_candidate_created": False, "integration_retry_executed": False,
        "integration_results_review_created": False, "integration_execution_successful": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "approved_selected_package": deepcopy(APPROVED_SELECTED_PACKAGE),
        "approved_future_worktree_restoration_requirements": deepcopy(APPROVED_FUTURE_WORKTREE_RESTORATION_REQUIREMENTS),
        "approved_future_worktree_restoration_plan": deepcopy(APPROVED_FUTURE_WORKTREE_RESTORATION_PLAN),
        "future_plan_approval_status": "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY",
        "future_plan_execution_status": "NOT_EXECUTED",
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "remediation_execution_ready_now": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation", {})
    values: dict[str, tuple[Any, Any]] = {
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_worktree_restoration_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, approval.get("source_worktree_restoration_candidate_digest")),
        "source_remediation_approval_digest_bound": (EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST, approval.get("source_remediation_approval_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, approval.get("source_failure_diagnosis_digest")),
        "blocked_execution_status_recorded": (EXPECTED_BLOCKED_EXECUTION_STATUS, approval.get("blocked_remediation_execution_status")),
        "integration_branch_name_bound": (EXPECTED_INTEGRATION_BRANCH_NAME, approval.get("integration_branch_name")),
        "integration_head_commit_bound": (EXPECTED_INTEGRATION_HEAD_COMMIT, approval.get("integration_branch_head_commit")),
        "origin_main_commit_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, approval.get("origin_main_commit")),
        "source_evidence_root_exists_recorded": (True, approval.get("source_evidence_root_exists")),
        "required_manifest_exists_recorded": (True, approval.get("source_required_manifest_exists")),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (True, attestation.get("operator_confirms_approval_scope_only")),
        "selected_package_registered_detached_worktree": (SELECTED_WORKTREE_RESTORATION_PACKAGE, approval.get("selected_worktree_restoration_package")),
        "approval_created_true": (True, approval.get("worktree_restoration_approval_created")),
        "restoration_selected_true": (True, approval.get("worktree_restoration_selected")),
        "restoration_approved_true": (True, approval.get("worktree_restoration_approved")),
        "restoration_authorized_true": (True, approval.get("worktree_restoration_authorized")),
        "ready_for_restoration_execution_true": (True, approval.get("ready_for_worktree_restoration_execution")),
        "restoration_executed_false": (False, approval.get("worktree_restoration_executed")),
        "detached_worktree_created_false": (False, approval.get("detached_worktree_created")),
        "detached_worktree_restored_false": (False, approval.get("detached_worktree_restored")),
        "detached_worktree_deleted_false": (False, approval.get("detached_worktree_deleted")),
        "integration_branch_deleted_or_reset_false": (False, approval.get("integration_branch_deleted_or_reset")),
        "remediation_executed_false": (False, approval.get("remediation_executed")),
        "evidence_staged_false": (False, approval.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, approval.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, approval.get("marketflow_outputs_committed")),
        "retry_candidate_created_false": (False, approval.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, approval.get("integration_retry_executed")),
        "results_review_created_false": (False, approval.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, approval.get("integration_execution_successful")),
        "integration_branch_pushed_false": (False, approval.get("integration_branch_pushed")),
        "main_push_false": (False, approval.get("main_push_performed")),
        "origin_main_modified_false": (False, approval.get("origin_main_modified_by_this_task")),
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
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_WORKTREE_RESTORATION_REQUIREMENTS, approval.get("approved_future_worktree_restoration_requirements")),
        "future_plan_approved_not_executed": ([APPROVED_FUTURE_WORKTREE_RESTORATION_PLAN, "NOT_EXECUTED"], [approval.get("approved_future_worktree_restoration_plan"), approval.get("future_plan_execution_status")]),
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
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "worktree_restoration_selected": True, "worktree_restoration_approved": True,
        "worktree_restoration_authorized": True, "worktree_restoration_approval_created": True,
        "selected_worktree_restoration_package": SELECTED_WORKTREE_RESTORATION_PACKAGE,
        "ready_for_worktree_restoration_execution": True, "detached_worktree_created": False,
        "worktree_restoration_executed": False, "remediation_execution_ready_now": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic approval digest."""
    payload = deepcopy(dict(approval))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build future restoration approval from exact review evidence and attestation."""
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval[
        "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"
    ] = marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest_v1(
        approval
    )
    validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        approval
    )
    return approval


def validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
    approval: dict,
) -> dict:
    """Validate exact attestation, selection, and closed execution boundaries."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval must be an object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
                f"{field} mismatch"
            )
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval checklist failed"
        )
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get(
        "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval digest missing"
        )
    if digest != marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest_v1(
        approval
    ):
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED,
        "artifact_kind": approval["artifact_kind"], "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest": digest,
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated approval-only package."""
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        approval
    )
    attestation = approval["operator_attestation"]
    sections = [
        ("Operator Attestation", [f"Operator reference: `{attestation['operator_reference']}`.", f"Timestamp: `{attestation['operator_attestation_timestamp_utc']}`.", f"Decision: `{attestation['operator_decision']}`.", "All required digest, ref, scope, and closed-boundary confirmations are complete."]),
        ("Source Operator Review", [f"Artifact/status/digest: `{approval['source_worktree_restoration_operator_review_artifact_kind']}` / `{approval['source_worktree_restoration_operator_review_status']}` / `{approval['source_worktree_restoration_operator_review_digest']}`."]),
        ("Blocked Remediation Execution Observation", [f"`{approval['blocked_remediation_execution_artifact_kind']}` / `{approval['blocked_remediation_execution_status']}`.", f"Integration branch/head: `{approval['integration_branch_name']}` / `{approval['integration_branch_head_commit']}`."]),
        ("Approval Scope", [f"`{approval['approval_scope']}`."]),
        ("Selected Restoration Package", [f"`{approval['selected_worktree_restoration_package']}`: approved for future restoration execution only; not executed."]),
        ("Approved Future Restoration Requirements", [f"`{row['requirement_id']}`: `{row['approval_status']}`." for row in approval["approved_future_worktree_restoration_requirements"]]),
        ("Approved Future Restoration Plan", [f"`{row['step_id']}`: {row['instruction']} (`{row['approval_status']}` / `{row['execution_status']}`)" for row in approval["approved_future_worktree_restoration_plan"]]),
        ("Supporting Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["supporting_packages"]]),
        ("Blocked Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in approval["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in approval["risk_controls"]]),
        ("Authority Boundaries", ["Approval authorizes only a separate future restoration execution. No worktree, remediation, retry, results review, runtime authority, or trading authority is created now."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The execution task must re-verify exact refs and path state before creating a worktree.", "The failed integration gate remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Detached Worktree Restoration Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
    output_dir: str | Path,
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        approval
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"], "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest": validation[
            "marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
