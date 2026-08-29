"""Offline, attestation-gated approval for future integration-branch validation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_merge_strategy_operator_review_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1 = (
    "marketflow_repository_merge_strategy_approval_v1"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED"
)
REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_VALID = (
    "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_VALID"
)
PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION = (
    source_service.source_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
)

REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE REPOSITORY MERGE STRATEGY "
    "PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION "
    "MARKETFLOW INTEGRATION BRANCH VALIDATION ORIGIN MAIN PROTECTED TERMINAL EVIDENCE STACK "
    "REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
OPERATOR_DECISION = "APPROVE_REPOSITORY_MERGE_STRATEGY"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_merge_strategy_approval_attestation_v1"

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "557c0960704c09c512fc4cdd64964742d67a11793d1750569e775a5868a45930"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST
EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST
EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT = "34fbc53a31eab0e9feec8df1814dfbd9b22c4f4b"
EXPECTED_SOURCE_CANDIDATE_COMMIT = source_service.EXPECTED_SOURCE_CANDIDATE_COMMIT
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)

INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_BASE = "origin/main"
INTEGRATION_SOURCE_BRANCH = "feature/marketflow-repository-tag-push-results-review-v1"
INTEGRATION_SOURCE_COMMIT = "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

APPROVED_SELECTED_PACKAGE = {
    "package_id": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
    "approval_status": "APPROVED_FOR_FUTURE_INTEGRATION_BRANCH_EXECUTION_ONLY",
    "selected": True, "approved": True, "authorized_for_future_execution": True,
    "executed": False, "integration_branch_created": False, "main_push_required": False,
    "runtime_authority_created": False, "predictive_usefulness_accepted": False,
    "profitability_accepted": False,
}
SUPPORTING_PACKAGES = [
    {
        "package_id": package_id, "approval_status": "AVAILABLE_NOT_SELECTED",
        "selected": False, "approved": False, "authorized_for_future_execution": False,
        "executed": False,
    }
    for package_id in (
        source_service.source_service.PACKAGE_NO_MAIN_MERGE_BRANCH_AND_TAG_TRACEABILITY_ONLY,
        source_service.source_service.PACKAGE_SQUASH_MERGE_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW,
        source_service.source_service.PACKAGE_MERGE_COMMIT_TERMINAL_STACK_TO_MAIN_AFTER_REVIEW,
        source_service.source_service.PACKAGE_SELECTIVE_DOCS_AND_STATUS_ONLY_INTEGRATION,
        source_service.source_service.PACKAGE_DEFER_MERGE_UNTIL_BRANCH_CLEANUP_PLAN,
    )
]
APPROVED_INTEGRATION_BRANCH_PLAN = {
    "integration_branch_name": INTEGRATION_BRANCH_NAME,
    "integration_base": INTEGRATION_BASE,
    "integration_source_branch": INTEGRATION_SOURCE_BRANCH,
    "integration_source_commit": INTEGRATION_SOURCE_COMMIT,
    "integration_plan_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY",
    "integration_branch_created": False, "integration_merge_performed": False,
    "integration_pytest_performed": False, "main_merge_performed": False,
    "main_push_performed": False, "separate_execution_required": True,
    "separate_results_review_required": True, "main_merge_requires_separate_approval": True,
}
FUTURE_EXECUTION_BOUNDARY = {
    "approved_future_execution_type": "CREATE_TEMPORARY_INTEGRATION_BRANCH_AND_VALIDATE_FULL_STACK_ONLY",
    "approved_future_execution_scope": "INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME",
    "future_execution_may_create_integration_branch": True,
    "future_execution_may_attempt_integration_merge_on_integration_branch": True,
    "future_execution_may_run_full_pytest_on_integration_branch": True,
    "future_execution_must_not_push_main": True,
    "future_execution_must_not_delete_branches": True,
    "future_execution_must_not_force_push": True,
    "future_execution_must_not_accept_predictive_usefulness": True,
    "future_execution_must_not_authorize_runtime": True,
}

NEXT_CHAIN = [
    "Repository Integration Branch Execution v1, if separately invoked.",
    "Repository Integration Branch Results Review v1.",
    "Repository Main Merge Approval v1, only if integration branch review passes.",
    "Repository Main Merge Execution v1, only if separately approved.",
    "Repository Branch Cleanup Candidate v1, only after main integration strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
]
NEXT_GATES = [
    "repository_integration_branch_execution_if_approved",
    "repository_integration_branch_results_review",
    "repository_main_merge_approval_if_integration_passes",
    "repository_main_merge_execution_if_approved",
    "repository_branch_cleanup_candidate_after_merge_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
]
RISK_CONTROLS = [
    "approval_does_not_create_integration_branch", "approval_does_not_merge",
    "approval_does_not_rebase", "approval_does_not_squash_merge",
    "approval_does_not_cherry_pick", "approval_does_not_push_main",
    "approval_does_not_force_push", "approval_does_not_delete_branches",
    "approval_does_not_delete_remote_branches", "approval_does_not_prune_remotes",
    "approval_does_not_modify_origin_main", "approval_does_not_modify_tags",
    "approval_does_not_push_additional_tags", "approval_does_not_modify_marketflow_outputs",
    "approval_does_not_call_providers", "approval_does_not_acquire_market_data",
    "approval_does_not_regenerate_dataset", "approval_does_not_rerun_merge_strategy_candidate",
    "approval_does_not_rerun_merge_strategy_operator_review",
    "approval_does_not_rerun_tag_push_results_review", "approval_does_not_rerun_tag_push_execution",
    "approval_does_not_rerun_inventory", "approval_does_not_rerun_evidence",
    "approval_does_not_recompute_metrics", "approval_does_not_train_models",
    "approval_does_not_score_strategy", "approval_does_not_generate_recommendations",
    "approval_does_not_accept_predictive_usefulness", "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime", "approval_does_not_authorize_broker_execution",
    "selected_strategy_approved_for_future_execution_only",
    "separate_execution_required_before_integration_branch",
    "separate_approval_required_before_main_merge", "main_push_requires_separate_approval",
    "protect_origin_main", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound", "source_candidate_digest_bound",
    "source_tag_push_results_review_digest_bound", "source_remote_manifest_review_digest_bound",
    "source_tag_push_execution_digest_bound", "source_tag_push_approval_digest_bound",
    "source_inventory_plan_digest_bound", "source_final_archive_digest_bound",
    "source_archive_digest_bound", "source_operator_selection_digest_bound",
    "source_closure_digest_bound", "source_readiness_digest_bound",
    "source_reassessment_digest_bound", "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound", "records_digest_bound", "origin_main_commit_bound",
    "operator_decision_matches", "operator_attestation_phrase_matches", "approval_scope_only",
    "selected_package_integration_branch_validation", "approval_created_true",
    "strategy_selected_true", "strategy_approved_true", "strategy_authorized_true",
    "ready_for_integration_branch_execution_true", "strategy_executed_false",
    "integration_branch_plan_approved", "integration_branch_name_matches",
    "integration_base_origin_main", "integration_source_commit_matches",
    "integration_branch_created_false", "integration_merge_performed_false",
    "integration_pytest_performed_false", "main_merge_performed_false", "main_push_false",
    "merge_performed_false", "rebase_performed_false", "squash_merge_performed_false",
    "cherry_pick_performed_false", "branch_delete_false", "remote_delete_false",
    "force_push_false", "remote_prune_false", "origin_main_modified_false",
    "tags_pushed_again_false", "additional_tags_created_false", "tags_modified_false",
    "tags_deleted_false", "cleanup_candidate_created_false", "marketflow_outputs_not_tracked",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]

ATTESTATION_STRING_FIELDS = {
    "operator_decision": OPERATOR_DECISION,
    "selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
    "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
    "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_tag_push_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    "operator_confirms_source_remote_manifest_review_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
    "operator_confirms_source_tag_push_execution_digest": EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
    "operator_confirms_source_tag_push_approval_digest": EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
    "operator_confirms_origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "operator_confirms_selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
    "operator_confirms_integration_branch_name": INTEGRATION_BRANCH_NAME,
    "operator_confirms_integration_base": INTEGRATION_BASE,
    "operator_confirms_integration_source_branch": INTEGRATION_SOURCE_BRANCH,
    "operator_confirms_integration_source_commit": INTEGRATION_SOURCE_COMMIT,
}
ATTESTATION_TRUE_FIELDS = [
    "operator_confirms_approval_scope_only", "operator_confirms_integration_branch_not_created",
    "operator_confirms_no_merge", "operator_confirms_no_rebase",
    "operator_confirms_no_squash_merge", "operator_confirms_no_cherry_pick",
    "operator_confirms_no_main_push", "operator_confirms_no_branch_delete",
    "operator_confirms_no_remote_delete", "operator_confirms_no_force_push",
    "operator_confirms_no_remote_prune", "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_tag_mutation", "operator_confirms_no_additional_tag_push",
    "operator_confirms_no_provider_requests", "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized", "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]


class MarketFlowRepositoryMergeStrategyApprovalError(ValueError):
    """Raised when approval evidence or attestation fails closed."""


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryMergeStrategyApprovalError("operator_attestation must be an object")
    for field, expected in ATTESTATION_STRING_FIELDS.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryMergeStrategyApprovalError(f"operator attestation {field} mismatch")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowRepositoryMergeStrategyApprovalError(f"operator attestation {field} missing")
    for field in ATTESTATION_TRUE_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryMergeStrategyApprovalError(f"operator attestation {field} must be true")


def build_marketflow_repository_merge_strategy_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_tag_push_results_review_digest: str,
    operator_confirms_source_remote_manifest_review_digest: str,
    operator_confirms_source_tag_push_execution_digest: str,
    operator_confirms_source_tag_push_approval_digest: str,
    operator_confirms_origin_main_commit: str,
    operator_confirms_selected_merge_strategy_package: str,
    operator_confirms_integration_branch_name: str,
    operator_confirms_integration_base: str,
    operator_confirms_integration_source_branch: str,
    operator_confirms_integration_source_commit: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_integration_branch_not_created: bool,
    operator_confirms_no_merge: bool,
    operator_confirms_no_rebase: bool,
    operator_confirms_no_squash_merge: bool,
    operator_confirms_no_cherry_pick: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_remote_delete: bool,
    operator_confirms_no_force_push: bool,
    operator_confirms_no_remote_prune: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_tag_mutation: bool,
    operator_confirms_no_additional_tag_push: bool,
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
    selected_merge_strategy_package: str = PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the complete non-secret operator attestation."""
    supplied_values = locals().copy()
    attestation = {
        "operator_decision": operator_decision,
        "selected_merge_strategy_package": selected_merge_strategy_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        **{field: supplied_values[field] for field in ATTESTATION_STRING_FIELDS if field.startswith("operator_confirms_")},
        **{field: supplied_values[field] for field in ATTESTATION_TRUE_FIELDS},
    }
    _validate_attestation(attestation)
    return attestation


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_review, dict):
        raise MarketFlowRepositoryMergeStrategyApprovalError("source_review must be an object")
    try:
        source_service.validate_marketflow_repository_merge_strategy_operator_review_v1(source_review)
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryMergeStrategyApprovalError(
            "source merge-strategy operator review is invalid"
        ) from exc
    if source_review.get("marketflow_repository_merge_strategy_operator_review_digest") != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryMergeStrategyApprovalError(
            "source merge-strategy operator review digest mismatch"
        )
    return deepcopy(source_review["source_evidence"])


def _base_approval(
    source_review: Mapping[str, Any] | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_attestation(operator_attestation)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED,
        "approval_scope": REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "created_offline": True, "planning_only": True, "governance_only": True,
        "operator_attestation_required": True, "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_merge_strategy_operator_review_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1,
        "source_merge_strategy_operator_review_status": source_service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_READY,
        "source_merge_strategy_operator_review_scope": source_service.REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_merge_strategy_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_merge_strategy_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tag_push_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest": EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_remote_manifest_digest": EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST,
        "source_tag_push_approval_digest": EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_merge_strategy_candidate_commit": EXPECTED_SOURCE_CANDIDATE_COMMIT,
        "source_operator_review_commit": EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_repository_context": {
            "local_branch_count": 302, "remote_ref_count": 274, "total_ref_count": 576,
            "local_tag_count": 32, "verified_terminal_tags": 4,
        },
        "repository_merge_strategy_candidate_created": True,
        "repository_merge_strategy_operator_review_created": True,
        "repository_merge_strategy_operator_review_ready": True,
        "repository_merge_strategy_selected": True, "repository_merge_strategy_approved": True,
        "repository_merge_strategy_authorized": True,
        "repository_merge_strategy_approval_created": True,
        "ready_for_repository_integration_branch_execution": True,
        "repository_merge_strategy_executed": False,
        "repository_integration_branch_created": False, "integration_branch_created": False,
        "integration_merge_performed": False, "integration_pytest_performed": False,
        "main_merge_performed": False, "main_push_performed": False,
        "git_merge_performed": False, "git_rebase_performed": False,
        "git_squash_merge_performed": False, "git_cherry_pick_performed": False,
        "git_main_push_performed": False, "origin_main_modified_by_this_task": False,
        "repository_cleanup_candidate_created": False, "repository_cleanup_approved": False,
        "repository_cleanup_executed": False, "git_branch_delete_performed": False,
        "git_remote_delete_performed": False, "git_force_push_performed": False,
        "git_remote_prune_performed": False, "repository_tags_pushed_again": False,
        "additional_tag_push_performed": False, "additional_tags_created": False,
        "tags_modified": False, "tags_deleted": False,
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
        "approved_selected_package": deepcopy(APPROVED_SELECTED_PACKAGE),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "approved_integration_branch_plan": deepcopy(APPROVED_INTEGRATION_BRANCH_PLAN),
        "future_execution_boundary": deepcopy(FUTURE_EXECUTION_BOUNDARY),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1",
    }


def _check_values(approval: Mapping[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    plan = approval.get("approved_integration_branch_plan", {})
    return {
        "source_operator_review_digest_bound": approval.get("source_merge_strategy_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": approval.get("source_merge_strategy_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tag_push_results_review_digest_bound": approval.get("source_tag_push_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_remote_manifest_review_digest_bound": approval.get("source_remote_manifest_review_digest") == EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "source_tag_push_execution_digest_bound": approval.get("source_tag_push_execution_digest") == EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "source_tag_push_approval_digest_bound": approval.get("source_tag_push_approval_digest") == EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "source_inventory_plan_digest_bound": approval.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": approval.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": approval.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": approval.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": approval.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": approval.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": approval.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest_bound": approval.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": approval.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": approval.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": approval.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_package_integration_branch_validation": approval.get("selected_merge_strategy_package") == PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "approval_created_true": approval.get("repository_merge_strategy_approval_created") is True,
        "strategy_selected_true": approval.get("repository_merge_strategy_selected") is True,
        "strategy_approved_true": approval.get("repository_merge_strategy_approved") is True,
        "strategy_authorized_true": approval.get("repository_merge_strategy_authorized") is True,
        "ready_for_integration_branch_execution_true": approval.get("ready_for_repository_integration_branch_execution") is True,
        "strategy_executed_false": approval.get("repository_merge_strategy_executed") is False,
        "integration_branch_plan_approved": plan == APPROVED_INTEGRATION_BRANCH_PLAN,
        "integration_branch_name_matches": plan.get("integration_branch_name") == INTEGRATION_BRANCH_NAME,
        "integration_base_origin_main": plan.get("integration_base") == INTEGRATION_BASE,
        "integration_source_commit_matches": plan.get("integration_source_commit") == INTEGRATION_SOURCE_COMMIT,
        "integration_branch_created_false": approval.get("repository_integration_branch_created") is False and approval.get("integration_branch_created") is False and plan.get("integration_branch_created") is False,
        "integration_merge_performed_false": approval.get("integration_merge_performed") is False and plan.get("integration_merge_performed") is False,
        "integration_pytest_performed_false": approval.get("integration_pytest_performed") is False and plan.get("integration_pytest_performed") is False,
        "main_merge_performed_false": approval.get("main_merge_performed") is False and plan.get("main_merge_performed") is False,
        "main_push_false": approval.get("main_push_performed") is False and approval.get("git_main_push_performed") is False and plan.get("main_push_performed") is False,
        "merge_performed_false": approval.get("git_merge_performed") is False,
        "rebase_performed_false": approval.get("git_rebase_performed") is False,
        "squash_merge_performed_false": approval.get("git_squash_merge_performed") is False,
        "cherry_pick_performed_false": approval.get("git_cherry_pick_performed") is False,
        "branch_delete_false": approval.get("git_branch_delete_performed") is False,
        "remote_delete_false": approval.get("git_remote_delete_performed") is False,
        "force_push_false": approval.get("git_force_push_performed") is False,
        "remote_prune_false": approval.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": approval.get("origin_main_modified_by_this_task") is False,
        "tags_pushed_again_false": approval.get("repository_tags_pushed_again") is False and approval.get("additional_tag_push_performed") is False,
        "additional_tags_created_false": approval.get("additional_tags_created") is False,
        "tags_modified_false": approval.get("tags_modified") is False,
        "tags_deleted_false": approval.get("tags_deleted") is False,
        "cleanup_candidate_created_false": approval.get("repository_cleanup_candidate_created") is False,
        "marketflow_outputs_not_tracked": approval.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": approval.get("provider_requests_made_in_approval") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval") is False,
        "dataset_generation_false": approval.get("dataset_generation_performed_in_approval") is False,
        "metric_recomputation_false": approval.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": approval.get("model_training_performed") is False,
        "strategy_scoring_false": approval.get("strategy_scoring_performed") is False,
        "recommendations_false": approval.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED and approval.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED and approval.get("profitability_accepted") is False,
        "runtime_not_authorized": approval.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id, "status": PASS if actual else FAIL, "expected": True,
        "actual": actual, "severity": BLOCKER,
        "message": "approval evidence matches" if actual else "approval evidence mismatch",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(approval)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_merge_strategy_selected": True, "repository_merge_strategy_approved": True,
        "repository_merge_strategy_authorized": True,
        "repository_merge_strategy_approval_created": True,
        "selected_merge_strategy_package": PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "ready_for_repository_integration_branch_execution": True,
        "integration_branch_created": False, "merge_performed": False, "main_pushed": False,
        "cleanup_candidate_created": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1",
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_merge_strategy_approval_digest_v1(approval: Mapping[str, Any]) -> str:
    """Return the deterministic semantic digest for the approval."""
    payload = deepcopy(dict(approval))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_merge_strategy_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_merge_strategy_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Build future-execution approval from exact committed evidence and attestation."""
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_merge_strategy_approval_digest"] = (
        marketflow_repository_merge_strategy_approval_digest_v1(approval)
    )
    validate_marketflow_repository_merge_strategy_approval_v1(approval)
    return approval


def validate_marketflow_repository_merge_strategy_approval_v1(approval: dict) -> dict:
    """Validate exact attestation, evidence, selection, and closed execution gates."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval must be an object")
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryMergeStrategyApprovalError(f"{field} mismatch")
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval checklist failed")
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval summary mismatch")
    digest = approval.get("marketflow_repository_merge_strategy_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval digest missing")
    if digest != marketflow_repository_merge_strategy_approval_digest_v1(approval):
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"], "approval_status": approval["approval_status"],
        "marketflow_repository_merge_strategy_approval_digest": digest,
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_merge_strategy_approval_markdown_v1(approval: dict) -> str:
    """Render a sanitized Markdown view without secrets or raw payloads."""
    validation = validate_marketflow_repository_merge_strategy_approval_v1(approval)
    sections = [
        ("Title", ["MarketFlow Repository Merge Strategy Approval v1"]),
        ("MarketFlow Repository Merge Strategy Approval v1", [f"Artifact/status: `{approval['artifact_kind']}` / `{approval['approval_status']}`.", f"Digest: `{validation['marketflow_repository_merge_strategy_approval_digest']}`."]),
        ("Operator Attestation", [f"Decision: `{approval['operator_attestation']['operator_decision']}`.", f"Reference: `{approval['operator_attestation']['operator_reference']}`.", f"Timestamp: `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`."]),
        ("Source Merge Strategy Operator Review", [f"Source digest: `{approval['source_merge_strategy_operator_review_digest']}`.", f"Source commit: `{approval['source_operator_review_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(approval['source_evidence'])}."]),
        ("Repository Context", [str(approval["source_repository_context"])]),
        ("Approval Scope", [approval["approval_scope"]]),
        ("Selected Merge Strategy Package", [f"`{approval['selected_merge_strategy_package']}`: approved for future integration-branch execution only."]),
        ("Approved Integration Branch Plan", [str(approval["approved_integration_branch_plan"])]),
        ("Supporting Packages", [f"{row['package_id']}: {row['approval_status']}" for row in approval["supporting_packages"]]),
        ("Future Execution Boundary", [f"{key}: {value}" for key, value in approval["future_execution_boundary"].items()]),
        ("Next Chain", list(approval["next_chain"])), ("Next Gates", list(approval["next_gates"])),
        ("Risk Controls", list(approval["risk_controls"])),
        ("Authority Boundaries", ["Approval authorizes only a separate future integration-branch execution. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{approval['summary']['passed_checks']} / {approval['summary']['total_checks']} checks pass; {approval['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No integration branch, merge, rebase, squash, cherry-pick, deletion, main/force push, tag mutation, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Merge Strategy Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_merge_strategy_approval_v1(
    output_dir: str | Path, *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_merge_strategy_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_merge_strategy_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryMergeStrategyApprovalError("approval output already exists")
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "marketflow_repository_merge_strategy_approval_digest": approval["marketflow_repository_merge_strategy_approval_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
