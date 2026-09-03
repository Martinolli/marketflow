from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_service
    as service,
)


def _attestation_kwargs() -> dict:
    return {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1,
        **service.STRING_CONFIRMATIONS,
        **{field: True for field in service.BOOLEAN_CONFIRMATION_FIELDS},
    }


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1(**_attestation_kwargs())


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(operator_attestation=_attestation())


def _set_path(value: dict, path: str, replacement: object) -> None:
    parts = path.split(".")
    target = value
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_targeted_diagnostic_capture_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1
    assert attestation["operator_attestation_version"] == service.ATTESTATION_VERSION
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert len(attestation["operator_attestation_digest"]) == 64


def test_approval_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: pytest.fail("command attempted"))
    approval = _build()
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("approval_status", service.APPROVAL_STATUS),
        ("approval_scope", service.APPROVAL_SCOPE),
        ("selected_targeted_diagnostic_capture_package", service.SELECTED_PACKAGE),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_targeted_diagnostic_output_capture_candidate_digest", service.source.SOURCE_CANDIDATE_DIGEST),
        ("source_results_review_digest", service.source.SOURCE_BINDINGS["source_results_review_digest"]),
        ("source_prioritized_planning_review_digest", service.source.SOURCE_BINDINGS["source_prioritized_planning_review_digest"]),
        ("source_results_review_manifest_digest", service.source.SOURCE_BINDINGS["source_results_review_manifest_digest"]),
        ("source_planning_execution_digest", service.source.SOURCE_BINDINGS["source_planning_execution_digest"]),
        ("source_prioritized_planning_digest", service.source.SOURCE_BINDINGS["source_prioritized_planning_digest"]),
        ("source_planning_digest_manifest_digest", service.source.SOURCE_BINDINGS["source_planning_digest_manifest_digest"]),
        ("retry_execution_commit", service.source.source.RETRY_EXECUTION_COMMIT),
        ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_is_exact(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_retry_and_priority_one_facts_are_bound() -> None:
    approval = _build()
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert [item["module_path"] for item in approval["priority_1_top_module_groups"]] == [item["module_path"] for item in service.source.source.TOP_MODULES]
    assert [item["failed_or_errored_nodeid_count"] for item in approval["priority_1_top_module_groups"]] == [136, 131, 122, 112, 111]


def test_operator_decision_and_attestation_phrase_match() -> None:
    attestation = _build()["operator_attestation"]
    assert attestation["operator_decision"] == "APPROVE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE"
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_APPROVAL_ATTESTATION_PHRASE_V1


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_approved_authority_fields_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_approval_boundaries_remain_false(field: str) -> None:
    assert _build()[field] is False


def test_selected_package_is_approved_for_future_execution_only() -> None:
    package = _build()["approved_package"]
    assert package == service.APPROVED_PACKAGE
    assert package["selected"] is True
    assert package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False


def test_requirements_are_approved_but_not_executed() -> None:
    requirements = _build()["approved_future_diagnostic_capture_requirements"]
    assert requirements == service.APPROVED_REQUIREMENTS
    assert len(requirements) == 35
    assert all(item["approval_status"] == "APPROVED_FOR_FUTURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_EXECUTION_ONLY" for item in requirements)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in requirements)


def test_plan_is_approved_but_not_executed() -> None:
    plan = _build()["approved_future_diagnostic_capture_plan"]
    assert plan == service.APPROVED_PLAN
    assert len(plan) == 13
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in plan)


def test_command_template_is_approved_but_not_executed() -> None:
    template = _build()["future_diagnostic_command_template"]
    assert template == service.FUTURE_COMMAND_TEMPLATE
    assert template["future_diagnostic_command_template_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED"
    assert template["future_diagnostic_command_is_retry"] is False
    assert template["future_diagnostic_command_is_full_pytest"] is False
    assert template["future_diagnostic_command_executed"] is False


def test_planned_outputs_supporting_and_blocked_packages_are_closed() -> None:
    approval = _build()
    assert approval["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(approval["planned_outputs"]) == 14
    assert all(item["status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["planned_outputs"])
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert all(item["selected"] is False and item["approved"] is False for item in approval["supporting_packages"])
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert len(approval["blocked_packages"]) == 6
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in approval["blocked_packages"])


def test_next_chain_gates_and_risk_controls_are_exact() -> None:
    approval = _build()
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass() -> None:
    approval = _build()
    assert approval["checklist"]
    assert all(item["status"] == service.PASS for item in approval["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(approval["checklist"])
    assert approval["summary"]["passed_checks"] == len(approval["checklist"])
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0
    assert approval["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_approval_digest_is_deterministic() -> None:
    first = _build()
    second = _build()
    assert first[service.DIGEST_KEY] == second[service.DIGEST_KEY]
    assert first["approval_digest"] == first[service.DIGEST_KEY]


def test_validator_accepts_valid_approval() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(_build())
    assert validation["failed_checks"] == 0
    assert validation["approval_status"] == service.APPROVAL_STATUS


@pytest.mark.parametrize("field", sorted(service.STRING_CONFIRMATIONS))
def test_attestation_rejects_changed_digest_or_package_confirmation(field: str) -> None:
    values = _attestation_kwargs()
    values[field] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1(**values)


@pytest.mark.parametrize("field", service.BOOLEAN_CONFIRMATION_FIELDS)
def test_attestation_rejects_false_boundary_confirmation(field: str) -> None:
    values = _attestation_kwargs()
    values[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("operator_reference", ""), ("operator_attestation_timestamp_utc", "2026-08-23T00:00:00"),
        ("operator_attestation_phrase", "WRONG"), ("operator_decision", "WRONG"),
        ("selected_targeted_diagnostic_capture_package", "WRONG"),
    ],
)
def test_attestation_rejects_invalid_identity_or_core_authority(field: str, replacement: object) -> None:
    values = _attestation_kwargs()
    values[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_attestation_v1(**values)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("approval_status", "WRONG"), ("approval_scope", "WRONG"),
        ("selected_targeted_diagnostic_capture_package", "WRONG"),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_results_review_manifest_digest", "0" * 64), ("source_planning_execution_digest", "0" * 64),
        ("source_prioritized_planning_digest", "0" * 64), ("source_planning_digest_manifest_digest", "0" * 64),
        ("source_detail_binding_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_materialization_results_review_digest", "0" * 64),
        ("source_materialized_payload_digest", "0" * 64), ("source_detail_binding_approval_digest", "0" * 64),
        ("source_prior_blocked_detail_binding_execution_digest", "0" * 64),
        ("source_prior_blocked_detail_binding_reason", None), ("source_recovery_results_review_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64), ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context.counts", {}),
        ("priority_1_top_module_groups", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("operator_attestation.operator_decision", "WRONG"),
        ("operator_attestation.operator_attestation_phrase", "WRONG"),
        ("targeted_diagnostic_output_capture_approval_created", False),
        ("diagnostic_capture_package_selected", False), ("diagnostic_capture_package_approved", False),
        ("diagnostic_capture_package_authorized", False),
        ("ready_for_targeted_diagnostic_output_capture_execution", False),
        ("diagnostic_capture_execution_performed", True), ("diagnostic_capture_results_review_created", True),
        ("diagnostic_output_captured", True), ("diagnostic_command_executed", True),
        ("targeted_pytest_performed", True), ("full_pytest_performed", True), ("retry_rerun_performed", True),
        ("cache_read_in_approval", True), ("cache_modified_in_approval", True),
        ("planning_reentry_rerun_performed", True), ("detail_binding_reattempt_rerun_performed", True),
        ("materialization_execution_rerun_performed", True), ("source_recovery_rerun_performed", True),
        ("code_remediation_executed", True), ("classification_execution_performed_in_approval", True),
        ("failure_error_separation_claimed", True), ("first_failure_identified", True),
        ("first_error_identified", True), ("traceback_root_cause_claimed", True),
        ("direct_code_remediation_recommended", True), ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("main_merge_approval_created", True),
        ("integration_execution_successful", True), ("main_push_performed", True),
        ("integration_branch_pushed", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_approval", True), ("env_inspection_performed_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True), ("dataset_generation_performed_in_approval", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("approved_future_diagnostic_capture_requirements", []),
        ("approved_future_diagnostic_capture_plan", []), ("planned_outputs", []),
        ("next_chain", []), ("risk_controls", []), ("approval_digest", "0" * 64),
    ],
)
def test_validator_rejects_contract_mutation(path: str, replacement: object) -> None:
    approval = deepcopy(_build())
    _set_path(approval, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(approval)


def test_builder_accepts_exact_source_operator_review() -> None:
    approval = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(source_operator_review=service._expected_source_review(), operator_attestation=_attestation())
    assert approval["source_targeted_diagnostic_output_capture_candidate_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST


def test_builder_rejects_changed_source_operator_review() -> None:
    review = service._expected_source_review()
    review[service.source.DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(source_operator_review=review, operator_attestation=_attestation())


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(tmp_path, operator_attestation=_attestation())
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1.json"
    approval = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["approval_digest"] == approval[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(approval)["failed_checks"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_v1(tmp_path / protected, operator_attestation=_attestation())


@pytest.mark.parametrize(
    "heading",
    [
        "Operator Attestation", "Source Targeted Diagnostic Output Capture Candidate Operator Review",
        "Source Targeted Diagnostic Output Capture Candidate", "Source Remediation or Method Results Review",
        "Source Planning Reentry with Complete Detail", "Source Detail Binding Results Review",
        "Source Materialization Results Review", "Retry Failure Context", "Approval Scope",
        "Selected Diagnostic Capture Package", "Priority 1 Top Module Groups", "Future Diagnostic Command Template",
        "Approved Future Diagnostic Capture Requirements", "Approved Future Diagnostic Capture Plan",
        "Planned Outputs", "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_approval_markdown_v1(_build())
    assert f"## {heading}" in markdown
