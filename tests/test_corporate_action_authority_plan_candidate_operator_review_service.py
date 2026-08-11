from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    corporate_action_authority_plan_candidate_operator_review_service as review,
)


EXPECTED_CANDIDATE_DIGEST = (
    "3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a"
)


def _package() -> dict[str, Any]:
    return review.build_corporate_action_authority_plan_candidate_review_package_v1()


def _mutated_package(field: str, value: Any) -> dict[str, Any]:
    package = _package()
    package[field] = value
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review.plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["live_validation_rerun_performed"] is False
    assert package["live_provider_transport_enabled_in_review"] is False


def test_artifact_kind_status_schema_and_binding_mode_are_exact():
    package = _package()

    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert package["schema_version"] == (
        review.SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1
    )
    assert package["corporate_action_authority_plan_candidate_binding_mode"] == (
        review.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING
    )


def test_reviewed_candidate_evidence_is_bound():
    package = _package()

    assert package["reviewed_corporate_action_authority_plan_candidate_kind"] == (
        review.plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE
    )
    assert package["reviewed_corporate_action_authority_plan_candidate_status"] == (
        review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert package["reviewed_corporate_action_authority_plan_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )
    assert package["reviewed_corporate_action_authority_plan_candidate_checklist_total"] == 79
    assert package["reviewed_corporate_action_authority_plan_candidate_checklist_passed"] == 79
    assert package["reviewed_corporate_action_authority_plan_candidate_checklist_failed"] == 0
    assert package["reviewed_corporate_action_authority_plan_candidate_blocker_count"] == 0


def test_source_digest_chain_is_bound():
    package = _package()

    assert package["corporate_action_authority_plan_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )
    assert package["post_identity_freeze_registry_inventory_approval_digest"] == (
        review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert package["post_identity_freeze_registry_inventory_candidate_review_package_digest"] == (
        review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["post_identity_freeze_registry_inventory_candidate_digest"] == (
        review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
    )
    assert package["identity_authority_freeze_digest"] == (
        review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert package["identity_authority_candidate_review_package_digest"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["identity_authority_candidate_digest"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
    )
    assert package["live_ticker_validation_results_review_package_digest"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["live_ticker_validation_execution_digest"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_identity_and_registry_inventory_are_preserved():
    package = _package()

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["identity_inventory_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["identity_authority_frozen"] is True
    assert package["post_identity_freeze_registry_inventory_approved"] is True
    assert package["authority_scope"] == (
        review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
    )


def test_corporate_action_plan_objective_scope_mode_and_creation_status_are_reviewed():
    package = _package()

    assert package["corporate_action_authority_plan_objective"] == (
        review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE
    )
    assert package["corporate_action_authority_plan_scope"] == (
        review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE
    )
    assert package["corporate_action_authority_plan_mode"] == (
        review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_MODE
    )
    assert package["corporate_action_authority_creation_status"] == (
        review.plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS
    )
    assert package["plan_scope"] == review.plan.PLAN_SCOPE


def test_per_ticker_plan_and_review_entries_are_ready_for_operator_assessment():
    package = _package()
    entries = package["per_ticker_corporate_action_plan_entries"]
    review_entries = package["per_ticker_corporate_action_plan_review_entries"]

    assert len(entries) == 12
    assert len(review_entries) == 12
    assert [entry["ticker"] for entry in review_entries] == (
        review.VALIDATION_TARGET_UNIVERSE
    )
    for entry in review_entries:
        assert entry["identity_authority_status"] == (
            review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
        )
        assert entry["registry_inventory_status"] == (
            review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        )
        assert entry["corporate_action_plan_status"] == review.plan.PLANNED_NOT_CREATED
        assert entry["corporate_action_plan_review_status"] == (
            review.READY_FOR_OPERATOR_ASSESSMENT
        )
        assert entry["split_event_authority_status"] == review.plan.NOT_CREATED
        assert entry["dividend_event_authority_status"] == review.plan.NOT_CREATED
        assert entry["corporate_action_authority_created"] is False
        assert entry["dataset_generation_authorized"] is False
        assert len(entry["per_ticker_corporate_action_plan_digest"]) == 64
        assert len(entry["per_ticker_corporate_action_plan_review_digest"]) == 64


def test_evidence_requirements_future_chains_gates_and_risk_controls_are_reviewed():
    package = _package()

    assert package["corporate_action_evidence_requirements"] == (
        review.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS
    )
    assert package["corporate_action_evidence_requirement_policy"] == (
        review.CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY
    )
    assert package["future_split_event_authority_chain"] == (
        review.FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN
    )
    assert package["future_dividend_event_authority_chain"] == (
        review.FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN
    )
    assert package["future_corporate_action_readiness_chain"] == (
        review.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
    )
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    package = _package()

    assert package["planned_output_count"] == 9
    assert {item["generation_status"] for item in package["planned_outputs"]} == {
        review.plan.PLANNED_NOT_GENERATED
    }
    assert {item["actionability"] for item in package["planned_outputs"]} == {
        review.plan.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "corporate_action_authority_plan_approved",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
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
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ],
)
def test_closed_boolean_boundaries_remain_false(field: str):
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    package = _package()
    not_authorized = (
        review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )

    assert package["predictive_usefulness"] == (
        review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    )
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == not_authorized
    assert package["strategy_use"] == not_authorized
    assert package["paper_trading"] == not_authorized
    assert package["broker_execution"] == not_authorized


def test_checklist_contains_all_required_check_ids_and_all_pass():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_and_blockers_correctly():
    summary = _package()["review_summary"]

    assert summary == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_assessment": True,
        "ready_for_corporate_action_authority_plan_approval": False,
        "ready_for_split_event_authority_candidate": False,
        "ready_for_dividend_event_authority_candidate": False,
        "corporate_action_authority_authorized": False,
        "split_event_authority_authorized": False,
        "dividend_event_authority_authorized": False,
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

    assert first["corporate_action_authority_plan_candidate_review_package_digest"] == (
        second["corporate_action_authority_plan_candidate_review_package_digest"]
    )
    assert first["corporate_action_authority_plan_candidate_review_package_digest"] == (
        review.corporate_action_authority_plan_candidate_review_package_digest_v1(first)
    )
    assert [
        entry["per_ticker_corporate_action_plan_review_digest"]
        for entry in first["per_ticker_corporate_action_plan_review_entries"]
    ] == [
        entry["per_ticker_corporate_action_plan_review_digest"]
        for entry in second["per_ticker_corporate_action_plan_review_entries"]
    ]


def test_validator_accepts_valid_review_package():
    validation = review.validate_corporate_action_authority_plan_candidate_review_package_v1(
        _package()
    )

    assert validation["status"] == (
        "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["review_status"] == (
        review.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert validation["blocker_count"] == 0
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_corporate_action_authority_plan_approval"] is False
    assert validation["ready_for_split_event_authority_candidate"] is False
    assert validation["ready_for_dividend_event_authority_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "CORPORATE_ACTION_AUTHORITY_APPROVED", "artifact_kind"),
        ("review_status", "APPROVED", "review_status"),
        ("reviewed_corporate_action_authority_plan_candidate_digest", "0" * 64, "candidate_digest"),
        ("corporate_action_authority_plan_candidate_digest", "0" * 64, "candidate_digest"),
        ("reviewed_corporate_action_authority_plan_candidate_status", "CREATED", "candidate_status"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("live_provider_transport_enabled_in_review", True, "live_provider_transport_enabled_in_review"),
        ("target_universe_count", 11, "target_universe_count"),
        ("identity_authority_frozen", False, "identity_authority_frozen"),
        ("post_identity_freeze_registry_inventory_approved", False, "post_identity_freeze_registry_inventory_approved"),
        ("corporate_action_authority_plan_scope", "AUTHORITY", "corporate_action_authority_plan_scope"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("corporate_action_authority_plan_approved", True, "corporate_action_authority_plan_approved"),
        ("split_event_authority_candidate_created", True, "split_event_authority_candidate_created"),
        ("split_event_authority_review_created", True, "split_event_authority_review_created"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("split_event_authority_frozen", True, "split_event_authority_frozen"),
        ("dividend_event_authority_candidate_created", True, "dividend_event_authority_candidate_created"),
        ("dividend_event_authority_review_created", True, "dividend_event_authority_review_created"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
        ("dividend_event_authority_frozen", True, "dividend_event_authority_frozen"),
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
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_invalid_top_level_mutations(field: str, value: Any, match: str):
    package = _mutated_package(field, value)

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("corporate_action_evidence_requirements", "corporate_action_evidence_requirements"),
        ("future_split_event_authority_chain", "future_split_event_authority_chain"),
        ("future_dividend_event_authority_chain", "future_dividend_event_authority_chain"),
        ("future_corporate_action_readiness_chain", "future_corporate_action_readiness_chain"),
        ("future_gates", "future_gates"),
        ("risk_controls", "risk_controls"),
    ],
)
def test_validator_rejects_missing_required_review_sections(field: str, match: str):
    package = _package()
    package.pop(field)

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_target_universe_mismatch():
    package = _package()
    package["target_universe"] = package["target_universe"][:-1]

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match="target_universe",
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("per_ticker_corporate_action_plan_entries", "plan_entries"),
        ("per_ticker_corporate_action_plan_review_entries", "review_entries"),
    ],
)
def test_validator_rejects_per_ticker_count_mismatch(field: str, match: str):
    package = _package()
    package[field] = package[field][:-1]

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("digest_field", "match"),
    [
        ("per_ticker_corporate_action_plan_digest", "plan_digest"),
        ("per_ticker_corporate_action_plan_review_digest", "review_digest"),
    ],
)
def test_validator_rejects_missing_per_ticker_digests(digest_field: str, match: str):
    package = _package()
    package["per_ticker_corporate_action_plan_review_entries"][0].pop(digest_field)

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_review_package_digest_mismatch():
    package = _package()
    package["corporate_action_authority_plan_candidate_review_package_digest"] = "0" * 64

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match="review_package_digest",
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_missing_review_package_digest():
    package = _package()
    package.pop("corporate_action_authority_plan_candidate_review_package_digest")

    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match="review_package_digest",
    ):
        review.validate_corporate_action_authority_plan_candidate_review_package_v1(
            package
        )


def test_markdown_includes_required_sections():
    markdown = review.build_corporate_action_authority_plan_candidate_review_markdown_v1(
        _package()
    )

    for section in (
        "## Title",
        "## Reviewed Corporate-Action Authority Plan Candidate",
        "## Source Registry Inventory Approval",
        "## Target Universe",
        "## Corporate-Action Authority Plan Objective",
        "## Per-Ticker Corporate-Action Plan Review",
        "## Corporate-Action Evidence Requirements",
        "## Future Split Event Authority Chain",
        "## Future Dividend Event Authority Chain",
        "## Future Corporate-Action Readiness Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Corporate-Action Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_corporate_action_authority_plan_candidate_review_package_v1(
        tmp_path
    )

    assert result["artifact_kind"] == (
        review.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written["artifact_kind"] == (
        review.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    with pytest.raises(
        review.CorporateActionAuthorityPlanCandidateReviewPackageError,
        match="already exists",
    ):
        review.write_corporate_action_authority_plan_candidate_review_package_v1(
            tmp_path
        )


def test_services_package_exports_review_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_corporate_action_authority_plan_candidate_review_package_v1 is (
        review.build_corporate_action_authority_plan_candidate_review_package_v1
    )
    assert services.validate_corporate_action_authority_plan_candidate_review_package_v1 is (
        review.validate_corporate_action_authority_plan_candidate_review_package_v1
    )
    assert services.write_corporate_action_authority_plan_candidate_review_package_v1 is (
        review.write_corporate_action_authority_plan_candidate_review_package_v1
    )
    assert services.build_corporate_action_authority_plan_candidate_review_markdown_v1 is (
        review.build_corporate_action_authority_plan_candidate_review_markdown_v1
    )
    assert services.corporate_action_authority_plan_candidate_review_package_digest_v1 is (
        review.corporate_action_authority_plan_candidate_review_package_digest_v1
    )
