"""Define candidate-only remediation planning options after reviewed method results."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_service
    as source,
)

ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_RESULTS_REVIEW_COMMIT = "b847470633387b7056cb2c436a674dbeab347e61"
SOURCE_RESULTS_REVIEW_DIGEST = "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"
SOURCE_CLASSIFICATION_REVIEW_DIGEST = "8ed1fabd5c06d7be6f5c86130551b09a7e3a01a9b4df9b67ae2326c2bc38f77f"
SOURCE_BOUNDED_REVIEW_DIGEST = "53ec713cc45e0c85ca94edebec8dba62b34a7403c33fe1191bf872fcfa100980"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "11e3ad0c24bd29684854b51efd13b4557d7aeab9e1e193b807a1aa3373e0f00b"
RECOMMENDED_PACKAGE = "PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_V1"
CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_digest"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

PHILOSOPHY = (
    "The method results review verified four high-confidence observable failure families from bounded diagnostic evidence: "
    "assertion_or_value_mismatch, digest_or_hash_mismatch, fixture_or_test_isolation_issue, and missing_or_unexpected_field. "
    "These families support a governed remediation-planning decision surface, but they do not establish root cause, direct "
    "remediation readiness, retry readiness, or main-merge readiness. The safest next step is to define plan-first remediation "
    "options for operator review, preserving all evidence and downstream gates."
)
CANDIDATE_BOUNDARY = (
    "Candidate-only; no package selection, approval, remediation planning execution, code remediation, evidence remediation, "
    "method rerun, diagnostic rerun, retry, results review, main merge, runtime, or trading authority is created."
)
CANDIDATE_GOAL = (
    "Define safe future remediation-plan or remediation-execution packages after reviewed method results, with a plan-first "
    "recommendation based on the four reviewed observable families."
)


def _package(package_id: str, status: str, purpose: str, *, reason: str | None = None) -> dict[str, Any]:
    item = {
        "package_id": package_id, "status": status, "purpose": purpose,
        "selected": False, "approved": False, "authorized": False, "executed": False,
    }
    if reason is not None:
        item["recommended_reason" if status.startswith("RECOMMENDED") else "blocked_reason"] = reason
    return item


PROPOSED_PACKAGES = [
    _package(RECOMMENDED_PACKAGE, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may create a remediation plan mapping the four reviewed observable families to bounded workstreams, candidate file/test areas, verification evidence, and governance controls. It must not modify code, update tests, change digests, execute remediation, run pytest, or create retry readiness.",
             reason="The method results review found four high-confidence observable families, but direct remediation readiness remains false. A targeted remediation plan is the safest next step before any code or test remediation approval."),
    _package("PACKAGE_CREATE_SCHEMA_FIELD_CONTRACT_RECONCILIATION_PLAN", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may prepare a plan for resolving missing_or_unexpected_field and artifact kind/status/scope contract mismatches, using reviewed method evidence only."),
    _package("PACKAGE_CREATE_DIGEST_AND_HASH_BOUNDARY_REVIEW_PLAN", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may prepare a plan to review digest/hash mismatch patterns, expected-digest provenance, deterministic serialization, and source-binding drift before any change."),
    _package("PACKAGE_CREATE_FIXTURE_ISOLATION_AND_DETERMINISM_REMEDIATION_PLAN", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may prepare a plan to review fixture isolation, shared constants, deterministic timestamps, injected evidence, and test pollution risks."),
    _package("PACKAGE_CREATE_ASSERTION_VALUE_MISMATCH_TRIAGE_PLAN", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may prepare a triage plan for assertion_or_value_mismatch patterns, including expected/actual grouping and source-of-truth checks, without changing assertions."),
    _package("PACKAGE_REQUEST_ADDITIONAL_BOUNDED_DIAGNOSTIC_CAPTURE_IF_PLAN_CANNOT_BE_SUPPORTED", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
             "Future execution may recommend separately governed additional diagnostic capture only if remediation planning cannot be supported by reviewed method evidence."),
    _package("PACKAGE_DIRECT_CODE_REMEDIATION_FROM_FAMILY_LABELS", "BLOCKED_NOT_ALLOWED",
             "Direct code remediation from family labels is prohibited.", reason="Reviewed family labels are planning evidence only and do not prove root cause or safe code-change scope."),
    _package("PACKAGE_UPDATE_DIGESTS_OR_EXPECTED_VALUES_WITHOUT_SOURCE_AUTHORITY", "BLOCKED_NOT_ALLOWED",
             "Blind expected-value updates are prohibited.", reason="Digest/hash mismatches must not be fixed by blindly updating expected values without source authority and review."),
    _package("PACKAGE_REWRITE_TESTS_TO_PASS_WITHOUT_ARTIFACT_REVIEW", "BLOCKED_NOT_ALLOWED",
             "Unreviewed test rewriting is prohibited.", reason="Test changes without artifact contract review could mask real governance or evidence-binding failures."),
    _package("PACKAGE_EXECUTE_REMEDIATION_NOW_WITHOUT_APPROVAL", "BLOCKED_NOT_ALLOWED",
             "Unapproved remediation is prohibited.", reason="Remediation execution requires separate operator review, approval, execution, and results review."),
    _package("PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_RESULTS_REVIEW", "BLOCKED_NOT_ALLOWED",
             "A premature retry is prohibited.", reason="A new retry remains blocked until remediation planning or execution is approved, completed, and reviewed."),
    _package("PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY", "BLOCKED_NOT_ALLOWED",
             "Main merge remains prohibited.", reason="Main merge remains blocked until a future retry results review passes."),
]

FUTURE_REQUIREMENT_IDS = """source_method_results_review_must_be_ready
source_method_results_review_digest_must_be_bound
source_classification_review_digest_must_be_bound
source_bounded_excerpt_review_digest_must_be_bound
source_results_review_manifest_digest_must_be_bound
source_method_execution_digest_must_be_bound
source_failure_family_classification_digest_must_be_bound
source_bounded_excerpt_analysis_digest_must_be_bound
source_method_execution_manifest_digest_must_be_bound
source_approval_digest_must_be_bound
source_operator_review_digest_must_be_bound
source_candidate_digest_must_be_bound
source_diagnostic_results_review_digests_must_be_bound
source_controlled_recapture_digests_must_be_bound
source_durable_receipt_path_must_be_bound
retry_failure_counts_must_be_bound
priority_1_top_module_paths_must_be_bound
priority_1_total_must_be_612
top_10_total_must_be_1069
module_summary_total_must_be_29
failed_or_errored_nodeids_total_must_be_1404
observable_family_count_must_be_4
observable_evidence_items_must_be_188
assertion_or_value_mismatch_family_must_be_bound
digest_or_hash_mismatch_family_must_be_bound
fixture_or_test_isolation_issue_family_must_be_bound
missing_or_unexpected_field_family_must_be_bound
family_confidence_must_remain_reviewed_high
future_remediation_plan_must_not_claim_root_cause
future_remediation_plan_must_not_claim_first_failure
future_remediation_plan_must_not_claim_full_retry_failure_error_separation
future_remediation_plan_must_not_recommend_direct_code_changes_without_results_review
future_remediation_execution_requires_separate_approval
future_code_change_requires_separate_approval
future_test_change_requires_separate_approval
future_digest_update_requires_source_authority_and_review
future_remediation_results_review_required_before_retry_candidate
future_retry_requires_separate_candidate_approval_execution_and_review
main_merge_requires_passing_retry_results_review
runtime_and_trading_remain_not_authorized""".splitlines()
FUTURE_REQUIREMENTS = [
    {"requirement_id": item, "required": True,
     "status": "REQUIRED_FOR_FUTURE_REMEDIATION_PLAN_OR_EXECUTION", "execution_status": "NOT_EXECUTED"}
    for item in FUTURE_REQUIREMENT_IDS
]

FUTURE_PLAN_ACTIONS = [
    "Bind this candidate and the source method results-review evidence.",
    "Bind method execution, classification, bounded-excerpt, and manifest digests.",
    "Bind diagnostic capture, durable receipt, planning, detail-binding, recovery, and staged-inventory digests.",
    "Bind retry failure counts and Priority 1 module facts.",
    "Bind the four reviewed observable families and their evidence counts.",
    "Select one remediation plan or execution package.",
    "If the recommended plan-first package is selected, create only a targeted remediation plan.",
    "Map assertion/value mismatch, digest/hash mismatch, fixture/isolation, and missing/unexpected-field families to controlled workstreams.",
    "Preserve that family classification is not root cause, not direct remediation approval, and not retry evidence.",
    "Define verification evidence needed before any remediation execution or code/test change.",
    "Require remediation plan or execution results review before a new retry candidate.",
    "Keep retry, main merge, runtime, broker, and trading closed.",
]
FUTURE_PLAN = [
    {"step": index, "action": action, "status": "PLANNED_NOT_EXECUTED"}
    for index, action in enumerate(FUTURE_PLAN_ACTIONS, start=1)
]

PLANNED_OUTPUT_IDS = """remediation_plan_or_execution_candidate_after_method_results_review_manifest
source_method_results_review_binding_report
source_method_execution_binding_report
observable_failure_family_summary_report
remediation_package_comparison_report
recommended_targeted_remediation_plan_package_report
assertion_value_mismatch_workstream_placeholder
digest_hash_mismatch_workstream_placeholder
fixture_isolation_workstream_placeholder
missing_unexpected_field_workstream_placeholder
future_remediation_requirements_report
future_remediation_plan_report
verification_evidence_requirements_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
PLANNED_OUTPUTS = [{"output_id": item, "status": "PLANNED_NOT_GENERATED"} for item in PLANNED_OUTPUT_IDS]

NON_GOALS = """do_not_select_remediation_package_now
do_not_approve_remediation_package_now
do_not_authorize_remediation_package_now
do_not_execute_remediation_plan_now
do_not_execute_remediation_now
do_not_modify_production_code_now
do_not_modify_existing_tests_now
do_not_update_expected_digests_now
do_not_parse_durable_receipt_now
do_not_analyze_diagnostic_output_now
do_not_rerun_method_execution_now
do_not_rerun_controlled_recapture_now
do_not_run_diagnostic_command_now
do_not_run_targeted_pytest_now
do_not_run_full_pytest_now
do_not_rerun_retry_now
do_not_read_cache_now
do_not_modify_cache_now
do_not_parse_terminal_logs_now
do_not_parse_operator_logs_now
do_not_inspect_env_now
do_not_reconstruct_prior_lost_values_now
do_not_reconstruct_full_stdout_or_stderr_now
do_not_classify_modules_again_now
do_not_classify_full_retry_failures_now
do_not_classify_full_retry_errors_now
do_not_claim_failure_error_separation_now
do_not_identify_first_failure_now
do_not_identify_first_error_now
do_not_claim_traceback_root_cause_now
do_not_claim_root_cause_now
do_not_recommend_direct_code_remediation_now
do_not_create_remediation_approval_now
do_not_create_remediation_execution_now
do_not_create_remediation_results_review_now
do_not_create_new_retry_candidate_now
do_not_create_retry_results_review_now
do_not_create_integration_results_review_now
do_not_mark_integration_successful
do_not_push_integration_branch
do_not_push_main
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_call_providers
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_trading""".splitlines()

NEXT_CHAIN = [
    "Remediation Plan or Execution Candidate After Method Results Review Operator Review v1.",
    "Remediation Plan or Execution Approval v1, if selected.", "Remediation Plan or Execution v1, if approved.",
    "Remediation Plan or Execution Results Review v1.",
    "New Integration Branch Retry Candidate v1, only after remediation results review.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
]
NEXT_GATES = """remediation_plan_or_execution_candidate_after_method_results_review_operator_review
remediation_plan_or_execution_approval_if_selected
remediation_plan_or_execution_if_approved
remediation_plan_or_execution_results_review
new_integration_branch_retry_candidate_after_remediation_results_review
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()

RISK_CONTROLS = """candidate_after_method_results_review_does_not_select_package
candidate_after_method_results_review_does_not_approve_package
candidate_after_method_results_review_does_not_authorize_package
candidate_after_method_results_review_does_not_execute_remediation_plan
candidate_after_method_results_review_does_not_execute_remediation
candidate_after_method_results_review_does_not_modify_production_code
candidate_after_method_results_review_does_not_modify_existing_tests
candidate_after_method_results_review_does_not_update_expected_digests
candidate_after_method_results_review_does_not_parse_durable_receipt
candidate_after_method_results_review_does_not_analyze_diagnostic_output
candidate_after_method_results_review_does_not_rerun_method_execution
candidate_after_method_results_review_does_not_rerun_controlled_recapture
candidate_after_method_results_review_does_not_run_diagnostic_command
candidate_after_method_results_review_does_not_run_targeted_pytest
candidate_after_method_results_review_does_not_run_full_pytest
candidate_after_method_results_review_does_not_rerun_retry
candidate_after_method_results_review_does_not_read_pytest_cache
candidate_after_method_results_review_does_not_modify_pytest_cache
candidate_after_method_results_review_does_not_parse_terminal_logs
candidate_after_method_results_review_does_not_parse_operator_logs
candidate_after_method_results_review_does_not_inspect_env
candidate_after_method_results_review_does_not_reconstruct_prior_lost_values
candidate_after_method_results_review_does_not_reconstruct_full_streams
candidate_after_method_results_review_does_not_classify_modules_again
candidate_after_method_results_review_does_not_classify_full_retry_failures
candidate_after_method_results_review_does_not_classify_full_retry_errors
candidate_after_method_results_review_does_not_claim_failure_error_separation
candidate_after_method_results_review_does_not_identify_authoritative_first_failure
candidate_after_method_results_review_does_not_identify_authoritative_first_error
candidate_after_method_results_review_does_not_claim_traceback_root_cause
candidate_after_method_results_review_does_not_claim_root_cause
candidate_after_method_results_review_does_not_recommend_direct_code_remediation
candidate_after_method_results_review_does_not_create_remediation_approval
candidate_after_method_results_review_does_not_create_remediation_execution
candidate_after_method_results_review_does_not_create_remediation_results_review
candidate_after_method_results_review_does_not_create_new_retry_candidate
candidate_after_method_results_review_does_not_create_retry_results_review
candidate_after_method_results_review_does_not_create_integration_results_review
candidate_after_method_results_review_does_not_mark_integration_successful
candidate_after_method_results_review_does_not_generate_successful_integration_digest
candidate_after_method_results_review_does_not_treat_method_analysis_as_retry_success
candidate_after_method_results_review_does_not_treat_family_classification_as_root_cause
candidate_after_method_results_review_does_not_push_integration_branch
candidate_after_method_results_review_does_not_push_main
candidate_after_method_results_review_does_not_delete_integration_branch
candidate_after_method_results_review_does_not_delete_worktree
candidate_after_method_results_review_does_not_force_push
candidate_after_method_results_review_does_not_prune_remotes
candidate_after_method_results_review_does_not_modify_tags
candidate_after_method_results_review_does_not_modify_staged_evidence
candidate_after_method_results_review_does_not_regenerate_evidence
candidate_after_method_results_review_does_not_call_providers
candidate_after_method_results_review_does_not_acquire_market_data
candidate_after_method_results_review_does_not_regenerate_dataset
candidate_after_method_results_review_does_not_recompute_metrics
candidate_after_method_results_review_does_not_train_models
candidate_after_method_results_review_does_not_score_strategy
candidate_after_method_results_review_does_not_generate_recommendations
candidate_after_method_results_review_does_not_accept_predictive_usefulness
candidate_after_method_results_review_does_not_accept_profitability
candidate_after_method_results_review_does_not_authorize_runtime
candidate_after_method_results_review_does_not_authorize_broker_execution
method_results_review_remains_source_evidence
observable_failure_family_classification_is_method_planning_only
failure_family_classification_is_not_root_cause
failure_family_classification_is_not_direct_remediation
failure_family_classification_is_not_retry_success
direct_remediation_ready_remains_false
retry_ready_remains_false
main_merge_ready_remains_false
diagnostic_capture_results_review_remains_source_evidence
durable_receipt_is_diagnostic_evidence_only
controlled_recapture_is_not_retry_success
priority_1_selection_is_not_root_cause
module_concentration_is_not_failure_error_separation
prior_blocked_diagnostic_capture_execution_remains_historically_blocked
previous_method_execution_remains_source_evidence
previous_remediation_or_method_approval_remains_source_evidence
previous_receipt_recovery_or_recapture_results_review_remains_source_evidence
previous_planning_results_review_remains_valid
previous_detail_binding_results_review_remains_valid
previous_materialization_results_review_remains_valid
previous_source_recovery_results_review_remains_valid
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_operator_review_required_before_remediation_approval
separate_approval_required_before_remediation_plan_or_execution
separate_results_review_required_after_remediation_plan_or_execution
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines()

TRUE_FIELDS = """remediation_plan_or_execution_candidate_after_method_results_review_created
remediation_plan_or_execution_candidate_after_method_results_review_ready_for_operator_review
source_method_results_review_bound
source_method_execution_results_reviewed
observable_failure_families_bound
family_classification_evidence_available_for_future_remediation_planning
remediation_plan_or_execution_packages_defined
future_remediation_requirements_defined
future_remediation_plan_defined
ready_for_remediation_plan_or_execution_candidate_operator_review""".splitlines()
FALSE_FIELDS = """remediation_plan_or_execution_package_selected
remediation_plan_or_execution_package_approved
remediation_plan_or_execution_package_authorized
remediation_plan_or_execution_performed
remediation_plan_generated
remediation_execution_performed
code_remediation_executed
evidence_remediation_executed
method_execution_rerun_performed
diagnostic_receipt_parsed_in_candidate
diagnostic_output_analyzed_in_candidate
failure_family_classification_performed_in_candidate
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
targeted_pytest_performed_in_candidate
full_pytest_performed
retry_rerun_performed
cache_read_in_candidate
cache_modified_in_candidate
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
provider_requests_made_in_candidate
market_data_acquisition_performed_in_candidate
dataset_generation_performed_in_candidate
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError(ValueError):
    """Raised when candidate evidence, inventory, or closed authority changes."""


def _source_bindings() -> dict[str, Any]:
    inherited = source._source_bindings()
    return {
        **inherited,
        "source_method_results_review_artifact_kind": source.ARTIFACT_KIND,
        "source_method_results_review_status": source.REVIEW_STATUS,
        "source_method_results_review_scope": source.REVIEW_SCOPE,
        "source_method_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_failure_family_classification_review_digest": SOURCE_CLASSIFICATION_REVIEW_DIGEST,
        "source_bounded_excerpt_analysis_review_digest": SOURCE_BOUNDED_REVIEW_DIGEST,
        "source_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_method_execution_commit": source.SOURCE_EXECUTION_COMMIT,
        "source_method_execution_manifest_digest": source.SOURCE_EXECUTION_MANIFEST_DIGEST,
    }


def _core() -> dict[str, Any]:
    bindings = _source_bindings()
    families = deepcopy(source.OBSERVABLE_FAMILY_REVIEWS)
    return {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True, "governance_only": True, "candidate_only": True,
        "operator_review_required": True, **bindings,
        "selected_source_method_package": source.SELECTED_PACKAGE,
        "retry_execution_commit": source.source.approval_source.source.RETRY_EXECUTION_COMMIT,
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
                                  "first_result_authoritative": True, "pytest_passed": False,
                                  "pytest_failed": True, "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": deepcopy(source.source.approval_source.source.PRIORITY_1_TARGET_MODULES),
        "priority_1_total_nodeids": 612, "top_10_count_sum": 1069,
        "module_summary_module_count": 29, "failed_or_errored_nodeids_count": 1404,
        "source_exit_code": 1, "source_duration_seconds": "21.584361",
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "source_combined_output_byte_count": 1231380,
        "source_stdout_sha256": source.source.approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"],
        "source_stderr_sha256": source.source.approval_source.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"],
        "source_stdout_excerpt_truncated": True, "source_stderr_excerpt_truncated": False,
        "source_redaction_checked": True, "source_exit_code_is_diagnostic_only": True,
        "source_method_results_review_summary": {
            "review_digest": SOURCE_RESULTS_REVIEW_DIGEST, "ready": True,
            "candidate_readiness_only": True, "direct_remediation_ready": False,
            "retry_ready": False, "main_merge_ready": False,
        },
        "source_method_execution_summary": deepcopy(source._core()["source_method_execution_summary"]),
        "source_failure_family_classification_summary": deepcopy(source._core()["source_failure_family_classification_summary"]),
        "source_bounded_excerpt_analysis_summary": deepcopy(source._core()["source_bounded_excerpt_analysis_summary"]),
        "source_diagnostic_results_review_summary": deepcopy(source._core()["source_diagnostic_results_review_summary"]),
        "source_controlled_recapture_execution_summary": deepcopy(source._core()["source_controlled_recapture_execution_summary"]),
        "source_durable_receipt_summary": deepcopy(source._core()["source_durable_receipt_summary"]),
        "source_receipt_loss_history_summary": deepcopy(source._core()["source_receipt_loss_history_summary"]),
        "source_planning_and_detail_binding_summary": deepcopy(source._core()["source_planning_and_detail_binding_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(source._core()["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": families,
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.FAMILY_IDS),
        "additional_diagnostic_capture_may_be_needed": False, "direct_remediation_ready": False,
        "retry_ready": False, "main_merge_ready": False,
        "remediation_plan_or_execution_candidate_after_method_results_review_philosophy": PHILOSOPHY,
        "candidate_philosophy": {"philosophy": PHILOSOPHY, "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL},
        "candidate_boundary": CANDIDATE_BOUNDARY, "candidate_goal": CANDIDATE_GOAL,
        "proposed_remediation_plan_or_execution_packages": deepcopy(PROPOSED_PACKAGES),
        "recommended_remediation_plan_or_execution_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "recommended_package_selected": False,
        "recommended_package": deepcopy(PROPOSED_PACKAGES[0]),
        "recommendation_reason": "The method results review identified four high-confidence observable failure families but explicitly preserved direct_remediation_ready=false, retry_ready=false, and main_merge_ready=false. A plan-first package can convert the reviewed bounded method evidence into controlled remediation workstreams without prematurely modifying code, updating tests, running pytest, or creating retry readiness.",
        "future_remediation_requirements": deepcopy(FUTURE_REQUIREMENTS),
        "future_remediation_plan": deepcopy(FUTURE_PLAN), "future_remediation_plan_status": "PLANNED_NOT_EXECUTED",
        "planned_outputs": deepcopy(PLANNED_OUTPUTS), "non_goals": list(NON_GOALS),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual),
            "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


SOURCE_CHECK_FIELDS = {
    "source_method_results_review_commit_bound": "source_method_results_review_commit",
    "source_method_results_review_digest_bound": "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
    "source_failure_family_classification_review_digest_bound": "source_failure_family_classification_review_digest",
    "source_bounded_excerpt_analysis_review_digest_bound": "source_bounded_excerpt_analysis_review_digest",
    "source_results_review_manifest_digest_bound": "source_results_review_manifest_digest",
    "source_method_execution_commit_bound": "source_method_execution_commit",
    "source_method_execution_digest_bound": "source_remediation_or_method_execution_after_diagnostic_capture_digest",
    "source_failure_family_classification_digest_bound": "source_failure_family_classification_digest",
    "source_bounded_excerpt_analysis_digest_bound": "source_bounded_excerpt_analysis_digest",
    "source_method_execution_manifest_digest_bound": "source_method_execution_manifest_digest",
    "source_approval_digest_bound": "source_remediation_or_method_approval_after_diagnostic_capture_digest",
    "source_operator_review_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
    "source_candidate_digest_bound": "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
    "source_diagnostic_results_review_digest_bound": "source_receipt_recovery_or_recapture_results_review_digest",
    "source_payload_review_digest_bound": "source_receipt_recovery_or_recapture_payload_review_digest",
    "source_durable_receipt_review_digest_bound": "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
    "source_diagnostic_results_review_manifest_digest_bound": "source_receipt_recovery_or_recapture_results_review_manifest_digest",
    "source_controlled_recapture_execution_commit_bound": "source_receipt_recovery_or_recapture_execution_commit",
    "source_controlled_recapture_execution_digest_bound": "source_receipt_recovery_or_recapture_execution_digest",
    "source_controlled_recapture_payload_digest_bound": "source_receipt_recovery_or_recapture_payload_digest",
    "source_controlled_recapture_receipt_digest_bound": "source_receipt_recovery_or_recapture_receipt_digest",
    "source_controlled_recapture_manifest_digest_bound": "source_receipt_recovery_or_recapture_digest_manifest_digest",
    "source_durable_receipt_path_bound": "source_durable_receipt_path",
    "source_receipt_recovery_approval_digest_bound": "source_receipt_recovery_or_recapture_approval_digest",
    "source_receipt_recovery_candidate_operator_review_digest_bound": "source_receipt_recovery_or_recapture_candidate_operator_review_digest",
    "source_receipt_recovery_candidate_digest_bound": "source_receipt_recovery_or_recapture_candidate_digest",
    "source_failure_diagnosis_digest_bound": "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
    "source_prior_execution_digest_bound": "source_targeted_diagnostic_output_capture_execution_digest",
    "source_blocked_manifest_digest_bound": "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest",
    "source_blocked_reason_bound": "source_targeted_diagnostic_output_capture_execution_blocked_reason",
    "source_primary_failure_class_bound": "source_primary_failure_class", "source_secondary_failure_class_bound": "source_secondary_failure_class",
    "source_targeted_diagnostic_approval_digest_bound": "source_targeted_diagnostic_output_capture_approval_digest",
    "source_targeted_diagnostic_candidate_operator_review_digest_bound": "source_targeted_diagnostic_output_capture_candidate_operator_review_digest",
    "source_targeted_diagnostic_candidate_digest_bound": "source_targeted_diagnostic_output_capture_candidate_digest",
    "source_planning_results_review_digest_bound": "source_planning_results_review_digest",
    "source_prioritized_planning_review_digest_bound": "source_prioritized_planning_review_digest",
    "source_planning_execution_digest_bound": "source_planning_execution_digest",
    "source_prioritized_planning_digest_bound": "source_prioritized_planning_digest",
    "source_detail_binding_results_review_digest_bound": "source_detail_binding_results_review_digest",
    "source_complete_29_row_binding_digest_bound": "source_complete_29_row_binding_digest",
    "source_materialized_payload_digest_bound": "source_materialized_payload_digest",
    "source_recovery_results_review_digest_bound": "source_recovery_results_review_digest",
    "source_recovery_detail_digest_bound": "source_recovery_detail_digest",
    "source_after_v2_approval_digest_bound": "source_after_v2_approval_digest",
    "source_module_grouping_digest_bound": "source_module_grouping_digest",
}

FALSE_CHECK_FIELDS = {
    "remediation_plan_or_execution_package_selected_false": "remediation_plan_or_execution_package_selected",
    "remediation_plan_or_execution_package_approved_false": "remediation_plan_or_execution_package_approved",
    "remediation_plan_or_execution_package_authorized_false": "remediation_plan_or_execution_package_authorized",
    "remediation_plan_or_execution_performed_false": "remediation_plan_or_execution_performed",
    "remediation_plan_generated_false": "remediation_plan_generated", "remediation_execution_false": "remediation_execution_performed",
    "code_remediation_false": "code_remediation_executed", "evidence_remediation_false": "evidence_remediation_executed",
    "method_execution_rerun_false": "method_execution_rerun_performed", "diagnostic_receipt_parsed_false": "diagnostic_receipt_parsed_in_candidate",
    "diagnostic_output_analyzed_false": "diagnostic_output_analyzed_in_candidate",
    "failure_family_classification_performed_in_candidate_false": "failure_family_classification_performed_in_candidate",
    "controlled_recapture_rerun_false": "controlled_recapture_rerun_performed", "diagnostic_command_rerun_false": "diagnostic_command_rerun_performed",
    "targeted_pytest_in_candidate_false": "targeted_pytest_performed_in_candidate", "full_pytest_false": "full_pytest_performed",
    "retry_rerun_false": "retry_rerun_performed", "cache_read_false": "cache_read_in_candidate", "cache_modified_false": "cache_modified_in_candidate",
    "pytest_cache_committed_false": "pytest_cache_committed", "marketflow_outputs_committed_false": "marketflow_outputs_committed",
    "terminal_logs_parsed_false": "terminal_logs_parsed", "operator_logs_parsed_false": "operator_logs_parsed",
    "env_inspection_false": "env_inspection_performed", "prior_lost_values_reconstructed_false": "prior_lost_values_reconstructed",
    "full_stdout_reconstructed_false": "full_stdout_reconstructed", "full_stderr_reconstructed_false": "full_stderr_reconstructed",
    "failure_modules_classified_false": "failure_modules_classified", "error_modules_classified_false": "error_modules_classified",
    "failure_error_separation_claimed_false": "failure_error_separation_claimed", "first_failure_identified_false": "first_failure_identified",
    "first_error_identified_false": "first_error_identified", "first_order_claim_made_false": "first_order_claim_made",
    "traceback_root_cause_claimed_false": "traceback_root_cause_claimed", "root_cause_claimed_false": "root_cause_claimed",
    "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
    "new_retry_candidate_created_false": "new_retry_candidate_created", "new_retry_executed_false": "new_retry_executed",
    "new_retry_results_review_created_false": "new_retry_results_review_created", "main_merge_approval_created_false": "main_merge_approval_created",
    "ready_for_remediation_plan_or_execution_approval_false": "ready_for_remediation_plan_or_execution_approval",
    "ready_for_remediation_plan_or_execution_execution_false": "ready_for_remediation_plan_or_execution_execution",
    "ready_for_remediation_execution_false": "ready_for_remediation_execution", "ready_for_retry_candidate_false": "ready_for_retry_candidate",
    "ready_for_main_merge_approval_false": "ready_for_main_merge_approval", "integration_success_false": "integration_execution_successful",
    "successful_integration_digest_false": "successful_integration_execution_digest_generated",
    "integration_branch_pushed_false": "integration_branch_pushed", "main_push_false": "main_push_performed",
    "origin_main_modified_false": "origin_main_modified_by_this_task", "evidence_regenerated_false": "evidence_regenerated",
    "provider_requests_false": "provider_requests_made_in_candidate", "market_data_acquisition_false": "market_data_acquisition_performed_in_candidate",
    "dataset_generation_false": "dataset_generation_performed_in_candidate", "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
    "model_training_false": "model_training_performed", "strategy_scoring_false": "strategy_scoring_performed",
    "recommendations_false": "trade_recommendations_generated",
}


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected = _core()
    checks = [_check(check_id, expected[field], candidate.get(field)) for check_id, field in SOURCE_CHECK_FIELDS.items()]
    checks += [
        _check("retry_execution_commit_bound", expected["retry_execution_commit"], candidate.get("retry_execution_commit")),
        _check("retry_failure_counts_bound", expected["retry_failure_context"]["counts"], candidate.get("retry_failure_context", {}).get("counts")),
        _check("priority_1_top_module_paths_bound", expected["priority_1_target_modules"], candidate.get("priority_1_target_modules")),
        _check("priority_1_total_612_bound", 612, candidate.get("priority_1_total_nodeids")), _check("top_10_total_1069_bound", 1069, candidate.get("top_10_count_sum")),
        _check("module_summary_count_29_bound", 29, candidate.get("module_summary_module_count")), _check("failed_or_errored_nodeids_1404_bound", 1404, candidate.get("failed_or_errored_nodeids_count")),
        _check("exit_code_1_bound_as_diagnostic_only", [1, True], [candidate.get("source_exit_code"), candidate.get("source_exit_code_is_diagnostic_only")]),
        _check("stdout_hash_bound", expected["source_stdout_sha256"], candidate.get("source_stdout_sha256")), _check("stderr_hash_bound", expected["source_stderr_sha256"], candidate.get("source_stderr_sha256")),
        _check("stdout_byte_count_1231380_bound", 1231380, candidate.get("source_stdout_byte_count")), _check("stderr_byte_count_0_bound", 0, candidate.get("source_stderr_byte_count")),
        _check("stdout_excerpt_truncated_true_bound", True, candidate.get("source_stdout_excerpt_truncated")), _check("stderr_excerpt_truncated_false_bound", False, candidate.get("source_stderr_excerpt_truncated")),
        _check("redaction_checked_true_bound", True, candidate.get("source_redaction_checked")),
        _check("observable_family_count_4_bound", 4, candidate.get("observable_failure_family_count")), _check("observable_evidence_items_188_bound", 188, candidate.get("total_observable_evidence_items")),
    ]
    families = candidate.get("reviewed_observable_failure_families", [])
    family_ids = {item.get("family_id") for item in families if isinstance(item, dict)}
    checks.extend(_check(f"{family_id}_family_bound", True, family_id in family_ids) for family_id in source.FAMILY_IDS)
    checks += [
        _check("family_confidence_high_bound", True, len(families) == 4 and all(item.get("confidence") == "HIGH" for item in families)),
        _check("additional_diagnostic_capture_false_bound", False, candidate.get("additional_diagnostic_capture_may_be_needed")),
        _check("direct_remediation_ready_false_bound", False, candidate.get("direct_remediation_ready")), _check("retry_ready_false_bound", False, candidate.get("retry_ready")),
        _check("main_merge_ready_false_bound", False, candidate.get("main_merge_ready")),
        _check("candidate_created_true", True, candidate.get("remediation_plan_or_execution_candidate_after_method_results_review_created")),
        _check("candidate_ready_true", True, candidate.get("remediation_plan_or_execution_candidate_after_method_results_review_ready_for_operator_review")),
        _check("source_method_results_review_bound_true", True, candidate.get("source_method_results_review_bound")),
        _check("observable_failure_families_bound_true", True, candidate.get("observable_failure_families_bound")),
        _check("remediation_plan_or_execution_packages_defined_true", True, candidate.get("remediation_plan_or_execution_packages_defined")),
        _check("recommended_package_defined", RECOMMENDED_PACKAGE, candidate.get("recommended_remediation_plan_or_execution_package")),
        _check("recommended_package_not_selected", False, candidate.get("recommended_package_selected")),
        _check("packages_present_12", 12, len(candidate.get("proposed_remediation_plan_or_execution_packages", []))),
        _check("blocked_packages_present_6", 6, sum(item.get("status") == "BLOCKED_NOT_ALLOWED" for item in candidate.get("proposed_remediation_plan_or_execution_packages", []))),
        _check("future_remediation_requirements_defined", FUTURE_REQUIREMENTS, candidate.get("future_remediation_requirements")),
        _check("future_remediation_plan_defined", FUTURE_PLAN, candidate.get("future_remediation_plan")),
        _check("planned_outputs_defined", PLANNED_OUTPUTS, candidate.get("planned_outputs")),
        _check("non_goals_defined", NON_GOALS, candidate.get("non_goals")),
    ]
    checks.extend(_check(check_id, False, candidate.get(field)) for check_id, field in FALSE_CHECK_FIELDS.items())
    checks += [
        _check("ready_for_operator_review_true", True, candidate.get("ready_for_remediation_plan_or_execution_candidate_operator_review")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")), _check("runtime_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("recommendation_defined", expected["recommendation_reason"], candidate.get("recommendation_reason")),
        _check("next_chain_defined", NEXT_CHAIN, candidate.get("next_chain")), _check("next_gates_defined", NEXT_GATES, candidate.get("next_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("no_tracked_marketflow_files", True, candidate.get("no_tracked_marketflow_files")), _check("no_tracked_pytest_cache_files", True, candidate.get("no_tracked_pytest_cache_files")),
    ]
    return checks


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    checks = candidate.get("checklist", [])
    passed = sum(item.get("status") == PASS for item in checks)
    return {
        "total_checks": len(checks), "passed_checks": passed, "failed_checks": len(checks) - passed, "blocker_count": len(checks) - passed,
        **{field: candidate.get(field) for field in TRUE_FIELDS},
        "recommended_remediation_plan_or_execution_package": RECOMMENDED_PACKAGE, "recommended_package_selected": False,
        **{field: candidate.get(field) for field in FALSE_FIELDS},
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "highest_confidence_family_ids": list(source.FAMILY_IDS), "additional_diagnostic_capture_may_be_needed": False,
        "direct_remediation_ready": False, "retry_ready": False, "main_merge_ready": False,
        "source_exit_code": 1, "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29, "priority_1_top_module_count": 5,
        "priority_1_total_nodeids": 612, "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _digest(candidate: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(candidate))
    for field in ("checklist", "summary", CANDIDATE_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
    *, source_method_results_review: dict | None = None,
) -> dict:
    """Build a plan-first candidate without selecting or executing any package."""

    if source_method_results_review is not None:
        try:
            source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
                deepcopy(source_method_results_review)
            )
        except source.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError as exc:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError(
                "source method results review invalid"
            ) from exc
        if source_method_results_review.get(source.RESULTS_REVIEW_DIGEST_KEY) != SOURCE_RESULTS_REVIEW_DIGEST:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError(
                "source method results review digest mismatch"
            )
    candidate = _core()
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    candidate[CANDIDATE_DIGEST_KEY] = _digest(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
    candidate: dict,
) -> dict:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError
    if not isinstance(candidate, dict):
        raise error("candidate must be an object")
    expected = _core()
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise error(f"{field} mismatch")
    if candidate.get(CANDIDATE_DIGEST_KEY) != _digest(candidate):
        raise error("candidate digest mismatch")
    checklist = _checklist(candidate)
    if candidate.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if candidate.get("summary") != _summary(candidate):
        raise error("summary mismatch")
    return {"artifact_kind": ARTIFACT_KIND, "candidate_status": CANDIDATE_STATUS, "candidate_scope": CANDIDATE_SCOPE,
            "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
            **{key: candidate["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


def write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
    output_dir: str | Path, *, source_method_results_review: dict | None = None,
) -> dict:
    candidate = build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
        source_method_results_review=source_method_results_review
    )
    output = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache"} for part in output.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError("protected output directory")
    path = output / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError("output exists")
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_markdown_v1(candidate), encoding="utf-8")
    return candidate


def build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_markdown_v1(
    candidate: dict,
) -> str:
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(candidate)
    sections = [
        ("Source Method Results Review", [SOURCE_RESULTS_REVIEW_COMMIT, SOURCE_RESULTS_REVIEW_DIGEST]),
        ("Source Method Execution", [candidate["source_method_execution_commit"], candidate["source_remediation_or_method_execution_after_diagnostic_capture_digest"]]),
        ("Source Failure-Family Classification", [candidate["source_failure_family_classification_review_digest"], candidate["source_failure_family_classification_digest"]]),
        ("Source Bounded Excerpt Analysis", [candidate["source_bounded_excerpt_analysis_review_digest"], candidate["source_bounded_excerpt_analysis_digest"]]),
        ("Source Diagnostic Results Review", [candidate["source_receipt_recovery_or_recapture_results_review_digest"]]),
        ("Source Controlled Recapture Execution", [candidate["source_receipt_recovery_or_recapture_execution_digest"]]),
        ("Source Durable Receipt", [candidate["source_durable_receipt_path"], candidate["source_receipt_recovery_or_recapture_receipt_digest"]]),
        ("Source Receipt Loss History", [candidate["source_targeted_diagnostic_output_capture_execution_blocked_reason"]]),
        ("Source Planning and Detail Binding Evidence", [candidate["source_planning_execution_digest"], candidate["source_detail_binding_results_review_digest"], candidate["source_recovery_detail_digest"]]),
        ("Retry Failure Context", [str(candidate["retry_failure_context"])]), ("Candidate Scope", [CANDIDATE_SCOPE]),
        ("Selected Source Method Package", [candidate["selected_source_method_package"]]),
        ("Priority 1 Target Modules", [item["module_path"] for item in candidate["priority_1_target_modules"]]),
        ("Diagnostic Capture Evidence Summary", [str(candidate["diagnostic_capture_evidence_summary"])]),
        ("Reviewed Observable Failure Families", [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in candidate["reviewed_observable_failure_families"]]),
        ("Candidate Philosophy", [PHILOSOPHY, CANDIDATE_BOUNDARY, CANDIDATE_GOAL]),
        ("Proposed Remediation Plan or Execution Packages", [f"{item['package_id']}: {item['status']}" for item in candidate["proposed_remediation_plan_or_execution_packages"]]),
        ("Recommended Package", [RECOMMENDED_PACKAGE, candidate["recommendation_reason"]]),
        ("Future Remediation Requirements", [item["requirement_id"] for item in candidate["future_remediation_requirements"]]),
        ("Future Remediation Plan", [f"{item['step']}. {item['action']}" for item in candidate["future_remediation_plan"]]),
        ("Planned Outputs", [item["output_id"] for item in candidate["planned_outputs"]]),
        ("Non-Goals", candidate["non_goals"]), ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]), ("Risk Controls", candidate["risk_controls"]),
        ("Authority Boundaries", [CANDIDATE_BOUNDARY]),
        ("Checklist Summary", [f"{validation['passed_checks']}/{validation['total_checks']} checks pass; {validation['blocker_count']} blockers."]),
        ("Guardrails", ["Constants-only candidate; no receipt/output access, execution, remediation, retry, provider, or protected-branch authority."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Candidate After Method Results Review v1", ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", "", *[f"- {value}" for value in values], ""])
    return "\n".join(lines)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
PACKAGE_CREATE_TARGETED_REMEDIATION_PLAN_FROM_REVIEWED_FAILURE_FAMILIES_ONLY = RECOMMENDED_PACKAGE

__all__ = [name for name in globals() if name.isupper() or name.startswith(("build_marketflow_", "validate_marketflow_", "write_marketflow_", "MarketFlowRepository"))]
