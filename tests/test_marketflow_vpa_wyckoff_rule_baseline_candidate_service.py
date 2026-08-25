from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import marketflow_vpa_wyckoff_rule_baseline_candidate_service as service


EXPECTED_CANDIDATE_DIGEST = (
    "7f5bd67e553834978bf6e2fb0a5142e450e55941696704d6da489c1a23b97d66"
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1()


def test_candidate_builds_offline_without_reading_or_executing_matrix_outputs(candidate: dict) -> None:
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False
    assert candidate["feature_label_matrix_execution_rerun_performed"] is False
    assert candidate["feature_label_matrix_results_review_rerun_performed"] is False
    source = inspect.getsource(service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1)
    assert "open(" not in source
    assert "build_marketflow_feature_label_matrix_results_review" not in source


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1"),
    ("schema_version", "marketflow_vpa_wyckoff_rule_baseline_candidate_v1"),
    ("candidate_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW"),
    ("candidate_scope", "VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"),
    ("source_feature_label_matrix_results_review_digest", service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST),
    ("source_feature_label_matrix_execution_digest", service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST),
    ("source_feature_label_matrix_output_binding_digest", service.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST),
    ("source_feature_label_matrix_rows_digest", service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST),
    ("source_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
    ("source_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
    ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ("selected_matrix_package", service.execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX),
    ("selected_matrix_layout", service.execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE),
    ("selected_feature_package", service.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET),
    ("selected_label_target_package", service.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
    ("selected_objective_path", service.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
    ("target_universe_count", 12), ("total_canonical_record_count", 11946),
    ("meta_record_count", 913), ("non_meta_record_count", 1003),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_candidate_core_contract(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


@pytest.mark.parametrize("evidence_key", list(service.SOURCE_EVIDENCE))
def test_complete_source_evidence_chain_is_bound(candidate: dict, evidence_key: str) -> None:
    assert candidate["source_evidence"][evidence_key] == service.SOURCE_EVIDENCE[evidence_key]


def test_universe_order_records_and_meta_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["records_digest"] == service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert candidate["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize("field", [
    "feature_label_matrix_results_review_created",
    "feature_label_matrix_results_review_ready",
    "ready_for_vpa_wyckoff_rule_baseline_candidate",
    "vpa_wyckoff_rule_baseline_candidate_created",
    "vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review",
    "ready_for_vpa_wyckoff_rule_baseline_candidate_operator_review",
])
def test_candidate_readiness_fields_are_true(candidate: dict, field: str) -> None:
    assert candidate[field] is True


def test_candidate_basis_and_philosophy_are_defined(candidate: dict) -> None:
    assert candidate["candidate_philosophy"] == service.CANDIDATE_PHILOSOPHY
    assert candidate["candidate_primary_question"] == service.CANDIDATE_PRIMARY_QUESTION
    assert candidate["candidate_secondary_question"] == service.CANDIDATE_SECONDARY_QUESTION
    assert candidate["candidate_boundary"] == service.CANDIDATE_BOUNDARY
    assert candidate["matrix_row_count"] == 179190
    assert candidate["feature_group_count_per_matrix_row"] == 13


def test_ten_rule_families_are_defined_but_not_executed(candidate: dict) -> None:
    rows = candidate["proposed_vpa_wyckoff_rule_families"]
    assert [row["rule_family_id"] for row in rows] == service.VPA_RULE_FAMILY_IDS
    assert len(rows) == 10
    assert all(row["candidate_status"] == "VPA_WYCKOFF_RULE_CANDIDATE_DEFINED_NOT_EXECUTED" for row in rows)
    assert all(row["rule_execution_authorized"] is False for row in rows)
    assert all(row["rule_values_created"] is False for row in rows)


def test_eight_state_families_are_defined_but_not_executed(candidate: dict) -> None:
    rows = candidate["proposed_wyckoff_state_families"]
    assert [row["state_family_id"] for row in rows] == service.WYCKOFF_STATE_FAMILY_IDS
    assert len(rows) == 8
    assert all(row["candidate_status"] == "WYCKOFF_STATE_CANDIDATE_DEFINED_NOT_EXECUTED" for row in rows)
    assert all(row["state_values_created"] is False for row in rows)


def test_recommended_and_supporting_packages_are_unselected(candidate: dict) -> None:
    packages = candidate["proposed_baseline_packages"]
    assert candidate["recommended_vpa_wyckoff_package"] == service.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE
    assert candidate["supporting_vpa_wyckoff_package"] == service.PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT
    assert packages[0]["included_rule_families"] == service.PRIMARY_RULE_FAMILIES
    assert packages[0]["included_state_families"] == service.PRIMARY_STATE_FAMILIES
    assert all(row["selection_created"] is False for row in packages)


def test_all_thirteen_source_feature_groups_are_mapped_without_targets(candidate: dict) -> None:
    mappings = candidate["source_feature_group_mapping"]
    assert [row["source_feature_group"] for row in mappings] == [row[0] for row in service.SOURCE_FEATURE_GROUP_MAPPING]
    assert len(mappings) == 13
    assert all(row["mapping_status"] == "PLANNED_NOT_EXECUTED" for row in mappings)
    assert all(row["target_values_used"] is False and row["future_data_used"] is False for row in mappings)


def test_twelve_design_questions_remain_unanswered(candidate: dict) -> None:
    questions = candidate["rule_design_questions"]
    assert [row["question"] for row in questions] == service.RULE_DESIGN_QUESTION_TEXTS
    assert len(questions) == 12
    assert all(row["question_status"] == "NOT_ANSWERED" for row in questions)


def test_future_outputs_are_planned_and_not_generated(candidate: dict) -> None:
    outputs = candidate["planned_future_outputs"]
    assert [row["output_id"] for row in outputs] == service.FUTURE_OUTPUT_IDS
    assert len(outputs) == 10
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in outputs)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in outputs)


PLANNED_COUNTS = [
    ("planned_source_matrix_row_count", 179190),
    ("planned_rule_family_count", 10),
    ("planned_wyckoff_state_family_count", 8),
    ("planned_primary_package_rule_family_count", 8),
    ("planned_primary_package_state_family_count", 6),
    ("planned_rule_value_rows", 179190),
    ("planned_rule_state_rows", 179190),
]


@pytest.mark.parametrize(("field", "expected"), PLANNED_COUNTS)
def test_planned_counts_are_defined(candidate: dict, field: str, expected: int) -> None:
    assert candidate[field] == expected


def test_per_ticker_entries_and_digests(candidate: dict) -> None:
    entries = candidate["per_ticker_vpa_wyckoff_rule_baseline_candidate_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_vpa_wyckoff_rule_baseline_candidate_digest")
        assert digest == semantic_digest(payload)
        assert row["vpa_wyckoff_rule_baseline_selected"] is False
        assert row["vpa_wyckoff_rule_values_created"] is False
        if row["ticker"] == "META":
            assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (913, 13695)
            assert row["candidate_note"] == "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE"
        else:
            assert (row["historical_record_count"], row["planned_matrix_row_count"]) == (1003, 15045)


CLOSED_FALSE_FIELDS = [
    "vpa_wyckoff_rule_baseline_selected", "vpa_wyckoff_rule_baseline_approved",
    "vpa_wyckoff_rule_baseline_authorized", "vpa_wyckoff_rule_baseline_executed",
    "vpa_wyckoff_rule_values_created", "vpa_wyckoff_baseline_outputs_created",
    "selection_created", "approval_created", "execution_created", "generation_created",
    "expectancy_backtest_lab_candidate_created", "backtest_execution_authorized",
    "backtest_execution_performed", "model_training_authorized", "model_training_performed",
    "metric_computation_authorized", "metric_computation_performed", "strategy_scoring_performed",
    "trade_recommendations_generated", "provider_requests_made_in_candidate",
    "market_data_acquisition_performed_in_candidate", "canonical_dataset_regenerated_in_candidate",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "signal_feature_generation_execution_rerun_performed",
    "signal_feature_results_review_rerun_performed",
    "target_generation_execution_rerun_performed", "target_results_review_rerun_performed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_candidate_keeps_execution_and_authority_closed(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_acceptance_profitability_runtime_and_trading_remain_closed(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert candidate[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_defined(candidate: dict) -> None:
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_candidate_checklist_passes(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(service.REQUIRED_CHECK_IDS) == 92
    assert all(row["status"] == service.PASS for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"]["passed_checks"] == 92
    assert candidate["candidate_summary"]["failed_checks"] == 0


def test_candidate_and_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    second = service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1()
    assert candidate["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert second["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert second["per_ticker_vpa_wyckoff_rule_baseline_candidate_entries"] == candidate["per_ticker_vpa_wyckoff_rule_baseline_candidate_entries"]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_VALID
    assert result["passed_checks"] == 92


SCALAR_MUTATIONS = [
    ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"),
    ("candidate_scope", "WRONG"),
    ("source_feature_label_matrix_results_review_digest", "0" * 64),
    ("source_feature_label_matrix_rows_digest", "0" * 64),
    ("selected_matrix_package", "WRONG"), ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"), ("selected_objective_path", "WRONG"),
    ("target_universe", ["MSFT"]), ("target_universe_count", 11),
    ("records_digest", "0" * 64), ("meta_record_count", 912),
    ("feature_label_matrix_results_review_ready", False),
    ("vpa_wyckoff_rule_baseline_candidate_created", False),
    ("vpa_wyckoff_rule_baseline_candidate_ready_for_operator_review", False),
    ("candidate_philosophy", ""), ("selection_created", True),
    ("approval_created", True), ("execution_created", True),
    ("vpa_wyckoff_rule_baseline_selected", True),
    ("vpa_wyckoff_rule_baseline_approved", True),
    ("vpa_wyckoff_rule_baseline_executed", True),
    ("vpa_wyckoff_rule_values_created", True),
    ("vpa_wyckoff_baseline_outputs_created", True),
    ("expectancy_backtest_lab_candidate_created", True),
    ("backtest_execution_performed", True), ("model_training_performed", True),
    ("metric_computation_performed", True), ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True), ("provider_requests_made_in_candidate", True),
    ("market_data_acquisition_performed_in_candidate", True),
    ("canonical_dataset_regenerated_in_candidate", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("feature_label_matrix_results_review_rerun_performed", True),
    ("signal_feature_generation_execution_rerun_performed", True),
    ("signal_feature_results_review_rerun_performed", True),
    ("target_generation_execution_rerun_performed", True),
    ("target_results_review_rerun_performed", True),
    ("risk_controls", []),
]


@pytest.mark.parametrize(("field", "value"), SCALAR_MUTATIONS)
def test_validator_rejects_contract_mutations(
    candidate: dict, field: str, value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = value
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(invalid)


@pytest.mark.parametrize("field", [
    "proposed_vpa_wyckoff_rule_families", "proposed_wyckoff_state_families",
    "proposed_baseline_packages", "source_feature_group_mapping",
    "rule_design_questions", "planned_future_outputs",
])
def test_validator_rejects_missing_candidate_design(candidate: dict, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = []
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(invalid)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid.pop("marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest")
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["per_ticker_vpa_wyckoff_rule_baseline_candidate_entries"][0].pop(
        "per_ticker_vpa_wyckoff_rule_baseline_candidate_digest"
    )
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(invalid)


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_markdown_v1(candidate)
    for section in (
        "VPA/Wyckoff Rule Baseline Candidate v1", "Source Feature-Label Matrix Results Review",
        "Bound Evidence", "Dataset and Universe", "Candidate Basis", "Candidate Philosophy",
        "Proposed VPA/Wyckoff Rule Families", "Proposed Wyckoff State Families",
        "Recommended Baseline Package", "Supporting Baseline Package",
        "Source Feature Group Mapping", "Rule Design Questions", "Planned Rule Outputs",
        "Planned Counts", "Per-Ticker Candidate Summary", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_writer_uses_explicit_isolated_directory(candidate: dict, tmp_path: Path) -> None:
    result = service.write_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(tmp_path)
    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    assert json_path.is_file() and markdown_path.is_file()
    persisted = json.loads(json_path.read_text(encoding="utf-8"))
    assert persisted["marketflow_vpa_wyckoff_rule_baseline_candidate_v1_digest"] == EXPECTED_CANDIDATE_DIGEST
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineCandidateError):
        service.write_marketflow_vpa_wyckoff_rule_baseline_candidate_v1(tmp_path)


def test_services_export_candidate_api() -> None:
    assert services.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1 is service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_v1
    assert services.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1 is service.validate_marketflow_vpa_wyckoff_rule_baseline_candidate_v1
    assert services.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE == "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"
