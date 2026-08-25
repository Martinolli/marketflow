"""Offline operator review of the feature-label matrix candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_feature_label_matrix_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_feature_label_matrix_candidate_operator_review_v1"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_VALID = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_VALID"
)

EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST = (
    "ef3d42d39a5ae353044d29d645a7ca1ad01143e5557951b05b85f837413187b4"
)
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
RECOMMENDED_MATRIX_PACKAGE = (
    candidate_service.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER
BOUND_EVIDENCE = {
    **{
        key: value
        for key, value in candidate_service.SOURCE_EVIDENCE.items()
        if key not in {"feature_label_matrix_digest", "feature_values_digest"}
    },
    "prior_feature_label_matrix_digest": candidate_service.SOURCE_EVIDENCE[
        "feature_label_matrix_digest"
    ],
    "prior_feature_values_digest": candidate_service.SOURCE_EVIDENCE[
        "feature_values_digest"
    ],
}

NEXT_CHAIN = [
    "Feature-Label Matrix Approval v1, if selected.",
    "Feature-Label Matrix Execution v1, if approved.",
    "Feature-Label Matrix Results Review v1.",
    "VPA/Wyckoff baseline candidate only after separate approval.",
    "Expectancy backtest lab candidate only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_matrix_approval_if_selected",
    "feature_label_matrix_execution_if_approved",
    "feature_label_matrix_results_review",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_select_matrix_package",
    "review_does_not_approve_matrix_construction",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_join_features_and_targets",
    "review_does_not_create_matrix_rows",
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
    "review_does_not_rerun_signal_feature_generation_execution",
    "review_does_not_rerun_signal_feature_results_review",
    "review_does_not_rerun_matrix_candidate_creation",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

EVIDENCE_CHECK_FIELDS = [
    ("source_signal_feature_results_review_digest_bound", "marketflow_signal_or_feature_generation_results_review_digest"),
    ("source_signal_feature_execution_digest_bound", "marketflow_signal_or_feature_generation_execution_digest"),
    ("source_signal_feature_output_binding_digest_bound", "signal_or_feature_generation_output_binding_digest"),
    ("source_feature_values_digest_bound", "signal_or_feature_values_digest"),
    ("source_target_results_review_digest_bound", "marketflow_objective_label_or_target_generation_results_review_digest"),
    ("source_target_generation_execution_digest_bound", "marketflow_objective_label_or_target_generation_execution_digest"),
    ("source_target_output_binding_digest_bound", "objective_label_or_target_generation_output_binding_digest"),
    ("source_target_values_digest_bound", "objective_label_or_target_values_digest"),
    ("source_signal_feature_approval_digest_bound", "marketflow_signal_or_feature_generation_approval_digest"),
    ("source_signal_feature_candidate_review_digest_bound", "marketflow_signal_or_feature_generation_candidate_operator_review_digest"),
    ("source_signal_feature_candidate_digest_bound", "marketflow_signal_or_feature_generation_candidate_v1_digest"),
    ("source_target_approval_digest_bound", "marketflow_objective_label_or_target_generation_approval_digest"),
    ("source_design_results_review_digest_bound", "marketflow_expectancy_objective_design_results_review_digest"),
    ("source_design_execution_digest_bound", "marketflow_expectancy_objective_design_execution_digest"),
    ("source_design_output_binding_digest_bound", "expectancy_objective_design_output_binding_digest"),
    ("source_expectancy_objective_approval_digest_bound", "marketflow_expectancy_objective_approval_digest"),
    ("source_strategy_charter_approval_digest_bound", "marketflow_algorithm_strategy_charter_approval_digest"),
    ("source_strategy_charter_digest_bound", "marketflow_algorithm_strategy_charter_v1_digest"),
    ("source_final_archive_digest_bound", "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest"),
    ("source_archive_digest_bound", "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest"),
    ("source_selection_digest_bound", "operator_method_or_closure_selection_using_improved_evidence_digest"),
    ("source_closure_digest_bound", "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest"),
    ("source_readiness_digest_bound", "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest"),
    ("source_reassessment_digest_bound", "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"),
    ("source_results_review_digest_bound", "additional_predictive_evidence_results_review_using_improved_evidence_digest"),
    ("source_prior_execution_digest_bound", "additional_predictive_evidence_execution_using_improved_evidence_digest"),
    ("prior_matrix_digest_bound", "prior_feature_label_matrix_digest"),
    ("prior_feature_values_digest_bound", "prior_feature_values_digest"),
    ("prior_label_values_digest_bound", "redesigned_label_values_digest"),
    ("research_registry_digest_bound", "research_registry_approval_digest"),
    ("records_digest_bound", "records_digest"),
]

REQUIRED_CHECK_IDS = [
    "source_matrix_candidate_digest_bound",
    *[check_id for check_id, _ in EVIDENCE_CHECK_FIELDS],
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "source_candidate_status_ready", "source_candidate_scope_preserved",
    "review_created_true", "review_ready_true", "ready_for_approval_false",
    "recommended_matrix_package_reviewed_not_selected", "matrix_layouts_reviewed",
    "alignment_keys_reviewed_9", "feature_side_join_rules_reviewed_8",
    "target_side_join_rules_reviewed_7", "quality_checks_reviewed_13",
    "future_outputs_reviewed_not_generated_12", "planned_matrix_row_count_179190",
    "planned_available_matrix_row_count_177090",
    "planned_unavailable_target_row_count_2100", "per_ticker_entries_12",
    "per_ticker_digests_present", "selection_created_false",
    "approval_created_false", "execution_created_false",
    "feature_label_matrix_selected_false", "feature_label_matrix_approved_false",
    "feature_label_matrix_authorized_false", "feature_label_matrix_created_false",
    "feature_label_matrix_rows_created_false", "backtest_execution_authorized_false",
    "backtest_execution_performed_false", "model_training_authorized_false",
    "model_training_performed_false", "metric_computation_authorized_false",
    "metric_computation_performed_false", "strategy_scoring_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "signal_feature_generation_execution_rerun_false",
    "signal_feature_results_review_rerun_false",
    "matrix_candidate_creation_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(ValueError):
    """Raised when the operator review violates its review-only contract."""


def _source_candidate(candidate: dict | None) -> dict:
    source = (
        candidate_service.build_marketflow_feature_label_matrix_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        validation = candidate_service.validate_marketflow_feature_label_matrix_candidate_v1(source)
    except candidate_service.MarketFlowFeatureLabelMatrixCandidateError as exc:
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "source feature-label matrix candidate invalid"
        ) from exc
    if validation["marketflow_feature_label_matrix_candidate_v1_digest"] != EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST:
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "source feature-label matrix candidate digest mismatch"
        )
    return source


def _reviewed_rows(
    rows: Iterable[Mapping[str, Any]], *, review_status: str
) -> list[dict[str, Any]]:
    return [{**deepcopy(dict(row)), "review_status": review_status} for row in rows]


def _reviewed_layouts(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    reviewed = []
    for row in source["matrix_layouts"]:
        item = deepcopy(row)
        item["source_status"] = item.pop("status")
        item["review_status"] = (
            "REVIEWED_RECOMMENDED_LAYOUT_NOT_SELECTED"
            if item["layout_id"] == "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
            else "REVIEWED_AVAILABLE_LAYOUT_NOT_SELECTED"
        )
        reviewed.append(item)
    return reviewed


def _reviewed_package(source: Mapping[str, Any]) -> dict[str, Any]:
    package = deepcopy(source["recommended_matrix_package_definition"])
    package["source_status"] = package.pop("status")
    package["review_status"] = (
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    )
    package["research_only"] = True
    package["non_actionable"] = True
    return package


def per_ticker_feature_label_matrix_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_feature_label_matrix_candidate_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_feature_label_matrix_candidate_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "feature_label_matrix_candidate_status": source["candidate_status"],
            "feature_label_matrix_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "signal_or_feature_results_review_status": row["signal_or_feature_results_review_status"],
            "target_results_review_status": row["target_results_review_status"],
            "selected_feature_package": row["selected_feature_package"],
            "selected_label_target_package": row["selected_label_target_package"],
            "selected_objective_path": row["selected_objective_path"],
            "recommended_matrix_package": row["recommended_matrix_package"],
            "planned_matrix_row_count": row["planned_matrix_row_count"],
            "planned_available_matrix_row_count": row["planned_available_matrix_row_count"],
            "planned_unavailable_target_row_count": row["planned_unavailable_target_row_count"],
            "planned_feature_row_count": row["planned_feature_row_count"],
            "feature_label_matrix_selected": False,
            "feature_label_matrix_approved": False,
            "feature_label_matrix_authorized": False,
            "feature_label_matrix_created": False,
            "feature_label_matrix_rows_created": False,
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
            "source_matrix_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
            "source_signal_feature_results_review_digest": candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
            "source_feature_values_digest": candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
            "source_target_values_digest": candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_CANDIDATE_REVIEW"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_feature_label_matrix_candidate_review_digest"] = (
            per_ticker_feature_label_matrix_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: Mapping[str, Any]) -> dict[str, Any]:
    reviewed_basis_fields = [
        "recommended_matrix_package", "selected_feature_package",
        "selected_label_target_package", "selected_objective_path",
        "feature_values_digest", "target_values_digest", "feature_row_count",
        "available_feature_row_count", "unavailable_feature_row_count",
        "target_row_count", "available_target_row_count", "unavailable_target_row_count",
        "selected_feature_group_count", "target_profile_count", "planned_matrix_row_count",
        "planned_available_matrix_row_count", "planned_unavailable_target_row_count",
        "planned_feature_group_count", "planned_target_profile_count",
        "planned_canonical_record_count",
    ]
    reviewed_basis = {field: deepcopy(source[field]) for field in reviewed_basis_fields}
    reviewed_basis.update({
        "review_status": "REVIEWED_MATRIX_CANDIDATE_BASIS",
        "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
    })
    reviewed_philosophy = {
        field: deepcopy(source[field])
        for field in (
            "candidate_philosophy", "candidate_primary_question",
            "candidate_secondary_question", "candidate_boundary",
        )
    }
    reviewed_philosophy.update({
        "review_status": "REVIEWED_MATRIX_CANDIDATE_PHILOSOPHY",
        "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
    })
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_feature_label_matrix_candidate_artifact_kind": source["artifact_kind"],
        "source_feature_label_matrix_candidate_status": source["candidate_status"],
        "source_feature_label_matrix_candidate_scope": source["candidate_scope"],
        "source_feature_label_matrix_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "marketflow_feature_label_matrix_candidate_v1_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "source_signal_feature_results_review_digest": candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        "source_signal_feature_execution_digest": candidate_service.EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
        "source_signal_feature_output_binding_digest": candidate_service.EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
        "source_feature_values_digest": candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_results_review_digest": candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        "source_target_values_digest": candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        **deepcopy(source["source_evidence"]),
        "prior_feature_label_matrix_digest": source["source_evidence"]["feature_label_matrix_digest"],
        "prior_feature_values_digest": source["source_evidence"]["feature_values_digest"],
        "feature_label_matrix_candidate_created": True,
        "feature_label_matrix_candidate_ready_for_operator_review": True,
        "feature_label_matrix_candidate_review_created": True,
        "feature_label_matrix_candidate_review_ready": True,
        "ready_for_feature_label_matrix_approval": False,
        "feature_label_matrix_selected": False,
        "feature_label_matrix_approved": False,
        "feature_label_matrix_authorized": False,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "feature_label_matrix_execution_performed": False,
        "selection_created": False,
        "approval_created": False,
        "creation_created": False,
        "execution_created": False,
        "generation_created": False,
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
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "matrix_candidate_creation_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
    }
    copied_fields = [
        "selected_feature_package", "selected_label_target_package",
        "selected_objective_path", "dataset_name", "source_profile", "timeframe",
        "date_range_start", "date_range_end", "target_universe",
        "target_universe_count", "total_canonical_record_count", "records_digest",
        "meta_record_count", "non_meta_record_count", "meta_reduced_record_count_preserved",
        "feature_values_digest", "target_values_digest", "feature_row_count",
        "available_feature_row_count", "unavailable_feature_row_count",
        "target_row_count", "available_target_row_count", "unavailable_target_row_count",
        "selected_feature_group_count", "target_profile_count", "candidate_philosophy",
        "candidate_primary_question", "candidate_secondary_question", "candidate_boundary",
        "planned_matrix_row_count", "planned_available_matrix_row_count",
        "planned_unavailable_target_row_count", "planned_feature_group_count",
        "planned_target_profile_count", "planned_canonical_record_count",
    ]
    review.update({field: deepcopy(source[field]) for field in copied_fields})
    review.update({
        "recommended_matrix_package": RECOMMENDED_MATRIX_PACKAGE,
        "reviewed_candidate_basis": reviewed_basis,
        "reviewed_candidate_philosophy": reviewed_philosophy,
        "reviewed_matrix_layouts": _reviewed_layouts(source),
        "reviewed_recommended_matrix_package": _reviewed_package(source),
        "reviewed_matrix_alignment_keys": _reviewed_rows(
            source["matrix_alignment_keys"],
            review_status="REVIEWED_PLANNED_KEY_NOT_EXECUTED",
        ),
        "reviewed_feature_side_join_rules": _reviewed_rows(
            source["feature_side_join_rules"],
            review_status="REVIEWED_PLANNED_FEATURE_JOIN_RULE_NOT_EXECUTED",
        ),
        "reviewed_target_side_join_rules": _reviewed_rows(
            source["target_side_join_rules"],
            review_status="REVIEWED_PLANNED_TARGET_JOIN_RULE_NOT_EXECUTED",
        ),
        "reviewed_matrix_quality_checks": _reviewed_rows(
            source["matrix_quality_checks"],
            review_status="REVIEWED_PLANNED_MATRIX_QUALITY_CHECK_NOT_EXECUTED",
        ),
        "reviewed_planned_matrix_outputs": _reviewed_rows(
            source["planned_future_outputs"],
            review_status="REVIEWED_PLANNED_MATRIX_OUTPUT_NOT_GENERATED",
        ),
        "per_ticker_feature_label_matrix_candidate_review_entries": _per_ticker_entries(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    })
    return review


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and [row.get("ticker") for row in entries if isinstance(row, Mapping)] == TARGET_UNIVERSE
        and all(
            isinstance(row, Mapping)
            and row.get("per_ticker_feature_label_matrix_candidate_review_digest")
            == per_ticker_feature_label_matrix_candidate_review_digest_v1(row)
            for row in entries
        )
    )


def _review_conditions(review: Mapping[str, Any]) -> dict[str, bool]:
    evidence = BOUND_EVIDENCE
    conditions = {
        "source_matrix_candidate_digest_bound": review.get("source_feature_label_matrix_candidate_digest") == EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        **{
            check_id: review.get(field) == evidence[field]
            for check_id, field in EVIDENCE_CHECK_FIELDS
        },
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == 12,
        "records_digest_preserved": review.get("records_digest") == evidence["records_digest"],
        "meta_913_preserved": review.get("meta_record_count") == 913,
        "source_candidate_status_ready": review.get("source_feature_label_matrix_candidate_status") == candidate_service.MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source_candidate_scope_preserved": review.get("source_feature_label_matrix_candidate_scope") == candidate_service.FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION,
        "review_created_true": review.get("feature_label_matrix_candidate_review_created") is True,
        "review_ready_true": review.get("feature_label_matrix_candidate_review_ready") is True,
        "ready_for_approval_false": review.get("ready_for_feature_label_matrix_approval") is False,
        "recommended_matrix_package_reviewed_not_selected": review.get("reviewed_recommended_matrix_package", {}).get("review_status") == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" and review.get("reviewed_recommended_matrix_package", {}).get("selection_created") is False,
        "matrix_layouts_reviewed": len(review.get("reviewed_matrix_layouts", [])) == 3 and all(row.get("selection_created") is False for row in review.get("reviewed_matrix_layouts", [])),
        "alignment_keys_reviewed_9": len(review.get("reviewed_matrix_alignment_keys", [])) == 9 and all(row.get("review_status") == "REVIEWED_PLANNED_KEY_NOT_EXECUTED" for row in review.get("reviewed_matrix_alignment_keys", [])),
        "feature_side_join_rules_reviewed_8": len(review.get("reviewed_feature_side_join_rules", [])) == 8 and all(row.get("review_status") == "REVIEWED_PLANNED_FEATURE_JOIN_RULE_NOT_EXECUTED" for row in review.get("reviewed_feature_side_join_rules", [])),
        "target_side_join_rules_reviewed_7": len(review.get("reviewed_target_side_join_rules", [])) == 7 and all(row.get("review_status") == "REVIEWED_PLANNED_TARGET_JOIN_RULE_NOT_EXECUTED" for row in review.get("reviewed_target_side_join_rules", [])),
        "quality_checks_reviewed_13": len(review.get("reviewed_matrix_quality_checks", [])) == 13 and all(row.get("review_status") == "REVIEWED_PLANNED_MATRIX_QUALITY_CHECK_NOT_EXECUTED" for row in review.get("reviewed_matrix_quality_checks", [])),
        "future_outputs_reviewed_not_generated_12": len(review.get("reviewed_planned_matrix_outputs", [])) == 12 and all(row.get("review_status") == "REVIEWED_PLANNED_MATRIX_OUTPUT_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in review.get("reviewed_planned_matrix_outputs", [])),
        "planned_matrix_row_count_179190": review.get("planned_matrix_row_count") == 179190,
        "planned_available_matrix_row_count_177090": review.get("planned_available_matrix_row_count") == 177090,
        "planned_unavailable_target_row_count_2100": review.get("planned_unavailable_target_row_count") == 2100,
        "per_ticker_entries_12": len(review.get("per_ticker_feature_label_matrix_candidate_review_entries", [])) == 12,
        "per_ticker_digests_present": _per_ticker_digests_valid(review.get("per_ticker_feature_label_matrix_candidate_review_entries")),
        "selection_created_false": review.get("selection_created") is False,
        "approval_created_false": review.get("approval_created") is False,
        "execution_created_false": review.get("execution_created") is False,
        "feature_label_matrix_selected_false": review.get("feature_label_matrix_selected") is False,
        "feature_label_matrix_approved_false": review.get("feature_label_matrix_approved") is False,
        "feature_label_matrix_authorized_false": review.get("feature_label_matrix_authorized") is False,
        "feature_label_matrix_created_false": review.get("feature_label_matrix_created") is False,
        "feature_label_matrix_rows_created_false": review.get("feature_label_matrix_rows_created") is False,
        "backtest_execution_authorized_false": review.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": review.get("backtest_execution_performed") is False,
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "metric_computation_authorized_false": review.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": review.get("metric_computation_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review") is False,
        "target_generation_execution_rerun_false": review.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": review.get("target_generation_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": review.get("signal_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": review.get("signal_feature_results_review_rerun_performed") is False,
        "matrix_candidate_creation_rerun_false": review.get("matrix_candidate_creation_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    }
    if list(conditions) != REQUIRED_CHECK_IDS:
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "internal checklist definition mismatch"
        )
    return conditions


def _checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "status": PASS if actual else FAIL,
            "expected": True,
            "actual": actual,
            "severity": BLOCKER,
            "message": f"{check_id} {'passed' if actual else 'failed'}",
        }
        for check_id, actual in _review_conditions(review).items()
    ]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "feature_label_matrix_candidate_review_created": not failed,
        "feature_label_matrix_candidate_review_ready": not failed,
        "ready_for_feature_label_matrix_approval": False,
        "recommended_matrix_package": RECOMMENDED_MATRIX_PACKAGE,
        "selection_created": False,
        "approval_created": False,
        "execution_created": False,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_feature_label_matrix_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for the review package."""
    payload = deepcopy(dict(review))
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop("marketflow_feature_label_matrix_candidate_operator_review_digest", None)
    return semantic_digest(payload)


def build_marketflow_feature_label_matrix_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Build an operator-review package without selection or approval."""
    review = _base_review(_source_candidate(candidate))
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review["marketflow_feature_label_matrix_candidate_operator_review_digest"] = (
        marketflow_feature_label_matrix_candidate_operator_review_digest_v1(review)
    )
    validate_marketflow_feature_label_matrix_candidate_operator_review_v1(review)
    return review


def validate_marketflow_feature_label_matrix_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact evidence, reviewed content, and closed authorities."""
    if not isinstance(review, dict):
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "feature-label matrix candidate review must be a JSON object"
        )
    expected = _base_review(_source_candidate(None))
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
                f"{field} mismatch"
            )
    expected_checklist = _checklist(review)
    if review.get("review_checklist") != expected_checklist or any(
        row["status"] != PASS for row in expected_checklist
    ):
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "review checklist mismatch"
        )
    if review.get("review_summary") != _summary(expected_checklist):
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "review summary mismatch"
        )
    digest = review.get("marketflow_feature_label_matrix_candidate_operator_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "review digest missing"
        )
    if digest != marketflow_feature_label_matrix_candidate_operator_review_digest_v1(review):
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "review digest mismatch"
        )
    return {
        "status": MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_OPERATOR_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_feature_label_matrix_candidate_operator_review_digest": digest,
        **{
            field: review["review_summary"][field]
            for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_feature_label_matrix_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_marketflow_feature_label_matrix_candidate_operator_review_v1(review)
    sections = [
        ("Title", ["Feature-Label Matrix Candidate Operator Review v1"]),
        ("Feature-Label Matrix Candidate Operator Review v1", [f"Artifact/status/scope: `{review['artifact_kind']}` / `{review['review_status']}` / `{review['review_scope']}`.", f"Review digest: `{validation['marketflow_feature_label_matrix_candidate_operator_review_digest']}`."]),
        ("Source Feature-Label Matrix Candidate", [f"Candidate digest: `{review['source_feature_label_matrix_candidate_digest']}`.", f"Candidate status/scope: `{review['source_feature_label_matrix_candidate_status']}` / `{review['source_feature_label_matrix_candidate_scope']}`."]),
        ("Source Signal or Feature Results Review", [f"Source review digest: `{review['source_signal_feature_results_review_digest']}`."]),
        ("Source Target Results Review", [f"Source review digest: `{review['source_target_results_review_digest']}`."]),
        ("Bound Evidence", [f"Feature/target values: `{review['source_feature_values_digest']}` / `{review['source_target_values_digest']}`.", "The complete upstream digest chain is preserved."]),
        ("Dataset and Universe", [f"`{review['dataset_name']}`, {review['total_canonical_record_count']} records, ordered universe: {', '.join(review['target_universe'])}.", "META remains exactly 913 records; every other ticker remains 1,003."]),
        ("Reviewed Candidate Basis", [f"13 feature groups and 15 target profiles plan {review['planned_matrix_row_count']} rows; {review['planned_available_matrix_row_count']} available and {review['planned_unavailable_target_row_count']} unavailable."]),
        ("Reviewed Candidate Philosophy", [review["candidate_philosophy"], review["candidate_primary_question"], review["candidate_secondary_question"], review["candidate_boundary"]]),
        ("Reviewed Matrix Layouts", [f"`{row['layout_id']}`: {row['review_status']}." for row in review["reviewed_matrix_layouts"]]),
        ("Reviewed Recommended Matrix Package", [f"`{RECOMMENDED_MATRIX_PACKAGE}`: {review['reviewed_recommended_matrix_package']['review_status']}."]),
        ("Reviewed Alignment Keys", [f"`{row['alignment_key_id']}`: {row['review_status']}." for row in review["reviewed_matrix_alignment_keys"]]),
        ("Reviewed Feature-Side Join Rules", [f"`{row['feature_side_join_rule_id']}`: {row['review_status']}." for row in review["reviewed_feature_side_join_rules"]]),
        ("Reviewed Target-Side Join Rules", [f"`{row['target_side_join_rule_id']}`: {row['review_status']}." for row in review["reviewed_target_side_join_rules"]]),
        ("Reviewed Matrix Quality Checks", [f"`{row['quality_check_id']}`: {row['review_status']}." for row in review["reviewed_matrix_quality_checks"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_id']}`: {row['review_status']}." for row in review["reviewed_planned_matrix_outputs"]]),
        ("Per-Ticker Review Summary", [f"{row['ticker']}: records {row['historical_record_count']}, planned rows {row['planned_matrix_row_count']}, digest `{row['per_ticker_feature_label_matrix_candidate_review_digest']}`." for row in review["per_ticker_feature_label_matrix_candidate_review_entries"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass with zero blockers."]),
        ("Guardrails", ["This review selects and approves nothing and creates no matrix rows, joins, backtests, models, metrics, scores, recommendations, runtime artifacts, or trading authority."]),
    ]
    lines = ["# Feature-Label Matrix Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", "", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_feature_label_matrix_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write validated review JSON and Markdown to an explicit directory."""
    review = build_marketflow_feature_label_matrix_candidate_operator_review_v1(candidate)
    validation = validate_marketflow_feature_label_matrix_candidate_operator_review_v1(review)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_feature_label_matrix_candidate_operator_review_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowFeatureLabelMatrixCandidateOperatorReviewError(
            "feature-label matrix candidate operator review output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_feature_label_matrix_candidate_operator_review_markdown_v1(review),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path).replace("\\", "/"),
        "markdown_path": str(markdown_path).replace("\\", "/"),
    }
