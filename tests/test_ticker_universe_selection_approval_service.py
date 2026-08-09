from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import ticker_universe_selection_approval_service as approval


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-09T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_candidate_digest": (
            approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "operator_confirms_candidate_review_package_digest": (
            approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_scope_expansion_review_digest": (
            approval.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_approved_ticker_universe": (
            approval.APPROVED_EXPANDED_TICKER_UNIVERSE
        ),
        "operator_confirms_approved_ticker_count": len(
            approval.APPROVED_EXPANDED_TICKER_UNIVERSE
        ),
    }
    values.update({field: True for field in approval.OPERATOR_CONFIRMATION_FIELDS})
    values.update(overrides)
    return approval.build_ticker_universe_selection_approval_attestation_v1(**values)


def _artifact(**attestation_overrides: Any) -> dict[str, Any]:
    return approval.build_ticker_universe_selection_approved_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def _redigest(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["approval_checklist"] = approval._approval_checklist(artifact)
    artifact["approval_summary"] = approval._summary(artifact["approval_checklist"])
    artifact["ticker_universe_selection_approval_digest"] = (
        approval.ticker_universe_selection_approval_digest_v1(artifact)
    )
    return artifact


def test_approval_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("approval must not rebuild candidate with provider access")

    monkeypatch.setattr(
        approval.candidate_review.candidate_service,
        "build_ticker_universe_selection_candidate_v1",
        fail_if_called,
    )

    artifact = _artifact()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False


def test_artifact_kind_and_status_are_approved():
    artifact = _artifact()

    assert artifact["artifact_kind"] == approval.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED
    assert artifact["approval_status"] == approval.TICKER_UNIVERSE_SELECTION_APPROVED


def test_approval_scope_is_exact_future_validation_and_authority_chain_planning_only():
    artifact = _artifact()

    assert artifact["approval_scope"] == (
        approval.TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY
    )
    assert artifact["approval_entry_scope"] == (
        approval.FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY
    )


def test_approved_expanded_ticker_universe_matches_required_list_and_count():
    artifact = _artifact()

    assert artifact["approved_expanded_ticker_universe"] == [
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
    assert artifact["approved_expanded_ticker_count"] == 12
    assert artifact["expanded_ticker_universe_approved"] is True
    assert artifact["ticker_universe_selection_approved"] is True


def test_source_candidate_and_review_package_digests_are_bound():
    artifact = _artifact()

    assert artifact["source_candidate_digest"] == (
        approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
    )
    assert artifact["source_candidate_review_package_digest"] == (
        approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        approval.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
    )


def test_source_review_package_zero_blockers_are_preserved():
    artifact = _artifact()

    assert artifact["source_candidate_review_checklist_total"] == (
        approval.EXPECTED_REVIEW_CHECKLIST_TOTAL
    )
    assert artifact["source_candidate_review_checklist_passed"] == (
        approval.EXPECTED_REVIEW_CHECKLIST_PASSED
    )
    assert artifact["source_candidate_review_checklist_failed"] == 0
    assert artifact["source_candidate_review_blocker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "scope_expansion_authorized",
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
        "provider_requests_made",
        "provider_requests_made_in_approval",
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
        "live_ticker_validation_artifact_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ],
)
def test_downstream_authorization_execution_and_artifact_flags_remain_false(field: str):
    assert _artifact()[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed():
    artifact = _artifact()

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_use"] == approval.NOT_AUTHORIZED
    assert artifact["strategy_use"] == approval.NOT_AUTHORIZED
    assert artifact["paper_trading"] == approval.NOT_AUTHORIZED
    assert artifact["broker_execution"] == approval.NOT_AUTHORIZED


def test_approved_entries_keep_live_validation_and_listing_unverified():
    entries = _artifact()["approved_ticker_entries"]

    assert len(entries) == 12
    assert {entry["selection_approved"] for entry in entries} == {True}
    assert {entry["approval_entry_scope"] for entry in entries} == {
        approval.FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY
    }
    assert {entry["live_validation_status"] for entry in entries} == {approval.NOT_PERFORMED}
    assert {entry["listing_status"] for entry in entries} == {approval.NOT_VERIFIED}
    assert {entry["security_type_status"] for entry in entries} == {approval.NOT_VERIFIED}
    assert {entry["exchange_status"] for entry in entries} == {approval.NOT_VERIFIED}


def test_approved_entries_keep_authority_statuses_not_created():
    entries = _artifact()["approved_ticker_entries"]

    for field in (
        "identity_authority_status",
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {approval.NOT_CREATED}


def test_approved_entries_keep_runtime_and_execution_uses_not_authorized():
    entries = _artifact()["approved_ticker_entries"]

    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "broker_execution",
        "paper_trading",
    ):
        assert {entry[field] for entry in entries} == {approval.NOT_AUTHORIZED}


def test_attestation_contains_required_exact_phrase_and_confirmations():
    attestation = _attestation()

    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_confirms_approved_ticker_universe"] == (
        approval.APPROVED_EXPANDED_TICKER_UNIVERSE
    )
    assert all(attestation[field] is True for field in approval.OPERATOR_CONFIRMATION_FIELDS)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "APPROVE_RUNTIME_MIGRATION"),
        ("operator_attestation_phrase", "APPROVE SOMETHING ELSE"),
        ("operator_confirms_candidate_digest", "0" * 64),
        ("operator_confirms_candidate_review_package_digest", "0" * 64),
        ("operator_confirms_scope_expansion_review_digest", "0" * 64),
        ("operator_confirms_approved_ticker_universe", ["MSFT"]),
        ("operator_confirms_approved_ticker_count", 11),
    ],
)
def test_builder_rejects_wrong_attestation_bindings(field: str, value: Any):
    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        _artifact(**{field: value})


@pytest.mark.parametrize("field", approval.OPERATOR_CONFIRMATION_FIELDS)
def test_builder_rejects_missing_operator_boundary_confirmation(field: str):
    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        _artifact(**{field: False})


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _artifact()["approval_checklist"]] == (
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )


def test_all_approval_checks_pass():
    assert {item["status"] for item in _artifact()["approval_checklist"]} == {approval.PASS}


def test_summary_counts_and_readiness_are_approval_only():
    summary = _artifact()["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ticker_universe_selection_approved_by_operator"] is True
    assert summary["ready_for_live_ticker_validation_candidate"] is True
    assert summary["live_ticker_validation_authorized"] is False
    assert summary["new_ticker_authority_authorized"] is False
    assert summary["acquisition_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_approval_digest_is_deterministic_and_expected():
    assert _artifact()["ticker_universe_selection_approval_digest"] == (
        "e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c"
    )


def test_validator_accepts_valid_approval_artifact():
    validation = approval.validate_ticker_universe_selection_approved_v1(_artifact())

    assert validation["status"] == "TICKER_UNIVERSE_SELECTION_APPROVED_VALID"
    assert validation["ticker_universe_selection_approved"] is True
    assert validation["live_ticker_validation_authorized"] is False


@pytest.mark.parametrize(
    "field",
    [
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_approval",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    artifact = deepcopy(_artifact())
    artifact[field] = True

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


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
def test_validator_rejects_forbidden_authorization_values(field: str, value: str):
    artifact = deepcopy(_artifact())
    artifact[field] = value

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_artifact_kind_mismatch():
    artifact = deepcopy(_artifact())
    artifact["artifact_kind"] = "WRONG"

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_approval_scope_mismatch():
    artifact = deepcopy(_artifact())
    artifact["approval_scope"] = "TICKER_UNIVERSE_APPROVED_FOR_RUNTIME"
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_missing_approved_ticker():
    artifact = deepcopy(_artifact())
    artifact["approved_expanded_ticker_universe"] = artifact[
        "approved_expanded_ticker_universe"
    ][:-1]
    artifact["approved_expanded_ticker_count"] = 11
    artifact["approved_ticker_entries"] = artifact["approved_ticker_entries"][:-1]
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_aapl_in_approved_universe():
    artifact = deepcopy(_artifact())
    artifact["approved_expanded_ticker_universe"][0] = "AAPL"
    artifact["approved_ticker_entries"][0]["ticker"] = "AAPL"
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_approved_entry_live_validation_performed():
    artifact = deepcopy(_artifact())
    artifact["approved_ticker_entries"][0]["live_validation_status"] = "PERFORMED"
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_approved_entry_authority_created():
    artifact = deepcopy(_artifact())
    artifact["approved_ticker_entries"][0]["identity_authority_status"] = "CREATED"
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_runtime_authorized_on_approved_entry():
    artifact = deepcopy(_artifact())
    artifact["approved_ticker_entries"][0]["runtime_use"] = "AUTHORIZED"

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_validator_rejects_modified_source_review_package_digest():
    artifact = deepcopy(_artifact())
    artifact["source_candidate_review_package_digest"] = "0" * 64
    _redigest(artifact)

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.validate_ticker_universe_selection_approved_v1(artifact)


def test_builder_rejects_invalid_source_review_package():
    review_package = (
        approval.candidate_review.build_ticker_universe_selection_candidate_review_package_v1()
    )
    review_package["review_status"] = "TICKER_UNIVERSE_SELECTION_APPROVED"

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.build_ticker_universe_selection_approved_v1(
            operator_attestation=_attestation(),
            ticker_universe_selection_candidate_review_package=review_package,
        )


def test_markdown_writer_includes_required_sections():
    markdown = approval.build_ticker_universe_selection_approved_markdown_v1(_artifact())

    for section in [
        "## Title",
        "## Approved Ticker Universe",
        "## Operator Attestation",
        "## Source Review Package",
        "## Source Scope Expansion Evidence",
        "## Authority Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "ticker_universe_selection_approved_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(approval.TickerUniverseSelectionApprovalError):
        approval.write_ticker_universe_selection_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = approval.write_ticker_universe_selection_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert result["filename"] == "ticker_universe_selection_approved_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED == (
        approval.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED
    )
    assert services.TICKER_UNIVERSE_SELECTION_APPROVED == (
        approval.TICKER_UNIVERSE_SELECTION_APPROVED
    )
    assert services.REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.APPROVED_EXPANDED_TICKER_UNIVERSE == (
        approval.APPROVED_EXPANDED_TICKER_UNIVERSE
    )
    assert services.build_ticker_universe_selection_approval_attestation_v1 is (
        approval.build_ticker_universe_selection_approval_attestation_v1
    )
    assert services.build_ticker_universe_selection_approved_v1 is (
        approval.build_ticker_universe_selection_approved_v1
    )
    assert services.validate_ticker_universe_selection_approved_v1 is (
        approval.validate_ticker_universe_selection_approved_v1
    )
    assert services.write_ticker_universe_selection_approved_v1 is (
        approval.write_ticker_universe_selection_approved_v1
    )
