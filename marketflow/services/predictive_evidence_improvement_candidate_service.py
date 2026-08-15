"""Offline planning candidate for improving mixed predictive evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_acceptance_readiness_review_service as readiness_service


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE = (
    "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_V1 = (
    "predictive_evidence_improvement_candidate_v1"
)
PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_READINESS_REVIEW_DIGEST = (
    "d4ea4dc23590d9746727d5028116e2d0711fbc55dc8853f0b455d6ee4344a3e3"
)
EXPECTED_REASSESSMENT_REVIEW_DIGEST = (
    readiness_service.EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    readiness_service.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_RESULTS_REVIEW_DIGEST = readiness_service.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
EXPECTED_EXECUTION_DIGEST = readiness_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = readiness_service.EXPECTED_EXECUTION_APPROVAL_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    readiness_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    readiness_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = readiness_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(readiness_service.TARGET_UNIVERSE)
NOT_ACCEPTED = readiness_service.NOT_ACCEPTED
NOT_AUTHORIZED = readiness_service.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = readiness_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = readiness_service.PLANNED_NOT_GENERATED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"

IMPROVEMENT_OBJECTIVE = (
    "PLAN_IMPROVEMENTS_FOR_MIXED_PREDICTIVE_EVIDENCE_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
)
IMPROVEMENT_SCOPE = "IMPROVEMENT_CANDIDATE_ONLY_NOT_EXECUTION"

IMPROVEMENT_THEME_IDS = [
    "feature_signal_quality_improvement",
    "label_definition_refinement",
    "baseline_outperformance_improvement",
    "walk_forward_stability_improvement",
    "oos_generalization_improvement",
    "calibration_improvement",
    "false_positive_false_negative_balance_improvement",
    "ticker_cross_sectional_signal_review",
    "meta_reduced_record_count_handling_review",
    "data_quality_flag_enrichment",
    "model_family_comparison_planning",
]

REFINEMENT_OPTION_IDS = [
    "refine_return_bucket_thresholds",
    "test_alternative_horizons_5_10_20_sessions",
    "review_volatility_regime_label_windows",
    "review_drawdown_risk_label_thresholds",
    "add_or_refine_vpa_features",
    "add_relative_strength_and_cross_sectional_features",
    "add_quality_and_missingness_indicators",
    "compare_simple_baselines_with_regularized_models_if_available",
    "improve_walk_forward_window_policy",
    "add_stability_thresholds_for_acceptance_readiness",
]

FUTURE_IMPROVEMENT_CHAIN = [
    "Predictive evidence improvement candidate operator review package.",
    "Feature/label refinement plan candidate, if selected.",
    "Additional predictive evidence execution candidate for improved evidence.",
    "Additional predictive evidence execution approval ceremony, if required.",
    "Additional predictive evidence execution.",
    "Additional predictive evidence results review.",
    "Predictive usefulness reassessment review rerun.",
    "Predictive usefulness acceptance readiness review rerun.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "predictive_evidence_improvement_candidate_operator_review",
    "feature_label_refinement_plan_candidate_if_selected",
    "additional_predictive_evidence_execution_candidate_for_improved_evidence",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_review_rerun",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_improvement_execution_without_operator_approval",
    "no_label_refinement_execution_without_operator_approval",
    "no_feature_generation_without_execution_approval",
    "no_model_comparison_without_execution_approval",
    "no_predictive_usefulness_acceptance_from_improvement_candidate",
    "no_acceptance_when_readiness_not_met",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_predictive_evidence_without_new_approval",
    "preserve_meta_reduced_record_count",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_NAMES = [
    "predictive_evidence_improvement_candidate_manifest",
    "feature_label_refinement_options_matrix",
    "stability_improvement_plan_template",
    "baseline_outperformance_improvement_plan_template",
    "model_comparison_plan_template",
    "future_execution_candidate_template",
    "operator_review_summary_template",
]


class PredictiveEvidenceImprovementCandidateError(ValueError):
    """Raised when the improvement candidate violates its planning-only scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveEvidenceImprovementCandidateError(f"{field} mismatch")


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


def _source_readiness_review(readiness_review: dict | None) -> dict[str, Any]:
    source = (
        readiness_service.build_predictive_usefulness_acceptance_readiness_review_v1()
        if readiness_review is None
        else deepcopy(readiness_review)
    )
    readiness_service.validate_predictive_usefulness_acceptance_readiness_review_v1(
        source
    )
    _expect(
        source.get("predictive_usefulness_acceptance_readiness_review_digest"),
        EXPECTED_READINESS_REVIEW_DIGEST,
        "source readiness review digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_evidence_improvement_candidate_digest", None)
    return payload


def per_ticker_predictive_evidence_improvement_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker improvement candidate."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_readiness_entries"]:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "readiness_status": "NOT_READY",
            "improvement_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "improvement_note": (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG"
                if ticker == "META"
                else None
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_predictive_usefulness_acceptance_readiness_review_digest": (
                source["predictive_usefulness_acceptance_readiness_review_digest"]
            ),
            "source_per_ticker_predictive_usefulness_acceptance_readiness_digest": (
                source_entry[
                    "per_ticker_predictive_usefulness_acceptance_readiness_digest"
                ]
            ),
        }
        entry["per_ticker_predictive_evidence_improvement_candidate_digest"] = (
            per_ticker_predictive_evidence_improvement_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _improvement_themes() -> list[dict[str, str]]:
    return [
        {
            "theme_id": theme_id,
            "status": PLANNED_NOT_EXECUTED,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
            "evidence_classification": "NOT_ACCEPTANCE_EVIDENCE",
        }
        for theme_id in IMPROVEMENT_THEME_IDS
    ]


def _refinement_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "status": PLANNED_NOT_EXECUTED,
            "requires_separate_operator_review": True,
            "requires_separate_execution_approval": True,
        }
        for option_id in REFINEMENT_OPTION_IDS
    ]


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": output_name,
            "status": PLANNED_NOT_GENERATED,
            "label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate(source: dict[str, Any]) -> dict[str, Any]:
    facts = source["readiness_review_input_facts"]
    findings = {
        row["criterion_id"]: row["result"] for row in source["readiness_findings"]
    }
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "readiness_decision": readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY,
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
        "predictive_evidence_improvement_candidate_created": True,
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
        "predictive_usefulness_acceptance_readiness_review_digest": source[
            "predictive_usefulness_acceptance_readiness_review_digest"
        ],
        "predictive_usefulness_reassessment_review_package_digest": source[
            "predictive_usefulness_reassessment_review_package_digest"
        ],
        "predictive_usefulness_reassessment_candidate_review_package_digest": source[
            "predictive_usefulness_reassessment_candidate_review_package_digest"
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
        "predictive_evidence_improvement_objective": IMPROVEMENT_OBJECTIVE,
        "predictive_evidence_improvement_scope": IMPROVEMENT_SCOPE,
        "predictive_evidence_improvement_mode": PLANNED_NOT_EXECUTED,
        "predictive_evidence_improvement_authority_status": NOT_AUTHORIZED,
        "readiness_failure_summary": {
            "stability_consistency_required": findings[
                "stability_consistency_required"
            ],
            "baseline_outperformance_consistency_required": findings[
                "baseline_outperformance_consistency_required"
            ],
            "readiness_decision": source["readiness_decision"],
            "readiness_reason": source["readiness_reason"],
        },
        "evidence_basis": {
            "walk_forward_accuracy_range": facts["walk_forward_accuracy_range"],
            "oos_majority_accuracy": facts["oos_majority_accuracy"],
            "oos_previous_direction_accuracy": facts[
                "oos_previous_direction_accuracy"
            ],
            "oos_ticker_cross_sectional_accuracy": facts[
                "oos_ticker_cross_sectional_accuracy"
            ],
            "oos_brier_score": facts["oos_brier_score"],
            "leakage_status": facts["leakage_status"],
            "failed_leakage_controls": facts["failed_leakage_controls"],
        },
        "improvement_themes": _improvement_themes(),
        "refinement_options": _refinement_options(),
        "per_ticker_improvement_candidate_entries": _per_ticker_entries(source),
        "future_improvement_chain": deepcopy(FUTURE_IMPROVEMENT_CHAIN),
        "future_gates": deepcopy(FUTURE_GATES),
        "risk_controls": deepcopy(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("readiness_review_digest_bound", EXPECTED_READINESS_REVIEW_DIGEST, "predictive_usefulness_acceptance_readiness_review_digest"),
    ("reassessment_review_digest_bound", EXPECTED_REASSESSMENT_REVIEW_DIGEST, "predictive_usefulness_reassessment_review_package_digest"),
    ("candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, "predictive_usefulness_reassessment_candidate_review_package_digest"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_readiness_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("readiness_decision_not_ready", readiness_service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY, "readiness_decision"),
    ("readiness_reason_mixed_stability_and_insufficient_baseline_outperformance", "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", "readiness_reason"),
    ("stability_consistency_required_not_met", readiness_service.NOT_MET, "failure_stability_consistency_required"),
    ("baseline_outperformance_consistency_required_not_met", readiness_service.NOT_MET, "failure_baseline_outperformance_consistency_required"),
    ("predictive_evidence_improvement_candidate_created_true", True, "predictive_evidence_improvement_candidate_created"),
    ("improvement_candidate_scope_candidate_only", IMPROVEMENT_SCOPE, "predictive_evidence_improvement_scope"),
    ("improvement_authority_status_not_authorized", NOT_AUTHORIZED, "predictive_evidence_improvement_authority_status"),
    ("walk_forward_accuracy_range_bound", "0.498698 to 0.562842", "evidence_walk_forward_accuracy_range"),
    ("oos_performance_summary_bound", True, "oos_performance_summary_bound"),
    ("leakage_status_pass", PASS, "evidence_leakage_status"),
    ("failed_leakage_controls_zero", 0, "evidence_failed_leakage_controls"),
    ("improvement_themes_defined", IMPROVEMENT_THEME_IDS, "improvement_theme_ids"),
    ("refinement_options_defined", REFINEMENT_OPTION_IDS, "refinement_option_ids"),
    ("per_ticker_improvement_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_improvement_digests_present", True, "per_ticker_digests_valid"),
    ("future_improvement_chain_defined", FUTURE_IMPROVEMENT_CHAIN, "future_improvement_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("planned_outputs_not_generated", PLANNED_NOT_GENERATED, "planned_outputs_status"),
    ("planned_outputs_research_only", RESEARCH_ONLY_NON_ACTIONABLE, "planned_outputs_label"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("live_provider_transport_enabled_false", False, "live_provider_transport_enabled"),
    ("market_data_acquisition_performed_false", False, "market_data_acquisition_performed"),
    ("dataset_generation_performed_false", False, "dataset_generation_performed"),
    ("canonical_dataset_regenerated_false", False, "canonical_dataset_regenerated"),
    ("predictive_execution_rerun_performed_false", False, "predictive_execution_rerun_performed"),
    ("label_generation_rerun_performed_false", False, "label_generation_rerun_performed"),
    ("feature_matrix_rerun_performed_false", False, "feature_matrix_rerun_performed"),
    ("walk_forward_validation_rerun_performed_false", False, "walk_forward_validation_rerun_performed"),
    ("out_of_sample_evaluation_rerun_performed_false", False, "out_of_sample_evaluation_rerun_performed"),
    ("metrics_recomputation_performed_false", False, "metrics_recomputation_performed"),
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
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
]
REQUIRED_CHECK_IDS = [item[0] for item in CHECK_FIELD_SPECS]


def _derived_check_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    failure = candidate.get("readiness_failure_summary", {})
    evidence = candidate.get("evidence_basis", {})
    themes = candidate.get("improvement_themes", [])
    options = candidate.get("refinement_options", [])
    entries = candidate.get("per_ticker_improvement_candidate_entries", [])
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
        "per_ticker_digests_valid": isinstance(entries, list)
        and all(
            isinstance(row, dict)
            and isinstance(
                row.get("per_ticker_predictive_evidence_improvement_candidate_digest"),
                str,
            )
            and row["per_ticker_predictive_evidence_improvement_candidate_digest"]
            == per_ticker_predictive_evidence_improvement_candidate_digest_v1(row)
            for row in entries
        ),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(candidate)
    values.update(_derived_check_fields(candidate))
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
        "ready_for_operator_review": blockers == 0,
        "ready_for_feature_label_refinement_candidate": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_evidence_improvement_candidate_digest", None)
    return payload


def predictive_evidence_improvement_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the improvement candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_evidence_improvement_candidate_v1(
    *, readiness_review: dict | None = None
) -> dict:
    """Build a planning-only candidate from the exact not-ready decision."""
    source = _source_readiness_review(readiness_review)
    candidate = _base_candidate(source)
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["predictive_evidence_improvement_candidate_digest"] = (
        predictive_evidence_improvement_candidate_digest_v1(candidate)
    )
    validate_predictive_evidence_improvement_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
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
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed",
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
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveEvidenceImprovementCandidateError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveEvidenceImprovementCandidateError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveEvidenceImprovementCandidateError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveEvidenceImprovementCandidateError(
                    f"{current} must not be accepted"
                )
            if key == "predictive_evidence_improvement_authority_status" and item != NOT_AUTHORIZED:
                raise PredictiveEvidenceImprovementCandidateError(
                    f"{current} must remain {NOT_AUTHORIZED}"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_evidence_improvement_candidate_v1(
    candidate: dict,
) -> dict:
    """Validate exact bindings and reject execution or acceptance authority."""
    if not isinstance(candidate, dict):
        raise PredictiveEvidenceImprovementCandidateError(
            "predictive evidence improvement candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    expected_source = (
        readiness_service.build_predictive_usefulness_acceptance_readiness_review_v1()
    )
    expected_base = _base_candidate(expected_source)
    for field, expected in expected_base.items():
        _expect(candidate.get(field), expected, field)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidenceImprovementCandidateError(
            "candidate_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    _expect(checklist, expected_checklist, "candidate_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveEvidenceImprovementCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("predictive_evidence_improvement_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidenceImprovementCandidateError(
            "predictive evidence improvement candidate digest missing"
        )
    _expect(
        digest,
        predictive_evidence_improvement_candidate_digest_v1(candidate),
        "predictive_evidence_improvement_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_evidence_improvement_candidate_digest": digest,
        "source_readiness_review_digest": candidate[
            "predictive_usefulness_acceptance_readiness_review_digest"
        ],
        "per_ticker_improvement_entry_count": len(
            candidate["per_ticker_improvement_candidate_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_review": True,
        "predictive_evidence_improvement_authorized": False,
        "predictive_evidence_improvement_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_evidence_improvement_candidate_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized operator-facing improvement-candidate summary."""
    validation = validate_predictive_evidence_improvement_candidate_v1(candidate)
    failure = candidate["readiness_failure_summary"]
    evidence = candidate["evidence_basis"]
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Improvement Candidate Status",
        "",
        "## Title",
        "- Predictive Evidence Improvement Candidate v1.",
        "",
        "## Predictive Evidence Improvement Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['predictive_evidence_improvement_candidate_digest']}`",
        "",
        "## Source Acceptance Readiness Review",
        f"- Readiness-review digest: `{candidate['predictive_usefulness_acceptance_readiness_review_digest']}`",
        f"- Decision/reason: `{candidate['readiness_decision']}` / `{candidate['readiness_reason']}`",
        "",
        "## Readiness Failure Summary",
        f"- Stability/baseline criteria: `{failure['stability_consistency_required']}` / `{failure['baseline_outperformance_consistency_required']}`",
        "",
        "## Evidence Basis",
        f"- Walk-forward range: `{evidence['walk_forward_accuracy_range']}`",
        f"- OOS majority/previous/cross-sectional: `{evidence['oos_majority_accuracy']}` / `{evidence['oos_previous_direction_accuracy']}` / `{evidence['oos_ticker_cross_sectional_accuracy']}`",
        f"- Brier/leakage/failed controls: `{evidence['oos_brier_score']}` / `{evidence['leakage_status']}` / `{evidence['failed_leakage_controls']}`",
        "",
        "## Improvement Themes",
    ]
    lines.extend(f"- `{row['theme_id']}`" for row in candidate["improvement_themes"])
    lines.extend(["", "## Refinement Options"])
    lines.extend(f"- `{row['option_id']}`" for row in candidate["refinement_options"])
    lines.extend(
        [
            "",
            "## Per-Ticker Improvement Candidate Entries",
            f"- Entry count: `{len(candidate['per_ticker_improvement_candidate_entries'])}`; META preserves 913 records and every other ticker preserves 1003.",
            "",
            "## Future Improvement Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(candidate["future_improvement_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness/readiness: `{candidate['predictive_usefulness']}` / `{candidate['predictive_usefulness_acceptance_ready']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{candidate['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{candidate['runtime_use']}` / `{candidate['strategy_use']}` / `{candidate['paper_trading']}` / `{candidate['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This is a planning candidate only. No provider request, acquisition, generation, validation, evaluation, recomputation, model comparison, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- All themes, options, and outputs require separate review or approval and remain research-only non-actionable.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_improvement_candidate_v1(
    output_dir: str | Path,
    *,
    readiness_review: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical candidate JSON once without overwriting."""
    candidate = build_predictive_evidence_improvement_candidate_v1(
        readiness_review=readiness_review
    )
    validation = validate_predictive_evidence_improvement_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_improvement_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidenceImprovementCandidateError(
            "predictive evidence improvement candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidenceImprovementCandidateError(
            "predictive evidence improvement candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
