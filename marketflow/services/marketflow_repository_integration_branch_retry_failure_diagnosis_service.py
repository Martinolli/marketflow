"""Build an offline diagnosis of the failed authoritative integration retry."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1 = (
    "marketflow_repository_integration_branch_retry_failure_diagnosis_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_RETRY_EXECUTION_ARTIFACT_KIND = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED"
)
SOURCE_RETRY_EXECUTION_STATUS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED"
)
SOURCE_RETRY_EXECUTION_SCOPE = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SOURCE_RETRY_APPROVAL_DIGEST = "5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1"
SOURCE_RETRY_OPERATOR_REVIEW_DIGEST = "8adea54bd72bc3d1c0ea284930ea836101594e8ed12a971863c2032e9fb3a2ce"
SOURCE_RETRY_CANDIDATE_DIGEST = "35598851bf4bfec55385cd6e2559ebb933161d846302a3032861e72ed07985eb"
SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST = "b3f86722e05d7692805e51ca86f125df79099a10e0f4bb4d39ea9c824472ec67"
SOURCE_REMEDIATION_EXECUTION_DIGEST = "4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346"
SOURCE_STAGED_INVENTORY_DIGEST = "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
SOURCE_FAILURE_DIAGNOSIS_DIGEST = "a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947"
SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST = "34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c"

RETRY_EXECUTION_BRANCH = "feature/marketflow-repository-integration-branch-retry-execution-v1"
RETRY_EXECUTION_COMMIT = "ab178b65c69f0274b0abbf9c20df102d35e78d34"
RETRY_PYTEST_COMMAND = r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q"
RETRY_PYTEST_WORKING_DIRECTORY = r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1"
ORIGIN_MAIN_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_BRANCH_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"

ORIGINAL_FAILED_RUN = {"passed": 24481, "failed": 1300, "errors": 500, "skipped": 7}
RETRY_FAILED_RUN = {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
RUN_DELTA = {"passed": 396, "failed": -8, "errors": -388, "skipped": 0}
COMPARISON_INTERPRETATION = (
    "Evidence staging corrected or reduced some environment/evidence-root failures, "
    "but substantial failures and errors remain. The retry remains blocked."
)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_CANDIDATE_NOT_CREATED"
RECOMMENDED_ACTION = (
    "CREATE_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_FROM_FAILURE_DOMAIN_DIAGNOSIS"
)

DIAGNOSIS_DOMAINS = [
    {"domain": "RETRY_GATE_STATUS", "finding": "AUTHORITATIVE_RETRY_FAILED"},
    {"domain": "FAILURE_VOLUME", "finding": "RETRY_FAILURES_AND_ERRORS_REDUCED_BUT_GATE_STILL_FAILED"},
    {"domain": "ORIGINAL_FAILURE_COMPARISON", "finding": "RETRY_IMPROVED_ERROR_COUNT_BUT_DID_NOT_PASS"},
    {"domain": "DETACHED_WORKTREE_VALIDITY", "finding": "RETRY_EXECUTED_FROM_CORRECT_DETACHED_WORKTREE"},
    {"domain": "STAGED_EVIDENCE_VALIDITY", "finding": "STAGED_EVIDENCE_REMAINED_PRESENT_UNCHANGED_AND_UNTRACKED"},
    {"domain": "WRONG_WORKTREE_CONTROL", "finding": "ROOT_REGRESSION_IS_NOT_RETRY_EVIDENCE"},
    {"domain": "REMAINING_FAILURE_DOMAIN", "finding": "REQUIRES_TEST_FAILURE_DOMAIN_ANALYSIS"},
    {"domain": "PYTEST_ERROR_DOMAIN", "finding": "112_ERRORS_REQUIRE_FIRST_ORDER_CLASSIFICATION"},
    {"domain": "PYTEST_FAILURE_DOMAIN", "finding": "1292_FAILURES_REQUIRE_MODULE_AND_CONSTANT_TRACE"},
    {"domain": "AUTHORITY_BOUNDARY", "finding": "NO_RESULTS_REVIEW_OR_MAIN_MERGE_ALLOWED"},
    {"domain": "NEXT_REMEDIATION_DIRECTION", "finding": "PREPARE_RETRY_FAILURE_DIAGNOSIS_BASED_REMEDIATION_OR_METHOD_CANDIDATE"},
]

ROOT_CAUSE_QUESTIONS = [
    "Which test modules account for the 112 retry errors?",
    "Which test modules account for the 1,292 retry failures?",
    "Are remaining failures caused by additional ignored evidence roots missing from the detached worktree?",
    "Are remaining failures caused by branch/content differences between root feature worktree and detached integration worktree?",
    "Are remaining failures caused by path assumptions, cwd assumptions, absolute paths, or repository-root discovery?",
    "Are remaining failures caused by digest constants from later feature branches not present in the integration merge?",
    "Are remaining failures caused by generated-output assumptions outside acquisition evidence?",
    "Which failures disappeared compared with the original 500-error run?",
    "Which failures persist unchanged?",
    "What is the first failing test module by pytest order?",
    "What is the first error trace by pytest order?",
    "Is there a small targeted diagnostic command that can classify the failures without being treated as retry evidence?",
    "What remediation package is needed before another retry?",
]

NEXT_CHAIN = [
    "Integration Branch Retry Failure Remediation or Method Candidate v1.",
    "Candidate Operator Review v1.",
    "Approval v1, if selected.",
    "Execution v1, if approved.",
    "Results Review v1.",
    "New Retry Candidate v1, only after remediation/method review.",
    "New Retry Approval v1, if selected.",
    "New Retry Execution v1, if approved.",
    "New Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]

NEXT_GATES = [
    "retry_failure_remediation_or_method_candidate",
    "retry_failure_remediation_or_method_operator_review",
    "retry_failure_remediation_or_method_approval_if_selected",
    "retry_failure_remediation_or_method_execution_if_approved",
    "retry_failure_remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "diagnosis_does_not_rerun_retry", "diagnosis_does_not_run_full_pytest_as_retry_evidence",
    "diagnosis_does_not_create_retry_results_review", "diagnosis_does_not_create_integration_results_review",
    "diagnosis_does_not_mark_integration_successful", "diagnosis_does_not_generate_successful_integration_execution_digest",
    "diagnosis_does_not_generate_successful_integration_validation_digest", "diagnosis_does_not_modify_staged_evidence",
    "diagnosis_does_not_stage_additional_evidence", "diagnosis_does_not_regenerate_evidence",
    "diagnosis_does_not_call_providers", "diagnosis_does_not_commit_marketflow_outputs",
    "diagnosis_does_not_push_integration_branch", "diagnosis_does_not_push_main",
    "diagnosis_does_not_delete_integration_branch", "diagnosis_does_not_delete_worktree",
    "diagnosis_does_not_force_push", "diagnosis_does_not_prune_remotes",
    "diagnosis_does_not_modify_tags", "diagnosis_does_not_acquire_market_data",
    "diagnosis_does_not_regenerate_dataset", "diagnosis_does_not_recompute_metrics",
    "diagnosis_does_not_train_models", "diagnosis_does_not_score_strategy",
    "diagnosis_does_not_generate_recommendations", "diagnosis_does_not_accept_predictive_usefulness",
    "diagnosis_does_not_accept_profitability", "diagnosis_does_not_authorize_runtime",
    "diagnosis_does_not_authorize_broker_execution", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "new_remediation_or_method_candidate_required",
    "new_retry_approval_required_before_any_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_retry_approval_digest_bound", "source_retry_operator_review_digest_bound",
    "source_retry_candidate_digest_bound", "source_remediation_results_review_digest_bound",
    "source_remediation_execution_digest_bound", "source_staged_inventory_digest_bound",
    "retry_execution_branch_bound", "retry_execution_commit_bound", "retry_pytest_command_bound",
    "retry_pytest_working_directory_bound", "retry_pytest_ran_from_detached_worktree_true",
    "retry_pytest_first_result_authoritative_true", "retry_pytest_failed_recorded",
    "retry_pytest_counts_recorded", "success_digest_not_generated", "validation_digest_not_generated",
    "retry_results_review_created_false", "integration_results_review_created_false",
    "integration_execution_successful_false", "origin_main_unchanged", "integration_branch_head_unchanged",
    "detached_worktree_head_unchanged", "staged_evidence_unchanged", "marketflow_outputs_not_tracked",
    "root_regression_not_retry_evidence", "diagnosis_created_true", "diagnosis_ready_true",
    "diagnosis_domains_defined", "diagnostic_comparison_defined", "root_cause_questions_defined",
    "recommended_next_task_defined", "retry_results_review_blocked_true", "main_merge_approval_blocked_true",
    "integration_retry_allowed_now_false", "integration_branch_pushed_false",
    "remote_integration_branch_created_false", "main_push_false", "origin_main_modified_false",
    "provider_requests_false", "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError(ValueError):
    """Raised when retry-failure evidence or authority boundaries are invalid."""


def _source_execution() -> dict[str, Any]:
    return {
        "source_retry_execution_artifact_kind": SOURCE_RETRY_EXECUTION_ARTIFACT_KIND,
        "source_retry_execution_status": SOURCE_RETRY_EXECUTION_STATUS,
        "source_retry_execution_scope": SOURCE_RETRY_EXECUTION_SCOPE,
        "source_retry_approval_digest": SOURCE_RETRY_APPROVAL_DIGEST,
        "source_retry_operator_review_digest": SOURCE_RETRY_OPERATOR_REVIEW_DIGEST,
        "source_retry_candidate_digest": SOURCE_RETRY_CANDIDATE_DIGEST,
        "source_remediation_results_review_digest": SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
        "source_remediation_execution_digest": SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "source_staged_inventory_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_merge_strategy_approval_digest": SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST,
        "retry_execution_branch": RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_pytest_command": RETRY_PYTEST_COMMAND,
        "retry_pytest_working_directory": RETRY_PYTEST_WORKING_DIRECTORY,
        "retry_pytest_ran_from_detached_worktree": True,
        "retry_pytest_used_root_virtualenv_python": True,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_performed": True,
        "retry_pytest_exit_code": 1,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "retry_pytest_passed_count": RETRY_FAILED_RUN["passed"],
        "retry_pytest_failed_count": RETRY_FAILED_RUN["failed"],
        "retry_pytest_error_count": RETRY_FAILED_RUN["errors"],
        "retry_pytest_skipped_count": RETRY_FAILED_RUN["skipped"],
        "retry_pytest_duration_seconds": "1547.848456",
        "retry_pytest_reported_duration_seconds": "1538.84",
    }


def _failure_snapshot() -> dict[str, Any]:
    return {
        "first_retry_failure_authoritative": True,
        "later_retry_rerun_performed": False,
        "later_retry_rerun_overrides_first_retry_failure": False,
        "retry_execution_successful": False,
        "ready_for_retry_results_review": False,
        "retry_results_review_created": False,
        "integration_results_review_created": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "origin_main_commit_before_retry": ORIGIN_MAIN_COMMIT,
        "origin_main_commit_after_retry": ORIGIN_MAIN_COMMIT,
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit_before_retry": INTEGRATION_BRANCH_HEAD_COMMIT,
        "integration_branch_head_commit_after_retry": INTEGRATION_BRANCH_HEAD_COMMIT,
        "remote_integration_branch_exists_before_retry": False,
        "remote_integration_branch_exists_after_retry": False,
        "detached_integration_worktree_path": RETRY_PYTEST_WORKING_DIRECTORY,
        "detached_integration_worktree_head_commit_before_retry": INTEGRATION_BRANCH_HEAD_COMMIT,
        "detached_integration_worktree_head_commit_after_retry": INTEGRATION_BRANCH_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean_before_retry": True,
        "detached_integration_worktree_clean_after_retry": True,
        "staged_evidence_manifest_digest_before_retry": SOURCE_STAGED_INVENTORY_DIGEST,
        "staged_evidence_manifest_digest_after_retry": SOURCE_STAGED_INVENTORY_DIGEST,
        "staged_evidence_unchanged_by_retry": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "marketflow_outputs_committed": False,
        "evidence_regenerated": False,
        "root_full_regression_passed_count": 29066,
        "root_full_regression_skipped_count": 7,
        "root_full_regression_is_retry_evidence": False,
        "root_full_regression_does_not_override_detached_retry_failure": True,
    }


def _base_diagnosis(source: Mapping[str, Any], snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1,
        "diagnosis_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY,
        "diagnosis_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        **deepcopy(dict(source)), **deepcopy(dict(snapshot)),
        "diagnosis_created": True, "diagnosis_ready": True,
        "diagnosis_does_not_rerun_retry": True,
        "diagnosis_does_not_create_retry_results_review": True,
        "diagnosis_does_not_mark_integration_successful": True,
        "integration_branch_pushed": False, "remote_integration_branch_created": False,
        "main_merge_performed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "provider_requests_made_in_diagnosis": False,
        "market_data_acquisition_performed_in_diagnosis": False,
        "dataset_generation_performed_in_diagnosis": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "diagnosis_domains": deepcopy(DIAGNOSIS_DOMAINS),
        "diagnostic_comparison": {
            "original_failed_run": deepcopy(ORIGINAL_FAILED_RUN),
            "retry_failed_run": deepcopy(RETRY_FAILED_RUN),
            "delta": deepcopy(RUN_DELTA),
            "interpretation": COMPARISON_INTERPRETATION,
        },
        "root_cause_questions": list(ROOT_CAUSE_QUESTIONS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "retry_results_review_blocked": True, "main_merge_approval_blocked": True,
        "integration_retry_allowed_now": False,
        "integration_retry_requires_new_candidate_review_approval_execution_chain": True,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    retry_counts = {
        "passed": diagnosis.get("retry_pytest_passed_count"),
        "failed": diagnosis.get("retry_pytest_failed_count"),
        "errors": diagnosis.get("retry_pytest_error_count"),
        "skipped": diagnosis.get("retry_pytest_skipped_count"),
    }
    values: dict[str, tuple[Any, Any]] = {
        "source_retry_approval_digest_bound": (SOURCE_RETRY_APPROVAL_DIGEST, diagnosis.get("source_retry_approval_digest")),
        "source_retry_operator_review_digest_bound": (SOURCE_RETRY_OPERATOR_REVIEW_DIGEST, diagnosis.get("source_retry_operator_review_digest")),
        "source_retry_candidate_digest_bound": (SOURCE_RETRY_CANDIDATE_DIGEST, diagnosis.get("source_retry_candidate_digest")),
        "source_remediation_results_review_digest_bound": (SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST, diagnosis.get("source_remediation_results_review_digest")),
        "source_remediation_execution_digest_bound": (SOURCE_REMEDIATION_EXECUTION_DIGEST, diagnosis.get("source_remediation_execution_digest")),
        "source_staged_inventory_digest_bound": (SOURCE_STAGED_INVENTORY_DIGEST, diagnosis.get("source_staged_inventory_digest")),
        "retry_execution_branch_bound": (RETRY_EXECUTION_BRANCH, diagnosis.get("retry_execution_branch")),
        "retry_execution_commit_bound": (RETRY_EXECUTION_COMMIT, diagnosis.get("retry_execution_commit")),
        "retry_pytest_command_bound": (RETRY_PYTEST_COMMAND, diagnosis.get("retry_pytest_command")),
        "retry_pytest_working_directory_bound": (RETRY_PYTEST_WORKING_DIRECTORY, diagnosis.get("retry_pytest_working_directory")),
        "retry_pytest_ran_from_detached_worktree_true": (True, diagnosis.get("retry_pytest_ran_from_detached_worktree")),
        "retry_pytest_first_result_authoritative_true": (True, diagnosis.get("retry_pytest_first_result_authoritative")),
        "retry_pytest_failed_recorded": ([True, False, 1], [diagnosis.get("retry_pytest_failed"), diagnosis.get("retry_pytest_passed"), diagnosis.get("retry_pytest_exit_code")]),
        "retry_pytest_counts_recorded": (RETRY_FAILED_RUN, retry_counts),
        "success_digest_not_generated": (False, diagnosis.get("successful_integration_execution_digest_generated")),
        "validation_digest_not_generated": (False, diagnosis.get("successful_integration_validation_digest_generated")),
        "retry_results_review_created_false": (False, diagnosis.get("retry_results_review_created")),
        "integration_results_review_created_false": (False, diagnosis.get("integration_results_review_created")),
        "integration_execution_successful_false": (False, diagnosis.get("retry_execution_successful")),
        "origin_main_unchanged": (diagnosis.get("origin_main_commit_before_retry"), diagnosis.get("origin_main_commit_after_retry")),
        "integration_branch_head_unchanged": (diagnosis.get("integration_branch_head_commit_before_retry"), diagnosis.get("integration_branch_head_commit_after_retry")),
        "detached_worktree_head_unchanged": (diagnosis.get("detached_integration_worktree_head_commit_before_retry"), diagnosis.get("detached_integration_worktree_head_commit_after_retry")),
        "staged_evidence_unchanged": ([SOURCE_STAGED_INVENTORY_DIGEST, True], [diagnosis.get("staged_evidence_manifest_digest_after_retry"), diagnosis.get("staged_evidence_unchanged_by_retry")]),
        "marketflow_outputs_not_tracked": ([False, False], [diagnosis.get("marketflow_outputs_tracked_in_repository"), diagnosis.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "root_regression_not_retry_evidence": (False, diagnosis.get("root_full_regression_is_retry_evidence")),
        "diagnosis_created_true": (True, diagnosis.get("diagnosis_created")), "diagnosis_ready_true": (True, diagnosis.get("diagnosis_ready")),
        "diagnosis_domains_defined": (DIAGNOSIS_DOMAINS, diagnosis.get("diagnosis_domains")),
        "diagnostic_comparison_defined": ({"original_failed_run": ORIGINAL_FAILED_RUN, "retry_failed_run": RETRY_FAILED_RUN, "delta": RUN_DELTA, "interpretation": COMPARISON_INTERPRETATION}, diagnosis.get("diagnostic_comparison")),
        "root_cause_questions_defined": (ROOT_CAUSE_QUESTIONS, diagnosis.get("root_cause_questions")),
        "recommended_next_task_defined": (RECOMMENDED_NEXT_TASK, diagnosis.get("recommended_next_task")),
        "retry_results_review_blocked_true": (True, diagnosis.get("retry_results_review_blocked")),
        "main_merge_approval_blocked_true": (True, diagnosis.get("main_merge_approval_blocked")),
        "integration_retry_allowed_now_false": (False, diagnosis.get("integration_retry_allowed_now")),
        "integration_branch_pushed_false": (False, diagnosis.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, diagnosis.get("remote_integration_branch_created")),
        "main_push_false": (False, diagnosis.get("main_push_performed")),
        "origin_main_modified_false": (False, diagnosis.get("origin_main_modified_by_this_task")),
        "provider_requests_false": (False, diagnosis.get("provider_requests_made_in_diagnosis")),
        "market_data_acquisition_false": (False, diagnosis.get("market_data_acquisition_performed_in_diagnosis")),
        "dataset_generation_false": (False, diagnosis.get("dataset_generation_performed_in_diagnosis")),
        "metric_recomputation_false": (False, diagnosis.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, diagnosis.get("model_training_performed")),
        "strategy_scoring_false": (False, diagnosis.get("strategy_scoring_performed")),
        "recommendations_false": (False, diagnosis.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, diagnosis.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, diagnosis.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, diagnosis.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, diagnosis.get("broker_execution")),
        "next_chain_defined": (NEXT_CHAIN, diagnosis.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, diagnosis.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, diagnosis.get("risk_controls")),
        "no_tracked_marketflow_files": (True, diagnosis.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "diagnosis_created": True, "diagnosis_ready": True,
        "retry_execution_successful": False, "retry_results_review_blocked": True,
        "main_merge_approval_blocked": True, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_diagnosis_digest_v1(
    diagnosis: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the diagnosis."""
    payload = deepcopy(dict(diagnosis))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_diagnosis_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
    *, source_execution: dict | None = None, failure_snapshot: dict | None = None,
) -> dict:
    """Build the diagnosis from committed retry constants without external I/O."""
    source = _source_execution()
    snapshot = _failure_snapshot()
    for supplied, target, label in (
        (source_execution, source, "source_execution"),
        (failure_snapshot, snapshot, "failure_snapshot"),
    ):
        if supplied is not None:
            if not isinstance(supplied, dict):
                raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError(f"{label} must be an object")
            target.update(deepcopy(supplied))
    diagnosis = _base_diagnosis(source, snapshot)
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis["checklist"])
    diagnosis["marketflow_repository_integration_branch_retry_failure_diagnosis_digest"] = (
        marketflow_repository_integration_branch_retry_failure_diagnosis_digest_v1(diagnosis)
    )
    validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(diagnosis)
    return diagnosis


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError(f"{field} mismatch")


def validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict:
    """Validate exact failure evidence and reject widened authority."""
    if not isinstance(diagnosis, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError("diagnosis must be an object")
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1,
        "diagnosis_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_READY,
        "diagnosis_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_source_execution(), **_failure_snapshot(),
        "diagnosis_domains": DIAGNOSIS_DOMAINS,
        "diagnostic_comparison": {"original_failed_run": ORIGINAL_FAILED_RUN, "retry_failed_run": RETRY_FAILED_RUN, "delta": RUN_DELTA, "interpretation": COMPARISON_INTERPRETATION},
        "root_cause_questions": ROOT_CAUSE_QUESTIONS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in static.items():
        _expect(diagnosis.get(field), expected, field)
    for field in ("retry_execution_commit", "origin_main_commit_before_retry", "origin_main_commit_after_retry", "integration_branch_head_commit_before_retry", "integration_branch_head_commit_after_retry"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(diagnosis.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError(f"{field} invalid")
    required_true = (
        "created_offline", "governance_only", "diagnosis_only", "diagnosis_created", "diagnosis_ready",
        "diagnosis_does_not_rerun_retry", "diagnosis_does_not_create_retry_results_review",
        "diagnosis_does_not_mark_integration_successful",
        "integration_retry_requires_new_candidate_review_approval_execution_chain", "no_tracked_marketflow_files",
    )
    required_false = (
        "retry_execution_successful", "ready_for_retry_results_review", "retry_results_review_created",
        "integration_results_review_created", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "root_full_regression_is_retry_evidence",
        "integration_branch_pushed", "remote_integration_branch_created", "main_merge_performed",
        "main_push_performed", "origin_main_modified_by_this_task", "provider_requests_made_in_diagnosis",
        "market_data_acquisition_performed_in_diagnosis", "dataset_generation_performed_in_diagnosis",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated", "predictive_usefulness_accepted",
        "profitability_accepted", "integration_retry_allowed_now",
    )
    for field in required_true:
        _expect(diagnosis.get(field), True, field)
    for field in required_false:
        _expect(diagnosis.get(field), False, field)
    _expect(diagnosis.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(diagnosis.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(diagnosis.get(field), NOT_AUTHORIZED, field)
    checklist = diagnosis.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError("checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(diagnosis), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError("checklist failed")
    _expect(diagnosis.get("summary"), _summary(checklist), "summary")
    digest = diagnosis.get("marketflow_repository_integration_branch_retry_failure_diagnosis_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError("diagnosis digest missing")
    _expect(digest, marketflow_repository_integration_branch_retry_failure_diagnosis_digest_v1(diagnosis), "diagnosis digest")
    return {
        "status": diagnosis["diagnosis_status"], "artifact_kind": diagnosis["artifact_kind"],
        "diagnosis_scope": diagnosis["diagnosis_scope"],
        "marketflow_repository_integration_branch_retry_failure_diagnosis_digest": digest,
        **{key: diagnosis["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    """Render the validated diagnosis as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(diagnosis)
    comparison = diagnosis["diagnostic_comparison"]
    sections = [
        ("Source Retry Execution", [f"Artifact/status: `{diagnosis['source_retry_execution_artifact_kind']}` / `{diagnosis['source_retry_execution_status']}`.", f"Branch/commit: `{diagnosis['retry_execution_branch']}` / `{diagnosis['retry_execution_commit']}`."]),
        ("Failure Summary", [f"Authoritative result: `{RETRY_FAILED_RUN['passed']} passed, {RETRY_FAILED_RUN['failed']} failed, {RETRY_FAILED_RUN['errors']} errors, {RETRY_FAILED_RUN['skipped']} skipped`.", "The first retry remains authoritative and blocked."]),
        ("Retry Environment", [f"Command: `{diagnosis['retry_pytest_command']}`.", f"Working directory: `{diagnosis['retry_pytest_working_directory']}`.", "The integration worktree remained detached and clean."]),
        ("Original Failure Comparison", [f"Original: `{ORIGINAL_FAILED_RUN}`.", f"Retry: `{RETRY_FAILED_RUN}`.", f"Delta: `{comparison['delta']}`.", comparison["interpretation"]]),
        ("Root Regression Boundary", [f"Root regression: `{diagnosis['root_full_regression_passed_count']} passed, {diagnosis['root_full_regression_skipped_count']} skipped`.", "The root-worktree regression is not retry evidence and does not override the detached retry failure."]),
        ("Diagnosis Domains", [f"`{row['domain']}`: `{row['finding']}`" for row in diagnosis["diagnosis_domains"]]),
        ("Root-Cause Questions", diagnosis["root_cause_questions"]),
        ("Recommendation", [f"Next task: `{diagnosis['recommended_next_task']}`.", f"Action: `{diagnosis['recommended_action']}`."]),
        ("Next Chain", diagnosis["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in diagnosis["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in diagnosis["risk_controls"]]),
        ("Authority Boundaries", ["No retry, results review, main merge, predictive/profitability acceptance, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No provider, evidence regeneration, branch push, branch deletion, or tag mutation is performed.", "A new candidate/review/approval/execution chain is required before another retry."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Diagnosis v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
    failure_snapshot: dict | None = None,
) -> dict:
    """Write canonical diagnosis JSON without overwriting an existing artifact."""
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(
        source_execution=source_execution, failure_snapshot=failure_snapshot
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_diagnosis_v1(diagnosis)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_diagnosis_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDiagnosisError("failure diagnosis output already exists")
    payload = canonical_json_bytes(diagnosis)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": diagnosis["artifact_kind"],
        "diagnosis_status": diagnosis["diagnosis_status"], "diagnosis_scope": diagnosis["diagnosis_scope"],
        "marketflow_repository_integration_branch_retry_failure_diagnosis_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_diagnosis_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
