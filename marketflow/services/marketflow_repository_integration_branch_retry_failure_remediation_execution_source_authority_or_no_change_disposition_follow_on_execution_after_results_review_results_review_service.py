"""Review the follow-on source-authority acquisition candidate creation offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_V1"
REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_READY"
REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1"
SOURCE_FOLLOW_ON_EXECUTION_COMMIT = "a5a78331058c37b348108f9599fec6a24763bf06"
SOURCE_FOLLOW_ON_EXECUTION_DIGEST = "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208"
SOURCE_ACQUISITION_CANDIDATE_DIGEST = "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91"
SOURCE_ACQUISITION_SCOPE_DIGEST = "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8"
SOURCE_MISSING_AUTHORITY_MAPPING_DIGEST = "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334"
SOURCE_FOLLOW_ON_EXECUTION_MANIFEST_DIGEST = "56a6d540ae16cb9670696255c775fb690b9273c13c120cd822facf4a8bb85347"
SELECTED_FOLLOW_ON_PACKAGE = source.SELECTED_FOLLOW_ON_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_V1"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_ONLY_IF_THIS_RESULTS_REVIEW_CONFIRMS_CANDIDATE"
RECOMMENDATION_REASON = (
    "The follow-on execution successfully created a source-authority acquisition candidate, acquisition scope "
    "definition, missing-authority-to-source-evidence mapping, acceptable source-artifact inventory, "
    "operator-provided evidence requirements, evidence custody and digest requirements, and candidate "
    "results-review requirements. It did not acquire source authority, acquire evidence, establish concrete "
    "source authority, identify safe change authority, create no-change disposition, execute diagnostics, "
    "execute remediation, create retry readiness, or create main-merge readiness. The next governed step "
    "should review the acquisition candidate before any source-authority acquisition approval or execution can be considered."
)
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"
OUTPUT_STATUS = "GENERATED_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_ONLY"

REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_digest"
ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_acquisition_candidate_review_digest"
ACQUISITION_SCOPE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_acquisition_scope_review_digest"
MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_missing_authority_to_source_evidence_mapping_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_follow_on_execution_after_results_review_results_review_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_READY = REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = REVIEW_SCOPE
PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS = SELECTED_FOLLOW_ON_PACKAGE


RESULTS_REVIEW_FINDINGS = (
    "The source follow-on execution used the approved package PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS.",
    "The source follow-on execution created a source-authority acquisition candidate and did not acquire source authority.",
    "The source-authority acquisition candidate is ready for results review but remains not approved and not executed.",
    "The acquisition scope contains four sections mapped to assertion/value, digest/hash, fixture/isolation/determinism, and schema/field/contract workstreams.",
    "The missing-authority-to-source-evidence mapping contains 30 mapped items and all remain MISSING_NOT_ACQUIRED.",
    "Every mapped item preserves authority_acquired_now=false, evidence_acquired_now=false, and direct_change_authorized=false.",
    "The acceptable source-artifact inventory contains 13 future artifact types, all acquired-now false and requiring later results review.",
    "The operator-provided evidence requirements preserve no-secret, no-API-key, and no-broker-credential boundaries.",
    "The evidence custody and digest requirements preserve source identity, reproducible provenance, and review gates.",
    "The candidate results-review requirements preserve review before any acquisition, disposition, diagnostic, remediation, retry, or main-merge path.",
    "No source authority, evidence, external evidence, disposition, diagnostic, remediation, retry candidate, or main-merge readiness was created.",
    "No production code, existing tests, expected digests, or patches were modified.",
    "The detached retry remains failed and authoritative.",
    "Priority 1 current-root validation remains non-retry evidence.",
    "The output is ready only for a separately governed acquisition-candidate operator review if this review confirms the candidate.",
)

RESULTS_REVIEW_DOMAINS = (
    ("source_follow_on_execution_identity", "PASSED", "Source execution commit, artifact, status, scope, selected package, and execution digest are bound."),
    ("source_authority_acquisition_candidate", "REVIEWED_CANDIDATE_ONLY", "Candidate was created for results review only and remains not approved and not executed."),
    ("acquisition_scope_definition", "REVIEWED_SCOPE_ONLY", "Four acquisition-scope sections define future authority needs without acquiring evidence."),
    ("missing_authority_to_source_evidence_mapping", "REVIEWED_MISSING_NOT_ACQUIRED", "Thirty mapped items remain missing/not acquired and non-authorizing."),
    ("acceptable_source_artifact_inventory", "REVIEWED_FUTURE_ARTIFACT_TYPES_ONLY", "Thirteen acceptable artifact types were inventoried but none were acquired."),
    ("operator_provided_evidence_requirements", "REVIEWED_REQUIREMENTS_ONLY", "Operator-provided evidence requirements were defined but no evidence was received or accepted."),
    ("evidence_custody_and_digest_requirements", "REVIEWED_REQUIREMENTS_ONLY", "Custody and digest requirements were defined for future review only."),
    ("candidate_results_review_requirements", "REVIEWED_REQUIREMENTS_ONLY", "Results-review requirements were created to preserve downstream gates."),
    ("unsupported_claims_boundary", "PRESERVED", "No root-cause, direct-change, retry-success, or main-readiness claims were made."),
    ("protected_repository_boundaries", "PRESERVED", "Main, integration branch, detached worktree, cache, .marketflow, tags, and staged evidence boundaries remain preserved."),
    ("provider_runtime_trading_boundary", "PRESERVED", "No provider, market-data, model, strategy, runtime, broker, or trading action occurred."),
    ("downstream_readiness", "LIMITED", "Review may support a future acquisition-candidate operator review, but acquisition, remediation, retry, and main merge remain closed."),
)

OUTPUT_IDS = tuple(
    """follow_on_execution_after_results_review_results_review_manifest
source_follow_on_execution_binding_report
source_follow_on_approval_binding_report
source_follow_on_operator_review_binding_report
source_follow_on_candidate_binding_report
source_results_review_binding_report
source_execution_binding_report
source_approval_binding_report
source_failure_diagnosis_binding_report
source_blocked_execution_binding_report
source_plan_results_review_binding_report
source_plan_execution_binding_report
source_method_and_diagnostic_binding_report
source_planning_detail_recovery_binding_report
retry_failure_context_review
priority1_validation_disposition_review
diagnostic_metadata_boundary_review
reviewed_observable_families_review
reviewed_workstreams_review
enrichment_review_facts_review
source_authority_acquisition_candidate_review
acquisition_scope_definition_review
missing_authority_to_source_evidence_mapping_review
acceptable_source_artifact_inventory_review
operator_provided_evidence_requirements_review
evidence_custody_and_digest_requirements_review
acquisition_candidate_results_review_requirements_review
unsupported_claims_boundary_review
follow_on_candidate_operator_review_readiness_report
source_authority_acquisition_gate_preservation_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)

NEXT_CHAIN = (
    "Source-Authority Acquisition Candidate Operator Review After Follow-On Execution Results Review v1.",
    "Source-Authority Acquisition Approval v1, if selected.",
    "Source-Authority Acquisition Execution v1, if approved.",
    "Source-Authority Acquisition Results Review v1.",
    "A conditional disposition candidate only if reviewed source authority supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple(
    """source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review
source_authority_acquisition_approval_if_selected
source_authority_acquisition_execution_if_approved
source_authority_acquisition_results_review
no_change_disposition_candidate_if_supported
alternate_diagnostic_candidate_if_supported
remediation_reentry_candidate_if_supported
no_change_retry_criteria_candidate_if_supported
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines()
)

RISK_CONTROLS = tuple(
    """follow_on_execution_results_review_does_not_rerun_follow_on_execution
follow_on_execution_results_review_does_not_acquire_source_authority
follow_on_execution_results_review_does_not_acquire_source_authority_evidence
follow_on_execution_results_review_does_not_acquire_external_evidence
follow_on_execution_results_review_does_not_create_source_authority_acquisition_execution
follow_on_execution_results_review_does_not_create_no_change_disposition
follow_on_execution_results_review_does_not_execute_alternate_diagnostics
follow_on_execution_results_review_does_not_execute_remediation
follow_on_execution_results_review_does_not_modify_production_code
follow_on_execution_results_review_does_not_modify_existing_tests
follow_on_execution_results_review_does_not_update_expected_digests
follow_on_execution_results_review_does_not_generate_patch
follow_on_execution_results_review_does_not_apply_patch
follow_on_execution_results_review_does_not_run_pytest
follow_on_execution_results_review_does_not_run_full_pytest
follow_on_execution_results_review_does_not_rerun_priority1_validation
follow_on_execution_results_review_does_not_rerun_retry
follow_on_execution_results_review_does_not_rerun_detached_retry
follow_on_execution_results_review_does_not_parse_durable_receipt
follow_on_execution_results_review_does_not_analyze_diagnostic_output
follow_on_execution_results_review_does_not_rerun_source_authority_enrichment
follow_on_execution_results_review_does_not_rerun_plan_execution
follow_on_execution_results_review_does_not_regenerate_targeted_plan
follow_on_execution_results_review_does_not_rerun_method_execution
follow_on_execution_results_review_does_not_rerun_controlled_recapture
follow_on_execution_results_review_does_not_run_diagnostic_command
follow_on_execution_results_review_does_not_read_pytest_cache
follow_on_execution_results_review_does_not_modify_pytest_cache
follow_on_execution_results_review_does_not_parse_terminal_logs
follow_on_execution_results_review_does_not_parse_operator_logs
follow_on_execution_results_review_does_not_inspect_env
follow_on_execution_results_review_does_not_reconstruct_prior_lost_values
follow_on_execution_results_review_does_not_reconstruct_full_streams
follow_on_execution_results_review_does_not_classify_modules_again
follow_on_execution_results_review_does_not_classify_full_retry_failures
follow_on_execution_results_review_does_not_classify_full_retry_errors
follow_on_execution_results_review_does_not_claim_failure_error_separation
follow_on_execution_results_review_does_not_identify_authoritative_first_failure
follow_on_execution_results_review_does_not_identify_authoritative_first_error
follow_on_execution_results_review_does_not_claim_traceback_root_cause
follow_on_execution_results_review_does_not_claim_root_cause
follow_on_execution_results_review_does_not_claim_retry_success
follow_on_execution_results_review_does_not_claim_main_merge_readiness
follow_on_execution_results_review_does_not_create_retry_candidate
follow_on_execution_results_review_does_not_create_retry_approval
follow_on_execution_results_review_does_not_create_retry_execution
follow_on_execution_results_review_does_not_create_retry_results_review
follow_on_execution_results_review_does_not_create_integration_results_review
follow_on_execution_results_review_does_not_mark_integration_successful
follow_on_execution_results_review_does_not_generate_successful_integration_digest
follow_on_execution_results_review_does_not_push_integration_branch
follow_on_execution_results_review_does_not_push_main
follow_on_execution_results_review_does_not_delete_integration_branch
follow_on_execution_results_review_does_not_delete_worktree
follow_on_execution_results_review_does_not_force_push
follow_on_execution_results_review_does_not_prune_remotes
follow_on_execution_results_review_does_not_modify_tags
follow_on_execution_results_review_does_not_modify_staged_evidence
follow_on_execution_results_review_does_not_regenerate_evidence
follow_on_execution_results_review_does_not_call_providers
follow_on_execution_results_review_does_not_acquire_market_data
follow_on_execution_results_review_does_not_generate_dataset
follow_on_execution_results_review_does_not_recompute_metrics
follow_on_execution_results_review_does_not_train_models
follow_on_execution_results_review_does_not_score_strategy
follow_on_execution_results_review_does_not_generate_trade_recommendations
follow_on_execution_results_review_does_not_accept_predictive_usefulness
follow_on_execution_results_review_does_not_accept_profitability
follow_on_execution_results_review_does_not_authorize_runtime
follow_on_execution_results_review_does_not_authorize_broker_execution
source_authority_acquisition_candidate_review_is_not_acquisition_approval
source_authority_acquisition_candidate_is_not_source_authority_acquisition
source_authority_acquisition_scope_is_not_evidence_acquisition
acceptable_source_artifact_inventory_is_not_artifact_acquisition
operator_provided_evidence_requirements_are_not_operator_evidence
missing_authority_mapping_is_not_change_authority
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
source_follow_on_execution_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_operator_review_required_for_source_authority_acquisition_candidate
separate_approval_required_before_source_authority_acquisition
separate_results_review_required_after_any_acquisition
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
    """follow_on_execution_after_results_review_results_review_created
follow_on_execution_after_results_review_results_review_ready
source_follow_on_execution_reviewed
source_follow_on_execution_identity_verified
selected_follow_on_package_verified
source_authority_acquisition_candidate_reviewed
source_authority_acquisition_candidate_created_reviewed
source_authority_acquisition_candidate_ready_for_results_review_reviewed
source_authority_acquisition_scope_reviewed
missing_authority_to_source_evidence_mapping_reviewed
acceptable_source_artifact_inventory_reviewed
operator_provided_evidence_requirements_reviewed
evidence_custody_and_digest_requirements_reviewed
candidate_results_review_requirements_reviewed
source_follow_on_approval_verified
source_follow_on_operator_review_verified
source_follow_on_candidate_verified
source_results_review_verified
source_execution_verified
source_approval_verified
source_failure_diagnosis_verified
source_blocked_execution_verified
retry_failure_context_verified
priority_1_context_verified
priority1_validation_context_verified
diagnostic_metadata_verified
observable_families_verified
reviewed_workstreams_verified
missing_authority_inventory_review_facts_verified
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_source_authority_acquisition_candidate_operator_review_after_results_review""".splitlines()
)
FALSE_FIELDS = tuple(
    """source_authority_acquisition_performed
source_authority_evidence_acquired
external_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
source_authority_acquisition_execution_created
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
pytest_performed_in_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_review
diagnostic_output_analyzed_in_review
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
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
ready_for_source_authority_acquisition_execution
ready_for_no_change_disposition_candidate
ready_for_alternate_diagnostic_candidate
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
)


class MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError(ValueError):
    """Raised when reviewed source evidence or a protected boundary changes."""


def _committed_source_follow_on_execution() -> dict[str, Any]:
    common = source._common("2026-08-23T00:00:00Z")
    candidate = source._acquisition_candidate()
    scopes = source._acquisition_scopes()
    mapping = source._missing_authority_mapping()
    return {
        **common,
        "artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "execution_status": source.SUCCESS_STATUS,
        **{field: True for field in source.TRUE_FIELDS},
        "source_authority_acquisition_candidate": candidate,
        "source_authority_acquisition_scope_definition": scopes,
        "missing_authority_to_source_evidence_mapping": mapping,
        "acceptable_source_artifact_inventory": source._source_artifact_inventory(),
        "operator_provided_evidence_requirements": list(source.OPERATOR_EVIDENCE_REQUIREMENTS),
        "evidence_custody_and_digest_requirements": list(source.EVIDENCE_CUSTODY_REQUIREMENTS),
        "candidate_results_review_requirements": list(source.CANDIDATE_RESULTS_REVIEW_REQUIREMENTS),
        "outputs_generated": [{"output_id": item, "status": source.OUTPUT_STATUS} for item in source.OUTPUT_IDS],
        source.EXECUTION_DIGEST_KEY: SOURCE_FOLLOW_ON_EXECUTION_DIGEST,
        source.ACQUISITION_CANDIDATE_DIGEST_KEY: SOURCE_ACQUISITION_CANDIDATE_DIGEST,
        source.ACQUISITION_SCOPE_DIGEST_KEY: SOURCE_ACQUISITION_SCOPE_DIGEST,
        source.MISSING_AUTHORITY_MAPPING_DIGEST_KEY: SOURCE_MISSING_AUTHORITY_MAPPING_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_FOLLOW_ON_EXECUTION_MANIFEST_DIGEST,
    }


def _validate_source_follow_on_execution(candidate: Any) -> None:
    error = MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError
    if not isinstance(candidate, Mapping):
        raise error("source follow-on execution must be an object")
    expected = _committed_source_follow_on_execution()
    fields = tuple(expected)
    for field in fields:
        if candidate.get(field) != expected[field]:
            raise error(f"source follow-on execution {field} mismatch")


def _summary_records(execution: Mapping[str, Any]) -> dict[str, Any]:
    bindings = source.SOURCE_BINDINGS
    return {
        "source_follow_on_execution_summary": {
            "commit": SOURCE_FOLLOW_ON_EXECUTION_COMMIT, "artifact_kind": source.SUCCESS_ARTIFACT_KIND,
            "status": source.SUCCESS_STATUS, "scope": source.EXECUTION_SCOPE,
            "digest": SOURCE_FOLLOW_ON_EXECUTION_DIGEST, "selected_package": SELECTED_FOLLOW_ON_PACKAGE,
            "outputs_generated_count": 30,
        },
        "source_follow_on_approval_summary": {"commit": bindings["source_follow_on_approval_commit"], "digest": bindings["source_follow_on_approval_digest"]},
        "source_follow_on_operator_review_summary": {"commit": bindings["source_follow_on_candidate_operator_review_commit"], "digest": bindings["source_follow_on_candidate_operator_review_digest"]},
        "source_follow_on_candidate_summary": {"commit": bindings["source_follow_on_candidate_commit"], "digest": bindings["source_follow_on_candidate_digest"]},
        "source_results_review_summary": {"commit": bindings["source_results_review_commit"], "digest": bindings["source_results_review_digest"]},
        "source_execution_summary": {"commit": bindings["source_execution_commit"], "digest": bindings["source_execution_digest"]},
        "source_approval_summary": {"commit": bindings["source_approval_commit"], "digest": bindings["source_approval_digest"]},
        "source_historical_operator_review_summary": {"commit": bindings["source_operator_review_commit"], "digest": bindings["source_operator_review_digest"]},
        "source_historical_candidate_summary": {"commit": bindings["source_candidate_commit"], "digest": bindings["source_candidate_digest"]},
        "source_failure_diagnosis_summary": {"commit": bindings["source_failure_diagnosis_commit"], "digest": bindings["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"]},
        "source_blocked_execution_summary": {"commit": bindings["source_blocked_execution_commit"], "reason": bindings["source_blocked_reason"], "manifest_digest": bindings["source_blocked_manifest_digest"]},
        "source_plan_results_review_summary": {key: value for key, value in bindings.items() if "plan_results_review" in key or "historical_workstream_mapping_review" in key},
        "source_plan_execution_summary": {key: value for key, value in bindings.items() if "plan_execution" in key},
        "source_method_results_review_summary": {key: value for key, value in bindings.items() if "method_results_review" in key},
        "source_method_execution_summary": {key: value for key, value in bindings.items() if "method_execution" in key},
        "source_diagnostic_results_review_summary": {key: value for key, value in bindings.items() if "recapture_results_review" in key or "payload_review" in key or "durable_receipt_review" in key},
        "source_controlled_recapture_summary": {key: value for key, value in bindings.items() if "recapture_execution" in key or "recapture_receipt_digest" in key},
        "source_durable_receipt_summary": {"path": bindings["source_durable_receipt_path"], "parsed": False},
        "source_receipt_loss_history_summary": {"primary": bindings["source_primary_failure_class"], "secondary": bindings["source_secondary_failure_class"], "blocked_reason": bindings["source_targeted_diagnostic_output_capture_execution_blocked_reason"]},
        "source_planning_and_detail_binding_summary": {key: value for key, value in bindings.items() if any(token in key for token in ("planning_digest", "detail_binding", "complete_29", "materialized_payload", "recovery_detail", "module_grouping", "staged_inventory"))},
    }


def _candidate_review(execution: Mapping[str, Any]) -> dict[str, Any]:
    candidate = execution["source_authority_acquisition_candidate"]
    return {
        "candidate_type": candidate["candidate_type"], "candidate_status": candidate["candidate_status"],
        "candidate_scope": candidate["candidate_scope"], "candidate_digest": SOURCE_ACQUISITION_CANDIDATE_DIGEST,
        "reviewed": True, "created_reviewed": True, "ready_for_results_review_reviewed": True,
        "approved": False, "executed": False, "authority_acquired": False, "evidence_acquired": False,
    }


def _scope_review(execution: Mapping[str, Any]) -> dict[str, Any]:
    sections = deepcopy(execution["source_authority_acquisition_scope_definition"])
    return {
        "reviewed": True, "section_count": len(sections), "sections": sections,
        "all_sections_deny_evidence_acquisition": all(item["current_execution_does_not_acquire_evidence"] for item in sections),
        "all_sections_deny_direct_changes": all(item[source.SCOPE_CHANGE_FLAGS[item["section_id"]]] is False for item in sections),
    }


def _mapping_review(execution: Mapping[str, Any]) -> dict[str, Any]:
    mapping = deepcopy(execution["missing_authority_to_source_evidence_mapping"])
    return {
        "reviewed": True, "mapped_item_count": len(mapping), "items": mapping,
        "all_missing_not_acquired": all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in mapping),
        "all_authority_acquired_now_false": all(item["authority_acquired_now"] is False for item in mapping),
        "all_evidence_acquired_now_false": all(item["evidence_acquired_now"] is False for item in mapping),
        "all_direct_change_authorized_false": all(item["direct_change_authorized"] is False for item in mapping),
    }


def _inventory_review(execution: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = deepcopy(execution["acceptable_source_artifact_inventory"])
    return {
        "reviewed": True, "artifact_type_count": len(artifacts), "artifact_types": artifacts,
        "all_acquired_now_false": all(item["acquired_now"] is False for item in artifacts),
        "all_require_results_review": all(item["requires_results_review_before_use"] for item in artifacts),
    }


def _requirements_review(requirements: list[Any]) -> dict[str, Any]:
    return {"reviewed": True, "requirement_count": len(requirements), "requirements": deepcopy(requirements), "satisfied_or_acquired_now": False}


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {"check_id": check_id, "status": status, "expected": deepcopy(expected), "actual": deepcopy(actual), "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    bindings = {
        "source_follow_on_execution_commit": SOURCE_FOLLOW_ON_EXECUTION_COMMIT,
        "source_follow_on_execution_after_results_review_digest": SOURCE_FOLLOW_ON_EXECUTION_DIGEST,
        "source_follow_on_execution_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_follow_on_execution_status": source.SUCCESS_STATUS,
        "source_follow_on_execution_scope": source.EXECUTION_SCOPE,
        "source_authority_acquisition_candidate_digest": SOURCE_ACQUISITION_CANDIDATE_DIGEST,
        "source_authority_acquisition_scope_digest": SOURCE_ACQUISITION_SCOPE_DIGEST,
        "source_missing_authority_to_source_evidence_mapping_digest": SOURCE_MISSING_AUTHORITY_MAPPING_DIGEST,
        "source_follow_on_execution_manifest_digest": SOURCE_FOLLOW_ON_EXECUTION_MANIFEST_DIGEST,
        **source.SOURCE_BINDINGS,
    }
    checks = [_check(f"{field}_bound", expected, review.get(field)) for field, expected in bindings.items()]
    fixed = {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE, "acquisition_scope_section_count": 4,
        "mapped_missing_authority_item_count": 30, "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6, "candidate_results_review_requirement_count": 16,
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        "follow_on_execution_outputs_generated_count": 30, "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30, "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "outputs_generated": [{"output_id": item, "status": OUTPUT_STATUS} for item in OUTPUT_IDS],
        "results_review_domains": [{"domain_id": domain, "disposition": disposition, "explanation": explanation} for domain, disposition, explanation in RESULTS_REVIEW_DOMAINS],
        "results_review_findings": [{"finding_id": f"finding_{i}", "finding": finding} for i, finding in enumerate(RESULTS_REVIEW_FINDINGS, 1)],
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
    }
    checks.extend(_check(field, expected, review.get(field)) for field, expected in fixed.items())
    checks.extend(_check(f"{field}_true", True, review.get(field)) for field in TRUE_FIELDS)
    checks.extend(_check(f"{field}_false", False, review.get(field)) for field in FALSE_FIELDS)
    checks.extend((
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        _check("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, review.get("no_tracked_pytest_cache_files")),
    ))
    return checks


def _summary(review: Mapping[str, Any]) -> dict[str, Any]:
    checks = review["checklist"]
    return {
        "total_checks": len(checks), "passed_checks": len(checks), "failed_checks": 0, "blocker_count": 0,
        **{field: review[field] for field in TRUE_FIELDS + FALSE_FIELDS},
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "candidate_status": "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED",
        "acquisition_scope_section_count": 4, "mapped_missing_authority_item_count": 30,
        "acceptable_source_artifact_type_count": 13, "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6, "candidate_results_review_requirement_count": 16,
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "source_outputs_generated_count": 27,
        "review_outputs_generated_count": 28, "follow_on_execution_outputs_generated_count": 30,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }


def _review_digest(review: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(review))
    for field in ("checklist", "summary", REVIEW_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def _assemble_review() -> dict[str, Any]:
    execution = _committed_source_follow_on_execution()
    summaries = _summary_records(execution)
    candidate_review = _candidate_review(execution)
    scope_review = _scope_review(execution)
    mapping_review = _mapping_review(execution)
    inventory_review = _inventory_review(execution)
    operator_review = _requirements_review(execution["operator_provided_evidence_requirements"])
    custody_review = _requirements_review(execution["evidence_custody_and_digest_requirements"])
    results_requirements_review = _requirements_review(execution["candidate_results_review_requirements"])
    context_fields = (
        "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families", "reviewed_workstreams",
        "primary_failure_class", "secondary_failure_classes", "missing_authority_inventory_section_count",
        "missing_authority_inventory_item_count", "missing_authority_items_status", "workstream_mapping_count",
        "workstream_mapping_status", "source_outputs_generated_count", "review_outputs_generated_count",
    )
    review = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION,
        "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_follow_on_execution_artifact_kind": source.SUCCESS_ARTIFACT_KIND,
        "source_follow_on_execution_status": source.SUCCESS_STATUS,
        "source_follow_on_execution_scope": source.EXECUTION_SCOPE,
        "source_follow_on_execution_commit": SOURCE_FOLLOW_ON_EXECUTION_COMMIT,
        "source_follow_on_execution_after_results_review_digest": SOURCE_FOLLOW_ON_EXECUTION_DIGEST,
        "source_authority_acquisition_candidate_digest": SOURCE_ACQUISITION_CANDIDATE_DIGEST,
        "source_authority_acquisition_scope_digest": SOURCE_ACQUISITION_SCOPE_DIGEST,
        "source_missing_authority_to_source_evidence_mapping_digest": SOURCE_MISSING_AUTHORITY_MAPPING_DIGEST,
        "source_follow_on_execution_manifest_digest": SOURCE_FOLLOW_ON_EXECUTION_MANIFEST_DIGEST,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        **deepcopy(source.SOURCE_BINDINGS), **summaries,
        **{field: deepcopy(execution[field]) for field in context_fields},
        "source_authority_enrichment_review_summary": {"reviewed": True, "planning_only": True, "source_authority_acquired": False},
        "missing_authority_inventory_review_summary": {"reviewed": True, "section_count": 4, "item_count": 30, "item_status": "MISSING_NOT_ACQUIRED"},
        "workstream_authority_mapping_review_summary": {"reviewed": True, "mapping_count": 4, "mapping_status": "PLANNED_NOT_EXECUTED"},
        "source_authority_acquisition_candidate_review": candidate_review,
        "acquisition_scope_definition_review": scope_review,
        "missing_authority_to_source_evidence_mapping_review": mapping_review,
        "acceptable_source_artifact_inventory_review": inventory_review,
        "operator_provided_evidence_requirements_review": operator_review,
        "evidence_custody_and_digest_requirements_review": custody_review,
        "candidate_results_review_requirements_review": results_requirements_review,
        "acquisition_scope_section_count": 4, "mapped_missing_authority_item_count": 30,
        "acceptable_source_artifact_type_count": 13, "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6, "candidate_results_review_requirement_count": 16,
        "follow_on_execution_outputs_generated_count": 30,
        "unsupported_claims_boundary": [
            "No authority, evidence, root cause, direct change, retry success, or main readiness was established.",
            "Candidate review is not acquisition approval or execution.",
            "The failed detached retry remains authoritative and Priority 1 validation remains non-retry evidence.",
        ],
        "results_review_domains": [{"domain_id": domain, "disposition": disposition, "explanation": explanation} for domain, disposition, explanation in RESULTS_REVIEW_DOMAINS],
        "results_review_findings": [{"finding_id": f"finding_{i}", "finding": finding} for i, finding in enumerate(RESULTS_REVIEW_FINDINGS, 1)],
        "recommendation": {"recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED", "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON},
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION, "reason": RECOMMENDATION_REASON,
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "outputs_generated": [{"output_id": item, "status": OUTPUT_STATUS} for item in OUTPUT_IDS],
        **{field: True for field in TRUE_FIELDS}, **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    review[ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY] = semantic_digest(candidate_review)
    review[ACQUISITION_SCOPE_REVIEW_DIGEST_KEY] = semantic_digest(scope_review)
    review[MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY] = semantic_digest(mapping_review)
    review["digest_manifest"] = {
        "source_follow_on_execution_commit": SOURCE_FOLLOW_ON_EXECUTION_COMMIT,
        "source_follow_on_execution_digest": SOURCE_FOLLOW_ON_EXECUTION_DIGEST,
        ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY: review[ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY],
        ACQUISITION_SCOPE_REVIEW_DIGEST_KEY: review[ACQUISITION_SCOPE_REVIEW_DIGEST_KEY],
        MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY: review[MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    }
    review[MANIFEST_DIGEST_KEY] = semantic_digest(review["digest_manifest"])
    review["checklist"] = _checklist(review)
    review["summary"] = _summary(review)
    review[REVIEW_DIGEST_KEY] = _review_digest(review)
    return review


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(
    *, source_follow_on_execution: dict | None = None,
) -> dict[str, Any]:
    """Build the deterministic review without rerunning the reviewed execution."""

    execution = _committed_source_follow_on_execution() if source_follow_on_execution is None else deepcopy(source_follow_on_execution)
    _validate_source_follow_on_execution(execution)
    review = _assemble_review()
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(review)
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


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Reject any mutation of evidence, reviewed content, digest, or authority boundary."""

    if not isinstance(review, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError("review must be an object")
    expected = _assemble_review()
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError(f"{difference} mismatch")
    for key in (REVIEW_DIGEST_KEY, ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY, ACQUISITION_SCOPE_REVIEW_DIGEST_KEY, MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        if re.fullmatch(r"[0-9a-f]{64}", str(review.get(key))) is None:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError(f"{key} invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "review_status": REVIEW_STATUS, "review_scope": REVIEW_SCOPE,
        "review_digest": review[REVIEW_DIGEST_KEY],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Follow-On Execution", "Source Follow-On Execution Digests", "Source Follow-On Approval",
    "Source Follow-On Operator Review", "Source Follow-On Candidate", "Source Results Review", "Source Execution",
    "Source Approval", "Source Historical Operator Review", "Source Historical Candidate", "Source Failure Diagnosis",
    "Source Blocked Execution", "Blocked Reason", "Failure Classification", "Source Remediation Execution Approval",
    "Source Plan Results Review", "Source Plan Execution", "Source Method Results Review", "Source Method Execution",
    "Source Diagnostic Results Review", "Source Controlled Recapture", "Source Durable Receipt",
    "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Priority 1 Target Modules",
    "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Source Authority Enrichment Review Summary", "Missing Authority Inventory Review Summary",
    "Workstream Authority Mapping Review Summary", "Source Authority Acquisition Candidate Review",
    "Acquisition Scope Definition Review", "Missing Authority to Source Evidence Mapping Review",
    "Acceptable Source Artifact Inventory Review", "Operator-Provided Evidence Requirements Review",
    "Evidence Custody and Digest Requirements Review", "Candidate Results Review Requirements Review",
    "Unsupported Claims Boundary", "Results Review Domains", "Results Review Findings", "Recommendation",
    "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the validated review as a status document."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(deepcopy(review))
    sections = {
        "Source Follow-On Execution": review["source_follow_on_execution_summary"],
        "Source Follow-On Execution Digests": {key: review[key] for key in ("source_follow_on_execution_after_results_review_digest", "source_authority_acquisition_candidate_digest", "source_authority_acquisition_scope_digest", "source_missing_authority_to_source_evidence_mapping_digest", "source_follow_on_execution_manifest_digest")},
        "Source Follow-On Approval": review["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": review["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": review["source_follow_on_candidate_summary"],
        "Source Results Review": review["source_results_review_summary"], "Source Execution": review["source_execution_summary"],
        "Source Approval": review["source_approval_summary"],
        "Source Historical Operator Review": review["source_historical_operator_review_summary"],
        "Source Historical Candidate": review["source_historical_candidate_summary"],
        "Source Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Source Blocked Execution": review["source_blocked_execution_summary"], "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": review["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": review["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": review["source_plan_results_review_summary"],
        "Source Plan Execution": review["source_plan_execution_summary"],
        "Source Method Results Review": review["source_method_results_review_summary"],
        "Source Method Execution": review["source_method_execution_summary"],
        "Source Diagnostic Results Review": review["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": review["source_controlled_recapture_summary"],
        "Source Durable Receipt": review["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": review["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": review["retry_failure_context"], "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"],
        "Reviewed Workstreams": review["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": review["source_authority_enrichment_review_summary"],
        "Missing Authority Inventory Review Summary": review["missing_authority_inventory_review_summary"],
        "Workstream Authority Mapping Review Summary": review["workstream_authority_mapping_review_summary"],
        "Source Authority Acquisition Candidate Review": review["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Definition Review": review["acquisition_scope_definition_review"],
        "Missing Authority to Source Evidence Mapping Review": review["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory Review": review["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements Review": review["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements Review": review["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements Review": review["candidate_results_review_requirements_review"],
        "Unsupported Claims Boundary": review["unsupported_claims_boundary"], "Results Review Domains": review["results_review_domains"],
        "Results Review Findings": review["results_review_findings"], "Recommendation": review["recommendation"],
        "Next Chain": review["next_chain"], "Next Gates": review["next_gates"], "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {field: review[field] for field in FALSE_FIELDS},
        "Checklist Summary": review["summary"], "Guardrails": [field for field in FALSE_FIELDS if review[field] is False],
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Execution After Results Review Results Review v1",
        "", f"Artifact: `{review['artifact_kind']}`", "", f"Status: `{review['review_status']}`", "",
        f"Scope: `{review['review_scope']}`", "", f"Review digest: `{review[REVIEW_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(
    output_dir: str | Path, *, source_follow_on_execution: dict | None = None,
) -> dict[str, Any]:
    """Write the deterministic results-review status document."""

    review = build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(source_follow_on_execution=source_follow_on_execution)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "REVIEW_STATUS", "REVIEW_SCOPE", "SELECTED_FOLLOW_ON_PACKAGE",
    "REVIEW_DIGEST_KEY", "ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY", "ACQUISITION_SCOPE_REVIEW_DIGEST_KEY",
    "MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_markdown_v1",
]
