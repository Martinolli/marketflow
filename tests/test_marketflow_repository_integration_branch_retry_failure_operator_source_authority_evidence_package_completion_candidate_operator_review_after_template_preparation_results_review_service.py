from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateOperatorReviewError


def _review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1()


def _reject(review: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(review)


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
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert review["operator_review_scope"] == service.OPERATOR_REVIEW_SCOPE
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_source_completion_candidate_identity_and_digests_are_bound() -> None:
    review = _review()
    assert review["source_completion_candidate_commit"] == service.SOURCE_COMPLETION_CANDIDATE_COMMIT
    assert review["source_completion_candidate_artifact_kind"] == service.source.ARTIFACT_KIND
    assert review["source_completion_candidate_status"] == service.source.CANDIDATE_STATUS
    assert review["source_completion_candidate_scope"] == service.source.CANDIDATE_SCOPE
    assert review["source_completion_candidate_digest"] == service.SOURCE_COMPLETION_CANDIDATE_DIGEST
    assert review["source_completion_candidate_package_options_digest"] == service.SOURCE_COMPLETION_CANDIDATE_PACKAGE_OPTIONS_DIGEST
    assert review["source_completion_candidate_operator_input_requirements_digest"] == service.SOURCE_COMPLETION_CANDIDATE_OPERATOR_INPUT_REQUIREMENTS_DIGEST
    assert review["source_completion_candidate_template_binding_digest"] == service.SOURCE_COMPLETION_CANDIDATE_TEMPLATE_BINDING_DIGEST
    assert review["source_completion_candidate_coverage_digest"] == service.SOURCE_COMPLETION_CANDIDATE_COVERAGE_DIGEST
    assert review["source_completion_candidate_manifest_digest"] == service.SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST


def test_source_results_review_execution_and_governance_chain_are_bound() -> None:
    review = _review()
    required = (
        "source_results_review_commit", "source_results_review_digest", "source_template_review_digest",
        "source_evidence_item_template_review_digest", "source_preparation_checklist_review_digest",
        "source_template_coverage_review_digest", "source_results_review_manifest_digest",
        "source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope",
        "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest",
        "source_preparation_checklist_digest", "source_template_coverage_digest", "source_execution_manifest_digest",
        "source_approval_commit", "source_approval_digest", "source_attestation_digest",
        "source_operator_review_commit", "source_operator_review_digest", "source_preparation_candidate_commit",
        "source_preparation_candidate_digest", "source_failure_diagnosis_commit", "source_failure_diagnosis_digest",
        "source_blocked_acquisition_execution_commit", "source_blocked_acquisition_execution_manifest_digest",
        "source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest",
        "source_follow_on_results_review_digest", "source_follow_on_execution_digest", "source_follow_on_approval_digest",
        "source_follow_on_operator_review_digest", "source_follow_on_candidate_digest", "source_results_review_digest_historical",
        "source_enrichment_execution_digest", "historical_source_approval_digest", "historical_source_operator_review_digest",
        "historical_source_candidate_digest", "historical_failure_diagnosis_digest", "historical_blocked_remediation_manifest_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_durable_receipt_path",
        "source_detail_binding_results_review_digest", "source_module_grouping_digest", "source_staged_inventory_digest",
    )
    assert all(isinstance(review[key], str) and review[key] for key in required)
    assert review["source_blocked_acquisition_execution_reason"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
    assert review["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert review["selected_operator_source_authority_evidence_package_preparation_package"] == service.source.source.SELECTED_PACKAGE


def test_retry_priority_diagnostic_family_and_workstream_context_is_preserved() -> None:
    review = _review()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(review["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    assert review["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert review["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert review["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert review["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in review["reviewed_observable_failure_families"]) == 188
    assert len(review["reviewed_workstreams"]) == 4


def test_template_mapping_inventory_and_actual_coverage_are_reviewed() -> None:
    review = _review()
    assert len(review["reviewed_template_rows"]) == 30
    assert len(review["missing_authority_mapping"]) == 30
    assert len(review["acceptable_source_artifact_type_inventory"]) == 13
    assert review["actual_coverage_review"]["actual_covered_missing_authority_item_count"] == 0
    assert review["actual_coverage_review"]["actual_uncovered_missing_authority_item_count"] == 30
    assert review["actual_coverage_review"]["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert {row["current_status"] for row in review["reviewed_template_rows"]} == {"MISSING_NOT_ACQUIRED"}
    assert all(row["template_only"] is True for row in review["reviewed_template_rows"])
    assert all(not row[field] for row in review["reviewed_template_rows"] for field in ("actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound"))


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


def test_future_contracts_are_reviewed_but_not_executed() -> None:
    review = _review()
    assert len(review["reviewed_future_completion_requirements"]) == 69
    assert {item["review_status"] for item in review["reviewed_future_completion_requirements"]} == {"REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION"}
    assert {item["execution_status"] for item in review["reviewed_future_completion_requirements"]} == {"NOT_EXECUTED"}
    assert len(review["reviewed_future_completion_plan"]) == 17
    assert {item["review_status"] for item in review["reviewed_future_completion_plan"]} == {"REVIEWED_PLANNED_NOT_EXECUTED"}
    assert len(review["reviewed_planned_outputs"]) == 33
    assert {item["generation_status"] for item in review["reviewed_planned_outputs"]} == {"NOT_GENERATED"}
    assert len(review["reviewed_non_goals"]) == 76
    assert all(item["active"] is True for item in review["reviewed_non_goals"])


def test_count_label_distinction_is_preserved() -> None:
    review = _review()
    assert (review["future_completion_requirement_count"], review["source_enumerated_future_completion_requirement_count"]) == (67, 69)
    assert (review["non_goal_count"], review["source_enumerated_non_goal_count"]) == (71, 76)
    assert (review["risk_control_count"], review["source_enumerated_risk_control_count"]) == (104, 106)
    assert review["count_label_distinction"] == {
        "future_completion_requirement_count": 67,
        "source_enumerated_future_completion_requirement_count": 69,
        "non_goal_count": 71,
        "source_enumerated_non_goal_count": 76,
        "risk_control_count": 104,
        "source_enumerated_risk_control_count": 106,
        "preserved_without_reconciliation": True,
        "all_named_items_preserved": True,
        "distinction_is_not_a_failure": True,
    }


def test_authority_boundaries_remain_closed() -> None:
    review = _review()
    assert all(review[field] is True for field in service.TRUE_FIELDS)
    assert all(review[field] is False for field in service.FALSE_FIELDS)
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert {review[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_outputs_recommendation_chain_gates_and_controls_are_complete() -> None:
    review = _review()
    assert [item["output_id"] for item in review["outputs"]] == list(service.OUTPUT_IDS)
    assert {item["status"] for item in review["outputs"]} == {"GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_ONLY"}
    assert review["recommended_operator_source_authority_evidence_package_completion_package"] == service.RECOMMENDED_PACKAGE
    assert review["recommended_next_task"] == service.RECOMMENDED_TASK
    assert review["next_chain"] == list(service.NEXT_CHAIN)
    assert review["next_gates"] == list(service.NEXT_GATES)
    assert review["risk_controls"] == list(service.RISK_CONTROLS)
    assert review["reviewed_source_risk_controls"] == list(service.source.RISK_CONTROLS)


def test_checklist_and_digests_are_deterministic() -> None:
    first, second = _review(), _review()
    assert first["summary"]["total_checks"] == first["summary"]["passed_checks"] == len(first["checklist"])
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in first["checklist"])
    for key in (service.OPERATOR_REVIEW_DIGEST_KEY, service.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY, service.OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST_KEY, service.TEMPLATE_BINDING_REVIEW_DIGEST_KEY, service.COVERAGE_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64
        assert first[key] == second[key]


def test_validator_accepts_valid_review() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(_review())
    assert result["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert result["failed_checks"] == 0


SOURCE_SCALARS = tuple(key for key, value in _review().items() if key.startswith("source_") and isinstance(value, (str, int, bool)))


@pytest.mark.parametrize("field", SOURCE_SCALARS)
def test_validator_rejects_changed_source_binding(field: str) -> None:
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


@pytest.mark.parametrize("index", range(12))
def test_validator_rejects_changed_package_option(index: int) -> None:
    review = _review()
    review["reviewed_package_options"][index]["selected"] = True
    _reject(review)


@pytest.mark.parametrize("index", range(30))
def test_validator_rejects_changed_template_row(index: int) -> None:
    review = _review()
    review["reviewed_template_rows"][index]["current_status"] = "ACQUIRED"
    _reject(review)


@pytest.mark.parametrize("index", range(len(service.source.FUTURE_REQUIREMENT_IDS)))
def test_validator_rejects_changed_reviewed_requirement(index: int) -> None:
    review = _review()
    review["reviewed_future_completion_requirements"][index]["execution_status"] = "EXECUTED"
    _reject(review)


@pytest.mark.parametrize("index", range(len(service.OUTPUT_IDS)))
def test_validator_rejects_missing_output(index: int) -> None:
    review = _review()
    review["outputs"].pop(index)
    _reject(review)


@pytest.mark.parametrize("index", range(len(service.RISK_CONTROLS)))
def test_validator_rejects_changed_risk_control(index: int) -> None:
    review = _review()
    review["risk_controls"][index] = "changed"
    _reject(review)


@pytest.mark.parametrize("field", (
    "artifact_kind", "schema_version", "operator_review_status", "operator_review_scope", "primary_failure_class",
    "secondary_failure_classes", "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary",
    "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families", "reviewed_workstreams",
    "reviewed_template_structure", "missing_authority_mapping", "acceptable_source_artifact_type_inventory",
    "actual_evidence_absence", "actual_coverage_review", "operator_review_philosophy", "operator_review_boundary",
    "recommended_operator_source_authority_evidence_package_completion_package", "reviewed_operator_input_requirements",
    "reviewed_future_completion_plan", "reviewed_planned_outputs", "reviewed_non_goals", "count_label_distinction",
    "reviewed_source_risk_controls", "recommended_next_task", "recommended_action", "next_chain", "next_gates", "summary",
))
def test_validator_rejects_changed_contract_field(field: str) -> None:
    review = _review()
    review[field] = _changed(review[field])
    _reject(review)


def test_injected_source_completion_candidate_must_match_committed_source() -> None:
    candidate = deepcopy(service._COMMITTED_SOURCE_COMPLETION_CANDIDATE)
    candidate[service.source.CANDIDATE_DIGEST_KEY] = "0" * 64
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(source_completion_candidate=candidate)


def test_markdown_contains_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_markdown_v1(_review())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Candidate Operator Review")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_uses_only_requested_status_destination(tmp_path) -> None:
    review = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_OPERATOR_REVIEW_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_STATUS.md"
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS


@pytest.mark.parametrize("directory", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(tmp_path, directory: str) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_operator_review_after_template_preparation_results_review_v1(tmp_path / directory)
