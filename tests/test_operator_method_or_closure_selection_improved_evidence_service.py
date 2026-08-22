from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import operator_method_or_closure_selection_improved_evidence_service as service


@pytest.fixture
def operator_attestation() -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-22T23:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_METHOD_OR_CLOSURE_SELECTION_ATTESTATION_PHRASE,
        "operator_confirms_source_closure_digest": service.EXPECTED_CLOSURE_DIGEST,
        "operator_confirms_source_readiness_digest": service.EXPECTED_READINESS_DIGEST,
        "operator_confirms_records_digest": service.EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": service.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": service.SELECTED_OPTION,
        **{field: True for field in service.ATTESTATION_BOOLEAN_FIELDS},
    }
    return service.build_operator_method_or_closure_selection_using_improved_evidence_attestation_v1(
        **kwargs
    )


@pytest.fixture
def selection(operator_attestation: dict) -> dict:
    return service.build_operator_method_or_closure_selection_using_improved_evidence_v1(
        operator_attestation=operator_attestation
    )


def test_attestation_builder_creates_required_fields(operator_attestation: dict) -> None:
    assert operator_attestation["operator_decision"] == service.SELECTED_DECISION
    assert operator_attestation["selected_option"] == service.SELECTED_OPTION
    assert operator_attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert all(operator_attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_selection_builds_offline(selection: dict) -> None:
    assert selection["created_offline"] is True
    assert selection["provider_requests_made_in_selection"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE),
        ("selection_status", service.OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_IMPROVED_EVIDENCE),
        ("selection_scope", service.OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY),
        ("selected_option", service.SELECTED_OPTION),
        ("selection_decision", service.SELECTED_DECISION),
        ("selection_rationale", service.SELECTION_RATIONALE),
        ("source_closure_digest", service.EXPECTED_CLOSURE_DIGEST),
        ("source_readiness_digest", service.EXPECTED_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_REASSESSMENT_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_identity_decision_and_digest_bindings(
    selection: dict, field: str, expected: object
) -> None:
    assert selection[field] == expected


def test_universe_count_order_and_meta_are_preserved(selection: dict) -> None:
    assert selection["target_universe_count"] == 12
    assert selection["target_universe"] == service.TARGET_UNIVERSE
    assert selection["meta_record_count"] == 913
    assert selection["meta_reduced_record_count_preserved"] is True


def test_operator_decision_and_phrase_match(selection: dict) -> None:
    attestation = selection["operator_attestation"]
    assert attestation["operator_decision"] == service.SELECTED_DECISION
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_METHOD_OR_CLOSURE_SELECTION_ATTESTATION_PHRASE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("operator_method_or_closure_selection_created", True),
        ("operator_method_or_closure_selection_ready", True),
        ("ready_for_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence", True),
        ("archive_record_created", False),
        ("method_improvement_candidate_created", False),
        ("future_evidence_candidate_created", False),
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
        ("metric_recomputation_performed_in_selection", False),
        ("model_training_performed_in_selection", False),
        ("additional_predictive_evidence_execution_rerun_performed", False),
        ("predictive_usefulness_reassessment_rerun_performed", False),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", False),
    ],
)
def test_selection_authority_and_activity_boundaries(
    selection: dict, field: str, expected: object
) -> None:
    assert selection[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("matrix_row_count", 143352),
        ("cross_sectional_delta_vs_majority", "0.00309917"),
        ("optional_tree_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("optional_ensemble_model_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("leakage_control_passed", True),
        ("leakage_failed_control_count", 0),
    ],
)
def test_evidence_values_are_preserved(selection: dict, field: str, expected: object) -> None:
    assert selection[field] == expected


def test_local_model_equivalence_is_preserved(selection: dict) -> None:
    assert selection["local_model_accuracy"] == selection["majority_accuracy"] == "0.58626033"


def test_selection_options_are_present(selection: dict) -> None:
    assert selection["selection_options_review"] == service.SELECTION_OPTIONS_REVIEW
    assert len(selection["selection_options_review"]) == 8


def test_option_a_selected_and_matches_source_recommendation(selection: dict) -> None:
    assert selection["selected_option"] == selection["recommended_current_decision"] == service.SELECTED_OPTION
    assert selection["selection_options_review"][service.SELECTED_OPTION]["selection_status"] == "SELECTED_BY_OPERATOR"


def test_option_h_acceptance_candidate_is_not_allowed(selection: dict) -> None:
    assert selection["selection_options_review"]["OPTION_H_ACCEPTANCE_CANDIDATE"]["selection_status"] == "NOT_ALLOWED_CURRENTLY"


def test_meta_limitation_entry_is_preserved(selection: dict) -> None:
    meta = next(entry for entry in selection["per_ticker_selection_entries"] if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["selection_note"] == "PRESERVE_META_LIMITATION_IN_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE"


def test_per_ticker_entries_and_digests_are_complete(selection: dict) -> None:
    entries = selection["per_ticker_selection_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_operator_method_or_closure_selection_digest"]) == 64 for entry in entries)


def test_next_chain_gates_and_risk_controls_are_defined(selection: dict) -> None:
    assert selection["next_chain"] == service.NEXT_CHAIN
    assert selection["next_gates"] == service.NEXT_GATES
    assert selection["risk_controls"] == service.RISK_CONTROLS
    assert len(selection["risk_controls"]) == 30


def test_checklist_passes(selection: dict) -> None:
    summary = selection["selection_summary"]
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_selection_digest_is_deterministic(operator_attestation: dict, selection: dict) -> None:
    rebuilt = service.build_operator_method_or_closure_selection_using_improved_evidence_v1(
        operator_attestation=operator_attestation
    )
    assert rebuilt["operator_method_or_closure_selection_using_improved_evidence_digest"] == selection["operator_method_or_closure_selection_using_improved_evidence_digest"]


def test_per_ticker_digests_are_deterministic(operator_attestation: dict, selection: dict) -> None:
    rebuilt = service.build_operator_method_or_closure_selection_using_improved_evidence_v1(
        operator_attestation=operator_attestation
    )
    assert [row["per_ticker_operator_method_or_closure_selection_digest"] for row in rebuilt["per_ticker_selection_entries"]] == [row["per_ticker_operator_method_or_closure_selection_digest"] for row in selection["per_ticker_selection_entries"]]


def test_validator_accepts_valid_selection(selection: dict) -> None:
    validation = service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(selection)
    assert validation["status"] == "OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_IMPROVED_EVIDENCE_VALID"
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("selection_status", "WRONG"),
        ("selection_scope", "WRONG"),
        ("selected_option", "WRONG"),
        ("selection_decision", "WRONG"),
        ("selection_rationale", "WRONG"),
        ("source_closure_digest", "0" * 64),
        ("source_readiness_digest", "0" * 64),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("ready_for_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence", False),
        ("archive_record_created", True),
        ("method_improvement_candidate_created", True),
        ("future_evidence_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("metric_recomputation_performed_in_selection", True),
        ("model_training_performed_in_selection", True),
        ("provider_requests_made_in_selection", True),
        ("market_data_acquisition_performed_in_selection", True),
        ("canonical_dataset_regenerated_in_selection", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    selection: dict, field: str, value: object
) -> None:
    invalid = deepcopy(selection)
    invalid[field] = value
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
    ],
)
def test_validator_rejects_wrong_operator_attestation(
    selection: dict, field: str, value: str
) -> None:
    invalid = deepcopy(selection)
    invalid["operator_attestation"][field] = value
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


@pytest.mark.parametrize("field", ["selection_options_review", "risk_controls"])
def test_validator_rejects_missing_required_collections(selection: dict, field: str) -> None:
    invalid = deepcopy(selection)
    invalid.pop(field)
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


def test_validator_rejects_acceptance_candidate_option_allowed(selection: dict) -> None:
    invalid = deepcopy(selection)
    invalid["selection_options_review"]["OPTION_H_ACCEPTANCE_CANDIDATE"]["selection_status"] = "ALLOWED"
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


def test_attestation_mismatch_fails_closed(operator_attestation: dict) -> None:
    invalid = deepcopy(operator_attestation)
    invalid["operator_confirms_target_count"] = 11
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.build_operator_method_or_closure_selection_using_improved_evidence_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_confirms_source_closure_digest", "0" * 64),
        ("operator_confirms_source_readiness_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("operator_attestation_phrase", "WRONG"),
        ("selected_option", "WRONG"),
        ("operator_confirms_selected_option", "WRONG"),
        ("operator_confirms_selection_scope_only", False),
        ("operator_confirms_acceptance_path_closed_current_dataset", False),
    ],
)
def test_attestation_wrong_binding_or_closed_boundary_fails_closed(
    operator_attestation: dict, field: str, value: object
) -> None:
    invalid = deepcopy(operator_attestation)
    invalid[field] = value
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.build_operator_method_or_closure_selection_using_improved_evidence_v1(
            operator_attestation=invalid
        )


def test_validator_rejects_missing_selection_digest(selection: dict) -> None:
    invalid = deepcopy(selection)
    invalid.pop("operator_method_or_closure_selection_using_improved_evidence_digest")
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(selection: dict) -> None:
    invalid = deepcopy(selection)
    invalid["per_ticker_selection_entries"][0].pop(
        "per_ticker_operator_method_or_closure_selection_digest"
    )
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.validate_operator_method_or_closure_selection_using_improved_evidence_v1(invalid)


def test_writer_uses_isolated_output_and_refuses_overwrite(
    tmp_path, operator_attestation: dict
) -> None:
    result = service.write_operator_method_or_closure_selection_using_improved_evidence_v1(
        tmp_path, operator_attestation=operator_attestation
    )
    assert result["path"].endswith("operator_method_or_closure_selection_using_improved_evidence_v1.json")
    with pytest.raises(service.OperatorMethodOrClosureSelectionImprovedEvidenceError):
        service.write_operator_method_or_closure_selection_using_improved_evidence_v1(
            tmp_path, operator_attestation=operator_attestation
        )


def test_markdown_includes_required_sections(selection: dict) -> None:
    markdown = service.build_operator_method_or_closure_selection_using_improved_evidence_markdown_v1(selection)
    required = [
        "Title", "Operator Method or Closure Selection Using Improved Evidence",
        "Operator Attestation", "Source Closure", "Bound Evidence", "Dataset and Universe",
        "Selection Decision", "Selection Basis", "Evidence Summary", "Selection Options Review",
        "Selected Option", "Next Artifact", "Per-Ticker Selection", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required)
