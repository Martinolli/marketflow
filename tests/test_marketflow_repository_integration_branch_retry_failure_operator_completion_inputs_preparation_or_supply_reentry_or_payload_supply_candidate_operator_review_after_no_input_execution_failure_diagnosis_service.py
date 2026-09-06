from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_service
    as service,
)


def build_review():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1()


def test_operator_review_builds_offline_from_committed_candidate_constants():
    review = build_review()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


def test_artifact_identity_status_and_scope():
    review = build_review()
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert review["operator_review_scope"] == service.OPERATOR_REVIEW_SCOPE


def test_source_candidate_and_digest_surface_are_bound():
    review = build_review()
    assert review["source_candidate_commit"] == service.SOURCE_CANDIDATE_COMMIT
    assert review["source_candidate_artifact_kind"] == service.source.ARTIFACT_KIND
    assert review["source_candidate_status"] == service.source.CANDIDATE_STATUS
    assert review["source_candidate_scope"] == service.source.CANDIDATE_SCOPE
    assert review["source_candidate_digest"] == service.SOURCE_CANDIDATE_DIGEST
    assert review["source_package_options_digest"] == service.SOURCE_PACKAGE_OPTIONS_DIGEST
    assert review["source_future_requirements_digest"] == service.SOURCE_FUTURE_REQUIREMENTS_DIGEST
    assert review["source_future_contract_digest"] == service.SOURCE_FUTURE_CONTRACT_DIGEST
    assert review["source_candidate_source_binding_digest"] == service.SOURCE_CANDIDATE_SOURCE_BINDING_DIGEST
    assert review["source_candidate_manifest_digest"] == service.SOURCE_CANDIDATE_MANIFEST_DIGEST


def test_source_failure_diagnosis_and_execution_are_bound():
    review = build_review()
    assert review["source_failure_diagnosis_commit"] == service.source.SOURCE_FAILURE_DIAGNOSIS_COMMIT
    assert review["source_failure_diagnosis_digest"] == service.source.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert review["source_failure_classification_digest"] == service.source.SOURCE_FAILURE_CLASSIFICATION_DIGEST
    assert review["source_input_absence_diagnosis_digest"] == service.source.SOURCE_INPUT_ABSENCE_DIAGNOSIS_DIGEST
    assert review["source_binding_review_digest"] == service.source.SOURCE_BINDING_REVIEW_DIGEST
    assert review["source_coverage_diagnosis_digest"] == service.source.SOURCE_COVERAGE_DIAGNOSIS_DIGEST
    assert review["source_failure_diagnosis_manifest_digest"] == service.source.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST
    assert review["source_execution_commit"] == service.source.SOURCE_EXECUTION_COMMIT
    assert review["source_blocked_reason"] == service.source.SOURCE_BLOCKED_REASON


def test_blocked_digests_and_absent_success_digests_are_preserved():
    review = build_review()
    assert review["source_blocked_digest"] == service.source.SOURCE_BLOCKED_DIGEST
    assert review["source_source_binding_digest"] == service.source.SOURCE_SOURCE_BINDING_DIGEST
    assert review["source_input_absence_digest"] == service.source.SOURCE_INPUT_ABSENCE_DIGEST
    assert review["source_coverage_digest"] == service.source.SOURCE_COVERAGE_DIGEST
    assert review["source_blocked_manifest_digest"] == service.source.SOURCE_BLOCKED_MANIFEST_DIGEST
    assert review["source_success_digests_absent"] is True
    assert review["source_success_execution_digest"] is None
    assert review["source_prepared_operator_completion_inputs_digest"] is None
    assert review["source_prepared_operator_completion_inputs_manifest_digest"] is None


def test_failure_classes_are_preserved():
    review = build_review()
    assert review["primary_failure_class"] == service.source.PRIMARY_FAILURE_CLASS
    assert tuple(review["secondary_failure_classes"]) == service.source.SECONDARY_FAILURE_CLASSES


def test_approval_and_source_review_are_bound():
    review = build_review()
    assert review["source_approval_commit"] == "6623e6a6acb0a8da85fee15a29a52606a7fc6af1"
    assert review["source_approval_digest"] == "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72"
    assert review["source_attestation_digest"] == "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af"
    assert review["selected_operator_completion_inputs_preparation_or_supply_package"] == "PACKAGE_PREPARE_OR_SUPPLY_NON_SECRET_OPERATOR_COMPLETION_INPUTS_FOR_REVIEWED_TEMPLATE"
    assert review["source_operator_review_commit"] == "2efc22338250f9de88e76fbf6381796c82f817df"
    assert review["source_operator_review_digest"] == "82e0286d511ced1721346d3049ed434f37d953eba679e71585524529e7864b4a"
    assert review["source_input_contract_review_digest"] == "78c3a6ff08102a49434486c3683ff5d3be63c798932b4d6ae3d47ab66e17da94"
    assert review["source_binding_review_digest_prior_operator_review"] == "4f4ed7e71d0b70fdeedbb3c39361cb8bcabb4eceab156dcf12ce406581c34d99"


def test_prior_candidate_and_completion_failure_diagnosis_are_bound():
    review = build_review()
    assert review["source_prior_candidate_commit"] == "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1"
    assert review["source_prior_candidate_digest"] == "41a2df4be129a88b829439dadc3e0969715853944068f73800fd673720f02ca8"
    assert review["source_prior_candidate_manifest_digest"] == "c1bfffd4995beef0e4f65e74b8a1068b517caa67aece00c6b0104c5cf643f937"
    assert review["source_prior_completion_failure_diagnosis_commit"] == "07276fc4b171179eb7210ce679ba2a9bdbd17e8c"
    assert review["source_prior_completion_failure_diagnosis_digest"] == "3789d82ea1ef74aed2a6d7d7b1404254c0b5672eaf3c8080095ec21907e50759"
    assert review["source_prior_completion_failure_manifest_digest"] == "f354ae2af92e1d9fb1c29a409868747e075953969dec69f5aad69b4f8f7f37cc"


def test_completion_approval_candidate_and_template_chains_are_bound():
    review = build_review()
    assert review["source_completion_execution_commit"] == "945776b2164969e067d8dcc4809128282d3b1287"
    assert review["source_completion_execution_blocked_digest"] == "5fe3269b5787730da7d0287029af15956e9efae13f436c58c94e93ff7160b2c1"
    assert review["source_completion_execution_blocked_manifest_digest"] == "97b42143837d78ea6dba2d13a53cad5f42ffdcf8ea3f82d55c6ab521a9564cc6"
    assert review["source_completion_approval_commit"] == "40bee1289543bb07e64e383eb2e1c61d83615bd5"
    assert review["source_completion_candidate_operator_review_commit"] == "d71bfb14a656592ab637d94d9dd30d73912104b0"
    assert review["source_completion_candidate_commit"] == "7af6b1b5ad223f92da0997e2b7abcb73543470df"
    assert review["source_template_preparation_results_review_commit"] == "268c84d7ef4ed550bb38f07670247540590885f6"
    assert review["source_template_preparation_execution_commit"] == "a39332feb29a23612ee51cb45e8d5663b144c638"


def test_acquisition_enrichment_historical_and_recovery_chains_are_bound():
    review = build_review()
    for key in (
        "source_preparation_candidate_digest", "source_acquisition_approval_digest",
        "source_follow_on_results_review_digest", "source_follow_on_execution_digest",
        "source_enrichment_execution_digest", "source_authority_enrichment_plan_digest",
        "historical_source_approval_digest", "historical_failure_diagnosis_digest",
        "historical_blocked_remediation_manifest_digest", "source_targeted_remediation_plan_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest", "source_recovery_results_review_digest",
        "source_module_grouping_digest", "source_staged_inventory_digest",
    ):
        assert len(review[key]) == 64


def test_receipt_retry_priority_and_diagnostic_context_are_preserved():
    review = build_review()
    assert review["source_durable_receipt_path"].endswith("RECEIPT_V1.json")
    assert review["durable_receipt_not_parsed"] is True
    assert review["diagnostic_receipt_parsed_in_operator_review"] is False
    assert (review["retry_pytest_passed_count"], review["retry_pytest_failed_count"], review["retry_pytest_error_count"], review["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert len(review["priority_1_target_modules"]) == 5
    assert review["priority_1_total_nodeids"] == 612
    assert review["top_10_count_sum"] == 1069
    assert review["failed_or_errored_nodeids_count"] == 1404
    assert review["module_summary_module_count"] == 29
    assert review["priority1_pre_change_validation_passed_count"] == 675
    assert review["priority1_post_change_validation_passed_count"] == 675
    assert review["priority1_validation_is_retry_evidence"] is False
    assert review["source_exit_code"] == 1
    assert review["source_stdout_byte_count"] == 1231380
    assert review["source_stderr_byte_count"] == 0
    assert review["source_diagnostic_metadata_only"] is True


def test_reviewed_families_workstreams_template_and_mapping_are_preserved():
    review = build_review()
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert all(item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert review["reviewed_template_row_count"] == 30
    assert len(review["missing_authority_mapping"]) == 30
    assert review["actual_covered_missing_authority_item_count"] == 0
    assert review["actual_uncovered_missing_authority_item_count"] == 30
    assert review["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert review["count_label_distinction_preserved"] is True


def test_twelve_packages_are_reviewed_without_selection():
    options = build_review()["reviewed_package_options"]
    assert len(options) == 12
    assert options[0]["package_id"] == service.RECOMMENDED_PACKAGE
    assert options[0]["review_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert sum(item["review_status"] == "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED" for item in options) == 6
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in options) == 5
    assert all(not item[key] for item in options for key in ("selected", "approved", "authorized", "executed"))


def test_future_requirements_contract_plan_outputs_and_non_goals_are_reviewed_only():
    review = build_review()
    assert len(review["reviewed_future_requirements"]) == 62
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_requirements"])
    assert review["reviewed_future_payload_supply_contract"]["review_status"] == "REVIEWED_PLANNING_ONLY_NOT_SUPPLIED"
    assert review["reviewed_future_payload_supply_contract"]["future_evidence_item_count"] == 30
    assert review["reviewed_future_payload_supply_contract"]["operator_input_supplied"] is False
    assert len(review["reviewed_future_plan"]) == 15
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_plan"])
    assert len(review["reviewed_planned_outputs"]) == 34
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert all(item["active"] for item in review["reviewed_non_goals"])


def test_all_boundaries_outputs_and_authority_states_are_correct():
    review = build_review()
    assert all(review[key] is True for key in service.TRUE_FIELDS)
    assert all(review[key] is False for key in service.FALSE_FIELDS)
    assert set(service.RISK_CONTROLS).issubset(review["risk_controls"])
    assert [item["output_id"] for item in review["outputs"]] == list(service.OUTPUT_IDS)
    assert all(item["status"] == service.GENERATED_REVIEW_ONLY for item in review["outputs"])
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"
    assert review["ready_for_operator_completion_inputs_reentry_or_payload_supply_approval_if_selected"] is True
    assert review["ready_for_operator_completion_inputs_reentry_or_payload_supply_execution"] is False
    assert review["ready_for_retry_candidate"] is False
    assert review["ready_for_main_merge_approval"] is False


def test_checklist_passes_and_summary_is_complete():
    review = build_review()
    assert review["summary"]["total_checks"] == len(review["checklist"])
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"]
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_all_six_digests_are_deterministic_sha256():
    first, second = build_review(), build_review()
    for key in (
        service.OPERATOR_REVIEW_DIGEST_KEY, service.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY, service.FUTURE_CONTRACT_REVIEW_DIGEST_KEY,
        service.SOURCE_BINDING_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64


def test_valid_injected_source_candidate_is_accepted():
    review = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(source_candidate=deepcopy(service.EXPECTED_SOURCE_CANDIDATE))
    assert review["source_candidate_digest"] == service.SOURCE_CANDIDATE_DIGEST


def test_injected_source_candidate_drift_is_rejected():
    candidate = deepcopy(service.EXPECTED_SOURCE_CANDIDATE)
    candidate[service.source.CANDIDATE_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(source_candidate=candidate)


@pytest.mark.parametrize(
    ("key", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("operator_review_status", "WRONG"), ("operator_review_scope", "WRONG"),
        ("source_candidate_commit", "0" * 40), ("source_candidate_digest", "0" * 64),
        ("source_package_options_digest", "0" * 64), ("source_future_requirements_digest", "0" * 64),
        ("source_future_contract_digest", "0" * 64), ("source_candidate_source_binding_digest", "0" * 64),
        ("source_candidate_manifest_digest", "0" * 64), ("source_failure_diagnosis_digest", "0" * 64),
        ("source_execution_commit", "0" * 40), ("source_execution_status", "WRONG"),
        ("source_execution_scope", "WRONG"), ("source_blocked_reason", "WRONG"),
        ("source_blocked_digest", "0" * 64), ("source_source_binding_digest", "0" * 64),
        ("source_input_absence_digest", "0" * 64), ("source_coverage_digest", "0" * 64),
        ("source_blocked_manifest_digest", "0" * 64), ("source_success_execution_digest", "1" * 64),
        ("primary_failure_class", "WRONG"), ("source_approval_digest", "0" * 64),
        ("source_operator_review_digest", "0" * 64), ("source_prior_candidate_digest", "0" * 64),
        ("source_completion_execution_blocked_digest", "0" * 64),
        ("source_template_preparation_execution_digest", "0" * 64),
        ("source_follow_on_execution_digest", "0" * 64), ("source_targeted_remediation_plan_digest", "0" * 64),
        ("diagnostic_receipt_parsed_in_operator_review", True), ("retry_pytest_failed_count", 0),
        ("priority_1_total_nodeids", 0), ("source_stdout_byte_count", 0),
        ("actual_covered_missing_authority_item_count", 1), ("missing_authority_items_status", "ACQUIRED"),
        ("operator_completion_inputs_reentry_or_payload_supply_package_selected", True),
        ("operator_payload_supply_mechanism_created", True), ("operator_payload_created", True),
        ("operator_completion_inputs_supplied", True), ("operator_completion_inputs_validated_as_evidence", True),
        ("operator_source_authority_evidence_package_created", True), ("source_authority_evidence_acquired", True),
        ("remediation_execution_performed", True), ("pytest_performed_in_operator_review", True),
        ("cache_read_in_operator_review", True), ("env_inspection_performed", True),
        ("provider_requests_made_in_operator_review", True), ("root_cause_claimed", True),
        ("retry_success_claimed", True), ("ready_for_main_merge_approval", True),
        ("runtime_use", "AUTHORIZED"), (service.OPERATOR_REVIEW_DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_top_level_drift(key, replacement):
    review = build_review()
    review[key] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(review)


@pytest.mark.parametrize("key", ["reviewed_package_options", "reviewed_future_requirements", "reviewed_future_payload_supply_contract", "reviewed_future_plan", "reviewed_planned_outputs", "reviewed_non_goals", "outputs", "next_chain", "next_gates", "risk_controls"])
def test_validator_rejects_missing_review_surface(key):
    review = build_review()
    if isinstance(review[key], list):
        review[key] = review[key][:-1]
    else:
        review[key].pop(next(iter(review[key])))
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(review)


def test_validator_accepts_valid_review():
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(build_review())
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_markdown_contains_every_required_section():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_markdown_v1(build_review())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.RECOMMENDED_PACKAGE in markdown
    assert service.source.SOURCE_BLOCKED_REASON in markdown


def test_writer_writes_only_operator_review_status(tmp_path: Path):
    review = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_NO_INPUT_EXECUTION_FAILURE_DIAGNOSIS_STATUS.md"
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_directories(tmp_path: Path, protected: str):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryCandidateOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_candidate_operator_review_after_no_input_execution_failure_diagnosis_v1(tmp_path / protected)
