from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_service
    as target,
)


def valid_attestation():
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=target.REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        **deepcopy(target.SOURCE_ATTESTATION_FIELDS),
        **{field: True for field in target.ATTESTATION_BOOLEAN_FIELDS},
    )


def valid_approval():
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(
        operator_attestation=valid_attestation()
    )


def rejected(value):
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(value)


def test_attestation_and_approval_are_exact_offline_contract(monkeypatch):
    monkeypatch.setattr(target.source, "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1", lambda: (_ for _ in ()).throw(AssertionError("source builder called")))
    approval = valid_approval()
    assert approval["artifact_kind"] == target.ARTIFACT_KIND
    assert approval["approval_status"] == target.APPROVAL_STATUS
    assert approval["approval_scope"] == target.APPROVAL_SCOPE
    assert approval["selected_remediation_plan_or_execution_package"] == target.SELECTED_PACKAGE
    assert approval["created_offline"] is True
    assert approval["summary"]["failed_checks"] == 0


def test_source_evidence_and_reviewed_families_are_bound():
    approval = valid_approval()
    assert approval["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"] == target.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_remediation_plan_or_execution_candidate_after_method_results_review_digest"] == target.source.SOURCE_CANDIDATE_DIGEST
    assert approval["source_remediation_or_method_results_review_after_diagnostic_capture_digest"] == "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"
    assert approval["source_remediation_or_method_execution_after_diagnostic_capture_digest"] == "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88"
    assert approval["observable_failure_family_count"] == 4
    assert approval["total_observable_evidence_items"] == 188
    assert len(approval["highest_confidence_family_ids"]) == 4


def test_plan_first_package_and_future_boundary_are_approved_only():
    approval = valid_approval()
    package = approval["approved_package"]
    assert package["selected"] and package["approved"] and package["authorized_for_future_execution"]
    assert package["executed"] is False
    assert len(approval["approved_future_remediation_requirements"]) == 40
    assert len(approval["approved_future_remediation_plan"]) == 12
    assert len(approval["authorized_planned_outputs"]) == 16
    assert approval["future_execution_may_generate_targeted_remediation_plan"] is True
    assert approval["future_execution_may_modify_production_code"] is False
    assert approval["future_execution_may_run_pytest"] is False


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_all_current_execution_and_authority_boundaries_remain_false(field):
    assert valid_approval()[field] is False


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_only_approval_readiness_facts_are_true(field):
    assert valid_approval()[field] is True


@pytest.mark.parametrize("field", list(target.SOURCE_ATTESTATION_FIELDS)[:12])
def test_attestation_rejects_changed_source_bindings(field):
    kwargs = deepcopy(target.SOURCE_ATTESTATION_FIELDS)
    kwargs[field] = "wrong"
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=target.REQUIRED_REMEDIATION_PLAN_OR_EXECUTION_APPROVAL_AFTER_METHOD_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            **kwargs, **{name: True for name in target.ATTESTATION_BOOLEAN_FIELDS},
        )


@pytest.mark.parametrize("field", ["artifact_kind", "approval_status", "approval_scope", "selected_remediation_plan_or_execution_package", "source_stdout_sha256", "approved_future_remediation_plan", "authorized_planned_outputs", "risk_controls"])
def test_validator_rejects_tampering(field):
    approval = valid_approval()
    approval[field] = None
    rejected(approval)


def test_digest_is_deterministic_and_semantic():
    first, second = valid_approval(), valid_approval()
    assert first[target.APPROVAL_DIGEST_KEY] == second[target.APPROVAL_DIGEST_KEY]
    assert len(first[target.APPROVAL_DIGEST_KEY]) == 64
    altered = deepcopy(first)
    altered["operator_attestation"]["operator_reference"] = "OTHER"
    rejected(altered)


def test_writer_round_trips_and_refuses_overwrite_and_protected_paths(tmp_path):
    receipt = target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(tmp_path, operator_attestation=valid_attestation())
    loaded = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1.json").read_text(encoding="utf-8"))
    assert receipt["approval_digest"] == loaded[target.APPROVAL_DIGEST_KEY]
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(tmp_path, operator_attestation=valid_attestation())
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionApprovalAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1(tmp_path / ".marketflow", operator_attestation=valid_attestation())


def test_markdown_contains_all_required_sections():
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_markdown_v1(valid_approval())
    for heading in ("Operator Attestation", "Source Method Results Review", "Reviewed Observable Failure Families", "Approved Future Remediation Plan", "Future Remediation Execution Boundary", "Risk Controls", "Guardrails"):
        assert f"## {heading}" in markdown
