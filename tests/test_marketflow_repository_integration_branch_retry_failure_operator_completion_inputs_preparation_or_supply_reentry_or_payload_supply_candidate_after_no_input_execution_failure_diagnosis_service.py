from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_service
    as service,
)


def build_candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1()


def test_candidate_builds_offline_from_committed_constants():
    candidate = build_candidate()
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


def test_artifact_identity_status_and_scope():
    candidate = build_candidate()
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["schema_version"] == service.SCHEMA_VERSION
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE


def test_source_failure_diagnosis_is_bound():
    candidate = build_candidate()
    assert candidate["source_failure_diagnosis_commit"] == service.SOURCE_FAILURE_DIAGNOSIS_COMMIT
    assert candidate["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert candidate["source_failure_classification_digest"] == service.SOURCE_FAILURE_CLASSIFICATION_DIGEST
    assert candidate["source_input_absence_diagnosis_digest"] == service.SOURCE_INPUT_ABSENCE_DIAGNOSIS_DIGEST
    assert candidate["source_binding_review_digest"] == service.SOURCE_BINDING_REVIEW_DIGEST
    assert candidate["source_coverage_diagnosis_digest"] == service.SOURCE_COVERAGE_DIAGNOSIS_DIGEST
    assert candidate["source_failure_diagnosis_manifest_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST


def test_source_execution_and_block_are_bound():
    candidate = build_candidate()
    assert candidate["source_execution_commit"] == service.SOURCE_EXECUTION_COMMIT
    assert candidate["source_blocked_reason"] == service.SOURCE_BLOCKED_REASON
    assert candidate["source_blocked_digest"] == service.SOURCE_BLOCKED_DIGEST
    assert candidate["source_source_binding_digest"] == service.SOURCE_SOURCE_BINDING_DIGEST
    assert candidate["source_input_absence_digest"] == service.SOURCE_INPUT_ABSENCE_DIGEST
    assert candidate["source_coverage_digest"] == service.SOURCE_COVERAGE_DIGEST
    assert candidate["source_blocked_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST


def test_success_and_prepared_input_digests_remain_absent():
    candidate = build_candidate()
    assert candidate["source_success_digests_absent"] is True
    assert candidate["source_success_execution_digest"] is None
    assert candidate["source_prepared_operator_completion_inputs_digest"] is None
    assert candidate["source_prepared_operator_completion_inputs_manifest_digest"] is None


def test_failure_classes_are_preserved():
    candidate = build_candidate()
    assert candidate["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert tuple(candidate["secondary_failure_classes"]) == service.SECONDARY_FAILURE_CLASSES


def test_approval_review_candidate_and_completion_chains_are_bound():
    candidate = build_candidate()
    assert candidate["source_approval_commit"] == "6623e6a6acb0a8da85fee15a29a52606a7fc6af1"
    assert candidate["source_approval_digest"] == "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72"
    assert candidate["source_attestation_digest"] == "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af"
    assert candidate["source_operator_review_commit"] == "2efc22338250f9de88e76fbf6381796c82f817df"
    assert candidate["source_candidate_commit"] == "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1"
    assert candidate["source_completion_execution_commit"] == "945776b2164969e067d8dcc4809128282d3b1287"
    assert candidate["source_completion_approval_commit"] == "40bee1289543bb07e64e383eb2e1c61d83615bd5"
    assert candidate["source_completion_candidate_operator_review_commit"] == "d71bfb14a656592ab637d94d9dd30d73912104b0"
    assert candidate["source_completion_candidate_commit"] == "7af6b1b5ad223f92da0997e2b7abcb73543470df"


def test_template_preparation_acquisition_and_historical_chains_are_bound():
    candidate = build_candidate()
    assert candidate["source_template_preparation_results_review_commit"] == "268c84d7ef4ed550bb38f07670247540590885f6"
    assert candidate["source_template_preparation_execution_commit"] == "a39332feb29a23612ee51cb45e8d5663b144c638"
    assert candidate["source_preparation_candidate_digest"]
    assert candidate["source_previous_failure_diagnosis_digest"]
    assert candidate["source_acquisition_approval_digest"]
    assert candidate["source_follow_on_execution_digest"]
    assert candidate["source_enrichment_execution_digest"]
    assert candidate["historical_blocked_remediation_manifest_digest"]
    assert candidate["source_targeted_remediation_plan_digest"]
    assert candidate["source_recovery_results_review_digest"]


def test_durable_receipt_is_opaque_and_retry_facts_are_bound():
    candidate = build_candidate()
    assert candidate["source_durable_receipt_path"].endswith("RECEIPT_V1.json")
    assert candidate["durable_receipt_not_parsed"] is True
    assert candidate["diagnostic_receipt_parsed_in_candidate"] is False
    assert (candidate["retry_pytest_passed_count"], candidate["retry_pytest_failed_count"], candidate["retry_pytest_error_count"], candidate["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)


def test_priority_one_diagnostic_families_and_workstreams_are_preserved():
    candidate = build_candidate()
    assert len(candidate["priority_1_target_modules"]) == 5
    assert candidate["priority_1_total_nodeids"] == 612
    assert candidate["top_10_count_sum"] == 1069
    assert candidate["failed_or_errored_nodeids_count"] == 1404
    assert candidate["module_summary_module_count"] == 29
    assert candidate["priority1_pre_change_validation_passed_count"] == 675
    assert candidate["priority1_post_change_validation_passed_count"] == 675
    assert candidate["priority1_validation_is_retry_evidence"] is False
    assert candidate["source_exit_code"] == 1
    assert candidate["source_stdout_byte_count"] == 1231380
    assert candidate["source_stderr_byte_count"] == 0
    assert candidate["source_diagnostic_metadata_only"] is True
    assert len(candidate["reviewed_observable_failure_families"]) == 4
    assert len(candidate["reviewed_workstreams"]) == 4


def test_template_mapping_and_actual_coverage_remain_zero():
    candidate = build_candidate()
    assert candidate["reviewed_template_row_count"] == 30
    assert len(candidate["missing_authority_mapping"]) == 30
    assert candidate["actual_covered_missing_authority_item_count"] == 0
    assert candidate["actual_uncovered_missing_authority_item_count"] == 30
    assert candidate["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert candidate["count_label_distinction_preserved"] is True


def test_twelve_package_options_are_unselected_and_correctly_disposed():
    candidate = build_candidate()
    options = candidate["package_options"]
    assert len(options) == 12
    assert sum(item["candidate_status"] != "BLOCKED_NOT_ALLOWED" for item in options) == 7
    assert sum(item["candidate_status"] == "BLOCKED_NOT_ALLOWED" for item in options) == 5
    assert options[0]["package_id"] == service.RECOMMENDED_PACKAGE
    assert options[0]["candidate_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert all(not item[key] for item in options for key in ("selected", "approved", "authorized", "executed"))


def test_future_requirements_contract_plan_and_outputs_are_planning_only():
    candidate = build_candidate()
    assert len(candidate["future_requirements"]) == 62
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in candidate["future_requirements"])
    assert candidate["future_payload_supply_contract"]["contract_status"] == "PLANNING_ONLY_NOT_SUPPLIED"
    assert candidate["future_payload_supply_contract"]["future_evidence_item_count"] == 30
    assert candidate["future_payload_supply_contract"]["operator_input_supplied"] is False
    assert len(candidate["future_plan"]) == 15
    assert all(item["status"] == "PLANNED_NOT_EXECUTED" for item in candidate["future_plan"])
    assert len(candidate["planned_outputs"]) == 34
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])


def test_all_required_boundaries_and_outputs_are_active():
    candidate = build_candidate()
    assert all(candidate[key] is True for key in service.TRUE_FIELDS)
    assert all(candidate[key] is False for key in service.FALSE_FIELDS)
    assert all(item["active"] for item in candidate["non_goals"])
    assert set(service.RISK_CONTROLS).issubset(candidate["risk_controls"])
    assert [item["output_id"] for item in candidate["outputs"]] == list(service.OUTPUT_IDS)
    assert all(item["status"] == service.GENERATED_CANDIDATE_ONLY for item in candidate["outputs"])


def test_authority_and_acceptance_remain_closed():
    candidate = build_candidate()
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"
    assert candidate["paper_trading"] == "NOT_AUTHORIZED"
    assert candidate["broker_execution"] == "NOT_AUTHORIZED"
    assert candidate["ready_for_operator_completion_inputs_reentry_or_payload_supply_candidate_operator_review"] is True
    assert candidate["ready_for_operator_completion_inputs_reentry_or_payload_supply_approval"] is False
    assert candidate["ready_for_retry_candidate"] is False
    assert candidate["ready_for_main_merge_approval"] is False


def test_checklist_passes_and_summary_is_complete():
    candidate = build_candidate()
    assert candidate["summary"]["total_checks"] == len(candidate["checklist"])
    assert candidate["summary"]["passed_checks"] == candidate["summary"]["total_checks"]
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0


def test_digests_are_deterministic_and_sha256():
    first = build_candidate()
    second = build_candidate()
    for key in (
        service.CANDIDATE_DIGEST_KEY,
        service.PACKAGE_OPTIONS_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_DIGEST_KEY,
        service.FUTURE_CONTRACT_DIGEST_KEY,
        service.SOURCE_BINDING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64


def test_injected_valid_source_failure_diagnosis_is_accepted():
    candidate = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(
        source_failure_diagnosis=deepcopy(service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS)
    )
    assert candidate["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST


def test_injected_source_failure_diagnosis_drift_is_rejected():
    diagnosis = deepcopy(service.EXPECTED_SOURCE_FAILURE_DIAGNOSIS)
    diagnosis[service.source.DIAGNOSIS_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(source_failure_diagnosis=diagnosis)


@pytest.mark.parametrize(
    ("key", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("source_execution_commit", "0" * 40),
        ("source_execution_status", "WRONG"),
        ("source_execution_scope", "WRONG"),
        ("source_blocked_reason", "WRONG"),
        ("source_blocked_digest", "0" * 64),
        ("source_source_binding_digest", "0" * 64),
        ("source_input_absence_digest", "0" * 64),
        ("source_coverage_digest", "0" * 64),
        ("source_blocked_manifest_digest", "0" * 64),
        ("source_success_execution_digest", "1" * 64),
        ("primary_failure_class", "WRONG"),
        ("source_approval_digest", "0" * 64),
        ("source_operator_review_digest", "0" * 64),
        ("source_candidate_digest", "0" * 64),
        ("source_completion_execution_blocked_digest", "0" * 64),
        ("source_template_preparation_execution_digest", "0" * 64),
        ("source_follow_on_execution_digest", "0" * 64),
        ("source_targeted_remediation_plan_digest", "0" * 64),
        ("diagnostic_receipt_parsed_in_candidate", True),
        ("retry_pytest_failed_count", 0),
        ("priority_1_total_nodeids", 0),
        ("source_stdout_byte_count", 0),
        ("actual_covered_missing_authority_item_count", 1),
        ("missing_authority_items_status", "ACQUIRED"),
        ("operator_completion_inputs_reentry_or_payload_supply_package_selected", True),
        ("operator_payload_created", True),
        ("operator_completion_inputs_supplied", True),
        ("operator_completion_inputs_validated_as_evidence", True),
        ("operator_source_authority_evidence_package_created", True),
        ("source_authority_evidence_acquired", True),
        ("remediation_execution_performed", True),
        ("pytest_performed_in_candidate", True),
        ("cache_read_in_candidate", True),
        ("env_inspection_performed", True),
        ("provider_requests_made_in_candidate", True),
        ("root_cause_claimed", True),
        ("retry_success_claimed", True),
        ("ready_for_main_merge_approval", True),
        ("runtime_use", "AUTHORIZED"),
        (service.CANDIDATE_DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_top_level_drift(key, replacement):
    candidate = build_candidate()
    candidate[key] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(candidate)


@pytest.mark.parametrize("collection_key", ["package_options", "future_requirements", "future_plan", "planned_outputs", "non_goals", "outputs", "next_chain", "next_gates", "risk_controls"])
def test_validator_rejects_missing_governance_collection_items(collection_key):
    candidate = build_candidate()
    candidate[collection_key] = candidate[collection_key][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(candidate)


def test_validator_accepts_valid_candidate():
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(build_candidate())
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_markdown_contains_all_required_sections():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_markdown_v1(build_candidate())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.RECOMMENDED_PACKAGE in markdown
    assert service.SOURCE_BLOCKED_REASON in markdown


def test_writer_writes_only_candidate_status_markdown(tmp_path: Path):
    candidate = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_STATUS.md"
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(tmp_path: Path, protected: str):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_after_no_input_execution_failure_diagnosis_v1(tmp_path / protected)
