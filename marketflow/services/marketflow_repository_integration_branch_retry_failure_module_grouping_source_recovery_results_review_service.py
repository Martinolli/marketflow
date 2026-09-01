"""Review recovered module-grouping detail without reading cache or re-executing recovery."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1 = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1"
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1 = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE"
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1"
SOURCE_EXECUTION_DIGEST = "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a"
SOURCE_RECOVERY_DETAIL_DIGEST = "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"
SOURCE_DIGEST_MANIFEST_DIGEST = "940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

TOP_FIVE = [
    {"module_path": "tests/test_marketflow_signal_or_feature_generation_results_review_service.py", "failed_or_errored_nodeid_count": 136},
    {"module_path": "tests/test_post_identity_freeze_registry_inventory_approval_service.py", "failed_or_errored_nodeid_count": 131},
    {"module_path": "tests/test_corporate_action_authority_plan_candidate_service.py", "failed_or_errored_nodeid_count": 122},
    {"module_path": "tests/test_feature_generation_results_review_redesigned_labels_service.py", "failed_or_errored_nodeid_count": 112},
    {"module_path": "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", "failed_or_errored_nodeid_count": 111},
]
LIMITATIONS = [
    "cache source does not distinguish assertion failures from errors",
    "cache source does not preserve first-failure order",
    "cache source does not provide tracebacks",
    "recovered module grouping is planning source only",
    "recovered detail does not prove root cause",
    "recovered detail does not authorize retry or main merge",
]
UNSUPPORTED_CLAIMS = deepcopy(source.UNSUPPORTED_CLAIMS)
SUCCESS_NEXT_CHAIN = [
    "After-v2 Planning Reentry Using Recovered Module Grouping Source v1.",
    "Remediation or Method Execution After Classification v2 Review Reentry, if separately approved or authorized by reentry.",
    "Remediation or Method Results Review After Classification v2 Review v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Module Grouping Source Recovery Results Review Failure Diagnosis v1.",
    "Recovery remediation candidate, if needed.", "No planning re-entry, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "after_v2_planning_reentry_using_recovered_module_grouping_source",
    "remediation_or_method_execution_after_classification_v2_review_reentry_if_authorized",
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "module_grouping_source_recovery_results_review_failure_diagnosis",
    "source_recovery_results_review_remediation_candidate_if_needed",
    "planning_reentry_blocked_until_source_recovery_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "results_review_does_not_recover_module_grouping_again", "results_review_does_not_read_cache",
    "results_review_does_not_modify_cache", "results_review_does_not_commit_pytest_cache",
    "results_review_does_not_commit_marketflow_outputs", "results_review_does_not_parse_operator_logs",
    "results_review_does_not_run_diagnostic_commands", "results_review_does_not_execute_diagnostics",
    "results_review_does_not_execute_remediation", "results_review_does_not_execute_classification",
    "results_review_does_not_classify_modules_again", "results_review_does_not_rerun_retry",
    "results_review_does_not_run_full_pytest", "results_review_does_not_create_planning_reentry",
    "results_review_does_not_create_new_retry_candidate", "results_review_does_not_create_retry_results_review",
    "results_review_does_not_create_integration_results_review", "results_review_does_not_mark_integration_successful",
    "results_review_does_not_generate_successful_integration_digest", "results_review_does_not_claim_failure_error_separation",
    "results_review_does_not_claim_first_failure", "results_review_does_not_claim_first_error",
    "results_review_does_not_claim_traceback_root_cause", "results_review_does_not_recommend_direct_code_remediation",
    "results_review_does_not_treat_cache_or_classification_as_retry_success", "results_review_does_not_push_integration_branch",
    "results_review_does_not_push_main", "results_review_does_not_delete_integration_branch",
    "results_review_does_not_delete_worktree", "results_review_does_not_force_push",
    "results_review_does_not_prune_remotes", "results_review_does_not_modify_tags",
    "results_review_does_not_modify_staged_evidence", "results_review_does_not_regenerate_evidence",
    "results_review_does_not_call_providers", "results_review_does_not_acquire_market_data",
    "results_review_does_not_regenerate_dataset", "results_review_does_not_recompute_metrics",
    "results_review_does_not_train_models", "results_review_does_not_score_strategy",
    "results_review_does_not_generate_recommendations", "results_review_does_not_accept_predictive_usefulness",
    "results_review_does_not_accept_profitability", "results_review_does_not_authorize_runtime",
    "results_review_does_not_authorize_broker_execution", "source_recovery_output_is_planning_source_not_root_cause",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_after_v2_planning_reentry_required", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]
COMMON_CHECK_IDS = [
    "source_execution_digest_bound", "source_recovery_detail_digest_bound", "source_digest_manifest_bound",
    "source_approval_digest_bound", "source_operator_review_digest_bound", "source_candidate_digest_bound",
    "source_blocked_execution_digest_bound", "source_blocked_manifest_digest_bound", "source_blocked_reason_bound",
    "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound", "source_module_grouping_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "cache_hash_verification_reviewed",
    "cache_count_verification_reviewed", "lastfailed_subset_of_nodeids_reviewed",
    "module_grouping_detail_reviewed_true", "module_paths_reviewed_true", "per_module_counts_reviewed_true",
    "bounded_nodeid_samples_reviewed_true", "failed_or_errored_nodeids_1404", "module_count_29",
    "largest_module_counts_reviewed", "top_five_module_paths_reviewed", "top_five_count_sum_612",
    "top_five_percentage_reviewed", "top_ten_count_sum_1069", "top_ten_percentage_reviewed",
    "planned_outputs_reviewed_true", "limitations_reviewed_true", "unsupported_claims_boundary_reviewed_true",
    "failure_modules_classified_false", "error_modules_classified_false", "failure_error_separation_claimed_false",
    "first_failure_identified_false", "first_error_identified_false", "first_order_claim_made_false",
    "traceback_root_cause_claimed_false", "direct_code_remediation_recommended_false", "retry_success_claimed_false",
    "main_merge_readiness_claimed_false", "results_review_created_true", "results_review_ready_true",
    "ready_for_after_v2_planning_reentry_after_source_recovery_review_true", "after_v2_planning_reentry_created_false",
    "remediation_or_method_reentry_created_false", "new_retry_candidate_created_false", "new_retry_executed_false",
    "new_retry_results_review_created_false", "main_merge_approval_created_false", "retry_rerun_false",
    "full_pytest_false", "diagnostic_command_false", "diagnostic_output_false", "cache_read_in_review_false",
    "integration_success_false", "successful_integration_digest_false", "integration_branch_pushed_false",
    "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "pytest_cache_committed_false", "evidence_regenerated_false", "provider_requests_false",
    "market_data_acquisition_false", "dataset_generation_false", "metric_recomputation_false",
    "model_training_false", "strategy_scoring_false", "recommendations_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError(ValueError):
    pass


def _committed_source() -> dict[str, Any]:
    base = source._source_fields()
    cache = {
        "lastfailed_cache_path": str(source.DEFAULT_WORKTREE / ".pytest_cache/v/cache/lastfailed"),
        "lastfailed_cache_read": True, "lastfailed_cache_parseable_json": True,
        "lastfailed_cache_sha256_expected": source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_sha256_actual": source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count_expected": 1404, "lastfailed_cache_entry_count_actual": 1404,
        "nodeids_cache_path": str(source.DEFAULT_WORKTREE / ".pytest_cache/v/cache/nodeids"),
        "nodeids_cache_read": True, "nodeids_cache_parseable_json": True,
        "nodeids_cache_sha256_expected": source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_sha256_actual": source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count_expected": 26288, "nodeids_cache_entry_count_actual": 26288,
        "lastfailed_nodeids_subset_of_nodeids": True,
    }
    return {
        "artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1,
        "execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE,
        "execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN,
        "selected_module_grouping_source_recovery_package": source.SELECTED_PACKAGE,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest": SOURCE_EXECUTION_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        **base,
        "blocked_reason_before_recovery": base["blocked_reason_before_recovery"],
        "cache_hash_and_count_verification_report": cache,
        "module_grouping_source_recovery_executed": True, "module_grouping_detail_recovered": True,
        "module_grouping_detail_exposed": True, "module_paths_recovered": True,
        "per_module_counts_recovered": True, "bounded_nodeid_samples_recovered": True,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_module_source_detail_report": {
            "top_5_module_paths": [item["module_path"] for item in TOP_FIVE],
            "top_5_counts": [item["failed_or_errored_nodeid_count"] for item in TOP_FIVE],
            "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
            "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        },
        "recovered_module_grouping_detail_report": {"present": True, "digest": SOURCE_RECOVERY_DETAIL_DIGEST},
        "recovered_module_counts_by_path_report": {"module_count": 29, "total_failed_or_errored_nodeids": 1404},
        "recovered_bounded_nodeid_samples_report": {"present": True, "sample_limit": 5},
        "source_recovery_limitations_report": list(LIMITATIONS),
        "planned_outputs_generated": True,
        "planned_outputs": [{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in source.OUTPUT_IDS],
        **deepcopy(UNSUPPORTED_CLAIMS),
        "diagnostic_method_executed": False,
        "code_remediation_executed": False,
        "evidence_remediation_executed": False,
        "classification_execution_performed": False,
    }


def _source_checks(execution: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    expected = {
        "artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1,
        "execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE,
        "execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_digest": SOURCE_EXECUTION_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.SOURCE_APPROVAL_DIGEST,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "module_grouping_detail_recovered": True, "module_paths_recovered": True,
        "per_module_counts_recovered": True, "bounded_nodeid_samples_recovered": True,
        "diagnostic_method_executed": False, "code_remediation_executed": False,
        "evidence_remediation_executed": False, "classification_execution_performed": False,
    }
    for field, value in expected.items():
        if execution.get(field) != value:
            reasons.append(f"{field.upper()}_MISMATCH_OR_MISSING")
    cache = execution.get("cache_hash_and_count_verification_report")
    if not isinstance(cache, Mapping): reasons.append("CACHE_VERIFICATION_MISSING")
    else:
        if cache.get("lastfailed_cache_sha256_actual") != source.EXPECTED_LASTFAILED_SHA256 or cache.get("nodeids_cache_sha256_actual") != source.EXPECTED_NODEIDS_SHA256: reasons.append("CACHE_HASH_VERIFICATION_MISMATCH")
        if cache.get("lastfailed_cache_entry_count_actual") != 1404 or cache.get("nodeids_cache_entry_count_actual") != 26288: reasons.append("CACHE_COUNT_VERIFICATION_MISMATCH")
        if cache.get("lastfailed_nodeids_subset_of_nodeids") is not True: reasons.append("LASTFAILED_SUBSET_VERIFICATION_MISSING")
    top = execution.get("top_module_source_detail_report")
    if not isinstance(top, Mapping): reasons.append("TOP_MODULE_DETAIL_MISSING")
    else:
        if top.get("top_5_module_paths") != [item["module_path"] for item in TOP_FIVE]: reasons.append("TOP_FIVE_MODULE_PATHS_MISMATCH")
        if top.get("top_5_count_sum") != 612 or top.get("top_10_count_sum") != 1069: reasons.append("TOP_MODULE_CONCENTRATION_MISMATCH")
    if not execution.get("recovered_module_grouping_detail_report"): reasons.append("RECOVERED_MODULE_DETAIL_MISSING")
    if not execution.get("recovered_bounded_nodeid_samples_report"): reasons.append("BOUNDED_NODEID_SAMPLES_MISSING")
    if execution.get("source_recovery_limitations_report") != LIMITATIONS: reasons.append("LIMITATIONS_MISSING_OR_CHANGED")
    if {key: execution.get(key) for key in UNSUPPORTED_CLAIMS} != UNSUPPORTED_CLAIMS: reasons.append("UNSUPPORTED_CLAIMS_BOUNDARY_VIOLATED")
    return reasons


def _common() -> dict[str, Any]:
    source_fields = source._source_fields()
    return {
        "schema_version": SCHEMA_VERSION,
        "review_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN,
        "created_offline_except_read_only_file_verification": True, "governance_only": True, "results_review_only": True,
        "source_module_grouping_source_recovery_execution_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1,
        "source_module_grouping_source_recovery_execution_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE,
        "source_module_grouping_source_recovery_execution_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN,
        "source_module_grouping_source_recovery_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        **deepcopy(source_fields),
        "selected_module_grouping_source_recovery_package": source.SELECTED_PACKAGE,
        "retry_pytest_working_directory": str(source.DEFAULT_WORKTREE),
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False, "detached_integration_worktree_path": str(source.DEFAULT_WORKTREE),
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True, "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False, "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "module_grouping_source_recovery_results_review_created": True,
        "after_v2_planning_reentry_created": False, "remediation_or_method_after_v2_reentry_created": False,
        "new_retry_candidate_created": False, "new_retry_executed": False,
        "new_retry_results_review_created": False, "main_merge_approval_created": False,
        "retry_rerun_performed": False, "full_pytest_performed": False,
        "diagnostic_command_executed": False, "diagnostic_output_captured": False,
        "cache_read_in_review": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False,
        "origin_main_modified_by_this_task": False, "marketflow_outputs_committed": False,
        "pytest_cache_committed": False, "evidence_regenerated": False,
        "provider_requests_made_in_review": False, "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False, "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False,
        "trade_recommendations_generated": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "diagnostic_method_executed": False, "code_remediation_executed": False,
        "evidence_remediation_executed": False, "classification_execution_performed": False,
        **deepcopy(UNSUPPORTED_CLAIMS), "risk_controls": list(RISK_CONTROLS),
    }


def _observation(observation_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"observation_id": observation_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "message": f"{observation_id} {'passed' if status == PASS else 'failed'}"}


def _observations(review: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    values = {
        "source_execution_digest_bound": (SOURCE_EXECUTION_DIGEST, review.get("source_module_grouping_source_recovery_execution_digest")),
        "recovery_detail_digest_bound": (SOURCE_RECOVERY_DETAIL_DIGEST, review.get("source_module_grouping_source_recovery_detail_digest")),
        "digest_manifest_bound": (SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_approval_digest_bound": (source.SOURCE_APPROVAL_DIGEST, review.get("source_module_grouping_source_recovery_approval_digest")),
        "retry_failure_counts_bound": ([24877,1292,112,7],[review.get(f"retry_pytest_{n}_count") for n in ("passed","failed","error","skipped")]),
        "cache_hash_and_count_verification_reviewed": (success, review.get("cache_hash_and_count_verification_reviewed")),
        "lastfailed_subset_of_nodeids_reviewed": (success, review.get("lastfailed_subset_of_nodeids_reviewed")),
        "module_grouping_detail_reviewed": (success, review.get("module_grouping_detail_reviewed")),
        "module_paths_reviewed": (success, review.get("module_paths_reviewed")),
        "per_module_counts_reviewed": (success, review.get("per_module_counts_reviewed")),
        "bounded_nodeid_samples_reviewed": (success, review.get("bounded_nodeid_samples_reviewed")),
        "module_count_29_reviewed": (success, review.get("module_summary_module_count") == 29),
        "largest_module_counts_reviewed": (success, review.get("largest_module_nodeid_counts") == [136,131,122,112,111]),
        "top_five_module_paths_reviewed": (success, review.get("top_module_source_detail_reviewed")),
        "top_five_concentration_reviewed": (success, review.get("top_5_count_sum") == 612),
        "top_ten_concentration_reviewed": (success, review.get("top_10_count_sum") == 1069),
        "planned_outputs_reviewed": (success, review.get("planned_outputs_reviewed")),
        "limitations_reviewed": (success, review.get("source_recovery_limitations_reviewed")),
        "unsupported_claims_boundary_reviewed": (True, review.get("unsupported_claims_boundary_reviewed")),
        "failed_retry_preserved": (True, review.get("retry_pytest_first_result_authoritative")),
        "root_regression_not_retry_evidence": (False, review.get("root_full_regression_is_retry_evidence")),
        "ready_for_after_v2_planning_reentry_after_source_recovery_review": (success, review.get("ready_for_after_v2_planning_reentry_after_source_recovery_review")),
        "no_cache_read_in_review": (False, review.get("cache_read_in_review")),
        "no_retry_rerun": (False, review.get("retry_rerun_performed")), "no_full_pytest": (False, review.get("full_pytest_performed")),
        "no_diagnostic_command": (False, review.get("diagnostic_command_executed")),
        "no_planning_reentry_created": (False, review.get("after_v2_planning_reentry_created")),
        "no_new_retry_candidate": (False, review.get("new_retry_candidate_created")),
        "no_integration_success": (False, review.get("integration_execution_successful")),
        "no_protected_branch_push": ([False,False],[review.get("integration_branch_pushed"),review.get("main_push_performed")]),
        "no_provider_or_runtime_actions": ([False,NOT_AUTHORIZED],[review.get("provider_requests_made_in_review"),review.get("runtime_use")]),
    }
    return [_observation(key,*value) for key,value in values.items()]


def _review_manifest(review: Mapping[str, Any]) -> str:
    return semantic_digest({
        "source_execution_digest": review["source_module_grouping_source_recovery_execution_digest"],
        "source_detail_digest": review["source_module_grouping_source_recovery_detail_digest"],
        "source_digest_manifest": review["source_module_grouping_source_recovery_digest_manifest_digest"],
        "cache_review": review.get("cache_hash_and_count_verification_review"),
        "top_module_review": review.get("top_module_source_detail_review"),
        "limitations": review.get("source_recovery_limitations_review"),
        "unsupported_claims": {key: review.get(key) for key in UNSUPPORTED_CLAIMS},
    })


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def _finish(review: dict[str, Any], success: bool) -> dict[str, Any]:
    review["next_chain"] = list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN)
    review["next_gates"] = list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES)
    review["review_observations"] = _observations(review, success)
    if success:
        review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest"] = _review_manifest(review)
    else:
        review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest"] = semantic_digest({"blocked_reason":review["blocked_reason"],"source_execution_digest":review["source_module_grouping_source_recovery_execution_digest"]})
    review["checklist"] = _checklist(review, success)
    failed = [item for item in review["checklist"] if item["status"] != PASS]
    review["summary"] = {
        "total_checks": len(review["checklist"]), "passed_checks": len(review["checklist"])-len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "module_grouping_source_recovery_results_review_created": True,
        "module_grouping_source_recovery_results_review_ready": success,
        "ready_for_after_v2_planning_reentry_after_source_recovery_review": success,
        "after_v2_planning_reentry_created": False, "new_retry_candidate_created": False,
        "integration_execution_successful": False,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        review["summary"].update(
            module_grouping_source_recovery_execution_reviewed=True, module_grouping_detail_reviewed=True,
            module_paths_reviewed=True, per_module_counts_reviewed=True, bounded_nodeid_samples_reviewed=True,
            failed_or_errored_nodeids_count=1404, module_summary_module_count=29,
            top_5_count_sum=612, top_5_percentage_of_failed_or_errored_nodeids="43.58974359",
            top_10_count_sum=1069, top_10_percentage_of_failed_or_errored_nodeids="76.13960114",
            new_retry_executed=False,
        )
    else: review["summary"]["blocked_reason"] = review["blocked_reason"]
    review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"] = _review_digest(review)
    return review


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status=PASS if expected==actual else FAIL
    return {"check_id":check_id,"status":status,"expected":deepcopy(expected),"actual":deepcopy(actual),"severity":BLOCKER,"message":f"{check_id} {'passed' if status==PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    expected_success = success
    cache = review.get("cache_hash_and_count_verification_review", {})
    values: dict[str, tuple[Any, Any]] = {
        "source_execution_digest_bound":(SOURCE_EXECUTION_DIGEST,review.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound":(SOURCE_RECOVERY_DETAIL_DIGEST,review.get("source_module_grouping_source_recovery_detail_digest")),
        "source_digest_manifest_bound":(SOURCE_DIGEST_MANIFEST_DIGEST,review.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_approval_digest_bound":(source.SOURCE_APPROVAL_DIGEST,review.get("source_module_grouping_source_recovery_approval_digest")),
        "source_operator_review_digest_bound":(source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,review.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_candidate_digest_bound":(source.approval_source.source.SOURCE_CANDIDATE_DIGEST,review.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_execution_digest_bound":(source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,review.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_manifest_digest_bound":(source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,review.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound":(source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,review.get("blocked_reason_before_recovery")),
        "source_results_review_v2_digest_bound":(source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,review.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound":(source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,review.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound":(source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,review.get("source_module_grouping_digest")),
        "retry_execution_commit_bound":("ab178b65c69f0274b0abbf9c20df102d35e78d34",review.get("retry_execution_commit")),
        "retry_failure_counts_bound":([24877,1292,112,7],[review.get(f"retry_pytest_{n}_count") for n in ("passed","failed","error","skipped")]),
        "cache_hash_verification_reviewed":(expected_success,success and cache.get("lastfailed_cache_sha256_verified") and cache.get("nodeids_cache_sha256_verified")),
        "cache_count_verification_reviewed":(expected_success,success and cache.get("lastfailed_cache_count_verified") and cache.get("nodeids_cache_count_verified")),
        "lastfailed_subset_of_nodeids_reviewed":(expected_success,review.get("lastfailed_subset_of_nodeids_reviewed")),
        "module_grouping_detail_reviewed_true":(success,review.get("module_grouping_detail_reviewed")),
        "module_paths_reviewed_true":(success,review.get("module_paths_reviewed")),
        "per_module_counts_reviewed_true":(success,review.get("per_module_counts_reviewed")),
        "bounded_nodeid_samples_reviewed_true":(success,review.get("bounded_nodeid_samples_reviewed")),
        "failed_or_errored_nodeids_1404":(1404 if success else 0,review.get("failed_or_errored_nodeids_count",0)),
        "module_count_29":(29 if success else 0,review.get("module_summary_module_count",0)),
        "largest_module_counts_reviewed":([136,131,122,112,111] if success else [],review.get("largest_module_nodeid_counts",[])),
        "top_five_module_paths_reviewed":(success,review.get("top_module_source_detail_reviewed")),
        "top_five_count_sum_612":(612 if success else 0,review.get("top_5_count_sum",0)),
        "top_five_percentage_reviewed":("43.58974359" if success else None,review.get("top_5_percentage_of_failed_or_errored_nodeids")),
        "top_ten_count_sum_1069":(1069 if success else 0,review.get("top_10_count_sum",0)),
        "top_ten_percentage_reviewed":("76.13960114" if success else None,review.get("top_10_percentage_of_failed_or_errored_nodeids")),
        "planned_outputs_reviewed_true":(success,review.get("planned_outputs_reviewed")),
        "limitations_reviewed_true":(success,review.get("source_recovery_limitations_reviewed")),
        "unsupported_claims_boundary_reviewed_true":(True,review.get("unsupported_claims_boundary_reviewed")),
        "results_review_created_true":(True,review.get("module_grouping_source_recovery_results_review_created")),
        "results_review_ready_true":(success,review.get("module_grouping_source_recovery_results_review_ready")),
        "ready_for_after_v2_planning_reentry_after_source_recovery_review_true":(success,review.get("ready_for_after_v2_planning_reentry_after_source_recovery_review")),
        "next_chain_defined":(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN,review.get("next_chain")),
        "next_gates_defined":(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES,review.get("next_gates")),
        "risk_controls_defined":(RISK_CONTROLS,review.get("risk_controls")),
        "no_tracked_marketflow_files":(False,review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files":(False,review.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted":(NOT_ACCEPTED,review.get("predictive_usefulness")),
        "profitability_not_accepted":(NOT_ACCEPTED,review.get("profitability")),
        "runtime_not_authorized":(NOT_AUTHORIZED,review.get("runtime_use")),
        "broker_not_authorized":(NOT_AUTHORIZED,review.get("broker_execution")),
    }
    false_map={
        "failure_modules_classified_false":"failure_modules_classified","error_modules_classified_false":"error_modules_classified",
        "failure_error_separation_claimed_false":"failure_error_separation_claimed","first_failure_identified_false":"first_failure_identified",
        "first_error_identified_false":"first_error_identified","first_order_claim_made_false":"first_order_claim_made",
        "traceback_root_cause_claimed_false":"traceback_root_cause_claimed","direct_code_remediation_recommended_false":"direct_code_remediation_recommended",
        "retry_success_claimed_false":"retry_success_claimed","main_merge_readiness_claimed_false":"main_merge_readiness_claimed",
        "after_v2_planning_reentry_created_false":"after_v2_planning_reentry_created","remediation_or_method_reentry_created_false":"remediation_or_method_after_v2_reentry_created",
        "new_retry_candidate_created_false":"new_retry_candidate_created","new_retry_executed_false":"new_retry_executed",
        "new_retry_results_review_created_false":"new_retry_results_review_created","main_merge_approval_created_false":"main_merge_approval_created",
        "retry_rerun_false":"retry_rerun_performed","full_pytest_false":"full_pytest_performed",
        "diagnostic_command_false":"diagnostic_command_executed","diagnostic_output_false":"diagnostic_output_captured",
        "cache_read_in_review_false":"cache_read_in_review","integration_success_false":"integration_execution_successful",
        "integration_branch_pushed_false":"integration_branch_pushed","main_push_false":"main_push_performed",
        "origin_main_modified_false":"origin_main_modified_by_this_task","marketflow_outputs_committed_false":"marketflow_outputs_committed",
        "pytest_cache_committed_false":"pytest_cache_committed","evidence_regenerated_false":"evidence_regenerated",
        "provider_requests_false":"provider_requests_made_in_review","market_data_acquisition_false":"market_data_acquisition_performed_in_review",
        "dataset_generation_false":"dataset_generation_performed_in_review","metric_recomputation_false":"metric_recomputation_from_raw_rows_performed",
        "model_training_false":"model_training_performed","strategy_scoring_false":"strategy_scoring_performed",
        "recommendations_false":"trade_recommendations_generated",
    }
    values.update({check_id:(False,review.get(field)) for check_id,field in false_map.items()})
    values["successful_integration_digest_false"]=([False,False],[review.get("successful_integration_execution_digest_generated"),review.get("successful_integration_validation_digest_generated")])
    extra = {
        "blocked_reason_recorded":(True,bool(review.get("blocked_reason"))),
        "blocked_manifest_digest_generated":(True,bool(review.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest"))),
        "planning_reentry_ready_false":(False,review.get("ready_for_after_v2_planning_reentry_after_source_recovery_review")),
        "failure_diagnosis_defined":(BLOCKED_NEXT_TASK,review.get("recommended_next_task")),
    } if not success else {}
    values.update(extra)
    return [_check(check_id,*values[check_id]) for check_id in COMMON_CHECK_IDS+list(extra)]


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(*, source_execution: dict | None = None) -> dict:
    execution = deepcopy(source_execution) if source_execution is not None else _committed_source()
    reasons = _source_checks(execution)
    success = not reasons
    review = _common()
    if success:
        cache=execution["cache_hash_and_count_verification_report"]; top=execution["top_module_source_detail_report"]
        review.update(
            artifact_kind=ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1,
            review_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY,
            module_grouping_source_recovery_results_review_ready=True,
            module_grouping_source_recovery_execution_reviewed=True, module_grouping_detail_reviewed=True,
            module_paths_reviewed=True, per_module_counts_reviewed=True, bounded_nodeid_samples_reviewed=True,
            top_module_source_detail_reviewed=True, cache_hash_and_count_verification_reviewed=True,
            lastfailed_subset_of_nodeids_reviewed=True, source_recovery_limitations_reviewed=True,
            unsupported_claims_boundary_reviewed=True,
            ready_for_after_v2_planning_reentry_after_source_recovery_review=True,
            failed_or_errored_nodeids_count=1404, module_summary_module_count=29,
            largest_module_nodeid_counts=[136,131,122,112,111],
            top_five_module_paths=deepcopy(TOP_FIVE), top_5_count_sum=612,
            top_5_percentage_of_failed_or_errored_nodeids="43.58974359", top_10_count_sum=1069,
            top_10_percentage_of_failed_or_errored_nodeids="76.13960114",
            cache_hash_and_count_verification_review={
                "lastfailed_cache_sha256_verified":cache["lastfailed_cache_sha256_actual"]==source.EXPECTED_LASTFAILED_SHA256,
                "nodeids_cache_sha256_verified":cache["nodeids_cache_sha256_actual"]==source.EXPECTED_NODEIDS_SHA256,
                "lastfailed_cache_count_verified":cache["lastfailed_cache_entry_count_actual"]==1404,
                "nodeids_cache_count_verified":cache["nodeids_cache_entry_count_actual"]==26288,
                "lastfailed_nodeids_subset_of_nodeids":cache["lastfailed_nodeids_subset_of_nodeids"],
            },
            recovered_module_grouping_detail_review={"source_detail_digest":SOURCE_RECOVERY_DETAIL_DIGEST,"module_count":29,"nodeid_count":1404,"reviewed":True},
            top_module_source_detail_review=deepcopy(top),
            planned_outputs_reviewed=True, planned_outputs_review=deepcopy(execution["planned_outputs"]),
            source_recovery_limitations_review=deepcopy(LIMITATIONS),
            recommended_next_task=SUCCESS_NEXT_TASK,
        )
    else:
        review.update(
            artifact_kind=ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1,
            review_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE,
            module_grouping_source_recovery_results_review_ready=False,
            module_grouping_source_recovery_execution_reviewed=False, module_grouping_detail_reviewed=False,
            module_paths_reviewed=False, per_module_counts_reviewed=False, bounded_nodeid_samples_reviewed=False,
            top_module_source_detail_reviewed=False, cache_hash_and_count_verification_reviewed=False,
            lastfailed_subset_of_nodeids_reviewed=False, source_recovery_limitations_reviewed=False,
            unsupported_claims_boundary_reviewed=True, planned_outputs_reviewed=False,
            ready_for_after_v2_planning_reentry_after_source_recovery_review=False,
            blocked_reason=";".join(reasons), recommended_next_task=BLOCKED_NEXT_TASK,
        )
    review=_finish(review,success)
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(review: dict) -> dict:
    if not isinstance(review,dict): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("review must be object")
    success=review.get("artifact_kind")==ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1
    expected_kind=ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1 if success else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1
    expected_status=MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY if success else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE
    for field,value in {"artifact_kind":expected_kind,"review_status":expected_status,"review_scope":REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN,"source_module_grouping_source_recovery_execution_digest":SOURCE_EXECUTION_DIGEST,"source_module_grouping_source_recovery_detail_digest":SOURCE_RECOVERY_DETAIL_DIGEST,"source_module_grouping_source_recovery_digest_manifest_digest":SOURCE_DIGEST_MANIFEST_DIGEST}.items():
        if review.get(field)!=value: raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError(f"{field} mismatch")
    checklist=_checklist(review,success)
    if review.get("checklist")!=checklist or any(item["status"]!=PASS for item in checklist): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("checklist invalid")
    digest=review.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest")
    if not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest) or digest!=_review_digest(review): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("review digest invalid")
    manifest_field="marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest" if success else "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest"
    manifest_digest = str(review.get(manifest_field, ""))
    if not re.fullmatch(r"[0-9a-f]{64}", manifest_digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("review manifest digest missing")
    expected_manifest_digest = (
        _review_manifest(review)
        if success
        else semantic_digest(
            {
                "blocked_reason": review["blocked_reason"],
                "source_execution_digest": review["source_module_grouping_source_recovery_execution_digest"],
            }
        )
    )
    if manifest_digest != expected_manifest_digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("review manifest digest invalid")
    return {"artifact_kind":review["artifact_kind"],"review_status":review["review_status"],"review_scope":review["review_scope"],"review_digest":digest,**{key:review["summary"][key] for key in ("total_checks","passed_checks","failed_checks","blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(output_dir: str | Path, *, source_execution: dict | None = None) -> dict:
    review=build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(source_execution=source_execution)
    path=Path(output_dir)/"marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError("output exists")
    payload=canonical_json_bytes(review); path.write_bytes(payload)
    return {"path":str(path),"artifact_kind":review["artifact_kind"],"review_status":review["review_status"],"review_digest":review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"],"payload_sha256":sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_markdown_v1(review: dict) -> str:
    validation=validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(review)
    sections=[("Source Recovery Execution",[SOURCE_EXECUTION_DIGEST]),("Source Approval and Candidate Chain",[source.SOURCE_APPROVAL_DIGEST,source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST]),("Retry Failure Context",["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]),("Cache Verification Review",[str(review.get("cache_hash_and_count_verification_review",{}))]),("Recovered Module Grouping Detail Review",[str(review.get("recovered_module_grouping_detail_review",{}))]),("Top Module Source Detail Review",[str(review.get("top_module_source_detail_review",{}))]),("Unsupported Claims Boundary",[str(UNSUPPORTED_CLAIMS)]),("Source Recovery Limitations",review.get("source_recovery_limitations_review",[])),("Success or Blocked Disposition",[review["review_status"]]),("Authority Boundaries",["No cache read, recovery execution, planning reentry, retry, main merge, runtime, or trading action."]),("Next Chain",review["next_chain"]),("Next Gates",review["next_gates"]),("Risk Controls",review["risk_controls"]),("Checklist Summary",[f"{validation['passed_checks']}/{validation['total_checks']} pass."]),("Guardrails",["Recovered detail remains planning evidence pending separate reentry."])]
    lines=["# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Results Review v1",""]
    for heading,rows in sections: lines += [f"## {heading}",*[f"- {row}" for row in rows],""]
    return "\n".join(lines)


__all__=[
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_markdown_v1",
]
