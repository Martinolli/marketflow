from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_service
    as service,
)


def _attestation_kwargs() -> dict:
    values = service._attestation_string_expectations()
    values.pop("operator_attestation_version")
    values.update({
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
    })
    values.update({field: True for field in service.ATTESTATION_BOOLEAN_FIELDS})
    return values


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture(scope="module")
def approval() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_complete_29_row_materialization_package"] == service.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_APPROVAL_ATTESTATION_PHRASE_V1
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_approval_builds_offline_with_exact_identity_and_source_bindings(approval: dict) -> None:
    assert approval["artifact_kind"] == service.ARTIFACT_KIND
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert approval["approval_scope"] == service.APPROVAL_SCOPE
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["selected_complete_29_row_materialization_package"] == service.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE
    expected = {
        "source_complete_29_row_materialization_operator_review_digest": "72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90",
        "source_complete_29_row_materialization_candidate_digest": "4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061",
        "source_detail_exposure_or_binding_execution_failure_diagnosis_digest": "8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41",
        "primary_failure_class": "COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE",
        "source_detail_exposure_or_binding_execution_blocked_digest": "9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca",
        "source_detail_exposure_or_binding_execution_blocked_manifest_digest": "c732eac857725728bb856f2d145eb86101ce1f839ddca740b66db4d48ae3aa4c",
        "source_detail_exposure_or_binding_execution_blocked_reason": "COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE",
        "source_detail_exposure_or_binding_approval_digest": "384ea3fcb8440c48be01d62a115e9abaf8424ea898832551d80b30383207954f",
        "source_detail_exposure_or_binding_operator_review_digest": "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b",
        "source_detail_exposure_or_binding_candidate_digest": "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23",
        "source_reentry_failure_diagnosis_digest": "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb",
        "source_reentry_execution_blocked_digest": "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49",
        "source_after_v2_planning_reentry_digest": "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927",
        "source_module_grouping_source_recovery_results_review_digest": "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266",
        "source_module_grouping_source_recovery_detail_digest": "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5",
        "source_blocked_after_v2_execution_digest": "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755",
        "source_after_v2_approval_digest": "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97",
        "source_results_review_v2_digest": "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86",
        "source_execution_v2_digest": "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017",
        "source_module_grouping_digest": "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
    }
    assert {field: approval[field] for field in expected} == expected


def test_retry_counts_recovered_summary_and_source_gap_are_preserved(approval: dict) -> None:
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["recovered_module_grouping_source_summary"] == {
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }
    assert len(approval["top_module_summary"]) == 5
    assert approval["top_5_count_sum"] == 612
    assert approval["top_10_count_sum"] == 1069
    assert approval["available_data"]
    assert approval["missing_data"]
    assert approval["actual_live_detail_binding_source_lacks_complete_29_rows"] is True
    assert approval["detail_binding_success_path_tested_with_complete_29_row_snapshot"] is True


def test_approval_authorizes_only_future_materialization_execution(approval: dict) -> None:
    assert approval["complete_29_row_materialization_approval_created"] is True
    assert approval["materialization_package_selected"] is True
    assert approval["materialization_package_approved"] is True
    assert approval["materialization_package_authorized"] is True
    assert approval["ready_for_complete_29_row_materialization_execution"] is True
    assert approval["approved_package"]["executed"] is False
    assert len(approval["approved_future_materialization_or_binding_requirements"]) == 47
    assert all(item["approval_status"] == service.APPROVED_ONLY and item["execution_status"] == service.NOT_EXECUTED for item in approval["approved_future_materialization_or_binding_requirements"])
    assert len(approval["approved_future_materialization_or_binding_plan"]) == 12
    assert all(item["execution_status"] == service.NOT_EXECUTED for item in approval["approved_future_materialization_or_binding_plan"])
    assert len(approval["authorized_planned_outputs"]) == 14
    assert all(item["authorization_status"] == service.AUTHORIZED_NOT_GENERATED for item in approval["authorized_planned_outputs"])
    assert len(approval["supporting_packages"]) == 5
    assert all(not item["selected"] and not item["approved"] for item in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 6
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in approval["blocked_packages"])


def test_execution_claim_and_runtime_boundaries_remain_closed(approval: dict) -> None:
    assert all(approval[field] is False for field in service.FALSE_BOUNDARIES)
    assert all(approval[field] is False for field in service.UNSUPPORTED_CLAIMS_FIELDS)
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED
    assert approval["profitability"] == service.NOT_ACCEPTED
    assert approval["runtime_use"] == service.NOT_AUTHORIZED
    assert approval["strategy_use"] == service.NOT_AUTHORIZED
    assert approval["paper_trading"] == service.NOT_AUTHORIZED
    assert approval["broker_execution"] == service.NOT_AUTHORIZED


def test_checklist_summary_and_digest_are_valid_and_deterministic(approval: dict) -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(approval)
    assert validation["passed_checks"] == validation["total_checks"] == 98
    assert validation["failed_checks"] == validation["blocker_count"] == 0
    assert len(approval["risk_controls"]) == 70
    assert approval["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
    assert approval[digest_key] == service.marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest_v1(approval)
    assert service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(operator_attestation=_attestation()) == approval


@pytest.mark.parametrize("field", service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_false_closed_boundary_confirmation(field: str) -> None:
    values = _attestation_kwargs()
    values[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    "field",
    [field for field in service._attestation_string_expectations() if field != "operator_attestation_version"],
)
def test_attestation_rejects_changed_binding(field: str) -> None:
    values = _attestation_kwargs()
    values[field] = "OTHER"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("approval_status", "OTHER"), ("approval_scope", "OTHER"),
        ("selected_complete_29_row_materialization_package", "OTHER"),
        ("source_complete_29_row_materialization_operator_review_digest", "0" * 64),
        ("source_complete_29_row_materialization_candidate_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "0" * 64),
        ("primary_failure_class", "OTHER"),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context", {}),
        ("recovered_module_grouping_source_summary", {}), ("top_module_summary", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068), ("available_data", []),
        ("missing_data", []), ("actual_live_detail_binding_source_lacks_complete_29_rows", False),
        ("complete_29_row_materialization_approval_created", False), ("materialization_package_selected", False),
        ("materialization_package_approved", False), ("materialization_package_authorized", False),
        ("ready_for_complete_29_row_materialization_execution", False), ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_required_approval_field(approval: dict, field: str, value: object) -> None:
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES + service.UNSUPPORTED_CLAIMS_FIELDS)
def test_validator_rejects_open_boundary(approval: dict, field: str) -> None:
    changed = deepcopy(approval)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(changed)


def test_validator_rejects_missing_digest_and_changed_attestation(approval: dict) -> None:
    digest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_digest"
    changed = deepcopy(approval)
    changed.pop(digest_key)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(changed)
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_attestation_phrase"] = "OTHER"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(changed)


def test_builder_rejects_changed_source_review() -> None:
    source_review = service._committed_source_review()
    source_review["primary_failure_class"] = "OTHER"
    with pytest.raises(ValueError):
        service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
            source_review=source_review, operator_attestation=_attestation()
        )


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(payload)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_v1(
            tmp_path, operator_attestation=_attestation()
        )


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_approval_markdown_v1(approval)
    for heading in (
        "Operator Attestation", "Source Materialization Candidate Operator Review", "Source Materialization Candidate",
        "Source Detail Exposure or Binding Execution Failure Diagnosis", "Source Blocked Detail Exposure or Binding Execution",
        "Source Detail Exposure or Binding Approval", "Source Reentry Failure Diagnosis", "Source Recovery Results Review",
        "Retry Failure Context", "Recovered Module Grouping Source Summary", "Available and Missing Detail Source",
        "Approval Scope", "Selected Complete 29-row Materialization Package",
        "Approved Future Materialization or Binding Requirements", "Approved Future Materialization or Binding Plan",
        "Planned Outputs", "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
