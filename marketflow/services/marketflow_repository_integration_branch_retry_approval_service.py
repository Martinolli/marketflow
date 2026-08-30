"""Offline attestation-bound approval for a future integration branch retry."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_candidate_operator_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_V1 = (
    "marketflow_repository_integration_branch_retry_approval_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_VALID = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_VALID"
)

SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE = (
    source.source.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE
)
APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY = (
    "APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY"
)
AVAILABLE_NOT_SELECTED = "AVAILABLE_NOT_SELECTED"
BLOCKED_NOT_APPROVED = "BLOCKED_NOT_APPROVED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE INTEGRATION BRANCH RETRY "
    "PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE "
    "MARKETFLOW FULL PYTEST FROM REMEDIATED DETACHED WORKTREE FIRST RETRY AUTHORITATIVE "
    "NO WRONG WORKTREE NO MAIN PUSH "
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN"
)
REQUIRED_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ATTESTATION_PHRASE = (
    REQUIRED_OPERATOR_ATTESTATION_PHRASE
)
OPERATOR_DECISION = "APPROVE_INTEGRATION_BRANCH_RETRY"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_retry_approval_attestation_v1"
)

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "8adea54bd72bc3d1c0ea284930ea836101594e8ed12a971863c2032e9fb3a2ce"
)
EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST
EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST = (
    source.EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST
)
EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST = source.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST
EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST = (
    source.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST = source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST
EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST

ATTEMPTED_EXECUTION_BRANCH = "feature/marketflow-repository-integration-branch-execution-v1"
ATTEMPTED_EXECUTION_COMMIT = "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba"
ORIGINAL_BLOCKED_STATUS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED"
)
EXPECTED_ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"
DETACHED_INTEGRATION_WORKTREE_PATH = str(
    source.source.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False)
)
STAGED_EVIDENCE_ROOT_PATH = str(source.source.EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False))
STAGED_REQUIRED_MANIFEST_PATH = str(source.source.EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False))

ATTESTATION_STRING_FIELDS = {
    "operator_decision": OPERATOR_DECISION,
    "selected_integration_branch_retry_package": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
    "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
    "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_retry_candidate_digest": EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST,
    "operator_confirms_source_remediation_results_review_digest": EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
    "operator_confirms_source_remediation_execution_digest": EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST,
    "operator_confirms_source_staged_inventory_digest": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
    "operator_confirms_attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
    "operator_confirms_original_blocked_status": ORIGINAL_BLOCKED_STATUS,
    "operator_confirms_origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "operator_confirms_integration_branch_name": INTEGRATION_BRANCH_NAME,
    "operator_confirms_integration_branch_head": INTEGRATION_HEAD_COMMIT,
    "operator_confirms_detached_worktree_path": DETACHED_INTEGRATION_WORKTREE_PATH,
    "operator_confirms_detached_worktree_head": INTEGRATION_HEAD_COMMIT,
    "operator_confirms_staged_evidence_root_path": STAGED_EVIDENCE_ROOT_PATH,
    "operator_confirms_staged_evidence_digest": EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
    "operator_confirms_selected_retry_package": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
}
ATTESTATION_TRUE_FIELDS = (
    "operator_confirms_first_failed_pytest_authoritative",
    "operator_confirms_later_wrong_worktree_rerun_diagnostic_only",
    "operator_confirms_approval_scope_only",
    "operator_confirms_no_retry_execution",
    "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review",
    "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_execution_digest",
    "operator_confirms_no_successful_validation_digest",
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
)

APPROVED_SELECTED_PACKAGE = {
    "package_id": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
    "approval_status": APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY,
    "selected": True,
    "approved": True,
    "authorized_for_future_execution": True,
    "executed": False,
}
APPROVED_FUTURE_RETRY_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "source_value": source_value,
        "approval_status": APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY,
    }
    for requirement_id, source_value in source.source.FUTURE_RETRY_REQUIREMENTS.items()
]
APPROVED_FUTURE_RETRY_PLAN = [
    {
        "step_id": f"STEP_{index:02d}",
        "instruction": instruction,
        "approval_status": APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY,
        "execution_status": NOT_EXECUTED,
    }
    for index, instruction in enumerate(source.source.FUTURE_RETRY_EXECUTION_PLAN, start=1)
]
SUPPORTING_PACKAGES = [
    {
        "package_id": package_id,
        "approval_status": AVAILABLE_NOT_SELECTED,
        "selected": False,
        "approved": False,
        "authorized_for_future_execution": False,
        "executed": False,
    }
    for package_id in (
        source.source.PACKAGE_PRECHECK_THEN_FULL_PYTEST_RETRY_FROM_DETACHED_WORKTREE,
        source.source.PACKAGE_TARGETED_ACQUISITION_REVIEW_TESTS_THEN_FULL_PYTEST_RETRY,
        source.source.PACKAGE_FULL_PYTEST_RETRY_WITH_CACHE_AND_ENVIRONMENT_GUARD,
    )
]
BLOCKED_PACKAGES = [
    {
        "package_id": package_id,
        "approval_status": BLOCKED_NOT_APPROVED,
        "selected": False,
        "approved": False,
        "authorized_for_future_execution": False,
        "executed": False,
    }
    for package_id in (
        source.source.PACKAGE_ACCEPT_REMEDIATION_RESULTS_WITHOUT_INTEGRATION_RETRY,
        source.source.PACKAGE_RETRY_FROM_FEATURE_WORKTREE_OR_ROOT_WORKTREE,
    )
]

RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1"
NEXT_CHAIN = [
    "Integration Branch Retry Execution v1, if separately invoked.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval v1, only if retry results review passes.",
    "Main Merge Execution v1, only if separately approved.",
    "Branch Cleanup Candidate v1, only after merge strategy is settled.",
]
NEXT_GATES = [
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
    "main_merge_execution_if_approved",
    "branch_cleanup_candidate_after_merge_strategy",
]
RISK_CONTROLS = [
    "approval_does_not_run_retry",
    "approval_does_not_run_pytest",
    "approval_does_not_create_retry_execution",
    "approval_does_not_create_retry_results_review",
    "approval_does_not_create_integration_results_review",
    "approval_does_not_mark_integration_successful",
    "approval_does_not_generate_successful_integration_execution_digest",
    "approval_does_not_generate_successful_integration_validation_digest",
    "approval_does_not_stage_additional_evidence",
    "approval_does_not_modify_staged_evidence",
    "approval_does_not_regenerate_evidence",
    "approval_does_not_call_providers",
    "approval_does_not_commit_marketflow_outputs",
    "approval_does_not_push_integration_branch",
    "approval_does_not_push_main",
    "approval_does_not_delete_integration_branch",
    "approval_does_not_delete_worktree",
    "approval_does_not_force_push",
    "approval_does_not_prune_remotes",
    "approval_does_not_modify_tags",
    "approval_does_not_acquire_market_data",
    "approval_does_not_regenerate_dataset",
    "approval_does_not_recompute_metrics",
    "approval_does_not_train_models",
    "approval_does_not_score_strategy",
    "approval_does_not_generate_recommendations",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_broker_execution",
    "selected_retry_approved_for_future_execution_only",
    "staged_frozen_evidence_must_remain_untracked",
    "wrong_worktree_retry_must_fail_closed",
    "separate_execution_required_before_retry",
    "separate_results_review_required_after_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound",
    "source_retry_candidate_digest_bound",
    "source_remediation_results_review_digest_bound",
    "source_remediation_execution_digest_bound",
    "source_staged_inventory_digest_bound",
    "attempted_execution_commit_bound",
    "original_blocked_status_bound",
    "first_failed_pytest_preserved",
    "later_wrong_worktree_rerun_preserved",
    "origin_main_at_approval_bound",
    "integration_branch_head_bound",
    "detached_worktree_path_bound",
    "detached_worktree_head_bound",
    "staged_evidence_root_bound",
    "staged_evidence_digest_bound",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_package_authoritative_retry",
    "approval_created_true",
    "retry_selected_true",
    "retry_approved_true",
    "retry_authorized_true",
    "ready_for_retry_execution_true",
    "retry_executed_false",
    "retry_results_review_created_false",
    "integration_results_review_created_false",
    "integration_execution_successful_false",
    "successful_integration_execution_digest_generated_false",
    "successful_integration_validation_digest_generated_false",
    "integration_branch_pushed_false",
    "remote_integration_branch_created_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "evidence_regenerated_false",
    "provider_requests_false",
    "market_data_acquisition_false",
    "dataset_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "recommendations_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "broker_not_authorized",
    "requirements_approved_for_future_execution",
    "future_plan_approved_not_executed",
    "supporting_packages_not_selected",
    "blocked_packages_not_approved",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryApprovalError(ValueError):
    """Raised when retry approval evidence or attestation fails closed."""


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "operator_attestation must be an object"
        )
    for field, expected in ATTESTATION_STRING_FIELDS.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
                f"operator attestation {field} mismatch"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_TRUE_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
                f"operator attestation {field} must be true"
            )


def build_marketflow_repository_integration_branch_retry_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_retry_candidate_digest: str,
    operator_confirms_source_remediation_results_review_digest: str,
    operator_confirms_source_remediation_execution_digest: str,
    operator_confirms_source_staged_inventory_digest: str,
    operator_confirms_attempted_execution_commit: str,
    operator_confirms_original_blocked_status: str,
    operator_confirms_first_failed_pytest_authoritative: bool,
    operator_confirms_later_wrong_worktree_rerun_diagnostic_only: bool,
    operator_confirms_origin_main_commit: str,
    operator_confirms_integration_branch_name: str,
    operator_confirms_integration_branch_head: str,
    operator_confirms_detached_worktree_path: str,
    operator_confirms_detached_worktree_head: str,
    operator_confirms_staged_evidence_root_path: str,
    operator_confirms_staged_evidence_digest: str,
    operator_confirms_selected_retry_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_retry_execution: bool,
    operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_execution_digest: bool,
    operator_confirms_no_successful_validation_digest: bool,
    operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_force_push: bool,
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
    selected_integration_branch_retry_package: str = SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the complete non-secret operator attestation."""
    supplied = locals().copy()
    attestation = {
        "operator_decision": operator_decision,
        "selected_integration_branch_retry_package": selected_integration_branch_retry_package,
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


DEFAULT_SOURCE_REVIEW = (
    source.build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1()
)


def _source_review(source_review: dict | None) -> dict[str, Any]:
    review = deepcopy(DEFAULT_SOURCE_REVIEW if source_review is None else source_review)
    try:
        validation = source.validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
            review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "source retry candidate operator review is invalid"
        ) from exc
    if (
        validation["marketflow_repository_integration_branch_retry_candidate_operator_review_digest"]
        != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
    ):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "source retry candidate operator-review digest mismatch"
        )
    return review


def _base_approval(
    source_review: dict | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_attestation(operator_attestation)
    review = _source_review(source_review)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_integration_branch_retry_package": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_integration_branch_retry_operator_review_artifact_kind": review["artifact_kind"],
        "source_integration_branch_retry_operator_review_status": review["review_status"],
        "source_integration_branch_retry_operator_review_scope": review["review_scope"],
        "source_integration_branch_retry_operator_review_digest": review[
            "marketflow_repository_integration_branch_retry_candidate_operator_review_digest"
        ],
        "source_integration_branch_retry_candidate_digest": review[
            "source_integration_branch_retry_candidate_digest"
        ],
        "source_remediation_results_review_digest": review[
            "source_remediation_results_review_digest"
        ],
        "source_remediation_results_review_evidence_manifest_digest": review[
            "source_remediation_results_review_evidence_manifest_digest"
        ],
        "source_remediation_execution_digest": review["source_remediation_execution_digest"],
        "source_remediation_execution_evidence_manifest_digest": review[
            "source_remediation_execution_evidence_manifest_digest"
        ],
        "source_staged_inventory_digest": review["source_staged_inventory_digest"],
        "source_worktree_restoration_results_review_digest": review[
            "source_worktree_restoration_results_review_digest"
        ],
        "source_remediation_approval_digest": review["source_remediation_approval_digest"],
        "source_failure_diagnosis_digest": review["source_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": review["source_merge_strategy_approval_digest"],
        "attempted_execution_branch": review["attempted_execution_branch"],
        "attempted_execution_commit": review["attempted_execution_commit"],
        "original_blocked_artifact": review["original_blocked_artifact"],
        "original_blocked_status": review["original_blocked_status"],
        "first_integration_pytest_authoritative": review["first_integration_pytest_authoritative"],
        "first_integration_pytest_passed": review["first_integration_pytest_passed"],
        "first_integration_pytest_passed_count": review["first_integration_pytest_passed_count"],
        "first_integration_pytest_failed_count": review["first_integration_pytest_failed_count"],
        "first_integration_pytest_error_count": review["first_integration_pytest_error_count"],
        "first_integration_pytest_skipped_count": review["first_integration_pytest_skipped_count"],
        "later_wrong_worktree_rerun_diagnostic_only": review[
            "later_wrong_worktree_rerun_diagnostic_only"
        ],
        "later_wrong_worktree_rerun_passed_count": review[
            "later_wrong_worktree_rerun_passed_count"
        ],
        "later_wrong_worktree_rerun_skipped_count": review[
            "later_wrong_worktree_rerun_skipped_count"
        ],
        "later_wrong_worktree_rerun_overrides_first_failure": review[
            "later_wrong_worktree_rerun_overrides_first_failure"
        ],
        "representative_failure_domain": review["representative_failure_domain"],
        "required_ready_digest_prefix": review["required_ready_digest_prefix"],
        "blocked_digest_prefix": review["blocked_digest_prefix"],
        "diagnosed_root_cause": review["diagnosed_root_cause"],
        "origin_main_commit_at_approval": review["origin_main_commit_at_review"],
        "integration_branch_name": review["integration_branch_name"],
        "integration_branch_head_commit_at_approval": review[
            "integration_branch_head_commit_at_review"
        ],
        "integration_branch_matches_required_head_at_approval": review[
            "integration_branch_matches_required_head_at_review"
        ],
        "remote_integration_branch_exists_at_approval": review[
            "remote_integration_branch_exists_at_review"
        ],
        "detached_integration_worktree_path": review["detached_integration_worktree_path"],
        "detached_integration_worktree_exists_at_approval": review[
            "detached_integration_worktree_exists_at_review"
        ],
        "detached_integration_worktree_head_commit_at_approval": review[
            "detached_integration_worktree_head_commit_at_review"
        ],
        "detached_integration_worktree_head_verified_at_approval": review[
            "detached_integration_worktree_head_verified_at_review"
        ],
        "detached_integration_worktree_is_detached_at_approval": review[
            "detached_integration_worktree_is_detached_at_review"
        ],
        "detached_integration_worktree_clean_at_approval": review[
            "detached_integration_worktree_clean_at_review"
        ],
        "staged_evidence_root_path": review["staged_evidence_root_path"],
        "staged_required_manifest_path": review["staged_required_manifest_path"],
        "staged_evidence_file_count_at_approval": review["staged_evidence_file_count_at_review"],
        "staged_evidence_total_bytes_at_approval": review["staged_evidence_total_bytes_at_review"],
        "staged_evidence_manifest_digest_at_approval": review[
            "staged_evidence_manifest_digest_at_review"
        ],
        "staged_evidence_root_untracked_at_approval": review[
            "staged_evidence_root_untracked_at_review"
        ],
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "integration_branch_retry_selected": True,
        "integration_branch_retry_approved": True,
        "integration_branch_retry_authorized": True,
        "integration_branch_retry_approval_created": True,
        "ready_for_integration_branch_retry_execution": True,
        "integration_branch_retry_executed": False,
        "integration_branch_retry_results_review_created": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "approved_selected_package": deepcopy(APPROVED_SELECTED_PACKAGE),
        "approved_future_retry_requirements": deepcopy(APPROVED_FUTURE_RETRY_REQUIREMENTS),
        "approved_future_retry_plan": deepcopy(APPROVED_FUTURE_RETRY_PLAN),
        "future_plan_approval_status": APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY,
        "future_plan_execution_status": NOT_EXECUTED,
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = actual == expected
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "Requirement satisfied." if passed else "Required approval boundary mismatch.",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation", {})
    values = {
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_integration_branch_retry_operator_review_digest")),
        "source_retry_candidate_digest_bound": (EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST, approval.get("source_integration_branch_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, approval.get("source_remediation_results_review_digest")),
        "source_remediation_execution_digest_bound": (EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST, approval.get("source_remediation_execution_digest")),
        "source_staged_inventory_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, approval.get("source_staged_inventory_digest")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, approval.get("attempted_execution_commit")),
        "original_blocked_status_bound": (ORIGINAL_BLOCKED_STATUS, approval.get("original_blocked_status")),
        "first_failed_pytest_preserved": ([True, False, 24481, 1300, 500, 7], [approval.get("first_integration_pytest_authoritative"), approval.get("first_integration_pytest_passed"), approval.get("first_integration_pytest_passed_count"), approval.get("first_integration_pytest_failed_count"), approval.get("first_integration_pytest_error_count"), approval.get("first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved": ([True, False], [approval.get("later_wrong_worktree_rerun_diagnostic_only"), approval.get("later_wrong_worktree_rerun_overrides_first_failure")]),
        "origin_main_at_approval_bound": (EXPECTED_ORIGIN_MAIN_COMMIT, approval.get("origin_main_commit_at_approval")),
        "integration_branch_head_bound": (INTEGRATION_HEAD_COMMIT, approval.get("integration_branch_head_commit_at_approval")),
        "detached_worktree_path_bound": (DETACHED_INTEGRATION_WORKTREE_PATH, approval.get("detached_integration_worktree_path")),
        "detached_worktree_head_bound": (INTEGRATION_HEAD_COMMIT, approval.get("detached_integration_worktree_head_commit_at_approval")),
        "staged_evidence_root_bound": (STAGED_EVIDENCE_ROOT_PATH, approval.get("staged_evidence_root_path")),
        "staged_evidence_digest_bound": (EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST, approval.get("staged_evidence_manifest_digest_at_approval")),
        "operator_decision_matches": (OPERATOR_DECISION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "approval_scope_only": (REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN, approval.get("approval_scope")),
        "selected_package_authoritative_retry": (SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE, approval.get("selected_integration_branch_retry_package")),
        "approval_created_true": (True, approval.get("integration_branch_retry_approval_created")),
        "retry_selected_true": (True, approval.get("integration_branch_retry_selected")),
        "retry_approved_true": (True, approval.get("integration_branch_retry_approved")),
        "retry_authorized_true": (True, approval.get("integration_branch_retry_authorized")),
        "ready_for_retry_execution_true": (True, approval.get("ready_for_integration_branch_retry_execution")),
        "retry_executed_false": (False, approval.get("integration_branch_retry_executed")),
        "retry_results_review_created_false": (False, approval.get("integration_branch_retry_results_review_created")),
        "integration_results_review_created_false": (False, approval.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, approval.get("integration_execution_successful")),
        "successful_integration_execution_digest_generated_false": (False, approval.get("successful_integration_execution_digest_generated")),
        "successful_integration_validation_digest_generated_false": (False, approval.get("successful_integration_validation_digest_generated")),
        "integration_branch_pushed_false": (False, approval.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, approval.get("remote_integration_branch_created")),
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
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_RETRY_REQUIREMENTS, approval.get("approved_future_retry_requirements")),
        "future_plan_approved_not_executed": ([APPROVED_FUTURE_RETRY_PLAN, NOT_EXECUTED], [approval.get("approved_future_retry_plan"), approval.get("future_plan_execution_status")]),
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
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "integration_branch_retry_selected": True,
        "integration_branch_retry_approved": True,
        "integration_branch_retry_authorized": True,
        "integration_branch_retry_approval_created": True,
        "selected_integration_branch_retry_package": SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
        "ready_for_integration_branch_retry_execution": True,
        "integration_branch_retry_executed": False,
        "integration_branch_retry_results_review_created": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic approval digest."""
    payload = deepcopy(dict(approval))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_retry_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build future retry approval from exact review evidence and attestation."""
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_integration_branch_retry_approval_digest"] = (
        marketflow_repository_integration_branch_retry_approval_digest_v1(approval)
    )
    validate_marketflow_repository_integration_branch_retry_approval_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_approval_v1(
    approval: dict,
) -> dict:
    """Validate exact attestation, retry selection, and closed execution boundaries."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "approval must be an object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(f"{field} mismatch")
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "approval checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "approval checklist failed"
        )
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get("marketflow_repository_integration_branch_retry_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError("approval digest missing")
    if digest != marketflow_repository_integration_branch_retry_approval_digest_v1(approval):
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError("approval digest mismatch")
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_approval_digest": digest,
        **{
            key: approval["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized approval view without secrets or raw payloads."""
    validation = validate_marketflow_repository_integration_branch_retry_approval_v1(approval)
    sections = [
        ("Operator Attestation", [f"Decision: `{approval['operator_attestation']['operator_decision']}`.", f"Reference: `{approval['operator_attestation']['operator_reference']}`.", f"Timestamp: `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`."]),
        ("Source Retry Candidate Operator Review", [f"Artifact/status/digest: `{approval['source_integration_branch_retry_operator_review_artifact_kind']}` / `{approval['source_integration_branch_retry_operator_review_status']}` / `{approval['source_integration_branch_retry_operator_review_digest']}`."]),
        ("Source Remediation Results Review", [f"Results-review digest: `{approval['source_remediation_results_review_digest']}`.", f"Execution digest: `{approval['source_remediation_execution_digest']}`."]),
        ("Failure Context", ["The first integration pytest remains authoritative: `24481 passed, 1300 failed, 500 errors, 7 skipped`.", "The later `26842 passed, 7 skipped` wrong-worktree rerun remains diagnostic-only."]),
        ("Remediation Context", ["The remediated detached integration worktree contains seven matching ignored evidence files; staged evidence remains untracked and unchanged."]),
        ("Approval Scope", [f"`{approval['approval_scope']}`."]),
        ("Selected Retry Package", [f"`{approval['selected_integration_branch_retry_package']}`: approved for future retry execution only; not executed."]),
        ("Approved Future Retry Requirements", [f"`{row['requirement_id']}`: `{row['approval_status']}`." for row in approval["approved_future_retry_requirements"]]),
        ("Approved Future Retry Plan", [f"`{row['step_id']}`: {row['instruction']} (`{row['approval_status']}` / `{row['execution_status']}`)." for row in approval["approved_future_retry_plan"]]),
        ("Supporting Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["supporting_packages"]]),
        ("Blocked Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in approval["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in approval["risk_controls"]]),
        ("Authority Boundaries", ["Approval authorizes only a separately invoked future retry execution. It creates no retry execution, results review, integration-success, main-merge, runtime, broker, or trading authority."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No retry pytest, evidence mutation, `.marketflow` commit, protected-ref push, provider call, data action, model action, or tag mutation occurred."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_integration_branch_retry_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_retry_approval_digest": approval[
            "marketflow_repository_integration_branch_retry_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
