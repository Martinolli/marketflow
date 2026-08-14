from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import canonical_dataset_generation_approval_service as approval


def _attestation() -> dict:
    return approval.build_canonical_dataset_generation_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-14T15:00:00Z",
        operator_attestation_phrase=approval.REQUIRED_CANONICAL_DATASET_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_canonical_dataset_chain_candidate_review_digest=approval.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        operator_confirms_canonical_dataset_chain_candidate_digest=approval.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        operator_confirms_acquisition_generation_freeze_digest=approval.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        operator_confirms_acquisition_generation_approval_digest=approval.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        operator_confirms_acquisition_evidence_results_review_digest=approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_identity_freeze_digest=approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        operator_confirms_target_universe=list(approval.TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_source_profile=True,
        operator_confirms_historical_bar_evidence_collected_count=12,
        operator_confirms_meta_reduced_bar_count_preserved=True,
        operator_confirms_approval_scope_canonical_dataset_generation_only=True,
        operator_confirms_dataset_generation_authorized=True,
        operator_confirms_canonical_dataset_authorized=True,
        operator_confirms_ready_for_canonical_dataset_generation_execution=True,
        operator_confirms_no_canonical_dataset_candidate_created=True,
        operator_confirms_no_canonical_dataset_generation_executed=True,
        operator_confirms_no_canonical_dataset_freeze=True,
        operator_confirms_no_registry_approval=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_runtime_activation=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval._source_review(None)


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return approval.build_canonical_dataset_generation_approved_v1(
        canonical_dataset_chain_review_package=source_review,
        operator_attestation=_attestation(),
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_CANONICAL_DATASET_GENERATION
    assert attestation["operator_attestation_version"] == approval.OPERATOR_ATTESTATION_VERSION_CANONICAL_DATASET_GENERATION_APPROVAL_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        approval.candidate_service.freeze.approval.evidence_review.execution,
        "execute_acquisition_provider_evidence_v1",
        lambda *args, **kwargs: pytest.fail("provider evidence execution was called"),
    )
    artifact = approval.build_canonical_dataset_generation_approved_v1(operator_attestation=_attestation())
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["dataset_generation_performed_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", approval.ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_APPROVED),
        ("approval_status", approval.CANONICAL_DATASET_GENERATION_APPROVED),
        ("approval_scope", approval.CANONICAL_DATASET_GENERATION_APPROVAL_ONLY),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_generation_approved", True),
        ("ready_for_canonical_dataset_generation_execution", True),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_generation_executed", False),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("historical_bar_evidence_collected_count", 12),
        ("source_profile_confirmed", True),
        ("meta_reduced_bar_count_preserved", True),
        ("target_universe_count", 12),
        ("target_universe", approval.TARGET_UNIVERSE),
        ("canonical_dataset_chain_candidate_review_package_digest", approval.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("canonical_dataset_chain_candidate_digest", approval.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST),
        ("acquisition_generation_freeze_digest", approval.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST),
        ("acquisition_generation_approval_digest", approval.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST),
        ("acquisition_evidence_results_review_package_digest", approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("corporate_action_authority_approval_digest", approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("provider_requests_made_in_approval", False),
        ("live_provider_transport_enabled_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", approval.NOT_ACCEPTED),
        ("profitability", approval.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", approval.NOT_AUTHORIZED),
        ("strategy_use", approval.NOT_AUTHORIZED),
        ("paper_trading", approval.NOT_AUTHORIZED),
        ("broker_execution", approval.NOT_AUTHORIZED),
    ],
)
def test_approved_artifact_fields(approved: dict, field: str, expected: object):
    assert approved[field] == expected


def test_per_ticker_approvals_and_meta_are_preserved(approved: dict):
    entries = approved["per_ticker_canonical_dataset_generation_approvals"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    assert all(row["per_ticker_canonical_dataset_generation_approval_digest"] for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_bar_count"] == 913
    assert meta["meta_reduced_bar_count_flag"] is True
    assert all(row["historical_bar_count"] == 1003 for row in entries if row["ticker"] != "META")


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_decision", "REJECT"),
        ("operator_confirms_canonical_dataset_chain_candidate_review_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_chain_candidate_digest", "0" * 64),
        ("operator_confirms_acquisition_generation_freeze_digest", "0" * 64),
        ("operator_confirms_acquisition_generation_approval_digest", "0" * 64),
        ("operator_confirms_acquisition_evidence_results_review_digest", "0" * 64),
        ("operator_confirms_corporate_action_authority_approval_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_historical_bar_evidence_collected_count", 11),
    ]
    + [(field, False) for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS],
)
def test_invalid_operator_attestation_is_rejected(source_review: dict, field: str, bad_value: object):
    attestation = _attestation()
    attestation[field] = bad_value
    with pytest.raises(approval.CanonicalDatasetGenerationApprovalError):
        approval.build_canonical_dataset_generation_approved_v1(
            canonical_dataset_chain_review_package=source_review,
            operator_attestation=attestation,
        )


def test_validator_accepts_valid_approval(approved: dict):
    result = approval.validate_canonical_dataset_generation_approved_v1(approved)
    assert result["status"] == approval.CANONICAL_DATASET_GENERATION_APPROVED
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_generation_approved", False),
        ("ready_for_canonical_dataset_generation_execution", False),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_generation_executed", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("historical_bar_evidence_collected_count", 11),
        ("meta_reduced_bar_count_preserved", False),
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
        ("approval_creates_canonical_dataset_artifact", True),
        ("approval_creates_registry_approval", True),
        ("approval_creates_runtime_authority", True),
        ("canonical_dataset_generation_approval_digest", None),
    ],
)
def test_validator_rejects_invalid_approval(approved: dict, field: str, bad_value: object):
    invalid = deepcopy(approved)
    invalid[field] = bad_value
    with pytest.raises(approval.CanonicalDatasetGenerationApprovalError):
        approval.validate_canonical_dataset_generation_approved_v1(invalid)


def test_validator_rejects_wrong_attestation(approved: dict):
    invalid = deepcopy(approved)
    invalid["operator_attestation"]["operator_attestation_phrase"] = "wrong"
    with pytest.raises(approval.CanonicalDatasetGenerationApprovalError):
        approval.validate_canonical_dataset_generation_approved_v1(invalid)


def test_approval_and_per_ticker_digests_are_deterministic(source_review: dict):
    first = approval.build_canonical_dataset_generation_approved_v1(
        canonical_dataset_chain_review_package=source_review, operator_attestation=_attestation()
    )
    second = approval.build_canonical_dataset_generation_approved_v1(
        canonical_dataset_chain_review_package=source_review, operator_attestation=_attestation()
    )
    assert first["canonical_dataset_generation_approval_digest"] == second["canonical_dataset_generation_approval_digest"]
    assert [row["per_ticker_canonical_dataset_generation_approval_digest"] for row in first["per_ticker_canonical_dataset_generation_approvals"]] == [
        row["per_ticker_canonical_dataset_generation_approval_digest"] for row in second["per_ticker_canonical_dataset_generation_approvals"]
    ]


def test_markdown_includes_required_sections(approved: dict):
    markdown = approval.build_canonical_dataset_generation_approved_markdown_v1(approved)
    for section in (
        "Approved Canonical Dataset Generation", "Operator Attestation",
        "Source Canonical Dataset Chain Candidate Review", "Source Acquisition Generation Freeze",
        "Target Universe", "Approved Per-Ticker Canonical Dataset Generation Summary", "Source Profile",
        "META Reduced Bar Count Preservation", "Approval Scope", "Dataset Generation Boundary",
        "Canonical Dataset Creation Boundary", "Canonical Dataset Freeze Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Approval Checklist Summary",
        "Remaining Required Tasks", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(tmp_path, source_review: dict):
    result = approval.write_canonical_dataset_generation_approved_v1(
        tmp_path, canonical_dataset_chain_review_package=source_review, operator_attestation=_attestation()
    )
    payload = json.loads((tmp_path / "canonical_dataset_generation_approved_v1.json").read_text(encoding="utf-8"))
    assert payload["canonical_dataset_generation_approval_digest"] == result["canonical_dataset_generation_approval_digest"]
    with pytest.raises(approval.CanonicalDatasetGenerationApprovalError):
        approval.write_canonical_dataset_generation_approved_v1(
            tmp_path, canonical_dataset_chain_review_package=source_review, operator_attestation=_attestation()
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_APPROVED == approval.ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_APPROVED
    assert services.build_canonical_dataset_generation_approved_v1 is approval.build_canonical_dataset_generation_approved_v1
    assert services.validate_canonical_dataset_generation_approved_v1 is approval.validate_canonical_dataset_generation_approved_v1
