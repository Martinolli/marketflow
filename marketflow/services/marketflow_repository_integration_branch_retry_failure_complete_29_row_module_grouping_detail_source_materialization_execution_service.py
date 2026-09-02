"""Materialize a bounded complete 29-row source from reviewed cache evidence."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_service
    as approval_source,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_COMPLETE_29_ROW_SOURCE_CREATED"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_ONLY_COMPLETE_DETAIL_SOURCE_CREATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1"
SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE = approval_source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE
SOURCE_APPROVAL_DIGEST = "f8126d0d38793c9c562fca0217823ffdb919301596ec44b9bc33ff807fa77059"
EXPECTED_LASTFAILED_SHA256 = "24fb8cf5ce237ae6c952c29c37acaea7d22205ca885659a196f0bc27c4b1f1b1"
EXPECTED_NODEIDS_SHA256 = "9d69140fd12f57de3c14060139bc4d50a3096c29b0262c5e482af5b78ea0206d"
REVIEWED_LASTFAILED_SHA256 = EXPECTED_LASTFAILED_SHA256
REVIEWED_NODEIDS_SHA256 = EXPECTED_NODEIDS_SHA256
EXPECTED_LASTFAILED_COUNT = 1404
EXPECTED_NODEIDS_COUNT = 26288
EXPECTED_MODULE_COUNT = 29
EXPECTED_LARGEST_COUNTS = [136, 131, 122, 112, 111]
EXPECTED_TOP_FIVE_PATHS = [
    "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
    "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
    "tests/test_corporate_action_authority_plan_candidate_service.py",
    "tests/test_feature_generation_results_review_redesigned_labels_service.py",
    "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
]
DEFAULT_CACHE_ROOT = Path(r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1\.pytest_cache\v\cache")
SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_FAILURE_DIAGNOSIS_V1"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
ROW_SOURCE = "MATERIALIZED_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY"
ROW_BASIS = "VERIFIED_LASTFAILED_AND_NODEIDS_HASHES_WITH_RECOVERY_RESULTS_REVIEW_BINDING"
ROW_CONFIDENCE = "HIGH_FOR_MODULE_GROUPING_ONLY"
UNSUPPORTED_ROW_CLAIMS = [
    "no_failure_error_separation", "no_first_order_claim", "no_traceback_root_cause",
    "no_direct_code_remediation", "no_retry_success", "no_main_merge_readiness",
]
COMMITTED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE = (
    ("tests/test_marketflow_signal_or_feature_generation_results_review_service.py", 136, (
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py::test_all_local_output_hashes_are_bound_and_verified",
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py::test_checklist_passes",
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py::test_closed_review_flags_remain_false[approval_rerun_performed]",
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py::test_closed_review_flags_remain_false[candidate_creation_rerun_performed]",
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py::test_closed_review_flags_remain_false[candidate_review_rerun_performed]",
    )),
    ("tests/test_post_identity_freeze_registry_inventory_approval_service.py", 131, (
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py::test_approval_and_per_ticker_approval_digests_are_deterministic",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py::test_approved_artifact_builds_offline_without_provider_calls",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py::test_artifact_kind_status_scope_and_digest_are_exact",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py::test_checklist_and_summary_counts_are_complete",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py::test_closed_boolean_boundaries_remain_false[acquisition_authorization_created]",
    )),
    ("tests/test_corporate_action_authority_plan_candidate_service.py", 122, (
        "tests/test_corporate_action_authority_plan_candidate_service.py::test_artifact_kind_status_and_digest_are_exact",
        "tests/test_corporate_action_authority_plan_candidate_service.py::test_candidate_and_per_ticker_plan_digests_are_deterministic",
        "tests/test_corporate_action_authority_plan_candidate_service.py::test_candidate_builds_offline_without_provider_calls",
        "tests/test_corporate_action_authority_plan_candidate_service.py::test_checklist_contains_all_required_ids_and_passes",
        "tests/test_corporate_action_authority_plan_candidate_service.py::test_closed_boolean_boundaries_remain_false[acquisition_authorization_created]",
    )),
    ("tests/test_feature_generation_results_review_redesigned_labels_service.py", 112, (
        "tests/test_feature_generation_results_review_redesigned_labels_service.py::test_artifact_kind_is_correct",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py::test_baseline_error_context_is_unavailable_by_design",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py::test_checklist_passes",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py::test_closed_action_remains_false[additional_predictive_evidence_executed]",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py::test_closed_action_remains_false[additional_predictive_evidence_execution_authorized]",
    )),
    ("tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", 111, (
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py::test_all_local_output_hashes_are_bound_and_verified",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py::test_checklist_passes",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py::test_closed_review_flags_remain_false[approval_rerun_performed]",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py::test_closed_review_flags_remain_false[candidate_creation_rerun_performed]",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py::test_closed_review_flags_remain_false[candidate_review_rerun_performed]",
    )),
    ("tests/test_corporate_action_authority_plan_candidate_operator_review_service.py", 109, (
        "tests/test_corporate_action_authority_plan_candidate_operator_review_service.py::test_artifact_kind_status_schema_and_binding_mode_are_exact",
        "tests/test_corporate_action_authority_plan_candidate_operator_review_service.py::test_checklist_contains_all_required_check_ids_and_all_pass",
        "tests/test_corporate_action_authority_plan_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[acquisition_authorization_created]",
        "tests/test_corporate_action_authority_plan_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[acquisition_generation_authorized]",
        "tests/test_corporate_action_authority_plan_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[additional_predictive_evidence_executed]",
    )),
    ("tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py", 97, (
        "tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py::test_artifact_kind_status_scope_and_digest_are_exact",
        "tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py::test_build_rejects_missing_operator_boundary_confirmation[operator_confirms_authority_scope_identity_only]",
        "tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py::test_build_rejects_missing_operator_boundary_confirmation[operator_confirms_no_acquisition_authority]",
        "tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py::test_build_rejects_missing_operator_boundary_confirmation[operator_confirms_no_additional_predictive_evidence_execution]",
        "tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py::test_build_rejects_missing_operator_boundary_confirmation[operator_confirms_no_api_key_storage_or_printing]",
    )),
    ("tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py", 86, (
        "tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py::test_artifact_kind_status_and_digest_are_exact",
        "tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py::test_checklist_and_summary_counts_are_complete",
        "tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[acquisition_generation_authorized]",
        "tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[additional_predictive_evidence_executed]",
        "tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py::test_closed_boolean_boundaries_remain_false[additional_predictive_evidence_execution_authorized]",
    )),
    ("tests/test_post_identity_freeze_registry_inventory_candidate_service.py", 84, (
        "tests/test_post_identity_freeze_registry_inventory_candidate_service.py::test_artifact_kind_status_and_digest_are_exact",
        "tests/test_post_identity_freeze_registry_inventory_candidate_service.py::test_candidate_and_per_ticker_inventory_digests_are_deterministic",
        "tests/test_post_identity_freeze_registry_inventory_candidate_service.py::test_candidate_builds_offline_without_provider_calls",
        "tests/test_post_identity_freeze_registry_inventory_candidate_service.py::test_checklist_and_summary_counts_are_complete",
        "tests/test_post_identity_freeze_registry_inventory_candidate_service.py::test_closed_boolean_boundaries_remain_false[acquisition_generation_authorized]",
    )),
    ("tests/test_position_swing_canonical_dataset_operator_freeze_service.py", 81, (
        "tests/test_position_swing_canonical_dataset_operator_freeze_service.py::test_2025_01_cross_check_passed_and_has_20_bars",
        "tests/test_position_swing_canonical_dataset_operator_freeze_service.py::test_artifact_kind_is_position_swing_canonical_dataset_frozen",
        "tests/test_position_swing_canonical_dataset_operator_freeze_service.py::test_authority_digests_match_expected",
        "tests/test_position_swing_canonical_dataset_operator_freeze_service.py::test_dataset_manifest_digest_matches_expected",
        "tests/test_position_swing_canonical_dataset_operator_freeze_service.py::test_dataset_rows_digest_matches_expected",
    )),
    ("tests/test_swing_canonical_dataset_operator_freeze_service.py", 75, (
        "tests/test_swing_canonical_dataset_operator_freeze_service.py::test_2025_01_cross_check_passed_and_has_40_bars",
        "tests/test_swing_canonical_dataset_operator_freeze_service.py::test_artifact_kind_is_swing_canonical_dataset_frozen",
        "tests/test_swing_canonical_dataset_operator_freeze_service.py::test_authority_digests_match_expected",
        "tests/test_swing_canonical_dataset_operator_freeze_service.py::test_canonical_eligibility_remains_false",
        "tests/test_swing_canonical_dataset_operator_freeze_service.py::test_dataset_manifest_digest_matches_expected",
    )),
    ("tests/test_corporate_action_authority_plan_approval_service.py", 73, (
        "tests/test_corporate_action_authority_plan_approval_service.py::test_all_approval_checks_pass_and_summary_counts_are_correct",
        "tests/test_corporate_action_authority_plan_approval_service.py::test_approval_checklist_contains_all_required_check_ids",
        "tests/test_corporate_action_authority_plan_approval_service.py::test_approval_digest_is_deterministic_and_validated",
        "tests/test_corporate_action_authority_plan_approval_service.py::test_approved_artifact_builds_offline_without_provider_calls",
        "tests/test_corporate_action_authority_plan_approval_service.py::test_artifact_kind_status_and_scope_are_exact",
    )),
    ("tests/test_marketflow_signal_or_feature_generation_execution_service.py", 72, (
        "tests/test_marketflow_signal_or_feature_generation_execution_service.py::test_all_ten_outputs_exist_and_no_extra_output_exists",
        "tests/test_marketflow_signal_or_feature_generation_execution_service.py::test_digest_manifest_has_explicit_self_reference_policy",
        "tests/test_marketflow_signal_or_feature_generation_execution_service.py::test_downstream_and_external_authorities_remain_closed[api_keys_stored_or_printed]",
        "tests/test_marketflow_signal_or_feature_generation_execution_service.py::test_downstream_and_external_authorities_remain_closed[approval_rerun_performed]",
        "tests/test_marketflow_signal_or_feature_generation_execution_service.py::test_downstream_and_external_authorities_remain_closed[automatic_stitching]",
    )),
    ("tests/test_marketflow_objective_label_or_target_generation_execution_service.py", 48, (
        "tests/test_marketflow_objective_label_or_target_generation_execution_service.py::test_availability_no_peek_report_has_all_rules",
        "tests/test_marketflow_objective_label_or_target_generation_execution_service.py::test_checklist_passes_completely",
        "tests/test_marketflow_objective_label_or_target_generation_execution_service.py::test_closed_execution_flags_remain_false[approval_rerun_performed]",
        "tests/test_marketflow_objective_label_or_target_generation_execution_service.py::test_closed_execution_flags_remain_false[candidate_creation_rerun_performed]",
        "tests/test_marketflow_objective_label_or_target_generation_execution_service.py::test_closed_execution_flags_remain_false[candidate_review_rerun_performed]",
    )),
    ("tests/test_feature_generation_execution_redesigned_labels_service.py", 28, (
        "tests/test_feature_generation_execution_redesigned_labels_service.py::test_alignment_and_quality_reports_created",
        "tests/test_feature_generation_execution_redesigned_labels_service.py::test_all_expected_outputs_created",
        "tests/test_feature_generation_execution_redesigned_labels_service.py::test_artifact_kind_and_status",
        "tests/test_feature_generation_execution_redesigned_labels_service.py::test_baseline_error_context_is_unavailable",
        "tests/test_feature_generation_execution_redesigned_labels_service.py::test_bound_digest[feature_generation_approval_using_redesigned_labels_digest-595bb9685936979810cfe6e3a814ea9ef38e0e3d89b804426a2d540ec77471c1]",
    )),
    ("tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py", 17, (
        "tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py::test_aa_baseline_model_comparison_is_verified",
        "tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py::test_ab_metric_family_results_are_verified",
        "tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py::test_ad_calibration_stability_report_is_verified",
        "tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py::test_ag_per_ticker_review_is_verified",
        "tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py::test_aj_optional_model_unavailability_is_recorded",
    )),
    ("tests/test_live_month_rth_diagnostic.py", 4, (
        "tests/test_live_month_rth_diagnostic.py::test_accepted_source_receipt_reports_january_rth_row_reconciliation",
        "tests/test_live_month_rth_diagnostic.py::test_cli_package_and_source_runtime_boundary_are_sealed",
        "tests/test_live_month_rth_diagnostic.py::test_public_source_evidence_and_plan_are_cwd_independent",
        "tests/test_live_month_rth_diagnostic.py::test_shadow_cwd_marketflow_tree_is_not_read",
    )),
    ("tests/test_fixed_profile_orchestrator.py", 3, (
        "tests/test_fixed_profile_orchestrator.py::test_blocked_normal_cli_does_not_import_advanced_or_provider_modules",
        "tests/test_fixed_profile_orchestrator.py::test_normal_cli_rejects_semantic_options_and_malformed_ticker",
        "tests/test_fixed_profile_orchestrator.py::test_normal_cli_runs_without_streamlit_import_for_blocked_local_data",
    )),
    ("tests/test_ticker_event_audit.py", 3, (
        "tests/test_ticker_event_audit.py::test_live_command_endpoint_failure_reports_request_without_artifact",
        "tests/test_ticker_event_audit.py::test_live_command_parse_failure_reports_request_and_raw_artifact",
        "tests/test_ticker_event_audit.py::test_live_command_success_uses_one_mock_request_after_getpass",
    )),
    ("tests/test_dataset_file_availability_verification_service.py", 2, (
        "tests/test_dataset_file_availability_verification_service.py::test_dataset_file_sha256_is_computed",
        "tests/test_dataset_file_availability_verification_service.py::test_manifest_file_sha256_is_computed",
    )),
    ("tests/test_position_swing_canonical_dataset_operator_review_service.py", 2, (
        "tests/test_position_swing_canonical_dataset_operator_review_service.py::test_build_from_candidate_object_uses_object_binding",
        "tests/test_position_swing_canonical_dataset_operator_review_service.py::test_local_ignored_dataset_manifest_and_candidate_are_verified_when_available",
    )),
    ("tests/test_artifact_lineage_v1.py", 1, (
        "tests/test_artifact_lineage_v1.py::test_canonical_cli_receipts_and_no_geometry_override",
    )),
    ("tests/test_expanded_universe_per_ticker_identity_authority_candidate_operator_review_service.py", 1, (
        "tests/test_expanded_universe_per_ticker_identity_authority_candidate_operator_review_service.py::test_status_bound_review_package_binds_recorded_candidate_digest",
    )),
    ("tests/test_packaging_integrity.py", 1, (
        "tests/test_packaging_integrity.py::test_generated_packaging_artifacts_are_ignored_by_git",
    )),
    ("tests/test_position_swing_registry_approval_service.py", 1, (
        "tests/test_position_swing_registry_approval_service.py::test_candidate_can_bind_to_supplied_position_swing_frozen_artifact",
    )),
    ("tests/test_read_only_registry_discovery_operator_review_service.py", 1, (
        "tests/test_read_only_registry_discovery_operator_review_service.py::test_review_package_can_bind_supplied_discovery_candidate",
    )),
    ("tests/test_source_assurance.py", 1, (
        "tests/test_source_assurance.py::test_packaging_metadata_directory_is_ignored_and_untracked",
    )),
    ("tests/test_swing_canonical_dataset_operator_review_service.py", 1, (
        "tests/test_swing_canonical_dataset_operator_review_service.py::test_local_ignored_dataset_and_manifest_are_verified_when_available",
    )),
    ("tests/test_swing_registry_approval_service.py", 1, (
        "tests/test_swing_registry_approval_service.py::test_candidate_can_bind_to_supplied_frozen_artifact",
    )),
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_COMPLETE_29_ROW_SOURCE_CREATED = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_ONLY_COMPLETE_DETAIL_SOURCE_CREATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE

OUTPUT_IDS = [
    "complete_29_row_materialization_execution_manifest", "complete_29_row_module_grouping_detail_source",
    "complete_29_row_payload_source_selection_report", "complete_29_row_payload_integrity_report",
    "source_derived_module_paths_report", "per_module_counts_report", "bounded_nodeid_samples_report",
    "top_module_concentration_preservation_report", "tier_sum_preservation_report",
    "digest_is_not_payload_report", "unsupported_claims_boundary_report",
    "materialization_limitations_report", "detail_binding_reattempt_enablement_report", "digest_manifest",
]

SUCCESS_NEXT_CHAIN = [
    "Complete 29-row Module Grouping Detail Source Materialization Results Review v1.",
    "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.", "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Complete 29-row Materialization Execution Failure Diagnosis v1.",
    "Alternate materialization or binding candidate, if needed.",
    "No detail-binding reattempt, planning reentry, diagnostic capture, retry, or main merge.",
]
SUCCESS_NEXT_GATES = [
    "complete_29_row_module_grouping_detail_source_materialization_results_review",
    "detail_exposure_or_binding_execution_reattempt_with_complete_source", "detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported", "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected", "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review", "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "complete_29_row_materialization_execution_failure_diagnosis",
    "alternate_materialization_or_binding_candidate_if_needed",
    "detail_binding_reattempt_blocked_until_materialization_review_passes",
    "main_merge_blocked_until_new_retry_results_review_passes",
]

RISK_CONTROLS = [
    "materialization_execution_verifies_reviewed_cache_hashes_before_use", "materialization_execution_reads_cache_read_only",
    "materialization_execution_does_not_modify_cache", "materialization_execution_does_not_commit_pytest_cache",
    "materialization_execution_does_not_commit_marketflow_outputs", "materialization_execution_does_not_rerun_source_recovery",
    "materialization_execution_does_not_call_source_recovery_execution_for_cache_read",
    "materialization_execution_does_not_parse_operator_logs", "materialization_execution_does_not_run_diagnostic_commands",
    "materialization_execution_does_not_execute_diagnostics", "materialization_execution_does_not_execute_remediation",
    "materialization_execution_does_not_execute_classification", "materialization_execution_does_not_classify_modules_again",
    "materialization_execution_does_not_execute_detail_binding_reattempt",
    "materialization_execution_does_not_execute_after_v2_planning_reentry", "materialization_execution_does_not_rerun_retry",
    "materialization_execution_does_not_run_full_pytest", "materialization_execution_does_not_create_targeted_diagnostic_candidate",
    "materialization_execution_does_not_create_new_retry_candidate", "materialization_execution_does_not_create_retry_results_review",
    "materialization_execution_does_not_create_integration_results_review", "materialization_execution_does_not_mark_integration_successful",
    "materialization_execution_does_not_generate_successful_integration_digest",
    "materialization_execution_does_not_claim_failure_error_separation", "materialization_execution_does_not_claim_first_failure",
    "materialization_execution_does_not_claim_first_error", "materialization_execution_does_not_claim_traceback_root_cause",
    "materialization_execution_does_not_recommend_direct_code_remediation",
    "materialization_execution_does_not_treat_digest_as_payload", "materialization_execution_does_not_treat_detail_as_retry_success",
    "materialization_execution_does_not_push_integration_branch", "materialization_execution_does_not_push_main",
    "materialization_execution_does_not_delete_integration_branch", "materialization_execution_does_not_delete_worktree",
    "materialization_execution_does_not_force_push", "materialization_execution_does_not_prune_remotes",
    "materialization_execution_does_not_modify_tags", "materialization_execution_does_not_modify_staged_evidence",
    "materialization_execution_does_not_regenerate_evidence", "materialization_execution_does_not_call_providers",
    "materialization_execution_does_not_acquire_market_data", "materialization_execution_does_not_regenerate_dataset",
    "materialization_execution_does_not_recompute_metrics", "materialization_execution_does_not_train_models",
    "materialization_execution_does_not_score_strategy", "materialization_execution_does_not_generate_recommendations",
    "materialization_execution_does_not_accept_predictive_usefulness", "materialization_execution_does_not_accept_profitability",
    "materialization_execution_does_not_authorize_runtime", "materialization_execution_does_not_authorize_broker_execution",
    "complete_29_row_materialization_output_is_planning_source_not_root_cause", "cache_hash_match_required_before_materialization",
    "lastfailed_subset_of_nodeids_required", "bounded_samples_required_max_5", "complete_detail_gap_is_not_retry_success",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures", "previous_blocked_execution_remains_historically_blocked",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_results_review_required_after_materialization",
    "separate_detail_binding_reattempt_required_after_materialization_review", "separate_retry_approval_required_before_new_retry",
    "protect_origin_main", "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags", "preserve_meta_limitation",
]

FALSE_BOUNDARIES = [
    "detail_exposure_or_binding_reattempt_created", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "source_recovery_rerun_performed", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed", "classification_execution_performed_in_execution",
    "integration_execution_successful", "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
    "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]
UNSUPPORTED_CLAIMS_FIELDS = [
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError(ValueError):
    """Raised when materialization execution evidence violates its contract."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _normalize_nodeids(value: Any) -> list[str]:
    if isinstance(value, dict):
        values = value.keys()
    elif isinstance(value, list):
        values = value
    else:
        raise ValueError("cache JSON must be an object or list")
    result = sorted(str(item) for item in values)
    if not result:
        raise ValueError("cache JSON is empty")
    return result


def _cache_paths(cache_root: Path) -> tuple[Path, Path]:
    candidates = [cache_root, cache_root / "v" / "cache", cache_root / ".pytest_cache" / "v" / "cache"]
    for candidate in candidates:
        if (candidate / "lastfailed").is_file() or (candidate / "nodeids").is_file():
            return candidate / "lastfailed", candidate / "nodeids"
    return cache_root / "lastfailed", cache_root / "nodeids"


def _read_cache(cache_root: Path, snapshot: dict | None) -> dict[str, Any]:
    last_path, node_path = _cache_paths(cache_root)
    if snapshot is not None:
        return {
            "lastfailed_path": str(last_path), "nodeids_path": str(node_path),
            "lastfailed_sha256": snapshot.get("lastfailed_sha256", EXPECTED_LASTFAILED_SHA256),
            "nodeids_sha256": snapshot.get("nodeids_sha256", EXPECTED_NODEIDS_SHA256),
            "lastfailed": _normalize_nodeids(snapshot["lastfailed"]),
            "nodeids": _normalize_nodeids(snapshot["nodeids"]),
            "lastfailed_read": True, "nodeids_read": True,
            "lastfailed_parseable": True, "nodeids_parseable": True,
            "deterministic_test_snapshot_injected": True,
        }
    last_raw = last_path.read_bytes()
    node_raw = node_path.read_bytes()
    return {
        "lastfailed_path": str(last_path), "nodeids_path": str(node_path),
        "lastfailed_sha256": hashlib.sha256(last_raw).hexdigest(),
        "nodeids_sha256": hashlib.sha256(node_raw).hexdigest(),
        "lastfailed": _normalize_nodeids(json.loads(last_raw)),
        "nodeids": _normalize_nodeids(json.loads(node_raw)),
        "lastfailed_read": True, "nodeids_read": True,
        "lastfailed_parseable": True, "nodeids_parseable": True,
        "deterministic_test_snapshot_injected": False,
    }


def _source_fields(source_approval: dict | None) -> dict[str, Any]:
    if source_approval is not None:
        approval_source.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(source_approval)
        digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
        if source_approval.get(digest_key) != SOURCE_APPROVAL_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("source approval digest mismatch")
        if source_approval.get("ready_for_complete_29_row_materialization_execution") is not True:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("source approval does not authorize execution")
        base = source_approval
    else:
        review = approval_source._committed_source_review()
        base = {
            "source_complete_29_row_materialization_operator_review_digest": approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
            "source_complete_29_row_materialization_candidate_digest": review["source_complete_29_row_materialization_candidate_digest"],
            **{field: deepcopy(review[field]) for field in approval_source.SOURCE_COPY_FIELDS},
            "source_detail_exposure_or_binding_execution_blocked_reason": review["blocked_reason"],
            "ready_for_complete_29_row_materialization_execution": True,
        }
    fields = [
        "source_complete_29_row_materialization_operator_review_digest",
        "source_complete_29_row_materialization_candidate_digest",
        "source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "primary_failure_class",
        "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_detail_exposure_or_binding_execution_blocked_manifest_digest",
        "source_detail_exposure_or_binding_execution_blocked_reason",
        "source_detail_exposure_or_binding_approval_digest", "source_detail_exposure_or_binding_operator_review_digest",
        "source_detail_exposure_or_binding_candidate_digest", "source_reentry_failure_diagnosis_digest",
        "source_primary_failure_class", "source_reentry_execution_blocked_digest",
        "source_reentry_execution_blocked_manifest_digest", "source_reentry_execution_blocked_reason",
        "source_after_v2_planning_reentry_digest", "source_module_grouping_source_recovery_results_review_digest",
        "source_module_grouping_source_recovery_results_review_manifest_digest",
        "source_module_grouping_source_recovery_execution_digest", "source_module_grouping_source_recovery_detail_digest",
        "source_module_grouping_source_recovery_digest_manifest_digest", "source_module_grouping_source_recovery_approval_digest",
        "source_module_grouping_source_recovery_operator_review_digest", "source_module_grouping_source_recovery_candidate_digest",
        "source_blocked_after_v2_execution_digest", "source_blocked_after_v2_manifest_digest",
        "source_after_v2_approval_digest", "source_after_v2_operator_review_digest", "source_after_v2_candidate_digest",
        "source_results_review_v2_digest", "source_execution_v2_digest", "source_module_grouping_digest",
        "source_approval_v2_digest", "source_staged_inventory_digest", "retry_execution_commit", "retry_failure_context",
        "recovered_module_grouping_source_summary", "top_module_summary",
    ]
    return {
        "source_complete_29_row_materialization_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_approval_authorizes_execution": base["ready_for_complete_29_row_materialization_execution"],
        "source_reentry_failure_primary_failure_class": base["source_primary_failure_class"],
        **{field: deepcopy(base[field]) for field in fields},
    }


def _common(source_approval: dict | None, timestamp: str, cache_root: Path) -> dict[str, Any]:
    common = {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_complete_29_row_materialization_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        "created_offline": True, "governance_only": True, "materialization_execution_only": True,
        "run_timestamp_utc": timestamp, **_source_fields(source_approval),
        "source_complete_29_row_materialization_approval_artifact_kind": approval_source.ARTIFACT_KIND,
        "source_complete_29_row_materialization_approval_status": approval_source.APPROVAL_STATUS,
        "source_complete_29_row_materialization_approval_scope": approval_source.APPROVAL_SCOPE,
        "materialization_package_executed": True,
        "complete_29_row_detail_source_type": ROW_SOURCE,
        "complete_29_row_detail_source_basis": "REVIEWED_CACHE_HASHES_COUNTS_SUBSET_CHECK_AND_RECOVERY_CHAIN_DIGESTS",
        "module_paths_recovered_by_execution": False, "per_module_counts_recovered_by_execution": False,
        "bounded_nodeid_samples_recovered_by_execution": False, "module_grouping_recovered_in_execution": False,
        "cache_root": str(cache_root), "cache_modified": False,
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "staged_evidence_manifest_digest": "06d19e5e81485e416fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False, "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False, "pytest_cache_tracked_in_detached_worktree": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "risk_controls": list(RISK_CONTROLS),
    }
    common.update({field: False for field in FALSE_BOUNDARIES})
    common.update({field: False for field in UNSUPPORTED_CLAIMS_FIELDS})
    return common


def _verification(cache: Mapping[str, Any]) -> dict[str, Any]:
    nodeids = set(cache["nodeids"])
    return {
        "lastfailed_path": cache["lastfailed_path"], "lastfailed_read": cache["lastfailed_read"],
        "lastfailed_parseable_json": cache["lastfailed_parseable"],
        "lastfailed_sha256_expected": EXPECTED_LASTFAILED_SHA256,
        "lastfailed_sha256_actual": cache["lastfailed_sha256"],
        "lastfailed_hash_verified": cache["lastfailed_sha256"] == EXPECTED_LASTFAILED_SHA256,
        "lastfailed_entry_count_expected": EXPECTED_LASTFAILED_COUNT,
        "lastfailed_entry_count_actual": len(cache["lastfailed"]),
        "nodeids_path": cache["nodeids_path"], "nodeids_read": cache["nodeids_read"],
        "nodeids_parseable_json": cache["nodeids_parseable"],
        "nodeids_sha256_expected": EXPECTED_NODEIDS_SHA256,
        "nodeids_sha256_actual": cache["nodeids_sha256"],
        "nodeids_hash_verified": cache["nodeids_sha256"] == EXPECTED_NODEIDS_SHA256,
        "nodeids_entry_count_expected": EXPECTED_NODEIDS_COUNT,
        "nodeids_entry_count_actual": len(cache["nodeids"]),
        "entry_counts_verified": len(cache["lastfailed"]) == EXPECTED_LASTFAILED_COUNT and len(cache["nodeids"]) == EXPECTED_NODEIDS_COUNT,
        "lastfailed_subset_of_nodeids": all(nodeid in nodeids for nodeid in cache["lastfailed"]),
        "deterministic_test_snapshot_injected": cache["deterministic_test_snapshot_injected"],
    }


def _materialized_rows(lastfailed: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for nodeid in lastfailed:
        grouped[nodeid.split("::", 1)[0]].append(nodeid)
    counts = Counter({path: len(nodeids) for path, nodeids in grouped.items()})
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    rows = []
    for rank, (module_path, count) in enumerate(ordered, 1):
        tier = "PRIORITY_1_TOP_5_MODULE_GROUPS" if rank <= 5 else "PRIORITY_2_NEXT_5_MODULE_GROUPS" if rank <= 10 else "PRIORITY_3_REMAINING_MODULE_GROUPS"
        samples = sorted(grouped[module_path])[:5]
        rows.append({
            "module_path": module_path, "failed_or_errored_nodeid_count": count,
            "percentage_of_failed_or_errored_nodeids": f"{count * 100 / EXPECTED_LASTFAILED_COUNT:.8f}",
            "priority_order": rank, "priority_tier": tier,
            "sample_nodeids_bounded": samples, "sample_nodeids_bounded_count": len(samples),
            "source": ROW_SOURCE, "basis": ROW_BASIS, "confidence": ROW_CONFIDENCE,
            "unsupported_claims": list(UNSUPPORTED_ROW_CLAIMS),
        })
    return rows


def committed_complete_29_row_module_grouping_detail_source_v1() -> list[dict[str, Any]]:
    """Return the tracked, bounded source created by the reviewed materialization."""

    rows: list[dict[str, Any]] = []
    for rank, (module_path, count, samples) in enumerate(
        COMMITTED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE, 1
    ):
        tier = "PRIORITY_1_TOP_5_MODULE_GROUPS" if rank <= 5 else "PRIORITY_2_NEXT_5_MODULE_GROUPS" if rank <= 10 else "PRIORITY_3_REMAINING_MODULE_GROUPS"
        rows.append({
            "module_path": module_path,
            "failed_or_errored_nodeid_count": count,
            "percentage_of_failed_or_errored_nodeids": f"{count * 100 / EXPECTED_LASTFAILED_COUNT:.8f}",
            "priority_order": rank,
            "priority_tier": tier,
            "sample_nodeids_bounded": list(samples),
            "sample_nodeids_bounded_count": len(samples),
            "source": ROW_SOURCE,
            "basis": ROW_BASIS,
            "confidence": ROW_CONFIDENCE,
            "unsupported_claims": list(UNSUPPORTED_ROW_CLAIMS),
        })
    return rows


def _integrity_reasons(verification: Mapping[str, Any], rows: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    if verification.get("lastfailed_hash_verified") is not True: reasons.append("LASTFAILED_CACHE_SHA256_MISMATCH")
    if verification.get("nodeids_hash_verified") is not True: reasons.append("NODEIDS_CACHE_SHA256_MISMATCH")
    if verification.get("entry_counts_verified") is not True: reasons.append("REVIEWED_CACHE_ENTRY_COUNT_MISMATCH")
    if verification.get("lastfailed_subset_of_nodeids") is not True: reasons.append("LASTFAILED_NOT_SUBSET_OF_NODEIDS")
    if len(rows) != EXPECTED_MODULE_COUNT: reasons.append("COMPLETE_29_ROW_DETAIL_ROW_COUNT_MISMATCH")
    if any(not isinstance(row, Mapping) for row in rows):
        reasons.append("MATERIALIZED_ROW_INVALID")
        return reasons
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows]
    paths = [row.get("module_path") for row in rows]
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 1 for value in counts):
        reasons.append("PER_MODULE_COUNT_INVALID")
        return reasons
    if any(not isinstance(path, str) or not path for path in paths):
        reasons.append("MODULE_PATH_INVALID")
        return reasons
    if sum(counts) != EXPECTED_LASTFAILED_COUNT: reasons.append("FAILED_OR_ERRORED_NODEID_TOTAL_MISMATCH")
    if counts[:5] != EXPECTED_LARGEST_COUNTS: reasons.append("TOP_FIVE_COUNTS_MISMATCH")
    if paths[:5] != EXPECTED_TOP_FIVE_PATHS: reasons.append("TOP_FIVE_MODULE_PATHS_MISMATCH")
    if sum(counts[:5]) != 612: reasons.append("TOP_FIVE_SUM_MISMATCH")
    if sum(counts[:10]) != 1069: reasons.append("TOP_TEN_SUM_MISMATCH")
    if sum(counts[5:10]) != 457: reasons.append("PRIORITY_TIER_2_SUM_MISMATCH")
    if sum(counts[10:]) != 335: reasons.append("PRIORITY_TIER_3_SUM_MISMATCH")
    if any(
        not isinstance(row.get("sample_nodeids_bounded"), list)
        or not row["sample_nodeids_bounded"]
        or len(row["sample_nodeids_bounded"]) > 5
        or row.get("sample_nodeids_bounded_count") != len(row["sample_nodeids_bounded"])
        or any(not isinstance(nodeid, str) or not nodeid for nodeid in row["sample_nodeids_bounded"])
        for row in rows
    ):
        reasons.append("BOUNDED_NODEID_SAMPLES_INVALID")
    expected_tiers = [
        "PRIORITY_1_TOP_5_MODULE_GROUPS" if rank <= 5 else "PRIORITY_2_NEXT_5_MODULE_GROUPS" if rank <= 10 else "PRIORITY_3_REMAINING_MODULE_GROUPS"
        for rank in range(1, len(rows) + 1)
    ]
    if [row.get("priority_order") for row in rows] != list(range(1, len(rows) + 1)):
        reasons.append("PRIORITY_ORDER_INVALID")
    if [row.get("priority_tier") for row in rows] != expected_tiers:
        reasons.append("PRIORITY_TIER_INVALID")
    if any(
        row.get("percentage_of_failed_or_errored_nodeids") != f"{row['failed_or_errored_nodeid_count'] * 100 / EXPECTED_LASTFAILED_COUNT:.8f}"
        or row.get("source") != ROW_SOURCE
        or row.get("basis") != ROW_BASIS
        or row.get("confidence") != ROW_CONFIDENCE
        or row.get("unsupported_claims") != UNSUPPORTED_ROW_CLAIMS
        for row in rows
    ):
        reasons.append("MATERIALIZED_ROW_BOUNDARY_INVALID")
    if verification.get("committed_source_rows_match") is False:
        reasons.append("MATERIALIZED_ROWS_DO_NOT_MATCH_COMMITTED_SOURCE")
    return reasons


def _success(common: dict[str, Any], verification: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    top_five = rows[:5]
    top_ten = rows[:10]
    top_report = {
        "top_5_module_paths": [row["module_path"] for row in top_five],
        "top_5_counts": [row["failed_or_errored_nodeid_count"] for row in top_five],
        "top_5_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in top_five),
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in top_ten),
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tier_report = {
        "priority_tier_1_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in rows[:5]),
        "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in rows[5:10]),
        "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": sum(row["failed_or_errored_nodeid_count"] for row in rows[10:]),
        "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }
    payload_digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest"
    manifest_digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest"
    payload_digest = semantic_digest(rows)
    selection_report = {
        "selected_source": ROW_SOURCE, "basis": common["complete_29_row_detail_source_basis"],
        "selected_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
    }
    integrity_report = {
        "row_count": len(rows), "failed_or_errored_nodeids_count": sum(row["failed_or_errored_nodeid_count"] for row in rows),
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        **top_report, **tier_report,
    }
    limitations = [
        "materialized cache evidence does not separate failures from errors",
        "materialized cache evidence does not preserve first-failure order",
        "materialized cache evidence does not provide tracebacks or root cause",
        "materialized detail is planning source only and is not retry success or merge readiness",
    ]
    enablement = {
        "ready_for_complete_29_row_materialization_results_review": True,
        "detail_binding_reattempt_requires_materialization_results_review": True,
        "detail_binding_reattempt_created": False,
    }
    digest_manifest = {
        "materialized_payload": payload_digest,
        "cache_verification": semantic_digest(verification),
        "source_selection": semantic_digest(selection_report),
        "payload_integrity": semantic_digest(integrity_report),
        "top_module_concentration": semantic_digest(top_report),
        "priority_tiers": semantic_digest(tier_report),
        "unsupported_claims": semantic_digest(UNSUPPORTED_ROW_CLAIMS),
        "limitations": semantic_digest(limitations),
        "detail_binding_reattempt_enablement": semantic_digest(enablement),
    }
    execution = {
        **common, "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        "reviewed_cache_verification": verification,
        "used_reviewed_cache_read_only_for_materialization": True,
        "reviewed_cache_read_for_materialization": True, "cache_read_in_execution": True,
        "materialization_package_executed": True, "complete_29_row_detail_materialized": True,
        "complete_29_row_detail_exposed": True, "complete_29_row_detail_bound": True,
        "complete_29_row_detail_committed_source_created": True, "complete_29_row_detail_source_identified": True,
        "module_grouping_detail_materialized_by_execution": True,
        "module_paths_bound_by_execution": True, "per_module_counts_bound_by_execution": True,
        "bounded_nodeid_samples_bound_by_execution": True,
        "complete_29_row_module_grouping_detail_source": rows,
        "failed_or_errored_nodeids_count": EXPECTED_LASTFAILED_COUNT,
        "module_summary_module_count": len(rows),
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "top_5_count_sum": top_report["top_5_count_sum"],
        "top_5_percentage_of_failed_or_errored_nodeids": top_report["top_5_percentage_of_failed_or_errored_nodeids"],
        "top_10_count_sum": top_report["top_10_count_sum"],
        "top_10_percentage_of_failed_or_errored_nodeids": top_report["top_10_percentage_of_failed_or_errored_nodeids"],
        **tier_report,
        "complete_29_row_materialization_execution_manifest": {
            "source": ROW_SOURCE, "module_count": len(rows), "nodeid_count": EXPECTED_LASTFAILED_COUNT,
            "sample_nodeids_max_per_module": 5,
        },
        "complete_29_row_payload_source_selection_report": selection_report,
        "complete_29_row_payload_integrity_report": integrity_report,
        "source_derived_module_paths_report": [row["module_path"] for row in rows],
        "per_module_counts_report": [{"module_path": row["module_path"], "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"]} for row in rows],
        "bounded_nodeid_samples_report": [{"module_path": row["module_path"], "sample_nodeids_bounded": row["sample_nodeids_bounded"]} for row in rows],
        "top_module_concentration_preservation_report": top_report,
        "tier_sum_preservation_report": tier_report,
        "digest_is_not_payload_report": {"digest_is_payload": False, "payload_materialized_separately": True},
        "unsupported_claims_boundary_report": list(UNSUPPORTED_ROW_CLAIMS),
        "materialization_limitations_report": limitations,
        "detail_binding_reattempt_enablement_report": enablement,
        "digest_manifest": digest_manifest,
        payload_digest_key: payload_digest, manifest_digest_key: semantic_digest(digest_manifest),
        "outputs_generated": [{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
        "ready_for_complete_29_row_materialization_results_review": True,
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "recommended_next_task": SUCCESS_NEXT_TASK, "blocked_reason": None,
    }
    return execution


def _blocked(common: dict[str, Any], verification: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    blocked_reason = ";".join(dict.fromkeys(reasons))
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_blocked_manifest_digest"
    return {
        **common, "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        "reviewed_cache_verification": verification,
        "used_reviewed_cache_read_only_for_materialization": False,
        "reviewed_cache_read_for_materialization": bool(verification.get("lastfailed_read") or verification.get("nodeids_read")),
        "cache_read_in_execution": bool(verification.get("lastfailed_read") or verification.get("nodeids_read")),
        "materialization_package_executed": True, "complete_29_row_detail_materialized": False,
        "complete_29_row_detail_exposed": False, "complete_29_row_detail_bound": False,
        "complete_29_row_detail_committed_source_created": False, "complete_29_row_detail_source_identified": False,
        "module_grouping_detail_materialized_by_execution": False,
        "module_paths_bound_by_execution": False, "per_module_counts_bound_by_execution": False,
        "bounded_nodeid_samples_bound_by_execution": False,
        "complete_29_row_module_grouping_detail_source": [],
        "failed_or_errored_nodeids_count": 0, "module_summary_module_count": 0,
        "largest_module_nodeid_counts": [], "top_5_count_sum": 0, "top_10_count_sum": 0,
        "priority_tier_1_count_sum": 0, "priority_tier_2_count_sum": 0, "priority_tier_3_count_sum": 0,
        "outputs_generated": [], "blocked_reason": blocked_reason,
        "available_data": ["source digests", "retry counts", "reviewed cache paths if present", "cache hash verification result", "any available module grouping facts"],
        "missing_data": list(dict.fromkeys(reasons)),
        digest_key: semantic_digest({"blocked_reason": blocked_reason, "reviewed_cache_verification": verification}),
        "ready_for_complete_29_row_materialization_results_review": False,
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        "recommended_next_task": BLOCKED_NEXT_TASK,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    expected_source = _source_fields(None)
    verification = execution.get("reviewed_cache_verification", {})
    rows = execution.get("complete_29_row_module_grouping_detail_source", [])
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (SOURCE_APPROVAL_DIGEST, execution.get("source_complete_29_row_materialization_approval_digest")),
        "source_operator_review_digest_bound": (expected_source["source_complete_29_row_materialization_operator_review_digest"], execution.get("source_complete_29_row_materialization_operator_review_digest")),
        "source_candidate_digest_bound": (expected_source["source_complete_29_row_materialization_candidate_digest"], execution.get("source_complete_29_row_materialization_candidate_digest")),
        "source_diagnosis_digest_bound": (expected_source["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"], execution.get("source_detail_exposure_or_binding_execution_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (expected_source["primary_failure_class"], execution.get("primary_failure_class")),
        "source_detail_binding_blocked_execution_digest_bound": (expected_source["source_detail_exposure_or_binding_execution_blocked_digest"], execution.get("source_detail_exposure_or_binding_execution_blocked_digest")),
        "source_detail_binding_blocked_manifest_digest_bound": (expected_source["source_detail_exposure_or_binding_execution_blocked_manifest_digest"], execution.get("source_detail_exposure_or_binding_execution_blocked_manifest_digest")),
        "source_detail_binding_blocked_reason_bound": (expected_source["source_detail_exposure_or_binding_execution_blocked_reason"], execution.get("source_detail_exposure_or_binding_execution_blocked_reason")),
        "source_detail_binding_approval_digest_bound": (expected_source["source_detail_exposure_or_binding_approval_digest"], execution.get("source_detail_exposure_or_binding_approval_digest")),
        "source_detail_binding_operator_review_digest_bound": (expected_source["source_detail_exposure_or_binding_operator_review_digest"], execution.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_detail_binding_candidate_digest_bound": (expected_source["source_detail_exposure_or_binding_candidate_digest"], execution.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_reentry_failure_diagnosis_digest_bound": (expected_source["source_reentry_failure_diagnosis_digest"], execution.get("source_reentry_failure_diagnosis_digest")),
        "source_reentry_blocked_execution_digest_bound": (expected_source["source_reentry_execution_blocked_digest"], execution.get("source_reentry_execution_blocked_digest")),
        "source_reentry_blocked_manifest_digest_bound": (expected_source["source_reentry_execution_blocked_manifest_digest"], execution.get("source_reentry_execution_blocked_manifest_digest")),
        "source_planning_reentry_digest_bound": (expected_source["source_after_v2_planning_reentry_digest"], execution.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (expected_source["source_module_grouping_source_recovery_results_review_digest"], execution.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (expected_source["source_module_grouping_source_recovery_results_review_manifest_digest"], execution.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (expected_source["source_module_grouping_source_recovery_execution_digest"], execution.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (expected_source["source_module_grouping_source_recovery_detail_digest"], execution.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (expected_source["source_module_grouping_source_recovery_digest_manifest_digest"], execution.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (expected_source["source_blocked_after_v2_execution_digest"], execution.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (expected_source["source_blocked_after_v2_manifest_digest"], execution.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (expected_source["source_after_v2_approval_digest"], execution.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (expected_source["source_results_review_v2_digest"], execution.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (expected_source["source_execution_v2_digest"], execution.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (expected_source["source_module_grouping_digest"], execution.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (expected_source["retry_execution_commit"], execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": (expected_source["retry_failure_context"]["counts"], execution.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": (expected_source["recovered_module_grouping_source_summary"], execution.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (expected_source["top_module_summary"], execution.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, execution.get("top_5_count_sum") if success else 612),
        "top_ten_count_sum_1069_bound": (1069, execution.get("top_10_count_sum") if success else 1069),
        "approval_authorizes_execution_true": (True, execution.get("source_approval_authorizes_execution")),
        "reviewed_cache_lastfailed_hash_verified_if_success": (success, success and verification.get("lastfailed_hash_verified") is True),
        "reviewed_cache_nodeids_hash_verified_if_success": (success, success and verification.get("nodeids_hash_verified") is True),
        "reviewed_cache_entry_counts_verified_if_success": (success, success and verification.get("entry_counts_verified") is True),
        "lastfailed_subset_of_nodeids_if_success": (success, success and verification.get("lastfailed_subset_of_nodeids") is True),
        "materialization_package_executed_true": (True, execution.get("materialization_package_executed")),
        "complete_29_row_detail_materialized_true_if_success": (success, execution.get("complete_29_row_detail_materialized")),
        "complete_29_row_detail_exposed_true_if_success": (success, execution.get("complete_29_row_detail_exposed")),
        "complete_29_row_detail_bound_true_if_success": (success, execution.get("complete_29_row_detail_bound")),
        "complete_29_row_detail_committed_source_created_true_if_success": (success, execution.get("complete_29_row_detail_committed_source_created")),
        "complete_29_row_detail_source_identified_true_if_success": (success, execution.get("complete_29_row_detail_source_identified")),
        "complete_29_row_rows_exactly_29_if_success": (EXPECTED_MODULE_COUNT if success else 0, len(rows)),
        "failed_or_errored_nodeids_1404_if_success": (EXPECTED_LASTFAILED_COUNT if success else 0, sum(value for value in counts if isinstance(value, int))),
        "largest_module_counts_if_success": (EXPECTED_LARGEST_COUNTS if success else [], counts[:5]),
        "top_five_paths_preserved_if_success": (EXPECTED_TOP_FIVE_PATHS if success else [], paths[:5]),
        "top_five_sum_612_if_success": (612 if success else 0, sum(counts[:5])),
        "top_ten_sum_1069_if_success": (1069 if success else 0, sum(counts[:10])),
        "tier_1_sum_612_if_success": (612 if success else 0, sum(counts[:5])),
        "tier_2_sum_457_if_success": (457 if success else 0, sum(counts[5:10])),
        "tier_3_sum_335_if_success": (335 if success else 0, sum(counts[10:])),
        "bounded_samples_max_5_if_success": (success, success and bool(rows) and all(0 < len(row.get("sample_nodeids_bounded", [])) <= 5 for row in rows)),
        "payload_digest_generated_if_success": (success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest"))),
        "digest_manifest_digest_generated_if_success": (success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest"))),
        "blocked_reason_recorded_if_blocked": (not success, bool(execution.get("blocked_reason"))),
        "blocked_manifest_digest_generated_if_blocked": (not success, bool(execution.get("marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_blocked_manifest_digest"))),
    }
    false_map = {
        "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed",
        "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed", "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "detail_binding_reattempt_created_false": "detail_exposure_or_binding_reattempt_created",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created",
        "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created", "source_recovery_rerun_false": "source_recovery_rerun_performed",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_execution",
        "integration_success_false": "integration_execution_successful", "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed", "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed", "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated", "provider_requests_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution",
        "dataset_generation_false": "dataset_generation_performed_in_execution",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, execution.get(field)) for check_id, field in false_map.items()})
    values.update({
        "successful_integration_digest_false": ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")]),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, execution.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, execution.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, execution.get("broker_execution")),
        "next_chain_defined": (SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN, execution.get("next_chain")),
        "next_gates_defined": (SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES, execution.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (False, execution.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, execution.get("pytest_cache_tracked_in_repository")),
    })
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]], success: bool) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    result = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "materialization_package_executed": execution.get("materialization_package_executed"),
        "complete_29_row_detail_materialized": execution.get("complete_29_row_detail_materialized"),
        "complete_29_row_detail_exposed": execution.get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound": execution.get("complete_29_row_detail_bound"),
        "complete_29_row_detail_committed_source_created": execution.get("complete_29_row_detail_committed_source_created"),
        "detail_exposure_or_binding_reattempt_created": execution.get("detail_exposure_or_binding_reattempt_created"),
        "after_v2_planning_execution_reentry_created": execution.get("after_v2_planning_execution_reentry_created"),
        "after_v2_planning_execution_reentry_performed": execution.get("after_v2_planning_execution_reentry_performed"),
        "targeted_diagnostic_output_capture_candidate_created": execution.get("targeted_diagnostic_output_capture_candidate_created"),
        "new_retry_candidate_created": execution.get("new_retry_candidate_created"),
        "new_retry_executed": execution.get("new_retry_executed"),
        "integration_execution_successful": execution.get("integration_execution_successful"),
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if success:
        result.update({field: execution.get(field) for field in (
            "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
            "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
            "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
            "priority_tier_2_count_sum", "priority_tier_3_count_sum",
            "ready_for_complete_29_row_materialization_results_review",
        )})
    else:
        result["blocked_reason"] = execution.get("blocked_reason")
    return result


def marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist", "summary",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
    *, source_approval: dict | None = None, complete_detail_snapshot: dict | None = None,
    cache_root: str | Path | None = None, run_timestamp_utc: str | None = None,
) -> dict:
    """Execute approved read-only materialization or return a blocked artifact."""

    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("run timestamp invalid")
    root = Path(cache_root) if cache_root is not None else DEFAULT_CACHE_ROOT
    common = _common(source_approval, timestamp, root)
    last_path, node_path = _cache_paths(root)
    try:
        cache = _read_cache(root, complete_detail_snapshot)
        verification = _verification(cache)
        rows = _materialized_rows(cache["lastfailed"])
        is_reviewed_source = (
            not cache["deterministic_test_snapshot_injected"]
            and cache["lastfailed_sha256"] == REVIEWED_LASTFAILED_SHA256
            and cache["nodeids_sha256"] == REVIEWED_NODEIDS_SHA256
        )
        verification["committed_source_rows_match"] = (
            rows == committed_complete_29_row_module_grouping_detail_source_v1()
            if is_reviewed_source
            else None
        )
        reasons = _integrity_reasons(verification, rows)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, KeyError) as exc:
        cache = {
            "lastfailed_path": str(last_path), "nodeids_path": str(node_path),
            "lastfailed_sha256": None, "nodeids_sha256": None, "lastfailed": [], "nodeids": [],
            "lastfailed_read": last_path.is_file(), "nodeids_read": node_path.is_file(),
            "lastfailed_parseable": False, "nodeids_parseable": False,
            "deterministic_test_snapshot_injected": complete_detail_snapshot is not None,
        }
        verification = _verification(cache)
        verification["committed_source_rows_match"] = None
        rows = []
        if not last_path.is_file() and complete_detail_snapshot is None:
            reasons = ["REVIEWED_LASTFAILED_CACHE_MISSING"]
        elif not node_path.is_file() and complete_detail_snapshot is None:
            reasons = ["REVIEWED_NODEIDS_CACHE_MISSING"]
        else:
            reasons = [f"CACHE_SOURCE_UNAVAILABLE_OR_UNPARSEABLE:{type(exc).__name__}"]
    execution = _success(common, verification, rows) if not reasons else _blocked(common, verification, reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest"
    execution[digest_key] = marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest_v1(execution)
    validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
    execution: dict,
) -> dict:
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, expected_status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, expected_status = False, BLOCKED_STATUS
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("artifact kind invalid")
    constants = {
        "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "selected_complete_29_row_materialization_package": SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        "source_complete_29_row_materialization_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_complete_29_row_materialization_approval_artifact_kind": approval_source.ARTIFACT_KIND,
        "source_complete_29_row_materialization_approval_status": approval_source.APPROVAL_STATUS,
        "source_complete_29_row_materialization_approval_scope": approval_source.APPROVAL_SCOPE,
    }
    constants.update(_source_fields(None))
    for field, expected in constants.items():
        if execution.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError(f"{field} mismatch")
    if not _iso_utc(execution.get("run_timestamp_utc")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("run timestamp invalid")
    if execution.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("risk controls mismatch")
    for field in FALSE_BOUNDARIES + UNSUPPORTED_CLAIMS_FIELDS:
        if execution.get(field) is not False:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError(f"{field} must be false")
    rows = execution.get("complete_29_row_module_grouping_detail_source")
    if not isinstance(rows, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("materialized rows missing")
    if success:
        reasons = _integrity_reasons(execution.get("reviewed_cache_verification", {}), rows)
        if reasons:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("success integrity invalid: " + ";".join(reasons))
        expected_true = [
            "materialization_package_executed", "complete_29_row_detail_materialized", "complete_29_row_detail_exposed",
            "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
            "complete_29_row_detail_source_identified", "module_grouping_detail_materialized_by_execution",
            "module_paths_bound_by_execution", "per_module_counts_bound_by_execution",
            "bounded_nodeid_samples_bound_by_execution", "ready_for_complete_29_row_materialization_results_review",
        ]
        if any(execution.get(field) is not True for field in expected_true):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("success flag missing")
        payload_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest"
        manifest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest"
        if execution.get(payload_key) != semantic_digest(rows):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("payload digest mismatch")
        if execution.get(manifest_key) != semantic_digest(execution.get("digest_manifest")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("digest manifest digest mismatch")
        if [item.get("output_id") for item in execution.get("outputs_generated", [])] != OUTPUT_IDS:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("generated outputs mismatch")
    else:
        if not execution.get("blocked_reason"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("blocked reason missing")
        blocked_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_blocked_manifest_digest"
        expected_blocked = semantic_digest({"blocked_reason": execution["blocked_reason"], "reviewed_cache_verification": execution["reviewed_cache_verification"]})
        if execution.get(blocked_key) != expected_blocked:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("blocked manifest digest mismatch")
        closed = ["complete_29_row_detail_materialized", "complete_29_row_detail_exposed", "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created"]
        if any(execution.get(field) is not False for field in closed):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("blocked materialization flag open")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("checklist invalid")
    summary = _summary(execution, checklist, success)
    if execution.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("summary mismatch")
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest"
    digest = execution.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("execution digest missing")
    if digest != marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest_v1(execution):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError("execution digest mismatch")
    return {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"], "execution_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_markdown_v1(
    execution: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(execution)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    verification = execution["reviewed_cache_verification"]
    sections = [
        ("Source Approval", [SOURCE_APPROVAL_DIGEST, approval_source.APPROVAL_STATUS]),
        ("Source Operator Review and Candidate", [execution["source_complete_29_row_materialization_operator_review_digest"], execution["source_complete_29_row_materialization_candidate_digest"]]),
        ("Source Detail Exposure or Binding Failure Diagnosis", [execution["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"], execution["primary_failure_class"]]),
        ("Source Recovery Results Review", [execution["source_module_grouping_source_recovery_results_review_digest"], execution["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; the root regression is not retry evidence."]),
        ("Execution Scope", [EXECUTION_SCOPE]),
        ("Reviewed Cache Verification", [
            f"lastfailed hash verified: {verification.get('lastfailed_hash_verified')}",
            f"nodeids hash verified: {verification.get('nodeids_hash_verified')}",
            f"entry counts verified: {verification.get('entry_counts_verified')}",
            f"lastfailed subset of nodeids: {verification.get('lastfailed_subset_of_nodeids')}",
        ]),
        ("Complete 29-row Materialized Source", [f"Rows: {len(execution['complete_29_row_module_grouping_detail_source'])}.", f"Disposition: {'materialized' if success else 'blocked'}."]),
        ("Top Module Concentration Preservation", [f"Top-five sum: {execution.get('top_5_count_sum')}.", f"Top-ten sum: {execution.get('top_10_count_sum')}."]),
        ("Priority Tier Enablement", [f"Tier sums: {execution.get('priority_tier_1_count_sum')}/{execution.get('priority_tier_2_count_sum')}/{execution.get('priority_tier_3_count_sum')}."]),
        ("Unsupported Claims Boundary", list(UNSUPPORTED_ROW_CLAIMS)),
        ("Success or Blocked Disposition", [execution["execution_status"], execution.get("blocked_reason") or SUCCESS_NEXT_TASK]),
        ("Authority Boundaries", ["Cache remained read-only; no pytest, recovery rerun, retry, diagnostics, remediation, classification, downstream binding/reentry, main action, runtime, or trading action occurred."]),
        ("Next Chain", execution["next_chain"]), ("Next Gates", execution["next_gates"]),
        ("Risk Controls", execution["risk_controls"]),
        ("Checklist Summary", [f"`{validation['passed_checks']}/{validation['total_checks']}` checks pass."]),
        ("Guardrails", ["A separate materialization results review is required before detail-binding reattempt."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Execution v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_COMPLETE_29_ROW_SOURCE_CREATED",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_BLOCKED_SOURCE_UNAVAILABLE_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_ONLY_COMPLETE_DETAIL_SOURCE_CREATION_NOT_RETRY_NOT_MAIN",
    "SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE",
    "COMMITTED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE",
    "committed_complete_29_row_module_grouping_detail_source_v1",
    "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_markdown_v1",
    "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest_v1",
]
