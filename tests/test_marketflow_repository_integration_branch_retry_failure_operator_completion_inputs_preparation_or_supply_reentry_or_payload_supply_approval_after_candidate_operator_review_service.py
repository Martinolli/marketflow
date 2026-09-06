from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_service
    as service,
)


def build():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1()


def reject(mutator):
    artifact = build()
    mutator(artifact)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(artifact)


def test_builds_offline_from_committed_constants(monkeypatch):
    monkeypatch.setattr(service.source, "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1", lambda **_: (_ for _ in ()).throw(AssertionError("source builder called")))
    assert build()["created_offline"] is True


@pytest.mark.parametrize("key, expected", [
    ("artifact_kind", service.ARTIFACT_KIND),
    ("schema_version", service.SCHEMA_VERSION),
    ("approval_status", service.APPROVAL_STATUS),
    ("approval_scope", service.APPROVAL_SCOPE),
    ("selected_operator_completion_inputs_reentry_or_payload_supply_package", service.SELECTED_PACKAGE),
    ("selected_package_approved_for_future_execution_only", True),
    ("selected_package_executed", False),
    ("source_operator_review_commit", service.SOURCE_OPERATOR_REVIEW_COMMIT),
    ("source_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
    ("source_package_options_review_digest", service.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST),
    ("source_future_requirements_review_digest", service.SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST),
    ("source_future_contract_review_digest", service.SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST),
    ("source_binding_review_digest", service.SOURCE_BINDING_REVIEW_DIGEST),
    ("source_operator_review_manifest_digest", service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST),
    ("source_candidate_commit", "052b9f9002ba774361ebc099eea52be6cdbc7e62"),
    ("source_candidate_digest", "f895767f7e54d97bbcf9ef7f44562f974505f6f32ebab2e66257e4d28c2dbd1a"),
    ("source_candidate_package_options_digest", "82386fc8e116417e5fe9f394bfea12655e4e2c0185718dfab23cb893a04a144c"),
    ("source_candidate_future_requirements_digest", "7760e95b3996820e5d39a4c12e800687fb25a21332eb8a4e30ec7899236caa31"),
    ("source_candidate_future_contract_digest", "4d21b3a0b885efe2277e64190630a53cdab6622fb9013c6d0f13d48dd447a625"),
    ("source_candidate_source_binding_digest", "fc50eed1d4caa7053450a54d0b6e49c96bf4c2e1fdfaea0906137b69b314bd2c"),
    ("source_candidate_manifest_digest", "2b51213f447ca52cfe1cd74339a681fb1ffcc879208342fb1f96c158013af6aa"),
    ("source_failure_diagnosis_commit", "0bcec575d04c103bea4da1c09738f69aa5fe2cc7"),
    ("source_failure_diagnosis_digest", "b7fb8275d1e156e5ce4b0ef442934d1916c3ffa2b3871f8070ceef194da1f4d6"),
    ("source_failure_classification_digest", "08b02ede52fa4edcdac89bbe466b14c671053c146b568939910c00410639024b"),
    ("source_input_absence_diagnosis_digest", "b86a8c047d2b579b69344e0f50b6f42d150194b218b5b0a45e4f2bd1fd3cc122"),
    ("source_failure_diagnosis_source_binding_review_digest", "f6afb43954adf7f30c8aaf440b1d6d9576f305c0e72f727438e3f10af938b49b"),
    ("source_coverage_diagnosis_digest", "ce7b3278901c8cf85c3c0613d7d8508a6bd57ce9167f598991466ec747f98bd8"),
    ("source_failure_diagnosis_manifest_digest", "91eef3ab2c5f743ddd87de1b525d3126917707f1631017184f08591a300e2024"),
    ("source_execution_commit", "3cb60e016592480f2f23d977952ee5fd4ca3fd21"),
    ("source_blocked_reason", "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"),
    ("source_blocked_digest", "0316a49a2def7e5f922e4e43fc83c9a7e3b1db4a5233f1a4996675eab53918dd"),
    ("source_source_binding_digest", "d7047b7205b3b2758d1388566ca2afdd55a47895ff9dd9508daca26066f885ef"),
    ("source_input_absence_digest", "33db19e44c27eb521720336830d75d804fdfe5757c630853159b3b879601c3e2"),
    ("source_coverage_digest", "35a3561d865b5ed0c50a854456d5f03a6b05a5db15b4018a07adb789dbb26ae8"),
    ("source_blocked_manifest_digest", "496a3be007b31008ca6ecdfc3b501cbd7ffe8d59ef56b2f858a92c7f4489969c"),
    ("source_approval_commit", "6623e6a6acb0a8da85fee15a29a52606a7fc6af1"),
    ("source_approval_digest", "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72"),
    ("source_attestation_digest", "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af"),
    ("source_prior_operator_review_commit", "2efc22338250f9de88e76fbf6381796c82f817df"),
    ("source_prior_candidate_commit", "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1"),
    ("source_prior_completion_failure_diagnosis_commit", "07276fc4b171179eb7210ce679ba2a9bdbd17e8c"),
    ("source_completion_execution_commit", "945776b2164969e067d8dcc4809128282d3b1287"),
    ("source_completion_execution_blocked_reason", "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED"),
    ("source_completion_approval_commit", "40bee1289543bb07e64e383eb2e1c61d83615bd5"),
    ("source_completion_candidate_operator_review_commit", "d71bfb14a656592ab637d94d9dd30d73912104b0"),
    ("source_completion_candidate_commit", "7af6b1b5ad223f92da0997e2b7abcb73543470df"),
    ("source_template_preparation_results_review_commit", "268c84d7ef4ed550bb38f07670247540590885f6"),
    ("source_template_preparation_execution_commit", "a39332feb29a23612ee51cb45e8d5663b144c638"),
    ("source_durable_receipt_path", "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"),
    ("retry_pytest_passed_count", 24877),
    ("retry_pytest_failed_count", 1292),
    ("retry_pytest_error_count", 112),
    ("retry_pytest_skipped_count", 7),
    ("priority_1_total_nodeids", 612),
    ("top_10_count_sum", 1069),
    ("failed_or_errored_nodeids_count", 1404),
    ("module_summary_module_count", 29),
    ("reviewed_template_row_count", 30),
    ("actual_covered_missing_authority_item_count", 0),
    ("actual_uncovered_missing_authority_item_count", 30),
    ("missing_authority_items_status", "MISSING_NOT_ACQUIRED"),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
])
def test_core_identity_and_binding_values(key, expected):
    assert build()[key] == expected


def test_source_success_and_prepared_input_digests_remain_absent():
    artifact = build()
    assert artifact["source_success_digests_absent"] is True
    assert artifact["source_success_execution_digest"] is None
    assert artifact["source_prepared_operator_completion_inputs_digest"] is None
    assert artifact["source_prepared_operator_completion_inputs_manifest_digest"] is None


def test_primary_and_secondary_failure_classes_are_preserved():
    artifact = build()
    assert artifact["primary_failure_class"] == service.source.source.PRIMARY_FAILURE_CLASS
    assert tuple(artifact["secondary_failure_classes"]) == service.source.source.SECONDARY_FAILURE_CLASSES
    assert len(artifact["secondary_failure_classes"]) == 9


def test_execution_and_historical_digest_chains_are_exact():
    artifact = build()
    expected = {
        "source_execution_artifact_kind": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_V1",
        "source_execution_status": "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_OPERATOR_INPUTS_UNAVAILABLE_OR_BOUNDARY_FAILURE",
        "source_execution_scope": "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_ONLY_INPUT_PREPARATION_OR_SUPPLY_FROM_EXPLICIT_NON_SECRET_OPERATOR_INPUTS_NOT_EVIDENCE_PACKAGE_COMPLETION_NOT_SOURCE_AUTHORITY_ACQUISITION_NOT_EVIDENCE_VALIDATION_NOT_EVIDENCE_BINDING_NOT_NO_CHANGE_DISPOSITION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN",
        "source_prior_operator_review_digest": "82e0286d511ced1721346d3049ed434f37d953eba679e71585524529e7864b4a",
        "source_prior_package_options_review_digest": "a649f00a011ffd85e7bb08eea6a0034a42a75847d6460f4bfbb81b6a48fb0ea3",
        "source_prior_input_contract_review_digest": "78c3a6ff08102a49434486c3683ff5d3be63c798932b4d6ae3d47ab66e17da94",
        "source_prior_binding_review_digest": "4f4ed7e71d0b70fdeedbb3c39361cb8bcabb4eceab156dcf12ce406581c34d99",
        "source_prior_operator_review_coverage_digest": "35a3561d865b5ed0c50a854456d5f03a6b05a5db15b4018a07adb789dbb26ae8",
        "source_prior_operator_review_manifest_digest": "e8587a7c06142bbee9defbdeb7f91d702914186f0da0cb3c035e0074284fcbfb",
        "source_prior_candidate_digest": "41a2df4be129a88b829439dadc3e0969715853944068f73800fd673720f02ca8",
        "source_prior_candidate_package_options_digest": "28ec7b372252beb98b6e2b939c70545d7aac66c40adaef6099c935998ec625b8",
        "source_prior_candidate_input_contract_digest": "a6086f4bae684216a7dd34233f1cb68ed165523dcfbddb6bd77d3d030a055bd9",
        "source_prior_candidate_source_binding_digest": "78b01abcb34b4e88951587eaccfbc5d500ffece96b51fd54a849a06d7389ced5",
        "source_prior_candidate_manifest_digest": "c1bfffd4995beef0e4f65e74b8a1068b517caa67aece00c6b0104c5cf643f937",
        "source_prior_completion_failure_diagnosis_digest": "3789d82ea1ef74aed2a6d7d7b1404254c0b5672eaf3c8080095ec21907e50759",
        "source_prior_completion_failure_classification_digest": "e8086ac688202f1a9f850a605c6ae2bbf942413b8bbfab2730aa062edfd2d16d",
        "source_prior_operator_input_absence_diagnosis_digest": "607a9745ff0c76af61af884e4696138354446e2a7dcfbfd362ec508bbfb1b38e",
        "source_prior_completion_failure_manifest_digest": "f354ae2af92e1d9fb1c29a409868747e075953969dec69f5aad69b4f8f7f37cc",
        "source_completion_execution_blocked_digest": "5fe3269b5787730da7d0287029af15956e9efae13f436c58c94e93ff7160b2c1",
        "source_completion_execution_blocked_manifest_digest": "97b42143837d78ea6dba2d13a53cad5f42ffdcf8ea3f82d55c6ab521a9564cc6",
        "source_completion_approval_digest": "f6c37c0a7c64487cdf9adb218f8d12b8c0a2dacc4d4c1debf96105d1b5ee954c",
        "source_completion_approval_attestation_digest": "5434cbb4c94d22f1e4fefb3efc0e6e651401a22d6217d4c118638fa6d38dc714",
        "source_completion_candidate_operator_review_digest": "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663",
        "source_completion_candidate_digest": "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207",
        "source_template_preparation_results_review_digest": "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332",
        "source_template_preparation_execution_digest": "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3",
        "source_package_template_digest": "fb406078ca1a1199a430dd836050f9b198373c1f46c19cb5ee899ffe7e975a9a",
        "source_evidence_item_template_digest": "820cdf4c4a758b1d24ad0112fa6a1b05a8e6a330dc717c3564be4434b00af6e9",
        "source_preparation_checklist_digest": "4f965c0e7072dc6061ed3731e0eb7a639e117780c09544a6031663d6a6959605",
        "source_template_preparation_execution_manifest_digest": "272cadca012100d25e5628f09a3e91f8919a9fb80b8433ca2841a28d65a76a39",
        "source_template_approval_digest": "e7f1d8a5ae413ca0f971257e13554a63b3ee95e942e156adb5b204cbcc378cbd",
        "source_preparation_candidate_digest": "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391",
        "source_blocked_acquisition_execution_manifest_digest": "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3",
        "source_acquisition_approval_digest": "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69",
        "source_follow_on_results_review_digest": "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb",
        "source_enrichment_execution_digest": "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c",
        "source_missing_authority_inventory_digest": "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8",
        "historical_blocked_remediation_manifest_digest": "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002",
        "source_failure_family_classification_digest": "3e3f2409315228bc88c23fb02dfdf3dbea4724d30356f0a4548243105a49dac1",
        "source_staged_inventory_digest": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
    }
    for key, value in expected.items():
        assert artifact[key] == value


def test_exact_default_attestation_is_bound():
    artifact = build()
    assert artifact["operator_attestation"] == service.DEFAULT_OPERATOR_ATTESTATION
    assert artifact["operator_attestation"]["operator_id"] == "TEST_OPERATOR"
    assert artifact["operator_attestation"]["approval_timestamp_utc"] == "2026-09-06T00:00:00Z"


@pytest.mark.parametrize("key", list(service.DEFAULT_OPERATOR_ATTESTATION))
def test_attestation_rejects_changed_required_value(key):
    value = deepcopy(service.DEFAULT_OPERATOR_ATTESTATION)
    value[key] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(operator_attestation=value)


def test_attestation_rejects_unexpected_secret_like_field():
    value = deepcopy(service.DEFAULT_OPERATOR_ATTESTATION)
    value["api_key"] = "not-a-real-secret"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(operator_attestation=value)


def test_source_operator_review_injection_is_validated():
    assert build()["source_operator_review_bound"] is True
    changed = deepcopy(service.SOURCE_OPERATOR_REVIEW_BINDINGS)
    changed["source_operator_review_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(source_operator_review=changed)


def test_selected_supporting_and_blocked_package_dispositions():
    rows = build()["approved_package_options"]
    assert len(rows) == 12
    assert rows[0]["selected"] is rows[0]["approved"] is rows[0]["authorized"] is True
    assert rows[0]["executed"] is False
    assert all(not row["selected"] and not row["approved"] and not row["authorized"] for row in rows[1:])
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in rows[1:7])
    assert all(row["approval_status"] == "BLOCKED_NOT_APPROVED" for row in rows[7:])


def test_future_requirements_contract_plan_and_outputs_are_not_executed():
    artifact = build()
    assert len(artifact["approved_future_requirements"]) == 62
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in artifact["approved_future_requirements"])
    contract = artifact["approved_future_payload_supply_contract"]
    assert contract["contract_status"] == "APPROVED_PLANNING_ONLY_NOT_SUPPLIED"
    assert contract["operator_input_supplied"] is False
    assert contract["execution_status"] == "NOT_EXECUTED"
    assert len(artifact["approved_future_plan"]) == 15
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in artifact["approved_future_plan"])
    assert len(artifact["authorized_planned_outputs"]) == 34
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for row in artifact["authorized_planned_outputs"])


def test_observable_workstream_template_and_mapping_context_is_preserved():
    artifact = build()
    assert len(artifact["reviewed_observable_failure_families"]) == 4
    assert sum(row["observable_evidence_count"] for row in artifact["reviewed_observable_failure_families"]) == 188
    assert all(row["confidence"] == "HIGH" for row in artifact["reviewed_observable_failure_families"])
    assert len(artifact["reviewed_workstreams"]) == 4
    assert artifact["reviewed_template_structure"]["template_only"] is True
    assert len(artifact["missing_authority_mapping"]) == 30
    assert all(row["current_status"] == "MISSING_NOT_ACQUIRED" for row in artifact["missing_authority_mapping"])


@pytest.mark.parametrize("key", service.TRUE_FIELDS)
def test_required_true_boundaries(key):
    assert build()[key] is True


@pytest.mark.parametrize("key", service.FALSE_FIELDS)
def test_required_false_boundaries(key):
    assert build()[key] is False


@pytest.mark.parametrize("key", [
    service.APPROVAL_DIGEST_KEY,
    service.ATTESTATION_DIGEST_KEY,
    service.PACKAGE_OPTIONS_DIGEST_KEY,
    service.FUTURE_REQUIREMENTS_DIGEST_KEY,
    service.FUTURE_CONTRACT_DIGEST_KEY,
    service.SOURCE_BINDING_DIGEST_KEY,
    service.MANIFEST_DIGEST_KEY,
])
def test_digests_are_deterministic_sha256(key):
    first, second = build(), build()
    assert first[key] == second[key]
    assert len(first[key]) == 64
    int(first[key], 16)


def test_checklist_passes_without_blockers():
    artifact = build()
    assert artifact["summary"]["passed_checks"] == artifact["summary"]["total_checks"]
    assert artifact["summary"]["failed_checks"] == 0
    assert artifact["summary"]["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in artifact["checklist"])


@pytest.mark.parametrize("mutator", [
    lambda x: x.__setitem__("artifact_kind", "wrong"),
    lambda x: x.__setitem__("approval_status", "wrong"),
    lambda x: x.__setitem__("approval_scope", "wrong"),
    lambda x: x.__setitem__("source_operator_review_digest", "0" * 64),
    lambda x: x.__setitem__("source_candidate_digest", "0" * 64),
    lambda x: x.__setitem__("source_failure_diagnosis_digest", "0" * 64),
    lambda x: x.__setitem__("source_execution_commit", "0" * 40),
    lambda x: x.__setitem__("source_execution_status", "wrong"),
    lambda x: x.__setitem__("source_execution_scope", "wrong"),
    lambda x: x.__setitem__("source_blocked_reason", "wrong"),
    lambda x: x.__setitem__("source_blocked_digest", "0" * 64),
    lambda x: x.__setitem__("source_success_execution_digest", "1" * 64),
    lambda x: x.__setitem__("primary_failure_class", "wrong"),
    lambda x: x["secondary_failure_classes"].pop(),
    lambda x: x.__setitem__("source_approval_digest", "0" * 64),
    lambda x: x.__setitem__("selected_operator_completion_inputs_reentry_or_payload_supply_package", "wrong"),
    lambda x: x.__setitem__("selected_package_executed", True),
    lambda x: x["operator_attestation"].__setitem__("operator_id", "changed"),
    lambda x: x["approved_package_options"][1].__setitem__("selected", True),
    lambda x: x["approved_package_options"][7].__setitem__("approved", True),
    lambda x: x["approved_future_requirements"][0].__setitem__("execution_status", "EXECUTED"),
    lambda x: x["approved_future_payload_supply_contract"].__setitem__("operator_input_supplied", True),
    lambda x: x["approved_future_plan"][0].__setitem__("execution_status", "EXECUTED"),
    lambda x: x["authorized_planned_outputs"][0].__setitem__("authorization_status", "GENERATED"),
    lambda x: x.__setitem__("durable_receipt_not_parsed", False),
    lambda x: x.__setitem__("retry_pytest_failed_count", 0),
    lambda x: x.__setitem__("priority_1_total_nodeids", 0),
    lambda x: x.__setitem__("source_exit_code", 0),
    lambda x: x["reviewed_observable_failure_families"].pop(),
    lambda x: x["reviewed_workstreams"].pop(),
    lambda x: x.__setitem__("actual_covered_missing_authority_item_count", 1),
    lambda x: x.__setitem__("missing_authority_items_status", "ACQUIRED"),
    lambda x: x.__setitem__("operator_completion_inputs_prepared", True),
    lambda x: x.__setitem__("operator_payload_supply_mechanism_created", True),
    lambda x: x.__setitem__("operator_source_authority_evidence_package_created", True),
    lambda x: x.__setitem__("source_authority_evidence_acquired", True),
    lambda x: x.__setitem__("remediation_execution_performed", True),
    lambda x: x.__setitem__("production_code_modified", True),
    lambda x: x.__setitem__("pytest_performed_in_approval", True),
    lambda x: x.__setitem__("cache_read_in_approval", True),
    lambda x: x.__setitem__("diagnostic_receipt_parsed_in_approval", True),
    lambda x: x.__setitem__("source_owners_contacted", True),
    lambda x: x.__setitem__("provider_requests_made_in_approval", True),
    lambda x: x.__setitem__("root_cause_claimed", True),
    lambda x: x.__setitem__("ready_for_main_merge_approval", True),
    lambda x: x.__setitem__("runtime_use", "AUTHORIZED"),
    lambda x: x.__setitem__("outputs", []),
    lambda x: x.__setitem__("next_chain", []),
    lambda x: x.__setitem__("risk_controls", []),
    lambda x: x.__setitem__(service.APPROVAL_DIGEST_KEY, "0" * 64),
])
def test_validator_rejects_boundary_tampering(mutator):
    reject(mutator)


def test_validator_accepts_valid_approval():
    summary = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(build())
    assert summary["blocker_count"] == 0


def test_markdown_contains_every_required_section():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_markdown_v1(build())
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.APPROVAL_STATUS in markdown
    assert service.SELECTED_PACKAGE in markdown


def test_writer_writes_only_status_markdown(tmp_path: Path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].suffix == ".md"
    assert artifact["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_approval_after_candidate_operator_review_v1(Path(protected))
