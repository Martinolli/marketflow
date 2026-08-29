"""Offline diagnosis of the failed repository integration-branch pytest gate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1 = (
    "marketflow_repository_integration_branch_execution_failure_diagnosis_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY"
)
REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW = (
    "REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW"
)

SOURCE_APPROVAL_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED"
SOURCE_APPROVAL_DIGEST = "34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c"
ATTEMPTED_EXECUTION_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED"
ATTEMPTED_EXECUTION_BLOCKED_STATUS = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED"
)
ATTEMPTED_EXECUTION_BRANCH = "feature/marketflow-repository-integration-branch-execution-v1"
ATTEMPTED_EXECUTION_COMMIT = "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba"
INTEGRATION_BRANCH_NAME = "integration/marketflow-terminal-evidence-stack-validation-v1"
INTEGRATION_HEAD_COMMIT = "220fbc220365fce9cae13ab4853cddff118c0187"
INTEGRATION_BASE_COMMIT = "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
INTEGRATION_SOURCE_COMMIT = "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"
INTEGRATION_MERGE_METHOD = "NO_FF_MERGE_COMMIT"

FIRST_PYTEST_COUNTS = {"passed": 24481, "failed": 1300, "errors": 500, "skipped": 7}
LATER_RERUN_COUNTS = {"passed": 26842, "skipped": 7}
REPRESENTATIVE_FAILURE_DOMAIN = "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH"
REPRESENTATIVE_ACTUAL_DIGEST = "783e0013424de9a4e9f02b2ec896c8aa152c0ca701c448ae3e3cfffec05a9b93"
REPRESENTATIVE_REQUIRED_DIGEST = "57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415"

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1"
)
RECOMMENDED_NEXT_TASK_STATUS = "FUTURE_CANDIDATE_NOT_CREATED"
RECOMMENDED_ACTION = "CREATE_REMEDIATION_CANDIDATE_FOR_DIGEST_MISMATCH_AND_STATE_ORDER_DEPENDENCE"

DIAGNOSIS_DOMAINS = [
    {"domain": "FAILURE_GATE_STATUS", "finding": "FIRST_INTEGRATION_PYTEST_FAILED_AUTHORITATIVE_GATE"},
    {"domain": "LATER_RERUN_STATUS", "finding": "LATER_PASSING_RERUN_IS_DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE"},
    {"domain": "DIGEST_MISMATCH_DOMAIN", "finding": "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH_REQUIRES_ROOT_CAUSE"},
    {"domain": "STATE_ORDER_DEPENDENCE", "finding": "TEST_ORDER_OR_STATE_DEPENDENCE_SUSPECTED"},
    {"domain": "SOURCE_CONSTANT_CONSISTENCY", "finding": "REQUIRED_AND_ACTUAL_DIGEST_CONSTANTS_REQUIRE_TRACE"},
    {"domain": "PYTEST_ISOLATION", "finding": "ISOLATED_PASS_SUGGESTS_GLOBAL_STATE_OR_CACHE_EFFECT"},
    {"domain": "INTEGRATION_BRANCH_STATUS", "finding": "INTEGRATION_BRANCH_EXISTS_LOCAL_ONLY_NOT_PUSHED"},
    {"domain": "MAIN_PROTECTION", "finding": "ORIGIN_MAIN_UNCHANGED"},
    {"domain": "AUTHORITY_BOUNDARY", "finding": "NO_RESULTS_REVIEW_OR_MAIN_MERGE_ALLOWED"},
    {"domain": "REMEDIATION_DIRECTION", "finding": "PREPARE_SEPARATE_REMEDIATION_CANDIDATE_BEFORE_ANY_RETRY"},
    {"domain": "EVIDENCE_ROOT_DEPENDENCY", "finding": "MISSING_IGNORED_ACQUISITION_EVIDENCE_ROOT_PRODUCES_BLOCKED_DIGEST_783E0013"},
    {"domain": "RERUN_CWD_TRACE", "finding": "LATER_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_WORKTREE"},
]

ROOT_CAUSE_QUESTIONS = [
    "Which test module first observed the acquisition evidence review digest mismatch?",
    "Which service or constant defines required digest 57c0a06e...?",
    "Which service or runtime path produced actual digest 783e0013...?",
    "Is the actual digest derived from mutable ordering, timestamp, path, environment, cache, or imported module state?",
    "Does the failure depend on test order?",
    "Does the failure depend on prior tests mutating module-level constants, caches, environment variables, temp dirs, or global registries?",
    "Does the failure depend on current branch, local tag state, or integration branch content?",
    "Are source constants inconsistent between historical evidence artifacts and new integration stack?",
    "Did the integration branch expose previously hidden stale constants?",
    "What deterministic repair is needed before integration retry?",
]

CONFIRMED_ROOT_CAUSE_FINDINGS = [
    {
        "finding_id": "FIRST_OBSERVER_TRACE",
        "status": "CONFIRMED",
        "finding": "tests/test_acquisition_generation_freeze_service.py setup reached the acquisition-generation approval source-review check and exposed the representative mismatch",
    },
    {
        "finding_id": "REQUIRED_DIGEST_TRACE",
        "status": "CONFIRMED",
        "finding": "acquisition_generation_approval_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST defines the frozen required digest 57c0a06e...",
    },
    {
        "finding_id": "ACTUAL_DIGEST_TRACE",
        "status": "CONFIRMED",
        "finding": "acquisition_evidence_results_review_service deterministically produces blocked digest 783e0013... when acquisition_provider_evidence_run_manifest.json is absent",
    },
    {
        "finding_id": "ISOLATED_WORKTREE_EVIDENCE_ROOT",
        "status": "CONFIRMED",
        "finding": "the temporary integration worktree does not contain ignored .marketflow acquisition evidence outputs required by default-path historical evidence tests",
    },
    {
        "finding_id": "LATER_RERUN_CWD",
        "status": "CONFIRMED",
        "finding": "the later passing diagnostic command created a detached worktree but invoked pytest from the feature worktree, so it was not an integration-branch acceptance rerun",
    },
    {
        "finding_id": "REMEDIATION_BOUNDARY",
        "status": "RECOMMENDATION_ONLY",
        "finding": "a separate remediation candidate must define deterministic ignored-evidence availability or fixture isolation before any approved retry",
    },
]

NEXT_CHAIN = [
    "Repository Integration Branch Validation Failure Remediation Candidate v1.",
    "Remediation Candidate Operator Review v1.",
    "Remediation Approval v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Results Review v1.",
    "Integration Branch Retry Candidate v1, only after remediation review.",
    "Integration Branch Retry Approval v1, if selected.",
    "Integration Branch Retry Execution v1, if approved.",
    "Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if retry results review passes.",
]

NEXT_GATES = [
    "integration_failure_remediation_candidate",
    "integration_failure_remediation_operator_review",
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
    "diagnosis_does_not_mark_execution_successful",
    "diagnosis_does_not_create_results_review",
    "diagnosis_does_not_retry_integration",
    "diagnosis_does_not_generate_successful_execution_digest",
    "diagnosis_does_not_generate_successful_validation_digest",
    "diagnosis_does_not_delete_integration_branch",
    "diagnosis_does_not_reset_integration_branch",
    "diagnosis_does_not_push_integration_branch",
    "diagnosis_does_not_push_main",
    "diagnosis_does_not_merge_to_main",
    "diagnosis_does_not_rebase",
    "diagnosis_does_not_squash_merge",
    "diagnosis_does_not_cherry_pick",
    "diagnosis_does_not_delete_branches",
    "diagnosis_does_not_delete_remote_branches",
    "diagnosis_does_not_force_push",
    "diagnosis_does_not_prune_remotes",
    "diagnosis_does_not_modify_origin_main",
    "diagnosis_does_not_modify_tags",
    "diagnosis_does_not_push_additional_tags",
    "diagnosis_does_not_modify_marketflow_outputs",
    "diagnosis_does_not_call_providers",
    "diagnosis_does_not_acquire_market_data",
    "diagnosis_does_not_regenerate_dataset",
    "diagnosis_does_not_recompute_metrics",
    "diagnosis_does_not_train_models",
    "diagnosis_does_not_score_strategy",
    "diagnosis_does_not_generate_recommendations",
    "diagnosis_does_not_accept_predictive_usefulness",
    "diagnosis_does_not_accept_profitability",
    "diagnosis_does_not_authorize_runtime",
    "diagnosis_does_not_authorize_broker_execution",
    "first_failed_pytest_is_authoritative",
    "later_passing_rerun_is_diagnostic_only",
    "separate_remediation_required_before_retry",
    "separate_retry_approval_required_before_execution",
    "protect_origin_main",
    "preserve_integration_branch_for_diagnosis",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_approval_digest_bound", "attempted_execution_branch_bound",
    "attempted_execution_commit_bound", "integration_branch_name_bound",
    "integration_head_commit_bound", "integration_base_commit_bound",
    "integration_source_commit_bound", "origin_main_before_bound",
    "origin_main_after_unchanged", "first_pytest_failed_authoritative",
    "first_pytest_counts_recorded", "later_rerun_passed_recorded",
    "later_rerun_not_acceptance_evidence", "representative_digest_mismatch_recorded",
    "diagnosis_domains_present", "root_cause_questions_present",
    "integration_execution_successful_false", "successful_execution_digest_generated_false",
    "successful_validation_digest_generated_false", "integration_results_review_ready_false",
    "integration_results_review_created_false", "integration_branch_created_true",
    "integration_merge_performed_true", "integration_pytest_performed_true",
    "integration_pytest_passed_false", "integration_validation_completed_false",
    "integration_branch_pushed_false", "remote_integration_branch_created_false",
    "main_merge_performed_false", "main_push_false", "rebase_performed_false",
    "squash_merge_performed_false", "cherry_pick_performed_false", "branch_delete_false",
    "remote_delete_false", "force_push_false", "remote_prune_false",
    "origin_main_modified_false", "tags_pushed_again_false", "additional_tags_created_false",
    "tags_modified_false", "tags_deleted_false", "cleanup_candidate_created_false",
    "marketflow_outputs_not_tracked", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false",
    "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "recommended_next_task_remediation_candidate", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(ValueError):
    """Raised when failure-diagnosis evidence or authority boundaries are invalid."""


def _base_failure_snapshot() -> dict[str, Any]:
    return {
        "attempted_execution_artifact_kind": ATTEMPTED_EXECUTION_ARTIFACT_KIND,
        "attempted_execution_blocked_status": ATTEMPTED_EXECUTION_BLOCKED_STATUS,
        "attempted_execution_branch": ATTEMPTED_EXECUTION_BRANCH,
        "attempted_execution_commit": ATTEMPTED_EXECUTION_COMMIT,
        "integration_branch_name": INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": INTEGRATION_HEAD_COMMIT,
        "integration_merge_method": INTEGRATION_MERGE_METHOD,
        "integration_base_commit": INTEGRATION_BASE_COMMIT,
        "integration_source_commit": INTEGRATION_SOURCE_COMMIT,
        "origin_main_commit_before_execution": INTEGRATION_BASE_COMMIT,
        "origin_main_commit_after_execution": INTEGRATION_BASE_COMMIT,
        "first_integration_pytest_passed_count": FIRST_PYTEST_COUNTS["passed"],
        "first_integration_pytest_failed_count": FIRST_PYTEST_COUNTS["failed"],
        "first_integration_pytest_error_count": FIRST_PYTEST_COUNTS["errors"],
        "first_integration_pytest_skipped_count": FIRST_PYTEST_COUNTS["skipped"],
        "later_isolated_rerun_passed_count": LATER_RERUN_COUNTS["passed"],
        "later_isolated_rerun_skipped_count": LATER_RERUN_COUNTS["skipped"],
    }


def _base_diagnosis(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1,
        "diagnosis_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY,
        "diagnosis_scope": REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW,
        "created_offline": True, "governance_only": True, "failure_diagnosis_only": True,
        "source_merge_strategy_approval_artifact_kind": SOURCE_APPROVAL_ARTIFACT_KIND,
        "source_merge_strategy_approval_digest": SOURCE_APPROVAL_DIGEST,
        **deepcopy(dict(snapshot)),
        "origin_main_modified_by_this_task": False,
        "first_integration_pytest_authoritative": True,
        "first_integration_pytest_passed": False,
        "later_isolated_rerun_passed": True,
        "later_isolated_rerun_overrides_first_failure": False,
        "later_isolated_rerun_label_validated": False,
        "later_rerun_actual_scope": "FEATURE_BRANCH_DIAGNOSTIC_RERUN_NOT_INTEGRATION_ACCEPTANCE",
        "representative_failure_domain": REPRESENTATIVE_FAILURE_DOMAIN,
        "representative_actual_digest_prefix": REPRESENTATIVE_ACTUAL_DIGEST[:8],
        "representative_required_digest_prefix": REPRESENTATIVE_REQUIRED_DIGEST[:8],
        "representative_actual_digest": REPRESENTATIVE_ACTUAL_DIGEST,
        "representative_required_digest": REPRESENTATIVE_REQUIRED_DIGEST,
        "representative_missing_input": "acquisition_provider_evidence_run_manifest.json",
        "integration_execution_successful": False,
        "successful_execution_digest_generated": False,
        "successful_validation_digest_generated": False,
        "integration_results_review_ready": False,
        "integration_results_review_created": False,
        "repository_integration_branch_created": True, "integration_branch_created": True,
        "integration_merge_performed": True, "integration_pytest_performed": True,
        "integration_pytest_passed": False, "integration_validation_completed": False,
        "integration_branch_pushed": False, "remote_integration_branch_created": False,
        "main_merge_performed": False, "main_push_performed": False,
        "git_main_push_performed": False, "git_rebase_performed": False,
        "git_squash_merge_performed": False, "git_cherry_pick_performed": False,
        "git_branch_delete_performed": False, "git_remote_delete_performed": False,
        "git_force_push_performed": False, "git_remote_prune_performed": False,
        "repository_cleanup_candidate_created": False, "repository_cleanup_executed": False,
        "repository_tags_pushed_again": False, "additional_tag_push_performed": False,
        "additional_tags_created": False, "tags_modified": False, "tags_deleted": False,
        "tracked_marketflow_file_count": 0, "no_tracked_marketflow_files": True,
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
        "root_cause_questions": list(ROOT_CAUSE_QUESTIONS),
        "confirmed_root_cause_findings": deepcopy(CONFIRMED_ROOT_CAUSE_FINDINGS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "integration_results_review_blocked": True,
        "integration_retry_allowed_now": False,
        "integration_retry_requires_remediation_approval": True,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_DIGEST, diagnosis.get("source_merge_strategy_approval_digest")),
        "attempted_execution_branch_bound": (ATTEMPTED_EXECUTION_BRANCH, diagnosis.get("attempted_execution_branch")),
        "attempted_execution_commit_bound": (ATTEMPTED_EXECUTION_COMMIT, diagnosis.get("attempted_execution_commit")),
        "integration_branch_name_bound": (INTEGRATION_BRANCH_NAME, diagnosis.get("integration_branch_name")),
        "integration_head_commit_bound": (INTEGRATION_HEAD_COMMIT, diagnosis.get("integration_branch_head_commit")),
        "integration_base_commit_bound": (INTEGRATION_BASE_COMMIT, diagnosis.get("integration_base_commit")),
        "integration_source_commit_bound": (INTEGRATION_SOURCE_COMMIT, diagnosis.get("integration_source_commit")),
        "origin_main_before_bound": (INTEGRATION_BASE_COMMIT, diagnosis.get("origin_main_commit_before_execution")),
        "origin_main_after_unchanged": (diagnosis.get("origin_main_commit_before_execution"), diagnosis.get("origin_main_commit_after_execution")),
        "first_pytest_failed_authoritative": ([True, False], [diagnosis.get("first_integration_pytest_authoritative"), diagnosis.get("first_integration_pytest_passed")]),
        "first_pytest_counts_recorded": (
            FIRST_PYTEST_COUNTS,
            {
                "passed": diagnosis.get("first_integration_pytest_passed_count"),
                "failed": diagnosis.get("first_integration_pytest_failed_count"),
                "errors": diagnosis.get("first_integration_pytest_error_count"),
                "skipped": diagnosis.get("first_integration_pytest_skipped_count"),
            },
        ),
        "later_rerun_passed_recorded": ([True, *LATER_RERUN_COUNTS.values()], [diagnosis.get("later_isolated_rerun_passed"), diagnosis.get("later_isolated_rerun_passed_count"), diagnosis.get("later_isolated_rerun_skipped_count")]),
        "later_rerun_not_acceptance_evidence": (False, diagnosis.get("later_isolated_rerun_overrides_first_failure")),
        "representative_digest_mismatch_recorded": ([REPRESENTATIVE_ACTUAL_DIGEST[:8], REPRESENTATIVE_REQUIRED_DIGEST[:8]], [diagnosis.get("representative_actual_digest_prefix"), diagnosis.get("representative_required_digest_prefix")]),
        "diagnosis_domains_present": (DIAGNOSIS_DOMAINS, diagnosis.get("diagnosis_domains")),
        "root_cause_questions_present": (ROOT_CAUSE_QUESTIONS, diagnosis.get("root_cause_questions")),
        "integration_execution_successful_false": (False, diagnosis.get("integration_execution_successful")),
        "successful_execution_digest_generated_false": (False, diagnosis.get("successful_execution_digest_generated")),
        "successful_validation_digest_generated_false": (False, diagnosis.get("successful_validation_digest_generated")),
        "integration_results_review_ready_false": (False, diagnosis.get("integration_results_review_ready")),
        "integration_results_review_created_false": (False, diagnosis.get("integration_results_review_created")),
        "integration_branch_created_true": (True, diagnosis.get("integration_branch_created")),
        "integration_merge_performed_true": (True, diagnosis.get("integration_merge_performed")),
        "integration_pytest_performed_true": (True, diagnosis.get("integration_pytest_performed")),
        "integration_pytest_passed_false": (False, diagnosis.get("integration_pytest_passed")),
        "integration_validation_completed_false": (False, diagnosis.get("integration_validation_completed")),
        "integration_branch_pushed_false": (False, diagnosis.get("integration_branch_pushed")),
        "remote_integration_branch_created_false": (False, diagnosis.get("remote_integration_branch_created")),
        "main_merge_performed_false": (False, diagnosis.get("main_merge_performed")),
        "main_push_false": (False, diagnosis.get("main_push_performed")),
        "rebase_performed_false": (False, diagnosis.get("git_rebase_performed")),
        "squash_merge_performed_false": (False, diagnosis.get("git_squash_merge_performed")),
        "cherry_pick_performed_false": (False, diagnosis.get("git_cherry_pick_performed")),
        "branch_delete_false": (False, diagnosis.get("git_branch_delete_performed")),
        "remote_delete_false": (False, diagnosis.get("git_remote_delete_performed")),
        "force_push_false": (False, diagnosis.get("git_force_push_performed")),
        "remote_prune_false": (False, diagnosis.get("git_remote_prune_performed")),
        "origin_main_modified_false": (False, diagnosis.get("origin_main_modified_by_this_task")),
        "tags_pushed_again_false": (False, diagnosis.get("repository_tags_pushed_again")),
        "additional_tags_created_false": (False, diagnosis.get("additional_tags_created")),
        "tags_modified_false": (False, diagnosis.get("tags_modified")),
        "tags_deleted_false": (False, diagnosis.get("tags_deleted")),
        "cleanup_candidate_created_false": (False, diagnosis.get("repository_cleanup_candidate_created")),
        "marketflow_outputs_not_tracked": (0, diagnosis.get("tracked_marketflow_file_count")),
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
        "recommended_next_task_remediation_candidate": (RECOMMENDED_NEXT_TASK, diagnosis.get("recommended_next_task")),
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
        "blocker_count": sum(1 for row in failed if row.get("severity") == BLOCKER),
        "integration_execution_successful": False,
        "integration_results_review_ready": False,
        "integration_results_review_created": False,
        "integration_failure_diagnosis_created": True,
        "first_integration_pytest_failed_authoritative": True,
        "later_rerun_overrides_first_failure": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_execution_failure_diagnosis_digest_v1(
    diagnosis: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic diagnosis digest."""
    payload = deepcopy(dict(diagnosis))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_execution_failure_diagnosis_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
    *, failure_snapshot: dict | None = None,
) -> dict:
    """Build the diagnosis offline from committed failure evidence only."""
    snapshot = _base_failure_snapshot()
    if failure_snapshot is not None:
        if not isinstance(failure_snapshot, dict):
            raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(
                "failure_snapshot must be an object"
            )
        snapshot.update(deepcopy(failure_snapshot))
    diagnosis = _base_diagnosis(snapshot)
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis["checklist"])
    diagnosis["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"] = (
        marketflow_repository_integration_branch_execution_failure_diagnosis_digest_v1(diagnosis)
    )
    validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(diagnosis)
    return diagnosis


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(f"{field} mismatch")


def validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict:
    """Validate exact failure evidence and reject any widened authority."""
    if not isinstance(diagnosis, dict):
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(
            "diagnosis must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1,
        "diagnosis_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY,
        "diagnosis_scope": REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW,
        "source_merge_strategy_approval_artifact_kind": SOURCE_APPROVAL_ARTIFACT_KIND,
        "source_merge_strategy_approval_digest": SOURCE_APPROVAL_DIGEST,
        "attempted_execution_artifact_kind": ATTEMPTED_EXECUTION_ARTIFACT_KIND,
        "attempted_execution_blocked_status": ATTEMPTED_EXECUTION_BLOCKED_STATUS,
        **_base_failure_snapshot(),
        "representative_failure_domain": REPRESENTATIVE_FAILURE_DOMAIN,
        "representative_actual_digest_prefix": REPRESENTATIVE_ACTUAL_DIGEST[:8],
        "representative_required_digest_prefix": REPRESENTATIVE_REQUIRED_DIGEST[:8],
        "representative_actual_digest": REPRESENTATIVE_ACTUAL_DIGEST,
        "representative_required_digest": REPRESENTATIVE_REQUIRED_DIGEST,
        "diagnosis_domains": DIAGNOSIS_DOMAINS,
        "root_cause_questions": ROOT_CAUSE_QUESTIONS,
        "confirmed_root_cause_findings": CONFIRMED_ROOT_CAUSE_FINDINGS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": RECOMMENDED_NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, expected in static.items():
        _expect(diagnosis.get(field), expected, field)
    for field in ("attempted_execution_commit", "integration_branch_head_commit", "integration_base_commit", "integration_source_commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(diagnosis.get(field, ""))):
            raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(f"{field} invalid")
    required_true = (
        "created_offline", "governance_only", "failure_diagnosis_only",
        "first_integration_pytest_authoritative", "later_isolated_rerun_passed",
        "repository_integration_branch_created", "integration_branch_created",
        "integration_merge_performed", "integration_pytest_performed",
        "integration_results_review_blocked", "integration_retry_requires_remediation_approval",
        "no_tracked_marketflow_files",
    )
    required_false = (
        "origin_main_modified_by_this_task", "first_integration_pytest_passed",
        "later_isolated_rerun_overrides_first_failure", "later_isolated_rerun_label_validated",
        "integration_execution_successful", "successful_execution_digest_generated",
        "successful_validation_digest_generated", "integration_results_review_ready",
        "integration_results_review_created", "integration_pytest_passed",
        "integration_validation_completed", "integration_branch_pushed",
        "remote_integration_branch_created", "main_merge_performed", "main_push_performed",
        "git_main_push_performed", "git_rebase_performed", "git_squash_merge_performed",
        "git_cherry_pick_performed", "git_branch_delete_performed",
        "git_remote_delete_performed", "git_force_push_performed", "git_remote_prune_performed",
        "repository_cleanup_candidate_created", "repository_cleanup_executed",
        "repository_tags_pushed_again", "additional_tag_push_performed",
        "additional_tags_created", "tags_modified", "tags_deleted",
        "provider_requests_made_in_diagnosis", "market_data_acquisition_performed_in_diagnosis",
        "dataset_generation_performed_in_diagnosis", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted", "integration_retry_allowed_now",
    )
    for field in required_true:
        _expect(diagnosis.get(field), True, field)
    for field in required_false:
        _expect(diagnosis.get(field), False, field)
    _expect(diagnosis.get("tracked_marketflow_file_count"), 0, "tracked_marketflow_file_count")
    _expect(diagnosis.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(diagnosis.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(diagnosis.get(field), NOT_AUTHORIZED, field)
    checklist = diagnosis.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError("checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(diagnosis), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError("checklist failed")
    _expect(diagnosis.get("summary"), _summary(checklist), "summary")
    digest = diagnosis.get(
        "marketflow_repository_integration_branch_execution_failure_diagnosis_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError("diagnosis digest missing")
    _expect(
        digest,
        marketflow_repository_integration_branch_execution_failure_diagnosis_digest_v1(diagnosis),
        "diagnosis digest",
    )
    return {
        "status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY,
        "artifact_kind": diagnosis["artifact_kind"],
        "diagnosis_scope": diagnosis["diagnosis_scope"],
        "marketflow_repository_integration_branch_execution_failure_diagnosis_digest": digest,
        **{key: diagnosis["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_execution_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    """Render the validated diagnosis as a governance-only Markdown record."""
    validation = validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(diagnosis)
    sections = [
        ("Source Merge Strategy Approval", [f"Artifact/digest: `{diagnosis['source_merge_strategy_approval_artifact_kind']}` / `{diagnosis['source_merge_strategy_approval_digest']}`."]),
        ("Attempted Execution State", [f"Branch/commit: `{diagnosis['attempted_execution_branch']}` / `{diagnosis['attempted_execution_commit']}`.", f"Blocked status: `{diagnosis['attempted_execution_blocked_status']}`."]),
        ("Integration Branch State", [f"Branch/head: `{diagnosis['integration_branch_name']}` / `{diagnosis['integration_branch_head_commit']}`.", "Local only; not pushed."]),
        ("Authoritative Pytest Failure", [f"Passed/failed/errors/skipped: `{FIRST_PYTEST_COUNTS['passed']} / {FIRST_PYTEST_COUNTS['failed']} / {FIRST_PYTEST_COUNTS['errors']} / {FIRST_PYTEST_COUNTS['skipped']}`."]),
        ("Later Diagnostic Rerun", [f"Recorded pass/skips: `{LATER_RERUN_COUNTS['passed']} / {LATER_RERUN_COUNTS['skipped']}`.", "The command ran from the feature worktree and is not integration acceptance evidence."]),
        ("Representative Failure", [f"Blocked/required digests: `{REPRESENTATIVE_ACTUAL_DIGEST}` / `{REPRESENTATIVE_REQUIRED_DIGEST}`.", "The blocked digest is reproduced by a missing ignored acquisition evidence manifest."]),
        ("Diagnosis Domains", [f"`{row['domain']}`: `{row['finding']}`" for row in diagnosis["diagnosis_domains"]]),
        ("Root-Cause Questions", diagnosis["root_cause_questions"]),
        ("Recommendation", [f"Next task: `{diagnosis['recommended_next_task']}`.", f"Action: `{diagnosis['recommended_action']}`."]),
        ("Next Chain", diagnosis["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in diagnosis["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in diagnosis["risk_controls"]]),
        ("Authority Boundaries", ["No retry, results review, main merge, runtime authority, or trading authority is created."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The first failed pytest gate remains authoritative.", "A separate approved remediation and retry chain is required."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Execution Failure Diagnosis v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
    output_dir: str | Path,
    *, failure_snapshot: dict | None = None,
) -> dict:
    """Write canonical diagnosis JSON without overwriting an existing artifact."""
    diagnosis = build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
        failure_snapshot=failure_snapshot
    )
    validation = validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
        diagnosis
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_execution_failure_diagnosis_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError(
            "failure diagnosis output already exists"
        )
    payload = canonical_json_bytes(diagnosis)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": diagnosis["artifact_kind"],
        "diagnosis_status": diagnosis["diagnosis_status"],
        "diagnosis_scope": diagnosis["diagnosis_scope"],
        "marketflow_repository_integration_branch_execution_failure_diagnosis_digest": validation[
            "marketflow_repository_integration_branch_execution_failure_diagnosis_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
