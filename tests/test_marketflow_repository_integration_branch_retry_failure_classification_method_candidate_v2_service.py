from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_service as service,
)


@pytest.fixture
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2()


def test_candidate_builds_offline_without_cache_read(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("source builder or cache read must not be called")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1",
        forbidden,
    )
    monkeypatch.setattr(service.source.source, "_fixture_or_live_snapshot", forbidden)
    built = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2()
    assert built["created_offline"] is True
    assert built["classification_method_candidate_v2_ready_for_operator_review"] is True


def test_candidate_accepts_valid_injected_reentry():
    reentry = service.source.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1()
    built = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(
        source_reentry=reentry
    )
    assert built["source_classification_method_reentry_digest"] == service.SOURCE_REENTRY_DIGEST
    assert built["marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"] == service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2()["marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"]


def test_artifact_status_and_scope(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2
    assert candidate["candidate_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_READY_FOR_OPERATOR_REVIEW
    assert candidate["candidate_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        ("source_classification_method_reentry_digest", service.SOURCE_REENTRY_DIGEST),
        ("source_classification_source_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_cache_manifest_review_digest", service.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST),
        ("source_output_capture_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_classification_source_manifest_digest", service.SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST),
        ("source_retry_failure_diagnosis_digest", service.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_staged_inventory_digest", service.SOURCE_STAGED_INVENTORY_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("lastfailed_cache_entry_count", 1404),
        ("nodeids_cache_entry_count", 26288),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("retry_pytest_first_result_authoritative", True),
        ("root_full_regression_is_retry_evidence", False),
    ],
)
def test_candidate_binds_source_retry_cache_and_module_facts(candidate, field, expected):
    assert candidate[field] == expected


def test_candidate_preserves_cache_supported_capabilities_and_limits(candidate):
    assert candidate["classification_source_valid_for_v2_candidate"] is True
    assert candidate["classification_source_type"] == "DETACHED_PYTEST_CACHE_LASTFAILED"
    assert candidate["classification_source_accepted_for_module_level_only"] is True
    assert candidate["classification_source_not_accepted_for_failure_error_separation"] is True
    assert candidate["classification_source_not_accepted_for_first_order_failure_analysis"] is True
    assert candidate["classification_source_not_accepted_for_traceback_root_cause"] is True
    assert candidate["classification_source_not_retry_success_evidence"] is True
    assert candidate["classification_source_limitations"] == service.CLASSIFICATION_SOURCE_LIMITATIONS


def test_candidate_philosophy_goal_and_boundary(candidate):
    assert candidate["candidate_v2_philosophy"] == service.CANDIDATE_V2_PHILOSOPHY
    assert candidate["candidate_v2_boundary"] == service.CANDIDATE_V2_BOUNDARY
    assert candidate["candidate_v2_goal"] == service.CANDIDATE_V2_GOAL


def test_nine_packages_and_four_blocked_packages_are_present(candidate):
    packages = candidate["proposed_classification_method_v2_packages"]
    assert packages == service.PROPOSED_V2_PACKAGES
    assert len(packages) == 9
    assert sum(row["status"] == "BLOCKED_NOT_ALLOWED" for row in packages) == 4
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_recommended_package_is_present_but_not_selected(candidate):
    package = next(row for row in candidate["proposed_classification_method_v2_packages"] if row["package_id"] == service.RECOMMENDED_PACKAGE)
    assert candidate["recommended_classification_method_v2_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert candidate["recommendation_reason"] == service.RECOMMENDATION_REASON
    assert package["status"] == candidate["recommendation_status"]
    assert package["selected"] is False
    assert package["approved"] is False
    assert package["executed"] is False


@pytest.mark.parametrize(
    "field,expected",
    [
        ("classification_method_candidate_v2_created", True),
        ("classification_method_candidate_v2_ready_for_operator_review", True),
        ("ready_for_classification_method_candidate_v2_operator_review", True),
        ("classification_method_v2_selected", False),
        ("classification_method_v2_approved", False),
        ("classification_method_v2_authorized", False),
        ("classification_method_v2_executed", False),
        ("classification_execution_created", False),
        ("classification_execution_performed", False),
        ("failure_modules_classified", False),
        ("error_modules_classified", False),
        ("first_failure_identified", False),
        ("first_error_identified", False),
        ("failure_error_separation_claimed", False),
        ("first_order_failure_analysis_claimed", False),
        ("traceback_root_cause_claimed", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("integration_results_review_created", False),
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
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("strategy_use", service.NOT_AUTHORIZED),
        ("paper_trading", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_candidate_preserves_authority_boundaries(candidate, field, expected):
    assert candidate[field] == expected


def test_future_requirements_plan_outputs_and_non_goals(candidate):
    assert candidate["future_classification_method_v2_requirements"] == service.FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS
    assert len(candidate["future_classification_method_v2_requirements"]) == 16
    assert all(candidate["future_classification_method_v2_requirements"].values())
    assert candidate["future_classification_method_v2_execution_plan"] == service.FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_PLAN
    assert len(candidate["future_classification_method_v2_execution_plan"]) == 10
    assert candidate["future_classification_method_v2_execution_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 9
    assert set(candidate["planned_outputs"].values()) == {"PLANNED_NOT_GENERATED"}
    assert candidate["non_goals"] == service.NON_GOALS
    assert len(candidate["non_goals"]) == 25


def test_next_chain_gates_controls_and_tracking_boundaries(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 48
    assert candidate["no_tracked_marketflow_files"] is True
    assert candidate["no_tracked_pytest_cache_files"] is True
    assert candidate["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_checklist_summary_and_digest_are_deterministic(candidate):
    second = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2()
    assert len(candidate["checklist"]) == len(service.CHECK_IDS) == 63
    assert all(row["status"] == service.PASS for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == 63
    assert candidate["summary"]["passed_checks"] == 63
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    digest_field = "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"
    assert candidate[digest_field] == second[digest_field]
    assert candidate[digest_field] == service.marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(candidate)
    assert result["artifact_kind"] == candidate["artifact_kind"]
    assert result["status"] == candidate["candidate_status"]
    assert result["passed_checks"] == 63


def _set_field(field, value):
    def mutate(payload):
        payload[field] = value
    return mutate


def _delete_field(field):
    def mutate(payload):
        payload.pop(field, None)
    return mutate


def _set_recommended_package(field, value):
    def mutate(payload):
        for package in payload["proposed_classification_method_v2_packages"]:
            if package["package_id"] == service.RECOMMENDED_PACKAGE:
                package[field] = value
    return mutate


VALIDATOR_MUTATIONS = [
    ("wrong_artifact_kind", _set_field("artifact_kind", "WRONG")),
    ("wrong_status", _set_field("candidate_status", "WRONG")),
    ("wrong_scope", _set_field("candidate_scope", "WRONG")),
    ("changed_source_reentry_digest", _set_field("source_classification_method_reentry_digest", "0" * 64)),
    ("changed_source_review_digest", _set_field("source_classification_source_results_review_digest", "0" * 64)),
    ("changed_cache_manifest_digest", _set_field("source_cache_manifest_review_digest", "0" * 64)),
    ("missing_retry_counts", _delete_field("retry_pytest_failed_count")),
    ("missing_cache_counts", _delete_field("lastfailed_cache_entry_count")),
    ("missing_module_summary", _delete_field("module_summary_module_count")),
    ("missing_limitations", _set_field("classification_source_limitations", [])),
    ("candidate_created_false", _set_field("classification_method_candidate_v2_created", False)),
    ("candidate_ready_false", _set_field("classification_method_candidate_v2_ready_for_operator_review", False)),
    ("operator_review_ready_false", _set_field("ready_for_classification_method_candidate_v2_operator_review", False)),
    ("missing_recommended_package", _set_field("recommended_classification_method_v2_package", "MISSING")),
    ("missing_packages", _set_field("proposed_classification_method_v2_packages", [])),
    ("recommended_selected", _set_recommended_package("selected", True)),
    ("recommended_approved", _set_recommended_package("approved", True)),
    ("recommended_executed", _set_recommended_package("executed", True)),
    ("method_selected", _set_field("classification_method_v2_selected", True)),
    ("method_approved", _set_field("classification_method_v2_approved", True)),
    ("method_authorized", _set_field("classification_method_v2_authorized", True)),
    ("method_executed", _set_field("classification_method_v2_executed", True)),
    ("classification_execution_created", _set_field("classification_execution_created", True)),
    ("classification_execution_performed", _set_field("classification_execution_performed", True)),
    ("failure_modules_classified", _set_field("failure_modules_classified", True)),
    ("error_modules_classified", _set_field("error_modules_classified", True)),
    ("first_failure_identified", _set_field("first_failure_identified", True)),
    ("first_error_identified", _set_field("first_error_identified", True)),
    ("failure_error_separation_claimed", _set_field("failure_error_separation_claimed", True)),
    ("first_order_claimed", _set_field("first_order_failure_analysis_claimed", True)),
    ("traceback_claimed", _set_field("traceback_root_cause_claimed", True)),
    ("new_retry_candidate", _set_field("new_retry_candidate_created", True)),
    ("new_retry_executed", _set_field("new_retry_executed", True)),
    ("new_retry_results_review", _set_field("new_retry_results_review_created", True)),
    ("main_merge_approval", _set_field("main_merge_approval_created", True)),
    ("retry_rerun", _set_field("retry_rerun_performed", True)),
    ("full_pytest", _set_field("full_pytest_performed", True)),
    ("diagnostic_command", _set_field("diagnostic_command_executed", True)),
    ("diagnostic_output", _set_field("diagnostic_output_captured", True)),
    ("integration_success", _set_field("integration_execution_successful", True)),
    ("successful_integration_digest", _set_field("successful_integration_execution_digest_generated", True)),
    ("integration_branch_pushed", _set_field("integration_branch_pushed", True)),
    ("main_pushed", _set_field("main_push_performed", True)),
    ("origin_main_modified", _set_field("origin_main_modified_by_this_task", True)),
    ("marketflow_committed", _set_field("marketflow_outputs_committed", True)),
    ("pytest_cache_committed", _set_field("pytest_cache_committed", True)),
    ("evidence_regenerated", _set_field("evidence_regenerated", True)),
    ("provider_requests", _set_field("provider_requests_made_in_candidate", True)),
    ("market_data", _set_field("market_data_acquisition_performed_in_candidate", True)),
    ("dataset_generation", _set_field("dataset_generation_performed_in_candidate", True)),
    ("metric_recomputation", _set_field("metric_recomputation_from_raw_rows_performed", True)),
    ("model_training", _set_field("model_training_performed", True)),
    ("strategy_scoring", _set_field("strategy_scoring_performed", True)),
    ("recommendations", _set_field("trade_recommendations_generated", True)),
    ("predictive_accepted", _set_field("predictive_usefulness", "accepted")),
    ("profitability_accepted", _set_field("profitability", "accepted")),
    ("runtime_authorized", _set_field("runtime_use", "AUTHORIZED")),
    ("broker_authorized", _set_field("broker_execution", "AUTHORIZED")),
    ("missing_v2_requirements", _set_field("future_classification_method_v2_requirements", {})),
    ("missing_v2_plan", _set_field("future_classification_method_v2_execution_plan", [])),
    ("missing_planned_outputs", _set_field("planned_outputs", {})),
    ("missing_non_goals", _set_field("non_goals", [])),
    ("missing_risk_controls", _set_field("risk_controls", [])),
    ("missing_digest", _delete_field("marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest")),
]


@pytest.mark.parametrize("name,mutate", VALIDATOR_MUTATIONS, ids=[row[0] for row in VALIDATOR_MUTATIONS])
def test_validator_rejects_invalid_candidate(candidate, name, mutate):
    invalid = deepcopy(candidate)
    mutate(invalid)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(invalid)


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_markdown_v1(candidate)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Classification Method Candidate v2",
        "Source Reentry",
        "Source Classification-Source Review",
        "Retry Failure Context",
        "Candidate Scope",
        "Candidate Philosophy",
        "Proposed v2 Packages",
        "Recommended v2 Package",
        "Future v2 Requirements",
        "Future v2 Execution Plan",
        "Planned Outputs",
        "Non-Goals",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert title in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2.json"
    assert receipt["path"] == str(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2
    assert payload["marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"] == receipt["marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodCandidateV2Error):
        service.write_marketflow_repository_integration_branch_retry_failure_classification_method_candidate_v2(tmp_path)
