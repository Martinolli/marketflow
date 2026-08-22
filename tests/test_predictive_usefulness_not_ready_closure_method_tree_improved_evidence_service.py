from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import predictive_usefulness_not_ready_closure_method_tree_improved_evidence_service as service


@pytest.fixture
def closure() -> dict:
    return service.build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1()


def test_closure_builds_offline(closure: dict) -> None:
    assert closure["created_offline"] is True
    assert closure["provider_requests_made_in_closure"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE),
        ("closure_status", service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE),
        ("closure_decision", service.CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION),
        ("closure_reason", service.CLOSURE_REASON),
        ("source_readiness_digest", service.EXPECTED_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_REASSESSMENT_DIGEST),
        ("source_results_review_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("source_execution_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_identity_decision_and_digest_bindings(
    closure: dict, field: str, expected: object
) -> None:
    assert closure[field] == expected


def test_universe_count_order_and_meta_are_preserved(closure: dict) -> None:
    assert closure["target_universe_count"] == 12
    assert closure["target_universe"] == service.TARGET_UNIVERSE
    assert closure["meta_record_count"] == 913
    assert closure["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE"),
        ("current_improved_evidence_acceptance_path_closure_created", True),
        ("predictive_usefulness_acceptance_path_closed_for_current_improved_evidence", True),
        ("method_planning_tree_created", True),
        ("operator_future_method_selection_required", True),
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
        ("metric_recomputation_performed_in_closure", False),
        ("model_training_performed_in_closure", False),
        ("additional_predictive_evidence_execution_rerun_performed", False),
        ("predictive_usefulness_reassessment_rerun_performed", False),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", False),
    ],
)
def test_closure_authority_and_activity_boundaries(
    closure: dict, field: str, expected: object
) -> None:
    assert closure[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("matrix_row_count", 143352),
        ("evaluable_matrix_row_count", 142200),
        ("unavailable_target_count", 1152),
        ("oos_row_count", 34848),
        ("cross_sectional_delta_vs_majority", "0.00309917"),
        ("optional_tree_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("optional_ensemble_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("leakage_control_passed", True),
        ("leakage_failed_control_count", 0),
    ],
)
def test_evidence_values_are_preserved(closure: dict, field: str, expected: object) -> None:
    assert closure[field] == expected


def test_local_model_equivalence_is_preserved(closure: dict) -> None:
    assert closure["local_model_accuracy"] == closure["majority_accuracy"] == "0.58626033"


def test_meta_limitation_entry_is_preserved(closure: dict) -> None:
    meta = next(entry for entry in closure["per_ticker_closure_entries"] if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["closure_note"] == "PRESERVE_META_LIMITATION_IN_NOT_READY_CLOSURE_USING_IMPROVED_EVIDENCE"


def test_method_tree_options_are_present_and_unselected(closure: dict) -> None:
    options = closure["method_planning_tree_options"]
    assert list(options) == list(service.METHOD_PLANNING_TREE)
    assert len(options) == 8
    assert all(option["selected"] is False for option in options.values())


def test_option_a_stop_current_dataset_is_recommended(closure: dict) -> None:
    assert closure["recommended_current_decision"] == "OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET"
    assert closure["method_planning_tree_options"]["OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET"]["option_status"] == "RECOMMENDED_CURRENT_DECISION"


def test_acceptance_candidate_option_is_not_allowed(closure: dict) -> None:
    option = closure["method_planning_tree_options"]["OPTION_H_ACCEPTANCE_CANDIDATE"]
    assert option["option_status"] == "NOT_ALLOWED_CURRENTLY"
    assert option["selected"] is False


def test_per_ticker_entries_and_digests_are_complete(closure: dict) -> None:
    entries = closure["per_ticker_closure_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_not_ready_closure_digest"]) == 64 for entry in entries)


def test_next_chain_gates_and_risk_controls_are_defined(closure: dict) -> None:
    assert closure["next_chain"] == service.NEXT_CHAIN
    assert closure["next_gates"] == service.NEXT_GATES
    assert closure["risk_controls"] == service.RISK_CONTROLS
    assert len(closure["risk_controls"]) == 29


def test_checklist_passes(closure: dict) -> None:
    assert closure["closure_summary"]["total_checks"] == 67
    assert closure["closure_summary"]["passed_checks"] == 67
    assert closure["closure_summary"]["failed_checks"] == 0
    assert closure["closure_summary"]["blocker_count"] == 0


def test_closure_digest_is_deterministic(closure: dict) -> None:
    rebuilt = service.build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1()
    assert rebuilt["predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"] == closure["predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"]


def test_per_ticker_digests_are_deterministic(closure: dict) -> None:
    rebuilt = service.build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1()
    assert [row["per_ticker_not_ready_closure_digest"] for row in rebuilt["per_ticker_closure_entries"]] == [row["per_ticker_not_ready_closure_digest"] for row in closure["per_ticker_closure_entries"]]


def test_validator_accepts_valid_closure(closure: dict) -> None:
    validation = service.validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(closure)
    assert validation["status"] == "PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_USING_IMPROVED_EVIDENCE_VALID"
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("closure_status", "WRONG"),
        ("closure_decision", "WRONG"),
        ("closure_reason", "WRONG"),
        ("source_readiness_digest", "0" * 64),
        ("selected_redesign_direction", "WRONG"),
        ("current_improved_evidence_acceptance_path_closure_created", False),
        ("predictive_usefulness_acceptance_path_closed_for_current_improved_evidence", False),
        ("method_planning_tree_created", False),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("metric_recomputation_performed_in_closure", True),
        ("model_training_performed_in_closure", True),
        ("provider_requests_made_in_closure", True),
        ("market_data_acquisition_performed_in_closure", True),
        ("canonical_dataset_regenerated_in_closure", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    closure: dict, field: str, value: object
) -> None:
    invalid = deepcopy(closure)
    invalid[field] = value
    with pytest.raises(service.PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError):
        service.validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(invalid)


@pytest.mark.parametrize("field", ["method_planning_tree_options", "risk_controls"])
def test_validator_rejects_missing_required_collections(closure: dict, field: str) -> None:
    invalid = deepcopy(closure)
    invalid.pop(field)
    with pytest.raises(service.PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError):
        service.validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(invalid)


def test_validator_rejects_acceptance_candidate_option_allowed(closure: dict) -> None:
    invalid = deepcopy(closure)
    invalid["method_planning_tree_options"]["OPTION_H_ACCEPTANCE_CANDIDATE"]["option_status"] = "AVAILABLE"
    with pytest.raises(service.PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError):
        service.validate_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(invalid)


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(tmp_path)
    assert result["path"].endswith("predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1.json")
    with pytest.raises(service.PredictiveUsefulnessNotReadyClosureMethodTreeImprovedEvidenceError):
        service.write_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_v1(tmp_path)


def test_markdown_includes_required_sections(closure: dict) -> None:
    markdown = service.build_predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_markdown_v1(closure)
    required = [
        "Title",
        "Predictive Usefulness Not-Ready Closure and Method Planning Tree Using Improved Evidence",
        "Source Readiness Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Closure Decision",
        "Closure Basis",
        "Evidence Summary",
        "Why Acceptance Is Not Ready",
        "Method Planning Tree",
        "Recommended Current Decision",
        "Per-Ticker Closure",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)
