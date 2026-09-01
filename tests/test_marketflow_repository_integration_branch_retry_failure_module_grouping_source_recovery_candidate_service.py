from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_service
    as service,
)


_DELETE = object()


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1()


def test_candidate_builds_offline(candidate):
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN),
        ("source_blocked_after_v2_execution_digest", service.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", service.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_after_v2_approval_digest", service.source.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_after_v2_operator_review_digest", service.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_after_v2_candidate_digest", service.source.approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
        ("source_results_review_v2_digest", service.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("known_available_detail", service.KNOWN_AVAILABLE_DETAIL),
        ("known_missing_detail", service.KNOWN_MISSING_DETAIL),
        ("unsupported_claims_boundary", service.UNSUPPORTED_CLAIMS_BOUNDARY),
        ("module_grouping_source_recovery_candidate_created", True),
        ("module_grouping_source_recovery_candidate_ready_for_operator_review", True),
        ("ready_for_module_grouping_source_recovery_operator_review", True),
        ("recommended_module_grouping_source_recovery_package", service.RECOMMENDED_PACKAGE),
        ("module_grouping_source_recovery_selected", False),
        ("module_grouping_source_recovery_approved", False),
        ("module_grouping_source_recovery_authorized", False),
        ("module_grouping_source_recovery_executed", False),
        ("module_grouping_detail_recovered", False),
        ("module_grouping_detail_exposed", False),
        ("module_paths_recovered", False),
        ("per_module_counts_recovered", False),
        ("bounded_nodeid_samples_recovered", False),
        ("remediation_or_method_after_v2_reentry_created", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("main_merge_approval_created", False),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("diagnostic_output_captured", False),
        ("cache_read", False),
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
def test_required_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_retry_counts_and_classification_summary(candidate):
    assert [candidate[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert candidate["classification_evidence_summary"] == service._classification_summary()


def test_ten_packages_and_five_blocked(candidate):
    packages = candidate["proposed_packages"]
    assert len(packages) == 10
    assert len([package for package in packages if package["status"].startswith("BLOCKED_")]) == 5
    assert all(package["selected"] is False for package in packages)
    assert all(package["approved"] is False for package in packages)
    assert all(package["executed"] is False for package in packages)


def test_recommended_package_is_read_only_and_unselected(candidate):
    package = next(package for package in candidate["proposed_packages"] if package["package_id"] == service.RECOMMENDED_PACKAGE)
    assert package["status"] == service.RECOMMENDATION_STATUS
    assert package["selected"] is False
    assert "read-only" in candidate["recommendation_reason"]
    assert "without rerunning pytest" in candidate["recommendation_reason"]


def test_future_material_is_defined_but_not_executed(candidate):
    assert len(candidate["future_source_recovery_requirements"]) == 23
    assert all(candidate["future_source_recovery_requirements"].values())
    assert len(candidate["future_source_recovery_plan"]) == 10
    assert all(step["status"] == "PLANNED_NOT_EXECUTED" for step in candidate["future_source_recovery_plan"])
    assert len(candidate["planned_outputs"]) == 10
    assert all(output["status"] == "PLANNED_NOT_GENERATED" for output in candidate["planned_outputs"])
    assert candidate["non_goals"] == service.NON_GOALS


def test_next_chain_gates_and_risk_controls(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["next_chain"]) == 13
    assert len(candidate["next_gates"]) == 15
    assert len(candidate["risk_controls"]) == 58


def test_checklist_passes(candidate):
    assert candidate["summary"]["passed_checks"] == candidate["summary"]["total_checks"] == 67
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert all(check["status"] == "PASS" for check in candidate["checklist"])


def test_candidate_digest_is_deterministic(candidate):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1()
    assert rebuilt == candidate
    assert candidate["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest"] == "4c0542256406f1db4d86f32958d738f6c86dc83ea2dd2132e2d54bcf5afb8bcb"


def test_builder_accepts_exact_blocked_source(candidate):
    blocked = service.source.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(run_timestamp_utc="2026-08-23T00:00:00Z")
    assert service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(source_blocked_execution=blocked) == candidate


def test_validator_accepts_candidate(candidate):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(candidate)["failed_checks"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_blocked_after_v2_manifest_digest", "0" * 64),
        ("blocked_reason", _DELETE),
        ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_pytest_failed_count", _DELETE),
        ("classification_evidence_summary", _DELETE),
        ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136]),
        ("known_missing_detail", _DELETE),
        ("unsupported_claims_boundary", _DELETE),
        ("module_grouping_source_recovery_candidate_created", False),
        ("module_grouping_source_recovery_candidate_ready_for_operator_review", False),
        ("recommended_module_grouping_source_recovery_package", _DELETE),
        ("proposed_packages", _DELETE),
        ("module_grouping_source_recovery_selected", True),
        ("module_grouping_source_recovery_approved", True),
        ("module_grouping_source_recovery_executed", True),
        ("module_grouping_detail_recovered", True),
        ("module_grouping_detail_exposed", True),
        ("module_paths_recovered", True),
        ("per_module_counts_recovered", True),
        ("bounded_nodeid_samples_recovered", True),
        ("remediation_or_method_after_v2_reentry_created", True),
        ("new_retry_candidate_created", True),
        ("new_retry_executed", True),
        ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True),
        ("retry_rerun_performed", True),
        ("full_pytest_performed", True),
        ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True),
        ("cache_read", True),
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
        ("future_source_recovery_requirements", _DELETE),
        ("future_source_recovery_plan", _DELETE),
        ("risk_controls", _DELETE),
        ("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_digest", _DELETE),
    ],
)
def test_validator_rejects_invalid_candidate(candidate, field, value):
    changed = deepcopy(candidate)
    if value is _DELETE:
        changed.pop(field, None)
    else:
        changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(changed)


def test_validator_rejects_recommended_package_selected(candidate):
    changed = deepcopy(candidate)
    next(package for package in changed["proposed_packages"] if package["package_id"] == service.RECOMMENDED_PACKAGE)["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(changed)


def test_writer_round_trips_candidate(tmp_path, candidate):
    result = service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1(tmp_path)
    assert json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1.json").read_text(encoding="utf-8")) == candidate
    assert result["candidate"] == candidate


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_markdown_v1(candidate)
    for heading in (
        "Source Blocked After-v2 Execution",
        "Source Classification Results Review v2",
        "Retry Failure Context",
        "Known Available and Missing Detail",
        "Candidate Scope",
        "Candidate Philosophy",
        "Proposed Module Grouping Source Recovery Packages",
        "Recommended Package",
        "Future Source Recovery Requirements",
        "Future Source Recovery Plan",
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


def test_exports_are_available():
    assert services.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1 is service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_v1
    assert services.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1 == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1
