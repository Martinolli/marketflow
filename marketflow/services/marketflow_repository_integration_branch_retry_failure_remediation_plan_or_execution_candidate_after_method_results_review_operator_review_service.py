"""Review the remediation-plan candidate after method results review, without selection."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_service
    as source,
)

ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_CANDIDATE_DIGEST = "6d65a12f6fcb17859e8e241f45ef6fa45839f475429c966ad2adbbb3f1990ea2"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_V1_IF_SELECTED"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

REVIEWED_PHILOSOPHY = (
    "The method results review verified four high-confidence observable failure families from bounded diagnostic evidence: "
    "assertion_or_value_mismatch, digest_or_hash_mismatch, fixture_or_test_isolation_issue, and missing_or_unexpected_field. "
    "These families support controlled remediation planning, but they do not establish root cause, direct remediation readiness, "
    "retry readiness, or main-merge readiness. The reviewed candidate correctly recommends a plan-first package rather than "
    "direct remediation execution."
)
REVIEWED_CANDIDATE_BOUNDARY = (
    "Operator-review only; no package selection, approval, remediation planning execution, code remediation, evidence "
    "remediation, method rerun, diagnostic rerun, retry, results review, main merge, runtime, or trading authority is created."
)
REVIEWED_CANDIDATE_GOAL = (
    "Review safe future remediation-plan or remediation-execution packages after method results review, preserving a plan-first "
    "recommendation and all downstream gates."
)
REVIEWED_PLANNING_STATUS = "REVIEWED_PLANNING_ONLY"
RECOMMENDATION_REASON = (
    "The method results review identified four high-confidence observable failure families, but direct_remediation_ready, "
    "retry_ready, and main_merge_ready remain false. A plan-first remediation package can convert the reviewed bounded method "
    "evidence into controlled remediation workstreams without prematurely modifying code, updating tests, changing digests, "
    "running pytest, or creating retry readiness."
)
NEXT_TASK_REASON = (
    "The remediation plan or execution candidate after method results review has been reviewed, but no remediation plan or "
    "execution package has been selected or approved by this review. The recommended plan-first package requires a separate "
    "approval ceremony before any remediation planning execution."
)


def _reviewed_package(item: Mapping[str, Any]) -> dict[str, Any]:
    source_status = item["status"]
    if source_status == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED":
        review_status = "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    elif source_status == "BLOCKED_NOT_ALLOWED":
        review_status = "REVIEWED_BLOCKED_NOT_ALLOWED"
    else:
        review_status = "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
    reviewed = {
        "package_id": item["package_id"],
        "source_status": source_status,
        "review_status": review_status,
        "selected": False,
        "approved": False,
        "authorized": False,
        "executed": False,
        "purpose": item["purpose"],
    }
    for field in ("recommended_reason", "blocked_reason"):
        if field in item:
            reviewed[field] = item[field]
    return reviewed


REVIEWED_PACKAGES = [_reviewed_package(item) for item in source.PROPOSED_PACKAGES]
REVIEWED_FUTURE_REQUIREMENTS = [
    {
        "requirement_id": item["requirement_id"],
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION_PLAN_OR_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }
    for item in source.FUTURE_REQUIREMENTS
]
REVIEWED_FUTURE_PLAN = [
    {
        "step_id": item["step"],
        "action": item["action"],
        "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        "execution_status": "NOT_EXECUTED",
    }
    for item in source.FUTURE_PLAN
]
REVIEWED_PLANNED_OUTPUTS = [
    {
        "output_id": item["output_id"],
        "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
        "generation_status": "NOT_GENERATED",
    }
    for item in source.PLANNED_OUTPUTS
]
REVIEWED_NON_GOALS = [
    {"non_goal_id": item, "review_status": "REVIEWED_ACTIVE"}
    for item in source.NON_GOALS
]

NEXT_CHAIN = [
    "Remediation Plan or Execution Approval After Method Results Review v1, if selected.",
    "Remediation Plan or Execution After Method Results Review v1, if approved.",
    "Remediation Plan or Execution Results Review After Method Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = """remediation_plan_or_execution_approval_after_method_results_review_if_selected
remediation_plan_or_execution_after_method_results_review_if_approved
remediation_plan_or_execution_results_review_after_method_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()

RISK_CONTROLS = [
    item.replace("candidate_after_method_results_review_", "operator_review_after_method_results_review_")
    for item in source.RISK_CONTROLS
    if item != "separate_operator_review_required_before_remediation_approval"
]
RISK_CONTROLS.insert(
    RISK_CONTROLS.index("method_results_review_remains_source_evidence") + 1,
    "remediation_plan_or_execution_candidate_remains_source_evidence",
)

TRUE_FIELDS = """remediation_plan_or_execution_candidate_after_method_results_review_operator_review_created
remediation_plan_or_execution_candidate_after_method_results_review_operator_review_ready
source_candidate_reviewed
source_method_results_review_reviewed
source_method_execution_reviewed
observable_failure_families_reviewed
family_classification_evidence_reviewed_for_future_remediation_planning
remediation_plan_or_execution_packages_reviewed
future_remediation_requirements_reviewed
future_remediation_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed""".splitlines()

FALSE_FIELDS = """recommended_package_selected
remediation_plan_or_execution_package_selected
remediation_plan_or_execution_package_approved
remediation_plan_or_execution_package_authorized
remediation_plan_or_execution_performed
remediation_plan_generated
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
method_execution_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
failure_family_classification_performed_in_review
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_review
full_pytest_performed
retry_rerun_performed
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
direct_code_remediation_recommended
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_plan_or_execution_approval
ready_for_remediation_plan_or_execution_execution
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
provider_requests_made_in_review
market_data_acquisition_performed_in_review
dataset_generation_performed_in_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError(ValueError):
    """Raised when operator-review evidence or its closed authority changes."""


def _source_bindings() -> dict[str, Any]:
    return {
        **source._source_bindings(),
        "source_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_candidate_status": source.CANDIDATE_STATUS,
        "source_candidate_scope": source.CANDIDATE_SCOPE,
        "source_remediation_plan_or_execution_candidate_after_method_results_review_digest": SOURCE_CANDIDATE_DIGEST,
    }


def _core() -> dict[str, Any]:
    source_core = source._core()
    return {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **_source_bindings(),
        "selected_source_method_package": source.source.SELECTED_PACKAGE,
        "retry_execution_commit": source_core["retry_execution_commit"],
        "retry_failure_context": deepcopy(source_core["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(source_core["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": source_core["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": source_core["source_stdout_sha256"],
        "source_stderr_sha256": source_core["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "source_candidate_summary": {
            "candidate_digest": SOURCE_CANDIDATE_DIGEST,
            "candidate_created": True,
            "candidate_ready_for_operator_review": True,
            "recommended_package": RECOMMENDED_PACKAGE,
            "recommended_package_selected": False,
        },
        "source_method_results_review_summary": deepcopy(source_core["source_method_results_review_summary"]),
        "source_method_execution_summary": deepcopy(source_core["source_method_execution_summary"]),
        "source_failure_family_classification_summary": deepcopy(source_core["source_failure_family_classification_summary"]),
        "source_bounded_excerpt_analysis_summary": deepcopy(source_core["source_bounded_excerpt_analysis_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(source_core["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_execution_summary": deepcopy(source_core["source_controlled_recapture_execution_summary"]),
        "source_durable_receipt_summary": deepcopy(source_core["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(source_core["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(source_core["source_planning_and_detail_binding_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(source_core["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(source_core["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "reviewed_remediation_plan_or_execution_candidate_after_method_results_review_philosophy": REVIEWED_PHILOSOPHY,
        "reviewed_candidate_philosophy": {
            "philosophy": REVIEWED_PHILOSOPHY,
            "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
            "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
            "review_status": REVIEWED_PLANNING_STATUS,
        },
        "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
        "reviewed_planning_status": REVIEWED_PLANNING_STATUS,
        "reviewed_remediation_plan_or_execution_packages": deepcopy(REVIEWED_PACKAGES),
        "recommended_remediation_plan_or_execution_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommendation_reason": RECOMMENDATION_REASON,
        "reviewed_future_remediation_requirements": deepcopy(REVIEWED_FUTURE_REQUIREMENTS),
        "reviewed_future_remediation_plan": deepcopy(REVIEWED_FUTURE_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
            "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_PLAN_OR_EXECUTION",
            "reason": NEXT_TASK_REASON,
        },
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_PLAN_OR_EXECUTION",
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


SOURCE_CHECK_FIELDS = {
    "source_candidate_digest_bound": "source_remediation_plan_or_execution_candidate_after_method_results_review_digest",
    **{
        ("source_remediation_or_method_candidate_digest_bound" if check_id == "source_candidate_digest_bound" else check_id): field
        for check_id, field in source.SOURCE_CHECK_FIELDS.items()
    },
}

_REVIEW_FIELD_RENAMES = {
    "diagnostic_receipt_parsed_in_candidate": "diagnostic_receipt_parsed_in_review",
    "diagnostic_output_analyzed_in_candidate": "diagnostic_output_analyzed_in_review",
    "failure_family_classification_performed_in_candidate": "failure_family_classification_performed_in_review",
    "targeted_pytest_performed_in_candidate": "targeted_pytest_performed_in_review",
    "cache_read_in_candidate": "cache_read_in_review",
    "cache_modified_in_candidate": "cache_modified_in_review",
    "provider_requests_made_in_candidate": "provider_requests_made_in_review",
    "market_data_acquisition_performed_in_candidate": "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_candidate": "dataset_generation_performed_in_review",
}
FALSE_CHECK_FIELDS = {
    check_id.replace("performed_in_candidate", "performed_in_review").replace("targeted_pytest_in_candidate", "targeted_pytest_in_review"):
    _REVIEW_FIELD_RENAMES.get(field, field)
    for check_id, field in source.FALSE_CHECK_FIELDS.items()
}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected = _core()
    checks = [_check(check_id, expected[field], review.get(field)) for check_id, field in SOURCE_CHECK_FIELDS.items()]
    checks += [
        _check("retry_execution_commit_bound", expected["retry_execution_commit"], review.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", expected["retry_failure_context"]["counts"], review.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", expected["priority_1_target_modules"], review.get("priority_1_target_modules")),
        _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
        _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
        _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
        _check("exit_code_1_bound_as_diagnostic_only", [1, True], [review.get("source_exit_code"), review.get("source_exit_code_is_diagnostic_only")]),
        _check("stdout_hash_bound", expected["source_stdout_sha256"], review.get("source_stdout_sha256")),
        _check("stderr_hash_bound", expected["source_stderr_sha256"], review.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, review.get("source_stdout_byte_count")),
        _check("stderr_byte_count_0_bound", 0, review.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, review.get("source_stdout_excerpt_truncated")),
        _check("stderr_excerpt_truncated_false_bound", False, review.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, review.get("source_redaction_checked")),
        _check("observable_family_count_4_bound", 4, review.get("observable_failure_family_count")),
        _check("observable_evidence_items_188_bound", 188, review.get("total_observable_evidence_items")),
    ]
    families = review.get("reviewed_observable_failure_families", [])
    family_ids = {item.get("family_id") for item in families if isinstance(item, dict)}
    checks.extend(_check(f"{family_id}_family_bound", True, family_id in family_ids) for family_id in source.source.FAMILY_IDS)
    checks += [
        _check("family_confidence_high_bound", True, len(families) == 4 and all(item.get("confidence") == "HIGH" for item in families)),
        _check("additional_diagnostic_capture_false_bound", False, review.get("additional_diagnostic_capture_may_be_needed")),
        _check("direct_remediation_ready_false_bound", False, review.get("direct_remediation_ready")),
        _check("retry_ready_false_bound", False, review.get("retry_ready")),
        _check("main_merge_ready_false_bound", False, review.get("main_merge_ready")),
        _check("operator_review_created_true", True, review.get("remediation_plan_or_execution_candidate_after_method_results_review_operator_review_created")),
        _check("operator_review_ready_true", True, review.get("remediation_plan_or_execution_candidate_after_method_results_review_operator_review_ready")),
        _check("source_candidate_reviewed_true", True, review.get("source_candidate_reviewed")),
        _check("source_method_results_review_reviewed_true", True, review.get("source_method_results_review_reviewed")),
        _check("source_method_execution_reviewed_true", True, review.get("source_method_execution_reviewed")),
        _check("observable_failure_families_reviewed_true", True, review.get("observable_failure_families_reviewed")),
        _check("remediation_plan_or_execution_packages_reviewed_true", True, review.get("remediation_plan_or_execution_packages_reviewed")),
        _check("recommended_package_reviewed_not_selected", [RECOMMENDED_PACKAGE, False], [review.get("recommended_remediation_plan_or_execution_package"), review.get("recommended_package_selected")]),
        _check("packages_reviewed_12", 12, len(review.get("reviewed_remediation_plan_or_execution_packages", []))),
        _check("blocked_packages_reviewed_6", 6, sum(item.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review.get("reviewed_remediation_plan_or_execution_packages", []))),
        _check("future_remediation_requirements_reviewed", [True, REVIEWED_FUTURE_REQUIREMENTS], [review.get("future_remediation_requirements_reviewed"), review.get("reviewed_future_remediation_requirements")]),
        _check("future_remediation_plan_reviewed", [True, REVIEWED_FUTURE_PLAN], [review.get("future_remediation_plan_reviewed"), review.get("reviewed_future_remediation_plan")]),
        _check("planned_outputs_reviewed", [True, REVIEWED_PLANNED_OUTPUTS], [review.get("planned_outputs_reviewed"), review.get("reviewed_planned_outputs")]),
        _check("non_goals_reviewed", [True, REVIEWED_NON_GOALS], [review.get("non_goals_reviewed"), review.get("reviewed_non_goals")]),
    ]
    checks.extend(_check(check_id, False, review.get(field)) for check_id, field in FALSE_CHECK_FIELDS.items())
    checks += [
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("recommendation_defined", expected["recommendation"], review.get("recommendation")),
        _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        _check("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, review.get("no_tracked_pytest_cache_files")),
    ]
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checks = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checks)
    return {
        "total_checks": len(checks),
        "passed_checks": passed,
        "failed_checks": len(checks) - passed,
        "blocker_count": len(checks) - passed,
        **{field: review.get(field) for field in TRUE_FIELDS},
        "recommended_remediation_plan_or_execution_package": RECOMMENDED_PACKAGE,
        **{field: review.get(field) for field in FALSE_FIELDS},
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "priority_1_top_module_count": 5,
        "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359",
        "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def _digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict:
    """Build the operator review without selecting or executing a package."""

    if source_candidate is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
                deepcopy(source_candidate)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError(
                "source candidate invalid"
            ) from exc
        if source_candidate.get(source.CANDIDATE_DIGEST_KEY) != SOURCE_CANDIDATE_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError(
                "source candidate digest mismatch"
            )
    review = _core()
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
    review: dict,
) -> dict:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    expected = _core()
    for field, value in expected.items():
        if review.get(field) != value:
            raise error(f"{field} mismatch")
    if review.get(OPERATOR_REVIEW_DIGEST_KEY) != _digest(review):
        raise error("operator review digest mismatch")
    checklist = _checklist(review)
    if review.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if review.get("summary") != _summary(review):
        raise error("summary mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
    output_dir: str | Path, *, source_candidate: dict | None = None,
) -> dict:
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
        source_candidate=source_candidate
    )
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError(
            "protected output directory"
        )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError(
            "output exists"
        )
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_markdown_v1(review),
        encoding="utf-8",
    )
    return review


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(review)
    sections = [
        ("Source Candidate", [SOURCE_CANDIDATE_DIGEST, source.ARTIFACT_KIND, source.CANDIDATE_STATUS]),
        ("Source Method Results Review", [review["source_method_results_review_commit"], review["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [review["source_method_execution_commit"], review["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [review["source_failure_family_classification_review_digest"], review["source_failure_family_classification_digest"]]),
        ("Source Bounded Excerpt Analysis", [review["source_bounded_excerpt_analysis_review_digest"], review["source_bounded_excerpt_analysis_digest"]]),
        ("Source Diagnostic Results Review", [review["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [review["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [review["source_durable_receipt_path"], review["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [review["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [review["source_planning_execution_digest"], review["source_detail_binding_results_review_digest"], review["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(review["retry_failure_context"])]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in review["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(review["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in review["reviewed_observable_failure_families"]]),
        ("Reviewed Candidate Philosophy", [REVIEWED_PHILOSOPHY, REVIEWED_CANDIDATE_BOUNDARY, REVIEWED_CANDIDATE_GOAL]),
        ("Reviewed Remediation Plan or Execution Packages", [f"{item['package_id']}: {item['review_status']}" for item in review["reviewed_remediation_plan_or_execution_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, RECOMMENDATION_REASON]),
        ("Reviewed Future Remediation Requirements", [item["requirement_id"] for item in review["reviewed_future_remediation_requirements"]]),
        ("Reviewed Future Remediation Plan", [f"{item['step_id']}. {item['action']}" for item in review["reviewed_future_remediation_plan"]]),
        ("Reviewed Planned Outputs", [item["output_id"] for item in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [item["non_goal_id"] for item in review["reviewed_non_goals"]]),
        ("Recommendation", [RECOMMENDED_NEXT_TASK, NEXT_TASK_REASON]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", [REVIEWED_CANDIDATE_BOUNDARY]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Constants-only review; no candidate builder, receipt/output access, execution, remediation, retry, provider, or protected-branch authority."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Candidate After Method Results Review Operator Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY = RECOMMENDED_PACKAGE
PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN = "PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN"
PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN = "PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN"
PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN = "PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN"
PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN = "PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN"
PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED = "PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED"
PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS = "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS"
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY = "PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY"
PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW = "PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW"
PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL = "PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL"
PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW = "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW"
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY"

__all__ = [
    name
    for name in globals()
    if name.isupper()
    or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))
]
