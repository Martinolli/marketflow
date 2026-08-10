from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    post_identity_freeze_registry_inventory_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_post_identity_freeze_registry_inventory_candidate_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_validation_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_kind_status_and_digest_are_exact():
    package = _package()

    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert package["post_identity_freeze_registry_inventory_candidate_review_package_digest"] == (
        "d35861b3bb19d361241df0e6ba080306e647116cf5b12815ce1ddf2fb48cf51c"
    )


def test_reviewed_candidate_evidence_is_bound():
    package = _package()

    assert package["reviewed_registry_inventory_candidate_kind"] == (
        review.candidate_service.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE
    )
    assert package["reviewed_registry_inventory_candidate_status"] == (
        review.candidate_service.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW
    )
    assert package["reviewed_registry_inventory_candidate_digest"] == (
        review.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
    )
    assert package["reviewed_registry_inventory_candidate_checklist_total"] == 72
    assert package["reviewed_registry_inventory_candidate_checklist_passed"] == 72
    assert package["reviewed_registry_inventory_candidate_checklist_failed"] == 0
    assert package["reviewed_registry_inventory_candidate_blocker_count"] == 0


def test_source_evidence_digests_are_bound():
    package = _package()

    assert package["post_identity_freeze_registry_inventory_candidate_digest"] == (
        review.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
    )
    assert package["identity_authority_freeze_digest"] == (
        review.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert package["identity_authority_candidate_review_package_digest"] == (
        review.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["identity_authority_candidate_digest"] == (
        review.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["identity_authority_plan_candidate_review_package_digest"] == (
        review.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["live_ticker_validation_results_review_package_digest"] == (
        review.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        review.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_identity_and_registry_inventory_scope_are_preserved():
    package = _package()

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["frozen_identity_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["identity_authority_frozen"] is True
    assert package["authority_scope"] == review.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
    assert package["registry_inventory_objective"] == (
        review.candidate_service.REGISTRY_INVENTORY_OBJECTIVE
    )
    assert package["registry_inventory_mode"] == review.candidate_service.REGISTRY_INVENTORY_MODE
    assert package["registry_inventory_approval_status"] == (
        review.candidate_service.REGISTRY_INVENTORY_APPROVAL_STATUS
    )


def test_per_ticker_inventory_review_entries_are_ready_and_bound():
    package = _package()
    entries = package["per_ticker_registry_inventory_review_entries"]

    assert len(package["per_ticker_registry_inventory_entries"]) == 12
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == review.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["identity_freeze_status"] == (
            review.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
        )
        assert entry["identity_authority_scope"] == (
            review.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
        )
        assert entry["registry_inventory_review_status"] == review.READY_FOR_OPERATOR_ASSESSMENT
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_authority_created"] is False
        assert entry["dataset_generation_authorized"] is False
        assert len(entry["source_per_ticker_identity_freeze_digest"]) == 64
        assert len(entry["source_per_ticker_identity_candidate_digest"]) == 64
        assert len(entry["source_per_ticker_identity_review_digest"]) == 64
        assert len(entry["per_ticker_registry_inventory_digest"]) == 64
        assert len(entry["per_ticker_registry_inventory_review_digest"]) == 64


def test_inventory_metadata_and_planned_outputs_are_reviewed():
    package = _package()

    assert package["inventory_field_groups"] == review.INVENTORY_FIELD_GROUPS
    assert package["inventory_limitations"] == review.INVENTORY_LIMITATIONS
    assert package["future_chain"] == review.FUTURE_CHAIN
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert package["planned_output_count"] == 7
    assert package["planned_outputs_status"] == review.candidate_service.PLANNED_NOT_GENERATED
    assert package["planned_outputs_label"] == review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE


def test_unavailable_fields_remain_unavailable_and_not_fabricated():
    package = _package()

    for entry in package["per_ticker_registry_inventory_review_entries"]:
        summary = entry["unavailable_fields_summary"]
        assert "provider_canonical_ticker" in summary["unavailable_fields"]
        assert "ticker" in summary["available_fields"]
        assert entry["unavailable_fields_preserved_as_unavailable"] is True


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    package = _package()

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == (
        review.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert package["strategy_use"] == (
        review.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert package["paper_trading"] == (
        review.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )
    assert package["broker_execution"] == (
        review.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )


def test_checklist_and_summary_counts_are_complete():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}
    assert package["review_summary"] == {
        "total_checks": 79,
        "passed_checks": 79,
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_assessment": True,
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


def test_review_package_and_per_ticker_review_digests_are_deterministic():
    first = _package()
    second = _package()

    assert first["post_identity_freeze_registry_inventory_candidate_review_package_digest"] == (
        second["post_identity_freeze_registry_inventory_candidate_review_package_digest"]
    )
    assert [
        entry["per_ticker_registry_inventory_review_digest"]
        for entry in first["per_ticker_registry_inventory_review_entries"]
    ] == [
        entry["per_ticker_registry_inventory_review_digest"]
        for entry in second["per_ticker_registry_inventory_review_entries"]
    ]


def test_validator_accepts_valid_review_package():
    package = _package()

    validation = review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        package
    )

    assert validation["status"] == (
        "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["blocker_count"] == 0
    assert validation["ready_for_registry_inventory_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_registry_inventory_candidate_digest", "0" * 64),
        ("reviewed_registry_inventory_candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("identity_authority_frozen", False),
        ("authority_scope", "WRONG"),
        ("registry_inventory_mode", "APPROVED"),
        ("post_identity_freeze_registry_inventory_approved", True),
    ],
)
def test_validator_rejects_invalid_top_level_fields(field: str, value: Any):
    package = _package()
    package[field] = value

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
    package = _package()
    package[field] = True

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


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
    package = _package()
    package[field] = value

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


def test_validator_rejects_target_universe_mismatch():
    package = _package()
    package["target_universe"] = list(reversed(package["target_universe"]))

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_registry_inventory_entries",
        "per_ticker_registry_inventory_review_entries",
    ],
)
def test_validator_rejects_per_ticker_count_not_12(field: str):
    package = _package()
    package[field] = package[field][:-1]

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "source_per_ticker_identity_freeze_digest",
        "per_ticker_registry_inventory_digest",
        "per_ticker_registry_inventory_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(field: str):
    package = _package()
    package["per_ticker_registry_inventory_review_entries"][0].pop(field)

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


def test_validator_rejects_unavailable_field_fabricated():
    package = _package()
    package["per_ticker_registry_inventory_review_entries"][0]["unavailable_fields_summary"][
        "unavailable_fields"
    ] = "fabricated"

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    ["inventory_field_groups", "inventory_limitations", "future_chain", "future_gates", "risk_controls"],
)
def test_validator_rejects_missing_required_sections(field: str):
    package = _package()
    package.pop(field)

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


def test_validator_rejects_review_package_digest_mismatch():
    package = _package()
    package["post_identity_freeze_registry_inventory_candidate_review_package_digest"] = "0" * 64

    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            package
        )


def test_markdown_includes_required_sections():
    markdown = review.build_post_identity_freeze_registry_inventory_candidate_review_markdown_v1(
        _package()
    )

    for section in [
        "## Reviewed Post-Identity-Freeze Registry Inventory Candidate",
        "## Source Identity Freeze",
        "## Target Universe",
        "## Per-Ticker Identity Registry Inventory Review",
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


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        tmp_path
    )

    assert Path(result["path"]).exists()
    assert result["filename"].endswith(".json")
    with pytest.raises(review.PostIdentityFreezeRegistryInventoryCandidateReviewPackageError):
        review.write_post_identity_freeze_registry_inventory_candidate_review_package_v1(
            tmp_path
        )


def test_services_package_exports_review_helpers():
    from marketflow import services

    assert services.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_post_identity_freeze_registry_inventory_candidate_review_package_v1 is (
        review.build_post_identity_freeze_registry_inventory_candidate_review_package_v1
    )
    assert services.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1 is (
        review.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1
    )
