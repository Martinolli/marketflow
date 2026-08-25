from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import (
    marketflow_feature_label_matrix_candidate_operator_review_service as review_service,
)


@pytest.fixture(scope="module")
def source_candidate() -> dict:
    return review_service.candidate_service.build_marketflow_feature_label_matrix_candidate_v1()


@pytest.fixture(scope="module")
def review() -> dict:
    return review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1()


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["live_provider_transport_enabled_in_review"] is False
    assert review["matrix_candidate_creation_rerun_performed"] is False


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE"),
    ("schema_version", "marketflow_feature_label_matrix_candidate_operator_review_v1"),
    ("review_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"),
    ("review_scope", "FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"),
    ("source_feature_label_matrix_candidate_artifact_kind", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1"),
    ("source_feature_label_matrix_candidate_status", "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW"),
    ("source_feature_label_matrix_candidate_scope", "FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    ("selected_label_target_package", "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("feature_row_count", 155298),
    ("available_feature_row_count", 155142),
    ("unavailable_feature_row_count", 156),
    ("target_row_count", 179190),
    ("available_target_row_count", 177090),
    ("unavailable_target_row_count", 2100),
    ("selected_feature_group_count", 13),
    ("target_profile_count", 15),
    ("planned_matrix_row_count", 179190),
    ("planned_available_matrix_row_count", 177090),
    ("planned_unavailable_target_row_count", 2100),
    ("planned_feature_group_count", 13),
    ("planned_target_profile_count", 15),
    ("planned_canonical_record_count", 11946),
    ("feature_label_matrix_candidate_created", True),
    ("feature_label_matrix_candidate_ready_for_operator_review", True),
    ("feature_label_matrix_candidate_review_created", True),
    ("feature_label_matrix_candidate_review_ready", True),
    ("ready_for_feature_label_matrix_approval", False),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


BOUND_DIGESTS = {
    "source_feature_label_matrix_candidate_digest": review_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
    "marketflow_feature_label_matrix_candidate_v1_digest": review_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
    "source_signal_feature_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
    "source_signal_feature_execution_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
    "source_signal_feature_output_binding_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
    "source_feature_values_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
    "source_target_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
    "source_target_values_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    **review_service.BOUND_EVIDENCE,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    review: dict, field: str, expected: str
) -> None:
    assert review[field] == expected
    assert len(review[field]) == 64


def test_build_accepts_exact_source_candidate(
    source_candidate: dict, review: dict
) -> None:
    assert review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1(
        source_candidate
    ) == review


def test_build_rejects_changed_source_candidate(source_candidate: dict) -> None:
    changed = deepcopy(source_candidate)
    changed["marketflow_feature_label_matrix_candidate_v1_digest"] = "0" * 64
    with pytest.raises(
        review_service.MarketFlowFeatureLabelMatrixCandidateOperatorReviewError
    ):
        review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1(
            changed
        )


def test_universe_order_and_meta_limitation_are_preserved(review: dict) -> None:
    assert review["target_universe"] == review_service.TARGET_UNIVERSE
    assert review["records_digest"] == review_service.BOUND_EVIDENCE["records_digest"]
    assert review["meta_reduced_record_count_preserved"] is True


def test_candidate_basis_and_philosophy_are_reviewed(review: dict) -> None:
    basis = review["reviewed_candidate_basis"]
    assert basis["recommended_matrix_package"] == review_service.RECOMMENDED_MATRIX_PACKAGE
    assert basis["feature_row_count"] == 155298
    assert basis["target_row_count"] == 179190
    assert basis["review_status"] == "REVIEWED_MATRIX_CANDIDATE_BASIS"
    assert basis["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    philosophy = review["reviewed_candidate_philosophy"]
    assert philosophy["review_status"] == "REVIEWED_MATRIX_CANDIDATE_PHILOSOPHY"
    assert philosophy["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    assert "history-only" in philosophy["candidate_philosophy"]
    assert "no-peek" in philosophy["candidate_primary_question"]


def test_matrix_layouts_are_reviewed_not_selected(review: dict) -> None:
    layouts = review["reviewed_matrix_layouts"]
    assert [row["layout_id"] for row in layouts] == [row["layout_id"] for row in review_service.candidate_service.MATRIX_LAYOUTS]
    assert layouts[0]["review_status"] == "REVIEWED_RECOMMENDED_LAYOUT_NOT_SELECTED"
    assert all(row["selection_created"] is False for row in layouts)
    assert layouts[1]["planned_long_audit_pair_count"] == 2329470
    assert layouts[2]["planned_canonical_feature_bundle_count"] == 11946


def test_recommended_package_is_reviewed_not_selected(review: dict) -> None:
    package = review["reviewed_recommended_matrix_package"]
    assert package["package_id"] == review_service.RECOMMENDED_MATRIX_PACKAGE
    assert package["source_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["execution_created"] is False


REVIEWED_COLLECTIONS = [
    ("reviewed_matrix_alignment_keys", "alignment_key_id", review_service.candidate_service.ALIGNMENT_KEY_IDS, "REVIEWED_PLANNED_KEY_NOT_EXECUTED"),
    ("reviewed_feature_side_join_rules", "feature_side_join_rule_id", review_service.candidate_service.FEATURE_SIDE_JOIN_RULE_IDS, "REVIEWED_PLANNED_FEATURE_JOIN_RULE_NOT_EXECUTED"),
    ("reviewed_target_side_join_rules", "target_side_join_rule_id", review_service.candidate_service.TARGET_SIDE_JOIN_RULE_IDS, "REVIEWED_PLANNED_TARGET_JOIN_RULE_NOT_EXECUTED"),
    ("reviewed_matrix_quality_checks", "quality_check_id", review_service.candidate_service.QUALITY_CHECK_IDS, "REVIEWED_PLANNED_MATRIX_QUALITY_CHECK_NOT_EXECUTED"),
    ("reviewed_planned_matrix_outputs", "output_id", review_service.candidate_service.FUTURE_OUTPUT_IDS, "REVIEWED_PLANNED_MATRIX_OUTPUT_NOT_GENERATED"),
]


@pytest.mark.parametrize(
    ("field", "id_field", "expected_ids", "review_status"), REVIEWED_COLLECTIONS
)
def test_candidate_collection_is_reviewed_not_executed(
    review: dict,
    field: str,
    id_field: str,
    expected_ids: list[str],
    review_status: str,
) -> None:
    rows = review[field]
    assert [row[id_field] for row in rows] == expected_ids
    assert all(row["review_status"] == review_status for row in rows)


def test_future_outputs_remain_not_generated(review: dict) -> None:
    for row in review["reviewed_planned_matrix_outputs"]:
        assert row["output_status"] == "PLANNED_NOT_GENERATED"
        assert row["research_only"] is True
        assert row["non_actionable"] is True


def test_per_ticker_entries_and_digests(review: dict) -> None:
    rows = review["per_ticker_feature_label_matrix_candidate_review_entries"]
    assert [row["ticker"] for row in rows] == review_service.TARGET_UNIVERSE
    for row in rows:
        assert row["per_ticker_feature_label_matrix_candidate_review_digest"] == (
            review_service.per_ticker_feature_label_matrix_candidate_review_digest_v1(row)
        )
        assert row["feature_label_matrix_selected"] is False
        assert row["feature_label_matrix_approved"] is False
        assert row["feature_label_matrix_authorized"] is False
        assert row["feature_label_matrix_created"] is False
        assert row["feature_label_matrix_rows_created"] is False
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["planned_matrix_row_count"] == 13695
    assert meta["planned_available_matrix_row_count"] == 13520
    assert meta["review_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_CANDIDATE_REVIEW"
    non_meta = [row for row in rows if row["ticker"] != "META"]
    assert all(row["historical_record_count"] == 1003 for row in non_meta)
    assert all(row["planned_matrix_row_count"] == 15045 for row in non_meta)


FALSE_BOUNDARY_FIELDS = [
    "feature_label_matrix_selected", "feature_label_matrix_approved",
    "feature_label_matrix_authorized", "feature_label_matrix_created",
    "feature_label_matrix_rows_created", "feature_label_matrix_execution_performed",
    "selection_created", "approval_created", "creation_created", "execution_created",
    "generation_created", "backtest_execution_authorized", "backtest_execution_performed",
    "model_training_authorized", "model_training_performed",
    "metric_computation_authorized", "metric_computation_performed",
    "strategy_scoring_performed", "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended", "profitability_acceptance_ready",
    "profitability_acceptance_recommended", "runtime_migration_approved",
    "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
    "trade_recommendations_generated", "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review", "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review", "canonical_dataset_regenerated_in_review",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "signal_feature_generation_execution_rerun_performed",
    "signal_feature_results_review_rerun_performed",
    "matrix_candidate_creation_rerun_performed", "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", FALSE_BOUNDARY_FIELDS)
def test_authority_and_execution_boundary_remains_false(
    review: dict, field: str
) -> None:
    assert review[field] is False


def test_next_chain_gates_risk_controls_and_checklist(review: dict) -> None:
    assert review["next_chain"] == review_service.NEXT_CHAIN
    assert review["next_gates"] == review_service.NEXT_GATES
    assert review["risk_controls"] == review_service.RISK_CONTROLS
    assert [row["check_id"] for row in review["review_checklist"]] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["review_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["review_checklist"])
    assert review["review_summary"]["total_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0
    assert review["review_summary"]["ready_for_feature_label_matrix_approval"] is False


def test_review_and_per_ticker_digests_are_deterministic(review: dict) -> None:
    rebuilt = review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1()
    assert rebuilt == review
    assert review["marketflow_feature_label_matrix_candidate_operator_review_digest"] == review_service.marketflow_feature_label_matrix_candidate_operator_review_digest_v1(review)


def test_validator_accepts_valid_review(review: dict) -> None:
    result = review_service.validate_marketflow_feature_label_matrix_candidate_operator_review_v1(review)
    assert result["status"] == "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_VALID"
    assert result["passed_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert result["failed_checks"] == 0


MUTATIONS = [
    ("wrong_artifact_kind", lambda row: row.__setitem__("artifact_kind", "WRONG")),
    ("wrong_status", lambda row: row.__setitem__("review_status", "WRONG")),
    ("wrong_scope", lambda row: row.__setitem__("review_scope", "WRONG")),
    ("changed_candidate_digest", lambda row: row.__setitem__("source_feature_label_matrix_candidate_digest", "0" * 64)),
    ("changed_feature_review_digest", lambda row: row.__setitem__("source_signal_feature_results_review_digest", "0" * 64)),
    ("changed_feature_values_digest", lambda row: row.__setitem__("source_feature_values_digest", "0" * 64)),
    ("changed_target_values_digest", lambda row: row.__setitem__("source_target_values_digest", "0" * 64)),
    ("wrong_feature_package", lambda row: row.__setitem__("selected_feature_package", "WRONG")),
    ("wrong_target_package", lambda row: row.__setitem__("selected_label_target_package", "WRONG")),
    ("wrong_objective", lambda row: row.__setitem__("selected_objective_path", "WRONG")),
    ("wrong_universe", lambda row: row.__setitem__("target_universe", list(reversed(row["target_universe"])))),
    ("wrong_target_count", lambda row: row.__setitem__("target_universe_count", 11)),
    ("wrong_records_digest", lambda row: row.__setitem__("records_digest", "0" * 64)),
    ("wrong_meta_count", lambda row: row.__setitem__("meta_record_count", 1003)),
    ("review_created_false", lambda row: row.__setitem__("feature_label_matrix_candidate_review_created", False)),
    ("review_ready_false", lambda row: row.__setitem__("feature_label_matrix_candidate_review_ready", False)),
    ("ready_for_approval_true", lambda row: row.__setitem__("ready_for_feature_label_matrix_approval", True)),
    ("missing_package_review", lambda row: row.pop("reviewed_recommended_matrix_package")),
    ("missing_layout_review", lambda row: row.pop("reviewed_matrix_layouts")),
    ("missing_key_review", lambda row: row.pop("reviewed_matrix_alignment_keys")),
    ("missing_feature_join_review", lambda row: row.pop("reviewed_feature_side_join_rules")),
    ("missing_target_join_review", lambda row: row.pop("reviewed_target_side_join_rules")),
    ("missing_quality_review", lambda row: row.pop("reviewed_matrix_quality_checks")),
    ("selection_true", lambda row: row.__setitem__("selection_created", True)),
    ("approval_true", lambda row: row.__setitem__("approval_created", True)),
    ("execution_true", lambda row: row.__setitem__("execution_created", True)),
    ("matrix_selected", lambda row: row.__setitem__("feature_label_matrix_selected", True)),
    ("matrix_approved", lambda row: row.__setitem__("feature_label_matrix_approved", True)),
    ("matrix_authorized", lambda row: row.__setitem__("feature_label_matrix_authorized", True)),
    ("matrix_created", lambda row: row.__setitem__("feature_label_matrix_created", True)),
    ("matrix_rows_created", lambda row: row.__setitem__("feature_label_matrix_rows_created", True)),
    ("backtest_true", lambda row: row.__setitem__("backtest_execution_performed", True)),
    ("training_true", lambda row: row.__setitem__("model_training_performed", True)),
    ("metrics_true", lambda row: row.__setitem__("metric_computation_performed", True)),
    ("scoring_true", lambda row: row.__setitem__("strategy_scoring_performed", True)),
    ("usefulness_accepted", lambda row: row.__setitem__("predictive_usefulness", "accepted")),
    ("profitability_accepted", lambda row: row.__setitem__("profitability", "accepted")),
    ("runtime_authorized", lambda row: row.__setitem__("runtime_use", "AUTHORIZED")),
    ("strategy_authorized", lambda row: row.__setitem__("strategy_use", "AUTHORIZED")),
    ("paper_authorized", lambda row: row.__setitem__("paper_trading", "AUTHORIZED")),
    ("broker_authorized", lambda row: row.__setitem__("broker_execution", "AUTHORIZED")),
    ("recommendations_true", lambda row: row.__setitem__("trade_recommendations_generated", True)),
    ("provider_true", lambda row: row.__setitem__("provider_requests_made_in_review", True)),
    ("acquisition_true", lambda row: row.__setitem__("market_data_acquisition_performed_in_review", True)),
    ("regeneration_true", lambda row: row.__setitem__("canonical_dataset_regenerated_in_review", True)),
    ("target_execution_rerun", lambda row: row.__setitem__("target_generation_execution_rerun_performed", True)),
    ("target_review_rerun", lambda row: row.__setitem__("target_generation_results_review_rerun_performed", True)),
    ("feature_execution_rerun", lambda row: row.__setitem__("signal_feature_generation_execution_rerun_performed", True)),
    ("feature_review_rerun", lambda row: row.__setitem__("signal_feature_results_review_rerun_performed", True)),
    ("candidate_rerun", lambda row: row.__setitem__("matrix_candidate_creation_rerun_performed", True)),
    ("missing_outputs", lambda row: row.pop("reviewed_planned_matrix_outputs")),
    ("missing_risks", lambda row: row.pop("risk_controls")),
    ("missing_digest", lambda row: row.pop("marketflow_feature_label_matrix_candidate_operator_review_digest")),
    ("missing_per_ticker_digest", lambda row: row["per_ticker_feature_label_matrix_candidate_review_entries"][0].pop("per_ticker_feature_label_matrix_candidate_review_digest")),
]


@pytest.mark.parametrize(("case", "mutate"), MUTATIONS, ids=[row[0] for row in MUTATIONS])
def test_validator_rejects_contract_mutation(
    review: dict, case: str, mutate: object
) -> None:
    invalid = deepcopy(review)
    mutate(invalid)
    with pytest.raises(
        review_service.MarketFlowFeatureLabelMatrixCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_feature_label_matrix_candidate_operator_review_v1(
            invalid
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = review_service.build_marketflow_feature_label_matrix_candidate_operator_review_markdown_v1(review)
    for section in (
        "Feature-Label Matrix Candidate Operator Review v1",
        "Source Feature-Label Matrix Candidate",
        "Source Signal or Feature Results Review",
        "Source Target Results Review",
        "Bound Evidence", "Dataset and Universe", "Reviewed Candidate Basis",
        "Reviewed Candidate Philosophy", "Reviewed Matrix Layouts",
        "Reviewed Recommended Matrix Package", "Reviewed Alignment Keys",
        "Reviewed Feature-Side Join Rules", "Reviewed Target-Side Join Rules",
        "Reviewed Matrix Quality Checks", "Reviewed Planned Outputs",
        "Per-Ticker Review Summary", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert section in markdown


def test_writer_round_trip_and_refuses_overwrite(tmp_path, review: dict) -> None:
    result = review_service.write_marketflow_feature_label_matrix_candidate_operator_review_v1(tmp_path)
    json_path = tmp_path / "marketflow_feature_label_matrix_candidate_operator_review_v1.json"
    markdown_path = tmp_path / "marketflow_feature_label_matrix_candidate_operator_review_v1.md"
    assert result["json_path"] == str(json_path).replace("\\", "/")
    assert json_path.read_bytes() == canonical_json_bytes(review)
    assert json.loads(json_path.read_text(encoding="utf-8")) == review
    assert "Feature-Label Matrix Candidate Operator Review v1" in markdown_path.read_text(encoding="utf-8")
    with pytest.raises(
        review_service.MarketFlowFeatureLabelMatrixCandidateOperatorReviewError
    ):
        review_service.write_marketflow_feature_label_matrix_candidate_operator_review_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE
    assert services.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY == review_service.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY
    assert services.FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL == review_service.FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL
    assert services.build_marketflow_feature_label_matrix_candidate_operator_review_v1 is review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1
