from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_service as service,
)


@pytest.fixture
def closure() -> dict:
    return service.build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1()


def test_closure_builds_offline_without_invoking_readiness_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        service.readiness,
        "build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1",
        lambda **_: pytest.fail("source readiness builder must not run"),
    )
    closure = service.build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1()
    assert closure["created_offline"] is True
    assert closure["provider_requests_made_in_closure"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_EXPECTANCY_LAB_EVIDENCE),
        ("closure_status", service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("closure_decision", service.CLOSE_CURRENT_EXPECTANCY_LAB_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_OR_ARCHIVE_SELECTION),
        ("closure_scope", service.PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME),
        ("source_acceptance_readiness_digest", service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_SOURCE_REASSESSMENT_DIGEST),
        ("source_expectancy_backtest_lab_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_expectancy_backtest_rows_digest", service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST),
        ("source_expectancy_metric_report_digest", service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST),
        ("source_vpa_wyckoff_rule_values_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST),
        ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
        ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ],
)
def test_identity_and_digest_bindings(closure: dict, field: str, expected: object) -> None:
    assert closure[field] == expected


def test_complete_upstream_digest_chain_is_bound(closure: dict) -> None:
    assert len(closure["source_evidence"]) == 57
    assert closure["source_evidence"]["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


def test_dataset_universe_order_and_meta_are_preserved(closure: dict) -> None:
    assert closure["target_universe_count"] == 12
    assert closure["target_universe"] == service.TARGET_UNIVERSE
    assert closure["total_canonical_record_count"] == 11946
    assert closure["meta_record_count"] == 913
    assert closure["non_meta_record_count"] == 1003
    assert closure["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("selected_backtest_lab_package", "PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB"),
        ("selected_vpa_wyckoff_package", "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"),
        ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
        ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
        ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
        ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
        ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ],
)
def test_selected_packages_are_preserved(closure: dict, field: str, expected: str) -> None:
    assert closure[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("readiness_decision", service.readiness.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("predictive_usefulness_not_ready_closure_created", True),
        ("predictive_usefulness_acceptance_path_closed_not_ready", True),
        ("method_planning_tree_created", True),
        ("operator_method_or_closure_selection_required", True),
        ("ready_for_operator_method_or_closure_selection", True),
        ("operator_method_or_closure_selection_created", False),
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
def test_closure_and_authority_boundaries(closure: dict, field: str, expected: object) -> None:
    assert closure[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_matrix_row_count", 179190),
        ("expectancy_backtest_lab_row_count", 179190),
        ("evaluable_target_row_count", 177090),
        ("unavailable_target_row_count", 2100),
        ("embargoed_cross_split_forward_horizon_row_count", 4200),
        ("aggregate_metric_eligible_row_count", 172890),
        ("approved_metric_family_count", 13),
        ("blocked_metric_family_count", 1),
        ("approved_baseline_count", 6),
        ("blocked_baseline_count", 1),
        ("metric_materiality_readiness", "NOT_READY"),
        ("baseline_outperformance_readiness", "NOT_READY"),
        ("per_ticker_stability_readiness", "REQUIRES_OPERATOR_REVIEW"),
        ("meta_readiness", "PASS_WITH_OPERATOR_AWARENESS"),
    ],
)
def test_closure_basis_is_preserved(closure: dict, field: str, expected: object) -> None:
    assert closure[field] == expected


def test_closure_classification_and_recommendation(closure: dict) -> None:
    assert closure["closure_classification"] == "COMPLETED_RESEARCH_ONLY"
    assert closure["current_acceptance_path_status"] == "CLOSED_NOT_READY"
    assert closure["recommended_current_decision"] == service.RECOMMENDED_CURRENT_DECISION
    assert closure["next_artifact_ready"] == service.NEXT_ARTIFACT
    assert closure["next_artifact_created"] is False


def test_method_tree_has_eight_unselected_options(closure: dict) -> None:
    options = closure["method_planning_tree_options"]
    assert list(options) == list(service.METHOD_PLANNING_TREE)
    assert len(options) == 8
    assert all(option["selection_created"] is False for option in options.values())
    assert all(option["approval_created"] is False for option in options.values())
    assert all(option["execution_created"] is False for option in options.values())
    assert all(option["acceptance_candidate_created"] is False for option in options.values())
    assert all(option["runtime_authority_created"] is False for option in options.values())


def test_method_tree_statuses(closure: dict) -> None:
    options = closure["method_planning_tree_options"]
    assert options[service.RECOMMENDED_CURRENT_DECISION]["option_status"] == "RECOMMENDED_FOR_OPERATOR_SELECTION_NOT_SELECTED"
    assert all(row["option_status"] == "AVAILABLE_FOR_OPERATOR_SELECTION_NOT_SELECTED" for row in list(options.values())[1:6])
    assert options["OPTION_G_PROFITABILITY_AND_RUNTIME_CHAIN_BLOCKED_UNTIL_USEFULNESS_ACCEPTED"]["option_status"] == "BLOCKED_NOT_SELECTABLE_FOR_CURRENT_STAGE"
    assert options["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["option_status"] == "NOT_ALLOWED_CURRENTLY"


def test_per_ticker_closure_entries_are_complete(closure: dict) -> None:
    entries = closure["per_ticker_closure_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert all(len(entry["per_ticker_not_ready_closure_digest"]) == 64 for entry in entries)
    assert all(entry["recommended_option"] == service.RECOMMENDED_CURRENT_DECISION for entry in entries)


def test_meta_limitation_and_per_ticker_counts_are_preserved(closure: dict) -> None:
    for entry in closure["per_ticker_closure_entries"]:
        if entry["ticker"] == "META":
            assert entry["historical_record_count"] == 913
            assert entry["backtest_lab_row_count"] == 13695
            assert entry["evaluable_target_row_count"] == 13520
            assert entry["meta_reduced_record_count_flag"] is True
            assert entry["closure_note"] == "PRESERVE_META_LIMITATION_IN_NOT_READY_CLOSURE_USING_EXPECTANCY_LAB_EVIDENCE"
        else:
            assert entry["historical_record_count"] == 1003
            assert entry["backtest_lab_row_count"] == 15045
            assert entry["evaluable_target_row_count"] == 14870
            assert entry["meta_reduced_record_count_flag"] is False
        assert entry["unavailable_target_row_count"] == 175


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_closure",
        "market_data_acquisition_performed_in_closure",
        "canonical_dataset_regenerated_in_closure",
        "metric_recomputation_from_raw_rows_performed",
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
def test_no_execution_or_source_rerun_occurred(closure: dict, field: str) -> None:
    assert closure[field] is False


def test_next_chain_gates_and_risk_controls_are_exact(closure: dict) -> None:
    assert closure["next_chain"] == service.NEXT_CHAIN
    assert closure["next_gates"] == service.NEXT_GATES
    assert closure["risk_controls"] == service.RISK_CONTROLS
    assert len(closure["risk_controls"]) == 37


def test_checklist_passes(closure: dict) -> None:
    assert closure["closure_summary"]["total_checks"] == 73
    assert closure["closure_summary"]["passed_checks"] == 73
    assert closure["closure_summary"]["failed_checks"] == 0
    assert closure["closure_summary"]["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in closure["closure_checklist"])


def test_closure_and_per_ticker_digests_are_deterministic(closure: dict) -> None:
    rebuilt = service.build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1()
    assert rebuilt["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"] == closure["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"]
    assert [row["per_ticker_not_ready_closure_digest"] for row in rebuilt["per_ticker_closure_entries"]] == [row["per_ticker_not_ready_closure_digest"] for row in closure["per_ticker_closure_entries"]]


def test_validator_accepts_valid_closure(closure: dict) -> None:
    result = service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(closure)
    assert result["status"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_METHOD_TREE_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("closure_status", "WRONG"),
        ("closure_decision", "WRONG"),
        ("closure_scope", "WRONG"),
        ("source_acceptance_readiness_digest", "0" * 64),
        ("source_reassessment_digest", "0" * 64),
        ("source_expectancy_backtest_lab_results_review_digest", "0" * 64),
        ("source_expectancy_backtest_rows_digest", "0" * 64),
        ("source_expectancy_metric_report_digest", "0" * 64),
        ("selected_backtest_lab_package", "WRONG"),
        ("selected_vpa_wyckoff_package", "WRONG"),
        ("selected_matrix_package", "WRONG"),
        ("selected_matrix_layout", "WRONG"),
        ("selected_feature_package", "WRONG"),
        ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("predictive_usefulness_not_ready_closure_created", False),
        ("predictive_usefulness_acceptance_path_closed_not_ready", False),
        ("method_planning_tree_created", False),
        ("operator_method_or_closure_selection_required", False),
        ("operator_method_or_closure_selection_created", True),
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
        ("provider_requests_made_in_closure", True),
        ("market_data_acquisition_performed_in_closure", True),
        ("canonical_dataset_regenerated_in_closure", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("acceptance_readiness_review_rerun_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_values(closure: dict, field: str, value: object) -> None:
    mutated = deepcopy(closure)
    mutated[field] = value
    with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_target_universe_mismatch(closure: dict) -> None:
    mutated = deepcopy(closure)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize("field", ["method_planning_tree_options", "risk_controls"])
def test_validator_rejects_missing_tree_or_controls(closure: dict, field: str) -> None:
    mutated = deepcopy(closure)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_option_h_allowed(closure: dict) -> None:
    mutated = deepcopy(closure)
    mutated["method_planning_tree_options"]["OPTION_H_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"]["option_status"] = "ALLOWED"
    with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_closure_or_per_ticker_digest(closure: dict) -> None:
    missing_closure = deepcopy(closure)
    missing_closure.pop("marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest")
    missing_ticker = deepcopy(closure)
    missing_ticker["per_ticker_closure_entries"][0].pop("per_ticker_not_ready_closure_digest")
    for mutated in (missing_closure, missing_ticker):
        with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
            service.validate_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(mutated)


def test_markdown_includes_required_sections(closure: dict) -> None:
    markdown = service.build_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_markdown_v1(closure)
    for heading in (
        "Source Acceptance Readiness Review", "Bound Evidence", "Dataset and Universe",
        "Closure Scope", "Closure Basis", "Closure Classification", "Method Planning Tree",
        "Recommended Current Decision", "Per-Ticker Closure", "META Limitation", "Next Chain",
        "Next Gates", "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json(tmp_path) -> None:
    result = service.write_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1.json").read_text(encoding="utf-8"))
    assert payload["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"] == result["marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_digest"]
    with pytest.raises(service.MarketFlowPredictiveUsefulnessNotReadyClosureMethodTreeExpectancyLabEvidenceError):
        service.write_marketflow_predictive_usefulness_not_ready_closure_method_tree_expectancy_lab_evidence_v1(tmp_path)
