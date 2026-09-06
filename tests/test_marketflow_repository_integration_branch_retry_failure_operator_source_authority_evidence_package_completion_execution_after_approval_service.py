from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_service
    as service,
)


def _blocked() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1()


def _valid_inputs() -> dict:
    review = service._committed_source_review()
    templates = {row["mapped_missing_authority_id"]: row for row in review["reviewed_template_rows"]}
    rows = []
    for index, mapping in enumerate(review["missing_authority_mapping"], 1):
        missing_id = mapping["missing_authority_id"]
        rows.append({
            "evidence_id": f"TEST-EVIDENCE-{index:02d}",
            "mapped_missing_authority_id": missing_id,
            "section_id": mapping["section_id"],
            "workstream_id": mapping["workstream_id"],
            "acceptable_source_artifact_type": templates[missing_id]["allowed_acceptable_source_artifact_types"][0],
            "source_owner_or_origin": "TEST_OPERATOR",
            "source_reference": f"test-fixture-reference-{index:02d}",
            "digest_or_reproducible_provenance": f"sha256:{index:064x}",
            "evidence_classification": "SPECIFICATION",
            "specification_or_observation": "SPECIFICATION",
            "expected_or_actual_scope": "EXPECTED",
            "authority_statement": f"Synthetic test authority statement {index:02d}",
            "results_review_required_before_use": True,
            "direct_change_authorized_now": False,
            "remediation_authorized_now": False,
            "retry_authorized_now": False,
            "main_merge_authorized_now": False,
            "actual_evidence_supplied": True,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "COMPLETED_OPERATOR_INPUT_PENDING_RESULTS_REVIEW",
        })
    return {
        "test_fixture_marker": "TEST_ONLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_NOT_REAL_SOURCE_AUTHORITY",
        "package_header": {
            "package_source_owner_or_origin": "TEST_OPERATOR",
            "package_reference": "test-fixture-package-reference",
            "package_created_utc": "2026-08-23T00:00:00Z",
            "package_digest_or_reproducible_provenance": "sha256:" + "a" * 64,
            "package_declares_no_secrets": True,
            "package_declares_no_api_keys": True,
            "package_declares_no_broker_credentials": True,
            "package_declares_no_personal_financial_credentials": True,
            "package_distinguishes_specification_from_observation": True,
            "package_distinguishes_expected_from_actual": True,
            "package_distinguishes_source_authority_from_diagnostic_output": True,
        },
        "evidence_items": rows,
    }


def _success() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(
        operator_completion_inputs=_valid_inputs()
    )


def test_actual_execution_is_blocked_offline_without_inputs() -> None:
    artifact = _blocked()
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["execution_status"] == service.BLOCKED_STATUS
    assert artifact["execution_scope"] == service.EXECUTION_SCOPE
    assert artifact["blocked_reason"] == service.NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED
    assert artifact["created_offline"] is True
    assert artifact["governance_only"] is True
    assert artifact["execution_attempted"] is True
    assert artifact["execution_blocked"] is True


@pytest.mark.parametrize("field,expected", [
    ("source_approval_commit", service.SOURCE_APPROVAL_COMMIT),
    ("source_approval_digest", service.SOURCE_APPROVAL_DIGEST),
    ("source_attestation_digest", service.SOURCE_ATTESTATION_DIGEST),
    ("selected_operator_source_authority_evidence_package_completion_package", service.SELECTED_PACKAGE),
    ("source_operator_review_commit", "d71bfb14a656592ab637d94d9dd30d73912104b0"),
    ("source_operator_review_digest", "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663"),
    ("source_completion_candidate_commit", "7af6b1b5ad223f92da0997e2b7abcb73543470df"),
    ("source_completion_candidate_digest", "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207"),
    ("source_results_review_digest", "a33038171faf25b4b077d5c0c7c5ecaf794d655d5007d92b1fbc7c6bf38db332"),
    ("source_execution_digest", "2f4fac84f615fa6ccf8210a802842ed1bbf1814333ae41afe78247fc39170ae3"),
    ("source_failure_diagnosis_digest", "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c"),
    ("source_blocked_acquisition_execution_reason", "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"),
    ("source_blocked_acquisition_execution_manifest_digest", "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"),
    ("source_acquisition_approval_digest", "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"),
    ("source_follow_on_results_review_digest", "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"),
    ("source_enrichment_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
    ("historical_source_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
    ("source_durable_receipt_path", "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"),
])
def test_source_bindings_are_preserved(field: str, expected: object) -> None:
    assert _blocked()[field] == expected


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
def test_blocked_counts_and_diagnostic_context(field: str, expected: object) -> None:
    assert _blocked()[field] == expected


@pytest.mark.parametrize("field", service.ALWAYS_FALSE_FIELDS + service.BLOCKED_ONLY_FALSE_FIELDS)
def test_blocked_authority_and_action_boundaries_remain_false(field: str) -> None:
    assert _blocked()[field] is False


def test_blocked_context_and_count_distinctions() -> None:
    artifact = _blocked()
    assert len(artifact["priority_1_target_modules"]) == 5
    assert len(artifact["reviewed_observable_failure_families"]) == 4
    assert len(artifact["reviewed_workstreams"]) == 4
    assert len(artifact["reviewed_template_rows"]) == 30
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in artifact["missing_authority_mapping"])
    assert artifact["count_label_distinction"]["preserved_without_reconciliation"] is True
    assert artifact["diagnostic_receipt_parsed_in_execution"] is False


def test_blocked_outputs_recommendation_chain_and_controls() -> None:
    artifact = _blocked()
    assert [item["output_id"] for item in artifact["outputs"]] == list(service.BLOCKED_OUTPUT_IDS)
    assert all(item["status"].endswith("BLOCKED_ONLY") for item in artifact["outputs"])
    assert len(artifact["next_chain"]) == 13
    assert len(artifact["next_gates"]) == 16
    assert set(service.RISK_CONTROLS) == set(artifact["risk_controls"])
    assert artifact["recommended_next_task"].endswith("FAILURE_DIAGNOSIS_V1")


def test_blocked_checklist_and_digests_are_deterministic() -> None:
    first, second = _blocked(), _blocked()
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == 0
    assert first[service.BLOCKED_DIGEST_KEY] == second[service.BLOCKED_DIGEST_KEY]
    assert first[service.BLOCKED_MANIFEST_DIGEST_KEY] == second[service.BLOCKED_MANIFEST_DIGEST_KEY]
    assert all(key not in first for key in (
        service.EXECUTION_DIGEST_KEY, service.COMPLETED_PACKAGE_DIGEST_KEY,
        service.COMPLETED_ITEMS_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ))


def test_valid_synthetic_inputs_create_test_only_success_path() -> None:
    artifact = _success()
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
    assert artifact["execution_status"] == service.EXECUTION_STATUS
    assert artifact["blocked_reason"] is None
    assert artifact["operator_completion_inputs_summary"]["test_fixture_marker"] == "TEST_ONLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_NOT_REAL_SOURCE_AUTHORITY"
    assert artifact["operator_completion_inputs_provided"] is True
    assert artifact["operator_completion_inputs_validated"] is True
    assert artifact["operator_completion_inputs_bound"] is True
    assert artifact["operator_source_authority_evidence_package_completion_executed"] is True
    assert artifact["operator_source_authority_evidence_package_completed"] is True
    assert artifact["completed_operator_evidence_item_count"] == 30
    assert artifact["actual_covered_missing_authority_item_count"] == 30
    assert artifact["actual_uncovered_missing_authority_item_count"] == 0
    assert artifact["ready_for_operator_source_authority_evidence_package_completion_results_review"] is True
    assert artifact["ready_for_source_authority_acquisition_execution_retry"] is False


def test_success_rows_cover_exact_reviewed_mapping_and_keep_boundaries_closed() -> None:
    artifact = _success()
    items = artifact["completed_operator_evidence_items"]
    assert {item["mapped_missing_authority_id"] for item in items} == {f"MA-{index:03d}" for index in range(1, 31)}
    assert all(item["actual_evidence_supplied"] is True for item in items)
    assert all(item["actual_evidence_validated"] is False for item in items)
    assert all(item["actual_evidence_bound"] is False for item in items)
    assert all(item["results_review_required_before_use"] is True for item in items)
    for item in items:
        assert item["direct_change_authorized_now"] is False
        assert item["remediation_authorized_now"] is False
        assert item["retry_authorized_now"] is False
        assert item["main_merge_authorized_now"] is False
    assert all(artifact[field] is False for field in service.ALWAYS_FALSE_FIELDS)


def test_validators_accept_both_paths() -> None:
    assert service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(_blocked())["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(_success())["failed_checks"] == 0


@pytest.mark.parametrize("field,value", [
    ("artifact_kind", "WRONG"), ("execution_status", "WRONG"), ("execution_scope", "WRONG"),
    ("blocked_reason", "WRONG"), ("source_approval_digest", "0" * 64),
    ("source_attestation_digest", "0" * 64),
    ("selected_operator_source_authority_evidence_package_completion_package", "WRONG"),
    ("source_operator_review_digest", "0" * 64), ("source_completion_candidate_digest", "0" * 64),
    ("source_results_review_digest", "0" * 64), ("source_execution_digest", "0" * 64),
    ("source_failure_diagnosis_digest", "0" * 64),
    ("source_blocked_acquisition_execution_reason", "WRONG"),
    ("retry_pytest_failed_count", 0), ("priority_1_total_nodeids", 0),
    ("source_stdout_byte_count", 0), ("observable_failure_family_count", 0),
    ("reviewed_template_row_count", 29), ("actual_covered_missing_authority_item_count", 1),
    ("operator_completion_inputs_provided", True), ("operator_source_authority_evidence_package_validated", True),
    ("source_authority_acquisition_performed", True), ("concrete_source_authority_established", True),
    ("production_code_modified", True), ("pytest_performed_in_execution", True),
    ("cache_read_in_execution", True), ("terminal_logs_parsed", True),
    ("env_inspection_performed", True), ("root_cause_claimed", True),
    ("retry_success_claimed", True), ("new_retry_candidate_created", True),
    ("main_merge_approval_created", True), ("provider_requests_made_in_execution", True),
    ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
])
def test_validator_rejects_mutated_blocked_artifact(field: str, value: object) -> None:
    artifact = _blocked()
    artifact[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(artifact)


@pytest.mark.parametrize("field", ["outputs", "recommended_next_task", "next_chain", "next_gates", "risk_controls"])
def test_validator_rejects_missing_required_collection_or_recommendation(field: str) -> None:
    artifact = _blocked()
    artifact.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(artifact)


@pytest.mark.parametrize("mutation,expected_reason", [
    (lambda value: value["evidence_items"].pop(), "OPERATOR_COMPLETION_INPUTS_INCOMPLETE"),
    (lambda value: value["evidence_items"][0].update(mapped_missing_authority_id="MA-999"), "OPERATOR_COMPLETION_INPUTS_INVALID_MISSING_AUTHORITY_MAPPING"),
    (lambda value: value["evidence_items"][0].update(section_id="wrong"), "OPERATOR_COMPLETION_INPUTS_INVALID_SECTION_ID"),
    (lambda value: value["evidence_items"][0].update(workstream_id="wrong"), "OPERATOR_COMPLETION_INPUTS_INVALID_WORKSTREAM_ID"),
    (lambda value: value["evidence_items"][0].update(acceptable_source_artifact_type="wrong"), "OPERATOR_COMPLETION_INPUTS_INVALID_ARTIFACT_TYPE"),
    (lambda value: value["evidence_items"][0].update(evidence_classification="wrong"), "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"),
    (lambda value: value["evidence_items"][0].update(expected_or_actual_scope="wrong"), "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"),
    (lambda value: value["evidence_items"][0].update(direct_change_authorized_now=True), "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_DIRECT_CHANGE"),
    (lambda value: value["evidence_items"][0].update(remediation_authorized_now=True), "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_REMEDIATION"),
    (lambda value: value["evidence_items"][0].update(retry_authorized_now=True), "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_RETRY"),
    (lambda value: value["evidence_items"][0].update(main_merge_authorized_now=True), "OPERATOR_COMPLETION_INPUTS_ATTEMPT_TO_AUTHORIZE_MAIN_MERGE"),
    (lambda value: value["evidence_items"][0].update(actual_evidence_validated=True), "TEMPLATE_COMPLETION_BOUNDARY_FAILURE"),
    (lambda value: value["package_header"].update(package_source_owner_or_origin=""), "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_OWNER_OR_ORIGIN"),
    (lambda value: value["package_header"].update(package_reference=""), "OPERATOR_COMPLETION_INPUTS_MISSING_SOURCE_REFERENCE"),
    (lambda value: value["package_header"].update(package_digest_or_reproducible_provenance=""), "OPERATOR_COMPLETION_INPUTS_MISSING_DIGEST_OR_REPRODUCIBLE_PROVENANCE"),
    (lambda value: value["evidence_items"][0].update(authority_statement=""), "OPERATOR_COMPLETION_INPUTS_MISSING_AUTHORITY_STATEMENT"),
])
def test_invalid_inputs_fail_closed(mutation, expected_reason: str) -> None:
    inputs = _valid_inputs()
    mutation(inputs)
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(operator_completion_inputs=inputs)
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["blocked_reason"] == expected_reason
    assert artifact["operator_source_authority_evidence_package_created"] is False


@pytest.mark.parametrize("field,value,reason", [
    ("source_reference", "api_key=sk-abcdefghijklmnop", "OPERATOR_COMPLETION_INPUTS_CONTAIN_API_KEYS"),
    ("source_reference", "IBKR broker credential", "OPERATOR_COMPLETION_INPUTS_CONTAIN_BROKER_CREDENTIALS"),
    ("source_reference", "account number 12345", "OPERATOR_COMPLETION_INPUTS_CONTAIN_PERSONAL_FINANCIAL_CREDENTIALS"),
    ("source_reference", "market data credential", "OPERATOR_COMPLETION_INPUTS_CONTAIN_MARKET_DATA_CREDENTIALS"),
    ("source_reference", "private token abc", "OPERATOR_COMPLETION_INPUTS_CONTAIN_PRIVATE_TOKENS"),
    ("source_reference", "password=hunter2", "OPERATOR_COMPLETION_INPUTS_CONTAIN_SECRETS"),
])
def test_secret_or_credential_red_flags_fail_closed(field: str, value: str, reason: str) -> None:
    inputs = _valid_inputs()
    inputs["evidence_items"][0][field] = value
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(operator_completion_inputs=inputs)
    assert artifact["blocked_reason"] == reason
    assert artifact["completed_operator_evidence_package"] is None
    assert artifact["completed_operator_evidence_items"] == []


def test_validator_rejects_mutated_success_input_and_authority_boundary() -> None:
    artifact = _success()
    artifact["completed_operator_evidence_items"][0]["mapped_missing_authority_id"] = "MA-999"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(artifact)


def test_markdown_contains_required_sections_without_full_input_payload() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_markdown_v1(_blocked())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert "Full inputs are intentionally not rendered" in markdown


def test_writer_writes_only_status_markdown(tmp_path: Path) -> None:
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_execution_after_approval_v1(tmp_path)
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_EXECUTION_AFTER_APPROVAL_STATUS.md"
    assert output.is_file()
    assert artifact["blocked_reason"] == service.NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED
    assert list(tmp_path.iterdir()) == [output]
