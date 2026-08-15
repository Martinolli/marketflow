from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import feature_label_refinement_plan_candidate_service as plan


@pytest.fixture(scope="module")
def candidate() -> dict:
    return plan.build_feature_label_refinement_plan_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = plan.build_feature_label_refinement_plan_candidate_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False


def test_candidate_accepts_exact_supplied_review_package() -> None:
    source = (
        plan.review_service.build_predictive_evidence_improvement_candidate_review_package_v1()
    )
    built = plan.build_feature_label_refinement_plan_candidate_v1(source)
    assert built["predictive_evidence_improvement_candidate_review_package_digest"] == (
        source["predictive_evidence_improvement_candidate_review_package_digest"]
    )


def test_artifact_schema_and_candidate_status(candidate: dict) -> None:
    assert candidate["artifact_kind"] == (
        plan.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE
    )
    assert candidate["schema_version"] == (
        plan.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_V1
    )
    assert candidate["candidate_status"] == (
        plan.FEATURE_LABEL_REFINEMENT_PLAN_READY_FOR_OPERATOR_REVIEW
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("predictive_evidence_improvement_candidate_review_package_digest", plan.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", plan.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", plan.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", plan.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", plan.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", plan.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", plan.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", plan.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", plan.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_digests_are_bound(
    candidate: dict, field: str, expected: str
) -> None:
    assert candidate[field] == expected


def test_target_universe_is_exact_and_ordered(candidate: dict) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_readiness_failure_basis_is_preserved(candidate: dict) -> None:
    assert candidate["readiness_decision"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
    )
    assert candidate["readiness_reason"] == (
        "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
    )
    assert candidate["readiness_failure_summary"] == {
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
    }


def test_readiness_evidence_basis_is_preserved(candidate: dict) -> None:
    assert candidate["evidence_basis"] == {
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


def test_plan_objective_scope_mode_and_authority(candidate: dict) -> None:
    assert candidate["feature_label_refinement_plan_objective"] == plan.PLAN_OBJECTIVE
    assert candidate["feature_label_refinement_plan_scope"] == plan.PLAN_SCOPE
    assert candidate["feature_label_refinement_plan_mode"] == plan.PLANNED_NOT_EXECUTED
    assert candidate["feature_label_refinement_authority_status"] == plan.NOT_AUTHORIZED
    assert candidate["feature_label_refinement_plan_candidate_created"] is True
    assert candidate["feature_label_refinement_plan_ready_for_operator_review"] is True


@pytest.mark.parametrize(
    "field,expected_ids",
    [
        ("planned_label_refinement_groups", plan.LABEL_REFINEMENT_GROUP_IDS),
        ("planned_feature_refinement_groups", plan.FEATURE_REFINEMENT_GROUP_IDS),
        ("planned_protocol_refinement_groups", plan.PROTOCOL_REFINEMENT_GROUP_IDS),
        ("planned_model_comparison_groups", plan.MODEL_COMPARISON_GROUP_IDS),
    ],
)
def test_planned_refinement_groups_are_complete_and_non_authorizing(
    candidate: dict, field: str, expected_ids: list[str]
) -> None:
    groups = candidate[field]
    assert [row["group_id"] for row in groups] == expected_ids
    assert all(row["planning_status"] == plan.PLANNED_NOT_EXECUTED for row in groups)
    assert all(row["authorization_status"] == plan.NOT_AUTHORIZED for row in groups)
    assert all(row["execution_status"] == plan.NOT_EXECUTED for row in groups)
    assert all(row["research_only"] is True for row in groups)
    assert all(row["non_actionable"] is True for row in groups)


def test_refinement_priority_is_defined_without_approval(candidate: dict) -> None:
    assert candidate["refinement_priority"] == plan.REFINEMENT_PRIORITY
    assert candidate["feature_label_refinement_plan_approved"] is False
    assert candidate["feature_label_refinement_authorized"] is False


def test_per_ticker_refinement_entries_preserve_counts_and_boundaries(
    candidate: dict,
) -> None:
    entries = candidate["per_ticker_refinement_plan_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == plan.TARGET_UNIVERSE
    assert len(
        {
            row["per_ticker_feature_label_refinement_plan_candidate_digest"]
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
        assert row["refinement_authorized"] is False
        assert row["refinement_executed"] is False
        assert row["predictive_usefulness"] == plan.NOT_ACCEPTED
        assert row["profitability"] == plan.NOT_ACCEPTED
        assert row["runtime_use"] == plan.NOT_AUTHORIZED
        assert row["strategy_use"] == plan.NOT_AUTHORIZED
        assert row["paper_trading"] == plan.NOT_AUTHORIZED
        assert row["broker_execution"] == plan.NOT_AUTHORIZED
        assert row[
            "per_ticker_feature_label_refinement_plan_candidate_digest"
        ] == plan.per_ticker_feature_label_refinement_plan_candidate_digest_v1(row)


def test_meta_limitation_note_is_exact_and_not_inferred_for_other_tickers(
    candidate: dict,
) -> None:
    entries = candidate["per_ticker_refinement_plan_entries"]
    meta = next(row for row in entries if row["ticker"] == "META")
    others = [row for row in entries if row["ticker"] != "META"]
    assert meta["refinement_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
    )
    assert all("refinement_note" not in row for row in others)


def test_future_refinement_chain_is_defined(candidate: dict) -> None:
    assert candidate["future_refinement_chain"] == plan.FUTURE_REFINEMENT_CHAIN


def test_future_gates_are_defined(candidate: dict) -> None:
    assert candidate["future_gates"] == plan.FUTURE_GATES


def test_risk_controls_are_defined(candidate: dict) -> None:
    assert candidate["risk_controls"] == plan.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_are_research_only(candidate: dict) -> None:
    assert [row["output_name"] for row in candidate["planned_outputs"]] == (
        plan.PLANNED_OUTPUT_NAMES
    )
    assert candidate["planned_outputs_status"] == plan.PLANNED_NOT_GENERATED
    assert candidate["planned_outputs_label"] == plan.RESEARCH_ONLY_NON_ACTIONABLE
    assert all(row["status"] == plan.PLANNED_NOT_GENERATED for row in candidate["planned_outputs"])
    assert all(row["label"] == plan.RESEARCH_ONLY_NON_ACTIONABLE for row in candidate["planned_outputs"])


@pytest.mark.parametrize(
    "field,expected",
    [
        ("provider_requests_made", False),
        ("live_provider_transport_enabled", False),
        ("market_data_acquisition_performed", False),
        ("dataset_generation_performed", False),
        ("canonical_dataset_regenerated", False),
        ("predictive_execution_rerun_performed", False),
        ("label_generation_rerun_performed", False),
        ("feature_matrix_rerun_performed", False),
        ("walk_forward_validation_rerun_performed", False),
        ("out_of_sample_evaluation_rerun_performed", False),
        ("metrics_recomputation_performed", False),
        ("improvement_execution_performed", False),
        ("refinement_option_execution_performed", False),
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
        ("predictive_usefulness", plan.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", plan.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("profitability_acceptance_recommended", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", plan.NOT_AUTHORIZED),
        ("strategy_use", plan.NOT_AUTHORIZED),
        ("paper_trading", plan.NOT_AUTHORIZED),
        ("broker_execution", plan.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_all_execution_acceptance_and_runtime_boundaries_remain_closed(
    candidate: dict, field: str, expected: object
) -> None:
    assert candidate[field] == expected


def test_checklist_contains_all_required_check_ids(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == (
        plan.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_and_summary_counts_match(candidate: dict) -> None:
    checklist = candidate["candidate_checklist"]
    summary = candidate["candidate_summary"]
    assert all(row["status"] == plan.PASS for row in checklist)
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert summary["total_checks"] == len(plan.REQUIRED_CHECK_IDS) == 72
    assert summary["passed_checks"] == 72
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_feature_label_refinement_plan_approval"] is False
    assert summary["ready_for_feature_label_refinement_execution_candidate"] is False
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    rebuilt = plan.build_feature_label_refinement_plan_candidate_v1()
    assert rebuilt["feature_label_refinement_plan_candidate_digest"] == candidate[
        "feature_label_refinement_plan_candidate_digest"
    ]
    assert candidate["feature_label_refinement_plan_candidate_digest"] == (
        plan.feature_label_refinement_plan_candidate_digest_v1(candidate)
    )


def test_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    rebuilt = plan.build_feature_label_refinement_plan_candidate_v1()
    assert [
        row["per_ticker_feature_label_refinement_plan_candidate_digest"]
        for row in rebuilt["per_ticker_refinement_plan_entries"]
    ] == [
        row["per_ticker_feature_label_refinement_plan_candidate_digest"]
        for row in candidate["per_ticker_refinement_plan_entries"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = plan.validate_feature_label_refinement_plan_candidate_v1(candidate)
    assert result["status"] == "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_VALID"
    assert result["blocker_count"] == 0
    assert result["feature_label_refinement_authorized"] is False
    assert result["predictive_usefulness"] == plan.NOT_ACCEPTED
    assert result["profitability"] == plan.NOT_ACCEPTED


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("predictive_evidence_improvement_candidate_review_package_digest", "0" * 64),
        ("predictive_usefulness_acceptance_readiness_review_digest", "0" * 64),
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "WRONG"),
        ("feature_label_refinement_plan_candidate_created", False),
        ("feature_label_refinement_authority_status", "AUTHORIZED"),
        ("refined_label_generation_authorized", True),
        ("refined_label_generation_performed", True),
        ("refined_feature_generation_authorized", True),
        ("refined_feature_generation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
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
        ("model_comparison_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_forbidden_top_level_mutations(
    candidate: dict, field: str, value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = value
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "planned_label_refinement_groups",
        "planned_feature_refinement_groups",
        "planned_protocol_refinement_groups",
        "planned_model_comparison_groups",
        "refinement_priority",
        "future_refinement_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_planning_sections(candidate: dict, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_validator_rejects_stability_criterion_pass(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["readiness_failure_summary"]["stability_consistency_required"] = "PASS"
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_validator_rejects_baseline_criterion_pass(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["readiness_failure_summary"][
        "baseline_outperformance_consistency_required"
    ] = "PASS"
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_validator_rejects_target_universe_mismatch(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["target_universe"] = list(reversed(invalid["target_universe"]))
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid.pop("feature_label_refinement_plan_candidate_digest")
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["per_ticker_refinement_plan_entries"][0].pop(
        "per_ticker_feature_label_refinement_plan_candidate_digest"
    )
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.validate_feature_label_refinement_plan_candidate_v1(invalid)


def test_builder_rejects_changed_source_review_digest() -> None:
    source = (
        plan.review_service.build_predictive_evidence_improvement_candidate_review_package_v1()
    )
    source["predictive_evidence_improvement_candidate_review_package_digest"] = "0" * 64
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.build_feature_label_refinement_plan_candidate_v1(source)


def test_markdown_builder_includes_required_sections(candidate: dict) -> None:
    markdown = plan.build_feature_label_refinement_plan_candidate_markdown_v1(candidate)
    for heading in (
        "# MarketFlow Feature/Label Refinement Plan Candidate Status",
        "## Title",
        "## Feature/Label Refinement Plan Candidate",
        "## Source Improvement Candidate Review",
        "## Readiness Failure Basis",
        "## Planned Label Refinements",
        "## Planned Feature Refinements",
        "## Planned Protocol Refinements",
        "## Planned Model Comparison Groups",
        "## Refinement Priority",
        "## Per-Ticker Refinement Plan Entries",
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


def test_writer_emits_canonical_json_in_isolated_directory(
    tmp_path,
) -> None:
    result = plan.write_feature_label_refinement_plan_candidate_v1(tmp_path)
    output = tmp_path / result["filename"]
    payload = output.read_bytes()
    written = json.loads(payload)
    assert payload == canonical_json_bytes(written)
    assert result["payload_byte_size"] == len(payload)
    assert result["payload_sha256"] == sha256_bytes(payload)
    assert result["feature_label_refinement_plan_candidate_digest"] == written[
        "feature_label_refinement_plan_candidate_digest"
    ]


def test_writer_refuses_overwrite(tmp_path) -> None:
    plan.write_feature_label_refinement_plan_candidate_v1(tmp_path)
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.write_feature_label_refinement_plan_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["../candidate.json", "candidate.txt"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename: str) -> None:
    with pytest.raises(plan.FeatureLabelRefinementPlanCandidateError):
        plan.write_feature_label_refinement_plan_candidate_v1(
            tmp_path, filename=filename
        )
