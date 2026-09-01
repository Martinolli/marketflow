from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_service
    as service,
)


def _snapshot() -> dict:
    counts = [136, 131, 122, 112, 111] + [33] * 24
    failed = [f"tests/mod{index:02d}.py::test_{item:04d}" for index, count in enumerate(counts) for item in range(count)]
    inventory = failed + [f"tests/inventory.py::test_{item:05d}" for item in range(service.EXPECTED_NODEIDS_COUNT - len(failed))]
    return {"lastfailed": failed, "nodeids": inventory}


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(
        cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    snapshot = _snapshot()
    snapshot["lastfailed_sha256"] = "0" * 64
    return service.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(cache_snapshot=snapshot)


def test_success_and_blocked_artifacts_build(success, blocked):
    assert success["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_V1
    assert success["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTED_DETAIL_RECOVERED_FROM_REVIEWED_DETACHED_PYTEST_CACHE
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1
    assert blocked["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_CACHE_SOURCE_MISMATCH_OR_DETAIL_UNAVAILABLE


@pytest.mark.parametrize("mutation", ["node_count", "subset", "module_count"])
def test_fail_closed_snapshot_variants(mutation):
    snapshot = _snapshot()
    if mutation == "node_count": snapshot["nodeids"].pop()
    elif mutation == "subset": snapshot["nodeids"].remove(snapshot["lastfailed"][0])
    else: snapshot["lastfailed"][0] = "tests/extra_module.py::test_extra"
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(cache_snapshot=snapshot)
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_BLOCKED_V1
    assert artifact["module_grouping_detail_recovered"] is False
    assert artifact["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_blocked_manifest_digest"]


@pytest.mark.parametrize(
    "field,expected",
    [
        ("execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_EXECUTION_ONLY_READ_ONLY_CACHE_NOT_RETRY_NOT_MAIN),
        ("selected_module_grouping_source_recovery_package", service.SELECTED_PACKAGE),
        ("source_module_grouping_source_recovery_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("source_module_grouping_source_recovery_operator_review_digest", service.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_candidate_digest", service.approval_source.source.SOURCE_CANDIDATE_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason_before_recovery", service.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_results_review_v2_digest", service.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("module_grouping_source_recovery_executed", True), ("module_grouping_detail_recovered", True),
        ("module_grouping_detail_exposed", True), ("module_paths_recovered", True),
        ("per_module_counts_recovered", True), ("bounded_nodeid_samples_recovered", True),
        ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("ready_for_module_grouping_source_recovery_results_review", True),
        ("ready_for_after_v2_planning_reentry", False),
    ],
)
def test_success_fields(success, field, expected):
    assert success[field] == expected


def test_cache_verification_and_recovered_reports(success):
    report = success["cache_hash_and_count_verification_report"]
    assert report["lastfailed_cache_sha256_actual"] == service.EXPECTED_LASTFAILED_SHA256
    assert report["nodeids_cache_sha256_actual"] == service.EXPECTED_NODEIDS_SHA256
    assert report["lastfailed_cache_entry_count_actual"] == 1404
    assert report["nodeids_cache_entry_count_actual"] == 26288
    assert report["lastfailed_nodeids_subset_of_nodeids"] is True
    rows = success["recovered_module_grouping_detail_report"]
    assert len(rows) == 29
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert all(len(row["sample_nodeids_bounded"]) <= 5 for row in rows)
    assert rows == sorted(rows, key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"]))


def test_outputs_digests_and_next_paths(success, blocked):
    assert len(success["planned_outputs"]) == 10
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in success["planned_outputs"])
    assert success["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_detail_digest"]
    assert success["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_digest_manifest_digest"]
    assert success["summary"]["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert blocked["summary"]["recommended_next_task"] == service.BLOCKED_NEXT_TASK
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN


def test_closed_boundaries_and_checklists(success, blocked):
    false_fields = [
        *service.UNSUPPORTED_CLAIMS, "diagnostic_method_executed", "code_remediation_executed",
        "evidence_remediation_executed", "classification_execution_performed",
        "remediation_or_method_after_v2_reentry_created", "new_retry_candidate_created", "new_retry_executed",
        "new_retry_results_review_created", "main_merge_approval_created", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
        "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
        "evidence_regenerated", "provider_requests_made_in_execution", "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    ]
    assert all(success[field] is False for field in false_fields)
    assert success["predictive_usefulness"] == success["profitability"] == "not accepted"
    assert success["runtime_use"] == success["broker_execution"] == "NOT_AUTHORIZED"
    for artifact in (success, blocked):
        assert artifact["summary"]["failed_checks"] == 0
        assert all(item["status"] == "PASS" for item in artifact["checklist"])
        assert artifact["risk_controls"] == service.RISK_CONTROLS


def test_digests_are_deterministic(success, blocked):
    assert service.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z") == success
    snapshot = _snapshot(); snapshot["lastfailed_sha256"] = "0" * 64
    assert service.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(cache_snapshot=snapshot) == blocked


def test_validator_accepts_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(success)["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(blocked)["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"),
        ("selected_module_grouping_source_recovery_package", "WRONG"),
        ("source_module_grouping_source_recovery_approval_digest", "0" * 64),
        ("source_module_grouping_source_recovery_operator_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_candidate_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_pytest_failed_count", None),
        ("module_summary_module_count", 28), ("recovered_module_grouping_detail_report", []),
        ("module_paths_recovered", False), ("bounded_nodeid_samples_recovered", False),
        ("failure_error_separation_claimed", True), ("first_failure_identified", True),
        ("traceback_root_cause_claimed", True), ("direct_code_remediation_recommended", True),
        ("retry_success_claimed", True), ("new_retry_candidate_created", True),
        ("retry_rerun_performed", True), ("full_pytest_performed", True),
        ("diagnostic_command_executed", True), ("integration_execution_successful", True),
        ("main_push_performed", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("provider_requests_made_in_execution", True),
        ("predictive_usefulness", "accepted"), ("runtime_use", "AUTHORIZED"), ("risk_controls", []),
    ],
)
def test_validator_rejects_mutations(success, field, value):
    changed = deepcopy(success); changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(changed)


def test_markdown_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_markdown_v1(success)
    for section in ["Source Approval", "Cache Verification", "Recovered Module Grouping Detail", "Top Module Source Detail", "Unsupported Claims Boundary", "Success or Blocked Disposition", "Authority Boundaries", "Next Chain", "Next Gates", "Risk Controls", "Checklist Summary", "Guardrails"]:
        assert f"## {section}" in markdown


def test_public_export(success):
    assert services.execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1(cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z") == success
