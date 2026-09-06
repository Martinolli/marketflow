"""Review the no-input re-entry candidate without selecting or executing it.

The artifact produced here is deterministic, offline, and governance-only. It
reviews committed candidate constants; it does not call source builders or read
operator inputs, evidence, files, caches, logs, environment, or providers.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1"
OPERATOR_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_READY"
OPERATOR_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_V1_IF_SELECTED"

SOURCE_CANDIDATE_COMMIT = "052b9f9002ba774361ebc099eea52be6cdbc7e62"
SOURCE_CANDIDATE_DIGEST = "f895767f7e54d97bbcf9ef7f44562f974505f6f32ebab2e66257e4d28c2dbd1a"
SOURCE_PACKAGE_OPTIONS_DIGEST = "82386fc8e116417e5fe9f394bfea12655e4e2c0185718dfab23cb893a04a144c"
SOURCE_FUTURE_REQUIREMENTS_DIGEST = "7760e95b3996820e5d39a4c12e800687fb25a21332eb8a4e30ec7899236caa31"
SOURCE_FUTURE_CONTRACT_DIGEST = "4d21b3a0b885efe2277e64190630a53cdab6622fb9013c6d0f13d48dd447a625"
SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST = "fc50eed1d4caa7053450a54d0b6e49c96bf4c2e1fdfaea0906137b69b314bd2c"
SOURCE_CANDIDATE_MANIFEST_DIGEST = "2b51213f447ca52cfe1cd74339a681fb1ffcc879208342fb1f96c158013af6aa"

OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_digest"
PACKAGE_OPTIONS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_package_options_review_digest"
FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_future_requirements_review_digest"
FUTURE_CONTRACT_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_future_contract_review_digest"
SOURCE_BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_source_binding_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_READY = OPERATOR_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = OPERATOR_REVIEW_SCOPE

# Re-export the reviewed decision surface under stable package constants.
PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY = source.PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY
PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD = source.PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD
PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY = source.PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY
PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY = source.PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY
PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY = source.PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY
PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY = source.PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY
PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY = source.PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY
PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS = source.PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS
PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV = source.PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV
PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD = source.PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS = source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS
PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS = source.PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_EXECUTED = "NOT_EXECUTED"
GENERATED_REVIEW_ONLY = "GENERATED_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_ONLY"


def _reviewed_packages() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(source.PACKAGE_OPTIONS):
        row = {key: deepcopy(value) for key, value in item.items() if key != "candidate_status"}
        if index == 0:
            row["review_status"] = "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
        elif index < 7:
            row["review_status"] = "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED"
        else:
            row["review_status"] = "REVIEWED_BLOCKED_NOT_ALLOWED"
        rows.append(row)
    return rows


REVIEWED_PACKAGE_OPTIONS = tuple(_reviewed_packages())

FUTURE_PLAN_REVIEW = (
    "Bind source no-input failure diagnosis.",
    "Bind source blocked execution, approvals, reviews, candidates, completion, templates, acquisition, enrichment, historical remediation, diagnostic recovery, module grouping, and staged inventory.",
    f"Preserve blocked reason {source.SOURCE_BLOCKED_REASON}.",
    "Preserve success, prepared-input, and success-manifest digests as null or absent.",
    "Preserve actual coverage as 0/30 and all missing-authority rows as MISSING_NOT_ACQUIRED.",
    "Review re-entry or payload-supply package options without selecting any.",
    "Review the payload-supply mechanism package as recommended for possible future approval.",
    "Review the future explicit non-secret operator payload contract.",
    "Review allowed values and secret-screening boundaries.",
    "Preserve direct-change, remediation, retry, acquisition, and main-merge flags as false.",
    "Require separate approval before execution.",
    "Require results review after any future payload-supply execution.",
    "Require separately approved completion reattempt after reviewed explicit non-secret payload exists.",
    "Preserve acquisition, disposition, remediation, retry, main, provider, runtime, broker, and trading gates.",
    "Preserve all source-digest and count-label distinctions without reconciliation.",
)

OUTPUT_IDS = tuple("""reentry_or_payload_supply_candidate_operator_review_manifest
source_candidate_binding_report
source_package_options_review_report
source_future_requirements_review_report
source_future_contract_review_report
source_binding_review_report
source_manifest_review_report
source_failure_diagnosis_binding_report
source_execution_binding_report
source_blocked_reason_report
source_success_digests_absence_report
source_approval_binding_report
source_operator_review_binding_report
source_prior_candidate_binding_report
source_prior_completion_failure_diagnosis_binding_report
source_completion_execution_binding_report
source_completion_approval_binding_report
source_completion_candidate_operator_review_binding_report
source_completion_candidate_binding_report
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
source_preparation_failure_acquisition_chain_binding_report
follow_on_enrichment_historical_binding_report
plan_method_diagnostic_recovery_binding_report
durable_receipt_opaque_reference_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
reentry_or_payload_supply_package_options_review_report
recommended_payload_supply_mechanism_review_report
future_payload_supply_contract_review_report
non_secret_and_allowed_values_review_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Approval After Candidate Operator Review v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Execution v1, if approved.",
    "Operator Completion Inputs Preparation or Supply Results Review v1, only if explicit non-secret inputs are prepared or supplied.",
    "Operator Source Authority Evidence Package Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional evidence-supported disposition candidate or hold only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""operator_completion_inputs_reentry_or_payload_supply_approval_if_selected
operator_completion_inputs_reentry_or_payload_supply_execution_if_approved
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

# Preserve every candidate control while changing only the actor label.
RISK_CONTROLS = tuple(
    item.replace("candidate_does_not_", "operator_review_does_not_", 1)
    for item in source.RISK_CONTROLS
)

TRUE_FIELDS = tuple("""operator_completion_inputs_reentry_or_payload_supply_candidate_operator_review_created
operator_completion_inputs_reentry_or_payload_supply_candidate_operator_review_ready
source_candidate_bound
source_candidate_reviewed
source_package_options_reviewed
source_future_requirements_reviewed
source_future_contract_reviewed
source_binding_reviewed
source_manifest_reviewed
source_failure_diagnosis_bound
source_failure_diagnosis_reviewed
source_execution_bound
source_execution_blocked_reason_verified
source_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
selected_historical_package_bound
approval_authorizes_future_execution_only_verified
operator_completion_inputs_absence_verified
execution_correctly_failed_closed
no_input_inference_verified
approval_not_input_verified
template_placeholder_boundary_preserved
diagnostic_output_boundary_preserved
synthetic_success_path_test_only_verified
source_operator_review_bound
source_prior_candidate_bound
source_prior_completion_failure_diagnosis_bound
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
reviewed_template_rows_bound
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
template_not_acquisition_success_verified
actual_coverage_zero_bound
evidence_package_absence_bound
missing_authority_inventory_bound
count_label_distinction_preserved
package_options_reviewed
recommended_package_reviewed
future_payload_supply_contract_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_reentry_or_payload_supply_approval_if_selected""".splitlines())

FALSE_FIELDS = tuple(item.replace("_in_candidate", "_in_operator_review") for item in source.FALSE_FIELDS if item != "ready_for_operator_completion_inputs_reentry_or_payload_supply_approval")

COUNTS = deepcopy(source.COUNTS)


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError(ValueError):
    """Raised when source bindings or operator-review boundaries drift."""


EXPECTED_SOURCE_CANDIDATE = {
    "artifact_kind": source.ARTIFACT_KIND,
    "candidate_status": source.CANDIDATE_STATUS,
    "candidate_scope": source.CANDIDATE_SCOPE,
    source.CANDIDATE_DIGEST_KEY: SOURCE_CANDIDATE_DIGEST,
    source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_DIGEST,
    source.FUTURE_REQUIREMENTS_DIGEST_KEY: SOURCE_FUTURE_REQUIREMENTS_DIGEST,
    source.FUTURE_CONTRACT_DIGEST_KEY: SOURCE_FUTURE_CONTRACT_DIGEST,
    source.SOURCE_BINDING_DIGEST_KEY: SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
    source.MANIFEST_DIGEST_KEY: SOURCE_CANDIDATE_MANIFEST_DIGEST,
}


def _validate_source_candidate(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError("source_candidate must be an object")
    for key, expected in EXPECTED_SOURCE_CANDIDATE.items():
        if value.get(key) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError(f"source_candidate.{key} mismatch")


def _first_difference(actual: Any, expected: Any, path: str = "operator_review") -> str | None:
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


def _digest_without(value: Mapping[str, Any], *keys: str) -> str:
    return semantic_digest({key: item for key, item in value.items() if key not in keys})


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {"check_id": check_id, "status": PASS if actual else BLOCKER, "expected": True, "actual": actual, "severity": BLOCKER, "message": "Boundary preserved." if actual else "Boundary drifted."}


def _source_projection() -> dict[str, Any]:
    context = deepcopy(source.SOURCE_CONTEXT)
    context.update({
        "source_prior_candidate_commit": context["source_candidate_commit"],
        "source_prior_candidate_artifact_kind": context["source_candidate_artifact_kind"],
        "source_prior_candidate_status": context["source_candidate_status"],
        "source_prior_candidate_scope": context["source_candidate_scope"],
        "source_prior_candidate_digest": context["source_candidate_digest"],
        "source_prior_candidate_package_options_digest": context["source_candidate_package_options_digest"],
        "source_prior_candidate_input_contract_digest": context["source_candidate_input_contract_digest"],
        "source_prior_candidate_source_binding_digest": context["source_candidate_source_binding_digest"],
        "source_prior_candidate_coverage_digest": context["source_candidate_coverage_digest"],
        "source_prior_candidate_manifest_digest": context["source_candidate_manifest_digest"],
        "source_prior_completion_failure_diagnosis_commit": context["source_prior_failure_diagnosis_commit"],
        "source_prior_completion_failure_diagnosis_digest": context["source_prior_failure_diagnosis_digest"],
        "source_prior_completion_failure_classification_digest": context["source_prior_failure_classification_digest"],
        "source_prior_operator_input_absence_diagnosis_digest": context["source_prior_input_absence_diagnosis_digest"],
        "source_prior_completion_failure_coverage_diagnosis_digest": context["source_prior_coverage_diagnosis_digest"],
        "source_prior_completion_failure_manifest_digest": context["source_prior_failure_diagnosis_manifest_digest"],
        "source_binding_review_digest_prior_operator_review": "4f4ed7e71d0b70fdeedbb3c39361cb8bcabb4eceab156dcf12ce406581c34d99",
        "source_completion_candidate_operator_input_requirements_review_digest_alias": "571582717ed926182363bed83f673c0312eeb28535151bf4a2e06a83b645faa5",
        "source_completion_candidate_template_binding_review_digest_alias": "e09fef3bc04abafafe1ce9fab37948be709b092d2a09c828a98c29c83bd66841",
        "source_candidate_commit": SOURCE_CANDIDATE_COMMIT,
        "source_candidate_artifact_kind": source.ARTIFACT_KIND,
        "source_candidate_status": source.CANDIDATE_STATUS,
        "source_candidate_scope": source.CANDIDATE_SCOPE,
        "source_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "source_package_options_digest": SOURCE_PACKAGE_OPTIONS_DIGEST,
        "source_future_requirements_digest": SOURCE_FUTURE_REQUIREMENTS_DIGEST,
        "source_future_contract_digest": SOURCE_FUTURE_CONTRACT_DIGEST,
        "source_candidate_source_binding_digest": SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
        "source_candidate_manifest_digest": SOURCE_CANDIDATE_MANIFEST_DIGEST,
    })
    return context


SOURCE_CONTEXT = _source_projection()


def _assemble_operator_review() -> dict[str, Any]:
    review = deepcopy(SOURCE_CONTEXT)
    contract = deepcopy(source.FUTURE_PAYLOAD_SUPPLY_CONTRACT)
    contract.update({"review_status": "REVIEWED_PLANNING_ONLY_NOT_SUPPLIED", "execution_status": NOT_EXECUTED})
    review.update({
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        "operator_review_philosophy": "The source candidate defines safe future governance choices after the no-input execution failure diagnosis. The review assesses the re-entry and payload-supply decision surface without selecting, approving, authorizing, executing, creating, inferring, preparing, supplying, validating, binding, completing, acquiring, remediating, retrying, merging, or authorizing runtime or trading.",
        "operator_review_boundary": "Operator review only. The missing-input condition, 0/30 coverage, all missing-authority rows, and all downstream gates remain preserved; no payload, input, evidence, source authority, remediation, retry readiness, or merge readiness is created.",
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(source.SECONDARY_FAILURE_CLASSES),
        "recommended_operator_completion_inputs_reentry_or_payload_supply_package": RECOMMENDED_PACKAGE,
        "review_recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommendation_reason": "The source candidate preserves the no-input diagnosis and offers a safe future governed supply mechanism. This review finds it suitable for possible future selection but does not select, approve, authorize, or execute it.",
        "reviewed_package_options": deepcopy(list(REVIEWED_PACKAGE_OPTIONS)),
        "reviewed_future_requirements": [{"requirement_id": item, "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_REENTRY_OR_PAYLOAD_SUPPLY_GOVERNANCE", "execution_status": NOT_EXECUTED} for item in source.FUTURE_REQUIREMENT_IDS],
        "reviewed_future_payload_supply_contract": contract,
        "reviewed_future_plan": [{"step": index, "description": item, "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": NOT_EXECUTED} for index, item in enumerate(FUTURE_PLAN_REVIEW, 1)],
        "reviewed_planned_outputs": [{"output_id": item, "review_status": "REVIEWED_PLANNED_NOT_GENERATED"} for item in source.PLANNED_OUTPUT_IDS],
        "reviewed_non_goals": [{"non_goal_id": item, "active": True, "review_status": "REVIEWED_ACTIVE"} for item in source.NON_GOALS],
        "outputs": [{"output_id": item, "status": GENERATED_REVIEW_ONLY} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_SEPARATE_APPROVAL_REQUIRED_BEFORE_ANY_PAYLOAD_SUPPLY_MECHANISM_EXECUTION",
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
    review.update({key: True for key in TRUE_FIELDS})
    review.update({key: False for key in FALSE_FIELDS})
    review.update(COUNTS)

    review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY] = semantic_digest(review["reviewed_package_options"])
    review[FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY] = semantic_digest(review["reviewed_future_requirements"])
    review[FUTURE_CONTRACT_REVIEW_DIGEST_KEY] = semantic_digest(review["reviewed_future_payload_supply_contract"])
    review[SOURCE_BINDING_REVIEW_DIGEST_KEY] = semantic_digest({key: value for key, value in review.items() if key.startswith("source_") or key.startswith("retry_") or key.startswith("priority1_")})
    digest_keys = (OPERATOR_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY, "checklist", "summary")
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest_without(review, *digest_keys)
    review[MANIFEST_DIGEST_KEY] = semantic_digest({
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        "package_options_review_digest": review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY],
        "future_requirements_review_digest": review[FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY],
        "future_contract_review_digest": review[FUTURE_CONTRACT_REVIEW_DIGEST_KEY],
        "source_binding_review_digest": review[SOURCE_BINDING_REVIEW_DIGEST_KEY],
        "output_ids": list(OUTPUT_IDS),
    })

    checks = [
        _check("artifact_kind_correct", review["artifact_kind"] == ARTIFACT_KIND),
        _check("operator_review_status_correct", review["operator_review_status"] == OPERATOR_REVIEW_STATUS),
        _check("operator_review_scope_correct", review["operator_review_scope"] == OPERATOR_REVIEW_SCOPE),
        _check("source_candidate_commit_bound", review["source_candidate_commit"] == SOURCE_CANDIDATE_COMMIT),
        _check("source_candidate_digest_bound", review["source_candidate_digest"] == SOURCE_CANDIDATE_DIGEST),
        _check("source_candidate_digest_surface_bound", all(review[key] == expected for key, expected in {
            "source_package_options_digest": SOURCE_PACKAGE_OPTIONS_DIGEST,
            "source_future_requirements_digest": SOURCE_FUTURE_REQUIREMENTS_DIGEST,
            "source_future_contract_digest": SOURCE_FUTURE_CONTRACT_DIGEST,
            "source_candidate_source_binding_digest": SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST,
            "source_candidate_manifest_digest": SOURCE_CANDIDATE_MANIFEST_DIGEST,
        }.items())),
        _check("source_blocked_reason_bound", review["source_blocked_reason"] == source.SOURCE_BLOCKED_REASON),
        _check("source_success_digests_absent", review["source_success_digests_absent"] and review["source_success_execution_digest"] is None and review["source_prepared_operator_completion_inputs_digest"] is None and review["source_prepared_operator_completion_inputs_manifest_digest"] is None),
        _check("primary_failure_class_bound", review["primary_failure_class"] == source.PRIMARY_FAILURE_CLASS),
        _check("secondary_failure_classes_bound", tuple(review["secondary_failure_classes"]) == source.SECONDARY_FAILURE_CLASSES),
        _check("package_option_count_12", len(review["reviewed_package_options"]) == 12),
        _check("available_package_count_7", sum(item["review_status"] != "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review["reviewed_package_options"]) == 7),
        _check("blocked_package_count_5", sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in review["reviewed_package_options"]) == 5),
        _check("recommended_package_reviewed", review["recommended_operator_completion_inputs_reentry_or_payload_supply_package"] == RECOMMENDED_PACKAGE),
        _check("future_requirements_reviewed", len(review["reviewed_future_requirements"]) == 62 and all(item["execution_status"] == NOT_EXECUTED for item in review["reviewed_future_requirements"])),
        _check("future_contract_reviewed", review["reviewed_future_payload_supply_contract"]["review_status"] == "REVIEWED_PLANNING_ONLY_NOT_SUPPLIED" and review["reviewed_future_payload_supply_contract"]["operator_input_supplied"] is False),
        _check("future_plan_reviewed", len(review["reviewed_future_plan"]) == 15 and all(item["execution_status"] == NOT_EXECUTED for item in review["reviewed_future_plan"])),
        _check("planned_outputs_reviewed", len(review["reviewed_planned_outputs"]) == 34),
        _check("non_goals_reviewed", all(item["active"] for item in review["reviewed_non_goals"])),
        _check("actual_coverage_zero", review["actual_covered_missing_authority_item_count"] == 0 and review["actual_uncovered_missing_authority_item_count"] == 30),
        _check("missing_authority_items_missing_not_acquired", review["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"),
        _check("outputs_generated", [item["output_id"] for item in review["outputs"]] == list(OUTPUT_IDS)),
        _check("recommendation_defined", review["recommended_next_task"] == RECOMMENDED_NEXT_TASK),
        _check("next_chain_defined", review["next_chain"] == list(NEXT_CHAIN)),
        _check("next_gates_defined", review["next_gates"] == list(NEXT_GATES)),
    ]
    checks.extend(_check(f"{key}_true", review[key] is True) for key in TRUE_FIELDS)
    checks.extend(_check(f"{key}_false", review[key] is False) for key in FALSE_FIELDS)
    checks.extend(_check(f"package_{item['package_id']}_reviewed", item["review_status"].startswith("REVIEWED_") and not any(item[key] for key in ("selected", "approved", "authorized", "executed"))) for item in review["reviewed_package_options"])
    checks.extend(_check(f"requirement_{item}_reviewed", any(row["requirement_id"] == item and row["execution_status"] == NOT_EXECUTED for row in review["reviewed_future_requirements"])) for item in source.FUTURE_REQUIREMENT_IDS)
    checks.extend(_check(f"non_goal_{item}_reviewed", any(row["non_goal_id"] == item and row["active"] for row in review["reviewed_non_goals"])) for item in source.NON_GOALS)
    checks.extend(_check(f"risk_control_{item}_defined", item in review["risk_controls"]) for item in RISK_CONTROLS)
    checks.extend(_check(f"output_{item}_generated", any(row["output_id"] == item and row["status"] == GENERATED_REVIEW_ONLY for row in review["outputs"])) for item in OUTPUT_IDS)
    for key in (OPERATOR_REVIEW_DIGEST_KEY, PACKAGE_OPTIONS_REVIEW_DIGEST_KEY, FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY, FUTURE_CONTRACT_REVIEW_DIGEST_KEY, SOURCE_BINDING_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY):
        checks.append(_check(f"{key}_generated", re.fullmatch(r"[0-9a-f]{64}", review[key]) is not None))
    review["checklist"] = checks
    review["summary"] = {
        "total_checks": len(checks),
        "passed_checks": sum(item["status"] == PASS for item in checks),
        "failed_checks": sum(item["status"] != PASS for item in checks),
        "blocker_count": sum(item["status"] != PASS and item["severity"] == BLOCKER for item in checks),
        "operator_completion_inputs_reentry_or_payload_supply_candidate_operator_review_created": True,
        "operator_completion_inputs_reentry_or_payload_supply_candidate_operator_review_ready": True,
        "source_candidate_digest": SOURCE_CANDIDATE_DIGEST,
        "source_failure_diagnosis_digest": source.SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_blocked_reason": source.SOURCE_BLOCKED_REASON,
        "source_blocked_digest": source.SOURCE_BLOCKED_DIGEST,
        "source_input_absence_digest": source.SOURCE_INPUT_ABSENCE_DIGEST,
        "source_success_digests_absent": True,
        "primary_failure_class": source.PRIMARY_FAILURE_CLASS,
        "recommended_operator_completion_inputs_reentry_or_payload_supply_package": RECOMMENDED_PACKAGE,
        "package_selected": False, "package_approved": False, "package_authorized": False, "package_executed": False,
        "operator_payload_created": False, "operator_completion_inputs_prepared": False, "operator_completion_inputs_supplied": False,
        "operator_completion_inputs_provided": False, "operator_completion_inputs_validated_as_evidence": False,
        "operator_completion_inputs_bound_as_evidence": False, "prepared_operator_completion_inputs_for_results_review": False,
        "operator_source_authority_evidence_package_completed": False, "operator_source_authority_evidence_package_created": False,
        "source_authority_acquisition_performed": False, "source_authority_evidence_acquired": False, "external_evidence_acquired": False,
        "concrete_source_authority_established": False, "safe_source_authority_bound_change_identified": False,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_completion_inputs_reentry_or_payload_supply_approval_if_selected": True,
        "ready_for_operator_completion_inputs_reentry_or_payload_supply_execution": False,
        "ready_for_operator_completion_inputs_preparation_or_supply_execution_reattempt": False,
        "ready_for_retry_candidate": False, "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "priority_1_total_nodeids": 612, "failed_or_errored_nodeids_count": 1404,
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "package_option_count": 12, "available_package_count": 7, "blocked_package_count": 5,
        "future_requirement_count": 62, "future_plan_step_count": 15, "planned_output_count": 34,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False,
    }
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(*, source_candidate: dict | None = None) -> dict[str, Any]:
    """Build an operator review from committed constants or validated injection."""
    if source_candidate is not None:
        _validate_source_candidate(deepcopy(source_candidate))
    review = _assemble_operator_review()
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(operator_review: dict) -> dict[str, Any]:
    """Reject source drift, selection, execution, or authority expansion."""
    if not isinstance(operator_review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError("operator_review must be an object")
    expected = _assemble_operator_review()
    difference = _first_difference(operator_review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError(f"{difference} mismatch")
    if operator_review["summary"]["failed_checks"] or operator_review["summary"]["blocker_count"]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError("operator-review checklist failed")
    return {
        "artifact_kind": ARTIFACT_KIND,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "operator_review_digest": operator_review[OPERATOR_REVIEW_DIGEST_KEY],
        **{key: operator_review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Operator Review Disposition
Source Candidate
Candidate Digest Surface
Source Failure Diagnosis
Source Execution
Blocked Reason
Primary Failure Class
Secondary Failure Classes
Source Approval
Selected Historical Input Preparation Package
Source Operator Review
Source Prior Candidate
Source Prior Completion-Failure Diagnosis
Source Completion Execution
Source Completion Approval
Source Completion Candidate Operator Review
Source Completion Candidate
Source Template Preparation Results Review
Source Template Preparation Execution
Source Preparation Failure Acquisition Chains
Source Follow-On and Enrichment Chain
Historical Blocked Remediation
Plan Method Diagnostic Recovery Chain
Durable Receipt
Retry Failure Context
Priority 1 Target Modules
Priority 1 Validation Summary
Diagnostic Capture Evidence Summary
Reviewed Observable Families
Reviewed Workstreams
Reviewed Template Structure
Actual Evidence Absence
Actual Coverage Zero
Count Label Distinction
Operator Input Absence
Future Payload Supply Contract Review
Reviewed Package Options
Reviewed Recommended Package
Reviewed Future Requirements
Reviewed Future Plan
Reviewed Planned Outputs
Reviewed Non-Goals
Source Authority Gap Preservation
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_markdown_v1(operator_review: dict) -> str:
    """Render the review without introducing operator values or authority."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(operator_review)
    facts = {
        "Operator Review Disposition": f"`{OPERATOR_REVIEW_STATUS}` within `{OPERATOR_REVIEW_SCOPE}`. Review `{operator_review[OPERATOR_REVIEW_DIGEST_KEY]}`; manifest `{operator_review[MANIFEST_DIGEST_KEY]}`.",
        "Source Candidate": f"Commit `{SOURCE_CANDIDATE_COMMIT}`; artifact `{source.ARTIFACT_KIND}`; status `{source.CANDIDATE_STATUS}`; scope `{source.CANDIDATE_SCOPE}`.",
        "Candidate Digest Surface": f"Candidate `{SOURCE_CANDIDATE_DIGEST}`; packages `{SOURCE_PACKAGE_OPTIONS_DIGEST}`; requirements `{SOURCE_FUTURE_REQUIREMENTS_DIGEST}`; contract `{SOURCE_FUTURE_CONTRACT_DIGEST}`; binding `{SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST}`; manifest `{SOURCE_CANDIDATE_MANIFEST_DIGEST}`.",
        "Source Failure Diagnosis": f"Commit `{operator_review['source_failure_diagnosis_commit']}`; digest `{operator_review['source_failure_diagnosis_digest']}`; manifest `{operator_review['source_failure_diagnosis_manifest_digest']}`.",
        "Source Execution": f"Commit `{operator_review['source_execution_commit']}`; artifact `{operator_review['source_execution_artifact_kind']}`; status `{operator_review['source_execution_status']}`; scope `{operator_review['source_execution_scope']}`.",
        "Blocked Reason": f"`{operator_review['source_blocked_reason']}`; blocked `{operator_review['source_blocked_digest']}`; input absence `{operator_review['source_input_absence_digest']}`; manifest `{operator_review['source_blocked_manifest_digest']}`.",
        "Primary Failure Class": f"`{operator_review['primary_failure_class']}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in operator_review["secondary_failure_classes"]),
        "Source Approval": f"Commit `{operator_review['source_approval_commit']}`; approval `{operator_review['source_approval_digest']}`; attestation `{operator_review['source_attestation_digest']}`.",
        "Selected Historical Input Preparation Package": f"`{operator_review['selected_operator_completion_inputs_preparation_or_supply_package']}` supplied no operator input.",
        "Source Operator Review": f"Commit `{operator_review['source_operator_review_commit']}`; digest `{operator_review['source_operator_review_digest']}`; manifest `{operator_review['source_operator_review_manifest_digest']}`.",
        "Source Prior Candidate": f"Commit `{operator_review['source_prior_candidate_commit']}`; digest `{operator_review['source_prior_candidate_digest']}`; manifest `{operator_review['source_prior_candidate_manifest_digest']}`.",
        "Source Prior Completion-Failure Diagnosis": f"Commit `{operator_review['source_prior_completion_failure_diagnosis_commit']}`; digest `{operator_review['source_prior_completion_failure_diagnosis_digest']}`; manifest `{operator_review['source_prior_completion_failure_manifest_digest']}`.",
        "Source Completion Execution": f"Commit `{operator_review['source_completion_execution_commit']}`; reason `{operator_review['source_completion_execution_blocked_reason']}`; blocked `{operator_review['source_completion_execution_blocked_digest']}`; manifest `{operator_review['source_completion_execution_blocked_manifest_digest']}`.",
        "Source Completion Approval": f"Commit `{operator_review['source_completion_approval_commit']}`; digest `{operator_review['source_completion_approval_digest']}`; attestation `{operator_review['source_completion_approval_attestation_digest']}`.",
        "Source Completion Candidate Operator Review": f"Commit `{operator_review['source_completion_candidate_operator_review_commit']}`; digest `{operator_review['source_completion_candidate_operator_review_digest']}`.",
        "Source Completion Candidate": f"Commit `{operator_review['source_completion_candidate_commit']}`; digest `{operator_review['source_completion_candidate_digest']}`; manifest `{operator_review['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"Commit `{operator_review['source_template_preparation_results_review_commit']}`; digest `{operator_review['source_template_preparation_results_review_digest']}`; manifest `{operator_review['source_template_preparation_results_review_manifest_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{operator_review['source_template_preparation_execution_commit']}`; digest `{operator_review['source_template_preparation_execution_digest']}`; manifest `{operator_review['source_template_preparation_execution_manifest_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{operator_review['source_preparation_candidate_digest']}`; blocked acquisition `{operator_review['source_blocked_acquisition_execution_reason']}`; approval `{operator_review['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Follow-on `{operator_review['source_follow_on_execution_digest']}`; enrichment `{operator_review['source_enrichment_execution_digest']}`; historical review `{operator_review['source_results_review_digest_historical']}`.",
        "Historical Blocked Remediation": f"`{operator_review['historical_blocked_remediation_reason']}`; manifest `{operator_review['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Plan `{operator_review['source_targeted_remediation_plan_digest']}`; method `{operator_review['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{operator_review['source_recovery_results_review_digest']}`; staged inventory `{operator_review['source_staged_inventory_digest']}`.",
        "Durable Receipt": f"`{operator_review['source_durable_receipt_path']}` remains opaque and unparsed.",
        "Retry Failure Context": "The authoritative retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped.",
        "Priority 1 Target Modules": "Five modules total 612 node IDs; top ten total 1,069; 29 modules cover 1,404 failed-or-errored node IDs.",
        "Priority 1 Validation Summary": "675/675 before and after remains non-retry current-root evidence and was not rerun.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout 1,231,380 bytes `{operator_review['source_stdout_sha256']}`; stderr 0 bytes `{operator_review['source_stderr_sha256']}`; metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence families, 47 observations each and 188 total, remain planning evidence.",
        "Reviewed Workstreams": "Four reviewed workstreams remain non-authorizing.",
        "Reviewed Template Structure": "Thirty template rows map MA-001 through MA-030; the template remains non-evidence and non-authority.",
        "Actual Evidence Absence": "No actual evidence item or completed evidence package exists.",
        "Actual Coverage Zero": "Coverage remains 0/30 and every row remains `MISSING_NOT_ACQUIRED`.",
        "Count Label Distinction": "Preserved without reconciliation: 67/69/69, 71/76, 104/106, source-local 62/17/34/76/105, candidate-local 62/15/34/78/112.",
        "Operator Input Absence": "No payload or operator completion input was created, prepared, supplied, validated, secret-screened, or bound.",
        "Future Payload Supply Contract Review": f"Planning-only 30-item contract reviewed, not supplied or executed; digest `{operator_review[FUTURE_CONTRACT_REVIEW_DIGEST_KEY]}`.",
        "Reviewed Recommended Package": f"`{RECOMMENDED_PACKAGE}` is reviewable for possible future approval but remains unselected.",
        "Source Authority Gap Preservation": "No evidence, authority, acquisition, safe change, disposition, remediation, retry, or merge readiness was created.",
        "Unsupported Claims Boundary": "No root-cause, retry-success, predictive, profitability, runtime, broker, trading, or main-readiness claim is made.",
        "Recommendation": f"`{RECOMMENDED_NEXT_TASK}` remains future and optional. `{operator_review['recommended_action']}`.",
        "Authority Boundaries": "Only optional separate approval if selected is ready; all execution and downstream authority remains closed.",
        "Checklist Summary": f"{operator_review['summary']['passed_checks']}/{operator_review['summary']['total_checks']} PASS; blockers={operator_review['summary']['blocker_count']}.",
        "Guardrails": "Offline deterministic dictionaries only; no source builders, files, subprocesses, pytest, cache, receipt, logs, environment, external documents, source owners, providers, data, models, runtime, broker, or trading systems are accessed.",
    }
    list_sections = {
        "Reviewed Package Options": (operator_review["reviewed_package_options"], lambda item, _: f"- `{item['package_id']}` — `{item['review_status']}`"),
        "Reviewed Future Requirements": (operator_review["reviewed_future_requirements"], lambda item, _: f"- `{item['requirement_id']}` — `{item['review_status']}` / `{item['execution_status']}`"),
        "Reviewed Future Plan": (operator_review["reviewed_future_plan"], lambda item, _: f"{item['step']}. {item['description']} — `{item['review_status']}`"),
        "Reviewed Planned Outputs": (operator_review["reviewed_planned_outputs"], lambda item, _: f"- `{item['output_id']}` — `{item['review_status']}`"),
        "Reviewed Non-Goals": (operator_review["reviewed_non_goals"], lambda item, _: f"- `{item['non_goal_id']}`"),
        "Next Chain": (operator_review["next_chain"], lambda item, index: f"{index}. {item}"),
        "Next Gates": (operator_review["next_gates"], lambda item, _: f"- `{item}`"),
        "Risk Controls": (operator_review["risk_controls"], lambda item, _: f"- `{item}`"),
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs Preparation or Supply Reentry or Payload Supply Candidate Operator Review After No-Input Execution Failure Diagnosis v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", ""))
        if section in list_sections:
            values, formatter = list_sections[section]
            lines.extend(formatter(item, index) for index, item in enumerate(values, 1))
        else:
            lines.append(facts.get(section, "Preserved from committed source evidence; no new authority is created."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(output_dir: str | Path, *, source_candidate: dict | None = None) -> dict[str, Any]:
    """Write only the requested operator-review status Markdown artifact."""
    destination_root = Path(output_dir)
    if {part.lower() for part in destination_root.parts}.intersection({".marketflow", ".pytest_cache", ".env"}):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(source_candidate=source_candidate)
    destination = destination_root / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "OPERATOR_REVIEW_STATUS", "OPERATOR_REVIEW_SCOPE", "RECOMMENDED_PACKAGE", "RECOMMENDED_NEXT_TASK",
    "SOURCE_CANDIDATE_COMMIT", "SOURCE_CANDIDATE_DIGEST", "SOURCE_PACKAGE_OPTIONS_DIGEST", "SOURCE_FUTURE_REQUIREMENTS_DIGEST",
    "SOURCE_FUTURE_CONTRACT_DIGEST", "SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST", "SOURCE_CANDIDATE_MANIFEST_DIGEST",
    "OPERATOR_REVIEW_DIGEST_KEY", "PACKAGE_OPTIONS_REVIEW_DIGEST_KEY", "FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY",
    "FUTURE_CONTRACT_REVIEW_DIGEST_KEY", "SOURCE_BINDING_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_OPERATOR_PAYLOAD_CREATION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_COMPLETION_REATTEMPT_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_ALTERNATE_DIAGNOSTIC_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY",
    "PACKAGE_HOLD_PENDING_EXPLICIT_NON_SECRET_OPERATOR_COMPLETION_INPUT_PAYLOAD", "PACKAGE_REENTER_INPUT_PREPARATION_OR_SUPPLY_WITH_EXPLICIT_OPERATOR_PAYLOAD_ONLY",
    "PACKAGE_CREATE_OPERATOR_PAYLOAD_FIELD_CHECKLIST_ONLY", "PACKAGE_CREATE_WORKSTREAM_SEGMENTED_PAYLOAD_SUPPLY_PLAN_ONLY",
    "PACKAGE_CREATE_ALLOWED_VALUES_AND_SECRET_SCREENING_GUIDANCE_ONLY", "PACKAGE_CREATE_OPERATOR_ATTESTATION_FRAMEWORK_FOR_FUTURE_PAYLOAD_SUPPLY_ONLY",
    "PACKAGE_FABRICATE_OPERATOR_PAYLOAD_FROM_TEMPLATE_OR_PLACEHOLDERS", "PACKAGE_DERIVE_OPERATOR_PAYLOAD_FROM_DIAGNOSTIC_OUTPUT_DIGESTS_CACHE_LOGS_OR_ENV",
    "PACKAGE_RERUN_INPUT_PREPARATION_OR_SUPPLY_EXECUTION_WITHOUT_OPERATOR_PAYLOAD", "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_OR_ACQUIRE_SOURCE_AUTHORITY_FROM_MISSING_INPUTS_DIAGNOSIS",
    "PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_NO_INPUT_FAILURE_DIAGNOSIS", "REVIEWED_PACKAGE_OPTIONS", "FUTURE_PLAN_REVIEW",
    "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS", "EXPECTED_SOURCE_CANDIDATE", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_markdown_v1",
]
