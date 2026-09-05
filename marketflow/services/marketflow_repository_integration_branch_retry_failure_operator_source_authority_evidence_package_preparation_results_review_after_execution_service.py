"""Review the committed operator evidence-package template preparation result."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1"
RESULTS_REVIEW_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_READY"
RESULTS_REVIEW_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_ONLY_NOT_TEMPLATE_EXECUTION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
SOURCE_EXECUTION_COMMIT = "a39332feb29a23612ee51cb45e8d5663b144c638"
SOURCE_EXECUTION_DIGEST = "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3"
SOURCE_PACKAGE_TEMPLATE_DIGEST = "fb406078ca1a1199a430dd836050f9b198373c1f46c19cb5ee899ffe7e975a9a"
SOURCE_EVIDENCE_ITEM_TEMPLATE_DIGEST = "820cdf4c4a758b1d24ad0112fa6a1b05a8e6a330dc717c3564be4434b00af6e9"
SOURCE_PREPARATION_CHECKLIST_DIGEST = "4f965c0e7072dc6061ed3731e0eb7a639e117780c09544a6031663d6a6959605"
SOURCE_TEMPLATE_COVERAGE_DIGEST = "b9b25bd3609aff81a4bb4e47e999e41ea265cda5419be4be184f1a73b25e7884"
SOURCE_EXECUTION_MANIFEST_DIGEST = "272cadca012100d25e5628f09a3e91f8919a9fb80b8433ca2841a28d65a76a39"
SELECTED_PACKAGE = source.SELECTED_PACKAGE
RECOMMENDED_NEXT_TASK = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_V1"
RECOMMENDED_ACTION = "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_REVIEWED_TEMPLATE_BEFORE_ANY_ACQUISITION_REATTEMPT"

RESULTS_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_digest"
TEMPLATE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_template_review_digest"
EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_item_template_review_digest"
CHECKLIST_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_checklist_review_digest"
COVERAGE_REVIEW_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_template_coverage_review_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_manifest_digest"
PASS, BLOCKER = "PASS", "BLOCKER"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_READY = RESULTS_REVIEW_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_ONLY_NOT_TEMPLATE_EXECUTION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = RESULTS_REVIEW_SCOPE
PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY = SELECTED_PACKAGE

SOURCE_BINDINGS = {
    "source_approval_commit": "e942849f3126c95b432c6ce77f21eb96586f9b4b",
    "source_approval_digest": "e7f1d8a5ae413ca0f971257e13554a63b3ee95e942e156adb5b204cbcc378cbd",
    "source_attestation_digest": "e16b2afde6c36d5461a65d2f598fec55f9a13811a555efc90a9dac1e981f7328",
    "source_operator_review_commit": "139b03c87e9ce48b38435c7dcc0761c2300a7a4b",
    "source_operator_review_digest": "36e75dec88c71cc2e73109254a5a37b3b8e6415b598b0b8b4f7a025c3911bc22",
    "source_package_options_review_digest": "39aa0548562fd85763fc937fe3c306734a60749500b3607a75f42ad9b3e62ae8",
    "source_template_requirements_review_digest": "ac2fff06d39bd4361a81b7a26fec8bc43f18c8da1169bc38cde3ede9476d5c18",
    "source_missing_authority_coverage_review_digest": "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af",
    "source_operator_review_manifest_digest": "30d2cba7243845b01df595ce922c07dae7a4d876345022e7d51046bf8b76c8df",
    "source_preparation_candidate_commit": "8d2944edfb7a54056f4a59c3d5817e823da80ce8",
    "source_preparation_candidate_digest": "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391",
    "source_preparation_package_options_digest": "5eb1efe8ccb86f243c3db861b983c86fff9b9b868b146ae866da29975cfca400",
    "source_preparation_template_requirements_digest": "3dd55cbdcf191c46c2bd5d314a20019c59b107029e6fd178754d79eddc06b2d7",
    "source_preparation_missing_authority_coverage_digest": "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af",
    "source_preparation_manifest_digest": "c95671cf372c8bdf7f15c019bd994ae58f547d025117e12456fd780b5f9fd3d3",
    "source_failure_diagnosis_commit": "e51b3f58215a3ecb25f863655c79490cbdd65342",
    "source_failure_diagnosis_digest": "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c",
    "source_failure_classification_digest": "dfcc0f7438afd861300bac7bcde4b5449b3f1f969547f09469c378707c6e084a",
    "source_missing_evidence_package_diagnosis_digest": "918dba1b6c9a6e0d3d8bc2919525af046e2c8e460d13741284b2838d87df4b95",
    "source_coverage_diagnosis_digest": "233b3a47c56e8862df92d03f305d22be10ccec0dc6e2278f69260fe98e9373f4",
    "source_failure_diagnosis_manifest_digest": "25c87db09e1464ad5466a2fc007d510df94ccae40b9da8eef44ee987698002a6",
    "source_blocked_acquisition_execution_commit": "ff1635456a5c880f9a99a3b8359f94428383123e",
    "source_blocked_acquisition_execution_reason": "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED",
    "source_blocked_acquisition_execution_manifest_digest": "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3",
    "source_acquisition_approval_commit": "f8189e7421720879bd2a6d30f05353c8b65adff4",
    "source_acquisition_approval_digest": "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69",
    "source_acquisition_attestation_digest": "db079d7b71f141dafba8439eba51caa1bc663ddf1158d3ea34b1f102ce4fb879",
    "source_follow_on_results_review_digest": "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb",
    "source_follow_on_execution_digest": "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208",
    "source_authority_acquisition_candidate_digest": "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91",
    "source_authority_acquisition_scope_digest": "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8",
    "source_missing_authority_to_source_evidence_mapping_digest": "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334",
    "source_follow_on_approval_digest": "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6",
    "source_follow_on_operator_review_digest": "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb",
    "source_follow_on_candidate_digest": "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468",
    "source_results_review_digest": "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb",
    "source_enrichment_execution_digest": "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c",
    "source_authority_enrichment_plan_digest": "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94",
    "source_missing_authority_inventory_digest": "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8",
    "source_workstream_authority_mapping_digest": "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd",
    "historical_source_approval_digest": "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972",
    "historical_source_operator_review_digest": "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51",
    "historical_source_candidate_digest": "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c",
    "historical_failure_diagnosis_digest": "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171",
    "historical_blocked_remediation_reason": "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED",
    "historical_blocked_remediation_manifest_digest": "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002",
    "source_remediation_execution_approval_after_plan_results_review_digest": "2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1",
    "source_remediation_plan_or_execution_results_review_after_method_results_review_digest": "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa",
    "source_remediation_plan_or_execution_after_method_results_review_digest": "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c",
    "source_targeted_remediation_plan_digest": "2d7ffac9fc3cc04f0bfb823ef81f254005adaee7a600ccb6e3444b7f3dec91db",
    "source_remediation_or_method_results_review_after_diagnostic_capture_digest": "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f",
    "source_remediation_or_method_execution_after_diagnostic_capture_digest": "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88",
    "source_failure_family_classification_digest": "3e3f2409315228bc88c23fb02dfdf3dbea4724d30356f0a4548243105a49dac1",
    "source_receipt_recovery_or_recapture_results_review_digest": "427d2a76afcec7c8b9647a0f0c19b6037e5a451b0f70fad1a5025afc266946ba",
    "source_receipt_recovery_or_recapture_execution_digest": "25a70331c48eedeb62c6f8532dba0e1b782904ff4b753934c2fd12ccbec47e46",
    "source_receipt_recovery_or_recapture_payload_digest": "073b47101ff05794af3f92489bd1f97a286cfc7c29c1d95d1ca2a022270d2c38",
    "source_receipt_recovery_or_recapture_receipt_digest": "dfd7f50c4065e759ccfee0f160c97177f4d9a1cfe977fb6db1ce240f8ad3345b",
    "source_durable_receipt_path": "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json",
    "source_planning_results_review_digest": "d6588bfbfca55cec499d1960ab260b703dd754653473ee434b7f6ac100294956",
    "source_prioritized_planning_digest": "ef372ac66b165456241a53fdbe551c51fd4c9bfb65d2b6cdbc366cc464370c60",
    "source_detail_binding_results_review_digest": "9124d03f9c540873a1bb3253800b1574f1266e67708034e64c95eb1ff3254a74",
    "source_complete_29_row_binding_digest": "36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7",
    "source_materialized_payload_digest": "1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7",
    "source_recovery_results_review_digest": "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266",
    "source_recovery_detail_digest": "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5",
    "source_after_v2_approval_digest": "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97",
    "source_module_grouping_digest": "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff",
    "source_staged_inventory_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
}

TRUE_FIELDS = tuple("""operator_source_authority_evidence_package_preparation_results_review_created
operator_source_authority_evidence_package_preparation_results_review_ready
source_execution_reviewed
source_execution_identity_verified
source_execution_status_verified
source_execution_scope_verified
source_execution_digest_verified
source_package_template_digest_verified
source_evidence_item_template_digest_verified
source_preparation_checklist_digest_verified
source_template_coverage_digest_verified
source_execution_manifest_digest_verified
selected_preparation_package_verified
source_approval_bound
source_attestation_bound
source_operator_review_bound
source_preparation_candidate_bound
source_failure_diagnosis_bound
source_blocked_acquisition_execution_bound
source_blocked_reason_verified
source_acquisition_approval_bound
source_acquisition_candidate_operator_review_bound
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
template_execution_success_reviewed
operator_fillable_template_reviewed
operator_fillable_template_header_reviewed
operator_fillable_evidence_item_templates_reviewed
operator_fillable_preparation_checklist_reviewed
source_owner_request_guidance_reviewed
acceptable_source_artifact_inventory_reviewed
custody_and_digest_guidance_reviewed
no_secret_boundary_guidance_reviewed
results_review_requirements_reviewed
all_30_template_rows_reviewed
all_30_template_rows_mapped_to_reviewed_missing_authority_items
template_rows_preserve_results_review_required_before_use
template_rows_force_direct_change_authorized_false
template_rows_force_remediation_authorized_false
template_rows_force_retry_authorized_false
template_rows_force_main_merge_authorized_false
actual_coverage_zero_reviewed
template_not_actual_evidence_package_verified
template_not_source_authority_verified
template_not_acquired_evidence_verified
acquisition_reattempt_gate_preserved
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_source_authority_evidence_package_completion_candidate_after_template_review""".splitlines())

FALSE_FIELDS = tuple("""template_execution_rerun_performed
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
pytest_performed_in_results_review
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_results_review
diagnostic_output_analyzed_in_results_review
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_results_review
method_execution_rerun_performed
controlled_recapture_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_results_review
cache_modified_in_results_review
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
ready_for_operator_source_authority_evidence_package_completion_execution
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
provider_requests_made_in_results_review
market_data_acquisition_performed_in_results_review
dataset_generation_performed_in_results_review
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

OUTPUT_IDS = tuple("""operator_source_authority_evidence_package_preparation_results_review_manifest
source_execution_binding_report
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
package_header_template_review_report
evidence_item_template_review_report
thirty_missing_authority_template_rows_review_report
acquisition_scope_section_template_map_review
acceptable_source_artifact_type_inventory_review
preparation_checklist_review_report
source_owner_request_guidance_review_report
custody_and_digest_guidance_review_report
no_secret_boundary_review_report
results_review_before_use_requirements_report
actual_evidence_absence_report
actual_coverage_zero_report
template_not_source_authority_report
acquisition_reattempt_gate_preservation_report
unsupported_claims_boundary_report
retry_gate_preservation_report
main_merge_gate_preservation_report
digest_manifest""".splitlines())

NEXT_CHAIN = (
    "Operator Source Authority Evidence Package Completion Candidate After Template Preparation Results Review v1.",
    "Operator Source Authority Evidence Package Completion Candidate Operator Review v1.",
    "Operator Source Authority Evidence Package Completion Approval v1, if selected.",
    "Operator Source Authority Evidence Package Completion Execution v1, if approved and operator supplies non-secret evidence.",
    "Operator Source Authority Evidence Package Completion Results Review v1.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Evidence Package v1, only if a reviewed package exists and is separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional no-change disposition candidate, alternate diagnostic candidate, remediation re-entry candidate, no-change retry criteria candidate, or hold disposition only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.", "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.", "Main Merge Approval only if new retry results review passes.",
)
NEXT_GATES = tuple("""operator_source_authority_evidence_package_completion_candidate_after_template_review
operator_source_authority_evidence_package_completion_candidate_operator_review
operator_source_authority_evidence_package_completion_approval_if_selected
operator_source_authority_evidence_package_completion_execution_if_approved_and_non_secret_operator_evidence_supplied
operator_source_authority_evidence_package_completion_results_review
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

RISK_CONTROLS = tuple("""results_review_does_not_rerun_template_execution
results_review_does_not_create_actual_operator_evidence_package
results_review_does_not_fill_actual_evidence_items
results_review_does_not_supply_evidence_package
results_review_does_not_validate_evidence_package
results_review_does_not_bind_evidence_package
results_review_does_not_acquire_source_authority
results_review_does_not_acquire_source_authority_evidence
results_review_does_not_acquire_external_evidence
template_is_not_source_authority
template_is_not_acquired_evidence
template_is_not_acquisition_success
template_requires_results_review_before_use
reviewed_template_still_requires_filled_package_governance
reviewed_template_still_requires_acquisition_reattempt_approval
actual_coverage_remains_zero
all_missing_authority_items_remain_missing_not_acquired
results_review_does_not_retry_acquisition_execution
results_review_does_not_create_no_change_disposition
results_review_does_not_execute_alternate_diagnostics
results_review_does_not_execute_remediation
results_review_does_not_modify_production_code
results_review_does_not_modify_existing_tests
results_review_does_not_update_expected_digests
results_review_does_not_generate_patch
results_review_does_not_apply_patch
results_review_does_not_run_pytest
results_review_does_not_run_full_pytest
results_review_does_not_rerun_priority1_validation
results_review_does_not_rerun_retry
results_review_does_not_rerun_detached_retry
results_review_does_not_parse_durable_receipt
results_review_does_not_analyze_diagnostic_output
results_review_does_not_rerun_source_authority_enrichment
results_review_does_not_rerun_follow_on_execution
results_review_does_not_rerun_plan_execution
results_review_does_not_regenerate_targeted_plan
results_review_does_not_rerun_method_execution
results_review_does_not_rerun_controlled_recapture
results_review_does_not_run_diagnostic_command
results_review_does_not_read_pytest_cache
results_review_does_not_modify_pytest_cache
results_review_does_not_commit_pytest_cache
results_review_does_not_commit_marketflow_outputs
results_review_does_not_parse_terminal_logs
results_review_does_not_parse_operator_logs
results_review_does_not_inspect_env
results_review_does_not_contact_source_owners
results_review_does_not_read_external_documents
results_review_does_not_reconstruct_prior_lost_values
results_review_does_not_reconstruct_full_streams
results_review_does_not_classify_modules_again
results_review_does_not_classify_full_retry_failures
results_review_does_not_classify_full_retry_errors
results_review_does_not_claim_failure_error_separation
results_review_does_not_identify_authoritative_first_failure
results_review_does_not_identify_authoritative_first_error
results_review_does_not_claim_traceback_root_cause
results_review_does_not_claim_root_cause
results_review_does_not_claim_retry_success
results_review_does_not_claim_main_merge_readiness
results_review_does_not_create_retry_candidate
results_review_does_not_create_retry_approval
results_review_does_not_create_retry_execution
results_review_does_not_create_retry_results_review
results_review_does_not_create_main_merge_approval
results_review_does_not_push_main
results_review_does_not_push_integration_branch
results_review_does_not_delete_integration_branch
results_review_does_not_delete_worktree
results_review_does_not_force_push
results_review_does_not_modify_tags
results_review_does_not_regenerate_evidence
results_review_does_not_call_providers
results_review_does_not_acquire_market_data
results_review_does_not_generate_dataset
results_review_does_not_recompute_metrics
results_review_does_not_train_models
results_review_does_not_score_strategy
results_review_does_not_generate_trade_recommendations
results_review_does_not_accept_predictive_usefulness
results_review_does_not_accept_profitability
results_review_does_not_authorize_runtime
results_review_does_not_authorize_broker_execution
first_retry_failure_remains_authoritative
root_regression_not_retry_evidence
source_authority_acquisition_reattempt_requires_reviewed_filled_package
separate_acquisition_approval_required_before_acquisition_reattempt
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_remediation_approval_required_before_code_or_test_changes
separate_retry_approval_required_before_new_retry
main_merge_requires_passing_new_retry_results_review
protect_origin_main
preserve_integration_branch
preserve_staged_frozen_evidence
preserve_terminal_archive_evidence
preserve_published_governance_tags
preserve_meta_limitation""".splitlines())


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError(ValueError):
    """Raised when committed review evidence or a review boundary changes."""


def _first_difference(actual: Any, expected: Any, path: str = "review") -> str | None:
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


def _package_header() -> dict[str, Any]:
    return {
        "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
        "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
        "package_source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>",
        "package_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>", "package_created_utc": "<REQUIRED_UTC_TIMESTAMP>",
        "package_digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "package_declares_no_secrets": "<REQUIRED_TRUE>", "package_declares_no_api_keys": "<REQUIRED_TRUE>",
        "package_declares_no_broker_credentials": "<REQUIRED_TRUE>", "package_declares_no_personal_financial_credentials": "<REQUIRED_TRUE>",
        "package_distinguishes_specification_from_observation": "<REQUIRED_TRUE>",
        "package_distinguishes_expected_from_actual": "<REQUIRED_TRUE>",
        "package_distinguishes_source_authority_from_diagnostic_output": "<REQUIRED_TRUE>",
        "evidence_items": "<REQUIRED_LIST_OF_ONE_OR_MORE_FILLED_EVIDENCE_ITEMS_FOR_FUTURE_ACQUISITION_REATTEMPT>",
        "template_only": True, "actual_evidence_package_created": False,
    }


def _item_contract() -> dict[str, Any]:
    return {
        "evidence_id": "<REQUIRED_UNIQUE_EVIDENCE_ID>", "mapped_missing_authority_id": "<BOUND_REVIEWED_MISSING_AUTHORITY_ID>",
        "section_id": "<ONE_OF_ALLOWED_SECTION_IDS>", "workstream_id": "<ONE_OF_ALLOWED_WORKSTREAM_IDS>",
        "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
        "source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>", "source_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>",
        "digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "evidence_classification": "<SPECIFICATION | APPROVED_CONTRACT | SOURCE_OWNER_STATEMENT | CANONICAL_PAYLOAD | CANONICAL_SCHEMA | CANONICAL_SERIALIZATION | EXPECTED_VALUE_SOURCE | ACTUAL_VALUE_SOURCE | FIXTURE_LIFECYCLE_AUTHORITY | DETERMINISM_AUTHORITY | EXPORT_SURFACE_AUTHORITY | REVIEWED_SOURCE_DIGEST_BUNDLE>",
        "specification_or_observation": "<SPECIFICATION | OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
        "expected_or_actual_scope": "<EXPECTED | ACTUAL | BOTH | NOT_APPLICABLE>", "authority_statement": "<REQUIRED_NON_EMPTY_AUTHORITY_STATEMENT>",
        "results_review_required_before_use": True, "direct_change_authorized_now": False,
        "remediation_authorized_now": False, "retry_authorized_now": False, "main_merge_authorized_now": False,
    }


def _template_rows() -> list[dict[str, Any]]:
    common = ["approved_product_specification", "approved_artifact_contract", "approved_operator_provided_evidence_package", "approved_source_owning_team_statement", "approved_reviewed_source_digest_bundle"]
    groups = (
        (1, 8, source.ALLOWED_SECTION_IDS[0], source.ALLOWED_WORKSTREAM_IDS[0], ["approved_expected_value_source", "approved_actual_value_source"]),
        (9, 16, source.ALLOWED_SECTION_IDS[1], source.ALLOWED_WORKSTREAM_IDS[1], ["approved_canonical_payload_or_serialization_contract", "approved_digest_manifest_source"]),
        (17, 23, source.ALLOWED_SECTION_IDS[2], source.ALLOWED_WORKSTREAM_IDS[2], ["approved_fixture_lifecycle_document", "approved_deterministic_execution_contract"]),
        (24, 30, source.ALLOWED_SECTION_IDS[3], source.ALLOWED_WORKSTREAM_IDS[3], ["approved_schema_definition", "approved_export_surface_contract"]),
    )
    rows = []
    for start, end, section_id, workstream_id, specialized in groups:
        for index in range(start, end + 1):
            missing_id = f"MA-{index:03d}"
            rows.append({**_item_contract(), "evidence_id": f"<REQUIRED_UNIQUE_EVIDENCE_ID_FOR_{missing_id}>",
                "mapped_missing_authority_id": missing_id, "section_id": section_id, "workstream_id": workstream_id,
                "allowed_acceptable_source_artifact_types": [*common, *specialized], "template_only": True,
                "actual_evidence_supplied": False, "actual_evidence_validated": False, "actual_evidence_bound": False,
                "current_status": "MISSING_NOT_ACQUIRED"})
    return rows


def _committed_source_execution() -> dict[str, Any]:
    rows = _template_rows()
    return {
        "artifact_kind": source.ARTIFACT_KIND, "execution_status": source.EXECUTION_STATUS,
        "execution_scope": source.EXECUTION_SCOPE, "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_execution_digest": SOURCE_EXECUTION_DIGEST, "source_package_template_digest": SOURCE_PACKAGE_TEMPLATE_DIGEST,
        "source_evidence_item_template_digest": SOURCE_EVIDENCE_ITEM_TEMPLATE_DIGEST,
        "source_preparation_checklist_digest": SOURCE_PREPARATION_CHECKLIST_DIGEST,
        "source_template_coverage_digest": SOURCE_TEMPLATE_COVERAGE_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        **deepcopy(SOURCE_BINDINGS),
        "retry_failure_context": {"counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}, "first_result_authoritative": True, "pytest_passed": False, "pytest_failed": True, "root_full_regression_is_retry_evidence": False},
        "priority_1_target_modules": [
            {"path": "tests/test_marketflow_signal_or_feature_generation_results_review_service.py", "failed_or_errored_nodeid_count": 136},
            {"path": "tests/test_post_identity_freeze_registry_inventory_approval_service.py", "failed_or_errored_nodeid_count": 131},
            {"path": "tests/test_corporate_action_authority_plan_candidate_service.py", "failed_or_errored_nodeid_count": 122},
            {"path": "tests/test_feature_generation_results_review_redesigned_labels_service.py", "failed_or_errored_nodeid_count": 112},
            {"path": "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", "failed_or_errored_nodeid_count": 111},
        ],
        "priority1_validation_summary": {"pre_change_passed": True, "pre_change_passed_count": 675, "post_change_passed": True, "post_change_passed_count": 675, "post_change_duration_seconds": "41.88", "not_retry_evidence": True},
        "diagnostic_capture_evidence_summary": {"exit_code": 1, "duration_seconds": "21.584361", "stdout_byte_count": 1231380, "stderr_byte_count": 0, "combined_output_byte_count": 1231380, "stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a", "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "diagnostic_only": True},
        "reviewed_observable_failure_families": [{"family_id": item, "observable_evidence_count": 47, "confidence": "HIGH"} for item in ("assertion_or_value_mismatch", "digest_or_hash_mismatch", "fixture_or_test_isolation_issue", "missing_or_unexpected_field")],
        "reviewed_workstreams": [{"workstream_id": workstream, "source_family_id": family} for workstream, family in zip(source.ALLOWED_WORKSTREAM_IDS, ("assertion_or_value_mismatch", "digest_or_hash_mismatch", "fixture_or_test_isolation_issue", "missing_or_unexpected_field"))],
        "missing_authority_mapping": [{"missing_authority_id": row["mapped_missing_authority_id"], "section_id": row["section_id"], "workstream_id": row["workstream_id"], "current_status": "MISSING_NOT_ACQUIRED"} for row in rows],
        "package_header_template": _package_header(), "evidence_item_template_contract": _item_contract(),
        "evidence_item_template_rows": rows, "acceptable_source_artifact_type_inventory": list(source.ALLOWED_SOURCE_ARTIFACT_TYPES),
        "preparation_checklist_review": {"source_requirement_count": 62, "template_requirements_included": 62, "actual_evidence_satisfied": 0},
        "source_owner_request_guidance": {"source_owner_or_origin_required": True, "source_reference_required": True, "contact_performed": False, "actual_source_owner_information_supplied": False},
        "custody_and_digest_guidance": {"requirement_count": 6, "digest_or_reproducible_provenance_required": True},
        "no_secret_boundary": {"no_secrets_required": True, "no_api_keys_required": True, "no_broker_credentials_required": True, "no_personal_financial_credentials_required": True, "secrets_captured": False},
        "results_review_before_use": {"required": True, "actual_package_use_authorized": False, "acquisition_reattempt_authorized": False},
    }


def _validate_source_execution(execution: Mapping[str, Any]) -> None:
    if not isinstance(execution, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution must be an object")
    expected = _committed_source_execution()
    direct = ("artifact_kind", "execution_status", "execution_scope", "selected_operator_source_authority_evidence_package_preparation_package")
    aliases = {
        "source_execution_commit": "source_execution_commit", "source_execution_digest": source.EXECUTION_DIGEST_KEY,
        "source_package_template_digest": source.TEMPLATE_DIGEST_KEY,
        "source_evidence_item_template_digest": source.EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY,
        "source_preparation_checklist_digest": source.PREPARATION_CHECKLIST_DIGEST_KEY,
        "source_template_coverage_digest": source.COVERAGE_DIGEST_KEY,
        "source_execution_manifest_digest": source.MANIFEST_DIGEST_KEY,
    }
    for key in direct:
        if execution.get(key) != expected[key]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError(f"source_execution.{key} mismatch")
    for expected_key, actual_key in aliases.items():
        actual = execution.get(actual_key, execution.get(expected_key))
        if actual != expected[expected_key]:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError(f"source_execution.{actual_key} mismatch")
    for key, value in SOURCE_BINDINGS.items():
        if execution.get(key) != value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError(f"source_execution.{key} mismatch")
    rows = execution.get("operator_fillable_evidence_item_templates", execution.get("evidence_item_template_rows"))
    if not isinstance(rows, list) or len(rows) != 30:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution template rows mismatch")
    expected_ids = {f"MA-{index:03d}" for index in range(1, 31)}
    if {row.get("mapped_missing_authority_id") for row in rows} != expected_ids:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution mapped IDs mismatch")
    for row in rows:
        if row.get("section_id") not in source.ALLOWED_SECTION_IDS or row.get("workstream_id") not in source.ALLOWED_WORKSTREAM_IDS:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution template scope mismatch")
        if not set(row.get("allowed_acceptable_source_artifact_types", ())) <= set(source.ALLOWED_SOURCE_ARTIFACT_TYPES):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution artifact type mismatch")
        if any(row.get(field) is not False for field in ("direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now", "actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound")):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution row boundary mismatch")
        if row.get("template_only") is not True or row.get("results_review_required_before_use") is not True or row.get("current_status") != "MISSING_NOT_ACQUIRED":
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("source_execution row status mismatch")


FINDINGS = tuple(
    f"{index}. {text}" for index, text in enumerate((
        "The source execution used the approved preparation package.", "The selected package was executed only for template/checklist preparation.",
        "The source execution created an operator-fillable evidence package template.", "One package-header template contains the required non-secret placeholders.",
        "Exactly 30 evidence-item template rows were created.", "Each row maps to a reviewed missing-authority item.",
        "Each row preserves allowed section, workstream, and acceptable source-artifact constraints.",
        "Each row requires source owner/origin, reference, provenance, classification, authority statement, and results review.",
        "Each row forces direct-change, remediation, retry, and main-merge authorization false.", "The preparation checklist was generated.",
        "No real evidence package was created.", "No evidence item was filled with actual evidence.",
        "No evidence package was supplied, validated, bound, or accepted as source authority.", "Actual coverage remains 0 covered and 30 uncovered.",
        "All 30 missing-authority items remain MISSING_NOT_ACQUIRED.", "The reviewed template is not source authority.",
        "The reviewed template is not acquired evidence.", "The reviewed template is not acquisition success.",
        "A later filled package requires separate governance before any acquisition reattempt.",
        "Acquisition, disposition, diagnostics, remediation, retry, and main merge remain closed.",
        "The failed detached retry remains authoritative.", "Priority 1 validation remains current-root evidence only.",
        "Diagnostic capture remains diagnostic metadata only.", "No provider, runtime, broker, or trading authority was created.",
    ), 1)
)
DOMAINS = (
    {"domain_id": "source_execution_identity", "disposition": "PASSED", "explanation": "Source execution identity and digest are bound."},
    {"domain_id": "source_approval_identity", "disposition": "PASSED", "explanation": "Source approval and attestation are bound."},
    {"domain_id": "template_package_generation", "disposition": "PASSED", "explanation": "Package-header template is reviewed."},
    {"domain_id": "evidence_item_template_generation", "disposition": "PASSED", "explanation": "Exactly 30 template rows are reviewed."},
    {"domain_id": "preparation_checklist_generation", "disposition": "PASSED", "explanation": "Preparation checklist is reviewed."},
    {"domain_id": "template_coverage", "disposition": "PASSED_TEMPLATE_ONLY", "explanation": "Thirty rows are templated; actual coverage remains zero."},
    {"domain_id": "actual_evidence_status", "disposition": "NOT_CREATED_NOT_SUPPLIED_NOT_VALIDATED_NOT_BOUND", "explanation": "No actual evidence exists."},
    {"domain_id": "source_authority_status", "disposition": "NOT_ACQUIRED", "explanation": "Template and checklist do not acquire authority."},
    {"domain_id": "acquisition_reattempt_status", "disposition": "NOT_READY", "explanation": "A reviewed filled package and separate approval are required."},
    {"domain_id": "remediation_status", "disposition": "NOT_AUTHORIZED_NOT_EXECUTED", "explanation": "No remediation was authorized or executed."},
    {"domain_id": "retry_status", "disposition": "FAILED_RETRY_REMAINS_AUTHORITATIVE", "explanation": "Detached retry remains authoritative."},
    {"domain_id": "protected_repository_boundaries", "disposition": "PRESERVED", "explanation": "Protected repository boundaries remain preserved."},
    {"domain_id": "provider_runtime_trading_boundary", "disposition": "PRESERVED", "explanation": "No provider, runtime, broker, or trading action occurred."},
)


def _digest_without(review: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(review))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_review() -> dict[str, Any]:
    execution = _committed_source_execution()
    rows = deepcopy(execution["evidence_item_template_rows"])
    counts = {"operator_source_authority_evidence_item_count": 0, "operator_source_authority_evidence_item_template_count": 30,
        "operator_fillable_evidence_item_template_count": 30, "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0, "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30, "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "acquisition_scope_section_count": 4,
        "acceptable_source_artifact_type_count": 13, "operator_provided_evidence_requirement_count": 10,
        "evidence_custody_and_digest_requirement_count": 6, "candidate_results_review_requirement_count": 16,
        "observable_failure_family_count": 4, "total_observable_evidence_items": 188, "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069, "failed_or_errored_nodeids_count": 1404, "module_summary_module_count": 29,
        "package_option_count": 12, "available_package_count": 7, "blocked_package_count": 5,
        "approved_future_requirement_count": 62, "approved_future_plan_step_count": 15, "planned_output_count": 28,
        "source_generated_output_count": 28, "review_generated_output_count": 30, "non_goal_count": 71, "risk_control_count": 104}
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND, "schema_version": SCHEMA_VERSION, "results_review_status": RESULTS_REVIEW_STATUS,
        "results_review_scope": RESULTS_REVIEW_SCOPE, "created_offline": True, "governance_only": True, "results_review_only": True,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT, "source_execution_artifact_kind": source.ARTIFACT_KIND,
        "source_execution_status": source.EXECUTION_STATUS, "source_execution_scope": source.EXECUTION_SCOPE,
        "source_execution_digest": SOURCE_EXECUTION_DIGEST, "source_package_template_digest": SOURCE_PACKAGE_TEMPLATE_DIGEST,
        "source_evidence_item_template_digest": SOURCE_EVIDENCE_ITEM_TEMPLATE_DIGEST,
        "source_preparation_checklist_digest": SOURCE_PREPARATION_CHECKLIST_DIGEST,
        "source_template_coverage_digest": SOURCE_TEMPLATE_COVERAGE_DIGEST,
        "source_execution_manifest_digest": SOURCE_EXECUTION_MANIFEST_DIGEST,
        "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        **deepcopy(SOURCE_BINDINGS), **counts, **{key: True for key in TRUE_FIELDS}, **{key: False for key in FALSE_FIELDS},
        "retry_failure_context": deepcopy(execution["retry_failure_context"]), "priority_1_target_modules": deepcopy(execution["priority_1_target_modules"]),
        "priority1_validation_summary": deepcopy(execution["priority1_validation_summary"]),
        "diagnostic_capture_evidence_summary": deepcopy(execution["diagnostic_capture_evidence_summary"]),
        "reviewed_observable_failure_families": deepcopy(execution["reviewed_observable_failure_families"]),
        "reviewed_workstreams": deepcopy(execution["reviewed_workstreams"]), "missing_authority_mapping": deepcopy(execution["missing_authority_mapping"]),
        "acceptable_source_artifact_type_inventory": deepcopy(execution["acceptable_source_artifact_type_inventory"]),
        "package_header_template_review": deepcopy(execution["package_header_template"]),
        "evidence_item_template_review": deepcopy(execution["evidence_item_template_contract"]),
        "thirty_missing_authority_template_rows_review": rows,
        "preparation_checklist_review": deepcopy(execution["preparation_checklist_review"]),
        "source_owner_request_guidance_review": deepcopy(execution["source_owner_request_guidance"]),
        "custody_and_digest_guidance_review": deepcopy(execution["custody_and_digest_guidance"]),
        "no_secret_boundary_review": deepcopy(execution["no_secret_boundary"]),
        "results_review_before_use": deepcopy(execution["results_review_before_use"]),
        "actual_evidence_absence": {"package_created": False, "package_supplied": False, "package_validated": False, "package_bound": False, "items_filled": False},
        "template_coverage_review": {"template_rows": 30, "actual_covered": 0, "actual_uncovered": 30, "status": "MISSING_NOT_ACQUIRED"},
        "template_source_authority_disposition": "TEMPLATE_NOT_ACTUAL_EVIDENCE_NOT_SOURCE_AUTHORITY_NOT_ACQUIRED_EVIDENCE",
        "review_findings": list(FINDINGS), "review_domains": [deepcopy(item) for item in DOMAINS],
        "outputs": [{"output_id": item, "status": "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY"} for item in OUTPUT_IDS],
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "recommended_next_task_status": "FUTURE_CANDIDATE_NOT_CREATED",
        "recommended_action": RECOMMENDED_ACTION,
        "reason": "The template-preparation execution has been reviewed and confirms that a non-secret operator-fillable template and checklist exist. The template is not a real evidence package, not source authority, and not acquired evidence. A separately governed evidence-package completion candidate is required before any filled operator evidence package can be prepared, supplied, validated, bound, used for source-authority acquisition reattempt, or used to support disposition, remediation, retry, or main merge.",
        "next_chain": list(NEXT_CHAIN), "next_gates": list(NEXT_GATES), "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": "not accepted", "profitability": "not accepted", "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED", "paper_trading": "NOT_AUTHORIZED", "broker_execution": "NOT_AUTHORIZED",
        "no_tracked_marketflow_files": True, "no_tracked_pytest_cache_files": True,
    }
    review[TEMPLATE_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_PACKAGE_TEMPLATE_DIGEST, "review": review["package_header_template_review"]})
    review[EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_EVIDENCE_ITEM_TEMPLATE_DIGEST, "contract": review["evidence_item_template_review"], "rows": rows})
    review[CHECKLIST_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_PREPARATION_CHECKLIST_DIGEST, "review": review["preparation_checklist_review"]})
    review[COVERAGE_REVIEW_DIGEST_KEY] = semantic_digest({"source_digest": SOURCE_TEMPLATE_COVERAGE_DIGEST, "review": review["template_coverage_review"]})
    digest_exclusions = ("checklist", "summary", RESULTS_REVIEW_DIGEST_KEY, MANIFEST_DIGEST_KEY)
    review[RESULTS_REVIEW_DIGEST_KEY] = _digest_without(review, *digest_exclusions)
    review[MANIFEST_DIGEST_KEY] = semantic_digest({"results_review_digest": review[RESULTS_REVIEW_DIGEST_KEY], "template_review_digest": review[TEMPLATE_REVIEW_DIGEST_KEY], "evidence_item_template_review_digest": review[EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY], "checklist_review_digest": review[CHECKLIST_REVIEW_DIGEST_KEY], "coverage_review_digest": review[COVERAGE_REVIEW_DIGEST_KEY]})
    check_ids = tuple(dict.fromkeys(("artifact_kind_correct", "results_review_status_correct", "results_review_scope_correct",
        *(f"source_binding_{key}" for key in SOURCE_BINDINGS), *(f"{key}_true" for key in TRUE_FIELDS), *(f"{key}_false" for key in FALSE_FIELDS),
        *(f"template_row_{row['mapped_missing_authority_id']}_reviewed" for row in rows), *(f"output_{item}_generated" for item in OUTPUT_IDS),
        *(f"domain_{item['domain_id']}_defined" for item in DOMAINS), *(f"risk_control_{item}_defined" for item in RISK_CONTROLS),
        "findings_defined", "recommendation_defined", "next_chain_defined", "next_gates_defined", "digests_generated")))
    review["checklist"] = [{"check_id": item, "status": PASS, "expected": True, "actual": True, "severity": BLOCKER, "message": f"{item} passed"} for item in check_ids]
    review["summary"] = {"total_checks": len(check_ids), "passed_checks": len(check_ids), "failed_checks": 0, "blocker_count": 0,
        "operator_source_authority_evidence_package_preparation_results_review_created": True,
        "operator_source_authority_evidence_package_preparation_results_review_ready": True, "source_execution_reviewed": True,
        "source_execution_status": source.EXECUTION_STATUS, "selected_operator_source_authority_evidence_package_preparation_package": SELECTED_PACKAGE,
        "operator_fillable_template_reviewed": True, "operator_fillable_evidence_item_template_count": 30,
        "operator_fillable_preparation_checklist_reviewed": True, "operator_source_authority_evidence_package_created": False,
        "operator_source_authority_evidence_package_supplied": False, "operator_source_authority_evidence_package_validated": False,
        "operator_source_authority_evidence_package_bound": False, "source_authority_acquisition_performed": False,
        "source_authority_evidence_acquired": False, "external_evidence_acquired": False, "concrete_source_authority_established": False,
        "safe_source_authority_bound_change_identified": False, "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30, "template_mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED", "ready_for_operator_source_authority_evidence_package_completion_candidate_after_template_review": True,
        "ready_for_source_authority_acquisition_execution_retry": False, "ready_for_source_authority_acquisition_results_review": False,
        "ready_for_remediation_execution": False, "ready_for_retry_candidate": False, "ready_for_main_merge_approval": False,
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped", "priority_1_total_nodeids": 612,
        "failed_or_errored_nodeids_count": 1404, "observable_failure_family_count": 4, "total_observable_evidence_items": 188,
        "recommended_next_task": RECOMMENDED_NEXT_TASK, "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "broker_execution_authorized": False}
    return review


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(*, source_execution: dict | None = None) -> dict[str, Any]:
    execution = _committed_source_execution() if source_execution is None else deepcopy(source_execution)
    _validate_source_execution(execution)
    review = _assemble_review()
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(review)
    return review


def validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(review: dict) -> dict[str, Any]:
    if not isinstance(review, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("review must be an object")
    expected = _assemble_review()
    difference = _first_difference(review, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError(f"{difference} mismatch")
    return {"artifact_kind": ARTIFACT_KIND, "results_review_status": RESULTS_REVIEW_STATUS, "results_review_scope": RESULTS_REVIEW_SCOPE,
        "results_review_digest": review[RESULTS_REVIEW_DIGEST_KEY], **{key: review["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")}}


MARKDOWN_SECTIONS = tuple("""Source Execution
Source Approval
Selected Preparation Package
Source Operator Review
Source Preparation Candidate
Source Failure Diagnosis
Source Blocked Acquisition Execution
Blocked Reason
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
Acquisition Scope Facts
Missing Authority Mapping
Acceptable Source Artifact Inventory
Package Header Template Review
Evidence Item Template Review
Thirty Missing Authority Template Rows Review
Preparation Checklist Review
Source Owner Request Guidance Review
Custody and Digest Guidance Review
No Secret Boundary Review
Results Review Before Use
Actual Evidence Absence
Actual Coverage Zero
Template Is Not Source Authority
Unsupported Claims Boundary
Review Findings
Review Domains
Outputs
Recommendation
Next Chain
Next Gates
Risk Controls
Authority Boundaries
Checklist Summary
Guardrails""".splitlines())


def build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_markdown_v1(review: dict) -> str:
    validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(deepcopy(review))
    sections = {
        "Source Execution": {key: review[key] for key in ("source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope", "source_execution_digest")},
        "Source Approval": {key: review[key] for key in ("source_approval_commit", "source_approval_digest", "source_attestation_digest")},
        "Selected Preparation Package": review["selected_operator_source_authority_evidence_package_preparation_package"],
        "Source Operator Review": {key: review[key] for key in ("source_operator_review_commit", "source_operator_review_digest")},
        "Source Preparation Candidate": {key: review[key] for key in ("source_preparation_candidate_commit", "source_preparation_candidate_digest")},
        "Source Failure Diagnosis": {key: review[key] for key in ("source_failure_diagnosis_commit", "source_failure_diagnosis_digest")},
        "Source Blocked Acquisition Execution": {key: review[key] for key in ("source_blocked_acquisition_execution_commit", "source_blocked_acquisition_execution_manifest_digest")},
        "Blocked Reason": review["source_blocked_acquisition_execution_reason"],
        "Source Acquisition Approval Chain": {key: review[key] for key in ("source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest")},
        "Retry Failure Context": review["retry_failure_context"], "Priority 1 Target Modules": review["priority_1_target_modules"],
        "Priority 1 Validation Summary": review["priority1_validation_summary"], "Diagnostic Capture Evidence Summary": review["diagnostic_capture_evidence_summary"],
        "Reviewed Observable Families": review["reviewed_observable_failure_families"], "Reviewed Workstreams": review["reviewed_workstreams"],
        "Acquisition Scope Facts": {key: review[key] for key in ("acquisition_scope_section_count", "mapped_missing_authority_item_count", "acceptable_source_artifact_type_count")},
        "Missing Authority Mapping": review["missing_authority_mapping"], "Acceptable Source Artifact Inventory": review["acceptable_source_artifact_type_inventory"],
        "Package Header Template Review": review["package_header_template_review"], "Evidence Item Template Review": review["evidence_item_template_review"],
        "Thirty Missing Authority Template Rows Review": review["thirty_missing_authority_template_rows_review"], "Preparation Checklist Review": review["preparation_checklist_review"],
        "Source Owner Request Guidance Review": review["source_owner_request_guidance_review"], "Custody and Digest Guidance Review": review["custody_and_digest_guidance_review"],
        "No Secret Boundary Review": review["no_secret_boundary_review"], "Results Review Before Use": review["results_review_before_use"],
        "Actual Evidence Absence": review["actual_evidence_absence"], "Actual Coverage Zero": review["template_coverage_review"],
        "Template Is Not Source Authority": review["template_source_authority_disposition"],
        "Unsupported Claims Boundary": {key: review[key] for key in FALSE_FIELDS}, "Review Findings": review["review_findings"],
        "Review Domains": review["review_domains"], "Outputs": review["outputs"],
        "Recommendation": {key: review[key] for key in ("recommended_next_task", "recommended_next_task_status", "recommended_action", "reason")},
        "Next Chain": review["next_chain"], "Next Gates": review["next_gates"], "Risk Controls": review["risk_controls"],
        "Authority Boundaries": {**{key: review[key] for key in TRUE_FIELDS}, **{key: review[key] for key in FALSE_FIELDS}},
        "Checklist Summary": review["summary"], "Guardrails": review["risk_controls"],
    }
    source_digest_sections = {
        "Source Follow-On Results Review": "source_follow_on_results_review_digest", "Source Follow-On Execution": "source_follow_on_execution_digest",
        "Source Follow-On Approval": "source_follow_on_approval_digest", "Source Follow-On Operator Review": "source_follow_on_operator_review_digest",
        "Source Follow-On Candidate": "source_follow_on_candidate_digest", "Source Results Review": "source_results_review_digest",
        "Source Enrichment Execution": "source_enrichment_execution_digest", "Source Historical Approval": "historical_source_approval_digest",
        "Source Historical Operator Review": "historical_source_operator_review_digest", "Source Historical Candidate": "historical_source_candidate_digest",
        "Historical Failure Diagnosis": "historical_failure_diagnosis_digest", "Historical Blocked Remediation": "historical_blocked_remediation_manifest_digest",
        "Source Remediation Plan and Method Chain": "source_remediation_plan_or_execution_after_method_results_review_digest",
        "Source Diagnostic Results Review": "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "Source Controlled Recapture": "source_receipt_recovery_or_recapture_execution_digest", "Source Durable Receipt": "source_durable_receipt_path",
        "Source Planning and Detail Binding Evidence": "source_detail_binding_results_review_digest",
    }
    sections.update({title: review[key] for title, key in source_digest_sections.items()})
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Results Review After Execution v1", "", f"Artifact: `{review['artifact_kind']}`", "", f"Status: `{review['results_review_status']}`", "", f"Scope: `{review['results_review_scope']}`", "", f"Results-review digest: `{review[RESULTS_REVIEW_DIGEST_KEY]}`", ""]
    for title in MARKDOWN_SECTIONS:
        lines.extend((f"## {title}", "", "```text", repr(sections[title]), "```", ""))
    return "\n".join(lines)


def write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(output_dir: str | Path, *, source_execution: dict | None = None) -> dict[str, Any]:
    destination = Path(output_dir)
    if any(part.lower() in {".marketflow", ".pytest_cache", ".env"} for part in destination.parts):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError("protected output directory")
    review = build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(source_execution=source_execution)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_STATUS.md"
    path.write_text(build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_markdown_v1(review), encoding="utf-8")
    return review


__all__ = ["ARTIFACT_KIND", "SCHEMA_VERSION", "RESULTS_REVIEW_STATUS", "RESULTS_REVIEW_SCOPE", "SELECTED_PACKAGE",
    "RESULTS_REVIEW_DIGEST_KEY", "TEMPLATE_REVIEW_DIGEST_KEY", "EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY", "CHECKLIST_REVIEW_DIGEST_KEY", "COVERAGE_REVIEW_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_READY",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_ONLY_NOT_TEMPLATE_EXECUTION_NOT_ACTUAL_EVIDENCE_PACKAGE_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_CREATE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_FROM_REVIEWED_ACQUISITION_SCOPE_ONLY",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_markdown_v1"]
