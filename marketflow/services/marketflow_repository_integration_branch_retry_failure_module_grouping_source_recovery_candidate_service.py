"""Define a candidate for recovering module-grouping source detail later."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_V1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_"
    "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN"
)
SCHEMA_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_module_grouping_"
    "source_recovery_candidate_v1"
)
SOURCE_BLOCKED_EXECUTION_DIGEST = (
    "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755"
)
SOURCE_BLOCKED_MANIFEST_DIGEST = (
    "c3d644957eb536ede1d725c912f0211a0d84aa72e56d5f8cbed2e0939a907cef"
)
RECOMMENDED_PACKAGE = (
    "PACKAGE_RECOVER_MODULE_GROUPING_DETAIL_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY"
)
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_PHILOSOPHY = (
    "The after-v2 planning execution failed closed because committed evidence did "
    "not expose module paths, per-module counts, or bounded node-ID samples. The "
    "next safe step is to choose a controlled source-recovery method that recovers "
    "or exposes module-grouping detail without inventing module identities and "
    "without rerunning the failed retry."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no cache read, source recovery, diagnostics, remediation, "
    "classification, retry, results review, main merge, or runtime authority is "
    "created by this artifact."
)
CANDIDATE_GOAL = (
    "Define safe future packages to recover a module-grouping detail source "
    "sufficient for re-entering prioritized planning, while preserving all "
    "unsupported-claim and failed-retry boundaries."
)
KNOWN_AVAILABLE_DETAIL = [
    "aggregate retry counts",
    "total failed-or-errored node-ID count",
    "module count",
    "largest module counts",
    "module-grouping digest",
    "source execution/review digests",
]
KNOWN_MISSING_DETAIL = [
    "module paths",
    "per-module counts by module path",
    "bounded node-ID samples by module",
    "module grouping report content",
    "committed source snapshot suitable for downstream prioritization",
]
UNSUPPORTED_CLAIMS_BOUNDARY = {
    "failure_modules_classified": False,
    "error_modules_classified": False,
    "failure_error_separation_claimed": False,
    "first_failure_identified": False,
    "first_error_identified": False,
    "first_order_claim_made": False,
    "traceback_root_cause_claimed": False,
    "retry_success_claimed": False,
    "main_merge_readiness_claimed": False,
    "direct_code_remediation_recommended": False,
}

PROPOSED_PACKAGES = [
    {
        "package_id": RECOMMENDED_PACKAGE,
        "status": RECOMMENDATION_STATUS,
        "purpose": (
            "In a future separately approved execution, read the same reviewed "
            "detached pytest cache read-only, verify the reviewed hashes and "
            "counts, reconstruct deterministic module-path grouping, and expose "
            "a bounded module grouping source artifact."
        ),
        "recommended_for": (
            "It is the most direct source because the reviewed cache produced the "
            "original 1,404-node / 29-module grouping and does not require "
            "rerunning pytest."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_EXPOSE_MODULE_GROUPING_FROM_CLASSIFICATION_EXECUTION_V2_OUTPUT_IF_LOCATABLE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Search committed source artifacts or explicitly referenced ignored "
            "local execution artifacts for the original Classification Method "
            "Execution v2 module grouping output, then expose it if present and "
            "digest-verifiable."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_OPERATOR_PROVIDED_CLASSIFICATION_EXECUTION_V2_MODULE_GROUPING_REPORT_PATH",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Allow the operator to provide an explicit path to the original module "
            "grouping report if it exists outside committed files."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_CREATE_BOUNDED_COMMITTED_MODULE_GROUPING_SUMMARY_FROM_VERIFIED_CACHE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL",
        "purpose": (
            "Future execution may create a bounded, non-secret, committed status "
            "artifact containing module paths, counts, percentages, and bounded "
            "node-ID samples derived from verified cache, while keeping "
            ".pytest_cache untracked."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_RECOVER_ONLY_TOP_MODULE_PATHS_FROM_VERIFIED_CACHE",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Recover only the top module paths and counts needed for targeted "
            "diagnostic-output capture planning, reducing exposure of full "
            "node-ID detail."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_USE_AGGREGATE_COUNTS_AND_TOP_COUNTS_WITHOUT_MODULE_PATHS",
        "status": "BLOCKED_NOT_SUFFICIENT",
        "purpose": (
            "Proceed using only 1,404 node count, 29 module count, and largest "
            "counts 136, 131, 122, 112, 111."
        ),
        "blocked_reason": (
            "Aggregate counts cannot support module-specific planning, diagnostic "
            "targeting, or remediation prioritization without inventing module "
            "identities."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_INFER_MODULE_NAMES_FROM_COUNTS_OR_DIGESTS",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Infer module names from counts, digests, or historical intuition.",
        "blocked_reason": (
            "Module names and node IDs must come from source evidence, not "
            "inference or fabrication."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_RERUN_AUTHORITATIVE_RETRY_TO_RECREATE_MODULE_GROUPING",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Rerun pytest to recreate cache or module grouping.",
        "blocked_reason": (
            "The failed retry remains authoritative. Rerunning pytest would create "
            "a new retry-like event and cannot be used as source recovery under "
            "this candidate."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_DIRECT_REMEDIATION_OR_NEW_RETRY_WITHOUT_MODULE_GROUPING_SOURCE",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": (
            "Proceed directly to remediation or retry without recovered module "
            "grouping detail."
        ),
        "blocked_reason": (
            "The previous planning execution blocked specifically because "
            "module-level detail was unavailable. Direct remediation/retry would "
            "bypass the recovery gate."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_MAIN_MERGE_DESPITE_MISSING_MODULE_GROUPING_SOURCE",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": (
            "Proceed to main merge despite failed retry and missing module grouping "
            "detail."
        ),
        "blocked_reason": (
            "Main merge approval remains blocked until a future retry results "
            "review passes."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
]

RECOMMENDATION_REASON = (
    "The reviewed detached cache is the proven source of the Classification "
    "Method Execution v2 grouping. A future approved read-only cache recovery can "
    "reconstruct module paths and counts without rerunning pytest, inventing data, "
    "or treating the cache as retry success evidence."
)
FUTURE_REQUIREMENTS = {
    "source_blocked_after_v2_execution_must_be_ready": True,
    "source_blocked_execution_digest_must_be_bound": True,
    "source_blocked_manifest_digest_must_be_bound": True,
    "source_results_review_v2_must_be_ready": True,
    "source_module_grouping_digest_must_be_bound": True,
    "retry_failure_counts_must_be_bound": True,
    "module_count_and_largest_counts_must_be_bound": True,
    "unsupported_claims_boundary_must_be_preserved": True,
    "source_recovery_must_not_rerun_retry": True,
    "source_recovery_must_not_run_full_pytest": True,
    "source_recovery_must_not_run_diagnostic_commands": True,
    "source_recovery_must_not_treat_cache_as_retry_success_evidence": True,
    "source_recovery_must_not_infer_module_paths": True,
    "source_recovery_must_fail_closed_if_cache_hash_or_count_mismatches": True,
    "source_recovery_must_fail_closed_if_module_detail_unavailable": True,
    "source_recovery_must_not_commit_pytest_cache": True,
    "source_recovery_must_not_commit_marketflow_outputs": True,
    "source_recovery_must_preserve_origin_main": True,
    "source_recovery_must_preserve_integration_branch": True,
    "source_recovery_must_preserve_staged_evidence": True,
    "future_planning_reentry_requires_source_recovery_results_review": True,
    "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_PLAN_STEPS = [
    "Bind blocked after-v2 execution digest and blocked-manifest digest.",
    "Bind Classification Method Results Review v2 digest and module-grouping digest.",
    "Verify protected refs and untracked .marketflow / .pytest_cache boundaries.",
    (
        "Select one approved recovery source: reviewed detached pytest cache; "
        "original classification execution v2 output if locatable; or an "
        "operator-provided explicit module grouping report path."
    ),
    "If using cache, verify reviewed lastfailed and nodeids hashes and counts before parsing.",
    (
        "Recover module paths, per-module counts, percentages, deterministic "
        "priority order, and bounded node-ID samples."
    ),
    "Produce a bounded module grouping source recovery artifact.",
    (
        "Preserve no failure/error separation, first-order cause, traceback root "
        "cause, direct remediation, retry success, or main-merge readiness claims."
    ),
    (
        "Require source-recovery results review before re-entering after-v2 "
        "planning execution."
    ),
    "Keep new retry, main merge, runtime, and trading closed.",
]
FUTURE_PLAN = [
    {
        "step_id": f"future_source_recovery_step_{index:02d}",
        "description": description,
        "status": "PLANNED_NOT_EXECUTED",
    }
    for index, description in enumerate(FUTURE_PLAN_STEPS, 1)
]
PLANNED_OUTPUT_IDS = [
    "module_grouping_source_recovery_manifest",
    "recovered_module_grouping_detail_report",
    "recovered_module_counts_by_path_report",
    "recovered_bounded_nodeid_samples_report",
    "top_module_source_detail_report",
    "cache_hash_and_count_verification_report",
    "unsupported_claims_boundary_report",
    "source_recovery_limitations_report",
    "planning_reentry_readiness_report",
    "digest_manifest",
]
PLANNED_OUTPUTS = [
    {"output_id": output_id, "status": "PLANNED_NOT_GENERATED"}
    for output_id in PLANNED_OUTPUT_IDS
]
NON_GOALS = [
    "do_not_recover_module_grouping_now",
    "do_not_expose_module_paths_now",
    "do_not_read_cache_now",
    "do_not_modify_cache_now",
    "do_not_parse_operator_logs_now",
    "do_not_run_diagnostic_commands_now",
    "do_not_execute_diagnostics_now",
    "do_not_execute_remediation_now",
    "do_not_execute_classification_now",
    "do_not_classify_modules_again_now",
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
    "do_not_treat_classification_as_retry_success",
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
    "Module Grouping Source Recovery Candidate Operator Review v1.",
    "Module Grouping Source Recovery Approval v1, if selected.",
    "Module Grouping Source Recovery Execution v1, if approved.",
    "Module Grouping Source Recovery Results Review v1.",
    "Re-enter after-v2 planning execution, if source detail is recovered and reviewed.",
    "Remediation or Method Results Review After Classification v2 Review v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Approval / Execution / Results Review, if selected.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "module_grouping_source_recovery_candidate_operator_review",
    "module_grouping_source_recovery_approval_if_selected",
    "module_grouping_source_recovery_execution_if_approved",
    "module_grouping_source_recovery_results_review",
    "after_v2_planning_reentry_if_source_recovered",
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_if_supported",
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
    "candidate_source_recovery_does_not_recover_module_grouping",
    "candidate_source_recovery_does_not_expose_module_paths",
    "candidate_source_recovery_does_not_read_cache",
    "candidate_source_recovery_does_not_modify_cache",
    "candidate_source_recovery_does_not_parse_operator_logs",
    "candidate_source_recovery_does_not_run_diagnostic_commands",
    "candidate_source_recovery_does_not_execute_diagnostics",
    "candidate_source_recovery_does_not_execute_remediation",
    "candidate_source_recovery_does_not_execute_classification",
    "candidate_source_recovery_does_not_classify_modules_again",
    "candidate_source_recovery_does_not_rerun_retry",
    "candidate_source_recovery_does_not_run_full_pytest",
    "candidate_source_recovery_does_not_create_new_retry_candidate",
    "candidate_source_recovery_does_not_create_retry_results_review",
    "candidate_source_recovery_does_not_create_integration_results_review",
    "candidate_source_recovery_does_not_mark_integration_successful",
    "candidate_source_recovery_does_not_generate_successful_integration_digest",
    "candidate_source_recovery_does_not_claim_failure_error_separation",
    "candidate_source_recovery_does_not_claim_first_failure",
    "candidate_source_recovery_does_not_claim_first_error",
    "candidate_source_recovery_does_not_claim_traceback_root_cause",
    "candidate_source_recovery_does_not_recommend_direct_code_remediation",
    "candidate_source_recovery_does_not_treat_cache_or_classification_as_retry_success",
    "candidate_source_recovery_does_not_push_integration_branch",
    "candidate_source_recovery_does_not_push_main",
    "candidate_source_recovery_does_not_delete_integration_branch",
    "candidate_source_recovery_does_not_delete_worktree",
    "candidate_source_recovery_does_not_force_push",
    "candidate_source_recovery_does_not_prune_remotes",
    "candidate_source_recovery_does_not_modify_tags",
    "candidate_source_recovery_does_not_commit_marketflow_outputs",
    "candidate_source_recovery_does_not_commit_pytest_cache",
    "candidate_source_recovery_does_not_modify_staged_evidence",
    "candidate_source_recovery_does_not_regenerate_evidence",
    "candidate_source_recovery_does_not_call_providers",
    "candidate_source_recovery_does_not_acquire_market_data",
    "candidate_source_recovery_does_not_regenerate_dataset",
    "candidate_source_recovery_does_not_recompute_metrics",
    "candidate_source_recovery_does_not_train_models",
    "candidate_source_recovery_does_not_score_strategy",
    "candidate_source_recovery_does_not_generate_recommendations",
    "candidate_source_recovery_does_not_accept_predictive_usefulness",
    "candidate_source_recovery_does_not_accept_profitability",
    "candidate_source_recovery_does_not_authorize_runtime",
    "candidate_source_recovery_does_not_authorize_broker_execution",
    "source_recovery_output_would_be_planning_source_not_root_cause",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_operator_review_required",
    "separate_approval_required_before_source_recovery",
    "separate_results_review_required_after_source_recovery",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_blocked_after_v2_execution_digest_bound",
    "source_blocked_after_v2_manifest_digest_bound",
    "source_blocked_reason_bound",
    "source_after_v2_approval_digest_bound",
    "source_after_v2_operator_review_digest_bound",
    "source_after_v2_candidate_digest_bound",
    "source_results_review_v2_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "classification_evidence_summary_bound",
    "module_count_29_bound",
    "largest_module_counts_bound",
    "known_missing_detail_bound",
    "unsupported_claims_boundary_bound",
    "candidate_created_true",
    "candidate_ready_true",
    "recommended_package_present",
    "packages_present_10",
    "blocked_packages_present_5",
    "recommended_package_not_selected",
    "source_recovery_selected_false",
    "source_recovery_approved_false",
    "source_recovery_executed_false",
    "module_grouping_detail_recovered_false",
    "module_paths_recovered_false",
    "per_module_counts_recovered_false",
    "bounded_nodeid_samples_recovered_false",
    "remediation_or_method_reentry_created_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "cache_read_false",
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
    "future_requirements_defined",
    "future_plan_defined",
    "planned_outputs_defined",
    "non_goals_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
    ValueError
):
    """Raised when the source-recovery candidate crosses its closed boundary."""


def _source_fields() -> dict[str, Any]:
    fields = source._source_fields()
    return {
        "source_blocked_after_v2_execution_artifact_kind": source.ARTIFACT_KIND_BLOCKED,
        "source_blocked_after_v2_execution_status": source.EXECUTION_STATUS_BLOCKED_MODULE_DETAIL,
        "source_blocked_after_v2_execution_scope": source.EXECUTION_SCOPE,
        "source_blocked_after_v2_execution_digest": SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": source.BLOCKED_REASON_MODULE_DETAIL,
        **{
            key: deepcopy(fields[key])
            for key in (
                "source_after_v2_approval_digest",
                "source_after_v2_operator_review_digest",
                "source_after_v2_candidate_digest",
                "source_results_review_v2_digest",
                "source_review_manifest_digest",
                "source_execution_v2_digest",
                "source_module_grouping_digest",
                "source_digest_manifest_digest",
                "source_approval_v2_digest",
                "source_staged_inventory_digest",
                "retry_execution_branch",
                "retry_execution_commit",
                "retry_pytest_passed_count",
                "retry_pytest_failed_count",
                "retry_pytest_error_count",
                "retry_pytest_skipped_count",
                "retry_pytest_first_result_authoritative",
                "root_full_regression_is_retry_evidence",
                "failed_or_errored_nodeids_count",
                "module_summary_module_count",
                "largest_module_nodeid_counts",
                "detached_integration_worktree_path",
                "detached_integration_worktree_head_commit",
            )
        },
    }


def _classification_summary() -> dict[str, Any]:
    return {
        "classification_method_v2_executed": True,
        "classification_execution_created": True,
        "classification_execution_performed": True,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_used_for_module_level_only": True,
        "failed_or_errored_nodeids_classified": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_level_grouping_generated": True,
        "module_level_grouping_reviewed": True,
        "module_summary_generated": True,
        "module_summary_reviewed": True,
        "module_summary_module_count": 29,
        "largest_module_summary_generated": True,
        "largest_module_summary_reviewed": True,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }


def _base() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1,
        "schema_version": SCHEMA_VERSION,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        "operator_review_required": True,
        **_source_fields(),
        "classification_evidence_summary": _classification_summary(),
        "known_available_detail": list(KNOWN_AVAILABLE_DETAIL),
        "known_missing_detail": list(KNOWN_MISSING_DETAIL),
        "unsupported_claims_boundary": deepcopy(UNSUPPORTED_CLAIMS_BOUNDARY),
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "staged_evidence_manifest_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "pytest_cache_tracked_in_repository": False,
        "module_grouping_source_recovery_candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL,
        "module_grouping_source_recovery_candidate_created": True,
        "module_grouping_source_recovery_candidate_ready_for_operator_review": True,
        "ready_for_module_grouping_source_recovery_operator_review": True,
        "module_grouping_source_recovery_selected": False,
        "module_grouping_source_recovery_approved": False,
        "module_grouping_source_recovery_authorized": False,
        "module_grouping_source_recovery_executed": False,
        "module_grouping_detail_recovered": False,
        "module_grouping_detail_exposed": False,
        "module_paths_recovered": False,
        "per_module_counts_recovered": False,
        "bounded_nodeid_samples_recovered": False,
        "remediation_or_method_after_v2_reentry_created": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "cache_read": False,
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
        "proposed_packages": deepcopy(PROPOSED_PACKAGES),
        "recommended_module_grouping_source_recovery_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": RECOMMENDATION_REASON,
        "future_source_recovery_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_source_recovery_plan": deepcopy(FUTURE_PLAN),
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "non_goals": list(NON_GOALS),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
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


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    blocked_packages = [
        package
        for package in candidate.get("proposed_packages", [])
        if str(package.get("status", "")).startswith("BLOCKED_")
    ]
    false_fields = {
        "source_recovery_selected_false": "module_grouping_source_recovery_selected",
        "source_recovery_approved_false": "module_grouping_source_recovery_approved",
        "source_recovery_executed_false": "module_grouping_source_recovery_executed",
        "module_grouping_detail_recovered_false": "module_grouping_detail_recovered",
        "module_paths_recovered_false": "module_paths_recovered",
        "per_module_counts_recovered_false": "per_module_counts_recovered",
        "bounded_nodeid_samples_recovered_false": "bounded_nodeid_samples_recovered",
        "remediation_or_method_reentry_created_false": "remediation_or_method_after_v2_reentry_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "retry_rerun_false": "retry_rerun_performed",
        "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed",
        "diagnostic_output_false": "diagnostic_output_captured",
        "cache_read_false": "cache_read",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_candidate",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_candidate",
        "dataset_generation_false": "dataset_generation_performed_in_candidate",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values: dict[str, tuple[Any, Any]] = {
        "source_blocked_after_v2_execution_digest_bound": (SOURCE_BLOCKED_EXECUTION_DIGEST, candidate.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (SOURCE_BLOCKED_MANIFEST_DIGEST, candidate.get("source_blocked_after_v2_manifest_digest")),
        "source_blocked_reason_bound": (source.BLOCKED_REASON_MODULE_DETAIL, candidate.get("blocked_reason")),
        "source_after_v2_approval_digest_bound": (source.SOURCE_AFTER_V2_APPROVAL_DIGEST, candidate.get("source_after_v2_approval_digest")),
        "source_after_v2_operator_review_digest_bound": (source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, candidate.get("source_after_v2_operator_review_digest")),
        "source_after_v2_candidate_digest_bound": (source.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST, candidate.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.SOURCE_RESULTS_REVIEW_V2_DIGEST, candidate.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (source.results_source.SOURCE_EXECUTION_V2_DIGEST, candidate.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.results_source.SOURCE_MODULE_GROUPING_DIGEST, candidate.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [candidate.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "classification_evidence_summary_bound": (_classification_summary(), candidate.get("classification_evidence_summary")),
        "module_count_29_bound": (29, candidate.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], candidate.get("largest_module_nodeid_counts")),
        "known_missing_detail_bound": (KNOWN_MISSING_DETAIL, candidate.get("known_missing_detail")),
        "unsupported_claims_boundary_bound": (UNSUPPORTED_CLAIMS_BOUNDARY, candidate.get("unsupported_claims_boundary")),
        "candidate_created_true": (True, candidate.get("module_grouping_source_recovery_candidate_created")),
        "candidate_ready_true": (True, candidate.get("module_grouping_source_recovery_candidate_ready_for_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, candidate.get("recommended_module_grouping_source_recovery_package")),
        "packages_present_10": (10, len(candidate.get("proposed_packages", []))),
        "blocked_packages_present_5": (5, len(blocked_packages)),
        "recommended_package_not_selected": (False, next((package.get("selected") for package in candidate.get("proposed_packages", []) if package.get("package_id") == RECOMMENDED_PACKAGE), None)),
        "successful_integration_digest_false": ([False, False], [candidate.get("successful_integration_execution_digest_generated"), candidate.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "future_requirements_defined": (FUTURE_REQUIREMENTS, candidate.get("future_source_recovery_requirements")),
        "future_plan_defined": (FUTURE_PLAN, candidate.get("future_source_recovery_plan")),
        "planned_outputs_defined": (PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": (False, candidate.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, candidate.get("pytest_cache_tracked_in_repository")),
    }
    values.update({check_id: (False, candidate.get(field)) for check_id, field in false_fields.items()})
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(item["severity"] == BLOCKER for item in failed),
        "module_grouping_source_recovery_candidate_created": True,
        "module_grouping_source_recovery_candidate_ready_for_operator_review": True,
        "recommended_module_grouping_source_recovery_package": RECOMMENDED_PACKAGE,
        "source_recovery_selected": False,
        "source_recovery_approved": False,
        "source_recovery_executed": False,
        "module_grouping_detail_recovered": False,
        "module_paths_recovered": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(
    *, source_blocked_execution: dict | None = None
) -> dict:
    """Build the candidate without reading cache or recovering module detail."""
    if source_blocked_execution is not None:
        source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
            source_blocked_execution
        )
        if source_blocked_execution.get("artifact_kind") != source.ARTIFACT_KIND_BLOCKED:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
                "source execution must be the blocked module-detail disposition"
            )
        if source_blocked_execution.get("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest") != SOURCE_BLOCKED_EXECUTION_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
                "source blocked execution digest mismatch"
            )
        if source_blocked_execution.get("marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest") != SOURCE_BLOCKED_MANIFEST_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
                "source blocked manifest digest mismatch"
            )
    candidate = _base()
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate["checklist"])
    candidate["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest"] = marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest_v1(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(candidate)
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings and every candidate-only boundary."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
            "candidate must be an object"
        )
    expected = _base()
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    checklist = _checklist(candidate)
    _expect(candidate.get("checklist"), checklist, "checklist")
    summary = _summary(checklist)
    _expect(candidate.get("summary"), summary, "summary")
    digest = candidate.get("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest_v1(candidate),
        "candidate_digest",
    )
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError(
            f"candidate has {len(failed)} failed checks"
        )
    return deepcopy(summary)


def write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(
    output_dir: str | Path,
    *,
    source_blocked_execution: dict | None = None,
) -> dict:
    """Write the deterministic candidate JSON to an explicitly supplied directory."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(
        source_blocked_execution=source_blocked_execution
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1.json"
    path.write_bytes(canonical_json_bytes(candidate) + b"\n")
    return {"path": str(path), "candidate": candidate}


def build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated candidate and its closed authority boundary."""
    validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(candidate)
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Candidate v1",
        "",
        "## Source Blocked After-v2 Execution",
        "",
        f"- Execution digest: `{candidate['source_blocked_after_v2_execution_digest']}`",
        f"- Blocked-manifest digest: `{candidate['source_blocked_after_v2_manifest_digest']}`",
        f"- Reason: `{candidate['blocked_reason']}`",
        "",
        "## Source Classification Results Review v2",
        "",
        f"- Results-review digest: `{candidate['source_results_review_v2_digest']}`",
        f"- Module-grouping digest: `{candidate['source_module_grouping_digest']}`",
        "",
        "## Retry Failure Context",
        "",
        "The authoritative retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped.",
        "",
        "## Known Available and Missing Detail",
        "",
        *[f"- Available: {item}" for item in candidate["known_available_detail"]],
        *[f"- Missing: {item}" for item in candidate["known_missing_detail"]],
        "",
        "## Candidate Scope",
        "",
        f"`{candidate['candidate_scope']}`",
        "",
        "## Candidate Philosophy",
        "",
        candidate["module_grouping_source_recovery_candidate_philosophy"],
        "",
        "## Proposed Module Grouping Source Recovery Packages",
        "",
        *[f"- `{package['package_id']}`: {package['status']}" for package in candidate["proposed_packages"]],
        "",
        "## Recommended Package",
        "",
        f"`{candidate['recommended_module_grouping_source_recovery_package']}`",
        "",
        "## Future Source Recovery Requirements",
        "",
        f"{len(FUTURE_REQUIREMENTS)} requirements are defined but grant no execution authority.",
        "",
        "## Future Source Recovery Plan",
        "",
        *[f"- {step['description']} ({step['status']})" for step in candidate["future_source_recovery_plan"]],
        "",
        "## Planned Outputs",
        "",
        *[f"- `{output['output_id']}`: {output['status']}" for output in candidate["planned_outputs"]],
        "",
        "## Non-Goals",
        "",
        *[f"- `{item}`" for item in candidate["non_goals"]],
        "",
        "## Next Chain",
        "",
        *[f"- {item}" for item in candidate["next_chain"]],
        "",
        "## Next Gates",
        "",
        *[f"- `{item}`" for item in candidate["next_gates"]],
        "",
        "## Risk Controls",
        "",
        f"{len(RISK_CONTROLS)} controls preserve the candidate-only boundary.",
        "",
        "## Authority Boundaries",
        "",
        candidate["candidate_boundary"],
        "",
        "## Checklist Summary",
        "",
        f"{candidate['summary']['passed_checks']}/{candidate['summary']['total_checks']} checks pass.",
        "",
        "## Guardrails",
        "",
        "No cache read, source recovery, diagnostics, remediation, retry, provider action, runtime use, or trading is performed.",
        "",
    ]
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN",
    "RECOMMENDED_PACKAGE",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1",
    "write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1",
    "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_markdown_v1",
]
