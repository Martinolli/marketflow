from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_evidence_improvement_candidate_operator_review_service as review


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review.build_predictive_evidence_improvement_candidate_review_package_v1()


def test_review_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_predictive_evidence_improvement_candidate_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_accepts_exact_supplied_candidate() -> None:
    source = review.candidate_service.build_predictive_evidence_improvement_candidate_v1()
    package = review.build_predictive_evidence_improvement_candidate_review_package_v1(
        source
    )
    assert package["reviewed_predictive_evidence_improvement_candidate_digest"] == (
        source["predictive_evidence_improvement_candidate_digest"]
    )


def test_artifact_schema_and_status(review_package: dict) -> None:
    assert review_package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE
    )
    assert review_package["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_V1
    )
    assert review_package["review_status"] == (
        review.PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_reviewed_candidate_identity_and_checklist_are_bound(review_package: dict) -> None:
    assert review_package["reviewed_predictive_evidence_improvement_candidate_kind"] == (
        review.candidate_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE
    )
    assert review_package["reviewed_predictive_evidence_improvement_candidate_status"] == (
        review.candidate_service.PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW
    )
    assert review_package["reviewed_predictive_evidence_improvement_candidate_digest"] == review.EXPECTED_CANDIDATE_DIGEST
    assert review_package["reviewed_predictive_evidence_improvement_candidate_checklist_total"] == 60
    assert review_package["reviewed_predictive_evidence_improvement_candidate_checklist_passed"] == 60
    assert review_package["reviewed_predictive_evidence_improvement_candidate_checklist_failed"] == 0
    assert review_package["reviewed_predictive_evidence_improvement_candidate_blocker_count"] == 0


def test_all_source_digests_are_bound(review_package: dict) -> None:
    expected = {
        "predictive_evidence_improvement_candidate_digest": review.EXPECTED_CANDIDATE_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_digest": review.EXPECTED_READINESS_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_review_package_digest": review.EXPECTED_REASSESSMENT_REVIEW_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": review.EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": review.EXPECTED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_digest": review.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "research_registry_approval_digest": review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": review.EXPECTED_RECORDS_DIGEST,
    }
    assert {key: review_package[key] for key in expected} == expected


def test_target_universe_is_exact_and_ordered(review_package: dict) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_readiness_failure_summary_is_preserved(review_package: dict) -> None:
    assert review_package["reviewed_readiness_failure_summary"] == {
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
    }


def test_evidence_basis_is_preserved(review_package: dict) -> None:
    assert review_package["reviewed_evidence_basis"] == {
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


def test_improvement_objective_scope_mode_and_authority_are_preserved(
    review_package: dict,
) -> None:
    assert review_package["predictive_evidence_improvement_objective"] == (
        review.candidate_service.IMPROVEMENT_OBJECTIVE
    )
    assert review_package["predictive_evidence_improvement_scope"] == (
        review.candidate_service.IMPROVEMENT_SCOPE
    )
    assert review_package["predictive_evidence_improvement_mode"] == (
        review.PLANNED_NOT_EXECUTED
    )
    assert review_package["predictive_evidence_improvement_authority_status"] == (
        review.NOT_AUTHORIZED
    )


def test_all_improvement_themes_are_reviewed_without_mutation(review_package: dict) -> None:
    themes = review_package["reviewed_improvement_themes"]
    assert [row["theme_id"] for row in themes] == review.candidate_service.IMPROVEMENT_THEME_IDS
    assert all(row["status"] == review.PLANNED_NOT_EXECUTED for row in themes)
    assert all(row["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for row in themes)
    assert all(row["evidence_classification"] == "NOT_ACCEPTANCE_EVIDENCE" for row in themes)


def test_all_refinement_options_are_reviewed_without_mutation(review_package: dict) -> None:
    options = review_package["reviewed_refinement_options"]
    assert [row["option_id"] for row in options] == review.candidate_service.REFINEMENT_OPTION_IDS
    assert all(row["status"] == review.PLANNED_NOT_EXECUTED for row in options)
    assert all(row["requires_separate_operator_review"] is True for row in options)
    assert all(row["requires_separate_execution_approval"] is True for row in options)


def test_per_ticker_entries_preserve_counts_and_digests(review_package: dict) -> None:
    entries = review_package["per_ticker_improvement_candidate_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    assert len({row["per_ticker_predictive_evidence_improvement_candidate_review_digest"] for row in entries}) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["improvement_note"] == (
            "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG"
            if is_meta
            else None
        )
        assert row["readiness_status"] == "NOT_READY"
        assert row["improvement_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW"
        assert row["improvement_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT"
        assert row["source_predictive_evidence_improvement_candidate_digest"] == review.EXPECTED_CANDIDATE_DIGEST
        assert len(row["per_ticker_predictive_evidence_improvement_candidate_digest"]) == 64
        assert row["per_ticker_predictive_evidence_improvement_candidate_review_digest"] == review.per_ticker_predictive_evidence_improvement_candidate_review_digest_v1(row)
        assert row["runtime_use"] == review.NOT_AUTHORIZED


def test_future_chain_gates_and_controls_are_preserved(review_package: dict) -> None:
    assert review_package["reviewed_future_improvement_chain"] == review.candidate_service.FUTURE_IMPROVEMENT_CHAIN
    assert review_package["reviewed_future_gates"] == review.candidate_service.FUTURE_GATES
    assert review_package["reviewed_risk_controls"] == review.candidate_service.RISK_CONTROLS


def test_planned_outputs_are_preserved_and_not_generated(review_package: dict) -> None:
    assert review_package["planned_output_count"] == 7
    assert [row["output_name"] for row in review_package["reviewed_planned_outputs"]] == review.candidate_service.PLANNED_OUTPUT_NAMES
    assert review_package["planned_outputs_status"] == review.PLANNED_NOT_GENERATED
    assert review_package["planned_outputs_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE


@pytest.mark.parametrize(
    "field,expected",
    [
        ("provider_requests_made_in_review", False),
        ("live_provider_transport_enabled_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("canonical_dataset_regenerated_in_review", False),
        ("predictive_execution_rerun_performed", False),
        ("label_generation_rerun_performed", False),
        ("feature_matrix_rerun_performed", False),
        ("walk_forward_validation_rerun_performed", False),
        ("out_of_sample_evaluation_rerun_performed", False),
        ("metrics_recomputation_performed", False),
        ("improvement_execution_performed", False),
        ("refinement_option_execution_performed", False),
        ("model_comparison_performed", False),
        ("predictive_evidence_improvement_approved", False),
        ("predictive_evidence_improvement_executed", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("label_generation_authorized", False),
        ("label_generation_performed", False),
        ("feature_matrix_generation_authorized", False),
        ("feature_matrix_generation_performed", False),
        ("walk_forward_validation_authorized", False),
        ("walk_forward_validation_performed", False),
        ("out_of_sample_evaluation_authorized", False),
        ("out_of_sample_evaluation_performed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", review.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", review.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("profitability_acceptance_recommended", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", review.NOT_AUTHORIZED),
        ("strategy_use", review.NOT_AUTHORIZED),
        ("paper_trading", review.NOT_AUTHORIZED),
        ("broker_execution", review.NOT_AUTHORIZED),
        ("automatic_stitching", False),
        ("feature_label_refinement_plan_candidate_created", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
    ],
)
def test_closed_execution_and_authority_boundaries(
    review_package: dict, field: str, expected: object
) -> None:
    assert review_package[field] == expected


def test_checklist_is_complete_and_all_checks_pass(review_package: dict) -> None:
    checklist = review_package["review_checklist"]
    assert [row["check_id"] for row in checklist] == review.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == review.PASS for row in checklist)


def test_summary_counts_and_boundaries(review_package: dict) -> None:
    assert review_package["review_summary"] == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_assessment": True,
        "ready_for_feature_label_refinement_candidate": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_review_and_per_ticker_digests_are_deterministic(review_package: dict) -> None:
    second = review.build_predictive_evidence_improvement_candidate_review_package_v1()
    assert second == review_package
    assert len(review_package["predictive_evidence_improvement_candidate_review_package_digest"]) == 64
    assert [row["per_ticker_predictive_evidence_improvement_candidate_review_digest"] for row in second["per_ticker_improvement_candidate_review_entries"]] == [row["per_ticker_predictive_evidence_improvement_candidate_review_digest"] for row in review_package["per_ticker_improvement_candidate_review_entries"]]


def test_validator_accepts_valid_review(review_package: dict) -> None:
    result = review.validate_predictive_evidence_improvement_candidate_review_package_v1(
        review_package
    )
    assert result["status"] == "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert result["per_ticker_review_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_operator_assessment"] is True
    assert result["predictive_evidence_improvement_authorized"] is False


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_predictive_evidence_improvement_candidate_digest", "0" * 64),
        ("reviewed_predictive_evidence_improvement_candidate_status", "WRONG"),
        ("predictive_usefulness_acceptance_readiness_review_digest", "0" * 64),
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "WRONG"),
        ("predictive_evidence_improvement_candidate_created", False),
        ("predictive_evidence_improvement_candidate_review_created", False),
        ("predictive_evidence_improvement_authority_status", "AUTHORIZED"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("predictive_evidence_improvement_approved", True),
        ("predictive_evidence_improvement_executed", True),
        ("improvement_execution_performed", True),
        ("refinement_option_execution_performed", True),
        ("model_comparison_performed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("predictive_execution_rerun_performed", True),
        ("label_generation_rerun_performed", True),
        ("feature_matrix_rerun_performed", True),
        ("walk_forward_validation_rerun_performed", True),
        ("out_of_sample_evaluation_rerun_performed", True),
        ("metrics_recomputation_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("feature_label_refinement_plan_candidate_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
    ],
)
def test_validator_rejects_changed_top_level_contract(
    review_package: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid[field] = bad_value
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.validate_predictive_evidence_improvement_candidate_review_package_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_improvement_themes",
        "reviewed_refinement_options",
        "reviewed_future_improvement_chain",
        "reviewed_future_gates",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_review_structure(
    review_package: dict, field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid.pop(field)
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.validate_predictive_evidence_improvement_candidate_review_package_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    ["stability_consistency_required", "baseline_outperformance_consistency_required"],
)
def test_validator_rejects_failed_criterion_marked_pass(
    review_package: dict, field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_readiness_failure_summary"][field] = review.PASS
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.validate_predictive_evidence_improvement_candidate_review_package_v1(
            invalid
        )


def test_validator_rejects_missing_or_changed_review_digest(review_package: dict) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(review_package)
        if replacement is None:
            invalid.pop("predictive_evidence_improvement_candidate_review_package_digest")
        else:
            invalid["predictive_evidence_improvement_candidate_review_package_digest"] = replacement
        with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
            review.validate_predictive_evidence_improvement_candidate_review_package_v1(
                invalid
            )


def test_validator_rejects_missing_candidate_or_review_ticker_digest(
    review_package: dict,
) -> None:
    for field in (
        "per_ticker_predictive_evidence_improvement_candidate_digest",
        "per_ticker_predictive_evidence_improvement_candidate_review_digest",
    ):
        invalid = deepcopy(review_package)
        invalid["per_ticker_improvement_candidate_review_entries"][0].pop(field)
        with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
            review.validate_predictive_evidence_improvement_candidate_review_package_v1(
                invalid
            )


def test_validator_rejects_missing_check_or_fabricated_summary(review_package: dict) -> None:
    missing_check = deepcopy(review_package)
    missing_check["review_checklist"].pop()
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.validate_predictive_evidence_improvement_candidate_review_package_v1(
            missing_check
        )
    fabricated = deepcopy(review_package)
    fabricated["review_summary"]["passed_checks"] = 0
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.validate_predictive_evidence_improvement_candidate_review_package_v1(
            fabricated
        )


def test_markdown_contains_required_sections(review_package: dict) -> None:
    markdown = review.build_predictive_evidence_improvement_candidate_review_markdown_v1(
        review_package
    )
    for heading in (
        "Title",
        "Predictive Evidence Improvement Candidate Review Package",
        "Reviewed Improvement Candidate",
        "Source Acceptance Readiness Review",
        "Readiness Failure Summary",
        "Evidence Basis",
        "Reviewed Improvement Themes",
        "Reviewed Refinement Options",
        "Per-Ticker Improvement Candidate Review Entries",
        "Future Improvement Chain",
        "Future Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_uses_canonical_json_and_does_not_overwrite(tmp_path: Path) -> None:
    result = review.write_predictive_evidence_improvement_candidate_review_package_v1(
        tmp_path
    )
    path = Path(result["path"])
    package = json.loads(path.read_text(encoding="utf-8"))
    payload = canonical_json_bytes(package)
    assert path.read_bytes() == payload
    assert result["payload_sha256"] == sha256_bytes(payload)
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.write_predictive_evidence_improvement_candidate_review_package_v1(tmp_path)


@pytest.mark.parametrize("filename", ["nested/review.json", "review.txt", "../review.json"])
def test_writer_rejects_unsafe_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(review.PredictiveEvidenceImprovementCandidateReviewError):
        review.write_predictive_evidence_improvement_candidate_review_package_v1(
            tmp_path, filename=filename
        )
