from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import expanded_universe_per_ticker_identity_authority_freeze_service as freeze


def _attestation(**overrides: Any) -> dict[str, Any]:
    payload = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-10T00:00:00Z",
        "operator_attestation_phrase": freeze.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_identity_candidate_review_package_digest": (
            freeze.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_identity_candidate_digest": (
            freeze.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        ),
        "operator_confirms_identity_plan_review_package_digest": (
            freeze.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_live_validation_results_review_digest": (
            freeze.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_target_universe": freeze.VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_authority_scope_identity_only": True,
        "operator_confirms_per_ticker_identity_entries_reviewed": True,
        "operator_confirms_no_provider_requests_in_freeze": True,
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
    payload.update(overrides)
    return freeze.build_expanded_universe_per_ticker_identity_authority_freeze_attestation_v1(
        **payload
    )


def _package(**attestation_overrides: Any) -> dict[str, Any]:
    return freeze.build_expanded_universe_per_ticker_identity_authority_frozen_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == (
        freeze.OPERATOR_DECISION_FREEZE_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY
    )
    assert attestation["operator_attestation_phrase"] == (
        freeze.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_target_universe"] == (
        freeze.VALIDATION_TARGET_UNIVERSE
    )
    assert all(attestation[field] is True for field in freeze.REQUIRED_TRUE_ATTESTATION_FIELDS)


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        freeze.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_freeze"] is False
    assert package["live_validation_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_freeze"] is False
    assert package["source_output_file_reinspection_performed"] is False


def test_artifact_kind_status_scope_and_digest_are_exact():
    package = _package()

    assert package["artifact_kind"] == (
        freeze.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN
    )
    assert package["freeze_status"] == (
        freeze.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN
    )
    assert package["authority_scope"] == freeze.IDENTITY_AUTHORITY_ONLY
    assert package["expanded_universe_per_ticker_identity_authority_freeze_digest"] == (
        "55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30"
    )


def test_source_evidence_digests_are_bound():
    package = _package()

    assert package["identity_authority_candidate_review_package_digest"] == (
        freeze.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["identity_authority_candidate_digest"] == (
        freeze.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["identity_authority_plan_candidate_review_package_digest"] == (
        freeze.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["identity_authority_plan_candidate_digest"] == (
        freeze.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert package["live_ticker_validation_results_review_package_digest"] == (
        freeze.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["live_ticker_validation_execution_digest"] == (
        freeze.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert package["live_ticker_validation_approval_digest"] == (
        freeze.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        freeze.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_is_preserved_exactly():
    package = _package()

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == freeze.VALIDATION_TARGET_UNIVERSE
    assert package["reviewed_universe"] == freeze.VALIDATION_TARGET_UNIVERSE


def test_identity_authority_created_and_frozen_state_is_identity_only():
    package = _package()

    assert package["per_ticker_identity_authority_candidate_created"] is True
    assert package["per_ticker_identity_authority_review_created"] is True
    assert package["per_ticker_identity_authority_frozen"] is True
    assert package["identity_authority_created"] is True
    assert package["identity_authority_frozen"] is True
    assert package["new_ticker_identity_authority_created"] is True
    assert package["authority_scope"] == freeze.IDENTITY_AUTHORITY_ONLY


def test_per_ticker_frozen_entries_are_identity_only_and_not_runtime_authorized():
    package = _package()
    entries = package["per_ticker_frozen_identity_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == freeze.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["live_validation_status"] == (
            freeze.candidate_service.plan_review.plan.VALIDATED_READ_ONLY
        )
        assert entry["identity_candidate_status"] == (
            freeze.candidate_service.IDENTITY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
        )
        assert entry["identity_review_status"] == freeze.review_service.REVIEW_PACKAGE_CREATED
        assert entry["identity_freeze_status"] == freeze.IDENTITY_FREEZE_STATUS_FROZEN
        assert entry["identity_authority_scope"] == freeze.IDENTITY_AUTHORITY_ONLY
        assert entry["identity_authority_created"] is True
        assert entry["identity_authority_frozen"] is True
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authority_created"] is False
        assert entry["dataset_generation_authorized"] is False
        assert entry["runtime_use"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
        assert entry["strategy_use"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
        assert entry["paper_trading"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
        assert entry["broker_execution"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED


def test_frozen_identity_fields_preserve_unavailable_values_and_source_digests():
    package = _package()

    for entry in package["per_ticker_frozen_identity_entries"]:
        fields = entry["frozen_identity_fields"]
        assert set(fields) == set(freeze.IDENTITY_FIELDS_TO_BIND)
        for field in fields.values():
            assert set(field) == {"value", "status"}
            if field["status"] == freeze.candidate_service.UNAVAILABLE_IN_SOURCE:
                assert field["value"] is None
        assert entry["unavailable_fields_preserved_as_unavailable"] is True
        assert entry["identity_evidence_limitations"] == freeze.IDENTITY_EVIDENCE_LIMITATIONS
        assert len(entry["source_per_ticker_identity_candidate_digest"]) == 64
        assert len(entry["source_per_ticker_identity_review_digest"]) == 64
        assert len(entry["per_ticker_identity_freeze_digest"]) == 64


@pytest.mark.parametrize(
    "field",
    [
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
def test_downstream_authority_and_execution_flags_remain_false(field: str):
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    package = _package()

    assert package["predictive_usefulness"] == freeze.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == freeze.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["strategy_use"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["paper_trading"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED
    assert package["broker_execution"] == freeze.candidate_service.plan_review.plan.NOT_AUTHORIZED


def test_checklist_and_summary_counts_are_complete():
    package = _package()

    assert [item["check_id"] for item in package["freeze_checklist"]] == (
        freeze.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in package["freeze_checklist"]} == {freeze.PASS}
    assert package["freeze_summary"] == {
        "total_checks": 86,
        "passed_checks": 86,
        "failed_checks": 0,
        "blocker_count": 0,
        "identity_authority_frozen_by_operator": True,
        "authority_scope": freeze.IDENTITY_AUTHORITY_ONLY,
        "ready_for_post_identity_freeze_registry_inventory": True,
        "ready_for_corporate_action_authority_candidate": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_freeze_digest_and_per_ticker_digests_are_deterministic():
    first = _package()
    second = _package()

    assert first["expanded_universe_per_ticker_identity_authority_freeze_digest"] == (
        second["expanded_universe_per_ticker_identity_authority_freeze_digest"]
    )
    assert [
        entry["per_ticker_identity_freeze_digest"]
        for entry in first["per_ticker_frozen_identity_entries"]
    ] == [
        entry["per_ticker_identity_freeze_digest"]
        for entry in second["per_ticker_frozen_identity_entries"]
    ]


def test_validator_accepts_valid_frozen_artifact():
    package = _package()

    validation = freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)

    assert validation["status"] == "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN_VALID"
    assert validation["blocker_count"] == 0
    assert validation["ready_for_post_identity_freeze_registry_inventory"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("freeze_status", "NOT_FROZEN"),
        ("authority_scope", "BROADER_AUTHORITY"),
        ("identity_authority_created", False),
        ("identity_authority_frozen", False),
        ("per_ticker_identity_authority_frozen", False),
        ("target_universe_count", 11),
    ],
)
def test_validator_rejects_invalid_top_level_identity_fields(field: str, value: Any):
    package = _package()
    package[field] = value

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "DO_NOT_FREEZE"),
        ("operator_attestation_phrase", "wrong phrase"),
        ("operator_confirms_identity_candidate_review_package_digest", "0" * 64),
        ("operator_confirms_identity_candidate_digest", "0" * 64),
        ("operator_confirms_identity_plan_review_package_digest", "0" * 64),
        ("operator_confirms_live_validation_results_review_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(freeze.VALIDATION_TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
    ],
)
def test_build_rejects_wrong_operator_attestation_values(field: str, value: Any):
    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        _package(**{field: value})


@pytest.mark.parametrize("field", freeze.REQUIRED_TRUE_ATTESTATION_FIELDS)
def test_build_rejects_missing_operator_boundary_confirmation(field: str):
    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        _package(**{field: False})


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_freeze",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_freeze",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "runtime_migration_approved",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    package = _package()
    package[field] = True

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


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
def test_validator_rejects_accepted_or_authorized_runtime_values(field: str, value: str):
    package = _package()
    package[field] = value

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_validator_rejects_target_universe_mismatch():
    package = _package()
    package["target_universe"] = list(reversed(package["target_universe"]))

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_validator_rejects_missing_per_ticker_frozen_entry():
    package = _package()
    package["per_ticker_frozen_identity_entries"] = package[
        "per_ticker_frozen_identity_entries"
    ][:-1]

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_validator_rejects_missing_per_ticker_freeze_digest():
    package = _package()
    package["per_ticker_frozen_identity_entries"][0].pop("per_ticker_identity_freeze_digest")

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_validator_rejects_fabricated_unavailable_field():
    package = _package()
    field = package["per_ticker_frozen_identity_entries"][0]["frozen_identity_fields"][
        "provider_canonical_ticker"
    ]
    field["status"] = freeze.candidate_service.UNAVAILABLE_IN_SOURCE
    field["value"] = "MSFT"

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_validator_rejects_freeze_digest_mismatch():
    package = _package()
    package["expanded_universe_per_ticker_identity_authority_freeze_digest"] = "0" * 64

    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(package)


def test_remaining_roadmap_keeps_downstream_work_future():
    package = _package()

    assert package["remaining_required_tasks"] == [
        "post_identity_freeze_registry_inventory_candidate",
        "corporate_action_authority_chain_candidate",
        "acquisition_generation_chain_candidate",
        "canonical_dataset_chain_candidate",
        "research_registry_chain_candidate",
    ]
    assert package["freeze_summary"]["ready_for_corporate_action_authority_candidate"] is False


def test_markdown_includes_required_sections_and_guardrails():
    markdown = freeze.build_expanded_universe_per_ticker_identity_authority_frozen_markdown_v1(
        _package()
    )

    for section in [
        "## Frozen Expanded Universe Identity Authority",
        "## Operator Attestation",
        "## Source Identity Candidate Review Package",
        "## Target Universe",
        "## Frozen Per-Ticker Identity Entries",
        "## Preserved Unavailable Fields and Limitations",
        "## Authority Scope",
        "## Corporate-Action Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Freeze Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert section in markdown
    assert "No Massive.com / Polygon provider request was made." in markdown


def test_write_frozen_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = freeze.write_expanded_universe_per_ticker_identity_authority_frozen_v1(
        tmp_path,
        operator_attestation=_attestation(),
    )

    assert Path(result["path"]).exists()
    assert result["filename"].endswith(".json")
    with pytest.raises(freeze.ExpandedUniversePerTickerIdentityAuthorityFreezeError):
        freeze.write_expanded_universe_per_ticker_identity_authority_frozen_v1(
            tmp_path,
            operator_attestation=_attestation(),
        )


def test_services_package_exports_freeze_helpers():
    from marketflow import services

    assert services.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN == (
        freeze.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FROZEN
    )
    assert services.REQUIRED_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_FREEZE_OPERATOR_ATTESTATION_PHRASE == (
        freeze.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_frozen_v1 is (
        freeze.build_expanded_universe_per_ticker_identity_authority_frozen_v1
    )
    assert services.validate_expanded_universe_per_ticker_identity_authority_frozen_v1 is (
        freeze.validate_expanded_universe_per_ticker_identity_authority_frozen_v1
    )
