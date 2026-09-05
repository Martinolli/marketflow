from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1()


def _reject(review: dict) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(review)


def test_operator_review_builds_offline_without_invoking_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source builder must not run")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1",
        forbidden,
    )
    review = _build()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_artifact_status_scope_and_source_follow_on_identity_are_exact() -> None:
    review = _build()
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["source_follow_on_candidate_artifact_kind"] == service.source.ARTIFACT_KIND
    assert review["source_follow_on_candidate_status"] == service.source.CANDIDATE_STATUS
    assert review["source_follow_on_candidate_scope"] == service.source.CANDIDATE_SCOPE
    assert review["source_follow_on_candidate_commit"] == service.SOURCE_FOLLOW_ON_CANDIDATE_COMMIT
    assert review["source_follow_on_candidate_digest"] == service.SOURCE_FOLLOW_ON_CANDIDATE_DIGEST


@pytest.mark.parametrize(
    "field",
    [
        "source_results_review_artifact_kind", "source_results_review_status", "source_results_review_scope",
        "source_results_review_commit", "source_results_review_digest", "source_enrichment_plan_review_digest",
        "source_missing_authority_inventory_review_digest", "source_workstream_mapping_review_digest",
        "source_results_review_manifest_digest", "source_execution_artifact_kind", "source_execution_status",
        "source_execution_scope", "source_execution_commit", "source_execution_digest",
        "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest",
        "source_workstream_authority_mapping_digest", "source_execution_manifest_digest",
        "selected_source_authority_or_no_change_disposition_package", "source_approval_artifact_kind",
        "source_approval_status", "source_approval_scope", "source_approval_commit", "source_approval_digest",
        "source_operator_review_artifact_kind", "source_operator_review_status", "source_operator_review_scope",
        "source_operator_review_commit", "source_operator_review_digest", "source_candidate_artifact_kind",
        "source_candidate_status", "source_candidate_scope", "source_candidate_commit", "source_candidate_digest",
        "source_failure_diagnosis_artifact_kind", "source_failure_diagnosis_status",
        "source_failure_diagnosis_scope", "source_failure_diagnosis_commit",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_artifact_kind", "source_blocked_execution_status",
        "source_blocked_execution_scope", "source_blocked_execution_commit", "source_blocked_reason",
        "source_blocked_manifest_digest", "primary_failure_class", "secondary_failure_classes",
        "source_remediation_execution_approval_after_plan_results_review_commit",
        "source_remediation_execution_approval_after_plan_results_review_digest",
        "historical_selected_remediation_execution_package", "source_plan_results_review_commit",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_plan_results_review_manifest_digest",
        "source_plan_execution_commit", "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_plan_execution_manifest_digest", "source_method_results_review_commit",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_failure_family_classification_review_digest", "source_bounded_excerpt_analysis_review_digest",
        "source_method_results_review_manifest_digest", "source_method_execution_commit",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_failure_family_classification_digest", "source_bounded_excerpt_analysis_digest",
        "source_method_execution_manifest_digest", "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_payload_review_digest",
        "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
        "source_receipt_recovery_or_recapture_results_review_manifest_digest",
        "source_receipt_recovery_or_recapture_execution_commit",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_payload_digest",
        "source_receipt_recovery_or_recapture_receipt_digest",
        "source_receipt_recovery_or_recapture_digest_manifest_digest", "source_durable_receipt_path",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason", "source_planning_execution_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_detail_digest", "source_module_grouping_digest", "source_staged_inventory_digest",
    ],
)
def test_complete_source_chain_is_bound(field: str) -> None:
    review = _build()
    assert review[field] == service._source_bindings()[field]


def test_source_context_and_review_summaries_are_bound() -> None:
    review = _build()
    assert review["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(review["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    assert review["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["not_retry_evidence"] is True
    assert review["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert review["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert review["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert review["source_durable_receipt_summary"]["parsed"] is False
    assert review["source_plan_results_review_summary"]["workstream_mapping_review_digest"] == "f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334"


def test_four_families_and_workstreams_remain_planning_evidence() -> None:
    review = _build()
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in review["reviewed_observable_failure_families"]) == 188
    assert all(item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert all(item["planning_evidence_only"] is True for item in review["reviewed_workstreams"])
    assert all(item["direct_change_authorized"] is False for item in review["reviewed_workstreams"])


def test_enrichment_inventory_mapping_and_input_review_limits_are_preserved() -> None:
    review = _build()
    assert review["source_authority_enrichment_review_summary"] == {"reviewed": True, "planning_only": True, "source_authority_acquired": False}
    assert review["missing_authority_inventory_review_summary"]["section_count"] == 4
    assert review["missing_authority_inventory_review_summary"]["item_count"] == 30
    assert review["missing_authority_inventory_review_summary"]["item_status"] == "MISSING_NOT_ACQUIRED"
    assert review["workstream_authority_mapping_review_summary"]["mapping_count"] == 4
    assert review["workstream_authority_mapping_review_summary"]["mapping_status"] == "PLANNED_NOT_EXECUTED"
    assert review["source_evidence_requirements_review_summary"]["section_count"] == 4
    assert review["no_change_disposition_input_review_summary"]["input_count"] == 7
    assert review["alternate_diagnostic_input_review_summary"]["input_count"] == 8
    assert review["retry_basis_requirements_review_summary"]["requirement_count"] == 7


def test_candidate_philosophy_and_all_twelve_packages_are_reviewed_without_selection() -> None:
    review = _build()
    assert review["reviewed_candidate_philosophy"] == service.REVIEWED_CANDIDATE_PHILOSOPHY
    packages = review["reviewed_follow_on_packages"]
    assert len(packages) == 12
    assert sum(item["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" for item in packages) == 1
    assert sum(item["review_status"] == "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED" for item in packages) == 5
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False for item in packages)
    assert all(item["approved"] is False for item in packages)
    assert all(item["authorized"] is False for item in packages)
    assert all(item["executed"] is False for item in packages)
    assert all(item.get("blocked_reason") for item in packages if item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED")


def test_recommendation_is_reviewed_but_not_selected_or_approved() -> None:
    review = _build()
    assert review["recommended_follow_on_package"] == service.RECOMMENDED_PACKAGE
    assert review["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["recommended_package"]["reason"] == service.RECOMMENDATION_REASON
    assert review["recommended_package_selected"] is False
    assert review["follow_on_package_selected"] is False
    assert review["follow_on_package_approved"] is False
    assert review["ready_for_follow_on_approval"] is False
    assert review["ready_for_follow_on_execution"] is False


def test_future_requirements_plan_outputs_and_non_goals_are_reviewed_only() -> None:
    review = _build()
    assert len(review["reviewed_future_requirements"]) == 63
    assert all(item["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_CONDITIONAL_FOLLOW_ON_AFTER_SOURCE_AUTHORITY_ENRICHMENT_RESULTS_REVIEW" for item in review["reviewed_future_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_requirements"])
    assert len(review["reviewed_future_plan"]) == 12
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" for item in review["reviewed_future_plan"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_plan"])
    assert len(review["reviewed_planned_outputs"]) == 27
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert all(item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert len(review["reviewed_non_goals"]) == 76
    assert all(item["review_status"] == "REVIEWED_ACTIVE" for item in review["reviewed_non_goals"])


def test_recommendation_chain_gates_controls_and_boundaries_are_exact() -> None:
    review = _build()
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["recommended_action"] == "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_FOLLOW_ON_EXECUTION"
    assert review["recommendation"]["reason"] == service.NEXT_REASON
    assert len(review["next_chain"]) == 9
    assert len(review["next_gates"]) == 13
    assert len(review["risk_controls"]) == 96
    assert all(review[field] is True for field in service.TRUE_FIELDS)
    assert all(review[field] is False for field in service.FALSE_FIELDS)
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert all(review[field] == "NOT_AUTHORIZED" for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_checklist_and_summary_pass_without_blockers() -> None:
    review = _build()
    assert {item["check_id"] for item in review["checklist"]} == set(service.CHECK_IDS)
    assert all(item["status"] == "PASS" for item in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_operator_review_digest_is_deterministic() -> None:
    first, second = _build(), _build()
    assert first[service.OPERATOR_REVIEW_DIGEST_KEY] == second[service.OPERATOR_REVIEW_DIGEST_KEY]
    assert len(first[service.OPERATOR_REVIEW_DIGEST_KEY]) == 64


def test_validator_accepts_valid_review() -> None:
    validated = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(_build())
    assert validated["review_status"] == service.REVIEW_STATUS
    assert validated["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "review_status", "review_scope", "source_follow_on_candidate_commit",
        "source_follow_on_candidate_digest", "source_results_review_digest",
        "source_enrichment_plan_review_digest", "source_missing_authority_inventory_review_digest",
        "source_workstream_mapping_review_digest", "source_results_review_manifest_digest",
        "source_execution_commit", "source_execution_digest", "source_authority_enrichment_plan_digest",
        "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest",
        "source_execution_manifest_digest", "selected_source_authority_or_no_change_disposition_package",
        "source_approval_digest", "source_operator_review_digest", "source_candidate_digest",
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "source_blocked_execution_commit", "source_blocked_reason", "source_blocked_manifest_digest",
        "primary_failure_class", "source_remediation_execution_approval_after_plan_results_review_digest",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_receipt_recovery_or_recapture_receipt_digest",
        "source_durable_receipt_path", "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest", "source_module_grouping_digest",
        "missing_authority_inventory_section_count", "missing_authority_inventory_item_count",
        "missing_authority_items_status", "workstream_mapping_count", "workstream_mapping_status",
        "recommended_follow_on_package", "recommendation_status", "recommended_next_task",
        "recommended_next_task_status", "recommended_action", service.OPERATOR_REVIEW_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_bound_scalar(field: str) -> None:
    review = _build()
    review[field] = "changed"
    _reject(review)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_false_review_fact(field: str) -> None:
    review = _build()
    review[field] = False
    _reject(review)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_boundary(field: str) -> None:
    review = _build()
    review[field] = True
    _reject(review)


@pytest.mark.parametrize(
    "field",
    [
        "source_follow_on_candidate_summary", "source_results_review_summary", "source_execution_summary",
        "source_approval_summary", "source_operator_review_summary", "source_candidate_summary",
        "source_failure_diagnosis_summary", "source_blocked_execution_summary",
        "source_plan_results_review_summary", "source_plan_execution_summary",
        "source_method_results_review_summary", "source_method_execution_summary",
        "source_diagnostic_results_review_summary", "source_controlled_recapture_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary", "priority_1_target_modules",
        "priority1_validation_summary", "diagnostic_capture_evidence_summary",
        "reviewed_observable_failure_families", "reviewed_workstreams",
        "source_authority_enrichment_review_summary", "missing_authority_inventory_review_summary",
        "workstream_authority_mapping_review_summary", "source_evidence_requirements_review_summary",
        "no_change_disposition_input_review_summary", "alternate_diagnostic_input_review_summary",
        "retry_basis_requirements_review_summary", "reviewed_candidate_philosophy",
        "reviewed_follow_on_packages", "recommended_package", "reviewed_future_requirements",
        "reviewed_future_plan", "reviewed_planned_outputs", "reviewed_non_goals", "recommendation",
        "next_chain", "next_gates", "risk_controls", "checklist", "summary", "secondary_failure_classes",
    ],
)
def test_validator_rejects_changed_review_structure(field: str) -> None:
    review = _build()
    review[field] = []
    _reject(review)


@pytest.mark.parametrize("index", range(12))
@pytest.mark.parametrize("field", ["selected", "approved", "authorized", "executed"])
def test_validator_rejects_open_reviewed_package_boundary(index: int, field: str) -> None:
    review = _build()
    review["reviewed_follow_on_packages"][index][field] = True
    _reject(review)


def test_builder_rejects_changed_source_candidate_digest() -> None:
    candidate = service._committed_source_follow_on_candidate()
    candidate[service.source.CANDIDATE_DIGEST_KEY] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(source_follow_on_candidate=candidate)


def test_builder_accepts_the_offline_source_candidate_artifact() -> None:
    candidate = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_v1()
    review = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(source_follow_on_candidate=candidate)
    assert review["source_follow_on_candidate_digest"] == service.SOURCE_FOLLOW_ON_CANDIDATE_DIGEST


def test_source_candidate_argument_is_not_mutated() -> None:
    candidate = service._committed_source_follow_on_candidate()
    original = deepcopy(candidate)
    service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(source_follow_on_candidate=candidate)
    assert candidate == original


def test_markdown_includes_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Candidate After Results Review Operator Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_operator_review_status(tmp_path) -> None:
    review = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_candidate_after_results_review_operator_review_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_CANDIDATE_AFTER_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert review["artifact_kind"] == service.ARTIFACT_KIND
