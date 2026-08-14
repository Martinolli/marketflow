"""Offline planning candidate for the registry-approved predictive evidence chain."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import research_registry_approval_service as registry_approval


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_V1 = (
    "additional_predictive_evidence_chain_candidate_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_READY_FOR_OPERATOR_REVIEW = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    registry_approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST = (
    registry_approval.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    registry_approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST = (
    registry_approval.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    registry_approval.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
)
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    registry_approval.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST = (
    registry_approval.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST
)
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    registry_approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    registry_approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    registry_approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    registry_approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_RECORDS_DIGEST = registry_approval.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(registry_approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(registry_approval.EXPECTED_RECORD_COUNTS)
APPROVED_REGISTRY_METADATA = deepcopy(registry_approval.APPROVED_REGISTRY_METADATA)

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PLANNED_NOT_AUTHORIZED = "PLANNED_NOT_AUTHORIZED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
NOT_AUTHORIZED_FOR_EXECUTION = "NOT_AUTHORIZED_FOR_EXECUTION"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_OBJECTIVE = (
    "PLAN_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_FOR_RESEARCH_REGISTRY_APPROVED_EXPANDED_UNIVERSE"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_SCOPE = "CHAIN_CANDIDATE_ONLY_NOT_EXECUTION"
ADDITIONAL_PREDICTIVE_EVIDENCE_MODE = "PLANNED_NOT_EXECUTED"
ADDITIONAL_PREDICTIVE_EVIDENCE_AUTHORITY_STATUS = NOT_AUTHORIZED

PREDICTIVE_EVIDENCE_PLANNING_DIMENSIONS = [
    "registry_approved_dataset_binding",
    "frozen_canonical_dataset_binding",
    "records_digest_binding",
    "ticker_universe_order_policy",
    "source_profile_policy",
    "meta_reduced_record_count_preservation_policy",
    "label_definition_policy",
    "feature_family_policy",
    "feature_matrix_policy",
    "walk_forward_validation_policy",
    "out_of_sample_evaluation_policy",
    "baseline_comparison_policy",
    "signal_quality_metrics_policy",
    "stability_analysis_policy",
    "false_positive_false_negative_policy",
    "calibration_review_policy",
    "lift_analysis_policy",
    "leakage_control_policy",
    "embargo_gap_policy",
    "deterministic_reproducibility_policy",
    "digest_manifest_policy",
    "research_only_output_labeling_policy",
    "predictive_usefulness_boundary_policy",
    "profitability_boundary_policy",
    "runtime_boundary_policy",
    "trade_recommendation_boundary_policy",
]

PLANNED_LABEL_FAMILY_IDS = [
    "NEXT_BAR_DIRECTION",
    "NEXT_BAR_RETURN_BUCKET",
    "NEXT_SESSION_DIRECTION",
    "NEXT_SESSION_RETURN_BUCKET",
    "MULTI_HORIZON_RETURN_BUCKET",
    "VOLATILITY_REGIME_LABEL",
    "DRAWDOWN_RISK_LABEL",
]

PLANNED_FEATURE_FAMILY_IDS = [
    "ohlcv_return_features",
    "volume_price_features",
    "volatility_features",
    "trend_momentum_features",
    "wyckoff_vpa_features",
    "corporate_action_context_features",
    "cross_ticker_relative_strength_features",
    "calendar_session_features",
    "data_quality_flags",
    "meta_reduced_record_count_flag",
]

PLANNED_EVALUATION_PROTOCOL = [
    "chronological_split_policy",
    "walk_forward_validation_policy",
    "out_of_sample_holdout_policy",
    "no_shuffle_policy",
    "forward_only_label_policy",
    "leakage_prevention_policy",
    "baseline_comparison_policy",
    "stability_review_policy",
    "operator_review_required_before_execution",
]

FUTURE_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN = [
    "Additional predictive evidence chain candidate operator review package.",
    "Additional predictive evidence execution candidate.",
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
    "additional_predictive_evidence_chain_candidate_operator_review",
    "additional_predictive_evidence_execution_candidate",
    "additional_predictive_evidence_execution_candidate_review",
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

RISK_CONTROLS = [
    "no_predictive_execution_without_operator_approval",
    "no_label_generation_without_execution_approval",
    "no_feature_matrix_generation_without_execution_approval",
    "no_walk_forward_validation_without_execution_approval",
    "no_out_of_sample_evaluation_without_execution_approval",
    "no_predictive_usefulness_acceptance_without_results_review",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "preserve_meta_reduced_record_count",
    "do_not_mutate_frozen_canonical_dataset",
    "all_outputs_labeled_research_only",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
]

PLANNED_OUTPUT_IDS = [
    "additional_predictive_evidence_chain_manifest",
    "label_definition_plan",
    "feature_family_plan",
    "feature_matrix_plan",
    "walk_forward_validation_plan",
    "out_of_sample_evaluation_plan",
    "baseline_comparison_plan",
    "signal_quality_metrics_plan",
    "stability_analysis_plan",
    "false_positive_false_negative_plan",
    "leakage_control_plan",
    "predictive_usefulness_reassessment_plan",
    "operator_review_summary_template",
]

REQUIRED_CHECK_IDS = [
    "research_registry_approval_digest_bound",
    "research_registry_candidate_review_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_results_review_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_registry_approved_universe",
    "registry_approval_created_true",
    "research_registry_approved_true",
    "ready_for_additional_predictive_evidence_chain_candidate_true",
    "additional_predictive_evidence_chain_candidate_created_true",
    "additional_predictive_evidence_chain_scope_candidate_only",
    "additional_predictive_evidence_authority_status_not_authorized",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "predictive_evidence_planning_dimensions_defined",
    "planned_label_families_defined",
    "planned_feature_families_defined",
    "planned_evaluation_protocol_defined",
    "future_predictive_evidence_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
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
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
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

FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_EXPERIMENT_RERUN_APPROVED",
    "PREDICTIVE_EXPERIMENT_RERUN_EXECUTED",
    "FEATURE_MATRIX_REGENERATION_EXECUTED",
    "NEW_STRATEGY_SCORING_EXECUTED",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


class AdditionalPredictiveEvidenceChainCandidateError(ValueError):
    """Raised when a chain candidate violates its non-authorizing contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceChainCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceChainCandidateError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceChainCandidateError(f"{field} must be false")


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


def _planned_items(item_ids: list[str], id_field: str) -> list[dict[str, Any]]:
    return [
        {
            id_field: item_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "execution_authority_status": NOT_AUTHORIZED_FOR_EXECUTION,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for item_id in item_ids
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def per_ticker_additional_predictive_evidence_chain_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return a semantic digest for one ticker planning entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_additional_predictive_evidence_chain_candidate_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": registry_approval.APPROVED_FOR_RESEARCH_REGISTRY_ONLY,
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "additional_predictive_evidence_chain_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
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
        }
        entry["per_ticker_additional_predictive_evidence_chain_candidate_digest"] = (
            per_ticker_additional_predictive_evidence_chain_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_V1,
        "candidate_status": ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_READY_FOR_OPERATOR_REVIEW,
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
        "additional_predictive_evidence_chain_ready_for_operator_review": True,
        "additional_predictive_evidence_chain_approved": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "new_ticker_acquisition_authorized": True,
        "acquisition_generation_authorized": True,
        "acquisition_generation_approved": True,
        "acquisition_generation_frozen": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "identity_authority_created": True,
        "identity_authority_frozen": True,
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
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "research_registry_candidate_review_package_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_registry_candidate_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "approved_registry_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "total_canonical_record_count": sum(EXPECTED_RECORD_COUNTS.values()),
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "per_ticker_predictive_evidence_planning_entries": _per_ticker_entries(),
        "additional_predictive_evidence_chain_objective": ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_OBJECTIVE,
        "additional_predictive_evidence_chain_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_SCOPE,
        "additional_predictive_evidence_mode": ADDITIONAL_PREDICTIVE_EVIDENCE_MODE,
        "additional_predictive_evidence_authority_status": ADDITIONAL_PREDICTIVE_EVIDENCE_AUTHORITY_STATUS,
        "predictive_evidence_planning_dimensions": list(PREDICTIVE_EVIDENCE_PLANNING_DIMENSIONS),
        "planned_label_families": _planned_items(PLANNED_LABEL_FAMILY_IDS, "label_family_id"),
        "planned_feature_families": _planned_items(PLANNED_FEATURE_FAMILY_IDS, "feature_family_id"),
        "planned_evaluation_protocol": [
            {"protocol_item_id": item, "execution_status": "PLANNED_NOT_EXECUTED"}
            for item in PLANNED_EVALUATION_PROTOCOL
        ],
        "future_additional_predictive_evidence_chain": list(FUTURE_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "additional_predictive_evidence_execution_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_predictive_evidence_planning_entries", [])
    outputs = candidate.get("planned_outputs", [])
    return [
        _check("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, candidate.get("research_registry_approval_digest")),
        _check("research_registry_candidate_review_digest_bound", EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("research_registry_candidate_review_package_digest")),
        _check("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, candidate.get("canonical_dataset_freeze_digest")),
        _check("canonical_dataset_results_review_digest_bound", EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("canonical_dataset_results_review_package_digest")),
        _check("canonical_dataset_generation_digest_bound", EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, candidate.get("canonical_dataset_generation_digest")),
        _check("records_digest_bound", EXPECTED_RECORDS_DIGEST, candidate.get("records_digest")),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check("target_universe_matches_registry_approved_universe", TARGET_UNIVERSE, candidate.get("target_universe")),
        _check("registry_approval_created_true", True, candidate.get("registry_approval_created")),
        _check("research_registry_approved_true", True, candidate.get("research_registry_approved")),
        _check("ready_for_additional_predictive_evidence_chain_candidate_true", True, candidate.get("ready_for_additional_predictive_evidence_chain_candidate")),
        _check("additional_predictive_evidence_chain_candidate_created_true", True, candidate.get("additional_predictive_evidence_chain_candidate_created")),
        _check("additional_predictive_evidence_chain_scope_candidate_only", ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_SCOPE, candidate.get("additional_predictive_evidence_chain_scope")),
        _check("additional_predictive_evidence_authority_status_not_authorized", NOT_AUTHORIZED, candidate.get("additional_predictive_evidence_authority_status")),
        _check("canonical_dataset_generated_true", True, candidate.get("canonical_dataset_generated")),
        _check("canonical_dataset_frozen_true", True, candidate.get("canonical_dataset_frozen")),
        _check("total_canonical_record_count_11946", 11946, candidate.get("total_canonical_record_count")),
        _check("meta_record_count_913_preserved", 913, candidate.get("per_ticker_record_counts", {}).get("META")),
        _check("non_meta_record_counts_1003_preserved", True, all(candidate.get("per_ticker_record_counts", {}).get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META")),
        _check("predictive_evidence_planning_dimensions_defined", PREDICTIVE_EVIDENCE_PLANNING_DIMENSIONS, candidate.get("predictive_evidence_planning_dimensions")),
        _check("planned_label_families_defined", _planned_items(PLANNED_LABEL_FAMILY_IDS, "label_family_id"), candidate.get("planned_label_families")),
        _check("planned_feature_families_defined", _planned_items(PLANNED_FEATURE_FAMILY_IDS, "feature_family_id"), candidate.get("planned_feature_families")),
        _check("planned_evaluation_protocol_defined", [{"protocol_item_id": item, "execution_status": "PLANNED_NOT_EXECUTED"} for item in PLANNED_EVALUATION_PROTOCOL], candidate.get("planned_evaluation_protocol")),
        _check("future_predictive_evidence_chain_defined", FUTURE_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN, candidate.get("future_additional_predictive_evidence_chain")),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("planned_outputs_not_generated", True, bool(outputs) and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs)),
        _check("planned_outputs_research_only", True, bool(outputs) and all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)),
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
        _check("additional_predictive_evidence_execution_authorized_false", False, candidate.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, candidate.get("additional_predictive_evidence_executed")),
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
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "ready_for_predictive_usefulness_reassessment": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def additional_predictive_evidence_chain_candidate_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the chain candidate."""
    payload = deepcopy(candidate)
    payload.pop("additional_predictive_evidence_chain_candidate_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_chain_candidate_v1() -> dict[str, Any]:
    """Build the offline chain candidate without executing predictive work."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["additional_predictive_evidence_chain_candidate_digest"] = (
        additional_predictive_evidence_chain_candidate_digest_v1(candidate)
    )
    validate_additional_predictive_evidence_chain_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceChainCandidateError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_ticker_entries(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_predictive_evidence_planning_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceChainCandidateError("per-ticker entries missing")
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    expected_entries = _per_ticker_entries()
    _expect(entries, expected_entries, "per-ticker entries")
    for entry in entries:
        digest = entry.get("per_ticker_additional_predictive_evidence_chain_candidate_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise AdditionalPredictiveEvidenceChainCandidateError("per-ticker digest missing")
        _expect(digest, per_ticker_additional_predictive_evidence_chain_candidate_digest_v1(entry), "per-ticker digest")


def validate_additional_predictive_evidence_chain_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the artifact remains a complete planning-only candidate."""
    if not isinstance(candidate, dict):
        raise AdditionalPredictiveEvidenceChainCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline", "research_registry_approved", "registry_approval_created",
        "ready_for_additional_predictive_evidence_chain_candidate",
        "additional_predictive_evidence_chain_candidate_created",
        "additional_predictive_evidence_chain_ready_for_operator_review",
        "canonical_dataset_generated", "canonical_dataset_frozen", "research_only",
        "operator_review_required",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made", "live_provider_transport_enabled",
        "market_data_acquisition_performed", "dataset_generation_performed",
        "canonical_dataset_regenerated", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "additional_predictive_evidence_chain_approved",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "label_generation_authorized", "label_generation_performed",
        "feature_matrix_generation_authorized", "feature_matrix_generation_performed",
        "walk_forward_validation_authorized", "walk_forward_validation_performed",
        "out_of_sample_evaluation_authorized", "out_of_sample_evaluation_performed",
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
    for field, expected in {
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "additional_predictive_evidence_chain_objective": ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_OBJECTIVE,
        "additional_predictive_evidence_chain_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_SCOPE,
        "additional_predictive_evidence_mode": ADDITIONAL_PREDICTIVE_EVIDENCE_MODE,
        "additional_predictive_evidence_authority_status": NOT_AUTHORIZED,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "research_registry_candidate_review_package_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "research_registry_candidate_digest": EXPECTED_RESEARCH_REGISTRY_CANDIDATE_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_results_review_package_digest": EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "acquisition_generation_freeze_digest": EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "approved_registry_metadata": APPROVED_REGISTRY_METADATA,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "predictive_evidence_planning_dimensions": PREDICTIVE_EVIDENCE_PLANNING_DIMENSIONS,
        "planned_label_families": _planned_items(PLANNED_LABEL_FAMILY_IDS, "label_family_id"),
        "planned_feature_families": _planned_items(PLANNED_FEATURE_FAMILY_IDS, "feature_family_id"),
        "planned_evaluation_protocol": [{"protocol_item_id": item, "execution_status": "PLANNED_NOT_EXECUTED"} for item in PLANNED_EVALUATION_PROTOCOL],
        "future_additional_predictive_evidence_chain": FUTURE_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": _planned_outputs(),
    }.items():
        value = candidate.get(field)
        if isinstance(expected, list) and not value:
            raise AdditionalPredictiveEvidenceChainCandidateError(f"{field} missing")
        _expect(value, expected, field)
    _validate_ticker_entries(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceChainCandidateError("candidate_checklist missing")
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "candidate_checklist check IDs")
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise AdditionalPredictiveEvidenceChainCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("additional_predictive_evidence_chain_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceChainCandidateError("candidate digest missing")
    _expect(digest, additional_predictive_evidence_chain_candidate_digest_v1(candidate), "candidate digest")
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "additional_predictive_evidence_chain_candidate_digest": digest,
        "ready_for_operator_review": expected_summary["ready_for_operator_review"],
        "blocker_count": expected_summary["blocker_count"],
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_chain_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized operator-review summary of the candidate."""
    validation = validate_additional_predictive_evidence_chain_candidate_v1(candidate)
    metadata = candidate["approved_registry_metadata"]
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Chain Candidate Status",
        "", "## Title", "- Additional Predictive Evidence Chain Candidate v1.",
        "", "## Additional Predictive Evidence Chain Candidate",
        f"- Artifact: `{candidate['artifact_kind']}`",
        f"- Status: `{candidate['candidate_status']}`",
        f"- Candidate digest: `{validation['additional_predictive_evidence_chain_candidate_digest']}`",
        "", "## Source Research Registry Approval",
        f"- Approval digest: `{candidate['research_registry_approval_digest']}`",
        f"- Candidate review digest: `{candidate['research_registry_candidate_review_package_digest']}`",
        f"- Canonical dataset freeze digest: `{candidate['canonical_dataset_freeze_digest']}`",
        "", "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in metadata.items())
    lines.extend(["", "## Target Universe", f"- `{' '.join(candidate['target_universe'])}`"])
    lines.extend(["", "## Per-Ticker Predictive Evidence Planning Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; `{item['additional_predictive_evidence_chain_status']}`" for item in candidate["per_ticker_predictive_evidence_planning_entries"])
    lines.extend(["", "## Planned Label Families"])
    lines.extend(f"- `{item['label_family_id']}`: `{item['generation_status']}`" for item in candidate["planned_label_families"])
    lines.extend(["", "## Planned Feature Families"])
    lines.extend(f"- `{item['feature_family_id']}`: `{item['generation_status']}`" for item in candidate["planned_feature_families"])
    lines.extend(["", "## Planned Evaluation Protocol"])
    lines.extend(f"- `{item['protocol_item_id']}`: `{item['execution_status']}`" for item in candidate["planned_evaluation_protocol"])
    for heading, values in (
        ("Future Predictive Evidence Chain", candidate["future_additional_predictive_evidence_chain"]),
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
        "", "## Guardrails", "- Planning only; no predictive evidence execution is authorized or performed.", "- No labels, features, walk-forward validation, or out-of-sample evaluation are generated.", "- No provider request, market-data acquisition, dataset regeneration, runtime activation, or trade recommendation occurs.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_chain_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical candidate JSON once; existing output fails closed."""
    candidate = build_additional_predictive_evidence_chain_candidate_v1()
    validation = validate_additional_predictive_evidence_chain_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "additional_predictive_evidence_chain_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceChainCandidateError(
            "candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceChainCandidateError("candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
