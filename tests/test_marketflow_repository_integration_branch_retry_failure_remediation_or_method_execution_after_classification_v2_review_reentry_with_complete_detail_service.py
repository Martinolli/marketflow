from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_service
    as service,
)


TIMESTAMP = "2026-08-23T00:00:00Z"


def _rows() -> list[dict]:
    return service.review_source._committed_binding_rows()


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        run_timestamp_utc=TIMESTAMP
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        complete_detail_binding_source=[], run_timestamp_utc=TIMESTAMP
    )


def test_success_builds_from_explicit_deterministic_complete_binding() -> None:
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        source_detail_binding_results_review=service._committed_source_review(),
        complete_detail_binding_source=_rows(),
        run_timestamp_utc=TIMESTAMP,
    )
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert artifact["complete_29_row_detail_used_for_planning"] is True


def test_success_builds_from_committed_reviewed_binding(success: dict) -> None:
    assert success["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert success["execution_status"] == service.SUCCESS_STATUS
    assert success["used_committed_source_evidence_only"] is True
    assert success["used_reviewed_complete_29_row_detail_binding"] is True


def test_default_execution_does_not_call_prior_builders_or_executors(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("prior builder or executor must not run")

    monkeypatch.setattr(
        service.review_source,
        "build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.review_source.source.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
        forbidden,
    )
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        run_timestamp_utc=TIMESTAMP
    )
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert artifact["cache_read_in_execution"] is False
    assert artifact["detail_binding_reattempt_rerun_performed"] is False
    assert artifact["materialization_execution_rerun_performed"] is False
    assert artifact["source_recovery_rerun_performed"] is False


def _missing_row(rows: list[dict]) -> None:
    rows.pop()


def _wrong_total(rows: list[dict]) -> None:
    rows[10]["failed_or_errored_nodeid_count"] -= 1


def _wrong_top_count(rows: list[dict]) -> None:
    rows[0]["failed_or_errored_nodeid_count"] -= 1


def _wrong_top_path(rows: list[dict]) -> None:
    rows[0]["module_path"] = "tests/not_the_reviewed_module.py"


def _wrong_top_ten_sum(rows: list[dict]) -> None:
    rows[5]["failed_or_errored_nodeid_count"] -= 1
    rows[10]["failed_or_errored_nodeid_count"] += 1


def _wrong_tier_sums(rows: list[dict]) -> None:
    rows[5]["failed_or_errored_nodeid_count"] -= 1
    rows[28]["failed_or_errored_nodeid_count"] += 1


def _samples_over_bound(rows: list[dict]) -> None:
    rows[0]["sample_nodeids_bounded"] = [f"node-{index}" for index in range(6)]


@pytest.mark.parametrize(
    ("mutator", "reason"),
    [
        (_missing_row, "COMPLETE_DETAIL_ROW_COUNT_NOT_29"),
        (_wrong_total, "FAILED_OR_ERRORED_NODEID_TOTAL_NOT_1404"),
        (_wrong_top_count, "TOP_FIVE_COUNTS_MISMATCH"),
        (_wrong_top_path, "TOP_FIVE_PATHS_MISMATCH"),
        (_wrong_top_ten_sum, "TOP_TEN_SUM_NOT_1069"),
        (_wrong_tier_sums, "PRIORITY_TIER_SUMS_MISMATCH"),
        (_samples_over_bound, "SAMPLES_MISSING_OR_EXCEED_BOUND_5"),
    ],
)
def test_invalid_complete_binding_blocks(mutator, reason: str) -> None:
    rows = _rows()
    mutator(rows)
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        complete_detail_binding_source=rows, run_timestamp_utc=TIMESTAMP
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["execution_status"] == service.BLOCKED_STATUS
    assert reason in artifact["blocked_reason"]
    assert artifact["outputs_generated"] == []


def test_missing_complete_binding_blocks(blocked: dict) -> None:
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert "REVIEWED_COMPLETE_29_ROW_DETAIL_BINDING_UNAVAILABLE" in blocked["blocked_reason"]
    assert blocked["after_v2_planning_execution_reentry_performed"] is False


def test_changed_source_review_blocks() -> None:
    review = service._committed_source_review()
    review[service.review_source.REVIEW_DIGEST_KEY] = "0" * 64
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        source_detail_binding_results_review=review,
        complete_detail_binding_source=_rows(),
        run_timestamp_utc=TIMESTAMP,
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert "SOURCE_REVIEW_" in artifact["blocked_reason"]


def test_identity_scope_package_and_source_bindings(success: dict, blocked: dict) -> None:
    assert success["execution_scope"] == service.EXECUTION_SCOPE
    assert blocked["execution_scope"] == service.EXECUTION_SCOPE
    assert success["selected_after_v2_planning_package"] == service.SELECTED_AFTER_V2_PLANNING_PACKAGE
    assert blocked["selected_after_v2_planning_package"] == service.SELECTED_AFTER_V2_PLANNING_PACKAGE
    assert {field: success[field] for field in service.SOURCE_BINDINGS} == service.SOURCE_BINDINGS
    assert success["source_detail_binding_reattempt_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert success["source_complete_29_row_binding_review_digest"] == service.SOURCE_BINDING_REVIEW_DIGEST
    assert success["source_detail_binding_reattempt_results_review_manifest_digest"] == service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST


def test_retry_context_and_reviewed_detail_facts(success: dict) -> None:
    assert success["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert success["retry_failure_context"]["counts"] == {
        "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
    }
    rows = success["complete_29_row_detail_binding_source"]
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert [row["module_path"] for row in rows[:5]] == service.TOP_FIVE_PATHS
    assert all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows)


def test_success_planning_outputs(success: dict) -> None:
    assert success["module_prioritization_generated"] is True
    assert success["priority_tier_report_generated"] is True
    assert success["top_module_concentration_report_generated"] is True
    assert success["planning_buckets_generated"] is True
    assert success["planned_outputs_generated"] is True
    assert [item["output_id"] for item in success["outputs_generated"]] == service.OUTPUT_IDS
    assert all(item["status"] == service.GENERATED_RESEARCH_ONLY for item in success["outputs_generated"])
    assert all(bucket["status"] == service.PLANNING_ONLY_NOT_EXECUTED for bucket in success["planning_buckets"])


def test_priority_groups_concentration_and_follow_on(success: dict) -> None:
    groups = success["prioritized_module_group_summary"]
    assert [group["priority_group"] for group in groups] == [
        "PRIORITY_1_TOP_5_MODULE_GROUPS",
        "PRIORITY_2_NEXT_5_MODULE_GROUPS",
        "PRIORITY_3_REMAINING_MODULE_GROUPS",
    ]
    assert [group["failed_or_errored_nodeid_count"] for group in groups] == [612, 457, 335]
    assert [group["module_count"] for group in groups] == [5, 5, 19]
    assert success["top_5_count_sum"] == 612
    assert success["top_10_count_sum"] == 1069
    assert success["top_5_percentage_of_failed_or_errored_nodeids"] == "43.58974359"
    assert success["top_10_percentage_of_failed_or_errored_nodeids"] == "76.13960114"
    assert success["ready_for_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail"] is True
    assert success["ready_for_targeted_diagnostic_output_capture_candidate"] is False
    assert success["ready_for_retry_candidate"] is False


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_every_closed_boolean_boundary_remains_false(success: dict, blocked: dict, field: str) -> None:
    assert success[field] is False
    assert blocked[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("strategy_use", service.NOT_AUTHORIZED),
        ("paper_trading", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_non_boolean_authority_boundaries(success: dict, blocked: dict, field: str, expected: str) -> None:
    assert success[field] == expected
    assert blocked[field] == expected


def test_next_chain_gates_risk_controls_and_checklists(success: dict, blocked: dict) -> None:
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert success["risk_controls"] == service.RISK_CONTROLS
    assert blocked["risk_controls"] == service.RISK_CONTROLS
    assert success["summary"]["passed_checks"] == success["summary"]["total_checks"]
    assert blocked["summary"]["passed_checks"] == blocked["summary"]["total_checks"]
    assert all(item["status"] == service.PASS for item in success["checklist"])
    assert all(item["status"] == service.PASS for item in blocked["checklist"])


def test_digests_are_deterministic(success: dict, blocked: dict) -> None:
    repeated_success = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        run_timestamp_utc=TIMESTAMP
    )
    repeated_blocked = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
        complete_detail_binding_source=[], run_timestamp_utc=TIMESTAMP
    )
    for key in (service.EXECUTION_DIGEST_KEY, service.PLANNING_DIGEST_KEY, service.MANIFEST_DIGEST_KEY):
        assert repeated_success[key] == success[key]
    assert repeated_blocked[service.EXECUTION_DIGEST_KEY] == blocked[service.EXECUTION_DIGEST_KEY]
    assert repeated_blocked[service.BLOCKED_MANIFEST_DIGEST_KEY] == blocked[service.BLOCKED_MANIFEST_DIGEST_KEY]


def test_validator_accepts_success_and_blocked(success: dict, blocked: dict) -> None:
    success_validation = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(success)
    blocked_validation = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(blocked)
    assert success_validation["passed_checks"] == success_validation["total_checks"]
    assert blocked_validation["passed_checks"] == blocked_validation["total_checks"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("execution_status", "OTHER"), ("execution_scope", "OTHER"),
        ("selected_after_v2_planning_package", "OTHER"),
        ("source_detail_binding_reattempt_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_review_digest", "0" * 64),
        ("source_detail_binding_reattempt_results_review_manifest_digest", "0" * 64),
        ("source_detail_binding_reattempt_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_detail_binding_reattempt_digest_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context", {}),
        ("source_detail_binding_results_review_status", "OTHER"),
        ("used_reviewed_complete_29_row_detail_binding", False),
        ("planned_outputs_generated", False),
        (service.PLANNING_DIGEST_KEY, "0" * 64),
        (service.MANIFEST_DIGEST_KEY, "0" * 64),
        ("outputs_generated", []), ("risk_controls", []),
        ("next_chain", []), ("next_gates", []), (service.EXECUTION_DIGEST_KEY, None),
    ],
)
def test_validator_rejects_changed_required_success_content(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_opened_boolean_boundary(success: dict, field: str) -> None:
    changed = deepcopy(success)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_opened_acceptance_or_authority(success: dict, field: str, value: str) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("largest_module_nodeid_counts", [1]), ("top_five_module_paths", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("priority_tier_1_count_sum", 611), ("priority_tier_2_count_sum", 456),
        ("priority_tier_3_count_sum", 334), ("prioritized_module_group_summary", []),
        ("planning_buckets", []),
    ],
)
def test_validator_rejects_changed_planning_facts(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    "mutator",
    [_missing_row, _wrong_total, _wrong_top_count, _wrong_top_path, _wrong_top_ten_sum, _wrong_tier_sums, _samples_over_bound],
)
def test_validator_rejects_tampered_success_rows(success: dict, mutator) -> None:
    changed = deepcopy(success)
    mutator(changed["complete_29_row_detail_binding_source"])
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [("blocked_reason", ""), (service.BLOCKED_MANIFEST_DIGEST_KEY, None), ("outputs_generated", [{"output_id": "forbidden"}])],
)
def test_validator_rejects_invalid_blocked_artifact(blocked: dict, field: str, value: object) -> None:
    changed = deepcopy(blocked)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


def test_prechecks_steps_summary_and_outputs_are_complete(success: dict) -> None:
    assert [item["precheck_id"] for item in success["precheck_results"]] == service.PRECHECK_IDS
    assert [item["step_id"] for item in success["execution_steps"]] == service.STEP_IDS
    assert all(set(item) == {"step_id", "status", "expected", "actual", "message"} for item in success["execution_steps"])
    assert success["summary"]["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert success["summary"]["blocker_count"] == 0


def test_markdown_includes_all_required_sections(success: dict, blocked: dict) -> None:
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry with Complete Detail v1",
        "## Source Detail Binding Reattempt Results Review", "## Source Detail Binding Reattempt",
        "## Source Materialization Results Review", "## Source Materialization Execution",
        "## Source Prior Blocked Planning Reentry", "## Source Recovery Results Review",
        "## Retry Failure Context", "## Execution Scope", "## Reviewed Complete 29-row Detail Binding Source",
        "## Planning Reentry Result", "## Prioritized Module Group Summary", "## Priority Tier Report",
        "## Top Module Concentration Report", "## Planning Buckets", "## Unsupported Claims Boundary",
        "## Success or Blocked Disposition", "## Authority Boundaries", "## Next Chain", "## Next Gates",
        "## Risk Controls", "## Checklist Summary", "## Guardrails",
    ]
    for artifact in (success, blocked):
        markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_markdown_v1(artifact)
        assert all(section in markdown for section in required)


def test_public_exports_are_available() -> None:
    import marketflow.services as exports

    assert exports.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_EXECUTED_V1 == service.SUCCESS_ARTIFACT_KIND
    assert exports.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1 is service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1


@pytest.mark.parametrize("timestamp", ["", "2026-08-23", "not-a-time", "2026-08-23T00:00:00+01:00"])
def test_invalid_timestamp_is_rejected(timestamp: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailurePlanningReentryWithCompleteDetailError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1(
            run_timestamp_utc=timestamp
        )
