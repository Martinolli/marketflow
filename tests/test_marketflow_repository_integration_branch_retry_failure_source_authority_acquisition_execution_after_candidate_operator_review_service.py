from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionExecutionError
RUN_TIMESTAMP = "2026-08-23T00:00:00Z"


def _valid_package() -> dict:
    mapped = service._COMMITTED_SOURCE_APPROVAL[
        "missing_authority_to_source_evidence_mapping_review"
    ]["items"][0]
    return {
        "package_kind": service.EVIDENCE_PACKAGE_KIND,
        "package_status": service.EVIDENCE_PACKAGE_STATUS,
        "package_source_owner_or_origin": "TEST_SOURCE_OWNER",
        "package_reference": "TEST_REFERENCE",
        "package_created_utc": RUN_TIMESTAMP,
        "package_digest_or_reproducible_provenance": "sha256:test-package-provenance",
        "package_declares_no_secrets": True,
        "package_declares_no_api_keys": True,
        "package_declares_no_broker_credentials": True,
        "package_declares_no_personal_financial_credentials": True,
        "package_distinguishes_specification_from_observation": True,
        "package_distinguishes_expected_from_actual": True,
        "package_distinguishes_source_authority_from_diagnostic_output": True,
        "evidence_items": [
            {
                "evidence_id": "TEST-EVIDENCE-001",
                "mapped_missing_authority_id": mapped["missing_authority_id"],
                "section_id": mapped["section_id"],
                "workstream_id": mapped["workstream_id"],
                "acceptable_source_artifact_type": "approved_product_specification",
                "source_owner_or_origin": "TEST_SOURCE_OWNER",
                "source_reference": "TEST_REFERENCE",
                "digest_or_reproducible_provenance": "sha256:test-evidence-provenance",
                "evidence_classification": "SPECIFICATION",
                "specification_or_observation": "SPECIFICATION",
                "expected_or_actual_scope": "EXPECTED",
                "authority_statement": "Test-only source authority statement for results review.",
                "results_review_required_before_use": True,
                "direct_change_authorized_now": False,
                "remediation_authorized_now": False,
                "retry_authorized_now": False,
                "main_merge_authorized_now": False,
            }
        ],
    }


def _blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        run_timestamp_utc=RUN_TIMESTAMP
    )


def _success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        operator_source_authority_evidence_package=_valid_package(),
        run_timestamp_utc=RUN_TIMESTAMP,
    )


def _reject(execution: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
            execution
        )


def test_execution_blocks_offline_without_operator_evidence_package() -> None:
    execution = _blocked()
    assert execution["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert execution["execution_status"] == service.BLOCKED_STATUS
    assert execution["execution_succeeded"] is False
    assert execution["blocked_fail_closed"] is True
    assert execution["blocked_reason"] == service.DEFAULT_BLOCKED_REASON
    assert execution["missing_or_failed_data"] == ["operator_source_authority_evidence_package"]


def test_success_path_uses_injected_valid_package_only() -> None:
    execution = _success()
    assert execution["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert execution["execution_status"] == service.SUCCESS_STATUS
    assert execution["execution_succeeded"] is True
    assert execution["blocked_reason"] is None
    assert execution["operator_source_authority_evidence_package"] == _valid_package()


def test_execution_does_not_call_prohibited_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("prohibited source builder invoked")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_approval_after_candidate_operator_review_v1",
        forbidden,
    )
    assert _blocked()["blocked_fail_closed"] is True
    assert _success()["execution_succeeded"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("schema_version", service.SCHEMA_VERSION),
        ("execution_scope", service.EXECUTION_SCOPE),
        ("selected_source_authority_acquisition_package", service.SELECTED_PACKAGE),
        ("source_approval_commit", service.SOURCE_APPROVAL_COMMIT),
        ("source_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("source_attestation_digest", service.SOURCE_ATTESTATION_DIGEST),
        ("source_operator_review_commit", "d23bbacd7f59003b178a689a526054bb5c508dfb"),
        ("source_operator_review_digest", "88fe49607f9b15b3386db8be78f0dccd8637ff194edbe5b950c68ad27bdea1d0"),
        ("source_candidate_review_digest", "6c122b5bb1489861a969efdf9ab9c36f4ce9a799b7ecf76b791d41a550f653e5"),
        ("source_scope_review_digest", "713aefda1df0916f1ddd25084751cb3f2a23ddc9679e16ff4827409678092d0e"),
        ("source_mapping_review_digest", "83104c9ff91bceed69f368f194cf454629f3530e0c6e8dabed83099677a7b381"),
        ("source_operator_review_manifest_digest", "aed56abc9ed50be991066fea1cf79f0e35ed3e2c851cd847e8cb691825f3b38a"),
        ("source_follow_on_results_review_commit", "c3b894179fb89c14d95ba43a72393e943ff44199"),
        ("source_follow_on_results_review_digest", "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"),
        ("source_follow_on_execution_commit", "a5a78331058c37b348108f9599fec6a24763bf06"),
        ("source_follow_on_execution_after_results_review_digest", "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208"),
        ("source_authority_acquisition_candidate_digest", "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91"),
        ("source_authority_acquisition_scope_digest", "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8"),
        ("source_missing_authority_to_source_evidence_mapping_digest", "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334"),
        ("source_follow_on_approval_digest", "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6"),
        ("source_follow_on_candidate_operator_review_digest", "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"),
        ("source_follow_on_candidate_digest", "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"),
        ("source_results_review_digest", "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"),
        ("source_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
        ("source_authority_enrichment_plan_digest", "b2887bcbb29f6ba7905f41f4e500f07042a1903649caa8b3b51c9045aec5cf94"),
        ("source_missing_authority_inventory_digest", "44ece9639ff992936c6e9386eec9efefdd3990b9a35b01c7efcf3ce1e218ecf8"),
        ("source_workstream_authority_mapping_digest", "175f20cd8ba96aa026ea13d3fdfda9b45f44843095f71b905acdedc96999b6fd"),
        ("source_historical_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
        ("source_historical_operator_review_digest", "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51"),
        ("source_candidate_digest", "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c"),
        ("source_remediation_execution_after_plan_results_review_failure_diagnosis_digest", "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"),
        ("source_blocked_execution_commit", "65aab2f4a5cc699cc630756c4142dee12f96c838"),
        ("source_blocked_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("source_blocked_manifest_digest", "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"),
        ("source_remediation_execution_approval_after_plan_results_review_digest", "2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1"),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa"),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c"),
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
def test_success_and_blocked_bind_source_chain(field: str, expected: object) -> None:
    assert _success()[field] == expected
    assert _blocked()[field] == expected


@pytest.mark.parametrize("field", service.COMMON_TRUE_FIELDS)
def test_common_required_true_fields(field: str) -> None:
    assert _success()[field] is True
    assert _blocked()[field] is True


@pytest.mark.parametrize("field", service.SUCCESS_TRUE_FIELDS)
def test_success_required_true_fields(field: str) -> None:
    assert _success()[field] is True


@pytest.mark.parametrize("field", service.BLOCKED_FALSE_FIELDS)
def test_blocked_required_false_fields(field: str) -> None:
    assert _blocked()[field] is False


@pytest.mark.parametrize("field", service.CLOSED_FALSE_FIELDS)
def test_closed_boundaries_remain_false_on_both_paths(field: str) -> None:
    assert _success()[field] is False
    assert _blocked()[field] is False


def test_retry_priority_diagnostic_family_and_workstream_facts() -> None:
    execution = _blocked()
    assert execution["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(execution["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in execution["priority_1_target_modules"]) == 612
    assert execution["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert execution["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert execution["priority1_validation_summary"]["not_retry_evidence"] is True
    diagnostic = execution["diagnostic_capture_evidence_summary"]
    assert (diagnostic["exit_code"], diagnostic["stdout_byte_count"], diagnostic["stderr_byte_count"]) == (1, 1231380, 0)
    assert diagnostic["diagnostic_only"] is True
    assert len(execution["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in execution["reviewed_observable_failure_families"]) == 188
    assert {item["confidence"] for item in execution["reviewed_observable_failure_families"]} == {"HIGH"}
    assert len(execution["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in execution["reviewed_workstreams"])


def test_candidate_scope_mapping_inventory_and_requirement_counts() -> None:
    execution = _blocked()
    candidate = execution["source_authority_acquisition_candidate_review"]
    assert candidate["candidate_status"] == "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED"
    assert candidate["approved"] is False and candidate["executed"] is False
    assert candidate["authority_acquired"] is False and candidate["evidence_acquired"] is False
    assert execution["acquisition_scope_sections_review"]["section_count"] == 4
    mapping = execution["missing_authority_to_source_evidence_mapping_review"]
    assert mapping["mapped_item_count"] == 30 and len(mapping["items"]) == 30
    assert mapping["all_missing_not_acquired"] is True
    assert execution["acceptable_source_artifact_inventory_review"]["artifact_type_count"] == 13
    assert execution["operator_provided_evidence_requirements_review"]["requirement_count"] == 10
    assert execution["evidence_custody_and_digest_requirements_review"]["requirement_count"] == 6
    assert execution["candidate_results_review_requirements_review"]["requirement_count"] == 16


def test_valid_package_contract_mapping_and_coverage() -> None:
    execution = _success()
    package = execution["operator_source_authority_evidence_package"]
    assert set(package) == service.PACKAGE_FIELDS
    assert all(package[field] is True for field in (
        "package_declares_no_secrets", "package_declares_no_api_keys",
        "package_declares_no_broker_credentials", "package_declares_no_personal_financial_credentials",
        "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual",
        "package_distinguishes_source_authority_from_diagnostic_output",
    ))
    assert len(execution["acquired_or_bound_evidence_item_inventory"]) == 1
    assert len(execution["source_authority_evidence_mapping"]) == 1
    assert execution["covered_missing_authority_item_count"] == 1
    assert execution["uncovered_missing_authority_item_count"] == 29
    assert len(execution["missing_authority_coverage"]) == 30
    assert {item["coverage_status"] for item in execution["missing_authority_coverage"]} == {
        "EVIDENCE_BOUND_FOR_RESULTS_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY", "MISSING_NOT_ACQUIRED"
    }


@pytest.mark.parametrize(
    ("field", "expected_reason"),
    [
        ("package_kind", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_KIND"),
        ("package_status", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_STATUS"),
        ("package_source_owner_or_origin", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVENANCE"),
        ("package_reference", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVENANCE"),
        ("package_created_utc", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVENANCE"),
        ("package_digest_or_reproducible_provenance", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVENANCE"),
        ("package_declares_no_secrets", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SECRET_BOUNDARY"),
        ("package_declares_no_api_keys", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SECRET_BOUNDARY"),
        ("package_declares_no_broker_credentials", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SECRET_BOUNDARY"),
        ("package_declares_no_personal_financial_credentials", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SECRET_BOUNDARY"),
        ("package_distinguishes_specification_from_observation", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SEMANTIC_BOUNDARY"),
        ("package_distinguishes_expected_from_actual", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SEMANTIC_BOUNDARY"),
        ("package_distinguishes_source_authority_from_diagnostic_output", "INVALID_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_SEMANTIC_BOUNDARY"),
    ],
)
def test_invalid_package_fields_fail_closed(field: str, expected_reason: str) -> None:
    package = _valid_package()
    package[field] = False if isinstance(package[field], bool) else ""
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        operator_source_authority_evidence_package=package, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert execution["blocked_reason"] == expected_reason
    assert execution["operator_source_authority_evidence_package_supplied"] is True
    assert execution["operator_source_authority_evidence_package_bound"] is False
    assert execution["operator_source_authority_evidence_package"] is None
    assert execution["acquired_or_bound_evidence_item_inventory"] == []


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("mapped_missing_authority_id", "UNKNOWN", "UNKNOWN_MAPPED_MISSING_AUTHORITY_ID"),
        ("section_id", "UNKNOWN", "UNKNOWN_OR_MISMATCHED_SOURCE_AUTHORITY_SECTION_ID"),
        ("workstream_id", "UNKNOWN", "UNKNOWN_OR_MISMATCHED_SOURCE_AUTHORITY_WORKSTREAM_ID"),
        ("acceptable_source_artifact_type", "UNKNOWN", "UNKNOWN_ACCEPTABLE_SOURCE_ARTIFACT_TYPE"),
        ("evidence_classification", "UNKNOWN", "INVALID_SOURCE_AUTHORITY_EVIDENCE_CLASSIFICATION"),
        ("specification_or_observation", "UNKNOWN", "INVALID_SPECIFICATION_OR_OBSERVATION"),
        ("expected_or_actual_scope", "UNKNOWN", "INVALID_EXPECTED_OR_ACTUAL_SCOPE"),
        ("results_review_required_before_use", False, "RESULTS_REVIEW_NOT_REQUIRED_BEFORE_USE"),
        ("direct_change_authorized_now", True, "SOURCE_AUTHORITY_EVIDENCE_ITEM_AUTHORITY_BOUNDARY_FAILURE"),
        ("remediation_authorized_now", True, "SOURCE_AUTHORITY_EVIDENCE_ITEM_AUTHORITY_BOUNDARY_FAILURE"),
        ("retry_authorized_now", True, "SOURCE_AUTHORITY_EVIDENCE_ITEM_AUTHORITY_BOUNDARY_FAILURE"),
        ("main_merge_authorized_now", True, "SOURCE_AUTHORITY_EVIDENCE_ITEM_AUTHORITY_BOUNDARY_FAILURE"),
    ],
)
def test_invalid_evidence_item_fails_closed(field: str, value: object, reason: str) -> None:
    package = _valid_package()
    package["evidence_items"][0][field] = value
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        operator_source_authority_evidence_package=package, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["blocked_reason"] == reason
    assert execution["source_authority_evidence_acquired"] is False


def test_success_and_blocked_digests_are_deterministic() -> None:
    first, second = _success(), _success()
    for field in (
        service.EXECUTION_DIGEST_KEY, service.EVIDENCE_PACKAGE_DIGEST_KEY,
        service.EVIDENCE_MAPPING_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ):
        assert first[field] == second[field]
        assert len(first[field]) == 64
    blocked_first, blocked_second = _blocked(), _blocked()
    assert blocked_first[service.BLOCKED_MANIFEST_DIGEST_KEY] == blocked_second[service.BLOCKED_MANIFEST_DIGEST_KEY]
    assert len(blocked_first[service.BLOCKED_MANIFEST_DIGEST_KEY]) == 64
    assert all(blocked_first[field] is None for field in (
        service.EXECUTION_DIGEST_KEY, service.EVIDENCE_PACKAGE_DIGEST_KEY,
        service.EVIDENCE_MAPPING_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ))


def test_outputs_recommendations_chains_gates_and_risks() -> None:
    success, blocked = _success(), _blocked()
    assert len(success["outputs"]) == 23
    assert {item["output_id"] for item in success["outputs"]} == set(service.SUCCESS_OUTPUT_IDS)
    assert {item["status"] for item in success["outputs"]} == {"GENERATED_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_EVIDENCE_BOUND_FOR_RESULTS_REVIEW_ONLY"}
    assert len(blocked["outputs"]) == 9
    assert {item["output_id"] for item in blocked["outputs"]} == set(service.BLOCKED_OUTPUT_IDS)
    assert {item["status"] for item in blocked["outputs"]} == {"BLOCKED_NOT_GENERATED_OR_BOUNDARY_REPORT_ONLY"}
    assert success["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK
    assert success["next_chain"] == list(service.SUCCESS_NEXT_CHAIN)
    assert blocked["next_chain"] == list(service.BLOCKED_NEXT_CHAIN)
    assert success["next_gates"] == blocked["next_gates"] == list(service.NEXT_GATES)
    assert len(service.NEXT_GATES) == 13
    assert success["risk_controls"] == blocked["risk_controls"] == list(service.RISK_CONTROLS)
    assert len(service.RISK_CONTROLS) == 83


def test_checklists_and_non_actionable_authority_values() -> None:
    for execution in (_success(), _blocked()):
        assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in execution["checklist"])
        assert execution["summary"]["passed_checks"] == execution["summary"]["total_checks"]
        assert execution["summary"]["failed_checks"] == 0
        assert execution["summary"]["blocker_count"] == 0
        assert execution["predictive_usefulness"] == "not accepted"
        assert execution["profitability"] == "not accepted"
        assert {execution[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_validator_accepts_success_and_blocked_artifacts() -> None:
    success = service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(_success())
    blocked = service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(_blocked())
    assert success["execution_succeeded"] is True and success["failed_checks"] == 0
    assert blocked["execution_succeeded"] is False and blocked["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "execution_status", "execution_scope", "selected_source_authority_acquisition_package",
        "source_approval_commit", "source_approval_digest", "source_attestation_digest",
        "source_operator_review_digest", "source_candidate_review_digest", "source_scope_review_digest",
        "source_mapping_review_digest", "source_operator_review_manifest_digest",
        "source_follow_on_results_review_digest", "source_follow_on_execution_after_results_review_digest",
        "source_authority_acquisition_candidate_digest", "source_authority_acquisition_scope_digest",
        "source_missing_authority_to_source_evidence_mapping_digest", "source_follow_on_approval_digest",
        "source_follow_on_candidate_operator_review_digest", "source_follow_on_candidate_digest",
        "source_results_review_digest", "source_execution_digest", "source_authority_enrichment_plan_digest",
        "source_historical_approval_digest", "source_historical_operator_review_digest", "source_candidate_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit", "source_blocked_reason", "source_blocked_manifest_digest",
        "primary_failure_class", "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest", "source_durable_receipt_path",
        "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest",
        "source_module_grouping_digest", "source_staged_inventory_digest",
        "recommended_next_task", "predictive_usefulness", "runtime_use",
    ],
)
@pytest.mark.parametrize("builder", [_success, _blocked], ids=["success", "blocked"])
def test_validator_rejects_changed_scalars(builder, field: str) -> None:
    execution = builder()
    execution[field] = "changed"
    _reject(execution)


@pytest.mark.parametrize("field", service.COMMON_TRUE_FIELDS)
@pytest.mark.parametrize("builder", [_success, _blocked], ids=["success", "blocked"])
def test_validator_rejects_required_common_true_changed(builder, field: str) -> None:
    execution = builder()
    execution[field] = False
    _reject(execution)


@pytest.mark.parametrize("field", service.SUCCESS_TRUE_FIELDS)
def test_validator_rejects_success_true_changed(field: str) -> None:
    execution = _success()
    execution[field] = False
    _reject(execution)


@pytest.mark.parametrize("field", service.BLOCKED_FALSE_FIELDS)
def test_validator_rejects_blocked_false_changed(field: str) -> None:
    execution = _blocked()
    execution[field] = True
    _reject(execution)


@pytest.mark.parametrize("field", service.CLOSED_FALSE_FIELDS)
def test_validator_rejects_success_closed_boundary_changed(field: str) -> None:
    execution = _success()
    execution[field] = True
    _reject(execution)


@pytest.mark.parametrize(
    "field",
    [
        "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families",
        "reviewed_workstreams", "source_authority_acquisition_candidate_review",
        "acquisition_scope_sections_review", "missing_authority_to_source_evidence_mapping_review",
        "acceptable_source_artifact_inventory_review", "operator_provided_evidence_requirements_review",
        "evidence_custody_and_digest_requirements_review", "candidate_results_review_requirements_review",
        "outputs", "next_chain", "next_gates", "risk_controls", "checklist", "summary",
    ],
)
@pytest.mark.parametrize("builder", [_success, _blocked], ids=["success", "blocked"])
def test_validator_rejects_changed_structured_evidence(builder, field: str) -> None:
    execution = builder()
    execution[field] = [] if isinstance(execution[field], list) else {}
    _reject(execution)


def test_validator_rejects_missing_secondary_failure_class() -> None:
    execution = _success()
    execution["secondary_failure_classes"].pop()
    _reject(execution)


@pytest.mark.parametrize(
    "field",
    [
        "package_declares_no_secrets", "package_declares_no_api_keys",
        "package_declares_no_broker_credentials", "package_declares_no_personal_financial_credentials",
        "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual",
        "package_distinguishes_source_authority_from_diagnostic_output",
    ],
)
def test_validator_rejects_success_package_boundary_mutation(field: str) -> None:
    execution = _success()
    execution["operator_source_authority_evidence_package"][field] = False
    _reject(execution)


@pytest.mark.parametrize(
    "field",
    [
        "direct_change_authorized_now", "remediation_authorized_now",
        "retry_authorized_now", "main_merge_authorized_now",
    ],
)
def test_validator_rejects_success_evidence_authority_mutation(field: str) -> None:
    execution = _success()
    execution["operator_source_authority_evidence_package"]["evidence_items"][0][field] = True
    _reject(execution)


@pytest.mark.parametrize(
    "field",
    [
        service.EXECUTION_DIGEST_KEY, service.EVIDENCE_PACKAGE_DIGEST_KEY,
        service.EVIDENCE_MAPPING_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_missing_or_changed_success_digest(field: str) -> None:
    execution = _success()
    execution[field] = None
    _reject(execution)


def test_validator_rejects_missing_or_changed_blocked_manifest_and_reason() -> None:
    for field, value in ((service.BLOCKED_MANIFEST_DIGEST_KEY, None), ("blocked_reason", None)):
        execution = _blocked()
        execution[field] = value
        _reject(execution)


def test_builder_accepts_exact_injected_approval_without_mutating_it() -> None:
    approval = deepcopy(service._COMMITTED_SOURCE_APPROVAL)
    original = deepcopy(approval)
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        source_approval=approval, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["source_approval_digest"] == service.SOURCE_APPROVAL_DIGEST
    assert approval == original


def test_builder_rejects_changed_injected_approval() -> None:
    approval = deepcopy(service._COMMITTED_SOURCE_APPROVAL)
    approval[service.source.APPROVAL_DIGEST_KEY] = "changed"
    with pytest.raises(Error):
        service.execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
            source_approval=approval, run_timestamp_utc=RUN_TIMESTAMP
        )


@pytest.mark.parametrize("builder", [_success, _blocked], ids=["success", "blocked"])
def test_markdown_includes_every_required_section(builder) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_markdown_v1(builder())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Execution After Candidate Operator Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_default_writer_creates_fail_closed_status(tmp_path) -> None:
    execution = service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
        tmp_path, run_timestamp_utc=RUN_TIMESTAMP
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.BLOCKED_ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert execution["blocked_reason"] == service.DEFAULT_BLOCKED_REASON


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(tmp_path, protected: str) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1(
            tmp_path / protected, run_timestamp_utc=RUN_TIMESTAMP
        )
