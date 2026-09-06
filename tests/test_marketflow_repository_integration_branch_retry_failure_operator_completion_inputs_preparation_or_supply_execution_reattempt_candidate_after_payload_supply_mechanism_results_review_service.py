from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_service
    as service,
)


@pytest.fixture
def candidate() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1()


def test_candidate_builds_offline_from_committed_source_results_review_constants(candidate):
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("candidate_status", service.CANDIDATE_STATUS),
        ("candidate_scope", service.CANDIDATE_SCOPE),
        ("source_results_review_commit", service.SOURCE_RESULTS_REVIEW_COMMIT),
        ("source_results_review_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_results_review_status", service.source.RESULTS_REVIEW_STATUS),
        ("source_results_review_scope", service.source.RESULTS_REVIEW_SCOPE),
        ("source_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_payload_supply_mechanism_review_digest", service.SOURCE_PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST),
        ("source_operator_payload_submission_schema_review_digest", service.SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST),
        ("source_allowed_values_and_secret_screening_review_digest", service.SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST),
        ("source_workstream_supply_plan_review_digest", service.SOURCE_WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST),
        ("source_binding_review_digest", service.SOURCE_BINDING_REVIEW_DIGEST),
        ("source_results_review_manifest_digest", service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_execution_commit", service.source.SOURCE_EXECUTION_COMMIT),
        ("source_execution_artifact_kind", service.source.source.ARTIFACT_KIND),
        ("source_execution_status", service.source.source.EXECUTION_STATUS),
        ("source_execution_scope", service.source.source.EXECUTION_SCOPE),
        ("source_execution_digest", service.source.SOURCE_EXECUTION_DIGEST),
        ("source_payload_supply_mechanism_digest", service.source.SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST),
        ("source_operator_payload_submission_schema_digest", service.source.SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST),
        ("source_allowed_values_and_secret_screening_digest", service.source.SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST),
        ("source_workstream_supply_plan_digest", service.source.SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST),
        ("source_execution_source_binding_digest", service.source.SOURCE_EXECUTION_SOURCE_BINDING_DIGEST),
        ("source_execution_manifest_digest", service.source.SOURCE_EXECUTION_MANIFEST_DIGEST),
        ("recommended_package", service.RECOMMENDED_PACKAGE),
        ("recommended_package_status", service.RECOMMENDED_PACKAGE_STATUS),
        ("missing_authority_items_status", "MISSING_NOT_ACQUIRED"),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_identity_source_and_authority_fields(candidate, field, expected):
    assert candidate[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_true_fields(candidate, field):
    assert candidate[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_required_false_fields(candidate, field):
    assert candidate[field] is False


@pytest.mark.parametrize("field,expected", list(service.COUNTS.items()))
def test_required_counts(candidate, field, expected):
    assert candidate[field] == expected


def test_mechanism_review_facts_are_exact(candidate):
    assert candidate["source_execution_not_rerun"] is True
    assert candidate["source_payload_supply_mechanism_not_regenerated"] is True
    assert candidate["source_mechanism_review_section_count"] == 13
    assert len(candidate["source_mechanism_review_section_names"]) == 13
    assert candidate["payload_supply_mechanism_section_count"] == 4
    assert len(candidate["package_header_schema_fields"]) == 14
    assert len(candidate["evidence_item_schema_fields"]) == 21
    assert candidate["future_operator_completion_input_item_ids"] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert candidate["workstream_segment_item_counts"] == [8, 8, 7, 7]
    assert len(candidate["allowed_artifact_types"]) == 13
    assert len(candidate["allowed_evidence_classifications"]) == 12
    assert len(candidate["secret_screening_indicators"]) == 13


def test_package_options_are_exactly_candidate_only(candidate):
    options = candidate["package_options"]
    assert len(options) == 12
    assert options[0]["package_id"] == service.RECOMMENDED_PACKAGE
    assert options[0]["candidate_status"] == service.RECOMMENDED_PACKAGE_STATUS
    assert sum(item["candidate_status"] == service.AVAILABLE_PACKAGE_STATUS for item in options) == 6
    assert sum(item["candidate_status"] == service.BLOCKED_PACKAGE_STATUS for item in options) == 5
    assert all(item["selected"] is False for item in options)
    assert all(item["approved"] is False for item in options)
    assert all(item["authorized"] is False for item in options)
    assert all(item["executed"] is False for item in options)
    assert all(item["blocked_reason"] for item in options if item["candidate_status"] == service.BLOCKED_PACKAGE_STATUS)


def test_future_requirements_plan_and_planned_outputs_are_unexecuted(candidate):
    assert len(candidate["future_requirements"]) == 58
    assert {item["requirement_id"] for item in candidate["future_requirements"]} == set(service.FUTURE_REQUIREMENT_IDS)
    assert all(item["requirement_status"] == service.FUTURE_REQUIREMENT_STATUS for item in candidate["future_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in candidate["future_requirements"])
    assert len(candidate["future_plan"]) == 14
    assert all(item["status"] == "PLANNED_NOT_EXECUTED" for item in candidate["future_plan"])
    assert len(candidate["planned_outputs"]) == 32
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])


def test_historical_retry_priority_and_diagnostic_evidence_remains_bound(candidate):
    assert candidate["source_approval_commit"] == "9c97a344e2a0e6f193804570c4a2ee8a3820e7f3"
    assert candidate["source_operator_review_commit"] == "fc6d9d00ed95c19f0bf679cbf39b2f5acadcdb35"
    assert candidate["source_candidate_commit"] == "052b9f9002ba774361ebc099eea52be6cdbc7e62"
    assert candidate["source_failure_diagnosis_commit"] == "0bcec575d04c103bea4da1c09738f69aa5fe2cc7"
    assert candidate["source_blocked_input_preparation_execution_commit"] == "3cb60e016592480f2f23d977952ee5fd4ca3fd21"
    assert candidate["source_blocked_input_preparation_execution_reason"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert candidate["prepared_operator_completion_inputs_digest"] is None
    assert candidate["prepared_operator_completion_inputs_manifest_digest"] is None
    assert candidate["success_execution_digest"] is None
    assert candidate["retry_pytest_passed_count"] == 24877
    assert candidate["retry_pytest_failed_count"] == 1292
    assert candidate["retry_pytest_error_count"] == 112
    assert candidate["retry_pytest_skipped_count"] == 7
    assert candidate["priority_1_total_nodeids"] == 612
    assert candidate["top_10_count_sum"] == 1069
    assert candidate["failed_or_errored_nodeids_count"] == 1404
    assert candidate["module_summary_module_count"] == 29
    assert candidate["priority1_pre_change_validation_passed_count"] == 675
    assert candidate["priority1_post_change_validation_passed_count"] == 675
    assert candidate["source_exit_code"] == 1
    assert candidate["source_stdout_byte_count"] == 1231380
    assert candidate["source_stderr_byte_count"] == 0
    assert candidate["source_durable_receipt_path"].endswith("EXECUTION_RECEIPT_V1.json")


def test_reviewed_families_workstreams_and_template_are_bound(candidate):
    assert len(candidate["observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in candidate["observable_failure_families"]) == 188
    assert all(item["confidence"] == "HIGH" for item in candidate["observable_failure_families"])
    assert len(candidate["reviewed_workstreams"]) == 4
    assert candidate["reviewed_template_row_count"] == 30
    assert candidate["actual_covered_missing_authority_item_count"] == 0
    assert candidate["actual_uncovered_missing_authority_item_count"] == 30
    assert [item["missing_authority_id"] for item in candidate["missing_authority_items"]] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert all(item["status"] == "MISSING_NOT_ACQUIRED" for item in candidate["missing_authority_items"])


def test_outputs_recommendation_chain_gates_and_controls(candidate):
    assert [item["output_kind"] for item in candidate["outputs"]] == list(service.OUTPUT_NAMES)
    assert all(item["status"] == service.GENERATED_OUTPUT_STATUS for item in candidate["outputs"])
    assert candidate["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert len(candidate["next_chain"]) == 14
    assert len(candidate["next_gates"]) == 18
    assert set(service._CANDIDATE_RISK_CONTROLS).issubset(candidate["risk_controls"])
    assert set(service.source.RISK_CONTROLS).issubset(candidate["risk_controls"])


@pytest.mark.parametrize(
    "digest_key",
    [
        service.CANDIDATE_DIGEST_KEY,
        service.PACKAGE_OPTIONS_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_DIGEST_KEY,
        service.FUTURE_CONTRACT_DIGEST_KEY,
        service.SOURCE_BINDING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_digests_are_deterministic(candidate, digest_key):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1()
    assert candidate[digest_key] == rebuilt[digest_key]
    assert len(candidate[digest_key]) == 64


def test_builder_accepts_exact_injected_source_bindings(candidate):
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(
        source_results_review=deepcopy(service.SOURCE_RESULTS_REVIEW_BINDINGS)
    )
    assert rebuilt == candidate


def test_validator_accepts_valid_candidate(candidate):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(candidate) == candidate


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "candidate_status", "candidate_scope", "source_results_review_commit",
        "source_results_review_digest", "source_execution_commit", "source_execution_digest",
        "source_payload_supply_mechanism_digest", "source_payload_supply_mechanism_review_digest",
        "source_operator_payload_submission_schema_review_digest",
        "source_allowed_values_and_secret_screening_review_digest", "source_workstream_supply_plan_review_digest",
        "source_binding_review_digest", "source_results_review_manifest_digest", "recommended_package",
        service.CANDIDATE_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY, service.FUTURE_REQUIREMENTS_DIGEST_KEY,
        service.FUTURE_CONTRACT_DIGEST_KEY, service.SOURCE_BINDING_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_identity_binding_or_digest(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_field_changed(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_prohibited_action(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("field", list(service.COUNTS))
def test_validator_rejects_changed_count(candidate, field):
    changed = deepcopy(candidate)
    changed[field] += 1
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize("surface", ["package_options", "future_requirements", "future_plan", "planned_outputs", "outputs", "next_chain", "next_gates", "risk_controls", "missing_authority_items"])
def test_validator_rejects_missing_required_surface(candidate, surface):
    changed = deepcopy(candidate)
    changed[surface] = changed[surface][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


@pytest.mark.parametrize(
    ("surface", "field", "value"),
    [
        ("package_options", "selected", True),
        ("package_options", "approved", True),
        ("package_options", "authorized", True),
        ("package_options", "executed", True),
        ("future_requirements", "execution_status", "EXECUTED"),
        ("future_plan", "status", "EXECUTED"),
        ("planned_outputs", "status", "GENERATED"),
        ("missing_authority_items", "status", "ACQUIRED"),
    ],
)
def test_validator_rejects_nested_authority_change(candidate, surface, field, value):
    changed = deepcopy(candidate)
    changed[surface][0][field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(changed)


def test_injected_source_results_review_must_match_committed_bindings():
    changed = deepcopy(service.SOURCE_RESULTS_REVIEW_BINDINGS)
    changed["source_results_review_digest"] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(source_results_review=changed)


def test_writer_round_trips_candidate_and_markdown(tmp_path, candidate):
    written = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_v1(tmp_path)
    destination = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_CANDIDATE_AFTER_PAYLOAD_SUPPLY_MECHANISM_RESULTS_REVIEW_STATUS.md"
    assert written == candidate
    assert destination.is_file()
    assert destination.read_text(encoding="utf-8") == service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_markdown_v1(candidate)


def test_markdown_contains_all_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_candidate_after_payload_supply_mechanism_results_review_markdown_v1(candidate)
    required = (
        "Candidate Disposition", "Source Results Review", "Results Review Digest Surface", "Source Execution",
        "Execution Digest Surface", "Selected Source Package", "Payload Supply Mechanism Review",
        "Operator Payload Submission Schema Review", "Allowed Values and Secret Screening Review",
        "Workstream Supply Plan Review", "Future Explicit Payload Requirement", "Package Options",
        "Recommended Package", "Source Approval", "Source Operator Review", "Source Candidate",
        "Source Failure Diagnosis", "Source Blocked Input Preparation Execution", "Blocked Reason",
        "Primary Failure Class", "Secondary Failure Classes", "Historical Completion Template Acquisition Chains",
        "Follow-On and Enrichment Chain", "Historical Blocked Remediation", "Plan Method Diagnostic Recovery Chain",
        "Durable Receipt", "Retry Failure Context", "Priority 1 Target Modules", "Priority 1 Validation Summary",
        "Diagnostic Capture Evidence Summary", "Reviewed Observable Families", "Reviewed Workstreams",
        "Reviewed Template Structure", "Actual Payload Absence", "Actual Evidence Absence", "Actual Coverage Zero",
        "Missing Authority Inventory", "Count Label Distinction", "Unsupported Claims Boundary", "Recommendation",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    )
    assert all(f"## {heading}" in markdown for heading in required)
    assert service.RECOMMENDED_PACKAGE in markdown
    assert service.RECOMMENDED_NEXT_TASK in markdown
