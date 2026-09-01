from __future__ import annotations

import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_service
    as service,
)


def build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1()


def validate(candidate: dict) -> dict:
    return service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(candidate)


def test_candidate_builds_offline_with_correct_identity() -> None:
    candidate = build()
    assert candidate["created_offline"] is True
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_reentry_failure_diagnosis_digest", service.SOURCE_DIAGNOSIS_DIGEST),
        ("primary_failure_class", service.PRIMARY_FAILURE_CLASS),
        ("source_reentry_execution_blocked_digest", service.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_reentry_execution_blocked_manifest_digest", service.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("source_reentry_execution_blocked_reason", service.source.SOURCE_BLOCKED_REASON),
        ("source_after_v2_planning_reentry_digest", service.source.SOURCE_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", service.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", service.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", service.source.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_after_v2_approval_digest", service.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", service.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", service.source.RETRY_EXECUTION_COMMIT),
    ],
)
def test_source_chain_is_bound(field: str, expected: str) -> None:
    assert build()[field] == expected


def test_retry_module_and_top_five_summaries_are_bound() -> None:
    candidate = build()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert candidate["recovered_module_grouping_source_summary"]["failed_or_errored_nodeids_count"] == 1404
    assert candidate["recovered_module_grouping_source_summary"]["module_summary_module_count"] == 29
    assert candidate["top_module_summary"] == service.source.TOP_FIVE
    assert candidate["top_5_count_sum"] == 612
    assert candidate["top_10_count_sum"] == 1069


def test_available_and_missing_details_preserve_the_live_gap() -> None:
    candidate = build()
    assert candidate["available_committed_reentry_detail"] == service.source.AVAILABLE_COMMITTED_DETAIL
    assert candidate["missing_committed_reentry_detail"] == service.source.MISSING_COMMITTED_DETAIL
    assert candidate["actual_live_reentry_source_lacks_complete_29_rows"] is True
    assert candidate["reentry_success_path_tested_with_complete_29_row_snapshot"] is True
    assert len(candidate["top_module_summary"]) == 5
    assert "module_rows" not in candidate


def test_candidate_and_recommendation_are_ready_but_not_selected() -> None:
    candidate = build()
    assert candidate["reentry_module_grouping_detail_exposure_or_binding_candidate_created"] is True
    assert candidate["reentry_module_grouping_detail_exposure_or_binding_candidate_ready_for_operator_review"] is True
    assert candidate["ready_for_reentry_module_grouping_detail_exposure_or_binding_operator_review"] is True
    assert candidate["recommended_detail_exposure_or_binding_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommended_package"]["selected"] is False


def test_eleven_packages_include_five_blocked_packages() -> None:
    packages = build()["proposed_packages"]
    assert packages == service.PROPOSED_PACKAGES
    assert len(packages) == 11
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 5
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES)
def test_all_candidate_execution_boundaries_remain_false(field: str) -> None:
    assert build()[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", service.NOT_ACCEPTED), ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED), ("strategy_use", service.NOT_AUTHORIZED),
        ("paper_trading", service.NOT_AUTHORIZED), ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_predictive_and_runtime_authority_remains_closed(field: str, expected: str) -> None:
    assert build()[field] == expected


def test_future_requirements_plan_outputs_non_goals_and_chain_are_defined() -> None:
    candidate = build()
    assert candidate["future_detail_exposure_or_binding_requirements"] == service.FUTURE_REQUIREMENTS
    assert candidate["future_detail_exposure_or_binding_plan"] == {"status": service.PLANNED_NOT_EXECUTED, "steps": service.FUTURE_PLAN}
    assert candidate["planned_outputs"] == [{"output_id": output_id, "status": service.PLANNED_NOT_GENERATED} for output_id in service.PLANNED_OUTPUT_IDS]
    assert candidate["non_goals"] == service.NON_GOALS
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


@pytest.mark.parametrize("output_id", service.PLANNED_OUTPUT_IDS)
def test_each_output_is_planned_not_generated(output_id: str) -> None:
    outputs = {item["output_id"]: item["status"] for item in build()["planned_outputs"]}
    assert outputs[output_id] == service.PLANNED_NOT_GENERATED


def test_checklist_and_candidate_digest_are_deterministic() -> None:
    first = build()
    second = build()
    assert first == second
    assert first["summary"]["total_checks"] == 92
    assert first["summary"]["passed_checks"] == 92
    assert first["summary"]["failed_checks"] == 0
    assert first["summary"]["blocker_count"] == 0
    assert first["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest"] == second["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_digest"]


def test_validator_accepts_valid_candidate() -> None:
    result = validate(build())
    assert result["candidate_status"] == service.CANDIDATE_STATUS
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"), ("candidate_scope", "WRONG"),
        ("source_reentry_failure_diagnosis_digest", "0" * 64), ("primary_failure_class", "WRONG"),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_reentry_execution_blocked_manifest_digest", "0" * 64),
        ("source_reentry_execution_blocked_reason", ""),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64), ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64), ("source_module_grouping_digest", "0" * 64),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("actual_live_reentry_source_lacks_complete_29_rows", False),
        ("recommended_detail_exposure_or_binding_package", ""),
        ("detail_exposure_or_binding_selected", True), ("detail_exposure_or_binding_approved", True),
        ("detail_exposure_or_binding_executed", True), ("complete_29_row_detail_exposed", True),
        ("complete_29_row_detail_bound", True), ("module_grouping_detail_exposed_by_candidate", True),
        ("module_paths_recovered_by_candidate", True), ("per_module_counts_recovered_by_candidate", True),
        ("bounded_nodeid_samples_recovered_by_candidate", True),
        ("after_v2_planning_execution_reentry_created", True), ("after_v2_planning_execution_reentry_performed", True),
        ("targeted_diagnostic_output_capture_candidate_created", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("source_recovery_rerun_performed", True),
        ("cache_read_in_candidate", True), ("module_grouping_recovered_in_candidate", True),
        ("retry_rerun_performed", True), ("full_pytest_performed", True),
        ("diagnostic_command_executed", True), ("diagnostic_output_captured", True),
        ("integration_execution_successful", True), ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True), ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_candidate", True), ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_tampered_scalar_fields(field: str, replacement: object) -> None:
    candidate = build()
    candidate[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError):
        validate(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "retry_failure_context", "recovered_module_grouping_source_summary", "top_module_summary",
        "available_committed_reentry_detail", "missing_committed_reentry_detail", "proposed_packages",
        "future_detail_exposure_or_binding_requirements", "future_detail_exposure_or_binding_plan",
        "planned_outputs", "non_goals", "next_chain", "risk_controls",
    ],
)
def test_validator_rejects_missing_structures(field: str) -> None:
    candidate = build()
    candidate.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError):
        validate(candidate)


def test_builder_accepts_exact_source_diagnosis_and_rejects_changed_source() -> None:
    diagnosis = service._committed_source_diagnosis()
    assert service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(source_diagnosis=diagnosis)["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    diagnosis["primary_failure_class"] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(source_diagnosis=diagnosis)


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1(tmp_path)
    json_path = tmp_path / "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_v1.json"
    markdown_path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1.md"
    assert json.loads(json_path.read_text(encoding="utf-8")) == result["artifact"]
    assert markdown_path.is_file()


@pytest.mark.parametrize(
    "heading",
    [
        "Source Reentry Failure Diagnosis", "Source Blocked Reentry Execution", "Source Recovery Results Review",
        "Retry Failure Context", "Recovered Module Grouping Source Summary", "Available and Missing Committed Detail",
        "Candidate Scope", "Candidate Philosophy", "Proposed Detail Exposure or Binding Packages",
        "Recommended Package", "Future Detail Exposure or Binding Requirements",
        "Future Detail Exposure or Binding Plan", "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_candidate_markdown_v1(build())
    assert f"## {heading}" in markdown
