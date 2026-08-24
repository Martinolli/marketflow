from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow import services
from marketflow.services import (
    marketflow_signal_or_feature_generation_candidate_service as candidate_service,
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()


def test_candidate_builds_offline(candidate: dict) -> None:
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False
    assert candidate["live_provider_transport_enabled_in_candidate"] is False
    assert candidate["market_data_acquisition_performed_in_candidate"] is False
    assert candidate["target_generation_execution_rerun_performed"] is False
    assert candidate["target_generation_results_review_rerun_performed"] is False


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1"),
    ("schema_version", "marketflow_signal_or_feature_generation_candidate_v1"),
    (
        "candidate_status",
        "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    ),
    (
        "candidate_scope",
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
    ("target_results_review_ready", True),
    ("ready_for_signal_or_feature_generation_candidate", True),
    ("signal_or_feature_generation_candidate_created", True),
    ("signal_or_feature_generation_candidate_ready_for_operator_review", True),
    ("ready_for_signal_or_feature_generation_candidate_operator_review", True),
    ("target_profile_count", 15),
    ("target_row_count", 179190),
    ("available_target_row_count", 177090),
    ("unavailable_target_row_count", 2100),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("strategy_use", "NOT_AUTHORIZED"),
    ("paper_trading", "NOT_AUTHORIZED"),
    ("broker_execution", "NOT_AUTHORIZED"),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    list(candidate_service.SOURCE_EVIDENCE_DIGESTS.items()),
)
def test_required_source_digest_is_bound(
    candidate: dict, field: str, expected: str
) -> None:
    assert candidate[field] == expected
    assert len(candidate[field]) == 64


def test_source_target_review_contract_is_bound(candidate: dict) -> None:
    assert candidate[
        "source_objective_label_or_target_generation_results_review_artifact_kind"
    ] == "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE"
    assert candidate[
        "source_objective_label_or_target_generation_results_review_status"
    ] == "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE_READY"
    assert candidate[
        "source_objective_label_or_target_generation_results_review_scope"
    ] == "OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_GENERATION_NOT_BACKTEST"
    assert candidate[
        "source_objective_label_or_target_generation_results_review_digest"
    ] == candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
    assert candidate[
        "source_objective_label_or_target_generation_execution_digest"
    ] == candidate_service.EXPECTED_SOURCE_EXECUTION_DIGEST
    assert candidate[
        "source_objective_label_or_target_generation_output_binding_digest"
    ] == candidate_service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST
    assert candidate[
        "source_objective_label_or_target_values_digest"
    ] == candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST


def test_target_universe_order_and_record_counts_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE
    assert candidate["per_ticker_record_counts"] == candidate_service.EXPECTED_RECORD_COUNTS
    assert candidate["meta_reduced_record_count_preserved"] is True
    assert candidate["records_digest"] == (
        "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
    )


@pytest.mark.parametrize(
    "field",
    [
        "candidate_philosophy",
        "candidate_primary_question",
        "candidate_secondary_question",
        "candidate_boundary",
    ],
)
def test_candidate_philosophy_is_defined(candidate: dict, field: str) -> None:
    assert isinstance(candidate[field], str)
    assert candidate[field]


def test_signal_families_are_candidate_only(candidate: dict) -> None:
    rows = candidate["proposed_signal_families"]
    assert [row["signal_family_id"] for row in rows] == candidate_service.SIGNAL_FAMILY_IDS
    assert len(rows) == 10
    for row in rows:
        assert row["candidate_status"] == "SIGNAL_CANDIDATE_DEFINED_NOT_GENERATED"
        assert row["operator_review_required"] is True
        assert row["approval_required_before_generation"] is True
        assert row["signal_generation_authorized"] is False
        assert row["feature_generation_authorized"] is False
        assert row["feature_values_created"] is False
        assert row["feature_label_matrix_created"] is False
        assert row["metric_computation_authorized"] is False
        assert row["backtest_authorized"] is False
        assert row["model_training_authorized"] is False
        assert row["research_only"] is True
        assert row["non_actionable"] is True


def test_feature_families_are_candidate_only(candidate: dict) -> None:
    rows = candidate["proposed_feature_families"]
    assert [row["feature_family_id"] for row in rows] == candidate_service.FEATURE_FAMILY_IDS
    assert len(rows) == 10
    for row in rows:
        assert row["candidate_status"] == "FEATURE_CANDIDATE_DEFINED_NOT_GENERATED"
        assert row["operator_review_required"] is True
        assert row["approval_required_before_generation"] is True
        assert row["feature_generation_authorized"] is False
        assert row["feature_values_created"] is False
        assert row["feature_label_matrix_created"] is False
        assert row["target_values_used_as_features"] is False
        assert row["future_data_used_as_features"] is False
        assert row["research_only"] is True
        assert row["non_actionable"] is True


def test_recommended_feature_package_is_defined_not_selected(candidate: dict) -> None:
    package = candidate["recommended_feature_package"]
    assert package["package_id"] == candidate_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
    assert package["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["includes_signal_families"] == candidate_service.RECOMMENDED_SIGNAL_FAMILIES
    assert package["includes_feature_families"] == candidate_service.RECOMMENDED_FEATURE_FAMILIES
    assert "expectancy-target" in package["rationale"]
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_supporting_feature_package_is_defined_not_selected(candidate: dict) -> None:
    package = candidate["supporting_feature_package"]
    assert package["package_id"] == candidate_service.PACKAGE_REGIME_CONTEXT_SIGNAL_SET
    assert package["status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["includes_signal_families"] == candidate_service.SUPPORTING_SIGNAL_FAMILIES
    assert package["includes_feature_families"] == candidate_service.SUPPORTING_FEATURE_FAMILIES
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_feature_groups_are_candidate_only(candidate: dict) -> None:
    rows = candidate["proposed_feature_groups"]
    assert [row["feature_group_id"] for row in rows] == candidate_service.FEATURE_GROUP_IDS
    assert len(rows) == 17
    assert all(row["group_status"] == "FEATURE_GROUP_CANDIDATE_NOT_GENERATED" for row in rows)
    assert all(row["requires_future_generation_approval"] is True for row in rows)
    assert all(row["target_values_used_as_features"] is False for row in rows)
    assert all(row["future_data_used_as_features"] is False for row in rows)


def test_no_peek_rules_are_planned_only(candidate: dict) -> None:
    rows = candidate["no_peek_and_target_separation_rules"]
    assert [row["rule_id"] for row in rows] == candidate_service.NO_PEEK_RULE_IDS
    assert len(rows) == 10
    assert all(row["rule_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["requires_future_generation_approval"] is True for row in rows)


def test_quality_checks_are_planned_only(candidate: dict) -> None:
    rows = candidate["planned_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == candidate_service.PLANNED_QUALITY_CHECK_IDS
    assert len(rows) == 10
    assert all(row["quality_check_status"] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_future_outputs_are_not_generated(candidate: dict) -> None:
    rows = candidate["future_outputs"]
    assert [row["future_output_id"] for row in rows] == candidate_service.FUTURE_OUTPUT_IDS
    assert len(rows) == 10
    assert candidate["future_outputs_generated"] is False
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["research_only"] is True for row in rows)
    assert all(row["non_actionable"] is True for row in rows)


def test_per_ticker_entries_preserve_target_counts(candidate: dict) -> None:
    entries = candidate["per_ticker_candidate_entries"]
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    assert len(entries) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["target_row_count"] == (13695 if is_meta else 15045)
        assert row["available_target_row_count"] == (13520 if is_meta else 14870)
        assert row["unavailable_target_row_count"] == 175
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["source_target_results_review_digest"] == candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
        assert row["source_target_values_digest"] == candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
        assert row["per_ticker_signal_or_feature_generation_candidate_digest"] == (
            candidate_service.per_ticker_signal_or_feature_generation_candidate_digest_v1(row)
        )
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["candidate_note"] == "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE"


CLOSED_FALSE_FIELDS = [
    "selection_created",
    "approval_created",
    "generation_created",
    "signal_or_feature_generation_selected",
    "signal_or_feature_generation_approved",
    "signal_or_feature_generation_authorized",
    "signal_or_feature_generation_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
    "signal_generation_authorized",
    "signal_generation_performed",
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
    "provider_requests_made_in_candidate",
    "live_provider_transport_enabled_in_candidate",
    "market_data_acquisition_performed_in_candidate",
    "dataset_generation_performed_in_candidate",
    "canonical_dataset_regenerated_in_candidate",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_closed_authority_or_action_field_is_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_authorities_are_not_authorized(
    candidate: dict, field: str
) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_exact(candidate: dict) -> None:
    assert candidate["next_chain"] == candidate_service.NEXT_CHAIN
    assert candidate["next_gates"] == candidate_service.NEXT_GATES
    assert candidate["next_chain"][0] == "Signal or Feature Generation Candidate Operator Review v1."


def test_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 25


def test_checklist_passes(candidate: dict) -> None:
    checklist = candidate["candidate_checklist"]
    assert [row["check_id"] for row in checklist] == candidate_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    summary = candidate["candidate_summary"]
    assert summary["total_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["recommended_feature_package"] == candidate_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    rebuilt = candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()
    digest = candidate["marketflow_signal_or_feature_generation_candidate_v1_digest"]
    assert len(digest) == 64
    assert rebuilt == candidate
    assert rebuilt["marketflow_signal_or_feature_generation_candidate_v1_digest"] == digest
    assert candidate_service.marketflow_signal_or_feature_generation_candidate_v1_digest(candidate) == digest


def test_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    rebuilt = candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()
    assert [row["per_ticker_signal_or_feature_generation_candidate_digest"] for row in rebuilt["per_ticker_candidate_entries"]] == [
        row["per_ticker_signal_or_feature_generation_candidate_digest"]
        for row in candidate["per_ticker_candidate_entries"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(candidate)
    assert result["status"] == "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_VALID"
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


INVALID_TOP_LEVEL_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("candidate_status", "WRONG"),
    ("candidate_scope", "WRONG"),
    ("source_objective_label_or_target_generation_results_review_digest", "0" * 64),
    ("source_objective_label_or_target_values_digest", "0" * 64),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("target_universe_count", 11),
    ("records_digest", "0" * 64),
    ("meta_record_count", 914),
    ("target_results_review_ready", False),
    ("signal_or_feature_generation_candidate_created", False),
    ("signal_or_feature_generation_candidate_ready_for_operator_review", False),
    ("selection_created", True),
    ("approval_created", True),
    ("generation_created", True),
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
    ("provider_requests_made_in_candidate", True),
    ("market_data_acquisition_performed_in_candidate", True),
    ("canonical_dataset_regenerated_in_candidate", True),
    ("target_generation_execution_rerun_performed", True),
    ("target_generation_results_review_rerun_performed", True),
]


@pytest.mark.parametrize(("field", "value"), INVALID_TOP_LEVEL_MUTATIONS)
def test_validator_rejects_invalid_top_level_mutation(
    candidate: dict, field: str, value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = value
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


INVALID_REMOVED_FIELDS = [
    "candidate_philosophy",
    "proposed_signal_families",
    "proposed_feature_families",
    "recommended_feature_package",
    "proposed_feature_groups",
    "no_peek_and_target_separation_rules",
    "planned_quality_checks",
    "future_outputs",
    "risk_controls",
    "marketflow_signal_or_feature_generation_candidate_v1_digest",
]


@pytest.mark.parametrize("field", INVALID_REMOVED_FIELDS)
def test_validator_rejects_missing_required_field(candidate: dict, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


def test_validator_rejects_target_universe_mismatch(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["target_universe"] = list(reversed(invalid["target_universe"]))
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


def test_validator_rejects_missing_supporting_package(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid.pop("supporting_feature_package")
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


def test_validator_rejects_missing_quality_checks(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["planned_quality_checks"] = []
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["per_ticker_candidate_entries"][0].pop(
        "per_ticker_signal_or_feature_generation_candidate_digest"
    )
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(invalid)


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_marketflow_signal_or_feature_generation_candidate_markdown_v1(candidate)
    required_sections = [
        "Title",
        "Signal or Feature Generation Candidate v1",
        "Source Target Results Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Candidate Basis",
        "Candidate Philosophy",
        "Proposed Signal Families",
        "Proposed Feature Families",
        "Recommended Feature Package",
        "Supporting Feature Package",
        "Feature Groups",
        "No-Peek and Target-Separation Rules",
        "Planned Quality Checks",
        "Future Outputs",
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
    for section in required_sections:
        assert f"## {section}" in markdown
    assert candidate["marketflow_signal_or_feature_generation_candidate_v1_digest"] in markdown


def test_writer_round_trip_is_canonical_and_isolated(tmp_path: Path) -> None:
    result = candidate_service.write_marketflow_signal_or_feature_generation_candidate_v1(tmp_path)
    path = Path(result["path"])
    payload = path.read_bytes()
    written = json.loads(payload)
    assert path.parent == tmp_path
    assert payload == canonical_json_bytes(written)
    assert result["payload_sha256"] == sha256_bytes(payload)
    validation = candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(written)
    assert result["marketflow_signal_or_feature_generation_candidate_v1_digest"] == validation[
        "marketflow_signal_or_feature_generation_candidate_v1_digest"
    ]


def test_writer_refuses_to_overwrite(tmp_path: Path) -> None:
    candidate_service.write_marketflow_signal_or_feature_generation_candidate_v1(tmp_path)
    with pytest.raises(candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError):
        candidate_service.write_marketflow_signal_or_feature_generation_candidate_v1(tmp_path)


def test_services_package_exports_candidate_api() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1 == candidate_service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1
    assert services.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW == candidate_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert services.SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION == candidate_service.SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION
    assert services.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET == candidate_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
    assert services.PACKAGE_REGIME_CONTEXT_SIGNAL_SET == candidate_service.PACKAGE_REGIME_CONTEXT_SIGNAL_SET
    assert services.build_marketflow_signal_or_feature_generation_candidate_v1 is candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1
    assert services.validate_marketflow_signal_or_feature_generation_candidate_v1 is candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1
    assert services.write_marketflow_signal_or_feature_generation_candidate_v1 is candidate_service.write_marketflow_signal_or_feature_generation_candidate_v1
    assert services.build_marketflow_signal_or_feature_generation_candidate_markdown_v1 is candidate_service.build_marketflow_signal_or_feature_generation_candidate_markdown_v1
