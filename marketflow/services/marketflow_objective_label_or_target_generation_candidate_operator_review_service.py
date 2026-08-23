"""Offline operator review of the objective label or target generation candidate."""

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
    marketflow_objective_label_or_target_generation_candidate_service as candidate_service,
)


ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE"
)
SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_V1 = (
    "marketflow_objective_label_or_target_generation_candidate_operator_review_v1"
)
MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY"
)
OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL = (
    "OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL"
)

EXPECTED_SOURCE_CANDIDATE_DIGEST = (
    "26f26f739a8161633beb27e7993cd1af445a070978fbc61699c2df68adcdfff9"
)
SELECTED_OBJECTIVE_PATH = candidate_service.SELECTED_OBJECTIVE_PATH
RECOMMENDED_PACKAGE_ID = candidate_service.RECOMMENDED_PACKAGE_ID
SUPPORTING_PACKAGE_ID = candidate_service.SUPPORTING_PACKAGE_ID
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
SOURCE_EVIDENCE_DIGESTS = dict(candidate_service.SOURCE_EVIDENCE_DIGESTS)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

NEXT_CHAIN = [
    "Objective Label or Target Generation Approval v1, if selected.",
    "Objective Label or Target Generation Execution v1, if approved.",
    "Objective Label or Target Generation Results Review v1.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "objective_label_or_target_generation_approval_if_selected",
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
    "review_does_not_select_package",
    "review_does_not_approve_generation",
    "review_does_not_generate_labels",
    "review_does_not_create_targets",
    "review_does_not_create_target_values",
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
    "review_does_not_rerun_candidate_creation",
    "review_does_not_rerun_design_results_review",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_candidate_digest_bound",
    "source_design_results_review_digest_bound",
    "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_candidate_review_digest_bound",
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
    "source_candidate_status_ready",
    "source_candidate_scope_preserved",
    "review_created_true",
    "review_ready_true",
    "ready_for_approval_false",
    "candidate_philosophy_reviewed",
    "label_target_families_reviewed_10",
    "recommended_package_reviewed_not_selected",
    "supporting_package_reviewed_not_selected",
    "formula_dimensions_reviewed_14",
    "availability_rules_reviewed_10",
    "quality_checks_reviewed_10",
    "future_outputs_reviewed_not_generated",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "selection_created_false",
    "approval_created_false",
    "generation_created_false",
    "objective_label_or_target_generation_selected_false",
    "objective_label_or_target_generation_approved_false",
    "objective_label_or_target_generation_authorized_false",
    "objective_label_or_target_generation_performed_false",
    "label_generation_authorized_false",
    "label_generation_performed_false",
    "new_targets_created_false",
    "target_values_created_false",
    "target_definition_change_authorized_false",
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
    "design_results_review_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
    ValueError
):
    """Raised when the operator review violates its review-only boundary."""


def _source_candidate(candidate: dict | None) -> dict:
    source = (
        candidate_service.build_marketflow_objective_label_or_target_generation_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    validation = candidate_service.validate_marketflow_objective_label_or_target_generation_candidate_v1(
        source
    )
    if (
        validation[
            "marketflow_objective_label_or_target_generation_candidate_v1_digest"
        ]
        != EXPECTED_SOURCE_CANDIDATE_DIGEST
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "source objective label or target generation candidate digest mismatch"
        )
    return source


def _reviewed_candidate_basis(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "selected_objective_path": source["selected_objective_path"],
        "source_reviewed_design_components": deepcopy(source["candidate_basis"]),
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


def _reviewed_families(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_LABEL_OR_TARGET_CANDIDATE_NOT_GENERATED",
            "approval_status": "NOT_APPROVED_BY_THIS_REVIEW",
        }
        for row in source["proposed_label_target_families"]
    ]


def _reviewed_package(
    source_package: Mapping[str, Any], *, review_status: str
) -> dict[str, Any]:
    return {
        "package_id": source_package["package_id"],
        "source_status": source_package["status"],
        "review_status": review_status,
        "includes": deepcopy(source_package["includes"]),
        "rationale": source_package["rationale"],
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _reviewed_formula_dimensions(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_CANDIDATE_FORMULA_NOT_COMPUTED",
        }
        for row in source["formula_candidate_dimensions"]
    ]


def _reviewed_availability_rules(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **deepcopy(row),
            "review_status": "REVIEWED_PLANNED_RULE_NOT_EXECUTED",
        }
        for row in source["availability_no_peek_rules"]
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


def per_ticker_objective_label_or_target_generation_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    payload = deepcopy(dict(entry))
    payload.pop(
        "per_ticker_objective_label_or_target_generation_candidate_review_digest",
        None,
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
            "objective_label_or_target_generation_candidate_status": source[
                "candidate_status"
            ],
            "objective_label_or_target_generation_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "selected_objective_path": source["selected_objective_path"],
            "recommended_label_target_package": RECOMMENDED_PACKAGE_ID,
            "objective_label_or_target_generation_selected": False,
            "objective_label_or_target_generation_approved": False,
            "objective_label_or_target_generation_authorized": False,
            "objective_label_or_target_generation_performed": False,
            "label_generation_authorized": False,
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
            "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
            "source_design_results_review_digest": SOURCE_EVIDENCE_DIGESTS[
                "source_expectancy_objective_design_results_review_digest"
            ],
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_REVIEW"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_objective_label_or_target_generation_candidate_review_digest"
        ] = per_ticker_objective_label_or_target_generation_candidate_review_digest_v1(
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
    evidence = SOURCE_EVIDENCE_DIGESTS
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_V1,
        "review_status": MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_PACKAGE_READY,
        "review_scope": OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_objective_label_or_target_generation_candidate_artifact_kind": source[
            "artifact_kind"
        ],
        "source_objective_label_or_target_generation_candidate_status": source[
            "candidate_status"
        ],
        "source_objective_label_or_target_generation_candidate_scope": source[
            "candidate_scope"
        ],
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
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "objective_label_or_target_generation_candidate_created": True,
        "objective_label_or_target_generation_candidate_ready_for_operator_review": True,
        "objective_label_or_target_generation_candidate_review_created": True,
        "objective_label_or_target_generation_candidate_review_ready": True,
        "ready_for_objective_label_or_target_generation_approval": False,
        "objective_label_or_target_generation_selected": False,
        "objective_label_or_target_generation_approved": False,
        "objective_label_or_target_generation_authorized": False,
        "objective_label_or_target_generation_performed": False,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_values_created": False,
        "target_definition_change_authorized": False,
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
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "candidate_creation_rerun_performed": False,
        "design_results_review_rerun_performed": False,
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
        "candidate_philosophy",
        "candidate_primary_question",
        "candidate_secondary_question",
        "candidate_boundary",
    ]
    review.update({field: deepcopy(source[field]) for field in copied_fields})
    review.update(
        {
            "reviewed_candidate_basis": _reviewed_candidate_basis(source),
            "reviewed_candidate_philosophy": _reviewed_candidate_philosophy(source),
            "reviewed_label_target_families": _reviewed_families(source),
            "reviewed_recommended_label_target_package": _reviewed_package(
                source["recommended_label_target_package"],
                review_status="REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED",
            ),
            "reviewed_supporting_label_target_package": _reviewed_package(
                source["supporting_label_target_package"],
                review_status="REVIEWED_AVAILABLE_SUPPORTING_PACKAGE_NOT_SELECTED",
            ),
            "reviewed_formula_dimensions": _reviewed_formula_dimensions(source),
            "reviewed_availability_no_peek_rules": _reviewed_availability_rules(
                source
            ),
            "reviewed_quality_checks": _reviewed_quality_checks(source),
            "reviewed_future_outputs": _reviewed_future_outputs(source),
            "per_ticker_objective_label_or_target_generation_candidate_review_entries": _per_ticker_entries(
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
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(entry, Mapping)
        and entry.get(
            "per_ticker_objective_label_or_target_generation_candidate_review_digest"
        )
        == per_ticker_objective_label_or_target_generation_candidate_review_digest_v1(
            entry
        )
        for entry in entries
    )


def _reviewed_future_outputs_valid(rows: Any) -> bool:
    return isinstance(rows, list) and len(rows) == 11 and all(
        isinstance(row, Mapping)
        and row.get("review_status")
        == "REVIEWED_PLANNED_OUTPUT_NOT_GENERATED"
        and row.get("output_status") == "PLANNED_NOT_GENERATED"
        and row.get("generated") is False
        for row in rows
    )


def _check_definitions(review: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    source = candidate_service.build_marketflow_objective_label_or_target_generation_candidate_v1()
    expected = _base_review(source)
    evidence = SOURCE_EVIDENCE_DIGESTS
    entries = review.get(
        "per_ticker_objective_label_or_target_generation_candidate_review_entries",
        [],
    )
    definitions = [
        ("source_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_objective_label_or_target_generation_candidate_digest")),
        ("source_design_results_review_digest_bound", evidence["source_expectancy_objective_design_results_review_digest"], review.get("source_design_results_review_digest")),
        ("source_design_execution_digest_bound", evidence["source_expectancy_objective_design_execution_digest"], review.get("source_design_execution_digest")),
        ("source_design_output_binding_digest_bound", evidence["source_expectancy_objective_design_output_binding_digest"], review.get("source_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", evidence["source_expectancy_objective_approval_digest"], review.get("source_expectancy_objective_approval_digest")),
        ("source_candidate_review_digest_bound", evidence["source_expectancy_objective_candidate_review_digest"], review.get("source_expectancy_objective_candidate_review_digest")),
        ("source_expectancy_objective_candidate_digest_bound", evidence["source_expectancy_objective_candidate_digest"], review.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", evidence["source_strategy_charter_approval_digest"], review.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", evidence["source_strategy_charter_digest"], review.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", evidence["source_final_archive_digest"], review.get("source_final_archive_digest")),
        ("source_archive_digest_bound", evidence["source_archive_digest"], review.get("source_archive_digest")),
        ("source_selection_digest_bound", evidence["source_selection_digest"], review.get("source_selection_digest")),
        ("source_closure_digest_bound", evidence["source_closure_digest"], review.get("source_closure_digest")),
        ("source_readiness_digest_bound", evidence["source_readiness_digest"], review.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", evidence["source_reassessment_digest"], review.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", evidence["source_results_review_digest"], review.get("source_results_review_digest")),
        ("source_execution_digest_bound", evidence["source_execution_digest"], review.get("source_execution_digest")),
        ("matrix_digest_bound", evidence["feature_label_matrix_digest"], review.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", evidence["feature_values_digest"], review.get("feature_values_digest")),
        ("label_values_digest_bound", evidence["redesigned_label_values_digest"], review.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", evidence["research_registry_approval_digest"], review.get("research_registry_approval_digest")),
        ("records_digest_bound", evidence["records_digest"], review.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, review.get("target_universe")),
        ("records_digest_preserved", evidence["records_digest"], review.get("records_digest")),
        ("meta_913_preserved", 913, review.get("meta_record_count")),
        ("source_candidate_status_ready", candidate_service.MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW, review.get("source_objective_label_or_target_generation_candidate_status")),
        ("source_candidate_scope_preserved", candidate_service.OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION, review.get("source_objective_label_or_target_generation_candidate_scope")),
        ("review_created_true", True, review.get("objective_label_or_target_generation_candidate_review_created")),
        ("review_ready_true", True, review.get("objective_label_or_target_generation_candidate_review_ready")),
        ("ready_for_approval_false", False, review.get("ready_for_objective_label_or_target_generation_approval")),
        ("candidate_philosophy_reviewed", expected["reviewed_candidate_philosophy"], review.get("reviewed_candidate_philosophy")),
        ("label_target_families_reviewed_10", expected["reviewed_label_target_families"], review.get("reviewed_label_target_families")),
        ("recommended_package_reviewed_not_selected", expected["reviewed_recommended_label_target_package"], review.get("reviewed_recommended_label_target_package")),
        ("supporting_package_reviewed_not_selected", expected["reviewed_supporting_label_target_package"], review.get("reviewed_supporting_label_target_package")),
        ("formula_dimensions_reviewed_14", expected["reviewed_formula_dimensions"], review.get("reviewed_formula_dimensions")),
        ("availability_rules_reviewed_10", expected["reviewed_availability_no_peek_rules"], review.get("reviewed_availability_no_peek_rules")),
        ("quality_checks_reviewed_10", expected["reviewed_quality_checks"], review.get("reviewed_quality_checks")),
        ("future_outputs_reviewed_not_generated", True, _reviewed_future_outputs_valid(review.get("reviewed_future_outputs"))),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("selection_created_false", False, review.get("selection_created")),
        ("approval_created_false", False, review.get("approval_created")),
        ("generation_created_false", False, review.get("generation_created")),
        ("objective_label_or_target_generation_selected_false", False, review.get("objective_label_or_target_generation_selected")),
        ("objective_label_or_target_generation_approved_false", False, review.get("objective_label_or_target_generation_approved")),
        ("objective_label_or_target_generation_authorized_false", False, review.get("objective_label_or_target_generation_authorized")),
        ("objective_label_or_target_generation_performed_false", False, review.get("objective_label_or_target_generation_performed")),
        ("label_generation_authorized_false", False, review.get("label_generation_authorized")),
        ("label_generation_performed_false", False, review.get("label_generation_performed")),
        ("new_targets_created_false", False, review.get("new_targets_created")),
        ("target_values_created_false", False, review.get("target_values_created")),
        ("target_definition_change_authorized_false", False, review.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, review.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, review.get("feature_generation_performed")),
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
        ("candidate_creation_rerun_false", False, review.get("candidate_creation_rerun_performed")),
        ("design_results_review_rerun_false", False, review.get("design_results_review_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, review.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, review.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        ("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
    ]
    if [definition[0] for definition in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
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
        "objective_label_or_target_generation_candidate_review_created": not failed,
        "objective_label_or_target_generation_candidate_review_ready": not failed,
        "ready_for_objective_label_or_target_generation_approval": False,
        "recommended_label_target_package": RECOMMENDED_PACKAGE_ID,
        "selection_created": False,
        "approval_created": False,
        "generation_created": False,
        "label_generation_performed": False,
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


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("review_checklist", None)
    payload.pop("review_summary", None)
    payload.pop(
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        None,
    )
    return payload


def marketflow_objective_label_or_target_generation_candidate_operator_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(review))


def build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
    candidate: dict | None = None,
) -> dict:
    """Build the review package without selection, approval, or generation."""
    review = _base_review(_source_candidate(candidate))
    checklist = _checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    review[
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    ] = marketflow_objective_label_or_target_generation_candidate_operator_review_digest_v1(
        review
    )
    validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        review
    )
    return review


def validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
    review: dict,
) -> dict:
    """Validate exact evidence, reviewed content, and every closed authority."""
    if not isinstance(review, dict):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "review must be a JSON object"
        )
    expected = _base_review(_source_candidate(None))
    for field, value in expected.items():
        if review.get(field) != value:
            raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
                f"{field} mismatch"
            )
    expected_checklist = _checklist(review)
    if review.get("review_checklist") != expected_checklist or any(
        row.get("status") != PASS for row in expected_checklist
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "review checklist mismatch"
        )
    if review.get("review_summary") != _summary(expected_checklist):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "review summary mismatch"
        )
    digest = review.get(
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "review digest missing"
        )
    if digest != marketflow_objective_label_or_target_generation_candidate_operator_review_digest_v1(
        review
    ):
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "review digest mismatch"
        )
    return {
        "status": "MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_CANDIDATE_OPERATOR_REVIEW_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest": digest,
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


def build_marketflow_objective_label_or_target_generation_candidate_operator_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        review
    )
    sections = [
        ("Title", ["Objective Label or Target Generation Candidate Operator Review v1"]),
        ("Objective Label or Target Generation Candidate Operator Review v1", [f"Artifact/status/scope: {review['artifact_kind']} / {review['review_status']} / {review['review_scope']}.", f"Review digest: {validation['marketflow_objective_label_or_target_generation_candidate_operator_review_digest']}." ]),
        ("Source Candidate", [f"Artifact/status/scope: {review['source_objective_label_or_target_generation_candidate_artifact_kind']} / {review['source_objective_label_or_target_generation_candidate_status']} / {review['source_objective_label_or_target_generation_candidate_scope']}.", f"Candidate digest: {review['source_objective_label_or_target_generation_candidate_digest']}." ]),
        ("Bound Evidence", [f"Design review/execution/output binding: {review['source_design_results_review_digest']} / {review['source_design_execution_digest']} / {review['source_design_output_binding_digest']}.", f"Matrix/features/labels/records: {review['feature_label_matrix_digest']} / {review['feature_values_digest']} / {review['redesigned_label_values_digest']} / {review['records_digest']}." ]),
        ("Dataset and Universe", [f"{review['dataset_name']} / {review['total_canonical_record_count']} records.", "Universe: " + ", ".join(review["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Reviewed Candidate Basis", [f"{key}: {value}." for key, value in review["reviewed_candidate_basis"].items()]),
        ("Reviewed Candidate Philosophy", [review["candidate_philosophy"], review["candidate_primary_question"], review["candidate_secondary_question"], review["candidate_boundary"]]),
        ("Reviewed Label/Target Families", [f"{row['label_target_family_id']}: {row['review_status']}." for row in review["reviewed_label_target_families"]]),
        ("Reviewed Recommended Package", [f"{review['reviewed_recommended_label_target_package']['package_id']}: {review['reviewed_recommended_label_target_package']['review_status']}.", "No selection, approval, or generation is created."]),
        ("Reviewed Supporting Package", [f"{review['reviewed_supporting_label_target_package']['package_id']}: {review['reviewed_supporting_label_target_package']['review_status']}."]),
        ("Reviewed Formula Dimensions", [f"{row['formula_dimension_id']}: {row['review_status']}." for row in review["reviewed_formula_dimensions"]]),
        ("Reviewed Availability and No-Peek Rules", [f"{row['rule_id']}: {row['review_status']}." for row in review["reviewed_availability_no_peek_rules"]]),
        ("Reviewed Quality Checks", [f"{row['quality_check_id']}: {row['review_status']}." for row in review["reviewed_quality_checks"]]),
        ("Reviewed Future Outputs", [f"{row['future_output_id']}: {row['review_status']}." for row in review["reviewed_future_outputs"]]),
        ("Per-Ticker Review Summary", [f"{row['ticker']}: {row['objective_label_or_target_generation_candidate_review_status']}, records {row['historical_record_count']}, digest {row['per_ticker_objective_label_or_target_generation_candidate_review_digest']}." for row in review["per_ticker_objective_label_or_target_generation_candidate_review_entries"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {review['review_summary']['total_checks']} / {review['review_summary']['passed_checks']} / {review['review_summary']['failed_checks']} / {review['review_summary']['blocker_count']}."]),
        ("Guardrails", ["This review creates no selection, approval, labels, targets, target values, features, matrix rows, backtests, models, metrics, scoring, recommendations, acceptance, profitability, runtime, provider, market-data, paper-trading, or broker authority."]),
    ]
    lines = ["# Objective Label or Target Generation Candidate Operator Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON once in an explicitly supplied directory."""
    review = build_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        candidate
    )
    validation = validate_marketflow_objective_label_or_target_generation_candidate_operator_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = (
        directory
        / "marketflow_objective_label_or_target_generation_candidate_operator_review_v1.json"
    )
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowObjectiveLabelOrTargetGenerationCandidateOperatorReviewError(
            "objective label or target generation candidate operator review output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_objective_label_or_target_generation_candidate_operator_review_digest": validation[
            "marketflow_objective_label_or_target_generation_candidate_operator_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
