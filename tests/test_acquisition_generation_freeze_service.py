from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import acquisition_generation_freeze_service as freeze


def _attestation() -> dict:
    return freeze.build_acquisition_generation_freeze_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-14T13:00:00Z",
        operator_attestation_phrase=freeze.REQUIRED_ACQUISITION_GENERATION_FREEZE_ATTESTATION_PHRASE,
        operator_confirms_acquisition_generation_approval_digest=freeze.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        operator_confirms_acquisition_evidence_results_review_digest=freeze.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_acquisition_provider_evidence_execution_digest=freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        operator_confirms_acquisition_provider_evidence_request_approval_digest=freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        operator_confirms_acquisition_chain_candidate_review_digest=freeze.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_target_universe=list(freeze.TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_historical_bar_evidence_collected_count=12,
        operator_confirms_provider_request_count=12,
        operator_confirms_successful_provider_response_count=12,
        operator_confirms_failed_provider_response_count_zero=True,
        operator_confirms_meta_reduced_bar_count_preserved=True,
        operator_confirms_freeze_scope_acquisition_generation_only=True,
        operator_confirms_acquisition_generation_authorized=True,
        operator_confirms_acquisition_generation_approved=True,
        operator_confirms_ready_for_canonical_dataset_chain_candidate=True,
        operator_confirms_no_acquisition_generation_execution=True,
        operator_confirms_no_dataset_generation_authorization=True,
        operator_confirms_no_canonical_dataset_authorization=True,
        operator_confirms_no_canonical_dataset_candidate=True,
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
def source_approval() -> dict:
    return freeze._source_approval(None)


@pytest.fixture(scope="module")
def frozen(source_approval: dict) -> dict:
    return freeze.build_acquisition_generation_frozen_v1(
        acquisition_generation_approval_artifact=source_approval,
        operator_attestation=_attestation(),
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == freeze.OPERATOR_DECISION_FREEZE_ACQUISITION_GENERATION
    assert attestation["operator_attestation_version"] == freeze.OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_FREEZE_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        freeze.approval.evidence_review.execution,
        "execute_acquisition_provider_evidence_v1",
        lambda *args, **kwargs: pytest.fail("provider evidence execution was called"),
    )
    artifact = freeze.build_acquisition_generation_frozen_v1(operator_attestation=_attestation())
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_freeze"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", freeze.ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN),
        ("freeze_status", freeze.ACQUISITION_GENERATION_FROZEN),
        ("freeze_scope", freeze.ACQUISITION_GENERATION_FREEZE_ONLY),
        ("new_ticker_acquisition_authorized", True),
        ("acquisition_generation_authorized", True),
        ("acquisition_generation_approved", True),
        ("acquisition_generation_frozen", True),
        ("ready_for_canonical_dataset_chain_candidate", True),
        ("acquisition_generation_executed", False),
        ("acquisition_generation_results_created", False),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("historical_bar_evidence_collected_count", 12),
        ("provider_request_count", 12),
        ("successful_provider_response_count", 12),
        ("failed_provider_response_count", 0),
        ("target_universe_count", 12),
        ("target_universe", freeze.TARGET_UNIVERSE),
        ("acquisition_generation_approval_digest", freeze.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST),
        ("acquisition_evidence_results_review_package_digest", freeze.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("acquisition_provider_evidence_execution_digest", freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST),
        ("acquisition_provider_evidence_request_approval_digest", freeze.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST),
        ("acquisition_generation_chain_candidate_review_package_digest", freeze.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("corporate_action_authority_approval_digest", freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("provider_requests_made_in_freeze", False),
        ("live_provider_transport_enabled_in_freeze", False),
        ("market_data_acquisition_performed_in_freeze", False),
        ("acquisition_provider_evidence_rerun_performed", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", freeze.NOT_ACCEPTED),
        ("profitability", freeze.PROFITABILITY_NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_use", freeze.NOT_AUTHORIZED),
        ("strategy_use", freeze.NOT_AUTHORIZED),
        ("paper_trading", freeze.NOT_AUTHORIZED),
        ("broker_execution", freeze.NOT_AUTHORIZED),
    ],
)
def test_frozen_artifact_fields(frozen: dict, field: str, expected: object):
    assert frozen[field] == expected


def test_meta_and_per_ticker_freezes_are_preserved(frozen: dict):
    entries = frozen["per_ticker_acquisition_generation_freezes"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == freeze.TARGET_UNIVERSE
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_bar_count"] == 913
    assert meta["meta_reduced_bar_count_flag"] is True
    assert all(row["historical_bar_count"] == 1003 for row in entries if row["ticker"] != "META")
    assert all(row["per_ticker_acquisition_generation_freeze_digest"] for row in entries)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_decision", "REJECT"),
        ("operator_confirms_acquisition_generation_approval_digest", "0" * 64),
        ("operator_confirms_acquisition_evidence_results_review_digest", "0" * 64),
        ("operator_confirms_acquisition_provider_evidence_execution_digest", "0" * 64),
        ("operator_confirms_acquisition_provider_evidence_request_approval_digest", "0" * 64),
        ("operator_confirms_acquisition_chain_candidate_review_digest", "0" * 64),
        ("operator_confirms_corporate_action_authority_approval_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_historical_bar_evidence_collected_count", 11),
        ("operator_confirms_provider_request_count", 11),
        ("operator_confirms_successful_provider_response_count", 11),
    ]
    + [(field, False) for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS],
)
def test_invalid_operator_attestation_is_rejected(source_approval: dict, field: str, bad_value: object):
    attestation = _attestation()
    attestation[field] = bad_value
    with pytest.raises(freeze.AcquisitionGenerationFreezeError):
        freeze.build_acquisition_generation_frozen_v1(
            acquisition_generation_approval_artifact=source_approval,
            operator_attestation=attestation,
        )


def test_validator_accepts_valid_freeze(frozen: dict):
    result = freeze.validate_acquisition_generation_frozen_v1(frozen)
    assert result["status"] == freeze.ACQUISITION_GENERATION_FROZEN
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("freeze_status", "WRONG"),
        ("freeze_scope", "WRONG"),
        ("new_ticker_acquisition_authorized", False),
        ("acquisition_generation_authorized", False),
        ("acquisition_generation_approved", False),
        ("acquisition_generation_frozen", False),
        ("ready_for_canonical_dataset_chain_candidate", False),
        ("acquisition_generation_executed", True),
        ("acquisition_generation_results_created", True),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("historical_bar_evidence_collected_count", 11),
        ("provider_request_count", 11),
        ("successful_provider_response_count", 11),
        ("failed_provider_response_count", 1),
        ("meta_reduced_bar_count_preserved", False),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("provider_requests_made_in_freeze", True),
        ("live_provider_transport_enabled_in_freeze", True),
        ("market_data_acquisition_performed_in_freeze", True),
        ("acquisition_provider_evidence_rerun_performed", True),
        ("acquisition_generation_freeze_creates_dataset_authority", True),
        ("acquisition_generation_freeze_creates_canonical_dataset_authority", True),
        ("acquisition_generation_freeze_creates_registry_approval", True),
        ("acquisition_generation_freeze_creates_runtime_authority", True),
        ("acquisition_generation_freeze_digest", None),
    ],
)
def test_validator_rejects_invalid_freeze(frozen: dict, field: str, bad_value: object):
    invalid = deepcopy(frozen)
    invalid[field] = bad_value
    with pytest.raises(freeze.AcquisitionGenerationFreezeError):
        freeze.validate_acquisition_generation_frozen_v1(invalid)


def test_validator_rejects_missing_or_wrong_operator_attestation(frozen: dict):
    invalid = deepcopy(frozen)
    invalid["operator_attestation"]["operator_attestation_phrase"] = "wrong"
    with pytest.raises(freeze.AcquisitionGenerationFreezeError):
        freeze.validate_acquisition_generation_frozen_v1(invalid)


def test_validator_rejects_changed_meta_entry(frozen: dict):
    invalid = deepcopy(frozen)
    meta = next(row for row in invalid["per_ticker_acquisition_generation_freezes"] if row["ticker"] == "META")
    meta["historical_bar_count"] = 1003
    with pytest.raises(freeze.AcquisitionGenerationFreezeError):
        freeze.validate_acquisition_generation_frozen_v1(invalid)


def test_freeze_and_per_ticker_digests_are_deterministic(source_approval: dict):
    first = freeze.build_acquisition_generation_frozen_v1(
        acquisition_generation_approval_artifact=source_approval,
        operator_attestation=_attestation(),
    )
    second = freeze.build_acquisition_generation_frozen_v1(
        acquisition_generation_approval_artifact=source_approval,
        operator_attestation=_attestation(),
    )
    assert first["acquisition_generation_freeze_digest"] == second["acquisition_generation_freeze_digest"]
    assert [row["per_ticker_acquisition_generation_freeze_digest"] for row in first["per_ticker_acquisition_generation_freezes"]] == [
        row["per_ticker_acquisition_generation_freeze_digest"] for row in second["per_ticker_acquisition_generation_freezes"]
    ]


def test_markdown_includes_required_sections(frozen: dict):
    markdown = freeze.build_acquisition_generation_frozen_markdown_v1(frozen)
    for section in (
        "Frozen Acquisition Generation", "Operator Attestation", "Source Acquisition Generation Approval",
        "Source Acquisition Evidence Results Review", "Target Universe",
        "Frozen Per-Ticker Acquisition Generation Summary", "META Reduced Bar Count Preservation",
        "Freeze Scope", "Dataset Boundary", "Canonical Dataset Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Freeze Checklist Summary",
        "Remaining Required Tasks", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(tmp_path, source_approval: dict):
    result = freeze.write_acquisition_generation_frozen_v1(
        tmp_path,
        acquisition_generation_approval_artifact=source_approval,
        operator_attestation=_attestation(),
    )
    payload = json.loads((tmp_path / "acquisition_generation_frozen_v1.json").read_text(encoding="utf-8"))
    assert payload["acquisition_generation_freeze_digest"] == result["acquisition_generation_freeze_digest"]
    with pytest.raises(freeze.AcquisitionGenerationFreezeError):
        freeze.write_acquisition_generation_frozen_v1(
            tmp_path,
            acquisition_generation_approval_artifact=source_approval,
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN == freeze.ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN
    assert services.build_acquisition_generation_freeze_ceremony_v1 is freeze.build_acquisition_generation_frozen_v1
    assert services.validate_acquisition_generation_freeze_ceremony_v1 is freeze.validate_acquisition_generation_frozen_v1
