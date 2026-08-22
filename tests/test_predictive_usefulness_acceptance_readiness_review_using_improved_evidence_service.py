from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import predictive_usefulness_acceptance_readiness_review_using_improved_evidence_service as service


@pytest.fixture
def readiness_review() -> dict:
    return service.build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1()


def test_readiness_review_builds_offline(readiness_review: dict) -> None:
    assert readiness_review["created_offline"] is True
    assert readiness_review["provider_requests_made_in_readiness_review"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE),
        ("review_status", service.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_COMPLETED),
        ("readiness_decision", service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE),
        ("readiness_reason", service.READINESS_REASON),
        ("source_reassessment_digest", service.EXPECTED_REASSESSMENT_DIGEST),
        ("source_results_review_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("source_execution_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("source_output_binding_digest", service.EXPECTED_OUTPUT_BINDING_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_identity_decision_and_digest_bindings(
    readiness_review: dict, field: str, expected: object
) -> None:
    assert readiness_review[field] == expected


def test_universe_count_order_and_meta_are_preserved(readiness_review: dict) -> None:
    assert readiness_review["target_universe_count"] == 12
    assert readiness_review["target_universe"] == service.TARGET_UNIVERSE
    assert readiness_review["meta_record_count"] == 913
    assert readiness_review["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_reassessment_ready", True),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", True),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_ready", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("label_regeneration_performed", False),
        ("new_targets_created", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("metric_recomputation_performed_in_readiness_review", False),
        ("model_training_performed_in_readiness_review", False),
    ],
)
def test_authority_and_activity_boundaries(
    readiness_review: dict, field: str, expected: object
) -> None:
    assert readiness_review[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("matrix_row_count", 143352),
        ("evaluable_matrix_row_count", 142200),
        ("unavailable_target_count", 1152),
        ("oos_row_count", 34848),
        ("cross_sectional_delta_vs_majority", "0.00309917"),
        ("majority_brier", "0.04867526"),
        ("local_model_brier", "0.04867526"),
        ("cross_sectional_brier", "0.04831065"),
        ("optional_tree_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("optional_ensemble_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("leakage_control_passed", True),
        ("leakage_failed_control_count", 0),
    ],
)
def test_reviewed_evidence_facts_are_preserved(
    readiness_review: dict, field: str, expected: object
) -> None:
    assert readiness_review[field] == expected


def test_local_model_equivalence_is_preserved(readiness_review: dict) -> None:
    assert readiness_review["local_model_accuracy"] == readiness_review["majority_accuracy"] == "0.58626033"


def test_meta_limitation_entry_is_preserved(readiness_review: dict) -> None:
    meta = next(entry for entry in readiness_review["per_ticker_readiness_entries"] if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["readiness_note"] == "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE"


def test_readiness_criteria_are_complete_and_have_expected_findings(readiness_review: dict) -> None:
    criteria = readiness_review["readiness_criteria"]
    assert list(criteria) == list(service.CRITERIA_POLICY)
    assert len(criteria) == 15
    assert {name: value["criterion_status"] for name, value in criteria.items()} == {
        name: policy[0] for name, policy in service.CRITERIA_POLICY.items()
    }
    assert all(value["acceptance_evidence"] is False for value in criteria.values())
    assert all(value["research_only"] is True and value["non_actionable"] is True for value in criteria.values())


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("readiness_classification", "COMPLETED_RESEARCH_ONLY"),
        ("predictive_signal_readiness", "NOT_READY"),
        ("baseline_outperformance_readiness", "NOT_READY"),
        ("local_model_readiness", "NOT_READY"),
        ("cross_sectional_edge_readiness", "NOT_READY"),
        ("oos_performance_readiness", "NOT_READY"),
        ("walk_forward_readiness", "REQUIRES_OPERATOR_REVIEW"),
        ("calibration_brier_readiness", "REQUIRES_OPERATOR_REVIEW"),
        ("leakage_readiness", "PASS"),
        ("meta_readiness", "PASS_WITH_OPERATOR_AWARENESS"),
        ("acceptance_candidate_allowed", False),
        ("additional_evidence_or_method_improvement_required", True),
    ],
)
def test_readiness_classification_is_conservative(
    readiness_review: dict, field: str, expected: object
) -> None:
    assert readiness_review[field] == expected


def test_per_ticker_entries_and_digests_are_complete(readiness_review: dict) -> None:
    entries = readiness_review["per_ticker_readiness_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_predictive_usefulness_acceptance_readiness_digest"]) == 64 for entry in entries)


def test_next_chain_gates_and_risk_controls_are_defined(readiness_review: dict) -> None:
    assert readiness_review["next_chain"] == service.NEXT_CHAIN
    assert readiness_review["next_gates"] == service.NEXT_GATES
    assert readiness_review["risk_controls"] == service.RISK_CONTROLS
    assert len(readiness_review["risk_controls"]) == 26


def test_checklist_passes(readiness_review: dict) -> None:
    assert readiness_review["readiness_summary"]["total_checks"] == 84
    assert readiness_review["readiness_summary"]["passed_checks"] == 84
    assert readiness_review["readiness_summary"]["failed_checks"] == 0
    assert readiness_review["readiness_summary"]["blocker_count"] == 0


def test_readiness_digest_is_deterministic(readiness_review: dict) -> None:
    rebuilt = service.build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1()
    assert rebuilt["predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"] == readiness_review["predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"]


def test_per_ticker_digests_are_deterministic(readiness_review: dict) -> None:
    rebuilt = service.build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1()
    assert [row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] for row in rebuilt["per_ticker_readiness_entries"]] == [row["per_ticker_predictive_usefulness_acceptance_readiness_digest"] for row in readiness_review["per_ticker_readiness_entries"]]


def test_validator_accepts_valid_readiness_review(readiness_review: dict) -> None:
    validation = service.validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(readiness_review)
    assert validation["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE_VALID"
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("readiness_decision", "READY"),
        ("readiness_reason", "WRONG"),
        ("source_reassessment_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64),
        ("source_execution_digest", "0" * 64),
        ("source_output_binding_digest", "0" * 64),
        ("selected_redesign_direction", "WRONG"),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", False),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("metric_recomputation_performed_in_readiness_review", True),
        ("model_training_performed_in_readiness_review", True),
        ("provider_requests_made_in_readiness_review", True),
        ("market_data_acquisition_performed_in_readiness_review", True),
        ("canonical_dataset_regenerated_in_readiness_review", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    readiness_review: dict, field: str, value: object
) -> None:
    invalid = deepcopy(readiness_review)
    invalid[field] = value
    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError):
        service.validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(invalid)


@pytest.mark.parametrize("field", ["readiness_criteria", "readiness_classification", "risk_controls"])
def test_validator_rejects_missing_required_readiness_content(
    readiness_review: dict, field: str
) -> None:
    invalid = deepcopy(readiness_review)
    invalid.pop(field)
    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError):
        service.validate_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(invalid)


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(tmp_path)
    assert result["path"].endswith("predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1.json")
    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessReviewImprovedEvidenceError):
        service.write_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_v1(tmp_path)


def test_markdown_includes_required_sections(readiness_review: dict) -> None:
    markdown = service.build_predictive_usefulness_acceptance_readiness_review_using_improved_evidence_markdown_v1(readiness_review)
    required = [
        "Title",
        "Predictive Usefulness Acceptance Readiness Review Using Improved Evidence",
        "Source Reassessment",
        "Bound Evidence",
        "Dataset and Universe",
        "Evidence Summary",
        "Readiness Decision",
        "Readiness Criteria",
        "Predictive Signal Readiness",
        "Baseline Outperformance Readiness",
        "Local Model Readiness",
        "Cross-Sectional Edge Readiness",
        "OOS Readiness",
        "Walk-Forward Readiness",
        "Calibration / Brier Readiness",
        "Optional Model Coverage",
        "Leakage Readiness",
        "META Readiness",
        "Acceptance Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Per-Ticker Readiness",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)
