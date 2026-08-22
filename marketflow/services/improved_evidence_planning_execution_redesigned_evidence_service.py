"""Execute approved improved-evidence planning over frozen redesigned evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    improved_evidence_planning_approval_redesigned_evidence_service as approval,
)


ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE"
)
ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_BLOCKED_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_BLOCKED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_V1 = (
    "improved_evidence_planning_executed_using_redesigned_evidence_v1"
)
IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY = (
    "IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
)
IMPROVED_EVIDENCE_PLANNING_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)
IMPROVED_EVIDENCE_PLANNING_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID = (
    "IMPROVED_EVIDENCE_PLANNING_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_CANONICAL_ROOT = Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
DEFAULT_LABEL_ROOT = Path(".marketflow") / "redesigned_label_generation" / "expanded_universe_v1"
DEFAULT_FEATURE_ROOT = Path(".marketflow") / "feature_generation_using_redesigned_labels" / "expanded_universe_v1"
DEFAULT_PREDICTIVE_EVIDENCE_ROOT = Path(".marketflow") / "additional_predictive_evidence_using_redesigned_labels" / "expanded_universe_v1"
DEFAULT_LABEL_OBJECTIVE_REVIEW_ROOT = Path(".marketflow") / "label_objective_target_definition_review_using_redesigned_evidence" / "expanded_universe_v1"
DEFAULT_LABEL_OBJECTIVE_REDESIGN_ROOT = Path(".marketflow") / "label_objective_redesign_using_redesigned_evidence" / "expanded_universe_v1"
DEFAULT_OUTPUT_ROOT = Path(".marketflow") / "improved_evidence_planning_using_redesigned_evidence" / "expanded_universe_v1"
DEFAULT_BRANCH = "feature/improved-evidence-planning-execution-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "480f88c34fa0f5e3ef64f97c344c7c29a103bce5"

DATASET_NAME = "expanded_universe_canonical_dataset_v1"
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
SELF_REFERENCE_POLICY = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
SELECTED_DIRECTION = approval.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION
PLANNED_REQUIRES_RESULTS_REVIEW = "PLANNED_REQUIRES_RESULTS_REVIEW"
COMPLETED_RESEARCH_ONLY = "COMPLETED_RESEARCH_ONLY"
PLANNING_EXECUTION_SCOPE = "PLANNING_EXECUTION_ONLY_NOT_EVIDENCE_EXECUTION"
PLANNING_DECISION_RECOMMENDATION = (
    "NO_LABEL_GENERATION_FEATURE_GENERATION_MATRIX_CREATION_OR_PREDICTIVE_EXECUTION_"
    "AUTHORIZED_BY_THIS_EXECUTION"
)

EXPECTED_APPROVAL_DIGEST = "6aad4b27a57310b59c33e3ecfc93754df7da815c3ea15d8e686f8fe73abef664"
EXPECTED_CANDIDATE_REVIEW_DIGEST = approval.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_CANDIDATE_DIGEST = approval.EXPECTED_CANDIDATE_DIGEST
BOUND_DIGESTS = deepcopy(approval.BOUND_DIGESTS)
EXPECTED_RECORDS_DIGEST = BOUND_DIGESTS["records_digest"]
EXPECTED_LABEL_VALUES_DIGEST = BOUND_DIGESTS["redesigned_label_values_digest"]
EXPECTED_FEATURE_VALUES_DIGEST = BOUND_DIGESTS["feature_values_digest"]
EXPECTED_MATRIX_DIGEST = BOUND_DIGESTS["feature_label_matrix_digest"]
EXPECTED_REDESIGN_EXECUTION_DIGEST = BOUND_DIGESTS[
    "label_objective_redesign_execution_using_redesigned_evidence_digest"
]
EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST = BOUND_DIGESTS[
    "label_objective_redesign_output_binding_digest"
]
EXPECTED_REVIEW_EXECUTION_DIGEST = BOUND_DIGESTS[
    "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
]
EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST = BOUND_DIGESTS[
    "label_objective_target_definition_review_output_binding_digest"
]

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(approval.EXPECTED_RECORD_COUNTS)
CANDIDATE_SERVICE = approval.review_service.candidate_service
IMPROVED_EVIDENCE_THEME_IDS = list(CANDIDATE_SERVICE.IMPROVED_EVIDENCE_THEME_IDS)
PLANNED_EVIDENCE_COMPONENT_IDS = list(CANDIDATE_SERVICE.PLANNED_EVIDENCE_COMPONENT_IDS)
PLANNED_DATA_PRODUCT_IDS = list(approval.APPROVED_DATA_PRODUCT_IDS)
PLANNED_FUTURE_OUTPUT_IDS = list(CANDIDATE_SERVICE.PLANNED_FUTURE_OUTPUT_IDS)
CANDIDATE_BASIS = deepcopy(CANDIDATE_SERVICE.CANDIDATE_BASIS)

OUTPUT_FILENAMES = [
    "improved_evidence_planning_execution_manifest.json",
    "proposed_label_schema_report.json",
    "no_trade_abstain_coverage_report.json",
    "material_move_threshold_report.json",
    "horizon_specific_validation_report.json",
    "ticker_regime_split_validation_report.json",
    "feature_label_alignment_report.json",
    "chronological_split_embargo_report.json",
    "baseline_model_comparison_plan.json",
    "calibration_brier_plan.json",
    "leakage_no_peek_control_plan.json",
    "per_ticker_meta_reporting_plan.json",
    "operator_review_summary.json",
    "improved_evidence_planning_digest_manifest.json",
]

SOURCE_FILES = {
    "canonical_records": ("canonical", "canonical_dataset_records.jsonl"),
    "label_values": ("label", "redesigned_label_values.jsonl"),
    "label_family_coverage": ("label", "redesigned_label_family_coverage_report.json"),
    "label_availability": ("label", "redesigned_label_availability_report.json"),
    "per_ticker_label_summary": ("label", "per_ticker_redesigned_label_summary.json"),
    "feature_values": ("feature", "feature_values.jsonl"),
    "feature_label_matrix": ("predictive", "feature_label_matrix.jsonl"),
    "baseline_comparison": ("predictive", "baseline_model_comparison_results.json"),
    "metric_family_results": ("predictive", "metric_family_results.json"),
    "per_ticker_cross_sectional": ("predictive", "per_ticker_cross_sectional_review.json"),
    "review_execution_manifest": ("review", "label_objective_target_definition_review_execution_manifest.json"),
    "redesign_execution_manifest": ("redesign", "label_objective_redesign_execution_manifest.json"),
    "majority_structure_redesign": ("redesign", "flat_class_and_majority_structure_redesign_report.json"),
    "no_trade_abstain_objective": ("redesign", "no_trade_abstain_objective_report.json"),
    "material_move_target": ("redesign", "material_move_target_definition_report.json"),
    "horizon_specific_target": ("redesign", "horizon_specific_target_design_report.json"),
    "ticker_regime_split_target": ("redesign", "ticker_or_regime_split_target_report.json"),
    "risk_adjusted_target": ("redesign", "risk_adjusted_target_definition_report.json"),
    "label_family_impact": ("redesign", "label_family_impact_review_report.json"),
    "meta_target_limitation": ("redesign", "meta_target_limitation_review_report.json"),
    "acceptance_threshold": ("redesign", "acceptance_threshold_prerequisite_report.json"),
    "redesign_operator_summary": ("redesign", "operator_review_summary.json"),
    "redesign_digest_manifest": ("redesign", "label_objective_redesign_digest_manifest.json"),
}

TRUE_EXECUTION_FIELDS = [
    "created_offline",
    "research_only",
    "operator_review_required",
    "improved_evidence_planning_approved",
    "improved_evidence_planning_authorized",
    "ready_for_improved_evidence_planning_execution_using_redesigned_evidence",
    "improved_evidence_planning_executed",
    "improved_evidence_planning_results_created",
    "improved_evidence_planning_execution_manifest_created",
    "proposed_label_schema_report_created",
    "no_trade_abstain_coverage_report_created",
    "material_move_threshold_report_created",
    "horizon_specific_validation_report_created",
    "ticker_regime_split_validation_report_created",
    "feature_label_alignment_report_created",
    "chronological_split_embargo_report_created",
    "baseline_model_comparison_plan_created",
    "calibration_brier_plan_created",
    "leakage_no_peek_control_plan_created",
    "per_ticker_meta_reporting_plan_created",
    "operator_review_summary_created",
    "digest_manifest_created",
    "meta_reduced_record_count_preserved",
]

FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "redesigned_label_regeneration_performed",
    "feature_regeneration_performed",
    "predictive_evidence_execution_rerun_performed",
    "label_objective_target_definition_review_execution_rerun_performed",
    "label_objective_redesign_execution_rerun_performed",
    "metric_recomputation_performed_in_execution",
    "model_training_performed_in_execution",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "label_regeneration_authorized",
    "label_regeneration_performed",
    "new_targets_created",
    "target_definition_change_authorized",
    "target_definition_change_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
    "feature_label_matrix_created",
    "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_executed",
    "improved_evidence_planning_results_review_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
]


class ImprovedEvidencePlanningExecutionRedesignedEvidenceError(ValueError):
    """Raised when planning execution violates its research-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def _source_evidence() -> dict[str, str]:
    return {
        "improved_evidence_planning_approval_using_redesigned_evidence_digest": EXPECTED_APPROVAL_DIGEST,
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **deepcopy(BOUND_DIGESTS),
    }


def _output_manifest_binding_digest() -> str:
    return semantic_digest(
        {"filenames": OUTPUT_FILENAMES, "self_reference_policy": SELF_REFERENCE_POLICY}
    )


def improved_evidence_planning_execution_using_redesigned_evidence_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    """Return a path-independent semantic digest for a planning execution."""
    clone = deepcopy(dict(artifact))
    clone.pop("improved_evidence_planning_execution_using_redesigned_evidence_digest", None)
    clone.pop("source_roots", None)
    clone.pop("generated_output_root", None)
    return semantic_digest(clone)


def per_ticker_improved_evidence_planning_execution_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_improved_evidence_planning_execution_digest", None)
    return semantic_digest(clone)


def _verify_sources(
    roots: dict[str, Path],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    paths = {
        source_id: roots[root_key] / filename
        for source_id, (root_key, filename) in SOURCE_FILES.items()
    }
    for source_id, path in paths.items():
        if not path.is_file():
            failures.append(
                {
                    "failure_id": "missing_source_file",
                    "source_id": source_id,
                    "path": _path_text(path),
                }
            )
    if failures:
        return {"all_required_source_files_present": False}, {}, failures

    before_hashes = {source_id: sha256_file(path) for source_id, path in paths.items()}
    expected_hashes = {
        "canonical_records": EXPECTED_RECORDS_DIGEST,
        "label_values": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix": EXPECTED_MATRIX_DIGEST,
    }
    for source_id, expected in expected_hashes.items():
        if before_hashes[source_id] != expected:
            failures.append(
                {
                    "failure_id": "source_digest_mismatch",
                    "source_id": source_id,
                    "expected": expected,
                    "actual": before_hashes[source_id],
                }
            )

    reports: dict[str, dict[str, Any]] = {}
    for source_id, path in paths.items():
        if path.suffix != ".json":
            continue
        try:
            reports[source_id] = _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            failures.append(
                {
                    "failure_id": "invalid_source_json",
                    "source_id": source_id,
                    "message": str(exc),
                }
            )

    expected_reports = set(SOURCE_FILES) - {
        "canonical_records",
        "label_values",
        "feature_values",
        "feature_label_matrix",
    }
    if set(reports) != expected_reports:
        failures.append({"failure_id": "source_report_set_incomplete"})
    else:
        for source_id, report in reports.items():
            if report.get("dataset_name") != DATASET_NAME:
                failures.append(
                    {"failure_id": "dataset_name_mismatch", "source_id": source_id}
                )
            if report.get("records_digest") != EXPECTED_RECORDS_DIGEST:
                failures.append(
                    {
                        "failure_id": "records_digest_binding_mismatch",
                        "source_id": source_id,
                    }
                )

        redesign = reports["redesign_execution_manifest"]
        if (
            redesign.get(
                "label_objective_redesign_execution_using_redesigned_evidence_digest"
            )
            != EXPECTED_REDESIGN_EXECUTION_DIGEST
        ):
            failures.append({"failure_id": "redesign_execution_digest_mismatch"})
        if (
            redesign.get("output_digest_manifest_summary", {}).get("binding_digest")
            != EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST
        ):
            failures.append({"failure_id": "redesign_output_binding_digest_mismatch"})
        if redesign.get("selected_label_objective_redesign_direction") != SELECTED_DIRECTION:
            failures.append({"failure_id": "selected_direction_mismatch"})

        review = reports["review_execution_manifest"]
        if (
            review.get(
                "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
            )
            != EXPECTED_REVIEW_EXECUTION_DIGEST
        ):
            failures.append({"failure_id": "review_execution_digest_mismatch"})
        if (
            review.get("output_digest_manifest_summary", {}).get("binding_digest")
            != EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST
        ):
            failures.append({"failure_id": "review_output_binding_digest_mismatch"})

        label_rows = reports["per_ticker_label_summary"].get(
            "per_ticker_label_summary", []
        )
        tickers = [row.get("ticker") for row in label_rows if isinstance(row, dict)]
        counts = {
            row.get("ticker"): row.get("historical_record_count")
            for row in label_rows
            if isinstance(row, dict)
        }
        if tickers != TARGET_UNIVERSE:
            failures.append({"failure_id": "target_universe_mismatch"})
        if counts != EXPECTED_RECORD_COUNTS:
            failures.append(
                {"failure_id": "record_count_mismatch", "actual": counts}
            )

    after_hashes = {source_id: sha256_file(path) for source_id, path in paths.items()}
    unchanged = before_hashes == after_hashes
    if not unchanged:
        failures.append({"failure_id": "source_artifact_mutated"})
    verification = {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": not any(
            row["failure_id"] == "source_digest_mismatch" for row in failures
        ),
        "all_required_source_bindings_match": not failures,
        "source_files_unchanged": unchanged,
        "source_file_count": len(paths),
        "source_file_sha256": before_hashes,
        "verified_records_digest": before_hashes["canonical_records"],
        "verified_redesigned_label_values_digest": before_hashes["label_values"],
        "verified_feature_values_digest": before_hashes["feature_values"],
        "verified_feature_label_matrix_digest": before_hashes[
            "feature_label_matrix"
        ],
        "verified_redesign_execution_digest": reports.get(
            "redesign_execution_manifest", {}
        ).get("label_objective_redesign_execution_using_redesigned_evidence_digest"),
        "verified_redesign_output_binding_digest": reports.get(
            "redesign_execution_manifest", {}
        ).get("output_digest_manifest_summary", {}).get("binding_digest"),
        "verified_review_execution_digest": reports.get(
            "review_execution_manifest", {}
        ).get(
            "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
        ),
        "verified_review_output_binding_digest": reports.get(
            "review_execution_manifest", {}
        ).get("output_digest_manifest_summary", {}).get("binding_digest"),
    }
    return verification, reports, failures


def _planning_facts() -> dict[str, Any]:
    return {
        **deepcopy(CANDIDATE_BASIS),
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "meta_record_count": 913,
        "meta_reduced_record_count_preserved": True,
    }


def _classification() -> dict[str, Any]:
    return {
        "improved_evidence_planning_classification": COMPLETED_RESEARCH_ONLY,
        "planning_execution_scope": PLANNING_EXECUTION_SCOPE,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "label_schema_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "no_trade_abstain_coverage_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "material_move_threshold_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "horizon_specific_validation_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "ticker_regime_split_validation_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "feature_label_alignment_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "chronological_split_embargo_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "baseline_model_comparison_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "calibration_brier_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "leakage_no_peek_control_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "per_ticker_meta_reporting_plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "additional_predictive_evidence_candidate_status": (
            "NOT_CREATED_REQUIRES_PLANNING_RESULTS_REVIEW"
        ),
        "planning_decision_recommendation": PLANNING_DECISION_RECOMMENDATION,
    }


def _plan(
    plan_id: str,
    *,
    objective: str,
    source_facts: dict[str, Any],
    planned_steps: list[str],
    controls: list[str],
) -> dict[str, Any]:
    return {
        "plan_id": plan_id,
        "plan_status": PLANNED_REQUIRES_RESULTS_REVIEW,
        "objective": objective,
        "source_facts": deepcopy(source_facts),
        "planned_steps": list(planned_steps),
        "controls": list(controls),
        "execution_performed": False,
        "metric_computation_performed": False,
        "model_training_performed": False,
        "research_only": True,
        "non_actionable": True,
    }


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "improved_evidence_planning_execution_status": "EXECUTED_RESEARCH_ONLY",
            "improved_evidence_planning_results_status": "CREATED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "improved_evidence_planning_approved": True,
            "improved_evidence_planning_executed": True,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "additional_predictive_evidence_execution_candidate_created": False,
            "additional_predictive_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
            "source_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "execution_note": (
                "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_EXECUTION"
                if is_meta
                else "STANDARD_FROZEN_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_improved_evidence_planning_execution_digest"] = (
            per_ticker_improved_evidence_planning_execution_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _planning_results() -> dict[str, Any]:
    facts = _planning_facts()
    common_controls = [
        "planning_only_no_evidence_execution",
        "no_label_or_target_creation",
        "no_feature_or_matrix_generation",
        "results_review_required_before_any_follow_on_candidate",
    ]
    plans = {
        "proposed_label_schema_plan": _plan(
            "proposed_label_schema_plan",
            objective="Define a review structure for a possible no-trade/abstain label schema without creating labels or targets.",
            source_facts={
                "selected_direction": SELECTED_DIRECTION,
                "largest_aggregated_class": facts["largest_aggregated_class"],
                "redesign_decision_review": facts["redesign_decision_review"],
            },
            planned_steps=[
                "review_directional_and_abstain_semantics",
                "document_eligibility_and_abstention_questions",
                "define_schema_review_acceptance_questions",
            ],
            controls=common_controls,
        ),
        "no_trade_abstain_coverage_plan": _plan(
            "no_trade_abstain_coverage_plan",
            objective="Plan coverage and class-balance review for no-trade/abstain semantics.",
            source_facts={
                "flat_count": facts["largest_aggregated_class_count"],
                "no_trade_count": facts["no_trade_count"],
                "oos_evaluated_rows": facts["oos_evaluated_rows"],
            },
            planned_steps=[
                "review_coverage_by_ticker_and_horizon",
                "review_abstention_eligibility_without_relabeling",
                "document_class_balance_decision_questions",
            ],
            controls=common_controls,
        ),
        "material_move_threshold_plan": _plan(
            "material_move_threshold_plan",
            objective="Plan a future material-move threshold analysis without selecting or generating a target.",
            source_facts={
                "global_five_session_threshold": facts[
                    "global_five_session_threshold"
                ],
                "benchmark_relative_threshold": facts[
                    "benchmark_relative_threshold"
                ],
            },
            planned_steps=[
                "review_threshold_sensitivity_candidates",
                "compare_global_and_benchmark_relative_policy_questions",
                "require_results_review_before_threshold_selection",
            ],
            controls=common_controls,
        ),
        "horizon_specific_validation_plan": _plan(
            "horizon_specific_validation_plan",
            objective="Plan chronological validation of horizon-specific design candidates.",
            source_facts={"source_horizons_sessions": [5, 10, 20]},
            planned_steps=[
                "review_each_horizon_separately",
                "preserve_chronological_order_and_embargo",
                "report_coverage_stability_and_limitations",
            ],
            controls=common_controls,
        ),
        "ticker_regime_split_validation_plan": _plan(
            "ticker_regime_split_validation_plan",
            objective="Plan per-ticker and regime review without creating split targets.",
            source_facts={"target_universe": TARGET_UNIVERSE, "meta_record_count": 913},
            planned_steps=[
                "review_per_ticker_coverage",
                "define_regime_review_dimensions_without_target_creation",
                "preserve_meta_limitation_as_a_separate_reported_constraint",
            ],
            controls=common_controls,
        ),
        "feature_label_alignment_plan": _plan(
            "feature_label_alignment_plan",
            objective="Plan read-only feature/label alignment checks without generating features or matrix rows.",
            source_facts={
                "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
                "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
                "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
            },
            planned_steps=[
                "review_timestamp_and_identity_alignment",
                "review_missingness_and_horizon_compatibility",
                "require_no_peek_checks_before_any_future evidence execution".replace(" ", "_"),
            ],
            controls=common_controls,
        ),
        "chronological_split_embargo_plan": _plan(
            "chronological_split_embargo_plan",
            objective="Define a future chronological split and embargo review policy.",
            source_facts={
                "date_range_start": "2022-01-01",
                "date_range_end": "2025-12-31",
            },
            planned_steps=[
                "prohibit_random_time_shuffling",
                "define_embargo_selection_as_future_results_review_input",
                "separate_training_validation_and_oos_holdout_periods",
            ],
            controls=common_controls,
        ),
        "baseline_model_comparison_plan": _plan(
            "baseline_model_comparison_plan",
            objective="Plan majority/local/cross-sectional comparisons without recomputing metrics or training models.",
            source_facts={
                "majority_accuracy": facts["majority_accuracy"],
                "local_model_accuracy": facts["local_model_accuracy"],
                "cross_sectional_accuracy": facts["cross_sectional_accuracy"],
                "cross_sectional_delta_vs_majority": facts[
                    "cross_sectional_delta_vs_majority"
                ],
            },
            planned_steps=[
                "preserve_majority_baseline_comparison",
                "preserve_local_model_comparison",
                "preserve_cross_sectional_comparison",
                "require_materiality_review_before_acceptance_readiness",
            ],
            controls=common_controls,
        ),
        "calibration_brier_plan": _plan(
            "calibration_brier_plan",
            objective="Plan future calibration and Brier review without computing metrics now.",
            source_facts={"predictive_usefulness": NOT_ACCEPTED},
            planned_steps=[
                "define_probability_calibration_review",
                "define_brier_score_reporting_questions",
                "define_stability_review_by_ticker_and_horizon",
            ],
            controls=common_controls,
        ),
        "leakage_no_peek_control_plan": _plan(
            "leakage_no_peek_control_plan",
            objective="Define future leakage and no-peek controls for separately approved evidence execution.",
            source_facts={"records_digest": EXPECTED_RECORDS_DIGEST},
            planned_steps=[
                "freeze_features_before_label_horizon_outcomes",
                "enforce_chronological_training_boundaries",
                "verify_embargo_and_identity_isolation",
                "record_all_source_and_output_digests",
            ],
            controls=common_controls,
        ),
        "per_ticker_meta_reporting_plan": _plan(
            "per_ticker_meta_reporting_plan",
            objective="Plan exact-order per-ticker reporting with META's reduced record count explicit.",
            source_facts={
                "target_universe": TARGET_UNIVERSE,
                "record_counts": EXPECTED_RECORD_COUNTS,
            },
            planned_steps=[
                "report_all_tickers_in_frozen_order",
                "report_meta_913_without_repair_or_inference",
                "separate_aggregate_and_per_ticker_limitations",
            ],
            controls=common_controls,
        ),
    }
    return {
        "planning_facts": facts,
        "planning_execution_classification": _classification(),
        "improved_evidence_themes": [
            {
                "theme_id": theme_id,
                "planning_execution_status": "EXECUTED_RESEARCH_ONLY",
                "evidence_execution_performed": False,
                "research_only": True,
                "non_actionable": True,
            }
            for theme_id in IMPROVED_EVIDENCE_THEME_IDS
        ],
        "planned_evidence_components": [
            {
                "component_id": component_id,
                "planning_execution_status": "EXECUTED_RESEARCH_ONLY",
                "component_execution_performed": False,
                "research_only": True,
                "non_actionable": True,
            }
            for component_id in PLANNED_EVIDENCE_COMPONENT_IDS
        ],
        "planned_data_products": [
            {
                "data_product_id": product_id,
                "planning_output_status": "CREATED_RESEARCH_ONLY",
                "evidence_output_generated": False,
                "research_only": True,
                "non_actionable": True,
            }
            for product_id in PLANNED_DATA_PRODUCT_IDS
        ],
        "planned_future_outputs": [
            {
                "future_output_id": output_id,
                "future_output_status": "PLANNED_NOT_GENERATED",
                "research_only": True,
                "non_actionable": True,
            }
            for output_id in PLANNED_FUTURE_OUTPUT_IDS
        ],
        "per_ticker_execution_entries": _per_ticker_entries(),
        **plans,
    }


def _common_output_fields(run_timestamp_utc: str) -> dict[str, Any]:
    return {
        "run_timestamp_utc": run_timestamp_utc,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": DATASET_NAME,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "improved_evidence_planning_approved": True,
        "improved_evidence_planning_authorized": True,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": True,
        "improved_evidence_planning_executed": True,
        "improved_evidence_planning_results_created": True,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "research_only": True,
        "non_actionable": True,
    }


def _blocked_artifact(
    *,
    roots: dict[str, Path],
    output_root: Path,
    run_timestamp_utc: str,
    verification: dict[str, Any],
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_BLOCKED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": IMPROVED_EVIDENCE_PLANNING_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "run_timestamp_utc": run_timestamp_utc,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "generated_output_root": _path_text(output_root),
        "created_offline": True,
        "research_only": True,
        "source_verification": verification,
        "failure_count": len(failures),
        "failures": failures,
        "improved_evidence_planning_approved": True,
        "improved_evidence_planning_authorized": True,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": True,
        "improved_evidence_planning_executed": False,
        "improved_evidence_planning_results_created": False,
        "generated_output_count": 0,
        "improved_evidence_planning_execution_using_redesigned_evidence_digest": "NOT_CREATED",
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = "PASS" if expected == actual else "FAIL"
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": "BLOCKER",
        "message": f"{check_id} {'passed' if status == 'PASS' else 'failed'}",
    }


def _execution_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    values: list[tuple[str, Any, Any]] = [
        ("artifact_kind_exact", ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE, artifact.get("artifact_kind")),
        ("execution_status_exact", IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY, artifact.get("execution_status")),
        ("approval_digest_bound", EXPECTED_APPROVAL_DIGEST, artifact.get("source_evidence", {}).get("improved_evidence_planning_approval_using_redesigned_evidence_digest")),
        ("planning_approved_true", True, artifact.get("improved_evidence_planning_approved")),
        ("planning_authorized_true", True, artifact.get("improved_evidence_planning_authorized")),
        ("ready_for_execution_true", True, artifact.get("ready_for_improved_evidence_planning_execution_using_redesigned_evidence")),
        ("planning_executed_true", True, artifact.get("improved_evidence_planning_executed")),
        ("planning_results_created_true", True, artifact.get("improved_evidence_planning_results_created")),
        ("generated_output_count_14", 14, artifact.get("generated_output_count")),
        ("target_universe_preserved", TARGET_UNIVERSE, artifact.get("target_universe")),
        ("meta_913_preserved", 913, artifact.get("meta_record_count")),
        ("selected_direction_preserved", SELECTED_DIRECTION, artifact.get("selected_redesign_direction")),
        ("themes_11", 11, artifact.get("improved_evidence_theme_count")),
        ("components_13", 13, artifact.get("planned_evidence_component_count")),
        ("data_products_13", 13, artifact.get("planned_data_product_count")),
        ("future_outputs_12", 12, artifact.get("planned_future_output_count")),
        ("per_ticker_entries_12", 12, len(artifact.get("per_ticker_execution_entries", []))),
        ("label_regeneration_false", False, artifact.get("label_regeneration_performed")),
        ("new_targets_false", False, artifact.get("new_targets_created")),
        ("feature_generation_false", False, artifact.get("feature_generation_performed")),
        ("feature_label_matrix_false", False, artifact.get("feature_label_matrix_created")),
        ("predictive_candidate_false", False, artifact.get("additional_predictive_evidence_execution_candidate_created")),
        ("predictive_execution_false", False, artifact.get("additional_predictive_evidence_executed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, artifact.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, artifact.get("runtime_use")),
        ("trade_recommendations_false", False, artifact.get("trade_recommendations_generated")),
        ("provider_requests_false", False, artifact.get("provider_requests_made_in_execution")),
        ("dataset_regeneration_false", False, artifact.get("canonical_dataset_regenerated_in_execution")),
        ("metric_recomputation_false", False, artifact.get("metric_recomputation_performed_in_execution")),
        ("model_training_false", False, artifact.get("model_training_performed_in_execution")),
        ("source_files_unchanged", True, artifact.get("source_verification", {}).get("source_files_unchanged")),
    ]
    return [_check(*row) for row in values]


def _build_artifact(
    *,
    roots: dict[str, Path],
    output_root: Path,
    run_timestamp_utc: str,
    verification: dict[str, Any],
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "run_timestamp_utc": run_timestamp_utc,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "generated_output_root": _path_text(output_root),
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "source_evidence": _source_evidence(),
        "source_verification": verification,
        "dataset_name": DATASET_NAME,
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 14,
        "generated_output_names": OUTPUT_FILENAMES,
        "improved_evidence_theme_count": 11,
        "planned_evidence_component_count": 13,
        "planned_data_product_count": 13,
        "planned_future_output_count": 12,
        "output_digest_manifest_summary": {
            "filename": "improved_evidence_planning_digest_manifest.json",
            "entry_count": 14,
            "self_reference_policy": SELF_REFERENCE_POLICY,
            "binding_digest": _output_manifest_binding_digest(),
        },
        "failure_count": 0,
        "warning_count": 1,
        "warnings": ["META_PRESERVED_REDUCED_RECORD_COUNT_913"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        **{field: True for field in TRUE_EXECUTION_FIELDS},
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        **_planning_results(),
    }
    artifact["execution_checklist"] = _execution_checklist(artifact)
    failed = [row for row in artifact["execution_checklist"] if row["status"] != "PASS"]
    artifact["execution_checklist_summary"] = {
        "total_checks": len(artifact["execution_checklist"]),
        "passed_checks": len(artifact["execution_checklist"]) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
    }
    artifact["improved_evidence_planning_execution_using_redesigned_evidence_digest"] = (
        improved_evidence_planning_execution_using_redesigned_evidence_digest_v1(
            artifact
        )
    )
    return artifact


def _build_outputs(artifact: dict[str, Any]) -> dict[str, bytes]:
    common = _common_output_fields(artifact["run_timestamp_utc"])
    reports: dict[str, dict[str, Any]] = {
        "improved_evidence_planning_execution_manifest.json": deepcopy(artifact),
        "proposed_label_schema_report.json": {
            **common,
            "report_name": "proposed_label_schema_report",
            **deepcopy(artifact["proposed_label_schema_plan"]),
        },
        "no_trade_abstain_coverage_report.json": {
            **common,
            "report_name": "no_trade_abstain_coverage_report",
            **deepcopy(artifact["no_trade_abstain_coverage_plan"]),
        },
        "material_move_threshold_report.json": {
            **common,
            "report_name": "material_move_threshold_report",
            **deepcopy(artifact["material_move_threshold_plan"]),
        },
        "horizon_specific_validation_report.json": {
            **common,
            "report_name": "horizon_specific_validation_report",
            **deepcopy(artifact["horizon_specific_validation_plan"]),
        },
        "ticker_regime_split_validation_report.json": {
            **common,
            "report_name": "ticker_regime_split_validation_report",
            **deepcopy(artifact["ticker_regime_split_validation_plan"]),
        },
        "feature_label_alignment_report.json": {
            **common,
            "report_name": "feature_label_alignment_report",
            **deepcopy(artifact["feature_label_alignment_plan"]),
        },
        "chronological_split_embargo_report.json": {
            **common,
            "report_name": "chronological_split_embargo_report",
            **deepcopy(artifact["chronological_split_embargo_plan"]),
        },
        "baseline_model_comparison_plan.json": {
            **common,
            "report_name": "baseline_model_comparison_plan",
            **deepcopy(artifact["baseline_model_comparison_plan"]),
        },
        "calibration_brier_plan.json": {
            **common,
            "report_name": "calibration_brier_plan",
            **deepcopy(artifact["calibration_brier_plan"]),
        },
        "leakage_no_peek_control_plan.json": {
            **common,
            "report_name": "leakage_no_peek_control_plan",
            **deepcopy(artifact["leakage_no_peek_control_plan"]),
        },
        "per_ticker_meta_reporting_plan.json": {
            **common,
            "report_name": "per_ticker_meta_reporting_plan",
            **deepcopy(artifact["per_ticker_meta_reporting_plan"]),
            "per_ticker_execution_entries": deepcopy(
                artifact["per_ticker_execution_entries"]
            ),
        },
        "operator_review_summary.json": {
            **common,
            "report_name": "operator_review_summary",
            "execution_status": artifact["execution_status"],
            "execution_digest": artifact[
                "improved_evidence_planning_execution_using_redesigned_evidence_digest"
            ],
            "planning_execution_classification": deepcopy(
                artifact["planning_execution_classification"]
            ),
            "generated_output_count": 14,
            "next_task": "Optional Improved Evidence Planning Results Review Using Redesigned Evidence v1",
        },
    }
    payloads = {
        filename: canonical_json_bytes(payload) for filename, payload in reports.items()
    }
    entries = [
        (
            {
                "filename": filename,
                "digest_kind": SELF_REFERENCE_POLICY,
                "sha256": None,
            }
            if filename == "improved_evidence_planning_digest_manifest.json"
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": sha256_bytes(payloads[filename]),
            }
        )
        for filename in OUTPUT_FILENAMES
    ]
    manifest = {
        **common,
        "report_name": "improved_evidence_planning_digest_manifest",
        "generated_output_count": 14,
        "output_digest_entries": entries,
        "all_non_self_output_digests_present": True,
        "self_reference_policy": SELF_REFERENCE_POLICY,
        "output_manifest_binding_digest": _output_manifest_binding_digest(),
        "execution_digest": artifact[
            "improved_evidence_planning_execution_using_redesigned_evidence_digest"
        ],
    }
    payloads["improved_evidence_planning_digest_manifest.json"] = canonical_json_bytes(
        manifest
    )
    return payloads


def _write_outputs_once(output_root: Path, payloads: dict[str, bytes]) -> None:
    existing = [name for name in OUTPUT_FILENAMES if (output_root / name).exists()]
    if existing:
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            f"planning execution outputs already exist: {', '.join(existing)}"
        )
    output_root.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        try:
            with (output_root / filename).open("xb") as handle:
                handle.write(payloads[filename])
        except FileExistsError as exc:
            raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
                f"refusing to overwrite planning execution output: {filename}"
            ) from exc


def execute_improved_evidence_planning_using_redesigned_evidence_v1(
    *,
    canonical_root: str | Path | None = None,
    label_root: str | Path | None = None,
    feature_root: str | Path | None = None,
    predictive_evidence_root: str | Path | None = None,
    label_objective_review_root: str | Path | None = None,
    label_objective_redesign_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Verify frozen evidence and write 14 research-only planning outputs once."""
    roots = {
        "canonical": DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root),
        "label": DEFAULT_LABEL_ROOT if label_root is None else Path(label_root),
        "feature": DEFAULT_FEATURE_ROOT if feature_root is None else Path(feature_root),
        "predictive": DEFAULT_PREDICTIVE_EVIDENCE_ROOT if predictive_evidence_root is None else Path(predictive_evidence_root),
        "review": DEFAULT_LABEL_OBJECTIVE_REVIEW_ROOT if label_objective_review_root is None else Path(label_objective_review_root),
        "redesign": DEFAULT_LABEL_OBJECTIVE_REDESIGN_ROOT if label_objective_redesign_root is None else Path(label_objective_redesign_root),
    }
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, _reports, failures = _verify_sources(roots)
    if failures:
        return _blocked_artifact(
            roots=roots,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            verification=verification,
            failures=failures,
        )
    artifact = _build_artifact(
        roots=roots,
        output_root=output_path,
        run_timestamp_utc=timestamp,
        verification=verification,
    )
    validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
        artifact
    )
    _write_outputs_once(output_path, _build_outputs(artifact))
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate planning execution and every closed downstream boundary."""
    if not isinstance(artifact, dict):
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "artifact must be a JSON object"
        )
    expected = {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "source_evidence": _source_evidence(),
        "dataset_name": DATASET_NAME,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 14,
        "generated_output_names": OUTPUT_FILENAMES,
        "improved_evidence_theme_count": 11,
        "planned_evidence_component_count": 13,
        "planned_data_product_count": 13,
        "planned_future_output_count": 12,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, field)
    for field in TRUE_EXECUTION_FIELDS:
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)

    verification = artifact.get("source_verification")
    if not isinstance(verification, dict):
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "source verification missing"
        )
    for field in (
        "all_required_source_files_present",
        "all_required_source_digests_match",
        "all_required_source_bindings_match",
        "source_files_unchanged",
    ):
        _expect(verification.get(field), True, field)
    verified_digests = {
        "verified_records_digest": EXPECTED_RECORDS_DIGEST,
        "verified_redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "verified_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "verified_feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "verified_redesign_execution_digest": EXPECTED_REDESIGN_EXECUTION_DIGEST,
        "verified_redesign_output_binding_digest": EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST,
        "verified_review_execution_digest": EXPECTED_REVIEW_EXECUTION_DIGEST,
        "verified_review_output_binding_digest": EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST,
    }
    for field, expected_value in verified_digests.items():
        _expect(verification.get(field), expected_value, field)

    manifest = artifact.get("output_digest_manifest_summary")
    if not isinstance(manifest, dict):
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "output digest manifest missing"
        )
    _expect(manifest.get("entry_count"), 14, "output manifest entry count")
    _expect(
        manifest.get("self_reference_policy"),
        SELF_REFERENCE_POLICY,
        "self reference policy",
    )
    _expect(
        manifest.get("binding_digest"),
        _output_manifest_binding_digest(),
        "output manifest digest",
    )

    collections = (
        ("improved_evidence_themes", 11),
        ("planned_evidence_components", 13),
        ("planned_data_products", 13),
        ("planned_future_outputs", 12),
        ("per_ticker_execution_entries", 12),
    )
    for field, count in collections:
        value = artifact.get(field)
        if not isinstance(value, list) or len(value) != count:
            raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
                f"{field} mismatch"
            )
    for entry in artifact["per_ticker_execution_entries"]:
        digest = entry.get("per_ticker_improved_evidence_planning_execution_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
                "per-ticker execution digest missing"
            )
        _expect(
            digest,
            per_ticker_improved_evidence_planning_execution_digest_v1(entry),
            "per-ticker execution digest",
        )

    classification = artifact.get("planning_execution_classification", {})
    _expect(
        classification.get("improved_evidence_planning_classification"),
        COMPLETED_RESEARCH_ONLY,
        "planning classification",
    )
    _expect(
        classification.get("planning_execution_scope"),
        PLANNING_EXECUTION_SCOPE,
        "planning execution scope",
    )
    _expect(
        classification.get("planning_decision_recommendation"),
        PLANNING_DECISION_RECOMMENDATION,
        "planning decision recommendation",
    )
    for field, value in classification.items():
        if field.endswith("_plan_status"):
            _expect(value, PLANNED_REQUIRES_RESULTS_REVIEW, field)
    _expect(
        classification.get("additional_predictive_evidence_candidate_status"),
        "NOT_CREATED_REQUIRES_PLANNING_RESULTS_REVIEW",
        "additional predictive evidence candidate status",
    )

    checklist = artifact.get("execution_checklist")
    if not isinstance(checklist, list) or not checklist:
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "execution checklist missing"
        )
    if any(row.get("status") != "PASS" for row in checklist):
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "execution checklist must pass"
        )
    _expect(checklist, _execution_checklist(artifact), "execution checklist")
    _expect(artifact.get("failure_count"), 0, "failure_count")

    digest = artifact.get(
        "improved_evidence_planning_execution_using_redesigned_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ImprovedEvidencePlanningExecutionRedesignedEvidenceError(
            "execution digest missing"
        )
    _expect(
        digest,
        improved_evidence_planning_execution_using_redesigned_evidence_digest_v1(
            artifact
        ),
        "execution digest",
    )
    return {
        "status": IMPROVED_EVIDENCE_PLANNING_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "improved_evidence_planning_execution_using_redesigned_evidence_digest": digest,
        "generated_output_count": 14,
        "failure_count": 0,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_improved_evidence_planning_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    """Render a sanitized planning execution status document."""
    validation = (
        validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            artifact
        )
    )
    source = artifact["source_evidence"]
    sections = [
        ("Title", ["Optional Improved Evidence Planning Execution Using Redesigned Evidence v1."]),
        ("Optional Improved Evidence Planning Execution Using Redesigned Evidence", [
            f"Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
            f"Execution digest: `{validation['improved_evidence_planning_execution_using_redesigned_evidence_digest']}`.",
        ]),
        ("Source Approval", [f"Approval digest: `{source['improved_evidence_planning_approval_using_redesigned_evidence_digest']}`."]),
        ("Bound Evidence", [
            f"Records/labels/features/matrix: `{source['records_digest']}` / `{source['redesigned_label_values_digest']}` / `{source['feature_values_digest']}` / `{source['feature_label_matrix_digest']}`.",
        ]),
        ("Dataset and Universe", [f"`{DATASET_NAME}`; 11,946 records; META 913.", ", ".join(TARGET_UNIVERSE)]),
        ("Planning Execution Policy", ["Research-only planning was performed over read-only frozen evidence; no evidence generation or predictive execution occurred."]),
        ("Planning Facts", [f"`{artifact['planning_facts']}`"]),
        ("Selected Redesign Direction", [f"`{SELECTED_DIRECTION}`; planning only, results review required."]),
        ("Proposed Label Schema Plan", [f"`{artifact['proposed_label_schema_plan']}`"]),
        ("No-Trade / Abstain Coverage Plan", [f"`{artifact['no_trade_abstain_coverage_plan']}`"]),
        ("Material-Move Threshold Plan", [f"`{artifact['material_move_threshold_plan']}`"]),
        ("Horizon-Specific Validation Plan", [f"`{artifact['horizon_specific_validation_plan']}`"]),
        ("Ticker / Regime Split Validation Plan", [f"`{artifact['ticker_regime_split_validation_plan']}`"]),
        ("Feature-Label Alignment Plan", [f"`{artifact['feature_label_alignment_plan']}`"]),
        ("Chronological Split and Embargo Plan", [f"`{artifact['chronological_split_embargo_plan']}`"]),
        ("Baseline and Model Comparison Plan", [f"`{artifact['baseline_model_comparison_plan']}`"]),
        ("Calibration / Brier Plan", [f"`{artifact['calibration_brier_plan']}`"]),
        ("Leakage and No-Peek Control Plan", [f"`{artifact['leakage_no_peek_control_plan']}`"]),
        ("Per-Ticker and META Reporting Plan", ["12 deterministic entries; META remains exactly 913 without repair or inference."]),
        ("Output Digest Manifest", [f"14 entries; `{SELF_REFERENCE_POLICY}`; binding `{artifact['output_digest_manifest_summary']['binding_digest']}`."]),
        ("Authority Boundary", ["Planning execution created planning outputs only. Labels, targets, features, matrix rows, predictive evidence, and results review were not created."]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains `not accepted`; readiness and candidacy remain false."]),
        ("Profitability Boundary", ["Profitability remains `not accepted`."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, broker execution, recommendations, and trading remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"`{artifact['execution_checklist_summary']}`"]),
        ("Guardrails", ["No provider call, acquisition, regeneration, metric recomputation, model training, runtime action, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Improved Evidence Planning Execution Using Redesigned Evidence Status", ""]
    for title, body in sections:
        lines.extend([f"## {title}", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)
