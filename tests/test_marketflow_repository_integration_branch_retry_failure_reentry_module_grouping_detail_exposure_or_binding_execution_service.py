from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_service
    as service,
)


def _complete_snapshot() -> dict:
    counts = [136, 131, 122, 112, 111, 100, 95, 92, 87, 83, *([18] * 18), 11]
    paths = [
        *service.TOP_FIVE_PATHS,
        *[f"tests/test_committed_recovered_module_{index:02d}.py" for index in range(6, 30)],
    ]
    rows = [
        {
            "module_path": path,
            "failed_or_errored_nodeid_count": count,
            "sample_nodeids_bounded": [f"{path}::test_b", f"{path}::test_a"],
        }
        for path, count in zip(paths, counts, strict=True)
    ]
    return {"rows": rows, "source_detail_digest": service.SOURCE_DETAIL_DIGEST}


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
        complete_detail_snapshot=_complete_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def test_success_execution_builds_from_deterministic_complete_snapshot(success: dict) -> None:
    assert success["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert success["execution_status"] == service.SUCCESS_STATUS
    assert success["execution_scope"] == service.EXECUTION_SCOPE
    assert success["selected_detail_exposure_or_binding_package"] == service.SELECTED_PACKAGE
    assert success["detail_exposure_or_binding_executed"] is True
    assert success["complete_29_row_detail_exposed"] is True
    assert success["complete_29_row_detail_bound"] is True
    assert success["complete_29_row_detail_source_identified"] is True
    assert success["module_grouping_detail_exposed_by_execution"] is True
    assert success["module_paths_bound_by_execution"] is True
    assert success["per_module_counts_bound_by_execution"] is True
    assert success["bounded_nodeid_samples_bound_by_execution"] is True


def test_blocked_execution_builds_when_committed_detail_is_missing(blocked: dict) -> None:
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert blocked["execution_scope"] == service.EXECUTION_SCOPE
    assert blocked["detail_exposure_or_binding_executed"] is True
    assert blocked["complete_29_row_detail_exposed"] is False
    assert blocked["complete_29_row_detail_bound"] is False
    assert blocked["complete_29_row_detail_source_identified"] is False
    assert blocked["blocked_reason"] == service.BLOCKED_SOURCE_UNAVAILABLE
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK


def test_default_execution_never_calls_cache_reading_source_recovery(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("source recovery executor must not be called")

    monkeypatch.setattr(
        service.recovery_source,
        "execute_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_execution_v1",
        forbidden,
    )
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["cache_read_in_execution"] is False
    assert artifact["source_recovery_rerun_performed"] is False


@pytest.mark.parametrize(
    ("mutator", "reason"),
    [
        (lambda snapshot: snapshot["rows"].pop(), "COMPLETE_DETAIL_ROW_COUNT_NOT_29"),
        (lambda snapshot: snapshot["rows"][10].update(failed_or_errored_nodeid_count=17), "FAILED_OR_ERRORED_NODEID_TOTAL_NOT_1404"),
        (lambda snapshot: snapshot["rows"][0].update(failed_or_errored_nodeid_count=135), "TOP_FIVE_COUNTS_MISMATCH"),
        (lambda snapshot: snapshot["rows"][5].update(failed_or_errored_nodeid_count=99), "PRIORITY_TIER_2_SUM_NOT_457"),
        (lambda snapshot: snapshot["rows"][0].update(sample_nodeids_bounded=[f"node::{index}" for index in range(6)]), "SAMPLES_EXCEED_BOUND_5"),
    ],
)
def test_incomplete_or_inconsistent_snapshot_blocks(mutator, reason: str) -> None:
    snapshot = _complete_snapshot()
    mutator(snapshot)
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
        complete_detail_snapshot=snapshot, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert reason in artifact["blocked_reason"]
    assert artifact["complete_29_row_detail_bound"] is False


def test_snapshot_with_wrong_source_digest_blocks() -> None:
    snapshot = _complete_snapshot()
    snapshot["source_detail_digest"] = "0" * 64
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(
        complete_detail_snapshot=snapshot, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert "COMPLETE_DETAIL_SNAPSHOT_SOURCE_DIGEST_MISMATCH" in artifact["blocked_reason"]


def test_success_binds_all_required_source_digests(success: dict) -> None:
    expected = {
        "source_detail_exposure_or_binding_approval_digest": "384ea3fcb8440c48be01d62a115e9abaf8424ea898832551d80b30383207954f",
        "source_detail_exposure_or_binding_operator_review_digest": "8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b",
        "source_detail_exposure_or_binding_candidate_digest": "e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23",
        "source_reentry_failure_diagnosis_digest": "7ca7cc9ac5bb92acd0b1ec5fbfc79b4dbcf4281144807f152b420e9cd67c54cb",
        "source_reentry_execution_blocked_digest": "e085828db499ec8998662b5a701dd5c47b402ca136f31b3ff867804c8b210a49",
        "source_reentry_execution_blocked_manifest_digest": "8bedff69537bdb105ac2825151c2dd3940b0016d79eab2b768c8201c0320eb99",
        "source_after_v2_planning_reentry_digest": "8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927",
        "source_module_grouping_source_recovery_results_review_digest": "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266",
        "source_module_grouping_source_recovery_execution_digest": "250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a",
        "source_module_grouping_source_recovery_detail_digest": "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5",
        "source_blocked_after_v2_execution_digest": "7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755",
        "source_after_v2_approval_digest": "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97",
        "source_results_review_v2_digest": "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86",
        "source_execution_v2_digest": "054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017",
        "source_module_grouping_digest": "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff",
        "retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
    }
    assert {key: success[key] for key in expected} == expected
    assert success["primary_failure_class"] == "COMMITTED_REENTRY_SOURCE_DETAIL_GAP"
    assert success["source_reentry_execution_blocked_reason"] == "RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT"


def test_success_preserves_counts_ordering_concentration_and_tiers(success: dict) -> None:
    rows = success["complete_29_row_module_grouping_detail_source"]
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert [row["module_path"] for row in rows[:5]] == service.TOP_FIVE_PATHS
    assert success["top_5_count_sum"] == 612
    assert success["top_10_count_sum"] == 1069
    assert success["priority_tier_1_count_sum"] == 612
    assert success["priority_tier_2_count_sum"] == 457
    assert success["priority_tier_3_count_sum"] == 335
    assert all(row["priority_order"] == index for index, row in enumerate(rows, 1))
    assert all(len(row["sample_nodeids_bounded"]) <= 5 for row in rows)
    assert all(row["sample_nodeids_bounded"] == sorted(row["sample_nodeids_bounded"]) for row in rows)
    assert all(row["source"] == service.ROW_SOURCE for row in rows)


def test_success_generates_only_research_outputs_and_requires_results_review(success: dict) -> None:
    assert success["planned_outputs_generated"] is True
    assert len(success["planned_outputs"]) == 12
    assert all(item["status"] == service.GENERATED_RESEARCH_ONLY for item in success["planned_outputs"])
    assert success["ready_for_detail_exposure_or_binding_results_review"] is True
    assert success["ready_for_after_v2_planning_reentry_with_complete_detail"] is False
    assert success["after_v2_planning_reentry_requires_detail_exposure_results_review"] is True
    assert success["recommended_next_task"] == service.SUCCESS_NEXT_TASK


def test_blocked_execution_generates_no_planned_outputs(blocked: dict) -> None:
    assert blocked["planned_outputs_generated"] is False
    assert len(blocked["planned_outputs"]) == 12
    assert all(item["status"] == service.BLOCKED_NOT_GENERATED for item in blocked["planned_outputs"])
    assert blocked["marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest"] is None
    assert blocked["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest"] is None
    assert blocked["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest"]


@pytest.mark.parametrize("artifact_fixture", ["success", "blocked"])
def test_execution_keeps_unsupported_and_operational_boundaries_closed(request, artifact_fixture: str) -> None:
    artifact = request.getfixturevalue(artifact_fixture)
    assert all(artifact[field] is False for field in service.FALSE_BOUNDARIES)
    assert artifact["predictive_usefulness"] == service.NOT_ACCEPTED
    assert artifact["profitability"] == service.NOT_ACCEPTED
    assert artifact["runtime_use"] == service.NOT_AUTHORIZED
    assert artifact["strategy_use"] == service.NOT_AUTHORIZED
    assert artifact["paper_trading"] == service.NOT_AUTHORIZED
    assert artifact["broker_execution"] == service.NOT_AUTHORIZED


@pytest.mark.parametrize("artifact_fixture", ["success", "blocked"])
def test_checklist_and_execution_digest_are_deterministic(request, artifact_fixture: str) -> None:
    artifact = request.getfixturevalue(artifact_fixture)
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(artifact)
    assert validation["passed_checks"] == validation["total_checks"]
    assert validation["failed_checks"] == 0
    assert validation["blocker_count"] == 0
    assert len(artifact["risk_controls"]) == 64
    assert artifact["marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest"] == service.marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest_v1(artifact)


def test_success_and_blocked_specialized_digests_are_deterministic(success: dict, blocked: dict) -> None:
    assert success["marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest"] == service.semantic_digest(success["complete_29_row_module_grouping_detail_source"])
    assert success["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest"] == service.semantic_digest(success["digest_manifest"])
    assert blocked["marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest"] == service.semantic_digest(blocked["blocked_manifest"])


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("execution_status", "OTHER"), ("execution_scope", "OTHER"),
        ("selected_detail_exposure_or_binding_package", "OTHER"),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_operator_review_digest", "0" * 64),
        ("source_detail_exposure_or_binding_candidate_digest", "0" * 64),
        ("source_reentry_failure_diagnosis_digest", "0" * 64), ("primary_failure_class", "OTHER"),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_reentry_execution_blocked_manifest_digest", "0" * 64),
        ("source_reentry_execution_blocked_reason", ""),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_results_review_v2_digest", "0" * 64), ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context", {}),
        ("recovered_module_grouping_source_summary", {}), ("top_module_summary", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068), ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_required_field(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES)
def test_validator_rejects_open_boundary(success: dict, field: str) -> None:
    changed = deepcopy(success)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("complete_29_row_detail_exposed", False), ("complete_29_row_detail_bound", False),
        ("complete_29_row_detail_source_identified", False), ("complete_29_row_module_grouping_detail_source", []),
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("largest_module_nodeid_counts", [1]), ("priority_tier_1_count_sum", 611),
        ("priority_tier_2_count_sum", 456), ("priority_tier_3_count_sum", 334),
        ("marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_module_grouping_detail_binding_digest", None),
        ("marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_digest_manifest_digest", None),
    ],
)
def test_validator_rejects_invalid_success_detail(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


def test_validator_rejects_success_sample_over_bound(success: dict) -> None:
    changed = deepcopy(success)
    changed["complete_29_row_module_grouping_detail_source"][0]["sample_nodeids_bounded"] = [str(i) for i in range(6)]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


@pytest.mark.parametrize(
    "field",
    ["blocked_reason", "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_binding_blocked_manifest_digest"],
)
def test_validator_rejects_blocked_artifact_without_disposition(blocked: dict, field: str) -> None:
    changed = deepcopy(blocked)
    changed[field] = None
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


def test_validator_rejects_missing_execution_digest(success: dict) -> None:
    changed = deepcopy(success)
    changed.pop("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryModuleGroupingDetailExposureOrBindingExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_v1(changed)


@pytest.mark.parametrize("artifact_fixture", ["success", "blocked"])
def test_markdown_includes_required_sections(request, artifact_fixture: str) -> None:
    artifact = request.getfixturevalue(artifact_fixture)
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_markdown_v1(artifact)
    for heading in (
        "Source Approval", "Source Operator Review and Candidate", "Source Reentry Failure Diagnosis",
        "Source Blocked Reentry Execution", "Source Recovery Results Review", "Retry Failure Context",
        "Execution Scope", "Complete 29-row Detail Source", "Detail Binding Result",
        "Top Module Concentration Preservation", "Priority Tier Enablement", "Unsupported Claims Boundary",
        "Success or Blocked Disposition", "Authority Boundaries", "Next Chain", "Next Gates",
        "Risk Controls", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
