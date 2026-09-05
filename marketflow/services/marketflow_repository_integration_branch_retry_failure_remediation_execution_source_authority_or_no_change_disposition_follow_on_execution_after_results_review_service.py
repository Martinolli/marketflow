"""Create the approved source-authority acquisition candidate, without acquiring evidence."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_service
    as historical_execution,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_service
    as source_approval,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_service
    as source_candidate,
)


SUCCESS_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_V1"
BLOCKED_ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_V1"
SUCCESS_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_READY"
BLOCKED_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE"
EXECUTION_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1"
SELECTED_FOLLOW_ON_PACKAGE = source_approval.SELECTED_FOLLOW_ON_PACKAGE
SOURCE_FOLLOW_ON_APPROVAL_COMMIT = "61e0d95e47ac16901fd05620d83214430718788d"
SOURCE_FOLLOW_ON_APPROVAL_DIGEST = "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6"
SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT = "1d610d49852fe76101c3d9293f83ccd65ec40749"
SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST = "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"
SOURCE_FOLLOW_ON_CANDIDATE_COMMIT = "072fa2c4c88f66ac95ef7864590b847368ed490c"
SOURCE_FOLLOW_ON_CANDIDATE_DIGEST = "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"
SOURCE_RESULTS_REVIEW_COMMIT = "f71143ec0743a3732535c47d2ef1d0d887403dc7"
SOURCE_RESULTS_REVIEW_DIGEST = "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"
SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST = "0cc52bd10f4b3fc61220f92f0024b728c98c43133c6b71906535037cbe824d46"
SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST = "72dd695b4b112e4a4c7d285efd896a54bfd05ec0f8cd1c9bc3eb2087a40b49ec"
SOURCE_WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST = "f64e8575ef00ebacf54d1bf145140a94001c8e475e5a89c44e62a609421c7597"
SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST = "1d06a9b1ffd9127fa4808f960be188cf09ac85acaf4145845194c9d025e2e3ba"
SOURCE_EXECUTION_COMMIT = "e80ddda241863eca8e52ea97fa050dcd6daea5ec"
SOURCE_EXECUTION_DIGEST = "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"
SOURCE_ENRICHMENT_PLAN_DIGEST = "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94"
SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST = "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8"
SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST = "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd"
SOURCE_EXECUTION_MANIFEST_DIGEST = "8a544aa173597f2c24e531a69f4eab2264fb1aa0796a67f87b00af291e6109d6"

SUCCESS_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_V1"
BLOCKED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1"
OUTPUT_STATUS = "GENERATED_FOLLOW_ON_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_ONLY"
PASS, FAIL, BLOCKER = "PASS", "FAIL", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

EXECUTION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_digest"
ACQUISITION_CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_acquisition_candidate_digest"
ACQUISITION_SCOPE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_acquisition_scope_digest"
MISSING_AUTHORITY_MAPPING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_missing_authority_to_source_evidence_mapping_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_follow_on_execution_after_results_review_manifest_digest"
BLOCKED_MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_blocked_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_V1 = SUCCESS_ARTIFACT_KIND
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_V1 = BLOCKED_ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_READY = SUCCESS_STATUS
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE = BLOCKED_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = EXECUTION_SCOPE
PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS = SELECTED_FOLLOW_ON_PACKAGE


ACQUISITION_SCOPE_REQUIREMENTS = {
    "assertion_value_mismatch_source_authority_scope": (
        "canonical source of expected values", "canonical source of actual values",
        "artifact contract proving which value is authoritative", "provenance for source values",
        "provenance for test expectations", "backward compatibility implications",
        "change authority decision evidence", "focused verification requirements before any future change",
    ),
    "digest_hash_boundary_source_authority_scope": (
        "canonical payload source", "canonical serialization method", "digest input-boundary definition",
        "digest manifest field authority", "expected hash authority", "old/new digest traceability",
        "proof required before any digest constant update", "proof required before any expected hash update",
    ),
    "fixture_isolation_determinism_source_authority_scope": (
        "shared-state leakage evidence", "fixture lifecycle authority", "fixture isolation authority",
        "deterministic timestamp authority", "deterministic path/CWD/worktree authority",
        "deterministic seed/randomness authority", "temp-path boundary evidence",
        "mutation/isolation verification requirements",
    ),
    "schema_field_contract_source_authority_scope": (
        "canonical schema contract", "required/optional field authority", "artifact field contract",
        "export-surface authority", "backward-compatible alias requirements",
        "field addition/removal authority", "validation requirements", "deprecation / compatibility requirements",
    ),
}
SCOPE_TO_WORKSTREAM = {
    "assertion_value_mismatch_source_authority_scope": "assertion_value_mismatch_workstream",
    "digest_hash_boundary_source_authority_scope": "digest_hash_boundary_workstream",
    "fixture_isolation_determinism_source_authority_scope": "fixture_isolation_determinism_workstream",
    "schema_field_contract_source_authority_scope": "schema_field_contract_workstream",
}
SCOPE_CHANGE_FLAGS = {
    "assertion_value_mismatch_source_authority_scope": "direct_value_or_assertion_change_authorized",
    "digest_hash_boundary_source_authority_scope": "direct_digest_update_authorized",
    "fixture_isolation_determinism_source_authority_scope": "direct_fixture_or_test_rewrite_authorized",
    "schema_field_contract_source_authority_scope": "direct_schema_or_export_redesign_authorized",
}
ACCEPTABLE_SOURCE_ARTIFACT_TYPES = (
    "approved product specification", "approved schema definition", "approved artifact contract",
    "approved canonical payload or serialization contract", "approved expected-value source",
    "approved actual-value source", "approved digest manifest source", "approved fixture lifecycle document",
    "approved deterministic execution contract", "approved export-surface contract",
    "approved operator-provided evidence package", "approved source-owning-team statement",
    "approved reviewed source-digest bundle",
)
OPERATOR_EVIDENCE_REQUIREMENTS = (
    "must be repository-relative or explicitly identified", "must have source owner or origin",
    "must have digest or reproducible provenance", "must distinguish specification from observation",
    "must distinguish expected from actual", "must distinguish source authority from diagnostic output",
    "must not include secrets", "must not include API keys", "must not include broker credentials",
    "must require results review before use",
)
EVIDENCE_CUSTODY_REQUIREMENTS = (
    "record source owner and origin", "record repository-relative path or explicit identifier",
    "bind a SHA-256 digest or reproducible provenance", "preserve the original artifact unchanged",
    "separate specification evidence from observed diagnostic evidence",
    "require a separate results review before evidence may support any change",
)
CANDIDATE_RESULTS_REVIEW_REQUIREMENTS = (
    "source approval and package selection", "source follow-on approval digest",
    "source operator review digest", "source results-review digest", "source execution digest",
    "acquisition candidate created", "acquisition candidate scope is complete",
    "30 mapped missing-authority items remain missing/not acquired", "no source authority was acquired",
    "no evidence was acquired", "no direct change authority was created",
    "no no-change disposition was created", "no diagnostic was executed", "no remediation was executed",
    "no retry candidate was created", "no main-merge readiness was created",
)

OUTPUT_IDS = tuple(
    """follow_on_execution_after_results_review_manifest
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
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
enrichment_review_facts_report
source_authority_acquisition_candidate
source_authority_acquisition_scope_definition
missing_authority_to_source_evidence_mapping
acceptable_source_artifact_inventory
operator_provided_evidence_requirements
evidence_custody_and_digest_requirements
acquisition_candidate_results_review_requirements
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines()
)

SUCCESS_NEXT_CHAIN = (
    "Follow-On Execution After Results Review Results Review v1.",
    "Source-Authority Acquisition Candidate Operator Review v1, only if results review confirms the candidate.",
    "Source-Authority Acquisition Approval v1, if selected.",
    "Source-Authority Acquisition Execution v1, if approved.",
    "Source-Authority Acquisition Results Review v1.",
    "A conditional disposition candidate only if reviewed source authority supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
BLOCKED_NEXT_CHAIN = (
    "Follow-On Execution After Results Review Failure Diagnosis v1.",
    "Alternate approved path only after review.", "No source-authority acquisition, retry, or main merge.",
)
SUCCESS_NEXT_GATES = tuple(
    """follow_on_execution_results_review_after_source_authority_acquisition_candidate_creation
source_authority_acquisition_candidate_operator_review_if_results_review_confirms
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
BLOCKED_NEXT_GATES = (
    "follow_on_execution_after_results_review_failure_diagnosis",
    "alternate_approved_path_only_after_review", "source_authority_acquisition_retry_and_main_merge_remain_blocked",
)

RISK_CONTROLS = tuple(
    """follow_on_execution_uses_approved_package_only
follow_on_execution_creates_source_authority_acquisition_candidate_only
follow_on_execution_does_not_acquire_source_authority
follow_on_execution_does_not_acquire_source_authority_evidence
follow_on_execution_does_not_acquire_external_evidence
follow_on_execution_does_not_create_source_authority_acquisition_execution
follow_on_execution_does_not_create_no_change_disposition
follow_on_execution_does_not_execute_alternate_diagnostics
follow_on_execution_does_not_execute_remediation
follow_on_execution_does_not_modify_production_code
follow_on_execution_does_not_modify_existing_tests
follow_on_execution_does_not_update_expected_digests
follow_on_execution_does_not_generate_patch
follow_on_execution_does_not_apply_patch
follow_on_execution_does_not_run_pytest
follow_on_execution_does_not_run_full_pytest
follow_on_execution_does_not_rerun_priority1_validation
follow_on_execution_does_not_rerun_retry
follow_on_execution_does_not_rerun_detached_retry
follow_on_execution_does_not_parse_durable_receipt
follow_on_execution_does_not_analyze_diagnostic_output
follow_on_execution_does_not_rerun_source_authority_enrichment
follow_on_execution_does_not_rerun_plan_execution
follow_on_execution_does_not_regenerate_targeted_plan
follow_on_execution_does_not_rerun_method_execution
follow_on_execution_does_not_rerun_controlled_recapture
follow_on_execution_does_not_run_diagnostic_command
follow_on_execution_does_not_read_pytest_cache
follow_on_execution_does_not_modify_pytest_cache
follow_on_execution_does_not_parse_terminal_logs
follow_on_execution_does_not_parse_operator_logs
follow_on_execution_does_not_inspect_env
follow_on_execution_does_not_reconstruct_prior_lost_values
follow_on_execution_does_not_reconstruct_full_streams
follow_on_execution_does_not_classify_modules_again
follow_on_execution_does_not_classify_full_retry_failures
follow_on_execution_does_not_classify_full_retry_errors
follow_on_execution_does_not_claim_failure_error_separation
follow_on_execution_does_not_identify_authoritative_first_failure
follow_on_execution_does_not_identify_authoritative_first_error
follow_on_execution_does_not_claim_traceback_root_cause
follow_on_execution_does_not_claim_root_cause
follow_on_execution_does_not_claim_retry_success
follow_on_execution_does_not_claim_main_merge_readiness
follow_on_execution_does_not_create_retry_candidate
follow_on_execution_does_not_create_retry_approval
follow_on_execution_does_not_create_retry_execution
follow_on_execution_does_not_create_retry_results_review
follow_on_execution_does_not_create_integration_results_review
follow_on_execution_does_not_mark_integration_successful
follow_on_execution_does_not_generate_successful_integration_digest
follow_on_execution_does_not_push_integration_branch
follow_on_execution_does_not_push_main
follow_on_execution_does_not_delete_integration_branch
follow_on_execution_does_not_delete_worktree
follow_on_execution_does_not_force_push
follow_on_execution_does_not_prune_remotes
follow_on_execution_does_not_modify_tags
follow_on_execution_does_not_modify_staged_evidence
follow_on_execution_does_not_regenerate_evidence
follow_on_execution_does_not_call_providers
follow_on_execution_does_not_acquire_market_data
follow_on_execution_does_not_generate_dataset
follow_on_execution_does_not_recompute_metrics
follow_on_execution_does_not_train_models
follow_on_execution_does_not_score_strategy
follow_on_execution_does_not_generate_trade_recommendations
follow_on_execution_does_not_accept_predictive_usefulness
follow_on_execution_does_not_accept_profitability
follow_on_execution_does_not_authorize_runtime
follow_on_execution_does_not_authorize_broker_execution
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
source_follow_on_approval_remains_source_evidence
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
separate_results_review_required_after_follow_on_execution
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
    """follow_on_execution_after_results_review_created
follow_on_execution_after_results_review_performed
selected_follow_on_package_executed
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
source_authority_acquisition_candidate_created
source_authority_acquisition_candidate_ready_for_results_review
source_authority_acquisition_scope_defined
missing_authority_to_source_evidence_mapping_created
acceptable_source_artifact_inventory_created
operator_provided_evidence_requirements_created
candidate_results_review_requirements_created
source_authority_acquisition_candidate_digest_generated
ready_for_follow_on_execution_results_review""".splitlines()
)
FALSE_FIELDS = tuple(
    """source_authority_acquisition_performed
source_authority_evidence_acquired
external_evidence_acquired
concrete_source_authority_established
safe_source_authority_bound_change_identified
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
pytest_performed_in_execution
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_execution
diagnostic_output_analyzed_in_execution
source_authority_enrichment_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_execution
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_execution
cache_modified_in_execution
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
provider_requests_made_in_execution
market_data_acquisition_performed_in_execution
dataset_generation_performed_in_execution
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines()
)


class MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionError(ValueError):
    """Raised when source approval or execution evidence violates the frozen contract."""


def _iso_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _source_bindings() -> dict[str, Any]:
    bindings = source_candidate._source_bindings()
    bindings.update({
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_execution_digest": SOURCE_EXECUTION_DIGEST,
        "source_authority_enrichment_plan_digest": SOURCE_ENRICHMENT_PLAN_DIGEST,
        "source_missing_authority_inventory_digest": SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST,
        "source_workstream_authority_mapping_digest": SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        "source_results_review_commit": SOURCE_RESULTS_REVIEW_COMMIT,
        "source_results_review_digest": SOURCE_RESULTS_REVIEW_DIGEST,
        "source_enrichment_plan_review_digest": SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST,
        "source_missing_authority_inventory_review_digest": SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST,
        "source_workstream_authority_mapping_review_digest": SOURCE_WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST,
        "source_results_review_manifest_digest": SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST,
        "source_historical_workstream_mapping_review_digest": "f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334",
        "source_historical_planning_results_review_digest": "d6588bfbfca55cec499d1960ab260b703dd754653473ee434b7f6ac100294956",
        "source_follow_on_candidate_commit": SOURCE_FOLLOW_ON_CANDIDATE_COMMIT,
        "source_follow_on_candidate_digest": SOURCE_FOLLOW_ON_CANDIDATE_DIGEST,
        "source_follow_on_candidate_operator_review_commit": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT,
        "source_follow_on_candidate_operator_review_digest": SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST,
        "source_follow_on_approval_commit": SOURCE_FOLLOW_ON_APPROVAL_COMMIT,
        "source_follow_on_approval_digest": SOURCE_FOLLOW_ON_APPROVAL_DIGEST,
    })
    return bindings


SOURCE_BINDINGS = _source_bindings()


def _committed_source_follow_on_approval() -> dict[str, Any]:
    return {
        "artifact_kind": source_approval.ARTIFACT_KIND,
        "approval_status": source_approval.APPROVAL_STATUS,
        "approval_scope": source_approval.APPROVAL_SCOPE,
        source_approval.APPROVAL_DIGEST_KEY: SOURCE_FOLLOW_ON_APPROVAL_DIGEST,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "follow_on_package_selected": True,
        "follow_on_package_approved": True,
        "follow_on_package_authorized_for_future_execution": True,
        "ready_for_follow_on_execution_after_results_review": True,
        "follow_on_execution_performed": False,
        "source_authority_acquisition_candidate_created": False,
        "future_execution_may_create_source_authority_acquisition_candidate": True,
        "future_execution_may_define_source_authority_acquisition_scope": True,
        "future_execution_may_define_evidence_to_obtain_or_bind": True,
        "future_execution_may_map_missing_authority_items_to_candidate_inputs": True,
        "future_execution_may_define_operator_provided_evidence_requirements": True,
        "future_execution_may_define_candidate_results_review_requirements": True,
        "future_execution_may_acquire_source_authority": False,
        "future_execution_may_acquire_external_evidence": False,
        "future_execution_may_create_no_change_disposition": False,
        "future_execution_may_execute_alternate_diagnostics": False,
        "future_execution_may_execute_remediation": False,
        "future_execution_may_run_pytest": False,
        "future_execution_may_run_retry": False,
        "future_execution_may_push_main": False,
    }


def _source_reasons(candidate: Any) -> list[str]:
    if not isinstance(candidate, Mapping):
        return ["SOURCE_FOLLOW_ON_APPROVAL_NOT_AN_OBJECT"]
    expected = _committed_source_follow_on_approval()
    return [
        f"SOURCE_FOLLOW_ON_APPROVAL_{field.upper()}_MISMATCH"
        for field, value in expected.items()
        if candidate.get(field) != value
    ]


def _acquisition_scopes() -> list[dict[str, Any]]:
    scopes = []
    for section_id, requirements in ACQUISITION_SCOPE_REQUIREMENTS.items():
        scopes.append({
            "section_id": section_id,
            "workstream_id": SCOPE_TO_WORKSTREAM[section_id],
            "requirements_to_obtain_or_bind": list(requirements),
            "current_execution_does_not_acquire_evidence": True,
            SCOPE_CHANGE_FLAGS[section_id]: False,
        })
    return scopes


def _acceptable_artifacts_for(section_id: str) -> list[str]:
    shared = ["approved product specification", "approved artifact contract", "approved operator-provided evidence package", "approved source-owning-team statement", "approved reviewed source-digest bundle"]
    specific = {
        "assertion_value_mismatch_source_authority_scope": ["approved expected-value source", "approved actual-value source"],
        "digest_hash_boundary_source_authority_scope": ["approved canonical payload or serialization contract", "approved digest manifest source"],
        "fixture_isolation_determinism_source_authority_scope": ["approved fixture lifecycle document", "approved deterministic execution contract"],
        "schema_field_contract_source_authority_scope": ["approved schema definition", "approved export-surface contract"],
    }
    return shared + specific[section_id]


def _missing_authority_mapping() -> list[dict[str, Any]]:
    mapping: list[dict[str, Any]] = []
    item_number = 1
    section_for_workstream = {workstream: section for section, workstream in SCOPE_TO_WORKSTREAM.items()}
    for workstream_id, requirements in historical_execution.WORKSTREAM_REQUIREMENTS.items():
        section_id = section_for_workstream[workstream_id]
        for requirement in requirements:
            mapping.append({
                "missing_authority_id": f"MA-{item_number:03d}",
                "section_id": section_id,
                "workstream_id": workstream_id,
                "current_status": "MISSING_NOT_ACQUIRED",
                "candidate_requirement_status": "DEFINED_FOR_FUTURE_ACQUISITION_CANDIDATE_ONLY",
                "evidence_to_obtain_or_bind": requirement,
                "acceptable_source_artifact_types": _acceptable_artifacts_for(section_id),
                "minimum_review_before_use": "SEPARATE_SOURCE_AUTHORITY_ACQUISITION_RESULTS_REVIEW_AND_APPROVAL",
                "authority_acquired_now": False, "evidence_acquired_now": False,
                "direct_change_authorized": False,
            })
            item_number += 1
    return mapping


def _source_artifact_inventory() -> list[dict[str, Any]]:
    return [{
        "artifact_type": artifact_type, "allowed_for_future_review": True,
        "acquired_now": False, "requires_results_review_before_use": True,
        "requires_digest_or_provenance_binding": True,
        "may_authorize_direct_change_without_later_approval": False,
    } for artifact_type in ACCEPTABLE_SOURCE_ARTIFACT_TYPES]


def _acquisition_candidate() -> dict[str, Any]:
    return {
        "candidate_type": "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS",
        "candidate_status": "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED",
        "candidate_scope": "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_ONLY_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
        "candidate_basis": "Reviewed source-authority enrichment results identified 30 missing authority items across four sections and no acquired authority.",
        "candidate_boundary": "This candidate defines what authority or evidence must be obtained or bound later. It does not obtain, bind, acquire, validate, or accept the evidence now.",
        "acquisition_scope_sections": _acquisition_scopes(),
        "missing_authority_to_source_evidence_mapping": _missing_authority_mapping(),
        "acceptable_source_artifact_inventory": _source_artifact_inventory(),
        "operator_provided_evidence_requirements": list(OPERATOR_EVIDENCE_REQUIREMENTS),
        "evidence_custody_and_digest_requirements": list(EVIDENCE_CUSTODY_REQUIREMENTS),
        "candidate_results_review_requirements": list(CANDIDATE_RESULTS_REVIEW_REQUIREMENTS),
        "authority_acquired_now": False, "evidence_acquired_now": False,
        "direct_change_authorized": False,
    }


def _common(timestamp: str) -> dict[str, Any]:
    context = source_candidate._source_context()
    return {
        "schema_version": SCHEMA_VERSION, "execution_scope": EXECUTION_SCOPE,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "created_offline": True, "governance_only": True, "follow_on_execution_only": True,
        "source_authority_acquisition_candidate_creation_only": True,
        "source_authority_acquisition_candidate_results_review_required": True,
        "run_timestamp_utc": timestamp,
        "source_follow_on_approval_artifact_kind": source_approval.ARTIFACT_KIND,
        "source_follow_on_approval_status": source_approval.APPROVAL_STATUS,
        "source_follow_on_approval_scope": source_approval.APPROVAL_SCOPE,
        **deepcopy(SOURCE_BINDINGS),
        **deepcopy(context),
        "primary_failure_class": "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED",
        "secondary_failure_classes": [
            "REVIEWED_WORKSTREAMS_ARE_PLANNING_EVIDENCE_NOT_CHANGE_AUTHORITY",
            "PRIORITY_1_FOCUSED_VALIDATION_ALREADY_PASSING_IN_CURRENT_ROOT_CONTEXT",
            "NO_RETAINED_CHANGE_RECORDS_AVAILABLE_FOR_REMEDIATION_SUCCESS",
            "DETACHED_RETRY_FAILURE_REMAINS_AUTHORITATIVE_AND_UNREMEDIATED",
        ],
        "missing_authority_inventory_section_count": 4,
        "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "workstream_mapping_count": 4, "workstream_mapping_status": "PLANNED_NOT_EXECUTED",
        "source_outputs_generated_count": 27, "review_outputs_generated_count": 28,
        "no_change_disposition_input_count": 7, "alternate_diagnostic_input_count": 8,
        "retry_basis_requirement_count": 7,
        "risk_controls": list(RISK_CONTROLS),
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }


def _success(common: dict[str, Any]) -> dict[str, Any]:
    candidate = _acquisition_candidate()
    scopes = candidate["acquisition_scope_sections"]
    mapping = candidate["missing_authority_to_source_evidence_mapping"]
    execution = {
        **common, "artifact_kind": SUCCESS_ARTIFACT_KIND, "execution_status": SUCCESS_STATUS,
        **{field: True for field in TRUE_FIELDS},
        "source_authority_acquisition_candidate": candidate,
        "source_authority_acquisition_scope_definition": scopes,
        "missing_authority_to_source_evidence_mapping": mapping,
        "acceptable_source_artifact_inventory": candidate["acceptable_source_artifact_inventory"],
        "operator_provided_evidence_requirements": candidate["operator_provided_evidence_requirements"],
        "evidence_custody_and_digest_requirements": candidate["evidence_custody_and_digest_requirements"],
        "candidate_results_review_requirements": candidate["candidate_results_review_requirements"],
        "unsupported_claims_boundary": [
            "No source authority or source-authority evidence was acquired.",
            "No direct change authority, no-change disposition, diagnostic, remediation, retry, or main-merge readiness was created.",
            "The failed detached retry remains authoritative; current-root focused validation is not retry evidence.",
        ],
        "outputs_generated": [{"output_id": output_id, "status": OUTPUT_STATUS} for output_id in OUTPUT_IDS],
        "recommended_next_task": SUCCESS_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_AFTER_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION",
        "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
        "blocked_reason": None, "available_data": [], "missing_or_failed_data": [],
    }
    execution[ACQUISITION_CANDIDATE_DIGEST_KEY] = semantic_digest(candidate)
    execution[ACQUISITION_SCOPE_DIGEST_KEY] = semantic_digest(scopes)
    execution[MISSING_AUTHORITY_MAPPING_DIGEST_KEY] = semantic_digest(mapping)
    execution["digest_manifest"] = {
        "source_follow_on_approval_commit": SOURCE_FOLLOW_ON_APPROVAL_COMMIT,
        "source_follow_on_approval_digest": SOURCE_FOLLOW_ON_APPROVAL_DIGEST,
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        ACQUISITION_CANDIDATE_DIGEST_KEY: execution[ACQUISITION_CANDIDATE_DIGEST_KEY],
        ACQUISITION_SCOPE_DIGEST_KEY: execution[ACQUISITION_SCOPE_DIGEST_KEY],
        MISSING_AUTHORITY_MAPPING_DIGEST_KEY: execution[MISSING_AUTHORITY_MAPPING_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    }
    execution[MANIFEST_DIGEST_KEY] = semantic_digest(execution["digest_manifest"])
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = None
    return execution


def _blocked(common: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    reasons = list(dict.fromkeys(reasons))
    blocked_reason = ";".join(reasons)
    execution = {
        **common, "artifact_kind": BLOCKED_ARTIFACT_KIND, "execution_status": BLOCKED_STATUS,
        **{field: False for field in TRUE_FIELDS},
        "follow_on_execution_after_results_review_created": True,
        "source_authority_acquisition_candidate": None,
        "source_authority_acquisition_scope_definition": [],
        "missing_authority_to_source_evidence_mapping": [],
        "acceptable_source_artifact_inventory": [], "operator_provided_evidence_requirements": [],
        "evidence_custody_and_digest_requirements": [], "candidate_results_review_requirements": [],
        "unsupported_claims_boundary": [], "outputs_generated": [], "digest_manifest": None,
        "available_data": [
            "source follow-on approval digest", "source follow-on operator-review digest",
            "source follow-on candidate digest", "source results-review digest", "source execution digest",
            "source approval digest", "source failure diagnosis digest", "source blocked execution reason",
            "retry counts", "Priority 1 validation facts", "missing-authority inventory facts", "workstream facts",
        ],
        "missing_or_failed_data": reasons, "blocked_reason": blocked_reason,
        "recommended_next_task": BLOCKED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_DIAGNOSIS_NOT_CREATED",
        "recommended_action": "DIAGNOSE_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE_BEFORE_ANY_FOLLOW_ON",
        "next_chain": list(BLOCKED_NEXT_CHAIN), "next_gates": list(BLOCKED_NEXT_GATES),
        EXECUTION_DIGEST_KEY: None, ACQUISITION_CANDIDATE_DIGEST_KEY: None,
        ACQUISITION_SCOPE_DIGEST_KEY: None, MISSING_AUTHORITY_MAPPING_DIGEST_KEY: None,
        MANIFEST_DIGEST_KEY: None,
    }
    execution[BLOCKED_MANIFEST_DIGEST_KEY] = semantic_digest({
        "blocked_reason": blocked_reason,
        "source_follow_on_approval_commit": SOURCE_FOLLOW_ON_APPROVAL_COMMIT,
        "source_follow_on_approval_digest": SOURCE_FOLLOW_ON_APPROVAL_DIGEST,
        "missing_or_failed_data": reasons,
    })
    return execution


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": deepcopy(expected),
        "actual": deepcopy(actual), "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(execution: Mapping[str, Any], success: bool) -> list[dict[str, Any]]:
    checks = [_check(f"{field}_bound", value, execution.get(field)) for field, value in SOURCE_BINDINGS.items()]
    fixed = {
        "artifact_kind": SUCCESS_ARTIFACT_KIND if success else BLOCKED_ARTIFACT_KIND,
        "execution_status": SUCCESS_STATUS if success else BLOCKED_STATUS,
        "execution_scope": EXECUTION_SCOPE, "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "retry_failure_counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "priority_1_total_612": 612, "top_10_total_1069": 1069,
        "module_summary_count_29": 29, "failed_or_errored_nodeids_1404": 1404,
        "observable_family_count_4": 4, "observable_evidence_items_188": 188,
        "workstream_count_4": 4, "inventory_sections_4": 4, "inventory_items_30": 30,
        "inventory_status": "MISSING_NOT_ACQUIRED", "mapping_status": "PLANNED_NOT_EXECUTED",
        "source_outputs_27": 27, "review_outputs_28": 28,
    }
    actual = {
        "artifact_kind": execution.get("artifact_kind"), "execution_status": execution.get("execution_status"),
        "execution_scope": execution.get("execution_scope"),
        "selected_follow_on_package": execution.get("selected_follow_on_package"),
        "retry_failure_counts": execution.get("retry_failure_context", {}).get("counts"),
        "priority_1_total_612": execution.get("priority_1_total_nodeids"),
        "top_10_total_1069": execution.get("top_10_count_sum"),
        "module_summary_count_29": execution.get("module_summary_module_count"),
        "failed_or_errored_nodeids_1404": execution.get("failed_or_errored_nodeids_count"),
        "observable_family_count_4": len(execution.get("reviewed_observable_failure_families", [])),
        "observable_evidence_items_188": sum(item.get("observable_evidence_count", 0) for item in execution.get("reviewed_observable_failure_families", [])),
        "workstream_count_4": len(execution.get("reviewed_workstreams", [])),
        "inventory_sections_4": execution.get("missing_authority_inventory_section_count"),
        "inventory_items_30": execution.get("missing_authority_inventory_item_count"),
        "inventory_status": execution.get("missing_authority_items_status"),
        "mapping_status": execution.get("workstream_mapping_status"),
        "source_outputs_27": execution.get("source_outputs_generated_count"),
        "review_outputs_28": execution.get("review_outputs_generated_count"),
    }
    checks.extend(_check(key, value, actual[key]) for key, value in fixed.items())
    for field in TRUE_FIELDS:
        expected = success or field == "follow_on_execution_after_results_review_created"
        checks.append(_check(f"{field}_{str(expected).lower()}", expected, execution.get(field)))
    checks.extend(_check(f"{field}_false", False, execution.get(field)) for field in FALSE_FIELDS)
    checks.extend((
        _check("risk_controls_defined", list(RISK_CONTROLS), execution.get("risk_controls")),
        _check("next_chain_defined", list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN), execution.get("next_chain")),
        _check("next_gates_defined", list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES), execution.get("next_gates")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, execution.get("predictive_usefulness")),
        _check("profitability_not_accepted", NOT_ACCEPTED, execution.get("profitability")),
        _check("runtime_not_authorized", NOT_AUTHORIZED, execution.get("runtime_use")),
        _check("broker_not_authorized", NOT_AUTHORIZED, execution.get("broker_execution")),
        _check("no_tracked_marketflow_files", True, execution.get("no_tracked_marketflow_files")),
        _check("no_tracked_pytest_cache_files", True, execution.get("no_tracked_pytest_cache_files")),
    ))
    if success:
        checks.extend((
            _check("acquisition_candidate", _acquisition_candidate(), execution.get("source_authority_acquisition_candidate")),
            _check("acquisition_scope", _acquisition_scopes(), execution.get("source_authority_acquisition_scope_definition")),
            _check("missing_authority_mapping", _missing_authority_mapping(), execution.get("missing_authority_to_source_evidence_mapping")),
            _check("acceptable_source_artifacts", _source_artifact_inventory(), execution.get("acceptable_source_artifact_inventory")),
            _check("operator_evidence_requirements", list(OPERATOR_EVIDENCE_REQUIREMENTS), execution.get("operator_provided_evidence_requirements")),
            _check("candidate_results_review_requirements", list(CANDIDATE_RESULTS_REVIEW_REQUIREMENTS), execution.get("candidate_results_review_requirements")),
            _check("outputs_generated", [{"output_id": output_id, "status": OUTPUT_STATUS} for output_id in OUTPUT_IDS], execution.get("outputs_generated")),
        ))
    else:
        checks.extend((
            _check("blocked_reason_recorded", True, bool(execution.get("blocked_reason"))),
            _check("blocked_manifest_digest_generated", True, isinstance(execution.get(BLOCKED_MANIFEST_DIGEST_KEY), str)),
            _check("blocked_outputs_empty", [], execution.get("outputs_generated")),
        ))
    return checks


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]], success: bool) -> dict[str, Any]:
    failed = sum(item["status"] != PASS for item in checklist)
    summary = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - failed,
        "failed_checks": failed, "blocker_count": failed,
        **{field: execution.get(field) for field in TRUE_FIELDS + FALSE_FIELDS},
        "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "source_workstream_count": 4, "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188, "source_exit_code": 1,
        "source_stdout_byte_count": 1231380, "source_stderr_byte_count": 0,
        "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "priority_1_top_module_count": 5, "priority_1_total_nodeids": 612,
        "top_5_percentage_of_failed_or_errored_nodeids": "43.58974359", "top_10_count_sum": 1069,
        "missing_authority_inventory_section_count": 4, "missing_authority_inventory_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "workstream_mapping_count": 4,
        "workstream_mapping_status": "PLANNED_NOT_EXECUTED", "source_outputs_generated_count": 27,
        "review_outputs_generated_count": 28,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    if not success:
        summary["blocked_reason"] = execution.get("blocked_reason")
    return summary


def _execution_digest(execution: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(execution))
    for field in ("checklist", "summary", EXECUTION_DIGEST_KEY):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
    *, source_follow_on_approval: dict | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Create only a deterministic acquisition candidate or a fail-closed record."""

    timestamp = "2026-08-23T00:00:00Z" if run_timestamp_utc is None else run_timestamp_utc
    if not _iso_utc(timestamp):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionError("run timestamp invalid")
    approval = _committed_source_follow_on_approval() if source_follow_on_approval is None else deepcopy(source_follow_on_approval)
    reasons = _source_reasons(approval)
    execution = _success(_common(timestamp)) if not reasons else _blocked(_common(timestamp), reasons)
    success = execution["artifact_kind"] == SUCCESS_ARTIFACT_KIND
    execution["checklist"] = _checklist(execution, success)
    execution["summary"] = _summary(execution, execution["checklist"], success)
    if success:
        execution[EXECUTION_DIGEST_KEY] = _execution_digest(execution)
    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(execution)
    return execution


def validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
    execution: dict,
) -> dict[str, Any]:
    """Validate success or blocked output against all frozen evidence and boundaries."""

    error = MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionError
    if not isinstance(execution, dict):
        raise error("execution must be an object")
    kind = execution.get("artifact_kind")
    if kind == SUCCESS_ARTIFACT_KIND:
        success, expected_status = True, SUCCESS_STATUS
    elif kind == BLOCKED_ARTIFACT_KIND:
        success, expected_status = False, BLOCKED_STATUS
    else:
        raise error("artifact kind invalid")
    fixed = {
        "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "schema_version": SCHEMA_VERSION, "selected_follow_on_package": SELECTED_FOLLOW_ON_PACKAGE,
        "source_follow_on_approval_artifact_kind": source_approval.ARTIFACT_KIND,
        "source_follow_on_approval_status": source_approval.APPROVAL_STATUS,
        "source_follow_on_approval_scope": source_approval.APPROVAL_SCOPE,
        **SOURCE_BINDINGS,
    }
    for field, expected in fixed.items():
        if execution.get(field) != expected:
            raise error(f"{field} mismatch")
    common = _common(execution.get("run_timestamp_utc"))
    protected_context_fields = (
        "retry_failure_context", "priority_1_target_modules", "priority_1_top_module_count",
        "priority_1_total_nodeids", "top_5_percentage_of_failed_or_errored_nodeids", "top_10_count_sum",
        "module_summary_module_count", "failed_or_errored_nodeids_count", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families", "reviewed_workstreams",
        "primary_failure_class", "secondary_failure_classes", "missing_authority_inventory_section_count",
        "missing_authority_inventory_item_count", "missing_authority_items_status", "workstream_mapping_count",
        "workstream_mapping_status", "source_outputs_generated_count", "review_outputs_generated_count",
        "no_change_disposition_input_count", "alternate_diagnostic_input_count", "retry_basis_requirement_count",
        "risk_controls",
    )
    for field in protected_context_fields:
        if execution.get(field) != common[field]:
            raise error(f"{field} mismatch")
    for field in ("created_offline", "governance_only", "follow_on_execution_only",
                  "source_authority_acquisition_candidate_creation_only",
                  "source_authority_acquisition_candidate_results_review_required"):
        if execution.get(field) is not True:
            raise error(f"{field} must be true")
    if any(execution.get(field) is not False for field in FALSE_FIELDS):
        raise error("closed execution boundary opened")
    if execution.get("predictive_usefulness") != NOT_ACCEPTED or execution.get("profitability") != NOT_ACCEPTED:
        raise error("acceptance boundary changed")
    if any(execution.get(field) != NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")):
        raise error("runtime or trading boundary changed")
    if success:
        if any(execution.get(field) is not True for field in TRUE_FIELDS):
            raise error("success fact missing")
        content = {
            "source_authority_acquisition_candidate": _acquisition_candidate(),
            "source_authority_acquisition_scope_definition": _acquisition_scopes(),
            "missing_authority_to_source_evidence_mapping": _missing_authority_mapping(),
            "acceptable_source_artifact_inventory": _source_artifact_inventory(),
            "operator_provided_evidence_requirements": list(OPERATOR_EVIDENCE_REQUIREMENTS),
            "evidence_custody_and_digest_requirements": list(EVIDENCE_CUSTODY_REQUIREMENTS),
            "candidate_results_review_requirements": list(CANDIDATE_RESULTS_REVIEW_REQUIREMENTS),
            "outputs_generated": [{"output_id": output_id, "status": OUTPUT_STATUS} for output_id in OUTPUT_IDS],
            "next_chain": list(SUCCESS_NEXT_CHAIN), "next_gates": list(SUCCESS_NEXT_GATES),
            "recommended_next_task": SUCCESS_NEXT_TASK,
            "recommended_next_task_status": "FUTURE_RESULTS_REVIEW_NOT_CREATED",
        }
        for field, expected in content.items():
            if execution.get(field) != expected:
                raise error(f"{field} mismatch")
        digests = {
            ACQUISITION_CANDIDATE_DIGEST_KEY: semantic_digest(execution["source_authority_acquisition_candidate"]),
            ACQUISITION_SCOPE_DIGEST_KEY: semantic_digest(execution["source_authority_acquisition_scope_definition"]),
            MISSING_AUTHORITY_MAPPING_DIGEST_KEY: semantic_digest(execution["missing_authority_to_source_evidence_mapping"]),
            MANIFEST_DIGEST_KEY: semantic_digest(execution["digest_manifest"]),
        }
        for field, expected in digests.items():
            if execution.get(field) != expected or re.fullmatch(r"[0-9a-f]{64}", str(expected)) is None:
                raise error(f"{field} mismatch")
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) is not None or execution.get("blocked_reason") is not None:
            raise error("success carries blocked evidence")
        digest = execution.get(EXECUTION_DIGEST_KEY)
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None or digest != _execution_digest(execution):
            raise error("execution digest mismatch")
    else:
        if execution.get("follow_on_execution_after_results_review_created") is not True:
            raise error("blocked execution record not created")
        if any(execution.get(field) is not False for field in TRUE_FIELDS[1:]):
            raise error("blocked artifact claims execution success")
        if any(execution.get(field) not in (None, []) for field in (
            "source_authority_acquisition_candidate", "source_authority_acquisition_scope_definition",
            "missing_authority_to_source_evidence_mapping", "acceptable_source_artifact_inventory",
            "operator_provided_evidence_requirements", "candidate_results_review_requirements", "outputs_generated",
        )):
            raise error("blocked artifact generated candidate outputs")
        if not execution.get("blocked_reason") or not execution.get("missing_or_failed_data"):
            raise error("blocked reason missing")
        expected_blocked = semantic_digest({
            "blocked_reason": execution["blocked_reason"],
            "source_follow_on_approval_commit": SOURCE_FOLLOW_ON_APPROVAL_COMMIT,
            "source_follow_on_approval_digest": SOURCE_FOLLOW_ON_APPROVAL_DIGEST,
            "missing_or_failed_data": execution["missing_or_failed_data"],
        })
        if execution.get(BLOCKED_MANIFEST_DIGEST_KEY) != expected_blocked:
            raise error("blocked manifest mismatch")
        if any(execution.get(field) is not None for field in (
            EXECUTION_DIGEST_KEY, ACQUISITION_CANDIDATE_DIGEST_KEY, ACQUISITION_SCOPE_DIGEST_KEY,
            MISSING_AUTHORITY_MAPPING_DIGEST_KEY, MANIFEST_DIGEST_KEY,
        )):
            raise error("blocked artifact carries success digest")
        if execution.get("next_chain") != list(BLOCKED_NEXT_CHAIN) or execution.get("next_gates") != list(BLOCKED_NEXT_GATES):
            raise error("blocked next path mismatch")
        if execution.get("recommended_next_task") != BLOCKED_NEXT_TASK:
            raise error("blocked recommendation mismatch")
    checklist = _checklist(execution, success)
    if execution.get("checklist") != checklist or any(item["status"] != PASS for item in checklist):
        raise error("checklist mismatch")
    if execution.get("summary") != _summary(execution, checklist, success):
        raise error("summary mismatch")
    return {
        "artifact_kind": kind, "execution_status": expected_status, "execution_scope": EXECUTION_SCOPE,
        "execution_digest": execution.get(EXECUTION_DIGEST_KEY),
        "blocked_manifest_digest": execution.get(BLOCKED_MANIFEST_DIGEST_KEY),
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = (
    "Source Follow-On Approval", "Source Follow-On Operator Review", "Source Follow-On Candidate",
    "Source Results Review", "Source Execution", "Source Approval", "Source Operator Review", "Source Candidate",
    "Source Failure Diagnosis", "Source Blocked Execution", "Blocked Reason", "Failure Classification",
    "Source Remediation Execution Approval", "Source Plan Results Review", "Source Plan Execution",
    "Source Method Results Review", "Source Method Execution", "Source Diagnostic Results Review",
    "Source Controlled Recapture", "Source Durable Receipt", "Source Planning and Detail Binding Evidence",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Source Authority Enrichment Review Summary", "Missing Authority Inventory Review Summary",
    "Workstream Authority Mapping Review Summary", "Execution Scope", "Selected Follow-On Package",
    "Source Authority Acquisition Candidate", "Acquisition Scope Definition",
    "Missing Authority to Source Evidence Mapping", "Acceptable Source Artifact Inventory",
    "Operator-Provided Evidence Requirements", "Evidence Custody and Digest Requirements",
    "Candidate Results Review Requirements", "Unsupported Claims Boundary", "Success or Blocked Disposition",
    "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
    "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_markdown_v1(
    execution: dict,
) -> str:
    """Render the validated execution record."""

    validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(deepcopy(execution))
    sections = {
        "Source Follow-On Approval": {"commit": execution["source_follow_on_approval_commit"], "digest": execution["source_follow_on_approval_digest"]},
        "Source Follow-On Operator Review": {"commit": execution["source_follow_on_candidate_operator_review_commit"], "digest": execution["source_follow_on_candidate_operator_review_digest"]},
        "Source Follow-On Candidate": {"commit": execution["source_follow_on_candidate_commit"], "digest": execution["source_follow_on_candidate_digest"]},
        "Source Results Review": {"commit": execution["source_results_review_commit"], "digest": execution["source_results_review_digest"]},
        "Source Execution": {"commit": execution["source_execution_commit"], "digest": execution["source_execution_digest"]},
        "Source Approval": {"commit": execution["source_approval_commit"], "digest": execution["source_approval_digest"]},
        "Source Operator Review": {"commit": execution["source_operator_review_commit"], "digest": execution["source_operator_review_digest"]},
        "Source Candidate": {"commit": execution["source_candidate_commit"], "digest": execution["source_candidate_digest"]},
        "Source Failure Diagnosis": {"commit": execution["source_failure_diagnosis_commit"], "digest": execution["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"]},
        "Source Blocked Execution": {"commit": execution["source_blocked_execution_commit"], "digest": execution["source_blocked_manifest_digest"]},
        "Blocked Reason": execution["source_blocked_reason"],
        "Failure Classification": {"primary": execution["primary_failure_class"], "secondary": execution["secondary_failure_classes"]},
        "Source Remediation Execution Approval": {"commit": execution["source_remediation_execution_approval_after_plan_results_review_commit"], "digest": execution["source_remediation_execution_approval_after_plan_results_review_digest"]},
        "Source Plan Results Review": {key: value for key, value in execution.items() if "plan_results_review" in key or key == "source_historical_workstream_mapping_review_digest"},
        "Source Plan Execution": {key: value for key, value in execution.items() if "plan_execution" in key},
        "Source Method Results Review": {key: value for key, value in execution.items() if "method_results_review" in key},
        "Source Method Execution": {key: value for key, value in execution.items() if "method_execution" in key},
        "Source Diagnostic Results Review": {key: value for key, value in execution.items() if "recapture_results_review" in key or "payload_review" in key or "durable_receipt_review" in key},
        "Source Controlled Recapture": {key: value for key, value in execution.items() if "recapture_execution" in key or "recapture_receipt_digest" in key},
        "Source Durable Receipt": {"path": execution["source_durable_receipt_path"], "parsed": execution["diagnostic_receipt_parsed_in_execution"]},
        "Source Planning and Detail Binding Evidence": {key: value for key, value in execution.items() if any(token in key for token in ("planning_digest", "detail_binding", "complete_29", "materialized_payload", "recovery_detail", "module_grouping", "staged_inventory"))},
        "Retry Failure Context": execution["retry_failure_context"],
        "Priority 1 Target Modules": execution["priority_1_target_modules"],
        "Priority 1 Validation Summary": execution["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": execution["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": execution["reviewed_observable_failure_families"],
        "Reviewed Workstreams": execution["reviewed_workstreams"],
        "Source Authority Enrichment Review Summary": {"reviewed": True, "source_authority_acquired": False},
        "Missing Authority Inventory Review Summary": {"sections": 4, "items": 30, "status": "MISSING_NOT_ACQUIRED"},
        "Workstream Authority Mapping Review Summary": {"mappings": 4, "status": "PLANNED_NOT_EXECUTED"},
        "Execution Scope": execution["execution_scope"], "Selected Follow-On Package": execution["selected_follow_on_package"],
        "Source Authority Acquisition Candidate": execution["source_authority_acquisition_candidate"],
        "Acquisition Scope Definition": execution["source_authority_acquisition_scope_definition"],
        "Missing Authority to Source Evidence Mapping": execution["missing_authority_to_source_evidence_mapping"],
        "Acceptable Source Artifact Inventory": execution["acceptable_source_artifact_inventory"],
        "Operator-Provided Evidence Requirements": execution["operator_provided_evidence_requirements"],
        "Evidence Custody and Digest Requirements": execution["evidence_custody_and_digest_requirements"],
        "Candidate Results Review Requirements": execution["candidate_results_review_requirements"],
        "Unsupported Claims Boundary": execution["unsupported_claims_boundary"],
        "Success or Blocked Disposition": {"artifact_kind": execution["artifact_kind"], "status": execution["execution_status"], "blocked_reason": execution["blocked_reason"], "execution_digest": execution.get(EXECUTION_DIGEST_KEY)},
        "Recommendation": {"next_task": execution["recommended_next_task"], "status": execution["recommended_next_task_status"], "action": execution["recommended_action"]},
        "Next Chain": execution["next_chain"], "Next Gates": execution["next_gates"],
        "Risk Controls": execution["risk_controls"],
        "Authority Boundaries": {field: execution[field] for field in FALSE_FIELDS},
        "Checklist Summary": execution["summary"],
        "Guardrails": [field for field in FALSE_FIELDS if execution[field] is False],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Execution After Results Review v1", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
    output_dir: str | Path, *, source_follow_on_approval: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Write the deterministic success or blocked status document."""

    execution = execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
        source_follow_on_approval=source_follow_on_approval, run_timestamp_utc=run_timestamp_utc,
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_markdown_v1(execution), encoding="utf-8")
    return execution


__all__ = [
    "SUCCESS_ARTIFACT_KIND", "BLOCKED_ARTIFACT_KIND", "SUCCESS_STATUS", "BLOCKED_STATUS", "EXECUTION_SCOPE",
    "SELECTED_FOLLOW_ON_PACKAGE", "EXECUTION_DIGEST_KEY", "ACQUISITION_CANDIDATE_DIGEST_KEY",
    "ACQUISITION_SCOPE_DIGEST_KEY", "MISSING_AUTHORITY_MAPPING_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "BLOCKED_MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTED_AFTER_RESULTS_REVIEW_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_READY",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_BLOCKED_AFTER_RESULTS_REVIEW_SOURCE_APPROVAL_OR_BOUNDARY_FAILURE",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_ONLY_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS",
    "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_markdown_v1",
]
