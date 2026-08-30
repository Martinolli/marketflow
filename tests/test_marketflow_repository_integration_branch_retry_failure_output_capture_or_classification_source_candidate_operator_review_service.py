from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_service as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1()


def test_review_builds_offline_with_exact_identity(review):
    assert review["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_V1
    assert review["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY
    assert review["review_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_source_candidate_and_method_evidence_are_bound(review):
    assert review["source_output_capture_candidate_digest"] == service.SOURCE_OUTPUT_CAPTURE_CANDIDATE_DIGEST
    assert review["source_method_execution_digest"] == "522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562"
    assert review["source_method_blocked_manifest_digest"] == "3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f"
    assert review["source_method_approval_digest"] == "44e0d7c7ea17f0be0444bc2ad3f4f1974d606f1cb8b1f2d59f0748f462135f02"
    assert review["source_method_operator_review_digest"] == "cf541e8681724e1018cf0c343daf718a3a50249e3bdf8640c54d88791427f0be"
    assert review["source_method_candidate_digest"] == "414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6"
    assert review["source_retry_failure_diagnosis_digest"] == "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
    assert review["source_staged_inventory_digest"] == "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"


def test_retry_and_blocked_classification_context_are_preserved(review):
    assert review["retry_execution_branch"] == "feature/marketflow-repository-integration-branch-retry-execution-v1"
    assert review["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert [review[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert review["retry_pytest_first_result_authoritative"] is True
    assert review["classification_source_available"] is False
    assert review["classification_blocked_reason"] == "AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE"
    assert review["available_retry_data"] == service.source.source._available_retry_data()
    assert review["missing_retry_data"] == service.source.source.MISSING_RETRY_DATA
    assert review["root_full_regression_is_retry_evidence"] is False


def test_protected_state_is_bound(review):
    assert review["origin_main_commit"] == "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
    assert review["integration_branch_head_commit"] == "220fbc220365fce9cae13ab4853cddff118c0187"
    assert review["detached_integration_worktree_head_commit"] == "220fbc220365fce9cae13ab4853cddff118c0187"
    assert review["detached_integration_worktree_is_detached"] is True
    assert review["detached_integration_worktree_clean"] is True
    assert review["staged_evidence_manifest_digest"] == "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
    assert review["staged_evidence_unchanged"] is True
    assert review["marketflow_outputs_tracked_in_repository"] is False
    assert review["marketflow_outputs_tracked_in_detached_worktree"] is False


def test_review_flags_are_ready_but_approval_is_not(review):
    for field in (
        "output_capture_candidate_operator_review_created",
        "output_capture_candidate_operator_review_ready",
        "output_capture_packages_reviewed",
        "future_output_capture_requirements_reviewed",
        "future_output_capture_plan_reviewed",
        "planned_outputs_reviewed",
        "non_goals_reviewed",
    ):
        assert review[field] is True
    assert review["ready_for_output_capture_approval"] is False


def test_candidate_philosophy_is_reviewed_planning_only(review):
    assert review["reviewed_candidate_philosophy"] == service.source.CANDIDATE_PHILOSOPHY
    assert review["reviewed_candidate_boundary"].startswith("Candidate-only reviewed")
    assert review["reviewed_candidate_goal"] == service.source.CANDIDATE_GOAL
    assert review["review_disposition"] == "REVIEWED_PLANNING_ONLY"


def test_all_eight_packages_are_reviewed_without_selection(review):
    packages = review["reviewed_output_capture_or_classification_source_packages"]
    assert packages == service.REVIEWED_PACKAGES
    assert len(packages) == 8
    recommended = next(row for row in packages if row["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert recommended["selected"] is False
    assert recommended["approved"] is False
    assert recommended["executed"] is False
    assert len([row for row in packages if row["source_status"].startswith("BLOCKED_")]) == 4
    assert all(row["selected"] is False and row["approved"] is False and row["executed"] is False for row in packages)


def test_requirements_plan_outputs_and_non_goals_are_reviewed_not_executed(review):
    assert review["reviewed_future_output_capture_requirements"] == service.REVIEWED_FUTURE_OUTPUT_CAPTURE_REQUIREMENTS
    assert len(review["reviewed_future_output_capture_requirements"]) == 18
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_OUTPUT_CAPTURE" and row["execution_status"] == "NOT_EXECUTED" for row in review["reviewed_future_output_capture_requirements"])
    assert review["reviewed_future_output_capture_plan"] == service.REVIEWED_FUTURE_OUTPUT_CAPTURE_PLAN
    assert len(review["reviewed_future_output_capture_plan"]) == 10
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in review["reviewed_future_output_capture_plan"])
    assert review["reviewed_planned_outputs"] == service.REVIEWED_PLANNED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 9
    assert all(row["generation_status"] == "NOT_GENERATED" for row in review["reviewed_planned_outputs"])
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == 27
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_non_goals"])


def test_recommendation_next_chain_gates_and_controls(review):
    assert review["recommended_output_capture_or_classification_source_package"] == service.RECOMMENDED_PACKAGE
    assert review["recommended_package_selected"] is False
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 9
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 9
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 49


def test_no_package_or_downstream_authority_is_created(review):
    for field in (
        "output_capture_method_selected",
        "output_capture_method_approved",
        "output_capture_method_authorized",
        "output_capture_method_executed",
        "classification_source_capture_executed",
        "classification_source_generated",
        "classification_source_review_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "new_classification_method_candidate_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "evidence_regenerated",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        assert review[field] is False
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    assert all(review[field] == service.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_checklist_and_summary_pass(review):
    assert len(review["checklist"]) == len(service.REQUIRED_CHECK_IDS) == 64
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == 64
    assert review["summary"]["passed_checks"] == 64
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(review):
    digest = review["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"]
    assert digest == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest_v1(review)
    assert service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1() == review


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(review)
    assert result["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_OPERATOR_REVIEW_READY
    assert result["passed_checks"] == 64
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "wrong"),
        ("review_status", "wrong"),
        ("review_scope", "wrong"),
        ("source_output_capture_candidate_digest", "0" * 64),
        ("source_method_execution_digest", "0" * 64),
        ("source_method_blocked_manifest_digest", "0" * 64),
        ("retry_pytest_failed_count", None),
        ("classification_blocked_reason", None),
        ("root_full_regression_is_retry_evidence", True),
        ("output_capture_candidate_operator_review_created", False),
        ("output_capture_candidate_operator_review_ready", False),
        ("output_capture_packages_reviewed", False),
        ("future_output_capture_requirements_reviewed", False),
        ("future_output_capture_plan_reviewed", False),
        ("planned_outputs_reviewed", False),
        ("non_goals_reviewed", False),
        ("ready_for_output_capture_approval", True),
        ("recommended_package_selected", True),
        ("output_capture_method_selected", True),
        ("output_capture_method_approved", True),
        ("output_capture_method_executed", True),
        ("classification_source_generated", True),
        ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
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
def test_validator_rejects_contract_mutation(review, field, value):
    invalid = deepcopy(review)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(invalid)


def test_validator_rejects_missing_package_review_or_selected_recommended_package(review):
    invalid = deepcopy(review)
    invalid["reviewed_output_capture_or_classification_source_packages"] = invalid[
        "reviewed_output_capture_or_classification_source_packages"
    ][1:]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(invalid)
    invalid = deepcopy(review)
    invalid["reviewed_output_capture_or_classification_source_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(invalid)


def test_validator_rejects_missing_digest(review):
    invalid = deepcopy(review)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(invalid)


def test_builder_rejects_changed_source_candidate_digest():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
            source_candidate={"source_output_capture_candidate_digest": "0" * 64}
        )


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_markdown_v1(review)
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Candidate Operator Review v1",
        "## Source Output Capture Candidate",
        "## Source Method Execution",
        "## Blocked Classification Context",
        "## Retry Failure Context",
        "## Review Scope",
        "## Reviewed Candidate Philosophy",
        "## Reviewed Output Capture or Classification Source Packages",
        "## Reviewed Future Output Capture Requirements",
        "## Reviewed Future Output Capture Plan",
        "## Reviewed Planned Outputs",
        "## Reviewed Non-Goals",
        "## Recommendation",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Authority Boundaries",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_json_and_refuses_overwrite(tmp_path, review):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == review
    assert receipt["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"] == review["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_operator_review_v1(tmp_path)
