from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_service
    as service,
)


RUN_TIMESTAMP = "2026-08-23T00:00:00Z"
_DELETE = object()


def _snapshot() -> dict:
    counts = [136, 131, 122, 112, 111] + [33] * 24
    return {
        "module_grouping": [
            {
                "module_path": f"tests/test_module_{index:02d}.py",
                "failed_or_errored_nodeid_count": count,
                "sample_nodeids": [
                    f"tests/test_module_{index:02d}.py::test_bounded_sample"
                ],
            }
            for index, count in enumerate(counts)
        ]
    }


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        module_grouping_snapshot=_snapshot(), run_timestamp_utc=RUN_TIMESTAMP
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        run_timestamp_utc=RUN_TIMESTAMP
    )


def test_success_execution_builds_from_deterministic_snapshot(success):
    assert success["module_prioritization_generated"] is True
    assert len(success["module_prioritization_report"]) == 29


def test_blocked_execution_builds_without_module_detail(blocked):
    assert blocked["module_prioritization_generated"] is False
    assert blocked["blocked_reason"] == service.BLOCKED_REASON_MODULE_DETAIL


@pytest.mark.parametrize(
    "field,success_expected,blocked_expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND_EXECUTED, service.ARTIFACT_KIND_BLOCKED),
        ("execution_status", service.EXECUTION_STATUS_READY, service.EXECUTION_STATUS_BLOCKED_MODULE_DETAIL),
        ("execution_scope", service.EXECUTION_SCOPE, service.EXECUTION_SCOPE),
        ("selected_remediation_or_method_after_v2_package", service.SELECTED_PACKAGE, service.SELECTED_PACKAGE),
        ("source_after_v2_approval_digest", service.SOURCE_AFTER_V2_APPROVAL_DIGEST, service.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_after_v2_operator_review_digest", service.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST, service.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_after_v2_candidate_digest", service.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST, service.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
        ("source_results_review_v2_digest", service.SOURCE_RESULTS_REVIEW_V2_DIGEST, service.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.results_source.SOURCE_EXECUTION_V2_DIGEST, service.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.results_source.SOURCE_MODULE_GROUPING_DIGEST, service.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("failed_or_errored_nodeids_count", 1404, 1404),
        ("module_summary_module_count", 29, 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111], [136, 131, 122, 112, 111]),
        ("planning_method_after_v2_executed", True, True),
        ("diagnostic_method_after_v2_executed", False, False),
        ("code_remediation_after_v2_executed", False, False),
        ("evidence_remediation_after_v2_executed", False, False),
        ("classification_again_executed", False, False),
        ("cache_read_performed", False, False),
        ("module_prioritization_generated", True, False),
        ("top_module_concentration_report_generated", True, False),
        ("recommended_next_package_report_generated", True, False),
        ("failure_modules_classified", False, False),
        ("error_modules_classified", False, False),
        ("failure_error_separation_claimed", False, False),
        ("first_failure_identified", False, False),
        ("first_error_identified", False, False),
        ("first_order_claim_made", False, False),
        ("traceback_root_cause_claimed", False, False),
        ("direct_code_remediation_recommended", False, False),
        ("retry_success_claimed", False, False),
        ("main_merge_readiness_claimed", False, False),
        ("new_retry_candidate_created", False, False),
        ("new_retry_executed", False, False),
        ("new_retry_results_review_created", False, False),
        ("main_merge_approval_created", False, False),
        ("retry_rerun_performed", False, False),
        ("full_pytest_performed", False, False),
        ("diagnostic_command_executed", False, False),
        ("diagnostic_output_captured", False, False),
        ("integration_execution_successful", False, False),
        ("successful_integration_execution_digest_generated", False, False),
        ("integration_branch_pushed", False, False),
        ("main_push_performed", False, False),
        ("origin_main_modified_by_this_task", False, False),
        ("marketflow_outputs_committed", False, False),
        ("pytest_cache_committed", False, False),
        ("evidence_regenerated", False, False),
        ("provider_requests_made_in_execution", False, False),
        ("market_data_acquisition_performed_in_execution", False, False),
        ("dataset_generation_performed_in_execution", False, False),
        ("metric_recomputation_from_raw_rows_performed", False, False),
        ("model_training_performed", False, False),
        ("strategy_scoring_performed", False, False),
        ("trade_recommendations_generated", False, False),
        ("predictive_usefulness", "not accepted", "not accepted"),
        ("profitability", "not accepted", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED", "NOT_AUTHORIZED"),
    ],
)
def test_required_fields(success, blocked, field, success_expected, blocked_expected):
    assert success[field] == success_expected
    assert blocked[field] == blocked_expected


def test_retry_counts_and_module_summary_are_bound(success, blocked):
    for artifact in (success, blocked):
        assert [
            artifact[f"retry_pytest_{name}_count"]
            for name in ("passed", "failed", "error", "skipped")
        ] == [24877, 1292, 112, 7]
        assert artifact["module_level_grouping_reviewed"] is True
        assert artifact["unsupported_claims_boundary"] == service._unsupported_claims_boundary()


def test_success_priorities_sort_by_count_then_path(success):
    rows = success["module_prioritization_report"]
    assert [(row["failed_or_errored_nodeid_count"], row["module_path"]) for row in rows] == sorted(
        [(row["failed_or_errored_nodeid_count"], row["module_path"]) for row in rows],
        key=lambda pair: (-pair[0], pair[1]),
    )
    assert [row["priority_tier"] for row in rows[:5]] == [service.PRIORITY_TIER_POLICY[0]] * 5
    assert [row["priority_tier"] for row in rows[5:10]] == [service.PRIORITY_TIER_POLICY[1]] * 5
    assert [row["priority_tier"] for row in rows[10:]] == [service.PRIORITY_TIER_POLICY[2]] * 19
    assert [row["priority_rank"] for row in rows] == list(range(1, 30))


def test_success_top_five_concentration_and_follow_on(success):
    report = success["top_module_concentration_report"]
    assert report["failed_or_errored_nodeid_count"] == 612
    assert report["percentage_of_failed_or_errored_nodeids"] == "43.589744"
    assert success["recommended_follow_on_package_after_results_review"] == service.FOLLOW_ON_PACKAGE
    assert success["recommended_follow_on_package_status"] == service.FOLLOW_ON_PACKAGE_STATUS


def test_success_rows_remain_planning_only(success):
    for row in success["module_prioritization_report"]:
        assert row["recommended_planning_bucket_candidates"] == service.PLANNING_BUCKET_CANDIDATES
        assert row["planning_confidence"] == "LOW_TO_MEDIUM"
        assert row["basis"] == "MODULE_LEVEL_GROUPING_ONLY_NOT_TRACEBACK_BASED"
        assert row["unsupported_claims"] == service.UNSUPPORTED_CLAIMS
        assert len(row["sample_nodeids_bounded_if_available"]) <= 5


def test_planned_outputs_match_disposition(success, blocked):
    assert len(success["planned_outputs"]) == len(blocked["planned_outputs"]) == 11
    assert all(row["status"] == "GENERATED_RESEARCH_ONLY" for row in success["planned_outputs"])
    assert all(row["status"] == "NOT_GENERATED_BLOCKED" for row in blocked["planned_outputs"])


def test_blocked_records_missing_detail_and_source_recovery(blocked):
    assert blocked["available_data"] == service.AVAILABLE_DATA
    assert blocked["missing_data"] == service.MISSING_DATA
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK
    assert blocked["blocked_manifest"]["blocked_reason"] == service.BLOCKED_REASON_MODULE_DETAIL


def test_next_chains_gates_and_risks(success, blocked):
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert success["risk_controls"] == blocked["risk_controls"] == service.RISK_CONTROLS


def test_prechecks_and_execution_steps_pass(success, blocked):
    for artifact in (success, blocked):
        assert len(artifact["precheck_results"]) == 17
        assert all(row["status"] == "PASS" for row in artifact["precheck_results"])
        assert len(artifact["execution_steps"]) == 16
        assert all(row["status"] == "PASS" for row in artifact["execution_steps"])


def test_checklists_pass(success, blocked):
    assert success["summary"]["passed_checks"] == success["summary"]["total_checks"] == 65
    assert blocked["summary"]["passed_checks"] == blocked["summary"]["total_checks"] == 69
    assert success["summary"]["failed_checks"] == blocked["summary"]["failed_checks"] == 0


def test_all_digests_are_deterministic(success, blocked):
    rebuilt_success = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        module_grouping_snapshot=_snapshot(), run_timestamp_utc=RUN_TIMESTAMP
    )
    rebuilt_blocked = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        run_timestamp_utc=RUN_TIMESTAMP
    )
    assert rebuilt_success == success
    assert rebuilt_blocked == blocked
    assert success["marketflow_repository_integration_branch_retry_failure_after_v2_prioritized_module_planning_digest"]
    assert success["marketflow_repository_integration_branch_retry_failure_after_v2_execution_digest_manifest_digest"]
    assert blocked["marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest"]


def test_validator_accepts_both_dispositions(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(success)["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(blocked)["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_remediation_or_method_after_v2_package", "WRONG"),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_after_v2_operator_review_digest", "0" * 64),
        ("source_after_v2_candidate_digest", "0" * 64),
        ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_pytest_failed_count", _DELETE),
        ("failed_or_errored_nodeids_count", _DELETE),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136, 131]),
        ("unsupported_claims_boundary", _DELETE),
        ("planning_method_after_v2_executed", False),
        ("diagnostic_method_after_v2_executed", True),
        ("code_remediation_after_v2_executed", True),
        ("evidence_remediation_after_v2_executed", True),
        ("classification_again_executed", True),
        ("cache_read_performed", True),
        ("module_prioritization_generated", False),
        ("top_module_concentration_report_generated", False),
        ("recommended_next_package_report_generated", False),
        ("failure_modules_classified", True),
        ("error_modules_classified", True),
        ("failure_error_separation_claimed", True),
        ("first_failure_identified", True),
        ("first_error_identified", True),
        ("first_order_claim_made", True),
        ("traceback_root_cause_claimed", True),
        ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True),
        ("main_merge_readiness_claimed", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True),
        ("evidence_regenerated", True),
        ("provider_requests_made_in_execution", True),
        ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", _DELETE),
        ("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest", _DELETE),
    ],
)
def test_validator_rejects_invalid_success(success, field, value):
    changed = deepcopy(success)
    if value is _DELETE:
        changed.pop(field, None)
    else:
        changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(changed)


def test_validator_rejects_success_without_module_prioritization(success):
    changed = deepcopy(success)
    changed.pop("module_prioritization_report")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(changed)


def test_validator_rejects_blocked_without_manifest_digest(blocked):
    changed = deepcopy(blocked)
    changed.pop("marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(changed)


@pytest.mark.parametrize(
    "snapshot",
    [
        {"module_grouping": [{"module_path": "tests/test_one.py", "failed_or_errored_nodeid_count": 1404}]},
        {"module_grouping": [{"module_path": "", "failed_or_errored_nodeid_count": 1}]},
        {"module_grouping": [{"module_path": "tests/test_one.py", "failed_or_errored_nodeid_count": 0}]},
    ],
)
def test_invalid_snapshots_fail_closed_without_invention(snapshot):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
            module_grouping_snapshot=snapshot, run_timestamp_utc=RUN_TIMESTAMP
        )


def test_markdown_includes_required_sections(success, blocked):
    headings = (
        "Source Approval",
        "Source Classification Results Review v2",
        "Retry Failure Context",
        "Classification Evidence Summary",
        "Execution Scope",
        "Prioritized Module Planning",
        "Top Module Concentration",
        "Diagnostic and Remediation Planning Buckets",
        "Unsupported Claims Boundary",
        "Success or Blocked Disposition",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    )
    for artifact in (success, blocked):
        markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_markdown_v1(artifact)
        assert all(heading in markdown for heading in headings)


def test_exports_are_available():
    assert services.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1 is service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1
    assert services.ARTIFACT_KIND_EXECUTED_AFTER_CLASSIFICATION_V2_REVIEW == service.ARTIFACT_KIND_EXECUTED
    assert services.ARTIFACT_KIND_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW == service.ARTIFACT_KIND_BLOCKED
