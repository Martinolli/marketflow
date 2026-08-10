from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import post_identity_freeze_registry_inventory_approval_service as approval


EXPECTED_APPROVAL_DIGEST = (
    "c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82"
)


def _attestation(**overrides: Any) -> dict[str, Any]:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-10T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_registry_inventory_candidate_review_package_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_registry_inventory_candidate_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        ),
        "operator_confirms_identity_freeze_digest": (
            approval.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "operator_confirms_identity_authority_scope_identity_only": True,
        "operator_confirms_target_universe": approval.VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_registry_inventory_scope_identity_inventory_only": True,
        "operator_confirms_registry_inventory_entries_reviewed": True,
        "operator_confirms_no_provider_requests_in_approval": True,
        "operator_confirms_no_live_validation_rerun": True,
        "operator_confirms_no_live_provider_transport_enabled": True,
        "operator_confirms_no_corporate_action_authority": True,
        "operator_confirms_no_split_event_authority": True,
        "operator_confirms_no_dividend_event_authority": True,
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
    return approval.build_post_identity_freeze_registry_inventory_approval_attestation_v1(
        **values
    )


def _artifact(**attestation_overrides: Any) -> dict[str, Any]:
    return approval.build_post_identity_freeze_registry_inventory_approved_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_V1
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_target_universe"] == approval.VALIDATION_TARGET_UNIVERSE
    assert attestation["operator_confirms_target_count"] == 12
    for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        approval.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    artifact = _artifact()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_validation_rerun_performed"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


def test_artifact_kind_status_scope_and_digest_are_exact():
    artifact = _artifact()

    assert artifact["artifact_kind"] == (
        approval.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED
    )
    assert artifact["approval_status"] == approval.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED
    assert artifact["approval_scope"] == approval.IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY
    assert artifact["post_identity_freeze_registry_inventory_approval_digest"] == (
        EXPECTED_APPROVAL_DIGEST
    )
    assert artifact["post_identity_freeze_registry_inventory_approved"] is True


def test_source_evidence_digests_are_bound():
    artifact = _artifact()

    assert artifact["post_identity_freeze_registry_inventory_candidate_review_package_digest"] == (
        approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["post_identity_freeze_registry_inventory_candidate_digest"] == (
        approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
    )
    assert artifact["identity_authority_freeze_digest"] == (
        approval.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert artifact["identity_authority_candidate_review_package_digest"] == (
        approval.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["identity_authority_candidate_digest"] == (
        approval.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert artifact["live_ticker_validation_results_review_package_digest"] == (
        approval.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["ticker_universe_selection_approval_digest"] == (
        approval.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_identity_and_approval_scope_are_preserved():
    artifact = _artifact()

    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == approval.VALIDATION_TARGET_UNIVERSE
    assert artifact["frozen_identity_universe"] == approval.VALIDATION_TARGET_UNIVERSE
    assert artifact["identity_authority_frozen"] is True
    assert artifact["authority_scope"] == (
        approval.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
    )
    assert artifact["registry_inventory_objective"] == (
        approval.review_service.candidate_service.REGISTRY_INVENTORY_OBJECTIVE
    )
    assert artifact["registry_inventory_scope"] == (
        approval.review_service.candidate_service.REGISTRY_INVENTORY_SCOPE
    )
    assert artifact["registry_inventory_approval_status"] == approval.APPROVED


def test_per_ticker_inventory_approval_entries_are_approved_and_bound():
    artifact = _artifact()
    entries = artifact["per_ticker_registry_inventory_approval_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == approval.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["identity_freeze_status"] == (
            approval.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
        )
        assert entry["identity_authority_scope"] == (
            approval.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
        )
        assert entry["identity_authority_created"] is True
        assert entry["identity_authority_frozen"] is True
        assert entry["registry_inventory_entry_status"] == (
            approval.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        )
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authority_created"] is False
        assert entry["dataset_generation_authorized"] is False
        for field in (
            "source_per_ticker_identity_freeze_digest",
            "source_per_ticker_identity_candidate_digest",
            "source_per_ticker_identity_review_digest",
            "per_ticker_registry_inventory_digest",
            "per_ticker_registry_inventory_review_digest",
            "per_ticker_registry_inventory_approval_digest",
        ):
            assert len(entry[field]) == 64
        assert "frozen_identity_fields_summary" in entry
        assert "unavailable_fields_summary" in entry
        assert "identity_evidence_limitations" in entry


def test_unavailable_fields_remain_unavailable_and_not_fabricated():
    artifact = _artifact()

    for entry in artifact["per_ticker_registry_inventory_approval_entries"]:
        summary = entry["unavailable_fields_summary"]
        assert "provider_canonical_ticker" in summary["unavailable_fields"]
        assert "ticker" in summary["available_fields"]
        assert entry["unavailable_fields_preserved_as_unavailable"] is True


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_approval",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_approval",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
        "corporate_action_authority_artifact_created",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ],
)
def test_closed_boolean_boundaries_remain_false(field: str):
    assert _artifact()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    artifact = _artifact()
    not_authorized = (
        approval.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )

    assert artifact["predictive_usefulness"] == approval.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert artifact["profitability"] == approval.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert artifact["runtime_use"] == not_authorized
    assert artifact["strategy_use"] == not_authorized
    assert artifact["paper_trading"] == not_authorized
    assert artifact["broker_execution"] == not_authorized


def test_checklist_and_summary_counts_are_complete():
    artifact = _artifact()

    assert [item["check_id"] for item in artifact["approval_checklist"]] == (
        approval.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in artifact["approval_checklist"]} == {approval.PASS}
    assert artifact["approval_summary"] == {
        "total_checks": 91,
        "passed_checks": 91,
        "failed_checks": 0,
        "blocker_count": 0,
        "registry_inventory_approved_by_operator": True,
        "approval_scope": approval.IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY,
        "ready_for_corporate_action_authority_plan_candidate": True,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_approval_and_per_ticker_approval_digests_are_deterministic():
    first = _artifact()
    second = _artifact()

    assert first["post_identity_freeze_registry_inventory_approval_digest"] == (
        second["post_identity_freeze_registry_inventory_approval_digest"]
    )
    assert [
        entry["per_ticker_registry_inventory_approval_digest"]
        for entry in first["per_ticker_registry_inventory_approval_entries"]
    ] == [
        entry["per_ticker_registry_inventory_approval_digest"]
        for entry in second["per_ticker_registry_inventory_approval_entries"]
    ]


def test_validator_accepts_valid_approval_artifact():
    validation = approval.validate_post_identity_freeze_registry_inventory_approved_v1(
        _artifact()
    )

    assert validation["status"] == "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED_VALID"
    assert validation["blocker_count"] == 0
    assert validation["registry_inventory_approved_by_operator"] is True
    assert validation["ready_for_corporate_action_authority_plan_candidate"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_attestation_phrase", "WRONG"),
        ("operator_decision", "REJECT"),
        ("operator_confirms_registry_inventory_candidate_review_package_digest", "0" * 64),
        ("operator_confirms_registry_inventory_candidate_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval.VALIDATION_TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_identity_authority_scope_identity_only", False),
        ("operator_confirms_registry_inventory_scope_identity_inventory_only", False),
        ("operator_confirms_registry_inventory_entries_reviewed", False),
        ("operator_confirms_no_provider_requests_in_approval", False),
        ("operator_confirms_no_live_validation_rerun", False),
        ("operator_confirms_no_live_provider_transport_enabled", False),
        ("operator_confirms_no_corporate_action_authority", False),
        ("operator_confirms_no_split_event_authority", False),
        ("operator_confirms_no_dividend_event_authority", False),
        ("operator_confirms_no_acquisition_authority", False),
        ("operator_confirms_no_dataset_generation_authorization", False),
        ("operator_confirms_no_additional_predictive_evidence_execution", False),
        ("operator_confirms_no_predictive_usefulness_acceptance", False),
        ("operator_confirms_no_profitability_acceptance", False),
        ("operator_confirms_no_runtime_migration_approval", False),
        ("operator_confirms_no_runtime_activation", False),
        ("operator_confirms_no_paper_trading", False),
        ("operator_confirms_no_broker_execution", False),
        ("operator_confirms_no_trade_recommendations", False),
        ("operator_confirms_no_api_key_storage_or_printing", False),
        ("operator_confirms_no_raw_payload_commit", False),
    ],
)
def test_wrong_operator_attestation_values_are_rejected(field: str, value: Any):
    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        _artifact(**{field: value})


def test_missing_operator_attestation_is_rejected():
    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.build_post_identity_freeze_registry_inventory_approved_v1(
            operator_attestation=None  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("post_identity_freeze_registry_inventory_approved", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(approval.VALIDATION_TARGET_UNIVERSE))),
        ("identity_authority_frozen", False),
        ("authority_scope", "WRONG"),
    ],
)
def test_validator_rejects_invalid_top_level_fields(field: str, value: Any):
    artifact = _artifact()
    artifact[field] = value

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_registry_inventory_approval_entries",
    ],
)
def test_validator_rejects_missing_per_ticker_approval_entry(field: str):
    artifact = _artifact()
    artifact[field] = artifact[field][:-1]

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


@pytest.mark.parametrize(
    "field",
    [
        "source_per_ticker_identity_freeze_digest",
        "source_per_ticker_identity_candidate_digest",
        "source_per_ticker_identity_review_digest",
        "per_ticker_registry_inventory_digest",
        "per_ticker_registry_inventory_review_digest",
        "per_ticker_registry_inventory_approval_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(field: str):
    artifact = _artifact()
    artifact["per_ticker_registry_inventory_approval_entries"][0].pop(field)

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


def test_validator_rejects_unavailable_field_fabricated():
    artifact = _artifact()
    artifact["per_ticker_registry_inventory_approval_entries"][0]["unavailable_fields_summary"][
        "unavailable_fields"
    ] = "fabricated"

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_approval",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_approval",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    artifact = _artifact()
    artifact[field] = True

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


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
def test_validator_rejects_accepted_or_authorized_values(field: str, value: str):
    artifact = _artifact()
    artifact[field] = value

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


def test_validator_rejects_approval_digest_mismatch():
    artifact = _artifact()
    artifact["post_identity_freeze_registry_inventory_approval_digest"] = "0" * 64

    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)


def test_remaining_roadmap_preserves_downstream_future_tasks():
    artifact = _artifact()

    assert artifact["future_chain"] == [
        "Corporate-action authority plan candidate.",
        "Split event authority candidate/review/freeze per ticker.",
        "Dividend event authority candidate/review/freeze per ticker.",
        "Acquisition generation candidate only after identity and corporate-action authority.",
        "Canonical dataset candidate only after acquisition generation freeze.",
        "Research registry approval only after canonical dataset freeze.",
    ]


def test_markdown_includes_required_sections_and_guardrails():
    markdown = approval.build_post_identity_freeze_registry_inventory_approved_markdown_v1(
        _artifact()
    )

    for section in [
        "## Approved Post-Identity-Freeze Registry Inventory",
        "## Operator Attestation",
        "## Source Registry Inventory Review Package",
        "## Source Identity Freeze",
        "## Target Universe",
        "## Approved Per-Ticker Identity Registry Inventory",
        "## Preserved Unavailable Fields and Limitations",
        "## Approval Scope",
        "## Corporate-Action Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
        "No Massive.com / Polygon provider request was made.",
    ]:
        assert section in markdown


def test_write_approval_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = approval.write_post_identity_freeze_registry_inventory_approved_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert Path(result["path"]).exists()
    assert result["filename"] == "post_identity_freeze_registry_inventory_approved_v1.json"
    assert result["post_identity_freeze_registry_inventory_approval_digest"] == (
        EXPECTED_APPROVAL_DIGEST
    )
    with pytest.raises(approval.PostIdentityFreezeRegistryInventoryApprovalError):
        approval.write_post_identity_freeze_registry_inventory_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_services_package_exports_approval_helpers():
    from marketflow import services

    assert services.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED == (
        approval.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED
    )
    assert services.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED == (
        approval.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED
    )
    assert services.REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE == (
        approval.REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE
    )
    assert services.build_post_identity_freeze_registry_inventory_approval_attestation_v1 is (
        approval.build_post_identity_freeze_registry_inventory_approval_attestation_v1
    )
    assert services.build_post_identity_freeze_registry_inventory_approved_v1 is (
        approval.build_post_identity_freeze_registry_inventory_approved_v1
    )
    assert services.validate_post_identity_freeze_registry_inventory_approved_v1 is (
        approval.validate_post_identity_freeze_registry_inventory_approved_v1
    )
    assert services.write_post_identity_freeze_registry_inventory_approved_v1 is (
        approval.write_post_identity_freeze_registry_inventory_approved_v1
    )
