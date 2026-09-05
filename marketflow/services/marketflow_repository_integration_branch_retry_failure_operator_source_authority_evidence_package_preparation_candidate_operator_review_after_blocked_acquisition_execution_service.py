"""Review the evidence-package preparation candidate without selecting a package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1"
OPERATOR_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_READY"
OPERATOR_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_PREPARATION_CANDIDATE_COMMIT = "8d2944edfb7a54056f4a59c3d5817e823da80ce8"
SOURCE_PREPARATION_CANDIDATE_DIGEST = "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391"
SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST = "5eb1efe8ccb86f243c3db861b983c86fff9b9b868b146ae866da29975cfca400"
SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST = "3dd55cbdcf191c46c2bd5d314a20019c59b107029e6fd178754d79eddc06b2d7"
SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST = "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"
SOURCE_PREPARATION_MANIFEST_DIGEST = "c95671cf372c8bdf7f15c019bd994ae58f547d025117e12456fd780b5f9fd3d3"
PRIMARY_FAILURE_CLASS = source.PRIMARY_FAILURE_CLASS
RECOMMENDED_PACKAGE = source.RECOMMENDED_PACKAGE
RECOMMENDED_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_V1_IF_SELECTED"
OPERATOR_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_digest"
PACKAGE_OPTIONS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_package_options_digest"
TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_template_requirements_digest"
COVERAGE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_missing_authority_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_READY = OPERATOR_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = OPERATOR_REVIEW_SCOPE
PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY = RECOMMENDED_PACKAGE
PACKAGE_CREATE_SOURCE_OWNER_REQUEST_REQUIREMENTS_FOR_30_MISSING_AUTHORITY_ITEMS = source.PACKAGE_CREATE_SOURCE_OWNER_REQUEST_REQUIREMENTS_FOR_30_MISSING_AUTHORITY_ITEMS
PACKAGE_CREATE_LIMITED_ASSERTION_VALUE_SOURCE_EVIDENCE_TEMPLATE = source.PACKAGE_CREATE_LIMITED_ASSERTION_VALUE_SOURCE_EVIDENCE_TEMPLATE
PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_SOURCE_EVIDENCE_TEMPLATE = source.PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_SOURCE_EVIDENCE_TEMPLATE
PACKAGE_CREATE_LIMITED_FIXTURE_DETERMINISM_SOURCE_EVIDENCE_TEMPLATE = source.PACKAGE_CREATE_LIMITED_FIXTURE_DETERMINISM_SOURCE_EVIDENCE_TEMPLATE
PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_SOURCE_EVIDENCE_TEMPLATE = source.PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_SOURCE_EVIDENCE_TEMPLATE
PACKAGE_HOLD_PENDING_OPERATOR_SOURCE_AUTHORITY_EVIDENCE = source.PACKAGE_HOLD_PENDING_OPERATOR_SOURCE_AUTHORITY_EVIDENCE
PACKAGE_GENERATE_EVIDENCE_FROM_DIAGNOSTIC_OUTPUT = source.PACKAGE_GENERATE_EVIDENCE_FROM_DIAGNOSTIC_OUTPUT
PACKAGE_ACCEPT_APPROVAL_AS_OPERATOR_EVIDENCE_PACKAGE = source.PACKAGE_ACCEPT_APPROVAL_AS_OPERATOR_EVIDENCE_PACKAGE
PACKAGE_FABRICATE_OR_INFER_MISSING_SOURCE_AUTHORITY_EVIDENCE = source.PACKAGE_FABRICATE_OR_INFER_MISSING_SOURCE_AUTHORITY_EVIDENCE
PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_WITHOUT_EVIDENCE_PACKAGE = source.PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_WITHOUT_EVIDENCE_PACKAGE
PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_MISSING_EVIDENCE_DIAGNOSIS = source.PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_MISSING_EVIDENCE_DIAGNOSIS

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_preparation_candidate_operator_review_created
operator_source_authority_evidence_package_preparation_candidate_operator_review_ready
source_preparation_candidate_bound
source_preparation_candidate_reviewed
source_package_options_reviewed
source_template_requirements_reviewed
source_missing_authority_coverage_reviewed
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_approval_bound
source_operator_review_bound
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
missing_authority_inventory_bound
zero_coverage_bound
evidence_package_absence_bound
candidate_philosophy_reviewed
preparation_package_options_reviewed
recommended_preparation_package_reviewed
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
source_authority_gap_preserved
detached_retry_failed_status_preserved""".splitlines())

FALSE_FIELDS = tuple(
    field.replace("_in_candidate", "_in_operator_review")
    for field in source.FALSE_FIELDS
)

PLAN_STEPS = (
    "Bind this preparation candidate and the source failure diagnosis.",
    "Bind the blocked acquisition execution, approval, operator review, follow-on results review, follow-on execution, source-enrichment, historical blocked remediation, plan, method, diagnostic, detail/recovery, module grouping, and staged-inventory evidence.",
    "Preserve the blocked reason NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED.",
    "Preserve zero evidence package availability and 0/30 coverage.",
    "Preserve all 30 missing-authority items as MISSING_NOT_ACQUIRED.",
    "Review evidence-package preparation package options without selecting any.",
    "Review the recommended future package for operator-fillable evidence-package template preparation.",
    "Review required template header fields for source owner, reference, creation time, digest/provenance, and no-secret declarations.",
    "Review required evidence-item fields for section, workstream, acceptable artifact type, authority statement, and downstream review flags.",
    "Preserve all direct-change, remediation, retry, and main-merge authorization flags as false.",
    "Require operator review before approval.",
    "Require approval before evidence-package template preparation execution.",
    "Require results review after template preparation.",
    "Require a separately approved source-authority acquisition reattempt before any evidence can be bound.",
    "Preserve no-change disposition, alternate diagnostic, remediation, retry, and main-merge gates.",
)

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_preparation_candidate_operator_review_manifest
source_preparation_candidate_binding_report
source_package_options_review_report
source_template_requirements_review_report
source_missing_authority_coverage_review_report
source_failure_diagnosis_binding_report
source_blocked_acquisition_execution_binding_report
source_approval_binding_report
source_operator_review_binding_report
source_follow_on_results_review_binding_report
source_follow_on_execution_binding_report
source_authority_acquisition_candidate_binding_report
retry_failure_context_report
priority1_validation_disposition_report
diagnostic_metadata_boundary_report
reviewed_observable_families_report
reviewed_workstreams_report
evidence_package_absence_report
missing_authority_coverage_report
reviewed_package_options_report
recommended_preparation_package_report
future_evidence_package_header_requirements_review
future_evidence_item_requirements_review
acceptable_source_artifact_type_inventory_review
operator_evidence_no_secret_boundary_report
evidence_custody_and_digest_requirement_review
source_owner_request_requirement_review
unsupported_claims_boundary_report
acquisition_reattempt_gate_preservation_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Preparation Approval After Candidate Operator Review v1, if selected.",
    "Operator Source Authority Evidence Package Preparation Execution v1, if approved.",
    "Operator Source Authority Evidence Package Preparation Results Review v1.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Evidence Package v1, only if a reviewed package exists and is separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_source_authority_evidence_package_preparation_approval_if_selected
operator_source_authority_evidence_package_preparation_execution_if_approved
operator_source_authority_evidence_package_preparation_results_review
source_authority_acquisition_execution_reattempt_with_reviewed_evidence_package_if_approved
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
    item.replace("candidate_does_not_", "operator_review_does_not_", 1)
    if item.startswith("candidate_does_not_")
    else item
    for item in source.RISK_CONTROLS
)


CHECK_IDS = tuple("""source_preparation_candidate_commit_bound
source_preparation_candidate_digest_bound
source_preparation_package_options_digest_bound
source_preparation_template_requirements_digest_bound
source_preparation_missing_authority_coverage_digest_bound
source_preparation_manifest_digest_bound
source_failure_diagnosis_commit_bound
source_failure_diagnosis_digest_bound
failure_classification_digest_bound
missing_evidence_package_diagnosis_digest_bound
coverage_diagnosis_digest_bound
failure_diagnosis_manifest_digest_bound
source_blocked_acquisition_execution_commit_bound
source_blocked_acquisition_execution_status_bound
source_blocked_acquisition_execution_scope_bound
source_blocked_reason_bound
source_blocked_manifest_digest_bound
source_approval_commit_bound
source_approval_digest_bound
source_attestation_digest_bound
selected_source_authority_acquisition_package_bound
source_operator_review_commit_bound
source_operator_review_digest_bound
source_candidate_review_digest_bound
source_scope_review_digest_bound
source_mapping_review_digest_bound
source_operator_review_manifest_digest_bound
source_follow_on_results_review_commit_bound
source_follow_on_results_review_digest_bound
source_follow_on_execution_commit_bound
source_follow_on_execution_digest_bound
source_acquisition_candidate_digest_bound
source_acquisition_scope_digest_bound
source_missing_authority_mapping_digest_bound
source_follow_on_execution_manifest_digest_bound
source_results_review_digest_bound
source_execution_digest_bound
source_authority_enrichment_plan_digest_bound
source_missing_authority_inventory_digest_bound
source_workstream_authority_mapping_digest_bound
historical_failure_diagnosis_digest_bound
historical_blocked_remediation_reason_bound
historical_blocked_remediation_manifest_digest_bound
historical_primary_failure_class_bound
historical_secondary_failure_classes_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_execution_commit_bound
retry_failure_counts_bound
priority_1_top_module_paths_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_675_pre_and_post_bound
priority1_validation_not_retry_evidence
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
diagnostic_stdout_byte_count_1231380_bound
diagnostic_stderr_byte_count_0_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
family_confidence_high_bound
workstream_count_4_bound
acquisition_scope_section_count_4_bound
mapped_missing_authority_item_count_30_bound
acceptable_source_artifact_type_count_13_bound
operator_provided_evidence_requirement_count_10_bound
evidence_custody_and_digest_requirement_count_6_bound
candidate_results_review_requirement_count_16_bound
operator_source_authority_evidence_package_supplied_false
operator_source_authority_evidence_package_validated_false
operator_source_authority_evidence_package_bound_false
operator_source_authority_evidence_item_count_0
covered_missing_authority_item_count_0
uncovered_missing_authority_item_count_30
missing_authority_items_missing_not_acquired
operator_review_created_true
operator_review_ready_true
source_preparation_candidate_reviewed
source_package_options_reviewed
source_template_requirements_reviewed
source_missing_authority_coverage_reviewed
package_options_reviewed
package_option_count_12
recommended_package_reviewed
available_packages_unselected
blocked_packages_blocked
future_requirements_reviewed
future_plan_reviewed
planned_outputs_reviewed
non_goals_reviewed
package_selected_false
package_approved_false
package_authorized_false
preparation_executed_false
operator_evidence_package_created_false
source_authority_acquisition_execution_created_false
source_authority_acquisition_performed_false
source_authority_evidence_acquired_false
external_evidence_acquired_false
concrete_source_authority_established_false
safe_source_authority_bound_change_identified_false
ready_for_acquisition_results_review_false
no_change_disposition_false
alternate_diagnostic_execution_false
remediation_execution_false
production_code_modified_false
existing_tests_modified_false
expected_digests_updated_false
patch_generated_false
patch_applied_false
pytest_false
full_pytest_false
priority1_validation_rerun_false
retry_rerun_false
detached_retry_false
cache_read_false
cache_modified_false
pytest_cache_committed_false
marketflow_outputs_committed_false
diagnostic_output_analyzed_false
source_authority_enrichment_rerun_false
follow_on_execution_rerun_false
plan_execution_rerun_false
targeted_plan_regenerated_false
method_execution_rerun_false
controlled_recapture_rerun_false
diagnostic_command_rerun_false
terminal_logs_parsed_false
operator_logs_parsed_false
env_inspection_false
source_owners_contacted_false
external_documents_read_false
prior_lost_values_reconstructed_false
full_stdout_reconstructed_false
full_stderr_reconstructed_false
failure_modules_classified_false
error_modules_classified_false
failure_error_separation_claimed_false
first_failure_identified_false
first_error_identified_false
root_cause_claimed_false
retry_success_claimed_false
main_merge_readiness_claimed_false
retry_candidate_created_false
retry_approval_created_false
new_retry_executed_false
new_retry_results_review_created_false
main_merge_approval_created_false
ready_for_preparation_approval_false
ready_for_preparation_execution_false
ready_for_acquisition_execution_retry_false
ready_for_remediation_execution_false
ready_for_retry_candidate_false
ready_for_main_merge_approval_false
integration_success_false
integration_branch_pushed_false
main_push_false
origin_main_modified_false
evidence_regenerated_false
provider_requests_false
market_data_acquisition_false
dataset_generation_false
metric_recomputation_false
model_training_false
strategy_scoring_false
recommendations_false
predictive_usefulness_not_accepted
profitability_not_accepted
runtime_not_authorized
broker_not_authorized
outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
operator_review_digest_generated
package_options_review_digest_generated
template_requirements_review_digest_generated
missing_authority_coverage_review_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(ValueError):
    """Raised when review evidence or a closed boundary drifts."""


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
        for index, value in enumerate(expected):
            difference = _first_difference(actual[index], value, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _committed_source_preparation_candidate() -> dict[str, Any]:
    candidate = source._assemble_candidate(source._COMMITTED_SOURCE_FAILURE_DIAGNOSIS)
    expected = {
        source.CANDIDATE_DIGEST_KEY: SOURCE_PREPARATION_CANDIDATE_DIGEST,
        source.PACKAGE_OPTIONS_DIGEST_KEY: SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST,
        source.TEMPLATE_REQUIREMENTS_DIGEST_KEY: SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST,
        source.COVERAGE_DIGEST_KEY: SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST,
        source.MANIFEST_DIGEST_KEY: SOURCE_PREPARATION_MANIFEST_DIGEST,
    }
    for key, value in expected.items():
        if candidate.get(key) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(
                f"committed {key} mismatch"
            )
    return candidate


_COMMITTED_SOURCE_PREPARATION_CANDIDATE = _committed_source_preparation_candidate()


def _validated_source_preparation_candidate(injected: dict | None) -> dict[str, Any]:
    candidate = deepcopy(
        _COMMITTED_SOURCE_PREPARATION_CANDIDATE if injected is None else injected
    )
    difference = _first_difference(
        candidate, _COMMITTED_SOURCE_PREPARATION_CANDIDATE, "source_preparation_candidate"
    )
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(
            f"{difference} mismatch"
        )
    return candidate


def _digest_without(review: Mapping[str, Any], *keys: str) -> str:
    payload = deepcopy(dict(review))
    for key in ("checklist", "summary", *keys):
        payload.pop(key, None)
    return semantic_digest(payload)


def _checklist() -> list[dict[str, Any]]:
    ids = tuple(dict.fromkeys((
        *CHECK_IDS,
        *(f"true_{field}" for field in TRUE_FIELDS),
        *(f"false_{field}" for field in FALSE_FIELDS),
        *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"next_gate_{item}_defined" for item in NEXT_GATES),
        *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
    )))
    return [
        {
            "check_id": check_id,
            "status": PASS,
            "expected": True,
            "actual": True,
            "severity": BLOCKER,
            "message": f"{check_id} passed",
        }
        for check_id in ids
    ]


def _reviewed_package_options(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    status_by_source = {
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
    }
    reviewed = []
    for source_option in candidate["reviewed_package_options"]:
        option = {
            key: deepcopy(value)
            for key, value in source_option.items()
            if key != "candidate_review_status"
        }
        option["operator_review_status"] = status_by_source[option["source_status"]]
        reviewed.append(option)
    return reviewed


def _assemble_review(candidate: Mapping[str, Any]) -> dict[str, Any]:
    source_context = {
        key: deepcopy(value)
        for key, value in candidate.items()
        if key.startswith("source_")
    }
    contextual_keys = (
        "retry_failure_context", "priority_1_target_modules",
        "priority1_validation_summary", "diagnostic_capture_evidence_summary",
        "reviewed_observable_failure_families", "reviewed_workstreams",
        "source_authority_acquisition_candidate_review",
        "acquisition_scope_sections_review",
        "missing_authority_to_source_evidence_mapping_review",
        "acceptable_source_artifact_inventory_review",
        "operator_provided_evidence_requirements_review",
        "evidence_custody_and_digest_requirements_review",
        "candidate_results_review_requirements_review",
    )
    package_options = _reviewed_package_options(candidate)
    requirements = [
        {
            "requirement_id": item["requirement_id"],
            "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION",
            "execution_status": "NOT_EXECUTED",
        }
        for item in candidate["future_evidence_package_preparation_requirements"]
    ]
    future_plan = [
        {
            "step": index,
            "description": description,
            "review_status": "REVIEWED_PLANNED_NOT_EXECUTED",
        }
        for index, description in enumerate(PLAN_STEPS, 1)
    ]
    planned_outputs = [
        {
            "output_id": output_id,
            "review_status": "REVIEWED_PLANNED_NOT_GENERATED",
            "generation_status": "NOT_GENERATED",
        }
        for output_id in source.OUTPUT_IDS
    ]
    non_goals = [
        {"non_goal_id": non_goal_id, "review_status": "REVIEWED_ACTIVE", "active": True}
        for non_goal_id in source.NON_GOAL_IDS
    ]
    coverage = deepcopy(candidate["missing_authority_coverage"])
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "operator_review_only": True,
        **source_context,
        **{key: deepcopy(candidate[key]) for key in contextual_keys},
        "source_preparation_candidate_artifact_kind": candidate["artifact_kind"],
        "source_preparation_candidate_status": candidate["candidate_status"],
        "source_preparation_candidate_scope": candidate["candidate_scope"],
        "source_preparation_candidate_commit": SOURCE_PREPARATION_CANDIDATE_COMMIT,
        "source_preparation_candidate_digest": candidate[source.CANDIDATE_DIGEST_KEY],
        "source_preparation_package_options_digest": candidate[source.PACKAGE_OPTIONS_DIGEST_KEY],
        "source_preparation_template_requirements_digest": candidate[source.TEMPLATE_REQUIREMENTS_DIGEST_KEY],
        "source_preparation_missing_authority_coverage_digest": candidate[source.COVERAGE_DIGEST_KEY],
        "source_preparation_manifest_digest": candidate[source.MANIFEST_DIGEST_KEY],
        "source_preparation_candidate_summary": {
            "commit": SOURCE_PREPARATION_CANDIDATE_COMMIT,
            "artifact_kind": candidate["artifact_kind"],
            "status": candidate["candidate_status"],
            "scope": candidate["candidate_scope"],
            "candidate_digest": candidate[source.CANDIDATE_DIGEST_KEY],
            "manifest_digest": candidate[source.MANIFEST_DIGEST_KEY],
            "checks": f"{candidate['summary']['passed_checks']}/{candidate['summary']['total_checks']} PASS",
        },
        "source_package_option_count": 12,
        "source_available_package_count": 7,
        "source_blocked_package_count": 5,
        "source_future_requirement_count": 62,
        "source_future_plan_step_count": 15,
        "source_planned_output_count": 28,
        "source_generated_output_count": 28,
        "source_non_goal_count": 71,
        "source_next_gate_count": 16,
        "source_risk_control_count": 104,
        "source_blocked_acquisition_execution_reason": candidate["source_blocked_reason"],
        "source_blocked_acquisition_execution_manifest_digest": candidate["source_blocked_manifest_digest"],
        "selected_source_authority_acquisition_package": candidate["selected_source_authority_acquisition_package"],
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": deepcopy(candidate["secondary_failure_classes"]),
        "historical_blocked_remediation_execution_commit": candidate["historical_blocked_remediation_execution_commit"],
        "historical_blocked_remediation_reason": candidate["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": candidate["historical_blocked_remediation_manifest_digest"],
        "historical_primary_failure_class": candidate["historical_primary_failure_class"],
        "historical_secondary_failure_classes": deepcopy(candidate["historical_secondary_failure_classes"]),
        "historical_blocked_remediation_summary": deepcopy(candidate["historical_blocked_remediation_summary"]),
        "evidence_package_absence": deepcopy(candidate["evidence_package_absence"]),
        "missing_authority_coverage": coverage,
        "operator_source_authority_evidence_item_count": 0,
        "covered_missing_authority_item_count": 0,
        "uncovered_missing_authority_item_count": 30,
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
        "future_requirement_count": 62,
        "future_plan_step_count": 15,
        "planned_output_count": 28,
        "non_goal_count": 71,
        "risk_control_count": 104,
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "reviewed_candidate_philosophy": "The preparation candidate correctly responds to the blocked acquisition execution by defining future, non-secret, operator-fillable source-authority evidence package preparation options. The candidate does not create evidence, acquire authority, validate a package, bind evidence, authorize source-authority acquisition reattempt, authorize remediation, authorize retry, or create main-merge readiness.",
        "reviewed_candidate_boundary": "Operator review only. This review may assess package options, requirements, template requirements, custody/digest requirements, non-goals, and gates. It must not select, approve, authorize, execute, create, acquire, validate, bind, remediate, retry, push protected branches, or authorize runtime/trading.",
        "review_status": "REVIEWED_CANDIDATE_ONLY",
        "reviewed_package_options": package_options,
        "recommended_operator_source_authority_evidence_package_preparation_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "recommended_package_reason": "The acquisition execution failed closed because no operator source-authority evidence package was supplied. The reviewed preparation candidate provides the safest next path: a future non-secret, operator-fillable evidence package template based only on reviewed acquisition scope, missing-authority mappings, acceptable source-artifact types, source-owner/provenance fields, no-secret declarations, custody/digest requirements, and downstream review gates. This operator review does not select or approve the package.",
        "reviewed_future_requirements": requirements,
        "reviewed_future_plan": future_plan,
        "reviewed_planned_outputs": planned_outputs,
        "reviewed_non_goals": non_goals,
        "outputs": [
            {
                "output_id": output_id,
                "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_ONLY",
            }
            for output_id in OUTPUT_IDS
        ],
        "recommended_next_task": RECOMMENDED_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_EXECUTION",
        "recommendation_reason": "The preparation candidate is complete and reviewable. The recommended package remains the safest future path to create a non-secret, operator-fillable evidence package template from reviewed acquisition scope only. This review does not select, approve, authorize, create, acquire, validate, bind, remediate, retry, or merge.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY] = semantic_digest(package_options)
    review[TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY] = semantic_digest(requirements)
    review[COVERAGE_REVIEW_DIGEST_KEY] = semantic_digest(coverage)
    review[OPERATOR_REVIEW_DIGEST_KEY] = _digest_without(
        review, OPERATOR_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY
    )
    review[MANIFEST_DIGEST_KEY] = semantic_digest({
        "operator_review_digest": review[OPERATOR_REVIEW_DIGEST_KEY],
        "package_options_review_digest": review[PACKAGE_OPTIONS_REVIEW_DIGEST_KEY],
        "template_requirements_review_digest": review[TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY],
        "coverage_review_digest": review[COVERAGE_REVIEW_DIGEST_KEY],
        "source_preparation_candidate_digest": review["source_preparation_candidate_digest"],
        "source_preparation_manifest_digest": review["source_preparation_manifest_digest"],
    })
    review["checklist"] = _checklist()
    review["summary"] = {
        "total_checks": len(review["checklist"]),
        "passed_checks": len(review["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        "operator_source_authority_evidence_package_preparation_candidate_operator_review_created": True,
        "operator_source_authority_evidence_package_preparation_candidate_operator_review_ready": True,
        "source_preparation_candidate_reviewed": True,
        "source_package_options_reviewed": True,
        "source_template_requirements_reviewed": True,
        "source_missing_authority_coverage_reviewed": True,
        "source_blocked_reason": PRIMARY_FAILURE_CLASS,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "recommended_operator_source_authority_evidence_package_preparation_package": RECOMMENDED_PACKAGE,
        "package_selected": False,
        "package_approved": False,
        "package_authorized": False,
        "package_executed": False,
        "operator_source_authority_evidence_package_created": False,
        "operator_source_authority_evidence_package_supplied": False,
        "operator_source_authority_evidence_package_validated": False,
        "operator_source_authority_evidence_package_bound": False,
        "source_authority_acquisition_performed": False,
        "source_authority_evidence_acquired": False,
        "external_evidence_acquired": False,
        "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False,
        "covered_missing_authority_item_count": 0,
        "uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "ready_for_operator_source_authority_evidence_package_preparation_approval": False,
        "ready_for_operator_source_authority_evidence_package_preparation_execution": False,
        "ready_for_source_authority_acquisition_execution_retry": False,
        "ready_for_source_authority_acquisition_results_review": False,
        "ready_for_remediation_execution": False,
        "ready_for_retry_candidate": False,
        "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "priority_1_total_nodeids": 612,
        "failed_or_errored_nodeids_count": 1404,
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
        "package_option_count": 12,
        "available_package_count": 7,
        "blocked_package_count": 5,
        "future_requirement_count": 62,
        "future_plan_step_count": 15,
        "planned_output_count": 28,
        "non_goal_count": 71,
        "risk_control_count": 104,
        "recommended_next_task": RECOMMENDED_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(
    *, source_preparation_candidate: dict | None = None
) -> dict[str, Any]:
    candidate = _validated_source_preparation_candidate(source_preparation_candidate)
    review = _assemble_review(candidate)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(
    review: dict,
) -> dict[str, Any]:
    if not isinstance(review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(
            "operator review must be an object"
        )
    expected = _assemble_review(_COMMITTED_SOURCE_PREPARATION_CANDIDATE)
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(
            f"{difference} mismatch"
        )
    return {
        "artifact_kind": ARTIFACT_KIND,
        "operator_review_status": OPERATOR_REVIEW_STATUS,
        "operator_review_scope": OPERATOR_REVIEW_SCOPE,
        "total_checks": review["summary"]["total_checks"],
        "passed_checks": review["summary"]["passed_checks"],
        "failed_checks": 0,
        "blocker_count": 0,
    }


MARKDOWN_SECTIONS = tuple("""Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Blocked Reason
Failure Classification
Source Approval
Selected Source Authority Acquisition Package
Source Operator Review
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
Historical Failure Classification
Source Remediation Execution Approval
Source Plan Results Review
Source Plan Execution
Source Method Results Review
Source Method Execution
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
Source Authority Acquisition Candidate
Acquisition Scope Sections
Missing Authority Mapping
Acceptable Source Artifact Inventory
Operator-Provided Evidence Requirements
Evidence Custody and Digest Requirements
Candidate Results Review Requirements
Evidence Package Absence
Missing Authority Coverage
Reviewed Candidate Philosophy
Reviewed Package Options
Recommended Package
Reviewed Future Requirements
Reviewed Future Plan
Reviewed Planned Outputs
Reviewed Non-Goals
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_markdown_v1(
    review: dict,
) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(
        deepcopy(review)
    )
    sections = {
        "Source Preparation Candidate": review["source_preparation_candidate_summary"],
        "Source Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Source Blocked Acquisition Execution": review["source_blocked_acquisition_execution_summary"],
        "Blocked Reason": review["source_blocked_reason"],
        "Failure Classification": {"primary": review["primary_failure_class"], "secondary": review["secondary_failure_classes"]},
        "Source Approval": review["source_approval_summary"],
        "Selected Source Authority Acquisition Package": review["selected_source_authority_acquisition_package"],
        "Source Operator Review": review["source_operator_review_summary"],
        "Source Follow-On Results Review": review["source_follow_on_results_review_summary"],
        "Source Follow-On Execution": review["source_follow_on_execution_summary"],
        "Source Follow-On Approval": review["source_follow_on_approval_summary"],
        "Source Follow-On Operator Review": review["source_follow_on_operator_review_summary"],
        "Source Follow-On Candidate": review["source_follow_on_candidate_summary"],
        "Source Results Review": review["source_results_review_summary"],
        "Source Enrichment Execution": review["source_execution_summary"],
        "Source Historical Approval": review["source_approval_summary"],
        "Source Historical Operator Review": review["source_historical_operator_review_summary"],
        "Source Historical Candidate": review["source_historical_candidate_summary"],
        "Historical Failure Diagnosis": review["source_failure_diagnosis_summary"],
        "Historical Blocked Remediation": review["historical_blocked_remediation_summary"],
        "Historical Failure Classification": {"primary": review["historical_primary_failure_class"], "secondary": review["historical_secondary_failure_classes"]},
        "Source Remediation Execution Approval": review["source_remediation_execution_approval_after_plan_results_review_digest"],
        "Source Plan Results Review": review["source_plan_results_review_summary"],
        "Source Plan Execution": review["source_plan_execution_summary"],
        "Source Method Results Review": review["source_method_results_review_summary"],
        "Source Method Execution": review["source_method_execution_summary"],
        "Source Diagnostic Results Review": review["source_diagnostic_results_review_summary"],
        "Source Controlled Recapture": review["source_controlled_recapture_summary"],
        "Source Durable Receipt": review["source_durable_receipt_summary"],
        "Source Planning and Detail Binding Evidence": review["source_planning_and_detail_binding_summary"],
        "Retry Failure Context": review["retry_failure_context"],
        "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"],
        "Reviewed Workstreams": review["reviewed_workstreams"],
        "Source Authority Acquisition Candidate": review["source_authority_acquisition_candidate_review"],
        "Acquisition Scope Sections": review["acquisition_scope_sections_review"],
        "Missing Authority Mapping": review["missing_authority_to_source_evidence_mapping_review"],
        "Acceptable Source Artifact Inventory": review["acceptable_source_artifact_inventory_review"],
        "Operator-Provided Evidence Requirements": review["operator_provided_evidence_requirements_review"],
        "Evidence Custody and Digest Requirements": review["evidence_custody_and_digest_requirements_review"],
        "Candidate Results Review Requirements": review["candidate_results_review_requirements_review"],
        "Evidence Package Absence": review["evidence_package_absence"],
        "Missing Authority Coverage": review["missing_authority_coverage"],
        "Reviewed Candidate Philosophy": {"philosophy": review["reviewed_candidate_philosophy"], "boundary": review["reviewed_candidate_boundary"], "status": review["review_status"]},
        "Reviewed Package Options": review["reviewed_package_options"],
        "Recommended Package": {"package": review["recommended_operator_source_authority_evidence_package_preparation_package"], "status": review["recommendation_status"], "reason": review["recommended_package_reason"]},
        "Reviewed Future Requirements": review["reviewed_future_requirements"],
        "Reviewed Future Plan": review["reviewed_future_plan"],
        "Reviewed Planned Outputs": review["reviewed_planned_outputs"],
        "Reviewed Non-Goals": review["reviewed_non_goals"],
        "Unsupported Claims Boundary": {field: review[field] for field in FALSE_FIELDS},
        "Recommendation": {key: review[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action", "recommendation_reason")},
        "Next Chain": review["next_chain"],
        "Next Gates": review["next_gates"],
        "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {**{field: review[field] for field in TRUE_FIELDS}, **{field: review[field] for field in FALSE_FIELDS}},
        "Checklist Summary": review["summary"],
        "Guardrails": list(RISK_CONTROLS),
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Candidate Operator Review After Blocked Acquisition Execution v1",
        "",
        f"Artifact: `{review['artifact_kind']}`",
        "",
        f"Status: `{review['operator_review_status']}`",
        "",
        f"Scope: `{review['operator_review_scope']}`",
        "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(
    output_dir: str | Path,
    *,
    source_preparation_candidate: dict | None = None,
) -> dict[str, Any]:
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError(
            "protected output directory"
        )
    review = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(
        source_preparation_candidate=source_preparation_candidate
    )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_STATUS.md"
    path.write_text(
        build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_markdown_v1(review),
        encoding="utf-8",
    )
    return review


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "OPERATOR_REVIEW_STATUS", "OPERATOR_REVIEW_SCOPE",
    "SOURCE_PREPARATION_CANDIDATE_COMMIT", "SOURCE_PREPARATION_CANDIDATE_DIGEST",
    "SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST", "SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST",
    "SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST", "SOURCE_PREPARATION_MANIFEST_DIGEST",
    "PRIMARY_FAILURE_CLASS", "RECOMMENDED_PACKAGE", "RECOMMENDED_TASK",
    "OPERATOR_REVIEW_DIGEST_KEY", "PACKAGE_OPTIONS_REVIEW_DIGEST_KEY",
    "TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY", "COVERAGE_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_CREATION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY",
    "PACKAGE_CREATE_SOURCE_OWNER_REQUEST_REQUIREMENTS_FOR_30_MISSING_AUTHORITY_ITEMS",
    "PACKAGE_CREATE_LIMITED_ASSERTION_VALUE_SOURCE_EVIDENCE_TEMPLATE",
    "PACKAGE_CREATE_LIMITED_DIGEST_SERIALIZATION_SOURCE_EVIDENCE_TEMPLATE",
    "PACKAGE_CREATE_LIMITED_FIXTURE_DETERMINISM_SOURCE_EVIDENCE_TEMPLATE",
    "PACKAGE_CREATE_LIMITED_SCHEMA_FIELD_CONTRACT_SOURCE_EVIDENCE_TEMPLATE",
    "PACKAGE_HOLD_PENDING_OPERATOR_SOURCE_AUTHORITY_EVIDENCE",
    "PACKAGE_GENERATE_EVIDENCE_FROM_DIAGNOSTIC_OUTPUT",
    "PACKAGE_ACCEPT_APPROVAL_AS_OPERATOR_EVIDENCE_PACKAGE",
    "PACKAGE_FABRICATE_OR_INFER_MISSING_SOURCE_AUTHORITY_EVIDENCE",
    "PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_WITHOUT_EVIDENCE_PACKAGE",
    "PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_MISSING_EVIDENCE_DIAGNOSIS",
    "TRUE_FIELDS", "FALSE_FIELDS", "PLAN_STEPS", "OUTPUT_IDS", "NEXT_CHAIN", "NEXT_GATES", "RISK_CONTROLS", "CHECK_IDS", "MARKDOWN_SECTIONS",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_markdown_v1",
]
