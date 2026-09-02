from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_service
    as svc,
)


@pytest.fixture
def review() -> dict:
    return svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1()


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_operator_review_digest_is_deterministic() -> None:
    first = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1()
    second = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1()
    assert first == second


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", svc.ARTIFACT_KIND), ("review_status", svc.REVIEW_STATUS), ("review_scope", svc.REVIEW_SCOPE),
        ("source_complete_29_row_materialization_candidate_digest", svc.SOURCE_CANDIDATE_DIGEST),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", svc.source.SOURCE_DIAGNOSIS_DIGEST),
        ("primary_failure_class", svc.source.PRIMARY_FAILURE_CLASS),
        ("source_detail_exposure_or_binding_execution_blocked_digest", svc.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", svc.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", svc.source.source.SOURCE_BLOCKED_REASON),
        ("source_detail_exposure_or_binding_approval_digest", svc.source.source.SOURCE_APPROVAL_DIGEST),
        ("source_detail_exposure_or_binding_operator_review_digest", svc.source.source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_detail_exposure_or_binding_candidate_digest", svc.source.source.SOURCE_CANDIDATE_DIGEST),
        ("source_reentry_failure_diagnosis_digest", svc.source.source.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_reentry_execution_blocked_digest", svc.source.source.SOURCE_REENTRY_BLOCKED_DIGEST),
        ("source_after_v2_planning_reentry_digest", svc.source.source.SOURCE_PLANNING_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", svc.source.source.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", svc.source.source.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", svc.source.source.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", svc.source.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", svc.source.source.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", svc.source.source.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_after_v2_approval_digest", svc.source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", svc.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", svc.source.source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", svc.source.source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", svc.source.source.RETRY_EXECUTION_COMMIT),
        ("top_5_count_sum", 612), ("top_10_count_sum", 1069),
        ("actual_live_detail_binding_source_lacks_complete_29_rows", True),
        ("detail_binding_success_path_tested_with_complete_29_row_snapshot", True),
        ("complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_created", True),
        ("complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_ready", True),
        ("materialization_packages_reviewed", True),
        ("future_materialization_or_binding_requirements_reviewed", True),
        ("future_materialization_or_binding_plan_reviewed", True),
        ("planned_outputs_reviewed", True), ("non_goals_reviewed", True),
        ("recommended_complete_29_row_materialization_package", svc.RECOMMENDED_PACKAGE),
        ("recommended_next_task", svc.RECOMMENDED_NEXT_TASK),
        ("predictive_usefulness", svc.NOT_ACCEPTED), ("profitability", svc.NOT_ACCEPTED),
        ("runtime_use", svc.NOT_AUTHORIZED), ("broker_execution", svc.NOT_AUTHORIZED),
    ],
)
def test_required_fields_are_bound(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_retry_counts_summary_and_top_five_are_bound(review: dict) -> None:
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["recovered_module_grouping_source_summary"]["module_summary_module_count"] == 29
    assert review["recovered_module_grouping_source_summary"]["failed_or_errored_nodeids_count"] == 1404
    assert review["top_module_summary"] == svc.source.TOP_FIVE


def test_available_and_missing_data_are_recorded(review: dict) -> None:
    assert review["source_execution_available_data"] == svc.source.AVAILABLE_DATA
    assert review["source_execution_missing_data"] == svc.source.MISSING_DATA


def test_all_packages_reviewed_without_selection(review: dict) -> None:
    packages = review["reviewed_materialization_or_binding_packages"]
    assert len(packages) == 12
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


@pytest.mark.parametrize("row", svc.REVIEWED_REQUIREMENTS)
def test_future_requirements_are_reviewed(review: dict, row: dict) -> None:
    assert row in review["reviewed_future_materialization_or_binding_requirements"]


@pytest.mark.parametrize("row", svc.REVIEWED_PLAN)
def test_future_plan_is_reviewed_not_executed(review: dict, row: dict) -> None:
    assert row in review["reviewed_future_materialization_or_binding_plan"]


@pytest.mark.parametrize("row", svc.REVIEWED_OUTPUTS)
def test_planned_outputs_are_reviewed_not_generated(review: dict, row: dict) -> None:
    assert row in review["reviewed_planned_outputs"]


@pytest.mark.parametrize("row", svc.REVIEWED_NON_GOALS)
def test_non_goals_remain_active(review: dict, row: dict) -> None:
    assert row in review["reviewed_non_goals"]


@pytest.mark.parametrize("field", svc.FALSE_BOUNDARIES)
def test_review_boundaries_remain_false(review: dict, field: str) -> None:
    assert review[field] is False


def test_recommendation_is_not_selection_or_approval(review: dict) -> None:
    assert review["recommendation"]["package"] == svc.RECOMMENDED_PACKAGE
    assert review["recommendation"]["selected"] is False
    assert review["ready_for_complete_29_row_materialization_approval"] is False


def test_next_chain_gates_and_risk_controls_are_complete(review: dict) -> None:
    assert review["next_chain"] == svc.NEXT_CHAIN
    assert review["next_gates"] == svc.NEXT_GATES
    assert review["risk_controls"] == svc.RISK_CONTROLS


def test_checklist_passes(review: dict) -> None:
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"]
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert all(item["status"] == svc.PASS for item in review["checklist"])


def test_validator_accepts_valid_review(review: dict) -> None:
    result = svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(review)
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("artifact_kind",), "WRONG"), (("review_status",), "WRONG"), (("review_scope",), "WRONG"),
        (("source_complete_29_row_materialization_candidate_digest",), "0" * 64),
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
        (("reviewed_materialization_or_binding_packages",), []),
        (("reviewed_future_materialization_or_binding_requirements",), []),
        (("ready_for_complete_29_row_materialization_approval",), True), (("recommendation", "selected"), True),
        (("materialization_package_selected",), True), (("materialization_package_approved",), True),
        (("materialization_package_authorized",), True), (("materialization_package_executed",), True),
        (("complete_29_row_detail_materialized",), True), (("complete_29_row_detail_exposed",), True),
        (("complete_29_row_detail_bound",), True), (("complete_29_row_detail_committed_source_created",), True),
        (("module_paths_recovered_by_review",), True), (("per_module_counts_recovered_by_review",), True),
        (("bounded_nodeid_samples_recovered_by_review",), True), (("detail_exposure_or_binding_reattempt_created",), True),
        (("after_v2_planning_execution_reentry_created",), True), (("after_v2_planning_execution_reentry_performed",), True),
        (("targeted_diagnostic_output_capture_candidate_created",), True), (("new_retry_candidate_created",), True),
        (("new_retry_executed",), True), (("new_retry_results_review_created",), True),
        (("main_merge_approval_created",), True), (("source_recovery_rerun_performed",), True),
        (("cache_read_in_review",), True), (("module_grouping_recovered_in_review",), True),
        (("retry_rerun_performed",), True), (("full_pytest_performed",), True),
        (("diagnostic_command_executed",), True), (("diagnostic_output_captured",), True),
        (("integration_execution_successful",), True), (("successful_integration_execution_digest_generated",), True),
        (("integration_branch_pushed",), True), (("main_push_performed",), True),
        (("origin_main_modified_by_this_task",), True), (("marketflow_outputs_committed",), True),
        (("pytest_cache_committed",), True), (("evidence_regenerated",), True),
        (("provider_requests_made_in_review",), True), (("market_data_acquisition_performed_in_review",), True),
        (("dataset_generation_performed_in_review",), True), (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True), (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"), (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_contract_mutations(review: dict, path: tuple[str, ...], replacement: object) -> None:
    changed = deepcopy(review)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(changed)


def test_validator_rejects_missing_digest(review: dict) -> None:
    changed = deepcopy(review)
    changed.pop("marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_digest")
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationOperatorReviewError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(changed)


def test_injected_source_is_accepted() -> None:
    review = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(source_candidate=svc._committed_source_candidate())
    assert review["review_status"] == svc.REVIEW_STATUS


def test_injected_source_mutation_is_rejected() -> None:
    candidate = svc._committed_source_candidate()
    candidate["top_5_count_sum"] = 611
    with pytest.raises(svc.source.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationCandidateError):
        svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(source_candidate=candidate)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Complete 29-row Materialization Candidate", "Source Execution Failure Diagnosis",
        "Source Blocked Detail Exposure or Binding Execution", "Source Approval and Operator Review",
        "Source Reentry Failure Diagnosis", "Source Recovery Results Review", "Retry Failure Context",
        "Recovered Module Grouping Source Summary", "Available and Missing Detail Source", "Review Scope",
        "Reviewed Candidate Philosophy", "Reviewed Materialization or Binding Packages",
        "Reviewed Future Materialization or Binding Requirements", "Reviewed Future Materialization or Binding Plan",
        "Reviewed Planned Outputs", "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(review: dict, heading: str) -> None:
    markdown = svc.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_markdown_v1(review)
    assert f"## {heading}" in markdown


def test_writer_round_trips_in_isolated_directory(tmp_path) -> None:
    result = svc.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_candidate_operator_review_v1(tmp_path)
    with open(result["json_path"], encoding="utf-8") as handle:
        stored = json.load(handle)
    assert stored == result["artifact"]
    assert "# MarketFlow Repository" in (tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_CANDIDATE_OPERATOR_REVIEW_V1.md").read_text(encoding="utf-8")
