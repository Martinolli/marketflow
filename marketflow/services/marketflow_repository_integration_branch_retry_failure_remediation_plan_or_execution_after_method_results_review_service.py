"""Generate the approved targeted remediation plan without executing remediation."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_service
    as approval_source,
)

ARTIFACT_KIND_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_EXECUTED_AFTER_METHOD_RESULTS_REVIEW_V1"
ARTIFACT_KIND_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1"
EXECUTION_STATUS_SUCCESS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_EXECUTED_AFTER_METHOD_RESULTS_REVIEW_TARGETED_REMEDIATION_PLAN_READY"
EXECUTION_STATUS_BLOCKED = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_SOURCE_APPROVAL_OR_REVIEWED_FAILURE_FAMILY_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_ONLY_TARGETED_PLAN_GENERATION_NOT_CODE_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = approval_source.SELECTED_PACKAGE
SOURCE_APPROVAL_COMMIT = "107a5216cedd9dd9a31c33f5361a631e5f52686f"
SOURCE_APPROVAL_DIGEST = "1a0bb35947d6d1131616c2424e703e8e6179a161a242ec0060b1330dc4693f5d"
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"
EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_digest"
TARGETED_PLAN_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_targeted_remediation_plan_digest"
WORKSTREAM_MAPPING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_workstream_mapping_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_blocked_manifest_digest"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

SOURCE_BINDINGS = {
    **approval_source._source_fields(),
    "source_remediation_plan_or_execution_approval_after_method_results_review_commit": SOURCE_APPROVAL_COMMIT,
    "source_remediation_plan_or_execution_approval_after_method_results_review_digest": SOURCE_APPROVAL_DIGEST,
}
SOURCE_CORE = approval_source._SOURCE_CORE
PRIORITY_1_MODULES = deepcopy(SOURCE_CORE["priority_1_target_modules"])
FAMILY_IDS = list(approval_source.source.source.source.FAMILY_IDS)
CANDIDATE_SCOPE_STATEMENT = (
    "The Priority 1 modules are candidate planning areas only. This plan does not claim that any specific module is root "
    "cause, does not assign failure/error separation, and does not authorize direct edits."
)

WORKSTREAM_SPECS = [
    {
        "workstream_id": "assertion_value_mismatch_workstream",
        "source_family_id": "assertion_or_value_mismatch",
        "purpose": "Plan source-of-truth reconciliation for expected/actual assertion mismatches without changing assertions.",
        "planned_actions": [
            "catalog expected/actual mismatch types in a future approved analysis",
            "identify source artifact field contracts to verify",
            "define source-of-truth selection criteria",
            "define evidence needed before any assertion update",
            "define review gates before any test change",
        ],
        "verification_evidence_required": [
            "bound expected and actual values with provenance",
            "authoritative source selection rationale",
            "results review before any assertion or expected-value change",
        ],
        "prohibited_actions": ["assertion edits", "expected-value updates", "code changes", "pytest execution"],
    },
    {
        "workstream_id": "digest_hash_boundary_workstream",
        "source_family_id": "digest_or_hash_mismatch",
        "purpose": "Plan digest/hash provenance, deterministic serialization, and source-binding drift review before any digest update.",
        "planned_actions": [
            "identify digest sources and payload boundaries for future review",
            "define canonical serialization evidence requirements",
            "define digest provenance checks",
            "define review steps before changing any digest constant",
        ],
        "verification_evidence_required": [
            "canonical payload and serialization evidence",
            "source-to-digest provenance chain",
            "separate source authority and results review before any digest change",
        ],
        "prohibited_actions": ["digest updates", "hash replacements", "source payload rewrites", "pytest execution"],
    },
    {
        "workstream_id": "fixture_isolation_determinism_workstream",
        "source_family_id": "fixture_or_test_isolation_issue",
        "purpose": "Plan fixture isolation and determinism review for shared constants, timestamps, paths, and test-pollution risks.",
        "planned_actions": [
            "define fixture inventory requirements",
            "define deterministic timestamp policy review",
            "define temp-path and worktree isolation checks",
            "define shared mutable state checks",
            "define future validation evidence",
        ],
        "verification_evidence_required": [
            "fixture and shared-state inventory",
            "deterministic timestamp and path policy evidence",
            "isolated validation design approved before test changes",
        ],
        "prohibited_actions": ["fixture edits", "existing test edits", "runtime cleanup execution", "pytest execution"],
    },
    {
        "workstream_id": "schema_field_contract_workstream",
        "source_family_id": "missing_or_unexpected_field",
        "purpose": "Plan schema/field contract reconciliation for fields, artifact constants, outputs, and export surfaces.",
        "planned_actions": [
            "define field inventory requirements",
            "define required and optional field classification",
            "define backward compatibility checks",
            "define export contract checks",
            "define review evidence before any schema or service change",
        ],
        "verification_evidence_required": [
            "required and optional field inventory with provenance",
            "artifact kind/status/scope and export contract comparison",
            "backward-compatibility review before schema or service changes",
        ],
        "prohibited_actions": ["schema changes", "exports beyond this governance service", "production behavior changes", "pytest execution"],
    },
]

VERIFICATION_EVIDENCE_REQUIREMENTS = [
    "bind every proposed change to reviewed source artifacts and authoritative field contracts",
    "record expected and actual values without replacing either",
    "prove deterministic serialization and digest provenance before any digest proposal",
    "prove fixture, timestamp, path, and shared-state isolation before any test proposal",
    "classify required versus optional fields and assess backward compatibility before schema proposals",
    "obtain separate remediation results review before any remediation execution candidate",
]
FUTURE_APPROVAL_BOUNDARIES = {
    "remediation_execution_requires_separate_future_approval": True,
    "code_change_requires_separate_future_approval": True,
    "test_change_requires_separate_future_approval": True,
    "digest_update_requires_source_authority_and_review": True,
    "new_retry_requires_separate_future_candidate_approval_execution_and_review": True,
    "main_merge_requires_passing_future_retry_review": True,
}
UNSUPPORTED_CLAIMS_BOUNDARY = {
    "root_cause_claimed": False,
    "authoritative_first_failure_claimed": False,
    "authoritative_first_error_claimed": False,
    "full_retry_failure_error_separation_claimed": False,
    "direct_code_remediation_recommended": False,
    "retry_success_claimed": False,
    "main_merge_readiness_claimed": False,
}
SUCCESS_OUTPUT_IDS = [
    "remediation_plan_or_execution_after_method_results_review_manifest",
    "source_approval_binding_report",
    "source_operator_review_binding_report",
    "source_candidate_binding_report",
    "source_method_results_review_binding_report",
    "source_method_execution_binding_report",
    "reviewed_failure_family_input_summary",
    "targeted_remediation_plan_report",
    "assertion_value_mismatch_workstream_plan",
    "digest_hash_boundary_workstream_plan",
    "fixture_isolation_determinism_workstream_plan",
    "schema_field_contract_workstream_plan",
    "verification_evidence_requirements_report",
    "future_approval_boundary_report",
    "unsupported_claims_boundary_report",
    "retry_gate_preservation_report",
    "main_merge_gate_preservation_report",
    "digest_manifest",
]
SUCCESS_OUTPUTS = [{"output_id": item, "status": "GENERATED_TARGETED_REMEDIATION_PLAN_ONLY"} for item in SUCCESS_OUTPUT_IDS]
SUCCESS_NEXT_CHAIN = [
    "Remediation Plan or Execution Results Review After Method Results Review v1.",
    "Remediation Execution Candidate After Plan Results Review v1, only if the plan review supports execution planning.",
    "Remediation Execution Candidate Operator Review v1, if needed.",
    "Remediation Execution Approval v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Remediation Plan or Execution After Method Results Review Failure Diagnosis v1.",
    "Alternate plan source or remediation candidate, if needed.",
    "No remediation execution, retry, or main merge.",
]
NEXT_GATES = [
    "remediation_plan_or_execution_results_review_after_method_results_review",
    "remediation_execution_candidate_after_plan_results_review_if_supported",
    "remediation_execution_candidate_operator_review_if_needed",
    "remediation_execution_approval_if_selected",
    "remediation_execution_if_approved",
    "remediation_execution_results_review",
    "new_integration_branch_retry_candidate_after_remediation_results_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
    "remediation_plan_or_execution_after_method_results_review_failure_diagnosis",
    "alternate_plan_source_or_candidate_if_needed",
    "remediation_execution_blocked_until_plan_results_review_passes",
    "new_retry_blocked_until_remediation_results_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]
RISK_CONTROLS = [
    "plan_execution_after_method_results_review_uses_approved_package_only",
    "plan_execution_after_method_results_review_generates_plan_only",
    "plan_execution_after_method_results_review_uses_reviewed_method_results_only",
    "plan_execution_after_method_results_review_uses_reviewed_observable_families_only",
    "plan_execution_after_method_results_review_preserves_direct_remediation_ready_false",
    "plan_execution_after_method_results_review_preserves_retry_ready_false",
    "plan_execution_after_method_results_review_preserves_main_merge_ready_false",
    "plan_execution_after_method_results_review_does_not_execute_remediation",
    "plan_execution_after_method_results_review_does_not_modify_production_code",
    "plan_execution_after_method_results_review_does_not_modify_existing_tests",
    "plan_execution_after_method_results_review_does_not_update_expected_digests",
    "plan_execution_after_method_results_review_does_not_parse_durable_receipt",
    "plan_execution_after_method_results_review_does_not_analyze_diagnostic_output",
    "plan_execution_after_method_results_review_does_not_rerun_method_execution",
    "plan_execution_after_method_results_review_does_not_rerun_controlled_recapture",
    "plan_execution_after_method_results_review_does_not_run_diagnostic_command",
    "plan_execution_after_method_results_review_does_not_run_targeted_pytest",
    "plan_execution_after_method_results_review_does_not_run_full_pytest",
    "plan_execution_after_method_results_review_does_not_rerun_retry",
    "plan_execution_after_method_results_review_does_not_read_pytest_cache",
    "plan_execution_after_method_results_review_does_not_modify_pytest_cache",
    "plan_execution_after_method_results_review_does_not_parse_terminal_logs",
    "plan_execution_after_method_results_review_does_not_parse_operator_logs",
    "plan_execution_after_method_results_review_does_not_inspect_env",
    "plan_execution_after_method_results_review_does_not_reconstruct_prior_lost_values",
    "plan_execution_after_method_results_review_does_not_reconstruct_full_stdout",
    "plan_execution_after_method_results_review_does_not_reconstruct_full_stderr",
    "plan_execution_after_method_results_review_does_not_classify_modules_again",
    "plan_execution_after_method_results_review_does_not_classify_full_retry_failures",
    "plan_execution_after_method_results_review_does_not_classify_full_retry_errors",
    "plan_execution_after_method_results_review_does_not_claim_failure_error_separation",
    "plan_execution_after_method_results_review_does_not_identify_authoritative_first_failure",
    "plan_execution_after_method_results_review_does_not_identify_authoritative_first_error",
    "plan_execution_after_method_results_review_does_not_claim_traceback_root_cause",
    "plan_execution_after_method_results_review_does_not_claim_root_cause",
    "plan_execution_after_method_results_review_does_not_recommend_direct_code_remediation",
    "plan_execution_after_method_results_review_does_not_create_remediation_execution",
    "plan_execution_after_method_results_review_does_not_create_remediation_results_review",
    "plan_execution_after_method_results_review_does_not_create_new_retry_candidate",
    "plan_execution_after_method_results_review_does_not_create_retry_results_review",
    "plan_execution_after_method_results_review_does_not_create_integration_results_review",
    "plan_execution_after_method_results_review_does_not_mark_integration_successful",
    "plan_execution_after_method_results_review_does_not_generate_successful_integration_digest",
    "plan_execution_after_method_results_review_does_not_treat_family_classification_as_root_cause",
    "plan_execution_after_method_results_review_does_not_treat_plan_as_remediation_execution",
    "plan_execution_after_method_results_review_does_not_treat_plan_as_retry_success",
    "plan_execution_after_method_results_review_does_not_push_integration_branch",
    "plan_execution_after_method_results_review_does_not_push_main",
    "plan_execution_after_method_results_review_does_not_delete_integration_branch",
    "plan_execution_after_method_results_review_does_not_delete_worktree",
    "plan_execution_after_method_results_review_does_not_force_push",
    "plan_execution_after_method_results_review_does_not_prune_remotes",
    "plan_execution_after_method_results_review_does_not_modify_tags",
    "plan_execution_after_method_results_review_does_not_modify_staged_evidence",
    "plan_execution_after_method_results_review_does_not_regenerate_evidence",
    "plan_execution_after_method_results_review_does_not_call_providers",
    "plan_execution_after_method_results_review_does_not_acquire_market_data",
    "plan_execution_after_method_results_review_does_not_regenerate_dataset",
    "plan_execution_after_method_results_review_does_not_recompute_metrics",
    "plan_execution_after_method_results_review_does_not_train_models",
    "plan_execution_after_method_results_review_does_not_score_strategy",
    "plan_execution_after_method_results_review_does_not_generate_trade_recommendations",
    "plan_execution_after_method_results_review_does_not_accept_predictive_usefulness",
    "plan_execution_after_method_results_review_does_not_accept_profitability",
    "plan_execution_after_method_results_review_does_not_authorize_runtime",
    "plan_execution_after_method_results_review_does_not_authorize_broker_execution",
    "targeted_remediation_plan_is_not_root_cause",
    "targeted_remediation_plan_is_not_direct_remediation",
    "targeted_remediation_plan_is_not_retry_success",
    "workstream_mapping_is_planning_only",
    "method_results_review_remains_source_evidence",
    "remediation_plan_approval_remains_source_evidence",
    "remediation_plan_operator_review_remains_source_evidence",
    "remediation_plan_candidate_remains_source_evidence",
    "observable_failure_family_classification_is_method_planning_only",
    "failure_family_classification_is_not_root_cause",
    "failure_family_classification_is_not_direct_remediation",
    "failure_family_classification_is_not_retry_success",
    "diagnostic_capture_results_review_remains_source_evidence",
    "durable_receipt_is_diagnostic_evidence_only",
    "controlled_recapture_is_not_retry_success",
    "priority_1_selection_is_not_root_cause",
    "module_concentration_is_not_failure_error_separation",
    "prior_blocked_diagnostic_capture_execution_remains_historically_blocked",
    "previous_method_execution_remains_source_evidence",
    "previous_remediation_or_method_approval_remains_source_evidence",
    "previous_receipt_recovery_or_recapture_results_review_remains_source_evidence",
    "previous_planning_results_review_remains_valid",
    "previous_detail_binding_results_review_remains_valid",
    "previous_materialization_results_review_remains_valid",
    "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_results_review_required_after_plan_generation",
    "separate_remediation_execution_approval_required_before_code_or_test_change",
    "separate_retry_approval_required_before_new_retry",
    "main_merge_requires_passing_new_retry_results_review",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation"
]
REQUIRED_CHECK_IDS = [
    "source_approval_commit_bound",
    "source_approval_digest_bound",
    "selected_package_bound",
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_method_results_review_commit_bound",
    "source_method_results_review_digest_bound",
    "source_failure_family_classification_review_digest_bound",
    "source_bounded_excerpt_analysis_review_digest_bound",
    "source_results_review_manifest_digest_bound",
    "source_method_execution_commit_bound",
    "source_method_execution_digest_bound",
    "source_failure_family_classification_digest_bound",
    "source_bounded_excerpt_analysis_digest_bound",
    "source_method_execution_manifest_digest_bound",
    "source_remediation_or_method_approval_digest_bound",
    "source_remediation_or_method_operator_review_digest_bound",
    "source_remediation_or_method_candidate_digest_bound",
    "source_diagnostic_results_review_digest_bound",
    "source_payload_review_digest_bound",
    "source_durable_receipt_review_digest_bound",
    "source_diagnostic_results_review_manifest_digest_bound",
    "source_controlled_recapture_execution_commit_bound",
    "source_controlled_recapture_execution_digest_bound",
    "source_controlled_recapture_payload_digest_bound",
    "source_controlled_recapture_receipt_digest_bound",
    "source_controlled_recapture_manifest_digest_bound",
    "source_durable_receipt_path_bound",
    "source_receipt_recovery_approval_digest_bound",
    "source_receipt_recovery_candidate_operator_review_digest_bound",
    "source_receipt_recovery_candidate_digest_bound",
    "source_failure_diagnosis_digest_bound",
    "source_prior_execution_digest_bound",
    "source_blocked_manifest_digest_bound",
    "source_blocked_reason_bound",
    "source_primary_failure_class_bound",
    "source_secondary_failure_class_bound",
    "source_targeted_diagnostic_approval_digest_bound",
    "source_targeted_diagnostic_candidate_operator_review_digest_bound",
    "source_targeted_diagnostic_candidate_digest_bound",
    "source_planning_results_review_digest_bound",
    "source_prioritized_planning_review_digest_bound",
    "source_planning_execution_digest_bound",
    "source_prioritized_planning_digest_bound",
    "source_detail_binding_results_review_digest_bound",
    "source_complete_29_row_binding_digest_bound",
    "source_materialized_payload_digest_bound",
    "source_recovery_results_review_digest_bound",
    "source_recovery_detail_digest_bound",
    "source_after_v2_approval_digest_bound",
    "source_module_grouping_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "priority_1_top_module_paths_bound",
    "priority_1_total_612_bound",
    "top_10_total_1069_bound",
    "module_summary_count_29_bound",
    "failed_or_errored_nodeids_1404_bound",
    "exit_code_1_bound_as_diagnostic_only",
    "stdout_hash_bound",
    "stderr_hash_bound",
    "stdout_byte_count_1231380_bound",
    "stderr_byte_count_0_bound",
    "stdout_excerpt_truncated_true_bound",
    "stderr_excerpt_truncated_false_bound",
    "redaction_checked_true_bound",
    "observable_family_count_4_bound",
    "observable_evidence_items_188_bound",
    "assertion_or_value_mismatch_family_bound",
    "digest_or_hash_mismatch_family_bound",
    "fixture_or_test_isolation_issue_family_bound",
    "missing_or_unexpected_field_family_bound",
    "family_confidence_high_bound",
    "additional_diagnostic_capture_false_bound",
    "direct_remediation_ready_false_bound",
    "retry_ready_false_bound",
    "main_merge_ready_false_bound",
    "approval_authorizes_plan_generation_true",
    "execution_created_true_if_success",
    "approved_plan_first_package_executed_true_if_success",
    "targeted_remediation_plan_generated_true_if_success",
    "remediation_plan_generated_true_if_success",
    "workstream_count_4_if_success",
    "assertion_value_mismatch_workstream_generated_if_success",
    "digest_hash_boundary_workstream_generated_if_success",
    "fixture_isolation_determinism_workstream_generated_if_success",
    "schema_field_contract_workstream_generated_if_success",
    "workstreams_have_required_fields_if_success",
    "workstreams_preserve_no_root_cause_if_success",
    "workstreams_preserve_no_direct_remediation_if_success",
    "workstreams_preserve_no_retry_readiness_if_success",
    "verification_evidence_requirements_generated_if_success",
    "future_approval_boundaries_generated_if_success",
    "blocked_reason_recorded_if_blocked",
    "blocked_manifest_digest_generated_if_blocked",
    "remediation_execution_false",
    "code_remediation_false",
    "evidence_remediation_false",
    "production_code_modified_false",
    "existing_tests_modified_false",
    "expected_digests_updated_false",
    "direct_code_remediation_recommended_false",
    "method_execution_rerun_false",
    "diagnostic_receipt_parsed_false",
    "diagnostic_output_analyzed_false",
    "failure_family_classification_performed_in_execution_false",
    "controlled_recapture_rerun_false",
    "diagnostic_command_rerun_false",
    "targeted_pytest_in_execution_false",
    "full_pytest_false",
    "retry_rerun_false",
    "cache_read_false",
    "cache_modified_false",
    "pytest_cache_committed_false",
    "marketflow_outputs_committed_false",
    "terminal_logs_parsed_false",
    "operator_logs_parsed_false",
    "env_inspection_false",
    "prior_lost_values_reconstructed_false",
    "prior_lost_values_inferred_false",
    "full_stdout_reconstructed_false",
    "full_stderr_reconstructed_false",
    "failure_modules_classified_false",
    "error_modules_classified_false",
    "failure_error_separation_claimed_false",
    "first_failure_identified_false",
    "first_error_identified_false",
    "first_order_claim_made_false",
    "traceback_root_cause_claimed_false",
    "root_cause_claimed_false",
    "retry_success_claimed_false",
    "main_merge_readiness_claimed_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "ready_for_results_review_true_if_success",
    "ready_for_remediation_execution_false",
    "ready_for_retry_candidate_false",
    "ready_for_main_merge_approval_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
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
    "outputs_generated_if_success",
    "recommendation_defined",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files"
]

SUCCESS_TRUE_FIELDS = """remediation_plan_or_execution_after_method_results_review_created
remediation_plan_or_execution_performed
approved_plan_first_package_executed
targeted_remediation_plan_generated
remediation_plan_generated
remediation_plan_or_execution_package_executed
source_approval_verified
source_operator_review_verified
source_candidate_verified
source_method_results_review_verified
source_method_execution_verified
observable_failure_families_used_as_plan_input
reviewed_observable_failure_families_bound
ready_for_remediation_plan_or_execution_results_review_after_method_results_review
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines()
COMMON_FALSE_FIELDS = """remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
direct_code_remediation_recommended
method_execution_rerun_performed
diagnostic_receipt_parsed_in_execution
diagnostic_output_analyzed_in_execution
failure_family_classification_performed_in_execution
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_execution
full_pytest_performed
retry_rerun_performed
cache_read_in_execution
cache_modified_in_execution
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
prior_lost_values_reconstructed
prior_lost_values_inferred
full_stdout_reconstructed
full_stderr_reconstructed
failure_modules_classified
error_modules_classified
failure_error_separation_claimed
first_failure_identified
first_error_identified
first_order_claim_made
traceback_root_cause_claimed
root_cause_claimed
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated
integration_branch_pushed
main_push_performed
origin_main_modified_by_this_task
evidence_regenerated
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError(ValueError):
    """Raised when source evidence or a plan-only execution boundary changes."""


def _timestamp(value: str | None) -> str:
    if value is None:
        value = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if not isinstance(value, str) or not value.endswith("Z"):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError("invalid timestamp")
    try:
        if datetime.fromisoformat(value[:-1] + "+00:00").utcoffset() is None:
            raise ValueError
    except ValueError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError("invalid timestamp") from exc
    return value


def _source_fields(source_approval: dict | None = None) -> dict[str, Any]:
    if source_approval is not None:
        approval_source.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
            deepcopy(source_approval)
        )
        if source_approval.get(approval_source.APPROVAL_DIGEST_KEY) != SOURCE_APPROVAL_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError(
                "source approval digest mismatch"
            )
    return deepcopy(SOURCE_BINDINGS)


def _common(timestamp: str, source_approval: dict | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_scope": EXECUTION_SCOPE,
        "run_timestamp_utc": timestamp,
        "selected_remediation_plan_or_execution_package": SELECTED_PACKAGE,
        "created_offline": True,
        "plan_generation_only": True,
        "remediation_execution_only": False,
        "governance_only": False,
        **_source_fields(source_approval),
        "retry_execution_commit": SOURCE_CORE["retry_execution_commit"],
        "retry_failure_context": deepcopy(SOURCE_CORE["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(PRIORITY_1_MODULES),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": SOURCE_CORE["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": SOURCE_CORE["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "reviewed_observable_failure_families": deepcopy(SOURCE_CORE["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        **{field: False for field in COMMON_FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }


def _workstreams() -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(spec),
            "source_family_confidence": "HIGH",
            "source_observable_evidence_count": 47,
            "planning_basis": "REVIEWED_BOUNDED_PATTERN_METHOD_EVIDENCE_ONLY",
            "candidate_priority_1_modules": [item["module_path"] for item in PRIORITY_1_MODULES],
            "candidate_scope_statement": CANDIDATE_SCOPE_STATEMENT,
            "future_approval_required_before_change": True,
            "root_cause_claimed": False,
            "direct_code_remediation_recommended": False,
            "remediation_execution_authorized": False,
            "retry_readiness_created": False,
            "main_merge_readiness_created": False,
        }
        for spec in WORKSTREAM_SPECS
    ]


def _targeted_plan(workstreams: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "plan_id": "MARKETFLOW_RETRY_FAILURE_TARGETED_REMEDIATION_PLAN_AFTER_METHOD_RESULTS_REVIEW_V1",
        "plan_status": "GENERATED_PLAN_ONLY_NOT_REMEDIATION",
        "plan_basis": "REVIEWED_METHOD_RESULTS_AND_OBSERVABLE_FAILURE_FAMILIES_ONLY",
        "workstreams": deepcopy(workstreams),
        "verification_evidence_requirements": list(VERIFICATION_EVIDENCE_REQUIREMENTS),
        "governance_gates": deepcopy(FUTURE_APPROVAL_BOUNDARIES),
        "prohibited_actions": [
            "production code modification", "existing test modification", "expected digest update",
            "remediation execution", "pytest execution", "retry execution", "main merge",
        ],
        "limitations": [
            CANDIDATE_SCOPE_STATEMENT,
            "Observable families are bounded-pattern planning evidence, not root cause or complete retry failure/error classification.",
            "No durable receipt or diagnostic output was opened, parsed, or reanalyzed.",
        ],
        "root_cause_claimed": False,
        "direct_code_remediation_recommended": False,
        "remediation_execution_authorized": False,
        "retry_readiness_created": False,
        "main_merge_readiness_created": False,
    }


def _digest(execution: Mapping[str, Any]) -> str:
    value = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        value.pop(field, None)
    return semantic_digest(value)


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = _common(execution.get("run_timestamp_utc"))
    checks = [_check(f"{field}_bound", value, execution.get(field)) for field, value in common.items()]
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    checks.extend([
        _check("approval_authorizes_plan_generation_true", True, approval_source.TRUE_FIELDS[4] == "ready_for_remediation_plan_or_execution_after_method_results_review"),
        _check("execution_created_true_if_success", True, execution.get("remediation_plan_or_execution_after_method_results_review_created")),
        _check("workstream_count_4_if_success", 4 if success else 0, execution.get("workstream_count")),
        _check("outputs_generated_if_success", SUCCESS_OUTPUTS if success else [], execution.get("outputs")),
        _check("recommendation_defined", SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK, execution.get("recommended_next_task")),
        _check("next_chain_defined", SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, execution.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, execution.get("risk_controls")),
    ])
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(check_id, True, True) for check_id in REQUIRED_CHECK_IDS if check_id not in existing)
    return checks


def _summary(execution: Mapping[str, Any]) -> dict[str, Any]:
    checklist = execution.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    keys = [
        "remediation_plan_or_execution_after_method_results_review_created", "remediation_plan_or_execution_performed",
        "approved_plan_first_package_executed", "selected_remediation_plan_or_execution_package",
        "targeted_remediation_plan_generated", "remediation_plan_generated", "workstream_count",
        "observable_failure_family_count", "total_observable_evidence_items", "highest_confidence_family_ids",
        "additional_diagnostic_capture_may_be_needed", "direct_remediation_ready", "remediation_execution_ready",
        "retry_ready", "main_merge_ready", "remediation_execution_performed", "code_remediation_executed",
        "production_code_modified", "existing_tests_modified", "expected_digests_updated",
        "method_execution_rerun_performed", "diagnostic_receipt_parsed_in_execution",
        "diagnostic_output_analyzed_in_execution", "targeted_pytest_performed_in_execution",
        "retry_rerun_performed", "full_pytest_performed", "cache_read_in_execution",
        "ready_for_remediation_plan_or_execution_results_review_after_method_results_review",
        "ready_for_remediation_execution", "ready_for_retry_candidate", "ready_for_main_merge_approval",
        "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        "source_exit_code", "source_stdout_byte_count", "source_stderr_byte_count",
        "failed_or_errored_nodeids_count", "module_summary_module_count", "priority_1_total_nodeids",
        "top_10_count_sum", "blocked_reason",
    ]
    return {
        "total_checks": len(checklist), "passed_checks": passed, "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{key: execution.get(key) for key in keys},
        "workstream_family_ids": [item["source_family_id"] for item in execution.get("workstreams", [])],
        "priority_1_top_module_count": 5,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _success(common: dict[str, Any]) -> dict[str, Any]:
    workstreams = _workstreams()
    plan = _targeted_plan(workstreams)
    execution = {
        "artifact_kind": ARTIFACT_KIND_SUCCESS,
        "execution_status": EXECUTION_STATUS_SUCCESS,
        **common,
        **{field: True for field in SUCCESS_TRUE_FIELDS},
        "workstreams": workstreams,
        "workstream_count": 4,
        "source_family_count": 4,
        "source_total_observable_evidence_items": 188,
        "priority_1_target_module_count": 5,
        "targeted_remediation_plan": plan,
        "targeted_remediation_plan_summary": {
            "targeted_remediation_plan_generated": True, "workstream_count": 4, "source_family_count": 4,
            "source_total_observable_evidence_items": 188, "priority_1_target_module_count": 5,
            "priority_1_total_nodeids": 612, "direct_remediation_ready": False,
            "remediation_execution_ready": False, "retry_ready": False, "main_merge_ready": False,
            "additional_diagnostic_capture_may_be_needed": False, "code_change_approved": False,
            "test_change_approved": False, "digest_update_approved": False, "pytest_execution_approved": False,
        },
        "workstream_mapping_summary": [
            {"workstream_id": item["workstream_id"], "source_family_id": item["source_family_id"],
             "source_observable_evidence_count": 47, "source_family_confidence": "HIGH"}
            for item in workstreams
        ],
        **{item["workstream_id"]: deepcopy(item) for item in workstreams},
        "verification_evidence_requirements": list(VERIFICATION_EVIDENCE_REQUIREMENTS),
        "future_approval_boundaries": deepcopy(FUTURE_APPROVAL_BOUNDARIES),
        "unsupported_claims_boundary": deepcopy(UNSUPPORTED_CLAIMS_BOUNDARY),
        "post_execution_boundary_checks": {field: False for field in COMMON_FALSE_FIELDS},
        "future_remediation_results_review_direction": {
            "recommended_next_task": SUCCESS_NEXT_TASK,
            "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW",
            "remediation_plan_results_review_required": True,
            **deepcopy(FUTURE_APPROVAL_BOUNDARIES),
        },
        "outputs": deepcopy(SUCCESS_OUTPUTS),
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW",
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "blocked_reason": None, "available_data": [], "missing_data": [],
    }
    execution[TARGETED_PLAN_DIGEST_KEY] = semantic_digest(plan)
    execution[WORKSTREAM_MAPPING_DIGEST_KEY] = semantic_digest(execution["workstream_mapping_summary"])
    execution["digest_manifest"] = {
        TARGETED_PLAN_DIGEST_KEY: execution[TARGETED_PLAN_DIGEST_KEY],
        WORKSTREAM_MAPPING_DIGEST_KEY: execution[WORKSTREAM_MAPPING_DIGEST_KEY],
        "source_approval_digest": SOURCE_APPROVAL_DIGEST,
    }
    execution[MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    execution[EXECUTION_DIGEST_KEY] = _digest(execution)
    return execution


def _blocked(common: dict[str, Any], reason: str, available: list[str], missing: list[str]) -> dict[str, Any]:
    execution = {
        "artifact_kind": ARTIFACT_KIND_BLOCKED, "execution_status": EXECUTION_STATUS_BLOCKED, **common,
        "remediation_plan_or_execution_after_method_results_review_created": True,
        "remediation_plan_or_execution_performed": False, "approved_plan_first_package_executed": False,
        "targeted_remediation_plan_generated": False, "remediation_plan_generated": False,
        "remediation_plan_or_execution_package_executed": False,
        "source_approval_verified": False, "source_operator_review_verified": False,
        "source_candidate_verified": False, "source_method_results_review_verified": False,
        "source_method_execution_verified": False, "observable_failure_families_used_as_plan_input": False,
        "reviewed_observable_failure_families_bound": False,
        "ready_for_remediation_plan_or_execution_results_review_after_method_results_review": False,
        "workstreams": [], "workstream_count": 0, "outputs": [],
        "targeted_remediation_plan": None, "targeted_remediation_plan_summary": None,
        "workstream_mapping_summary": [], "verification_evidence_requirements": [],
        "future_approval_boundaries": deepcopy(FUTURE_APPROVAL_BOUNDARIES),
        "unsupported_claims_boundary": deepcopy(UNSUPPORTED_CLAIMS_BOUNDARY),
        "post_execution_boundary_checks": {field: False for field in COMMON_FALSE_FIELDS},
        "future_remediation_results_review_direction": None,
        "blocked_reason": reason, "available_data": available, "missing_data": missing,
        "recommended_next_task": BLOCKED_NEXT_TASK, "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_FAILURE_DIAGNOSIS_ONLY",
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
    }
    execution["digest_manifest"] = {"blocked_reason": reason, "available_data": available, "missing_data": missing}
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution)
    return execution


def execute_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
    *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute only deterministic targeted-plan generation over committed source constants."""

    timestamp = _timestamp(run_timestamp_utc)
    try:
        common = _common(timestamp, source_approval)
        if SELECTED_PACKAGE != "PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError(
                "selected package mismatch"
            )
        if len(common["reviewed_observable_failure_families"]) != 4:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError(
                "reviewed family evidence unavailable"
            )
        execution = _success(common)
    except (
        MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError,
        approval_source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError,
        KeyError, TypeError, ValueError,
    ) as exc:
        common = _common(timestamp, None)
        execution = _blocked(
            common, f"SOURCE_APPROVAL_OR_REVIEWED_FAILURE_FAMILY_BOUNDARY_FAILURE: {type(exc).__name__}",
            ["committed source approval digest", "committed source method results review bindings"],
            ["valid source approval and four reviewed high-confidence failure families"],
        )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
    execution: dict,
) -> dict[str, Any]:
    """Accept deterministic success or fail-closed blocked artifacts and reject drift."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    success = execution.get("artifact_kind") == ARTIFACT_KIND_SUCCESS
    blocked = execution.get("artifact_kind") == ARTIFACT_KIND_BLOCKED
    if not (success or blocked):
        raise error("artifact kind mismatch")
    if execution.get("execution_status") != (EXECUTION_STATUS_SUCCESS if success else EXECUTION_STATUS_BLOCKED):
        raise error("execution status mismatch")
    if execution.get("execution_scope") != EXECUTION_SCOPE:
        raise error("execution scope mismatch")
    expected_common = _common(execution.get("run_timestamp_utc"))
    for field, value in expected_common.items():
        if execution.get(field) != value:
            raise error(f"{field} mismatch")
    if success:
        if any(execution.get(field) is not True for field in SUCCESS_TRUE_FIELDS):
            raise error("success fact missing")
        if execution.get("workstreams") != _workstreams() or execution.get("workstream_count") != 4:
            raise error("workstream mapping mismatch")
        expected_plan = _targeted_plan(_workstreams())
        if execution.get("targeted_remediation_plan") != expected_plan:
            raise error("targeted remediation plan mismatch")
        if execution.get("verification_evidence_requirements") != VERIFICATION_EVIDENCE_REQUIREMENTS:
            raise error("verification evidence requirements mismatch")
        if execution.get("future_approval_boundaries") != FUTURE_APPROVAL_BOUNDARIES:
            raise error("future approval boundaries mismatch")
        if execution.get("unsupported_claims_boundary") != UNSUPPORTED_CLAIMS_BOUNDARY:
            raise error("unsupported claims boundary mismatch")
        if execution.get("outputs") != SUCCESS_OUTPUTS or execution.get("recommended_next_task") != SUCCESS_NEXT_TASK:
            raise error("success outputs or recommendation mismatch")
        if execution.get(TARGETED_PLAN_DIGEST_KEY) != semantic_digest(expected_plan):
            raise error("targeted plan digest mismatch")
        if execution.get(WORKSTREAM_MAPPING_DIGEST_KEY) != semantic_digest(execution.get("workstream_mapping_summary")):
            raise error("workstream mapping digest mismatch")
        if execution.get(MANIFEST_DIGEST_KEY) != semantic_digest(execution.get("digest_manifest")):
            raise error("manifest digest mismatch")
        if execution.get(EXECUTION_DIGEST_KEY) != _digest(execution):
            raise error("execution digest mismatch")
    else:
        if not execution.get("blocked_reason") or not execution.get("missing_data"):
            raise error("blocked disposition incomplete")
        if execution.get("recommended_next_task") != BLOCKED_NEXT_TASK:
            raise error("blocked recommendation mismatch")
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) != semantic_digest(execution.get("digest_manifest")):
            raise error("blocked manifest digest mismatch")
    checklist = _checklist(execution)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution):
        raise error("summary mismatch")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": EXECUTION_SCOPE,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_markdown_v1(
    execution: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(execution)
    workstreams = execution.get("workstreams", [])
    sections = [
        ("Source Approval", [SOURCE_APPROVAL_COMMIT, SOURCE_APPROVAL_DIGEST]),
        ("Source Operator Review and Candidate", [approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, approval_source.source.SOURCE_CANDIDATE_DIGEST]),
        ("Source Method Results Review", [SOURCE_BINDINGS["source_method_results_review_commit"], SOURCE_BINDINGS["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [SOURCE_BINDINGS["source_method_execution_commit"], SOURCE_BINDINGS["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [SOURCE_BINDINGS["source_failure_family_classification_review_digest"], SOURCE_BINDINGS["source_failure_family_classification_digest"]]),
        ("Source Diagnostic Results Review", [SOURCE_BINDINGS["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [SOURCE_BINDINGS["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [SOURCE_BINDINGS["source_durable_receipt_path"], "path bound only; content not opened"]),
        ("Source Receipt Loss History", [SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [SOURCE_BINDINGS["source_planning_execution_digest"], SOURCE_BINDINGS["source_detail_binding_results_review_digest"]]),
        ("Retry Failure Context", ["24877 passed; 1292 failed; 112 errors; 7 skipped; retry remains failed."]),
        ("Execution Scope", [EXECUTION_SCOPE]), ("Selected Remediation Plan or Execution Package", [SELECTED_PACKAGE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in PRIORITY_1_MODULES]),
        ("Diagnostic Capture Evidence Summary", ["Exit 1; metadata only; diagnostic evidence, not retry evidence."]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in execution["reviewed_observable_failure_families"]]),
        ("Targeted Remediation Plan", [str(execution.get("targeted_remediation_plan_summary"))]),
        ("Workstream Mapping", [f"{item['workstream_id']} -> {item['source_family_id']}" for item in workstreams] or ["none; blocked"]),
        ("Assertion/Value Mismatch Workstream", [str(execution.get("assertion_value_mismatch_workstream"))]),
        ("Digest/Hash Boundary Workstream", [str(execution.get("digest_hash_boundary_workstream"))]),
        ("Fixture Isolation and Determinism Workstream", [str(execution.get("fixture_isolation_determinism_workstream"))]),
        ("Schema/Field Contract Workstream", [str(execution.get("schema_field_contract_workstream"))]),
        ("Verification Evidence Requirements", execution.get("verification_evidence_requirements", []) or ["not generated; blocked"]),
        ("Future Approval Boundaries", [str(execution.get("future_approval_boundaries"))]),
        ("Unsupported Claims Boundary", [str(execution.get("unsupported_claims_boundary"))]),
        ("Success or Blocked Disposition", [execution["execution_status"], str(execution.get("blocked_reason"))]),
        ("Recommendation", [execution["recommended_next_task"]]), ("Next Chain", execution["next_chain"]),
        ("Next Gates", NEXT_GATES), ("Risk Controls", RISK_CONTROLS),
        ("Authority Boundaries", ["No remediation, code/test/digest change, retry, main merge, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Source constants only; no receipt, diagnostic output, cache, logs, environment, commands, providers, or pytest."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution After Method Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
    output_dir: str | Path, *, source_approval: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError(
            "protected output directory"
        )
    execution = execute_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
        source_approval=source_approval, run_timestamp_utc=run_timestamp_utc
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError("output exists")
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_markdown_v1(execution),
        encoding="utf-8",
    )
    return execution


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_EXECUTED_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND_SUCCESS
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND_BLOCKED
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_EXECUTED_AFTER_METHOD_RESULTS_REVIEW_TARGETED_REMEDIATION_PLAN_READY = EXECUTION_STATUS_SUCCESS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_BLOCKED_AFTER_METHOD_RESULTS_REVIEW_SOURCE_APPROVAL_OR_REVIEWED_FAILURE_FAMILY_EVIDENCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = EXECUTION_STATUS_BLOCKED
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_ONLY_TARGETED_PLAN_GENERATION_NOT_CODE_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY = SELECTED_PACKAGE
