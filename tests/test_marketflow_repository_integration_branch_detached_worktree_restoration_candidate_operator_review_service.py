from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1()


def test_review_builds_offline_and_deterministically(review):
    assert service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1() == review
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY),
        ("source_worktree_restoration_candidate_artifact_kind", service.source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1),
        ("source_worktree_restoration_candidate_status", service.source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("source_worktree_restoration_candidate_scope", service.source.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY),
        ("source_worktree_restoration_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_remediation_approval_digest", service.source.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_remediation_operator_review_digest", service.source.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.source.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.source.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.source.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("blocked_remediation_execution_artifact_kind", service.source.BLOCKED_REMEDIATION_EXECUTION_ARTIFACT_KIND),
        ("blocked_remediation_execution_status", service.source.BLOCKED_REMEDIATION_EXECUTION_STATUS),
        ("integration_branch_name", service.source.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit", service.source.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("integration_branch_exists_local", True),
        ("integration_branch_matches_required_head", True),
        ("detached_integration_worktree_exists", False),
        ("registered_worktree_entries_present", False),
        ("git_worktrees_directory_present", False),
        ("remote_integration_branch_exists", False),
        ("origin_main_commit", service.source.ORIGIN_MAIN_COMMIT),
        ("source_evidence_root_path", service.source.SOURCE_EVIDENCE_ROOT_PATH),
        ("source_evidence_root_exists", True),
        ("source_required_manifest_name", service.source.SOURCE_REQUIRED_MANIFEST_NAME),
        ("source_required_manifest_exists", True),
        ("source_evidence_file_count", 7),
        ("source_evidence_total_bytes", 2458181),
        ("source_evidence_ignored_by_gitignore", True),
        ("marketflow_outputs_tracked", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("worktree_restoration_candidate_created", True),
        ("worktree_restoration_candidate_ready_for_operator_review", True),
        ("worktree_restoration_candidate_operator_review_created", True),
        ("worktree_restoration_candidate_operator_review_ready", True),
        ("restoration_packages_reviewed", True),
        ("restoration_requirements_reviewed", True),
        ("future_restoration_plan_reviewed", True),
        ("restoration_non_goals_reviewed", True),
        ("ready_for_worktree_restoration_approval", False),
        ("recommended_worktree_restoration_package", service.source.PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD),
        ("recommended_package_selected", False),
        ("worktree_restoration_selected", False),
        ("worktree_restoration_approved", False),
        ("worktree_restoration_authorized", False),
        ("worktree_restoration_executed", False),
        ("detached_worktree_created", False),
        ("detached_worktree_restored", False),
        ("detached_worktree_deleted", False),
        ("integration_branch_deleted_or_reset", False),
        ("remediation_executed", False),
        ("evidence_staged", False),
        ("marketflow_outputs_copied", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
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
        ("worktree_restoration_review_status", "REVIEWED_PLANNING_ONLY"),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", "FUTURE_APPROVAL_NOT_CREATED"),
        ("recommended_action", service.RECOMMENDED_ACTION),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_all_restoration_packages_are_reviewed_without_selection(review):
    packages = review["reviewed_worktree_restoration_packages"]
    assert packages == service.REVIEWED_WORKTREE_RESTORATION_PACKAGES
    assert len(packages) == 6
    assert sum(row["source_status"].startswith("BLOCKED_") for row in packages) == 3
    assert packages[0]["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_all_requirements_are_reviewed_not_executed(review):
    rows = review["reviewed_worktree_restoration_requirements"]
    assert rows == service.REVIEWED_WORKTREE_RESTORATION_REQUIREMENTS
    assert len(rows) == len(service.source.WORKTREE_RESTORATION_REQUIREMENTS) == 17
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_WORKTREE_RESTORATION" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_all_future_plan_steps_are_reviewed_not_executed(review):
    rows = review["reviewed_future_worktree_restoration_plan"]
    assert rows == service.REVIEWED_FUTURE_WORKTREE_RESTORATION_PLAN
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_all_non_goals_remain_active(review):
    rows = review["reviewed_worktree_restoration_non_goals"]
    assert rows == service.REVIEWED_WORKTREE_RESTORATION_NON_GOALS
    assert len(rows) == 21
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in rows)


def test_reviewed_philosophy_and_governance_sections_are_exact(review):
    assert review["reviewed_worktree_restoration_philosophy"] == service.source.WORKTREE_RESTORATION_PHILOSOPHY
    assert review["reviewed_worktree_restoration_goal"] == service.source.WORKTREE_RESTORATION_GOAL
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert review["recommendation_reason"] == service.RECOMMENDATION_REASON


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 57
    assert review["summary"]["passed_checks"] == 57
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["ready_for_worktree_restoration_approval"] is False


def test_review_digest_is_deterministic(review):
    assert review["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"] == service.marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest_v1(review)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_worktree_restoration_candidate_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("blocked_remediation_execution_status", ""),
        ("integration_branch_exists_local", False),
        ("integration_branch_head_commit", ""),
        ("source_evidence_root_exists", False),
        ("source_required_manifest_exists", False),
        ("worktree_restoration_candidate_operator_review_created", False),
        ("worktree_restoration_candidate_operator_review_ready", False),
        ("restoration_packages_reviewed", False),
        ("restoration_requirements_reviewed", False),
        ("future_restoration_plan_reviewed", False),
        ("restoration_non_goals_reviewed", False),
        ("ready_for_worktree_restoration_approval", True),
        ("recommended_package_selected", True),
        ("reviewed_worktree_restoration_packages", []),
        ("reviewed_worktree_restoration_requirements", []),
        ("reviewed_future_worktree_restoration_plan", []),
        ("worktree_restoration_selected", True),
        ("worktree_restoration_approved", True),
        ("worktree_restoration_executed", True),
        ("detached_worktree_created", True),
        ("detached_worktree_restored", True),
        ("detached_worktree_deleted", True),
        ("integration_branch_deleted_or_reset", True),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied", True),
        ("marketflow_outputs_committed", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
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
    invalid = deepcopy(review)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(invalid)


def test_validator_rejects_recommended_package_selected(review):
    invalid = deepcopy(review)
    invalid["reviewed_worktree_restoration_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(invalid)


def test_builder_rejects_changed_source_candidate_digest():
    candidate = service.source.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1()
    candidate["source_evidence_file_count"] = 8
    with pytest.raises(service.source.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(
            source_candidate=candidate
        )


def test_validator_rejects_missing_digest(review):
    review.pop("marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(review)


def test_markdown_contains_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_markdown_v1(review)
    for heading in (
        "# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate Operator Review v1",
        "## Source Restoration Candidate", "## Blocked Remediation Execution Observation",
        "## Review Scope", "## Reviewed Worktree Restoration Philosophy",
        "## Reviewed Restoration Packages", "## Reviewed Restoration Requirements",
        "## Reviewed Future Restoration Plan", "## Reviewed Non-Goals", "## Recommendation",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path, review):
    receipt = service.write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1.json").read_text(encoding="utf-8"))
    assert payload == review
    assert receipt["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"] == review["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1(tmp_path)
