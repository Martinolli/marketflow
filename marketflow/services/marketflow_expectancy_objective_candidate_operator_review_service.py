"""Offline operator review of the MarketFlow expectancy objective candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_expectancy_objective_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_expectancy_objective_candidate_operator_review_v1"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST = (
    "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17"
)
EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST
)
EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST = (
    candidate_service.EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST
)
EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST = (
    candidate_service.EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST
)
EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE = (
    candidate_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE
)
RECOMMENDED_OBJECTIVE_PATH = candidate_service.RECOMMENDED_OBJECTIVE_PATH

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "Expectancy Objective Approval v1, if selected.",
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
    "expectancy_objective_approval_if_selected",
    "expectancy_objective_design_execution_if_approved",
    "expectancy_objective_results_review",
    "objective_label_or_target_generation_candidate",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_select_objective",
    "review_does_not_approve_objective",
    "review_does_not_generate_labels",
    "review_does_not_create_targets",
    "review_does_not_generate_features",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_run_backtest",
    "review_does_not_train_models",
    "review_does_not_compute_metrics",
    "review_does_not_score_strategy",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class MarketFlowExpectancyObjectiveCandidateOperatorReviewError(ValueError):
    """Raised when the review violates its review-only authority boundary."""


def _source_candidate(candidate: dict | None) -> dict:
    source = (
        candidate_service.build_marketflow_expectancy_objective_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    validation = candidate_service.validate_marketflow_expectancy_objective_candidate_v1(
        source
    )
    if (
        validation["marketflow_expectancy_objective_candidate_v1_digest"]
        != EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "source expectancy objective candidate digest mismatch"
        )
    return source


def _reviewed_objective_families(
    source: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    reviewed = {}
    for name, value in source["objective_candidate_families"].items():
        reviewed[name] = {
            **deepcopy(value),
            "review_status": "REVIEWED_OBJECTIVE_CANDIDATE_NOT_GENERATED",
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
        }
    return reviewed


def _reviewed_clusters(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    review_statuses = {
        "CLUSTER_EXPECTANCY_AND_PAYOFF": "REVIEWED_RECOMMENDED_PRIMARY_CLUSTER",
        "CLUSTER_ABSTENTION_AND_NO_TRADE": "REVIEWED_RECOMMENDED_SUPPORTING_CLUSTER",
        "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE": "REVIEWED_AVAILABLE_SECONDARY_CLUSTER",
        "CLUSTER_CONTEXTUAL_SELECTION": "REVIEWED_AVAILABLE_CONTEXTUAL_CLUSTER",
    }
    return {
        name: {
            "objective_families": deepcopy(value["objective_families"]),
            "candidate_rationale": value["candidate_rationale"],
            "source_status": value["status"],
            "review_status": review_statuses[name],
            "selection_created": False,
            "approval_created": False,
        }
        for name, value in source["recommended_objective_clusters"].items()
    }


def _reviewed_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question": row["question"],
            "source_question_status": row["question_status"],
            "question_status": "REVIEWED_NOT_ANSWERED",
            "requires_future_research": True,
            "answered_by_this_review": False,
            "research_only": True,
        }
        for row in source["objective_design_research_questions"]
    ]


def _reviewed_dimensions(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "review_status": "REVIEWED_CANDIDATE_DIMENSION_NOT_EXECUTED",
            "dimension_status": value["dimension_status"],
            "generation_authorized": False,
            "metric_computation_authorized": False,
        }
        for name, value in source["candidate_objective_design_dimensions"].items()
    }


def _reviewed_future_outputs(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "review_status": "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED",
            "output_status": value["output_status"],
            "research_only": True,
            "non_actionable": True,
        }
        for name, value in source["candidate_future_outputs"].items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_objective_candidate_review_digest", None)
    return payload


def per_ticker_expectancy_objective_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker review entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_expectancy_objective_candidate_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "strategy_charter_approval_status": row["strategy_charter_approval_status"],
            "expectancy_objective_candidate_status": source["candidate_status"],
            "expectancy_objective_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "strategy_direction": source["candidate_direction"],
            "recommended_objective_path": source["recommended_objective_path"],
            "expectancy_objective_selected": False,
            "expectancy_objective_approved": False,
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
            "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST,
            "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_CANDIDATE_REVIEW"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_expectancy_objective_candidate_review_digest"] = (
            per_ticker_expectancy_objective_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(value)
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _base_review(source: Mapping[str, Any]) -> dict[str, Any]:
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_expectancy_objective_candidate_artifact_kind": source["artifact_kind"],
        "source_expectancy_objective_candidate_status": source["candidate_status"],
        "source_expectancy_objective_candidate_scope": source["candidate_scope"],
        "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST,
        "source_strategy_charter_approval_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST,
        "source_strategy_charter_review_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST,
        "source_strategy_charter_digest": EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST,
        **_source_digest_chain(source),
    }
    review.update(
        {
            "expectancy_objective_candidate_created": True,
            "expectancy_objective_candidate_ready_for_operator_review": True,
            "expectancy_objective_candidate_review_created": True,
            "expectancy_objective_candidate_review_ready": True,
            "ready_for_expectancy_objective_approval": False,
            "expectancy_objective_selected": False,
            "expectancy_objective_approved": False,
            "expectancy_objective_generation_authorized": False,
            "expectancy_objective_generation_performed": False,
            "selection_created": False,
            "approval_created": False,
            "generation_created": False,
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
            "provider_requests_made_in_review": False,
            "live_provider_transport_enabled_in_review": False,
            "market_data_acquisition_performed_in_review": False,
            "dataset_generation_performed_in_review": False,
            "canonical_dataset_regenerated_in_review": False,
            "raw_provider_payloads_committed": False,
            "api_keys_stored_or_printed": False,
        }
    )
    copied_fields = [
        "dataset_name", "source_profile", "timeframe", "date_range_start", "date_range_end",
        "target_universe", "target_universe_count", "total_canonical_record_count",
        "per_ticker_record_counts", "meta_record_count", "non_meta_record_count",
        "meta_reduced_record_count_preserved", "strategy_direction",
        "marketflow_algorithm_identity", "core_philosophy", "previous_chain_status",
        "previous_predictive_usefulness_decision", "previous_acceptance_readiness_decision",
        "previous_runtime_decision", "previous_profitability_decision",
        "previous_operator_selected_option", "matrix_row_count", "evaluable_matrix_row_count",
        "unavailable_target_count", "oos_row_count", "majority_accuracy",
        "local_model_accuracy", "cross_sectional_accuracy",
        "cross_sectional_delta_vs_majority", "majority_brier", "local_model_brier",
        "cross_sectional_brier", "optional_tree_model_status",
        "optional_ensemble_model_status", "leakage_control_passed",
        "leakage_failed_control_count", "leakage_control_count", "majority_structure_risk",
        "largest_aggregated_class", "largest_aggregated_class_count", "no_trade_count",
        "objective_candidate_philosophy", "objective_candidate_primary_question",
        "objective_candidate_secondary_question", "objective_candidate_boundary",
    ]
    review.update({field: deepcopy(source[field]) for field in copied_fields})
    review.update(
        {
            "candidate_direction": source["candidate_direction"],
            "reviewed_objective_philosophy": {
                "objective_candidate_philosophy": source["objective_candidate_philosophy"],
                "objective_candidate_primary_question": source["objective_candidate_primary_question"],
                "objective_candidate_secondary_question": source["objective_candidate_secondary_question"],
                "objective_candidate_boundary": source["objective_candidate_boundary"],
                "review_status": "REVIEWED_CANDIDATE_PHILOSOPHY",
                "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
            },
            "reviewed_objective_families": _reviewed_objective_families(source),
            "reviewed_objective_clusters": _reviewed_clusters(source),
            "recommended_objective_path": source["recommended_objective_path"],
            "recommendation_status": "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            "recommended_primary_objective_cluster": source["recommended_primary_objective_cluster"],
            "recommended_supporting_objective_cluster": source["recommended_supporting_objective_cluster"],
            "recommended_secondary_cluster": source["recommended_secondary_cluster"],
            "reviewed_research_questions": _reviewed_questions(source),
            "reviewed_design_dimensions": _reviewed_dimensions(source),
            "reviewed_future_outputs": _reviewed_future_outputs(source),
            "per_ticker_expectancy_objective_candidate_review_entries": _per_ticker_entries(source),
            "next_chain": list(NEXT_CHAIN),
            "next_gates": list(NEXT_GATES),
            "risk_controls": list(RISK_CONTROLS),
            "no_tracked_marketflow_files": True,
        }
    )
    return review


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
        and isinstance(entry.get("per_ticker_expectancy_objective_candidate_review_digest"), str)
        and entry["per_ticker_expectancy_objective_candidate_review_digest"]
        == per_ticker_expectancy_objective_candidate_review_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(review: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = candidate_service.build_marketflow_expectancy_objective_candidate_v1()
    expected = _base_review(source)
    entries = review.get("per_ticker_expectancy_objective_candidate_review_entries", [])
    return [
        ("source_expectancy_objective_candidate_digest_bound", EXPECTED_SOURCE_EXPECTANCY_OBJECTIVE_CANDIDATE_DIGEST, review.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_APPROVAL_DIGEST, review.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_review_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_REVIEW_DIGEST, review.get("source_strategy_charter_review_digest")),
        ("source_strategy_charter_digest_bound", EXPECTED_SOURCE_STRATEGY_CHARTER_DIGEST, review.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", source["source_final_archive_digest"], review.get("source_final_archive_digest")),
        ("source_archive_digest_bound", source["source_archive_digest"], review.get("source_archive_digest")),
        ("source_selection_digest_bound", source["source_selection_digest"], review.get("source_selection_digest")),
        ("source_closure_digest_bound", source["source_closure_digest"], review.get("source_closure_digest")),
        ("source_readiness_digest_bound", source["source_readiness_digest"], review.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", source["source_reassessment_digest"], review.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", source["source_results_review_digest"], review.get("source_results_review_digest")),
        ("source_execution_digest_bound", source["source_execution_digest"], review.get("source_execution_digest")),
        ("matrix_digest_bound", source["feature_label_matrix_digest"], review.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", source["feature_values_digest"], review.get("feature_values_digest")),
        ("label_values_digest_bound", source["redesigned_label_values_digest"], review.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", source["research_registry_approval_digest"], review.get("research_registry_approval_digest")),
        ("records_digest_bound", source["records_digest"], review.get("records_digest")),
        ("target_universe_12_preserved", source["target_universe"], review.get("target_universe")),
        ("records_digest_preserved", source["records_digest"], review.get("records_digest")),
        ("meta_913_preserved", 913, review.get("meta_record_count")),
        ("candidate_status_ready", source["candidate_status"], review.get("source_expectancy_objective_candidate_status")),
        ("candidate_scope_preserved", source["candidate_scope"], review.get("source_expectancy_objective_candidate_scope")),
        ("candidate_direction_expectancy_first", EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE, review.get("candidate_direction")),
        ("review_created_true", True, review.get("expectancy_objective_candidate_review_created")),
        ("review_ready_true", True, review.get("expectancy_objective_candidate_review_ready")),
        ("ready_for_approval_false", False, review.get("ready_for_expectancy_objective_approval")),
        ("expectancy_objective_selected_false", False, review.get("expectancy_objective_selected")),
        ("expectancy_objective_approved_false", False, review.get("expectancy_objective_approved")),
        ("objective_philosophy_reviewed", expected["reviewed_objective_philosophy"], review.get("reviewed_objective_philosophy")),
        ("objective_families_reviewed_10", expected["reviewed_objective_families"], review.get("reviewed_objective_families")),
        ("objective_clusters_reviewed", expected["reviewed_objective_clusters"], review.get("reviewed_objective_clusters")),
        ("recommended_objective_path_reviewed", RECOMMENDED_OBJECTIVE_PATH, review.get("recommended_objective_path")),
        ("selection_created_false", False, review.get("selection_created")),
        ("approval_created_false", False, review.get("approval_created")),
        ("generation_created_false", False, review.get("generation_created")),
        ("research_questions_reviewed", expected["reviewed_research_questions"], review.get("reviewed_research_questions")),
        ("design_dimensions_reviewed", expected["reviewed_design_dimensions"], review.get("reviewed_design_dimensions")),
        ("future_outputs_reviewed_not_generated", expected["reviewed_future_outputs"], review.get("reviewed_future_outputs")),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("label_generation_authorized_false", False, review.get("label_generation_authorized")),
        ("new_targets_created_false", False, review.get("new_targets_created")),
        ("feature_generation_authorized_false", False, review.get("feature_generation_authorized")),
        ("feature_label_matrix_created_false", False, review.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, review.get("backtest_execution_authorized")),
        ("model_training_authorized_false", False, review.get("model_training_authorized")),
        ("metric_computation_authorized_false", False, review.get("metric_computation_authorized")),
        ("strategy_scoring_false", False, review.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, review.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        ("trade_recommendations_false", False, review.get("trade_recommendations_generated")),
        ("provider_requests_made_false", False, review.get("provider_requests_made_in_review")),
        ("market_data_acquisition_false", False, review.get("market_data_acquisition_performed_in_review")),
        ("dataset_regeneration_false", False, review.get("canonical_dataset_regenerated_in_review")),
        ("raw_provider_payloads_not_committed", False, review.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, review.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        ("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
    ]


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(review)]


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
        "expectancy_objective_candidate_review_created": True,
        "expectancy_objective_candidate_review_ready": True,
        "ready_for_expectancy_objective_approval": False,
        "recommended_objective_path": RECOMMENDED_OBJECTIVE_PATH,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "label_generation_authorized": False,
        "new_targets_created": False,
        "feature_generation_authorized": False,
        "backtest_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop("marketflow_expectancy_objective_candidate_operator_review_digest", None)
    return payload


def marketflow_expectancy_objective_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review))


def build_marketflow_expectancy_objective_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Build a review-only package without selection, approval, or execution."""
    review = _base_review(_source_candidate(candidate))
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review["marketflow_expectancy_objective_candidate_operator_review_digest"] = (
        marketflow_expectancy_objective_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_expectancy_objective_candidate_operator_review_v1(review)
    return review


def validate_marketflow_expectancy_objective_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact source bindings, reviewed content, and closed authorities."""
    if not isinstance(review, dict):
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review must be an object"
        )
    expected = _base_review(_source_candidate(None))
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
                f"{field} mismatch"
            )
    checklist = review.get("review_checklist")
    expected_checklist = _checklist(review)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review checklist mismatch"
        )
    if review.get("review_summary") != _summary(expected_checklist):
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review summary mismatch"
        )
    digest = review.get(
        "marketflow_expectancy_objective_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review digest missing"
        )
    if digest != marketflow_expectancy_objective_candidate_operator_review_digest_v1(
        review
    ):
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review digest mismatch"
        )
    return {
        "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_CANDIDATE_OPERATOR_REVIEW_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_expectancy_objective_candidate_operator_review_digest": digest,
        **{
            key: review["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_expectancy_objective_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = (
        validate_marketflow_expectancy_objective_candidate_operator_review_v1(review)
    )
    sections = [
        ("Title", ["Expectancy Objective Candidate Operator Review v1"]),
        ("Expectancy Objective Candidate Operator Review v1", [
            "Artifact/status/scope: "
            f"{review['artifact_kind']} / {review['review_status']} / "
            f"{review['review_scope']}.",
            "Review digest: "
            f"{validation['marketflow_expectancy_objective_candidate_operator_review_digest']}.",
        ]),
        ("Source Expectancy Objective Candidate", [
            "Artifact/status/scope: "
            f"{review['source_expectancy_objective_candidate_artifact_kind']} / "
            f"{review['source_expectancy_objective_candidate_status']} / "
            f"{review['source_expectancy_objective_candidate_scope']}.",
            f"Digest: {review['source_expectancy_objective_candidate_digest']}.",
        ]),
        ("Bound Evidence", [
            "Approval/review/charter: "
            f"{review['source_strategy_charter_approval_digest']} / "
            f"{review['source_strategy_charter_review_digest']} / "
            f"{review['source_strategy_charter_digest']}.",
            "Matrix/features/labels: "
            f"{review['feature_label_matrix_digest']} / "
            f"{review['feature_values_digest']} / "
            f"{review['redesigned_label_values_digest']}.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: {review['dataset_name']} / "
            f"{review['total_canonical_record_count']}.",
            "Universe: " + ", ".join(review["target_universe"]) + ".",
            "META remains 913; every non-META ticker remains 1003.",
        ]),
        ("Reviewed Candidate Basis", [
            f"Direction: {review['strategy_direction']}.",
            f"Previous chain: {review['previous_chain_status']}.",
            f"Core philosophy: {review['core_philosophy']}",
        ]),
        ("Reviewed Objective Philosophy", [
            review["objective_candidate_philosophy"],
            review["objective_candidate_primary_question"],
            review["objective_candidate_secondary_question"],
            review["objective_candidate_boundary"],
        ]),
        ("Reviewed Objective Families", [
            f"{name}: {value['review_status']}."
            for name, value in review["reviewed_objective_families"].items()
        ]),
        ("Reviewed Objective Clusters", [
            f"{name}: {value['review_status']} from {value['source_status']}."
            for name, value in review["reviewed_objective_clusters"].items()
        ]),
        ("Reviewed Candidate Recommendation", [
            f"Path: {review['recommended_objective_path']}.",
            f"Status: {review['recommendation_status']}.",
            "No selection, approval, or generation is created.",
        ]),
        ("Reviewed Research Questions", [
            f"{value['question']} Status: {value['question_status']}."
            for value in review["reviewed_research_questions"]
        ]),
        ("Reviewed Design Dimensions", [
            f"{name}: {value['review_status']}."
            for name, value in review["reviewed_design_dimensions"].items()
        ]),
        ("Reviewed Future Outputs", [
            f"{name}: {value['review_status']}."
            for name, value in review["reviewed_future_outputs"].items()
        ]),
        ("Per-Ticker Review Summary", [
            f"{row['ticker']}: {row['expectancy_objective_candidate_review_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_expectancy_objective_candidate_review_digest']}."
            for row in review["per_ticker_expectancy_objective_candidate_review_entries"]
        ]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted."
        ]),
        ("Profitability Boundary", [
            "Profitability remains not accepted."
        ]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            "Total/passed/failed/blockers: "
            f"{review['review_summary']['total_checks']} / "
            f"{review['review_summary']['passed_checks']} / "
            f"{review['review_summary']['failed_checks']} / "
            f"{review['review_summary']['blocker_count']}."
        ]),
        ("Guardrails", [
            "This review creates no selection, approval, labels, targets, features, "
            "matrix, backtest, model, metric, scoring, recommendation, acceptance, "
            "profitability, runtime, provider, market-data, paper-trading, or broker authority."
        ]),
    ]
    lines = ["# Expectancy Objective Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_expectancy_objective_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_expectancy_objective_candidate_operator_review_v1(
        candidate
    )
    validation = validate_marketflow_expectancy_objective_candidate_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_expectancy_objective_candidate_operator_review_v1.json"
    if path.exists():
        raise MarketFlowExpectancyObjectiveCandidateOperatorReviewError(
            "review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_expectancy_objective_candidate_operator_review_digest": validation[
            "marketflow_expectancy_objective_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
