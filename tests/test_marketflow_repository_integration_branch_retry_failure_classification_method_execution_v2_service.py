from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_service as service,
)


def _failed_nodeids():
    counts = [136, 131, 122, 112, 111] + [33] * 24
    return [
        f"tests/test_module_{module_index:02d}.py::test_case_{case_index:04d}"
        for module_index, count in enumerate(counts)
        for case_index in range(count)
    ]


def _snapshot(**cache_overrides):
    failed = _failed_nodeids()
    nodeids = failed + [f"tests/test_other.py::test_other_{index:05d}" for index in range(26288 - len(failed))]
    state = {
        "origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "integration_branch_head_commit": service.EXPECTED_INTEGRATION_HEAD,
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": str(service.DEFAULT_INTEGRATION_WORKTREE),
        "detached_integration_worktree_head_commit": service.EXPECTED_INTEGRATION_HEAD,
        "detached_integration_worktree_clean": True,
        "staged_evidence_manifest_digest": service.EXPECTED_STAGED_EVIDENCE_DIGEST,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
    }
    cache = {
        "lastfailed_cache_path": str(service.DEFAULT_INTEGRATION_WORKTREE / ".pytest_cache/v/cache/lastfailed"),
        "lastfailed_cache_read": True,
        "lastfailed_cache_sha256": service.EXPECTED_LASTFAILED_SHA256,
        "lastfailed_cache_entry_count": 1404,
        "lastfailed_cache_parseable": True,
        "failed_or_errored_nodeids": failed,
        "nodeids_cache_path": str(service.DEFAULT_INTEGRATION_WORKTREE / ".pytest_cache/v/cache/nodeids"),
        "nodeids_cache_read": True,
        "nodeids_cache_sha256": service.EXPECTED_NODEIDS_SHA256,
        "nodeids_cache_entry_count": 26288,
        "nodeids_cache_parseable": True,
        "nodeids": nodeids,
    }
    cache.update(cache_overrides)
    return {"before": state, "after": deepcopy(state), "cache": cache}


@pytest.fixture(scope="module")
def success():
    return service.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
        cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture(scope="module")
def blocked():
    return service.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
        cache_snapshot=_snapshot(lastfailed_cache_entry_count=1403),
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )


def test_success_execution_builds_from_deterministic_cache_snapshot(success):
    assert success["classification_method_v2_executed"] is True
    assert success["classification_execution_performed"] is True


def test_blocked_execution_builds_from_cache_mismatch(blocked):
    assert blocked["classification_method_v2_executed"] is True
    assert blocked["classification_execution_performed"] is False
    assert blocked["blocked_reason"] == "CACHE_SOURCE_HASH_COUNT_PARSE_OR_MODULE_BOUNDARY_MISMATCH"


@pytest.mark.parametrize(
    "fixture_name,field,expected",
    [
        ("success", "artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2),
        ("blocked", "artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2),
        ("success", "execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTED_V2_MODULE_LEVEL_NODEID_CLASSIFICATION_READY),
        ("blocked", "execution_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_BLOCKED_V2_CACHE_SOURCE_MISMATCH_OR_BOUNDARY_FAILURE),
        ("success", "execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("blocked", "execution_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_EXECUTION_V2_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("success", "selected_classification_method_v2_package", service.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE),
        ("success", "source_classification_method_approval_v2_digest", service.SOURCE_APPROVAL_V2_DIGEST),
        ("success", "source_classification_method_candidate_v2_operator_review_digest", service.source.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("success", "source_classification_method_candidate_v2_digest", service.source.source.SOURCE_CANDIDATE_V2_DIGEST),
        ("success", "source_classification_method_reentry_digest", service.source.source.source.SOURCE_REENTRY_DIGEST),
        ("success", "source_classification_source_results_review_digest", service.source.source.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("success", "source_cache_manifest_review_digest", service.source.source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST),
        ("success", "source_retry_failure_diagnosis_digest", service.source.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST),
        ("success", "retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
    ],
)
def test_identity_status_scope_and_source_bindings(request, fixture_name, field, expected):
    artifact = request.getfixturevalue(fixture_name)
    assert artifact[field] == expected


def test_retry_failure_counts_bound(success):
    assert [success[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert success["retry_pytest_first_result_authoritative"] is True
    assert success["root_full_regression_is_retry_evidence"] is False


def test_cache_hashes_and_counts_verified(success):
    assert success["lastfailed_cache_sha256"] == service.EXPECTED_LASTFAILED_SHA256
    assert success["nodeids_cache_sha256"] == service.EXPECTED_NODEIDS_SHA256
    assert success["lastfailed_cache_entry_count"] == 1404
    assert success["nodeids_cache_entry_count"] == 26288
    assert success["lastfailed_cache_read"] is True
    assert success["nodeids_cache_read"] is True


def test_module_summary_and_ordering(success):
    assert success["module_summary_module_count"] == 29
    assert success["largest_module_nodeid_counts"] == [136, 131, 122, 112, 111]
    assert success["module_summary_report"]["total_nodeids"] == 1404
    rows = success["module_nodeid_grouping_report"]
    assert len(rows) == 29
    assert [(row["failed_or_errored_nodeid_count"], row["module_path"]) for row in rows] == sorted(
        [(row["failed_or_errored_nodeid_count"], row["module_path"]) for row in rows],
        key=lambda row: (-row[0], row[1]),
    )
    assert all(len(row["sample_nodeids_bounded"]) <= 5 for row in rows)


@pytest.mark.parametrize(
    "field,expected",
    [
        ("classification_method_v2_executed", True),
        ("classification_method_v2_selected", True),
        ("classification_method_v2_approved", True),
        ("classification_method_v2_authorized", True),
        ("classification_method_v2_approval_created", True),
        ("ready_for_classification_method_v2_execution", True),
        ("classification_execution_created", True),
        ("classification_execution_performed", True),
        ("module_level_grouping_generated", True),
        ("module_summary_generated", True),
        ("failed_or_errored_nodeids_classified", True),
        ("failed_or_errored_nodeids_count", 1404),
        ("failure_modules_classified", False),
        ("error_modules_classified", False),
        ("failure_error_separation_claimed", False),
        ("first_failure_identified", False),
        ("first_error_identified", False),
        ("first_order_claim_made", False),
        ("traceback_root_cause_claimed", False),
        ("retry_success_claimed", False),
        ("main_merge_readiness_claimed", False),
        ("limitations_report_generated", True),
        ("unsupported_claims_exclusion_report_generated", True),
        ("planned_outputs_generated", True),
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
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
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
def test_success_outputs_and_closed_boundaries(success, field, expected):
    assert success[field] == expected


def test_limitations_and_unsupported_claims_reports(success):
    assert success["cache_source_limitation_report"] == {
        "module_grouping_supported": True,
        "failure_error_separation_supported": False,
        "first_order_supported": False,
        "traceback_root_cause_supported": False,
        "retry_success_supported": False,
    }
    assert all(success["unsupported_claims_exclusion_report"].values())
    assert success["root_cause_family_hints_generated"] is False
    assert success["root_cause_family_hints_basis"] == "NOT_GENERATED_BY_SELECTED_PACKAGE"


def test_planned_outputs(success):
    assert len(success["planned_outputs"]) == 9
    assert success["planned_outputs"]["low_confidence_root_cause_hint_report"] == "NOT_GENERATED_BY_SELECTED_PACKAGE"
    generated = [status for name, status in success["planned_outputs"].items() if name != "low_confidence_root_cause_hint_report"]
    assert generated == ["GENERATED_RESEARCH_ONLY"] * 8


def test_success_and_blocked_next_chain_and_gates(success, blocked):
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert success["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK


def test_risk_controls_defined(success, blocked):
    assert success["risk_controls"] == service.RISK_CONTROLS
    assert blocked["risk_controls"] == service.RISK_CONTROLS
    assert len(service.RISK_CONTROLS) == 47


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_checklist_passes(request, fixture_name):
    artifact = request.getfixturevalue(fixture_name)
    assert len(artifact["checklist"]) == 62
    assert [row["check_id"] for row in artifact["checklist"]] == service.CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in artifact["checklist"])
    assert all(row["status"] == "PASS" for row in artifact["checklist"])
    assert artifact["summary"]["passed_checks"] == 62
    assert artifact["summary"]["failed_checks"] == 0


def test_digests_deterministic():
    first = service.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
        cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    second = service.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(
        cache_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    for field in (
        "marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest",
        "marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest",
        "marketflow_repository_integration_branch_retry_failure_classification_method_v2_digest_manifest_digest",
    ):
        assert first[field] == second[field]


def test_validator_accepts_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(deepcopy(success))["passed_checks"] == 62
    assert service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(deepcopy(blocked))["passed_checks"] == 62


def _set_field(field, value):
    return lambda artifact: artifact.__setitem__(field, value)


def _delete_field(field):
    return lambda artifact: artifact.pop(field, None)


VALIDATOR_MUTATIONS = [
    ("wrong_kind", _set_field("artifact_kind", "wrong")),
    ("wrong_status", _set_field("execution_status", "wrong")),
    ("wrong_scope", _set_field("execution_scope", "wrong")),
    ("wrong_package", _set_field("selected_classification_method_v2_package", "wrong")),
    ("approval_digest", _set_field("source_classification_method_approval_v2_digest", "0" * 64)),
    ("candidate_digest", _set_field("source_classification_method_candidate_v2_digest", "0" * 64)),
    ("reentry_digest", _set_field("source_classification_method_reentry_digest", "0" * 64)),
    ("results_digest", _set_field("source_classification_source_results_review_digest", "0" * 64)),
    ("cache_manifest_digest", _set_field("source_cache_manifest_review_digest", "0" * 64)),
    ("retry_count", _delete_field("retry_pytest_failed_count")),
    ("cache_count", _set_field("lastfailed_cache_entry_count", 1403)),
    ("module_count", _set_field("module_summary_module_count", 28)),
    ("method_not_executed", _set_field("classification_method_v2_executed", False)),
    ("without_grouping", _set_field("module_level_grouping_generated", False)),
    ("without_grouping_digest", _delete_field("marketflow_repository_integration_branch_retry_failure_classification_method_v2_module_grouping_digest")),
    ("without_limitations", _set_field("cache_source_limitation_report", None)),
    ("without_exclusions", _set_field("unsupported_claims_exclusion_report", None)),
    ("failure_modules", _set_field("failure_modules_classified", True)),
    ("error_modules", _set_field("error_modules_classified", True)),
    ("failure_error", _set_field("failure_error_separation_claimed", True)),
    ("first_failure", _set_field("first_failure_identified", True)),
    ("first_error", _set_field("first_error_identified", True)),
    ("first_order", _set_field("first_order_claim_made", True)),
    ("traceback", _set_field("traceback_root_cause_claimed", True)),
    ("retry_success", _set_field("retry_success_claimed", True)),
    ("main_readiness", _set_field("main_merge_readiness_claimed", True)),
    ("retry_candidate", _set_field("new_retry_candidate_created", True)),
    ("retry_executed", _set_field("new_retry_executed", True)),
    ("retry_review", _set_field("new_retry_results_review_created", True)),
    ("main_approval", _set_field("main_merge_approval_created", True)),
    ("retry_rerun", _set_field("retry_rerun_performed", True)),
    ("full_pytest", _set_field("full_pytest_performed", True)),
    ("diagnostic", _set_field("diagnostic_command_executed", True)),
    ("integration_success", _set_field("integration_execution_successful", True)),
    ("success_digest", _set_field("successful_integration_execution_digest_generated", True)),
    ("integration_push", _set_field("integration_branch_pushed", True)),
    ("main_push", _set_field("main_push_performed", True)),
    ("origin_main", _set_field("origin_main_modified_by_this_task", True)),
    ("marketflow_commit", _set_field("marketflow_outputs_committed", True)),
    ("pytest_cache_commit", _set_field("pytest_cache_committed", True)),
    ("evidence_regenerated", _set_field("evidence_regenerated", True)),
    ("provider", _set_field("provider_requests_made_in_execution", True)),
    ("market_data", _set_field("market_data_acquisition_performed_in_execution", True)),
    ("dataset", _set_field("dataset_generation_performed_in_execution", True)),
    ("metrics", _set_field("metric_recomputation_from_raw_rows_performed", True)),
    ("model", _set_field("model_training_performed", True)),
    ("strategy", _set_field("strategy_scoring_performed", True)),
    ("recommendations", _set_field("trade_recommendations_generated", True)),
    ("predictive", _set_field("predictive_usefulness", "accepted")),
    ("profitability", _set_field("profitability", "accepted")),
    ("runtime", _set_field("runtime_use", "AUTHORIZED")),
    ("broker", _set_field("broker_execution", "AUTHORIZED")),
    ("risk_controls", _set_field("risk_controls", [])),
    ("missing_digest", _delete_field("marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_digest")),
]


@pytest.mark.parametrize("name,mutate", VALIDATOR_MUTATIONS, ids=[row[0] for row in VALIDATOR_MUTATIONS])
def test_validator_rejects_invalid_success(success, name, mutate):
    invalid = deepcopy(success)
    mutate(invalid)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodExecutionV2Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2(invalid)


def test_markdown_includes_required_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_markdown_v1(success)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Classification Method Execution v2",
        "Source Approval", "Retry Failure Context", "Cache Source Verification", "Execution Scope",
        "Module-Level Grouping", "Limitations", "Unsupported Claims Exclusion",
        "Success or Blocked Disposition", "Authority Boundaries", "Next Chain", "Next Gates",
        "Risk Controls", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown


def test_services_exports_execution_v2_surface():
    assert services.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2 is service.execute_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2
    assert services.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2 is service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2
    assert services.build_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_markdown_v1 is service.build_marketflow_repository_integration_branch_retry_failure_classification_method_execution_v2_markdown_v1
