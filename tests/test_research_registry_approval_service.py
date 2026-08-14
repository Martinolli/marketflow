from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.services import research_registry_approval_service as approval


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-14T00:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_research_registry_candidate_review_digest": approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_research_registry_candidate_digest": approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "operator_confirms_canonical_dataset_freeze_digest": approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "operator_confirms_canonical_dataset_results_review_digest": approval.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_canonical_dataset_generation_digest": approval.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "operator_confirms_identity_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_target_universe": approval.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dataset_name": "expanded_universe_canonical_dataset_v1",
        "operator_confirms_dataset_scope_research_only": True,
        "operator_confirms_total_canonical_record_count": 11946,
        "operator_confirms_records_digest": approval.EXPECTED_RECORDS_DIGEST,
        "operator_confirms_meta_reduced_record_count_preserved": True,
        "operator_confirms_approval_scope_research_registry_only": True,
        "operator_confirms_research_registry_approved": True,
        "operator_confirms_registry_approval_created": True,
        "operator_confirms_ready_for_additional_predictive_evidence_chain_candidate": True,
        "operator_confirms_no_predictive_usefulness_acceptance": True,
        "operator_confirms_no_profitability_acceptance": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_runtime_activation": True,
        "operator_confirms_no_strategy_authorization": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_trade_recommendations": True,
        "operator_confirms_no_api_key_storage_or_printing": True,
        "operator_confirms_no_raw_payload_commit": True,
        "operator_decision": "APPROVE_RESEARCH_REGISTRY",
    }
    values.update(overrides)
    return approval.build_research_registry_approval_attestation_v1(**values)


@pytest.fixture(scope="module")
def artifact() -> dict:
    return approval.build_research_registry_approved_v1(operator_attestation=_attestation())


def test_attestation_builder_creates_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_RESEARCH_REGISTRY"
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_RESEARCH_REGISTRY_APPROVAL_V1
    )
    assert all(attestation[field] is True for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        approval.review_service.candidate_service.freeze,
        "build_canonical_dataset_frozen_v1",
        lambda *args, **kwargs: pytest.fail("freeze ceremony rebuild was called"),
    )
    built = approval.build_research_registry_approved_v1(
        operator_attestation=_attestation()
    )
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "RESEARCH_REGISTRY_APPROVED"),
        ("schema_version", "research_registry_approval_v1"),
        ("approval_status", "RESEARCH_REGISTRY_APPROVED"),
        ("approval_scope", "RESEARCH_REGISTRY_APPROVAL_ONLY"),
        ("research_registry_approved", True),
        ("registry_approval_created", True),
        ("ready_for_additional_predictive_evidence_chain_candidate", True),
        ("research_registry_candidate_review_package_digest", approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("research_registry_candidate_digest", approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST),
        ("canonical_dataset_freeze_digest", approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_results_review_package_digest", approval.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("canonical_dataset_generation_digest", approval.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("identity_authority_freeze_digest", approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", approval.TARGET_UNIVERSE),
        ("total_canonical_record_count", 11946),
        ("records_digest", approval.EXPECTED_RECORDS_DIGEST),
        ("per_ticker_record_counts", approval.EXPECTED_RECORD_COUNTS),
        ("approved_registry_metadata", approval.APPROVED_REGISTRY_METADATA),
        ("research_registry_approved_by_operator", True),
        ("registry_approval_scope", "RESEARCH_REGISTRY_APPROVAL_ONLY"),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("provider_requests_made_in_approval", False),
        ("live_provider_transport_enabled_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("canonical_dataset_regenerated_in_approval", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("registry_approval_creates_predictive_usefulness_acceptance", False),
        ("registry_approval_creates_profitability_acceptance", False),
        ("registry_approval_creates_runtime_authority", False),
        ("registry_approval_creates_strategy_authority", False),
        ("registry_approval_creates_paper_trading_authority", False),
        ("registry_approval_creates_broker_execution_authority", False),
        ("limitations", approval.LIMITATIONS),
        ("next_gates", approval.NEXT_GATES),
    ],
)
def test_approved_artifact_contract(artifact: dict, field: str, expected: object) -> None:
    assert artifact[field] == expected


def test_approved_registry_metadata_is_exact(artifact: dict) -> None:
    metadata = artifact["approved_registry_metadata"]
    assert metadata["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert metadata["dataset_scope"] == "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY"
    assert metadata["registry_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
    assert metadata["registry_entry_status"] == "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
    assert "registry_candidate_label" not in metadata


def test_meta_and_non_meta_counts_are_preserved(artifact: dict) -> None:
    assert artifact["per_ticker_record_counts"]["META"] == 913
    assert all(
        count == 1003
        for ticker, count in artifact["per_ticker_record_counts"].items()
        if ticker != "META"
    )


def test_per_ticker_approval_entries_and_digests(artifact: dict) -> None:
    entries = artifact["per_ticker_research_registry_approvals"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    for row in entries:
        assert row["research_registry_approval_status"] == "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
        assert row["source_research_registry_candidate_review_digest"] == approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        assert row["source_research_registry_candidate_digest"] == approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST
        assert len(row["per_ticker_research_registry_approval_digest"]) == 64
        assert row["runtime_use"] == "NOT_AUTHORIZED"
        assert row["broker_execution"] == "NOT_AUTHORIZED"
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


def test_checklist_contains_all_required_ids_and_passes(artifact: dict) -> None:
    assert [row["check_id"] for row in artifact["approval_checklist"]] == approval.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" and row["severity"] == "BLOCKER" for row in artifact["approval_checklist"])


def test_approval_summary_counts_and_boundaries_are_correct(artifact: dict) -> None:
    summary = artifact["approval_summary"]
    assert summary["total_checks"] == len(approval.REQUIRED_CHECK_IDS) == 52
    assert summary["passed_checks"] == 52
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["research_registry_approved_by_operator"] is True
    assert summary["research_registry_approved"] is True
    assert summary["registry_approval_created"] is True
    assert summary["ready_for_additional_predictive_evidence_chain_candidate"] is True
    assert summary["additional_predictive_evidence_execution_authorized"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("operator_attestation_phrase", "WRONG"),
        ("operator_decision", "REJECT"),
        ("operator_confirms_research_registry_candidate_review_digest", "0" * 64),
        ("operator_confirms_research_registry_candidate_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_freeze_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_results_review_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_generation_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_dataset_name", "wrong"),
        ("operator_confirms_dataset_scope_research_only", False),
        ("operator_confirms_total_canonical_record_count", 11945),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_meta_reduced_record_count_preserved", False),
        ("operator_confirms_approval_scope_research_registry_only", False),
        ("operator_confirms_research_registry_approved", False),
        ("operator_confirms_registry_approval_created", False),
        ("operator_confirms_ready_for_additional_predictive_evidence_chain_candidate", False),
        ("operator_confirms_no_predictive_usefulness_acceptance", False),
        ("operator_confirms_no_profitability_acceptance", False),
        ("operator_confirms_no_runtime_migration_approval", False),
        ("operator_confirms_no_runtime_activation", False),
        ("operator_confirms_no_strategy_authorization", False),
        ("operator_confirms_no_paper_trading", False),
        ("operator_confirms_no_broker_execution", False),
        ("operator_confirms_no_trade_recommendations", False),
        ("operator_confirms_no_api_key_storage_or_printing", False),
        ("operator_confirms_no_raw_payload_commit", False),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_builder_rejects_invalid_or_partial_attestation(field: str, invalid: object) -> None:
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.build_research_registry_approved_v1(
            operator_attestation=_attestation(**{field: invalid})
        )


def test_builder_rejects_missing_operator_attestation() -> None:
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.build_research_registry_approved_v1(operator_attestation={})


def test_builder_accepts_explicit_valid_review_package() -> None:
    source = approval.review_service.build_research_registry_candidate_review_package_v1()
    artifact = approval.build_research_registry_approved_v1(
        research_registry_candidate_review_package=source,
        operator_attestation=_attestation(),
    )
    assert artifact["research_registry_approved"] is True


def test_builder_rejects_changed_source_review_digest() -> None:
    source = approval.review_service.build_research_registry_candidate_review_package_v1()
    source["research_registry_candidate_review_package_digest"] = "0" * 64
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.build_research_registry_approved_v1(
            research_registry_candidate_review_package=source,
            operator_attestation=_attestation(),
        )


def test_validator_accepts_valid_approval(artifact: dict) -> None:
    result = approval.validate_research_registry_approved_v1(artifact)
    assert result["status"] == "RESEARCH_REGISTRY_APPROVED"
    assert result["blocker_count"] == 0
    assert result["research_registry_approved"] is True
    assert result["registry_approval_created"] is True
    assert result["ready_for_additional_predictive_evidence_chain_candidate"] is True


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("research_registry_approved", False),
        ("registry_approval_created", False),
        ("ready_for_additional_predictive_evidence_chain_candidate", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("canonical_dataset_regenerated_in_approval", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("registry_approval_creates_predictive_usefulness_acceptance", True),
        ("registry_approval_creates_profitability_acceptance", True),
        ("registry_approval_creates_runtime_authority", True),
        ("research_registry_approval_digest", None),
    ],
)
def test_validator_rejects_invalid_artifact_fields(
    artifact: dict,
    field: str,
    invalid: object,
) -> None:
    changed = deepcopy(artifact)
    changed[field] = invalid
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.validate_research_registry_approved_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(
    artifact: dict,
    ticker: str,
    count: int,
) -> None:
    changed = deepcopy(artifact)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.validate_research_registry_approved_v1(changed)


def test_validator_rejects_missing_per_ticker_approval_digest(artifact: dict) -> None:
    changed = deepcopy(artifact)
    changed["per_ticker_research_registry_approvals"][0].pop(
        "per_ticker_research_registry_approval_digest"
    )
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.validate_research_registry_approved_v1(changed)


def test_validator_rejects_wrong_embedded_attestation(artifact: dict) -> None:
    changed = deepcopy(artifact)
    changed["operator_attestation"]["operator_decision"] = "REJECT"
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.validate_research_registry_approved_v1(changed)


def test_approval_digest_is_deterministic(artifact: dict) -> None:
    repeated = approval.build_research_registry_approved_v1(
        operator_attestation=_attestation()
    )
    assert repeated["research_registry_approval_digest"] == artifact[
        "research_registry_approval_digest"
    ]
    assert artifact["research_registry_approval_digest"] == (
        approval.research_registry_approval_digest_v1(artifact)
    )


def test_per_ticker_approval_digests_are_deterministic(artifact: dict) -> None:
    repeated = approval.build_research_registry_approved_v1(
        operator_attestation=_attestation()
    )
    assert [row["per_ticker_research_registry_approval_digest"] for row in repeated["per_ticker_research_registry_approvals"]] == [
        row["per_ticker_research_registry_approval_digest"]
        for row in artifact["per_ticker_research_registry_approvals"]
    ]


def test_markdown_includes_required_sections(artifact: dict) -> None:
    markdown = approval.build_research_registry_approved_markdown_v1(artifact)
    required = [
        "Title",
        "Approved Research Registry Entry",
        "Operator Attestation",
        "Source Research Registry Candidate Review",
        "Source Frozen Canonical Dataset",
        "Target Universe",
        "Approved Registry Metadata",
        "Per-Ticker Registry Approval Entries",
        "Records Digest",
        "META Reduced Record Count Preservation",
        "Approval Scope",
        "Predictive/Profitability Boundary",
        "Runtime Boundary",
        "Approval Checklist Summary",
        "Remaining Required Tasks",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_writer_writes_once_without_overwrite(artifact: dict, tmp_path: Path) -> None:
    result = approval.write_research_registry_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )
    written = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert written["research_registry_approval_digest"] == artifact[
        "research_registry_approval_digest"
    ]
    with pytest.raises(approval.ResearchRegistryApprovalError):
        approval.write_research_registry_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_RESEARCH_REGISTRY_APPROVED == (
        approval.ARTIFACT_KIND_RESEARCH_REGISTRY_APPROVED
    )
    assert services.RESEARCH_REGISTRY_APPROVED == approval.RESEARCH_REGISTRY_APPROVED
    assert services.RESEARCH_REGISTRY_APPROVAL_ONLY == approval.RESEARCH_REGISTRY_APPROVAL_ONLY
    assert services.REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_RESEARCH_REGISTRY_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_research_registry_approval_attestation_v1 is (
        approval.build_research_registry_approval_attestation_v1
    )
    assert services.build_research_registry_approved_v1 is (
        approval.build_research_registry_approved_v1
    )
    assert services.validate_research_registry_approved_v1 is (
        approval.validate_research_registry_approved_v1
    )
    assert services.write_research_registry_approved_v1 is (
        approval.write_research_registry_approved_v1
    )
    assert services.build_research_registry_approved_markdown_v1 is (
        approval.build_research_registry_approved_markdown_v1
    )
