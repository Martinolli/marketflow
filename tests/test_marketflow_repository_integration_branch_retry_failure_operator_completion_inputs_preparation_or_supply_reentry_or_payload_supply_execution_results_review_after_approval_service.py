from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_service
    as service,
)


@pytest.fixture()
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1()


def test_builds_offline_from_committed_source_execution_constants(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("subprocess forbidden"))
    monkeypatch.setattr(Path, "read_text", lambda *a, **k: pytest.fail("file reads forbidden"))
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1()
    assert artifact["created_offline"] is True
    assert artifact["results_review_only"] is True
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("key,expected", [
    ("artifact_kind", service.ARTIFACT_KIND),
    ("schema_version", service.SCHEMA_VERSION),
    ("results_review_status", service.RESULTS_REVIEW_STATUS),
    ("results_review_scope", service.RESULTS_REVIEW_SCOPE),
    ("source_execution_commit", service.SOURCE_EXECUTION_COMMIT),
    ("source_execution_artifact_kind", service.source.ARTIFACT_KIND),
    ("source_execution_status", service.source.EXECUTION_STATUS),
    ("source_execution_scope", service.source.EXECUTION_SCOPE),
    ("source_execution_digest", service.SOURCE_EXECUTION_DIGEST),
    ("source_payload_supply_mechanism_digest", service.SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST),
    ("source_operator_payload_submission_schema_digest", service.SOURCE_OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST),
    ("source_allowed_values_and_secret_screening_digest", service.SOURCE_ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST),
    ("source_workstream_supply_plan_digest", service.SOURCE_WORKSTREAM_SUPPLY_PLAN_DIGEST),
    ("source_execution_source_binding_digest", service.SOURCE_EXECUTION_SOURCE_BINDING_DIGEST),
    ("source_execution_manifest_digest", service.SOURCE_EXECUTION_MANIFEST_DIGEST),
    ("source_selected_package", service.SELECTED_PACKAGE),
    ("source_selected_package_executed", True),
    ("source_payload_supply_mechanism_created", True),
])
def test_identity_source_execution_and_digest_surface(review, key, expected):
    assert review[key] == expected


@pytest.mark.parametrize("key", service.TRUE_FIELDS)
def test_required_true_review_boundaries(review, key):
    assert review[key] is True


@pytest.mark.parametrize("key", service.FALSE_FIELDS)
def test_required_false_review_boundaries(review, key):
    assert review[key] is False


def test_mechanism_schema_checklist_allowed_values_and_secret_guidance_review(review):
    assert review["payload_supply_mechanism_definition_review"] == {
        "source_digest": service.SOURCE_PAYLOAD_SUPPLY_MECHANISM_DIGEST,
        "definition_present": True, "actual_payload_created": False, "item_count": 30, "section_count": 4,
    }
    schema = review["operator_payload_submission_schema_review"]
    assert len(schema["package_header_fields"]) == 14
    assert len(schema["evidence_item_fields"]) == 21
    assert schema["reviewed_missing_authority_ids"] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert schema["actual_payload_values_present"] is False
    assert review["operator_payload_field_checklist_review"]["field_count"] == 34
    allowed = review["allowed_values_matrix_review"]
    assert len(allowed["section_ids"]) == 4
    assert len(allowed["workstream_ids"]) == 4
    assert len(allowed["artifact_types"]) == 13
    assert len(allowed["evidence_classifications"]) == 12
    secret = review["secret_screening_guidance_review"]
    assert len(secret["required_indicators"]) == 13
    assert secret["actual_payload_screened"] is False


def test_workstream_plan_and_results_review_prerequisite(review):
    plan = review["workstream_segmented_payload_supply_plan_review"]
    assert plan["workstream_ids"] == list(service.source.ALLOWED_WORKSTREAM_IDS)
    assert plan["segment_item_counts"] == [8, 8, 7, 7]
    assert plan["mapped_item_count"] == 30
    assert plan["actual_supplied_item_count"] == 0
    prerequisite = review["results_review_prerequisite"]
    assert prerequisite["results_review_required_before_any_prepared_input_use"] is True
    assert prerequisite["future_reattempt_requires_explicit_non_secret_payload"] is True
    assert prerequisite["execution_reattempt_created"] is False


def test_source_approval_review_candidate_diagnosis_and_blocked_execution_are_bound(review):
    assert review["source_approval_commit"] == "9c97a344e2a0e6f193804570c4a2ee8a3820e7f3"
    assert review["source_operator_review_commit"] == "fc6d9d00ed95c19f0bf679cbf39b2f5acadcdb35"
    assert review["source_candidate_commit"] == "052b9f9002ba774361ebc099eea52be6cdbc7e62"
    assert review["source_failure_diagnosis_commit"] == "0bcec575d04c103bea4da1c09738f69aa5fe2cc7"
    assert review["source_blocked_input_preparation_execution_commit"] == "3cb60e016592480f2f23d977952ee5fd4ca3fd21"
    assert review["source_blocked_input_preparation_execution_reason"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert review["source_success_digests_absent"] is True
    assert review["prepared_operator_completion_inputs_digest"] is None
    assert review["prepared_operator_completion_inputs_manifest_digest"] is None
    assert review["success_execution_digest"] is None


def test_primary_secondary_and_historical_chains_are_preserved(review):
    assert review["primary_failure_class"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert len(review["secondary_failure_classes"]) == 9
    for key in (
        "source_prior_approval_commit", "source_prior_operator_review_commit", "source_prior_candidate_commit",
        "source_prior_completion_failure_diagnosis_commit", "source_completion_execution_commit",
        "source_completion_approval_commit", "source_completion_candidate_operator_review_commit",
        "source_completion_candidate_commit", "source_template_preparation_results_review_commit",
        "source_template_preparation_execution_commit", "source_template_approval_commit",
        "source_preparation_candidate_commit", "source_blocked_acquisition_execution_commit",
        "source_acquisition_approval_commit",
    ):
        assert re.fullmatch(r"[0-9a-f]{40}", review[key])
    assert review["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"


def test_durable_receipt_retry_priority_diagnostic_and_observable_context(review):
    assert review["source_durable_receipt_path"].endswith("EXECUTION_RECEIPT_V1.json")
    assert review["durable_receipt_not_parsed"] is True
    assert (review["retry_pytest_passed_count"], review["retry_pytest_failed_count"], review["retry_pytest_error_count"], review["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert sum(row["failed_or_errored_nodeid_count"] for row in review["priority_1_target_modules"]) == 612
    assert review["priority1_pre_change_validation_passed_count"] == 675
    assert review["priority1_post_change_validation_passed_count"] == 675
    assert review["priority1_validation_is_retry_evidence"] is False
    assert review["source_exit_code"] == 1
    assert review["source_combined_output_byte_count"] == 1231380
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert sum(row["observable_evidence_count"] for row in review["reviewed_observable_failure_families"]) == 188
    assert len(review["reviewed_workstreams"]) == 4


def test_counts_coverage_and_count_label_distinctions(review):
    for key, expected in service.COUNTS.items():
        assert review[key] == expected
    assert review["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert review["future_completion_requirement_count"] == 67
    assert review["source_enumerated_future_completion_requirement_count"] == 69
    assert review["approved_future_completion_requirement_named_count"] == 69
    assert review["source_execution_risk_control_count"] == 246


def test_outputs_recommendation_next_chain_gates_and_risk_controls(review):
    assert [row["output_id"] for row in review["outputs"]] == list(service.OUTPUT_IDS)
    assert all(row["status"] == service.GENERATED_OUTPUT_STATUS for row in review["outputs"])
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["next_chain"] == list(service.NEXT_CHAIN)
    assert review["next_gates"] == list(service.NEXT_GATES)
    assert review["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_passes(review):
    assert all(row["status"] == "PASS" and row["actual"] is True for row in review["checklist"])
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"]
    assert review["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("key", [
    service.RESULTS_REVIEW_DIGEST_KEY, service.PAYLOAD_SUPPLY_MECHANISM_REVIEW_DIGEST_KEY,
    service.OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_REVIEW_DIGEST_KEY,
    service.ALLOWED_VALUES_AND_SECRET_SCREENING_REVIEW_DIGEST_KEY,
    service.WORKSTREAM_SUPPLY_PLAN_REVIEW_DIGEST_KEY, service.SOURCE_BINDING_REVIEW_DIGEST_KEY,
    service.MANIFEST_DIGEST_KEY,
])
def test_review_digests_are_deterministic_sha256(key):
    first = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1()
    second = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1()
    assert re.fullmatch(r"[0-9a-f]{64}", first[key])
    assert first[key] == second[key]


def test_exact_source_execution_injection_is_accepted_and_drift_rejected():
    service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(source_execution=deepcopy(service.SOURCE_EXECUTION_BINDINGS))
    bad = deepcopy(service.SOURCE_EXECUTION_BINDINGS)
    bad["source_execution_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(source_execution=bad)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(review)
    assert result["blocker_count"] == 0


@pytest.mark.parametrize("mutator", [
    lambda x: x.update(artifact_kind="WRONG"),
    lambda x: x.update(results_review_status="WRONG"),
    lambda x: x.update(results_review_scope="WRONG"),
    lambda x: x.update(source_execution_commit="0" * 40),
    lambda x: x.update(source_execution_digest="0" * 64),
    lambda x: x.update(source_payload_supply_mechanism_digest="0" * 64),
    lambda x: x.update(source_operator_payload_submission_schema_digest="0" * 64),
    lambda x: x.update(source_allowed_values_and_secret_screening_digest="0" * 64),
    lambda x: x.update(source_workstream_supply_plan_digest="0" * 64),
    lambda x: x.update(source_execution_source_binding_digest="0" * 64),
    lambda x: x.update(source_execution_manifest_digest="0" * 64),
    lambda x: x.update(source_selected_package="WRONG"),
    lambda x: x.update(source_selected_package_executed=False),
    lambda x: x.update(source_payload_supply_mechanism_created=False),
    lambda x: x.update(payload_supply_mechanism_definition_reviewed=False),
    lambda x: x.pop("operator_payload_submission_schema_review"),
    lambda x: x.pop("operator_payload_field_checklist_review"),
    lambda x: x.pop("allowed_values_matrix_review"),
    lambda x: x.pop("secret_screening_guidance_review"),
    lambda x: x.pop("workstream_segmented_payload_supply_plan_review"),
    lambda x: x["operator_payload_submission_schema_review"].update(actual_payload_values_present=True),
    lambda x: x["operator_payload_submission_schema_review"]["reviewed_missing_authority_ids"].pop(),
    lambda x: x.update(operator_payload_created=True),
    lambda x: x.update(operator_completion_inputs_prepared=True),
    lambda x: x.update(operator_completion_inputs_supplied=True),
    lambda x: x.update(operator_completion_inputs_provided=True),
    lambda x: x.update(operator_completion_inputs_validated_as_evidence=True),
    lambda x: x.update(operator_completion_inputs_bound_as_evidence=True),
    lambda x: x.update(operator_source_authority_evidence_package_created=True),
    lambda x: x.update(operator_source_authority_evidence_package_supplied=True),
    lambda x: x.update(operator_source_authority_evidence_package_validated=True),
    lambda x: x.update(operator_source_authority_evidence_package_bound=True),
    lambda x: x.update(actual_evidence_items_filled=True),
    lambda x: x.update(source_authority_evidence_acquired=True),
    lambda x: x.update(external_evidence_acquired=True),
    lambda x: x.update(remediation_execution_performed=True),
    lambda x: x.update(production_code_modified=True),
    lambda x: x.update(existing_tests_modified=True),
    lambda x: x.update(expected_digests_updated=True),
    lambda x: x.update(patch_generated=True),
    lambda x: x.update(pytest_performed_in_results_review=True),
    lambda x: x.update(retry_rerun_performed=True),
    lambda x: x.update(cache_read_in_results_review=True),
    lambda x: x.update(terminal_logs_parsed=True),
    lambda x: x.update(env_inspection_performed=True),
    lambda x: x.update(diagnostic_receipt_parsed_in_results_review=True),
    lambda x: x.update(source_owners_contacted=True),
    lambda x: x.update(provider_requests_made_in_results_review=True),
    lambda x: x.update(root_cause_claimed=True),
    lambda x: x.update(retry_success_claimed=True),
    lambda x: x.update(main_merge_readiness_claimed=True),
    lambda x: x.update(runtime_authorized=True),
    lambda x: x.update(broker_execution_authorized=True),
    lambda x: x.update(actual_covered_missing_authority_item_count=1),
    lambda x: x.update(missing_authority_items_status="ACQUIRED"),
    lambda x: x.pop("outputs"),
    lambda x: x.pop("recommended_next_task"),
    lambda x: x.pop("next_chain"),
    lambda x: x.pop("risk_controls"),
])
def test_validator_rejects_boundary_tampering(review, mutator):
    mutator(review)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(review)


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_markdown_v1(review)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert "0/30" in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown


def test_writer_writes_only_results_review_status(tmp_path: Path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_RESULTS_REVIEW_AFTER_APPROVAL_STATUS.md"
    assert artifact["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPayloadSupplyExecutionResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_results_review_after_approval_v1(Path(protected))
