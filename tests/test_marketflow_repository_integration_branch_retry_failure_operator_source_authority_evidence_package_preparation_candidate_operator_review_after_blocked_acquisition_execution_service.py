from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateOperatorReviewError


def _review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1()


def _reject(review: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(review)


def _changed(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return "changed"
    if isinstance(value, list):
        return []
    if isinstance(value, dict):
        return {}
    return None


def test_operator_review_builds_offline_with_exact_identity() -> None:
    review = _review()
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert review["operator_review_scope"] == service.OPERATOR_REVIEW_SCOPE
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_source_preparation_candidate_is_digest_bound() -> None:
    review = _review()
    assert review["source_preparation_candidate_commit"] == service.SOURCE_PREPARATION_CANDIDATE_COMMIT
    assert review["source_preparation_candidate_digest"] == service.SOURCE_PREPARATION_CANDIDATE_DIGEST
    assert review["source_preparation_package_options_digest"] == service.SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST
    assert review["source_preparation_template_requirements_digest"] == service.SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST
    assert review["source_preparation_missing_authority_coverage_digest"] == service.SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST
    assert review["source_preparation_manifest_digest"] == service.SOURCE_PREPARATION_MANIFEST_DIGEST
    assert review["source_preparation_candidate_status"] == service.source.CANDIDATE_STATUS
    assert review["source_preparation_candidate_scope"] == service.source.CANDIDATE_SCOPE


def test_failure_diagnosis_and_blocked_execution_are_bound() -> None:
    review = _review()
    assert review["source_failure_diagnosis_commit"] == service.source.SOURCE_FAILURE_DIAGNOSIS_COMMIT
    assert review["source_failure_diagnosis_digest"] == service.source.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert review["source_failure_classification_digest"] == service.source.SOURCE_FAILURE_CLASSIFICATION_DIGEST
    assert review["source_missing_evidence_package_diagnosis_digest"] == service.source.SOURCE_MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST
    assert review["source_coverage_diagnosis_digest"] == service.source.SOURCE_COVERAGE_DIAGNOSIS_DIGEST
    assert review["source_failure_diagnosis_manifest_digest"] == service.source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST
    assert review["source_blocked_acquisition_execution_commit"] == service.source.source.SOURCE_BLOCKED_EXECUTION_COMMIT
    assert review["source_blocked_reason"] == service.PRIMARY_FAILURE_CLASS
    assert review["source_blocked_acquisition_execution_manifest_digest"] == service.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST


def test_approval_review_and_follow_on_chain_is_bound() -> None:
    review = _review()
    fields = (
        "source_approval_commit", "source_approval_digest", "source_attestation_digest",
        "source_operator_review_commit", "source_operator_review_digest", "source_candidate_review_digest",
        "source_scope_review_digest", "source_mapping_review_digest", "source_operator_review_manifest_digest",
        "source_follow_on_results_review_commit", "source_follow_on_results_review_digest",
        "source_follow_on_execution_commit", "source_follow_on_execution_after_results_review_digest",
        "source_authority_acquisition_candidate_digest", "source_authority_acquisition_scope_digest",
        "source_missing_authority_to_source_evidence_mapping_digest", "source_follow_on_execution_manifest_digest",
        "source_follow_on_approval_digest", "source_follow_on_candidate_operator_review_digest",
        "source_follow_on_candidate_digest", "source_results_review_digest", "source_execution_digest",
        "source_authority_enrichment_plan_digest", "source_missing_authority_inventory_digest",
        "source_workstream_authority_mapping_digest", "source_historical_approval_digest",
        "source_historical_operator_review_digest", "source_candidate_digest",
    )
    assert all(isinstance(review[field], str) and review[field] for field in fields)
    assert review["selected_source_authority_acquisition_package"] == "PACKAGE_EXECUTE_SOURCE_AUTHORITY_ACQUISITION_FROM_REVIEWED_CANDIDATE_SCOPE"


def test_historical_and_plan_method_diagnostic_recovery_evidence_is_bound() -> None:
    review = _review()
    assert review["historical_primary_failure_class"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert len(review["historical_secondary_failure_classes"]) == 4
    assert review["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    fields = (
        "source_remediation_execution_after_plan_results_review_failure_diagnosis_digest",
        "historical_blocked_remediation_manifest_digest",
        "source_planning_results_review_digest", "source_plan_execution_manifest_digest",
        "source_method_results_review_manifest_digest", "source_method_execution_manifest_digest",
        "source_targeted_diagnostic_output_capture_execution_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
    )
    assert all(review[field] for field in fields)
    assert review["source_durable_receipt_path"]
    assert review["diagnostic_receipt_parsed_in_operator_review"] is False


def test_retry_priority_diagnostic_families_and_workstreams_are_bound() -> None:
    review = _review()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(review["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    assert review["top_10_count_sum"] == 1069
    assert review["failed_or_errored_nodeids_count"] == 1404
    assert review["module_summary_module_count"] == 29
    assert review["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["not_retry_evidence"] is True
    assert review["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert review["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert review["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert review["diagnostic_capture_evidence_summary"]["diagnostic_only"] is True
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert {item["confidence"] for item in review["reviewed_observable_failure_families"]} == {"HIGH"}
    assert sum(item["observable_evidence_count"] for item in review["reviewed_observable_failure_families"]) == 188
    assert len(review["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in review["reviewed_workstreams"])


def test_acquisition_scope_requirements_and_zero_coverage_are_preserved() -> None:
    review = _review()
    assert review["acquisition_scope_section_count"] == 4
    assert review["mapped_missing_authority_item_count"] == 30
    assert review["acceptable_source_artifact_type_count"] == 13
    assert review["operator_provided_evidence_requirement_count"] == 10
    assert review["evidence_custody_and_digest_requirement_count"] == 6
    assert review["candidate_results_review_requirement_count"] == 16
    coverage = review["missing_authority_coverage"]
    assert coverage["covered_missing_authority_item_count"] == 0
    assert coverage["uncovered_missing_authority_item_count"] == 30
    assert coverage["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert len(coverage["items"]) == 30
    assert {item["coverage_status"] for item in coverage["items"]} == {"MISSING_NOT_ACQUIRED"}


def test_candidate_review_counts_are_exact() -> None:
    review = _review()
    assert review["source_package_option_count"] == review["package_option_count"] == 12
    assert review["source_available_package_count"] == review["available_package_count"] == 7
    assert review["source_blocked_package_count"] == review["blocked_package_count"] == 5
    assert review["source_future_requirement_count"] == review["future_requirement_count"] == 62
    assert review["source_future_plan_step_count"] == review["future_plan_step_count"] == 15
    assert review["source_planned_output_count"] == review["planned_output_count"] == 28
    assert review["source_generated_output_count"] == 28
    assert review["source_non_goal_count"] == review["non_goal_count"] == 71
    assert review["source_next_gate_count"] == 16
    assert review["source_risk_control_count"] == review["risk_control_count"] == 104


def test_package_options_are_reviewed_without_selection() -> None:
    review = _review()
    options = review["reviewed_package_options"]
    assert len(options) == 12
    assert sum(item["source_status"] != "BLOCKED_NOT_ALLOWED" for item in options) == 7
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in options) == 5
    assert all(not item[field] for item in options for field in ("selected", "approved", "authorized", "executed"))
    recommended = next(item for item in options if item["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["operator_review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"


def test_future_requirements_plan_outputs_and_non_goals_are_reviewed_only() -> None:
    review = _review()
    assert len(review["reviewed_future_requirements"]) == 62
    assert {item["review_status"] for item in review["reviewed_future_requirements"]} == {"REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION"}
    assert {item["execution_status"] for item in review["reviewed_future_requirements"]} == {"NOT_EXECUTED"}
    assert len(review["reviewed_future_plan"]) == 15
    assert {item["review_status"] for item in review["reviewed_future_plan"]} == {"REVIEWED_PLANNED_NOT_EXECUTED"}
    assert len(review["reviewed_planned_outputs"]) == 28
    assert {item["review_status"] for item in review["reviewed_planned_outputs"]} == {"REVIEWED_PLANNED_NOT_GENERATED"}
    assert {item["generation_status"] for item in review["reviewed_planned_outputs"]} == {"NOT_GENERATED"}
    assert len(review["reviewed_non_goals"]) == 71
    assert all(item["active"] is True for item in review["reviewed_non_goals"])


def test_all_authority_boundaries_remain_closed() -> None:
    review = _review()
    assert all(review[field] is True for field in service.TRUE_FIELDS)
    assert all(review[field] is False for field in service.FALSE_FIELDS)
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert {review[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_outputs_recommendation_chain_gates_and_risks_are_complete() -> None:
    review = _review()
    assert [item["output_id"] for item in review["outputs"]] == list(service.OUTPUT_IDS)
    assert {item["status"] for item in review["outputs"]} == {"GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_ONLY"}
    assert review["recommended_next_task"] == service.RECOMMENDED_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["next_chain"] == list(service.NEXT_CHAIN)
    assert review["next_gates"] == list(service.NEXT_GATES)
    assert review["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_summary_and_digests_are_deterministic() -> None:
    first, second = _review(), _review()
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in first["checklist"])
    assert first["summary"]["total_checks"] == first["summary"]["passed_checks"]
    assert first["summary"]["failed_checks"] == 0
    for key in (
        service.OPERATOR_REVIEW_DIGEST_KEY, service.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        service.TEMPLATE_REQUIREMENTS_REVIEW_DIGEST_KEY, service.COVERAGE_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert len(first[key]) == 64
        assert first[key] == second[key]


def test_validator_accepts_valid_review() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(_review())
    assert result["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert result["failed_checks"] == 0


def test_builder_does_not_call_prohibited_public_source_builder(monkeypatch) -> None:
    def prohibited(**_kwargs):
        raise AssertionError("public source preparation builder must not be called")
    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1",
        prohibited,
    )
    assert _review()["source_preparation_candidate_digest"] == service.SOURCE_PREPARATION_CANDIDATE_DIGEST


SOURCE_SCALAR_FIELDS = tuple(
    key for key, value in _review().items()
    if key.startswith("source_") and isinstance(value, (str, int, bool))
)


@pytest.mark.parametrize("field", SOURCE_SCALAR_FIELDS)
def test_validator_rejects_changed_source_scalar(field: str) -> None:
    review = _review()
    review[field] = _changed(review[field])
    _reject(review)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_changed(field: str) -> None:
    review = _review()
    review[field] = False
    _reject(review)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_changed(field: str) -> None:
    review = _review()
    review[field] = True
    _reject(review)


@pytest.mark.parametrize("field", (
    "artifact_kind", "operator_review_status", "operator_review_scope",
    "primary_failure_class", "secondary_failure_classes", "reviewed_package_options",
    "reviewed_future_requirements", "reviewed_future_plan", "reviewed_planned_outputs",
    "reviewed_non_goals", "outputs", "recommended_next_task", "next_chain", "next_gates",
    "risk_controls", "missing_authority_coverage", "retry_failure_context",
    "priority_1_target_modules", "priority1_validation_summary",
    "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families",
    "reviewed_workstreams",
))
def test_validator_rejects_changed_review_contract(field: str) -> None:
    review = _review()
    review[field] = _changed(review[field])
    _reject(review)


def test_validator_rejects_missing_digest() -> None:
    review = _review()
    review.pop(service.MANIFEST_DIGEST_KEY)
    _reject(review)


def test_injected_source_candidate_must_match_committed_source() -> None:
    candidate = deepcopy(service._COMMITTED_SOURCE_PREPARATION_CANDIDATE)
    candidate[service.source.CANDIDATE_DIGEST_KEY] = "0" * 64
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(source_preparation_candidate=candidate)


def test_markdown_contains_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_markdown_v1(_review())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Candidate Operator Review")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_uses_only_requested_status_destination(tmp_path) -> None:
    review = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_ACQUISITION_EXECUTION_STATUS.md"
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(protected: str, tmp_path) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_operator_review_after_blocked_acquisition_execution_v1(tmp_path / protected)
