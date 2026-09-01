from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_service
    as service,
)


_DELETE = object()


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1()


def test_review_builds_offline_with_public_exports(review):
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True
    assert services.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1() == review


@pytest.mark.parametrize(
    "field,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN),
        ("source_module_grouping_source_recovery_candidate_digest", service.SOURCE_CANDIDATE_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", service.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_after_v2_approval_digest", service.source.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_after_v2_operator_review_digest", service.source.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_after_v2_candidate_digest", service.source.source.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
        ("source_results_review_v2_digest", service.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("known_missing_detail", service.source.KNOWN_MISSING_DETAIL),
        ("unsupported_claims_boundary", service.source.UNSUPPORTED_CLAIMS_BOUNDARY),
        ("module_grouping_source_recovery_candidate_operator_review_created", True),
        ("module_grouping_source_recovery_candidate_operator_review_ready", True),
        ("ready_for_module_grouping_source_recovery_operator_review", True),
        ("source_recovery_packages_reviewed", True),
        ("future_source_recovery_requirements_reviewed", True),
        ("future_source_recovery_plan_reviewed", True),
        ("planned_outputs_reviewed", True),
        ("non_goals_reviewed", True),
        ("ready_for_module_grouping_source_recovery_approval", False),
        ("recommended_module_grouping_source_recovery_package", service.source.RECOMMENDED_PACKAGE),
        ("recommended_package_selected", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_bindings(review, field, expected):
    assert review[field] == expected


def test_retry_counts_and_classification_summary_are_bound(review):
    assert [review[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert review["classification_evidence_summary"] == service.source._classification_summary()


def test_packages_are_all_reviewed_and_none_selected(review):
    packages = review["reviewed_packages"]
    assert len(packages) == 10
    assert len([package for package in packages if "BLOCKED" in package["review_status"]]) == 5
    assert all(package["review_status"].startswith("REVIEWED_") for package in packages)
    assert all(package["selected"] is False for package in packages)
    assert all(package["approved"] is False for package in packages)
    assert all(package["executed"] is False for package in packages)
    recommended = next(package for package in packages if package["package_id"] == service.source.RECOMMENDED_PACKAGE)
    assert recommended["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"


def test_future_material_and_non_goals_are_reviewed_only(review):
    assert len(review["reviewed_future_source_recovery_requirements"]) == 23
    assert all(item["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_SOURCE_RECOVERY" and item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_source_recovery_requirements"])
    assert len(review["reviewed_future_source_recovery_plan"]) == 10
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" and item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_source_recovery_plan"])
    assert len(review["reviewed_planned_outputs"]) == 10
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" and item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert len(review["reviewed_non_goals"]) == 33
    assert all(item["review_status"] == "REVIEWED_ACTIVE" for item in review["reviewed_non_goals"])


def test_all_execution_and_authority_boundaries_remain_closed(review):
    false_fields = [
        "module_grouping_source_recovery_selected", "module_grouping_source_recovery_approved",
        "module_grouping_source_recovery_authorized", "module_grouping_source_recovery_executed",
        "module_grouping_detail_recovered", "module_grouping_detail_exposed", "module_paths_recovered",
        "per_module_counts_recovered", "bounded_nodeid_samples_recovered",
        "remediation_or_method_after_v2_reentry_created", "new_retry_candidate_created", "new_retry_executed",
        "new_retry_results_review_created", "main_merge_approval_created", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed", "diagnostic_output_captured", "cache_read",
        "integration_execution_successful", "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated", "integration_branch_pushed", "main_push_performed",
        "origin_main_modified_by_this_task", "marketflow_outputs_committed", "pytest_cache_committed",
        "evidence_regenerated", "provider_requests_made_in_review", "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    ]
    assert all(review[field] is False for field in false_fields)
    assert review["strategy_use"] == review["paper_trading"] == review["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_gates_controls_and_checklist_pass(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["next_chain"]) == 12
    assert len(review["next_gates"]) == 14
    assert len(review["risk_controls"]) == 59
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"] == 71
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" for item in review["checklist"])


def test_digest_is_deterministic_and_source_candidate_can_be_supplied(review):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1()
    source_candidate = service.source.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1()
    supplied = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(source_candidate=source_candidate)
    assert rebuilt == supplied == review
    assert review["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_digest"] == "f124b1bf3af19dbe722815d232f7e827af2373ceb449279d5ac80b4533f9b00e"


def test_validator_accepts_review_and_writer_round_trips(review, tmp_path):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(review)["failed_checks"] == 0
    result = service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(tmp_path)
    assert json.loads(result["path"] and (tmp_path / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1.json").read_text(encoding="utf-8")) == review


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_module_grouping_source_recovery_candidate_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64), ("source_blocked_after_v2_manifest_digest", "0" * 64),
        ("blocked_reason", _DELETE), ("source_results_review_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_pytest_failed_count", _DELETE),
        ("module_summary_module_count", 28), ("known_missing_detail", _DELETE),
        ("unsupported_claims_boundary", _DELETE), ("module_grouping_source_recovery_candidate_operator_review_ready", False),
        ("reviewed_packages", []), ("ready_for_module_grouping_source_recovery_approval", True),
        ("recommended_package_selected", True), ("module_grouping_source_recovery_selected", True),
        ("module_grouping_source_recovery_approved", True), ("module_grouping_source_recovery_executed", True),
        ("module_grouping_detail_recovered", True), ("module_grouping_detail_exposed", True),
        ("module_paths_recovered", True), ("new_retry_candidate_created", True), ("retry_rerun_performed", True),
        ("full_pytest_performed", True), ("diagnostic_command_executed", True), ("cache_read", True),
        ("integration_execution_successful", True), ("main_push_performed", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_review", True), ("predictive_usefulness", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("risk_controls", []),
    ],
)
def test_validator_rejects_boundary_or_binding_changes(review, field, value):
    changed = deepcopy(review)
    if value is _DELETE:
        changed.pop(field)
    else:
        changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(changed)


def test_validator_rejects_changed_source_candidate_input():
    candidate = service.source.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1()
    candidate["recommended_package_selected"] = True
    with pytest.raises(ValueError):
        service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1(source_candidate=candidate)


def test_markdown_includes_every_required_section(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_markdown_v1(review)
    sections = [
        "Source Module Grouping Source Recovery Candidate", "Source Blocked After-v2 Execution",
        "Source Classification Results Review v2", "Retry Failure Context", "Known Available and Missing Detail",
        "Review Scope", "Reviewed Candidate Philosophy", "Reviewed Module Grouping Source Recovery Packages",
        "Reviewed Future Source Recovery Requirements", "Reviewed Future Source Recovery Plan", "Reviewed Planned Outputs",
        "Reviewed Non-Goals", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)
