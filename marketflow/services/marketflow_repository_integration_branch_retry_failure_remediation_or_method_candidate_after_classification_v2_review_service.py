"""Propose candidate-only follow-up packages after classification review v2."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_service
    as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1 = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)
SOURCE_RESULTS_REVIEW_V2_DIGEST = "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86"
SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST = "6a7c4796c188e082d4433d86f93244f8a3fe2f985302a0a52c6a4843feef01a3"
RECOMMENDED_PACKAGE = "PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING"
RECOMMENDATION_STATUS = "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

CANDIDATE_AFTER_V2_PHILOSOPHY = (
    "The reviewed v2 classification provides module-level failure concentration evidence, not root cause. "
    "The next safe step is to select a remediation or diagnostic method that uses the module grouping to "
    "prioritize investigation without unsupported claims."
)
CANDIDATE_AFTER_V2_BOUNDARY = (
    "Candidate-only; no remediation, diagnostic execution, classification execution, retry, results review, "
    "main merge, or runtime authority is created by this artifact."
)
CANDIDATE_AFTER_V2_GOAL = (
    "Define safe next packages to use the reviewed 1,404-node / 29-module classification result for prioritized "
    "remediation planning, diagnostic-output capture, evidence-root review, path/CWD review, digest-drift review, "
    "or fixture-isolation review."
)
RECOMMENDATION_REASON = (
    "The reviewed classification result identifies 29 module groups and concentrated top modules, but it lacks "
    "failure/error separation and traceback root cause. A prioritization/planning package is safer than direct "
    "remediation or retry."
)

PROPOSED_PACKAGES = [
    {
        "package_id": RECOMMENDED_PACKAGE,
        "status": RECOMMENDATION_STATUS,
        "purpose": (
            "Use the reviewed 29-module grouping and largest-module concentration to prioritize a bounded "
            "diagnostic/remediation planning pass for the highest-count modules."
        ),
        "recommended_for": (
            "The v2 classification identifies concentration by module but not root cause. Prioritizing largest "
            "modules is the safest next planning step."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED_HIGH_CONTROL",
        "purpose": (
            "Prepare a separately approved diagnostic-output capture focused on the top module groups to obtain "
            "tracebacks and separate failures from errors."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_EVIDENCE_ROOT_REQUIREMENT_REVIEW_FOR_CLASSIFIED_MODULES",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Use module names and known source history to identify candidate missing ignored evidence roots or "
            "fixture artifacts required by grouped test modules."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_PATH_CWD_ASSUMPTION_REVIEW_FOR_CLASSIFIED_MODULES",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Identify modules likely sensitive to root path, detached worktree path, cwd, absolute path, or "
            "repository-root discovery assumptions."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_DIGEST_CONSTANT_DRIFT_REVIEW_FOR_CLASSIFIED_MODULES",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Identify modules likely failing because digest constants or historical artifact expectations changed "
            "across the integration stack."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_TEST_FIXTURE_ISOLATION_REVIEW_FOR_CLASSIFIED_MODULES",
        "status": "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "purpose": (
            "Identify modules likely affected by fixture isolation, cache/state assumptions, import ordering, or "
            "environment setup differences."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_MODULE_NAMES_ONLY",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Apply code changes based only on module grouping.",
        "blocked_reason": (
            "Module grouping alone does not provide traceback-based root cause or enough evidence for direct code "
            "remediation."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_OR_DIAGNOSTIC_ACTION",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Create a new retry candidate immediately after classification review.",
        "blocked_reason": (
            "The prior retry failed and module-level classification did not identify or fix root causes. New retry "
            "requires separate remediation/diagnostic path first."
        ),
        "selected": False,
        "approved": False,
        "executed": False,
    },
    {
        "package_id": "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY_AND_MODULE_CLASSIFICATION",
        "status": "BLOCKED_NOT_ALLOWED",
        "purpose": "Proceed to main merge despite failed retry and unresolved module-level classification.",
        "blocked_reason": "Main merge approval remains blocked until a future retry results review passes.",
        "selected": False,
        "approved": False,
        "executed": False,
    },
]

FUTURE_REQUIREMENTS = {
    "source_classification_results_review_v2_must_be_ready": True,
    "module_grouping_digest_must_be_bound": True,
    "module_summary_must_be_bound": True,
    "limitations_must_be_preserved": True,
    "method_must_not_claim_failure_error_separation": True,
    "method_must_not_claim_first_failure": True,
    "method_must_not_claim_traceback_root_cause": True,
    "method_must_not_treat_classification_as_retry_success": True,
    "method_must_prioritize_modules_without_code_change": True,
    "diagnostic_or_remediation_execution_requires_separate_approval": True,
    "new_retry_requires_separate_approval": True,
    "main_merge_requires_passing_retry_results_review": True,
}
FUTURE_PLAN_STEPS = [
    "Bind Classification Method Results Review v2 digest and module-grouping digest.",
    "Use reviewed module grouping only as prioritization evidence.",
    "Identify largest module groups and cumulative concentration.",
    (
        "Define candidate diagnostic/remediation planning buckets: top-module diagnostic-output capture; missing "
        "evidence-root review; path/cwd assumption review; digest constant drift review; fixture isolation review."
    ),
    (
        "Preserve unsupported-claims boundary: no failure/error separation; no traceback root cause; no first-order "
        "claim."
    ),
    "Recommend one next package after operator review.",
    "Keep new retry candidate, main merge, runtime, and trading closed.",
]
PLANNED_OUTPUTS = {
    name: "PLANNED_NOT_GENERATED"
    for name in (
        "after_v2_candidate_manifest",
        "prioritized_module_group_summary",
        "top_module_concentration_report",
        "diagnostic_capture_candidate_report",
        "evidence_root_review_candidate_report",
        "path_cwd_review_candidate_report",
        "digest_drift_review_candidate_report",
        "fixture_isolation_review_candidate_report",
        "unsupported_claims_boundary_report",
        "recommended_next_package_report",
        "digest_manifest",
    )
}
NON_GOALS = [
    "do_not_execute_remediation_now",
    "do_not_execute_diagnostics_now",
    "do_not_execute_classification_now",
    "do_not_read_cache_now",
    "do_not_run_retry_now",
    "do_not_run_full_pytest_now",
    "do_not_create_new_retry_candidate_now",
    "do_not_create_retry_results_review",
    "do_not_create_integration_results_review",
    "do_not_mark_integration_successful",
    "do_not_claim_failure_error_separation",
    "do_not_claim_first_failure",
    "do_not_claim_traceback_root_cause",
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
    "Remediation or Method Candidate After Classification v2 Review Operator Review.",
    "Remediation or Method Approval, if selected.",
    "Remediation or Method Execution, if approved.",
    "Remediation or Method Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = [
    "remediation_or_method_candidate_after_v2_review_operator_review",
    "remediation_or_method_approval_if_selected",
    "remediation_or_method_execution_if_approved",
    "remediation_or_method_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
RISK_CONTROLS = [
    "candidate_after_v2_does_not_execute_remediation",
    "candidate_after_v2_does_not_execute_diagnostics",
    "candidate_after_v2_does_not_execute_classification",
    "candidate_after_v2_does_not_read_cache",
    "candidate_after_v2_does_not_run_retry",
    "candidate_after_v2_does_not_run_full_pytest",
    "candidate_after_v2_does_not_create_new_retry_candidate",
    "candidate_after_v2_does_not_create_retry_results_review",
    "candidate_after_v2_does_not_create_integration_results_review",
    "candidate_after_v2_does_not_mark_integration_successful",
    "candidate_after_v2_does_not_generate_successful_integration_digest",
    "candidate_after_v2_does_not_claim_failure_error_separation",
    "candidate_after_v2_does_not_claim_first_failure",
    "candidate_after_v2_does_not_claim_traceback_root_cause",
    "candidate_after_v2_does_not_treat_classification_as_retry_success",
    "candidate_after_v2_does_not_push_integration_branch",
    "candidate_after_v2_does_not_push_main",
    "candidate_after_v2_does_not_delete_integration_branch",
    "candidate_after_v2_does_not_delete_worktree",
    "candidate_after_v2_does_not_force_push",
    "candidate_after_v2_does_not_prune_remotes",
    "candidate_after_v2_does_not_modify_tags",
    "candidate_after_v2_does_not_commit_marketflow_outputs",
    "candidate_after_v2_does_not_commit_pytest_cache",
    "candidate_after_v2_does_not_modify_staged_evidence",
    "candidate_after_v2_does_not_regenerate_evidence",
    "candidate_after_v2_does_not_call_providers",
    "candidate_after_v2_does_not_acquire_market_data",
    "candidate_after_v2_does_not_regenerate_dataset",
    "candidate_after_v2_does_not_recompute_metrics",
    "candidate_after_v2_does_not_train_models",
    "candidate_after_v2_does_not_score_strategy",
    "candidate_after_v2_does_not_generate_recommendations",
    "candidate_after_v2_does_not_accept_predictive_usefulness",
    "candidate_after_v2_does_not_accept_profitability",
    "candidate_after_v2_does_not_authorize_runtime",
    "candidate_after_v2_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_operator_review_required",
    "separate_approval_required_before_execution",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
CHECK_IDS = [
    "source_results_review_v2_digest_bound",
    "source_review_manifest_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "source_digest_manifest_bound",
    "source_approval_v2_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "module_grouping_reviewed_bound",
    "module_count_29_bound",
    "largest_module_counts_bound",
    "unsupported_claims_bound",
    "candidate_created_true",
    "candidate_ready_true",
    "recommended_package_present",
    "packages_present_9",
    "blocked_packages_present_3",
    "recommended_package_not_selected",
    "method_selected_false",
    "method_approved_false",
    "method_executed_false",
    "diagnostic_method_executed_false",
    "code_remediation_executed_false",
    "evidence_remediation_executed_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
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


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
    ValueError
):
    """Raised when candidate evidence or a closed boundary is invalid."""


def _committed_source_fields() -> dict[str, Any]:
    fields = source._committed_source_fields()
    source_candidate_created = fields.pop(
        "remediation_or_method_candidate_after_v2_review_created", False
    )
    return {
        "source_classification_method_results_review_v2_artifact_kind": (
            source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2
        ),
        "source_classification_method_results_review_v2_status": (
            source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_READY
        ),
        "source_classification_method_results_review_v2_scope": (
            source.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_RESULTS_REVIEW_V2_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN
        ),
        "source_classification_method_results_review_v2_digest": SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "source_classification_method_results_review_v2_manifest_digest": SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        **fields,
        "module_level_grouping_reviewed": True,
        "module_summary_reviewed": True,
        "largest_module_summary_reviewed": True,
        "limitations_reviewed": True,
        "unsupported_claims_exclusion_reviewed": True,
        "planned_outputs_reviewed": True,
        "source_classification_method_results_review_v2_created": True,
        "source_classification_method_results_review_v2_ready": True,
        "ready_for_remediation_or_method_candidate_after_v2_review": True,
        "source_remediation_or_method_candidate_after_v2_review_created": source_candidate_created,
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "detached_integration_worktree_clean_at_candidate": True,
    }


def _source_fields(source_results_review: dict | None) -> dict[str, Any]:
    if source_results_review is None:
        return _committed_source_fields()
    source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
        source_results_review
    )
    fields = _committed_source_fields()
    mapping = {
        "source_classification_method_results_review_v2_artifact_kind": "artifact_kind",
        "source_classification_method_results_review_v2_status": "review_status",
        "source_classification_method_results_review_v2_scope": "review_scope",
        "source_classification_method_results_review_v2_digest": (
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"
        ),
        "source_classification_method_results_review_v2_manifest_digest": (
            "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_manifest_digest"
        ),
    }
    for target, source_field in mapping.items():
        fields[target] = deepcopy(source_results_review.get(source_field))
    for field in set(fields) - set(mapping):
        if field in source_results_review:
            fields[field] = deepcopy(source_results_review[field])
    return fields


def _unsupported_claims_boundary() -> dict[str, bool]:
    return {
        "failure_modules_classified": False,
        "error_modules_classified": False,
        "failure_error_separation_claimed": False,
        "first_failure_identified": False,
        "first_error_identified": False,
        "first_order_claim_made": False,
        "traceback_root_cause_claimed": False,
        "retry_success_claimed": False,
        "main_merge_readiness_claimed": False,
    }


def _classification_evidence_summary() -> dict[str, Any]:
    return {
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_used_for_module_level_only": True,
        "failed_or_errored_nodeids_count": 1404,
        "module_level_grouping_reviewed": True,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
        "limitations_reviewed": True,
        "unsupported_claims_exclusion_reviewed": True,
    }


def _base_candidate(source_fields: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        **deepcopy(dict(source_fields)),
        "classification_evidence_summary": _classification_evidence_summary(),
        "unsupported_claims_boundary": _unsupported_claims_boundary(),
        "candidate_after_v2_philosophy": CANDIDATE_AFTER_V2_PHILOSOPHY,
        "candidate_after_v2_boundary": CANDIDATE_AFTER_V2_BOUNDARY,
        "candidate_after_v2_goal": CANDIDATE_AFTER_V2_GOAL,
        "proposed_packages": deepcopy(PROPOSED_PACKAGES),
        "recommended_remediation_or_method_after_v2_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": RECOMMENDATION_REASON,
        "future_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_plan": {"status": "PLANNED_NOT_EXECUTED", "steps": list(FUTURE_PLAN_STEPS)},
        "future_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": deepcopy(PLANNED_OUTPUTS),
        "non_goals": list(NON_GOALS),
        "remediation_or_method_candidate_after_v2_review_created": True,
        "remediation_or_method_candidate_after_v2_review_ready_for_operator_review": True,
        "ready_for_remediation_or_method_candidate_after_v2_review_operator_review": True,
        "remediation_or_method_after_v2_selected": False,
        "remediation_or_method_after_v2_approved": False,
        "remediation_or_method_after_v2_authorized": False,
        "remediation_or_method_after_v2_executed": False,
        "diagnostic_method_after_v2_executed": False,
        "code_remediation_after_v2_executed": False,
        "evidence_remediation_after_v2_executed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "integration_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
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
    packages = candidate.get("proposed_packages")
    packages = packages if isinstance(packages, list) else []
    recommended = next((row for row in packages if row.get("package_id") == RECOMMENDED_PACKAGE), {})
    values = {
        "source_results_review_v2_digest_bound": (SOURCE_RESULTS_REVIEW_V2_DIGEST, candidate.get("source_classification_method_results_review_v2_digest")),
        "source_review_manifest_digest_bound": (SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST, candidate.get("source_classification_method_results_review_v2_manifest_digest")),
        "source_execution_v2_digest_bound": (source.SOURCE_EXECUTION_V2_DIGEST, candidate.get("source_classification_method_execution_v2_digest")),
        "source_module_grouping_digest_bound": (source.SOURCE_MODULE_GROUPING_DIGEST, candidate.get("source_classification_method_v2_module_grouping_digest")),
        "source_digest_manifest_bound": (source.SOURCE_DIGEST_MANIFEST_DIGEST, candidate.get("source_classification_method_v2_digest_manifest_digest")),
        "source_approval_v2_digest_bound": (source.source.SOURCE_APPROVAL_V2_DIGEST, candidate.get("source_classification_method_approval_v2_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", candidate.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [candidate.get(f"retry_pytest_{name}_count") for name in ("passed", "failed", "error", "skipped")]),
        "module_grouping_reviewed_bound": (True, candidate.get("module_level_grouping_reviewed")),
        "module_count_29_bound": (29, candidate.get("module_summary_module_count")),
        "largest_module_counts_bound": ([136, 131, 122, 112, 111], candidate.get("largest_module_nodeid_counts")),
        "unsupported_claims_bound": (_unsupported_claims_boundary(), candidate.get("unsupported_claims_boundary")),
        "candidate_created_true": (True, candidate.get("remediation_or_method_candidate_after_v2_review_created")),
        "candidate_ready_true": (True, candidate.get("remediation_or_method_candidate_after_v2_review_ready_for_operator_review")),
        "recommended_package_present": (RECOMMENDED_PACKAGE, candidate.get("recommended_remediation_or_method_after_v2_package")),
        "packages_present_9": (9, len(packages)),
        "blocked_packages_present_3": (3, sum(row.get("status") == "BLOCKED_NOT_ALLOWED" for row in packages)),
        "recommended_package_not_selected": (False, recommended.get("selected")),
        "method_selected_false": (False, candidate.get("remediation_or_method_after_v2_selected")),
        "method_approved_false": (False, candidate.get("remediation_or_method_after_v2_approved")),
        "method_executed_false": (False, candidate.get("remediation_or_method_after_v2_executed")),
        "diagnostic_method_executed_false": (False, candidate.get("diagnostic_method_after_v2_executed")),
        "code_remediation_executed_false": (False, candidate.get("code_remediation_after_v2_executed")),
        "evidence_remediation_executed_false": (False, candidate.get("evidence_remediation_after_v2_executed")),
        "new_retry_candidate_created_false": (False, candidate.get("new_retry_candidate_created")),
        "new_retry_executed_false": (False, candidate.get("new_retry_executed")),
        "new_retry_results_review_created_false": (False, candidate.get("new_retry_results_review_created")),
        "main_merge_approval_created_false": (False, candidate.get("main_merge_approval_created")),
        "retry_rerun_false": (False, candidate.get("retry_rerun_performed")),
        "full_pytest_false": (False, candidate.get("full_pytest_performed")),
        "diagnostic_command_false": (False, candidate.get("diagnostic_command_executed")),
        "diagnostic_output_false": (False, candidate.get("diagnostic_output_captured")),
        "integration_success_false": (False, candidate.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [candidate.get("successful_integration_execution_digest_generated"), candidate.get("successful_integration_validation_digest_generated")]),
        "integration_branch_pushed_false": (False, candidate.get("integration_branch_pushed")),
        "main_push_false": (False, candidate.get("main_push_performed")),
        "origin_main_modified_false": (False, candidate.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, candidate.get("marketflow_outputs_committed")),
        "pytest_cache_committed_false": (False, candidate.get("pytest_cache_committed")),
        "evidence_regenerated_false": (False, candidate.get("evidence_regenerated")),
        "provider_requests_false": (False, candidate.get("provider_requests_made_in_candidate")),
        "market_data_acquisition_false": (False, candidate.get("market_data_acquisition_performed_in_candidate")),
        "dataset_generation_false": (False, candidate.get("dataset_generation_performed_in_candidate")),
        "metric_recomputation_false": (False, candidate.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, candidate.get("model_training_performed")),
        "strategy_scoring_false": (False, candidate.get("strategy_scoring_performed")),
        "recommendations_false": (False, candidate.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
        "future_requirements_defined": (FUTURE_REQUIREMENTS, candidate.get("future_requirements")),
        "future_plan_defined": ({"status": "PLANNED_NOT_EXECUTED", "steps": FUTURE_PLAN_STEPS}, candidate.get("future_plan")),
        "planned_outputs_defined": (PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        "non_goals_defined": (NON_GOALS, candidate.get("non_goals")),
        "next_chain_defined": (NEXT_CHAIN, candidate.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, candidate.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "no_tracked_marketflow_files": ([False, False], [candidate.get("marketflow_outputs_tracked_in_repository"), candidate.get("marketflow_outputs_tracked_in_detached_worktree")]),
        "no_tracked_pytest_cache_files": ([False, False], [candidate.get("pytest_cache_tracked_in_repository"), candidate.get("pytest_cache_tracked_in_detached_worktree")]),
    }
    return [_check(check_id, *values[check_id]) for check_id in CHECK_IDS]


def _summary(candidate: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "remediation_or_method_candidate_after_v2_review_created": True,
        "remediation_or_method_candidate_after_v2_review_ready_for_operator_review": True,
        "recommended_remediation_or_method_after_v2_package": RECOMMENDED_PACKAGE,
        "method_selected": False,
        "method_approved": False,
        "method_executed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(candidate))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
    *, source_results_review: dict | None = None,
) -> dict:
    """Build the deterministic candidate without cache or execution access."""
    candidate = _base_candidate(_source_fields(source_results_review))
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate, candidate["checklist"])
    candidate[
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest"
    ] = marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest_v1(
        candidate
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        candidate
    )
    return candidate


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
    candidate: dict,
) -> dict:
    """Validate source bindings, proposal contents, and every closed boundary."""
    if not isinstance(candidate, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            "candidate must be an object"
        )
    static = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        "candidate_status": MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW,
        "candidate_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        **_committed_source_fields(),
        "classification_evidence_summary": _classification_evidence_summary(),
        "unsupported_claims_boundary": _unsupported_claims_boundary(),
        "candidate_after_v2_philosophy": CANDIDATE_AFTER_V2_PHILOSOPHY,
        "candidate_after_v2_boundary": CANDIDATE_AFTER_V2_BOUNDARY,
        "candidate_after_v2_goal": CANDIDATE_AFTER_V2_GOAL,
        "proposed_packages": PROPOSED_PACKAGES,
        "recommended_remediation_or_method_after_v2_package": RECOMMENDED_PACKAGE,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommendation_reason": RECOMMENDATION_REASON,
        "future_requirements": FUTURE_REQUIREMENTS,
        "future_plan": {"status": "PLANNED_NOT_EXECUTED", "steps": FUTURE_PLAN_STEPS},
        "future_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": PLANNED_OUTPUTS,
        "non_goals": NON_GOALS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
    for field, expected in static.items():
        _expect(candidate.get(field), expected, field)
    required_true = (
        "created_offline",
        "governance_only",
        "candidate_only",
        "remediation_or_method_candidate_after_v2_review_created",
        "remediation_or_method_candidate_after_v2_review_ready_for_operator_review",
        "ready_for_remediation_or_method_candidate_after_v2_review_operator_review",
    )
    required_false = (
        "remediation_or_method_after_v2_selected",
        "remediation_or_method_after_v2_approved",
        "remediation_or_method_after_v2_authorized",
        "remediation_or_method_after_v2_executed",
        "diagnostic_method_after_v2_executed",
        "code_remediation_after_v2_executed",
        "evidence_remediation_after_v2_executed",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
        "marketflow_outputs_tracked_in_repository",
        "marketflow_outputs_tracked_in_detached_worktree",
        "pytest_cache_tracked_in_repository",
        "pytest_cache_tracked_in_detached_worktree",
    )
    for field in required_true:
        _expect(candidate.get(field), True, field)
    for field in required_false:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    checklist = candidate.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            "checklist missing"
        )
    _expect([row.get("check_id") for row in checklist], CHECK_IDS, "checklist ids")
    _expect(checklist, _checklist(candidate), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            "checklist failed"
        )
    _expect(candidate.get("summary"), _summary(candidate, checklist), "summary")
    digest = candidate.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            "candidate digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest_v1(
            candidate
        ),
        "candidate digest",
    )
    return {
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest": digest,
        **{
            key: candidate["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_markdown_v1(
    candidate: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        candidate
    )
    sections = [
        (
            "Source Results Review v2",
            [
                f"Results-review digest: `{SOURCE_RESULTS_REVIEW_V2_DIGEST}`.",
                f"Review-manifest digest: `{SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST}`.",
            ],
        ),
        (
            "Retry Failure Context",
            [
                "Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.",
                "The passing root regression is not retry evidence.",
            ],
        ),
        (
            "Classification Evidence Summary",
            ["The reviewed 1,404 node IDs form 29 module groups; largest counts are `136, 131, 122, 112, 111`."],
        ),
        ("Candidate Scope", [candidate["candidate_after_v2_boundary"]]),
        ("Candidate Philosophy", [candidate["candidate_after_v2_philosophy"], candidate["candidate_after_v2_goal"]]),
        (
            "Proposed Packages",
            [f"`{row['package_id']}` — `{row['status']}`" for row in candidate["proposed_packages"]],
        ),
        (
            "Recommended Package",
            [f"`{RECOMMENDED_PACKAGE}` — `{RECOMMENDATION_STATUS}`.", RECOMMENDATION_REASON],
        ),
        ("Future Requirements", [f"`{key}`: `{value}`" for key, value in candidate["future_requirements"].items()]),
        ("Future Plan", candidate["future_plan"]["steps"]),
        ("Planned Outputs", [f"`{key}`: `{value}`" for key, value in candidate["planned_outputs"].items()]),
        ("Non-Goals", [f"`{row}`" for row in candidate["non_goals"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", [f"`{row}`" for row in candidate["next_gates"]]),
        ("Risk Controls", [f"`{row}`" for row in candidate["risk_controls"]]),
        (
            "Authority Boundaries",
            ["No package is selected, approved, authorized, or executed; retry, main merge, runtime, and trading remain closed."],
        ),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / "
                f"{validation['failed_checks']} / {validation['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            [
                "Module grouping is prioritization evidence, not root-cause evidence.",
                "Operator review and a separate approval are required before any execution.",
            ],
        ),
    ]
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Classification v2 Review v1",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
    output_dir: str | Path,
    *,
    source_results_review: dict | None = None,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        source_results_review=source_results_review
    )
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_"
        "after_classification_v2_review_v1.json"
    )
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError(
            "candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest": validation[
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
