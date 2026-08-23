from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    marketflow_objective_label_or_target_generation_candidate_operator_review_service as review_service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1()


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["candidate_creation_rerun_performed"] is False
    assert review["design_results_review_rerun_performed"] is False


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    ),
    (
        "schema_version",
        "marketflow_objective_label_or_target_generation_candidate_operator_review_v1",
    ),
    (
        "review_status",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    ),
    (
        "review_scope",
        "OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    ),
    (
        "source_objective_label_or_target_generation_candidate_artifact_kind",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_V1",
    ),
    (
        "source_objective_label_or_target_generation_candidate_status",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW",
    ),
    (
        "source_objective_label_or_target_generation_candidate_scope",
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
    ("objective_label_or_target_generation_candidate_review_created", True),
    ("objective_label_or_target_generation_candidate_review_ready", True),
    ("ready_for_objective_label_or_target_generation_approval", False),
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
    "source_objective_label_or_target_generation_candidate_digest": review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_design_results_review_digest": review_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_results_review_digest"
    ],
    "source_design_execution_digest": review_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_execution_digest"
    ],
    "source_design_output_binding_digest": review_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_output_binding_digest"
    ],
    **review_service.SOURCE_EVIDENCE_DIGESTS,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    review: dict, field: str, expected: str
) -> None:
    assert review[field] == expected
    assert len(review[field]) == 64


def test_target_universe_order_and_record_counts_are_preserved(review: dict) -> None:
    assert review["target_universe"] == review_service.TARGET_UNIVERSE
    assert review["per_ticker_record_counts"] == review_service.EXPECTED_RECORD_COUNTS
    assert review["meta_reduced_record_count_preserved"] is True


def test_candidate_basis_and_philosophy_are_reviewed(review: dict) -> None:
    basis = review["reviewed_candidate_basis"]
    assert basis["selected_objective_path"] == review_service.SELECTED_OBJECTIVE_PATH
    assert len(basis["source_reviewed_design_components"]) == 10
    assert basis["review_status"] == "REVIEWED_CANDIDATE_BASIS"
    philosophy = review["reviewed_candidate_philosophy"]
    assert philosophy["review_status"] == "REVIEWED_CANDIDATE_PHILOSOPHY"
    assert philosophy["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
    assert "no-generation" in philosophy["candidate_philosophy"]
    assert "majority/flat-class" in philosophy["candidate_secondary_question"]


def test_label_target_families_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_label_target_families"]
    assert [row["label_target_family_id"] for row in rows] == (
        review_service.candidate_service.LABEL_TARGET_FAMILY_IDS
    )
    assert len(rows) == 10
    for row in rows:
        assert row["review_status"] == (
            "REVIEWED_LABEL_OR_TARGET_CANDIDATE_NOT_GENERATED"
        )
        assert row["candidate_status"] == (
            "LABEL_OR_TARGET_CANDIDATE_DEFINED_NOT_GENERATED"
        )
        assert row["approval_status"] == "NOT_APPROVED_BY_THIS_REVIEW"
        assert row["label_generation_authorized"] is False
        assert row["target_creation_authorized"] is False
        assert row["target_values_created"] is False


def test_recommended_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_recommended_label_target_package"]
    assert package["package_id"] == review_service.RECOMMENDED_PACKAGE_ID
    assert package["source_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == (
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    )
    assert package["includes"] == (
        review_service.candidate_service.RECOMMENDED_PACKAGE_FAMILIES
    )
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_supporting_package_is_reviewed_but_not_selected(review: dict) -> None:
    package = review["reviewed_supporting_label_target_package"]
    assert package["package_id"] == review_service.SUPPORTING_PACKAGE_ID
    assert package["source_status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert package["review_status"] == (
        "REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED"
    )
    assert package["includes"] == (
        review_service.candidate_service.SUPPORTING_PACKAGE_FAMILIES
    )
    assert package["selection_created"] is False
    assert package["approval_created"] is False
    assert package["generation_created"] is False


def test_formula_dimensions_are_reviewed_not_computed(review: dict) -> None:
    rows = review["reviewed_formula_dimensions"]
    assert [row["formula_dimension_id"] for row in rows] == (
        review_service.candidate_service.FORMULA_DIMENSION_IDS
    )
    assert len(rows) == 14
    assert all(
        row["review_status"] == "REVIEWED_CANDIDATE_FORMULA_NOT_COMPUTED"
        and row["formula_status"] == "CANDIDATE_FORMULA_NOT_COMPUTED"
        and row["generation_authorized"] is False
        and row["metric_computation_authorized"] is False
        for row in rows
    )


def test_availability_rules_are_reviewed_not_executed(review: dict) -> None:
    rows = review["reviewed_availability_no_peek_rules"]
    assert [row["rule_id"] for row in rows] == (
        review_service.candidate_service.AVAILABILITY_NO_PEEK_RULE_IDS
    )
    assert len(rows) == 10
    assert all(
        row["review_status"] == "REVIEWED_PLANNED_RULE_NOT_EXECUTED"
        and row["rule_status"] == "PLANNED_NOT_EXECUTED"
        and row["requires_future_generation_approval"] is True
        for row in rows
    )


def test_quality_checks_are_reviewed_not_executed(review: dict) -> None:
    rows = review["reviewed_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == (
        review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
    )
    assert len(rows) == 10
    assert all(
        row["review_status"] == "REVIEWED_PLANNED_CHECK_NOT_EXECUTED"
        and row["quality_check_status"] == "PLANNED_NOT_EXECUTED"
        for row in rows
    )


def test_future_outputs_are_reviewed_not_generated(review: dict) -> None:
    rows = review["reviewed_future_outputs"]
    assert [row["future_output_id"] for row in rows] == (
        review_service.candidate_service.FUTURE_OUTPUT_IDS
    )
    assert len(rows) == 11
    assert all(
        row["review_status"] == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
        and row["output_status"] == "PLANNED_NOT_GENERATED"
        and row["generated"] is False
        and row["research_only"] is True
        and row["non_actionable"] is True
        for row in rows
    )


def test_per_ticker_entries_and_digests_are_complete(review: dict) -> None:
    rows = review[
        "per_ticker_objective_label_or_target_generation_candidate_review_entries"
    ]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == review_service.TARGET_UNIVERSE
    for row in rows:
        assert row[
            "per_ticker_objective_label_or_target_generation_candidate_review_digest"
        ] == review_service.per_ticker_objective_label_or_target_generation_candidate_review_digest_v1(
            row
        )
        assert row["objective_label_or_target_generation_selected"] is False
        assert row["objective_label_or_target_generation_approved"] is False
        assert row["target_values_created"] is False
        assert row["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_limitation_is_preserved(review: dict) -> None:
    rows = review[
        "per_ticker_objective_label_or_target_generation_candidate_review_entries"
    ]
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["review_note"] == (
        "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_REVIEW"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


CLOSED_FALSE_FIELDS = [
    "ready_for_objective_label_or_target_generation_approval",
    "objective_label_or_target_generation_selected",
    "objective_label_or_target_generation_approved",
    "objective_label_or_target_generation_authorized",
    "objective_label_or_target_generation_performed",
    "selection_created",
    "approval_created",
    "generation_created",
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
    "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review",
    "candidate_creation_rerun_performed",
    "design_results_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_selection_approval_generation_and_downstream_authority_remain_closed(
    review: dict, field: str
) -> None:
    assert review[field] is False


def test_next_chain_next_gates_and_risk_controls_are_exact(review: dict) -> None:
    assert review["next_chain"] == review_service.NEXT_CHAIN
    assert review["next_gates"] == review_service.NEXT_GATES
    assert review["risk_controls"] == review_service.RISK_CONTROLS
    assert len(review["next_chain"]) == 8
    assert len(review["next_gates"]) == 9
    assert len(review["risk_controls"]) == 28


def test_checklist_passes(review: dict) -> None:
    rows = review["review_checklist"]
    assert [row["check_id"] for row in rows] == review_service.REQUIRED_CHECK_IDS
    assert len(rows) == 79
    assert all(row["status"] == "PASS" for row in rows)
    assert review["review_summary"]["total_checks"] == 79
    assert review["review_summary"]["passed_checks"] == 79
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0
    assert review["review_summary"]["selection_created"] is False
    assert review["review_summary"]["approval_created"] is False
    assert review["review_summary"]["generation_created"] is False


def test_review_and_per_ticker_digests_are_deterministic(review: dict) -> None:
    again = review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1()
    assert again[
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    ] == review[
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    ]
    field = (
        "per_ticker_objective_label_or_target_generation_candidate_review_digest"
    )
    assert [row[field] for row in again["per_ticker_objective_label_or_target_generation_candidate_review_entries"]] == [
        row[field]
        for row in review[
            "per_ticker_objective_label_or_target_generation_candidate_review_entries"
        ]
    ]


def test_validator_accepts_valid_review(review: dict) -> None:
    validation = review_service.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        deepcopy(review)
    )
    assert validation["status"] == (
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID"
    )
    assert validation["total_checks"] == 79


INVALID_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("review_status", "WRONG"),
    ("review_scope", "WRONG"),
    ("source_objective_label_or_target_generation_candidate_digest", "0" * 64),
    ("source_design_results_review_digest", "0" * 64),
    ("source_design_execution_digest", "0" * 64),
    ("source_design_output_binding_digest", "0" * 64),
    ("source_expectancy_objective_approval_digest", "0" * 64),
    ("selected_objective_path", "WRONG"),
    ("feature_label_matrix_digest", "0" * 64),
    ("feature_values_digest", "0" * 64),
    ("redesigned_label_values_digest", "0" * 64),
    ("records_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("meta_record_count", 1003),
    ("objective_label_or_target_generation_candidate_review_created", False),
    ("objective_label_or_target_generation_candidate_review_ready", False),
    ("ready_for_objective_label_or_target_generation_approval", True),
    ("reviewed_candidate_philosophy", {}),
    ("reviewed_label_target_families", []),
    ("reviewed_recommended_label_target_package", {}),
    ("reviewed_supporting_label_target_package", {}),
    ("reviewed_formula_dimensions", []),
    ("reviewed_availability_no_peek_rules", []),
    ("reviewed_quality_checks", []),
    ("reviewed_future_outputs", []),
    ("selection_created", True),
    ("approval_created", True),
    ("generation_created", True),
    ("objective_label_or_target_generation_selected", True),
    ("objective_label_or_target_generation_approved", True),
    ("objective_label_or_target_generation_authorized", True),
    ("objective_label_or_target_generation_performed", True),
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
    ("provider_requests_made_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
    ("candidate_creation_rerun_performed", True),
    ("design_results_review_rerun_performed", True),
    ("risk_controls", []),
    (
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        None,
    ),
]


@pytest.mark.parametrize(("field", "value"), INVALID_MUTATIONS)
def test_validator_rejects_invalid_review_field(
    review: dict, field: str, value: object
) -> None:
    mutated = deepcopy(review)
    mutated[field] = value
    with pytest.raises(
        review_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    mutated = deepcopy(review)
    mutated[
        "per_ticker_objective_label_or_target_generation_candidate_review_entries"
    ][0].pop(
        "per_ticker_objective_label_or_target_generation_candidate_review_digest"
    )
    with pytest.raises(
        review_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError
    ):
        review_service.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
            mutated
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_markdown_v1(
        review
    )
    sections = [
        "Title",
        "Objective Label or Target Generation Candidate Operator Review v1",
        "Source Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Reviewed Candidate Basis",
        "Reviewed Candidate Philosophy",
        "Reviewed Label/Target Families",
        "Reviewed Recommended Package",
        "Reviewed Supporting Package",
        "Reviewed Formula Dimensions",
        "Reviewed Availability and No-Peek Rules",
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
    assert all(f"## {section}" in markdown for section in sections)
    assert "not accepted" in markdown
    assert "NOT_AUTHORIZED" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path: Path, review: dict
) -> None:
    result = review_service.write_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        tmp_path
    )
    path = Path(result["path"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    assert result[
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    ] == review[
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    ]
    with pytest.raises(
        review_service.MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError
    ):
        review_service.write_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
            tmp_path
        )


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE
    assert services.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY == review_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY
    assert services.OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL == review_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL
    assert services.build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1 is review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1
    assert services.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1 is review_service.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1
    assert services.write_marketflow_objective_label_or_target_generation_candidate_operator_review_v1 is review_service.write_marketflow_objective_label_or_target_generation_candidate_operator_review_v1
    assert services.build_marketflow_objective_label_or_target_generation_candidate_operator_review_markdown_v1 is review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_markdown_v1
