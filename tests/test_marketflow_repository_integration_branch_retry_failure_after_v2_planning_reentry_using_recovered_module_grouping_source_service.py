from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_service
    as service,
)


@pytest.fixture(scope="module")
def reentry() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1()


def test_reentry_builds_offline_without_cache_or_source_builder(monkeypatch):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("reentry crossed its committed-source planning boundary")

    monkeypatch.setattr(service.Path, "read_bytes", forbidden)
    monkeypatch.setattr(service.Path, "read_text", forbidden)
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1",
        forbidden,
    )
    first = service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1()
    second = service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1()
    assert first == second
    assert first["cache_read_in_reentry"] is False
    assert first["after_v2_planning_execution_performed"] is False


@pytest.mark.parametrize(
    "field,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("reentry_status", service.REENTRY_STATUS),
        ("reentry_scope", service.REENTRY_SCOPE),
        ("source_module_grouping_source_recovery_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", service.source.SOURCE_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.source.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_approval_digest", service.source.source.SOURCE_APPROVAL_DIGEST),
        ("source_module_grouping_source_recovery_operator_review_digest", service.source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_candidate_digest", service.source.source.approval_source.source.SOURCE_CANDIDATE_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason_before_recovery", service.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_after_v2_approval_digest", service.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_after_v2_operator_review_digest", service.SOURCE_AFTER_V2_OPERATOR_REVIEW_DIGEST),
        ("source_after_v2_candidate_digest", service.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
        ("source_results_review_v2_digest", service.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("retry_pytest_first_result_authoritative", True),
        ("root_full_regression_is_retry_evidence", False),
        ("cache_hash_and_count_verification_reviewed", True),
        ("module_grouping_detail_reviewed", True),
        ("module_paths_reviewed", True),
        ("per_module_counts_reviewed", True),
        ("bounded_nodeid_samples_reviewed", True),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("top_five_module_paths", service.source.TOP_FIVE),
        ("top_5_count_sum", 612),
        ("top_10_count_sum", 1069),
        ("previous_after_v2_planning_execution_blocker_resolved_for_reentry", True),
        ("after_v2_planning_reentry_using_recovered_module_grouping_source_created", True),
        ("after_v2_planning_reentry_using_recovered_module_grouping_source_ready", True),
        ("recovered_module_grouping_source_accepted_for_planning_reentry", True),
        ("ready_for_remediation_or_method_execution_after_classification_v2_review_reentry", True),
        ("reentry_decision", service.REENTRY_DECISION),
        ("reentry_decision_status", service.REENTRY_DECISION_STATUS),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_reentry_binds_required_facts(reentry, field, expected):
    assert reentry[field] == expected


def test_cache_recovered_detail_and_top_concentration_are_bound(reentry):
    assert all(reentry["cache_verification_review"].values())
    assert reentry["lastfailed_cache_sha256_actual"] == service.source.source.EXPECTED_LASTFAILED_SHA256
    assert reentry["nodeids_cache_sha256_actual"] == service.source.source.EXPECTED_NODEIDS_SHA256
    assert reentry["lastfailed_cache_entry_count_actual"] == 1404
    assert reentry["nodeids_cache_entry_count_actual"] == 26288
    assert reentry["lastfailed_nodeids_subset_of_nodeids"] is True
    assert reentry["top_5_percentage_of_failed_or_errored_nodeids"] == "43.58974359"
    assert reentry["top_10_percentage_of_failed_or_errored_nodeids"] == "76.13960114"


def test_decision_acceptance_packages_plan_and_outputs(reentry):
    assert reentry["reason"] == service.REENTRY_REASON
    assert reentry["accepted_for"] == service.ACCEPTED_FOR
    assert reentry["not_accepted_for"] == service.NOT_ACCEPTED_FOR
    assert reentry["recommended_reentry_package"] == {
        "package_id": service.SELECTED_PACKAGE,
        "status": "RECOMMENDED_FOR_NEXT_TASK_NOT_EXECUTED",
        "purpose": "Use the reviewed recovered module-grouping source to rerun the previously blocked after-v2 planning execution as a separately invoked reentry execution.",
        "selected_for_next_task": True,
        "executed": False,
    }
    assert [item["status"] for item in reentry["alternative_reentry_packages"]] == [
        "AVAILABLE_NOT_SELECTED", "BLOCKED_NOT_ALLOWED", "BLOCKED_NOT_ALLOWED"
    ]
    assert reentry["future_reentry_execution_requirements"] == service.FUTURE_REENTRY_EXECUTION_REQUIREMENTS
    assert reentry["future_reentry_execution_plan"] == {
        "status": "PLANNED_NOT_EXECUTED",
        "steps": service.FUTURE_REENTRY_EXECUTION_PLAN,
    }
    assert len(reentry["planned_outputs"]) == 12
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in reentry["planned_outputs"])
    assert reentry["non_goals"] == service.NON_GOALS


@pytest.mark.parametrize(
    "field",
    [
        "failure_modules_classified",
        "error_modules_classified",
        "failure_error_separation_claimed",
        "first_failure_identified",
        "first_error_identified",
        "first_order_claim_made",
        "traceback_root_cause_claimed",
        "direct_code_remediation_recommended",
        "retry_success_claimed",
        "main_merge_readiness_claimed",
        "after_v2_planning_execution_reentered",
        "after_v2_planning_execution_performed",
        "remediation_or_method_after_v2_reentry_execution_created",
        "remediation_or_method_after_v2_reentry_execution_performed",
        "remediation_or_method_results_review_after_v2_created",
        "diagnostic_method_executed",
        "code_remediation_executed",
        "evidence_remediation_executed",
        "classification_execution_performed_in_reentry",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "cache_read_in_reentry",
        "module_grouping_recovered_in_reentry",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_reentry",
        "market_data_acquisition_performed_in_reentry",
        "dataset_generation_performed_in_reentry",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_reentry_preserves_false_claim_and_authority_boundaries(reentry, field):
    assert reentry[field] is False


def test_next_paths_risk_controls_checklist_and_summary(reentry):
    assert reentry["next_chain"] == service.NEXT_CHAIN
    assert reentry["next_gates"] == service.NEXT_GATES
    assert reentry["risk_controls"] == service.RISK_CONTROLS
    assert len(reentry["risk_controls"]) == 59
    assert all(item["status"] == service.PASS for item in reentry["checklist"])
    assert reentry["summary"]["total_checks"] == reentry["summary"]["passed_checks"] == 80
    assert reentry["summary"]["failed_checks"] == reentry["summary"]["blocker_count"] == 0
    assert reentry["summary"]["recommended_next_task"] == service.SUCCESS_NEXT_TASK


def test_digest_is_deterministic_and_validator_accepts(reentry):
    repeated = service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1()
    digest_field = "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest"
    assert repeated[digest_field] == reentry[digest_field]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(reentry)["failed_checks"] == 0


def test_builder_rejects_inconsistent_source_review():
    source_review = service._committed_source_results_review()
    source_review["module_paths_reviewed"] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError):
        service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(
            source_results_review=source_review
        )


DELETE = object()


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("reentry_status", "WRONG"),
        ("reentry_scope", "WRONG"),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", "0" * 64),
        ("source_module_grouping_source_recovery_execution_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_source_recovery_digest_manifest_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_blocked_after_v2_manifest_digest", "0" * 64),
        ("blocked_reason_before_recovery", DELETE),
        ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_pytest_failed_count", DELETE),
        ("cache_verification_review", DELETE),
        ("cache_hash_and_count_verification_reviewed", False),
        ("recovered_module_grouping_detail_review", DELETE),
        ("module_grouping_detail_reviewed", False),
        ("module_paths_reviewed", False),
        ("per_module_counts_reviewed", False),
        ("bounded_nodeid_samples_reviewed", False),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136]),
        ("top_five_module_paths", []),
        ("top_5_count_sum", 611),
        ("top_10_count_sum", 1068),
        ("unsupported_claims_boundary_reviewed", False),
        ("failure_error_separation_claimed", True),
        ("previous_after_v2_planning_execution_blocker_resolved_for_reentry", False),
        ("after_v2_planning_reentry_using_recovered_module_grouping_source_created", False),
        ("after_v2_planning_reentry_using_recovered_module_grouping_source_ready", False),
        ("recovered_module_grouping_source_accepted_for_planning_reentry", False),
        ("ready_for_remediation_or_method_execution_after_classification_v2_review_reentry", False),
        ("after_v2_planning_execution_reentered", True),
        ("after_v2_planning_execution_performed", True),
        ("remediation_or_method_after_v2_reentry_execution_created", True),
        ("remediation_or_method_after_v2_reentry_execution_performed", True),
        ("remediation_or_method_results_review_after_v2_created", True),
        ("diagnostic_method_executed", True),
        ("code_remediation_executed", True),
        ("evidence_remediation_executed", True),
        ("classification_execution_performed_in_reentry", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True),
        ("cache_read_in_reentry", True),
        ("module_grouping_recovered_in_reentry", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True),
        ("evidence_regenerated", True),
        ("provider_requests_made_in_reentry", True),
        ("market_data_acquisition_performed_in_reentry", True),
        ("dataset_generation_performed_in_reentry", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("future_reentry_execution_requirements", {}),
        ("future_reentry_execution_plan", {}),
        ("planned_outputs", []),
        ("non_goals", []),
        ("risk_controls", []),
        ("marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest", DELETE),
    ],
)
def test_validator_rejects_mutated_reentry(reentry, field, value):
    mutated = deepcopy(reentry)
    if value is DELETE:
        mutated.pop(field)
    else:
        mutated[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError):
        service.validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(mutated)


def test_writer_round_trip_and_refuses_overwrite(tmp_path, reentry):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == reentry
    assert receipt["reentry_digest"] == reentry["marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureAfterV2PlanningReentryUsingRecoveredModuleGroupingSourceError):
        service.write_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1(tmp_path)


def test_markdown_contains_required_sections(reentry):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_markdown_v1(reentry)
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure After-v2 Planning Reentry Using Recovered Module Grouping Source v1",
        "Source Module Grouping Source Recovery Results Review",
        "Source Recovery Execution",
        "Previous Blocked After-v2 Planning Execution",
        "Retry Failure Context",
        "Recovered Module Grouping Source",
        "Top Module Concentration",
        "Reentry Decision",
        "Accepted and Unsupported Uses",
        "Future Reentry Execution Requirements",
        "Future Reentry Execution Plan",
        "Planned Outputs",
        "Non-Goals",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert heading in markdown


def test_package_exports_are_available():
    assert services.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1 == service.ARTIFACT_KIND
    assert services.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_READY == service.REENTRY_STATUS
    assert services.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_ONLY_NOT_PLANNING_EXECUTION_NOT_RETRY_NOT_MAIN == service.REENTRY_SCOPE
    assert services.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1 is service.build_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1
    assert services.validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1 is service.validate_marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_v1
