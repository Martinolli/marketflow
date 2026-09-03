from copy import deepcopy
import json
import socket

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1()


def test_candidate_builds_offline_without_source_builder_or_execution(monkeypatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1",
        lambda *args, **kwargs: pytest.fail("source builder invoked"),
    )
    monkeypatch.setattr(
        service.source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_v1",
        lambda *args, **kwargs: pytest.fail("diagnostic execution invoked"),
    )
    candidate = _build()
    assert candidate["created_offline"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("schema_version", service.SCHEMA_VERSION),
        ("candidate_status", service.CANDIDATE_STATUS), ("candidate_scope", service.CANDIDATE_SCOPE),
        ("created_offline", True), ("governance_only", True), ("candidate_only", True),
        ("operator_review_required", True),
        ("source_failure_diagnosis_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_failure_diagnosis_status", service.source.DIAGNOSIS_STATUS),
        ("source_failure_diagnosis_scope", service.source.DIAGNOSIS_SCOPE),
        ("retry_execution_commit", service.source.source.RETRY_EXECUTION_COMMIT),
        ("priority_1_total_nodeids", 612), ("top_5_percentage_of_failed_or_errored_nodeids", "43.58974359"),
        ("top_10_count_sum", 1069), ("module_summary_module_count", 29),
        ("failed_or_errored_nodeids_count", 1404),
        ("recommended_receipt_recovery_or_recapture_package", service.RECOMMENDED_PACKAGE),
        ("recommendation_status", "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"),
        ("recommended_next_task", service.NEXT_TASK),
    ],
)
def test_exact_scalar_fields(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_retry_failure_context_is_bound() -> None:
    context = _build()["retry_failure_context"]
    assert context == {
        "retry_execution_branch": service.source.RETRY_EXECUTION_BRANCH,
        "retry_execution_commit": service.source.source.RETRY_EXECUTION_COMMIT,
        "retry_pytest_working_directory": service.source.RETRY_PYTEST_WORKING_DIRECTORY,
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "retry_pytest_first_result_authoritative": True, "retry_pytest_passed": False,
        "retry_pytest_failed": True, "root_full_regression_is_retry_evidence": False,
    }


def test_priority_1_modules_are_exact() -> None:
    candidate = _build()
    assert candidate["priority_1_target_modules"] == service.PRIORITY_1_TARGET_MODULES
    assert [x["failed_or_errored_nodeid_count"] for x in candidate["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert sum(x["failed_or_errored_nodeid_count"] for x in candidate["priority_1_target_modules"]) == 612


def test_receipt_loss_facts_and_unavailable_fields_are_preserved() -> None:
    candidate = _build()
    assert candidate["diagnostic_command_executed_once"] is True
    assert candidate["transient_success_artifact_returned"] is True
    assert candidate["durable_success_receipt_retained"] is False
    assert candidate["unavailable_diagnostic_payload_fields"] == service.UNAVAILABLE_FIELDS
    assert len(candidate["unavailable_diagnostic_payload_fields"]) == 14
    assert candidate["unavailable_values_reconstructed"] is False
    assert candidate["unavailable_values_inferred"] is False


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_candidate_true_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_candidate_boundaries_are_false(field: str) -> None:
    assert _build()[field] is False


def test_packages_are_exact_unselected_and_unexecuted() -> None:
    packages = _build()["proposed_receipt_recovery_or_recapture_packages"]
    assert packages == service.PROPOSED_PACKAGES
    assert len(packages) == 11
    assert sum(x["status"] == "BLOCKED_NOT_ALLOWED" for x in packages) == 7
    assert all(x["selected"] is False and x["approved"] is False and x["executed"] is False for x in packages)
    recommended = next(x for x in packages if x["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"


def test_future_requirements_plan_and_safeguards_are_planning_only() -> None:
    candidate = _build()
    assert candidate["future_receipt_recovery_or_recapture_requirements"] == service.FUTURE_REQUIREMENTS
    assert all(service.FUTURE_REQUIREMENTS.values())
    assert candidate["future_recovery_or_recapture_plan"] == service.FUTURE_PLAN
    assert candidate["future_recovery_or_recapture_plan"]["plan_status"] == "PLANNED_NOT_EXECUTED"
    assert len(candidate["future_recovery_or_recapture_plan"]["steps"]) == 17
    assert candidate["future_controlled_recapture_command_template"] == service.FUTURE_COMMAND_TEMPLATE
    assert candidate["future_controlled_recapture_command_template"]["future_recapture_command_executed"] is False
    assert candidate["future_durable_receipt_safeguards"] == service.FUTURE_RECEIPT_SAFEGUARDS
    assert all(service.FUTURE_RECEIPT_SAFEGUARDS.values())


def test_planned_outputs_and_non_goals_are_exact() -> None:
    candidate = _build()
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 16
    assert set(candidate["planned_outputs"].values()) == {service.PLANNED_NOT_GENERATED}
    assert candidate["non_goals"] == service.NON_GOALS


def test_next_chain_gates_and_risk_controls_are_exact() -> None:
    candidate = _build()
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["next_chain"]) == 14
    assert len(candidate["next_gates"]) == 14


def test_authority_remains_closed() -> None:
    candidate = _build()
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    assert all(candidate[field] == service.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_checklist_and_summary_pass() -> None:
    candidate = _build()
    assert all(x["status"] == service.PASS for x in candidate["checklist"])
    assert all(set(x) == {"check_id", "status", "expected", "actual", "severity", "message"} for x in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(candidate["checklist"])
    assert candidate["summary"]["passed_checks"] == len(candidate["checklist"])
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_candidate_digest_is_deterministic() -> None:
    assert _build()[service.DIGEST_KEY] == _build()[service.DIGEST_KEY]


def test_validator_accepts_valid_candidate() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(_build())
    assert result["failed_checks"] == 0
    assert result["candidate_status"] == service.CANDIDATE_STATUS


def test_full_source_failure_diagnosis_is_accepted() -> None:
    diagnosis = service.source.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1()
    candidate = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(source_failure_diagnosis=diagnosis)
    assert candidate["source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest"] == service.SOURCE_DIAGNOSIS_DIGEST


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"), ("diagnosis_scope", "WRONG"),
        (service.source.DIGEST_KEY, "0" * 64), ("primary_failure_class", "WRONG"),
        ("secondary_failure_class", "WRONG"), ("diagnostic_command_executed_once", False),
        ("transient_success_artifact_returned", False), ("durable_success_receipt_retained", True),
        ("unavailable_values_reconstructed", True), ("unavailable_values_inferred", True),
        ("diagnostic_command_rerun_to_recover_values", True),
    ],
)
def test_changed_source_failure_diagnosis_is_rejected(field: str, replacement: object) -> None:
    diagnosis = service.source.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_execution_failure_diagnosis_v1()
    diagnosis[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(source_failure_diagnosis=diagnosis)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"), ("candidate_scope", "WRONG"),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "WRONG"),
        ("source_primary_failure_class", "WRONG"), ("source_secondary_failure_class", "WRONG"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_operator_review_digest", "0" * 64),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_planning_execution_digest", "0" * 64), ("source_prioritized_planning_digest", "0" * 64),
        ("source_detail_binding_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64), ("source_materialized_payload_digest", "0" * 64),
        ("source_detail_binding_approval_digest", "0" * 64), ("source_recovery_results_review_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64), ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context", {}),
        ("priority_1_target_modules", []), ("priority_1_total_nodeids", 611), ("top_10_count_sum", 1068),
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("diagnostic_command_executed_once", False), ("transient_success_artifact_returned", False),
        ("durable_success_receipt_retained", True), ("unavailable_diagnostic_payload_fields", []),
        ("unavailable_values_reconstructed", True), ("unavailable_values_inferred", True),
        ("receipt_recovery_or_recapture_candidate_created", False),
        ("receipt_recovery_or_recapture_candidate_ready_for_operator_review", False),
        ("proposed_receipt_recovery_or_recapture_packages", []),
        ("recommended_receipt_recovery_or_recapture_package", "WRONG"), ("recommended_package_selected", True),
        ("receipt_recovery_package_selected", True), ("receipt_recovery_package_approved", True),
        ("receipt_recovery_execution_performed", True), ("receipt_recovered", True),
        ("controlled_recapture_package_selected", True), ("controlled_recapture_package_approved", True),
        ("controlled_recapture_execution_performed", True), ("diagnostic_command_executed_in_candidate", True),
        ("diagnostic_output_captured_in_candidate", True), ("targeted_pytest_performed", True),
        ("full_pytest_performed", True), ("retry_rerun_performed", True), ("cache_read_in_candidate", True),
        ("cache_modified_in_candidate", True), ("operator_logs_parsed", True), ("env_inspection_performed", True),
        ("diagnostic_results_review_created", True),
        ("remediation_or_method_candidate_after_diagnostic_capture_created", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True), ("main_merge_approval_created", True),
        ("classification_execution_performed_in_candidate", True), ("remediation_execution_performed", True),
        ("failure_error_separation_claimed", True), ("first_failure_identified", True),
        ("first_error_identified", True), ("traceback_root_cause_claimed", True),
        ("direct_code_remediation_recommended", True), ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True), ("integration_execution_successful", True),
        ("main_push_performed", True), ("integration_branch_pushed", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("future_receipt_recovery_or_recapture_requirements", {}), ("future_recovery_or_recapture_plan", {}),
        ("future_durable_receipt_safeguards", {}), ("planned_outputs", {}), ("non_goals", []),
        ("next_chain", []), ("next_gates", []), ("risk_controls", []), (service.DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_mutation(field: str, replacement: object) -> None:
    candidate = deepcopy(_build())
    candidate[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(candidate)


def test_writer_round_trips_in_temp_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1.json"
    candidate = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["candidate_digest"] == candidate[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(candidate)["failed_checks"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_output(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureCandidateError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_v1(tmp_path / protected)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Failure Diagnosis", "Source Targeted Diagnostic Output Capture Execution",
        "Source Approval and Operator Review", "Source Planning and Detail Binding Evidence",
        "Retry Failure Context", "Candidate Scope", "Receipt Loss Summary",
        "Unavailable Diagnostic Payload Fields", "Priority 1 Target Modules", "Candidate Philosophy",
        "Proposed Receipt Recovery or Recapture Packages", "Recommended Package",
        "Future Recovery or Recapture Requirements", "Future Recovery or Recapture Plan",
        "Future Controlled Recapture Command Template", "Future Durable Receipt Safeguards",
        "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_has_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_candidate_markdown_v1(_build())
    assert f"## {heading}" in markdown
