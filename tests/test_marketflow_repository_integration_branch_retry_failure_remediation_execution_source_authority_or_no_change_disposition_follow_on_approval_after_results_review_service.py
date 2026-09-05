from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_service
    as service,
)


def _confirmations() -> dict:
    return {**deepcopy(service.ATTESTATION_VALUE_FIELDS), **{field: True for field in service.ATTESTATION_BOOLEAN_FIELDS}}


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations=_confirmations(),
    )


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
        operator_attestation=_attestation()
    )


def _reject(approval: dict) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(approval)


def test_attestation_builder_creates_exact_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_follow_on_package"] == service.SELECTED_FOLLOW_ON_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION


def test_approval_builds_offline_without_prohibited_public_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("prohibited source builder invoked")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1",
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
        ("selected_follow_on_package", service.SELECTED_FOLLOW_ON_PACKAGE),
        ("source_follow_on_candidate_operator_review_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_follow_on_candidate_operator_review_status", service.source.REVIEW_STATUS),
        ("source_follow_on_candidate_operator_review_scope", service.source.REVIEW_SCOPE),
        ("source_follow_on_candidate_operator_review_commit", service.SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT),
        ("source_follow_on_candidate_operator_review_digest", service.SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST),
        ("source_follow_on_candidate_commit", "072fa2c4c88f66ac95ef7864590b847368ed490c"),
        ("source_follow_on_candidate_digest", "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"),
        ("source_results_review_commit", "f71143ec0743a3732535c47d2ef1d0d887403dc7"),
        ("source_results_review_digest", "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"),
        ("source_enrichment_plan_review_digest", "0cc52bd10f4b3fc61220f92f0024b728c98c43133c6b71906535037cbe824d46"),
        ("source_missing_authority_inventory_review_digest", "72dd695b4b112e4a4c7d285efd896a54bfd05ec0f8cd1c9bc3eb2087a40b49ec"),
        ("source_workstream_mapping_review_digest", "f64e8575ef00ebacf54d1bf145140a94001c8e475e5a89c44e62a609421c7597"),
        ("source_plan_workstream_mapping_review_digest", "f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334"),
        ("source_results_review_manifest_digest", "1d06a9b1ffd9127fa4808f960be188cf09ac85acaf4145845194c9d025e2e3ba"),
        ("source_execution_commit", "e80ddda241863eca8e52ea97fa050dcd6daea5ec"),
        ("source_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
        ("source_authority_enrichment_plan_digest", "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94"),
        ("source_missing_authority_inventory_digest", "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8"),
        ("source_workstream_authority_mapping_digest", "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd"),
        ("source_execution_manifest_digest", "8a544aa173597f2c24e531a69f4eab2264fb1aa0796a67f87b00af291e6109d6"),
        ("source_approval_commit", "c88d4c238224a5c532d07374ab191e8b8b859af5"),
        ("source_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
        ("source_operator_review_commit", "3c8fbf8fe4ac11c2122455d05fa0d82c67e05ddf"),
        ("source_operator_review_digest", "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51"),
        ("source_candidate_commit", "43a39a37636792dd8756cf45561a012d8dd7c275"),
        ("source_candidate_digest", "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c"),
        ("source_failure_diagnosis_commit", "954a3654bc6b1a485d2b13fe2462510ffebe1025"),
        ("source_remediation_execution_after_plan_results_review_failure_diagnosis_digest", "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"),
        ("source_blocked_execution_commit", "65aab2f4a5cc699cc630756c4142dee12f96c838"),
        ("source_blocked_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("source_blocked_manifest_digest", "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"),
        ("source_remediation_execution_approval_after_plan_results_review_commit", "07ecfa2353f450ffacd807809d4857c8f8231b9b"),
        ("source_remediation_execution_approval_after_plan_results_review_digest", "2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1"),
        ("source_plan_results_review_commit", "9cab8e24d7da93408008cc96a412d7ef03eada41"),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa"),
        ("source_targeted_remediation_plan_review_digest", "7570033ff0aeca33bc6cc5f8fbfc3a462d50cb1d3c5537421f6dbd7aefb3d115"),
        ("source_plan_execution_commit", "57ce0d2760d2ae6de2a16bade80291f4dbe05305"),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c"),
        ("source_targeted_remediation_plan_digest", "2d7ffac9fc3cc04f0bfb823ef81f254005adaee7a600ccb6e3444b7f3dec91db"),
        ("source_workstream_mapping_digest", "275b1e5a16e7bffc8bd323615b764fff7e88070d88198177cc11c64530e948e0"),
        ("source_method_results_review_commit", "b847470633387b7056cb2c436a674dbeab347e61"),
        ("source_remediation_or_method_results_review_after_diagnostic_capture_digest", "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"),
        ("source_method_execution_commit", "2e447891ac8bb8ed86b2a3ecaa09043b7933aef7"),
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
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
    ],
)
def test_approval_binds_identity_and_source_chain(field: str, expected: object) -> None:
    assert _build()[field] == expected


def test_approved_package_is_future_execution_only() -> None:
    package = _build()["approved_package"]
    assert package["package_id"] == service.SELECTED_FOLLOW_ON_PACKAGE
    assert package["source_review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["approval_status"] == service.APPROVED_ONLY
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
def test_future_candidate_definition_permissions(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_future_execution_prohibitions(field: str) -> None:
    assert _build()[field] is False


def test_future_requirements_are_all_approved_not_executed() -> None:
    requirements = _build()["approved_future_requirements"]
    assert len(requirements) == 63
    assert {item["requirement_id"] for item in requirements} == set(service.APPROVED_FUTURE_REQUIREMENTS)
    assert {item["approval_status"] for item in requirements} == {service.APPROVED_ONLY}
    assert {item["execution_status"] for item in requirements} == {"NOT_EXECUTED"}


def test_future_plan_is_approved_not_executed() -> None:
    plan = _build()["approved_future_plan"]
    assert len(plan) == 12
    assert [item["step_id"] for item in plan] == list(range(1, 13))
    assert {item["approval_status"] for item in plan} == {service.APPROVED_ONLY}
    assert {item["execution_status"] for item in plan} == {"NOT_EXECUTED"}


def test_planned_outputs_are_authorized_not_generated() -> None:
    outputs = _build()["authorized_planned_outputs"]
    assert len(outputs) == 27
    assert {item["output_id"] for item in outputs} == set(service.AUTHORIZED_OUTPUT_IDS)
    assert {item["authorization_status"] for item in outputs} == {"AUTHORIZED_NOT_GENERATED"}


def test_supporting_and_blocked_packages_preserve_boundaries() -> None:
    approval = _build()
    supporting = approval["supporting_packages"]
    blocked = approval["blocked_packages"]
    assert len(supporting) == 5
    assert len(blocked) == 6
    assert {item["approval_status"] for item in supporting} == {"AVAILABLE_NOT_SELECTED"}
    assert {item["approval_status"] for item in blocked} == {"BLOCKED_NOT_APPROVED"}
    assert all(not item[field] for item in supporting + blocked for field in ("selected", "approved", "authorized", "executed"))


def test_retry_priority_and_enrichment_facts_are_preserved() -> None:
    approval = _build()
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(approval["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in approval["priority_1_target_modules"]) == 612
    assert approval["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["not_retry_evidence"] is True
    assert approval["missing_authority_inventory_review_summary"]["item_count"] == 30
    assert approval["missing_authority_inventory_review_summary"]["item_status"] == "MISSING_NOT_ACQUIRED"
    assert approval["workstream_authority_mapping_review_summary"]["mapping_status"] == "PLANNED_NOT_EXECUTED"


def test_observable_families_workstreams_and_diagnostic_metadata_are_bound() -> None:
    approval = _build()
    assert {item["family_id"] for item in approval["reviewed_observable_failure_families"]} == {
        "assertion_or_value_mismatch", "digest_or_hash_mismatch",
        "fixture_or_test_isolation_issue", "missing_or_unexpected_field",
    }
    assert {item["workstream_id"] for item in approval["reviewed_workstreams"]} == {
        "assertion_value_mismatch_workstream", "digest_hash_boundary_workstream",
        "fixture_isolation_determinism_workstream", "schema_field_contract_workstream",
    }
    diagnostic = approval["diagnostic_capture_evidence_summary"]
    assert diagnostic["exit_code"] == 1
    assert diagnostic["stdout_byte_count"] == 1231380
    assert diagnostic["stderr_byte_count"] == 0
    assert diagnostic["diagnostic_only"] is True


def test_non_actionable_acceptance_and_runtime_values() -> None:
    approval = _build()
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"
    assert approval["runtime_use"] == "NOT_AUTHORIZED"
    assert approval["strategy_use"] == "NOT_AUTHORIZED"
    assert approval["paper_trading"] == "NOT_AUTHORIZED"
    assert approval["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_gates_risks_and_summary_are_complete() -> None:
    approval = _build()
    assert approval["next_chain"] == list(service.NEXT_CHAIN)
    assert approval["next_gates"] == list(service.NEXT_GATES)
    assert approval["risk_controls"] == list(service.RISK_CONTROLS)
    assert approval["summary"]["approved_future_requirement_count"] == 63
    assert approval["summary"]["approved_future_plan_step_count"] == 12
    assert approval["summary"]["authorized_planned_output_count"] == 27
    assert approval["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_checklist_is_complete_and_passes() -> None:
    approval = _build()
    assert len(approval["checklist"]) == len(service.CHECK_IDS)
    assert {item["check_id"] for item in approval["checklist"]} == set(service.CHECK_IDS)
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in approval["checklist"])
    assert approval["summary"]["passed_checks"] == approval["summary"]["total_checks"]
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic_and_valid() -> None:
    first = _build()
    second = _build()
    assert first[service.APPROVAL_DIGEST_KEY] == second[service.APPROVAL_DIGEST_KEY]
    assert len(first[service.APPROVAL_DIGEST_KEY]) == 64
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(first)
    assert result["approval_digest"] == first[service.APPROVAL_DIGEST_KEY]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "schema_version", "approval_status", "approval_scope", "selected_follow_on_package",
        "source_follow_on_candidate_operator_review_digest", "source_follow_on_candidate_digest",
        "source_results_review_digest", "source_enrichment_plan_review_digest",
        "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest",
        "source_results_review_manifest_digest", "source_execution_commit", "source_execution_digest",
        "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest",
        "source_workstream_authority_mapping_digest", "source_execution_manifest_digest",
        "source_approval_digest", "source_operator_review_digest", "source_candidate_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit", "source_blocked_reason", "source_blocked_manifest_digest",
        "primary_failure_class", "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_plan_workstream_mapping_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest", "source_durable_receipt_path",
        "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest",
        "source_module_grouping_digest", "source_staged_inventory_digest", "retry_execution_commit",
        "recommended_next_task", "predictive_usefulness", "runtime_use",
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
    ["approved_future_requirements", "approved_future_plan", "authorized_planned_outputs", "supporting_packages", "blocked_packages", "next_chain", "next_gates", "risk_controls", "checklist", "summary"],
)
def test_validator_rejects_missing_structured_evidence(field: str) -> None:
    approval = _build()
    approval[field] = [] if isinstance(approval[field], list) else {}
    _reject(approval)


def test_validator_rejects_missing_secondary_failure_class() -> None:
    approval = _build()
    approval["secondary_failure_classes"].pop()
    _reject(approval)


def test_validator_rejects_retry_priority_family_and_workstream_tampering() -> None:
    for path in ("retry_failure_context", "priority_1_target_modules", "priority1_validation_summary", "reviewed_observable_failure_families", "reviewed_workstreams"):
        approval = _build()
        if isinstance(approval[path], list):
            approval[path].pop()
        else:
            approval[path].clear()
        _reject(approval)


@pytest.mark.parametrize("field", tuple(service.ATTESTATION_VALUE_FIELDS))
def test_attestation_rejects_wrong_bound_value(field: str) -> None:
    confirmations = _confirmations()
    confirmations[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


@pytest.mark.parametrize("field", service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_missing_closed_boundary_confirmation(field: str) -> None:
    confirmations = _confirmations()
    confirmations.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


@pytest.mark.parametrize(
    ("overrides"),
    [
        {"operator_reference": ""},
        {"operator_attestation_timestamp_utc": "not-a-date"},
        {"operator_attestation_phrase": "wrong"},
        {"selected_follow_on_package": service.PACKAGE_CREATE_NO_CHANGE_DISPOSITION_CANDIDATE_FROM_REVIEWED_ENRICHMENT_RESULTS},
        {"operator_decision": "wrong"},
    ],
)
def test_attestation_rejects_invalid_identity(overrides: dict) -> None:
    values = {
        "operator_reference": "TEST_OPERATOR", "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_follow_on_package": service.SELECTED_FOLLOW_ON_PACKAGE,
        "operator_decision": service.OPERATOR_DECISION, "operator_confirmations": _confirmations(),
    }
    values.update(overrides)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_attestation_v1(**values)


def test_builder_accepts_exact_injected_source_review_without_mutating_it() -> None:
    source_review = service.source._assemble_review()
    original = deepcopy(source_review)
    approval = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
        operator_attestation=_attestation(), source_operator_review=source_review
    )
    assert approval["source_follow_on_candidate_operator_review_digest"] == service.SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST
    assert source_review == original


def test_builder_rejects_changed_injected_source_review() -> None:
    source_review = service.source._assemble_review()
    source_review[service.source.OPERATOR_REVIEW_DIGEST_KEY] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
            operator_attestation=_attestation(), source_operator_review=source_review
        )


def test_markdown_includes_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Approval After Results Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_approval_status(tmp_path) -> None:
    approval = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_APPROVAL_AFTER_RESULTS_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert approval["artifact_kind"] == service.ARTIFACT_KIND


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnApprovalAfterResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(
            tmp_path / protected, operator_attestation=_attestation()
        )
