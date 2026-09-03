from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1()


def _set_path(value: dict, path: str, replacement: object) -> None:
    parts = path.split(".")
    target = value
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: pytest.fail("command attempted"))
    artifact = _build()
    assert artifact["created_offline"] is True
    assert artifact["candidate_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("candidate_status", service.CANDIDATE_STATUS),
        ("candidate_scope", service.CANDIDATE_SCOPE),
        ("source_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_prioritized_planning_review_digest", service.SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST),
        ("source_results_review_manifest_digest", service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_planning_reentry_execution_digest", service.SOURCE_PLANNING_EXECUTION_DIGEST),
        ("source_prioritized_planning_digest", service.SOURCE_PRIORITIZED_PLANNING_DIGEST),
        ("source_planning_digest_manifest_digest", service.SOURCE_PLANNING_MANIFEST_DIGEST),
        ("selected_after_v2_planning_package", service.SELECTED_AFTER_V2_PLANNING_PACKAGE),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("recommended_targeted_diagnostic_capture_package", service.RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_is_bound(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_source_review_readiness_is_bound() -> None:
    summary = _build()["source_results_review_summary"]
    assert summary["status"] == service.source.REVIEW_STATUS
    assert summary["ready_for_targeted_diagnostic_output_capture_candidate"] is True
    assert summary["ready_for_retry_candidate"] is False


def test_retry_failure_counts_are_bound() -> None:
    assert _build()["retry_failure_context"]["counts"] == {
        "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
    }


def test_priority_one_paths_and_counts_are_bound() -> None:
    rows = _build()["priority_1_top_module_groups"]
    assert [row["module_path"] for row in rows] == [row["module_path"] for row in service.TOP_MODULES]
    assert [row["failed_or_errored_nodeid_count"] for row in rows] == [136, 131, 122, 112, 111]
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 612


def test_priority_tiers_and_planning_buckets_are_bound() -> None:
    artifact = _build()
    assert artifact["priority_tier_summary"] == service.PRIORITY_TIERS
    assert artifact["planning_buckets_summary"] == service.PLANNING_BUCKETS
    assert all(item["status"] == "PLANNING_ONLY_NOT_EXECUTED" for item in artifact["planning_buckets_summary"])


def test_proposed_packages_are_complete_and_unselected() -> None:
    packages = _build()["proposed_diagnostic_capture_packages"]
    assert len(packages) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


def test_recommended_package_is_defined_but_not_selected() -> None:
    artifact = _build()
    assert artifact["recommended_package"]["package_id"] == service.PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS
    assert artifact["recommended_package"]["selected"] is False
    assert artifact["diagnostic_capture_package_selected"] is False


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_candidate_flags_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_candidate_boundaries_remain_false(field: str) -> None:
    assert _build()[field] is False


def test_future_requirements_are_complete_and_true() -> None:
    requirements = _build()["future_diagnostic_capture_requirements"]
    assert requirements == service.FUTURE_REQUIREMENTS
    assert len(requirements) == 35
    assert all(requirements.values())


def test_future_plan_and_command_are_planned_not_executed() -> None:
    artifact = _build()
    assert artifact["future_diagnostic_capture_plan"] == {"status": service.PLANNED_NOT_EXECUTED, "steps": service.FUTURE_PLAN}
    assert artifact["future_diagnostic_command_template"] == service.FUTURE_COMMAND_TEMPLATE
    assert artifact["future_diagnostic_command_template"]["future_diagnostic_command_executed"] is False
    assert "-p no:cacheprovider" in artifact["future_diagnostic_command_template"]["future_diagnostic_command_template"]


def test_planned_outputs_non_goals_and_governance_lists_are_complete() -> None:
    artifact = _build()
    assert [item["output_id"] for item in artifact["planned_outputs"]] == service.PLANNED_OUTPUT_IDS
    assert all(item["status"] == service.PLANNED_NOT_GENERATED for item in artifact["planned_outputs"])
    assert artifact["non_goals"] == service.NON_GOALS
    assert artifact["next_chain"] == service.NEXT_CHAIN
    assert artifact["next_gates"] == service.NEXT_GATES
    assert artifact["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass() -> None:
    artifact = _build()
    assert artifact["checklist"]
    assert all(item["status"] == service.PASS for item in artifact["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in artifact["checklist"])
    assert artifact["summary"]["total_checks"] == len(artifact["checklist"])
    assert artifact["summary"]["passed_checks"] == len(artifact["checklist"])
    assert artifact["summary"]["failed_checks"] == 0
    assert artifact["summary"]["blocker_count"] == 0
    assert artifact["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_candidate_digest_is_deterministic() -> None:
    first = _build()
    second = _build()
    assert first[service.DIGEST_KEY] == second[service.DIGEST_KEY]
    assert first["candidate_digest"] == first[service.DIGEST_KEY]


def test_validator_accepts_valid_candidate() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(_build())
    assert validation["failed_checks"] == 0
    assert validation["candidate_status"] == service.CANDIDATE_STATUS


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"), ("candidate_scope", "WRONG"),
        ("source_results_review_digest", "0" * 64),
        ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_results_review_manifest_digest", "0" * 64),
        ("source_planning_reentry_execution_digest", "0" * 64),
        ("source_prioritized_planning_digest", "0" * 64),
        ("source_planning_digest_manifest_digest", "0" * 64),
        ("selected_after_v2_planning_package", "WRONG"),
        ("source_detail_binding_reattempt_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", None),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context.counts", {}),
        ("priority_1_top_module_groups", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("planning_buckets_summary", []),
        ("targeted_diagnostic_output_capture_candidate_created", False),
        ("targeted_diagnostic_output_capture_candidate_ready_for_operator_review", False),
        ("proposed_diagnostic_capture_packages", []), ("recommended_package.selected", True),
        ("diagnostic_capture_package_selected", True), ("diagnostic_capture_package_approved", True),
        ("diagnostic_capture_package_authorized", True), ("diagnostic_capture_execution_performed", True),
        ("diagnostic_capture_results_review_created", True), ("diagnostic_output_captured", True),
        ("diagnostic_command_executed", True), ("targeted_pytest_performed", True),
        ("retry_rerun_performed", True), ("full_pytest_performed", True),
        ("cache_read_in_candidate", True), ("cache_modified_in_candidate", True),
        ("planning_reentry_rerun_performed", True), ("detail_binding_reattempt_rerun_performed", True),
        ("materialization_execution_rerun_performed", True), ("source_recovery_rerun_performed", True),
        ("classification_execution_performed_in_candidate", True), ("failure_modules_classified", True),
        ("error_modules_classified", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("main_merge_readiness_claimed", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("main_merge_approval_created", True), ("integration_execution_successful", True),
        ("main_push_performed", True), ("integration_branch_pushed", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True), ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("future_diagnostic_capture_requirements", {}), ("future_diagnostic_capture_plan", {}),
        ("planned_outputs", []), ("next_chain", []), ("risk_controls", []),
        ("candidate_digest", "0" * 64),
    ],
)
def test_validator_rejects_contract_mutation(path: str, replacement: object) -> None:
    artifact = deepcopy(_build())
    _set_path(artifact, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(artifact)


def test_builder_accepts_exact_source_results_review() -> None:
    source_review = service._expected_source_review()
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(source_results_review=source_review)
    assert artifact["source_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST


def test_builder_rejects_changed_source_results_review() -> None:
    source_review = service._expected_source_review()
    source_review[service.source.REVIEW_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(source_results_review=source_review)


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1.json").read_text(encoding="utf-8"))
    assert receipt["candidate_digest"] == payload[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(payload)["failed_checks"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_v1(tmp_path / protected)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Remediation or Method Results Review", "Source Planning Reentry with Complete Detail",
        "Source Detail Binding Results Review", "Source Materialization Results Review", "Retry Failure Context",
        "Candidate Scope", "Reviewed Priority Planning Facts", "Priority 1 Top Module Groups", "Planning Buckets",
        "Candidate Philosophy", "Proposed Diagnostic Capture Packages", "Recommended Package",
        "Future Diagnostic Capture Requirements", "Future Diagnostic Capture Plan", "Future Diagnostic Command Template",
        "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_for_top_module_groups_markdown_v1(_build())
    assert f"## {heading}" in markdown
