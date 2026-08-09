from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_usefulness_acceptance_readiness_candidate_service as service


def _candidate() -> dict[str, Any]:
    return service.build_predictive_usefulness_acceptance_readiness_candidate_v1()


def _redigest(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["readiness_checklist"] = service._checklist(candidate)
    candidate["readiness_summary"] = service._summary(candidate["readiness_checklist"])
    candidate["predictive_usefulness_acceptance_readiness_candidate_digest"] = (
        service.predictive_usefulness_acceptance_readiness_candidate_digest_v1(candidate)
    )
    return candidate


def test_readiness_candidate_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("acceptance readiness must not rebuild assessment evidence")

    monkeypatch.setattr(
        service.assessment_review,
        "build_predictive_usefulness_assessment_candidate_review_package_v1",
        fail_if_called,
    )

    assert _candidate()["provider_requests_made"] is False


def test_artifact_kind_is_acceptance_readiness_candidate():
    assert _candidate()["artifact_kind"] == (
        service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE
    )


def test_candidate_status_is_not_ready_requires_additional_evidence():
    assert _candidate()["candidate_status"] == (
        service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE
    )


def test_assessment_candidate_review_digest_is_bound():
    assert _candidate()["predictive_usefulness_assessment_candidate_review_package_digest"] == (
        service.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_assessment_candidate_digest_is_bound():
    assert _candidate()["predictive_usefulness_assessment_candidate_digest"] == (
        service.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
    )


def test_predictive_experiment_results_review_digest_is_bound():
    assert _candidate()["predictive_experiment_results_review_package_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_experiment_execution_digest_is_bound():
    assert _candidate()["predictive_experiment_execution_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )


def test_predictive_experiment_execution_approval_digest_is_bound():
    assert _candidate()["predictive_experiment_execution_approval_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )


def test_predictive_experiment_plan_digest_is_bound():
    assert _candidate()["predictive_experiment_plan_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert _candidate()["swing_registry_approval_digest"] == (
        service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert _candidate()["position_swing_registry_approval_digest"] == (
        service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_output_count_is_thirteen():
    assert _candidate()["output_count"] == 13


def test_outputs_are_research_only_non_actionable():
    assert _candidate()["all_outputs_research_only_non_actionable"] is True


def test_metrics_label_is_not_acceptance_evidence():
    candidate = _candidate()

    assert candidate["metrics_label"] == service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    assert "metrics_marked_not_acceptance_evidence" in candidate["acceptance_not_ready_reasons"]


def test_labels_generated_is_true():
    assert _candidate()["labels_generated"] is True


def test_feature_matrices_generated_is_true():
    assert _candidate()["feature_matrices_generated"] is True


def test_walk_forward_result_is_available():
    assert _candidate()["walk_forward_result_generated"] is True


def test_oos_result_is_available():
    assert _candidate()["out_of_sample_result_generated"] is True


def test_failure_warning_counts_unavailable_are_acknowledged():
    candidate = _candidate()

    assert candidate["failure_count_status"] == (
        service.assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS
    )
    assert candidate["warning_count_status"] == (
        service.assessment_review.candidate_service.UNAVAILABLE_IN_SOURCE_REPORTS
    )


def test_acceptance_readiness_state_is_not_ready():
    assert _candidate()["acceptance_readiness_state"] == (
        service.ACCEPTANCE_READINESS_STATE_NOT_READY
    )


def test_predictive_evidence_available_for_review_is_true():
    assert _candidate()["predictive_evidence_available_for_review"] is True


def test_predictive_evidence_sufficient_for_acceptance_is_false():
    assert _candidate()["predictive_evidence_sufficient_for_acceptance"] is False


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


def test_profitability_acceptance_recommended_remains_false():
    assert _candidate()["profitability_acceptance_recommended"] is False


def test_runtime_migration_recommended_remains_false():
    assert _candidate()["runtime_migration_recommended"] is False


def test_runtime_migration_approved_remains_false():
    assert _candidate()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _candidate()["runtime_migration_active"] is False


def test_runtime_use_remains_not_authorized():
    assert _candidate()["runtime_use"] == service.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _candidate()["strategy_use"] == service.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _candidate()["paper_trading"] == service.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _candidate()["broker_execution"] == service.NOT_AUTHORIZED


def test_new_strategy_scoring_remains_false():
    assert _candidate()["new_strategy_scoring_performed"] is False


def test_trade_recommendations_generated_remains_false():
    assert _candidate()["trade_recommendations_generated"] is False


def test_additional_evidence_required_list_is_populated():
    assert _candidate()["additional_evidence_required"] == service.ADDITIONAL_EVIDENCE_REQUIRED


def test_next_gates_list_is_populated():
    assert _candidate()["next_gates"] == service.NEXT_GATES


def test_checklist_contains_all_required_check_ids():
    candidate = _candidate()

    assert [item["check_id"] for item in candidate["readiness_checklist"]] == (
        service.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_readiness_candidate():
    assert {item["status"] for item in _candidate()["readiness_checklist"]} == {service.PASS}


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _candidate()["readiness_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_acceptance_candidate"] is False


def test_candidate_digest_is_deterministic():
    assert _candidate()["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        _candidate()["predictive_usefulness_acceptance_readiness_candidate_digest"]
    )


def test_validator_accepts_valid_candidate():
    validation = service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(
        _candidate()
    )

    assert validation["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_VALID"
    assert validation["ready_for_acceptance_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("provider_requests_made", True),
        ("experiment_reexecution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)


@pytest.mark.parametrize(
    "state",
    ["READY_FOR_ACCEPTANCE", "PREDICTIVE_USEFULNESS_ACCEPTED"],
)
def test_validator_rejects_acceptance_readiness_state_ready_or_accepted(state: str):
    candidate = deepcopy(_candidate())
    candidate["acceptance_readiness_state"] = state
    _redigest(candidate)

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)


def test_validator_rejects_predictive_evidence_sufficient_for_acceptance_true():
    candidate = _candidate()
    candidate["predictive_evidence_sufficient_for_acceptance"] = True

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)


@pytest.mark.parametrize("field", ["additional_evidence_required", "next_gates"])
def test_validator_rejects_missing_required_lists(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    _redigest(candidate)

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "predictive_usefulness_assessment_candidate_review_package_digest",
        "predictive_usefulness_acceptance_readiness_candidate_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    if field != "predictive_usefulness_acceptance_readiness_candidate_digest":
        _redigest(candidate)

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.validate_predictive_usefulness_acceptance_readiness_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = service.build_predictive_usefulness_acceptance_readiness_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
        "## Source Assessment Evidence",
        "## Readiness Classification",
        "## Reasons Acceptance Is Not Ready",
        "## Additional Evidence Required",
        "## Next Gates",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "predictive_usefulness_acceptance_readiness_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessCandidateError):
        service.write_predictive_usefulness_acceptance_readiness_candidate_v1(tmp_path)
