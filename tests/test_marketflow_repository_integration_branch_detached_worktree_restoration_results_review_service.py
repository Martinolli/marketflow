from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_results_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    )


def test_review_builds_deterministically_without_git(monkeypatch):
    calls = []

    def fail_subprocess(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("snapshot mode must not invoke git")

    monkeypatch.setattr(service.subprocess, "run", fail_subprocess)
    first = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    )
    second = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    )
    assert first == second
    assert calls == []


def test_read_only_git_inspection_path_is_isolated(monkeypatch):
    observed = []

    def isolated(repo_root, worktree_path):
        observed.append((repo_root, worktree_path))
        return deepcopy(service.EXPECTED_GIT_SNAPSHOT)

    monkeypatch.setattr(service, "_read_git_snapshot", isolated)
    review = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        repo_root="C:\\fixture-repo"
    )
    assert len(observed) == 1
    assert str(observed[0][0]).endswith("fixture-repo")
    assert review["registered_worktree_clean"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN),
        ("created_offline_except_read_only_git_inspection", True),
        ("governance_only", True),
        ("source_worktree_restoration_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_worktree_manifest_digest", service.EXPECTED_SOURCE_WORKTREE_MANIFEST_DIGEST),
        ("source_worktree_restoration_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_worktree_restoration_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_worktree_restoration_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_remediation_operator_review_digest", service.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("blocked_remediation_execution_artifact_kind", service.EXPECTED_BLOCKED_EXECUTION_ARTIFACT_KIND),
        ("blocked_remediation_execution_status", service.EXPECTED_BLOCKED_EXECUTION_STATUS),
        ("origin_main_commit_at_review", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_name", service.EXPECTED_INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit_at_review", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("integration_branch_exists_local_at_review", True),
        ("integration_branch_matches_required_head_at_review", True),
        ("integration_branch_deleted_or_reset_by_review", False),
        ("worktree_restoration_path", str(service.DEFAULT_WORKTREE_PATH.resolve(strict=False))),
        ("worktree_restoration_path_exists_at_review", True),
        ("registered_worktree_entries_present_at_review", True),
        ("registered_worktree_path_verified", True),
        ("registered_worktree_head_commit", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("registered_worktree_head_verified", True),
        ("registered_worktree_is_detached", True),
        ("registered_worktree_branch_checked_out", False),
        ("registered_worktree_clean", True),
        ("remote_integration_branch_exists_at_review", False),
        ("integration_branch_pushed", False),
        ("worktree_restoration_results_review_created", True),
        ("worktree_restoration_results_review_ready", True),
        ("registered_detached_worktree_reviewed", True),
        ("worktree_head_reviewed", True),
        ("worktree_detached_status_reviewed", True),
        ("worktree_clean_status_reviewed", True),
        ("ready_for_remediation_execution_after_worktree_restoration", True),
        ("remediation_executed", False),
        ("evidence_staged", False),
        ("marketflow_outputs_copied", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("tracked_marketflow_file_count", 0),
        ("worktree_marketflow_path_exists_at_review", False),
        ("marketflow_outputs_not_tracked", True),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("no_tracked_marketflow_files", True),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_review_observations_are_complete_and_pass(review):
    assert [row["observation_id"] for row in review["review_observations"]] == service.REVIEW_OBSERVATION_IDS
    assert all(row["status"] == service.PASS for row in review["review_observations"])
    assert all(
        set(row) == {"observation_id", "status", "expected", "actual", "message"}
        for row in review["review_observations"]
    )


def test_next_chain_gates_and_risk_controls_are_exact(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["next_chain"]) == 7
    assert len(review["next_gates"]) == 7
    assert len(review["risk_controls"]) == 35


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in review["checklist"]
    )
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_digests_are_deterministic(review):
    assert review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
    ] == service.marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest_v1(
        review
    )
    assert review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest"
    ] == service.marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest_v1(
        review
    )


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        review
    )
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_worktree_restoration_execution_digest", "0" * 64),
        ("source_worktree_manifest_digest", "0" * 64),
        ("source_worktree_restoration_approval_digest", "0" * 64),
        ("source_worktree_restoration_operator_review_digest", "0" * 64),
        ("source_worktree_restoration_candidate_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("origin_main_commit_at_review", "0" * 40),
        ("integration_branch_head_commit_at_review", "0" * 40),
        ("integration_branch_exists_local_at_review", False),
        ("integration_branch_matches_required_head_at_review", False),
        ("integration_branch_deleted_or_reset_by_review", True),
        ("worktree_restoration_path_exists_at_review", False),
        ("registered_worktree_entries_present_at_review", False),
        ("registered_worktree_path_verified", False),
        ("registered_worktree_head_commit", "0" * 40),
        ("registered_worktree_head_verified", False),
        ("registered_worktree_is_detached", False),
        ("registered_worktree_branch_checked_out", True),
        ("registered_worktree_clean", False),
        ("remote_integration_branch_exists_at_review", True),
        ("integration_branch_pushed", True),
        ("worktree_restoration_results_review_created", False),
        ("worktree_restoration_results_review_ready", False),
        ("ready_for_remediation_execution_after_worktree_restoration", False),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied", True),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("tracked_marketflow_file_count", 1),
        ("marketflow_outputs_not_tracked", False),
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
        ("next_chain", []),
        ("next_gates", []),
        ("risk_controls", []),
        ("no_tracked_marketflow_files", False),
    ],
)
def test_validator_rejects_invalid_boundaries(review, field, bad_value):
    invalid = deepcopy(review)
    invalid[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError
    ):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest",
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_worktree_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(review, field):
    review.pop(field)
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError
    ):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
            review
        )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("worktree_path_exists", False),
        ("registered_worktree_entries_present", False),
        ("registered_worktree_head_commit", "0" * 40),
        ("registered_worktree_is_detached", False),
        ("registered_worktree_branch_checked_out", True),
        ("registered_worktree_clean", False),
        ("remote_integration_branch_exists", True),
    ],
)
def test_builder_blocks_mismatched_or_dirty_snapshot(field, bad_value):
    snapshot = deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    snapshot[field] = bad_value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError
    ) as exc_info:
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
            git_snapshot=snapshot
        )
    assert exc_info.value.artifact_kind == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_BLOCKED
    assert exc_info.value.blocked_status == service.BLOCKED_WORKTREE_MISMATCH_OR_DIRTY_STATE


def test_markdown_contains_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_markdown_v1(
        review
    )
    for heading in (
        "# MarketFlow Repository Integration Branch Detached Worktree Restoration Results Review v1",
        "## Source Restoration Execution",
        "## Bound Evidence",
        "## Review Scope",
        "## Registered Worktree Review",
        "## Worktree Head Verification",
        "## Worktree Cleanliness Review",
        "## Origin/Main Protection",
        "## Remote Integration Branch Check",
        "## Authority Boundaries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path, review):
    receipt = service.write_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
        tmp_path, git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    )
    path = tmp_path / "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == review
    assert receipt[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
    ] == review[
        "marketflow_repository_integration_branch_detached_worktree_restoration_results_review_digest"
    ]
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationResultsReviewError
    ):
        service.write_marketflow_repository_integration_branch_detached_worktree_restoration_results_review_v1(
            tmp_path, git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT)
        )
