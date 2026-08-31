import json
from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_service
    as service,
)


@pytest.fixture(scope="module")
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1()


def test_candidate_builds_offline_from_committed_review_constants(candidate):
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1,
        ),
        (
            "candidate_status",
            service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW,
        ),
        (
            "candidate_scope",
            service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        ),
        ("source_classification_method_results_review_v2_digest", service.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        (
            "source_classification_method_results_review_v2_manifest_digest",
            service.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        ),
        ("source_classification_method_execution_v2_digest", service.source.SOURCE_EXECUTION_V2_DIGEST),
        (
            "source_classification_method_v2_module_grouping_digest",
            service.source.SOURCE_MODULE_GROUPING_DIGEST,
        ),
        (
            "source_classification_method_v2_digest_manifest_digest",
            service.source.SOURCE_DIGEST_MANIFEST_DIGEST,
        ),
        ("source_classification_method_approval_v2_digest", service.source.source.SOURCE_APPROVAL_V2_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("module_level_grouping_reviewed", True),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("remediation_or_method_candidate_after_v2_review_created", True),
        ("remediation_or_method_candidate_after_v2_review_ready_for_operator_review", True),
        ("ready_for_remediation_or_method_candidate_after_v2_review_operator_review", True),
        ("recommended_remediation_or_method_after_v2_package", service.RECOMMENDED_PACKAGE),
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
def test_required_identity_bindings_and_boundaries(candidate, field, expected):
    assert candidate[field] == expected


def test_retry_failure_counts_are_bound(candidate):
    assert [candidate[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [
        24877,
        1292,
        112,
        7,
    ]
    assert candidate["retry_pytest_first_result_authoritative"] is True
    assert candidate["root_full_regression_is_retry_evidence"] is False


def test_classification_evidence_and_unsupported_claims_are_bound(candidate):
    assert candidate["classification_evidence_summary"] == service._classification_evidence_summary()
    assert candidate["unsupported_claims_boundary"] == service._unsupported_claims_boundary()
    assert all(value is False for value in candidate["unsupported_claims_boundary"].values())


def test_nine_packages_include_three_blocked_packages(candidate):
    packages = candidate["proposed_packages"]
    assert packages == service.PROPOSED_PACKAGES
    assert len(packages) == 9
    assert sum(row["status"] == "BLOCKED_NOT_ALLOWED" for row in packages) == 3
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_recommended_package_is_present_but_not_selected(candidate):
    package = next(
        row for row in candidate["proposed_packages"] if row["package_id"] == service.RECOMMENDED_PACKAGE
    )
    assert package["status"] == service.RECOMMENDATION_STATUS
    assert package["selected"] is False
    assert candidate["recommendation_reason"] == service.RECOMMENDATION_REASON


def test_candidate_philosophy_scope_and_goal_are_exact(candidate):
    assert candidate["candidate_after_v2_philosophy"] == service.CANDIDATE_AFTER_V2_PHILOSOPHY
    assert candidate["candidate_after_v2_boundary"] == service.CANDIDATE_AFTER_V2_BOUNDARY
    assert candidate["candidate_after_v2_goal"] == service.CANDIDATE_AFTER_V2_GOAL


def test_future_requirements_and_plan_are_defined_not_executed(candidate):
    assert candidate["future_requirements"] == service.FUTURE_REQUIREMENTS
    assert len(candidate["future_requirements"]) == 12
    assert all(candidate["future_requirements"].values())
    assert candidate["future_plan"] == {
        "status": "PLANNED_NOT_EXECUTED",
        "steps": service.FUTURE_PLAN_STEPS,
    }
    assert len(candidate["future_plan"]["steps"]) == 7


def test_planned_outputs_are_not_generated(candidate):
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 11
    assert set(candidate["planned_outputs"].values()) == {"PLANNED_NOT_GENERATED"}


def test_non_goals_next_chain_gates_and_risks_are_defined(candidate):
    assert candidate["non_goals"] == service.NON_GOALS
    assert len(candidate["non_goals"]) == 25
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert len(candidate["next_chain"]) == 9
    assert candidate["next_gates"] == service.NEXT_GATES
    assert len(candidate["next_gates"]) == 9
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 48


def test_checklist_passes_and_has_required_shape(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.CHECK_IDS
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in candidate["checklist"]
    )
    assert all(row["status"] == "PASS" for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == 60
    assert candidate["summary"]["passed_checks"] == 60
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1()
    assert rebuilt == candidate
    assert candidate[
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest"
    ] == service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest_v1(
        candidate
    )


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        candidate
    )
    assert result["total_checks"] == 60
    assert result["failed_checks"] == 0


_DELETE = object()


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_classification_method_results_review_v2_digest", "0" * 64),
        ("source_classification_method_results_review_v2_manifest_digest", "0" * 64),
        ("source_classification_method_execution_v2_digest", "0" * 64),
        ("source_classification_method_v2_module_grouping_digest", "0" * 64),
        ("retry_pytest_failed_count", _DELETE),
        ("classification_evidence_summary", _DELETE),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136, 131, 122, 112]),
        ("unsupported_claims_boundary", _DELETE),
        ("remediation_or_method_candidate_after_v2_review_created", False),
        ("remediation_or_method_candidate_after_v2_review_ready_for_operator_review", False),
        ("recommended_remediation_or_method_after_v2_package", _DELETE),
        ("proposed_packages", []),
        ("remediation_or_method_after_v2_selected", True),
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
        ("future_requirements", _DELETE),
        ("future_plan", _DELETE),
        ("risk_controls", _DELETE),
        (
            "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_digest",
            _DELETE,
        ),
    ],
)
def test_validator_rejects_changed_missing_or_authorizing_values(candidate, field, value):
    changed = deepcopy(candidate)
    if value is _DELETE:
        changed.pop(field, None)
    else:
        changed[field] = value
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
            changed
        )


def test_validator_rejects_recommended_package_selected(candidate):
    changed = deepcopy(candidate)
    package = next(
        row for row in changed["proposed_packages"] if row["package_id"] == service.RECOMMENDED_PACKAGE
    )
    package["selected"] = True
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
            changed
        )


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_markdown_v1(
        candidate
    )
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Classification v2 Review v1",
        "Source Results Review v2",
        "Retry Failure Context",
        "Classification Evidence Summary",
        "Candidate Scope",
        "Candidate Philosophy",
        "Proposed Packages",
        "Recommended Package",
        "Future Requirements",
        "Future Plan",
        "Planned Outputs",
        "Non-Goals",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path, candidate):
    result = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
        tmp_path
    )
    path = tmp_path / (
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_"
        "after_classification_v2_review_v1.json"
    )
    assert result["path"] == str(path)
    assert json.loads(path.read_text(encoding="utf-8")) == candidate
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterClassificationV2ReviewError
    ):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1(
            tmp_path
        )


def test_public_service_exports_are_available():
    for name in (
        "ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_V1",
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_READY_FOR_OPERATOR_REVIEW",
        "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1",
        "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1",
        "write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_v1",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_classification_v2_review_markdown_v1",
    ):
        assert getattr(services, name) is getattr(service, name)
