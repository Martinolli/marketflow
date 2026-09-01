from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_service
    as service,
)


@pytest.fixture(scope="module")
def success() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1()


@pytest.fixture(scope="module")
def blocked() -> dict:
    source_execution = service._committed_source()
    source_execution.pop("recovered_module_grouping_detail_report")
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(
        source_execution=source_execution
    )


def test_default_build_is_deterministic_and_does_not_read_cache_or_rerun_recovery(monkeypatch):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("results review crossed its read-only source-artifact boundary")

    monkeypatch.setattr(service.Path, "read_bytes", forbidden)
    monkeypatch.setattr(service.Path, "read_text", forbidden)
    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1",
        forbidden,
    )
    first = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1()
    second = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1()
    assert first == second
    assert first["cache_read_in_review"] is False


def test_success_and_blocked_dispositions(success, blocked):
    assert success["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1
    assert success["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_V1
    assert blocked["review_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_BLOCKED_SOURCE_RECOVERY_DETAIL_MISSING_OR_BOUNDARY_FAILURE
    assert "RECOVERED_MODULE_DETAIL_MISSING" in blocked["blocked_reason"]
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK


@pytest.mark.parametrize(
    "field,expected",
    [
        ("review_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN),
        ("source_module_grouping_source_recovery_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_approval_digest", service.source.SOURCE_APPROVAL_DIGEST),
        ("source_module_grouping_source_recovery_operator_review_digest", service.source.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_candidate_digest", service.source.approval_source.source.SOURCE_CANDIDATE_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.approval_source.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.source.approval_source.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason_before_recovery", service.source.approval_source.source.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_results_review_v2_digest", service.source.approval_source.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.approval_source.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.approval_source.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("retry_pytest_first_result_authoritative", True),
        ("root_full_regression_is_retry_evidence", False),
        ("selected_module_grouping_source_recovery_package", service.source.SELECTED_PACKAGE),
        ("module_grouping_source_recovery_execution_reviewed", True),
        ("module_grouping_detail_reviewed", True),
        ("module_paths_reviewed", True),
        ("per_module_counts_reviewed", True),
        ("bounded_nodeid_samples_reviewed", True),
        ("top_module_source_detail_reviewed", True),
        ("cache_hash_and_count_verification_reviewed", True),
        ("lastfailed_subset_of_nodeids_reviewed", True),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("top_5_count_sum", 612),
        ("top_5_percentage_of_failed_or_errored_nodeids", "43.58974359"),
        ("top_10_count_sum", 1069),
        ("top_10_percentage_of_failed_or_errored_nodeids", "76.13960114"),
        ("planned_outputs_reviewed", True),
        ("source_recovery_limitations_reviewed", True),
        ("unsupported_claims_boundary_reviewed", True),
        ("module_grouping_source_recovery_results_review_created", True),
        ("module_grouping_source_recovery_results_review_ready", True),
        ("ready_for_after_v2_planning_reentry_after_source_recovery_review", True),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_success_binds_required_review_facts(success, field, expected):
    assert success[field] == expected


def test_cache_module_and_top_module_reviews(success):
    cache = success["cache_hash_and_count_verification_review"]
    assert cache == {
        "lastfailed_cache_sha256_verified": True,
        "nodeids_cache_sha256_verified": True,
        "lastfailed_cache_count_verified": True,
        "nodeids_cache_count_verified": True,
        "lastfailed_nodeids_subset_of_nodeids": True,
    }
    assert success["recovered_module_grouping_detail_review"] == {
        "source_detail_digest": service.SOURCE_RECOVERY_DETAIL_DIGEST,
        "module_count": 29,
        "nodeid_count": 1404,
        "reviewed": True,
    }
    assert success["top_five_module_paths"] == service.TOP_FIVE
    assert success["source_recovery_limitations_review"] == service.LIMITATIONS
    assert len(success["planned_outputs_review"]) == 10
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in success["planned_outputs_review"])


@pytest.mark.parametrize(
    "field",
    [
        "failure_modules_classified",
        "error_modules_classified",
        "failure_error_separation_claimed",
        "first_failure_identified",
        "first_error_identified",
        "first_order_claim_made",
        "traceback_root_cause_claimed",
        "direct_code_remediation_recommended",
        "retry_success_claimed",
        "main_merge_readiness_claimed",
        "diagnostic_method_executed",
        "code_remediation_executed",
        "evidence_remediation_executed",
        "classification_execution_performed",
        "after_v2_planning_reentry_created",
        "remediation_or_method_after_v2_reentry_created",
        "new_retry_candidate_created",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "retry_rerun_performed",
        "full_pytest_performed",
        "diagnostic_command_executed",
        "diagnostic_output_captured",
        "cache_read_in_review",
        "integration_execution_successful",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "pytest_cache_committed",
        "evidence_regenerated",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_success_preserves_false_claim_and_authority_boundaries(success, field):
    assert success[field] is False


def test_next_paths_risk_controls_observations_and_checklists(success, blocked):
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert success["risk_controls"] == service.RISK_CONTROLS
    assert len(success["risk_controls"]) == 56
    expected_observations = {
        "source_execution_digest_bound", "recovery_detail_digest_bound", "digest_manifest_bound",
        "source_approval_digest_bound", "retry_failure_counts_bound",
        "cache_hash_and_count_verification_reviewed", "lastfailed_subset_of_nodeids_reviewed",
        "module_grouping_detail_reviewed", "module_paths_reviewed", "per_module_counts_reviewed",
        "bounded_nodeid_samples_reviewed", "module_count_29_reviewed", "largest_module_counts_reviewed",
        "top_five_module_paths_reviewed", "top_five_concentration_reviewed",
        "top_ten_concentration_reviewed", "planned_outputs_reviewed", "limitations_reviewed",
        "unsupported_claims_boundary_reviewed", "failed_retry_preserved",
        "root_regression_not_retry_evidence",
        "ready_for_after_v2_planning_reentry_after_source_recovery_review",
        "no_cache_read_in_review", "no_retry_rerun", "no_full_pytest", "no_diagnostic_command",
        "no_planning_reentry_created", "no_new_retry_candidate", "no_integration_success",
        "no_protected_branch_push", "no_provider_or_runtime_actions",
    }
    assert {item["observation_id"] for item in success["review_observations"]} == expected_observations
    assert all(item["status"] == service.PASS for item in success["review_observations"])
    assert all(item["status"] == service.PASS for item in success["checklist"])
    assert all(item["status"] == service.PASS for item in blocked["checklist"])
    assert success["summary"]["total_checks"] == success["summary"]["passed_checks"] == 80
    assert blocked["summary"]["total_checks"] == blocked["summary"]["passed_checks"] == 84


def test_review_and_manifest_digests_are_deterministic(success, blocked):
    repeated = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1()
    repeated_blocked_source = service._committed_source()
    repeated_blocked_source.pop("recovered_module_grouping_detail_report")
    repeated_blocked = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(
        source_execution=repeated_blocked_source
    )
    assert repeated["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"] == success["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"]
    assert repeated["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest"] == success["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest"]
    assert repeated_blocked["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"] == blocked["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"]
    assert repeated_blocked["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest"] == blocked["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest"]


def test_validator_accepts_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(success)["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(blocked)["failed_checks"] == 0


DELETE = object()


@pytest.mark.parametrize(
    "path,value",
    [
        (("artifact_kind",), "WRONG"),
        (("review_status",), "WRONG"),
        (("review_scope",), "WRONG"),
        (("source_module_grouping_source_recovery_execution_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_detail_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_digest_manifest_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_approval_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_operator_review_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_candidate_digest",), "0" * 64),
        (("source_blocked_after_v2_execution_digest",), "0" * 64),
        (("source_blocked_after_v2_manifest_digest",), "0" * 64),
        (("blocked_reason_before_recovery",), DELETE),
        (("source_results_review_v2_digest",), "0" * 64),
        (("source_execution_v2_digest",), "0" * 64),
        (("source_module_grouping_digest",), "0" * 64),
        (("retry_pytest_failed_count",), DELETE),
        (("cache_hash_and_count_verification_review",), DELETE),
        (("lastfailed_subset_of_nodeids_reviewed",), False),
        (("module_grouping_detail_reviewed",), False),
        (("module_paths_reviewed",), False),
        (("per_module_counts_reviewed",), False),
        (("bounded_nodeid_samples_reviewed",), False),
        (("module_summary_module_count",), 28),
        (("largest_module_nodeid_counts",), [136]),
        (("top_module_source_detail_reviewed",), False),
        (("top_5_count_sum",), 611),
        (("top_10_count_sum",), 1068),
        (("source_recovery_limitations_reviewed",), False),
        (("unsupported_claims_boundary_reviewed",), False),
        (("failure_error_separation_claimed",), True),
        (("first_failure_identified",), True),
        (("first_error_identified",), True),
        (("first_order_claim_made",), True),
        (("traceback_root_cause_claimed",), True),
        (("direct_code_remediation_recommended",), True),
        (("retry_success_claimed",), True),
        (("main_merge_readiness_claimed",), True),
        (("module_grouping_source_recovery_results_review_created",), False),
        (("module_grouping_source_recovery_results_review_ready",), False),
        (("ready_for_after_v2_planning_reentry_after_source_recovery_review",), False),
        (("after_v2_planning_reentry_created",), True),
        (("new_retry_candidate_created",), True),
        (("new_retry_executed",), True),
        (("new_retry_results_review_created",), True),
        (("main_merge_approval_created",), True),
        (("retry_rerun_performed",), True),
        (("full_pytest_performed",), True),
        (("diagnostic_command_executed",), True),
        (("diagnostic_output_captured",), True),
        (("cache_read_in_review",), True),
        (("integration_execution_successful",), True),
        (("successful_integration_execution_digest_generated",), True),
        (("integration_branch_pushed",), True),
        (("main_push_performed",), True),
        (("origin_main_modified_by_this_task",), True),
        (("marketflow_outputs_committed",), True),
        (("pytest_cache_committed",), True),
        (("evidence_regenerated",), True),
        (("provider_requests_made_in_review",), True),
        (("market_data_acquisition_performed_in_review",), True),
        (("dataset_generation_performed_in_review",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True),
        (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness",), "accepted"),
        (("profitability",), "accepted"),
        (("runtime_use",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("risk_controls",), []),
        (("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest",), DELETE),
        (("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_manifest_digest",), DELETE),
    ],
)
def test_validator_rejects_mutated_success_artifact(success, path, value):
    mutated = deepcopy(success)
    target = mutated
    for key in path[:-1]:
        target = target[key]
    if value is DELETE:
        target.pop(path[-1])
    else:
        target[path[-1]] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(mutated)


def test_validator_rejects_wrong_blocked_kind_status_and_missing_manifest(blocked):
    for field, value in (
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_blocked_manifest_digest", None),
    ):
        mutated = deepcopy(blocked)
        mutated[field] = value
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(mutated)


def test_write_round_trip_and_refuses_overwrite(tmp_path, success):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1.json").read_text(encoding="utf-8"))
    assert payload == success
    assert receipt["review_digest"] == success["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1(tmp_path)


def test_markdown_contains_all_required_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_markdown_v1(success)
    for heading in (
        "MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Results Review v1",
        "Source Recovery Execution",
        "Source Approval and Candidate Chain",
        "Retry Failure Context",
        "Cache Verification Review",
        "Recovered Module Grouping Detail Review",
        "Top Module Source Detail Review",
        "Unsupported Claims Boundary",
        "Source Recovery Limitations",
        "Success or Blocked Disposition",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert heading in markdown


def test_package_exports_are_available():
    assert services.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1 is service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1
    assert services.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1 is service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1
    assert services.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1 is service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_v1
    assert services.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_markdown_v1 is service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_results_review_markdown_v1
