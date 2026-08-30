from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import marketflow_repository_integration_branch_retry_candidate_service as candidate_service
from marketflow.services import (
    marketflow_repository_integration_branch_retry_candidate_operator_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1()


def test_review_builds_offline(monkeypatch):
    candidate = candidate_service.build_marketflow_repository_integration_branch_retry_candidate_v1()
    monkeypatch.setattr(candidate_service, "build_marketflow_repository_integration_branch_retry_candidate_v1", lambda: pytest.fail("default source rebuilt"))
    result = service.build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(
        source_candidate=candidate
    )
    assert result["created_offline"] is True
    assert result["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("source_integration_branch_retry_candidate_digest", service.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_results_review_evidence_manifest_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST),
        ("source_remediation_execution_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_remediation_execution_evidence_manifest_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST),
        ("source_staged_inventory_digest", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("source_worktree_restoration_results_review_digest", service.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("attempted_execution_commit", candidate_service.ATTEMPTED_EXECUTION_COMMIT),
        ("original_blocked_status", "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED"),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("later_wrong_worktree_rerun_diagnostic_only", True),
        ("later_wrong_worktree_rerun_overrides_first_failure", False),
        ("origin_main_commit_at_review", candidate_service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit_at_review", candidate_service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_path", str(candidate_service.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False))),
        ("detached_integration_worktree_head_commit_at_review", candidate_service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_clean_at_review", True),
        ("staged_evidence_root_path", str(candidate_service.EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False))),
        ("staged_required_manifest_path", str(candidate_service.EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False))),
        ("staged_evidence_manifest_digest_at_review", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("integration_branch_retry_candidate_operator_review_created", True),
        ("integration_branch_retry_candidate_operator_review_ready", True),
        ("retry_packages_reviewed", True),
        ("retry_requirements_reviewed", True),
        ("future_retry_plan_reviewed", True),
        ("retry_non_goals_reviewed", True),
        ("ready_for_integration_branch_retry_approval", False),
        ("recommended_integration_branch_retry_package", candidate_service.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE),
        ("recommended_package_selected", False),
        ("integration_branch_retry_selected", False),
        ("integration_branch_retry_approved", False),
        ("integration_branch_retry_authorized", False),
        ("integration_branch_retry_executed", False),
        ("integration_branch_retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
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
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", service.FUTURE_APPROVAL_NOT_CREATED),
        ("recommended_action", service.OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_INTEGRATION_RETRY),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_reviewed_packages_are_complete_and_unselected(review):
    packages = review["reviewed_retry_packages"]
    assert len(packages) == 6
    assert sum(row["review_status"] == service.REVIEWED_BLOCKED_NOT_ALLOWED for row in packages) == 2
    assert packages[0]["review_status"] == service.REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_requirements_plan_and_non_goals_are_reviewed_not_executed(review):
    requirements = review["reviewed_future_retry_requirements"]
    plan = review["reviewed_future_retry_plan"]
    non_goals = review["reviewed_retry_non_goals"]
    assert len(requirements) == len(candidate_service.FUTURE_RETRY_REQUIREMENTS)
    assert all(row["review_status"] == service.REVIEWED_REQUIRED_FOR_FUTURE_RETRY for row in requirements)
    assert all(row["execution_status"] == service.NOT_EXECUTED for row in requirements)
    assert len(plan) == len(candidate_service.FUTURE_RETRY_EXECUTION_PLAN)
    assert all(row["review_status"] == service.REVIEWED_PLANNED_NOT_EXECUTED for row in plan)
    assert all(row["execution_status"] == service.NOT_EXECUTED for row in plan)
    assert len(non_goals) == len(candidate_service.RETRY_NON_GOALS)
    assert all(row["review_status"] == service.REVIEWED_ACTIVE for row in non_goals)


def test_next_chain_gates_and_risk_controls_are_exact(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["ready_for_integration_branch_retry_approval"] is False


def test_operator_review_digest_is_deterministic(review):
    other = service.build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1()
    assert review == other
    assert review["marketflow_repository_integration_branch_retry_candidate_operator_review_digest"] == service.marketflow_repository_integration_branch_retry_candidate_operator_review_digest_v1(review)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(review)
    assert result["status"] == review["review_status"]
    assert result["total_checks"] == len(service.REQUIRED_CHECK_IDS)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "wrong"),
        ("review_status", "wrong"),
        ("review_scope", "wrong"),
        ("source_integration_branch_retry_candidate_digest", "0" * 64),
        ("source_remediation_results_review_digest", "0" * 64),
        ("source_remediation_execution_digest", "0" * 64),
        ("source_staged_inventory_digest", "0" * 64),
        ("origin_main_commit_at_review", "0" * 40),
        ("detached_integration_worktree_exists_at_review", False),
        ("staged_evidence_root_path", "missing"),
        ("first_integration_pytest_authoritative", False),
        ("first_integration_pytest_passed", True),
        ("later_wrong_worktree_rerun_overrides_first_failure", True),
        ("integration_branch_retry_candidate_operator_review_created", False),
        ("integration_branch_retry_candidate_operator_review_ready", False),
        ("retry_packages_reviewed", False),
        ("retry_requirements_reviewed", False),
        ("future_retry_plan_reviewed", False),
        ("retry_non_goals_reviewed", False),
        ("reviewed_retry_packages", []),
        ("reviewed_future_retry_requirements", []),
        ("reviewed_future_retry_plan", []),
        ("ready_for_integration_branch_retry_approval", True),
        ("recommended_package_selected", True),
        ("integration_branch_retry_selected", True),
        ("integration_branch_retry_approved", True),
        ("integration_branch_retry_authorized", True),
        ("integration_branch_retry_executed", True),
        ("integration_branch_retry_results_review_created", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
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
def test_validator_rejects_invalid_boundaries(review, field, bad_value):
    changed = deepcopy(review)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(changed)


def test_validator_rejects_recommended_package_selected(review):
    changed = deepcopy(review)
    changed["reviewed_retry_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(changed)


def test_validator_rejects_missing_digest(review):
    changed = deepcopy(review)
    changed.pop("marketflow_repository_integration_branch_retry_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(changed)


@pytest.mark.parametrize(
    "section",
    [
        "Source Retry Candidate", "Source Remediation Results Review", "Failure Context",
        "Remediation Context", "Review Scope", "Reviewed Retry Philosophy",
        "Reviewed Retry Packages", "Reviewed Future Retry Requirements",
        "Reviewed Future Retry Plan", "Reviewed Retry Non-Goals", "Recommendation",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_contains_required_sections(review, section):
    markdown = service.build_marketflow_repository_integration_branch_retry_candidate_operator_review_markdown_v1(review)
    assert section in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    receipt = service.write_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_candidate_operator_review_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1
    assert receipt["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_READY
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_candidate_operator_review_v1(tmp_path)
