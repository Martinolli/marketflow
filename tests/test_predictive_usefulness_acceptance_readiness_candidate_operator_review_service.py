from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import (
    predictive_usefulness_acceptance_readiness_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_predictive_usefulness_acceptance_readiness_candidate_review_package_v1()


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] = review.predictive_usefulness_acceptance_readiness_candidate_review_package_digest_v1(
        package
    )
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("readiness candidate must not be rebuilt by status binding")

    monkeypatch.setattr(
        review.readiness_service,
        "build_predictive_usefulness_acceptance_readiness_candidate_v1",
        fail_if_called,
    )

    assert _package()["provider_requests_made_in_review"] is False


def test_artifact_kind_is_acceptance_readiness_candidate_review_package():
    assert _package()["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == (
        review.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_readiness_candidate_digest_matches_expected():
    assert _package()["reviewed_readiness_candidate_digest"] == (
        review.EXPECTED_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
    )


def test_readiness_candidate_status_remains_not_ready():
    assert _package()["reviewed_readiness_candidate_status"] == (
        review.readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_REQUIRES_ADDITIONAL_EVIDENCE
    )


def test_assessment_candidate_review_digest_is_bound():
    assert _package()["predictive_usefulness_assessment_candidate_review_package_digest"] == (
        review.EXPECTED_ASSESSMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )


def test_assessment_candidate_digest_is_bound():
    assert _package()["predictive_usefulness_assessment_candidate_digest"] == (
        review.EXPECTED_ASSESSMENT_CANDIDATE_DIGEST
    )


def test_predictive_experiment_results_review_digest_is_bound():
    assert _package()["predictive_experiment_results_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_predictive_experiment_execution_digest_is_bound():
    assert _package()["predictive_experiment_execution_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )


def test_predictive_experiment_execution_approval_digest_is_bound():
    assert _package()["predictive_experiment_execution_approval_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )


def test_predictive_experiment_plan_digest_is_bound():
    assert _package()["predictive_experiment_plan_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )


def test_predictive_experiment_plan_review_package_digest_is_bound():
    assert _package()["predictive_experiment_plan_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
    )


def test_swing_registry_approval_digest_is_bound():
    assert _package()["swing_registry_approval_digest"] == (
        review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_position_swing_registry_approval_digest_is_bound():
    assert _package()["position_swing_registry_approval_digest"] == (
        review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_acceptance_readiness_state_is_not_ready():
    assert _package()["acceptance_readiness_state"] == (
        review.ACCEPTANCE_READINESS_STATE_NOT_READY
    )


def test_predictive_evidence_available_for_review_is_true():
    assert _package()["predictive_evidence_available_for_review"] is True


def test_predictive_evidence_sufficient_for_acceptance_is_false():
    assert _package()["predictive_evidence_sufficient_for_acceptance"] is False


def test_ready_for_acceptance_candidate_is_false():
    assert _package()["ready_for_acceptance_candidate"] is False


def test_reasons_acceptance_is_not_ready_are_populated():
    assert _package()["acceptance_not_ready_reasons"] == review.NOT_READY_REASONS


def test_additional_evidence_required_list_is_populated():
    assert _package()["additional_evidence_required"] == review.ADDITIONAL_EVIDENCE_REQUIRED


def test_next_gates_list_is_populated():
    assert _package()["next_gates"] == review.NEXT_GATES


def test_predictive_usefulness_remains_not_accepted():
    assert _package()["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false():
    assert _package()["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_acceptance_recommended_remains_false():
    assert _package()["predictive_usefulness_acceptance_recommended"] is False


def test_predictive_usefulness_acceptance_candidate_created_remains_false():
    assert _package()["predictive_usefulness_acceptance_candidate_created"] is False


def test_predictive_usefulness_acceptance_ceremony_required_is_true():
    assert _package()["predictive_usefulness_acceptance_ceremony_required"] is True


def test_profitability_remains_not_accepted():
    assert _package()["profitability"] == "not accepted"


def test_profitability_acceptance_ready_remains_false():
    assert _package()["profitability_acceptance_ready"] is False


def test_profitability_acceptance_recommended_remains_false():
    assert _package()["profitability_acceptance_recommended"] is False


def test_runtime_migration_recommended_remains_false():
    assert _package()["runtime_migration_recommended"] is False


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == review.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == review.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == review.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == review.NOT_AUTHORIZED


def test_new_strategy_scoring_remains_false():
    assert _package()["new_strategy_scoring_performed"] is False


def test_trade_recommendations_generated_remains_false():
    assert _package()["trade_recommendations_generated"] is False


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
    assert summary["ready_for_acceptance_candidate"] is False


def test_review_package_digest_is_deterministic():
    assert _package()[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] == _package()[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ]


def test_validator_accepts_valid_review_package():
    validation = (
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            _package()
        )
    )

    assert validation["status"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert validation["ready_for_acceptance_candidate"] is False


def test_validator_rejects_modified_readiness_candidate_digest():
    package = deepcopy(_package())
    package["reviewed_readiness_candidate_digest"] = "0" * 64
    _redigest(package)

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_validator_rejects_readiness_status_changed_away_from_not_ready():
    package = deepcopy(_package())
    package["reviewed_readiness_candidate_status"] = "READY_FOR_ACCEPTANCE"
    _redigest(package)

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


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
        ("provider_requests_made_in_review", True),
        ("experiment_reexecution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_forbidden_values(field: str, value: Any):
    package = deepcopy(_package())
    package[field] = value

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_validator_rejects_profitability_acceptance_recommended_true():
    package = deepcopy(_package())
    package["profitability_acceptance_recommended"] = True

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_validator_rejects_readiness_state_ready_or_accepted():
    package = deepcopy(_package())
    package["acceptance_readiness_state"] = "READY_FOR_ACCEPTANCE"
    _redigest(package)

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_validator_rejects_predictive_evidence_sufficient_for_acceptance_true():
    package = deepcopy(_package())
    package["predictive_evidence_sufficient_for_acceptance"] = True

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_validator_rejects_ready_for_acceptance_candidate_true():
    package = deepcopy(_package())
    package["ready_for_acceptance_candidate"] = True

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize("field", ["additional_evidence_required", "next_gates"])
def test_validator_rejects_missing_required_lists(field: str):
    package = deepcopy(_package())
    package.pop(field)
    _redigest(package)

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "predictive_usefulness_assessment_candidate_review_package_digest",
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_digests(field: str):
    package = deepcopy(_package())
    package.pop(field)
    if field != "predictive_usefulness_acceptance_readiness_candidate_review_package_digest":
        _redigest(package)

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.validate_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            package
        )


def test_markdown_writer_includes_required_sections():
    markdown = review.build_predictive_usefulness_acceptance_readiness_candidate_review_markdown_v1(
        _package()
    )

    for section in [
        "## Title",
        "## Reviewed Acceptance Readiness Candidate",
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
    output_path = (
        tmp_path
        / "predictive_usefulness_acceptance_readiness_candidate_review_package_v1.json"
    )
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(
        review.PredictiveUsefulnessAcceptanceReadinessCandidateReviewPackageError
    ):
        review.write_predictive_usefulness_acceptance_readiness_candidate_review_package_v1(
            tmp_path
        )
