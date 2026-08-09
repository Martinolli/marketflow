from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_plan_candidate_service as plan,
)


def _candidate() -> dict[str, Any]:
    return plan.build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1()


def _mutated_candidate(field: str, value: Any) -> dict[str, Any]:
    candidate = _candidate()
    candidate[field] = value
    return candidate


def test_plan_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        plan.results_review.provider,
        "fetch_massive_ticker_details_v1",
        fail_provider_call,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["live_validation_rerun_performed"] is False
    assert candidate["live_provider_transport_enabled"] is False


def test_artifact_kind_status_and_schema_are_exact():
    candidate = _candidate()

    assert candidate["artifact_kind"] == (
        plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert candidate["schema_version"] == (
        plan.SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_V1
    )


def test_source_digest_chain_is_bound():
    candidate = _candidate()

    assert candidate["live_ticker_validation_results_review_package_digest"] == (
        plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["live_ticker_validation_execution_digest"] == (
        plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
    )
    assert candidate["live_ticker_validation_approval_digest"] == (
        plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
    )
    assert candidate["ticker_universe_selection_approval_digest"] == (
        plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )
    assert candidate["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        plan.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_validated_universe_and_counts_are_preserved():
    candidate = _candidate()

    assert candidate["validation_target_universe"] == plan.VALIDATION_TARGET_UNIVERSE
    assert candidate["validation_target_count"] == 12
    assert candidate["provider_request_count"] == 12
    assert candidate["successful_provider_response_count"] == 12
    assert candidate["failed_provider_response_count"] == 0
    assert candidate["all_targets_validated_read_only"] is True


def test_per_ticker_identity_plan_entries_are_complete_and_not_created():
    entries = _candidate()["per_ticker_identity_plan_entries"]

    assert [entry["ticker"] for entry in entries] == plan.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["live_validation_status"] == plan.VALIDATED_READ_ONLY
        assert entry["identity_authority_plan_status"] == plan.PLANNED_NOT_CREATED
        assert entry["identity_candidate_status"] == plan.NOT_CREATED
        assert entry["identity_review_status"] == plan.NOT_CREATED
        assert entry["identity_freeze_status"] == plan.NOT_FROZEN
        assert entry["identity_authority_created"] is False
        assert entry["identity_fields_to_bind"] == plan.IDENTITY_FIELDS_TO_BIND
        assert entry["identity_evidence_source"] == plan.IDENTITY_EVIDENCE_SOURCE
        assert entry["identity_evidence_limitations"] == plan.IDENTITY_EVIDENCE_LIMITATIONS
        assert entry["next_required_identity_gate"] == plan.NEXT_REQUIRED_IDENTITY_GATE


def test_identity_fields_field_groups_limitations_future_gates_and_risk_controls_are_defined():
    candidate = _candidate()

    assert candidate["identity_fields_to_bind"] == plan.IDENTITY_FIELDS_TO_BIND
    assert candidate["identity_field_groups"] == plan.IDENTITY_FIELD_GROUPS
    assert list(candidate["identity_field_groups"]) == [
        "core_symbol_identity_fields",
        "provider_reference_identity_fields",
        "security_classification_fields",
        "exchange_and_market_fields",
        "provider_cross_reference_fields",
        "audit_digest_fields",
        "limitation_fields",
    ]
    assert candidate["identity_evidence_limitations"] == plan.IDENTITY_EVIDENCE_LIMITATIONS
    assert candidate["future_gates"] == plan.FUTURE_GATES
    assert candidate["risk_controls"] == plan.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    outputs = _candidate()["planned_outputs"]

    assert [item["output_id"] for item in outputs] == plan.PLANNED_OUTPUT_IDS
    assert {item["generation_status"] for item in outputs} == {plan.PLANNED_NOT_GENERATED}
    assert {item["actionability_label"] for item in outputs} == {
        plan.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
        "identity_authority_created",
        "identity_candidate_created",
        "identity_review_created",
        "identity_freeze_created",
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
        "identity_authority_candidate_created",
        "identity_authority_freeze_created",
        "corporate_action_authority_created_in_this_task",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ],
)
def test_closed_boolean_boundaries_remain_false(field: str):
    assert _candidate()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == plan.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert candidate["profitability"] == plan.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert candidate["runtime_use"] == plan.NOT_AUTHORIZED
    assert candidate["strategy_use"] == plan.NOT_AUTHORIZED
    assert candidate["paper_trading"] == plan.NOT_AUTHORIZED
    assert candidate["broker_execution"] == plan.NOT_AUTHORIZED


def test_checklist_and_summary_are_complete():
    candidate = _candidate()
    summary = candidate["plan_summary"]

    assert [item["check_id"] for item in candidate["plan_checklist"]] == plan.REQUIRED_CHECK_IDS
    assert {item["status"] for item in candidate["plan_checklist"]} == {plan.PASS}
    assert summary["total_checks"] == len(plan.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(plan.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_per_ticker_identity_authority_candidate"] is False
    assert summary["identity_authority_created"] is False
    assert summary["identity_freeze_created"] is False
    assert summary["ready_for_acquisition"] is False
    assert summary["ready_for_dataset_generation"] is False


def test_plan_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["expanded_universe_per_ticker_identity_authority_plan_candidate_digest"] == (
        second["expanded_universe_per_ticker_identity_authority_plan_candidate_digest"]
    )
    assert first["expanded_universe_per_ticker_identity_authority_plan_candidate_digest"] == (
        plan.expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_candidate():
    validation = plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
        _candidate()
    )

    assert validation["status"] == (
        "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_VALID"
    )
    assert validation["candidate_status"] == (
        plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_per_ticker_identity_authority_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "IDENTITY_AUTHORITY_CANDIDATE", "artifact_kind"),
        ("candidate_status", "IDENTITY_AUTHORITY_CREATED", "candidate_status"),
        ("validation_target_count", 11, "validation_target_count"),
        ("all_targets_validated_read_only", False, "all_targets_validated_read_only"),
        ("identity_authority_plan_mode", "CREATED", "identity_authority_plan_mode"),
        ("identity_authority_creation_status", "CREATED", "identity_authority_creation_status"),
        ("identity_freeze_status", "FROZEN", "identity_freeze_status"),
        ("provider_requests_made", True, "provider_requests_made"),
        ("live_validation_rerun_performed", True, "live_validation_rerun_performed"),
        ("new_ticker_authority_created", True, "new_ticker_authority_created"),
        ("new_ticker_acquisition_authorized", True, "new_ticker_acquisition_authorized"),
        ("dataset_generation_authorized", True, "dataset_generation_authorized"),
        ("corporate_action_authority_created", True, "corporate_action_authority_created"),
        ("acquisition_generation_authorized", True, "acquisition_generation_authorized"),
        ("canonical_dataset_authorized", True, "canonical_dataset_authorized"),
        ("registry_approval_created", True, "registry_approval_created"),
        ("additional_predictive_evidence_execution_authorized", True, "additional_predictive_evidence_execution_authorized"),
        ("predictive_experiment_rerun_performed", True, "predictive_experiment_rerun_performed"),
        ("trade_recommendations_generated", True, "trade_recommendations_generated"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("predictive_usefulness_acceptance_ready", True, "predictive_usefulness_acceptance_ready"),
        ("profitability", "accepted", "profitability"),
        ("profitability_acceptance_ready", True, "profitability_acceptance_ready"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
    ],
)
def test_validator_rejects_invalid_candidate_mutations(field: str, value: Any, match: str):
    candidate = _mutated_candidate(field, value)

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match=match,
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_validator_rejects_nested_artifact_kind_creation():
    candidate = _candidate()
    candidate["planned_outputs"][0]["artifact_kind"] = "IDENTITY_AUTHORITY_CANDIDATE"

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="artifact kind",
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_validator_rejects_per_ticker_identity_creation():
    candidate = _candidate()
    candidate["per_ticker_identity_plan_entries"][0]["identity_authority_created"] = True

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="identity_authority_created",
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_validator_rejects_missing_digest():
    candidate = _candidate()
    candidate.pop("expanded_universe_per_ticker_identity_authority_plan_candidate_digest")

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="expanded_universe_per_ticker_identity_authority_plan_candidate_digest",
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_validator_rejects_digest_mismatch():
    candidate = _candidate()
    candidate["expanded_universe_per_ticker_identity_authority_plan_candidate_digest"] = "0" * 64

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="expanded_universe_per_ticker_identity_authority_plan_candidate_digest",
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_validator_rejects_external_mutation_after_checklist_created():
    candidate = _candidate()
    candidate["planned_outputs"][0]["generation_status"] = "GENERATED"

    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="planned_outputs",
    ):
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            candidate
        )


def test_markdown_includes_required_sections():
    markdown = plan.build_expanded_universe_per_ticker_identity_authority_plan_candidate_markdown_v1(
        _candidate()
    )

    for section in (
        "## Title",
        "## Purpose",
        "## Plan Artifact",
        "## Bound Source Evidence",
        "## Validated Expanded Universe",
        "## Identity Plan Boundary",
        "## Per-Ticker Identity Plan",
        "## Identity Fields To Bind",
        "## Identity Field Groups",
        "## Identity Evidence Limitations",
        "## Future Identity Authority Chain",
        "## Future Gates",
        "## Planned Outputs",
        "## Risk Controls",
        "## Authority Boundary",
        "## Acquisition And Dataset Boundary",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_write_plan_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = plan.write_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
        tmp_path
    )

    assert result["artifact_kind"] == (
        plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
    )
    assert result["payload_sha256"]
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written["artifact_kind"] == (
        plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
    )
    with pytest.raises(
        plan.ExpandedUniversePerTickerIdentityAuthorityPlanCandidateError,
        match="already exists",
    ):
        plan.write_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(
            tmp_path
        )


def test_mutating_returned_candidate_does_not_change_future_builds():
    candidate = _candidate()
    candidate["identity_fields_to_bind"].append("unexpected_field")
    candidate["per_ticker_identity_plan_entries"][0]["identity_fields_to_bind"].append(
        "unexpected_field"
    )

    fresh = _candidate()

    assert fresh["identity_fields_to_bind"] == plan.IDENTITY_FIELDS_TO_BIND
    assert fresh["per_ticker_identity_plan_entries"][0]["identity_fields_to_bind"] == (
        plan.IDENTITY_FIELDS_TO_BIND
    )


def test_services_package_exports_plan_candidate_helpers():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE == (
        plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
    )
    assert services.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW == (
        plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1 is (
        plan.build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1
    )
    assert services.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1 is (
        plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1
    )
    assert services.write_expanded_universe_per_ticker_identity_authority_plan_candidate_v1 is (
        plan.write_expanded_universe_per_ticker_identity_authority_plan_candidate_v1
    )
    assert services.build_expanded_universe_per_ticker_identity_authority_plan_candidate_markdown_v1 is (
        plan.build_expanded_universe_per_ticker_identity_authority_plan_candidate_markdown_v1
    )
    assert services.expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1 is (
        plan.expanded_universe_per_ticker_identity_authority_plan_candidate_digest_v1
    )
