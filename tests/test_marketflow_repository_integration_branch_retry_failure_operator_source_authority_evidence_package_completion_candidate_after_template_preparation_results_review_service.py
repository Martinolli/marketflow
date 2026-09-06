from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionCandidateError


def _candidate() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1()


def _reject(candidate: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(candidate)


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


def test_candidate_builds_offline_with_exact_identity() -> None:
    candidate = _candidate()
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["schema_version"] == service.SCHEMA_VERSION
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


def test_source_results_review_identity_and_digests_are_bound() -> None:
    candidate = _candidate()
    assert candidate["source_results_review_commit"] == service.SOURCE_RESULTS_REVIEW_COMMIT
    assert candidate["source_results_review_artifact_kind"] == service.source.ARTIFACT_KIND
    assert candidate["source_results_review_status"] == service.source.RESULTS_REVIEW_STATUS
    assert candidate["source_results_review_scope"] == service.source.RESULTS_REVIEW_SCOPE
    assert candidate["source_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert candidate["source_template_review_digest"] == service.SOURCE_TEMPLATE_REVIEW_DIGEST
    assert candidate["source_evidence_item_template_review_digest"] == service.SOURCE_EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST
    assert candidate["source_preparation_checklist_review_digest"] == service.SOURCE_PREPARATION_CHECKLIST_REVIEW_DIGEST
    assert candidate["source_template_coverage_review_digest"] == service.SOURCE_TEMPLATE_COVERAGE_REVIEW_DIGEST
    assert candidate["source_results_review_manifest_digest"] == service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST


def test_source_execution_and_governance_chain_are_bound() -> None:
    candidate = _candidate()
    required = (
        "source_execution_commit", "source_execution_artifact_kind", "source_execution_status", "source_execution_scope",
        "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest",
        "source_preparation_checklist_digest", "source_template_coverage_digest", "source_execution_manifest_digest",
        "source_approval_commit", "source_approval_digest", "source_attestation_digest",
        "source_operator_review_commit", "source_operator_review_digest", "source_preparation_candidate_commit",
        "source_preparation_candidate_digest", "source_failure_diagnosis_commit", "source_failure_diagnosis_digest",
        "source_blocked_acquisition_execution_commit", "source_blocked_acquisition_execution_manifest_digest",
        "source_acquisition_approval_commit", "source_acquisition_approval_digest", "source_acquisition_attestation_digest",
        "source_follow_on_results_review_digest", "source_follow_on_execution_digest", "source_follow_on_approval_digest",
        "source_follow_on_operator_review_digest", "source_follow_on_candidate_digest", "source_prior_results_review_digest",
        "source_enrichment_execution_digest", "historical_source_approval_digest", "historical_source_operator_review_digest",
        "historical_source_candidate_digest", "historical_failure_diagnosis_digest", "historical_blocked_remediation_manifest_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_durable_receipt_path",
        "source_detail_binding_results_review_digest", "source_module_grouping_digest", "source_staged_inventory_digest",
    )
    assert all(isinstance(candidate[key], str) and candidate[key] for key in required)
    assert candidate["source_blocked_acquisition_execution_reason"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
    assert candidate["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert candidate["selected_operator_source_authority_evidence_package_preparation_package"] == service.source.SELECTED_PACKAGE


def test_retry_priority_diagnostic_family_and_workstream_context_is_preserved() -> None:
    candidate = _candidate()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(candidate["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]) == 612
    assert candidate["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert candidate["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert candidate["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert candidate["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert len(candidate["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in candidate["reviewed_observable_failure_families"]) == 188
    assert len(candidate["reviewed_workstreams"]) == 4


def test_reviewed_template_mapping_inventory_and_zero_coverage_are_preserved() -> None:
    candidate = _candidate()
    assert len(candidate["reviewed_template_rows"]) == 30
    assert len(candidate["missing_authority_mapping"]) == 30
    assert len(candidate["acceptable_source_artifact_type_inventory"]) == 13
    assert candidate["actual_coverage"] == {
        "template_row_count": 30,
        "template_mapped_missing_authority_item_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
        "actual_evidence_items_filled": False,
    }
    assert {row["current_status"] for row in candidate["reviewed_template_rows"]} == {"MISSING_NOT_ACQUIRED"}
    assert all(row["template_only"] is True for row in candidate["reviewed_template_rows"])
    assert all(not row[field] for row in candidate["reviewed_template_rows"] for field in ("actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound"))


def test_package_options_are_defined_but_not_selected() -> None:
    candidate = _candidate()
    options = candidate["reviewed_package_options"]
    assert len(options) == candidate["package_option_count"] == 12
    assert sum(item["source_status"] != "BLOCKED_NOT_ALLOWED" for item in options) == 7
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in options) == 5
    assert all(not item[field] for item in options for field in ("selected", "approved", "authorized", "executed"))
    recommended = next(item for item in options if item["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["candidate_review_status"] == "CANDIDATE_RECOMMENDED_NOT_SELECTED"


def test_future_contracts_and_count_disclosures_are_complete() -> None:
    candidate = _candidate()
    assert [item["requirement_id"] for item in candidate["future_completion_requirements"]] == list(service.FUTURE_REQUIREMENT_IDS)
    assert {item["execution_status"] for item in candidate["future_completion_requirements"]} == {"NOT_EXECUTED"}
    assert len(candidate["future_completion_plan"]) == 17
    assert {item["plan_status"] for item in candidate["future_completion_plan"]} == {"PLANNED_NOT_EXECUTED"}
    assert len(candidate["planned_outputs"]) == 33
    assert {item["generation_status"] for item in candidate["planned_outputs"]} == {"PLANNED_NOT_GENERATED"}
    assert all(item["active"] is True for item in candidate["non_goals"])
    assert (candidate["future_completion_requirement_count"], candidate["non_goal_count"], candidate["risk_control_count"]) == (67, 71, 104)
    assert candidate["enumerated_future_completion_requirement_count"] == len(service.FUTURE_REQUIREMENT_IDS) == 69
    assert candidate["enumerated_non_goal_count"] == len(service.NON_GOAL_IDS) == 76
    assert candidate["enumerated_risk_control_count"] == len(service.RISK_CONTROLS) == 106


def test_authority_boundaries_are_closed() -> None:
    candidate = _candidate()
    assert all(candidate[field] is True for field in service.TRUE_FIELDS)
    assert all(candidate[field] is False for field in service.FALSE_FIELDS)
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert {candidate[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_outputs_recommendation_chain_gates_and_risks_are_complete() -> None:
    candidate = _candidate()
    assert [item["output_id"] for item in candidate["outputs"]] == list(service.OUTPUT_IDS)
    assert {item["status"] for item in candidate["outputs"]} == {"GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_ONLY"}
    assert candidate["recommended_operator_source_authority_evidence_package_completion_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommended_next_task"] == service.RECOMMENDED_TASK
    assert candidate["next_chain"] == list(service.NEXT_CHAIN)
    assert candidate["next_gates"] == list(service.NEXT_GATES)
    assert candidate["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_and_digests_are_deterministic() -> None:
    first, second = _candidate(), _candidate()
    assert first["summary"]["total_checks"] == first["summary"]["passed_checks"] == len(first["checklist"])
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in first["checklist"])
    for key in (service.CANDIDATE_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY, service.OPERATOR_INPUT_REQUIREMENTS_DIGEST_KEY, service.TEMPLATE_BINDING_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64
        assert first[key] == second[key]


def test_validator_accepts_valid_candidate() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(_candidate())
    assert result["candidate_status"] == service.CANDIDATE_STATUS
    assert result["failed_checks"] == 0


SOURCE_SCALARS = tuple(key for key, value in _candidate().items() if key.startswith("source_") and isinstance(value, (str, int, bool)))


@pytest.mark.parametrize("field", SOURCE_SCALARS)
def test_validator_rejects_changed_source_binding(field: str) -> None:
    candidate = _candidate()
    candidate[field] = _changed(candidate[field])
    _reject(candidate)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_changed(field: str) -> None:
    candidate = _candidate()
    candidate[field] = False
    _reject(candidate)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_changed(field: str) -> None:
    candidate = _candidate()
    candidate[field] = True
    _reject(candidate)


@pytest.mark.parametrize("index", range(12))
def test_validator_rejects_changed_package_option(index: int) -> None:
    candidate = _candidate()
    candidate["reviewed_package_options"][index]["selected"] = True
    _reject(candidate)


@pytest.mark.parametrize("index", range(30))
def test_validator_rejects_changed_template_row(index: int) -> None:
    candidate = _candidate()
    candidate["reviewed_template_rows"][index]["current_status"] = "ACQUIRED"
    _reject(candidate)


@pytest.mark.parametrize("index", range(len(service.FUTURE_REQUIREMENT_IDS)))
def test_validator_rejects_changed_future_requirement(index: int) -> None:
    candidate = _candidate()
    candidate["future_completion_requirements"][index]["execution_status"] = "EXECUTED"
    _reject(candidate)


@pytest.mark.parametrize("index", range(len(service.OUTPUT_IDS)))
def test_validator_rejects_missing_generated_output(index: int) -> None:
    candidate = _candidate()
    candidate["outputs"].pop(index)
    _reject(candidate)


@pytest.mark.parametrize("index", range(len(service.RISK_CONTROLS)))
def test_validator_rejects_changed_risk_control(index: int) -> None:
    candidate = _candidate()
    candidate["risk_controls"][index] = "changed"
    _reject(candidate)


@pytest.mark.parametrize("field", (
    "artifact_kind", "schema_version", "candidate_status", "candidate_scope", "primary_failure_class", "secondary_failure_classes",
    "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary", "diagnostic_capture_evidence_summary",
    "reviewed_observable_failure_families", "reviewed_workstreams", "reviewed_template_structure", "missing_authority_mapping",
    "acceptable_source_artifact_type_inventory", "actual_evidence_absence", "actual_coverage", "candidate_philosophy",
    "candidate_boundary", "operator_input_requirements", "future_completion_plan", "planned_outputs", "non_goals",
    "recommended_next_task", "recommended_action", "next_chain", "next_gates", "summary",
))
def test_validator_rejects_changed_contract_field(field: str) -> None:
    candidate = _candidate()
    candidate[field] = _changed(candidate[field])
    _reject(candidate)


def test_injected_source_results_review_must_match_committed_source() -> None:
    review = service.source.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1()
    review[service.source.RESULTS_REVIEW_DIGEST_KEY] = "0" * 64
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(source_results_review=review)


def test_markdown_contains_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_markdown_v1(_candidate())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Completion Candidate")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_uses_only_requested_status_destination(tmp_path) -> None:
    candidate = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_CANDIDATE_AFTER_TEMPLATE_PREPARATION_RESULTS_REVIEW_STATUS.md"
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS


@pytest.mark.parametrize("directory", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(tmp_path, directory: str) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_candidate_after_template_preparation_results_review_v1(tmp_path / directory)
