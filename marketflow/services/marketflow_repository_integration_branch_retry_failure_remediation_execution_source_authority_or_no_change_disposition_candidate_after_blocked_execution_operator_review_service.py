"""Review candidate-only paths after the blocked remediation execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest"
SOURCE_CANDIDATE_COMMIT = "43a39a37636792dd8756cf45561a012d8dd7c275"
SOURCE_CANDIDATE_DIGEST = "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_V1_IF_SELECTED"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION = source.PACKAGE_CREATE_SOURCE_AUTHORITY_ENRICHMENT_PLAN_FOR_BLOCKED_REMEDIATION
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE = source.PACKAGE_CREATE_NO_CHANGE_DISPOSITION_REVIEW_FOR_CURRENT_ROOT_PRIORITY1_PASSING_STATE
PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES = source.PACKAGE_REQUEST_ALTERNATE_BOUNDED_DIAGNOSTIC_CAPTURE_FOR_DETACHED_RETRY_FAILURES
PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT = source.PACKAGE_COMPARE_CURRENT_ROOT_PRIORITY1_PASSING_STATE_TO_DETACHED_RETRY_CONTEXT
PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY = source.PACKAGE_CREATE_NO_CHANGE_RETRY_CANDIDATE_CRITERIA_ONLY
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY = source.PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_EXTERNAL_SOURCE_AUTHORITY
PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY = source.PACKAGE_DIRECT_REMEDIATION_DESPITE_NO_SOURCE_AUTHORITY
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE = source.PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_TO_MATCH_CURRENT_ROOT_PASSING_STATE
PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY = source.PACKAGE_REWRITE_TESTS_OR_SKIP_FAILURES_WITHOUT_SOURCE_AUTHORITY
PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES = source.PACKAGE_NEW_RETRY_BECAUSE_PRIORITY1_CURRENT_ROOT_PASSES
PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED = source.PACKAGE_MAIN_MERGE_BECAUSE_CURRENT_ROOT_REGRESSION_PREVIOUSLY_PASSED
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = source.PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY

REVIEWED_CANDIDATE_PHILOSOPHY = (
    "The blocked remediation execution and its diagnosis show that the reviewed plan and four workstreams provide "
    "planning structure but not concrete change authority. Priority 1 focused validation passes in the current root "
    "context, while the detached retry remains failed and authoritative. The candidate correctly defines future "
    "governed paths: source-authority enrichment, no-change disposition, alternate bounded diagnostics, context "
    "comparison, no-change retry criteria, or hold disposition. This operator review does not select, approve, "
    "authorize, or execute any path."
)
REVIEWED_CANDIDATE_BOUNDARY = "Operator-review only; no package selection, approval, execution, source-authority enrichment, no-change disposition, alternate diagnostics, remediation, code change, test change, digest update, patch generation, pytest, retry, main merge, provider request, runtime, broker, or trading authority is created."
REVIEWED_CANDIDATE_GOAL = "Review safe future paths after a blocked controlled remediation execution where no source-authority-bound change was identified."

NEXT_CHAIN = (
    "Source Authority or No-Change Disposition Approval After Blocked Execution v1, if selected.",
    "Source Authority or No-Change Disposition Execution v1, if approved.",
    "Source Authority or No-Change Disposition Results Review v1.",
    "Conditional remediation execution candidate, alternate diagnostic candidate, no-change retry candidate, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after a reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple(
    """source_authority_or_no_change_disposition_approval_after_blocked_execution_if_selected
source_authority_or_no_change_disposition_execution_if_approved
source_authority_or_no_change_disposition_results_review
conditional_follow_on_candidate_if_results_review_supports
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)

RISK_CONTROLS = tuple(
    """operator_review_after_blocked_execution_does_not_select_package
operator_review_after_blocked_execution_does_not_approve_package
operator_review_after_blocked_execution_does_not_authorize_package
operator_review_after_blocked_execution_does_not_execute_source_authority_enrichment
operator_review_after_blocked_execution_does_not_execute_no_change_disposition
operator_review_after_blocked_execution_does_not_execute_alternate_diagnostics
operator_review_after_blocked_execution_does_not_execute_remediation
operator_review_after_blocked_execution_does_not_modify_production_code
operator_review_after_blocked_execution_does_not_modify_existing_tests
operator_review_after_blocked_execution_does_not_update_expected_digests
operator_review_after_blocked_execution_does_not_generate_patch
operator_review_after_blocked_execution_does_not_apply_patch
operator_review_after_blocked_execution_does_not_run_pytest
operator_review_after_blocked_execution_does_not_run_full_pytest
operator_review_after_blocked_execution_does_not_rerun_priority1_validation
operator_review_after_blocked_execution_does_not_rerun_retry
operator_review_after_blocked_execution_does_not_rerun_detached_retry
operator_review_after_blocked_execution_does_not_parse_durable_receipt
operator_review_after_blocked_execution_does_not_analyze_diagnostic_output
operator_review_after_blocked_execution_does_not_rerun_plan_execution
operator_review_after_blocked_execution_does_not_regenerate_targeted_plan
operator_review_after_blocked_execution_does_not_rerun_method_execution
operator_review_after_blocked_execution_does_not_rerun_controlled_recapture
operator_review_after_blocked_execution_does_not_run_diagnostic_command
operator_review_after_blocked_execution_does_not_read_pytest_cache
operator_review_after_blocked_execution_does_not_modify_pytest_cache
operator_review_after_blocked_execution_does_not_parse_terminal_logs
operator_review_after_blocked_execution_does_not_parse_operator_logs
operator_review_after_blocked_execution_does_not_inspect_env
operator_review_after_blocked_execution_does_not_reconstruct_prior_lost_values
operator_review_after_blocked_execution_does_not_reconstruct_full_streams
operator_review_after_blocked_execution_does_not_classify_modules_again
operator_review_after_blocked_execution_does_not_classify_full_retry_failures
operator_review_after_blocked_execution_does_not_classify_full_retry_errors
operator_review_after_blocked_execution_does_not_claim_failure_error_separation
operator_review_after_blocked_execution_does_not_identify_authoritative_first_failure
operator_review_after_blocked_execution_does_not_identify_authoritative_first_error
operator_review_after_blocked_execution_does_not_claim_traceback_root_cause
operator_review_after_blocked_execution_does_not_claim_root_cause
operator_review_after_blocked_execution_does_not_claim_retry_success
operator_review_after_blocked_execution_does_not_claim_main_merge_readiness
operator_review_after_blocked_execution_does_not_create_remediation_execution
operator_review_after_blocked_execution_does_not_create_remediation_execution_results_review
operator_review_after_blocked_execution_does_not_create_new_retry_candidate
operator_review_after_blocked_execution_does_not_create_retry_approval
operator_review_after_blocked_execution_does_not_create_retry_execution
operator_review_after_blocked_execution_does_not_create_retry_results_review
operator_review_after_blocked_execution_does_not_create_integration_results_review
operator_review_after_blocked_execution_does_not_mark_integration_successful
operator_review_after_blocked_execution_does_not_generate_successful_integration_digest
operator_review_after_blocked_execution_does_not_push_integration_branch
operator_review_after_blocked_execution_does_not_push_main
operator_review_after_blocked_execution_does_not_delete_integration_branch
operator_review_after_blocked_execution_does_not_delete_worktree
operator_review_after_blocked_execution_does_not_force_push
operator_review_after_blocked_execution_does_not_prune_remotes
operator_review_after_blocked_execution_does_not_modify_tags
operator_review_after_blocked_execution_does_not_modify_staged_evidence
operator_review_after_blocked_execution_does_not_regenerate_evidence
operator_review_after_blocked_execution_does_not_call_providers
operator_review_after_blocked_execution_does_not_acquire_market_data
operator_review_after_blocked_execution_does_not_generate_dataset
operator_review_after_blocked_execution_does_not_recompute_metrics
operator_review_after_blocked_execution_does_not_train_models
operator_review_after_blocked_execution_does_not_score_strategy
operator_review_after_blocked_execution_does_not_generate_trade_recommendations
operator_review_after_blocked_execution_does_not_accept_predictive_usefulness
operator_review_after_blocked_execution_does_not_accept_profitability
operator_review_after_blocked_execution_does_not_authorize_runtime
operator_review_after_blocked_execution_does_not_authorize_broker_execution
source_authority_candidate_is_not_source_authority_enrichment_execution
no_change_disposition_candidate_is_not_no_change_disposition_execution
alternate_diagnostic_option_is_not_diagnostic_execution
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_candidate_remains_source_evidence
blocked_reason_remains_authoritative_for_review
source_authority_gap_is_not_root_cause
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
no_change_records_means_no_remediation_success
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_approval_required_before_any_execution
separate_results_review_required_after_any_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()
)

TRUE_FIELDS = tuple(
    """source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_created
source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_ready
source_candidate_reviewed
source_failure_diagnosis_reviewed
source_blocked_execution_reviewed
source_blocked_reason_reviewed
source_authority_gap_reviewed
priority1_validation_disposition_reviewed
retained_change_records_absence_reviewed
detached_retry_failed_status_preserved
candidate_philosophy_reviewed
source_authority_or_no_change_disposition_packages_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed""".splitlines()
)

FALSE_FIELDS = tuple(
    """recommended_package_selected
source_authority_or_no_change_disposition_package_selected
source_authority_or_no_change_disposition_package_approved
source_authority_or_no_change_disposition_package_authorized
source_authority_or_no_change_disposition_execution_performed
source_authority_enrichment_performed
no_change_disposition_performed
alternate_diagnostic_execution_performed
remediation_execution_performed
controlled_plan_derived_remediation_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
ready_for_source_authority_or_no_change_disposition_approval
ready_for_source_authority_or_no_change_disposition_execution
ready_for_remediation_execution
ready_for_retry_candidate
ready_for_main_merge_approval
pytest_performed_in_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_review
cache_modified_in_review
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
retry_approval_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
integration_execution_successful
successful_integration_execution_digest_generated
successful_integration_validation_digest_generated
integration_branch_pushed
main_push_performed
origin_main_modified_by_this_task
evidence_regenerated
provider_requests_made_in_review
market_data_acquisition_performed_in_review
dataset_generation_performed_in_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError(ValueError):
    """Raised when reviewed evidence or a closed boundary changes."""


def _validated_source_candidate(source_candidate: dict | None) -> dict[str, Any]:
    candidate = (
        source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
        if source_candidate is None
        else deepcopy(source_candidate)
    )
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(candidate)
    except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError(
            "source candidate validation failed"
        ) from exc
    if candidate.get(source.CANDIDATE_DIGEST_KEY) != SOURCE_CANDIDATE_DIGEST:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError(
            "source candidate digest mismatch"
        )
    return candidate


def _source_bindings() -> dict[str, Any]:
    bindings = deepcopy(source.SOURCE_BINDINGS)
    bindings.update(
        {
            "source_candidate_artifact_kind": source.ARTIFACT_KIND,
            "source_candidate_status": source.CANDIDATE_STATUS,
            "source_candidate_scope": source.CANDIDATE_SCOPE,
            "source_candidate_commit": SOURCE_CANDIDATE_COMMIT,
            "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest": SOURCE_CANDIDATE_DIGEST,
        }
    )
    return bindings


SOURCE_BINDINGS = _source_bindings()


def _reviewed_packages(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    reviewed = []
    for source_package in candidate["proposed_source_authority_or_no_change_disposition_packages"]:
        package = {
            "package_id": source_package["package_id"],
            "source_status": source_package["status"],
            "review_status": (
                "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
                if source_package["package_id"] == RECOMMENDED_PACKAGE
                else "REVIEWED_BLOCKED_NOT_ALLOWED"
                if source_package["status"] == "BLOCKED_NOT_ALLOWED"
                else "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
            ),
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        for field in ("purpose", "blocked_reason"):
            if field in source_package:
                package[field] = source_package[field]
        reviewed.append(package)
    return reviewed


def _reviewed_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": requirement_id,
            "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION",
            "execution_status": "NOT_EXECUTED",
        }
        for requirement_id in source.FUTURE_REQUIREMENT_IDS
    ]


def _reviewed_plan() -> list[dict[str, Any]]:
    return [
        {
            "step_id": index,
            "action": action,
            "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
            "execution_status": "NOT_EXECUTED",
        }
        for index, action in enumerate(source.FUTURE_PLAN, 1)
    ]


def _reviewed_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
            "generation_status": "NOT_GENERATED",
        }
        for output_id in source.PLANNED_OUTPUT_NAMES
    ]


def _reviewed_non_goals() -> list[dict[str, Any]]:
    return [
        {"non_goal_id": non_goal_id, "review_status": "REVIEWED_ACTIVE"}
        for non_goal_id in source.NON_GOALS
    ]


def _recommendation() -> dict[str, Any]:
    return {
        "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION",
        "reason": "The source-authority or no-change disposition candidate has been reviewed, but no package has been selected or approved by this review. The recommended source-authority enrichment package requires a separate approval ceremony before any source-authority enrichment, no-change disposition, alternate diagnostic execution, remediation, retry candidate, retry execution, or main merge.",
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


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        _check(f"{field}_bound", expected, review.get(field))
        for field, expected in SOURCE_BINDINGS.items()
    ]
    checks.extend(
        (
            _check("primary_failure_class_bound", source.source.PRIMARY_FAILURE_CLASS, review.get("primary_failure_class")),
            _check("secondary_failure_classes_bound", list(source.source.SECONDARY_FAILURE_CLASSES), review.get("secondary_failure_classes")),
            _check("recommended_package_bound", RECOMMENDED_PACKAGE, review.get("recommended_source_authority_or_no_change_disposition_package")),
            _check("reviewed_packages_12", 12, len(review.get("reviewed_source_authority_or_no_change_disposition_packages", []))),
            _check("reviewed_requirements_50", 50, len(review.get("reviewed_future_requirements", []))),
            _check("reviewed_plan_12", 12, len(review.get("reviewed_future_plan", []))),
            _check("reviewed_outputs_21", 21, len(review.get("reviewed_planned_outputs", []))),
            _check("reviewed_non_goals_71", 71, len(review.get("reviewed_non_goals", []))),
            _check("priority_1_total_612", 612, review.get("priority_1_total_nodeids")),
            _check("top_10_total_1069", 1069, review.get("top_10_count_sum")),
            _check("module_summary_29", 29, review.get("module_summary_module_count")),
            _check("failed_or_errored_1404", 1404, review.get("failed_or_errored_nodeids_count")),
            _check("priority1_pre_675", 675, review.get("priority1_pre_change_validation_passed_count")),
            _check("priority1_post_675", 675, review.get("priority1_post_change_validation_passed_count")),
            _check("observable_families_4", 4, review.get("observable_failure_family_count")),
            _check("observable_items_188", 188, review.get("total_observable_evidence_items")),
            _check("workstreams_4", 4, review.get("source_workstream_count")),
            _check("risk_controls_exact", list(RISK_CONTROLS), review.get("risk_controls")),
            _check("next_chain_exact", list(NEXT_CHAIN), review.get("next_chain")),
            _check("next_gates_exact", list(NEXT_GATES), review.get("next_gates")),
            _check("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, review.get("no_tracked_pytest_cache_files")),
        )
    )
    checks.extend(_check(f"{field}_true", True, review.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, review.get(field)) for field in FALSE_FIELDS)
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checks = review["checklist"]
    passed = sum(item["status"] == PASS for item in checks)
    failed = len(checks) - passed
    summary = {
        "total_checks": len(checks),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
    }
    for field in TRUE_FIELDS + FALSE_FIELDS:
        summary[field] = review[field]
    summary.update(
        {
            "source_blocked_reason": source.source.SOURCE_BLOCKED_REASON,
            "primary_failure_class": source.source.PRIMARY_FAILURE_CLASS,
            "secondary_failure_classes": list(source.source.SECONDARY_FAILURE_CLASSES),
            "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
            "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "source_workstream_count": 4,
            "observable_failure_family_count": 4,
            "total_observable_evidence_items": 188,
            "priority_1_total_nodeids": 612,
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "predictive_usefulness_accepted": False,
            "profitability_accepted": False,
            "runtime_authorized": False,
            "broker_execution_authorized": False,
        }
    )
    return summary


def _digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict[str, Any]:
    """Build an operator review without selecting or authorizing a package."""

    candidate = _validated_source_candidate(source_candidate)
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **SOURCE_BINDINGS,
        "selected_remediation_execution_package": candidate["selected_remediation_execution_package"],
        "primary_failure_class": candidate["primary_failure_class"],
        "secondary_failure_classes": deepcopy(candidate["secondary_failure_classes"]),
        "retry_failure_context": deepcopy(candidate["retry_failure_context"]),
        "source_candidate_summary": {
            "artifact_kind": candidate["artifact_kind"],
            "status": candidate["candidate_status"],
            "scope": candidate["candidate_scope"],
            "commit": SOURCE_CANDIDATE_COMMIT,
            "digest": SOURCE_CANDIDATE_DIGEST,
            "checklist": "267/267 PASS",
        },
        "source_failure_diagnosis_summary": deepcopy(candidate["source_failure_diagnosis_summary"]),
        "source_blocked_execution_summary": deepcopy(candidate["source_blocked_execution_summary"]),
        "source_approval_summary": deepcopy(candidate["source_approval_summary"]),
        "source_operator_review_and_candidate_summary": deepcopy(candidate["source_operator_review_and_candidate_summary"]),
        "source_plan_results_review_summary": deepcopy(candidate["source_plan_results_review_summary"]),
        "source_plan_execution_summary": deepcopy(candidate["source_plan_execution_summary"]),
        "source_targeted_remediation_plan_summary": deepcopy(candidate["source_targeted_remediation_plan_summary"]),
        "source_workstream_mapping_summary": deepcopy(candidate["source_workstream_mapping_summary"]),
        "source_method_results_review_summary": deepcopy(candidate["source_method_results_review_summary"]),
        "source_method_execution_summary": deepcopy(candidate["source_method_execution_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(candidate["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_summary": deepcopy(candidate["source_controlled_recapture_summary"]),
        "source_durable_receipt_summary": deepcopy(candidate["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(candidate["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(candidate["source_planning_and_detail_binding_summary"]),
        "priority_1_target_modules": deepcopy(candidate["priority_1_target_modules"]),
        "priority_1_total_nodeids": candidate["priority_1_total_nodeids"],
        "top_10_count_sum": candidate["top_10_count_sum"],
        "module_summary_module_count": candidate["module_summary_module_count"],
        "failed_or_errored_nodeids_count": candidate["failed_or_errored_nodeids_count"],
        "priority1_validation_summary": deepcopy(candidate["priority1_validation_summary"]),
        "priority1_pre_change_validation_passed": candidate["priority1_pre_change_validation_passed"],
        "priority1_pre_change_validation_passed_count": candidate["priority1_pre_change_validation_passed_count"],
        "priority1_post_change_validation_passed": candidate["priority1_post_change_validation_passed"],
        "priority1_post_change_validation_passed_count": candidate["priority1_post_change_validation_passed_count"],
        "priority1_post_change_stdout_sha256": candidate["priority1_post_change_stdout_sha256"],
        "priority1_post_change_stderr_sha256": candidate["priority1_post_change_stderr_sha256"],
        "source_exit_code": candidate["source_exit_code"],
        "source_stdout_byte_count": candidate["source_stdout_byte_count"],
        "source_stderr_byte_count": candidate["source_stderr_byte_count"],
        "source_stdout_sha256": candidate["source_stdout_sha256"],
        "source_stderr_sha256": candidate["source_stderr_sha256"],
        "diagnostic_capture_evidence_summary": deepcopy(candidate["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(candidate["reviewed_observable_failure_families"]),
        "observable_failure_family_count": candidate["observable_failure_family_count"],
        "total_observable_evidence_items": candidate["total_observable_evidence_items"],
        "reviewed_workstreams": deepcopy(candidate["reviewed_workstreams"]),
        "source_workstream_count": candidate["source_workstream_count"],
        "reviewed_candidate_philosophy": {
            "reviewed_source_authority_or_no_change_disposition_candidate_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
            "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
            "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
            "review_status": "REVIEWED_PLANNING_ONLY",
        },
        "reviewed_source_authority_or_no_change_disposition_packages": _reviewed_packages(candidate),
        "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "reviewed_future_requirements": _reviewed_requirements(),
        "reviewed_future_plan": _reviewed_plan(),
        "reviewed_planned_outputs": _reviewed_outputs(),
        "reviewed_non_goals": _reviewed_non_goals(),
        "recommendation": _recommendation(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(
    review: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError
    if not isinstance(review, dict):
        raise error("operator review must be an object")
    fixed = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        "selected_remediation_execution_package": source.source.source.SELECTED_PACKAGE,
        "primary_failure_class": source.source.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(source.source.SECONDARY_FAILURE_CLASSES),
        "recommended_source_authority_or_no_change_disposition_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "priority_1_target_modules": source.SOURCE_CORE["priority_1_target_modules"],
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "priority1_pre_change_validation_passed": True,
        "priority1_pre_change_validation_passed_count": 675,
        "priority1_post_change_validation_passed": True,
        "priority1_post_change_validation_passed_count": 675,
        "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_stdout_sha256": source.SOURCE_CORE["source_stdout_sha256"],
        "source_stderr_sha256": source.SOURCE_CORE["source_stderr_sha256"],
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "source_workstream_count": 4,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    for field, expected in fixed.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    for field, expected in SOURCE_BINDINGS.items():
        if review.get(field) != expected:
            raise error(f"{field} mismatch")
    source_candidate = source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
    expected_candidate_summary = {
        "artifact_kind": source_candidate["artifact_kind"],
        "status": source_candidate["candidate_status"],
        "scope": source_candidate["candidate_scope"],
        "commit": SOURCE_CANDIDATE_COMMIT,
        "digest": SOURCE_CANDIDATE_DIGEST,
        "checklist": "267/267 PASS",
    }
    if review.get("source_candidate_summary") != expected_candidate_summary:
        raise error("source candidate summary mismatch")
    source_summary_fields = (
        "source_failure_diagnosis_summary",
        "source_blocked_execution_summary",
        "source_approval_summary",
        "source_operator_review_and_candidate_summary",
        "source_plan_results_review_summary",
        "source_plan_execution_summary",
        "source_targeted_remediation_plan_summary",
        "source_workstream_mapping_summary",
        "source_method_results_review_summary",
        "source_method_execution_summary",
        "source_diagnostic_results_review_summary",
        "source_controlled_recapture_summary",
        "source_durable_receipt_summary",
        "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
        "priority1_validation_summary",
        "diagnostic_capture_evidence_summary",
    )
    for field in source_summary_fields:
        if review.get(field) != source_candidate[field]:
            raise error(f"{field} mismatch")
    if review.get("retry_failure_context") != source_candidate["retry_failure_context"]:
        raise error("retry failure counts mismatch")
    if review.get("reviewed_observable_failure_families") != source_candidate["reviewed_observable_failure_families"]:
        raise error("observable families mismatch")
    if review.get("reviewed_workstreams") != source_candidate["reviewed_workstreams"]:
        raise error("reviewed workstreams mismatch")
    expected_philosophy = {
        "reviewed_source_authority_or_no_change_disposition_candidate_philosophy": REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
        "review_status": "REVIEWED_PLANNING_ONLY",
    }
    if review.get("reviewed_candidate_philosophy") != expected_philosophy:
        raise error("reviewed candidate philosophy mismatch")
    if review.get("reviewed_source_authority_or_no_change_disposition_packages") != _reviewed_packages(source_candidate):
        raise error("reviewed packages mismatch")
    packages = review["reviewed_source_authority_or_no_change_disposition_packages"]
    if any(item.get("selected") or item.get("approved") or item.get("authorized") or item.get("executed") for item in packages):
        raise error("review selected or authorized a package")
    if review.get("reviewed_future_requirements") != _reviewed_requirements():
        raise error("reviewed future requirements mismatch")
    if review.get("reviewed_future_plan") != _reviewed_plan():
        raise error("reviewed future plan mismatch")
    if review.get("reviewed_planned_outputs") != _reviewed_outputs():
        raise error("reviewed planned outputs mismatch")
    if review.get("reviewed_non_goals") != _reviewed_non_goals():
        raise error("reviewed non-goals mismatch")
    if review.get("recommendation") != _recommendation():
        raise error("recommendation mismatch")
    if review.get("next_chain") != list(NEXT_CHAIN) or review.get("next_gates") != list(NEXT_GATES):
        raise error("next governance path mismatch")
    if review.get("risk_controls") != list(RISK_CONTROLS):
        raise error("risk controls mismatch")
    for field in TRUE_FIELDS:
        if review.get(field) is not True:
            raise error(f"{field} must be true")
    for field in FALSE_FIELDS:
        if review.get(field) is not False:
            raise error(f"{field} must be false")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    digest = review.get(OPERATOR_REVIEW_DIGEST_KEY)
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _digest(review):
        raise error("operator review digest missing or changed")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "operator_review_digest": digest,
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Candidate", "Source Failure Diagnosis", "Source Blocked Execution", "Blocked Reason",
    "Failure Classification", "Source Approval", "Source Operator Review and Candidate",
    "Source Plan Results Review", "Source Plan Execution", "Source Targeted Remediation Plan",
    "Source Workstream Mapping", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Receipt Loss History", "Source Planning and Detail Binding Evidence", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary",
    "Reviewed Observable Families", "Reviewed Workstreams", "Reviewed Candidate Philosophy",
    "Reviewed Packages", "Recommended Package", "Reviewed Future Requirements", "Reviewed Future Plan",
    "Reviewed Planned Outputs", "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates",
    "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_markdown_v1(
    review: dict,
) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(deepcopy(review))
    sections = {
        "Source Candidate": review["source_candidate_summary"],
        "Source Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Source Blocked Execution": review["source_blocked_execution_summary"],
        "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"], "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY]},
        "Source Approval": review["source_approval_summary"],
        "Source Operator Review and Candidate": review["source_operator_review_and_candidate_summary"],
        "Source Plan Results Review": review["source_plan_results_review_summary"],
        "Source Plan Execution": review["source_plan_execution_summary"],
        "Source Targeted Remediation Plan": review["source_targeted_remediation_plan_summary"],
        "Source Workstream Mapping": review["source_workstream_mapping_summary"],
        "Source Method Results Review": review["source_method_results_review_summary"],
        "Source Method Execution": review["source_method_execution_summary"],
        "Source Diagnostic Results Review": review["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": review["source_controlled_recapture_summary"],
        "Source Durable Receipt": review["source_durable_receipt_summary"],
        "Source Receipt Loss History": review["source_receipt_loss_history_summary"],
        "Source Planning and Detail Binding Evidence": review["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": review["retry_failure_context"],
        "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"],
        "Reviewed Workstreams": review["reviewed_workstreams"],
        "Reviewed Candidate Philosophy": review["reviewed_candidate_philosophy"],
        "Reviewed Packages": review["reviewed_source_authority_or_no_change_disposition_packages"],
        "Recommended Package": {"package": review["recommended_source_authority_or_no_change_disposition_package"], "status": review["recommendation_status"]},
        "Reviewed Future Requirements": review["reviewed_future_requirements"],
        "Reviewed Future Plan": review["reviewed_future_plan"],
        "Reviewed Planned Outputs": review["reviewed_planned_outputs"],
        "Reviewed Non-Goals": review["reviewed_non_goals"],
        "Recommendation": review["recommendation"],
        "Next Chain": review["next_chain"],
        "Next Gates": review["next_gates"],
        "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {"package_selected": False, "approval_ready": False, "retry_ready": False, "runtime_use": review["runtime_use"]},
        "Checklist Summary": review["summary"],
        "Guardrails": list(FALSE_FIELDS),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Candidate After Blocked Execution Operator Review v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", f"```text\n{sections[title]!r}\n```", ""))
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(source_candidate=source_candidate)
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_markdown_v1(review), encoding="utf-8")
    return review


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_DIGEST_KEY = OPERATOR_REVIEW_DIGEST_KEY
NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED = source.source.PRIMARY_FAILURE_CLASS
REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY = source.source.SECONDARY_FAILURE_CLASSES[0]
PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT = source.source.SECONDARY_FAILURE_CLASSES[1]
NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS = source.source.SECONDARY_FAILURE_CLASSES[2]
DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED = source.source.SECONDARY_FAILURE_CLASSES[3]
