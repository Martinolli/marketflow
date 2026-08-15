"""Offline candidate for a future additional predictive evidence execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_chain_candidate_service as chain_service
from marketflow.services import additional_predictive_evidence_chain_candidate_operator_review_service as review_service


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_V1 = (
    "additional_predictive_evidence_execution_candidate_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "41e7b4db107a056790b1caa749b789d434698c6416333328297b894fa0832c82"
)
EXPECTED_CHAIN_CANDIDATE_DIGEST = (
    review_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_DIGEST
)
TARGET_UNIVERSE = list(chain_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(chain_service.EXPECTED_RECORD_COUNTS)
APPROVED_REGISTRY_METADATA = deepcopy(chain_service.APPROVED_REGISTRY_METADATA)

NOT_ACCEPTED = chain_service.NOT_ACCEPTED
NOT_AUTHORIZED = chain_service.NOT_AUTHORIZED
PLANNED_NOT_AUTHORIZED = chain_service.PLANNED_NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = chain_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = chain_service.PLANNED_NOT_GENERATED
PLANNED_FOR_EXECUTION_CANDIDATE_ONLY = "PLANNED_FOR_EXECUTION_CANDIDATE_ONLY"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_COMPUTED = "PLANNED_NOT_COMPUTED"
NOT_AUTHORIZED_FOR_EXECUTION = "NOT_AUTHORIZED_FOR_EXECUTION"
PLANNED_NOT_EVALUATED = "PLANNED_NOT_EVALUATED"
NOT_ACCEPTANCE_EVIDENCE = "NOT_ACCEPTANCE_EVIDENCE"
REVIEWED_READY_FOR_OPERATOR_ASSESSMENT = "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXECUTION_CANDIDATE_OBJECTIVE = (
    "PREPARE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REGISTRY_APPROVED_EXPANDED_UNIVERSE"
)
EXECUTION_CANDIDATE_SCOPE = "EXECUTION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
EXECUTION_MODE = PLANNED_NOT_EXECUTED

PLANNED_LABEL_FAMILIES = list(chain_service.PLANNED_LABEL_FAMILY_IDS)
PLANNED_FEATURE_FAMILIES = list(chain_service.PLANNED_FEATURE_FAMILY_IDS)
PLANNED_EXECUTION_PROTOCOL_IDS = list(chain_service.PLANNED_EVALUATION_PROTOCOL)

PLANNED_SPLIT_PROFILE = {
    "planned_training_window": "2022-01-01 to 2023-12-31",
    "planned_validation_window": "2024-01-01 to 2024-12-31",
    "planned_out_of_sample_window": "2025-01-01 to 2025-12-31",
    "planned_embargo_gap_policy": "TO_BE_APPLIED_DURING_EXECUTION_IF_APPROVED",
    "planned_walk_forward_policy": (
        "EXPANDING_OR_ROLLING_WINDOWS_TO_BE_FINALIZED_IN_EXECUTION_APPROVAL"
    ),
}

PLANNED_METRIC_FAMILY_IDS = [
    "classification_metrics",
    "regression_metrics",
    "calibration_metrics",
    "ranking_lift_metrics",
    "baseline_comparison_metrics",
    "stability_metrics",
    "false_positive_false_negative_metrics",
    "leakage_control_metrics",
    "data_quality_metrics",
]

PLANNED_BASELINE_IDS = [
    "majority_class_baseline",
    "random_baseline",
    "previous_direction_baseline",
    "zero_return_baseline",
    "buy_hold_reference_only",
    "ticker_cross_sectional_baseline",
]

FUTURE_EXECUTION_OUTPUT_IDS = [
    "additional_predictive_evidence_execution_manifest",
    "label_generation_manifest",
    "label_distribution_report",
    "feature_matrix_manifest",
    "feature_quality_report",
    "walk_forward_results_report",
    "out_of_sample_results_report",
    "baseline_comparison_report",
    "calibration_report",
    "stability_analysis_report",
    "false_positive_false_negative_report",
    "leakage_control_report",
    "data_quality_report",
    "execution_digest_manifest",
    "operator_review_summary_template",
]

FUTURE_EXECUTION_CHAIN = [
    "Additional predictive evidence execution candidate operator review package.",
    "Additional predictive evidence execution approval ceremony, if required.",
    "Additional predictive evidence execution.",
    "Additional predictive evidence results review package.",
    "Predictive usefulness reassessment candidate.",
    "Predictive usefulness reassessment candidate review package.",
    "Predictive usefulness acceptance readiness review.",
    "Predictive usefulness acceptance ceremony, only if evidence is sufficient.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "additional_predictive_evidence_execution_candidate_operator_review",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_candidate",
    "predictive_usefulness_reassessment_review",
    "predictive_usefulness_acceptance_readiness_review",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = list(chain_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "chain_candidate_review_digest_bound",
    "chain_candidate_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_chain_review_universe",
    "registry_approval_created_true",
    "research_registry_approved_true",
    "additional_predictive_evidence_chain_candidate_created_true",
    "additional_predictive_evidence_chain_candidate_review_created_true",
    "additional_predictive_evidence_execution_candidate_created_true",
    "execution_candidate_scope_candidate_only",
    "execution_authority_status_not_authorized",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "planned_labels_7",
    "planned_features_10",
    "planned_execution_protocol_defined",
    "planned_split_profile_defined",
    "planned_metric_families_defined",
    "planned_baselines_defined",
    "future_execution_outputs_defined",
    "future_execution_outputs_not_generated",
    "future_execution_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "dataset_generation_performed_false",
    "canonical_dataset_regenerated_false",
    "label_generation_authorized_false",
    "label_generation_performed_false",
    "feature_matrix_generation_authorized_false",
    "feature_matrix_generation_performed_false",
    "walk_forward_validation_authorized_false",
    "walk_forward_validation_performed_false",
    "out_of_sample_evaluation_authorized_false",
    "out_of_sample_evaluation_performed_false",
    "baseline_comparison_authorized_false",
    "baseline_comparison_performed_false",
    "signal_quality_metrics_performed_false",
    "stability_analysis_performed_false",
    "leakage_control_review_performed_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "additional_predictive_evidence_results_created_false",
    "predictive_experiment_rerun_authorized_false",
    "predictive_experiment_rerun_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "no_additional_predictive_evidence_execution_artifact_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

FORBIDDEN_ARTIFACT_VALUES = set(chain_service.FORBIDDEN_ARTIFACT_VALUES) | {
    "LABEL_GENERATION_EXECUTED",
    "FEATURE_MATRIX_GENERATION_EXECUTED",
    "WALK_FORWARD_VALIDATION_EXECUTED",
    "OUT_OF_SAMPLE_EVALUATION_EXECUTED",
}


class AdditionalPredictiveEvidenceExecutionCandidateError(ValueError):
    """Raised when the execution candidate violates its planning-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            f"{field} must be false"
        )


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


def _execution_profile() -> dict[str, Any]:
    return {
        "dataset_binding": "expanded_universe_canonical_dataset_v1",
        "records_digest": chain_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "timeframe": "1d",
        "source_profile": "RTH_FULL_SESSION_1D",
        "execution_profile_status": PLANNED_NOT_EXECUTED,
    }


def _planned_labels() -> list[dict[str, Any]]:
    return [
        {
            "label_family": label,
            "execution_candidate_status": PLANNED_FOR_EXECUTION_CANDIDATE_ONLY,
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for label in PLANNED_LABEL_FAMILIES
    ]


def _planned_features() -> list[dict[str, Any]]:
    return [
        {
            "feature_family": feature,
            "execution_candidate_status": PLANNED_FOR_EXECUTION_CANDIDATE_ONLY,
            "feature_matrix_generation_authorized": False,
            "feature_matrix_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for feature in PLANNED_FEATURE_FAMILIES
    ]


def _planned_protocol() -> list[dict[str, Any]]:
    return [
        {"protocol_item": item, "execution_status": PLANNED_NOT_EXECUTED}
        for item in PLANNED_EXECUTION_PROTOCOL_IDS
    ]


def _planned_metrics() -> list[dict[str, Any]]:
    return [
        {
            "metric_family": metric,
            "computation_status": PLANNED_NOT_COMPUTED,
            "execution_authority_status": NOT_AUTHORIZED_FOR_EXECUTION,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for metric in PLANNED_METRIC_FAMILY_IDS
    ]


def _planned_baselines() -> list[dict[str, Any]]:
    return [
        {
            "baseline": baseline,
            "evaluation_status": PLANNED_NOT_EVALUATED,
            "acceptance_evidence_status": NOT_ACCEPTANCE_EVIDENCE,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for baseline in PLANNED_BASELINE_IDS
    ]


def _future_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in FUTURE_EXECUTION_OUTPUT_IDS
    ]


def per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one ticker execution-candidate entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_additional_predictive_evidence_execution_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": chain_service.registry_approval.APPROVED_FOR_RESEARCH_REGISTRY_ONLY,
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "additional_predictive_evidence_chain_status": REVIEWED_READY_FOR_OPERATOR_ASSESSMENT,
            "additional_predictive_evidence_execution_candidate_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "label_generation_status": PLANNED_NOT_AUTHORIZED,
            "feature_matrix_generation_status": PLANNED_NOT_AUTHORIZED,
            "walk_forward_validation_status": PLANNED_NOT_AUTHORIZED,
            "out_of_sample_evaluation_status": PLANNED_NOT_AUTHORIZED,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_additional_predictive_evidence_chain_candidate_review_digest": EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_additional_predictive_evidence_chain_candidate_digest": EXPECTED_CHAIN_CANDIDATE_DIGEST,
        }
        entry["per_ticker_additional_predictive_evidence_execution_candidate_digest"] = (
            per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_generation_performed": False,
        "canonical_dataset_regenerated": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_approved": True,
        "registry_approval_created": True,
        "ready_for_additional_predictive_evidence_chain_candidate": True,
        "additional_predictive_evidence_chain_candidate_created": True,
        "additional_predictive_evidence_chain_candidate_review_created": True,
        "additional_predictive_evidence_chain_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_review_created": False,
        "additional_predictive_evidence_execution_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "feature_matrix_generation_authorized": False,
        "feature_matrix_generation_performed": False,
        "walk_forward_validation_authorized": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_authorized": False,
        "out_of_sample_evaluation_performed": False,
        "baseline_comparison_authorized": False,
        "baseline_comparison_performed": False,
        "signal_quality_metrics_authorized": False,
        "signal_quality_metrics_performed": False,
        "stability_analysis_authorized": False,
        "stability_analysis_performed": False,
        "leakage_control_review_authorized": False,
        "leakage_control_review_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
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
        "operator_review_required": True,
        "additional_predictive_evidence_chain_candidate_review_package_digest": EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_chain_candidate_digest": EXPECTED_CHAIN_CANDIDATE_DIGEST,
        "research_registry_approval_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "research_registry_candidate_review_package_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_registry_candidate_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "canonical_dataset_freeze_digest": chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": chain_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": chain_service.EXPECTED_RECORDS_DIGEST,
        "acquisition_generation_freeze_digest": chain_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "corporate_action_authority_approval_digest": chain_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": chain_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": chain_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "approved_registry_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "per_ticker_execution_candidate_entries": _per_ticker_entries(),
        "additional_predictive_evidence_execution_candidate_objective": EXECUTION_CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": EXECUTION_CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
        "additional_predictive_evidence_execution_authority_status": NOT_AUTHORIZED,
        "execution_candidate_profile": _execution_profile(),
        "planned_label_set": _planned_labels(),
        "planned_feature_set": _planned_features(),
        "planned_execution_protocol": _planned_protocol(),
        "planned_split_profile": deepcopy(PLANNED_SPLIT_PROFILE),
        "planned_metric_families": _planned_metrics(),
        "planned_baselines": _planned_baselines(),
        "future_execution_outputs": _future_outputs(),
        "future_execution_chain": list(FUTURE_EXECUTION_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "additional_predictive_evidence_execution_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    counts = candidate.get("per_ticker_record_counts", {})
    outputs = candidate.get("future_execution_outputs", [])
    return [
        _check("chain_candidate_review_digest_bound", EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("additional_predictive_evidence_chain_candidate_review_package_digest")),
        _check("chain_candidate_digest_bound", EXPECTED_CHAIN_CANDIDATE_DIGEST, candidate.get("additional_predictive_evidence_chain_candidate_digest")),
        _check("research_registry_approval_digest_bound", chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, candidate.get("research_registry_approval_digest")),
        _check("canonical_dataset_freeze_digest_bound", chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, candidate.get("canonical_dataset_freeze_digest")),
        _check("canonical_dataset_generation_digest_bound", chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, candidate.get("canonical_dataset_generation_digest")),
        _check("records_digest_bound", chain_service.EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check("target_universe_matches_chain_review_universe", TARGET_UNIVERSE, candidate.get("target_universe")),
        _check("registry_approval_created_true", True, candidate.get("registry_approval_created")),
        _check("research_registry_approved_true", True, candidate.get("research_registry_approved")),
        _check("additional_predictive_evidence_chain_candidate_created_true", True, candidate.get("additional_predictive_evidence_chain_candidate_created")),
        _check("additional_predictive_evidence_chain_candidate_review_created_true", True, candidate.get("additional_predictive_evidence_chain_candidate_review_created")),
        _check("additional_predictive_evidence_execution_candidate_created_true", True, candidate.get("additional_predictive_evidence_execution_candidate_created")),
        _check("execution_candidate_scope_candidate_only", EXECUTION_CANDIDATE_SCOPE, candidate.get("additional_predictive_evidence_execution_candidate_scope")),
        _check("execution_authority_status_not_authorized", NOT_AUTHORIZED, candidate.get("additional_predictive_evidence_execution_authority_status")),
        _check("canonical_dataset_generated_true", True, candidate.get("canonical_dataset_generated")),
        _check("canonical_dataset_frozen_true", True, candidate.get("canonical_dataset_frozen")),
        _check("total_canonical_record_count_11946", 11946, candidate.get("total_canonical_record_count")),
        _check("meta_record_count_913_preserved", 913, counts.get("META")),
        _check("non_meta_record_counts_1003_preserved", True, all(counts.get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META")),
        _check("planned_labels_7", 7, len(candidate.get("planned_label_set", []))),
        _check("planned_features_10", 10, len(candidate.get("planned_feature_set", []))),
        _check("planned_execution_protocol_defined", _planned_protocol(), candidate.get("planned_execution_protocol")),
        _check("planned_split_profile_defined", PLANNED_SPLIT_PROFILE, candidate.get("planned_split_profile")),
        _check("planned_metric_families_defined", _planned_metrics(), candidate.get("planned_metric_families")),
        _check("planned_baselines_defined", _planned_baselines(), candidate.get("planned_baselines")),
        _check("future_execution_outputs_defined", _future_outputs(), outputs),
        _check("future_execution_outputs_not_generated", True, bool(outputs) and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs)),
        _check("future_execution_chain_defined", FUTURE_EXECUTION_CHAIN, candidate.get("future_execution_chain")),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("market_data_acquisition_performed_false", False, candidate.get("market_data_acquisition_performed")),
        _check("dataset_generation_performed_false", False, candidate.get("dataset_generation_performed")),
        _check("canonical_dataset_regenerated_false", False, candidate.get("canonical_dataset_regenerated")),
        _check("label_generation_authorized_false", False, candidate.get("label_generation_authorized")),
        _check("label_generation_performed_false", False, candidate.get("label_generation_performed")),
        _check("feature_matrix_generation_authorized_false", False, candidate.get("feature_matrix_generation_authorized")),
        _check("feature_matrix_generation_performed_false", False, candidate.get("feature_matrix_generation_performed")),
        _check("walk_forward_validation_authorized_false", False, candidate.get("walk_forward_validation_authorized")),
        _check("walk_forward_validation_performed_false", False, candidate.get("walk_forward_validation_performed")),
        _check("out_of_sample_evaluation_authorized_false", False, candidate.get("out_of_sample_evaluation_authorized")),
        _check("out_of_sample_evaluation_performed_false", False, candidate.get("out_of_sample_evaluation_performed")),
        _check("baseline_comparison_authorized_false", False, candidate.get("baseline_comparison_authorized")),
        _check("baseline_comparison_performed_false", False, candidate.get("baseline_comparison_performed")),
        _check("signal_quality_metrics_performed_false", False, candidate.get("signal_quality_metrics_performed")),
        _check("stability_analysis_performed_false", False, candidate.get("stability_analysis_performed")),
        _check("leakage_control_review_performed_false", False, candidate.get("leakage_control_review_performed")),
        _check("additional_predictive_evidence_execution_authorized_false", False, candidate.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, candidate.get("additional_predictive_evidence_executed")),
        _check("additional_predictive_evidence_results_created_false", False, candidate.get("additional_predictive_evidence_results_created")),
        _check("predictive_experiment_rerun_authorized_false", False, candidate.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, candidate.get("predictive_experiment_rerun_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, candidate.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", NOT_ACCEPTED, candidate.get("profitability")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_additional_predictive_evidence_execution_artifact_created", False, candidate.get("additional_predictive_evidence_execution_artifact_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(item.get("status") == FAIL and item.get("severity") == BLOCKER for item in checklist),
        "ready_for_operator_review": failed == 0,
        "ready_for_additional_predictive_evidence_execution_candidate_review": failed == 0,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "ready_for_additional_predictive_evidence_execution": False,
        "ready_for_predictive_usefulness_reassessment": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def additional_predictive_evidence_execution_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the execution candidate."""
    payload = deepcopy(candidate)
    payload.pop("additional_predictive_evidence_execution_candidate_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_v1() -> dict[str, Any]:
    """Build a future-execution candidate without authorizing or performing work."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["additional_predictive_evidence_execution_candidate_digest"] = (
        additional_predictive_evidence_execution_candidate_digest_v1(candidate)
    )
    validate_additional_predictive_evidence_execution_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker_entries(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_execution_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "per-ticker execution candidate entries missing"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    _expect(entries, _per_ticker_entries(), "per-ticker entries")
    for entry in entries:
        digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_digest"
        )
        if not isinstance(digest, str) or len(digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateError(
                "per-ticker execution candidate digest missing"
            )
        _expect(
            digest,
            per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(entry),
            "per-ticker execution candidate digest",
        )


def validate_additional_predictive_evidence_execution_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the artifact remains a complete non-authorizing candidate."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline", "research_registry_approved", "registry_approval_created",
        "ready_for_additional_predictive_evidence_chain_candidate",
        "additional_predictive_evidence_chain_candidate_created",
        "additional_predictive_evidence_chain_candidate_review_created",
        "additional_predictive_evidence_chain_ready_for_operator_review",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_ready_for_operator_review",
        "canonical_dataset_generated", "canonical_dataset_frozen", "research_only",
        "operator_review_required",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made", "live_provider_transport_enabled",
        "market_data_acquisition_performed", "dataset_generation_performed",
        "canonical_dataset_regenerated", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_review_created",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "label_generation_authorized", "label_generation_performed",
        "feature_matrix_generation_authorized", "feature_matrix_generation_performed",
        "walk_forward_validation_authorized", "walk_forward_validation_performed",
        "out_of_sample_evaluation_authorized", "out_of_sample_evaluation_performed",
        "baseline_comparison_authorized", "baseline_comparison_performed",
        "signal_quality_metrics_authorized", "signal_quality_metrics_performed",
        "stability_analysis_authorized", "stability_analysis_performed",
        "leakage_control_review_authorized", "leakage_control_review_performed",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved",
        "runtime_migration_active", "automatic_stitching",
        "additional_predictive_evidence_execution_artifact_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    expected_fields = {
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "additional_predictive_evidence_chain_candidate_review_package_digest": EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_chain_candidate_digest": EXPECTED_CHAIN_CANDIDATE_DIGEST,
        "research_registry_approval_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "research_registry_candidate_review_package_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_registry_candidate_digest": chain_service.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "canonical_dataset_freeze_digest": chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": chain_service.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": chain_service.EXPECTED_RECORDS_DIGEST,
        "acquisition_generation_freeze_digest": chain_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "corporate_action_authority_approval_digest": chain_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": chain_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": chain_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "approved_registry_metadata": APPROVED_REGISTRY_METADATA,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "additional_predictive_evidence_execution_candidate_objective": EXECUTION_CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": EXECUTION_CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
        "additional_predictive_evidence_execution_authority_status": NOT_AUTHORIZED,
        "execution_candidate_profile": _execution_profile(),
        "planned_label_set": _planned_labels(),
        "planned_feature_set": _planned_features(),
        "planned_execution_protocol": _planned_protocol(),
        "planned_split_profile": PLANNED_SPLIT_PROFILE,
        "planned_metric_families": _planned_metrics(),
        "planned_baselines": _planned_baselines(),
        "future_execution_outputs": _future_outputs(),
        "future_execution_chain": FUTURE_EXECUTION_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in expected_fields.items():
        value = candidate.get(field)
        if isinstance(expected, list) and not value:
            raise AdditionalPredictiveEvidenceExecutionCandidateError(f"{field} missing")
        if isinstance(expected, dict) and not value:
            raise AdditionalPredictiveEvidenceExecutionCandidateError(f"{field} missing")
        _expect(value, expected, field)
    _validate_per_ticker_entries(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "candidate_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("additional_predictive_evidence_execution_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "execution candidate digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_digest_v1(candidate),
        "execution candidate digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_execution_candidate_digest": digest,
        "ready_for_operator_review": expected_summary["ready_for_operator_review"],
        "blocker_count": expected_summary["blocker_count"],
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the execution candidate."""
    validation = validate_additional_predictive_evidence_execution_candidate_v1(candidate)
    metadata = candidate["approved_registry_metadata"]
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Status",
        "", "## Title", "- Additional Predictive Evidence Execution Candidate v1.",
        "", "## Additional Predictive Evidence Execution Candidate",
        f"- Artifact: `{candidate['artifact_kind']}`",
        f"- Status: `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['additional_predictive_evidence_execution_candidate_digest']}`",
        "", "## Source Chain Candidate Review",
        f"- Review digest: `{candidate['additional_predictive_evidence_chain_candidate_review_package_digest']}`",
        f"- Chain candidate digest: `{candidate['additional_predictive_evidence_chain_candidate_digest']}`",
        "", "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in metadata.items())
    lines.extend(["", "## Target Universe", f"- `{' '.join(candidate['target_universe'])}`"])
    lines.extend(["", "## Per-Ticker Execution Candidate Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; `{item['additional_predictive_evidence_execution_candidate_status']}`" for item in candidate["per_ticker_execution_candidate_entries"])
    lines.extend(["", "## Planned Label Set"])
    lines.extend(f"- `{item['label_family']}`: `{item['execution_candidate_status']}`" for item in candidate["planned_label_set"])
    lines.extend(["", "## Planned Feature Set"])
    lines.extend(f"- `{item['feature_family']}`: `{item['execution_candidate_status']}`" for item in candidate["planned_feature_set"])
    lines.extend(["", "## Planned Execution Protocol"])
    lines.extend(f"- `{item['protocol_item']}`: `{item['execution_status']}`" for item in candidate["planned_execution_protocol"])
    lines.extend(["", "## Planned Split Profile"])
    lines.extend(f"- {key}: `{value}`" for key, value in candidate["planned_split_profile"].items())
    for heading, key, id_field in (
        ("Planned Metric Families", "planned_metric_families", "metric_family"),
        ("Planned Baselines", "planned_baselines", "baseline"),
        ("Future Execution Outputs", "future_execution_outputs", "output_id"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_field]}`" for item in candidate[key])
    for heading, values in (
        ("Future Execution Chain", candidate["future_execution_chain"]),
        ("Future Gates", candidate["future_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {value}" for value in values)
    lines.extend([
        "", "## Predictive Usefulness Boundary", f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
        "", "## Profitability Boundary", f"- profitability: `{candidate['profitability']}`",
        "", "## Runtime Boundary", f"- runtime_use: `{candidate['runtime_use']}`", f"- strategy_use: `{candidate['strategy_use']}`", f"- paper_trading: `{candidate['paper_trading']}`", f"- broker_execution: `{candidate['broker_execution']}`",
        "", "## Checklist Summary", f"- Total checks: `{summary['total_checks']}`", f"- Passed checks: `{summary['passed_checks']}`", f"- Failed checks: `{summary['failed_checks']}`", f"- Blocker count: `{summary['blocker_count']}`",
        "", "## Guardrails", "- Candidate only; no predictive evidence execution is approved, authorized, or performed.", "- No labels, features, metrics, baselines, walk-forward validation, or out-of-sample evaluation are generated or computed.", "- No provider request, dataset regeneration, predictive/profitability acceptance, runtime activation, or trading action occurs.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical candidate JSON once; existing output fails closed."""
    candidate = build_additional_predictive_evidence_execution_candidate_v1()
    validation = validate_additional_predictive_evidence_execution_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "additional_predictive_evidence_execution_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceExecutionCandidateError(
            "candidate output already exists"
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
