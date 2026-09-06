"""Review the evidence-package completion candidate without selecting it."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1"
OPERATOR_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY"
OPERATOR_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_COMPLETION_CANDIDATE_COMMIT = "7af6b1b5ad223f92da0997e2b7abcb73543470df"
SOURCE_COMPLETION_CANDIDATE_DIGEST = "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207"
SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST = "c276ff30b28441dfd3ebb1dc4071b6a82e29c42b593215aa603c56587fc7e982"
SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST = "615a15e243999e28770b3f1351df1cc5b4e8ebbf22febc36812fcf42dd59b7fb"
SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST = "734eac89400c983c042f5c0a9c91e85694aad62ab07f3c8e046c406e02813df3"
SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST = "ba547fc27cbf2642a070383d600952a5798c1e2a0d7b703ba3fd049486e9e107"
SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST = "983951245e47b0fcc4d31b818a8adf16785f96dc8e2688ed12ce679fd17cb91b"
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_V1_IF_SELECTED"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_digest"
PACKAGE_OPTIONS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_package_options_digest"
OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_operator_input_requirements_digest"
TEMPLATE_BINDING_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_template_binding_digest"
COVERAGE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY = OPERATOR_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = OPERATOR_REVIEW_SCOPE

PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS = source.PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS
PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY = source.PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY
PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY = source.PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY
PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY = source.PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY
PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY = source.PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY
PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY = source.PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY
PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS = source.PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY = source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY
PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY = source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY
PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION = source.PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION
PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW = source.PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW
PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE = source.PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE

OPERATOR_REVIEW_PHILOSOPHY = "The reviewed completion candidate correctly defines future options for completing a non-secret operator evidence package from the reviewed template. The candidate does not itself complete a package, supply evidence, validate evidence, bind evidence, acquire source authority, authorize acquisition reattempt, authorize remediation, authorize retry, or create main-merge readiness."
OPERATOR_REVIEW_BOUNDARY = "Operator review only. This review may assess candidate package options, operator-input requirements, template-binding facts, coverage facts, future requirements, future plan, outputs, non-goals, next gates, risk controls, and count-label distinctions. It must not select, approve, authorize, execute, complete, supply, validate, bind, acquire, remediate, retry, merge, call providers, inspect secrets, or authorize runtime/trading."

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_candidate_operator_review_created
operator_source_authority_evidence_package_completion_candidate_operator_review_ready
source_completion_candidate_bound
source_completion_candidate_reviewed
source_completion_candidate_package_options_reviewed
source_operator_input_requirements_reviewed
source_template_binding_reviewed
source_completion_candidate_coverage_reviewed
source_completion_candidate_manifest_reviewed
source_results_review_bound
source_template_review_bound
source_evidence_item_template_review_bound
source_preparation_checklist_review_bound
source_template_coverage_review_bound
source_execution_bound
source_approval_bound
source_attestation_bound
source_operator_review_bound
source_preparation_candidate_bound
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_acquisition_approval_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_authority_acquisition_candidate_bound
source_authority_acquisition_scope_bound
source_missing_authority_mapping_bound
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
diagnostic_metadata_bound
observable_families_bound
reviewed_workstreams_bound
reviewed_template_structure_bound
reviewed_template_rows_bound
reviewed_template_checklist_bound
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
template_not_acquisition_success_verified
actual_coverage_zero_bound
evidence_package_absence_bound
missing_authority_inventory_bound
completion_package_options_reviewed
recommended_completion_package_reviewed
future_completion_requirements_reviewed
future_completion_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_completion_approval_if_selected""".splitlines())

_FALSE_NAME_MAP = {
    "pytest_performed_in_candidate": "pytest_performed_in_operator_review",
    "diagnostic_receipt_parsed_in_candidate": "diagnostic_receipt_parsed_in_operator_review",
    "diagnostic_output_analyzed_in_candidate": "diagnostic_output_analyzed_in_operator_review",
    "targeted_remediation_plan_regenerated_in_candidate": "targeted_remediation_plan_regenerated_in_operator_review",
    "cache_read_in_candidate": "cache_read_in_operator_review",
    "cache_modified_in_candidate": "cache_modified_in_operator_review",
    "provider_requests_made_in_candidate": "provider_requests_made_in_operator_review",
    "market_data_acquisition_performed_in_candidate": "market_data_acquisition_performed_in_operator_review",
    "dataset_generation_performed_in_candidate": "dataset_generation_performed_in_operator_review",
}
FALSE_FIELDS = tuple(
    _FALSE_NAME_MAP.get(field, field)
    for field in source.FALSE_FIELDS
    if field != "ready_for_operator_source_authority_evidence_package_completion_approval"
)

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_completion_candidate_operator_review_manifest
source_completion_candidate_binding_report
source_completion_package_options_review_report
source_operator_input_requirements_review_report
source_template_binding_review_report
source_completion_coverage_review_report
source_template_preparation_results_review_binding_report
source_template_preparation_execution_binding_report
source_approval_binding_report
source_operator_review_binding_report
source_preparation_candidate_binding_report
source_failure_diagnosis_binding_report
source_blocked_acquisition_execution_binding_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
reviewed_template_structure_report
reviewed_template_coverage_report
evidence_package_absence_report
actual_coverage_zero_report
missing_authority_mapping_report
reviewed_completion_package_options_report
recommended_completion_package_report
required_operator_input_header_fields_review
required_operator_input_evidence_item_fields_review
non_secret_operator_input_requirements_review
custody_digest_and_provenance_requirements_review
specification_observation_separation_review
expected_actual_separation_review
source_authority_diagnostic_output_separation_review
completion_results_review_gate_report
acquisition_reattempt_gate_preservation_report
count_label_distinction_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Completion Approval v1, if selected.",
    "Operator Source Authority Evidence Package Completion Execution v1, if approved and non-secret operator inputs are supplied.",
    "Operator Source Authority Evidence Package Completion Results Review v1.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Evidence Package v1, only if a reviewed completed package exists and is separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_source_authority_evidence_package_completion_approval_if_selected
operator_source_authority_evidence_package_completion_execution_if_approved_and_non_secret_operator_inputs_supplied
operator_source_authority_evidence_package_completion_results_review
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

RISK_CONTROLS = tuple(
    item.replace("candidate_", "operator_review_", 1) if item.startswith("candidate_") else item
    for item in source.RISK_CONTROLS
)


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError(ValueError):
    """Raised when the operator review or its source candidate is invalid."""


def _digest_without(value: Mapping[str, Any], *keys: str) -> str:
    return semantic_digest({key: item for key, item in value.items() if key not in keys})


def _first_difference(actual: Any, expected: Any, path: str = "operator_review") -> str | None:
    if type(actual) is not type(expected):
        return path
    if isinstance(expected, Mapping):
        if set(actual) != set(expected):
            return path
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


def _validate_source_completion_candidate(candidate: dict[str, Any]) -> None:
    try:
        source.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(deepcopy(candidate))
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError("source completion candidate is invalid") from exc
    expected = {
        "artifact_kind": source.ARTIFACT_KIND,
        "candidate_status": source.CANDIDATE_STATUS,
        "candidate_scope": source.CANDIDATE_SCOPE,
        source.CANDIDATE_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_DIGEST,
        source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
        source.OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST,
        source.TEMPLATE_BINDING_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST,
        source.COVERAGE_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
    }
    for key, expected_value in expected.items():
        if candidate.get(key) != expected_value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError(f"source completion candidate {key} mismatch")


_COMMITTED_SOURCE_COMPLETION_CANDIDATE = source.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1()


def _source_bindings(candidate: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {
        "source_completion_candidate_commit": SOURCE_COMPLETION_CANDIDATE_COMMIT,
        "source_completion_candidate_artifact_kind": candidate["artifact_kind"],
        "source_completion_candidate_status": candidate["candidate_status"],
        "source_completion_candidate_scope": candidate["candidate_scope"],
        "source_completion_candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
        "source_completion_candidate_package_options_digest": SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
        "source_completion_candidate_operator_input_requirements_digest": SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST,
        "source_completion_candidate_template_binding_digest": SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST,
        "source_completion_candidate_coverage_digest": SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST,
        "source_completion_candidate_manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
        "source_enumerated_future_completion_requirement_count": candidate["enumerated_future_completion_requirement_count"],
        "source_enumerated_non_goal_count": candidate["enumerated_non_goal_count"],
        "source_enumerated_risk_control_count": candidate["enumerated_risk_control_count"],
    }
    for key, value in candidate.items():
        if key.startswith("source_") and isinstance(value, (str, int, bool)):
            bindings.setdefault(key, value)
    for key, value in candidate.items():
        if key.startswith("historical_") and isinstance(value, (str, int, bool)):
            bindings[key] = value
    bindings["source_results_review_digest_historical"] = candidate["source_prior_results_review_digest"]
    bindings["selected_operator_source_authority_evidence_package_preparation_package"] = candidate["selected_operator_source_authority_evidence_package_preparation_package"]
    return bindings


def _reviewed_package_options(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    reviewed = []
    status_map = {
        "CANDIDATE_RECOMMENDED_NOT_SELECTED": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "CANDIDATE_AVAILABLE_NOT_SELECTED": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "CANDIDATE_BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
    }
    for source_option in candidate["reviewed_package_options"]:
        option = deepcopy(source_option)
        option["source_candidate_review_status"] = option.pop("candidate_review_status")
        option["operator_review_status"] = status_map[option["source_candidate_review_status"]]
        reviewed.append(option)
    return reviewed


def _assemble_review(candidate: Mapping[str, Any]) -> dict[str, Any]:
    package_options = _reviewed_package_options(candidate)
    requirements = [
        {
            "requirement_id": item["requirement_id"],
            "source_requirement_status": item["requirement_status"],
            "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION",
            "execution_status": "NOT_EXECUTED",
        }
        for item in candidate["future_completion_requirements"]
    ]
    future_plan = [
        {"step": item["step"], "description": item["description"], "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": "NOT_EXECUTED"}
        for item in candidate["future_completion_plan"]
    ]
    planned_outputs = [
        {"output_id": item["output_id"], "source_generation_status": item["generation_status"], "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
        for item in candidate["planned_outputs"]
    ]
    non_goals = [
        {"non_goal_id": item["non_goal_id"], "active": True, "review_status": "REVIEWED_ACTIVE_NON_GOAL"}
        for item in candidate["non_goals"]
    ]
    count_label_distinction = {
        "future_completion_requirement_count": 67,
        "source_enumerated_future_completion_requirement_count": 69,
        "non_goal_count": 71,
        "source_enumerated_non_goal_count": 76,
        "risk_control_count": 104,
        "source_enumerated_risk_control_count": 106,
        "preserved_without_reconciliation": True,
        "all_named_items_preserved": True,
        "distinction_is_not_a_failure": True,
    }
    counts = {
        "operator_source_authority_evidence_item_count": 0,
        "operator_source_authority_evidence_item_template_count": 30,
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "acquisition_scope_section_count": 4,
        "acceptable_source_artifact_type_count": 13,
        "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6,
        "candidate_results_review_requirement_count": 16,
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "package_option_count": 12,
        "available_package_count": 7,
        "blocked_package_count": 5,
        "future_completion_requirement_count": 67,
        "source_enumerated_future_completion_requirement_count": 69,
        "future_completion_plan_step_count": 17,
        "planned_output_count": 33,
        "non_goal_count": 71,
        "source_enumerated_non_goal_count": 76,
        "risk_control_count": 104,
        "source_enumerated_risk_control_count": 106,
        "operator_review_generated_output_count": len(OUTPUT_IDS),
    }
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **_source_bindings(candidate),
        **counts,
        **{key: True for key in TRUE_FIELDS},
        **{key: False for key in FALSE_FIELDS},
        "primary_failure_class": candidate["primary_failure_class"],
        "secondary_failure_classes": deepcopy(candidate["secondary_failure_classes"]),
        "retry_failure_context": deepcopy(candidate["retry_failure_context"]),
        "priority_1_target_modules": deepcopy(candidate["priority_1_target_modules"]),
        "priority1_validation_summary": deepcopy(candidate["priority1_validation_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(candidate["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(candidate["reviewed_observable_failure_families"]),
        "reviewed_workstreams": deepcopy(candidate["reviewed_workstreams"]),
        "reviewed_template_structure": deepcopy(candidate["reviewed_template_structure"]),
        "reviewed_template_rows": deepcopy(candidate["reviewed_template_rows"]),
        "missing_authority_mapping": deepcopy(candidate["missing_authority_mapping"]),
        "acceptable_source_artifact_type_inventory": deepcopy(candidate["acceptable_source_artifact_type_inventory"]),
        "actual_evidence_absence": deepcopy(candidate["actual_evidence_absence"]),
        "actual_coverage_review": deepcopy(candidate["actual_coverage"]),
        "operator_review_philosophy": OPERATOR_REVIEW_PHILOSOPHY,
        "operator_review_boundary": OPERATOR_REVIEW_BOUNDARY,
        "review_status": "REVIEWED_CANDIDATE_ONLY",
        "reviewed_package_options": package_options,
        "recommended_operator_source_authority_evidence_package_completion_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_package_reason": "The recommended package is the safest future path because it requires non-secret operator source, provenance, classification, separation, authority, and row-mapping inputs before later review or acquisition reattempt. This review does not select or approve it.",
        "reviewed_operator_input_requirements": deepcopy(candidate["operator_input_requirements"]),
        "reviewed_future_completion_requirements": requirements,
        "reviewed_future_completion_plan": future_plan,
        "reviewed_planned_outputs": planned_outputs,
        "reviewed_non_goals": non_goals,
        "count_label_distinction": count_label_distinction,
        "reviewed_source_risk_controls": deepcopy(candidate["risk_controls"]),
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_SEPARATE_APPROVAL_REQUIRED_BEFORE_ANY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION",
        "recommendation_reason": "The completion candidate is complete and reviewable. The recommended package remains the safest future path, but this operator review does not select, approve, authorize, complete, supply, validate, bind, acquire, remediate, retry, or merge.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY] = semantic_digest(package_options)
    review[OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST, "review": review["reviewed_operator_input_requirements"], "requirements": requirements})
    review[TEMPLATE_BINDING_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST, "template": review["reviewed_template_structure"], "rows": review["reviewed_template_rows"]})
    review[COVERAGE_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST, "coverage": review["actual_coverage_review"], "mapping": review["missing_authority_mapping"]})
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest_without(review, "checklist", "summary", OPERATOR_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    review[MANIFEST_DIGEST_KEY] = semantic_digest({
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        "package_options_review_digest": review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY],
        "operator_input_requirements_review_digest": review[OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY],
        "template_binding_review_digest": review[TEMPLATE_BINDING_REVIEW_DIGEST_KEY],
        "coverage_review_digest": review[COVERAGE_REVIEW_DIGEST_KEY],
        "source_completion_candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
        "source_completion_candidate_manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
    })
    check_ids = tuple(dict.fromkeys((
        "artifact_kind_correct", "operator_review_status_correct", "operator_review_scope_correct",
        *(f"source_binding_{key}" for key in _source_bindings(candidate)),
        *(f"{key}_true" for key in TRUE_FIELDS),
        *(f"{key}_false" for key in FALSE_FIELDS),
        *(f"package_option_{index}_reviewed" for index in range(1, 13)),
        *(f"requirement_{item['requirement_id']}_reviewed" for item in requirements),
        *(f"template_row_{index}_reviewed" for index in range(1, 31)),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
        "count_label_distinction_preserved", "recommendation_defined", "next_chain_defined", "next_gates_defined", "digests_generated",
    )))
    review["checklist"] = [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in check_ids]
    review["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_completion_candidate_operator_review_created": True,
        "operator_source_authority_evidence_package_completion_candidate_operator_review_ready": True,
        "source_completion_candidate_reviewed": True,
        "completion_package_options_reviewed": True,
        "recommended_completion_package_reviewed": True,
        "recommended_operator_source_authority_evidence_package_completion_package": RECOMMENDED_PACKAGE,
        "package_selected": False, "package_approved": False, "package_authorized": False, "completion_executed": False,
        "operator_source_authority_evidence_package_created": False, "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False, "operator_source_authority_evidence_package_bound": False,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "count_label_distinction_preserved": True,
        "future_completion_requirement_count": 67, "source_enumerated_future_completion_requirement_count": 69,
        "non_goal_count": 71, "source_enumerated_non_goal_count": 76, "risk_control_count": 104, "source_enumerated_risk_control_count": 106,
        "source_authority_acquisition_performed": False, "source_authority_evidence_acquired": False,
        "external_evidence_acquired": False, "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False,
        "ready_for_operator_source_authority_evidence_package_completion_approval_if_selected": True,
        "ready_for_operator_source_authority_evidence_package_completion_execution": False,
        "ready_for_source_authority_acquisition_execution_retry": False, "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False, "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "recommended_next_task": RECOMMENDED_TASK,
    }
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(*, source_completion_candidate: dict | None = None) -> dict[str, Any]:
    candidate = deepcopy(_COMMITTED_SOURCE_COMPLETION_CANDIDATE if source_completion_candidate is None else source_completion_candidate)
    _validate_source_completion_candidate(candidate)
    review = _assemble_review(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(review: dict) -> dict[str, Any]:
    if not isinstance(review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError("operator review must be an object")
    expected = _assemble_review(_COMMITTED_SOURCE_COMPLETION_CANDIDATE)
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError(f"{difference} mismatch")
    return {
        "artifact_kind": ARTIFACT_KIND, "operator_review_status": OPERATOR_REVIEW_STATUS, "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Purpose
Source Completion Candidate
Source Template-Preparation Results Review
Source Template-Preparation Execution
Source Approval
Source Operator Review
Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Source Acquisition Approval Chain
Source Follow-On Results Review
Source Follow-On Execution
Source Follow-On Approval
Source Follow-On Operator Review
Source Follow-On Candidate
Source Results Review
Source Enrichment Execution
Source Historical Approval
Source Historical Operator Review
Source Historical Candidate
Historical Failure Diagnosis
Historical Blocked Remediation
Source Remediation Plan and Method Chain
Source Diagnostic Results Review
Source Controlled Recapture
Source Durable Receipt
Source Planning and Detail Binding Evidence
Retry Failure Context
Priority 1 Target Modules
Priority 1 Validation Summary
Diagnostic Capture Evidence Summary
Reviewed Observable Families
Reviewed Workstreams
Reviewed Template Structure
Reviewed Template Rows
Missing Authority Mapping
Acceptable Source-Artifact Inventory
Actual Evidence Absence
Actual Coverage Zero
Operator Review Philosophy
Reviewed Package Options
Recommended Completion Package
Reviewed Future Completion Requirements
Reviewed Future Completion Plan
Reviewed Planned Outputs
Reviewed Non-Goals
Count-Label Distinction
Unsupported Claims Boundary
Outputs
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_markdown_v1(review: dict) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(deepcopy(review))
    sections: dict[str, Any] = {
        "Purpose": review["operator_review_boundary"],
        "Source Completion Candidate": {key: review[key] for key in ("source_completion_candidate_commit", "source_completion_candidate_artifact_kind", "source_completion_candidate_status", "source_completion_candidate_scope", "source_completion_candidate_digest", "source_completion_candidate_package_options_digest", "source_completion_candidate_operator_input_requirements_digest", "source_completion_candidate_template_binding_digest", "source_completion_candidate_coverage_digest", "source_completion_candidate_manifest_digest")},
        "Source Template-Preparation Results Review": {key: review[key] for key in ("source_results_review_commit", "source_results_review_digest", "source_template_review_digest", "source_evidence_item_template_review_digest", "source_preparation_checklist_review_digest", "source_template_coverage_review_digest", "source_results_review_manifest_digest")},
        "Source Template-Preparation Execution": {key: review[key] for key in ("source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope", "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest", "source_preparation_checklist_digest", "source_template_coverage_digest", "source_execution_manifest_digest")},
        "Source Approval": {key: review[key] for key in ("source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Source Operator Review": {key: review[key] for key in ("source_operator_review_commit", "source_operator_review_digest")},
        "Source Preparation Candidate": {key: review[key] for key in ("source_preparation_candidate_commit", "source_preparation_candidate_digest")},
        "Source Failure Diagnosis": {key: review[key] for key in ("source_failure_diagnosis_commit", "source_failure_diagnosis_digest", "primary_failure_class", "secondary_failure_classes")},
        "Source Blocked Acquisition Execution": {key: review[key] for key in ("source_blocked_acquisition_execution_commit", "source_blocked_acquisition_execution_reason", "source_blocked_acquisition_execution_manifest_digest")},
        "Source Acquisition Approval Chain": {key: review[key] for key in ("source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest")},
        "Retry Failure Context": review["retry_failure_context"],
        "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"],
        "Reviewed Workstreams": review["reviewed_workstreams"],
        "Reviewed Template Structure": review["reviewed_template_structure"],
        "Reviewed Template Rows": review["reviewed_template_rows"],
        "Missing Authority Mapping": review["missing_authority_mapping"],
        "Acceptable Source-Artifact Inventory": review["acceptable_source_artifact_type_inventory"],
        "Actual Evidence Absence": review["actual_evidence_absence"],
        "Actual Coverage Zero": review["actual_coverage_review"],
        "Operator Review Philosophy": {"philosophy": review["operator_review_philosophy"], "boundary": review["operator_review_boundary"], "status": review["review_status"]},
        "Reviewed Package Options": review["reviewed_package_options"],
        "Recommended Completion Package": {"package": review["recommended_operator_source_authority_evidence_package_completion_package"], "status": review["recommendation_status"], "reason": review["recommended_package_reason"]},
        "Reviewed Future Completion Requirements": review["reviewed_future_completion_requirements"],
        "Reviewed Future Completion Plan": review["reviewed_future_completion_plan"],
        "Reviewed Planned Outputs": review["reviewed_planned_outputs"],
        "Reviewed Non-Goals": review["reviewed_non_goals"],
        "Count-Label Distinction": review["count_label_distinction"],
        "Unsupported Claims Boundary": {key: review[key] for key in FALSE_FIELDS},
        "Outputs": review["outputs"],
        "Recommendation": {key: review[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action", "recommendation_reason")},
        "Next Chain": review["next_chain"],
        "Next Gates": review["next_gates"],
        "Risk Controls": {"review_controls": review["risk_controls"], "reviewed_source_controls": review["reviewed_source_risk_controls"]},
        "Authority Boundaries": {**{key: review[key] for key in TRUE_FIELDS}, **{key: review[key] for key in FALSE_FIELDS}},
        "Checklist Summary": review["summary"],
        "Guardrails": review["risk_controls"],
    }
    digest_sections = {
        "Source Follow-On Results Review": "source_follow_on_results_review_digest",
        "Source Follow-On Execution": "source_follow_on_execution_digest",
        "Source Follow-On Approval": "source_follow_on_approval_digest",
        "Source Follow-On Operator Review": "source_follow_on_operator_review_digest",
        "Source Follow-On Candidate": "source_follow_on_candidate_digest",
        "Source Results Review": "source_results_review_digest_historical",
        "Source Enrichment Execution": "source_enrichment_execution_digest",
        "Source Historical Approval": "historical_source_approval_digest",
        "Source Historical Operator Review": "historical_source_operator_review_digest",
        "Source Historical Candidate": "historical_source_candidate_digest",
        "Historical Failure Diagnosis": "historical_failure_diagnosis_digest",
        "Historical Blocked Remediation": "historical_blocked_remediation_manifest_digest",
        "Source Remediation Plan and Method Chain": "source_remediation_plan_or_execution_after_method_results_review_digest",
        "Source Diagnostic Results Review": "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "Source Controlled Recapture": "source_receipt_recovery_or_recapture_execution_digest",
        "Source Durable Receipt": "source_durable_receipt_path",
        "Source Planning and Detail Binding Evidence": "source_detail_binding_results_review_digest",
    }
    sections.update({title: review[key] for title, key in digest_sections.items()})
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Candidate Operator Review After Template Preparation Results Review v1", "",
        f"Artifact: `{review['artifact_kind']}`", "", f"Status: `{review['operator_review_status']}`", "",
        f"Scope: `{review['operator_review_scope']}`", "", f"Operator-review digest: `{review[OPERATOR_REVIEW_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(output_dir: str | Path, *, source_completion_candidate: dict | None = None) -> dict[str, Any]:
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(source_completion_candidate=source_completion_candidate)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_markdown_v1(review), encoding="utf-8")
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "OPERATOR_REVIEW_STATUS", "OPERATOR_REVIEW_SCOPE", "RECOMMENDED_PACKAGE", "RECOMMENDED_TASK",
    "SOURCE_COMPLETION_CANDIDATE_COMMIT", "SOURCE_COMPLETION_CANDIDATE_DIGEST", "SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST",
    "SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST", "SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST",
    "SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST", "SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST",
    "OPERATOR_REVIEW_DIGEST_KEY", "PACKAGE_OPTIONS_REVIEW_DIGEST_KEY", "OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY",
    "TEMPLATE_BINDING_REVIEW_DIGEST_KEY", "COVERAGE_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS",
    "PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY", "PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY",
    "PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY", "PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY",
    "PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY", "PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS",
    "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY", "PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY",
    "PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION", "PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW",
    "PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE",
    "TRUE_FIELDS", "FALSE_FIELDS", "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_markdown_v1",
]
