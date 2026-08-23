"""Offline attestation-bound approval of the MarketFlow expectancy objective."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_expectancy_objective_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_V1 = (
    "marketflow_expectancy_objective_approval_v1"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED = "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED"
EXPECTANCY_OBJECTIVE_APPROVAL_ONLY = "EXPECTANCY_OBJECTIVE_APPROVAL_ONLY"
SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT = (
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
)
APPROVED_PRIMARY_OBJECTIVE_CLUSTER = "CLUSTER_EXPECTANCY_AND_PAYOFF"
APPROVED_SUPPORTING_OBJECTIVE_CLUSTER = "CLUSTER_ABSTENTION_AND_NO_TRADE"
APPROVED_SECONDARY_OBJECTIVE_CLUSTER = "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE"
EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE = (
    review_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
)
OPERATOR_DECISION_APPROVE_EXPECTANCY_OBJECTIVE = "APPROVE_EXPECTANCY_OBJECTIVE"
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_V1 = (
    "marketflow_expectancy_objective_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE EXPECTANCY OBJECTIVE EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT "
    "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE MSFT NVDA AMZN GOOGL META TSLA "
    "JPM XOM JNJ WMT CAT LMT EXPECTANCY_OBJECTIVE_APPROVAL_ONLY"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "baac33f292d77d26eae6eacc4cffaa5cdabe17785cb2c090c053c82d1bfe551d"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    review_service.EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST
)
EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST = (
    review_service.EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST
)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_objective_selected",
    "operator_confirms_objective_approved",
    "operator_confirms_ready_for_design_execution",
    "operator_confirms_no_objective_generation",
    "operator_confirms_no_label_generation",
    "operator_confirms_no_new_targets",
    "operator_confirms_no_feature_generation",
    "operator_confirms_no_feature_label_matrix",
    "operator_confirms_no_backtest_execution",
    "operator_confirms_no_model_training",
    "operator_confirms_no_metric_computation",
    "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]
NEXT_CHAIN = [
    "Expectancy Objective Design Execution v1, if approved.",
    "Expectancy Objective Results Review v1.",
    "Future label/target generation candidate only after separate approval.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_objective_design_execution_if_approved",
    "expectancy_objective_results_review",
    "objective_label_or_target_generation_candidate",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_generate_labels",
    "approval_does_not_create_targets",
    "approval_does_not_generate_features",
    "approval_does_not_create_feature_label_matrix",
    "approval_does_not_run_backtest",
    "approval_does_not_train_models",
    "approval_does_not_compute_metrics",
    "approval_does_not_score_strategy",
    "approval_does_not_generate_trade_recommendations",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_call_providers",
    "approval_does_not_acquire_market_data",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowExpectancyObjectiveApprovalError(ValueError):
    """Raised when approval evidence violates the approval-only boundary."""


def build_marketflow_expectancy_objective_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_strategy_charter_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_objective_path: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_objective_selected: bool,
    operator_confirms_objective_approved: bool,
    operator_confirms_ready_for_design_execution: bool,
    operator_confirms_no_objective_generation: bool,
    operator_confirms_no_label_generation: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_feature_generation: bool,
    operator_confirms_no_feature_label_matrix: bool,
    operator_confirms_no_backtest_execution: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_metric_computation: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_objective_path: str = SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
    approved_strategy_direction: str = EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
    operator_decision: str = OPERATOR_DECISION_APPROVE_EXPECTANCY_OBJECTIVE,
) -> dict:
    """Build a non-secret attestation; approval validates every field exactly."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_V1
        )
    }


@lru_cache(maxsize=1)
def _canonical_source_review() -> dict:
    return review_service.build_marketflow_expectancy_objective_candidate_operator_review_v1()


def _source_review(source_review: dict | None) -> dict:
    if source_review is None:
        return deepcopy(_canonical_source_review())
    source = deepcopy(source_review)
    validation = (
        review_service.validate_marketflow_expectancy_objective_candidate_operator_review_v1(
            source
        )
    )
    if (
        validation[
            "marketflow_expectancy_objective_candidate_operator_review_digest"
        ]
        != EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveApprovalError(
            "source candidate review digest mismatch"
        )
    return source


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowExpectancyObjectiveApprovalError(
            "operator_attestation missing"
        )
    source = _canonical_source_review()
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_EXPECTANCY_OBJECTIVE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "approved_strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_V1,
        "operator_confirms_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        "operator_confirms_records_digest": source["records_digest"],
        "operator_confirms_target_universe": source["target_universe"],
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowExpectancyObjectiveApprovalError(f"{field} mismatch")
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowExpectancyObjectiveApprovalError(f"{field} must be true")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowExpectancyObjectiveApprovalError(f"{field} required")


def _approved_families(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "approval_status": "APPROVED_FOR_FUTURE_OBJECTIVE_DESIGN_EXECUTION_ONLY",
            "objective_status": value["candidate_status"],
            "label_generation_authorized": False,
            "target_creation_authorized": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for name, value in source["reviewed_objective_families"].items()
    }


def _approved_clusters(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    statuses = {
        APPROVED_PRIMARY_OBJECTIVE_CLUSTER: "APPROVED_PRIMARY_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION",
        APPROVED_SUPPORTING_OBJECTIVE_CLUSTER: "APPROVED_SUPPORTING_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION",
        APPROVED_SECONDARY_OBJECTIVE_CLUSTER: "APPROVED_SECONDARY_CLUSTER_FOR_FUTURE_DESIGN_EXECUTION",
        "CLUSTER_CONTEXTUAL_SELECTION": "APPROVED_AVAILABLE_CONTEXTUAL_CLUSTER_FOR_FUTURE_REVIEW",
    }
    return {
        name: {
            "objective_families": deepcopy(value["objective_families"]),
            "source_review_status": value["review_status"],
            "approval_status": statuses[name],
        }
        for name, value in source["reviewed_objective_clusters"].items()
    }


def _approved_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question": value["question"],
            "approval_status": "APPROVED_FOR_FUTURE_OBJECTIVE_DESIGN_RESEARCH_ONLY",
            "answered_by_this_approval": False,
            "requires_future_research": True,
        }
        for value in source["reviewed_research_questions"]
    ]


def _approved_dimensions(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "approval_status": "APPROVED_FOR_FUTURE_OBJECTIVE_DESIGN_EXECUTION_ONLY",
            "dimension_status": value["dimension_status"],
            "generation_authorized": False,
            "metric_computation_authorized": False,
        }
        for name, value in source["reviewed_design_dimensions"].items()
    }


def _approved_future_outputs(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "approval_status": "AUTHORIZED_NOT_GENERATED",
            "output_status": value["output_status"],
            "research_only": True,
            "non_actionable": True,
        }
        for name, value in source["reviewed_future_outputs"].items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_objective_approval_digest", None)
    return payload


def per_ticker_expectancy_objective_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker approval entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_expectancy_objective_candidate_review_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "strategy_charter_approval_status": row["strategy_charter_approval_status"],
            "expectancy_objective_candidate_review_status": source["review_status"],
            "expectancy_objective_approval_status": "APPROVED_FOR_FUTURE_OBJECTIVE_DESIGN_EXECUTION_ONLY",
            "strategy_direction": source["strategy_direction"],
            "selected_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "expectancy_objective_selected": True,
            "expectancy_objective_approved": True,
            "expectancy_objective_generation_authorized": False,
            "label_generation_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
            "backtest_execution_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_APPROVAL"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_objective_approval_digest"] = (
            per_ticker_expectancy_objective_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(value)
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _base_approval(
    source: Mapping[str, Any],
    attestation: Mapping[str, Any],
) -> dict[str, Any]:
    approval = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_V1,
        "approval_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVED,
        "approval_scope": EXPECTANCY_OBJECTIVE_APPROVAL_ONLY,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "approved_primary_objective_cluster": APPROVED_PRIMARY_OBJECTIVE_CLUSTER,
        "approved_supporting_objective_cluster": APPROVED_SUPPORTING_OBJECTIVE_CLUSTER,
        "approved_secondary_objective_cluster": APPROVED_SECONDARY_OBJECTIVE_CLUSTER,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_expectancy_objective_candidate_review_artifact_kind": source["artifact_kind"],
        "source_expectancy_objective_candidate_review_status": source["review_status"],
        "source_expectancy_objective_candidate_review_scope": source["review_scope"],
        "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_objective_candidate_artifact_kind": source["source_expectancy_objective_candidate_artifact_kind"],
        "source_expectancy_objective_candidate_status": source["source_expectancy_objective_candidate_status"],
        "source_expectancy_objective_candidate_scope": source["source_expectancy_objective_candidate_scope"],
        "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        "source_strategy_charter_digest": source["source_strategy_charter_digest"],
        **_source_digest_chain(source),
    }
    approval.update(
        {
            "expectancy_objective_candidate_created": True,
            "expectancy_objective_candidate_ready_for_operator_review": True,
            "expectancy_objective_candidate_review_created": True,
            "expectancy_objective_candidate_review_ready": True,
            "expectancy_objective_selected": True,
            "expectancy_objective_approved": True,
            "expectancy_objective_authorized": True,
            "expectancy_objective_approval_created": True,
            "ready_for_expectancy_objective_design_execution": True,
            "expectancy_objective_generation_authorized": False,
            "expectancy_objective_generation_performed": False,
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "backtest_execution_authorized": False,
            "backtest_execution_performed": False,
            "model_training_authorized": False,
            "model_training_performed": False,
            "metric_computation_authorized": False,
            "metric_computation_performed": False,
            "strategy_scoring_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_recommended": False,
            "profitability": NOT_ACCEPTED,
            "profitability_acceptance_ready": False,
            "profitability_acceptance_recommended": False,
            "runtime_migration_approved": False,
            "runtime_migration_active": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "automatic_stitching": False,
            "new_strategy_scoring_performed": False,
            "trade_recommendations_generated": False,
            "provider_requests_made_in_approval": False,
            "live_provider_transport_enabled_in_approval": False,
            "market_data_acquisition_performed_in_approval": False,
            "dataset_generation_performed_in_approval": False,
            "canonical_dataset_regenerated_in_approval": False,
            "raw_provider_payloads_committed": False,
            "api_keys_stored_or_printed": False,
        }
    )
    copied_fields = [
        "dataset_name", "source_profile", "timeframe", "date_range_start",
        "date_range_end", "target_universe", "target_universe_count",
        "total_canonical_record_count", "per_ticker_record_counts",
        "meta_record_count", "non_meta_record_count",
        "meta_reduced_record_count_preserved", "strategy_direction",
        "marketflow_algorithm_identity", "core_philosophy", "previous_chain_status",
        "previous_predictive_usefulness_decision", "previous_acceptance_readiness_decision",
        "previous_runtime_decision", "previous_profitability_decision",
        "previous_operator_selected_option", "matrix_row_count",
        "evaluable_matrix_row_count", "unavailable_target_count", "oos_row_count",
        "majority_accuracy", "local_model_accuracy", "cross_sectional_accuracy",
        "cross_sectional_delta_vs_majority", "majority_brier", "local_model_brier",
        "cross_sectional_brier", "optional_tree_model_status",
        "optional_ensemble_model_status", "leakage_control_passed",
        "leakage_failed_control_count", "leakage_control_count",
        "majority_structure_risk", "largest_aggregated_class",
        "largest_aggregated_class_count", "no_trade_count",
        "objective_candidate_philosophy", "objective_candidate_primary_question",
        "objective_candidate_secondary_question",
    ]
    approval.update({field: deepcopy(source[field]) for field in copied_fields})
    approval.update(
        {
            "approved_objective_philosophy": {
                "objective_candidate_philosophy": source["objective_candidate_philosophy"],
                "objective_candidate_primary_question": source["objective_candidate_primary_question"],
                "objective_candidate_secondary_question": source["objective_candidate_secondary_question"],
                "approved_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
                "approved_objective_boundary": "Approval-only; no label, target, feature, metric, backtest, model, or strategy artifact is generated.",
            },
            "approved_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "approved_objective_boundary": "Approval-only; no label, target, feature, metric, backtest, model, or strategy artifact is generated.",
            "approved_objective_families": _approved_families(source),
            "approved_objective_clusters": _approved_clusters(source),
            "approved_research_questions": _approved_questions(source),
            "approved_design_dimensions": _approved_dimensions(source),
            "approved_future_outputs": _approved_future_outputs(source),
            "per_ticker_expectancy_objective_approval_entries": _per_ticker_entries(source),
            "next_chain": list(NEXT_CHAIN),
            "next_gates": list(NEXT_GATES),
            "risk_controls": list(RISK_CONTROLS),
            "no_tracked_marketflow_files": True,
        }
    )
    return approval


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(entry, dict)
        and isinstance(entry.get("per_ticker_expectancy_objective_approval_digest"), str)
        and entry["per_ticker_expectancy_objective_approval_digest"]
        == per_ticker_expectancy_objective_approval_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(approval: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = _canonical_source_review()
    operator = approval.get("operator_attestation", {})
    entries = approval.get("per_ticker_expectancy_objective_approval_entries", [])
    return [
        ("source_candidate_review_digest_bound", EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST, approval.get("source_expectancy_objective_candidate_review_digest")),
        ("source_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, approval.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST, approval.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_review_digest_bound", source["source_strategy_charter_review_digest"], approval.get("source_strategy_charter_review_digest")),
        ("source_strategy_charter_digest_bound", source["source_strategy_charter_digest"], approval.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", source["source_final_archive_digest"], approval.get("source_final_archive_digest")),
        ("source_archive_digest_bound", source["source_archive_digest"], approval.get("source_archive_digest")),
        ("source_selection_digest_bound", source["source_selection_digest"], approval.get("source_selection_digest")),
        ("source_closure_digest_bound", source["source_closure_digest"], approval.get("source_closure_digest")),
        ("source_readiness_digest_bound", source["source_readiness_digest"], approval.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", source["source_reassessment_digest"], approval.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", source["source_results_review_digest"], approval.get("source_results_review_digest")),
        ("source_execution_digest_bound", source["source_execution_digest"], approval.get("source_execution_digest")),
        ("matrix_digest_bound", source["feature_label_matrix_digest"], approval.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", source["feature_values_digest"], approval.get("feature_values_digest")),
        ("label_values_digest_bound", source["redesigned_label_values_digest"], approval.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", source["research_registry_approval_digest"], approval.get("research_registry_approval_digest")),
        ("records_digest_bound", source["records_digest"], approval.get("records_digest")),
        ("target_universe_12_preserved", source["target_universe"], approval.get("target_universe")),
        ("records_digest_preserved", source["records_digest"], approval.get("records_digest")),
        ("meta_913_preserved", 913, approval.get("meta_record_count")),
        ("operator_decision_matches", OPERATOR_DECISION_APPROVE_EXPECTANCY_OBJECTIVE, operator.get("operator_decision")),
        ("operator_attestation_phrase_matches", REQUIRED_MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        ("approval_scope_only", EXPECTANCY_OBJECTIVE_APPROVAL_ONLY, approval.get("approval_scope")),
        ("selected_objective_path_expectancy_payoff_with_abstention", SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT, approval.get("selected_objective_path")),
        ("objective_selected_true", True, approval.get("expectancy_objective_selected")),
        ("objective_approved_true", True, approval.get("expectancy_objective_approved")),
        ("objective_authorized_true", True, approval.get("expectancy_objective_authorized")),
        ("approval_created_true", True, approval.get("expectancy_objective_approval_created")),
        ("ready_for_design_execution_true", True, approval.get("ready_for_expectancy_objective_design_execution")),
        ("objective_generation_authorized_false", False, approval.get("expectancy_objective_generation_authorized")),
        ("label_generation_authorized_false", False, approval.get("label_generation_authorized")),
        ("new_targets_created_false", False, approval.get("new_targets_created")),
        ("feature_generation_authorized_false", False, approval.get("feature_generation_authorized")),
        ("feature_label_matrix_created_false", False, approval.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, approval.get("backtest_execution_authorized")),
        ("model_training_authorized_false", False, approval.get("model_training_authorized")),
        ("metric_computation_authorized_false", False, approval.get("metric_computation_authorized")),
        ("strategy_scoring_false", False, approval.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, approval.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, approval.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, approval.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, approval.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, approval.get("broker_execution")),
        ("trade_recommendations_false", False, approval.get("trade_recommendations_generated")),
        ("approved_objective_philosophy_present", True, bool(approval.get("approved_objective_philosophy"))),
        ("approved_objective_families_10", 10, len(approval.get("approved_objective_families", {}))),
        ("approved_objective_clusters_present", 4, len(approval.get("approved_objective_clusters", {}))),
        ("approved_research_questions_10", 10, len(approval.get("approved_research_questions", []))),
        ("approved_design_dimensions_12", 12, len(approval.get("approved_design_dimensions", {}))),
        ("approved_future_outputs_11", 11, len(approval.get("approved_future_outputs", {}))),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, approval.get("provider_requests_made_in_approval")),
        ("market_data_acquisition_false", False, approval.get("market_data_acquisition_performed_in_approval")),
        ("dataset_regeneration_false", False, approval.get("canonical_dataset_regenerated_in_approval")),
        ("raw_provider_payloads_not_committed", False, approval.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, approval.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, approval.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, approval.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, approval.get("risk_controls")),
        ("no_tracked_marketflow_files", True, approval.get("no_tracked_marketflow_files")),
    ]


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(approval)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = sum(row.get("status") != PASS for row in rows)
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - failed,
        "failed_checks": failed,
        "blocker_count": sum(
            row.get("status") != PASS and row.get("severity") == BLOCKER
            for row in rows
        ),
        "expectancy_objective_selected": True,
        "expectancy_objective_approved": True,
        "expectancy_objective_authorized": True,
        "ready_for_expectancy_objective_design_execution": True,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH_EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "objective_generation_authorized": False,
        "label_generation_authorized": False,
        "new_targets_created": False,
        "feature_generation_authorized": False,
        "backtest_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(approval))
    payload.pop("approval_checklist", None)
    payload.pop("approval_summary", None)
    payload.pop("marketflow_expectancy_objective_approval_digest", None)
    return payload


def marketflow_expectancy_objective_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    return semantic_digest(_digest_payload(approval))


def build_marketflow_expectancy_objective_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build approval for future objective design execution only."""
    source = _source_review(source_review)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    approval["marketflow_expectancy_objective_approval_digest"] = (
        marketflow_expectancy_objective_approval_digest_v1(approval)
    )
    validate_marketflow_expectancy_objective_approval_v1(approval)
    return approval


def validate_marketflow_expectancy_objective_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, bindings, approved catalogs, and closed authorities."""
    if not isinstance(approval, dict):
        raise MarketFlowExpectancyObjectiveApprovalError(
            "approval must be an object"
        )
    source = _source_review(None)
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(source, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowExpectancyObjectiveApprovalError(f"{field} mismatch")
    expected_checklist = _checklist(approval)
    if approval.get("approval_checklist") != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowExpectancyObjectiveApprovalError(
            "approval checklist mismatch"
        )
    if approval.get("approval_summary") != _summary(expected_checklist):
        raise MarketFlowExpectancyObjectiveApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get("marketflow_expectancy_objective_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyObjectiveApprovalError("approval digest missing")
    if digest != marketflow_expectancy_objective_approval_digest_v1(approval):
        raise MarketFlowExpectancyObjectiveApprovalError("approval digest mismatch")
    return {
        "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "selected_objective_path": approval["selected_objective_path"],
        "marketflow_expectancy_objective_approval_digest": digest,
        **{
            key: approval["approval_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_expectancy_objective_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval artifact."""
    validation = validate_marketflow_expectancy_objective_approval_v1(approval)
    operator = approval["operator_attestation"]
    sections = [
        ("Title", ["Expectancy Objective Approval v1"]),
        ("Expectancy Objective Approval v1", [
            "Artifact/status/scope: "
            f"{approval['artifact_kind']} / {approval['approval_status']} / "
            f"{approval['approval_scope']}.",
            "Approval digest: "
            f"{validation['marketflow_expectancy_objective_approval_digest']}.",
        ]),
        ("Operator Attestation", [
            "Decision/reference/timestamp: "
            f"{operator['operator_decision']} / {operator['operator_reference']} / "
            f"{operator['operator_attestation_timestamp_utc']}.",
            f"Exact phrase: {operator['operator_attestation_phrase']}.",
        ]),
        ("Source Expectancy Objective Candidate Review", [
            "Artifact/status/scope: "
            f"{approval['source_expectancy_objective_candidate_review_artifact_kind']} / "
            f"{approval['source_expectancy_objective_candidate_review_status']} / "
            f"{approval['source_expectancy_objective_candidate_review_scope']}.",
            f"Digest: {approval['source_expectancy_objective_candidate_review_digest']}.",
        ]),
        ("Bound Evidence", [
            "Candidate/charter approval/records: "
            f"{approval['source_expectancy_objective_candidate_digest']} / "
            f"{approval['source_strategy_charter_approval_digest']} / "
            f"{approval['records_digest']}.",
            "Matrix/features/labels: "
            f"{approval['feature_label_matrix_digest']} / "
            f"{approval['feature_values_digest']} / "
            f"{approval['redesigned_label_values_digest']}.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: {approval['dataset_name']} / "
            f"{approval['total_canonical_record_count']}.",
            "Universe: " + ", ".join(approval["target_universe"]) + ".",
            "META remains 913; every non-META ticker remains 1003.",
        ]),
        ("Approved Objective Basis", [
            f"Direction: {approval['strategy_direction']}.",
            f"Core philosophy: {approval['core_philosophy']}",
            f"Previous chain remains {approval['previous_chain_status']} context.",
        ]),
        ("Approved Objective Philosophy", [
            approval["objective_candidate_philosophy"],
            approval["objective_candidate_primary_question"],
            approval["objective_candidate_secondary_question"],
            approval["approved_objective_boundary"],
        ]),
        ("Approved Objective Path", [
            f"Selected path: {approval['selected_objective_path']}.",
            "Approved for future objective design execution only.",
        ]),
        ("Approved Objective Families", [
            f"{name}: {value['approval_status']}."
            for name, value in approval["approved_objective_families"].items()
        ]),
        ("Approved Objective Clusters", [
            f"{name}: {value['approval_status']}."
            for name, value in approval["approved_objective_clusters"].items()
        ]),
        ("Approved Research Questions", [
            f"{value['question']} {value['approval_status']}."
            for value in approval["approved_research_questions"]
        ]),
        ("Approved Design Dimensions", [
            f"{name}: {value['approval_status']}."
            for name, value in approval["approved_design_dimensions"].items()
        ]),
        ("Approved Future Outputs", [
            f"{name}: {value['approval_status']}."
            for name, value in approval["approved_future_outputs"].items()
        ]),
        ("Per-Ticker Approval Summary", [
            f"{row['ticker']}: {row['expectancy_objective_approval_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_expectancy_objective_approval_digest']}."
            for row in approval["per_ticker_expectancy_objective_approval_entries"]
        ]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted."
        ]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            "Total/passed/failed/blockers: "
            f"{approval['approval_summary']['total_checks']} / "
            f"{approval['approval_summary']['passed_checks']} / "
            f"{approval['approval_summary']['failed_checks']} / "
            f"{approval['approval_summary']['blocker_count']}."
        ]),
        ("Guardrails", [
            "This approval authorizes future objective design execution only. It "
            "creates no labels, targets, features, matrix, backtest, model, metric, "
            "scoring, recommendation, acceptance, profitability, runtime, provider, "
            "market-data, paper-trading, or broker authority."
        ]),
    ]
    lines = ["# Expectancy Objective Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_expectancy_objective_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_expectancy_objective_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    validation = validate_marketflow_expectancy_objective_approval_v1(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_expectancy_objective_approval_v1.json"
    if path.exists():
        raise MarketFlowExpectancyObjectiveApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "selected_objective_path": approval["selected_objective_path"],
        "marketflow_expectancy_objective_approval_digest": validation[
            "marketflow_expectancy_objective_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
