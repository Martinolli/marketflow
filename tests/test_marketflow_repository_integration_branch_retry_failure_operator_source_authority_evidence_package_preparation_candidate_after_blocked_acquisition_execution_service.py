from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationCandidateError


def _candidate() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1()


def _reject(candidate: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1(candidate)


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
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE
    assert candidate["schema_version"] == service.SCHEMA_VERSION
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


def test_source_failure_diagnosis_and_blocked_execution_are_bound() -> None:
    candidate = _candidate()
    assert candidate["source_failure_diagnosis_commit"] == service.SOURCE_FAILURE_DIAGNOSIS_COMMIT
    assert candidate["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert candidate["source_failure_classification_digest"] == service.SOURCE_FAILURE_CLASSIFICATION_DIGEST
    assert candidate["source_missing_evidence_package_diagnosis_digest"] == service.SOURCE_MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST
    assert candidate["source_coverage_diagnosis_digest"] == service.SOURCE_COVERAGE_DIAGNOSIS_DIGEST
    assert candidate["source_failure_diagnosis_manifest_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST
    assert candidate["source_blocked_acquisition_execution_commit"] == service.source.SOURCE_BLOCKED_EXECUTION_COMMIT
    assert candidate["source_blocked_reason"] == service.PRIMARY_FAILURE_CLASS
    assert candidate["source_blocked_manifest_digest"] == service.source.SOURCE_BLOCKED_MANIFEST_DIGEST


def test_source_governance_and_acquisition_chain_digests_are_bound() -> None:
    candidate = _candidate()
    required = (
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
    assert all(isinstance(candidate[key], str) and candidate[key] for key in required)
    assert candidate["selected_source_authority_acquisition_package"] == service.source._COMMITTED_SOURCE_BLOCKED_EXECUTION["selected_source_authority_acquisition_package"]


def test_historical_failure_and_planning_chain_is_preserved() -> None:
    candidate = _candidate()
    assert candidate["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert candidate["historical_primary_failure_class"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert len(candidate["historical_secondary_failure_classes"]) == 4
    required = (
        "source_execution_failure_diagnosis_digest", "source_prior_blocked_detail_binding_execution_digest",
        "source_prior_blocked_detail_binding_manifest_digest", "source_planning_results_review_digest",
        "source_method_execution_manifest_digest", "source_targeted_diagnostic_output_capture_execution_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
    )
    assert all(candidate[key] for key in required)
    assert candidate["source_durable_receipt_path"]
    assert candidate["diagnostic_receipt_parsed_in_candidate"] is False


def test_retry_priority_diagnostic_observable_and_workstream_context_is_bound() -> None:
    candidate = _candidate()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(candidate["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]) == 612
    assert candidate["top_10_count_sum"] == 1069
    assert candidate["failed_or_errored_nodeids_count"] == 1404
    assert candidate["module_summary_module_count"] == 29
    assert candidate["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert candidate["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert candidate["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert candidate["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert len(candidate["reviewed_observable_failure_families"]) == 4
    assert {item["confidence"] for item in candidate["reviewed_observable_failure_families"]} == {"HIGH"}
    assert sum(item["observable_evidence_count"] for item in candidate["reviewed_observable_failure_families"]) == 188
    assert len(candidate["reviewed_workstreams"]) == 4


def test_acquisition_scope_requirements_and_zero_coverage_are_preserved() -> None:
    candidate = _candidate()
    assert candidate["acquisition_scope_section_count"] == 4
    assert candidate["mapped_missing_authority_item_count"] == 30
    assert candidate["acceptable_source_artifact_type_count"] == 13
    assert candidate["operator_provided_evidence_requirement_count"] == 10
    assert candidate["evidence_custody_and_digest_requirement_count"] == 6
    assert candidate["candidate_results_review_requirement_count"] == 16
    coverage = candidate["missing_authority_coverage"]
    assert coverage["covered_missing_authority_item_count"] == 0
    assert coverage["uncovered_missing_authority_item_count"] == 30
    assert coverage["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert len(coverage["items"]) == 30
    assert {item["coverage_status"] for item in coverage["items"]} == {"MISSING_NOT_ACQUIRED"}


def test_package_options_are_reviewable_but_never_selected() -> None:
    candidate = _candidate()
    options = candidate["reviewed_package_options"]
    assert len(options) == candidate["package_option_count"] == 12
    assert sum(item["source_status"] != "BLOCKED_NOT_ALLOWED" for item in options) == candidate["available_package_count"] == 7
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in options) == candidate["blocked_package_count"] == 5
    assert all(not item[field] for item in options for field in ("selected", "approved", "authorized", "executed"))
    recommended = next(item for item in options if item["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["candidate_review_status"] == "CANDIDATE_RECOMMENDED_NOT_SELECTED"


def test_future_contracts_remain_unexecuted() -> None:
    candidate = _candidate()
    assert [item["requirement_id"] for item in candidate["future_evidence_package_preparation_requirements"]] == list(service.FUTURE_REQUIREMENT_IDS)
    assert {item["execution_status"] for item in candidate["future_evidence_package_preparation_requirements"]} == {"NOT_EXECUTED"}
    assert {item["plan_status"] for item in candidate["future_plan"]} == {"PLANNED_NOT_EXECUTED"}
    assert {item["generation_status"] for item in candidate["planned_outputs"]} == {"PLANNED_NOT_GENERATED"}
    assert all(item["active"] is True for item in candidate["non_goals"])


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
    assert {item["status"] for item in candidate["outputs"]} == {"GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_ONLY"}
    assert candidate["recommended_operator_source_authority_evidence_package_preparation_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert candidate["recommended_next_task"] == service.RECOMMENDED_TASK
    assert candidate["next_chain"] == list(service.NEXT_CHAIN)
    assert candidate["next_gates"] == list(service.NEXT_GATES)
    assert candidate["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_summary_and_digests_are_deterministic() -> None:
    first, second = _candidate(), _candidate()
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in first["checklist"])
    assert first["summary"]["total_checks"] == first["summary"]["passed_checks"]
    assert first["summary"]["failed_checks"] == 0
    for key in (service.CANDIDATE_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY, service.TEMPLATE_REQUIREMENTS_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64
        assert first[key] == second[key]


def test_validator_accepts_valid_candidate() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1(_candidate())
    assert result["candidate_status"] == service.CANDIDATE_STATUS
    assert result["failed_checks"] == 0


def test_builder_does_not_call_prohibited_public_source_builder(monkeypatch) -> None:
    def prohibited(**_kwargs):
        raise AssertionError("public source diagnosis builder must not be called")
    monkeypatch.setattr(service.source, "build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1", prohibited)
    assert _candidate()["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST


SOURCE_SCALAR_FIELDS = tuple(
    key for key, value in _candidate().items()
    if key.startswith("source_") and isinstance(value, (str, int, bool))
)


@pytest.mark.parametrize("field", SOURCE_SCALAR_FIELDS)
def test_validator_rejects_changed_source_scalar(field: str) -> None:
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


@pytest.mark.parametrize("field", (
    "artifact_kind", "candidate_status", "candidate_scope", "primary_failure_class",
    "secondary_failure_classes", "reviewed_package_options", "future_evidence_package_preparation_requirements",
    "future_plan", "planned_outputs", "non_goals", "outputs", "recommended_next_task", "next_chain",
    "next_gates", "risk_controls", "missing_authority_coverage", "retry_failure_context",
    "priority_1_target_modules", "priority1_validation_summary", "diagnostic_capture_evidence_summary",
    "reviewed_observable_failure_families", "reviewed_workstreams",
))
def test_validator_rejects_changed_contract_field(field: str) -> None:
    candidate = _candidate()
    candidate[field] = _changed(candidate[field])
    _reject(candidate)


def test_validator_rejects_missing_digest() -> None:
    candidate = _candidate()
    candidate.pop(service.MANIFEST_DIGEST_KEY)
    _reject(candidate)


def test_injected_source_diagnosis_must_match_committed_source() -> None:
    diagnosis = deepcopy(service._COMMITTED_SOURCE_FAILURE_DIAGNOSIS)
    diagnosis[service.source.DIAGNOSIS_DIGEST_KEY] = "0" * 64
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1(source_failure_diagnosis=diagnosis)


def test_markdown_contains_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_markdown_v1(_candidate())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Candidate")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_uses_only_requested_status_destination(tmp_path) -> None:
    candidate = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_CANDIDATE_AFTER_BLOCKED_ACQUISITION_EXECUTION_STATUS.md"
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(protected: str, tmp_path) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_candidate_after_blocked_acquisition_execution_v1(tmp_path / protected)
