"""Offline attestation-gated approval for future integration remediation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_V1 = (
    "marketflow_repository_integration_branch_validation_failure_remediation_approval_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED"
)
REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW = (
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_VALID = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_VALID"
)

SELECTED_REMEDIATION_PACKAGE = (
    source.source.PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE
)
REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE INTEGRATION BRANCH VALIDATION FAILURE REMEDIATION "
    "PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE "
    "MARKETFLOW STAGE FROZEN IGNORED EVIDENCE ROOTS DETACHED INTEGRATION WORKTREE "
    "ACQUISITION MANIFEST REQUIRED NO REGENERATION NO MARKETFLOW COMMIT NO RETRY "
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW"
)
OPERATOR_DECISION = "APPROVE_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION"
OPERATOR_ATTESTATION_VERSION = (
    "marketflow_repository_integration_branch_validation_failure_remediation_approval_attestation_v1"
)

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "f32d7ded083256f4301903de41e1fdf06562b4af0e5bd0fc2c75685d4fd8a301"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_DIAGNOSIS_DIGEST = source.EXPECTED_SOURCE_DIAGNOSIS_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = source.EXPECTED_SOURCE_APPROVAL_DIGEST
ATTEMPTED_EXECUTION_COMMIT = "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ATTESTATION_STRING_FIELDS = {
    "operator_decision": OPERATOR_DECISION,
    "selected_remediation_package": SELECTED_REMEDIATION_PACKAGE,
    "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
    "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "operator_confirms_attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
    "operator_confirms_integration_branch_name": INTEGRATION_BRANCH_NAME,
    "operator_confirms_integration_head_commit": INTEGRATION_HEAD_COMMIT,
    "operator_confirms_selected_remediation_package": SELECTED_REMEDIATION_PACKAGE,
}
ATTESTATION_TRUE_FIELDS = (
    "operator_confirms_first_pytest_failure_authoritative",
    "operator_confirms_later_rerun_diagnostic_only",
    "operator_confirms_approval_scope_only",
    "operator_confirms_no_remediation_execution",
    "operator_confirms_no_evidence_staging",
    "operator_confirms_no_marketflow_copy",
    "operator_confirms_no_marketflow_commit",
    "operator_confirms_no_regeneration",
    "operator_confirms_no_retry",
    "operator_confirms_no_results_review",
    "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_execution_digest",
    "operator_confirms_no_successful_validation_digest",
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
    "package_id": SELECTED_REMEDIATION_PACKAGE,
    "approval_status": "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY",
    "selected": True,
    "approved": True,
    "authorized_for_future_execution": True,
    "executed": False,
}
APPROVED_FUTURE_REMEDIATION_REQUIREMENTS = [
    {
        "requirement_id": requirement_id,
        "source_value": source_value,
        "approval_status": "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY",
    }
    for requirement_id, source_value in source.source.REMEDIATION_REQUIREMENTS.items()
]
APPROVED_FUTURE_REMEDIATION_PLAN = [
    {
        "step_id": f"STEP_{index:02d}",
        "instruction": instruction,
        "approval_status": "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY",
        "execution_status": "NOT_EXECUTED",
    }
    for index, instruction in enumerate(source.source.FUTURE_REMEDIATION_EXECUTION_PLAN, start=1)
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
        source.source.PACKAGE_PARAMETERIZE_INTEGRATION_VALIDATION_WITH_READ_ONLY_EVIDENCE_ROOT,
        source.source.PACKAGE_ADD_PRECHECK_FAIL_CLOSED_FOR_MISSING_IGNORED_EVIDENCE_ROOTS,
        source.source.PACKAGE_COMMIT_MINIMAL_TEST_FIXTURES_FOR_ACQUISITION_REVIEW_ONLY,
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
        source.source.PACKAGE_REGENERATE_ACQUISITION_EVIDENCE_IN_INTEGRATION_WORKTREE,
        source.source.PACKAGE_ACCEPT_LATER_RERUN_AS_SUCCESS,
    )
]

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_V1"
)
NEXT_CHAIN = [
    "Remediation Execution v1, if separately invoked.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1, only after remediation review.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "integration_failure_remediation_execution_if_approved",
    "integration_failure_remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "approval_does_not_execute_remediation",
    "approval_does_not_stage_evidence",
    "approval_does_not_copy_marketflow_outputs",
    "approval_does_not_commit_marketflow_outputs",
    "approval_does_not_regenerate_evidence",
    "approval_does_not_retry_integration",
    "approval_does_not_create_results_review",
    "approval_does_not_mark_integration_successful",
    "approval_does_not_generate_successful_execution_digest",
    "approval_does_not_generate_successful_validation_digest",
    "approval_does_not_delete_integration_branch",
    "approval_does_not_reset_integration_branch",
    "approval_does_not_push_integration_branch",
    "approval_does_not_push_main",
    "approval_does_not_merge_to_main",
    "approval_does_not_force_push",
    "approval_does_not_prune_remotes",
    "approval_does_not_modify_tags",
    "approval_does_not_call_providers",
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
    "first_failed_pytest_remains_authoritative",
    "later_wrong_worktree_rerun_remains_diagnostic_only",
    "blocked_digest_must_not_be_treated_as_ready",
    "selected_remediation_approved_for_future_execution_only",
    "separate_execution_required_before_remediation",
    "separate_results_review_required_after_remediation",
    "separate_retry_approval_required_before_integration_retry",
    "protect_origin_main",
    "preserve_integration_branch_for_diagnosis",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_diagnosis_digest_bound",
    "source_approval_digest_bound",
    "attempted_execution_commit_bound",
    "integration_branch_name_bound",
    "integration_head_commit_bound",
    "first_pytest_failure_preserved",
    "later_wrong_worktree_rerun_preserved_as_diagnostic_only",
    "root_cause_preserved",
    "selected_package_frozen_ignored_evidence_staging",
    "approval_created_true",
    "remediation_selected_true",
    "remediation_approved_true",
    "remediation_authorized_true",
    "ready_for_remediation_execution_true",
    "remediation_executed_false",
    "evidence_staged_false",
    "marketflow_outputs_copied_false",
    "marketflow_outputs_committed_false",
    "evidence_regenerated_false",
    "retry_candidate_created_false",
    "retry_executed_false",
    "results_review_created_false",
    "integration_execution_successful_false",
    "successful_execution_digest_generated_false",
    "successful_validation_digest_generated_false",
    "integration_branch_pushed_false",
    "remote_integration_branch_false",
    "main_merge_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_not_tracked",
    "marketflow_outputs_not_committed",
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


class MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(ValueError):
    """Raised when approval evidence or attestation fails closed."""


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "operator_attestation must be an object"
        )
    for field, expected in ATTESTATION_STRING_FIELDS.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
                f"operator attestation {field} mismatch"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
                f"operator attestation {field} missing"
            )
    for field in ATTESTATION_TRUE_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
                f"operator attestation {field} must be true"
            )


def build_marketflow_repository_integration_branch_validation_failure_remediation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_diagnosis_digest: str,
    operator_confirms_source_approval_digest: str,
    operator_confirms_attempted_execution_commit: str,
    operator_confirms_integration_branch_name: str,
    operator_confirms_integration_head_commit: str,
    operator_confirms_first_pytest_failure_authoritative: bool,
    operator_confirms_later_rerun_diagnostic_only: bool,
    operator_confirms_selected_remediation_package: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_no_remediation_execution: bool,
    operator_confirms_no_evidence_staging: bool,
    operator_confirms_no_marketflow_copy: bool,
    operator_confirms_no_marketflow_commit: bool,
    operator_confirms_no_regeneration: bool,
    operator_confirms_no_retry: bool,
    operator_confirms_no_results_review: bool,
    operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_execution_digest: bool,
    operator_confirms_no_successful_validation_digest: bool,
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
    selected_remediation_package: str = SELECTED_REMEDIATION_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the complete non-secret operator attestation."""
    supplied = locals().copy()
    attestation = {
        "operator_decision": operator_decision,
        "selected_remediation_package": selected_remediation_package,
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
        source.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1()
        if source_review is None
        else deepcopy(source_review)
    )
    try:
        validation = source.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(
            review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "source remediation operator review is invalid"
        ) from exc
    if (
        validation[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"
        ]
        != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "source remediation operator-review digest mismatch"
        )
    return review


def _base_approval(
    source_review: dict | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_attestation(operator_attestation)
    review = _source_review(source_review)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW,
        "selected_remediation_package": SELECTED_REMEDIATION_PACKAGE,
        "created_offline": True,
        "governance_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_remediation_operator_review_artifact_kind": review["artifact_kind"],
        "source_remediation_operator_review_status": review["review_status"],
        "source_remediation_operator_review_scope": review["review_scope"],
        "source_remediation_operator_review_digest": review[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"
        ],
        "source_remediation_candidate_digest": review["source_remediation_candidate_digest"],
        "source_failure_diagnosis_digest": review["source_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": review["source_merge_strategy_approval_digest"],
        **{
            key: review[key]
            for key in (
                "attempted_execution_branch",
                "attempted_execution_commit",
                "integration_branch_name",
                "integration_branch_head_commit",
                "integration_base_commit",
                "integration_source_commit",
                "first_integration_pytest_authoritative",
                "first_integration_pytest_passed",
                "first_integration_pytest_passed_count",
                "first_integration_pytest_failed_count",
                "first_integration_pytest_error_count",
                "first_integration_pytest_skipped_count",
                "later_isolated_rerun_passed",
                "later_isolated_rerun_passed_count",
                "later_isolated_rerun_skipped_count",
                "later_isolated_rerun_overrides_first_failure",
                "representative_failure_domain",
                "required_ready_digest_prefix",
                "actual_blocked_digest_prefix",
                "diagnosed_root_cause",
                "missing_required_file",
                "later_rerun_problem",
            )
        },
        "remediation_selected": True,
        "remediation_approved": True,
        "remediation_authorized": True,
        "remediation_approval_created": True,
        "ready_for_remediation_execution": True,
        "remediation_executed": False,
        "evidence_staged": False,
        "marketflow_outputs_copied": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "integration_retry_candidate_created": False,
        "integration_retry_approved": False,
        "integration_retry_executed": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_execution_digest_generated": False,
        "successful_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "remote_integration_branch_created": False,
        "main_merge_performed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
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
        "approved_future_remediation_requirements": deepcopy(
            APPROVED_FUTURE_REMEDIATION_REQUIREMENTS
        ),
        "approved_future_remediation_plan": deepcopy(APPROVED_FUTURE_REMEDIATION_PLAN),
        "future_plan_approval_status": "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY",
        "future_plan_execution_status": "NOT_EXECUTED",
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "next_chain": deepcopy(NEXT_CHAIN),
        "next_gates": deepcopy(NEXT_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "integration_retry_allowed_now": False,
        "integration_results_review_ready": False,
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
    values = {
        "source_operator_review_digest_bound": (EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST, approval.get("source_remediation_operator_review_digest")),
        "source_candidate_digest_bound": (EXPECTED_SOURCE_CANDIDATE_DIGEST, approval.get("source_remediation_candidate_digest")),
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, approval.get("source_failure_diagnosis_digest")),
        "source_approval_digest_bound": (EXPECTED_SOURCE_APPROVAL_DIGEST, approval.get("source_merge_strategy_approval_digest")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, approval.get("attempted_execution_commit")),
        "integration_branch_name_bound": (INTEGRATION_BRANCH_NAME, approval.get("integration_branch_name")),
        "integration_head_commit_bound": (INTEGRATION_HEAD_COMMIT, approval.get("integration_branch_head_commit")),
        "first_pytest_failure_preserved": ([True, False, 24481, 1300, 500, 7], [approval.get("first_integration_pytest_authoritative"), approval.get("first_integration_pytest_passed"), approval.get("first_integration_pytest_passed_count"), approval.get("first_integration_pytest_failed_count"), approval.get("first_integration_pytest_error_count"), approval.get("first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved_as_diagnostic_only": ([True, False], [approval.get("later_isolated_rerun_passed"), approval.get("later_isolated_rerun_overrides_first_failure")]),
        "root_cause_preserved": ("DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT", approval.get("diagnosed_root_cause")),
        "selected_package_frozen_ignored_evidence_staging": (SELECTED_REMEDIATION_PACKAGE, approval.get("selected_remediation_package")),
        "approval_created_true": (True, approval.get("remediation_approval_created")),
        "remediation_selected_true": (True, approval.get("remediation_selected")),
        "remediation_approved_true": (True, approval.get("remediation_approved")),
        "remediation_authorized_true": (True, approval.get("remediation_authorized")),
        "ready_for_remediation_execution_true": (True, approval.get("ready_for_remediation_execution")),
        "remediation_executed_false": (False, approval.get("remediation_executed")),
        "evidence_staged_false": (False, approval.get("evidence_staged")),
        "marketflow_outputs_copied_false": (False, approval.get("marketflow_outputs_copied")),
        "marketflow_outputs_committed_false": (False, approval.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, approval.get("evidence_regenerated")),
        "retry_candidate_created_false": (False, approval.get("integration_retry_candidate_created")),
        "retry_executed_false": (False, approval.get("integration_retry_executed")),
        "results_review_created_false": (False, approval.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, approval.get("integration_execution_successful")),
        "successful_execution_digest_generated_false": (False, approval.get("successful_execution_digest_generated")),
        "successful_validation_digest_generated_false": (False, approval.get("successful_validation_digest_generated")),
        "integration_branch_pushed_false": (False, approval.get("integration_branch_pushed")),
        "remote_integration_branch_false": (False, approval.get("remote_integration_branch_created")),
        "main_merge_false": (False, approval.get("main_merge_performed")),
        "main_push_false": (False, approval.get("main_push_performed")),
        "origin_main_modified_false": (False, approval.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_not_tracked": (0, approval.get("tracked_marketflow_file_count")),
        "marketflow_outputs_not_committed": (False, approval.get("marketflow_outputs_committed")),
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
        "requirements_approved_for_future_execution": (APPROVED_FUTURE_REMEDIATION_REQUIREMENTS, approval.get("approved_future_remediation_requirements")),
        "future_plan_approved_not_executed": ([APPROVED_FUTURE_REMEDIATION_PLAN, "NOT_EXECUTED"], [approval.get("approved_future_remediation_plan"), approval.get("future_plan_execution_status")]),
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
        "remediation_selected": True,
        "remediation_approved": True,
        "remediation_authorized": True,
        "remediation_approval_created": True,
        "selected_remediation_package": SELECTED_REMEDIATION_PACKAGE,
        "ready_for_remediation_execution": True,
        "remediation_executed": False,
        "integration_retry_allowed_now": False,
        "integration_results_review_ready": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_validation_failure_remediation_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic approval digest."""
    payload = deepcopy(dict(approval))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop(
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest",
        None,
    )
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build future remediation approval from exact review evidence and attestation."""
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval[
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"
    ] = marketflow_repository_integration_branch_validation_failure_remediation_approval_digest_v1(
        approval
    )
    validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
        approval
    )
    return approval


def validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
    approval: dict,
) -> dict:
    """Validate exact attestation, selection, and closed execution boundaries."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval must be an object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
                f"{field} mismatch"
            )
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval checklist failed"
        )
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval digest missing"
        )
    if (
        digest
        != marketflow_repository_integration_branch_validation_failure_remediation_approval_digest_v1(
            approval
        )
    ):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest": digest,
        **{
            key: approval["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_validation_failure_remediation_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized approval view without secrets or raw payloads."""
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
        approval
    )
    sections = [
        ("Operator Attestation", [f"Decision: `{approval['operator_attestation']['operator_decision']}`.", f"Reference: `{approval['operator_attestation']['operator_reference']}`.", f"Timestamp: `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`."]),
        ("Source Operator Review", [f"Artifact/status/digest: `{approval['source_remediation_operator_review_artifact_kind']}` / `{approval['source_remediation_operator_review_status']}` / `{approval['source_remediation_operator_review_digest']}`."]),
        ("Failure Summary", ["The first integration pytest failure remains authoritative: `24481 passed, 1300 failed, 500 errors, 7 skipped`.", "The later passing rerun remains diagnostic-only."]),
        ("Root Cause", [f"`{approval['diagnosed_root_cause']}`.", f"Missing manifest: `{approval['missing_required_file']}`."]),
        ("Approval Scope", [f"`{approval['approval_scope']}`."]),
        ("Selected Remediation Package", [f"`{approval['selected_remediation_package']}`: approved for future remediation execution only; not executed."]),
        ("Approved Future Requirements", [f"`{row['requirement_id']}`: `{row['approval_status']}`." for row in approval["approved_future_remediation_requirements"]]),
        ("Approved Future Plan", [f"`{row['step_id']}`: {row['instruction']} (`{row['approval_status']}` / `{row['execution_status']}`)." for row in approval["approved_future_remediation_plan"]]),
        ("Supporting Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["supporting_packages"]]),
        ("Blocked Packages", [f"`{row['package_id']}`: `{row['approval_status']}`." for row in approval["blocked_packages"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in approval["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in approval["risk_controls"]]),
        ("Authority Boundaries", ["Approval authorizes only a separately invoked future remediation execution. No evidence staging, integration retry, results review, runtime, broker, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No remediation execution, evidence staging, `.marketflow` copy or commit, regeneration, retry, branch push, provider call, data action, or model action occurred."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Validation Failure Remediation Approval v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_v1.json"
    )
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest": approval[
            "marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
