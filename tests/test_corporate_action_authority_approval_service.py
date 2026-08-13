from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import corporate_action_authority_approval_service as approval


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-13T00:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_combined_readiness_review_digest": approval.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_dividend_authority_freeze_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_target_universe": approval.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        **{field: True for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS},
    }
    values.update(overrides)
    return approval.build_corporate_action_authority_approval_attestation_v1(**values)


def _approved() -> dict[str, Any]:
    return approval.build_corporate_action_authority_approved_v1(
        operator_attestation=_attestation()
    )


def _redigest(artifact: dict[str, Any]) -> None:
    artifact["corporate_action_authority_approval_digest"] = (
        approval.corporate_action_authority_approval_digest_v1(artifact)
    )


def test_operator_attestation_builder_creates_all_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY
    assert attestation["operator_attestation_phrase"] == approval.REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE
    assert attestation["operator_confirms_target_universe"] == approval.TARGET_UNIVERSE
    assert attestation["operator_confirms_target_count"] == 12
    assert all(attestation[field] is True for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider call")

    monkeypatch.setattr(
        approval.readiness.dividend_freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        provider_call,
    )
    monkeypatch.setattr(
        approval.readiness.split_freeze.review.execution,
        "execute_split_provider_evidence_v1",
        provider_call,
    )
    artifact = _approved()
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False
    assert artifact["split_provider_evidence_rerun_performed"] is False
    assert artifact["dividend_provider_evidence_rerun_performed"] is False


def test_artifact_identity_authority_and_universe_are_exact():
    artifact = _approved()
    assert artifact["artifact_kind"] == approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_APPROVED
    assert artifact["approval_status"] == approval.CORPORATE_ACTION_AUTHORITY_APPROVED
    assert artifact["authority_scope"] == approval.CORPORATE_ACTION_AUTHORITY_ONLY
    assert artifact["corporate_action_authority_created"] is True
    assert artifact["corporate_action_authority_approved"] is True
    assert artifact["corporate_action_authority_frozen"] is False
    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == approval.TARGET_UNIVERSE


def test_all_required_source_digests_are_bound():
    artifact = _approved()
    expected = {
        "combined_split_dividend_corporate_action_readiness_review_package_digest": approval.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_event_authority_freeze_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_event_evidence_results_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": approval.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }
    assert {field: artifact[field] for field in expected} == expected


def test_split_dividend_authorities_remain_created_and_frozen():
    artifact = _approved()
    assert artifact["split_event_authority_created"] is True
    assert artifact["split_event_authority_frozen"] is True
    assert artifact["dividend_event_authority_created"] is True
    assert artifact["dividend_event_authority_frozen"] is True


def test_per_ticker_authority_entries_preserve_classification_and_digests():
    artifact = _approved()
    source = approval.readiness.build_combined_split_dividend_corporate_action_readiness_review_package_v1()
    source_by_ticker = {row["ticker"]: row for row in source["per_ticker_combined_readiness"]}
    entries = artifact["per_ticker_corporate_action_authority"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    for row in entries:
        source_row = source_by_ticker[row["ticker"]]
        assert row["corporate_action_authority_status"] == "APPROVED"
        assert row["corporate_action_authority_scope"] == approval.CORPORATE_ACTION_AUTHORITY_ONLY
        assert row["split_event_authority_classification"] == source_row["split_event_authority_classification"]
        assert row["dividend_event_authority_classification"] == source_row["dividend_event_authority_classification"]
        assert row["per_ticker_corporate_action_authority_approval_digest"] == approval.per_ticker_corporate_action_authority_approval_digest_v1(row)


def test_readiness_conclusion_limitations_next_gates_and_summary_are_exact():
    artifact = _approved()
    assert artifact["ready_for_acquisition_generation_chain_candidate"] is True
    assert artifact["combined_split_dividend_authorities_available"] is True
    assert artifact["corporate_action_authority_approved_by_operator"] is True
    assert artifact["limitations"] == approval.LIMITATIONS
    assert artifact["next_gates"] == approval.NEXT_GATES
    assert [row["check_id"] for row in artifact["approval_checklist"]] == approval.REQUIRED_APPROVAL_CHECK_IDS
    assert all(row["status"] == approval.PASS for row in artifact["approval_checklist"])
    assert artifact["approval_summary"]["total_checks"] == 57
    assert artifact["approval_summary"]["blocker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
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
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "split_provider_evidence_rerun_performed",
        "dividend_provider_evidence_rerun_performed",
        "corporate_action_authority_creates_acquisition_authority",
        "corporate_action_authority_creates_dataset_generation_authority",
        "corporate_action_authority_creates_predictive_evidence_authority",
        "corporate_action_authority_creates_runtime_authority",
    ],
)
def test_forbidden_boolean_authorization_fields_are_rejected(field: str):
    artifact = _approved()
    artifact[field] = True
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.validate_corporate_action_authority_approved_v1(artifact)


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
def test_accepted_research_or_authorized_runtime_values_are_rejected(field: str, value: str):
    artifact = _approved()
    artifact[field] = value
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.validate_corporate_action_authority_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("authority_scope", "WRONG"),
        ("corporate_action_authority_created", False),
        ("corporate_action_authority_approved", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("ready_for_acquisition_generation_chain_candidate", False),
    ],
)
def test_validator_rejects_invalid_core_contract(field: str, value: Any):
    artifact = _approved()
    artifact[field] = value
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.validate_corporate_action_authority_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "REJECT"),
        ("operator_attestation_phrase", "wrong"),
        ("operator_confirms_combined_readiness_review_digest", "0" * 64),
        ("operator_confirms_split_authority_freeze_digest", "0" * 64),
        ("operator_confirms_dividend_authority_freeze_digest", "0" * 64),
        ("operator_confirms_corporate_action_plan_approval_digest", "0" * 64),
        ("operator_confirms_registry_inventory_approval_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_authority_scope_corporate_action_only", False),
        ("operator_confirms_ready_for_acquisition_generation_chain_candidate", False),
        ("operator_confirms_split_authority_frozen", False),
        ("operator_confirms_dividend_authority_frozen", False),
        ("operator_confirms_no_acquisition_authority", False),
        ("operator_confirms_no_dataset_generation_authorization", False),
        ("operator_confirms_no_runtime_activation", False),
        ("operator_confirms_no_paper_trading", False),
        ("operator_confirms_no_broker_execution", False),
        ("operator_confirms_no_api_key_storage_or_printing", False),
        ("operator_confirms_no_raw_payload_commit", False),
    ],
)
def test_wrong_or_missing_operator_attestation_values_are_rejected(field: str, value: Any):
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.build_corporate_action_authority_approved_v1(
            operator_attestation=_attestation(**{field: value})
        )


@pytest.mark.parametrize("field", approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS)
def test_every_operator_boundary_confirmation_is_required(field: str):
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.build_corporate_action_authority_approved_v1(
            operator_attestation=_attestation(**{field: False})
        )


def test_validator_accepts_valid_approval_and_rejects_missing_digest():
    artifact = _approved()
    validation = approval.validate_corporate_action_authority_approved_v1(artifact)
    assert validation["status"] == "CORPORATE_ACTION_AUTHORITY_APPROVED_VALID"
    assert validation["failed_checks"] == 0
    artifact.pop("corporate_action_authority_approval_digest")
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.validate_corporate_action_authority_approved_v1(artifact)


def test_validator_rejects_missing_or_changed_per_ticker_digest():
    artifact = _approved()
    artifact["per_ticker_corporate_action_authority"][0]["per_ticker_corporate_action_authority_approval_digest"] = "0" * 64
    _redigest(artifact)
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.validate_corporate_action_authority_approved_v1(artifact)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _approved()
    second = _approved()
    assert first == second
    assert first["corporate_action_authority_approval_digest"] == second["corporate_action_authority_approval_digest"]
    assert [row["per_ticker_corporate_action_authority_approval_digest"] for row in first["per_ticker_corporate_action_authority"]] == [row["per_ticker_corporate_action_authority_approval_digest"] for row in second["per_ticker_corporate_action_authority"]]


def test_markdown_contains_all_required_sections():
    markdown = approval.build_corporate_action_authority_approved_markdown_v1(_approved())
    required = [
        "Title", "Approved Corporate-Action Authority", "Operator Attestation",
        "Source Combined Readiness Review", "Source Split Authority Freeze",
        "Source Dividend Authority Freeze", "Target Universe",
        "Approved Per-Ticker Corporate-Action Authority Summary", "Authority Scope",
        "Acquisition Boundary", "Dataset Boundary", "Predictive/Profitability Boundary",
        "Runtime Boundary", "Approval Checklist Summary", "Remaining Required Tasks",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)


def test_writer_creates_valid_json_and_markdown_without_overwrite(tmp_path: Path):
    result = approval.write_corporate_action_authority_approved_v1(
        tmp_path, operator_attestation=_attestation()
    )
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json.loads(json_path.read_text(encoding="utf-8")) == result["artifact"]
    assert "## Guardrails" in markdown_path.read_text(encoding="utf-8")
    with pytest.raises(approval.CorporateActionAuthorityApprovalError):
        approval.write_corporate_action_authority_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )


def test_service_exports_are_available():
    expected = {
        "ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_APPROVED",
        "CORPORATE_ACTION_AUTHORITY_APPROVED",
        "CORPORATE_ACTION_AUTHORITY_ONLY",
        "REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE",
        "build_corporate_action_authority_approval_attestation_v1",
        "build_corporate_action_authority_approved_markdown_v1",
        "build_corporate_action_authority_approved_v1",
        "corporate_action_authority_approval_digest_v1",
        "per_ticker_corporate_action_authority_approval_digest_v1",
        "validate_corporate_action_authority_approved_v1",
        "write_corporate_action_authority_approved_v1",
    }
    assert all(name in services.__all__ for name in expected)
    assert all(hasattr(services, name) for name in expected)
