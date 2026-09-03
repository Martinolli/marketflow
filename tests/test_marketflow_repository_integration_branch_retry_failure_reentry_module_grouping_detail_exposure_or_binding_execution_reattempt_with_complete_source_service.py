from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_service
    as service,
)


TIMESTAMP = "2026-08-23T00:00:00Z"
EXECUTION_DIGEST_KEY = (
    "marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_"
    "exposure_or_binding_execution_reattempt_with_complete_source_digest"
)
BINDING_DIGEST_KEY = (
    "marketflow_repository_integration_branch_retry_failure_reentry_complete_29_row_"
    "module_grouping_detail_binding_after_materialization_digest"
)
MANIFEST_DIGEST_KEY = (
    "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_"
    "binding_reattempt_with_complete_source_digest_manifest_digest"
)
BLOCKED_MANIFEST_DIGEST_KEY = (
    "marketflow_repository_integration_branch_retry_failure_reentry_detail_exposure_or_"
    "binding_reattempt_with_complete_source_blocked_manifest_digest"
)


def _committed_rows() -> list[dict]:
    return service.review_source.source.committed_complete_29_row_module_grouping_detail_source_v1()


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        run_timestamp_utc=TIMESTAMP
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        complete_detail_source=[], run_timestamp_utc=TIMESTAMP
    )


def test_success_reattempt_builds_from_explicit_deterministic_complete_source() -> None:
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        complete_detail_source=_committed_rows(), run_timestamp_utc=TIMESTAMP
    )
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert artifact["complete_29_row_detail_bound"] is True


def test_success_reattempt_builds_from_committed_reviewed_source(success: dict) -> None:
    assert success["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert success["execution_status"] == service.SUCCESS_STATUS
    assert success["execution_scope"] == service.EXECUTION_SCOPE
    assert success["selected_detail_exposure_or_binding_package"] == service.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE
    assert success["used_reviewed_complete_29_row_materialized_source"] is True
    assert success["used_committed_source_evidence_only"] is True


def test_default_execution_does_not_call_review_builder_or_source_execution(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("an earlier execution or review builder must not run")

    monkeypatch.setattr(
        service.review_source,
        "build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
        forbidden,
    )
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        run_timestamp_utc=TIMESTAMP
    )
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert artifact["cache_read_in_reattempt"] is False
    assert artifact["materialization_execution_rerun_performed"] is False
    assert artifact["source_recovery_rerun_performed"] is False


def _remove_row(rows: list[dict]) -> None:
    rows.pop()


def _change_total(rows: list[dict]) -> None:
    rows[10]["failed_or_errored_nodeid_count"] -= 1


def _change_top_five_count(rows: list[dict]) -> None:
    rows[0]["failed_or_errored_nodeid_count"] -= 1


def _change_top_five_path(rows: list[dict]) -> None:
    rows[0]["module_path"] = "tests/test_not_the_reviewed_top_module.py"


def _change_top_ten_sum(rows: list[dict]) -> None:
    rows[7]["failed_or_errored_nodeid_count"] -= 1


def _change_tier_sum(rows: list[dict]) -> None:
    rows[12]["failed_or_errored_nodeid_count"] -= 1


def _exceed_sample_bound(rows: list[dict]) -> None:
    rows[0]["sample_nodeids_bounded"] = [f"tests/test_x.py::test_{index}" for index in range(6)]
    rows[0]["sample_nodeids_bounded_count"] = 6


@pytest.mark.parametrize(
    "mutator",
    [
        pytest.param(_remove_row, id="row-count-less-than-29"),
        pytest.param(_change_total, id="total-not-1404"),
        pytest.param(_change_top_five_count, id="top-five-counts"),
        pytest.param(_change_top_five_path, id="top-five-paths"),
        pytest.param(_change_top_ten_sum, id="top-ten-sum"),
        pytest.param(_change_tier_sum, id="tier-sums"),
        pytest.param(_exceed_sample_bound, id="bounded-samples"),
    ],
)
def test_incomplete_or_inconsistent_complete_source_blocks(mutator) -> None:
    rows = _committed_rows()
    mutator(rows)
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        complete_detail_source=rows, run_timestamp_utc=TIMESTAMP
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["execution_status"] == service.BLOCKED_STATUS
    assert artifact["complete_29_row_detail_bound"] is False
    assert artifact["blocked_reason"]


def test_missing_complete_source_builds_blocked_artifact(blocked: dict) -> None:
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert blocked["execution_scope"] == service.EXECUTION_SCOPE
    assert "REVIEWED_COMMITTED_COMPLETE_29_ROW_SOURCE_UNAVAILABLE" in blocked["blocked_reason"]
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK
    assert blocked[BLOCKED_MANIFEST_DIGEST_KEY]


def test_invalid_source_review_blocks() -> None:
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        source_materialization_results_review={},
        complete_detail_source=_committed_rows(),
        run_timestamp_utc=TIMESTAMP,
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert "SOURCE_REVIEW_ARTIFACT_KIND_MISMATCH_OR_MISSING" in artifact["blocked_reason"]


def test_success_binds_required_source_chain(success: dict) -> None:
    assert {field: success[field] for field in service.SOURCE_BINDINGS} == service.SOURCE_BINDINGS
    assert success["source_complete_29_row_materialization_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert success["source_complete_29_row_materialized_payload_review_digest"] == service.SOURCE_PAYLOAD_REVIEW_DIGEST
    assert success["source_complete_29_row_materialization_results_review_manifest_digest"] == service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST
    assert success["source_complete_29_row_materialization_execution_digest"] == service.SOURCE_MATERIALIZATION_EXECUTION_DIGEST
    assert success["source_complete_29_row_materialized_payload_digest"] == service.SOURCE_MATERIALIZED_PAYLOAD_DIGEST
    assert success["source_complete_29_row_materialization_digest_manifest_digest"] == service.SOURCE_MATERIALIZATION_DIGEST_MANIFEST_DIGEST
    assert success["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert success["retry_failure_context"]["counts"] == {
        "passed": 24877,
        "failed": 1292,
        "errors": 112,
        "skipped": 7,
    }


def test_success_exposes_exact_ordered_29_row_binding(success: dict) -> None:
    rows = success["complete_29_row_module_grouping_detail_binding_source"]
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert [row["module_path"] for row in rows[:5]] == service.review_source.source.EXPECTED_TOP_FIVE_PATHS
    assert rows == sorted(rows, key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"]))
    assert all(row["source"] == service.BINDING_ROW_SOURCE for row in rows)
    assert all(row["basis"] == service.BINDING_ROW_BASIS for row in rows)
    assert all(row["confidence"] == service.BINDING_ROW_CONFIDENCE for row in rows)
    assert all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows)
    assert all(row["sample_nodeids_bounded"] == sorted(row["sample_nodeids_bounded"]) for row in rows)


def test_success_preserves_concentration_and_enables_priority_tiers(success: dict) -> None:
    assert success["top_5_count_sum"] == 612
    assert success["top_5_percentage_of_failed_or_errored_nodeids"] == "43.58974359"
    assert success["top_10_count_sum"] == 1069
    assert success["top_10_percentage_of_failed_or_errored_nodeids"] == "76.13960114"
    assert success["priority_tier_1_count_sum"] == 612
    assert success["priority_tier_2_count_sum"] == 457
    assert success["priority_tier_3_count_sum"] == 335
    assert success["priority_tier_1_percentage_of_failed_or_errored_nodeids"] == "43.58974359"
    assert success["priority_tier_2_percentage_of_failed_or_errored_nodeids"] == "32.54985755"
    assert success["priority_tier_3_percentage_of_failed_or_errored_nodeids"] == "23.86039886"


def test_success_generates_required_outputs_and_next_chain(success: dict) -> None:
    assert success["planned_outputs_generated"] is True
    assert [item["output_id"] for item in success["outputs_generated"]] == service.OUTPUT_IDS
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in success["outputs_generated"])
    assert success["ready_for_detail_exposure_or_binding_results_review"] is True
    assert success["ready_for_after_v2_planning_reentry_with_complete_detail"] is False
    assert success["after_v2_planning_reentry_requires_detail_exposure_or_binding_results_review"] is True
    assert success["recommended_next_task"] == service.SUCCESS_NEXT_TASK


@pytest.mark.parametrize("artifact_fixture", ["success", "blocked"])
def test_checklist_passes_for_success_and_blocked(request, artifact_fixture: str) -> None:
    artifact = request.getfixturevalue(artifact_fixture)
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(artifact)
    assert validation["passed_checks"] == validation["total_checks"]
    assert validation["failed_checks"] == 0
    assert validation["blocker_count"] == 0
    assert all(item["status"] == service.PASS for item in artifact["checklist"])


@pytest.mark.parametrize("artifact_fixture", ["success", "blocked"])
def test_authority_and_unsupported_claim_boundaries_remain_closed(request, artifact_fixture: str) -> None:
    artifact = request.getfixturevalue(artifact_fixture)
    assert all(artifact[field] is False for field in service.FALSE_FIELDS)
    assert artifact["predictive_usefulness"] == service.NOT_ACCEPTED
    assert artifact["profitability"] == service.NOT_ACCEPTED
    assert artifact["runtime_use"] == service.NOT_AUTHORIZED
    assert artifact["strategy_use"] == service.NOT_AUTHORIZED
    assert artifact["paper_trading"] == service.NOT_AUTHORIZED
    assert artifact["broker_execution"] == service.NOT_AUTHORIZED
    assert artifact["risk_controls"] == service.RISK_CONTROLS


def test_success_and_blocked_digests_are_deterministic(success: dict, blocked: dict) -> None:
    repeated_success = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        run_timestamp_utc=TIMESTAMP
    )
    repeated_blocked = service.execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(
        complete_detail_source=[], run_timestamp_utc=TIMESTAMP
    )
    assert repeated_success[EXECUTION_DIGEST_KEY] == success[EXECUTION_DIGEST_KEY]
    assert repeated_success[BINDING_DIGEST_KEY] == success[BINDING_DIGEST_KEY]
    assert repeated_success[MANIFEST_DIGEST_KEY] == success[MANIFEST_DIGEST_KEY]
    assert repeated_blocked[EXECUTION_DIGEST_KEY] == blocked[EXECUTION_DIGEST_KEY]
    assert repeated_blocked[BLOCKED_MANIFEST_DIGEST_KEY] == blocked[BLOCKED_MANIFEST_DIGEST_KEY]
    assert success[BINDING_DIGEST_KEY] == service.semantic_digest(success["complete_29_row_module_grouping_detail_binding_source"])
    assert success[MANIFEST_DIGEST_KEY] == service.semantic_digest(success["digest_manifest"])


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"),
        ("execution_status", "OTHER"),
        ("execution_scope", "OTHER"),
        ("selected_detail_exposure_or_binding_package", "OTHER"),
        ("source_complete_29_row_materialization_results_review_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_review_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_execution_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_complete_29_row_materialization_digest_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_approval_digest", "0" * 64),
        ("source_complete_29_row_materialization_operator_review_digest", "0" * 64),
        ("source_complete_29_row_materialization_candidate_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "0" * 64),
        ("primary_failure_class", "OTHER"),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_operator_review_digest", "0" * 64),
        ("source_detail_exposure_or_binding_candidate_digest", "0" * 64),
        ("source_reentry_failure_diagnosis_digest", "0" * 64),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context", {}),
        ("risk_controls", []),
        (EXECUTION_DIGEST_KEY, None),
    ],
)
def test_validator_rejects_changed_required_field(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("complete_29_row_module_grouping_detail_binding_source", []),
        ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403),
        ("largest_module_nodeid_counts", [1]),
        ("top_five_module_paths", []),
        ("top_5_count_sum", 611),
        ("top_10_count_sum", 1068),
        ("priority_tier_1_count_sum", 611),
        ("priority_tier_2_count_sum", 456),
        ("priority_tier_3_count_sum", 334),
        (BINDING_DIGEST_KEY, "0" * 64),
        (MANIFEST_DIGEST_KEY, "0" * 64),
        ("complete_29_row_detail_exposed", False),
        ("complete_29_row_detail_bound", False),
        ("complete_29_row_detail_source_identified", False),
    ],
)
def test_validator_rejects_invalid_success_binding(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_boundary(success: dict, field: str) -> None:
    changed = deepcopy(success)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_acceptance_or_runtime_authority(success: dict, field: str, value: str) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


@pytest.mark.parametrize("sample_value", [[], [f"node::{index}" for index in range(6)]])
def test_validator_rejects_missing_or_over_bound_samples(success: dict, sample_value: list[str]) -> None:
    changed = deepcopy(success)
    changed["complete_29_row_module_grouping_detail_binding_source"][0]["sample_nodeids_bounded"] = sample_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("blocked_reason", ""),
        (BLOCKED_MANIFEST_DIGEST_KEY, "0" * 64),
        ("complete_29_row_detail_exposed", True),
    ],
)
def test_validator_rejects_invalid_blocked_artifact(blocked: dict, field: str, value: object) -> None:
    changed = deepcopy(blocked)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1(changed)


def test_markdown_includes_required_sections(success: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_markdown_v1(success)
    required_sections = [
        "Source Materialization Results Review",
        "Source Materialization Execution",
        "Source Detail Exposure or Binding Approval",
        "Source Prior Blocked Detail Exposure or Binding Execution",
        "Source Reentry Failure Diagnosis",
        "Source Recovery Results Review",
        "Retry Failure Context",
        "Execution Scope",
        "Reviewed Complete 29-row Source",
        "Detail Binding Reattempt Result",
        "Payload Digest Binding",
        "Top Module Concentration Preservation",
        "Priority Tier Enablement",
        "Unsupported Claims Boundary",
        "Authority Boundaries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required_sections)
