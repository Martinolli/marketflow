"""Offline operator review of the predictive-evidence improvement candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_evidence_improvement_candidate_service as candidate_service


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE = (
    "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_V1 = (
    "predictive_evidence_improvement_candidate_review_v1"
)
PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_READY"
)

EXPECTED_CANDIDATE_DIGEST = (
    "3f993453ad80705a3bc002891d1def677d15f2a92044109efa3e4cfe9349d43d"
)
EXPECTED_READINESS_REVIEW_DIGEST = candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_REVIEW_DIGEST = (
    candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST
)
EXPECTED_RESULTS_REVIEW_DIGEST = candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = candidate_service.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = candidate_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED
PLANNED_NOT_EXECUTED = candidate_service.PLANNED_NOT_EXECUTED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class PredictiveEvidenceImprovementCandidateReviewError(ValueError):
    """Raised when the operator review violates its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveEvidenceImprovementCandidateReviewError(f"{field} mismatch")


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
        candidate_service.build_predictive_evidence_improvement_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_predictive_evidence_improvement_candidate_v1(source)
    _expect(
        source.get("predictive_evidence_improvement_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source improvement candidate digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_evidence_improvement_candidate_review_digest", None)
    return payload


def per_ticker_predictive_evidence_improvement_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_improvement_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "readiness_status": source_entry["readiness_status"],
            "improvement_candidate_status": source_entry[
                "improvement_candidate_status"
            ],
            "improvement_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "improvement_note": source_entry["improvement_note"],
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_predictive_evidence_improvement_candidate_digest": source[
                "predictive_evidence_improvement_candidate_digest"
            ],
            "per_ticker_predictive_evidence_improvement_candidate_digest": source_entry[
                "per_ticker_predictive_evidence_improvement_candidate_digest"
            ],
        }
        entry["per_ticker_predictive_evidence_improvement_candidate_review_digest"] = (
            per_ticker_predictive_evidence_improvement_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    source_summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_V1,
        "review_status": PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "improvement_execution_performed": False,
        "refinement_option_execution_performed": False,
        "model_comparison_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "readiness_decision": source["readiness_decision"],
        "readiness_reason": source["readiness_reason"],
        "predictive_evidence_improvement_candidate_created": True,
        "predictive_evidence_improvement_candidate_review_created": True,
        "predictive_evidence_improvement_ready_for_operator_review": True,
        "predictive_evidence_improvement_approved": False,
        "predictive_evidence_improvement_executed": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "feature_matrix_generation_authorized": False,
        "feature_matrix_generation_performed": False,
        "walk_forward_validation_authorized": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_authorized": False,
        "out_of_sample_evaluation_performed": False,
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
        "research_only": True,
        "operator_review_required": True,
        "reviewed_predictive_evidence_improvement_candidate_kind": source[
            "artifact_kind"
        ],
        "reviewed_predictive_evidence_improvement_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_predictive_evidence_improvement_candidate_digest": source[
            "predictive_evidence_improvement_candidate_digest"
        ],
        "reviewed_predictive_evidence_improvement_candidate_checklist_total": (
            source_summary["total_checks"]
        ),
        "reviewed_predictive_evidence_improvement_candidate_checklist_passed": (
            source_summary["passed_checks"]
        ),
        "reviewed_predictive_evidence_improvement_candidate_checklist_failed": (
            source_summary["failed_checks"]
        ),
        "reviewed_predictive_evidence_improvement_candidate_blocker_count": (
            source_summary["blocker_count"]
        ),
        "predictive_evidence_improvement_candidate_digest": source[
            "predictive_evidence_improvement_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_review_digest": source[
            "predictive_usefulness_acceptance_readiness_review_digest"
        ],
        "predictive_usefulness_reassessment_review_package_digest": source[
            "predictive_usefulness_reassessment_review_package_digest"
        ],
        "additional_predictive_evidence_results_review_package_digest": source[
            "additional_predictive_evidence_results_review_package_digest"
        ],
        "additional_predictive_evidence_execution_digest": source[
            "additional_predictive_evidence_execution_digest"
        ],
        "additional_predictive_evidence_execution_approval_digest": source[
            "additional_predictive_evidence_execution_approval_digest"
        ],
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "records_digest": source["records_digest"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "registry_approved_dataset_metadata": deepcopy(
            source["registry_approved_dataset_metadata"]
        ),
        "predictive_evidence_improvement_objective": source[
            "predictive_evidence_improvement_objective"
        ],
        "predictive_evidence_improvement_scope": source[
            "predictive_evidence_improvement_scope"
        ],
        "predictive_evidence_improvement_mode": source[
            "predictive_evidence_improvement_mode"
        ],
        "predictive_evidence_improvement_authority_status": source[
            "predictive_evidence_improvement_authority_status"
        ],
        "reviewed_readiness_failure_summary": deepcopy(
            source["readiness_failure_summary"]
        ),
        "reviewed_evidence_basis": deepcopy(source["evidence_basis"]),
        "reviewed_improvement_themes": deepcopy(source["improvement_themes"]),
        "reviewed_refinement_options": deepcopy(source["refinement_options"]),
        "per_ticker_improvement_candidate_review_entries": _per_ticker_review_entries(
            source
        ),
        "reviewed_future_improvement_chain": deepcopy(
            source["future_improvement_chain"]
        ),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "planned_output_count": len(source["planned_outputs"]),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "feature_label_refinement_plan_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE, "reviewed_predictive_evidence_improvement_candidate_kind"),
    ("candidate_status_ready_for_review", candidate_service.PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW, "reviewed_predictive_evidence_improvement_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "reviewed_predictive_evidence_improvement_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "reviewed_predictive_evidence_improvement_candidate_blocker_count"),
    ("readiness_review_digest_bound", EXPECTED_READINESS_REVIEW_DIGEST, "predictive_usefulness_acceptance_readiness_review_digest"),
    ("reassessment_review_digest_bound", EXPECTED_REASSESSMENT_REVIEW_DIGEST, "predictive_usefulness_reassessment_review_package_digest"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_candidate_universe", TARGET_UNIVERSE, "target_universe"),
    ("readiness_decision_not_ready", candidate_service.readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY, "readiness_decision"),
    ("readiness_reason_mixed_stability_and_insufficient_baseline_outperformance", "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", "readiness_reason"),
    ("stability_consistency_required_not_met", candidate_service.readiness_service.NOT_MET, "failure_stability_consistency_required"),
    ("baseline_outperformance_consistency_required_not_met", candidate_service.readiness_service.NOT_MET, "failure_baseline_outperformance_consistency_required"),
    ("predictive_evidence_improvement_candidate_created_true", True, "predictive_evidence_improvement_candidate_created"),
    ("predictive_evidence_improvement_candidate_review_created_true", True, "predictive_evidence_improvement_candidate_review_created"),
    ("improvement_candidate_scope_candidate_only", candidate_service.IMPROVEMENT_SCOPE, "predictive_evidence_improvement_scope"),
    ("improvement_authority_status_not_authorized", NOT_AUTHORIZED, "predictive_evidence_improvement_authority_status"),
    ("walk_forward_accuracy_range_bound", "0.498698 to 0.562842", "evidence_walk_forward_accuracy_range"),
    ("oos_performance_summary_bound", True, "oos_performance_summary_bound"),
    ("leakage_status_pass", PASS, "evidence_leakage_status"),
    ("failed_leakage_controls_zero", 0, "evidence_failed_leakage_controls"),
    ("improvement_themes_reviewed", candidate_service.IMPROVEMENT_THEME_IDS, "improvement_theme_ids"),
    ("refinement_options_reviewed", candidate_service.REFINEMENT_OPTION_IDS, "refinement_option_ids"),
    ("per_ticker_improvement_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_improvement_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_improvement_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("future_improvement_chain_reviewed", candidate_service.FUTURE_IMPROVEMENT_CHAIN, "reviewed_future_improvement_chain"),
    ("future_gates_defined", candidate_service.FUTURE_GATES, "reviewed_future_gates"),
    ("risk_controls_defined", candidate_service.RISK_CONTROLS, "reviewed_risk_controls"),
    ("planned_outputs_7", 7, "planned_output_count"),
    ("planned_outputs_not_generated", PLANNED_NOT_GENERATED, "planned_outputs_status"),
    ("planned_outputs_research_only", RESEARCH_ONLY_NON_ACTIONABLE, "planned_outputs_label"),
    ("provider_requests_made_in_review_false", False, "provider_requests_made_in_review"),
    ("live_provider_transport_enabled_in_review_false", False, "live_provider_transport_enabled_in_review"),
    ("market_data_acquisition_performed_in_review_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_generation_performed_in_review_false", False, "dataset_generation_performed_in_review"),
    ("canonical_dataset_regenerated_in_review_false", False, "canonical_dataset_regenerated_in_review"),
    ("predictive_execution_rerun_performed_false", False, "predictive_execution_rerun_performed"),
    ("label_generation_rerun_performed_false", False, "label_generation_rerun_performed"),
    ("feature_matrix_rerun_performed_false", False, "feature_matrix_rerun_performed"),
    ("walk_forward_validation_rerun_performed_false", False, "walk_forward_validation_rerun_performed"),
    ("out_of_sample_evaluation_rerun_performed_false", False, "out_of_sample_evaluation_rerun_performed"),
    ("metrics_recomputation_performed_false", False, "metrics_recomputation_performed"),
    ("improvement_execution_performed_false", False, "improvement_execution_performed"),
    ("refinement_option_execution_performed_false", False, "refinement_option_execution_performed"),
    ("model_comparison_performed_false", False, "model_comparison_performed"),
    ("new_strategy_scoring_performed_false", False, "new_strategy_scoring_performed"),
    ("trade_recommendations_generated_false", False, "trade_recommendations_generated"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("predictive_usefulness_acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("predictive_usefulness_acceptance_recommended_false", False, "predictive_usefulness_acceptance_recommended"),
    ("predictive_usefulness_acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("profitability_acceptance_ready_false", False, "profitability_acceptance_ready"),
    ("profitability_acceptance_recommended_false", False, "profitability_acceptance_recommended"),
    ("runtime_migration_approved_false", False, "runtime_migration_approved"),
    ("runtime_use_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_use_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("paper_trading_not_authorized", NOT_AUTHORIZED, "paper_trading"),
    ("broker_execution_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("automatic_stitching_false", False, "automatic_stitching"),
    ("no_feature_label_refinement_candidate_created", False, "feature_label_refinement_plan_candidate_created"),
    ("no_additional_predictive_evidence_execution_candidate_created", False, "additional_predictive_evidence_execution_candidate_created"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
]
REQUIRED_CHECK_IDS = [item[0] for item in CHECK_FIELD_SPECS]


def _derived_check_fields(review_package: dict[str, Any]) -> dict[str, Any]:
    failure = review_package.get("reviewed_readiness_failure_summary", {})
    evidence = review_package.get("reviewed_evidence_basis", {})
    themes = review_package.get("reviewed_improvement_themes", [])
    options = review_package.get("reviewed_refinement_options", [])
    entries = review_package.get(
        "per_ticker_improvement_candidate_review_entries", []
    )
    return {
        "failure_stability_consistency_required": failure.get(
            "stability_consistency_required"
        ),
        "failure_baseline_outperformance_consistency_required": failure.get(
            "baseline_outperformance_consistency_required"
        ),
        "evidence_walk_forward_accuracy_range": evidence.get(
            "walk_forward_accuracy_range"
        ),
        "evidence_leakage_status": evidence.get("leakage_status"),
        "evidence_failed_leakage_controls": evidence.get(
            "failed_leakage_controls"
        ),
        "oos_performance_summary_bound": {
            key: evidence.get(key)
            for key in (
                "oos_majority_accuracy",
                "oos_previous_direction_accuracy",
                "oos_ticker_cross_sectional_accuracy",
                "oos_brier_score",
            )
        }
        == {
            "oos_majority_accuracy": "0.539491",
            "oos_previous_direction_accuracy": "0.495984",
            "oos_ticker_cross_sectional_accuracy": "0.502677",
            "oos_brier_score": "0.24875351",
        },
        "improvement_theme_ids": [
            row.get("theme_id") for row in themes if isinstance(row, dict)
        ],
        "refinement_option_ids": [
            row.get("option_id") for row in options if isinstance(row, dict)
        ],
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": isinstance(entries, list)
        and all(
            isinstance(row, dict)
            and isinstance(
                row.get("per_ticker_predictive_evidence_improvement_candidate_digest"),
                str,
            )
            and len(row["per_ticker_predictive_evidence_improvement_candidate_digest"])
            == 64
            for row in entries
        ),
        "per_ticker_review_digests_valid": isinstance(entries, list)
        and all(
            isinstance(row, dict)
            and isinstance(
                row.get(
                    "per_ticker_predictive_evidence_improvement_candidate_review_digest"
                ),
                str,
            )
            and row[
                "per_ticker_predictive_evidence_improvement_candidate_review_digest"
            ]
            == per_ticker_predictive_evidence_improvement_candidate_review_digest_v1(row)
            for row in entries
        ),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review_package)
    values.update(_derived_check_fields(review_package))
    return [_check(check_id, expected, values.get(field)) for check_id, expected, field in CHECK_FIELD_SPECS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(row.get("status") == PASS for row in checklist)
    failed = total - passed
    blockers = sum(
        row.get("status") == FAIL and row.get("severity") == BLOCKER
        for row in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "ready_for_operator_assessment": blockers == 0,
        "ready_for_feature_label_refinement_candidate": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("predictive_evidence_improvement_candidate_review_package_digest", None)
    return payload


def predictive_evidence_improvement_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    return semantic_digest(_digest_payload(review_package))


def build_predictive_evidence_improvement_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build an offline operator review of the exact improvement candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["predictive_evidence_improvement_candidate_review_package_digest"] = (
        predictive_evidence_improvement_candidate_review_package_digest_v1(
            review_package
        )
    )
    validate_predictive_evidence_improvement_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "LABEL_GENERATION_EXECUTED",
        "FEATURE_MATRIX_GENERATION_EXECUTED",
        "WALK_FORWARD_VALIDATION_EXECUTED",
        "OUT_OF_SAMPLE_EVALUATION_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed",
        "improvement_execution_performed",
        "refinement_option_execution_performed",
        "model_comparison_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_evidence_improvement_approved",
        "predictive_evidence_improvement_executed",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "label_generation_authorized",
        "label_generation_performed",
        "feature_matrix_generation_authorized",
        "feature_matrix_generation_performed",
        "walk_forward_validation_authorized",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_authorized",
        "out_of_sample_evaluation_performed",
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
        "feature_label_refinement_plan_candidate_created",
        "additional_predictive_evidence_execution_candidate_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveEvidenceImprovementCandidateReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveEvidenceImprovementCandidateReviewError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveEvidenceImprovementCandidateReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveEvidenceImprovementCandidateReviewError(
                    f"{current} must not be accepted"
                )
            if key == "predictive_evidence_improvement_authority_status" and item != NOT_AUTHORIZED:
                raise PredictiveEvidenceImprovementCandidateReviewError(
                    f"{current} must remain {NOT_AUTHORIZED}"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_evidence_improvement_candidate_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate the exact operator-review package and keep all later gates closed."""
    if not isinstance(review_package, dict):
        raise PredictiveEvidenceImprovementCandidateReviewError(
            "improvement candidate review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    expected_source = candidate_service.build_predictive_evidence_improvement_candidate_v1()
    expected_base = _base_review(expected_source)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceImprovementCandidateReviewError(
            "review_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveEvidenceImprovementCandidateReviewError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "predictive_evidence_improvement_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceImprovementCandidateReviewError(
            "predictive evidence improvement candidate review package digest missing"
        )
    _expect(
        digest,
        predictive_evidence_improvement_candidate_review_package_digest_v1(
            review_package
        ),
        "predictive_evidence_improvement_candidate_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "predictive_evidence_improvement_candidate_review_package_digest": digest,
        "reviewed_candidate_digest": review_package[
            "reviewed_predictive_evidence_improvement_candidate_digest"
        ],
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_improvement_candidate_review_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_assessment": True,
        "predictive_evidence_improvement_authorized": False,
        "predictive_evidence_improvement_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_evidence_improvement_candidate_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized operator-facing candidate-review summary."""
    validation = validate_predictive_evidence_improvement_candidate_review_package_v1(
        review_package
    )
    failure = review_package["reviewed_readiness_failure_summary"]
    evidence = review_package["reviewed_evidence_basis"]
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Improvement Candidate Operator Review Status",
        "",
        "## Title",
        "- Predictive Evidence Improvement Candidate Operator Review Package v1.",
        "",
        "## Predictive Evidence Improvement Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['predictive_evidence_improvement_candidate_review_package_digest']}`",
        "",
        "## Reviewed Improvement Candidate",
        f"- Candidate artifact/status: `{review_package['reviewed_predictive_evidence_improvement_candidate_kind']}` / `{review_package['reviewed_predictive_evidence_improvement_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_predictive_evidence_improvement_candidate_digest']}`",
        "",
        "## Source Acceptance Readiness Review",
        f"- Readiness-review digest: `{review_package['predictive_usefulness_acceptance_readiness_review_digest']}`",
        "",
        "## Readiness Failure Summary",
        f"- Decision/reason: `{failure['readiness_decision']}` / `{failure['readiness_reason']}`",
        f"- Stability/baseline: `{failure['stability_consistency_required']}` / `{failure['baseline_outperformance_consistency_required']}`",
        "",
        "## Evidence Basis",
        f"- Walk-forward range: `{evidence['walk_forward_accuracy_range']}`",
        f"- OOS majority/previous/cross-sectional: `{evidence['oos_majority_accuracy']}` / `{evidence['oos_previous_direction_accuracy']}` / `{evidence['oos_ticker_cross_sectional_accuracy']}`",
        f"- Brier/leakage/failed controls: `{evidence['oos_brier_score']}` / `{evidence['leakage_status']}` / `{evidence['failed_leakage_controls']}`",
        "",
        "## Reviewed Improvement Themes",
    ]
    lines.extend(
        f"- `{row['theme_id']}`" for row in review_package["reviewed_improvement_themes"]
    )
    lines.extend(["", "## Reviewed Refinement Options"])
    lines.extend(
        f"- `{row['option_id']}`" for row in review_package["reviewed_refinement_options"]
    )
    lines.extend(
        [
            "",
            "## Per-Ticker Improvement Candidate Review Entries",
            f"- Entry count: `{len(review_package['per_ticker_improvement_candidate_review_entries'])}`; META preserves 913 records and all other tickers preserve 1003.",
            "",
            "## Future Improvement Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(
            review_package["reviewed_future_improvement_chain"], start=1
        )
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness/readiness: `{review_package['predictive_usefulness']}` / `{review_package['predictive_usefulness_acceptance_ready']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{review_package['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']}` / `{review_package['strategy_use']}` / `{review_package['paper_trading']}` / `{review_package['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- Review built offline from the exact candidate. No provider request, acquisition, regeneration, rerun, improvement execution, refinement execution, model comparison, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Themes, options, and planned outputs remain research-only and non-authorizing.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_improvement_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical operator-review JSON once without overwriting."""
    review_package = build_predictive_evidence_improvement_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_predictive_evidence_improvement_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_improvement_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceImprovementCandidateReviewError(
            "predictive evidence improvement candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceImprovementCandidateReviewError(
            "predictive evidence improvement candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
