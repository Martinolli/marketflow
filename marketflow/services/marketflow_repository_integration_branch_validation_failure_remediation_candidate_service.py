"""Offline remediation candidate for the failed integration-branch validation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_execution_failure_diagnosis_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1 = (
    "marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY = (
    "REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY"
)

EXPECTED_SOURCE_DIAGNOSIS_DIGEST = (
    "a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = source.SOURCE_APPROVAL_DIGEST
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE = (
    "PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE"
)
PACKAGE_PARAMETERIZE_INTEGRATION_VALIDATION_WITH_READ_ONLY_EVIDENCE_ROOT = (
    "PACKAGE_PARAMETERIZE_INTEGRATION_VALIDATION_WITH_READ_ONLY_EVIDENCE_ROOT"
)
PACKAGE_ADD_PRECHECK_FAIL_CLOSED_FOR_MISSING_IGNORED_EVIDENCE_ROOTS = (
    "PACKAGE_ADD_PRECHECK_FAIL_CLOSED_FOR_MISSING_IGNORED_EVIDENCE_ROOTS"
)
PACKAGE_COMMIT_MINIMAL_TEST_FIXTURES_FOR_ACQUISITION_REVIEW_ONLY = (
    "PACKAGE_COMMIT_MINIMAL_TEST_FIXTURES_FOR_ACQUISITION_REVIEW_ONLY"
)
PACKAGE_REGENERATE_ACQUISITION_EVIDENCE_IN_INTEGRATION_WORKTREE = (
    "PACKAGE_REGENERATE_ACQUISITION_EVIDENCE_IN_INTEGRATION_WORKTREE"
)
PACKAGE_ACCEPT_LATER_RERUN_AS_SUCCESS = "PACKAGE_ACCEPT_LATER_RERUN_AS_SUCCESS"
RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED = "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
BLOCKED_NOT_RECOMMENDED = "BLOCKED_NOT_RECOMMENDED"
BLOCKED_NOT_ALLOWED = "BLOCKED_NOT_ALLOWED"

REMEDIATION_PHILOSOPHY = (
    "The integration validation must execute against the detached integration worktree with all required ignored frozen evidence roots available read-only, without regenerating evidence, committing .marketflow, weakening digest checks, or accepting later reruns as override evidence."
)
REMEDIATION_BOUNDARY = (
    "Candidate-only; no evidence staging, copy, retry, pytest acceptance rerun, digest repair, source rerun, or results review is executed by this artifact."
)
REMEDIATION_GOAL = (
    "Define a controlled future remediation path that makes required ignored evidence roots available to integration validation and prevents false-positive reruns from the wrong worktree."
)

REMEDIATION_PACKAGES = [
    {
        "package_id": PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Before future integration retry, stage or copy required ignored frozen .marketflow evidence roots into the detached integration worktree as untracked read-only local evidence, verify required manifests and frozen digests, then run pytest from that integration worktree.",
        "recommended_for": "Preserving existing frozen evidence while validating the real detached integration worktree.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_PARAMETERIZE_INTEGRATION_VALIDATION_WITH_READ_ONLY_EVIDENCE_ROOT,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Allow integration validation to explicitly reference a read-only frozen evidence root outside the integration worktree, with digest verification and no regeneration.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_ADD_PRECHECK_FAIL_CLOSED_FOR_MISSING_IGNORED_EVIDENCE_ROOTS,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Add a future precheck so integration validation blocks before full pytest if required ignored evidence roots are absent.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_COMMIT_MINIMAL_TEST_FIXTURES_FOR_ACQUISITION_REVIEW_ONLY,
        "status": AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "purpose": "Consider minimal committed fixtures for tests that require acquisition review evidence without committing full .marketflow outputs.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_REGENERATE_ACQUISITION_EVIDENCE_IN_INTEGRATION_WORKTREE,
        "status": BLOCKED_NOT_RECOMMENDED,
        "purpose": "Regenerate acquisition evidence in the integration worktree.",
        "blocked_reason": "Would violate frozen-evidence, no-provider, no-regeneration, and evidence-preservation boundaries unless separately governed by a new evidence chain.",
        "selected": False, "approved": False, "executed": False,
    },
    {
        "package_id": PACKAGE_ACCEPT_LATER_RERUN_AS_SUCCESS,
        "status": BLOCKED_NOT_ALLOWED,
        "purpose": "Treat the later passing rerun as overriding the failed integration gate.",
        "blocked_reason": "The later run executed from the wrong worktree and is diagnostic-only.",
        "selected": False, "approved": False, "executed": False,
    },
]

REMEDIATION_REQUIREMENTS = {
    "required_evidence_roots_identified_before_execution": True,
    "acquisition_provider_evidence_root_required": True,
    "required_manifest_name": "acquisition_provider_evidence_run_manifest.json",
    "source_evidence_root_must_exist_before_staging": True,
    "source_evidence_root_must_be_read_only_input": True,
    "staged_evidence_root_must_remain_untracked": True,
    "staged_evidence_root_must_not_be_committed": True,
    "staged_evidence_root_must_not_be_regenerated": True,
    "digest_manifest_must_be_verified_before_retry": True,
    "required_ready_digest_prefix_must_match_57c0a06e": True,
    "blocked_digest_prefix_783e0013_must_not_be_accepted_as_ready": True,
    "pytest_must_run_from_detached_integration_worktree": True,
    "working_directory_must_be_recorded": True,
    "wrong_worktree_pytest_must_block_retry_acceptance": True,
    "retry_requires_separate_candidate_review_approval_execution_chain": True,
    "integration_results_review_requires_successful_authoritative_retry": True,
}

FUTURE_REMEDIATION_EXECUTION_PLAN = [
    "Identify required ignored evidence roots for acquisition review and any other frozen-output-dependent tests.",
    "Verify source ignored evidence roots exist and are not tracked.",
    "Verify required manifests and known ready-package digest expectations.",
    "Stage evidence roots into the detached integration worktree as untracked local evidence.",
    "Run precheck from the detached integration worktree.",
    "Run full pytest from the detached integration worktree.",
    "Record exact working directory, evidence-root paths, digest checks, and pytest result.",
    "Do not commit .marketflow.",
    "Do not mark integration successful unless the first authoritative retry passes.",
    "Create separate retry execution and results review only after remediation is approved and executed.",
]

REMEDIATION_NON_GOALS = [
    "do_not_retry_now", "do_not_stage_evidence_now", "do_not_copy_marketflow_now",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_commit_marketflow_outputs",
    "do_not_weaken_digest_checks", "do_not_accept_blocked_digest_as_ready",
    "do_not_accept_later_wrong_worktree_rerun", "do_not_create_results_review_now",
    "do_not_push_integration_branch", "do_not_push_main",
    "do_not_delete_or_reset_integration_branch", "do_not_delete_worktree",
    "do_not_force_push", "do_not_modify_tags", "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability", "do_not_authorize_runtime", "do_not_authorize_trading",
]

ROOT_CAUSE_QUESTION_STATUS = {
    "answered_by_diagnosis": [
        "Which evidence root was missing?", "Why did blocked digest appear?",
        "Why did later rerun pass?", "Did later rerun override first failed gate?",
    ],
    "still_requires_remediation_execution_or_review": [
        "Exact full required ready digest, if not already bound in committed constants.",
        "Complete inventory of all ignored evidence roots needed by full integration pytest.",
        "Whether staging only acquisition evidence is sufficient or whether more frozen roots are needed.",
        "Exact precheck implementation for detached worktree validation.",
        "Exact retry execution plan after remediation.",
    ],
}

NEXT_CHAIN = [
    "Integration Branch Validation Failure Remediation Candidate Operator Review v1.",
    "Remediation Approval v1, if selected.", "Remediation Execution v1, if approved.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1, only after remediation review.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]
NEXT_GATES = [
    "integration_failure_remediation_candidate_operator_review",
    "integration_failure_remediation_approval_if_selected",
    "integration_failure_remediation_execution_if_approved",
    "integration_failure_remediation_results_review",
    "integration_branch_retry_candidate_after_remediation",
    "integration_branch_retry_approval_if_selected",
    "integration_branch_retry_execution_if_approved",
    "integration_branch_retry_results_review",
    "main_merge_approval_if_retry_passes",
]
RISK_CONTROLS = [
    "candidate_does_not_execute_remediation", "candidate_does_not_stage_evidence",
    "candidate_does_not_copy_marketflow_outputs", "candidate_does_not_retry_integration",
    "candidate_does_not_create_results_review", "candidate_does_not_mark_integration_successful",
    "candidate_does_not_generate_successful_execution_digest",
    "candidate_does_not_generate_successful_validation_digest",
    "candidate_does_not_delete_integration_branch", "candidate_does_not_reset_integration_branch",
    "candidate_does_not_push_integration_branch", "candidate_does_not_push_main",
    "candidate_does_not_merge_to_main", "candidate_does_not_force_push",
    "candidate_does_not_prune_remotes", "candidate_does_not_modify_tags",
    "candidate_does_not_commit_marketflow_outputs", "candidate_does_not_call_providers",
    "candidate_does_not_acquire_market_data", "candidate_does_not_regenerate_dataset",
    "candidate_does_not_recompute_metrics", "candidate_does_not_train_models",
    "candidate_does_not_score_strategy", "candidate_does_not_generate_recommendations",
    "candidate_does_not_accept_predictive_usefulness", "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime", "candidate_does_not_authorize_broker_execution",
    "first_failed_pytest_remains_authoritative",
    "later_wrong_worktree_rerun_remains_diagnostic_only",
    "blocked_digest_must_not_be_treated_as_ready", "separate_operator_review_required",
    "separate_approval_required_before_remediation",
    "separate_retry_approval_required_before_integration_retry", "protect_origin_main",
    "preserve_integration_branch_for_diagnosis", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1"
)

REQUIRED_CHECK_IDS = [
    "source_diagnosis_digest_bound", "source_approval_digest_bound",
    "attempted_execution_commit_bound", "integration_branch_head_bound",
    "integration_base_commit_bound", "integration_source_commit_bound",
    "first_pytest_failure_preserved", "later_wrong_worktree_rerun_preserved_as_diagnostic_only",
    "representative_digest_mismatch_preserved", "missing_acquisition_manifest_recorded",
    "root_cause_recorded", "candidate_created_true", "candidate_ready_true",
    "recommended_package_present", "remediation_packages_present_6",
    "blocked_packages_present_2", "recommended_package_not_selected",
    "remediation_selected_false", "remediation_approved_false",
    "remediation_authorized_false", "remediation_executed_false",
    "integration_retry_candidate_created_false", "integration_retry_executed_false",
    "integration_results_review_created_false", "integration_execution_successful_false",
    "successful_execution_digest_generated_false", "successful_validation_digest_generated_false",
    "integration_branch_pushed_false", "remote_integration_branch_created_false",
    "main_merge_false", "main_push_false", "origin_main_modified_false",
    "marketflow_outputs_not_tracked", "marketflow_outputs_not_committed",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "broker_not_authorized", "remediation_requirements_defined",
    "future_remediation_plan_defined", "non_goals_defined", "root_cause_question_status_defined",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(ValueError):
    """Raised when candidate evidence or candidate-only boundaries are invalid."""


def _source_diagnosis(source_diagnosis: dict | None) -> dict[str, Any]:
    diagnosis = (
        source.build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1()
        if source_diagnosis is None else deepcopy(source_diagnosis)
    )
    validation = source.validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
        diagnosis
    )
    if validation["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"] != EXPECTED_SOURCE_DIAGNOSIS_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "source failure diagnosis digest mismatch"
        )
    return diagnosis


def _base_candidate(diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY,
        "created_offline": True, "governance_only": True,
        "remediation_candidate_only": True, "operator_review_required": True,
        "source_failure_diagnosis_artifact_kind": diagnosis["artifact_kind"],
        "source_failure_diagnosis_status": diagnosis["diagnosis_status"],
        "source_failure_diagnosis_scope": diagnosis["diagnosis_scope"],
        "source_failure_diagnosis_digest": diagnosis["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"],
        "source_merge_strategy_approval_digest": diagnosis["source_merge_strategy_approval_digest"],
        **{key: diagnosis[key] for key in (
            "attempted_execution_artifact_kind", "attempted_execution_blocked_status",
            "attempted_execution_branch", "attempted_execution_commit", "integration_branch_name",
            "integration_branch_head_commit", "integration_merge_method", "integration_base_commit",
            "integration_source_commit", "first_integration_pytest_authoritative",
            "first_integration_pytest_passed", "first_integration_pytest_passed_count",
            "first_integration_pytest_failed_count", "first_integration_pytest_error_count",
            "first_integration_pytest_skipped_count", "later_isolated_rerun_passed",
            "later_isolated_rerun_passed_count", "later_isolated_rerun_skipped_count",
            "later_isolated_rerun_overrides_first_failure", "representative_failure_domain",
        )},
        "required_ready_digest_prefix": diagnosis["representative_required_digest_prefix"],
        "actual_blocked_digest_prefix": diagnosis["representative_actual_digest_prefix"],
        "diagnosed_root_cause": "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT",
        "missing_required_file": "acquisition_provider_evidence_run_manifest.json",
        "later_rerun_problem": "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE",
        "remediation_candidate_created": True,
        "remediation_candidate_ready_for_operator_review": True,
        "ready_for_remediation_candidate_operator_review": True,
        "remediation_selected": False, "remediation_approved": False,
        "remediation_authorized": False, "remediation_executed": False,
        "integration_retry_candidate_created": False, "integration_retry_approved": False,
        "integration_retry_executed": False, "integration_retry_allowed_now": False,
        "integration_results_review_ready": False, "integration_results_review_created": False,
        "integration_execution_successful": False,
        "successful_execution_digest_generated": False,
        "successful_validation_digest_generated": False,
        "integration_branch_pushed": False, "remote_integration_branch_created": False,
        "main_merge_performed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
        "marketflow_outputs_committed": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "remediation_philosophy": REMEDIATION_PHILOSOPHY,
        "remediation_boundary": REMEDIATION_BOUNDARY, "remediation_goal": REMEDIATION_GOAL,
        "remediation_packages": deepcopy(REMEDIATION_PACKAGES),
        "recommended_remediation_package": PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "recommendation_status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "recommendation_reason": "The diagnosed failure was caused by missing ignored frozen evidence in the detached integration worktree. Staging verified read-only copies preserves digest integrity and tests the actual integration branch content.",
        "remediation_requirements": deepcopy(REMEDIATION_REQUIREMENTS),
        "future_remediation_execution_plan": list(FUTURE_REMEDIATION_EXECUTION_PLAN),
        "future_remediation_execution_plan_status": "PLANNED_NOT_EXECUTED",
        "remediation_non_goals": list(REMEDIATION_NON_GOALS),
        "root_cause_question_status": deepcopy(ROOT_CAUSE_QUESTION_STATUS),
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = candidate.get("remediation_packages", [])
    values: dict[str, tuple[Any, Any]] = {
        "source_diagnosis_digest_bound": (EXPECTED_SOURCE_DIAGNOSIS_DIGEST, candidate.get("source_failure_diagnosis_digest")),
        "source_approval_digest_bound": (EXPECTED_SOURCE_APPROVAL_DIGEST, candidate.get("source_merge_strategy_approval_digest")),
        "attempted_execution_commit_bound": (source.ATTEMPTED_EXECUTION_COMMIT, candidate.get("attempted_execution_commit")),
        "integration_branch_head_bound": (source.INTEGRATION_HEAD_COMMIT, candidate.get("integration_branch_head_commit")),
        "integration_base_commit_bound": (source.INTEGRATION_BASE_COMMIT, candidate.get("integration_base_commit")),
        "integration_source_commit_bound": (source.INTEGRATION_SOURCE_COMMIT, candidate.get("integration_source_commit")),
        "first_pytest_failure_preserved": ([True, False, 24481, 1300, 500, 7], [candidate.get("first_integration_pytest_authoritative"), candidate.get("first_integration_pytest_passed"), candidate.get("first_integration_pytest_passed_count"), candidate.get("first_integration_pytest_failed_count"), candidate.get("first_integration_pytest_error_count"), candidate.get("first_integration_pytest_skipped_count")]),
        "later_wrong_worktree_rerun_preserved_as_diagnostic_only": ([True, False, "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE"], [candidate.get("later_isolated_rerun_passed"), candidate.get("later_isolated_rerun_overrides_first_failure"), candidate.get("later_rerun_problem")]),
        "representative_digest_mismatch_preserved": (["57c0a06e", "783e0013"], [candidate.get("required_ready_digest_prefix"), candidate.get("actual_blocked_digest_prefix")]),
        "missing_acquisition_manifest_recorded": ("acquisition_provider_evidence_run_manifest.json", candidate.get("missing_required_file")),
        "root_cause_recorded": ("DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT", candidate.get("diagnosed_root_cause")),
        "candidate_created_true": (True, candidate.get("remediation_candidate_created")),
        "candidate_ready_true": (True, candidate.get("remediation_candidate_ready_for_operator_review")),
        "recommended_package_present": (PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE, candidate.get("recommended_remediation_package")),
        "remediation_packages_present_6": (6, len(packages)),
        "blocked_packages_present_2": (2, sum(row.get("status", "").startswith("BLOCKED_") for row in packages)),
        "recommended_package_not_selected": (False, packages[0].get("selected") if packages else None),
        "remediation_selected_false": (False, candidate.get("remediation_selected")),
        "remediation_approved_false": (False, candidate.get("remediation_approved")),
        "remediation_authorized_false": (False, candidate.get("remediation_authorized")),
        "remediation_executed_false": (False, candidate.get("remediation_executed")),
        "integration_retry_candidate_created_false": (False, candidate.get("integration_retry_candidate_created")),
        "integration_retry_executed_false": (False, candidate.get("integration_retry_executed")),
        "integration_results_review_created_false": (False, candidate.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, candidate.get("integration_execution_successful")),
        "successful_execution_digest_generated_false": (False, candidate.get("successful_execution_digest_generated")),
        "successful_validation_digest_generated_false": (False, candidate.get("successful_validation_digest_generated")),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, candidate.get("remote_integration_branch_created")),
        "main_merge_false": (False, candidate.get("main_merge_performed")),
        "main_push_false": (False, candidate.get("main_push_performed")),
        "origin_main_modified_false": (False, candidate.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_not_tracked": (0, candidate.get("tracked_marketflow_file_count")),
        "marketflow_outputs_not_committed": (False, candidate.get("marketflow_outputs_committed")),
        "provider_requests_false": (False, candidate.get("provider_requests_made_in_candidate")),
        "market_data_acquisition_false": (False, candidate.get("market_data_acquisition_performed_in_candidate")),
        "dataset_generation_false": (False, candidate.get("dataset_generation_performed_in_candidate")),
        "metric_recomputation_false": (False, candidate.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, candidate.get("model_training_performed")),
        "strategy_scoring_false": (False, candidate.get("strategy_scoring_performed")),
        "recommendations_false": (False, candidate.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "remediation_requirements_defined": (REMEDIATION_REQUIREMENTS, candidate.get("remediation_requirements")),
        "future_remediation_plan_defined": (FUTURE_REMEDIATION_EXECUTION_PLAN, candidate.get("future_remediation_execution_plan")),
        "non_goals_defined": (REMEDIATION_NON_GOALS, candidate.get("remediation_non_goals")),
        "root_cause_question_status_defined": (ROOT_CAUSE_QUESTION_STATUS, candidate.get("root_cause_question_status")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "remediation_candidate_created": True,
        "remediation_candidate_ready_for_operator_review": True,
        "recommended_remediation_package": PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "remediation_selected": False, "remediation_approved": False, "remediation_executed": False,
        "integration_retry_allowed_now": False, "integration_results_review_ready": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic candidate digest."""
    payload = deepcopy(dict(candidate))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
    *, source_diagnosis: dict | None = None,
) -> dict:
    """Build the candidate offline without staging evidence or retrying integration."""
    candidate = _base_candidate(_source_diagnosis(source_diagnosis))
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"] = (
        marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest_v1(candidate)
    )
    validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate exact diagnosis bindings and every candidate-only boundary."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "candidate must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY,
        "source_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1,
        "source_failure_diagnosis_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY,
        "source_failure_diagnosis_scope": source.REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW,
        "source_failure_diagnosis_digest": EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "attempted_execution_commit": source.ATTEMPTED_EXECUTION_COMMIT,
        "integration_branch_head_commit": source.INTEGRATION_HEAD_COMMIT,
        "integration_base_commit": source.INTEGRATION_BASE_COMMIT,
        "integration_source_commit": source.INTEGRATION_SOURCE_COMMIT,
        "required_ready_digest_prefix": "57c0a06e", "actual_blocked_digest_prefix": "783e0013",
        "diagnosed_root_cause": "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT",
        "missing_required_file": "acquisition_provider_evidence_run_manifest.json",
        "later_rerun_problem": "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE",
        "remediation_philosophy": REMEDIATION_PHILOSOPHY, "remediation_boundary": REMEDIATION_BOUNDARY,
        "remediation_goal": REMEDIATION_GOAL, "remediation_packages": REMEDIATION_PACKAGES,
        "recommended_remediation_package": PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE,
        "recommendation_status": RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED,
        "remediation_requirements": REMEDIATION_REQUIREMENTS,
        "future_remediation_execution_plan": FUTURE_REMEDIATION_EXECUTION_PLAN,
        "future_remediation_execution_plan_status": "PLANNED_NOT_EXECUTED",
        "remediation_non_goals": REMEDIATION_NON_GOALS,
        "root_cause_question_status": ROOT_CAUSE_QUESTION_STATUS,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(candidate.get(field), expected, field)
    for field in ("attempted_execution_commit", "integration_branch_head_commit", "integration_base_commit", "integration_source_commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(candidate.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
                f"{field} invalid"
            )
    required_true = (
        "created_offline", "governance_only", "remediation_candidate_only", "operator_review_required",
        "first_integration_pytest_authoritative", "later_isolated_rerun_passed",
        "remediation_candidate_created", "remediation_candidate_ready_for_operator_review",
        "ready_for_remediation_candidate_operator_review", "no_tracked_marketflow_files",
    )
    required_false = (
        "first_integration_pytest_passed", "later_isolated_rerun_overrides_first_failure",
        "remediation_selected", "remediation_approved", "remediation_authorized", "remediation_executed",
        "integration_retry_candidate_created", "integration_retry_approved", "integration_retry_executed",
        "integration_retry_allowed_now", "integration_results_review_ready",
        "integration_results_review_created", "integration_execution_successful",
        "successful_execution_digest_generated", "successful_validation_digest_generated",
        "integration_branch_pushed", "remote_integration_branch_created", "main_merge_performed",
        "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
        "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
    )
    for field in required_true:
        _expect(candidate.get(field), True, field)
    for field in required_false:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("tracked_marketflow_file_count"), 0, "tracked_marketflow_file_count")
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "checklist failed"
        )
    _expect(candidate.get("summary"), _summary(checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "artifact_kind": candidate["artifact_kind"], "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest": digest,
        **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a validated governance-only remediation candidate."""
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
        candidate
    )
    sections = [
        ("Source Failure Diagnosis", [f"Artifact/status/digest: `{candidate['source_failure_diagnosis_artifact_kind']}` / `{candidate['source_failure_diagnosis_status']}` / `{candidate['source_failure_diagnosis_digest']}`."]),
        ("Failure Summary", ["The first integration pytest failure remains authoritative: `24481 passed, 1300 failed, 500 errors, 7 skipped`."]),
        ("Root Cause", [f"`{candidate['diagnosed_root_cause']}`.", f"Missing manifest: `{candidate['missing_required_file']}`.", f"Later rerun problem: `{candidate['later_rerun_problem']}`."]),
        ("Candidate Scope", [f"`{candidate['candidate_scope']}`."]),
        ("Remediation Philosophy", [candidate["remediation_philosophy"], candidate["remediation_boundary"], candidate["remediation_goal"]]),
        ("Proposed Remediation Packages", [f"`{row['package_id']}`: `{row['status']}`; selected/approved/executed `{row['selected']} / {row['approved']} / {row['executed']}`." for row in candidate["remediation_packages"]]),
        ("Recommended Remediation Package", [f"`{candidate['recommended_remediation_package']}` / `{candidate['recommendation_status']}`.", candidate["recommendation_reason"]]),
        ("Remediation Requirements", [f"`{key}`: `{value}`" for key, value in candidate["remediation_requirements"].items()]),
        ("Future Remediation Execution Plan", candidate["future_remediation_execution_plan"]),
        ("Remediation Non-Goals", [f"`{row}`" for row in candidate["remediation_non_goals"]]),
        ("Root-Cause Question Status", [f"Answered: {row}" for row in candidate["root_cause_question_status"]["answered_by_diagnosis"]] + [f"Open: {row}" for row in candidate["root_cause_question_status"]["still_requires_remediation_execution_or_review"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No remediation, evidence staging, integration retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The candidate requires separate operator review and approval.", "The first failed pytest remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Validation Failure Remediation Candidate v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
    output_dir: str | Path,
    *, source_diagnosis: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
        source_diagnosis=source_diagnosis
    )
    validation = validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError(
            "remediation candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"], "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest": validation[
            "marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
