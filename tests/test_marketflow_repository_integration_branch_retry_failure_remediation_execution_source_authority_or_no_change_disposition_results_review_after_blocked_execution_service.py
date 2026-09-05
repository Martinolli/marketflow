from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1()


def test_results_review_builds_offline_without_invoking_source_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source execution must not be invoked")

    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1",
        forbidden,
    )
    review = _build()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


def test_artifact_status_scope_and_selected_package_are_exact() -> None:
    review = _build()
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["selected_source_authority_or_no_change_disposition_package"] == service.SELECTED_PACKAGE


def test_source_execution_identity_and_digests_are_bound() -> None:
    review = _build()
    assert review["source_execution_commit"] == service.SOURCE_EXECUTION_COMMIT
    assert review["source_execution_artifact_kind"] == service.SOURCE_EXECUTION_ARTIFACT_KIND
    assert review["source_execution_status"] == service.SOURCE_EXECUTION_STATUS
    assert review["source_execution_scope"] == service.SOURCE_EXECUTION_SCOPE
    assert review["source_execution_digest"] == service.SOURCE_EXECUTION_DIGEST
    assert review["source_authority_enrichment_plan_digest"] == service.SOURCE_ENRICHMENT_PLAN_DIGEST
    assert review["source_missing_authority_inventory_digest"] == service.SOURCE_MISSING_AUTHORITY_INVENTORY_DIGEST
    assert review["source_workstream_authority_mapping_digest"] == service.SOURCE_WORKSTREAM_AUTHORITY_MAPPING_DIGEST
    assert review["source_execution_manifest_digest"] == service.SOURCE_EXECUTION_MANIFEST_DIGEST


@pytest.mark.parametrize(
    "field",
    [
        "source_approval_commit",
        "source_approval_digest",
        "source_operator_review_commit",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest",
        "source_candidate_commit",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest",
        "source_failure_diagnosis_commit",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit",
        "source_blocked_reason",
        "source_blocked_manifest_digest",
        "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest",
        "source_workstream_mapping_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest",
        "source_workstream_mapping_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest",
        "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest",
        "source_recovery_detail_digest",
        "source_module_grouping_digest",
        "source_staged_inventory_digest",
    ],
)
def test_historical_source_bindings_are_preserved(field: str) -> None:
    review = _build()
    assert review[field] == service.source.SOURCE_BINDINGS[field]


def test_failure_classification_retry_context_and_diagnostic_metadata_are_bound() -> None:
    review = _build()
    assert review["primary_failure_class"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert len(review["secondary_failure_classes"]) == 4
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["failed_or_errored_nodeids_count"] == 1404
    assert review["module_summary_module_count"] == 29
    assert review["priority_1_total_nodeids"] == 612
    assert review["top_10_count_sum"] == 1069
    assert review["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert review["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert review["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert review["diagnostic_capture_evidence_summary"]["diagnostic_only"] is True


def test_priority_1_validation_remains_non_retry_evidence() -> None:
    review = _build()
    summary = review["priority1_validation_summary"]
    assert summary["pre_change_passed_count"] == 675
    assert summary["post_change_passed_count"] == 675
    assert summary["post_change_passed"] is True
    assert summary["not_retry_evidence"] is True


def test_four_families_and_four_workstreams_are_reviewed() -> None:
    review = _build()
    assert review["observable_failure_family_count"] == 4
    assert review["total_observable_evidence_items"] == 188
    assert {item["family_id"] for item in review["reviewed_observable_failure_families"]} == {
        "assertion_or_value_mismatch",
        "digest_or_hash_mismatch",
        "fixture_or_test_isolation_issue",
        "missing_or_unexpected_field",
    }
    assert all(item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    assert review["source_workstream_count"] == 4
    assert all(item["direct_change_authorized"] is False for item in review["reviewed_workstreams"])


def test_missing_authority_inventory_has_four_sections_and_thirty_missing_items() -> None:
    review = _build()
    inventory = review["missing_authority_inventory_review"]
    assert inventory["section_count"] == 4
    assert inventory["item_count"] == 30
    assert sum(len(item["missing_authority_items"]) for item in inventory["sections"]) == 30
    assert all(item["authority_status"] == "MISSING_NOT_ACQUIRED" for item in inventory["sections"])
    assert all(item["direct_change_authorized"] is False for item in inventory["sections"])


def test_mapping_and_requirement_counts_are_reviewed_only() -> None:
    review = _build()
    mapping = review["workstream_to_missing_authority_mapping_review"]
    assert mapping["mapping_count"] == 4
    assert all(item["mapping_status"] == "PLANNED_NOT_EXECUTED" for item in mapping["mappings"])
    assert all(item["source_authority_acquired"] is False for item in mapping["mappings"])
    assert len(review["source_evidence_requirements_review"]) == 4
    assert len(review["no_change_disposition_input_requirements_review"]) == 7
    assert len(review["alternate_diagnostic_input_requirements_review"]) == 8
    assert len(review["retry_basis_requirements_review"]) == 7


def test_review_facts_and_all_operational_boundaries_are_closed() -> None:
    review = _build()
    assert all(review[field] is True for field in service.TRUE_FIELDS)
    assert all(review[field] is False for field in service.FALSE_FIELDS)
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert all(review[field] == "NOT_AUTHORIZED" for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_outputs_findings_domains_recommendation_chain_and_gates_are_complete() -> None:
    review = _build()
    assert len(review["outputs_generated"]) == 28
    assert all(item["status"] == service.OUTPUT_STATUS for item in review["outputs_generated"])
    assert len(review["results_review_findings"]) == 15
    assert len(review["results_review_domains"]) == 12
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert len(review["next_chain"]) == 11
    assert len(review["next_gates"]) == 15
    assert len(review["risk_controls"]) >= 90


def test_checklist_is_complete_and_passes() -> None:
    review = _build()
    assert {item["check_id"] for item in review["checklist"]} == set(service.CHECK_IDS)
    assert all(item["status"] == "PASS" for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_digests_are_deterministic_and_distinct() -> None:
    first = _build()
    second = _build()
    keys = (
        service.RESULTS_REVIEW_DIGEST_KEY,
        service.ENRICHMENT_PLAN_REVIEW_DIGEST_KEY,
        service.MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY,
        service.WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    )
    assert [first[key] for key in keys] == [second[key] for key in keys]
    assert len({first[key] for key in keys}) == len(keys)
    assert all(len(first[key]) == 64 for key in keys)


def test_validator_accepts_valid_review() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(_build())
    assert result["review_status"] == service.REVIEW_STATUS
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "review_status", "review_scope", "source_execution_commit",
        "source_execution_artifact_kind", "source_execution_status", "source_execution_scope",
        "source_execution_digest", "source_authority_enrichment_plan_digest",
        "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest",
        "source_execution_manifest_digest", "selected_source_authority_or_no_change_disposition_package",
        "source_approval_digest", "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_reason", "source_blocked_manifest_digest",
        "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_workstream_mapping_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_receipt_recovery_or_recapture_receipt_digest",
        "source_durable_receipt_path", "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest", "source_module_grouping_digest",
        "source_staged_inventory_digest", "retry_execution_commit", "priority_1_total_nodeids",
        "top_10_count_sum", "module_summary_module_count", "failed_or_errored_nodeids_count",
        "observable_failure_family_count", "total_observable_evidence_items", "source_workstream_count",
        "missing_authority_inventory_section_count", "missing_authority_inventory_item_count",
        "workstream_mapping_count", "no_change_disposition_input_count", "alternate_diagnostic_input_count",
        "retry_basis_requirement_count", "source_outputs_generated_count", "recommended_next_task",
        service.RESULTS_REVIEW_DIGEST_KEY, service.ENRICHMENT_PLAN_REVIEW_DIGEST_KEY,
        service.MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST_KEY, service.WORKSTREAM_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_bound_scalar(field: str) -> None:
    review = _build()
    review[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(review)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_review_fact(field: str) -> None:
    review = _build()
    review[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(review)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_operational_boundary(field: str) -> None:
    review = _build()
    review[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(review)


@pytest.mark.parametrize(
    "field",
    [
        "priority_1_target_modules", "priority1_validation_summary", "diagnostic_capture_evidence_summary",
        "reviewed_observable_failure_families", "reviewed_workstreams", "source_authority_enrichment_plan_review",
        "missing_authority_inventory_review", "workstream_to_missing_authority_mapping_review",
        "source_evidence_requirements_review", "canonical_serialization_authority_requirements_review",
        "schema_field_contract_authority_requirements_review", "fixture_isolation_authority_requirements_review",
        "no_change_disposition_input_requirements_review", "alternate_diagnostic_input_requirements_review",
        "retry_basis_requirements_review", "results_review_domains", "results_review_findings", "outputs_generated",
        "next_chain", "next_gates", "risk_controls", "digest_manifest", "checklist", "summary",
    ],
)
def test_validator_rejects_changed_review_structure(field: str) -> None:
    review = _build()
    review[field] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(review)


def test_builder_rejects_changed_source_execution() -> None:
    source_execution = service._committed_source_execution()
    source_execution[service.source.ENRICHMENT_PLAN_DIGEST_KEY] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(source_execution=source_execution)


def test_markdown_contains_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Results Review After Blocked Execution v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_status_document(tmp_path) -> None:
    review = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_RESULTS_REVIEW_AFTER_BLOCKED_EXECUTION_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert review["artifact_kind"] == service.ARTIFACT_KIND
