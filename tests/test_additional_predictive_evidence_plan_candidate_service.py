from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import additional_predictive_evidence_plan_candidate_service as plan


def _candidate() -> dict[str, Any]:
    return plan.build_additional_predictive_evidence_plan_candidate_v1()


def _redigest(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["plan_checklist"] = plan._checklist(candidate)
    candidate["plan_summary"] = plan._summary(candidate["plan_checklist"])
    candidate["additional_predictive_evidence_plan_candidate_digest"] = (
        plan.additional_predictive_evidence_plan_candidate_digest_v1(candidate)
    )
    return candidate


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("additional evidence plan must not rebuild readiness review")

    monkeypatch.setattr(
        plan.readiness_review,
        "build_predictive_usefulness_acceptance_readiness_candidate_review_package_v1",
        fail_if_called,
    )

    assert _candidate()["provider_requests_made"] is False


def test_artifact_kind_is_additional_predictive_evidence_plan_candidate():
    assert _candidate()["artifact_kind"] == (
        plan.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE
    )


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == (
        plan.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW
    )


def test_readiness_review_digest_is_bound():
    assert _candidate()[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] == plan.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST


def test_readiness_candidate_digest_is_bound():
    assert _candidate()["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        plan.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )


def test_assessment_review_and_candidate_digests_are_bound():
    candidate = _candidate()

    assert candidate["predictive_usefulness_assessment_candidate_review_package_digest"] == (
        plan.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["predictive_usefulness_assessment_candidate_digest"] == (
        plan.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
    )


def test_predictive_experiment_results_review_digest_is_bound():
    assert _candidate()["predictive_experiment_results_review_package_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_experiment_execution_digest_is_bound():
    assert _candidate()["predictive_experiment_execution_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )


def test_predictive_experiment_plan_digest_is_bound():
    assert _candidate()["predictive_experiment_plan_digest"] == (
        plan.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
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


@pytest.mark.parametrize(
    "gap",
    [
        "single_ticker_scope",
        "simplified_chronological_split",
        "failure_warning_counts_unavailable",
        "no_transaction_cost_model",
        "no_slippage_model",
        "no_multi_ticker_or_out_of_domain_generalization",
    ],
)
def test_required_gaps_are_addressed(gap: str):
    assert gap in _candidate()["gaps_addressed"]


def test_plan_phases_are_defined():
    candidate = _candidate()

    assert candidate["plan_phases"] == plan.PLAN_PHASES
    assert len(candidate["plan_phases"]) == 10
    assert all(item["execution_required"] is False for item in candidate["plan_phases"])
    assert all(
        item["operator_approval_required_before_execution"] is True
        for item in candidate["plan_phases"]
    )
    assert all(
        item["runtime_authorization_required"] is False
        for item in candidate["plan_phases"]
    )


def test_planned_outputs_are_not_generated():
    assert {
        item["generation_status"] for item in _candidate()["planned_outputs"]
    } == {plan.PLANNED_NOT_GENERATED}


def test_planned_outputs_are_research_only_non_actionable():
    assert {
        item["actionability_label"] for item in _candidate()["planned_outputs"]
    } == {plan.RESEARCH_ONLY_NON_ACTIONABLE}


def test_future_execution_gates_are_defined():
    assert _candidate()["future_execution_gates"] == plan.FUTURE_EXECUTION_GATES


def test_risk_controls_are_defined():
    assert _candidate()["risk_controls"] == plan.RISK_CONTROLS


def test_provider_requests_made_remains_false():
    assert _candidate()["provider_requests_made"] is False


def test_additional_predictive_evidence_execution_authorized_remains_false():
    assert _candidate()["additional_predictive_evidence_execution_authorized"] is False


def test_additional_predictive_evidence_executed_remains_false():
    assert _candidate()["additional_predictive_evidence_executed"] is False


def test_predictive_experiment_rerun_authorized_remains_false():
    assert _candidate()["predictive_experiment_rerun_authorized"] is False


def test_predictive_experiment_rerun_performed_remains_false():
    assert _candidate()["predictive_experiment_rerun_performed"] is False


def test_walk_forward_rerun_performed_remains_false():
    assert _candidate()["walk_forward_rerun_performed"] is False


def test_label_regeneration_performed_remains_false():
    assert _candidate()["label_regeneration_performed"] is False


def test_feature_matrix_regeneration_performed_remains_false():
    assert _candidate()["feature_matrix_regeneration_performed"] is False


def test_new_strategy_scoring_remains_false():
    assert _candidate()["new_strategy_scoring_performed"] is False


def test_trade_recommendations_generated_remains_false():
    assert _candidate()["trade_recommendations_generated"] is False


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


def test_profitability_acceptance_ready_remains_false():
    assert _candidate()["profitability_acceptance_ready"] is False


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
    assert summary["ready_for_additional_evidence_execution_candidate"] is False
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_candidate_digest_is_deterministic():
    assert _candidate()["additional_predictive_evidence_plan_candidate_digest"] == (
        _candidate()["additional_predictive_evidence_plan_candidate_digest"]
    )


def test_validator_accepts_valid_candidate():
    validation = plan.validate_additional_predictive_evidence_plan_candidate_v1(
        _candidate()
    )

    assert validation["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_VALID"
    assert validation["ready_for_additional_evidence_execution_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
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
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    candidate = deepcopy(_candidate())
    candidate[field] = value

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_validator_rejects_predictive_usefulness_acceptance_recommended_true():
    candidate = deepcopy(_candidate())
    candidate["predictive_usefulness_acceptance_recommended"] = True

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_validator_rejects_profitability_acceptance_ready_true():
    candidate = deepcopy(_candidate())
    candidate["profitability_acceptance_ready"] = True

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_validator_rejects_profitability_acceptance_recommended_true():
    candidate = deepcopy(_candidate())
    candidate["profitability_acceptance_recommended"] = True

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_validator_rejects_missing_readiness_review_digest():
    candidate = deepcopy(_candidate())
    candidate.pop("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")
    _redigest(candidate)

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["plan_phases", "future_execution_gates", "risk_controls"])
def test_validator_rejects_missing_required_plan_lists(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    _redigest(candidate)

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = deepcopy(_candidate())
    candidate.pop("additional_predictive_evidence_plan_candidate_digest")

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.validate_additional_predictive_evidence_plan_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = plan.build_additional_predictive_evidence_plan_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
        "## Source Readiness Evidence",
        "## Gaps Addressed",
        "## Plan Phases",
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
    output_path = tmp_path / "additional_predictive_evidence_plan_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(plan.AdditionalPredictiveEvidencePlanCandidateError):
        plan.write_additional_predictive_evidence_plan_candidate_v1(tmp_path)


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE == (
        plan.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE
    )
    assert services.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW == (
        plan.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert services.build_additional_predictive_evidence_plan_candidate_v1 is (
        plan.build_additional_predictive_evidence_plan_candidate_v1
    )
