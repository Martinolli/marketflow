from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_service as service,
)


def _attestation(**overrides):
    source_review = service._source_review()
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-30T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.SOURCE_OUTPUT_CAPTURE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_output_capture_candidate_digest": service.source.SOURCE_OUTPUT_CAPTURE_CANDIDATE_DIGEST,
        "operator_confirms_source_method_execution_digest": service.source.source.SOURCE_METHOD_EXECUTION_DIGEST,
        "operator_confirms_source_blocked_manifest_digest": service.source.source.SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST,
        "operator_confirms_retry_execution_commit": source_review["retry_execution_commit"],
        "operator_confirms_classification_blocked_reason": source_review["classification_blocked_reason"],
        "operator_confirms_detached_worktree_path": source_review["detached_integration_worktree_path"],
        "operator_confirms_detached_worktree_head": source_review["detached_integration_worktree_head_commit"],
        "operator_confirms_staged_evidence_digest": source_review["staged_evidence_manifest_digest"],
        "operator_confirms_selected_output_capture_package": service.SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_BOOLEAN_FIELDS})
    values.update(overrides)
    return service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_attestation_v1(
        **values
    )


@pytest.fixture
def approval():
    return service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert (
        attestation["selected_output_capture_or_classification_source_package"]
        == service.SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE
    )
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_output_capture_candidate_digest", "0" * 64),
        ("operator_confirms_source_method_execution_digest", "0" * 64),
        ("operator_confirms_source_blocked_manifest_digest", "0" * 64),
        ("operator_confirms_retry_execution_commit", "0" * 40),
        ("operator_confirms_classification_blocked_reason", "wrong"),
        ("operator_confirms_detached_worktree_path", "wrong"),
        ("operator_confirms_detached_worktree_head", "0" * 40),
        ("operator_confirms_staged_evidence_digest", "0" * 64),
        ("operator_confirms_selected_output_capture_package", "wrong"),
        ("selected_output_capture_or_classification_source_package", "wrong"),
        ("operator_decision", "wrong"),
        ("operator_confirms_retry_failure_counts", False),
        ("operator_confirms_no_pytest_cache_read", False),
        ("operator_confirms_no_diagnostic_command", False),
        ("operator_confirms_runtime_not_authorized", False),
    ],
)
def test_attestation_builder_rejects_incomplete_or_incorrect_confirmation(field, value):
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        _attestation(**{field: value})


def test_approval_builds_offline_and_binds_source_evidence(approval):
    assert (
        approval["artifact_kind"]
        == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVED
    )
    assert (
        approval["approval_status"]
        == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVED
    )
    assert (
        approval["approval_scope"]
        == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    )
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["source_output_capture_operator_review_digest"] == service.SOURCE_OUTPUT_CAPTURE_OPERATOR_REVIEW_DIGEST
    assert approval["source_output_capture_candidate_digest"] == "fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518"
    assert approval["source_method_execution_digest"] == "522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562"
    assert approval["source_method_blocked_manifest_digest"] == "3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f"
    assert approval["retry_execution_branch"] == "feature/marketflow-repository-integration-branch-retry-execution-v1"
    assert approval["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert [approval[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert approval["classification_blocked_reason"] == "AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE"
    assert approval["detached_integration_worktree_head_commit"] == "220fbc220365fce9cae13ab4853cddff118c0187"
    assert approval["staged_evidence_manifest_digest"] == "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"


def test_approval_sets_only_future_output_capture_authority(approval):
    for field in (
        "output_capture_method_selected",
        "output_capture_method_approved",
        "output_capture_method_authorized",
        "output_capture_method_approval_created",
        "ready_for_output_capture_execution",
    ):
        assert approval[field] is True
    for field in (
        "output_capture_method_executed",
        "classification_source_capture_executed",
        "classification_source_generated",
        "classification_source_review_created",
        "pytest_cache_read",
        "operator_logs_parsed",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "new_classification_method_candidate_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "integration_results_review_created",
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
    assert all(
        approval[field] == service.NOT_AUTHORIZED
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")
    )


def test_approval_carries_forward_reviewed_output_capture_contract(approval):
    assert approval["selected_output_capture_package"] == {
        "package_id": service.SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE,
        "approval_status": service.APPROVED_FOR_FUTURE_OUTPUT_CAPTURE_EXECUTION_ONLY,
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
    }
    assert len(approval["approved_future_output_capture_requirements"]) == 18
    assert all(
        row["approval_status"] == service.APPROVED_FOR_FUTURE_OUTPUT_CAPTURE_EXECUTION_ONLY
        for row in approval["approved_future_output_capture_requirements"]
    )
    assert len(approval["approved_future_output_capture_plan"]) == 10
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in approval["approved_future_output_capture_plan"])
    assert len(approval["planned_outputs"]) == 9
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for row in approval["planned_outputs"])
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_summary_and_digest_are_deterministic(approval):
    assert len(approval["checklist"]) == len(service.REQUIRED_CHECK_IDS) == 62
    assert all(row["status"] == service.PASS for row in approval["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in approval["checklist"]
    )
    assert approval["summary"]["total_checks"] == 62
    assert approval["summary"]["passed_checks"] == 62
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0
    digest = approval[
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_digest"
    ]
    assert digest == "41052b8621f57721383bc7d8fc416c95e9fef4d5af49b94278ede43209304d33"
    assert digest == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_digest_v1(
        approval
    )
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
        operator_attestation=_attestation()
    )
    assert rebuilt == approval


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
        approval
    )
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVED
    assert result["passed_checks"] == 62
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "wrong"),
        ("approval_status", "wrong"),
        ("approval_scope", "wrong"),
        ("selected_output_capture_or_classification_source_package", "wrong"),
        ("source_output_capture_operator_review_digest", "0" * 64),
        ("source_output_capture_candidate_digest", "0" * 64),
        ("source_method_execution_digest", "0" * 64),
        ("source_method_blocked_manifest_digest", "0" * 64),
        ("retry_pytest_failed_count", None),
        ("classification_blocked_reason", None),
        ("root_full_regression_is_retry_evidence", True),
        ("output_capture_method_approval_created", False),
        ("output_capture_method_selected", False),
        ("output_capture_method_approved", False),
        ("output_capture_method_authorized", False),
        ("ready_for_output_capture_execution", False),
        ("output_capture_method_executed", True),
        ("pytest_cache_read", True),
        ("operator_logs_parsed", True),
        ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("new_retry_results_review_created", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("classification_source_generated", True),
        ("classification_source_review_created", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("main_merge_approval_created", True),
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
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field,value",
    [("operator_decision", "wrong"), ("operator_attestation_phrase", "wrong")],
)
def test_validator_rejects_changed_operator_attestation(approval, field, value):
    invalid = deepcopy(approval)
    invalid["operator_attestation"][field] = value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
            invalid
        )


def test_validator_rejects_missing_digest(approval):
    invalid = deepcopy(approval)
    invalid.pop(
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_digest"
    )
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "source_output_capture_operator_review_digest",
        "source_output_capture_candidate_digest",
        "source_method_execution_digest",
        "source_method_blocked_manifest_digest",
    ],
)
def test_build_rejects_changed_source_review_evidence(field):
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
            source_review={field: "0" * 64}, operator_attestation=_attestation()
        )


def test_markdown_includes_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_markdown_v1(
        approval
    )
    for section in (
        "Operator Attestation",
        "Source Operator Review",
        "Source Output Capture Candidate",
        "Source Method Execution",
        "Retry Failure Context",
        "Approval Scope",
        "Selected Output Capture Package",
        "Approved Future Output Capture Requirements",
        "Approved Future Output Capture Plan",
        "Planned Outputs",
        "Supporting Packages",
        "Blocked Packages",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json(tmp_path, approval):
    result = service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
        tmp_path, operator_attestation=_attestation()
    )
    written = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1.json").read_text(encoding="utf-8"))
    assert written == approval
    assert result["artifact_kind"] == approval["artifact_kind"]
    assert result["approval_status"] == approval["approval_status"]
    assert result["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_digest"] == approval["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_digest"]


def test_writer_refuses_overwrite(tmp_path):
    service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
        tmp_path, operator_attestation=_attestation()
    )
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceApprovalError
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_approval_v1(
            tmp_path, operator_attestation=_attestation()
        )
