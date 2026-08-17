"""Offline operator approval for future redesigned-label generation only."""

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
    redesigned_label_generation_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_APPROVED = (
    "REDESIGNED_LABEL_GENERATION_APPROVED"
)
SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_APPROVAL_V1 = (
    "redesigned_label_generation_approval_v1"
)
REDESIGNED_LABEL_GENERATION_APPROVED = "REDESIGNED_LABEL_GENERATION_APPROVED"
REDESIGNED_LABEL_GENERATION_APPROVAL_VALID = (
    "REDESIGNED_LABEL_GENERATION_APPROVAL_VALID"
)
REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY = (
    "REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_REDESIGNED_LABEL_GENERATION = (
    "APPROVE_REDESIGNED_LABEL_GENERATION"
)
OPERATOR_ATTESTATION_VERSION_REDESIGNED_LABEL_GENERATION_APPROVAL_V1 = (
    "redesigned_label_generation_approval_operator_attestation_v1"
)
REQUIRED_REDESIGNED_LABEL_GENERATION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE REDESIGNED LABEL GENERATION MSFT NVDA AMZN GOOGL META TSLA JPM "
    "XOM JNJ WMT CAT LMT REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY"
)

EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "e9dfaa21fe643e6e25762d7f00939763d766d3a4ebeaffb3a12895abab7f2c52"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "bda6012c74cffb8841a6b9568c0985e2b6d1c337c7b7fcf892da4b724fcb15f9"
)
EXPECTED_EXECUTION_DIGEST = (
    "d43bb214850f8068b445d1620ae8f4f948162eda309f04acf6fdd7b73abd63a4"
)
EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    "8ca1dee0aa2c175a1ab5bf7f9ba724b8dc0df6e2057e4f97721bad02f4adaff0"
)
EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST = (
    "2f771999ff5e31dbd959ea1a33b08852cda46913ff1b5dfc6fe17bc0853ee14a"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED

APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY = (
    "APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY"
)
APPROVED_FOR_FUTURE_THRESHOLD_COMPUTATION_ONLY = (
    "APPROVED_FOR_FUTURE_THRESHOLD_COMPUTATION_ONLY"
)
APPROVED_FOR_FUTURE_HORIZON_EVALUATION_ONLY = (
    "APPROVED_FOR_FUTURE_HORIZON_EVALUATION_ONLY"
)
APPROVED_FOR_FUTURE_LABEL_AVAILABILITY_HANDLING_ONLY = (
    "APPROVED_FOR_FUTURE_LABEL_AVAILABILITY_HANDLING_ONLY"
)
NOT_GENERATED = "NOT_GENERATED"
NOT_EXECUTED = "NOT_EXECUTED"

REQUIRED_DIGEST_FIELDS = {
    "redesigned_label_generation_candidate_review_package_digest": (
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
    ),
    "redesigned_label_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
    "label_objective_redesign_results_review_package_digest": (
        EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
    ),
    "label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
    "label_objective_redesign_execution_approval_digest": (
        EXPECTED_EXECUTION_APPROVAL_DIGEST
    ),
    "operator_method_path_selection_digest": (
        EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST
    ),
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_source_design_artifacts_reviewed",
    "operator_confirms_redesigned_label_generation_approval_scope_only",
    "operator_confirms_redesigned_label_generation_authorized",
    "operator_confirms_ready_for_redesigned_label_generation_execution",
    "operator_confirms_no_redesigned_label_generation_performed",
    "operator_confirms_no_actual_redesigned_labels_generated",
    "operator_confirms_no_feature_generation_authorization",
    "operator_confirms_no_feature_generation",
    "operator_confirms_no_additional_predictive_evidence_execution_candidate",
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

NEXT_CHAIN = [
    "Redesigned Label Generation Execution v1.",
    "Redesigned Label Generation Results Review v1.",
    "Feature / Predictive Evidence Planning Candidate using redesigned labels, if results support it.",
    "Additional Predictive Evidence Execution Candidate using redesigned labels, if separately selected.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "redesigned_label_generation_execution",
    "redesigned_label_generation_results_review",
    "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "approval_does_not_generate_labels_now",
    "approval_does_not_authorize_feature_generation",
    "approval_does_not_authorize_predictive_evidence_execution",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_label_generation_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

CHECK_IDS = [
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "label_objective_redesign_results_review_digest_bound",
    "label_objective_redesign_execution_digest_bound",
    "label_objective_redesign_execution_approval_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_review_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_required_digests",
    "operator_confirms_source_design_artifacts_reviewed",
    "approval_scope_redesigned_label_generation_only",
    "redesigned_label_generation_approved_true",
    "redesigned_label_generation_authorized_true",
    "ready_for_redesigned_label_generation_execution_true",
    "redesigned_label_generation_performed_false",
    "actual_redesigned_labels_generated_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "approved_label_generation_inputs_8",
    "approved_label_families_10",
    "approved_threshold_strategies_7",
    "approved_horizon_strategies_5",
    "approved_availability_rules_8",
    "per_ticker_approval_entries_12",
    "per_ticker_approval_digests_present",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "label_generation_false",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "runtime_activation_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "no_redesigned_label_generation_execution_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class RedesignedLabelGenerationApprovalError(ValueError):
    """Raised when the approval or its source evidence is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise RedesignedLabelGenerationApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise RedesignedLabelGenerationApprovalError(f"{field} must be true")


def build_redesigned_label_generation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_redesigned_label_generation_candidate_review_digest: str,
    operator_confirms_redesigned_label_generation_candidate_digest: str,
    operator_confirms_label_objective_redesign_results_review_digest: str,
    operator_confirms_label_objective_redesign_execution_digest: str,
    operator_confirms_label_objective_redesign_execution_approval_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_source_design_artifacts_reviewed: bool,
    operator_confirms_redesigned_label_generation_approval_scope_only: bool,
    operator_confirms_redesigned_label_generation_authorized: bool,
    operator_confirms_ready_for_redesigned_label_generation_execution: bool,
    operator_confirms_no_redesigned_label_generation_performed: bool,
    operator_confirms_no_actual_redesigned_labels_generated: bool,
    operator_confirms_no_feature_generation_authorization: bool,
    operator_confirms_no_feature_generation: bool,
    operator_confirms_no_additional_predictive_evidence_execution_candidate: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_REDESIGNED_LABEL_GENERATION,
) -> dict:
    """Build the complete non-secret operator attestation object."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_REDESIGNED_LABEL_GENERATION_APPROVAL_V1
        )
    }


def _expected_attestation_digests() -> dict[str, str]:
    return {
        "operator_confirms_redesigned_label_generation_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_redesigned_label_generation_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_label_objective_redesign_results_review_digest": EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_label_objective_redesign_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "operator_confirms_label_objective_redesign_execution_approval_digest": EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise RedesignedLabelGenerationApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_REDESIGNED_LABEL_GENERATION,
        "operator_attestation_phrase": REQUIRED_REDESIGNED_LABEL_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_REDESIGNED_LABEL_GENERATION_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        **_expected_attestation_digests(),
    }
    for field, expected_value in expected.items():
        _expect(attestation.get(field), expected_value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise RedesignedLabelGenerationApprovalError(f"{field} required")


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        review_service.build_redesigned_label_generation_candidate_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        validation = review_service.validate_redesigned_label_generation_candidate_review_package_v1(
            package
        )
    except review_service.RedesignedLabelGenerationCandidateReviewError as exc:
        raise RedesignedLabelGenerationApprovalError(
            "source candidate review package is invalid"
        ) from exc
    _expect(
        package.get("redesigned_label_generation_candidate_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source candidate review status",
    )
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source blockers")
    _expect(
        validation.get("redesigned_label_generation_candidate_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "validated source candidate review digest",
    )
    return package


def _approved_inputs(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": row["source_input_id"],
            "output_label": row["output_label"],
            "approval_status": APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY,
            "generation_status": NOT_GENERATED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_redesigned_label_generation_inputs"]
    ]


def _approved_families(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "planned_label_family_id": row["planned_label_family_id"],
            "approval_status": APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY,
            "label_generation_authorized": True,
            "label_generation_performed": False,
            "actual_label_values_created": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_redesigned_label_families"]
    ]


def _approved_thresholds(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "threshold_strategy_id": row["threshold_strategy_id"],
            "approval_status": APPROVED_FOR_FUTURE_THRESHOLD_COMPUTATION_ONLY,
            "threshold_computation_authorized": True,
            "threshold_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_threshold_strategies"]
    ]


def _approved_horizons(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "horizon_strategy_id": row["horizon_strategy_id"],
            "approval_status": APPROVED_FOR_FUTURE_HORIZON_EVALUATION_ONLY,
            "horizon_selection_authorized": True,
            "horizon_selection_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_horizon_strategies"]
    ]


def _approved_rules(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "availability_rule_id": row["availability_rule_id"],
            "approval_status": APPROVED_FOR_FUTURE_LABEL_AVAILABILITY_HANDLING_ONLY,
            "execution_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_planned_label_availability_rules"]
    ]


def per_ticker_redesigned_label_generation_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker approval entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_redesigned_label_generation_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_review_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "source_label_objective_plan_status": row[
                "source_label_objective_plan_status"
            ],
            "redesigned_label_generation_candidate_status": (
                "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT"
            ),
            "redesigned_label_generation_approval_status": (
                APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY
            ),
            "redesigned_label_generation_authorized": True,
            "redesigned_label_generation_performed": False,
            "actual_redesigned_labels_generated": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_redesigned_label_generation_candidate_review_digest": row[
                "per_ticker_redesigned_label_generation_candidate_review_digest"
            ],
            "source_redesigned_label_generation_candidate_digest": row[
                "per_ticker_redesigned_label_generation_candidate_digest"
            ],
        }
        if row["ticker"] == "META":
            entry["label_availability_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_NO_BACKFILL_OR_SYNTHETIC_LABELS"
            )
        entry["per_ticker_redesigned_label_generation_approval_digest"] = (
            per_ticker_redesigned_label_generation_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_approval(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_APPROVED,
        "schema_version": SCHEMA_VERSION_REDESIGNED_LABEL_GENERATION_APPROVAL_V1,
        "approval_status": REDESIGNED_LABEL_GENERATION_APPROVED,
        "approval_scope": REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
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
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "ready_for_redesigned_label_generation_execution": True,
        "redesigned_label_generation_performed": False,
        "actual_redesigned_labels_generated": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
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
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "canonical_dataset_regenerated": False,
        "label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "redesigned_label_generation_execution_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        "operator_attestation": deepcopy(dict(attestation)),
        **REQUIRED_DIGEST_FIELDS,
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
        "redesigned_label_generation_objective": (
            "GENERATE_REDESIGNED_LABELS_FROM_REVIEWED_LABEL_OBJECTIVE_DESIGN_ARTIFACTS"
        ),
        "redesigned_label_generation_scope": (
            REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY
        ),
        "redesigned_label_generation_mode": "AUTHORIZED_NOT_GENERATED",
        "redesigned_label_generation_authority_status": (
            "AUTHORIZED_FOR_FUTURE_REDESIGNED_LABEL_GENERATION_ONLY"
        ),
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
        "approved_label_generation_inputs": _approved_inputs(source),
        "approved_redesigned_label_families": _approved_families(source),
        "approved_threshold_strategies": _approved_thresholds(source),
        "approved_horizon_strategies": _approved_horizons(source),
        "approved_availability_rules": _approved_rules(source),
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
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _derived_checks(approval: dict[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    inputs = approval.get("approved_label_generation_inputs", [])
    families = approval.get("approved_redesigned_label_families", [])
    thresholds = approval.get("approved_threshold_strategies", [])
    horizons = approval.get("approved_horizon_strategies", [])
    rules = approval.get("approved_availability_rules", [])
    entries = approval.get("per_ticker_approval_entries", [])
    confirmed = _expected_attestation_digests()
    return {
        "candidate_review_digest_bound": approval.get("redesigned_label_generation_candidate_review_package_digest") == EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "candidate_digest_bound": approval.get("redesigned_label_generation_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "label_objective_redesign_results_review_digest_bound": approval.get("label_objective_redesign_results_review_package_digest") == EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST,
        "label_objective_redesign_execution_digest_bound": approval.get("label_objective_redesign_execution_digest") == EXPECTED_EXECUTION_DIGEST,
        "label_objective_redesign_execution_approval_digest_bound": approval.get("label_objective_redesign_execution_approval_digest") == EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "research_registry_digest_bound": approval.get("research_registry_approval_digest") == EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": approval.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": approval.get("target_universe_count") == 12 and approval.get("target_universe") == TARGET_UNIVERSE,
        "target_universe_matches_review_universe": approval.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": approval.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": approval.get("meta_record_count") == 913 and approval.get("non_meta_record_count") == 1003 and approval.get("meta_reduced_record_count_preserved") is True,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION_APPROVE_REDESIGNED_LABEL_GENERATION,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_REDESIGNED_LABEL_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_all_required_digests": all(attestation.get(field) == value for field, value in confirmed.items()),
        "operator_confirms_source_design_artifacts_reviewed": attestation.get("operator_confirms_source_design_artifacts_reviewed") is True,
        "approval_scope_redesigned_label_generation_only": approval.get("approval_scope") == REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY,
        "redesigned_label_generation_approved_true": approval.get("redesigned_label_generation_approved") is True,
        "redesigned_label_generation_authorized_true": approval.get("redesigned_label_generation_authorized") is True,
        "ready_for_redesigned_label_generation_execution_true": approval.get("ready_for_redesigned_label_generation_execution") is True,
        "redesigned_label_generation_performed_false": approval.get("redesigned_label_generation_performed") is False,
        "actual_redesigned_labels_generated_false": approval.get("actual_redesigned_labels_generated") is False,
        "feature_generation_authorized_false": approval.get("redesigned_feature_generation_authorized") is False,
        "feature_generation_performed_false": approval.get("redesigned_feature_generation_performed") is False and approval.get("feature_generation_performed") is False,
        "additional_predictive_evidence_execution_candidate_created_false": approval.get("additional_predictive_evidence_execution_candidate_created") is False,
        "approved_label_generation_inputs_8": len(inputs) == 8 and all(row.get("approval_status") == APPROVED_FOR_FUTURE_LABEL_GENERATION_ONLY and row.get("generation_status") == NOT_GENERATED for row in inputs if isinstance(row, dict)),
        "approved_label_families_10": len(families) == 10 and all(row.get("label_generation_authorized") is True and row.get("label_generation_performed") is False and row.get("actual_label_values_created") is False for row in families if isinstance(row, dict)),
        "approved_threshold_strategies_7": len(thresholds) == 7 and all(row.get("threshold_computation_authorized") is True and row.get("threshold_computation_performed") is False for row in thresholds if isinstance(row, dict)),
        "approved_horizon_strategies_5": len(horizons) == 5 and all(row.get("horizon_selection_authorized") is True and row.get("horizon_selection_performed") is False for row in horizons if isinstance(row, dict)),
        "approved_availability_rules_8": len(rules) == 8 and all(row.get("execution_status") == NOT_EXECUTED for row in rules if isinstance(row, dict)),
        "per_ticker_approval_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries if isinstance(row, dict)] == TARGET_UNIVERSE,
        "per_ticker_approval_digests_present": len(entries) == 12 and all(isinstance(row.get("per_ticker_redesigned_label_generation_approval_digest"), str) and len(row["per_ticker_redesigned_label_generation_approval_digest"]) == 64 and row["per_ticker_redesigned_label_generation_approval_digest"] == per_ticker_redesigned_label_generation_approval_digest_v1(row) for row in entries if isinstance(row, dict)),
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": approval.get("runtime_migration_approved") is False and approval.get("runtime_migration_active") is False and approval.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": approval.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": approval.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": approval.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": approval.get("provider_requests_made") is False and approval.get("live_provider_transport_enabled") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": approval.get("dataset_regeneration_performed") is False and approval.get("canonical_dataset_regenerated") is False,
        "label_generation_false": approval.get("label_generation_performed") is False and approval.get("redesigned_label_generation_performed") is False,
        "feature_generation_false": approval.get("feature_generation_performed") is False and approval.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": approval.get("metric_recomputation_performed") is False,
        "model_training_false": approval.get("model_training_performed") is False,
        "strategy_scoring_false": approval.get("new_strategy_scoring_performed") is False,
        "runtime_activation_false": approval.get("runtime_migration_active") is False,
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed") is False,
        "no_redesigned_label_generation_execution_created": approval.get("redesigned_label_generation_execution_created") is False,
        "no_additional_predictive_evidence_execution_candidate_created": approval.get("additional_predictive_evidence_execution_candidate_created") is False,
        "no_predictive_usefulness_acceptance_artifact_created": approval.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": approval.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": approval.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True and approval.get("tracked_marketflow_files") == [],
    }


def _checklist(approval: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(approval)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


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
        "redesigned_label_generation_approved_by_operator": blockers == 0,
        "approval_scope": REDESIGNED_LABEL_GENERATION_APPROVAL_ONLY,
        "redesigned_label_generation_authorized": blockers == 0,
        "ready_for_redesigned_label_generation_execution": blockers == 0,
        "redesigned_label_generation_performed": False,
        "actual_redesigned_labels_generated": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def redesigned_label_generation_approval_digest_v1(approval: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the approval."""
    payload = deepcopy(approval)
    payload.pop("redesigned_label_generation_approval_digest", None)
    return semantic_digest(payload)


def _reject_forbidden_authority(value: Any, *, path: str = "approval") -> None:
    forbidden_artifacts = {
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
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
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
        "label_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "redesigned_label_generation_execution_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
        "actual_label_values_created",
        "threshold_computation_performed",
        "horizon_selection_performed",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise RedesignedLabelGenerationApprovalError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true_fields and item is True:
                raise RedesignedLabelGenerationApprovalError(
                    f"{current} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise RedesignedLabelGenerationApprovalError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise RedesignedLabelGenerationApprovalError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def build_redesigned_label_generation_approved_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build the attested approval without performing label generation."""
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["redesigned_label_generation_approval_digest"] = (
        redesigned_label_generation_approval_digest_v1(approval)
    )
    validate_redesigned_label_generation_approved_v1(approval)
    return approval


def validate_redesigned_label_generation_approved_v1(approval: dict) -> dict:
    """Validate the exact source, attestation, digest, and closed gates."""
    if not isinstance(approval, dict):
        raise RedesignedLabelGenerationApprovalError(
            "approval must be a JSON object"
        )
    _reject_forbidden_authority(approval)
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected_base = _base_approval(_source_review(None), attestation)
    for field, expected in expected_base.items():
        _expect(approval.get(field), expected, field)
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise RedesignedLabelGenerationApprovalError("approval_checklist missing")
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        CHECK_IDS,
        "approval_checklist check IDs",
    )
    expected_checklist = _checklist(approval)
    _expect(checklist, expected_checklist, "approval_checklist")
    if any(row["status"] != PASS for row in expected_checklist):
        raise RedesignedLabelGenerationApprovalError(
            "approval_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(approval.get("approval_summary"), expected_summary, "approval_summary")
    digest = approval.get("redesigned_label_generation_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise RedesignedLabelGenerationApprovalError(
            "redesigned label generation approval digest missing"
        )
    _expect(
        digest,
        redesigned_label_generation_approval_digest_v1(approval),
        "redesigned_label_generation_approval_digest",
    )
    return {
        "status": REDESIGNED_LABEL_GENERATION_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "redesigned_label_generation_approval_digest": digest,
        "redesigned_label_generation_approved": True,
        "redesigned_label_generation_authorized": True,
        "ready_for_redesigned_label_generation_execution": True,
        "redesigned_label_generation_performed": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_redesigned_label_generation_approved_markdown_v1(
    approval: dict,
) -> str:
    """Render a validated, non-secret approval summary."""
    validate_redesigned_label_generation_approved_v1(approval)
    operator = approval["operator_attestation"]
    summary = approval["approval_summary"]
    lines = [
        "# MarketFlow Redesigned Label Generation Approval",
        "",
        "## Title",
        "- Redesigned Label Generation Approval v1.",
        "",
        "## Redesigned Label Generation Approval",
        f"- Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.",
        "",
        "## Operator Attestation",
        f"- Decision: `{operator['operator_decision']}`.",
        f"- Reference/timestamp/version: `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}` / `{operator['operator_attestation_version']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(f"- {field}: `{approval[field]}`." for field in REQUIRED_DIGEST_FIELDS)
    lines.extend([
        "", "## Dataset and Universe",
        f"- Dataset: `{approval['dataset_name']}`; records: `{approval['total_canonical_record_count']}`.",
        f"- Universe: `{', '.join(approval['target_universe'])}`; META records: `{approval['meta_record_count']}`.",
        "", "## Approved Source Design Artifacts",
        f"- `{approval['source_label_objective_redesign_output_count']}` artifacts at `{approval['source_label_objective_redesign_output_root']}` remain `{approval['source_label_objective_redesign_output_status']}`.",
    ])
    for heading, key, id_key in [
        ("Approved Label Generation Inputs", "approved_label_generation_inputs", "source_input_id"),
        ("Approved Redesigned Label Families", "approved_redesigned_label_families", "planned_label_family_id"),
        ("Approved Threshold Strategies", "approved_threshold_strategies", "threshold_strategy_id"),
        ("Approved Horizon Strategies", "approved_horizon_strategies", "horizon_strategy_id"),
        ("Approved Availability Rules", "approved_availability_rules", "availability_rule_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{row[id_key]}`." for row in approval[key])
    lines.extend(["", "## Per-Ticker Approval Entries"])
    lines.extend(
        f"- `{row['ticker']}`: future label generation approved; no label values generated."
        for row in approval["per_ticker_approval_entries"]
    )
    for heading, key in [
        ("Next Chain", "next_chain"),
        ("Next Gates", "next_gates"),
        ("Risk Controls", "risk_controls"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in approval[key])
    lines.extend([
        "", "## Checklist Summary",
        f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "", "## Guardrails",
        "- Approval authorizes future redesigned-label generation only; it does not generate labels, authorize feature or predictive-evidence work, accept predictive usefulness or profitability, activate runtime, or authorize trading.",
        "",
    ])
    return "\n".join(lines)


def write_redesigned_label_generation_approved_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict:
    """Write one canonical approval artifact without overwriting."""
    approval = build_redesigned_label_generation_approved_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_redesigned_label_generation_approved_v1(approval)
    output_name = filename or "redesigned_label_generation_approval_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise RedesignedLabelGenerationApprovalError(
            "approval filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    if path.exists():
        raise RedesignedLabelGenerationApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
