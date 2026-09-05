from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_service
    as service,
)


Error = service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionFailureDiagnosisError


def _diagnosis() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1()


def _reject(diagnosis: dict) -> None:
    with pytest.raises(Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
            diagnosis
        )


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


def test_diagnosis_builds_offline_from_committed_source_constants() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["created_offline"] is True
    assert diagnosis["governance_only"] is True
    assert diagnosis["diagnosis_only"] is True


def test_artifact_status_scope_are_exact() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["artifact_kind"] == service.ARTIFACT_KIND
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert diagnosis["diagnosis_scope"] == service.DIAGNOSIS_SCOPE
    assert diagnosis["schema_version"] == service.SCHEMA_VERSION


def test_source_blocked_execution_identity_is_bound() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["source_blocked_execution_commit"] == service.SOURCE_BLOCKED_EXECUTION_COMMIT
    assert diagnosis["source_blocked_execution_artifact_kind"] == service.source.BLOCKED_ARTIFACT_KIND
    assert diagnosis["source_blocked_execution_status"] == service.source.BLOCKED_STATUS
    assert diagnosis["source_blocked_execution_scope"] == service.source.EXECUTION_SCOPE
    assert diagnosis["source_blocked_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST
    assert diagnosis["source_blocked_reason"] == service.PRIMARY_FAILURE_CLASS


def test_source_approval_and_selected_package_are_bound() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["source_approval_commit"] == service.source.SOURCE_APPROVAL_COMMIT
    assert diagnosis["source_approval_digest"] == service.source.SOURCE_APPROVAL_DIGEST
    assert diagnosis["source_attestation_digest"] == service.source.SOURCE_ATTESTATION_DIGEST
    assert diagnosis["selected_source_authority_acquisition_package"] == service.source.SELECTED_PACKAGE


def test_diagnosis_classification_is_exact() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert diagnosis["secondary_failure_classes"] == list(service.SECONDARY_FAILURE_CLASSES)
    assert diagnosis["diagnosis_classification"] == {
        "primary_failure_class": service.PRIMARY_FAILURE_CLASS,
        "secondary_failure_classes": list(service.SECONDARY_FAILURE_CLASSES),
    }


def test_historical_failure_classification_is_preserved() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["historical_primary_failure_class"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert len(diagnosis["historical_secondary_failure_classes"]) == 4
    assert diagnosis["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"


def test_evidence_package_availability_diagnosis_is_fail_closed() -> None:
    availability = _diagnosis()["evidence_package_availability_diagnosis"]
    assert availability["operator_source_authority_evidence_package_supplied"] is False
    assert availability["operator_source_authority_evidence_package_validated"] is False
    assert availability["operator_source_authority_evidence_package_bound"] is False
    assert availability["blocked_reason"] == service.PRIMARY_FAILURE_CLASS


def test_missing_authority_coverage_is_unchanged() -> None:
    diagnosis = _diagnosis()
    coverage = diagnosis["missing_authority_coverage_diagnosis"]
    assert coverage["covered_missing_authority_item_count"] == 0
    assert coverage["uncovered_missing_authority_item_count"] == 30
    assert coverage["mapped_missing_authority_item_count"] == 30
    assert coverage["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert len(coverage["items"]) == 30
    assert {item["coverage_status"] for item in coverage["items"]} == {"MISSING_NOT_ACQUIRED"}


def test_source_candidate_scope_and_requirement_counts_are_bound() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["acquisition_scope_section_count"] == 4
    assert diagnosis["mapped_missing_authority_item_count"] == 30
    assert diagnosis["acceptable_source_artifact_type_count"] == 13
    assert diagnosis["operator_provided_evidence_requirement_count"] == 10
    assert diagnosis["evidence_custody_and_digest_requirement_count"] == 6
    assert diagnosis["candidate_results_review_requirement_count"] == 16


def test_retry_priority_and_diagnostic_context_is_bound() -> None:
    diagnosis = _diagnosis()
    retry = diagnosis["retry_failure_context"]
    assert (retry["counts"]["passed"], retry["counts"]["failed"], retry["counts"]["errors"], retry["counts"]["skipped"]) == (24877, 1292, 112, 7)
    assert sum(item["failed_or_errored_nodeid_count"] for item in diagnosis["priority_1_target_modules"]) == 612
    assert diagnosis["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert diagnosis["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert diagnosis["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380


def test_observable_families_and_workstreams_are_preserved() -> None:
    diagnosis = _diagnosis()
    assert len(diagnosis["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in diagnosis["reviewed_observable_failure_families"]) == 188
    assert {item["confidence"] for item in diagnosis["reviewed_observable_failure_families"]} == {"HIGH"}
    assert len(diagnosis["reviewed_workstreams"]) == 4


def test_diagnosis_findings_and_domains_are_complete() -> None:
    diagnosis = _diagnosis()
    assert len(diagnosis["diagnosis_findings"]) == 20
    assert len(diagnosis["diagnosis_domains"]) == 13
    assert {item["domain_id"] for item in diagnosis["diagnosis_domains"]} == {item[0] for item in service.DOMAINS}
    assert next(item for item in diagnosis["diagnosis_domains"] if item["domain_id"] == "evidence_package_availability")["disposition"] == "FAILED_PRIMARY"


def test_outputs_recommendation_chain_gates_and_risks_are_complete() -> None:
    diagnosis = _diagnosis()
    assert [item["output_id"] for item in diagnosis["outputs"]] == list(service.OUTPUT_IDS)
    assert {item["status"] for item in diagnosis["outputs"]} == {"GENERATED_SOURCE_AUTHORITY_ACQUISITION_FAILURE_DIAGNOSIS_ONLY"}
    assert diagnosis["recommended_next_package"] == service.RECOMMENDED_PACKAGE
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_TASK
    assert diagnosis["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert len(diagnosis["next_chain"]) == 13
    assert diagnosis["next_gates"] == list(service.NEXT_GATES)
    assert diagnosis["risk_controls"] == list(service.RISK_CONTROLS)


def test_all_true_and_false_authority_fields_are_exact() -> None:
    diagnosis = _diagnosis()
    assert all(diagnosis[field] is True for field in service.TRUE_FIELDS)
    assert all(diagnosis[field] is False for field in service.FALSE_FIELDS)
    assert diagnosis["predictive_usefulness"] == "not accepted"
    assert diagnosis["profitability"] == "not accepted"
    assert {diagnosis[field] for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_digests_are_present_and_deterministic() -> None:
    first, second = _diagnosis(), _diagnosis()
    for key in (
        service.DIAGNOSIS_DIGEST_KEY,
        service.FAILURE_CLASSIFICATION_DIGEST_KEY,
        service.MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY,
        service.COVERAGE_DIAGNOSIS_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert len(first[key]) == 64
        assert first[key] == second[key]


def test_checklist_and_summary_pass() -> None:
    diagnosis = _diagnosis()
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in diagnosis["checklist"])
    assert diagnosis["summary"]["passed_checks"] == diagnosis["summary"]["total_checks"]
    assert diagnosis["summary"]["failed_checks"] == 0
    assert diagnosis["summary"]["blocker_count"] == 0
    assert diagnosis["summary"]["recommended_next_task"] == service.RECOMMENDED_TASK


def test_validator_accepts_valid_diagnosis() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(_diagnosis())
    assert result["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert result["failed_checks"] == 0


def test_builder_does_not_call_prohibited_source_execution(monkeypatch) -> None:
    def prohibited(**_kwargs):
        raise AssertionError("source execution must not be called")

    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_v1",
        prohibited,
    )
    assert _diagnosis()["source_blocked_reason"] == service.PRIMARY_FAILURE_CLASS


SOURCE_SCALAR_FIELDS = tuple(
    key
    for key, value in _diagnosis().items()
    if key.startswith("source_") and isinstance(value, (str, int, bool))
)


@pytest.mark.parametrize("field", SOURCE_SCALAR_FIELDS)
def test_validator_rejects_changed_source_scalar(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = _changed(diagnosis[field])
    _reject(diagnosis)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_changed(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = False
    _reject(diagnosis)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_false_changed(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = True
    _reject(diagnosis)


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "schema_version", "diagnosis_status", "diagnosis_scope",
        "primary_failure_class", "historical_primary_failure_class",
        "selected_source_authority_acquisition_package", "missing_authority_items_status",
        "recommended_next_package", "recommended_next_task", "recommended_next_task_status",
        "recommended_action", "recommendation_reason", "predictive_usefulness", "profitability",
        "runtime_use", "strategy_use", "paper_trading", "broker_execution",
    ],
)
def test_validator_rejects_changed_top_level_scalar(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = "changed"
    _reject(diagnosis)


@pytest.mark.parametrize(
    "field",
    [
        "retry_failure_context", "priority_1_target_modules", "priority1_validation_summary",
        "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families",
        "reviewed_workstreams", "source_authority_acquisition_candidate_review",
        "acquisition_scope_sections_review", "missing_authority_to_source_evidence_mapping_review",
        "acceptable_source_artifact_inventory_review", "operator_provided_evidence_requirements_review",
        "evidence_custody_and_digest_requirements_review", "candidate_results_review_requirements_review",
        "diagnosis_classification", "diagnosis_findings", "diagnosis_domains",
        "evidence_package_availability_diagnosis", "missing_authority_coverage_diagnosis",
        "outputs", "next_chain", "next_gates", "risk_controls", "checklist", "summary",
    ],
)
def test_validator_rejects_changed_structured_evidence(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = _changed(diagnosis[field])
    _reject(diagnosis)


@pytest.mark.parametrize(
    "field",
    [
        "operator_source_authority_evidence_item_count", "covered_missing_authority_item_count",
        "uncovered_missing_authority_item_count", "mapped_missing_authority_item_count",
        "acquisition_scope_section_count", "acceptable_source_artifact_type_count",
        "operator_provided_evidence_requirement_count", "evidence_custody_and_digest_requirement_count",
        "candidate_results_review_requirement_count", "observable_failure_family_count",
        "total_observable_evidence_items", "priority_1_total_nodeids", "top_10_count_sum",
        "failed_or_errored_nodeids_count", "module_summary_module_count",
    ],
)
def test_validator_rejects_changed_count(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] += 1
    _reject(diagnosis)


def test_validator_rejects_missing_secondary_failure_class() -> None:
    diagnosis = _diagnosis()
    diagnosis["secondary_failure_classes"].pop()
    _reject(diagnosis)


def test_validator_rejects_missing_historical_secondary_failure_class() -> None:
    diagnosis = _diagnosis()
    diagnosis["historical_secondary_failure_classes"].pop()
    _reject(diagnosis)


@pytest.mark.parametrize(
    "key",
    [
        service.DIAGNOSIS_DIGEST_KEY,
        service.FAILURE_CLASSIFICATION_DIGEST_KEY,
        service.MISSING_EVIDENCE_PACKAGE_DIAGNOSIS_DIGEST_KEY,
        service.COVERAGE_DIAGNOSIS_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_or_missing_digest(key: str) -> None:
    changed = _diagnosis()
    changed[key] = "0" * 64
    _reject(changed)
    missing = _diagnosis()
    missing.pop(key)
    _reject(missing)


def test_exact_injected_source_blocked_execution_is_accepted_without_mutation() -> None:
    source_execution = deepcopy(service._COMMITTED_SOURCE_BLOCKED_EXECUTION)
    original = deepcopy(source_execution)
    diagnosis = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
        source_blocked_execution=source_execution
    )
    assert diagnosis["source_blocked_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST
    assert source_execution == original


def test_changed_injected_source_blocked_execution_is_rejected() -> None:
    source_execution = deepcopy(service._COMMITTED_SOURCE_BLOCKED_EXECUTION)
    source_execution["blocked_reason"] = "changed"
    with pytest.raises(Error):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
            source_blocked_execution=source_execution
        )


def test_markdown_contains_all_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_markdown_v1(_diagnosis())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Source Authority Acquisition Execution After Candidate Operator Review Failure Diagnosis v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_creates_diagnosis_status(tmp_path) -> None:
    diagnosis = service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_AFTER_CANDIDATE_OPERATOR_REVIEW_FAILURE_DIAGNOSIS_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(tmp_path, protected: str) -> None:
    with pytest.raises(Error):
        service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_execution_after_candidate_operator_review_failure_diagnosis_v1(
            tmp_path / protected
        )
