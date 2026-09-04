from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_service
    as service,
)


def _attestation(**overrides: object) -> dict:
    values: dict[str, object] = {
        **service.STRING_CONFIRMATIONS,
        **{field: True for field in service.BOOLEAN_CONFIRMATION_FIELDS},
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1,
    }
    values.update(overrides)
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_attestation_v1(**values)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(operator_attestation=_attestation())


def _set_path(value: dict, path: str, replacement: object) -> None:
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_receipt_recovery_or_recapture_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_RECEIPT_RECOVERY_OR_RECAPTURE_APPROVAL_ATTESTATION_PHRASE_V1
    assert attestation["operator_attestation_version"] == service.ATTESTATION_VERSION
    assert len(attestation["operator_attestation_digest"]) == 64


def test_approval_builds_offline_without_review_builder_or_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: pytest.fail("command attempted"))
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1",
        lambda *args, **kwargs: pytest.fail("source review builder called"),
    )
    monkeypatch.setattr(
        service.source.source.source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
        lambda *args, **kwargs: pytest.fail("diagnostic execution called"),
    )
    approval = _build()
    assert approval["created_offline"] is True
    assert approval["approval_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("approval_status", service.APPROVAL_STATUS),
        ("approval_scope", service.APPROVAL_SCOPE), ("schema_version", service.SCHEMA_VERSION),
        ("selected_receipt_recovery_or_recapture_package", service.SELECTED_PACKAGE),
        ("source_receipt_recovery_or_recapture_candidate_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_candidate_digest", service.source.SOURCE_CANDIDATE_DIGEST),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", service.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"]),
        ("source_targeted_diagnostic_output_capture_execution_digest", service.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_digest"]),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", service.SOURCE_BINDINGS["source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest"]),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "POST_CAPTURE_ARTIFACT_REPORTING_BOUNDARY_FAILED"),
        ("source_primary_failure_class", "POST_CAPTURE_DURABLE_SUCCESS_RECEIPT_LOSS_AFTER_SINGLE_PERMITTED_DIAGNOSTIC_RUN"),
        ("source_secondary_failure_class", "OUTER_REPORTING_WRAPPER_NAMEERROR_AFTER_TRANSIENT_SERVICE_SUCCESS"),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29), ("failed_or_errored_nodeids_count", 1404),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_is_bound(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_approval_authority_fields_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_boundaries_are_false(field: str) -> None:
    assert _build()[field] is False


def test_retry_priority_and_missing_receipt_facts_are_preserved() -> None:
    approval = _build()
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["retry_failure_context"]["retry_pytest_first_result_authoritative"] is True
    assert [item["failed_or_errored_nodeid_count"] for item in approval["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert len(approval["unavailable_diagnostic_payload_fields"]) == 14
    assert approval["diagnostic_command_executed_once"] is True
    assert approval["transient_success_artifact_returned"] is True
    assert approval["durable_success_receipt_retained"] is False


def test_selected_package_is_authorized_for_future_execution_only() -> None:
    package = _build()["approved_package"]
    assert package == service.APPROVED_PACKAGE
    assert package["selected"] is True and package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False


def test_approved_planning_structures_are_exact_and_unexecuted() -> None:
    approval = _build()
    assert approval["approved_future_receipt_recovery_or_recapture_requirements"] == service.APPROVED_REQUIREMENTS
    assert len(service.APPROVED_REQUIREMENTS) == 42
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in service.APPROVED_REQUIREMENTS)
    assert approval["approved_future_recovery_or_recapture_plan"] == service.APPROVED_PLAN
    assert len(service.APPROVED_PLAN) == 17
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in service.APPROVED_PLAN)
    assert approval["future_controlled_recapture_command_template"] == service.FUTURE_COMMAND_TEMPLATE
    assert service.FUTURE_COMMAND_TEMPLATE["future_recapture_command_executed"] is False
    assert "-p no:cacheprovider" in service.FUTURE_COMMAND_TEMPLATE["future_recapture_command_template"]
    assert approval["approved_future_durable_receipt_safeguards"] == service.APPROVED_SAFEGUARDS
    assert len(service.APPROVED_SAFEGUARDS) == 15


def test_outputs_supporting_and_blocked_packages_remain_closed() -> None:
    approval = _build()
    assert approval["planned_outputs"] == service.PLANNED_OUTPUTS and len(service.PLANNED_OUTPUTS) == 16
    assert all(item["status"] == "AUTHORIZED_NOT_GENERATED" for item in service.PLANNED_OUTPUTS)
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES and len(service.SUPPORTING_PACKAGES) == 3
    assert all(item["selected"] is False and item["approved"] is False for item in service.SUPPORTING_PACKAGES)
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES and len(service.BLOCKED_PACKAGES) == 7
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in service.BLOCKED_PACKAGES)


def test_next_chain_gates_risks_checklist_and_summary_are_valid() -> None:
    approval = _build()
    assert approval["next_chain"] == service.NEXT_CHAIN and len(service.NEXT_CHAIN) == 12
    assert approval["next_gates"] == service.NEXT_GATES and len(service.NEXT_GATES) == 12
    assert approval["risk_controls"] == service.RISK_CONTROLS and len(service.RISK_CONTROLS) == 82
    assert len(approval["checklist"]) == 114
    assert all(item["status"] == service.PASS for item in approval["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in approval["checklist"])
    assert approval["summary"]["total_checks"] == 114
    assert approval["summary"]["passed_checks"] == 114
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0
    assert approval["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_approval_and_attestation_digests_are_deterministic() -> None:
    first = _build()
    second = _build()
    assert first[service.DIGEST_KEY] == second[service.DIGEST_KEY]
    assert first["approval_digest"] == first[service.DIGEST_KEY]
    assert first["operator_attestation"]["operator_attestation_digest"] == second["operator_attestation"]["operator_attestation_digest"]


def test_validator_accepts_valid_approval() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(_build())
    assert result["approval_status"] == service.APPROVAL_STATUS
    assert result["failed_checks"] == 0


@pytest.mark.parametrize("field", sorted(service.STRING_CONFIRMATIONS))
def test_attestation_builder_rejects_changed_string_confirmation(field: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        _attestation(**{field: "WRONG"})


@pytest.mark.parametrize("field", service.BOOLEAN_CONFIRMATION_FIELDS)
def test_attestation_builder_rejects_missing_boolean_confirmation(field: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        _attestation(**{field: False})


@pytest.mark.parametrize(
    "overrides",
    [
        {"operator_reference": ""}, {"operator_attestation_timestamp_utc": "not-utc"},
        {"operator_attestation_phrase": "WRONG"}, {"operator_decision": "WRONG"},
        {"selected_receipt_recovery_or_recapture_package": "WRONG"},
    ],
)
def test_attestation_builder_rejects_invalid_identity_or_selection(overrides: dict[str, object]) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        _attestation(**overrides)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("approval_status", "WRONG"), ("approval_scope", "WRONG"),
        ("selected_receipt_recovery_or_recapture_package", "WRONG"),
        ("source_receipt_recovery_or_recapture_candidate_operator_review_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_candidate_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "WRONG"),
        ("source_primary_failure_class", "WRONG"), ("source_secondary_failure_class", "WRONG"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64), ("source_materialized_payload_digest", "0" * 64),
        ("source_detail_binding_approval_digest", "0" * 64), ("source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context.counts", {}),
        ("priority_1_target_modules", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("diagnostic_command_executed_once", False),
        ("transient_success_artifact_returned", False), ("durable_success_receipt_retained", True),
        ("unavailable_values_reconstructed", True), ("unavailable_values_inferred", True),
        ("operator_attestation.operator_decision", "WRONG"),
        ("operator_attestation.operator_attestation_phrase", "WRONG"),
        ("receipt_recovery_or_recapture_approval_created", False),
        ("receipt_recovery_or_recapture_package_selected", False),
        ("receipt_recovery_or_recapture_package_approved", False),
        ("receipt_recovery_or_recapture_package_authorized", False),
        ("controlled_recapture_package_selected", False), ("controlled_recapture_package_approved", False),
        ("controlled_recapture_package_authorized", False),
        ("ready_for_receipt_recovery_or_recapture_execution", False),
        ("ready_for_controlled_recapture_execution", False),
        ("receipt_recovery_execution_performed", True), ("receipt_recovered", True),
        ("controlled_recapture_execution_performed", True), ("diagnostic_command_executed_in_approval", True),
        ("diagnostic_output_captured_in_approval", True), ("targeted_pytest_performed", True),
        ("full_pytest_performed", True), ("retry_rerun_performed", True),
        ("cache_read_in_approval", True), ("cache_modified_in_approval", True),
        ("terminal_logs_parsed", True), ("operator_logs_parsed", True), ("env_inspection_performed", True),
        ("diagnostic_results_review_created", True),
        ("remediation_or_method_candidate_after_diagnostic_capture_created", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("main_merge_approval_created", True), ("classification_execution_performed_in_approval", True),
        ("remediation_execution_performed", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("main_merge_readiness_claimed", True),
        ("integration_execution_successful", True), ("main_push_performed", True),
        ("integration_branch_pushed", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_approval", True), ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("approved_future_receipt_recovery_or_recapture_requirements", []),
        ("approved_future_recovery_or_recapture_plan", []),
        ("approved_future_durable_receipt_safeguards", []), ("planned_outputs", []),
        ("supporting_packages", []), ("blocked_packages", []), ("next_chain", []),
        ("next_gates", []), ("risk_controls", []), (service.DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_contract_mutation(path: str, replacement: object) -> None:
    approval = deepcopy(_build())
    _set_path(approval, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(approval)


def test_writer_round_trips_and_refuses_overwrite(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(tmp_path, operator_attestation=_attestation())
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1.json"
    approval = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["approval_digest"] == approval[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(approval)["failed_checks"] == 0
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(tmp_path, operator_attestation=_attestation())


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_v1(tmp_path / protected, operator_attestation=_attestation())


@pytest.mark.parametrize(
    "heading",
    [
        "Operator Attestation", "Source Receipt Recovery or Recapture Candidate Operator Review",
        "Source Receipt Recovery or Recapture Candidate", "Source Failure Diagnosis",
        "Source Targeted Diagnostic Output Capture Execution", "Source Approval and Operator Review",
        "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Approval Scope",
        "Selected Receipt Recovery or Recapture Package", "Priority 1 Target Modules",
        "Unavailable Diagnostic Payload Fields", "Future Controlled Recapture Command Template",
        "Approved Future Recovery or Recapture Requirements", "Approved Future Recovery or Recapture Plan",
        "Approved Future Durable Receipt Safeguards", "Planned Outputs", "Supporting Packages",
        "Blocked Packages", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_approval_markdown_v1(_build())
    assert f"## {heading}" in markdown
