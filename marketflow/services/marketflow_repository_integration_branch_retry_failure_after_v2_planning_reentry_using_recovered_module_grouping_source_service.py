"""Authorize a future after-v2 planning reentry without executing that plan."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1"
REENTRY_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_READY"
REENTRY_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_ONLY_NOT_PLANNING_EXECUTION_NOT_RETRY_NOT_MAIN"
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_READY = REENTRY_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_ONLY_NOT_PLANNING_EXECUTION_NOT_RETRY_NOT_MAIN = REENTRY_SCOPE
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1"
SOURCE_RESULTS_REVIEW_DIGEST = "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9"
SOURCE_AFTER_V2_APPROVAL_DIGEST = "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97"
SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST = "9ea3399758004bdfeb179ad9315a13ebce4514bd51e2cf3b9d39f507a3f1cf03"
SOURCE_AFTER_V2_CANDIDATE_DIGEST = "c6e22aec87122675e9eb2ccf62af7e72756c471ebec81d89cabe1d800633d5e4"
REENTRY_DECISION = "ALLOW_FUTURE_AFTER_V2_PLANNING_EXECUTION_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE"
REENTRY_DECISION_STATUS = "READY_FOR_SEPARATELY_INVOKED_REENTRY_EXECUTION_NOT_EXECUTED"
REENTRY_REASON = (
    "The source recovery results review verified recovered module paths, per-module counts, bounded node-ID "
    "samples, top-module concentration, limitations, and unsupported-claims boundaries. The previous planning "
    "blocker was the absence of module grouping detail; that blocker is resolved for a future planning re-entry, "
    "but no planning execution is performed by this artifact."
)
SELECTED_PACKAGE = "PACKAGE_REENTER_AFTER_V2_PLANNING_EXECUTION_WITH_RECOVERED_MODULE_GROUPING_SOURCE"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ACCEPTED_FOR = [
    "after-v2 planning execution reentry",
    "module-prioritization planning",
    "top-module concentration planning",
    "targeted diagnostic-output capture candidate planning",
    "evidence-root review candidate planning",
    "path/cwd review candidate planning",
    "digest-drift review candidate planning",
    "fixture-isolation review candidate planning",
]
NOT_ACCEPTED_FOR = [
    "failure/error separation",
    "first failure identification",
    "first error identification",
    "traceback root cause",
    "direct code remediation",
    "evidence remediation",
    "retry success",
    "main merge readiness",
    "predictive usefulness",
    "profitability",
    "runtime or broker authority",
]
FUTURE_REENTRY_EXECUTION_REQUIREMENTS = {
    "source_recovery_results_review_must_be_ready": True,
    "source_recovery_execution_digest_must_be_bound": True,
    "source_recovery_detail_digest_must_be_bound": True,
    "source_recovery_manifest_digest_must_be_bound": True,
    "previous_after_v2_blocked_execution_must_be_bound": True,
    "previous_after_v2_blocked_reason_must_be_bound": True,
    "recovered_module_paths_must_be_available": True,
    "per_module_counts_must_be_available": True,
    "bounded_nodeid_samples_must_be_available": True,
    "top_module_concentration_must_be_available": True,
    "unsupported_claims_boundary_must_be_preserved": True,
    "future_reentry_execution_must_not_read_cache": True,
    "future_reentry_execution_must_use_recovered_reviewed_source_only": True,
    "future_reentry_execution_must_not_run_retry": True,
    "future_reentry_execution_must_not_run_full_pytest": True,
    "future_reentry_execution_must_not_run_diagnostic_commands": True,
    "future_reentry_execution_must_not_claim_root_cause": True,
    "future_reentry_execution_must_not_recommend_direct_code_remediation": True,
    "future_reentry_execution_must_not_create_retry_candidate": True,
    "future_reentry_results_review_required": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_REENTRY_EXECUTION_PLAN = [
    "Bind this reentry digest and source recovery results-review digest.",
    "Bind recovered detail digest and module grouping source recovery manifest.",
    "Use recovered reviewed module grouping detail only.",
    "Build prioritized module planning rows using deterministic ordering.",
    "Define PRIORITY_1_TOP_5_MODULE_GROUPS, PRIORITY_2_NEXT_5_MODULE_GROUPS, and PRIORITY_3_REMAINING_MODULE_GROUPS.",
    "Generate top-module concentration planning summary.",
    "Generate targeted diagnostic-output capture, evidence-root requirement review, path/cwd assumption review, digest constant drift review, and fixture isolation review planning buckets.",
    "Preserve no failure/error separation, first-order, traceback root-cause, direct-remediation, retry-success, or main-merge-readiness claims.",
    "Recommend a follow-on candidate only after execution results review.",
    "Keep new retry, main merge, runtime, and trading closed.",
]
PLANNED_OUTPUT_IDS = [
    "after_v2_planning_reentry_execution_manifest",
    "prioritized_module_group_summary",
    "priority_tier_report",
    "top_module_concentration_report",
    "diagnostic_capture_candidate_report",
    "evidence_root_review_candidate_report",
    "path_cwd_review_candidate_report",
    "digest_drift_review_candidate_report",
    "fixture_isolation_review_candidate_report",
    "unsupported_claims_boundary_report",
    "recommended_follow_on_candidate_report",
    "digest_manifest",
]
NON_GOALS = [
    "do_not_execute_after_v2_planning_now",
    "do_not_execute_remediation_now",
    "do_not_execute_diagnostics_now",
    "do_not_execute_classification_now",
    "do_not_classify_modules_again_now",
    "do_not_read_cache_now",
    "do_not_recover_module_grouping_again_now",
    "do_not_modify_cache_now",
    "do_not_parse_operator_logs_now",
    "do_not_run_diagnostic_commands_now",
    "do_not_rerun_retry_now",
    "do_not_run_full_pytest_now",
    "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review",
    "do_not_create_integration_results_review",
    "do_not_mark_integration_successful",
    "do_not_claim_failure_error_separation",
    "do_not_claim_first_failure",
    "do_not_claim_first_error",
    "do_not_claim_traceback_root_cause",
    "do_not_recommend_direct_code_remediation",
    "do_not_treat_recovered_source_as_retry_success",
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
    "Remediation or Method Execution After Classification v2 Review Reentry v1.",
    "Remediation or Method Results Review After Classification v2 Review v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.",
    "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.",
    "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_or_method_execution_after_classification_v2_review_reentry",
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "reentry_does_not_execute_after_v2_planning",
    "reentry_does_not_execute_remediation",
    "reentry_does_not_execute_diagnostics",
    "reentry_does_not_execute_classification",
    "reentry_does_not_classify_modules_again",
    "reentry_does_not_read_cache",
    "reentry_does_not_recover_module_grouping_again",
    "reentry_does_not_modify_cache",
    "reentry_does_not_parse_operator_logs",
    "reentry_does_not_run_diagnostic_commands",
    "reentry_does_not_rerun_retry",
    "reentry_does_not_run_full_pytest",
    "reentry_does_not_create_new_retry_candidate",
    "reentry_does_not_create_retry_results_review",
    "reentry_does_not_create_integration_results_review",
    "reentry_does_not_mark_integration_successful",
    "reentry_does_not_generate_successful_integration_digest",
    "reentry_does_not_claim_failure_error_separation",
    "reentry_does_not_claim_first_failure",
    "reentry_does_not_claim_first_error",
    "reentry_does_not_claim_traceback_root_cause",
    "reentry_does_not_recommend_direct_code_remediation",
    "reentry_does_not_treat_recovered_source_as_retry_success",
    "reentry_does_not_push_integration_branch",
    "reentry_does_not_push_main",
    "reentry_does_not_delete_integration_branch",
    "reentry_does_not_delete_worktree",
    "reentry_does_not_force_push",
    "reentry_does_not_prune_remotes",
    "reentry_does_not_modify_tags",
    "reentry_does_not_commit_marketflow_outputs",
    "reentry_does_not_commit_pytest_cache",
    "reentry_does_not_modify_staged_evidence",
    "reentry_does_not_regenerate_evidence",
    "reentry_does_not_call_providers",
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
    "recovered_source_is_planning_source_not_root_cause",
    "previous_blocker_resolved_for_reentry_only",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_reentry_execution_required",
    "separate_reentry_results_review_required",
    "separate_diagnostic_capture_approval_required_before_diagnostics",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
UNSUPPORTED_CLAIMS = {
    "failure_modules_classified": False,
    "error_modules_classified": False,
    "failure_error_separation_claimed": False,
    "first_failure_identified": False,
    "first_error_identified": False,
    "first_order_claim_made": False,
    "traceback_root_cause_claimed": False,
    "direct_code_remediation_recommended": False,
    "retry_success_claimed": False,
    "main_merge_readiness_claimed": False,
}


class MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError(ValueError):
    """Raised when reentry evidence or a reentry artifact fails closed."""


def _committed_source_results_review() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1,
        "review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY,
        "review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.source.SOURCE_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.source.approval_source.source.SOURCE_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "source_results_review_v2_digest": source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_review_manifest_digest": "6a7c4796c188e082d4433d86f93244f8a3fe2f985302a0a52c6a4843feef01a3",
        "source_execution_v2_digest": source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_digest_manifest_digest": "ac0b172d1ed107922fb0dc115b931752848e9da5db882586cd71897a41cc6add",
        "source_approval_v2_digest": "a29132ad740c0e617fb438c154c4b5fed756f15bceed40ff132334d1c5e58412",
        "source_staged_inventory_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "module_grouping_source_recovery_results_review_created": True,
        "module_grouping_source_recovery_results_review_ready": True,
        "module_grouping_source_recovery_execution_reviewed": True,
        "module_grouping_detail_reviewed": True,
        "module_paths_reviewed": True,
        "per_module_counts_reviewed": True,
        "bounded_nodeid_samples_reviewed": True,
        "top_module_source_detail_reviewed": True,
        "cache_hash_and_count_verification_reviewed": True,
        "source_recovery_limitations_reviewed": True,
        "unsupported_claims_boundary_reviewed": True,
        "ready_for_after_v2_planning_reentry_after_source_recovery_review": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": deepcopy(source.TOP_FIVE),
        "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "cache_hash_and_count_verification_review": {
            "lastfailed_cache_sha256_verified": True,
            "nodeids_cache_sha256_verified": True,
            "lastfailed_cache_count_verified": True,
            "nodeids_cache_count_verified": True,
            "lastfailed_nodeids_subset_of_nodeids": True,
        },
        "recovered_module_grouping_detail_review": {
            "source_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
            "module_count": 29,
            "nodeid_count": 1404,
            "reviewed": True,
        },
        **deepcopy(UNSUPPORTED_CLAIMS),
    }


def _source_failures(review: Mapping[str, Any]) -> list[str]:
    expected = {
        "artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1,
        "review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY,
        "review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "source_results_review_v2_digest": source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "module_grouping_source_recovery_results_review_ready": True,
        "module_grouping_detail_reviewed": True,
        "module_paths_reviewed": True,
        "per_module_counts_reviewed": True,
        "bounded_nodeid_samples_reviewed": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": source.TOP_FIVE,
        "top_5_count_sum": 612,
        "top_10_count_sum": 1069,
        "unsupported_claims_boundary_reviewed": True,
        "ready_for_after_v2_planning_reentry_after_source_recovery_review": True,
    }
    failures = [f"{field.upper()}_MISMATCH_OR_MISSING" for field, value in expected.items() if review.get(field) != value]
    cache = review.get("cache_hash_and_count_verification_review")
    if not isinstance(cache, Mapping) or not all(cache.get(key) is True for key in (
        "lastfailed_cache_sha256_verified",
        "nodeids_cache_sha256_verified",
        "lastfailed_cache_count_verified",
        "nodeids_cache_count_verified",
        "lastfailed_nodeids_subset_of_nodeids",
    )):
        failures.append("CACHE_VERIFICATION_REVIEW_MISSING")
    detail = review.get("recovered_module_grouping_detail_review")
    if not isinstance(detail, Mapping) or detail.get("reviewed") is not True:
        failures.append("RECOVERED_MODULE_DETAIL_MISSING")
    if {key: review.get(key) for key in UNSUPPORTED_CLAIMS} != UNSUPPORTED_CLAIMS:
        failures.append("UNSUPPORTED_CLAIMS_BOUNDARY_MISSING")
    return failures


def _base_artifact(review: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "reentry_status": REENTRY_STATUS,
        "reentry_scope": REENTRY_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "reentry_only": True,
        "source_module_grouping_source_recovery_results_review_artifact_kind": review["artifact_kind"],
        "source_module_grouping_source_recovery_results_review_status": review["review_status"],
        "source_module_grouping_source_recovery_results_review_scope": review["review_scope"],
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": source.source.SOURCE_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": source.source.approval_source.source.SOURCE_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason_before_recovery": source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": review["source_results_review_v2_digest"],
        "source_review_manifest_digest": review["source_review_manifest_digest"],
        "source_execution_v2_digest": review["source_execution_v2_digest"],
        "source_module_grouping_digest": review["source_module_grouping_digest"],
        "source_digest_manifest_digest": review["source_digest_manifest_digest"],
        "source_approval_v2_digest": review["source_approval_v2_digest"],
        "source_staged_inventory_digest": review["source_staged_inventory_digest"],
        "retry_execution_branch": review["retry_execution_branch"],
        "retry_execution_commit": review["retry_execution_commit"],
        "retry_pytest_working_directory": str(source.source.DEFAULT_WORKTREE),
        "retry_pytest_passed_count": 24877,
        "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112,
        "retry_pytest_skipped_count": 7,
        "retry_pytest_first_result_authoritative": True,
        "retry_pytest_passed": False,
        "retry_pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
        "lastfailed_cache_read_in_source_execution": True,
        "lastfailed_cache_sha256_expected": source.source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_sha256_actual": source.source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count_expected": 1404,
        "lastfailed_cache_entry_count_actual": 1404,
        "nodeids_cache_read_in_source_execution": True,
        "nodeids_cache_sha256_expected": source.source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_sha256_actual": source.source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count_expected": 26288,
        "nodeids_cache_entry_count_actual": 26288,
        "lastfailed_nodeids_subset_of_nodeids": True,
        "cache_verification_review": deepcopy(review["cache_hash_and_count_verification_review"]),
        "recovered_module_grouping_detail_review": deepcopy(review["recovered_module_grouping_detail_review"]),
        "module_grouping_source_recovery_results_review_created": True,
        "module_grouping_source_recovery_results_review_ready": True,
        "module_grouping_source_recovery_execution_reviewed": True,
        "module_grouping_detail_reviewed": True,
        "module_paths_reviewed": True,
        "per_module_counts_reviewed": True,
        "bounded_nodeid_samples_reviewed": True,
        "top_module_source_detail_reviewed": True,
        "cache_hash_and_count_verification_reviewed": True,
        "source_recovery_limitations_reviewed": True,
        "source_recovery_limitations_review": list(source.LIMITATIONS),
        "unsupported_claims_boundary_reviewed": True,
        "ready_for_after_v2_planning_reentry_after_source_recovery_review": True,
        "module_grouping_source_recovery_executed": True,
        "module_grouping_detail_recovered": True,
        "module_grouping_detail_exposed": True,
        "module_paths_recovered": True,
        "per_module_counts_recovered": True,
        "bounded_nodeid_samples_recovered": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "deterministic_ordering": ["descending failed_or_errored_nodeid_count", "module_path ascending"],
        "sample_nodeids_bounded_per_module": 5,
        "top_five_module_paths": deepcopy(source.TOP_FIVE),
        "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "previous_after_v2_planning_execution_blocked": True,
        "previous_after_v2_planning_execution_blocked_reason": source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        "previous_after_v2_planning_execution_blocker_resolved_for_reentry": True,
        "previous_blocker_resolution_reason": (
            "The reviewed source-recovery results now provide module paths, per-module counts, bounded node-ID "
            "samples, top-module detail, and digest-bound recovery evidence needed to re-enter after-v2 planning execution."
        ),
        **deepcopy(UNSUPPORTED_CLAIMS),
        "diagnostic_method_executed": False,
        "code_remediation_executed": False,
        "evidence_remediation_executed": False,
        "classification_execution_performed_in_reentry": False,
        "reentry_decision": REENTRY_DECISION,
        "reentry_decision_status": REENTRY_DECISION_STATUS,
        "reason": REENTRY_REASON,
        "after_v2_planning_reentry_using_recovered_module_grouping_source_created": True,
        "after_v2_planning_reentry_using_recovered_module_grouping_source_ready": True,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "accepted_source_type": "RECOVERED_REVIEWED_DETACHED_PYTEST_CACHE_MODULE_GROUPING_DETAIL",
        "accepted_for": list(ACCEPTED_FOR),
        "not_accepted_for": list(NOT_ACCEPTED_FOR),
        "recommended_reentry_package": {
            "package_id": SELECTED_PACKAGE,
            "status": "RECOMMENDED_FOR_NEXT_TASK_NOT_EXECUTED",
            "purpose": "Use the reviewed recovered module-grouping source to rerun the previously blocked after-v2 planning execution as a separately invoked reentry execution.",
            "selected_for_next_task": True,
            "executed": False,
        },
        "alternative_reentry_packages": [
            {
                "package_id": "PACKAGE_REQUIRE_ADDITIONAL_SOURCE_RECOVERY_BEFORE_REENTRY",
                "status": "AVAILABLE_NOT_SELECTED",
                "reason": "Additional source recovery is not required because module paths, counts, samples, and top-module concentration were reviewed.",
                "selected": False,
            },
            {
                "package_id": "PACKAGE_RETRY_WITHOUT_AFTER_V2_PLANNING_REENTRY",
                "status": "BLOCKED_NOT_ALLOWED",
                "reason": "New retry remains blocked until remediation/method planning and review are completed.",
                "selected": False,
            },
            {
                "package_id": "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
                "status": "BLOCKED_NOT_ALLOWED",
                "reason": "Main merge remains blocked until a future retry results review passes.",
                "selected": False,
            },
        ],
        "future_reentry_execution_requirements": deepcopy(FUTURE_REENTRY_EXECUTION_REQUIREMENTS),
        "future_reentry_execution_plan": {
            "status": "PLANNED_NOT_EXECUTED",
            "steps": list(FUTURE_REENTRY_EXECUTION_PLAN),
        },
        "planned_outputs": [
            {"output_id": output_id, "status": "PLANNED_NOT_GENERATED"}
            for output_id in PLANNED_OUTPUT_IDS
        ],
        "non_goals": list(NON_GOALS),
        "ready_for_remediation_or_method_execution_after_classification_v2_review_reentry": True,
        "after_v2_planning_execution_reentered": False,
        "after_v2_planning_execution_performed": False,
        "remediation_or_method_after_v2_reentry_execution_created": False,
        "remediation_or_method_after_v2_reentry_execution_performed": False,
        "remediation_or_method_results_review_after_v2_created": False,
        "after_v2_planning_reentry_created": False,
        "remediation_or_method_after_v2_reentry_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "cache_read_in_reentry": False,
        "cache_read_in_review": False,
        "module_grouping_recovered_in_reentry": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(source.source.DEFAULT_WORKTREE),
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_reentry": False,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_reentry": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_reentry": False,
        "dataset_generation_performed_in_review": False,
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
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": SUCCESS_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(reentry: Mapping[str, Any]) -> list[dict[str, Any]]:
    values: dict[str, tuple[Any, Any]] = {
        "source_recovery_results_review_digest_bound": (SOURCE_RESULTS_REVIEW_DIGEST, reentry.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, reentry.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (source.SOURCE_EXECUTION_DIGEST, reentry.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (source.SOURCE_RECOVERY_DETAIL_DIGEST, reentry.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (source.SOURCE_DIGEST_MANIFEST_DIGEST, reentry.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_recovery_approval_digest_bound": (source.source.SOURCE_APPROVAL_DIGEST, reentry.get("source_module_grouping_source_recovery_approval_digest")),
        "source_recovery_operator_review_digest_bound": (source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, reentry.get("source_module_grouping_source_recovery_operator_review_digest")),
        "source_recovery_candidate_digest_bound": (source.source.approval_source.source.SOURCE_CANDIDATE_DIGEST, reentry.get("source_module_grouping_source_recovery_candidate_digest")),
        "source_blocked_after_v2_execution_digest_bound": (source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST, reentry.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST, reentry.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL, reentry.get("blocked_reason_before_recovery")),
        "source_results_review_v2_digest_bound": (source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST, reentry.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST, reentry.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST, reentry.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", reentry.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [reentry.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "cache_verification_reviewed_bound": (
            [True, {"lastfailed_cache_sha256_verified": True, "nodeids_cache_sha256_verified": True, "lastfailed_cache_count_verified": True, "nodeids_cache_count_verified": True, "lastfailed_nodeids_subset_of_nodeids": True}],
            [reentry.get("cache_hash_and_count_verification_reviewed"), reentry.get("cache_verification_review")],
        ),
        "recovered_module_detail_bound": (
            [True, {"source_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST, "module_count": 29, "nodeid_count": 1404, "reviewed": True}],
            [reentry.get("module_grouping_detail_reviewed"), reentry.get("recovered_module_grouping_detail_review")],
        ),
        "module_paths_reviewed_bound": (True, reentry.get("module_paths_reviewed")),
        "per_module_counts_reviewed_bound": (True, reentry.get("per_module_counts_reviewed")),
        "bounded_nodeid_samples_reviewed_bound": (True, reentry.get("bounded_nodeid_samples_reviewed")),
        "failed_or_errored_nodeids_1404_bound": (1404, reentry.get("failed_or_errored_nodeids_count")),
        "module_count_29_bound": (29, reentry.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], reentry.get("largest_module_nodeid_counts")),
        "top_five_module_paths_bound": (source.TOP_FIVE, reentry.get("top_five_module_paths")),
        "top_five_count_sum_612_bound": (612, reentry.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, reentry.get("top_10_count_sum")),
        "unsupported_claims_boundary_bound": (
            [True, UNSUPPORTED_CLAIMS],
            [reentry.get("unsupported_claims_boundary_reviewed"), {key: reentry.get(key) for key in UNSUPPORTED_CLAIMS}],
        ),
        "previous_blocker_resolved_for_reentry_true": (True, reentry.get("previous_after_v2_planning_execution_blocker_resolved_for_reentry")),
        "reentry_created_true": (True, reentry.get("after_v2_planning_reentry_using_recovered_module_grouping_source_created")),
        "reentry_ready_true": (True, reentry.get("after_v2_planning_reentry_using_recovered_module_grouping_source_ready")),
        "recovered_source_accepted_for_planning_reentry_true": (True, reentry.get("recovered_module_grouping_source_accepted_for_planning_reentry")),
        "ready_for_reentry_execution_true": (True, reentry.get("ready_for_remediation_or_method_execution_after_classification_v2_review_reentry")),
        "future_reentry_requirements_defined": (FUTURE_REENTRY_EXECUTION_REQUIREMENTS, reentry.get("future_reentry_execution_requirements")),
        "future_reentry_plan_defined": ({"status": "PLANNED_NOT_EXECUTED", "steps": FUTURE_REENTRY_EXECUTION_PLAN}, reentry.get("future_reentry_execution_plan")),
        "planned_outputs_defined": ([{"output_id": output_id, "status": "PLANNED_NOT_GENERATED"} for output_id in PLANNED_OUTPUT_IDS], reentry.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, reentry.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, reentry.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, reentry.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, reentry.get("risk_controls")),
        "no_tracked_marketflow_files": (False, reentry.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, reentry.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, reentry.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, reentry.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, reentry.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, reentry.get("broker_execution")),
    }
    false_fields = {
        "after_v2_planning_execution_reentered_false": "after_v2_planning_execution_reentered",
        "after_v2_planning_execution_performed_false": "after_v2_planning_execution_performed",
        "reentry_execution_created_false": "remediation_or_method_after_v2_reentry_execution_created",
        "reentry_execution_performed_false": "remediation_or_method_after_v2_reentry_execution_performed",
        "remediation_results_review_created_false": "remediation_or_method_results_review_after_v2_created",
        "diagnostic_method_executed_false": "diagnostic_method_executed",
        "code_remediation_executed_false": "code_remediation_executed",
        "evidence_remediation_executed_false": "evidence_remediation_executed",
        "classification_execution_performed_false": "classification_execution_performed_in_reentry",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "retry_rerun_false": "retry_rerun_performed",
        "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed",
        "diagnostic_output_false": "diagnostic_output_captured",
        "cache_read_in_reentry_false": "cache_read_in_reentry",
        "module_grouping_recovered_in_reentry_false": "module_grouping_recovered_in_reentry",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_reentry",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_reentry",
        "dataset_generation_false": "dataset_generation_performed_in_reentry",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, reentry.get(field)) for check_id, field in false_fields.items()})
    values["successful_integration_digest_false"] = (
        [False, False],
        [reentry.get("successful_integration_execution_digest_generated"), reentry.get("successful_integration_validation_digest_generated")],
    )
    ordered_ids = [
        "source_recovery_results_review_digest_bound", "source_recovery_results_review_manifest_digest_bound",
        "source_recovery_execution_digest_bound", "source_recovery_detail_digest_bound",
        "source_recovery_digest_manifest_bound", "source_recovery_approval_digest_bound",
        "source_recovery_operator_review_digest_bound", "source_recovery_candidate_digest_bound",
        "source_blocked_after_v2_execution_digest_bound", "source_blocked_after_v2_manifest_digest_bound",
        "source_blocked_reason_bound", "source_results_review_v2_digest_bound", "source_execution_v2_digest_bound",
        "source_module_grouping_digest_bound", "retry_execution_commit_bound", "retry_failure_counts_bound",
        "cache_verification_reviewed_bound", "recovered_module_detail_bound", "module_paths_reviewed_bound",
        "per_module_counts_reviewed_bound", "bounded_nodeid_samples_reviewed_bound",
        "failed_or_errored_nodeids_1404_bound", "module_count_29_bound", "largest_module_counts_bound",
        "top_five_module_paths_bound", "top_five_count_sum_612_bound", "top_ten_count_sum_1069_bound",
        "unsupported_claims_boundary_bound", "previous_blocker_resolved_for_reentry_true", "reentry_created_true",
        "reentry_ready_true", "recovered_source_accepted_for_planning_reentry_true", "ready_for_reentry_execution_true",
        *false_fields,
        "successful_integration_digest_false", "predictive_usefulness_not_accepted", "profitability_not_accepted",
        "runtime_not_authorized", "broker_not_authorized", "future_reentry_requirements_defined",
        "future_reentry_plan_defined", "planned_outputs_defined", "non_goals_defined", "next_chain_defined",
        "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
    ]
    return [_check(check_id, *values[check_id]) for check_id in ordered_ids]


def _summary(reentry: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "after_v2_planning_reentry_using_recovered_module_grouping_source_created": True,
        "after_v2_planning_reentry_using_recovered_module_grouping_source_ready": True,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "previous_after_v2_planning_execution_blocker_resolved_for_reentry": True,
        "ready_for_remediation_or_method_execution_after_classification_v2_review_reentry": True,
        "after_v2_planning_execution_reentered": False,
        "after_v2_planning_execution_performed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _digest(reentry: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(reentry))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(
    *, source_results_review: dict | None = None
) -> dict:
    """Build reentry authority from reviewed committed facts without executing planning."""

    review = deepcopy(source_results_review) if source_results_review is not None else _committed_source_results_review()
    failures = _source_failures(review)
    if failures:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError(
            ";".join(failures)
        )
    reentry = _base_artifact(review)
    reentry["checklist"] = _checklist(reentry)
    reentry["summary"] = _summary(reentry, reentry["checklist"])
    reentry["marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest"] = _digest(reentry)
    validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(reentry)
    return reentry


def validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(
    reentry: dict,
) -> dict:
    """Validate all source, planning-only, authority, checklist, and digest boundaries."""

    if not isinstance(reentry, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError("reentry must be object")
    for field, expected in {
        "artifact_kind": ARTIFACT_KIND,
        "reentry_status": REENTRY_STATUS,
        "reentry_scope": REENTRY_SCOPE,
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": source.SOURCE_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": source.SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": source.SOURCE_DIGEST_MANIFEST_DIGEST,
    }.items():
        if reentry.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError(f"{field} mismatch")
    checklist = _checklist(reentry)
    if reentry.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError("checklist invalid")
    summary = _summary(reentry, checklist)
    if reentry.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError("summary invalid")
    digest = reentry.get("marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _digest(reentry):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError("reentry digest invalid")
    return {
        "artifact_kind": reentry["artifact_kind"],
        "reentry_status": reentry["reentry_status"],
        "reentry_scope": reentry["reentry_scope"],
        "reentry_digest": digest,
        **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(
    output_dir: str | Path, *, source_results_review: dict | None = None
) -> dict:
    """Write one deterministic reentry artifact to an isolated caller-selected directory."""

    reentry = build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(
        source_results_review=source_results_review
    )
    path = Path(output_dir) / "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError("output exists")
    payload = canonical_json_bytes(reentry)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": reentry["artifact_kind"],
        "reentry_status": reentry["reentry_status"],
        "reentry_digest": reentry["marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest"],
        "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_markdown_v1(
    reentry: dict,
) -> str:
    """Render the validated reentry artifact as bounded governance Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(reentry)
    sections = [
        ("Source Module Grouping Source Recovery Results Review", [SOURCE_RESULTS_REVIEW_DIGEST, SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST]),
        ("Source Recovery Execution", [source.SOURCE_EXECUTION_DIGEST, source.SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Previous Blocked After-v2 Planning Execution", [reentry["blocked_reason_before_recovery"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped; the first failed retry remains authoritative."]),
        ("Recovered Module Grouping Source", ["1,404 failed-or-errored node IDs across 29 reviewed module groups."]),
        ("Top Module Concentration", ["Top five: 612 (43.58974359%); top ten: 1,069 (76.13960114%)."]),
        ("Reentry Decision", [REENTRY_DECISION, REENTRY_DECISION_STATUS, REENTRY_REASON]),
        ("Accepted and Unsupported Uses", [*reentry["accepted_for"], *reentry["not_accepted_for"]]),
        ("Future Reentry Execution Requirements", [f"{key}: {value}" for key, value in reentry["future_reentry_execution_requirements"].items()]),
        ("Future Reentry Execution Plan", reentry["future_reentry_execution_plan"]["steps"]),
        ("Planned Outputs", [f"{item['output_id']}: {item['status']}" for item in reentry["planned_outputs"]]),
        ("Non-Goals", reentry["non_goals"]),
        ("Authority Boundaries", ["Planning execution, diagnostics, remediation, retry, main merge, runtime, and trading remain closed."]),
        ("Next Chain", reentry["next_chain"]),
        ("Next Gates", reentry["next_gates"]),
        ("Risk Controls", reentry["risk_controls"]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["The recovered grouping is accepted only as input to a separately invoked planning reentry execution."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure After-v2 Planning Reentry Using Recovered Module Grouping Source v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND",
    "REENTRY_STATUS",
    "REENTRY_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_ONLY_NOT_PLANNING_EXECUTION_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1",
    "write_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1",
    "build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_markdown_v1",
]
