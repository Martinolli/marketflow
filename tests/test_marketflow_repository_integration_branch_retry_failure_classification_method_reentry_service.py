from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_reentry_service as service,
)


@pytest.fixture
def reentry():
    return service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1()


def test_reentry_builds_offline_without_cache_read(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("cache/source builder must not be called")

    monkeypatch.setattr(service.source, "_fixture_or_live_snapshot", forbidden)
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1",
        forbidden,
    )
    built = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1()
    assert built["created_offline"] is True
    assert built["classification_method_reentry_ready"] is True


def test_reentry_accepts_valid_injected_source_review():
    counts = [136, 131, 122, 112, 111, *([1] * 24)]
    snapshot = {
        "lastfailed_cache_path": str(service.source.source.EXPECTED_INTEGRATION_WORKTREE / service.source.source.LASTFAILED_RELATIVE_PATH),
        "lastfailed_cache_exists": True,
        "lastfailed_cache_read": True,
        "lastfailed_cache_parseable_json": True,
        "lastfailed_cache_sha256": service.source.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count": 1404,
        "lastfailed_nodeids_extracted": True,
        "failed_or_errored_nodeids_count": 1404,
        "nodeids_cache_path": str(service.source.source.EXPECTED_INTEGRATION_WORKTREE / service.source.source.NODEIDS_RELATIVE_PATH),
        "nodeids_cache_exists": True,
        "nodeids_cache_read": True,
        "nodeids_cache_parseable_json": True,
        "nodeids_cache_sha256": service.source.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count": 26288,
        "module_summary_generated": True,
        "module_summary": [
            {"module_path": f"tests/test_module_{index:02d}.py", "nodeid_count": count}
            for index, count in enumerate(counts, start=1)
        ],
        "module_summary_total_modules": 29,
        "module_summary_truncated": False,
        "origin_main_commit": service.source.source.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head_commit": service.source.source.INTEGRATION_HEAD_COMMIT,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(service.source.source.EXPECTED_INTEGRATION_WORKTREE),
        "detached_integration_worktree_head_commit": service.source.source.INTEGRATION_HEAD_COMMIT,
        "detached_integration_worktree_is_detached": True,
        "detached_integration_worktree_clean_at_review": True,
        "staged_evidence_manifest_digest": service.source.source.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
    }
    review = service.source.build_marketflow_repository_integration_branch_retry_failure_output_capture_or_classification_source_results_review_v1(
        cache_snapshot=snapshot
    )
    built = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(
        source_results_review=review
    )
    assert built["source_classification_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert built["marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"] == service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1()["marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"]


def test_artifact_status_and_scope(reentry):
    assert reentry["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1
    assert reentry["reentry_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY
    assert reentry["reentry_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN
    assert reentry["governance_only"] is True
    assert reentry["reentry_only"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        ("source_classification_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_cache_manifest_review_digest", service.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST),
        ("source_output_capture_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_classification_source_manifest_digest", service.SOURCE_CLASSIFICATION_SOURCE_MANIFEST_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("retry_pytest_passed_count", 24877),
        ("retry_pytest_failed_count", 1292),
        ("retry_pytest_error_count", 112),
        ("retry_pytest_skipped_count", 7),
        ("lastfailed_cache_entry_count", 1404),
        ("nodeids_cache_entry_count", 26288),
        ("module_summary_module_count", 29),
        ("module_summary_untruncated", True),
        ("largest_module_nodeid_counts_reviewed", [136, 131, 122, 112, 111]),
        ("root_full_regression_is_retry_evidence", False),
        ("retry_pytest_first_result_authoritative", True),
    ],
)
def test_reentry_binds_source_review_retry_cache_and_module_facts(reentry, field, expected):
    assert reentry[field] == expected


def test_classification_source_capability_and_limitations(reentry):
    assert reentry["classification_source_valid_for_reentry"] is True
    assert reentry["classification_source_validity_basis"] == service.CLASSIFICATION_SOURCE_VALIDITY_BASIS
    assert reentry["classification_source_reentry_limitations"] == service.CLASSIFICATION_SOURCE_REENTRY_LIMITATIONS
    assert reentry["classification_source_accepted_for"] == service.CLASSIFICATION_SOURCE_ACCEPTED_FOR
    assert reentry["classification_source_not_accepted_for"] == service.CLASSIFICATION_SOURCE_NOT_ACCEPTED_FOR
    assert reentry["classification_source_accepted_for_reentry"] is True
    assert reentry["classification_source_accepted_for_module_level_only"] is True
    assert reentry["classification_source_accepted_for_failure_error_separation"] is False
    assert reentry["classification_source_accepted_for_first_order_failure_analysis"] is False
    assert reentry["classification_source_not_accepted_for_failure_error_separation"] is True
    assert reentry["classification_source_not_accepted_for_first_order_failure_analysis"] is True


def test_reentry_decision_requires_v2_candidate(reentry):
    assert reentry["reentry_decision"] == service.REENTRY_DECISION
    assert reentry["recommended_reentry_path"] == service.REENTRY_DECISION
    assert reentry["reentry_reason"] == service.REENTRY_REASON


def test_reentry_options_select_only_v2_candidate(reentry):
    options = {row["option_id"]: row for row in reentry["reentry_options"]}
    assert options["OPTION_CREATE_CLASSIFICATION_METHOD_CANDIDATE_V2_FOR_CACHE_SOURCE"]["status"] == "RECOMMENDED_FOR_NEXT_TASK"
    assert options["OPTION_CREATE_CLASSIFICATION_METHOD_CANDIDATE_V2_FOR_CACHE_SOURCE"]["selected"] is True
    assert options["OPTION_DIRECT_REENTER_ORIGINAL_CLASSIFICATION_METHOD"]["status"] == "NOT_RECOMMENDED_LIMITED_SOURCE"
    assert options["OPTION_DIRECT_REENTER_ORIGINAL_CLASSIFICATION_METHOD"]["selected"] is False
    assert options["OPTION_REQUIRE_DIAGNOSTIC_OUTPUT_CAPTURE_BEFORE_ANY_CLASSIFICATION"]["status"] == "AVAILABLE_NOT_SELECTED"
    assert options["OPTION_REQUIRE_DIAGNOSTIC_OUTPUT_CAPTURE_BEFORE_ANY_CLASSIFICATION"]["selected"] is False
    assert options["OPTION_NEW_RETRY_WITHOUT_CLASSIFICATION"]["status"] == "BLOCKED_NOT_ALLOWED"
    assert options["OPTION_NEW_RETRY_WITHOUT_CLASSIFICATION"]["selected"] is False
    assert options["OPTION_MAIN_MERGE_DESPITE_FAILED_RETRY"]["status"] == "BLOCKED_NOT_ALLOWED"
    assert options["OPTION_MAIN_MERGE_DESPITE_FAILED_RETRY"]["selected"] is False


@pytest.mark.parametrize(
    "field,expected",
    [
        ("classification_method_reentry_created", True),
        ("classification_method_reentry_ready", True),
        ("classification_execution_created", False),
        ("classification_execution_performed", False),
        ("failure_modules_classified", False),
        ("error_modules_classified", False),
        ("first_failure_identified", False),
        ("first_error_identified", False),
        ("new_classification_method_candidate_created", False),
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
        ("provider_requests_made_in_reentry", False),
        ("market_data_acquisition_performed_in_reentry", False),
        ("dataset_generation_performed_in_reentry", False),
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
def test_reentry_preserves_authority_boundaries(reentry, field, expected):
    assert reentry[field] == expected


def test_future_v2_requirements_and_candidate_plan_are_planning_only(reentry):
    assert reentry["future_classification_method_v2_requirements"] == service.FUTURE_CLASSIFICATION_METHOD_V2_REQUIREMENTS
    assert all(reentry["future_classification_method_v2_requirements"].values())
    assert reentry["future_classification_method_v2_candidate_plan"] == service.FUTURE_CLASSIFICATION_METHOD_V2_CANDIDATE_PLAN
    assert reentry["future_classification_method_v2_candidate_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert reentry["new_classification_method_candidate_created"] is False


def test_next_chain_gates_controls_and_tracking_boundaries(reentry):
    assert reentry["next_chain"] == service.NEXT_CHAIN
    assert reentry["next_gates"] == service.NEXT_GATES
    assert reentry["risk_controls"] == service.RISK_CONTROLS
    assert len(reentry["risk_controls"]) == 49
    assert reentry["no_tracked_marketflow_files"] is True
    assert reentry["no_tracked_pytest_cache_files"] is True
    assert reentry["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK


def test_checklist_summary_and_digest_are_deterministic(reentry):
    second = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1()
    assert len(reentry["checklist"]) == len(service.CHECK_IDS) == 61
    assert all(row["status"] == service.PASS for row in reentry["checklist"])
    assert reentry["summary"]["total_checks"] == 61
    assert reentry["summary"]["passed_checks"] == 61
    assert reentry["summary"]["failed_checks"] == 0
    assert reentry["summary"]["blocker_count"] == 0
    digest_field = "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"
    assert reentry[digest_field] == second[digest_field]
    assert reentry[digest_field] == service.marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest_v1(reentry)


def test_validator_accepts_valid_reentry(reentry):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(reentry)
    assert result["artifact_kind"] == reentry["artifact_kind"]
    assert result["status"] == reentry["reentry_status"]
    assert result["passed_checks"] == 61


def _set_field(field, value):
    def mutate(payload):
        payload[field] = value
    return mutate


def _delete_field(field):
    def mutate(payload):
        payload.pop(field, None)
    return mutate


def _select_option(option_id):
    def mutate(payload):
        for option in payload["reentry_options"]:
            if option["option_id"] == option_id:
                option["selected"] = True
    return mutate


VALIDATOR_MUTATIONS = [
    ("wrong_artifact_kind", _set_field("artifact_kind", "WRONG")),
    ("wrong_status", _set_field("reentry_status", "WRONG")),
    ("wrong_scope", _set_field("reentry_scope", "WRONG")),
    ("changed_source_review_digest", _set_field("source_classification_results_review_digest", "0" * 64)),
    ("changed_cache_manifest_digest", _set_field("source_cache_manifest_review_digest", "0" * 64)),
    ("missing_retry_failure_counts", _delete_field("retry_pytest_failed_count")),
    ("missing_cache_counts", _delete_field("lastfailed_cache_entry_count")),
    ("missing_module_summary", _delete_field("module_summary_module_count")),
    ("missing_limitations", _set_field("classification_source_reentry_limitations", [])),
    ("source_invalid_for_reentry", _set_field("classification_source_valid_for_reentry", False)),
    ("failure_error_separation_accepted", _set_field("classification_source_accepted_for_failure_error_separation", True)),
    ("first_order_accepted", _set_field("classification_source_accepted_for_first_order_failure_analysis", True)),
    ("wrong_reentry_decision", _set_field("reentry_decision", "DIRECT_REENTRY")),
    ("direct_method_selected", _select_option("OPTION_DIRECT_REENTER_ORIGINAL_CLASSIFICATION_METHOD")),
    ("retry_without_classification_selected", _select_option("OPTION_NEW_RETRY_WITHOUT_CLASSIFICATION")),
    ("main_merge_despite_failure_selected", _select_option("OPTION_MAIN_MERGE_DESPITE_FAILED_RETRY")),
    ("reentry_created_false", _set_field("classification_method_reentry_created", False)),
    ("reentry_ready_false", _set_field("classification_method_reentry_ready", False)),
    ("classification_execution_created", _set_field("classification_execution_created", True)),
    ("classification_execution_performed", _set_field("classification_execution_performed", True)),
    ("failure_modules_classified", _set_field("failure_modules_classified", True)),
    ("error_modules_classified", _set_field("error_modules_classified", True)),
    ("first_failure_identified", _set_field("first_failure_identified", True)),
    ("first_error_identified", _set_field("first_error_identified", True)),
    ("new_method_candidate_created", _set_field("new_classification_method_candidate_created", True)),
    ("new_retry_candidate_created", _set_field("new_retry_candidate_created", True)),
    ("new_retry_executed", _set_field("new_retry_executed", True)),
    ("new_retry_review_created", _set_field("new_retry_results_review_created", True)),
    ("main_merge_approval_created", _set_field("main_merge_approval_created", True)),
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
    ("provider_requests", _set_field("provider_requests_made_in_reentry", True)),
    ("market_data", _set_field("market_data_acquisition_performed_in_reentry", True)),
    ("dataset_generation", _set_field("dataset_generation_performed_in_reentry", True)),
    ("metric_recomputation", _set_field("metric_recomputation_from_raw_rows_performed", True)),
    ("model_training", _set_field("model_training_performed", True)),
    ("strategy_scoring", _set_field("strategy_scoring_performed", True)),
    ("recommendations", _set_field("trade_recommendations_generated", True)),
    ("predictive_accepted", _set_field("predictive_usefulness", "accepted")),
    ("profitability_accepted", _set_field("profitability", "accepted")),
    ("runtime_authorized", _set_field("runtime_use", "AUTHORIZED")),
    ("broker_authorized", _set_field("broker_execution", "AUTHORIZED")),
    ("missing_v2_requirements", _set_field("future_classification_method_v2_requirements", {})),
    ("missing_v2_plan", _set_field("future_classification_method_v2_candidate_plan", [])),
    ("missing_risk_controls", _set_field("risk_controls", [])),
    ("missing_digest", _delete_field("marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest")),
]


@pytest.mark.parametrize("name,mutate", VALIDATOR_MUTATIONS, ids=[row[0] for row in VALIDATOR_MUTATIONS])
def test_validator_rejects_invalid_reentry(reentry, name, mutate):
    invalid = deepcopy(reentry)
    mutate(invalid)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError):
        service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(invalid)


def test_markdown_includes_required_sections(reentry):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_markdown_v1(reentry)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Classification Method Reentry v1",
        "Source Classification-Source Results Review",
        "Retry Failure Context",
        "Cache Source Capability",
        "Cache Source Limitations",
        "Reentry Decision",
        "Reentry Options",
        "Future Classification Method v2 Requirements",
        "Future Classification Method v2 Candidate Plan",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert title in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(tmp_path)
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1.json"
    assert receipt["path"] == str(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1
    assert payload["marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"] == receipt["marketflow_repository_integration_branch_retry_failure_classification_method_reentry_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodReentryError):
        service.write_marketflow_repository_integration_branch_retry_failure_classification_method_reentry_v1(tmp_path)
