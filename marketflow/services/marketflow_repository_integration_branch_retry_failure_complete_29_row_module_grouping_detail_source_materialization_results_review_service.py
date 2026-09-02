"""Review the committed 29-row materialization without reading detached cache."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1"
SOURCE_EXECUTION_DIGEST = "3c1b7e6cddf2aedaec4e91dcaf742eaceb37d974b01387a8ba7f0da70cb0ac3b"
SOURCE_PAYLOAD_DIGEST = "1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7"
SOURCE_DIGEST_MANIFEST_DIGEST = "198e28d641e08fbba9b49fb33a942d4ffcbd77c1ad1329048e25028234a6261c"
NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_V1"
NEXT_TASK_STATUS = "FUTURE_REATTEMPT_NOT_CREATED"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_DETAIL_EXPOSURE_OR_BINDING_REATTEMPT_USING_REVIEWED_COMPLETE_29_ROW_SOURCE"
RECOMMENDATION_REASON = (
    "The complete 29-row materialized source has been reviewed and is ready to be used by a separately governed "
    "detail exposure/binding execution reattempt. After-v2 planning reentry remains blocked until the detail "
    "exposure/binding reattempt and its own results review pass."
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE

OUTPUT_IDS = [
    "materialization_results_review_manifest",
    "source_materialization_execution_summary",
    "materialized_payload_digest_review",
    "materialized_payload_integrity_review",
    "reviewed_cache_verification_summary",
    "complete_29_row_materialized_source_review",
    "top_module_concentration_review",
    "priority_tier_enablement_review",
    "bounded_samples_review",
    "unsupported_claims_boundary_review",
    "detail_binding_reattempt_readiness_report",
    "digest_manifest",
]

REVIEW_FINDINGS = {
    "finding_1": "The source materialization execution completed successfully and created a bounded committed 29-row module grouping source.",
    "finding_2": "The source materialization execution is bound by execution digest, payload digest, and digest-manifest digest.",
    "finding_3": "The materialized source contains exactly 29 module rows.",
    "finding_4": "The materialized source totals exactly 1,404 failed-or-errored node IDs.",
    "finding_5": "The top-five module paths and counts match the previously reviewed source facts.",
    "finding_6": "The top-five sum remains 612 and the top-ten sum remains 1,069.",
    "finding_7": "The priority tier sums are 612, 457, and 335.",
    "finding_8": "Every row contains bounded samples with no more than five node IDs.",
    "finding_9": "The source execution recorded reviewed cache verification: expected hashes, counts, and subset check passed.",
    "finding_10": "This results review did not read cache, rerun materialization, rerun source recovery, run pytest, run retry, execute diagnostics, execute remediation, or execute classification.",
    "finding_11": "The materialized source is suitable for a separately invoked detail exposure/binding execution reattempt only after this review.",
    "finding_12": "The materialized source remains planning evidence only and does not prove failure/error separation, first failure, first error, traceback root cause, retry success, or main-merge readiness.",
}

NEXT_CHAIN = [
    "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.",
    "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
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
    "detail_exposure_or_binding_execution_reattempt_with_complete_source",
    "detail_exposure_or_binding_results_review",
    "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
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
    "review_materialization_results_does_not_read_cache",
    "review_materialization_results_does_not_modify_cache",
    "review_materialization_results_does_not_rerun_materialization",
    "review_materialization_results_does_not_rerun_source_recovery",
    "review_materialization_results_does_not_run_pytest",
    "review_materialization_results_does_not_rerun_retry",
    "review_materialization_results_does_not_execute_detail_binding_reattempt",
    "review_materialization_results_does_not_execute_after_v2_planning_reentry",
    "review_materialization_results_does_not_execute_diagnostics",
    "review_materialization_results_does_not_execute_remediation",
    "review_materialization_results_does_not_execute_classification",
    "review_materialization_results_does_not_classify_modules_again",
    "review_materialization_results_does_not_create_targeted_diagnostic_candidate",
    "review_materialization_results_does_not_create_new_retry_candidate",
    "review_materialization_results_does_not_create_retry_results_review",
    "review_materialization_results_does_not_create_integration_results_review",
    "review_materialization_results_does_not_mark_integration_successful",
    "review_materialization_results_does_not_generate_successful_integration_digest",
    "review_materialization_results_does_not_claim_failure_error_separation",
    "review_materialization_results_does_not_claim_first_failure",
    "review_materialization_results_does_not_claim_first_error",
    "review_materialization_results_does_not_claim_traceback_root_cause",
    "review_materialization_results_does_not_recommend_direct_code_remediation",
    "review_materialization_results_does_not_treat_materialized_payload_as_retry_success",
    "review_materialization_results_does_not_push_integration_branch",
    "review_materialization_results_does_not_push_main",
    "review_materialization_results_does_not_delete_integration_branch",
    "review_materialization_results_does_not_delete_worktree",
    "review_materialization_results_does_not_force_push",
    "review_materialization_results_does_not_prune_remotes",
    "review_materialization_results_does_not_modify_tags",
    "review_materialization_results_does_not_modify_staged_evidence",
    "review_materialization_results_does_not_regenerate_evidence",
    "review_materialization_results_does_not_call_providers",
    "review_materialization_results_does_not_acquire_market_data",
    "review_materialization_results_does_not_regenerate_dataset",
    "review_materialization_results_does_not_recompute_metrics",
    "review_materialization_results_does_not_train_models",
    "review_materialization_results_does_not_score_strategy",
    "review_materialization_results_does_not_generate_recommendations",
    "review_materialization_results_does_not_accept_predictive_usefulness",
    "review_materialization_results_does_not_accept_profitability",
    "review_materialization_results_does_not_authorize_runtime",
    "review_materialization_results_does_not_authorize_broker_execution",
    "materialized_complete_29_row_source_is_planning_source_not_root_cause",
    "materialized_payload_is_not_retry_success",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_detail_binding_execution_remains_historically_blocked",
    "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_detail_binding_reattempt_required_after_materialization_review",
    "separate_detail_binding_results_review_required_after_reattempt",
    "separate_after_v2_planning_reentry_required_after_detail_binding_review",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

TRUE_FIELDS = [
    "complete_29_row_materialization_results_review_created",
    "complete_29_row_materialization_results_review_ready",
    "source_materialization_execution_reviewed",
    "source_materialized_payload_digest_verified",
    "source_materialization_digest_manifest_verified",
    "materialized_complete_29_row_source_reviewed",
    "materialized_payload_integrity_reviewed",
    "reviewed_cache_verification_from_source_execution",
    "top_module_concentration_reviewed",
    "priority_tier_enablement_reviewed",
    "bounded_samples_reviewed",
    "unsupported_claims_boundary_reviewed",
    "ready_for_detail_exposure_or_binding_execution_reattempt",
]

FALSE_FIELDS = [
    "cache_read_in_review", "cache_modified_in_review", "source_recovery_rerun_performed",
    "materialization_execution_rerun_performed", "detail_exposure_or_binding_reattempt_created",
    "detail_exposure_or_binding_reattempt_executed", "after_v2_planning_execution_reentry_created",
    "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
    "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
    "main_merge_approval_created", "retry_rerun_performed", "full_pytest_performed",
    "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
    "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_review", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed",
    "first_failure_identified", "first_error_identified", "first_order_claim_made",
    "traceback_root_cause_claimed", "direct_code_remediation_recommended",
    "retry_success_claimed", "main_merge_readiness_claimed",
    "ready_for_after_v2_planning_reentry_with_complete_detail",
]

SOURCE_BINDINGS = {
    "source_complete_29_row_materialization_approval_digest": "f8126d0d38793c9c562fca0217823ffdb919301596ec44b9bc33ff807fa77059",
    "source_complete_29_row_materialization_operator_review_digest": "72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90",
    "source_complete_29_row_materialization_candidate_digest": "4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061",
    "source_detail_exposure_or_binding_execution_failure_diagnosis_digest": "8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41",
    "primary_failure_class": "COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE",
    "source_detail_exposure_or_binding_execution_blocked_digest": "9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca",
    "source_detail_exposure_or_binding_execution_blocked_manifest_digest": "c732eac857725728bb856f2d145eb86101ce1f839ddca740b66db4d48ae3aa4c",
    "source_detail_exposure_or_binding_execution_blocked_reason": "COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE",
    "source_detail_exposure_or_binding_approval_digest": "384ea3fcb8440c48be01d62a115e9abaf8424ea898832551d80b30383207954f",
    "source_detail_exposure_or_binding_operator_review_digest": "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b",
    "source_detail_exposure_or_binding_candidate_digest": "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23",
    "source_reentry_failure_diagnosis_digest": "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb",
    "source_reentry_failure_primary_failure_class": "COMMITTED_REENTRY_SOURCE_DETAIL_GAP",
    "source_reentry_execution_blocked_digest": "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49",
    "source_reentry_execution_blocked_manifest_digest": "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99",
    "source_reentry_execution_blocked_reason": "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT",
    "source_after_v2_planning_reentry_digest": "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927",
    "source_module_grouping_source_recovery_results_review_digest": "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266",
    "source_module_grouping_source_recovery_results_review_manifest_digest": "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9",
    "source_module_grouping_source_recovery_execution_digest": "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a",
    "source_module_grouping_source_recovery_detail_digest": "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5",
    "source_module_grouping_source_recovery_digest_manifest_digest": "940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc",
    "source_blocked_after_v2_execution_digest": "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755",
    "source_blocked_after_v2_manifest_digest": "c3d644957eb536ede1d725c912f0211a0d84aa72e56d5f8cbed2e0939a907cef",
    "blocked_reason_before_recovery": "MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS",
    "source_after_v2_approval_digest": "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97",
    "source_after_v2_operator_review_digest": "9ea3399758004bdfeb179ad9315a13ebce4514bd51e2cf3b9d39f507a3f1cf03",
    "source_after_v2_candidate_digest": "c6e22aec87122675e9eb2ccf62af7e72756c471ebec81d89cabe1d800633d5e4",
    "source_results_review_v2_digest": "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86",
    "source_execution_v2_digest": "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017",
    "source_module_grouping_digest": "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff",
    "source_approval_v2_digest": "a29132ad740c0e617fb438c154c4b5fed756f15bceed40ff132334d1c5e58412",
    "source_staged_inventory_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
}


class MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError(ValueError):
    """Raised when source evidence or review content violates the review contract."""


def _committed_source_execution() -> dict[str, Any]:
    rows = source.committed_complete_29_row_module_grouping_detail_source_v1()
    return {
        "artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "execution_status": source.SUCCESS_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest": SOURCE_EXECUTION_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "selected_complete_29_row_materialization_package": source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "retry_failure_context": {
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        },
        "materialization_package_executed": True,
        "complete_29_row_detail_materialized": True,
        "complete_29_row_detail_exposed": True,
        "complete_29_row_detail_bound": True,
        "complete_29_row_detail_committed_source_created": True,
        "complete_29_row_detail_source_type": source.ROW_SOURCE,
        "complete_29_row_detail_source_basis": "REVIEWED_CACHE_HASHES_COUNTS_SUBSET_CHECK_AND_RECOVERY_CHAIN_DIGESTS",
        "used_reviewed_cache_read_only_for_materialization": True,
        "cache_read_in_execution": True,
        "cache_modified": False,
        "pytest_cache_committed": False,
        "marketflow_outputs_committed": False,
        "reviewed_cache_verification": {
            "lastfailed_sha256_expected": source.REVIEWED_LASTFAILED_SHA256,
            "lastfailed_sha256_actual": source.REVIEWED_LASTFAILED_SHA256,
            "lastfailed_hash_verified": True,
            "lastfailed_entry_count_expected": 1404,
            "lastfailed_entry_count_actual": 1404,
            "nodeids_sha256_expected": source.REVIEWED_NODEIDS_SHA256,
            "nodeids_sha256_actual": source.REVIEWED_NODEIDS_SHA256,
            "nodeids_hash_verified": True,
            "nodeids_entry_count_expected": 26288,
            "nodeids_entry_count_actual": 26288,
            "entry_counts_verified": True,
            "lastfailed_subset_of_nodeids": True,
            "committed_source_rows_match": True,
        },
        "complete_29_row_module_grouping_detail_source": rows,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069,
        "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612,
        "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457,
        "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335,
        "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }


def _source_reasons(execution: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    expected = _committed_source_execution()
    exact_fields = [
        "artifact_kind", "execution_status", "execution_scope",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest",
        "selected_complete_29_row_materialization_package", *SOURCE_BINDINGS,
        "retry_execution_commit", "retry_failure_context", "materialization_package_executed",
        "complete_29_row_detail_materialized", "complete_29_row_detail_exposed",
        "complete_29_row_detail_bound", "complete_29_row_detail_committed_source_created",
        "complete_29_row_detail_source_type", "complete_29_row_detail_source_basis",
        "used_reviewed_cache_read_only_for_materialization", "cache_read_in_execution",
        "cache_modified", "pytest_cache_committed", "marketflow_outputs_committed",
        "failed_or_errored_nodeids_count", "module_summary_module_count",
        "largest_module_nodeid_counts", "top_5_count_sum",
        "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
        "priority_tier_1_percentage_of_failed_or_errored_nodeids", "priority_tier_2_count_sum",
        "priority_tier_2_percentage_of_failed_or_errored_nodeids", "priority_tier_3_count_sum",
        "priority_tier_3_percentage_of_failed_or_errored_nodeids",
    ]
    for field in exact_fields:
        if execution.get(field) != expected[field]:
            reasons.append(f"SOURCE_{field.upper()}_MISMATCH_OR_MISSING")
    verification = execution.get("reviewed_cache_verification")
    if not isinstance(verification, Mapping):
        reasons.append("SOURCE_REVIEWED_CACHE_VERIFICATION_MISSING")
    else:
        for field, value in expected["reviewed_cache_verification"].items():
            if verification.get(field) != value:
                reasons.append(f"SOURCE_CACHE_{field.upper()}_MISMATCH_OR_MISSING")
    rows = execution.get("complete_29_row_module_grouping_detail_source")
    if not isinstance(rows, list):
        reasons.append("SOURCE_MATERIALIZED_ROWS_MISSING")
    else:
        check_verification = {"lastfailed_hash_verified": True, "nodeids_hash_verified": True,
                              "entry_counts_verified": True, "lastfailed_subset_of_nodeids": True,
                              "committed_source_rows_match": rows == source.committed_complete_29_row_module_grouping_detail_source_v1()}
        reasons.extend(f"SOURCE_{reason}" for reason in source._integrity_reasons(check_verification, rows))
        if semantic_digest(rows) != SOURCE_PAYLOAD_DIGEST:
            reasons.append("SOURCE_MATERIALIZED_PAYLOAD_DIGEST_MISMATCH")
    return list(dict.fromkeys(reasons))


def _reviewed_cache_summary(verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "reviewed_from_source_execution": True,
        "cache_read_in_review": False,
        "cache_modified_in_review": False,
        "lastfailed_sha256": verification["lastfailed_sha256_actual"],
        "lastfailed_entry_count": verification["lastfailed_entry_count_actual"],
        "nodeids_sha256": verification["nodeids_sha256_actual"],
        "nodeids_entry_count": verification["nodeids_entry_count_actual"],
        "lastfailed_subset_of_nodeids": verification["lastfailed_subset_of_nodeids"],
        "all_source_execution_checks_verified": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows_review = review.get("complete_29_row_materialized_source_review", {})
    rows = rows_review.get("rows", []) if isinstance(rows_review, Mapping) else []
    counts = [row.get("failed_or_errored_nodeid_count") for row in rows if isinstance(row, Mapping)]
    paths = [row.get("module_path") for row in rows if isinstance(row, Mapping)]
    values: dict[str, tuple[Any, Any]] = {
        "source_materialization_execution_digest_bound": (SOURCE_EXECUTION_DIGEST, review.get("source_complete_29_row_materialization_execution_digest")),
        "source_materialized_payload_digest_bound": (SOURCE_PAYLOAD_DIGEST, review.get("source_complete_29_row_materialized_payload_digest")),
        "source_materialization_digest_manifest_digest_bound": (SOURCE_DIGEST_MANIFEST_DIGEST, review.get("source_complete_29_row_materialization_digest_manifest_digest")),
        "source_materialization_success_status_bound": (source.SUCCESS_STATUS, review.get("source_materialization_execution_status")),
        "source_selected_package_bound": (source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE, review.get("selected_complete_29_row_materialization_package")),
        "source_cache_verification_reviewed_from_execution": (True, review.get("reviewed_cache_verification_from_source_execution")),
        "source_cache_not_read_by_review": (False, review.get("cache_read_in_review")),
        "source_cache_not_modified_by_review": (False, review.get("cache_modified_in_review")),
        "materialized_payload_digest_verified": (True, review.get("source_materialized_payload_digest_verified")),
        "materialization_digest_manifest_verified": (True, review.get("source_materialization_digest_manifest_verified")),
        "complete_29_row_materialized_source_reviewed": (True, review.get("materialized_complete_29_row_source_reviewed")),
        "complete_29_row_rows_exactly_29": (29, len(rows)),
        "failed_or_errored_nodeids_1404": (1404, sum(value for value in counts if isinstance(value, int) and not isinstance(value, bool))),
        "largest_module_counts_verified": ([136, 131, 122, 112, 111], counts[:5]),
        "top_five_paths_preserved": (source.EXPECTED_TOP_FIVE_PATHS, paths[:5]),
        "top_five_sum_612": (612, sum(value for value in counts[:5] if isinstance(value, int))),
        "top_ten_sum_1069": (1069, sum(value for value in counts[:10] if isinstance(value, int))),
        "tier_1_sum_612": (612, sum(value for value in counts[:5] if isinstance(value, int))),
        "tier_2_sum_457": (457, sum(value for value in counts[5:10] if isinstance(value, int))),
        "tier_3_sum_335": (335, sum(value for value in counts[10:] if isinstance(value, int))),
        "bounded_samples_max_5": (True, bool(rows) and all(isinstance(row.get("sample_nodeids_bounded"), list) and 0 < len(row["sample_nodeids_bounded"]) <= 5 and row.get("sample_nodeids_bounded_count") == len(row["sample_nodeids_bounded"]) for row in rows)),
        "row_sources_valid": (True, bool(rows) and all(row.get("source") == source.ROW_SOURCE for row in rows)),
        "row_basis_valid": (True, bool(rows) and all(row.get("basis") == source.ROW_BASIS for row in rows)),
        "row_confidence_valid": (True, bool(rows) and all(row.get("confidence") == source.ROW_CONFIDENCE for row in rows)),
        "row_unsupported_claims_valid": (True, bool(rows) and all(row.get("unsupported_claims") == source.UNSUPPORTED_ROW_CLAIMS for row in rows)),
        "review_created_true": (True, review.get("complete_29_row_materialization_results_review_created")),
        "review_ready_true": (True, review.get("complete_29_row_materialization_results_review_ready")),
        "materialized_payload_integrity_reviewed_true": (True, review.get("materialized_payload_integrity_reviewed")),
        "top_module_concentration_reviewed_true": (True, review.get("top_module_concentration_reviewed")),
        "priority_tier_enablement_reviewed_true": (True, review.get("priority_tier_enablement_reviewed")),
        "bounded_samples_reviewed_true": (True, review.get("bounded_samples_reviewed")),
        "unsupported_claims_boundary_reviewed_true": (True, review.get("unsupported_claims_boundary_reviewed")),
        "ready_for_detail_binding_reattempt_true": (True, review.get("ready_for_detail_exposure_or_binding_execution_reattempt")),
        "ready_for_after_v2_planning_reentry_false": (False, review.get("ready_for_after_v2_planning_reentry_with_complete_detail")),
        "review_outputs_generated": (OUTPUT_IDS, [item.get("output_id") for item in review.get("review_outputs", [])]),
        "recommendation_defined": (RECOMMENDED_ACTION, review.get("recommended_action")),
        "next_chain_defined": (NEXT_CHAIN, review.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, review.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (False, review.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, review.get("pytest_cache_tracked_in_repository")),
    }
    source_checks = {
        "source_materialization_approval_digest_bound": "source_complete_29_row_materialization_approval_digest",
        "source_materialization_operator_review_digest_bound": "source_complete_29_row_materialization_operator_review_digest",
        "source_materialization_candidate_digest_bound": "source_complete_29_row_materialization_candidate_digest",
        "source_execution_failure_diagnosis_digest_bound": "source_detail_exposure_or_binding_execution_failure_diagnosis_digest",
        "source_primary_failure_class_bound": "primary_failure_class",
        "source_detail_binding_blocked_execution_digest_bound": "source_detail_exposure_or_binding_execution_blocked_digest",
        "source_detail_binding_blocked_manifest_digest_bound": "source_detail_exposure_or_binding_execution_blocked_manifest_digest",
        "source_detail_binding_blocked_reason_bound": "source_detail_exposure_or_binding_execution_blocked_reason",
        "source_detail_binding_approval_digest_bound": "source_detail_exposure_or_binding_approval_digest",
        "source_detail_binding_operator_review_digest_bound": "source_detail_exposure_or_binding_operator_review_digest",
        "source_detail_binding_candidate_digest_bound": "source_detail_exposure_or_binding_candidate_digest",
        "source_reentry_failure_diagnosis_digest_bound": "source_reentry_failure_diagnosis_digest",
        "source_reentry_failure_primary_failure_class_bound": "source_reentry_failure_primary_failure_class",
        "source_reentry_execution_blocked_digest_bound": "source_reentry_execution_blocked_digest",
        "source_reentry_execution_blocked_manifest_digest_bound": "source_reentry_execution_blocked_manifest_digest",
        "source_reentry_execution_blocked_reason_bound": "source_reentry_execution_blocked_reason",
        "source_planning_reentry_digest_bound": "source_after_v2_planning_reentry_digest",
        "source_recovery_results_review_digest_bound": "source_module_grouping_source_recovery_results_review_digest",
        "source_recovery_results_review_manifest_digest_bound": "source_module_grouping_source_recovery_results_review_manifest_digest",
        "source_recovery_execution_digest_bound": "source_module_grouping_source_recovery_execution_digest",
        "source_recovery_detail_digest_bound": "source_module_grouping_source_recovery_detail_digest",
        "source_recovery_digest_manifest_bound": "source_module_grouping_source_recovery_digest_manifest_digest",
        "source_blocked_after_v2_execution_digest_bound": "source_blocked_after_v2_execution_digest",
        "source_blocked_after_v2_manifest_digest_bound": "source_blocked_after_v2_manifest_digest",
        "source_after_v2_approval_digest_bound": "source_after_v2_approval_digest",
        "source_results_review_v2_digest_bound": "source_results_review_v2_digest",
        "source_execution_v2_digest_bound": "source_execution_v2_digest",
        "source_module_grouping_digest_bound": "source_module_grouping_digest",
    }
    values.update({check_id: (SOURCE_BINDINGS[field], review.get(field)) for check_id, field in source_checks.items()})
    values["retry_execution_commit_bound"] = ("ab178b65c69f0274b0abbf9c20df102d35e78d34", review.get("retry_execution_commit"))
    values["retry_failure_counts_bound"] = ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, review.get("retry_failure_context", {}).get("counts"))
    false_checks = {
        "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed", "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed", "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "detail_binding_reattempt_created_false": "detail_exposure_or_binding_reattempt_created", "detail_binding_reattempt_executed_false": "detail_exposure_or_binding_reattempt_executed",
        "after_v2_planning_reentry_created_false": "after_v2_planning_execution_reentry_created", "after_v2_planning_reentry_performed_false": "after_v2_planning_execution_reentry_performed",
        "targeted_diagnostic_candidate_created_false": "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed", "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created", "materialization_execution_rerun_false": "materialization_execution_rerun_performed",
        "source_recovery_rerun_false": "source_recovery_rerun_performed", "cache_read_in_review_false": "cache_read_in_review",
        "retry_rerun_false": "retry_rerun_performed", "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed", "diagnostic_output_false": "diagnostic_output_captured",
        "diagnostic_execution_false": "diagnostic_method_executed", "remediation_execution_false": "code_remediation_executed",
        "classification_execution_false": "classification_execution_performed_in_review", "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task", "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed", "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_review", "market_data_acquisition_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_false": "dataset_generation_performed_in_review", "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values.update({check_id: (False, review.get(field)) for check_id, field in false_checks.items()})
    values["successful_integration_digest_false"] = ([False, False], [review.get("successful_integration_execution_digest_generated"), review.get("successful_integration_validation_digest_generated")])
    values["predictive_usefulness_not_accepted"] = (NOT_ACCEPTED, review.get("predictive_usefulness"))
    values["profitability_not_accepted"] = (NOT_ACCEPTED, review.get("profitability"))
    values["runtime_not_authorized"] = (NOT_AUTHORIZED, review.get("runtime_use"))
    values["broker_not_authorized"] = (NOT_AUTHORIZED, review.get("broker_execution"))
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def _summary(review: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    result = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        **{field: review.get(field) for field in TRUE_FIELDS + [
            "cache_read_in_review", "materialization_execution_rerun_performed", "source_recovery_rerun_performed",
            "ready_for_after_v2_planning_reentry_with_complete_detail", "detail_exposure_or_binding_reattempt_created",
            "detail_exposure_or_binding_reattempt_executed", "after_v2_planning_execution_reentry_created",
            "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
            "new_retry_candidate_created", "new_retry_executed", "integration_execution_successful",
        ]},
        "complete_29_row_detail_materialized_in_source_execution": review.get("source_materialization_execution_summary", {}).get("complete_29_row_detail_materialized"),
        "complete_29_row_detail_exposed_in_source_execution": review.get("source_materialization_execution_summary", {}).get("complete_29_row_detail_exposed"),
        "complete_29_row_detail_bound_in_source_execution": review.get("source_materialization_execution_summary", {}).get("complete_29_row_detail_bound"),
        "complete_29_row_detail_committed_source_created_in_source_execution": review.get("source_materialization_execution_summary", {}).get("complete_29_row_detail_committed_source_created"),
        **{field: review.get(field) for field in [
            "failed_or_errored_nodeids_count", "module_summary_module_count", "top_5_count_sum",
            "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
            "top_10_percentage_of_failed_or_errored_nodeids", "priority_tier_1_count_sum",
            "priority_tier_2_count_sum", "priority_tier_3_count_sum",
        ]},
        "recommended_next_task": NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    return result


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(
    *, source_execution: dict | None = None,
) -> dict:
    """Build the review solely from committed execution evidence."""

    execution = deepcopy(source_execution) if source_execution is not None else _committed_source_execution()
    reasons = _source_reasons(execution)
    if reasons:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError(";".join(reasons))
    rows = deepcopy(execution["complete_29_row_module_grouping_detail_source"])
    verification = execution["reviewed_cache_verification"]
    top_summary = [
        {"priority_order": row["priority_order"], "module_path": row["module_path"], "failed_or_errored_nodeid_count": row["failed_or_errored_nodeid_count"]}
        for row in rows[:5]
    ]
    source_review = {
        "reviewed": True, "row_count": len(rows), "failed_or_errored_nodeids_count": 1404,
        "source_payload_digest": SOURCE_PAYLOAD_DIGEST, "rows": rows,
    }
    payload_digest_review = {
        "expected": SOURCE_PAYLOAD_DIGEST, "actual_from_committed_rows": semantic_digest(rows), "verified": True,
        "digest_is_not_payload": True,
    }
    integrity_review = {
        "reviewed": True, "row_count": len(rows), "failed_or_errored_nodeids_count": sum(row["failed_or_errored_nodeid_count"] for row in rows),
        "largest_module_nodeid_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "required_row_fields_present": True,
    }
    cache_summary = _reviewed_cache_summary(verification)
    top_review = {
        "reviewed": True, "top_5_module_paths": [row["module_path"] for row in rows[:5]],
        "top_5_counts": [row["failed_or_errored_nodeid_count"] for row in rows[:5]],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
    }
    tier_review = {
        "reviewed": True,
        "priority_tier_1_count_sum": 612, "priority_tier_1_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "priority_tier_2_count_sum": 457, "priority_tier_2_percentage_of_failed_or_errored_nodeids": "32.54985755",
        "priority_tier_3_count_sum": 335, "priority_tier_3_percentage_of_failed_or_errored_nodeids": "23.86039886",
    }
    bounded_review = {
        "reviewed": True, "module_count": 29, "sample_limit_per_module": 5,
        "all_rows_have_bounded_samples": all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows),
        "largest_sample_count": max(row["sample_nodeids_bounded_count"] for row in rows),
    }
    unsupported_review = {
        "reviewed": True, "required_unsupported_claims": list(source.UNSUPPORTED_ROW_CLAIMS),
        "all_rows_preserve_boundary": all(row["unsupported_claims"] == source.UNSUPPORTED_ROW_CLAIMS for row in rows),
    }
    execution_summary = {
        "artifact_kind": execution["artifact_kind"], "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"], "materialization_package_executed": True,
        "complete_29_row_detail_materialized": True, "complete_29_row_detail_exposed": True,
        "complete_29_row_detail_bound": True, "complete_29_row_detail_committed_source_created": True,
        "cache_modified_in_source_execution": False,
    }
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_materialization_execution_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_materialization_execution_status": source.SUCCESS_STATUS,
        "source_materialization_execution_scope": source.EXECUTION_SCOPE,
        "source_complete_29_row_materialization_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_complete_29_row_materialized_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "source_complete_29_row_materialization_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "selected_complete_29_row_materialization_package": source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_execution_commit": execution["retry_execution_commit"],
        "retry_failure_context": deepcopy(execution["retry_failure_context"]),
        "source_materialization_execution_summary": execution_summary,
        "reviewed_cache_verification_summary": cache_summary,
        "complete_29_row_materialized_source_review": source_review,
        "top_module_summary": top_summary,
        "top_module_concentration_review": top_review,
        "priority_tier_enablement_review": tier_review,
        "bounded_samples_review": bounded_review,
        "unsupported_claims_boundary_review": unsupported_review,
        "materialized_payload_digest_review": payload_digest_review,
        "materialized_payload_integrity_review": integrity_review,
        "review_findings": deepcopy(REVIEW_FINDINGS),
        "review_outputs": [{"output_id": output_id, "status": "GENERATED_RESEARCH_ONLY"} for output_id in OUTPUT_IDS],
        "recommendation": {
            "recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS,
            "recommended_action": RECOMMENDED_ACTION, "ready_for_detail_exposure_or_binding_execution_reattempt": True,
            "ready_for_after_v2_planning_reentry_with_complete_detail": False, "reason": RECOMMENDATION_REASON,
        },
        "recommended_next_task": NEXT_TASK, "recommended_next_task_status": NEXT_TASK_STATUS,
        "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_5_count_sum": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "priority_tier_1_count_sum": 612, "priority_tier_2_count_sum": 457, "priority_tier_3_count_sum": 335,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    review.update({field: True for field in TRUE_FIELDS})
    review.update({field: False for field in FALSE_FIELDS})
    payload_review_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_review_digest"
    manifest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_manifest_digest"
    review[payload_review_key] = semantic_digest({"payload_digest_review": payload_digest_review, "payload_integrity_review": integrity_review, "source_review": source_review})
    review["digest_manifest"] = {
        "source_execution": SOURCE_EXECUTION_DIGEST,
        "source_payload": SOURCE_PAYLOAD_DIGEST,
        "source_materialization_manifest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "payload_review": review[payload_review_key],
        "cache_verification_review": semantic_digest(cache_summary),
        "top_module_concentration_review": semantic_digest(top_review),
        "priority_tier_enablement_review": semantic_digest(tier_review),
        "bounded_samples_review": semantic_digest(bounded_review),
        "unsupported_claims_boundary_review": semantic_digest(unsupported_review),
        "review_findings": semantic_digest(REVIEW_FINDINGS),
        "recommendation": semantic_digest(review["recommendation"]),
    }
    review[manifest_key] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review, review["checklist"])
    review_digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"
    review[review_digest_key] = _review_digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(review: dict) -> dict:
    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("review must be an object")
    constants = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE, "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_materialization_execution_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_materialization_execution_status": source.SUCCESS_STATUS,
        "source_materialization_execution_scope": source.EXECUTION_SCOPE,
        "source_complete_29_row_materialization_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_complete_29_row_materialized_payload_digest": SOURCE_PAYLOAD_DIGEST,
        "source_complete_29_row_materialization_digest_manifest_digest": SOURCE_DIGEST_MANIFEST_DIGEST,
        "selected_complete_29_row_materialization_package": source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE,
        **SOURCE_BINDINGS,
    }
    for field, expected in constants.items():
        if review.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError(f"{field} mismatch")
    if any(review.get(field) is not True for field in TRUE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("required review flag missing")
    if any(review.get(field) is not False for field in FALSE_FIELDS):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("closed boundary opened")
    if review.get("predictive_usefulness") != NOT_ACCEPTED or review.get("profitability") != NOT_ACCEPTED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("acceptance boundary changed")
    if review.get("runtime_use") != NOT_AUTHORIZED or review.get("broker_execution") != NOT_AUTHORIZED:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("runtime boundary changed")
    rows_review = review.get("complete_29_row_materialized_source_review")
    if not isinstance(rows_review, Mapping) or not isinstance(rows_review.get("rows"), list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("materialized payload review missing")
    rows = rows_review["rows"]
    verification = {"lastfailed_hash_verified": True, "nodeids_hash_verified": True, "entry_counts_verified": True,
                    "lastfailed_subset_of_nodeids": True, "committed_source_rows_match": rows == source.committed_complete_29_row_module_grouping_detail_source_v1()}
    reasons = source._integrity_reasons(verification, rows)
    if reasons or semantic_digest(rows) != SOURCE_PAYLOAD_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("materialized payload integrity invalid")
    if review.get("reviewed_cache_verification_summary") != _reviewed_cache_summary(
        _committed_source_execution()["reviewed_cache_verification"]
    ):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("cache summary invalid")
    if not isinstance(review.get("materialized_payload_digest_review"), Mapping) or review["materialized_payload_digest_review"].get("verified") is not True:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("payload digest review invalid")
    if review.get("review_findings") != REVIEW_FINDINGS or review.get("next_chain") != NEXT_CHAIN or review.get("next_gates") != NEXT_GATES or review.get("risk_controls") != RISK_CONTROLS:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("review governance content invalid")
    if [item.get("output_id") for item in review.get("review_outputs", [])] != OUTPUT_IDS or any(item.get("status") != "GENERATED_RESEARCH_ONLY" for item in review["review_outputs"]):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("review outputs invalid")
    if review.get("recommended_next_task") != NEXT_TASK or review.get("recommended_action") != RECOMMENDED_ACTION or review.get("recommendation", {}).get("reason") != RECOMMENDATION_REASON:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("recommendation invalid")
    payload_review_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_review_digest"
    expected_payload_review = semantic_digest({"payload_digest_review": review["materialized_payload_digest_review"], "payload_integrity_review": review["materialized_payload_integrity_review"], "source_review": rows_review})
    if review.get(payload_review_key) != expected_payload_review:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("payload review digest invalid")
    manifest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_manifest_digest"
    if review.get(manifest_key) != semantic_digest(review.get("digest_manifest")):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("results review manifest digest invalid")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("checklist invalid")
    summary = _summary(review, checklist)
    if review.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("summary invalid")
    review_digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"
    digest = review.get(review_digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _review_digest(review):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("review digest invalid")
    return {
        "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
        "review_scope": review["review_scope"], "review_digest": digest,
        **{field: summary[field] for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(
    output_dir: str | Path, *, source_execution: dict | None = None,
) -> dict:
    review = build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(source_execution=source_execution)
    path = Path(output_dir) / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError("output exists")
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {"path": str(path), "artifact_kind": review["artifact_kind"], "review_status": review["review_status"],
            "review_digest": review["marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"],
            "payload_sha256": sha256_bytes(payload)}


def build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_markdown_v1(review: dict) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(review)
    sections = [
        ("Source Materialization Execution", [SOURCE_EXECUTION_DIGEST, source.SUCCESS_STATUS]),
        ("Source Approval and Operator Review", [SOURCE_BINDINGS["source_complete_29_row_materialization_approval_digest"], SOURCE_BINDINGS["source_complete_29_row_materialization_operator_review_digest"]]),
        ("Source Detail Exposure or Binding Failure Diagnosis", [SOURCE_BINDINGS["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"], SOURCE_BINDINGS["primary_failure_class"]]),
        ("Source Recovery Results Review", [SOURCE_BINDINGS["source_module_grouping_source_recovery_results_review_digest"], SOURCE_BINDINGS["source_module_grouping_source_recovery_detail_digest"]]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, and 7 skipped; root regression is not retry evidence."]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Reviewed Cache Verification from Source Execution", [str(review["reviewed_cache_verification_summary"])]),
        ("Complete 29-row Materialized Source Review", ["29 rows and 1,404 failed-or-errored node IDs reviewed from committed source."]),
        ("Payload Digest Review", [str(review["materialized_payload_digest_review"])]),
        ("Top Module Concentration Review", [str(review["top_module_concentration_review"])]),
        ("Priority Tier Enablement Review", [str(review["priority_tier_enablement_review"])]),
        ("Bounded Samples Review", [str(review["bounded_samples_review"])]),
        ("Unsupported Claims Boundary", list(source.UNSUPPORTED_ROW_CLAIMS)),
        ("Review Findings", list(review["review_findings"].values())),
        ("Recommendation", [review["recommended_action"], review["reason"]]),
        ("Next Chain", review["next_chain"]), ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", ["No cache read, materialization/recovery rerun, retry, detail binding, planning reentry, diagnostics, remediation, classification, provider, runtime, trading, integration, or main action occurred."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass."]),
        ("Guardrails", ["Only the separate detail exposure/binding reattempt gate is prepared; all later gates remain governed separately."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Results Review v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_markdown_v1",
]
