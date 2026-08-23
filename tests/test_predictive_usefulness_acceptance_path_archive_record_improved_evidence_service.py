from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import predictive_usefulness_acceptance_path_archive_record_improved_evidence_service as service


@pytest.fixture
def archive() -> dict:
    return service.build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1()


def test_archive_record_builds_offline(archive: dict) -> None:
    assert archive["created_offline"] is True
    assert archive["provider_requests_made_in_archive"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE,
        ),
        (
            "archive_status",
            service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_CURRENT_IMPROVED_EVIDENCE,
        ),
        (
            "archive_decision",
            service.ARCHIVE_CURRENT_IMPROVED_EVIDENCE_ACCEPTANCE_PATH_NOT_READY,
        ),
        ("archive_reason", service.ARCHIVE_REASON),
        ("archive_scope", service.ARCHIVE_RECORD_ONLY),
        ("source_operator_selection_digest", service.EXPECTED_SELECTION_DIGEST),
        ("source_closure_digest", service.EXPECTED_CLOSURE_DIGEST),
        ("source_readiness_digest", service.EXPECTED_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_REASSESSMENT_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_archive_identity_and_digest_bindings(
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


def test_universe_count_order_and_meta_are_preserved(archive: dict) -> None:
    assert archive["target_universe_count"] == 12
    assert archive["target_universe"] == service.TARGET_UNIVERSE
    assert archive["meta_record_count"] == 913
    assert archive["non_meta_record_count"] == 1003


def test_source_selected_option_and_decision_are_preserved(archive: dict) -> None:
    assert archive["source_selected_option"] == service.selection.SELECTED_OPTION
    assert archive["source_selected_decision"] == service.selection.SELECTED_DECISION


@pytest.mark.parametrize(
    "field",
    [
        "predictive_usefulness_acceptance_path_archive_record_created",
        "predictive_usefulness_acceptance_path_archived_for_current_improved_evidence",
        "current_improved_evidence_acceptance_path_final_disposition_recorded",
        "future_reopen_requires_new_operator_method_selection",
    ],
)
def test_archive_terminal_state_flags_are_true(archive: dict, field: str) -> None:
    assert archive[field] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("method_improvement_candidate_created", False),
        ("future_evidence_candidate_created", False),
        ("future_evidence_execution_created", False),
        ("future_reassessment_created", False),
        ("future_readiness_review_created", False),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("predictive_usefulness_acceptance_ceremony_allowed", False),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("label_regeneration_authorized", False),
        ("label_regeneration_performed", False),
        ("new_targets_created", False),
        ("target_definition_change_authorized", False),
        ("feature_generation_authorized", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("metric_recomputation_performed_in_archive", False),
        ("model_training_performed_in_archive", False),
        ("additional_predictive_evidence_execution_rerun_performed", False),
        ("predictive_usefulness_reassessment_rerun_performed", False),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", False),
    ],
)
def test_archive_authority_and_activity_boundaries(
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


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
        ("leakage_control_count", 8),
    ],
)
def test_evidence_values_are_preserved(
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


def test_local_model_equivalence_is_preserved(archive: dict) -> None:
    assert archive["local_model_accuracy"] == archive["majority_accuracy"] == "0.58626033"


def test_meta_limitation_is_preserved(archive: dict) -> None:
    assert archive["meta_reduced_record_count_preserved"] is True
    meta = next(row for row in archive["per_ticker_archive_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["archive_note"] == (
        "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE"
    )


def test_archived_options_are_present(archive: dict) -> None:
    assert archive["archived_options"] == service.ARCHIVED_OPTIONS
    assert len(archive["archived_options"]) == 8


def test_option_a_is_archived_selected_path(archive: dict) -> None:
    option = archive["archived_options"][service.selection.SELECTED_OPTION]
    assert option["source_status"] == "RECOMMENDED_CURRENT_DECISION"
    assert option["selection_status"] == "SELECTED_BY_OPERATOR"
    assert option["archive_status"] == "ARCHIVED_SELECTED_PATH"


def test_option_h_acceptance_candidate_is_prohibited(archive: dict) -> None:
    option = archive["archived_options"]["OPTION_H_ACCEPTANCE_CANDIDATE"]
    assert option["source_status"] == "NOT_ALLOWED_CURRENTLY"
    assert option["selection_status"] == "NOT_ALLOWED_CURRENTLY"
    assert option["archive_status"] == "PROHIBITED_CURRENT_EVIDENCE_NOT_READY"


def test_per_ticker_entries_and_digests_are_complete(archive: dict) -> None:
    entries = archive["per_ticker_archive_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_archive_record_digest"]) == 64 for entry in entries)


def test_next_chain_gates_and_risk_controls_are_defined(archive: dict) -> None:
    assert archive["next_chain"] == service.NEXT_CHAIN
    assert archive["next_gates"] == service.NEXT_GATES
    assert archive["risk_controls"] == service.RISK_CONTROLS
    assert len(archive["next_chain"]) == 7
    assert len(archive["next_gates"]) == 9
    assert len(archive["risk_controls"]) == 29


def test_checklist_passes(archive: dict) -> None:
    summary = archive["archive_summary"]
    assert summary["total_checks"] == 74
    assert summary["passed_checks"] == 74
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_archive_digest_is_deterministic(archive: dict) -> None:
    rebuilt = service.build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1()
    assert rebuilt[
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"
    ] == archive[
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"
    ]


def test_per_ticker_digests_are_deterministic(archive: dict) -> None:
    rebuilt = service.build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1()
    assert [row["per_ticker_archive_record_digest"] for row in rebuilt["per_ticker_archive_entries"]] == [
        row["per_ticker_archive_record_digest"] for row in archive["per_ticker_archive_entries"]
    ]


def test_validator_accepts_valid_archive(archive: dict) -> None:
    validation = service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
        archive
    )
    assert validation["status"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE_VALID"
    )
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("archive_status", "WRONG"),
        ("archive_decision", "WRONG"),
        ("archive_reason", "WRONG"),
        ("archive_scope", "WRONG"),
        ("source_operator_selection_digest", "0" * 64),
        ("source_closure_digest", "0" * 64),
        ("source_readiness_digest", "0" * 64),
        ("source_selected_option", "WRONG"),
        ("source_selected_decision", "WRONG"),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("predictive_usefulness_acceptance_path_archive_record_created", False),
        ("predictive_usefulness_acceptance_path_archived_for_current_improved_evidence", False),
        ("current_improved_evidence_acceptance_path_final_disposition_recorded", False),
        ("future_reopen_requires_new_operator_method_selection", False),
        ("method_improvement_candidate_created", True),
        ("future_evidence_candidate_created", True),
        ("future_evidence_execution_created", True),
        ("future_reassessment_created", True),
        ("future_readiness_review_created", True),
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
        ("metric_recomputation_performed_in_archive", True),
        ("model_training_performed_in_archive", True),
        ("provider_requests_made_in_archive", True),
        ("market_data_acquisition_performed_in_archive", True),
        ("canonical_dataset_regenerated_in_archive", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_archive_values(
    archive: dict, field: str, value: object
) -> None:
    invalid = deepcopy(archive)
    invalid[field] = value
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            invalid
        )


@pytest.mark.parametrize("field", ["archived_options", "risk_controls"])
def test_validator_rejects_missing_required_collection(
    archive: dict, field: str
) -> None:
    invalid = deepcopy(archive)
    invalid.pop(field)
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_option_h_not_prohibited(archive: dict) -> None:
    invalid = deepcopy(archive)
    invalid["archived_options"]["OPTION_H_ACCEPTANCE_CANDIDATE"]["archive_status"] = "ALLOWED"
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_archive_digest(archive: dict) -> None:
    invalid = deepcopy(archive)
    invalid.pop(
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"
    )
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(archive: dict) -> None:
    invalid = deepcopy(archive)
    invalid["per_ticker_archive_entries"][0].pop("per_ticker_archive_record_digest")
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.validate_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            invalid
        )


def test_writer_uses_isolated_output_and_refuses_overwrite(
    tmp_path,
) -> None:
    result = service.write_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
        tmp_path
    )
    assert result["path"].endswith(
        "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1.json"
    )
    with pytest.raises(
        service.PredictiveUsefulnessAcceptancePathArchiveRecordImprovedEvidenceError
    ):
        service.write_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_v1(
            tmp_path
        )


def test_markdown_includes_required_sections(archive: dict) -> None:
    markdown = service.build_predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_markdown_v1(
        archive
    )
    required = [
        "Title",
        "Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence",
        "Source Operator Selection",
        "Source Closure",
        "Bound Evidence",
        "Dataset and Universe",
        "Archive Decision",
        "Archive Basis",
        "Evidence Summary",
        "Archived Options",
        "Per-Ticker Archive",
        "Future Reopen Conditions",
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
