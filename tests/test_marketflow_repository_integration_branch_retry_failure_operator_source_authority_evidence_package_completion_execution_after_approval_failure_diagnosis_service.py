from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_service
    as service,
)


def _diagnosis() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1()


def test_builds_offline_failure_diagnosis_from_committed_projection() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["artifact_kind"] == service.ARTIFACT_KIND
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert diagnosis["diagnosis_scope"] == service.DIAGNOSIS_SCOPE
    assert diagnosis["created_offline"] is True
    assert diagnosis["governance_only"] is True
    assert diagnosis["failure_diagnosis_only"] is True


@pytest.mark.parametrize("field,expected", [
    ("source_completion_execution_commit", service.SOURCE_COMPLETION_EXECUTION_COMMIT),
    ("source_completion_execution_artifact_kind", service.source.BLOCKED_ARTIFACT_KIND),
    ("source_completion_execution_status", service.source.BLOCKED_STATUS),
    ("source_completion_execution_scope", service.source.EXECUTION_SCOPE),
    ("source_completion_execution_blocked_reason", service.PRIMARY_FAILURE_CLASS),
    ("source_completion_execution_blocked_digest", service.SOURCE_COMPLETION_EXECUTION_BLOCKED_DIGEST),
    ("source_completion_execution_blocked_manifest_digest", service.SOURCE_COMPLETION_EXECUTION_BLOCKED_MANIFEST_DIGEST),
    ("source_completion_execution_success_digests_absent", True),
    ("source_approval_commit", "40bee1289543bb07e64e383eb2e1c61d83615bd5"),
    ("source_approval_digest", "f6c37c0a7c64487cdf9adb218f8d12b8c0a2dacc4d4c1debf96105d1b5ee954c"),
    ("source_attestation_digest", "5434cbb4c94d22f1e4fefb3efc0e6e651401a22d6217d4c118638fa6d38dc714"),
    ("selected_operator_source_authority_evidence_package_completion_package", service.SELECTED_PACKAGE),
    ("source_operator_review_commit", "d71bfb14a656592ab637d94d9dd30d73912104b0"),
    ("source_operator_review_digest", "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663"),
    ("source_completion_candidate_commit", "7af6b1b5ad223f92da0997e2b7abcb73543470df"),
    ("source_completion_candidate_digest", "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207"),
    ("source_results_review_digest", "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332"),
    ("source_template_review_digest", "3e60c8bb9c9000f6d5ca561ae843c17ec4abd31276fa443d7b9d97b7524040b9"),
    ("source_execution_digest", "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3"),
    ("source_package_template_digest", "fb406078ca1a1199a430dd836050f9b198373c1f46c19cb5ee899ffe7e975a9a"),
    ("source_preparation_candidate_digest", "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391"),
    ("source_failure_diagnosis_digest", "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c"),
    ("source_blocked_acquisition_execution_reason", "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"),
    ("source_blocked_acquisition_execution_manifest_digest", "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"),
    ("source_acquisition_approval_digest", "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"),
    ("source_follow_on_results_review_digest", "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"),
    ("source_enrichment_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
    ("historical_source_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
    ("historical_blocked_remediation_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
    ("source_durable_receipt_path", "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"),
])
def test_source_chain_is_bound(field: str, expected: object) -> None:
    assert _diagnosis()[field] == expected


@pytest.mark.parametrize("field,expected", [
    ("retry_pytest_passed_count", 24877), ("retry_pytest_failed_count", 1292),
    ("retry_pytest_error_count", 112), ("retry_pytest_skipped_count", 7),
    ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
    ("failed_or_errored_nodeids_count", 1404), ("module_summary_module_count", 29),
    ("priority1_pre_change_validation_passed_count", 675),
    ("priority1_post_change_validation_passed_count", 675),
    ("source_exit_code", 1), ("source_stdout_byte_count", 1231380),
    ("source_stderr_byte_count", 0), ("observable_failure_family_count", 4),
    ("total_observable_evidence_items", 188), ("reviewed_template_row_count", 30),
    ("actual_covered_missing_authority_item_count", 0),
    ("actual_uncovered_missing_authority_item_count", 30),
    ("completed_operator_evidence_item_count", 0),
])
def test_counts_and_diagnostic_metadata_are_bound(field: str, expected: object) -> None:
    assert _diagnosis()[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_diagnosis_facts_are_true(field: str) -> None:
    assert _diagnosis()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_actions_authorities_and_unsupported_claims_are_false(field: str) -> None:
    assert _diagnosis()[field] is False


def test_failure_classification_domains_and_findings_are_complete() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert diagnosis["secondary_failure_classes"] == list(service.SECONDARY_FAILURE_CLASSES)
    assert len(diagnosis["diagnosis_domains"]) == 13
    assert {item["domain_id"] for item in diagnosis["diagnosis_domains"]} == {item[0] for item in service.DIAGNOSIS_DOMAINS}
    assert next(item for item in diagnosis["diagnosis_domains"] if item["domain_id"] == "operator_completion_input_availability")["disposition"] == "FAILED_PRIMARY"
    assert len(diagnosis["diagnosis_findings"]) == 20


def test_absence_coverage_template_and_synthetic_boundaries() -> None:
    diagnosis = _diagnosis()
    assert diagnosis["operator_completion_input_absence_diagnosis"]["fail_closed_behavior_correct"] is True
    assert diagnosis["operator_completion_input_absence_diagnosis"]["approval_is_operator_completion_inputs"] is False
    assert diagnosis["synthetic_success_path_boundary"]["test_only"] is True
    assert diagnosis["synthetic_success_path_boundary"]["repository_evidence"] is False
    assert diagnosis["coverage_diagnosis"]["all_missing_authority_items_remain_missing"] is True
    assert len(diagnosis["reviewed_template_rows"]) == 30
    assert len(diagnosis["missing_authority_mapping"]) == 30
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in diagnosis["missing_authority_mapping"])
    assert diagnosis["count_label_distinction"]["preserved_without_reconciliation"] is True


def test_outputs_recommendation_next_chain_gates_and_controls() -> None:
    diagnosis = _diagnosis()
    assert [item["output_id"] for item in diagnosis["outputs"]] == list(service.OUTPUT_IDS)
    assert all(item["status"] == "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_FAILURE_DIAGNOSIS_ONLY" for item in diagnosis["outputs"])
    assert diagnosis["recommended_next_task"].endswith("PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_V1")
    assert diagnosis["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert len(diagnosis["next_chain"]) == 13
    assert len(diagnosis["next_gates"]) == 17
    assert diagnosis["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_passes_and_all_digests_are_deterministic() -> None:
    first, second = _diagnosis(), _diagnosis()
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == 0
    assert first["summary"]["blocker_count"] == 0
    for key in (
        service.DIAGNOSIS_DIGEST_KEY, service.FAILURE_CLASSIFICATION_DIGEST_KEY,
        service.OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY,
        service.COVERAGE_DIAGNOSIS_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64


def test_source_projection_rejects_success_digests_and_changed_bindings() -> None:
    source_execution = service._committed_source_completion_execution()
    source_execution[service.source.EXECUTION_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(source_completion_execution=source_execution)


@pytest.mark.parametrize("field,value", [
    ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"), ("diagnosis_scope", "WRONG"),
    ("source_completion_execution_commit", "0" * 40),
    ("source_completion_execution_artifact_kind", "WRONG"),
    ("source_completion_execution_status", "WRONG"),
    ("source_completion_execution_scope", "WRONG"),
    ("source_completion_execution_blocked_reason", "WRONG"),
    ("source_completion_execution_blocked_digest", "0" * 64),
    ("source_completion_execution_blocked_manifest_digest", "0" * 64),
    ("source_completion_execution_success_digests_absent", False),
    ("primary_failure_class", "WRONG"), ("source_approval_digest", "0" * 64),
    ("source_attestation_digest", "0" * 64),
    ("selected_operator_source_authority_evidence_package_completion_package", "WRONG"),
    ("source_operator_review_digest", "0" * 64),
    ("source_completion_candidate_digest", "0" * 64),
    ("source_results_review_digest", "0" * 64), ("source_execution_digest", "0" * 64),
    ("source_failure_diagnosis_digest", "0" * 64),
    ("source_blocked_acquisition_execution_reason", "WRONG"),
    ("retry_pytest_failed_count", 0), ("priority_1_total_nodeids", 0),
    ("source_stdout_byte_count", 0), ("observable_failure_family_count", 0),
    ("reviewed_template_row_count", 29), ("actual_covered_missing_authority_item_count", 1),
    ("operator_completion_inputs_provided", True), ("operator_completion_inputs_validated", True),
    ("operator_completion_inputs_bound", True), ("completion_execution_rerun_performed", True),
    ("operator_source_authority_evidence_package_completion_executed", True),
    ("operator_source_authority_evidence_package_created", True), ("actual_evidence_items_filled", True),
    ("source_authority_acquisition_performed", True), ("source_authority_evidence_acquired", True),
    ("external_evidence_acquired", True), ("concrete_source_authority_established", True),
    ("safe_source_authority_bound_change_identified", True), ("remediation_execution_performed", True),
    ("production_code_modified", True), ("existing_tests_modified", True),
    ("expected_digests_updated", True), ("patch_generated", True),
    ("pytest_performed_in_diagnosis", True), ("retry_rerun_performed", True),
    ("cache_read_in_diagnosis", True), ("terminal_logs_parsed", True),
    ("env_inspection_performed", True), ("diagnostic_receipt_parsed_in_diagnosis", True),
    ("source_owners_contacted", True), ("provider_requests_made_in_diagnosis", True),
    ("root_cause_claimed", True), ("retry_success_claimed", True),
    ("main_merge_readiness_claimed", True), ("new_retry_candidate_created", True),
    ("retry_approval_created", True), ("new_retry_executed", True),
    ("new_retry_results_review_created", True), ("main_merge_approval_created", True),
    ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
])
def test_validator_rejects_mutation(field: str, value: object) -> None:
    diagnosis = _diagnosis()
    diagnosis[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(diagnosis)


@pytest.mark.parametrize("field", [
    "secondary_failure_classes", "diagnosis_domains", "diagnosis_findings", "outputs",
    "recommended_next_task", "next_chain", "next_gates", "risk_controls",
    service.DIAGNOSIS_DIGEST_KEY, service.FAILURE_CLASSIFICATION_DIGEST_KEY,
    service.OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY,
    service.COVERAGE_DIAGNOSIS_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
])
def test_validator_rejects_missing_required_content(field: str) -> None:
    diagnosis = _diagnosis()
    diagnosis.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(diagnosis)


def test_validator_accepts_committed_diagnosis() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(_diagnosis())
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    assert result["failed_checks"] == 0


def test_markdown_contains_required_sections_and_boundaries() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_markdown_v1(_diagnosis())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.PRIMARY_FAILURE_CLASS in markdown
    assert "success digests absent" in markdown
    assert "was not parsed" in markdown


def test_writer_writes_only_status_markdown(tmp_path: Path) -> None:
    diagnosis = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_failure_diagnosis_v1(tmp_path)
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_STATUS.md"
    assert output.is_file()
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert list(tmp_path.iterdir()) == [output]
