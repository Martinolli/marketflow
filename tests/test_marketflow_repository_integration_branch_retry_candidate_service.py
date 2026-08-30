from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import marketflow_repository_integration_branch_retry_candidate_service as service
from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_results_review_service as review_service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_candidate_v1()


def test_candidate_builds_offline(monkeypatch):
    monkeypatch.setattr(review_service, "_git", lambda *_args, **_kwargs: pytest.fail("Git called"))
    monkeypatch.setattr(review_service, "_inventory", lambda *_args: pytest.fail("files inspected"))
    result = service.build_marketflow_repository_integration_branch_retry_candidate_v1()
    assert result["created_offline"] is True


def test_candidate_accepts_valid_source_review():
    review = review_service.build_marketflow_repository_integration_branch_validation_failure_remediation_results_review_v1(
        git_snapshot=deepcopy(review_service.EXPECTED_GIT_SNAPSHOT),
        evidence_snapshot=deepcopy(review_service.EXPECTED_EVIDENCE_SNAPSHOT),
    )
    result = service.build_marketflow_repository_integration_branch_retry_candidate_v1(source_review=review)
    assert result["source_remediation_results_review_digest"] == service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("source_remediation_results_review_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_results_review_evidence_manifest_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_EVIDENCE_MANIFEST_DIGEST),
        ("source_remediation_execution_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_remediation_execution_evidence_manifest_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_EVIDENCE_MANIFEST_DIGEST),
        ("source_staged_inventory_digest", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("source_worktree_restoration_results_review_digest", service.EXPECTED_SOURCE_WORKTREE_RESTORATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("origin_main_commit_at_review", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit_at_review", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_path", str(service.EXPECTED_DETACHED_WORKTREE_PATH.resolve(strict=False))),
        ("detached_integration_worktree_head_commit_at_review", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_clean_at_review", True),
        ("staged_evidence_root_path", str(service.EXPECTED_STAGED_EVIDENCE_ROOT.resolve(strict=False))),
        ("staged_required_manifest_path", str(service.EXPECTED_REQUIRED_MANIFEST_PATH.resolve(strict=False))),
        ("source_and_staged_evidence_match_at_review", True),
        ("integration_branch_retry_candidate_created", True),
        ("integration_branch_retry_candidate_ready_for_operator_review", True),
        ("ready_for_integration_branch_retry_candidate_operator_review", True),
        ("recommended_integration_branch_retry_package", service.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE),
        ("recommendation_status", service.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED),
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
        ("provider_requests_made_in_candidate", False),
        ("market_data_acquisition_performed_in_candidate", False),
        ("dataset_generation_performed_in_candidate", False),
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
def test_required_candidate_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_retry_packages_are_complete_and_unselected(candidate):
    packages = candidate["retry_packages"]
    assert len(packages) == 6
    assert sum(row["status"] == service.BLOCKED_NOT_ALLOWED for row in packages) == 2
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)
    assert packages[0]["package_id"] == service.PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE


def test_future_plan_non_goals_chain_gates_and_controls_are_exact(candidate):
    assert candidate["future_retry_requirements"] == service.FUTURE_RETRY_REQUIREMENTS
    assert candidate["future_retry_execution_plan"] == service.FUTURE_RETRY_EXECUTION_PLAN
    assert candidate["future_retry_execution_plan_status"] == service.PLANNED_NOT_EXECUTED
    assert candidate["retry_non_goals"] == service.RETRY_NON_GOALS
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_candidate_digest_is_deterministic(candidate):
    other = service.build_marketflow_repository_integration_branch_retry_candidate_v1()
    assert candidate == other
    assert candidate["marketflow_repository_integration_branch_retry_candidate_digest"] == service.marketflow_repository_integration_branch_retry_candidate_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_retry_candidate_v1(candidate)
    assert result["status"] == candidate["candidate_status"]
    assert result["total_checks"] == len(service.REQUIRED_CHECK_IDS)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "wrong"),
        ("candidate_status", "wrong"),
        ("candidate_scope", "wrong"),
        ("source_remediation_results_review_digest", "0" * 64),
        ("source_remediation_results_review_evidence_manifest_digest", "0" * 64),
        ("source_remediation_execution_digest", "0" * 64),
        ("source_staged_inventory_digest", "0" * 64),
        ("origin_main_commit_at_review", "0" * 40),
        ("detached_integration_worktree_exists_at_review", False),
        ("staged_evidence_root_path", "missing"),
        ("integration_branch_retry_candidate_created", False),
        ("integration_branch_retry_candidate_ready_for_operator_review", False),
        ("recommended_integration_branch_retry_package", None),
        ("retry_packages", []),
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
        ("future_retry_requirements", {}),
        ("future_retry_execution_plan", []),
        ("retry_non_goals", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_boundaries(candidate, field, bad_value):
    changed = deepcopy(candidate)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_v1(changed)


def test_validator_rejects_recommended_package_selected(candidate):
    changed = deepcopy(candidate)
    changed["retry_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_v1(changed)


def test_validator_rejects_missing_digest(candidate):
    changed = deepcopy(candidate)
    changed.pop("marketflow_repository_integration_branch_retry_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_candidate_v1(changed)


@pytest.mark.parametrize(
    "section",
    [
        "Source Remediation Results Review", "Failure Context", "Remediation Context",
        "Candidate Scope", "Retry Philosophy", "Proposed Retry Packages",
        "Recommended Retry Package", "Future Retry Requirements", "Future Retry Execution Plan",
        "Retry Non-Goals", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_contains_required_sections(candidate, section):
    markdown = service.build_marketflow_repository_integration_branch_retry_candidate_markdown_v1(candidate)
    assert section in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    receipt = service.write_marketflow_repository_integration_branch_retry_candidate_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_candidate_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1
    assert receipt["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryCandidateError):
        service.write_marketflow_repository_integration_branch_retry_candidate_v1(tmp_path)
