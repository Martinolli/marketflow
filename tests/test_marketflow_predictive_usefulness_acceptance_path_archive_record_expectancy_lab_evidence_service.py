from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_service as service,
)


@pytest.fixture
def archive() -> dict:
    return service.build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1()


def test_archive_builds_offline_without_invoking_selection_builder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.selection_service,
        "build_marketflow_operator_method_or_closure_selection_expectancy_lab_evidence_v1",
        lambda **_: pytest.fail("source selection builder must not run"),
    )
    archive = service.build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1()
    assert archive["created_offline"] is True
    assert archive["provider_requests_made_in_archive"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE),
        ("archive_status", service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("archive_decision", service.ARCHIVE_CURRENT_EXPECTANCY_LAB_EVIDENCE_PATH_AS_NOT_READY),
        ("archive_scope", service.PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME),
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
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


def test_complete_upstream_digest_chain_is_bound(archive: dict) -> None:
    assert len(archive["source_evidence"]) == 57
    assert archive["source_evidence"]["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


def test_dataset_universe_order_and_meta_are_preserved(archive: dict) -> None:
    assert archive["target_universe_count"] == 12
    assert archive["target_universe"] == service.TARGET_UNIVERSE
    assert archive["total_canonical_record_count"] == 11946
    assert archive["meta_record_count"] == 913
    assert archive["non_meta_record_count"] == 1003
    assert archive["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("selected_operator_option", service.selection_service.SELECTED_OPERATOR_OPTION),
        ("selected_operator_decision", service.selection_service.SELECTED_OPERATOR_DECISION),
        ("operator_method_or_closure_selection_created", True),
        ("operator_method_or_closure_selection_completed", True),
        ("archive_record_created", True),
        ("predictive_usefulness_acceptance_path_archived", True),
        ("current_expectancy_lab_evidence_path_archived_not_ready", True),
        ("ready_for_marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence", True),
        ("final_archive_summary_created", False),
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
def test_archive_and_authority_boundaries(
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


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
def test_archive_basis_and_counts_are_preserved(
    archive: dict, field: str, expected: object
) -> None:
    assert archive[field] == expected


def test_archive_classification_and_reopening_requirement(archive: dict) -> None:
    assert archive["archive_classification"] == "COMPLETED_RESEARCH_ONLY"
    assert archive["current_acceptance_path_status"] == "ARCHIVED_NOT_READY"
    assert archive["archive_record_status"] == "ARCHIVED_SELECTED_PATH"
    assert archive["future_reopening_requirement"] == "NEW_OPERATOR_METHOD_SELECTION_REQUIRED"
    assert archive["immediate_next_required_action"] == "NONE_FOR_CURRENT_ARCHIVED_PATH"
    assert archive["next_artifact_created"] is False


def test_archived_option_statuses_are_preserved(archive: dict) -> None:
    options = archive["archived_options"]
    assert options[service.selection_service.SELECTED_OPERATOR_OPTION]["status_after_archive"] == "ARCHIVED_SELECTED_PATH"
    assert all(row["status_after_archive"] == "AVAILABLE_ONLY_IF_FUTURE_REOPENING_SELECTION_CREATED" for row in list(options.values())[1:6])
    assert options["OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED"]["status_after_archive"] == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
    assert options["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_archive"] == "NOT_ALLOWED_CURRENTLY"


def test_per_ticker_archive_entries_are_complete(archive: dict) -> None:
    entries = archive["per_ticker_archive_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_acceptance_path_archive_record_digest"]) == 64 for entry in entries)
    assert all(entry["archive_status"] == "ARCHIVED_NOT_READY" for entry in entries)


def test_meta_limitation_and_per_ticker_counts_are_preserved(archive: dict) -> None:
    for entry in archive["per_ticker_archive_entries"]:
        if entry["ticker"] == "META":
            assert entry["historical_record_count"] == 913
            assert entry["backtest_lab_row_count"] == 13695
            assert entry["evaluable_target_row_count"] == 13520
            assert entry["meta_reduced_record_count_flag"] is True
            assert entry["archive_note"] == "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_EXPECTANCY_LAB_EVIDENCE"
        else:
            assert entry["historical_record_count"] == 1003
            assert entry["backtest_lab_row_count"] == 15045
            assert entry["evaluable_target_row_count"] == 14870
            assert entry["meta_reduced_record_count_flag"] is False
        assert entry["unavailable_target_row_count"] == 175


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_archive",
        "market_data_acquisition_performed_in_archive",
        "canonical_dataset_regenerated_in_archive",
        "metric_recomputation_from_raw_rows_performed",
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
def test_no_execution_or_source_rerun_occurred(archive: dict, field: str) -> None:
    assert archive[field] is False


def test_next_chain_gates_and_risk_controls_are_exact(archive: dict) -> None:
    assert archive["next_chain"] == service.NEXT_CHAIN
    assert archive["next_gates"] == service.NEXT_GATES
    assert archive["risk_controls"] == service.RISK_CONTROLS
    assert len(archive["risk_controls"]) == 39


def test_checklist_passes(archive: dict) -> None:
    summary = archive["archive_summary"]
    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in archive["archive_checklist"])


def test_archive_and_per_ticker_digests_are_deterministic(archive: dict) -> None:
    rebuilt = service.build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1()
    assert rebuilt["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"] == archive["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"]
    assert [row["per_ticker_acceptance_path_archive_record_digest"] for row in rebuilt["per_ticker_archive_entries"]] == [row["per_ticker_acceptance_path_archive_record_digest"] for row in archive["per_ticker_archive_entries"]]


def test_validator_accepts_valid_archive(archive: dict) -> None:
    result = service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(archive)
    assert result["status"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("archive_status", "WRONG"),
        ("archive_decision", "WRONG"),
        ("archive_scope", "WRONG"),
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
        ("archive_record_created", False),
        ("predictive_usefulness_acceptance_path_archived", False),
        ("current_expectancy_lab_evidence_path_archived_not_ready", False),
        ("ready_for_marketflow_predictive_usefulness_final_archive_summary_using_expectancy_lab_evidence", False),
        ("final_archive_summary_created", True),
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
        ("provider_requests_made_in_archive", True),
        ("market_data_acquisition_performed_in_archive", True),
        ("canonical_dataset_regenerated_in_archive", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("operator_selection_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    archive: dict, field: str, value: object
) -> None:
    mutated = deepcopy(archive)
    mutated[field] = value
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_target_universe_mismatch(archive: dict) -> None:
    mutated = deepcopy(archive)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize("field", ["archived_options", "risk_controls"])
def test_validator_rejects_missing_options_or_controls(archive: dict, field: str) -> None:
    mutated = deepcopy(archive)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_option_a_not_archived(archive: dict) -> None:
    mutated = deepcopy(archive)
    mutated["archived_options"][service.selection_service.SELECTED_OPERATOR_OPTION]["status_after_archive"] = "NOT_ARCHIVED"
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_option_h_allowed(archive: dict) -> None:
    mutated = deepcopy(archive)
    mutated["archived_options"]["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["status_after_archive"] = "ALLOWED"
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_archive_or_per_ticker_digest(archive: dict) -> None:
    missing_archive = deepcopy(archive)
    missing_archive.pop("marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest")
    missing_ticker = deepcopy(archive)
    missing_ticker["per_ticker_archive_entries"][0].pop("per_ticker_acceptance_path_archive_record_digest")
    for mutated in (missing_archive, missing_ticker):
        with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
            service.validate_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(mutated)


def test_markdown_includes_required_sections(archive: dict) -> None:
    markdown = service.build_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_markdown_v1(archive)
    for heading in (
        "Source Operator Selection", "Bound Evidence", "Dataset and Universe", "Archive Scope",
        "Archive Basis", "Archive Classification", "Archived Options", "Per-Ticker Archive",
        "META Limitation", "Future Reopening Conditions", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json(tmp_path) -> None:
    result = service.write_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1.json").read_text(encoding="utf-8"))
    assert payload["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"] == result["marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_digest"]
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptancePathArchiveRecordExpectancyLabEvidenceError):
        service.write_marketflow_predictive_usefulness_acceptance_path_archive_record_expectancy_lab_evidence_v1(tmp_path)
