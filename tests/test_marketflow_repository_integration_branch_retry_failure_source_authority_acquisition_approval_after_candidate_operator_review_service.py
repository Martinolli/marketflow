from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionApprovalError


def _confirmations() -> dict:
    return {
        **deepcopy(service.ATTESTATION_VALUE_FIELDS),
        **{field: True for field in service.ATTESTATION_BOOLEAN_FIELDS},
    }


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations=_confirmations(),
    )


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
        operator_attestation=_attestation()
    )


def _reject(approval: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
            approval
        )


def test_attestation_builder_creates_all_required_flat_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_source_authority_acquisition_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1
    assert attestation["operator_attestation_version"] == "v1"
    assert all(attestation[field] == value for field, value in service.ATTESTATION_VALUE_FIELDS.items())
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)
    assert len(attestation[service.ATTESTATION_DIGEST_KEY]) == 64


def test_approval_builds_offline_without_prohibited_public_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("prohibited source builder invoked")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1",
        forbidden,
    )
    approval = _build()
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["approval_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("approval_status", service.APPROVAL_STATUS),
        ("approval_scope", service.APPROVAL_SCOPE),
        ("selected_source_authority_acquisition_package", service.SELECTED_PACKAGE),
        ("source_operator_review_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_operator_review_status", service.source.REVIEW_STATUS),
        ("source_operator_review_scope", service.source.REVIEW_SCOPE),
        ("source_operator_review_commit", service.SOURCE_OPERATOR_REVIEW_COMMIT),
        ("source_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_candidate_review_digest", service.SOURCE_CANDIDATE_REVIEW_DIGEST),
        ("source_scope_review_digest", service.SOURCE_SCOPE_REVIEW_DIGEST),
        ("source_mapping_review_digest", service.SOURCE_MAPPING_REVIEW_DIGEST),
        ("source_operator_review_manifest_digest", service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST),
        ("source_follow_on_results_review_commit", "c3b894179fb89c14d95ba43a72393e943ff44199"),
        ("source_follow_on_results_review_digest", "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"),
        ("source_acquisition_candidate_review_digest", "6c122b5bb1489861a969efdf9ab9c36f4ce9a799b7ecf76b791d41a550f653e5"),
        ("source_acquisition_scope_review_digest", "713aefda1df0916f1ddd25084751cb3f2a23ddc9679e16ff4827409678092d0e"),
        ("source_missing_authority_mapping_review_digest", "83104c9ff91bceed69f368f194cf454629f3530e0c6e8dabed83099677a7b381"),
        ("source_follow_on_results_review_manifest_digest", "be88a6b0679378ca52cc1489a173387e01f0acbbd5c4888aa4a345e1a46c6cb2"),
        ("source_follow_on_execution_commit", "a5a78331058c37b348108f9599fec6a24763bf06"),
        ("source_follow_on_execution_after_results_review_digest", "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208"),
        ("source_authority_acquisition_candidate_digest", "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91"),
        ("source_authority_acquisition_scope_digest", "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8"),
        ("source_missing_authority_to_source_evidence_mapping_digest", "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334"),
        ("source_follow_on_execution_manifest_digest", "56a6d540ae16cb9670696255c775fb690b9273c13c120cd822facf4a8bb85347"),
        ("source_follow_on_approval_digest", "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6"),
        ("source_follow_on_candidate_operator_review_digest", "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"),
        ("source_follow_on_candidate_digest", "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"),
        ("source_results_review_digest", "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"),
        ("source_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
        ("source_authority_enrichment_plan_digest", "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94"),
        ("source_missing_authority_inventory_digest", "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8"),
        ("source_workstream_authority_mapping_digest", "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd"),
        ("source_execution_manifest_digest", "8a544aa173597f2c24e531a69f4eab2264fb1aa0796a67f87b00af291e6109d6"),
        ("source_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
        ("source_historical_operator_review_digest", "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51"),
        ("source_candidate_digest", "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c"),
        ("source_remediation_execution_after_plan_results_review_failure_diagnosis_digest", "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"),
        ("source_blocked_execution_commit", "65aab2f4a5cc699cc630756c4142dee12f96c838"),
        ("source_blocked_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("source_blocked_manifest_digest", "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"),
        ("source_remediation_execution_approval_after_plan_results_review_digest", "2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1"),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa"),
        ("source_targeted_remediation_plan_review_digest", "7570033ff0aeca33bc6cc5f8fbfc3a462d50cb1d3c5537421f6dbd7aefb3d115"),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c"),
        ("source_targeted_remediation_plan_digest", "2d7ffac9fc3cc04f0bfb823ef81f254005adaee7a600ccb6e3444b7f3dec91db"),
        ("source_remediation_or_method_results_review_after_diagnostic_capture_digest", "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"),
        ("source_remediation_or_method_execution_after_diagnostic_capture_digest", "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88"),
        ("source_receipt_recovery_or_recapture_results_review_digest", "427d2a76afcec7c8b9647a0f0c19b6037e5a451b0f70fad1a5025afc266946ba"),
        ("source_receipt_recovery_or_recapture_execution_digest", "25a70331c48eedeb62c6f8532dba0e1b782904ff4b753934c2fd12ccbec47e46"),
        ("source_receipt_recovery_or_recapture_receipt_digest", "dfd7f50c4065e759ccfee0f160c97177f4d9a1cfe977fb6db1ce240f8ad3345b"),
        ("source_durable_receipt_path", "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"),
        ("source_planning_execution_digest", "846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b"),
        ("source_complete_29_row_binding_digest", "36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7"),
        ("source_materialized_payload_digest", "1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7"),
        ("source_recovery_detail_digest", "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"),
        ("source_module_grouping_digest", "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"),
        ("source_staged_inventory_digest", "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"),
    ],
)
def test_approval_binds_identity_and_source_chain(field: str, expected: object) -> None:
    assert _build()[field] == expected


def test_approved_package_is_future_execution_only() -> None:
    package = _build()["approved_package"]
    assert package["package_id"] == service.SELECTED_PACKAGE
    assert package["source_review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["approval_status"] == "APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY"
    assert package["selected"] is True
    assert package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_approval_true_facts(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_approval_closed_boundaries(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_future_execution_permissions(field: str) -> None:
    assert _build()[field] is True
    assert _build()["future_execution_boundary"][field] is True


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_future_execution_prohibitions(field: str) -> None:
    assert _build()[field] is False
    assert _build()["future_execution_boundary"][field] is False


def test_approved_requirements_plan_outputs_and_packages() -> None:
    approval = _build()
    requirements = approval["approved_future_requirements"]
    plan = approval["approved_future_plan"]
    outputs = approval["planned_outputs"]
    assert len(requirements) == 51
    assert {item["requirement_id"] for item in requirements} == set(service.source.FUTURE_REQUIREMENT_IDS)
    assert {item["approval_status"] for item in requirements} == {"APPROVED_FOR_FUTURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY"}
    assert {item["execution_status"] for item in requirements} == {"NOT_EXECUTED"}
    assert len(plan) == 13 and [item["step_id"] for item in plan] == list(range(1, 14))
    assert {item["execution_status"] for item in plan} == {"NOT_EXECUTED"}
    assert len(outputs) == 28 and {item["status"] for item in outputs} == {"AUTHORIZED_NOT_GENERATED"}
    assert {item["output_id"] for item in outputs} == set(service.PLANNED_OUTPUT_IDS)
    assert len(approval["supporting_packages"]) == 5
    assert len(approval["blocked_packages"]) == 6
    assert {item["approval_status"] for item in approval["supporting_packages"]} == {"AVAILABLE_NOT_SELECTED"}
    assert {item["approval_status"] for item in approval["blocked_packages"]} == {"BLOCKED_NOT_APPROVED"}
    assert all(not item[field] for item in approval["supporting_packages"] + approval["blocked_packages"] for field in ("selected", "approved", "authorized", "executed"))


def test_source_context_counts_states_and_boundaries() -> None:
    approval = _build()
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["retry_failure_context"]["first_result_authoritative"] is True
    assert approval["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert len(approval["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in approval["priority_1_target_modules"]) == 612
    assert approval["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["not_retry_evidence"] is True
    diagnostic = approval["diagnostic_capture_evidence_summary"]
    assert (diagnostic["exit_code"], diagnostic["stdout_byte_count"], diagnostic["stderr_byte_count"]) == (1, 1231380, 0)
    assert diagnostic["stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert diagnostic["stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert diagnostic["diagnostic_only"] is True
    assert len(approval["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in approval["reviewed_observable_failure_families"]) == 188
    assert {item["confidence"] for item in approval["reviewed_observable_failure_families"]} == {"HIGH"}
    assert len(approval["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in approval["reviewed_workstreams"])


def test_candidate_scope_mapping_and_requirement_counts() -> None:
    approval = _build()
    candidate = approval["source_authority_acquisition_candidate_review"]
    assert candidate["candidate_status"] == "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED"
    assert candidate["approved"] is False and candidate["executed"] is False
    assert candidate["authority_acquired"] is False and candidate["evidence_acquired"] is False
    scope = approval["acquisition_scope_sections_review"]
    mapping = approval["missing_authority_to_source_evidence_mapping_review"]
    inventory = approval["acceptable_source_artifact_inventory_review"]
    assert scope["section_count"] == 4 and len(scope["sections"]) == 4
    assert mapping["mapped_item_count"] == 30 and len(mapping["items"]) == 30
    assert mapping["all_missing_not_acquired"] is True
    assert mapping["all_authority_acquired_now_false"] is True
    assert mapping["all_evidence_acquired_now_false"] is True
    assert mapping["all_direct_change_authorized_false"] is True
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in mapping["items"])
    assert all(item["authority_acquired_now"] is False and item["evidence_acquired_now"] is False and item["direct_change_authorized"] is False for item in mapping["items"])
    assert inventory["artifact_type_count"] == 13 and len(inventory["artifact_types"]) == 13
    assert approval["operator_provided_evidence_requirements_review"]["requirement_count"] == 10
    assert approval["evidence_custody_and_digest_requirements_review"]["requirement_count"] == 6
    assert approval["candidate_results_review_requirements_review"]["requirement_count"] == 16


def test_next_chain_gates_risks_summary_and_checklist() -> None:
    approval = _build()
    assert approval["next_chain"] == list(service.NEXT_CHAIN) and len(approval["next_chain"]) == 8
    assert approval["next_gates"] == list(service.NEXT_GATES) and len(approval["next_gates"]) == 12
    assert approval["risk_controls"] == list(service.RISK_CONTROLS) and len(approval["risk_controls"]) == 95
    assert approval["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(approval["checklist"])
    assert approval["summary"]["passed_checks"] == len(approval["checklist"])
    assert approval["summary"]["failed_checks"] == 0 and approval["summary"]["blocker_count"] == 0
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"
    assert {approval[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_approval_digest_is_deterministic_and_validator_accepts() -> None:
    first, second = _build(), _build()
    assert first[service.APPROVAL_DIGEST_KEY] == second[service.APPROVAL_DIGEST_KEY]
    assert len(first[service.APPROVAL_DIGEST_KEY]) == 64
    result = service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(first)
    assert result["approval_digest"] == first[service.APPROVAL_DIGEST_KEY]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "schema_version", "approval_status", "approval_scope",
        "selected_source_authority_acquisition_package", "source_operator_review_commit",
        "source_operator_review_digest", "source_candidate_review_digest", "source_scope_review_digest",
        "source_mapping_review_digest", "source_operator_review_manifest_digest",
        "source_follow_on_results_review_digest", "source_acquisition_candidate_review_digest",
        "source_acquisition_scope_review_digest", "source_missing_authority_mapping_review_digest",
        "source_follow_on_execution_after_results_review_digest", "source_authority_acquisition_candidate_digest",
        "source_authority_acquisition_scope_digest", "source_missing_authority_to_source_evidence_mapping_digest",
        "source_follow_on_approval_digest", "source_follow_on_candidate_operator_review_digest",
        "source_follow_on_candidate_digest", "source_results_review_digest", "source_execution_digest",
        "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest",
        "source_workstream_authority_mapping_digest", "source_approval_digest",
        "source_historical_operator_review_digest", "source_candidate_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit", "source_blocked_reason", "source_blocked_manifest_digest",
        "primary_failure_class", "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest", "source_durable_receipt_path",
        "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest",
        "source_module_grouping_digest", "source_staged_inventory_digest",
        "recommended_next_task", "predictive_usefulness", "runtime_use", service.APPROVAL_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_scalar(field: str) -> None:
    approval = _build()
    approval[field] = "changed"
    _reject(approval)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_changed(field: str) -> None:
    approval = _build()
    approval[field] = False
    _reject(approval)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_changed(field: str) -> None:
    approval = _build()
    approval[field] = True
    _reject(approval)


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_validator_rejects_future_permission_removed(field: str) -> None:
    approval = _build()
    approval[field] = False
    _reject(approval)


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_validator_rejects_future_prohibition_opened(field: str) -> None:
    approval = _build()
    approval[field] = True
    _reject(approval)


@pytest.mark.parametrize(
    "field",
    [
        "approved_future_requirements", "approved_future_plan", "planned_outputs",
        "supporting_packages", "blocked_packages", "next_chain", "next_gates",
        "risk_controls", "checklist", "summary",
    ],
)
def test_validator_rejects_missing_structured_evidence(field: str) -> None:
    approval = _build()
    approval[field] = [] if isinstance(approval[field], list) else {}
    _reject(approval)


@pytest.mark.parametrize(
    "field",
    [
        "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families",
        "reviewed_workstreams", "source_authority_acquisition_candidate_review",
        "acquisition_scope_sections_review", "missing_authority_to_source_evidence_mapping_review",
        "acceptable_source_artifact_inventory_review", "operator_provided_evidence_requirements_review",
        "evidence_custody_and_digest_requirements_review", "candidate_results_review_requirements_review",
    ],
)
def test_validator_rejects_changed_source_context(field: str) -> None:
    approval = _build()
    approval[field] = [] if isinstance(approval[field], list) else {}
    _reject(approval)


def test_validator_rejects_missing_secondary_failure_class() -> None:
    approval = _build()
    approval["secondary_failure_classes"].pop()
    _reject(approval)


@pytest.mark.parametrize("field", tuple(service.ATTESTATION_VALUE_FIELDS))
def test_attestation_builder_rejects_wrong_bound_value(field: str) -> None:
    confirmations = _confirmations()
    confirmations[field] = "changed"
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1(
            operator_reference="TEST_OPERATOR",
            operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


@pytest.mark.parametrize("field", service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_builder_rejects_missing_closed_confirmation(field: str) -> None:
    confirmations = _confirmations()
    confirmations.pop(field)
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1(
            operator_reference="TEST_OPERATOR",
            operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


@pytest.mark.parametrize(
    "overrides",
    [
        {"operator_reference": ""},
        {"operator_attestation_timestamp_utc": "not-a-date"},
        {"operator_attestation_phrase": "wrong"},
        {"selected_source_authority_acquisition_package": "wrong"},
        {"operator_decision": "wrong"},
    ],
)
def test_attestation_builder_rejects_invalid_identity(overrides: dict) -> None:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_source_authority_acquisition_package": service.SELECTED_PACKAGE,
        "operator_decision": service.OPERATOR_DECISION,
        "operator_confirmations": _confirmations(),
    }
    values.update(overrides)
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_attestation_v1(**values)


def test_builder_accepts_exact_injected_source_review_without_mutating_it() -> None:
    source_review = service._committed_source_operator_review()
    original = deepcopy(source_review)
    approval = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
        source_operator_review=source_review, operator_attestation=_attestation()
    )
    assert approval["source_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert source_review == original


def test_builder_rejects_changed_injected_source_review() -> None:
    source_review = service._committed_source_operator_review()
    source_review[service.source.OPERATOR_REVIEW_DIGEST_KEY] = "changed"
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
            source_operator_review=source_review, operator_attestation=_attestation()
        )


def test_validator_rejects_attestation_digest_mutation() -> None:
    approval = _build()
    approval["operator_attestation"][service.ATTESTATION_DIGEST_KEY] = "0" * 64
    _reject(approval)


def test_markdown_includes_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Approval After Candidate Operator Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_status_document(tmp_path) -> None:
    approval = service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert approval["artifact_kind"] == service.ARTIFACT_KIND


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(tmp_path, protected: str) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1(
            tmp_path / protected, operator_attestation=_attestation()
        )
