from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    marketflow_signal_or_feature_generation_approval_service as approval_service,
)


def _attestation() -> dict:
    return approval_service.build_marketflow_signal_or_feature_generation_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-24T00:00:00Z",
        operator_attestation_phrase=approval_service.REQUIRED_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        operator_confirms_target_results_review_digest=approval_service.SOURCE_EVIDENCE_DIGESTS[
            "marketflow_objective_label_or_target_generation_results_review_digest"
        ],
        operator_confirms_target_values_digest=approval_service.SOURCE_EVIDENCE_DIGESTS[
            "objective_label_or_target_values_digest"
        ],
        operator_confirms_records_digest=approval_service.SOURCE_EVIDENCE_DIGESTS[
            "records_digest"
        ],
        operator_confirms_target_universe=approval_service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
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
def approval(attestation: dict) -> dict:
    return approval_service.build_marketflow_signal_or_feature_generation_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        approval_service.OPERATOR_DECISION_APPROVE_SIGNAL_OR_FEATURE_GENERATION
    )
    assert attestation["operator_attestation_phrase"] == (
        approval_service.REQUIRED_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ATTESTATION_PHRASE
    )
    assert all(
        attestation[field] is True
        for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED"),
    ("schema_version", "marketflow_signal_or_feature_generation_approval_v1"),
    ("approval_status", "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED"),
    ("approval_scope", "SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ONLY"),
    ("selected_feature_package", "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"),
    (
        "selected_label_target_package",
        "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET",
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
    ("target_profile_count", 15),
    ("target_row_count", 179190),
    ("available_target_row_count", 177090),
    ("unavailable_target_row_count", 2100),
    ("created_offline", True),
    ("signal_or_feature_generation_selected", True),
    ("signal_or_feature_generation_approved", True),
    ("signal_or_feature_generation_authorized", True),
    ("signal_or_feature_generation_approval_created", True),
    ("ready_for_signal_or_feature_generation_execution", True),
    ("signal_or_feature_generation_authorized_for_future_execution", True),
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
    "source_signal_or_feature_generation_candidate_review_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
    "source_signal_or_feature_generation_candidate_digest": approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "source_target_results_review_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "marketflow_objective_label_or_target_generation_results_review_digest"
    ],
    "source_target_generation_execution_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "marketflow_objective_label_or_target_generation_execution_digest"
    ],
    "source_target_values_digest": approval_service.SOURCE_EVIDENCE_DIGESTS[
        "objective_label_or_target_values_digest"
    ],
    **approval_service.SOURCE_EVIDENCE_DIGESTS,
}


@pytest.mark.parametrize(("field", "expected"), list(BOUND_DIGESTS.items()))
def test_required_source_digest_is_bound(
    approval: dict, field: str, expected: str
) -> None:
    assert approval[field] == expected
    assert len(approval[field]) == 64


def test_dataset_universe_and_meta_limitation_are_preserved(approval: dict) -> None:
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["per_ticker_record_counts"] == approval_service.EXPECTED_RECORD_COUNTS
    assert approval["meta_reduced_record_count_preserved"] is True


def test_selected_signal_families_are_future_execution_only(approval: dict) -> None:
    rows = approval["selected_signal_families"]
    assert [row["signal_family_id"] for row in rows] == (
        approval_service.SELECTED_SIGNAL_FAMILY_IDS
    )
    assert len(rows) == 7
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY"
        and row["generation_performed"] is False
        and row["signal_values_created"] is False
        and row["feature_values_created"] is False
        for row in rows
    )


def test_selected_feature_families_are_future_execution_only(approval: dict) -> None:
    rows = approval["selected_feature_families"]
    assert [row["feature_family_id"] for row in rows] == (
        approval_service.SELECTED_FEATURE_FAMILY_IDS
    )
    assert len(rows) == 8
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY"
        and row["feature_generation_performed"] is False
        and row["feature_values_created"] is False
        and row["target_values_used_as_features"] is False
        for row in rows
    )


def test_supporting_families_are_available_not_selected(approval: dict) -> None:
    rows = approval["supporting_families"]
    assert len(rows) == 5
    assert [row["family_id"] for row in rows] == (
        approval_service.SUPPORTING_SIGNAL_FAMILY_IDS
        + approval_service.SUPPORTING_FEATURE_FAMILY_IDS
    )
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in rows)


def test_feature_groups_preserve_selected_and_supporting_roles(approval: dict) -> None:
    selected = approval["selected_feature_groups"]
    supporting = approval["supporting_feature_groups"]
    assert [row["feature_group_id"] for row in selected] == (
        approval_service.SELECTED_FEATURE_GROUP_IDS
    )
    assert [row["feature_group_id"] for row in supporting] == (
        approval_service.SUPPORTING_FEATURE_GROUP_IDS
    )
    assert len(selected) == 13
    assert len(supporting) == 4
    assert all(row["generation_performed"] is False for row in selected + supporting)


def test_no_peek_rules_and_quality_checks_are_approved_not_executed(
    approval: dict,
) -> None:
    rules = approval["approved_no_peek_and_target_separation_rules"]
    checks = approval["approved_quality_checks"]
    assert len(rules) == 10
    assert len(checks) == 10
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_FEATURE_GENERATION_CONTROL"
        for row in rules
    )
    assert all(
        row["approval_status"]
        == "APPROVED_FOR_FUTURE_FEATURE_GENERATION_QUALITY_CONTROL"
        for row in checks
    )


def test_future_outputs_are_authorized_not_generated(approval: dict) -> None:
    rows = approval["approved_future_outputs"]
    assert len(rows) == 10
    assert all(
        row["approval_status"] == "AUTHORIZED_NOT_GENERATED"
        and row["output_status"] == "PLANNED_NOT_GENERATED"
        and row["generated"] is False
        for row in rows
    )


def test_per_ticker_entries_are_complete_digest_bound_and_closed(approval: dict) -> None:
    rows = approval["per_ticker_signal_or_feature_generation_approval_entries"]
    assert [row["ticker"] for row in rows] == approval_service.TARGET_UNIVERSE
    assert len(rows) == 12
    for row in rows:
        assert row["historical_record_count"] == approval_service.EXPECTED_RECORD_COUNTS[
            row["ticker"]
        ]
        assert row["signal_or_feature_generation_performed"] is False
        assert row["runtime_use"] == "NOT_AUTHORIZED"
        assert row["per_ticker_signal_or_feature_generation_approval_digest"] == (
            approval_service.per_ticker_signal_or_feature_generation_approval_digest_v1(
                row
            )
        )
    assert next(row for row in rows if row["ticker"] == "META")[
        "meta_reduced_record_count_flag"
    ] is True


CLOSED_FALSE_FIELDS = [
    "signal_or_feature_generation_performed",
    "signal_generation_performed",
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
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "target_generation_execution_rerun_performed",
    "target_generation_results_review_rerun_performed",
    "candidate_creation_rerun_performed",
    "candidate_review_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_downstream_and_execution_authorities_remain_closed(
    approval: dict, field: str
) -> None:
    assert approval[field] is False


def test_checklist_is_all_pass(approval: dict) -> None:
    assert approval["approval_summary"]["total_checks"] == 80
    assert approval["approval_summary"]["passed_checks"] == 80
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0
    assert len(approval["approval_checklist"]) == 80
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])


@pytest.mark.parametrize(
    "field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_false_boundary_confirmation(
    attestation: dict, field: str
) -> None:
    mutated = deepcopy(attestation)
    mutated[field] = False
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.build_marketflow_signal_or_feature_generation_approval_v1(
            operator_attestation=mutated
        )


INVALID_ATTESTATION_MUTATIONS = [
    ("operator_decision", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("operator_attestation_phrase", "WRONG"),
    ("operator_attestation_version", "WRONG"),
    ("operator_reference", ""),
    ("operator_attestation_timestamp_utc", ""),
    ("operator_confirms_candidate_review_digest", "0" * 64),
    ("operator_confirms_candidate_digest", "0" * 64),
    ("operator_confirms_target_results_review_digest", "0" * 64),
    ("operator_confirms_target_values_digest", "0" * 64),
    ("operator_confirms_records_digest", "0" * 64),
    ("operator_confirms_target_universe", ["MSFT"]),
    ("operator_confirms_target_count", 11),
    ("operator_confirms_meta_record_count", 1003),
    ("operator_confirms_non_meta_record_count", 913),
    ("operator_confirms_selected_feature_package", "WRONG"),
    ("operator_confirms_selected_label_target_package", "WRONG"),
    ("operator_confirms_selected_objective_path", "WRONG"),
]


@pytest.mark.parametrize(("field", "value"), INVALID_ATTESTATION_MUTATIONS)
def test_builder_rejects_invalid_attestation_field(
    attestation: dict, field: str, value: object
) -> None:
    mutated = deepcopy(attestation)
    mutated[field] = value
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.build_marketflow_signal_or_feature_generation_approval_v1(
            operator_attestation=mutated
        )


INVALID_APPROVAL_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("approval_status", "WRONG"),
    ("approval_scope", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("source_signal_or_feature_generation_candidate_review_digest", "0" * 64),
    ("source_signal_or_feature_generation_candidate_digest", "0" * 64),
    ("source_target_results_review_digest", "0" * 64),
    ("source_target_values_digest", "0" * 64),
    ("records_digest", "0" * 64),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("meta_record_count", 1003),
    ("signal_or_feature_generation_authorized_for_future_execution", False),
    ("signal_or_feature_generation_performed", True),
    ("signal_or_feature_generation_approval_created", False),
    ("ready_for_signal_or_feature_generation_execution", False),
    ("selected_signal_families", []),
    ("selected_feature_families", []),
    ("supporting_families", []),
    ("selected_feature_groups", []),
    ("supporting_feature_groups", []),
    ("approved_no_peek_and_target_separation_rules", []),
    ("approved_quality_checks", []),
    ("approved_future_outputs", []),
    ("per_ticker_signal_or_feature_generation_approval_entries", []),
    ("signal_generation_performed", True),
    ("feature_generation_performed", True),
    ("feature_values_created", True),
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
    ("marketflow_signal_or_feature_generation_approval_digest", None),
]


@pytest.mark.parametrize(("field", "value"), INVALID_APPROVAL_MUTATIONS)
def test_validator_rejects_invalid_approval_field(
    approval: dict, field: str, value: object
) -> None:
    mutated = deepcopy(approval)
    mutated[field] = value
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.validate_marketflow_signal_or_feature_generation_approval_v1(
            mutated
        )


def test_validator_rejects_nested_attestation_mutation(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.validate_marketflow_signal_or_feature_generation_approval_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated["per_ticker_signal_or_feature_generation_approval_entries"][0].pop(
        "per_ticker_signal_or_feature_generation_approval_digest"
    )
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.validate_marketflow_signal_or_feature_generation_approval_v1(
            mutated
        )


def test_source_review_digest_mismatch_fails_closed(
    approval: dict, attestation: dict
) -> None:
    source = approval_service.review_service.build_marketflow_signal_or_feature_generation_candidate_operator_review_v1()
    source["marketflow_signal_or_feature_generation_candidate_operator_review_digest"] = (
        "0" * 64
    )
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.build_marketflow_signal_or_feature_generation_approval_v1(
            source_review=source,
            operator_attestation=attestation,
        )


def test_markdown_includes_required_sections_and_closed_boundaries(
    approval: dict,
) -> None:
    markdown = approval_service.build_marketflow_signal_or_feature_generation_approval_markdown_v1(
        approval
    )
    sections = [
        "Operator Attestation",
        "Source Candidate Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Approval Scope",
        "Selected Feature Package",
        "Selected Target Package and Objective Path",
        "Selected Signal Families",
        "Selected Feature Families",
        "Supporting Families",
        "Selected Feature Groups",
        "No-Peek and Target-Separation Rules",
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
    result = approval_service.write_marketflow_signal_or_feature_generation_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    path = Path(result["path"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    assert result["marketflow_signal_or_feature_generation_approval_digest"] == (
        approval["marketflow_signal_or_feature_generation_approval_digest"]
    )
    with pytest.raises(approval_service.MarketFlowSignalOrFeatureGenerationApprovalError):
        approval_service.write_marketflow_signal_or_feature_generation_approval_v1(
            tmp_path, operator_attestation=attestation
        )


def test_deterministic_approval_digest(approval: dict, attestation: dict) -> None:
    rebuilt = approval_service.build_marketflow_signal_or_feature_generation_approval_v1(
        operator_attestation=attestation
    )
    assert approval == rebuilt
    assert approval["marketflow_signal_or_feature_generation_approval_digest"] == (
        "d174f5d775cb7b423121333838ab74956384068b8a46240760d399f02e229a8c"
    )


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED == approval_service.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED
    assert services.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED == approval_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED
    assert services.SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ONLY == approval_service.SIGNAL_OR_FEATURE_GENERATION_APPROVAL_ONLY
    assert services.build_marketflow_signal_or_feature_generation_approval_attestation_v1 is approval_service.build_marketflow_signal_or_feature_generation_approval_attestation_v1
    assert services.build_marketflow_signal_or_feature_generation_approval_v1 is approval_service.build_marketflow_signal_or_feature_generation_approval_v1
    assert services.validate_marketflow_signal_or_feature_generation_approval_v1 is approval_service.validate_marketflow_signal_or_feature_generation_approval_v1
    assert services.write_marketflow_signal_or_feature_generation_approval_v1 is approval_service.write_marketflow_signal_or_feature_generation_approval_v1
