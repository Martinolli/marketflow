"""Offline attestation-bound approval for the MarketFlow strategy charter."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_algorithm_strategy_charter_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED = (
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1 = (
    "marketflow_algorithm_strategy_charter_approval_v1"
)
MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED = (
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED"
)
STRATEGY_CHARTER_APPROVAL_ONLY = "STRATEGY_CHARTER_APPROVAL_ONLY"
EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE = (
    review_service.charter_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
)
OPERATOR_DECISION_APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER = (
    "APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER"
)
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1 = (
    "marketflow_algorithm_strategy_charter_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE MARKETFLOW ALGORITHM STRATEGY CHARTER "
    "EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE MSFT NVDA AMZN GOOGL META TSLA "
    "JPM XOM JNJ WMT CAT LMT STRATEGY_CHARTER_APPROVAL_ONLY"
)
EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST = (
    "d75e541f3f9d16593eb3a4da6f4f6de7a451c259295ce4e3e8f09171bbcbe8f9"
)
EXPECTED_SOURCE_CHARTER_DIGEST = review_service.EXPECTED_SOURCE_CHARTER_DIGEST

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_charter_approved",
    "operator_confirms_ready_for_expectancy_objective_candidate",
    "operator_confirms_expectancy_objective_candidate_not_created",
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
    "Expectancy Objective Candidate v1.",
    "Expectancy Objective Candidate Operator Review v1.",
    "Expectancy Objective Approval v1.",
    "Future objective/label generation only after separate approval.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff rule baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and reassessment only after execution artifacts exist.",
    "Predictive usefulness remains not accepted until a new evidence chain passes readiness.",
    "Profitability and runtime remain separately gated.",
]
NEXT_GATES = [
    "expectancy_objective_candidate_creation",
    "expectancy_objective_candidate_operator_review",
    "expectancy_objective_approval",
    "objective_or_label_generation_approval",
    "signal_or_feature_generation_approval",
    "vpa_wyckoff_rule_baseline_approval",
    "expectancy_backtest_lab_approval",
    "results_review_and_reassessment",
    "paper_research_readiness_review",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_create_expectancy_objective_candidate",
    "approval_does_not_create_labels",
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


class MarketFlowAlgorithmStrategyCharterApprovalError(ValueError):
    """Raised when approval evidence violates the charter-only boundary."""


def build_marketflow_algorithm_strategy_charter_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_charter_review_digest: str,
    operator_confirms_charter_digest: str,
    operator_confirms_final_archive_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_strategy_direction: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_charter_approved: bool,
    operator_confirms_ready_for_expectancy_objective_candidate: bool,
    operator_confirms_expectancy_objective_candidate_not_created: bool,
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
    approved_strategy_direction: str = EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
    operator_decision: str = OPERATOR_DECISION_APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER,
) -> dict:
    """Build a non-secret operator attestation; approval validates every field."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1
        )
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "operator_attestation missing"
        )
    source = review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER,
        "approved_strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1,
        "operator_confirms_charter_review_digest": EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST,
        "operator_confirms_charter_digest": EXPECTED_SOURCE_CHARTER_DIGEST,
        "operator_confirms_final_archive_digest": source["source_final_archive_digest"],
        "operator_confirms_records_digest": source["records_digest"],
        "operator_confirms_target_universe": source["target_universe"],
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowAlgorithmStrategyCharterApprovalError(
                f"{field} mismatch"
            )
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowAlgorithmStrategyCharterApprovalError(
                f"{field} must be true"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowAlgorithmStrategyCharterApprovalError(
                f"{field} required"
            )


def _source_review(source_review: dict | None) -> dict:
    source = (
        review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
        if source_review is None
        else deepcopy(source_review)
    )
    validation = (
        review_service.validate_marketflow_algorithm_strategy_charter_operator_review_v1(
            source
        )
    )
    if (
        validation["marketflow_algorithm_strategy_charter_operator_review_digest"]
        != EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST
    ):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "source charter review digest mismatch"
        )
    return source


def _approved_catalog(
    source: Mapping[str, Mapping[str, Any]],
    *,
    approval_status: str,
    source_status_key: str,
    status_key: str,
    authorization_fields: tuple[str, ...] = (),
) -> dict[str, dict[str, Any]]:
    approved = {}
    for name, value in source.items():
        row = {
            "approval_status": approval_status,
            status_key: value[source_status_key],
            "research_only": True,
            "non_actionable": True,
        }
        row.update({field: False for field in authorization_fields})
        approved[name] = row
    return approved


def _approved_principles(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY",
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for name in source["reviewed_strategy_principles"]
    }


def _approved_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question": row["question"],
            "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY",
            "answered_by_this_approval": False,
            "requires_future_research": True,
        }
        for row in source["reviewed_research_questions"]
    ]


def _approved_objectives(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _approved_catalog(
        source["reviewed_objective_families"],
        approval_status="APPROVED_FOR_FUTURE_EXPECTANCY_OBJECTIVE_CANDIDACY_ONLY",
        source_status_key="objective_status",
        status_key="objective_status",
        authorization_fields=("label_generation_authorized", "target_creation_authorized"),
    )


def _approved_signals(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _approved_catalog(
        source["reviewed_signal_families"],
        approval_status="APPROVED_FOR_FUTURE_SIGNAL_CANDIDACY_ONLY",
        source_status_key="signal_status",
        status_key="signal_status",
        authorization_fields=("feature_generation_authorized",),
    )


def _approved_metrics(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _approved_catalog(
        source["reviewed_validation_metrics"],
        approval_status="APPROVED_FOR_FUTURE_METRIC_CANDIDACY_ONLY",
        source_status_key="metric_status",
        status_key="metric_status",
        authorization_fields=("metric_computation_authorized",),
    )


def _approved_baselines(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _approved_catalog(
        source["reviewed_baselines"],
        approval_status="APPROVED_FOR_FUTURE_BASELINE_CANDIDACY_ONLY",
        source_status_key="baseline_status",
        status_key="baseline_status",
        authorization_fields=("model_training_authorized", "backtest_authorized"),
    )


def _approved_phase_plan(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    statuses = [
        "COMPLETED_BY_SOURCE_ARTIFACT",
        "FUTURE_READY_FOR_CANDIDATE_CREATION",
        *(["FUTURE_NOT_STARTED"] * 7),
    ]
    return {
        name: {
            "approval_status": "APPROVED_AS_FUTURE_STAGED_PLAN_ONLY",
            "status": statuses[index],
            "source_status": value["status"],
        }
        for index, (name, value) in enumerate(source["reviewed_phase_plan"].items())
    }


def _approved_gates(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "approval_status": "APPROVED_AS_FUTURE_GATE_ONLY",
            "gate_status": value["gate_status"],
            "approval_created": False,
            "execution_created": False,
            "opened_by_this_approval": False,
        }
        for name, value in source["reviewed_acceptance_gates"].items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_strategy_charter_approval_digest", None)
    return payload


def per_ticker_marketflow_algorithm_strategy_charter_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker approval entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_strategy_charter_review_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "source_charter_status": row["source_charter_status"],
            "strategy_charter_review_status": source["review_status"],
            "strategy_charter_approval_status": "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY",
            "strategy_direction": source["strategy_direction"],
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_charter_review_digest": EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST,
            "source_charter_digest": EXPECTED_SOURCE_CHARTER_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER_APPROVAL"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_strategy_charter_approval_digest"] = (
            per_ticker_marketflow_algorithm_strategy_charter_approval_digest_v1(entry)
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
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_V1,
        "approval_status": MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVED,
        "approval_scope": STRATEGY_CHARTER_APPROVAL_ONLY,
        "approved_strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_charter_review_artifact_kind": source["artifact_kind"],
        "source_charter_review_status": source["review_status"],
        "source_charter_review_scope": source["review_scope"],
        "source_charter_review_digest": EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST,
        "source_charter_artifact_kind": source["source_charter_artifact_kind"],
        "source_charter_status": source["source_charter_status"],
        "source_charter_digest": EXPECTED_SOURCE_CHARTER_DIGEST,
        "source_strategy_direction": source["source_strategy_direction"],
        **_source_digest_chain(source),
    }
    approval.update(
        {
            "marketflow_algorithm_strategy_charter_created": True,
            "marketflow_algorithm_strategy_charter_ready_for_operator_review": True,
            "marketflow_algorithm_strategy_charter_review_created": True,
            "marketflow_algorithm_strategy_charter_review_ready": True,
            "marketflow_algorithm_strategy_charter_approved": True,
            "marketflow_algorithm_strategy_charter_authorized": True,
            "marketflow_algorithm_strategy_charter_approval_created": True,
            "ready_for_expectancy_objective_candidate": True,
            "expectancy_objective_candidate_created": False,
            "expectancy_objective_generation_authorized": False,
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
        "dataset_name", "source_profile", "timeframe", "date_range_start", "date_range_end",
        "target_universe", "target_universe_count", "total_canonical_record_count",
        "per_ticker_record_counts", "meta_record_count", "non_meta_record_count",
        "meta_reduced_record_count_preserved", "previous_chain_status",
        "previous_predictive_usefulness_decision", "previous_acceptance_readiness_decision",
        "previous_runtime_decision", "previous_profitability_decision", "previous_reason",
        "previous_operator_selected_option", "matrix_row_count", "evaluable_matrix_row_count",
        "unavailable_target_count", "oos_row_count", "majority_accuracy",
        "local_model_accuracy", "cross_sectional_accuracy",
        "cross_sectional_delta_vs_majority", "majority_brier", "local_model_brier",
        "cross_sectional_brier", "optional_tree_model_status",
        "optional_ensemble_model_status", "leakage_control_passed",
        "leakage_failed_control_count", "leakage_control_count", "majority_structure_risk",
        "largest_aggregated_class", "largest_aggregated_class_count", "no_trade_count",
        "strategy_direction", "marketflow_algorithm_identity", "marketflow_algorithm_definition",
        "core_philosophy", "primary_question", "secondary_question",
    ]
    approval.update({field: deepcopy(source[field]) for field in copied_fields})
    approval.update(
        {
            "approved_strategy_philosophy": {
                "marketflow_algorithm_identity": source["marketflow_algorithm_identity"],
                "marketflow_algorithm_definition": source["marketflow_algorithm_definition"],
                "core_philosophy": source["core_philosophy"],
                "primary_question": source["primary_question"],
                "secondary_question": source["secondary_question"],
                "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_ONLY",
                "research_only": True,
                "non_actionable": True,
            },
            "approved_strategy_principles": _approved_principles(source),
            "approved_research_questions": _approved_questions(source),
            "approved_objective_families": _approved_objectives(source),
            "approved_signal_families": _approved_signals(source),
            "approved_validation_metrics": _approved_metrics(source),
            "approved_baselines": _approved_baselines(source),
            "approved_phase_plan": _approved_phase_plan(source),
            "approved_acceptance_gates": _approved_gates(source),
            "non_goals": deepcopy(source["reviewed_non_goals"]),
            "per_ticker_strategy_charter_approval_entries": _per_ticker_entries(source),
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
        and isinstance(entry.get("per_ticker_strategy_charter_approval_digest"), str)
        and entry["per_ticker_strategy_charter_approval_digest"]
        == per_ticker_marketflow_algorithm_strategy_charter_approval_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(approval: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = review_service.build_marketflow_algorithm_strategy_charter_operator_review_v1()
    operator = approval.get("operator_attestation", {})
    entries = approval.get("per_ticker_strategy_charter_approval_entries", [])
    return [
        ("source_charter_review_digest_bound", EXPECTED_SOURCE_CHARTER_REVIEW_DIGEST, approval.get("source_charter_review_digest")),
        ("source_charter_digest_bound", EXPECTED_SOURCE_CHARTER_DIGEST, approval.get("source_charter_digest")),
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
        ("operator_decision_matches", OPERATOR_DECISION_APPROVE_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER, operator.get("operator_decision")),
        ("operator_attestation_phrase_matches", REQUIRED_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        ("approval_scope_only", STRATEGY_CHARTER_APPROVAL_ONLY, approval.get("approval_scope")),
        ("strategy_direction_expectancy_first", EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE, approval.get("approved_strategy_direction")),
        ("strategy_charter_approved_true", True, approval.get("marketflow_algorithm_strategy_charter_approved")),
        ("strategy_charter_authorized_true", True, approval.get("marketflow_algorithm_strategy_charter_authorized")),
        ("strategy_charter_approval_created_true", True, approval.get("marketflow_algorithm_strategy_charter_approval_created")),
        ("ready_for_expectancy_objective_candidate_true", True, approval.get("ready_for_expectancy_objective_candidate")),
        ("expectancy_objective_candidate_created_false", False, approval.get("expectancy_objective_candidate_created")),
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
        ("approved_strategy_philosophy_present", True, bool(approval.get("approved_strategy_philosophy"))),
        ("approved_strategy_principles_10", 10, len(approval.get("approved_strategy_principles", {}))),
        ("approved_research_questions_10", 10, len(approval.get("approved_research_questions", []))),
        ("approved_objective_families_10", 10, len(approval.get("approved_objective_families", {}))),
        ("approved_signal_families_10", 10, len(approval.get("approved_signal_families", {}))),
        ("approved_validation_metrics_14", 14, len(approval.get("approved_validation_metrics", {}))),
        ("approved_baselines_7", 7, len(approval.get("approved_baselines", {}))),
        ("approved_phase_plan_9", 9, len(approval.get("approved_phase_plan", {}))),
        ("approved_acceptance_gates_10", 10, len(approval.get("approved_acceptance_gates", {}))),
        ("non_goals_preserved", source["reviewed_non_goals"], approval.get("non_goals")),
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
            row.get("status") != PASS and row.get("severity") == BLOCKER for row in rows
        ),
        "strategy_charter_approved": True,
        "strategy_charter_authorized": True,
        "ready_for_expectancy_objective_candidate": True,
        "strategy_direction": EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "expectancy_objective_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(approval))
    payload.pop("approval_checklist", None)
    payload.pop("approval_summary", None)
    payload.pop("marketflow_algorithm_strategy_charter_approval_digest", None)
    return payload


def marketflow_algorithm_strategy_charter_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    return semantic_digest(_digest_payload(approval))


def build_marketflow_algorithm_strategy_charter_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build charter-only approval from an exact review and explicit attestation."""
    source = _source_review(source_review)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    approval["marketflow_algorithm_strategy_charter_approval_digest"] = (
        marketflow_algorithm_strategy_charter_approval_digest_v1(approval)
    )
    validate_marketflow_algorithm_strategy_charter_approval_v1(approval)
    return approval


def validate_marketflow_algorithm_strategy_charter_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, source bindings, catalogs, and closed authorities."""
    if not isinstance(approval, dict):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval must be an object"
        )
    source = _source_review(None)
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(source, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowAlgorithmStrategyCharterApprovalError(
                f"{field} mismatch"
            )
    checklist = approval.get("approval_checklist")
    expected_checklist = _checklist(approval)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval checklist mismatch"
        )
    if approval.get("approval_summary") != _summary(expected_checklist):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get("marketflow_algorithm_strategy_charter_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval digest missing"
        )
    if digest != marketflow_algorithm_strategy_charter_approval_digest_v1(approval):
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval digest mismatch"
        )
    return {
        "status": "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "approved_strategy_direction": approval["approved_strategy_direction"],
        "marketflow_algorithm_strategy_charter_approval_digest": digest,
        **{
            key: approval["approval_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_algorithm_strategy_charter_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of a validated approval artifact."""
    validation = validate_marketflow_algorithm_strategy_charter_approval_v1(approval)
    operator = approval["operator_attestation"]
    sections = [
        ("Title", ["MarketFlow Algorithm Strategy Charter Approval"]),
        ("MarketFlow Algorithm Strategy Charter Approval", [
            "Artifact/status/scope: "
            f"{approval['artifact_kind']} / {approval['approval_status']} / "
            f"{approval['approval_scope']}.",
            "Approval digest: "
            f"{validation['marketflow_algorithm_strategy_charter_approval_digest']}.",
        ]),
        ("Operator Attestation", [
            "Decision/reference/timestamp: "
            f"{operator['operator_decision']} / {operator['operator_reference']} / "
            f"{operator['operator_attestation_timestamp_utc']}.",
            f"Exact phrase: {operator['operator_attestation_phrase']}.",
        ]),
        ("Source Charter Review", [
            "Artifact/status/scope: "
            f"{approval['source_charter_review_artifact_kind']} / "
            f"{approval['source_charter_review_status']} / "
            f"{approval['source_charter_review_scope']}.",
            f"Digest: {approval['source_charter_review_digest']}.",
        ]),
        ("Bound Evidence", [
            "Charter/final archive/archive: "
            f"{approval['source_charter_digest']} / "
            f"{approval['source_final_archive_digest']} / "
            f"{approval['source_archive_digest']}.",
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
        ("Approved Algorithm Identity", [approval["marketflow_algorithm_definition"]]),
        ("Approved Strategy Philosophy", [
            approval["core_philosophy"],
            approval["primary_question"],
            approval["secondary_question"],
        ]),
        ("Approved Strategy Principles", [
            f"{name}: {value['approval_status']}."
            for name, value in approval["approved_strategy_principles"].items()
        ]),
        ("Approved Research Questions", [
            f"{value['question']} {value['approval_status']}."
            for value in approval["approved_research_questions"]
        ]),
        ("Approved Objective Families", [
            f"{name}: {value['objective_status']}."
            for name, value in approval["approved_objective_families"].items()
        ]),
        ("Approved Signal Families", [
            f"{name}: {value['signal_status']}."
            for name, value in approval["approved_signal_families"].items()
        ]),
        ("Approved Validation Metrics", [
            f"{name}: {value['metric_status']}."
            for name, value in approval["approved_validation_metrics"].items()
        ]),
        ("Approved Baselines", [
            f"{name}: {value['baseline_status']}."
            for name, value in approval["approved_baselines"].items()
        ]),
        ("Approved Phase Plan", [
            f"{name}: {value['status']}."
            for name, value in approval["approved_phase_plan"].items()
        ]),
        ("Approved Acceptance Gates", [
            f"{name}: {value['gate_status']}."
            for name, value in approval["approved_acceptance_gates"].items()
        ]),
        ("Non-Goals", [
            f"{value['non_goal']} Active: {value['active']}."
            for value in approval["non_goals"]
        ]),
        ("Per-Ticker Approval Summary", [
            f"{row['ticker']}: {row['strategy_charter_approval_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_strategy_charter_approval_digest']}."
            for row in approval["per_ticker_strategy_charter_approval_entries"]
        ]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted; no acceptance candidate is created."
        ]),
        ("Profitability Boundary", [
            "Profitability remains not accepted and is not recommended by this approval."
        ]),
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
            "This approval authorizes the charter only. It creates no objective candidate, "
            "labels, targets, features, matrix, backtest, model, metric, scoring, "
            "recommendation, acceptance, profitability, runtime, provider, market-data, "
            "paper-trading, or broker authority."
        ]),
    ]
    lines = ["# MarketFlow Algorithm Strategy Charter Approval", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_algorithm_strategy_charter_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_algorithm_strategy_charter_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    validation = validate_marketflow_algorithm_strategy_charter_approval_v1(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_algorithm_strategy_charter_approval_v1.json"
    if path.exists():
        raise MarketFlowAlgorithmStrategyCharterApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_algorithm_strategy_charter_approval_digest": validation[
            "marketflow_algorithm_strategy_charter_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
