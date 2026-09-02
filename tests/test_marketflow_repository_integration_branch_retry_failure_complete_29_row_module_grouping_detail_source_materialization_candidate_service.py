from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_service
    as svc,
)


@pytest.fixture
def candidate() -> dict:
    return svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1()


def test_candidate_builds_offline(candidate: dict) -> None:
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


def test_candidate_digest_is_deterministic() -> None:
    first = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1()
    second = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1()
    assert first == second


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", svc.ARTIFACT_KIND), ("candidate_status", svc.CANDIDATE_STATUS),
        ("candidate_scope", svc.CANDIDATE_SCOPE),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", svc.SOURCE_DIAGNOSIS_DIGEST),
        ("primary_failure_class", svc.PRIMARY_FAILURE_CLASS),
        ("source_detail_exposure_or_binding_execution_blocked_digest", svc.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", svc.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", svc.source.SOURCE_BLOCKED_REASON),
        ("source_detail_exposure_or_binding_approval_digest", svc.source.SOURCE_APPROVAL_DIGEST),
        ("source_detail_exposure_or_binding_operator_review_digest", svc.source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_detail_exposure_or_binding_candidate_digest", svc.source.SOURCE_CANDIDATE_DIGEST),
        ("source_reentry_failure_diagnosis_digest", svc.source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_reentry_execution_blocked_digest", svc.source.SOURCE_REENTRY_BLOCKED_DIGEST),
        ("source_after_v2_planning_reentry_digest", svc.source.SOURCE_PLANNING_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", svc.source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", svc.source.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", svc.source.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", svc.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", svc.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", svc.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_after_v2_approval_digest", svc.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", svc.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", svc.source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", svc.source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", svc.source.RETRY_EXECUTION_COMMIT),
        ("top_5_count_sum", 612), ("top_10_count_sum", 1069),
        ("actual_live_detail_binding_source_lacks_complete_29_rows", True),
        ("detail_binding_success_path_tested_with_complete_29_row_snapshot", True),
        ("complete_29_row_module_grouping_detail_source_materialization_candidate_created", True),
        ("complete_29_row_module_grouping_detail_source_materialization_candidate_ready_for_operator_review", True),
        ("ready_for_complete_29_row_materialization_operator_review", True),
        ("recommended_complete_29_row_materialization_package", svc.RECOMMENDED_PACKAGE),
        ("recommendation_status", "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"),
        ("predictive_usefulness", svc.NOT_ACCEPTED), ("profitability", svc.NOT_ACCEPTED),
        ("runtime_use", svc.NOT_AUTHORIZED), ("broker_execution", svc.NOT_AUTHORIZED),
    ],
)
def test_required_fields_are_bound(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


def test_retry_counts_summary_and_top_five_are_bound(candidate: dict) -> None:
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert candidate["recovered_module_grouping_source_summary"]["module_summary_module_count"] == 29
    assert candidate["recovered_module_grouping_source_summary"]["failed_or_errored_nodeids_count"] == 1404
    assert candidate["top_module_summary"] == svc.TOP_FIVE
    assert sum(row["failed_or_errored_nodeid_count"] for row in candidate["top_module_summary"]) == 612


def test_available_and_missing_data_are_recorded(candidate: dict) -> None:
    assert candidate["source_execution_available_data"] == svc.AVAILABLE_DATA
    assert candidate["source_execution_missing_data"] == svc.MISSING_DATA


def test_twelve_packages_include_six_blocked(candidate: dict) -> None:
    assert len(candidate["proposed_packages"]) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in candidate["proposed_packages"]) == 6
    assert candidate["recommended_package"]["package"] == svc.RECOMMENDED_PACKAGE
    assert candidate["recommended_package"]["selected"] is False


@pytest.mark.parametrize("requirement", svc.FUTURE_REQUIREMENTS)
def test_future_materialization_requirements_are_defined(candidate: dict, requirement: str) -> None:
    assert candidate["future_materialization_or_binding_requirements"][requirement] is True


def test_future_plan_is_planned_not_executed(candidate: dict) -> None:
    assert candidate["future_materialization_or_binding_plan"] == {"status": svc.PLANNED_NOT_EXECUTED, "steps": svc.FUTURE_PLAN}


@pytest.mark.parametrize("output_id", svc.PLANNED_OUTPUTS)
def test_future_outputs_are_not_generated(candidate: dict, output_id: str) -> None:
    assert candidate["planned_outputs"][output_id] == svc.PLANNED_NOT_GENERATED


@pytest.mark.parametrize("non_goal", svc.NON_GOALS)
def test_non_goals_are_explicit(candidate: dict, non_goal: str) -> None:
    assert non_goal in candidate["non_goals"]


@pytest.mark.parametrize("field", svc.FALSE_BOUNDARIES)
def test_candidate_execution_boundaries_remain_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_next_chain_gates_and_risk_controls_are_complete(candidate: dict) -> None:
    assert candidate["next_chain"] == svc.NEXT_CHAIN
    assert candidate["next_gates"] == svc.NEXT_GATES
    assert candidate["risk_controls"] == svc.RISK_CONTROLS


def test_checklist_passes(candidate: dict) -> None:
    assert candidate["summary"]["passed_checks"] == candidate["summary"]["total_checks"]
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert all(item["status"] == svc.PASS for item in candidate["checklist"])


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(candidate)
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("artifact_kind",), "WRONG"), (("candidate_status",), "WRONG"), (("candidate_scope",), "WRONG"),
        (("source_detail_exposure_or_binding_execution_failure_diagnosis_digest",), "0" * 64),
        (("primary_failure_class",), "WRONG"), (("source_detail_exposure_or_binding_execution_blocked_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_execution_blocked_manifest_digest",), "0" * 64), (("blocked_reason",), None),
        (("source_detail_exposure_or_binding_approval_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_operator_review_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_candidate_digest",), "0" * 64),
        (("source_reentry_failure_diagnosis_digest",), "0" * 64), (("source_reentry_execution_blocked_digest",), "0" * 64),
        (("source_after_v2_planning_reentry_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_results_review_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_detail_digest",), "0" * 64),
        (("source_blocked_after_v2_execution_digest",), "0" * 64), (("source_after_v2_approval_digest",), "0" * 64),
        (("source_results_review_v2_digest",), "0" * 64), (("source_execution_v2_digest",), "0" * 64),
        (("source_module_grouping_digest",), "0" * 64), (("retry_failure_context", "counts"), {}),
        (("recovered_module_grouping_source_summary",), {}), (("top_module_summary",), []),
        (("top_5_count_sum",), 611), (("top_10_count_sum",), 1068),
        (("source_execution_available_data",), []), (("source_execution_missing_data",), []),
        (("actual_live_detail_binding_source_lacks_complete_29_rows",), False),
        (("recommended_complete_29_row_materialization_package",), None), (("proposed_packages",), []),
        (("recommended_package", "selected"), True), (("materialization_package_selected",), True),
        (("materialization_package_approved",), True), (("materialization_package_executed",), True),
        (("complete_29_row_detail_materialized",), True), (("complete_29_row_detail_exposed",), True),
        (("complete_29_row_detail_bound",), True), (("complete_29_row_detail_committed_source_created",), True),
        (("module_paths_recovered_by_candidate",), True), (("per_module_counts_recovered_by_candidate",), True),
        (("bounded_nodeid_samples_recovered_by_candidate",), True), (("detail_exposure_or_binding_reattempt_created",), True),
        (("after_v2_planning_execution_reentry_created",), True), (("after_v2_planning_execution_reentry_performed",), True),
        (("targeted_diagnostic_output_capture_candidate_created",), True), (("new_retry_candidate_created",), True),
        (("new_retry_executed",), True), (("new_retry_results_review_created",), True),
        (("main_merge_approval_created",), True), (("source_recovery_rerun_performed",), True),
        (("cache_read_in_candidate",), True), (("module_grouping_recovered_in_candidate",), True),
        (("retry_rerun_performed",), True), (("full_pytest_performed",), True),
        (("diagnostic_command_executed",), True), (("diagnostic_output_captured",), True),
        (("integration_execution_successful",), True), (("successful_integration_execution_digest_generated",), True),
        (("integration_branch_pushed",), True), (("main_push_performed",), True),
        (("origin_main_modified_by_this_task",), True), (("marketflow_outputs_committed",), True),
        (("pytest_cache_committed",), True), (("evidence_regenerated",), True),
        (("provider_requests_made_in_candidate",), True), (("market_data_acquisition_performed_in_candidate",), True),
        (("dataset_generation_performed_in_candidate",), True), (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True), (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"), (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("future_materialization_or_binding_requirements",), {}), (("future_materialization_or_binding_plan",), {}),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_contract_mutations(candidate: dict, path: tuple[str, ...], replacement: object) -> None:
    changed = deepcopy(candidate)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(changed)


def test_validator_rejects_missing_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed.pop("marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_digest")
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(changed)


def test_injected_source_is_accepted() -> None:
    candidate = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(source_diagnosis=svc._committed_source_diagnosis())
    assert candidate["candidate_status"] == svc.CANDIDATE_STATUS


def test_injected_source_mutation_is_rejected() -> None:
    diagnosis = svc._committed_source_diagnosis()
    diagnosis["top_5_count_sum"] = 611
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError):
        svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(source_diagnosis=diagnosis)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Execution Failure Diagnosis", "Source Blocked Detail Exposure or Binding Execution",
        "Source Approval and Operator Review", "Source Reentry Failure Diagnosis", "Source Recovery Results Review",
        "Retry Failure Context", "Recovered Module Grouping Source Summary", "Available and Missing Detail Source",
        "Candidate Scope", "Candidate Philosophy", "Proposed Materialization or Binding Packages",
        "Recommended Package", "Future Materialization or Binding Requirements",
        "Future Materialization or Binding Plan", "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(candidate: dict, heading: str) -> None:
    markdown = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_markdown_v1(candidate)
    assert f"## {heading}" in markdown


def test_writer_round_trips_in_isolated_directory(tmp_path) -> None:
    result = svc.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_v1(tmp_path)
    with open(result["json_path"], encoding="utf-8") as handle:
        stored = json.load(handle)
    assert stored == result["artifact"]
    assert "# MarketFlow Repository" in (tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_V1.md").read_text(encoding="utf-8")
