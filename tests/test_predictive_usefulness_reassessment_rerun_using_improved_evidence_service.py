from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import predictive_usefulness_reassessment_rerun_using_improved_evidence_service as service


@pytest.fixture
def reassessment() -> dict:
    return service.build_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1()


def test_reassessment_builds_offline(reassessment: dict) -> None:
    assert reassessment["created_offline"] is True
    assert reassessment["provider_requests_made_in_reassessment"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE),
        ("reassessment_status", service.PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY),
        ("source_results_review_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("source_execution_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("source_output_binding_digest", service.EXPECTED_OUTPUT_BINDING_DIGEST),
        ("source_approval_digest", service.EXPECTED_APPROVAL_DIGEST),
        ("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest", service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest", service.EXPECTED_CANDIDATE_DIGEST),
        ("improved_evidence_planning_results_review_using_redesigned_evidence_digest", service.SOURCE_EVIDENCE["improved_evidence_planning_results_review_using_redesigned_evidence_digest"]),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_identity_and_digest_bindings(reassessment: dict, field: str, expected: object) -> None:
    assert reassessment[field] == expected


def test_universe_count_order_and_meta_are_preserved(reassessment: dict) -> None:
    assert reassessment["target_universe_count"] == 12
    assert reassessment["target_universe"] == service.TARGET_UNIVERSE
    assert reassessment["meta_record_count"] == 913
    assert reassessment["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_results_review_ready", True),
        ("predictive_usefulness_reassessment_using_improved_evidence_created", True),
        ("predictive_usefulness_reassessment_using_improved_evidence_ready", True),
        ("ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence", True),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", False),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("label_regeneration_performed", False),
        ("new_targets_created", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("metric_recomputation_performed_in_reassessment", False),
        ("model_training_performed_in_reassessment", False),
    ],
)
def test_authority_and_activity_boundaries(reassessment: dict, field: str, expected: object) -> None:
    assert reassessment[field] == expected


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
def test_reviewed_evidence_facts_are_preserved(reassessment: dict, field: str, expected: object) -> None:
    assert reassessment[field] == expected


def test_local_model_equivalence_is_preserved(reassessment: dict) -> None:
    assert reassessment["local_model_accuracy"] == reassessment["majority_accuracy"] == "0.58626033"


def test_meta_limitation_entry_is_preserved(reassessment: dict) -> None:
    meta = next(entry for entry in reassessment["per_ticker_reassessment_entries"] if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["reassessment_note"] == "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_IMPROVED_EVIDENCE"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("reassessment_classification", "COMPLETED_RESEARCH_ONLY"),
        ("predictive_signal_review", "WEAK_TO_MODEST_MIXED"),
        ("baseline_outperformance_review", "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE"),
        ("local_model_review", "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE"),
        ("cross_sectional_review", "SMALL_EDGE_REQUIRES_ACCEPTANCE_READINESS_REVIEW"),
        ("acceptance_recommendation", "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE"),
    ],
)
def test_classification_is_conservative(reassessment: dict, field: str, expected: str) -> None:
    assert reassessment[field] == expected


def test_reassessment_domains_are_complete_and_non_actionable(reassessment: dict) -> None:
    assert list(reassessment["reassessment_domains"]) == list(service.DOMAIN_INTERPRETATIONS)
    assert len(reassessment["reassessment_domains"]) == 17
    assert all(domain["domain_status"] == "REVIEWED_RESEARCH_ONLY" for domain in reassessment["reassessment_domains"].values())
    assert all(domain["acceptance_evidence"] is False for domain in reassessment["reassessment_domains"].values())
    assert all(domain["research_only"] is True and domain["non_actionable"] is True for domain in reassessment["reassessment_domains"].values())


def test_per_ticker_entries_and_digests_are_complete(reassessment: dict) -> None:
    entries = reassessment["per_ticker_reassessment_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_predictive_usefulness_reassessment_digest"]) == 64 for entry in entries)


def test_next_chain_and_risk_controls_are_defined(reassessment: dict) -> None:
    assert reassessment["next_chain"] == service.NEXT_CHAIN
    assert reassessment["next_gates"] == service.NEXT_GATES
    assert reassessment["risk_controls"] == service.RISK_CONTROLS
    assert len(reassessment["risk_controls"]) == 25


def test_checklist_passes(reassessment: dict) -> None:
    assert reassessment["reassessment_summary"]["total_checks"] == 80
    assert reassessment["reassessment_summary"]["passed_checks"] == 80
    assert reassessment["reassessment_summary"]["failed_checks"] == 0
    assert reassessment["reassessment_summary"]["blocker_count"] == 0


def test_reassessment_digest_is_deterministic(reassessment: dict) -> None:
    rebuilt = service.build_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1()
    assert rebuilt["predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"] == reassessment["predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"]


def test_per_ticker_digests_are_deterministic(reassessment: dict) -> None:
    rebuilt = service.build_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1()
    assert [row["per_ticker_predictive_usefulness_reassessment_digest"] for row in rebuilt["per_ticker_reassessment_entries"]] == [row["per_ticker_predictive_usefulness_reassessment_digest"] for row in reassessment["per_ticker_reassessment_entries"]]


def test_validator_accepts_valid_reassessment(reassessment: dict) -> None:
    validation = service.validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(reassessment)
    assert validation["status"] == "PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_VALID"
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("reassessment_status", "WRONG"),
        ("source_results_review_digest", "0" * 64),
        ("source_execution_digest", "0" * 64),
        ("source_output_binding_digest", "0" * 64),
        ("source_approval_digest", "0" * 64),
        ("selected_redesign_direction", "WRONG"),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("runtime_use", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("metric_recomputation_performed_in_reassessment", True),
        ("model_training_performed_in_reassessment", True),
        ("provider_requests_made_in_reassessment", True),
        ("market_data_acquisition_performed_in_reassessment", True),
        ("canonical_dataset_regenerated_in_reassessment", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(reassessment: dict, field: str, value: object) -> None:
    invalid = deepcopy(reassessment)
    invalid[field] = value
    with pytest.raises(service.PredictiveUsefulnessReassessmentRerunImprovedEvidenceError):
        service.validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(invalid)


@pytest.mark.parametrize("field", ["reassessment_domains", "risk_controls"])
def test_validator_rejects_missing_required_collections(reassessment: dict, field: str) -> None:
    invalid = deepcopy(reassessment)
    invalid.pop(field)
    with pytest.raises(service.PredictiveUsefulnessReassessmentRerunImprovedEvidenceError):
        service.validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(invalid)


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(tmp_path)
    assert result["path"].endswith("predictive_usefulness_reassessment_rerun_using_improved_evidence_v1.json")
    with pytest.raises(service.PredictiveUsefulnessReassessmentRerunImprovedEvidenceError):
        service.write_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(tmp_path)


def test_markdown_includes_required_sections(reassessment: dict) -> None:
    markdown = service.build_predictive_usefulness_reassessment_rerun_using_improved_evidence_markdown_v1(reassessment)
    required = [
        "Title",
        "Predictive Usefulness Reassessment Rerun Using Improved Evidence",
        "Source Results Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Evidence Summary",
        "Reassessment Classification",
        "Predictive Signal Review",
        "Baseline Outperformance Review",
        "Local Model Review",
        "Cross-Sectional Edge Review",
        "OOS Review",
        "Walk-Forward Review",
        "Calibration / Brier Review",
        "Leakage Review",
        "META Limitation Review",
        "Acceptance Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Per-Ticker Reassessment",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)
