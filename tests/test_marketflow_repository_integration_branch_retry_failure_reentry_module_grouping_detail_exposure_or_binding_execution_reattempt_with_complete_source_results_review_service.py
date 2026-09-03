from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_service
    as service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1()


def test_results_review_builds_offline_without_source_executors(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("source execution must not run")

    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.source.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
        forbidden,
    )
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1()
    assert artifact["created_offline"] is True
    assert artifact["cache_read_in_review"] is False
    assert artifact["detail_binding_reattempt_rerun_performed"] is False
    assert artifact["materialization_execution_rerun_performed"] is False
    assert artifact["source_recovery_rerun_performed"] is False


def test_artifact_identity_status_scope_and_source_reattempt(review: dict) -> None:
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["source_detail_binding_reattempt_artifact_kind"] == service.source.SUCCESS_ARTIFACT_KIND
    assert review["source_detail_binding_reattempt_status"] == service.source.SUCCESS_STATUS
    assert review["source_detail_binding_reattempt_scope"] == service.source.EXECUTION_SCOPE
    assert review["selected_detail_exposure_or_binding_package"] == service.SELECTED_DETAIL_EXPOSURE_OR_BINDING_PACKAGE


def test_source_reattempt_digests_are_bound(review: dict) -> None:
    assert review["source_detail_binding_reattempt_digest"] == service.SOURCE_REATTEMPT_DIGEST
    assert review["source_complete_29_row_binding_digest"] == service.SOURCE_BINDING_DIGEST
    assert review["source_detail_binding_reattempt_digest_manifest_digest"] == service.SOURCE_REATTEMPT_MANIFEST_DIGEST


def test_all_prior_source_digests_are_bound(review: dict) -> None:
    assert {field: review[field] for field in service.SOURCE_BINDINGS} == service.SOURCE_BINDINGS
    assert review["source_complete_29_row_materialization_results_review_digest"] == service.source.SOURCE_RESULTS_REVIEW_DIGEST
    assert review["source_complete_29_row_materialized_payload_review_digest"] == service.source.SOURCE_PAYLOAD_REVIEW_DIGEST
    assert review["source_complete_29_row_materialization_results_review_manifest_digest"] == service.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST
    assert review["source_complete_29_row_materialization_execution_digest"] == service.source.SOURCE_MATERIALIZATION_EXECUTION_DIGEST
    assert review["source_complete_29_row_materialized_payload_digest"] == service.source.SOURCE_MATERIALIZED_PAYLOAD_DIGEST
    assert review["source_complete_29_row_materialization_digest_manifest_digest"] == service.source.SOURCE_MATERIALIZATION_DIGEST_MANIFEST_DIGEST


def test_retry_context_and_source_success_are_bound(review: dict) -> None:
    assert review["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert review["retry_failure_context"]["counts"] == {
        "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
    }
    summary = review["source_detail_binding_reattempt_summary"]
    assert summary["used_reviewed_complete_29_row_materialized_source"] is True
    assert summary["complete_29_row_detail_exposed"] is True
    assert summary["complete_29_row_detail_bound"] is True
    assert summary["complete_29_row_detail_source_identified"] is True
    assert summary["cache_read_in_reattempt"] is False


def test_binding_digest_and_manifest_are_verified(review: dict) -> None:
    assert review["source_detail_binding_reattempt_digest_verified"] is True
    assert review["source_detail_binding_digest_verified"] is True
    assert review["source_detail_binding_digest_manifest_verified"] is True
    assert review["binding_digest_review"]["verified"] is True
    assert review["binding_digest_review"]["actual_from_committed_rows"] == service.SOURCE_BINDING_DIGEST


def test_complete_29_row_binding_integrity_is_reviewed(review: dict) -> None:
    rows = review["complete_29_row_detail_binding_source_review"]["rows"]
    assert review["reviewed_complete_29_row_detail_binding_source"] is True
    assert review["complete_29_row_detail_binding_integrity_reviewed"] is True
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert [row["module_path"] for row in rows[:5]] == service.source.review_source.source.EXPECTED_TOP_FIVE_PATHS
    assert all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows)
    assert all(row["sample_nodeids_bounded_count"] == len(row["sample_nodeids_bounded"]) for row in rows)
    assert all(row["source"] == service.source.BINDING_ROW_SOURCE for row in rows)
    assert all(row["basis"] == service.source.BINDING_ROW_BASIS for row in rows)
    assert all(row["confidence"] == service.source.BINDING_ROW_CONFIDENCE for row in rows)
    assert all(row["unsupported_claims"] == service.source.review_source.source.UNSUPPORTED_ROW_CLAIMS for row in rows)


def test_concentration_tiers_samples_and_boundaries_are_reviewed(review: dict) -> None:
    assert review["top_module_concentration_reviewed"] is True
    assert review["priority_tier_enablement_reviewed"] is True
    assert review["bounded_samples_reviewed"] is True
    assert review["unsupported_claims_boundary_reviewed"] is True
    assert review["top_5_count_sum"] == 612
    assert review["top_10_count_sum"] == 1069
    assert review["priority_tier_1_count_sum"] == 612
    assert review["priority_tier_2_count_sum"] == 457
    assert review["priority_tier_3_count_sum"] == 335
    assert review["bounded_samples_review"]["largest_sample_count"] <= 5
    assert review["unsupported_claims_boundary_review"]["all_rows_preserve_boundary"] is True


def test_review_is_ready_only_for_separate_planning_reentry(review: dict) -> None:
    assert review["detail_exposure_or_binding_reattempt_results_review_created"] is True
    assert review["detail_exposure_or_binding_reattempt_results_review_ready"] is True
    assert review["ready_for_after_v2_planning_reentry_with_complete_detail"] is True
    assert review["ready_for_retry_candidate"] is False
    assert review["recommended_next_task"] == service.NEXT_TASK
    assert review["recommended_next_task_status"] == service.NEXT_TASK_STATUS
    assert review["recommended_action"] == service.RECOMMENDED_ACTION


def test_all_closed_boundaries_remain_closed(review: dict) -> None:
    assert all(review[field] is False for field in service.FALSE_FIELDS)
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    assert review["runtime_use"] == service.NOT_AUTHORIZED
    assert review["strategy_use"] == service.NOT_AUTHORIZED
    assert review["paper_trading"] == service.NOT_AUTHORIZED
    assert review["broker_execution"] == service.NOT_AUTHORIZED


def test_findings_outputs_next_chain_and_risk_controls(review: dict) -> None:
    assert review["review_findings"] == service.REVIEW_FINDINGS
    assert [item["output_id"] for item in review["review_outputs"]] == service.OUTPUT_IDS
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in review["review_outputs"])
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_digests_are_deterministic(review: dict) -> None:
    repeated = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1()
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(review)
    assert validation["passed_checks"] == validation["total_checks"]
    assert validation["failed_checks"] == 0
    assert validation["blocker_count"] == 0
    assert all(item["status"] == service.PASS for item in review["checklist"])
    assert repeated[service.REVIEW_DIGEST_KEY] == review[service.REVIEW_DIGEST_KEY]
    assert repeated[service.BINDING_REVIEW_DIGEST_KEY] == review[service.BINDING_REVIEW_DIGEST_KEY]
    assert repeated[service.REVIEW_MANIFEST_DIGEST_KEY] == review[service.REVIEW_MANIFEST_DIGEST_KEY]


def test_writer_round_trips_to_isolated_directory(tmp_path: Path, review: dict) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(tmp_path)
    payload = json.loads(Path(receipt["path"]).read_text(encoding="utf-8"))
    assert payload == review
    assert receipt["review_digest"] == review[service.REVIEW_DIGEST_KEY]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(tmp_path)


@pytest.mark.parametrize("protected_name", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_output_directories(tmp_path: Path, protected_name: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(tmp_path / protected_name)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("review_status", "OTHER"), ("review_scope", "OTHER"),
        ("source_detail_binding_reattempt_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_detail_binding_reattempt_digest_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_review_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_execution_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_complete_29_row_materialization_digest_manifest_digest", "0" * 64),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context", {}),
        ("selected_detail_exposure_or_binding_package", "OTHER"),
        ("source_detail_binding_reattempt_summary", {}),
        ("binding_digest_review", {}),
        ("review_outputs", []), ("next_chain", []), ("risk_controls", []),
        (service.REVIEW_DIGEST_KEY, None), (service.BINDING_REVIEW_DIGEST_KEY, None),
        (service.REVIEW_MANIFEST_DIGEST_KEY, None),
    ],
)
def test_validator_rejects_changed_required_content(review: dict, field: str, value: object) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("complete_29_row_detail_binding_source_review", {}),
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("largest_module_nodeid_counts", [1]), ("top_five_module_paths", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("priority_tier_1_count_sum", 611), ("priority_tier_2_count_sum", 456),
        ("priority_tier_3_count_sum", 334), ("bounded_samples_review", {}),
        ("unsupported_claims_boundary_review", {}),
    ],
)
def test_validator_rejects_invalid_binding_review_summary(review: dict, field: str, value: object) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(changed)


@pytest.mark.parametrize("mutation", ["row-count", "sample-missing", "sample-over-bound", "source", "basis", "confidence", "unsupported"])
def test_validator_rejects_invalid_binding_rows(review: dict, mutation: str) -> None:
    changed = deepcopy(review)
    rows = changed["complete_29_row_detail_binding_source_review"]["rows"]
    if mutation == "row-count":
        rows.pop()
    elif mutation == "sample-missing":
        rows[0]["sample_nodeids_bounded"] = []
    elif mutation == "sample-over-bound":
        rows[0]["sample_nodeids_bounded"] = [f"node::{index}" for index in range(6)]
    elif mutation == "source":
        rows[0]["source"] = "OTHER"
    elif mutation == "basis":
        rows[0]["basis"] = "OTHER"
    elif mutation == "confidence":
        rows[0]["confidence"] = "OTHER"
    else:
        rows[0]["unsupported_claims"] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_closed_boundary(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("ready_for_after_v2_planning_reentry_with_complete_detail", False),
        ("ready_for_retry_candidate", True),
    ],
)
def test_validator_rejects_acceptance_or_readiness_boundary(review: dict, field: str, value: object) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(changed)


def test_source_input_tampering_is_rejected() -> None:
    execution = service._committed_source_reattempt()
    execution["complete_29_row_module_grouping_detail_binding_source"].pop()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryDetailBindingReattemptResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_v1(source_reattempt=execution)


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_results_review_markdown_v1(review)
    sections = [
        "Source Detail Binding Reattempt", "Source Materialization Results Review",
        "Source Materialization Execution", "Source Detail Exposure or Binding Approval",
        "Source Prior Blocked Detail Exposure or Binding Execution", "Source Reentry Failure Diagnosis",
        "Source Recovery Results Review", "Retry Failure Context", "Review Scope",
        "Reviewed Complete 29-row Detail Binding Source", "Binding Digest Review",
        "Top Module Concentration Review", "Priority Tier Enablement Review", "Bounded Samples Review",
        "Unsupported Claims Boundary", "Review Findings", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in sections)
