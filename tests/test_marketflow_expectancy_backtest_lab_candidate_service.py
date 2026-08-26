from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import marketflow_expectancy_backtest_lab_candidate_service as service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_marketflow_expectancy_backtest_lab_candidate_v1()


def test_candidate_builds_fully_offline(candidate: dict) -> None:
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False
    assert candidate["market_data_acquisition_performed_in_candidate"] is False
    source = inspect.getsource(service.build_marketflow_expectancy_backtest_lab_candidate_v1)
    assert ".marketflow" not in source
    assert "source_review.build_" not in source


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1"),
    ("schema_version", "marketflow_expectancy_backtest_lab_candidate_v1"),
    ("candidate_status", "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW"),
    ("candidate_scope", "EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"),
    ("created_offline", True),
    ("research_only", True),
    ("operator_review_required", True),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("meta_reduced_record_count_preserved", True),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_candidate_core_contract(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


SOURCE_DIGEST_FIELDS = [
    ("source_vpa_wyckoff_rule_baseline_results_review_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST),
    ("source_vpa_wyckoff_rule_baseline_execution_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST),
    ("source_vpa_wyckoff_rule_baseline_output_binding_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST),
    ("source_vpa_wyckoff_rule_values_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST),
    ("source_vpa_wyckoff_rule_baseline_approval_digest", service.EXPECTED_SOURCE_VPA_WYCKOFF_APPROVAL_DIGEST),
    ("source_feature_label_matrix_results_review_digest", service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST),
    ("source_feature_label_matrix_execution_digest", service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST),
    ("source_feature_label_matrix_output_binding_digest", service.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST),
    ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
    ("source_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
    ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
]


@pytest.mark.parametrize(("field", "expected"), SOURCE_DIGEST_FIELDS)
def test_source_digest_chain_is_bound(candidate: dict, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_source_review_contract_is_preserved(candidate: dict) -> None:
    assert candidate["source_vpa_wyckoff_rule_baseline_results_review_artifact_kind"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE"
    assert candidate["source_vpa_wyckoff_rule_baseline_results_review_status"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY"
    assert candidate["source_vpa_wyckoff_rule_baseline_results_review_scope"] == "VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"
    assert candidate["vpa_wyckoff_rule_baseline_results_review_created"] is True
    assert candidate["vpa_wyckoff_rule_baseline_results_review_ready"] is True


def test_universe_order_is_preserved(candidate: dict) -> None:
    assert candidate["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


PACKAGE_FIELDS = [
    ("selected_vpa_wyckoff_package", "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
]


@pytest.mark.parametrize(("field", "expected"), PACKAGE_FIELDS)
def test_selected_source_packages_are_preserved(candidate: dict, field: str, expected: str) -> None:
    assert candidate[field] == expected


BASIS_COUNTS = [
    ("matrix_row_count", 179190),
    ("available_matrix_row_count", 177090),
    ("unavailable_target_matrix_row_count", 2100),
    ("feature_group_count_per_matrix_row", 13),
    ("feature_group_reference_count", 2329470),
    ("feature_source_row_count", 155298),
    ("target_source_row_count", 179190),
    ("rule_value_row_count", 179190),
    ("state_value_row_count", 179190),
    ("selected_rule_family_count", 8),
    ("selected_state_family_count", 6),
    ("rule_family_reference_count", 1433520),
    ("state_family_reference_count", 1075140),
    ("target_profile_count", 15),
    ("target_unavailable_row_count", 2100),
]


@pytest.mark.parametrize(("field", "expected"), BASIS_COUNTS)
def test_candidate_basis_counts(candidate: dict, field: str, expected: int) -> None:
    assert candidate[field] == expected


@pytest.mark.parametrize("field", [
    "candidate_philosophy",
    "candidate_primary_question",
    "candidate_secondary_question",
    "candidate_boundary",
])
def test_candidate_philosophy_and_questions_are_defined(candidate: dict, field: str) -> None:
    assert candidate[field]


def test_recommended_and_supporting_packages_are_candidate_only(candidate: dict) -> None:
    packages = candidate["backtest_lab_packages"]
    assert len(packages) == 4
    assert packages[0]["package_id"] == service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB
    assert packages[0]["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert candidate["recommended_backtest_lab_package"] == packages[0]["package_id"]
    assert [row["package_id"] for row in packages[1:]] == [
        service.PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
        service.PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
        service.PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
    ]
    assert all(
        row["selection_created"] is False
        and row["approval_created"] is False
        and row["execution_created"] is False
        for row in packages
    )


def test_ten_backtest_objectives_are_defined_not_executed(candidate: dict) -> None:
    rows = candidate["proposed_backtest_objectives"]
    assert [row["objective_id"] for row in rows] == service.BACKTEST_OBJECTIVE_IDS
    assert len(rows) == 10
    assert all(
        row["objective_status"] == "CANDIDATE_OBJECTIVE_NOT_EXECUTED"
        and row["metric_computation_authorized"] is False
        and row["backtest_execution_authorized"] is False
        and row["model_training_authorized"] is False
        for row in rows
    )


def test_seven_baselines_are_defined_not_executed(candidate: dict) -> None:
    rows = candidate["candidate_baselines"]
    assert [row["baseline_id"] for row in rows] == service.BASELINE_IDS
    assert len(rows) == 7
    assert all(row["baseline_status"] == "CANDIDATE_BASELINE_NOT_EXECUTED" for row in rows)
    blocked = next(
        row for row in rows
        if row["baseline_id"] == "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED"
    )
    assert blocked["allowed_for_future_execution"] is False
    assert "chronological/no-peek" in blocked["reason"]


def test_chronological_plan_is_planned_not_executed(candidate: dict) -> None:
    plan = candidate["proposed_chronological_plan"]
    assert plan == {
        "training_or_calibration_window": {
            "date_start": "2022-01-01", "date_end": "2023-12-31"
        },
        "validation_window": {
            "date_start": "2024-01-01", "date_end": "2024-12-31"
        },
        "holdout_window": {
            "date_start": "2025-01-01", "date_end": "2025-12-31"
        },
        "split_policy": "CHRONOLOGICAL_NO_SHUFFLE",
        "embargo_policy": "FUTURE_HORIZON_AWARE_EMBARGO_REQUIRED_BEFORE_EXECUTION",
        "split_execution_status": "PLANNED_NOT_EXECUTED",
    }


def test_fourteen_metric_families_are_not_computed(candidate: dict) -> None:
    rows = candidate["proposed_metric_families"]
    assert [row["metric_family_id"] for row in rows] == service.METRIC_FAMILY_IDS
    assert len(rows) == 14
    assert all(
        row["metric_status"] == "CANDIDATE_METRIC_NOT_COMPUTED"
        and row["metric_computation_authorized"] is False
        for row in rows
    )
    blocked = next(
        row for row in rows
        if row["metric_family_id"] == "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"
    )
    assert blocked["allowed_for_future_execution"] is False
    assert "chronological-dependence" in blocked["reason"]


def test_eleven_no_peek_controls_are_planned(candidate: dict) -> None:
    rows = candidate["proposed_no_peek_and_leakage_controls"]
    assert [row["control_id"] for row in rows] == service.NO_PEEK_CONTROL_IDS
    assert len(rows) == 11
    assert all(
        row["control_status"] == "PLANNED_NOT_EXECUTED"
        and row["requires_future_backtest_lab_approval"] is True
        for row in rows
    )


def test_fourteen_future_outputs_are_planned_not_generated(candidate: dict) -> None:
    rows = candidate["proposed_future_outputs"]
    assert [row["output_id"] for row in rows] == service.FUTURE_OUTPUT_IDS
    assert len(rows) == 14
    assert all(
        row["output_status"] == "PLANNED_NOT_GENERATED"
        and row["research_only"] is True
        and row["non_actionable"] is True
        for row in rows
    )


def test_planned_counts_are_exact_and_no_metric_values_exist(candidate: dict) -> None:
    assert candidate["planned_counts"] == service._planned_counts()
    assert candidate["planned_counts"]["metric_values_computed"] is False
    assert candidate["planned_counts"]["planned_backtest_execution_scope"] == "RESEARCH_ONLY_NOT_PRODUCTION_NOT_RUNTIME"


def test_per_ticker_entries_and_digests(candidate: dict) -> None:
    rows = candidate["per_ticker_expectancy_backtest_lab_candidate_entries"]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == candidate["target_universe"]
    for row in rows:
        assert row["per_ticker_expectancy_backtest_lab_candidate_digest"] == service.per_ticker_expectancy_backtest_lab_candidate_digest(row)
        assert row["expectancy_backtest_lab_executed"] is False
        assert row["expectancy_backtest_rows_created"] is False
        assert row["expectancy_backtest_results_created"] is False


def test_meta_and_non_meta_candidate_counts(candidate: dict) -> None:
    rows = {
        row["ticker"]: row
        for row in candidate["per_ticker_expectancy_backtest_lab_candidate_entries"]
    }
    meta = rows["META"]
    assert (
        meta["historical_record_count"],
        meta["planned_matrix_row_count"],
        meta["planned_evaluable_target_row_count"],
        meta["planned_unavailable_target_row_count"],
    ) == (913, 13695, 13520, 175)
    assert meta["candidate_note"] == "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_CANDIDATE"
    for ticker, row in rows.items():
        if ticker != "META":
            assert (
                row["historical_record_count"],
                row["planned_matrix_row_count"],
                row["planned_evaluable_target_row_count"],
                row["planned_unavailable_target_row_count"],
            ) == (1003, 15045, 14870, 175)


@pytest.mark.parametrize("field", [
    "ready_for_expectancy_backtest_lab_candidate",
    "expectancy_backtest_lab_candidate_created",
    "expectancy_backtest_lab_candidate_ready_for_operator_review",
    "ready_for_expectancy_backtest_lab_candidate_operator_review",
])
def test_only_candidate_readiness_is_true(candidate: dict, field: str) -> None:
    assert candidate[field] is True


@pytest.mark.parametrize("field", [
    "selection_created",
    "approval_created",
    "execution_created",
    "expectancy_backtest_lab_selected",
    "expectancy_backtest_lab_approved",
    "expectancy_backtest_lab_authorized",
    "expectancy_backtest_lab_executed",
    "expectancy_backtest_rows_created",
    "expectancy_backtest_results_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made_in_candidate",
    "live_provider_transport_enabled_in_candidate",
    "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate",
    "canonical_dataset_regenerated_in_candidate",
    "vpa_wyckoff_rule_baseline_execution_rerun_performed",
    "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "signal_feature_generation_rerun_performed",
    "target_generation_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
])
def test_all_execution_and_external_action_flags_are_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_acceptance_profitability_runtime_and_trading_are_closed(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert candidate[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_checklist_passes_completely(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["candidate_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["candidate_summary"]["failed_checks"] == 0
    assert candidate["candidate_summary"]["blocker_count"] == 0


def test_candidate_and_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    second = service.build_marketflow_expectancy_backtest_lab_candidate_v1()
    assert candidate["marketflow_expectancy_backtest_lab_candidate_v1_digest"] == second["marketflow_expectancy_backtest_lab_candidate_v1_digest"]
    assert candidate["per_ticker_expectancy_backtest_lab_candidate_entries"] == second["per_ticker_expectancy_backtest_lab_candidate_entries"]
    payload = deepcopy(candidate)
    digest = payload.pop("marketflow_expectancy_backtest_lab_candidate_v1_digest")
    assert digest == semantic_digest(payload)


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    validation = service.validate_marketflow_expectancy_backtest_lab_candidate_v1(candidate)
    assert validation["status"] == service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_VALID
    assert validation["blocker_count"] == 0


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("candidate_status", "WRONG"),
    ("candidate_scope", "WRONG"),
    ("source_vpa_wyckoff_rule_baseline_results_review_digest", "changed"),
    ("source_vpa_wyckoff_rule_baseline_execution_digest", "changed"),
    ("source_vpa_wyckoff_rule_baseline_output_binding_digest", "changed"),
    ("source_vpa_wyckoff_rule_values_digest", "changed"),
    ("source_vpa_wyckoff_rule_baseline_approval_digest", "changed"),
    ("source_feature_label_matrix_results_review_digest", "changed"),
    ("source_feature_label_matrix_rows_digest", "changed"),
    ("source_feature_values_digest", "changed"),
    ("source_target_values_digest", "changed"),
    ("records_digest", "changed"),
    ("selected_vpa_wyckoff_package", "WRONG"),
    ("selected_matrix_package", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("target_universe", ["WRONG"]),
    ("target_universe_count", 11),
    ("meta_record_count", 1003),
    ("vpa_wyckoff_rule_baseline_results_review_ready", False),
    ("ready_for_expectancy_backtest_lab_candidate", False),
    ("expectancy_backtest_lab_candidate_created", False),
    ("expectancy_backtest_lab_candidate_ready_for_operator_review", False),
    ("selection_created", True),
    ("approval_created", True),
    ("execution_created", True),
    ("expectancy_backtest_lab_selected", True),
    ("expectancy_backtest_lab_approved", True),
    ("expectancy_backtest_lab_authorized", True),
    ("expectancy_backtest_lab_executed", True),
    ("expectancy_backtest_rows_created", True),
    ("expectancy_backtest_results_created", True),
    ("backtest_execution_performed", True),
    ("model_training_performed", True),
    ("metric_computation_performed", True),
    ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"),
    ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True),
    ("provider_requests_made_in_candidate", True),
    ("market_data_acquisition_performed_in_candidate", True),
    ("canonical_dataset_regenerated_in_candidate", True),
    ("vpa_wyckoff_rule_baseline_execution_rerun_performed", True),
    ("vpa_wyckoff_rule_baseline_results_review_rerun_performed", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("feature_label_matrix_results_review_rerun_performed", True),
    ("signal_feature_generation_rerun_performed", True),
    ("target_generation_rerun_performed", True),
]


@pytest.mark.parametrize(("field", "value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_contract_mutations(
    candidate: dict, field: str, value: object
) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_v1(changed)


@pytest.mark.parametrize("field", [
    "candidate_philosophy",
    "backtest_lab_packages",
    "proposed_backtest_objectives",
    "candidate_baselines",
    "proposed_chronological_plan",
    "proposed_metric_families",
    "proposed_no_peek_and_leakage_controls",
    "proposed_future_outputs",
    "planned_counts",
    "risk_controls",
])
def test_validator_rejects_missing_candidate_sections(candidate: dict, field: str) -> None:
    changed = deepcopy(candidate)
    changed[field] = [] if isinstance(changed[field], list) else None
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_v1(changed)


def test_validator_rejects_missing_recommended_package(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["backtest_lab_packages"] = changed["backtest_lab_packages"][1:]
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed.pop("marketflow_expectancy_backtest_lab_candidate_v1_digest")
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_expectancy_backtest_lab_candidate_entries"][0].pop(
        "per_ticker_expectancy_backtest_lab_candidate_digest"
    )
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_v1(changed)


MARKDOWN_HEADINGS = [
    "Expectancy Backtest Lab Candidate v1",
    "Source VPA/Wyckoff Results Review",
    "Source Feature-Label Matrix Results Review",
    "Bound Evidence",
    "Dataset and Universe",
    "Candidate Basis",
    "Candidate Philosophy",
    "Recommended Backtest Lab Package",
    "Supporting Backtest Lab Packages",
    "Proposed Backtest Objectives",
    "Candidate Baselines",
    "Chronological Plan",
    "Metric Families",
    "No-Peek and Leakage Controls",
    "Planned Future Outputs",
    "Planned Counts",
    "Per-Ticker Candidate Summary",
    "Next Chain",
    "Next Gates",
    "Risk Controls",
    "Predictive Usefulness Boundary",
    "Profitability Boundary",
    "Runtime Boundary",
    "Checklist Summary",
    "Guardrails",
]


@pytest.mark.parametrize("heading", MARKDOWN_HEADINGS)
def test_markdown_contains_required_sections(candidate: dict, heading: str) -> None:
    markdown = service.build_marketflow_expectancy_backtest_lab_candidate_markdown_v1(
        candidate
    )
    assert heading in markdown


def test_writer_round_trips_candidate_in_isolated_directory(tmp_path: Path) -> None:
    written = service.write_marketflow_expectancy_backtest_lab_candidate_v1(
        tmp_path / "candidate"
    )
    assert Path(written["json_path"]).is_file()
    assert Path(written["markdown_path"]).is_file()
    assert json.loads(Path(written["json_path"]).read_text()) == written["candidate"]


PUBLIC_EXPORTS = [
    "ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1",
    "SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1",
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    "EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION",
    "PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB",
    "PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB",
    "PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB",
    "PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB",
    "build_marketflow_expectancy_backtest_lab_candidate_v1",
    "validate_marketflow_expectancy_backtest_lab_candidate_v1",
    "write_marketflow_expectancy_backtest_lab_candidate_v1",
    "build_marketflow_expectancy_backtest_lab_candidate_markdown_v1",
    "marketflow_expectancy_backtest_lab_candidate_v1_digest",
    "per_ticker_expectancy_backtest_lab_candidate_digest",
]


@pytest.mark.parametrize("name", PUBLIC_EXPORTS)
def test_public_exports(name: str) -> None:
    assert name in services.__all__
    assert getattr(services, name) is getattr(service, name)
