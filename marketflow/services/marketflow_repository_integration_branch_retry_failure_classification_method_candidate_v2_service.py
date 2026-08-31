"""Propose cache-supported classification method v2 packages without execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_reentry_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SOURCE_REENTRY_DIGEST = "318c0d1b3f6977a79cd77e8de466286f4057f13d7c7f2bd218c5a561c17e91a6"
SOURCE_RESULTS_REVIEW_DIGEST = "a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9"
SOURCE_CACHE_MANIFEST_REVIEW_DIGEST = "cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee"
SOURCE_EXECUTION_DIGEST = "b7c987e76b02a026bc118ae05801e4ba02c92bdadb81df9562e28a646b4f80bb"
SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST = "9218bad7b0b176bd3b4398293304159f22c1772fad0fa91b6e1d275a770ebcca"
SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST = "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
SOURCE_STAGED_INVENTORY_DIGEST = "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
RECOMMENDED_PACKAGE = "PACKAGE_CACHE_SUPPORTED_MODULE_LEVEL_NODEID_CLASSIFICATION_V2"
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_V2_PHILOSOPHY = (
    "Use the reviewed detached pytest-cache classification source only within its proven limits: "
    "module-level grouping and node-ID inventory. Do not infer failure/error separation, first-order "
    "failure, traceback root cause, or retry success."
)
CANDIDATE_V2_BOUNDARY = (
    "Candidate-only; no classification execution, no cache read, no retry, no results review, no main "
    "merge, and no runtime authority are created by this artifact."
)
CANDIDATE_V2_GOAL = (
    "Design a classification method v2 that can convert reviewed cache-supported node IDs into bounded "
    "module-level failure-domain planning evidence, while preserving all unsupported-claim boundaries."
)
CLASSIFICATION_SOURCE_LIMITATIONS = [
    "cannot distinguish failures from errors",
    "cannot identify first failure",
    "cannot identify first error",
    "cannot provide traceback root cause",
    "cannot provide retry success evidence",
]

PROPOSED_V2_PACKAGES = [
    {
        "package_id": RECOMMENDED_PACKAGE,
        "status": RECOMMENDATION_STATUS,
        "purpose": "Classify the 1,404 reviewed failed-or-errored node IDs into module-level groups using the reviewed cache source and reviewed module summary constraints.",
        "recommended_for": "Safe first v2 method because it uses only supported cache claims: node IDs and modules.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CACHE_SUPPORTED_MODULE_GROUPING_WITH_EVIDENCE_ROOT_HINTS_V2",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Classify modules and assign tentative root-cause family hints for additional ignored evidence roots based on module naming only.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CACHE_SUPPORTED_PATH_CWD_AND_DIGEST_HINTS_V2",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Classify modules into path/cwd and digest-drift candidate families using module names and known failure-history context, without claiming traceback certainty.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CACHE_SUPPORTED_MODULE_GROUPING_PLUS_LIMITATION_REPORT_V2",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Produce module grouping and a strong limitation report, deferring all root-cause family hints to a later diagnostic-output capture.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CACHE_PLUS_DIAGNOSTIC_OUTPUT_ENRICHMENT_V2",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL",
        "purpose": "Use cache source as a module/node map and plan a separately approved diagnostic-output capture for traceback enrichment.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_FAILURE_ERROR_SEPARATION_FROM_CACHE_ONLY_V2",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Separate assertion failures from setup/import/runtime errors using only lastfailed.",
        "blocked_reason": "Reviewed cache source does not support reliable failure/error separation.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_FIRST_ORDER_TRACE_ANALYSIS_FROM_CACHE_ONLY_V2",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Identify first failure, first error, or traceback root cause using only cache source.",
        "blocked_reason": "Reviewed cache source does not preserve authoritative first-failure order or traceback detail.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_NEW_RETRY_WITHOUT_CLASSIFICATION_V2",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Proceed to new retry without classification or remediation.",
        "blocked_reason": "A prior retry failed; repeating retry without classification is unsafe and uninformative.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY_V2",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Proceed to main merge despite failed retry.",
        "blocked_reason": "Main merge approval remains blocked until a future retry results review passes.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
]
RECOMMENDATION_REASON = (
    "The reviewed cache source supports node-ID and module-level grouping. It does not support "
    "failure/error separation or first-order trace analysis, so the safest v2 method begins with "
    "module-level node-ID classification only."
)

FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS = {
    "source_reentry_must_be_ready": True,
    "source_classification_results_review_must_be_ready": True,
    "cache_source_must_remain_digest_bound": True,
    "v2_method_must_limit_scope_to_nodeids_and_modules": True,
    "v2_method_must_not_claim_failure_error_separation": True,
    "v2_method_must_not_claim_first_failure": True,
    "v2_method_must_not_claim_first_error": True,
    "v2_method_must_not_claim_traceback_root_cause": True,
    "v2_method_must_not_use_cache_as_retry_success_evidence": True,
    "v2_method_must_preserve_failed_retry_authority": True,
    "v2_method_must_produce_module_grouping_only": True,
    "v2_method_may_produce_root_cause_family_hints_with_low_confidence_only": True,
    "v2_method_must_record_all_limitations": True,
    "v2_method_execution_requires_separate_approval": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN = [
    "Verify source reentry digest and classification-source results-review digest.",
    "Verify cache manifest review digest.",
    "Use only reviewed cache-supported node IDs, module grouping, and reviewed module counts.",
    "Build module-level node-ID grouping.",
    "Generate bounded module summary.",
    "Assign optional low-confidence root-cause family hints only from module names.",
    "Avoid failure/error separation, first-failure order, and traceback root-cause claims.",
    "Produce a limitation report.",
    "Recommend whether evidence-root, path/cwd, digest-drift, or diagnostic-output candidate is needed.",
    "Keep new retry, retry results review, main merge, runtime, and trading closed.",
]
FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN_STATUS = "PLANNED_NOT_EXECUTED"
PLANNED_OUTPUT_NAMES = [
    "classification_v2_manifest",
    "module_nodeid_grouping_report",
    "module_summary_report",
    "largest_module_summary",
    "cache_source_limitation_report",
    "low_confidence_root_cause_hint_report",
    "unsupported_claims_exclusion_report",
    "recommended_next_method_or_remediation_report",
    "digest_manifest",
]
PLANNED_OUTPUTS = {name: "PLANNED_NOT_GENERATED" for name in PLANNED_OUTPUT_NAMES}
NON_GOALS = [
    "do_not_execute_classification_now",
    "do_not_read_cache_now",
    "do_not_run_retry_now",
    "do_not_run_full_pytest_now",
    "do_not_run_diagnostic_commands_now",
    "do_not_claim_failure_error_separation",
    "do_not_claim_first_failure",
    "do_not_claim_first_error",
    "do_not_claim_traceback_root_cause",
    "do_not_use_cache_as_retry_success_evidence",
    "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review",
    "do_not_create_integration_results_review",
    "do_not_mark_integration_successful",
    "do_not_push_integration_branch",
    "do_not_push_main",
    "do_not_commit_marketflow_outputs",
    "do_not_commit_pytest_cache",
    "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence",
    "do_not_call_providers",
    "do_not_accept_predictive_usefulness",
    "do_not_accept_profitability",
    "do_not_authorize_runtime",
    "do_not_authorize_trading",
]
NEXT_CHAIN = [
    "Classification Method Candidate v2 Operator Review.",
    "Classification Method Approval v2, if selected.",
    "Classification Method Execution v2, if approved.",
    "Classification Method Results Review v2.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "classification_method_candidate_v2_operator_review",
    "classification_method_approval_v2_if_selected",
    "classification_method_execution_v2_if_approved",
    "classification_method_results_review_v2",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "candidate_v2_does_not_execute_classification",
    "candidate_v2_does_not_read_cache",
    "candidate_v2_does_not_run_retry",
    "candidate_v2_does_not_run_full_pytest",
    "candidate_v2_does_not_run_diagnostic_commands",
    "candidate_v2_does_not_claim_failure_error_separation",
    "candidate_v2_does_not_claim_first_failure",
    "candidate_v2_does_not_claim_first_error",
    "candidate_v2_does_not_claim_traceback_root_cause",
    "candidate_v2_does_not_use_cache_as_retry_success_evidence",
    "candidate_v2_does_not_create_new_retry_candidate",
    "candidate_v2_does_not_create_retry_results_review",
    "candidate_v2_does_not_create_integration_results_review",
    "candidate_v2_does_not_mark_integration_successful",
    "candidate_v2_does_not_generate_successful_integration_digest",
    "candidate_v2_does_not_push_integration_branch",
    "candidate_v2_does_not_push_main",
    "candidate_v2_does_not_delete_integration_branch",
    "candidate_v2_does_not_delete_worktree",
    "candidate_v2_does_not_force_push",
    "candidate_v2_does_not_prune_remotes",
    "candidate_v2_does_not_modify_tags",
    "candidate_v2_does_not_commit_marketflow_outputs",
    "candidate_v2_does_not_commit_pytest_cache",
    "candidate_v2_does_not_modify_staged_evidence",
    "candidate_v2_does_not_regenerate_evidence",
    "candidate_v2_does_not_call_providers",
    "candidate_v2_does_not_acquire_market_data",
    "candidate_v2_does_not_regenerate_dataset",
    "candidate_v2_does_not_recompute_metrics",
    "candidate_v2_does_not_train_models",
    "candidate_v2_does_not_score_strategy",
    "candidate_v2_does_not_generate_recommendations",
    "candidate_v2_does_not_accept_predictive_usefulness",
    "candidate_v2_does_not_accept_profitability",
    "candidate_v2_does_not_authorize_runtime",
    "candidate_v2_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_operator_review_required",
    "separate_v2_approval_required_before_execution",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_reentry_digest_bound",
    "source_results_review_digest_bound",
    "source_cache_manifest_digest_bound",
    "source_execution_digest_bound",
    "source_classification_manifest_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "cache_source_counts_bound",
    "module_summary_bound",
    "classification_source_limits_bound",
    "candidate_v2_created_true",
    "candidate_v2_ready_true",
    "ready_for_operator_review_true",
    "recommended_package_present",
    "v2_packages_present_9",
    "blocked_packages_present_4",
    "recommended_package_not_selected",
    "method_v2_selected_false",
    "method_v2_approved_false",
    "method_v2_authorized_false",
    "method_v2_executed_false",
    "classification_execution_created_false",
    "classification_execution_performed_false",
    "failure_modules_classified_false",
    "error_modules_classified_false",
    "first_failure_identified_false",
    "first_error_identified_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "pytest_cache_committed_false",
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
    "future_v2_requirements_defined",
    "future_v2_execution_plan_defined",
    "planned_outputs_defined",
    "non_goals_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(ValueError):
    """Raised when candidate v2 evidence or authority boundaries are invalid."""


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = expected == actual
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _committed_source_fields() -> dict[str, Any]:
    return {
        "source_classification_method_reentry_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1,
        "source_classification_method_reentry_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY,
        "source_classification_method_reentry_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN,
        "source_classification_method_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_classification_source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_cache_manifest_review_digest": SOURCE_CACHE_MANIFEST_REVIEW_DIGEST,
        "source_output_capture_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_classification_source_manifest_digest": SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST,
        "source_retry_failure_diagnosis_digest": SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST,
        "source_staged_inventory_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "root_full_regression_does_not_override_detached_retry_failure": True,
        "lastfailed_cache_entry_count": 1404,
        "nodeids_cache_entry_count": 26288,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "origin_main_commit": source.source.source.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_name": source.source.source.INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": source.source.source.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(source.source.source.EXPECTED_INTEGRATION_WORKTREE.resolve(strict=False)),
        "detached_integration_worktree_head_commit": source.source.source.INTEGRATION_HEAD_COMMIT,
        "staged_evidence_manifest_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "marketflow_outputs_tracked_in_repository": False,
        "pytest_cache_tracked_in_repository": False,
    }


def _source_fields(source_reentry: dict | None) -> dict[str, Any]:
    if source_reentry is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
        source_reentry
    )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_method_reentry_artifact_kind": "artifact_kind",
        "source_classification_method_reentry_status": "reentry_status",
        "source_classification_method_reentry_scope": "reentry_scope",
        "source_classification_method_reentry_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest",
        "source_classification_source_results_review_digest": "source_classification_results_review_digest",
        "largest_module_nodeid_counts": "largest_module_nodeid_counts_reviewed",
    }
    for target, source_field in mapping.items():
        fields[target] = deepcopy(source_reentry.get(source_field))
    for field in set(fields) - set(mapping):
        if field in source_reentry:
            fields[field] = deepcopy(source_reentry[field])
    return fields


def _package(candidate: Mapping[str, Any], package_id: str) -> Mapping[str, Any]:
    for package in candidate.get("proposed_classification_method_v2_packages", []):
        if package.get("package_id") == package_id:
            return package
    return {}


def _base_candidate(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        "operator_review_required": True,
        **deepcopy(dict(source_fields)),
        "classification_source_valid_for_v2_candidate": True,
        "classification_source_accepted_for_module_level_only": True,
        "classification_source_not_accepted_for_failure_error_separation": True,
        "classification_source_not_accepted_for_first_order_failure_analysis": True,
        "classification_source_not_accepted_for_traceback_root_cause": True,
        "classification_source_not_retry_success_evidence": True,
        "classification_source_limitations": list(CLASSIFICATION_SOURCE_LIMITATIONS),
        "candidate_v2_philosophy": CANDIDATE_V2_PHILOSOPHY,
        "candidate_v2_boundary": CANDIDATE_V2_BOUNDARY,
        "candidate_v2_goal": CANDIDATE_V2_GOAL,
        "proposed_classification_method_v2_packages": deepcopy(PROPOSED_V2_PACKAGES),
        "recommended_classification_method_v2_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": RECOMMENDATION_REASON,
        "future_classification_method_v2_requirements": deepcopy(FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS),
        "future_classification_method_v2_execution_plan": list(FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN),
        "future_classification_method_v2_execution_plan_status": FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN_STATUS,
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "non_goals": list(NON_GOALS),
        "classification_method_candidate_v2_created": True,
        "classification_method_candidate_v2_ready_for_operator_review": True,
        "ready_for_classification_method_candidate_v2_operator_review": True,
        "classification_method_v2_selected": False,
        "classification_method_v2_approved": False,
        "classification_method_v2_authorized": False,
        "classification_method_v2_executed": False,
        "classification_execution_created": False,
        "classification_execution_performed": False,
        "failure_modules_classified": False,
        "error_modules_classified": False,
        "first_failure_identified": False,
        "first_error_identified": False,
        "failure_error_separation_claimed": False,
        "first_order_failure_analysis_claimed": False,
        "traceback_root_cause_claimed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "integration_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = candidate.get("proposed_classification_method_v2_packages", [])
    recommended = _package(candidate, RECOMMENDED_PACKAGE)
    retry_counts = [candidate.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    values: dict[str, tuple[Any, Any]] = {
        "source_reentry_digest_bound": (SOURCE_REENTRY_DIGEST, candidate.get("source_classification_method_reentry_digest")),
        "source_results_review_digest_bound": (SOURCE_RESULTS_REVIEW_DIGEST, candidate.get("source_classification_source_results_review_digest")),
        "source_cache_manifest_digest_bound": (SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, candidate.get("source_cache_manifest_review_digest")),
        "source_execution_digest_bound": (SOURCE_EXECUTION_DIGEST, candidate.get("source_output_capture_execution_digest")),
        "source_classification_manifest_digest_bound": (SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST, candidate.get("source_classification_source_manifest_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], retry_counts),
        "cache_source_counts_bound": ([1404, 26288], [candidate.get("lastfailed_cache_entry_count"), candidate.get("nodeids_cache_entry_count")]),
        "module_summary_bound": ([29, [136, 131, 122, 112, 111]], [candidate.get("module_summary_module_count"), candidate.get("largest_module_nodeid_counts")]),
        "classification_source_limits_bound": (CLASSIFICATION_SOURCE_LIMITATIONS, candidate.get("classification_source_limitations")),
        "candidate_v2_created_true": (True, candidate.get("classification_method_candidate_v2_created")),
        "candidate_v2_ready_true": (True, candidate.get("classification_method_candidate_v2_ready_for_operator_review")),
        "ready_for_operator_review_true": (True, candidate.get("ready_for_classification_method_candidate_v2_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, recommended.get("package_id")),
        "v2_packages_present_9": (9, len(packages)),
        "blocked_packages_present_4": (4, sum(row.get("status") == "BLOCKED_NOT_ALLOWED" for row in packages)),
        "recommended_package_not_selected": ([RECOMMENDATION_STATUS, False, False, False], [recommended.get("status"), recommended.get("selected"), recommended.get("approved"), recommended.get("executed")]),
        "method_v2_selected_false": (False, candidate.get("classification_method_v2_selected")),
        "method_v2_approved_false": (False, candidate.get("classification_method_v2_approved")),
        "method_v2_authorized_false": (False, candidate.get("classification_method_v2_authorized")),
        "method_v2_executed_false": (False, candidate.get("classification_method_v2_executed")),
        "classification_execution_created_false": (False, candidate.get("classification_execution_created")),
        "classification_execution_performed_false": (False, candidate.get("classification_execution_performed")),
        "failure_modules_classified_false": (False, candidate.get("failure_modules_classified")),
        "error_modules_classified_false": (False, candidate.get("error_modules_classified")),
        "first_failure_identified_false": (False, candidate.get("first_failure_identified")),
        "first_error_identified_false": (False, candidate.get("first_error_identified")),
        "new_retry_candidate_created_false": (False, candidate.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, candidate.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, candidate.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, candidate.get("main_merge_approval_created")),
        "retry_rerun_false": (False, candidate.get("retry_rerun_performed")),
        "full_pytest_false": (False, candidate.get("full_pytest_performed")),
        "diagnostic_command_false": (False, candidate.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, candidate.get("diagnostic_output_captured")),
        "integration_success_false": (False, candidate.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [candidate.get("successful_integration_execution_digest_generated"), candidate.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
        "main_push_false": (False, candidate.get("main_push_performed")),
        "origin_main_modified_false": (False, candidate.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, candidate.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, candidate.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, candidate.get("evidence_regenerated")),
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
        "future_v2_requirements_defined": (FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS, candidate.get("future_classification_method_v2_requirements")),
        "future_v2_execution_plan_defined": ([FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN, FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN_STATUS], [candidate.get("future_classification_method_v2_execution_plan"), candidate.get("future_classification_method_v2_execution_plan_status")]),
        "planned_outputs_defined": (PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (True, candidate.get("no_tracked_marketflow_files")),
        "no_tracked_pytest_cache_files": (True, candidate.get("no_tracked_pytest_cache_files")),
    }
    return [_record(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(candidate: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "classification_method_candidate_v2_created": candidate.get("classification_method_candidate_v2_created"),
        "classification_method_candidate_v2_ready_for_operator_review": candidate.get("classification_method_candidate_v2_ready_for_operator_review"),
        "recommended_classification_method_v2_package": candidate.get("recommended_classification_method_v2_package"),
        "method_v2_selected": candidate.get("classification_method_v2_selected"),
        "method_v2_approved": candidate.get("classification_method_v2_approved"),
        "method_v2_executed": candidate.get("classification_method_v2_executed"),
        "classification_execution_performed": candidate.get("classification_execution_performed"),
        "new_retry_candidate_created": candidate.get("new_retry_candidate_created"),
        "new_retry_executed": candidate.get("new_retry_executed"),
        "integration_execution_successful": candidate.get("integration_execution_successful"),
        "recommended_next_task": candidate.get("recommended_next_task"),
        "predictive_usefulness_accepted": candidate.get("predictive_usefulness_accepted"),
        "profitability_accepted": candidate.get("profitability_accepted"),
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
    *, source_reentry: dict | None = None,
) -> dict:
    """Build the offline candidate package catalog without reading cache."""
    candidate = _base_candidate(_source_fields(source_reentry))
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate, candidate["checklist"])
    candidate[
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"
    ] = marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest_v1(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
    candidate: dict,
) -> dict:
    """Validate the candidate catalog and reject selection or expanded authority."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "candidate must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_committed_source_fields(),
        "classification_source_limitations": CLASSIFICATION_SOURCE_LIMITATIONS,
        "candidate_v2_philosophy": CANDIDATE_V2_PHILOSOPHY,
        "candidate_v2_boundary": CANDIDATE_V2_BOUNDARY,
        "candidate_v2_goal": CANDIDATE_V2_GOAL,
        "proposed_classification_method_v2_packages": PROPOSED_V2_PACKAGES,
        "recommended_classification_method_v2_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": RECOMMENDATION_REASON,
        "future_classification_method_v2_requirements": FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS,
        "future_classification_method_v2_execution_plan": FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN,
        "future_classification_method_v2_execution_plan_status": FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN_STATUS,
        "planned_outputs": PLANNED_OUTPUTS,
        "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(candidate.get(field), expected, field)
    for field in (
        "created_offline",
        "governance_only",
        "candidate_only",
        "operator_review_required",
        "classification_source_valid_for_v2_candidate",
        "classification_source_accepted_for_module_level_only",
        "classification_source_not_accepted_for_failure_error_separation",
        "classification_source_not_accepted_for_first_order_failure_analysis",
        "classification_source_not_accepted_for_traceback_root_cause",
        "classification_source_not_retry_success_evidence",
        "classification_method_candidate_v2_created",
        "classification_method_candidate_v2_ready_for_operator_review",
        "ready_for_classification_method_candidate_v2_operator_review",
        "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files",
    ):
        _expect(candidate.get(field), True, field)
    for field in (
        "classification_method_v2_selected",
        "classification_method_v2_approved",
        "classification_method_v2_authorized",
        "classification_method_v2_executed",
        "classification_execution_created",
        "classification_execution_performed",
        "failure_modules_classified",
        "error_modules_classified",
        "first_failure_identified",
        "first_error_identified",
        "failure_error_separation_claimed",
        "first_order_failure_analysis_claimed",
        "traceback_root_cause_claimed",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    packages = candidate.get("proposed_classification_method_v2_packages")
    if not isinstance(packages, list) or len(packages) != 9:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "v2 packages missing"
        )
    if any(row.get("selected") or row.get("approved") or row.get("executed") for row in packages):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "candidate package authority expanded"
        )
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "checklist missing"
        )
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "candidate checklist failed"
        )
    _expect(candidate.get("summary"), _summary(candidate, checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "artifact_kind": candidate["artifact_kind"],
        "status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest": digest,
        **{
            key: candidate["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated candidate v2 package catalog as Markdown."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
        candidate
    )
    sections = [
        ("Source Reentry", [f"Reentry digest: `{candidate['source_classification_method_reentry_digest']}`."]),
        ("Source Classification-Source Review", [f"Results-review digest: `{candidate['source_classification_source_results_review_digest']}`.", f"Cache-manifest review digest: `{candidate['source_cache_manifest_review_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry remains `24877 passed, 1292 failed, 112 errors, 7 skipped`."]),
        ("Candidate Scope", [candidate["candidate_v2_boundary"]]),
        ("Candidate Philosophy", [candidate["candidate_v2_philosophy"], candidate["candidate_v2_goal"]]),
        ("Proposed v2 Packages", [f"`{row['package_id']}` - `{row['status']}`." for row in candidate["proposed_classification_method_v2_packages"]]),
        ("Recommended v2 Package", [f"`{candidate['recommended_classification_method_v2_package']}` - `{candidate['recommendation_status']}`. {candidate['recommendation_reason']}"]),
        ("Future v2 Requirements", [f"`{key}`: `{value}`" for key, value in candidate["future_classification_method_v2_requirements"].items()]),
        ("Future v2 Execution Plan", [*candidate["future_classification_method_v2_execution_plan"], f"Status: `{candidate['future_classification_method_v2_execution_plan_status']}`."]),
        ("Planned Outputs", [f"`{key}`: `{value}`" for key, value in candidate["planned_outputs"].items()]),
        ("Non-Goals", [f"`{row}`" for row in candidate["non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        ("Authority Boundaries", ["No package is selected, approved, authorized, or executed; retry, main merge, runtime, and trading remain closed."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The candidate uses committed source constants and does not read cache.", "Operator review and separate approval are required before any v2 execution."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Classification Method Candidate v2",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
    output_dir: str | Path,
    *, source_reentry: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting existing output."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
        source_reentry=source_reentry
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
