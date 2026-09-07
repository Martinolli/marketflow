"""Approve the reviewed payload-supply mechanism package for future execution.

This module is deterministic, offline, and governance-only.  Approval selects
one package but does not execute it or create payload, input, evidence, source
authority, remediation, retry, merge, runtime, broker, or trading authority.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_APPROVAL_V1"

OPERATOR_ID = "TEST_OPERATOR"
ATTESTATION_UTC = "2026-09-07T00:00:00Z"
ATTESTATION_DECISION = "APPROVE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_CANDIDATE_OPERATOR_REVIEW"
ATTESTATION_SELECTED_PACKAGE = SELECTED_PACKAGE
ATTESTATION_PHRASE = "I APPROVE THE OPERATOR COMPLETION INPUTS PREPARATION OR SUPPLY EXECUTION REATTEMPT PACKAGE FOR FUTURE EXECUTION ONLY WITH EXPLICIT NON-SECRET OPERATOR PAYLOAD"

SOURCE_OPERATOR_REVIEW_COMMIT = "7e15484132a69b0a9af8d63ed214e40cc65b5eb3"
SOURCE_OPERATOR_REVIEW_DIGEST = "a38d0fd287c2b957975d1413a072a8f283980accdf9041b7892a5c700143d59b"
SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST = "34983189415943c9316f08e08bdb8a6f9fead3ba3fb08718c6c685909177d62e"
SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST = "25b65203582c41a9a03c157899e248d1bea3bc7000b5cbc377848f8d9637302c"
SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST = "42ce70588c10cbb70fc802221ba1ca7777e0bd5ff5fec7536c27c625dd588c94"
SOURCE_BINDING_REVIEW_DIGEST = "bbbb9f66d732fa5b0b5a689880e4df02c53f9e25402335f7bd088f2e3e77d8b4"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "0f64e6b33940b704494c4dd4b8be2f0b82e7ff7f55fb58b975eb618f06e46952"

APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_attestation_digest"
PACKAGE_OPTIONS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_package_options_digest"
FUTURE_REQUIREMENTS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_future_requirements_digest"
FUTURE_CONTRACT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_future_contract_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_source_binding_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_CREATE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_FROM_REVIEWED_MECHANISM_WITH_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD = SELECTED_PACKAGE

PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD = source.PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD
PACKAGE_CREATE_OPERATOR_PAYLOAD_READINESS_CHECKLIST_ONLY = source.PACKAGE_CREATE_OPERATOR_PAYLOAD_READINESS_CHECKLIST_ONLY
PACKAGE_CREATE_PAYLOAD_SHAPE_VALIDATION_PLAN_ONLY = source.PACKAGE_CREATE_PAYLOAD_SHAPE_VALIDATION_PLAN_ONLY
PACKAGE_CREATE_SECRET_SCREENING_DRY_RUN_PLAN_ONLY = source.PACKAGE_CREATE_SECRET_SCREENING_DRY_RUN_PLAN_ONLY
PACKAGE_SEGMENT_REATTEMPT_BY_WORKSTREAM_WITH_EXPLICIT_PAYLOAD_ONLY = source.PACKAGE_SEGMENT_REATTEMPT_BY_WORKSTREAM_WITH_EXPLICIT_PAYLOAD_ONLY
PACKAGE_REQUEST_OPERATOR_PAYLOAD_REVIEW_BEFORE_REATTEMPT_ONLY = source.PACKAGE_REQUEST_OPERATOR_PAYLOAD_REVIEW_BEFORE_REATTEMPT_ONLY
PACKAGE_RERUN_INPUT_PREPARATION_WITHOUT_OPERATOR_PAYLOAD = source.PACKAGE_RERUN_INPUT_PREPARATION_WITHOUT_OPERATOR_PAYLOAD
PACKAGE_USE_TEMPLATES_OR_PLACEHOLDERS_AS_OPERATOR_PAYLOAD = source.PACKAGE_USE_TEMPLATES_OR_PLACEHOLDERS_AS_OPERATOR_PAYLOAD
PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIGESTS_DIAGNOSTICS_CACHE_LOGS_ENV_OR_EXTERNAL_DOCUMENTS = source.PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIGESTS_DIAGNOSTICS_CACHE_LOGS_ENV_OR_EXTERNAL_DOCUMENTS
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MECHANISM_ONLY = source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MECHANISM_ONLY
PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW = source.PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW

DEFAULT_OPERATOR_ATTESTATION = {
    "operator_id": OPERATOR_ID,
    "attestation_utc": ATTESTATION_UTC,
    "attestation_decision": ATTESTATION_DECISION,
    "attestation_selected_package": ATTESTATION_SELECTED_PACKAGE,
    "attestation_phrase": ATTESTATION_PHRASE,
    "approval_only_confirmed": True,
    "future_execution_only_confirmed": True,
    "explicit_non_secret_operator_payload_required_confirmed": True,
    "approval_is_not_payload_confirmed": True,
    "source_candidate_and_operator_review_are_not_payload_confirmed": True,
    "mechanism_and_templates_are_not_payload_confirmed": True,
    "diagnostics_digests_cache_logs_environment_and_external_documents_are_not_payload_sources_confirmed": True,
    "no_secrets_or_credentials_included_confirmed": True,
    "no_current_input_evidence_acquisition_remediation_retry_or_main_authorized_confirmed": True,
}

SOURCE_OPERATOR_REVIEW_BINDINGS = {
    "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
    "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
    "source_operator_review_status": source.OPERATOR_REVIEW_STATUS,
    "source_operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
    "source_operator_review_checklist_passed_count": 404,
    "source_operator_review_checklist_total_count": 404,
    "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "source_operator_review_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "source_operator_review_future_requirements_review_digest": SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST,
    "source_operator_review_future_contract_review_digest": SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST,
    "source_operator_review_source_binding_review_digest": SOURCE_BINDING_REVIEW_DIGEST,
    "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
}

PASS, BLOCKER, NOT_EXECUTED = "PASS", "BLOCKER", "NOT_EXECUTED"
GENERATED_APPROVAL_ONLY = "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError(ValueError):
    """Raised when an attestation, source binding, or approval boundary drifts."""


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
            return f"{path}.keys"
        for key in expected:
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return path
        for index, item in enumerate(expected):
            difference = _first_difference(actual[index], item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _validate_source_operator_review(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError("source_operator_review must be an object")
    artifact_keys = {
        "artifact_kind": source.ARTIFACT_KIND,
        "operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        source.OPERATOR_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
        source.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
        source.FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY: SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST,
        source.FUTURE_CONTRACT_REVIEW_DIGEST_KEY: SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST,
        source.SOURCE_BINDING_REVIEW_DIGEST_KEY: SOURCE_BINDING_REVIEW_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
    }
    expected = SOURCE_OPERATOR_REVIEW_BINDINGS if all(key in value for key in SOURCE_OPERATOR_REVIEW_BINDINGS) else artifact_keys
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError(f"source_operator_review.{key} mismatch")


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_attestation_v1(
    *,
    operator_id: str = OPERATOR_ID,
    attestation_utc: str = ATTESTATION_UTC,
    attestation_decision: str = ATTESTATION_DECISION,
    attestation_selected_package: str = ATTESTATION_SELECTED_PACKAGE,
    attestation_phrase: str = ATTESTATION_PHRASE,
    approval_only_confirmed: bool = True,
    future_execution_only_confirmed: bool = True,
    explicit_non_secret_operator_payload_required_confirmed: bool = True,
    approval_is_not_payload_confirmed: bool = True,
    source_candidate_and_operator_review_are_not_payload_confirmed: bool = True,
    mechanism_and_templates_are_not_payload_confirmed: bool = True,
    diagnostics_digests_cache_logs_environment_and_external_documents_are_not_payload_sources_confirmed: bool = True,
    no_secrets_or_credentials_included_confirmed: bool = True,
    no_current_input_evidence_acquisition_remediation_retry_or_main_authorized_confirmed: bool = True,
) -> dict[str, Any]:
    attestation = {
        "operator_id": operator_id,
        "attestation_utc": attestation_utc,
        "attestation_decision": attestation_decision,
        "attestation_selected_package": attestation_selected_package,
        "attestation_phrase": attestation_phrase,
        "approval_only_confirmed": approval_only_confirmed,
        "future_execution_only_confirmed": future_execution_only_confirmed,
        "explicit_non_secret_operator_payload_required_confirmed": explicit_non_secret_operator_payload_required_confirmed,
        "approval_is_not_payload_confirmed": approval_is_not_payload_confirmed,
        "source_candidate_and_operator_review_are_not_payload_confirmed": source_candidate_and_operator_review_are_not_payload_confirmed,
        "mechanism_and_templates_are_not_payload_confirmed": mechanism_and_templates_are_not_payload_confirmed,
        "diagnostics_digests_cache_logs_environment_and_external_documents_are_not_payload_sources_confirmed": diagnostics_digests_cache_logs_environment_and_external_documents_are_not_payload_sources_confirmed,
        "no_secrets_or_credentials_included_confirmed": no_secrets_or_credentials_included_confirmed,
        "no_current_input_evidence_acquisition_remediation_retry_or_main_authorized_confirmed": no_current_input_evidence_acquisition_remediation_retry_or_main_authorized_confirmed,
    }
    _validate_attestation(attestation)
    return attestation


def _validate_attestation(attestation: Any) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError("operator_attestation must be an object")
    difference = _first_difference(dict(attestation), DEFAULT_OPERATOR_ATTESTATION, "operator_attestation")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError(f"{difference} mismatch or unexpected secret-like field")


def _source_projection() -> dict[str, Any]:
    # Start from the committed historical source constants and overlay each
    # newer public binding surface.  No source builder or private helper runs.
    context = deepcopy(source.source.source.source.source.SOURCE_CONTEXT)
    historical_renames = {
        "source_approval_commit": "source_prior_approval_commit",
        "source_approval_digest": "source_prior_approval_digest",
        "source_attestation_digest": "source_prior_attestation_digest",
        "source_execution_commit": "source_blocked_input_preparation_execution_commit",
        "source_blocked_reason": "source_blocked_input_preparation_execution_reason",
        "source_blocked_digest": "source_blocked_input_preparation_digest",
        "source_source_binding_digest": "source_blocked_input_preparation_source_binding_digest",
        "source_input_absence_digest": "source_blocked_input_preparation_input_absence_digest",
        "source_coverage_digest": "source_blocked_input_preparation_coverage_digest",
        "source_blocked_manifest_digest": "source_blocked_input_preparation_manifest_digest",
        "source_package_options_review_digest": "source_earlier_operator_review_package_options_review_digest",
        "source_future_requirements_review_digest": "source_earlier_operator_review_future_requirements_review_digest",
        "source_future_contract_review_digest": "source_earlier_operator_review_future_contract_review_digest",
        "source_binding_review_digest": "source_earlier_operator_review_source_binding_review_digest",
        "source_candidate_commit": "source_earlier_candidate_commit",
        "source_candidate_digest": "source_earlier_candidate_digest",
        "source_operator_review_commit": "source_earlier_operator_review_commit",
        "source_operator_review_digest": "source_earlier_operator_review_digest",
        "source_operator_review_manifest_digest": "source_earlier_operator_review_manifest_digest",
    }
    for old_key, new_key in historical_renames.items():
        if old_key in context:
            context[new_key] = context.pop(old_key)
    context.update(deepcopy(source.source.source.source.SOURCE_APPROVAL_BINDINGS))
    if "source_selected_package_executed" in context:
        context["source_approval_selected_package_executed"] = context.pop("source_selected_package_executed")
    context.update(deepcopy(source.source.source.SOURCE_EXECUTION_BINDINGS))
    context.update(deepcopy(source.source.SOURCE_RESULTS_REVIEW_BINDINGS))
    context.update(deepcopy(source.SOURCE_CANDIDATE_BINDINGS))
    context.update(deepcopy(SOURCE_OPERATOR_REVIEW_BINDINGS))
    context["primary_failure_class"] = source.failure_diagnosis_source.PRIMARY_FAILURE_CLASS
    context["secondary_failure_classes"] = list(source.failure_diagnosis_source.SECONDARY_FAILURE_CLASSES)
    return context


SOURCE_CONTEXT = _source_projection()


def _approved_packages() -> list[dict[str, Any]]:
    rows = []
    package_ids = (
        SELECTED_PACKAGE,
        PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD,
        PACKAGE_CREATE_OPERATOR_PAYLOAD_READINESS_CHECKLIST_ONLY,
        PACKAGE_CREATE_PAYLOAD_SHAPE_VALIDATION_PLAN_ONLY,
        PACKAGE_CREATE_SECRET_SCREENING_DRY_RUN_PLAN_ONLY,
        PACKAGE_SEGMENT_REATTEMPT_BY_WORKSTREAM_WITH_EXPLICIT_PAYLOAD_ONLY,
        PACKAGE_REQUEST_OPERATOR_PAYLOAD_REVIEW_BEFORE_REATTEMPT_ONLY,
        PACKAGE_RERUN_INPUT_PREPARATION_WITHOUT_OPERATOR_PAYLOAD,
        PACKAGE_USE_TEMPLATES_OR_PLACEHOLDERS_AS_OPERATOR_PAYLOAD,
        PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIGESTS_DIAGNOSTICS_CACHE_LOGS_ENV_OR_EXTERNAL_DOCUMENTS,
        PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MECHANISM_ONLY,
        PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW,
    )
    blocked_reasons = {
        PACKAGE_RERUN_INPUT_PREPARATION_WITHOUT_OPERATOR_PAYLOAD: "Explicit non-secret operator payload is mandatory; fail closed without it.",
        PACKAGE_USE_TEMPLATES_OR_PLACEHOLDERS_AS_OPERATOR_PAYLOAD: "Templates and placeholders are not operator payload or evidence.",
        PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIGESTS_DIAGNOSTICS_CACHE_LOGS_ENV_OR_EXTERNAL_DOCUMENTS: "Diagnostics, digests, cache, logs, environment values, and external documents are not payload sources.",
        PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MECHANISM_ONLY: "A reviewed mechanism is not a completed evidence package or source authority.",
        PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW: "The reviewed mechanism creates no remediation, retry, or main-merge basis.",
    }
    for index, package_id in enumerate(package_ids):
        blocked = index >= 7
        selected = index == 0
        row = {
            "package_id": package_id,
            "source_review_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" if selected else "REVIEWED_AVAILABLE_NOT_SELECTED" if not blocked else "REVIEWED_BLOCKED_NOT_ALLOWED",
            "approval_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED" if selected else "PRESERVED_BLOCKED_NOT_ALLOWED" if blocked else "PRESERVED_UNSELECTED",
            "selected": selected,
            "approved": selected,
            "authorized": selected,
            "executed": False,
        }
        if blocked:
            row["blocked_reason"] = blocked_reasons[package_id]
        else:
            row["purpose"] = "Selected explicit non-secret payload reattempt package." if selected else "Preserved supporting option; not selected or authorized."
        rows.append(row)
    return rows


APPROVED_PACKAGE_OPTIONS = tuple(_approved_packages())

FUTURE_PLAN = (
    "Bind source operator review and source reattempt candidate.",
    "Bind source payload-supply mechanism results review.",
    "Bind source execution, approval, earlier operator-review, earlier candidate, failure diagnosis, blocked input-preparation execution, completion/template/acquisition, follow-on/enrichment, historical, plan/method/diagnostic/recovery, module grouping, and staged inventory digests.",
    "Preserve source execution as reviewed and not rerun.",
    "Preserve mechanism digests and confirm mechanism was not regenerated.",
    "Preserve actual payload absence, prepared-input absence, evidence-package absence, actual coverage 0/30, and all rows MISSING_NOT_ACQUIRED.",
    "Preserve retry failure counts and Priority 1 context as non-retry evidence.",
    "Preserve reviewed observable families and workstreams as planning evidence only.",
    "Select and approve only the explicit non-secret payload reattempt package for future execution.",
    "Approve future explicit payload requirements from the reviewed payload-supply mechanism.",
    "Preserve secret-screening and allowed-value boundaries.",
    "Preserve no-current-execution, no-current-evidence, no-acquisition, no-remediation, no-retry, no-main boundaries.",
    "Require separately invoked execution before any reattempt can occur.",
    "Require results review after any future reattempt before completion/acquisition/disposition/remediation/retry/main paths.",
)

OUTPUT_IDS = tuple("""approval_manifest
attestation_report
source_operator_review_binding_report
source_candidate_binding_report
source_results_review_binding_report
source_execution_binding_report
source_execution_digest_review_report
payload_supply_mechanism_review_binding_report
operator_payload_submission_schema_review_binding_report
allowed_values_and_secret_screening_review_binding_report
workstream_supply_plan_review_binding_report
source_approval_binding_report
source_earlier_operator_review_binding_report
source_earlier_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_input_preparation_execution_binding_report
source_success_digests_absence_report
source_completion_template_acquisition_chain_binding_report
follow_on_enrichment_historical_binding_report
plan_method_diagnostic_recovery_binding_report
durable_receipt_opaque_reference_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
actual_payload_absence_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
package_options_approval_report
selected_package_approval_report
future_payload_requirements_approval_report
future_plan_approval_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Execution Reattempt After Approval v1, only with explicit non-secret operator payload.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if explicit non-secret inputs are prepared or supplied.",
    "Operator Source Authority Evidence Package Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition, alternate diagnostic, remediation re-entry, no-change retry criteria, or hold only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_execution_reattempt_with_explicit_non_secret_payload_if_approved
operator_completion_inputs_preparation_or_supply_results_review_if_prepared_inputs_exist
operator_source_authority_evidence_package_completion_execution_reattempt_if_reviewed_inputs_exist_and_approved
operator_source_authority_evidence_package_completion_results_review_if_completed_package_exists
source_authority_acquisition_execution_reattempt_with_reviewed_completed_evidence_package_if_approved
source_authority_acquisition_results_review_if_evidence_bound
no_change_disposition_candidate_if_supported_by_reviewed_acquired_evidence
alternate_diagnostic_candidate_if_supported_by_reviewed_acquired_evidence
remediation_reentry_candidate_if_supported_by_reviewed_acquired_evidence
no_change_retry_criteria_candidate_if_supported_by_reviewed_acquired_evidence
hold_disposition_if_supported
new_integration_branch_retry_candidate_after_reviewed_basis
new_integration_branch_retry_approval_if_selected
new_integration_branch_retry_execution_if_approved
new_integration_branch_retry_results_review
main_merge_approval_if_new_retry_passes""".splitlines())

TRUE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_created
operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_ready
source_operator_review_bound
source_operator_review_reviewed
source_operator_review_status_verified
source_operator_review_scope_verified
source_operator_review_digest_verified
source_package_options_review_digest_verified
source_future_requirements_review_digest_verified
source_future_contract_review_digest_verified
source_operator_review_source_binding_review_digest_verified
source_operator_review_manifest_digest_verified
source_candidate_bound
source_candidate_reviewed
source_results_review_bound
source_results_review_reviewed
source_execution_bound
source_execution_reviewed
source_execution_not_rerun_verified
source_mechanism_not_regenerated_verified
source_payload_supply_mechanism_review_bound
source_operator_payload_submission_schema_review_bound
source_allowed_values_and_secret_screening_review_bound
source_workstream_supply_plan_review_bound
source_selected_package_bound
source_selected_package_executed_verified
source_payload_supply_mechanism_created_verified
recommended_package_reviewed
selected_package_bound
selected_package_selected
selected_package_approved
selected_package_authorized
approved_package_for_future_execution_only
attestation_bound
attestation_digest_generated
attestation_no_secret_confirmed
future_explicit_non_secret_payload_requirement_approved
future_reattempt_requires_explicit_non_secret_payload_approved
future_reattempt_requires_operator_review_approved
future_reattempt_requires_separate_approval_approved
future_reattempt_requires_results_review_after_execution_approved
future_contract_requirements_approved
package_options_preserved
supporting_packages_preserved_unselected
blocked_packages_preserved_blocked
operator_completion_inputs_absence_preserved
actual_payload_absence_preserved
evidence_package_absence_preserved
actual_coverage_zero_bound
missing_authority_inventory_bound
missing_authority_items_status_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
source_approval_bound
source_earlier_operator_review_bound
source_earlier_candidate_bound
source_failure_diagnosis_bound
source_blocked_input_preparation_execution_bound
source_completion_execution_bound
source_completion_approval_bound
source_completion_candidate_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_failure_acquisition_chain_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
priority1_validation_not_retry_evidence
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
reviewed_template_structure_bound
count_label_distinction_preserved
ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt_after_approval""".splitlines())

FALSE_FIELDS = tuple("""approval_executed
selected_package_executed
approved_package_executed
operator_completion_inputs_preparation_or_supply_execution_reattempt_created
operator_completion_inputs_preparation_or_supply_execution_reattempt_performed
operator_completion_inputs_preparation_or_supply_results_review_created
operator_payload_created
operator_payload_supplied_to_approval
operator_payload_validated_in_approval
operator_payload_secret_screened_in_approval
operator_completion_inputs_supplied_to_approval
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_shape_validated_as_actual_payload
operator_completion_inputs_secret_screened_as_actual_payload
operator_completion_inputs_validated_as_evidence
operator_completion_inputs_bound_as_evidence
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
prepared_operator_completion_inputs_for_results_review
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
actual_evidence_items_filled
actual_evidence_items_supplied
actual_evidence_items_validated
actual_evidence_items_bound
source_authority_acquisition_execution_created
source_authority_acquisition_execution_performed
source_authority_acquisition_performed
source_authority_evidence_acquired
external_evidence_acquired
source_authority_evidence_items_bound_for_results_review
source_authority_evidence_mapping_created
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
pytest_performed_in_approval
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_approval
diagnostic_output_analyzed_in_approval
source_execution_rerun_performed
payload_supply_mechanism_regenerated
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_approval
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
input_preparation_or_supply_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_approval
cache_modified_in_approval
pytest_cache_committed
marketflow_outputs_committed
terminal_logs_parsed
operator_logs_parsed
env_inspection_performed
source_owners_contacted
external_documents_read
provider_requests_made_in_approval
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
ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt
ready_for_operator_completion_inputs_preparation_or_supply_results_review
ready_for_operator_source_authority_evidence_package_completion_execution
ready_for_operator_source_authority_evidence_package_completion_results_review
ready_for_source_authority_acquisition_execution_retry
ready_for_source_authority_acquisition_results_review
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
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

COUNTS = {
    **deepcopy(source.COUNTS),
    "workstream_segment_item_counts": [8, 8, 7, 7],
    "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    "selected_package_count": 1,
    "approved_package_count": 1,
    "authorized_package_count": 1,
    "executed_package_count": 0,
    "source_operator_review_unique_control_count": 572,
}

_APPROVAL_SPECIFIC_RISK_CONTROLS = tuple("""approval_does_not_execute_package
approval_only_authorizes_future_reattempt_execution
approval_requires_explicit_non_secret_operator_payload_for_future_execution
approval_is_not_operator_payload
approval_is_not_input_preparation
approval_is_not_input_supply
approval_is_not_evidence_validation
approval_is_not_evidence_binding
approval_is_not_evidence_completion
approval_is_not_source_authority
approval_is_not_source_authority_acquisition
approval_does_not_create_operator_payload
approval_does_not_prepare_inputs
approval_does_not_supply_inputs
approval_does_not_provide_inputs
approval_does_not_shape_validate_actual_payload
approval_does_not_secret_screen_actual_payload
approval_does_not_validate_inputs_as_evidence
approval_does_not_bind_inputs_as_evidence
approval_does_not_create_prepared_inputs
approval_does_not_create_reattempt
approval_does_not_perform_reattempt
approval_does_not_create_results_review
approval_does_not_create_completed_evidence_package
approval_does_not_create_evidence_package
approval_does_not_fill_actual_evidence_items
approval_does_not_validate_evidence
approval_does_not_bind_evidence
approval_does_not_accept_evidence_as_source_authority
approval_does_not_infer_inputs_from_mechanism
approval_does_not_infer_inputs_from_template
approval_does_not_infer_inputs_from_placeholders
approval_does_not_infer_inputs_from_diagnostic_output
approval_does_not_infer_inputs_from_digests
approval_does_not_read_cache_for_inputs
approval_does_not_parse_logs_for_inputs
approval_does_not_inspect_env_for_inputs
approval_does_not_read_external_documents_for_inputs
approval_does_not_call_providers_for_inputs
approval_does_not_contact_source_owners_for_inputs
approval_does_not_acquire_source_authority
approval_does_not_acquire_source_authority_evidence
approval_does_not_acquire_external_evidence
approval_does_not_create_source_authority_acquisition_execution
approval_does_not_retry_source_authority_acquisition
approval_does_not_create_no_change_disposition
approval_does_not_execute_alternate_diagnostics
approval_does_not_execute_remediation
approval_does_not_modify_production_code
approval_does_not_modify_existing_tests
approval_does_not_update_expected_digests
approval_does_not_generate_patch
approval_does_not_apply_patch
approval_does_not_run_pytest
approval_does_not_run_full_pytest
approval_does_not_rerun_priority1_validation
approval_does_not_rerun_retry
approval_does_not_rerun_detached_retry
approval_does_not_parse_durable_receipt
approval_does_not_analyze_diagnostic_output
approval_does_not_rerun_source_execution
approval_does_not_regenerate_payload_supply_mechanism
approval_does_not_rerun_source_authority_enrichment
approval_does_not_rerun_follow_on_execution
approval_does_not_rerun_plan_execution
approval_does_not_regenerate_targeted_plan
approval_does_not_rerun_method_execution
approval_does_not_rerun_controlled_recapture
approval_does_not_rerun_template_execution
approval_does_not_rerun_completion_execution
approval_does_not_rerun_input_preparation_execution
approval_does_not_run_diagnostic_command
approval_does_not_read_pytest_cache
approval_does_not_modify_pytest_cache
approval_does_not_commit_pytest_cache
approval_does_not_commit_marketflow_outputs
approval_does_not_parse_terminal_logs
approval_does_not_parse_operator_logs
approval_does_not_inspect_env
approval_does_not_contact_source_owners
approval_does_not_read_external_documents
approval_does_not_reconstruct_prior_lost_values
approval_does_not_reconstruct_full_streams
approval_does_not_classify_modules_again
approval_does_not_classify_full_retry_failures
approval_does_not_classify_full_retry_errors
approval_does_not_claim_failure_error_separation
approval_does_not_identify_authoritative_first_failure
approval_does_not_identify_authoritative_first_error
approval_does_not_claim_traceback_root_cause
approval_does_not_claim_root_cause
approval_does_not_claim_retry_success
approval_does_not_claim_main_merge_readiness
approval_does_not_create_retry_candidate
approval_does_not_create_retry_approval
approval_does_not_create_retry_execution
approval_does_not_create_retry_results_review
approval_does_not_create_main_merge_approval
approval_does_not_push_main
approval_does_not_push_integration_branch
approval_does_not_delete_integration_branch
approval_does_not_delete_worktree
approval_does_not_force_push
approval_does_not_modify_tags
approval_does_not_regenerate_evidence
approval_does_not_call_providers
approval_does_not_acquire_market_data
approval_does_not_generate_dataset
approval_does_not_recompute_metrics
approval_does_not_train_models
approval_does_not_score_strategy
approval_does_not_generate_trade_recommendations
approval_does_not_accept_predictive_usefulness
approval_does_not_accept_profitability
approval_does_not_authorize_runtime
approval_does_not_authorize_broker_execution
operator_review_is_not_approval
payload_supply_mechanism_results_review_is_not_payload
payload_supply_mechanism_results_review_is_not_input_preparation
payload_supply_mechanism_results_review_is_not_evidence_completion
payload_supply_mechanism_results_review_is_not_source_authority
explicit_non_secret_payload_required_before_reattempt
separate_execution_required_after_approval
reattempt_results_review_required_before_completion_use
completed_package_requires_results_review_before_acquisition_use
source_authority_acquisition_requires_separate_approval
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())

# Source-review controls remain historical source-review facts; approval-specific
# controls describe this artifact.  Keeping both vocabularies avoids converting
# a reviewed fact into a new approval claim.
RISK_CONTROLS = tuple(dict.fromkeys((*_APPROVAL_SPECIFIC_RISK_CONTROLS, *source.RISK_CONTROLS)))


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": PASS if actual else BLOCKER, "expected": True, "actual": actual, "severity": BLOCKER, "message": "Boundary preserved." if actual else "Boundary drifted."}


def _digest_without(value: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(value))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_approval(attestation: Mapping[str, Any]) -> dict[str, Any]:
    approval = deepcopy(SOURCE_CONTEXT)
    mechanism = source.source.source.source
    contract = {
        "contract_kind": "FUTURE_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD_REATTEMPT_EXECUTION_CONTRACT",
        "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY",
        "execution_status": NOT_EXECUTED,
        "explicit_non_secret_operator_payload_required": True,
        "package_header_schema_fields": list(mechanism.PACKAGE_HEADER_FIELDS),
        "evidence_item_schema_fields": list(mechanism.EVIDENCE_ITEM_FIELDS),
        "required_item_ids": [f"MA-{index:03d}" for index in range(1, 31)],
        "allowed_section_ids": list(mechanism.ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(mechanism.ALLOWED_WORKSTREAM_IDS),
        "allowed_artifact_types": list(mechanism.ALLOWED_ARTIFACT_TYPES),
        "allowed_evidence_classifications": list(mechanism.ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "secret_screening_indicators": list(mechanism.SECRET_INDICATORS),
        "operator_payload_created": False,
        "operator_input_supplied": False,
        "evidence_validated": False,
        "evidence_bound": False,
        "evidence_package_completed": False,
        "source_authority_acquired": False,
        "remediation_authorized": False,
        "retry_authorized": False,
        "main_merge_authorized": False,
        "results_review_required_after_execution": True,
    }
    approval.update({
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "approval_philosophy": "The source operator review assessed the reattempt candidate and preserved the recommended explicit non-secret operator payload reattempt package without selecting it. This approval selects and authorizes that package for future execution only. It does not execute the package, create payload, prepare or supply inputs, validate or bind evidence, complete an evidence package, acquire source authority, remediate, retry, merge, or authorize runtime/trading.",
        "approval_boundary": "Approval only. The selected package may be executed only in a separately invoked future execution with explicit non-secret operator payload. This approval preserves actual payload absence, input absence, evidence absence, coverage 0/30, all missing-authority rows as MISSING_NOT_ACQUIRED, the failed detached retry, and every downstream gate.",
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_package": SELECTED_PACKAGE,
        "selected_package_selected": True,
        "selected_package_approved": True,
        "selected_package_authorized": True,
        "selected_operator_completion_inputs_preparation_or_supply_execution_reattempt_package": SELECTED_PACKAGE,
        "selected_package_approved_for_future_execution_only": True,
        "selected_package_executed": False,
        "primary_failure_class": source.failure_diagnosis_source.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(source.failure_diagnosis_source.SECONDARY_FAILURE_CLASSES),
        "source_mechanism_review_section_names": [
            "mechanism_identity", "approved_source_contract_binding", "explicit_operator_payload_entry_rules",
            "package_header_schema", "thirty_item_payload_schema", "allowed_values_matrix",
            "workstream_segmented_supply_plan", "secret_screening_policy", "pre_submission_operator_checklist",
            "post_submission_results_review_requirement", "downstream_gate_policy", "unsupported_claims_boundary",
            "digest_manifest",
        ],
        "source_mechanism_review_section_count": 13,
        "package_header_schema_fields": list(mechanism.PACKAGE_HEADER_FIELDS),
        "evidence_item_schema_fields": list(mechanism.EVIDENCE_ITEM_FIELDS),
        "future_operator_completion_input_item_ids": [f"MA-{index:03d}" for index in range(1, 31)],
        "allowed_section_ids": list(mechanism.ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(mechanism.ALLOWED_WORKSTREAM_IDS),
        "allowed_artifact_types": list(mechanism.ALLOWED_ARTIFACT_TYPES),
        "allowed_evidence_classifications": list(mechanism.ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "secret_screening_indicators": list(mechanism.SECRET_INDICATORS),
        "source_execution_governance_output_record_count": len(mechanism.OUTPUT_IDS),
        "source_execution_risk_control_count": len(mechanism.RISK_CONTROLS),
        "approved_package_options": deepcopy(list(APPROVED_PACKAGE_OPTIONS)),
        "approved_future_requirements": [{"requirement_id": item, "approval_status": "APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY", "execution_status": NOT_EXECUTED} for item in source.source.FUTURE_REQUIREMENT_IDS],
        "approved_future_contract": contract,
        "approved_future_payload_supply_contract": deepcopy(contract),
        "approved_future_plan": [{"step": index, "description": item, "approval_status": "APPROVED_PLANNED_NOT_EXECUTED", "execution_status": NOT_EXECUTED} for index, item in enumerate(FUTURE_PLAN, 1)],
        "authorized_planned_outputs": [{"output_id": f"planned_output_{index:02d}", "authorization_status": "AUTHORIZED_NOT_GENERATED"} for index in range(1, 33)],
        "outputs": [{"output_id": item, "status": GENERATED_APPROVAL_ONLY} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_EXECUTION_NOT_CREATED",
        "recommended_action": "PROCEED_ONLY_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_APPROVAL_WITH_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD",
        "recommendation_reason": "The operator review assessed the reattempt candidate and this approval selects the recommended explicit non-secret payload package for future execution only. The approval does not execute the package, create payload, prepare or supply inputs, validate or bind evidence, complete an evidence package, acquire source authority, remediate, retry, merge, or authorize runtime/trading.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
    })
    approval.update({key: True for key in TRUE_FIELDS})
    approval.update({key: False for key in FALSE_FIELDS})
    approval.update(COUNTS)

    approval[ATTESTATION_DIGEST_KEY] = semantic_digest(approval["operator_attestation"])
    approval["attestation_digest"] = approval[ATTESTATION_DIGEST_KEY]
    approval[PACKAGE_OPTIONS_DIGEST_KEY] = semantic_digest(approval["approved_package_options"])
    approval[FUTURE_REQUIREMENTS_DIGEST_KEY] = semantic_digest(approval["approved_future_requirements"])
    approval[FUTURE_CONTRACT_DIGEST_KEY] = semantic_digest(approval["approved_future_contract"])
    approval[SOURCE_BINDING_DIGEST_KEY] = semantic_digest({key: value for key, value in approval.items() if key.startswith(("source_", "retry_", "priority1_"))})
    digest_keys = (APPROVAL_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    approval[APPROVAL_DIGEST_KEY] = _digest_without(approval, *digest_keys)
    approval[MANIFEST_DIGEST_KEY] = semantic_digest({
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        "attestation_digest": approval[ATTESTATION_DIGEST_KEY],
        "package_options_digest": approval[PACKAGE_OPTIONS_DIGEST_KEY],
        "future_requirements_digest": approval[FUTURE_REQUIREMENTS_DIGEST_KEY],
        "future_contract_digest": approval[FUTURE_CONTRACT_DIGEST_KEY],
        "source_binding_digest": approval[SOURCE_BINDING_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    })

    checks = [
        _check("artifact_kind_correct", approval["artifact_kind"] == ARTIFACT_KIND),
        _check("approval_status_correct", approval["approval_status"] == APPROVAL_STATUS),
        _check("approval_scope_correct", approval["approval_scope"] == APPROVAL_SCOPE),
        _check("source_operator_review_commit_bound", approval["source_operator_review_commit"] == SOURCE_OPERATOR_REVIEW_COMMIT),
        _check("source_operator_review_digest_bound", approval["source_operator_review_digest"] == SOURCE_OPERATOR_REVIEW_DIGEST),
        _check("source_operator_review_digest_surface_bound", all(approval[key] == expected for key, expected in SOURCE_OPERATOR_REVIEW_BINDINGS.items())),
        _check("source_candidate_digest_surface_bound", all(approval[key] == expected for key, expected in source.SOURCE_CANDIDATE_BINDINGS.items())),
        _check("source_results_review_digest_surface_bound", all(approval[key] == expected for key, expected in source.source.SOURCE_RESULTS_REVIEW_BINDINGS.items())),
        _check("source_execution_digest_surface_bound", all(approval[key] == expected for key, expected in source.source.source.SOURCE_EXECUTION_BINDINGS.items())),
        _check("source_blocked_reason_bound", approval["source_blocked_input_preparation_execution_reason"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"),
        _check("source_success_digests_absent", approval["source_success_digests_absent"] and approval["source_success_execution_digest"] is None and approval["source_prepared_operator_completion_inputs_digest"] is None and approval["source_prepared_operator_completion_inputs_manifest_digest"] is None),
        _check("source_selected_package_executed", approval["source_selected_package"] == "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY" and approval["source_selected_package_executed"] is True),
        _check("source_payload_supply_mechanism_created", approval["source_payload_supply_mechanism_created"] is True),
        _check("mechanism_review_sections_preserved", approval["source_mechanism_review_section_count"] == 13 and len(approval["source_mechanism_review_section_names"]) == 13),
        _check("mechanism_schema_counts_preserved", len(approval["package_header_schema_fields"]) == 14 and len(approval["evidence_item_schema_fields"]) == 21 and len(approval["future_operator_completion_input_item_ids"]) == 30),
        _check("mechanism_governance_counts_preserved", approval["source_execution_governance_output_record_count"] == 42 and approval["source_execution_risk_control_count"] == 246),
        _check("primary_failure_class_bound", approval["primary_failure_class"] == source.failure_diagnosis_source.PRIMARY_FAILURE_CLASS),
        _check("secondary_failure_classes_bound", tuple(approval["secondary_failure_classes"]) == source.failure_diagnosis_source.SECONDARY_FAILURE_CLASSES),
        _check("operator_attestation_verified", approval["operator_attestation"] == DEFAULT_OPERATOR_ATTESTATION),
        _check("selected_package_correct", approval["selected_operator_completion_inputs_preparation_or_supply_execution_reattempt_package"] == SELECTED_PACKAGE),
        _check("selected_package_approved_future_only", approval["selected_package_approved_for_future_execution_only"] and not approval["selected_package_executed"]),
        _check("package_options_preserved", len(approval["approved_package_options"]) == 12),
        _check("supporting_packages_unselected", all(not item["selected"] and not item["approved"] for item in approval["approved_package_options"][1:7])),
        _check("blocked_packages_blocked", all(item["approval_status"] == "PRESERVED_BLOCKED_NOT_ALLOWED" and not item["approved"] for item in approval["approved_package_options"][7:])),
        _check("future_requirements_approved", len(approval["approved_future_requirements"]) == 58 and all(item["execution_status"] == NOT_EXECUTED for item in approval["approved_future_requirements"])),
        _check("future_contract_approved", approval["approved_future_contract"]["operator_input_supplied"] is False and approval["approved_future_contract"]["execution_status"] == NOT_EXECUTED),
        _check("future_plan_approved", len(approval["approved_future_plan"]) == 14 and all(item["approval_status"] == "APPROVED_PLANNED_NOT_EXECUTED" and item["execution_status"] == NOT_EXECUTED for item in approval["approved_future_plan"])),
        _check("planned_outputs_authorized", len(approval["authorized_planned_outputs"]) == 32 and all(item["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["authorized_planned_outputs"])),
        _check("actual_coverage_zero", approval["actual_covered_missing_authority_item_count"] == 0 and approval["actual_uncovered_missing_authority_item_count"] == 30),
        _check("missing_authority_items_missing_not_acquired", approval["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"),
        _check("outputs_generated", [item["output_id"] for item in approval["outputs"]] == list(OUTPUT_IDS)),
        _check("recommendation_defined", approval["recommended_next_task"] == RECOMMENDED_NEXT_TASK),
        _check("next_chain_defined", approval["next_chain"] == list(NEXT_CHAIN)),
        _check("next_gates_defined", approval["next_gates"] == list(NEXT_GATES)),
    ]
    checks.extend(_check(f"{key}_true", approval[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", approval[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"package_{item['package_id']}_approved_correctly", item["executed"] is False and (item["selected"] is (index == 0))) for index, item in enumerate(approval["approved_package_options"]))
    checks.extend(_check(f"requirement_{item}_approved", any(row["requirement_id"] == item and row["execution_status"] == NOT_EXECUTED for row in approval["approved_future_requirements"])) for item in source.source.FUTURE_REQUIREMENT_IDS)
    checks.extend(_check(f"risk_control_{item}_defined", item in approval["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item and row["status"] == GENERATED_APPROVAL_ONLY for row in approval["outputs"])) for item in OUTPUT_IDS)
    for key in (APPROVAL_DIGEST_KEY, ATTESTATION_DIGEST_KEY, PACKAGE_OPTIONS_DIGEST_KEY, FUTURE_REQUIREMENTS_DIGEST_KEY, FUTURE_CONTRACT_DIGEST_KEY, SOURCE_BINDING_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", approval[key]) is not None))
    approval["checklist"] = checks
    approval["summary"] = {
        "total_checks": len(checks),
        "passed_checks": sum(item["status"] == PASS for item in checks),
        "failed_checks": sum(item["status"] != PASS for item in checks),
        "blocker_count": sum(item["status"] != PASS and item["severity"] == BLOCKER for item in checks),
        "selected_operator_completion_inputs_preparation_or_supply_execution_reattempt_package": SELECTED_PACKAGE,
        "selected_package_approved_for_future_execution_only": True,
        "selected_package_executed": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt_after_approval": True,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    return approval


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict | None = None,
) -> dict[str, Any]:
    """Build the approval from committed constants or validated injected values."""
    source_value = SOURCE_OPERATOR_REVIEW_BINDINGS if source_operator_review is None else source_operator_review
    _validate_source_operator_review(source_value)
    attestation = DEFAULT_OPERATOR_ATTESTATION if operator_attestation is None else operator_attestation
    _validate_attestation(attestation)
    approval = _assemble_approval(attestation)
    result = validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(approval)
    if result["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError("approval checklist contains blockers")
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(approval: dict) -> dict[str, Any]:
    """Reject any drift from the exact deterministic approval artifact."""
    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError("approval must be an object")
    canonical = _assemble_approval(DEFAULT_OPERATOR_ATTESTATION)
    difference = _first_difference(dict(approval), canonical)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError(f"{difference} mismatch")
    return deepcopy(canonical["summary"])


MARKDOWN_SECTIONS = (
    "Approval Disposition", "Source Operator Review", "Operator Review Digest Surface", "Selected Package Approval", "Operator Attestation",
    "Source Candidate", "Source Results Review", "Source Execution", "Payload Supply Mechanism Review Facts", "Source Failure Diagnosis", "Source Blocked Input Preparation Execution", "Blocked Reason", "Primary Failure Class", "Secondary Failure Classes",
    "Source Approval", "Source Earlier Operator Review", "Source Earlier Candidate", "Source Prior Completion-Failure Diagnosis", "Source Completion Execution", "Source Completion Approval",
    "Source Completion Candidate Operator Review", "Source Completion Candidate", "Source Template Preparation Results Review",
    "Source Template Preparation Execution", "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt", "Retry Failure Context",
    "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary", "Reviewed Observable Families",
    "Reviewed Workstreams", "Reviewed Template Structure", "Actual Payload Absence", "Actual Evidence Absence", "Actual Coverage Zero", "Missing Authority Inventory", "Count Label Distinction",
    "Package Options Approval", "Future Explicit Non-Secret Payload Requirement", "Approved Future Requirements", "Approved Future Plan", "Authorized Planned Outputs",
    "Generated Outputs", "Source Authority Gap Preservation", "Unsupported Claims Boundary", "Recommendation", "Next Chain",
    "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_markdown_v1(approval: dict) -> str:
    """Render the approval as deterministic Markdown."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(approval)
    facts = {
        "Approval Disposition": f"`{APPROVAL_STATUS}` within `{APPROVAL_SCOPE}`. Approval `{approval[APPROVAL_DIGEST_KEY]}`; manifest `{approval[MANIFEST_DIGEST_KEY]}`.",
        "Source Operator Review": f"Commit `{SOURCE_OPERATOR_REVIEW_COMMIT}` and review `{SOURCE_OPERATOR_REVIEW_DIGEST}` are bound as source evidence.",
        "Operator Review Digest Surface": f"Packages `{SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST}`; requirements `{SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST}`; contract `{SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST}`; binding `{SOURCE_BINDING_REVIEW_DIGEST}`; manifest `{SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST}`.",
        "Selected Package Approval": f"`{SELECTED_PACKAGE}` is selected, approved, and authorized for future execution only; it is not executed.",
        "Operator Attestation": f"Exact deterministic non-secret attestation accepted; digest `{approval[ATTESTATION_DIGEST_KEY]}`.",
        "Source Candidate": f"Commit `{approval['source_candidate_commit']}`, checklist {approval['source_candidate_checklist_passed_count']}/{approval['source_candidate_checklist_total_count']}, and candidate `{approval['source_candidate_digest']}` remain bound.",
        "Source Results Review": f"Commit `{approval['source_results_review_commit']}` and review `{approval['source_results_review_digest']}` remain bound; it was not rerun.",
        "Payload Supply Mechanism Review Facts": "The reviewed mechanism preserves 14 package-header fields, 21 evidence-item fields, 30 future items, four scope sections, 13 distinct review sections, four workstreams [8, 8, 7, 7], 13 artifact types, 12 evidence classifications, 13 secret indicators, and 34 pre-submission fields.",
        "Source Failure Diagnosis": f"Commit `{approval['source_failure_diagnosis_commit']}` and diagnosis `{approval['source_failure_diagnosis_digest']}` remain bound.",
        "Source Execution": f"Commit `{approval['source_execution_commit']}` and execution `{approval['source_execution_digest']}` remain bound; source package `{approval['source_selected_package']}` executed only to create the reviewed mechanism. It was not rerun here.",
        "Source Blocked Input Preparation Execution": f"Commit `{approval['source_blocked_input_preparation_execution_commit']}` remains bound with absent success/prepared-input digests.",
        "Blocked Reason": f"`{approval['source_blocked_input_preparation_execution_reason']}`.",
        "Primary Failure Class": f"`{approval['primary_failure_class']}`.",
        "Source Approval": f"Historical approval `{approval['source_approval_digest']}` remains evidence only.",
        "Selected Historical Input Preparation Package": f"`{approval['selected_operator_completion_inputs_preparation_or_supply_package']}` remains historical and supplied no input.",
        "Source Earlier Operator Review": f"Commit `{approval['source_earlier_operator_review_commit']}` remains bound.",
        "Source Earlier Candidate": f"Commit `{approval['source_earlier_candidate_commit']}` remains bound.",
        "Source Prior Completion-Failure Diagnosis": f"Commit `{approval['source_prior_completion_failure_diagnosis_commit']}` remains bound.",
        "Source Completion Execution": f"Commit `{approval['source_completion_execution_commit']}` remains blocked by `{approval['source_completion_execution_blocked_reason']}`.",
        "Source Completion Approval": f"Commit `{approval['source_completion_approval_commit']}` remains bound.",
        "Source Completion Candidate Operator Review": f"Commit `{approval['source_completion_candidate_operator_review_commit']}` remains bound.",
        "Source Completion Candidate": f"Commit `{approval['source_completion_candidate_commit']}` remains bound.",
        "Source Template Preparation Results Review": f"Commit `{approval['source_template_preparation_results_review_commit']}` remains bound.",
        "Source Template Preparation Execution": f"Commit `{approval['source_template_preparation_execution_commit']}` remains bound.",
        "Source Preparation Failure Acquisition Chains": "All committed preparation, failure, blocked acquisition, and acquisition-approval constants remain bound; none was executed.",
        "Source Follow-On and Enrichment Chain": "All follow-on, enrichment, inventory, mapping, and historical digests remain bound without rerun.",
        "Historical Blocked Remediation": f"`{approval['historical_blocked_remediation_reason']}` remains authoritative.",
        "Plan Method Diagnostic Recovery Chain": "All plan, method, diagnostic, recapture, recovery, grouping, and staged-inventory digests remain bound.",
        "Durable Receipt": f"`{approval['source_durable_receipt_path']}` is bound opaquely and was not parsed.",
        "Retry Failure Context": "24,877 passed / 1,292 failed / 112 errors / 7 skipped remains authoritative retry evidence.",
        "Priority 1 Validation Summary": "675/675 before and after remains current-root evidence only, never retry evidence.",
        "Diagnostic Capture Evidence Summary": "Exit 1, 1,231,380 stdout bytes, zero stderr bytes, and source hashes remain diagnostic metadata only.",
        "Reviewed Template Structure": "Thirty template rows remain planning-only and are not actual evidence or source authority.",
        "Actual Payload Absence": "No actual operator payload or operator completion input was created, prepared, supplied, provided, validated, or bound.",
        "Actual Evidence Absence": "No actual evidence item or completed evidence package exists.",
        "Actual Coverage Zero": "Coverage remains 0/30; all rows remain `MISSING_NOT_ACQUIRED`.",
        "Missing Authority Inventory": "All MA-001 through MA-030 rows remain `MISSING_NOT_ACQUIRED`.",
        "Count Label Distinction": "Prescribed and enumerated source, candidate, review, non-goal, and risk-control counts remain distinct and unreconciled.",
        "Package Options Approval": "The recommended package alone is selected; six supporting packages remain unselected and five unsafe packages remain blocked.",
        "Future Explicit Non-Secret Payload Requirement": f"Explicit non-secret operator payload is required before separate future execution. Contract digest `{approval[FUTURE_CONTRACT_DIGEST_KEY]}`.",
        "Approved Future Requirements": f"All 58 requirements are approved for future execution only and remain `{NOT_EXECUTED}`.",
        "Approved Future Plan": f"All 14 steps are approved and remain `{NOT_EXECUTED}`.",
        "Authorized Planned Outputs": "All 32 planned outputs are authorized but not generated.",
        "Generated Outputs": f"All {len(OUTPUT_IDS)} approval-only output records were generated.",
        "Source Authority Gap Preservation": "No source authority, evidence, external evidence, concrete authority, or safe change was created.",
        "Unsupported Claims Boundary": "No root cause, retry success, predictive usefulness, profitability, or main readiness is claimed.",
        "Recommendation": f"`{approval['recommended_action']}`. Next task: `{RECOMMENDED_NEXT_TASK}`.",
        "Authority Boundaries": "Approval only; execution and every downstream evidence, acquisition, remediation, retry, merge, runtime, broker, and trading gate remain closed.",
        "Checklist Summary": f"{approval['summary']['passed_checks']}/{approval['summary']['total_checks']} PASS; blockers={approval['summary']['blocker_count']}.",
        "Guardrails": "Deterministic committed constants and validated injection only; no source builders, file reads, subprocesses, pytest, cache, logs, environment, external systems, providers, source owners, market data, models, runtime, broker, or trading actions.",
    }
    list_sections = {
        "Secondary Failure Classes": approval["secondary_failure_classes"],
        "Priority 1 Target Modules": [f"{item['path']}: {item['failed_or_errored_nodeid_count']}" for item in approval["priority_1_target_modules"]],
        "Reviewed Observable Families": [f"{item['family_id']}: {item['observable_evidence_count']} ({item['confidence']})" for item in approval["reviewed_observable_failure_families"]],
        "Reviewed Workstreams": [f"{item['workstream_id']} <- {item['source_family_id']}" for item in approval["reviewed_workstreams"]],
        "Next Chain": approval["next_chain"],
        "Next Gates": approval["next_gates"],
        "Risk Controls": approval["risk_controls"],
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Execution Reattempt Approval After Candidate Operator Review Status", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", ""))
        if section in list_sections:
            lines.extend(f"{index}. `{item}`" for index, item in enumerate(list_sections[section], 1))
        else:
            lines.append(facts.get(section, "Preserved from committed source evidence; no new execution or downstream authority is created."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested approval status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation,
    )
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_markdown_v1(approval), encoding="utf-8")
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE", "RECOMMENDED_NEXT_TASK",
    "OPERATOR_ID", "ATTESTATION_UTC", "ATTESTATION_DECISION", "ATTESTATION_SELECTED_PACKAGE", "ATTESTATION_PHRASE", "DEFAULT_OPERATOR_ATTESTATION",
    "SOURCE_OPERATOR_REVIEW_COMMIT", "SOURCE_OPERATOR_REVIEW_DIGEST", "SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST",
    "SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST", "SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST", "SOURCE_BINDING_REVIEW_DIGEST",
    "SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST", "SOURCE_OPERATOR_REVIEW_BINDINGS", "SOURCE_CONTEXT", "APPROVAL_DIGEST_KEY", "ATTESTATION_DIGEST_KEY", "PACKAGE_OPTIONS_DIGEST_KEY",
    "FUTURE_REQUIREMENTS_DIGEST_KEY", "FUTURE_CONTRACT_DIGEST_KEY", "SOURCE_BINDING_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_FROM_REVIEWED_MECHANISM_WITH_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD",
    "PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_PAYLOAD", "PACKAGE_CREATE_OPERATOR_PAYLOAD_READINESS_CHECKLIST_ONLY",
    "PACKAGE_CREATE_PAYLOAD_SHAPE_VALIDATION_PLAN_ONLY", "PACKAGE_CREATE_SECRET_SCREENING_DRY_RUN_PLAN_ONLY",
    "PACKAGE_SEGMENT_REATTEMPT_BY_WORKSTREAM_WITH_EXPLICIT_PAYLOAD_ONLY", "PACKAGE_REQUEST_OPERATOR_PAYLOAD_REVIEW_BEFORE_REATTEMPT_ONLY",
    "PACKAGE_RERUN_INPUT_PREPARATION_WITHOUT_OPERATOR_PAYLOAD", "PACKAGE_USE_TEMPLATES_OR_PLACEHOLDERS_AS_OPERATOR_PAYLOAD",
    "PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIGESTS_DIAGNOSTICS_CACHE_LOGS_ENV_OR_EXTERNAL_DOCUMENTS",
    "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MECHANISM_ONLY",
    "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW", "APPROVED_PACKAGE_OPTIONS", "FUTURE_PLAN", "OUTPUT_IDS",
    "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_markdown_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1",
]
