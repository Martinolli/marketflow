from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_service as service,
)


def _snapshot(**overrides):
    values = {
        "origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head_commit": service.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": "fixture-worktree",
        "detached_integration_worktree_head_commit": service.INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean": True,
        "staged_evidence_manifest_digest": service.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "staged_evidence_file_count": 7,
        "repository_tracked_marketflow_count": 0,
        "worktree_tracked_marketflow_count": 0,
    }
    values.update(overrides)
    return values


def _patch_snapshot(monkeypatch, **overrides):
    monkeypatch.setattr(service, "_snapshot", lambda *_: deepcopy(_snapshot(**overrides)))


def _cache_dir(tmp_path):
    path = tmp_path / ".pytest_cache" / "v" / "cache"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _success(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch)
    worktree = tmp_path / "success"
    cache_dir = _cache_dir(worktree)
    lastfailed = {
        "tests/test_alpha.py::test_one": True,
        "tests/test_alpha.py::TestGroup::test_two": True,
        "tests/test_beta.py::test_three": True,
    }
    (cache_dir / "lastfailed").write_text(json.dumps(lastfailed), encoding="utf-8")
    (cache_dir / "nodeids").write_text(
        json.dumps([*lastfailed, "tests/test_gamma.py::test_four"]), encoding="utf-8"
    )
    return service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path,
        integration_worktree_path=worktree,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )


def _blocked_missing(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch)
    worktree = tmp_path / "blocked"
    worktree.mkdir(exist_ok=True)
    return service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path,
        integration_worktree_path=worktree,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )


@pytest.fixture
def success(monkeypatch, tmp_path):
    return _success(monkeypatch, tmp_path)


@pytest.fixture
def blocked(monkeypatch, tmp_path):
    return _blocked_missing(monkeypatch, tmp_path)


def test_success_execution_builds_from_fixture_lastfailed_cache(success):
    assert success["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED
    assert success["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTED_DETACHED_PYTEST_CACHE_CAPTURED
    assert success["execution_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert success["selected_output_capture_or_classification_source_package"] == service.SELECTED_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_PACKAGE
    assert success["lastfailed_cache_exists"] is True
    assert success["lastfailed_cache_read"] is True
    assert success["lastfailed_cache_parseable_json"] is True
    assert success["lastfailed_cache_entry_count"] == 3
    assert success["failed_or_errored_nodeids_count"] == 3
    assert success["classification_source_generated"] is True
    assert success["module_summary_generated"] is True


def test_blocked_execution_builds_when_lastfailed_missing(blocked):
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED
    assert blocked["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_DETACHED_PYTEST_CACHE_UNAVAILABLE_OR_INSUFFICIENT
    assert blocked["lastfailed_cache_exists"] is False
    assert blocked["lastfailed_cache_read"] is False
    assert blocked["lastfailed_cache_parseable_json"] is None
    assert blocked["classification_source_generated"] is False
    assert blocked["blocked_reason"] == service.BLOCKED_REASON


def test_blocked_execution_builds_when_lastfailed_empty(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch)
    (_cache_dir(tmp_path) / "lastfailed").write_text("{}", encoding="utf-8")
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path, integration_worktree_path=tmp_path
    )
    assert execution["lastfailed_cache_exists"] is True
    assert execution["lastfailed_cache_read"] is True
    assert execution["lastfailed_cache_parseable_json"] is True
    assert execution["lastfailed_cache_entry_count"] == 0
    assert execution["classification_source_generated"] is False


def test_blocked_execution_builds_when_lastfailed_corrupt(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch)
    (_cache_dir(tmp_path) / "lastfailed").write_text("not-json", encoding="utf-8")
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path, integration_worktree_path=tmp_path
    )
    assert execution["lastfailed_cache_exists"] is True
    assert execution["lastfailed_cache_read"] is True
    assert execution["lastfailed_cache_parseable_json"] is False
    assert execution["classification_source_generated"] is False


def test_precheck_failure_does_not_read_existing_cache(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch, origin_main_commit="0" * 40)
    cache_path = _cache_dir(tmp_path) / "lastfailed"
    cache_path.write_text('{"tests/test_alpha.py::test_one": true}', encoding="utf-8")
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path, integration_worktree_path=tmp_path
    )
    assert execution["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_BLOCKED_PRECHECK_FAILED
    assert execution["lastfailed_cache_read"] is False
    assert execution["pytest_cache_read"] is False
    assert execution["blocked_reason"] == service.PRECHECK_BLOCKED_REASON


def test_execution_does_not_modify_cache(monkeypatch, tmp_path):
    _patch_snapshot(monkeypatch)
    cache_path = _cache_dir(tmp_path) / "lastfailed"
    payload = b'{"tests/test_alpha.py::test_one": true}'
    cache_path.write_bytes(payload)
    service.execute_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_v1(
        repo_root=tmp_path, integration_worktree_path=tmp_path
    )
    assert cache_path.read_bytes() == payload


@pytest.mark.parametrize(
    "field,expected",
    [
        ("source_output_capture_approval_digest", service.SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST),
        ("source_output_capture_operator_review_digest", "f73a94b36e7884d778c980d4989c999c383a04310f45e58b6ffae9da6172aa8c"),
        ("source_output_capture_candidate_digest", "fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518"),
        ("source_method_execution_digest", "522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562"),
        ("source_method_blocked_manifest_digest", "3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f"),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("root_full_regression_is_retry_evidence", False),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit", service.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit", service.INTEGRATION_HEAD_COMMIT),
        ("staged_evidence_manifest_digest_before_cache_read", service.EXPECTED_STAGED_EVIDENCE_DIGEST),
        ("staged_evidence_manifest_digest_after_cache_read", service.EXPECTED_STAGED_EVIDENCE_DIGEST),
    ],
)
def test_execution_binds_source_and_protected_state(success, field, expected):
    assert success[field] == expected


@pytest.mark.parametrize(
    "field,expected",
    [
        ("output_capture_method_executed", True),
        ("classification_source_capture_executed", True),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("diagnostic_output_captured", False),
        ("operator_logs_parsed", False),
        ("new_retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("new_retry_candidate_created", False),
        ("main_merge_approval_created", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_execution_preserves_authority_boundaries(success, field, expected):
    assert success[field] == expected


def test_success_classification_source_records_limitations_and_summary(success):
    assert success["classification_source_type"] == "DETACHED_PYTEST_CACHE_LASTFAILED"
    assert success["classification_source_contains_nodeids"] is True
    assert success["classification_source_can_distinguish_failures_from_errors"] is False
    assert success["first_failure_identified"] is False
    assert success["first_error_identified"] is False
    assert success["ordering_limitation_recorded"] is True
    assert len(success["classification_source_limitations"]) == 3
    assert success["module_summary"] == [
        {"module_path": "tests/test_alpha.py", "nodeid_count": 2},
        {"module_path": "tests/test_beta.py", "nodeid_count": 1},
    ]
    assert success["nodeids_cache_exists"] is True
    assert success["nodeids_cache_parseable_json"] is True
    assert success["nodeids_cache_entry_count"] == 4


def test_success_manifest_and_execution_digest_are_deterministic(monkeypatch, tmp_path):
    first = _success(monkeypatch, tmp_path)
    second = _success(monkeypatch, tmp_path)
    assert first == second
    assert first["marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest"] == service.marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1(first)
    assert first["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest"] == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest_v1(first)


def test_blocked_manifest_and_execution_digest_are_deterministic(monkeypatch, tmp_path):
    first = _blocked_missing(monkeypatch, tmp_path)
    second = _blocked_missing(monkeypatch, tmp_path)
    assert first == second
    assert first["marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest"] == service.marketflow_repository_integration_branch_retry_failure_output_capture_blocked_manifest_digest_v1(first)
    assert first["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest"] == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest_v1(first)


def test_next_chain_and_gates_follow_disposition(success, blocked):
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert success["summary"]["recommended_next_task"].endswith("RESULTS_REVIEW_V1")
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert blocked["summary"]["recommended_next_task"].endswith("DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_V1")


def test_checklists_pass_for_success_and_blocked(success, blocked):
    assert len(success["checklist"]) == len(service.COMMON_CHECK_IDS) + len(service.SUCCESS_CHECK_IDS) == 53
    assert len(blocked["checklist"]) == len(service.COMMON_CHECK_IDS) + len(service.BLOCKED_CHECK_IDS) == 47
    assert all(row["status"] == service.PASS for row in success["checklist"])
    assert all(row["status"] == service.PASS for row in blocked["checklist"])
    assert success["summary"]["passed_checks"] == 53
    assert blocked["summary"]["passed_checks"] == 47


def test_validator_accepts_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(success)["passed_checks"] == 53
    assert service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(blocked)["passed_checks"] == 47


@pytest.mark.parametrize(
    "field,value",
    [
        ("selected_output_capture_or_classification_source_package", "wrong"),
        ("source_output_capture_approval_digest", "0" * 64),
        ("retry_pytest_failed_count", None),
        ("root_full_regression_is_retry_evidence", True),
        ("output_capture_method_executed", False),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True),
        ("operator_logs_parsed", True),
        ("new_retry_results_review_created", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("new_retry_candidate_created", True),
        ("main_merge_approval_created", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
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
        ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_common_contract(success, field, value):
    invalid = deepcopy(success)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(invalid)


@pytest.mark.parametrize(
    "field,value",
    [
        ("lastfailed_cache_parseable_json", False),
        ("classification_source_contains_nodeids", False),
        ("module_summary_generated", False),
        ("marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest", None),
    ],
)
def test_validator_rejects_invalid_success_state(success, field, value):
    invalid = deepcopy(success)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(invalid)


def test_validator_rejects_blocked_with_classification_source(blocked):
    invalid = deepcopy(blocked)
    invalid["classification_source_generated"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(invalid)


def test_validator_rejects_missing_execution_digest(success):
    invalid = deepcopy(success)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_v1(invalid)


def test_markdown_includes_required_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_execution_markdown_v1(success)
    for section in (
        "Source Approval",
        "Retry Failure Context",
        "Execution Scope",
        "Read-Only Cache Inputs",
        "Cache Capture Result",
        "Classification Source Result",
        "Success or Blocked Disposition",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown
