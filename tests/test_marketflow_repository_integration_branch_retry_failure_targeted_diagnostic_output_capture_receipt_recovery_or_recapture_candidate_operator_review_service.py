from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1()


def _set_path(value: dict, path: str, replacement: object) -> None:
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_operator_review_builds_offline_without_source_builder_or_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: pytest.fail("command attempted"))
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1",
        lambda *args, **kwargs: pytest.fail("source candidate builder called"),
    )
    monkeypatch.setattr(
        service.source.source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
        lambda *args, **kwargs: pytest.fail("diagnostic execution called"),
    )
    review = _build()
    assert review["created_offline"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("review_status", service.REVIEW_STATUS),
        ("review_scope", service.REVIEW_SCOPE),
        ("schema_version", service.SCHEMA_VERSION),
        ("source_receipt_recovery_or_recapture_candidate_digest", service.SOURCE_CANDIDATE_DIGEST),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", service.source.SOURCE_DIAGNOSIS_DIGEST),
        ("source_targeted_diagnostic_output_capture_execution_digest", service.source.source.SOURCE_EXECUTION_DIGEST),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", service.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", service.source.source.SOURCE_BLOCKED_REASON),
        ("source_primary_failure_class", service.source.source.PRIMARY_FAILURE_CLASS),
        ("source_secondary_failure_class", service.source.source.SECONDARY_FAILURE_CLASS),
        ("retry_execution_commit", service.source.source.source.RETRY_EXECUTION_COMMIT),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29), ("failed_or_errored_nodeids_count", 1404),
        ("recommended_receipt_recovery_or_recapture_package", service.RECOMMENDED_PACKAGE),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_is_bound(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_retry_failure_context_and_priority_one_modules_are_bound() -> None:
    review = _build()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["retry_failure_context"]["retry_pytest_first_result_authoritative"] is True
    assert review["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert [row["module_path"] for row in review["priority_1_target_modules"]] == [row["module_path"] for row in service.source.PRIORITY_1_TARGET_MODULES]
    assert [row["failed_or_errored_nodeid_count"] for row in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_receipt_loss_and_unavailable_fields_are_reviewed_without_reconstruction() -> None:
    review = _build()
    assert review["reviewed_receipt_loss_summary"]["diagnostic_command_executed_once"] is True
    assert review["reviewed_receipt_loss_summary"]["transient_success_artifact_returned"] is True
    assert review["reviewed_receipt_loss_summary"]["durable_success_receipt_retained"] is False
    assert review["reviewed_unavailable_diagnostic_payload_fields"] == service.source.UNAVAILABLE_FIELDS
    assert len(review["reviewed_unavailable_diagnostic_payload_fields"]) == 14
    assert review["unavailable_values_reconstructed"] is False
    assert review["unavailable_values_inferred"] is False


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_flags_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_review_boundaries_remain_false(field: str) -> None:
    assert _build()[field] is False


def test_all_eleven_packages_are_reviewed_unselected_and_unexecuted() -> None:
    packages = _build()["reviewed_receipt_recovery_or_recapture_packages"]
    assert packages == service.REVIEWED_PACKAGES
    assert len(packages) == 11
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 7
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


def test_recommended_package_is_reviewed_not_selected() -> None:
    review = _build()
    recommendation = review["recommended_package"]
    assert recommendation["recommended_receipt_recovery_or_recapture_package"] == service.RECOMMENDED_PACKAGE
    assert recommendation["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["recommended_package_selected"] is False


def test_reviewed_planning_structures_have_exact_counts_and_closed_statuses() -> None:
    review = _build()
    assert len(review["reviewed_future_receipt_recovery_or_recapture_requirements"]) == 42
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_receipt_recovery_or_recapture_requirements"])
    assert len(review["reviewed_future_recovery_or_recapture_plan"]) == 17
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_recovery_or_recapture_plan"])
    command = review["reviewed_future_controlled_recapture_command_template"]
    assert command["future_recapture_command_template_review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED"
    assert command["future_recapture_command_executed"] is False
    assert "-p no:cacheprovider" in command["future_recapture_command_template"]
    assert len(review["reviewed_future_durable_receipt_safeguards"]) == 15
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_durable_receipt_safeguards"])
    assert len(review["reviewed_planned_outputs"]) == 16
    assert all(item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert len(review["reviewed_non_goals"]) == 38
    assert all(item["review_status"] == "REVIEWED_ACTIVE" for item in review["reviewed_non_goals"])


def test_recommendation_next_chain_gates_and_risk_controls_are_exact() -> None:
    review = _build()
    assert review["recommendation"] == service.RECOMMENDATION
    assert review["next_chain"] == service.NEXT_CHAIN and len(review["next_chain"]) == 13
    assert review["next_gates"] == service.NEXT_GATES and len(review["next_gates"]) == 13
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass() -> None:
    review = _build()
    assert len(review["checklist"]) == 116
    assert all(item["status"] == service.PASS for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == 116
    assert review["summary"]["passed_checks"] == 116
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_operator_review_digest_is_deterministic() -> None:
    first = _build()
    second = _build()
    assert first[service.DIGEST_KEY] == second[service.DIGEST_KEY]
    assert len(first[service.DIGEST_KEY]) == 64


def test_validator_accepts_valid_review() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(_build())
    assert validation["review_status"] == service.REVIEW_STATUS
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_receipt_recovery_or_recapture_candidate_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", None),
        ("source_primary_failure_class", "WRONG"), ("source_secondary_failure_class", "WRONG"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64),
        ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_planning_execution_digest", "0" * 64),
        ("source_prioritized_planning_digest", "0" * 64),
        ("source_detail_binding_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_materialized_payload_digest", "0" * 64),
        ("source_detail_binding_approval_digest", "0" * 64),
        ("source_recovery_results_review_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context.counts", {}), ("priority_1_target_modules", []),
        ("priority_1_total_nodeids", 611), ("top_10_count_sum", 1068),
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("diagnostic_command_executed_once", False), ("transient_success_artifact_returned", False),
        ("durable_success_receipt_retained", True), ("reviewed_unavailable_diagnostic_payload_fields", []),
        ("unavailable_values_reconstructed", True), ("unavailable_values_inferred", True),
        ("receipt_recovery_or_recapture_candidate_operator_review_created", False),
        ("receipt_recovery_or_recapture_candidate_operator_review_ready", False),
        ("source_candidate_reviewed", False), ("source_failure_diagnosis_reviewed", False),
        ("receipt_loss_failure_class_reviewed", False), ("reviewed_receipt_recovery_or_recapture_packages", []),
        ("recommended_package_selected", True), ("receipt_recovery_package_selected", True),
        ("receipt_recovery_package_approved", True), ("receipt_recovery_package_authorized", True),
        ("receipt_recovery_execution_performed", True), ("receipt_recovered", True),
        ("controlled_recapture_package_selected", True), ("controlled_recapture_package_approved", True),
        ("controlled_recapture_package_authorized", True), ("controlled_recapture_execution_performed", True),
        ("diagnostic_command_executed_in_review", True), ("diagnostic_output_captured_in_review", True),
        ("targeted_pytest_performed", True), ("full_pytest_performed", True), ("retry_rerun_performed", True),
        ("cache_read_in_review", True), ("cache_modified_in_review", True),
        ("terminal_logs_parsed", True), ("operator_logs_parsed", True), ("env_inspection_performed", True),
        ("diagnostic_results_review_created", True),
        ("remediation_or_method_candidate_after_diagnostic_capture_created", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("main_merge_approval_created", True), ("classification_execution_performed_in_review", True),
        ("remediation_execution_performed", True), ("failure_modules_classified", True),
        ("error_modules_classified", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("main_merge_readiness_claimed", True),
        ("integration_execution_successful", True), ("main_push_performed", True),
        ("integration_branch_pushed", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_review", True), ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("reviewed_future_receipt_recovery_or_recapture_requirements", []),
        ("reviewed_future_recovery_or_recapture_plan", []),
        ("reviewed_future_controlled_recapture_command_template", {}),
        ("reviewed_future_durable_receipt_safeguards", []), ("reviewed_planned_outputs", []),
        ("reviewed_non_goals", []), ("next_chain", []), ("next_gates", []), ("risk_controls", []),
        (service.DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_contract_mutation(path: str, replacement: object) -> None:
    review = deepcopy(_build())
    _set_path(review, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(review)


def test_writer_round_trips_in_temporary_directory_and_refuses_overwrite(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1.json"
    review = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["operator_review_digest"] == review[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(review)["failed_checks"] == 0
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_v1(tmp_path / protected)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Receipt Recovery or Recapture Candidate", "Source Failure Diagnosis",
        "Source Targeted Diagnostic Output Capture Execution", "Source Approval and Operator Review",
        "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Review Scope",
        "Receipt Loss Summary", "Unavailable Diagnostic Payload Fields", "Priority 1 Target Modules",
        "Reviewed Candidate Philosophy", "Reviewed Receipt Recovery or Recapture Packages",
        "Recommended Package", "Reviewed Future Recovery or Recapture Requirements",
        "Reviewed Future Recovery or Recapture Plan", "Reviewed Future Controlled Recapture Command Template",
        "Reviewed Future Durable Receipt Safeguards", "Reviewed Planned Outputs", "Reviewed Non-Goals",
        "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_operator_review_markdown_v1(_build())
    assert f"## {heading}" in markdown
