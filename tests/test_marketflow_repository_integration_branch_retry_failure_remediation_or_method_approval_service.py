from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_service as service,
)


def _attestation(**overrides):
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-30T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_method_candidate_digest": service.source.SOURCE_METHOD_CANDIDATE_DIGEST,
        "operator_confirms_source_retry_failure_diagnosis_digest": service.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST,
        "operator_confirms_retry_execution_commit": service.source.source.source.RETRY_EXECUTION_COMMIT,
        "operator_confirms_selected_method_package": service.SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_BOOLEAN_FIELDS})
    values.update(overrides)
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_attestation_v1(
        **values
    )


@pytest.fixture
def approval():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_retry_failure_method_package"] == service.SELECTED_RETRY_FAILURE_METHOD_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_method_candidate_digest", "0" * 64),
        ("operator_confirms_source_retry_failure_diagnosis_digest", "0" * 64),
        ("operator_confirms_retry_execution_commit", "0" * 40),
        ("operator_confirms_selected_method_package", "wrong"),
        ("selected_retry_failure_method_package", "wrong"),
        ("operator_decision", "wrong"),
        ("operator_confirms_retry_failure_counts", False),
        ("operator_confirms_root_regression_not_retry_evidence", False),
        ("operator_confirms_approval_scope_only", False),
        ("operator_confirms_no_method_execution", False),
        ("operator_confirms_no_provider_requests", False),
        ("operator_confirms_runtime_not_authorized", False),
    ],
)
def test_attestation_builder_rejects_incomplete_or_incorrect_confirmation(field, value):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        _attestation(**{field: value})


def test_approval_builds_offline_with_exact_evidence_and_authority_boundaries(approval):
    assert approval["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED
    assert approval["approval_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED
    assert approval["approval_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert approval["selected_retry_failure_method_package"] == service.SELECTED_RETRY_FAILURE_METHOD_PACKAGE
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["source_retry_failure_method_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_retry_failure_method_candidate_digest"] == "414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6"
    assert approval["source_retry_failure_diagnosis_digest"] == "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
    assert approval["source_retry_approval_digest"] == "5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1"
    assert approval["retry_execution_branch"] == "feature/marketflow-repository-integration-branch-retry-execution-v1"
    assert approval["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert [approval[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert approval["root_full_regression_passed_count"] == 29200
    assert approval["root_full_regression_skipped_count"] == 7
    assert approval["root_full_regression_is_retry_evidence"] is False
    assert approval["root_full_regression_does_not_override_detached_retry_failure"] is True


def test_approval_sets_only_future_method_authority(approval):
    for field in (
        "retry_failure_method_selected",
        "retry_failure_method_approved",
        "retry_failure_method_authorized",
        "retry_failure_method_approval_created",
        "ready_for_retry_failure_method_execution",
    ):
        assert approval[field] is True
    for field in (
        "retry_failure_method_executed",
        "diagnostic_method_executed",
        "failure_domain_classification_generated",
        "planned_outputs_generated",
        "new_remediation_candidate_created",
        "new_retry_candidate_created",
        "new_retry_approved",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "evidence_regenerated",
        "provider_requests_made_in_approval",
        "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        assert approval[field] is False
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED
    assert approval["profitability"] == service.NOT_ACCEPTED
    assert all(approval[field] == service.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_approval_carries_forward_reviewed_method_contract(approval):
    selected = approval["selected_method_package"]
    assert selected == {
        "package_id": service.SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        "approval_status": service.APPROVED_FOR_FUTURE_EXECUTION_ONLY,
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
    }
    assert approval["approved_future_method_requirements"] == service.APPROVED_FUTURE_METHOD_REQUIREMENTS
    assert all(row["requirement_value"] is True for row in approval["approved_future_method_requirements"])
    assert approval["approved_future_method_plan"] == service.APPROVED_FUTURE_METHOD_PLAN
    assert approval["future_method_plan_execution_status"] == "NOT_EXECUTED"
    assert approval["planned_outputs"] == service.AUTHORIZED_PLANNED_OUTPUTS
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_summary_and_digest_are_deterministic(approval):
    assert len(approval["checklist"]) == len(service.REQUIRED_CHECK_IDS) == 53
    assert all(row["status"] == service.PASS for row in approval["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == 53
    assert approval["summary"]["passed_checks"] == 53
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0
    digest = approval["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"]
    assert digest == service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest_v1(approval)
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(operator_attestation=_attestation())
    assert rebuilt == approval


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED
    assert result["passed_checks"] == 53
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "wrong"),
        ("approval_status", "wrong"),
        ("approval_scope", "wrong"),
        ("selected_retry_failure_method_package", "wrong"),
        ("source_retry_failure_method_operator_review_digest", "0" * 64),
        ("source_retry_failure_method_candidate_digest", "0" * 64),
        ("source_retry_failure_diagnosis_digest", "0" * 64),
        ("retry_pytest_failed_count", None),
        ("root_full_regression_is_retry_evidence", True),
        ("retry_failure_method_approval_created", False),
        ("retry_failure_method_selected", False),
        ("retry_failure_method_approved", False),
        ("retry_failure_method_authorized", False),
        ("ready_for_retry_failure_method_execution", False),
        ("retry_failure_method_executed", True),
        ("diagnostic_method_executed", True),
        ("failure_domain_classification_generated", True),
        ("planned_outputs_generated", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
        ("provider_requests_made_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_contract_field(approval, field, value):
    invalid = deepcopy(approval)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(invalid)


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_decision", "wrong"),
        ("operator_attestation_phrase", "wrong"),
    ],
)
def test_validator_rejects_changed_operator_attestation(approval, field, value):
    invalid = deepcopy(approval)
    invalid["operator_attestation"][field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(invalid)


def test_validator_rejects_missing_digest(approval):
    invalid = deepcopy(approval)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(invalid)


def test_build_rejects_changed_source_review_digest():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
            source_review={"source_retry_failure_method_operator_review_digest": "0" * 64},
            operator_attestation=_attestation(),
        )


def test_markdown_includes_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_markdown_v1(approval)
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Approval v1",
        "## Operator Attestation",
        "## Source Operator Review",
        "## Source Method Candidate",
        "## Retry Failure Context",
        "## Approval Scope",
        "## Selected Method Package",
        "## Approved Future Method Requirements",
        "## Approved Future Method Plan",
        "## Planned Outputs",
        "## Supporting Packages",
        "## Blocked Packages",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Authority Boundaries",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path, approval):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == approval
    assert receipt["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"] == approval["marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_v1(
            tmp_path, operator_attestation=_attestation()
        )
