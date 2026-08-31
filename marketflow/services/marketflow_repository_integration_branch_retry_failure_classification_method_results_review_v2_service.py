"""Review successful classification-method execution v2 without re-execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2 = (
    "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)
SOURCE_EXECUTION_V2_DIGEST = "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017"
SOURCE_MODULE_GROUPING_DIGEST = "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"
SOURCE_DIGEST_MANIFEST_DIGEST = "ac0b172d1ed107922fb0dc115b931752848e9da5db882586cd71897a41cc6add"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PLANNED_OUTPUTS_REVIEW = {
    "classification_v2_manifest": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "module_nodeid_grouping_report": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "module_summary_report": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "largest_module_summary": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "cache_source_limitation_report": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "low_confidence_root_cause_hint_report": "REVIEWED_NOT_GENERATED_BY_SELECTED_PACKAGE",
    "unsupported_claims_exclusion_report": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "recommended_next_method_or_remediation_report": "REVIEWED_GENERATED_RESEARCH_ONLY",
    "digest_manifest": "REVIEWED_GENERATED_RESEARCH_ONLY",
}
NEXT_CHAIN = [
    "Remediation or Method Candidate After Classification v2 Review v1.",
    "Candidate Operator Review.", "Approval, if selected.", "Execution, if approved.",
    "Results Review.",
    "New Integration Branch Retry Candidate v1, only after classification/remediation path.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_or_method_candidate_after_v2_review",
    "remediation_or_method_candidate_operator_review",
    "remediation_or_method_approval_if_selected", "remediation_or_method_execution_if_approved",
    "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_classification_or_remediation",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "review_v2_does_not_reexecute_classification", "review_v2_does_not_run_retry",
    "review_v2_does_not_run_full_pytest", "review_v2_does_not_run_diagnostic_commands",
    "review_v2_does_not_claim_failure_error_separation", "review_v2_does_not_claim_first_failure",
    "review_v2_does_not_claim_first_error", "review_v2_does_not_claim_traceback_root_cause",
    "review_v2_does_not_use_classification_as_retry_success_evidence",
    "review_v2_does_not_create_remediation_candidate", "review_v2_does_not_create_new_retry_candidate",
    "review_v2_does_not_create_retry_results_review", "review_v2_does_not_create_integration_results_review",
    "review_v2_does_not_mark_integration_successful",
    "review_v2_does_not_generate_successful_integration_digest",
    "review_v2_does_not_push_integration_branch", "review_v2_does_not_push_main",
    "review_v2_does_not_delete_integration_branch", "review_v2_does_not_delete_worktree",
    "review_v2_does_not_force_push", "review_v2_does_not_prune_remotes",
    "review_v2_does_not_modify_tags", "review_v2_does_not_commit_marketflow_outputs",
    "review_v2_does_not_commit_pytest_cache", "review_v2_does_not_modify_staged_evidence",
    "review_v2_does_not_regenerate_evidence", "review_v2_does_not_call_providers",
    "review_v2_does_not_acquire_market_data", "review_v2_does_not_regenerate_dataset",
    "review_v2_does_not_recompute_metrics", "review_v2_does_not_train_models",
    "review_v2_does_not_score_strategy", "review_v2_does_not_generate_recommendations",
    "review_v2_does_not_accept_predictive_usefulness", "review_v2_does_not_accept_profitability",
    "review_v2_does_not_authorize_runtime", "review_v2_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_remediation_or_method_candidate_required",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
OBSERVATION_IDS = [
    "source_execution_digest_bound", "module_grouping_digest_bound", "digest_manifest_bound",
    "module_level_grouping_reviewed", "module_summary_reviewed", "largest_module_summary_reviewed",
    "limitations_reviewed", "unsupported_claims_reviewed", "no_failure_error_separation_claimed",
    "no_first_order_claimed", "no_traceback_root_cause_claimed", "no_retry_success_claimed",
    "no_main_merge_readiness_claimed", "failed_retry_preserved", "root_regression_not_retry_evidence",
    "ready_for_remediation_or_method_candidate_after_v2_review", "no_retry_rerun",
    "no_full_pytest", "no_diagnostic_command", "no_new_retry_candidate",
    "no_integration_success", "no_protected_branch_push", "no_provider_or_runtime_actions",
]
CHECK_IDS = [
    "source_execution_digest_bound", "source_module_grouping_digest_bound", "source_digest_manifest_bound",
    "source_approval_digest_bound", "retry_execution_commit_bound", "retry_failure_counts_bound",
    "module_grouping_reviewed_true", "module_summary_reviewed_true", "module_count_29",
    "largest_module_counts_reviewed", "failed_or_errored_nodeids_1404", "limitations_reviewed_true",
    "unsupported_claims_exclusion_reviewed_true", "failure_modules_classified_false",
    "error_modules_classified_false", "failure_error_separation_claimed_false",
    "first_failure_identified_false", "first_error_identified_false", "first_order_claim_made_false",
    "traceback_root_cause_claimed_false", "retry_success_claimed_false",
    "main_merge_readiness_claimed_false", "planned_outputs_reviewed_true",
    "results_review_created_true", "results_review_ready_true",
    "ready_for_remediation_or_method_candidate_after_v2_review_true",
    "remediation_or_method_candidate_created_false", "new_retry_candidate_created_false",
    "new_retry_executed_false", "new_retry_results_review_created_false",
    "main_merge_approval_created_false", "retry_rerun_false", "full_pytest_false",
    "diagnostic_command_false", "diagnostic_output_false", "integration_success_false",
    "successful_integration_digest_false", "integration_branch_pushed_false", "main_push_false",
    "origin_main_modified_false", "marketflow_outputs_committed_false", "pytest_cache_committed_false",
    "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false",
    "strategy_scoring_false", "recommendations_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "broker_not_authorized",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(ValueError):
    """Raised when reviewed execution evidence or review boundaries are invalid."""


def _committed_source_fields() -> dict[str, Any]:
    execution_source = source._source_fields()
    return {
        "source_classification_method_execution_v2_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2,
        "source_classification_method_execution_v2_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY,
        "source_classification_method_execution_v2_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_classification_method_execution_v2_digest": SOURCE_EXECUTION_V2_DIGEST,
        "source_classification_method_v2_module_grouping_digest": SOURCE_MODULE_GROUPING_DIGEST,
        "source_classification_method_v2_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        **execution_source,
        "selected_classification_method_v2_package": source.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "lastfailed_cache_path": str(
            source.DEFAULT_INTEGRATION_WORKTREE.resolve(strict=False)
            / ".pytest_cache"
            / "v"
            / "cache"
            / "lastfailed"
        ),
        "lastfailed_cache_sha256": source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count": 1404, "nodeids_cache_entry_count": 26288,
        "nodeids_cache_path": str(
            source.DEFAULT_INTEGRATION_WORKTREE.resolve(strict=False)
            / ".pytest_cache"
            / "v"
            / "cache"
            / "nodeids"
        ),
        "nodeids_cache_sha256": source.EXPECTED_NODEIDS_SHA256,
        "classification_method_v2_executed": True, "classification_execution_created": True,
        "classification_execution_performed": True,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_used_for_module_level_only": True,
        "failed_or_errored_nodeids_classified": True, "failed_or_errored_nodeids_count": 1404,
        "module_level_grouping_generated": True, "module_summary_generated": True,
        "module_summary_module_count": 29, "largest_module_summary_generated": True,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "deterministic_ordering": ["descending count", "ascending module path"],
        "sample_nodeids_bounded_per_module": 5,
        "failure_modules_classified": False, "error_modules_classified": False,
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "retry_success_claimed": False,
        "main_merge_readiness_claimed": False, "root_cause_family_hints_generated": False,
        "root_cause_family_hints_basis": "NOT_GENERATED_BY_SELECTED_PACKAGE",
        "limitations_report_generated": True, "unsupported_claims_exclusion_report_generated": True,
        "planned_outputs_generated": True,
        "origin_main_commit": source.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_name": source.INTEGRATION_BRANCH_NAME,
        "integration_branch_head_commit": source.EXPECTED_INTEGRATION_HEAD,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(source.DEFAULT_INTEGRATION_WORKTREE.resolve(strict=False)),
        "detached_integration_worktree_head_commit": source.EXPECTED_INTEGRATION_HEAD,
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_manifest_digest": source.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
    }


def _source_fields(source_execution: dict | None) -> dict[str, Any]:
    if source_execution is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
        source_execution
    )
    if source_execution.get("artifact_kind") != source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "source execution must be successful"
        )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_method_execution_v2_artifact_kind": "artifact_kind",
        "source_classification_method_execution_v2_status": "execution_status",
        "source_classification_method_execution_v2_scope": "execution_scope",
        "source_classification_method_execution_v2_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest",
        "source_classification_method_v2_module_grouping_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest",
        "source_classification_method_v2_digest_manifest_digest": "marketflow_repository_integration_branch_retry_failure_classification_method_v2_digest_manifest_digest",
    }
    for target, field in mapping.items():
        fields[target] = deepcopy(source_execution.get(field))
    for field in set(fields) - set(mapping):
        if field in source_execution:
            fields[field] = deepcopy(source_execution[field])
    return fields


def _observation(observation_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"observation_id": observation_id, "status": status,
            "expected": deepcopy(expected), "actual": deepcopy(actual),
            "message": f"{observation_id} {'confirmed' if status == PASS else 'not confirmed'}"}


def _observations(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "source_execution_digest_bound": (SOURCE_EXECUTION_V2_DIGEST, review.get("source_classification_method_execution_v2_digest")),
        "module_grouping_digest_bound": (SOURCE_MODULE_GROUPING_DIGEST, review.get("source_classification_method_v2_module_grouping_digest")),
        "digest_manifest_bound": (SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_classification_method_v2_digest_manifest_digest")),
        "module_level_grouping_reviewed": (True, review.get("module_level_grouping_reviewed")),
        "module_summary_reviewed": (True, review.get("module_summary_reviewed")),
        "largest_module_summary_reviewed": (True, review.get("largest_module_summary_reviewed")),
        "limitations_reviewed": (True, review.get("limitations_reviewed")),
        "unsupported_claims_reviewed": (True, review.get("unsupported_claims_exclusion_reviewed")),
        "no_failure_error_separation_claimed": (False, review.get("failure_error_separation_claimed")),
        "no_first_order_claimed": (False, review.get("first_order_claim_made")),
        "no_traceback_root_cause_claimed": (False, review.get("traceback_root_cause_claimed")),
        "no_retry_success_claimed": (False, review.get("retry_success_claimed")),
        "no_main_merge_readiness_claimed": (False, review.get("main_merge_readiness_claimed")),
        "failed_retry_preserved": (True, review.get("retry_pytest_first_result_authoritative")),
        "root_regression_not_retry_evidence": (False, review.get("root_full_regression_is_retry_evidence")),
        "ready_for_remediation_or_method_candidate_after_v2_review": (True, review.get("ready_for_remediation_or_method_candidate_after_v2_review")),
        "no_retry_rerun": (False, review.get("retry_rerun_performed")),
        "no_full_pytest": (False, review.get("full_pytest_performed")),
        "no_diagnostic_command": (False, review.get("diagnostic_command_executed")),
        "no_new_retry_candidate": (False, review.get("new_retry_candidate_created")),
        "no_integration_success": (False, review.get("integration_execution_successful")),
        "no_protected_branch_push": ([False, False], [review.get("integration_branch_pushed"), review.get("main_push_performed")]),
        "no_provider_or_runtime_actions": ([False, NOT_AUTHORIZED], [review.get("provider_requests_made_in_review"), review.get("runtime_use")]),
    }
    return [_observation(observation_id, *values[observation_id]) for observation_id in OBSERVATION_IDS]


def _base_review(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN,
        "created_offline_except_read_only_file_verification": True, "governance_only": True,
        "results_review_only": True, **deepcopy(dict(source_fields)),
        "module_level_grouping_reviewed": True,
        "module_level_grouping_review": {
            "source_digest": SOURCE_MODULE_GROUPING_DIGEST, "failed_or_errored_nodeids": 1404,
            "module_count": 29, "deterministic_ordering": ["descending count", "ascending module path"],
            "sample_nodeids_bounded_per_module": 5, "review_status": "REVIEWED_MODULE_LEVEL_GROUPING_ONLY",
        },
        "module_summary_reviewed": True,
        "module_summary_review": {"module_count": 29, "total_nodeids": 1404,
                                  "largest_module_nodeid_counts": [136, 131, 122, 112, 111]},
        "largest_module_summary_reviewed": True,
        "failure_error_separation_exclusion_reviewed": True,
        "first_order_exclusion_reviewed": True, "traceback_root_cause_exclusion_reviewed": True,
        "retry_success_exclusion_reviewed": True, "main_merge_readiness_exclusion_reviewed": True,
        "limitations_reviewed": True,
        "limitations_review": {
            "module_grouping_supported": True, "failure_error_separation_supported": False,
            "first_order_supported": False, "traceback_root_cause_supported": False,
            "retry_success_supported": False,
        },
        "unsupported_claims_exclusion_reviewed": True,
        "unsupported_claims_exclusion_review": {
            "failure_error_separation_excluded": True, "first_failure_excluded": True,
            "first_error_excluded": True, "first_order_claim_excluded": True,
            "traceback_root_cause_excluded": True, "retry_success_excluded": True,
            "main_merge_readiness_excluded": True,
        },
        "planned_outputs_reviewed": True, "planned_outputs_review": deepcopy(PLANNED_OUTPUTS_REVIEW),
        "classification_method_results_review_v2_created": True,
        "classification_method_results_review_v2_ready": True,
        "ready_for_remediation_or_method_candidate_after_v2_review": True,
        "remediation_or_method_candidate_after_v2_review_created": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "integration_results_review_created": False,
        "main_merge_approval_created": False, "retry_rerun_performed": False,
        "full_pytest_performed": False, "diagnostic_command_executed": False,
        "diagnostic_output_captured": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "pytest_cache_committed": False, "evidence_regenerated": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED, "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected),
            "actual": deepcopy(actual), "severity": BLOCKER,
            "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "source_execution_digest_bound": (SOURCE_EXECUTION_V2_DIGEST, review.get("source_classification_method_execution_v2_digest")),
        "source_module_grouping_digest_bound": (SOURCE_MODULE_GROUPING_DIGEST, review.get("source_classification_method_v2_module_grouping_digest")),
        "source_digest_manifest_bound": (SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_classification_method_v2_digest_manifest_digest")),
        "source_approval_digest_bound": (source.SOURCE_APPROVAL_V2_DIGEST, review.get("source_classification_method_approval_v2_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [review.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "module_grouping_reviewed_true": (True, review.get("module_level_grouping_reviewed")),
        "module_summary_reviewed_true": (True, review.get("module_summary_reviewed")),
        "module_count_29": (29, review.get("module_summary_module_count")),
        "largest_module_counts_reviewed": ([136, 131, 122, 112, 111], review.get("largest_module_nodeid_counts")),
        "failed_or_errored_nodeids_1404": (1404, review.get("failed_or_errored_nodeids_count")),
        "limitations_reviewed_true": (True, review.get("limitations_reviewed")),
        "unsupported_claims_exclusion_reviewed_true": (True, review.get("unsupported_claims_exclusion_reviewed")),
        "failure_modules_classified_false": (False, review.get("failure_modules_classified")),
        "error_modules_classified_false": (False, review.get("error_modules_classified")),
        "failure_error_separation_claimed_false": (False, review.get("failure_error_separation_claimed")),
        "first_failure_identified_false": (False, review.get("first_failure_identified")),
        "first_error_identified_false": (False, review.get("first_error_identified")),
        "first_order_claim_made_false": (False, review.get("first_order_claim_made")),
        "traceback_root_cause_claimed_false": (False, review.get("traceback_root_cause_claimed")),
        "retry_success_claimed_false": (False, review.get("retry_success_claimed")),
        "main_merge_readiness_claimed_false": (False, review.get("main_merge_readiness_claimed")),
        "planned_outputs_reviewed_true": (True, review.get("planned_outputs_reviewed")),
        "results_review_created_true": (True, review.get("classification_method_results_review_v2_created")),
        "results_review_ready_true": (True, review.get("classification_method_results_review_v2_ready")),
        "ready_for_remediation_or_method_candidate_after_v2_review_true": (True, review.get("ready_for_remediation_or_method_candidate_after_v2_review")),
        "remediation_or_method_candidate_created_false": (False, review.get("remediation_or_method_candidate_after_v2_review_created")),
        "new_retry_candidate_created_false": (False, review.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, review.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, review.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, review.get("main_merge_approval_created")),
        "retry_rerun_false": (False, review.get("retry_rerun_performed")),
        "full_pytest_false": (False, review.get("full_pytest_performed")),
        "diagnostic_command_false": (False, review.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, review.get("diagnostic_output_captured")),
        "integration_success_false": (False, review.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, review.get("integration_branch_pushed")),
        "main_push_false": (False, review.get("main_push_performed")),
        "origin_main_modified_false": (False, review.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, review.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, review.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, review.get("evidence_regenerated")),
        "provider_requests_false": (False, review.get("provider_requests_made_in_review")),
        "market_data_acquisition_false": (False, review.get("market_data_acquisition_performed_in_review")),
        "dataset_generation_false": (False, review.get("dataset_generation_performed_in_review")),
        "metric_recomputation_false": (False, review.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, review.get("model_training_performed")),
        "strategy_scoring_false": (False, review.get("strategy_scoring_performed")),
        "recommendations_false": (False, review.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": ([False, False], [review.get("marketflow_outputs_tracked_in_repository"), review.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "no_tracked_pytest_cache_files": ([False, False], [review.get("pytest_cache_tracked_in_repository"), review.get("pytest_cache_tracked_in_detached_worktree")]),
    }
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "classification_method_results_review_v2_created": True,
        "classification_method_results_review_v2_ready": True,
        "module_level_grouping_reviewed": True, "module_summary_reviewed": True,
        "limitations_reviewed": True, "unsupported_claims_exclusion_reviewed": True,
        "ready_for_remediation_or_method_candidate_after_v2_review": True,
        "remediation_or_method_candidate_after_v2_review_created": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "integration_execution_successful": False, "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    for field in ("review_observations", "checklist", "summary",
                  "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
    *, source_execution: dict | None = None,
) -> dict:
    """Build a deterministic review from committed or validated execution evidence."""
    review = _base_review(_source_fields(source_execution))
    manifest = {
        "source_execution_v2_digest": SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": SOURCE_MODULE_GROUPING_DIGEST,
        "source_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "limitations_reviewed": True, "unsupported_claims_exclusion_reviewed": True,
    }
    review["review_manifest"] = manifest
    review["marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest"] = semantic_digest(manifest)
    review["review_observations"] = _observations(review)
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review["marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"] = (
        marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest_v1(review)
    )
    validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
    review: dict,
) -> dict:
    """Validate source bindings, reviewed results, and all closed boundaries."""
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2,
        "review_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN,
        **_committed_source_fields(), "planned_outputs_review": PLANNED_OUTPUTS_REVIEW,
        "module_level_grouping_review": {
            "source_digest": SOURCE_MODULE_GROUPING_DIGEST,
            "failed_or_errored_nodeids": 1404,
            "module_count": 29,
            "deterministic_ordering": ["descending count", "ascending module path"],
            "sample_nodeids_bounded_per_module": 5,
            "review_status": "REVIEWED_MODULE_LEVEL_GROUPING_ONLY",
        },
        "module_summary_review": {
            "module_count": 29,
            "total_nodeids": 1404,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        },
        "limitations_review": {
            "module_grouping_supported": True,
            "failure_error_separation_supported": False,
            "first_order_supported": False,
            "traceback_root_cause_supported": False,
            "retry_success_supported": False,
        },
        "unsupported_claims_exclusion_review": {
            "failure_error_separation_excluded": True,
            "first_failure_excluded": True,
            "first_error_excluded": True,
            "first_order_claim_excluded": True,
            "traceback_root_cause_excluded": True,
            "retry_success_excluded": True,
            "main_merge_readiness_excluded": True,
        },
        "review_manifest": {
            "source_execution_v2_digest": SOURCE_EXECUTION_V2_DIGEST,
            "source_module_grouping_digest": SOURCE_MODULE_GROUPING_DIGEST,
            "source_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
            "module_count": 29,
            "failed_or_errored_nodeids_count": 1404,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
            "limitations_reviewed": True,
            "unsupported_claims_exclusion_reviewed": True,
        },
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(review.get(field), expected, field)
    required_true = (
        "created_offline_except_read_only_file_verification", "governance_only", "results_review_only",
        "module_level_grouping_reviewed", "module_summary_reviewed", "largest_module_summary_reviewed",
        "failure_error_separation_exclusion_reviewed", "first_order_exclusion_reviewed",
        "traceback_root_cause_exclusion_reviewed", "retry_success_exclusion_reviewed",
        "main_merge_readiness_exclusion_reviewed", "limitations_reviewed",
        "unsupported_claims_exclusion_reviewed", "planned_outputs_reviewed",
        "classification_method_results_review_v2_created", "classification_method_results_review_v2_ready",
        "ready_for_remediation_or_method_candidate_after_v2_review",
    )
    required_false = (
        "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
        "first_failure_identified", "first_error_identified", "first_order_claim_made",
        "traceback_root_cause_claimed", "retry_success_claimed", "main_merge_readiness_claimed",
        "root_cause_family_hints_generated", "remediation_or_method_candidate_after_v2_review_created",
        "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
        "integration_results_review_created", "main_merge_approval_created", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed",
        "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
        "pytest_cache_committed", "evidence_regenerated", "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_accepted", "profitability_accepted",
        "marketflow_outputs_tracked_in_repository", "marketflow_outputs_tracked_in_detached_worktree",
        "pytest_cache_tracked_in_repository", "pytest_cache_tracked_in_detached_worktree",
    )
    for field in required_true:
        _expect(review.get(field), True, field)
    for field in required_false:
        _expect(review.get(field), False, field)
    if not isinstance(review.get("module_level_grouping_review"), dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "module grouping review missing"
        )
    if not isinstance(review.get("module_summary_review"), dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "module summary review missing"
        )
    if not isinstance(review.get("limitations_review"), dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "limitations review missing"
        )
    if not isinstance(review.get("unsupported_claims_exclusion_review"), dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "unsupported claims review missing"
        )
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    observations = review.get("review_observations")
    if not isinstance(observations, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review_observations missing"
        )
    _expect([row.get("observation_id") for row in observations], OBSERVATION_IDS, "observation ids")
    _expect(observations, _observations(review), "review observations")
    if any(row.get("status") != PASS for row in observations):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review observation failed"
        )
    checklist = review.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(review), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "checklist failed"
        )
    _expect(review.get("summary"), _summary(review, checklist), "summary")
    manifest = review.get("review_manifest")
    if not isinstance(manifest, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review_manifest missing"
        )
    manifest_digest = review.get("marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest")
    if not isinstance(manifest_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", manifest_digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review manifest digest missing"
        )
    _expect(manifest_digest, semantic_digest(manifest), "review manifest digest")
    digest = review.get("marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "review digest missing"
        )
    _expect(digest, marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest_v1(review), "review digest")
    return {
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest": digest,
        "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest": manifest_digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(review)
    sections = [
        ("Source Execution v2", [f"Execution digest: `{SOURCE_EXECUTION_V2_DIGEST}`.", f"Module-grouping digest: `{SOURCE_MODULE_GROUPING_DIGEST}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "The root regression is not retry evidence."]),
        ("Module-Level Grouping Review", ["All 1,404 reviewed node IDs are grouped into 29 modules with deterministic ordering and bounded samples."]),
        ("Module Summary Review", ["Largest module counts: `136, 131, 122, 112, 111`."]),
        ("Limitations Review", ["The reviewed cache supports module/node grouping only."]),
        ("Unsupported Claims Exclusion", ["Failure/error separation, first order, traceback root cause, retry success, and main-merge readiness remain excluded."]),
        ("Authority Boundaries", ["No classification execution, remediation candidate, retry, protected-branch action, provider/data action, runtime, or trading authority is created."]),
        ("Next Chain", review["next_chain"]), ("Next Gates", [f"`{row}`" for row in review["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in review["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Execution v2 remains immutable source evidence.", "A separate remediation or method candidate is required before any further action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Classification Method Results Review v2", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
        source_execution=source_execution
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2.json"
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodResultsReviewV2Error(
            "results review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"], "review_scope": review["review_scope"],
        "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"
        ],
        "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
