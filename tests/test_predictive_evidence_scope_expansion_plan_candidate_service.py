from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import predictive_evidence_scope_expansion_plan_candidate_service as plan


def _candidate() -> dict[str, Any]:
    return plan.build_predictive_evidence_scope_expansion_plan_candidate_v1()


def _redigest(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["plan_checklist"] = plan._checklist(candidate)
    candidate["plan_summary"] = plan._summary(candidate["plan_checklist"])
    candidate["predictive_evidence_scope_expansion_plan_candidate_digest"] = (
        plan.predictive_evidence_scope_expansion_plan_candidate_digest_v1(candidate)
    )
    return candidate


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("scope expansion plan must not rebuild review package")

    monkeypatch.setattr(
        plan.additional_review,
        "build_additional_predictive_evidence_plan_candidate_review_package_v1",
        fail_if_called,
    )

    assert _candidate()["provider_requests_made"] is False


def test_artifact_kind_is_predictive_evidence_scope_expansion_plan_candidate():
    assert _candidate()["artifact_kind"] == (
        plan.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE
    )


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == (
        plan.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW
    )


def test_additional_predictive_evidence_plan_review_digest_is_bound():
    assert _candidate()["additional_predictive_evidence_plan_candidate_review_package_digest"] == (
        plan.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_additional_predictive_evidence_plan_candidate_digest_is_bound():
    assert _candidate()["additional_predictive_evidence_plan_candidate_digest"] == (
        plan.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
    )


def test_acceptance_readiness_review_digest_is_bound():
    assert _candidate()["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"] == (
        plan.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
    )


def test_acceptance_readiness_candidate_digest_is_bound():
    assert _candidate()["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        plan.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )


def test_predictive_experiment_results_review_digest_is_bound():
    assert _candidate()["predictive_experiment_results_review_package_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_experiment_execution_digest_is_bound():
    assert _candidate()["predictive_experiment_execution_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )


def test_predictive_experiment_approval_digest_is_bound():
    assert _candidate()["predictive_experiment_execution_approval_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert _candidate()["swing_registry_approval_digest"] == (
        plan.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert _candidate()["position_swing_registry_approval_digest"] == (
        plan.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_readiness_state_is_not_ready():
    assert _candidate()["acceptance_readiness_state"] == (
        plan.ACCEPTANCE_READINESS_STATE_NOT_READY
    )


def test_predictive_evidence_sufficient_for_acceptance_is_false():
    assert _candidate()["predictive_evidence_sufficient_for_acceptance"] is False


def test_ready_for_acceptance_candidate_is_false():
    assert _candidate()["ready_for_acceptance_candidate"] is False


def test_scope_expansion_objective_is_defined():
    candidate = _candidate()

    assert candidate["scope_expansion_objective"] == plan.SCOPE_EXPANSION_OBJECTIVE
    assert candidate["scope_expansion_mode"] == plan.PLANNED_NOT_AUTHORIZED
    assert candidate["new_ticker_selection_status"] == plan.NOT_SELECTED
    assert candidate["new_ticker_authority_status"] == plan.NOT_CREATED
    assert candidate["new_data_acquisition_status"] == plan.NOT_AUTHORIZED


def test_single_ticker_scope_gap_is_addressed():
    assert "single_ticker_scope" in _candidate()["scope_gaps_addressed"]


def test_generalization_gap_is_addressed():
    assert (
        "no_multi_ticker_or_out_of_domain_generalization"
        in _candidate()["scope_gaps_addressed"]
    )


def test_single_asset_class_scope_gap_is_addressed():
    assert "single_asset_class_scope_if_applicable" in _candidate()["scope_gaps_addressed"]


def test_expansion_dimensions_are_defined():
    candidate = _candidate()

    assert candidate["expansion_dimensions"] == plan.EXPANSION_DIMENSIONS
    assert candidate["expansion_dimension_count"] == 10
    assert all(item["execution_required"] is False for item in candidate["expansion_dimensions"])
    assert all(
        item["operator_approval_required_before_execution"] is True
        for item in candidate["expansion_dimensions"]
    )


def test_ticker_selection_policy_is_defined():
    candidate = _candidate()

    assert candidate["ticker_selection_policy"] == plan._ticker_selection_policy()
    assert candidate["ticker_selection_policy_status"] == (
        plan.CRITERIA_DEFINED_SELECTION_NOT_PERFORMED
    )
    assert candidate["candidate_ticker_list_status"] == plan.NOT_BOUND
    assert candidate["minimum_additional_ticker_count"] == "planned"
    assert candidate["target_additional_ticker_count_range"] == "5_to_12"


def test_final_ticker_selection_is_not_performed():
    assert _candidate()["final_ticker_selection_performed"] is False


def test_approved_expanded_ticker_universe_is_empty():
    assert _candidate()["approved_expanded_ticker_universe"] == []


def test_future_ticker_authority_chain_is_defined():
    candidate = _candidate()

    assert candidate["future_ticker_authority_chain"] == plan._future_ticker_authority_chain()
    assert candidate["future_ticker_authority_chain_step_count"] == 15
    assert all(
        item["performed_in_this_task"] is False
        for item in candidate["future_ticker_authority_chain"]
    )


def test_planned_outputs_are_not_generated():
    assert {item["generation_status"] for item in _candidate()["planned_outputs"]} == {
        plan.PLANNED_NOT_GENERATED
    }


def test_planned_outputs_are_research_only_non_actionable():
    assert {item["actionability_label"] for item in _candidate()["planned_outputs"]} == {
        plan.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_future_gates_are_defined():
    candidate = _candidate()

    assert candidate["future_gates"] == plan.FUTURE_GATES
    assert candidate["future_gate_count"] == 14


def test_risk_controls_are_defined():
    candidate = _candidate()

    assert candidate["risk_controls"] == plan.RISK_CONTROLS
    assert candidate["risk_control_count"] == 14


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_ticker_validation_performed",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_authority_and_execution_flags_remain_false(field: str):
    assert _candidate()[field] is False


def test_predictive_usefulness_remains_not_accepted():
    assert _candidate()["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false():
    assert _candidate()["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_acceptance_recommended_remains_false():
    assert _candidate()["predictive_usefulness_acceptance_recommended"] is False


def test_predictive_usefulness_acceptance_candidate_created_remains_false():
    assert _candidate()["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_remains_not_accepted():
    assert _candidate()["profitability"] == "not accepted"


def test_runtime_migration_recommended_remains_false():
    assert _candidate()["runtime_migration_recommended"] is False


def test_runtime_migration_approved_remains_false():
    assert _candidate()["runtime_migration_approved"] is False


def test_runtime_use_remains_not_authorized():
    assert _candidate()["runtime_use"] == plan.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _candidate()["strategy_use"] == plan.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _candidate()["paper_trading"] == plan.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _candidate()["broker_execution"] == plan.NOT_AUTHORIZED


def test_checklist_contains_all_required_check_ids():
    candidate = _candidate()

    assert [item["check_id"] for item in candidate["plan_checklist"]] == (
        plan.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_accepted_plan():
    assert {item["status"] for item in _candidate()["plan_checklist"]} == {plan.PASS}


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _candidate()["plan_summary"]

    assert summary["total_checks"] == len(plan.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(plan.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_ticker_universe_selection_candidate"] is False
    assert summary["ready_for_scope_expansion_execution"] is False
    assert summary["ready_for_additional_evidence_execution_candidate"] is False
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_candidate_digest_is_deterministic():
    assert _candidate()["predictive_evidence_scope_expansion_plan_candidate_digest"] == (
        _candidate()["predictive_evidence_scope_expansion_plan_candidate_digest"]
    )


def test_validator_accepts_valid_candidate():
    validation = plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(
        _candidate()
    )

    assert validation["status"] == (
        "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_VALID"
    )
    assert validation["ready_for_scope_expansion_execution"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scope_expansion_authorized", True),
        ("expanded_ticker_universe_approved", True),
        ("final_ticker_selection_performed", True),
        ("live_ticker_validation_performed", True),
        ("new_ticker_authority_created", True),
        ("new_ticker_acquisition_authorized", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", True),
        ("walk_forward_rerun_performed", True),
        ("label_regeneration_performed", True),
        ("feature_matrix_regeneration_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("provider_requests_made", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_migration_active", True),
        ("strategy_runtime_migration", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    candidate = deepcopy(_candidate())
    candidate[field] = value

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


def test_validator_rejects_approved_expanded_ticker_universe_not_empty():
    candidate = deepcopy(_candidate())
    candidate["approved_expanded_ticker_universe"] = ["MSFT"]

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


def test_validator_rejects_wrong_artifact_kind():
    candidate = deepcopy(_candidate())
    candidate["artifact_kind"] = "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED"
    _redigest(candidate)

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


def test_validator_rejects_wrong_candidate_status():
    candidate = deepcopy(_candidate())
    candidate["candidate_status"] = "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED"
    _redigest(candidate)

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_plan_candidate_review_package_digest",
        "predictive_evidence_scope_expansion_plan_candidate_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    if field != "predictive_evidence_scope_expansion_plan_candidate_digest":
        _redigest(candidate)

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "expansion_dimensions",
        "ticker_selection_policy",
        "future_ticker_authority_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_plan_components(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    _redigest(candidate)

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.validate_predictive_evidence_scope_expansion_plan_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = plan.build_predictive_evidence_scope_expansion_plan_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
        "## Source Evidence",
        "## Scope Expansion Objective",
        "## Expansion Dimensions",
        "## Ticker Selection Policy",
        "## Required Authority Chain for Future Tickers",
        "## Planned Outputs",
        "## Future Gates",
        "## Risk Controls",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "predictive_evidence_scope_expansion_plan_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(plan.PredictiveEvidenceScopeExpansionPlanCandidateError):
        plan.write_predictive_evidence_scope_expansion_plan_candidate_v1(tmp_path)


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = plan.write_predictive_evidence_scope_expansion_plan_candidate_v1(tmp_path)

    assert result["filename"] == "predictive_evidence_scope_expansion_plan_candidate_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE == (
        plan.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE
    )
    assert services.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW == (
        plan.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_predictive_evidence_scope_expansion_plan_candidate_v1 is (
        plan.build_predictive_evidence_scope_expansion_plan_candidate_v1
    )
