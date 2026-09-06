from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_service
    as service,
)


@pytest.fixture()
def execution():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1()


def test_builds_offline_from_committed_source_approval_constants(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("subprocess forbidden"))
    monkeypatch.setattr(Path, "read_text", lambda *a, **k: pytest.fail("file reads forbidden"))
    artifact = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1()
    assert artifact["created_offline"] is True
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("key,expected", [
    ("artifact_kind", service.ARTIFACT_KIND),
    ("schema_version", service.SCHEMA_VERSION),
    ("execution_status", service.EXECUTION_STATUS),
    ("execution_scope", service.EXECUTION_SCOPE),
    ("source_approval_commit", service.SOURCE_APPROVAL_COMMIT),
    ("source_requested_approval_commit", service.SOURCE_REQUESTED_APPROVAL_COMMIT),
    ("source_approval_digest", service.SOURCE_APPROVAL_DIGEST),
    ("source_attestation_digest", service.SOURCE_ATTESTATION_DIGEST),
    ("source_package_options_digest", service.SOURCE_PACKAGE_OPTIONS_DIGEST),
    ("source_future_requirements_digest", service.SOURCE_FUTURE_REQUIREMENTS_DIGEST),
    ("source_future_contract_digest", service.SOURCE_FUTURE_CONTRACT_DIGEST),
    ("source_approval_source_binding_digest", service.SOURCE_APPROVAL_SOURCE_BINDING_DIGEST),
    ("source_approval_manifest_digest", service.SOURCE_APPROVAL_MANIFEST_DIGEST),
    ("selected_package", service.SELECTED_PACKAGE),
    ("payload_supply_mechanism_status", service.MECHANISM_STATUS),
])
def test_core_identity_approval_binding_and_selected_package(execution, key, expected):
    assert execution[key] == expected


@pytest.mark.parametrize("key", service.TRUE_FIELDS)
def test_required_true_execution_boundaries(execution, key):
    assert execution[key] is True


@pytest.mark.parametrize("key", service.FALSE_FIELDS)
def test_required_false_execution_boundaries(execution, key):
    assert execution[key] is False


def test_mechanism_contains_all_thirteen_required_sections(execution):
    assert tuple(execution["payload_supply_mechanism"]) == (
        "mechanism_identity", "approved_source_contract_binding", "explicit_operator_payload_entry_rules",
        "package_header_schema", "thirty_item_payload_schema", "allowed_values_matrix",
        "workstream_segmented_supply_plan", "secret_screening_policy", "pre_submission_operator_checklist",
        "post_submission_results_review_requirement", "downstream_gate_policy", "unsupported_claims_boundary",
        "digest_manifest",
    )


def test_operator_payload_submission_schema_and_checklist_are_generated_without_values(execution):
    schema = execution["operator_payload_submission_schema"]
    assert {row["field_name"] for row in schema["package_header_schema"]} == set(service.PACKAGE_HEADER_FIELDS)
    assert {row["field_name"] for row in schema["evidence_item_schema"]} == set(service.EVIDENCE_ITEM_FIELDS)
    assert schema["actual_payload_values_present"] is False
    assert execution["operator_payload_field_checklist"]
    assert all(row["actual_value_present"] is False for row in execution["operator_payload_field_checklist"])


def test_allowed_values_matrix_and_secret_screening_guidance_are_complete(execution):
    allowed = execution["allowed_values_matrix"]
    assert tuple(allowed["section_id"]) == service.ALLOWED_SECTION_IDS
    assert tuple(allowed["workstream_id"]) == service.ALLOWED_WORKSTREAM_IDS
    assert tuple(allowed["acceptable_source_artifact_type"]) == service.ALLOWED_ARTIFACT_TYPES
    assert tuple(allowed["evidence_classification"]) == service.ALLOWED_EVIDENCE_CLASSIFICATIONS
    assert tuple(allowed["specification_or_observation"]) == service.ALLOWED_SPECIFICATION_OR_OBSERVATION
    assert tuple(allowed["expected_or_actual_scope"]) == service.ALLOWED_EXPECTED_OR_ACTUAL_SCOPE
    assert set(execution["secret_screening_guidance"]["reject_if_any_string_field_appears_to_contain"]) == set(service.SECRET_INDICATORS)


def test_workstream_plan_is_segmented_and_totals_thirty(execution):
    plan = execution["workstream_segmented_payload_supply_plan"]
    assert len(plan) == 4
    assert {row["workstream_id"] for row in plan} == set(service.ALLOWED_WORKSTREAM_IDS)
    assert sum(row["planned_item_count"] for row in plan) == 30
    assert all(row["actual_supplied_item_count"] == 0 and row["status"] == "MISSING_NOT_ACQUIRED" for row in plan)


def test_future_payload_schema_maps_exactly_ma_001_through_ma_030(execution):
    rows = execution["operator_payload_submission_schema"]["future_evidence_item_templates"]
    assert len(rows) == 30
    assert [row["missing_authority_id"] for row in rows] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert all(row["section_id"] in service.ALLOWED_SECTION_IDS for row in rows)
    assert all(row["workstream_id"] in service.ALLOWED_WORKSTREAM_IDS for row in rows)
    operator_fields = (
        "acceptable_source_artifact_type", "evidence_classification", "specification_or_observation",
        "expected_or_actual_scope", "source_owner_or_origin", "source_reference",
        "digest_or_reproducible_provenance", "authority_statement", "no_secret_attestation",
    )
    assert all(all(row[key] is None for key in operator_fields) for row in rows)


def test_each_future_item_preserves_review_and_closed_change_gates(execution):
    rows = execution["operator_payload_submission_schema"]["future_evidence_item_templates"]
    assert all(row["requires_results_review_before_use"] is True for row in rows)
    closed = ("direct_change_authorized", "remediation_authorized", "retry_authorized", "main_merge_authorized", "actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound", "source_authority_acquired")
    assert all(all(row[key] is False for key in closed) for row in rows)


def test_results_review_prerequisite_recommendation_next_chain_and_gates(execution):
    assert execution["results_review_prerequisite"]["required_before_any_prepared_input_use"] is True
    assert execution["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert execution["recommended_next_task_status"] == "FUTURE_RESULTS_REVIEW_NOT_CREATED"
    assert execution["next_chain"] == list(service.NEXT_CHAIN)
    assert execution["next_gates"] == list(service.NEXT_GATES)


def test_source_execution_failure_and_absent_success_digests_are_preserved(execution):
    assert execution["source_blocked_reason"] == "NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION"
    assert execution["source_success_digests_absent"] is True
    for key in ("prepared_operator_completion_inputs_digest", "prepared_operator_completion_inputs_manifest_digest", "success_execution_digest"):
        assert execution[key] is None
    assert execution["primary_failure_class"] == execution["source_blocked_reason"]
    assert len(execution["secondary_failure_classes"]) == 9


def test_source_chains_and_opaque_durable_receipt_are_bound(execution):
    for key in (
        "source_operator_review_commit", "source_candidate_commit", "source_failure_diagnosis_commit",
        "source_execution_commit", "source_prior_approval_commit", "source_prior_operator_review_commit",
        "source_prior_candidate_commit", "source_prior_completion_failure_diagnosis_commit",
        "source_completion_execution_commit", "source_completion_approval_commit",
        "source_completion_candidate_operator_review_commit", "source_completion_candidate_commit",
        "source_template_preparation_results_review_commit", "source_template_preparation_execution_commit",
    ):
        assert re.fullmatch(r"[0-9a-f]{40}", execution[key])
    assert execution["source_durable_receipt_path"].endswith("EXECUTION_RECEIPT_V1.json")
    assert execution["durable_receipt_not_parsed"] is True


def test_retry_priority_validation_diagnostic_and_observable_facts_are_preserved(execution):
    assert (execution["retry_pytest_passed_count"], execution["retry_pytest_failed_count"], execution["retry_pytest_error_count"], execution["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert sum(row["failed_or_errored_nodeid_count"] for row in execution["priority_1_target_modules"]) == 612
    assert execution["failed_or_errored_nodeids_count"] == 1404
    assert execution["priority1_pre_change_validation_passed_count"] == 675
    assert execution["priority1_post_change_validation_passed_count"] == 675
    assert execution["priority1_validation_is_retry_evidence"] is False
    assert execution["source_exit_code"] == 1
    assert execution["source_combined_output_byte_count"] == 1231380
    assert len(execution["reviewed_observable_failure_families"]) == 4
    assert sum(row["observable_evidence_count"] for row in execution["reviewed_observable_failure_families"]) == 188


def test_counts_actual_coverage_and_count_label_distinctions(execution):
    for key, value in service.COUNTS.items():
        assert execution[key] == value
    assert execution["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert execution["future_completion_requirement_count"] == 67
    assert execution["source_enumerated_future_completion_requirement_count"] == 69
    assert execution["approved_future_completion_requirement_named_count"] == 69
    assert execution["source_approval_enumerated_risk_control_count"] == 146


def test_outputs_risk_controls_and_checklist_are_complete(execution):
    assert [row["output_id"] for row in execution["outputs"]] == list(service.OUTPUT_IDS)
    assert all(row["status"] == service.GENERATED_OUTPUT_STATUS for row in execution["outputs"])
    assert execution["risk_controls"] == list(service.RISK_CONTROLS)
    assert all(item["status"] == "PASS" and item["actual"] is True for item in execution["checklist"])
    assert execution["summary"]["passed_checks"] == execution["summary"]["total_checks"]
    assert execution["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("key", [
    service.EXECUTION_DIGEST_KEY, service.PAYLOAD_SUPPLY_MECHANISM_DIGEST_KEY,
    service.OPERATOR_PAYLOAD_SUBMISSION_SCHEMA_DIGEST_KEY,
    service.ALLOWED_VALUES_AND_SECRET_SCREENING_DIGEST_KEY,
    service.WORKSTREAM_SUPPLY_PLAN_DIGEST_KEY, service.SOURCE_BINDING_DIGEST_KEY,
    service.MANIFEST_DIGEST_KEY,
])
def test_digests_are_deterministic_sha256(key):
    first = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1()
    second = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1()
    assert re.fullmatch(r"[0-9a-f]{64}", first[key])
    assert first[key] == second[key]


def test_source_approval_injection_accepts_exact_binding_and_rejects_drift():
    service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(source_approval=deepcopy(service.SOURCE_APPROVAL_BINDINGS))
    bad = deepcopy(service.SOURCE_APPROVAL_BINDINGS)
    bad["source_approval_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(source_approval=bad)


def test_validator_accepts_valid_execution(execution):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(execution)
    assert result["blocker_count"] == 0


@pytest.mark.parametrize("mutator", [
    lambda x: x.update(artifact_kind="WRONG"),
    lambda x: x.update(execution_status="WRONG"),
    lambda x: x.update(execution_scope="WRONG"),
    lambda x: x.update(source_approval_digest="0" * 64),
    lambda x: x.update(selected_package="WRONG"),
    lambda x: x.update(selected_package_executed=False),
    lambda x: x.update(payload_supply_mechanism_created=False),
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
    lambda x: x.update(pytest_performed_in_execution=True),
    lambda x: x.update(retry_rerun_performed=True),
    lambda x: x.update(cache_read_in_execution=True),
    lambda x: x.update(terminal_logs_parsed=True),
    lambda x: x.update(env_inspection_performed=True),
    lambda x: x.update(diagnostic_receipt_parsed_in_execution=True),
    lambda x: x.update(source_owners_contacted=True),
    lambda x: x.update(provider_requests_made_in_execution=True),
    lambda x: x.update(root_cause_claimed=True),
    lambda x: x.update(retry_success_claimed=True),
    lambda x: x.update(main_merge_readiness_claimed=True),
    lambda x: x.update(runtime_authorized=True),
    lambda x: x.update(broker_execution_authorized=True),
    lambda x: x.pop("payload_supply_mechanism_definition"),
    lambda x: x.pop("operator_payload_submission_schema"),
    lambda x: x.pop("operator_payload_field_checklist"),
    lambda x: x.pop("allowed_values_matrix"),
    lambda x: x.pop("secret_screening_guidance"),
    lambda x: x.pop("workstream_segmented_payload_supply_plan"),
    lambda x: x["operator_payload_submission_schema"]["future_evidence_item_templates"][0].update(source_reference="actual-value"),
    lambda x: x.update(actual_covered_missing_authority_item_count=1),
    lambda x: x.update(missing_authority_items_status="ACQUIRED"),
    lambda x: x.pop("outputs"),
    lambda x: x.pop("recommended_next_task"),
    lambda x: x.pop("next_chain"),
    lambda x: x.pop("risk_controls"),
])
def test_validator_rejects_boundary_tampering(execution, mutator):
    mutator(execution)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(execution)


def test_markdown_includes_all_required_sections(execution):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_markdown_v1(execution)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert "0/30" in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown


def test_writer_writes_only_status_markdown(tmp_path: Path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_REENTRY_OR_PAYLOAD_SUPPLY_EXECUTION_AFTER_APPROVAL_STATUS.md"
    assert artifact["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReentryPayloadSupplyExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_reentry_or_payload_supply_execution_after_approval_v1(Path(protected))
