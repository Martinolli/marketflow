from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_service
    as service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1()


def test_results_review_builds_offline_without_cache_or_execution_rerun(monkeypatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("results review crossed its committed-source boundary")

    monkeypatch.setattr(service.Path, "read_bytes", forbidden)
    monkeypatch.setattr(service.Path, "read_text", forbidden)
    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
        forbidden,
    )
    first = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1()
    second = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1()
    assert first == second
    assert first["cache_read_in_review"] is False
    assert first["materialization_execution_rerun_performed"] is False


def test_artifact_status_scope_and_source_execution_are_exact(review: dict) -> None:
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["source_materialization_execution_artifact_kind"] == service.source.SUCCESS_ARTIFACT_KIND
    assert review["source_materialization_execution_status"] == service.source.SUCCESS_STATUS
    assert review["source_materialization_execution_scope"] == service.source.EXECUTION_SCOPE
    assert review["selected_complete_29_row_materialization_package"] == service.source.SELECTED_COMPLETE_29_ROW_MATERIALIZATION_PACKAGE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_complete_29_row_materialization_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_complete_29_row_materialized_payload_digest", service.SOURCE_PAYLOAD_DIGEST),
        ("source_complete_29_row_materialization_digest_manifest_digest", service.SOURCE_DIGEST_MANIFEST_DIGEST),
        *list(service.SOURCE_BINDINGS.items()),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("top_5_count_sum", 612),
        ("top_5_percentage_of_failed_or_errored_nodeids", "43.58974359"),
        ("top_10_count_sum", 1069),
        ("top_10_percentage_of_failed_or_errored_nodeids", "76.13960114"),
        ("priority_tier_1_count_sum", 612),
        ("priority_tier_2_count_sum", 457),
        ("priority_tier_3_count_sum", 335),
    ],
)
def test_source_bindings_and_review_totals(review: dict, field: str, expected) -> None:
    assert review[field] == expected


def test_retry_and_source_execution_summaries_are_bound(review: dict) -> None:
    assert review["retry_failure_context"]["counts"] == {
        "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
    }
    summary = review["source_materialization_execution_summary"]
    assert summary["materialization_package_executed"] is True
    assert summary["complete_29_row_detail_materialized"] is True
    assert summary["complete_29_row_detail_exposed"] is True
    assert summary["complete_29_row_detail_bound"] is True
    assert summary["complete_29_row_detail_committed_source_created"] is True
    assert summary["cache_modified_in_source_execution"] is False


def test_source_bindings_match_committed_execution_lineage() -> None:
    committed_lineage = service.source._source_fields(None)
    for field, expected in service.SOURCE_BINDINGS.items():
        if field in committed_lineage:
            assert expected == committed_lineage[field]


def test_reviewed_cache_verification_is_copied_from_source_execution(review: dict) -> None:
    verification = review["reviewed_cache_verification_summary"]
    assert verification == {
        "reviewed_from_source_execution": True,
        "cache_read_in_review": False,
        "cache_modified_in_review": False,
        "lastfailed_sha256": service.source.REVIEWED_LASTFAILED_SHA256,
        "lastfailed_entry_count": 1404,
        "nodeids_sha256": service.source.REVIEWED_NODEIDS_SHA256,
        "nodeids_entry_count": 26288,
        "lastfailed_subset_of_nodeids": True,
        "all_source_execution_checks_verified": True,
    }


def test_complete_29_row_source_and_payload_integrity_are_reviewed(review: dict) -> None:
    source_review = review["complete_29_row_materialized_source_review"]
    rows = source_review["rows"]
    assert source_review["reviewed"] is True
    assert source_review["source_payload_digest"] == service.SOURCE_PAYLOAD_DIGEST
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["module_path"] for row in rows[:5]] == service.source.EXPECTED_TOP_FIVE_PATHS
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert all(0 < len(row["sample_nodeids_bounded"]) <= 5 for row in rows)
    assert all(row["sample_nodeids_bounded_count"] == len(row["sample_nodeids_bounded"]) for row in rows)
    assert all(row["source"] == service.source.ROW_SOURCE for row in rows)
    assert all(row["basis"] == service.source.ROW_BASIS for row in rows)
    assert all(row["confidence"] == service.source.ROW_CONFIDENCE for row in rows)
    assert all(row["unsupported_claims"] == service.source.UNSUPPORTED_ROW_CLAIMS for row in rows)
    assert review["materialized_payload_digest_review"]["verified"] is True
    assert review["materialized_payload_integrity_review"]["required_row_fields_present"] is True


def test_concentration_tiers_samples_and_claim_boundaries_are_reviewed(review: dict) -> None:
    top = review["top_module_concentration_review"]
    assert top["top_5_count_sum"] == 612
    assert top["top_10_count_sum"] == 1069
    assert top["top_5_module_paths"] == service.source.EXPECTED_TOP_FIVE_PATHS
    tiers = review["priority_tier_enablement_review"]
    assert [tiers[f"priority_tier_{index}_count_sum"] for index in (1, 2, 3)] == [612, 457, 335]
    assert review["bounded_samples_review"]["all_rows_have_bounded_samples"] is True
    assert review["bounded_samples_review"]["largest_sample_count"] == 5
    assert review["unsupported_claims_boundary_review"]["all_rows_preserve_boundary"] is True


def test_findings_outputs_recommendation_and_gates_are_exact(review: dict) -> None:
    assert review["review_findings"] == service.REVIEW_FINDINGS
    assert len(review["review_findings"]) == 12
    assert [item["output_id"] for item in review["review_outputs"]] == service.OUTPUT_IDS
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in review["review_outputs"])
    assert review["recommended_next_task"] == service.NEXT_TASK
    assert review["recommended_next_task_status"] == service.NEXT_TASK_STATUS
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert review["recommendation"]["reason"] == service.RECOMMENDATION_REASON
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_flags_are_true(review: dict, field: str) -> None:
    assert review[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_review_boundaries_are_false(review: dict, field: str) -> None:
    assert review[field] is False


def test_acceptance_runtime_and_trading_authorities_remain_closed(review: dict) -> None:
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    assert review["runtime_use"] == service.NOT_AUTHORIZED
    assert review["strategy_use"] == service.NOT_AUTHORIZED
    assert review["paper_trading"] == service.NOT_AUTHORIZED
    assert review["broker_execution"] == service.NOT_AUTHORIZED


def test_checklist_and_summary_pass(review: dict) -> None:
    assert len(review["checklist"]) == 119
    assert all(item["status"] == service.PASS for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == review["summary"]["passed_checks"] == 119
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_next_task"] == service.NEXT_TASK


def test_review_digests_are_deterministic(review: dict) -> None:
    second = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1()
    review_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"
    payload_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_review_digest"
    manifest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_manifest_digest"
    assert review[review_key] == second[review_key] == service._review_digest(review)
    assert review[payload_key] == second[payload_key]
    assert review[manifest_key] == second[manifest_key]


def test_validator_accepts_review(review: dict) -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(review)
    assert validation["artifact_kind"] == service.ARTIFACT_KIND
    assert validation["passed_checks"] == validation["total_checks"] == 119


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("review_status", "OTHER"), ("review_scope", "OTHER"),
        ("source_complete_29_row_materialization_execution_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_complete_29_row_materialization_digest_manifest_digest", "0" * 64),
        ("source_complete_29_row_materialization_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "0" * 64),
        ("primary_failure_class", "OTHER"),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", None),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("selected_complete_29_row_materialization_package", "OTHER"),
        ("risk_controls", []), ("review_outputs", []), ("next_chain", []),
    ],
)
def test_validator_rejects_changed_constants_and_governance(review: dict, field: str, value) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "cache_read_in_review", "cache_modified_in_review", "failure_error_separation_claimed",
        "first_failure_identified", "first_error_identified", "first_order_claim_made",
        "traceback_root_cause_claimed", "direct_code_remediation_recommended", "retry_success_claimed",
        "main_merge_readiness_claimed", "detail_exposure_or_binding_reattempt_created",
        "detail_exposure_or_binding_reattempt_executed", "after_v2_planning_execution_reentry_created",
        "after_v2_planning_execution_reentry_performed", "targeted_diagnostic_output_capture_candidate_created",
        "new_retry_candidate_created", "new_retry_executed", "new_retry_results_review_created",
        "main_merge_approval_created", "materialization_execution_rerun_performed",
        "source_recovery_rerun_performed", "retry_rerun_performed", "full_pytest_performed",
        "diagnostic_command_executed", "diagnostic_output_captured", "diagnostic_method_executed",
        "code_remediation_executed", "classification_execution_performed_in_review",
        "integration_execution_successful", "main_push_performed", "marketflow_outputs_committed",
        "pytest_cache_committed", "provider_requests_made_in_review",
    ],
)
def test_validator_rejects_opened_closed_boundary(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(changed)


def test_validator_rejects_row_integrity_mutations(review: dict) -> None:
    mutations = []
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"].pop(); mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["failed_or_errored_nodeid_count"] -= 1; mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["module_path"] = "tests/other.py"; mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["sample_nodeids_bounded"].append("extra"); mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["source"] = "OTHER"; mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["basis"] = "OTHER"; mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["confidence"] = "OTHER"; mutations.append(changed)
    changed = deepcopy(review); changed["complete_29_row_materialized_source_review"]["rows"][0]["unsupported_claims"] = []; mutations.append(changed)
    for changed in mutations:
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "execution_status", "execution_scope",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest",
        "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest",
        "selected_complete_29_row_materialization_package", "retry_failure_context",
        "complete_29_row_module_grouping_detail_source", "reviewed_cache_verification",
    ],
)
def test_builder_rejects_invalid_supplied_source_execution(field: str) -> None:
    execution = service._committed_source_execution()
    execution.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(source_execution=execution)


def test_writer_round_trips_in_temporary_directory(tmp_path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1.json").read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND
    assert receipt["review_digest"] == payload["marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_v1(tmp_path)


def test_markdown_contains_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_results_review_markdown_v1(review)
    for heading in (
        "Source Materialization Execution", "Source Approval and Operator Review",
        "Source Detail Exposure or Binding Failure Diagnosis", "Source Recovery Results Review",
        "Retry Failure Context", "Review Scope", "Reviewed Cache Verification from Source Execution",
        "Complete 29-row Materialized Source Review", "Payload Digest Review",
        "Top Module Concentration Review", "Priority Tier Enablement Review", "Bounded Samples Review",
        "Unsupported Claims Boundary", "Review Findings", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
