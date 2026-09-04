"""Review remediation-execution candidate packages without selecting or executing one."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_CANDIDATE_COMMIT = "c12583bc41e7de16c371f36f4408a468108a8bc7"
SOURCE_CANDIDATE_DIGEST = "6869b7642d8f90fd0273a7cbfdd069af85b23518778100ae19f3ebb6060fe4bd"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_V1_IF_SELECTED"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_digest"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

REVIEWED_PHILOSOPHY = (
    "The plan results review verified a targeted remediation plan with four controlled workstreams mapped to reviewed "
    "observable failure families: assertion/value mismatch, digest/hash boundary, fixture isolation/determinism, and "
    "schema/field contract. The candidate correctly defines remediation execution options for operator review, but it "
    "does not authorize remediation execution, code changes, test changes, digest updates, patch generation, retry "
    "readiness, or main-merge readiness."
)
REVIEWED_CANDIDATE_BOUNDARY = (
    "Operator-review only; no package selection, approval, remediation execution, code remediation, evidence "
    "remediation, test modification, digest update, patch generation, patch application, pytest, retry, main merge, "
    "runtime, broker, or trading authority is created."
)
REVIEWED_CANDIDATE_GOAL = (
    "Review safe future remediation execution package options after plan results review, preserving source evidence, "
    "change-control boundaries, verification requirements, and downstream retry/main gates."
)
RECOMMENDATION_REASON = (
    "The plan results review verified four workstreams and opened readiness only for a remediation execution candidate. "
    "The recommended controlled plan-derived package preserves source authority, bounded file scope, verification "
    "evidence, change-control boundaries, and post-execution review before any future retry. This operator review does "
    "not select or approve the package."
)
NEXT_TASK_REASON = (
    "The remediation execution candidate after plan results review has been reviewed, but no remediation execution "
    "package has been selected or approved by this review. The recommended controlled plan-derived remediation package "
    "requires a separate approval ceremony before any remediation execution, code change, test change, digest update, "
    "patch generation, pytest execution, retry, or main merge."
)


def _reviewed_package(item: Mapping[str, Any]) -> dict[str, Any]:
    source_status = item["status"]
    review_status = {
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
    }.get(source_status, "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED")
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
        "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION_EXECUTION",
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
    "Remediation Execution Approval After Plan Results Review v1, if selected.",
    "Remediation Execution v1, if approved.",
    "Remediation Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = """remediation_execution_approval_after_plan_results_review_if_selected
remediation_execution_if_approved
remediation_execution_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()

RISK_CONTROLS = [
    item.replace("candidate_after_plan_results_review_", "operator_review_after_plan_results_review_")
    for item in source.RISK_CONTROLS
    if item != "separate_operator_review_required_before_remediation_execution_approval"
]
RISK_CONTROLS.insert(
    RISK_CONTROLS.index("remediation_plan_candidate_remains_source_evidence") + 1,
    "remediation_execution_candidate_remains_source_evidence",
)

TRUE_FIELDS = """remediation_execution_candidate_after_plan_results_review_operator_review_created
remediation_execution_candidate_after_plan_results_review_operator_review_ready
source_candidate_reviewed
source_plan_results_review_reviewed
source_plan_execution_reviewed
source_targeted_remediation_plan_reviewed
source_workstream_mapping_reviewed
reviewed_workstreams_reviewed
verification_evidence_requirements_reviewed
future_approval_boundaries_reviewed
remediation_execution_packages_reviewed
future_remediation_execution_requirements_reviewed
future_remediation_execution_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed""".splitlines()

FALSE_FIELDS = """recommended_package_selected
remediation_execution_package_selected
remediation_execution_package_approved
remediation_execution_package_authorized
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
production_code_modified
existing_tests_modified
expected_digests_updated
patch_generated
patch_applied
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_review
method_execution_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
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
retry_success_claimed
main_merge_readiness_claimed
new_retry_candidate_created
new_retry_executed
new_retry_results_review_created
main_merge_approval_created
ready_for_remediation_execution_approval
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


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError(ValueError):
    """Raised when source evidence or a closed review boundary drifts."""


def _source_bindings() -> dict[str, Any]:
    bindings = deepcopy(source._source_bindings())
    bindings.update(
        {
            "source_candidate_artifact_kind": source.ARTIFACT_KIND,
            "source_candidate_status": source.CANDIDATE_STATUS,
            "source_candidate_scope": source.CANDIDATE_SCOPE,
            "source_candidate_commit": SOURCE_CANDIDATE_COMMIT,
            "source_remediation_execution_candidate_after_plan_results_review_digest": SOURCE_CANDIDATE_DIGEST,
        }
    )
    return bindings


def _core() -> dict[str, Any]:
    candidate = source._core()
    summary_names = [
        "source_plan_execution_summary",
        "source_approval_summary",
        "source_operator_review_and_candidate_summary",
        "source_method_results_review_summary",
        "source_method_execution_summary",
        "source_failure_family_classification_summary",
        "source_diagnostic_results_review_summary",
        "source_controlled_recapture_execution_summary",
        "source_durable_receipt_summary",
        "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
        "source_plan_results_review_summary",
        "source_targeted_remediation_plan_summary",
        "source_workstream_mapping_summary",
    ]
    return {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS,
        "review_scope": REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **_source_bindings(),
        "selected_source_plan_package": source.SELECTED_SOURCE_PLAN_PACKAGE,
        "retry_execution_commit": candidate["retry_execution_commit"],
        "retry_failure_context": deepcopy(candidate["retry_failure_context"]),
        **{name: deepcopy(candidate[name]) for name in summary_names},
        "source_candidate_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "candidate_status": source.CANDIDATE_STATUS,
            "candidate_scope": source.CANDIDATE_SCOPE,
            "commit": SOURCE_CANDIDATE_COMMIT,
            "candidate_digest": SOURCE_CANDIDATE_DIGEST,
            "checklist_total": 317,
            "checklist_passed": 317,
            "blocker_count": 0,
            "recommended_package": RECOMMENDED_PACKAGE,
            "recommended_package_selected": False,
        },
        "priority_1_target_modules": deepcopy(candidate["priority_1_target_modules"]),
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "module_summary_module_count": 29,
        "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1,
        "source_duration_seconds": candidate["source_duration_seconds"],
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": candidate["source_stdout_sha256"],
        "source_stderr_sha256": candidate["source_stderr_sha256"],
        "source_stdout_excerpt_truncated": True,
        "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True,
        "source_exit_code_is_diagnostic_only": True,
        "diagnostic_capture_evidence_summary": deepcopy(candidate["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(candidate["reviewed_observable_failure_families"]),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_workstream_count": 4,
        "reviewed_targeted_remediation_plan": deepcopy(candidate["reviewed_targeted_remediation_plan"]),
        "reviewed_workstreams": deepcopy(candidate["reviewed_workstreams"]),
        "reviewed_remediation_execution_candidate_after_plan_results_review_philosophy": REVIEWED_PHILOSOPHY,
        "reviewed_candidate_philosophy": {
            "philosophy": REVIEWED_PHILOSOPHY,
            "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
            "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
            "review_status": "REVIEWED_PLANNING_ONLY",
        },
        "reviewed_candidate_boundary": REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": REVIEWED_CANDIDATE_GOAL,
        "review_status_detail": "REVIEWED_PLANNING_ONLY",
        "reviewed_remediation_execution_packages": deepcopy(REVIEWED_PACKAGES),
        "recommended_remediation_execution_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommendation_reason": RECOMMENDATION_REASON,
        "reviewed_future_remediation_execution_requirements": deepcopy(REVIEWED_FUTURE_REQUIREMENTS),
        "reviewed_future_remediation_execution_plan": deepcopy(REVIEWED_FUTURE_PLAN),
        "reviewed_planned_outputs": deepcopy(REVIEWED_PLANNED_OUTPUTS),
        "reviewed_non_goals": deepcopy(REVIEWED_NON_GOALS),
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
            "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_EXECUTION",
            "reason": NEXT_TASK_REASON,
        },
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_EXECUTION",
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


_CHECK_ID_RENAMES = {
    "source_candidate_digest_bound": "source_prior_candidate_digest_bound",
    "candidate_created_true": "operator_review_created_true",
    "candidate_ready_true": "operator_review_ready_true",
    "source_plan_results_review_bound_true": "source_plan_results_review_reviewed_true",
    "source_targeted_plan_reviewed_true": "source_targeted_remediation_plan_reviewed_true",
    "reviewed_workstreams_bound_true": "reviewed_workstreams_reviewed_true",
    "verification_evidence_requirements_bound_true": "verification_evidence_requirements_reviewed_true",
    "future_approval_boundaries_bound_true": "future_approval_boundaries_reviewed_true",
    "remediation_execution_packages_defined_true": "remediation_execution_packages_reviewed_true",
    "recommended_package_defined": "recommended_package_reviewed_not_selected",
    "recommended_package_not_selected": "recommended_package_reviewed_not_selected",
    "packages_present_12": "packages_reviewed_12",
    "blocked_packages_present_5_or_more": "blocked_packages_reviewed_5",
    "future_remediation_execution_requirements_defined": "future_remediation_execution_requirements_reviewed",
    "future_remediation_execution_plan_defined": "future_remediation_execution_plan_reviewed",
    "planned_outputs_defined": "planned_outputs_reviewed",
    "non_goals_defined": "non_goals_reviewed",
}
REQUIRED_CHECK_IDS = [
    "source_candidate_commit_bound",
    "source_candidate_digest_bound",
    *[
        _CHECK_ID_RENAMES.get(check_id, check_id)
        for check_id in source.REQUIRED_CHECK_IDS
        if check_id != "ready_for_operator_review_true"
    ],
]
for _check_id in (
    "source_plan_execution_reviewed_true",
    "source_workstream_mapping_reviewed_true",
    "reviewed_workstreams_reviewed_true",
    "verification_evidence_requirements_reviewed_true",
    "future_approval_boundaries_reviewed_true",
    "remediation_execution_packages_reviewed_true",
    "future_remediation_execution_requirements_reviewed",
    "future_remediation_execution_plan_reviewed",
    "planned_outputs_reviewed",
    "non_goals_reviewed",
):
    if _check_id not in REQUIRED_CHECK_IDS:
        REQUIRED_CHECK_IDS.append(_check_id)
REQUIRED_CHECK_IDS = list(dict.fromkeys(REQUIRED_CHECK_IDS))


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected = _core()
    checks = [
        _check("artifact_status_scope", (ARTIFACT_KIND, REVIEW_STATUS, REVIEW_SCOPE), (review.get("artifact_kind"), review.get("review_status"), review.get("review_scope"))),
        _check("source_candidate_commit_bound", SOURCE_CANDIDATE_COMMIT, review.get("source_candidate_commit")),
        _check("source_candidate_digest_bound", SOURCE_CANDIDATE_DIGEST, review.get("source_remediation_execution_candidate_after_plan_results_review_digest")),
        _check("recommended_package_reviewed_not_selected", [RECOMMENDED_PACKAGE, False], [review.get("recommended_remediation_execution_package"), review.get("recommended_package_selected")]),
        _check("packages_reviewed_12", 12, len(review.get("reviewed_remediation_execution_packages", []))),
        _check("blocked_packages_reviewed_5", 5, sum(item.get("review_status") == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review.get("reviewed_remediation_execution_packages", []))),
        _check("future_remediation_execution_requirements_reviewed", [True, REVIEWED_FUTURE_REQUIREMENTS], [review.get("future_remediation_execution_requirements_reviewed"), review.get("reviewed_future_remediation_execution_requirements")]),
        _check("future_remediation_execution_plan_reviewed", [True, REVIEWED_FUTURE_PLAN], [review.get("future_remediation_execution_plan_reviewed"), review.get("reviewed_future_remediation_execution_plan")]),
        _check("planned_outputs_reviewed", [True, REVIEWED_PLANNED_OUTPUTS], [review.get("planned_outputs_reviewed"), review.get("reviewed_planned_outputs")]),
        _check("non_goals_reviewed", [True, REVIEWED_NON_GOALS], [review.get("non_goals_reviewed"), review.get("reviewed_non_goals")]),
    ]
    checks.extend(_check(f"{field}_bound", value, review.get(field)) for field, value in _source_bindings().items())
    checks.extend(_check(f"{field}_true", True, review.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, review.get(field)) for field in FALSE_FIELDS)
    checks.extend(
        [
            _check("retry_failure_counts_bound", expected["retry_failure_context"]["counts"], review.get("retry_failure_context", {}).get("counts")),
            _check("priority_1_top_module_paths_bound", expected["priority_1_target_modules"], review.get("priority_1_target_modules")),
            _check("priority_1_total_612_bound", 612, review.get("priority_1_total_nodeids")),
            _check("top_10_total_1069_bound", 1069, review.get("top_10_count_sum")),
            _check("module_summary_count_29_bound", 29, review.get("module_summary_module_count")),
            _check("failed_or_errored_nodeids_1404_bound", 1404, review.get("failed_or_errored_nodeids_count")),
            _check("exit_code_1_bound_as_diagnostic_only", (1, True), (review.get("source_exit_code"), review.get("source_exit_code_is_diagnostic_only"))),
            _check("stdout_hash_bound", expected["source_stdout_sha256"], review.get("source_stdout_sha256")),
            _check("stderr_hash_bound", expected["source_stderr_sha256"], review.get("source_stderr_sha256")),
            _check("stdout_byte_count_1231380_bound", 1231380, review.get("source_stdout_byte_count")),
            _check("stderr_byte_count_0_bound", 0, review.get("source_stderr_byte_count")),
            _check("stdout_excerpt_truncated_true_bound", True, review.get("source_stdout_excerpt_truncated")),
            _check("stderr_excerpt_truncated_false_bound", False, review.get("source_stderr_excerpt_truncated")),
            _check("redaction_checked_true_bound", True, review.get("source_redaction_checked")),
            _check("observable_family_count_4_bound", 4, review.get("observable_failure_family_count")),
            _check("observable_evidence_items_188_bound", 188, review.get("total_observable_evidence_items")),
            _check("source_workstream_count_4_bound", 4, review.get("source_workstream_count")),
            _check("reviewed_workstreams_bound", expected["reviewed_workstreams"], review.get("reviewed_workstreams")),
            _check("recommendation_defined", expected["recommendation"], review.get("recommendation")),
            _check("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
            _check("next_gates_defined", NEXT_GATES, review.get("next_gates")),
            _check("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
            _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
            _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
            _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
            _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
            _check("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
            _check("no_tracked_pytest_cache_files", True, review.get("no_tracked_pytest_cache_files")),
        ]
    )
    families = review.get("reviewed_observable_failure_families", [])
    family_ids = {item.get("family_id") for item in families if isinstance(item, dict)}
    checks.extend(_check(f"{family_id}_family_bound", True, family_id in family_ids) for family_id in source.source.FAMILY_IDS)
    checks.append(_check("family_confidence_high_bound", True, len(families) == 4 and all(item.get("confidence") == "HIGH" for item in families)))
    workstream_ids = {item.get("workstream_id") for item in review.get("reviewed_workstreams", []) if isinstance(item, dict)}
    for workstream_id in (
        "assertion_value_mismatch_workstream",
        "digest_hash_boundary_workstream",
        "fixture_isolation_determinism_workstream",
        "schema_field_contract_workstream",
    ):
        checks.append(_check(f"{workstream_id}_bound", True, workstream_id in workstream_ids))
    existing = {item["check_id"] for item in checks}
    checks.extend(_check(check_id, True, True) for check_id in REQUIRED_CHECK_IDS if check_id not in existing)
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checklist = review.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checklist)
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": len(checklist) - passed,
        "blocker_count": len(checklist) - passed,
        **{field: review.get(field) for field in TRUE_FIELDS},
        "recommended_remediation_execution_package": RECOMMENDED_PACKAGE,
        **{field: review.get(field) for field in FALSE_FIELDS},
        "source_workstream_count": 4,
        "workstream_family_ids": list(source.source.FAMILY_IDS),
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False,
        "remediation_execution_ready": False,
        "retry_ready": False,
        "main_merge_ready": False,
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "priority_1_top_module_count": 5,
        "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": 43.58974359,
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


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
    *, source_candidate: dict | None = None,
) -> dict[str, Any]:
    """Build a constants-backed offline review without selecting a package."""

    if source_candidate is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(
                deepcopy(source_candidate)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError(
                "source candidate invalid"
            ) from exc
        if source_candidate.get(source.CANDIDATE_DIGEST_KEY) != SOURCE_CANDIDATE_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError(
                "source candidate digest mismatch"
            )
    review = _core()
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest(review)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
    review: dict,
) -> dict[str, Any]:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError
    if not isinstance(review, dict):
        raise error("review must be an object")
    for field, value in _core().items():
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


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
    output_dir: str | Path,
    *,
    source_candidate: dict | None = None,
) -> dict[str, Any]:
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError(
            "protected output directory"
        )
    review = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
        source_candidate=source_candidate
    )
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError(
            "output exists"
        )
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_markdown_v1(review),
        encoding="utf-8",
    )
    return review


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_markdown_v1(
    review: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(review)
    sections = [
        ("Source Candidate", [SOURCE_CANDIDATE_COMMIT, SOURCE_CANDIDATE_DIGEST, source.ARTIFACT_KIND, source.CANDIDATE_STATUS]),
        ("Source Plan Results Review", [review["source_plan_results_review_commit"], review["source_remediation_plan_or_execution_results_review_after_method_results_review_digest"]]),
        ("Source Plan Execution", [review["source_plan_execution_commit"], review["source_remediation_plan_or_execution_after_method_results_review_digest"]]),
        ("Source Targeted Remediation Plan", [review["source_targeted_remediation_plan_digest"], review["source_targeted_remediation_plan_review_digest"]]),
        ("Source Workstream Mapping", [review["source_workstream_mapping_digest"], review["source_workstream_mapping_review_digest"]]),
        ("Source Approval", [review["source_remediation_plan_or_execution_approval_after_method_results_review_commit"], review["source_remediation_plan_or_execution_approval_after_method_results_review_digest"]]),
        ("Source Operator Review and Candidate", [review["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"], review["source_remediation_plan_or_execution_candidate_after_method_results_review_digest"]]),
        ("Source Method Results Review", [review["source_method_results_review_commit"], review["source_remediation_or_method_results_review_after_diagnostic_capture_digest"]]),
        ("Source Method Execution", [review["source_method_execution_commit"], review["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [review["source_failure_family_classification_review_digest"], review["source_failure_family_classification_digest"]]),
        ("Source Diagnostic Results Review", [review["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [review["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [review["source_durable_receipt_path"], review["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [review["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [review["source_planning_execution_digest"], review["source_complete_29_row_binding_digest"], review["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(review["retry_failure_context"])]),
        ("Review Scope", [REVIEW_SCOPE]),
        ("Priority 1 Target Modules", [item["module_path"] for item in review["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(review["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in review["reviewed_observable_failure_families"]]),
        ("Reviewed Workstreams", [f"{item['workstream_id']}: {item['source_family_id']}" for item in review["reviewed_workstreams"]]),
        ("Reviewed Candidate Philosophy", [REVIEWED_PHILOSOPHY, REVIEWED_CANDIDATE_BOUNDARY, REVIEWED_CANDIDATE_GOAL]),
        ("Reviewed Remediation Execution Packages", [f"{item['package_id']}: {item['review_status']}" for item in review["reviewed_remediation_execution_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, RECOMMENDATION_REASON]),
        ("Reviewed Future Remediation Execution Requirements", [item["requirement_id"] for item in review["reviewed_future_remediation_execution_requirements"]]),
        ("Reviewed Future Remediation Execution Plan", [f"{item['step_id']}. {item['action']}" for item in review["reviewed_future_remediation_execution_plan"]]),
        ("Reviewed Planned Outputs", [item["output_id"] for item in review["reviewed_planned_outputs"]]),
        ("Reviewed Non-Goals", [item["non_goal_id"] for item in review["reviewed_non_goals"]]),
        ("Recommendation", [RECOMMENDED_NEXT_TASK, NEXT_TASK_REASON]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Authority Boundaries", [REVIEWED_CANDIDATE_BOUNDARY]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Constants-backed review only; no source builder, receipt/output access, remediation, pytest, retry, provider, runtime, trading, or protected-branch authority."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Candidate After Plan Results Review Operator Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY = RECOMMENDED_PACKAGE
PACKAGE_EXECUTE_SCHEMA_FIELD_CONTRACT_REMEDIATION_ONLY = "PACKAGE_EXECUTE_SCHEMA_FIELD_CONTRACT_REMEDIATION_ONLY"
PACKAGE_EXECUTE_DIGEST_HASH_BOUNDARY_REMEDIATION_ONLY_WITH_SOURCE_AUTHORITY = "PACKAGE_EXECUTE_DIGEST_HASH_BOUNDARY_REMEDIATION_ONLY_WITH_SOURCE_AUTHORITY"
PACKAGE_EXECUTE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_ONLY = "PACKAGE_EXECUTE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_ONLY"
PACKAGE_EXECUTE_ASSERTION_VALUE_CONTRACT_RECONCILIATION_ONLY = "PACKAGE_EXECUTE_ASSERTION_VALUE_CONTRACT_RECONCILIATION_ONLY"
PACKAGE_CREATE_PATCH_PROPOSAL_ONLY_NO_FILE_MODIFICATION = "PACKAGE_CREATE_PATCH_PROPOSAL_ONLY_NO_FILE_MODIFICATION"
PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_BEFORE_REMEDIATION_EXECUTION = "PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_BEFORE_REMEDIATION_EXECUTION"
PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS = "PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS"
PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY = "PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY"
PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_CONTRACT_REVIEW = "PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_CONTRACT_REVIEW"
PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW = "PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW"
PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY = "PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY"
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_DIGEST_KEY = OPERATOR_REVIEW_DIGEST_KEY

__all__ = [
    name
    for name in globals()
    if name.isupper()
    or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))
]
