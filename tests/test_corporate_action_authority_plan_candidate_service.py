from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from marketflow.services import corporate_action_authority_plan_candidate_service as plan


EXPECTED_CANDIDATE_DIGEST = (
    "3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a"
)


def _candidate() -> dict[str, Any]:
    return plan.build_corporate_action_authority_plan_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        plan.approval_service.review_service.candidate_service.freeze_service.review_service.candidate_service.plan_review.plan.results_review.provider,
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
        plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE
    )
    assert candidate["candidate_status"] == (
        plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert candidate["corporate_action_authority_plan_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )


def test_source_evidence_digests_are_bound():
    candidate = _candidate()

    assert candidate["post_identity_freeze_registry_inventory_approval_digest"] == (
        plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
    )
    assert candidate["post_identity_freeze_registry_inventory_candidate_review_package_digest"] == (
        plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["post_identity_freeze_registry_inventory_candidate_digest"] == (
        plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
    )
    assert candidate["identity_authority_freeze_digest"] == (
        plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
    )
    assert candidate["identity_authority_candidate_review_package_digest"] == (
        plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["live_ticker_validation_results_review_package_digest"] == (
        plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["ticker_universe_selection_approval_digest"] == (
        plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
    )


def test_target_universe_identity_and_registry_inventory_are_bound():
    candidate = _candidate()

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == plan.VALIDATION_TARGET_UNIVERSE
    assert candidate["identity_inventory_universe"] == plan.VALIDATION_TARGET_UNIVERSE
    assert candidate["identity_authority_frozen"] is True
    assert candidate["post_identity_freeze_registry_inventory_approved"] is True
    assert candidate["authority_scope"] == (
        plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY
    )


def test_corporate_action_plan_objective_scope_mode_and_creation_status():
    candidate = _candidate()

    assert candidate["corporate_action_authority_plan_objective"] == (
        plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE
    )
    assert candidate["corporate_action_authority_plan_scope"] == (
        plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE
    )
    assert candidate["corporate_action_authority_plan_mode"] == (
        plan.CORPORATE_ACTION_AUTHORITY_PLAN_MODE
    )
    assert candidate["corporate_action_authority_creation_status"] == (
        plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS
    )
    assert candidate["plan_scope"] == plan.PLAN_SCOPE


def test_per_ticker_corporate_action_plan_entries_are_planned_not_authority():
    candidate = _candidate()
    entries = candidate["per_ticker_corporate_action_plan_entries"]

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == plan.VALIDATION_TARGET_UNIVERSE
    for entry in entries:
        assert entry["identity_authority_status"] == (
            plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
        )
        assert entry["registry_inventory_status"] == (
            plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        )
        assert entry["corporate_action_plan_status"] == plan.PLANNED_NOT_CREATED
        assert entry["split_event_authority_status"] == plan.NOT_CREATED
        assert entry["dividend_event_authority_status"] == plan.NOT_CREATED
        assert entry["corporate_action_authority_created"] is False
        assert entry["acquisition_precondition_status"] == (
            plan.BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN
        )
        assert entry["dataset_generation_authorized"] is False
        assert len(entry["source_identity_freeze_digest"]) == 64
        assert len(entry["source_registry_inventory_approval_digest"]) == 64
        assert len(entry["source_per_ticker_registry_inventory_approval_digest_if_available"]) == 64
        assert len(entry["per_ticker_corporate_action_plan_digest"]) == 64


def test_evidence_requirements_future_chains_gates_and_risk_controls_are_defined():
    candidate = _candidate()

    assert candidate["corporate_action_evidence_requirements"] == (
        plan.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS
    )
    assert candidate["corporate_action_evidence_requirement_policy"] == (
        plan.CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY
    )
    assert candidate["future_split_event_authority_chain"] == (
        plan.FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN
    )
    assert candidate["future_dividend_event_authority_chain"] == (
        plan.FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN
    )
    assert candidate["future_corporate_action_readiness_chain"] == (
        plan.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
    )
    assert candidate["future_gates"] == plan.FUTURE_GATES
    assert candidate["risk_controls"] == plan.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only():
    outputs = _candidate()["planned_outputs"]

    assert len(outputs) == 9
    assert {item["generation_status"] for item in outputs} == {
        plan.PLANNED_NOT_GENERATED
    }
    assert {item["actionability"] for item in outputs} == {
        plan.RESEARCH_ONLY_NON_ACTIONABLE
    }


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "corporate_action_authority_plan_review_created",
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
    assert _candidate()[field] is False


def test_predictive_profitability_and_runtime_authorizations_remain_closed():
    candidate = _candidate()
    not_authorized = (
        plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    )

    assert candidate["predictive_usefulness"] == plan.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert candidate["profitability"] == plan.acquisition.PROFITABILITY_NOT_ACCEPTED
    assert candidate["runtime_use"] == not_authorized
    assert candidate["strategy_use"] == not_authorized
    assert candidate["paper_trading"] == not_authorized
    assert candidate["broker_execution"] == not_authorized


def test_summary_keeps_future_authority_candidates_not_ready():
    summary = _candidate()["plan_summary"]

    assert summary == {
        "total_checks": 79,
        "passed_checks": 79,
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
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


def test_checklist_contains_all_required_ids_and_passes():
    candidate = _candidate()

    assert [item["check_id"] for item in candidate["plan_checklist"]] == (
        plan.REQUIRED_CHECK_IDS
    )
    assert {item["status"] for item in candidate["plan_checklist"]} == {plan.PASS}


def test_candidate_and_per_ticker_plan_digests_are_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["corporate_action_authority_plan_candidate_digest"] == (
        second["corporate_action_authority_plan_candidate_digest"]
    )
    assert [
        entry["per_ticker_corporate_action_plan_digest"]
        for entry in first["per_ticker_corporate_action_plan_entries"]
    ] == [
        entry["per_ticker_corporate_action_plan_digest"]
        for entry in second["per_ticker_corporate_action_plan_entries"]
    ]


def test_validator_accepts_valid_candidate():
    validation = plan.validate_corporate_action_authority_plan_candidate_v1(_candidate())

    assert validation["status"] == "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_VALID"
    assert validation["blocker_count"] == 0
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_corporate_action_authority_plan_approval"] is False
    assert validation["ready_for_split_event_authority_candidate"] is False
    assert validation["ready_for_dividend_event_authority_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(plan.VALIDATION_TARGET_UNIVERSE))),
        ("identity_authority_frozen", False),
        ("post_identity_freeze_registry_inventory_approved", False),
        ("corporate_action_authority_plan_scope", "AUTHORITY"),
        ("corporate_action_authority_plan_mode", "AUTHORITY"),
        ("corporate_action_authority_creation_status", "CREATED"),
    ],
)
def test_validator_rejects_invalid_top_level_fields(field: str, value: Any):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "corporate_action_authority_plan_approved",
        "corporate_action_authority_created",
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
    candidate = _candidate()
    candidate[field] = True

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


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

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


def test_validator_rejects_per_ticker_plan_count_not_12():
    candidate = _candidate()
    candidate["per_ticker_corporate_action_plan_entries"] = candidate[
        "per_ticker_corporate_action_plan_entries"
    ][:-1]

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_plan_digest():
    candidate = _candidate()
    candidate["per_ticker_corporate_action_plan_entries"][0].pop(
        "per_ticker_corporate_action_plan_digest"
    )

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "corporate_action_evidence_requirements",
        "future_split_event_authority_chain",
        "future_dividend_event_authority_chain",
        "future_corporate_action_readiness_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_planning_sections(field: str):
    candidate = _candidate()
    candidate[field] = []

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "post_identity_freeze_registry_inventory_approval_digest",
        "post_identity_freeze_registry_inventory_candidate_digest",
        "corporate_action_authority_plan_candidate_digest",
    ],
)
def test_validator_rejects_missing_or_wrong_candidate_digests(field: str):
    candidate = _candidate()
    candidate[field] = "0" * 64

    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.validate_corporate_action_authority_plan_candidate_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = plan.build_corporate_action_authority_plan_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
        "## Source Identity Registry Inventory Approval",
        "## Target Universe",
        "## Corporate-Action Authority Plan Objective",
        "## Per-Ticker Corporate-Action Plan Entries",
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
    ]:
        assert section in markdown


def test_write_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = plan.write_corporate_action_authority_plan_candidate_v1(tmp_path)

    assert Path(result["path"]).exists()
    assert result["filename"] == "corporate_action_authority_plan_candidate_v1.json"
    assert result["corporate_action_authority_plan_candidate_digest"] == (
        EXPECTED_CANDIDATE_DIGEST
    )
    with pytest.raises(plan.CorporateActionAuthorityPlanCandidateError):
        plan.write_corporate_action_authority_plan_candidate_v1(tmp_path)


def test_services_package_exports_plan_candidate_helpers():
    from marketflow import services

    assert services.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE == (
        plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE
    )
    assert services.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW == (
        plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_corporate_action_authority_plan_candidate_v1 is (
        plan.build_corporate_action_authority_plan_candidate_v1
    )
    assert services.validate_corporate_action_authority_plan_candidate_v1 is (
        plan.validate_corporate_action_authority_plan_candidate_v1
    )
    assert services.write_corporate_action_authority_plan_candidate_v1 is (
        plan.write_corporate_action_authority_plan_candidate_v1
    )
    assert services.build_corporate_action_authority_plan_candidate_markdown_v1 is (
        plan.build_corporate_action_authority_plan_candidate_markdown_v1
    )
    assert services.corporate_action_authority_plan_candidate_digest_v1 is (
        plan.corporate_action_authority_plan_candidate_digest_v1
    )
