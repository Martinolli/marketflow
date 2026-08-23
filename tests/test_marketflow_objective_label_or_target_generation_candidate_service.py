from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow import services
from marketflow.services import (
    marketflow_objective_label_or_target_generation_candidate_service as candidate_service,
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_marketflow_objective_label_or_target_generation_candidate_v1()


def test_candidate_builds_offline(candidate: dict) -> None:
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False
    assert candidate["objective_design_execution_rerun_performed"] is False
    assert candidate["objective_design_results_review_rerun_performed"] is False


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1",
    ),
    (
        "schema_version",
        "marketflow_objective_label_or_target_generation_candidate_v1",
    ),
    (
        "candidate_status",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    ),
    (
        "candidate_scope",
        "OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION",
    ),
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
    ("expectancy_objective_design_results_review_ready", True),
    ("ready_for_objective_label_or_target_generation_candidate", True),
    ("objective_label_or_target_generation_candidate_created", True),
    (
        "objective_label_or_target_generation_candidate_ready_for_operator_review",
        True,
    ),
    (
        "ready_for_objective_label_or_target_generation_candidate_operator_review",
        True,
    ),
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


def test_source_review_contract_is_bound(candidate: dict) -> None:
    assert candidate[
        "source_expectancy_objective_design_results_review_artifact_kind"
    ] == "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE"
    assert candidate[
        "source_expectancy_objective_design_results_review_status"
    ] == "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY"
    assert candidate[
        "source_expectancy_objective_design_results_review_scope"
    ] == "EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION"


def test_target_universe_order_and_record_counts_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE
    assert candidate["per_ticker_record_counts"] == (
        candidate_service.EXPECTED_RECORD_COUNTS
    )
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_candidate_basis_preserves_review_statuses(candidate: dict) -> None:
    assert candidate["candidate_basis"] == candidate_service.review_service.REVIEW_STATUSES
    assert candidate["source_expected_output_count"] == 11
    assert candidate["source_observed_output_count"] == 11
    assert candidate["source_output_digest_mismatch_count"] == 0
    assert candidate["source_output_file_inspection_performed"] is True
    assert candidate["source_digest_manifest_self_reference_policy"] == (
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    )


def test_reviewed_design_counts_are_preserved(candidate: dict) -> None:
    assert candidate["source_objective_family_count"] == 10
    assert candidate["source_expectancy_payoff_candidate_field_count"] == 7
    assert candidate["source_abstention_candidate_field_count"] == 6
    assert candidate["source_material_move_candidate_field_count"] == 5
    assert candidate["source_label_generation_plan_step_count"] == 10
    assert candidate["source_validation_metric_count"] == 14
    assert candidate["source_baseline_count"] == 7
    assert candidate["source_per_ticker_review_count"] == 12


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


def test_label_target_families_are_candidate_only(candidate: dict) -> None:
    rows = candidate["proposed_label_target_families"]
    assert [row["label_target_family_id"] for row in rows] == (
        candidate_service.LABEL_TARGET_FAMILY_IDS
    )
    assert len(rows) == 10
    assert all(
        row["candidate_status"]
        == "LABEL_OR_TARGET_CANDIDATE_DEFINED_NOT_GENERATED"
        for row in rows
    )
    for row in rows:
        assert row["operator_review_required"] is True
        assert row["approval_required_before_generation"] is True
        assert row["label_generation_authorized"] is False
        assert row["target_creation_authorized"] is False
        assert row["target_values_created"] is False
        assert row["feature_generation_authorized"] is False
        assert row["metric_computation_authorized"] is False
        assert row["backtest_authorized"] is False
        assert row["model_training_authorized"] is False
        assert row["research_only"] is True
        assert row["non_actionable"] is True


def test_recommended_package_is_defined_not_selected(candidate: dict) -> None:
    package = candidate["recommended_label_target_package"]
    assert package["package_id"] == candidate_service.RECOMMENDED_PACKAGE_ID
    assert package["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["includes"] == candidate_service.RECOMMENDED_PACKAGE_FAMILIES
    assert "expectancy" in package["rationale"].lower()
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_supporting_package_is_defined_not_selected(candidate: dict) -> None:
    package = candidate["supporting_label_target_package"]
    assert package["package_id"] == candidate_service.SUPPORTING_PACKAGE_ID
    assert package["status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["includes"] == candidate_service.SUPPORTING_PACKAGE_FAMILIES
    assert "trend" in package["rationale"].lower()
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_formula_candidate_dimensions_are_not_computed(candidate: dict) -> None:
    rows = candidate["formula_candidate_dimensions"]
    assert [row["formula_dimension_id"] for row in rows] == (
        candidate_service.FORMULA_DIMENSION_IDS
    )
    assert len(rows) == 14
    assert all(row["formula_status"] == "CANDIDATE_FORMULA_NOT_COMPUTED" for row in rows)
    assert all(row["generation_authorized"] is False for row in rows)
    assert all(row["metric_computation_authorized"] is False for row in rows)


def test_availability_and_no_peek_rules_are_planned(candidate: dict) -> None:
    rows = candidate["availability_no_peek_rules"]
    assert [row["rule_id"] for row in rows] == (
        candidate_service.AVAILABILITY_NO_PEEK_RULE_IDS
    )
    assert len(rows) == 10
    assert all(row["rule_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["requires_future_generation_approval"] is True for row in rows)


def test_quality_checks_are_planned_not_executed(candidate: dict) -> None:
    rows = candidate["planned_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == (
        candidate_service.PLANNED_QUALITY_CHECK_IDS
    )
    assert len(rows) == 10
    assert all(
        row["quality_check_status"] == "PLANNED_NOT_EXECUTED" for row in rows
    )


def test_future_outputs_are_not_generated(candidate: dict) -> None:
    rows = candidate["future_outputs"]
    assert [row["future_output_id"] for row in rows] == (
        candidate_service.FUTURE_OUTPUT_IDS
    )
    assert len(rows) == 11
    assert candidate["future_outputs_generated"] is False
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["research_only"] is True for row in rows)
    assert all(row["non_actionable"] is True for row in rows)


def test_per_ticker_entries_and_digests_are_complete(candidate: dict) -> None:
    rows = candidate["per_ticker_candidate_entries"]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == candidate_service.TARGET_UNIVERSE
    for row in rows:
        assert row[
            "per_ticker_objective_label_or_target_generation_candidate_digest"
        ] == candidate_service.per_ticker_objective_label_or_target_generation_candidate_digest_v1(
            row
        )
        assert row["recommended_label_target_package"] == (
            candidate_service.RECOMMENDED_PACKAGE_ID
        )
        assert row["label_generation_authorized"] is False
        assert row["target_values_created"] is False
        assert row["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_limitation_is_preserved(candidate: dict) -> None:
    meta = next(
        row for row in candidate["per_ticker_candidate_entries"] if row["ticker"] == "META"
    )
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["candidate_note"] == (
        "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in candidate["per_ticker_candidate_entries"]
        if row["ticker"] != "META"
    )


CLOSED_FALSE_FIELDS = [
    "selection_created",
    "approval_created",
    "generation_created",
    "objective_label_or_target_generation_approved",
    "objective_label_or_target_generation_authorized",
    "objective_label_or_target_generation_performed",
    "label_generation_authorized",
    "label_generation_performed",
    "new_targets_created",
    "target_values_created",
    "target_definition_change_authorized",
    "target_definition_change_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
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
    "objective_design_execution_rerun_performed",
    "objective_design_results_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_selection_generation_and_downstream_authority_remain_closed(
    candidate: dict, field: str
) -> None:
    assert candidate[field] is False


def test_next_chain_next_gates_and_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["next_chain"] == candidate_service.NEXT_CHAIN
    assert candidate["next_gates"] == candidate_service.NEXT_GATES
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS
    assert len(candidate["next_chain"]) == 9
    assert len(candidate["next_gates"]) == 9
    assert len(candidate["risk_controls"]) == 26


def test_checklist_passes(candidate: dict) -> None:
    rows = candidate["candidate_checklist"]
    assert [row["check_id"] for row in rows] == candidate_service.REQUIRED_CHECK_IDS
    assert len(rows) == 75
    assert all(row["status"] == "PASS" for row in rows)
    assert candidate["candidate_summary"]["total_checks"] == 75
    assert candidate["candidate_summary"]["passed_checks"] == 75
    assert candidate["candidate_summary"]["failed_checks"] == 0
    assert candidate["candidate_summary"]["blocker_count"] == 0
    assert candidate["candidate_summary"]["selection_created"] is False
    assert candidate["candidate_summary"]["approval_created"] is False
    assert candidate["candidate_summary"]["generation_created"] is False


def test_candidate_and_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    again = candidate_service.build_marketflow_objective_label_or_target_generation_candidate_v1()
    assert again[
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    ] == candidate[
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    ]
    assert [
        row["per_ticker_objective_label_or_target_generation_candidate_digest"]
        for row in again["per_ticker_candidate_entries"]
    ] == [
        row["per_ticker_objective_label_or_target_generation_candidate_digest"]
        for row in candidate["per_ticker_candidate_entries"]
    ]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    validation = candidate_service.validate_marketflow_objective_label_or_target_generation_candidate_v1(
        deepcopy(candidate)
    )
    assert validation["status"] == (
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_VALID"
    )
    assert validation["total_checks"] == 75


INVALID_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("candidate_status", "WRONG"),
    ("candidate_scope", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_expectancy_objective_design_results_review_digest", "0" * 64),
    ("source_expectancy_objective_design_execution_digest", "0" * 64),
    ("source_expectancy_objective_design_output_binding_digest", "0" * 64),
    ("source_expectancy_objective_approval_digest", "0" * 64),
    ("feature_label_matrix_digest", "0" * 64),
    ("feature_values_digest", "0" * 64),
    ("redesigned_label_values_digest", "0" * 64),
    ("records_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("meta_record_count", 1003),
    ("expectancy_objective_design_results_review_ready", False),
    ("ready_for_objective_label_or_target_generation_candidate", False),
    ("objective_label_or_target_generation_candidate_created", False),
    (
        "objective_label_or_target_generation_candidate_ready_for_operator_review",
        False,
    ),
    ("candidate_philosophy", ""),
    ("proposed_label_target_families", []),
    ("recommended_label_target_package", {}),
    ("supporting_label_target_package", {}),
    ("formula_candidate_dimensions", []),
    ("availability_no_peek_rules", []),
    ("planned_quality_checks", []),
    ("future_outputs", []),
    ("selection_created", True),
    ("approval_created", True),
    ("generation_created", True),
    ("label_generation_authorized", True),
    ("label_generation_performed", True),
    ("new_targets_created", True),
    ("target_values_created", True),
    ("target_definition_change_authorized", True),
    ("feature_generation_authorized", True),
    ("feature_label_matrix_created", True),
    ("backtest_execution_authorized", True),
    ("model_training_authorized", True),
    ("metric_computation_authorized", True),
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
    ("objective_design_execution_rerun_performed", True),
    ("objective_design_results_review_rerun_performed", True),
    ("risk_controls", []),
    ("marketflow_objective_label_or_target_generation_candidate_v1_digest", None),
]


@pytest.mark.parametrize(("field", "value"), INVALID_MUTATIONS)
def test_validator_rejects_invalid_candidate_field(
    candidate: dict, field: str, value: object
) -> None:
    mutated = deepcopy(candidate)
    mutated[field] = value
    with pytest.raises(
        candidate_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateError
    ):
        candidate_service.validate_marketflow_objective_label_or_target_generation_candidate_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    mutated = deepcopy(candidate)
    mutated["per_ticker_candidate_entries"][0].pop(
        "per_ticker_objective_label_or_target_generation_candidate_digest"
    )
    with pytest.raises(
        candidate_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateError
    ):
        candidate_service.validate_marketflow_objective_label_or_target_generation_candidate_v1(
            mutated
        )


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_marketflow_objective_label_or_target_generation_candidate_markdown_v1(
        candidate
    )
    sections = [
        "Title",
        "Objective Label or Target Generation Candidate v1",
        "Source Design Results Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Candidate Basis",
        "Candidate Philosophy",
        "Proposed Label/Target Families",
        "Recommended Label/Target Package",
        "Supporting Label/Target Package",
        "Formula Candidate Dimensions",
        "Availability and No-Peek Rules",
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
    assert all(f"## {section}" in markdown for section in sections)
    assert "not accepted" in markdown
    assert "NOT_AUTHORIZED" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path: Path, candidate: dict
) -> None:
    result = candidate_service.write_marketflow_objective_label_or_target_generation_candidate_v1(
        tmp_path
    )
    path = Path(result["path"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    assert result[
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    ] == candidate[
        "marketflow_objective_label_or_target_generation_candidate_v1_digest"
    ]
    with pytest.raises(
        candidate_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateError
    ):
        candidate_service.write_marketflow_objective_label_or_target_generation_candidate_v1(
            tmp_path
        )


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1 == candidate_service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1
    assert services.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW == candidate_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert services.OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION == candidate_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION
    assert services.build_marketflow_objective_label_or_target_generation_candidate_v1 is candidate_service.build_marketflow_objective_label_or_target_generation_candidate_v1
    assert services.validate_marketflow_objective_label_or_target_generation_candidate_v1 is candidate_service.validate_marketflow_objective_label_or_target_generation_candidate_v1
    assert services.write_marketflow_objective_label_or_target_generation_candidate_v1 is candidate_service.write_marketflow_objective_label_or_target_generation_candidate_v1
    assert services.build_marketflow_objective_label_or_target_generation_candidate_markdown_v1 is candidate_service.build_marketflow_objective_label_or_target_generation_candidate_markdown_v1
