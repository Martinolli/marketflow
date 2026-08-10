from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_plan_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return (
        review.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1()
    )


def _mutated_package(field: str, value: Any) -> dict[str, Any]:
    package = _package()
    package[field] = value
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        review.plan.results_review.provider,
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
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert package["schema_version"] == (
        review.SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1
    )
    assert package["identity_authority_plan_candidate_binding_mode"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING
    )


def test_reviewed_candidate_evidence_is_bound():
    package = _package()

    assert package["reviewed_identity_authority_plan_candidate_kind"] == (
        review.plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
    )
    assert package["reviewed_identity_authority_plan_candidate_status"] == (
        review.plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert package["reviewed_identity_authority_plan_candidate_digest"] == (
        review.EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
    )
    assert package["reviewed_identity_authority_plan_candidate_checklist_total"] == 71
    assert package["reviewed_identity_authority_plan_candidate_checklist_passed"] == 71
    assert package["reviewed_identity_authority_plan_candidate_checklist_failed"] == 0
    assert package["reviewed_identity_authority_plan_candidate_blocker_count"] == 0


def test_source_digest_chain_is_bound():
    package = _package()

    assert package["live_ticker_validation_results_review_package_digest"] == (
        review.plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["live_ticker_validation_execution_digest"] == (
        review.plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert package["live_ticker_validation_approval_digest"] == (
        review.plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    )
    assert package["live_ticker_validation_candidate_digest"] == (
        review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
    )
    assert package["live_ticker_validation_candidate_review_package_digest"] == (
        review.plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["ticker_universe_selection_approval_digest"] == (
        review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )
    assert package["ticker_universe_selection_candidate_digest"] == (
        review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
    )
    assert package["ticker_universe_selection_candidate_review_package_digest"] == (
        review.plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        review.plan.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["additional_predictive_evidence_plan_candidate_review_package_digest"] == (
        review.plan.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_target_universe_and_validation_summary_are_preserved():
    package = _package()

    assert package["target_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["validated_universe"] == review.VALIDATION_TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["all_targets_validated_read_only"] is True
    assert package["validated_read_only_count"] == 12
    assert package["provider_request_count"] == 12
    assert package["successful_provider_response_count"] == 12
    assert package["failed_provider_response_count"] == 0
    assert package["validation_supports_future_authority_chain_planning"] is True
    assert package["validation_creates_new_ticker_authority"] is False


def test_identity_plan_objective_boundary_and_entries_are_preserved():
    package = _package()
    entries = package["per_ticker_identity_plan_entries"]

    assert package["identity_authority_plan_objective"] == review.plan.IDENTITY_AUTHORITY_PLAN_OBJECTIVE
    assert package["identity_authority_plan_mode"] == review.plan.PLANNED_NOT_CREATED
    assert package["identity_authority_creation_status"] == review.plan.NOT_CREATED
    assert package["identity_freeze_status"] == review.plan.NOT_FROZEN
    assert len(entries) == 12
    for entry in entries:
        assert entry["live_validation_status"] == review.plan.VALIDATED_READ_ONLY
        assert entry["identity_authority_plan_status"] == review.plan.PLANNED_NOT_CREATED
        assert entry["identity_candidate_status"] == review.plan.NOT_CREATED
        assert entry["identity_review_status"] == review.plan.NOT_CREATED
        assert entry["identity_freeze_status"] == review.plan.NOT_FROZEN
        assert entry["identity_authority_created"] is False
        assert entry["identity_fields_to_bind"] == review.IDENTITY_FIELDS_TO_BIND
        assert entry["identity_evidence_limitations"] == review.IDENTITY_EVIDENCE_LIMITATIONS


def test_identity_fields_classification_limitations_future_chain_gates_and_risks_are_defined():
    package = _package()

    assert package["identity_fields_to_bind"] == review.IDENTITY_FIELDS_TO_BIND
    assert list(package["identity_field_groups"]) == [
        "core_symbol_identity_fields",
        "provider_reference_identity_fields",
        "security_classification_fields",
        "exchange_and_market_fields",
        "provider_cross_reference_fields",
        "audit_digest_fields",
        "limitation_fields",
    ]
    assert package["identity_evidence_limitations"] == review.IDENTITY_EVIDENCE_LIMITATIONS
    assert len(package["future_identity_authority_chain"]) == 9
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    package = _package()

    assert package["planned_output_count"] == 9
    assert [item["output_id"] for item in package["planned_outputs"]] == review.PLANNED_OUTPUT_IDS
    assert package["planned_outputs_status"] == review.plan.PLANNED_NOT_GENERATED
    assert package["planned_outputs_label"] == review.plan.RESEARCH_ONLY_NON_ACTIONABLE


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "per_ticker_identity_authority_candidate_created",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
        "identity_authority_created",
        "identity_authority_frozen",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
    ],
)
def test_closed_boolean_boundaries_remain_false(field: str):
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    package = _package()

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert package["runtime_use"] == review.plan.NOT_AUTHORIZED
    assert package["strategy_use"] == review.plan.NOT_AUTHORIZED
    assert package["paper_trading"] == review.plan.NOT_AUTHORIZED
    assert package["broker_execution"] == review.plan.NOT_AUTHORIZED


def test_checklist_contains_all_required_check_ids_and_all_pass():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_and_blockers_correctly():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_per_ticker_identity_authority_candidate"] is False
    assert summary["identity_authority_created"] is False
    assert summary["identity_authority_frozen"] is False
    assert summary["corporate_action_authority_authorized"] is False
    assert summary["acquisition_authorized"] is False
    assert summary["dataset_generation_authorized"] is False
    assert summary["additional_predictive_evidence_execution_authorized"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first[
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    ] == second[
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    ]
    assert first[
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    ] == review.expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1(
        first
    )


def test_validator_accepts_valid_review_package():
    validation = review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
        _package()
    )

    assert validation["status"] == (
        "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["review_status"] == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_per_ticker_identity_authority_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "PER_TICKER_IDENTITY_AUTHORITY_CANDIDATE", "artifact_kind"),
        ("review_status", "IDENTITY_AUTHORITY_CREATED", "review_status"),
        ("reviewed_identity_authority_plan_candidate_digest", "0" * 64, "candidate_digest"),
        ("reviewed_identity_authority_plan_candidate_status", "CREATED", "candidate_status"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("live_provider_transport_enabled_in_review", True, "live_provider_transport_enabled_in_review"),
        ("target_universe_count", 11, "target_universe_count"),
        ("identity_authority_plan_mode", "CREATED", "identity_authority_plan_mode"),
        ("identity_authority_created", True, "identity_authority_created"),
        ("per_ticker_identity_authority_candidate_created", True, "per_ticker_identity_authority_candidate_created"),
        ("per_ticker_identity_authority_review_created", True, "per_ticker_identity_authority_review_created"),
        ("per_ticker_identity_authority_frozen", True, "per_ticker_identity_authority_frozen"),
        ("new_ticker_authority_created", True, "new_ticker_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("split_event_authority_created", True, "split_event_authority_created"),
        ("dividend_event_authority_created", True, "dividend_event_authority_created"),
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
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("field", "match"),
    [
        ("identity_fields_to_bind", "identity_fields_to_bind"),
        ("identity_field_groups", "identity_field_groups"),
        ("identity_evidence_limitations", "identity_evidence_limitations"),
        ("future_identity_authority_chain", "future_identity_authority_chain"),
        ("future_gates", "future_gates"),
        ("risk_controls", "risk_controls"),
        ("live_ticker_validation_results_review_package_digest", "live_ticker_validation_results_review_package_digest"),
    ],
)
def test_validator_rejects_missing_required_review_sections(field: str, match: str):
    package = _package()
    package.pop(field)

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match=match,
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_target_universe_mismatch():
    package = _package()
    package["target_universe"] = package["target_universe"][:-1]

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match="target_universe",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_non_validated_read_only_target():
    package = _package()
    package["per_ticker_identity_plan_entries"][0]["live_validation_status"] = "FAILED"

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match="live_validation_status",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_digest_mismatch():
    package = _package()
    package[
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    ] = "0" * 64

    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match="review_package_digest",
    ):
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            package
        )


def test_markdown_includes_required_sections():
    markdown = (
        review.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_markdown_v1(
            _package()
        )
    )

    for section in (
        "## Title",
        "## Reviewed Expanded Universe Identity Authority Plan Candidate",
        "## Source Live Ticker Validation Results",
        "## Target Universe",
        "## Identity Authority Plan Objective",
        "## Per-Ticker Identity Plan Entries",
        "## Identity Fields to Bind",
        "## Evidence Limitations",
        "## Future Identity Authority Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Authority Boundary",
        "## Acquisition Boundary",
        "## Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = (
        review.write_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            tmp_path
        )
    )

    assert result["artifact_kind"] == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert result["payload_sha256"]
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written["artifact_kind"] == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    with pytest.raises(
        review.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError,
        match="already exists",
    ):
        review.write_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
            tmp_path
        )


def test_services_package_exports_review_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1 is (
        review.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1
    )
    assert services.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1 is (
        review.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1
    )
    assert services.write_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1 is (
        review.write_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_markdown_v1 is (
        review.build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_markdown_v1
    )
    assert services.expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1 is (
        review.expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1
    )
