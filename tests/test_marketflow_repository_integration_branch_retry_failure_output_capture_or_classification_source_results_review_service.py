from copy import deepcopy
import json
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_service as service,
)


def _snapshot(**overrides):
    counts = [136, 131, 122, 112, 111, *([1] * 24)]
    values = {
        "lastfailed_cache_path": str(service.source.EXPECTED_INTEGRATION_WORKTREE / service.source.LASTFAILED_RELATIVE_PATH),
        "lastfailed_cache_exists": True,
        "lastfailed_cache_read": True,
        "lastfailed_cache_parseable_json": True,
        "lastfailed_cache_sha256": service.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count": 1404,
        "lastfailed_nodeids_extracted": True,
        "failed_or_errored_nodeids_count": 1404,
        "nodeids_cache_path": str(service.source.EXPECTED_INTEGRATION_WORKTREE / service.source.NODEIDS_RELATIVE_PATH),
        "nodeids_cache_exists": True,
        "nodeids_cache_read": True,
        "nodeids_cache_parseable_json": True,
        "nodeids_cache_sha256": service.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count": 26288,
        "module_summary_generated": True,
        "module_summary": [
            {"module_path": f"tests/test_module_{index:02d}.py", "nodeid_count": count}
            for index, count in enumerate(counts, start=1)
        ],
        "module_summary_total_modules": 29,
        "module_summary_truncated": False,
        "origin_main_commit": service.source.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head_commit": service.source.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(service.source.EXPECTED_INTEGRATION_WORKTREE),
        "detached_integration_worktree_head_commit": service.source.INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_manifest_digest": service.source.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
    }
    values.update(overrides)
    return values


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        cache_snapshot=_snapshot()
    )


def test_review_builds_from_deterministic_cache_snapshot(review):
    assert review["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1
    assert review["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY
    assert review["review_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_ONLY_NOT_CLASSIFICATION_REENTRY_NOT_RETRY_NOT_MAIN
    assert review["created_offline_except_read_only_cache_and_file_inspection"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


def test_read_only_cache_verification_path_is_isolated(monkeypatch, tmp_path):
    snapshot = _snapshot()
    protected = {
        "origin_main_commit": snapshot["origin_main_commit"],
        "integration_branch_head_commit": snapshot["integration_branch_head_commit"],
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": snapshot["detached_integration_worktree_path"],
        "detached_integration_worktree_head_commit": snapshot["detached_integration_worktree_head_commit"],
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean": True,
        "staged_evidence_manifest_digest": snapshot["staged_evidence_manifest_digest"],
        "repository_tracked_marketflow_count": 0,
        "worktree_tracked_marketflow_count": 0,
    }
    cache = {key: value for key, value in snapshot.items() if key.startswith(("lastfailed_", "nodeids_", "failed_or_", "module_summary"))}
    calls = []
    monkeypatch.setattr(service.source, "_snapshot", lambda *_: deepcopy(protected))
    monkeypatch.setattr(service.source, "_cache_capture", lambda *_, **__: calls.append("read") or deepcopy(cache))
    monkeypatch.setattr(service.source, "_git", lambda *_: subprocess.CompletedProcess([], 0, "", ""))
    monkeypatch.setattr(
        service.source,
        "marketflow_repository_integration_branch_retry_failure_pytest_cache_classification_source_manifest_digest_v1",
        lambda *_: service.SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST,
    )
    built = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        repo_root=tmp_path, integration_worktree_path=tmp_path
    )
    assert calls == ["read"]
    assert built["classification_source_results_review_ready"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        ("source_output_capture_execution_digest", service.SOURCE_OUTPUT_CAPTURE_EXECUTION_DIGEST),
        ("source_classification_source_manifest_digest", service.SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST),
        ("source_output_capture_approval_digest", service.source.SOURCE_OUTPUT_CAPTURE_APPROVAL_DIGEST),
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
        ("origin_main_commit", service.source.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit", service.source.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_head_commit", service.source.INTEGRATION_HEAD_COMMIT),
        ("staged_evidence_manifest_digest", service.source.EXPECTED_STAGED_EVIDENCE_DIGEST),
    ],
)
def test_review_binds_source_and_protected_state(review, field, expected):
    assert review[field] == expected


def test_review_verifies_cache_and_classification_source(review):
    assert review["lastfailed_cache_exists_at_review"] is True
    assert review["lastfailed_cache_read_for_review"] is True
    assert review["lastfailed_cache_parseable_json_at_review"] is True
    assert review["lastfailed_cache_sha256_at_review"] == service.EXPECTED_LASTFAILED_SHA256
    assert review["lastfailed_cache_entry_count_at_review"] == 1404
    assert review["nodeids_cache_exists_at_review"] is True
    assert review["nodeids_cache_read_for_review"] is True
    assert review["nodeids_cache_parseable_json_at_review"] is True
    assert review["nodeids_cache_sha256_at_review"] == service.EXPECTED_NODEIDS_SHA256
    assert review["nodeids_cache_entry_count_at_review"] == 26288
    assert review["classification_source_generated"] is True
    assert review["classification_source_reviewed"] is True
    assert review["module_summary_reviewed"] is True
    assert review["module_summary_module_count"] == 29
    assert review["module_summary_untruncated"] is True
    assert review["largest_module_nodeid_counts_reviewed"] == [136, 131, 122, 112, 111]


def test_review_preserves_classification_limitations(review):
    assert review["classification_source_limitations"] == service.CLASSIFICATION_SOURCE_LIMITATIONS
    assert review["classification_source_limitations_reviewed"] is True
    assert review["classification_source_can_distinguish_failures_from_errors"] is False
    assert review["failure_error_separation_not_claimed"] is True
    assert review["first_failure_identified"] is False
    assert review["first_error_identified"] is False
    assert review["first_failure_or_error_order_not_claimed"] is True
    assert review["cache_treated_as_retry_evidence"] is False


@pytest.mark.parametrize(
    "field,expected",
    [
        ("classification_source_results_review_created", True),
        ("classification_source_results_review_ready", True),
        ("lastfailed_cache_reviewed", True),
        ("nodeids_cache_reviewed", True),
        ("module_summary_reviewed", True),
        ("ready_for_classification_method_reentry", True),
        ("classification_method_reentry_created", False),
        ("new_classification_method_candidate_created", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("main_merge_approval_created", False),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("diagnostic_output_captured", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("pytest_cache_committed", False),
        ("evidence_regenerated", False),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
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
def test_review_preserves_authority_boundaries(review, field, expected):
    assert review[field] == expected


def test_review_defines_observations_next_chain_gates_and_controls(review):
    assert [row["observation_id"] for row in review["review_observations"]] == service.REVIEW_OBSERVATION_IDS
    assert all(row["status"] == service.PASS for row in review["review_observations"])
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_checklist_summary_and_digests_are_deterministic(review):
    assert len(review["checklist"]) == len(service.CHECK_IDS) == 65
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert review["summary"]["total_checks"] == 65
    assert review["summary"]["passed_checks"] == 65
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest"] == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest_v1(review)
    assert review["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest"] == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest_v1(review)
    assert review == service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(cache_snapshot=_snapshot())


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_READY
    assert result["passed_checks"] == 65
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "wrong"),
        ("review_status", "wrong"),
        ("review_scope", "wrong"),
        ("source_output_capture_execution_digest", "0" * 64),
        ("source_classification_source_manifest_digest", "0" * 64),
        ("lastfailed_cache_sha256_at_review", "0" * 64),
        ("nodeids_cache_sha256_at_review", "0" * 64),
        ("lastfailed_cache_entry_count_at_review", 0),
        ("nodeids_cache_entry_count_at_review", 0),
        ("classification_source_generated", False),
        ("module_summary_generated", False),
        ("module_summary_reviewed", False),
        ("classification_source_limitations", []),
        ("classification_source_limitations_reviewed", False),
        ("classification_source_can_distinguish_failures_from_errors", True),
        ("failure_error_separation_not_claimed", False),
        ("first_failure_identified", True),
        ("first_error_identified", True),
        ("cache_treated_as_retry_evidence", True),
        ("root_full_regression_is_retry_evidence", True),
        ("classification_source_results_review_created", False),
        ("classification_source_results_review_ready", False),
        ("ready_for_classification_method_reentry", False),
        ("classification_method_reentry_created", True),
        ("new_retry_candidate_created", True),
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
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
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
def test_validator_rejects_changed_review_contract(review, field, value):
    invalid = deepcopy(review)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_digest",
        "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_cache_manifest_digest",
    ],
)
def test_validator_rejects_missing_digest(review, field):
    invalid = deepcopy(review)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(invalid)


def test_cache_mismatch_builds_fail_closed_blocked_review():
    blocked = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        cache_snapshot=_snapshot(lastfailed_cache_sha256="0" * 64)
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_BLOCKED
    assert blocked["classification_source_results_review_ready"] is False
    assert blocked["ready_for_classification_method_reentry"] is False


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_markdown_v1(review)
    for section in (
        "Source Execution",
        "Retry Failure Context",
        "Cache Review",
        "Classification Source Review",
        "Limitations",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json(tmp_path, review):
    result = service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        tmp_path, cache_snapshot=_snapshot()
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == review
    assert result["artifact_kind"] == review["artifact_kind"]


def test_writer_refuses_overwrite(tmp_path):
    service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        tmp_path, cache_snapshot=_snapshot()
    )
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
            tmp_path, cache_snapshot=_snapshot()
        )
