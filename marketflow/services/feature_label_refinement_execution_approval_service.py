"""Offline operator approval for future feature/label refinement execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_label_refinement_execution_candidate_operator_review_service as review_service


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1 = (
    "feature_label_refinement_execution_approval_v1"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_VALID = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_VALID"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION = (
    "APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION"
)
OPERATOR_ATTESTATION_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1 = (
    "feature_label_refinement_execution_approval_operator_attestation_v1"
)
REQUIRED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE FEATURE LABEL REFINEMENT EXECUTION MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY"
)

EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "e6f72e45d85d58759d8f35518c1d5e6795b02923acb43f9170c5cc34a810d9ef"
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = review_service.EXPECTED_EXECUTION_CANDIDATE_DIGEST
EXPECTED_PLAN_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_PLAN_APPROVAL_DIGEST
)
EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    review_service.candidate_service.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PLAN_CANDIDATE_DIGEST = (
    review_service.candidate_service.EXPECTED_PLAN_CANDIDATE_DIGEST
)
EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    review_service.candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST = (
    review_service.candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST
)
EXPECTED_READINESS_REVIEW_DIGEST = (
    review_service.candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
)
EXPECTED_REASSESSMENT_REVIEW_DIGEST = (
    review_service.candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST
)
EXPECTED_RESULTS_REVIEW_DIGEST = (
    review_service.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
)
EXPECTED_EXECUTION_DIGEST = review_service.candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    review_service.candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    review_service.candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = review_service.candidate_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
NOT_EXECUTED = "NOT_EXECUTED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
AUTHORIZED_FOR_FUTURE_REFINEMENT_EXECUTION_ONLY = (
    "AUTHORIZED_FOR_FUTURE_REFINEMENT_EXECUTION_ONLY"
)
EXECUTION_OBJECTIVE = "EXECUTE_FEATURE_LABEL_REFINEMENT_FOR_APPROVED_PLAN"
EXECUTION_SCOPE = FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY
EXECUTION_MODE = AUTHORIZED_NOT_EXECUTED
EXECUTION_AUTHORITY_STATUS = AUTHORIZED_FOR_FUTURE_REFINEMENT_EXECUTION_ONLY

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_readiness_decision_not_ready",
    "operator_confirms_execution_approval_scope_only",
    "operator_confirms_execution_authorized",
    "operator_confirms_refined_label_generation_authorized",
    "operator_confirms_refined_feature_generation_authorized",
    "operator_confirms_refined_walk_forward_validation_authorized",
    "operator_confirms_refined_out_of_sample_evaluation_authorized",
    "operator_confirms_refined_metrics_recomputation_authorized",
    "operator_confirms_model_comparison_authorized",
    "operator_confirms_no_refinement_execution_performed",
    "operator_confirms_no_refinement_results_created",
    "operator_confirms_no_refined_label_generation_performed",
    "operator_confirms_no_refined_feature_generation_performed",
    "operator_confirms_no_refined_walk_forward_validation_performed",
    "operator_confirms_no_refined_out_of_sample_evaluation_performed",
    "operator_confirms_no_refined_metrics_recomputation_performed",
    "operator_confirms_no_model_comparison_performed",
    "operator_confirms_no_additional_predictive_evidence_execution_candidate",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

NEXT_CHAIN = [
    "Feature/Label Refinement Execution.",
    "Feature/Label Refinement Results Review Package.",
    "Additional Predictive Evidence Execution Candidate for refined evidence.",
    "Additional Predictive Evidence Execution Approval Ceremony, if required.",
    "Additional Predictive Evidence Execution.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment Review rerun.",
    "Predictive Usefulness Acceptance Readiness Review rerun.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_refinement_execution",
    "feature_label_refinement_results_review",
    "additional_predictive_evidence_execution_candidate_for_refined_evidence",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_review_rerun",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_approval_does_not_execute_refinement",
    "no_predictive_usefulness_acceptance_from_execution_approval",
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
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
]
LIMITATIONS = [
    "approval_is_not_refinement_execution",
    "approval_authorizes_future_refinement_execution_only",
    "refinement_results_not_created",
    "approved_label_generation_not_performed",
    "approved_feature_generation_not_performed",
    "approved_validation_oos_metrics_not_performed",
    "approved_model_comparison_not_performed",
    "additional_predictive_evidence_execution_candidate_not_created",
    "readiness_remains_not_ready",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "meta_reduced_record_count_preserved",
]

REQUIRED_CHECK_IDS = [
    "execution_candidate_review_digest_matches_expected",
    "execution_candidate_review_has_zero_blockers",
    "execution_candidate_digest_bound",
    "plan_approval_digest_bound",
    "plan_candidate_review_digest_bound",
    "plan_candidate_digest_bound",
    "readiness_review_digest_bound",
    "results_review_digest_bound",
    "execution_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_candidate_review_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_readiness_decision_not_ready",
    "operator_confirms_readiness_reason",
    "approval_scope_feature_label_refinement_execution_only",
    "feature_label_refinement_execution_approved_true",
    "feature_label_refinement_execution_authorized_true",
    "ready_for_feature_label_refinement_execution_true",
    "refined_label_generation_authorized_true",
    "refined_feature_generation_authorized_true",
    "refined_walk_forward_validation_authorized_true",
    "refined_out_of_sample_evaluation_authorized_true",
    "refined_metrics_recomputation_authorized_true",
    "model_comparison_authorized_true",
    "feature_label_refinement_executed_false",
    "feature_label_refinement_results_created_false",
    "refined_label_generation_performed_false",
    "refined_feature_generation_performed_false",
    "refined_walk_forward_validation_performed_false",
    "refined_out_of_sample_evaluation_performed_false",
    "refined_metrics_recomputation_performed_false",
    "model_comparison_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "approved_execution_steps_13",
    "approved_label_refinement_groups_7",
    "approved_feature_refinement_groups_9",
    "approved_protocol_refinement_groups_6",
    "approved_model_comparison_groups_5",
    "future_outputs_12_authorized_not_generated",
    "per_ticker_execution_approval_entries_12",
    "per_ticker_execution_approval_digests_present",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "market_data_acquisition_performed_in_approval_false",
    "dataset_generation_performed_in_approval_false",
    "canonical_dataset_regenerated_in_approval_false",
    "predictive_execution_rerun_performed_false",
    "label_generation_rerun_performed_false",
    "feature_matrix_rerun_performed_false",
    "walk_forward_validation_rerun_performed_false",
    "out_of_sample_evaluation_rerun_performed_false",
    "metrics_recomputation_performed_false",
    "improvement_execution_performed_false",
    "refinement_option_execution_performed_false",
    "label_refinement_execution_performed_false",
    "feature_refinement_execution_performed_false",
    "protocol_refinement_execution_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "approval_creates_predictive_usefulness_acceptance_false",
    "approval_creates_profitability_acceptance_false",
    "approval_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_feature_label_refinement_execution_artifact_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class FeatureLabelRefinementExecutionApprovalError(ValueError):
    """Raised when execution approval evidence violates its ceremony contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementExecutionApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise FeatureLabelRefinementExecutionApprovalError(f"{field} must be true")


def build_feature_label_refinement_execution_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_feature_label_refinement_execution_candidate_review_digest: str,
    operator_confirms_feature_label_refinement_execution_candidate_digest: str,
    operator_confirms_feature_label_refinement_plan_approval_digest: str,
    operator_confirms_feature_label_refinement_plan_candidate_review_digest: str,
    operator_confirms_readiness_review_digest: str,
    operator_confirms_results_review_digest: str,
    operator_confirms_execution_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_readiness_decision_not_ready: bool,
    operator_confirms_readiness_reason: str,
    operator_confirms_execution_approval_scope_only: bool,
    operator_confirms_execution_authorized: bool,
    operator_confirms_refined_label_generation_authorized: bool,
    operator_confirms_refined_feature_generation_authorized: bool,
    operator_confirms_refined_walk_forward_validation_authorized: bool,
    operator_confirms_refined_out_of_sample_evaluation_authorized: bool,
    operator_confirms_refined_metrics_recomputation_authorized: bool,
    operator_confirms_model_comparison_authorized: bool,
    operator_confirms_no_refinement_execution_performed: bool,
    operator_confirms_no_refinement_results_created: bool,
    operator_confirms_no_refined_label_generation_performed: bool,
    operator_confirms_no_refined_feature_generation_performed: bool,
    operator_confirms_no_refined_walk_forward_validation_performed: bool,
    operator_confirms_no_refined_out_of_sample_evaluation_performed: bool,
    operator_confirms_no_refined_metrics_recomputation_performed: bool,
    operator_confirms_no_model_comparison_performed: bool,
    operator_confirms_no_additional_predictive_evidence_execution_candidate: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION,
) -> dict[str, Any]:
    """Build a non-secret operator attestation; approval validates every field."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1
        )
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_feature_label_refinement_execution_candidate_review_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_feature_label_refinement_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "operator_confirms_feature_label_refinement_plan_approval_digest": EXPECTED_PLAN_APPROVAL_DIGEST,
        "operator_confirms_feature_label_refinement_plan_candidate_review_digest": EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_readiness_review_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "operator_confirms_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise FeatureLabelRefinementExecutionApprovalError(
            "operator_attestation missing"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION,
        "operator_attestation_phrase": REQUIRED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
        **_expected_digest_confirmations(),
    }
    for field, expected_value in expected.items():
        _expect(attestation.get(field), expected_value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise FeatureLabelRefinementExecutionApprovalError(f"{field} required")


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        review_service.build_feature_label_refinement_execution_candidate_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        validation = review_service.validate_feature_label_refinement_execution_candidate_review_package_v1(
            package
        )
    except review_service.FeatureLabelRefinementExecutionCandidateReviewPackageError as exc:
        raise FeatureLabelRefinementExecutionApprovalError(
            "source feature/label refinement execution candidate review is invalid"
        ) from exc
    _expect(
        package.get(
            "feature_label_refinement_execution_candidate_review_package_digest"
        ),
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source execution candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source execution candidate review status",
    )
    _expect(
        package.get("review_summary", {}).get("blocker_count"),
        0,
        "source execution candidate review blocker_count",
    )
    _expect(
        validation.get(
            "feature_label_refinement_execution_candidate_review_package_digest"
        ),
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "validated source execution candidate review digest",
    )
    return package


def _approved_steps(source_steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "step_id": row["step_id"],
            "authorization_status": AUTHORIZED_NOT_EXECUTED,
            "execution_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source_steps
    ]


def _approved_groups(source_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "group_id": row["group_id"],
            "authorization_status": AUTHORIZED_NOT_EXECUTED,
            "execution_status": NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source_groups
    ]


def _future_outputs(source_outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "output_name": row["output_name"],
            "generation_status": AUTHORIZED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for row in source_outputs
    ]


def per_ticker_feature_label_refinement_execution_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker execution approval."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_label_refinement_execution_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for row in source["per_ticker_execution_candidate_review_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row[
                "meta_reduced_record_count_flag"
            ],
            "readiness_status": "NOT_READY",
            "feature_label_refinement_execution_approval_status": (
                AUTHORIZED_FOR_FUTURE_REFINEMENT_EXECUTION_ONLY
            ),
            "feature_label_refinement_execution_authorized": True,
            "feature_label_refinement_executed": False,
            "refined_label_generation_authorized": True,
            "refined_label_generation_performed": False,
            "refined_feature_generation_authorized": True,
            "refined_feature_generation_performed": False,
            "model_comparison_authorized": True,
            "model_comparison_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_label_refinement_execution_candidate_review_digest": (
                EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
            "source_feature_label_refinement_execution_candidate_digest": (
                EXPECTED_EXECUTION_CANDIDATE_DIGEST
            ),
        }
        if row["ticker"] == "META":
            entry["refinement_note"] = row["refinement_note"]
        entry["per_ticker_feature_label_refinement_execution_approval_digest"] = (
            per_ticker_feature_label_refinement_execution_approval_digest_v1(entry)
        )
        approvals.append(entry)
    return approvals


def _base_artifact(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1,
        "approval_status": FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED,
        "approval_scope": FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "predictive_execution_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_matrix_rerun_performed": False,
        "walk_forward_validation_rerun_performed": False,
        "out_of_sample_evaluation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "improvement_execution_performed": False,
        "refinement_option_execution_performed": False,
        "label_refinement_execution_performed": False,
        "feature_refinement_execution_performed": False,
        "protocol_refinement_execution_performed": False,
        "model_comparison_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_plan_approved": True,
        "feature_label_refinement_plan_approval_created": True,
        "feature_label_refinement_execution_candidate_created": True,
        "feature_label_refinement_execution_candidate_review_created": True,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "ready_for_feature_label_refinement_execution": True,
        "feature_label_refinement_executed": False,
        "feature_label_refinement_results_created": False,
        "refined_label_generation_authorized": True,
        "refined_label_generation_performed": False,
        "refined_feature_generation_authorized": True,
        "refined_feature_generation_performed": False,
        "refined_walk_forward_validation_authorized": True,
        "refined_walk_forward_validation_performed": False,
        "refined_out_of_sample_evaluation_authorized": True,
        "refined_out_of_sample_evaluation_performed": False,
        "refined_metrics_recomputation_authorized": True,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_authorized": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
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
        "feature_label_refinement_execution_candidate_review_package_digest": source[
            "feature_label_refinement_execution_candidate_review_package_digest"
        ],
        "feature_label_refinement_execution_candidate_digest": source[
            "feature_label_refinement_execution_candidate_digest"
        ],
        "feature_label_refinement_plan_approval_digest": source[
            "feature_label_refinement_plan_approval_digest"
        ],
        "feature_label_refinement_plan_candidate_review_package_digest": source[
            "feature_label_refinement_plan_candidate_review_package_digest"
        ],
        "feature_label_refinement_plan_candidate_digest": source[
            "feature_label_refinement_plan_candidate_digest"
        ],
        "predictive_evidence_improvement_candidate_review_package_digest": source[
            "predictive_evidence_improvement_candidate_review_package_digest"
        ],
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
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "records_digest": source["records_digest"],
        "source_execution_candidate_review_blocker_count": source["review_summary"][
            "blocker_count"
        ],
        "target_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "feature_label_refinement_execution_objective": EXECUTION_OBJECTIVE,
        "feature_label_refinement_execution_scope": EXECUTION_SCOPE,
        "feature_label_refinement_execution_mode": EXECUTION_MODE,
        "feature_label_refinement_execution_authority_status": (
            EXECUTION_AUTHORITY_STATUS
        ),
        "readiness_failure_basis": deepcopy(
            source["reviewed_readiness_failure_basis"]
        ),
        "approved_execution_steps": _approved_steps(
            source["reviewed_planned_execution_steps"]
        ),
        "approved_label_refinement_execution_groups": _approved_groups(
            source["reviewed_label_refinement_execution_groups"]
        ),
        "approved_feature_refinement_execution_groups": _approved_groups(
            source["reviewed_feature_refinement_execution_groups"]
        ),
        "approved_protocol_refinement_execution_groups": _approved_groups(
            source["reviewed_protocol_refinement_execution_groups"]
        ),
        "approved_model_comparison_execution_groups": _approved_groups(
            source["reviewed_model_comparison_execution_groups"]
        ),
        "future_execution_outputs": _future_outputs(
            source["reviewed_planned_execution_outputs"]
        ),
        "per_ticker_feature_label_refinement_execution_approvals": (
            _per_ticker_approvals(source)
        ),
        "feature_label_refinement_execution_approved_by_operator": True,
        "feature_label_refinement_execution_approval_scope": (
            FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY
        ),
        "refinement_execution_authorized_by_this_artifact": True,
        "label_generation_authorized_by_this_artifact": True,
        "feature_generation_authorized_by_this_artifact": True,
        "walk_forward_validation_authorized_by_this_artifact": True,
        "out_of_sample_evaluation_authorized_by_this_artifact": True,
        "metrics_recomputation_authorized_by_this_artifact": True,
        "model_comparison_authorized_by_this_artifact": True,
        "predictive_usefulness_acceptance_created_by_this_artifact": False,
        "profitability_acceptance_created_by_this_artifact": False,
        "runtime_authorized_by_this_artifact": False,
        "approval_creates_predictive_usefulness_acceptance": False,
        "approval_creates_profitability_acceptance": False,
        "approval_creates_runtime_authority": False,
        "limitations": list(LIMITATIONS),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "operator_attestation": deepcopy(dict(attestation)),
        "feature_label_refinement_execution_artifact_created": False,
        "additional_predictive_evidence_execution_candidate_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = artifact.get("operator_attestation", {})
    entries = artifact.get(
        "per_ticker_feature_label_refinement_execution_approvals", []
    )
    outputs = artifact.get("future_execution_outputs", [])
    confirmations = _expected_digest_confirmations()
    values = {
        "execution_candidate_review_digest_matches_expected": (EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("feature_label_refinement_execution_candidate_review_package_digest")),
        "execution_candidate_review_has_zero_blockers": (0, artifact.get("source_execution_candidate_review_blocker_count")),
        "execution_candidate_digest_bound": (EXPECTED_EXECUTION_CANDIDATE_DIGEST, artifact.get("feature_label_refinement_execution_candidate_digest")),
        "plan_approval_digest_bound": (EXPECTED_PLAN_APPROVAL_DIGEST, artifact.get("feature_label_refinement_plan_approval_digest")),
        "plan_candidate_review_digest_bound": (EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("feature_label_refinement_plan_candidate_review_package_digest")),
        "plan_candidate_digest_bound": (EXPECTED_PLAN_CANDIDATE_DIGEST, artifact.get("feature_label_refinement_plan_candidate_digest")),
        "readiness_review_digest_bound": (EXPECTED_READINESS_REVIEW_DIGEST, artifact.get("predictive_usefulness_acceptance_readiness_review_digest")),
        "results_review_digest_bound": (EXPECTED_RESULTS_REVIEW_DIGEST, artifact.get("additional_predictive_evidence_results_review_package_digest")),
        "execution_digest_bound": (EXPECTED_EXECUTION_DIGEST, artifact.get("additional_predictive_evidence_execution_digest")),
        "research_registry_approval_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, artifact.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, artifact.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_execution_candidate_review_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(attestation.get(field) == expected for field, expected in confirmations.items())),
        "operator_confirms_readiness_decision_not_ready": (True, attestation.get("operator_confirms_readiness_decision_not_ready")),
        "operator_confirms_readiness_reason": ("MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", attestation.get("operator_confirms_readiness_reason")),
        "approval_scope_feature_label_refinement_execution_only": (FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY, artifact.get("approval_scope")),
        "feature_label_refinement_execution_approved_true": (True, artifact.get("feature_label_refinement_execution_approved")),
        "feature_label_refinement_execution_authorized_true": (True, artifact.get("feature_label_refinement_execution_authorized")),
        "ready_for_feature_label_refinement_execution_true": (True, artifact.get("ready_for_feature_label_refinement_execution")),
        "refined_label_generation_authorized_true": (True, artifact.get("refined_label_generation_authorized")),
        "refined_feature_generation_authorized_true": (True, artifact.get("refined_feature_generation_authorized")),
        "refined_walk_forward_validation_authorized_true": (True, artifact.get("refined_walk_forward_validation_authorized")),
        "refined_out_of_sample_evaluation_authorized_true": (True, artifact.get("refined_out_of_sample_evaluation_authorized")),
        "refined_metrics_recomputation_authorized_true": (True, artifact.get("refined_metrics_recomputation_authorized")),
        "model_comparison_authorized_true": (True, artifact.get("model_comparison_authorized")),
        "approved_execution_steps_13": (13, len(artifact.get("approved_execution_steps", []))),
        "approved_label_refinement_groups_7": (7, len(artifact.get("approved_label_refinement_execution_groups", []))),
        "approved_feature_refinement_groups_9": (9, len(artifact.get("approved_feature_refinement_execution_groups", []))),
        "approved_protocol_refinement_groups_6": (6, len(artifact.get("approved_protocol_refinement_execution_groups", []))),
        "approved_model_comparison_groups_5": (5, len(artifact.get("approved_model_comparison_execution_groups", []))),
        "future_outputs_12_authorized_not_generated": (True, len(outputs) == 12 and all(row.get("generation_status") == AUTHORIZED_NOT_GENERATED and row.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "per_ticker_execution_approval_entries_12": (12, len(entries)),
        "per_ticker_execution_approval_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_feature_label_refinement_execution_approval_digest"), str) and len(row["per_ticker_feature_label_refinement_execution_approval_digest"]) == 64 and row["per_ticker_feature_label_refinement_execution_approval_digest"] == per_ticker_feature_label_refinement_execution_approval_digest_v1(row) for row in entries)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "raw_provider_payloads_not_committed": (False, artifact.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, artifact.get("api_keys_stored_or_printed")),
        "limitations_recorded": (LIMITATIONS, artifact.get("limitations")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
    }
    false_checks = {
        "feature_label_refinement_executed_false": "feature_label_refinement_executed",
        "feature_label_refinement_results_created_false": "feature_label_refinement_results_created",
        "refined_label_generation_performed_false": "refined_label_generation_performed",
        "refined_feature_generation_performed_false": "refined_feature_generation_performed",
        "refined_walk_forward_validation_performed_false": "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_performed_false": "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_performed_false": "refined_metrics_recomputation_performed",
        "model_comparison_performed_false": "model_comparison_performed",
        "additional_predictive_evidence_execution_candidate_created_false": "additional_predictive_evidence_execution_candidate_created",
        "provider_requests_made_in_approval_false": "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval_false": "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval_false": "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval_false": "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval_false": "canonical_dataset_regenerated_in_approval",
        "predictive_execution_rerun_performed_false": "predictive_execution_rerun_performed",
        "label_generation_rerun_performed_false": "label_generation_rerun_performed",
        "feature_matrix_rerun_performed_false": "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed_false": "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed_false": "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed_false": "metrics_recomputation_performed",
        "improvement_execution_performed_false": "improvement_execution_performed",
        "refinement_option_execution_performed_false": "refinement_option_execution_performed",
        "label_refinement_execution_performed_false": "label_refinement_execution_performed",
        "feature_refinement_execution_performed_false": "feature_refinement_execution_performed",
        "protocol_refinement_execution_performed_false": "protocol_refinement_execution_performed",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready_false": "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended_false": "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready_false": "profitability_acceptance_ready",
        "profitability_acceptance_recommended_false": "profitability_acceptance_recommended",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "approval_creates_predictive_usefulness_acceptance_false": "approval_creates_predictive_usefulness_acceptance",
        "approval_creates_profitability_acceptance_false": "approval_creates_profitability_acceptance",
        "approval_creates_runtime_authority_false": "approval_creates_runtime_authority",
        "no_feature_label_refinement_execution_artifact_created": "feature_label_refinement_execution_artifact_created",
        "no_additional_predictive_evidence_execution_candidate_created": "additional_predictive_evidence_execution_candidate_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update(
        {check_id: (False, artifact.get(field)) for check_id, field in false_checks.items()}
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "feature_label_refinement_execution_approved_by_operator": not failed,
        "approval_scope": FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY,
        "feature_label_refinement_execution_authorized": not failed,
        "ready_for_feature_label_refinement_execution": not failed,
        "feature_label_refinement_executed": False,
        "feature_label_refinement_results_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def feature_label_refinement_execution_approval_digest_v1(
    artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    payload = deepcopy(artifact)
    payload.pop("feature_label_refinement_execution_approval_digest", None)
    return semantic_digest(payload)


def build_feature_label_refinement_execution_approved_v1(
    *,
    feature_label_refinement_execution_candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Build approval from the reviewed candidate without executing refinement."""
    source = _source_review(
        feature_label_refinement_execution_candidate_review_package
    )
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["approval_checklist"] = _checklist(artifact)
    artifact["approval_summary"] = _summary(artifact["approval_checklist"])
    artifact["feature_label_refinement_execution_approval_digest"] = (
        feature_label_refinement_execution_approval_digest_v1(artifact)
    )
    validate_feature_label_refinement_execution_approved_v1(artifact)
    return artifact


def _reject_forbidden_values(value: Any, *, path: str = "approved_artifact") -> None:
    forbidden_artifacts = {
        "FEATURE_LABEL_REFINEMENT_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "LABEL_GENERATION_EXECUTED",
        "FEATURE_MATRIX_GENERATION_EXECUTED",
        "WALK_FORWARD_VALIDATION_EXECUTED",
        "OUT_OF_SAMPLE_EVALUATION_EXECUTED",
        "MODEL_COMPARISON_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeatureLabelRefinementExecutionApprovalError(
                    f"{current} must not emit {item}"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise FeatureLabelRefinementExecutionApprovalError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeatureLabelRefinementExecutionApprovalError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get(
        "per_ticker_feature_label_refinement_execution_approvals"
    )
    if not isinstance(entries, list) or len(entries) != 12:
        raise FeatureLabelRefinementExecutionApprovalError(
            "per-ticker execution approvals mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker tickers")
    expected = _per_ticker_approvals(_source_review(None))
    _expect(entries, expected, "per-ticker execution approvals")
    for row in entries:
        digest = row.get(
            "per_ticker_feature_label_refinement_execution_approval_digest"
        )
        if not isinstance(digest, str) or len(digest) != 64:
            raise FeatureLabelRefinementExecutionApprovalError(
                "per-ticker execution approval digest missing"
            )
        _expect(
            digest,
            per_ticker_feature_label_refinement_execution_approval_digest_v1(row),
            "per-ticker execution approval digest",
        )


def validate_feature_label_refinement_execution_approved_v1(
    approved_artifact: dict,
) -> dict[str, Any]:
    """Validate approval while requiring every execution result to remain absent."""
    if not isinstance(approved_artifact, dict):
        raise FeatureLabelRefinementExecutionApprovalError(
            "feature/label refinement execution approval must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    _validate_attestation(approved_artifact.get("operator_attestation", {}))
    expected_source = _source_review(None)
    expected_base = _base_artifact(
        expected_source, approved_artifact["operator_attestation"]
    )
    for field, expected in expected_base.items():
        _expect(approved_artifact.get(field), expected, field)
    _validate_per_ticker(approved_artifact)
    checklist = approved_artifact.get("approval_checklist")
    if not isinstance(checklist, list):
        raise FeatureLabelRefinementExecutionApprovalError(
            "approval_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "approval_checklist check IDs",
    )
    expected_checklist = _checklist(approved_artifact)
    _expect(checklist, expected_checklist, "approval_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise FeatureLabelRefinementExecutionApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(approved_artifact.get("approval_summary"), expected_summary, "approval_summary")
    digest = approved_artifact.get("feature_label_refinement_execution_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementExecutionApprovalError(
            "feature label refinement execution approval digest missing"
        )
    _expect(
        digest,
        feature_label_refinement_execution_approval_digest_v1(approved_artifact),
        "feature_label_refinement_execution_approval_digest",
    )
    return {
        "status": FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_VALID,
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "feature_label_refinement_execution_approval_digest": digest,
        "source_execution_candidate_review_digest": approved_artifact[
            "feature_label_refinement_execution_candidate_review_package_digest"
        ],
        "per_ticker_approval_count": len(
            approved_artifact[
                "per_ticker_feature_label_refinement_execution_approvals"
            ]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "ready_for_feature_label_refinement_execution": True,
        "feature_label_refinement_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_execution_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized operator-facing approval summary."""
    validation = validate_feature_label_refinement_execution_approved_v1(
        approved_artifact
    )
    operator = approved_artifact["operator_attestation"]
    failure = approved_artifact["readiness_failure_basis"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Feature/Label Refinement Execution Approval Status",
        "",
        "## Title",
        "- Feature/Label Refinement Execution Approval Ceremony v1.",
        "",
        "## Approved Feature/Label Refinement Execution",
        f"- Artifact/status/scope: `{approved_artifact['artifact_kind']}` / `{approved_artifact['approval_status']}` / `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['feature_label_refinement_execution_approval_digest']}`",
        "",
        "## Operator Attestation",
        f"- Reference/timestamp/version: `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}` / `{operator['operator_attestation_version']}`",
        "- Exact non-secret phrase and every required digest, authorization, and boundary confirmation passed.",
        "",
        "## Source Execution Candidate Review",
        f"- Review digest: `{approved_artifact['feature_label_refinement_execution_candidate_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['feature_label_refinement_execution_candidate_digest']}`",
        "",
        "## Execution Objective",
        f"- Objective/scope/mode/authority: `{approved_artifact['feature_label_refinement_execution_objective']}` / `{approved_artifact['feature_label_refinement_execution_scope']}` / `{approved_artifact['feature_label_refinement_execution_mode']}` / `{approved_artifact['feature_label_refinement_execution_authority_status']}`",
        "",
        "## Readiness Failure Basis",
        f"- Decision/reason: `{failure['readiness_decision']}` / `{failure['readiness_reason']}`",
        f"- Stability/baseline: `{failure['stability_consistency_required']}` / `{failure['baseline_outperformance_consistency_required']}`",
    ]
    for heading, key, id_field in (
        ("Approved Execution Steps", "approved_execution_steps", "step_id"),
        ("Approved Label Refinement Execution Groups", "approved_label_refinement_execution_groups", "group_id"),
        ("Approved Feature Refinement Execution Groups", "approved_feature_refinement_execution_groups", "group_id"),
        ("Approved Protocol Refinement Execution Groups", "approved_protocol_refinement_execution_groups", "group_id"),
        ("Approved Model Comparison Execution Groups", "approved_model_comparison_execution_groups", "group_id"),
        ("Future Execution Outputs", "future_execution_outputs", "output_name"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{row[id_field]}`" for row in approved_artifact[key])
    lines.extend(
        [
            "",
            "## Per-Ticker Execution Approval Entries",
            f"- Entry count: `{len(approved_artifact['per_ticker_feature_label_refinement_execution_approvals'])}`; META preserves 913 records and all other tickers preserve 1003.",
            "",
            "## Execution Boundary",
            "- Approval authorizes future refinement execution only. No refinement, label, feature, validation, OOS, metrics, model-comparison, or results work is performed by this artifact.",
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness/readiness: `{approved_artifact['predictive_usefulness']}` / `{approved_artifact['predictive_usefulness_acceptance_ready']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{approved_artifact['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{approved_artifact['runtime_use']}` / `{approved_artifact['strategy_use']}` / `{approved_artifact['paper_trading']}` / `{approved_artifact['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Passed checks: `{summary['passed_checks']}/{summary['total_checks']}`.",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(approved_artifact["next_chain"], start=1)
    )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Approval was built offline from the exact reviewed candidate and explicit attestation. No provider request, acquisition, regeneration, rerun, refinement execution, comparison, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- All approved steps, groups, and outputs remain research-only, non-actionable, and not performed or generated.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_label_refinement_execution_approved_v1(
    output_dir: str | Path,
    *,
    feature_label_refinement_execution_candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical approval JSON once without overwriting."""
    approved_artifact = build_feature_label_refinement_execution_approved_v1(
        feature_label_refinement_execution_candidate_review_package=(
            feature_label_refinement_execution_candidate_review_package
        ),
        operator_attestation=operator_attestation,
    )
    validation = validate_feature_label_refinement_execution_approved_v1(
        approved_artifact
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "feature_label_refinement_execution_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureLabelRefinementExecutionApprovalError(
            "feature label refinement execution approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise FeatureLabelRefinementExecutionApprovalError(
            "feature label refinement execution approval output already exists"
        )
    payload = canonical_json_bytes(approved_artifact)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
