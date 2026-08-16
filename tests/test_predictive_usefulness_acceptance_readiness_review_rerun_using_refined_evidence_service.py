from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_service as review,
)


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1()


def test_review_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = review.build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_review"] is False


def test_artifact_status_decision_and_reason_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE
    assert package["review_status"] == review.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_COMPLETED
    assert package["readiness_decision"] == review.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE
    assert package["readiness_reason"] == review.READINESS_REASON_REFINED_EVIDENCE_WEAK_OR_MIXED_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest", review.EXPECTED_REASSESSMENT_RERUN_DIGEST),
        ("additional_predictive_evidence_results_review_for_refined_evidence_package_digest", review.EXPECTED_REFINED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_for_refined_evidence_digest", review.EXPECTED_REFINED_EXECUTION_DIGEST),
        ("additional_predictive_evidence_execution_approval_for_refined_evidence_digest", review.EXPECTED_REFINED_EXECUTION_APPROVAL_DIGEST),
        ("research_registry_approval_digest", review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", review.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_digest_chain_is_bound(package: dict, field: str, expected: str) -> None:
    assert package[field] == expected


def test_registry_universe_and_record_counts_are_exact(package: dict) -> None:
    assert package["registry_approved_dataset_metadata"] == review.REGISTRY_APPROVED_DATASET_METADATA
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["meta_record_count"] == 913
    assert package["non_meta_record_count"] == 1003
    assert package["per_ticker_record_counts"] == review.EXPECTED_RECORD_COUNTS
    assert all(package["per_ticker_record_counts"][ticker] == 1003 for ticker in review.TARGET_UNIVERSE if ticker != "META")


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created", True),
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_ready", True),
        ("predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_created", True),
        ("predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_completed", True),
        ("refined_label_family_count", 7),
        ("refined_feature_group_count", 9),
        ("refined_feature_field_count", 19),
        ("refined_protocol_group_count", 6),
        ("model_comparison_group_count", 5),
        ("refined_oos_evaluation_rows", 2988),
        ("refined_oos_accuracy_range", "0.119813 to 0.480924"),
        ("refined_leakage_status", "PASS"),
        ("failed_leakage_controls", 0),
    ],
)
def test_refined_evidence_and_review_facts_are_exact(package: dict, field: str, expected: object) -> None:
    assert package[field] == expected


def test_readiness_criteria_and_findings_are_exact(package: dict) -> None:
    assert package["readiness_criteria"] == review.READINESS_CRITERIA
    findings = {item["criterion_id"]: item["result"] for item in package["readiness_findings"]}
    assert findings == review.READINESS_FINDING_RESULTS
    assert findings["minimum_refined_evidence_review_completion_required"] == review.PASS
    for criterion in (
        "refined_oos_performance_minimum_required",
        "refined_signal_consistency_required",
        "refined_baseline_outperformance_required",
        "model_comparison_support_required",
        "calibration_stability_support_required",
    ):
        assert findings[criterion] == review.NOT_MET


def test_not_ready_boundary_requires_more_evidence(package: dict) -> None:
    assert package["acceptance_candidate_allowed"] is False
    assert package["acceptance_ceremony_allowed"] is False
    assert package["additional_evidence_or_model_improvement_required"] is True
    assert package["ready_for_refined_evidence_improvement_or_additional_evidence_planning"] is True


def test_per_ticker_readiness_entries_are_complete_and_digest_bound(package: dict) -> None:
    entries = package["per_ticker_readiness_entries"]
    assert [entry["ticker"] for entry in entries] == review.TARGET_UNIVERSE
    assert len(entries) == 12
    for entry in entries:
        assert entry["historical_record_count"] == review.EXPECTED_RECORD_COUNTS[entry["ticker"]]
        assert entry["predictive_usefulness"] == review.NOT_ACCEPTED
        assert entry["runtime_use"] == review.NOT_AUTHORIZED
        assert entry["per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"] == review.per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(entry)
    meta = entries[4]
    assert meta["ticker"] == "META"
    assert meta["historical_record_count"] == 913
    assert meta["refinement_note"] == "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_READINESS_RERUN"


def test_future_chain_gates_controls_and_planned_outputs_are_exact(package: dict) -> None:
    assert package["future_improvement_chain"] == review.FUTURE_IMPROVEMENT_CHAIN
    assert package["future_gates"] == review.FUTURE_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert [item["output_name"] for item in package["planned_outputs"]] == review.PLANNED_OUTPUT_NAMES
    assert all(item["status"] == review.PLANNED_NOT_GENERATED for item in package["planned_outputs"])
    assert all(item["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE for item in package["planned_outputs"])


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
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_execution_and_runtime_actions_remain_false(package: dict, field: str) -> None:
    assert package[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", review.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", review.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("profitability_acceptance_recommended", False),
        ("runtime_migration_approved", False),
        ("runtime_use", review.NOT_AUTHORIZED),
        ("strategy_use", review.NOT_AUTHORIZED),
        ("paper_trading", review.NOT_AUTHORIZED),
        ("broker_execution", review.NOT_AUTHORIZED),
    ],
)
def test_acceptance_profitability_and_runtime_remain_closed(package: dict, field: str, expected: object) -> None:
    assert package[field] == expected


def test_checklist_and_summary_are_complete(package: dict) -> None:
    checklist = package["review_checklist"]
    assert [item["check_id"] for item in checklist] == review.REQUIRED_CHECK_IDS
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in checklist)
    assert all(item["status"] == review.PASS for item in checklist)
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS) == 79
    assert summary["passed_checks"] == 79
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["readiness_decision"] == review.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE


def test_review_and_per_ticker_digests_are_deterministic(package: dict) -> None:
    repeated = review.build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1()
    digest_field = "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
    assert repeated[digest_field] == package[digest_field]
    assert repeated[digest_field] == review.predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest_v1(repeated)
    per_ticker_field = "per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest"
    assert [item[per_ticker_field] for item in repeated["per_ticker_readiness_entries"]] == [item[per_ticker_field] for item in package["per_ticker_readiness_entries"]]


def test_validator_accepts_valid_review(package: dict) -> None:
    validation = review.validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(package)
    assert validation["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_RERUN_USING_REFINED_EVIDENCE_VALID"
    assert validation["blocker_count"] == 0
    assert validation["predictive_usefulness_acceptance_ready"] is False


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "WRONG"),
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_package_digest", "0" * 64),
        ("additional_predictive_evidence_results_review_for_refined_evidence_package_digest", "0" * 64),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("total_canonical_record_count", 11945),
        ("meta_record_count", 1003),
        ("refined_label_family_count", 6),
        ("refined_feature_group_count", 8),
        ("refined_feature_field_count", 18),
        ("refined_leakage_status", "FAIL"),
        ("failed_leakage_controls", 1),
        ("acceptance_candidate_allowed", True),
        ("acceptance_ceremony_allowed", True),
        ("additional_evidence_or_model_improvement_required", False),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
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
        ("automatic_stitching", True),
        ("future_improvement_chain", []),
        ("future_gates", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_contract_fields(package: dict, field: str, replacement: object) -> None:
    invalid = deepcopy(package)
    invalid[field] = replacement
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError):
        review.validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(invalid)


@pytest.mark.parametrize(
    "criterion",
    [
        "refined_oos_performance_minimum_required",
        "refined_signal_consistency_required",
        "refined_baseline_outperformance_required",
        "model_comparison_support_required",
        "calibration_stability_support_required",
    ],
)
def test_validator_rejects_failed_readiness_criterion_changed_to_pass(package: dict, criterion: str) -> None:
    invalid = deepcopy(package)
    next(item for item in invalid["readiness_findings"] if item["criterion_id"] == criterion)["result"] = review.PASS
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError):
        review.validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(invalid)


def test_validator_rejects_wrong_ticker_count_and_missing_digests(package: dict) -> None:
    cases = []
    wrong_meta = deepcopy(package)
    wrong_meta["per_ticker_record_counts"]["META"] = 1003
    cases.append(wrong_meta)
    missing_review_digest = deepcopy(package)
    missing_review_digest.pop("predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest")
    cases.append(missing_review_digest)
    missing_ticker_digest = deepcopy(package)
    missing_ticker_digest["per_ticker_readiness_entries"][0].pop("per_ticker_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest")
    cases.append(missing_ticker_digest)
    for invalid in cases:
        with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError):
            review.validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(invalid)


def test_markdown_contains_all_required_sections(package: dict) -> None:
    markdown = review.build_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_markdown_v1(package)
    for heading in (
        "Title",
        "Predictive Usefulness Acceptance Readiness Review Rerun Using Refined Evidence",
        "Source Reassessment Rerun",
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


def test_writer_writes_canonical_json_without_overwrite(tmp_path) -> None:
    result = review.write_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    review.validate_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(payload)
    with pytest.raises(review.PredictiveUsefulnessAcceptanceReadinessReviewRerunUsingRefinedEvidenceError):
        review.write_predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_v1(tmp_path)
