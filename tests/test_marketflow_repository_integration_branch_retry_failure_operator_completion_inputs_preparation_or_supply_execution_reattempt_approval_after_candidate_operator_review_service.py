from copy import deepcopy
from pathlib import Path
import re

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_service
    as service,
)


def _build():
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1()


def test_builds_offline_from_committed_constants(monkeypatch):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("source builders and execution helpers must not run")

    for name in dir(service.source):
        if name.startswith(("build_", "write_", "validate_")):
            monkeypatch.setattr(service.source, name, forbidden)
    approval = _build()
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["approval_only"] is True


@pytest.mark.parametrize(
    "key,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("approval_status", service.APPROVAL_STATUS),
        ("approval_scope", service.APPROVAL_SCOPE),
        ("source_operator_review_commit", service.SOURCE_OPERATOR_REVIEW_COMMIT),
        ("source_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_operator_review_package_options_review_digest", service.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST),
        ("source_operator_review_future_requirements_review_digest", service.SOURCE_FUTURE_REQUIREMENTS_REVIEW_DIGEST),
        ("source_operator_review_future_contract_review_digest", service.SOURCE_FUTURE_CONTRACT_REVIEW_DIGEST),
        ("source_operator_review_source_binding_review_digest", service.SOURCE_BINDING_REVIEW_DIGEST),
        ("source_operator_review_manifest_digest", service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST),
        ("selected_package", service.SELECTED_PACKAGE),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_identity_source_review_and_selection(key, expected):
    assert _build()[key] == expected


def test_all_source_digest_surfaces_are_bound_exactly():
    approval = _build()
    for bindings in (
        service.SOURCE_OPERATOR_REVIEW_BINDINGS,
        service.source.SOURCE_CANDIDATE_BINDINGS,
        service.source.source.SOURCE_RESULTS_REVIEW_BINDINGS,
        service.source.source.source.SOURCE_EXECUTION_BINDINGS,
    ):
        assert {key: approval[key] for key in bindings} == bindings


def test_source_execution_and_mechanism_are_reviewed_without_rerun_or_regeneration():
    approval = _build()
    assert approval["source_selected_package"] == "PACKAGE_DEFINE_OPERATOR_COMPLETION_INPUT_PAYLOAD_SUPPLY_MECHANISM_FROM_APPROVED_CONTRACT_ONLY"
    assert approval["source_selected_package_executed"] is True
    assert approval["source_payload_supply_mechanism_created"] is True
    assert approval["source_execution_rerun_performed"] is False
    assert approval["payload_supply_mechanism_regenerated"] is False


def test_exact_default_attestation_is_bound_and_non_secret():
    approval = _build()
    assert approval["operator_attestation"] == service.DEFAULT_OPERATOR_ATTESTATION
    assert approval["operator_attestation"]["no_secrets_or_credentials_included_confirmed"] is True


@pytest.mark.parametrize("key", list(service.DEFAULT_OPERATOR_ATTESTATION))
def test_attestation_rejects_missing_and_changed_required_fields(key):
    missing = deepcopy(service.DEFAULT_OPERATOR_ATTESTATION)
    missing.pop(key)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(operator_attestation=missing)
    changed = deepcopy(service.DEFAULT_OPERATOR_ATTESTATION)
    changed[key] = False if isinstance(changed[key], bool) else f"changed-{changed[key]}"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(operator_attestation=changed)


def test_attestation_rejects_unexpected_secret_like_field():
    attestation = deepcopy(service.DEFAULT_OPERATOR_ATTESTATION)
    attestation["api_key"] = "must-not-be-accepted"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(operator_attestation=attestation)


@pytest.mark.parametrize("key", list(service.SOURCE_OPERATOR_REVIEW_BINDINGS))
def test_source_operator_review_injection_rejects_drift(key):
    source_review = deepcopy(service.SOURCE_OPERATOR_REVIEW_BINDINGS)
    source_review[key] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(source_operator_review=source_review)


def test_package_options_select_only_recommended_future_execution_package():
    approval = _build()
    rows = approval["approved_package_options"]
    assert len(rows) == 12
    assert rows[0]["package_id"] == service.SELECTED_PACKAGE
    assert (rows[0]["selected"], rows[0]["approved"], rows[0]["authorized"], rows[0]["executed"]) == (True, True, True, False)
    assert all(not row["selected"] and not row["approved"] and not row["authorized"] and not row["executed"] for row in rows[1:])
    assert all(row["approval_status"] == "PRESERVED_UNSELECTED" for row in rows[1:7])
    assert all(row["approval_status"] == "PRESERVED_BLOCKED_NOT_ALLOWED" for row in rows[7:])


def test_future_requirements_plan_and_outputs_are_approved_not_executed():
    approval = _build()
    requirements = approval["approved_future_requirements"]
    assert [row["requirement_id"] for row in requirements] == list(service.source.source.FUTURE_REQUIREMENT_IDS)
    assert len(requirements) == 58
    assert {row["approval_status"] for row in requirements} == {"APPROVED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_AFTER_CANDIDATE_OPERATOR_REVIEW_ONLY"}
    assert {row["execution_status"] for row in requirements} == {"NOT_EXECUTED"}
    assert len(approval["approved_future_plan"]) == 14
    assert {row["approval_status"] for row in approval["approved_future_plan"]} == {"APPROVED_PLANNED_NOT_EXECUTED"}
    assert {row["execution_status"] for row in approval["approved_future_plan"]} == {"NOT_EXECUTED"}
    assert len(approval["authorized_planned_outputs"]) == 32
    assert {row["authorization_status"] for row in approval["authorized_planned_outputs"]} == {"AUTHORIZED_NOT_GENERATED"}


def test_future_contract_requires_explicit_non_secret_payload_and_preserves_gates():
    approval = _build()
    contract = approval["approved_future_contract"]
    assert contract["explicit_non_secret_operator_payload_required"] is True
    assert len(contract["package_header_schema_fields"]) == 14
    assert len(contract["evidence_item_schema_fields"]) == 21
    assert len(contract["required_item_ids"]) == 30
    assert contract["required_item_ids"] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert all(contract[key] is False for key in ("operator_payload_created", "operator_input_supplied", "evidence_validated", "evidence_bound", "evidence_package_completed", "source_authority_acquired", "remediation_authorized", "retry_authorized", "main_merge_authorized"))
    assert approval["source_mechanism_review_section_count"] == 13
    assert approval["workstream_segment_item_counts"] == [8, 8, 7, 7]
    assert approval["source_execution_governance_output_record_count"] == 42
    assert approval["source_execution_risk_control_count"] == 246


@pytest.mark.parametrize("key,expected", list(service.COUNTS.items()))
def test_required_counts_and_count_label_distinctions(key, expected):
    assert _build()[key] == expected


@pytest.mark.parametrize("key", service.TRUE_FIELDS)
def test_required_true_boundaries(key):
    assert _build()[key] is True


@pytest.mark.parametrize("key", service.FALSE_FIELDS)
def test_required_false_boundaries(key):
    assert _build()[key] is False


def test_actual_payload_evidence_and_authority_remain_absent():
    approval = _build()
    assert approval["actual_covered_missing_authority_item_count"] == 0
    assert approval["actual_uncovered_missing_authority_item_count"] == 30
    assert approval["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert approval["operator_payload_created"] is False
    assert approval["operator_source_authority_evidence_package_completed"] is False
    assert approval["actual_evidence_items_filled"] is False
    assert approval["source_authority_evidence_acquired"] is False


@pytest.mark.parametrize(
    "key",
    [
        service.APPROVAL_DIGEST_KEY,
        service.ATTESTATION_DIGEST_KEY,
        service.PACKAGE_OPTIONS_DIGEST_KEY,
        service.FUTURE_REQUIREMENTS_DIGEST_KEY,
        service.FUTURE_CONTRACT_DIGEST_KEY,
        service.SOURCE_BINDING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_digests_are_deterministic_sha256(key):
    first = _build()[key]
    second = _build()[key]
    assert first == second
    assert re.fullmatch(r"[0-9a-f]{64}", first)


def test_checklist_passes_without_blockers():
    summary = _build()["summary"]
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


@pytest.mark.parametrize(
    "path,value",
    [
        (("artifact_kind",), "wrong"),
        (("approval_status",), "wrong"),
        (("approval_scope",), "wrong"),
        (("source_operator_review_digest",), "0" * 64),
        (("source_candidate_digest",), "0" * 64),
        (("source_results_review_digest",), "0" * 64),
        (("source_execution_digest",), "0" * 64),
        (("source_payload_supply_mechanism_review_digest",), "0" * 64),
        (("source_operator_payload_submission_schema_review_digest",), "0" * 64),
        (("source_allowed_values_and_secret_screening_review_digest",), "0" * 64),
        (("source_workstream_supply_plan_review_digest",), "0" * 64),
        (("source_binding_review_digest",), "0" * 64),
        (("source_results_review_manifest_digest",), "0" * 64),
        (("source_selected_package_executed",), False),
        (("source_payload_supply_mechanism_created",), False),
        (("source_execution_rerun_performed",), True),
        (("payload_supply_mechanism_regenerated",), True),
        (("selected_package",), "wrong"),
        (("selected_package_selected",), False),
        (("selected_package_approved",), False),
        (("selected_package_authorized",), False),
        (("selected_package_executed",), True),
        (("operator_payload_created",), True),
        (("operator_completion_inputs_prepared",), True),
        (("operator_completion_inputs_supplied",), True),
        (("operator_completion_inputs_provided",), True),
        (("operator_completion_inputs_validated_as_evidence",), True),
        (("operator_completion_inputs_bound_as_evidence",), True),
        (("operator_completion_inputs_preparation_or_supply_execution_reattempt_created",), True),
        (("operator_completion_inputs_preparation_or_supply_execution_reattempt_performed",), True),
        (("operator_source_authority_evidence_package_completed",), True),
        (("operator_source_authority_evidence_package_created",), True),
        (("actual_evidence_items_filled",), True),
        (("source_authority_acquisition_execution_created",), True),
        (("source_authority_evidence_acquired",), True),
        (("external_evidence_acquired",), True),
        (("production_code_modified",), True),
        (("existing_tests_modified",), True),
        (("expected_digests_updated",), True),
        (("patch_generated",), True),
        (("pytest_performed_in_approval",), True),
        (("retry_rerun_performed",), True),
        (("cache_read_in_approval",), True),
        (("provider_requests_made_in_approval",), True),
        (("root_cause_claimed",), True),
        (("retry_success_claimed",), True),
        (("ready_for_retry_candidate",), True),
        (("ready_for_main_merge_approval",), True),
        (("actual_covered_missing_authority_item_count",), 1),
        (("missing_authority_items_status",), "ACQUIRED"),
        (("outputs",), []),
        (("risk_controls",), []),
        (("next_chain",), []),
    ],
)
def test_validator_rejects_boundary_tampering(path, value):
    approval = _build()
    approval[path[0]] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(approval)


def test_validator_accepts_valid_approval():
    summary = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(_build())
    assert summary["blocker_count"] == 0


def test_markdown_contains_every_required_section():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_markdown_v1(_build())
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.SELECTED_PACKAGE in markdown
    assert "58 requirements" in markdown
    assert "coverage remains 0/30" in markdown.lower()


def test_writer_writes_only_status_markdown(tmp_path: Path):
    approval = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert [path.name for path in files] == ["MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_REATTEMPT_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"]


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsReattemptApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_reattempt_approval_after_candidate_operator_review_v1(Path(protected))
