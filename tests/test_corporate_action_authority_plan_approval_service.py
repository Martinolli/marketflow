from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import corporate_action_authority_plan_approval_service as approval


def _attestation(**overrides: Any) -> dict[str, Any]:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-11T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_corporate_action_plan_review_package_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_corporate_action_plan_candidate_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "operator_confirms_identity_freeze_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_target_universe": approval.review.VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_plan_approval_scope_only": True,
        "operator_confirms_ready_for_split_event_authority_candidate": True,
        "operator_confirms_ready_for_dividend_event_authority_candidate": True,
        "operator_confirms_no_provider_requests_in_approval": True,
        "operator_confirms_no_live_validation_rerun": True,
        "operator_confirms_no_live_provider_transport": True,
        "operator_confirms_no_corporate_action_authority_created": True,
        "operator_confirms_no_split_authority_created": True,
        "operator_confirms_no_dividend_authority_created": True,
        "operator_confirms_no_acquisition_authority": True,
        "operator_confirms_no_dataset_generation_authorization": True,
        "operator_confirms_no_additional_predictive_evidence_execution": True,
        "operator_confirms_no_predictive_usefulness_acceptance": True,
        "operator_confirms_no_profitability_acceptance": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_runtime_activation": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_trade_recommendations": True,
        "operator_confirms_no_api_key_storage_or_printing": True,
        "operator_confirms_no_raw_payload_commit": True,
    }
    values.update(overrides)
    return approval.build_corporate_action_authority_plan_approval_attestation_v1(
        **values
    )


def _approved() -> dict[str, Any]:
    return approval.build_corporate_action_authority_plan_approved_v1(
        operator_attestation=_attestation()
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert (
        attestation["operator_decision"]
        == approval.OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN
    )
    assert (
        attestation["operator_attestation_phrase"]
        == approval.REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE
    )
    assert (
        attestation["operator_confirms_corporate_action_plan_review_package_digest"]
        == approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert (
        attestation["operator_confirms_corporate_action_plan_candidate_digest"]
        == approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )


def test_approved_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        approval.review.plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_validation_rerun_performed"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


def test_artifact_kind_status_and_scope_are_exact():
    artifact = _approved()

    assert (
        artifact["artifact_kind"]
        == approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED
    )
    assert artifact["approval_status"] == approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED
    assert artifact["approval_scope"] == approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY


def test_plan_approval_sets_only_plan_readiness_flags_true():
    artifact = _approved()

    assert artifact["corporate_action_authority_plan_approved"] is True
    assert artifact["ready_for_split_event_authority_candidate"] is True
    assert artifact["ready_for_dividend_event_authority_candidate"] is True
    assert artifact["corporate_action_authority_created"] is False
    assert artifact["split_event_authority_candidate_created"] is False
    assert artifact["split_event_authority_created"] is False
    assert artifact["dividend_event_authority_candidate_created"] is False
    assert artifact["dividend_event_authority_created"] is False


def test_source_review_and_candidate_digest_chain_is_bound():
    artifact = _approved()

    assert (
        artifact["source_corporate_action_plan_review_package_digest"]
        == approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert (
        artifact["source_corporate_action_plan_candidate_digest"]
        == approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert (
        artifact["post_identity_freeze_registry_inventory_approval_digest"]
        == approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert (
        artifact["identity_authority_freeze_digest"]
        == approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )


def test_target_universe_plan_objective_and_evidence_requirements_are_preserved():
    artifact = _approved()

    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == approval.review.VALIDATION_TARGET_UNIVERSE
    assert artifact["corporate_action_authority_plan_objective"] == (
        approval.review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE
    )
    assert artifact["corporate_action_authority_plan_scope"] == (
        approval.review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE
    )
    assert artifact["corporate_action_authority_creation_status"] == (
        approval.review.plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS
    )
    assert artifact["corporate_action_evidence_requirements"] == (
        approval.review.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS
    )


def test_per_ticker_approval_entries_bind_source_and_approval_digests():
    entries = _approved()["per_ticker_corporate_action_plan_approval_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == approval.review.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["source_corporate_action_plan_status"] == (
            approval.review.plan.PLANNED_NOT_CREATED
        )
        assert entry["source_corporate_action_plan_review_status"] == (
            approval.review.READY_FOR_OPERATOR_ASSESSMENT
        )
        assert entry["corporate_action_plan_status"] == (
            approval.APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY
        )
        assert entry["split_event_authority_status"] == approval.review.plan.NOT_CREATED
        assert entry["dividend_event_authority_status"] == approval.review.plan.NOT_CREATED
        assert entry["dataset_generation_authorized"] is False
        assert entry["source_per_ticker_corporate_action_plan_digest"] == (
            entry["per_ticker_corporate_action_plan_digest"]
        )
        assert entry["source_per_ticker_corporate_action_plan_review_digest"] == (
            entry["per_ticker_corporate_action_plan_review_digest"]
        )
        assert entry["per_ticker_corporate_action_plan_approval_digest"] == (
            approval.per_ticker_corporate_action_plan_approval_digest_v1(entry)
        )


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_approval",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_approval",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "split_event_authority_candidate_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_forbidden_boolean_fields_must_remain_false(field: str):
    artifact = _approved()
    artifact[field] = True

    with pytest.raises(approval.CorporateActionAuthorityPlanApprovalError):
        approval.validate_corporate_action_authority_plan_approved_v1(artifact)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
    ],
)
def test_authorized_runtime_or_accepted_research_values_are_rejected(
    field: str,
    value: str,
):
    artifact = _approved()
    artifact[field] = value

    with pytest.raises(approval.CorporateActionAuthorityPlanApprovalError):
        approval.validate_corporate_action_authority_plan_approved_v1(artifact)


def test_approval_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _approved()["approval_checklist"]] == (
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )


def test_all_approval_checks_pass_and_summary_counts_are_correct():
    artifact = _approved()
    summary = artifact["approval_summary"]

    assert {item["status"] for item in artifact["approval_checklist"]} == {approval.PASS}
    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["corporate_action_authority_plan_approved_by_operator"] is True
    assert summary["ready_for_split_event_authority_candidate"] is True
    assert summary["ready_for_dividend_event_authority_candidate"] is True
    assert summary["corporate_action_authority_authorized"] is False
    assert summary["acquisition_authorized"] is False
    assert summary["dataset_generation_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_operator_attestation_phrase_must_match_exactly():
    with pytest.raises(
        approval.CorporateActionAuthorityPlanApprovalError,
        match="operator_attestation_phrase_matches",
    ):
        approval.build_corporate_action_authority_plan_approved_v1(
            operator_attestation=_attestation(operator_attestation_phrase="APPROVE")
        )


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(
        approval.CorporateActionAuthorityPlanApprovalError,
        match="operator_decision_approved",
    ):
        approval.build_corporate_action_authority_plan_approved_v1(
            operator_attestation=_attestation(operator_decision="REJECT")
        )


@pytest.mark.parametrize("field", approval.OPERATOR_CONFIRMATION_FIELDS)
def test_operator_boolean_confirmations_must_be_true(field: str):
    with pytest.raises(approval.CorporateActionAuthorityPlanApprovalError, match=field):
        approval.build_corporate_action_authority_plan_approved_v1(
            operator_attestation=_attestation(**{field: False})
        )


def test_wrong_source_review_digest_is_rejected():
    package = approval.review.build_corporate_action_authority_plan_candidate_review_package_v1()
    package["corporate_action_authority_plan_candidate_review_package_digest"] = "0" * 64

    with pytest.raises(approval.CorporateActionAuthorityPlanApprovalError):
        approval.build_corporate_action_authority_plan_approved_v1(
            corporate_action_plan_review_package=package,
            operator_attestation=_attestation(),
        )


def test_mutated_per_ticker_approval_digest_is_rejected():
    artifact = _approved()
    artifact["per_ticker_corporate_action_plan_approval_entries"][0][
        "per_ticker_corporate_action_plan_approval_digest"
    ] = "0" * 64

    with pytest.raises(
        approval.CorporateActionAuthorityPlanApprovalError,
        match="per_ticker_corporate_action_plan_approval_digest",
    ):
        approval.validate_corporate_action_authority_plan_approved_v1(artifact)


def test_approval_digest_is_deterministic_and_validated():
    first = _approved()
    second = _approved()
    validation = approval.validate_corporate_action_authority_plan_approved_v1(first)

    assert first["corporate_action_authority_plan_approval_digest"] == (
        second["corporate_action_authority_plan_approval_digest"]
    )
    assert validation["status"] == "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED_VALID"


def test_markdown_contains_approval_status_and_guardrails():
    markdown = approval.build_corporate_action_authority_plan_approved_markdown_v1(
        _approved()
    )

    assert "# MarketFlow Corporate-Action Authority Plan Approval Status" in markdown
    assert "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY" in markdown
    assert "No corporate-action authority, split authority, or dividend authority was created." in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_writer_emits_json_and_refuses_overwrite(tmp_path: Path):
    result = approval.write_corporate_action_authority_plan_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert result["filename"] == "corporate_action_authority_plan_approved_v1.json"
    assert payload["artifact_kind"] == (
        approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED
    )
    with pytest.raises(approval.CorporateActionAuthorityPlanApprovalError):
        approval.write_corporate_action_authority_plan_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_top_level_services_exports_are_available():
    assert services.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED == (
        approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED
    )
    assert services.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED == (
        approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED
    )
    assert services.REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.corporate_action_authority_plan_approval_digest_v1(_approved()) == (
        _approved()["corporate_action_authority_plan_approval_digest"]
    )
