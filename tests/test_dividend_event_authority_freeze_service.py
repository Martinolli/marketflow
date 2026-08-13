from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import dividend_event_authority_freeze_service as freeze


def _source_approval() -> dict[str, Any]:
    entries = []
    for ticker in freeze.TARGET_UNIVERSE:
        status, count = freeze.EXPECTED_PER_TICKER[ticker]
        entry = {
            "ticker": ticker,
            "dividend_evidence_status": status,
            "dividend_event_count": count,
            "per_ticker_dividend_policy_reconciliation_approval_digest": (
                ticker.lower() + "0" * 64
            )[:64],
        }
        entries.append(entry)
    return {
        "artifact_kind": freeze.approval.ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "approval_status": freeze.approval.DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "approval_scope": freeze.approval.DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY,
        "dividend_policy_reconciliation_approval_digest": freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "target_universe": freeze.TARGET_UNIVERSE,
        "target_universe_count": 12,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": freeze.ZERO_DIVIDEND_TICKERS,
        "total_return_assumed": False,
        "dividend_reinvestment_assumed": False,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "approval_summary": {"blocker_count": 0},
        "per_ticker_policy_approval_entries": entries,
    }


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-13T08:00:00Z",
        "operator_attestation_phrase": freeze.REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE,
        **freeze._expected_digest_confirmations(),
        "operator_confirms_target_universe": freeze.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dividend_evidence_collected_count": 10,
        "operator_confirms_no_dividend_events_returned_count": 2,
        **{field: True for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS},
        "operator_decision": freeze.OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY,
    }
    values.update(overrides)
    return freeze.build_dividend_event_authority_freeze_attestation_v1(**values)


@pytest.fixture(autouse=True)
def _offline_source(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        freeze.approval,
        "validate_dividend_policy_reconciliation_approved_v1",
        lambda _source: {
            "dividend_policy_reconciliation_approval_digest": freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
            "blocker_count": 0,
        },
    )
    monkeypatch.setattr(freeze, "_build_expected_policy_approval_artifact", _source_approval)


def _artifact(**attestation_overrides: Any) -> dict[str, Any]:
    return freeze.build_dividend_event_authority_frozen_v1(
        dividend_policy_reconciliation_approval_artifact=_source_approval(),
        operator_attestation=_attestation(**attestation_overrides),
    )


def _redigest(artifact: dict[str, Any]) -> None:
    artifact["dividend_event_authority_freeze_digest"] = (
        freeze.dividend_event_authority_freeze_digest_v1(artifact)
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == freeze.OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY
    assert attestation["operator_attestation_phrase"] == freeze.REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == freeze.OPERATOR_ATTESTATION_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        freeze.approval.review.evidence.execution,
        "execute_dividend_provider_evidence_v1",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("provider call")),
    )
    artifact = freeze.build_dividend_event_authority_frozen_v1(
        operator_attestation=_attestation()
    )
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_freeze"] is False
    assert artifact["live_provider_transport_enabled_in_freeze"] is False
    assert artifact["dividend_provider_evidence_rerun_performed"] is False


def test_artifact_kind_status_scope_and_authority_state_are_exact():
    artifact = _artifact()
    assert artifact["artifact_kind"] == freeze.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN
    assert artifact["freeze_status"] == freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN
    assert artifact["authority_scope"] == freeze.DIVIDEND_EVENT_AUTHORITY_ONLY
    assert artifact["dividend_event_authority_created"] is True
    assert artifact["dividend_event_authority_frozen"] is True


def test_source_evidence_digests_are_bound():
    artifact = _artifact()
    expected = {
        "dividend_policy_reconciliation_approval_digest": freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": freeze.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": freeze.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": freeze.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_report_digest": freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "corporate_action_authority_plan_approval_digest": freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
    }
    assert {field: artifact[field] for field in expected} == expected


def test_target_universe_counts_and_zero_dividend_policy_are_exact():
    artifact = _artifact()
    assert artifact["target_universe"] == freeze.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["provider_request_count"] == 12
    assert artifact["successful_provider_response_count"] == 12
    assert artifact["failed_provider_response_count"] == 0
    assert artifact["dividend_evidence_collected_count"] == 10
    assert artifact["no_dividend_events_returned_count"] == 2
    assert artifact["zero_dividend_tickers"] == ["AMZN", "TSLA"]


def test_per_ticker_freeze_entries_preserve_counts_classification_and_digests():
    entries = _artifact()["per_ticker_dividend_event_authority"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == freeze.TARGET_UNIVERSE
    for row in entries:
        ticker = row["ticker"]
        assert row["dividend_event_count"] == freeze.EXPECTED_PER_TICKER[ticker][1]
        assert len(row["per_ticker_dividend_event_authority_freeze_digest"]) == 64
        assert row["per_ticker_dividend_event_authority_freeze_digest"] == freeze.per_ticker_dividend_event_authority_freeze_digest_v1(row)
        if ticker in ("AMZN", "TSLA"):
            assert row["dividend_event_authority_classification"] == freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY
            assert row["dividend_absence_policy_status"] == freeze.ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY
        else:
            assert row["dividend_event_authority_classification"] == freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE
            assert row["dividend_absence_policy_status"] == freeze.DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE


def test_policy_and_downstream_boundaries_remain_closed():
    artifact = _artifact()
    assert artifact["total_return_assumed"] is False
    assert artifact["dividend_reinvestment_assumed"] is False
    assert artifact["canonical_dataset_impact_authorized"] is False
    assert artifact["predictive_label_impact_authorized"] is False
    assert artifact["predictive_use_authorized"] is False
    assert artifact["split_event_authority_created"] is True
    assert artifact["split_event_authority_frozen"] is True
    assert artifact["corporate_action_authority_created"] is False
    assert artifact["ready_for_combined_corporate_action_readiness_review"] is True
    assert artifact["new_ticker_acquisition_authorized"] is False
    assert artifact["dataset_generation_authorized"] is False
    assert artifact["additional_predictive_evidence_execution_authorized"] is False
    assert artifact["additional_predictive_evidence_executed"] is False
    assert artifact["predictive_usefulness"] == freeze.NOT_ACCEPTED
    assert artifact["profitability"] == freeze.PROFITABILITY_NOT_ACCEPTED
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_use"] == freeze.NOT_AUTHORIZED
    assert artifact["strategy_use"] == freeze.NOT_AUTHORIZED
    assert artifact["paper_trading"] == freeze.NOT_AUTHORIZED
    assert artifact["broker_execution"] == freeze.NOT_AUTHORIZED


def test_checklist_and_summary_pass_without_blockers():
    artifact = _artifact()
    assert [row["check_id"] for row in artifact["freeze_checklist"]] == freeze.REQUIRED_FREEZE_CHECK_IDS
    assert all(row["status"] == freeze.PASS for row in artifact["freeze_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in artifact["freeze_checklist"])
    assert artifact["freeze_summary"]["total_checks"] == len(freeze.REQUIRED_FREEZE_CHECK_IDS)
    assert artifact["freeze_summary"]["passed_checks"] == len(freeze.REQUIRED_FREEZE_CHECK_IDS)
    assert artifact["freeze_summary"]["failed_checks"] == 0
    assert artifact["freeze_summary"]["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "APPROVE"),
        ("operator_attestation_phrase", "wrong"),
        ("operator_confirms_target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_dividend_evidence_collected_count", 9),
        ("operator_confirms_no_dividend_events_returned_count", 3),
        *[(field, "0" * 64) for field in freeze._expected_digest_confirmations()],
        *[(field, False) for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS],
    ],
)
def test_invalid_operator_attestation_is_rejected(field: str, bad_value: Any):
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        _artifact(**{field: bad_value})


@pytest.mark.parametrize("field", ["operator_reference", "operator_attestation_timestamp_utc"])
def test_missing_operator_identity_metadata_is_rejected(field: str):
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        _artifact(**{field: ""})


def test_wrong_source_approval_digest_is_rejected():
    source = _source_approval()
    source["dividend_policy_reconciliation_approval_digest"] = "0" * 64
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.build_dividend_event_authority_frozen_v1(
            dividend_policy_reconciliation_approval_artifact=source,
            operator_attestation=_attestation(),
        )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("schema_version", "wrong"),
        ("freeze_status", "WRONG"),
        ("authority_scope", "WRONG"),
        ("dividend_event_authority_created", False),
        ("dividend_event_authority_frozen", False),
        ("target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("dividend_evidence_collected_count", 9),
        ("no_dividend_events_returned_count", 3),
        ("zero_dividend_tickers", ["AMZN"]),
        ("total_return_assumed", True),
        ("dividend_reinvestment_assumed", True),
        ("dataset_generation_authorized", True),
        ("predictive_use_authorized", True),
        ("provider_requests_made_in_freeze", True),
        ("live_provider_transport_enabled_in_freeze", True),
        ("dividend_provider_evidence_rerun_performed", True),
        ("split_event_authority_created", False),
        ("split_event_authority_frozen", False),
        ("split_provider_evidence_rerun_performed", True),
        ("corporate_action_authority_created", True),
        ("new_ticker_acquisition_authorized", True),
        ("acquisition_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("registry_approval_created", True),
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
    ],
)
def test_validator_rejects_invalid_authority_or_boundary(field: str, bad_value: Any):
    artifact = _artifact()
    artifact[field] = bad_value
    _redigest(artifact)
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.validate_dividend_event_authority_frozen_v1(artifact)


def test_validator_rejects_missing_per_ticker_entry():
    artifact = _artifact()
    artifact["per_ticker_dividend_event_authority"].pop()
    _redigest(artifact)
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.validate_dividend_event_authority_frozen_v1(artifact)


def test_validator_rejects_missing_per_ticker_digest():
    artifact = _artifact()
    artifact["per_ticker_dividend_event_authority"][0].pop(
        "per_ticker_dividend_event_authority_freeze_digest"
    )
    _redigest(artifact)
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.validate_dividend_event_authority_frozen_v1(artifact)


def test_validator_rejects_wrong_attestation_and_missing_freeze_digest():
    artifact = _artifact()
    artifact["operator_attestation"]["operator_decision"] = "WRONG"
    _redigest(artifact)
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.validate_dividend_event_authority_frozen_v1(artifact)
    artifact = _artifact()
    artifact.pop("dividend_event_authority_freeze_digest")
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.validate_dividend_event_authority_frozen_v1(artifact)


def test_validator_accepts_valid_freeze():
    result = freeze.validate_dividend_event_authority_frozen_v1(_artifact())
    assert result["status"] == "DIVIDEND_EVENT_AUTHORITY_FROZEN_VALID"
    assert result["authority_scope"] == freeze.DIVIDEND_EVENT_AUTHORITY_ONLY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_freeze_and_per_ticker_digests_are_deterministic():
    first = _artifact()
    second = _artifact()
    assert first["dividend_event_authority_freeze_digest"] == second["dividend_event_authority_freeze_digest"]
    assert [row["per_ticker_dividend_event_authority_freeze_digest"] for row in first["per_ticker_dividend_event_authority"]] == [row["per_ticker_dividend_event_authority_freeze_digest"] for row in second["per_ticker_dividend_event_authority"]]


def test_markdown_includes_required_sections():
    markdown = freeze.build_dividend_event_authority_frozen_markdown_v1(_artifact())
    for section in (
        "Frozen Dividend Event Authority",
        "Operator Attestation",
        "Source Dividend Policy Reconciliation Approval",
        "Source Dividend Evidence Results",
        "Target Universe",
        "Frozen Per-Ticker Dividend Authority Summary",
        "Zero-Dividend Response Absence Policy",
        "Total Return and Reinvestment Boundary",
        "Canonical Dataset Impact Boundary",
        "Predictive Label Impact Boundary",
        "Authority Scope",
        "Split Authority Boundary",
        "Corporate-Action Authority Boundary",
        "Acquisition Boundary",
        "Dataset Boundary",
        "Predictive/Profitability Boundary",
        "Runtime Boundary",
        "Freeze Checklist Summary",
        "Remaining Required Tasks",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_json_and_markdown_without_overwrite(tmp_path: Path):
    result = freeze.write_dividend_event_authority_frozen_v1(
        tmp_path,
        dividend_policy_reconciliation_approval_artifact=_source_approval(),
        operator_attestation=_attestation(),
    )
    assert Path(result["json_path"]).exists()
    assert Path(result["markdown_path"]).exists()
    payload = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    assert payload["freeze_status"] == freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN
    with pytest.raises(freeze.DividendEventAuthorityFreezeError):
        freeze.write_dividend_event_authority_frozen_v1(
            tmp_path,
            dividend_policy_reconciliation_approval_artifact=_source_approval(),
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN == freeze.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN
    assert services.DIVIDEND_EVENT_AUTHORITY_FROZEN == freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN
    assert services.DIVIDEND_EVENT_AUTHORITY_ONLY == freeze.DIVIDEND_EVENT_AUTHORITY_ONLY
    assert services.REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE == freeze.REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE
    assert services.build_dividend_event_authority_freeze_attestation_v1 is freeze.build_dividend_event_authority_freeze_attestation_v1
    assert services.build_dividend_event_authority_frozen_v1 is freeze.build_dividend_event_authority_frozen_v1
    assert services.validate_dividend_event_authority_frozen_v1 is freeze.validate_dividend_event_authority_frozen_v1
    assert services.write_dividend_event_authority_frozen_v1 is freeze.write_dividend_event_authority_frozen_v1
