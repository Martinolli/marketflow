from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import (
    marketflow_vpa_wyckoff_rule_baseline_approval_service as approval_service,
)


def _attestation() -> dict:
    return approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-26T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        operator_confirms_matrix_results_review_digest=approval_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        operator_confirms_matrix_rows_digest=approval_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        operator_confirms_feature_values_digest=approval_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        operator_confirms_target_values_digest=approval_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        operator_confirms_records_digest=approval_service.EXPECTED_SOURCE_RECORDS_DIGEST,
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_vpa_wyckoff_package=approval_service.SELECTED_VPA_WYCKOFF_PACKAGE,
        operator_confirms_selected_matrix_package=approval_service.SELECTED_MATRIX_PACKAGE,
        operator_confirms_selected_matrix_layout=approval_service.SELECTED_MATRIX_LAYOUT,
        operator_confirms_selected_feature_package=approval_service.SELECTED_FEATURE_PACKAGE,
        operator_confirms_selected_label_target_package=approval_service.SELECTED_LABEL_TARGET_PACKAGE,
        operator_confirms_selected_objective_path=approval_service.SELECTED_OBJECTIVE_PATH,
        **{
            field: True
            for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    )


@pytest.fixture(scope="module")
def attestation() -> dict:
    return _attestation()


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval_service.review_service.build_marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_v1()


@pytest.fixture(scope="module")
def approval(attestation: dict) -> dict:
    return approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_VPA_WYCKOFF_RULE_BASELINE"
    assert attestation["operator_attestation_phrase"] == (
        approval_service.REQUIRED_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        "marketflow_vpa_wyckoff_rule_baseline_approval_operator_attestation_v1"
    )
    assert all(
        attestation[field] is True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline(approval: dict) -> None:
    assert approval["created_offline"] is True
    assert approval["provider_requests_made_in_approval"] is False
    assert approval["live_provider_transport_enabled_in_approval"] is False
    assert approval["market_data_acquisition_performed_in_approval"] is False


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED"),
    ("schema_version", "marketflow_vpa_wyckoff_rule_baseline_approval_v1"),
    ("approval_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED"),
    ("approval_scope", "VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY"),
    ("selected_vpa_wyckoff_package", "PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("source_vpa_wyckoff_rule_baseline_candidate_review_artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"),
    ("source_vpa_wyckoff_rule_baseline_candidate_review_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"),
    ("source_vpa_wyckoff_rule_baseline_candidate_review_scope", "VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"),
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
    ("feature_group_count_per_matrix_row", 13),
    ("feature_group_reference_count", 2329470),
    ("feature_source_row_count", 155298),
    ("target_source_row_count", 179190),
    ("vpa_wyckoff_rule_baseline_candidate_created", True),
    ("vpa_wyckoff_rule_baseline_candidate_review_created", True),
    ("vpa_wyckoff_rule_baseline_candidate_review_ready", True),
    ("vpa_wyckoff_rule_baseline_selected", True),
    ("vpa_wyckoff_rule_baseline_approved", True),
    ("vpa_wyckoff_rule_baseline_authorized", True),
    ("vpa_wyckoff_rule_baseline_approval_created", True),
    ("ready_for_vpa_wyckoff_rule_baseline_execution", True),
    ("vpa_wyckoff_rule_baseline_authorized_for_future_execution", True),
    ("vpa_wyckoff_rule_baseline_executed", False),
    ("vpa_wyckoff_rule_values_created", False),
    ("vpa_wyckoff_state_values_created", False),
    ("vpa_wyckoff_baseline_outputs_created", False),
    ("expectancy_backtest_lab_candidate_created", False),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(approval: dict, field: str, expected: object) -> None:
    assert approval[field] == expected


BOUND_DIGESTS = {
    "source_vpa_wyckoff_rule_baseline_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_vpa_wyckoff_rule_baseline_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_feature_label_matrix_results_review_digest": approval_service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
    "source_feature_label_matrix_execution_digest": approval_service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
    "source_feature_label_matrix_rows_digest": approval_service.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
    "source_feature_values_digest": approval_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
    "source_target_values_digest": approval_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "source_records_digest": approval_service.EXPECTED_SOURCE_RECORDS_DIGEST,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    approval: dict, field: str, expected: str
) -> None:
    assert approval[field] == expected
    assert len(approval[field]) == 64


def test_complete_upstream_digest_chain_is_preserved(
    approval: dict, source_review: dict
) -> None:
    assert approval["source_evidence"] == source_review["source_evidence"]
    assert len(approval["source_evidence"]) > 40


def test_build_accepts_exact_source_review(
    source_review: dict, attestation: dict, approval: dict
) -> None:
    rebuilt = approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        source_review=source_review, operator_attestation=attestation
    )
    assert rebuilt == approval


def test_build_rejects_changed_source_review(
    source_review: dict, attestation: dict
) -> None:
    changed = deepcopy(source_review)
    changed["marketflow_vpa_wyckoff_rule_baseline_candidate_operator_review_digest"] = "0" * 64
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            source_review=changed, operator_attestation=attestation
        )


def test_dataset_universe_and_meta_limitation_are_preserved(approval: dict) -> None:
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["records_digest"] == approval_service.EXPECTED_SOURCE_RECORDS_DIGEST
    assert approval["meta_reduced_record_count_preserved"] is True


def test_approved_and_supporting_packages(approval: dict) -> None:
    package = approval["approved_vpa_wyckoff_package"]
    supporting = approval["supporting_vpa_wyckoff_package"]
    assert package["approval_status"] == (
        "APPROVED_FOR_FUTURE_VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY"
    )
    assert package["selected_rule_family_count"] == 8
    assert package["selected_wyckoff_state_family_count"] == 6
    assert package["rule_execution_performed"] is False
    assert supporting["package_id"] == approval_service.SUPPORTING_VPA_WYCKOFF_PACKAGE
    assert supporting["approval_status"] == "AVAILABLE_NOT_SELECTED"


def test_approved_and_supporting_family_counts(approval: dict) -> None:
    assert [
        row["rule_family_id"]
        for row in approval["approved_vpa_wyckoff_rule_families"]
    ] == approval_service.SELECTED_RULE_FAMILY_IDS
    assert [
        row["state_family_id"]
        for row in approval["approved_wyckoff_state_families"]
    ] == approval_service.SELECTED_STATE_FAMILY_IDS
    assert len(approval["supporting_vpa_wyckoff_rule_families"]) == 2
    assert len(approval["supporting_wyckoff_state_families"]) == 2


def test_feature_mappings_questions_and_future_outputs(approval: dict) -> None:
    assert len(approval["approved_feature_group_mappings"]) == 13
    assert all(
        row["mapping_status"] == "PLANNED_NOT_EXECUTED"
        and row["target_values_used"] is False
        and row["future_data_used"] is False
        for row in approval["approved_feature_group_mappings"]
    )
    assert len(approval["approved_rule_design_questions"]) == 12
    assert all(
        row["question_status"] == "NOT_ANSWERED"
        for row in approval["approved_rule_design_questions"]
    )
    assert len(approval["approved_future_outputs"]) == 10
    assert all(
        row["approval_status"] == "AUTHORIZED_NOT_GENERATED"
        and row["output_status"] == "PLANNED_NOT_GENERATED"
        for row in approval["approved_future_outputs"]
    )


def test_planned_counts_and_per_ticker_approval(approval: dict) -> None:
    assert approval["planned_rule_value_rows"] == 179190
    assert approval["planned_rule_state_rows"] == 179190
    entries = approval["per_ticker_vpa_wyckoff_rule_baseline_approval_entries"]
    assert [row["ticker"] for row in entries] == approval_service.TARGET_UNIVERSE
    assert len(entries) == 12
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["planned_matrix_row_count"] == 13695
    assert meta["meta_reduced_record_count_flag"] is True
    assert all(
        len(row["per_ticker_vpa_wyckoff_rule_baseline_approval_digest"]) == 64
        for row in entries
    )


CLOSED_FIELDS = [
    "vpa_wyckoff_rule_baseline_executed",
    "vpa_wyckoff_rule_values_created",
    "vpa_wyckoff_state_values_created",
    "vpa_wyckoff_baseline_outputs_created",
    "expectancy_backtest_lab_candidate_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "runtime_migration_approved",
    "runtime_migration_active",
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "vpa_wyckoff_candidate_creation_rerun_performed",
    "vpa_wyckoff_candidate_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FIELDS)
def test_closed_boundary_field_remains_false(approval: dict, field: str) -> None:
    assert approval[field] is False


ATTESTATION_EXACT_FIELDS = [
    "operator_decision",
    "selected_vpa_wyckoff_package",
    "selected_matrix_package",
    "selected_matrix_layout",
    "selected_feature_package",
    "selected_label_target_package",
    "selected_objective_path",
    "operator_attestation_phrase",
    "operator_attestation_version",
    "operator_confirms_candidate_review_digest",
    "operator_confirms_candidate_digest",
    "operator_confirms_matrix_results_review_digest",
    "operator_confirms_matrix_rows_digest",
    "operator_confirms_feature_values_digest",
    "operator_confirms_target_values_digest",
    "operator_confirms_records_digest",
    "operator_confirms_target_universe",
    "operator_confirms_target_count",
    "operator_confirms_meta_record_count",
    "operator_confirms_non_meta_record_count",
    "operator_confirms_selected_vpa_wyckoff_package",
    "operator_confirms_selected_matrix_package",
    "operator_confirms_selected_matrix_layout",
    "operator_confirms_selected_feature_package",
    "operator_confirms_selected_label_target_package",
    "operator_confirms_selected_objective_path",
]


@pytest.mark.parametrize("field", ATTESTATION_EXACT_FIELDS)
def test_builder_rejects_incorrect_attestation_value(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = [] if field == "operator_confirms_target_universe" else "WRONG"
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize(
    "field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_closed_boundary_confirmation(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = False
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize(
    "field", ["operator_reference", "operator_attestation_timestamp_utc"]
)
def test_builder_rejects_missing_operator_metadata(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = ""
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            operator_attestation=invalid
        )


def test_next_chain_gates_risk_controls_and_checklist(approval: dict) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN
    assert approval["next_gates"] == approval_service.NEXT_GATES
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS
    assert [row["check_id"] for row in approval["approval_checklist"]] == (
        approval_service.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in approval["approval_checklist"]
    )
    assert approval["approval_summary"]["total_checks"] == len(
        approval_service.REQUIRED_CHECK_IDS
    )
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0


def test_approval_and_per_ticker_digests_are_deterministic(
    attestation: dict, approval: dict
) -> None:
    rebuilt = approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        operator_attestation=attestation
    )
    assert rebuilt == approval
    assert approval["marketflow_vpa_wyckoff_rule_baseline_approval_digest"] == (
        approval_service.marketflow_vpa_wyckoff_rule_baseline_approval_digest_v1(
            approval
        )
    )
    for entry in approval[
        "per_ticker_vpa_wyckoff_rule_baseline_approval_entries"
    ]:
        assert entry["per_ticker_vpa_wyckoff_rule_baseline_approval_digest"] == (
            approval_service.per_ticker_vpa_wyckoff_rule_baseline_approval_digest_v1(
                entry
            )
        )


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = approval_service.validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        approval
    )
    assert result["status"] == "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVAL_VALID"
    assert result["passed_checks"] == len(approval_service.REQUIRED_CHECK_IDS)
    assert result["failed_checks"] == 0


MUTATIONS = [
    ("wrong_artifact", lambda row: row.__setitem__("artifact_kind", "WRONG")),
    ("wrong_status", lambda row: row.__setitem__("approval_status", "WRONG")),
    ("wrong_scope", lambda row: row.__setitem__("approval_scope", "WRONG")),
    ("wrong_vpa_package", lambda row: row.__setitem__("selected_vpa_wyckoff_package", "WRONG")),
    ("wrong_matrix_package", lambda row: row.__setitem__("selected_matrix_package", "WRONG")),
    ("wrong_layout", lambda row: row.__setitem__("selected_matrix_layout", "WRONG")),
    ("wrong_feature_package", lambda row: row.__setitem__("selected_feature_package", "WRONG")),
    ("wrong_target_package", lambda row: row.__setitem__("selected_label_target_package", "WRONG")),
    ("wrong_objective", lambda row: row.__setitem__("selected_objective_path", "WRONG")),
    ("changed_review_digest", lambda row: row.__setitem__("source_vpa_wyckoff_rule_baseline_candidate_review_digest", "0" * 64)),
    ("changed_candidate_digest", lambda row: row.__setitem__("source_vpa_wyckoff_rule_baseline_candidate_digest", "0" * 64)),
    ("changed_matrix_review", lambda row: row.__setitem__("source_feature_label_matrix_results_review_digest", "0" * 64)),
    ("changed_matrix_rows", lambda row: row.__setitem__("source_feature_label_matrix_rows_digest", "0" * 64)),
    ("wrong_universe", lambda row: row.__setitem__("target_universe", list(reversed(row["target_universe"])))),
    ("wrong_count", lambda row: row.__setitem__("target_universe_count", 11)),
    ("wrong_records", lambda row: row.__setitem__("records_digest", "0" * 64)),
    ("wrong_meta", lambda row: row.__setitem__("meta_record_count", 1003)),
    ("decision", lambda row: row["operator_attestation"].__setitem__("operator_decision", "WRONG")),
    ("phrase", lambda row: row["operator_attestation"].__setitem__("operator_attestation_phrase", "WRONG")),
    ("not_authorized", lambda row: row.__setitem__("vpa_wyckoff_rule_baseline_authorized_for_future_execution", False)),
    ("approval_false", lambda row: row.__setitem__("vpa_wyckoff_rule_baseline_approval_created", False)),
    ("ready_false", lambda row: row.__setitem__("ready_for_vpa_wyckoff_rule_baseline_execution", False)),
    ("executed", lambda row: row.__setitem__("vpa_wyckoff_rule_baseline_executed", True)),
    ("rule_values", lambda row: row.__setitem__("vpa_wyckoff_rule_values_created", True)),
    ("state_values", lambda row: row.__setitem__("vpa_wyckoff_state_values_created", True)),
    ("outputs", lambda row: row.__setitem__("vpa_wyckoff_baseline_outputs_created", True)),
    ("lab_candidate", lambda row: row.__setitem__("expectancy_backtest_lab_candidate_created", True)),
    ("backtest", lambda row: row.__setitem__("backtest_execution_performed", True)),
    ("training", lambda row: row.__setitem__("model_training_performed", True)),
    ("metrics", lambda row: row.__setitem__("metric_computation_performed", True)),
    ("scoring", lambda row: row.__setitem__("strategy_scoring_performed", True)),
    ("usefulness", lambda row: row.__setitem__("predictive_usefulness", "accepted")),
    ("profitability", lambda row: row.__setitem__("profitability", "accepted")),
    ("runtime", lambda row: row.__setitem__("runtime_use", "AUTHORIZED")),
    ("strategy", lambda row: row.__setitem__("strategy_use", "AUTHORIZED")),
    ("paper", lambda row: row.__setitem__("paper_trading", "AUTHORIZED")),
    ("broker", lambda row: row.__setitem__("broker_execution", "AUTHORIZED")),
    ("recommendations", lambda row: row.__setitem__("trade_recommendations_generated", True)),
    ("provider", lambda row: row.__setitem__("provider_requests_made_in_approval", True)),
    ("acquisition", lambda row: row.__setitem__("market_data_acquisition_performed_in_approval", True)),
    ("regeneration", lambda row: row.__setitem__("canonical_dataset_regenerated_in_approval", True)),
    ("matrix_exec_rerun", lambda row: row.__setitem__("feature_label_matrix_execution_rerun_performed", True)),
    ("matrix_review_rerun", lambda row: row.__setitem__("feature_label_matrix_results_review_rerun_performed", True)),
    ("candidate_rerun", lambda row: row.__setitem__("vpa_wyckoff_candidate_creation_rerun_performed", True)),
    ("review_rerun", lambda row: row.__setitem__("vpa_wyckoff_candidate_review_rerun_performed", True)),
    ("missing_package", lambda row: row.pop("approved_vpa_wyckoff_package")),
    ("missing_rules", lambda row: row.pop("approved_vpa_wyckoff_rule_families")),
    ("missing_states", lambda row: row.pop("approved_wyckoff_state_families")),
    ("missing_mappings", lambda row: row.pop("approved_feature_group_mappings")),
    ("missing_outputs", lambda row: row.pop("approved_future_outputs")),
    ("missing_risks", lambda row: row.pop("risk_controls")),
    ("missing_digest", lambda row: row.pop("marketflow_vpa_wyckoff_rule_baseline_approval_digest")),
    ("missing_ticker_digest", lambda row: row["per_ticker_vpa_wyckoff_rule_baseline_approval_entries"][0].pop("per_ticker_vpa_wyckoff_rule_baseline_approval_digest")),
]


@pytest.mark.parametrize(("case", "mutate"), MUTATIONS, ids=[row[0] for row in MUTATIONS])
def test_validator_rejects_contract_mutation(
    approval: dict, case: str, mutate: object
) -> None:
    invalid = deepcopy(approval)
    mutate(invalid)
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.validate_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            invalid
        )


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_markdown_v1(
        approval
    )
    for section in (
        "VPA/Wyckoff Rule Baseline Approval v1",
        "Operator Attestation",
        "Source Candidate Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approval Scope",
        "Selected VPA/Wyckoff Package",
        "Selected Matrix and Feature Packages",
        "Approved Rule Families",
        "Approved Wyckoff State Families",
        "Supporting Package",
        "Approved Feature Group Mapping",
        "Design Questions",
        "Approved Future Outputs",
        "Planned Counts",
        "Per-Ticker Approval Summary",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert section in markdown


def test_writer_round_trip_and_refuses_overwrite(
    tmp_path, attestation: dict, approval: dict
) -> None:
    result = approval_service.write_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    json_path = tmp_path / "marketflow_vpa_wyckoff_rule_baseline_approval_v1.json"
    markdown_path = tmp_path / "marketflow_vpa_wyckoff_rule_baseline_approval_v1.md"
    assert result["json_path"] == str(json_path).replace("\\", "/")
    assert json_path.read_bytes() == canonical_json_bytes(approval)
    assert json.loads(json_path.read_text(encoding="utf-8")) == approval
    assert "VPA/Wyckoff Rule Baseline Approval v1" in markdown_path.read_text(
        encoding="utf-8"
    )
    with pytest.raises(approval_service.MarketFlowVpaWyckoffRuleBaselineApprovalError):
        approval_service.write_marketflow_vpa_wyckoff_rule_baseline_approval_v1(
            tmp_path, operator_attestation=attestation
        )


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED == (
        approval_service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED
    )
    assert services.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED == (
        approval_service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED
    )
    assert services.VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY == (
        approval_service.VPA_WYCKOFF_RULE_BASELINE_APPROVAL_ONLY
    )
    assert services.SELECTED_VPA_WYCKOFF_PACKAGE == (
        approval_service.SELECTED_VPA_WYCKOFF_PACKAGE
    )
    assert services.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1 is (
        approval_service.build_marketflow_vpa_wyckoff_rule_baseline_approval_v1
    )
