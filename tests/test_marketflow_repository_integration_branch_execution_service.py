from copy import deepcopy

import pytest

from marketflow.services import marketflow_repository_integration_branch_execution_service as service


@pytest.fixture
def execution():
    return service.execute_marketflow_repository_integration_branch_v1(
        execute_git_operations=False,
        run_pytest=False,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )


def test_execution_builds_deterministic_artifact_in_fixture_mode(execution):
    assert service.execute_marketflow_repository_integration_branch_v1(
        execute_git_operations=False,
        run_pytest=False,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    ) == execution


def test_fixture_mode_does_not_call_real_git_mutation(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("real git execution must not run in fixture mode")

    monkeypatch.setattr(service, "_execute_real", fail)
    result = service.execute_marketflow_repository_integration_branch_v1(
        execute_git_operations=False, run_pytest=False,
    )
    assert result["integration_branch_created"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1),
        ("execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED),
        ("execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME),
        ("selected_merge_strategy_package", service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_merge_strategy_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_merge_strategy_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tag_push_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_remote_manifest_review_digest", service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST),
        ("source_tag_push_execution_digest", service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST),
        ("source_tag_push_approval_digest", service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit_before_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_base", "origin/main"),
        ("integration_base_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_source_branch", service.INTEGRATION_SOURCE_BRANCH),
        ("integration_source_commit", service.INTEGRATION_SOURCE_COMMIT),
        ("integration_merge_method", "NO_FF_MERGE_COMMIT"),
        ("integration_branch_created", True), ("integration_merge_performed", True),
        ("integration_branch_pushed", False), ("remote_integration_branch_created", False),
        ("integration_pytest_performed", True), ("integration_pytest_passed", True),
        ("integration_pytest_exit_code", 0), ("integration_validation_completed", True),
        ("repository_merge_strategy_selected", True),
        ("repository_merge_strategy_approved", True),
        ("repository_merge_strategy_authorized", True),
        ("repository_merge_strategy_executed", True),
        ("repository_integration_branch_created", True),
        ("ready_for_repository_integration_branch_results_review", True),
        ("main_merge_performed", False), ("main_push_performed", False),
        ("git_main_push_performed", False), ("origin_main_modified_by_this_task", False),
        ("repository_cleanup_candidate_created", False),
        ("repository_cleanup_executed", False), ("git_rebase_performed", False),
        ("git_squash_merge_performed", False), ("git_cherry_pick_performed", False),
        ("git_branch_delete_performed", False), ("git_remote_delete_performed", False),
        ("git_force_push_performed", False), ("git_remote_prune_performed", False),
        ("repository_tags_pushed_again", False), ("additional_tag_push_performed", False),
        ("additional_tags_created", False), ("tags_modified", False), ("tags_deleted", False),
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"), ("predictive_usefulness_accepted", False),
        ("profitability", "not accepted"), ("profitability_accepted", False),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
        ("tracked_marketflow_file_count", 0), ("no_tracked_marketflow_files", True),
    ],
)
def test_required_execution_fields(execution, field, expected):
    assert execution[field] == expected


def test_fixture_commit_and_merge_base_evidence(execution):
    assert len(execution["integration_branch_head_commit"]) == 40
    assert execution["integration_branch_head_commit"] == execution["integration_merge_commit"]
    assert execution["integration_merge_base_with_origin_main"] == service.EXPECTED_ORIGIN_MAIN_COMMIT
    assert execution["integration_merge_base_with_source_commit"] == service.INTEGRATION_SOURCE_COMMIT


def test_fixture_pytest_record(execution):
    assert execution["integration_pytest_command"] == "env\\Scripts\\python.exe -m pytest -q"
    assert execution["integration_pytest_passed_count"] == 26706
    assert execution["integration_pytest_skipped_count"] == 7
    assert execution["integration_pytest_duration_seconds"] is None


def test_prechecks_and_execution_steps_pass(execution):
    assert [row["precheck_id"] for row in execution["precheck_results"]] == service.PRECHECK_IDS
    assert [row["step_id"] for row in execution["execution_steps"]] == service.EXECUTION_STEP_IDS
    assert all(row["status"] == "PASS" for row in execution["precheck_results"])
    assert all(row["status"] == "PASS" for row in execution["execution_steps"])


def test_next_chain_gates_and_risk_controls(execution):
    assert execution["next_chain"] == service.NEXT_CHAIN
    assert execution["next_gates"] == service.NEXT_GATES
    assert execution["risk_controls"] == service.RISK_CONTROLS
    assert execution["recommended_next_task"] == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RESULTS_REVIEW_V1"


def test_checklist_and_summary_pass(execution):
    assert [row["check_id"] for row in execution["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in execution["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in execution["checklist"])
    assert execution["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["failed_checks"] == 0
    assert execution["summary"]["blocker_count"] == 0


def test_execution_digest_is_deterministic(execution):
    assert execution["marketflow_repository_integration_branch_execution_digest"] == service.marketflow_repository_integration_branch_execution_digest_v1(execution)


def test_validation_digest_is_deterministic(execution):
    assert execution["marketflow_repository_integration_branch_execution_validation_digest"] == service.marketflow_repository_integration_branch_execution_validation_digest_v1(execution)


def test_validator_accepts_valid_execution(execution):
    result = service.validate_marketflow_repository_integration_branch_execution_v1(execution)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"), (("execution_status",), "WRONG"),
        (("execution_scope",), "WRONG"), (("selected_merge_strategy_package",), "WRONG"),
        (("source_merge_strategy_approval_digest",), "0" * 64),
        (("source_merge_strategy_operator_review_digest",), "0" * 64),
        (("source_merge_strategy_candidate_digest",), "0" * 64),
        (("source_tag_push_results_review_digest",), "0" * 64),
        (("source_tag_push_execution_digest",), "0" * 64),
        (("source_tag_push_approval_digest",), "0" * 64),
        (("origin_main_commit_before_execution",), "0" * 40),
        (("origin_main_commit_after_execution",), "0" * 40),
        (("repository_merge_strategy_authorized",), False),
        (("repository_merge_strategy_executed",), False),
        (("repository_integration_branch_created",), False),
        (("integration_branch_created",), False), (("integration_branch_name",), "WRONG"),
        (("integration_base",), "WRONG"), (("integration_source_commit",), "0" * 40),
        (("integration_merge_performed",), False), (("integration_branch_pushed",), True),
        (("remote_integration_branch_created",), True),
        (("integration_pytest_performed",), False), (("integration_pytest_passed",), False),
        (("integration_validation_completed",), False), (("main_merge_performed",), True),
        (("main_push_performed",), True), (("git_main_push_performed",), True),
        (("git_rebase_performed",), True), (("git_squash_merge_performed",), True),
        (("git_cherry_pick_performed",), True), (("git_branch_delete_performed",), True),
        (("git_remote_delete_performed",), True), (("git_force_push_performed",), True),
        (("git_remote_prune_performed",), True), (("origin_main_modified_by_this_task",), True),
        (("repository_tags_pushed_again",), True), (("additional_tags_created",), True),
        (("tags_modified",), True), (("tags_deleted",), True),
        (("repository_cleanup_candidate_created",), True),
        (("provider_requests_made_in_execution",), True),
        (("market_data_acquisition_performed_in_execution",), True),
        (("dataset_generation_performed_in_execution",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness_accepted",), True), (("profitability_accepted",), True),
        (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutations(execution, path, bad_value):
    changed = deepcopy(execution)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionError):
        service.validate_marketflow_repository_integration_branch_execution_v1(changed)


def test_validator_rejects_missing_execution_digest(execution):
    changed = deepcopy(execution)
    changed.pop("marketflow_repository_integration_branch_execution_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionError):
        service.validate_marketflow_repository_integration_branch_execution_v1(changed)


def test_validator_rejects_missing_validation_digest(execution):
    changed = deepcopy(execution)
    changed.pop("marketflow_repository_integration_branch_execution_validation_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionError):
        service.validate_marketflow_repository_integration_branch_execution_v1(changed)


def test_validator_rejects_failed_precheck_record(execution):
    changed = deepcopy(execution)
    changed["precheck_results"][0]["status"] = "FAIL"
    changed["precheck_results"][0]["actual"] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionError):
        service.validate_marketflow_repository_integration_branch_execution_v1(changed)


def test_markdown_has_required_sections(execution):
    markdown = service.build_marketflow_repository_integration_branch_execution_markdown_v1(execution)
    for title in (
        "Title", "MarketFlow Repository Integration Branch Execution v1",
        "Source Merge Strategy Approval", "Bound Evidence", "Repository Context",
        "Execution Scope", "Integration Branch Creation", "Integration Merge",
        "Integration Pytest Validation", "Origin/Main Protection", "Next Chain",
        "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {title}" in markdown
