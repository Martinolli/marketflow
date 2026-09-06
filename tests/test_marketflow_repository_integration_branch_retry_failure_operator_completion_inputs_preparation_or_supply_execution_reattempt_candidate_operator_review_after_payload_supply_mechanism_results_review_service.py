from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_service
    as service,
)


@pytest.fixture
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1()


def test_operator_review_builds_offline_from_committed_source_candidate_constants(review):
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["operator_review_status"] == service.OPERATOR_REVIEW_STATUS
    assert review["operator_review_scope"] == service.OPERATOR_REVIEW_SCOPE


def test_source_candidate_identity_checklist_and_digests_are_bound(review):
    assert {key: review[key] for key in service.SOURCE_CANDIDATE_BINDINGS} == service.SOURCE_CANDIDATE_BINDINGS
    assert review["source_candidate_checklist"] == {"passed": 265, "total": 265, "blockers": 0}


def test_source_results_review_and_execution_are_bound(review):
    expected = {
        "source_results_review_commit": "ea82014534ad79480207aa368d008483127a935a",
        "source_results_review_digest": "998f551af3ff8831ace04050e518a3ec227d7e3b6e3c7c5dc1006f55654f3ddf",
        "source_payload_supply_mechanism_review_digest": "9cba19df4cfc9cef262ebdf5327048044faeee10fca8ccd09bd8b2fc265745fc",
        "source_operator_payload_submission_schema_review_digest": "80712a5d90c5a2db1d3edd1b19ae8ce45f4bcc886214e4d1e93c183938f44c21",
        "source_allowed_values_and_secret_screening_review_digest": "19c8f5e89aecd3c720b891903567533bf44ec1a81979d4c38c63603a5d5bb5f5",
        "source_workstream_supply_plan_review_digest": "9ab3e967198557a13a02bd07fb862bda5b544c9ed901dd8bdcda93f246ea31de",
        "source_binding_review_digest": "03e03b69f6c29b715957f771bd37a8214e627a2e40694552d58b8dc6c92536fb",
        "source_results_review_manifest_digest": "4875d967dd31006dd1965abedbf7da757cbc077b5608745b755ee1dbc39c76fd",
        "source_execution_commit": "615c06c21360100c44a5f82c53a8d1606fd27e67",
        "source_execution_digest": "e91075b6e70592c63b83b7614f1445d7ec2af7129a0675a0fc51031b5759ccb7",
        "source_payload_supply_mechanism_digest": "51c6d7f9c64f6e90a986a1fd93be987ec98fba6d241337caab46b8d72840b123",
        "source_operator_payload_submission_schema_digest": "6c17ab33380e6a758e53012111bbe33d653acdda597b950d02b49d8b17e28574",
        "source_allowed_values_and_secret_screening_digest": "cf1d5b5174fcc62336dd74a10728e6a61788d395d3a751524a4bbd40d92cf5e5",
        "source_workstream_supply_plan_digest": "6ebd76ad3559dd758b4aa34faaccd1a5b02c742283f5155e6a77740054fe4149",
        "source_execution_source_binding_digest": "aad8a414581b2a42c87617a75fba94853f46c66ae85a705252bbe780dd328b5f",
        "source_execution_manifest_digest": "765c97e5993bfe090ada473cf1457abbdbd9501b35185bf08a774f8c9ec40539",
    }
    assert {key: review[key] for key in expected} == expected
    assert review["source_results_review_checklist"] == {"passed": 630, "total": 630, "blockers": 0}
    assert review["source_execution_checklist"] == {"passed": 515, "total": 515, "blockers": 0}
    assert review["source_selected_package"] == "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY"
    assert review["source_selected_package_executed"] is True
    assert review["source_payload_supply_mechanism_created"] is True
    assert review["source_execution_not_rerun"] is True
    assert review["source_payload_supply_mechanism_not_regenerated"] is True


def test_mechanism_schema_allowed_values_and_workstream_facts_are_preserved(review):
    assert review["source_mechanism_review_section_count"] == 13
    assert len(review["source_mechanism_review_section_names"]) == 13
    assert review["payload_supply_mechanism_section_count"] == 4
    assert len(review["package_header_schema_fields"]) == 14
    assert len(review["evidence_item_schema_fields"]) == 21
    assert review["future_operator_completion_input_item_ids"] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert review["workstream_segment_item_counts"] == [8, 8, 7, 7]
    assert len(review["allowed_artifact_types"]) == 13
    assert len(review["allowed_evidence_classifications"]) == 12
    assert len(review["secret_screening_indicators"]) == 13


def test_source_approval_review_diagnosis_and_blocked_execution_are_bound(review):
    assert review["source_approval_commit"] == "9c97a344e2a0e6f193804570c4a2ee8a3820e7f3"
    assert review["source_operator_review_commit"] == "fc6d9d00ed95c19f0bf679cbf39b2f5acadcdb35"
    assert review["source_earlier_candidate_commit"] == "052b9f9002ba774361ebc099eea52be6cdbc7e62"
    assert review["source_failure_diagnosis_commit"] == "0bcec575d04c103bea4da1c09738f69aa5fe2cc7"
    assert review["source_blocked_input_preparation_execution_commit"] == "3cb60e016592480f2f23d977952ee5fd4ca3fd21"
    assert review["source_blocked_input_preparation_execution_reason"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert review["prepared_operator_completion_inputs_digest"] is None
    assert review["prepared_operator_completion_inputs_manifest_digest"] is None
    assert review["success_execution_digest"] is None
    assert review["primary_failure_class"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert len(review["secondary_failure_classes"]) == 9


def test_historical_completion_acquisition_enrichment_and_recovery_chain_is_bound(review):
    expected_commits = {
        "source_prior_approval_commit": "6623e6a6acb0a8da85fee15a29a52606a7fc6af1",
        "source_completion_execution_commit": "945776b2164969e067d8dcc4809128282d3b1287",
        "source_completion_approval_commit": "40bee1289543bb07e64e383eb2e1c61d83615bd5",
        "source_completion_candidate_operator_review_commit": "d71bfb14a656592ab637d94d9dd30d73912104b0",
        "source_completion_candidate_commit": "7af6b1b5ad223f92da0997e2b7abcb73543470df",
        "source_template_preparation_results_review_commit": "268c84d7ef4ed550bb38f07670247540590885f6",
        "source_template_preparation_execution_commit": "a39332feb29a23612ee51cb45e8d5663b144c638",
    }
    assert {key: review[key] for key in expected_commits} == expected_commits
    digest_keys = (
        "source_prior_approval_digest", "source_completion_execution_blocked_digest",
        "source_completion_approval_digest", "source_completion_candidate_operator_review_digest",
        "source_completion_candidate_digest", "source_template_preparation_results_review_digest",
        "source_template_preparation_execution_digest", "source_package_template_digest",
        "source_evidence_item_template_digest", "source_follow_on_results_review_digest",
        "source_follow_on_execution_digest", "source_authority_acquisition_candidate_digest",
        "source_authority_acquisition_scope_digest", "source_missing_authority_to_source_evidence_mapping_digest",
        "source_enrichment_execution_digest", "source_authority_enrichment_plan_digest",
        "source_missing_authority_inventory_digest", "source_workstream_authority_mapping_digest",
        "historical_blocked_remediation_manifest_digest", "source_targeted_remediation_plan_digest",
        "source_failure_family_classification_digest", "source_receipt_recovery_or_recapture_results_review_digest",
        "source_planning_results_review_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_results_review_digest",
        "source_after_v2_approval_digest", "source_module_grouping_digest", "source_staged_inventory_digest",
    )
    assert all(len(review[key]) == 64 for key in digest_keys)


def test_receipt_retry_priority_diagnostic_families_workstreams_and_template_are_bound(review):
    assert review["source_durable_receipt_path"].endswith("EXECUTION_RECEIPT_V1.json")
    assert review["durable_receipt_not_parsed"] is True
    assert (review["retry_pytest_passed_count"], review["retry_pytest_failed_count"], review["retry_pytest_error_count"], review["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert len(review["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    assert review["priority1_pre_change_validation_passed_count"] == 675
    assert review["priority1_post_change_validation_passed_count"] == 675
    assert review["priority1_validation_is_retry_evidence"] is False
    assert review["source_exit_code"] == 1
    assert review["source_stdout_byte_count"] == 1231380
    assert review["source_stderr_byte_count"] == 0
    assert review["source_diagnostic_metadata_only"] is True
    assert len(review["observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in review["observable_failure_families"]) == 188
    assert all(item["confidence"] == "HIGH" for item in review["observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert review["reviewed_template_row_count"] == 30
    assert len(review["missing_authority_mapping"]) == 30


def test_package_options_are_reviewed_without_selection_approval_authorization_or_execution(review):
    options = review["package_options_review"]
    assert len(options) == 12
    assert options[0]["package_id"] == service.RECOMMENDED_PACKAGE
    assert options[0]["operator_review_status"] == service.RECOMMENDED_REVIEW_STATUS
    assert sum(item["operator_review_status"] == service.AVAILABLE_REVIEW_STATUS for item in options) == 6
    assert sum(item["operator_review_status"] == service.BLOCKED_REVIEW_STATUS for item in options) == 5
    assert all(item["blocked_reason"] for item in options if item["operator_review_status"] == service.BLOCKED_REVIEW_STATUS)
    assert all(not item[key] for item in options for key in ("selected", "approved", "authorized", "executed"))


def test_future_requirements_plan_and_outputs_are_reviewed_not_executed_or_generated(review):
    assert len(review["future_requirements_review"]) == 58
    assert {item["requirement_id"] for item in review["future_requirements_review"]} == set(service.source.FUTURE_REQUIREMENT_IDS)
    assert all(item["review_status"] == service.FUTURE_REQUIREMENT_REVIEW_STATUS for item in review["future_requirements_review"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["future_requirements_review"])
    assert len(review["future_plan_review"]) == 14
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" and item["execution_status"] == "NOT_EXECUTED" for item in review["future_plan_review"])
    assert len(review["planned_outputs_review"]) == 32
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" for item in review["planned_outputs_review"])


def test_payload_evidence_authority_and_coverage_absence_is_preserved(review):
    assert review["actual_covered_missing_authority_item_count"] == 0
    assert review["actual_uncovered_missing_authority_item_count"] == 30
    assert review["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert [item["missing_authority_id"] for item in review["missing_authority_items"]] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert all(item["status"] == "MISSING_NOT_ACQUIRED" for item in review["missing_authority_items"])
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"


def test_outputs_recommendation_chain_gates_risks_and_checklist(review):
    assert [item["output_kind"] for item in review["outputs"]] == list(service.OUTPUT_NAMES)
    assert all(item["status"] == service.GENERATED_OUTPUT_STATUS for item in review["outputs"])
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert len(review["next_chain"]) == 13
    assert len(review["next_gates"]) == 17
    assert set(service._OPERATOR_REVIEW_RISK_CONTROLS).issubset(review["risk_controls"])
    assert set(service.source.RISK_CONTROLS).issubset(review["risk_controls"])
    check_ids = [item["check_id"] for item in review["checklist"]]
    assert set(service.REQUIRED_CHECK_IDS).issubset(check_ids)
    assert len(check_ids) == len(set(check_ids))
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"]
    assert review["summary"]["blocker_count"] == 0


@pytest.mark.parametrize(
    "digest_key",
    [
        service.OPERATOR_REVIEW_DIGEST_KEY,
        service.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY,
        service.FUTURE_CONTRACT_REVIEW_DIGEST_KEY,
        service.SOURCE_BINDING_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_digests_are_deterministic(review, digest_key):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1()
    assert review[digest_key] == rebuilt[digest_key]
    assert len(review[digest_key]) == 64


def test_builder_accepts_exact_injected_source_candidate_bindings(review):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(
        source_candidate=deepcopy(service.SOURCE_CANDIDATE_BINDINGS)
    )
    assert rebuilt == review


def test_validator_accepts_valid_operator_review(review):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(review) == review


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "operator_review_status", "operator_review_scope", "source_candidate_commit",
        "source_candidate_digest", "source_candidate_package_options_digest", "source_candidate_future_requirements_digest",
        "source_candidate_future_contract_digest", "source_candidate_source_binding_digest", "source_candidate_manifest_digest",
        "source_results_review_commit", "source_results_review_digest", "source_execution_commit", "source_execution_digest",
        "source_payload_supply_mechanism_digest", "source_payload_supply_mechanism_review_digest",
        "source_operator_payload_submission_schema_digest", "source_operator_payload_submission_schema_review_digest",
        "source_allowed_values_and_secret_screening_digest", "source_allowed_values_and_secret_screening_review_digest",
        "source_workstream_supply_plan_digest", "source_workstream_supply_plan_review_digest",
        "source_execution_source_binding_digest", "source_execution_manifest_digest", "source_binding_review_digest",
        "source_results_review_manifest_digest", "source_selected_package", "recommended_package",
        service.OPERATOR_REVIEW_DIGEST_KEY, service.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_REVIEW_DIGEST_KEY, service.FUTURE_CONTRACT_REVIEW_DIGEST_KEY,
        service.SOURCE_BINDING_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_identity_binding_or_digest(review, field):
    changed = deepcopy(review)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_field_changed(review, field):
    changed = deepcopy(review)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_prohibited_action(review, field):
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", list(service.COUNTS))
def test_validator_rejects_changed_count(review, field):
    changed = deepcopy(review)
    changed[field] += 1
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize(
    "surface",
    ["package_options_review", "future_requirements_review", "future_plan_review", "planned_outputs_review", "outputs", "next_chain", "next_gates", "risk_controls", "missing_authority_items"],
)
def test_validator_rejects_missing_required_surface(review, surface):
    changed = deepcopy(review)
    changed[surface] = changed[surface][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize(
    ("surface", "field", "value"),
    [
        ("package_options_review", "selected", True),
        ("package_options_review", "approved", True),
        ("package_options_review", "authorized", True),
        ("package_options_review", "executed", True),
        ("package_options_review", "operator_review_status", "CHANGED"),
        ("future_requirements_review", "execution_status", "EXECUTED"),
        ("future_plan_review", "execution_status", "EXECUTED"),
        ("planned_outputs_review", "review_status", "GENERATED"),
        ("missing_authority_items", "status", "ACQUIRED"),
    ],
)
def test_validator_rejects_nested_authority_change(review, surface, field, value):
    changed = deepcopy(review)
    changed[surface][0][field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(changed)


def test_injected_source_candidate_must_match_committed_bindings():
    changed = deepcopy(service.SOURCE_CANDIDATE_BINDINGS)
    changed["source_candidate_digest"] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(source_candidate=changed)


def test_writer_round_trips_operator_review_and_markdown(tmp_path, review):
    written = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_v1(tmp_path)
    destination = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_CANDIDATE_OPERATOR_REVIEW_AFTER_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW_STATUS.md"
    assert written == review
    assert destination.read_text(encoding="utf-8") == service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_markdown_v1(review)


def test_markdown_contains_all_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_operator_review_after_payload_supply_mechanism_results_review_markdown_v1(review)
    required = (
        "Operator Review Disposition", "Source Candidate", "Candidate Digest Surface", "Source Results Review",
        "Results Review Digest Surface", "Source Execution", "Execution Digest Surface", "Selected Source Package",
        "Payload Supply Mechanism Review", "Operator Payload Submission Schema Review",
        "Allowed Values and Secret Screening Review", "Workstream Supply Plan Review", "Future Explicit Payload Requirement",
        "Package Options Review", "Recommended Package Review", "Source Approval", "Source Operator Review",
        "Source Failure Diagnosis", "Source Blocked Input Preparation Execution", "Blocked Reason", "Primary Failure Class",
        "Secondary Failure Classes", "Historical Completion Template Acquisition Chains", "Follow-On and Enrichment Chain",
        "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain", "Durable Receipt", "Retry Failure Context",
        "Priority 1 Target Modules", "Priority 1 Validation Summary", "Diagnostic Capture Evidence Summary",
        "Reviewed Observable Families", "Reviewed Workstreams", "Reviewed Template Structure", "Actual Payload Absence",
        "Actual Evidence Absence", "Actual Coverage Zero", "Missing Authority Inventory", "Count Label Distinction",
        "Unsupported Claims Boundary", "Recommendation", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    )
    assert all(f"## {heading}" in markdown for heading in required)
    assert service.RECOMMENDED_PACKAGE in markdown
    assert service.RECOMMENDED_NEXT_TASK in markdown
