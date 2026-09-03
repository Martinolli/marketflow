from __future__ import annotations

from copy import deepcopy
import json
import socket
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1()


def _set_path(value: dict, path: str, replacement: object) -> None:
    parts = path.split(".")
    target = value
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_operator_review_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: pytest.fail("command attempted"))
    review = _build()
    assert review["created_offline"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("review_status", service.REVIEW_STATUS),
        ("review_scope", service.REVIEW_SCOPE),
        ("source_targeted_diagnostic_output_capture_candidate_digest", service.SOURCE_CANDIDATE_DIGEST),
        ("source_results_review_digest", service.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_prioritized_planning_review_digest", service.source.SOURCE_PRIORITIZED_PLANNING_REVIEW_DIGEST),
        ("source_results_review_manifest_digest", service.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_planning_execution_digest", service.source.SOURCE_PLANNING_EXECUTION_DIGEST),
        ("source_prioritized_planning_digest", service.source.SOURCE_PRIORITIZED_PLANNING_DIGEST),
        ("source_planning_digest_manifest_digest", service.source.SOURCE_PLANNING_MANIFEST_DIGEST),
        ("selected_after_v2_planning_package", service.source.SELECTED_AFTER_V2_PLANNING_PACKAGE),
        ("retry_execution_commit", service.source.RETRY_EXECUTION_COMMIT),
        ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("recommended_targeted_diagnostic_capture_package", service.RECOMMENDED_TARGETED_DIAGNOSTIC_CAPTURE_PACKAGE),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_is_bound(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_retry_failure_counts_and_source_readiness_are_bound() -> None:
    review = _build()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["source_candidate_summary"]["status"] == service.source.CANDIDATE_STATUS
    assert review["source_candidate_summary"]["candidate_ready"] is True
    assert review["source_candidate_summary"]["ready_for_retry_candidate"] is False
    assert review["source_results_review_summary"]["status"] == service.source.source.REVIEW_STATUS


def test_priority_one_paths_counts_and_totals_are_reviewed() -> None:
    review = _build()
    rows = review["priority_1_top_module_groups"]
    assert [row["module_path"] for row in rows] == [row["module_path"] for row in service.source.TOP_MODULES]
    assert [row["failed_or_errored_nodeid_count"] for row in rows] == [136, 131, 122, 112, 111]
    assert review["priority_1_total_nodeids"] == 612
    assert review["top_10_count_sum"] == 1069
    assert review["module_summary_module_count"] == 29
    assert review["failed_or_errored_nodeids_count"] == 1404


def test_planning_buckets_are_reviewed_without_execution() -> None:
    assert _build()["planning_buckets_summary"] == service.source.PLANNING_BUCKETS
    assert all(item["status"] == "PLANNING_ONLY_NOT_EXECUTED" for item in _build()["planning_buckets_summary"])


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_flags_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_review_boundaries_remain_false(field: str) -> None:
    assert _build()[field] is False


def test_all_twelve_packages_are_reviewed_and_unselected() -> None:
    packages = _build()["reviewed_diagnostic_capture_packages"]
    assert packages == service.REVIEWED_PACKAGES
    assert len(packages) == 12
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


def test_recommended_package_is_reviewed_not_selected() -> None:
    review = _build()
    assert review["recommendation"]["recommended_targeted_diagnostic_capture_package"] == service.PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS
    assert review["recommendation"]["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["recommendation"]["selected"] is False
    assert review["diagnostic_capture_package_selected"] is False


def test_future_requirements_are_reviewed_not_executed() -> None:
    requirements = _build()["reviewed_future_diagnostic_capture_requirements"]
    assert requirements == service.REVIEWED_REQUIREMENTS
    assert len(requirements) == 35
    assert all(item["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_TARGETED_DIAGNOSTIC_CAPTURE" for item in requirements)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in requirements)


def test_future_plan_is_reviewed_not_executed() -> None:
    plan = _build()["reviewed_future_diagnostic_capture_plan"]
    assert plan == service.REVIEWED_PLAN
    assert len(plan) == 13
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" for item in plan)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in plan)


def test_command_template_is_reviewed_not_executed() -> None:
    template = _build()["reviewed_future_diagnostic_command_template"]
    assert template == service.REVIEWED_COMMAND_TEMPLATE
    assert template["future_diagnostic_command_template_review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED"
    assert template["future_diagnostic_command_executed"] is False
    assert "-p no:cacheprovider" in template["future_diagnostic_command_template"]


def test_outputs_and_non_goals_are_reviewed() -> None:
    review = _build()
    assert review["reviewed_planned_outputs"] == service.REVIEWED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 14
    assert all(item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert all(item["review_status"] == "REVIEWED_ACTIVE" for item in review["reviewed_non_goals"])


def test_next_chain_gates_and_risk_controls_are_exact() -> None:
    review = _build()
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass() -> None:
    review = _build()
    assert review["checklist"]
    assert all(item["status"] == service.PASS for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == len(review["checklist"])
    assert review["summary"]["passed_checks"] == len(review["checklist"])
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_operator_review_digest_is_deterministic() -> None:
    first = _build()
    second = _build()
    assert first[service.DIGEST_KEY] == second[service.DIGEST_KEY]
    assert first["operator_review_digest"] == first[service.DIGEST_KEY]


def test_validator_accepts_valid_review() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(_build())
    assert validation["failed_checks"] == 0
    assert validation["review_status"] == service.REVIEW_STATUS


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_targeted_diagnostic_output_capture_candidate_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64), ("source_prioritized_planning_review_digest", "0" * 64),
        ("source_results_review_manifest_digest", "0" * 64), ("source_planning_execution_digest", "0" * 64),
        ("source_prioritized_planning_digest", "0" * 64), ("source_planning_digest_manifest_digest", "0" * 64),
        ("selected_after_v2_planning_package", "WRONG"),
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
        ("failed_or_errored_nodeids_count", 1403), ("planning_buckets_summary", []),
        ("targeted_diagnostic_output_capture_candidate_operator_review_created", False),
        ("targeted_diagnostic_output_capture_candidate_operator_review_ready", False),
        ("source_candidate_reviewed", False), ("reviewed_diagnostic_capture_packages", []),
        ("recommendation.selected", True), ("diagnostic_capture_package_selected", True),
        ("diagnostic_capture_package_approved", True), ("diagnostic_capture_package_authorized", True),
        ("diagnostic_capture_execution_performed", True), ("diagnostic_capture_results_review_created", True),
        ("diagnostic_output_captured", True), ("diagnostic_command_executed", True),
        ("targeted_pytest_performed", True), ("retry_rerun_performed", True), ("full_pytest_performed", True),
        ("cache_read_in_review", True), ("cache_modified_in_review", True),
        ("planning_reentry_rerun_performed", True), ("detail_binding_reattempt_rerun_performed", True),
        ("materialization_execution_rerun_performed", True), ("source_recovery_rerun_performed", True),
        ("classification_execution_performed_in_review", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("main_merge_readiness_claimed", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("main_merge_approval_created", True), ("integration_execution_successful", True),
        ("main_push_performed", True), ("integration_branch_pushed", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True), ("dataset_generation_performed_in_review", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("reviewed_future_diagnostic_capture_requirements", []),
        ("reviewed_future_diagnostic_capture_plan", []), ("reviewed_planned_outputs", []),
        ("next_chain", []), ("risk_controls", []), ("operator_review_digest", "0" * 64),
    ],
)
def test_validator_rejects_contract_mutation(path: str, replacement: object) -> None:
    review = deepcopy(_build())
    _set_path(review, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(review)


def test_builder_accepts_exact_source_candidate() -> None:
    review = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(source_candidate=service._expected_source_candidate())
    assert review["source_targeted_diagnostic_output_capture_candidate_digest"] == service.SOURCE_CANDIDATE_DIGEST


def test_builder_rejects_changed_source_candidate() -> None:
    candidate = service._expected_source_candidate()
    candidate[service.source.DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(source_candidate=candidate)


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1.json"
    review = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["operator_review_digest"] == review[service.DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(review)["failed_checks"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_v1(tmp_path / protected)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Targeted Diagnostic Output Capture Candidate", "Source Remediation or Method Results Review",
        "Source Planning Reentry with Complete Detail", "Source Detail Binding Results Review",
        "Source Materialization Results Review", "Retry Failure Context", "Review Scope",
        "Reviewed Priority Planning Facts", "Priority 1 Top Module Groups", "Planning Buckets",
        "Reviewed Candidate Philosophy", "Reviewed Diagnostic Capture Packages",
        "Reviewed Future Diagnostic Capture Requirements", "Reviewed Future Diagnostic Capture Plan",
        "Reviewed Future Diagnostic Command Template", "Reviewed Planned Outputs", "Reviewed Non-Goals",
        "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_candidate_operator_review_markdown_v1(_build())
    assert f"## {heading}" in markdown
