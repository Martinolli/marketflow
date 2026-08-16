from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    predictive_usefulness_reassessment_review_rerun_using_refined_evidence_service as review,
)


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1()


def test_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_and_status_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE
    )
    assert package["review_status"] == (
        review.PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_RERUN_USING_REFINED_EVIDENCE_PACKAGE_READY
    )


def test_source_digest_chain_is_bound(package: dict) -> None:
    assert package[
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    ] == review.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST
    assert package[
        "additional_predictive_evidence_execution_for_refined_evidence_digest"
    ] == review.EXPECTED_REFINED_EXECUTION_DIGEST
    assert package[
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
    ] == review.EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST
    assert package["feature_label_refinement_results_review_package_digest"] == (
        review.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST
    )
    assert package["research_registry_approval_digest"] == (
        review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
    )
    assert package["records_digest"] == review.EXPECTED_RECORDS_DIGEST


def test_registry_universe_and_record_counts_are_exact(package: dict) -> None:
    assert package["registry_approved_dataset_metadata"] == (
        review.REGISTRY_APPROVED_DATASET_METADATA
    )
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["meta_record_count"] == 913
    assert package["non_meta_record_count"] == 1003
    assert package["per_ticker_record_counts"] == review.EXPECTED_RECORD_COUNTS


def test_source_results_and_reassessment_states_are_exact(package: dict) -> None:
    assert package[
        "additional_predictive_evidence_execution_for_refined_evidence_executed"
    ] is True
    assert package[
        "additional_predictive_evidence_results_for_refined_evidence_created"
    ] is True
    assert package[
        "additional_predictive_evidence_results_review_for_refined_evidence_created"
    ] is True
    assert package[
        "additional_predictive_evidence_results_review_for_refined_evidence_ready"
    ] is True
    assert package[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created"
    ] is True
    assert package[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready"
    ] is True
    assert package[
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence"
    ] is True
    assert package[
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created"
    ] is False


def test_refined_evidence_facts_are_bound(package: dict) -> None:
    assert package["generated_output_count"] == 10
    assert package["failure_count"] == 0
    assert package["warning_count"] == 1
    assert package["refined_label_family_count"] == 7
    assert package["refined_label_available_values"] == 82698
    assert package["refined_label_unavailable_values"] == 924
    assert package["refined_feature_group_count"] == 9
    assert package["refined_feature_category_count"] == 11
    assert package["refined_feature_field_count"] == 19
    assert package["refined_feature_rows"] == 11946
    assert package["refined_protocol_group_count"] == 6
    assert package["chronological_splits"] is True
    assert package["one_session_embargo"] is True
    assert package["no_shuffle"] is True
    assert package["no_lookahead"] is True


def test_reassessment_metrics_are_bound(package: dict) -> None:
    assert package["refined_walk_forward_fold_count"] == 4
    assert package["refined_walk_forward_evaluation_rows"] == 3024
    assert package["refined_oos_evaluation_rows"] == 2988
    assert package["refined_oos_accuracy_range"] == "0.119813 to 0.480924"
    assert package["model_comparison_group_count"] == 5
    assert package["deterministic_comparisons_evaluated"] == 7
    assert package["unavailable_model_family_requests"] == 3
    assert package["unavailable_model_family_status"] == (
        "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    )
    assert package["refined_leakage_status"] == "PASS"
    assert package["failed_leakage_controls"] == 0
    assert package["data_quality_status"] == "PASS_WITH_PRESERVED_SOURCE_LIMITATION"


def test_reassessment_classification_is_conservative(package: dict) -> None:
    assert package["reassessment_review_status"] == "COMPLETED_RESEARCH_ONLY"
    assert package["refined_evidence_predictive_signal_consistency"] == "WEAK_OR_MIXED"
    assert package["refined_baseline_outperformance_consistency"] == (
        "INSUFFICIENT_OR_MIXED"
    )
    assert package["refined_oos_performance_assessment"] == (
        "LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE"
    )
    assert package["model_comparison_assessment"] == (
        "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE"
    )
    assert package["calibration_stability_assessment"] == (
        "NOT_ACCEPTANCE_EVIDENCE_UNTIL_READINESS_REVIEW"
    )
    assert package[
        "reassessment_supports_future_acceptance_readiness_review_rerun_using_refined_evidence"
    ] is True
    assert package[
        "reassessment_supports_direct_predictive_usefulness_acceptance"
    ] is False
    assert package["reassessment_recommends_predictive_usefulness_acceptance"] is False


def test_review_domains_are_complete_and_non_authorizing(package: dict) -> None:
    domains = package["review_domains"]
    assert {item["domain_id"]: item["review_result"] for item in domains} == (
        review.REVIEW_DOMAIN_RESULTS
    )
    assert all(item["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for item in domains)
    assert all(item["authority"] == review.NOT_ACCEPTANCE for item in domains)


def test_per_ticker_entries_are_complete_and_digest_bound(package: dict) -> None:
    entries = package["per_ticker_reassessment_rerun_entries"]
    assert [entry["ticker"] for entry in entries] == review.TARGET_UNIVERSE
    assert len(entries) == 12
    for entry in entries:
        ticker = entry["ticker"]
        assert entry["historical_record_count"] == review.EXPECTED_RECORD_COUNTS[ticker]
        assert entry["meta_reduced_record_count_flag"] is (ticker == "META")
        assert entry["predictive_usefulness"] == review.NOT_ACCEPTED
        assert entry["runtime_use"] == review.NOT_AUTHORIZED
        assert entry[
            "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
        ] == review.per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest_v1(
            entry
        )
    meta = entries[4]
    assert meta["ticker"] == "META"
    assert meta["historical_record_count"] == 913
    assert meta["refinement_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_REASSESSMENT_RERUN"
    )


def test_future_chain_gates_controls_and_planned_outputs(package: dict) -> None:
    assert package["future_chain"] == review.FUTURE_CHAIN
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert [item["output_name"] for item in package["planned_outputs"]] == (
        review.PLANNED_OUTPUT_NAMES
    )
    assert all(
        item["status"] == review.PLANNED_NOT_GENERATED
        for item in package["planned_outputs"]
    )
    assert all(
        item["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE
        for item in package["planned_outputs"]
    )


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_reassessment_rerun_performed",
        "refined_out_of_sample_reassessment_rerun_performed",
        "refined_metrics_recomputation_performed",
        "refined_model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_for_refined_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_prohibited_work_remains_false(package: dict, field: str) -> None:
    assert package[field] is False


@pytest.mark.parametrize(
    "field, expected",
    [
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
        ("predictive_usefulness_acceptance_artifact_created", False),
        ("profitability_acceptance_created", False),
        ("runtime_migration_approval_created", False),
    ],
)
def test_acceptance_profitability_and_runtime_remain_closed(
    package: dict, field: str, expected: object
) -> None:
    assert package[field] == expected


def test_checklist_and_summary_are_complete(package: dict) -> None:
    assert [row["check_id"] for row in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary[
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence"
    ] is True


def test_package_and_per_ticker_digests_are_deterministic(package: dict) -> None:
    repeated = review.build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1()
    assert repeated == package
    assert package[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
    ] == review.predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest_v1(
        package
    )
    assert [
        item[
            "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
        ]
        for item in repeated["per_ticker_reassessment_rerun_entries"]
    ] == [
        item[
            "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
        ]
        for item in package["per_ticker_reassessment_rerun_entries"]
    ]


def test_validator_accepts_valid_package(package: dict) -> None:
    validation = review.validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
        package
    )
    assert validation["blocker_count"] == 0
    assert validation["per_ticker_reassessment_entry_count"] == 12
    assert validation[
        "ready_for_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence"
    ] is True


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("additional_predictive_evidence_results_review_for_refined_evidence_package_digest", "0" * 64),
        ("additional_predictive_evidence_execution_for_refined_evidence_digest", "0" * 64),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("per_ticker_record_counts", review.EXPECTED_RECORD_COUNTS | {"META": 914}),
        ("refined_label_family_count", 6),
        ("refined_feature_group_count", 8),
        ("refined_feature_field_count", 18),
        ("refined_protocol_group_count", 5),
        ("model_comparison_group_count", 4),
        ("refined_walk_forward_fold_count", 3),
        ("refined_oos_evaluation_rows", 2987),
        ("refined_leakage_status", "FAIL"),
        ("failed_leakage_controls", 1),
        ("reassessment_supports_direct_predictive_usefulness_acceptance", True),
        ("reassessment_recommends_predictive_usefulness_acceptance", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("feature_label_refinement_execution_rerun_performed", True),
        ("refined_label_generation_rerun_performed", True),
        ("refined_feature_generation_rerun_performed", True),
        ("refined_metrics_recomputation_performed", True),
        ("refined_model_comparison_rerun_performed", True),
        ("additional_predictive_evidence_execution_for_refined_evidence_rerun_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("review_domains", []),
        ("future_chain", []),
        ("future_gates", []),
        ("risk_controls", []),
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest", None),
    ],
)
def test_validator_rejects_invalid_or_authorizing_mutations(
    package: dict, field: str, invalid_value: object
) -> None:
    invalid = deepcopy(package)
    invalid[field] = invalid_value
    with pytest.raises(
        review.PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError
    ):
        review.validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["per_ticker_reassessment_rerun_entries"][0].pop(
        "per_ticker_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest"
    )
    with pytest.raises(
        review.PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError
    ):
        review.validate_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
            invalid
        )


def test_markdown_contains_required_sections(package: dict) -> None:
    markdown = review.build_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_markdown_v1(
        package
    )
    for section in (
        "# MarketFlow Predictive Usefulness Reassessment Review Rerun Using Refined Evidence",
        "## Source Refined-Evidence Results Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Refined Evidence Facts",
        "## Reassessment Classification",
        "## Review Domains",
        "## Per-Ticker Reassessment Entries",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_writer_isolated_and_no_overwrite(package: dict, tmp_path: Path) -> None:
    result = review.write_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
        tmp_path
    )
    assert Path(result["path"]).is_file()
    assert result[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
    ] == package[
        "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest"
    ]
    with pytest.raises(
        review.PredictiveUsefulnessReassessmentReviewRerunUsingRefinedEvidenceError
    ):
        review.write_predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_v1(
            tmp_path
        )
