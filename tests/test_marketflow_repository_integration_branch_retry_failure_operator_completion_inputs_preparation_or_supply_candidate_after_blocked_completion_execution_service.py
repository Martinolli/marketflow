from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_service
    as service,
)


def _candidate() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1()


def _changed(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_CHANGED"
    if isinstance(value, list):
        return []
    if isinstance(value, dict):
        return {}
    raise AssertionError(f"unsupported test value {type(value)!r}")


def test_builds_offline_candidate_from_committed_projection() -> None:
    candidate = _candidate()
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["schema_version"] == service.SCHEMA_VERSION
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["candidate_disposition"] == service.CANDIDATE_DISPOSITION


@pytest.mark.parametrize("field,expected", [
    ("source_failure_diagnosis_commit", service.SOURCE_FAILURE_DIAGNOSIS_COMMIT),
    ("source_failure_diagnosis_digest", service.SOURCE_FAILURE_DIAGNOSIS_DIGEST),
    ("source_failure_classification_digest", service.SOURCE_FAILURE_CLASSIFICATION_DIGEST),
    ("source_operator_input_absence_diagnosis_digest", service.SOURCE_OPERATOR_INPUT_ABSENCE_DIAGNOSIS_DIGEST),
    ("source_coverage_diagnosis_digest", service.SOURCE_COVERAGE_DIAGNOSIS_DIGEST),
    ("source_failure_diagnosis_manifest_digest", service.SOURCE_FAILURE_DIAGNOSIS_MANIFEST_DIGEST),
    ("source_failure_diagnosis_artifact_kind", service.source.ARTIFACT_KIND),
    ("source_failure_diagnosis_status", service.source.DIAGNOSIS_STATUS),
    ("source_failure_diagnosis_scope", service.source.DIAGNOSIS_SCOPE),
    ("primary_failure_class", service.PRIMARY_FAILURE_CLASS),
    ("secondary_failure_classes", list(service.SECONDARY_FAILURE_CLASSES)),
])
def test_source_failure_diagnosis_is_bound(field: str, expected: object) -> None:
    assert _candidate()[field] == expected


@pytest.mark.parametrize("field,expected", list(service.SOURCE_BINDINGS.items()))
def test_all_committed_source_bindings_are_preserved(field: str, expected: object) -> None:
    assert _candidate()[field] == expected


@pytest.mark.parametrize("field,expected", list(service.SOURCE_CONTEXT.items()))
def test_retry_validation_and_diagnostic_context_is_bound(field: str, expected: object) -> None:
    assert _candidate()[field] == expected


@pytest.mark.parametrize("field,expected", list(service.COUNTS.items()))
def test_required_counts_and_count_labels_are_preserved(field: str, expected: object) -> None:
    assert _candidate()[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_candidate_facts_are_true(field: str) -> None:
    assert _candidate()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_selection_execution_authority_and_unsupported_claims_are_false(field: str) -> None:
    assert _candidate()[field] is False


def test_twelve_package_options_have_seven_available_and_five_blocked() -> None:
    candidate = _candidate()
    options = candidate["package_options"]
    assert len(options) == 12
    assert len({item["package_id"] for item in options}) == 12
    assert sum(item["source_status"] != "BLOCKED_NOT_ALLOWED" for item in options) == 7
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in options) == 5
    assert all(item["selected"] is False for item in options)
    assert all(item["approved"] is False for item in options)
    assert all(item["authorized"] is False for item in options)
    assert all(item["executed"] is False for item in options)


def test_recommended_package_is_defined_but_not_selected() -> None:
    candidate = _candidate()
    assert candidate["recommended_operator_completion_inputs_preparation_or_supply_package"] == service.RECOMMENDED_PACKAGE
    recommended = next(item for item in candidate["package_options"] if item["package_id"] == service.RECOMMENDED_PACKAGE)
    assert recommended["candidate_review_status"] == "CANDIDATE_RECOMMENDED_NOT_SELECTED"
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert recommended["selected"] is False


def test_blocked_shortcuts_are_explicitly_disallowed() -> None:
    blocked = [item for item in _candidate()["package_options"] if item["source_status"] == "BLOCKED_NOT_ALLOWED"]
    assert len(blocked) == 5
    assert all(item["candidate_review_status"] == "CANDIDATE_BLOCKED_NOT_ALLOWED" for item in blocked)
    assert all(item["blocked_reason"] for item in blocked)


def test_sixty_two_future_requirements_are_defined_not_executed() -> None:
    requirements = _candidate()["future_input_preparation_requirements"]
    assert len(requirements) == 62
    assert [item["requirement_id"] for item in requirements] == list(service.FUTURE_INPUT_REQUIREMENT_IDS)
    assert all(item["requirement_status"] == "REQUIRED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION" for item in requirements)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in requirements)


def test_future_input_supply_contract_is_planning_only_and_maps_thirty_rows() -> None:
    contract = _candidate()["future_input_supply_contract"]
    assert contract["contract_status"] == "PLANNING_ONLY_NOT_EXECUTED"
    assert len(contract["evidence_items"]) == 30
    assert [item["mapped_missing_authority_id"] for item in contract["evidence_items"]] == [f"MA-{index:03d}" for index in range(1, 31)]
    assert all(item["actual_evidence_supplied"] is True for item in contract["evidence_items"])
    assert all(item["actual_evidence_validated"] is False for item in contract["evidence_items"])
    assert all(item["actual_evidence_bound"] is False for item in contract["evidence_items"])
    assert all(item["results_review_required_before_use"] is True for item in contract["evidence_items"])
    assert all(item["direct_change_authorized_now"] is False for item in contract["evidence_items"])
    assert contract["candidate_inspects_secrets"] is False


def test_contract_allowed_values_and_secret_rejection_markers_are_complete() -> None:
    contract = _candidate()["future_input_supply_contract"]
    assert contract["allowed_section_ids"] == list(service.ALLOWED_SECTION_IDS)
    assert contract["allowed_workstream_ids"] == list(service.ALLOWED_WORKSTREAM_IDS)
    assert contract["allowed_acceptable_source_artifact_types"] == list(service.ALLOWED_ARTIFACT_TYPES)
    assert contract["allowed_evidence_classifications"] == list(service.ALLOWED_EVIDENCE_CLASSIFICATIONS)
    assert contract["allowed_specification_or_observation"] == list(service.ALLOWED_SPECIFICATION_OR_OBSERVATION)
    assert contract["allowed_expected_or_actual_scope"] == list(service.ALLOWED_EXPECTED_OR_ACTUAL_SCOPE)
    assert contract["future_execution_rejected_secret_markers"] == list(service.SECRET_MARKERS)


def test_actual_template_and_coverage_remain_missing() -> None:
    candidate = _candidate()
    assert len(candidate["reviewed_template_rows"]) == 30
    assert len(candidate["missing_authority_mapping"]) == 30
    assert all(item["actual_evidence_supplied"] is False for item in candidate["reviewed_template_rows"])
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in candidate["reviewed_template_rows"])
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in candidate["missing_authority_mapping"])
    assert candidate["actual_coverage"] == {
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    }


def test_priority_modules_families_and_workstreams_are_preserved() -> None:
    candidate = _candidate()
    assert [(item["path"], item["failed_or_errored_nodeid_count"]) for item in candidate["priority_1_target_modules"]] == list(service.PRIORITY_1_TARGET_MODULES)
    assert [(item["family_id"], item["observable_evidence_count"], item["confidence"]) for item in candidate["reviewed_observable_failure_families"]] == list(service.OBSERVABLE_FAMILIES)
    assert [(item["workstream_id"], item["source_family_id"]) for item in candidate["reviewed_workstreams"]] == list(service.WORKSTREAMS)


def test_count_label_distinction_is_not_silently_reconciled() -> None:
    candidate = _candidate()
    distinction = candidate["count_label_distinction"]
    assert distinction["future_completion_requirement_count"] == 67
    assert distinction["source_enumerated_future_completion_requirement_count"] == 69
    assert distinction["approved_future_completion_requirement_named_count"] == 69
    assert distinction["non_goal_count"] == 71
    assert distinction["source_enumerated_non_goal_count"] == 76
    assert distinction["risk_control_count"] == 104
    assert distinction["source_enumerated_risk_control_count"] == 106
    assert distinction["preserved_without_reconciliation"] is True
    assert candidate["non_goal_count"] == 76
    assert candidate["risk_control_count"] == 105
    assert len(candidate["non_goals"]) >= candidate["non_goal_count"]
    assert len(candidate["risk_controls"]) >= candidate["risk_control_count"]


def test_future_plan_planned_outputs_outputs_and_next_gates_are_complete() -> None:
    candidate = _candidate()
    assert len(candidate["future_plan"]) == 17
    assert all(item["plan_status"] == "PLANNED_NOT_EXECUTED" for item in candidate["future_plan"])
    assert len(candidate["planned_outputs"]) == 34
    assert all(item["generation_status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])
    assert [item["output_id"] for item in candidate["outputs"]] == list(service.PLANNED_OUTPUT_IDS)
    assert all(item["status"] == "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_ONLY" for item in candidate["outputs"])
    assert len(candidate["next_chain"]) == 14
    assert len(candidate["next_gates"]) == 18
    assert candidate["next_gates"] == list(service.NEXT_GATES)


def test_non_goals_and_risk_controls_include_every_required_minimum() -> None:
    candidate = _candidate()
    assert [item["non_goal_id"] for item in candidate["non_goals"]] == list(service.NON_GOALS)
    assert all(item["active"] is True for item in candidate["non_goals"])
    assert candidate["risk_controls"] == list(service.RISK_CONTROLS)


def test_summary_and_checklist_pass() -> None:
    candidate = _candidate()
    summary = candidate["summary"]
    assert summary["passed_checks"] == summary["total_checks"] == len(candidate["checklist"])
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert all(check["status"] == "PASS" for check in candidate["checklist"])
    assert all(check["severity"] == "BLOCKER" for check in candidate["checklist"])


def test_all_six_digests_are_deterministic() -> None:
    first, second = _candidate(), _candidate()
    for key in (
        service.CANDIDATE_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY,
        service.INPUT_CONTRACT_DIGEST_KEY, service.SOURCE_BINDING_DIGEST_KEY,
        service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64
        assert set(first[key]) <= set("0123456789abcdef")


def test_accepts_an_injected_exact_committed_source_projection() -> None:
    source_diagnosis = service._committed_source_failure_diagnosis()
    candidate = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
        source_failure_diagnosis=source_diagnosis,
    )
    assert candidate["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST


@pytest.mark.parametrize("field", [
    "source_failure_diagnosis_commit", "source_failure_diagnosis_digest",
    "source_failure_classification_digest", "source_operator_input_absence_diagnosis_digest",
    "source_coverage_diagnosis_digest", "source_failure_diagnosis_manifest_digest",
    "source_completion_execution_blocked_reason", "source_completion_execution_blocked_digest",
    "source_completion_execution_blocked_manifest_digest", "source_approval_digest",
    "source_attestation_digest", "source_operator_review_digest", "source_completion_candidate_digest",
    "source_results_review_digest", "source_template_preparation_execution_digest",
    "source_preparation_candidate_digest", "source_previous_failure_diagnosis_digest",
    "source_blocked_acquisition_execution_reason", "source_acquisition_approval_digest",
    "source_follow_on_results_review_digest", "historical_blocked_remediation_manifest_digest",
    "source_targeted_remediation_plan_digest", "source_durable_receipt_path",
    "retry_pytest_failed_count", "priority_1_total_nodeids", "source_stdout_byte_count",
    "reviewed_template_row_count", "actual_covered_missing_authority_item_count",
])
def test_injected_source_projection_rejects_changed_binding(field: str) -> None:
    source_diagnosis = service._committed_source_failure_diagnosis()
    source_diagnosis[field] = _changed(source_diagnosis[field])
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(
            source_failure_diagnosis=source_diagnosis,
        )


@pytest.mark.parametrize("field", [
    "artifact_kind", "schema_version", "candidate_status", "candidate_scope",
    "source_failure_diagnosis_commit", "source_failure_diagnosis_digest",
    "source_failure_classification_digest", "source_operator_input_absence_diagnosis_digest",
    "source_coverage_diagnosis_digest", "source_failure_diagnosis_manifest_digest",
    "source_completion_execution_commit", "source_completion_execution_artifact_kind",
    "source_completion_execution_status", "source_completion_execution_scope",
    "source_completion_execution_blocked_reason", "source_completion_execution_blocked_digest",
    "source_completion_execution_blocked_manifest_digest", "source_completion_execution_success_digests_absent",
    "primary_failure_class", "source_approval_digest", "source_attestation_digest",
    "selected_operator_source_authority_evidence_package_completion_package",
    "source_operator_review_digest", "source_completion_candidate_digest", "source_results_review_digest",
    "source_template_preparation_execution_digest", "source_preparation_candidate_digest",
    "source_blocked_acquisition_execution_reason", "source_acquisition_approval_digest",
    "retry_pytest_failed_count", "priority_1_total_nodeids", "source_stdout_byte_count",
    "observable_failure_family_count", "reviewed_template_row_count",
    "actual_covered_missing_authority_item_count", "missing_authority_items_status",
    "recommended_operator_completion_inputs_preparation_or_supply_package",
    "predictive_usefulness", "profitability", "runtime_use", "broker_execution",
])
def test_validator_rejects_changed_top_level_value(field: str) -> None:
    candidate = _candidate()
    candidate[field] = _changed(candidate[field])
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_field_set_false(field: str) -> None:
    candidate = _candidate()
    candidate[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_set_true(field: str) -> None:
    candidate = _candidate()
    candidate[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


@pytest.mark.parametrize("field", [
    "package_options", "future_input_preparation_requirements", "future_input_supply_contract",
    "secret_safety_for_future_execution", "future_plan", "planned_outputs", "non_goals",
    "actual_evidence_absence", "actual_coverage", "outputs", "recommended_next_task",
    "next_chain", "next_gates", "risk_controls", "checklist", "summary",
    service.CANDIDATE_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY,
    service.INPUT_CONTRACT_DIGEST_KEY, service.SOURCE_BINDING_DIGEST_KEY,
    service.COVERAGE_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
])
def test_validator_rejects_missing_required_content(field: str) -> None:
    candidate = _candidate()
    candidate.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


@pytest.mark.parametrize("index", range(12))
def test_validator_rejects_any_package_option_selection(index: int) -> None:
    candidate = _candidate()
    candidate["package_options"][index]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


def test_validator_rejects_contract_or_actual_coverage_mutation() -> None:
    candidate = _candidate()
    candidate["future_input_supply_contract"]["evidence_items"][0]["direct_change_authorized_now"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)
    candidate = _candidate()
    candidate["actual_coverage"]["actual_covered_missing_authority_item_count"] = 1
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(candidate)


def test_validator_accepts_committed_candidate() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(_candidate())
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_markdown_contains_every_required_section_and_boundary() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_markdown_v1(_candidate())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.RECOMMENDED_PACKAGE in markdown
    assert service.PRIMARY_FAILURE_CLASS in markdown
    assert "was not parsed" in markdown
    assert "0/30" in markdown


def test_writer_writes_only_candidate_status_markdown(tmp_path: Path) -> None:
    candidate = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(tmp_path)
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_AFTER_BLOCKED_COMPLETION_EXECUTION_STATUS.md"
    assert output.is_file()
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert list(tmp_path.iterdir()) == [output]
