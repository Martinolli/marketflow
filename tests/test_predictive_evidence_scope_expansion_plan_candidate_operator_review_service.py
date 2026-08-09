from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import (
    predictive_evidence_scope_expansion_plan_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1()


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] = (
        review.predictive_evidence_scope_expansion_plan_candidate_review_package_digest_v1(
            package
        )
    )
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("scope expansion candidate must not be rebuilt by status binding")

    monkeypatch.setattr(
        review.plan_service,
        "build_predictive_evidence_scope_expansion_plan_candidate_v1",
        fail_if_called,
    )

    assert _package()["provider_requests_made_in_review"] is False


def test_artifact_kind_is_scope_expansion_plan_candidate_review_package():
    assert _package()["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == (
        review.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_scope_expansion_candidate_digest_matches_expected():
    assert _package()["reviewed_scope_expansion_candidate_digest"] == (
        review.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
    )


def test_scope_expansion_candidate_checklist_has_zero_blockers():
    package = _package()

    assert package["reviewed_scope_expansion_candidate_checklist_total"] == 57
    assert package["reviewed_scope_expansion_candidate_checklist_passed"] == 57
    assert package["reviewed_scope_expansion_candidate_checklist_failed"] == 0
    assert package["reviewed_scope_expansion_candidate_blocker_count"] == 0


def test_source_evidence_digests_are_bound():
    package = _package()

    assert package["additional_predictive_evidence_plan_candidate_review_package_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["additional_predictive_evidence_plan_candidate_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
    )
    assert package["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )


def test_predictive_experiment_and_registry_digests_are_bound():
    package = _package()

    assert package["predictive_experiment_results_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_experiment_execution_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )
    assert package["predictive_experiment_execution_approval_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )
    assert package["swing_registry_approval_digest"] == (
        review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert package["position_swing_registry_approval_digest"] == (
        review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_scope_expansion_objective_and_mode_match():
    package = _package()

    assert package["scope_expansion_objective"] == review.SCOPE_EXPANSION_OBJECTIVE
    assert package["scope_expansion_mode"] == review.PLANNED_NOT_AUTHORIZED


def test_single_ticker_and_generalization_gaps_are_addressed():
    gaps = _package()["scope_gaps_addressed"]

    assert "single_ticker_scope" in gaps
    assert "no_multi_ticker_or_out_of_domain_generalization" in gaps


def test_expansion_dimension_count_is_10():
    package = _package()

    assert package["dimension_count"] == 10
    assert package["expansion_dimensions"] == review.EXPANSION_DIMENSIONS


def test_ticker_selection_policy_is_criteria_defined_selection_not_performed():
    package = _package()

    assert package["ticker_selection_policy_status"] == (
        review.CRITERIA_DEFINED_SELECTION_NOT_PERFORMED
    )
    assert package["ticker_selection_policy"] == review._ticker_selection_policy()


def test_candidate_ticker_list_is_not_bound():
    assert _package()["candidate_ticker_list_status"] == review.NOT_BOUND


def test_approved_expanded_ticker_universe_is_empty():
    assert _package()["approved_expanded_ticker_universe"] == []


def test_future_ticker_authority_chain_has_15_steps():
    package = _package()

    assert package["future_ticker_authority_chain_step_count"] == 15
    assert package["future_ticker_authority_chain"] == review._future_ticker_authority_chain()


def test_planned_outputs_count_is_10():
    assert _package()["planned_output_count"] == 10


def test_planned_outputs_are_not_generated():
    assert {item["generation_status"] for item in _package()["planned_outputs"]} == {
        review.PLANNED_NOT_GENERATED
    }


def test_planned_outputs_are_research_only_non_actionable():
    assert {item["actionability_label"] for item in _package()["planned_outputs"]} == {
        review.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_future_gates_count_is_14():
    package = _package()

    assert package["future_gate_count"] == 14
    assert package["future_gates"] == review.FUTURE_GATES


def test_risk_controls_count_is_14():
    package = _package()

    assert package["risk_control_count"] == 14
    assert package["risk_controls"] == review.RISK_CONTROLS


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_candidate_created",
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
def test_review_execution_and_authority_flags_remain_false(field: str):
    assert _package()[field] is False


def test_predictive_usefulness_remains_not_accepted():
    assert _package()["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false():
    assert _package()["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_acceptance_recommended_remains_false():
    assert _package()["predictive_usefulness_acceptance_recommended"] is False


def test_predictive_usefulness_acceptance_candidate_created_remains_false():
    assert _package()["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_remains_not_accepted():
    assert _package()["profitability"] == "not accepted"


def test_runtime_migration_recommended_remains_false():
    assert _package()["runtime_migration_recommended"] is False


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_strategy_paper_and_broker_remain_not_authorized():
    package = _package()

    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED


def test_review_readiness_flags_remain_false():
    package = _package()

    assert package["ready_for_ticker_universe_selection_candidate"] is False
    assert package["ready_for_scope_expansion_execution"] is False
    assert package["ready_for_additional_evidence_execution_candidate"] is False
    assert package["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_checklist_contains_all_required_check_ids():
    package = _package()

    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_ready_review_package():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_ticker_universe_selection_candidate"] is False
    assert summary["ready_for_scope_expansion_execution"] is False
    assert summary["ready_for_additional_evidence_execution_candidate"] is False
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_review_package_digest_is_deterministic():
    assert _package()[
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
    ] == _package()["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"]


def test_validator_accepts_valid_review_package():
    validation = review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        _package()
    )

    assert validation["status"] == (
        "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_scope_expansion_execution"] is False


def test_review_package_can_bind_valid_candidate_object():
    candidate = review.plan_service.build_predictive_evidence_scope_expansion_plan_candidate_v1()
    package = review.build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        candidate=candidate
    )

    assert package["scope_expansion_candidate_binding_mode"] == (
        review.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_OBJECT_BINDING
    )
    assert package["reviewed_scope_expansion_candidate_digest"] == (
        candidate["predictive_evidence_scope_expansion_plan_candidate_digest"]
    )


def test_review_package_uses_status_binding_by_default():
    assert _package()["scope_expansion_candidate_binding_mode"] == (
        review.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_STATUS_BINDING
    )


def test_validator_rejects_modified_scope_expansion_candidate_digest():
    package = deepcopy(_package())
    package["reviewed_scope_expansion_candidate_digest"] = "0" * 64
    _redigest(package)

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_candidate_status_changed_away_from_ready():
    package = deepcopy(_package())
    package["reviewed_scope_expansion_candidate_status"] = "SCOPE_EXPANSION_APPROVED"
    _redigest(package)

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scope_expansion_authorized", True),
        ("expanded_ticker_universe_approved", True),
        ("ticker_universe_selection_candidate_created", True),
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
        ("provider_requests_made_in_review", True),
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
        ("ready_for_ticker_universe_selection_candidate", True),
        ("ready_for_scope_expansion_execution", True),
        ("ready_for_additional_evidence_execution_candidate", True),
        ("ready_for_predictive_usefulness_acceptance_candidate", True),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    package = deepcopy(_package())
    package[field] = value

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "scope_expansion_approval_artifact_created",
        "ticker_universe_selection_candidate_artifact_created",
        "expanded_ticker_universe_approval_artifact_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ],
)
def test_validator_rejects_created_follow_on_artifacts(field: str):
    package = deepcopy(_package())
    package[field] = True

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_approved_expanded_ticker_universe_not_empty():
    package = deepcopy(_package())
    package["approved_expanded_ticker_universe"] = ["MSFT"]

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_plan_candidate_review_package_digest",
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    package = deepcopy(_package())
    package.pop(field)
    if field != "predictive_evidence_scope_expansion_plan_candidate_review_package_digest":
        _redigest(package)

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


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
    package = deepcopy(_package())
    package.pop(field)
    _redigest(package)

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.validate_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            package
        )


def test_markdown_writer_includes_required_sections():
    markdown = (
        review.build_predictive_evidence_scope_expansion_plan_candidate_review_markdown_v1(
            _package()
        )
    )

    for section in [
        "## Title",
        "## Reviewed Predictive Evidence Scope Expansion Plan",
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
    output_path = (
        tmp_path
        / "predictive_evidence_scope_expansion_plan_candidate_review_package_v1.json"
    )
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(review.PredictiveEvidenceScopeExpansionPlanCandidateReviewPackageError):
        review.write_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
            tmp_path
        )


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = review.write_predictive_evidence_scope_expansion_plan_candidate_review_package_v1(
        tmp_path
    )

    assert result["filename"] == (
        "predictive_evidence_scope_expansion_plan_candidate_review_package_v1.json"
    )
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1 is (
        review.build_predictive_evidence_scope_expansion_plan_candidate_review_package_v1
    )
