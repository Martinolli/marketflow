"""Diagnose the blocked complete-detail binding execution from committed evidence."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1"
DIAGNOSIS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_READY"
DIAGNOSIS_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_READY = DIAGNOSIS_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN = DIAGNOSIS_SCOPE

SOURCE_BLOCKED_EXECUTION_DIGEST = "9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca"
SOURCE_BLOCKED_MANIFEST_DIGEST = "c732eac857725728bb856f2d145eb86101ce1f839ddca740b66db4d48ae3aa4c"
SOURCE_BLOCKED_REASON = "COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE"
SOURCE_APPROVAL_DIGEST = "384ea3fcb8440c48be01d62a115e9abaf8424ea898832551d80b30383207954f"
SOURCE_OPERATOR_REVIEW_DIGEST = "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b"
SOURCE_CANDIDATE_DIGEST = "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23"
SELECTED_PACKAGE = "PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY"
SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST = "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb"
SOURCE_PRIMARY_FAILURE_CLASS = "COMMITTED_REENTRY_SOURCE_DETAIL_GAP"
SOURCE_REENTRY_BLOCKED_DIGEST = "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49"
SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST = "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99"
SOURCE_REENTRY_BLOCKED_REASON = "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"
SOURCE_PLANNING_REENTRY_DIGEST = "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927"
SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST = "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266"
SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST = "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9"
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
PRIMARY_FAILURE_CLASS = "COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE"
RECOMMENDED_NEXT_PACKAGE = "PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1"
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

AVAILABLE_DATA = [
    "source digests", "retry counts", "recovered detail digest", "aggregate recovery evidence",
    "top-five module paths", "top-five counts", "top-five/top-ten concentration",
    "execution service success path with injected complete 29-row snapshot",
]
MISSING_DATA = [
    "committed complete 29-row module grouping detail source",
    "all 29 module paths in a live committed binding source",
    "all per-module path-bound counts in a live committed binding source",
    "all bounded node-ID samples in a live committed binding source",
    "complete planning-ready 29-row snapshot available without cache read or source-recovery rerun",
]
NOT_ROOT_CAUSES = [
    "not an origin/main change", "not an integration branch change", "not a detached worktree problem",
    "not a staged evidence mutation", "not a cache hash/count failure in the source recovery execution",
    "not a source recovery execution failure", "not a source recovery results review failure",
    "not a planning reentry authority failure", "not a retry rerun problem", "not a full pytest problem",
    "not a provider or market-data issue", "not a runtime or broker issue",
]

NEXT_CHAIN = [
    "Complete 29-row Module Grouping Detail Source Materialization Candidate v1.",
    "Candidate Operator Review.", "Approval, if selected.", "Execution, if approved.", "Results Review.",
    "Detail Exposure or Binding Execution reattempt using complete committed source.",
    "Detail Exposure or Binding Results Review.",
    "Re-enter after-v2 planning execution using complete recovered detail.",
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
    "complete_29_row_module_grouping_detail_source_materialization_candidate",
    "complete_29_row_module_grouping_detail_source_materialization_operator_review",
    "complete_29_row_module_grouping_detail_source_materialization_approval_if_selected",
    "complete_29_row_module_grouping_detail_source_materialization_execution_if_approved",
    "complete_29_row_module_grouping_detail_source_materialization_results_review",
    "detail_exposure_or_binding_execution_reattempt_with_complete_source",
    "detail_exposure_or_binding_results_review", "after_v2_planning_reentry_execution_with_complete_detail",
    "remediation_or_method_results_review_after_classification_v2_review_reentry",
    "targeted_diagnostic_output_capture_candidate_if_supported", "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected", "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes",
]

RISK_CONTROLS = [
    "diagnosis_does_not_fix_detail_binding_execution", "diagnosis_does_not_expose_29_module_rows",
    "diagnosis_does_not_bind_complete_detail", "diagnosis_does_not_recover_module_grouping_again",
    "diagnosis_does_not_read_cache", "diagnosis_does_not_modify_cache", "diagnosis_does_not_parse_operator_logs",
    "diagnosis_does_not_run_diagnostic_commands", "diagnosis_does_not_execute_diagnostics",
    "diagnosis_does_not_execute_remediation", "diagnosis_does_not_execute_classification",
    "diagnosis_does_not_classify_modules_again", "diagnosis_does_not_execute_after_v2_planning_reentry",
    "diagnosis_does_not_rerun_retry", "diagnosis_does_not_run_full_pytest",
    "diagnosis_does_not_create_targeted_diagnostic_candidate", "diagnosis_does_not_create_new_retry_candidate",
    "diagnosis_does_not_create_retry_results_review", "diagnosis_does_not_create_integration_results_review",
    "diagnosis_does_not_mark_integration_successful", "diagnosis_does_not_generate_successful_integration_digest",
    "diagnosis_does_not_claim_failure_error_separation", "diagnosis_does_not_claim_first_failure",
    "diagnosis_does_not_claim_first_error", "diagnosis_does_not_claim_traceback_root_cause",
    "diagnosis_does_not_recommend_direct_code_remediation", "diagnosis_does_not_treat_detail_or_digest_as_retry_success",
    "diagnosis_does_not_push_integration_branch", "diagnosis_does_not_push_main",
    "diagnosis_does_not_delete_integration_branch", "diagnosis_does_not_delete_worktree",
    "diagnosis_does_not_force_push", "diagnosis_does_not_prune_remotes", "diagnosis_does_not_modify_tags",
    "diagnosis_does_not_modify_staged_evidence", "diagnosis_does_not_regenerate_evidence",
    "diagnosis_does_not_call_providers", "diagnosis_does_not_acquire_market_data",
    "diagnosis_does_not_regenerate_dataset", "diagnosis_does_not_recompute_metrics",
    "diagnosis_does_not_train_models", "diagnosis_does_not_score_strategy",
    "diagnosis_does_not_generate_recommendations", "diagnosis_does_not_accept_predictive_usefulness",
    "diagnosis_does_not_accept_profitability", "diagnosis_does_not_authorize_runtime",
    "diagnosis_does_not_authorize_broker_execution", "digest_only_is_not_complete_detail_payload",
    "top_five_only_is_not_complete_29_row_source", "complete_detail_gap_is_not_retry_success",
    "complete_detail_gap_is_not_root_cause_of_original_pytest_failures",
    "previous_blocked_execution_remains_historically_blocked", "previous_source_recovery_results_review_remains_valid",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence",
    "separate_materialization_candidate_required", "separate_approval_required_before_detail_materialization_execution",
    "separate_results_review_required_after_materialization",
    "separate_detail_binding_reattempt_required_after_materialization_review",
    "separate_retry_approval_required_before_new_retry", "protect_origin_main", "preserve_integration_branch",
    "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]

OUTPUT_IDS = [
    "diagnosis_manifest", "blocked_detail_exposure_or_binding_execution_summary",
    "committed_complete_detail_availability_report", "missing_complete_29_row_detail_report",
    "digest_only_is_not_payload_report", "cache_materialization_boundary_report",
    "root_cause_classification_report", "not_root_cause_report", "next_candidate_options_report",
    "recommended_next_package_report", "unsupported_claims_boundary_report", "digest_manifest",
]

FALSE_BOUNDARIES = [
    "complete_29_row_detail_exposed_by_diagnosis", "complete_29_row_detail_bound_by_diagnosis",
    "module_grouping_detail_exposed_by_diagnosis", "module_paths_recovered_by_diagnosis",
    "per_module_counts_recovered_by_diagnosis", "bounded_nodeid_samples_recovered_by_diagnosis",
    "source_recovery_rerun_performed", "cache_read_in_diagnosis", "module_grouping_recovered_in_diagnosis",
    "after_v2_planning_execution_reentry_created_by_diagnosis",
    "after_v2_planning_execution_reentry_performed_by_diagnosis",
    "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created", "new_retry_executed",
    "new_retry_results_review_created", "main_merge_approval_created", "retry_rerun_performed",
    "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
    "diagnostic_method_executed", "code_remediation_executed", "evidence_remediation_executed",
    "classification_execution_performed_in_diagnosis", "integration_execution_successful",
    "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
    "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
    "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
    "provider_requests_made_in_diagnosis", "market_data_acquisition_performed_in_diagnosis",
    "dataset_generation_performed_in_diagnosis", "metric_recomputation_from_raw_rows_performed",
    "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError(ValueError):
    """Raised when the committed-evidence diagnosis contract is violated."""


def _committed_source_blocked_execution() -> dict[str, Any]:
    """Return only the committed summary fields available to this diagnosis."""
    return {
        "artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "execution_status": source.BLOCKED_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest": SOURCE_BLOCKED_EXECUTION_DIGEST,
        "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": SOURCE_BLOCKED_REASON,
        "source_detail_exposure_or_binding_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_detail_exposure_or_binding_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_detail_exposure_or_binding_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "selected_detail_exposure_or_binding_package": SELECTED_PACKAGE,
        "source_reentry_failure_diagnosis_digest": SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST,
        "primary_failure_class": SOURCE_PRIMARY_FAILURE_CLASS,
        "source_reentry_execution_blocked_digest": SOURCE_REENTRY_BLOCKED_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST,
        "source_reentry_execution_blocked_reason": SOURCE_REENTRY_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": SOURCE_PLANNING_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST,
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
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}},
        "recovered_module_grouping_source_summary": {
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        },
        "top_module_summary": deepcopy(TOP_FIVE), "top_5_count_sum": 612, "top_10_count_sum": 1069,
    }


def _validate_source(blocked: Mapping[str, Any]) -> None:
    expected = _committed_source_blocked_execution()
    mismatches = [key for key, value in expected.items() if blocked.get(key) != value]
    if mismatches:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError(
            f"source blocked execution mismatch: {', '.join(mismatches)}"
        )


def _diagnosis_questions() -> list[dict[str, Any]]:
    answers = [
        ("Was the detail exposure/binding execution approved and authorized?", True),
        ("Was the selected package correct?", True),
        ("Did the execution correctly avoid cache read and source recovery rerun?", True),
        ("Did the committed source chain bind a recovery-detail digest?", True),
        ("Did the committed source chain expose the complete 29-row detail payload?", False),
        ("Did source recovery previously prove the complete detail can be produced?", True),
        ("Did results review verify recovery without carrying the full row payload forward?", True),
        ("Did the blocked reentry diagnosis identify a committed source-detail gap?", True),
        ("Did the latest execution fail because the recovered detail itself was invalid?", False),
        ("Did it fail because complete detail was unavailable from committed source structures?", True),
        ("Did the service reject top-five-only, aggregate-only, and digest-only binding?", True),
        ("Did the service refuse to infer the missing 24 rows?", True),
        ("Is this a complete-detail source availability failure?", True),
        ("Should a controlled complete-detail materialization candidate be next?", True),
    ]
    return [
        {"question_id": f"question_{index}", "question": question, "answer": answer,
         "evidence_status": "SUPPORTED_BY_COMMITTED_SOURCE"}
        for index, (question, answer) in enumerate(answers, 1)
    ]


def _findings() -> list[dict[str, str]]:
    texts = [
        "The detail exposure/binding execution preserved the correct source chain and selected package.",
        "The execution was approved to expose or bind complete recovered module grouping detail for future execution only.",
        "The execution correctly did not read cache, rerun recovery, execute planning, diagnostics, remediation, classification, or pytest.",
        "The source recovery chain proves 1,404 failed-or-errored node IDs were grouped across 29 modules.",
        "The committed source chain preserves the recovery-detail digest and summary facts.",
        "The committed source chain does not expose the complete 29 module rows required for binding.",
        "The cache materialization path was prohibited by the execution contract.",
        "Aggregate counts, top-five paths, and digests cannot construct a complete 29-row planning source.",
        "The execution correctly blocked instead of inferring the missing 24 module rows.",
        "The implemented success path is valid only when a complete 29-row source snapshot is provided.",
        "The next safe step is a separately approved candidate to materialize, expose, or bind that source.",
    ]
    return [{"finding_id": f"finding_{i}", "finding": text, "evidence_status": "SUPPORTED_BY_COMMITTED_SOURCE"} for i, text in enumerate(texts, 1)]


def _candidate_options() -> list[dict[str, str]]:
    return [
        {"package": "PACKAGE_MATERIALIZE_COMPLETE_29_ROW_DETAIL_FROM_REVIEWED_CACHE_READ_ONLY", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_REQUIRES_SEPARATE_APPROVAL", "purpose": "Reconstruct and commit a bounded non-secret 29-row planning source from reviewed detached pytest cache under new approval."},
        {"package": "PACKAGE_BIND_COMPLETE_29_ROW_DETAIL_AS_COMMITTED_STATUS_SOURCE_FROM_EXISTING_RECOVERY_ARTIFACT_IF_LOCATABLE", "status": "AVAILABLE_FOR_NEXT_CANDIDATE", "purpose": "Bind an existing complete committed recovery structure only if locatable and digest-verifiable."},
        {"package": "PACKAGE_OPERATOR_PROVIDES_EXISTING_COMPLETE_RECOVERY_DETAIL_REPORT_PATH", "status": "AVAILABLE_FOR_NEXT_CANDIDATE", "purpose": "Bind an operator-provided existing report only if hash-verifiable."},
        {"package": "PACKAGE_CREATE_HIGH_CONTROL_29_ROW_SOURCE_CONSTANT_FROM_REVIEWED_RECOVERY_EVIDENCE", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_HIGH_CONTROL", "purpose": "Add exactly 29 bounded source rows without committing runtime outputs."},
        {"package": "PACKAGE_REDUCED_SCOPE_TOP_FIVE_ONLY_PLANNING", "status": "AVAILABLE_FOR_NEXT_CANDIDATE_NOT_RECOMMENDED", "reason": "It changes the full 29-row planning contract."},
        {"package": "PACKAGE_USE_RECOVERY_DETAIL_DIGEST_AS_PROXY_FOR_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "A digest proves identity, not row payload."},
        {"package": "PACKAGE_INFER_MISSING_24_MODULE_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Source evidence cannot be inferred or fabricated."},
        {"package": "PACKAGE_RERUN_PYTEST_TO_RECREATE_ROWS", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "The failed retry remains authoritative."},
        {"package": "PACKAGE_DIRECT_DIAGNOSTIC_CAPTURE_WITHOUT_COMPLETE_DETAIL_REVIEW", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Diagnostic capture remains separately gated."},
        {"package": "PACKAGE_NEW_RETRY_DESPITE_BLOCKED_DETAIL_BINDING", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "A new retry remains blocked."},
        {"package": "PACKAGE_MAIN_MERGE_DESPITE_BLOCKED_DETAIL_BINDING_AND_FAILED_RETRY", "status": "BLOCKED_NOT_ALLOWED", "blocked_reason": "Main merge requires a passing future retry review."},
    ]


def _record(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(diagnosis: Mapping[str, Any]) -> list[dict[str, Any]]:
    outputs_ok = all(
        isinstance(diagnosis.get(output_id), Mapping)
        and diagnosis[output_id].get("status") == GENERATED_RESEARCH_ONLY
        for output_id in OUTPUT_IDS
    )
    pairs: dict[str, tuple[Any, Any]] = {
        "source_detail_binding_execution_blocked_digest_bound": (SOURCE_BLOCKED_EXECUTION_DIGEST, diagnosis.get("source_detail_exposure_or_binding_execution_blocked_digest")),
        "source_detail_binding_execution_blocked_manifest_digest_bound": (SOURCE_BLOCKED_MANIFEST_DIGEST, diagnosis.get("source_detail_exposure_or_binding_execution_blocked_manifest_digest")),
        "source_detail_binding_execution_blocked_reason_bound": (SOURCE_BLOCKED_REASON, diagnosis.get("blocked_reason")),
        "source_detail_binding_approval_digest_bound": (SOURCE_APPROVAL_DIGEST, diagnosis.get("source_detail_exposure_or_binding_approval_digest")),
        "source_detail_binding_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST, diagnosis.get("source_detail_exposure_or_binding_operator_review_digest")),
        "source_detail_binding_candidate_digest_bound": (SOURCE_CANDIDATE_DIGEST, diagnosis.get("source_detail_exposure_or_binding_candidate_digest")),
        "source_reentry_failure_diagnosis_digest_bound": (SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST, diagnosis.get("source_reentry_failure_diagnosis_digest")),
        "source_primary_failure_class_bound": (SOURCE_PRIMARY_FAILURE_CLASS, diagnosis.get("source_primary_failure_class")),
        "source_reentry_execution_blocked_digest_bound": (SOURCE_REENTRY_BLOCKED_DIGEST, diagnosis.get("source_reentry_execution_blocked_digest")),
        "source_reentry_execution_blocked_manifest_digest_bound": (SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST, diagnosis.get("source_reentry_execution_blocked_manifest_digest")),
        "source_reentry_execution_blocked_reason_bound": (SOURCE_REENTRY_BLOCKED_REASON, diagnosis.get("source_reentry_execution_blocked_reason")),
        "source_planning_reentry_digest_bound": (SOURCE_PLANNING_REENTRY_DIGEST, diagnosis.get("source_after_v2_planning_reentry_digest")),
        "source_recovery_results_review_digest_bound": (SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, diagnosis.get("source_module_grouping_source_recovery_results_review_digest")),
        "source_recovery_results_review_manifest_digest_bound": (SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST, diagnosis.get("source_module_grouping_source_recovery_results_review_manifest_digest")),
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
        "source_execution_available_data_recorded": (AVAILABLE_DATA, diagnosis.get("source_execution_available_data")),
        "source_execution_missing_data_recorded": (MISSING_DATA, diagnosis.get("source_execution_missing_data")),
        "actual_live_detail_binding_source_lacks_complete_29_rows_true": (True, diagnosis.get("actual_live_detail_binding_source_lacks_complete_29_rows")),
        "success_path_with_injected_snapshot_recorded": (True, diagnosis.get("detail_binding_success_path_tested_with_complete_29_row_snapshot")),
        "root_cause_classification_completed": (True, diagnosis.get("root_cause_classification_completed")),
        "primary_failure_class_committed_complete_29_row_detail_source_unavailable": (PRIMARY_FAILURE_CLASS, diagnosis.get("primary_failure_class")),
        "not_root_causes_recorded": (NOT_ROOT_CAUSES, diagnosis.get("not_root_causes")),
        "diagnosis_created_true": (True, diagnosis.get("detail_exposure_or_binding_execution_failure_diagnosis_created")),
        "diagnosis_ready_true": (True, diagnosis.get("detail_exposure_or_binding_execution_failure_diagnosis_ready")),
        "complete_29_row_source_availability_diagnosed_true": (True, diagnosis.get("complete_29_row_source_availability_diagnosed")),
        "committed_complete_29_row_detail_source_gap_identified_true": (True, diagnosis.get("committed_complete_29_row_detail_source_gap_identified")),
        "ready_for_complete_29_row_detail_source_materialization_candidate_true": (True, diagnosis.get("ready_for_complete_29_row_detail_source_materialization_candidate")),
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
    boundary_check_ids = {
        "complete_29_row_detail_exposed_by_diagnosis": "complete_29_row_detail_exposed_by_diagnosis_false",
        "complete_29_row_detail_bound_by_diagnosis": "complete_29_row_detail_bound_by_diagnosis_false",
        "module_grouping_detail_exposed_by_diagnosis": "module_grouping_detail_exposed_by_diagnosis_false",
        "module_paths_recovered_by_diagnosis": "module_paths_recovered_by_diagnosis_false",
        "per_module_counts_recovered_by_diagnosis": "per_module_counts_recovered_by_diagnosis_false",
        "bounded_nodeid_samples_recovered_by_diagnosis": "bounded_nodeid_samples_recovered_by_diagnosis_false",
        "source_recovery_rerun_performed": "source_recovery_rerun_false",
        "cache_read_in_diagnosis": "cache_read_in_diagnosis_false",
        "module_grouping_recovered_in_diagnosis": "module_grouping_recovered_in_diagnosis_false",
        "after_v2_planning_execution_reentry_created_by_diagnosis": "planning_reentry_created_by_diagnosis_false",
        "after_v2_planning_execution_reentry_performed_by_diagnosis": "planning_reentry_performed_by_diagnosis_false",
        "targeted_diagnostic_output_capture_candidate_created": "targeted_diagnostic_candidate_created_false",
        "new_retry_candidate_created": "new_retry_candidate_created_false", "new_retry_executed": "new_retry_executed_false",
        "new_retry_results_review_created": "new_retry_results_review_created_false",
        "main_merge_approval_created": "main_merge_approval_created_false", "retry_rerun_performed": "retry_rerun_false",
        "full_pytest_performed": "full_pytest_false", "diagnostic_command_executed": "diagnostic_command_false",
        "diagnostic_output_captured": "diagnostic_output_false", "diagnostic_method_executed": "diagnostic_method_executed_false",
        "code_remediation_executed": "code_remediation_executed_false", "evidence_remediation_executed": "evidence_remediation_executed_false",
        "classification_execution_performed_in_diagnosis": "classification_execution_false",
        "integration_execution_successful": "integration_success_false",
        "successful_integration_execution_digest_generated": "successful_integration_digest_false",
        "successful_integration_validation_digest_generated": "successful_integration_validation_digest_false",
        "integration_branch_pushed": "integration_branch_pushed_false", "main_push_performed": "main_push_false",
        "origin_main_modified_by_this_task": "origin_main_modified_false", "marketflow_outputs_committed": "marketflow_outputs_committed_false",
        "pytest_cache_committed": "pytest_cache_committed_false", "evidence_regenerated": "evidence_regenerated_false",
        "provider_requests_made_in_diagnosis": "provider_requests_false",
        "market_data_acquisition_performed_in_diagnosis": "market_data_acquisition_false",
        "dataset_generation_performed_in_diagnosis": "dataset_generation_false",
        "metric_recomputation_from_raw_rows_performed": "metric_recomputation_false",
        "model_training_performed": "model_training_false", "strategy_scoring_performed": "strategy_scoring_false",
        "trade_recommendations_generated": "recommendations_false",
    }
    pairs.update({check_id: (False, diagnosis.get(field)) for field, check_id in boundary_check_ids.items()})
    return [_record(check_id, expected, actual) for check_id, (expected, actual) in pairs.items()]


def _summary(diagnosis: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "detail_exposure_or_binding_execution_failure_diagnosis_created": diagnosis.get("detail_exposure_or_binding_execution_failure_diagnosis_created"),
        "detail_exposure_or_binding_execution_failure_diagnosis_ready": diagnosis.get("detail_exposure_or_binding_execution_failure_diagnosis_ready"),
        "complete_29_row_source_availability_diagnosed": diagnosis.get("complete_29_row_source_availability_diagnosed"),
        "committed_complete_29_row_detail_source_gap_identified": diagnosis.get("committed_complete_29_row_detail_source_gap_identified"),
        "primary_failure_class": diagnosis.get("primary_failure_class"),
        "actual_live_detail_binding_execution_blocked": diagnosis.get("actual_live_detail_binding_execution_blocked"),
        "complete_29_row_detail_available_to_live_binding_execution": diagnosis.get("complete_29_row_detail_available_to_live_binding_execution"),
        "complete_29_row_detail_exposed_by_diagnosis": diagnosis.get("complete_29_row_detail_exposed_by_diagnosis"),
        "complete_29_row_detail_bound_by_diagnosis": diagnosis.get("complete_29_row_detail_bound_by_diagnosis"),
        "cache_read_in_diagnosis": diagnosis.get("cache_read_in_diagnosis"),
        "source_recovery_rerun_performed": diagnosis.get("source_recovery_rerun_performed"),
        "after_v2_planning_execution_reentry_performed_by_diagnosis": diagnosis.get("after_v2_planning_execution_reentry_performed_by_diagnosis"),
        "targeted_diagnostic_output_capture_candidate_created": diagnosis.get("targeted_diagnostic_output_capture_candidate_created"),
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
    for key in (
        "checklist", "summary",
        "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_digest",
    ):
        payload.pop(key, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(
    *, source_blocked_execution: dict | None = None,
) -> dict:
    """Build a deterministic diagnosis without cache, recovery, or retry access."""

    blocked = deepcopy(source_blocked_execution) if source_blocked_execution is not None else _committed_source_blocked_execution()
    _validate_source(blocked)
    root_cause_summary = (
        "The detail exposure/binding execution had approval to bind complete recovered module grouping detail, "
        "but the committed source artifacts available to the execution contained only the recovery-detail digest, "
        "aggregate recovery facts, top-five paths, and concentration summaries. The complete 29 module rows, "
        "per-module counts, and bounded samples were not available as committed source structures. The service "
        "correctly failed closed rather than rereading cache, rerunning source recovery, or inventing missing module rows."
    )
    contributing_factors = [
        "Source recovery execution previously recovered the 29-row detail and produced a recovery-detail digest.",
        "Source recovery results review accepted the recovered detail and summary evidence.",
        "The after-v2 planning reentry accepted the recovered source for future planning authority.",
        "The reentry execution and later detail binding execution both required complete 29-row detail.",
        "The committed interface carried forward summaries and digests, not the full payload.",
        "The only known live materialization path depends on detached pytest cache, which execution was forbidden to read.",
        "Deterministic injected tests proved the algorithm succeeds when a full 29-row snapshot is provided.",
        "The live execution correctly blocked because no complete committed 29-row snapshot existed.",
    ]
    diagnosis: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "created_offline": True, "governance_only": True, "diagnosis_only": True,
        "source_detail_exposure_or_binding_execution_blocked_artifact_kind": blocked["artifact_kind"],
        "source_detail_exposure_or_binding_execution_blocked_status": blocked["execution_status"],
        "source_detail_exposure_or_binding_execution_blocked_scope": blocked["execution_scope"],
        "source_detail_exposure_or_binding_execution_blocked_digest": SOURCE_BLOCKED_EXECUTION_DIGEST,
        "source_detail_exposure_or_binding_execution_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
        "blocked_reason": SOURCE_BLOCKED_REASON,
        "source_detail_exposure_or_binding_approval_digest": SOURCE_APPROVAL_DIGEST,
        "source_detail_exposure_or_binding_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_detail_exposure_or_binding_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "selected_detail_exposure_or_binding_package": SELECTED_PACKAGE,
        "source_reentry_failure_diagnosis_digest": SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST,
        "source_primary_failure_class": SOURCE_PRIMARY_FAILURE_CLASS,
        "source_reentry_execution_blocked_digest": SOURCE_REENTRY_BLOCKED_DIGEST,
        "source_reentry_execution_blocked_manifest_digest": SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST,
        "source_reentry_execution_blocked_reason": SOURCE_REENTRY_BLOCKED_REASON,
        "source_after_v2_planning_reentry_digest": SOURCE_PLANNING_REENTRY_DIGEST,
        "source_module_grouping_source_recovery_results_review_digest": SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST,
        "source_module_grouping_source_recovery_results_review_manifest_digest": SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST,
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
        "retry_pytest_working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "retry_failure_context": {
            "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
            "first_result_authoritative": True, "retry_pytest_passed": False, "retry_pytest_failed": True,
            "root_full_regression_is_retry_evidence": False,
        },
        "recovered_module_grouping_source_summary": {
            "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
            "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        },
        "top_module_summary": deepcopy(TOP_FIVE), "top_5_count_sum": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage_of_failed_or_errored_nodeids": "76.13960114",
        "source_execution_available_data": list(AVAILABLE_DATA),
        "source_execution_missing_data": list(MISSING_DATA),
        "diagnosis_questions": _diagnosis_questions(), "diagnosis_findings": _findings(),
        "root_cause_classification": {
            "primary_failure_class": PRIMARY_FAILURE_CLASS, "root_cause_summary": root_cause_summary,
            "contributing_factors": contributing_factors,
        },
        "primary_failure_class": PRIMARY_FAILURE_CLASS, "root_cause_summary": root_cause_summary,
        "contributing_factors": contributing_factors, "not_root_causes": list(NOT_ROOT_CAUSES),
        "candidate_recommendation": {
            "package": RECOMMENDED_NEXT_PACKAGE, "status": "RECOMMENDED_FOR_NEXT_CANDIDATE_NOT_SELECTED",
            "purpose": "Create a future candidate to materialize, expose, or bind the complete 29-row recovered module grouping detail source required for deterministic planning reentry, without inference, retry rerun, provider calls, or main-merge authority.",
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
        },
        "supporting_next_options": _candidate_options(), "recommended_next_package": RECOMMENDED_NEXT_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_NEXT_CANDIDATE_NOT_SELECTED",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "detail_exposure_or_binding_execution_failure_diagnosis_created": True,
        "detail_exposure_or_binding_execution_failure_diagnosis_ready": True,
        "complete_29_row_source_availability_diagnosed": True,
        "committed_complete_29_row_detail_source_gap_identified": True,
        "actual_blocked_reason_preserved": True, "root_cause_classification_completed": True,
        "ready_for_complete_29_row_detail_source_materialization_candidate": True,
        "detail_exposure_or_binding_executed": True,
        "complete_29_row_detail_exposed": False, "complete_29_row_detail_bound": False,
        "complete_29_row_detail_source_identified": False,
        "module_grouping_detail_exposed_by_execution": False,
        "module_paths_bound_by_execution": False, "per_module_counts_bound_by_execution": False,
        "bounded_nodeid_samples_bound_by_execution": False, "planned_outputs_generated": False,
        "actual_live_detail_binding_source_lacks_complete_29_rows": True,
        "actual_live_detail_binding_source_did_not_expose_complete_29_row_snapshot": True,
        "actual_live_detail_binding_execution_blocked": True,
        "complete_29_row_detail_available_to_live_binding_execution": False,
        "detail_binding_success_path_implemented_with_injected_snapshot": True,
        "detail_binding_success_path_tested_with_complete_29_row_snapshot": True,
        "success_path_expected_tier_sums": {"tier_1": 612, "tier_2": 457, "tier_3": 335},
        "module_grouping_source_recovery_execution_reviewed": True, "module_grouping_detail_reviewed": True,
        "module_paths_reviewed": True, "per_module_counts_reviewed": True,
        "bounded_nodeid_samples_reviewed": True, "top_module_source_detail_reviewed": True,
        "cache_hash_and_count_verification_reviewed": True, "source_recovery_limitations_reviewed": True,
        "unsupported_claims_boundary_reviewed": True,
        "recovered_module_grouping_source_accepted_for_planning_reentry": True,
        "accepted_source_type": "RECOVERED_REVIEWED_DETACHED_PYTEST_CACHE_MODULE_GROUPING_DETAIL",
        "module_grouping_source_recovery_executed": True, "module_grouping_detail_recovered": True,
        "module_grouping_detail_exposed": True, "module_paths_recovered": True,
        "per_module_counts_recovered": True, "bounded_nodeid_samples_recovered": True,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "marketflow_outputs_tracked_in_repository": False, "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False, "pytest_cache_tracked_in_detached_worktree": False,
        "origin_main_commit": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "detached_integration_worktree_head_commit": "220fbc220365fce9cae13ab4853cddff118c0187",
        "staged_evidence_manifest_digest": SOURCE_STAGED_INVENTORY_DIGEST, "staged_evidence_unchanged": True,
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
        "blocked_detail_exposure_or_binding_execution_summary": {"digest": SOURCE_BLOCKED_EXECUTION_DIGEST, "blocked_reason": SOURCE_BLOCKED_REASON},
        "committed_complete_detail_availability_report": {"available": AVAILABLE_DATA, "complete_29_rows_available": False},
        "missing_complete_29_row_detail_report": {"missing": MISSING_DATA},
        "digest_only_is_not_payload_report": {"detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST, "digest_is_row_payload": False},
        "cache_materialization_boundary_report": {"cache_read_performed": False, "separate_approval_required": True},
        "root_cause_classification_report": {"primary_failure_class": PRIMARY_FAILURE_CLASS, "summary": root_cause_summary},
        "not_root_cause_report": {"items": NOT_ROOT_CAUSES},
        "next_candidate_options_report": {"options": _candidate_options()},
        "recommended_next_package_report": {"package": RECOMMENDED_NEXT_PACKAGE, "task": RECOMMENDED_NEXT_TASK},
        "unsupported_claims_boundary_report": {"failure_modules_classified": False, "traceback_root_cause_claimed": False, "retry_success_claimed": False},
        "digest_manifest": {"source_blocked_execution_digest": SOURCE_BLOCKED_EXECUTION_DIGEST, "source_blocked_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST, "source_recovery_detail_digest": SOURCE_RECOVERY_DETAIL_DIGEST},
    }
    for output_id, content in output_content.items():
        diagnosis[output_id] = {"status": GENERATED_RESEARCH_ONLY, **deepcopy(content)}
    diagnosis["checklist"] = _checklist(diagnosis)
    diagnosis["summary"] = _summary(diagnosis, diagnosis["checklist"])
    digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_digest"
    diagnosis[digest_key] = _diagnosis_digest(diagnosis)
    validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(diagnosis)
    return diagnosis


def validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(
    diagnosis: dict,
) -> dict:
    """Validate all source bindings, fail-closed boundaries, outputs, and digest."""

    if not isinstance(diagnosis, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError("diagnosis must be object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "diagnosis_status": DIAGNOSIS_STATUS, "diagnosis_scope": DIAGNOSIS_SCOPE,
        "source_detail_exposure_or_binding_execution_blocked_artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "source_detail_exposure_or_binding_execution_blocked_status": source.BLOCKED_STATUS,
        "source_detail_exposure_or_binding_execution_blocked_scope": source.EXECUTION_SCOPE,
    }
    for field, expected in fixed.items():
        if diagnosis.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError(f"{field} mismatch")
    checklist = _checklist(diagnosis)
    if diagnosis.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError("checklist invalid")
    summary = _summary(diagnosis, checklist)
    if diagnosis.get("summary") != summary:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError("summary invalid")
    digest_key = "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_digest"
    digest = diagnosis.get(digest_key)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != _diagnosis_digest(diagnosis):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError("diagnosis digest invalid")
    return {
        "artifact_kind": diagnosis["artifact_kind"], "diagnosis_status": diagnosis["diagnosis_status"],
        "diagnosis_scope": diagnosis["diagnosis_scope"], "diagnosis_digest": digest,
        **{key: summary[key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_markdown_v1(
    diagnosis: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(diagnosis)
    sections = [
        ("Source Blocked Detail Exposure or Binding Execution", [SOURCE_BLOCKED_EXECUTION_DIGEST, SOURCE_BLOCKED_MANIFEST_DIGEST, SOURCE_BLOCKED_REASON]),
        ("Source Approval and Operator Review", [SOURCE_APPROVAL_DIGEST, SOURCE_OPERATOR_REVIEW_DIGEST, SOURCE_CANDIDATE_DIGEST]),
        ("Source Reentry Failure Diagnosis", [SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST, SOURCE_PRIMARY_FAILURE_CLASS]),
        ("Source Recovery Results Review", [SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST, SOURCE_RECOVERY_DETAIL_DIGEST]),
        ("Retry Failure Context", ["24,877 passed, 1,292 failed, 112 errors, 7 skipped; the first retry result remains authoritative."]),
        ("Recovered Module Grouping Source Summary", [str(diagnosis["recovered_module_grouping_source_summary"])]),
        ("Available and Missing Detail Source", [*AVAILABLE_DATA, *MISSING_DATA]),
        ("Diagnosis Questions", [f"{item['question']} {item['answer']}" for item in diagnosis["diagnosis_questions"]]),
        ("Diagnosis Findings", [item["finding"] for item in diagnosis["diagnosis_findings"]]),
        ("Root Cause Classification", [PRIMARY_FAILURE_CLASS, diagnosis["root_cause_summary"]]),
        ("Not Root Causes", diagnosis["not_root_causes"]),
        ("Recommended Next Package", [RECOMMENDED_NEXT_PACKAGE, RECOMMENDED_NEXT_TASK]),
        ("Next Chain", diagnosis["next_chain"]), ("Next Gates", diagnosis["next_gates"]),
        ("Risk Controls", diagnosis["risk_controls"]),
        ("Authority Boundaries", ["Diagnosis only: no detail exposure or binding, cache read, recovery, planning, retry, provider, runtime, or trading authority."]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} pass."]),
        ("Guardrails", ["A digest is not the missing row payload. This source gap is neither retry success nor the root cause of the original pytest failures."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Execution Failure Diagnosis v1", ""]
    for heading, rows in sections:
        lines.extend([f"## {heading}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(
    output_dir: str | Path, *, source_blocked_execution: dict | None = None,
) -> dict:
    diagnosis = build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(
        source_blocked_execution=source_blocked_execution
    )
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1.json"
    markdown_path = target / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1.md"
    json_path.write_text(json.dumps(diagnosis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_markdown_v1(diagnosis),
        encoding="utf-8",
    )
    return {"artifact": diagnosis, "json_path": str(json_path), "markdown_path": str(markdown_path)}


__all__ = [
    "ARTIFACT_KIND", "DIAGNOSIS_STATUS", "DIAGNOSIS_SCOPE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_DETAIL_EXPOSURE_NOT_SOURCE_RECOVERY_NOT_REENTRY_NOT_RETRY_NOT_MAIN",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_markdown_v1",
]
