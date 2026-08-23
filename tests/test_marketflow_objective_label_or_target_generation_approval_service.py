from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    marketflow_objective_label_or_target_generation_approval_service as approval_service,
)


def _attestation() -> dict:
    return approval_service.build_marketflow_objective_label_or_target_generation_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        operator_confirms_design_results_review_digest=approval_service.SOURCE_EVIDENCE_DIGESTS[
            "source_expectancy_objective_design_results_review_digest"
        ],
        operator_confirms_records_digest=approval_service.SOURCE_EVIDENCE_DIGESTS[
            "records_digest"
        ],
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
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
def approval(attestation: dict) -> dict:
    return approval_service.build_marketflow_objective_label_or_target_generation_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        approval_service.OPERATOR_DECISION_APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION
    )
    assert attestation["operator_attestation_phrase"] == (
        approval_service.REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE
    )
    assert all(
        attestation[field] is True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline(approval: dict) -> None:
    assert approval["created_offline"] is True
    assert approval["provider_requests_made_in_approval"] is False
    assert approval["candidate_creation_rerun_performed"] is False
    assert approval["candidate_review_rerun_performed"] is False


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED",
    ),
    (
        "schema_version",
        "marketflow_objective_label_or_target_generation_approval_v1",
    ),
    (
        "approval_status",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED",
    ),
    ("approval_scope", "OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY"),
    (
        "selected_label_target_package",
        "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET",
    ),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    (
        "source_objective_label_or_target_generation_candidate_review_artifact_kind",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE",
    ),
    (
        "source_objective_label_or_target_generation_candidate_review_status",
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY",
    ),
    (
        "source_objective_label_or_target_generation_candidate_review_scope",
        "OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL",
    ),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("objective_label_or_target_generation_selected", True),
    ("objective_label_or_target_generation_approved", True),
    ("objective_label_or_target_generation_authorized", True),
    ("objective_label_or_target_generation_approval_created", True),
    ("ready_for_objective_label_or_target_generation_execution", True),
    ("label_or_target_generation_authorized_for_future_execution", True),
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
    "source_objective_label_or_target_generation_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_objective_label_or_target_generation_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_design_results_review_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_results_review_digest"
    ],
    "source_design_execution_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_execution_digest"
    ],
    "source_design_output_binding_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "source_expectancy_objective_design_output_binding_digest"
    ],
    **approval_service.SOURCE_EVIDENCE_DIGESTS,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    approval: dict, field: str, expected: str
) -> None:
    assert approval[field] == expected
    assert len(approval[field]) == 64


def test_target_universe_order_and_record_counts_are_preserved(approval: dict) -> None:
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["per_ticker_record_counts"] == approval_service.EXPECTED_RECORD_COUNTS
    assert approval["meta_reduced_record_count_preserved"] is True


def test_selected_label_target_families_are_future_execution_only(
    approval: dict,
) -> None:
    rows = approval["selected_label_target_families"]
    assert [row["label_target_family_id"] for row in rows] == (
        approval_service.review_service.candidate_service.RECOMMENDED_PACKAGE_FAMILIES
    )
    assert len(rows) == 5
    for row in rows:
        assert row["approval_status"] == (
            "APPROVED_FOR_FUTURE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY"
        )
        assert row["candidate_status"] == (
            "LABEL_OR_TARGET_CANDIDATE_DEFINED_NOT_GENERATED"
        )
        assert row["generation_performed"] is False
        assert row["target_values_created"] is False
        assert row["feature_generation_authorized"] is False


def test_supporting_families_are_available_not_selected(approval: dict) -> None:
    rows = approval["supporting_label_target_families"]
    assert [row["label_target_family_id"] for row in rows] == (
        approval_service.review_service.candidate_service.SUPPORTING_PACKAGE_FAMILIES
    )
    assert len(rows) == 5
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in rows)
    assert all(row["generation_performed"] is False for row in rows)
    assert all(row["target_values_created"] is False for row in rows)


def test_formula_dimensions_are_approved_for_planning_only(approval: dict) -> None:
    rows = approval["approved_formula_dimensions"]
    assert [row["formula_dimension_id"] for row in rows] == (
        approval_service.review_service.candidate_service.FORMULA_DIMENSION_IDS
    )
    assert len(rows) == 14
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_FORMULA_EXECUTION_PLANNING_ONLY"
        and row["formula_status"] == "CANDIDATE_FORMULA_NOT_COMPUTED"
        and row["generation_performed"] is False
        and row["metric_computation_authorized"] is False
        for row in rows
    )


def test_availability_rules_are_approved_as_future_controls(approval: dict) -> None:
    rows = approval["approved_availability_no_peek_rules"]
    assert [row["rule_id"] for row in rows] == (
        approval_service.review_service.candidate_service.AVAILABILITY_NO_PEEK_RULE_IDS
    )
    assert len(rows) == 10
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_GENERATION_EXECUTION_CONTROL"
        and row["rule_status"] == "PLANNED_NOT_EXECUTED"
        for row in rows
    )


def test_quality_checks_are_approved_as_future_controls(approval: dict) -> None:
    rows = approval["approved_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == (
        approval_service.review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
    )
    assert len(rows) == 10
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_GENERATION_QUALITY_CONTROL"
        and row["quality_check_status"] == "PLANNED_NOT_EXECUTED"
        for row in rows
    )


def test_future_outputs_are_authorized_not_generated(approval: dict) -> None:
    rows = approval["approved_future_outputs"]
    assert [row["future_output_id"] for row in rows] == (
        approval_service.review_service.candidate_service.FUTURE_OUTPUT_IDS
    )
    assert len(rows) == 11
    assert all(
        row["approval_status"] == "AUTHORIZED_NOT_GENERATED"
        and row["output_status"] == "PLANNED_NOT_GENERATED"
        and row["generated"] is False
        and row["research_only"] is True
        and row["non_actionable"] is True
        for row in rows
    )


def test_per_ticker_entries_and_digests_are_complete(approval: dict) -> None:
    rows = approval[
        "per_ticker_objective_label_or_target_generation_approval_entries"
    ]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == approval_service.TARGET_UNIVERSE
    for row in rows:
        assert row[
            "per_ticker_objective_label_or_target_generation_approval_digest"
        ] == approval_service.per_ticker_objective_label_or_target_generation_approval_digest_v1(
            row
        )
        assert row["objective_label_or_target_generation_selected"] is True
        assert row["objective_label_or_target_generation_approved"] is True
        assert row["objective_label_or_target_generation_performed"] is False
        assert row["target_values_created"] is False
        assert row["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_limitation_is_preserved(approval: dict) -> None:
    rows = approval[
        "per_ticker_objective_label_or_target_generation_approval_entries"
    ]
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["approval_note"] == (
        "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL"
    )
    assert all(
        row["historical_record_count"] == 1003
        and row["meta_reduced_record_count_flag"] is False
        for row in rows
        if row["ticker"] != "META"
    )


CLOSED_FALSE_FIELDS = [
    "objective_label_or_target_generation_performed",
    "label_generation_performed",
    "target_generation_performed",
    "new_targets_created",
    "target_values_created",
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
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "candidate_creation_rerun_performed",
    "candidate_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_execution_and_downstream_authority_remain_closed(
    approval: dict, field: str
) -> None:
    assert approval[field] is False


def test_next_chain_next_gates_and_risk_controls_are_exact(approval: dict) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN
    assert approval["next_gates"] == approval_service.NEXT_GATES
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS
    assert len(approval["next_chain"]) == 7
    assert len(approval["next_gates"]) == 8
    assert len(approval["risk_controls"]) == 27


def test_checklist_passes(approval: dict) -> None:
    rows = approval["approval_checklist"]
    assert [row["check_id"] for row in rows] == approval_service.REQUIRED_CHECK_IDS
    assert len(rows) == 74
    assert all(row["status"] == "PASS" for row in rows)
    assert approval["approval_summary"]["total_checks"] == 74
    assert approval["approval_summary"]["passed_checks"] == 74
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0
    assert approval["approval_summary"]["objective_label_or_target_generation_selected"] is True
    assert approval["approval_summary"]["objective_label_or_target_generation_performed"] is False


def test_approval_and_per_ticker_digests_are_deterministic(
    approval: dict, attestation: dict
) -> None:
    again = approval_service.build_marketflow_objective_label_or_target_generation_approval_v1(
        operator_attestation=attestation
    )
    assert again[
        "marketflow_objective_label_or_target_generation_approval_digest"
    ] == approval[
        "marketflow_objective_label_or_target_generation_approval_digest"
    ]
    field = "per_ticker_objective_label_or_target_generation_approval_digest"
    assert [row[field] for row in again["per_ticker_objective_label_or_target_generation_approval_entries"]] == [
        row[field]
        for row in approval[
            "per_ticker_objective_label_or_target_generation_approval_entries"
        ]
    ]


def test_validator_accepts_valid_approval(approval: dict) -> None:
    validation = approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1(
        deepcopy(approval)
    )
    assert validation["status"] == (
        "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_VALID"
    )
    assert validation["total_checks"] == 74


@pytest.mark.parametrize(
    "field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_boundary_confirmation(
    attestation: dict, field: str
) -> None:
    mutated = deepcopy(attestation)
    mutated[field] = False
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.build_marketflow_objective_label_or_target_generation_approval_v1(
            operator_attestation=mutated
        )


INVALID_ATTESTATION_MUTATIONS = [
    ("operator_decision", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("operator_attestation_phrase", "WRONG"),
    ("operator_attestation_version", "WRONG"),
    ("operator_reference", ""),
    ("operator_attestation_timestamp_utc", ""),
    ("operator_confirms_candidate_review_digest", "0" * 64),
    ("operator_confirms_candidate_digest", "0" * 64),
    ("operator_confirms_design_results_review_digest", "0" * 64),
    ("operator_confirms_records_digest", "0" * 64),
    ("operator_confirms_target_universe", ["MSFT"]),
    ("operator_confirms_target_count", 11),
    ("operator_confirms_meta_record_count", 1003),
    ("operator_confirms_non_meta_record_count", 913),
    ("operator_confirms_selected_label_target_package", "WRONG"),
    ("operator_confirms_selected_objective_path", "WRONG"),
]


@pytest.mark.parametrize(("field", "value"), INVALID_ATTESTATION_MUTATIONS)
def test_builder_rejects_invalid_attestation_field(
    attestation: dict, field: str, value: object
) -> None:
    mutated = deepcopy(attestation)
    mutated[field] = value
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.build_marketflow_objective_label_or_target_generation_approval_v1(
            operator_attestation=mutated
        )


INVALID_APPROVAL_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("approval_status", "WRONG"),
    ("approval_scope", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_objective_label_or_target_generation_candidate_review_digest", "0" * 64),
    ("source_objective_label_or_target_generation_candidate_digest", "0" * 64),
    ("source_design_results_review_digest", "0" * 64),
    ("records_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("meta_record_count", 1003),
    ("label_or_target_generation_authorized_for_future_execution", False),
    ("objective_label_or_target_generation_performed", True),
    ("objective_label_or_target_generation_approval_created", False),
    ("ready_for_objective_label_or_target_generation_execution", False),
    ("selected_label_target_families", []),
    ("supporting_label_target_families", []),
    ("approved_formula_dimensions", []),
    ("approved_availability_no_peek_rules", []),
    ("approved_quality_checks", []),
    ("approved_future_outputs", []),
    ("label_generation_performed", True),
    ("target_generation_performed", True),
    ("new_targets_created", True),
    ("target_values_created", True),
    ("target_definition_change_performed", True),
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
    ("provider_requests_made_in_approval", True),
    ("market_data_acquisition_performed_in_approval", True),
    ("canonical_dataset_regenerated_in_approval", True),
    ("candidate_creation_rerun_performed", True),
    ("candidate_review_rerun_performed", True),
    ("risk_controls", []),
    ("marketflow_objective_label_or_target_generation_approval_digest", None),
]


@pytest.mark.parametrize(("field", "value"), INVALID_APPROVAL_MUTATIONS)
def test_validator_rejects_invalid_approval_field(
    approval: dict, field: str, value: object
) -> None:
    mutated = deepcopy(approval)
    mutated[field] = value
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1(
            mutated
        )


def test_validator_rejects_wrong_nested_operator_decision(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated["operator_attestation"]["operator_decision"] = "WRONG"
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1(
            mutated
        )


def test_validator_rejects_wrong_nested_attestation_phrase(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated[
        "per_ticker_objective_label_or_target_generation_approval_entries"
    ][0].pop("per_ticker_objective_label_or_target_generation_approval_digest")
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1(
            mutated
        )


def test_markdown_includes_required_sections(approval: dict) -> None:
    markdown = approval_service.build_marketflow_objective_label_or_target_generation_approval_markdown_v1(
        approval
    )
    sections = [
        "Title",
        "Objective Label or Target Generation Approval v1",
        "Operator Attestation",
        "Source Candidate Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approval Scope",
        "Selected Label/Target Package",
        "Selected Objective Path",
        "Selected Label/Target Families",
        "Supporting Label/Target Families",
        "Approved Formula Dimensions",
        "Approved Availability and No-Peek Rules",
        "Approved Quality Checks",
        "Approved Future Outputs",
        "Per-Ticker Approval Summary",
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
    tmp_path: Path, approval: dict, attestation: dict
) -> None:
    result = approval_service.write_marketflow_objective_label_or_target_generation_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    path = Path(result["path"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    assert result[
        "marketflow_objective_label_or_target_generation_approval_digest"
    ] == approval[
        "marketflow_objective_label_or_target_generation_approval_digest"
    ]
    with pytest.raises(
        approval_service.MarketFlowObjectiveLabelOrTargetGenerationApprovalError
    ):
        approval_service.write_marketflow_objective_label_or_target_generation_approval_v1(
            tmp_path, operator_attestation=attestation
        )


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED == approval_service.ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED
    assert services.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED == approval_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED
    assert services.OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY == approval_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY
    assert services.SELECTED_LABEL_TARGET_PACKAGE == approval_service.SELECTED_LABEL_TARGET_PACKAGE
    assert services.REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE == approval_service.REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE
    assert services.build_marketflow_objective_label_or_target_generation_approval_attestation_v1 is approval_service.build_marketflow_objective_label_or_target_generation_approval_attestation_v1
    assert services.build_marketflow_objective_label_or_target_generation_approval_v1 is approval_service.build_marketflow_objective_label_or_target_generation_approval_v1
    assert services.validate_marketflow_objective_label_or_target_generation_approval_v1 is approval_service.validate_marketflow_objective_label_or_target_generation_approval_v1
    assert services.write_marketflow_objective_label_or_target_generation_approval_v1 is approval_service.write_marketflow_objective_label_or_target_generation_approval_v1
    assert services.build_marketflow_objective_label_or_target_generation_approval_markdown_v1 is approval_service.build_marketflow_objective_label_or_target_generation_approval_markdown_v1
