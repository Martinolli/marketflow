from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import marketflow_feature_label_matrix_candidate_service as service


EXPECTED_CANDIDATE_DIGEST = (
    "ef3d42d39a5ae353044d29d645a7ca1ad01143e5557951b05b85f837413187b4"
)


@pytest.fixture(scope="module")
def candidate():
    return service.build_marketflow_feature_label_matrix_candidate_v1()


def test_candidate_builds_offline_without_source_execution(candidate):
    assert candidate["created_offline"] is True
    assert candidate["research_only"] is True
    assert candidate["provider_requests_made_in_candidate"] is False
    assert candidate["market_data_acquisition_performed_in_candidate"] is False
    assert candidate["target_generation_execution_rerun_performed"] is False
    assert candidate["signal_or_feature_generation_results_review_rerun_performed"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION),
        ("source_signal_or_feature_generation_results_review_digest", service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST),
        ("source_signal_or_feature_generation_execution_digest", service.EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST),
        ("source_signal_or_feature_generation_output_binding_digest", service.EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST),
        ("source_signal_or_feature_values_digest", service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST),
        ("source_objective_label_or_target_generation_results_review_digest", service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST),
        ("source_objective_label_or_target_values_digest", service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST),
        ("selected_feature_package", service.feature_review.execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET),
        ("selected_label_target_package", service.feature_review.execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
        ("selected_objective_path", service.feature_review.execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
        ("target_universe_count", 12),
        ("total_canonical_record_count", 11946),
        ("meta_record_count", 913),
        ("feature_row_count", 155298),
        ("available_feature_row_count", 155142),
        ("unavailable_feature_row_count", 156),
        ("target_row_count", 179190),
        ("available_target_row_count", 177090),
        ("unavailable_target_row_count", 2100),
        ("selected_feature_group_count", 13),
        ("target_profile_count", 15),
    ],
)
def test_candidate_contract_fields(candidate, field, expected):
    assert candidate[field] == expected


@pytest.mark.parametrize(
    "evidence_key",
    [
        "marketflow_signal_or_feature_generation_results_review_digest",
        "marketflow_signal_or_feature_generation_execution_digest",
        "signal_or_feature_generation_output_binding_digest",
        "signal_or_feature_values_digest",
        "marketflow_signal_or_feature_generation_approval_digest",
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "marketflow_signal_or_feature_generation_candidate_v1_digest",
        "marketflow_objective_label_or_target_generation_results_review_digest",
        "marketflow_objective_label_or_target_generation_execution_digest",
        "objective_label_or_target_generation_output_binding_digest",
        "objective_label_or_target_values_digest",
        "marketflow_objective_label_or_target_generation_approval_digest",
        "marketflow_expectancy_objective_design_results_review_digest",
        "marketflow_expectancy_objective_design_execution_digest",
        "expectancy_objective_design_output_binding_digest",
        "marketflow_algorithm_strategy_charter_v1_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "research_registry_approval_digest",
        "records_digest",
    ],
)
def test_bound_source_evidence(candidate, evidence_key):
    assert candidate["source_evidence"][evidence_key] == service.SOURCE_EVIDENCE[evidence_key]


def test_universe_order_records_and_meta_are_preserved(candidate):
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["records_digest"] == service.feature_review.execution.EXPECTED_RECORDS_DIGEST
    assert candidate["meta_record_count"] == 913
    assert candidate["non_meta_record_count"] == 1003
    assert candidate["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    "field",
    [
        "target_results_review_ready",
        "signal_or_feature_generation_results_review_ready",
        "ready_for_feature_label_matrix_candidate",
        "feature_label_matrix_candidate_created",
        "feature_label_matrix_candidate_ready_for_operator_review",
        "ready_for_feature_label_matrix_candidate_operator_review",
    ],
)
def test_candidate_readiness_fields_are_true(candidate, field):
    assert candidate[field] is True


def test_candidate_basis_and_philosophy_are_defined(candidate):
    assert candidate["feature_values_digest"] == service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
    assert candidate["target_values_digest"] == service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
    assert candidate["candidate_philosophy"] == service.CANDIDATE_PHILOSOPHY
    assert candidate["candidate_primary_question"] == service.CANDIDATE_PRIMARY_QUESTION
    assert candidate["candidate_secondary_question"] == service.CANDIDATE_SECONDARY_QUESTION
    assert candidate["candidate_boundary"] == service.CANDIDATE_BOUNDARY


def test_recommended_matrix_package_is_defined_but_not_selected(candidate):
    assert candidate["recommended_matrix_package"] == service.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
    package = candidate["recommended_matrix_package_definition"]
    assert package["package_id"] == service.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
    assert package["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["recommended_layout"] == "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["execution_created"] is False


def test_three_matrix_layouts_are_candidate_only(candidate):
    assert candidate["matrix_layouts"] == service.MATRIX_LAYOUTS
    assert [row["layout_id"] for row in candidate["matrix_layouts"]] == [
        "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE",
        "MATRIX_LAYOUT_LONG_FEATURE_TARGET_AUDIT",
        "MATRIX_LAYOUT_CANONICAL_RECORD_FEATURE_BUNDLE",
    ]
    assert candidate["matrix_layouts"][0]["planned_matrix_row_count"] == 179190
    assert candidate["matrix_layouts"][1]["planned_long_audit_pair_count"] == 2329470
    assert candidate["matrix_layouts"][2]["planned_canonical_feature_bundle_count"] == 11946
    assert all(row["selection_created"] is False for row in candidate["matrix_layouts"])


@pytest.mark.parametrize(
    ("field", "id_field", "expected_ids", "status_field"),
    [
        ("matrix_alignment_keys", "alignment_key_id", service.ALIGNMENT_KEY_IDS, "key_status"),
        ("feature_side_join_rules", "feature_side_join_rule_id", service.FEATURE_SIDE_JOIN_RULE_IDS, "rule_status"),
        ("target_side_join_rules", "target_side_join_rule_id", service.TARGET_SIDE_JOIN_RULE_IDS, "rule_status"),
        ("matrix_quality_checks", "quality_check_id", service.QUALITY_CHECK_IDS, "quality_check_status"),
    ],
)
def test_planned_keys_rules_and_quality_checks(candidate, field, id_field, expected_ids, status_field):
    rows = candidate[field]
    assert [row[id_field] for row in rows] == expected_ids
    assert all(row[status_field] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_future_outputs_are_planned_and_not_generated(candidate):
    outputs = candidate["planned_future_outputs"]
    assert [row["output_id"] for row in outputs] == service.FUTURE_OUTPUT_IDS
    assert len(outputs) == 12
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in outputs)
    assert all(row["research_only"] is True for row in outputs)
    assert all(row["non_actionable"] is True for row in outputs)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("planned_matrix_row_count", 179190),
        ("planned_available_matrix_row_count", 177090),
        ("planned_unavailable_target_row_count", 2100),
        ("planned_feature_group_count", 13),
        ("planned_target_profile_count", 15),
        ("planned_canonical_record_count", 11946),
    ],
)
def test_planned_matrix_counts(candidate, field, expected):
    assert candidate[field] == expected


def test_per_ticker_entries_and_digests(candidate):
    entries = candidate["per_ticker_feature_label_matrix_candidate_entries"]
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop("per_ticker_feature_label_matrix_candidate_digest")
        assert digest == semantic_digest(payload)
        assert row["source_signal_feature_results_review_digest"] == service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST
        assert row["feature_label_matrix_created"] is False
        if row["ticker"] == "META":
            assert (
                row["historical_record_count"], row["planned_matrix_row_count"],
                row["planned_available_matrix_row_count"], row["planned_feature_row_count"],
            ) == (913, 13695, 13520, 11869)
            assert row["candidate_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_CANDIDATE"
        else:
            assert (
                row["historical_record_count"], row["planned_matrix_row_count"],
                row["planned_available_matrix_row_count"], row["planned_feature_row_count"],
            ) == (1003, 15045, 14870, 13039)


@pytest.mark.parametrize(
    "field",
    [
        "feature_label_matrix_selected",
        "feature_label_matrix_approved",
        "feature_label_matrix_authorized",
        "feature_label_matrix_created",
        "feature_label_matrix_rows_created",
        "feature_label_matrix_execution_performed",
        "selection_created",
        "approval_created",
        "creation_created",
        "execution_created",
        "generation_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "canonical_dataset_regenerated_in_candidate",
        "target_generation_execution_rerun_performed",
        "target_generation_results_review_rerun_performed",
        "signal_or_feature_generation_execution_rerun_performed",
        "signal_or_feature_generation_results_review_rerun_performed",
    ],
)
def test_closed_candidate_flags_remain_false(candidate, field):
    assert candidate[field] is False


def test_acceptance_profitability_and_runtime_remain_closed(candidate):
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert candidate[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert len(candidate["next_chain"]) == 8
    assert candidate["next_gates"] == service.NEXT_GATES
    assert len(candidate["next_gates"]) == 8
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 28


def test_checklist_passes(candidate):
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(service.REQUIRED_CHECK_IDS) == 92
    summary = candidate["candidate_summary"]
    assert summary["total_checks"] == 92
    assert summary["passed_checks"] == 92
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_candidate_and_per_ticker_digests_are_deterministic(candidate):
    assert candidate["marketflow_feature_label_matrix_candidate_v1_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert service.marketflow_feature_label_matrix_candidate_v1_digest(candidate) == EXPECTED_CANDIDATE_DIGEST
    second = service.build_marketflow_feature_label_matrix_candidate_v1()
    assert second == candidate


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_feature_label_matrix_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_VALID
    assert result["passed_checks"] == 92


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_signal_or_feature_generation_results_review_digest", "0" * 64),
        ("source_signal_or_feature_generation_execution_digest", "0" * 64),
        ("source_signal_or_feature_values_digest", "0" * 64),
        ("source_objective_label_or_target_generation_results_review_digest", "0" * 64),
        ("source_objective_label_or_target_values_digest", "0" * 64),
        ("selected_feature_package", "WRONG"),
        ("selected_label_target_package", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("target_universe", ["AAPL"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 914),
        ("target_results_review_ready", False),
        ("signal_or_feature_generation_results_review_ready", False),
        ("ready_for_feature_label_matrix_candidate", False),
        ("feature_label_matrix_candidate_created", False),
        ("feature_label_matrix_candidate_ready_for_operator_review", False),
        ("ready_for_feature_label_matrix_candidate_operator_review", False),
        ("recommended_matrix_package", None),
        ("matrix_layouts", []),
        ("matrix_alignment_keys", []),
        ("feature_side_join_rules", []),
        ("target_side_join_rules", []),
        ("matrix_quality_checks", []),
        ("planned_future_outputs", []),
        ("selection_created", True),
        ("approval_created", True),
        ("execution_created", True),
        ("feature_label_matrix_selected", True),
        ("feature_label_matrix_approved", True),
        ("feature_label_matrix_created", True),
        ("feature_label_matrix_rows_created", True),
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
        ("target_generation_execution_rerun_performed", True),
        ("target_generation_results_review_rerun_performed", True),
        ("signal_or_feature_generation_execution_rerun_performed", True),
        ("signal_or_feature_generation_results_review_rerun_performed", True),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_candidate_fields(candidate, field, bad_value):
    changed = deepcopy(candidate)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.validate_marketflow_feature_label_matrix_candidate_v1(changed)


@pytest.mark.parametrize(
    "source_field",
    [
        "marketflow_signal_or_feature_generation_results_review_digest",
        "marketflow_signal_or_feature_generation_execution_digest",
        "signal_or_feature_values_digest",
        "marketflow_objective_label_or_target_generation_results_review_digest",
        "objective_label_or_target_values_digest",
    ],
)
def test_validator_rejects_changed_source_evidence(candidate, source_field):
    changed = deepcopy(candidate)
    changed["source_evidence"][source_field] = "0" * 64
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.validate_marketflow_feature_label_matrix_candidate_v1(changed)


def test_validator_rejects_missing_recommended_package_definition(candidate):
    changed = deepcopy(candidate)
    changed["recommended_matrix_package_definition"] = None
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.validate_marketflow_feature_label_matrix_candidate_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate):
    changed = deepcopy(candidate)
    changed["per_ticker_feature_label_matrix_candidate_entries"][0].pop(
        "per_ticker_feature_label_matrix_candidate_digest"
    )
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.validate_marketflow_feature_label_matrix_candidate_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate):
    changed = deepcopy(candidate)
    changed.pop("marketflow_feature_label_matrix_candidate_v1_digest")
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.validate_marketflow_feature_label_matrix_candidate_v1(changed)


def test_writer_creates_json_and_markdown(candidate, tmp_path):
    result = service.write_marketflow_feature_label_matrix_candidate_v1(tmp_path)
    json_path = tmp_path / "marketflow_feature_label_matrix_candidate_v1.json"
    markdown_path = tmp_path / "marketflow_feature_label_matrix_candidate_v1.md"
    assert json_path.is_file()
    assert markdown_path.is_file()
    written = json.loads(json_path.read_text(encoding="utf-8"))
    assert written["marketflow_feature_label_matrix_candidate_v1_digest"] == EXPECTED_CANDIDATE_DIGEST
    assert result["json_path"].endswith(json_path.name)
    assert result["markdown_path"].endswith(markdown_path.name)
    with pytest.raises(service.MarketFlowFeatureLabelMatrixCandidateError):
        service.write_marketflow_feature_label_matrix_candidate_v1(tmp_path)


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_feature_label_matrix_candidate_markdown_v1(
        candidate
    )
    for heading in (
        "# Feature-Label Matrix Candidate v1",
        "## Source Signal or Feature Results Review",
        "## Source Target Results Review",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Candidate Basis",
        "## Candidate Philosophy",
        "## Recommended Matrix Package",
        "## Proposed Matrix Layouts",
        "## Matrix Alignment Keys",
        "## Feature-Side Join Rules",
        "## Target-Side Join Rules",
        "## Planned Matrix Counts",
        "## Matrix Quality Checks",
        "## Planned Future Outputs",
        "## Per-Ticker Candidate Summary",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1 == service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1
    assert services.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW == service.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert services.FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION == service.FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION
    assert services.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX == service.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
    assert services.build_marketflow_feature_label_matrix_candidate_v1 is service.build_marketflow_feature_label_matrix_candidate_v1
    assert services.validate_marketflow_feature_label_matrix_candidate_v1 is service.validate_marketflow_feature_label_matrix_candidate_v1
    assert services.write_marketflow_feature_label_matrix_candidate_v1 is service.write_marketflow_feature_label_matrix_candidate_v1
