from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_service
    as service,
)


def _snapshot() -> dict:
    rows = [
        {
            "module_path": path,
            "failed_or_errored_nodeid_count": count,
            "sample_nodeids_bounded_if_available": [f"{path}::test_{index}" for index in range(6, 0, -1)],
        }
        for path, count in zip(service.TOP_FIVE_PATHS, [136, 131, 122, 112, 111])
    ]
    rows.extend(
        {
            "module_path": f"tests/reentry_next_{index:02d}.py",
            "failed_or_errored_nodeid_count": count,
            "sample_nodeids_bounded_if_available": [f"tests/reentry_next_{index:02d}.py::test_sample"],
        }
        for index, count in enumerate([100, 95, 92, 88, 82], 1)
    )
    rows.extend(
        {
            "module_path": f"tests/reentry_remaining_{index:02d}.py",
            "failed_or_errored_nodeid_count": count,
            "sample_nodeids_bounded_if_available": [],
        }
        for index, count in enumerate([18] * 18 + [11], 1)
    )
    return {"module_rows": rows}


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        recovered_module_grouping_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def test_success_and_default_blocked_execution_dispositions(success, blocked):
    assert success["artifact_kind"] == service.ARTIFACT_KIND_EXECUTED
    assert success["execution_status"] == service.EXECUTION_STATUS_READY
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert blocked["execution_status"] == service.EXECUTION_STATUS_BLOCKED_SOURCE
    assert blocked["blocked_reason"] == "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK


@pytest.mark.parametrize("mutation", ["missing_rows", "missing_path", "module_count", "top_count"])
def test_inconsistent_recovered_snapshots_block(mutation):
    snapshot = _snapshot()
    if mutation == "missing_rows":
        snapshot = {}
    elif mutation == "missing_path":
        snapshot["module_rows"][0].pop("module_path")
    elif mutation == "module_count":
        snapshot["module_rows"].pop()
    else:
        snapshot["module_rows"][0]["failed_or_errored_nodeid_count"] = 135
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        recovered_module_grouping_snapshot=snapshot
    )
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_BLOCKED
    assert artifact["module_prioritization_generated"] is False
    assert artifact["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"]


def test_source_precheck_failure_uses_specific_blocked_status():
    reentry = service._committed_source_reentry()
    reentry["marketflow_repository_integration_branch_retry_failure_after_v2_planning_reentry_using_recovered_module_grouping_source_digest"] = "0" * 64
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        source_reentry=reentry, recovered_module_grouping_snapshot=_snapshot()
    )
    assert artifact["execution_status"] == service.EXECUTION_STATUS_BLOCKED_PRECHECK
    assert "DIGEST_MISMATCH_OR_MISSING" in artifact["blocked_reason"]


@pytest.mark.parametrize(
    "field,expected",
    [
        ("execution_scope", service.EXECUTION_SCOPE),
        ("selected_remediation_or_method_after_v2_package", service.SELECTED_PACKAGE),
        ("source_after_v2_planning_reentry_digest", service.SOURCE_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", service.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", service.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", service.source.source.SOURCE_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.source.source.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.source.source.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.source.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.source.source.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason_before_recovery", service.source.source.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_after_v2_approval_digest", service.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", service.source.source.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.source.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877), ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112), ("retry_pytest_skipped_count", 7),
        ("recovered_module_grouping_source_accepted_for_planning_reentry", True),
        ("previous_after_v2_planning_execution_blocker_resolved_for_reentry", True),
        ("recovered_module_detail_available", True), ("module_paths_available", True),
        ("per_module_counts_available", True), ("bounded_samples_available", True),
        ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("top_five_module_paths", service.TOP_FIVE_PATHS),
        ("top_5_count_sum", 612), ("top_10_count_sum", 1069),
        ("priority_tier_policy", service.PRIORITY_TIER_POLICY),
        ("priority_tier_1_count_sum", 612), ("priority_tier_2_count_sum", 457),
        ("priority_tier_3_count_sum", 335),
        ("module_prioritization_generated", True),
        ("prioritized_module_group_summary_generated", True),
        ("priority_tier_report_generated", True),
        ("top_module_concentration_report_generated", True),
        ("recommended_follow_on_candidate_report_generated", True),
        ("recommended_follow_on_package_after_results_review", service.FOLLOW_ON_PACKAGE),
        ("after_v2_planning_execution_reentered", True),
        ("after_v2_planning_execution_performed", True),
        ("remediation_or_method_after_v2_reentry_execution_created", True),
        ("remediation_or_method_after_v2_reentry_execution_performed", True),
        ("planning_method_after_v2_reentry_executed", True),
        ("ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry", True),
        ("predictive_usefulness", service.NOT_ACCEPTED), ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED), ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_success_binds_required_execution_facts(success, field, expected):
    assert success[field] == expected


def test_prioritized_rows_are_deterministic_bounded_and_planning_only(success):
    rows = success["prioritized_module_group_summary"]
    assert len(rows) == 29
    assert rows == sorted(rows, key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"]))
    assert [row["priority_rank"] for row in rows] == list(range(1, 30))
    assert [row["priority_tier"] for row in rows[:5]] == [service.PRIORITY_TIER_POLICY[0]] * 5
    assert [row["priority_tier"] for row in rows[5:10]] == [service.PRIORITY_TIER_POLICY[1]] * 5
    assert [row["priority_tier"] for row in rows[10:]] == [service.PRIORITY_TIER_POLICY[2]] * 19
    assert all(len(row["sample_nodeids_bounded_if_available"]) <= 5 for row in rows)
    assert all(row["sample_nodeids_bounded_if_available"] == sorted(row["sample_nodeids_bounded_if_available"]) for row in rows)
    assert all(row["recommended_planning_bucket_candidates"] == service.PLANNING_BUCKETS for row in rows)
    assert all(row["planning_confidence"] == "LOW_TO_MEDIUM" for row in rows)
    assert all(row["basis"] == "MODULE_LEVEL_GROUPING_ONLY_NOT_TRACEBACK_BASED" for row in rows)
    assert all(row["unsupported_claims"] == service.ROW_UNSUPPORTED_CLAIMS for row in rows)


def test_reports_outputs_and_follow_on_are_research_only(success):
    assert [item["count_sum"] for item in success["priority_tier_report"]] == [612, 457, 335]
    assert success["top_module_concentration_report"] == {
        "top_5_count_sum": 612, "top_5_percentage": "43.58974359",
        "top_10_count_sum": 1069, "top_10_percentage": "76.13960114",
    }
    assert success["recommended_follow_on_candidate_report"]["status"] == "RECOMMENDED_FOR_FUTURE_CANDIDATE_AFTER_RESULTS_REVIEW_NOT_SELECTED"
    assert len(success["planned_outputs"]) == 12
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in success["planned_outputs"])


@pytest.mark.parametrize(
    "field",
    [
        "diagnostic_method_executed", "code_remediation_executed", "evidence_remediation_executed",
        "classification_execution_performed_in_reentry", "cache_read_in_reentry",
        "module_grouping_recovered_in_reentry", "failure_modules_classified", "error_modules_classified",
        "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
        "first_order_claim_made", "traceback_root_cause_claimed", "direct_code_remediation_recommended",
        "retry_success_claimed", "main_merge_readiness_claimed",
        "remediation_or_method_results_review_after_v2_created",
        "targeted_diagnostic_output_capture_candidate_created", "new_retry_candidate_created",
        "new_retry_executed", "new_retry_results_review_created", "main_merge_approval_created",
        "retry_rerun_performed", "full_pytest_performed", "diagnostic_command_executed",
        "diagnostic_output_captured", "integration_execution_successful",
        "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
        "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
        "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
        "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    ],
)
def test_success_preserves_false_claim_and_authority_boundaries(success, field):
    assert success[field] is False


def test_digests_paths_risk_controls_and_checklists(success, blocked):
    assert success["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest"]
    assert success["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest"]
    assert blocked["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"]
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert success["risk_controls"] == service.RISK_CONTROLS
    assert len(success["risk_controls"]) == 62
    assert all(item["status"] == service.PASS for item in success["checklist"])
    assert all(item["status"] == service.PASS for item in blocked["checklist"])
    assert success["summary"]["total_checks"] == success["summary"]["passed_checks"]
    assert blocked["summary"]["total_checks"] == blocked["summary"]["passed_checks"]


def test_digests_are_deterministic_and_validator_accepts(success, blocked):
    repeated_success = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        recovered_module_grouping_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    repeated_blocked = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    for field in (
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest",
        "marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest",
        "marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest",
    ):
        assert repeated_success[field] == success[field]
    assert repeated_blocked["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"] == blocked["marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest"]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(success)["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(blocked)["failed_checks"] == 0


DELETE = object()


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"), ("execution_scope", "WRONG"),
        ("selected_remediation_or_method_after_v2_package", "WRONG"),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", "0" * 64),
        ("source_module_grouping_source_recovery_execution_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_blocked_after_v2_manifest_digest", "0" * 64),
        ("blocked_reason_before_recovery", DELETE), ("source_after_v2_approval_digest", "0" * 64),
        ("source_results_review_v2_digest", "0" * 64), ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_pytest_failed_count", DELETE),
        ("recovered_module_grouping_source_accepted_for_planning_reentry", False),
        ("previous_after_v2_planning_execution_blocker_resolved_for_reentry", False),
        ("recovered_module_detail_available", False), ("module_paths_available", False),
        ("per_module_counts_available", False), ("bounded_samples_available", False),
        ("module_summary_module_count", 28), ("largest_module_nodeid_counts", [136]),
        ("top_five_module_paths", []), ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("priority_tier_policy", []), ("module_prioritization_generated", False),
        ("top_module_concentration_report_generated", False),
        ("recommended_follow_on_candidate_report_generated", False),
        ("after_v2_planning_execution_performed", False), ("diagnostic_method_executed", True),
        ("code_remediation_executed", True), ("evidence_remediation_executed", True),
        ("classification_execution_performed_in_reentry", True), ("cache_read_in_reentry", True),
        ("module_grouping_recovered_in_reentry", True), ("failure_error_separation_claimed", True),
        ("first_failure_identified", True), ("first_error_identified", True), ("first_order_claim_made", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("main_merge_readiness_claimed", True),
        ("remediation_or_method_results_review_after_v2_created", True),
        ("targeted_diagnostic_output_capture_candidate_created", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("retry_rerun_performed", True),
        ("full_pytest_performed", True), ("diagnostic_command_executed", True),
        ("integration_execution_successful", True), ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True), ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_execution", True), ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True), ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True), ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
        ("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_digest", DELETE),
        ("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_prioritized_module_planning_digest", DELETE),
        ("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_digest_manifest_digest", DELETE),
    ],
)
def test_validator_rejects_mutated_success(success, field, value):
    mutated = deepcopy(success)
    if value is DELETE:
        mutated.pop(field)
    else:
        mutated[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(mutated)


def test_validator_rejects_bad_blocked_manifest(blocked):
    mutated = deepcopy(blocked)
    mutated.pop("marketflow_repository_integration_branch_retry_failure_after_v2_reentry_execution_blocked_manifest_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewReentryError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1(mutated)


def test_markdown_contains_required_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_markdown_v1(success)
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry v1",
        "Source Planning Reentry", "Source Recovery Results Review", "Previous Blocked After-v2 Execution",
        "Retry Failure Context", "Recovered Module Grouping Source", "Execution Scope",
        "Prioritized Module Planning", "Priority Tier Report", "Top Module Concentration",
        "Diagnostic and Remediation Planning Buckets", "Recommended Follow-on Candidate",
        "Unsupported Claims Boundary", "Success or Blocked Disposition", "Authority Boundaries",
        "Next Chain", "Next Gates", "Risk Controls", "Checklist Summary", "Guardrails",
    ):
        assert heading in markdown


def test_package_exports_are_available():
    assert services.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1 is service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1
    assert services.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1 is service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_v1
