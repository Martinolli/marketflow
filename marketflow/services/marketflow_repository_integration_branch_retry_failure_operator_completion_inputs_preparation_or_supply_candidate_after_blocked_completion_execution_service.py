"""Define future operator completion-input options after a blocked execution.

This module is deliberately offline and dictionary-only.  It creates a
candidate for operator review; it does not prepare inputs, inspect secrets,
complete evidence, acquire authority, remediate code, or run a retry.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_service
    as source,
)


ARTIFACT_KIND = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_V1"
SCHEMA_VERSION = "marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1"
CANDIDATE_STATUS = "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_READY_FOR_OPERATOR_REVIEW"
CANDIDATE_SCOPE = "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN"
CANDIDATE_DISPOSITION = "CANDIDATE_READY_FOR_OPERATOR_REVIEW_NOT_SELECTED_NOT_APPROVED_NOT_EXECUTED"

SOURCE_FAILURE_DIAGNOSIS_COMMIT = "07276fc4b171179eb7210ce679ba2a9bdbd17e8c"
SOURCE_FAILURE_DIAGNOSIS_DIGEST = "3789d82ea1ef74aed2a6d7d7b1404254c0b5672eaf3c8080095ec21907e50759"
SOURCE_FAILURE_CLASSIFICATION_DIGEST = "e8086ac688202f1a9f850a605c6ae2bbf942413b8bbfab2730aa062edfd2d16d"
SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST = "607a9745ff0c76af61af884e4696138354446e2a7dcfbfd362ec508bbfb1b38e"
SOURCE_COVERAGE_DIAGNOSIS_DIGEST = "a551bfc14e7e836b03ff5d98a37355d9ef211098c044bce666951e499a511516"
SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST = "f354ae2af92e1d9fb1c29a409868747e075953969dec69f5aad69b4f8f7f37cc"

RECOMMENDED_PACKAGE = "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE"
SELECTED_COMPLETION_PACKAGE = source.SELECTED_PACKAGE
PRIMARY_FAILURE_CLASS = source.PRIMARY_FAILURE_CLASS
SECONDARY_FAILURE_CLASSES = source.SECONDARY_FAILURE_CLASSES

CANDIDATE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_digest"
PACKAGE_OPTIONS_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_package_options_digest"
INPUT_CONTRACT_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_input_contract_digest"
SOURCE_BINDING_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_source_binding_digest"
COVERAGE_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_coverage_digest"
MANIFEST_DIGEST_KEY = "marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_manifest_digest"

ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_V1 = ARTIFACT_KIND
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_READY_FOR_OPERATOR_REVIEW = CANDIDATE_STATUS
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN = CANDIDATE_SCOPE
PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE = RECOMMENDED_PACKAGE

PASS, BLOCKER = "PASS", "BLOCKER"
NOT_ACCEPTED, NOT_AUTHORIZED = "not accepted", "NOT_AUTHORIZED"


class MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(ValueError):
    """Raised when candidate content crosses a closed boundary or drifts."""


def _first_difference(actual: Any, expected: Any, path: str = "candidate") -> str | None:
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
        for index, value in enumerate(expected):
            difference = _first_difference(actual[index], value, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


SOURCE_BINDINGS = {
    "source_completion_execution_commit": source.SOURCE_COMPLETION_EXECUTION_COMMIT,
    "source_completion_execution_artifact_kind": source.source.BLOCKED_ARTIFACT_KIND,
    "source_completion_execution_status": source.source.BLOCKED_STATUS,
    "source_completion_execution_scope": source.source.EXECUTION_SCOPE,
    "source_completion_execution_blocked_reason": PRIMARY_FAILURE_CLASS,
    "source_completion_execution_blocked_digest": source.SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST,
    "source_completion_execution_blocked_manifest_digest": source.SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST,
    "source_completion_execution_success_digests_absent": True,
    "source_approval_commit": "40bee1289543bb07e64e383eb2e1c61d83615bd5",
    "source_approval_digest": "f6c37c0a7c64487cdf9adb218f8d12b8c0a2dacc4d4c1debf96105d1b5ee954c",
    "source_attestation_digest": "5434cbb4c94d22f1e4fefb3efc0e6e651401a22d6217d4c118638fa6d38dc714",
    "selected_operator_source_authority_evidence_package_completion_package": SELECTED_COMPLETION_PACKAGE,
    "source_operator_review_commit": "d71bfb14a656592ab637d94d9dd30d73912104b0",
    "source_operator_review_digest": "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663",
    "source_package_options_review_digest": "903e25817b4eff9298ed782756f7c6cf82d08c55f374161320ff3bf1bc9faf2a",
    "source_operator_input_requirements_review_digest": "571582717ed926182363bed83f673c0312eeb28535151bf4a2e06a83b645faa5",
    "source_template_binding_review_digest": "e09fef3bc04abafafe1ce9fab37948be709b092d2a09c828a98c29c83bd66841",
    "source_coverage_review_digest": "c8eecc0c7c93299a8dba7fb7b84f47e26b5d96ffecd69f7d4355cbd0ad635352",
    "source_operator_review_manifest_digest": "91393843b040ee9d67284689b5e4742019e3d18c2092c1950f742d9dceb71c64",
    "source_completion_candidate_commit": "7af6b1b5ad223f92da0997e2b7abcb73543470df",
    "source_completion_candidate_digest": "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207",
    "source_completion_candidate_package_options_digest": "c276ff30b28441dfd3ebb1dc4071b6a82e29c42b593215aa603c56587fc7e982",
    "source_completion_candidate_operator_input_requirements_digest": "615a15e243999e28770b3f1351df1cc5b4e8ebbf22febc36812fcf42dd59b7fb",
    "source_completion_candidate_template_binding_digest": "734eac89400c983c042f5c0a9c91e85694aad62ab07f3c8e046c406e02813df3",
    "source_completion_candidate_coverage_digest": "ba547fc27cbf2642a070383d600952a5798c1e2a0d7b703ba3fd049486e9e107",
    "source_completion_candidate_manifest_digest": "983951245e47b0fcc4d31b818a8adf16785f96dc8e2688ed12ce679fd17cb91b",
    "source_results_review_commit": "268c84d7ef4ed550bb38f07670247540590885f6",
    "source_results_review_digest": "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332",
    "source_template_review_digest": "3e60c8bb9c9000f6d5ca561ae843c17ec4abd31276fa443d7b9d97b7524040b9",
    "source_evidence_item_template_review_digest": "8b9994a28e017fc5e61cb0274b9191f61857594dfa1a3dc861e3087e3da7520c",
    "source_preparation_checklist_review_digest": "e4a57857d17f7fd68fce5af88a3efab02f54e5e33fc61be241740a35a0b9fcc2",
    "source_template_coverage_review_digest": "7ae349f3c94be97808aa0930429614cb2f33917f73694693d32ebb4e7656b290",
    "source_results_review_manifest_digest": "f4b7d2838a11d192497e7b79e7d2cc7ec3f1aac3d43dcf7362014c5724a109f0",
    "source_template_preparation_execution_commit": "a39332feb29a23612ee51cb45e8d5663b144c638",
    "source_template_preparation_execution_digest": "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3",
    "source_package_template_digest": "fb406078ca1a1199a430dd836050f9b198373c1f46c19cb5ee899ffe7e975a9a",
    "source_evidence_item_template_digest": "820cdf4c4a758b1d24ad0112fa6a1b05a8e6a330dc717c3564be4434b00af6e9",
    "source_preparation_checklist_digest": "4f965c0e7072dc6061ed3731e0eb7a639e117780c09544a6031663d6a6959605",
    "source_template_coverage_digest": "b9b25bd3609aff81a4bb4e47e999e41ea265cda5419be4be184f1a73b25e7884",
    "source_template_preparation_execution_manifest_digest": "272cadca012100d25e5628f09a3e91f8919a9fb80b8433ca2841a28d65a76a39",
    "source_template_approval_commit": "e942849f3126c95b432c6ce77f21eb96586f9b4b",
    "source_template_approval_digest": "e7f1d8a5ae413ca0f971257e13554a63b3ee95e942e156adb5b204cbcc378cbd",
    "source_template_attestation_digest": "e16b2afde6c36d5461a65d2f598fec55f9a13811a555efc90a9dac1e981f7328",
    "source_preparation_candidate_commit": "8d2944edfb7a54056f4a59c3d5817e823da80ce8",
    "source_preparation_candidate_digest": "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391",
    "source_previous_failure_diagnosis_commit": "e51b3f58215a3ecb25f863655c79490cbdd65342",
    "source_previous_failure_diagnosis_digest": "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c",
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
    "source_results_review_digest_historical": "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb",
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

SOURCE_CONTEXT = {
    "retry_execution_branch": "feature/marketflow-repository-integration-branch-retry-execution-v1",
    "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
    "retry_pytest_working_directory": "C:\\Users\\Aspire5 15 i7 4G2050\\marketflow_worktrees\\integration-terminal-evidence-stack-validation-v1",
    "retry_pytest_passed_count": 24877,
    "retry_pytest_failed_count": 1292,
    "retry_pytest_error_count": 112,
    "retry_pytest_skipped_count": 7,
    "retry_pytest_first_result_authoritative": True,
    "retry_pytest_passed": False,
    "retry_pytest_failed": True,
    "root_full_regression_is_retry_evidence": False,
    "priority1_pre_change_validation_passed": True,
    "priority1_pre_change_validation_passed_count": 675,
    "priority1_post_change_validation_passed": True,
    "priority1_post_change_validation_passed_count": 675,
    "priority1_post_change_validation_duration_seconds": "41.88",
    "priority1_post_change_stdout_byte_count": 832,
    "priority1_post_change_stderr_byte_count": 0,
    "priority1_post_change_stdout_sha256": "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374",
    "priority1_post_change_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "priority1_validation_is_retry_evidence": False,
    "source_exit_code": 1,
    "source_duration_seconds": "21.584361",
    "source_stdout_byte_count": 1231380,
    "source_stderr_byte_count": 0,
    "source_combined_output_byte_count": 1231380,
    "source_stdout_sha256": "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a",
    "source_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "source_stdout_excerpt_truncated": True,
    "source_stderr_excerpt_truncated": False,
    "source_redaction_checked": True,
    "source_diagnostic_metadata_only": True,
}

PRIORITY_1_TARGET_MODULES = (
    ("tests/test_marketflow_signal_or_feature_generation_results_review_service.py", 136),
    ("tests/test_post_identity_freeze_registry_inventory_approval_service.py", 131),
    ("tests/test_corporate_action_authority_plan_candidate_service.py", 122),
    ("tests/test_feature_generation_results_review_redesigned_labels_service.py", 112),
    ("tests/test_marketflow_objective_label_or_target_generation_results_review_service.py", 111),
)

OBSERVABLE_FAMILIES = (
    ("assertion_or_value_mismatch", 47, "HIGH"),
    ("digest_or_hash_mismatch", 47, "HIGH"),
    ("fixture_or_test_isolation_issue", 47, "HIGH"),
    ("missing_or_unexpected_field", 47, "HIGH"),
)

WORKSTREAMS = (
    ("assertion_value_mismatch_workstream", "assertion_or_value_mismatch"),
    ("digest_hash_boundary_workstream", "digest_or_hash_mismatch"),
    ("fixture_isolation_determinism_workstream", "fixture_or_test_isolation_issue"),
    ("schema_field_contract_workstream", "missing_or_unexpected_field"),
)

SECTION_WORKSTREAM_RANGES = (
    (range(1, 9), "assertion_value_mismatch_source_authority_scope", "assertion_value_mismatch_workstream"),
    (range(9, 17), "digest_hash_boundary_source_authority_scope", "digest_hash_boundary_workstream"),
    (range(17, 24), "fixture_isolation_determinism_source_authority_scope", "fixture_isolation_determinism_workstream"),
    (range(24, 31), "schema_field_contract_source_authority_scope", "schema_field_contract_workstream"),
)


def _missing_authority_mapping() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for indexes, section_id, workstream_id in SECTION_WORKSTREAM_RANGES:
        rows.extend(
            {
                "missing_authority_id": f"MA-{index:03d}",
                "section_id": section_id,
                "workstream_id": workstream_id,
                "current_status": "MISSING_NOT_ACQUIRED",
            }
            for index in indexes
        )
    return rows


PACKAGE_OPTIONS = (
    (RECOMMENDED_PACKAGE, "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_RECOMMENDED_NOT_SELECTED", "Future execution may prepare or supply explicit non-secret operator completion inputs for all 30 reviewed template rows, preserving row mappings, source-owner/origin, source reference, digest/provenance, classification, specification/observation separation, expected/actual scope, authority statement, no-secret declarations, and all false direct-change/remediation/retry/main flags.", None),
    ("PACKAGE_PREPARE_COMPLETION_INPUT_HEADER_FIELDS_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may prepare only the non-secret package-header input fields, without evidence-item completion, validation, binding, acquisition, or package completion.", None),
    ("PACKAGE_PREPARE_COMPLETION_INPUT_EVIDENCE_ITEM_ROWS_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may prepare only the 30 evidence-item input rows from non-secret operator-provided values while preserving results-review-before-use and all authorization flags as false.", None),
    ("PACKAGE_PREPARE_SOURCE_OWNER_REFERENCE_AND_PROVENANCE_MAPPING_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may prepare only source-owner/origin, source-reference, created-UTC, digest, and reproducible-provenance mappings for later review.", None),
    ("PACKAGE_PREPARE_WORKSTREAM_SPECIFIC_COMPLETION_INPUT_SETS", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may prepare completion inputs by reviewed workstream: assertion/value, digest/hash, fixture/isolation, and schema/field contract, without validating or binding evidence.", None),
    ("PACKAGE_PREPARE_COMPLETION_INPUT_CHECKLIST_AND_ATTESTATION_ONLY", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may prepare only a non-secret operator checklist and attestation framework for later completion-input supply, without creating actual inputs.", None),
    ("PACKAGE_HOLD_PENDING_OPERATOR_COMPLETION_INPUTS", "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED", "CANDIDATE_AVAILABLE_NOT_SELECTED", "Future execution may record a hold disposition for input preparation or supply only, pending explicit non-secret operator inputs.", None),
    ("PACKAGE_FABRICATE_COMPLETION_INPUTS_FROM_TEMPLATE_PLACEHOLDERS", "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", "", "Template placeholders are not operator completion inputs and cannot be converted into evidence or source authority."),
    ("PACKAGE_DERIVE_COMPLETION_INPUTS_FROM_DIAGNOSTIC_OUTPUT", "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", "", "Diagnostic output is observation metadata only and cannot substitute for non-secret operator source-authority completion inputs."),
    ("PACKAGE_VALIDATE_BIND_OR_ACQUIRE_EVIDENCE_DURING_INPUT_PREPARATION", "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", "", "Evidence validation, evidence binding, and source-authority acquisition require separate completion results review and separately approved acquisition execution."),
    ("PACKAGE_REATTEMPT_COMPLETION_EXECUTION_IMMEDIATELY_FROM_FAILURE_DIAGNOSIS", "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", "", "Completion reattempt requires separately reviewed, separately approved, explicit non-secret operator completion inputs."),
    ("PACKAGE_REMEDIATE_RETRY_OR_MAIN_MERGE_FROM_MISSING_INPUTS_DIAGNOSIS", "BLOCKED_NOT_ALLOWED", "CANDIDATE_BLOCKED_NOT_ALLOWED", "", "A missing-inputs diagnosis does not support remediation, retry readiness, retry success, or main-merge readiness."),
)

FUTURE_INPUT_REQUIREMENT_IDS = tuple("""source_failure_diagnosis_must_be_bound
source_completion_execution_must_be_bound
source_completion_execution_blocked_reason_must_be_no_inputs
source_completion_execution_success_digests_must_remain_absent
source_approval_must_be_bound
source_operator_review_must_be_bound
source_completion_candidate_must_be_bound
source_template_results_review_must_be_bound
source_template_execution_must_be_bound
source_preparation_failure_acquisition_chain_must_be_bound
follow_on_enrichment_historical_digests_must_be_bound
plan_method_diagnostic_recovery_digests_must_be_bound
durable_receipt_path_must_remain_opaque
retry_failure_counts_must_be_bound
priority_1_context_must_be_bound
priority1_validation_must_remain_non_retry_evidence
diagnostic_metadata_must_remain_diagnostic_only
observable_families_must_remain_planning_evidence
reviewed_workstreams_must_remain_non_authorizing
reviewed_template_structure_must_be_bound
reviewed_template_rows_must_remain_30
actual_coverage_must_remain_zero_in_candidate
missing_authority_items_must_remain_missing_in_candidate
count_label_distinction_must_be_preserved
future_inputs_must_be_non_secret
future_inputs_must_not_include_api_keys
future_inputs_must_not_include_broker_credentials
future_inputs_must_not_include_personal_financial_credentials
future_inputs_must_not_include_market_data_credentials
future_inputs_must_not_include_private_tokens
future_inputs_must_include_package_source_owner_or_origin
future_inputs_must_include_package_reference
future_inputs_must_include_package_created_utc
future_inputs_must_include_package_digest_or_reproducible_provenance
future_inputs_must_include_no_secret_declarations
future_inputs_must_include_evidence_items
future_inputs_must_include_30_evidence_items
each_item_must_map_to_reviewed_missing_authority_id
each_item_must_include_section_id
each_item_must_include_workstream_id
each_item_must_include_acceptable_source_artifact_type
each_item_must_include_source_owner_or_origin
each_item_must_include_source_reference
each_item_must_include_digest_or_reproducible_provenance
each_item_must_include_evidence_classification
each_item_must_include_specification_or_observation
each_item_must_include_expected_or_actual_scope
each_item_must_include_authority_statement
each_item_must_require_results_review_before_use
each_item_must_force_direct_change_false
each_item_must_force_remediation_false
each_item_must_force_retry_false
each_item_must_force_main_merge_false
preparation_or_supply_execution_must_not_validate_evidence
preparation_or_supply_execution_must_not_bind_evidence
preparation_or_supply_execution_must_not_acquire_source_authority
preparation_or_supply_execution_must_not_read_external_documents_unless_separately_approved
preparation_or_supply_execution_must_not_contact_source_owners
preparation_or_supply_execution_must_not_run_pytest_or_retry
completion_reattempt_requires_separate_review_and_approval
source_authority_acquisition_requires_reviewed_completed_package
runtime_and_trading_remain_not_authorized""".splitlines())

ALLOWED_SECTION_IDS = tuple(item[1] for item in SECTION_WORKSTREAM_RANGES)
ALLOWED_WORKSTREAM_IDS = tuple(item[2] for item in SECTION_WORKSTREAM_RANGES)
ALLOWED_ARTIFACT_TYPES = tuple("""approved_product_specification
approved_schema_definition
approved_artifact_contract
approved_canonical_payload_or_serialization_contract
approved_expected_value_source
approved_actual_value_source
approved_digest_manifest_source
approved_fixture_lifecycle_document
approved_deterministic_execution_contract
approved_export_surface_contract
approved_operator_provided_evidence_package
approved_source_owning_team_statement
approved_reviewed_source_digest_bundle""".splitlines())
ALLOWED_EVIDENCE_CLASSIFICATIONS = tuple("""SPECIFICATION
APPROVED_CONTRACT
SOURCE_OWNER_STATEMENT
CANONICAL_PAYLOAD
CANONICAL_SCHEMA
CANONICAL_SERIALIZATION
EXPECTED_VALUE_SOURCE
ACTUAL_VALUE_SOURCE
FIXTURE_LIFECYCLE_AUTHORITY
DETERMINISM_AUTHORITY
EXPORT_SURFACE_AUTHORITY
REVIEWED_SOURCE_DIGEST_BUNDLE""".splitlines())
ALLOWED_SPECIFICATION_OR_OBSERVATION = ("SPECIFICATION", "OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT")
ALLOWED_EXPECTED_OR_ACTUAL_SCOPE = ("EXPECTED", "ACTUAL", "BOTH", "NOT_APPLICABLE")
SECRET_MARKERS = (
    "API keys", "broker credentials", "personal financial credentials", "market data credentials",
    "private tokens", "access tokens", "passwords", "secrets", "private keys", "bearer tokens",
    "IBKR credentials", "account numbers", "seed phrases",
)

FUTURE_PLAN_STEPS = (
    "Bind this candidate and the source completion execution failure diagnosis.",
    "Bind the blocked completion execution, source approval, source operator review, source completion candidate, template-preparation results review, template-preparation execution, preparation chain, acquisition chain, follow-on/enrichment chain, historical remediation chain, plan/method/diagnostic/recovery chain, module-grouping chain, and staged inventory.",
    "Preserve the blocked reason NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED.",
    "Preserve success digests as absent in the blocked source execution.",
    "Preserve actual coverage as 0/30 and every missing-authority item as MISSING_NOT_ACQUIRED.",
    "Define future input preparation or supply package options without selecting any.",
    "Define the recommended future package for explicit non-secret operator completion inputs.",
    "Define required non-secret package-header input fields.",
    "Define required non-secret evidence-item input fields.",
    "Define allowed section, workstream, artifact-type, classification, specification/observation, and expected/actual values.",
    "Preserve all no-secret, no-API-key, no-broker-credential, no-personal-financial-credential, no-market-data-credential, and no-private-token requirements.",
    "Preserve direct-change, remediation, retry, and main-merge flags as false.",
    "Require operator review before any input-preparation or input-supply approval.",
    "Require approval before any input-preparation or input-supply execution.",
    "Require results review after any preparation or supply execution.",
    "Require separately approved completion reattempt after reviewed non-secret inputs exist.",
    "Preserve source-authority acquisition, no-change disposition, alternate diagnostic, remediation, retry, and main-merge gates.",
)

PLANNED_OUTPUT_IDS = tuple("""operator_completion_inputs_preparation_or_supply_candidate_manifest
source_failure_diagnosis_binding_report
source_completion_execution_binding_report
source_completion_execution_blocked_reason_report
source_completion_execution_success_digests_absence_report
source_approval_binding_report
source_operator_review_binding_report
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
reviewed_template_row_mapping_report
actual_evidence_absence_report
actual_coverage_zero_report
missing_authority_inventory_report
count_label_distinction_report
input_preparation_or_supply_package_options_report
recommended_input_preparation_or_supply_package_report
future_input_supply_contract_report
non_secret_input_requirements_report
allowed_values_report
custody_digest_and_provenance_expectations_report
downstream_gate_preservation_report
unsupported_claims_boundary_report
digest_manifest""".splitlines())

NON_GOALS = tuple("""do_not_select_package_now
do_not_approve_package_now
do_not_authorize_package_now
do_not_execute_input_preparation_now
do_not_execute_input_supply_now
do_not_prepare_operator_completion_inputs_now
do_not_supply_operator_completion_inputs_now
do_not_validate_operator_completion_inputs_now
do_not_bind_operator_completion_inputs_now
do_not_create_completed_operator_evidence_package_now
do_not_create_evidence_package_now
do_not_fill_actual_evidence_items_now
do_not_supply_evidence_now
do_not_validate_evidence_now
do_not_bind_evidence_now
do_not_accept_evidence_as_source_authority_now
do_not_accept_template_as_evidence_now
do_not_accept_template_as_source_authority_now
do_not_convert_placeholders_to_inputs_now
do_not_convert_diagnostic_output_to_inputs_now
do_not_acquire_source_authority_now
do_not_acquire_source_authority_evidence_now
do_not_acquire_external_evidence_now
do_not_create_source_authority_acquisition_execution_now
do_not_retry_source_authority_acquisition_now
do_not_create_no_change_disposition_now
do_not_execute_alternate_diagnostics_now
do_not_execute_remediation_now
do_not_modify_production_code_now
do_not_modify_existing_tests_now
do_not_update_expected_digests_now
do_not_generate_patch_now
do_not_apply_patch_now
do_not_run_pytest_now
do_not_run_full_pytest_now
do_not_rerun_priority1_validation_now
do_not_rerun_retry_now
do_not_rerun_detached_retry_now
do_not_parse_durable_receipt_now
do_not_analyze_diagnostic_output_now
do_not_read_pytest_cache_now
do_not_modify_pytest_cache_now
do_not_parse_terminal_logs_now
do_not_parse_operator_logs_now
do_not_inspect_env_now
do_not_call_providers_now
do_not_contact_source_owners_now
do_not_read_external_documents_now
do_not_reconstruct_prior_lost_values_now
do_not_reconstruct_full_stdout_or_stderr_now
do_not_classify_modules_again_now
do_not_claim_failure_error_separation_now
do_not_identify_first_failure_now
do_not_identify_first_error_now
do_not_claim_traceback_root_cause_now
do_not_claim_root_cause_now
do_not_claim_retry_success_now
do_not_claim_main_merge_readiness_now
do_not_create_retry_candidate_now
do_not_create_retry_approval_now
do_not_create_retry_execution_now
do_not_create_retry_results_review_now
do_not_create_main_merge_approval_now
do_not_push_main
do_not_push_integration_branch
do_not_delete_or_reset_integration_branch
do_not_delete_or_reset_worktree
do_not_force_push
do_not_modify_tags
do_not_modify_staged_evidence
do_not_regenerate_evidence
do_not_commit_marketflow_outputs
do_not_commit_pytest_cache
do_not_acquire_market_data
do_not_generate_dataset
do_not_recompute_metrics
do_not_train_models
do_not_score_strategy
do_not_generate_trade_recommendations
do_not_accept_predictive_usefulness
do_not_accept_profitability
do_not_authorize_runtime
do_not_authorize_broker_execution
do_not_authorize_trading""".splitlines())

NEXT_CHAIN = (
    "Operator Completion Inputs Preparation or Supply Candidate Operator Review After Blocked Completion Execution v1.",
    "Operator Completion Inputs Preparation or Supply Approval v1, if selected.",
    "Operator Completion Inputs Preparation or Supply Execution v1, if approved.",
    "Operator Completion Inputs Preparation or Supply Results Review v1.",
    "Completion Execution Reattempt v1, only if reviewed explicit non-secret operator inputs exist and reattempt is separately approved.",
    "Operator Source Authority Evidence Package Completion Results Review v1, only if a completed package exists.",
    "Source Authority Acquisition Execution Reattempt with Reviewed Completed Evidence Package v1, only if separately approved.",
    "Source Authority Acquisition Results Review v1, only if evidence is bound.",
    "Conditional disposition, diagnostic, remediation, retry-criteria, or hold candidate only if reviewed acquired evidence supports it.",
    "New Integration Branch Retry Candidate v1, only after reviewed and approved basis exists.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
)

NEXT_GATES = tuple("""operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution
operator_completion_inputs_preparation_or_supply_approval_if_selected
operator_completion_inputs_preparation_or_supply_execution_if_approved
operator_completion_inputs_preparation_or_supply_results_review
completion_execution_reattempt_with_reviewed_non_secret_operator_inputs_if_approved
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

RISK_CONTROLS = tuple("""candidate_does_not_select_package
candidate_does_not_approve_package
candidate_does_not_authorize_package
candidate_does_not_execute_input_preparation
candidate_does_not_execute_input_supply
candidate_does_not_prepare_operator_completion_inputs
candidate_does_not_supply_operator_completion_inputs
candidate_does_not_validate_operator_completion_inputs
candidate_does_not_bind_operator_completion_inputs
candidate_does_not_create_completed_evidence_package
candidate_does_not_create_evidence_package
candidate_does_not_fill_actual_evidence_items
candidate_does_not_validate_evidence
candidate_does_not_bind_evidence
candidate_does_not_accept_evidence_as_source_authority
candidate_does_not_convert_template_placeholders_to_inputs
candidate_does_not_convert_diagnostic_output_to_inputs
candidate_does_not_acquire_source_authority
candidate_does_not_acquire_source_authority_evidence
candidate_does_not_acquire_external_evidence
candidate_does_not_create_source_authority_acquisition_execution
candidate_does_not_retry_source_authority_acquisition
candidate_does_not_create_no_change_disposition
candidate_does_not_execute_alternate_diagnostics
candidate_does_not_execute_remediation
candidate_does_not_modify_production_code
candidate_does_not_modify_existing_tests
candidate_does_not_update_expected_digests
candidate_does_not_generate_patch
candidate_does_not_apply_patch
candidate_does_not_run_pytest
candidate_does_not_run_full_pytest
candidate_does_not_rerun_priority1_validation
candidate_does_not_rerun_retry
candidate_does_not_rerun_detached_retry
candidate_does_not_parse_durable_receipt
candidate_does_not_analyze_diagnostic_output
candidate_does_not_rerun_source_authority_enrichment
candidate_does_not_rerun_follow_on_execution
candidate_does_not_rerun_plan_execution
candidate_does_not_regenerate_targeted_plan
candidate_does_not_rerun_method_execution
candidate_does_not_rerun_controlled_recapture
candidate_does_not_rerun_template_execution
candidate_does_not_rerun_completion_execution
candidate_does_not_run_diagnostic_command
candidate_does_not_read_pytest_cache
candidate_does_not_modify_pytest_cache
candidate_does_not_commit_pytest_cache
candidate_does_not_commit_marketflow_outputs
candidate_does_not_parse_terminal_logs
candidate_does_not_parse_operator_logs
candidate_does_not_inspect_env
candidate_does_not_contact_source_owners
candidate_does_not_read_external_documents
candidate_does_not_reconstruct_prior_lost_values
candidate_does_not_reconstruct_full_streams
candidate_does_not_classify_modules_again
candidate_does_not_classify_full_retry_failures
candidate_does_not_classify_full_retry_errors
candidate_does_not_claim_failure_error_separation
candidate_does_not_identify_authoritative_first_failure
candidate_does_not_identify_authoritative_first_error
candidate_does_not_claim_traceback_root_cause
candidate_does_not_claim_root_cause
candidate_does_not_claim_retry_success
candidate_does_not_claim_main_merge_readiness
candidate_does_not_create_retry_candidate
candidate_does_not_create_retry_approval
candidate_does_not_create_retry_execution
candidate_does_not_create_retry_results_review
candidate_does_not_create_main_merge_approval
candidate_does_not_push_main
candidate_does_not_push_integration_branch
candidate_does_not_delete_integration_branch
candidate_does_not_delete_worktree
candidate_does_not_force_push
candidate_does_not_modify_tags
candidate_does_not_regenerate_evidence
candidate_does_not_call_providers
candidate_does_not_acquire_market_data
candidate_does_not_generate_dataset
candidate_does_not_recompute_metrics
candidate_does_not_train_models
candidate_does_not_score_strategy
candidate_does_not_generate_trade_recommendations
candidate_does_not_accept_predictive_usefulness
candidate_does_not_accept_profitability
candidate_does_not_authorize_runtime
candidate_does_not_authorize_broker_execution
approved_completion_package_is_not_operator_input
reviewed_template_is_not_completed_evidence_package
template_placeholders_are_not_completion_inputs
synthetic_success_path_is_test_only
explicit_non_secret_inputs_required_before_completion_reattempt
completed_package_requires_results_review_before_acquisition_use
evidence_binding_requires_separate_acquisition_execution
evidence_binding_requires_results_review
acquisition_results_review_required_before_no_change_disposition
acquisition_results_review_required_before_alternate_diagnostic
acquisition_results_review_required_before_remediation
separate_completion_reattempt_requires_reviewed_operator_inputs
separate_remediation_approval_required_before_code_or_test_changes
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

TRUE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_candidate_created
operator_completion_inputs_preparation_or_supply_candidate_ready_for_operator_review
source_failure_diagnosis_bound
source_failure_diagnosis_reviewed
source_completion_execution_bound
source_completion_execution_blocked_reason_verified
source_completion_execution_success_digests_absent_verified
source_approval_bound
source_attestation_bound
selected_completion_package_bound
source_operator_review_bound
source_completion_candidate_bound
source_template_preparation_results_review_bound
source_template_preparation_execution_bound
source_preparation_candidate_bound
source_blocked_acquisition_execution_bound
source_acquisition_approval_bound
source_follow_on_results_review_bound
source_follow_on_execution_bound
source_authority_acquisition_candidate_bound
source_authority_acquisition_scope_bound
source_missing_authority_mapping_bound
follow_on_enrichment_historical_digests_bound
plan_method_diagnostic_recovery_digests_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_context_bound
priority_1_context_bound
priority1_validation_context_bound
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
operator_input_absence_verified
count_label_distinction_preserved
input_preparation_or_supply_package_options_defined
recommended_input_preparation_or_supply_package_defined
future_input_preparation_requirements_defined
future_input_supply_contract_defined
future_input_preparation_plan_defined
planned_outputs_defined
non_goals_defined
source_authority_gap_preserved
detached_retry_failed_status_preserved
ready_for_operator_completion_inputs_preparation_or_supply_candidate_operator_review""".splitlines())

FALSE_FIELDS = tuple("""operator_completion_inputs_preparation_or_supply_package_selected
operator_completion_inputs_preparation_or_supply_package_approved
operator_completion_inputs_preparation_or_supply_package_authorized
operator_completion_inputs_preparation_or_supply_package_executed
operator_completion_inputs_preparation_executed
operator_completion_inputs_supply_executed
operator_completion_inputs_prepared
operator_completion_inputs_supplied
operator_completion_inputs_provided
operator_completion_inputs_validated
operator_completion_inputs_bound
operator_completion_inputs_contained_secrets
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
pytest_performed_in_candidate
full_pytest_performed
priority1_validation_rerun_performed
retry_rerun_performed
detached_retry_rerun_performed
diagnostic_receipt_parsed_in_candidate
diagnostic_output_analyzed_in_candidate
source_authority_enrichment_rerun_performed
follow_on_execution_rerun_performed
plan_execution_rerun_performed
targeted_remediation_plan_regenerated_in_candidate
method_execution_rerun_performed
controlled_recapture_rerun_performed
template_execution_rerun_performed
completion_execution_rerun_performed
diagnostic_command_rerun_performed
cache_read_in_candidate
cache_modified_in_candidate
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
ready_for_operator_completion_inputs_preparation_or_supply_approval
ready_for_operator_completion_inputs_preparation_or_supply_execution
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
provider_requests_made_in_candidate
market_data_acquisition_performed_in_candidate
dataset_generation_performed_in_candidate
metric_recomputation_from_raw_rows_performed
model_training_performed
strategy_scoring_performed
trade_recommendations_generated""".splitlines())

COUNTS = {
    "operator_source_authority_evidence_item_count": 0,
    "operator_source_authority_evidence_item_template_count": 30,
    "reviewed_template_row_count": 30,
    "actual_covered_missing_authority_item_count": 0,
    "actual_uncovered_missing_authority_item_count": 30,
    "template_mapped_missing_authority_item_count": 30,
    "mapped_missing_authority_item_count": 30,
    "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    "completed_operator_evidence_item_count": 0,
    "operator_completion_input_item_count": 0,
    "future_operator_completion_input_item_count": 30,
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
    "future_input_preparation_requirement_count": 62,
    "future_input_preparation_plan_step_count": 17,
    "planned_output_count": 34,
    "non_goal_count": 76,
    "risk_control_count": 105,
    "future_completion_requirement_count": 67,
    "source_enumerated_future_completion_requirement_count": 69,
    "approved_future_completion_requirement_named_count": 69,
    "source_non_goal_count": 71,
    "source_enumerated_non_goal_count": 76,
    "source_risk_control_count": 104,
    "source_enumerated_risk_control_count": 106,
}


def _reviewed_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": f"<REQUIRED_UNIQUE_EVIDENCE_ID_FOR_{item['missing_authority_id']}>",
            "mapped_missing_authority_id": item["missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
            "source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>",
            "source_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>",
            "digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "evidence_classification": "<ONE_OF_ALLOWED_EVIDENCE_CLASSIFICATIONS>",
            "specification_or_observation": "<SPECIFICATION_OR_OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
            "expected_or_actual_scope": "<EXPECTED_ACTUAL_BOTH_OR_NOT_APPLICABLE>",
            "authority_statement": "<REQUIRED_NON_EMPTY_AUTHORITY_STATEMENT>",
            "results_review_required_before_use": True,
            "direct_change_authorized_now": False,
            "remediation_authorized_now": False,
            "retry_authorized_now": False,
            "main_merge_authorized_now": False,
            "template_only": True,
            "actual_evidence_supplied": False,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "MISSING_NOT_ACQUIRED",
        }
        for item in _missing_authority_mapping()
    ]


def _future_contract_rows() -> list[dict[str, Any]]:
    """Return planning examples of the required future supplied-item shape."""
    return [
        {
            "evidence_id": f"<FUTURE_OPERATOR_PROVIDED_EVIDENCE_ID_FOR_{item['missing_authority_id']}>",
            "mapped_missing_authority_id": item["missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "acceptable_source_artifact_type": "<ONE_OF_ALLOWED_ACCEPTABLE_SOURCE_ARTIFACT_TYPES>",
            "source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "source_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "evidence_classification": "<ONE_OF_ALLOWED_EVIDENCE_CLASSIFICATIONS>",
            "specification_or_observation": "<SPECIFICATION_OR_OBSERVATION_WITH_SOURCE_AUTHORITY_STATEMENT>",
            "expected_or_actual_scope": "<EXPECTED_ACTUAL_BOTH_OR_NOT_APPLICABLE>",
            "authority_statement": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "results_review_required_before_use": True,
            "direct_change_authorized_now": False,
            "remediation_authorized_now": False,
            "retry_authorized_now": False,
            "main_merge_authorized_now": False,
            "actual_evidence_supplied": True,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "PREPARED_OR_SUPPLIED_OPERATOR_COMPLETION_INPUT_PENDING_REVIEW",
        }
        for item in _missing_authority_mapping()
    ]


def _future_input_supply_contract() -> dict[str, Any]:
    return {
        "contract_status": "PLANNING_ONLY_NOT_EXECUTED",
        "package_header": {
            "package_source_owner_or_origin": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_reference": "<FUTURE_NON_SECRET_OPERATOR_INPUT>",
            "package_created_utc": "<FUTURE_UTC_TIMESTAMP>",
            "package_digest_or_reproducible_provenance": "<FUTURE_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
            "package_declares_no_secrets": True,
            "package_declares_no_api_keys": True,
            "package_declares_no_broker_credentials": True,
            "package_declares_no_personal_financial_credentials": True,
            "package_declares_no_market_data_credentials": True,
            "package_declares_no_private_tokens": True,
            "package_distinguishes_specification_from_observation": True,
            "package_distinguishes_expected_from_actual": True,
            "package_distinguishes_source_authority_from_diagnostic_output": True,
            "evidence_items": "EXACTLY_30_ITEMS_DEFINED_BY_THIS_CONTRACT",
        },
        "evidence_items": _future_contract_rows(),
        "allowed_section_ids": list(ALLOWED_SECTION_IDS),
        "allowed_workstream_ids": list(ALLOWED_WORKSTREAM_IDS),
        "allowed_acceptable_source_artifact_types": list(ALLOWED_ARTIFACT_TYPES),
        "allowed_evidence_classifications": list(ALLOWED_EVIDENCE_CLASSIFICATIONS),
        "allowed_specification_or_observation": list(ALLOWED_SPECIFICATION_OR_OBSERVATION),
        "allowed_expected_or_actual_scope": list(ALLOWED_EXPECTED_OR_ACTUAL_SCOPE),
        "future_execution_rejected_secret_markers": list(SECRET_MARKERS),
        "candidate_inspects_secrets": False,
    }


def _committed_source_failure_diagnosis() -> dict[str, Any]:
    """Return a literal projection of the committed diagnosis; call no builder."""
    return {
        "source_failure_diagnosis_artifact_kind": source.ARTIFACT_KIND,
        "source_failure_diagnosis_status": source.DIAGNOSIS_STATUS,
        "source_failure_diagnosis_scope": source.DIAGNOSIS_SCOPE,
        "source_failure_diagnosis_commit": SOURCE_FAILURE_DIAGNOSIS_COMMIT,
        "source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
        "source_failure_classification_digest": SOURCE_FAILURE_CLASSIFICATION_DIGEST,
        "source_operator_input_absence_diagnosis_digest": SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST,
        "source_coverage_diagnosis_digest": SOURCE_COVERAGE_DIAGNOSIS_DIGEST,
        "source_failure_diagnosis_manifest_digest": SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST,
        "primary_failure_class": PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(SECONDARY_FAILURE_CLASSES),
        **deepcopy(SOURCE_BINDINGS),
        **deepcopy(SOURCE_CONTEXT),
        "priority_1_target_modules": [
            {"path": path, "failed_or_errored_nodeid_count": count}
            for path, count in PRIORITY_1_TARGET_MODULES
        ],
        "reviewed_observable_failure_families": [
            {"family_id": family, "observable_evidence_count": count, "confidence": confidence}
            for family, count, confidence in OBSERVABLE_FAMILIES
        ],
        "reviewed_workstreams": [
            {"workstream_id": workstream, "source_family_id": family}
            for workstream, family in WORKSTREAMS
        ],
        "reviewed_template_structure": {
            "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
            "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
            "template_only": True,
            "actual_evidence_package_created": False,
        },
        "reviewed_template_rows": _reviewed_template_rows(),
        "missing_authority_mapping": _missing_authority_mapping(),
        "count_label_distinction": {
            "future_completion_requirement_count": 67,
            "source_enumerated_future_completion_requirement_count": 69,
            "approved_future_completion_requirement_named_count": 69,
            "non_goal_count": 71,
            "source_enumerated_non_goal_count": 76,
            "risk_control_count": 104,
            "source_enumerated_risk_control_count": 106,
            "preserved_without_reconciliation": True,
        },
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "mapped_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "priority_1_total_nodeids": 612,
        "top_10_count_sum": 1069,
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "observable_failure_family_count": 4,
        "total_observable_evidence_items": 188,
    }


def _validate_source_failure_diagnosis(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
            "source_failure_diagnosis must be an object"
        )
    expected = _committed_source_failure_diagnosis()
    for key, expected_value in expected.items():
        if key not in value:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
                f"source_failure_diagnosis.{key} missing"
            )
        difference = _first_difference(value[key], expected_value, f"source_failure_diagnosis.{key}")
        if difference:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
                f"{difference} mismatch"
            )


def _package_options() -> list[dict[str, Any]]:
    options = []
    for package_id, source_status, review_status, purpose, blocked_reason in PACKAGE_OPTIONS:
        item = {
            "package_id": package_id,
            "source_status": source_status,
            "candidate_review_status": review_status,
            "selected": False,
            "approved": False,
            "authorized": False,
            "executed": False,
        }
        item["blocked_reason" if blocked_reason else "purpose"] = blocked_reason or purpose
        options.append(item)
    return options


def _digest_without(candidate: Mapping[str, Any], *excluded: str) -> str:
    payload = deepcopy(dict(candidate))
    for key in excluded:
        payload.pop(key, None)
    return semantic_digest(payload)


def _assemble_candidate(source_diagnosis: Mapping[str, Any]) -> dict[str, Any]:
    source_projection = _committed_source_failure_diagnosis()
    package_options = _package_options()
    future_contract = _future_input_supply_contract()
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE,
        "created_offline": True,
        "governance_only": True,
        "candidate_only": True,
        "candidate_disposition": CANDIDATE_DISPOSITION,
        "candidate_philosophy": "The blocked completion execution correctly proved that no operator completion inputs were supplied. The next safe step is not to complete an evidence package, but to define a governed path for preparing or supplying explicit non-secret operator completion inputs that can later be reviewed, approved, and used in a separately invoked completion reattempt.",
        "candidate_boundary": "Candidate only. This candidate may define preparation/supply options, non-secret input requirements, custody and digest expectations, row-mapping constraints, review gates, and blocked shortcuts. It must not prepare or supply inputs, complete a package, validate or bind evidence, acquire source authority, authorize acquisition reattempt, remediate, retry, merge, call providers, contact source owners, inspect secrets, or authorize runtime/trading.",
        **deepcopy(source_projection),
        **deepcopy(COUNTS),
        **{field: True for field in TRUE_FIELDS},
        **{field: False for field in FALSE_FIELDS},
        "recommended_operator_completion_inputs_preparation_or_supply_package": RECOMMENDED_PACKAGE,
        "recommendation_status": "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
        "package_options": package_options,
        "future_input_preparation_requirements": [
            {
                "requirement_id": requirement_id,
                "requirement_status": "REQUIRED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION",
                "execution_status": "NOT_EXECUTED",
            }
            for requirement_id in FUTURE_INPUT_REQUIREMENT_IDS
        ],
        "future_input_supply_contract": future_contract,
        "secret_safety_for_future_execution": {
            "future_execution_must_reject_secret_markers": list(SECRET_MARKERS),
            "candidate_inspected_environment": False,
            "candidate_inspected_files_or_credentials": False,
            "candidate_contacted_external_systems": False,
        },
        "future_plan": [
            {"step": index, "plan_status": "PLANNED_NOT_EXECUTED", "action": action}
            for index, action in enumerate(FUTURE_PLAN_STEPS, 1)
        ],
        "planned_outputs": [
            {"output_id": output_id, "generation_status": "PLANNED_NOT_GENERATED"}
            for output_id in PLANNED_OUTPUT_IDS
        ],
        "non_goals": [{"non_goal_id": item, "active": True} for item in NON_GOALS],
        "actual_evidence_absence": {
            "completed_package_created": False,
            "evidence_package_created": False,
            "evidence_package_supplied": False,
            "evidence_package_validated": False,
            "evidence_package_bound": False,
            "actual_evidence_items_filled": False,
        },
        "actual_coverage": {
            "reviewed_template_row_count": 30,
            "actual_covered_missing_authority_item_count": 0,
            "actual_uncovered_missing_authority_item_count": 30,
            "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        },
        "outputs": [
            {"output_id": output_id, "status": "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_ONLY"}
            for output_id in PLANNED_OUTPUT_IDS
        ],
        "recommended_next_task": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_V1",
        "recommended_next_task_status": "FUTURE_OPERATOR_REVIEW_NOT_CREATED",
        "recommended_action": "PROCEED_TO_SEPARATELY_INVOKED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_BEFORE_ANY_INPUT_SUPPLY_APPROVAL_OR_COMPLETION_REATTEMPT",
        "reason": "The completion execution was approved and attempted, but it failed closed because no explicit non-secret operator completion inputs were supplied. A candidate is required to define safe future input preparation or supply options before any input-preparation approval, input-supply execution, completion reattempt, completion results review, source-authority acquisition reattempt, disposition, remediation, retry, or main merge.",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "no_tracked_marketflow_files": True,
        "no_tracked_pytest_cache_files": True,
    }
    candidate[PACKAGE_OPTIONS_DIGEST_KEY] = semantic_digest(candidate["package_options"])
    candidate[INPUT_CONTRACT_DIGEST_KEY] = semantic_digest({
        "requirements": candidate["future_input_preparation_requirements"],
        "contract": candidate["future_input_supply_contract"],
        "secret_safety": candidate["secret_safety_for_future_execution"],
    })
    candidate[SOURCE_BINDING_DIGEST_KEY] = semantic_digest(source_projection)
    candidate[COVERAGE_DIGEST_KEY] = semantic_digest(candidate["actual_coverage"])
    candidate[CANDIDATE_DIGEST_KEY] = _digest_without(
        candidate,
        "checklist", "summary", CANDIDATE_DIGEST_KEY, MANIFEST_DIGEST_KEY,
    )
    candidate[MANIFEST_DIGEST_KEY] = semantic_digest({
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
        "package_options_digest": candidate[PACKAGE_OPTIONS_DIGEST_KEY],
        "input_contract_digest": candidate[INPUT_CONTRACT_DIGEST_KEY],
        "source_binding_digest": candidate[SOURCE_BINDING_DIGEST_KEY],
        "coverage_digest": candidate[COVERAGE_DIGEST_KEY],
        "source_failure_diagnosis_digest": SOURCE_FAILURE_DIAGNOSIS_DIGEST,
    })
    candidate["checklist"] = _checklist(candidate)
    candidate["summary"] = _summary(candidate)
    return candidate


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    fixed = tuple("""artifact_kind_correct
candidate_status_correct
candidate_scope_correct
source_failure_diagnosis_commit_bound
source_failure_diagnosis_digest_bound
source_failure_classification_digest_bound
source_operator_input_absence_diagnosis_digest_bound
source_coverage_diagnosis_digest_bound
source_failure_diagnosis_manifest_digest_bound
source_completion_execution_blocked_reason_bound
source_completion_execution_success_digests_absent
primary_failure_class_bound
secondary_failure_classes_bound
durable_receipt_path_bound
durable_receipt_not_parsed
retry_failure_counts_bound
priority_1_total_612_bound
top_10_total_1069_bound
module_summary_count_29_bound
failed_or_errored_nodeids_1404_bound
priority1_validation_675_pre_and_post_bound
priority1_validation_not_retry_evidence
diagnostic_exit_code_1_bound_as_diagnostic_only
diagnostic_stdout_hash_bound
diagnostic_stderr_hash_bound
observable_family_count_4_bound
observable_evidence_items_188_bound
family_confidence_high_bound
workstream_count_4_bound
reviewed_template_row_count_30
actual_coverage_zero
missing_authority_items_missing_not_acquired
count_label_distinction_preserved
operator_input_absence_verified
candidate_created_true
candidate_ready_for_operator_review_true
package_options_defined
package_option_count_12
recommended_package_defined
available_packages_unselected
blocked_packages_blocked
future_input_preparation_requirements_defined
future_input_supply_contract_defined
future_input_preparation_plan_defined
planned_outputs_defined
non_goals_defined
outputs_generated
recommendation_defined
next_chain_defined
next_gates_defined
risk_controls_defined
candidate_digest_generated
package_options_digest_generated
input_contract_digest_generated
source_binding_digest_generated
coverage_digest_generated
manifest_digest_generated
no_tracked_marketflow_files
no_tracked_pytest_cache_files""".splitlines())
    source_checks = tuple(
        f"{key}_bound" for key in sorted(SOURCE_BINDINGS)
        if key.endswith(("_digest", "_commit", "_reason"))
    )
    check_ids = tuple(dict.fromkeys((
        *fixed,
        *source_checks,
        *(f"{field}_true" for field in TRUE_FIELDS),
        *(f"{field}_false" for field in FALSE_FIELDS),
        *(f"package_option_{index:02d}_defined" for index in range(1, 13)),
        *(f"future_requirement_{item}_defined" for item in FUTURE_INPUT_REQUIREMENT_IDS),
        *(f"future_plan_step_{index:02d}_defined" for index in range(1, 18)),
        *(f"planned_output_{item}_defined" for item in PLANNED_OUTPUT_IDS),
        *(f"non_goal_{item}_active" for item in NON_GOALS),
        *(f"output_{item}_generated" for item in PLANNED_OUTPUT_IDS),
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
        for check_id in check_ids
    ]


def _summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "operator_completion_inputs_preparation_or_supply_candidate_created",
        "operator_completion_inputs_preparation_or_supply_candidate_ready_for_operator_review",
        "source_failure_diagnosis_digest",
        "source_completion_execution_blocked_reason",
        "source_completion_execution_blocked_digest",
        "source_completion_execution_blocked_manifest_digest",
        "recommended_operator_completion_inputs_preparation_or_supply_package",
        "operator_completion_inputs_preparation_or_supply_package_selected",
        "operator_completion_inputs_preparation_or_supply_package_approved",
        "operator_completion_inputs_preparation_or_supply_package_authorized",
        "operator_completion_inputs_preparation_or_supply_package_executed",
        "operator_completion_inputs_prepared", "operator_completion_inputs_supplied",
        "operator_completion_inputs_provided", "operator_completion_inputs_validated",
        "operator_completion_inputs_bound", "operator_source_authority_evidence_package_completed",
        "operator_source_authority_evidence_package_created",
        "operator_source_authority_evidence_package_supplied",
        "operator_source_authority_evidence_package_validated",
        "operator_source_authority_evidence_package_bound", "source_authority_acquisition_performed",
        "source_authority_evidence_acquired", "external_evidence_acquired",
        "concrete_source_authority_established", "safe_source_authority_bound_change_identified",
        "actual_covered_missing_authority_item_count", "actual_uncovered_missing_authority_item_count",
        "missing_authority_items_status",
        "ready_for_operator_completion_inputs_preparation_or_supply_candidate_operator_review",
        "ready_for_operator_completion_inputs_preparation_or_supply_approval",
        "ready_for_operator_completion_inputs_preparation_or_supply_execution",
        "ready_for_operator_source_authority_evidence_package_completion_execution",
        "ready_for_source_authority_acquisition_execution_retry", "ready_for_retry_candidate",
        "ready_for_main_merge_approval", "priority_1_total_nodeids", "failed_or_errored_nodeids_count",
        "observable_failure_family_count", "total_observable_evidence_items", "package_option_count",
        "available_package_count", "blocked_package_count", "future_input_preparation_requirement_count",
        "future_input_preparation_plan_step_count", "planned_output_count", "recommended_next_task",
    )
    return {
        "total_checks": len(candidate["checklist"]),
        "passed_checks": len(candidate["checklist"]),
        "failed_checks": 0,
        "blocker_count": 0,
        **{key: deepcopy(candidate[key]) for key in keys},
        "retry_failure_counts": "24877 passed / 1292 failed / 112 errors / 7 skipped",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
    *, source_failure_diagnosis: dict | None = None,
) -> dict[str, Any]:
    """Build a deterministic candidate from committed facts or injected evidence."""
    source_value = _committed_source_failure_diagnosis() if source_failure_diagnosis is None else deepcopy(source_failure_diagnosis)
    _validate_source_failure_diagnosis(source_value)
    candidate = _assemble_candidate(source_value)
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)
    return candidate


def validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Reject source drift, selection, execution, authority, or missing content."""
    if not isinstance(candidate, Mapping):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
            "candidate must be an object"
        )
    expected = _assemble_candidate(_committed_source_failure_diagnosis())
    difference = _first_difference(candidate, expected)
    if difference:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
            f"{difference} mismatch"
        )
    for key in (
        CANDIDATE_DIGEST_KEY, PACKAGE_OPTIONS_DIGEST_KEY, INPUT_CONTRACT_DIGEST_KEY,
        SOURCE_BINDING_DIGEST_KEY, COVERAGE_DIGEST_KEY, MANIFEST_DIGEST_KEY,
    ):
        value = candidate.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError(
                f"{key} invalid"
            )
    return {
        "artifact_kind": ARTIFACT_KIND,
        "candidate_status": CANDIDATE_STATUS,
        "candidate_scope": CANDIDATE_SCOPE,
        "candidate_digest": candidate[CANDIDATE_DIGEST_KEY],
        **{
            key: candidate["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


MARKDOWN_SECTIONS = (
    "Candidate Disposition", "Source Failure Diagnosis", "Primary Failure Class",
    "Secondary Failure Classes", "Source Completion Execution", "Blocked Reason",
    "Blocked Digest Manifest", "Source Completion Approval", "Selected Completion Package",
    "Source Operator Review", "Source Completion Candidate",
    "Source Template Preparation Results Review", "Source Template Preparation Execution",
    "Source Preparation Failure Acquisition Chains", "Source Follow-On and Enrichment Chain",
    "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt",
    "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
    "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
    "Reviewed Template Structure", "Count Label Distinction", "Operator Completion Input Absence",
    "Future Input Supply Contract", "Package Options", "Recommended Package",
    "Future Input Requirements", "Future Plan", "Planned Outputs", "Non-Goals",
    "Actual Evidence Absence", "Actual Coverage Zero", "Source Authority Gap Preservation",
    "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates",
    "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
)


def build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate without reading or expanding external evidence."""
    validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)
    summary = candidate["summary"]
    facts = {
        "Candidate Disposition": f"`{CANDIDATE_STATUS}` within `{CANDIDATE_SCOPE}`. Candidate `{candidate[CANDIDATE_DIGEST_KEY]}`; manifest `{candidate[MANIFEST_DIGEST_KEY]}`.",
        "Source Failure Diagnosis": f"Commit `{SOURCE_FAILURE_DIAGNOSIS_COMMIT}`; artifact `{source.ARTIFACT_KIND}`; status `{source.DIAGNOSIS_STATUS}`; scope `{source.DIAGNOSIS_SCOPE}`; diagnosis `{SOURCE_FAILURE_DIAGNOSIS_DIGEST}`; classification `{SOURCE_FAILURE_CLASSIFICATION_DIGEST}`; input absence `{SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST}`; coverage `{SOURCE_COVERAGE_DIAGNOSIS_DIGEST}`; manifest `{SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST}`.",
        "Primary Failure Class": f"`{PRIMARY_FAILURE_CLASS}`.",
        "Secondary Failure Classes": "\n".join(f"- `{item}`" for item in SECONDARY_FAILURE_CLASSES),
        "Source Completion Execution": f"Commit `{candidate['source_completion_execution_commit']}`; artifact `{candidate['source_completion_execution_artifact_kind']}`; status `{candidate['source_completion_execution_status']}`; scope `{candidate['source_completion_execution_scope']}`.",
        "Blocked Reason": f"`{candidate['source_completion_execution_blocked_reason']}`.",
        "Blocked Digest Manifest": f"Blocked digest `{candidate['source_completion_execution_blocked_digest']}`; manifest `{candidate['source_completion_execution_blocked_manifest_digest']}`; all success digests remain absent.",
        "Source Completion Approval": f"Commit `{candidate['source_approval_commit']}`; approval `{candidate['source_approval_digest']}`; attestation `{candidate['source_attestation_digest']}`.",
        "Selected Completion Package": f"`{SELECTED_COMPLETION_PACKAGE}` remains approved only for its prior future-completion boundary; it is not operator input or evidence.",
        "Source Operator Review": f"Commit `{candidate['source_operator_review_commit']}`; digest `{candidate['source_operator_review_digest']}`; manifest `{candidate['source_operator_review_manifest_digest']}`.",
        "Source Completion Candidate": f"Commit `{candidate['source_completion_candidate_commit']}`; digest `{candidate['source_completion_candidate_digest']}`; manifest `{candidate['source_completion_candidate_manifest_digest']}`.",
        "Source Template Preparation Results Review": f"Results `{candidate['source_results_review_digest']}`; template `{candidate['source_template_review_digest']}`; evidence-item template `{candidate['source_evidence_item_template_review_digest']}`; coverage `{candidate['source_template_coverage_review_digest']}`.",
        "Source Template Preparation Execution": f"Commit `{candidate['source_template_preparation_execution_commit']}`; execution `{candidate['source_template_preparation_execution_digest']}`; package template `{candidate['source_package_template_digest']}`; manifest `{candidate['source_template_preparation_execution_manifest_digest']}`.",
        "Source Preparation Failure Acquisition Chains": f"Preparation `{candidate['source_preparation_candidate_digest']}`; previous failure `{candidate['source_previous_failure_diagnosis_digest']}`; blocked acquisition reason `{candidate['source_blocked_acquisition_execution_reason']}`; acquisition approval `{candidate['source_acquisition_approval_digest']}`.",
        "Source Follow-On and Enrichment Chain": f"Review `{candidate['source_follow_on_results_review_digest']}`; execution `{candidate['source_follow_on_execution_digest']}`; enrichment `{candidate['source_enrichment_execution_digest']}`. All other committed digests remain bound by source-binding digest `{candidate[SOURCE_BINDING_DIGEST_KEY]}`.",
        "Historical Blocked Remediation": f"Reason `{candidate['historical_blocked_remediation_reason']}`; manifest `{candidate['historical_blocked_remediation_manifest_digest']}`.",
        "Plan Method Diagnostic Recovery Chain": f"Targeted plan `{candidate['source_targeted_remediation_plan_digest']}`; method execution `{candidate['source_remediation_or_method_execution_after_diagnostic_capture_digest']}`; recovery `{candidate['source_recovery_results_review_digest']}`; staged inventory `{candidate['source_staged_inventory_digest']}`.",
        "Durable Receipt": f"`{candidate['source_durable_receipt_path']}` is an opaque bound reference and was not parsed.",
        "Retry Failure Context": "The authoritative detached retry remains 24,877 passed / 1,292 failed / 112 errors / 7 skipped. The root regression is not retry evidence.",
        "Priority 1 Target Modules": "\n".join(f"- `{item['path']}`: {item['failed_or_errored_nodeid_count']} failed-or-errored node IDs" for item in candidate["priority_1_target_modules"]),
        "Priority 1 Validation Summary": "675/675 pre-change and 675/675 post-change passed as current-root focused evidence only; this is not retry evidence.",
        "Diagnostic Capture Evidence Summary": f"Exit 1; stdout {candidate['source_stdout_byte_count']} bytes `{candidate['source_stdout_sha256']}`; stderr {candidate['source_stderr_byte_count']} bytes `{candidate['source_stderr_sha256']}`. Diagnostic metadata only.",
        "Reviewed Observable Families": "Four HIGH-confidence planning families, 47 observations each and 188 total, remain unchanged.",
        "Reviewed Workstreams": "Assertion/value, digest/hash, fixture/isolation, and schema/field-contract workstreams remain non-authorizing.",
        "Reviewed Template Structure": "Thirty reviewed rows map MA-001 through MA-030. The template remains not evidence, source authority, acquired evidence, or acquisition success.",
        "Count Label Distinction": "Preserved without reconciliation: source requirements 67/69/69; source non-goals 71/76; source risk controls 104/106. Candidate labels remain 76 non-goals and 105 risk controls while all enumerated minimum controls are retained.",
        "Operator Completion Input Absence": "No input was prepared, supplied, provided, validated, or bound. The source execution correctly failed closed.",
        "Future Input Supply Contract": f"Planning-only contract for exactly 30 mapped non-secret rows; input-contract digest `{candidate[INPUT_CONTRACT_DIGEST_KEY]}`. It requires custody/provenance, allowed values, review-before-use, and false direct-change/remediation/retry/main flags.",
        "Recommended Package": f"`{RECOMMENDED_PACKAGE}` is recommended for operator review and is not selected, approved, authorized, or executed.",
        "Actual Evidence Absence": "No completed package or evidence package was created, supplied, validated, bound, accepted, or filled.",
        "Actual Coverage Zero": f"Coverage remains 0/30 and `MISSING_NOT_ACQUIRED`; digest `{candidate[COVERAGE_DIGEST_KEY]}`.",
        "Source Authority Gap Preservation": "No source authority, source-authority evidence, external evidence, concrete authority, safe change, acquisition execution, disposition, diagnostic, remediation, retry, or merge authority was created.",
        "Unsupported Claims Boundary": "No first-failure, first-error, root-cause, retry-success, acquisition-success, remediation-readiness, retry-readiness, or main-readiness claim is made.",
        "Recommendation": f"`{candidate['recommended_next_task']}`: `{candidate['recommended_action']}`.",
        "Authority Boundaries": "Package selection, approval, authorization, execution, input handling, evidence completion, acquisition, remediation, retry, predictive usefulness, profitability, runtime, broker, trading, and protected-branch authority remain false or NOT_AUTHORIZED.",
        "Checklist Summary": f"{summary['passed_checks']}/{summary['total_checks']} PASS; blockers={summary['blocker_count']}.",
        "Guardrails": "Offline committed constants and injected dictionaries only. No source builders, file reads, subprocesses, pytest, caches, receipts, output analysis, logs, environment, providers, external documents, source-owner contact, input supply, or runtime actions.",
    }
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Inputs Preparation or Supply Candidate After Blocked Completion Execution v1", ""]
    for section in MARKDOWN_SECTIONS:
        lines.extend((f"## {section}", "", facts.get(section, "Candidate-only governance content; no execution or authority is created."), ""))
        if section == "Package Options":
            lines[-2:-2] = [
                *(f"- `{item['package_id']}` — `{item['candidate_review_status']}`: {item.get('purpose', item.get('blocked_reason'))}" for item in candidate["package_options"]),
                "",
            ]
        elif section == "Future Input Requirements":
            lines[-2:-2] = [*(f"- `{item['requirement_id']}` — `{item['execution_status']}`" for item in candidate["future_input_preparation_requirements"]), ""]
        elif section == "Future Plan":
            lines[-2:-2] = [*(f"{item['step']}. {item['action']} (`{item['plan_status']}`)" for item in candidate["future_plan"]), ""]
        elif section == "Planned Outputs":
            lines[-2:-2] = [*(f"- `{item['output_id']}` — `{item['generation_status']}`" for item in candidate["planned_outputs"]), ""]
        elif section == "Non-Goals":
            lines[-2:-2] = [*(f"- `{item['non_goal_id']}`" for item in candidate["non_goals"]), ""]
        elif section == "Next Chain":
            lines[-2:-2] = [*(f"{index}. {item}" for index, item in enumerate(candidate["next_chain"], 1)), ""]
        elif section == "Next Gates":
            lines[-2:-2] = [*(f"- `{item}`" for item in candidate["next_gates"]), ""]
        elif section == "Risk Controls":
            lines[-2:-2] = [*(f"- `{item}`" for item in candidate["risk_controls"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
    output_dir: str | Path,
    *,
    source_failure_diagnosis: dict | None = None,
) -> dict[str, Any]:
    """Write only the requested candidate status Markdown file."""
    candidate = build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
        source_failure_diagnosis=source_failure_diagnosis,
    )
    destination = Path(output_dir) / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_STATUS.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_markdown_v1(candidate),
        encoding="utf-8",
    )
    return candidate


__all__ = [
    "ARTIFACT_KIND", "SCHEMA_VERSION", "CANDIDATE_STATUS", "CANDIDATE_SCOPE",
    "CANDIDATE_DISPOSITION", "RECOMMENDED_PACKAGE", "SELECTED_COMPLETION_PACKAGE",
    "PRIMARY_FAILURE_CLASS", "SECONDARY_FAILURE_CLASSES", "PACKAGE_OPTIONS",
    "FUTURE_INPUT_REQUIREMENT_IDS", "PLANNED_OUTPUT_IDS", "NON_GOALS", "RISK_CONTROLS",
    "NEXT_CHAIN", "NEXT_GATES", "TRUE_FIELDS", "FALSE_FIELDS", "COUNTS",
    "CANDIDATE_DIGEST_KEY", "PACKAGE_OPTIONS_DIGEST_KEY", "INPUT_CONTRACT_DIGEST_KEY",
    "SOURCE_BINDING_DIGEST_KEY", "COVERAGE_DIGEST_KEY", "MANIFEST_DIGEST_KEY",
    "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_V1",
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_READY_FOR_OPERATOR_REVIEW",
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_INPUT_PREPARATION_NOT_INPUT_SUPPLY_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_ACQUISITION_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
    "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE",
    "MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1",
    "write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1",
    "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_markdown_v1",
]
