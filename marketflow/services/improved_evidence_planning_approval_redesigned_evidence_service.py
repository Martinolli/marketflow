"""Offline operator-attested approval for future improved-evidence planning."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    improved_evidence_planning_candidate_redesigned_evidence_operator_review_service as review_service,
)


ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1 = (
    "improved_evidence_planning_approval_using_redesigned_evidence_v1"
)
IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE = (
    "IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE"
)
IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY = (
    "IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY"
)
IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID = (
    "IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID"
)
SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION = review_service.SELECTED_DIRECTION
OPERATOR_DECISION_APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE = (
    "APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE"
)
OPERATOR_ATTESTATION_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1 = (
    "improved_evidence_planning_approval_using_redesigned_evidence_operator_attestation_v1"
)
REQUIRED_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_ATTESTATION_PHRASE = (
    "APPROVE IMPROVED EVIDENCE PLANNING USING REDESIGNED EVIDENCE "
    "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY"
)

DEFAULT_BRANCH = "feature/improved-evidence-planning-approval-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "eb3e4cacb4f398ef83c5da8cb3b38e2206190579"
EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    "d69cf64437f1dbd69a929e00c94a6cc9c13e6148102cd2adc91d1ed4eff8ceb6"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
BOUND_DIGESTS = deepcopy(review_service.candidate_service.BOUND_DIGESTS)
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(review_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
PLANNED_NOT_GENERATED = review_service.candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = (
    review_service.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
)
APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY = (
    "APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY"
)

APPROVED_OBJECTIVE = (
    "AUTHORIZE_FUTURE_RESEARCH_ONLY_IMPROVED_EVIDENCE_PLANNING_FOR_NO_TRADE_ABSTAIN_LABEL_OBJECTIVE_REDESIGN"
)
APPROVED_SCOPE = IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY
APPROVED_MODE = AUTHORIZED_NOT_EXECUTED
APPROVED_AUTHORITY_STATUS = (
    "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_PLANNING_EXECUTION"
)

APPROVED_DATA_PRODUCT_IDS = [
    "improved_evidence_planning_execution_manifest",
    "proposed_label_schema_report",
    "no_trade_abstain_coverage_report",
    "material_move_threshold_report",
    "horizon_specific_validation_report",
    "ticker_regime_split_validation_report",
    "feature_label_alignment_report",
    "chronological_split_embargo_report",
    "baseline_model_comparison_plan",
    "calibration_brier_plan",
    "leakage_no_peek_control_plan",
    "per_ticker_meta_reporting_plan",
    "operator_review_summary",
]

NEXT_CHAIN = [
    "Optional Improved Evidence Planning Execution Using Redesigned Evidence v1.",
    "Optional Improved Evidence Planning Results Review Using Redesigned Evidence v1.",
    "Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence v1, if supported.",
    "Optional Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "improved_evidence_planning_execution_using_redesigned_evidence_if_approved",
    "improved_evidence_planning_results_review_using_redesigned_evidence",
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_if_supported",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "approval_does_not_execute_planning_now",
    "approval_does_not_generate_labels",
    "approval_does_not_create_new_targets",
    "approval_does_not_authorize_target_definition_change",
    "approval_does_not_generate_features",
    "approval_does_not_create_feature_label_matrix",
    "approval_does_not_create_predictive_evidence_execution_candidate",
    "approval_does_not_execute_predictive_evidence",
    "approval_does_not_rerun_predictive_evidence",
    "approval_does_not_retrain_models",
    "approval_does_not_recompute_metrics",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_create_acceptance_candidate",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "do_not_mutate_label_objective_review_outputs",
    "do_not_mutate_label_objective_redesign_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_planning_authorized",
    "operator_confirms_ready_for_planning_execution",
    "operator_confirms_no_planning_execution",
    "operator_confirms_no_label_regeneration",
    "operator_confirms_no_new_targets",
    "operator_confirms_no_target_definition_change_authorization",
    "operator_confirms_no_feature_generation",
    "operator_confirms_no_feature_label_matrix_creation",
    "operator_confirms_no_additional_predictive_evidence_execution_candidate",
    "operator_confirms_no_predictive_evidence_execution",
    "operator_confirms_no_predictive_evidence_rerun",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
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


class ImprovedEvidencePlanningApprovalRedesignedEvidenceError(ValueError):
    """Raised when an approval violates its exact attested boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            f"{field} must be true"
        )


def build_improved_evidence_planning_approval_using_redesigned_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_review_digest: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_redesign_results_review_digest: str,
    operator_confirms_redesign_execution_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_redesign_direction: str,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_planning_authorized: bool,
    operator_confirms_ready_for_planning_execution: bool,
    operator_confirms_no_planning_execution: bool,
    operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_new_targets: bool,
    operator_confirms_no_target_definition_change_authorization: bool,
    operator_confirms_no_feature_generation: bool,
    operator_confirms_no_feature_label_matrix_creation: bool,
    operator_confirms_no_additional_predictive_evidence_execution_candidate: bool,
    operator_confirms_no_predictive_evidence_execution: bool,
    operator_confirms_no_predictive_evidence_rerun: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_redesign_direction: str = SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
    operator_decision: str = OPERATOR_DECISION_APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE,
) -> dict:
    """Build a non-secret attestation; the approval validates every field."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_redesign_results_review_digest": BOUND_DIGESTS[
            "label_objective_redesign_results_review_using_redesigned_evidence_digest"
        ],
        "operator_confirms_redesign_execution_digest": BOUND_DIGESTS[
            "label_objective_redesign_execution_using_redesigned_evidence_digest"
        ],
        "operator_confirms_records_digest": BOUND_DIGESTS["records_digest"],
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "operator_attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE,
        "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "operator_attestation_phrase": REQUIRED_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        **_expected_digest_confirmations(),
    }
    for field, expected_value in expected.items():
        _expect(attestation.get(field), expected_value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
                f"{field} required"
            )


def _source_review(source: dict | None) -> dict[str, Any]:
    package = (
        review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        validation = review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
            package
        )
    except review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError as exc:
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "source candidate review is invalid"
        ) from exc
    _expect(
        package.get(
            "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "source candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "source candidate review status",
    )
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source blockers")
    _expect(
        validation.get(
            "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "validated source candidate review digest",
    )
    return package


def _approved_themes(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "theme_id": row["theme_id"],
            "approval_status": APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY,
            "execution_performed": False,
            "label_generation_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "metric_computation_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_improved_evidence_themes"]
    ]


def _approved_components(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "component_id": row["component_id"],
            "approval_status": APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY,
            "execution_performed": False,
            "label_generation_authorized": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_creation_authorized": False,
            "metric_computation_authorized": False,
            "model_training_authorized": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_evidence_components"]
    ]


def _approved_data_products() -> list[dict[str, Any]]:
    return [
        {
            "data_product_id": product_id,
            "output_status": AUTHORIZED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for product_id in APPROVED_DATA_PRODUCT_IDS
    ]


def _approved_future_outputs(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "future_output_id": row["future_output_id"],
            "output_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_future_outputs"]
    ]


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_improved_evidence_planning_approval_digest", None)
    return payload


def per_ticker_improved_evidence_planning_approval_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one ticker approval."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_approvals(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for row in source["per_ticker_review_entries"]:
        is_meta = row["ticker"] == "META"
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row[
                "meta_reduced_record_count_flag"
            ],
            "label_objective_redesign_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "improved_evidence_planning_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "improved_evidence_planning_approval_status": APPROVED_FOR_FUTURE_RESEARCH_PLANNING_EXECUTION_ONLY,
            "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
            "improved_evidence_planning_authorized": True,
            "improved_evidence_planning_executed": False,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
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
            "source_improved_evidence_planning_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "source_improved_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "approval_note": (
                "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_APPROVAL"
                if is_meta
                else "STANDARD_FROZEN_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_improved_evidence_planning_approval_digest"] = (
            per_ticker_improved_evidence_planning_approval_digest_v1(entry)
        )
        approvals.append(entry)
    return approvals


def _base_approval(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1,
        "approval_status": IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE,
        "approval_scope": IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_attestation": deepcopy(dict(attestation)),
        "source_candidate_review_artifact_kind": source["artifact_kind"],
        "source_candidate_review_status": source["review_status"],
        "source_candidate_artifact_kind": source["source_candidate_artifact_kind"],
        "source_candidate_status": source["source_candidate_status"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **deepcopy(BOUND_DIGESTS),
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence": True,
        "improved_evidence_planning_candidate_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created": True,
        "improved_evidence_planning_approved": True,
        "improved_evidence_planning_approval_created": True,
        "improved_evidence_planning_authorized": True,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": True,
        "improved_evidence_planning_executed": False,
        "improved_evidence_planning_execution_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
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
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "metric_recomputation_performed_in_approval": False,
        "model_training_performed_in_approval": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe_count": source["target_universe_count"],
        "target_universe": deepcopy(source["target_universe"]),
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source[
            "meta_reduced_record_count_preserved"
        ],
        "approved_candidate_basis": deepcopy(source["reviewed_candidate_basis"]),
        "selected_direction": source["selected_direction"],
        "majority_structure_risk": source["majority_structure_risk"],
        "largest_aggregated_class": source["largest_aggregated_class"],
        "largest_aggregated_class_count": source["largest_aggregated_class_count"],
        "no_trade_count": source["no_trade_count"],
        "oos_evaluated_rows": source["oos_evaluated_rows"],
        "majority_accuracy": source["majority_accuracy"],
        "local_model_accuracy": source["local_model_accuracy"],
        "cross_sectional_accuracy": source["cross_sectional_accuracy"],
        "cross_sectional_delta_vs_majority": source[
            "cross_sectional_delta_vs_majority"
        ],
        "global_five_session_threshold": source["global_five_session_threshold"],
        "benchmark_relative_threshold": source["benchmark_relative_threshold"],
        "improved_evidence_planning_objective": APPROVED_OBJECTIVE,
        "improved_evidence_planning_scope": APPROVED_SCOPE,
        "improved_evidence_planning_mode": APPROVED_MODE,
        "improved_evidence_planning_authority_status": APPROVED_AUTHORITY_STATUS,
        "approved_improved_evidence_themes": _approved_themes(source),
        "approved_planned_evidence_components": _approved_components(source),
        "approved_data_products": _approved_data_products(),
        "approved_future_outputs": _approved_future_outputs(source),
        "per_ticker_approval_entries": _per_ticker_approvals(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


REQUIRED_CHECK_IDS = [
    "candidate_review_digest_bound", "candidate_digest_bound",
    "redesign_results_review_digest_bound", "redesign_execution_digest_bound",
    "redesign_output_binding_digest_bound", "redesign_approval_digest_bound",
    "redesign_candidate_review_digest_bound", "redesign_candidate_digest_bound",
    "target_definition_results_review_digest_bound", "target_definition_execution_digest_bound",
    "path_selection_digest_bound", "readiness_review_digest_bound", "reassessment_digest_bound",
    "predictive_results_review_digest_bound", "predictive_execution_digest_bound",
    "matrix_digest_bound", "feature_values_digest_bound", "label_values_digest_bound",
    "research_registry_digest_bound", "records_digest_bound", "target_universe_12_preserved",
    "target_universe_matches_review_universe", "records_digest_preserved", "meta_913_preserved",
    "operator_decision_matches", "operator_attestation_phrase_matches",
    "selected_redesign_direction_preserved", "approval_scope_only",
    "improved_evidence_planning_approved_true", "improved_evidence_planning_approval_created_true",
    "improved_evidence_planning_authorized_true", "ready_for_planning_execution_true",
    "planning_executed_false", "label_regeneration_authorized_false",
    "label_regeneration_performed_false", "new_targets_created_false",
    "target_definition_change_authorized_false", "target_definition_change_performed_false",
    "feature_generation_authorized_false", "feature_generation_performed_false",
    "feature_label_matrix_created_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_executed_false", "predictive_usefulness_not_accepted",
    "acceptance_ready_false", "acceptance_candidate_created_false", "profitability_not_accepted",
    "runtime_not_authorized", "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "approved_candidate_basis_preserved",
    "approved_objective_defined", "approved_themes_11", "approved_components_13",
    "approved_data_products_13", "approved_future_outputs_12",
    "per_ticker_approval_entries_12", "per_ticker_approval_digests_present",
    "provider_requests_made_false", "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "label_objective_redesign_execution_rerun_false",
    "metric_recomputation_in_approval_false", "model_training_in_approval_false",
    "raw_provider_payloads_not_committed", "api_keys_not_stored_or_printed",
    "no_improved_evidence_planning_execution_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created", "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created", "next_chain_defined", "next_gates_defined",
    "risk_controls_defined", "no_tracked_marketflow_files",
]


def _per_ticker_digests_valid(entries: Any) -> bool:
    return (
        isinstance(entries, list)
        and len(entries) == 12
        and all(
            isinstance(
                row.get("per_ticker_improved_evidence_planning_approval_digest"),
                str,
            )
            and len(row["per_ticker_improved_evidence_planning_approval_digest"])
            == 64
            and row["per_ticker_improved_evidence_planning_approval_digest"]
            == per_ticker_improved_evidence_planning_approval_digest_v1(row)
            for row in entries
        )
    )


def _checklist(approval: dict[str, Any]) -> list[dict[str, Any]]:
    operator = approval["operator_attestation"]
    entries = approval["per_ticker_approval_entries"]
    values: dict[str, tuple[Any, Any]] = {
        "candidate_review_digest_bound": (EXPECTED_CANDIDATE_REVIEW_DIGEST, approval.get("improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest")),
        "candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, approval.get("improved_evidence_planning_candidate_using_redesigned_evidence_digest")),
        "redesign_results_review_digest_bound": (BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"], approval.get("label_objective_redesign_results_review_using_redesigned_evidence_digest")),
        "redesign_execution_digest_bound": (BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"], approval.get("label_objective_redesign_execution_using_redesigned_evidence_digest")),
        "redesign_output_binding_digest_bound": (BOUND_DIGESTS["label_objective_redesign_output_binding_digest"], approval.get("label_objective_redesign_output_binding_digest")),
        "redesign_approval_digest_bound": (BOUND_DIGESTS["label_objective_redesign_approval_using_redesigned_evidence_digest"], approval.get("label_objective_redesign_approval_using_redesigned_evidence_digest")),
        "redesign_candidate_review_digest_bound": (BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"], approval.get("label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest")),
        "redesign_candidate_digest_bound": (BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_digest"], approval.get("label_objective_redesign_candidate_using_redesigned_evidence_digest")),
        "target_definition_results_review_digest_bound": (BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], approval.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest")),
        "target_definition_execution_digest_bound": (BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], approval.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest")),
        "path_selection_digest_bound": (BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], approval.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest")),
        "readiness_review_digest_bound": (BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], approval.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest")),
        "reassessment_digest_bound": (BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], approval.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest")),
        "predictive_results_review_digest_bound": (BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], approval.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest")),
        "predictive_execution_digest_bound": (BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], approval.get("additional_predictive_evidence_execution_using_redesigned_labels_digest")),
        "matrix_digest_bound": (BOUND_DIGESTS["feature_label_matrix_digest"], approval.get("feature_label_matrix_digest")),
        "feature_values_digest_bound": (BOUND_DIGESTS["feature_values_digest"], approval.get("feature_values_digest")),
        "label_values_digest_bound": (BOUND_DIGESTS["redesigned_label_values_digest"], approval.get("redesigned_label_values_digest")),
        "research_registry_digest_bound": (BOUND_DIGESTS["research_registry_approval_digest"], approval.get("research_registry_approval_digest")),
        "records_digest_bound": (BOUND_DIGESTS["records_digest"], approval.get("records_digest")),
        "target_universe_12_preserved": (12, approval.get("target_universe_count")),
        "target_universe_matches_review_universe": (TARGET_UNIVERSE, approval.get("target_universe")),
        "records_digest_preserved": (BOUND_DIGESTS["records_digest"], approval.get("records_digest")),
        "meta_913_preserved": (913, approval.get("meta_record_count")),
        "operator_decision_matches": (OPERATOR_DECISION_APPROVE_IMPROVED_EVIDENCE_PLANNING_USING_REDESIGNED_EVIDENCE, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "selected_redesign_direction_preserved": (SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION, approval.get("selected_direction")),
        "approval_scope_only": (IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY, approval.get("approval_scope")),
        "improved_evidence_planning_approved_true": (True, approval.get("improved_evidence_planning_approved")),
        "improved_evidence_planning_approval_created_true": (True, approval.get("improved_evidence_planning_approval_created")),
        "improved_evidence_planning_authorized_true": (True, approval.get("improved_evidence_planning_authorized")),
        "ready_for_planning_execution_true": (True, approval.get("ready_for_improved_evidence_planning_execution_using_redesigned_evidence")),
        "planning_executed_false": (False, approval.get("improved_evidence_planning_executed")),
        "label_regeneration_authorized_false": (False, approval.get("label_regeneration_authorized")),
        "label_regeneration_performed_false": (False, approval.get("label_regeneration_performed")),
        "new_targets_created_false": (False, approval.get("new_targets_created")),
        "target_definition_change_authorized_false": (False, approval.get("target_definition_change_authorized")),
        "target_definition_change_performed_false": (False, approval.get("target_definition_change_performed")),
        "feature_generation_authorized_false": (False, approval.get("feature_generation_authorized")),
        "feature_generation_performed_false": (False, approval.get("feature_generation_performed")),
        "feature_label_matrix_created_false": (False, approval.get("feature_label_matrix_created")),
        "additional_predictive_evidence_execution_candidate_created_false": (False, approval.get("additional_predictive_evidence_execution_candidate_created")),
        "additional_predictive_evidence_executed_false": (False, approval.get("additional_predictive_evidence_executed")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "acceptance_ready_false": (False, approval.get("predictive_usefulness_acceptance_ready")),
        "acceptance_candidate_created_false": (False, approval.get("predictive_usefulness_acceptance_candidate_created")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, approval.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "trade_recommendations_false": (False, approval.get("trade_recommendations_generated")),
        "approved_candidate_basis_preserved": (review_service.candidate_service.CANDIDATE_BASIS, approval.get("approved_candidate_basis")),
        "approved_objective_defined": (APPROVED_OBJECTIVE, approval.get("improved_evidence_planning_objective")),
        "approved_themes_11": (11, len(approval.get("approved_improved_evidence_themes", []))),
        "approved_components_13": (13, len(approval.get("approved_planned_evidence_components", []))),
        "approved_data_products_13": (13, len(approval.get("approved_data_products", []))),
        "approved_future_outputs_12": (12, len(approval.get("approved_future_outputs", []))),
        "per_ticker_approval_entries_12": (12, len(entries)),
        "per_ticker_approval_digests_present": (True, _per_ticker_digests_valid(entries)),
        "provider_requests_made_false": (False, approval.get("provider_requests_made_in_approval")),
        "market_data_acquisition_false": (False, approval.get("market_data_acquisition_performed_in_approval")),
        "dataset_regeneration_false": (False, approval.get("canonical_dataset_regenerated_in_approval")),
        "redesigned_label_regeneration_false": (False, approval.get("redesigned_label_regeneration_performed")),
        "feature_regeneration_false": (False, approval.get("feature_regeneration_performed")),
        "predictive_evidence_rerun_false": (False, approval.get("predictive_evidence_execution_rerun_performed")),
        "label_objective_redesign_execution_rerun_false": (False, approval.get("label_objective_redesign_execution_rerun_performed")),
        "metric_recomputation_in_approval_false": (False, approval.get("metric_recomputation_performed_in_approval")),
        "model_training_in_approval_false": (False, approval.get("model_training_performed_in_approval")),
        "raw_provider_payloads_not_committed": (False, approval.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, approval.get("api_keys_stored_or_printed")),
        "no_improved_evidence_planning_execution_created": (False, approval.get("improved_evidence_planning_execution_created")),
        "no_additional_predictive_evidence_execution_candidate_created": (False, approval.get("additional_predictive_evidence_execution_candidate_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, approval.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, approval.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, approval.get("runtime_migration_approval_created")),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "no_tracked_marketflow_files": (True, approval.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    approved = not failed
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "improved_evidence_planning_approved_by_operator": approved,
        "approval_scope": IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY,
        "selected_redesign_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        "improved_evidence_planning_authorized": approved,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": approved,
        "improved_evidence_planning_executed": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(approval))
    payload.pop(
        "improved_evidence_planning_approval_using_redesigned_evidence_digest",
        None,
    )
    return payload


def improved_evidence_planning_approval_using_redesigned_evidence_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    return semantic_digest(_digest_payload(approval))


def build_improved_evidence_planning_approved_using_redesigned_evidence_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build the attestation-gated approval without executing planning."""
    source = _source_review(candidate_review_package)
    _validate_attestation(operator_attestation)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval[
        "improved_evidence_planning_approval_using_redesigned_evidence_digest"
    ] = improved_evidence_planning_approval_using_redesigned_evidence_digest_v1(
        approval
    )
    validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(
        approval
    )
    return approval


def _reject_forbidden_values(value: Any, *, path: str = "approval") -> None:
    forbidden_artifacts = {
        "IMPROVED_EVIDENCE_PLANNING_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "improved_evidence_planning_executed",
        "improved_evidence_planning_execution_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_approval",
        "model_training_performed_in_approval",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(
    approval: dict,
) -> dict:
    """Fail closed unless the approval is exact and future-planning-only."""
    if not isinstance(approval, dict):
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "approval must be a JSON object"
        )
    _expect(approval.get("artifact_kind"), ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE, "artifact_kind")
    _expect(approval.get("schema_version"), SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_V1, "schema_version")
    _expect(approval.get("approval_status"), IMPROVED_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_EVIDENCE, "approval_status")
    _expect(approval.get("approval_scope"), IMPROVED_EVIDENCE_PLANNING_APPROVAL_ONLY, "approval_scope")
    _validate_attestation(approval.get("operator_attestation", {}))
    _reject_forbidden_values(approval)

    expected = {
        "source_candidate_review_artifact_kind": review_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "source_candidate_review_status": review_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "source_candidate_artifact_kind": review_service.candidate_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "source_candidate_status": review_service.candidate_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **BOUND_DIGESTS,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe_count": 12,
        "target_universe": TARGET_UNIVERSE,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "approved_candidate_basis": review_service.candidate_service.CANDIDATE_BASIS,
        "selected_direction": SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
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
        "improved_evidence_planning_objective": APPROVED_OBJECTIVE,
        "improved_evidence_planning_scope": APPROVED_SCOPE,
        "improved_evidence_planning_mode": APPROVED_MODE,
        "improved_evidence_planning_authority_status": APPROVED_AUTHORITY_STATUS,
        "approved_improved_evidence_themes": _approved_themes(
            review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
        ),
        "approved_planned_evidence_components": _approved_components(
            review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
        ),
        "approved_data_products": _approved_data_products(),
        "approved_future_outputs": _approved_future_outputs(
            review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
        ),
        "per_ticker_approval_entries": _per_ticker_approvals(
            review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
        ),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(approval.get(field), expected_value, field)

    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "label_objective_redesign_results_review_created", "label_objective_redesign_results_review_ready",
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence",
        "improved_evidence_planning_candidate_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review",
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created",
        "improved_evidence_planning_approved", "improved_evidence_planning_approval_created",
        "improved_evidence_planning_authorized",
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    ]
    false_fields = [
        "improved_evidence_planning_executed", "improved_evidence_planning_execution_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended", "profitability_acceptance_created",
        "runtime_migration_approved", "runtime_migration_active", "runtime_migration_approval_created",
        "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval", "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed", "metric_recomputation_performed_in_approval",
        "model_training_performed_in_approval", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    ]
    for field in true_fields:
        _expect(approval.get(field), True, field)
    for field in false_fields:
        _expect(approval.get(field), False, field)
    _expect(approval.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(approval.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approval.get(field), NOT_AUTHORIZED, field)

    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "approval_checklist mismatch"
        )
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "approval_checklist check ids")
    _expect(checklist, _checklist(approval), "approval_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "approval_checklist must pass"
        )
    _expect(approval.get("approval_summary"), _summary(checklist), "approval_summary")
    digest = approval.get(
        "improved_evidence_planning_approval_using_redesigned_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "missing approval digest"
        )
    _expect(digest, improved_evidence_planning_approval_using_redesigned_evidence_digest_v1(approval), "approval digest")
    return {
        "status": IMPROVED_EVIDENCE_PLANNING_APPROVAL_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "improved_evidence_planning_approval_using_redesigned_evidence_digest": digest,
        "blocker_count": approval["approval_summary"]["blocker_count"],
        "improved_evidence_planning_authorized": True,
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence": True,
        "improved_evidence_planning_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_improved_evidence_planning_approved_using_redesigned_evidence_markdown_v1(
    approval: dict,
) -> str:
    """Render the approval without implying planning execution or downstream use."""
    validation = validate_improved_evidence_planning_approved_using_redesigned_evidence_v1(
        approval
    )
    summary = approval["approval_summary"]
    operator = approval["operator_attestation"]
    lines = [
        "# MarketFlow Improved Evidence Planning Approval Status", "",
        "## Title", "- Optional Improved Evidence Planning Approval Using Redesigned Evidence v1.", "",
        "## Optional Improved Evidence Planning Approval Using Redesigned Evidence",
        f"- Artifact/status/scope/digest: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}` / `{validation['improved_evidence_planning_approval_using_redesigned_evidence_digest']}`.", "",
        "## Operator Attestation",
        f"- Non-secret reference `{operator['operator_reference']}` at `{operator['operator_attestation_timestamp_utc']}` used the exact required phrase and confirmations.", "",
        "## Source Candidate Review",
        f"- Review/candidate digests: `{approval['improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest']}` / `{approval['improved_evidence_planning_candidate_using_redesigned_evidence_digest']}`.", "",
        "## Bound Evidence",
        f"- Redesign review/execution/output/approval: `{approval['label_objective_redesign_results_review_using_redesigned_evidence_digest']}` / `{approval['label_objective_redesign_execution_using_redesigned_evidence_digest']}` / `{approval['label_objective_redesign_output_binding_digest']}` / `{approval['label_objective_redesign_approval_using_redesigned_evidence_digest']}`.", "",
        "## Dataset and Universe",
        f"- `{approval['dataset_name']}` has `{approval['total_canonical_record_count']}` frozen records for 12 ordered tickers; META remains `{approval['meta_record_count']}`.", "",
        "## Approved Candidate Basis",
        f"- Selected direction: `{approval['selected_direction']}`; the reviewed research-only basis is preserved.", "",
        "## Approved Objective",
        f"- `{approval['improved_evidence_planning_objective']}` / `{approval['improved_evidence_planning_mode']}` / `{approval['improved_evidence_planning_authority_status']}`.", "",
        "## Approved Improved Evidence Themes",
    ]
    lines.extend(f"- `{row['theme_id']}`: `{row['approval_status']}`." for row in approval["approved_improved_evidence_themes"])
    lines.extend(["", "## Approved Planned Evidence Components"])
    lines.extend(f"- `{row['component_id']}`: `{row['approval_status']}`." for row in approval["approved_planned_evidence_components"])
    lines.extend(["", "## Approved Data Products"])
    lines.extend(f"- `{row['data_product_id']}`: `{row['output_status']}`." for row in approval["approved_data_products"])
    lines.extend(["", "## Approved Future Outputs"])
    lines.extend(f"- `{row['future_output_id']}`: `{row['output_status']}`." for row in approval["approved_future_outputs"])
    lines.extend(["", "## Per-Ticker Approval Entries", "- Twelve digest-bound approvals preserve registry order; META remains 913 and every other ticker 1003.", "", "## Next Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1))
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in approval["next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in approval["risk_controls"])
    lines.extend([
        "", "## Predictive Usefulness Boundary", "- Predictive usefulness remains `not accepted`; no acceptance candidate is created.",
        "", "## Profitability Boundary", "- Profitability remains `not accepted`.",
        "", "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- This approval authorizes only a future research-only planning execution. It does not execute planning or create labels, targets, features, matrices, metrics, models, predictive evidence, recommendations, runtime actions, or trades.", "",
    ])
    return "\n".join(lines)


def write_improved_evidence_planning_approved_using_redesigned_evidence_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict:
    """Write one canonical approval JSON file without overwriting."""
    approval = build_improved_evidence_planning_approved_using_redesigned_evidence_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    output_name = filename or "improved_evidence_planning_approval_using_redesigned_evidence_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "approval filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(approval)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ImprovedEvidencePlanningApprovalRedesignedEvidenceError(
            "approval output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "approval_status": approval["approval_status"],
        "improved_evidence_planning_approval_using_redesigned_evidence_digest": approval[
            "improved_evidence_planning_approval_using_redesigned_evidence_digest"
        ],
    }
