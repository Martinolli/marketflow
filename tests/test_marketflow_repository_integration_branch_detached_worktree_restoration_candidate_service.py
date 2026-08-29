from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_candidate_service as service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1()


def test_candidate_builds_offline_and_deterministically(candidate):
    assert service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1() == candidate
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["worktree_restoration_candidate_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_remediation_operator_review_digest", service.EXPECTED_SOURCE_REMEDIATION_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_REMEDIATION_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_MERGE_STRATEGY_APPROVAL_DIGEST),
        ("blocked_remediation_execution_artifact_kind", service.BLOCKED_REMEDIATION_EXECUTION_ARTIFACT_KIND),
        ("blocked_remediation_execution_status", service.BLOCKED_REMEDIATION_EXECUTION_STATUS),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit", service.INTEGRATION_BRANCH_HEAD_COMMIT),
        ("integration_branch_exists_local", True),
        ("integration_branch_matches_required_head", True),
        ("detached_integration_worktree_exists", False),
        ("registered_worktree_entries_present", False),
        ("git_worktrees_directory_present", False),
        ("remote_integration_branch_exists", False),
        ("origin_main_commit", service.ORIGIN_MAIN_COMMIT),
        ("source_evidence_root_path", service.SOURCE_EVIDENCE_ROOT_PATH),
        ("source_evidence_root_exists", True),
        ("source_required_manifest_name", service.SOURCE_REQUIRED_MANIFEST_NAME),
        ("source_required_manifest_exists", True),
        ("source_evidence_file_count", 7),
        ("source_evidence_total_bytes", 2458181),
        ("source_evidence_ignored_by_gitignore", True),
        ("marketflow_outputs_tracked", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("worktree_restoration_candidate_created", True),
        ("worktree_restoration_candidate_ready_for_operator_review", True),
        ("ready_for_worktree_restoration_operator_review", True),
        ("recommended_worktree_restoration_package", service.PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD),
        ("recommendation_status", service.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED),
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
        ("successful_execution_digest_generated", False),
        ("successful_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_candidate", False),
        ("market_data_acquisition_performed_in_candidate", False),
        ("dataset_generation_performed_in_candidate", False),
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
    ],
)
def test_required_candidate_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_restoration_packages_are_complete_and_candidate_only(candidate):
    packages = candidate["worktree_restoration_packages"]
    assert packages == service.WORKTREE_RESTORATION_PACKAGES
    assert len(packages) == 6
    assert sum(row["status"].startswith("BLOCKED_") for row in packages) == 3
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_governance_sections_are_exact(candidate):
    assert candidate["worktree_restoration_philosophy"] == service.WORKTREE_RESTORATION_PHILOSOPHY
    assert candidate["worktree_restoration_boundary"] == service.WORKTREE_RESTORATION_BOUNDARY
    assert candidate["worktree_restoration_goal"] == service.WORKTREE_RESTORATION_GOAL
    assert candidate["worktree_restoration_requirements"] == service.WORKTREE_RESTORATION_REQUIREMENTS
    assert candidate["future_worktree_restoration_plan"] == service.FUTURE_WORKTREE_RESTORATION_PLAN
    assert candidate["future_worktree_restoration_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["worktree_restoration_non_goals"] == service.WORKTREE_RESTORATION_NON_GOALS
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 55
    assert candidate["summary"]["passed_checks"] == 55
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["remediation_execution_ready_now"] is False


def test_candidate_digest_is_deterministic(candidate):
    assert candidate["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"] == service.marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_remediation_approval_digest", "0" * 64),
        ("blocked_remediation_execution_status", ""),
        ("integration_branch_exists_local", False),
        ("integration_branch_head_commit", ""),
        ("source_evidence_root_exists", False),
        ("source_required_manifest_exists", False),
        ("worktree_restoration_candidate_created", False),
        ("worktree_restoration_candidate_ready_for_operator_review", False),
        ("recommended_worktree_restoration_package", ""),
        ("worktree_restoration_packages", []),
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
        ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_boundaries(candidate, field, bad_value):
    invalid = deepcopy(candidate)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["worktree_restoration_requirements", "future_worktree_restoration_plan", "risk_controls"],
)
def test_validator_rejects_missing_governance_sections(candidate, field):
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(invalid)


def test_builder_rejects_mismatched_worktree_observation():
    observation = deepcopy(service.DEFAULT_WORKTREE_OBSERVATION)
    observation["source_required_manifest_exists"] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(
            worktree_observation=observation
        )


def test_validator_rejects_recommended_package_selected(candidate):
    invalid = deepcopy(candidate)
    invalid["worktree_restoration_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(invalid)


def test_validator_rejects_missing_digest(candidate):
    candidate.pop("marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(candidate)


def test_markdown_contains_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_markdown_v1(candidate)
    for heading in (
        "# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate v1",
        "## Source Remediation Approval", "## Blocked Remediation Execution Observation",
        "## Candidate Scope", "## Worktree Restoration Philosophy",
        "## Proposed Restoration Packages", "## Recommended Restoration Package",
        "## Future Restoration Requirements", "## Future Restoration Plan",
        "## Restoration Non-Goals", "## Next Chain", "## Next Gates",
        "## Risk Controls", "## Authority Boundaries", "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path, candidate):
    receipt = service.write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1.json").read_text(encoding="utf-8"))
    assert payload == candidate
    assert receipt["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"] == candidate["marketflow_repository_integration_branch_detached_worktree_restoration_candidate_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationCandidateError):
        service.write_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_v1(tmp_path)
