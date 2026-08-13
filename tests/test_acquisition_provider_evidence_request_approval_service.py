from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import acquisition_provider_evidence_request_approval_service as approval


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-13T00:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_acquisition_chain_candidate_review_digest": approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_acquisition_chain_candidate_digest": approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "operator_confirms_corporate_action_authority_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "operator_confirms_combined_readiness_review_digest": approval.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_dividend_authority_freeze_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_identity_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_target_universe": approval.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        **{field: True for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS},
    }
    values.update(overrides)
    return approval.build_acquisition_provider_evidence_request_approval_attestation_v1(
        **values
    )


def _approved() -> dict[str, Any]:
    return approval.build_acquisition_provider_evidence_request_approved_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_ACQUISITION_PROVIDER_EVIDENCE_REQUEST
    assert attestation["operator_attestation_phrase"] == approval.REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_target_universe"] == approval.TARGET_UNIVERSE
    assert all(attestation[field] is True for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approval_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider call")

    monkeypatch.setattr(
        approval.chain_review.candidate_service.authority.readiness.dividend_freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        provider_call,
    )
    monkeypatch.setattr(
        approval.chain_review.candidate_service.authority.readiness.split_freeze.review.execution,
        "execute_split_provider_evidence_v1",
        provider_call,
    )
    artifact = _approved()
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False
    assert artifact["market_data_acquisition_performed_in_approval"] is False


def test_identity_scope_authorization_and_execution_states_are_exact():
    artifact = _approved()
    assert artifact["artifact_kind"] == approval.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED
    assert artifact["approval_status"] == approval.ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED
    assert artifact["approval_scope"] == approval.READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY
    assert artifact["acquisition_provider_request_authorized"] is True
    assert artifact["ready_for_acquisition_provider_evidence_execution"] is True
    assert artifact["acquisition_provider_evidence_executed"] is False
    assert artifact["acquisition_provider_evidence_results_created"] is False
    assert artifact["acquisition_provider_evidence_execution_status"] == approval.NOT_EXECUTED
    assert artifact["acquisition_provider_evidence_results_status"] == approval.NOT_CREATED


def test_source_digests_and_target_universe_are_bound():
    artifact = _approved()
    expected = {
        "acquisition_generation_chain_candidate_review_package_digest": approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "acquisition_generation_chain_candidate_digest": approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": approval.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    assert {field: artifact[field] for field in expected} == expected
    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == approval.TARGET_UNIVERSE


def test_request_objective_scope_policy_and_outputs_are_exact():
    artifact = _approved()
    assert artifact["acquisition_provider_evidence_request_objective"] == approval.ACQUISITION_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE
    assert artifact["acquisition_provider_evidence_request_scope"] == approval.ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE
    assert artifact["acquisition_provider_evidence_authority_scope"] == approval.ACQUISITION_PROVIDER_EVIDENCE_AUTHORITY_SCOPE
    assert artifact["read_only_request_policy"] == approval.READ_ONLY_REQUEST_POLICY
    assert [row["output_name"] for row in artifact["planned_outputs"]] == approval.PLANNED_ACQUISITION_EVIDENCE_OUTPUT_NAMES
    assert all(row["generation_status"] == approval.PLANNED_NOT_GENERATED for row in artifact["planned_outputs"])
    assert all(row["actionability"] == approval.RESEARCH_ONLY_NON_ACTIONABLE for row in artifact["planned_outputs"])


def test_per_ticker_request_approvals_are_authorized_not_executed_and_digest_bound():
    entries = _approved()["per_ticker_acquisition_provider_evidence_request_approvals"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    for row in entries:
        assert row["acquisition_provider_request_status"] == approval.AUTHORIZED_NOT_EXECUTED
        assert row["acquisition_provider_evidence_execution_status"] == approval.NOT_EXECUTED
        assert row["acquisition_provider_evidence_results_status"] == approval.NOT_CREATED
        assert row["acquisition_generation_authorized"] is False
        assert row["acquisition_generation_executed"] is False
        assert row["per_ticker_acquisition_provider_evidence_request_approval_digest"] == approval.per_ticker_acquisition_provider_evidence_request_approval_digest_v1(row)


def test_checklist_and_summary_are_complete_and_passing():
    artifact = _approved()
    checklist = artifact["approval_checklist"]
    summary = artifact["approval_summary"]
    assert [row["check_id"] for row in checklist] == approval.REQUIRED_APPROVAL_CHECK_IDS
    assert all(row["status"] == approval.PASS for row in checklist)
    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS) == 53
    assert summary["passed_checks"] == 53
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["acquisition_provider_request_authorized_by_operator"] is True
    assert summary["ready_for_acquisition_provider_evidence_execution"] is True
    assert summary["acquisition_authorized"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "acquisition_provider_evidence_executed",
        "acquisition_provider_evidence_results_created",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
        "acquisition_generation_results_created",
        "acquisition_generation_frozen",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_candidate_created",
        "canonical_dataset_frozen",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_fields(field: str):
    artifact = _approved()
    artifact[field] = True
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_acceptance_or_runtime_authorization(field: str, value: str):
    artifact = _approved()
    artifact[field] = value
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("acquisition_provider_request_authorized", False),
        ("ready_for_acquisition_provider_evidence_execution", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
    ],
)
def test_validator_rejects_invalid_core_contract(field: str, value: Any):
    artifact = _approved()
    artifact[field] = value
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "REJECT"),
        ("operator_attestation_phrase", "wrong"),
        ("operator_confirms_acquisition_chain_candidate_review_digest", "0" * 64),
        ("operator_confirms_acquisition_chain_candidate_digest", "0" * 64),
        ("operator_confirms_corporate_action_authority_approval_digest", "0" * 64),
        ("operator_confirms_combined_readiness_review_digest", "0" * 64),
        ("operator_confirms_split_authority_freeze_digest", "0" * 64),
        ("operator_confirms_dividend_authority_freeze_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
    ],
)
def test_wrong_attestation_identity_or_source_values_are_rejected(field: str, value: Any):
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.build_acquisition_provider_evidence_request_approved_v1(
            operator_attestation=_attestation(**{field: value})
        )


@pytest.mark.parametrize("field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)
def test_every_operator_boundary_confirmation_is_required(field: str):
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.build_acquisition_provider_evidence_request_approved_v1(
            operator_attestation=_attestation(**{field: False})
        )


def test_validator_accepts_valid_artifact_and_rejects_missing_digest():
    artifact = _approved()
    validation = approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)
    assert validation["status"] == "ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID"
    assert validation["blocker_count"] == 0
    artifact.pop("acquisition_provider_evidence_request_approval_digest")
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)


def test_validator_rejects_missing_per_ticker_approval_digest():
    artifact = _approved()
    artifact["per_ticker_acquisition_provider_evidence_request_approvals"][0].pop(
        "per_ticker_acquisition_provider_evidence_request_approval_digest"
    )
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.validate_acquisition_provider_evidence_request_approved_v1(artifact)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _approved()
    second = _approved()
    assert first == second
    assert first["acquisition_provider_evidence_request_approval_digest"] == second["acquisition_provider_evidence_request_approval_digest"]
    assert [row["per_ticker_acquisition_provider_evidence_request_approval_digest"] for row in first["per_ticker_acquisition_provider_evidence_request_approvals"]] == [row["per_ticker_acquisition_provider_evidence_request_approval_digest"] for row in second["per_ticker_acquisition_provider_evidence_request_approvals"]]


def test_markdown_contains_all_required_sections():
    markdown = approval.build_acquisition_provider_evidence_request_approved_markdown_v1(_approved())
    sections = [
        "Title", "Approved Acquisition Provider Evidence Request", "Operator Attestation",
        "Source Acquisition Chain Candidate Review", "Source Corporate-Action Authority Approval",
        "Target Universe", "Approval Scope", "Read-Only Provider Request Boundary",
        "Acquisition Execution Boundary", "Dataset Boundary", "Canonical Dataset Boundary",
        "Registry Boundary", "Predictive/Profitability Boundary", "Runtime Boundary",
        "Approval Checklist Summary", "Remaining Required Tasks", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_creates_valid_files_without_overwrite(tmp_path: Path):
    result = approval.write_acquisition_provider_evidence_request_approved_v1(
        tmp_path, operator_attestation=_attestation()
    )
    assert json.loads(Path(result["json_path"]).read_text(encoding="utf-8")) == result["artifact"]
    assert "## Guardrails" in Path(result["markdown_path"]).read_text(encoding="utf-8")
    with pytest.raises(approval.AcquisitionProviderEvidenceRequestApprovalError):
        approval.write_acquisition_provider_evidence_request_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )


def test_public_exports_are_available():
    expected = {
        "ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED",
        "ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVED",
        "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY",
        "REQUIRED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE",
        "build_acquisition_provider_evidence_request_approval_attestation_v1",
        "build_acquisition_provider_evidence_request_approved_markdown_v1",
        "build_acquisition_provider_evidence_request_approved_v1",
        "validate_acquisition_provider_evidence_request_approved_v1",
        "write_acquisition_provider_evidence_request_approved_v1",
        "acquisition_provider_evidence_request_approval_digest_v1",
        "per_ticker_acquisition_provider_evidence_request_approval_digest_v1",
    }
    assert all(name in services.__all__ for name in expected)
    assert all(hasattr(services, name) for name in expected)
