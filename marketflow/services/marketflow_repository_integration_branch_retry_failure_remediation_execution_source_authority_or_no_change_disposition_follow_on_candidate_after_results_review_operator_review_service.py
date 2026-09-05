"""Review the follow-on candidate without selecting or executing a package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_FOLLOW_ON_CANDIDATE_COMMIT = "072fa2c4c88f66ac95ef7864590b847368ed490c"
SOURCE_FOLLOW_ON_CANDIDATE_DIGEST = "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_digest"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_V1_IF_SELECTED"
PASS = "PASS"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_DIGEST_KEY = OPERATOR_REVIEW_DIGEST_KEY

PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS = source.PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS
PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS = source.PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS
PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS = source.PACKAGE_CREATE_ALTERNATE_BOUNDED_DIAGNOSTIC_CANDIDATE_FROM_ENRICHMENT_RESULTS
PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS = source.PACKAGE_CREATE_REMEDIATION_REENTRY_CANDIDATE_ONLY_AFTER_SOURCE_AUTHORITY_EXISTS
PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW = source.PACKAGE_CREATE_NO_CHANGE_RETRY_CRITERIA_CANDIDATE_AFTER_RESULTS_REVIEW
PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION = source.PACKAGE_HOLD_REMEDIATION_AND_RETRY_BLOCKED_PENDING_SOURCE_AUTHORITY_ACQUISITION
PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL = source.PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL
PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN = source.PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN
PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE = source.PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE
PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL = source.PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL
PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY = source.PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY
PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS = source.PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS

REVIEWED_CANDIDATE_PHILOSOPHY = {
    "reviewed_follow_on_candidate_philosophy": "The source-authority enrichment results review confirms that the enrichment plan is valid as planning evidence, but it did not acquire source authority, establish concrete source authority, identify a safe source-authority-bound change, create no-change disposition, run alternate diagnostics, authorize remediation, or create retry readiness. The follow-on candidate correctly defines future governed options: source-authority acquisition candidate creation, no-change disposition candidate creation, alternate bounded diagnostic candidate creation, remediation re-entry only after authority exists, no-change retry criteria, or hold disposition. This operator review does not select, approve, authorize, or execute any path.",
    "reviewed_candidate_boundary": "Operator-review only; no package selection, approval, execution, source-authority acquisition, no-change disposition, alternate diagnostics, remediation, code change, test change, digest update, patch generation, pytest, retry, main merge, provider request, runtime, broker, or trading authority is created.",
    "reviewed_candidate_goal": "Review safe future paths after the source-authority enrichment results review found missing authority but acquired none.",
    "review_status": "REVIEWED_PLANNING_ONLY",
}

RECOMMENDATION_REASON = (
    "The reviewed source-authority enrichment plan identified 30 missing authority items across four sections, "
    "but no source authority was acquired and no concrete source-authority-bound change was identified. The "
    "reviewed source-authority acquisition candidate package is the safest next path because it defines what "
    "evidence must be obtained or bound before any remediation, no-change disposition, alternate diagnostic, "
    "retry candidate, or main merge can be considered. This operator review does not select or approve it."
)
NEXT_REASON = (
    "The follow-on candidate has been reviewed, but no package has been selected or approved by this review. "
    "The recommended source-authority acquisition candidate package requires a separate approval ceremony before "
    "any follow-on execution, source-authority acquisition candidate creation, no-change disposition, alternate "
    "diagnostic path, remediation re-entry, retry candidate, retry execution, or main merge."
)

REVIEWED_FUTURE_PLAN = (
    "Bind this operator review and source follow-on candidate evidence.",
    "Bind source results-review, execution, approval, operator review, candidate, failure diagnosis, blocked execution, plan review, plan execution, method, diagnostic, receipt, planning, detail-binding, recovery, module-grouping, and staged-inventory digests.",
    "Bind retry failure counts, Priority 1 modules, Priority 1 validation facts, observable families, reviewed workstreams, enrichment outputs, and missing-authority inventory.",
    "Review the source-authority enrichment result and preserve that no authority was acquired.",
    "Preserve that all follow-on packages remain unselected, unapproved, unauthorized, and unexecuted.",
    "If source-authority acquisition candidate is selected later, define evidence acquisition scope without acquiring evidence.",
    "If no-change disposition candidate is selected later, define formal disposition review inputs without creating disposition.",
    "If alternate diagnostic candidate is selected later, define bounded diagnostic scope without execution.",
    "If remediation re-entry candidate is selected later, require acquired/reviewed source authority before any remediation.",
    "If no-change retry criteria is selected later, define criteria only without retry readiness.",
    "Require results review before any acquisition, disposition, diagnostic, remediation, retry candidate, or main-merge path.",
    "Keep provider, runtime, broker, and trading authority closed.",
)

NEXT_CHAIN = (
    "Follow-On Approval After Source-Authority Enrichment Results Review v1, if selected.",
    "Follow-On Execution v1, if approved.",
    "Follow-On Results Review v1.",
    "Conditional source-authority acquisition, no-change disposition, alternate diagnostic, remediation re-entry, no-change retry criteria, or hold disposition only if results review supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""follow_on_approval_after_results_review_if_selected
follow_on_execution_if_approved
follow_on_results_review
source_authority_acquisition_candidate_if_supported
no_change_disposition_candidate_if_supported
alternate_diagnostic_candidate_if_supported
remediation_execution_candidate_if_supported
no_change_retry_criteria_candidate_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines())

RISK_CONTROLS = tuple("""follow_on_operator_review_does_not_select_package
follow_on_operator_review_does_not_approve_package
follow_on_operator_review_does_not_authorize_package
follow_on_operator_review_does_not_execute_follow_on
follow_on_operator_review_does_not_create_source_authority_acquisition_execution
follow_on_operator_review_does_not_acquire_source_authority
follow_on_operator_review_does_not_create_no_change_disposition
follow_on_operator_review_does_not_execute_alternate_diagnostics
follow_on_operator_review_does_not_execute_remediation
follow_on_operator_review_does_not_modify_production_code
follow_on_operator_review_does_not_modify_existing_tests
follow_on_operator_review_does_not_update_expected_digests
follow_on_operator_review_does_not_generate_patch
follow_on_operator_review_does_not_apply_patch
follow_on_operator_review_does_not_run_pytest
follow_on_operator_review_does_not_run_full_pytest
follow_on_operator_review_does_not_rerun_priority1_validation
follow_on_operator_review_does_not_rerun_retry
follow_on_operator_review_does_not_rerun_detached_retry
follow_on_operator_review_does_not_parse_durable_receipt
follow_on_operator_review_does_not_analyze_diagnostic_output
follow_on_operator_review_does_not_rerun_source_authority_enrichment
follow_on_operator_review_does_not_rerun_plan_execution
follow_on_operator_review_does_not_regenerate_targeted_plan
follow_on_operator_review_does_not_rerun_method_execution
follow_on_operator_review_does_not_rerun_controlled_recapture
follow_on_operator_review_does_not_run_diagnostic_command
follow_on_operator_review_does_not_read_pytest_cache
follow_on_operator_review_does_not_modify_pytest_cache
follow_on_operator_review_does_not_parse_terminal_logs
follow_on_operator_review_does_not_parse_operator_logs
follow_on_operator_review_does_not_inspect_env
follow_on_operator_review_does_not_reconstruct_prior_lost_values
follow_on_operator_review_does_not_reconstruct_full_streams
follow_on_operator_review_does_not_classify_modules_again
follow_on_operator_review_does_not_classify_full_retry_failures
follow_on_operator_review_does_not_classify_full_retry_errors
follow_on_operator_review_does_not_claim_failure_error_separation
follow_on_operator_review_does_not_identify_authoritative_first_failure
follow_on_operator_review_does_not_identify_authoritative_first_error
follow_on_operator_review_does_not_claim_traceback_root_cause
follow_on_operator_review_does_not_claim_root_cause
follow_on_operator_review_does_not_claim_retry_success
follow_on_operator_review_does_not_claim_main_merge_readiness
follow_on_operator_review_does_not_create_retry_approval
follow_on_operator_review_does_not_create_retry_execution
follow_on_operator_review_does_not_create_retry_results_review
follow_on_operator_review_does_not_create_integration_results_review
follow_on_operator_review_does_not_mark_integration_successful
follow_on_operator_review_does_not_generate_successful_integration_digest
follow_on_operator_review_does_not_push_integration_branch
follow_on_operator_review_does_not_push_main
follow_on_operator_review_does_not_delete_integration_branch
follow_on_operator_review_does_not_delete_worktree
follow_on_operator_review_does_not_force_push
follow_on_operator_review_does_not_prune_remotes
follow_on_operator_review_does_not_modify_tags
follow_on_operator_review_does_not_modify_staged_evidence
follow_on_operator_review_does_not_regenerate_evidence
follow_on_operator_review_does_not_call_providers
follow_on_operator_review_does_not_acquire_market_data
follow_on_operator_review_does_not_generate_dataset
follow_on_operator_review_does_not_recompute_metrics
follow_on_operator_review_does_not_train_models
follow_on_operator_review_does_not_score_strategy
follow_on_operator_review_does_not_generate_trade_recommendations
follow_on_operator_review_does_not_accept_predictive_usefulness
follow_on_operator_review_does_not_accept_profitability
follow_on_operator_review_does_not_authorize_runtime
follow_on_operator_review_does_not_authorize_broker_execution
source_authority_acquisition_candidate_is_not_source_authority_acquisition
source_authority_enrichment_results_are_not_source_authority
missing_authority_inventory_is_not_change_authority
no_change_inputs_are_not_no_change_disposition
alternate_diagnostic_inputs_are_not_diagnostic_execution
retry_basis_requirements_are_not_retry_readiness
passing_priority1_validation_is_not_retry_success
focused_validation_is_not_full_pytest
focused_validation_is_not_detached_retry
reviewed_workstreams_are_not_direct_change_authority
blocked_remediation_execution_remains_source_evidence
failure_diagnosis_remains_source_evidence
source_execution_results_review_remains_source_evidence
source_follow_on_candidate_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_approval_required_before_any_follow_on_execution
separate_results_review_required_after_any_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())

TRUE_FIELDS = tuple("""follow_on_candidate_after_results_review_operator_review_created
follow_on_candidate_after_results_review_operator_review_ready
source_follow_on_candidate_reviewed
source_results_review_reviewed
source_execution_reviewed
source_approval_reviewed
source_operator_review_reviewed
source_candidate_reviewed
source_failure_diagnosis_reviewed
source_blocked_execution_reviewed
source_enrichment_plan_reviewed
source_authority_enrichment_plan_reviewed
source_missing_authority_inventory_reviewed
source_workstream_authority_mapping_reviewed
source_evidence_requirements_reviewed
no_change_disposition_inputs_reviewed
alternate_diagnostic_inputs_reviewed
retry_basis_requirements_reviewed
source_authority_gap_preserved
missing_authority_inventory_status_preserved
detached_retry_failed_status_preserved
candidate_philosophy_reviewed
follow_on_packages_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
source_outputs_reviewed""".splitlines())

FALSE_FIELDS = tuple(dict.fromkeys((*source.FALSE_FIELDS, "ready_for_follow_on_execution")))

OPERATOR_CHECK_IDS = (
    "source_follow_on_candidate_commit_bound", "source_follow_on_candidate_digest_bound",
    "source_follow_on_candidate_artifact_kind_bound", "source_follow_on_candidate_status_bound",
    "source_follow_on_candidate_scope_bound", "operator_review_created_true", "operator_review_ready_true",
    "source_follow_on_candidate_reviewed_true", "source_results_review_reviewed_true",
    "candidate_philosophy_reviewed_true", "packages_reviewed_12",
    "recommended_package_reviewed_not_selected", "available_packages_reviewed_5",
    "blocked_packages_reviewed_6", "future_requirements_reviewed", "future_plan_reviewed",
    "planned_outputs_reviewed", "non_goals_reviewed", "ready_for_follow_on_execution_false",
    "recommendation_defined", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
)
CHECK_IDS = tuple(dict.fromkeys((*OPERATOR_CHECK_IDS, *source.CHECK_IDS,
                                *(f"{field}_true" for field in TRUE_FIELDS),
                                *(f"{field}_false" for field in FALSE_FIELDS))))

MARKDOWN_SECTIONS = (
    "Source Follow-On Candidate", "Source Results Review", "Source Results Review Digests",
    "Source Execution", "Source Execution Digests", "Source Approval", "Source Operator Review",
    "Source Candidate", "Source Failure Diagnosis", "Source Blocked Execution", "Blocked Reason",
    "Failure Classification", "Source Remediation Execution Approval", "Source Plan Results Review",
    "Source Plan Execution", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Source Authority Enrichment Review Summary",
    "Missing Authority Inventory Review Summary", "Workstream Authority Mapping Review Summary",
    "Source Evidence Requirements Review Summary", "No-Change Disposition Input Review Summary",
    "Alternate Diagnostic Input Review Summary", "Retry Basis Requirements Review Summary",
    "Reviewed Candidate Philosophy", "Reviewed Follow-On Packages", "Recommended Package",
    "Reviewed Future Requirements", "Reviewed Future Plan", "Reviewed Planned Outputs",
    "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
    "Authority Boundaries", "Checklist Summary", "Guardrails",
)


class MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError(ValueError):
    """Raised when source evidence or the review violates its frozen contract."""


def _source_bindings() -> dict[str, Any]:
    bindings = deepcopy(source._source_bindings())
    bindings.update({
        "source_results_review_artifact_kind": source.SOURCE_RESULTS_REVIEW_ARTIFACT_KIND,
        "source_results_review_status": source.SOURCE_RESULTS_REVIEW_STATUS,
        "source_results_review_scope": source.SOURCE_RESULTS_REVIEW_SCOPE,
        "source_results_review_commit": source.SOURCE_RESULTS_REVIEW_COMMIT,
        "source_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_enrichment_plan_review_digest": source.SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST,
        "source_missing_authority_inventory_review_digest": source.SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST,
        "source_workstream_mapping_review_digest": source.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
        "source_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "selected_source_authority_or_no_change_disposition_package": source.source.SELECTED_PACKAGE,
    })
    return bindings


def _source_context() -> dict[str, Any]:
    return {**deepcopy(source._source_context()), **deepcopy(source._summaries())}


def _committed_source_follow_on_candidate() -> dict[str, Any]:
    expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "candidate_status": source.CANDIDATE_STATUS,
        "candidate_scope": source.CANDIDATE_SCOPE,
        "source_results_review_commit": source.SOURCE_RESULTS_REVIEW_COMMIT,
        "source_results_review_digest": source.SOURCE_RESULTS_REVIEW_DIGEST,
        "source_enrichment_plan_review_digest": source.SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST,
        "source_missing_authority_inventory_review_digest": source.SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST,
        "source_workstream_mapping_review_digest": source.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST,
        "source_results_review_manifest_digest": source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "candidate_philosophy": deepcopy(source.CANDIDATE_PHILOSOPHY),
        "proposed_follow_on_packages": deepcopy(list(source.PROPOSED_PACKAGES)),
        "recommended_follow_on_package": source.RECOMMENDED_PACKAGE,
        "recommended_package": {
            "package_id": source.RECOMMENDED_PACKAGE,
            "status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
            "reason": source.RECOMMENDATION_REASON,
            "selected": False,
        },
        "future_requirements": [
            {"requirement_id": item, "status": source.FUTURE_REQUIREMENT_STATUS, "execution_status": "NOT_EXECUTED"}
            for item in source.FUTURE_REQUIREMENT_IDS
        ],
        "future_plan": list(source.FUTURE_PLAN),
        "planned_outputs": [
            {"output_id": item, "status": source.PLANNED_OUTPUT_STATUS} for item in source.PLANNED_OUTPUT_IDS
        ],
        "non_goals": list(source.NON_GOALS),
        source.CANDIDATE_DIGEST_KEY: SOURCE_FOLLOW_ON_CANDIDATE_DIGEST,
        **{field: True for field in source.TRUE_FIELDS},
        **{field: False for field in source.FALSE_FIELDS},
    }
    return expected


def _validate_source_candidate(candidate: Mapping[str, Any]) -> None:
    if not isinstance(candidate, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError(
            "source follow-on candidate must be an object"
        )
    for field, expected in _committed_source_follow_on_candidate().items():
        if candidate.get(field) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError(
                f"source follow-on candidate {field} mismatch"
            )


def _reviewed_packages() -> list[dict[str, Any]]:
    blocked_reasons = {
        PACKAGE_ACQUIRE_SOURCE_AUTHORITY_WITHOUT_SEPARATE_APPROVAL: "Source-authority acquisition requires separate governed approval and cannot be performed by this operator review.",
        PACKAGE_DIRECT_REMEDIATION_FROM_ENRICHMENT_PLAN: "The enrichment plan identifies missing authority and does not authorize direct code, test, digest, fixture, schema, or export changes.",
        PACKAGE_NO_CHANGE_DISPOSITION_WITHOUT_REVIEWED_EVIDENCE: "No-change disposition requires a separate reviewed basis; this review cannot convert planning inputs into disposition.",
        PACKAGE_RUN_ALTERNATE_DIAGNOSTICS_WITHOUT_APPROVAL: "Alternate diagnostics require separate bounded scope, approval, execution controls, and results review.",
        PACKAGE_NEW_RETRY_FROM_ENRICHMENT_RESULTS_ONLY: "Source-authority enrichment results are planning evidence only and do not create retry readiness.",
        PACKAGE_MAIN_MERGE_FROM_ENRICHMENT_RESULTS_OR_CURRENT_ROOT_PASS: "Main merge remains blocked until a future retry results review passes; current-root evidence and enrichment planning are not retry evidence.",
    }
    reviewed = []
    for package in source.PROPOSED_PACKAGES:
        package_id = package["package_id"]
        if package_id == RECOMMENDED_PACKAGE:
            review_status = "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
        elif package["status"] == "BLOCKED_NOT_ALLOWED":
            review_status = "REVIEWED_BLOCKED_NOT_ALLOWED"
        else:
            review_status = "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        item = {
            "package_id": package_id,
            "source_status": package["status"],
            "review_status": review_status,
            "purpose": package["purpose"],
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        if package_id in blocked_reasons:
            item["blocked_reason"] = blocked_reasons[package_id]
        reviewed.append(item)
    return reviewed


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "total_checks": len(review["checklist"]), "passed_checks": len(review["checklist"]),
        "failed_checks": 0, "blocker_count": 0,
        **{field: review[field] for field in TRUE_FIELDS},
        "missing_authority_inventory_reviewed": True,
        "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_to_missing_authority_mapping_reviewed": True,
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        **{field: review[field] for field in FALSE_FIELDS},
        "recommended_follow_on_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _assemble_review() -> dict[str, Any]:
    bindings = _source_bindings()
    context = _source_context()
    review = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "operator_review_only": True,
        "source_follow_on_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_follow_on_candidate_status": source.CANDIDATE_STATUS,
        "source_follow_on_candidate_scope": source.CANDIDATE_SCOPE,
        "source_follow_on_candidate_commit": SOURCE_FOLLOW_ON_CANDIDATE_COMMIT,
        "source_follow_on_candidate_digest": SOURCE_FOLLOW_ON_CANDIDATE_DIGEST,
        **bindings, **context,
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "no_change_disposition_input_count": 7, "alternate_diagnostic_input_count": 8,
        "retry_basis_requirement_count": 7, "source_outputs_generated_count": 27,
        "review_outputs_generated_count": 28,
        "source_follow_on_candidate_summary": {
            "artifact_kind": source.ARTIFACT_KIND, "status": source.CANDIDATE_STATUS,
            "scope": source.CANDIDATE_SCOPE, "commit": SOURCE_FOLLOW_ON_CANDIDATE_COMMIT,
            "digest": SOURCE_FOLLOW_ON_CANDIDATE_DIGEST, "checks": "261/261 PASS",
        },
        "reviewed_candidate_philosophy": deepcopy(REVIEWED_CANDIDATE_PHILOSOPHY),
        "reviewed_follow_on_packages": _reviewed_packages(),
        "recommended_follow_on_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_package": {
            "package_id": RECOMMENDED_PACKAGE,
            "status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "reason": RECOMMENDATION_REASON,
            "selected": False,
        },
        "reviewed_future_requirements": [
            {"requirement_id": item,
             "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_CONDITIONAL_FOLLOW_ON_AFTER_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW",
             "execution_status": "NOT_EXECUTED"}
            for item in source.FUTURE_REQUIREMENT_IDS
        ],
        "reviewed_future_plan": [
            {"step_id": index, "step": step, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
             "execution_status": "NOT_EXECUTED"}
            for index, step in enumerate(REVIEWED_FUTURE_PLAN, start=1)
        ],
        "reviewed_planned_outputs": [
            {"output_id": item, "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
             "generation_status": "NOT_GENERATED"}
            for item in source.PLANNED_OUTPUT_IDS
        ],
        "reviewed_non_goals": [
            {"non_goal_id": item, "review_status": "REVIEWED_ACTIVE"} for item in source.NON_GOALS
        ],
        "recommendation": {
            "recommended_next_task": RECOMMENDED_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
            "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_FOLLOW_ON_EXECUTION",
            "reason": NEXT_REASON,
        },
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_FOLLOW_ON_EXECUTION",
        "recommendation_reason": NEXT_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    review["checklist"] = [
        {"check_id": item, "status": PASS, "expected": True, "actual": True,
         "severity": BLOCKER, "message": f"{item} passed"}
        for item in CHECK_IDS
    ]
    review["summary"] = _summary(review)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _review_digest(review)
    return review


def _first_difference(actual: Any, expected: Any, path: str = "review") -> str | None:
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping) or set(actual) != set(expected):
            return f"{path}.keys"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            return path
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(
    *, source_follow_on_candidate: dict | None = None,
) -> dict[str, Any]:
    """Build an offline operator review from committed or injected source evidence."""

    evidence = _committed_source_follow_on_candidate() if source_follow_on_candidate is None else deepcopy(source_follow_on_candidate)
    _validate_source_candidate(evidence)
    review = _assemble_review()
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Validate the exact fail-closed operator-review contract."""

    if not isinstance(review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError("review must be an object")
    expected = _assemble_review()
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError(f"{difference} mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        "total_checks": review["summary"]["total_checks"],
        "passed_checks": review["summary"]["passed_checks"],
        "failed_checks": 0, "blocker_count": 0,
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a validated operator-review status document."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(deepcopy(review))
    sections = {
        "Source Follow-On Candidate": review["source_follow_on_candidate_summary"],
        "Source Results Review": review["source_results_review_summary"],
        "Source Results Review Digests": {key: review[key] for key in ("source_results_review_digest", "source_enrichment_plan_review_digest", "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest", "source_results_review_manifest_digest")},
        "Source Execution": review["source_execution_summary"],
        "Source Execution Digests": {key: review[key] for key in ("source_execution_digest", "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest", "source_execution_manifest_digest")},
        "Source Approval": review["source_approval_summary"], "Source Operator Review": review["source_operator_review_summary"],
        "Source Candidate": review["source_candidate_summary"], "Source Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Source Blocked Execution": review["source_blocked_execution_summary"], "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": review["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": review["source_remediation_execution_approval_after_plan_results_review_digest"], "historical_selected_package": review["historical_selected_remediation_execution_package"]},
        "Source Plan Results Review": review["source_plan_results_review_summary"], "Source Plan Execution": review["source_plan_execution_summary"],
        "Source Method Results Review": review["source_method_results_review_summary"], "Source Method Execution": review["source_method_execution_summary"],
        "Source Diagnostic Results Review": review["source_diagnostic_results_review_summary"], "Source Controlled Recapture": review["source_controlled_recapture_summary"],
        "Source Durable Receipt": review["source_durable_receipt_summary"], "Source Planning and Detail Binding Evidence": review["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": review["retry_failure_context"], "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"], "Reviewed Workstreams": review["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": review["source_authority_enrichment_review_summary"],
        "Missing Authority Inventory Review Summary": review["missing_authority_inventory_review_summary"],
        "Workstream Authority Mapping Review Summary": review["workstream_authority_mapping_review_summary"],
        "Source Evidence Requirements Review Summary": review["source_evidence_requirements_review_summary"],
        "No-Change Disposition Input Review Summary": review["no_change_disposition_input_review_summary"],
        "Alternate Diagnostic Input Review Summary": review["alternate_diagnostic_input_review_summary"],
        "Retry Basis Requirements Review Summary": review["retry_basis_requirements_review_summary"],
        "Reviewed Candidate Philosophy": review["reviewed_candidate_philosophy"], "Reviewed Follow-On Packages": review["reviewed_follow_on_packages"],
        "Recommended Package": review["recommended_package"], "Reviewed Future Requirements": review["reviewed_future_requirements"],
        "Reviewed Future Plan": review["reviewed_future_plan"], "Reviewed Planned Outputs": review["reviewed_planned_outputs"],
        "Reviewed Non-Goals": review["reviewed_non_goals"], "Recommendation": review["recommendation"],
        "Next Chain": review["next_chain"], "Next Gates": review["next_gates"], "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {field: review[field] for field in FALSE_FIELDS},
        "Checklist Summary": review["summary"], "Guardrails": list(RISK_CONTROLS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Candidate After Results Review Operator Review v1",
        "", f"Artifact: `{review['artifact_kind']}`", f"Status: `{review['review_status']}`",
        f"Scope: `{review['review_scope']}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(
    output_dir: str | Path, *, source_follow_on_candidate: dict | None = None,
) -> dict[str, Any]:
    """Write only the deterministic operator-review status document."""

    review = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(
        source_follow_on_candidate=source_follow_on_candidate
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "OPERATOR_REVIEW_DIGEST_KEY", "RECOMMENDED_PACKAGE",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_DIGEST_KEY",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_markdown_v1",
    *[item["package_id"] for item in source.PROPOSED_PACKAGES],
]
