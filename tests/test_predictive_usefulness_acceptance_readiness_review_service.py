from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_usefulness_acceptance_readiness_review_service as review


@pytest.fixture(scope="module")
def readiness_review() -> dict:
    return review.build_predictive_usefulness_acceptance_readiness_review_v1()


def test_readiness_review_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_predictive_usefulness_acceptance_readiness_review_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_accepts_exact_supplied_reassessment_review() -> None:
    source = review.reassessment_service.build_predictive_usefulness_reassessment_review_package_v1()
    package = review.build_predictive_usefulness_acceptance_readiness_review_v1(
        reassessment_review_package=source
    )
    assert package["predictive_usefulness_reassessment_review_package_digest"] == (
        source["predictive_usefulness_reassessment_review_package_digest"]
    )


def test_artifact_schema_status_and_decision(readiness_review: dict) -> None:
    assert readiness_review["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW
    )
    assert readiness_review["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_V1
    )
    assert readiness_review["review_status"] == (
        review.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_COMPLETED
    )
    assert readiness_review["readiness_decision"] == (
        review.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY
    )


def test_all_source_digests_are_bound(readiness_review: dict) -> None:
    expected = {
        "predictive_usefulness_reassessment_review_package_digest": review.EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_reassessment_candidate_review_package_digest": review.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_reassessment_candidate_digest": review.EXPECTED_CANDIDATE_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": review.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_execution_digest": review.EXPECTED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_digest": review.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "research_registry_approval_digest": review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": review.EXPECTED_RECORDS_DIGEST,
    }
    assert {key: readiness_review[key] for key in expected} == expected


def test_target_universe_is_exact_and_ordered(readiness_review: dict) -> None:
    assert readiness_review["target_universe_count"] == 12
    assert readiness_review["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_registry_dataset_metadata_is_preserved(readiness_review: dict) -> None:
    metadata = readiness_review["registry_approved_dataset_metadata"]
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


def test_readiness_input_facts_are_preserved(readiness_review: dict) -> None:
    facts = readiness_review["readiness_review_input_facts"]
    expected = {
        "label_coverage_entries": 84,
        "label_available_values": 82854,
        "label_unavailable_values": 768,
        "feature_rows": 11946,
        "feature_fields": 22,
        "walk_forward_fold_count": 4,
        "oos_evaluation_rows": 2988,
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "walk_forward_accuracy_stability_status": "MIXED_REQUIRES_OPERATOR_REVIEW",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "reassessment_review_status": "COMPLETED_RESEARCH_ONLY",
        "evidence_quality_for_acceptance_readiness": "MIXED_REQUIRES_READINESS_REVIEW",
        "predictive_signal_consistency": "MIXED",
        "baseline_outperformance_consistency": "INSUFFICIENT_OR_MIXED",
        "leakage_control_assessment": "PASS",
        "data_quality_assessment": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
    }
    for field, value in expected.items():
        assert facts[field] == value


def test_readiness_criteria_and_findings_are_exact(readiness_review: dict) -> None:
    assert readiness_review["readiness_criteria"] == review.READINESS_CRITERIA
    assert {
        row["criterion_id"]: row["result"]
        for row in readiness_review["readiness_findings"]
    } == review.READINESS_FINDING_RESULTS


def test_readiness_interpretation_is_conservative(readiness_review: dict) -> None:
    assert readiness_review["readiness_reason"] == (
        "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
    )
    assert readiness_review["acceptance_candidate_allowed"] is False
    assert readiness_review["acceptance_ceremony_allowed"] is False
    assert readiness_review["additional_evidence_or_model_improvement_required"] is True
    assert readiness_review[
        "ready_for_predictive_usefulness_improvement_or_additional_evidence_planning"
    ] is True


def test_per_ticker_entries_preserve_counts_and_digests(readiness_review: dict) -> None:
    entries = readiness_review["per_ticker_readiness_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review.TARGET_UNIVERSE
    assert len({row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] for row in entries}) == 12
    for row in entries:
        assert row["historical_record_count"] == (913 if row["ticker"] == "META" else 1003)
        assert row["meta_reduced_record_count_flag"] is (row["ticker"] == "META")
        assert row["predictive_usefulness_acceptance_readiness_status"] == "NOT_READY"
        assert row["source_predictive_usefulness_reassessment_review_package_digest"] == review.EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST
        assert row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] == review.per_ticker_predictive_usefulness_acceptance_readiness_digest_v1(row)
        assert row["predictive_usefulness"] == review.NOT_ACCEPTED
        assert row["runtime_use"] == review.NOT_AUTHORIZED


def test_future_chain_gates_and_controls_are_exact(readiness_review: dict) -> None:
    assert readiness_review["future_improvement_chain"] == review.FUTURE_IMPROVEMENT_CHAIN
    assert readiness_review["future_gates"] == review.FUTURE_GATES
    assert readiness_review["risk_controls"] == review.RISK_CONTROLS


def test_planned_outputs_remain_not_generated(readiness_review: dict) -> None:
    outputs = readiness_review["planned_outputs"]
    assert [row["output_name"] for row in outputs] == review.PLANNED_OUTPUT_NAMES
    assert all(row["status"] == review.PLANNED_NOT_GENERATED for row in outputs)
    assert all(row["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)


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
        ("predictive_usefulness_acceptance_ceremony_ready", False),
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
def test_closed_boundaries(readiness_review: dict, field: str, expected: object) -> None:
    assert readiness_review[field] == expected


def test_checklist_is_complete_and_all_checks_pass(readiness_review: dict) -> None:
    checklist = readiness_review["review_checklist"]
    assert [row["check_id"] for row in checklist] == review.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == review.PASS for row in checklist)


def test_summary_counts_and_boundaries(readiness_review: dict) -> None:
    assert readiness_review["review_summary"] == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "acceptance_readiness_review_completed": True,
        "readiness_decision": review.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "ready_for_improvement_or_additional_evidence_planning": True,
    }


def test_readiness_and_per_ticker_digests_are_deterministic(
    readiness_review: dict,
) -> None:
    second = review.build_predictive_usefulness_acceptance_readiness_review_v1()
    assert second == readiness_review
    assert len(readiness_review["predictive_usefulness_acceptance_readiness_review_digest"]) == 64
    assert [row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] for row in second["per_ticker_readiness_entries"]] == [row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] for row in readiness_review["per_ticker_readiness_entries"]]


def test_validator_accepts_valid_readiness_review(readiness_review: dict) -> None:
    result = review.validate_predictive_usefulness_acceptance_readiness_review_v1(
        readiness_review
    )
    assert result["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_VALID"
    assert result["readiness_decision"] == review.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY
    assert result["per_ticker_readiness_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_improvement_or_additional_evidence_planning"] is True


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("predictive_usefulness_reassessment_review_package_digest", "0" * 64),
        ("predictive_usefulness_reassessment_candidate_review_package_digest", "0" * 64),
        ("additional_predictive_evidence_results_review_package_digest", "0" * 64),
        ("additional_predictive_evidence_execution_digest", "0" * 64),
        ("additional_predictive_evidence_executed", False),
        ("additional_predictive_evidence_results_review_ready", False),
        ("predictive_usefulness_reassessment_review_created", False),
        ("predictive_usefulness_reassessment_review_ready", False),
        ("predictive_usefulness_acceptance_readiness_review_created", False),
        ("predictive_usefulness_acceptance_readiness_review_completed", False),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("acceptance_candidate_allowed", True),
        ("acceptance_ceremony_allowed", True),
        ("additional_evidence_or_model_improvement_required", False),
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
    readiness_review: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(readiness_review)
    invalid[field] = bad_value
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


@pytest.mark.parametrize(
    "criterion,bad_result",
    [
        ("leakage_controls_pass_required", "FAIL"),
        ("no_failed_controls_required", "FAIL"),
        ("minimum_evidence_review_completion_required", "FAIL"),
        ("stability_consistency_required", review.PASS),
        ("baseline_outperformance_consistency_required", review.PASS),
    ],
)
def test_validator_rejects_changed_readiness_findings(
    readiness_review: dict, criterion: str, bad_result: str
) -> None:
    invalid = deepcopy(readiness_review)
    next(row for row in invalid["readiness_findings"] if row["criterion_id"] == criterion)[
        "result"
    ] = bad_result
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


@pytest.mark.parametrize(
    "field,bad_value",
    [("leakage_status", "FAIL"), ("failed_leakage_controls", 1)],
)
def test_validator_rejects_changed_leakage_facts(
    readiness_review: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(readiness_review)
    invalid["readiness_review_input_facts"][field] = bad_value
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["future_improvement_chain", "future_gates", "risk_controls"],
)
def test_validator_rejects_missing_future_structure(
    readiness_review: dict, field: str
) -> None:
    invalid = deepcopy(readiness_review)
    invalid.pop(field)
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


def test_validator_rejects_missing_or_changed_readiness_digest(
    readiness_review: dict,
) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(readiness_review)
        if replacement is None:
            invalid.pop("predictive_usefulness_acceptance_readiness_review_digest")
        else:
            invalid["predictive_usefulness_acceptance_readiness_review_digest"] = replacement
        with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
            review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


def test_validator_rejects_missing_or_changed_per_ticker_digest(
    readiness_review: dict,
) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(readiness_review)
        entry = invalid["per_ticker_readiness_entries"][0]
        if replacement is None:
            entry.pop("per_ticker_predictive_usefulness_acceptance_readiness_digest")
        else:
            entry["per_ticker_predictive_usefulness_acceptance_readiness_digest"] = replacement
        with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
            review.validate_predictive_usefulness_acceptance_readiness_review_v1(invalid)


def test_validator_rejects_missing_check_or_fabricated_summary(
    readiness_review: dict,
) -> None:
    missing_check = deepcopy(readiness_review)
    missing_check["review_checklist"].pop()
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(missing_check)
    fabricated = deepcopy(readiness_review)
    fabricated["review_summary"]["passed_checks"] = 0
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.validate_predictive_usefulness_acceptance_readiness_review_v1(fabricated)


def test_markdown_contains_required_sections(readiness_review: dict) -> None:
    markdown = review.build_predictive_usefulness_acceptance_readiness_review_markdown_v1(
        readiness_review
    )
    for heading in (
        "Title",
        "Predictive Usefulness Acceptance Readiness Review",
        "Source Reassessment Review",
        "Registry-Approved Dataset Metadata",
        "Target Universe",
        "Readiness Criteria",
        "Readiness Findings",
        "Readiness Decision",
        "Per-Ticker Readiness Entries",
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
    result = review.write_predictive_usefulness_acceptance_readiness_review_v1(tmp_path)
    path = Path(result["path"])
    package = json.loads(path.read_text(encoding="utf-8"))
    payload = canonical_json_bytes(package)
    assert path.read_bytes() == payload
    assert result["payload_sha256"] == sha256_bytes(payload)
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.write_predictive_usefulness_acceptance_readiness_review_v1(tmp_path)


@pytest.mark.parametrize("filename", ["nested/review.json", "review.txt", "../review.json"])
def test_writer_rejects_unsafe_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewError):
        review.write_predictive_usefulness_acceptance_readiness_review_v1(
            tmp_path, filename=filename
        )
