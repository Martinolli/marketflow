from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_service
    as service,
)


def _attestation_kwargs() -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1,
        "operator_confirms_source_operator_review_digest": "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b",
        "operator_confirms_source_candidate_digest": "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23",
        "operator_confirms_source_diagnosis_digest": "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb",
        "operator_confirms_primary_failure_class": "COMMITTED_REENTRY_SOURCE_DETAIL_GAP",
        "operator_confirms_source_blocked_reentry_execution_digest": "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49",
        "operator_confirms_source_blocked_reentry_manifest_digest": "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99",
        "operator_confirms_source_blocked_reentry_reason": "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT",
        "operator_confirms_source_planning_reentry_digest": "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927",
        "operator_confirms_source_recovery_results_review_digest": "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266",
        "operator_confirms_source_recovery_results_review_manifest_digest": "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9",
        "operator_confirms_source_recovery_execution_digest": "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a",
        "operator_confirms_source_recovery_detail_digest": "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5",
        "operator_confirms_source_recovery_digest_manifest_digest": "940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc",
        "operator_confirms_source_blocked_after_v2_execution_digest": "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755",
        "operator_confirms_source_after_v2_approval_digest": "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97",
        "operator_confirms_source_results_review_v2_digest": "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86",
        "operator_confirms_source_execution_v2_digest": "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017",
        "operator_confirms_source_module_grouping_digest": "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff",
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_detail_exposure_or_binding_package": service.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_BOOLEAN_FIELDS})
    return values


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture(scope="module")
def approval() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_detail_exposure_or_binding_package"] == service.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_APPROVAL_ATTESTATION_PHRASE_V1
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_approval_builds_offline_and_binds_required_source_facts(approval: dict) -> None:
    assert approval["artifact_kind"] == service.ARTIFACT_KIND
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert approval["approval_scope"] == service.APPROVAL_SCOPE
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["selected_detail_exposure_or_binding_package"] == service.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE
    assert approval["source_detail_exposure_or_binding_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_detail_exposure_or_binding_candidate_digest"] == "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23"
    assert approval["source_reentry_failure_diagnosis_digest"] == "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb"
    assert approval["primary_failure_class"] == "COMMITTED_REENTRY_SOURCE_DETAIL_GAP"
    assert approval["source_reentry_execution_blocked_digest"] == "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49"
    assert approval["source_reentry_execution_blocked_manifest_digest"] == "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99"
    assert approval["source_reentry_execution_blocked_reason"] == "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"
    assert approval["source_after_v2_planning_reentry_digest"] == "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927"
    assert approval["source_module_grouping_source_recovery_results_review_digest"] == "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266"
    assert approval["source_module_grouping_source_recovery_results_review_manifest_digest"] == "4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9"
    assert approval["source_module_grouping_source_recovery_execution_digest"] == "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a"
    assert approval["source_module_grouping_source_recovery_detail_digest"] == "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"
    assert approval["source_module_grouping_source_recovery_digest_manifest_digest"] == "940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc"
    assert approval["source_blocked_after_v2_execution_digest"] == "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755"
    assert approval["source_after_v2_approval_digest"] == "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97"
    assert approval["source_results_review_v2_digest"] == "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86"
    assert approval["source_execution_v2_digest"] == "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017"
    assert approval["source_module_grouping_digest"] == "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"
    assert approval["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"


def test_approval_preserves_retry_and_recovered_source_summary(approval: dict) -> None:
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["recovered_module_grouping_source_summary"] == {
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }
    assert len(approval["top_module_summary"]) == 5
    assert approval["top_5_count_sum"] == 612
    assert approval["top_10_count_sum"] == 1069
    assert approval["available_committed_reentry_detail"]
    assert approval["missing_committed_reentry_detail"]
    assert approval["actual_live_reentry_source_lacks_complete_29_rows"] is True
    assert approval["reentry_success_path_tested_with_complete_29_row_snapshot"] is True


def test_approval_authorizes_only_future_execution(approval: dict) -> None:
    assert approval["detail_exposure_or_binding_approval_created"] is True
    assert approval["detail_exposure_or_binding_selected"] is True
    assert approval["detail_exposure_or_binding_approved"] is True
    assert approval["detail_exposure_or_binding_authorized"] is True
    assert approval["ready_for_detail_exposure_or_binding_execution"] is True
    assert approval["approved_package"]["executed"] is False
    assert len(approval["approved_future_detail_exposure_or_binding_requirements"]) == 31
    assert all(item["approval_status"] == service.APPROVED_ONLY for item in approval["approved_future_detail_exposure_or_binding_requirements"])
    assert len(approval["approved_future_detail_exposure_or_binding_plan"]) == 10
    assert all(item["execution_status"] == service.NOT_EXECUTED for item in approval["approved_future_detail_exposure_or_binding_plan"])
    assert len(approval["authorized_planned_outputs"]) == 12
    assert all(item["authorization_status"] == service.AUTHORIZED_NOT_GENERATED for item in approval["authorized_planned_outputs"])
    assert len(approval["supporting_packages"]) == 5
    assert all(not item["selected"] and not item["approved"] for item in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 5
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in approval["blocked_packages"])


def test_all_execution_and_authority_boundaries_remain_closed(approval: dict) -> None:
    assert all(approval[field] is False for field in service.FALSE_BOUNDARIES)
    assert all(approval[field] is False for field in service.UNSUPPORTED_CLAIMS_FIELDS)
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED
    assert approval["profitability"] == service.NOT_ACCEPTED
    assert approval["runtime_use"] == service.NOT_AUTHORIZED
    assert approval["strategy_use"] == service.NOT_AUTHORIZED
    assert approval["paper_trading"] == service.NOT_AUTHORIZED
    assert approval["broker_execution"] == service.NOT_AUTHORIZED


def test_checklist_summary_and_digest_are_valid_and_deterministic(approval: dict) -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(approval)
    assert validation["passed_checks"] == validation["total_checks"]
    assert validation["failed_checks"] == 0
    assert validation["blocker_count"] == 0
    assert len(approval["risk_controls"]) == 63
    assert approval["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert approval["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest"] == service.marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest_v1(approval)
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(operator_attestation=_attestation())
    assert rebuilt == approval


@pytest.mark.parametrize("field", service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_missing_or_false_closed_boundary_confirmation(field: str) -> None:
    values = _attestation_kwargs()
    values[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "REJECT"),
        ("operator_attestation_phrase", "wrong"),
        ("operator_attestation_timestamp_utc", "2026-08-23"),
        ("operator_reference", ""),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_candidate_digest", "0" * 64),
        ("operator_confirms_source_diagnosis_digest", "0" * 64),
        ("operator_confirms_primary_failure_class", "OTHER"),
        ("operator_confirms_source_blocked_reentry_execution_digest", "0" * 64),
        ("operator_confirms_source_blocked_reentry_manifest_digest", "0" * 64),
        ("operator_confirms_source_blocked_reentry_reason", ""),
        ("operator_confirms_source_planning_reentry_digest", "0" * 64),
        ("operator_confirms_source_recovery_results_review_digest", "0" * 64),
        ("operator_confirms_source_recovery_detail_digest", "0" * 64),
        ("operator_confirms_source_module_grouping_digest", "0" * 64),
        ("operator_confirms_retry_execution_commit", "0" * 40),
        ("operator_confirms_selected_detail_exposure_or_binding_package", "OTHER"),
        ("selected_detail_exposure_or_binding_package", "OTHER"),
    ],
)
def test_attestation_rejects_changed_binding(field: str, value: object) -> None:
    values = _attestation_kwargs()
    values[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("approval_status", "OTHER"), ("approval_scope", "OTHER"),
        ("selected_detail_exposure_or_binding_package", "OTHER"),
        ("source_detail_exposure_or_binding_operator_review_digest", "0" * 64),
        ("source_detail_exposure_or_binding_candidate_digest", "0" * 64),
        ("source_reentry_failure_diagnosis_digest", "0" * 64), ("primary_failure_class", "OTHER"),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_reentry_execution_blocked_manifest_digest", "0" * 64),
        ("source_reentry_execution_blocked_reason", ""),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_results_review_v2_digest", "0" * 64), ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("top_module_summary", []), ("available_committed_reentry_detail", []),
        ("missing_committed_reentry_detail", []), ("actual_live_reentry_source_lacks_complete_29_rows", False),
        ("detail_exposure_or_binding_approval_created", False), ("detail_exposure_or_binding_selected", False),
        ("detail_exposure_or_binding_approved", False), ("detail_exposure_or_binding_authorized", False),
        ("ready_for_detail_exposure_or_binding_execution", False), ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_required_approval_field(approval: dict, field: str, value: object) -> None:
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES)
def test_validator_rejects_open_execution_boundary(approval: dict, field: str) -> None:
    changed = deepcopy(approval)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(changed)


def test_validator_rejects_missing_retry_counts_and_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["retry_failure_context"]["counts"] = {}
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(changed)
    changed = deepcopy(approval)
    changed.pop("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(changed)


def test_builder_rejects_changed_source_review() -> None:
    source_review = service._committed_source_review()
    source_review["primary_failure_class"] = "OTHER"
    with pytest.raises(ValueError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
            source_review=source_review, operator_attestation=_attestation()
        )


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
        tmp_path, operator_attestation=_attestation()
    )
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1.json").read_text(encoding="utf-8"))
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(payload)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_v1(
            tmp_path, operator_attestation=_attestation()
        )


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_approval_markdown_v1(approval)
    for heading in (
        "Operator Attestation", "Source Operator Review", "Source Detail Exposure or Binding Candidate",
        "Source Reentry Failure Diagnosis", "Source Blocked Reentry Execution", "Source Recovery Results Review",
        "Retry Failure Context", "Recovered Module Grouping Source Summary", "Available and Missing Committed Detail",
        "Approval Scope", "Selected Detail Exposure or Binding Package",
        "Approved Future Detail Exposure or Binding Requirements", "Approved Future Detail Exposure or Binding Plan",
        "Planned Outputs", "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
