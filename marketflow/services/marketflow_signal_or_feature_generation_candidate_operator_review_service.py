"""Offline operator review of the signal or feature generation candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    marketflow_signal_or_feature_generation_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_signal_or_feature_generation_candidate_operator_review_v1"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "e9369666fdc7efc35321d6c3c028071b012e139b84c8633177946ab842201f59"
)
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
SOURCE_EVIDENCE_DIGESTS = dict(candidate_service.SOURCE_EVIDENCE_DIGESTS)
SELECTED_LABEL_TARGET_PACKAGE = (
    candidate_service.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET
)
SELECTED_OBJECTIVE_PATH = candidate_service.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT
RECOMMENDED_PACKAGE_ID = candidate_service.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
SUPPORTING_PACKAGE_ID = candidate_service.PACKAGE_REGIME_CONTEXT_SIGNAL_SET
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

NEXT_CHAIN = [
    "Signal or Feature Generation Approval v1, if selected.",
    "Signal or Feature Generation Execution v1, if approved.",
    "Signal or Feature Generation Results Review v1.",
    "Future feature-label matrix candidate only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "signal_or_feature_generation_approval_if_selected",
    "signal_or_feature_generation_execution_if_approved",
    "signal_or_feature_generation_results_review",
    "feature_label_matrix_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_select_feature_package",
    "review_does_not_approve_feature_generation",
    "review_does_not_generate_signal_values",
    "review_does_not_generate_feature_values",
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
    "review_does_not_rerun_target_generation_execution",
    "review_does_not_rerun_target_results_review",
    "review_does_not_rerun_candidate_creation",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_signal_or_feature_candidate_digest_bound",
    "source_target_results_review_digest_bound",
    "source_target_generation_execution_digest_bound",
    "source_target_values_digest_bound",
    "source_target_approval_digest_bound",
    "source_target_candidate_review_digest_bound",
    "source_target_candidate_digest_bound",
    "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound",
    "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_prior_execution_digest_bound",
    "matrix_digest_bound",
    "feature_values_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "source_candidate_status_ready",
    "source_candidate_scope_preserved",
    "review_created_true",
    "review_ready_true",
    "ready_for_approval_false",
    "candidate_philosophy_reviewed",
    "signal_families_reviewed_10",
    "feature_families_reviewed_10",
    "recommended_package_reviewed_not_selected",
    "supporting_package_reviewed_not_selected",
    "feature_groups_reviewed_17",
    "no_peek_rules_reviewed_10",
    "quality_checks_reviewed_10",
    "future_outputs_reviewed_not_generated",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "selection_created_false",
    "approval_created_false",
    "generation_created_false",
    "signal_or_feature_generation_selected_false",
    "signal_or_feature_generation_approved_false",
    "signal_or_feature_generation_authorized_false",
    "signal_or_feature_generation_performed_false",
    "signal_generation_authorized_false",
    "signal_generation_performed_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
    "feature_values_created_false",
    "feature_label_matrix_created_false",
    "backtest_execution_authorized_false",
    "backtest_execution_performed_false",
    "model_training_authorized_false",
    "model_training_performed_false",
    "metric_computation_authorized_false",
    "metric_computation_performed_false",
    "strategy_scoring_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "target_generation_execution_rerun_false",
    "target_results_review_rerun_false",
    "candidate_creation_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(ValueError):
    """Raised when the operator review violates its review-only boundary."""


def _source_candidate(candidate: dict | None) -> dict:
    source = (
        candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        validation = candidate_service.validate_marketflow_signal_or_feature_generation_candidate_v1(
            source
        )
    except candidate_service.MarketFlowSignalOrFeatureGenerationCandidateError as exc:
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "source signal or feature generation candidate invalid"
        ) from exc
    if (
        validation["marketflow_signal_or_feature_generation_candidate_v1_digest"]
        != EXPECTED_SOURCE_CANDIDATE_DIGEST
    ):
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "source signal or feature generation candidate digest mismatch"
        )
    return source


def _reviewed_candidate_basis(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "selected_label_target_package": source["selected_label_target_package"],
        "selected_objective_path": source["selected_objective_path"],
        "target_profile_count": source["target_profile_count"],
        "target_row_count": source["target_row_count"],
        "available_target_row_count": source["available_target_row_count"],
        "unavailable_target_row_count": source["unavailable_target_row_count"],
        "source_target_values_digest": source["source_target_values_digest"],
        "review_status": "REVIEWED_CANDIDATE_BASIS",
        "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
    }


def _reviewed_candidate_philosophy(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "candidate_philosophy": source["candidate_philosophy"],
        "candidate_primary_question": source["candidate_primary_question"],
        "candidate_secondary_question": source["candidate_secondary_question"],
        "candidate_boundary": source["candidate_boundary"],
        "review_status": "REVIEWED_CANDIDATE_PHILOSOPHY",
        "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
    }


def _reviewed_signal_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_SIGNAL_CANDIDATE_NOT_GENERATED",
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
        }
        for row in source["proposed_signal_families"]
    ]


def _reviewed_feature_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_FEATURE_CANDIDATE_NOT_GENERATED",
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
        }
        for row in source["proposed_feature_families"]
    ]


def _reviewed_package(
    source_package: Mapping[str, Any], *, review_status: str
) -> dict[str, Any]:
    return {
        "package_id": source_package["package_id"],
        "source_status": source_package["status"],
        "review_status": review_status,
        "includes_signal_families": deepcopy(
            source_package["includes_signal_families"]
        ),
        "includes_feature_families": deepcopy(
            source_package["includes_feature_families"]
        ),
        "rationale": source_package["rationale"],
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _reviewed_feature_groups(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_FEATURE_GROUP_CANDIDATE_NOT_GENERATED",
        }
        for row in source["proposed_feature_groups"]
    ]


def _reviewed_no_peek_rules(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_PLANNED_RULE_NOT_EXECUTED",
        }
        for row in source["no_peek_and_target_separation_rules"]
    ]


def _reviewed_quality_checks(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_PLANNED_CHECK_NOT_EXECUTED",
        }
        for row in source["planned_quality_checks"]
    ]


def _reviewed_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED",
        }
        for row in source["future_outputs"]
    ]


def per_ticker_signal_or_feature_generation_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    payload = deepcopy(dict(entry))
    payload.pop(
        "per_ticker_signal_or_feature_generation_candidate_review_digest", None
    )
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_candidate_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "target_generation_results_review_status": row[
                "target_generation_results_review_status"
            ],
            "signal_or_feature_generation_candidate_status": source[
                "candidate_status"
            ],
            "signal_or_feature_generation_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "selected_label_target_package": source[
                "selected_label_target_package"
            ],
            "selected_objective_path": source["selected_objective_path"],
            "recommended_feature_package": RECOMMENDED_PACKAGE_ID,
            "target_profile_count": row["target_profile_count"],
            "target_row_count": row["target_row_count"],
            "available_target_row_count": row["available_target_row_count"],
            "unavailable_target_row_count": row["unavailable_target_row_count"],
            "signal_or_feature_generation_selected": False,
            "signal_or_feature_generation_approved": False,
            "signal_or_feature_generation_authorized": False,
            "signal_or_feature_generation_performed": False,
            "signal_generation_authorized": False,
            "signal_generation_performed": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
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
            "source_signal_or_feature_generation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_target_results_review_digest": candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
            "source_target_values_digest": candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_REVIEW"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_signal_or_feature_generation_candidate_review_digest"
        ] = per_ticker_signal_or_feature_generation_candidate_review_digest_v1(
            entry
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
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_signal_or_feature_generation_candidate_artifact_kind": source[
            "artifact_kind"
        ],
        "source_signal_or_feature_generation_candidate_status": source[
            "candidate_status"
        ],
        "source_signal_or_feature_generation_candidate_scope": source[
            "candidate_scope"
        ],
        "source_signal_or_feature_generation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_target_results_review_digest": candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_target_generation_execution_digest": candidate_service.EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_target_values_digest": candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        **_source_digest_chain(source),
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "signal_or_feature_generation_candidate_created": True,
        "signal_or_feature_generation_candidate_ready_for_operator_review": True,
        "signal_or_feature_generation_candidate_review_created": True,
        "signal_or_feature_generation_candidate_review_ready": True,
        "ready_for_signal_or_feature_generation_approval": False,
        "signal_or_feature_generation_selected": False,
        "signal_or_feature_generation_approved": False,
        "signal_or_feature_generation_authorized": False,
        "signal_or_feature_generation_performed": False,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "signal_generation_authorized": False,
        "signal_generation_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_values_created": False,
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
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "candidate_creation_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
    }
    copied_fields = [
        "dataset_name",
        "source_profile",
        "timeframe",
        "date_range_start",
        "date_range_end",
        "target_universe",
        "target_universe_count",
        "total_canonical_record_count",
        "per_ticker_record_counts",
        "meta_record_count",
        "non_meta_record_count",
        "meta_reduced_record_count_preserved",
        "target_profile_count",
        "target_row_count",
        "available_target_row_count",
        "unavailable_target_row_count",
        "candidate_philosophy",
        "candidate_primary_question",
        "candidate_secondary_question",
        "candidate_boundary",
    ]
    review.update({field: deepcopy(source[field]) for field in copied_fields})
    review.update(
        {
            "reviewed_candidate_basis": _reviewed_candidate_basis(source),
            "reviewed_candidate_philosophy": _reviewed_candidate_philosophy(
                source
            ),
            "reviewed_signal_families": _reviewed_signal_families(source),
            "reviewed_feature_families": _reviewed_feature_families(source),
            "reviewed_recommended_feature_package": _reviewed_package(
                source["recommended_feature_package"],
                review_status="REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            ),
            "reviewed_supporting_feature_package": _reviewed_package(
                source["supporting_feature_package"],
                review_status="REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED",
            ),
            "reviewed_feature_groups": _reviewed_feature_groups(source),
            "reviewed_no_peek_and_target_separation_rules": _reviewed_no_peek_rules(
                source
            ),
            "reviewed_quality_checks": _reviewed_quality_checks(source),
            "reviewed_future_outputs": _reviewed_future_outputs(source),
            "per_ticker_signal_or_feature_generation_candidate_review_entries": _per_ticker_entries(
                source
            ),
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
    return (
        isinstance(entries, list)
        and [entry.get("ticker") for entry in entries if isinstance(entry, Mapping)]
        == TARGET_UNIVERSE
        and all(
            isinstance(entry, Mapping)
            and entry.get(
                "per_ticker_signal_or_feature_generation_candidate_review_digest"
            )
            == per_ticker_signal_or_feature_generation_candidate_review_digest_v1(
                entry
            )
            for entry in entries
        )
    )


def _reviewed_future_outputs_valid(rows: Any) -> bool:
    return (
        isinstance(rows, list)
        and len(rows) == len(candidate_service.FUTURE_OUTPUT_IDS)
        and all(
            isinstance(row, Mapping)
            and row.get("review_status")
            == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
            and row.get("output_status") == "PLANNED_NOT_GENERATED"
            and row.get("generated") is False
            for row in rows
        )
    )


def _check_definitions(review: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = candidate_service.build_marketflow_signal_or_feature_generation_candidate_v1()
    expected = _base_review(source)
    evidence = SOURCE_EVIDENCE_DIGESTS
    entries = review.get(
        "per_ticker_signal_or_feature_generation_candidate_review_entries", []
    )
    definitions = [
        ("source_signal_or_feature_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_signal_or_feature_generation_candidate_digest")),
        ("source_target_results_review_digest_bound", candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST, review.get("source_target_results_review_digest")),
        ("source_target_generation_execution_digest_bound", candidate_service.EXPECTED_SOURCE_EXECUTION_DIGEST, review.get("source_target_generation_execution_digest")),
        ("source_target_values_digest_bound", candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST, review.get("source_target_values_digest")),
        ("source_target_approval_digest_bound", candidate_service.EXPECTED_SOURCE_APPROVAL_DIGEST, review.get("marketflow_objective_label_or_target_generation_approval_digest")),
        ("source_target_candidate_review_digest_bound", evidence["marketflow_objective_label_or_target_generation_candidate_operator_review_digest"], review.get("marketflow_objective_label_or_target_generation_candidate_operator_review_digest")),
        ("source_target_candidate_digest_bound", evidence["marketflow_objective_label_or_target_generation_candidate_v1_digest"], review.get("marketflow_objective_label_or_target_generation_candidate_v1_digest")),
        ("source_design_results_review_digest_bound", evidence["marketflow_expectancy_objective_design_results_review_digest"], review.get("marketflow_expectancy_objective_design_results_review_digest")),
        ("source_design_execution_digest_bound", evidence["marketflow_expectancy_objective_design_execution_digest"], review.get("marketflow_expectancy_objective_design_execution_digest")),
        ("source_design_output_binding_digest_bound", evidence["expectancy_objective_design_output_binding_digest"], review.get("expectancy_objective_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", evidence["marketflow_expectancy_objective_approval_digest"], review.get("marketflow_expectancy_objective_approval_digest")),
        ("source_strategy_charter_approval_digest_bound", evidence["marketflow_algorithm_strategy_charter_approval_digest"], review.get("marketflow_algorithm_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", evidence["marketflow_algorithm_strategy_charter_v1_digest"], review.get("marketflow_algorithm_strategy_charter_v1_digest")),
        ("source_final_archive_digest_bound", evidence["marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"], review.get("marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest")),
        ("source_archive_digest_bound", evidence["predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"], review.get("predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest")),
        ("source_selection_digest_bound", evidence["operator_method_or_closure_selection_using_improved_evidence_digest"], review.get("operator_method_or_closure_selection_using_improved_evidence_digest")),
        ("source_closure_digest_bound", evidence["predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"], review.get("predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest")),
        ("source_readiness_digest_bound", evidence["predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"], review.get("predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest")),
        ("source_reassessment_digest_bound", evidence["predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"], review.get("predictive_usefulness_reassessment_rerun_using_improved_evidence_digest")),
        ("source_results_review_digest_bound", evidence["additional_predictive_evidence_results_review_using_improved_evidence_digest"], review.get("additional_predictive_evidence_results_review_using_improved_evidence_digest")),
        ("source_prior_execution_digest_bound", evidence["additional_predictive_evidence_execution_using_improved_evidence_digest"], review.get("additional_predictive_evidence_execution_using_improved_evidence_digest")),
        ("matrix_digest_bound", evidence["feature_label_matrix_digest"], review.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", evidence["feature_values_digest"], review.get("feature_values_digest")),
        ("label_values_digest_bound", evidence["redesigned_label_values_digest"], review.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", evidence["research_registry_approval_digest"], review.get("research_registry_approval_digest")),
        ("records_digest_bound", evidence["records_digest"], review.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, review.get("target_universe")),
        ("records_digest_preserved", evidence["records_digest"], review.get("records_digest")),
        ("meta_913_preserved", 913, review.get("meta_record_count")),
        ("source_candidate_status_ready", candidate_service.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW, review.get("source_signal_or_feature_generation_candidate_status")),
        ("source_candidate_scope_preserved", candidate_service.SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION, review.get("source_signal_or_feature_generation_candidate_scope")),
        ("review_created_true", True, review.get("signal_or_feature_generation_candidate_review_created")),
        ("review_ready_true", True, review.get("signal_or_feature_generation_candidate_review_ready")),
        ("ready_for_approval_false", False, review.get("ready_for_signal_or_feature_generation_approval")),
        ("candidate_philosophy_reviewed", expected["reviewed_candidate_philosophy"], review.get("reviewed_candidate_philosophy")),
        ("signal_families_reviewed_10", expected["reviewed_signal_families"], review.get("reviewed_signal_families")),
        ("feature_families_reviewed_10", expected["reviewed_feature_families"], review.get("reviewed_feature_families")),
        ("recommended_package_reviewed_not_selected", expected["reviewed_recommended_feature_package"], review.get("reviewed_recommended_feature_package")),
        ("supporting_package_reviewed_not_selected", expected["reviewed_supporting_feature_package"], review.get("reviewed_supporting_feature_package")),
        ("feature_groups_reviewed_17", expected["reviewed_feature_groups"], review.get("reviewed_feature_groups")),
        ("no_peek_rules_reviewed_10", expected["reviewed_no_peek_and_target_separation_rules"], review.get("reviewed_no_peek_and_target_separation_rules")),
        ("quality_checks_reviewed_10", expected["reviewed_quality_checks"], review.get("reviewed_quality_checks")),
        ("future_outputs_reviewed_not_generated", True, _reviewed_future_outputs_valid(review.get("reviewed_future_outputs"))),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("selection_created_false", False, review.get("selection_created")),
        ("approval_created_false", False, review.get("approval_created")),
        ("generation_created_false", False, review.get("generation_created")),
        ("signal_or_feature_generation_selected_false", False, review.get("signal_or_feature_generation_selected")),
        ("signal_or_feature_generation_approved_false", False, review.get("signal_or_feature_generation_approved")),
        ("signal_or_feature_generation_authorized_false", False, review.get("signal_or_feature_generation_authorized")),
        ("signal_or_feature_generation_performed_false", False, review.get("signal_or_feature_generation_performed")),
        ("signal_generation_authorized_false", False, review.get("signal_generation_authorized")),
        ("signal_generation_performed_false", False, review.get("signal_generation_performed")),
        ("feature_generation_authorized_false", False, review.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, review.get("feature_generation_performed")),
        ("feature_values_created_false", False, review.get("feature_values_created")),
        ("feature_label_matrix_created_false", False, review.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, review.get("backtest_execution_authorized")),
        ("backtest_execution_performed_false", False, review.get("backtest_execution_performed")),
        ("model_training_authorized_false", False, review.get("model_training_authorized")),
        ("model_training_performed_false", False, review.get("model_training_performed")),
        ("metric_computation_authorized_false", False, review.get("metric_computation_authorized")),
        ("metric_computation_performed_false", False, review.get("metric_computation_performed")),
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
        ("target_generation_execution_rerun_false", False, review.get("target_generation_execution_rerun_performed")),
        ("target_results_review_rerun_false", False, review.get("target_generation_results_review_rerun_performed")),
        ("candidate_creation_rerun_false", False, review.get("candidate_creation_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, review.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, review.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        ("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
    ]
    if [definition[0] for definition in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "internal checklist definition mismatch"
        )
    return definitions


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(review)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "signal_or_feature_generation_candidate_review_created": not failed,
        "signal_or_feature_generation_candidate_review_ready": not failed,
        "ready_for_signal_or_feature_generation_approval": False,
        "recommended_feature_package": RECOMMENDED_PACKAGE_ID,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "signal_generation_performed": False,
        "feature_generation_performed": False,
        "feature_values_created": False,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop(
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        None,
    )
    return payload


def marketflow_signal_or_feature_generation_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review))


def build_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Build the review package without selection, approval, or generation."""
    review = _base_review(_source_candidate(candidate))
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review[
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest"
    ] = marketflow_signal_or_feature_generation_candidate_operator_review_digest_v1(
        review
    )
    validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        review
    )
    return review


def validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact evidence, reviewed content, and every closed authority."""
    if not isinstance(review, dict):
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "review must be a JSON object"
        )
    expected = _base_review(_source_candidate(None))
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
                f"{field} mismatch"
            )
    expected_checklist = _checklist(review)
    if review.get("review_checklist") != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "review checklist mismatch"
        )
    if review.get("review_summary") != _summary(expected_checklist):
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "review summary mismatch"
        )
    digest = review.get(
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "review digest missing"
        )
    if digest != marketflow_signal_or_feature_generation_candidate_operator_review_digest_v1(
        review
    ):
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "review digest mismatch"
        )
    return {
        "status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest": digest,
        **{
            key: review["review_summary"][key]
            for key in (
                "total_checks",
                "passed_checks",
                "failed_checks",
                "blocker_count",
            )
        },
    }


def build_marketflow_signal_or_feature_generation_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        review
    )
    sections = [
        ("Title", ["Signal or Feature Generation Candidate Operator Review v1"]),
        ("Signal or Feature Generation Candidate Operator Review v1", [f"Artifact/status/scope: {review['artifact_kind']} / {review['review_status']} / {review['review_scope']}.", f"Review digest: {validation['marketflow_signal_or_feature_generation_candidate_operator_review_digest']}."]),
        ("Source Signal or Feature Candidate", [f"Candidate digest: {review['source_signal_or_feature_generation_candidate_digest']}.", f"Candidate status/scope: {review['source_signal_or_feature_generation_candidate_status']} / {review['source_signal_or_feature_generation_candidate_scope']}."]),
        ("Bound Evidence", [f"Target review/execution/target values: {review['source_target_results_review_digest']} / {review['source_target_generation_execution_digest']} / {review['source_target_values_digest']}.", f"Matrix/features/labels/records: {review['feature_label_matrix_digest']} / {review['feature_values_digest']} / {review['redesigned_label_values_digest']} / {review['records_digest']}."]),
        ("Dataset and Universe", [f"{review['dataset_name']} / {review['total_canonical_record_count']} records.", "Universe: " + ", ".join(review["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Reviewed Candidate Basis", [f"Package/path: {review['selected_label_target_package']} / {review['selected_objective_path']}.", f"Profiles/rows/available/unavailable: {review['target_profile_count']} / {review['target_row_count']} / {review['available_target_row_count']} / {review['unavailable_target_row_count']}."]),
        ("Reviewed Candidate Philosophy", [review["candidate_philosophy"], review["candidate_primary_question"], review["candidate_secondary_question"], review["candidate_boundary"]]),
        ("Reviewed Signal Families", [f"{row['signal_family_id']}: {row['review_status']}." for row in review["reviewed_signal_families"]]),
        ("Reviewed Feature Families", [f"{row['feature_family_id']}: {row['review_status']}." for row in review["reviewed_feature_families"]]),
        ("Reviewed Recommended Feature Package", [f"{review['reviewed_recommended_feature_package']['package_id']}: {review['reviewed_recommended_feature_package']['review_status']}.", review["reviewed_recommended_feature_package"]["rationale"]]),
        ("Reviewed Supporting Feature Package", [f"{review['reviewed_supporting_feature_package']['package_id']}: {review['reviewed_supporting_feature_package']['review_status']}.", review["reviewed_supporting_feature_package"]["rationale"]]),
        ("Reviewed Feature Groups", [f"{row['feature_group_id']}: {row['review_status']}." for row in review["reviewed_feature_groups"]]),
        ("Reviewed No-Peek and Target-Separation Rules", [f"{row['rule_id']}: {row['review_status']}." for row in review["reviewed_no_peek_and_target_separation_rules"]]),
        ("Reviewed Quality Checks", [f"{row['quality_check_id']}: {row['review_status']}." for row in review["reviewed_quality_checks"]]),
        ("Reviewed Future Outputs", [f"{row['future_output_id']}: {row['review_status']}." for row in review["reviewed_future_outputs"]]),
        ("Per-Ticker Review Summary", [f"{row['ticker']}: records {row['historical_record_count']}, targets {row['target_row_count']}, digest {row['per_ticker_signal_or_feature_generation_candidate_review_digest']}." for row in review["per_ticker_signal_or_feature_generation_candidate_review_entries"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {review['review_summary']['total_checks']} / {review['review_summary']['passed_checks']} / {review['review_summary']['failed_checks']} / {review['review_summary']['blocker_count']}."]),
        ("Guardrails", [review["candidate_boundary"]]),
    ]
    lines = ["# Signal or Feature Generation Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON once in an explicitly supplied directory."""
    review = build_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        candidate
    )
    validation = validate_marketflow_signal_or_feature_generation_candidate_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (
        "marketflow_signal_or_feature_generation_candidate_operator_review_v1.json"
    )
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowSignalOrFeatureGenerationCandidateOperatorReviewError(
            "signal or feature generation candidate operator review output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_signal_or_feature_generation_candidate_operator_review_digest": validation[
            "marketflow_signal_or_feature_generation_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
