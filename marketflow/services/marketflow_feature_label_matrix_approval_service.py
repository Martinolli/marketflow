"""Offline attestation-bound approval for future feature-label matrix execution."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import (
    marketflow_feature_label_matrix_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED = (
    "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_V1 = (
    "marketflow_feature_label_matrix_approval_v1"
)
MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED = "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED"
FEATURE_LABEL_MATRIX_APPROVAL_ONLY = "FEATURE_LABEL_MATRIX_APPROVAL_ONLY"
SELECTED_MATRIX_PACKAGE = review_service.RECOMMENDED_MATRIX_PACKAGE
SELECTED_MATRIX_LAYOUT = "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE"
SELECTED_FEATURE_PACKAGE = "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET"
SELECTED_LABEL_TARGET_PACKAGE = "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET"
SELECTED_OBJECTIVE_PATH = "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
OPERATOR_DECISION_APPROVE_FEATURE_LABEL_MATRIX = "APPROVE_FEATURE_LABEL_MATRIX"
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_V1 = (
    "marketflow_feature_label_matrix_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE FEATURE LABEL MATRIX "
    "PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX "
    "MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE "
    "PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET "
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET "
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT FEATURE_LABEL_MATRIX_APPROVAL_ONLY"
)

EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "0a7f440b6bfa79a8ddb0e73d24270f4004b95ef79a0cded3f188acfea4487e56"
)
EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST = (
    review_service.EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST
)
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
BOUND_EVIDENCE = dict(review_service.BOUND_EVIDENCE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_feature_label_matrix_authorized_for_future_execution_only",
    "operator_confirms_matrix_not_created",
    "operator_confirms_no_matrix_rows_created",
    "operator_confirms_no_joined_output_created",
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
    "Feature-Label Matrix Execution v1, if approved.",
    "Feature-Label Matrix Results Review v1.",
    "VPA/Wyckoff baseline candidate only after separate approval.",
    "Expectancy backtest lab candidate only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_matrix_execution_if_approved",
    "feature_label_matrix_results_review",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_matrix_construction",
    "approval_does_not_create_feature_label_matrix",
    "approval_does_not_join_features_and_targets",
    "approval_does_not_create_matrix_rows",
    "approval_does_not_create_joined_matrix_output",
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
    "approval_does_not_rerun_target_generation_execution",
    "approval_does_not_rerun_target_results_review",
    "approval_does_not_rerun_signal_feature_generation_execution",
    "approval_does_not_rerun_signal_feature_results_review",
    "approval_does_not_rerun_matrix_candidate_creation",
    "approval_does_not_rerun_matrix_candidate_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

EVIDENCE_CHECK_FIELDS = list(review_service.EVIDENCE_CHECK_FIELDS)
REQUIRED_CHECK_IDS = [
    "source_candidate_review_digest_bound", "source_matrix_candidate_digest_bound",
    *[check_id for check_id, _ in EVIDENCE_CHECK_FIELDS],
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "operator_decision_matches", "operator_attestation_phrase_matches",
    "approval_scope_only", "selected_matrix_package_wide_feature_matrix",
    "selected_matrix_layout_target_profile_wide_bundle",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "matrix_authorized_for_future_execution_true",
    "matrix_not_created", "matrix_rows_created_false",
    "joined_matrix_output_created_false", "approval_created_true",
    "ready_for_matrix_execution_true", "approved_matrix_package_present",
    "supporting_matrix_layouts_available_not_selected", "alignment_keys_approved_9",
    "feature_side_join_rules_approved_8", "target_side_join_rules_approved_7",
    "quality_checks_approved_13", "future_outputs_authorized_not_generated_12",
    "planned_matrix_row_count_179190", "planned_available_matrix_row_count_177090",
    "planned_unavailable_target_row_count_2100", "per_ticker_entries_12",
    "per_ticker_digests_present", "backtest_execution_authorized_false",
    "backtest_execution_performed_false", "model_training_authorized_false",
    "model_training_performed_false", "metric_computation_authorized_false",
    "metric_computation_performed_false", "strategy_scoring_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "signal_feature_generation_execution_rerun_false",
    "signal_feature_results_review_rerun_false", "matrix_candidate_creation_rerun_false",
    "matrix_candidate_review_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


class MarketFlowFeatureLabelMatrixApprovalError(ValueError):
    """Raised when evidence violates the approval-only contract."""


def build_marketflow_feature_label_matrix_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_signal_feature_results_review_digest: str,
    operator_confirms_feature_values_digest: str,
    operator_confirms_target_results_review_digest: str,
    operator_confirms_target_values_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_matrix_package: str,
    operator_confirms_selected_matrix_layout: str,
    operator_confirms_selected_feature_package: str,
    operator_confirms_selected_label_target_package: str,
    operator_confirms_selected_objective_path: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_feature_label_matrix_authorized_for_future_execution_only: bool,
    operator_confirms_matrix_not_created: bool,
    operator_confirms_no_matrix_rows_created: bool,
    operator_confirms_no_joined_output_created: bool,
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
    selected_matrix_package: str = SELECTED_MATRIX_PACKAGE,
    selected_matrix_layout: str = SELECTED_MATRIX_LAYOUT,
    selected_feature_package: str = SELECTED_FEATURE_PACKAGE,
    selected_label_target_package: str = SELECTED_LABEL_TARGET_PACKAGE,
    selected_objective_path: str = SELECTED_OBJECTIVE_PATH,
    operator_decision: str = OPERATOR_DECISION_APPROVE_FEATURE_LABEL_MATRIX,
) -> dict:
    """Build the complete non-secret operator attestation object."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_V1
        )
    }


@lru_cache(maxsize=1)
def _canonical_source_review() -> dict:
    return review_service.build_marketflow_feature_label_matrix_candidate_operator_review_v1()


def _source_review(source_review: dict | None) -> dict:
    source = deepcopy(_canonical_source_review()) if source_review is None else deepcopy(source_review)
    try:
        validation = review_service.validate_marketflow_feature_label_matrix_candidate_operator_review_v1(source)
    except review_service.MarketFlowFeatureLabelMatrixCandidateOperatorReviewError as exc:
        raise MarketFlowFeatureLabelMatrixApprovalError(
            "source feature-label matrix candidate review invalid"
        ) from exc
    if validation["marketflow_feature_label_matrix_candidate_operator_review_digest"] != EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST:
        raise MarketFlowFeatureLabelMatrixApprovalError(
            "source feature-label matrix candidate review digest mismatch"
        )
    return source


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowFeatureLabelMatrixApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_FEATURE_LABEL_MATRIX,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_V1,
        "operator_confirms_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "operator_confirms_signal_feature_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_feature_values_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "operator_confirms_target_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        "operator_confirms_target_values_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "operator_confirms_records_digest": BOUND_EVIDENCE["records_digest"],
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "operator_confirms_selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "operator_confirms_selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "operator_confirms_selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "operator_confirms_selected_objective_path": SELECTED_OBJECTIVE_PATH,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowFeatureLabelMatrixApprovalError(f"{field} mismatch")
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowFeatureLabelMatrixApprovalError(f"{field} must be true")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowFeatureLabelMatrixApprovalError(f"{field} required")


def _approved_matrix_package(source: Mapping[str, Any]) -> dict[str, Any]:
    reviewed = source["reviewed_recommended_matrix_package"]
    return {
        "package_id": SELECTED_MATRIX_PACKAGE,
        "approval_status": "APPROVED_FOR_FUTURE_FEATURE_LABEL_MATRIX_EXECUTION_ONLY",
        "selected_layout": SELECTED_MATRIX_LAYOUT,
        "planned_matrix_row_count": reviewed["planned_matrix_row_count"],
        "planned_available_matrix_row_count": reviewed["planned_available_matrix_row_count"],
        "planned_unavailable_target_row_count": reviewed["planned_unavailable_target_row_count"],
        "planned_feature_group_count": reviewed["planned_feature_group_count"],
        "planned_target_profile_count": reviewed["planned_target_profile_count"],
        "planned_canonical_record_count": source["planned_canonical_record_count"],
        "matrix_creation_performed": False,
        "matrix_rows_created": False,
        "joined_output_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _supporting_matrix_layouts(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "layout_id": row["layout_id"],
            "approval_status": "AVAILABLE_NOT_SELECTED",
            **({"planned_long_audit_pair_count": row["planned_long_audit_pair_count"]} if "planned_long_audit_pair_count" in row else {}),
            **({"planned_canonical_feature_bundle_count": row["planned_canonical_feature_bundle_count"]} if "planned_canonical_feature_bundle_count" in row else {}),
            "execution_performed": False,
        }
        for row in source["reviewed_matrix_layouts"]
        if row["layout_id"] != SELECTED_MATRIX_LAYOUT
    ]


def _approved_rows(
    rows: Iterable[Mapping[str, Any]], *, id_field: str, status_field: str,
    approval_status: str,
) -> list[dict[str, Any]]:
    return [
        {
            id_field: row[id_field],
            "approval_status": approval_status,
            status_field: row[status_field],
        }
        for row in rows
    ]


def _approved_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "output_id": row["output_id"],
            "approval_status": "AUTHORIZED_NOT_GENERATED",
            "output_status": row["output_status"],
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_matrix_outputs"]
    ]


def per_ticker_feature_label_matrix_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker approval entry."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_feature_label_matrix_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_feature_label_matrix_candidate_review_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "feature_label_matrix_candidate_review_status": source["review_status"],
            "feature_label_matrix_approval_status": "APPROVED_FOR_FUTURE_FEATURE_LABEL_MATRIX_EXECUTION_ONLY",
            "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
            "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
            "selected_feature_package": SELECTED_FEATURE_PACKAGE,
            "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "planned_matrix_row_count": row["planned_matrix_row_count"],
            "planned_available_matrix_row_count": row["planned_available_matrix_row_count"],
            "planned_unavailable_target_row_count": row["planned_unavailable_target_row_count"],
            "planned_feature_row_count": row["planned_feature_row_count"],
            "feature_label_matrix_selected": True,
            "feature_label_matrix_approved": True,
            "feature_label_matrix_authorized": True,
            "feature_label_matrix_created": False,
            "feature_label_matrix_rows_created": False,
            "joined_matrix_output_created": False,
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
            "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "source_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
            "source_feature_values_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
            "source_target_values_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_FEATURE_LABEL_MATRIX_APPROVAL"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_feature_label_matrix_approval_digest"] = (
            per_ticker_feature_label_matrix_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, str]:
    return {
        key: value
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _base_approval(
    source: Mapping[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    approval = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_V1,
        "approval_status": MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED,
        "approval_scope": FEATURE_LABEL_MATRIX_APPROVAL_ONLY,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "selected_feature_package": SELECTED_FEATURE_PACKAGE,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_feature_label_matrix_candidate_review_artifact_kind": source["artifact_kind"],
        "source_feature_label_matrix_candidate_review_status": source["review_status"],
        "source_feature_label_matrix_candidate_review_scope": source["review_scope"],
        "source_feature_label_matrix_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_feature_label_matrix_candidate_digest": EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        "source_signal_feature_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_RESULTS_REVIEW_DIGEST,
        "source_signal_feature_execution_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_EXECUTION_DIGEST,
        "source_signal_feature_output_binding_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_OUTPUT_BINDING_DIGEST,
        "source_feature_values_digest": review_service.candidate_service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_results_review_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_RESULTS_REVIEW_DIGEST,
        "source_target_values_digest": review_service.candidate_service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": BOUND_EVIDENCE["records_digest"],
        **_source_digest_chain(source),
        "feature_label_matrix_candidate_created": True,
        "feature_label_matrix_candidate_review_created": True,
        "feature_label_matrix_candidate_review_ready": True,
        "feature_label_matrix_selected": True,
        "feature_label_matrix_approved": True,
        "feature_label_matrix_authorized": True,
        "feature_label_matrix_approval_created": True,
        "ready_for_feature_label_matrix_execution": True,
        "feature_label_matrix_authorized_for_future_execution": True,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "feature_label_matrix_execution_performed": False,
        "joined_matrix_output_created": False,
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
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "signal_feature_generation_execution_rerun_performed": False,
        "signal_feature_results_review_rerun_performed": False,
        "matrix_candidate_creation_rerun_performed": False,
        "matrix_candidate_review_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
    }
    copied_fields = [
        "dataset_name", "source_profile", "timeframe", "date_range_start",
        "date_range_end", "target_universe", "target_universe_count",
        "total_canonical_record_count", "records_digest", "meta_record_count",
        "non_meta_record_count", "meta_reduced_record_count_preserved",
        "feature_row_count", "available_feature_row_count", "unavailable_feature_row_count",
        "target_row_count", "available_target_row_count", "unavailable_target_row_count",
        "selected_feature_group_count", "target_profile_count", "planned_matrix_row_count",
        "planned_available_matrix_row_count", "planned_unavailable_target_row_count",
        "planned_feature_group_count", "planned_target_profile_count",
        "planned_canonical_record_count",
    ]
    approval.update({field: deepcopy(source[field]) for field in copied_fields})
    approval.update({
        "approved_matrix_package": _approved_matrix_package(source),
        "supporting_matrix_layouts": _supporting_matrix_layouts(source),
        "approved_matrix_alignment_keys": _approved_rows(
            source["reviewed_matrix_alignment_keys"], id_field="alignment_key_id",
            status_field="key_status", approval_status="APPROVED_FOR_FUTURE_MATRIX_EXECUTION",
        ),
        "approved_feature_side_join_rules": _approved_rows(
            source["reviewed_feature_side_join_rules"], id_field="feature_side_join_rule_id",
            status_field="rule_status", approval_status="APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL",
        ),
        "approved_target_side_join_rules": _approved_rows(
            source["reviewed_target_side_join_rules"], id_field="target_side_join_rule_id",
            status_field="rule_status", approval_status="APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL",
        ),
        "approved_matrix_quality_checks": _approved_rows(
            source["reviewed_matrix_quality_checks"], id_field="quality_check_id",
            status_field="quality_check_status", approval_status="APPROVED_FOR_FUTURE_MATRIX_QUALITY_CONTROL",
        ),
        "approved_future_outputs": _approved_future_outputs(source),
        "per_ticker_feature_label_matrix_approval_entries": _per_ticker_entries(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    })
    return approval


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and [row.get("ticker") for row in entries if isinstance(row, Mapping)] == TARGET_UNIVERSE
        and all(
            isinstance(row, Mapping)
            and row.get("per_ticker_feature_label_matrix_approval_digest")
            == per_ticker_feature_label_matrix_approval_digest_v1(row)
            for row in entries
        )
    )


def _conditions(approval: Mapping[str, Any]) -> dict[str, bool]:
    operator = approval.get("operator_attestation", {})
    evidence = BOUND_EVIDENCE
    entries = approval.get("per_ticker_feature_label_matrix_approval_entries", [])
    conditions = {
        "source_candidate_review_digest_bound": approval.get("source_feature_label_matrix_candidate_review_digest") == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_matrix_candidate_digest_bound": approval.get("source_feature_label_matrix_candidate_digest") == EXPECTED_SOURCE_MATRIX_CANDIDATE_DIGEST,
        **{check_id: approval.get(field) == evidence[field] for check_id, field in EVIDENCE_CHECK_FIELDS},
        "target_universe_12_preserved": approval.get("target_universe") == TARGET_UNIVERSE and approval.get("target_universe_count") == 12,
        "records_digest_preserved": approval.get("records_digest") == evidence["records_digest"],
        "meta_913_preserved": approval.get("meta_record_count") == 913,
        "operator_decision_matches": operator.get("operator_decision") == OPERATOR_DECISION_APPROVE_FEATURE_LABEL_MATRIX,
        "operator_attestation_phrase_matches": operator.get("operator_attestation_phrase") == REQUIRED_MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == FEATURE_LABEL_MATRIX_APPROVAL_ONLY,
        "selected_matrix_package_wide_feature_matrix": approval.get("selected_matrix_package") == SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout_target_profile_wide_bundle": approval.get("selected_matrix_layout") == SELECTED_MATRIX_LAYOUT,
        "selected_feature_package_preserved": approval.get("selected_feature_package") == SELECTED_FEATURE_PACKAGE,
        "selected_target_package_preserved": approval.get("selected_label_target_package") == SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path_preserved": approval.get("selected_objective_path") == SELECTED_OBJECTIVE_PATH,
        "matrix_authorized_for_future_execution_true": approval.get("feature_label_matrix_authorized_for_future_execution") is True,
        "matrix_not_created": approval.get("feature_label_matrix_created") is False,
        "matrix_rows_created_false": approval.get("feature_label_matrix_rows_created") is False,
        "joined_matrix_output_created_false": approval.get("joined_matrix_output_created") is False,
        "approval_created_true": approval.get("feature_label_matrix_approval_created") is True,
        "ready_for_matrix_execution_true": approval.get("ready_for_feature_label_matrix_execution") is True,
        "approved_matrix_package_present": approval.get("approved_matrix_package", {}).get("approval_status") == "APPROVED_FOR_FUTURE_FEATURE_LABEL_MATRIX_EXECUTION_ONLY",
        "supporting_matrix_layouts_available_not_selected": len(approval.get("supporting_matrix_layouts", [])) == 2 and all(row.get("approval_status") == "AVAILABLE_NOT_SELECTED" for row in approval.get("supporting_matrix_layouts", [])),
        "alignment_keys_approved_9": len(approval.get("approved_matrix_alignment_keys", [])) == 9 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_MATRIX_EXECUTION" for row in approval.get("approved_matrix_alignment_keys", [])),
        "feature_side_join_rules_approved_8": len(approval.get("approved_feature_side_join_rules", [])) == 8 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL" for row in approval.get("approved_feature_side_join_rules", [])),
        "target_side_join_rules_approved_7": len(approval.get("approved_target_side_join_rules", [])) == 7 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_MATRIX_EXECUTION_CONTROL" for row in approval.get("approved_target_side_join_rules", [])),
        "quality_checks_approved_13": len(approval.get("approved_matrix_quality_checks", [])) == 13 and all(row.get("approval_status") == "APPROVED_FOR_FUTURE_MATRIX_QUALITY_CONTROL" for row in approval.get("approved_matrix_quality_checks", [])),
        "future_outputs_authorized_not_generated_12": len(approval.get("approved_future_outputs", [])) == 12 and all(row.get("approval_status") == "AUTHORIZED_NOT_GENERATED" and row.get("output_status") == "PLANNED_NOT_GENERATED" for row in approval.get("approved_future_outputs", [])),
        "planned_matrix_row_count_179190": approval.get("planned_matrix_row_count") == 179190,
        "planned_available_matrix_row_count_177090": approval.get("planned_available_matrix_row_count") == 177090,
        "planned_unavailable_target_row_count_2100": approval.get("planned_unavailable_target_row_count") == 2100,
        "per_ticker_entries_12": len(entries) == 12 if isinstance(entries, list) else False,
        "per_ticker_digests_present": _per_ticker_digests_valid(entries),
        "backtest_execution_authorized_false": approval.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": approval.get("backtest_execution_performed") is False,
        "model_training_authorized_false": approval.get("model_training_authorized") is False,
        "model_training_performed_false": approval.get("model_training_performed") is False,
        "metric_computation_authorized_false": approval.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": approval.get("metric_computation_performed") is False,
        "strategy_scoring_false": approval.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": approval.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": approval.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": approval.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": approval.get("provider_requests_made_in_approval") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval") is False,
        "dataset_regeneration_false": approval.get("canonical_dataset_regenerated_in_approval") is False,
        "target_generation_execution_rerun_false": approval.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": approval.get("target_generation_results_review_rerun_performed") is False,
        "signal_feature_generation_execution_rerun_false": approval.get("signal_feature_generation_execution_rerun_performed") is False,
        "signal_feature_results_review_rerun_false": approval.get("signal_feature_results_review_rerun_performed") is False,
        "matrix_candidate_creation_rerun_false": approval.get("matrix_candidate_creation_rerun_performed") is False,
        "matrix_candidate_review_rerun_false": approval.get("matrix_candidate_review_rerun_performed") is False,
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True,
    }
    if list(conditions) != REQUIRED_CHECK_IDS:
        raise MarketFlowFeatureLabelMatrixApprovalError("internal checklist definition mismatch")
    return conditions


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "status": PASS if actual else FAIL,
            "expected": True,
            "actual": actual,
            "severity": BLOCKER,
            "message": f"{check_id} {'passed' if actual else 'failed'}",
        }
        for check_id, actual in _conditions(approval).items()
    ]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "feature_label_matrix_selected": True,
        "feature_label_matrix_approved": True,
        "feature_label_matrix_authorized": True,
        "ready_for_feature_label_matrix_execution": True,
        "selected_matrix_package": SELECTED_MATRIX_PACKAGE,
        "selected_matrix_layout": SELECTED_MATRIX_LAYOUT,
        "feature_label_matrix_authorized_for_future_execution": True,
        "feature_label_matrix_created": False,
        "feature_label_matrix_rows_created": False,
        "joined_matrix_output_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def marketflow_feature_label_matrix_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    payload = deepcopy(dict(approval))
    payload.pop("approval_checklist", None)
    payload.pop("approval_summary", None)
    payload.pop("marketflow_feature_label_matrix_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_feature_label_matrix_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict
) -> dict:
    """Build approval for future feature-label matrix execution only."""
    source = _source_review(source_review)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    approval["marketflow_feature_label_matrix_approval_digest"] = (
        marketflow_feature_label_matrix_approval_digest_v1(approval)
    )
    validate_marketflow_feature_label_matrix_approval_v1(approval)
    return approval


def validate_marketflow_feature_label_matrix_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, evidence, approved controls, and closed authorities."""
    if not isinstance(approval, dict):
        raise MarketFlowFeatureLabelMatrixApprovalError("approval must be a JSON object")
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(_source_review(None), attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowFeatureLabelMatrixApprovalError(f"{field} mismatch")
    expected_checklist = _checklist(approval)
    if approval.get("approval_checklist") != expected_checklist or any(
        row["status"] != PASS for row in expected_checklist
    ):
        raise MarketFlowFeatureLabelMatrixApprovalError("approval checklist mismatch")
    if approval.get("approval_summary") != _summary(expected_checklist):
        raise MarketFlowFeatureLabelMatrixApprovalError("approval summary mismatch")
    digest = approval.get("marketflow_feature_label_matrix_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowFeatureLabelMatrixApprovalError("approval digest missing")
    if digest != marketflow_feature_label_matrix_approval_digest_v1(approval):
        raise MarketFlowFeatureLabelMatrixApprovalError("approval digest mismatch")
    return {
        "status": "MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "marketflow_feature_label_matrix_approval_digest": digest,
        **{
            field: approval["approval_summary"][field]
            for field in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_feature_label_matrix_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval artifact."""
    validation = validate_marketflow_feature_label_matrix_approval_v1(approval)
    operator = approval["operator_attestation"]
    sections = [
        ("Title", ["Feature-Label Matrix Approval v1"]),
        ("Feature-Label Matrix Approval v1", [f"Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.", f"Approval digest: `{validation['marketflow_feature_label_matrix_approval_digest']}`."]),
        ("Operator Attestation", [f"Decision/reference/timestamp: `{operator['operator_decision']}` / `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}`.", f"Exact phrase: {operator['operator_attestation_phrase']}."]),
        ("Source Matrix Candidate Review", [f"Review/candidate digests: `{approval['source_feature_label_matrix_candidate_review_digest']}` / `{approval['source_feature_label_matrix_candidate_digest']}`."]),
        ("Bound Evidence", [f"Feature/target values: `{approval['source_feature_values_digest']}` / `{approval['source_target_values_digest']}`.", f"Records: `{approval['records_digest']}`; complete upstream digest chain preserved."]),
        ("Dataset and Universe", [f"`{approval['dataset_name']}`, {approval['total_canonical_record_count']} records; {', '.join(approval['target_universe'])}.", "META remains exactly 913 records; every other ticker remains 1,003."]),
        ("Approval Scope", ["Future feature-label matrix execution only; this artifact performs no matrix construction."]),
        ("Selected Matrix Package", [approval["selected_matrix_package"]]),
        ("Selected Matrix Layout", [approval["selected_matrix_layout"]]),
        ("Selected Feature and Target Packages", [f"{approval['selected_feature_package']} / {approval['selected_label_target_package']} / {approval['selected_objective_path']}."]),
        ("Approved Matrix Counts", [f"{approval['planned_matrix_row_count']} planned rows; {approval['planned_available_matrix_row_count']} available and {approval['planned_unavailable_target_row_count']} unavailable."]),
        ("Approved Alignment Keys", [row["alignment_key_id"] for row in approval["approved_matrix_alignment_keys"]]),
        ("Approved Feature-Side Join Rules", [row["feature_side_join_rule_id"] for row in approval["approved_feature_side_join_rules"]]),
        ("Approved Target-Side Join Rules", [row["target_side_join_rule_id"] for row in approval["approved_target_side_join_rules"]]),
        ("Approved Matrix Quality Checks", [row["quality_check_id"] for row in approval["approved_matrix_quality_checks"]]),
        ("Approved Future Outputs", [f"{row['output_id']}: {row['approval_status']}." for row in approval["approved_future_outputs"]]),
        ("Per-Ticker Approval Summary", [f"{row['ticker']}: records {row['historical_record_count']}, planned rows {row['planned_matrix_row_count']}, digest `{row['per_ticker_feature_label_matrix_approval_digest']}`." for row in approval["per_ticker_feature_label_matrix_approval_entries"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{approval['approval_summary']['passed_checks']}/{approval['approval_summary']['total_checks']} checks pass with zero blockers."]),
        ("Guardrails", ["This approval authorizes only future research-only matrix execution and creates no matrix, joined output, metric, model, recommendation, runtime artifact, or trading authority."]),
    ]
    lines = ["# Feature-Label Matrix Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", "", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_feature_label_matrix_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write validated approval JSON and Markdown to an explicit directory."""
    approval = build_marketflow_feature_label_matrix_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_feature_label_matrix_approval_v1(approval)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_feature_label_matrix_approval_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowFeatureLabelMatrixApprovalError(
            "feature-label matrix approval output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(approval))
    markdown_path.write_text(
        build_marketflow_feature_label_matrix_approval_markdown_v1(approval),
        encoding="utf-8", newline="\n",
    )
    return {
        **validation,
        "json_path": str(json_path).replace("\\", "/"),
        "markdown_path": str(markdown_path).replace("\\", "/"),
    }
