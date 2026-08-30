from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_service as service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1()


def test_candidate_builds_offline_with_exact_identity(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1
    assert candidate["candidate_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert candidate["candidate_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


def test_source_execution_and_retry_evidence_are_bound(candidate):
    assert candidate["source_method_execution_digest"] == service.SOURCE_METHOD_EXECUTION_DIGEST
    assert candidate["source_method_blocked_manifest_digest"] == service.SOURCE_METHOD_BLOCKED_MANIFEST_DIGEST
    assert candidate["source_method_approval_digest"] == "44e0d7c7ea17f0be0444bc2ad3f4f1974d606f1cb8b1f2d59f0748f462135f02"
    assert candidate["source_method_operator_review_digest"] == "cf541e8681724e1018cf0c343daf718a3a50249e3bdf8640c54d88791427f0be"
    assert candidate["source_method_candidate_digest"] == "414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6"
    assert candidate["source_retry_failure_diagnosis_digest"] == "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
    assert candidate["source_staged_inventory_digest"] == "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
    assert candidate["retry_execution_branch"] == "feature/marketflow-repository-integration-branch-retry-execution-v1"
    assert candidate["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert [candidate[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert candidate["retry_pytest_first_result_authoritative"] is True
    assert candidate["root_full_regression_is_retry_evidence"] is False


def test_blocked_classification_context_is_preserved(candidate):
    assert candidate["classification_source_available"] is False
    assert candidate["classification_blocked_reason"] == "AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE"
    assert candidate["available_retry_data"] == service.source._available_retry_data()
    assert candidate["missing_retry_data"] == service.source.MISSING_RETRY_DATA
    assert candidate["available_retry_data"]["aggregate_counts"] == {
        "passed": 24877,
        "failed": 1292,
        "errors": 112,
        "skipped": 7,
    }


def test_protected_repository_evidence_is_bound(candidate):
    assert candidate["origin_main_commit"] == "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"
    assert candidate["integration_branch_head_commit"] == "220fbc220365fce9cae13ab4853cddff118c0187"
    assert candidate["detached_integration_worktree_head_commit"] == "220fbc220365fce9cae13ab4853cddff118c0187"
    assert candidate["detached_integration_worktree_is_detached"] is True
    assert candidate["detached_integration_worktree_clean"] is True
    assert candidate["staged_evidence_manifest_digest"] == "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"
    assert candidate["staged_evidence_unchanged"] is True
    assert candidate["marketflow_outputs_tracked_in_repository"] is False
    assert candidate["marketflow_outputs_tracked_in_detached_worktree"] is False


def test_candidate_is_ready_but_no_package_is_selected_or_executed(candidate):
    assert candidate["output_capture_candidate_created"] is True
    assert candidate["output_capture_candidate_ready_for_operator_review"] is True
    assert candidate["ready_for_output_capture_candidate_operator_review"] is True
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
    ):
        assert candidate[field] is False


def test_recommended_package_and_all_eight_packages_are_planning_only(candidate):
    packages = candidate["proposed_output_capture_or_classification_source_packages"]
    assert len(packages) == 8
    assert candidate["recommended_output_capture_or_classification_source_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommendation_status"] == service.RECOMMENDATION_STATUS
    recommended = next(row for row in packages if row["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert recommended["selected"] is False
    assert recommended["approved"] is False
    assert recommended["executed"] is False
    blocked = [row for row in packages if row["status"].startswith("BLOCKED_")]
    assert len(blocked) == 4
    assert all(row["selected"] is False and row["approved"] is False and row["executed"] is False for row in packages)


def test_candidate_philosophy_requirements_plan_and_outputs(candidate):
    assert candidate["candidate_philosophy"] == service.CANDIDATE_PHILOSOPHY
    assert candidate["candidate_boundary"] == service.CANDIDATE_BOUNDARY
    assert candidate["candidate_goal"] == service.CANDIDATE_GOAL
    assert candidate["future_output_capture_requirements"] == service.FUTURE_OUTPUT_CAPTURE_REQUIREMENTS
    assert len(candidate["future_output_capture_requirements"]) == 18
    assert all(candidate["future_output_capture_requirements"].values())
    assert candidate["future_output_capture_plan"] == service.FUTURE_OUTPUT_CAPTURE_PLAN
    assert len(candidate["future_output_capture_plan"]) == 10
    assert candidate["future_output_capture_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 9
    assert all(row["status"] == "PLANNED_NOT_GENERATED" for row in candidate["planned_outputs"])


def test_non_goals_next_chain_gates_and_risk_controls_are_exact(candidate):
    assert candidate["non_goals"] == service.NON_GOALS
    assert len(candidate["non_goals"]) == 27
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert len(candidate["next_chain"]) == 10
    assert candidate["next_gates"] == service.NEXT_GATES
    assert len(candidate["next_gates"]) == 10
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 47


def test_all_downstream_authority_remains_closed(candidate):
    for field in (
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
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        assert candidate[field] is False
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    assert all(candidate[field] == service.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_checklist_and_summary_pass(candidate):
    assert len(candidate["checklist"]) == len(service.REQUIRED_CHECK_IDS) == 61
    assert all(row["status"] == service.PASS for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == 61
    assert candidate["summary"]["passed_checks"] == 61
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_candidate_digest_is_deterministic(candidate):
    digest = candidate["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"]
    assert digest == service.marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest_v1(candidate)
    assert service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1() == candidate


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(candidate)
    assert result["candidate_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert result["passed_checks"] == 61
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "wrong"),
        ("candidate_status", "wrong"),
        ("candidate_scope", "wrong"),
        ("source_method_execution_digest", "0" * 64),
        ("source_method_blocked_manifest_digest", "0" * 64),
        ("retry_pytest_failed_count", None),
        ("classification_blocked_reason", None),
        ("root_full_regression_is_retry_evidence", True),
        ("output_capture_candidate_created", False),
        ("output_capture_candidate_ready_for_operator_review", False),
        ("recommended_output_capture_or_classification_source_package", "wrong"),
        ("output_capture_method_selected", True),
        ("output_capture_method_approved", True),
        ("output_capture_method_executed", True),
        ("classification_source_generated", True),
        ("diagnostic_command_executed", True),
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
        ("future_output_capture_requirements", {}),
        ("future_output_capture_plan", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_contract_mutation(candidate, field, value):
    invalid = deepcopy(candidate)
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(invalid)


def test_validator_rejects_missing_package_or_selected_recommended_package(candidate):
    invalid = deepcopy(candidate)
    invalid["proposed_output_capture_or_classification_source_packages"] = invalid[
        "proposed_output_capture_or_classification_source_packages"
    ][1:]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(invalid)
    invalid = deepcopy(candidate)
    invalid["proposed_output_capture_or_classification_source_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(invalid)


def test_validator_rejects_missing_digest(candidate):
    invalid = deepcopy(candidate)
    invalid.pop("marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(invalid)


def test_builder_rejects_changed_source_execution_digest():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
            source_execution={"source_method_execution_digest": "0" * 64}
        )


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_markdown_v1(candidate)
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Candidate v1",
        "## Source Method Execution",
        "## Blocked Classification Context",
        "## Retry Failure Context",
        "## Candidate Scope",
        "## Candidate Philosophy",
        "## Proposed Output Capture or Classification Source Packages",
        "## Recommended Package",
        "## Future Output Capture Requirements",
        "## Future Output Capture Plan",
        "## Planned Outputs",
        "## Non-Goals",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Authority Boundaries",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_json_and_refuses_overwrite(tmp_path, candidate):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == candidate
    assert receipt["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"] == candidate["marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOutputCaptureOrClassificationSourceCandidateError):
        service.write_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_candidate_v1(tmp_path)
