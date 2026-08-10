from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import post_identity_freeze_registry_inventory_candidate_service as inventory


def _candidate() -> dict[str, Any]:
    return inventory.build_post_identity_freeze_registry_inventory_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        inventory.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["live_validation_rerun_performed"] is False
    assert candidate["live_provider_transport_enabled"] is False


def test_artifact_kind_status_and_digest_are_exact():
    candidate = _candidate()

    assert candidate["artifact_kind"] == (
        inventory.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        inventory.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW
    )
    assert candidate["post_identity_freeze_registry_inventory_candidate_digest"] == (
        "459f20151cf531b32de91defb7d0a676b20ad68a13b4f391840a0e1db921ea34"
    )


def test_source_evidence_digests_are_bound():
    candidate = _candidate()

    assert candidate["identity_authority_freeze_digest"] == (
        inventory.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert candidate["identity_authority_candidate_review_package_digest"] == (
        inventory.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["identity_authority_candidate_digest"] == (
        inventory.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert candidate["identity_authority_plan_candidate_review_package_digest"] == (
        inventory.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["identity_authority_plan_candidate_digest"] == (
        inventory.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert candidate["live_ticker_validation_results_review_package_digest"] == (
        inventory.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["ticker_universe_selection_approval_digest"] == (
        inventory.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_and_frozen_identity_authority_are_preserved():
    candidate = _candidate()

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == inventory.VALIDATION_TARGET_UNIVERSE
    assert candidate["frozen_identity_universe"] == inventory.VALIDATION_TARGET_UNIVERSE
    assert candidate["per_ticker_identity_authority_frozen"] is True
    assert candidate["identity_authority_created"] is True
    assert candidate["identity_authority_frozen"] is True
    assert candidate["new_ticker_identity_authority_created"] is True
    assert candidate["authority_scope"] == inventory.freeze_service.IDENTITY_AUTHORITY_ONLY


def test_registry_inventory_objective_scope_mode_and_approval_are_candidate_only():
    candidate = _candidate()

    assert candidate["registry_inventory_objective"] == inventory.REGISTRY_INVENTORY_OBJECTIVE
    assert candidate["registry_inventory_scope"] == inventory.REGISTRY_INVENTORY_SCOPE
    assert candidate["registry_inventory_mode"] == inventory.REGISTRY_INVENTORY_MODE
    assert candidate["registry_inventory_approval_status"] == (
        inventory.REGISTRY_INVENTORY_APPROVAL_STATUS
    )
    assert candidate["post_identity_freeze_registry_inventory_candidate_created"] is True
    assert candidate["post_identity_freeze_registry_inventory_review_created"] is False
    assert candidate["post_identity_freeze_registry_inventory_approved"] is False
    assert candidate["operator_review_required"] is True


def test_per_ticker_registry_inventory_entries_are_frozen_identity_only():
    candidate = _candidate()
    entries = candidate["per_ticker_registry_inventory_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == inventory.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["identity_freeze_status"] == inventory.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
        assert entry["identity_authority_scope"] == inventory.freeze_service.IDENTITY_AUTHORITY_ONLY
        assert entry["identity_authority_created"] is True
        assert entry["identity_authority_frozen"] is True
        assert entry["registry_inventory_entry_status"] == (
            inventory.INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authority_created"] is False
        assert entry["dataset_generation_authorized"] is False
        assert entry["runtime_use"] == (
            inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
        )
        assert entry["strategy_use"] == (
            inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
        )
        assert entry["paper_trading"] == (
            inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
        )
        assert entry["broker_execution"] == (
            inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
        )


def test_per_ticker_source_digests_and_inventory_digests_are_present():
    candidate = _candidate()

    for entry in candidate["per_ticker_registry_inventory_entries"]:
        assert len(entry["source_per_ticker_identity_freeze_digest"]) == 64
        assert len(entry["source_per_ticker_identity_candidate_digest"]) == 64
        assert len(entry["source_per_ticker_identity_review_digest"]) == 64
        assert len(entry["per_ticker_registry_inventory_digest"]) == 64


def test_unavailable_fields_and_limitations_are_preserved_without_fabrication():
    candidate = _candidate()

    for entry in candidate["per_ticker_registry_inventory_entries"]:
        summary = entry["unavailable_fields_summary"]
        assert "provider_canonical_ticker" in summary["unavailable_fields"]
        assert "ticker" in summary["available_fields"]
        assert entry["unavailable_fields_preserved_as_unavailable"] is True
        assert entry["identity_evidence_limitations"] == inventory.INVENTORY_LIMITATIONS
    assert candidate["inventory_limitations"] == inventory.INVENTORY_LIMITATIONS


def test_inventory_field_groups_future_chain_gates_risk_controls_and_outputs_are_defined():
    candidate = _candidate()

    assert candidate["inventory_field_groups"] == inventory.INVENTORY_FIELD_GROUPS
    assert candidate["future_chain"] == inventory.FUTURE_CHAIN
    assert candidate["future_gates"] == inventory.FUTURE_GATES
    assert candidate["risk_controls"] == inventory.RISK_CONTROLS
    assert [item["planned_output"] for item in candidate["planned_outputs"]] == (
        inventory.PLANNED_OUTPUT_NAMES
    )
    assert {item["generation_status"] for item in candidate["planned_outputs"]} == {
        inventory.PLANNED_NOT_GENERATED
    }
    assert {item["actionability"] for item in candidate["planned_outputs"]} == {
        inventory.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "post_identity_freeze_registry_inventory_approved",
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
def test_closed_boolean_boundaries_remain_false(field: str):
    assert _candidate()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == (
        inventory.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert candidate["profitability"] == inventory.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert candidate["runtime_use"] == (
        inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert candidate["strategy_use"] == (
        inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert candidate["paper_trading"] == (
        inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert candidate["broker_execution"] == (
        inventory.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )


def test_checklist_and_summary_counts_are_complete():
    candidate = _candidate()

    assert [item["check_id"] for item in candidate["inventory_checklist"]] == (
        inventory.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in candidate["inventory_checklist"]} == {inventory.PASS}
    assert candidate["inventory_summary"] == {
        "total_checks": 72,
        "passed_checks": 72,
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_registry_inventory_approval": False,
        "ready_for_corporate_action_authority_plan": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_candidate_and_per_ticker_inventory_digests_are_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["post_identity_freeze_registry_inventory_candidate_digest"] == (
        second["post_identity_freeze_registry_inventory_candidate_digest"]
    )
    assert [
        entry["per_ticker_registry_inventory_digest"]
        for entry in first["per_ticker_registry_inventory_entries"]
    ] == [
        entry["per_ticker_registry_inventory_digest"]
        for entry in second["per_ticker_registry_inventory_entries"]
    ]


def test_validator_accepts_valid_candidate():
    candidate = _candidate()

    validation = inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)

    assert validation["status"] == "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_VALID"
    assert validation["blocker_count"] == 0
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_registry_inventory_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("identity_authority_frozen", False),
        ("authority_scope", "WRONG"),
        ("registry_inventory_mode", "APPROVED"),
        ("post_identity_freeze_registry_inventory_approved", True),
    ],
)
def test_validator_rejects_invalid_top_level_fields(field: str, value: Any):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "runtime_migration_approved",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    candidate = _candidate()
    candidate[field] = True

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


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
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_per_ticker_inventory_count_not_12():
    candidate = _candidate()
    candidate["per_ticker_registry_inventory_entries"] = candidate[
        "per_ticker_registry_inventory_entries"
    ][:-1]

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_identity_freeze_digest():
    candidate = _candidate()
    candidate["per_ticker_registry_inventory_entries"][0].pop(
        "source_per_ticker_identity_freeze_digest"
    )

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_registry_inventory_digest():
    candidate = _candidate()
    candidate["per_ticker_registry_inventory_entries"][0].pop(
        "per_ticker_registry_inventory_digest"
    )

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_unavailable_field_fabricated():
    candidate = _candidate()
    candidate["per_ticker_registry_inventory_entries"][0]["unavailable_fields_summary"][
        "unavailable_fields"
    ] = "fabricated"

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "inventory_field_groups",
        "inventory_limitations",
        "future_chain",
        "future_gates",
        "risk_controls",
        "identity_authority_freeze_digest",
    ],
)
def test_validator_rejects_missing_required_sections(field: str):
    candidate = _candidate()
    candidate.pop(field)

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_validator_rejects_candidate_digest_mismatch():
    candidate = _candidate()
    candidate["post_identity_freeze_registry_inventory_candidate_digest"] = "0" * 64

    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = inventory.build_post_identity_freeze_registry_inventory_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Purpose",
        "## Source Identity Freeze",
        "## Target Universe",
        "## Per-Ticker Identity Registry Inventory",
        "## Inventory Field Groups",
        "## Preserved Unavailable Fields and Limitations",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Corporate-Action Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_write_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = inventory.write_post_identity_freeze_registry_inventory_candidate_v1(tmp_path)

    assert Path(result["path"]).exists()
    assert result["filename"].endswith(".json")
    with pytest.raises(inventory.PostIdentityFreezeRegistryInventoryCandidateError):
        inventory.write_post_identity_freeze_registry_inventory_candidate_v1(tmp_path)


def test_services_package_exports_inventory_helpers():
    from marketflow import services

    assert services.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE == (
        inventory.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE
    )
    assert services.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW == (
        inventory.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_post_identity_freeze_registry_inventory_candidate_v1 is (
        inventory.build_post_identity_freeze_registry_inventory_candidate_v1
    )
    assert services.validate_post_identity_freeze_registry_inventory_candidate_v1 is (
        inventory.validate_post_identity_freeze_registry_inventory_candidate_v1
    )
