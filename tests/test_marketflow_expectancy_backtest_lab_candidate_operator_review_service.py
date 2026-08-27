from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_expectancy_backtest_lab_candidate_operator_review_service as service,
)


EXPECTED_REVIEW_DIGEST = (
    "20266beddbc11d488cdfb81e24748391949a1270c11e28c0b173752a0ee61b3b"
)


@pytest.fixture(scope="module")
def source_candidate() -> dict:
    return service.candidate_service.build_marketflow_expectancy_backtest_lab_candidate_v1()


@pytest.fixture(scope="module")
def review(source_candidate: dict) -> dict:
    return service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        source_candidate
    )


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["live_provider_transport_enabled_in_review"] is False
    assert review["market_data_acquisition_performed_in_review"] is False


def test_default_builder_builds_and_validates_source_candidate() -> None:
    review = service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1()
    assert (
        review["marketflow_expectancy_backtest_lab_candidate_operator_review_digest"]
        == EXPECTED_REVIEW_DIGEST
    )


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    ),
    (
        "schema_version",
        "marketflow_expectancy_backtest_lab_candidate_operator_review_v1",
    ),
    (
        "review_status",
        "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    ),
    (
        "review_scope",
        "EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    ),
    (
        "source_expectancy_backtest_lab_candidate_digest",
        service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    ),
    (
        "source_vpa_wyckoff_rule_baseline_results_review_digest",
        service.EXPECTED_SOURCE_VPA_WYCKOFF_RESULTS_REVIEW_DIGEST,
    ),
    (
        "source_vpa_wyckoff_rule_baseline_execution_digest",
        service.EXPECTED_SOURCE_VPA_WYCKOFF_EXECUTION_DIGEST,
    ),
    (
        "source_vpa_wyckoff_rule_baseline_output_binding_digest",
        service.EXPECTED_SOURCE_VPA_WYCKOFF_OUTPUT_BINDING_DIGEST,
    ),
    (
        "source_vpa_wyckoff_rule_values_digest",
        service.EXPECTED_SOURCE_VPA_WYCKOFF_RULE_VALUES_DIGEST,
    ),
    (
        "source_feature_label_matrix_results_review_digest",
        service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
    ),
    ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
    ("source_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
    ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_review_core_contract(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_complete_source_evidence_chain_is_bound(
    review: dict, source_candidate: dict
) -> None:
    assert review["source_evidence"] == {
        "marketflow_expectancy_backtest_lab_candidate_v1_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        **source_candidate["source_evidence"],
    }


def test_universe_order_records_and_meta_are_preserved(review: dict) -> None:
    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert review["meta_reduced_record_count_preserved"] is True


TRUE_FIELDS = [
    "expectancy_backtest_lab_candidate_created",
    "expectancy_backtest_lab_candidate_ready_for_operator_review",
    "expectancy_backtest_lab_candidate_review_created",
    "expectancy_backtest_lab_candidate_review_ready",
]


@pytest.mark.parametrize("field", TRUE_FIELDS)
def test_candidate_and_review_readiness_are_true(review: dict, field: str) -> None:
    assert review[field] is True


FALSE_FIELDS = [
    "ready_for_expectancy_backtest_lab_approval",
    "expectancy_backtest_lab_selected",
    "expectancy_backtest_lab_approved",
    "expectancy_backtest_lab_authorized",
    "expectancy_backtest_lab_executed",
    "expectancy_backtest_rows_created",
    "expectancy_backtest_results_created",
    "selection_created",
    "approval_created",
    "execution_created",
    "generation_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "trade_recommendations_generated",
    "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review",
    "vpa_wyckoff_rule_baseline_execution_rerun_performed",
    "vpa_wyckoff_rule_baseline_results_review_rerun_performed",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "signal_feature_generation_rerun_performed",
    "target_generation_rerun_performed",
    "expectancy_backtest_lab_candidate_creation_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", FALSE_FIELDS)
def test_all_authority_and_execution_flags_remain_false(review: dict, field: str) -> None:
    assert review[field] is False


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_acceptance_remains_not_accepted(review: dict, field: str) -> None:
    assert review[field] == service.NOT_ACCEPTED


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(review: dict, field: str) -> None:
    assert review[field] == service.NOT_AUTHORIZED


BASIS_FIELDS = [
    ("matrix_row_count", 179190),
    ("available_matrix_row_count", 177090),
    ("unavailable_target_matrix_row_count", 2100),
    ("rule_value_row_count", 179190),
    ("state_value_row_count", 179190),
    ("selected_rule_family_count", 8),
    ("selected_state_family_count", 6),
    ("rule_family_reference_count", 1433520),
    ("state_family_reference_count", 1075140),
    ("target_profile_count", 15),
    ("feature_group_count_per_matrix_row", 13),
    ("target_unavailable_row_count", 2100),
]


@pytest.mark.parametrize(("field", "expected"), BASIS_FIELDS)
def test_candidate_basis_is_reviewed(review: dict, field: str, expected: int) -> None:
    assert review[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("candidate_philosophy", service.candidate_service.CANDIDATE_PHILOSOPHY),
        ("candidate_primary_question", service.candidate_service.CANDIDATE_PRIMARY_QUESTION),
        ("candidate_secondary_question", service.candidate_service.CANDIDATE_SECONDARY_QUESTION),
        ("candidate_boundary", service.candidate_service.CANDIDATE_BOUNDARY),
    ],
)
def test_candidate_philosophy_is_reviewed(
    review: dict, field: str, expected: str
) -> None:
    assert review[field] == expected


PACKAGE_CASES = [
    (
        service.candidate_service.PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB,
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
        "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED",
    ),
    (
        service.candidate_service.PACKAGE_EXPECTANCY_FEATURE_ONLY_DIAGNOSTIC_LAB,
        "REVIEWED_AVAILABLE_DIAGNOSTIC_PACKAGE_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
    ),
    (
        service.candidate_service.PACKAGE_EXPECTANCY_ABSTENTION_QUALITY_DIAGNOSTIC_LAB,
        "REVIEWED_AVAILABLE_DIAGNOSTIC_PACKAGE_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
    ),
    (
        service.candidate_service.PACKAGE_EXPECTANCY_COST_SENSITIVITY_DIAGNOSTIC_LAB,
        "REVIEWED_AVAILABLE_DIAGNOSTIC_PACKAGE_NOT_SELECTED",
        "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED",
    ),
]


@pytest.mark.parametrize(("package_id", "review_status", "source_status"), PACKAGE_CASES)
def test_packages_are_reviewed_but_not_selected(
    review: dict, package_id: str, review_status: str, source_status: str
) -> None:
    row = next(
        item
        for item in review["reviewed_backtest_lab_packages"]
        if item["package_id"] == package_id
    )
    assert row["review_status"] == review_status
    assert row["source_status"] == source_status
    assert row["selection_created"] is False
    assert row["approval_created"] is False
    assert row["execution_created"] is False


@pytest.mark.parametrize("objective_id", service.candidate_service.BACKTEST_OBJECTIVE_IDS)
def test_all_objectives_are_reviewed_not_executed(
    review: dict, objective_id: str
) -> None:
    row = next(
        item for item in review["reviewed_backtest_objectives"] if item["objective_id"] == objective_id
    )
    assert row["review_status"] == "REVIEWED_CANDIDATE_OBJECTIVE_NOT_EXECUTED"
    assert row["objective_status"] == "CANDIDATE_OBJECTIVE_NOT_EXECUTED"
    assert row["metric_computation_authorized"] is False
    assert row["backtest_execution_authorized"] is False
    assert row["model_training_authorized"] is False


@pytest.mark.parametrize("baseline_id", service.candidate_service.BASELINE_IDS)
def test_all_baselines_are_reviewed_not_executed(
    review: dict, baseline_id: str
) -> None:
    row = next(
        item for item in review["reviewed_baselines"] if item["baseline_id"] == baseline_id
    )
    assert row["review_status"] == "REVIEWED_CANDIDATE_BASELINE_NOT_EXECUTED"
    assert row["baseline_status"] == "CANDIDATE_BASELINE_NOT_EXECUTED"
    assert row["metric_computation_authorized"] is False


def test_randomized_baseline_remains_blocked(review: dict) -> None:
    row = next(
        item
        for item in review["reviewed_baselines"]
        if item["baseline_id"] == "BASELINE_RANDOMIZED_NULL_REFERENCE_BLOCKED"
    )
    assert row["allowed_for_future_execution"] is False
    assert "chronological/no-peek" in row["reason"]


def test_chronological_plan_is_reviewed_not_executed(review: dict) -> None:
    plan = review["reviewed_chronological_plan"]
    assert plan["training_or_calibration_window"] == {
        "date_start": "2022-01-01",
        "date_end": "2023-12-31",
    }
    assert plan["validation_window"]["date_start"] == "2024-01-01"
    assert plan["holdout_window"]["date_end"] == "2025-12-31"
    assert plan["split_policy"] == "CHRONOLOGICAL_NO_SHUFFLE"
    assert plan["split_execution_status"] == "PLANNED_NOT_EXECUTED"
    assert plan["review_status"] == "REVIEWED_CHRONOLOGICAL_PLAN_NOT_EXECUTED"


@pytest.mark.parametrize("metric_id", service.candidate_service.METRIC_FAMILY_IDS)
def test_all_metric_families_are_reviewed_not_computed(
    review: dict, metric_id: str
) -> None:
    row = next(
        item for item in review["reviewed_metric_families"] if item["metric_family_id"] == metric_id
    )
    assert row["review_status"] == "REVIEWED_CANDIDATE_METRIC_NOT_COMPUTED"
    assert row["metric_status"] == "CANDIDATE_METRIC_NOT_COMPUTED"
    assert row["metric_computation_authorized"] is False


def test_bootstrap_metric_remains_blocked(review: dict) -> None:
    row = next(
        item
        for item in review["reviewed_metric_families"]
        if item["metric_family_id"] == "METRIC_CONFIDENCE_INTERVAL_OR_BOOTSTRAP_BLOCKED"
    )
    assert row["allowed_for_future_execution"] is False
    assert "chronological-dependence" in row["reason"]


@pytest.mark.parametrize("control_id", service.candidate_service.NO_PEEK_CONTROL_IDS)
def test_all_no_peek_controls_are_reviewed_not_executed(
    review: dict, control_id: str
) -> None:
    row = next(
        item
        for item in review["reviewed_no_peek_and_leakage_controls"]
        if item["control_id"] == control_id
    )
    assert row["review_status"] == "REVIEWED_PLANNED_CONTROL_NOT_EXECUTED"
    assert row["control_status"] == "PLANNED_NOT_EXECUTED"
    assert row["requires_future_backtest_lab_approval"] is True


@pytest.mark.parametrize("output_id", service.candidate_service.FUTURE_OUTPUT_IDS)
def test_all_future_outputs_are_reviewed_not_generated(
    review: dict, output_id: str
) -> None:
    row = next(
        item for item in review["reviewed_future_outputs"] if item["output_id"] == output_id
    )
    assert row["review_status"] == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
    assert row["output_status"] == "PLANNED_NOT_GENERATED"


@pytest.mark.parametrize(
    ("field", "expected"),
    list(service.candidate_service._planned_counts().items()),
)
def test_planned_counts_are_reviewed(
    review: dict, field: str, expected: object
) -> None:
    assert review["reviewed_planned_counts"][field] == expected


@pytest.mark.parametrize("ticker", service.TARGET_UNIVERSE)
def test_per_ticker_review_entries_preserve_counts(review: dict, ticker: str) -> None:
    row = next(
        item
        for item in review["per_ticker_expectancy_backtest_lab_candidate_review_entries"]
        if item["ticker"] == ticker
    )
    assert row["expectancy_backtest_lab_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT"
    assert row["source_expectancy_backtest_lab_candidate_digest"] == service.EXPECTED_SOURCE_CANDIDATE_DIGEST
    if ticker == "META":
        assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (913, 13695)
        assert row["planned_evaluable_target_row_count"] == 13520
        assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_EXPECTANCY_BACKTEST_LAB_CANDIDATE_REVIEW"
    else:
        assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (1003, 15045)
        assert row["planned_evaluable_target_row_count"] == 14870
    assert row["planned_unavailable_target_row_count"] == 175
    assert row["expectancy_backtest_lab_selected"] is False
    assert row["per_ticker_expectancy_backtest_lab_candidate_review_digest"] == service.per_ticker_expectancy_backtest_lab_candidate_review_digest_v1(row)


def test_next_chain_gates_and_risk_controls_are_exact(review: dict) -> None:
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(review: dict) -> None:
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["review_checklist"])
    assert review["review_summary"]["total_checks"] == 67
    assert review["review_summary"]["passed_checks"] == 67
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(source_candidate: dict, review: dict) -> None:
    again = service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        source_candidate
    )
    assert again == review
    assert review["marketflow_expectancy_backtest_lab_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert service.marketflow_expectancy_backtest_lab_candidate_operator_review_digest_v1(review) == EXPECTED_REVIEW_DIGEST


def test_per_ticker_digests_are_unique_and_deterministic(review: dict) -> None:
    rows = review["per_ticker_expectancy_backtest_lab_candidate_review_entries"]
    digests = [row["per_ticker_expectancy_backtest_lab_candidate_review_digest"] for row in rows]
    assert len(set(digests)) == 12
    assert all(len(value) == 64 for value in digests)


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_VALID
    assert result["passed_checks"] == 67


INVALID_EXACT_FIELDS = [
    "artifact_kind",
    "review_status",
    "review_scope",
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
def test_validator_rejects_changed_exact_field(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


def test_validator_rejects_target_universe_mismatch(review: dict) -> None:
    changed = deepcopy(review)
    changed["target_universe"] = list(reversed(changed["target_universe"]))
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


@pytest.mark.parametrize("field", TRUE_FIELDS[2:])
def test_validator_rejects_required_review_readiness_false(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = False
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


@pytest.mark.parametrize("field", FALSE_FIELDS)
def test_validator_rejects_opened_authority_or_execution_gate(
    review: dict, field: str
) -> None:
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


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
    review: dict, field: str, value: str
) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


MISSING_REVIEW_SECTIONS = [
    "reviewed_backtest_lab_packages",
    "reviewed_backtest_objectives",
    "reviewed_baselines",
    "reviewed_chronological_plan",
    "reviewed_metric_families",
    "reviewed_no_peek_and_leakage_controls",
    "reviewed_future_outputs",
    "reviewed_planned_counts",
    "risk_controls",
]


@pytest.mark.parametrize("field", MISSING_REVIEW_SECTIONS)
def test_validator_rejects_missing_review_section(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed.pop(field)
    with pytest.raises((service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError, KeyError, StopIteration)):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    changed = deepcopy(review)
    changed.pop("marketflow_expectancy_backtest_lab_candidate_operator_review_digest")
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    changed = deepcopy(review)
    changed["per_ticker_expectancy_backtest_lab_candidate_review_entries"][0].pop(
        "per_ticker_expectancy_backtest_lab_candidate_review_digest"
    )
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(changed)


MARKDOWN_HEADINGS = [
    "# Expectancy Backtest Lab Candidate Operator Review v1",
    "## Source Candidate",
    "## Source VPA/Wyckoff Results Review",
    "## Source Feature-Label Matrix Results Review",
    "## Bound Evidence",
    "## Dataset and Universe",
    "## Reviewed Candidate Basis",
    "## Reviewed Candidate Philosophy",
    "## Reviewed Recommended Backtest Lab Package",
    "## Reviewed Supporting Backtest Lab Packages",
    "## Reviewed Backtest Objectives",
    "## Reviewed Baselines",
    "## Reviewed Chronological Plan",
    "## Reviewed Metric Families",
    "## Reviewed No-Peek and Leakage Controls",
    "## Reviewed Planned Outputs",
    "## Reviewed Planned Counts",
    "## Per-Ticker Review Summary",
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
def test_markdown_includes_required_sections(review: dict, heading: str) -> None:
    markdown = service.build_marketflow_expectancy_backtest_lab_candidate_operator_review_markdown_v1(review)
    assert heading in markdown


def test_writer_round_trips_review_in_explicit_directory(
    tmp_path: Path, source_candidate: dict
) -> None:
    result = service.write_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        tmp_path, candidate=source_candidate
    )
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["marketflow_expectancy_backtest_lab_candidate_operator_review_digest"] == EXPECTED_REVIEW_DIGEST
    assert "## Guardrails" in markdown_path.read_text(encoding="utf-8")


def test_writer_refuses_overwrite(tmp_path: Path, source_candidate: dict) -> None:
    service.write_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
        tmp_path, candidate=source_candidate
    )
    with pytest.raises(service.MarketFlowExpectancyBacktestLabCandidateOperatorReviewError):
        service.write_marketflow_expectancy_backtest_lab_candidate_operator_review_v1(
            tmp_path, candidate=source_candidate
        )


def test_digest_helper_uses_canonical_semantics(review: dict) -> None:
    payload = deepcopy(review)
    payload.pop("marketflow_expectancy_backtest_lab_candidate_operator_review_digest")
    assert semantic_digest(payload) == EXPECTED_REVIEW_DIGEST


EXPORTED_NAMES = [
    "ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    "SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_V1",
    "MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    "EXPECTANCY_BACKTEST_LAB_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    "build_marketflow_expectancy_backtest_lab_candidate_operator_review_v1",
    "validate_marketflow_expectancy_backtest_lab_candidate_operator_review_v1",
    "write_marketflow_expectancy_backtest_lab_candidate_operator_review_v1",
    "build_marketflow_expectancy_backtest_lab_candidate_operator_review_markdown_v1",
    "marketflow_expectancy_backtest_lab_candidate_operator_review_digest_v1",
    "per_ticker_expectancy_backtest_lab_candidate_review_digest_v1",
]


@pytest.mark.parametrize("name", EXPORTED_NAMES)
def test_public_service_exports(name: str) -> None:
    assert getattr(services, name) is getattr(service, name)
