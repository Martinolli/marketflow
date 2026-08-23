from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import marketflow_predictive_usefulness_final_archive_summary_improved_evidence_service as service


@pytest.fixture
def summary() -> dict:
    return service.build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1()


def test_final_archive_summary_builds_offline(summary: dict) -> None:
    assert summary["created_offline"] is True
    assert summary["provider_requests_made_in_final_summary"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE,
        ),
        (
            "summary_status",
            service.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY,
        ),
        (
            "final_decision",
            service.CURRENT_IMPROVED_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED,
        ),
        ("final_reason", service.FINAL_REASON),
        ("summary_scope", service.FINAL_ARCHIVE_SUMMARY_ONLY),
        ("source_archive_digest", service.EXPECTED_ARCHIVE_DIGEST),
        ("source_selection_digest", service.EXPECTED_SELECTION_DIGEST),
        ("source_closure_digest", service.EXPECTED_CLOSURE_DIGEST),
        ("source_readiness_digest", service.EXPECTED_READINESS_DIGEST),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_final_summary_identity_and_digest_bindings(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


def test_universe_count_order_and_meta_are_preserved(summary: dict) -> None:
    assert summary["target_universe_count"] == 12
    assert summary["target_universe"] == service.TARGET_UNIVERSE
    assert summary["meta_record_count"] == 913
    assert summary["non_meta_record_count"] == 1003


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_predictive_usefulness_final_archive_summary_created",
        "current_improved_evidence_predictive_usefulness_chain_finalized",
        "current_improved_evidence_predictive_usefulness_chain_archived_not_ready",
        "future_research_requires_new_method_concept",
    ],
)
def test_final_terminal_state_flags_are_true(summary: dict, field: str) -> None:
    assert summary[field] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
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
        ("metric_recomputation_performed_in_final_summary", False),
        ("model_training_performed_in_final_summary", False),
        ("additional_predictive_evidence_execution_rerun_performed", False),
        ("predictive_usefulness_reassessment_rerun_performed", False),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", False),
    ],
)
def test_final_summary_authority_and_activity_boundaries(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


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
def test_final_evidence_values_are_preserved(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


def test_local_model_equivalence_is_preserved(summary: dict) -> None:
    assert summary["local_model_accuracy"] == summary["majority_accuracy"] == "0.58626033"


def test_final_outcome_classification_is_complete(summary: dict) -> None:
    outcome = summary["final_outcome_classification"]
    assert outcome["final_chain_status"] == "ARCHIVED_NOT_READY"
    assert outcome["final_predictive_usefulness_decision"] == "NOT_ACCEPTED"
    assert outcome["final_acceptance_readiness_decision"] == "NOT_READY"
    assert outcome["final_runtime_decision"] == "NOT_AUTHORIZED"
    assert outcome["final_profitability_decision"] == "NOT_ACCEPTED"
    assert outcome["final_reason"] == service.FINAL_OUTCOME_REASON


def test_meta_limitation_is_preserved(summary: dict) -> None:
    assert summary["meta_reduced_record_count_preserved"] is True
    meta = next(row for row in summary["per_ticker_final_summary_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["final_summary_note"] == (
        "PRESERVE_META_LIMITATION_IN_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE"
    )


def test_final_phase_summary_is_complete_and_ordered(summary: dict) -> None:
    assert summary["final_phase_summary"] == service.FINAL_PHASE_SUMMARY
    assert len(summary["final_phase_summary"]) == 17


def test_future_reopen_conditions_and_possible_methods_are_present(
    summary: dict,
) -> None:
    assert summary["future_reopen_conditions"] == service.FUTURE_REOPEN_CONDITIONS
    assert all(summary["future_reopen_conditions"].values())
    assert summary["possible_future_methods_only_if_reopened"] == (
        service.POSSIBLE_FUTURE_METHODS_IF_REOPENED
    )


def test_per_ticker_entries_and_digests_are_complete(summary: dict) -> None:
    entries = summary["per_ticker_final_summary_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_final_archive_summary_digest"]) == 64 for entry in entries)


def test_next_chain_is_terminal_and_gates_and_risks_are_defined(summary: dict) -> None:
    assert summary["next_chain"] == service.NEXT_CHAIN
    assert summary["next_chain"][0] == (
        "No immediate next task required for the archived current path."
    )
    assert summary["next_gates"] == service.NEXT_GATES
    assert summary["risk_controls"] == service.RISK_CONTROLS
    assert len(summary["next_chain"]) == 6
    assert len(summary["next_gates"]) == 9
    assert len(summary["risk_controls"]) == 29


def test_checklist_passes(summary: dict) -> None:
    totals = summary["final_summary_summary"]
    assert totals["total_checks"] == 64
    assert totals["passed_checks"] == 64
    assert totals["failed_checks"] == 0
    assert totals["blocker_count"] == 0


def test_summary_digest_is_deterministic(summary: dict) -> None:
    rebuilt = service.build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1()
    assert rebuilt[
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"
    ] == summary[
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"
    ]


def test_per_ticker_digests_are_deterministic(summary: dict) -> None:
    rebuilt = service.build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1()
    assert [
        row["per_ticker_final_archive_summary_digest"]
        for row in rebuilt["per_ticker_final_summary_entries"]
    ] == [
        row["per_ticker_final_archive_summary_digest"]
        for row in summary["per_ticker_final_summary_entries"]
    ]


def test_validator_accepts_valid_summary(summary: dict) -> None:
    validation = service.validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
        summary
    )
    assert validation["status"] == (
        "MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE_VALID"
    )
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("summary_status", "WRONG"),
        ("final_decision", "WRONG"),
        ("final_reason", "WRONG"),
        ("summary_scope", "WRONG"),
        ("source_archive_digest", "0" * 64),
        ("source_selection_digest", "0" * 64),
        ("source_readiness_digest", "0" * 64),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("marketflow_predictive_usefulness_final_archive_summary_created", False),
        ("current_improved_evidence_predictive_usefulness_chain_finalized", False),
        ("current_improved_evidence_predictive_usefulness_chain_archived_not_ready", False),
        ("future_research_requires_new_method_concept", False),
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
        ("metric_recomputation_performed_in_final_summary", True),
        ("model_training_performed_in_final_summary", True),
        ("provider_requests_made_in_final_summary", True),
        ("market_data_acquisition_performed_in_final_summary", True),
        ("canonical_dataset_regenerated_in_final_summary", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
        ("predictive_usefulness_acceptance_readiness_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_summary_values(
    summary: dict, field: str, value: object
) -> None:
    invalid = deepcopy(summary)
    invalid[field] = value
    with pytest.raises(
        service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError
    ):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field", ["final_phase_summary", "future_reopen_conditions", "risk_controls"]
)
def test_validator_rejects_missing_required_collection(
    summary: dict, field: str
) -> None:
    invalid = deepcopy(summary)
    invalid.pop(field)
    with pytest.raises(
        service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError
    ):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_final_summary_digest(summary: dict) -> None:
    invalid = deepcopy(summary)
    invalid.pop(
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"
    )
    with pytest.raises(
        service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError
    ):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(summary: dict) -> None:
    invalid = deepcopy(summary)
    invalid["per_ticker_final_summary_entries"][0].pop(
        "per_ticker_final_archive_summary_digest"
    )
    with pytest.raises(
        service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError
    ):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
            invalid
        )


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
        tmp_path
    )
    assert result["path"].endswith(
        "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1.json"
    )
    with pytest.raises(
        service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryImprovedEvidenceError
    ):
        service.write_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_v1(
            tmp_path
        )


def test_markdown_includes_required_sections(summary: dict) -> None:
    markdown = service.build_marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_markdown_v1(
        summary
    )
    required = [
        "Title",
        "MarketFlow Predictive Usefulness Final Archive Summary Using Improved Evidence",
        "Source Archive Record",
        "Bound Evidence",
        "Dataset and Universe",
        "Final Decision",
        "Final Evidence Summary",
        "Final Outcome Classification",
        "Completed Phase Summary",
        "Per-Ticker Final Summary",
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
