"""Approve the after-v2 planning package for future execution only."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_service
    as source,
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW_V1 = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW"
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE = source.source.RECOMMENDED_PACKAGE
SOURCE_OPERATOR_REVIEW_DIGEST = "9ea3399758004bdfeb179ad9315a13ebce4514bd51e2cf3b9d39f507a3f1cf03"
REQUIRED_OPERATOR_ATTESTATION_PHRASE = "APPROVE AFTER CLASSIFICATION V2 REMEDIATION METHOD PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING MARKETFLOW PRIORITIZE LARGEST MODULE GROUPS FOR PLANNING ONLY NO REMEDIATION NO DIAGNOSTICS NO RETRY NO FULL PYTEST NO RESULTS REVIEW NO MAIN PUSH AFTER_V2_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
OPERATOR_DECISION = "APPROVE_AFTER_CLASSIFICATION_V2_REMEDIATION_METHOD"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_attestation_v1"
APPROVED_ONLY = "APPROVED_FOR_FUTURE_AFTER_V2_REMEDIATION_OR_METHOD_EXECUTION_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_V1"
NOT_ACCEPTED, NOT_AUTHORIZED, PASS, FAIL, BLOCKER = "not accepted", "NOT_AUTHORIZED", "PASS", "FAIL", "BLOCKER"

ATTESTATION_BOOLEAN_FIELDS = [
    "operator_confirms_retry_failure_counts", "operator_confirms_module_grouping_reviewed",
    "operator_confirms_module_count_29", "operator_confirms_largest_module_counts",
    "operator_confirms_unsupported_claims_boundary", "operator_confirms_approval_scope_only",
    "operator_confirms_no_remediation_execution", "operator_confirms_no_diagnostic_execution",
    "operator_confirms_no_classification_execution", "operator_confirms_no_retry",
    "operator_confirms_no_full_pytest", "operator_confirms_no_retry_results_review",
    "operator_confirms_no_integration_results_review", "operator_confirms_no_integration_success",
    "operator_confirms_no_successful_integration_digest", "operator_confirms_no_integration_branch_push",
    "operator_confirms_no_main_push", "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_branch_delete", "operator_confirms_no_force_push",
    "operator_confirms_no_tag_mutation", "operator_confirms_no_evidence_regeneration",
    "operator_confirms_no_marketflow_commit", "operator_confirms_no_pytest_cache_commit",
    "operator_confirms_no_provider_requests", "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation", "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training", "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations", "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance", "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized", "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]
APPROVED_REQUIREMENTS = {
    "source_operator_review_must_be_ready": True, "source_after_v2_candidate_must_be_ready": True,
    "source_results_review_v2_must_be_ready": True, "module_grouping_digest_must_be_bound": True,
    "module_summary_must_be_bound": True, "unsupported_claims_must_be_preserved": True,
    "approval_must_not_execute_remediation_or_diagnostics": True,
    "execution_must_prioritize_modules_without_direct_code_change": True,
    "execution_must_not_claim_root_cause": True, "execution_must_not_create_retry_candidate": True,
    "execution_must_not_run_retry": True, "future_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
APPROVED_FUTURE_REQUIREMENTS = [{"requirement_id": k, "requirement_value": v, "approval_status": APPROVED_ONLY} for k, v in APPROVED_REQUIREMENTS.items()]
FUTURE_PLAN_STEPS = [
    "Bind source operator-review digest, candidate digest, results-review-v2 digest, and module-grouping digest.",
    "Use reviewed module grouping only as prioritization evidence.",
    "Identify largest module groups and cumulative concentration.",
    "Define diagnostic/remediation planning buckets: top-module diagnostic-output capture; missing evidence-root review; path/cwd assumption review; digest constant drift review; fixture isolation review.",
    "Preserve unsupported-claims boundary.",
    "Recommend one next package after execution review.",
    "Keep new retry candidate, main merge, runtime, and trading closed.",
]
APPROVED_FUTURE_PLAN = [{"step_id": f"future_plan_step_{i:02d}", "source_step": step, "approval_status": APPROVED_ONLY, "execution_status": "NOT_EXECUTED"} for i, step in enumerate(FUTURE_PLAN_STEPS, 1)]
AUTHORIZED_PLANNED_OUTPUTS = [{"output_id": name, "authorization_status": "AUTHORIZED_NOT_GENERATED"} for name in source.source.PLANNED_OUTPUTS]
SUPPORTING_PACKAGE_STATUSES = {
    "PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS": "AVAILABLE_NOT_SELECTED_HIGH_CONTROL",
    "PACKAGE_EVIDENCE_ROOT_REQUIREMENT_REVIEW_FOR_CLASSIFIED_MODULES": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_PATH_CWD_ASSUMPTION_REVIEW_FOR_CLASSIFIED_MODULES": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_DIGEST_CONSTANT_DRIFT_REVIEW_FOR_CLASSIFIED_MODULES": "AVAILABLE_NOT_SELECTED",
    "PACKAGE_TEST_FIXTURE_ISOLATION_REVIEW_FOR_CLASSIFIED_MODULES": "AVAILABLE_NOT_SELECTED",
}
SUPPORTING_PACKAGES = [{"package_id": k, "approval_status": v, "selected": False, "approved": False} for k, v in SUPPORTING_PACKAGE_STATUSES.items()]
BLOCKED_PACKAGES = [{"package_id": k, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False} for k in (
    "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_MODULE_NAMES_ONLY",
    "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_OR_DIAGNOSTIC_ACTION",
    "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY_AND_MODULE_CLASSIFICATION",
)]
NEXT_CHAIN = [
    "Remediation or Method Execution After Classification v2 Review, if approved.",
    "Remediation or Method Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = ["remediation_or_method_execution_after_v2_review_if_approved", "remediation_or_method_results_review", "new_integration_branch_retry_candidate_after_remediation_or_method_review", "new_integration_branch_retry_approval_if_selected", "new_integration_branch_retry_execution_if_approved", "new_integration_branch_retry_results_review", "main_merge_approval_if_new_retry_passes"]
RISK_CONTROLS = [
    "approval_after_v2_does_not_execute_remediation", "approval_after_v2_does_not_execute_diagnostics",
    "approval_after_v2_does_not_execute_classification", "approval_after_v2_does_not_read_cache",
    "approval_after_v2_does_not_run_retry", "approval_after_v2_does_not_run_full_pytest",
    "approval_after_v2_does_not_create_new_retry_candidate", "approval_after_v2_does_not_create_retry_results_review",
    "approval_after_v2_does_not_create_integration_results_review", "approval_after_v2_does_not_mark_integration_successful",
    "approval_after_v2_does_not_generate_successful_integration_digest", "approval_after_v2_does_not_claim_failure_error_separation",
    "approval_after_v2_does_not_claim_first_failure", "approval_after_v2_does_not_claim_traceback_root_cause",
    "approval_after_v2_does_not_treat_classification_as_retry_success", "approval_after_v2_does_not_push_integration_branch",
    "approval_after_v2_does_not_push_main", "approval_after_v2_does_not_delete_integration_branch",
    "approval_after_v2_does_not_delete_worktree", "approval_after_v2_does_not_force_push",
    "approval_after_v2_does_not_prune_remotes", "approval_after_v2_does_not_modify_tags",
    "approval_after_v2_does_not_commit_marketflow_outputs", "approval_after_v2_does_not_commit_pytest_cache",
    "approval_after_v2_does_not_modify_staged_evidence", "approval_after_v2_does_not_regenerate_evidence",
    "approval_after_v2_does_not_call_providers", "approval_after_v2_does_not_acquire_market_data",
    "approval_after_v2_does_not_regenerate_dataset", "approval_after_v2_does_not_recompute_metrics",
    "approval_after_v2_does_not_train_models", "approval_after_v2_does_not_score_strategy",
    "approval_after_v2_does_not_generate_recommendations", "approval_after_v2_does_not_accept_predictive_usefulness",
    "approval_after_v2_does_not_accept_profitability", "approval_after_v2_does_not_authorize_runtime",
    "approval_after_v2_does_not_authorize_broker_execution", "selected_after_v2_package_approved_for_future_execution_only",
    "first_retry_failure_remains_authoritative", "root_regression_not_retry_evidence", "separate_execution_required",
    "separate_results_review_required", "separate_retry_approval_required_before_new_retry", "protect_origin_main",
    "preserve_integration_branch", "preserve_staged_frozen_evidence", "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags", "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_operator_review_digest_bound", "source_after_v2_candidate_digest_bound", "source_results_review_v2_digest_bound",
    "source_review_manifest_digest_bound", "source_execution_v2_digest_bound", "source_module_grouping_digest_bound",
    "retry_execution_commit_bound", "retry_failure_counts_bound", "module_grouping_reviewed_bound", "module_count_29_bound",
    "largest_module_counts_bound", "unsupported_claims_bound", "operator_decision_matches", "operator_attestation_phrase_matches",
    "approval_scope_only", "selected_package_prioritize_largest_modules", "approval_created_true", "method_selected_true",
    "method_approved_true", "method_authorized_true", "ready_for_execution_true", "method_executed_false",
    "diagnostic_method_executed_false", "code_remediation_executed_false", "evidence_remediation_executed_false",
    "new_retry_candidate_created_false", "new_retry_executed_false", "new_retry_results_review_created_false",
    "main_merge_approval_created_false", "retry_rerun_false", "full_pytest_false", "diagnostic_command_false",
    "diagnostic_output_false", "integration_success_false", "successful_integration_digest_false",
    "integration_branch_pushed_false", "main_push_false", "origin_main_modified_false", "marketflow_outputs_committed_false",
    "pytest_cache_committed_false", "evidence_regenerated_false", "provider_requests_false", "market_data_acquisition_false",
    "dataset_generation_false", "metric_recomputation_false", "model_training_false", "strategy_scoring_false",
    "recommendations_false", "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "broker_not_authorized", "requirements_approved_for_future_execution", "future_plan_approved_not_executed",
    "planned_outputs_authorized_not_generated", "supporting_packages_not_selected", "blocked_packages_not_approved",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files", "no_tracked_pytest_cache_files",
]

class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError(ValueError):
    pass

def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"): return False
    try: return datetime.fromisoformat(value[:-1] + "+00:00").utcoffset() is not None
    except ValueError: return False

def _validate_attestation(a: Mapping[str, Any]) -> None:
    expected = {
        "operator_decision": OPERATOR_DECISION,
        "selected_remediation_or_method_after_v2_package": SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,
        "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "operator_confirms_source_results_review_v2_digest": source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "operator_confirms_source_review_manifest_digest": source.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        "operator_confirms_source_execution_v2_digest": source.source.source.SOURCE_EXECUTION_V2_DIGEST,
        "operator_confirms_source_module_grouping_digest": source.source.source.SOURCE_MODULE_GROUPING_DIGEST,
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_after_v2_package": SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,
    }
    for k, v in expected.items():
        if a.get(k) != v: raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError(f"{k} mismatch")
    if not _iso_utc(a.get("operator_attestation_timestamp_utc")): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("timestamp invalid")
    if not isinstance(a.get("operator_reference"), str) or not a["operator_reference"].strip(): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("operator reference missing")
    for k in ATTESTATION_BOOLEAN_FIELDS:
        if a.get(k) is not True: raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError(f"{k} must be true")

def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_attestation_v1(
    *, operator_reference: str, operator_attestation_timestamp_utc: str, operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str, operator_confirms_source_after_v2_candidate_digest: str,
    operator_confirms_source_results_review_v2_digest: str, operator_confirms_source_review_manifest_digest: str,
    operator_confirms_source_execution_v2_digest: str, operator_confirms_source_module_grouping_digest: str,
    operator_confirms_retry_execution_commit: str, operator_confirms_retry_failure_counts: bool,
    operator_confirms_module_grouping_reviewed: bool, operator_confirms_module_count_29: bool,
    operator_confirms_largest_module_counts: bool, operator_confirms_unsupported_claims_boundary: bool,
    operator_confirms_selected_after_v2_package: str, operator_confirms_approval_scope_only: bool,
    operator_confirms_no_remediation_execution: bool, operator_confirms_no_diagnostic_execution: bool,
    operator_confirms_no_classification_execution: bool, operator_confirms_no_retry: bool,
    operator_confirms_no_full_pytest: bool, operator_confirms_no_retry_results_review: bool,
    operator_confirms_no_integration_results_review: bool, operator_confirms_no_integration_success: bool,
    operator_confirms_no_successful_integration_digest: bool, operator_confirms_no_integration_branch_push: bool,
    operator_confirms_no_main_push: bool, operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_branch_delete: bool, operator_confirms_no_force_push: bool,
    operator_confirms_no_tag_mutation: bool, operator_confirms_no_evidence_regeneration: bool,
    operator_confirms_no_marketflow_commit: bool, operator_confirms_no_pytest_cache_commit: bool,
    operator_confirms_no_provider_requests: bool, operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool, operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool, operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool, operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool, operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool, operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_remediation_or_method_after_v2_package: str = SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    record = dict(locals())
    record["operator_attestation_version"] = OPERATOR_ATTESTATION_VERSION
    _validate_attestation(record)
    return record

def _source_fields() -> dict[str, Any]:
    c = source._committed_source_fields()
    return {
        "source_after_v2_operator_review_artifact_kind": source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        "source_after_v2_operator_review_status": source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY,
        "source_after_v2_operator_review_scope": source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "source_after_v2_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_after_v2_candidate_digest": source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "source_results_review_v2_digest": source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_review_manifest_digest": source.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        "source_execution_v2_digest": source.source.source.SOURCE_EXECUTION_V2_DIGEST,
        "source_module_grouping_digest": source.source.source.SOURCE_MODULE_GROUPING_DIGEST,
        "source_digest_manifest_digest": source.source.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        "source_approval_v2_digest": source.source.source.source.SOURCE_APPROVAL_V2_DIGEST,
        "source_staged_inventory_digest": c["source_staged_inventory_digest"],
        **{k: deepcopy(c[k]) for k in ("retry_execution_branch", "retry_execution_commit", "retry_pytest_passed_count", "retry_pytest_failed_count", "retry_pytest_error_count", "retry_pytest_skipped_count", "retry_pytest_first_result_authoritative", "root_full_regression_is_retry_evidence", "failed_or_errored_nodeids_count", "module_level_grouping_reviewed", "module_summary_module_count", "largest_module_nodeid_counts", "failure_modules_classified", "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified", "first_error_identified", "first_order_claim_made", "traceback_root_cause_claimed", "retry_success_claimed", "main_merge_readiness_claimed", "origin_main_commit", "integration_branch_name", "integration_branch_head_commit", "remote_integration_branch_exists", "detached_integration_worktree_path", "detached_integration_worktree_head_commit", "staged_evidence_manifest_digest", "marketflow_outputs_tracked_in_repository", "pytest_cache_tracked_in_repository")},
    }

def _base(a: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        "schema_version": SCHEMA_VERSION, "approval_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW,
        "approval_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_remediation_or_method_after_v2_package": SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,
        "created_offline": True, "governance_only": True, "operator_attestation_required": True,
        **_source_fields(), "operator_attestation": deepcopy(dict(a)), "unsupported_claims_boundary": source._unsupported_claims_boundary(),
        "selected_package": {"package_id": SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE, "approval_status": APPROVED_ONLY, "selected": True, "approved": True, "authorized_for_future_execution": True, "executed": False},
        "approved_future_requirements": deepcopy(APPROVED_FUTURE_REQUIREMENTS), "approved_future_plan": deepcopy(APPROVED_FUTURE_PLAN),
        "authorized_planned_outputs": deepcopy(AUTHORIZED_PLANNED_OUTPUTS), "supporting_packages": deepcopy(SUPPORTING_PACKAGES), "blocked_packages": deepcopy(BLOCKED_PACKAGES),
        "remediation_or_method_after_v2_selected": True, "remediation_or_method_after_v2_approved": True,
        "remediation_or_method_after_v2_authorized": True, "remediation_or_method_after_v2_approval_created": True,
        "ready_for_remediation_or_method_after_v2_execution": True, "remediation_or_method_after_v2_executed": False,
        "diagnostic_method_after_v2_executed": False, "code_remediation_after_v2_executed": False, "evidence_remediation_after_v2_executed": False,
        "new_retry_candidate_created": False, "new_retry_executed": False, "new_retry_results_review_created": False,
        "main_merge_approval_created": False, "retry_rerun_performed": False, "full_pytest_performed": False,
        "diagnostic_command_executed": False, "diagnostic_output_captured": False, "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False, "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False, "main_push_performed": False, "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False, "pytest_cache_committed": False, "evidence_regenerated": False,
        "provider_requests_made_in_approval": False, "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False, "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False, "strategy_scoring_performed": False, "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_accepted": False, "profitability": NOT_ACCEPTED,
        "profitability_accepted": False, "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED, "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS), "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }

def _check(i: str, e: Any, a: Any) -> dict[str, Any]:
    s = PASS if e == a else FAIL
    return {"check_id": i, "status": s, "expected": deepcopy(e), "actual": deepcopy(a), "severity": BLOCKER, "message": f"{i} {'passed' if s == PASS else 'failed'}"}

def _checklist(x: Mapping[str, Any]) -> list[dict[str, Any]]:
    a=x.get("operator_attestation", {}); vals={
        "source_operator_review_digest_bound": (SOURCE_OPERATOR_REVIEW_DIGEST,x.get("source_after_v2_operator_review_digest")), "source_after_v2_candidate_digest_bound": (source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,x.get("source_after_v2_candidate_digest")),
        "source_results_review_v2_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,x.get("source_results_review_v2_digest")), "source_review_manifest_digest_bound": (source.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,x.get("source_review_manifest_digest")),
        "source_execution_v2_digest_bound": (source.source.source.SOURCE_EXECUTION_V2_DIGEST,x.get("source_execution_v2_digest")), "source_module_grouping_digest_bound": (source.source.source.SOURCE_MODULE_GROUPING_DIGEST,x.get("source_module_grouping_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34",x.get("retry_execution_commit")), "retry_failure_counts_bound": ([24877,1292,112,7],[x.get(f"retry_pytest_{n}_count") for n in ("passed","failed","error","skipped")]),
        "module_grouping_reviewed_bound": (True,x.get("module_level_grouping_reviewed")), "module_count_29_bound": (29,x.get("module_summary_module_count")), "largest_module_counts_bound": ([136,131,122,112,111],x.get("largest_module_nodeid_counts")), "unsupported_claims_bound": (source._unsupported_claims_boundary(),x.get("unsupported_claims_boundary")),
        "operator_decision_matches": (OPERATOR_DECISION,a.get("operator_decision")), "operator_attestation_phrase_matches": (REQUIRED_OPERATOR_ATTESTATION_PHRASE,a.get("operator_attestation_phrase")), "approval_scope_only": (True,a.get("operator_confirms_approval_scope_only")), "selected_package_prioritize_largest_modules": (SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,x.get("selected_remediation_or_method_after_v2_package")),
        "approval_created_true": (True,x.get("remediation_or_method_after_v2_approval_created")), "method_selected_true": (True,x.get("remediation_or_method_after_v2_selected")), "method_approved_true": (True,x.get("remediation_or_method_after_v2_approved")), "method_authorized_true": (True,x.get("remediation_or_method_after_v2_authorized")), "ready_for_execution_true": (True,x.get("ready_for_remediation_or_method_after_v2_execution")),
    }
    false_map={"method_executed_false":"remediation_or_method_after_v2_executed","diagnostic_method_executed_false":"diagnostic_method_after_v2_executed","code_remediation_executed_false":"code_remediation_after_v2_executed","evidence_remediation_executed_false":"evidence_remediation_after_v2_executed","new_retry_candidate_created_false":"new_retry_candidate_created","new_retry_executed_false":"new_retry_executed","new_retry_results_review_created_false":"new_retry_results_review_created","main_merge_approval_created_false":"main_merge_approval_created","retry_rerun_false":"retry_rerun_performed","full_pytest_false":"full_pytest_performed","diagnostic_command_false":"diagnostic_command_executed","diagnostic_output_false":"diagnostic_output_captured","integration_success_false":"integration_execution_successful","integration_branch_pushed_false":"integration_branch_pushed","main_push_false":"main_push_performed","origin_main_modified_false":"origin_main_modified_by_this_task","marketflow_outputs_committed_false":"marketflow_outputs_committed","pytest_cache_committed_false":"pytest_cache_committed","evidence_regenerated_false":"evidence_regenerated","provider_requests_false":"provider_requests_made_in_approval","market_data_acquisition_false":"market_data_acquisition_performed_in_approval","dataset_generation_false":"dataset_generation_performed_in_approval","metric_recomputation_false":"metric_recomputation_from_raw_rows_performed","model_training_false":"model_training_performed","strategy_scoring_false":"strategy_scoring_performed","recommendations_false":"trade_recommendations_generated"}
    vals.update({k:(False,x.get(v)) for k,v in false_map.items()}); vals.update({
        "successful_integration_digest_false":([False,False],[x.get("successful_integration_execution_digest_generated"),x.get("successful_integration_validation_digest_generated")]), "predictive_usefulness_not_accepted":(NOT_ACCEPTED,x.get("predictive_usefulness")), "profitability_not_accepted":(NOT_ACCEPTED,x.get("profitability")), "runtime_not_authorized":(NOT_AUTHORIZED,x.get("runtime_use")), "broker_not_authorized":(NOT_AUTHORIZED,x.get("broker_execution")),
        "requirements_approved_for_future_execution":(APPROVED_FUTURE_REQUIREMENTS,x.get("approved_future_requirements")), "future_plan_approved_not_executed":(APPROVED_FUTURE_PLAN,x.get("approved_future_plan")), "planned_outputs_authorized_not_generated":(AUTHORIZED_PLANNED_OUTPUTS,x.get("authorized_planned_outputs")), "supporting_packages_not_selected":(SUPPORTING_PACKAGES,x.get("supporting_packages")), "blocked_packages_not_approved":(BLOCKED_PACKAGES,x.get("blocked_packages")), "next_chain_defined":(NEXT_CHAIN,x.get("next_chain")), "next_gates_defined":(NEXT_GATES,x.get("next_gates")), "risk_controls_defined":(RISK_CONTROLS,x.get("risk_controls")), "no_tracked_marketflow_files":(False,x.get("marketflow_outputs_tracked_in_repository")), "no_tracked_pytest_cache_files":(False,x.get("pytest_cache_tracked_in_repository"))})
    return [_check(i,*vals[i]) for i in CHECK_IDS]

def _summary(x: Mapping[str,Any], c:list[dict[str,Any]]) -> dict[str,Any]:
    f=[r for r in c if r["status"]!=PASS]; return {"total_checks":len(c),"passed_checks":len(c)-len(f),"failed_checks":len(f),"blocker_count":sum(r["severity"]==BLOCKER for r in f),"remediation_or_method_after_v2_selected":True,"remediation_or_method_after_v2_approved":True,"remediation_or_method_after_v2_authorized":True,"remediation_or_method_after_v2_approval_created":True,"selected_remediation_or_method_after_v2_package":SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,"ready_for_remediation_or_method_after_v2_execution":True,"method_executed":False,"new_retry_candidate_created":False,"new_retry_executed":False,"integration_execution_successful":False,"recommended_next_task":RECOMMENDED_NEXT_TASK,"predictive_usefulness_accepted":False,"profitability_accepted":False,"runtime_authorized":False,"broker_execution_authorized":False}

def marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest_v1(x: Mapping[str,Any])->str:
    p=deepcopy(dict(x)); [p.pop(k,None) for k in ("checklist","summary","marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest")]; return semantic_digest(p)

def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(*, source_review:dict|None=None, operator_attestation:dict)->dict:
    _validate_attestation(operator_attestation)
    if source_review is not None: source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(source_review)
    x=_base(operator_attestation); x["checklist"]=_checklist(x); x["summary"]=_summary(x,x["checklist"]); x["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest"]=marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest_v1(x); validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(x); return x

def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(x:dict)->dict:
    if not isinstance(x,dict): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("approval must be object")
    _validate_attestation(x.get("operator_attestation",{})); expected=_base(x["operator_attestation"])
    for k,v in expected.items():
        if x.get(k)!=v: raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError(f"{k} mismatch")
    c=x.get("checklist");
    if not isinstance(c,list) or c!=_checklist(x) or any(r["status"]!=PASS for r in c): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("checklist invalid")
    if x.get("summary")!=_summary(x,c): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("summary mismatch")
    d=x.get("marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest")
    if not isinstance(d,str) or not re.fullmatch(r"[0-9a-f]{64}",d) or d!=marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest_v1(x): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("digest invalid")
    return {"artifact_kind":x["artifact_kind"],"approval_status":x["approval_status"],"approval_scope":x["approval_scope"],"marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest":d,**{k:x["summary"][k] for k in ("total_checks","passed_checks","failed_checks","blocker_count")}}

def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_markdown_v1(x:dict)->str:
    v=validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(x); sections=[("Operator Attestation",[f"Decision: `{OPERATOR_DECISION}`."]), ("Source Operator Review",[f"Digest: `{SOURCE_OPERATOR_REVIEW_DIGEST}`."]), ("Source After-v2 Candidate",[f"Digest: `{source.SOURCE_AFTER_V2_CANDIDATE_DIGEST}`."]), ("Source Results Review v2",[f"Digest: `{source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST}`."]), ("Retry Failure Context",["`24877 passed, 1292 failed, 112 errors, 7 skipped`; root regression is not retry evidence."]), ("Approval Scope",["Future planning execution only; no execution occurs here."]), ("Selected Package",[f"`{SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE}`."]), ("Approved Future Requirements",[r["requirement_id"] for r in APPROVED_FUTURE_REQUIREMENTS]), ("Approved Future Plan",[r["source_step"] for r in APPROVED_FUTURE_PLAN]), ("Planned Outputs",[r["output_id"] for r in AUTHORIZED_PLANNED_OUTPUTS]), ("Supporting Packages",[r["package_id"] for r in SUPPORTING_PACKAGES]), ("Blocked Packages",[r["package_id"] for r in BLOCKED_PACKAGES]), ("Next Chain",NEXT_CHAIN), ("Next Gates",NEXT_GATES), ("Risk Controls",RISK_CONTROLS), ("Authority Boundaries",["Execution, retry, main merge, runtime, and trading remain closed."]), ("Checklist Summary",[f"`{v['passed_checks']}/{v['total_checks']}` pass."]), ("Guardrails",["Separate execution and results review are required."])]
    lines=["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Approval After Classification v2 Review v1",""]
    for h,rows in sections: lines += [f"## {h}",*[f"- {r}" for r in rows],""]
    return "\n".join(lines)

def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(output_dir:str|Path,*,source_review:dict|None=None,operator_attestation:dict)->dict:
    x=build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(source_review=source_review,operator_attestation=operator_attestation); p=Path(output_dir)/"marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1.json"; p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError("output exists")
    b=canonical_json_bytes(x); p.write_bytes(b); return {"path":str(p),"artifact_kind":x["artifact_kind"],"approval_status":x["approval_status"],"approval_scope":x["approval_scope"],"marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest":x["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest"],"payload_sha256":sha256_bytes(b)}
