from __future__ import annotations

from copy import deepcopy
import json
import socket

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1()


def _set_path(value: dict, path: str, replacement: object) -> None:
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_builder_is_offline_and_does_not_invoke_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
        lambda *args, **kwargs: pytest.fail("execution invoked"),
    )
    diagnosis = _build()
    assert diagnosis["created_offline"] is True
    assert diagnosis["diagnosis_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("schema_version", service.SCHEMA_VERSION),
        ("diagnosis_status", service.DIAGNOSIS_STATUS), ("diagnosis_scope", service.DIAGNOSIS_SCOPE),
        ("source_execution_artifact_kind", service.source.ARTIFACT_KIND_BLOCKED),
        ("source_execution_status", service.source.EXECUTION_STATUS_BLOCKED),
        ("source_execution_scope", service.source.EXECUTION_SCOPE),
        ("primary_failure_class", service.PRIMARY_FAILURE_CLASS),
        ("secondary_failure_class", service.SECONDARY_FAILURE_CLASS),
        ("selected_targeted_diagnostic_capture_package", service.SELECTED_PACKAGE),
        ("retry_execution_branch", service.RETRY_EXECUTION_BRANCH),
        ("retry_execution_commit", service.source.RETRY_EXECUTION_COMMIT),
        ("retry_pytest_working_directory", service.RETRY_PYTEST_WORKING_DIRECTORY),
        ("retry_pytest_passed_count", 24877), ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112), ("retry_pytest_skipped_count", 7),
        ("retry_pytest_first_result_authoritative", True), ("retry_pytest_passed", False),
        ("retry_pytest_failed", True), ("root_full_regression_is_retry_evidence", False),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29), ("failed_or_errored_nodeids_count", 1404),
        ("recommended_next_package", service.RECOMMENDED_PACKAGE),
        ("recommended_next_task", service.NEXT_TASK),
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


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_acknowledged_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_unavailable_and_closed_boundaries_are_false(field: str) -> None:
    assert _build()[field] is False


def test_findings_are_exact_and_complete() -> None:
    diagnosis = _build()
    assert diagnosis["diagnosis_findings"] == service.FINDINGS
    assert list(diagnosis["diagnosis_findings"]) == [f"finding_{index}" for index in range(1, 13)]


def test_failure_domains_are_exact_and_classified() -> None:
    domains = {item["domain_id"]: item for item in _build()["failure_classification_domains"]}
    assert len(domains) == 12
    assert domains["durable_success_receipt_persistence"]["classification"] == "FAILED_PRIMARY"
    assert domains["outer_reporting_wrapper"]["classification"] == "FAILED_CONTRIBUTING"
    for domain_id in (
        "diagnostic_cwd_and_python", "target_module_scope", "cacheprovider_boundary",
        "post_execution_git_boundaries",
    ):
        assert domains[domain_id]["classification"] == "NOT_FAILED_BY_AVAILABLE_EVIDENCE"
    assert all(set(item) == {"domain_id", "classification", "evidence_summary", "boundary_status", "next_action_required"} for item in domains.values())


def test_unavailable_data_is_explicit_and_not_reconstructed() -> None:
    diagnosis = _build()
    assert diagnosis["unavailable_due_to_receipt_loss"] == service.UNAVAILABLE_FIELDS
    assert len(diagnosis["unavailable_due_to_receipt_loss"]) == 14
    assert diagnosis["unavailable_values_reconstructed"] is False
    assert diagnosis["unavailable_values_inferred"] is False
    assert diagnosis["diagnostic_command_rerun_to_recover_values"] is False


def test_recommendation_is_candidate_only() -> None:
    diagnosis = _build()
    for field, expected in service.RECOMMENDATION.items():
        assert diagnosis[field] == expected
    assert diagnosis["ready_for_receipt_recovery_or_recapture_candidate"] is True
    assert diagnosis["ready_for_diagnostic_results_review"] is False
    assert diagnosis["ready_for_remediation_or_method_candidate"] is False
    assert diagnosis["ready_for_retry_candidate"] is False


def test_future_packages_are_listed_not_selected_or_approved() -> None:
    packages = _build()["possible_future_packages"]
    assert packages == service.FUTURE_PACKAGES
    assert len(packages) == 10
    assert all(item["selected"] is False and item["approved"] is False for item in packages)
    assert [item["status"] for item in packages[:4]] == ["FUTURE_CANDIDATE_OPTION_NOT_SELECTED"] * 4
    assert [item["status"] for item in packages[4:]] == ["BLOCKED_NOT_ALLOWED"] * 6


def test_next_chain_gates_and_risk_controls_are_exact() -> None:
    diagnosis = _build()
    assert diagnosis["next_chain"] == service.NEXT_CHAIN
    assert diagnosis["next_gates"] == service.NEXT_GATES
    assert diagnosis["risk_controls"] == service.RISK_CONTROLS
    assert len(diagnosis["next_chain"]) == 15
    assert len(diagnosis["next_gates"]) == 15


def test_checklist_and_summary_pass() -> None:
    diagnosis = _build()
    assert all(item["status"] == service.PASS for item in diagnosis["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in diagnosis["checklist"])
    assert diagnosis["summary"]["total_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["passed_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["failed_checks"] == 0
    assert diagnosis["summary"]["blocker_count"] == 0
    assert diagnosis["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_digest_is_deterministic() -> None:
    assert _build()[service.DIGEST_KEY] == _build()[service.DIGEST_KEY]


def test_validator_accepts_diagnosis() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(_build())
    assert validation["failed_checks"] == 0
    assert validation["diagnosis_status"] == service.DIAGNOSIS_STATUS


def test_exact_source_execution_is_accepted() -> None:
    diagnosis = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(
        source_execution=service._expected_source_execution()
    )
    assert diagnosis["source_targeted_diagnostic_output_capture_execution_digest"] == service.SOURCE_EXECUTION_DIGEST


@pytest.mark.parametrize("field", sorted(service._expected_source_execution()))
def test_changed_source_execution_is_rejected(field: str) -> None:
    execution = service._expected_source_execution()
    execution[field] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(source_execution=execution)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"), ("diagnosis_scope", "WRONG"),
        ("created_offline", False), ("governance_only", False), ("diagnosis_only", False),
        ("source_targeted_diagnostic_output_capture_execution_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "WRONG"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_planning_execution_digest", "0" * 64), ("source_prioritized_planning_digest", "0" * 64),
        ("source_detail_binding_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64), ("source_materialized_payload_digest", "0" * 64),
        ("source_detail_binding_approval_digest", "0" * 64), ("source_recovery_results_review_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64), ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_counts", {}),
        ("priority_1_top_module_groups", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("primary_failure_class", "WRONG"),
        ("secondary_failure_class", "WRONG"), ("diagnosis_findings", {}),
        ("failure_classification_domains", []), ("durable_success_receipt_retained", True),
        ("unavailable_due_to_receipt_loss", []), ("unavailable_values_reconstructed", True),
        ("unavailable_values_inferred", True), ("diagnostic_command_rerun_to_recover_values", True),
        ("targeted_pytest_rerun_performed", True), ("full_pytest_performed", True),
        ("retry_rerun_performed", True), ("cache_read_in_diagnosis", True),
        ("cache_modified_in_diagnosis", True), ("operator_logs_parsed", True),
        ("env_inspection_performed", True), ("diagnostic_results_review_created", True),
        ("remediation_or_method_candidate_created", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("classification_execution_performed", True),
        ("remediation_execution_performed", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("first_order_claim_made", True), ("traceback_root_cause_claimed", True),
        ("direct_code_remediation_recommended", True), ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True), ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True), ("integration_branch_pushed", True),
        ("main_push_performed", True), ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_diagnosis", True),
        ("market_data_acquisition_performed_in_diagnosis", True),
        ("dataset_generation_performed_in_diagnosis", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("recommended_next_package", "WRONG"), ("next_chain", []), ("next_gates", []),
        ("risk_controls", []), (service.DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_mutation(path: str, replacement: object) -> None:
    diagnosis = deepcopy(_build())
    _set_path(diagnosis, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(diagnosis)


def test_writer_round_trips_in_temp_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1.json").read_text(encoding="utf-8"))
    assert receipt["diagnosis_digest"] == payload[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(payload)["failed_checks"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_output(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureExecutionFailureDiagnosisError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1(tmp_path / protected)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Targeted Diagnostic Output Capture Execution", "Source Approval and Operator Review",
        "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Diagnosis Scope",
        "Execution Failure Summary", "Transient Success and Durable Receipt Loss",
        "Unavailable Diagnostic Payload Fields", "Failure Classification Domains", "Unsupported Claims Boundary",
        "Recommendation", "Possible Future Packages", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_has_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_markdown_v1(_build())
    assert f"## {heading}" in markdown
