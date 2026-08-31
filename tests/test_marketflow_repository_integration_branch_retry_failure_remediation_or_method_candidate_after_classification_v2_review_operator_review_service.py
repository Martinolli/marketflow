import json
from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_service
    as service,
)


@pytest.fixture(scope="module")
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1()


def test_operator_review_builds_offline_from_committed_candidate_constants(review):
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1,
        ),
        (
            "review_status",
            service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY,
        ),
        (
            "review_scope",
            service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        ),
        ("source_after_v2_candidate_digest", service.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
        ("source_results_review_v2_digest", service.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_review_manifest_digest", service.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST),
        ("source_execution_v2_digest", service.source.source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.SOURCE_MODULE_GROUPING_DIGEST),
        ("source_digest_manifest_digest", service.source.source.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_approval_v2_digest", service.source.source.source.SOURCE_APPROVAL_V2_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("module_level_grouping_reviewed", True),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("remediation_or_method_candidate_after_v2_review_operator_review_created", True),
        ("remediation_or_method_candidate_after_v2_review_operator_review_ready", True),
        ("after_v2_packages_reviewed", True),
        ("future_after_v2_requirements_reviewed", True),
        ("future_after_v2_plan_reviewed", True),
        ("planned_outputs_reviewed", True),
        ("non_goals_reviewed", True),
        ("ready_for_after_v2_remediation_or_method_approval", False),
        ("recommended_package_selected", False),
        ("remediation_or_method_after_v2_selected", False),
        ("remediation_or_method_after_v2_approved", False),
        ("remediation_or_method_after_v2_authorized", False),
        ("remediation_or_method_after_v2_executed", False),
        ("diagnostic_method_after_v2_executed", False),
        ("code_remediation_after_v2_executed", False),
        ("evidence_remediation_after_v2_executed", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("main_merge_approval_created", False),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("diagnostic_output_captured", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("pytest_cache_committed", False),
        ("evidence_regenerated", False),
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
    ],
)
def test_required_bindings_review_facts_and_boundaries(review, field, expected):
    assert review[field] == expected


def test_retry_failure_counts_are_bound(review):
    assert [review[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [
        24877,
        1292,
        112,
        7,
    ]
    assert review["retry_pytest_first_result_authoritative"] is True
    assert review["root_full_regression_is_retry_evidence"] is False


def test_classification_evidence_and_unsupported_claims_are_bound(review):
    assert review["failed_or_errored_nodeids_count"] == 1404
    assert review["unsupported_claims_boundary"] == service._unsupported_claims_boundary()
    assert all(value is False for value in review["unsupported_claims_boundary"].values())


def test_candidate_philosophy_is_reviewed_planning_only(review):
    assert review["reviewed_candidate_after_v2_philosophy"] == service.REVIEWED_CANDIDATE_PHILOSOPHY
    assert review["reviewed_candidate_after_v2_boundary"] == service.REVIEWED_CANDIDATE_BOUNDARY
    assert review["reviewed_candidate_after_v2_goal"] == service.REVIEWED_CANDIDATE_GOAL
    assert review["candidate_philosophy_review_status"] == "REVIEWED_PLANNING_ONLY"


def test_nine_packages_and_three_blocked_packages_are_reviewed(review):
    assert review["reviewed_packages"] == service.REVIEWED_PACKAGES
    assert len(review["reviewed_packages"]) == 9
    assert sum(row["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for row in review["reviewed_packages"]) == 3
    assert all(row["selected"] is False for row in review["reviewed_packages"])
    assert all(row["approved"] is False for row in review["reviewed_packages"])
    assert all(row["executed"] is False for row in review["reviewed_packages"])


def test_recommended_package_reviewed_but_not_selected(review):
    package = next(
        row for row in review["reviewed_packages"] if row["package_id"] == service.source.RECOMMENDED_PACKAGE
    )
    assert package["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["selected"] is False


def test_future_requirements_plan_outputs_and_non_goals_reviewed(review):
    assert review["reviewed_future_requirements"] == service.REVIEWED_FUTURE_REQUIREMENTS
    assert len(review["reviewed_future_requirements"]) == 12
    assert review["reviewed_future_plan"] == service.REVIEWED_FUTURE_PLAN
    assert len(review["reviewed_future_plan"]) == 7
    assert review["reviewed_planned_outputs"] == service.REVIEWED_PLANNED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 11
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == 25


def test_recommendation_requires_optional_selection_and_future_approval(review):
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert review["recommendation_reason"] == service.RECOMMENDATION_REASON
    assert review["ready_for_after_v2_remediation_or_method_approval"] is False


def test_next_chain_gates_and_risk_controls_are_complete(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 8
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 8
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 49


def test_checklist_passes_and_has_required_shape(review):
    assert [row["check_id"] for row in review["checklist"]] == service.CHECK_IDS
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in review["checklist"]
    )
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert review["summary"]["total_checks"] == 62
    assert review["summary"]["passed_checks"] == 62
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_operator_review_digest_is_deterministic(review):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1()
    assert rebuilt == review
    assert review[
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest"
    ] == service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest_v1(
        review
    )


def test_validator_accepts_valid_operator_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        review
    )
    assert result["total_checks"] == 62
    assert result["failed_checks"] == 0


_DELETE = object()


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_after_v2_candidate_digest", "0" * 64),
        ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_pytest_failed_count", _DELETE),
        ("module_level_grouping_reviewed", _DELETE),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136, 131, 122, 112]),
        ("unsupported_claims_boundary", _DELETE),
        ("remediation_or_method_candidate_after_v2_review_operator_review_created", False),
        ("remediation_or_method_candidate_after_v2_review_operator_review_ready", False),
        ("reviewed_packages", _DELETE),
        ("ready_for_after_v2_remediation_or_method_approval", True),
        ("recommended_package_selected", True),
        ("remediation_or_method_after_v2_approved", True),
        ("remediation_or_method_after_v2_executed", True),
        ("diagnostic_method_after_v2_executed", True),
        ("code_remediation_after_v2_executed", True),
        ("evidence_remediation_after_v2_executed", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True),
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
        ("risk_controls", _DELETE),
        (
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_digest",
            _DELETE,
        ),
    ],
)
def test_validator_rejects_changed_missing_or_authorizing_values(review, field, value):
    changed = deepcopy(review)
    if value is _DELETE:
        changed.pop(field, None)
    else:
        changed[field] = value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
            changed
        )


def test_validator_rejects_recommended_package_selected(review):
    changed = deepcopy(review)
    package = next(
        row for row in changed["reviewed_packages"] if row["package_id"] == service.source.RECOMMENDED_PACKAGE
    )
    package["selected"] = True
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
            changed
        )


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_markdown_v1(
        review
    )
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Classification v2 Review Operator Review v1",
        "Source After-v2 Candidate",
        "Source Results Review v2",
        "Retry Failure Context",
        "Classification Evidence Summary",
        "Review Scope",
        "Reviewed Candidate Philosophy",
        "Reviewed Packages",
        "Reviewed Future Requirements",
        "Reviewed Future Plan",
        "Reviewed Planned Outputs",
        "Reviewed Non-Goals",
        "Recommendation",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path, review):
    result = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
        tmp_path
    )
    path = tmp_path / (
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_"
        "classification_v2_review_operator_review_v1.json"
    )
    assert result["path"] == str(path)
    assert json.loads(path.read_text(encoding="utf-8")) == review
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewOperatorReviewError
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1(
            tmp_path
        )


def test_public_service_exports_are_available():
    for name in (
        "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1",
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_READY",
        "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1",
        "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1",
        "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_v1",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_operator_review_markdown_v1",
    ):
        assert getattr(services, name) is getattr(service, name)
