from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_candidate_service as service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1()


def test_candidate_builds_offline_and_deterministically(candidate):
    assert service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1() == candidate
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["remediation_candidate_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY),
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
        ("remediation_candidate_created", True),
        ("remediation_candidate_ready_for_operator_review", True),
        ("recommended_remediation_package", service.PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE),
        ("recommendation_status", service.RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED),
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
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_candidate_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_remediation_packages_are_complete_and_candidate_only(candidate):
    packages = candidate["remediation_packages"]
    assert packages == service.REMEDIATION_PACKAGES
    assert len(packages) == 6
    assert sum(row["status"].startswith("BLOCKED_") for row in packages) == 2
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_governance_sections_are_exact(candidate):
    assert candidate["remediation_requirements"] == service.REMEDIATION_REQUIREMENTS
    assert len(candidate["remediation_requirements"]) == 16
    assert candidate["future_remediation_execution_plan"] == service.FUTURE_REMEDIATION_EXECUTION_PLAN
    assert candidate["future_remediation_execution_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["remediation_non_goals"] == service.REMEDIATION_NON_GOALS
    assert len(candidate["remediation_non_goals"]) == 20
    assert candidate["root_cause_question_status"] == service.ROOT_CAUSE_QUESTION_STATUS
    assert len(candidate["root_cause_question_status"]["answered_by_diagnosis"]) == 4
    assert len(candidate["root_cause_question_status"]["still_requires_remediation_execution_or_review"]) == 5
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["next_chain"]) == 9
    assert len(candidate["next_gates"]) == 9
    assert len(candidate["risk_controls"]) == 39


def test_checklist_and_summary_pass(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 53
    assert candidate["summary"]["passed_checks"] == 53
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["integration_retry_allowed_now"] is False
    assert candidate["summary"]["integration_results_review_ready"] is False


def test_candidate_digest_is_deterministic(candidate):
    assert candidate["marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"] == service.marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("source_merge_strategy_approval_digest", "0" * 64),
        ("attempted_execution_commit", ""),
        ("integration_branch_head_commit", ""),
        ("first_integration_pytest_passed", True),
        ("later_isolated_rerun_overrides_first_failure", True),
        ("representative_failure_domain", ""),
        ("diagnosed_root_cause", ""),
        ("remediation_candidate_created", False),
        ("remediation_candidate_ready_for_operator_review", False),
        ("recommended_remediation_package", ""),
        ("remediation_packages", []),
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
        ("remote_integration_branch_created", True),
        ("main_merge_performed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
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
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["remediation_requirements", "future_remediation_execution_plan", "risk_controls"],
)
def test_validator_rejects_missing_governance_sections(candidate, field):
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(invalid)


def test_validator_rejects_recommended_package_selected(candidate):
    invalid = deepcopy(candidate)
    invalid["remediation_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(invalid)


def test_validator_rejects_missing_digest(candidate):
    candidate.pop("marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(candidate)


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_markdown_v1(candidate)
    for title in (
        "MarketFlow Repository Integration Branch Validation Failure Remediation Candidate v1",
        "Source Failure Diagnosis", "Failure Summary", "Root Cause", "Candidate Scope",
        "Remediation Philosophy", "Proposed Remediation Packages",
        "Recommended Remediation Package", "Remediation Requirements",
        "Future Remediation Execution Plan", "Remediation Non-Goals",
        "Root-Cause Question Status", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown


def test_writer_round_trips_without_overwrite(tmp_path, candidate):
    receipt = service.write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1.json").read_text(encoding="utf-8"))
    assert payload == candidate
    assert receipt["marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"] == candidate["marketflow_repository_integration_branch_validation_failure_remediation_candidate_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationCandidateError):
        service.write_marketflow_repository_integration_branch_validation_failure_remediation_candidate_v1(tmp_path)
