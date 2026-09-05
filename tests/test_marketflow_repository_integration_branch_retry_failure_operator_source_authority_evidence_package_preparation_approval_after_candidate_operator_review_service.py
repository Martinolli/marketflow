from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_service
    as service,
)


def _confirmations() -> dict:
    return {
        **service.ATTESTATION_VALUE_FIELDS,
        **{key: True for key in service.ATTESTATION_BOOLEAN_FIELDS},
    }


def _attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations=_confirmations(),
    )


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
        operator_attestation=_attestation()
    )


def _reject(approval: dict) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(approval)


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_operator_source_authority_evidence_package_preparation_package"] == service.SELECTED_PACKAGE
    assert attestation["operator_attestation_version"] == service.SCHEMA_VERSION
    assert len(attestation[service.ATTESTATION_DIGEST_KEY]) == 64
    assert set(service.ATTESTATION_VALUE_FIELDS).issubset(attestation)
    assert set(service.ATTESTATION_BOOLEAN_FIELDS).issubset(attestation)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("operator_attestation_phrase", "WRONG"),
        ("selected_operator_source_authority_evidence_package_preparation_package", "WRONG"),
        ("operator_decision", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", "2026-08-23"),
    ),
)
def test_attestation_builder_rejects_invalid_identity(field: str, value: str) -> None:
    arguments = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_operator_source_authority_evidence_package_preparation_package": service.SELECTED_PACKAGE,
        "operator_decision": service.OPERATOR_DECISION,
        "operator_confirmations": _confirmations(),
    }
    arguments[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1(**arguments)


@pytest.mark.parametrize("field", tuple(service.ATTESTATION_VALUE_FIELDS) + service.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_builder_rejects_changed_or_missing_confirmation(field: str) -> None:
    confirmations = _confirmations()
    confirmations[field] = False if field in service.ATTESTATION_BOOLEAN_FIELDS else "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_attestation_v1(
            operator_reference="TEST_OPERATOR",
            operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=service.REQUIRED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=confirmations,
        )


def test_approval_builds_offline_without_calling_upstream_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def prohibited(*args, **kwargs):
        raise AssertionError("upstream builder called")

    for name in dir(service.source):
        if name.startswith(("build_", "write_", "validate_")):
            monkeypatch.setattr(service.source, name, prohibited)
    approval = _build()
    assert approval["created_offline"] is True
    assert approval["approval_only"] is True
    assert approval["operator_source_authority_evidence_package_preparation_execution_performed"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("approval_status", service.APPROVAL_STATUS),
        ("approval_scope", service.APPROVAL_SCOPE),
        ("selected_operator_source_authority_evidence_package_preparation_package", service.SELECTED_PACKAGE),
        ("source_operator_review_commit", service.SOURCE_OPERATOR_REVIEW_COMMIT),
        ("source_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_package_options_review_digest", service.SOURCE_PACKAGE_OPTIONS_REVIEW_DIGEST),
        ("source_template_requirements_review_digest", service.SOURCE_TEMPLATE_REQUIREMENTS_REVIEW_DIGEST),
        ("source_missing_authority_coverage_review_digest", service.SOURCE_MISSING_AUTHORITY_COVERAGE_REVIEW_DIGEST),
        ("source_operator_review_manifest_digest", service.SOURCE_OPERATOR_REVIEW_MANIFEST_DIGEST),
        ("source_preparation_candidate_commit", service.SOURCE_PREPARATION_CANDIDATE_COMMIT),
        ("source_preparation_candidate_digest", service.SOURCE_PREPARATION_CANDIDATE_DIGEST),
        ("source_preparation_package_options_digest", service.SOURCE_PREPARATION_PACKAGE_OPTIONS_DIGEST),
        ("source_preparation_template_requirements_digest", service.SOURCE_PREPARATION_TEMPLATE_REQUIREMENTS_DIGEST),
        ("source_preparation_missing_authority_coverage_digest", service.SOURCE_PREPARATION_MISSING_AUTHORITY_COVERAGE_DIGEST),
        ("source_preparation_manifest_digest", service.SOURCE_PREPARATION_MANIFEST_DIGEST),
        ("source_failure_diagnosis_digest", service.SOURCE_FAILURE_DIAGNOSIS_DIGEST),
        ("source_blocked_reason", service.SOURCE_BLOCKED_REASON),
        ("source_blocked_manifest_digest", service.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("source_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("source_attestation_digest", service.SOURCE_ATTESTATION_DIGEST),
        ("operator_source_authority_evidence_item_count", 0),
        ("covered_missing_authority_item_count", 0),
        ("uncovered_missing_authority_item_count", 30),
        ("mapped_missing_authority_item_count", 30),
        ("missing_authority_items_status", "MISSING_NOT_ACQUIRED"),
        ("acquisition_scope_section_count", 4),
        ("acceptable_source_artifact_type_count", 13),
        ("operator_provided_evidence_requirement_count", 10),
        ("evidence_custody_and_digest_requirement_count", 6),
        ("candidate_results_review_requirement_count", 16),
        ("observable_failure_family_count", 4),
        ("total_observable_evidence_items", 188),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("package_option_count", 12),
        ("available_package_count", 7),
        ("blocked_package_count", 5),
        ("future_requirement_count", 62),
        ("future_plan_step_count", 15),
        ("planned_output_count", 28),
        ("non_goal_count", 71),
        ("risk_control_count", 104),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ),
)
def test_approval_binds_identity_source_chain_and_counts(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_approval_required_true_facts(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_approval_closed_boundaries(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_future_execution_template_permissions(field: str) -> None:
    approval = _build()
    assert approval[field] is True
    assert approval["future_execution_boundary"][field] is True


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_future_execution_prohibitions(field: str) -> None:
    approval = _build()
    assert approval[field] is False
    assert approval["future_execution_boundary"][field] is False


def test_reviewed_context_and_exact_collections_are_preserved() -> None:
    approval = _build()
    assert len(approval["priority_1_target_modules"]) == 5
    assert approval["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert approval["priority1_validation_summary"]["not_retry_evidence"] is True
    assert approval["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert approval["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert approval["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0
    assert len(approval["reviewed_observable_failure_families"]) == 4
    assert len(approval["reviewed_workstreams"]) == 4
    assert approval["acquisition_scope_sections_review"]["section_count"] == 4
    mapping = approval["missing_authority_to_source_evidence_mapping_review"]
    assert mapping["mapped_item_count"] == 30
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in mapping["items"])
    assert approval["acceptable_source_artifact_inventory_review"]["artifact_type_count"] == 13
    assert approval["operator_provided_evidence_requirements_review"]["requirement_count"] == 10
    assert approval["evidence_custody_and_digest_requirements_review"]["requirement_count"] == 6
    assert approval["candidate_results_review_requirements_review"]["requirement_count"] == 16


def test_package_requirements_plan_outputs_non_goals_and_gates() -> None:
    approval = _build()
    package = approval["approved_package"]
    assert package["selected"] is package["approved"] is package["authorized_for_future_execution"] is True
    assert package["executed"] is False
    assert len(approval["approved_future_requirements"]) == 62
    assert len({item["requirement_id"] for item in approval["approved_future_requirements"]}) == 62
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_requirements"])
    assert len(approval["approved_future_plan"]) == 15
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_plan"])
    assert len(approval["planned_outputs"]) == 28
    assert all(item["status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["planned_outputs"])
    assert len(approval["supporting_packages"]) == 6
    assert all(not item["selected"] and item["approval_status"] == "AVAILABLE_NOT_SELECTED" for item in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 5
    assert all(not item["approved"] and item["approval_status"] == "BLOCKED_NOT_APPROVED" for item in approval["blocked_packages"])
    assert len(approval["approved_non_goals"]) == 71
    assert approval["next_chain"]
    assert approval["next_gates"]
    assert len(approval["risk_controls"]) == 104


def test_approval_digest_is_deterministic_and_validator_accepts() -> None:
    first = _build()
    second = _build()
    assert first[service.APPROVAL_DIGEST_KEY] == second[service.APPROVAL_DIGEST_KEY]
    assert len(first[service.APPROVAL_DIGEST_KEY]) == 64
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(first)
    assert validation["failed_checks"] == 0
    assert validation["passed_checks"] == validation["total_checks"]


@pytest.mark.parametrize(
    "field",
    (
        "artifact_kind", "approval_status", "approval_scope",
        "selected_operator_source_authority_evidence_package_preparation_package",
        "source_operator_review_digest", "source_package_options_review_digest",
        "source_template_requirements_review_digest", "source_missing_authority_coverage_review_digest",
        "source_operator_review_manifest_digest", "source_preparation_candidate_digest",
        "source_preparation_package_options_digest", "source_preparation_template_requirements_digest",
        "source_preparation_missing_authority_coverage_digest", "source_preparation_manifest_digest",
        "source_failure_diagnosis_digest", "source_blocked_reason", "source_blocked_manifest_digest",
        "source_approval_digest", "source_attestation_digest", "priority_1_total_nodeids",
        "top_10_count_sum", "failed_or_errored_nodeids_count", "observable_failure_family_count",
        "total_observable_evidence_items", "risk_control_count", "runtime_use", "broker_execution",
    ),
)
def test_validator_rejects_changed_scalar(field: str) -> None:
    approval = _build()
    approval[field] = "WRONG"
    _reject(approval)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_removed(field: str) -> None:
    approval = _build()
    approval[field] = False
    _reject(approval)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_opened(field: str) -> None:
    approval = _build()
    approval[field] = True
    _reject(approval)


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_TRUE_FIELDS)
def test_validator_rejects_future_permission_removed(field: str) -> None:
    approval = _build()
    approval["future_execution_boundary"][field] = False
    _reject(approval)


@pytest.mark.parametrize("field", service.FUTURE_PERMISSION_FALSE_FIELDS)
def test_validator_rejects_future_prohibition_opened(field: str) -> None:
    approval = _build()
    approval["future_execution_boundary"][field] = True
    _reject(approval)


@pytest.mark.parametrize(
    "field",
    (
        "approved_future_requirements", "approved_future_plan", "planned_outputs",
        "supporting_packages", "blocked_packages", "approved_non_goals", "next_chain", "next_gates", "risk_controls",
        "reviewed_observable_failure_families", "reviewed_workstreams", "priority_1_target_modules",
        "acquisition_scope_sections_review", "missing_authority_to_source_evidence_mapping_review",
        "acceptable_source_artifact_inventory_review", "operator_provided_evidence_requirements_review",
        "evidence_custody_and_digest_requirements_review", "candidate_results_review_requirements_review",
    ),
)
def test_validator_rejects_missing_structured_evidence(field: str) -> None:
    approval = _build()
    approval[field] = []
    _reject(approval)


def test_validator_rejects_attestation_digest_mutation() -> None:
    approval = _build()
    approval["operator_attestation"][service.ATTESTATION_DIGEST_KEY] = "0" * 64
    _reject(approval)


def test_injected_source_review_is_accepted_without_mutation() -> None:
    review = service._committed_source_operator_review()
    review.update(service.SOURCE_REVIEW_DIGEST_FIELDS)
    original = deepcopy(review)
    approval = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
        source_operator_review=review, operator_attestation=_attestation()
    )
    assert review == original
    assert approval["source_operator_review_digest"] == service.SOURCE_OPERATOR_REVIEW_DIGEST


def test_injected_source_review_mutation_is_rejected() -> None:
    review = service._committed_source_operator_review()
    review.update(service.SOURCE_REVIEW_DIGEST_FIELDS)
    review["priority_1_target_modules"] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
            source_operator_review=review, operator_attestation=_attestation()
        )


def test_markdown_includes_every_required_section() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Source Authority Evidence Package Preparation Approval")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_writer_round_trips_status_document(tmp_path: Path) -> None:
    approval = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_APPROVAL_AFTER_CANDIDATE_OPERATOR_REVIEW_STATUS.md"
    assert path.is_file()
    assert approval[service.APPROVAL_DIGEST_KEY] in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directories(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationApprovalError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_approval_after_candidate_operator_review_v1(
            tmp_path / protected, operator_attestation=_attestation()
        )
