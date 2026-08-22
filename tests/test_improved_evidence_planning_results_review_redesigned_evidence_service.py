from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import improved_evidence_planning_execution_redesigned_evidence_service as execution
from marketflow.services import improved_evidence_planning_results_review_redesigned_evidence_service as review


FIXED_TIMESTAMP = "2026-08-22T12:00:00Z"


def _verification() -> dict:
    return {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": True,
        "all_required_source_bindings_match": True,
        "source_files_unchanged": True,
        "source_file_count": len(execution.SOURCE_FILES),
        "source_file_sha256": {},
        "verified_records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "verified_redesigned_label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
        "verified_feature_values_digest": execution.EXPECTED_FEATURE_VALUES_DIGEST,
        "verified_feature_label_matrix_digest": execution.EXPECTED_MATRIX_DIGEST,
        "verified_redesign_execution_digest": execution.EXPECTED_REDESIGN_EXECUTION_DIGEST,
        "verified_redesign_output_binding_digest": execution.EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST,
        "verified_review_execution_digest": execution.EXPECTED_REVIEW_EXECUTION_DIGEST,
        "verified_review_output_binding_digest": execution.EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST,
    }


@pytest.fixture
def reviewed(tmp_path, monkeypatch: pytest.MonkeyPatch):
    output_root = tmp_path / "outputs"
    monkeypatch.setattr(execution, "_verify_sources", lambda _roots: (_verification(), {}, []))
    monkeypatch.setattr(
        execution,
        "improved_evidence_planning_execution_using_redesigned_evidence_digest_v1",
        lambda _artifact: review.EXPECTED_EXECUTION_DIGEST,
    )
    artifact = execution.execute_improved_evidence_planning_using_redesigned_evidence_v1(
        canonical_root=tmp_path / "canonical", label_root=tmp_path / "labels",
        feature_root=tmp_path / "features", predictive_evidence_root=tmp_path / "predictive",
        label_objective_review_root=tmp_path / "review", label_objective_redesign_root=tmp_path / "redesign",
        output_root=output_root, run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["improved_evidence_planning_execution_using_redesigned_evidence_digest"] == review.EXPECTED_EXECUTION_DIGEST
    return review.build_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
        output_root=output_root
    ), output_root


def test_results_review_builds_offline(reviewed, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("socket.socket.connect", lambda *_args, **_kwargs: pytest.fail("network access"))
    package, _ = reviewed
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_results_review_blocks_when_output_root_is_missing(tmp_path) -> None:
    package = review.build_improved_evidence_planning_results_review_using_redesigned_evidence_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["blocker_count"] == 14


def test_artifact_kind_and_review_status_are_exact(reviewed) -> None:
    package, _ = reviewed
    assert package["artifact_kind"] == review.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE
    assert package["review_status"] == review.IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY


@pytest.mark.parametrize(("field", "expected"), list(review._source_evidence().items()))
def test_all_source_evidence_digests_are_bound(reviewed, field: str, expected: str) -> None:
    package, _ = reviewed
    assert package["source_evidence"][field] == expected


def test_source_execution_output_binding_and_approval_are_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["source_execution_digest"] == review.EXPECTED_EXECUTION_DIGEST
    assert package["source_output_binding_digest"] == review.EXPECTED_OUTPUT_BINDING_DIGEST
    assert package["source_approval_digest"] == review.EXPECTED_APPROVAL_DIGEST


def test_dataset_universe_and_meta_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["target_universe"] == execution.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert package["meta_record_count"] == 913
    assert package["non_meta_record_count"] == 1003


def test_selected_direction_and_planning_scope_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["selected_redesign_direction"] == execution.SELECTED_DIRECTION
    assert package["review_classification"]["planning_execution_scope_review"] == execution.PLANNING_EXECUTION_SCOPE
    assert package["review_classification"]["selected_redesign_direction_review"] == "REVIEWED_RESEARCH_ONLY"
    assert package["review_classification"]["additional_predictive_evidence_candidate_readiness"] == "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION"


def test_output_verification_is_complete_and_digest_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["generated_output_count"] == 14
    assert package["expected_output_count"] == 14
    assert package["observed_output_count"] == 14
    assert package["output_digest_mismatch_count"] == 0
    assert package["non_self_output_digest_match_count"] == 13
    assert len(package["local_output_hashes"]) == 14
    assert package["outputs_research_only_non_actionable"] is True


@pytest.mark.parametrize("field", [
    "planning_execution_manifest_review", "proposed_label_schema_plan_review",
    "no_trade_abstain_coverage_plan_review", "material_move_threshold_plan_review",
    "horizon_specific_validation_plan_review", "ticker_regime_split_validation_plan_review",
    "feature_label_alignment_plan_review", "chronological_split_embargo_plan_review",
    "baseline_model_comparison_plan_review", "calibration_brier_plan_review",
    "leakage_no_peek_control_plan_review", "per_ticker_meta_reporting_plan_review",
    "operator_summary_review",
])
def test_each_planning_output_is_verified(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field]["verified"] is True


def test_results_review_readiness_is_open_but_candidate_is_not_created(reviewed) -> None:
    package, _ = reviewed
    assert package["improved_evidence_planning_results_review_created"] is True
    assert package["improved_evidence_planning_results_review_ready"] is True
    assert package["ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"] is True
    assert package["additional_predictive_evidence_execution_candidate_created"] is False
    assert package["additional_predictive_evidence_executed"] is False


@pytest.mark.parametrize("field", [
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
    "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created",
    "trade_recommendations_generated", "improved_evidence_planning_execution_rerun_performed",
    "metric_recomputation_performed_in_review", "model_training_performed_in_review",
])
def test_all_execution_and_acceptance_authorities_remain_false(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed(reviewed) -> None:
    package, _ = reviewed
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert package[field] == "NOT_AUTHORIZED"


def test_per_ticker_entries_and_meta_limitation_are_preserved(reviewed) -> None:
    package, _ = reviewed
    entries = package["per_ticker_results_review_entries"]
    assert len(entries) == 12
    assert all(len(row["per_ticker_improved_evidence_planning_results_review_digest"]) == 64 for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["review_note"] == "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW"


def test_limitations_next_chain_next_gates_and_risk_controls_are_exact(reviewed) -> None:
    package, _ = reviewed
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_chain"] == review.NEXT_CHAIN
    assert package["next_gates"] == review.NEXT_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_checklist_passes(reviewed) -> None:
    package, _ = reviewed
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in package["review_checklist"])
    assert package["review_summary"] == {
        "total_checks": 88, "passed_checks": 88, "failed_checks": 0, "blocker_count": 0,
        "results_review_ready": True,
        "ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence": True,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False, "predictive_usefulness_accepted": False,
        "profitability_accepted": False, "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_review_digest_is_deterministic(reviewed) -> None:
    package, _ = reviewed
    assert package["improved_evidence_planning_results_review_using_redesigned_evidence_digest"] == review.improved_evidence_planning_results_review_using_redesigned_evidence_digest_v1(package)


def test_validator_accepts_valid_package(reviewed) -> None:
    package, _ = reviewed
    validation = review.validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(package)
    assert validation["status"] == review.IMPROVED_EVIDENCE_PLANNING_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("source_execution_digest", "0" * 64),
    ("source_output_binding_digest", "0" * 64), ("source_approval_digest", "0" * 64),
    ("selected_redesign_direction", "WRONG"), ("target_universe", ["AAPL"]),
    ("target_universe_count", 11), ("records_digest", "0" * 64), ("meta_record_count", 1003),
    ("generated_output_count", 13), ("output_digest_mismatch_count", 1),
    ("improved_evidence_planning_results_review_ready", False),
    ("label_regeneration_authorized", True), ("label_regeneration_performed", True),
    ("new_targets_created", True), ("target_definition_change_authorized", True),
    ("target_definition_change_performed", True), ("feature_generation_performed", True),
    ("feature_label_matrix_created", True),
    ("additional_predictive_evidence_execution_candidate_created", True),
    ("additional_predictive_evidence_executed", True), ("predictive_usefulness", "accepted"),
    ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("provider_requests_made_in_review", True),
    ("market_data_acquisition_performed_in_review", True), ("canonical_dataset_regenerated_in_review", True),
    ("improved_evidence_planning_execution_rerun_performed", True),
    ("metric_recomputation_performed_in_review", True), ("model_training_performed_in_review", True),
])
def test_validator_rejects_forbidden_mutations(reviewed, field: str, value) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed[field] = value
    with pytest.raises(review.ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError):
        review.validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(changed)


@pytest.mark.parametrize("field", ["limitations", "next_chain", "risk_controls",
                                    "improved_evidence_planning_results_review_using_redesigned_evidence_digest"])
def test_validator_rejects_missing_required_sections(reviewed, field: str) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop(field)
    with pytest.raises(review.ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError):
        review.validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(reviewed) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed["per_ticker_results_review_entries"][0].pop("per_ticker_improved_evidence_planning_results_review_digest")
    with pytest.raises(review.ImprovedEvidencePlanningResultsReviewRedesignedEvidenceError):
        review.validate_improved_evidence_planning_results_review_using_redesigned_evidence_v1(changed)


def test_markdown_includes_required_sections(reviewed) -> None:
    package, _ = reviewed
    markdown = review.build_improved_evidence_planning_results_review_using_redesigned_evidence_markdown_v1(package)
    for heading in (
        "# MarketFlow Improved Evidence Planning Results Review Using Redesigned Evidence Status",
        "## Source Execution", "## Output Verification", "## Planning Scope Review",
        "## Proposed Label Schema Plan Review", "## No-Trade / Abstain Coverage Plan Review",
        "## Material-Move Threshold Plan Review", "## Horizon-Specific Validation Plan Review",
        "## Ticker / Regime Split Validation Plan Review", "## Feature-Label Alignment Plan Review",
        "## Chronological Split and Embargo Plan Review", "## Baseline and Model Comparison Plan Review",
        "## Calibration / Brier Plan Review", "## Leakage and No-Peek Control Plan Review",
        "## Per-Ticker and META Reporting Plan Review", "## Review Classification", "## Limitations",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Guardrails",
    ):
        assert heading in markdown
