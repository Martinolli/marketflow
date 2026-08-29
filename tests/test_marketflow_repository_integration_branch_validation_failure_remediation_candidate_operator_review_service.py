from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1()


def test_review_builds_offline_and_deterministically(review):
    assert service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1() == review
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("attempted_execution_branch", "feature/marketflow-repository-integration-branch-execution-v1"),
        ("attempted_execution_commit", "9d3dbc488747a0e17921bd4dcab7be2fadefc5ba"),
        ("integration_branch_name", "integration/marketflow-terminal-evidence-stack-validation-v1"),
        ("integration_branch_head_commit", "220fbc220365fce9cae13ab4853cddff118c0187"),
        ("integration_base_commit", "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"),
        ("integration_source_commit", "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("first_integration_pytest_skipped_count", 7),
        ("later_isolated_rerun_passed", True),
        ("later_isolated_rerun_passed_count", 26842),
        ("later_isolated_rerun_skipped_count", 7),
        ("later_isolated_rerun_overrides_first_failure", False),
        ("representative_failure_domain", "ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH"),
        ("required_ready_digest_prefix", "57c0a06e"),
        ("actual_blocked_digest_prefix", "783e0013"),
        ("missing_required_file", "acquisition_provider_evidence_run_manifest.json"),
        ("diagnosed_root_cause", "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT"),
        ("later_rerun_problem", "PYTEST_RERUN_EXECUTED_FROM_FEATURE_WORKTREE_NOT_DETACHED_INTEGRATION_WORKTREE"),
        ("remediation_candidate_operator_review_created", True),
        ("remediation_candidate_operator_review_ready", True),
        ("remediation_packages_reviewed", True),
        ("remediation_requirements_reviewed", True),
        ("future_remediation_plan_reviewed", True),
        ("root_cause_question_status_reviewed", True),
        ("ready_for_remediation_approval", False),
        ("remediation_selected", False),
        ("remediation_approved", False),
        ("remediation_authorized", False),
        ("remediation_executed", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_execution_digest_generated", False),
        ("successful_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_merge_performed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("marketflow_outputs_committed", False),
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
        ("broker_execution", "NOT_AUTHORIZED"),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", service.RECOMMENDED_NEXT_TASK_STATUS),
        ("recommended_action", service.RECOMMENDED_ACTION),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_all_six_packages_are_reviewed_without_selection(review):
    packages = review["reviewed_remediation_packages"]
    assert packages == service.REVIEWED_REMEDIATION_PACKAGES
    assert len(packages) == 6
    assert sum(row["review_status"].startswith("REVIEWED_BLOCKED_") for row in packages) == 2
    assert packages[0]["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_requirements_plan_non_goals_and_questions_are_reviewed(review):
    assert review["reviewed_remediation_requirements"] == service.REVIEWED_REMEDIATION_REQUIREMENTS
    assert len(review["reviewed_remediation_requirements"]) == 16
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION" for row in review["reviewed_remediation_requirements"])
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in review["reviewed_remediation_requirements"])
    assert review["reviewed_future_remediation_plan"] == service.REVIEWED_FUTURE_REMEDIATION_PLAN
    assert len(review["reviewed_future_remediation_plan"]) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" for row in review["reviewed_future_remediation_plan"])
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in review["reviewed_future_remediation_plan"])
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == 20
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_non_goals"])
    assert review["root_cause_question_review"] == service.ROOT_CAUSE_QUESTION_REVIEW
    assert len(review["root_cause_question_review"]["answered_by_diagnosis"]) == 4
    assert len(review["root_cause_question_review"]["still_requires_remediation_execution_or_review"]) == 5


def test_reviewed_philosophy_chain_gates_and_controls(review):
    assert review["reviewed_remediation_philosophy"] == service.REVIEWED_REMEDIATION_PHILOSOPHY
    assert review["reviewed_remediation_boundary"] == service.REVIEWED_REMEDIATION_BOUNDARY
    assert review["reviewed_remediation_goal"] == service.REVIEWED_REMEDIATION_GOAL
    assert review["reviewed_remediation_philosophy_status"] == service.REVIEWED_PLANNING_ONLY
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 8
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 8
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 40


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 55
    assert review["summary"]["passed_checks"] == 55
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["ready_for_remediation_approval"] is False
    assert review["summary"]["integration_retry_allowed_now"] is False


def test_review_digest_is_deterministic(review):
    assert review["marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"] == service.marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest_v1(review)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_remediation_candidate_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("source_merge_strategy_approval_digest", "0" * 64),
        ("first_integration_pytest_passed", True),
        ("later_isolated_rerun_overrides_first_failure", True),
        ("diagnosed_root_cause", ""),
        ("remediation_candidate_operator_review_created", False),
        ("remediation_candidate_operator_review_ready", False),
        ("remediation_packages_reviewed", False),
        ("remediation_requirements_reviewed", False),
        ("future_remediation_plan_reviewed", False),
        ("ready_for_remediation_approval", True),
        ("reviewed_remediation_packages", []),
        ("reviewed_remediation_requirements", []),
        ("reviewed_future_remediation_plan", []),
        ("remediation_selected", True),
        ("remediation_approved", True),
        ("remediation_executed", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_execution_digest_generated", True),
        ("successful_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
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
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(invalid)


def test_validator_rejects_recommended_package_selected(review):
    invalid = deepcopy(review)
    invalid["reviewed_remediation_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(invalid)


def test_validator_rejects_missing_digest(review):
    review.pop("marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(review)


def test_invalid_source_candidate_fails_closed():
    source_candidate = service.source.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1()
    source_candidate["source_failure_diagnosis_digest"] = "0" * 64
    with pytest.raises(Exception):
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(source_candidate=source_candidate)


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_markdown_v1(review)
    for title in (
        "MarketFlow Repository Integration Branch Validation Failure Remediation Candidate Operator Review v1",
        "Source Remediation Candidate", "Failure Summary", "Root Cause Review",
        "Review Scope", "Reviewed Remediation Philosophy", "Reviewed Remediation Packages",
        "Reviewed Remediation Requirements", "Reviewed Future Remediation Plan",
        "Reviewed Non-Goals", "Root-Cause Question Review", "Recommendation",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ):
        assert title in markdown


def test_writer_round_trips_without_overwrite(tmp_path, review):
    receipt = service.write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1.json").read_text(encoding="utf-8"))
    assert payload == review
    assert receipt["marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"] == review["marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1(tmp_path)
