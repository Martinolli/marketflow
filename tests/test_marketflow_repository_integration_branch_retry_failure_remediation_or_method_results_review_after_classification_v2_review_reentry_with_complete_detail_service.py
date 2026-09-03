from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_service
    as service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1()


def test_results_review_builds_offline_without_source_execution(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("source execution must not run")

    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_with_complete_detail_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.source.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_reattempt_with_complete_source_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.source.review_source.source.review_source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1",
        forbidden,
    )
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1()
    assert artifact["created_offline"] is True
    assert artifact["cache_read_in_review"] is False
    assert artifact["planning_reentry_rerun_performed"] is False
    assert artifact["detail_binding_reattempt_rerun_performed"] is False


def test_explicit_committed_source_is_reviewed() -> None:
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
        source_execution=service._committed_source_execution()
    )
    assert artifact["source_planning_reentry_with_complete_detail_reviewed"] is True
    assert artifact["source_planning_reentry_digest_verified"] is True


def test_identity_status_scope_and_source_planning_execution(review: dict) -> None:
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["source_planning_reentry_artifact_kind"] == service.source.SUCCESS_ARTIFACT_KIND
    assert review["source_planning_reentry_status"] == service.source.SUCCESS_STATUS
    assert review["source_planning_reentry_scope"] == service.source.EXECUTION_SCOPE


def test_source_planning_digests_and_package_are_bound(review: dict) -> None:
    assert review["source_planning_reentry_execution_digest"] == service.SOURCE_EXECUTION_DIGEST
    assert review["source_prioritized_planning_digest"] == service.SOURCE_PLANNING_DIGEST
    assert review["source_planning_digest_manifest_digest"] == service.SOURCE_MANIFEST_DIGEST
    assert review["selected_after_v2_planning_package"] == service.source.SELECTED_AFTER_V2_PLANNING_PACKAGE
    assert {field: review[field] for field in service.SOURCE_BINDINGS} == service.SOURCE_BINDINGS


def test_retry_context_and_source_summary(review: dict) -> None:
    assert review["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert review["retry_failure_context"]["counts"] == {
        "passed": 24877, "failed": 1292, "errors": 112, "skipped": 7,
    }
    summary = review["source_planning_reentry_summary"]
    assert summary["complete_29_row_detail_used_for_planning"] is True
    assert summary["module_prioritization_generated"] is True
    assert summary["priority_tier_report_generated"] is True
    assert summary["top_module_concentration_report_generated"] is True
    assert summary["planning_buckets_generated"] is True
    assert summary["planned_outputs_generated"] is True


def test_complete_detail_planning_source_is_reviewed(review: dict) -> None:
    detail = review["reviewed_complete_29_row_detail_binding_summary"]
    rows = detail["rows"]
    assert detail["reviewed"] is True
    assert detail["used_for_planning"] is True
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == [136, 131, 122, 112, 111]
    assert [row["module_path"] for row in rows[:5]] == service.source.TOP_FIVE_PATHS


def test_planning_digest_review_is_verified(review: dict) -> None:
    digest_review = review["planning_digest_review"]
    assert digest_review["reviewed"] is True
    assert all(digest_review[key]["verified"] is True for key in (
        "execution_digest", "prioritized_planning_digest", "digest_manifest_digest"
    ))
    assert review["source_planning_reentry_digest_verified"] is True
    assert review["source_prioritized_planning_digest_verified"] is True
    assert review["source_planning_digest_manifest_verified"] is True


def test_priority_group_and_tier_reviews(review: dict) -> None:
    groups_review = review["prioritized_module_group_summary_review"]
    groups = groups_review["priority_groups"]
    assert groups_review["reviewed"] is True
    assert [group["priority_group"] for group in groups] == [
        "PRIORITY_1_TOP_5_MODULE_GROUPS", "PRIORITY_2_NEXT_5_MODULE_GROUPS",
        "PRIORITY_3_REMAINING_MODULE_GROUPS",
    ]
    assert [group["module_count"] for group in groups] == [5, 5, 19]
    assert [group["failed_or_errored_nodeid_count"] for group in groups] == [612, 457, 335]
    assert review["priority_tier_report_review"]["reviewed"] is True
    assert review["priority_tier_1_count_sum"] == 612
    assert review["priority_tier_2_count_sum"] == 457
    assert review["priority_tier_3_count_sum"] == 335


def test_concentration_and_planning_bucket_reviews(review: dict) -> None:
    concentration = review["top_module_concentration_report_review"]
    assert concentration["reviewed"] is True
    assert concentration["top_5_count_sum"] == 612
    assert concentration["top_10_count_sum"] == 1069
    buckets = review["planning_buckets_review"]
    assert buckets["reviewed"] is True
    assert buckets["bucket_count"] == 5
    assert buckets["all_planning_only_not_executed"] is True
    assert all(item["status"] == service.source.PLANNING_ONLY_NOT_EXECUTED for item in buckets["planning_buckets"])


@pytest.mark.parametrize(
    "field",
    [
        "diagnostic_capture_planning_review", "evidence_root_review_planning_review",
        "path_cwd_review_planning_review", "digest_drift_review_planning_review",
        "fixture_isolation_review_planning_review",
    ],
)
def test_each_planning_bucket_reviewed_without_execution(review: dict, field: str) -> None:
    item = review[field]
    assert item["reviewed"] is True
    assert item["planning_bucket"]["status"] == service.source.PLANNING_ONLY_NOT_EXECUTED
    assert item.get("executed", item.get("diagnostic_executed")) is False


def test_review_readiness_and_unsupported_claims(review: dict) -> None:
    assert review["ready_for_targeted_diagnostic_output_capture_candidate"] is True
    assert review["ready_for_retry_candidate"] is False
    assert review["targeted_diagnostic_output_capture_candidate_created"] is False
    unsupported = review["unsupported_claims_boundary_review"]
    assert unsupported["reviewed"] is True
    assert unsupported["required_unsupported_claims"] == service.source.UNSUPPORTED_ROW_CLAIMS
    assert all(unsupported[field] is False for field in (
        "failure_error_separation_claimed", "first_failure_identified", "first_error_identified",
        "traceback_root_cause_claimed", "direct_code_remediation_recommended",
        "retry_success_claimed", "main_merge_readiness_claimed",
    ))


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_all_required_review_flags_are_true(review: dict, field: str) -> None:
    assert review[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_all_closed_boundaries_remain_false(review: dict, field: str) -> None:
    assert review[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", service.NOT_ACCEPTED), ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED), ("strategy_use", service.NOT_AUTHORIZED),
        ("paper_trading", service.NOT_AUTHORIZED), ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_acceptance_and_runtime_boundaries(review: dict, field: str, expected: str) -> None:
    assert review[field] == expected


def test_findings_outputs_recommendation_and_governance(review: dict) -> None:
    assert review["review_findings"] == service.REVIEW_FINDINGS
    assert [item["output_id"] for item in review["review_outputs"]] == service.OUTPUT_IDS
    assert all(item["status"] == service.GENERATED_RESEARCH_ONLY for item in review["review_outputs"])
    assert review["recommended_next_task"] == service.NEXT_TASK
    assert review["recommended_next_task_status"] == service.NEXT_TASK_STATUS
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert review["reason"] == service.RECOMMENDATION_REASON
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_summary_and_digests_are_deterministic(review: dict) -> None:
    repeated = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1()
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"]
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert all(item["status"] == service.PASS for item in review["checklist"])
    for key in (service.REVIEW_DIGEST_KEY, service.PLANNING_REVIEW_DIGEST_KEY, service.REVIEW_MANIFEST_DIGEST_KEY):
        assert repeated[key] == review[key]


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(review)
    assert result["passed_checks"] == result["total_checks"]
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("review_status", "OTHER"), ("review_scope", "OTHER"),
        ("selected_after_v2_planning_package", "OTHER"),
        ("source_planning_reentry_execution_digest", "0" * 64),
        ("source_prioritized_planning_digest", "0" * 64),
        ("source_planning_digest_manifest_digest", "0" * 64),
        ("source_detail_binding_reattempt_results_review_digest", "0" * 64),
        ("source_complete_29_row_binding_review_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_complete_29_row_materialization_results_review_digest", "0" * 64),
        ("source_complete_29_row_materialized_payload_digest", "0" * 64),
        ("source_detail_exposure_or_binding_approval_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context", {}), ("source_planning_reentry_status", "OTHER"),
        ("review_outputs", []), ("recommendation", {}), ("recommended_action", "OTHER"),
        ("next_chain", []), ("next_gates", []), ("risk_controls", []),
        (service.REVIEW_DIGEST_KEY, None), (service.PLANNING_REVIEW_DIGEST_KEY, None),
        (service.REVIEW_MANIFEST_DIGEST_KEY, None),
    ],
)
def test_validator_rejects_changed_required_content(review: dict, field: str, value: object) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_required_review_flag(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_opened_boundary(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_open_acceptance_or_authority(review: dict, field: str, value: str) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("largest_module_nodeid_counts", [1]), ("top_five_module_paths", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("priority_tier_1_count_sum", 611), ("priority_tier_2_count_sum", 456),
        ("priority_tier_3_count_sum", 334), ("planning_digest_review", {}),
        ("prioritized_module_group_summary_review", {}), ("priority_tier_report_review", {}),
        ("top_module_concentration_report_review", {}), ("planning_buckets_review", {}),
        ("diagnostic_capture_planning_review", {}), ("unsupported_claims_boundary_review", {}),
    ],
)
def test_validator_rejects_changed_review_facts(review: dict, field: str, value: object) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


def test_validator_rejects_changed_reviewed_rows(review: dict) -> None:
    changed = deepcopy(review)
    changed["reviewed_complete_29_row_detail_binding_summary"]["rows"].pop()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (service.source.EXECUTION_DIGEST_KEY, "0" * 64),
        (service.source.PLANNING_DIGEST_KEY, "0" * 64),
        (service.source.MANIFEST_DIGEST_KEY, "0" * 64),
        ("complete_29_row_detail_used_for_planning", False),
        ("module_prioritization_generated", False), ("priority_tier_report_generated", False),
        ("top_module_concentration_report_generated", False), ("planning_buckets_generated", False),
        ("planned_outputs_generated", False), ("complete_29_row_detail_binding_source", []),
        ("prioritized_module_group_summary", []), ("outputs_generated", []),
    ],
)
def test_builder_rejects_changed_source_execution(field: str, value: object) -> None:
    execution = service._committed_source_execution()
    execution[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(
            source_execution=execution
        )


def test_writer_round_trips_in_isolated_directory(tmp_path: Path, review: dict) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(tmp_path)
    payload = json.loads(Path(receipt["path"]).read_text(encoding="utf-8"))
    assert payload == review
    assert receipt["review_digest"] == review[service.REVIEW_DIGEST_KEY]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_directory(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationMethodResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1(tmp_path / protected)


def test_markdown_contains_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_markdown_v1(review)
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Results Review After Classification v2 Review Reentry with Complete Detail v1",
        "## Source Planning Reentry with Complete Detail", "## Source Detail Binding Reattempt Results Review",
        "## Source Materialization Results Review", "## Source Detail Exposure or Binding Approval",
        "## Source Prior Blocked Planning Reentry", "## Source Recovery Results Review", "## Retry Failure Context",
        "## Review Scope", "## Reviewed Complete 29-row Planning Source", "## Planning Digest Review",
        "## Prioritized Module Group Summary Review", "## Priority Tier Report Review",
        "## Top Module Concentration Review", "## Planning Buckets Review",
        "## Diagnostic Capture Planning Review", "## Unsupported Claims Boundary", "## Review Findings",
        "## Recommendation", "## Next Chain", "## Next Gates", "## Risk Controls",
        "## Authority Boundaries", "## Checklist Summary", "## Guardrails",
    ]
    assert all(section in markdown for section in required)


def test_public_exports_are_available() -> None:
    import marketflow.services as exports

    assert exports.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_WITH_COMPLETE_DETAIL_V1 == service.ARTIFACT_KIND
    assert exports.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1 is service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_classification_v2_review_reentry_with_complete_detail_v1
