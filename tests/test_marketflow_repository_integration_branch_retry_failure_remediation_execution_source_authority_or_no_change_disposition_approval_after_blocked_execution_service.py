from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_service
    as service,
)


def _confirmations():
    return {**service.ATTESTATION_VALUE_FIELDS, **{field: True for field in service.ATTESTATION_BOOLEAN_FIELDS}}


def _attestation():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1,
        operator_confirmations=_confirmations(),
    )


@pytest.fixture()
def approval():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=_attestation())


def _validate(approval):
    return service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(approval)


def _assert_rejected(approval):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        _validate(approval)


def test_approval_builds_offline_with_exact_identity(approval):
    assert approval["artifact_kind"] == service.ARTIFACT_KIND
    assert approval["schema_version"] == service.SCHEMA_VERSION
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert approval["approval_scope"] == service.APPROVAL_SCOPE
    assert approval["created_offline"] is approval["governance_only"] is approval["approval_only"] is True
    assert approval["operator_attestation_required"] is True


def test_attestation_is_exact_and_non_secret(approval):
    attestation = approval["operator_attestation"]
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_source_authority_or_no_change_disposition_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert all(attestation[field] == value for field, value in service.ATTESTATION_VALUE_FIELDS.items())
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_source_operator_review_and_candidate_are_bound(approval):
    assert approval["source_operator_review_commit"] == service.SOURCE_OPERATOR_REVIEW_COMMIT
    assert approval["source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_candidate_commit"] == service.source.SOURCE_CANDIDATE_COMMIT
    assert approval["source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"] == service.source.SOURCE_CANDIDATE_DIGEST
    assert approval["source_operator_review_summary"]["checklist"] == "256/256 PASS"


def test_all_source_bindings_are_preserved(approval):
    for field, expected in service.SOURCE_BINDINGS.items():
        assert approval[field] == expected


def test_selected_package_is_approved_for_future_execution_only(approval):
    assert approval["selected_source_authority_or_no_change_disposition_package"] == service.SELECTED_PACKAGE
    assert approval["approved_package"] == service._approved_package()
    assert approval["approved_package"]["approval_status"] == service.APPROVED_ONLY
    assert approval["approved_package"]["selected"] is True
    assert approval["approved_package"]["approved"] is True
    assert approval["approved_package"]["authorized_for_future_execution"] is True
    assert approval["approved_package"]["executed"] is False


def test_failure_and_retry_evidence_remains_bound(approval):
    assert approval["source_blocked_reason"] == service.source.source.source.SOURCE_BLOCKED_REASON
    assert approval["primary_failure_class"] == service.source.source.source.PRIMARY_FAILURE_CLASS
    assert approval["secondary_failure_classes"] == list(service.source.source.source.SECONDARY_FAILURE_CLASSES)
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["priority_1_total_nodeids"] == 612
    assert approval["top_10_count_sum"] == 1069
    assert approval["module_summary_module_count"] == 29
    assert approval["failed_or_errored_nodeids_count"] == 1404


def test_priority1_and_diagnostic_metadata_is_preserved(approval):
    assert approval["priority1_pre_change_validation_passed_count"] == 675
    assert approval["priority1_post_change_validation_passed_count"] == 675
    assert approval["priority1_validation_summary"]["not_retry_evidence"] is True
    assert approval["source_exit_code"] == 1
    assert approval["source_stdout_byte_count"] == 1231380
    assert approval["source_stderr_byte_count"] == 0
    assert approval["diagnostic_receipt_parsed_in_approval"] is False
    assert approval["diagnostic_output_analyzed_in_approval"] is False


def test_families_and_workstreams_are_preserved(approval):
    assert len(approval["reviewed_observable_failure_families"]) == 4
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in approval["reviewed_observable_failure_families"])
    assert len(approval["reviewed_workstreams"]) == 4
    assert approval["total_observable_evidence_items"] == 188


def test_approved_requirements_plan_and_outputs_are_not_executed(approval):
    assert approval["approved_future_requirements"] == service._approved_requirements()
    assert approval["approved_future_plan"] == service._approved_plan()
    assert approval["authorized_planned_outputs"] == service._authorized_outputs()
    assert len(approval["approved_future_requirements"]) == 50
    assert len(approval["approved_future_plan"]) == 12
    assert len(approval["authorized_planned_outputs"]) == 21
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_plan"])


def test_supporting_and_blocked_packages_remain_unselected(approval):
    assert approval["supporting_packages"] == service._supporting_packages()
    assert approval["blocked_packages"] == service._blocked_packages()
    assert len(approval["supporting_packages"]) == 5
    assert len(approval["blocked_packages"]) == 6
    assert all(not item["selected"] and not item["approved"] and not item["authorized"] and not item["executed"] for item in approval["supporting_packages"] + approval["blocked_packages"])


def test_future_execution_boundary_is_narrow(approval):
    assert approval["future_source_authority_or_no_change_disposition_execution_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED"
    assert approval["future_source_authority_or_no_change_disposition_execution_type"] == "SOURCE_AUTHORITY_ENRICHMENT_PLAN_AFTER_BLOCKED_REMEDIATION"
    for field in service.FUTURE_PERMISSION_TRUE_FIELDS:
        assert approval[field] is True
    for field in service.FUTURE_PERMISSION_FALSE_FIELDS:
        assert approval[field] is False


def test_all_current_execution_and_downstream_boundaries_remain_closed(approval):
    for field in service.FALSE_FIELDS:
        assert approval[field] is False
    assert approval["predictive_usefulness"] == approval["profitability"] == service.NOT_ACCEPTED
    assert approval["runtime_use"] == approval["strategy_use"] == approval["paper_trading"] == approval["broker_execution"] == service.NOT_AUTHORIZED


def test_chain_gates_and_risk_controls_are_exact(approval):
    assert approval["next_chain"] == list(service.NEXT_CHAIN)
    assert approval["next_gates"] == list(service.NEXT_GATES)
    assert approval["risk_controls"] == list(service.RISK_CONTROLS)
    assert len(approval["next_chain"]) == len(approval["next_gates"]) == 8
    assert len(approval["risk_controls"]) == 99


def test_checklist_passes_without_blockers(approval):
    assert approval["summary"]["total_checks"] == len(approval["checklist"])
    assert approval["summary"]["passed_checks"] == len(approval["checklist"])
    assert approval["summary"]["failed_checks"] == approval["summary"]["blocker_count"] == 0


def test_digest_is_deterministic():
    left = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=_attestation())
    right = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=_attestation())
    assert left[service.APPROVAL_DIGEST_KEY] == right[service.APPROVAL_DIGEST_KEY]


def test_validator_accepts_valid_approval(approval):
    result = _validate(approval)
    assert result["approval_digest"] == approval[service.APPROVAL_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == result["blocker_count"] == 0


def test_builder_accepts_exact_source_operator_review():
    review = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()
    approval = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=_attestation(), source_operator_review=review)
    assert approval["source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST


def test_builder_rejects_changed_source_operator_review():
    review = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()
    review["source_blocked_reason"] = "CHANGED"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(operator_attestation=_attestation(), source_operator_review=review)


@pytest.mark.parametrize("field", service.ATTESTATION_VALUE_FIELDS)
def test_attestation_rejects_changed_value_confirmation(field):
    confirmations = _confirmations()
    confirmations[field] = "CHANGED"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z", operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, operator_confirmations=confirmations)


@pytest.mark.parametrize("field", service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_false_boolean_confirmation(field):
    confirmations = _confirmations()
    confirmations[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z", operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, operator_confirmations=confirmations)


@pytest.mark.parametrize("field", ["operator_attestation_timestamp_utc", "operator_attestation_phrase", "selected_source_authority_or_no_change_disposition_package", "operator_decision"])
def test_attestation_rejects_invalid_identity_field(field):
    kwargs = {"operator_reference": "TEST_OPERATOR", "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z", "operator_attestation_phrase": service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, "selected_source_authority_or_no_change_disposition_package": service.SELECTED_PACKAGE, "operator_decision": service.OPERATOR_DECISION, "operator_confirmations": _confirmations()}
    kwargs[field] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(**kwargs)


def test_attestation_rejects_blank_operator_reference():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(operator_reference=" ", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z", operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, operator_confirmations=_confirmations())


def test_attestation_rejects_missing_or_extra_confirmation():
    missing = _confirmations()
    missing.pop(next(iter(missing)))
    extra = _confirmations()
    extra["unexpected"] = True
    for confirmations in (missing, extra):
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
            service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_attestation_v1(operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z", operator_attestation_phrase=service.REQUIRED_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ATTESTATION_PHRASE_V1, operator_confirmations=confirmations)


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(approval, field):
    changed = deepcopy(approval)
    changed[field] = "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS + service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_validator_rejects_required_true_fact_changed(approval, field):
    changed = deepcopy(approval)
    changed[field] = False
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS + service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_validator_rejects_forbidden_fact_true(approval, field):
    changed = deepcopy(approval)
    changed[field] = True
    _assert_rejected(changed)


@pytest.mark.parametrize("requirement_index", range(50))
def test_validator_rejects_changed_approved_requirement(approval, requirement_index):
    changed = deepcopy(approval)
    changed["approved_future_requirements"][requirement_index]["execution_status"] = "EXECUTED"
    _assert_rejected(changed)


@pytest.mark.parametrize("plan_index", range(12))
def test_validator_rejects_changed_approved_plan(approval, plan_index):
    changed = deepcopy(approval)
    changed["approved_future_plan"][plan_index]["action"] = "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("output_index", range(21))
def test_validator_rejects_changed_authorized_output(approval, output_index):
    changed = deepcopy(approval)
    changed["authorized_planned_outputs"][output_index]["authorization_status"] = "GENERATED"
    _assert_rejected(changed)


@pytest.mark.parametrize("package_group", ["supporting_packages", "blocked_packages"])
def test_validator_rejects_changed_nonselected_package(approval, package_group):
    changed = deepcopy(approval)
    changed[package_group][0]["selected"] = True
    _assert_rejected(changed)


@pytest.mark.parametrize("risk_control", service.RISK_CONTROLS)
def test_validator_rejects_missing_risk_control(approval, risk_control):
    changed = deepcopy(approval)
    changed["risk_controls"].remove(risk_control)
    _assert_rejected(changed)


def test_validator_rejects_changed_package_checklist_summary_or_digest(approval):
    mutations = []
    package = deepcopy(approval)
    package["approved_package"]["executed"] = True
    mutations.append(package)
    checklist = deepcopy(approval)
    checklist["checklist"] = []
    mutations.append(checklist)
    summary = deepcopy(approval)
    summary["summary"]["total_checks"] = 0
    mutations.append(summary)
    digest = deepcopy(approval)
    digest[service.APPROVAL_DIGEST_KEY] = "0" * 64
    mutations.append(digest)
    for changed in mutations:
        _assert_rejected(changed)


def test_writer_writes_isolated_status_and_refuses_overwrite(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(tmp_path, operator_attestation=_attestation())
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_STATUS.md"
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
    assert path.is_file()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(tmp_path, operator_attestation=_attestation())


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionApprovalAfterBlockedExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_v1(Path(protected), operator_attestation=_attestation())


def test_markdown_contains_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_approval_after_blocked_execution_markdown_v1(approval)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Approval After Blocked Execution v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_public_aliases_match_contract():
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION_V1 == service.ARTIFACT_KIND
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVED_AFTER_BLOCKED_EXECUTION == service.APPROVAL_STATUS
    assert service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_ONLY_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN == service.APPROVAL_SCOPE
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_APPROVAL_AFTER_BLOCKED_EXECUTION_DIGEST_KEY == service.APPROVAL_DIGEST_KEY
