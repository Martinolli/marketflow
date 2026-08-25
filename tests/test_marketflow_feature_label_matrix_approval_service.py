from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import marketflow_feature_label_matrix_approval_service as approval_service


def _attestation() -> dict:
    return approval_service.build_marketflow_feature_label_matrix_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-25T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        operator_confirms_signal_feature_results_review_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        operator_confirms_feature_values_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        operator_confirms_target_results_review_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        operator_confirms_target_values_digest=approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        operator_confirms_records_digest=approval_service.BOUND_EVIDENCE["records_digest"],
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
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
    return approval_service.review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1()


@pytest.fixture(scope="module")
def approval(attestation: dict) -> dict:
    return approval_service.build_marketflow_feature_label_matrix_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == "APPROVE_FEATURE_LABEL_MATRIX"
    assert attestation["operator_attestation_phrase"] == approval_service.REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == "marketflow_feature_label_matrix_approval_operator_attestation_v1"
    assert all(attestation[field] is True for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approval_builds_offline(approval: dict) -> None:
    assert approval["created_offline"] is True
    assert approval["provider_requests_made_in_approval"] is False
    assert approval["live_provider_transport_enabled_in_approval"] is False
    assert approval["market_data_acquisition_performed_in_approval"] is False


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED"),
    ("schema_version", "marketflow_feature_label_matrix_approval_v1"),
    ("approval_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED"),
    ("approval_scope", "FEATURE_LABEL_MATRIX_APPROVAL_ONLY"),
    ("selected_matrix_package", "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX"),
    ("selected_matrix_layout", "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("source_feature_label_matrix_candidate_review_artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE"),
    ("source_feature_label_matrix_candidate_review_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"),
    ("source_feature_label_matrix_candidate_review_scope", "FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("planned_matrix_row_count", 179190),
    ("planned_available_matrix_row_count", 177090),
    ("planned_unavailable_target_row_count", 2100),
    ("planned_feature_group_count", 13),
    ("planned_target_profile_count", 15),
    ("planned_canonical_record_count", 11946),
    ("feature_label_matrix_candidate_created", True),
    ("feature_label_matrix_candidate_review_created", True),
    ("feature_label_matrix_candidate_review_ready", True),
    ("feature_label_matrix_selected", True),
    ("feature_label_matrix_approved", True),
    ("feature_label_matrix_authorized", True),
    ("feature_label_matrix_approval_created", True),
    ("ready_for_feature_label_matrix_execution", True),
    ("feature_label_matrix_authorized_for_future_execution", True),
    ("feature_label_matrix_created", False),
    ("feature_label_matrix_rows_created", False),
    ("joined_matrix_output_created", False),
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
    "source_feature_label_matrix_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_feature_label_matrix_candidate_digest": approval_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
    "source_signal_feature_results_review_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
    "source_signal_feature_execution_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
    "source_signal_feature_output_binding_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
    "source_feature_values_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
    "source_target_results_review_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
    "source_target_values_digest": approval_service.review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "source_records_digest": approval_service.BOUND_EVIDENCE["records_digest"],
    **approval_service.BOUND_EVIDENCE,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    approval: dict, field: str, expected: str
) -> None:
    assert approval[field] == expected
    assert len(approval[field]) == 64


def test_build_accepts_exact_source_review(
    source_review: dict, attestation: dict, approval: dict
) -> None:
    rebuilt = approval_service.build_marketflow_feature_label_matrix_approval_v1(
        source_review=source_review, operator_attestation=attestation
    )
    assert rebuilt == approval


def test_build_rejects_changed_source_review(
    source_review: dict, attestation: dict
) -> None:
    changed = deepcopy(source_review)
    changed["marketflow_feature_label_matrix_candidate_operator_review_digest"] = "0" * 64
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.build_marketflow_feature_label_matrix_approval_v1(
            source_review=changed, operator_attestation=attestation
        )


def test_dataset_universe_and_meta_limitation_are_preserved(approval: dict) -> None:
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["records_digest"] == approval_service.BOUND_EVIDENCE["records_digest"]
    assert approval["meta_reduced_record_count_preserved"] is True


def test_approved_matrix_package_is_future_execution_only(approval: dict) -> None:
    package = approval["approved_matrix_package"]
    assert package["package_id"] == approval_service.SELECTED_MATRIX_PACKAGE
    assert package["approval_status"] == "APPROVED_FOR_FUTURE_FEATURE_LABEL_MATRIX_EXECUTION_ONLY"
    assert package["selected_layout"] == approval_service.SELECTED_MATRIX_LAYOUT
    assert package["planned_matrix_row_count"] == 179190
    assert package["matrix_creation_performed"] is False
    assert package["matrix_rows_created"] is False
    assert package["joined_output_created"] is False


def test_supporting_layouts_are_available_not_selected(approval: dict) -> None:
    rows = approval["supporting_matrix_layouts"]
    assert [row["layout_id"] for row in rows] == [
        "MATRIX_LAYOUT_LONG_FEATURE_TARGET_AUDIT",
        "MATRIX_LAYOUT_CANONICAL_RECORD_FEATURE_BUNDLE",
    ]
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in rows)
    assert all(row["execution_performed"] is False for row in rows)


APPROVED_COLLECTIONS = [
    ("approved_matrix_alignment_keys", "alignment_key_id", approval_service.review_service.candidate_service.ALIGNMENT_KEY_IDS, "APPROVED_FOR_FUTURE_MATRIX_EXECUTION", "key_status"),
    ("approved_feature_side_join_rules", "feature_side_join_rule_id", approval_service.review_service.candidate_service.FEATURE_SIDE_JOIN_RULE_IDS, "APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL", "rule_status"),
    ("approved_target_side_join_rules", "target_side_join_rule_id", approval_service.review_service.candidate_service.TARGET_SIDE_JOIN_RULE_IDS, "APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL", "rule_status"),
    ("approved_matrix_quality_checks", "quality_check_id", approval_service.review_service.candidate_service.QUALITY_CHECK_IDS, "APPROVED_FOR_FUTURE_MATRIX_QUALITY_CONTROL", "quality_check_status"),
]


@pytest.mark.parametrize(
    ("field", "id_field", "ids", "approval_status", "status_field"),
    APPROVED_COLLECTIONS,
)
def test_control_collection_is_approved_but_unexecuted(
    approval: dict,
    field: str,
    id_field: str,
    ids: list[str],
    approval_status: str,
    status_field: str,
) -> None:
    rows = approval[field]
    assert [row[id_field] for row in rows] == ids
    assert all(row["approval_status"] == approval_status for row in rows)
    assert all(row[status_field] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_future_outputs_are_authorized_not_generated(approval: dict) -> None:
    rows = approval["approved_future_outputs"]
    assert [row["output_id"] for row in rows] == approval_service.review_service.candidate_service.FUTURE_OUTPUT_IDS
    assert all(row["approval_status"] == "AUTHORIZED_NOT_GENERATED" for row in rows)
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in rows)


def test_per_ticker_entries_are_complete_digest_bound_and_closed(approval: dict) -> None:
    rows = approval["per_ticker_feature_label_matrix_approval_entries"]
    assert [row["ticker"] for row in rows] == approval_service.TARGET_UNIVERSE
    for row in rows:
        assert row["per_ticker_feature_label_matrix_approval_digest"] == approval_service.per_ticker_feature_label_matrix_approval_digest_v1(row)
        assert row["feature_label_matrix_selected"] is True
        assert row["feature_label_matrix_approved"] is True
        assert row["feature_label_matrix_authorized"] is True
        assert row["feature_label_matrix_created"] is False
        assert row["feature_label_matrix_rows_created"] is False
        assert row["joined_matrix_output_created"] is False
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["planned_matrix_row_count"] == 13695
    assert meta["approval_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_APPROVAL"
    assert all(row["historical_record_count"] == 1003 for row in rows if row["ticker"] != "META")


FALSE_BOUNDARY_FIELDS = [
    "feature_label_matrix_created", "feature_label_matrix_rows_created",
    "feature_label_matrix_execution_performed", "joined_matrix_output_created",
    "backtest_execution_authorized", "backtest_execution_performed",
    "model_training_authorized", "model_training_performed",
    "metric_computation_authorized", "metric_computation_performed",
    "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended", "profitability_acceptance_ready",
    "profitability_acceptance_recommended", "runtime_migration_approved",
    "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
    "trade_recommendations_generated", "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval", "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval", "canonical_dataset_regenerated_in_approval",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "signal_feature_generation_execution_rerun_performed",
    "signal_feature_results_review_rerun_performed",
    "matrix_candidate_creation_rerun_performed", "matrix_candidate_review_rerun_performed",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", FALSE_BOUNDARY_FIELDS)
def test_execution_and_downstream_boundary_remains_false(
    approval: dict, field: str
) -> None:
    assert approval[field] is False


ATTESTATION_EXACT_FIELDS = [
    "operator_decision", "selected_matrix_package", "selected_matrix_layout",
    "selected_feature_package", "selected_label_target_package", "selected_objective_path",
    "operator_attestation_phrase", "operator_attestation_version",
    "operator_confirms_candidate_review_digest", "operator_confirms_candidate_digest",
    "operator_confirms_signal_feature_results_review_digest",
    "operator_confirms_feature_values_digest", "operator_confirms_target_results_review_digest",
    "operator_confirms_target_values_digest", "operator_confirms_records_digest",
    "operator_confirms_target_universe", "operator_confirms_target_count",
    "operator_confirms_meta_record_count", "operator_confirms_non_meta_record_count",
    "operator_confirms_selected_matrix_package", "operator_confirms_selected_matrix_layout",
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
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.build_marketflow_feature_label_matrix_approval_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize("field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)
def test_builder_rejects_missing_closed_boundary_confirmation(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = False
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.build_marketflow_feature_label_matrix_approval_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize("field", ["operator_reference", "operator_attestation_timestamp_utc"])
def test_builder_rejects_missing_operator_metadata(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = ""
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.build_marketflow_feature_label_matrix_approval_v1(
            operator_attestation=invalid
        )


def test_next_chain_gates_risk_controls_and_checklist(approval: dict) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN
    assert approval["next_gates"] == approval_service.NEXT_GATES
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS
    assert [row["check_id"] for row in approval["approval_checklist"]] == approval_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["approval_checklist"])
    assert approval["approval_summary"]["total_checks"] == len(approval_service.REQUIRED_CHECK_IDS)
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0


def test_approval_and_per_ticker_digests_are_deterministic(
    attestation: dict, approval: dict
) -> None:
    rebuilt = approval_service.build_marketflow_feature_label_matrix_approval_v1(
        operator_attestation=attestation
    )
    assert rebuilt == approval
    assert approval["marketflow_feature_label_matrix_approval_digest"] == approval_service.marketflow_feature_label_matrix_approval_digest_v1(approval)


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = approval_service.validate_marketflow_feature_label_matrix_approval_v1(approval)
    assert result["status"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_VALID"
    assert result["passed_checks"] == len(approval_service.REQUIRED_CHECK_IDS)
    assert result["failed_checks"] == 0


MUTATIONS = [
    ("wrong_artifact", lambda row: row.__setitem__("artifact_kind", "WRONG")),
    ("wrong_status", lambda row: row.__setitem__("approval_status", "WRONG")),
    ("wrong_scope", lambda row: row.__setitem__("approval_scope", "WRONG")),
    ("wrong_matrix_package", lambda row: row.__setitem__("selected_matrix_package", "WRONG")),
    ("wrong_layout", lambda row: row.__setitem__("selected_matrix_layout", "WRONG")),
    ("wrong_feature_package", lambda row: row.__setitem__("selected_feature_package", "WRONG")),
    ("wrong_target_package", lambda row: row.__setitem__("selected_label_target_package", "WRONG")),
    ("wrong_objective", lambda row: row.__setitem__("selected_objective_path", "WRONG")),
    ("changed_review_digest", lambda row: row.__setitem__("source_feature_label_matrix_candidate_review_digest", "0" * 64)),
    ("changed_candidate_digest", lambda row: row.__setitem__("source_feature_label_matrix_candidate_digest", "0" * 64)),
    ("changed_feature_values", lambda row: row.__setitem__("source_feature_values_digest", "0" * 64)),
    ("changed_target_values", lambda row: row.__setitem__("source_target_values_digest", "0" * 64)),
    ("wrong_universe", lambda row: row.__setitem__("target_universe", list(reversed(row["target_universe"])))),
    ("wrong_count", lambda row: row.__setitem__("target_universe_count", 11)),
    ("wrong_records", lambda row: row.__setitem__("records_digest", "0" * 64)),
    ("wrong_meta", lambda row: row.__setitem__("meta_record_count", 1003)),
    ("decision", lambda row: row["operator_attestation"].__setitem__("operator_decision", "WRONG")),
    ("phrase", lambda row: row["operator_attestation"].__setitem__("operator_attestation_phrase", "WRONG")),
    ("not_authorized", lambda row: row.__setitem__("feature_label_matrix_authorized_for_future_execution", False)),
    ("approval_false", lambda row: row.__setitem__("feature_label_matrix_approval_created", False)),
    ("ready_false", lambda row: row.__setitem__("ready_for_feature_label_matrix_execution", False)),
    ("matrix_created", lambda row: row.__setitem__("feature_label_matrix_created", True)),
    ("rows_created", lambda row: row.__setitem__("feature_label_matrix_rows_created", True)),
    ("joined_created", lambda row: row.__setitem__("joined_matrix_output_created", True)),
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
    ("target_exec_rerun", lambda row: row.__setitem__("target_generation_execution_rerun_performed", True)),
    ("target_review_rerun", lambda row: row.__setitem__("target_generation_results_review_rerun_performed", True)),
    ("feature_exec_rerun", lambda row: row.__setitem__("signal_feature_generation_execution_rerun_performed", True)),
    ("feature_review_rerun", lambda row: row.__setitem__("signal_feature_results_review_rerun_performed", True)),
    ("candidate_rerun", lambda row: row.__setitem__("matrix_candidate_creation_rerun_performed", True)),
    ("review_rerun", lambda row: row.__setitem__("matrix_candidate_review_rerun_performed", True)),
    ("missing_package", lambda row: row.pop("approved_matrix_package")),
    ("missing_keys", lambda row: row.pop("approved_matrix_alignment_keys")),
    ("missing_feature_rules", lambda row: row.pop("approved_feature_side_join_rules")),
    ("missing_target_rules", lambda row: row.pop("approved_target_side_join_rules")),
    ("missing_checks", lambda row: row.pop("approved_matrix_quality_checks")),
    ("missing_outputs", lambda row: row.pop("approved_future_outputs")),
    ("missing_risks", lambda row: row.pop("risk_controls")),
    ("missing_digest", lambda row: row.pop("marketflow_feature_label_matrix_approval_digest")),
    ("missing_ticker_digest", lambda row: row["per_ticker_feature_label_matrix_approval_entries"][0].pop("per_ticker_feature_label_matrix_approval_digest")),
]


@pytest.mark.parametrize(("case", "mutate"), MUTATIONS, ids=[row[0] for row in MUTATIONS])
def test_validator_rejects_contract_mutation(
    approval: dict, case: str, mutate: object
) -> None:
    invalid = deepcopy(approval)
    mutate(invalid)
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.validate_marketflow_feature_label_matrix_approval_v1(invalid)


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = approval_service.build_marketflow_feature_label_matrix_approval_markdown_v1(approval)
    for section in (
        "Feature-Label Matrix Approval v1", "Operator Attestation",
        "Source Matrix Candidate Review", "Bound Evidence", "Dataset and Universe",
        "Approval Scope", "Selected Matrix Package", "Selected Matrix Layout",
        "Selected Feature and Target Packages", "Approved Matrix Counts",
        "Approved Alignment Keys", "Approved Feature-Side Join Rules",
        "Approved Target-Side Join Rules", "Approved Matrix Quality Checks",
        "Approved Future Outputs", "Per-Ticker Approval Summary", "Next Chain",
        "Next Gates", "Risk Controls", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_writer_round_trip_and_refuses_overwrite(
    tmp_path, attestation: dict, approval: dict
) -> None:
    result = approval_service.write_marketflow_feature_label_matrix_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    json_path = tmp_path / "marketflow_feature_label_matrix_approval_v1.json"
    markdown_path = tmp_path / "marketflow_feature_label_matrix_approval_v1.md"
    assert result["json_path"] == str(json_path).replace("\\", "/")
    assert json_path.read_bytes() == canonical_json_bytes(approval)
    assert json.loads(json_path.read_text(encoding="utf-8")) == approval
    assert "Feature-Label Matrix Approval v1" in markdown_path.read_text(encoding="utf-8")
    with pytest.raises(approval_service.MarketFlowFeatureLabelMatrixApprovalError):
        approval_service.write_marketflow_feature_label_matrix_approval_v1(
            tmp_path, operator_attestation=attestation
        )


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED == approval_service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED
    assert services.MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED == approval_service.MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED
    assert services.FEATURE_LABEL_MATRIX_APPROVAL_ONLY == approval_service.FEATURE_LABEL_MATRIX_APPROVAL_ONLY
    assert services.SELECTED_MATRIX_PACKAGE == approval_service.SELECTED_MATRIX_PACKAGE
    assert services.SELECTED_MATRIX_LAYOUT == approval_service.SELECTED_MATRIX_LAYOUT
    assert services.build_marketflow_feature_label_matrix_approval_v1 is approval_service.build_marketflow_feature_label_matrix_approval_v1
