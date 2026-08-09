from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import (
    additional_predictive_evidence_plan_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_additional_predictive_evidence_plan_candidate_review_package_v1()


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["additional_predictive_evidence_plan_candidate_review_package_digest"] = (
        review.additional_predictive_evidence_plan_candidate_review_package_digest_v1(
            package
        )
    )
    return package


def test_review_package_builds_offline_without_rebuilding_plan_candidate(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("plan candidate must not be rebuilt by status binding")

    monkeypatch.setattr(
        review.plan_service,
        "build_additional_predictive_evidence_plan_candidate_v1",
        fail_if_called,
    )

    assert _package()["provider_requests_made_in_review"] is False


def test_artifact_kind_is_additional_predictive_evidence_plan_candidate_review_package():
    assert _package()["artifact_kind"] == (
        review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_reviewed_plan_candidate_digest_matches_expected():
    assert _package()["reviewed_plan_candidate_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
    )


def test_reviewed_plan_candidate_status_remains_ready_for_review():
    assert _package()["reviewed_plan_candidate_status"] == (
        review.plan_service.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_READY_FOR_OPERATOR_REVIEW
    )


def test_reviewed_plan_candidate_checklist_has_zero_blockers():
    package = _package()

    assert package["reviewed_plan_candidate_checklist_total"] == 53
    assert package["reviewed_plan_candidate_checklist_passed"] == 53
    assert package["reviewed_plan_candidate_checklist_failed"] == 0
    assert package["reviewed_plan_candidate_blocker_count"] == 0


def test_source_readiness_digests_are_bound():
    package = _package()

    assert package["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_usefulness_acceptance_readiness_candidate_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )
    assert package["predictive_usefulness_assessment_candidate_review_package_digest"] == (
        review.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_usefulness_assessment_candidate_digest"] == (
        review.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
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
    assert package["predictive_experiment_plan_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )
    assert package["predictive_experiment_plan_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
    )
    assert package["swing_registry_approval_digest"] == (
        review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert package["position_swing_registry_approval_digest"] == (
        review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_acceptance_readiness_basis_remains_not_ready():
    package = _package()

    assert package["acceptance_readiness_state"] == review.ACCEPTANCE_READINESS_STATE_NOT_READY
    assert package["acceptance_readiness_reason"] == (
        review.ACCEPTANCE_READINESS_REASON_RESEARCH_ONLY_LIMITED
    )
    assert package["predictive_evidence_available_for_review"] is True
    assert package["predictive_evidence_sufficient_for_acceptance"] is False
    assert package["ready_for_acceptance_candidate"] is False


def test_gaps_phases_outputs_gates_and_controls_are_bound():
    package = _package()

    assert package["gaps_addressed"] == review.GAPS_ADDRESSED
    assert package["gap_count"] == 12
    assert package["plan_phases"] == review.PLAN_PHASES
    assert package["plan_phase_count"] == 10
    assert package["planned_outputs"] == review._planned_outputs()
    assert package["planned_output_count"] == 10
    assert package["future_execution_gates"] == review.FUTURE_EXECUTION_GATES
    assert package["future_gate_count"] == 12
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert package["risk_control_count"] == 11


def test_all_reviewed_outputs_are_planned_not_generated_and_research_only():
    package = _package()

    assert package["planned_outputs_status"] == review.PLANNED_NOT_GENERATED
    assert package["planned_outputs_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE
    assert {item["generation_status"] for item in package["planned_outputs"]} == {
        review.PLANNED_NOT_GENERATED
    }
    assert {item["actionability_label"] for item in package["planned_outputs"]} == {
        review.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_execution_and_rerun_flags_remain_false():
    package = _package()

    for field in [
        "provider_requests_made_in_review",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ]:
        assert package[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed():
    package = _package()

    assert package["predictive_usefulness"] == "not accepted"
    assert package["predictive_usefulness_acceptance_ready"] is False
    assert package["predictive_usefulness_acceptance_recommended"] is False
    assert package["predictive_usefulness_acceptance_candidate_created"] is False
    assert package["profitability"] == "not accepted"
    assert package["profitability_acceptance_ready"] is False
    assert package["profitability_acceptance_recommended"] is False
    assert package["runtime_migration_recommended"] is False
    assert package["runtime_migration_approved"] is False
    assert package["runtime_migration_active"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED
    assert package["automatic_stitching"] is False


def test_no_follow_on_acceptance_or_runtime_artifacts_are_created():
    package = _package()

    assert package["additional_predictive_evidence_execution_artifact_created"] is False
    assert package["predictive_usefulness_acceptance_candidate_artifact_created"] is False
    assert package["predictive_usefulness_acceptance_artifact_created"] is False
    assert package["profitability_acceptance_artifact_created"] is False
    assert package["runtime_migration_approval_artifact_created"] is False


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
    assert summary["ready_for_additional_evidence_execution_candidate"] is False
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    assert _package()[
        "additional_predictive_evidence_plan_candidate_review_package_digest"
    ] == _package()["additional_predictive_evidence_plan_candidate_review_package_digest"]


def test_validator_accepts_valid_review_package():
    validation = (
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            _package()
        )
    )

    assert validation["status"] == (
        "ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_additional_evidence_execution_candidate"] is False
    assert validation["ready_for_predictive_usefulness_acceptance_candidate"] is False


def test_review_package_can_bind_valid_plan_candidate_object():
    candidate = review.plan_service.build_additional_predictive_evidence_plan_candidate_v1()
    package = review.build_additional_predictive_evidence_plan_candidate_review_package_v1(
        candidate=candidate
    )

    assert package["plan_candidate_binding_mode"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_OBJECT_BINDING
    )
    assert package["reviewed_plan_candidate_digest"] == (
        candidate["additional_predictive_evidence_plan_candidate_digest"]
    )


def test_review_package_uses_status_binding_by_default():
    assert _package()["plan_candidate_binding_mode"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_STATUS_BINDING
    )


def test_validator_rejects_modified_plan_candidate_digest():
    package = deepcopy(_package())
    package["reviewed_plan_candidate_digest"] = "0" * 64
    _redigest(package)

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_plan_status_changed_away_from_ready_for_review():
    package = deepcopy(_package())
    package["reviewed_plan_candidate_status"] = "EXECUTION_READY"
    _redigest(package)

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


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
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    package = deepcopy(_package())
    package[field] = value

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_execution_artifact_created",
        "predictive_usefulness_acceptance_candidate_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ],
)
def test_validator_rejects_created_follow_on_artifacts(field: str):
    package = deepcopy(_package())
    package[field] = True

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "gaps_addressed",
        "plan_phases",
        "future_execution_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_plan_lists(field: str):
    package = deepcopy(_package())
    package.pop(field)
    _redigest(package)

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_plan_candidate_digest",
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    package = deepcopy(_package())
    package.pop(field)
    if field != "additional_predictive_evidence_plan_candidate_review_package_digest":
        _redigest(package)

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


def test_validator_rejects_missing_review_package_digest():
    package = deepcopy(_package())
    package.pop("additional_predictive_evidence_plan_candidate_review_package_digest")

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.validate_additional_predictive_evidence_plan_candidate_review_package_v1(
            package
        )


def test_markdown_writer_includes_required_sections():
    markdown = review.build_additional_predictive_evidence_plan_candidate_review_markdown_v1(
        _package()
    )

    for section in [
        "## Title",
        "## Reviewed Additional Predictive Evidence Plan Candidate",
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
    output_path = (
        tmp_path
        / "additional_predictive_evidence_plan_candidate_review_package_v1.json"
    )
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(review.AdditionalPredictiveEvidencePlanCandidateReviewPackageError):
        review.write_additional_predictive_evidence_plan_candidate_review_package_v1(
            tmp_path
        )


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = review.write_additional_predictive_evidence_plan_candidate_review_package_v1(
        tmp_path
    )

    assert result["filename"] == (
        "additional_predictive_evidence_plan_candidate_review_package_v1.json"
    )
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_additional_predictive_evidence_plan_candidate_review_package_v1 is (
        review.build_additional_predictive_evidence_plan_candidate_review_package_v1
    )
