from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    feature_label_refinement_plan_candidate_operator_review_service as review,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review.build_feature_label_refinement_plan_candidate_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_feature_label_refinement_plan_candidate_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_accepts_exact_supplied_candidate() -> None:
    source = review.candidate_service.build_feature_label_refinement_plan_candidate_v1()
    package = review.build_feature_label_refinement_plan_candidate_review_package_v1(
        source
    )
    assert package["reviewed_feature_label_refinement_plan_candidate_digest"] == (
        source["feature_label_refinement_plan_candidate_digest"]
    )


def test_artifact_schema_and_review_status(review_package: dict) -> None:
    assert review_package["artifact_kind"] == (
        review.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE
    )
    assert review_package["schema_version"] == (
        review.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_V1
    )
    assert review_package["review_status"] == (
        review.FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_reviewed_candidate_identity_and_checklist_are_bound(
    review_package: dict,
) -> None:
    assert review_package["reviewed_feature_label_refinement_plan_candidate_kind"] == (
        review.candidate_service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE
    )
    assert review_package["reviewed_feature_label_refinement_plan_candidate_status"] == (
        review.candidate_service.FEATURE_LABEL_REFINEMENT_PLAN_READY_FOR_OPERATOR_REVIEW
    )
    assert review_package["reviewed_feature_label_refinement_plan_candidate_digest"] == (
        review.EXPECTED_CANDIDATE_DIGEST
    )
    assert review_package[
        "reviewed_feature_label_refinement_plan_candidate_checklist_total"
    ] == 72
    assert review_package[
        "reviewed_feature_label_refinement_plan_candidate_checklist_passed"
    ] == 72
    assert review_package[
        "reviewed_feature_label_refinement_plan_candidate_checklist_failed"
    ] == 0
    assert review_package[
        "reviewed_feature_label_refinement_plan_candidate_blocker_count"
    ] == 0


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_label_refinement_plan_candidate_digest", review.EXPECTED_CANDIDATE_DIGEST),
        ("predictive_evidence_improvement_candidate_review_package_digest", review.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", review.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", review.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", review.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", review.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", review.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", review.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_all_source_evidence_digests_are_bound(
    review_package: dict, field: str, expected: str
) -> None:
    assert review_package[field] == expected


def test_target_universe_is_exact_and_ordered(review_package: dict) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_readiness_failure_basis_is_preserved(review_package: dict) -> None:
    assert review_package["reviewed_readiness_failure_basis"] == {
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


def test_plan_objective_scope_mode_and_authority_are_preserved(
    review_package: dict,
) -> None:
    assert review_package["feature_label_refinement_plan_objective"] == (
        review.candidate_service.PLAN_OBJECTIVE
    )
    assert review_package["feature_label_refinement_plan_scope"] == (
        review.candidate_service.PLAN_SCOPE
    )
    assert review_package["feature_label_refinement_plan_mode"] == (
        review.PLANNED_NOT_EXECUTED
    )
    assert review_package["feature_label_refinement_authority_status"] == (
        review.NOT_AUTHORIZED
    )
    assert review_package["feature_label_refinement_plan_candidate_created"] is True
    assert review_package["feature_label_refinement_plan_candidate_review_created"] is True


@pytest.mark.parametrize(
    "field,expected_ids",
    [
        ("reviewed_label_refinement_groups", review.candidate_service.LABEL_REFINEMENT_GROUP_IDS),
        ("reviewed_feature_refinement_groups", review.candidate_service.FEATURE_REFINEMENT_GROUP_IDS),
        ("reviewed_protocol_refinement_groups", review.candidate_service.PROTOCOL_REFINEMENT_GROUP_IDS),
        ("reviewed_model_comparison_groups", review.candidate_service.MODEL_COMPARISON_GROUP_IDS),
    ],
)
def test_refinement_groups_are_reviewed_without_mutation_or_authority(
    review_package: dict, field: str, expected_ids: list[str]
) -> None:
    groups = review_package[field]
    assert [row["group_id"] for row in groups] == expected_ids
    assert all(row["planning_status"] == review.PLANNED_NOT_EXECUTED for row in groups)
    assert all(row["authorization_status"] == review.NOT_AUTHORIZED for row in groups)
    assert all(row["execution_status"] == review.candidate_service.NOT_EXECUTED for row in groups)
    assert all(row["research_only"] is True for row in groups)
    assert all(row["non_actionable"] is True for row in groups)


def test_refinement_priority_is_reviewed_without_approval(review_package: dict) -> None:
    assert review_package["reviewed_refinement_priority"] == (
        review.candidate_service.REFINEMENT_PRIORITY
    )
    assert review_package["feature_label_refinement_plan_approved"] is False
    assert review_package["feature_label_refinement_authorized"] is False


def test_per_ticker_review_entries_preserve_counts_and_digests(
    review_package: dict,
) -> None:
    entries = review_package["per_ticker_refinement_plan_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    assert len(
        {
            row["per_ticker_feature_label_refinement_plan_candidate_review_digest"]
            for row in entries
        }
    ) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["registry_approval_status"] == "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
        assert row["canonical_dataset_status"] == "FROZEN"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["readiness_status"] == "NOT_READY"
        assert row["feature_label_refinement_plan_status"] == (
            "PLANNED_READY_FOR_OPERATOR_REVIEW"
        )
        assert row["feature_label_refinement_plan_review_status"] == (
            "READY_FOR_OPERATOR_ASSESSMENT"
        )
        assert row["refinement_authorized"] is False
        assert row["refinement_executed"] is False
        assert row["source_feature_label_refinement_plan_candidate_digest"] == (
            review.EXPECTED_CANDIDATE_DIGEST
        )
        assert len(
            row["per_ticker_feature_label_refinement_plan_candidate_digest"]
        ) == 64
        assert row[
            "per_ticker_feature_label_refinement_plan_candidate_review_digest"
        ] == review.per_ticker_feature_label_refinement_plan_candidate_review_digest_v1(
            row
        )
        assert row["predictive_usefulness"] == review.NOT_ACCEPTED
        assert row["profitability"] == review.NOT_ACCEPTED
        assert row["runtime_use"] == review.NOT_AUTHORIZED
        assert row["strategy_use"] == review.NOT_AUTHORIZED
        assert row["paper_trading"] == review.NOT_AUTHORIZED
        assert row["broker_execution"] == review.NOT_AUTHORIZED


def test_meta_limitation_is_preserved_exactly(review_package: dict) -> None:
    entries = review_package["per_ticker_refinement_plan_review_entries"]
    meta = next(row for row in entries if row["ticker"] == "META")
    others = [row for row in entries if row["ticker"] != "META"]
    assert meta["refinement_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
    )
    assert all("refinement_note" not in row for row in others)


def test_future_refinement_chain_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_future_refinement_chain"] == (
        review.candidate_service.FUTURE_REFINEMENT_CHAIN
    )


def test_future_gates_are_preserved(review_package: dict) -> None:
    assert review_package["reviewed_future_gates"] == review.candidate_service.FUTURE_GATES


def test_risk_controls_are_preserved(review_package: dict) -> None:
    assert review_package["reviewed_risk_controls"] == review.candidate_service.RISK_CONTROLS


def test_planned_outputs_remain_ungenerated_and_research_only(
    review_package: dict,
) -> None:
    assert review_package["planned_output_count"] == 7
    assert [row["output_name"] for row in review_package["reviewed_planned_outputs"]] == (
        review.candidate_service.PLANNED_OUTPUT_NAMES
    )
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
        ("label_refinement_execution_performed", False),
        ("feature_refinement_execution_performed", False),
        ("protocol_refinement_execution_performed", False),
        ("model_comparison_performed", False),
        ("refined_label_generation_authorized", False),
        ("refined_label_generation_performed", False),
        ("refined_feature_generation_authorized", False),
        ("refined_feature_generation_performed", False),
        ("refined_walk_forward_validation_authorized", False),
        ("refined_walk_forward_validation_performed", False),
        ("refined_out_of_sample_evaluation_authorized", False),
        ("refined_out_of_sample_evaluation_performed", False),
        ("refined_metrics_recomputation_authorized", False),
        ("refined_metrics_recomputation_performed", False),
        ("model_comparison_authorized", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
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
    ],
)
def test_execution_acceptance_and_runtime_boundaries_remain_closed(
    review_package: dict, field: str, expected: object
) -> None:
    assert review_package[field] == expected


def test_checklist_contains_all_required_check_ids(review_package: dict) -> None:
    assert [row["check_id"] for row in review_package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_and_summary_counts_match(review_package: dict) -> None:
    checklist = review_package["review_checklist"]
    summary = review_package["review_summary"]
    assert all(row["status"] == review.PASS for row in checklist)
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS) == 83
    assert summary["passed_checks"] == 83
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_feature_label_refinement_plan_approval"] is False
    assert summary["ready_for_feature_label_refinement_execution_candidate"] is False
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False


def test_review_package_digest_is_deterministic(review_package: dict) -> None:
    rebuilt = review.build_feature_label_refinement_plan_candidate_review_package_v1()
    assert rebuilt[
        "feature_label_refinement_plan_candidate_review_package_digest"
    ] == review_package[
        "feature_label_refinement_plan_candidate_review_package_digest"
    ]
    assert review_package[
        "feature_label_refinement_plan_candidate_review_package_digest"
    ] == review.feature_label_refinement_plan_candidate_review_package_digest_v1(
        review_package
    )


def test_per_ticker_review_digests_are_deterministic(review_package: dict) -> None:
    rebuilt = review.build_feature_label_refinement_plan_candidate_review_package_v1()
    assert [
        row["per_ticker_feature_label_refinement_plan_candidate_review_digest"]
        for row in rebuilt["per_ticker_refinement_plan_review_entries"]
    ] == [
        row["per_ticker_feature_label_refinement_plan_candidate_review_digest"]
        for row in review_package["per_ticker_refinement_plan_review_entries"]
    ]


def test_validator_accepts_valid_review_package(review_package: dict) -> None:
    result = review.validate_feature_label_refinement_plan_candidate_review_package_v1(
        review_package
    )
    assert result["status"] == (
        "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert result["blocker_count"] == 0
    assert result["ready_for_operator_assessment"] is True
    assert result["feature_label_refinement_authorized"] is False
    assert result["predictive_usefulness"] == review.NOT_ACCEPTED
    assert result["profitability"] == review.NOT_ACCEPTED


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_feature_label_refinement_plan_candidate_digest", "0" * 64),
        ("reviewed_feature_label_refinement_plan_candidate_status", "WRONG"),
        ("feature_label_refinement_plan_candidate_digest", "0" * 64),
        ("predictive_evidence_improvement_candidate_review_package_digest", "0" * 64),
        ("predictive_usefulness_acceptance_readiness_review_digest", "0" * 64),
        ("feature_label_refinement_plan_candidate_created", False),
        ("feature_label_refinement_plan_candidate_review_created", False),
        ("feature_label_refinement_authority_status", "AUTHORIZED"),
        ("refined_label_generation_authorized", True),
        ("refined_label_generation_performed", True),
        ("refined_feature_generation_authorized", True),
        ("refined_feature_generation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("label_refinement_execution_performed", True),
        ("feature_refinement_execution_performed", True),
        ("protocol_refinement_execution_performed", True),
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
        ("improvement_execution_performed", True),
        ("refinement_option_execution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_forbidden_top_level_mutations(
    review_package: dict, field: str, value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid[field] = value
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_label_refinement_groups",
        "reviewed_feature_refinement_groups",
        "reviewed_protocol_refinement_groups",
        "reviewed_model_comparison_groups",
        "reviewed_refinement_priority",
        "reviewed_future_refinement_chain",
        "reviewed_future_gates",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_review_sections(
    review_package: dict, field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid.pop(field)
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(
            invalid
        )


def test_validator_rejects_readiness_decision_ready(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_readiness_failure_basis"]["readiness_decision"] = (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"
    )
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_wrong_readiness_reason(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_readiness_failure_basis"]["readiness_reason"] = "WRONG"
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_stability_criterion_pass(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_readiness_failure_basis"]["stability_consistency_required"] = "PASS"
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_baseline_criterion_pass(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_readiness_failure_basis"][
        "baseline_outperformance_consistency_required"
    ] = "PASS"
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_target_universe_mismatch(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["target_universe"] = list(reversed(invalid["target_universe"]))
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_missing_review_package_digest(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid.pop("feature_label_refinement_plan_candidate_review_package_digest")
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_missing_per_ticker_candidate_digest(
    review_package: dict,
) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_refinement_plan_review_entries"][0].pop(
        "per_ticker_feature_label_refinement_plan_candidate_digest"
    )
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_validator_rejects_missing_per_ticker_review_digest(
    review_package: dict,
) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_refinement_plan_review_entries"][0].pop(
        "per_ticker_feature_label_refinement_plan_candidate_review_digest"
    )
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.validate_feature_label_refinement_plan_candidate_review_package_v1(invalid)


def test_builder_rejects_changed_source_candidate_digest() -> None:
    source = review.candidate_service.build_feature_label_refinement_plan_candidate_v1()
    source["feature_label_refinement_plan_candidate_digest"] = "0" * 64
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.build_feature_label_refinement_plan_candidate_review_package_v1(source)


def test_markdown_builder_includes_required_sections(review_package: dict) -> None:
    markdown = review.build_feature_label_refinement_plan_candidate_review_markdown_v1(
        review_package
    )
    for heading in (
        "# MarketFlow Feature/Label Refinement Plan Candidate Operator Review Status",
        "## Title",
        "## Feature/Label Refinement Plan Candidate Review Package",
        "## Reviewed Candidate",
        "## Source Improvement Candidate Review",
        "## Readiness Failure Basis",
        "## Reviewed Label Refinements",
        "## Reviewed Feature Refinements",
        "## Reviewed Protocol Refinements",
        "## Reviewed Model Comparison Groups",
        "## Refinement Priority",
        "## Per-Ticker Refinement Plan Review Entries",
        "## Future Refinement Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_emits_canonical_json_in_isolated_directory(tmp_path) -> None:
    result = review.write_feature_label_refinement_plan_candidate_review_package_v1(
        tmp_path
    )
    output = tmp_path / result["filename"]
    payload = output.read_bytes()
    written = json.loads(payload)
    assert payload == canonical_json_bytes(written)
    assert result["payload_byte_size"] == len(payload)
    assert result["payload_sha256"] == sha256_bytes(payload)
    assert result[
        "feature_label_refinement_plan_candidate_review_package_digest"
    ] == written["feature_label_refinement_plan_candidate_review_package_digest"]


def test_writer_refuses_overwrite(tmp_path) -> None:
    review.write_feature_label_refinement_plan_candidate_review_package_v1(tmp_path)
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.write_feature_label_refinement_plan_candidate_review_package_v1(tmp_path)


@pytest.mark.parametrize("filename", ["../review.json", "review.txt"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename: str) -> None:
    with pytest.raises(review.FeatureLabelRefinementPlanCandidateReviewError):
        review.write_feature_label_refinement_plan_candidate_review_package_v1(
            tmp_path, filename=filename
        )
