from __future__ import annotations

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1()


def test_candidate_builds_offline_without_invoking_source_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source builder or execution must not run")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_results_review_after_blocked_execution_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.source.source,
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1",
        forbidden,
    )
    candidate = _build()
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


def test_artifact_status_scope_and_digest_are_exact() -> None:
    candidate = _build()
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE
    assert len(candidate[service.CANDIDATE_DIGEST_KEY]) == 64


def test_source_results_review_identity_and_digests_are_bound() -> None:
    candidate = _build()
    assert candidate["source_results_review_artifact_kind"] == service.SOURCE_RESULTS_REVIEW_ARTIFACT_KIND
    assert candidate["source_results_review_status"] == service.SOURCE_RESULTS_REVIEW_STATUS
    assert candidate["source_results_review_scope"] == service.SOURCE_RESULTS_REVIEW_SCOPE
    assert candidate["source_results_review_commit"] == service.SOURCE_RESULTS_REVIEW_COMMIT
    assert candidate["source_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert candidate["source_enrichment_plan_review_digest"] == service.SOURCE_ENRICHMENT_PLAN_REVIEW_DIGEST
    assert candidate["source_missing_authority_inventory_review_digest"] == service.SOURCE_MISSING_AUTHORITY_INVENTORY_REVIEW_DIGEST
    assert candidate["source_workstream_mapping_review_digest"] == service.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST
    assert candidate["source_results_review_manifest_digest"] == service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST


@pytest.mark.parametrize(
    "field",
    [
        "source_execution_commit", "source_execution_digest", "source_execution_artifact_kind",
        "source_execution_status", "source_execution_scope", "source_authority_enrichment_plan_digest",
        "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest",
        "source_execution_manifest_digest", "source_approval_commit", "source_approval_digest",
        "source_operator_review_commit", "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest",
        "source_candidate_commit", "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest",
        "source_failure_diagnosis_commit", "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit", "source_blocked_reason", "source_blocked_manifest_digest",
        "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_receipt_recovery_or_recapture_receipt_digest",
        "source_durable_receipt_path", "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason", "source_planning_execution_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest", "source_recovery_detail_digest",
        "source_module_grouping_digest", "source_staged_inventory_digest",
    ],
)
def test_complete_source_chain_is_bound(field: str) -> None:
    candidate = _build()
    assert candidate[field] == service._source_bindings()[field]


def test_retry_priority_diagnostic_family_and_workstream_facts_are_bound() -> None:
    candidate = _build()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert sum(item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]) == 612
    assert candidate["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert candidate["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert candidate["priority1_validation_summary"]["not_retry_evidence"] is True
    assert candidate["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert candidate["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert candidate["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert len(candidate["reviewed_observable_failure_families"]) == 4
    assert all(item["confidence"] == "HIGH" for item in candidate["reviewed_observable_failure_families"])
    assert len(candidate["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in candidate["reviewed_workstreams"])


def test_current_and_historical_workstream_review_digests_remain_distinguishable() -> None:
    candidate = _build()
    assert candidate["source_workstream_mapping_review_digest"] == service.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST
    assert candidate["source_plan_results_review_summary"]["workstream_mapping_review_digest"] == service._source_bindings()["source_workstream_mapping_review_digest"]


def test_enrichment_inventory_mapping_and_input_summaries_preserve_reviewed_limits() -> None:
    candidate = _build()
    assert candidate["source_authority_enrichment_review_summary"] == {"reviewed": True, "planning_only": True, "source_authority_acquired": False}
    assert candidate["missing_authority_inventory_review_summary"]["section_count"] == 4
    assert candidate["missing_authority_inventory_review_summary"]["item_count"] == 30
    assert candidate["missing_authority_inventory_review_summary"]["item_status"] == "MISSING_NOT_ACQUIRED"
    assert candidate["workstream_authority_mapping_review_summary"]["mapping_count"] == 4
    assert candidate["workstream_authority_mapping_review_summary"]["mapping_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["source_evidence_requirements_review_summary"]["section_count"] == 4
    assert candidate["no_change_disposition_input_review_summary"]["input_count"] == 7
    assert candidate["alternate_diagnostic_input_review_summary"]["input_count"] == 8
    assert candidate["retry_basis_requirements_review_summary"]["requirement_count"] == 7


def test_candidate_defines_twelve_packages_without_selection_or_execution() -> None:
    candidate = _build()
    packages = candidate["proposed_follow_on_packages"]
    assert len(packages) == 12
    assert sum(item["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED" for item in packages) == 1
    assert sum(item["status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED" for item in packages) == 5
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False for item in packages)
    assert all(item["approved"] is False for item in packages)
    assert all(item["authorized"] is False for item in packages)
    assert all(item["executed"] is False for item in packages)
    assert all(item.get("blocked_reason") for item in packages if item["status"] == "BLOCKED_NOT_ALLOWED")


def test_source_authority_acquisition_candidate_is_recommended_but_not_selected() -> None:
    candidate = _build()
    assert candidate["recommended_follow_on_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert candidate["recommended_package_selected"] is False
    assert candidate["follow_on_package_selected"] is False
    assert candidate["ready_for_follow_on_approval"] is False


def test_future_requirements_plan_outputs_and_non_goals_are_complete_and_unexecuted() -> None:
    candidate = _build()
    assert len(candidate["future_requirements"]) == 63
    assert all(item["status"] == service.FUTURE_REQUIREMENT_STATUS for item in candidate["future_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in candidate["future_requirements"])
    assert len(candidate["future_plan"]) == 12
    assert candidate["future_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert len(candidate["planned_outputs"]) == 27
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])
    assert len(candidate["non_goals"]) == 76


def test_all_candidate_facts_and_closed_boundaries_are_exact() -> None:
    candidate = _build()
    assert all(candidate[field] is True for field in service.TRUE_FIELDS)
    assert all(candidate[field] is False for field in service.FALSE_FIELDS)
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert all(candidate[field] == "NOT_AUTHORIZED" for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_next_chain_gates_risk_controls_and_checklist_are_complete() -> None:
    candidate = _build()
    assert len(candidate["next_chain"]) == 10
    assert len(candidate["next_gates"]) == 14
    assert len(candidate["risk_controls"]) == 96
    assert {item["check_id"] for item in candidate["checklist"]} == set(service.CHECK_IDS)
    assert all(item["status"] == "PASS" for item in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.CHECK_IDS)
    assert candidate["summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic() -> None:
    first, second = _build(), _build()
    assert first[service.CANDIDATE_DIGEST_KEY] == second[service.CANDIDATE_DIGEST_KEY]
    assert len(first[service.CANDIDATE_DIGEST_KEY]) == 64


def test_validator_accepts_valid_candidate() -> None:
    validated = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(_build())
    assert validated["candidate_status"] == service.CANDIDATE_STATUS
    assert validated["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "candidate_status", "candidate_scope", "source_results_review_commit",
        "source_results_review_digest", "source_enrichment_plan_review_digest",
        "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest",
        "source_results_review_manifest_digest", "source_execution_commit", "source_execution_digest",
        "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest",
        "source_workstream_authority_mapping_digest", "source_execution_manifest_digest",
        "selected_source_authority_or_no_change_disposition_package", "source_approval_digest",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_digest",
        "source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_reason", "source_blocked_manifest_digest",
        "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_receipt_recovery_or_recapture_receipt_digest",
        "source_durable_receipt_path", "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest", "source_module_grouping_digest",
        "source_staged_inventory_digest", "missing_authority_inventory_section_count",
        "missing_authority_inventory_item_count", "missing_authority_items_status", "workstream_mapping_count",
        "workstream_mapping_status", "no_change_disposition_input_count", "alternate_diagnostic_input_count",
        "retry_basis_requirement_count", "source_outputs_generated_count", "review_outputs_generated_count",
        "recommended_follow_on_package", "recommendation_status", "future_plan_status", "recommended_next_task",
        service.CANDIDATE_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_bound_scalar(field: str) -> None:
    candidate = _build()
    candidate[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_candidate_fact(field: str) -> None:
    candidate = _build()
    candidate[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_boundary(field: str) -> None:
    candidate = _build()
    candidate[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "source_results_review_summary", "source_execution_summary", "source_approval_summary",
        "source_operator_review_summary", "source_candidate_summary", "source_failure_diagnosis_summary",
        "source_blocked_execution_summary", "source_plan_results_review_summary", "source_plan_execution_summary",
        "source_method_results_review_summary", "source_method_execution_summary",
        "source_diagnostic_results_review_summary", "source_controlled_recapture_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary", "priority_1_target_modules", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families", "reviewed_workstreams",
        "source_authority_enrichment_review_summary", "missing_authority_inventory_review_summary",
        "workstream_authority_mapping_review_summary", "source_evidence_requirements_review_summary",
        "no_change_disposition_input_review_summary", "alternate_diagnostic_input_review_summary",
        "retry_basis_requirements_review_summary", "candidate_philosophy", "proposed_follow_on_packages",
        "future_requirements", "future_plan", "planned_outputs", "non_goals", "next_chain", "next_gates",
        "risk_controls", "checklist", "summary",
    ],
)
def test_validator_rejects_changed_candidate_structure(field: str) -> None:
    candidate = _build()
    candidate[field] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)


@pytest.mark.parametrize("index", range(12))
def test_validator_rejects_selected_proposed_package(index: int) -> None:
    candidate = _build()
    candidate["proposed_follow_on_packages"][index]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(candidate)


def test_builder_rejects_changed_source_results_review() -> None:
    source_review = service._committed_source_results_review()
    source_review[service.source.RESULTS_REVIEW_DIGEST_KEY] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(source_results_review=source_review)


def test_markdown_includes_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Candidate After Results Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_candidate_status(tmp_path) -> None:
    candidate = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
