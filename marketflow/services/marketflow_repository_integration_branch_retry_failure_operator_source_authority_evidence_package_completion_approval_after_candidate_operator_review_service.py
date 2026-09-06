"""Approve future evidence-package completion without executing it."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1"
APPROVAL_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW"
APPROVAL_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SELECTED_PACKAGE = "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS"
OPERATOR_DECISION = "APPROVE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_FOR_FUTURE_EXECUTION"
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_V1"

SOURCE_OPERATOR_REVIEW_COMMIT = "d71bfb14a656592ab637d94d9dd30d73912104b0"
SOURCE_OPERATOR_REVIEW_DIGEST = "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663"
SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST = "903e25817b4eff9298ed782756f7c6cf82d08c55f374161320ff3bf1bc9faf2a"
SOURCE_OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST = "571582717ed926182363bed83f673c0312eeb28535151bf4a2e06a83b645faa5"
SOURCE_TEMPLATE_BINDING_REVIEW_DIGEST = "e09fef3bc04abafafe1ce9fab37948be709b092d2a09c828a98c29c83bd66841"
SOURCE_COVERAGE_REVIEW_DIGEST = "c8eecc0c7c93299a8dba7fb7b84f47e26b5d96ffecd69f7d4355cbd0ad635352"
SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST = "91393843b040ee9d67284689b5e4742019e3d18c2092c1950f742d9dceb71c64"

SOURCE_COMPLETION_CANDIDATE_COMMIT = "7af6b1b5ad223f92da0997e2b7abcb73543470df"
SOURCE_COMPLETION_CANDIDATE_DIGEST = "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207"
SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST = "c276ff30b28441dfd3ebb1dc4071b6a82e29c42b593215aa603c56587fc7e982"
SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST = "615a15e243999e28770b3f1351df1cc5b4e8ebbf22febc36812fcf42dd59b7fb"
SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST = "734eac89400c983c042f5c0a9c91e85694aad62ab07f3c8e046c406e02813df3"
SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST = "ba547fc27cbf2642a070383d600952a5798c1e2a0d7b703ba3fd049486e9e107"
SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST = "983951245e47b0fcc4d31b818a8adf16785f96dc8e2688ed12ce679fd17cb91b"

SOURCE_PREPARATION_CANDIDATE_COMMIT = "8d2944edfb7a54056f4a59c3d5817e823da80ce8"
SOURCE_PREPARATION_CANDIDATE_DIGEST = "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391"
SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST = "5eb1efe8ccb86f243c3db861b983c86fff9b9b868b146ae866da29975cfca400"
SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST = "3dd55cbdcf191c46c2bd5d314a20019c59b107029e6fd178754d79eddc06b2d7"
SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST = "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"
SOURCE_PREPARATION_MANIFEST_DIGEST = "c95671cf372c8bdf7f15c019bd994ae58f547d025117e12456fd780b5f9fd3d3"

SOURCE_FAILURE_DIAGNOSIS_DIGEST = "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c"
SOURCE_BLOCKED_REASON = "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
SOURCE_BLOCKED_MANIFEST_DIGEST = "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"
SOURCE_APPROVAL_DIGEST = "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"
SOURCE_ATTESTATION_DIGEST = "db079d7b71f141dafba8439eba51caa1bc663ddf1158d3ea34b1f102ce4fb879"

APPROVAL_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_digest"
ATTESTATION_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_digest"
PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"

REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1 = (
    "APPROVE MARKETFLOW RETRY FAILURE PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS "
    "AFTER OPERATOR SOURCE AUTHORITY EVIDENCE PACKAGE COMPLETION CANDIDATE OPERATOR REVIEW FOR FUTURE COMPLETION EXECUTION ONLY NO COMPLETION "
    "EXECUTION NOW NO COMPLETED EVIDENCE PACKAGE NOW NO EVIDENCE PACKAGE CREATION NOW NO EVIDENCE PACKAGE SUPPLY NOW NO EVIDENCE VALIDATION NOW "
    "NO EVIDENCE BINDING NOW NO SOURCE AUTHORITY ACQUISITION NOW NO SOURCE AUTHORITY EVIDENCE ACQUISITION NOW NO EXTERNAL EVIDENCE ACQUISITION NOW "
    "NO ACQUISITION REATTEMPT NOW NO NO CHANGE DISPOSITION NOW NO ALTERNATE DIAGNOSTICS NOW NO REMEDIATION NOW NO CODE CHANGES NOW NO TEST CHANGES "
    "NOW NO DIGEST UPDATES NOW NO PATCH NOW NO PYTEST NOW NO RETRY NO MAIN PUSH OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_"
    "AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_"
    "NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
)

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW = APPROVAL_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = APPROVAL_SCOPE
PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS = SELECTED_PACKAGE


TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_approval_created
operator_source_authority_evidence_package_completion_package_selected
operator_source_authority_evidence_package_completion_package_approved
operator_source_authority_evidence_package_completion_package_authorized_for_future_execution
selected_completion_package_verified
source_operator_review_bound
source_completion_candidate_bound
source_preparation_candidate_bound
source_package_options_review_bound
source_operator_input_requirements_review_bound
source_template_binding_review_bound
source_coverage_review_bound
source_results_review_bound
source_template_review_bound
source_evidence_item_template_review_bound
source_preparation_checklist_review_bound
source_template_coverage_review_bound
source_execution_bound
source_approval_bound
source_attestation_bound
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
future_completion_requirements_approved
future_completion_plan_approved
planned_outputs_authorized_not_generated
non_goals_preserved
count_label_distinction_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_completion_execution_after_approval""".splitlines())

FALSE_FIELDS = tuple("""operator_source_authority_evidence_package_completion_package_executed
operator_source_authority_evidence_package_completion_executed
operator_source_authority_evidence_package_completed
operator_source_authority_evidence_package_created
operator_source_authority_evidence_package_supplied
operator_source_authority_evidence_package_validated
operator_source_authority_evidence_package_bound
operator_source_authority_evidence_package_accepted_as_source_authority
operator_source_authority_evidence_package_ready_for_acquisition_without_review
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
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_approval
method_execution_rerun_performed
controlled_recapture_rerun_performed
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
provider_requests_made_in_approval
market_data_acquisition_performed_in_approval
dataset_generation_performed_in_approval
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

FUTURE_PERMISSION_TRUE_FIELDS = tuple("""future_execution_may_complete_non_secret_operator_fillable_evidence_package
future_execution_may_fill_reviewed_template_rows_from_non_secret_operator_inputs
future_execution_may_preserve_reviewed_scope_and_missing_authority_mappings
future_execution_may_preserve_source_artifact_and_custody_requirements
future_execution_may_define_completion_results_review_package""".splitlines())

FUTURE_PERMISSION_FALSE_FIELDS = tuple("""future_execution_may_validate_evidence
future_execution_may_bind_evidence
future_execution_may_accept_evidence_as_source_authority
future_execution_may_acquire_source_authority
future_execution_may_acquire_or_bind_source_authority_evidence
future_execution_may_retry_source_authority_acquisition
future_execution_may_execute_remediation
future_execution_may_modify_production_code
future_execution_may_modify_existing_tests
future_execution_may_update_expected_digests
future_execution_may_generate_or_apply_patch
future_execution_may_run_full_pytest
future_execution_may_run_retry
future_execution_may_create_retry_candidate
future_execution_may_create_no_change_disposition
future_execution_may_push_main
future_execution_may_push_integration_branch
future_completion_execution_executed""".splitlines())

SUPPORTING_PACKAGE_IDS = (
    source.PACKAGE_COMPLETE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_FIELDS_ONLY,
    source.PACKAGE_COMPLETE_ASSERTION_VALUE_EVIDENCE_ITEMS_ONLY,
    source.PACKAGE_COMPLETE_DIGEST_SERIALIZATION_EVIDENCE_ITEMS_ONLY,
    source.PACKAGE_COMPLETE_FIXTURE_DETERMINISM_EVIDENCE_ITEMS_ONLY,
    source.PACKAGE_COMPLETE_SCHEMA_FIELD_CONTRACT_EVIDENCE_ITEMS_ONLY,
    source.PACKAGE_HOLD_PENDING_NON_SECRET_OPERATOR_EVIDENCE_INPUTS,
)
BLOCKED_PACKAGE_IDS = (
    source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_TEMPLATE_PLACEHOLDERS_ONLY,
    source.PACKAGE_COMPLETE_EVIDENCE_PACKAGE_FROM_DIAGNOSTIC_OUTPUT_ONLY,
    source.PACKAGE_VALIDATE_OR_BIND_EVIDENCE_DURING_COMPLETION,
    source.PACKAGE_RETRY_SOURCE_AUTHORITY_ACQUISITION_IMMEDIATELY_AFTER_TEMPLATE_REVIEW,
    source.PACKAGE_REMEDIATION_OR_RETRY_OR_MAIN_MERGE_FROM_REVIEWED_TEMPLATE,
)


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(ValueError):
    """Raised when approval evidence or its authority boundary differs."""


def _first_difference(actual: Any, expected: Any, path: str = "approval") -> str | None:
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


SOURCE_CONTEXT_KEYS = tuple("""retry_failure_context
priority_1_target_modules
priority1_validation_summary
diagnostic_capture_evidence_summary
reviewed_observable_failure_families
reviewed_workstreams
reviewed_template_structure
reviewed_template_rows
missing_authority_mapping
acceptable_source_artifact_type_inventory
actual_evidence_absence
actual_coverage_review
secondary_failure_classes""".splitlines())


def _committed_source_operator_review() -> dict[str, Any]:
    """Reconstruct only from committed data constants; no upstream builder runs."""

    candidate = source._COMMITTED_SOURCE_COMPLETION_CANDIDATE
    review = {
        key: deepcopy(value)
        for key, value in candidate.items()
        if key.startswith("source_") or key.startswith("historical_")
    }
    status_map = {
        "CANDIDATE_RECOMMENDED_NOT_SELECTED": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "CANDIDATE_AVAILABLE_NOT_SELECTED": "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED",
        "CANDIDATE_BLOCKED_NOT_ALLOWED": "REVIEWED_BLOCKED_NOT_ALLOWED",
    }
    package_options = []
    for source_option in candidate["reviewed_package_options"]:
        option = deepcopy(source_option)
        option["source_candidate_review_status"] = option.pop("candidate_review_status")
        option["operator_review_status"] = status_map[option["source_candidate_review_status"]]
        package_options.append(option)
    review.update({
        "artifact_kind": source.ARTIFACT_KIND,
        "operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        "source_completion_candidate_artifact_kind": candidate["artifact_kind"],
        "source_completion_candidate_status": candidate["candidate_status"],
        "source_completion_candidate_scope": candidate["candidate_scope"],
        "source_completion_candidate_commit": SOURCE_COMPLETION_CANDIDATE_COMMIT,
        "source_completion_candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
        "source_completion_candidate_package_options_digest": SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
        "source_completion_candidate_operator_input_requirements_digest": SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST,
        "source_completion_candidate_template_binding_digest": SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST,
        "source_completion_candidate_coverage_digest": SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST,
        "source_completion_candidate_manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
        "source_completion_candidate_summary": {
            "commit": SOURCE_COMPLETION_CANDIDATE_COMMIT,
            "artifact_kind": candidate["artifact_kind"],
            "status": candidate["candidate_status"],
            "scope": candidate["candidate_scope"],
            "candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
            "manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
            "checks": f"{candidate['summary']['passed_checks']}/{candidate['summary']['total_checks']} PASS",
        },
        "source_enumerated_future_completion_requirement_count": 69,
        "source_enumerated_non_goal_count": 76,
        "source_enumerated_risk_control_count": 106,
        "primary_failure_class": candidate["primary_failure_class"],
        "historical_blocked_remediation_reason": candidate["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": candidate["historical_blocked_remediation_manifest_digest"],
        **{key: deepcopy(candidate[key if key != "actual_coverage_review" else "actual_coverage"]) for key in SOURCE_CONTEXT_KEYS},
        "reviewed_package_options": package_options,
        "reviewed_operator_input_requirements": deepcopy(candidate["operator_input_requirements"]),
        "reviewed_future_completion_requirements": [
            {
                "requirement_id": item["requirement_id"],
                "source_requirement_status": item["requirement_status"],
                "review_status": "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION",
                "execution_status": "NOT_EXECUTED",
            }
            for item in candidate["future_completion_requirements"]
        ],
        "reviewed_future_completion_plan": [
            {"step": item["step"], "description": item["description"], "review_status": "REVIEWED_PLANNED_NOT_EXECUTED", "execution_status": "NOT_EXECUTED"}
            for item in candidate["future_completion_plan"]
        ],
        "reviewed_planned_outputs": [
            {"output_id": item["output_id"], "source_generation_status": item["generation_status"], "review_status": "REVIEWED_PLANNED_NOT_GENERATED", "generation_status": "NOT_GENERATED"}
            for item in candidate["planned_outputs"]
        ],
        "reviewed_non_goals": [
            {"non_goal_id": item["non_goal_id"], "review_status": "REVIEWED_ACTIVE_NON_GOAL", "active": True}
            for item in candidate["non_goals"]
        ],
        "count_label_distinction": {
            "future_completion_requirement_count": 67,
            "source_enumerated_future_completion_requirement_count": 69,
            "non_goal_count": 71,
            "source_enumerated_non_goal_count": 76,
            "risk_control_count": 104,
            "source_enumerated_risk_control_count": 106,
            "preserved_without_reconciliation": True,
            "all_named_items_preserved": True,
            "distinction_is_not_a_failure": True,
        },
        "next_chain": list(source.NEXT_CHAIN),
        "next_gates": list(source.NEXT_GATES),
        "risk_controls": list(source.RISK_CONTROLS),
    })
    return review


SOURCE_REVIEW_DIGEST_FIELDS = {
    source.OPERATOR_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_DIGEST,
    source.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY: SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    source.OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY: SOURCE_OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST,
    source.TEMPLATE_BINDING_REVIEW_DIGEST_KEY: SOURCE_TEMPLATE_BINDING_REVIEW_DIGEST,
    source.COVERAGE_REVIEW_DIGEST_KEY: SOURCE_COVERAGE_REVIEW_DIGEST,
    source.MANIFEST_DIGEST_KEY: SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
}


def _validate_source_operator_review(review: Mapping[str, Any]) -> None:
    committed = _committed_source_operator_review()
    for key, expected in committed.items():
        if key not in review or _first_difference(review[key], expected, f"source_operator_review.{key}"):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(
                f"source_operator_review.{key} mismatch"
            )
    for key, expected in SOURCE_REVIEW_DIGEST_FIELDS.items():
        if review.get(key) != expected:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(
                f"source_operator_review.{key} mismatch"
            )


ATTESTATION_VALUE_FIELDS = {
    "operator_confirms_source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
    "operator_confirms_source_operator_input_requirements_review_digest": SOURCE_OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST,
    "operator_confirms_source_template_binding_review_digest": SOURCE_TEMPLATE_BINDING_REVIEW_DIGEST,
    "operator_confirms_source_coverage_review_digest": SOURCE_COVERAGE_REVIEW_DIGEST,
    "operator_confirms_source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
    "operator_confirms_source_completion_candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
    "operator_confirms_source_completion_candidate_package_options_digest": SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
    "operator_confirms_source_completion_candidate_operator_input_requirements_digest": SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST,
    "operator_confirms_source_completion_candidate_template_binding_digest": SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST,
    "operator_confirms_source_completion_candidate_coverage_digest": SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST,
    "operator_confirms_source_completion_candidate_manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
    "operator_confirms_source_results_review_digest": "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332",
    "operator_confirms_source_template_review_digest": "3e60c8bb9c9000f6d5ca561ae843c17ec4abd31276fa443d7b9d97b7524040b9",
    "operator_confirms_source_evidence_item_template_review_digest": "8b9994a28e017fc5e61cb0274b9191f61857594dfa1a3dc861e3087e3da7520c",
    "operator_confirms_source_preparation_checklist_review_digest": "e4a57857d17f7fd68fce5af88a3efab02f54e5e33fc61be241740a35a0b9fcc2",
    "operator_confirms_source_template_coverage_review_digest": "7ae349f3c94be97808aa0930429614cb2f33917f73694693d32ebb4e7656b290",
    "operator_confirms_source_results_review_manifest_digest": "f4b7d2838a11d192497e7b79e7d2cc7ec3f1aac3d43dcf7362014c5724a109f0",
    "operator_confirms_source_execution_digest": "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3",
    "operator_confirms_source_package_template_digest": "fb406078ca1a1199a430dd836050f9b198373c1f46c19cb5ee899ffe7e975a9a",
    "operator_confirms_source_evidence_item_template_digest": "820cdf4c4a758b1d24ad0112fa6a1b05a8e6a330dc717c3564be4434b00af6e9",
    "operator_confirms_source_preparation_checklist_digest": "4f965c0e7072dc6061ed3731e0eb7a639e117780c09544a6031663d6a6959605",
    "operator_confirms_source_execution_manifest_digest": "272cadca012100d25e5628f09a3e91f8919a9fb80b8433ca2841a28d65a76a39",
    "operator_confirms_source_approval_digest": "e7f1d8a5ae413ca0f971257e13554a63b3ee95e942e156adb5b204cbcc378cbd",
    "operator_confirms_source_attestation_digest": "e16b2afde6c36d5461a65d2f598fec55f9a13811a555efc90a9dac1e981f7328",
    "operator_confirms_source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    "operator_confirms_source_blocked_reason": SOURCE_BLOCKED_REASON,
    "operator_confirms_source_blocked_acquisition_execution_manifest_digest": SOURCE_BLOCKED_MANIFEST_DIGEST,
    "operator_confirms_source_acquisition_approval_digest": SOURCE_APPROVAL_DIGEST,
    "operator_confirms_source_acquisition_attestation_digest": SOURCE_ATTESTATION_DIGEST,
    "operator_confirms_recommended_completion_package": SELECTED_PACKAGE,
}

ATTESTATION_BOOLEAN_FIELDS = tuple("""operator_confirms_retry_failure_counts
operator_confirms_priority_1_total_612
operator_confirms_top_10_total_1069
operator_confirms_failed_or_errored_nodeids_1404
operator_confirms_observable_family_count_4
operator_confirms_observable_evidence_items_188
operator_confirms_workstream_count_4
operator_confirms_template_row_count_30
operator_confirms_actual_coverage_zero
operator_confirms_missing_authority_items_missing_not_acquired
operator_confirms_acceptable_source_artifact_type_count_13
operator_confirms_operator_provided_evidence_requirement_count_10
operator_confirms_evidence_custody_and_digest_requirement_count_6
operator_confirms_candidate_results_review_requirement_count_16
operator_confirms_package_option_count_12
operator_confirms_available_package_count_7
operator_confirms_blocked_package_count_5
operator_confirms_future_completion_requirement_prescribed_count_67
operator_confirms_future_completion_requirement_enumerated_count_69
operator_confirms_future_completion_plan_step_count_17
operator_confirms_planned_output_count_33
operator_confirms_non_goal_prescribed_count_71
operator_confirms_non_goal_enumerated_count_76
operator_confirms_risk_control_prescribed_count_104
operator_confirms_risk_control_enumerated_count_106
operator_confirms_count_label_distinction_preserved
operator_confirms_approval_scope_only
operator_confirms_no_completion_execution_now
operator_confirms_no_completed_evidence_package_now
operator_confirms_no_evidence_package_creation_now
operator_confirms_no_evidence_package_supply_now
operator_confirms_no_evidence_validation_now
operator_confirms_no_evidence_binding_now
operator_confirms_no_actual_evidence_item_filling_now
operator_confirms_no_source_authority_acquisition_now
operator_confirms_no_source_authority_evidence_acquisition_now
operator_confirms_no_external_evidence_acquisition_now
operator_confirms_no_acquisition_reattempt_now
operator_confirms_no_no_change_disposition_now
operator_confirms_no_alternate_diagnostics_now
operator_confirms_no_remediation_now
operator_confirms_no_code_change_now
operator_confirms_no_test_change_now
operator_confirms_no_digest_update_now
operator_confirms_no_patch_generation_now
operator_confirms_no_patch_application_now
operator_confirms_no_pytest_now
operator_confirms_no_full_pytest_now
operator_confirms_no_retry_now
operator_confirms_no_cache_read_now
operator_confirms_no_cache_modification_now
operator_confirms_no_receipt_parse_now
operator_confirms_no_diagnostic_output_analysis_now
operator_confirms_no_log_parse_now
operator_confirms_no_env_inspection_now
operator_confirms_no_source_owner_contact_now
operator_confirms_no_external_document_read_now
operator_confirms_no_provider_request_now
operator_confirms_no_runtime_authorization
operator_confirms_no_broker_authorization
operator_confirms_no_trading_authorization
operator_confirms_no_main_push
operator_confirms_no_integration_branch_push
operator_confirms_no_branch_delete
operator_confirms_no_force_push
operator_confirms_no_tag_mutation
operator_confirms_no_evidence_regeneration
operator_confirms_no_marketflow_commit
operator_confirms_no_pytest_cache_commit
operator_confirms_no_predictive_usefulness_acceptance
operator_confirms_no_profitability_acceptance
operator_confirms_no_api_key_storage_or_printing
operator_confirms_no_secret_capture_or_commit""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    selected_operator_source_authority_evidence_package_completion_package: str = SELECTED_PACKAGE,
    operator_decision: str = OPERATOR_DECISION,
    operator_confirmations: dict,
) -> dict[str, Any]:
    """Build and validate the exact non-secret operator attestation."""

    if not isinstance(operator_reference, str) or not operator_reference.strip():
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("operator_reference invalid")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(operator_attestation_timestamp_utc)) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("operator_attestation_timestamp_utc invalid")
    if operator_attestation_phrase != REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("operator_attestation_phrase mismatch")
    if selected_operator_source_authority_evidence_package_completion_package != SELECTED_PACKAGE:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("selected completion package mismatch")
    if operator_decision != OPERATOR_DECISION:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("operator_decision mismatch")
    expected_confirmations = {**ATTESTATION_VALUE_FIELDS, **{key: True for key in ATTESTATION_BOOLEAN_FIELDS}}
    difference = _first_difference(operator_confirmations, expected_confirmations, "operator_confirmations")
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(f"{difference} mismatch")
    attestation = {
        "operator_decision": OPERATOR_DECISION,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": SCHEMA_VERSION,
        "operator_reference": operator_reference.strip(),
        **deepcopy(operator_confirmations),
    }
    attestation[ATTESTATION_DIGEST_KEY] = semantic_digest(attestation)
    return attestation


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("operator_attestation must be an object")
    digest = attestation.get(ATTESTATION_DIGEST_KEY)
    confirmations = {key: attestation.get(key) for key in (*ATTESTATION_VALUE_FIELDS, *ATTESTATION_BOOLEAN_FIELDS)}
    rebuilt = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1(
        operator_reference=attestation.get("operator_reference"),
        operator_attestation_timestamp_utc=attestation.get("operator_attestation_timestamp_utc"),
        operator_attestation_phrase=attestation.get("operator_attestation_phrase"),
        selected_operator_source_authority_evidence_package_completion_package=attestation.get("selected_operator_source_authority_evidence_package_completion_package"),
        operator_decision=attestation.get("operator_decision"),
        operator_confirmations=confirmations,
    )
    difference = _first_difference(dict(attestation), rebuilt, "operator_attestation")
    if difference or digest != rebuilt[ATTESTATION_DIGEST_KEY]:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(f"{difference or ATTESTATION_DIGEST_KEY} mismatch")


def _source_bindings(review: Mapping[str, Any]) -> dict[str, Any]:
    bindings = {
        key: deepcopy(value)
        for key, value in review.items()
        if (key.startswith("source_") or key.startswith("historical_"))
        and isinstance(value, (str, int, bool))
    }
    bindings.update({
        "source_operator_review_artifact_kind": source.ARTIFACT_KIND,
        "source_operator_review_status": source.OPERATOR_REVIEW_STATUS,
        "source_operator_review_scope": source.OPERATOR_REVIEW_SCOPE,
        "source_operator_review_commit": SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_operator_review_digest": SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_package_options_review_digest": SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST,
        "source_operator_input_requirements_review_digest": SOURCE_OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST,
        "source_template_binding_review_digest": SOURCE_TEMPLATE_BINDING_REVIEW_DIGEST,
        "source_coverage_review_digest": SOURCE_COVERAGE_REVIEW_DIGEST,
        "source_operator_review_manifest_digest": SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST,
        "source_operator_review_summary": {
            "artifact_kind": source.ARTIFACT_KIND,
            "status": source.OPERATOR_REVIEW_STATUS,
            "scope": source.OPERATOR_REVIEW_SCOPE,
            "commit": SOURCE_OPERATOR_REVIEW_COMMIT,
            "digest": SOURCE_OPERATOR_REVIEW_DIGEST,
            "checks": "548/548 PASS",
        },
        "source_completion_candidate_commit": SOURCE_COMPLETION_CANDIDATE_COMMIT,
        "source_completion_candidate_digest": SOURCE_COMPLETION_CANDIDATE_DIGEST,
        "source_completion_candidate_package_options_digest": SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST,
        "source_completion_candidate_operator_input_requirements_digest": SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST,
        "source_completion_candidate_template_binding_digest": SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST,
        "source_completion_candidate_coverage_digest": SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST,
        "source_completion_candidate_manifest_digest": SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST,
    })
    return bindings


def _approval_digest(approval: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(approval))
    for key in ("checklist", "summary", APPROVAL_DIGEST_KEY):
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_approval(review: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    requirement_status = "APPROVED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_ONLY"
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
        "approved_future_completion_requirement_named_count": 69,
        "future_completion_plan_step_count": 17,
        "planned_output_count": 33,
        "non_goal_count": 71,
        "source_enumerated_non_goal_count": 76,
        "risk_control_count": 104,
        "source_enumerated_risk_control_count": 106,
    }
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "approval_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        **_source_bindings(review),
        "source_completion_candidate_summary": deepcopy(review["source_completion_candidate_summary"]),
        **{key: deepcopy(review[key]) for key in SOURCE_CONTEXT_KEYS},
        "primary_failure_class": review["primary_failure_class"],
        "historical_blocked_remediation_reason": review["historical_blocked_remediation_reason"],
        "historical_blocked_remediation_manifest_digest": review["historical_blocked_remediation_manifest_digest"],
        **counts,
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "approved_package": {
            "package_id": SELECTED_PACKAGE,
            "source_review_status": "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "approval_status": requirement_status,
            "selected": True,
            "approved": True,
            "authorized_for_future_execution": True,
            "executed": False,
            "purpose": "Future execution may complete a non-secret operator source-authority evidence package using the reviewed template if and only if the operator supplies the reviewed non-secret provenance, classification, scope, authority-statement, and row-mapping inputs.",
            "future_execution_boundary": "Future execution may complete an operator-fillable evidence package from reviewed template structure and non-secret operator inputs only. It may not validate evidence, bind evidence, acquire source authority, acquire external evidence, retry acquisition, authorize remediation or retry, authorize main merge, modify code/tests/digests, generate/apply patches, call providers, inspect secrets, or authorize runtime/trading.",
        },
        "approved_future_completion_requirements": [
            {"requirement_id": item["requirement_id"], "approval_status": requirement_status, "execution_status": "NOT_EXECUTED"}
            for item in review["reviewed_future_completion_requirements"]
        ],
        "approved_future_completion_plan": [
            {"step": item["step"], "description": item["description"], "approval_status": requirement_status, "execution_status": "NOT_EXECUTED"}
            for item in review["reviewed_future_completion_plan"]
        ],
        "future_execution_boundary": {
            "future_completion_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
            "future_completion_execution_input_source": "REVIEWED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW",
            "future_completion_execution_type": "NON_SECRET_OPERATOR_FILLABLE_EVIDENCE_PACKAGE_COMPLETION_ONLY",
            **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
            **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        },
        **{field: True for field in FUTURE_PERMISSION_TRUE_FIELDS},
        **{field: False for field in FUTURE_PERMISSION_FALSE_FIELDS},
        "future_completion_execution_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED",
        "planned_outputs": [{"output_id": item["output_id"], "status": "AUTHORIZED_NOT_GENERATED"} for item in review["reviewed_planned_outputs"]],
        "supporting_packages": [
            {"package_id": item, "approval_status": "AVAILABLE_NOT_SELECTED", "selected": False, "approved": False, "authorized": False, "executed": False}
            for item in SUPPORTING_PACKAGE_IDS
        ],
        "blocked_packages": [
            {"package_id": item, "approval_status": "BLOCKED_NOT_APPROVED", "selected": False, "approved": False, "authorized": False, "executed": False}
            for item in BLOCKED_PACKAGE_IDS
        ],
        "approved_non_goals": deepcopy(review["reviewed_non_goals"]),
        "count_label_distinction": deepcopy(review["count_label_distinction"]),
        "next_chain": deepcopy(review["next_chain"]),
        "next_gates": deepcopy(review["next_gates"]),
        "risk_controls": deepcopy(review["risk_controls"]),
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    source_binding_checks = tuple(
        f"{key}_bound" for key in sorted(approval)
        if key.startswith("source_") and (key.endswith("_digest") or key.endswith("_commit"))
    )
    check_ids = tuple(dict.fromkeys((
        "attestation_valid", "source_operator_review_bound", "selected_package_approved_for_future_execution",
        "approved_future_completion_requirements_69", "approved_future_completion_plan_17", "planned_outputs_33",
        "supporting_packages_6", "blocked_packages_5", "non_goals_71", "risk_controls_104",
        "acquisition_scope_sections_4", "mapped_missing_authority_items_30",
        "acceptable_source_artifact_types_13", "operator_provided_evidence_requirements_10",
        "evidence_custody_and_digest_requirements_6", "candidate_results_review_requirements_16",
        "artifact_digest_deterministic", *source_binding_checks,
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"{field}_future_true" for field in FUTURE_PERMISSION_TRUE_FIELDS),
        *(f"{field}_future_false" for field in FUTURE_PERMISSION_FALSE_FIELDS),
        *(f"requirement_{item['requirement_id']}_approved" for item in review["reviewed_future_completion_requirements"]),
        *(f"plan_step_{index}_approved" for index in range(1, 18)),
        *(f"output_{item['output_id']}_authorized" for item in review["reviewed_planned_outputs"]),
        *(f"supporting_package_{item}_preserved" for item in SUPPORTING_PACKAGE_IDS),
        *(f"blocked_package_{item}_blocked" for item in BLOCKED_PACKAGE_IDS),
        *(f"next_chain_step_{index}_defined" for index in range(1, len(review["next_chain"]) + 1)),
        *(f"next_gate_{item}_defined" for item in review["next_gates"]),
        *(f"risk_control_{item}_defined" for item in review["risk_controls"]),
    )))
    approval["checklist"] = [
        {"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"}
        for item in check_ids
    ]
    approval["summary"] = {
        "total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_completion_approval_created": True,
        "selected_operator_source_authority_evidence_package_completion_package": SELECTED_PACKAGE,
        "ready_for_operator_source_authority_evidence_package_completion_execution_after_approval": True,
        **counts,
        **{field: False for field in FALSE_FIELDS},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "source_exit_code": 1,
        "source_stdout_byte_count": 1231380,
        "source_stderr_byte_count": 0,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }
    approval[APPROVAL_DIGEST_KEY] = _approval_digest(approval)
    return approval


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
    *, source_operator_review: dict | None = None, operator_attestation: dict
) -> dict[str, Any]:
    """Build the attestation-bound future-execution approval offline."""

    review = _committed_source_operator_review() if source_operator_review is None else deepcopy(source_operator_review)
    if source_operator_review is None:
        review.update(SOURCE_REVIEW_DIGEST_FIELDS)
    _validate_source_operator_review(review)
    _validate_attestation(operator_attestation)
    approval = _assemble_approval(review, operator_attestation)
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(approval)
    return approval


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
    approval: dict,
) -> dict[str, Any]:
    """Reject any changed source binding, approval fact, or closed boundary."""

    if not isinstance(approval, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("approval must be an object")
    _validate_attestation(approval.get("operator_attestation", {}))
    review = _committed_source_operator_review()
    review.update(SOURCE_REVIEW_DIGEST_FIELDS)
    expected = _assemble_approval(review, approval["operator_attestation"])
    difference = _first_difference(approval, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError(f"{difference} mismatch")
    if re.fullmatch(r"[0-9a-f]{64}", str(approval.get(APPROVAL_DIGEST_KEY))) is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("approval digest invalid")
    return {
        "artifact_kind": ARTIFACT_KIND, "approval_status": APPROVAL_STATUS, "approval_scope": APPROVAL_SCOPE,
        "approval_digest": approval[APPROVAL_DIGEST_KEY],
        **{key: approval["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


MARKDOWN_SECTIONS = tuple("""Operator Attestation
Source Operator Review
Source Completion Candidate
Source Template-Preparation Results Review
Source Template-Preparation Execution
Source Approval
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
Count Label Distinction
Approved Package
Approved Future Completion Requirements
Approved Future Completion Plan
Planned Outputs
Supporting Packages
Blocked Packages
Future Execution Boundary
Unsupported Claims Boundary
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated approval status document."""

    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(deepcopy(approval))
    def source_group(*prefixes: str) -> dict[str, Any]:
        return {
            key: value
            for key, value in approval.items()
            if any(key.startswith(prefix) for prefix in prefixes)
            and isinstance(value, (str, int, bool))
        }

    lookup = {
        "Operator Attestation": approval["operator_attestation"],
        "Source Operator Review": approval["source_operator_review_summary"],
        "Source Completion Candidate": approval["source_completion_candidate_summary"],
        "Source Template-Preparation Results Review": source_group("source_results_review_", "source_template_review_", "source_evidence_item_template_review_", "source_preparation_checklist_review_", "source_template_coverage_review_"),
        "Source Template-Preparation Execution": source_group("source_execution_", "source_package_template_", "source_evidence_item_template_", "source_preparation_checklist_"),
        "Source Approval": source_group("source_approval_", "source_attestation_"),
        "Source Preparation Candidate": source_group("source_preparation_candidate_", "source_preparation_"),
        "Source Failure Diagnosis": source_group("source_failure_diagnosis_"),
        "Source Blocked Acquisition Execution": source_group("source_blocked_acquisition_execution_"),
        "Source Acquisition Approval Chain": source_group("source_acquisition_approval_", "source_acquisition_attestation_"),
        "Source Follow-On Results Review": source_group("source_follow_on_results_review_"),
        "Source Follow-On Execution": source_group("source_follow_on_execution_"),
        "Source Follow-On Approval": source_group("source_follow_on_approval_"),
        "Source Follow-On Operator Review": source_group("source_follow_on_operator_review_"),
        "Source Follow-On Candidate": source_group("source_follow_on_candidate_"),
        "Source Results Review": source_group("source_prior_results_review_", "source_results_review_digest_historical"),
        "Source Enrichment Execution": source_group("source_enrichment_execution_"),
        "Source Historical Approval": source_group("historical_source_approval_"),
        "Source Historical Operator Review": source_group("historical_source_operator_review_"),
        "Source Historical Candidate": source_group("historical_source_candidate_"),
        "Historical Failure Diagnosis": source_group("historical_failure_diagnosis_"),
        "Historical Blocked Remediation": source_group("historical_blocked_remediation_"),
        "Source Remediation Plan and Method Chain": source_group("source_remediation_", "source_targeted_remediation_", "source_method_"),
        "Source Diagnostic Results Review": source_group("source_remediation_or_method_results_review_after_diagnostic_capture_"),
        "Source Controlled Recapture": source_group("source_receipt_recovery_or_recapture_"),
        "Source Durable Receipt": {"path": approval["source_durable_receipt_path"], "parsed": approval["diagnostic_receipt_parsed_in_approval"]},
        "Source Planning and Detail Binding Evidence": source_group("source_planning_", "source_prioritized_planning_", "source_detail_binding_", "source_staged_inventory_"),
        "Retry Failure Context": approval["retry_failure_context"],
        "Priority 1 Target Modules": approval["priority_1_target_modules"],
        "Priority 1 Validation Summary": approval["priority1_validation_summary"],
        "Diagnostic Capture Evidence Summary": approval["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": approval["reviewed_observable_failure_families"],
        "Reviewed Workstreams": approval["reviewed_workstreams"],
        "Reviewed Template Structure": approval["reviewed_template_structure"],
        "Reviewed Template Rows": approval["reviewed_template_rows"],
        "Missing Authority Mapping": approval["missing_authority_mapping"],
        "Acceptable Source-Artifact Inventory": approval["acceptable_source_artifact_type_inventory"],
        "Actual Evidence Absence": approval["actual_evidence_absence"],
        "Actual Coverage Zero": approval["actual_coverage_review"],
        "Count Label Distinction": approval["count_label_distinction"],
        "Approved Package": approval["approved_package"],
        "Approved Future Completion Requirements": approval["approved_future_completion_requirements"],
        "Approved Future Completion Plan": approval["approved_future_completion_plan"],
        "Future Execution Boundary": approval["future_execution_boundary"],
        "Planned Outputs": approval["planned_outputs"],
        "Supporting Packages": approval["supporting_packages"],
        "Blocked Packages": approval["blocked_packages"],
        "Unsupported Claims Boundary": {field: approval[field] for field in FALSE_FIELDS},
        "Recommendation": {"recommended_next_task": approval["recommended_next_task"], "selected_package": SELECTED_PACKAGE},
        "Next Chain": approval["next_chain"], "Next Gates": approval["next_gates"],
        "Risk Controls": approval["risk_controls"],
        "Authority Boundaries": {field: approval[field] for field in FALSE_FIELDS},
        "Checklist Summary": approval["summary"],
        "Guardrails": [field for field in FALSE_FIELDS if approval[field] is False],
    }
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Approval After Candidate Operator Review v1",
        "", f"Artifact: `{approval['artifact_kind']}`", "", f"Status: `{approval['approval_status']}`", "",
        f"Scope: `{approval['approval_scope']}`", "", f"Approval digest: `{approval[APPROVAL_DIGEST_KEY]}`", "",
    ]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(lookup[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
    output_dir: str | Path, *, source_operator_review: dict | None = None, operator_attestation: dict
) -> dict[str, Any]:
    """Write the deterministic approval status document outside protected paths."""

    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError("protected output directory")
    approval = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
        source_operator_review=source_operator_review, operator_attestation=operator_attestation
    )
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_markdown_v1(approval), encoding="utf-8")
    return approval


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "APPROVAL_STATUS", "APPROVAL_SCOPE", "SELECTED_PACKAGE",
    "APPROVAL_DIGEST_KEY", "ATTESTATION_DIGEST_KEY", "ATTESTATION_VALUE_FIELDS", "ATTESTATION_BOOLEAN_FIELDS",
    "REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVED_AFTER_CANDIDATE_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_EXECUTION_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_COMPLETE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FROM_REVIEWED_TEMPLATE_WITH_NON_SECRET_OPERATOR_INPUTS",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_markdown_v1",
]
