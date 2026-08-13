from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import dividend_policy_reconciliation_approval_service as approval


def _source_review() -> dict[str, Any]:
    entries = []
    for ticker in approval.EXPECTED_TARGET_UNIVERSE:
        status, count = approval.review.evidence.EXPECTED_PER_TICKER[ticker]
        entries.append({
            "ticker": ticker,
            "dividend_evidence_status": status,
            "dividend_event_count": count,
            "per_ticker_dividend_policy_reconciliation_review_digest": (ticker.lower() + "0" * 64)[:64],
        })
    return {
        "artifact_kind": approval.review.ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE,
        "review_status": approval.review.DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY,
        "dividend_policy_reconciliation_review_package_digest": approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "per_ticker_policy_review": entries,
        "review_summary": {"blocker_count": 0},
    }


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-13T00:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE,
        **approval._expected_digest_confirmations(),
        "operator_confirms_target_universe": approval.EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dividend_evidence_collected_count": 10,
        "operator_confirms_no_dividend_events_returned_count": 2,
        **{field: True for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS},
        "operator_decision": approval.OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION,
    }
    values.update(overrides)
    return approval.build_dividend_policy_reconciliation_approval_attestation_v1(**values)


def _patch_review(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(approval.review, "validate_dividend_policy_reconciliation_review_package_v1", lambda _source: {"blocker_count": 0})
    monkeypatch.setattr(approval.review, "build_dividend_policy_reconciliation_review_package_v1", _source_review)


def _artifact(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    _patch_review(monkeypatch)
    return approval.build_dividend_policy_reconciliation_approved_v1(
        dividend_policy_reconciliation_review_package=_source_review(),
        operator_attestation=_attestation(),
    )


def _redigest(artifact: dict[str, Any]) -> None:
    artifact["dividend_policy_reconciliation_approval_digest"] = (
        approval.dividend_policy_reconciliation_approval_digest_v1(artifact)
    )


def test_attestation_builder_creates_all_required_fields():
    attestation = _attestation()
    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION
    assert attestation["operator_attestation_phrase"] == approval.REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == approval.OPERATOR_ATTESTATION_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1
    assert all(attestation[field] is True for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    _patch_review(monkeypatch)
    monkeypatch.setattr(approval.review.evidence.execution, "execute_dividend_provider_evidence_v1", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("provider call")))
    artifact = approval.build_dividend_policy_reconciliation_approved_v1(operator_attestation=_attestation())
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


def test_artifact_status_scope_policy_approval_and_freeze_readiness(monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(monkeypatch)
    assert artifact["artifact_kind"] == approval.ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_APPROVED
    assert artifact["approval_status"] == approval.DIVIDEND_POLICY_RECONCILIATION_APPROVED
    assert artifact["approval_scope"] == approval.DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY
    assert artifact["dividend_policy_reconciliation_approved"] is True
    assert artifact["ready_for_dividend_event_authority_freeze"] is True


def test_all_source_digests_counts_and_universe_are_bound(monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(monkeypatch)
    expected = {
        "dividend_policy_reconciliation_review_package_digest": approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": approval.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": approval.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_report_digest": approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
    }
    assert {field: artifact[field] for field in expected} == expected
    assert artifact["target_universe"] == approval.EXPECTED_TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["dividend_evidence_collected_count"] == 10
    assert artifact["no_dividend_events_returned_count"] == 2
    assert artifact["zero_dividend_tickers"] == ["AMZN", "TSLA"]


def test_policy_decisions_are_approved_for_freeze_input_only(monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(monkeypatch)
    for field in (
        "dividend_adjusted_price_policy_approved_for_freeze_input",
        "cash_dividend_treatment_policy_approved_for_freeze_input",
        "special_dividend_treatment_policy_approved_for_freeze_input",
        "zero_dividend_absence_policy_approved_for_freeze_input",
    ):
        assert artifact[field] is True
    assert artifact["total_return_assumed"] is False
    assert artifact["dividend_reinvestment_assumed"] is False
    assert artifact["dataset_generation_authorized"] is False
    assert artifact["predictive_use_authorized"] is False


def test_per_ticker_entries_and_zero_row_policy_are_deterministic(monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(monkeypatch)
    assert len(artifact["per_ticker_policy_approval_entries"]) == 12
    for row in artifact["per_ticker_policy_approval_entries"]:
        assert len(row["per_ticker_dividend_policy_reconciliation_approval_digest"]) == 64
        assert row["policy_reconciliation_approval_status"] == "APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY"
        expected = "ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY" if row["ticker"] in {"AMZN", "TSLA"} else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
        assert row["dividend_absence_policy_status"] == expected


@pytest.mark.parametrize("field", [
    "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
    "dividend_provider_evidence_rerun_performed", "dividend_event_authority_created",
    "dividend_event_authority_frozen", "split_provider_evidence_rerun_performed",
    "corporate_action_authority_created", "new_ticker_acquisition_authorized",
    "dataset_generation_authorized", "acquisition_generation_authorized",
    "canonical_dataset_authorized", "registry_approval_created",
    "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
    "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
    "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
    "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
    "automatic_stitching", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
])
def test_downstream_authority_and_execution_boundaries_remain_false(monkeypatch: pytest.MonkeyPatch, field: str):
    assert _artifact(monkeypatch)[field] is False


@pytest.mark.parametrize(("field", "value"), [
    ("operator_decision", "WRONG"),
    ("operator_attestation_phrase", "WRONG"),
    ("operator_confirms_target_universe", list(reversed(approval.EXPECTED_TARGET_UNIVERSE))),
    ("operator_confirms_target_count", 11),
    ("operator_confirms_dividend_evidence_collected_count", 9),
    ("operator_confirms_no_dividend_events_returned_count", 3),
    ("operator_confirms_dividend_policy_reconciliation_review_package_digest", "0" * 64),
    ("operator_confirms_dividend_evidence_results_review_package_digest", "1" * 64),
    ("operator_confirms_dividend_provider_evidence_execution_digest", "2" * 64),
    ("operator_confirms_dividend_provider_evidence_request_approval_digest", "3" * 64),
    ("operator_confirms_dividend_policy_reconciliation_report_digest", "4" * 64),
])
def test_wrong_attestation_values_are_rejected(monkeypatch: pytest.MonkeyPatch, field: str, value: Any):
    _patch_review(monkeypatch)
    with pytest.raises(approval.DividendPolicyReconciliationApprovalError, match=field):
        approval.build_dividend_policy_reconciliation_approved_v1(
            dividend_policy_reconciliation_review_package=_source_review(),
            operator_attestation=_attestation(**{field: value}),
        )


@pytest.mark.parametrize("field", approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS)
def test_each_required_boolean_confirmation_is_fail_closed(monkeypatch: pytest.MonkeyPatch, field: str):
    _patch_review(monkeypatch)
    with pytest.raises(approval.DividendPolicyReconciliationApprovalError, match=field):
        approval.build_dividend_policy_reconciliation_approved_v1(
            dividend_policy_reconciliation_review_package=_source_review(),
            operator_attestation=_attestation(**{field: False}),
        )


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("approval_status", "WRONG"),
    ("approval_scope", "WRONG"), ("dividend_policy_reconciliation_approved", False),
    ("ready_for_dividend_event_authority_freeze", False),
    ("dividend_evidence_collected_count", 9), ("no_dividend_events_returned_count", 3),
    ("zero_dividend_tickers", ["AMZN"]), ("total_return_assumed", True),
    ("dividend_reinvestment_assumed", True), ("dataset_generation_authorized", True),
    ("predictive_use_authorized", True), ("dividend_event_authority_created", True),
    ("dividend_event_authority_frozen", True), ("split_event_authority_created", False),
    ("split_event_authority_frozen", False), ("split_provider_evidence_rerun_performed", True),
    ("corporate_action_authority_created", True), ("new_ticker_acquisition_authorized", True),
    ("canonical_dataset_authorized", True), ("registry_approval_created", True),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
    ("runtime_migration_approved", True), ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"), ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"), ("automatic_stitching", True),
    ("dividend_policy_reconciliation_approval_digest", None),
])
def test_validator_rejects_invalid_artifact_fields(monkeypatch: pytest.MonkeyPatch, field: str, value: Any):
    artifact = _artifact(monkeypatch)
    artifact[field] = value
    if field != "dividend_policy_reconciliation_approval_digest":
        _redigest(artifact)
    with pytest.raises(approval.DividendPolicyReconciliationApprovalError, match=field):
        approval.validate_dividend_policy_reconciliation_approved_v1(artifact)


def test_checklist_summary_and_validator_accept_valid_approval(monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(monkeypatch)
    assert [row["check_id"] for row in artifact["approval_checklist"]] == approval.REQUIRED_APPROVAL_CHECK_IDS
    assert all(row["status"] == approval.PASS for row in artifact["approval_checklist"])
    assert artifact["approval_summary"]["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert artifact["approval_summary"]["blocker_count"] == 0
    result = approval.validate_dividend_policy_reconciliation_approved_v1(artifact)
    assert result["status"] == "DIVIDEND_POLICY_RECONCILIATION_APPROVED_VALID"


def test_approval_and_per_ticker_digests_are_deterministic(monkeypatch: pytest.MonkeyPatch):
    first, second = _artifact(monkeypatch), _artifact(monkeypatch)
    assert first["dividend_policy_reconciliation_approval_digest"] == second["dividend_policy_reconciliation_approval_digest"]
    assert [row["per_ticker_dividend_policy_reconciliation_approval_digest"] for row in first["per_ticker_policy_approval_entries"]] == [row["per_ticker_dividend_policy_reconciliation_approval_digest"] for row in second["per_ticker_policy_approval_entries"]]


def test_markdown_contains_required_sections(monkeypatch: pytest.MonkeyPatch):
    markdown = approval.build_dividend_policy_reconciliation_approved_markdown_v1(_artifact(monkeypatch))
    for heading in (
        "# MarketFlow Dividend Policy Reconciliation Approval Status",
        "## Approved Dividend Policy Reconciliation", "## Operator Attestation",
        "## Source Dividend Policy Reconciliation Review", "## Target Universe",
        "## Approved Per-Ticker Dividend Policy Entries", "## Zero-Dividend Response Absence Policy",
        "## Adjusted vs Unadjusted Price Policy", "## Cash and Special Dividend Treatment",
        "## Total Return and Reinvestment Boundary", "## Canonical Dataset Impact Boundary",
        "## Predictive Label Impact Boundary", "## Dividend Authority Boundary",
        "## Split Authority Boundary", "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary", "## Dataset Boundary", "## Predictive/Profitability Boundary",
        "## Runtime Boundary", "## Approval Checklist Summary", "## Remaining Required Tasks", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_json_and_refuses_overwrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _patch_review(monkeypatch)
    result = approval.write_dividend_policy_reconciliation_approved_v1(
        tmp_path, dividend_policy_reconciliation_review_package=_source_review(),
        operator_attestation=_attestation(),
    )
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert payload["approval_status"] == approval.DIVIDEND_POLICY_RECONCILIATION_APPROVED
    with pytest.raises(approval.DividendPolicyReconciliationApprovalError, match="already exists"):
        approval.write_dividend_policy_reconciliation_approved_v1(
            tmp_path, dividend_policy_reconciliation_review_package=_source_review(),
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.build_dividend_policy_reconciliation_approved_v1 is approval.build_dividend_policy_reconciliation_approved_v1
    assert services.validate_dividend_policy_reconciliation_approved_v1 is approval.validate_dividend_policy_reconciliation_approved_v1
    assert services.write_dividend_policy_reconciliation_approved_v1 is approval.write_dividend_policy_reconciliation_approved_v1
