from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import split_provider_evidence_request_approval_service as approval


def _attestation(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-11T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_split_candidate_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_split_candidate_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "operator_confirms_dividend_candidate_review_package_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_corporate_action_plan_approval_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "operator_confirms_identity_freeze_digest": (
            approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_target_universe": approval.VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
    }
    values.update({field: True for field in approval.OPERATOR_CONFIRMATION_FIELDS})
    values.update(overrides)
    return approval.build_split_provider_evidence_request_approval_attestation_v1(
        **values
    )


def _approved(**attestation_overrides: Any) -> dict[str, Any]:
    return approval.build_split_provider_evidence_request_approved_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def _mutated(field: str, value: Any) -> dict[str, Any]:
    artifact = _approved()
    artifact[field] = value
    return artifact


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_SPLIT_PROVIDER_EVIDENCE_REQUEST
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_confirms_split_candidate_review_package_digest"] == (
        approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert attestation["operator_confirms_target_universe"] == (
        approval.VALIDATION_TARGET_UNIVERSE
    )
    for field in approval.OPERATOR_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_approval_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_provider_call(*_args: Any, **_kwargs: Any) -> None:  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        approval.split_review.candidate_service.approval.review.plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


def test_artifact_kind_status_and_scope_are_exact():
    artifact = _approved()

    assert artifact["artifact_kind"] == (
        approval.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert artifact["approval_status"] == approval.SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    assert artifact["approval_scope"] == (
        approval.READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY
    )


def test_split_provider_request_is_authorized_but_not_executed():
    artifact = _approved()

    assert artifact["split_provider_evidence_request_authorized"] is True
    assert artifact["ready_for_split_provider_evidence_execution"] is True
    assert artifact["split_provider_evidence_executed"] is False
    assert artifact["split_provider_evidence_results_created"] is False
    assert artifact["split_event_authority_created"] is False
    assert artifact["split_event_authority_frozen"] is False


def test_dividend_corporate_action_acquisition_dataset_and_runtime_remain_closed():
    artifact = _approved()

    assert artifact["dividend_provider_evidence_request_authorized"] is False
    assert artifact["dividend_event_authority_created"] is False
    assert artifact["corporate_action_authority_created"] is False
    assert artifact["new_ticker_acquisition_authorized"] is False
    assert artifact["dataset_generation_authorized"] is False
    assert artifact["acquisition_generation_authorized"] is False
    assert artifact["canonical_dataset_authorized"] is False
    assert artifact["registry_approval_created"] is False
    assert artifact["additional_predictive_evidence_execution_authorized"] is False
    assert artifact["additional_predictive_evidence_executed"] is False
    assert artifact["predictive_usefulness"] == (
        approval.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert artifact["profitability"] == approval.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_use"] == approval.split_review.candidate_service.NOT_AUTHORIZED
    assert artifact["strategy_use"] == approval.split_review.candidate_service.NOT_AUTHORIZED
    assert artifact["paper_trading"] == approval.split_review.candidate_service.NOT_AUTHORIZED
    assert artifact["broker_execution"] == approval.split_review.candidate_service.NOT_AUTHORIZED


def test_source_digest_chain_is_bound():
    artifact = _approved()

    assert artifact["split_event_authority_candidate_review_package_digest"] == (
        approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["split_event_authority_candidate_digest"] == (
        approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )
    assert artifact["dividend_event_authority_candidate_review_package_digest"] == (
        approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["dividend_event_authority_candidate_digest"] == (
        approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
    )
    assert artifact["corporate_action_authority_plan_approval_digest"] == (
        approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
    )
    assert artifact["post_identity_freeze_registry_inventory_approval_digest"] == (
        approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert artifact["identity_authority_freeze_digest"] == (
        approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )


def test_target_universe_objective_scope_and_read_only_policy_are_exact():
    artifact = _approved()

    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == approval.VALIDATION_TARGET_UNIVERSE
    assert artifact["split_provider_evidence_request_objective"] == (
        approval.SPLIT_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE
    )
    assert artifact["split_provider_evidence_request_scope"] == (
        approval.SPLIT_PROVIDER_EVIDENCE_REQUEST_SCOPE
    )
    assert artifact["split_provider_evidence_authority_scope"] == (
        approval.SPLIT_PROVIDER_EVIDENCE_AUTHORITY_SCOPE
    )
    assert artifact["split_provider_evidence_execution_status"] == approval.NOT_EXECUTED
    assert artifact["read_only_request_policy"] == approval.READ_ONLY_REQUEST_POLICY


def test_per_ticker_request_approval_entries_are_authorized_not_executed():
    entries = _approved()["per_ticker_split_provider_evidence_request_approval_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == approval.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["split_event_candidate_status"] == (
            approval.split_review.candidate_service.SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["split_event_review_status"] == approval.split_review.READY_FOR_OPERATOR_ASSESSMENT
        assert entry["split_provider_evidence_request_status"] == (
            approval.AUTHORIZED_NOT_EXECUTED
        )
        assert entry["split_provider_evidence_execution_status"] == approval.NOT_EXECUTED
        assert entry["split_provider_evidence_results_status"] == approval.NOT_CREATED
        assert entry["split_event_authority_status"] == (
            approval.split_review.candidate_service.NOT_CREATED
        )
        assert entry["split_event_freeze_status"] == (
            approval.split_review.candidate_service.NOT_FROZEN
        )
        assert entry["dividend_event_authority_status"] == approval.NOT_CREATED
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authorized"] is False
        assert entry["dataset_generation_authorized"] is False
        assert len(entry["source_split_event_candidate_digest"]) == 64
        assert len(entry["source_split_event_review_digest"]) == 64
        assert len(entry["source_corporate_action_plan_approval_digest"]) == 64
        assert entry["per_ticker_split_provider_evidence_request_approval_digest"] == (
            approval.per_ticker_split_provider_evidence_request_approval_digest_v1(
                entry
            )
        )


def test_planned_outputs_are_not_generated_and_research_only():
    artifact = _approved()

    assert artifact["planned_output_count"] == 6
    assert [item["output_name"] for item in artifact["planned_outputs"]] == (
        approval.PLANNED_SPLIT_EVIDENCE_OUTPUT_NAMES
    )
    assert {item["generation_status"] for item in artifact["planned_outputs"]} == {
        approval.PLANNED_NOT_GENERATED
    }
    assert {item["generated"] for item in artifact["planned_outputs"]} == {False}
    assert {item["actionability"] for item in artifact["planned_outputs"]} == {
        approval.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_checklist_summary_and_validator_accept_valid_artifact():
    artifact = _approved()
    validation = approval.validate_split_provider_evidence_request_approved_v1(
        artifact
    )

    assert [item["check_id"] for item in artifact["approval_checklist"]] == (
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert {item["status"] for item in artifact["approval_checklist"]} == {
        approval.PASS
    }
    assert artifact["approval_summary"]["total_checks"] == len(
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert artifact["approval_summary"]["passed_checks"] == len(
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert artifact["approval_summary"]["failed_checks"] == 0
    assert artifact["approval_summary"]["blocker_count"] == 0
    assert validation["status"] == "SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID"
    assert validation["split_provider_evidence_request_authorized_by_operator"] is True
    assert validation["ready_for_split_provider_evidence_execution"] is True
    assert validation["split_provider_evidence_executed"] is False
    assert validation["split_event_authority_authorized"] is False
    assert validation["dividend_provider_evidence_request_authorized"] is False
    assert validation["corporate_action_authority_authorized"] is False


@pytest.mark.parametrize(
    ("override", "value", "match"),
    [
        ("operator_decision", "WRONG", "operator_decision_approved"),
        ("operator_attestation_phrase", "WRONG", "operator_attestation_phrase"),
        ("operator_confirms_split_candidate_review_package_digest", "0" * 64, "split_candidate_review_digest"),
        ("operator_confirms_split_candidate_digest", "0" * 64, "split_candidate_digest"),
        ("operator_confirms_dividend_candidate_review_package_digest", "0" * 64, "dividend_candidate_review_digest"),
        ("operator_confirms_corporate_action_plan_approval_digest", "0" * 64, "corporate_action_plan_approval_digest"),
        ("operator_confirms_registry_inventory_approval_digest", "0" * 64, "registry_inventory_approval_digest"),
        ("operator_confirms_identity_freeze_digest", "0" * 64, "identity_freeze_digest"),
        ("operator_confirms_target_universe", ["MSFT"], "target_universe"),
        ("operator_confirms_target_count", 11, "target_count"),
        ("operator_confirms_request_scope_read_only_split_event_evidence_only", False, "request_scope"),
        ("operator_confirms_ready_for_split_provider_evidence_execution", False, "ready_for_split_provider_evidence_execution"),
        ("operator_confirms_no_provider_requests_made_in_approval", False, "no_provider_requests"),
        ("operator_confirms_no_live_provider_transport_enabled", False, "no_live_provider_transport"),
        ("operator_confirms_no_split_provider_evidence_executed", False, "no_split_provider_evidence_executed"),
        ("operator_confirms_no_split_provider_evidence_results_created", False, "no_split_provider_evidence_results_created"),
        ("operator_confirms_no_split_event_authority_created", False, "no_split_event_authority_created"),
        ("operator_confirms_no_split_event_authority_frozen", False, "no_split_event_authority_frozen"),
        ("operator_confirms_no_dividend_provider_evidence_request_authorized", False, "no_dividend_provider_evidence_request_authorized"),
        ("operator_confirms_no_dividend_event_authority_created", False, "no_dividend_event_authority_created"),
        ("operator_confirms_no_corporate_action_authority_created", False, "no_corporate_action_authority_created"),
        ("operator_confirms_no_acquisition_authority", False, "no_acquisition_authority"),
        ("operator_confirms_no_dataset_generation_authorization", False, "no_dataset_generation_authorization"),
        ("operator_confirms_no_predictive_usefulness_acceptance", False, "no_predictive_usefulness_acceptance"),
        ("operator_confirms_no_profitability_acceptance", False, "no_profitability_acceptance"),
        ("operator_confirms_no_runtime_migration_approval", False, "no_runtime_migration_approval"),
        ("operator_confirms_no_runtime_activation", False, "no_runtime_activation"),
        ("operator_confirms_no_paper_trading", False, "no_paper_trading"),
        ("operator_confirms_no_broker_execution", False, "no_broker_execution"),
        ("operator_confirms_no_trade_recommendations", False, "no_trade_recommendations"),
        ("operator_confirms_no_api_key_storage_or_printing", False, "no_api_key_storage_or_printing"),
        ("operator_confirms_no_raw_payload_commit", False, "no_raw_payload_commit"),
    ],
)
def test_wrong_or_missing_operator_attestation_values_are_rejected(
    override: str, value: Any, match: str
):
    with pytest.raises(
        approval.SplitProviderEvidenceRequestApprovalError,
        match=match,
    ):
        _approved(**{override: value})


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "SPLIT_EVENT_AUTHORITY_APPROVED", "artifact_kind"),
        ("approval_status", "WRONG", "approval_status"),
        ("approval_scope", "WRONG", "approval_scope"),
        ("split_provider_evidence_request_authorized", False, "split_provider_evidence_request_authorized"),
        ("ready_for_split_provider_evidence_execution", False, "ready_for_split_provider_evidence_execution"),
        ("provider_requests_made_in_approval", True, "provider_requests_made_in_approval"),
        ("live_provider_transport_enabled_in_approval", True, "live_provider_transport_enabled_in_approval"),
        ("split_provider_evidence_executed", True, "split_provider_evidence_executed"),
        ("split_provider_evidence_results_created", True, "split_provider_evidence_results_created"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("split_event_authority_frozen", True, "split_event_authority_frozen"),
        ("dividend_provider_evidence_request_authorized", True, "dividend_provider_evidence_request_authorized"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("target_universe_count", 11, "target_universe_count"),
        ("target_universe", ["MSFT"], "target_universe"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("acquisition_generation_authorized", True, "acquisition_generation_authorized"),
        ("canonical_dataset_authorized", True, "canonical_dataset_authorized"),
        ("registry_approval_created", True, "registry_approval_created"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("additional_predictive_evidence_executed", True, "additional_predictive_evidence_executed"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
    ],
)
def test_validator_rejects_invalid_top_level_mutations(
    field: str, value: Any, match: str
):
    artifact = _mutated(field, value)

    with pytest.raises(
        approval.SplitProviderEvidenceRequestApprovalError,
        match=match,
    ):
        approval.validate_split_provider_evidence_request_approved_v1(artifact)


def test_validator_rejects_missing_per_ticker_approval_digest():
    artifact = _approved()
    artifact["per_ticker_split_provider_evidence_request_approval_entries"][0].pop(
        "per_ticker_split_provider_evidence_request_approval_digest"
    )

    with pytest.raises(
        approval.SplitProviderEvidenceRequestApprovalError,
        match="request_approval_digest",
    ):
        approval.validate_split_provider_evidence_request_approved_v1(artifact)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _approved()
    second = _approved()

    assert first["split_provider_evidence_request_approval_digest"] == (
        second["split_provider_evidence_request_approval_digest"]
    )
    assert first["split_provider_evidence_request_approval_digest"] == (
        approval.split_provider_evidence_request_approval_digest_v1(first)
    )
    assert [
        entry["per_ticker_split_provider_evidence_request_approval_digest"]
        for entry in first["per_ticker_split_provider_evidence_request_approval_entries"]
    ] == [
        entry["per_ticker_split_provider_evidence_request_approval_digest"]
        for entry in second["per_ticker_split_provider_evidence_request_approval_entries"]
    ]


def test_remaining_roadmap_contains_required_follow_on_tasks():
    roadmap = _approved()["remaining_roadmap"]

    for item in (
        "Split provider evidence execution.",
        "Split event evidence/results review package.",
        "Split event authority freeze ceremony.",
        "Dividend provider evidence request approval ceremony.",
        "Dividend provider evidence execution.",
        "Dividend event authority freeze ceremony.",
    ):
        assert item in roadmap


def test_markdown_includes_required_sections_and_guardrails():
    markdown = approval.build_split_provider_evidence_request_approved_markdown_v1(
        _approved()
    )

    for section in (
        "## Title",
        "## Approved Split Provider Evidence Request",
        "## Operator Attestation",
        "## Source Split Candidate Review Package",
        "## Source Dividend Candidate Review Package",
        "## Target Universe",
        "## Approval Scope",
        "## Read-Only Provider Request Boundary",
        "## Split Evidence Execution Boundary",
        "## Split Authority Boundary",
        "## Dividend Boundary",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_approval_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = approval.write_split_provider_evidence_request_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert result["artifact_kind"] == (
        approval.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert result["payload_sha256"]
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written["artifact_kind"] == (
        approval.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    with pytest.raises(
        approval.SplitProviderEvidenceRequestApprovalError,
        match="already exists",
    ):
        approval.write_split_provider_evidence_request_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_services_package_exports_approval_helpers():
    artifact = _approved()
    first_entry = artifact[
        "per_ticker_split_provider_evidence_request_approval_entries"
    ][0]

    assert services.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED == (
        approval.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert services.SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED == (
        approval.SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVED
    )
    assert services.REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_split_provider_evidence_request_approved_v1 is (
        approval.build_split_provider_evidence_request_approved_v1
    )
    assert services.validate_split_provider_evidence_request_approved_v1 is (
        approval.validate_split_provider_evidence_request_approved_v1
    )
    assert services.write_split_provider_evidence_request_approved_v1 is (
        approval.write_split_provider_evidence_request_approved_v1
    )
    assert services.split_provider_evidence_request_approval_digest_v1(artifact) == (
        artifact["split_provider_evidence_request_approval_digest"]
    )
    assert services.per_ticker_split_provider_evidence_request_approval_digest_v1(
        first_entry
    ) == first_entry["per_ticker_split_provider_evidence_request_approval_digest"]
