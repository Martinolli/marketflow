from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_review_service as review


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review.build_predictive_usefulness_reassessment_review_package_v1()


def test_review_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_predictive_usefulness_reassessment_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_accepts_exact_supplied_candidate_review() -> None:
    source = review.candidate_review_service.build_predictive_usefulness_reassessment_candidate_review_package_v1()
    package = review.build_predictive_usefulness_reassessment_review_package_v1(
        candidate_review_package=source
    )
    assert package["predictive_usefulness_reassessment_candidate_review_package_digest"] == (
        source["predictive_usefulness_reassessment_candidate_review_package_digest"]
    )


def test_artifact_kind_schema_and_status(review_package: dict) -> None:
    assert review_package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE
    )
    assert review_package["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_V1
    )
    assert review_package["review_status"] == (
        review.PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_READY
    )


def test_all_source_digests_are_bound(review_package: dict) -> None:
    expected = {
        "predictive_usefulness_reassessment_candidate_review_package_digest": review.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_reassessment_candidate_digest": review.EXPECTED_CANDIDATE_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": review.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
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


def test_registry_approved_dataset_metadata_is_preserved(review_package: dict) -> None:
    metadata = review_package["registry_approved_dataset_metadata"]
    assert metadata["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert metadata["dataset_scope"] == "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY"
    assert metadata["registry_entry_status"] == "APPROVED_FOR_RESEARCH_REGISTRY_ONLY"
    assert metadata["source_profile"] == "RTH_FULL_SESSION_1D"
    assert metadata["date_range_start"] == "2022-01-01"
    assert metadata["date_range_end"] == "2025-12-31"
    assert metadata["timeframe"] == "1d"
    assert metadata["target_universe_count"] == 12
    assert metadata["total_canonical_record_count"] == 11946
    assert metadata["records_digest"] == review.EXPECTED_RECORDS_DIGEST
    assert metadata["data_quality_status"] == "PASS_WITH_PRESERVED_SOURCE_LIMITATION"
    assert metadata["registry_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE


def test_evidence_summary_is_preserved(review_package: dict) -> None:
    assert review_package["evidence_summary"] == {
        "label_coverage_entries": 84,
        "label_available_values": 82854,
        "label_unavailable_values": 768,
        "feature_rows": 11946,
        "feature_fields": 22,
        "walk_forward_fold_count": 4,
        "oos_evaluation_rows": 2988,
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


def test_performance_interpretation_is_preserved(review_package: dict) -> None:
    performance = review_package["performance_interpretation"]
    assert performance["walk_forward_accuracy_range"] == "0.498698 to 0.562842"
    assert performance["walk_forward_accuracy_stability_status"] == (
        "MIXED_REQUIRES_OPERATOR_REVIEW"
    )
    assert performance["oos_majority_accuracy"] == "0.539491"
    assert performance["oos_previous_direction_accuracy"] == "0.495984"
    assert performance["oos_ticker_cross_sectional_accuracy"] == "0.502677"
    assert performance["oos_brier_score"] == "0.24875351"
    assert performance["performance_signal_status"] == (
        "REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE"
    )
    assert performance["baseline_outperformance_status"] == (
        "MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE"
    )


def test_conservative_reassessment_outputs(review_package: dict) -> None:
    assert review_package["reassessment_review_status"] == "COMPLETED_RESEARCH_ONLY"
    assert review_package["evidence_quality_for_acceptance_readiness"] == (
        "MIXED_REQUIRES_READINESS_REVIEW"
    )
    assert review_package["predictive_signal_consistency"] == "MIXED"
    assert review_package["baseline_outperformance_consistency"] == (
        "INSUFFICIENT_OR_MIXED"
    )
    assert review_package["leakage_control_assessment"] == "PASS"
    assert review_package["data_quality_assessment"] == (
        "PASS_WITH_PRESERVED_SOURCE_LIMITATION"
    )
    assert review_package["meta_limitation_assessment"] == (
        "PRESERVED_REQUIRES_OPERATOR_AWARENESS"
    )
    assert review_package["reassessment_supports_future_acceptance_readiness_review"] is True
    assert review_package["reassessment_supports_direct_predictive_usefulness_acceptance"] is False
    assert review_package["reassessment_recommends_predictive_usefulness_acceptance"] is False
    assert review_package["acceptance_decision_required_later"] is True


def test_per_ticker_entries_preserve_counts_and_bound_digests(review_package: dict) -> None:
    entries = review_package["per_ticker_reassessment_review_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == review.TARGET_UNIVERSE
    assert len({entry["per_ticker_predictive_usefulness_reassessment_review_digest"] for entry in entries}) == 12
    for entry in entries:
        assert entry["historical_record_count"] == (913 if entry["ticker"] == "META" else 1003)
        assert entry["meta_reduced_record_count_flag"] is (entry["ticker"] == "META")
        assert entry["source_predictive_usefulness_reassessment_candidate_review_digest"] == review.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        assert entry["source_predictive_usefulness_reassessment_candidate_digest"] == review.EXPECTED_CANDIDATE_DIGEST
        assert entry["per_ticker_predictive_usefulness_reassessment_review_digest"] == review.per_ticker_predictive_usefulness_reassessment_review_digest_v1(entry)
        assert entry["predictive_usefulness"] == review.NOT_ACCEPTED
        assert entry["runtime_use"] == review.NOT_AUTHORIZED


def test_review_domains_are_conservative_and_non_authorizing(review_package: dict) -> None:
    domains = review_package["review_domains"]
    assert {row["domain_id"]: row["review_result"] for row in domains} == review.REVIEW_DOMAIN_RESULTS
    assert all(row["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for row in domains)
    assert all(row["authority"] == "NOT_ACCEPTANCE" for row in domains)


def test_future_chain_gates_and_risk_controls_are_exact(review_package: dict) -> None:
    assert review_package["future_acceptance_chain"] == review.FUTURE_ACCEPTANCE_CHAIN
    assert review_package["future_gates"] == review.FUTURE_GATES
    assert review_package["risk_controls"] == review.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only(review_package: dict) -> None:
    outputs = review_package["planned_outputs"]
    assert [row["output_name"] for row in outputs] == review.PLANNED_OUTPUT_NAMES
    assert all(row["status"] == review.PLANNED_NOT_GENERATED for row in outputs)
    assert all(row["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)


def test_review_opens_only_acceptance_readiness_review_gate(review_package: dict) -> None:
    assert review_package["predictive_usefulness_reassessment_review_created"] is True
    assert review_package["predictive_usefulness_reassessment_review_ready"] is True
    assert review_package["ready_for_predictive_usefulness_acceptance_readiness_review"] is True
    assert review_package["ready_for_predictive_usefulness_acceptance"] is False


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
def test_closed_boundaries(review_package: dict, field: str, expected: object) -> None:
    assert review_package[field] == expected


def test_checklist_contains_every_required_check_and_all_pass(review_package: dict) -> None:
    checklist = review_package["review_checklist"]
    assert [row["check_id"] for row in checklist] == review.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == review.PASS for row in checklist)


def test_summary_counts_and_boundaries(review_package: dict) -> None:
    summary = review_package["review_summary"]
    assert summary == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review": True,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_review_and_per_ticker_digests_are_deterministic(review_package: dict) -> None:
    second = review.build_predictive_usefulness_reassessment_review_package_v1()
    assert second == review_package
    assert len(review_package["predictive_usefulness_reassessment_review_package_digest"]) == 64
    assert [row["per_ticker_predictive_usefulness_reassessment_review_digest"] for row in second["per_ticker_reassessment_review_entries"]] == [row["per_ticker_predictive_usefulness_reassessment_review_digest"] for row in review_package["per_ticker_reassessment_review_entries"]]


def test_validator_accepts_valid_review_package(review_package: dict) -> None:
    result = review.validate_predictive_usefulness_reassessment_review_package_v1(review_package)
    assert result["status"] == "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE_VALID"
    assert result["per_ticker_review_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_predictive_usefulness_acceptance_readiness_review"] is True
    assert result["ready_for_predictive_usefulness_acceptance"] is False


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("predictive_usefulness_reassessment_candidate_review_package_digest", "0" * 64),
        ("predictive_usefulness_reassessment_candidate_digest", "0" * 64),
        ("additional_predictive_evidence_results_review_package_digest", "0" * 64),
        ("additional_predictive_evidence_execution_digest", "0" * 64),
        ("additional_predictive_evidence_executed", False),
        ("additional_predictive_evidence_results_review_ready", False),
        ("predictive_usefulness_reassessment_candidate_created", False),
        ("predictive_usefulness_reassessment_candidate_review_created", False),
        ("predictive_usefulness_reassessment_review_created", False),
        ("predictive_usefulness_reassessment_review_ready", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("reassessment_supports_direct_predictive_usefulness_acceptance", True),
        ("reassessment_recommends_predictive_usefulness_acceptance", True),
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
    ],
)
def test_validator_rejects_changed_top_level_contract(
    review_package: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid[field] = bad_value
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(invalid)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("label_coverage_entries", 83),
        ("label_available_values", 82853),
        ("label_unavailable_values", 767),
        ("feature_rows", 11945),
        ("feature_fields", 21),
        ("walk_forward_fold_count", 3),
        ("oos_evaluation_rows", 2987),
        ("leakage_status", "FAIL"),
        ("failed_leakage_controls", 1),
    ],
)
def test_validator_rejects_changed_evidence(
    review_package: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid["evidence_summary"][field] = bad_value
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["review_domains", "future_acceptance_chain", "future_gates", "risk_controls"],
)
def test_validator_rejects_missing_review_structures(
    review_package: dict, field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid.pop(field)
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(invalid)


def test_validator_rejects_missing_or_changed_package_digest(review_package: dict) -> None:
    missing = deepcopy(review_package)
    missing.pop("predictive_usefulness_reassessment_review_package_digest")
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(missing)
    changed = deepcopy(review_package)
    changed["predictive_usefulness_reassessment_review_package_digest"] = "0" * 64
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(changed)


def test_validator_rejects_missing_or_changed_per_ticker_digest(review_package: dict) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(review_package)
        entry = invalid["per_ticker_reassessment_review_entries"][0]
        if replacement is None:
            entry.pop("per_ticker_predictive_usefulness_reassessment_review_digest")
        else:
            entry["per_ticker_predictive_usefulness_reassessment_review_digest"] = replacement
        with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
            review.validate_predictive_usefulness_reassessment_review_package_v1(invalid)


def test_validator_rejects_missing_check_or_fabricated_summary(review_package: dict) -> None:
    missing_check = deepcopy(review_package)
    missing_check["review_checklist"].pop()
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(missing_check)
    fabricated_summary = deepcopy(review_package)
    fabricated_summary["review_summary"]["passed_checks"] = 0
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.validate_predictive_usefulness_reassessment_review_package_v1(fabricated_summary)


def test_markdown_contains_all_required_sections(review_package: dict) -> None:
    markdown = review.build_predictive_usefulness_reassessment_review_markdown_v1(review_package)
    for heading in (
        "Title",
        "Predictive Usefulness Reassessment Review Package",
        "Source Candidate Review",
        "Source Additional Predictive Evidence Results Review",
        "Registry-Approved Dataset Metadata",
        "Target Universe",
        "Evidence Summary",
        "Performance Interpretation",
        "Per-Ticker Reassessment Review Entries",
        "Review Domains",
        "Future Acceptance Chain",
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
    result = review.write_predictive_usefulness_reassessment_review_package_v1(tmp_path)
    path = Path(result["path"])
    package = json.loads(path.read_text(encoding="utf-8"))
    payload = canonical_json_bytes(package)
    assert path.read_bytes() == payload
    assert result["payload_sha256"] == sha256_bytes(payload)
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.write_predictive_usefulness_reassessment_review_package_v1(tmp_path)


@pytest.mark.parametrize("filename", ["nested/review.json", "review.txt", "../review.json"])
def test_writer_rejects_unsafe_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(review.PredictiveUsefulnessReassessmentReviewError):
        review.write_predictive_usefulness_reassessment_review_package_v1(
            tmp_path, filename=filename
        )
