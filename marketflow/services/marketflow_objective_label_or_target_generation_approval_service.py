"""Offline attestation-bound approval for future label or target generation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    marketflow_objective_label_or_target_generation_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_V1 = (
    "marketflow_objective_label_or_target_generation_approval_v1"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED"
)
OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY = (
    "OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY"
)
SELECTED_LABEL_TARGET_PACKAGE = review_service.RECOMMENDED_PACKAGE_ID
SELECTED_OBJECTIVE_PATH = review_service.SELECTED_OBJECTIVE_PATH
OPERATOR_DECISION_APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION = (
    "APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION"
)
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_V1 = (
    "marketflow_objective_label_or_target_generation_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE OBJECTIVE LABEL OR TARGET GENERATION "
    "PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET "
    "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT "
    "OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY"
)
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    "ec9e117ad735e984a52c5600374ae274aceec8e58bc5aeb9e75a4357dcfd5e1b"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
SOURCE_EVIDENCE_DIGESTS = dict(review_service.SOURCE_EVIDENCE_DIGESTS)
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
NOT_ACCEPTED = review_service.NOT_ACCEPTED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_generation_authorized_for_future_execution_only",
    "operator_confirms_generation_not_performed",
    "operator_confirms_no_label_values_created",
    "operator_confirms_no_target_values_created",
    "operator_confirms_no_new_targets_created",
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
    "Objective Label or Target Generation Execution v1, if approved.",
    "Objective Label or Target Generation Results Review v1.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "objective_label_or_target_generation_execution_if_approved",
    "objective_label_or_target_generation_results_review",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_generation",
    "approval_does_not_create_label_values",
    "approval_does_not_create_target_values",
    "approval_does_not_create_new_targets_now",
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
    "approval_does_not_rerun_candidate_creation",
    "approval_does_not_rerun_candidate_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_expectancy_objective_candidate_digest_bound",
    "source_strategy_charter_approval_digest_bound",
    "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_execution_digest_bound",
    "matrix_digest_bound",
    "feature_values_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_package_expectancy_payoff_abstention",
    "selected_objective_path_preserved",
    "generation_authorized_for_future_execution_true",
    "generation_performed_false",
    "approval_created_true",
    "ready_for_generation_execution_true",
    "selected_label_target_families_5",
    "supporting_label_target_families_available_not_selected",
    "formula_dimensions_approved_14",
    "availability_rules_approved_10",
    "quality_checks_approved_10",
    "future_outputs_authorized_not_generated_11",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "label_generation_performed_false",
    "target_generation_performed_false",
    "new_targets_created_false",
    "target_values_created_false",
    "target_definition_change_performed_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
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
    "candidate_creation_rerun_false",
    "candidate_review_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowObjectiveLabelOrTargetGenerationApprovalError(ValueError):
    """Raised when approval evidence violates the approval-only boundary."""


def build_marketflow_objective_label_or_target_generation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_design_results_review_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_label_target_package: str,
    operator_confirms_selected_objective_path: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_generation_authorized_for_future_execution_only: bool,
    operator_confirms_generation_not_performed: bool,
    operator_confirms_no_label_values_created: bool,
    operator_confirms_no_target_values_created: bool,
    operator_confirms_no_new_targets_created: bool,
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
    selected_label_target_package: str = SELECTED_LABEL_TARGET_PACKAGE,
    selected_objective_path: str = SELECTED_OBJECTIVE_PATH,
    operator_decision: str = OPERATOR_DECISION_APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION,
) -> dict:
    """Build the complete non-secret operator attestation object."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_V1
        )
    }


@lru_cache(maxsize=1)
def _canonical_source_review() -> dict:
    return review_service.build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1()


def _source_review(source_review: dict | None) -> dict:
    source = (
        deepcopy(_canonical_source_review())
        if source_review is None
        else deepcopy(source_review)
    )
    validation = review_service.validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        source
    )
    if (
        validation[
            "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
        ]
        != EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "source candidate review digest mismatch"
        )
    return source


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "operator_attestation missing"
        )
    source = _canonical_source_review()
    evidence = SOURCE_EVIDENCE_DIGESTS
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_V1,
        "operator_confirms_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_design_results_review_digest": evidence[
            "source_expectancy_objective_design_results_review_digest"
        ],
        "operator_confirms_records_digest": source["records_digest"],
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "operator_confirms_selected_objective_path": SELECTED_OBJECTIVE_PATH,
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
                f"{field} mismatch"
            )
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
                f"{field} must be true"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
                f"{field} required"
            )


def _approved_selected_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = {
        row["label_target_family_id"]: row
        for row in source["reviewed_label_target_families"]
    }
    return [
        {
            "label_target_family_id": family_id,
            "approval_status": "APPROVED_FOR_FUTURE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY",
            "candidate_status": source_rows[family_id]["candidate_status"],
            "generation_performed": False,
            "target_values_created": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "backtest_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in review_service.candidate_service.RECOMMENDED_PACKAGE_FAMILIES
    ]


def _supporting_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "label_target_family_id": family_id,
            "approval_status": "AVAILABLE_NOT_SELECTED",
            "generation_performed": False,
            "target_values_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family_id in review_service.candidate_service.SUPPORTING_PACKAGE_FAMILIES
    ]


def _approved_formula_dimensions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "formula_dimension_id": row["formula_dimension_id"],
            "approval_status": "APPROVED_FOR_FUTURE_FORMULA_EXECUTION_PLANNING_ONLY",
            "formula_status": row["formula_status"],
            "generation_performed": False,
            "metric_computation_authorized": False,
        }
        for row in source["reviewed_formula_dimensions"]
    ]


def _approved_availability_rules(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "rule_id": row["rule_id"],
            "approval_status": "APPROVED_FOR_FUTURE_GENERATION_EXECUTION_CONTROL",
            "rule_status": row["rule_status"],
        }
        for row in source["reviewed_availability_no_peek_rules"]
    ]


def _approved_quality_checks(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "quality_check_id": row["quality_check_id"],
            "approval_status": "APPROVED_FOR_FUTURE_GENERATION_QUALITY_CONTROL",
            "quality_check_status": row["quality_check_status"],
        }
        for row in source["reviewed_quality_checks"]
    ]


def _approved_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "future_output_id": row["future_output_id"],
            "approval_status": "AUTHORIZED_NOT_GENERATED",
            "output_status": row["output_status"],
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_future_outputs"]
    ]


def per_ticker_objective_label_or_target_generation_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker approval entry."""
    payload = deepcopy(dict(entry))
    payload.pop(
        "per_ticker_objective_label_or_target_generation_approval_digest", None
    )
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source[
        "per_ticker_objective_label_or_target_generation_candidate_review_entries"
    ]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": is_meta,
            "objective_label_or_target_generation_candidate_review_status": source[
                "review_status"
            ],
            "objective_label_or_target_generation_approval_status": "APPROVED_FOR_FUTURE_LABEL_OR_TARGET_GENERATION_EXECUTION_ONLY",
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
            "objective_label_or_target_generation_selected": True,
            "objective_label_or_target_generation_approved": True,
            "objective_label_or_target_generation_authorized": True,
            "objective_label_or_target_generation_performed": False,
            "label_generation_performed": False,
            "new_targets_created": False,
            "target_values_created": False,
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
            "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
            "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_design_results_review_digest": SOURCE_EVIDENCE_DIGESTS[
                "source_expectancy_objective_design_results_review_digest"
            ],
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_objective_label_or_target_generation_approval_digest"
        ] = per_ticker_objective_label_or_target_generation_approval_digest_v1(entry)
        entries.append(entry)
    return entries


def _source_digest_chain(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: deepcopy(value)
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str)
    }


def _base_approval(
    source: Mapping[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    evidence = SOURCE_EVIDENCE_DIGESTS
    approval = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_V1,
        "approval_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED,
        "approval_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "created_offline": True,
        "research_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_objective_label_or_target_generation_candidate_review_artifact_kind": source[
            "artifact_kind"
        ],
        "source_objective_label_or_target_generation_candidate_review_status": source[
            "review_status"
        ],
        "source_objective_label_or_target_generation_candidate_review_scope": source[
            "review_scope"
        ],
        "source_objective_label_or_target_generation_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_objective_label_or_target_generation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_design_results_review_digest": evidence[
            "source_expectancy_objective_design_results_review_digest"
        ],
        "source_design_execution_digest": evidence[
            "source_expectancy_objective_design_execution_digest"
        ],
        "source_design_output_binding_digest": evidence[
            "source_expectancy_objective_design_output_binding_digest"
        ],
        "source_expectancy_objective_approval_digest": evidence[
            "source_expectancy_objective_approval_digest"
        ],
        **_source_digest_chain(source),
        "objective_label_or_target_generation_candidate_created": True,
        "objective_label_or_target_generation_candidate_review_created": True,
        "objective_label_or_target_generation_candidate_review_ready": True,
        "objective_label_or_target_generation_selected": True,
        "objective_label_or_target_generation_approved": True,
        "objective_label_or_target_generation_authorized": True,
        "objective_label_or_target_generation_approval_created": True,
        "ready_for_objective_label_or_target_generation_execution": True,
        "approved_primary_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "supporting_label_target_package_status": "AVAILABLE_NOT_SELECTED",
        "label_or_target_generation_authorized_for_future_execution": True,
        "objective_label_or_target_generation_performed": False,
        "label_generation_performed": False,
        "target_generation_performed": False,
        "new_targets_created": False,
        "target_values_created": False,
        "target_definition_change_performed": False,
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
        "candidate_creation_rerun_performed": False,
        "candidate_review_rerun_performed": False,
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
    ]
    approval.update({field: deepcopy(source[field]) for field in copied_fields})
    approval.update(
        {
            "selected_label_target_families": _approved_selected_families(source),
            "supporting_label_target_families": _supporting_families(source),
            "approved_formula_dimensions": _approved_formula_dimensions(source),
            "approved_availability_no_peek_rules": _approved_availability_rules(
                source
            ),
            "approved_quality_checks": _approved_quality_checks(source),
            "approved_future_outputs": _approved_future_outputs(source),
            "per_ticker_objective_label_or_target_generation_approval_entries": _per_ticker_entries(
                source
            ),
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
        isinstance(entry, Mapping)
        and entry.get(
            "per_ticker_objective_label_or_target_generation_approval_digest"
        )
        == per_ticker_objective_label_or_target_generation_approval_digest_v1(entry)
        for entry in entries
    )


def _approved_future_outputs_valid(rows: Any) -> bool:
    return isinstance(rows, list) and len(rows) == 11 and all(
        isinstance(row, Mapping)
        and row.get("approval_status") == "AUTHORIZED_NOT_GENERATED"
        and row.get("output_status") == "PLANNED_NOT_GENERATED"
        and row.get("generated") is False
        for row in rows
    )


def _check_definitions(approval: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = _canonical_source_review()
    expected = _base_approval(source, approval.get("operator_attestation", {}))
    evidence = SOURCE_EVIDENCE_DIGESTS
    operator = approval.get("operator_attestation", {})
    entries = approval.get(
        "per_ticker_objective_label_or_target_generation_approval_entries", []
    )
    definitions = [
        ("source_candidate_review_digest_bound", EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST, approval.get("source_objective_label_or_target_generation_candidate_review_digest")),
        ("source_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, approval.get("source_objective_label_or_target_generation_candidate_digest")),
        ("source_design_results_review_digest_bound", evidence["source_expectancy_objective_design_results_review_digest"], approval.get("source_design_results_review_digest")),
        ("source_design_execution_digest_bound", evidence["source_expectancy_objective_design_execution_digest"], approval.get("source_design_execution_digest")),
        ("source_design_output_binding_digest_bound", evidence["source_expectancy_objective_design_output_binding_digest"], approval.get("source_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", evidence["source_expectancy_objective_approval_digest"], approval.get("source_expectancy_objective_approval_digest")),
        ("source_expectancy_objective_candidate_digest_bound", evidence["source_expectancy_objective_candidate_digest"], approval.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", evidence["source_strategy_charter_approval_digest"], approval.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", evidence["source_strategy_charter_digest"], approval.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", evidence["source_final_archive_digest"], approval.get("source_final_archive_digest")),
        ("source_archive_digest_bound", evidence["source_archive_digest"], approval.get("source_archive_digest")),
        ("source_selection_digest_bound", evidence["source_selection_digest"], approval.get("source_selection_digest")),
        ("source_closure_digest_bound", evidence["source_closure_digest"], approval.get("source_closure_digest")),
        ("source_readiness_digest_bound", evidence["source_readiness_digest"], approval.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", evidence["source_reassessment_digest"], approval.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", evidence["source_results_review_digest"], approval.get("source_results_review_digest")),
        ("source_execution_digest_bound", evidence["source_execution_digest"], approval.get("source_execution_digest")),
        ("matrix_digest_bound", evidence["feature_label_matrix_digest"], approval.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", evidence["feature_values_digest"], approval.get("feature_values_digest")),
        ("label_values_digest_bound", evidence["redesigned_label_values_digest"], approval.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", evidence["research_registry_approval_digest"], approval.get("research_registry_approval_digest")),
        ("records_digest_bound", evidence["records_digest"], approval.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, approval.get("target_universe")),
        ("records_digest_preserved", evidence["records_digest"], approval.get("records_digest")),
        ("meta_913_preserved", 913, approval.get("meta_record_count")),
        ("operator_decision_matches", OPERATOR_DECISION_APPROVE_OBJECTIVE_LABEL_OR_TARGET_GENERATION, operator.get("operator_decision")),
        ("operator_attestation_phrase_matches", REQUIRED_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        ("approval_scope_only", OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_ONLY, approval.get("approval_scope")),
        ("selected_package_expectancy_payoff_abstention", SELECTED_LABEL_TARGET_PACKAGE, approval.get("selected_label_target_package")),
        ("selected_objective_path_preserved", SELECTED_OBJECTIVE_PATH, approval.get("selected_objective_path")),
        ("generation_authorized_for_future_execution_true", True, approval.get("label_or_target_generation_authorized_for_future_execution")),
        ("generation_performed_false", False, approval.get("objective_label_or_target_generation_performed")),
        ("approval_created_true", True, approval.get("objective_label_or_target_generation_approval_created")),
        ("ready_for_generation_execution_true", True, approval.get("ready_for_objective_label_or_target_generation_execution")),
        ("selected_label_target_families_5", expected["selected_label_target_families"], approval.get("selected_label_target_families")),
        ("supporting_label_target_families_available_not_selected", expected["supporting_label_target_families"], approval.get("supporting_label_target_families")),
        ("formula_dimensions_approved_14", expected["approved_formula_dimensions"], approval.get("approved_formula_dimensions")),
        ("availability_rules_approved_10", expected["approved_availability_no_peek_rules"], approval.get("approved_availability_no_peek_rules")),
        ("quality_checks_approved_10", expected["approved_quality_checks"], approval.get("approved_quality_checks")),
        ("future_outputs_authorized_not_generated_11", True, _approved_future_outputs_valid(approval.get("approved_future_outputs"))),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("label_generation_performed_false", False, approval.get("label_generation_performed")),
        ("target_generation_performed_false", False, approval.get("target_generation_performed")),
        ("new_targets_created_false", False, approval.get("new_targets_created")),
        ("target_values_created_false", False, approval.get("target_values_created")),
        ("target_definition_change_performed_false", False, approval.get("target_definition_change_performed")),
        ("feature_generation_authorized_false", False, approval.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, approval.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, approval.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, approval.get("backtest_execution_authorized")),
        ("backtest_execution_performed_false", False, approval.get("backtest_execution_performed")),
        ("model_training_authorized_false", False, approval.get("model_training_authorized")),
        ("model_training_performed_false", False, approval.get("model_training_performed")),
        ("metric_computation_authorized_false", False, approval.get("metric_computation_authorized")),
        ("metric_computation_performed_false", False, approval.get("metric_computation_performed")),
        ("strategy_scoring_false", False, approval.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, approval.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, approval.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, approval.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, approval.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, approval.get("broker_execution")),
        ("trade_recommendations_false", False, approval.get("trade_recommendations_generated")),
        ("provider_requests_made_false", False, approval.get("provider_requests_made_in_approval")),
        ("market_data_acquisition_false", False, approval.get("market_data_acquisition_performed_in_approval")),
        ("dataset_regeneration_false", False, approval.get("canonical_dataset_regenerated_in_approval")),
        ("candidate_creation_rerun_false", False, approval.get("candidate_creation_rerun_performed")),
        ("candidate_review_rerun_false", False, approval.get("candidate_review_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, approval.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, approval.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, approval.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, approval.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, approval.get("risk_controls")),
        ("no_tracked_marketflow_files", True, approval.get("no_tracked_marketflow_files")),
    ]
    if [definition[0] for definition in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "internal checklist definition mismatch"
        )
    return definitions


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(*definition) for definition in _check_definitions(approval)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "objective_label_or_target_generation_selected": True,
        "objective_label_or_target_generation_approved": True,
        "objective_label_or_target_generation_authorized": True,
        "ready_for_objective_label_or_target_generation_execution": True,
        "selected_label_target_package": SELECTED_LABEL_TARGET_PACKAGE,
        "label_or_target_generation_authorized_for_future_execution": True,
        "objective_label_or_target_generation_performed": False,
        "label_generation_performed": False,
        "target_generation_performed": False,
        "new_targets_created": False,
        "target_values_created": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(approval))
    payload.pop("approval_checklist", None)
    payload.pop("approval_summary", None)
    payload.pop("marketflow_objective_label_or_target_generation_approval_digest", None)
    return payload


def marketflow_objective_label_or_target_generation_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    return semantic_digest(_digest_payload(approval))


def build_marketflow_objective_label_or_target_generation_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict
) -> dict:
    """Build approval for future label or target generation execution only."""
    source = _source_review(source_review)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    checklist = _checklist(approval)
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = _summary(checklist)
    approval["marketflow_objective_label_or_target_generation_approval_digest"] = (
        marketflow_objective_label_or_target_generation_approval_digest_v1(approval)
    )
    validate_marketflow_objective_label_or_target_generation_approval_v1(approval)
    return approval


def validate_marketflow_objective_label_or_target_generation_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, evidence, approved catalogs, and closed authorities."""
    if not isinstance(approval, dict):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "approval must be a JSON object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(_source_review(None), attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
                f"{field} mismatch"
            )
    expected_checklist = _checklist(approval)
    if approval.get("approval_checklist") != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "approval checklist mismatch"
        )
    if approval.get("approval_summary") != _summary(expected_checklist):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get(
        "marketflow_objective_label_or_target_generation_approval_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "approval digest missing"
        )
    if digest != marketflow_objective_label_or_target_generation_approval_digest_v1(
        approval
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "approval digest mismatch"
        )
    return {
        "status": "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "selected_label_target_package": approval["selected_label_target_package"],
        "selected_objective_path": approval["selected_objective_path"],
        "marketflow_objective_label_or_target_generation_approval_digest": digest,
        **{
            key: approval["approval_summary"][key]
            for key in (
                "total_checks",
                "passed_checks",
                "failed_checks",
                "blocker_count",
            )
        },
    }


def build_marketflow_objective_label_or_target_generation_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval artifact."""
    validation = validate_marketflow_objective_label_or_target_generation_approval_v1(
        approval
    )
    operator = approval["operator_attestation"]
    sections = [
        ("Title", ["Objective Label or Target Generation Approval v1"]),
        ("Objective Label or Target Generation Approval v1", [f"Artifact/status/scope: {approval['artifact_kind']} / {approval['approval_status']} / {approval['approval_scope']}.", f"Approval digest: {validation['marketflow_objective_label_or_target_generation_approval_digest']}." ]),
        ("Operator Attestation", [f"Decision/reference/timestamp: {operator['operator_decision']} / {operator['operator_reference']} / {operator['operator_attestation_timestamp_utc']}.", f"Exact phrase: {operator['operator_attestation_phrase']}." ]),
        ("Source Candidate Review", [f"Artifact/status/scope: {approval['source_objective_label_or_target_generation_candidate_review_artifact_kind']} / {approval['source_objective_label_or_target_generation_candidate_review_status']} / {approval['source_objective_label_or_target_generation_candidate_review_scope']}.", f"Digest: {approval['source_objective_label_or_target_generation_candidate_review_digest']}." ]),
        ("Bound Evidence", [f"Candidate/design review/execution: {approval['source_objective_label_or_target_generation_candidate_digest']} / {approval['source_design_results_review_digest']} / {approval['source_design_execution_digest']}.", f"Matrix/features/labels/records: {approval['feature_label_matrix_digest']} / {approval['feature_values_digest']} / {approval['redesigned_label_values_digest']} / {approval['records_digest']}." ]),
        ("Dataset and Universe", [f"{approval['dataset_name']} / {approval['total_canonical_record_count']} records.", "Universe: " + ", ".join(approval["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Approval Scope", ["Approval authorizes only future label or target generation execution.", "No generation is performed by this artifact."]),
        ("Selected Label/Target Package", [f"{approval['selected_label_target_package']} is selected for future generation execution only."]),
        ("Selected Objective Path", [approval["selected_objective_path"]]),
        ("Selected Label/Target Families", [f"{row['label_target_family_id']}: {row['approval_status']}." for row in approval["selected_label_target_families"]]),
        ("Supporting Label/Target Families", [f"{row['label_target_family_id']}: {row['approval_status']}." for row in approval["supporting_label_target_families"]]),
        ("Approved Formula Dimensions", [f"{row['formula_dimension_id']}: {row['approval_status']}." for row in approval["approved_formula_dimensions"]]),
        ("Approved Availability and No-Peek Rules", [f"{row['rule_id']}: {row['approval_status']}." for row in approval["approved_availability_no_peek_rules"]]),
        ("Approved Quality Checks", [f"{row['quality_check_id']}: {row['approval_status']}." for row in approval["approved_quality_checks"]]),
        ("Approved Future Outputs", [f"{row['future_output_id']}: {row['approval_status']}." for row in approval["approved_future_outputs"]]),
        ("Per-Ticker Approval Summary", [f"{row['ticker']}: {row['objective_label_or_target_generation_approval_status']}, records {row['historical_record_count']}, digest {row['per_ticker_objective_label_or_target_generation_approval_digest']}." for row in approval["per_ticker_objective_label_or_target_generation_approval_entries"]]),
        ("Next Chain", approval["next_chain"]),
        ("Next Gates", approval["next_gates"]),
        ("Risk Controls", approval["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {approval['approval_summary']['total_checks']} / {approval['approval_summary']['passed_checks']} / {approval['approval_summary']['failed_checks']} / {approval['approval_summary']['blocker_count']}."]),
        ("Guardrails", ["This approval authorizes future generation execution only. It creates no label values, target values, new targets, features, matrix rows, backtests, models, metrics, scoring, recommendations, acceptance, profitability, runtime, provider, market-data, paper-trading, or broker authority."]),
    ]
    lines = ["# Objective Label or Target Generation Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_objective_label_or_target_generation_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON once in an explicitly supplied directory."""
    approval = build_marketflow_objective_label_or_target_generation_approval_v1(
        source_review=source_review, operator_attestation=operator_attestation
    )
    validation = validate_marketflow_objective_label_or_target_generation_approval_v1(
        approval
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_objective_label_or_target_generation_approval_v1.json"
    payload = canonical_json_bytes(approval)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowObjectiveLabelOrTargetGenerationApprovalError(
            "objective label or target generation approval output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "selected_label_target_package": approval["selected_label_target_package"],
        "selected_objective_path": approval["selected_objective_path"],
        "marketflow_objective_label_or_target_generation_approval_digest": validation[
            "marketflow_objective_label_or_target_generation_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
