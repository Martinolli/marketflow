from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_service as service,
)


def build_attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-28T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_ATTESTATION_PHRASE,
        "operator_confirms_source_closure_digest": service.EXPECTED_SOURCE_CLOSURE_DIGEST,
        "operator_confirms_acceptance_readiness_digest": service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "operator_confirms_reassessment_digest": service.EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "operator_confirms_results_review_digest": service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_backtest_rows_digest": service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "operator_confirms_metric_report_digest": service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "operator_confirms_records_digest": service.EXPECTED_SOURCE_RECORDS_DIGEST,
        "operator_confirms_target_universe": service.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": service.SELECTED_OPERATOR_OPTION,
        **{field: True for field in service.ATTESTATION_BOOLEAN_FIELDS},
    }
    values.update(overrides)
    return service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_attestation_v1(**values)


@pytest.fixture
def attestation() -> dict:
    return build_attestation()


@pytest.fixture
def selection(attestation: dict) -> dict:
    return service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_exact_required_fields(attestation: dict) -> None:
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_operator_option"] == service.SELECTED_OPERATOR_OPTION
    assert attestation["selected_operator_decision"] == service.SELECTED_OPERATOR_DECISION
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_selection_builds_offline_without_invoking_source_builder(
    monkeypatch: pytest.MonkeyPatch, attestation: dict
) -> None:
    monkeypatch.setattr(
        service.closure_service,
        "build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1",
        lambda **_: pytest.fail("source closure builder must not run"),
    )
    selection = service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
        operator_attestation=attestation
    )
    assert selection["created_offline"] is True
    assert selection["provider_requests_made_in_selection"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE),
        ("selection_status", service.MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTED_USING_EXPECTANCY_LAB_EVIDENCE),
        ("selection_scope", service.OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY_NOT_ARCHIVE_NOT_ACCEPTANCE_NOT_RUNTIME),
        ("selected_operator_option", service.SELECTED_OPERATOR_OPTION),
        ("selected_operator_decision", service.SELECTED_OPERATOR_DECISION),
        ("source_closure_digest", service.EXPECTED_SOURCE_CLOSURE_DIGEST),
        ("source_acceptance_readiness_digest", service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_SOURCE_REASSESSMENT_DIGEST),
        ("source_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_backtest_rows_digest", service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST),
        ("source_metric_report_digest", service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST),
        ("source_vpa_wyckoff_rule_values_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST),
        ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
        ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ],
)
def test_identity_selection_and_digest_bindings(
    selection: dict, field: str, expected: object
) -> None:
    assert selection[field] == expected


def test_complete_upstream_digest_chain_is_bound(selection: dict) -> None:
    assert len(selection["source_evidence"]) == 57
    assert selection["source_evidence"]["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


def test_dataset_universe_order_and_meta_are_preserved(selection: dict) -> None:
    assert selection["target_universe_count"] == 12
    assert selection["target_universe"] == service.TARGET_UNIVERSE
    assert selection["total_canonical_record_count"] == 11946
    assert selection["meta_record_count"] == 913
    assert selection["non_meta_record_count"] == 1003
    assert selection["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("operator_method_or_closure_selection_created", True),
        ("operator_method_or_closure_selection_completed", True),
        ("ready_for_predictive_usefulness_acceptance_path_archive_record", True),
        ("archive_record_created", False),
        ("method_improvement_candidate_created", False),
        ("new_evidence_candidate_created", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_accepted", False),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("profitability", "not accepted"),
        ("profitability_accepted", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("model_training_authorized", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
    ],
)
def test_selection_and_authority_boundaries(
    selection: dict, field: str, expected: object
) -> None:
    assert selection[field] == expected


def test_attestation_is_bound_to_operator_decision_phrase_and_scope(selection: dict) -> None:
    attestation = selection["operator_attestation"]
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_ATTESTATION_PHRASE
    assert attestation["operator_confirms_selection_scope_only"] is True


def test_option_a_is_selected_for_archive_but_archive_is_not_created(selection: dict) -> None:
    option = selection["selection_options"][service.SELECTED_OPERATOR_OPTION]
    assert option["option_status_before_selection"] == "RECOMMENDED_FOR_OPERATOR_SELECTION_NOT_SELECTED"
    assert option["option_status_after_selection"] == "SELECTED_FOR_ARCHIVE_RECORD_NOT_CREATED"
    assert option["selected_by_operator"] is True
    assert option["selected_for_archive_record"] is True
    assert option["archive_record_created"] is False


def test_unselected_option_statuses_are_preserved(selection: dict) -> None:
    options = selection["selection_options"]
    assert all(row["status_after_selection"] == "AVAILABLE_FOR_FUTURE_OPERATOR_SELECTION_NOT_SELECTED" and row["selected_by_operator"] is False for row in list(options.values())[1:6])
    assert options["OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED"]["status_after_selection"] == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
    assert options["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_selection"] == "NOT_ALLOWED_CURRENTLY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_matrix_row_count", 179190),
        ("expectancy_backtest_lab_row_count", 179190),
        ("evaluable_target_row_count", 177090),
        ("unavailable_target_row_count", 2100),
        ("embargoed_cross_split_forward_horizon_row_count", 4200),
        ("aggregate_metric_eligible_row_count", 172890),
        ("metric_materiality_readiness", "NOT_READY"),
        ("baseline_outperformance_readiness", "NOT_READY"),
        ("per_ticker_stability_readiness", "REQUIRES_OPERATOR_REVIEW"),
        ("meta_readiness", "PASS_WITH_OPERATOR_AWARENESS"),
    ],
)
def test_selection_basis_and_counts_are_preserved(
    selection: dict, field: str, expected: object
) -> None:
    assert selection[field] == expected


def test_per_ticker_selection_entries_are_complete(selection: dict) -> None:
    entries = selection["per_ticker_selection_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_operator_method_or_closure_selection_digest"]) == 64 for entry in entries)
    assert all(entry["selected_operator_option"] == service.SELECTED_OPERATOR_OPTION for entry in entries)


def test_meta_limitation_and_per_ticker_counts_are_preserved(selection: dict) -> None:
    for entry in selection["per_ticker_selection_entries"]:
        if entry["ticker"] == "META":
            assert entry["historical_record_count"] == 913
            assert entry["backtest_lab_row_count"] == 13695
            assert entry["evaluable_target_row_count"] == 13520
            assert entry["meta_reduced_record_count_flag"] is True
            assert entry["selection_note"] == "PRESERVE_META_LIMITATION_IN_OPERATOR_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE"
        else:
            assert entry["historical_record_count"] == 1003
            assert entry["backtest_lab_row_count"] == 15045
            assert entry["evaluable_target_row_count"] == 14870
            assert entry["meta_reduced_record_count_flag"] is False
        assert entry["unavailable_target_row_count"] == 175


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_selection",
        "market_data_acquisition_performed_in_selection",
        "canonical_dataset_regenerated_in_selection",
        "metric_recomputation_from_raw_rows_performed",
        "closure_rerun_performed",
        "acceptance_readiness_review_rerun_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "expectancy_backtest_lab_execution_rerun_performed",
        "expectancy_backtest_lab_results_review_rerun_performed",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed",
        "target_generation_rerun_performed",
    ],
)
def test_no_execution_or_source_rerun_occurred(selection: dict, field: str) -> None:
    assert selection[field] is False


def test_next_chain_gates_and_risk_controls_are_exact(selection: dict) -> None:
    assert selection["next_chain"] == service.NEXT_CHAIN
    assert selection["next_gates"] == service.NEXT_GATES
    assert selection["risk_controls"] == service.RISK_CONTROLS
    assert len(selection["risk_controls"]) == 38


def test_checklist_passes(selection: dict) -> None:
    summary = selection["selection_summary"]
    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in selection["selection_checklist"])


def test_selection_and_per_ticker_digests_are_deterministic(
    selection: dict, attestation: dict
) -> None:
    rebuilt = service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
        operator_attestation=attestation
    )
    assert rebuilt["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"] == selection["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"]
    assert [row["per_ticker_operator_method_or_closure_selection_digest"] for row in rebuilt["per_ticker_selection_entries"]] == [row["per_ticker_operator_method_or_closure_selection_digest"] for row in selection["per_ticker_selection_entries"]]


def test_validator_accepts_valid_selection(selection: dict) -> None:
    result = service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(selection)
    assert result["status"] == service.MARKETFLOW_OPERATOR_METHOD_OR_CLOSURE_SELECTION_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("selection_status", "WRONG"),
        ("selection_scope", "WRONG"),
        ("selected_operator_option", "WRONG"),
        ("selected_operator_decision", "WRONG"),
        ("source_closure_digest", "0" * 64),
        ("source_acceptance_readiness_digest", "0" * 64),
        ("source_reassessment_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64),
        ("source_backtest_rows_digest", "0" * 64),
        ("source_metric_report_digest", "0" * 64),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("operator_method_or_closure_selection_created", False),
        ("operator_method_or_closure_selection_completed", False),
        ("ready_for_predictive_usefulness_acceptance_path_archive_record", False),
        ("archive_record_created", True),
        ("method_improvement_candidate_created", True),
        ("new_evidence_candidate_created", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("predictive_usefulness_accepted", True),
        ("profitability_accepted", True),
        ("runtime_migration_approved", True),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("provider_requests_made_in_selection", True),
        ("market_data_acquisition_performed_in_selection", True),
        ("canonical_dataset_regenerated_in_selection", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("closure_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    selection: dict, field: str, value: object
) -> None:
    mutated = deepcopy(selection)
    mutated[field] = value
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_source_closure_digest", "0" * 64),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_selected_option", "WRONG"),
        ("operator_confirms_runtime_not_authorized", False),
    ],
)
def test_builder_rejects_invalid_attestation(field: str, value: object) -> None:
    attestation = build_attestation(**{field: value})
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
            operator_attestation=attestation
        )


def test_builder_rejects_missing_attestation_confirmation(attestation: dict) -> None:
    attestation.pop("operator_confirms_no_broker_execution")
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
            operator_attestation=attestation
        )


def test_validator_rejects_target_universe_mismatch(selection: dict) -> None:
    mutated = deepcopy(selection)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize("field", ["selection_options", "risk_controls"])
def test_validator_rejects_missing_options_or_controls(selection: dict, field: str) -> None:
    mutated = deepcopy(selection)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_option_h_allowed(selection: dict) -> None:
    mutated = deepcopy(selection)
    mutated["selection_options"]["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_selection"] = "ALLOWED"
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_selection_or_per_ticker_digest(selection: dict) -> None:
    missing_selection = deepcopy(selection)
    missing_selection.pop("marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest")
    missing_ticker = deepcopy(selection)
    missing_ticker["per_ticker_selection_entries"][0].pop("per_ticker_operator_method_or_closure_selection_digest")
    for mutated in (missing_selection, missing_ticker):
        with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
            service.validate_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(mutated)


def test_markdown_includes_required_sections(selection: dict) -> None:
    markdown = service.build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_markdown_v1(selection)
    for heading in (
        "Operator Attestation", "Source Closure", "Bound Evidence", "Dataset and Universe",
        "Selection Scope", "Selected Option", "Selection Basis", "Unselected Options",
        "Per-Ticker Selection", "META Limitation", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json(tmp_path, attestation: dict) -> None:
    result = service.write_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
        tmp_path, operator_attestation=attestation
    )
    payload = json.loads((tmp_path / "marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1.json").read_text(encoding="utf-8"))
    assert payload["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"] == result["marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_digest"]
    with pytest.raises(service.MarketFlowOperatorMethodOrClosureSelectionExpectancyLabEvidenceError):
        service.write_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1(
            tmp_path, operator_attestation=attestation
        )
