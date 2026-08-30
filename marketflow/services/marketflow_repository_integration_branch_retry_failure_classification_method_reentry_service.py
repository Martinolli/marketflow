"""Select the safe classification-method reentry path from reviewed cache evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN"
)

SOURCE_RESULTS_REVIEW_DIGEST = "a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9"
SOURCE_CACHE_MANIFEST_REVIEW_DIGEST = "cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee"
SOURCE_EXECUTION_DIGEST = "b7c987e76b02a026bc118ae05801e4ba02c92bdadb81df9562e28a646b4f80bb"
SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST = "9218bad7b0b176bd3b4398293304159f22c1772fad0fa91b6e1d275a770ebcca"
REENTRY_DECISION = "NEW_CLASSIFICATION_METHOD_CANDIDATE_V2_REQUIRED"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CLASSIFICATION_SOURCE_VALIDITY_BASIS = (
    "Reviewed detached pytest-cache lastfailed source contains 1,404 node IDs and reviewed module summary with 29 modules."
)
CLASSIFICATION_SOURCE_REENTRY_LIMITATIONS = [
    "cannot distinguish failures from errors",
    "cannot identify first failure",
    "cannot identify first error",
    "cannot provide traceback snippets",
    "cannot by itself recommend code remediation",
    "cannot replace authoritative failed retry",
]
CLASSIFICATION_SOURCE_ACCEPTED_FOR = [
    "module-level grouping",
    "node-id inventory",
    "bounded root-cause family candidate pre-classification",
    "planning a method candidate v2",
]
CLASSIFICATION_SOURCE_NOT_ACCEPTED_FOR = [
    "failure/error separation",
    "first failure ordering",
    "traceback-based root cause",
    "remediation execution",
    "retry success evidence",
    "main merge approval",
]
REENTRY_REASON = (
    "The reviewed cache source is valid but limited. It supports a safer v2 method candidate focused on "
    "module-level grouping and node-ID classification, not direct execution of the earlier method that "
    "expected failure/error separation and first-order trace detail."
)

REENTRY_OPTIONS = [
    {
        "option_id": "OPTION_DIRECT_REENTER_ORIGINAL_CLASSIFICATION_METHOD",
        "status": "NOT_RECOMMENDED_LIMITED_SOURCE",
        "reason": "The original method expected failure/error module separation and first failure/error detail that the cache source does not provide.",
        "selected": False,
    },
    {
        "option_id": "OPTION_CREATE_CLASSIFICATION_METHOD_CANDIDATE_V2_FOR_CACHE_SOURCE",
        "status": "RECOMMENDED_FOR_NEXT_TASK",
        "reason": "A v2 method can use cache-source node IDs within known limitations and avoid unsupported claims.",
        "selected": True,
    },
    {
        "option_id": "OPTION_REQUIRE_DIAGNOSTIC_OUTPUT_CAPTURE_BEFORE_ANY_CLASSIFICATION",
        "status": "AVAILABLE_NOT_SELECTED",
        "reason": "Diagnostic output capture could provide richer traceback detail, but the current cache source is enough for module-level v2 candidate planning.",
        "selected": False,
    },
    {
        "option_id": "OPTION_NEW_RETRY_WITHOUT_CLASSIFICATION",
        "status": "BLOCKED_NOT_ALLOWED",
        "reason": "Another retry without classification or remediation would repeat a failed path.",
        "selected": False,
    },
    {
        "option_id": "OPTION_MAIN_MERGE_DESPITE_FAILED_RETRY",
        "status": "BLOCKED_NOT_ALLOWED",
        "reason": "Main merge remains blocked until a future retry results review passes.",
        "selected": False,
    },
]

FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS = {
    "source_classification_results_review_must_be_ready": True,
    "cache_source_must_remain_reviewed_and_digest_bound": True,
    "v2_method_must_limit_scope_to_cache_supported_claims": True,
    "v2_method_must_not_claim_failure_error_separation": True,
    "v2_method_must_not_claim_first_failure": True,
    "v2_method_must_not_claim_first_error": True,
    "v2_method_must_not_use_cache_as_retry_success_evidence": True,
    "v2_method_must_preserve_failed_retry_authority": True,
    "v2_method_must_produce_module_grouping_candidate_only": True,
    "v2_method_must_keep_retry_and_main_merge_closed": True,
    "v2_method_execution_requires_separate_approval": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN = [
    "Bind classification-source results-review digest and cache-manifest digest.",
    "Define cache-supported outputs: node-id inventory, module summary, module-name-only candidate root-cause family hints, and limitation report.",
    "Prohibit failure/error separation, first-failure ordering, and traceback-based root-cause outputs.",
    "Define module grouping, evidence-root mapping, path/cwd assumption mapping, digest-drift mapping, and fallback diagnostic-output-capture packages.",
    "Keep the v2 candidate planning-only.",
    "Require operator review and approval before v2 execution.",
    "Keep new retry candidate, main merge, runtime, and trading closed.",
]
FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN_STATUS = "PLANNED_NOT_EXECUTED"

NEXT_CHAIN = [
    "New Classification Method Candidate v2.",
    "New Classification Method Candidate Operator Review v2.",
    "New Classification Method Approval v2, if selected.",
    "New Classification Method Execution v2, if approved.",
    "New Classification Method Results Review v2.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "new_classification_method_candidate_v2",
    "new_classification_method_candidate_operator_review_v2",
    "new_classification_method_approval_v2_if_selected",
    "new_classification_method_execution_v2_if_approved",
    "new_classification_method_results_review_v2",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "reentry_does_not_classify_modules",
    "reentry_does_not_execute_classification",
    "reentry_does_not_read_or_modify_cache",
    "reentry_does_not_parse_operator_logs",
    "reentry_does_not_run_diagnostic_commands",
    "reentry_does_not_rerun_retry",
    "reentry_does_not_run_full_pytest",
    "reentry_does_not_treat_cache_as_retry_evidence",
    "reentry_does_not_replace_failed_retry_result",
    "reentry_does_not_create_new_retry_candidate",
    "reentry_does_not_create_retry_results_review",
    "reentry_does_not_create_integration_results_review",
    "reentry_does_not_mark_integration_successful",
    "reentry_does_not_generate_successful_integration_execution_digest",
    "reentry_does_not_generate_successful_integration_validation_digest",
    "reentry_does_not_stage_additional_evidence",
    "reentry_does_not_modify_staged_evidence",
    "reentry_does_not_regenerate_evidence",
    "reentry_does_not_call_providers",
    "reentry_does_not_commit_marketflow_outputs",
    "reentry_does_not_commit_pytest_cache",
    "reentry_does_not_push_integration_branch",
    "reentry_does_not_push_main",
    "reentry_does_not_delete_integration_branch",
    "reentry_does_not_delete_worktree",
    "reentry_does_not_force_push",
    "reentry_does_not_prune_remotes",
    "reentry_does_not_modify_tags",
    "reentry_does_not_acquire_market_data",
    "reentry_does_not_regenerate_dataset",
    "reentry_does_not_recompute_metrics",
    "reentry_does_not_train_models",
    "reentry_does_not_score_strategy",
    "reentry_does_not_generate_recommendations",
    "reentry_does_not_accept_predictive_usefulness",
    "reentry_does_not_accept_profitability",
    "reentry_does_not_authorize_runtime",
    "reentry_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_v2_candidate_required",
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
    "source_results_review_digest_bound",
    "source_cache_manifest_digest_bound",
    "source_execution_digest_bound",
    "source_classification_source_manifest_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "cache_counts_bound",
    "module_summary_bound",
    "limitations_bound",
    "classification_source_valid_for_reentry_true",
    "classification_source_accepted_for_module_level_only_true",
    "classification_source_not_accepted_for_failure_error_separation_true",
    "classification_source_not_accepted_for_first_order_failure_analysis_true",
    "reentry_decision_v2_required",
    "recommended_option_selected_v2_candidate",
    "direct_reentry_not_recommended",
    "new_retry_without_classification_blocked",
    "main_merge_despite_failure_blocked",
    "reentry_created_true",
    "reentry_ready_true",
    "classification_execution_created_false",
    "classification_execution_performed_false",
    "failure_modules_classified_false",
    "error_modules_classified_false",
    "first_failure_identified_false",
    "first_error_identified_false",
    "new_classification_method_candidate_created_false",
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
    "future_v2_candidate_plan_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(ValueError):
    """Raised when reentry evidence or authority boundaries are invalid."""


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
        "source_classification_results_review_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1,
        "source_classification_results_review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY,
        "source_classification_results_review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN,
        "source_classification_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_cache_manifest_review_digest": SOURCE_CACHE_MANIFEST_REVIEW_DIGEST,
        "source_output_capture_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_classification_source_manifest_digest": SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST,
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "root_full_regression_does_not_override_detached_retry_failure": True,
        "classification_source_results_review_created": True,
        "classification_source_results_review_ready": True,
        "classification_source_reviewed": True,
        "lastfailed_cache_reviewed": True,
        "nodeids_cache_reviewed": True,
        "module_summary_reviewed": True,
        "classification_source_limitations_reviewed": True,
        "ready_for_classification_method_reentry": True,
        "classification_source_generated": True,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_contains_nodeids": True,
        "lastfailed_cache_sha256": source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count": 1404,
        "nodeids_cache_sha256": source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count": 26288,
        "failed_or_errored_nodeids_count_reviewed": 1404,
        "module_summary_module_count": 29,
        "module_summary_untruncated": True,
        "largest_module_nodeid_counts_reviewed": [136, 131, 122, 112, 111],
        "source_classification_source_limitations": list(source.CLASSIFICATION_SOURCE_LIMITATIONS),
        "origin_main_commit": source.source.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_name": source.source.INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": source.source.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(source.source.EXPECTED_INTEGRATION_WORKTREE.resolve(strict=False)),
        "detached_integration_worktree_head_commit": source.source.INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_manifest_digest": source.source.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
    }


def _source_fields(source_results_review: dict | None) -> dict[str, Any]:
    if source_results_review is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        source_results_review
    )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_results_review_artifact_kind": "artifact_kind",
        "source_classification_results_review_status": "review_status",
        "source_classification_results_review_scope": "review_scope",
        "source_classification_results_review_digest": "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest",
        "source_cache_manifest_review_digest": "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest",
        "lastfailed_cache_sha256": "lastfailed_cache_sha256_at_review",
        "lastfailed_cache_entry_count": "lastfailed_cache_entry_count_at_review",
        "nodeids_cache_sha256": "nodeids_cache_sha256_at_review",
        "nodeids_cache_entry_count": "nodeids_cache_entry_count_at_review",
        "source_classification_source_limitations": "classification_source_limitations",
    }
    for target, source_field in mapping.items():
        fields[target] = deepcopy(source_results_review.get(source_field))
    direct = set(fields) - set(mapping)
    for field in direct:
        if field in source_results_review:
            fields[field] = deepcopy(source_results_review[field])
    return fields


def _option(reentry: Mapping[str, Any], option_id: str) -> Mapping[str, Any]:
    for option in reentry.get("reentry_options", []):
        if option.get("option_id") == option_id:
            return option
    return {}


def _base_reentry(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1,
        "reentry_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY,
        "reentry_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "reentry_only": True,
        **deepcopy(dict(source_fields)),
        "classification_source_valid_for_reentry": True,
        "classification_source_validity_basis": CLASSIFICATION_SOURCE_VALIDITY_BASIS,
        "classification_source_reentry_limitations": list(CLASSIFICATION_SOURCE_REENTRY_LIMITATIONS),
        "classification_source_accepted_for": list(CLASSIFICATION_SOURCE_ACCEPTED_FOR),
        "classification_source_not_accepted_for": list(CLASSIFICATION_SOURCE_NOT_ACCEPTED_FOR),
        "classification_source_accepted_for_reentry": True,
        "classification_source_accepted_for_module_level_only": True,
        "classification_source_accepted_for_failure_error_separation": False,
        "classification_source_accepted_for_first_order_failure_analysis": False,
        "classification_source_not_accepted_for_failure_error_separation": True,
        "classification_source_not_accepted_for_first_order_failure_analysis": True,
        "reentry_decision": REENTRY_DECISION,
        "recommended_reentry_path": REENTRY_DECISION,
        "reentry_reason": REENTRY_REASON,
        "reentry_options": deepcopy(REENTRY_OPTIONS),
        "future_classification_method_v2_requirements": deepcopy(FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS),
        "future_classification_method_v2_candidate_plan": list(FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN),
        "future_classification_method_v2_candidate_plan_status": FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN_STATUS,
        "classification_method_reentry_created": True,
        "classification_method_reentry_ready": True,
        "classification_execution_created": False,
        "classification_execution_performed": False,
        "failure_modules_classified": False,
        "error_modules_classified": False,
        "first_failure_identified": False,
        "first_error_identified": False,
        "new_classification_method_candidate_created": False,
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
        "provider_requests_made_in_reentry": False,
        "market_data_acquisition_performed_in_reentry": False,
        "dataset_generation_performed_in_reentry": False,
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


def _checklist(reentry: Mapping[str, Any]) -> list[dict[str, Any]]:
    retry_counts = [reentry.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]
    cache_counts = [reentry.get("lastfailed_cache_entry_count"), reentry.get("nodeids_cache_entry_count")]
    v2_option = _option(reentry, "OPTION_CREATE_CLASSIFICATION_METHOD_CANDIDATE_V2_FOR_CACHE_SOURCE")
    direct_option = _option(reentry, "OPTION_DIRECT_REENTER_ORIGINAL_CLASSIFICATION_METHOD")
    retry_option = _option(reentry, "OPTION_NEW_RETRY_WITHOUT_CLASSIFICATION")
    merge_option = _option(reentry, "OPTION_MAIN_MERGE_DESPITE_FAILED_RETRY")
    values: dict[str, tuple[Any, Any]] = {
        "source_results_review_digest_bound": (SOURCE_RESULTS_REVIEW_DIGEST, reentry.get("source_classification_results_review_digest")),
        "source_cache_manifest_digest_bound": (SOURCE_CACHE_MANIFEST_REVIEW_DIGEST, reentry.get("source_cache_manifest_review_digest")),
        "source_execution_digest_bound": (SOURCE_EXECUTION_DIGEST, reentry.get("source_output_capture_execution_digest")),
        "source_classification_source_manifest_digest_bound": (SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST, reentry.get("source_classification_source_manifest_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", reentry.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], retry_counts),
        "cache_counts_bound": ([1404, 26288], cache_counts),
        "module_summary_bound": ([29, True, [136, 131, 122, 112, 111]], [reentry.get("module_summary_module_count"), reentry.get("module_summary_untruncated"), reentry.get("largest_module_nodeid_counts_reviewed")]),
        "limitations_bound": (CLASSIFICATION_SOURCE_REENTRY_LIMITATIONS, reentry.get("classification_source_reentry_limitations")),
        "classification_source_valid_for_reentry_true": (True, reentry.get("classification_source_valid_for_reentry")),
        "classification_source_accepted_for_module_level_only_true": (True, reentry.get("classification_source_accepted_for_module_level_only")),
        "classification_source_not_accepted_for_failure_error_separation_true": ([False, True], [reentry.get("classification_source_accepted_for_failure_error_separation"), reentry.get("classification_source_not_accepted_for_failure_error_separation")]),
        "classification_source_not_accepted_for_first_order_failure_analysis_true": ([False, True], [reentry.get("classification_source_accepted_for_first_order_failure_analysis"), reentry.get("classification_source_not_accepted_for_first_order_failure_analysis")]),
        "reentry_decision_v2_required": (REENTRY_DECISION, reentry.get("reentry_decision")),
        "recommended_option_selected_v2_candidate": (["RECOMMENDED_FOR_NEXT_TASK", True], [v2_option.get("status"), v2_option.get("selected")]),
        "direct_reentry_not_recommended": (["NOT_RECOMMENDED_LIMITED_SOURCE", False], [direct_option.get("status"), direct_option.get("selected")]),
        "new_retry_without_classification_blocked": (["BLOCKED_NOT_ALLOWED", False], [retry_option.get("status"), retry_option.get("selected")]),
        "main_merge_despite_failure_blocked": (["BLOCKED_NOT_ALLOWED", False], [merge_option.get("status"), merge_option.get("selected")]),
        "reentry_created_true": (True, reentry.get("classification_method_reentry_created")),
        "reentry_ready_true": (True, reentry.get("classification_method_reentry_ready")),
        "classification_execution_created_false": (False, reentry.get("classification_execution_created")),
        "classification_execution_performed_false": (False, reentry.get("classification_execution_performed")),
        "failure_modules_classified_false": (False, reentry.get("failure_modules_classified")),
        "error_modules_classified_false": (False, reentry.get("error_modules_classified")),
        "first_failure_identified_false": (False, reentry.get("first_failure_identified")),
        "first_error_identified_false": (False, reentry.get("first_error_identified")),
        "new_classification_method_candidate_created_false": (False, reentry.get("new_classification_method_candidate_created")),
        "new_retry_candidate_created_false": (False, reentry.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, reentry.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, reentry.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, reentry.get("main_merge_approval_created")),
        "retry_rerun_false": (False, reentry.get("retry_rerun_performed")),
        "full_pytest_false": (False, reentry.get("full_pytest_performed")),
        "diagnostic_command_false": (False, reentry.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, reentry.get("diagnostic_output_captured")),
        "integration_success_false": (False, reentry.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [reentry.get("successful_integration_execution_digest_generated"), reentry.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, reentry.get("integration_branch_pushed")),
        "main_push_false": (False, reentry.get("main_push_performed")),
        "origin_main_modified_false": (False, reentry.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, reentry.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, reentry.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, reentry.get("evidence_regenerated")),
        "provider_requests_false": (False, reentry.get("provider_requests_made_in_reentry")),
        "market_data_acquisition_false": (False, reentry.get("market_data_acquisition_performed_in_reentry")),
        "dataset_generation_false": (False, reentry.get("dataset_generation_performed_in_reentry")),
        "metric_recomputation_false": (False, reentry.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, reentry.get("model_training_performed")),
        "strategy_scoring_false": (False, reentry.get("strategy_scoring_performed")),
        "recommendations_false": (False, reentry.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, reentry.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, reentry.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, reentry.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, reentry.get("broker_execution")),
        "future_v2_requirements_defined": (FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS, reentry.get("future_classification_method_v2_requirements")),
        "future_v2_candidate_plan_defined": ([FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN, FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN_STATUS], [reentry.get("future_classification_method_v2_candidate_plan"), reentry.get("future_classification_method_v2_candidate_plan_status")]),
        "next_chain_defined": (NEXT_CHAIN, reentry.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, reentry.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, reentry.get("risk_controls")),
        "no_tracked_marketflow_files": (True, reentry.get("no_tracked_marketflow_files")),
        "no_tracked_pytest_cache_files": (True, reentry.get("no_tracked_pytest_cache_files")),
    }
    return [_record(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(reentry: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "classification_method_reentry_created": reentry.get("classification_method_reentry_created"),
        "classification_method_reentry_ready": reentry.get("classification_method_reentry_ready"),
        "classification_source_valid_for_reentry": reentry.get("classification_source_valid_for_reentry"),
        "classification_source_accepted_for_reentry": reentry.get("classification_source_accepted_for_reentry"),
        "classification_source_accepted_for_module_level_only": reentry.get("classification_source_accepted_for_module_level_only"),
        "classification_source_not_accepted_for_failure_error_separation": reentry.get("classification_source_not_accepted_for_failure_error_separation"),
        "classification_source_not_accepted_for_first_order_failure_analysis": reentry.get("classification_source_not_accepted_for_first_order_failure_analysis"),
        "recommended_reentry_path": reentry.get("recommended_reentry_path"),
        "classification_execution_performed": reentry.get("classification_execution_performed"),
        "new_classification_method_candidate_created": reentry.get("new_classification_method_candidate_created"),
        "new_retry_candidate_created": reentry.get("new_retry_candidate_created"),
        "new_retry_executed": reentry.get("new_retry_executed"),
        "integration_execution_successful": reentry.get("integration_execution_successful"),
        "recommended_next_task": reentry.get("recommended_next_task"),
        "predictive_usefulness_accepted": reentry.get("predictive_usefulness_accepted"),
        "profitability_accepted": reentry.get("profitability_accepted"),
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest_v1(
    reentry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(reentry))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
    *, source_results_review: dict | None = None,
) -> dict:
    """Build the offline, digest-bound reentry decision without reading cache."""
    reentry = _base_reentry(_source_fields(source_results_review))
    reentry["checklist"] = _checklist(reentry)
    reentry["summary"] = _summary(reentry, reentry["checklist"])
    reentry[
        "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"
    ] = marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest_v1(reentry)
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(reentry)
    return reentry


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
    reentry: dict,
) -> dict:
    """Validate the reentry decision and reject any expanded authority."""
    if not isinstance(reentry, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            "reentry must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1,
        "reentry_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY,
        "reentry_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN,
        **_committed_source_fields(),
        "classification_source_validity_basis": CLASSIFICATION_SOURCE_VALIDITY_BASIS,
        "classification_source_reentry_limitations": CLASSIFICATION_SOURCE_REENTRY_LIMITATIONS,
        "classification_source_accepted_for": CLASSIFICATION_SOURCE_ACCEPTED_FOR,
        "classification_source_not_accepted_for": CLASSIFICATION_SOURCE_NOT_ACCEPTED_FOR,
        "reentry_decision": REENTRY_DECISION,
        "recommended_reentry_path": REENTRY_DECISION,
        "reentry_reason": REENTRY_REASON,
        "reentry_options": REENTRY_OPTIONS,
        "future_classification_method_v2_requirements": FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS,
        "future_classification_method_v2_candidate_plan": FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN,
        "future_classification_method_v2_candidate_plan_status": FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN_STATUS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(reentry.get(field), expected, field)
    for field in (
        "created_offline",
        "governance_only",
        "reentry_only",
        "classification_source_valid_for_reentry",
        "classification_source_accepted_for_reentry",
        "classification_source_accepted_for_module_level_only",
        "classification_source_not_accepted_for_failure_error_separation",
        "classification_source_not_accepted_for_first_order_failure_analysis",
        "classification_method_reentry_created",
        "classification_method_reentry_ready",
        "no_tracked_marketflow_files",
        "no_tracked_pytest_cache_files",
    ):
        _expect(reentry.get(field), True, field)
    for field in (
        "classification_source_accepted_for_failure_error_separation",
        "classification_source_accepted_for_first_order_failure_analysis",
        "classification_execution_created",
        "classification_execution_performed",
        "failure_modules_classified",
        "error_modules_classified",
        "first_failure_identified",
        "first_error_identified",
        "new_classification_method_candidate_created",
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
        "provider_requests_made_in_reentry",
        "market_data_acquisition_performed_in_reentry",
        "dataset_generation_performed_in_reentry",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(reentry.get(field), False, field)
    _expect(reentry.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(reentry.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(reentry.get(field), NOT_AUTHORIZED, field)
    checklist = reentry.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            "checklist missing"
        )
    _expect(checklist, _checklist(reentry), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            "reentry checklist failed"
        )
    _expect(reentry.get("summary"), _summary(reentry, checklist), "summary")
    digest = reentry.get(
        "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            "reentry digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest_v1(reentry),
        "reentry digest",
    )
    return {
        "artifact_kind": reentry["artifact_kind"],
        "status": reentry["reentry_status"],
        "reentry_scope": reentry["reentry_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest": digest,
        **{
            key: reentry["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_markdown_v1(
    reentry: dict,
) -> str:
    """Render the validated classification-method reentry as Markdown."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
        reentry
    )
    sections = [
        ("Source Classification-Source Results Review", [f"Review digest: `{reentry['source_classification_results_review_digest']}`.", f"Cache-manifest review digest: `{reentry['source_cache_manifest_review_digest']}`."]),
        ("Retry Failure Context", ["Authoritative retry remains `24877 passed, 1292 failed, 112 errors, 7 skipped`."]),
        ("Cache Source Capability", [f"Accepted only for: {', '.join(reentry['classification_source_accepted_for'])}."]),
        ("Cache Source Limitations", reentry["classification_source_reentry_limitations"]),
        ("Reentry Decision", [f"`{reentry['reentry_decision']}`: {reentry['reentry_reason']}"]),
        ("Reentry Options", [f"`{row['option_id']}` - `{row['status']}` - selected `{row['selected']}`." for row in reentry["reentry_options"]]),
        ("Future Classification Method v2 Requirements", [f"`{key}`: `{value}`" for key, value in reentry["future_classification_method_v2_requirements"].items()]),
        ("Future Classification Method v2 Candidate Plan", [*reentry["future_classification_method_v2_candidate_plan"], f"Status: `{reentry['future_classification_method_v2_candidate_plan_status']}`."]),
        ("Authority Boundaries", ["No classification execution, retry, results review, integration success, main merge, runtime, or trading authority is created."]),
        ("Next Chain", reentry["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in reentry["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in reentry["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["The reentry uses committed source constants and does not read cache.", "A separate v2 candidate, review, approval, and execution chain is required."]),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Classification Method Reentry v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
    output_dir: str | Path,
    *, source_results_review: dict | None = None,
) -> dict:
    """Write canonical reentry JSON without overwriting existing output."""
    reentry = build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
        source_results_review=source_results_review
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
        reentry
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError(
            "reentry output already exists"
        )
    payload = canonical_json_bytes(reentry)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": reentry["artifact_kind"],
        "reentry_status": reentry["reentry_status"],
        "reentry_scope": reentry["reentry_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
