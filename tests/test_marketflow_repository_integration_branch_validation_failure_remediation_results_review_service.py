from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_results_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT),
        evidence_snapshot=deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT),
    )


def test_review_builds_from_deterministic_snapshots(monkeypatch):
    monkeypatch.setattr(service, "_read_git_snapshot", lambda *_: pytest.fail("Git inspected"))
    monkeypatch.setattr(service, "_read_evidence_snapshot", lambda *_: pytest.fail("files inspected"))
    first = service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT),
        evidence_snapshot=deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT),
    )
    second = service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT),
        evidence_snapshot=deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT),
    )
    assert first == second


def test_read_only_inspection_path_is_isolated(monkeypatch):
    calls = []

    def git_reader(*_):
        calls.append("git")
        return deepcopy(service.EXPECTED_GIT_SNAPSHOT)

    def evidence_reader(*_):
        calls.append("evidence")
        return deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT)

    monkeypatch.setattr(service, "_read_git_snapshot", git_reader)
    monkeypatch.setattr(service, "_read_evidence_snapshot", evidence_reader)
    result = service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1()
    assert calls == ["git", "evidence"]
    assert result["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_ONLY_NOT_RETRY_NOT_INTEGRATION_RESULTS_REVIEW_NOT_MAIN),
        ("source_remediation_execution_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_remediation_evidence_manifest_digest", service.EXPECTED_SOURCE_REMEDIATION_EVIDENCE_MANIFEST_DIGEST),
        ("source_staged_inventory_manifest_digest", service.EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST),
        ("source_worktree_restoration_results_review_digest", service.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("origin_main_commit_at_review", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit_at_review", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("integration_branch_matches_required_head_at_review", True),
        ("remote_integration_branch_exists_at_review", False),
        ("detached_integration_worktree_exists_at_review", True),
        ("detached_integration_worktree_head_verified_at_review", True),
        ("detached_integration_worktree_is_detached_at_review", True),
        ("detached_integration_worktree_clean_at_review", True),
        ("source_evidence_root_exists_at_review", True),
        ("staged_evidence_root_exists_at_review", True),
        ("staged_required_manifest_exists_at_review", True),
        ("source_evidence_file_count_at_review", 7),
        ("staged_evidence_file_count_at_review", 7),
        ("source_evidence_total_bytes_at_review", 2458181),
        ("staged_evidence_total_bytes_at_review", 2458181),
        ("source_evidence_manifest_digest_at_review", service.EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST),
        ("staged_evidence_manifest_digest_at_review", service.EXPECTED_SOURCE_STAGED_INVENTORY_MANIFEST_DIGEST),
        ("source_and_staged_evidence_match_at_review", True),
        ("staged_evidence_root_untracked_at_review", True),
        ("marketflow_outputs_tracked_in_repository", False),
        ("marketflow_outputs_tracked_in_detached_worktree", False),
        ("remediation_results_review_created", True),
        ("remediation_results_review_ready", True),
        ("staged_evidence_reviewed", True),
        ("staged_manifest_reviewed", True),
        ("source_staged_digest_match_reviewed", True),
        ("staged_evidence_untracked_reviewed", True),
        ("wrong_worktree_guard_reviewed", True),
        ("ready_for_integration_branch_retry_candidate", True),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied_to_integration_worktree", True),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_approved", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
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
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_next_chain_gates_risk_controls_and_observations(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert [row["observation_id"] for row in review["review_observations"]] == service.REVIEW_OBSERVATION_IDS
    assert all(row["status"] == service.PASS for row in review["review_observations"])


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_review_digests_are_deterministic(review):
    assert review["marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest"] == service.marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest_v1(review)
    assert review["marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest"] == service.marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest_v1(review)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(review)
    assert result["status"] == review["review_status"]
    assert result["total_checks"] == len(service.REQUIRED_CHECK_IDS)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "wrong"),
        ("review_status", "wrong"),
        ("review_scope", "wrong"),
        ("source_remediation_execution_digest", "0" * 64),
        ("source_remediation_evidence_manifest_digest", "0" * 64),
        ("source_staged_inventory_manifest_digest", "0" * 64),
        ("source_worktree_restoration_results_review_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("origin_main_commit_at_review", "0" * 40),
        ("integration_branch_head_commit_at_review", "0" * 40),
        ("detached_integration_worktree_exists_at_review", False),
        ("detached_integration_worktree_head_verified_at_review", False),
        ("detached_integration_worktree_is_detached_at_review", False),
        ("staged_evidence_root_exists_at_review", False),
        ("staged_required_manifest_exists_at_review", False),
        ("source_evidence_file_count_at_review", 6),
        ("staged_evidence_total_bytes_at_review", 1),
        ("source_and_staged_evidence_match_at_review", False),
        ("staged_evidence_root_untracked_at_review", False),
        ("marketflow_outputs_tracked_in_repository", True),
        ("marketflow_outputs_tracked_in_detached_worktree", True),
        ("remediation_results_review_created", False),
        ("remediation_results_review_ready", False),
        ("ready_for_integration_branch_retry_candidate", False),
        ("evidence_regenerated", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
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
def test_validator_rejects_invalid_boundaries(review, field, bad_value):
    changed = deepcopy(review)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_digest",
        "marketflow_repository_integration_branch_validation_failure_remediation_results_review_evidence_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(review, field):
    changed = deepcopy(review)
    changed.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(changed)


@pytest.mark.parametrize(
    ("snapshot_name", "field", "bad_value"),
    [
        ("git", "origin_main_commit", "0" * 40),
        ("git", "integration_branch_head_commit", "0" * 40),
        ("git", "worktree_exists", False),
        ("git", "worktree_head_commit", "0" * 40),
        ("git", "worktree_is_detached", False),
        ("git", "worktree_clean", False),
        ("git", "staged_evidence_ignored", False),
        ("git", "worktree_tracked_marketflow_file_count", 1),
        ("evidence", "source_root_exists", False),
        ("evidence", "staged_root_exists", False),
        ("evidence", "staged_manifest_exists", False),
        ("evidence", "staged_manifest", []),
    ],
)
def test_builder_blocks_mismatched_snapshots(snapshot_name, field, bad_value):
    git_snapshot = deepcopy(service.EXPECTED_GIT_SNAPSHOT)
    evidence_snapshot = deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT)
    target = git_snapshot if snapshot_name == "git" else evidence_snapshot
    target[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError) as error:
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
            git_snapshot=git_snapshot, evidence_snapshot=evidence_snapshot
        )
    assert error.value.artifact_kind == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED


def test_wrong_worktree_guard_blocks_review(tmp_path):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError) as error:
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
            integration_worktree_path=tmp_path,
            git_snapshot=deepcopy(service.EXPECTED_GIT_SNAPSHOT),
            evidence_snapshot=deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT),
        )
    assert error.value.blocked_status == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_BLOCKED_STAGED_EVIDENCE_MISMATCH_OR_TRACKING_RISK


@pytest.mark.parametrize(
    "section",
    [
        "Source Remediation Execution", "Source Worktree Restoration Review", "Failure Context",
        "Review Scope", "Detached Worktree Review", "Staged Evidence Review", "Digest Verification",
        "Tracking and Commit Boundary", "Authority Boundaries", "Next Chain", "Next Gates",
        "Risk Controls", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_contains_required_sections(review, section):
    markdown = service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_markdown_v1(review)
    assert section in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    kwargs = {
        "git_snapshot": deepcopy(service.EXPECTED_GIT_SNAPSHOT),
        "evidence_snapshot": deepcopy(service.EXPECTED_EVIDENCE_SNAPSHOT),
    }
    receipt = service.write_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        tmp_path, **kwargs
    )
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1.json").read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1
    assert receipt["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationResultsReviewError):
        service.write_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
            tmp_path, **kwargs
        )
