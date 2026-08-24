from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    marketflow_signal_or_feature_generation_candidate_operator_review_service as review_service,
)


@pytest.fixture(scope="module")
def source_candidate() -> dict:
    return review_service.candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()


@pytest.fixture(scope="module")
def review() -> dict:
    return review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1()


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["live_provider_transport_enabled_in_review"] is False
    assert review["target_generation_execution_rerun_performed"] is False
    assert review["target_generation_results_review_rerun_performed"] is False
    assert review["candidate_creation_rerun_performed"] is False


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    ),
    (
        "schema_version",
        "marketflow_signal_or_feature_generation_candidate_operator_review_v1",
    ),
    (
        "review_status",
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    ),
    (
        "review_scope",
        "SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    ),
    (
        "source_signal_or_feature_generation_candidate_artifact_kind",
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1",
    ),
    (
        "source_signal_or_feature_generation_candidate_status",
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    ),
    (
        "source_signal_or_feature_generation_candidate_scope",
        "SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION",
    ),
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
    ("target_profile_count", 15),
    ("target_row_count", 179190),
    ("available_target_row_count", 177090),
    ("unavailable_target_row_count", 2100),
    ("signal_or_feature_generation_candidate_created", True),
    ("signal_or_feature_generation_candidate_ready_for_operator_review", True),
    ("signal_or_feature_generation_candidate_review_created", True),
    ("signal_or_feature_generation_candidate_review_ready", True),
    ("ready_for_signal_or_feature_generation_approval", False),
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
    "source_signal_or_feature_generation_candidate_digest": review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_target_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    "source_target_generation_execution_digest": review_service.candidate_service.EXPECTED_SOURCE_EXECUTION_DIGEST,
    "source_target_values_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
    "marketflow_signal_or_feature_generation_candidate_v1_digest": review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    **review_service.SOURCE_EVIDENCE_DIGESTS,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    review: dict, field: str, expected: str
) -> None:
    assert review[field] == expected
    assert len(review[field]) == 64


def test_build_accepts_the_exact_source_candidate(
    source_candidate: dict, review: dict
) -> None:
    rebuilt = review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        source_candidate
    )
    assert rebuilt == review


def test_build_rejects_changed_source_candidate(source_candidate: dict) -> None:
    invalid = deepcopy(source_candidate)
    invalid["marketflow_signal_or_feature_generation_candidate_v1_digest"] = "0" * 64
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            invalid
        )


def test_target_universe_order_and_record_counts_are_preserved(review: dict) -> None:
    assert review["target_universe"] == review_service.TARGET_UNIVERSE
    assert review["per_ticker_record_counts"] == review_service.EXPECTED_RECORD_COUNTS
    assert review["meta_reduced_record_count_preserved"] is True
    assert review["records_digest"] == (
        "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
    )


def test_candidate_basis_and_philosophy_are_reviewed(review: dict) -> None:
    basis = review["reviewed_candidate_basis"]
    assert basis["selected_label_target_package"] == review_service.SELECTED_LABEL_TARGET_PACKAGE
    assert basis["selected_objective_path"] == review_service.SELECTED_OBJECTIVE_PATH
    assert basis["target_profile_count"] == 15
    assert basis["target_row_count"] == 179190
    assert basis["available_target_row_count"] == 177090
    assert basis["unavailable_target_row_count"] == 2100
    assert basis["source_target_values_digest"] == review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
    assert basis["review_status"] == "REVIEWED_CANDIDATE_BASIS"
    assert basis["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    philosophy = review["reviewed_candidate_philosophy"]
    assert philosophy["review_status"] == "REVIEWED_CANDIDATE_PHILOSOPHY"
    assert philosophy["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    assert "target values" in philosophy["candidate_philosophy"]
    assert "no-peek" in philosophy["candidate_secondary_question"]


def test_signal_families_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_signal_families"]
    assert [row["signal_family_id"] for row in rows] == review_service.candidate_service.SIGNAL_FAMILY_IDS
    assert len(rows) == 10
    for row in rows:
        assert row["review_status"] == "REVIEWED_SIGNAL_CANDIDATE_NOT_GENERATED"
        assert row["candidate_status"] == "SIGNAL_CANDIDATE_DEFINED_NOT_GENERATED"
        assert row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
        assert row["signal_generation_authorized"] is False
        assert row["feature_generation_authorized"] is False
        assert row["feature_values_created"] is False
        assert row["feature_label_matrix_created"] is False


def test_feature_families_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_feature_families"]
    assert [row["feature_family_id"] for row in rows] == review_service.candidate_service.FEATURE_FAMILY_IDS
    assert len(rows) == 10
    for row in rows:
        assert row["review_status"] == "REVIEWED_FEATURE_CANDIDATE_NOT_GENERATED"
        assert row["candidate_status"] == "FEATURE_CANDIDATE_DEFINED_NOT_GENERATED"
        assert row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
        assert row["feature_generation_authorized"] is False
        assert row["feature_values_created"] is False
        assert row["feature_label_matrix_created"] is False
        assert row["target_values_used_as_features"] is False
        assert row["future_data_used_as_features"] is False


def test_recommended_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_recommended_feature_package"]
    assert package["package_id"] == review_service.RECOMMENDED_PACKAGE_ID
    assert package["source_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert package["includes_signal_families"] == review_service.candidate_service.RECOMMENDED_SIGNAL_FAMILIES
    assert package["includes_feature_families"] == review_service.candidate_service.RECOMMENDED_FEATURE_FAMILIES
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_supporting_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_supporting_feature_package"]
    assert package["package_id"] == review_service.SUPPORTING_PACKAGE_ID
    assert package["source_status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == "REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED"
    assert package["includes_signal_families"] == review_service.candidate_service.SUPPORTING_SIGNAL_FAMILIES
    assert package["includes_feature_families"] == review_service.candidate_service.SUPPORTING_FEATURE_FAMILIES
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_feature_groups_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_feature_groups"]
    assert [row["feature_group_id"] for row in rows] == review_service.candidate_service.FEATURE_GROUP_IDS
    assert len(rows) == 17
    assert all(row["review_status"] == "REVIEWED_FEATURE_GROUP_CANDIDATE_NOT_GENERATED" for row in rows)
    assert all(row["group_status"] == "FEATURE_GROUP_CANDIDATE_NOT_GENERATED" for row in rows)
    assert all(row["target_values_used_as_features"] is False for row in rows)
    assert all(row["future_data_used_as_features"] is False for row in rows)


def test_no_peek_rules_are_reviewed_not_executed(review: dict) -> None:
    rows = review["reviewed_no_peek_and_target_separation_rules"]
    assert [row["rule_id"] for row in rows] == review_service.candidate_service.NO_PEEK_RULE_IDS
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_RULE_NOT_EXECUTED" for row in rows)
    assert all(row["rule_status"] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_quality_checks_are_reviewed_not_executed(review: dict) -> None:
    rows = review["reviewed_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_CHECK_NOT_EXECUTED" for row in rows)
    assert all(row["quality_check_status"] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_future_outputs_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_future_outputs"]
    assert [row["future_output_id"] for row in rows] == review_service.candidate_service.FUTURE_OUTPUT_IDS
    assert len(rows) == 10
    assert all(row["review_status"] == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED" for row in rows)
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["research_only"] is True for row in rows)
    assert all(row["non_actionable"] is True for row in rows)


def test_per_ticker_entries_preserve_target_counts(review: dict) -> None:
    entries = review["per_ticker_signal_or_feature_generation_candidate_review_entries"]
    assert [row["ticker"] for row in entries] == review_service.TARGET_UNIVERSE
    assert len(entries) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["target_row_count"] == (13695 if is_meta else 15045)
        assert row["available_target_row_count"] == (13520 if is_meta else 14870)
        assert row["unavailable_target_row_count"] == 175
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["source_signal_or_feature_generation_candidate_digest"] == review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
        assert row["source_target_results_review_digest"] == review_service.candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
        assert row["source_target_values_digest"] == review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
        assert row["per_ticker_signal_or_feature_generation_candidate_review_digest"] == review_service.per_ticker_signal_or_feature_generation_candidate_review_digest_v1(row)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["review_note"] == "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_REVIEW"


CLOSED_FALSE_FIELDS = [
    "ready_for_signal_or_feature_generation_approval",
    "signal_or_feature_generation_selected",
    "signal_or_feature_generation_approved",
    "signal_or_feature_generation_authorized",
    "signal_or_feature_generation_performed",
    "selection_created",
    "approval_created",
    "generation_created",
    "signal_generation_authorized",
    "signal_generation_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
    "feature_values_created",
    "feature_label_matrix_created",
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
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "candidate_creation_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_closed_authority_or_action_field_is_false(review: dict, field: str) -> None:
    assert review[field] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_authorities_are_not_authorized(
    review: dict, field: str
) -> None:
    assert review[field] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_exact(review: dict) -> None:
    assert review["next_chain"] == review_service.NEXT_CHAIN
    assert review["next_gates"] == review_service.NEXT_GATES
    assert review["next_chain"][0] == "Signal or Feature Generation Approval v1, if selected."


def test_risk_controls_are_exact(review: dict) -> None:
    assert review["risk_controls"] == review_service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 28


def test_checklist_passes(review: dict) -> None:
    checklist = review["review_checklist"]
    assert [row["check_id"] for row in checklist] == review_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    summary = review["review_summary"]
    assert summary["total_checks"] == len(review_service.REQUIRED_CHECK_IDS) == 83
    assert summary["passed_checks"] == 83
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_signal_or_feature_generation_approval"] is False
    assert summary["recommended_feature_package"] == review_service.RECOMMENDED_PACKAGE_ID


def test_review_digest_is_deterministic(review: dict) -> None:
    rebuilt = review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1()
    digest = review["marketflow_signal_or_feature_generation_candidate_operator_review_digest"]
    assert len(digest) == 64
    assert rebuilt == review
    assert review_service.marketflow_signal_or_feature_generation_candidate_operator_review_digest_v1(review) == digest


def test_per_ticker_digests_are_deterministic(review: dict) -> None:
    rebuilt = review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1()
    assert [row["per_ticker_signal_or_feature_generation_candidate_review_digest"] for row in rebuilt["per_ticker_signal_or_feature_generation_candidate_review_entries"]] == [
        row["per_ticker_signal_or_feature_generation_candidate_review_digest"]
        for row in review["per_ticker_signal_or_feature_generation_candidate_review_entries"]
    ]


def test_validator_accepts_valid_review(review: dict) -> None:
    result = review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(review)
    assert result["status"] == "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID"
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


INVALID_TOP_LEVEL_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("review_status", "WRONG"),
    ("review_scope", "WRONG"),
    ("source_signal_or_feature_generation_candidate_digest", "0" * 64),
    ("source_target_results_review_digest", "0" * 64),
    ("source_target_values_digest", "0" * 64),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("target_universe_count", 11),
    ("records_digest", "0" * 64),
    ("meta_record_count", 914),
    ("signal_or_feature_generation_candidate_review_created", False),
    ("signal_or_feature_generation_candidate_review_ready", False),
    ("ready_for_signal_or_feature_generation_approval", True),
    ("selection_created", True),
    ("approval_created", True),
    ("generation_created", True),
    ("signal_or_feature_generation_selected", True),
    ("signal_or_feature_generation_approved", True),
    ("signal_or_feature_generation_authorized", True),
    ("signal_or_feature_generation_performed", True),
    ("signal_generation_authorized", True),
    ("signal_generation_performed", True),
    ("feature_generation_authorized", True),
    ("feature_generation_performed", True),
    ("feature_values_created", True),
    ("feature_label_matrix_created", True),
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
    ("provider_requests_made_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
    ("target_generation_execution_rerun_performed", True),
    ("target_generation_results_review_rerun_performed", True),
    ("candidate_creation_rerun_performed", True),
]


@pytest.mark.parametrize(("field", "value"), INVALID_TOP_LEVEL_MUTATIONS)
def test_validator_rejects_invalid_top_level_mutation(
    review: dict, field: str, value: object
) -> None:
    invalid = deepcopy(review)
    invalid[field] = value
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            invalid
        )


INVALID_REMOVED_FIELDS = [
    "reviewed_candidate_philosophy",
    "reviewed_signal_families",
    "reviewed_feature_families",
    "reviewed_recommended_feature_package",
    "reviewed_supporting_feature_package",
    "reviewed_feature_groups",
    "reviewed_no_peek_and_target_separation_rules",
    "reviewed_quality_checks",
    "reviewed_future_outputs",
    "risk_controls",
    "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
]


@pytest.mark.parametrize("field", INVALID_REMOVED_FIELDS)
def test_validator_rejects_missing_required_field(review: dict, field: str) -> None:
    invalid = deepcopy(review)
    invalid.pop(field)
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            invalid
        )


def test_validator_rejects_target_universe_mismatch(review: dict) -> None:
    invalid = deepcopy(review)
    invalid["target_universe"] = list(reversed(invalid["target_universe"]))
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    invalid = deepcopy(review)
    invalid["per_ticker_signal_or_feature_generation_candidate_review_entries"][0].pop(
        "per_ticker_signal_or_feature_generation_candidate_review_digest"
    )
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            invalid
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_markdown_v1(review)
    required_sections = [
        "Title",
        "Signal or Feature Generation Candidate Operator Review v1",
        "Source Signal or Feature Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Reviewed Candidate Basis",
        "Reviewed Candidate Philosophy",
        "Reviewed Signal Families",
        "Reviewed Feature Families",
        "Reviewed Recommended Feature Package",
        "Reviewed Supporting Feature Package",
        "Reviewed Feature Groups",
        "Reviewed No-Peek and Target-Separation Rules",
        "Reviewed Quality Checks",
        "Reviewed Future Outputs",
        "Per-Ticker Review Summary",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in required_sections:
        assert f"## {section}" in markdown
    assert review["marketflow_signal_or_feature_generation_candidate_operator_review_digest"] in markdown


def test_writer_round_trip_is_canonical_and_isolated(
    tmp_path: Path, source_candidate: dict
) -> None:
    result = review_service.write_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        tmp_path, candidate=source_candidate
    )
    path = Path(result["path"])
    payload = path.read_bytes()
    written = json.loads(payload)
    assert path.parent == tmp_path
    assert payload == canonical_json_bytes(written)
    assert result["payload_sha256"] == sha256_bytes(payload)
    validation = review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        written
    )
    assert result["marketflow_signal_or_feature_generation_candidate_operator_review_digest"] == validation[
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest"
    ]


def test_writer_refuses_to_overwrite(tmp_path: Path) -> None:
    review_service.write_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        tmp_path
    )
    with pytest.raises(
        review_service.MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError
    ):
        review_service.write_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
            tmp_path
        )


def test_services_package_exports_operator_review_api() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE
    assert services.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY == review_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY
    assert services.SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL == review_service.SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL
    assert services.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1 is review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1
    assert services.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1 is review_service.validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1
    assert services.write_marketflow_signal_or_feature_generation_candidate_operator_review_v1 is review_service.write_marketflow_signal_or_feature_generation_candidate_operator_review_v1
    assert services.build_marketflow_signal_or_feature_generation_candidate_operator_review_markdown_v1 is review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_markdown_v1
