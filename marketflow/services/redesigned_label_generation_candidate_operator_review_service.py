"""Offline operator review of the redesigned-label generation candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import redesigned_label_generation_candidate_service as candidate_service


ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_V1 = (
    "redesigned_label_generation_candidate_review_v1"
)
REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY"
)
REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_VALID = (
    "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_VALID"
)
EXPECTED_CANDIDATE_DIGEST = (
    "6ef5c93b660e2f2ad825a774299e3dae1adc3041a1f619f7b3df0001c18f5a08"
)
EXPECTED_CANDIDATE_CHECKLIST_TOTAL = 46
EXPECTED_CANDIDATE_CHECKLIST_PASSED = 46
EXPECTED_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_CANDIDATE_BLOCKER_COUNT = 0
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "redesigned_label_generation_candidate_digest_bound",
    "label_objective_redesign_results_review_digest_bound",
    "label_objective_redesign_execution_digest_bound",
    "label_objective_redesign_execution_approval_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_candidate_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "results_review_ready_true",
    "ready_for_redesigned_label_generation_candidate_true",
    "redesigned_label_generation_candidate_created_true",
    "redesigned_label_generation_candidate_ready_for_operator_review_true",
    "redesigned_label_generation_candidate_review_created_true",
    "redesigned_label_generation_approved_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "actual_redesigned_labels_generated_false",
    "source_design_inputs_reviewed",
    "planned_label_families_10_reviewed",
    "planned_threshold_strategies_7_reviewed",
    "planned_horizon_strategies_5_reviewed",
    "planned_availability_rules_reviewed",
    "per_ticker_entries_12",
    "per_ticker_candidate_digests_present",
    "per_ticker_review_digests_present",
    "future_chain_reviewed",
    "future_gates_reviewed",
    "risk_controls_reviewed",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "no_actual_label_generation",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class RedesignedLabelGenerationCandidateReviewError(ValueError):
    """Raised when the review violates its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise RedesignedLabelGenerationCandidateReviewError(f"{field} mismatch")


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


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_redesigned_label_generation_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        validation = candidate_service.validate_redesigned_label_generation_candidate_v1(
            source
        )
    except candidate_service.RedesignedLabelGenerationCandidateError as exc:
        raise RedesignedLabelGenerationCandidateReviewError(
            "source redesigned label generation candidate is invalid"
        ) from exc
    _expect(
        source.get("artifact_kind"),
        candidate_service.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE,
        "source candidate kind",
    )
    _expect(
        source.get("candidate_status"),
        candidate_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "source candidate status",
    )
    _expect(
        source.get("redesigned_label_generation_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    _expect(
        source.get("review_summary", {}).get("total_checks"),
        EXPECTED_CANDIDATE_CHECKLIST_TOTAL,
        "source candidate checklist total",
    )
    _expect(
        source.get("review_summary", {}).get("passed_checks"),
        EXPECTED_CANDIDATE_CHECKLIST_PASSED,
        "source candidate checklist passed",
    )
    _expect(
        source.get("review_summary", {}).get("failed_checks"),
        EXPECTED_CANDIDATE_CHECKLIST_FAILED,
        "source candidate checklist failed",
    )
    _expect(
        source.get("review_summary", {}).get("blocker_count"),
        EXPECTED_CANDIDATE_BLOCKER_COUNT,
        "source candidate blocker count",
    )
    _expect(
        validation.get("redesigned_label_generation_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "validated source candidate digest",
    )
    return source


def per_ticker_redesigned_label_generation_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one reviewed ticker entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_redesigned_label_generation_candidate_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_candidate_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "source_label_objective_plan_status": row[
                "source_label_objective_plan_status"
            ],
            "redesigned_label_generation_candidate_status": row[
                "redesigned_label_generation_candidate_status"
            ],
            "redesigned_label_generation_candidate_review_status": (
                "READY_FOR_OPERATOR_ASSESSMENT"
            ),
            "redesigned_label_generation_authorized": False,
            "redesigned_label_generation_performed": False,
            "actual_redesigned_labels_generated": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_redesigned_label_generation_candidate_digest": (
                EXPECTED_CANDIDATE_DIGEST
            ),
            "per_ticker_redesigned_label_generation_candidate_digest": row[
                "per_ticker_redesigned_label_generation_candidate_digest"
            ],
        }
        if row["ticker"] == "META":
            entry["label_availability_note"] = row["label_availability_note"]
        entry["per_ticker_redesigned_label_generation_candidate_review_digest"] = (
            per_ticker_redesigned_label_generation_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    source_summary = source["review_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_V1,
        "review_status": REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "canonical_dataset_regenerated": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "ready_for_redesigned_label_generation_candidate": True,
        "redesigned_label_generation_candidate_created": True,
        "redesigned_label_generation_candidate_ready_for_operator_review": True,
        "redesigned_label_generation_candidate_review_created": True,
        "redesigned_label_generation_approved": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "actual_redesigned_labels_generated": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
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
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        "reviewed_redesigned_label_generation_candidate_kind": source[
            "artifact_kind"
        ],
        "reviewed_redesigned_label_generation_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_redesigned_label_generation_candidate_digest": source[
            "redesigned_label_generation_candidate_digest"
        ],
        "reviewed_redesigned_label_generation_candidate_checklist_total": source_summary[
            "total_checks"
        ],
        "reviewed_redesigned_label_generation_candidate_checklist_passed": source_summary[
            "passed_checks"
        ],
        "reviewed_redesigned_label_generation_candidate_checklist_failed": source_summary[
            "failed_checks"
        ],
        "reviewed_redesigned_label_generation_candidate_blocker_count": source_summary[
            "blocker_count"
        ],
        "redesigned_label_generation_candidate_digest": source[
            "redesigned_label_generation_candidate_digest"
        ],
        "label_objective_redesign_results_review_package_digest": source[
            "label_objective_redesign_results_review_package_digest"
        ],
        "label_objective_redesign_execution_digest": source[
            "label_objective_redesign_execution_digest"
        ],
        "label_objective_redesign_execution_approval_digest": source[
            "label_objective_redesign_execution_approval_digest"
        ],
        "label_objective_redesign_execution_candidate_review_package_digest": source[
            "label_objective_redesign_execution_candidate_review_package_digest"
        ],
        "label_objective_redesign_execution_candidate_digest": source[
            "label_objective_redesign_execution_candidate_digest"
        ],
        "label_objective_redesign_approval_digest": source[
            "label_objective_redesign_approval_digest"
        ],
        "operator_method_path_selection_digest": source[
            "operator_method_path_selection_digest"
        ],
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "records_digest": source["records_digest"],
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source[
            "meta_reduced_record_count_preserved"
        ],
        "redesigned_label_generation_candidate_objective": source[
            "redesigned_label_generation_candidate_objective"
        ],
        "redesigned_label_generation_candidate_scope": source[
            "redesigned_label_generation_candidate_scope"
        ],
        "redesigned_label_generation_candidate_mode": source[
            "redesigned_label_generation_candidate_mode"
        ],
        "redesigned_label_generation_candidate_authority_status": source[
            "redesigned_label_generation_candidate_authority_status"
        ],
        "source_label_objective_redesign_output_root": source[
            "source_label_objective_redesign_output_root"
        ],
        "source_label_objective_redesign_output_count": source[
            "source_label_objective_redesign_output_count"
        ],
        "source_label_objective_redesign_output_status": source[
            "source_label_objective_redesign_output_status"
        ],
        "label_family_candidate_count": source["label_family_candidate_count"],
        "threshold_design_strategy_count": source[
            "threshold_design_strategy_count"
        ],
        "horizon_design_candidate_count": source["horizon_design_candidate_count"],
        "per_ticker_plan_count": source["per_ticker_plan_count"],
        "planning_output_interpretation": source[
            "planning_output_interpretation"
        ],
        "label_generation_interpretation": source[
            "label_generation_interpretation"
        ],
        "predictive_usefulness_interpretation": source[
            "predictive_usefulness_interpretation"
        ],
        "reviewed_redesigned_label_generation_inputs": deepcopy(
            source["source_design_inputs"]
        ),
        "reviewed_planned_redesigned_label_families": deepcopy(
            source["planned_redesigned_label_families"]
        ),
        "reviewed_planned_threshold_strategies": deepcopy(
            source["planned_threshold_strategies"]
        ),
        "reviewed_planned_horizon_strategies": deepcopy(
            source["planned_horizon_strategies"]
        ),
        "reviewed_planned_label_availability_rules": deepcopy(
            source["planned_label_availability_rules"]
        ),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "reviewed_future_chain": list(source["future_chain"]),
        "reviewed_future_gates": list(source["future_gates"]),
        "reviewed_risk_controls": list(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
    }


def _derived_checks(review_package: dict[str, Any]) -> dict[str, bool]:
    entries = review_package.get("per_ticker_review_entries", [])
    inputs = review_package.get("reviewed_redesigned_label_generation_inputs", [])
    families = review_package.get("reviewed_planned_redesigned_label_families", [])
    thresholds = review_package.get("reviewed_planned_threshold_strategies", [])
    horizons = review_package.get("reviewed_planned_horizon_strategies", [])
    rules = review_package.get("reviewed_planned_label_availability_rules", [])
    outputs = review_package.get("reviewed_planned_outputs", [])
    counts = review_package.get("per_ticker_record_counts", {})
    return {
        "candidate_kind_matches": review_package.get("reviewed_redesigned_label_generation_candidate_kind") == candidate_service.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE,
        "candidate_status_ready_for_review": review_package.get("reviewed_redesigned_label_generation_candidate_status") == candidate_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "candidate_digest_matches_expected": review_package.get("reviewed_redesigned_label_generation_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "candidate_checklist_zero_blockers": review_package.get("reviewed_redesigned_label_generation_candidate_checklist_total") == 46 and review_package.get("reviewed_redesigned_label_generation_candidate_checklist_passed") == 46 and review_package.get("reviewed_redesigned_label_generation_candidate_checklist_failed") == 0 and review_package.get("reviewed_redesigned_label_generation_candidate_blocker_count") == 0,
        "redesigned_label_generation_candidate_digest_bound": review_package.get("redesigned_label_generation_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "label_objective_redesign_results_review_digest_bound": review_package.get("label_objective_redesign_results_review_package_digest") == candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "label_objective_redesign_execution_digest_bound": review_package.get("label_objective_redesign_execution_digest") == candidate_service.EXPECTED_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest_bound": review_package.get("label_objective_redesign_execution_approval_digest") == candidate_service.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "records_digest_bound": review_package.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": review_package.get("target_universe_count") == 12 and review_package.get("target_universe") == TARGET_UNIVERSE,
        "target_universe_matches_candidate_universe": review_package.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": review_package.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": review_package.get("meta_record_count") == 913 and counts.get("META") == 913 and review_package.get("meta_reduced_record_count_preserved") is True,
        "results_review_ready_true": review_package.get("label_objective_redesign_results_review_ready") is True,
        "ready_for_redesigned_label_generation_candidate_true": review_package.get("ready_for_redesigned_label_generation_candidate") is True,
        "redesigned_label_generation_candidate_created_true": review_package.get("redesigned_label_generation_candidate_created") is True,
        "redesigned_label_generation_candidate_ready_for_operator_review_true": review_package.get("redesigned_label_generation_candidate_ready_for_operator_review") is True,
        "redesigned_label_generation_candidate_review_created_true": review_package.get("redesigned_label_generation_candidate_review_created") is True,
        "redesigned_label_generation_approved_false": review_package.get("redesigned_label_generation_approved") is False,
        "redesigned_label_generation_authorized_false": review_package.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_performed_false": review_package.get("redesigned_label_generation_performed") is False,
        "actual_redesigned_labels_generated_false": review_package.get("actual_redesigned_labels_generated") is False,
        "source_design_inputs_reviewed": [item.get("source_input_id") for item in inputs if isinstance(item, dict)] == candidate_service.SOURCE_DESIGN_INPUT_IDS,
        "planned_label_families_10_reviewed": [item.get("planned_label_family_id") for item in families if isinstance(item, dict)] == candidate_service.PLANNED_LABEL_FAMILY_IDS,
        "planned_threshold_strategies_7_reviewed": [item.get("threshold_strategy_id") for item in thresholds if isinstance(item, dict)] == candidate_service.PLANNED_THRESHOLD_STRATEGY_IDS,
        "planned_horizon_strategies_5_reviewed": [item.get("horizon_strategy_id") for item in horizons if isinstance(item, dict)] == candidate_service.PLANNED_HORIZON_STRATEGY_IDS,
        "planned_availability_rules_reviewed": [item.get("availability_rule_id") for item in rules if isinstance(item, dict)] == candidate_service.PLANNED_AVAILABILITY_RULE_IDS,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_candidate_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_redesigned_label_generation_candidate_digest"), str) and len(item["per_ticker_redesigned_label_generation_candidate_digest"]) == 64 for item in entries if isinstance(item, dict)),
        "per_ticker_review_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_redesigned_label_generation_candidate_review_digest"), str) and len(item["per_ticker_redesigned_label_generation_candidate_review_digest"]) == 64 and item["per_ticker_redesigned_label_generation_candidate_review_digest"] == per_ticker_redesigned_label_generation_candidate_review_digest_v1(item) for item in entries if isinstance(item, dict)),
        "future_chain_reviewed": review_package.get("reviewed_future_chain") == candidate_service.FUTURE_CHAIN,
        "future_gates_reviewed": review_package.get("reviewed_future_gates") == candidate_service.FUTURE_GATES,
        "risk_controls_reviewed": review_package.get("reviewed_risk_controls") == candidate_service.RISK_CONTROLS,
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == 8 and all(item.get("planned_output_status") == "PLANNED_NOT_GENERATED" for item in outputs if isinstance(item, dict)),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == 8 and all(item.get("output_label") == "RESEARCH_ONLY_NON_ACTIONABLE" and item.get("research_only") is True and item.get("non_actionable") is True for item in outputs if isinstance(item, dict)),
        "feature_generation_false": review_package.get("feature_generation_performed") is False and review_package.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": review_package.get("metric_recomputation_performed") is False,
        "model_training_false": review_package.get("model_training_performed") is False,
        "additional_predictive_evidence_execution_candidate_created_false": review_package.get("additional_predictive_evidence_execution_candidate_created") is False,
        "predictive_usefulness_not_accepted": review_package.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review_package.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review_package.get("runtime_migration_approved") is False and review_package.get("runtime_migration_active") is False and review_package.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review_package.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review_package.get("paper_trading") == NOT_AUTHORIZED and review_package.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review_package.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": review_package.get("provider_requests_made") is False,
        "market_data_acquisition_false": review_package.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": review_package.get("dataset_regeneration_performed") is False and review_package.get("canonical_dataset_regenerated") is False,
        "no_actual_label_generation": review_package.get("label_generation_performed") is False and review_package.get("redesigned_label_generation_performed") is False and review_package.get("actual_redesigned_labels_generated") is False,
        "no_predictive_usefulness_acceptance_artifact_created": review_package.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": review_package.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": review_package.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": review_package.get("no_tracked_marketflow_files") is True and review_package.get("tracked_marketflow_files") == [],
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(review_package)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_redesigned_label_generation_approval": False,
        "ready_for_redesigned_label_generation_execution": False,
        "actual_redesigned_labels_generated": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def redesigned_label_generation_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for the complete review package."""
    payload = deepcopy(review_package)
    payload.pop("redesigned_label_generation_candidate_review_package_digest", None)
    return semantic_digest(payload)


def build_redesigned_label_generation_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build a review-only package for the exact candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["redesigned_label_generation_candidate_review_package_digest"] = (
        redesigned_label_generation_candidate_review_package_digest_v1(
            review_package
        )
    )
    validate_redesigned_label_generation_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_authority(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "REDESIGNED_LABEL_GENERATION_APPROVED",
        "REDESIGNED_LABEL_GENERATION_EXECUTED",
        "LABEL_GENERATION_EXECUTED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "label_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
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
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "label_objective_redesign_execution_rerun_performed",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
        "label_generation_authorized",
        "actual_label_values_created",
        "threshold_computation_authorized",
        "threshold_computation_performed",
        "horizon_selection_authorized",
        "horizon_selection_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise RedesignedLabelGenerationCandidateReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true_fields and item is True:
                raise RedesignedLabelGenerationCandidateReviewError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise RedesignedLabelGenerationCandidateReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise RedesignedLabelGenerationCandidateReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_redesigned_label_generation_candidate_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Validate the exact candidate binding and every closed authority gate."""
    if not isinstance(review_package, dict):
        raise RedesignedLabelGenerationCandidateReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_authority(review_package)
    for field, expected in _base_review(_source_candidate(None)).items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise RedesignedLabelGenerationCandidateReviewError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise RedesignedLabelGenerationCandidateReviewError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "redesigned_label_generation_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise RedesignedLabelGenerationCandidateReviewError(
            "candidate review package digest missing"
        )
    _expect(
        digest,
        redesigned_label_generation_candidate_review_package_digest_v1(
            review_package
        ),
        "redesigned_label_generation_candidate_review_package_digest",
    )
    return {
        "status": REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "redesigned_label_generation_candidate_review_package_digest": digest,
        "reviewed_redesigned_label_generation_candidate_digest": (
            EXPECTED_CANDIDATE_DIGEST
        ),
        "ready_for_operator_assessment": True,
        "ready_for_redesigned_label_generation_approval": False,
        "ready_for_redesigned_label_generation_execution": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_redesigned_label_generation_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render the validated review-only package as Markdown."""
    validate_redesigned_label_generation_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Redesigned Label Generation Candidate Review Package", "",
        "## Title", "- Redesigned Label Generation Candidate Operator Review Package v1.", "",
        "## Redesigned Label Generation Candidate Review Package", f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.", f"- Review digest: `{review_package['redesigned_label_generation_candidate_review_package_digest']}`.", "",
        "## Reviewed Candidate", f"- Kind/status/digest: `{review_package['reviewed_redesigned_label_generation_candidate_kind']}` / `{review_package['reviewed_redesigned_label_generation_candidate_status']}` / `{review_package['reviewed_redesigned_label_generation_candidate_digest']}`.", "- Candidate checklist: `46 / 46` passed; `0` blockers.", "",
        "## Bound Evidence", f"- Results review/execution/approval: `{review_package['label_objective_redesign_results_review_package_digest']}` / `{review_package['label_objective_redesign_execution_digest']}` / `{review_package['label_objective_redesign_execution_approval_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` records for `{', '.join(review_package['target_universe'])}`; META remains `{review_package['meta_record_count']}`.", "",
        "## Source Design Artifacts", f"- `{review_package['source_label_objective_redesign_output_count']}` artifacts remain `{review_package['source_label_objective_redesign_output_status']}`.", "",
        "## Reviewed Redesigned Label Generation Inputs",
    ]
    lines.extend(f"- `{item['source_input_id']}`: `{item['source_input_status']}`." for item in review_package["reviewed_redesigned_label_generation_inputs"])
    for heading, key, id_key in [
        ("Reviewed Planned Label Families", "reviewed_planned_redesigned_label_families", "planned_label_family_id"),
        ("Reviewed Planned Threshold Strategies", "reviewed_planned_threshold_strategies", "threshold_strategy_id"),
        ("Reviewed Planned Horizon Strategies", "reviewed_planned_horizon_strategies", "horizon_strategy_id"),
        ("Reviewed Planned Availability Rules", "reviewed_planned_label_availability_rules", "availability_rule_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in review_package[key])
    lines.extend(["", "## Per-Ticker Review Entries"])
    lines.extend(f"- `{item['ticker']}`: review ready; label generation unauthorized." for item in review_package["per_ticker_review_entries"])
    for heading, key in [("Future Chain", "reviewed_future_chain"), ("Future Gates", "reviewed_future_gates"), ("Risk Controls", "reviewed_risk_controls")]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in review_package[key])
    lines.extend([
        "", "## Checklist Summary", f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "", "## Guardrails", "- Review only: no label or feature generation, predictive evidence, acceptance, profitability approval, runtime, trading, or recommendations.", "- Any approval remains a separate future ceremony if selected.", "",
    ])
    return "\n".join(lines)


def write_redesigned_label_generation_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting."""
    review_package = build_redesigned_label_generation_candidate_review_package_v1(
        candidate
    )
    validation = validate_redesigned_label_generation_candidate_review_package_v1(
        review_package
    )
    output_name = (
        filename
        or "redesigned_label_generation_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RedesignedLabelGenerationCandidateReviewError(
            "review package filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(review_package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise RedesignedLabelGenerationCandidateReviewError(
            "review package output already exists"
        ) from exc
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
