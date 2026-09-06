from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_service
    as service,
)


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations={
            **service.ATTESTATION_VALUE_FIELDS,
            **{key: True for key in service.ATTESTATION_BOOLEAN_FIELDS},
        },
    )


def _approval() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builds_required_non_secret_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_operator_source_authority_evidence_package_completion_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert len(attestation[service.ATTESTATION_DIGEST_KEY]) == 64


@pytest.mark.parametrize(
    ("override", "message"),
    (
        ({"operator_attestation_phrase": "wrong"}, "operator_attestation_phrase mismatch"),
        ({"selected_operator_source_authority_evidence_package_completion_package": "wrong"}, "selected completion package mismatch"),
        ({"operator_decision": "wrong"}, "operator_decision mismatch"),
        ({"operator_reference": ""}, "operator_reference invalid"),
        ({"operator_attestation_timestamp_utc": "not-utc"}, "operator_attestation_timestamp_utc invalid"),
    ),
)
def test_attestation_rejects_invalid_core_fields(override: dict, message: str) -> None:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_operator_source_authority_evidence_package_completion_package": service.SELECTED_PACKAGE,
        "operator_decision": service.OPERATOR_DECISION,
        "operator_confirmations": {**service.ATTESTATION_VALUE_FIELDS, **{key: True for key in service.ATTESTATION_BOOLEAN_FIELDS}},
    }
    kwargs.update(override)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match=message):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1(**kwargs)


@pytest.mark.parametrize("confirmation", (*service.ATTESTATION_VALUE_FIELDS, *service.ATTESTATION_BOOLEAN_FIELDS))
def test_attestation_rejects_changed_confirmation(confirmation: str) -> None:
    confirmations = {**service.ATTESTATION_VALUE_FIELDS, **{key: True for key in service.ATTESTATION_BOOLEAN_FIELDS}}
    confirmations[confirmation] = False if confirmations[confirmation] is True else "wrong"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="operator_confirmations"):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_attestation_v1(
            operator_reference="TEST_OPERATOR",
            operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


def test_approval_identity_selection_and_source_review_binding() -> None:
    approval = _approval()
    assert approval["artifact_kind"] == service.ARTIFACT_KIND
    assert approval["approval_status"] == service.APPROVAL_STATUS
    assert approval["approval_scope"] == service.APPROVAL_SCOPE
    assert approval["selected_operator_source_authority_evidence_package_completion_package"] == service.SELECTED_PACKAGE
    assert approval["source_operator_review_commit"] == service.SOURCE_OPERATOR_REVIEW_COMMIT
    assert approval["source_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST
    assert approval["source_package_options_review_digest"] == service.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST
    assert approval["source_operator_input_requirements_review_digest"] == service.SOURCE_OPERATOR_INPUT_REQUIREMENTS_REVIEW_DIGEST
    assert approval["source_template_binding_review_digest"] == service.SOURCE_TEMPLATE_BINDING_REVIEW_DIGEST
    assert approval["source_coverage_review_digest"] == service.SOURCE_COVERAGE_REVIEW_DIGEST
    assert approval["source_operator_review_manifest_digest"] == service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST


def test_completion_candidate_and_template_preparation_chain_are_bound() -> None:
    approval = _approval()
    assert approval["source_completion_candidate_commit"] == service.SOURCE_COMPLETION_CANDIDATE_COMMIT
    assert approval["source_completion_candidate_digest"] == service.SOURCE_COMPLETION_CANDIDATE_DIGEST
    assert approval["source_completion_candidate_manifest_digest"] == service.SOURCE_COMPLETION_CANDIDATE_MANIFEST_DIGEST
    for key in (
        "source_results_review_digest", "source_template_review_digest", "source_evidence_item_template_review_digest",
        "source_preparation_checklist_review_digest", "source_template_coverage_review_digest", "source_results_review_manifest_digest",
        "source_execution_digest", "source_package_template_digest", "source_evidence_item_template_digest",
        "source_preparation_checklist_digest", "source_execution_manifest_digest", "source_approval_digest", "source_attestation_digest",
    ):
        assert isinstance(approval[key], str) and len(approval[key]) == 64


def test_failure_acquisition_follow_on_historical_and_recovery_chain_are_bound() -> None:
    approval = _approval()
    assert approval["source_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert approval["source_blocked_acquisition_execution_reason"] == service.SOURCE_BLOCKED_REASON
    assert approval["source_blocked_acquisition_execution_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST
    assert approval["source_acquisition_approval_digest"] == service.SOURCE_APPROVAL_DIGEST
    assert approval["source_acquisition_attestation_digest"] == service.SOURCE_ATTESTATION_DIGEST
    assert approval["source_durable_receipt_path"].endswith("_RECEIPT_V1.json")
    required_digest_fragments = ("follow_on", "historical", "remediation", "diagnostic", "recapture", "planning", "detail_binding")
    for fragment in required_digest_fragments:
        assert any(fragment in key and key.endswith("_digest") for key in approval)


def test_retry_priority_diagnostic_and_reviewed_context_is_preserved() -> None:
    approval = _approval()
    assert approval["priority_1_total_nodeids"] == 612
    assert approval["top_10_count_sum"] == 1069
    assert approval["failed_or_errored_nodeids_count"] == 1404
    assert approval["observable_failure_family_count"] == 4
    assert approval["total_observable_evidence_items"] == 188
    assert len(approval["reviewed_observable_failure_families"]) == 4
    assert len(approval["reviewed_workstreams"]) == 4
    assert len(approval["reviewed_template_rows"]) == 30
    assert approval["diagnostic_capture_evidence_summary"]["diagnostic_only"] is True


def test_actual_evidence_absence_and_count_label_distinction_are_preserved() -> None:
    approval = _approval()
    assert approval["operator_source_authority_evidence_item_count"] == 0
    assert approval["actual_covered_missing_authority_item_count"] == 0
    assert approval["actual_uncovered_missing_authority_item_count"] == 30
    assert approval["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert approval["future_completion_requirement_count"] == 67
    assert approval["source_enumerated_future_completion_requirement_count"] == 69
    assert approval["non_goal_count"] == 71
    assert approval["source_enumerated_non_goal_count"] == 76
    assert approval["risk_control_count"] == 104
    assert approval["source_enumerated_risk_control_count"] == 106
    assert approval["count_label_distinction"]["all_named_items_preserved"] is True


def test_approved_package_future_requirements_plan_and_outputs() -> None:
    approval = _approval()
    package = approval["approved_package"]
    assert package["package_id"] == service.SELECTED_PACKAGE
    assert package["selected"] is True and package["approved"] is True
    assert package["authorized_for_future_execution"] is True and package["executed"] is False
    assert len(approval["approved_future_completion_requirements"]) == 69
    assert len(approval["approved_future_completion_plan"]) == 17
    assert len(approval["planned_outputs"]) == 33
    assert all(item["status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["planned_outputs"])
    assert len(approval["supporting_packages"]) == 6
    assert len(approval["blocked_packages"]) == 5
    assert all(item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in approval["blocked_packages"])


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_approval_fact_is_true(field: str) -> None:
    assert _approval()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_authority_or_action_is_false(field: str) -> None:
    assert _approval()[field] is False


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_future_completion_permission_is_narrowly_true(field: str) -> None:
    approval = _approval()
    assert approval[field] is True
    assert approval["future_execution_boundary"][field] is True


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_future_completion_permission_remains_false(field: str) -> None:
    approval = _approval()
    assert approval[field] is False
    assert approval["future_execution_boundary"][field] is False


def test_approval_is_deterministic_and_validates() -> None:
    first = _approval()
    second = _approval()
    assert first == second
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(first)
    assert result["approval_digest"] == first[service.APPROVAL_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "changed"),
    (
        ("artifact_kind", "wrong"), ("approval_status", "wrong"), ("approval_scope", "wrong"),
        ("selected_operator_source_authority_evidence_package_completion_package", "wrong"),
        ("source_operator_review_digest", "0" * 64), ("source_package_options_review_digest", "0" * 64),
        ("source_operator_input_requirements_review_digest", "0" * 64), ("source_template_binding_review_digest", "0" * 64),
        ("source_coverage_review_digest", "0" * 64), ("source_operator_review_manifest_digest", "0" * 64),
        ("source_completion_candidate_digest", "0" * 64), ("source_results_review_digest", "0" * 64),
        ("source_execution_digest", "0" * 64), ("source_approval_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64), ("source_blocked_acquisition_execution_reason", "wrong"),
        ("source_acquisition_approval_digest", "0" * 64), ("source_durable_receipt_path", ""),
        ("priority_1_total_nodeids", 0), ("top_10_count_sum", 0), ("failed_or_errored_nodeids_count", 0),
        ("reviewed_template_row_count", 0), ("actual_covered_missing_authority_item_count", 1),
        ("missing_authority_items_status", "ACQUIRED"), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"),
    ),
)
def test_validator_rejects_changed_top_level_fact(field: str, changed: object) -> None:
    approval = _approval()
    approval[field] = changed
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(approval)


@pytest.mark.parametrize("field", (*service.TRUE_FIELDS, *service.FALSE_FIELDS))
def test_validator_rejects_changed_boundary_field(field: str) -> None:
    approval = _approval()
    approval[field] = not approval[field]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(approval)


@pytest.mark.parametrize(
    "collection",
    ("approved_future_completion_requirements", "approved_future_completion_plan", "planned_outputs", "supporting_packages", "blocked_packages", "next_chain", "next_gates", "risk_controls"),
)
def test_validator_rejects_missing_approved_collection_item(collection: str) -> None:
    approval = _approval()
    approval[collection] = approval[collection][:-1]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="mismatch"):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(approval)


def test_default_build_uses_committed_data_without_calling_public_source_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source builder called")

    for name in dir(service.source):
        if name.startswith("build_") or name.startswith("write_"):
            monkeypatch.setattr(service.source, name, forbidden)
    assert _approval()["source_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST


def test_injected_source_review_must_match_committed_constants() -> None:
    review = service._committed_source_operator_review()
    review.update(service.SOURCE_REVIEW_DIGEST_FIELDS)
    review[service.source.OPERATOR_REVIEW_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="source_operator_review"):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
            source_operator_review=review, operator_attestation=_attestation()
        )


def test_markdown_contains_every_required_section_and_boundary() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_markdown_v1(_approval())
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.SELECTED_PACKAGE in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown
    assert service.APPROVAL_SCOPE in markdown


def test_writer_round_trips_status_document(tmp_path: Path) -> None:
    approval = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    assert path.exists()
    assert approval["approval_status"] in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directory(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackageCompletionApprovalError, match="protected output directory"):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_completion_approval_after_candidate_operator_review_v1(
            tmp_path / protected, operator_attestation=_attestation()
        )
