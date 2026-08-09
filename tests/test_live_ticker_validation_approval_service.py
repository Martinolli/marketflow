from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import live_ticker_validation_approval_service as approval


EXPECTED_APPROVAL_DIGEST = (
    "2bf668bb4aae3756652ee5eea790b76d1ba73bdd7723efc1c31227c5c3e897e4"
)


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-09T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_live_ticker_validation_candidate_digest": (
            approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
        ),
        "operator_confirms_live_ticker_validation_candidate_review_package_digest": (
            approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_ticker_universe_selection_approval_digest": (
            approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "operator_confirms_validation_target_universe": (
            approval.APPROVED_EXPANDED_TICKER_UNIVERSE
        ),
        "operator_confirms_validation_target_count": 12,
    }
    values.update({field: True for field in approval.OPERATOR_CONFIRMATION_FIELDS})
    values.update(overrides)
    return approval.build_live_ticker_validation_approval_attestation_v1(**values)


def _approved(**attestation_overrides: Any) -> dict[str, Any]:
    return approval.build_live_ticker_validation_approved_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def _redigest(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["approval_checklist"] = approval._approval_checklist(artifact)
    artifact["approval_summary"] = approval._summary(artifact["approval_checklist"])
    artifact["live_ticker_validation_approval_digest"] = (
        approval.live_ticker_validation_approval_digest_v1(artifact)
    )
    return artifact


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_LIVE_TICKER_VALIDATION
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_confirms_live_ticker_validation_candidate_digest"] == (
        approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    )
    assert all(attestation[field] is True for field in approval.OPERATOR_CONFIRMATION_FIELDS)


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("approval ceremony must not call provider or rebuild live paths")

    monkeypatch.setattr(
        approval.review.candidate_service,
        "build_live_ticker_validation_candidate_v1",
        fail_if_called,
    )
    monkeypatch.setattr(
        approval.review.candidate_service.selection_approval,
        "build_ticker_universe_selection_approved_v1",
        fail_if_called,
    )

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["provider_requests_made_in_approval"] is False


def test_artifact_kind_status_and_scope_are_live_ticker_validation_approved():
    artifact = _approved()

    assert artifact["artifact_kind"] == approval.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED
    assert artifact["approval_status"] == approval.LIVE_TICKER_VALIDATION_APPROVED
    assert artifact["approval_scope"] == approval.READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY


def test_provider_request_and_live_ticker_validation_are_authorized_only_for_future_run():
    artifact = _approved()

    assert artifact["provider_request_authorized"] is True
    assert artifact["live_ticker_validation_authorized"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled"] is False
    assert artifact["live_ticker_validation_performed"] is False
    assert artifact["live_validation_results_created"] is False


def test_validation_target_universe_has_12_expected_tickers_in_order():
    artifact = _approved()

    assert artifact["validation_target_universe"] == [
        "MSFT",
        "NVDA",
        "AMZN",
        "GOOGL",
        "META",
        "TSLA",
        "JPM",
        "XOM",
        "JNJ",
        "WMT",
        "CAT",
        "LMT",
    ]
    assert artifact["validation_target_count"] == 12


def test_source_candidate_review_and_ticker_universe_approval_digests_match():
    artifact = _approved()

    assert artifact["source_live_ticker_validation_candidate_digest"] == (
        approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    )
    assert artifact["source_live_ticker_validation_candidate_review_package_digest"] == (
        approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["ticker_universe_selection_approval_digest"] == (
        approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )
    assert artifact["source_live_ticker_validation_candidate_review_checklist_failed"] == 0
    assert artifact["source_live_ticker_validation_candidate_review_blocker_count"] == 0


def test_validation_targets_preserve_request_validation_listing_authority_and_runtime_boundaries():
    entries = _approved()["validation_target_entries"]

    assert len(entries) == 12
    assert {entry["validation_approval_scope"] for entry in entries} == {
        approval.READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY
    }
    assert {entry["provider_request_authorized"] for entry in entries} == {True}
    assert {entry["live_validation_authorized"] for entry in entries} == {True}
    assert {entry["provider_request_status"] for entry in entries} == {approval.NOT_REQUESTED}
    assert {entry["live_validation_status"] for entry in entries} == {approval.NOT_PERFORMED}
    for field in (
        "listing_status",
        "security_type_status",
        "exchange_status",
        "active_status",
        "delisting_status",
        "tradability_status",
        "corporate_action_data_availability_status",
        "historical_aggregate_data_availability_status",
    ):
        assert {entry[field] for entry in entries} == {approval.NOT_VERIFIED}
    for field in (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {approval.NOT_CREATED}
    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
    ):
        assert {entry[field] for entry in entries} == {approval.NOT_AUTHORIZED}


@pytest.mark.parametrize(
    "field",
    [
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "live_ticker_validation_execution_artifact_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ],
)
def test_downstream_execution_authority_and_artifact_flags_remain_false(field: str):
    assert _approved()[field] is False


def test_predictive_profitability_and_runtime_uses_remain_closed():
    artifact = _approved()

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_use"] == approval.NOT_AUTHORIZED
    assert artifact["strategy_use"] == approval.NOT_AUTHORIZED
    assert artifact["paper_trading"] == approval.NOT_AUTHORIZED
    assert artifact["broker_execution"] == approval.NOT_AUTHORIZED


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_attestation_phrase", "APPROVE SOMETHING ELSE", "operator_attestation_phrase_matches"),
        ("operator_decision", "REJECT", "operator_decision_approved"),
        ("operator_confirms_live_ticker_validation_candidate_digest", "0" * 64, "operator_confirms_candidate_digest"),
        ("operator_confirms_live_ticker_validation_candidate_review_package_digest", "0" * 64, "operator_confirms_candidate_review_digest"),
        ("operator_confirms_ticker_universe_selection_approval_digest", "0" * 64, "operator_confirms_ticker_universe_approval_digest"),
        ("operator_confirms_validation_target_universe", ["MSFT"], "operator_confirms_validation_target_universe"),
        ("operator_confirms_validation_target_count", 11, "validation_target_count_12"),
    ],
)
def test_builder_rejects_wrong_attestation_bindings(field: str, value: Any, match: str):
    with pytest.raises(approval.LiveTickerValidationApprovalError, match=match):
        _approved(**{field: value})


@pytest.mark.parametrize("field", approval.OPERATOR_CONFIRMATION_FIELDS)
def test_builder_rejects_missing_operator_boundary_confirmation(field: str):
    with pytest.raises(approval.LiveTickerValidationApprovalError, match=field):
        _approved(**{field: False})


def test_checklist_contains_all_required_check_ids_and_passes():
    checklist = _approved()["approval_checklist"]

    assert [item["check_id"] for item in checklist] == approval.REQUIRED_APPROVAL_CHECK_IDS
    assert {item["status"] for item in checklist} == {approval.PASS}
    assert len(checklist) == 80


def test_summary_counts_and_authorization_boundaries_are_approval_only():
    summary = _approved()["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["live_ticker_validation_authorized_by_operator"] is True
    assert summary["provider_request_authorized"] is True
    assert summary["provider_requests_made"] is False
    assert summary["live_provider_transport_enabled"] is False
    assert summary["live_ticker_validation_performed"] is False
    assert summary["live_validation_results_created"] is False
    assert summary["new_ticker_authority_authorized"] is False
    assert summary["acquisition_authorized"] is False
    assert summary["dataset_generation_authorized"] is False
    assert summary["additional_predictive_evidence_execution_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_validator_accepts_valid_approval_artifact():
    validation = approval.validate_live_ticker_validation_approved_v1(_approved())

    assert validation["status"] == "LIVE_TICKER_VALIDATION_APPROVED_VALID"
    assert validation["provider_request_authorized"] is True
    assert validation["live_ticker_validation_authorized"] is True
    assert validation["live_ticker_validation_performed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "RUNTIME_VALIDATION"),
        ("provider_request_authorized", False),
        ("live_ticker_validation_authorized", False),
        ("provider_requests_made", True),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled", True),
        ("live_ticker_validation_performed", True),
        ("live_validation_results_created", True),
        ("new_ticker_authority_created", True),
        ("new_ticker_acquisition_authorized", True),
        ("dataset_generation_authorized", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", True),
        ("walk_forward_rerun_performed", True),
        ("label_regeneration_performed", True),
        ("feature_matrix_regeneration_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_migration_active", True),
        ("strategy_runtime_migration", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
    ],
)
def test_validator_rejects_invalid_approval_mutations(field: str, value: Any):
    artifact = deepcopy(_approved())
    artifact[field] = value

    with pytest.raises(approval.LiveTickerValidationApprovalError):
        approval.validate_live_ticker_validation_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("validation_target_count", 11),
        ("validation_target_universe", ["MSFT"]),
    ],
)
def test_validator_rejects_invalid_validation_target_universe(field: str, value: Any):
    artifact = deepcopy(_approved())
    artifact[field] = value
    _redigest(artifact)

    with pytest.raises(approval.LiveTickerValidationApprovalError):
        approval.validate_live_ticker_validation_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_request_status", "REQUESTED"),
        ("live_validation_status", "PERFORMED"),
        ("listing_status", "VERIFIED"),
        ("identity_authority_status", "CREATED"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_validation_target_statuses(field: str, value: str):
    artifact = deepcopy(_approved())
    artifact["validation_target_entries"][0][field] = value
    _redigest(artifact)

    with pytest.raises(approval.LiveTickerValidationApprovalError):
        approval.validate_live_ticker_validation_approved_v1(artifact)


def test_validator_rejects_missing_operator_attestation():
    artifact = deepcopy(_approved())
    artifact["operator_attestation"] = None

    with pytest.raises(approval.LiveTickerValidationApprovalError, match="operator_attestation"):
        approval.validate_live_ticker_validation_approved_v1(artifact)


def test_validator_rejects_mutated_approval_digest():
    artifact = deepcopy(_approved())
    artifact["live_ticker_validation_approval_digest"] = "0" * 64

    with pytest.raises(approval.LiveTickerValidationApprovalError, match="approval_digest"):
        approval.validate_live_ticker_validation_approved_v1(artifact)


def test_approval_artifact_digest_is_deterministic_and_expected():
    first = _approved()
    second = _approved()

    assert first["live_ticker_validation_approval_digest"] == EXPECTED_APPROVAL_DIGEST
    assert first["live_ticker_validation_approval_digest"] == second[
        "live_ticker_validation_approval_digest"
    ]
    assert first["live_ticker_validation_approval_digest"] == (
        approval.live_ticker_validation_approval_digest_v1(first)
    )


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _approved()["remaining_roadmap"]

    assert "Live ticker validation execution." in roadmap
    assert "Live ticker validation results review." in roadmap
    assert "Per-ticker identity authority chain." in roadmap
    assert "Per-ticker corporate-action authority chain." in roadmap
    assert "Per-ticker acquisition authority chain." in roadmap
    assert "Dataset authority chain after validated ticker authority." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = approval.build_live_ticker_validation_approved_markdown_v1(_approved())

    for section in [
        "## Title",
        "## Approved Live Ticker Validation",
        "## Operator Attestation",
        "## Source Candidate Review Package",
        "## Validation Target Universe",
        "## Approval Scope",
        "## Provider Request Boundary",
        "## API Key / Raw Payload Boundary",
        "## Validation Execution Boundary",
        "## New Ticker Authority Boundary",
        "## Acquisition Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert section in markdown
    assert "No provider request was made" in markdown


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = approval.write_live_ticker_validation_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert result["filename"] == "live_ticker_validation_approved_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0
    with pytest.raises(approval.LiveTickerValidationApprovalError, match="already exists"):
        approval.write_live_ticker_validation_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED == (
        approval.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_APPROVED
    )
    assert services.LIVE_TICKER_VALIDATION_APPROVED == approval.LIVE_TICKER_VALIDATION_APPROVED
    assert services.REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_LIVE_TICKER_VALIDATION_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_live_ticker_validation_approval_attestation_v1 is (
        approval.build_live_ticker_validation_approval_attestation_v1
    )
    assert services.build_live_ticker_validation_approved_v1 is (
        approval.build_live_ticker_validation_approved_v1
    )
    assert services.validate_live_ticker_validation_approved_v1 is (
        approval.validate_live_ticker_validation_approved_v1
    )
    assert services.write_live_ticker_validation_approved_v1 is (
        approval.write_live_ticker_validation_approved_v1
    )
    assert services.build_live_ticker_validation_approved_markdown_v1 is (
        approval.build_live_ticker_validation_approved_markdown_v1
    )
    assert services.live_ticker_validation_approval_digest_v1 is (
        approval.live_ticker_validation_approval_digest_v1
    )
