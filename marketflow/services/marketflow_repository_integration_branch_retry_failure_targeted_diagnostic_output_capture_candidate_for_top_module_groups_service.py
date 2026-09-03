"""Build the top-module targeted diagnostic-output capture candidate offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_V1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1"
DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_digest"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE

SOURCE_RESULTS_REVIEW_DIGEST = "d6588bfbfca55cec499d1960ab260b703dd754653473ee434b7f6ac100294956"
SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST = "2dec0b1aa1b7dfc8d3db2323ea0c48986a2f883ff8de5f9405eb480841d8bd91"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "02d83a02ccdd0e67ccd13e36575b8a654617cce3190b98ec977fd829d8bc295d"
SOURCE_PLANNING_EXECUTION_DIGEST = "846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b"
SOURCE_PRIORITIZED_PLANNING_DIGEST = "ef372ac66b165456241a53fdbe551c51fd4c9bfb65d2b6cdbc366cc464370c60"
SOURCE_PLANNING_MANIFEST_DIGEST = "cb0db6d23e2c206473f154e0ab91e7f098e37fcb524669f7c9a89af0b070ccac"
RETRY_EXECUTION_COMMIT = "ab178b65c69f0274b0abbf9c20df102d35e78d34"
SELECTED_AFTER_V2_PLANNING_PACKAGE = "PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING"
RECOMMENDED_ACTION_FROM_SOURCE = "PROCEED_TO_SEPARATELY_INVOKED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS"
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_V1"

PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS = "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS"
PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED = "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED"
PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE = "PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE"
PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT = "PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT"
PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH = "PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH"
PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY = "PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY"
PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT = "PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT"
PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE = "PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE"
PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT = "PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT"
PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION = "PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION"
PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW = "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW"
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY"
RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE = PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS

CANDIDATE_PHILOSOPHY = (
    "The reviewed after-v2 planning reentry identified Priority 1 top module groups as the highest-concentration "
    "diagnostic planning target. The next safe step is to define a controlled diagnostic-output capture method "
    "for those modules only, preserving the failed retry as authoritative while collecting bounded diagnostic "
    "information for later review. The candidate must not execute diagnostics, run pytest, infer root cause, "
    "recommend remediation, or create retry readiness."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no diagnostic command, diagnostic capture, remediation, classification, retry, results "
    "review, main merge, runtime, or trading authority is created."
)
CANDIDATE_GOAL = "Define safe future packages for targeted diagnostic output capture from the reviewed Priority 1 top module groups."

TOP_MODULES = [
    {"rank": 1, "module_path": "tests/test_marketflow_signal_or_feature_generation_results_review_service.py", "failed_or_errored_nodeid_count": 136},
    {"rank": 2, "module_path": "tests/test_post_identity_freeze_registry_inventory_approval_service.py", "failed_or_errored_nodeid_count": 131},
    {"rank": 3, "module_path": "tests/test_corporate_action_authority_plan_candidate_service.py", "failed_or_errored_nodeid_count": 122},
    {"rank": 4, "module_path": "tests/test_feature_generation_results_review_redesigned_labels_service.py", "failed_or_errored_nodeid_count": 112},
    {"rank": 5, "module_path": "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", "failed_or_errored_nodeid_count": 111},
]
PRIORITY_TIERS = [
    {"priority_tier": "PRIORITY_1_TOP_5_MODULE_GROUPS", "rank_start": 1, "rank_end": 5, "failed_or_errored_nodeid_count": 612, "status": "PLANNING_ONLY_NOT_EXECUTED", "root_cause_claimed": False},
    {"priority_tier": "PRIORITY_2_NEXT_5_MODULE_GROUPS", "rank_start": 6, "rank_end": 10, "failed_or_errored_nodeid_count": 457, "status": "PLANNING_ONLY_NOT_EXECUTED", "root_cause_claimed": False},
    {"priority_tier": "PRIORITY_3_REMAINING_MODULE_GROUPS", "rank_start": 11, "rank_end": 29, "failed_or_errored_nodeid_count": 335, "status": "PLANNING_ONLY_NOT_EXECUTED", "root_cause_claimed": False},
]
PLANNING_BUCKETS = [
    {"planning_bucket": name, "status": "PLANNING_ONLY_NOT_EXECUTED"}
    for name in (
        "TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_PLANNING",
        "EVIDENCE_ROOT_REQUIREMENT_REVIEW_PLANNING",
        "PATH_AND_CWD_ASSUMPTION_REVIEW_PLANNING",
        "DIGEST_CONSTANT_DRIFT_REVIEW_PLANNING",
        "TEST_FIXTURE_ISOLATION_REVIEW_PLANNING",
    )
]

SOURCE_BINDINGS = {
    "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
    "source_prioritized_planning_review_digest": SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
    "source_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
    "source_planning_reentry_execution_digest": SOURCE_PLANNING_EXECUTION_DIGEST,
    "source_prioritized_planning_digest": SOURCE_PRIORITIZED_PLANNING_DIGEST,
    "source_planning_digest_manifest_digest": SOURCE_PLANNING_MANIFEST_DIGEST,
    **deepcopy(source.SOURCE_BINDINGS),
}

PACKAGES = [
    {
        "package_id": PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Future execution may run a controlled targeted diagnostic capture against the five Priority 1 module files only, with bounded stdout/stderr capture, no full pytest, no retry-success claim, no cache commit, and no main-merge authority.",
        "recommended_for": "The reviewed planning output shows the top five modules contain 612 of 1,404 failed-or-errored node IDs, representing 43.58974359% of the failure/error concentration.",
    },
    {
        "package_id": PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_HIGH_CONTROL_NOT_SELECTED",
        "purpose": "Future execution may run targeted pytest diagnostics for Priority 1 modules with pytest cache provider disabled, for example with `-p no:cacheprovider`, to avoid modifying `.pytest_cache`.",
    },
    {
        "package_id": PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Future execution may capture bounded output per Priority 1 module, limiting trace volume and preventing unbounded log commits.",
    },
    {
        "package_id": PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_RECOMMENDED_FOR_FIRST_PASS",
        "purpose": "Future execution may capture diagnostics for Priority 1 and Priority 2 modules together.",
        "not_recommended_reason": "The first diagnostic capture should remain smaller and more controlled because Priority 1 alone contains 612 node IDs and five high-concentration modules.",
    },
    {
        "package_id": PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Future execution may bind an explicit operator-provided diagnostic log path if existing targeted logs are available, hash-verifiable, and bounded.",
    },
    {
        "package_id": PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY,
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": "Future execution may create only a command manifest for later diagnostic capture without running diagnostics.",
    },
    {
        "package_id": PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "The cache provides node IDs and module grouping only; it does not provide tracebacks, assertion messages, setup error details, or first-failure order.",
    },
    {
        "package_id": PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "A full pytest run would resemble a retry/full-suite execution and could confuse diagnostic evidence with retry evidence.",
    },
    {
        "package_id": PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "Root regression remains separate from detached integration retry evidence and cannot replace targeted diagnostic output.",
    },
    {
        "package_id": PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "Module concentration is planning evidence only and does not identify failure/error mechanism or root cause.",
    },
    {
        "package_id": PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "New retry remains blocked until diagnostic capture and any required remediation/method review are separately completed.",
    },
    {
        "package_id": PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY,
        "status": "BLOCKED_NOT_ALLOWED",
        "blocked_reason": "Main merge remains blocked until a future retry results review passes.",
    },
]
for _package in PACKAGES:
    _package.update({"selected": False, "approved": False, "executed": False})

FUTURE_REQUIREMENTS = {
    name: True
    for name in (
        "source_results_review_must_be_ready", "source_results_review_digest_must_be_bound",
        "source_prioritized_planning_review_digest_must_be_bound", "source_results_review_manifest_digest_must_be_bound",
        "source_planning_execution_digest_must_be_bound", "source_prioritized_planning_digest_must_be_bound",
        "source_planning_manifest_digest_must_be_bound", "source_detail_binding_results_review_must_be_bound",
        "source_complete_29_row_binding_digest_must_be_bound", "source_materialized_payload_digest_must_be_bound",
        "retry_failure_counts_must_be_bound", "priority_1_top_module_paths_must_be_bound",
        "priority_1_top_module_counts_must_be_bound", "priority_1_total_must_be_612",
        "top_10_total_must_be_1069", "module_summary_total_must_be_29",
        "failed_or_errored_nodeids_total_must_be_1404", "future_diagnostic_capture_must_target_reviewed_modules_only",
        "future_diagnostic_capture_must_not_run_full_pytest", "future_diagnostic_capture_must_not_be_treated_as_retry",
        "future_diagnostic_capture_must_capture_command_cwd_exit_code_stdout_stderr",
        "future_diagnostic_capture_must_record_python_executable", "future_diagnostic_capture_must_record_target_module_list",
        "future_diagnostic_capture_must_bound_output_volume", "future_diagnostic_capture_must_avoid_secret_capture",
        "future_diagnostic_capture_must_not_inspect_env", "future_diagnostic_capture_must_not_commit_pytest_cache",
        "future_diagnostic_capture_must_not_commit_marketflow_outputs", "future_diagnostic_capture_must_preserve_origin_main",
        "future_diagnostic_capture_must_preserve_integration_branch", "future_diagnostic_capture_must_preserve_staged_evidence",
        "future_diagnostic_capture_results_review_required", "future_remediation_or_method_candidate_requires_diagnostic_results_review",
        "future_retry_requires_separate_candidate_approval_execution_and_review", "main_merge_requires_passing_retry_results_review",
    )
}
FUTURE_PLAN = [
    "Bind this candidate and the source results-review evidence.",
    "Bind the planning execution digest, prioritized planning digest, and manifest digest.",
    "Bind the reviewed complete 29-row detail source and Priority 1 top module list.",
    "Select one diagnostic-output capture package.",
    "Verify the selected package targets only approved Priority 1 module paths unless a separate approval expands scope.",
    "Build an explicit diagnostic command template for future approval.",
    "Use the detached integration worktree as the future diagnostic working directory if approved.",
    "Use the repository virtual environment Python executable if approved.",
    "Disable or control pytest cache writes if pytest-based diagnostic capture is selected.",
    "Capture command, cwd, target modules, exit code, stdout, stderr, duration, and bounded diagnostic excerpts if approved.",
    "Preserve the failed retry as authoritative and avoid retry-success claims.",
    "Require diagnostic capture results review before any remediation/method candidate.",
    "Keep new retry, main merge, runtime, and trading closed.",
]
FUTURE_COMMAND_TEMPLATE = {
    "future_diagnostic_command_template_status": PLANNED_NOT_EXECUTED,
    "future_diagnostic_working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
    "future_diagnostic_python_executable": r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe",
    "future_diagnostic_command_template": r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=short -rA tests/test_marketflow_signal_or_feature_generation_results_review_service.py tests/test_post_identity_freeze_registry_inventory_approval_service.py tests/test_corporate_action_authority_plan_candidate_service.py tests/test_feature_generation_results_review_redesigned_labels_service.py tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    "future_diagnostic_command_is_retry": False,
    "future_diagnostic_command_is_full_pytest": False,
    "future_diagnostic_command_executed": False,
}
PLANNED_OUTPUT_IDS = [
    "targeted_diagnostic_output_capture_candidate_manifest", "priority_1_top_module_target_selection_report",
    "diagnostic_command_template_report", "diagnostic_output_capture_boundary_report",
    "diagnostic_output_capture_integrity_requirements", "diagnostic_output_volume_bound_plan",
    "diagnostic_cache_write_prevention_plan", "diagnostic_secret_avoidance_plan",
    "diagnostic_results_review_enablement_report", "remediation_or_method_candidate_enablement_report",
    "retry_gate_preservation_report", "unsupported_claims_boundary_report",
    "recommended_next_package_report", "digest_manifest",
]
NON_GOALS = [
    "do_not_select_diagnostic_package_now", "do_not_approve_diagnostic_package_now",
    "do_not_execute_diagnostic_capture_now", "do_not_run_pytest_now", "do_not_run_targeted_pytest_now",
    "do_not_run_full_pytest_now", "do_not_rerun_retry_now", "do_not_read_cache_now", "do_not_modify_cache_now",
    "do_not_rerun_planning_reentry_now", "do_not_rerun_detail_binding_now", "do_not_rerun_materialization_now",
    "do_not_rerun_source_recovery_now", "do_not_execute_remediation_now", "do_not_execute_classification_now",
    "do_not_classify_modules_again_now", "do_not_identify_first_failure_now", "do_not_identify_first_error_now",
    "do_not_claim_traceback_root_cause_now", "do_not_recommend_direct_code_remediation_now",
    "do_not_create_diagnostic_operator_review_now", "do_not_create_diagnostic_approval_now",
    "do_not_create_diagnostic_results_review_now", "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review_now", "do_not_create_integration_results_review_now",
    "do_not_mark_integration_successful", "do_not_push_integration_branch", "do_not_push_main",
    "do_not_commit_marketflow_outputs", "do_not_commit_pytest_cache", "do_not_modify_staged_evidence",
    "do_not_regenerate_evidence", "do_not_call_providers", "do_not_inspect_env",
    "do_not_accept_predictive_usefulness", "do_not_accept_profitability", "do_not_authorize_runtime",
    "do_not_authorize_trading",
]
NEXT_CHAIN = [
    "Targeted Diagnostic Output Capture Candidate Operator Review v1.",
    "Targeted Diagnostic Output Capture Approval v1, if selected.",
    "Targeted Diagnostic Output Capture Execution v1, if approved.",
    "Targeted Diagnostic Output Capture Results Review v1.",
    "Retry Failure Remediation or Method Candidate After Diagnostic Capture v1, if needed.",
    "Remediation or Method Operator Review v1, if needed.", "Remediation or Method Approval v1, if selected.",
    "Remediation or Method Execution v1, if approved.", "Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation or method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "targeted_diagnostic_output_capture_candidate_operator_review", "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved", "targeted_diagnostic_output_capture_results_review",
    "retry_failure_remediation_or_method_candidate_after_diagnostic_capture_if_needed",
    "remediation_or_method_operator_review_if_needed", "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved", "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "candidate_diagnostic_capture_does_not_select_package", "candidate_diagnostic_capture_does_not_approve_package",
    "candidate_diagnostic_capture_does_not_execute_diagnostic_capture", "candidate_diagnostic_capture_does_not_run_pytest",
    "candidate_diagnostic_capture_does_not_run_targeted_pytest", "candidate_diagnostic_capture_does_not_run_full_pytest",
    "candidate_diagnostic_capture_does_not_rerun_retry", "candidate_diagnostic_capture_does_not_read_cache",
    "candidate_diagnostic_capture_does_not_modify_cache", "candidate_diagnostic_capture_does_not_rerun_planning",
    "candidate_diagnostic_capture_does_not_rerun_detail_binding", "candidate_diagnostic_capture_does_not_rerun_materialization",
    "candidate_diagnostic_capture_does_not_rerun_source_recovery", "candidate_diagnostic_capture_does_not_execute_remediation",
    "candidate_diagnostic_capture_does_not_execute_classification", "candidate_diagnostic_capture_does_not_classify_modules_again",
    "candidate_diagnostic_capture_does_not_identify_first_failure", "candidate_diagnostic_capture_does_not_identify_first_error",
    "candidate_diagnostic_capture_does_not_claim_traceback_root_cause", "candidate_diagnostic_capture_does_not_recommend_direct_code_remediation",
    "candidate_diagnostic_capture_does_not_create_diagnostic_operator_review", "candidate_diagnostic_capture_does_not_create_diagnostic_approval",
    "candidate_diagnostic_capture_does_not_create_diagnostic_results_review", "candidate_diagnostic_capture_does_not_create_new_retry_candidate",
    "candidate_diagnostic_capture_does_not_create_retry_results_review", "candidate_diagnostic_capture_does_not_create_integration_results_review",
    "candidate_diagnostic_capture_does_not_mark_integration_successful", "candidate_diagnostic_capture_does_not_generate_successful_integration_digest",
    "candidate_diagnostic_capture_does_not_push_integration_branch", "candidate_diagnostic_capture_does_not_push_main",
    "candidate_diagnostic_capture_does_not_delete_integration_branch", "candidate_diagnostic_capture_does_not_delete_worktree",
    "candidate_diagnostic_capture_does_not_force_push", "candidate_diagnostic_capture_does_not_prune_remotes",
    "candidate_diagnostic_capture_does_not_modify_tags", "candidate_diagnostic_capture_does_not_modify_staged_evidence",
    "candidate_diagnostic_capture_does_not_regenerate_evidence", "candidate_diagnostic_capture_does_not_call_providers",
    "candidate_diagnostic_capture_does_not_inspect_env", "candidate_diagnostic_capture_does_not_acquire_market_data",
    "candidate_diagnostic_capture_does_not_regenerate_dataset", "candidate_diagnostic_capture_does_not_recompute_metrics",
    "candidate_diagnostic_capture_does_not_train_models", "candidate_diagnostic_capture_does_not_score_strategy",
    "candidate_diagnostic_capture_does_not_generate_recommendations", "candidate_diagnostic_capture_does_not_accept_predictive_usefulness",
    "candidate_diagnostic_capture_does_not_accept_profitability", "candidate_diagnostic_capture_does_not_authorize_runtime",
    "candidate_diagnostic_capture_does_not_authorize_broker_execution", "candidate_output_is_planning_only_not_diagnostic_execution",
    "future_diagnostic_capture_is_not_retry_success", "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation", "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid", "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_operator_review_required",
    "separate_approval_required_before_diagnostic_execution", "separate_results_review_required_after_diagnostic_capture",
    "separate_remediation_or_method_candidate_required_after_diagnostic_review", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "targeted_diagnostic_output_capture_candidate_created",
    "targeted_diagnostic_output_capture_candidate_ready_for_operator_review",
    "priority_1_top_module_groups_bound_for_candidate", "diagnostic_capture_packages_defined",
    "future_diagnostic_capture_requirements_defined", "future_diagnostic_capture_plan_defined",
    "ready_for_targeted_diagnostic_output_capture_candidate_operator_review",
]
FALSE_FIELDS = [
    "diagnostic_capture_package_selected", "diagnostic_capture_package_approved", "diagnostic_capture_package_authorized",
    "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created", "diagnostic_output_captured",
    "diagnostic_command_executed", "diagnostic_method_executed", "ready_for_diagnostic_capture_approval",
    "ready_for_diagnostic_capture_execution", "ready_for_retry_candidate", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "cache_read_in_candidate", "cache_modified_in_candidate", "planning_reentry_rerun_performed",
    "detail_binding_reattempt_rerun_performed", "materialization_execution_rerun_performed",
    "source_recovery_rerun_performed", "module_grouping_recovered_in_candidate", "retry_rerun_performed",
    "full_pytest_performed", "targeted_pytest_performed", "code_remediation_executed",
    "evidence_remediation_executed", "classification_execution_performed_in_candidate", "failure_modules_classified",
    "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified",
    "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed",
    "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
    "evidence_regenerated", "provider_requests_made_in_candidate", "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError(ValueError):
    """Raised when the candidate or its source bindings violate the contract."""


def _expected_source_review() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND,
        "review_status": source.REVIEW_STATUS,
        "review_scope": source.REVIEW_SCOPE,
        source.REVIEW_DIGEST_KEY: SOURCE_RESULTS_REVIEW_DIGEST,
        source.PLANNING_REVIEW_DIGEST_KEY: SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
        source.REVIEW_MANIFEST_DIGEST_KEY: SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "recommended_action": RECOMMENDED_ACTION_FROM_SOURCE,
        "ready_for_targeted_diagnostic_output_capture_candidate": True,
        "ready_for_retry_candidate": False,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "top_five_module_paths": [item["module_path"] for item in TOP_MODULES],
        "largest_module_nodeid_counts": [item["failed_or_errored_nodeid_count"] for item in TOP_MODULES],
        "top_5_count_sum": 612,
        "top_10_count_sum": 1069,
    }


def _bind_source_review(value: dict | None) -> dict[str, Any]:
    expected = _expected_source_review()
    if value is None:
        return expected
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("source results review must be an object")
    for field, required in expected.items():
        if value.get(field) != required:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError(f"source results review {field} mismatch")
    return deepcopy(dict(value))


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


CHECKLIST_ALIASES = {
    "source_planning_execution_digest_bound": "source_planning_reentry_execution_digest",
    "source_detail_binding_results_review_digest_bound": "source_detail_binding_reattempt_results_review_digest",
    "source_detail_binding_results_review_manifest_digest_bound": "source_detail_binding_reattempt_results_review_manifest_digest",
    "source_detail_binding_reattempt_manifest_digest_bound": "source_detail_binding_reattempt_digest_manifest_digest",
    "source_materialization_results_review_digest_bound": "source_complete_29_row_materialization_results_review_digest",
    "source_materialized_payload_review_digest_bound": "source_complete_29_row_materialized_payload_review_digest",
    "source_materialization_results_review_manifest_digest_bound": "source_complete_29_row_materialization_results_review_manifest_digest",
    "source_materialization_execution_digest_bound": "source_complete_29_row_materialization_execution_digest",
    "source_materialized_payload_digest_bound": "source_complete_29_row_materialized_payload_digest",
    "source_materialization_digest_manifest_digest_bound": "source_complete_29_row_materialization_digest_manifest_digest",
    "source_detail_binding_approval_digest_bound": "source_detail_exposure_or_binding_approval_digest",
    "source_prior_blocked_detail_binding_execution_digest_bound": "source_detail_exposure_or_binding_execution_blocked_digest",
    "source_prior_blocked_detail_binding_reason_bound": "source_detail_exposure_or_binding_execution_blocked_reason",
    "source_materialization_approval_digest_bound": "source_complete_29_row_materialization_approval_digest",
    "source_materialization_operator_review_digest_bound": "source_complete_29_row_materialization_operator_review_digest",
    "source_materialization_candidate_digest_bound": "source_complete_29_row_materialization_candidate_digest",
    "source_execution_failure_diagnosis_digest_bound": "source_detail_exposure_or_binding_execution_failure_diagnosis_digest",
    "source_primary_failure_class_bound": "primary_failure_class",
    "source_recovery_results_review_digest_bound": "source_module_grouping_source_recovery_results_review_digest",
    "source_recovery_detail_digest_bound": "source_module_grouping_source_recovery_detail_digest",
}
FALSE_CHECKLIST_ALIASES = {
    "diagnostic_capture_execution_false": "diagnostic_capture_execution_performed",
    "diagnostic_capture_results_review_false": "diagnostic_capture_results_review_created",
    "planning_reentry_rerun_false": "planning_reentry_rerun_performed",
    "detail_binding_reattempt_rerun_false": "detail_binding_reattempt_rerun_performed",
    "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
    "source_recovery_rerun_false": "source_recovery_rerun_performed",
    "targeted_pytest_false": "targeted_pytest_performed", "retry_rerun_false": "retry_rerun_performed",
    "full_pytest_false": "full_pytest_performed", "code_remediation_false": "code_remediation_executed",
    "evidence_remediation_false": "evidence_remediation_executed",
    "classification_execution_false": "classification_execution_performed_in_candidate",
    "integration_success_false": "integration_execution_successful",
    "successful_integration_digest_false": "successful_integration_execution_digest_generated",
    "main_push_false": "main_push_performed", "origin_main_modified_false": "origin_main_modified_by_this_task",
    "provider_requests_false": "provider_requests_made_in_candidate",
    "market_data_acquisition_false": "market_data_acquisition_performed_in_candidate",
    "dataset_generation_false": "dataset_generation_performed_in_candidate",
    "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
    "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
    "recommendations_false": "trade_recommendations_generated",
}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    mappings: list[tuple[str, Any, Any]] = []
    for field, expected in SOURCE_BINDINGS.items():
        mappings.append((f"{field}_bound", expected, candidate.get(field)))
    mappings.extend([
        ("source_selected_after_v2_planning_package_bound", SELECTED_AFTER_V2_PLANNING_PACKAGE, candidate.get("selected_after_v2_planning_package")),
        ("retry_execution_commit_bound", RETRY_EXECUTION_COMMIT, candidate.get("retry_execution_commit")),
        ("retry_failure_counts_bound", {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, candidate.get("retry_failure_context", {}).get("counts")),
        ("source_review_ready_bound", source.REVIEW_STATUS, candidate.get("source_results_review_summary", {}).get("status")),
        ("ready_for_targeted_diagnostic_candidate_from_source_true", True, candidate.get("source_results_review_summary", {}).get("ready_for_targeted_diagnostic_output_capture_candidate")),
        ("ready_for_retry_candidate_from_source_false", False, candidate.get("source_results_review_summary", {}).get("ready_for_retry_candidate")),
        ("priority_1_top_module_paths_bound", [item["module_path"] for item in TOP_MODULES], [item.get("module_path") for item in candidate.get("priority_1_top_module_groups", [])]),
        ("priority_1_top_module_counts_bound", [136, 131, 122, 112, 111], [item.get("failed_or_errored_nodeid_count") for item in candidate.get("priority_1_top_module_groups", [])]),
        ("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")),
        ("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
        ("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")),
        ("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
        ("planning_buckets_bound", PLANNING_BUCKETS, candidate.get("planning_buckets_summary")),
        ("candidate_created_true", True, candidate.get("targeted_diagnostic_output_capture_candidate_created")),
        ("candidate_ready_true", True, candidate.get("targeted_diagnostic_output_capture_candidate_ready_for_operator_review")),
        ("diagnostic_capture_packages_defined_true", True, candidate.get("diagnostic_capture_packages_defined")),
        ("future_requirements_defined_true", True, candidate.get("future_diagnostic_capture_requirements_defined")),
        ("future_plan_defined_true", True, candidate.get("future_diagnostic_capture_plan_defined")),
        ("future_command_template_defined_not_executed", PLANNED_NOT_EXECUTED, candidate.get("future_diagnostic_command_template", {}).get("future_diagnostic_command_template_status")),
        ("recommended_package_defined", RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE, candidate.get("recommended_targeted_diagnostic_capture_package")),
        ("recommended_package_not_selected", False, candidate.get("recommended_package", {}).get("selected")),
        ("packages_present_12", 12, len(candidate.get("proposed_diagnostic_capture_packages", []))),
        ("blocked_packages_present_6", 6, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_diagnostic_capture_packages", []))),
    ])
    for field in FALSE_FIELDS:
        mappings.append((f"{field}_false", False, candidate.get(field)))
    for check_id, field in CHECKLIST_ALIASES.items():
        mappings.append((check_id, SOURCE_BINDINGS[field], candidate.get(field)))
    for check_id, field in FALSE_CHECKLIST_ALIASES.items():
        mappings.append((check_id, False, candidate.get(field)))
    mappings.extend([
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        ("planned_outputs_defined", PLANNED_OUTPUT_IDS, [item.get("output_id") for item in candidate.get("planned_outputs", [])]),
        ("non_goals_defined", NON_GOALS, candidate.get("non_goals")),
        ("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        ("no_tracked_marketflow_files", False, candidate.get("marketflow_outputs_committed")),
        ("no_tracked_pytest_cache_files", False, candidate.get("pytest_cache_committed")),
    ])
    return [_check(*item) for item in mappings]


def _summary(candidate: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(item["status"] == PASS for item in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": failed, "blocker_count": failed,
        **{field: candidate.get(field) for field in TRUE_FIELDS},
        **{field: candidate.get(field) for field in (
            "diagnostic_capture_package_selected", "diagnostic_capture_package_approved", "diagnostic_capture_package_authorized",
            "diagnostic_capture_execution_performed", "diagnostic_capture_results_review_created", "diagnostic_output_captured",
            "diagnostic_command_executed", "targeted_pytest_performed", "retry_rerun_performed", "full_pytest_performed",
            "ready_for_diagnostic_capture_approval", "ready_for_diagnostic_capture_execution", "ready_for_retry_candidate",
            "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        )},
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", DIGEST_KEY, "candidate_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(
    *, source_results_review: dict | None = None,
) -> dict:
    """Create the candidate from committed evidence without executing diagnostics."""

    bound_source = _bind_source_review(source_results_review)
    recommendation = {
        "package_id": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "selected": False,
        "reason": "The reviewed planning output confirms that the Priority 1 top five module groups contain 612 of 1,404 failed-or-errored node IDs. A targeted diagnostic-output capture candidate focused on these modules is the safest next step before any remediation method or new retry candidate.",
    }
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_artifact_kind": source.ARTIFACT_KIND,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_status": source.REVIEW_STATUS,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_scope": source.REVIEW_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        "recommended_action_from_source_review": RECOMMENDED_ACTION_FROM_SOURCE,
        "selected_after_v2_planning_package": SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {
            "branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
            "working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
            "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "source_results_review_summary": {
            "artifact_kind": bound_source["artifact_kind"], "status": bound_source["review_status"],
            "scope": bound_source["review_scope"], "results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
            "prioritized_planning_review_digest": SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
            "manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
            "ready_for_targeted_diagnostic_output_capture_candidate": True, "ready_for_retry_candidate": False,
        },
        "source_planning_reentry_summary": {
            "execution_digest": SOURCE_PLANNING_EXECUTION_DIGEST,
            "prioritized_planning_digest": SOURCE_PRIORITIZED_PLANNING_DIGEST,
            "manifest_digest": SOURCE_PLANNING_MANIFEST_DIGEST,
            "selected_package": SELECTED_AFTER_V2_PLANNING_PACKAGE,
            "status": "REVIEWED_COMPLETE_DETAIL_PLANNING_SOURCE_BOUND_NOT_RERUN",
        },
        "reviewed_complete_29_row_detail_summary": {
            "row_count": 29, "failed_or_errored_nodeids_count": 1404,
            "binding_digest": SOURCE_BINDINGS["source_complete_29_row_binding_digest"],
            "materialized_payload_digest": SOURCE_BINDINGS["source_complete_29_row_materialized_payload_digest"],
            "status": "REVIEWED_SOURCE_BOUND_NOT_RERUN",
        },
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_1_total_nodeids": 612, "priority_tier_1_count_sum": 612,
        "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        "priority_1_top_module_groups": deepcopy(TOP_MODULES), "priority_tier_summary": deepcopy(PRIORITY_TIERS),
        "planning_buckets_summary": deepcopy(PLANNING_BUCKETS),
        "candidate_philosophy": CANDIDATE_PHILOSOPHY, "candidate_boundary": CANDIDATE_BOUNDARY,
        "candidate_goal": CANDIDATE_GOAL, "proposed_diagnostic_capture_packages": deepcopy(PACKAGES),
        "recommended_targeted_diagnostic_capture_package": RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommended_package": recommendation,
        "future_diagnostic_capture_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_diagnostic_capture_plan": {"status": PLANNED_NOT_EXECUTED, "steps": list(FUTURE_PLAN)},
        "future_diagnostic_command_template": deepcopy(FUTURE_COMMAND_TEMPLATE),
        "planned_outputs": [{"output_id": item, "status": PLANNED_NOT_GENERATED} for item in PLANNED_OUTPUT_IDS],
        "non_goals": list(NON_GOALS), "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    candidate.update({field: True for field in TRUE_FIELDS})
    candidate.update({field: False for field in FALSE_FIELDS})
    candidate["digest_manifest"] = {
        "source_results_review": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_prioritized_planning_review": SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
        "source_results_review_manifest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_planning_execution": SOURCE_PLANNING_EXECUTION_DIGEST,
        "source_prioritized_planning": SOURCE_PRIORITIZED_PLANNING_DIGEST,
        "source_planning_manifest": SOURCE_PLANNING_MANIFEST_DIGEST,
        "priority_1_top_module_groups": semantic_digest(TOP_MODULES),
        "proposed_diagnostic_capture_packages": semantic_digest(PACKAGES),
        "future_diagnostic_capture_requirements": semantic_digest(FUTURE_REQUIREMENTS),
        "future_diagnostic_capture_plan": semantic_digest(FUTURE_PLAN),
    }
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate, candidate["checklist"])
    candidate[DIGEST_KEY] = _candidate_digest(candidate)
    candidate["candidate_digest"] = candidate[DIGEST_KEY]
    validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(
    candidate: dict,
) -> dict:
    """Reject source drift, incomplete planning content, or opened authority."""

    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("candidate must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True, "operator_review_required": True,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_artifact_kind": source.ARTIFACT_KIND,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_status": source.REVIEW_STATUS,
        "source_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_scope": source.REVIEW_SCOPE,
        "selected_after_v2_planning_package": SELECTED_AFTER_V2_PLANNING_PACKAGE,
        "recommended_action_from_source_review": RECOMMENDED_ACTION_FROM_SOURCE,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError(f"{field} mismatch")
    if candidate.get("retry_failure_context", {}).get("counts") != {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("retry failure counts mismatch")
    if candidate.get("source_results_review_summary") != {
        "artifact_kind": source.ARTIFACT_KIND, "status": source.REVIEW_STATUS, "scope": source.REVIEW_SCOPE,
        "results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "prioritized_planning_review_digest": SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
        "manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "ready_for_targeted_diagnostic_output_capture_candidate": True, "ready_for_retry_candidate": False,
    }:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("source results review summary mismatch")
    expected_scalars = {
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111], "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114", "priority_1_total_nodeids": 612,
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        "priority_1_top_module_groups": TOP_MODULES, "priority_tier_summary": PRIORITY_TIERS,
        "planning_buckets_summary": PLANNING_BUCKETS, "candidate_philosophy": CANDIDATE_PHILOSOPHY,
        "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
    }
    for field, expected in expected_scalars.items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError(f"{field} mismatch")
    if any(candidate.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("required candidate flag missing")
    if any(candidate.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("closed boundary opened")
    if candidate.get("predictive_usefulness") != NOT_ACCEPTED or candidate.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("acceptance boundary changed")
    if candidate.get("runtime_use") != NOT_AUTHORIZED or candidate.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("runtime boundary changed")
    packages = candidate.get("proposed_diagnostic_capture_packages")
    if packages != PACKAGES or len(packages) != 12 or sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) != 6:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("proposed packages mismatch")
    if any(item.get("selected") or item.get("approved") or item.get("executed") for item in packages):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("package authority opened")
    recommendation = candidate.get("recommended_package")
    if not isinstance(recommendation, Mapping) or recommendation.get("package_id") != RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE or recommendation.get("selected") is not False:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("recommended package mismatch")
    if candidate.get("recommended_targeted_diagnostic_capture_package") != RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("recommended package missing")
    if candidate.get("future_diagnostic_capture_requirements") != FUTURE_REQUIREMENTS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("future requirements mismatch")
    if candidate.get("future_diagnostic_capture_plan") != {"status": PLANNED_NOT_EXECUTED, "steps": FUTURE_PLAN}:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("future plan mismatch")
    if candidate.get("future_diagnostic_command_template") != FUTURE_COMMAND_TEMPLATE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("future command template mismatch")
    outputs = candidate.get("planned_outputs")
    if not isinstance(outputs, list) or [item.get("output_id") for item in outputs] != PLANNED_OUTPUT_IDS or any(item.get("status") != PLANNED_NOT_GENERATED for item in outputs):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("planned outputs mismatch")
    if candidate.get("non_goals") != NON_GOALS or candidate.get("next_chain") != NEXT_CHAIN or candidate.get("next_gates") != NEXT_GATES:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("governance sequence mismatch")
    if candidate.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("risk controls mismatch")
    expected_manifest = {
        "source_results_review": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_prioritized_planning_review": SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST,
        "source_results_review_manifest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_planning_execution": SOURCE_PLANNING_EXECUTION_DIGEST,
        "source_prioritized_planning": SOURCE_PRIORITIZED_PLANNING_DIGEST,
        "source_planning_manifest": SOURCE_PLANNING_MANIFEST_DIGEST,
        "priority_1_top_module_groups": semantic_digest(TOP_MODULES),
        "proposed_diagnostic_capture_packages": semantic_digest(PACKAGES),
        "future_diagnostic_capture_requirements": semantic_digest(FUTURE_REQUIREMENTS),
        "future_diagnostic_capture_plan": semantic_digest(FUTURE_PLAN),
    }
    if candidate.get("digest_manifest") != expected_manifest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("digest manifest mismatch")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("checklist mismatch")
    summary = _summary(candidate, checklist)
    if candidate.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("summary mismatch")
    digest = candidate.get(DIGEST_KEY)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _candidate_digest(candidate):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("candidate digest mismatch")
    if candidate.get("candidate_digest") != digest:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("candidate digest alias mismatch")
    return {
        "artifact_kind": candidate["artifact_kind"], "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"], "candidate_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(
    output_dir: str | Path, *, source_results_review: dict | None = None,
) -> dict:
    """Write the deterministic JSON artifact outside protected runtime directories."""

    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("protected output directory")
    candidate = build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(
        source_results_review=source_results_review
    )
    path = output / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError("output exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"], "candidate_digest": candidate[DIGEST_KEY],
        "payload_sha256": sha256_bytes(payload),
    }


def build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_markdown_v1(
    candidate: dict,
) -> str:
    """Render the validated governance candidate as Markdown."""

    validation = validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(candidate)
    sections = [
        ("Source Remediation or Method Results Review", [SOURCE_RESULTS_REVIEW_DIGEST, SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST, SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST]),
        ("Source Planning Reentry with Complete Detail", [SOURCE_PLANNING_EXECUTION_DIGEST, SOURCE_PRIORITIZED_PLANNING_DIGEST, SOURCE_PLANNING_MANIFEST_DIGEST]),
        ("Source Detail Binding Results Review", [SOURCE_BINDINGS["source_detail_binding_reattempt_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_binding_digest"]]),
        ("Source Materialization Results Review", [SOURCE_BINDINGS["source_complete_29_row_materialization_results_review_digest"], SOURCE_BINDINGS["source_complete_29_row_materialized_payload_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the failed retry remains authoritative."]),
        ("Candidate Scope", [CANDIDATE_SCOPE]),
        ("Reviewed Priority Planning Facts", ["29 modules; 1,404 failed-or-errored node IDs; Priority 1 contains 612 (43.58974359%)."]),
        ("Priority 1 Top Module Groups", [f"{item['rank']}. {item['module_path']}: {item['failed_or_errored_nodeid_count']}" for item in TOP_MODULES]),
        ("Planning Buckets", [f"{item['planning_bucket']}: {item['status']}" for item in PLANNING_BUCKETS]),
        ("Candidate Philosophy", [CANDIDATE_PHILOSOPHY, CANDIDATE_BOUNDARY, CANDIDATE_GOAL]),
        ("Proposed Diagnostic Capture Packages", [f"{item['package_id']}: {item['status']}" for item in PACKAGES]),
        ("Recommended Package", [RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE, candidate["recommended_package"]["reason"]]),
        ("Future Diagnostic Capture Requirements", list(FUTURE_REQUIREMENTS)),
        ("Future Diagnostic Capture Plan", list(FUTURE_PLAN)),
        ("Future Diagnostic Command Template", [FUTURE_COMMAND_TEMPLATE["future_diagnostic_command_template_status"], FUTURE_COMMAND_TEMPLATE["future_diagnostic_command_template"]]),
        ("Planned Outputs", list(PLANNED_OUTPUT_IDS)), ("Non-Goals", list(NON_GOALS)),
        ("Next Chain", list(NEXT_CHAIN)), ("Next Gates", list(NEXT_GATES)), ("Risk Controls", list(RISK_CONTROLS)),
        ("Authority Boundaries", [CANDIDATE_BOUNDARY, "Predictive usefulness and profitability are not accepted; runtime and broker execution are not authorized."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["This candidate defines future choices only and executes no diagnostic command, pytest run, retry, remediation, provider, runtime, or trading action."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Candidate for Top Module Groups v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "CANDIDATE_STATUS", "CANDIDATE_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS",
    "PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_WITH_CACHE_DISABLED",
    "PACKAGE_CAPTURE_BOUNDED_FIRST_N_FAILURE_OUTPUT_PER_PRIORITY_1_MODULE",
    "PACKAGE_CAPTURE_PRIORITY_1_AND_PRIORITY_2_DIAGNOSTIC_OUTPUT",
    "PACKAGE_OPERATOR_PROVIDES_EXISTING_TARGETED_DIAGNOSTIC_LOG_PATH", "PACKAGE_CREATE_DIAGNOSTIC_COMMAND_MANIFEST_ONLY",
    "PACKAGE_USE_PYTEST_LASTFAILED_CACHE_AS_DIAGNOSTIC_OUTPUT", "PACKAGE_RUN_FULL_PYTEST_AS_DIAGNOSTIC_CAPTURE",
    "PACKAGE_ACCEPT_ROOT_REGRESSION_AS_DIAGNOSTIC_OUTPUT", "PACKAGE_DIRECT_REMEDIATION_FROM_MODULE_CONCENTRATION",
    "PACKAGE_NEW_RETRY_WITHOUT_DIAGNOSTIC_CAPTURE_REVIEW", "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY",
    "RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1",
    "write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1",
    "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_markdown_v1",
]
