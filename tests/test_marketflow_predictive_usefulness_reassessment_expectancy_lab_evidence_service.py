from __future__ import annotations

from copy import deepcopy
import json

import pytest

import marketflow.services as services
from marketflow.services import (
    marketflow_predictive_usefulness_reassessment_expectancy_lab_evidence_service as service,
)


@pytest.fixture(scope="module")
def reassessment() -> dict:
    return service.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1()


def test_reassessment_builds_offline_without_source_review_rerun(monkeypatch):
    monkeypatch.setattr(
        service.results_review,
        "build_marketflow_expectancy_backtest_lab_results_review_v1",
        lambda **_: pytest.fail("results review must not be rerun"),
    )
    package = service.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1()
    assert package["created_offline"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_V1),
        ("reassessment_status", service.MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_PACKAGE_READY),
        ("reassessment_scope", service.PREDICTIVE_USEFULNESS_REASSESSMENT_ONLY_NOT_ACCEPTANCE_NOT_RUNTIME),
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
        ("selected_backtest_lab_package", service.execution.SELECTED_BACKTEST_LAB_PACKAGE),
        ("selected_vpa_wyckoff_package", service.execution.SELECTED_VPA_WYCKOFF_PACKAGE),
        ("selected_matrix_package", service.execution.SELECTED_MATRIX_PACKAGE),
        ("selected_matrix_layout", service.execution.SELECTED_MATRIX_LAYOUT),
        ("selected_feature_package", service.execution.SELECTED_FEATURE_PACKAGE),
        ("selected_label_target_package", service.execution.SELECTED_LABEL_TARGET_PACKAGE),
        ("selected_objective_path", service.execution.SELECTED_OBJECTIVE_PATH),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
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
        ("evidence_integrity", "PASS"),
        ("source_output_integrity", "PASS"),
        ("no_peek_and_leakage", "PASS"),
        ("chronology_and_embargo", "PASS_WITH_REVIEWED_EMBARGO_EXCLUSIONS"),
        ("reassessment_classification", "COMPLETED_RESEARCH_ONLY"),
        ("recommendation", "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE"),
    ],
)
def test_required_field_values(reassessment, field, expected):
    assert reassessment[field] == expected


def test_universe_order_and_records_are_preserved(reassessment):
    assert reassessment["target_universe"] == service.TARGET_UNIVERSE
    assert reassessment["total_canonical_record_count"] == 11946
    assert reassessment["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST


@pytest.mark.parametrize(
    "field",
    [
        "expectancy_backtest_lab_results_review_created",
        "expectancy_backtest_lab_results_review_ready",
        "predictive_usefulness_reassessment_created",
        "predictive_usefulness_reassessment_ready",
        "ready_for_predictive_usefulness_acceptance_readiness_review",
        "readiness_for_acceptance_readiness_review",
        "meta_reduced_record_count_preserved",
        "backtest_rows_jsonl_schema_verified",
        "metric_report_verified",
        "baseline_comparison_report_verified",
        "vpa_wyckoff_rule_alignment_report_verified",
        "abstention_quality_report_verified",
        "per_ticker_backtest_report_verified",
        "chronological_split_report_verified",
        "meta_limitation_report_verified",
        "no_peek_report_verified",
        "operator_summary_verified",
    ],
)
def test_required_true_flags(reassessment, field):
    assert reassessment[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_accepted",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_accepted",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "model_training_authorized", "model_training_performed",
        "strategy_scoring_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_reassessment",
        "live_provider_transport_enabled_in_reassessment",
        "market_data_acquisition_performed_in_reassessment",
        "dataset_generation_performed_in_reassessment",
        "canonical_dataset_regenerated_in_reassessment",
        "metric_recomputation_from_raw_rows_performed",
        "expectancy_backtest_lab_execution_rerun_performed",
        "expectancy_backtest_lab_results_review_rerun_performed",
        "expectancy_backtest_lab_approval_rerun_performed",
        "expectancy_backtest_lab_candidate_review_rerun_performed",
        "expectancy_backtest_lab_candidate_creation_rerun_performed",
        "vpa_wyckoff_rule_baseline_execution_rerun_performed",
        "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
        "feature_label_matrix_execution_rerun_performed",
        "feature_label_matrix_results_review_rerun_performed",
        "signal_feature_generation_rerun_performed", "target_generation_rerun_performed",
        "target_values_used_as_predictors", "target_classes_used_as_predictors",
        "forward_returns_used_as_features", "prediction_fields_present",
        "strategy_score_fields_present", "trade_recommendation_fields_present",
        "broker_order_fields_present", "provider_payload_fields_present", "api_key_fields_present",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    ],
)
def test_closed_and_no_action_flags(reassessment, field):
    assert reassessment[field] is False


@pytest.mark.parametrize(
    "field",
    ["runtime_use", "strategy_use", "paper_trading", "broker_execution"],
)
def test_authority_fields_are_not_authorized(reassessment, field):
    assert reassessment[field] == "NOT_AUTHORIZED"


def test_predictive_usefulness_and_profitability_are_not_accepted(reassessment):
    assert reassessment["predictive_usefulness"] == "not accepted"
    assert reassessment["profitability"] == "not accepted"


def test_reassessment_domains_are_complete_and_research_only(reassessment):
    domains = reassessment["reassessment_domains"]
    assert list(domains) == service.DOMAIN_IDS
    assert len(domains) == 18
    for domain_id, domain in domains.items():
        assert domain["domain_status"] == "REVIEWED_RESEARCH_ONLY"
        assert domain["acceptance_evidence"] is False
        assert domain["research_only"] is True
        assert domain["non_actionable"] is True
        if domain_id in service.BOUNDARY_DOMAINS:
            assert domain["requires_acceptance_readiness_review"] is False
            assert domain["authority_boundary_closed"] is True


def test_per_ticker_entries_and_digests_are_complete(reassessment):
    entries = reassessment["per_ticker_reassessment_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    assert sum(row["backtest_lab_row_count"] for row in entries) == 179190
    assert sum(row["evaluable_target_row_count"] for row in entries) == 177090
    assert sum(row["unavailable_target_row_count"] for row in entries) == 2100
    assert sum(row["aggregate_metric_eligible_row_count"] for row in entries) == 172890
    for row in entries:
        assert row["per_ticker_predictive_usefulness_reassessment_digest"] == (
            service.per_ticker_predictive_usefulness_reassessment_digest_v1(row)
        )


def test_meta_limitation_is_preserved(reassessment):
    meta = next(row for row in reassessment["per_ticker_reassessment_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["backtest_lab_row_count"] == 13695
    assert meta["evaluable_target_row_count"] == 13520
    assert meta["unavailable_target_row_count"] == 175
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["reassessment_note"] == "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE"


def test_non_meta_counts_are_preserved(reassessment):
    for row in reassessment["per_ticker_reassessment_entries"]:
        if row["ticker"] != "META":
            assert row["historical_record_count"] == 1003
            assert row["backtest_lab_row_count"] == 15045
            assert row["evaluable_target_row_count"] == 14870
            assert row["unavailable_target_row_count"] == 175
            assert row["meta_reduced_record_count_flag"] is False


def test_next_chain_gates_and_risk_controls_are_exact(reassessment):
    assert reassessment["next_chain"] == service.NEXT_CHAIN
    assert reassessment["next_gates"] == service.NEXT_GATES
    assert reassessment["risk_controls"] == service.RISK_CONTROLS


def test_checklist_passes(reassessment):
    assert [row["check_id"] for row in reassessment["reassessment_checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in reassessment["reassessment_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in reassessment["reassessment_checklist"])
    assert reassessment["reassessment_summary"]["total_checks"] == 84
    assert reassessment["reassessment_summary"]["passed_checks"] == 84
    assert reassessment["reassessment_summary"]["failed_checks"] == 0
    assert reassessment["reassessment_summary"]["blocker_count"] == 0


def test_reassessment_and_per_ticker_digests_are_deterministic(reassessment):
    second = service.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1()
    assert second == reassessment
    assert second["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"] == reassessment["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"]


def test_validator_accepts_valid_reassessment(reassessment):
    result = service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(reassessment)
    assert result["status"] == service.MARKETFLOW_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_EXPECTANCY_LAB_EVIDENCE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("reassessment_status", "WRONG"),
        ("reassessment_scope", "WRONG"),
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
        ("predictive_usefulness_reassessment_created", False),
        ("predictive_usefulness_reassessment_ready", False),
        ("ready_for_predictive_usefulness_acceptance_readiness_review", False),
        ("predictive_usefulness_acceptance_readiness_review_created", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_accepted", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("profitability", "accepted"), ("profitability_accepted", True),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True), ("model_training_authorized", True),
        ("model_training_performed", True), ("strategy_scoring_performed", True),
        ("provider_requests_made_in_reassessment", True),
        ("market_data_acquisition_performed_in_reassessment", True),
        ("canonical_dataset_regenerated_in_reassessment", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("expectancy_backtest_lab_execution_rerun_performed", True),
        ("expectancy_backtest_lab_results_review_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_top_level_fields(reassessment, field, bad_value):
    mutated = deepcopy(reassessment)
    mutated[field] = bad_value
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_wrong_universe(reassessment):
    mutated = deepcopy(reassessment)
    mutated["target_universe"] = list(reversed(mutated["target_universe"]))
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_domains(reassessment):
    mutated = deepcopy(reassessment)
    mutated["reassessment_domains"].pop(service.DOMAIN_IDS[0])
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_risk_controls(reassessment):
    mutated = deepcopy(reassessment)
    mutated["risk_controls"] = []
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_reassessment_digest(reassessment):
    mutated = deepcopy(reassessment)
    mutated.pop("marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest")
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


def test_validator_rejects_missing_per_ticker_digest(reassessment):
    mutated = deepcopy(reassessment)
    mutated["per_ticker_reassessment_entries"][0].pop("per_ticker_predictive_usefulness_reassessment_digest")
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(mutated)


@pytest.mark.parametrize(
    "section",
    [
        "Title", "Predictive-Usefulness Reassessment Using Expectancy Lab Evidence v1",
        "Source Expectancy Backtest Lab Results Review", "Bound Evidence",
        "Dataset and Universe", "Reassessment Scope", "Evidence Basis",
        "Metric Evidence Summary", "Baseline Comparison Summary",
        "VPA/Wyckoff Alignment Summary", "Abstention Quality Summary",
        "Chronology and Embargo", "No-Peek and Leakage", "Per-Ticker Reassessment",
        "META Limitation", "Reassessment Classification", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Next Chain", "Next Gates",
        "Risk Controls", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(reassessment, section):
    markdown = service.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_markdown_v1(reassessment)
    assert section in markdown


def test_writer_creates_canonical_json(tmp_path, reassessment):
    result = service.write_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1.json").read_text(encoding="utf-8"))
    assert payload == reassessment
    assert result["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"] == reassessment["marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_digest"]
    with pytest.raises(service.MarketFlowPredictiveUsefulnessReassessmentExpectancyLabEvidenceError):
        service.write_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1(tmp_path)


def test_public_exports_are_available():
    assert services.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1 is service.build_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1
    assert services.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1 is service.validate_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1
    assert services.write_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1 is service.write_marketflow_predictive_usefulness_reassessment_using_expectancy_lab_evidence_v1
