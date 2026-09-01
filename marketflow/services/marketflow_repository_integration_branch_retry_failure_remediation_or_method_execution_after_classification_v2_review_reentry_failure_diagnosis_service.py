"""Diagnose the blocked after-v2 reentry execution from committed evidence only."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1"
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE

SOURCE_BLOCKED_EXECUTION_DIGEST = "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49"
SOURCE_BLOCKED_MANIFEST_DIGEST = "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99"
SOURCE_BLOCKED_REASON = "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"
SOURCE_REENTRY_DIGEST = "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927"
SOURCE_RESULTS_REVIEW_DIGEST = "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9"
SOURCE_RECOVERY_EXECUTION_DIGEST = "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a"
SOURCE_RECOVERY_DETAIL_DIGEST = "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"
SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST = "940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc"
SOURCE_RECOVERY_APPROVAL_DIGEST = "3b2e00be71e6aa209520bba347397bc12134566adfd30ff29e432ba0c7ce4b76"
SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST = "f124b1bf3af19dbe722815d232f7e827af2373ceb449279d5ac80b4533f9b00e"
SOURCE_RECOVERY_CANDIDATE_DIGEST = "4c0542256406f1db4d86f32958d738f6c86dc83ea2dd2132e2d54bcf5afb8bcb"
SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST = "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755"
SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST = "c3d644957eb536ede1d725c912f0211a0d84aa72e56d5f8cbed2e0939a907cef"
SOURCE_AFTER_V2_APPROVAL_DIGEST = "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97"
SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST = "9ea3399758004bdfeb179ad9315a13ebce4514bd51e2cf3b9d39f507a3f1cf03"
SOURCE_AFTER_V2_CANDIDATE_DIGEST = "c6e22aec87122675e9eb2ccf62af7e72756c471ebec81d89cabe1d800633d5e4"
SOURCE_RESULTS_REVIEW_V2_DIGEST = "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86"
SOURCE_EXECUTION_V2_DIGEST = "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017"
SOURCE_MODULE_GROUPING_DIGEST = "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"
SOURCE_APPROVAL_V2_DIGEST = "a29132ad740c0e617fb438c154c4b5fed756f15bceed40ff132334d1c5e58412"
SOURCE_STAGED_INVENTORY_DIGEST = "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
RETRY_EXECUTION_COMMIT = "ab178b65c69f0274b0abbf9c20df102d35e78d34"
PRIMARY_FAILURE_CLASS = "COMMITTED_REENTRY_SOURCE_DETAIL_GAP"
RECOMMENDED_NEXT_PACKAGE = "PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1"
GENERATED_RESEARCH_ONLY = "GENERATED_RESEARCH_ONLY"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

TOP_FIVE = [
    {"module_path": "tests/test_marketflow_signal_or_feature_generation_results_review_service.py", "failed_or_errored_nodeid_count": 136},
    {"module_path": "tests/test_post_identity_freeze_registry_inventory_approval_service.py", "failed_or_errored_nodeid_count": 131},
    {"module_path": "tests/test_corporate_action_authority_plan_candidate_service.py", "failed_or_errored_nodeid_count": 122},
    {"module_path": "tests/test_feature_generation_results_review_redesigned_labels_service.py", "failed_or_errored_nodeid_count": 112},
    {"module_path": "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", "failed_or_errored_nodeid_count": 111},
]

AVAILABLE_COMMITTED_DETAIL = [
    "retry counts", "1404 failed-or-errored node-ID count", "29 module count",
    "largest module counts", "top five module paths", "top five counts",
    "top five concentration", "top ten concentration", "source digests",
    "recovered detail digest",
]
MISSING_COMMITTED_DETAIL = [
    "all 29 module paths", "all per-module counts by module path",
    "all bounded node-ID samples by module", "full recovered module grouping detail rows",
    "committed source snapshot sufficient for deterministic priority-tier planning",
]

NOT_ROOT_CAUSES = [
    "not an origin/main change", "not an integration branch change",
    "not a detached worktree problem", "not a staged evidence mutation",
    "not a cache hash/count failure in the source recovery execution",
    "not a retry rerun problem", "not a full pytest problem",
    "not a provider or market-data issue", "not a runtime or broker issue",
]

NEXT_CHAIN = [
    "Reentry Module Grouping Detail Exposure or Binding Candidate v1.",
    "Candidate Operator Review.", "Approval, if selected.", "Execution, if approved.",
    "Results Review.", "Re-enter after-v2 planning execution using complete recovered detail.",
    "Remediation or Method Results Review After Classification v2 Review Reentry v1, if planning execution succeeds.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if supported.",
    "Diagnostic Capture Operator Review.", "Diagnostic Capture Approval, if selected.",
    "Diagnostic Capture Execution, if approved.", "Diagnostic Capture Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]

NEXT_GATES = [
    "reentry_module_grouping_detail_exposure_or_binding_candidate",
    "reentry_module_grouping_detail_exposure_or_binding_operator_review",
    "reentry_module_grouping_detail_exposure_or_binding_approval_if_selected",
    "reentry_module_grouping_detail_exposure_or_binding_execution_if_approved",
    "reentry_module_grouping_detail_exposure_or_binding_results_review",
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
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "diagnosis_does_not_fix_reentry_execution", "diagnosis_does_not_expose_29_module_rows",
    "diagnosis_does_not_recover_module_grouping_again", "diagnosis_does_not_read_cache",
    "diagnosis_does_not_modify_cache", "diagnosis_does_not_parse_operator_logs",
    "diagnosis_does_not_run_diagnostic_commands", "diagnosis_does_not_execute_diagnostics",
    "diagnosis_does_not_execute_remediation", "diagnosis_does_not_execute_classification",
    "diagnosis_does_not_classify_modules_again", "diagnosis_does_not_rerun_retry",
    "diagnosis_does_not_run_full_pytest", "diagnosis_does_not_create_planning_reentry",
    "diagnosis_does_not_create_new_retry_candidate", "diagnosis_does_not_create_retry_results_review",
    "diagnosis_does_not_create_integration_results_review", "diagnosis_does_not_mark_integration_successful",
    "diagnosis_does_not_generate_successful_integration_digest", "diagnosis_does_not_claim_failure_error_separation",
    "diagnosis_does_not_claim_first_failure", "diagnosis_does_not_claim_first_error",
    "diagnosis_does_not_claim_traceback_root_cause", "diagnosis_does_not_recommend_direct_code_remediation",
    "diagnosis_does_not_treat_recovered_source_as_retry_success", "diagnosis_does_not_push_integration_branch",
    "diagnosis_does_not_push_main", "diagnosis_does_not_delete_integration_branch",
    "diagnosis_does_not_delete_worktree", "diagnosis_does_not_force_push",
    "diagnosis_does_not_prune_remotes", "diagnosis_does_not_modify_tags",
    "diagnosis_does_not_modify_staged_evidence", "diagnosis_does_not_regenerate_evidence",
    "diagnosis_does_not_call_providers", "diagnosis_does_not_acquire_market_data",
    "diagnosis_does_not_regenerate_dataset", "diagnosis_does_not_recompute_metrics",
    "diagnosis_does_not_train_models", "diagnosis_does_not_score_strategy",
    "diagnosis_does_not_generate_recommendations", "diagnosis_does_not_accept_predictive_usefulness",
    "diagnosis_does_not_accept_profitability", "diagnosis_does_not_authorize_runtime",
    "diagnosis_does_not_authorize_broker_execution", "source_detail_gap_is_not_retry_success",
    "source_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked",
    "previous_source_recovery_results_review_remains_valid", "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence", "separate_detail_exposure_candidate_required",
    "separate_approval_required_before_detail_exposure_execution",
    "separate_results_review_required_after_detail_exposure",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence", "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

OUTPUT_IDS = [
    "diagnosis_manifest", "blocked_reentry_execution_summary",
    "source_detail_availability_report", "missing_committed_detail_report",
    "source_chain_detail_carry_forward_report", "root_cause_classification_report",
    "not_root_cause_report", "next_candidate_options_report",
    "recommended_next_package_report", "unsupported_claims_boundary_report", "digest_manifest",
]

FALSE_BOUNDARIES = [
    "module_grouping_detail_exposed_by_diagnosis", "module_paths_recovered_by_diagnosis",
    "per_module_counts_recovered_by_diagnosis", "bounded_nodeid_samples_recovered_by_diagnosis",
    "after_v2_planning_execution_reentered_by_diagnosis",
    "after_v2_planning_execution_performed_by_diagnosis",
    "remediation_or_method_after_v2_reentry_execution_created_by_diagnosis",
    "remediation_or_method_after_v2_reentry_execution_performed_by_diagnosis",
    "diagnostic_method_executed", "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_diagnosis", "source_recovery_rerun_performed",
    "cache_read_in_diagnosis", "module_grouping_recovered_in_diagnosis",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created",
    "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
    "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
    "diagnostic_output_captured", "integration_execution_successful",
    "successful_integration_execution_digest_generated",
    "successful_integration_validation_digest_generated", "integration_branch_pushed",
    "main_push_performed", "origin_main_modified_by_this_task", "marketflow_outputs_committed",
    "pytest_cache_committed", "evidence_regenerated", "provider_requests_made_in_diagnosis",
    "market_data_acquisition_performed_in_diagnosis", "dataset_generation_performed_in_diagnosis",
    "metric_recomputation_from_raw_rows_performed", "model_training_performed",
    "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError(ValueError):
    """Raised when the committed-evidence diagnosis contract is violated."""


def _committed_source_blocked_execution() -> dict[str, Any]:
    return {
        "artifact_kind": source.ARTIFACT_KIND_BLOCKED,
        "execution_status": source.EXECUTION_STATUS_BLOCKED_SOURCE,
        "execution_scope": source.EXECUTION_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest": SOURCE_BLOCKED_EXECUTION_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": SOURCE_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": SOURCE_RECOVERY_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST,
        "source_blocked_after_v2_execution_digest": SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST,
        "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_results_review_v2_digest": SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": SOURCE_MODULE_GROUPING_DIGEST,
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_pytest_passed_count": 24877, "retry_pytest_failed_count": 1292,
        "retry_pytest_error_count": 112, "retry_pytest_skipped_count": 7,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "top_five_module_paths": [item["module_path"] for item in TOP_FIVE],
        "top_5_count_sum": 612, "top_10_count_sum": 1069,
    }


def _validate_source_blocked_execution(blocked: Mapping[str, Any]) -> None:
    expected = _committed_source_blocked_execution()
    mismatches = [key for key, value in expected.items() if blocked.get(key) != value]
    if mismatches:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError(
            f"source blocked execution mismatch: {', '.join(mismatches)}"
        )


def _diagnosis_questions() -> list[dict[str, Any]]:
    answers = [
        ("Was the blocked reentry execution based on the reviewed recovered module grouping source?", True),
        ("Did the reentry execution source expose all 29 module rows?", False),
        ("Did it expose only top-five paths plus aggregate/tier facts?", True),
        ("Did the execution fail because the recovered source itself was invalid?", False),
        ("Did it fail because the committed reentry source did not carry the complete recovered detail forward?", True),
        ("Did source recovery previously recover all 29 module paths?", True),
        ("Did source recovery results review confirm recovered module detail?", True),
        ("Did the later reentry preserve summary-level details rather than the full 29-row source?", True),
        ("Did the reentry execution correctly refuse to invent missing module rows?", True),
        ("Is this a source-detail availability failure?", True),
        ("Was the previous blocker resolved for authority but insufficient for live planning without full rows?", True),
        ("Should the next candidate expose or bind the complete recovered module grouping detail?", True),
    ]
    return [{"question_id": f"question_{index}", "question": question, "answer": answer, "evidence_status": "SUPPORTED_BY_COMMITTED_SOURCE"} for index, (question, answer) in enumerate(answers, 1)]


def _findings() -> list[dict[str, str]]:
    texts = [
        "The blocked reentry execution preserved the correct source chain and did not execute planning.",
        "The source recovery execution recovered module detail and produced a recovery-detail digest.",
        "The source recovery results review accepted the recovered module detail for future planning reentry.",
        "The after-v2 planning reentry accepted the recovered source for future execution only.",
        "The live reentry execution did not have a complete 29-row committed source snapshot available.",
        "The live reentry execution only had aggregate facts, top-five paths, top-five/top-ten concentration, and source digests.",
        "The live reentry execution correctly failed closed because full deterministic priority-tier planning requires all 29 rows.",
        "The implemented success path was tested using an injected complete 29-row snapshot, showing the algorithm path is ready when the source detail is available.",
        "No retry, full pytest, cache read, diagnostic command, remediation, or source recovery rerun occurred.",
        "The next safe step is a separate candidate to expose or bind the complete recovered module grouping detail source.",
    ]
    return [{"finding_id": f"finding_{index}", "finding": text, "evidence_status": "SUPPORTED_BY_COMMITTED_SOURCE"} for index, text in enumerate(texts, 1)]


def _candidate_options() -> list[dict[str, str]]:
    return [
        {"package": "PACKAGE_EXPOSE_COMPLETE_29_ROW_DETAIL_FROM_SOURCE_RECOVERY_EXECUTION_ARTIFACT", "status": "AVAILABLE_FOR_NEXT_CANDIDATE"},
        {"package": "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_HIGH_CONTROL"},
        {"package": "PACKAGE_USE_OPERATOR_PROVIDED_RECOVERY_DETAIL_REPORT_PATH", "status": "AVAILABLE_FOR_NEXT_CANDIDATE"},
        {"package": "PACKAGE_RECONSTRUCT_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_REQUIRES_SEPARATE_APPROVAL"},
        {"package": "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING_REENTRY", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_NOT_RECOMMENDED", "reason": "Top-five paths are available, but this changes the planning contract and does not satisfy the original 29-row priority-tier plan."},
        {"package": "PACKAGE_INFER_MISSING_24_MODULES", "status": "BLOCKED_NOT_ALLOWED"},
        {"package": "PACKAGE_RERUN_PYTEST_TO_RECREATE_DETAIL", "status": "BLOCKED_NOT_ALLOWED"},
        {"package": "PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_REENTRY_REVIEW", "status": "BLOCKED_NOT_ALLOWED"},
        {"package": "PACKAGE_NEW_RETRY_DESPITE_BLOCKED_REENTRY", "status": "BLOCKED_NOT_ALLOWED"},
        {"package": "PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_REENTRY_AND_FAILED_RETRY", "status": "BLOCKED_NOT_ALLOWED"},
    ]


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    outputs_ok = all(
        isinstance(diagnosis.get(output_id), Mapping)
        and diagnosis[output_id].get("status") == GENERATED_RESEARCH_ONLY
        for output_id in OUTPUT_IDS
    )
    pairs: dict[str, tuple[Any, Any]] = {
        "source_reentry_execution_blocked_digest_bound": (SOURCE_BLOCKED_EXECUTION_DIGEST, diagnosis.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (SOURCE_BLOCKED_MANIFEST_DIGEST, diagnosis.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (SOURCE_BLOCKED_REASON, diagnosis.get("blocked_reason")),
        "source_after_v2_planning_reentry_digest_bound": (SOURCE_REENTRY_DIGEST, diagnosis.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (SOURCE_RESULTS_REVIEW_DIGEST, diagnosis.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST, diagnosis.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
        "source_recovery_execution_digest_bound": (SOURCE_RECOVERY_EXECUTION_DIGEST, diagnosis.get("source_module_grouping_source_recovery_execution_digest")),
        "source_recovery_detail_digest_bound": (SOURCE_RECOVERY_DETAIL_DIGEST, diagnosis.get("source_module_grouping_source_recovery_detail_digest")),
        "source_recovery_digest_manifest_bound": (SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST, diagnosis.get("source_module_grouping_source_recovery_digest_manifest_digest")),
        "source_blocked_after_v2_execution_digest_bound": (SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST, diagnosis.get("source_blocked_after_v2_execution_digest")),
        "source_blocked_after_v2_manifest_digest_bound": (SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST, diagnosis.get("source_blocked_after_v2_manifest_digest")),
        "source_after_v2_approval_digest_bound": (SOURCE_AFTER_V2_APPROVAL_DIGEST, diagnosis.get("source_after_v2_approval_digest")),
        "source_results_review_v2_digest_bound": (SOURCE_RESULTS_REVIEW_V2_DIGEST, diagnosis.get("source_results_review_v2_digest")),
        "source_execution_v2_digest_bound": (SOURCE_EXECUTION_V2_DIGEST, diagnosis.get("source_execution_v2_digest")),
        "source_module_grouping_digest_bound": (SOURCE_MODULE_GROUPING_DIGEST, diagnosis.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": (RETRY_EXECUTION_COMMIT, diagnosis.get("retry_execution_commit")),
        "retry_failure_counts_bound": ({"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, diagnosis.get("retry_failure_context", {}).get("counts")),
        "recovered_module_summary_bound": ({"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]}, diagnosis.get("recovered_module_grouping_source_summary")),
        "top_five_paths_bound": (TOP_FIVE, diagnosis.get("top_module_summary")),
        "top_five_count_sum_612_bound": (612, diagnosis.get("top_5_count_sum")),
        "top_ten_count_sum_1069_bound": (1069, diagnosis.get("top_10_count_sum")),
        "available_committed_detail_recorded": (AVAILABLE_COMMITTED_DETAIL, diagnosis.get("available_committed_reentry_detail")),
        "missing_committed_detail_recorded": (MISSING_COMMITTED_DETAIL, diagnosis.get("missing_committed_reentry_detail")),
        "actual_live_reentry_source_lacks_complete_29_rows_true": (True, diagnosis.get("actual_live_reentry_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, diagnosis.get("reentry_success_path_tested_with_complete_29_row_snapshot")),
        "root_cause_classification_completed": (True, diagnosis.get("root_cause_classification_completed")),
        "primary_failure_class_committed_reentry_source_detail_gap": (PRIMARY_FAILURE_CLASS, diagnosis.get("primary_failure_class")),
        "not_root_causes_recorded": (NOT_ROOT_CAUSES, diagnosis.get("not_root_causes")),
        "diagnosis_created_true": (True, diagnosis.get("reentry_failure_diagnosis_created")),
        "diagnosis_ready_true": (True, diagnosis.get("reentry_failure_diagnosis_ready")),
        "source_detail_availability_diagnosed_true": (True, diagnosis.get("source_detail_availability_diagnosed")),
        "committed_reentry_detail_gap_identified_true": (True, diagnosis.get("committed_reentry_detail_gap_identified")),
        "ready_for_detail_exposure_candidate_true": (True, diagnosis.get("ready_for_reentry_module_detail_exposure_or_binding_candidate")),
        "diagnosis_outputs_generated": (True, outputs_ok),
        "recommended_next_package_defined": (RECOMMENDED_NEXT_PACKAGE, diagnosis.get("recommended_next_package")),
        "next_chain_defined": (NEXT_CHAIN, diagnosis.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, diagnosis.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, diagnosis.get("risk_controls")),
        "no_tracked_marketflow_files": (False, diagnosis.get("marketflow_outputs_tracked_in_repository")),
        "no_tracked_pytest_cache_files": (False, diagnosis.get("pytest_cache_tracked_in_repository")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, diagnosis.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, diagnosis.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, diagnosis.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, diagnosis.get("broker_execution")),
    }
    boundary_ids = {
        "module_grouping_detail_exposed_by_diagnosis": "module_grouping_detail_exposed_by_diagnosis_false",
        "module_paths_recovered_by_diagnosis": "module_paths_recovered_by_diagnosis_false",
        "per_module_counts_recovered_by_diagnosis": "per_module_counts_recovered_by_diagnosis_false",
        "bounded_nodeid_samples_recovered_by_diagnosis": "bounded_nodeid_samples_recovered_by_diagnosis_false",
        "after_v2_planning_execution_performed_by_diagnosis": "after_v2_planning_execution_performed_by_diagnosis_false",
        "diagnostic_method_executed": "diagnostic_method_executed_false",
        "code_remediation_executed": "code_remediation_executed_false",
        "evidence_remediation_executed": "evidence_remediation_executed_false",
        "classification_execution_performed_in_diagnosis": "classification_execution_false",
        "cache_read_in_diagnosis": "cache_read_in_diagnosis_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "retry_rerun_performed": "retry_rerun_false", "full_pytest_performed": "full_pytest_false",
        "diagnostic_command_executed": "diagnostic_command_false",
        "diagnostic_output_captured": "diagnostic_output_false",
        "targeted_diagnostic_output_capture_candidate_created": "targeted_diagnostic_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false",
        "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false",
        "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false",
        "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false",
        "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_diagnosis": "provider_requests_false",
        "market_data_acquisition_performed_in_diagnosis": "market_data_acquisition_false",
        "dataset_generation_performed_in_diagnosis": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    pairs.update({check_id: (False, diagnosis.get(field)) for field, check_id in boundary_ids.items()})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(diagnosis: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "reentry_failure_diagnosis_created": diagnosis.get("reentry_failure_diagnosis_created"),
        "reentry_failure_diagnosis_ready": diagnosis.get("reentry_failure_diagnosis_ready"),
        "source_detail_availability_diagnosed": diagnosis.get("source_detail_availability_diagnosed"),
        "committed_reentry_detail_gap_identified": diagnosis.get("committed_reentry_detail_gap_identified"),
        "primary_failure_class": diagnosis.get("primary_failure_class"),
        "actual_live_reentry_execution_blocked": diagnosis.get("actual_live_reentry_execution_blocked"),
        "previous_blocker_resolved_for_reentry_authority": diagnosis.get("previous_blocker_resolved_for_reentry_authority"),
        "complete_29_row_detail_available_to_live_reentry_execution": diagnosis.get("complete_29_row_detail_available_to_live_reentry_execution"),
        "module_grouping_detail_exposed_by_diagnosis": diagnosis.get("module_grouping_detail_exposed_by_diagnosis"),
        "cache_read_in_diagnosis": diagnosis.get("cache_read_in_diagnosis"),
        "source_recovery_rerun_performed": diagnosis.get("source_recovery_rerun_performed"),
        "after_v2_planning_execution_performed_by_diagnosis": diagnosis.get("after_v2_planning_execution_performed_by_diagnosis"),
        "new_retry_candidate_created": diagnosis.get("new_retry_candidate_created"),
        "new_retry_executed": diagnosis.get("new_retry_executed"),
        "integration_execution_successful": diagnosis.get("integration_execution_successful"),
        "recommended_next_package": diagnosis.get("recommended_next_package"),
        "recommended_next_task": diagnosis.get("recommended_next_task"),
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _diagnosis_digest(diagnosis: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(diagnosis))
    for key in ("checklist", "summary", "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest"):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(
    *, source_blocked_execution: dict | None = None,
) -> dict:
    """Build the fail-closed diagnosis without cache, provider, or execution access."""

    blocked = deepcopy(source_blocked_execution) if source_blocked_execution is not None else _committed_source_blocked_execution()
    _validate_source_blocked_execution(blocked)
    root_cause_summary = (
        "The reentry execution had authority to use recovered module grouping evidence, but the committed source "
        "available to the live reentry execution did not expose the complete 29 module rows, per-module counts, "
        "and bounded samples required for deterministic prioritization. The service correctly failed closed "
        "instead of inventing module identities."
    )
    contributing = [
        "Source recovery execution reported full recovery and produced a recovery-detail digest.",
        "Source recovery results review accepted recovered detail.",
        "Reentry artifact accepted source for future planning reentry.",
        "Downstream live execution required complete 29-row detail.",
        "Committed reentry/source constants exposed top-five and aggregate details, not all module rows.",
        "Injected deterministic tests proved the success path only when a complete 29-row snapshot is available.",
    ]
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        "source_reentry_execution_blocked_artifact_kind": blocked["artifact_kind"],
        "source_reentry_execution_blocked_status": blocked["execution_status"],
        "source_reentry_execution_blocked_scope": blocked["execution_scope"],
        "source_reentry_execution_blocked_digest": SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": SOURCE_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": SOURCE_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_execution_digest": SOURCE_RECOVERY_EXECUTION_DIGEST,
        "source_module_grouping_source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST,
        "source_module_grouping_source_recovery_digest_manifest_digest": SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST,
        "source_module_grouping_source_recovery_approval_digest": SOURCE_RECOVERY_APPROVAL_DIGEST,
        "source_module_grouping_source_recovery_operator_review_digest": SOURCE_RECOVERY_OPERATOR_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_candidate_digest": SOURCE_RECOVERY_CANDIDATE_DIGEST,
        "source_blocked_after_v2_execution_digest": SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST,
        "source_blocked_after_v2_manifest_digest": SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST,
        "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_execution_v2_digest": SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": SOURCE_MODULE_GROUPING_DIGEST,
        "source_approval_v2_digest": SOURCE_APPROVAL_V2_DIGEST,
        "source_staged_inventory_digest": SOURCE_STAGED_INVENTORY_DIGEST,
        "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
        "retry_execution_commit": RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, "first_result_authoritative": True, "root_full_regression_is_retry_evidence": False},
        "recovered_module_grouping_source_summary": {"failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "largest_module_nodeid_counts": [136, 131, 122, 112, 111]},
        "top_module_summary": deepcopy(TOP_FIVE), "top_5_count_sum": 612, "top_10_count_sum": 1069,
        "available_committed_reentry_detail": list(AVAILABLE_COMMITTED_DETAIL),
        "missing_committed_reentry_detail": list(MISSING_COMMITTED_DETAIL),
        "diagnosis_questions": _diagnosis_questions(), "diagnosis_findings": _findings(),
        "root_cause_classification": {"primary_failure_class": PRIMARY_FAILURE_CLASS, "root_cause_summary": root_cause_summary, "contributing_factors": contributing},
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "root_cause_summary": root_cause_summary,
        "contributing_factors": contributing, "not_root_causes": list(NOT_ROOT_CAUSES),
        "candidate_recommendation": {"package": RECOMMENDED_NEXT_PACKAGE, "status": "RECOMMENDED_FOR_NEXT_CANDIDATE_NOT_SELECTED", "purpose": "Create a future candidate to expose, bind, or carry forward the complete 29-row recovered module grouping detail from reviewed source recovery evidence so the after-v2 planning execution can re-enter without cache read, inference, or pytest rerun.", "recommended_next_task": RECOMMENDED_NEXT_TASK},
        "supporting_next_options": _candidate_options(), "recommended_next_package": RECOMMENDED_NEXT_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_NEXT_CANDIDATE_NOT_SELECTED",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "reentry_failure_diagnosis_created": True, "reentry_failure_diagnosis_ready": True,
        "source_detail_availability_diagnosed": True, "committed_reentry_detail_gap_identified": True,
        "actual_blocked_reason_preserved": True, "root_cause_classification_completed": True,
        "ready_for_reentry_module_detail_exposure_or_binding_candidate": True,
        "actual_live_reentry_source_lacks_complete_29_rows": True,
        "actual_live_reentry_source_did_not_expose_complete_29_row_snapshot": True,
        "actual_live_reentry_execution_blocked": True,
        "previous_blocker_resolved_for_reentry_authority": True,
        "complete_29_row_detail_available_to_live_reentry_execution": False,
        "reentry_success_path_implemented_with_injected_snapshot": True,
        "reentry_success_path_tested_with_complete_29_row_snapshot": True,
        "success_path_generates_tier_sums": {"tier_1": 612, "tier_2": 457, "tier_3": 335},
        "marketflow_outputs_tracked_in_repository": False, "pytest_cache_tracked_in_repository": False,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    diagnosis.update({key: False for key in FALSE_BOUNDARIES})
    diagnosis.update({
        "failure_modules_classified": False, "error_modules_classified": False,
        "failure_error_separation_claimed": False, "first_failure_identified": False,
        "first_error_identified": False, "first_order_claim_made": False,
        "traceback_root_cause_claimed": False, "direct_code_remediation_recommended": False,
        "retry_success_claimed": False, "main_merge_readiness_claimed": False,
    })
    output_content = {
        "diagnosis_manifest": {"artifact_kind": ARTIFACT_KIND, "primary_failure_class": PRIMARY_FAILURE_CLASS},
        "blocked_reentry_execution_summary": {"digest": SOURCE_BLOCKED_EXECUTION_DIGEST, "blocked_reason": SOURCE_BLOCKED_REASON},
        "source_detail_availability_report": {"available": AVAILABLE_COMMITTED_DETAIL, "complete_29_rows_available": False},
        "missing_committed_detail_report": {"missing": MISSING_COMMITTED_DETAIL},
        "source_chain_detail_carry_forward_report": {"recovery_detail_reviewed": True, "complete_detail_carried_forward": False},
        "root_cause_classification_report": {"primary_failure_class": PRIMARY_FAILURE_CLASS, "summary": root_cause_summary},
        "not_root_cause_report": {"items": NOT_ROOT_CAUSES},
        "next_candidate_options_report": {"options": _candidate_options()},
        "recommended_next_package_report": {"package": RECOMMENDED_NEXT_PACKAGE, "task": RECOMMENDED_NEXT_TASK},
        "unsupported_claims_boundary_report": {"failure_modules_classified": False, "traceback_root_cause_claimed": False, "retry_success_claimed": False},
        "digest_manifest": {"source_blocked_execution_digest": SOURCE_BLOCKED_EXECUTION_DIGEST, "source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST},
    }
    for output_id, content in output_content.items():
        diagnosis[output_id] = {"status": GENERATED_RESEARCH_ONLY, **deepcopy(content)}
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis, diagnosis["checklist"])
    diagnosis["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest"] = _diagnosis_digest(diagnosis)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict:
    """Validate source binding, fail-closed boundaries, outputs, summary, and digest."""

    if not isinstance(diagnosis, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError("diagnosis must be object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "diagnosis_status": DIAGNOSIS_STATUS,
        "diagnosis_scope": DIAGNOSIS_SCOPE, "schema_version": SCHEMA_VERSION,
        "source_reentry_execution_blocked_artifact_kind": source.ARTIFACT_KIND_BLOCKED,
        "source_reentry_execution_blocked_status": source.EXECUTION_STATUS_BLOCKED_SOURCE,
        "source_reentry_execution_blocked_scope": source.EXECUTION_SCOPE,
    }
    for field, expected in fixed.items():
        if diagnosis.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError(f"{field} mismatch")
    checklist = _checklist(diagnosis)
    if diagnosis.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError("checklist invalid")
    expected_summary = _summary(diagnosis, checklist)
    if diagnosis.get("summary") != expected_summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError("summary invalid")
    digest = diagnosis.get("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _diagnosis_digest(diagnosis):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError("diagnosis digest invalid")
    return {
        "artifact_kind": diagnosis["artifact_kind"], "diagnosis_status": diagnosis["diagnosis_status"],
        "diagnosis_scope": diagnosis["diagnosis_scope"], "diagnosis_digest": digest,
        **{key: expected_summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(diagnosis)
    sections = [
        ("Source Blocked Reentry Execution", [SOURCE_BLOCKED_EXECUTION_DIGEST, SOURCE_BLOCKED_REASON]),
        ("Source Planning Reentry", [SOURCE_REENTRY_DIGEST]),
        ("Source Recovery Results Review", [SOURCE_RESULTS_REVIEW_DIGEST, SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped."]),
        ("Recovered Module Grouping Source Summary", [str(diagnosis["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Committed Detail", [*AVAILABLE_COMMITTED_DETAIL, *MISSING_COMMITTED_DETAIL]),
        ("Diagnosis Questions", [f"{item['question']} {item['answer']}" for item in diagnosis["diagnosis_questions"]]),
        ("Diagnosis Findings", [item["finding"] for item in diagnosis["diagnosis_findings"]]),
        ("Root Cause Classification", [PRIMARY_FAILURE_CLASS, diagnosis["root_cause_summary"]]),
        ("Not Root Causes", diagnosis["not_root_causes"]),
        ("Recommended Next Package", [RECOMMENDED_NEXT_PACKAGE, RECOMMENDED_NEXT_TASK]),
        ("Next Chain", diagnosis["next_chain"]), ("Next Gates", diagnosis["next_gates"]),
        ("Risk Controls", diagnosis["risk_controls"]),
        ("Authority Boundaries", ["Diagnosis only: no detail exposure, cache read, execution, retry, provider, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["The source-detail gap is not retry success and is not a root-cause claim about the original pytest failures."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry Failure Diagnosis v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(
    output_dir: str | Path, *, source_blocked_execution: dict | None = None,
) -> dict:
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(source_blocked_execution=source_blocked_execution)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1.md"
    json_path.write_text(json.dumps(diagnosis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_markdown_v1(diagnosis), encoding="utf-8")
    return {"artifact": diagnosis, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = [
    "ARTIFACT_KIND", "DIAGNOSIS_STATUS", "DIAGNOSIS_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_ONLY_NOT_REMEDIATION_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_markdown_v1",
]
