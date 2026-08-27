from __future__ import annotations

from copy import deepcopy
import json

import pytest

import marketflow.services as services
from marketflow.services import (
    marketflow_predictive_usefulness_acceptance_readiness_review_expectancy_lab_evidence_service as service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1()


def test_readiness_review_builds_offline_without_reassessment_rerun(monkeypatch):
    monkeypatch.setattr(
        service.reassessment,
        "build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1",
        lambda **_: pytest.fail("source reassessment must not be rerun"),
    )
    package = service.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1()
    assert package["created_offline"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_V1),
        ("readiness_status", service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_COMPLETED),
        ("readiness_scope", service.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME),
        ("readiness_decision", service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE),
        ("decision_reason", service.READINESS_DECISION_REASON),
        ("source_predictive_usefulness_reassessment_digest", service.EXPECTED_SOURCE_REASSESSMENT_DIGEST),
        ("source_expectancy_backtest_lab_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_expectancy_backtest_lab_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_expectancy_backtest_lab_output_binding_digest", service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST),
        ("source_expectancy_backtest_rows_digest", service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST),
        ("source_expectancy_metric_report_digest", service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST),
        ("source_expectancy_backtest_lab_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_vpa_wyckoff_rule_values_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST),
        ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
        ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("selected_backtest_lab_package", service.reassessment.execution.SELECTED_BACKTEST_LAB_PACKAGE),
        ("selected_vpa_wyckoff_package", service.reassessment.execution.SELECTED_VPA_WYCKOFF_PACKAGE),
        ("selected_matrix_package", service.reassessment.execution.SELECTED_MATRIX_PACKAGE),
        ("selected_matrix_layout", service.reassessment.execution.SELECTED_MATRIX_LAYOUT),
        ("selected_feature_package", service.reassessment.execution.SELECTED_FEATURE_PACKAGE),
        ("selected_label_target_package", service.reassessment.execution.SELECTED_LABEL_TARGET_PACKAGE),
        ("selected_objective_path", service.reassessment.execution.SELECTED_OBJECTIVE_PATH),
        ("target_universe_count", 12), ("meta_record_count", 913),
        ("source_matrix_row_count", 179190), ("expectancy_backtest_lab_row_count", 179190),
        ("evaluable_target_row_count", 177090), ("unavailable_target_row_count", 2100),
        ("embargoed_cross_split_forward_horizon_row_count", 4200),
        ("aggregate_metric_eligible_row_count", 172890),
        ("approved_metric_family_count", 13), ("blocked_metric_family_count", 1),
        ("approved_baseline_count", 6), ("blocked_baseline_count", 1),
        ("evidence_integrity", "PASS"), ("source_output_integrity", "PASS"),
        ("no_peek_and_leakage", "PASS"),
        ("chronology_and_embargo", "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS"),
        ("readiness_classification", "COMPLETED_RESEARCH_ONLY"),
        ("predictive_signal_readiness", "NOT_READY"),
        ("metric_materiality_readiness", "NOT_READY"),
        ("baseline_outperformance_readiness", "NOT_READY"),
        ("per_ticker_stability_readiness", "REQUIRES_OPERATOR_REVIEW"),
        ("source_reassessment_recommendation", "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE"),
        ("recommendation", "DO_NOT_CREATE_PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE"),
    ],
)
def test_required_field_values(review, field, expected):
    assert review[field] == expected


def test_universe_and_records_are_preserved(review):
    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["total_canonical_record_count"] == 11946
    assert review["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


@pytest.mark.parametrize(
    "field",
    [
        "predictive_usefulness_reassessment_created",
        "predictive_usefulness_reassessment_ready",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_readiness_review_completed",
        "ready_for_predictive_usefulness_not_ready_closure_or_method_selection",
        "meta_reduced_record_count_preserved",
    ],
)
def test_required_true_flags(review, field):
    assert review[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "ready_for_predictive_usefulness_acceptance_candidate",
        "predictive_usefulness_accepted", "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_accepted", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved",
        "runtime_migration_active", "automatic_stitching", "model_training_authorized",
        "model_training_performed", "strategy_scoring_performed",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "acceptance_candidate_allowed", "acceptance_candidate_recommended",
        "provider_requests_made_in_readiness_review",
        "live_provider_transport_enabled_in_readiness_review",
        "market_data_acquisition_performed_in_readiness_review",
        "dataset_generation_performed_in_readiness_review",
        "canonical_dataset_regenerated_in_readiness_review",
        "metric_recomputation_from_raw_rows_performed",
        "predictive_usefulness_reassessment_rerun_performed",
        "expectancy_backtest_lab_execution_rerun_performed",
        "expectancy_backtest_lab_results_review_rerun_performed",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed", "target_generation_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    ],
)
def test_closed_and_no_action_flags(review, field):
    assert review[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_authority_fields_are_not_authorized(review, field):
    assert review[field] == "NOT_AUTHORIZED"


def test_predictive_usefulness_and_profitability_are_not_accepted(review):
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"


@pytest.mark.parametrize(
    ("criterion_id", "finding"),
    [(criterion_id, policy[0]) for criterion_id, policy in service.CRITERIA_POLICY.items()],
)
def test_readiness_criteria_are_complete(review, criterion_id, finding):
    criterion = review["readiness_criteria"][criterion_id]
    assert criterion["criterion_id"] == criterion_id
    assert criterion["criterion_status"] == "REVIEWED_RESEARCH_ONLY"
    assert criterion["finding"] == finding
    assert criterion["research_only"] is True
    assert criterion["non_actionable"] is True
    assert criterion["reason"]


def test_readiness_findings_are_conservative(review):
    assert review["predictive_usefulness_acceptance_decision"] == "NOT_READY"
    assert review["chronology_readiness"] == "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS"
    assert review["no_peek_readiness"] == "PASS"
    assert review["meta_readiness"] == "PASS_WITH_OPERATOR_AWARENESS"
    assert review["next_recommended_action"] == "CREATE_NOT_READY_CLOSURE_OR_OPERATOR_METHOD_SELECTION_USING_EXPECTANCY_LAB_EVIDENCE"


def test_per_ticker_entries_and_digests_are_complete(review):
    entries = review["per_ticker_readiness_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    assert sum(row["backtest_lab_row_count"] for row in entries) == 179190
    assert sum(row["evaluable_target_row_count"] for row in entries) == 177090
    assert sum(row["unavailable_target_row_count"] for row in entries) == 2100
    assert sum(row["aggregate_metric_eligible_row_count"] for row in entries) == 172890
    for row in entries:
        assert row["acceptance_readiness_decision"] == "NOT_READY"
        assert row["per_ticker_acceptance_readiness_review_digest"] == (
            service.per_ticker_acceptance_readiness_review_digest_v1(row)
        )


def test_meta_limitation_is_preserved(review):
    meta = next(row for row in review["per_ticker_readiness_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["backtest_lab_row_count"] == 13695
    assert meta["evaluable_target_row_count"] == 13520
    assert meta["unavailable_target_row_count"] == 175
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["readiness_note"] == "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE"


def test_non_meta_counts_are_preserved(review):
    for row in review["per_ticker_readiness_entries"]:
        if row["ticker"] != "META":
            assert row["historical_record_count"] == 1003
            assert row["backtest_lab_row_count"] == 15045
            assert row["evaluable_target_row_count"] == 14870
            assert row["unavailable_target_row_count"] == 175
            assert row["meta_reduced_record_count_flag"] is False


def test_next_chain_gates_and_risk_controls_are_exact(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_passes(review):
    checklist = review["readiness_checklist"]
    assert [row["check_id"] for row in checklist] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in checklist)
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert review["readiness_summary"]["total_checks"] == 90
    assert review["readiness_summary"]["passed_checks"] == 90
    assert review["readiness_summary"]["failed_checks"] == 0
    assert review["readiness_summary"]["blocker_count"] == 0


def test_readiness_and_per_ticker_digests_are_deterministic(review):
    second = service.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1()
    assert second == review


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(review)
    assert result["status"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["readiness_decision"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_EXPECTANCY_LAB_EVIDENCE


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("readiness_status", "WRONG"),
        ("readiness_scope", "WRONG"), ("readiness_decision", "READY"),
        ("source_predictive_usefulness_reassessment_digest", "0" * 64),
        ("source_expectancy_backtest_lab_results_review_digest", "0" * 64),
        ("source_expectancy_backtest_lab_execution_digest", "0" * 64),
        ("source_expectancy_backtest_rows_digest", "0" * 64),
        ("source_expectancy_metric_report_digest", "0" * 64),
        ("source_expectancy_backtest_lab_approval_digest", "0" * 64),
        ("selected_backtest_lab_package", "WRONG"),
        ("selected_vpa_wyckoff_package", "WRONG"),
        ("selected_matrix_package", "WRONG"), ("selected_matrix_layout", "WRONG"),
        ("selected_feature_package", "WRONG"), ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"), ("target_universe_count", 11),
        ("records_digest", "0" * 64), ("meta_record_count", 1003),
        ("predictive_usefulness_acceptance_readiness_review_created", False),
        ("predictive_usefulness_acceptance_readiness_review_completed", False),
        ("ready_for_predictive_usefulness_acceptance_candidate", True),
        ("ready_for_predictive_usefulness_not_ready_closure_or_method_selection", False),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("predictive_usefulness", "accepted"), ("predictive_usefulness_accepted", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("profitability", "accepted"), ("profitability_accepted", True),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True), ("model_training_authorized", True),
        ("model_training_performed", True), ("strategy_scoring_performed", True),
        ("provider_requests_made_in_readiness_review", True),
        ("market_data_acquisition_performed_in_readiness_review", True),
        ("canonical_dataset_regenerated_in_readiness_review", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("predictive_usefulness_reassessment_rerun_performed", True),
        ("expectancy_backtest_lab_execution_rerun_performed", True),
        ("expectancy_backtest_lab_results_review_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_fields(review, field, bad_value):
    mutated = deepcopy(review)
    mutated[field] = bad_value
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_wrong_universe(review):
    mutated = deepcopy(review)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_readiness_criteria(review):
    mutated = deepcopy(review)
    mutated["readiness_criteria"].pop(next(iter(mutated["readiness_criteria"])))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_readiness_findings(review):
    mutated = deepcopy(review)
    mutated.pop("metric_materiality_readiness")
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_risk_controls(review):
    mutated = deepcopy(review)
    mutated["risk_controls"] = []
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_readiness_digest(review):
    mutated = deepcopy(review)
    mutated.pop("marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_digest")
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_per_ticker_digest(review):
    mutated = deepcopy(review)
    mutated["per_ticker_readiness_entries"][0].pop("per_ticker_acceptance_readiness_review_digest")
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize(
    "section",
    [
        "Title", "Predictive-Usefulness Acceptance Readiness Review Using Expectancy Lab Evidence v1",
        "Source Reassessment", "Bound Evidence", "Dataset and Universe", "Readiness Scope",
        "Readiness Basis", "Readiness Criteria", "Readiness Findings",
        "Metric Materiality Readiness", "Baseline Outperformance Readiness",
        "Per-Ticker Stability Readiness", "Chronology and Embargo", "No-Peek and Leakage",
        "META Limitation", "Readiness Decision", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Per-Ticker Readiness",
        "Next Chain", "Next Gates", "Risk Controls", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(review, section):
    markdown = service.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_markdown_v1(review)
    assert section in markdown


def test_writer_creates_canonical_json(tmp_path, review):
    result = service.write_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(tmp_path)
    path = tmp_path / "marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1.json"
    assert json.loads(path.read_text(encoding="utf-8")) == review
    assert result["readiness_decision"] == review["readiness_decision"]
    with pytest.raises(service.MarketFlowPredictiveUsefulnessAcceptanceReadinessReviewExpectancyLabEvidenceError):
        service.write_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1(tmp_path)


def test_public_exports_are_available():
    assert services.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1 is service.build_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1
    assert services.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1 is service.validate_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1
    assert services.write_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1 is service.write_marketflow_predictive_usefulness_acceptance_readiness_review_using_expectancy_lab_evidence_v1
