from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_service as service,
)


@pytest.fixture
def summary() -> dict:
    return service.build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1()


def test_final_summary_builds_offline_without_invoking_archive_builder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.archive_service,
        "build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1",
        lambda **_: pytest.fail("source archive builder must not run"),
    )
    result = service.build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_final_summary"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("final_summary_status", service.MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("final_summary_decision", service.CURRENT_EXPECTANCY_LAB_EVIDENCE_PREDICTIVE_USEFULNESS_PATH_FINALIZED_NOT_ACCEPTED),
        ("final_summary_scope", service.PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_ONLY_NOT_REOPENING_NOT_ACCEPTANCE_NOT_RUNTIME),
        ("source_archive_record_digest", service.EXPECTED_SOURCE_ARCHIVE_RECORD_DIGEST),
        ("source_operator_selection_digest", service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST),
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
def test_identity_decision_and_digest_bindings(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


def test_complete_upstream_digest_chain_is_bound(summary: dict) -> None:
    assert len(summary["source_evidence"]) == 57
    assert summary["source_evidence"]["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


def test_dataset_universe_order_and_meta_are_preserved(summary: dict) -> None:
    assert summary["target_universe"] == service.TARGET_UNIVERSE
    assert summary["target_universe_count"] == 12
    assert summary["total_canonical_record_count"] == 11946
    assert summary["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert summary["meta_record_count"] == 913
    assert summary["non_meta_record_count"] == 1003
    assert summary["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("selected_operator_option", "OPTION_A_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"),
        ("selected_operator_decision", "SELECT_ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY"),
        ("archive_record_created", True),
        ("predictive_usefulness_acceptance_path_archived", True),
        ("current_expectancy_lab_evidence_path_archived_not_ready", True),
        ("final_archive_summary_created", True),
        ("predictive_usefulness_chain_finalized", True),
        ("current_expectancy_lab_evidence_path_finalized_archived_not_ready", True),
        ("no_immediate_next_action_required_for_current_archived_path", True),
        ("future_reopening_requires_new_operator_method_selection", True),
        ("future_reopening_created", False),
        ("method_improvement_candidate_created", False),
        ("new_evidence_candidate_created", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_accepted", False),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("profitability", "not accepted"),
        ("profitability_accepted", False),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("model_training_authorized", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("new_strategy_scoring_performed", False),
    ],
)
def test_final_summary_and_authority_boundaries(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


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
        ("final_summary_classification", "COMPLETED_RESEARCH_ONLY"),
        ("current_evidence_path_status", "FINALIZED_ARCHIVED_NOT_READY"),
        ("final_decision", "PREDICTIVE_USEFULNESS_NOT_ACCEPTED_FOR_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH"),
    ],
)
def test_final_summary_basis_and_classification(
    summary: dict, field: str, expected: object
) -> None:
    assert summary[field] == expected


def test_completed_phases_are_ordered_research_only_and_non_authorizing(summary: dict) -> None:
    phases = summary["completed_phases"]
    assert [row["phase_id"] for row in phases] == service.COMPLETED_PHASE_IDS
    assert [row["phase_number"] for row in phases] == list(range(1, 14))
    assert all(row["phase_status"] == "COMPLETED_OR_BOUND_SOURCE_EVIDENCE" for row in phases)
    assert all(row["research_only"] is True for row in phases)
    assert all(row["acceptance_authority_created"] is False for row in phases)
    assert all(row["runtime_authority_created"] is False for row in phases)


def test_archived_option_statuses_are_final(summary: dict) -> None:
    options = summary["archived_options_summary"]
    assert options[service.archive_service.selection_service.SELECTED_OPERATOR_OPTION]["status_after_final_summary"] == "FINALIZED_ARCHIVED_SELECTED_PATH"
    assert all(row["status_after_final_summary"] == "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED" for row in list(options.values())[1:6])
    assert options["OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED"]["status_after_final_summary"] == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
    assert options["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_final_summary"] == "NOT_ALLOWED_CURRENTLY"


def test_future_reopening_creates_no_inherited_authority(summary: dict) -> None:
    conditions = summary["future_reopening_conditions"]
    assert conditions["future_reopening_allowed"] is True
    assert conditions["future_reopening_requires_new_operator_method_selection"] is True
    assert conditions["future_reopening_requires_new_candidate_review_approval_chain"] is True
    assert conditions["future_reopening_requires_new_evidence_if_execution_selected"] is True
    assert conditions["future_reopening_requires_new_reassessment_and_readiness"] is True
    assert conditions["future_reopening_does_not_inherit_acceptance_authority"] is True
    assert conditions["future_reopening_does_not_inherit_profitability_authority"] is True
    assert conditions["future_reopening_does_not_inherit_runtime_authority"] is True


def test_per_ticker_final_summary_entries_are_complete(summary: dict) -> None:
    entries = summary["per_ticker_final_summary_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(entry["final_summary_status"] == "FINALIZED_ARCHIVED_NOT_READY" for entry in entries)
    assert all(entry["predictive_usefulness_accepted"] is False for entry in entries)
    assert all(len(entry["per_ticker_final_archive_summary_digest"]) == 64 for entry in entries)


def test_meta_limitation_and_per_ticker_counts_are_preserved(summary: dict) -> None:
    for entry in summary["per_ticker_final_summary_entries"]:
        if entry["ticker"] == "META":
            assert entry["historical_record_count"] == 913
            assert entry["backtest_lab_row_count"] == 13695
            assert entry["evaluable_target_row_count"] == 13520
            assert entry["meta_reduced_record_count_flag"] is True
            assert entry["final_summary_note"] == "PRESERVE_META_LIMITATION_IN_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE"
        else:
            assert entry["historical_record_count"] == 1003
            assert entry["backtest_lab_row_count"] == 15045
            assert entry["evaluable_target_row_count"] == 14870
            assert entry["meta_reduced_record_count_flag"] is False
        assert entry["unavailable_target_row_count"] == 175


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_final_summary",
        "market_data_acquisition_performed_in_final_summary",
        "canonical_dataset_regenerated_in_final_summary",
        "metric_recomputation_from_raw_rows_performed",
        "archive_record_rerun_performed",
        "operator_selection_rerun_performed",
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
def test_no_provider_data_metric_or_source_rerun_occurred(
    summary: dict, field: str
) -> None:
    assert summary[field] is False


def test_next_chain_gates_and_risk_controls_are_exact(summary: dict) -> None:
    assert summary["next_chain"] == service.NEXT_CHAIN
    assert summary["next_gates"] == service.NEXT_GATES
    assert summary["risk_controls"] == service.RISK_CONTROLS
    assert len(summary["risk_controls"]) == 40
    assert summary["next_recommended_task"] == "NONE_FOR_CURRENT_ARCHIVED_PATH"


def test_checklist_passes(summary: dict) -> None:
    checklist_summary = summary["final_summary_checklist_summary"]
    assert checklist_summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 84
    assert checklist_summary["passed_checks"] == 84
    assert checklist_summary["failed_checks"] == 0
    assert checklist_summary["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in summary["final_summary_checklist"])


def test_final_summary_and_per_ticker_digests_are_deterministic(summary: dict) -> None:
    rebuilt = service.build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1()
    assert rebuilt["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"] == summary["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"]
    assert [row["per_ticker_final_archive_summary_digest"] for row in rebuilt["per_ticker_final_summary_entries"]] == [row["per_ticker_final_archive_summary_digest"] for row in summary["per_ticker_final_summary_entries"]]


def test_validator_accepts_valid_final_summary(summary: dict) -> None:
    result = service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(summary)
    assert result["status"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("final_summary_status", "WRONG"),
        ("final_summary_decision", "WRONG"),
        ("final_summary_scope", "WRONG"),
        ("source_archive_record_digest", "0" * 64),
        ("source_operator_selection_digest", "0" * 64),
        ("source_closure_digest", "0" * 64),
        ("source_acceptance_readiness_digest", "0" * 64),
        ("source_reassessment_digest", "0" * 64),
        ("source_results_review_digest", "0" * 64),
        ("source_backtest_rows_digest", "0" * 64),
        ("source_metric_report_digest", "0" * 64),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("final_archive_summary_created", False),
        ("predictive_usefulness_chain_finalized", False),
        ("current_expectancy_lab_evidence_path_finalized_archived_not_ready", False),
        ("no_immediate_next_action_required_for_current_archived_path", False),
        ("future_reopening_requires_new_operator_method_selection", False),
        ("future_reopening_created", True),
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
        ("provider_requests_made_in_final_summary", True),
        ("market_data_acquisition_performed_in_final_summary", True),
        ("canonical_dataset_regenerated_in_final_summary", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("archive_record_rerun_performed", True),
        ("operator_selection_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    summary: dict, field: str, value: object
) -> None:
    mutated = deepcopy(summary)
    mutated[field] = value
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_target_universe_mismatch(summary: dict) -> None:
    mutated = deepcopy(summary)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize("field", ["completed_phases", "archived_options_summary", "risk_controls"])
def test_validator_rejects_missing_terminal_structure(summary: dict, field: str) -> None:
    mutated = deepcopy(summary)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_completed_phase_count_not_13(summary: dict) -> None:
    mutated = deepcopy(summary)
    mutated["completed_phases"].pop()
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_option_h_allowed(summary: dict) -> None:
    mutated = deepcopy(summary)
    mutated["archived_options_summary"]["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_final_summary"] = "ALLOWED"
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_final_or_per_ticker_digest(summary: dict) -> None:
    missing_final = deepcopy(summary)
    missing_final.pop("marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest")
    missing_ticker = deepcopy(summary)
    missing_ticker["per_ticker_final_summary_entries"][0].pop("per_ticker_final_archive_summary_digest")
    for mutated in (missing_final, missing_ticker):
        with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
            service.validate_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(mutated)


def test_markdown_includes_required_sections(summary: dict) -> None:
    markdown = service.build_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_markdown_v1(summary)
    for heading in (
        "Title", "MarketFlow Predictive-Usefulness Final Archive Summary Using Expectancy Lab Evidence v1",
        "Source Archive Record", "Bound Evidence", "Dataset and Universe", "Final Summary Scope",
        "Final Summary Basis", "Final Classification", "Completed Phases", "Archived Options Summary",
        "Per-Ticker Final Summary", "META Limitation", "Future Reopening Conditions",
        "No Immediate Next Action", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(tmp_path)
    path = tmp_path / "marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"] == result["marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_digest"]
    with pytest.raises(service.MarketFlowPredictiveUsefulnessFinalArchiveSummaryExpectancyLabEvidenceError):
        service.write_marketflow_predictive_usefulness_final_archive_summary_expectancy_lab_evidence_v1(tmp_path)
