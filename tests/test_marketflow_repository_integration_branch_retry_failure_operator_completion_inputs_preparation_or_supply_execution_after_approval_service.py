from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_service
    as service,
)


def _blocked() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1()


def _valid_inputs() -> dict:
    rows = []
    for index, item in enumerate(service._source_projection()["missing_authority_mapping"], 1):
        rows.append({
            "evidence_id": f"TEST-EVIDENCE-{index:03d}",
            "mapped_missing_authority_id": item["missing_authority_id"],
            "section_id": item["section_id"],
            "workstream_id": item["workstream_id"],
            "acceptable_source_artifact_type": service.ALLOWED_SOURCE_ARTIFACT_TYPES[0],
            "source_owner_or_origin": "TEST_OPERATOR",
            "source_reference": f"TEST-REFERENCE-{index:03d}",
            "digest_or_reproducible_provenance": f"{index:064x}",
            "evidence_classification": "SPECIFICATION",
            "specification_or_observation": "SPECIFICATION",
            "expected_or_actual_scope": "EXPECTED",
            "authority_statement": "TEST OPERATOR AUTHORITY STATEMENT",
            "results_review_required_before_use": True,
            "direct_change_authorized_now": False,
            "remediation_authorized_now": False,
            "retry_authorized_now": False,
            "main_merge_authorized_now": False,
            "actual_evidence_supplied": True,
            "actual_evidence_validated": False,
            "actual_evidence_bound": False,
            "current_status": "PREPARED_OR_SUPPLIED_OPERATOR_COMPLETION_INPUT_PENDING_REVIEW",
        })
    return {
        "package_header": {
            "package_source_owner_or_origin": "TEST_OPERATOR",
            "package_reference": "TEST-OPERATOR-COMPLETION-INPUT-PACKAGE",
            "package_created_utc": "2026-08-23T00:00:00Z",
            "package_digest_or_reproducible_provenance": "a" * 64,
            **{key: True for key in service.REQUIRED_PACKAGE_HEADER_TRUE_FIELDS},
        },
        "evidence_items": rows,
    }


def _success() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(
        operator_completion_inputs=_valid_inputs()
    )


def test_actual_no_input_execution_builds_blocked_offline() -> None:
    artifact = _blocked()
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["execution_status"] == service.BLOCKED_STATUS
    assert artifact["execution_scope"] == service.EXECUTION_SCOPE
    assert artifact["blocked_reason"] == service.NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION
    assert artifact["created_offline"] is True
    assert artifact["governance_only"] is True
    assert artifact["execution_gate_only"] is True


def test_source_approval_identity_digests_and_selected_package_are_bound() -> None:
    artifact = _blocked()
    for key, value in service.SOURCE_APPROVAL_BINDINGS.items():
        assert artifact[key] == value
    assert artifact["source_approval_commit"] == "6623e6a6acb0a8da85fee15a29a52606a7fc6af1"
    assert artifact["source_approval_digest"] == "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72"
    assert artifact["source_attestation_digest"] == "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af"
    assert artifact["selected_operator_completion_inputs_preparation_or_supply_package"] == service.SELECTED_PACKAGE


def test_all_frozen_source_bindings_are_carried_forward() -> None:
    artifact = _blocked()
    projection = service._source_projection()
    for key, value in projection.items():
        assert artifact[key] == value
    assert artifact["source_operator_review_commit"] == "2efc22338250f9de88e76fbf6381796c82f817df"
    assert artifact["source_candidate_commit"] == "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1"
    assert artifact["source_failure_diagnosis_commit"] == "07276fc4b171179eb7210ce679ba2a9bdbd17e8c"
    assert artifact["source_completion_execution_commit"] == "945776b2164969e067d8dcc4809128282d3b1287"
    assert artifact["source_completion_execution_blocked_reason"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED"
    assert artifact["source_completion_execution_success_digests_absent"] is True


def test_retry_priority_diagnostic_family_and_workstream_context_is_preserved() -> None:
    artifact = _blocked()
    assert (artifact["retry_pytest_passed_count"], artifact["retry_pytest_failed_count"], artifact["retry_pytest_error_count"], artifact["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert artifact["priority_1_total_nodeids"] == 612
    assert artifact["top_10_count_sum"] == 1069
    assert artifact["module_summary_module_count"] == 29
    assert artifact["failed_or_errored_nodeids_count"] == 1404
    assert artifact["priority1_pre_change_validation_passed_count"] == 675
    assert artifact["priority1_post_change_validation_passed_count"] == 675
    assert artifact["priority1_validation_is_retry_evidence"] is False
    assert artifact["source_exit_code"] == 1
    assert artifact["source_stdout_byte_count"] == 1231380
    assert artifact["source_stderr_byte_count"] == 0
    assert artifact["source_diagnostic_metadata_only"] is True
    assert len(artifact["reviewed_observable_failure_families"]) == 4
    assert all(item["confidence"] == "HIGH" for item in artifact["reviewed_observable_failure_families"])
    assert len(artifact["reviewed_workstreams"]) == 4
    assert len(artifact["priority_1_target_modules"]) == 5


def test_actual_coverage_template_mapping_and_count_labels_are_preserved() -> None:
    artifact = _blocked()
    assert artifact["reviewed_template_row_count"] == 30
    assert len(artifact["missing_authority_mapping"]) == 30
    assert {item["current_status"] for item in artifact["missing_authority_mapping"]} == {"MISSING_NOT_ACQUIRED"}
    assert artifact["actual_covered_missing_authority_item_count"] == 0
    assert artifact["actual_uncovered_missing_authority_item_count"] == 30
    assert artifact["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert artifact["operator_completion_input_item_count"] == 0
    assert artifact["prepared_operator_completion_input_item_count"] == 0
    assert (artifact["future_completion_requirement_count"], artifact["source_enumerated_future_completion_requirement_count"], artifact["approved_future_completion_requirement_named_count"]) == (67, 69, 69)
    assert (artifact["source_non_goal_count"], artifact["source_enumerated_non_goal_count"], artifact["non_goal_count"]) == (71, 76, 76)
    assert (artifact["source_risk_control_count"], artifact["source_enumerated_risk_control_count"], artifact["risk_control_count"]) == (104, 106, 105)


@pytest.mark.parametrize("field", service.BLOCKED_TRUE_FIELDS)
def test_actual_blocked_fact_is_true(field: str) -> None:
    assert _blocked()[field] is True


@pytest.mark.parametrize("field", (*service.ALWAYS_FALSE_FIELDS, *service.BLOCKED_ONLY_FALSE_FIELDS))
def test_actual_execution_action_authority_or_claim_is_false(field: str) -> None:
    assert _blocked()[field] is False


def test_actual_blocked_success_digests_are_null_and_outputs_are_generated() -> None:
    artifact = _blocked()
    assert artifact["prepared_operator_completion_inputs"] is None
    assert artifact["prepared_operator_completion_input_items"] == []
    assert artifact["prepared_operator_completion_inputs_digest"] is None
    assert artifact["prepared_operator_completion_inputs_manifest_digest"] is None
    assert artifact["success_execution_digest"] is None
    for key in (service.SUCCESS_DIGEST_KEY, service.PREPARED_INPUTS_DIGEST_KEY, service.SUCCESS_MANIFEST_DIGEST_KEY):
        assert key not in artifact
    assert len(artifact["outputs"]) == len(service.BLOCKED_OUTPUT_IDS)
    assert all(item["status"] == "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_BLOCKED_AFTER_APPROVAL_ONLY" for item in artifact["outputs"])


def test_actual_recommendation_next_chain_gates_and_risk_controls() -> None:
    artifact = _blocked()
    assert artifact["recommended_next_task"] == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_V1"
    assert len(artifact["next_chain"]) == 16
    assert len(artifact["next_gates"]) == 20
    assert set(service.EXECUTION_SPECIFIC_RISK_CONTROLS).issubset(artifact["risk_controls"])
    assert len(artifact["risk_controls"]) >= 105


def test_blocked_digests_are_deterministic_and_validator_accepts_artifact() -> None:
    first = _blocked()
    second = _blocked()
    assert first == second
    for key in (service.BLOCKED_DIGEST_KEY, service.SOURCE_BINDING_DIGEST_KEY, service.INPUT_ABSENCE_DIGEST_KEY, service.COVERAGE_DIGEST_KEY, service.BLOCKED_MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(first)
    assert result["execution_digest"] == first[service.BLOCKED_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == 0


def test_synthetic_test_operator_payload_prepares_exactly_30_rows_for_review_only() -> None:
    artifact = _success()
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert artifact["execution_status"] == service.SUCCESS_STATUS
    assert artifact["blocked_reason"] is None
    assert len(artifact["prepared_operator_completion_input_items"]) == 30
    assert artifact["operator_completion_input_item_count"] == 30
    assert artifact["prepared_operator_completion_input_item_count"] == 30
    assert artifact["prepared_operator_completion_inputs_for_results_review"] is True
    assert artifact["ready_for_operator_completion_inputs_preparation_or_supply_results_review"] is True
    assert artifact["operator_completion_inputs_validated_as_evidence"] is False
    assert artifact["operator_completion_inputs_bound_as_evidence"] is False
    assert artifact["source_authority_acquisition_performed"] is False
    assert artifact["actual_covered_missing_authority_item_count"] == 0
    assert artifact["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert artifact["synthetic_success_path_boundary"]["test_only"] is True
    service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


@pytest.mark.parametrize("field", service.SUCCESS_TRUE_FIELDS)
def test_synthetic_success_narrow_permission_is_true(field: str) -> None:
    assert _success()[field] is True


@pytest.mark.parametrize("field", service.ALWAYS_FALSE_FIELDS)
def test_synthetic_success_never_expands_evidence_or_authority(field: str) -> None:
    assert _success()[field] is False


def test_synthetic_success_digests_are_deterministic() -> None:
    first = _success()
    second = _success()
    assert first == second
    for key in (service.SUCCESS_DIGEST_KEY, service.PREPARED_INPUTS_DIGEST_KEY, service.SUCCESS_MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        (lambda value: value.pop("package_header"), "shape invalid"),
        (lambda value: value["evidence_items"].pop(), "exactly 30"),
        (lambda value: value["package_header"].update(package_source_owner_or_origin=""), "package_source_owner_or_origin"),
        (lambda value: value["package_header"].update(package_created_utc="wrong"), "package_created_utc"),
        (lambda value: value["package_header"].update(package_declares_no_secrets=False), "declaration invalid"),
        (lambda value: value["package_header"].update(package_reference="password=example"), "secret-like"),
        (lambda value: value["evidence_items"][0].update(mapped_missing_authority_id="MA-999"), "mapped_missing_authority_id"),
        (lambda value: value["evidence_items"][0].update(section_id="wrong"), "section_id"),
        (lambda value: value["evidence_items"][0].update(workstream_id="wrong"), "workstream_id"),
        (lambda value: value["evidence_items"][0].update(acceptable_source_artifact_type="wrong"), "artifact_type"),
        (lambda value: value["evidence_items"][0].update(evidence_classification="wrong"), "evidence_classification"),
        (lambda value: value["evidence_items"][0].update(specification_or_observation="wrong"), "specification_or_observation"),
        (lambda value: value["evidence_items"][0].update(expected_or_actual_scope="wrong"), "expected_or_actual_scope"),
        (lambda value: value["evidence_items"][0].update(direct_change_authorized_now=True), "direct_change_authorized_now"),
        (lambda value: value["evidence_items"][0].update(remediation_authorized_now=True), "remediation_authorized_now"),
        (lambda value: value["evidence_items"][0].update(retry_authorized_now=True), "retry_authorized_now"),
        (lambda value: value["evidence_items"][0].update(main_merge_authorized_now=True), "main_merge_authorized_now"),
        (lambda value: value["evidence_items"][0].update(actual_evidence_validated=True), "actual_evidence_validated"),
        (lambda value: value["evidence_items"][0].update(actual_evidence_bound=True), "actual_evidence_bound"),
        (lambda value: value["evidence_items"][0].update(current_status="ACCEPTED"), "current_status"),
    ),
)
def test_builder_rejects_invalid_or_unsafe_synthetic_inputs(mutation, message: str) -> None:
    inputs = _valid_inputs()
    mutation(inputs)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match=message):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(operator_completion_inputs=inputs)


@pytest.mark.parametrize(
    ("field", "changed"),
    (
        ("artifact_kind", "wrong"), ("execution_status", "wrong"), ("execution_scope", "wrong"),
        ("blocked_reason", "wrong"), ("source_approval_commit", "0" * 40),
        ("source_approval_digest", "0" * 64), ("source_attestation_digest", "0" * 64),
        ("selected_operator_completion_inputs_preparation_or_supply_package", "wrong"),
        ("source_operator_review_digest", "0" * 64), ("source_candidate_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64), ("source_completion_execution_blocked_reason", "wrong"),
        ("source_completion_execution_blocked_digest", "0" * 64), ("source_completion_execution_blocked_manifest_digest", "0" * 64),
        ("source_completion_execution_success_digests_absent", False), ("source_completion_approval_digest", "0" * 64),
        ("source_completion_candidate_operator_review_digest", "0" * 64), ("source_completion_candidate_digest", "0" * 64),
        ("source_template_preparation_results_review_digest", "0" * 64), ("source_template_preparation_execution_digest", "0" * 64),
        ("source_preparation_candidate_digest", "0" * 64), ("source_acquisition_approval_digest", "0" * 64),
        ("source_follow_on_execution_digest", "0" * 64), ("historical_blocked_remediation_manifest_digest", "0" * 64),
        ("source_targeted_remediation_plan_digest", "0" * 64), ("source_durable_receipt_path", ""),
        ("retry_pytest_failed_count", 0), ("priority_1_total_nodeids", 0), ("source_stdout_byte_count", 0),
        ("observable_failure_family_count", 0), ("reviewed_template_row_count", 29),
        ("actual_covered_missing_authority_item_count", 1), ("missing_authority_items_status", "ACQUIRED"),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"),
        (service.BLOCKED_DIGEST_KEY, "0" * 64), (service.SOURCE_BINDING_DIGEST_KEY, "0" * 64),
        (service.INPUT_ABSENCE_DIGEST_KEY, "0" * 64), (service.COVERAGE_DIGEST_KEY, "0" * 64),
        (service.BLOCKED_MANIFEST_DIGEST_KEY, "0" * 64),
    ),
)
def test_validator_rejects_changed_blocked_top_level_fact(field: str, changed: object) -> None:
    artifact = _blocked()
    artifact[field] = changed
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


@pytest.mark.parametrize("field", (*service.BLOCKED_TRUE_FIELDS, *service.ALWAYS_FALSE_FIELDS, *service.BLOCKED_ONLY_FALSE_FIELDS))
def test_validator_rejects_changed_blocked_boundary(field: str) -> None:
    artifact = _blocked()
    artifact[field] = not artifact[field]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


@pytest.mark.parametrize(
    "collection",
    ("secondary_failure_classes", "reviewed_observable_failure_families", "reviewed_workstreams", "missing_authority_mapping", "outputs", "next_chain", "next_gates", "risk_controls"),
)
def test_validator_rejects_missing_blocked_collection_item(collection: str) -> None:
    artifact = _blocked()
    artifact[collection] = artifact[collection][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


@pytest.mark.parametrize(
    ("collection", "field", "changed"),
    (
        ("reviewed_observable_failure_families", "confidence", "LOW"),
        ("reviewed_workstreams", "workstream_id", "wrong"),
        ("missing_authority_mapping", "current_status", "ACQUIRED"),
    ),
)
def test_validator_rejects_changed_source_context(collection: str, field: str, changed: object) -> None:
    artifact = _blocked()
    artifact[collection][0][field] = changed
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


def test_validator_rejects_success_path_boundary_expansion() -> None:
    artifact = _success()
    artifact["prepared_operator_completion_input_items"][0]["actual_evidence_bound"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="actual_evidence_bound"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(artifact)


def test_default_build_calls_no_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source builder called")

    for module in (service.source, service.source.source, service.source.source.source):
        for name in dir(module):
            if name.startswith(("build_", "write_")):
                monkeypatch.setattr(module, name, forbidden)
    assert _blocked()["source_approval_digest"] == service.SOURCE_APPROVAL_DIGEST


def test_injected_source_approval_must_match_committed_constants() -> None:
    approval = service._committed_source_approval()
    approval["source_approval_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="source_approval"):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(source_approval=approval)


def test_markdown_contains_all_required_sections_and_hides_input_values() -> None:
    blocked_markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_markdown_v1(_blocked())
    success_markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_markdown_v1(_success())
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in blocked_markdown
    assert service.NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION in blocked_markdown
    assert "TEST-REFERENCE-001" not in success_markdown
    assert "MISSING_NOT_ACQUIRED" in blocked_markdown


def test_writer_creates_only_actual_blocked_status(tmp_path: Path) -> None:
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(tmp_path)
    paths = list(tmp_path.iterdir())
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert len(paths) == 1
    assert paths[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_STATUS.md"
    assert service.NO_OPERATOR_COMPLETION_INPUTS_PROVIDED_FOR_PREPARATION_OR_SUPPLY_EXECUTION in paths[0].read_text(encoding="utf-8")


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionError, match="protected output directory"):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1(tmp_path / protected)


def test_service_source_has_no_external_execution_calls() -> None:
    source_text = Path(service.__file__).read_text(encoding="utf-8")
    assert "import subprocess" not in source_text
    assert "subprocess." not in source_text
    assert "source.build_" not in source_text
    assert "source.source.build_" not in source_text
