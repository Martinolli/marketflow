from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from marketflow import services
from marketflow.services import acquisition_generation_approval_service as approval


def _source_review() -> dict:
    return {
        "review_status": approval.evidence_review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
        "acquisition_evidence_results_review_package_digest": approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "review_summary": {"blocker_count": 0},
        "historical_bar_evidence_collected_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "meta_reduced_bar_count_recorded": True,
        "per_ticker_acquisition_evidence_summary": [
            {
                "ticker": ticker,
                "acquisition_provider_evidence_status": approval.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
                "historical_bar_count": 913 if ticker == "META" else 1003,
            }
            for ticker in approval.TARGET_UNIVERSE
        ],
    }


def _attestation() -> dict:
    return approval.build_acquisition_generation_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-14T12:00:00Z",
        operator_attestation_phrase=approval.REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_acquisition_evidence_results_review_digest=approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_acquisition_provider_evidence_execution_digest=approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        operator_confirms_acquisition_provider_evidence_request_approval_digest=approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        operator_confirms_acquisition_chain_candidate_review_digest=approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_target_universe=list(approval.TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_historical_bar_evidence_collected_count=12,
        operator_confirms_provider_request_count=12,
        operator_confirms_successful_provider_response_count=12,
        operator_confirms_failed_provider_response_count_zero=True,
        operator_confirms_meta_reduced_bar_count_preserved=True,
        operator_confirms_approval_scope_acquisition_generation_only=True,
        operator_confirms_new_ticker_acquisition_authorized=True,
        operator_confirms_acquisition_generation_authorized=True,
        operator_confirms_ready_for_acquisition_generation_freeze=True,
        operator_confirms_no_acquisition_generation_execution=True,
        operator_confirms_no_acquisition_generation_freeze=True,
        operator_confirms_no_dataset_generation_authorization=True,
        operator_confirms_no_canonical_dataset_authorization=True,
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


def _build(source: dict | None = None, attestation: dict | None = None) -> dict:
    source = _source_review() if source is None else source
    validation = {
        "acquisition_evidence_results_review_package_digest": (
            approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        )
    }
    with patch.object(
        approval.evidence_review,
        "validate_acquisition_evidence_results_review_package_v1",
        return_value=validation,
    ):
        return approval.build_acquisition_generation_approved_v1(
            acquisition_evidence_results_review_package=source,
            operator_attestation=_attestation() if attestation is None else attestation,
        )


@pytest.fixture(scope="module")
def approved() -> dict:
    return _build()


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION
    assert attestation["operator_attestation_version"] == approval.OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_APPROVAL_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    source = _source_review()
    monkeypatch.setattr(approval.evidence_review, "build_acquisition_evidence_results_review_package_v1", lambda: source)
    monkeypatch.setattr(
        approval.evidence_review,
        "validate_acquisition_evidence_results_review_package_v1",
        lambda package: {
            "acquisition_evidence_results_review_package_digest": approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        },
    )
    monkeypatch.setattr(
        approval.evidence_review.execution,
        "execute_acquisition_provider_evidence_v1",
        lambda *args, **kwargs: pytest.fail("provider evidence execution was called"),
    )
    artifact = approval.build_acquisition_generation_approved_v1(operator_attestation=_attestation())
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", approval.ARTIFACT_KIND_ACQUISITION_GENERATION_APPROVED),
        ("approval_status", approval.ACQUISITION_GENERATION_APPROVED),
        ("approval_scope", approval.ACQUISITION_GENERATION_APPROVAL_ONLY),
        ("new_ticker_acquisition_authorized", True),
        ("acquisition_generation_authorized", True),
        ("acquisition_generation_approved", True),
        ("ready_for_acquisition_generation_freeze", True),
        ("acquisition_generation_executed", False),
        ("acquisition_generation_frozen", False),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_candidate_created", False),
        ("registry_approval_created", False),
        ("historical_bar_evidence_collected_count", 12),
        ("provider_request_count", 12),
        ("successful_provider_response_count", 12),
        ("failed_provider_response_count", 0),
        ("target_universe_count", 12),
        ("target_universe", approval.TARGET_UNIVERSE),
        ("acquisition_evidence_results_review_package_digest", approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("acquisition_provider_evidence_execution_digest", approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST),
        ("acquisition_provider_evidence_request_approval_digest", approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST),
        ("acquisition_generation_chain_candidate_review_package_digest", approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("corporate_action_authority_approval_digest", approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("provider_requests_made_in_approval", False),
        ("live_provider_transport_enabled_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("acquisition_provider_evidence_rerun_performed", False),
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


def test_meta_and_per_ticker_approvals_are_preserved(approved: dict):
    entries = approved["per_ticker_acquisition_generation_approvals"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_bar_count"] == 913
    assert meta["meta_reduced_bar_count_flag"] is True
    assert all(row["historical_bar_count"] == 1003 for row in entries if row["ticker"] != "META")
    assert all(row["per_ticker_acquisition_generation_approval_digest"] for row in entries)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_decision", "REJECT"),
        ("operator_confirms_acquisition_evidence_results_review_digest", "0" * 64),
        ("operator_confirms_acquisition_provider_evidence_execution_digest", "0" * 64),
        ("operator_confirms_acquisition_provider_evidence_request_approval_digest", "0" * 64),
        ("operator_confirms_acquisition_chain_candidate_review_digest", "0" * 64),
        ("operator_confirms_corporate_action_authority_approval_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_historical_bar_evidence_collected_count", 11),
        ("operator_confirms_provider_request_count", 11),
        ("operator_confirms_successful_provider_response_count", 11),
    ]
    + [(field, False) for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS],
)
def test_invalid_operator_attestation_is_rejected(field: str, bad_value: object):
    attestation = _attestation()
    attestation[field] = bad_value
    with pytest.raises(approval.AcquisitionGenerationApprovalError):
        _build(attestation=attestation)


def test_validator_accepts_valid_approval(approved: dict):
    result = approval.validate_acquisition_generation_approved_v1(approved)
    assert result["status"] == approval.ACQUISITION_GENERATION_APPROVED
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("new_ticker_acquisition_authorized", False),
        ("acquisition_generation_authorized", False),
        ("acquisition_generation_approved", False),
        ("ready_for_acquisition_generation_freeze", False),
        ("acquisition_generation_executed", True),
        ("acquisition_generation_frozen", True),
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
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("acquisition_provider_evidence_rerun_performed", True),
        ("approval_creates_dataset_authority", True),
        ("approval_creates_canonical_dataset_authority", True),
        ("approval_creates_registry_approval", True),
        ("approval_creates_runtime_authority", True),
    ],
)
def test_validator_rejects_invalid_authority_or_scope(approved: dict, field: str, bad_value: object):
    changed = deepcopy(approved)
    changed[field] = bad_value
    with pytest.raises(approval.AcquisitionGenerationApprovalError):
        approval.validate_acquisition_generation_approved_v1(changed)


def test_validator_rejects_missing_or_wrong_attestation_and_digest(approved: dict):
    for mutation in ("missing_attestation", "wrong_attestation", "missing_digest"):
        changed = deepcopy(approved)
        if mutation == "missing_attestation":
            changed.pop("operator_attestation")
        elif mutation == "wrong_attestation":
            changed["operator_attestation"]["operator_decision"] = "REJECT"
        else:
            changed.pop("acquisition_generation_approval_digest")
        with pytest.raises(approval.AcquisitionGenerationApprovalError):
            approval.validate_acquisition_generation_approved_v1(changed)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _build()
    second = _build()
    assert first["acquisition_generation_approval_digest"] == second["acquisition_generation_approval_digest"]
    assert [row["per_ticker_acquisition_generation_approval_digest"] for row in first["per_ticker_acquisition_generation_approvals"]] == [
        row["per_ticker_acquisition_generation_approval_digest"]
        for row in second["per_ticker_acquisition_generation_approvals"]
    ]


def test_markdown_includes_required_sections(approved: dict):
    markdown = approval.build_acquisition_generation_approved_markdown_v1(approved)
    for heading in (
        "Approved Acquisition Generation", "Operator Attestation",
        "Source Acquisition Evidence Results Review", "Source Provider Evidence Execution",
        "Target Universe", "Approved Per-Ticker Acquisition Generation Summary",
        "META Reduced Bar Count Preservation", "Approval Scope", "Acquisition Execution Boundary",
        "Acquisition Freeze Boundary", "Dataset Boundary", "Canonical Dataset Boundary",
        "Registry Boundary", "Predictive/Profitability Boundary", "Runtime Boundary",
        "Approval Checklist Summary", "Remaining Required Tasks", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_writes_canonical_json_and_refuses_overwrite(tmp_path: Path):
    source = _source_review()
    validation = {
        "acquisition_evidence_results_review_package_digest": approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
    }
    with patch.object(approval.evidence_review, "validate_acquisition_evidence_results_review_package_v1", return_value=validation):
        receipt = approval.write_acquisition_generation_approved_v1(
            tmp_path,
            acquisition_evidence_results_review_package=source,
            operator_attestation=_attestation(),
        )
        with pytest.raises(approval.AcquisitionGenerationApprovalError):
            approval.write_acquisition_generation_approved_v1(
                tmp_path,
                acquisition_evidence_results_review_package=source,
                operator_attestation=_attestation(),
            )
    payload = json.loads(Path(receipt["path"]).read_text(encoding="utf-8"))
    assert payload["acquisition_generation_approval_digest"] == receipt["acquisition_generation_approval_digest"]


def test_public_services_exports_approval_api():
    for name in (
        "ARTIFACT_KIND_ACQUISITION_GENERATION_APPROVED",
        "ACQUISITION_GENERATION_APPROVED",
        "ACQUISITION_GENERATION_APPROVAL_ONLY",
        "REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE",
        "build_acquisition_generation_approval_attestation_v1",
        "build_acquisition_generation_approved_v1",
        "validate_acquisition_generation_approved_v1",
        "write_acquisition_generation_approved_v1",
        "build_acquisition_generation_approved_markdown_v1",
    ):
        assert name in services.__all__
        assert hasattr(services, name)
