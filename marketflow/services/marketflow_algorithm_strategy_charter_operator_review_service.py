"""Offline operator review of the MarketFlow algorithm strategy charter."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_algorithm_strategy_charter_service as charter_service


ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_V1 = (
    "marketflow_algorithm_strategy_charter_operator_review_v1"
)
MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE_READY"
)
STRATEGY_CHARTER_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "STRATEGY_CHARTER_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
EXPECTED_SOURCE_CHARTER_DIGEST = (
    "3f5e3fd4088c38c5783618642c378874d2c0fbcc72954945cdca9fca68281853"
)
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "MarketFlow Algorithm Strategy Charter Approval v1, if selected.",
    "Expectancy Objective Candidate v1, only after charter approval.",
    "Expectancy Objective Candidate Operator Review v1.",
    "Expectancy Objective Approval v1.",
    "Future objective/label execution only after separate approval.",
    "Future feature/backtest work only after separate gates.",
    "Predictive usefulness remains not accepted until a new evidence chain passes readiness.",
    "Profitability and runtime remain separately gated.",
]
NEXT_GATES = [
    "marketflow_algorithm_strategy_charter_approval_if_selected",
    "expectancy_objective_candidate_if_approved",
    "expectancy_objective_operator_review",
    "expectancy_objective_generation_approval",
    "feature_generation_approval",
    "expectancy_backtest_lab_approval",
    "results_review_and_reassessment",
    "paper_research_readiness_review",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_approve_strategy_charter",
    "review_does_not_create_expectancy_objective_candidate",
    "review_does_not_create_labels",
    "review_does_not_create_targets",
    "review_does_not_generate_features",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_run_backtest",
    "review_does_not_train_models",
    "review_does_not_recompute_metrics",
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


class MarketFlowAlgorithmStrategyCharterOperatorReviewError(ValueError):
    """Raised when a review violates its review-only authority boundary."""


def _reviewed_catalog(
    values: Mapping[str, Mapping[str, Any]],
    *,
    review_status: str,
    status_key: str,
    authorization_fields: tuple[str, ...] = (),
) -> dict[str, dict[str, Any]]:
    reviewed = {}
    for name, value in values.items():
        row = {
            "review_status": review_status,
            status_key: value["status"],
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
            "research_only": True,
            "non_actionable": True,
        }
        row.update({field: False for field in authorization_fields})
        reviewed[name] = row
    return reviewed


def _reviewed_principles(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "review_status": "REVIEWED_RESEARCH_ONLY",
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for name in source["strategy_principles"]
    }


def _reviewed_questions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question": question,
            "review_status": "REVIEWED_RESEARCH_ONLY",
            "answered_by_this_review": False,
            "requires_future_research": True,
        }
        for question in source["research_questions"]
    ]


def _reviewed_objectives(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _reviewed_catalog(
        source["candidate_objective_families"],
        review_status="REVIEWED_CANDIDATE_OBJECTIVE",
        status_key="objective_status",
        authorization_fields=("label_generation_authorized", "target_creation_authorized"),
    )


def _reviewed_signals(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _reviewed_catalog(
        source["candidate_signal_families"],
        review_status="REVIEWED_CANDIDATE_SIGNAL",
        status_key="signal_status",
        authorization_fields=("feature_generation_authorized",),
    )


def _reviewed_metrics(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _reviewed_catalog(
        source["candidate_validation_metrics"],
        review_status="REVIEWED_CANDIDATE_METRIC",
        status_key="metric_status",
        authorization_fields=("metric_computation_authorized",),
    )


def _reviewed_baselines(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return _reviewed_catalog(
        source["candidate_baselines"],
        review_status="REVIEWED_CANDIDATE_BASELINE",
        status_key="baseline_status",
        authorization_fields=("model_training_authorized", "backtest_authorized"),
    )


def _reviewed_phase_plan(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "review_status": "REVIEWED_RESEARCH_ONLY",
            "status": "COMPLETED_BY_SOURCE_ARTIFACT" if index == 0 else "FUTURE_NOT_STARTED",
            "source_status": value["status"],
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
        }
        for index, (name, value) in enumerate(source["proposed_phase_plan"].items())
    }


def _reviewed_gates(source: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "review_status": "REVIEWED_CLOSED_FUTURE_GATE",
            "gate_status": value["status"],
            "approval_created": False,
            "execution_created": False,
            "opened_by_this_review": False,
        }
        for name, value in source["proposed_acceptance_gates"].items()
    }


def _reviewed_non_goals(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"non_goal": value, "review_status": "REVIEWED_ACTIVE", "active": True}
        for value in source["non_goals"]
    ]


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_strategy_charter_review_digest", None)
    return payload


def per_ticker_marketflow_algorithm_strategy_charter_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker review entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for ticker in source["target_universe"]:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source["per_ticker_record_counts"][ticker],
            "meta_reduced_record_count_flag": is_meta,
            "source_charter_status": source["charter_status"],
            "strategy_charter_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "strategy_direction": source["strategy_direction"],
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_charter_digest": EXPECTED_SOURCE_CHARTER_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_ALGORITHM_STRATEGY_CHARTER_REVIEW"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_strategy_charter_review_digest"] = (
            per_ticker_marketflow_algorithm_strategy_charter_review_digest_v1(entry)
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
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": STRATEGY_CHARTER_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_charter_artifact_kind": source["artifact_kind"],
        "source_charter_status": source["charter_status"],
        "source_charter_digest": EXPECTED_SOURCE_CHARTER_DIGEST,
        "source_strategy_direction": source["strategy_direction"],
        **_source_digest_chain(source),
    }
    review.update(
        {
            "marketflow_algorithm_strategy_charter_created": True,
            "marketflow_algorithm_strategy_charter_ready_for_operator_review": True,
            "marketflow_algorithm_strategy_charter_review_created": True,
            "marketflow_algorithm_strategy_charter_review_ready": True,
            "ready_for_marketflow_algorithm_strategy_charter_approval": False,
            "marketflow_algorithm_strategy_charter_approved": False,
            "marketflow_algorithm_strategy_charter_authorized": False,
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
    review.update({field: deepcopy(source[field]) for field in copied_fields})
    review.update(
        {
            "reviewed_strategy_philosophy": {
                **deepcopy(source["strategy_philosophy"]),
                "review_status": "REVIEWED_RESEARCH_ONLY",
                "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
                "answered_by_this_review": False,
            },
            "reviewed_strategy_principles": _reviewed_principles(source),
            "reviewed_research_questions": _reviewed_questions(source),
            "reviewed_objective_families": _reviewed_objectives(source),
            "reviewed_signal_families": _reviewed_signals(source),
            "reviewed_validation_metrics": _reviewed_metrics(source),
            "reviewed_baselines": _reviewed_baselines(source),
            "reviewed_phase_plan": _reviewed_phase_plan(source),
            "reviewed_acceptance_gates": _reviewed_gates(source),
            "reviewed_non_goals": _reviewed_non_goals(source),
            "per_ticker_strategy_charter_review_entries": _per_ticker_entries(source),
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
        and isinstance(entry.get("per_ticker_strategy_charter_review_digest"), str)
        and entry["per_ticker_strategy_charter_review_digest"]
        == per_ticker_marketflow_algorithm_strategy_charter_review_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(review: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = charter_service.build_marketflow_algorithm_strategy_charter_v1()
    expected = _base_review(source)
    entries = review.get("per_ticker_strategy_charter_review_entries", [])
    return [
        ("source_charter_digest_bound", EXPECTED_SOURCE_CHARTER_DIGEST, review.get("source_charter_digest")),
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
        ("source_charter_status_ready", source["charter_status"], review.get("source_charter_status")),
        ("strategy_direction_expectancy_first", charter_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE, review.get("strategy_direction")),
        ("review_created_true", True, review.get("marketflow_algorithm_strategy_charter_review_created")),
        ("review_ready_true", True, review.get("marketflow_algorithm_strategy_charter_review_ready")),
        ("approval_false", False, review.get("marketflow_algorithm_strategy_charter_approved")),
        ("ready_for_approval_false", False, review.get("ready_for_marketflow_algorithm_strategy_charter_approval")),
        ("expectancy_objective_candidate_created_false", False, review.get("expectancy_objective_candidate_created")),
        ("strategy_philosophy_reviewed", expected["reviewed_strategy_philosophy"], review.get("reviewed_strategy_philosophy")),
        ("strategy_principles_reviewed", expected["reviewed_strategy_principles"], review.get("reviewed_strategy_principles")),
        ("research_questions_reviewed", expected["reviewed_research_questions"], review.get("reviewed_research_questions")),
        ("objective_families_reviewed", expected["reviewed_objective_families"], review.get("reviewed_objective_families")),
        ("signal_families_reviewed", expected["reviewed_signal_families"], review.get("reviewed_signal_families")),
        ("validation_metrics_reviewed", expected["reviewed_validation_metrics"], review.get("reviewed_validation_metrics")),
        ("baselines_reviewed", expected["reviewed_baselines"], review.get("reviewed_baselines")),
        ("phase_plan_reviewed", expected["reviewed_phase_plan"], review.get("reviewed_phase_plan")),
        ("acceptance_gates_reviewed_closed", expected["reviewed_acceptance_gates"], review.get("reviewed_acceptance_gates")),
        ("non_goals_reviewed_active", expected["reviewed_non_goals"], review.get("reviewed_non_goals")),
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
        "strategy_charter_review_created": True,
        "strategy_charter_review_ready": True,
        "ready_for_approval": False,
        "strategy_direction": charter_service.EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE,
        "expectancy_objective_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop("marketflow_algorithm_strategy_charter_operator_review_digest", None)
    return payload


def marketflow_algorithm_strategy_charter_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review))


def build_marketflow_algorithm_strategy_charter_operator_review_v1(
    charter: dict | None = None,
) -> dict:
    """Build a review-only package without providers, generation, or execution."""
    source = (
        charter_service.build_marketflow_algorithm_strategy_charter_v1()
        if charter is None
        else deepcopy(charter)
    )
    charter_service.validate_marketflow_algorithm_strategy_charter_v1(source)
    if source["marketflow_algorithm_strategy_charter_v1_digest"] != EXPECTED_SOURCE_CHARTER_DIGEST:
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "source charter digest mismatch"
        )
    review = _base_review(source)
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review["marketflow_algorithm_strategy_charter_operator_review_digest"] = (
        marketflow_algorithm_strategy_charter_operator_review_digest_v1(review)
    )
    validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)
    return review


def validate_marketflow_algorithm_strategy_charter_operator_review_v1(
    review: dict,
) -> dict:
    """Validate source bindings, reviewed catalogs, and closed authorities."""
    if not isinstance(review, dict):
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review must be an object"
        )
    source = charter_service.build_marketflow_algorithm_strategy_charter_v1()
    expected = _base_review(source)
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
                f"{field} mismatch"
            )
    checklist = review.get("review_checklist")
    expected_checklist = _checklist(review)
    if checklist != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review checklist mismatch"
        )
    if review.get("review_summary") != _summary(expected_checklist):
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review summary mismatch"
        )
    digest = review.get("marketflow_algorithm_strategy_charter_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review digest missing"
        )
    if digest != marketflow_algorithm_strategy_charter_operator_review_digest_v1(review):
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review digest mismatch"
        )
    return {
        "status": "MARKETFLOW_ALGORITHM_STRATEGY_CHARTER_OPERATOR_REVIEW_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "strategy_direction": review["strategy_direction"],
        "marketflow_algorithm_strategy_charter_operator_review_digest": digest,
        **{
            key: review["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_algorithm_strategy_charter_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)
    sections = [
        ("Title", ["MarketFlow Algorithm Strategy Charter Operator Review"]),
        ("MarketFlow Algorithm Strategy Charter Operator Review", [
            "Artifact/status/scope: "
            f"{review['artifact_kind']} / {review['review_status']} / {review['review_scope']}.",
            "Review digest: "
            f"{validation['marketflow_algorithm_strategy_charter_operator_review_digest']}.",
        ]),
        ("Source Strategy Charter", [
            f"Artifact/status: {review['source_charter_artifact_kind']} / {review['source_charter_status']}.",
            f"Digest: {review['source_charter_digest']}.",
        ]),
        ("Bound Evidence", [
            "Final archive/archive/selection: "
            f"{review['source_final_archive_digest']} / {review['source_archive_digest']} / "
            f"{review['source_selection_digest']}.",
            "Matrix/features/labels: "
            f"{review['feature_label_matrix_digest']} / {review['feature_values_digest']} / "
            f"{review['redesigned_label_values_digest']}.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: {review['dataset_name']} / {review['total_canonical_record_count']}.",
            "Universe: " + ", ".join(review["target_universe"]) + ".",
            "META remains 913; every non-META ticker remains 1003.",
        ]),
        ("Reviewed Algorithm Identity", [review["marketflow_algorithm_definition"]]),
        ("Reviewed Strategy Philosophy", [
            review["core_philosophy"], review["primary_question"], review["secondary_question"]
        ]),
        ("Reviewed Strategy Principles", [
            f"{name}: {value['review_status']}."
            for name, value in review["reviewed_strategy_principles"].items()
        ]),
        ("Reviewed Research Questions", [
            f"{value['question']} {value['review_status']}."
            for value in review["reviewed_research_questions"]
        ]),
        ("Reviewed Objective Families", [
            f"{name}: {value['objective_status']}."
            for name, value in review["reviewed_objective_families"].items()
        ]),
        ("Reviewed Signal Families", [
            f"{name}: {value['signal_status']}."
            for name, value in review["reviewed_signal_families"].items()
        ]),
        ("Reviewed Validation Metrics", [
            f"{name}: {value['metric_status']}."
            for name, value in review["reviewed_validation_metrics"].items()
        ]),
        ("Reviewed Baselines", [
            f"{name}: {value['baseline_status']}."
            for name, value in review["reviewed_baselines"].items()
        ]),
        ("Reviewed Phase Plan", [
            f"{name}: {value['status']}."
            for name, value in review["reviewed_phase_plan"].items()
        ]),
        ("Reviewed Acceptance Gates", [
            f"{name}: {value['gate_status']}."
            for name, value in review["reviewed_acceptance_gates"].items()
        ]),
        ("Reviewed Non-Goals", [
            f"{value['non_goal']} Active: {value['active']}."
            for value in review["reviewed_non_goals"]
        ]),
        ("Per-Ticker Review Summary", [
            f"{row['ticker']}: {row['strategy_charter_review_status']}, "
            f"records {row['historical_record_count']}, "
            f"digest {row['per_ticker_strategy_charter_review_digest']}."
            for row in review["per_ticker_strategy_charter_review_entries"]
        ]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted; this review creates no acceptance candidate."
        ]),
        ("Profitability Boundary", [
            "Profitability remains not accepted and is not recommended by this review."
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
            "This review creates no approval, objective, labels, targets, features, matrix, "
            "backtest, model, metric, scoring, recommendation, acceptance, profitability, "
            "runtime, provider, market-data, paper-trading, or broker authority."
        ]),
    ]
    lines = ["# MarketFlow Algorithm Strategy Charter Operator Review", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_algorithm_strategy_charter_operator_review_v1(
    output_dir: str | Path,
    *,
    charter: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review = build_marketflow_algorithm_strategy_charter_operator_review_v1(charter)
    validation = validate_marketflow_algorithm_strategy_charter_operator_review_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_algorithm_strategy_charter_operator_review_v1.json"
    if path.exists():
        raise MarketFlowAlgorithmStrategyCharterOperatorReviewError(
            "review output already exists"
        )
    payload = canonical_json_bytes(review)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_algorithm_strategy_charter_operator_review_digest": validation[
            "marketflow_algorithm_strategy_charter_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
