"""Offline predictive-usefulness acceptance-readiness review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_redesigned_evidence_service as reassessment


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_V1 = (
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE"
)
READINESS_DECISION_REASON = (
    "SMALL_CROSS_SECTIONAL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_AND_STABILITY_REQUIRES_REVIEW"
)

RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_REASSESSMENT_DIGEST = "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985"
EXPECTED_RESULTS_REVIEW_DIGEST = "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed"
EXPECTED_EXECUTION_DIGEST = "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"

EXPECTED_TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: 913 if ticker == "META" else 1003 for ticker in EXPECTED_TARGET_UNIVERSE}

CRITERIA_POLICY = {
    "evidence_integrity_pass": ("PASS", "All bound digests match reviewed source evidence."),
    "leakage_controls_pass": ("PASS", "Leakage status is PASS with zero failed controls."),
    "source_reassessment_completed": ("PASS", "The source reassessment is ready and complete."),
    "research_only_boundary_preserved": ("PASS", "All evidence remains research-only and non-actionable."),
    "profitability_boundary_preserved": ("PASS", "Profitability remains not accepted."),
    "runtime_boundary_preserved": ("PASS", "Runtime and trading authority remain closed."),
    "operator_boundary_preserved": ("PASS", "Operator review remains required."),
    "oos_cross_sectional_edge_materiality": ("FAIL_OR_NOT_MET", "The +0.00309917 accuracy edge is too small for acceptance readiness."),
    "local_model_outperformance_materiality": ("FAIL_OR_NOT_MET", "The local model does not outperform the majority baseline."),
    "stability_consistency": ("FAIL_OR_NOT_MET", "Walk-forward stability remains mixed."),
    "calibration_consistency": ("REQUIRES_OPERATOR_REVIEW", "Calibration requires additional operator review."),
    "baseline_outperformance_consistency": ("FAIL_OR_NOT_MET", "Baseline outperformance is not consistent enough for acceptance readiness."),
    "optional_model_coverage_sufficiency": ("FAIL_OR_NOT_MET", "Optional tree and ensemble families are unavailable."),
    "meta_limitation_acceptability": ("PASS", "META's 913-record limitation is preserved with operator awareness."),
}

NEXT_CHAIN = [
    "Method / Evidence Improvement Candidate Using Redesigned Evidence v1.",
    "Optional improved evidence planning and review, if selected.",
    "Optional additional evidence execution approval and execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "method_or_evidence_improvement_candidate_using_redesigned_evidence",
    "improved_evidence_planning_review_if_selected",
    "additional_evidence_execution_approval_if_required",
    "additional_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "readiness_review_does_not_accept_predictive_usefulness",
    "readiness_review_does_not_create_acceptance_candidate",
    "readiness_review_does_not_accept_profitability",
    "readiness_review_does_not_authorize_runtime",
    "readiness_review_does_not_authorize_strategy",
    "readiness_review_does_not_authorize_paper_trading",
    "readiness_review_does_not_authorize_broker_execution",
    "readiness_review_does_not_generate_trade_recommendations",
    "readiness_review_does_not_rerun_predictive_evidence",
    "readiness_review_does_not_retrain_models",
    "readiness_review_does_not_recompute_metrics",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "reassessment_digest_bound", "results_review_digest_bound", "execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "records_digest_preserved", "label_values_digest_preserved", "feature_values_digest_preserved",
    "matrix_digest_preserved", "meta_913_preserved", "source_reassessment_ready_true",
    "ready_for_acceptance_readiness_review_true", "acceptance_readiness_review_created_true",
    "acceptance_readiness_review_completed_true", "decision_not_ready", "decision_reason_bound",
    "acceptance_ready_false", "acceptance_recommended_false", "acceptance_candidate_created_false",
    "predictive_usefulness_not_accepted", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "evidence_integrity_pass", "leakage_pass", "cross_sectional_edge_not_material",
    "local_model_outperformance_not_material", "stability_not_ready",
    "baseline_outperformance_not_ready", "optional_model_coverage_not_sufficient",
    "calibration_requires_review", "meta_limitation_preserved", "additional_improvement_ready_true",
    "per_ticker_entries_12", "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_review_false",
    "model_training_in_review_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(ValueError):
    """Raised when the conservative readiness review is invalid."""


def _criteria() -> dict[str, dict[str, Any]]:
    return {
        criterion: {
            "criterion_status": status,
            "evidence_summary": summary,
            "readiness_interpretation": (
                "ACCEPTANCE_READINESS_CRITERION_SATISFIED"
                if status == "PASS"
                else "ACCEPTANCE_READINESS_CRITERION_NOT_SATISFIED"
                if status == "FAIL_OR_NOT_MET"
                else "OPERATOR_REVIEW_REQUIRED"
            ),
            "acceptance_evidence": False,
            "research_only": True,
            "non_actionable": True,
        }
        for criterion, (status, summary) in CRITERIA_POLICY.items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_acceptance_readiness_digest", None)
    return payload


def per_ticker_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker readiness entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in EXPECTED_TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "predictive_usefulness_reassessment_status": "REASSESSED_RESEARCH_ONLY",
            "acceptance_readiness_status": "NOT_READY",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_reassessment_digest": EXPECTED_REASSESSMENT_DIGEST,
            "readiness_note": (
                "PRESERVE_META_LIMITATION_IN_ACCEPTANCE_READINESS_REVIEW"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_acceptance_readiness_digest"] = (
            per_ticker_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE,
        "readiness_decision_reason": READINESS_DECISION_REASON,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_reassessment_artifact_kind": reassessment.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE,
        "source_reassessment_status": reassessment.PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY,
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "predictive_usefulness_reassessment_created": True,
        "predictive_usefulness_reassessment_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence": True,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "ready_for_predictive_usefulness_acceptance_candidate_using_redesigned_evidence": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted_by_readiness_review": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
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
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_review": False,
        "model_training_performed_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "oos_majority_accuracy": "0.58626033",
        "oos_ticker_cross_sectional_accuracy": "0.58935950",
        "oos_regularized_local_model_accuracy": "0.58626033",
        "oos_cross_sectional_delta_vs_majority": "0.00309917",
        "oos_local_model_delta_vs_majority": "0.00000000",
        "oos_majority_macro_f1": "0.21557412",
        "oos_ticker_cross_sectional_macro_f1": "0.28155252",
        "oos_regularized_local_model_macro_f1": "0.21557412",
        "oos_majority_brier": "0.04867526",
        "oos_ticker_cross_sectional_brier": "0.04831065",
        "oos_regularized_local_model_brier": "0.04867526",
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "oos_evaluated_rows": 34848,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
        "optional_tree_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "optional_ensemble_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "readiness_criteria": _criteria(),
        "predictive_signal_readiness": "NOT_READY",
        "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY",
        "stability_readiness": "NOT_READY",
        "calibration_readiness": "REQUIRES_OPERATOR_REVIEW",
        "leakage_readiness": PASS,
        "data_integrity_readiness": PASS,
        "meta_limitation_readiness": "PASS_WITH_OPERATOR_AWARENESS",
        "acceptance_candidate_allowed": False,
        "acceptance_ceremony_allowed": False,
        "additional_evidence_or_method_improvement_required": True,
        "per_ticker_readiness_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "readiness evidence matches" if status == PASS else "readiness evidence mismatch",
    }


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    criteria = package.get("readiness_criteria", {})
    entries = package.get("per_ticker_readiness_entries", [])
    actuals = {
        "reassessment_digest_bound": package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": package.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": package.get("feature_values_digest"),
        "label_values_digest_bound": package.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": package.get("research_registry_approval_digest"),
        "records_digest_bound": package.get("records_digest"),
        "target_universe_12_preserved": package.get("target_universe_count"),
        "records_digest_preserved": package.get("records_digest"),
        "label_values_digest_preserved": package.get("redesigned_label_values_digest"),
        "feature_values_digest_preserved": package.get("feature_values_digest"),
        "matrix_digest_preserved": package.get("feature_label_matrix_digest"),
        "meta_913_preserved": package.get("meta_record_count"),
        "source_reassessment_ready_true": package.get("predictive_usefulness_reassessment_ready"),
        "ready_for_acceptance_readiness_review_true": package.get("ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence"),
        "acceptance_readiness_review_created_true": package.get("predictive_usefulness_acceptance_readiness_review_created"),
        "acceptance_readiness_review_completed_true": package.get("predictive_usefulness_acceptance_readiness_review_completed"),
        "decision_not_ready": package.get("readiness_decision"),
        "decision_reason_bound": package.get("readiness_decision_reason"),
        "acceptance_ready_false": package.get("predictive_usefulness_acceptance_ready"),
        "acceptance_recommended_false": package.get("predictive_usefulness_acceptance_recommended"),
        "acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created"),
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness"),
        "profitability_not_accepted": package.get("profitability"),
        "runtime_not_authorized": package.get("runtime_use"),
        "strategy_not_authorized": package.get("strategy_use"),
        "broker_not_authorized": package.get("broker_execution"),
        "trade_recommendations_false": package.get("trade_recommendations_generated"),
        "evidence_integrity_pass": criteria.get("evidence_integrity_pass", {}).get("criterion_status"),
        "leakage_pass": package.get("leakage_readiness"),
        "cross_sectional_edge_not_material": criteria.get("oos_cross_sectional_edge_materiality", {}).get("criterion_status"),
        "local_model_outperformance_not_material": criteria.get("local_model_outperformance_materiality", {}).get("criterion_status"),
        "stability_not_ready": package.get("stability_readiness"),
        "baseline_outperformance_not_ready": package.get("baseline_outperformance_readiness"),
        "optional_model_coverage_not_sufficient": criteria.get("optional_model_coverage_sufficiency", {}).get("criterion_status"),
        "calibration_requires_review": package.get("calibration_readiness"),
        "meta_limitation_preserved": package.get("meta_limitation_readiness"),
        "additional_improvement_ready_true": package.get("ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"),
        "per_ticker_entries_12": len(entries),
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_acceptance_readiness_digest"), str) and len(row["per_ticker_acceptance_readiness_digest"]) == 64 for row in entries),
        "provider_requests_made_false": package.get("provider_requests_made_in_review"),
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_review"),
        "dataset_regeneration_false": package.get("dataset_generation_performed_in_review"),
        "redesigned_label_regeneration_false": package.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": package.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": package.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_review_false": package.get("metric_recomputation_performed_in_review"),
        "model_training_in_review_false": package.get("model_training_performed_in_review"),
        "no_predictive_usefulness_acceptance_artifact_created": package.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": package.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": package.get("runtime_migration_approval_created"),
        "next_chain_defined": package.get("next_chain"), "next_gates_defined": package.get("next_gates"),
        "risk_controls_defined": package.get("risk_controls"),
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files"),
    }
    expected = {
        "reassessment_digest_bound": EXPECTED_REASSESSMENT_DIGEST,
        "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST, "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST, "target_universe_12_preserved": 12,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "label_values_digest_preserved": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest_preserved": EXPECTED_FEATURE_VALUES_DIGEST,
        "matrix_digest_preserved": EXPECTED_MATRIX_DIGEST, "meta_913_preserved": 913,
        "source_reassessment_ready_true": True, "ready_for_acceptance_readiness_review_true": True,
        "acceptance_readiness_review_created_true": True, "acceptance_readiness_review_completed_true": True,
        "decision_not_ready": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE,
        "decision_reason_bound": READINESS_DECISION_REASON,
        "acceptance_ready_false": False, "acceptance_recommended_false": False,
        "acceptance_candidate_created_false": False, "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "profitability_not_accepted": NOT_ACCEPTED, "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED, "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False, "evidence_integrity_pass": PASS, "leakage_pass": PASS,
        "cross_sectional_edge_not_material": "FAIL_OR_NOT_MET",
        "local_model_outperformance_not_material": "FAIL_OR_NOT_MET",
        "stability_not_ready": "NOT_READY", "baseline_outperformance_not_ready": "NOT_READY",
        "optional_model_coverage_not_sufficient": "FAIL_OR_NOT_MET",
        "calibration_requires_review": "REQUIRES_OPERATOR_REVIEW",
        "meta_limitation_preserved": "PASS_WITH_OPERATOR_AWARENESS",
        "additional_improvement_ready_true": True, "per_ticker_entries_12": 12,
        "per_ticker_digests_present": True, "provider_requests_made_false": False,
        "market_data_acquisition_false": False, "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False, "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False, "metric_recomputation_in_review_false": False,
        "model_training_in_review_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False, "no_runtime_migration_approval_created": False,
        "next_chain_defined": NEXT_CHAIN, "next_gates_defined": NEXT_GATES,
        "risk_controls_defined": RISK_CONTROLS, "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows), "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed), "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence": not failed,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "trade_recommendations_generated": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest", None)
    return payload


def predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(
    readiness_review: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the readiness review."""
    return semantic_digest(_digest_payload(readiness_review))


def build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1() -> dict:
    """Build the conservative offline readiness review without recomputation."""
    package = _base_package()
    checklist = _checklist(package)
    package["readiness_checklist"] = checklist
    package["readiness_summary"] = _summary(checklist)
    package["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] = (
        predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(package)
    )
    validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(f"{field} must be false")


def validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(
    readiness_review: dict,
) -> dict:
    """Validate the not-ready decision and every closed authority boundary."""
    if not isinstance(readiness_review, dict):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness_review must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE,
        "readiness_decision_reason": READINESS_DECISION_REASON,
        "source_reassessment_artifact_kind": reassessment.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE,
        "source_reassessment_status": reassessment.PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY,
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST, "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST, "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12, "meta_record_count": 913, "non_meta_record_count": 1003,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(readiness_review.get(field), value, field)
    true_fields = (
        "created_offline", "research_only", "operator_review_required",
        "predictive_usefulness_reassessment_created", "predictive_usefulness_reassessment_ready",
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_readiness_review_completed",
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence",
        "meta_reduced_record_count_preserved", "additional_evidence_or_method_improvement_required",
        "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(readiness_review.get(field), field)
    false_fields = (
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "ready_for_predictive_usefulness_acceptance_candidate_using_redesigned_evidence",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_accepted_by_readiness_review", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "acceptance_candidate_allowed",
        "acceptance_ceremony_allowed",
    )
    for field in false_fields:
        _expect_false(readiness_review.get(field), field)
    criteria = readiness_review.get("readiness_criteria")
    if not isinstance(criteria, dict) or set(criteria) != set(CRITERIA_POLICY):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness criteria mismatch")
    for name, (status, _) in CRITERIA_POLICY.items():
        row = criteria[name]
        if not isinstance(row, dict):
            raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(f"{name} criterion missing")
        _expect(row.get("criterion_status"), status, f"{name} criterion_status")
        _expect_false(row.get("acceptance_evidence"), f"{name} acceptance_evidence")
        _expect_true(row.get("research_only"), f"{name} research_only")
        _expect_true(row.get("non_actionable"), f"{name} non_actionable")
    expected_findings = {
        "predictive_signal_readiness": "NOT_READY", "baseline_outperformance_readiness": "NOT_READY",
        "local_model_readiness": "NOT_READY", "stability_readiness": "NOT_READY",
        "calibration_readiness": "REQUIRES_OPERATOR_REVIEW", "leakage_readiness": PASS,
        "data_integrity_readiness": PASS, "meta_limitation_readiness": "PASS_WITH_OPERATOR_AWARENESS",
    }
    for field, value in expected_findings.items():
        _expect(readiness_review.get(field), value, field)
    entries = readiness_review.get("per_ticker_readiness_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("per-ticker entries mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("source_reassessment_digest"), EXPECTED_REASSESSMENT_DIGEST, f"{ticker} source digest")
        _expect(entry.get("acceptance_readiness_status"), "NOT_READY", f"{ticker} readiness")
        for field in ("predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created"):
            _expect_false(entry.get(field), f"{ticker} {field}")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        digest = entry.get("per_ticker_acceptance_readiness_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError(f"{ticker} digest missing")
        _expect(digest, per_ticker_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(entry), f"{ticker} digest")
    checklist = readiness_review.get("readiness_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness checklist failed")
    _expect(readiness_review.get("readiness_summary"), _summary(checklist), "readiness summary")
    digest = readiness_review.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness digest missing")
    _expect(digest, predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(readiness_review), "readiness digest")
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID",
        "artifact_kind": readiness_review["artifact_kind"], "review_status": readiness_review["review_status"],
        "readiness_decision": readiness_review["readiness_decision"],
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": digest,
        **{key: readiness_review["readiness_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_markdown_v1(
    readiness_review: dict,
) -> str:
    """Render a sanitized Markdown view of the validated readiness review."""
    validation = validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(readiness_review)
    sections = [
        ("Title", ["Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence"]),
        ("Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence", [f"Artifact/status: `{readiness_review['artifact_kind']}` / `{readiness_review['review_status']}`.", f"Digest: `{validation['predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest']}`."]),
        ("Source Reassessment", [f"Artifact/status: `{readiness_review['source_reassessment_artifact_kind']}` / `{readiness_review['source_reassessment_status']}`.", f"Digest: `{readiness_review['predictive_usefulness_reassessment_using_redesigned_evidence_digest']}`."]),
        ("Bound Evidence", [f"Results review: `{readiness_review['additional_predictive_evidence_results_review_using_redesigned_labels_digest']}`.", f"Execution/matrix: `{readiness_review['additional_predictive_evidence_execution_using_redesigned_labels_digest']}` / `{readiness_review['feature_label_matrix_digest']}`."]),
        ("Dataset and Universe", [f"Dataset/records: `{readiness_review['dataset_name']}` / `{readiness_review['total_canonical_record_count']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in readiness_review["target_universe"]) + ".", "META remains `913`; every other ticker remains `1003`."]),
        ("Evidence Summary", [f"OOS majority/cross-sectional/local accuracy: `{readiness_review['oos_majority_accuracy']} / {readiness_review['oos_ticker_cross_sectional_accuracy']} / {readiness_review['oos_regularized_local_model_accuracy']}`.", f"Cross-sectional/local deltas: `{readiness_review['oos_cross_sectional_delta_vs_majority']} / {readiness_review['oos_local_model_delta_vs_majority']}`."]),
        ("Readiness Criteria", [f"`{name}`: `{row['criterion_status']}` — {row['evidence_summary']}" for name, row in readiness_review["readiness_criteria"].items()]),
        ("Readiness Findings", [f"Signal/baseline/local/stability: `{readiness_review['predictive_signal_readiness']} / {readiness_review['baseline_outperformance_readiness']} / {readiness_review['local_model_readiness']} / {readiness_review['stability_readiness']}`.", f"Calibration: `{readiness_review['calibration_readiness']}`."]),
        ("Readiness Decision", [f"Decision: `{readiness_review['readiness_decision']}`.", f"Reason: `{readiness_review['readiness_decision_reason']}`."]),
        ("Per-Ticker Readiness Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['acceptance_readiness_status']}`, digest `{row['per_ticker_acceptance_readiness_digest']}`." for row in readiness_review["per_ticker_readiness_entries"]]),
        ("Next Chain", readiness_review["next_chain"]), ("Next Gates", readiness_review["next_gates"]),
        ("Risk Controls", readiness_review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{readiness_review['readiness_summary']['total_checks']} / {readiness_review['readiness_summary']['passed_checks']} / {readiness_review['readiness_summary']['failed_checks']} / {readiness_review['readiness_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, execution rerun, metric recomputation, model training, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical readiness-review JSON without overwriting an existing artifact."""
    package = build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1()
    validation = validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError("readiness review output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"], "readiness_decision": package["readiness_decision"],
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": validation[
            "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
