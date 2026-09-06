from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_service
    as service,
)


def _confirmations() -> dict:
    return {
        **service.ATTESTATION_VALUE_FIELDS,
        **{key: True for key in service.ATTESTATION_BOOLEAN_FIELDS},
    }


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations=_confirmations(),
    )


def _approval() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_exact_non_secret_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_operator_completion_inputs_preparation_or_supply_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert attestation["operator_attestation_version"] == service.SCHEMA_VERSION
    assert len(attestation[service.ATTESTATION_DIGEST_KEY]) == 64


@pytest.mark.parametrize(
    ("override", "message"),
    (
        ({"operator_attestation_phrase": "wrong"}, "operator_attestation_phrase mismatch"),
        ({"selected_operator_completion_inputs_preparation_or_supply_package": "wrong"}, "selected package mismatch"),
        ({"operator_decision": "wrong"}, "operator_decision mismatch"),
        ({"operator_reference": ""}, "operator_reference invalid"),
        ({"operator_attestation_timestamp_utc": "not-utc"}, "operator_attestation_timestamp_utc invalid"),
    ),
)
def test_attestation_builder_rejects_invalid_core_fields(override: dict, message: str) -> None:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_operator_completion_inputs_preparation_or_supply_package": service.SELECTED_PACKAGE,
        "operator_decision": service.OPERATOR_DECISION,
        "operator_confirmations": _confirmations(),
    }
    kwargs.update(override)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match=message):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1(**kwargs)


@pytest.mark.parametrize("confirmation", (*service.ATTESTATION_VALUE_FIELDS, *service.ATTESTATION_BOOLEAN_FIELDS))
def test_attestation_builder_rejects_changed_confirmation(confirmation: str) -> None:
    confirmations = _confirmations()
    confirmations[confirmation] = False if confirmations[confirmation] is True else "wrong"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="operator_confirmations"):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_attestation_v1(
            operator_reference="TEST_OPERATOR",
            operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


def test_approval_identity_selection_and_current_source_review_are_bound() -> None:
    approval = _approval()
    assert approval["artifact_kind"] == service.ARTIFACT_KIND
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert approval["approval_scope"] == service.APPROVAL_SCOPE
    assert approval["selected_operator_completion_inputs_preparation_or_supply_package"] == service.SELECTED_PACKAGE
    assert approval["source_operator_review_commit"] == service.SOURCE_OPERATOR_REVIEW_COMMIT
    assert approval["source_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_package_options_review_digest"] == service.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST
    assert approval["source_input_contract_review_digest"] == service.SOURCE_INPUT_CONTRACT_REVIEW_DIGEST
    assert approval["source_binding_review_digest"] == service.SOURCE_BINDING_REVIEW_DIGEST
    assert approval["source_coverage_review_digest"] == service.SOURCE_COVERAGE_REVIEW_DIGEST
    assert approval["source_operator_review_manifest_digest"] == service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST


def test_candidate_failure_completion_and_approval_chains_are_bound() -> None:
    approval = _approval()
    expected = {
        "source_candidate_commit": "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1",
        "source_candidate_digest": "41a2df4be129a88b829439dadc3e0969715853944068f73800fd673720f02ca8",
        "source_failure_diagnosis_commit": "07276fc4b171179eb7210ce679ba2a9bdbd17e8c",
        "source_failure_diagnosis_digest": "3789d82ea1ef74aed2a6d7d7b1404254c0b5672eaf3c8080095ec21907e50759",
        "source_completion_execution_commit": "945776b2164969e067d8dcc4809128282d3b1287",
        "source_completion_execution_blocked_reason": "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED",
        "source_completion_execution_blocked_digest": "5fe3269b5787730da7d0287029af15956e9efae13f436c58c94e93ff7160b2c1",
        "source_completion_execution_blocked_manifest_digest": "97b42143837d78ea6dba2d13a53cad5f42ffdcf8ea3f82d55c6ab521a9564cc6",
        "source_completion_approval_commit": "40bee1289543bb07e64e383eb2e1c61d83615bd5",
        "source_completion_approval_digest": "f6c37c0a7c64487cdf9adb218f8d12b8c0a2dacc4d4c1debf96105d1b5ee954c",
        "source_completion_approval_attestation_digest": "5434cbb4c94d22f1e4fefb3efc0e6e651401a22d6217d4c118638fa6d38dc714",
        "source_completion_candidate_operator_review_commit": "d71bfb14a656592ab637d94d9dd30d73912104b0",
        "source_completion_candidate_operator_review_digest": "3f866714c903d3ae53d67fd46462d73eb7627fa73cb532e6023a561a5dd52663",
        "source_completion_candidate_commit": "7af6b1b5ad223f92da0997e2b7abcb73543470df",
        "source_completion_candidate_digest": "c5ab1fd16d42cc4cdb0a8a610867ea9ffea75e19ef77769afab7da2fa2abd207",
    }
    for key, value in expected.items():
        assert approval[key] == value
    assert approval["source_completion_execution_success_digests_absent"] is True
    assert approval["primary_failure_class"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED"
    assert len(approval["secondary_failure_classes"]) == 7


def test_template_preparation_acquisition_follow_on_and_recovery_chains_are_bound() -> None:
    approval = _approval()
    required_fragments = (
        "template_preparation_results_review", "template_preparation_execution", "preparation_candidate",
        "blocked_acquisition", "acquisition_approval", "follow_on", "enrichment", "historical",
        "remediation", "diagnostic", "receipt_recovery", "planning", "detail_binding", "materialized",
        "recovery", "module_grouping", "staged_inventory",
    )
    for fragment in required_fragments:
        assert any(fragment in key and key.endswith(("_digest", "_manifest_digest")) for key in approval)
    assert approval["source_blocked_acquisition_execution_reason"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
    assert approval["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"


def test_durable_retry_priority_diagnostic_and_reviewed_context_are_preserved() -> None:
    approval = _approval()
    assert approval["source_durable_receipt_path"].endswith("_RECEIPT_V1.json")
    assert approval["durable_receipt_not_parsed"] is True
    assert (approval["retry_pytest_passed_count"], approval["retry_pytest_failed_count"], approval["retry_pytest_error_count"], approval["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert approval["priority_1_total_nodeids"] == 612
    assert approval["top_10_count_sum"] == 1069
    assert approval["failed_or_errored_nodeids_count"] == 1404
    assert approval["priority1_validation_is_retry_evidence"] is False
    assert approval["source_diagnostic_metadata_only"] is True
    assert len(approval["reviewed_observable_failure_families"]) == 4
    assert all(item["confidence"] == "HIGH" for item in approval["reviewed_observable_failure_families"])
    assert len(approval["reviewed_workstreams"]) == 4
    assert len(approval["priority_1_target_modules"]) == 5


def test_template_input_absence_actual_coverage_and_count_labels_are_preserved() -> None:
    approval = _approval()
    assert approval["reviewed_template_row_count"] == 30
    assert len(approval["missing_authority_mapping"]) == 30
    assert {item["current_status"] for item in approval["missing_authority_mapping"]} == {"MISSING_NOT_ACQUIRED"}
    assert approval["operator_completion_input_item_count"] == 0
    assert approval["actual_covered_missing_authority_item_count"] == 0
    assert approval["actual_uncovered_missing_authority_item_count"] == 30
    assert approval["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert approval["count_label_distinction_preserved"] is True
    assert (approval["future_completion_requirement_count"], approval["source_enumerated_future_completion_requirement_count"], approval["approved_future_completion_requirement_named_count"]) == (67, 69, 69)
    assert (approval["source_non_goal_count"], approval["source_enumerated_non_goal_count"], approval["non_goal_count"]) == (71, 76, 76)
    assert (approval["source_risk_control_count"], approval["source_enumerated_risk_control_count"], approval["risk_control_count"]) == (104, 106, 105)


def test_selected_supporting_and_blocked_packages_preserve_approval_boundary() -> None:
    approval = _approval()
    package = approval["approved_package"]
    assert package["package_id"] == service.SELECTED_PACKAGE
    assert package["selected"] is True and package["approved"] is True
    assert package["authorized_for_future_execution"] is True and package["executed"] is False
    assert len(approval["package_options"]) == 12
    assert len(approval["supporting_packages"]) == 6
    assert all(not item["selected"] and not item["approved"] for item in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 5
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" and not item["approved"] for item in approval["blocked_packages"])


def test_future_requirements_contract_plan_outputs_non_goals_and_recommendation() -> None:
    approval = _approval()
    assert len(approval["approved_future_input_preparation_requirements"]) == 62
    assert all(item["approval_status"].startswith("APPROVED_FOR_FUTURE") and item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_input_preparation_requirements"])
    contract = approval["approved_future_input_supply_contract"]
    assert contract["contract_status"] == "APPROVED_PLANNING_ONLY_NOT_EXECUTED"
    assert len(contract["evidence_items"]) == 30
    assert all(not item["direct_change_authorized_now"] and not item["remediation_authorized_now"] and not item["retry_authorized_now"] and not item["main_merge_authorized_now"] for item in contract["evidence_items"])
    assert len(approval["approved_future_plan"]) == 17
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_plan"])
    assert len(approval["planned_outputs"]) == 34
    assert all(item["status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["planned_outputs"])
    assert all(item["preserved"] for item in approval["non_goals"])
    assert approval["recommended_next_task"] == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_V1"
    assert len(approval["next_chain"]) == 12 and len(approval["next_gates"]) == 16
    assert len(approval["risk_controls"]) >= 105


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_approval_fact_is_true(field: str) -> None:
    assert _approval()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_action_authority_or_claim_is_false(field: str) -> None:
    assert _approval()[field] is False


def test_approval_and_all_six_digests_are_deterministic_and_valid() -> None:
    first = _approval()
    second = _approval()
    assert first == second
    for key in (service.APPROVAL_DIGEST_KEY, service.ATTESTATION_DIGEST_KEY, service.PACKAGE_OPTIONS_DIGEST_KEY, service.FUTURE_REQUIREMENTS_DIGEST_KEY, service.FUTURE_PLAN_DIGEST_KEY, service.MANIFEST_DIGEST_KEY):
        assert len(first[key]) == 64
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(first)
    assert result["approval_digest"] == first[service.APPROVAL_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "changed"),
    (
        ("artifact_kind", "wrong"), ("approval_status", "wrong"), ("approval_scope", "wrong"),
        ("selected_operator_completion_inputs_preparation_or_supply_package", "wrong"),
        ("source_operator_review_commit", "0" * 40), ("source_operator_review_digest", "0" * 64),
        ("source_package_options_review_digest", "0" * 64), ("source_input_contract_review_digest", "0" * 64),
        ("source_binding_review_digest", "0" * 64), ("source_coverage_review_digest", "0" * 64),
        ("source_operator_review_manifest_digest", "0" * 64), ("source_candidate_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64), ("source_completion_execution_blocked_reason", "wrong"),
        ("source_completion_execution_blocked_digest", "0" * 64), ("source_completion_execution_blocked_manifest_digest", "0" * 64),
        ("source_completion_execution_success_digests_absent", False), ("source_completion_approval_digest", "0" * 64),
        ("source_completion_approval_attestation_digest", "0" * 64), ("source_completion_candidate_digest", "0" * 64),
        ("source_template_preparation_results_review_digest", "0" * 64), ("source_template_preparation_execution_digest", "0" * 64),
        ("source_preparation_candidate_digest", "0" * 64), ("source_blocked_acquisition_execution_reason", "wrong"),
        ("source_follow_on_execution_digest", "0" * 64), ("historical_blocked_remediation_manifest_digest", "0" * 64),
        ("source_targeted_remediation_plan_digest", "0" * 64), ("source_durable_receipt_path", ""),
        ("retry_pytest_failed_count", 0), ("priority_1_total_nodeids", 0), ("source_stdout_byte_count", 0),
        ("observable_failure_family_count", 0), ("reviewed_template_row_count", 29),
        ("actual_covered_missing_authority_item_count", 1), ("missing_authority_items_status", "ACQUIRED"),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"),
        (service.APPROVAL_DIGEST_KEY, "0" * 64), (service.ATTESTATION_DIGEST_KEY, "0" * 64),
    ),
)
def test_validator_rejects_changed_top_level_fact(field: str, changed: object) -> None:
    approval = _approval()
    approval[field] = changed
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)


@pytest.mark.parametrize("field", (*service.TRUE_FIELDS, *service.FALSE_FIELDS))
def test_validator_rejects_changed_boundary_field(field: str) -> None:
    approval = _approval()
    approval[field] = not approval[field]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)


@pytest.mark.parametrize(
    "collection",
    ("secondary_failure_classes", "reviewed_observable_failure_families", "reviewed_workstreams", "missing_authority_mapping", "package_options", "approved_future_input_preparation_requirements", "approved_future_plan", "planned_outputs", "supporting_packages", "blocked_packages", "non_goals", "next_chain", "next_gates", "risk_controls"),
)
def test_validator_rejects_missing_collection_item(collection: str) -> None:
    approval = _approval()
    approval[collection] = approval[collection][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)


@pytest.mark.parametrize(
    ("collection", "field", "changed"),
    (
        ("package_options", "approved", False),
        ("package_options", "authorized_for_future_execution", False),
        ("package_options", "executed", True),
        ("supporting_packages", "selected", True),
        ("blocked_packages", "approved", True),
        ("reviewed_observable_failure_families", "confidence", "LOW"),
        ("reviewed_workstreams", "workstream_id", "wrong"),
        ("missing_authority_mapping", "current_status", "ACQUIRED"),
    ),
)
def test_validator_rejects_changed_nested_boundary(collection: str, field: str, changed: object) -> None:
    approval = _approval()
    approval[collection][0][field] = changed
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)


def test_validator_rejects_wrong_attestation_phrase() -> None:
    approval = _approval()
    approval["operator_attestation"]["operator_attestation_phrase"] = "wrong"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="operator_attestation_phrase"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(approval)


def test_default_build_uses_committed_constants_without_calling_source_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source builder called")

    for module in (service.source, service.source.source):
        for name in dir(module):
            if name.startswith(("build_", "write_")):
                monkeypatch.setattr(module, name, forbidden)
    assert _approval()["source_operator_review_commit"] == service.SOURCE_OPERATOR_REVIEW_COMMIT


def test_injected_source_review_must_match_committed_constants() -> None:
    review = service._committed_source_operator_review()
    review["source_operator_review_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="source_operator_review"):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
            source_operator_review=review,
            operator_attestation=_attestation(),
        )


def test_markdown_contains_every_required_section_and_boundary() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_markdown_v1(_approval())
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.SELECTED_PACKAGE in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown
    assert service.APPROVAL_SCOPE in markdown


def test_writer_round_trips_only_requested_status_document(tmp_path: Path) -> None:
    approval = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )
    paths = list(tmp_path.iterdir())
    assert len(paths) == 1
    assert paths[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    assert approval["approval_status"] in paths[0].read_text(encoding="utf-8")


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyApprovalError, match="protected output directory"):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_approval_after_candidate_operator_review_v1(
            tmp_path / protected,
            operator_attestation=_attestation(),
        )


def test_service_source_contains_no_execution_or_upstream_builder_calls() -> None:
    source_text = Path(service.__file__).read_text(encoding="utf-8")
    assert "import subprocess" not in source_text
    assert "subprocess." not in source_text
    assert "source.build_" not in source_text
    assert "source.source.build_" not in source_text
    assert ".pytest_cache" in source_text
