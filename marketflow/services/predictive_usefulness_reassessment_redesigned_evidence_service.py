"""Offline predictive-usefulness reassessment using reviewed redesigned evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_results_review_redesigned_labels_service as results_review


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_V1 = (
    "predictive_usefulness_reassessment_using_redesigned_evidence_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY"
)

RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_RESULTS_REVIEW_DIGEST = "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed"
EXPECTED_EXECUTION_DIGEST = "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_APPROVAL_DIGEST = "cc45d6692f1f249cc76554f7019f148c8510efedeade22adb3ccb3fcbc54fe96"
EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST = "e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_LABEL_RESULTS_REVIEW_DIGEST = "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"

EXPECTED_TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: 913 if ticker == "META" else 1003 for ticker in EXPECTED_TARGET_UNIVERSE}

DOMAIN_INTERPRETATIONS = {
    "evidence_integrity": ("All reviewed digests remain bound.", "SOURCE_EVIDENCE_INTEGRITY_PRESERVED"),
    "dataset_scope": ("The frozen 12-ticker research dataset remains unchanged.", "DATASET_SCOPE_RESEARCH_ONLY"),
    "label_integrity": ("Reviewed redesigned-label values remain digest-bound.", "LABEL_EVIDENCE_PRESERVED_NOT_REGENERATED"),
    "feature_integrity": ("Reviewed feature values remain digest-bound.", "FEATURE_EVIDENCE_PRESERVED_NOT_REGENERATED"),
    "matrix_integrity": ("The reviewed 143352-row feature-label matrix remains bound.", "MATRIX_EVIDENCE_PRESERVED_NOT_REBUILT"),
    "chronological_split_integrity": ("Four chronological folds and the 2025 OOS holdout remain the reviewed protocol.", "CHRONOLOGICAL_PROTOCOL_PRESERVED"),
    "walk_forward_stability": ("Walk-forward accuracy varied across four folds.", "MIXED_REQUIRES_ACCEPTANCE_READINESS_REVIEW"),
    "oos_baseline_outperformance": ("Cross-sectional OOS accuracy exceeded majority by 0.00309917.", "SMALL_EDGE_NOT_ACCEPTANCE_EVIDENCE"),
    "model_family_comparison": ("The local model matched majority and optional tree/ensemble families were unavailable.", "MODEL_EVIDENCE_MIXED_NOT_ACCEPTANCE_EVIDENCE"),
    "metric_family_consistency": ("Ten reviewed metric families remain internally bound.", "METRICS_REVIEWED_NOT_RECOMPUTED"),
    "calibration_and_brier_quality": ("Cross-sectional Brier score was marginally below majority.", "REQUIRES_ACCEPTANCE_READINESS_REVIEW"),
    "leakage_and_quality_controls": ("Leakage status is PASS with zero failed controls.", "PASS"),
    "per_ticker_cross_sectional_consistency": ("All 12 tickers have reviewed research-only evidence.", "CROSS_SECTIONAL_VARIATION_REQUIRES_OPERATOR_REVIEW"),
    "meta_limitation_awareness": ("META remains limited to 913 records.", "PRESERVED_REQUIRES_OPERATOR_AWARENESS"),
    "acceptance_boundary_review": ("This reassessment does not accept predictive usefulness.", "DO_NOT_ACCEPT_AT_REASSESSMENT_STAGE"),
    "profitability_boundary_review": ("Profitability was not evaluated and is not accepted.", "NOT_EVALUATED_NOT_ACCEPTED"),
    "runtime_boundary_review": ("Runtime, strategy, paper, and broker use remain unauthorized.", "NOT_AUTHORIZED"),
}

NEXT_CHAIN = [
    "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Predictive Usefulness Acceptance Ceremony, only if separately approved.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_acceptance_readiness_using_redesigned_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_approved",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "reassessment_does_not_accept_predictive_usefulness",
    "reassessment_does_not_create_acceptance_candidate",
    "reassessment_does_not_accept_profitability",
    "reassessment_does_not_authorize_runtime",
    "reassessment_does_not_authorize_strategy",
    "reassessment_does_not_authorize_paper_trading",
    "reassessment_does_not_authorize_broker_execution",
    "reassessment_does_not_generate_trade_recommendations",
    "reassessment_does_not_rerun_predictive_evidence",
    "reassessment_does_not_retrain_models",
    "reassessment_does_not_recompute_metrics",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "results_review_digest_bound", "execution_digest_bound", "matrix_digest_bound",
    "approval_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "records_digest_preserved", "label_values_digest_preserved", "feature_values_digest_preserved",
    "matrix_digest_preserved", "meta_913_preserved", "source_results_review_ready_true",
    "ready_for_reassessment_true", "reassessment_created_true", "reassessment_ready_true",
    "ready_for_acceptance_readiness_review_true", "acceptance_readiness_review_created_false",
    "acceptance_candidate_created_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "oos_cross_sectional_delta_bound",
    "local_model_delta_bound", "leakage_pass", "optional_model_unavailability_recorded",
    "domains_defined", "classification_conservative", "acceptance_recommendation_do_not_accept",
    "per_ticker_entries_12", "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_reassessment_false",
    "model_training_in_reassessment_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class PredictiveUsefulnessReassessmentRedesignedEvidenceError(ValueError):
    """Raised when the research-only reassessment package is invalid."""


def _domain_package() -> dict[str, dict[str, Any]]:
    return {
        domain: {
            "domain_status": "REASSESSED_RESEARCH_ONLY",
            "evidence_summary": summary,
            "reassessment_interpretation": interpretation,
            "acceptance_evidence": False,
            "research_only": True,
            "non_actionable": True,
        }
        for domain, (summary, interpretation) in DOMAIN_INTERPRETATIONS.items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_predictive_usefulness_reassessment_digest", None)
    return payload


def per_ticker_predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker reassessment entry."""
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
            "predictive_evidence_results_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_status": "REASSESSED_RESEARCH_ONLY",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
            "reassessment_note": (
                "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_predictive_usefulness_reassessment_digest"] = (
            per_ticker_predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_V1,
        "reassessment_status": PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_results_review_artifact_kind": results_review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "source_results_review_status": results_review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "additional_predictive_evidence_executed": True,
        "predictive_evidence_results_created": True,
        "source_metric_recomputation_performed": True,
        "source_model_training_performed": True,
        "metric_recomputation_performed_in_reassessment": False,
        "model_training_performed_in_reassessment": False,
        "predictive_evidence_execution_rerun_performed": False,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence": True,
        "predictive_usefulness_reassessment_created": True,
        "predictive_usefulness_reassessment_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence": True,
        "predictive_usefulness_acceptance_readiness_review_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
        "provider_requests_made_in_reassessment": False,
        "live_provider_transport_enabled_in_reassessment": False,
        "market_data_acquisition_performed_in_reassessment": False,
        "dataset_generation_performed_in_reassessment": False,
        "canonical_dataset_regenerated_in_reassessment": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
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
        "reassessment_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_classification": "WEAK_TO_MODEST_MIXED",
        "baseline_outperformance_classification": "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_classification": "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE",
        "stability_classification": "MIXED_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "calibration_classification": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "leakage_classification": PASS,
        "meta_limitation_classification": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "acceptance_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "next_recommended_gate": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE",
        "predictive_usefulness_accepted_by_reassessment": False,
        "profitability_accepted_by_reassessment": False,
        "runtime_authorized_by_reassessment": False,
        "reassessment_domains": _domain_package(),
        "per_ticker_reassessment_entries": _per_ticker_entries(),
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
        "message": "reassessment evidence matches" if status == PASS else "reassessment evidence mismatch",
    }


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = package.get("per_ticker_reassessment_entries", [])
    actuals = {
        "results_review_digest_bound": package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": package.get("feature_label_matrix_digest"),
        "approval_digest_bound": package.get("additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"),
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
        "source_results_review_ready_true": package.get("additional_predictive_evidence_results_review_ready"),
        "ready_for_reassessment_true": package.get("ready_for_predictive_usefulness_reassessment_using_redesigned_evidence"),
        "reassessment_created_true": package.get("predictive_usefulness_reassessment_created"),
        "reassessment_ready_true": package.get("predictive_usefulness_reassessment_ready"),
        "ready_for_acceptance_readiness_review_true": package.get("ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence"),
        "acceptance_readiness_review_created_false": package.get("predictive_usefulness_acceptance_readiness_review_created"),
        "acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created"),
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness"),
        "profitability_not_accepted": package.get("profitability"),
        "runtime_not_authorized": package.get("runtime_use"),
        "strategy_not_authorized": package.get("strategy_use"),
        "broker_not_authorized": package.get("broker_execution"),
        "trade_recommendations_false": package.get("trade_recommendations_generated"),
        "oos_cross_sectional_delta_bound": package.get("oos_cross_sectional_delta_vs_majority"),
        "local_model_delta_bound": package.get("oos_local_model_delta_vs_majority"),
        "leakage_pass": package.get("leakage_control_status"),
        "optional_model_unavailability_recorded": [package.get("optional_tree_family_status"), package.get("optional_ensemble_family_status")],
        "domains_defined": list(package.get("reassessment_domains", {})),
        "classification_conservative": package.get("reassessment_classification"),
        "acceptance_recommendation_do_not_accept": package.get("acceptance_recommendation"),
        "per_ticker_entries_12": len(entries),
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_predictive_usefulness_reassessment_digest"), str) and len(row["per_ticker_predictive_usefulness_reassessment_digest"]) == 64 for row in entries),
        "provider_requests_made_false": package.get("provider_requests_made_in_reassessment"),
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_reassessment"),
        "dataset_regeneration_false": package.get("dataset_generation_performed_in_reassessment"),
        "redesigned_label_regeneration_false": package.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": package.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": package.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_reassessment_false": package.get("metric_recomputation_performed_in_reassessment"),
        "model_training_in_reassessment_false": package.get("model_training_performed_in_reassessment"),
        "no_predictive_usefulness_acceptance_artifact_created": package.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": package.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": package.get("runtime_migration_approval_created"),
        "next_chain_defined": package.get("next_chain"),
        "next_gates_defined": package.get("next_gates"),
        "risk_controls_defined": package.get("risk_controls"),
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files"),
    }
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    expected = {
        "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "approval_digest_bound": EXPECTED_APPROVAL_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "label_values_digest_preserved": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest_preserved": EXPECTED_FEATURE_VALUES_DIGEST,
        "matrix_digest_preserved": EXPECTED_MATRIX_DIGEST,
        "meta_913_preserved": 913,
        "source_results_review_ready_true": True, "ready_for_reassessment_true": True,
        "reassessment_created_true": True, "reassessment_ready_true": True,
        "ready_for_acceptance_readiness_review_true": True,
        "acceptance_readiness_review_created_false": False, "acceptance_candidate_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED, "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED, "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED, "trade_recommendations_false": False,
        "oos_cross_sectional_delta_bound": "0.00309917", "local_model_delta_bound": "0.00000000",
        "leakage_pass": PASS, "optional_model_unavailability_recorded": [unavailable, unavailable],
        "domains_defined": list(DOMAIN_INTERPRETATIONS), "classification_conservative": "COMPLETED_RESEARCH_ONLY",
        "acceptance_recommendation_do_not_accept": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "per_ticker_entries_12": 12, "per_ticker_digests_present": True,
        "provider_requests_made_false": False, "market_data_acquisition_false": False,
        "dataset_regeneration_false": False, "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False, "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_reassessment_false": False, "model_training_in_reassessment_false": False,
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
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "predictive_usefulness_reassessment_ready": not failed,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence": not failed,
        "predictive_usefulness_acceptance_readiness_review_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop("predictive_usefulness_reassessment_using_redesigned_evidence_digest", None)
    return payload


def predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(
    reassessment: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the reassessment package."""
    return semantic_digest(_digest_payload(reassessment))


def build_predictive_usefulness_reassessment_using_redesigned_evidence_v1() -> dict:
    """Build the offline, research-only reassessment without recomputing evidence."""
    package = _base_package()
    checklist = _checklist(package)
    package["reassessment_checklist"] = checklist
    package["reassessment_summary"] = _summary(checklist)
    package["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] = (
        predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(package)
    )
    validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{field} must be false")


def validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(
    reassessment: dict,
) -> dict:
    """Validate evidence bindings, conservative classification, and closed gates."""
    if not isinstance(reassessment, dict):
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_V1,
        "reassessment_status": PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY,
        "source_results_review_artifact_kind": results_review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "source_results_review_status": results_review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "meta_record_count": 913, "non_meta_record_count": 1003,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "oos_cross_sectional_delta_vs_majority": "0.00309917",
        "oos_local_model_delta_vs_majority": "0.00000000",
        "leakage_control_status": PASS,
        "reassessment_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_classification": "WEAK_TO_MODEST_MIXED",
        "baseline_outperformance_classification": "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_classification": "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE",
        "stability_classification": "MIXED_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "calibration_classification": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "acceptance_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES, "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(reassessment.get(field), value, field)
    true_fields = (
        "created_offline", "research_only", "operator_review_required",
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "predictive_evidence_results_created",
        "source_metric_recomputation_performed", "source_model_training_performed",
        "additional_predictive_evidence_results_review_created",
        "additional_predictive_evidence_results_review_ready",
        "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence",
        "predictive_usefulness_reassessment_created", "predictive_usefulness_reassessment_ready",
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(reassessment.get(field), field)
    false_fields = (
        "metric_recomputation_performed_in_reassessment", "model_training_performed_in_reassessment",
        "predictive_evidence_execution_rerun_performed",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready", "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_reassessment", "live_provider_transport_enabled_in_reassessment",
        "market_data_acquisition_performed_in_reassessment", "dataset_generation_performed_in_reassessment",
        "canonical_dataset_regenerated_in_reassessment", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "predictive_usefulness_accepted_by_reassessment", "profitability_accepted_by_reassessment",
        "runtime_authorized_by_reassessment",
    )
    for field in false_fields:
        _expect_false(reassessment.get(field), field)

    domains = reassessment.get("reassessment_domains")
    if not isinstance(domains, dict) or set(domains) != set(DOMAIN_INTERPRETATIONS):
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment domains mismatch")
    for domain, value in domains.items():
        if not isinstance(value, dict):
            raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{domain} domain missing")
        _expect(value.get("domain_status"), "REASSESSED_RESEARCH_ONLY", f"{domain} domain_status")
        _expect_false(value.get("acceptance_evidence"), f"{domain} acceptance_evidence")
        _expect_true(value.get("research_only"), f"{domain} research_only")
        _expect_true(value.get("non_actionable"), f"{domain} non_actionable")
        if not value.get("evidence_summary") or not value.get("reassessment_interpretation"):
            raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{domain} evidence missing")

    entries = reassessment.get("per_ticker_reassessment_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("per-ticker entries mismatch")
    _expect([entry.get("ticker") for entry in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("source_results_review_digest"), EXPECTED_RESULTS_REVIEW_DIGEST, f"{ticker} source digest")
        for field in ("predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created"):
            _expect_false(entry.get(field), f"{ticker} {field}")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        digest = entry.get("per_ticker_predictive_usefulness_reassessment_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise PredictiveUsefulnessReassessmentRedesignedEvidenceError(f"{ticker} per-ticker digest missing")
        _expect(digest, per_ticker_predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(entry), f"{ticker} per-ticker digest")

    checklist = reassessment.get("reassessment_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment checklist failed")
    _expect(reassessment.get("reassessment_summary"), _summary(checklist), "reassessment summary")
    digest = reassessment.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment digest missing")
    _expect(digest, predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(reassessment), "reassessment digest")
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_VALID",
        "artifact_kind": reassessment["artifact_kind"],
        "reassessment_status": reassessment["reassessment_status"],
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": digest,
        **{key: reassessment["reassessment_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_predictive_usefulness_reassessment_using_redesigned_evidence_markdown_v1(
    reassessment: dict,
) -> str:
    """Render a sanitized Markdown view of the validated reassessment."""
    validation = validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(reassessment)
    sections = [
        ("Title", ["Predictive Usefulness Reassessment Using Redesigned Evidence"]),
        ("Predictive Usefulness Reassessment Using Redesigned Evidence", [f"Artifact/status: `{reassessment['artifact_kind']}` / `{reassessment['reassessment_status']}`.", f"Digest: `{validation['predictive_usefulness_reassessment_using_redesigned_evidence_digest']}`."]),
        ("Source Results Review", [f"Artifact/status: `{reassessment['source_results_review_artifact_kind']}` / `{reassessment['source_results_review_status']}`.", f"Digest: `{reassessment['additional_predictive_evidence_results_review_using_redesigned_labels_digest']}`."]),
        ("Bound Evidence", [f"Execution: `{reassessment['additional_predictive_evidence_execution_using_redesigned_labels_digest']}`.", f"Matrix: `{reassessment['feature_label_matrix_digest']}`.", f"Records: `{reassessment['records_digest']}`."]),
        ("Dataset and Universe", [f"Dataset/records: `{reassessment['dataset_name']}` / `{reassessment['total_canonical_record_count']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in reassessment["target_universe"]) + ".", "META remains `913`; each non-META ticker remains `1003`."]),
        ("Evidence Summary", [f"OOS majority/cross-sectional/local accuracy: `{reassessment['oos_majority_accuracy']} / {reassessment['oos_ticker_cross_sectional_accuracy']} / {reassessment['oos_regularized_local_model_accuracy']}`.", f"Cross-sectional/local delta versus majority: `{reassessment['oos_cross_sectional_delta_vs_majority']} / {reassessment['oos_local_model_delta_vs_majority']}`.", f"Leakage status/failed controls: `{reassessment['leakage_control_status']} / {reassessment['leakage_failed_control_count']}`."]),
        ("Reassessment Domains", [f"`{name}`: `{value['reassessment_interpretation']}`." for name, value in reassessment["reassessment_domains"].items()]),
        ("Reassessment Classification", [f"Signal: `{reassessment['predictive_signal_classification']}`.", f"Recommendation: `{reassessment['acceptance_recommendation']}`.", f"Next gate: `{reassessment['next_recommended_gate']}`."]),
        ("Per-Ticker Reassessment Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, digest `{row['per_ticker_predictive_usefulness_reassessment_digest']}`." for row in reassessment["per_ticker_reassessment_entries"]]),
        ("Next Chain", reassessment["next_chain"]),
        ("Next Gates", reassessment["next_gates"]),
        ("Risk Controls", reassessment["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; this reassessment creates no acceptance candidate."]),
        ("Profitability Boundary", ["Profitability remains not accepted and was not evaluated by reassessment."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{reassessment['reassessment_summary']['total_checks']} / {reassessment['reassessment_summary']['passed_checks']} / {reassessment['reassessment_summary']['failed_checks']} / {reassessment['reassessment_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, execution rerun, metric recomputation, model training, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Predictive Usefulness Reassessment Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_using_redesigned_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical reassessment JSON without overwriting an existing package."""
    package = build_predictive_usefulness_reassessment_using_redesigned_evidence_v1()
    validation = validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_reassessment_using_redesigned_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessReassessmentRedesignedEvidenceError("reassessment output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "reassessment_status": package["reassessment_status"],
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": validation[
            "predictive_usefulness_reassessment_using_redesigned_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
