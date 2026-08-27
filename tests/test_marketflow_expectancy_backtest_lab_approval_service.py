from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_expectancy_backtest_lab_approval_service as service,
)


def _attestation() -> dict:
    return service.build_marketflow_expectancy_backtest_lab_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-27T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        operator_confirms_vpa_wyckoff_results_review_digest=service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
        operator_confirms_vpa_wyckoff_rule_values_digest=service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
        operator_confirms_matrix_rows_digest=service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        operator_confirms_target_values_digest=service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        operator_confirms_records_digest=service.EXPECTED_SOURCE_RECORDS_DIGEST,
        operator_confirms_target_universe=service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_backtest_lab_package=service.SELECTED_BACKTEST_LAB_PACKAGE,
        operator_confirms_selected_vpa_wyckoff_package=service.SELECTED_VPA_WYCKOFF_PACKAGE,
        operator_confirms_selected_matrix_package=service.SELECTED_MATRIX_PACKAGE,
        operator_confirms_selected_matrix_layout=service.SELECTED_MATRIX_LAYOUT,
        operator_confirms_selected_feature_package=service.SELECTED_FEATURE_PACKAGE,
        operator_confirms_selected_label_target_package=service.SELECTED_LABEL_TARGET_PACKAGE,
        operator_confirms_selected_objective_path=service.SELECTED_OBJECTIVE_PATH,
        **{
            field: True
            for field in service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    )


@pytest.fixture(scope="module")
def attestation() -> dict:
    return _attestation()


@pytest.fixture(scope="module")
def source_review() -> dict:
    return service.review_service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1()


@pytest.fixture(scope="module")
def approval(source_review: dict, attestation: dict) -> dict:
    return service.build_marketflow_expectancy_backtest_lab_approval_v1(
        source_review=source_review,
        operator_attestation=attestation,
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_EXPECTANCY_BACKTEST_LAB"
    assert attestation["operator_attestation_phrase"] == (
        service.REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        "marketflow_expectancy_backtest_lab_approval_operator_attestation_v1"
    )
    assert all(
        attestation[field] is True
        for field in service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline(approval: dict) -> None:
    assert approval["created_offline"] is True
    assert approval["provider_requests_made_in_approval"] is False
    assert approval["live_provider_transport_enabled_in_approval"] is False
    assert approval["market_data_acquisition_performed_in_approval"] is False


def test_default_source_review_builder_is_supported(attestation: dict) -> None:
    approval = service.build_marketflow_expectancy_backtest_lab_approval_v1(
        operator_attestation=attestation
    )
    assert approval["approval_status"] == service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED"),
    ("schema_version", "marketflow_expectancy_backtest_lab_approval_v1"),
    ("approval_status", "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED"),
    ("approval_scope", "EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY"),
    ("selected_backtest_lab_package", service.SELECTED_BACKTEST_LAB_PACKAGE),
    ("selected_vpa_wyckoff_package", service.SELECTED_VPA_WYCKOFF_PACKAGE),
    ("selected_matrix_package", service.SELECTED_MATRIX_PACKAGE),
    ("selected_matrix_layout", service.SELECTED_MATRIX_LAYOUT),
    ("selected_feature_package", service.SELECTED_FEATURE_PACKAGE),
    ("selected_label_target_package", service.SELECTED_LABEL_TARGET_PACKAGE),
    ("selected_objective_path", service.SELECTED_OBJECTIVE_PATH),
    (
        "source_expectancy_backtest_lab_candidate_review_artifact_kind",
        "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    ),
    (
        "source_expectancy_backtest_lab_candidate_review_status",
        "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    ),
    (
        "source_expectancy_backtest_lab_candidate_review_scope",
        "EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    ),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("matrix_row_count", 179190),
    ("available_matrix_row_count", 177090),
    ("unavailable_target_matrix_row_count", 2100),
    ("rule_value_row_count", 179190),
    ("state_value_row_count", 179190),
    ("selected_rule_family_count", 8),
    ("selected_state_family_count", 6),
    ("target_profile_count", 15),
    ("feature_group_count_per_matrix_row", 13),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(approval: dict, field: str, expected: object) -> None:
    assert approval[field] == expected


BOUND_DIGESTS = {
    "source_expectancy_backtest_lab_candidate_review_digest": service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_expectancy_backtest_lab_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_vpa_wyckoff_rule_baseline_results_review_digest": service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
    "source_vpa_wyckoff_rule_values_digest": service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
    "source_feature_label_matrix_rows_digest": service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    "source_target_values_digest": service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "source_records_digest": service.EXPECTED_SOURCE_RECORDS_DIGEST,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_source_digest_is_bound(approval: dict, field: str, expected: str) -> None:
    assert approval[field] == expected
    assert len(approval[field]) == 64


def test_complete_upstream_digest_chain_is_preserved(
    approval: dict, source_review: dict
) -> None:
    assert approval["source_evidence"] == source_review["source_evidence"]
    assert len(approval["source_evidence"]) > 40


def test_dataset_universe_and_meta_are_preserved(approval: dict) -> None:
    assert approval["target_universe"] == service.TARGET_UNIVERSE
    assert approval["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert approval["meta_reduced_record_count_preserved"] is True


TRUE_APPROVAL_FIELDS = [
    "expectancy_backtest_lab_candidate_created",
    "expectancy_backtest_lab_candidate_review_created",
    "expectancy_backtest_lab_candidate_review_ready",
    "expectancy_backtest_lab_selected",
    "expectancy_backtest_lab_approved",
    "expectancy_backtest_lab_authorized",
    "expectancy_backtest_lab_approval_created",
    "ready_for_expectancy_backtest_lab_execution",
    "expectancy_backtest_lab_authorized_for_future_execution",
    "backtest_execution_authorized_for_future_lab_execution",
    "metric_computation_authorized_for_future_lab_execution",
]


@pytest.mark.parametrize("field", TRUE_APPROVAL_FIELDS)
def test_future_lab_approval_fields_are_true(approval: dict, field: str) -> None:
    assert approval[field] is True


FALSE_BOUNDARY_FIELDS = [
    "expectancy_backtest_lab_executed",
    "expectancy_backtest_rows_created",
    "expectancy_backtest_results_created",
    "metric_values_computed",
    "metric_reports_created",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "vpa_wyckoff_rule_baseline_execution_rerun_performed",
    "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "signal_feature_generation_rerun_performed",
    "target_generation_rerun_performed",
    "expectancy_backtest_lab_candidate_creation_rerun_performed",
    "expectancy_backtest_lab_candidate_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", FALSE_BOUNDARY_FIELDS)
def test_execution_and_downstream_boundaries_remain_false(
    approval: dict, field: str
) -> None:
    assert approval[field] is False


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_acceptance_remains_not_accepted(approval: dict, field: str) -> None:
    assert approval[field] == service.NOT_ACCEPTED


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(
    approval: dict, field: str
) -> None:
    assert approval[field] == service.NOT_AUTHORIZED


ATTESTATION_EXACT_FIELDS = {
    "operator_decision": service.OPERATOR_DECISION_APPROVE_EXPECTANCY_BACKTEST_LAB,
    "operator_attestation_phrase": service.REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE,
    "operator_confirms_candidate_review_digest": service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "operator_confirms_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_vpa_wyckoff_results_review_digest": service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
    "operator_confirms_vpa_wyckoff_rule_values_digest": service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
    "operator_confirms_matrix_rows_digest": service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    "operator_confirms_target_values_digest": service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "operator_confirms_records_digest": service.EXPECTED_SOURCE_RECORDS_DIGEST,
    "operator_confirms_target_universe": service.TARGET_UNIVERSE,
    "operator_confirms_target_count": 12,
    "operator_confirms_meta_record_count": 913,
    "operator_confirms_non_meta_record_count": 1003,
    "operator_confirms_selected_backtest_lab_package": service.SELECTED_BACKTEST_LAB_PACKAGE,
    "operator_confirms_selected_vpa_wyckoff_package": service.SELECTED_VPA_WYCKOFF_PACKAGE,
    "operator_confirms_selected_matrix_package": service.SELECTED_MATRIX_PACKAGE,
    "operator_confirms_selected_matrix_layout": service.SELECTED_MATRIX_LAYOUT,
    "operator_confirms_selected_feature_package": service.SELECTED_FEATURE_PACKAGE,
    "operator_confirms_selected_label_target_package": service.SELECTED_LABEL_TARGET_PACKAGE,
    "operator_confirms_selected_objective_path": service.SELECTED_OBJECTIVE_PATH,
}


@pytest.mark.parametrize(("field", "expected"), list(ATTESTATION_EXACT_FIELDS.items()))
def test_operator_attestation_is_exact(
    approval: dict, field: str, expected: object
) -> None:
    assert approval["operator_attestation"][field] == expected


def test_approved_package_is_future_only(approval: dict) -> None:
    package = approval["approved_backtest_lab_package"]
    assert package["package_id"] == service.SELECTED_BACKTEST_LAB_PACKAGE
    assert package["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert package["planned_backtest_lab_row_count"] == 179190
    assert package["planned_metric_family_count"] == 13
    assert package["backtest_execution_performed"] is False
    assert package["metric_values_computed"] is False


@pytest.mark.parametrize(
    "package_id",
    [
        service.review_service.candidate_service.PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
        service.review_service.candidate_service.PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
        service.review_service.candidate_service.PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
    ],
)
def test_supporting_packages_are_available_not_selected(
    approval: dict, package_id: str
) -> None:
    row = next(
        item
        for item in approval["supporting_backtest_lab_packages"]
        if item["package_id"] == package_id
    )
    assert row["approval_status"] == "AVAILABLE_NOT_SELECTED"
    assert row["execution_performed"] is False


@pytest.mark.parametrize(
    "objective_id", service.review_service.candidate_service.BACKTEST_OBJECTIVE_IDS
)
def test_all_ten_objectives_are_approved_for_future_execution(
    approval: dict, objective_id: str
) -> None:
    row = next(
        item
        for item in approval["approved_backtest_objectives"]
        if item["objective_id"] == objective_id
    )
    assert row["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert row["objective_status"] == "CANDIDATE_OBJECTIVE_NOT_EXECUTED"
    assert row["execution_performed"] is False
    assert row["metric_values_computed"] is False


@pytest.mark.parametrize("baseline_id", service.APPROVED_BASELINE_IDS)
def test_six_baselines_are_approved_for_future_execution(
    approval: dict, baseline_id: str
) -> None:
    row = next(
        item
        for item in approval["approved_baselines"]
        if item["baseline_id"] == baseline_id
    )
    assert row["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert row["execution_performed"] is False
    assert row["metric_values_computed"] is False
    assert row["model_training_authorized"] is False


def test_randomized_baseline_remains_blocked(approval: dict) -> None:
    row = approval["blocked_baseline"]
    assert row["baseline_id"] == service.BLOCKED_BASELINE_ID
    assert row["approval_status"] == (
        "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL"
    )
    assert row["allowed_for_future_execution"] is False
    assert "chronological/no-peek" in row["reason"]


def test_chronological_plan_is_approved_but_not_executed(approval: dict) -> None:
    plan = approval["approved_chronological_plan"]
    assert plan["training_or_calibration_window"] == {
        "date_start": "2022-01-01",
        "date_end": "2023-12-31",
    }
    assert plan["validation_window"]["date_start"] == "2024-01-01"
    assert plan["holdout_window"]["date_end"] == "2025-12-31"
    assert plan["split_policy"] == "CHRONOLOGICAL_NO_SHUFFLE"
    assert plan["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert plan["split_execution_status"] == "PLANNED_NOT_EXECUTED"


@pytest.mark.parametrize("metric_id", service.APPROVED_METRIC_FAMILY_IDS)
def test_thirteen_metric_families_are_approved_for_future_computation(
    approval: dict, metric_id: str
) -> None:
    row = next(
        item
        for item in approval["approved_metric_families"]
        if item["metric_family_id"] == metric_id
    )
    assert row["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert row["metric_status"] == "CANDIDATE_METRIC_NOT_COMPUTED"
    assert row["metric_computation_authorized_for_future_lab_execution"] is True
    assert row["metric_values_computed"] is False


def test_bootstrap_metric_remains_blocked(approval: dict) -> None:
    row = approval["blocked_metric_family"]
    assert row["metric_family_id"] == service.BLOCKED_METRIC_FAMILY_ID
    assert row["approval_status"] == (
        "NOT_APPROVED_BLOCKED_REQUIRES_SEPARATE_OPERATOR_APPROVAL"
    )
    assert row["allowed_for_future_execution"] is False
    assert "chronological-dependence" in row["reason"]


@pytest.mark.parametrize(
    "control_id", service.review_service.candidate_service.NO_PEEK_CONTROL_IDS
)
def test_all_no_peek_controls_are_approved(
    approval: dict, control_id: str
) -> None:
    row = next(
        item
        for item in approval["approved_no_peek_and_leakage_controls"]
        if item["control_id"] == control_id
    )
    assert row["approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_CONTROL"
    )
    assert row["control_status"] == "PLANNED_NOT_EXECUTED"


@pytest.mark.parametrize(
    "output_id", service.review_service.candidate_service.FUTURE_OUTPUT_IDS
)
def test_all_future_outputs_are_authorized_not_generated(
    approval: dict, output_id: str
) -> None:
    row = next(
        item
        for item in approval["approved_future_outputs"]
        if item["output_id"] == output_id
    )
    assert row["approval_status"] == "AUTHORIZED_NOT_GENERATED"
    assert row["output_status"] == "PLANNED_NOT_GENERATED"


PLANNED_COUNTS = [
    ("planned_backtest_lab_row_count", 179190),
    ("planned_evaluable_target_row_count", 177090),
    ("planned_unavailable_target_row_count", 2100),
    ("planned_metric_family_count", 13),
    ("planned_blocked_metric_family_count", 1),
    ("planned_baseline_count", 6),
    ("planned_blocked_baseline_count", 1),
]


@pytest.mark.parametrize(("field", "expected"), PLANNED_COUNTS)
def test_planned_counts_are_preserved(
    approval: dict, field: str, expected: int
) -> None:
    assert approval[field] == expected


@pytest.mark.parametrize("ticker", service.TARGET_UNIVERSE)
def test_per_ticker_approval_entries_preserve_counts(
    approval: dict, ticker: str
) -> None:
    row = next(
        item
        for item in approval["per_ticker_expectancy_backtest_lab_approval_entries"]
        if item["ticker"] == ticker
    )
    assert row["expectancy_backtest_lab_approval_status"] == (
        "APPROVED_FOR_FUTURE_EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY"
    )
    assert row["expectancy_backtest_lab_selected"] is True
    assert row["expectancy_backtest_lab_executed"] is False
    if ticker == "META":
        assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (
            913,
            13695,
        )
        assert row["planned_evaluable_target_row_count"] == 13520
        assert row["approval_note"] == (
            "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_APPROVAL"
        )
    else:
        assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (
            1003,
            15045,
        )
        assert row["planned_evaluable_target_row_count"] == 14870
    assert row["planned_unavailable_target_row_count"] == 175
    assert row["per_ticker_expectancy_backtest_lab_approval_digest"] == (
        service.per_ticker_expectancy_backtest_lab_approval_digest_v1(row)
    )


def test_next_chain_gates_and_risk_controls_are_exact(approval: dict) -> None:
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(approval: dict) -> None:
    assert [row["check_id"] for row in approval["approval_checklist"]] == (
        service.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    assert approval["approval_summary"]["total_checks"] == 75
    assert approval["approval_summary"]["passed_checks"] == 75
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(
    source_review: dict, attestation: dict, approval: dict
) -> None:
    again = service.build_marketflow_expectancy_backtest_lab_approval_v1(
        source_review=source_review,
        operator_attestation=attestation,
    )
    assert again == approval
    assert approval["marketflow_expectancy_backtest_lab_approval_digest"] == (
        service.marketflow_expectancy_backtest_lab_approval_digest_v1(approval)
    )


def test_per_ticker_digests_are_unique_and_deterministic(approval: dict) -> None:
    rows = approval["per_ticker_expectancy_backtest_lab_approval_entries"]
    digests = [row["per_ticker_expectancy_backtest_lab_approval_digest"] for row in rows]
    assert len(set(digests)) == 12
    assert all(len(value) == 64 for value in digests)


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = service.validate_marketflow_expectancy_backtest_lab_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED
    assert result["passed_checks"] == 75


@pytest.mark.parametrize("field", list(ATTESTATION_EXACT_FIELDS))
def test_build_rejects_changed_attestation_exact_field(
    source_review: dict, attestation: dict, field: str
) -> None:
    changed = deepcopy(attestation)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.build_marketflow_expectancy_backtest_lab_approval_v1(
            source_review=source_review,
            operator_attestation=changed,
        )


@pytest.mark.parametrize("field", service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)
def test_build_rejects_false_closed_boundary_confirmation(
    source_review: dict, attestation: dict, field: str
) -> None:
    changed = deepcopy(attestation)
    changed[field] = False
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.build_marketflow_expectancy_backtest_lab_approval_v1(
            source_review=source_review,
            operator_attestation=changed,
        )


def test_build_rejects_changed_source_review(
    source_review: dict, attestation: dict
) -> None:
    changed = deepcopy(source_review)
    changed[
        "marketflow_expectancy_backtest_lab_candidate_operator_review_digest"
    ] = "0" * 64
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.build_marketflow_expectancy_backtest_lab_approval_v1(
            source_review=changed,
            operator_attestation=attestation,
        )


INVALID_EXACT_FIELDS = [
    "artifact_kind",
    "approval_status",
    "approval_scope",
    "selected_backtest_lab_package",
    "selected_vpa_wyckoff_package",
    "selected_matrix_package",
    "selected_matrix_layout",
    "selected_feature_package",
    "selected_label_target_package",
    "selected_objective_path",
    "source_expectancy_backtest_lab_candidate_review_digest",
    "source_expectancy_backtest_lab_candidate_digest",
    "source_vpa_wyckoff_rule_baseline_results_review_digest",
    "source_vpa_wyckoff_rule_values_digest",
    "source_feature_label_matrix_rows_digest",
    "source_target_values_digest",
    "source_records_digest",
    "records_digest",
    "target_universe_count",
    "meta_record_count",
]


@pytest.mark.parametrize("field", INVALID_EXACT_FIELDS)
def test_validator_rejects_changed_exact_field(approval: dict, field: str) -> None:
    changed = deepcopy(approval)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


def test_validator_rejects_target_universe_mismatch(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["target_universe"] = list(reversed(changed["target_universe"]))
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "expectancy_backtest_lab_authorized_for_future_execution",
        "backtest_execution_authorized_for_future_lab_execution",
        "metric_computation_authorized_for_future_lab_execution",
        "expectancy_backtest_lab_approval_created",
        "ready_for_expectancy_backtest_lab_execution",
    ],
)
def test_validator_rejects_required_future_authority_false(
    approval: dict, field: str
) -> None:
    changed = deepcopy(approval)
    changed[field] = False
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


@pytest.mark.parametrize("field", FALSE_BOUNDARY_FIELDS)
def test_validator_rejects_execution_or_downstream_boundary_opened(
    approval: dict, field: str
) -> None:
    changed = deepcopy(approval)
    changed[field] = True
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_acceptance_runtime_or_trading_authority(
    approval: dict, field: str, value: str
) -> None:
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


MISSING_APPROVAL_SECTIONS = [
    "approved_backtest_lab_package",
    "approved_backtest_objectives",
    "approved_baselines",
    "blocked_baseline",
    "approved_chronological_plan",
    "approved_metric_families",
    "blocked_metric_family",
    "approved_no_peek_and_leakage_controls",
    "approved_future_outputs",
    "risk_controls",
]


@pytest.mark.parametrize("field", MISSING_APPROVAL_SECTIONS)
def test_validator_rejects_missing_approval_section(
    approval: dict, field: str
) -> None:
    changed = deepcopy(approval)
    changed.pop(field)
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


def test_validator_rejects_wrong_operator_decision(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_decision"] = "REJECT"
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


def test_validator_rejects_wrong_attestation_phrase(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_attestation_phrase"] = "changed"
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


def test_validator_rejects_missing_approval_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed.pop("marketflow_expectancy_backtest_lab_approval_digest")
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(approval: dict) -> None:
    changed = deepcopy(approval)
    changed["per_ticker_expectancy_backtest_lab_approval_entries"][0].pop(
        "per_ticker_expectancy_backtest_lab_approval_digest"
    )
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.validate_marketflow_expectancy_backtest_lab_approval_v1(changed)


MARKDOWN_HEADINGS = [
    "# Expectancy Backtest Lab Approval v1",
    "## Operator Attestation",
    "## Source Candidate Review",
    "## Bound Evidence",
    "## Dataset and Universe",
    "## Approval Scope",
    "## Selected Backtest Lab Package",
    "## Selected Source Packages",
    "## Approved Objectives",
    "## Approved Baselines",
    "## Blocked Baselines",
    "## Approved Chronological Plan",
    "## Approved Metric Families",
    "## Blocked Metrics",
    "## Approved No-Peek Controls",
    "## Approved Future Outputs",
    "## Planned Counts",
    "## Per-Ticker Approval Summary",
    "## Next Chain",
    "## Next Gates",
    "## Risk Controls",
    "## Predictive Usefulness Boundary",
    "## Profitability Boundary",
    "## Runtime Boundary",
    "## Checklist Summary",
    "## Guardrails",
]


@pytest.mark.parametrize("heading", MARKDOWN_HEADINGS)
def test_markdown_includes_required_sections(approval: dict, heading: str) -> None:
    markdown = service.build_marketflow_expectancy_backtest_lab_approval_markdown_v1(
        approval
    )
    assert heading in markdown


def test_writer_round_trips_in_explicit_directory(
    tmp_path: Path, source_review: dict, attestation: dict
) -> None:
    result = service.write_marketflow_expectancy_backtest_lab_approval_v1(
        tmp_path,
        source_review=source_review,
        operator_attestation=attestation,
    )
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["marketflow_expectancy_backtest_lab_approval_digest"] == (
        result["marketflow_expectancy_backtest_lab_approval_digest"]
    )
    assert "## Guardrails" in markdown_path.read_text(encoding="utf-8")


def test_writer_refuses_overwrite(
    tmp_path: Path, source_review: dict, attestation: dict
) -> None:
    service.write_marketflow_expectancy_backtest_lab_approval_v1(
        tmp_path,
        source_review=source_review,
        operator_attestation=attestation,
    )
    with pytest.raises(service.MarketFlowExpectancyBacktestLabApprovalError):
        service.write_marketflow_expectancy_backtest_lab_approval_v1(
            tmp_path,
            source_review=source_review,
            operator_attestation=attestation,
        )


def test_digest_helper_uses_canonical_semantics(approval: dict) -> None:
    payload = deepcopy(approval)
    payload.pop("marketflow_expectancy_backtest_lab_approval_digest")
    assert semantic_digest(payload) == approval[
        "marketflow_expectancy_backtest_lab_approval_digest"
    ]


EXPORTED_NAMES = [
    "ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED",
    "SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_V1",
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED",
    "EXPECTANCY_BACKTEST_LAB_APPROVAL_ONLY",
    "SELECTED_BACKTEST_LAB_PACKAGE",
    "SELECTED_VPA_WYCKOFF_PACKAGE",
    "SELECTED_MATRIX_PACKAGE",
    "SELECTED_MATRIX_LAYOUT",
    "SELECTED_FEATURE_PACKAGE",
    "SELECTED_LABEL_TARGET_PACKAGE",
    "SELECTED_OBJECTIVE_PATH",
    "REQUIRED_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVAL_ATTESTATION_PHRASE",
    "build_marketflow_expectancy_backtest_lab_approval_attestation_v1",
    "build_marketflow_expectancy_backtest_lab_approval_v1",
    "validate_marketflow_expectancy_backtest_lab_approval_v1",
    "write_marketflow_expectancy_backtest_lab_approval_v1",
    "build_marketflow_expectancy_backtest_lab_approval_markdown_v1",
    "marketflow_expectancy_backtest_lab_approval_digest_v1",
    "per_ticker_expectancy_backtest_lab_approval_digest_v1",
]


@pytest.mark.parametrize("name", EXPORTED_NAMES)
def test_public_service_exports(name: str) -> None:
    assert getattr(services, name) is getattr(service, name)
