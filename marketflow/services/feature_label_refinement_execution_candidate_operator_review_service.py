"""Offline operator review of the feature/label refinement execution candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_label_refinement_execution_candidate_service as candidate_service


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_V1 = (
    "feature_label_refinement_execution_candidate_review_v1"
)
FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY"
)
EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING"
)
EXECUTION_CANDIDATE_OBJECT_BINDING = (
    "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    "9977616fd85dbb07ff3f1192b067c77157f26935668f07135cd44eb93b5f5bc5"
)
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_TOTAL = 81
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_PASSED = 81
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_EXECUTION_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "execution_candidate_digest_bound",
    "plan_approval_digest_bound",
    "plan_candidate_review_digest_bound",
    "plan_candidate_digest_bound",
    "improvement_candidate_review_digest_bound",
    "readiness_review_digest_bound",
    "reassessment_review_digest_bound",
    "results_review_digest_bound",
    "execution_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_candidate_universe",
    "plan_approved_true",
    "ready_for_feature_label_refinement_execution_candidate_true",
    "feature_label_refinement_execution_candidate_created_true",
    "feature_label_refinement_execution_candidate_review_created_true",
    "execution_candidate_scope_candidate_only",
    "execution_authority_status_not_authorized",
    "readiness_decision_not_ready",
    "readiness_reason_mixed_stability_and_insufficient_baseline_outperformance",
    "label_refinement_execution_groups_7_reviewed",
    "feature_refinement_execution_groups_9_reviewed",
    "protocol_refinement_execution_groups_6_reviewed",
    "model_comparison_execution_groups_5_reviewed",
    "planned_execution_steps_13_reviewed",
    "planned_outputs_12_reviewed",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_execution_candidate_entries_12",
    "per_ticker_execution_candidate_digests_present",
    "per_ticker_execution_candidate_review_digests_present",
    "future_execution_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
    "canonical_dataset_regenerated_in_review_false",
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
    "model_comparison_performed_false",
    "feature_label_refinement_execution_approved_false",
    "feature_label_refinement_execution_authorized_false",
    "feature_label_refinement_executed_false",
    "feature_label_refinement_results_created_false",
    "refined_label_generation_authorized_false",
    "refined_label_generation_performed_false",
    "refined_feature_generation_authorized_false",
    "refined_feature_generation_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
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
    "no_feature_label_refinement_execution_approval_created",
    "no_feature_label_refinement_execution_artifact_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

FORBIDDEN_ARTIFACT_VALUES = set(candidate_service.FORBIDDEN_ARTIFACT_VALUES)


class FeatureLabelRefinementExecutionCandidateReviewPackageError(ValueError):
    """Raised when the review package violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            f"{field} mismatch"
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


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        bound = candidate_service.build_feature_label_refinement_execution_candidate_v1()
        binding_mode = EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING
    else:
        candidate_service.validate_feature_label_refinement_execution_candidate_v1(candidate)
        bound = deepcopy(candidate)
        binding_mode = EXECUTION_CANDIDATE_OBJECT_BINDING
    _expect(
        bound.get("feature_label_refinement_execution_candidate_digest"),
        EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "execution candidate digest",
    )
    return bound, binding_mode


def per_ticker_feature_label_refinement_execution_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_feature_label_refinement_execution_candidate_review_digest",
        None,
    )
    return semantic_digest(payload)


def _per_ticker_review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in candidate["per_ticker_execution_candidate_entries"]:
        entry = deepcopy(source)
        entry["feature_label_refinement_execution_candidate_review_status"] = (
            READY_FOR_OPERATOR_ASSESSMENT
        )
        entry["source_feature_label_refinement_execution_candidate_digest"] = (
            candidate["feature_label_refinement_execution_candidate_digest"]
        )
        entry[
            "per_ticker_feature_label_refinement_execution_candidate_review_digest"
        ] = per_ticker_feature_label_refinement_execution_candidate_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review_package(
    candidate: dict[str, Any], binding_mode: str
) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    package = {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_V1,
        "review_status": FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "execution_candidate_binding_mode": binding_mode,
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
        "label_refinement_execution_performed": False,
        "feature_refinement_execution_performed": False,
        "protocol_refinement_execution_performed": False,
        "model_comparison_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_label_refinement_plan_candidate_created": True,
        "feature_label_refinement_plan_candidate_review_created": True,
        "feature_label_refinement_plan_approved": True,
        "feature_label_refinement_plan_approval_created": True,
        "ready_for_feature_label_refinement_execution_candidate": True,
        "feature_label_refinement_execution_candidate_created": True,
        "feature_label_refinement_execution_candidate_review_created": True,
        "feature_label_refinement_execution_candidate_ready_for_operator_review": True,
        "feature_label_refinement_execution_approved": False,
        "feature_label_refinement_execution_authorized": False,
        "feature_label_refinement_executed": False,
        "feature_label_refinement_results_created": False,
        "refined_label_generation_authorized": False,
        "refined_label_generation_performed": False,
        "refined_feature_generation_authorized": False,
        "refined_feature_generation_performed": False,
        "refined_walk_forward_validation_authorized": False,
        "refined_walk_forward_validation_performed": False,
        "refined_out_of_sample_evaluation_authorized": False,
        "refined_out_of_sample_evaluation_performed": False,
        "refined_metrics_recomputation_authorized": False,
        "refined_metrics_recomputation_performed": False,
        "model_comparison_authorized": False,
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
        "reviewed_feature_label_refinement_execution_candidate_kind": candidate[
            "artifact_kind"
        ],
        "reviewed_feature_label_refinement_execution_candidate_status": candidate[
            "candidate_status"
        ],
        "reviewed_feature_label_refinement_execution_candidate_digest": candidate[
            "feature_label_refinement_execution_candidate_digest"
        ],
        "reviewed_feature_label_refinement_execution_candidate_checklist_total": summary[
            "total_checks"
        ],
        "reviewed_feature_label_refinement_execution_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_feature_label_refinement_execution_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_feature_label_refinement_execution_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "feature_label_refinement_execution_candidate_digest": candidate[
            "feature_label_refinement_execution_candidate_digest"
        ],
        "feature_label_refinement_plan_approval_digest": candidate[
            "feature_label_refinement_plan_approval_digest"
        ],
        "feature_label_refinement_plan_candidate_review_package_digest": candidate[
            "feature_label_refinement_plan_candidate_review_package_digest"
        ],
        "feature_label_refinement_plan_candidate_digest": candidate[
            "feature_label_refinement_plan_candidate_digest"
        ],
        "predictive_evidence_improvement_candidate_review_package_digest": candidate[
            "predictive_evidence_improvement_candidate_review_package_digest"
        ],
        "predictive_evidence_improvement_candidate_digest": candidate[
            "predictive_evidence_improvement_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_review_digest": candidate[
            "predictive_usefulness_acceptance_readiness_review_digest"
        ],
        "predictive_usefulness_reassessment_review_package_digest": candidate[
            "predictive_usefulness_reassessment_review_package_digest"
        ],
        "additional_predictive_evidence_results_review_package_digest": candidate[
            "additional_predictive_evidence_results_review_package_digest"
        ],
        "additional_predictive_evidence_execution_digest": candidate[
            "additional_predictive_evidence_execution_digest"
        ],
        "research_registry_approval_digest": candidate[
            "research_registry_approval_digest"
        ],
        "canonical_dataset_freeze_digest": candidate[
            "canonical_dataset_freeze_digest"
        ],
        "records_digest": candidate["records_digest"],
        "target_universe": list(candidate["target_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "per_ticker_record_counts": deepcopy(candidate["per_ticker_record_counts"]),
        "feature_label_refinement_execution_candidate_objective": candidate[
            "feature_label_refinement_execution_candidate_objective"
        ],
        "feature_label_refinement_execution_candidate_scope": candidate[
            "feature_label_refinement_execution_candidate_scope"
        ],
        "feature_label_refinement_execution_mode": candidate[
            "feature_label_refinement_execution_mode"
        ],
        "feature_label_refinement_execution_authority_status": candidate[
            "feature_label_refinement_execution_authority_status"
        ],
        "reviewed_readiness_failure_basis": deepcopy(
            candidate["readiness_failure_basis"]
        ),
        "reviewed_execution_candidate_profile": deepcopy(
            candidate["execution_candidate_profile"]
        ),
        "reviewed_planned_execution_steps": deepcopy(
            candidate["planned_execution_steps"]
        ),
        "reviewed_label_refinement_execution_groups": deepcopy(
            candidate["planned_label_refinement_execution_groups"]
        ),
        "reviewed_feature_refinement_execution_groups": deepcopy(
            candidate["planned_feature_refinement_execution_groups"]
        ),
        "reviewed_protocol_refinement_execution_groups": deepcopy(
            candidate["planned_protocol_refinement_execution_groups"]
        ),
        "reviewed_model_comparison_execution_groups": deepcopy(
            candidate["planned_model_comparison_execution_groups"]
        ),
        "reviewed_planned_execution_outputs": deepcopy(
            candidate["planned_execution_outputs"]
        ),
        "per_ticker_execution_candidate_review_entries": (
            _per_ticker_review_entries(candidate)
        ),
        "reviewed_future_execution_chain": list(candidate["future_execution_chain"]),
        "reviewed_future_gates": list(candidate["future_gates"]),
        "reviewed_risk_controls": list(candidate["risk_controls"]),
        "feature_label_refinement_execution_approval_created": False,
        "feature_label_refinement_execution_artifact_created": False,
        "additional_predictive_evidence_execution_candidate_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }
    return package


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    basis = review_package.get("reviewed_readiness_failure_basis", {})
    outputs = review_package.get("reviewed_planned_execution_outputs", [])
    entries = review_package.get("per_ticker_execution_candidate_review_entries", [])
    fields = {
        "candidate_kind_matches": (candidate_service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE, review_package.get("reviewed_feature_label_refinement_execution_candidate_kind")),
        "candidate_status_ready_for_review": (candidate_service.FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_feature_label_refinement_execution_candidate_status")),
        "candidate_digest_matches_expected": (EXPECTED_EXECUTION_CANDIDATE_DIGEST, review_package.get("reviewed_feature_label_refinement_execution_candidate_digest")),
        "candidate_checklist_zero_blockers": (0, review_package.get("reviewed_feature_label_refinement_execution_candidate_blocker_count")),
        "execution_candidate_digest_bound": (EXPECTED_EXECUTION_CANDIDATE_DIGEST, review_package.get("feature_label_refinement_execution_candidate_digest")),
        "plan_approval_digest_bound": (candidate_service.EXPECTED_PLAN_APPROVAL_DIGEST, review_package.get("feature_label_refinement_plan_approval_digest")),
        "plan_candidate_review_digest_bound": (candidate_service.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("feature_label_refinement_plan_candidate_review_package_digest")),
        "plan_candidate_digest_bound": (candidate_service.EXPECTED_PLAN_CANDIDATE_DIGEST, review_package.get("feature_label_refinement_plan_candidate_digest")),
        "improvement_candidate_review_digest_bound": (candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_evidence_improvement_candidate_review_package_digest")),
        "readiness_review_digest_bound": (candidate_service.EXPECTED_READINESS_REVIEW_DIGEST, review_package.get("predictive_usefulness_acceptance_readiness_review_digest")),
        "reassessment_review_digest_bound": (candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST, review_package.get("predictive_usefulness_reassessment_review_package_digest")),
        "results_review_digest_bound": (candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST, review_package.get("additional_predictive_evidence_results_review_package_digest")),
        "execution_digest_bound": (candidate_service.EXPECTED_EXECUTION_DIGEST, review_package.get("additional_predictive_evidence_execution_digest")),
        "research_registry_approval_digest_bound": (candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, review_package.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, review_package.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (candidate_service.EXPECTED_RECORDS_DIGEST, review_package.get("records_digest")),
        "target_universe_count_12": (12, review_package.get("target_universe_count")),
        "target_universe_matches_execution_candidate_universe": (TARGET_UNIVERSE, review_package.get("target_universe")),
        "plan_approved_true": (True, review_package.get("feature_label_refinement_plan_approved")),
        "ready_for_feature_label_refinement_execution_candidate_true": (True, review_package.get("ready_for_feature_label_refinement_execution_candidate")),
        "feature_label_refinement_execution_candidate_created_true": (True, review_package.get("feature_label_refinement_execution_candidate_created")),
        "feature_label_refinement_execution_candidate_review_created_true": (True, review_package.get("feature_label_refinement_execution_candidate_review_created")),
        "execution_candidate_scope_candidate_only": (candidate_service.EXECUTION_CANDIDATE_SCOPE, review_package.get("feature_label_refinement_execution_candidate_scope")),
        "execution_authority_status_not_authorized": (NOT_AUTHORIZED, review_package.get("feature_label_refinement_execution_authority_status")),
        "readiness_decision_not_ready": ("PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY", basis.get("readiness_decision")),
        "readiness_reason_mixed_stability_and_insufficient_baseline_outperformance": ("MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", basis.get("readiness_reason")),
        "label_refinement_execution_groups_7_reviewed": (7, len(review_package.get("reviewed_label_refinement_execution_groups", []))),
        "feature_refinement_execution_groups_9_reviewed": (9, len(review_package.get("reviewed_feature_refinement_execution_groups", []))),
        "protocol_refinement_execution_groups_6_reviewed": (6, len(review_package.get("reviewed_protocol_refinement_execution_groups", []))),
        "model_comparison_execution_groups_5_reviewed": (5, len(review_package.get("reviewed_model_comparison_execution_groups", []))),
        "planned_execution_steps_13_reviewed": (13, len(review_package.get("reviewed_planned_execution_steps", []))),
        "planned_outputs_12_reviewed": (12, len(outputs)),
        "planned_outputs_not_generated": (True, bool(outputs) and all(item.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for item in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(item.get("actionability_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)),
        "per_ticker_execution_candidate_entries_12": (12, len(entries)),
        "per_ticker_execution_candidate_digests_present": (True, bool(entries) and all(isinstance(item.get("per_ticker_feature_label_refinement_execution_candidate_digest"), str) and len(item["per_ticker_feature_label_refinement_execution_candidate_digest"]) == 64 for item in entries)),
        "per_ticker_execution_candidate_review_digests_present": (True, bool(entries) and all(isinstance(item.get("per_ticker_feature_label_refinement_execution_candidate_review_digest"), str) and len(item["per_ticker_feature_label_refinement_execution_candidate_review_digest"]) == 64 for item in entries)),
        "future_execution_chain_reviewed": (candidate_service.FUTURE_EXECUTION_CHAIN, review_package.get("reviewed_future_execution_chain")),
        "future_gates_defined": (candidate_service.FUTURE_GATES, review_package.get("reviewed_future_gates")),
        "risk_controls_defined": (candidate_service.RISK_CONTROLS, review_package.get("reviewed_risk_controls")),
    }
    false_checks = {
        "provider_requests_made_in_review_false": "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review_false": "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review_false": "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review_false": "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review_false": "canonical_dataset_regenerated_in_review",
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
        "model_comparison_performed_false": "model_comparison_performed",
        "feature_label_refinement_execution_approved_false": "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized_false": "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed_false": "feature_label_refinement_executed",
        "feature_label_refinement_results_created_false": "feature_label_refinement_results_created",
        "refined_label_generation_authorized_false": "refined_label_generation_authorized",
        "refined_label_generation_performed_false": "refined_label_generation_performed",
        "refined_feature_generation_authorized_false": "refined_feature_generation_authorized",
        "refined_feature_generation_performed_false": "refined_feature_generation_performed",
        "additional_predictive_evidence_execution_candidate_created_false": "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready_false": "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended_false": "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created_false": "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready_false": "profitability_acceptance_ready",
        "profitability_acceptance_recommended_false": "profitability_acceptance_recommended",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_feature_label_refinement_execution_approval_created": "feature_label_refinement_execution_approval_created",
        "no_feature_label_refinement_execution_artifact_created": "feature_label_refinement_execution_artifact_created",
        "no_additional_predictive_evidence_execution_candidate_created": "additional_predictive_evidence_execution_candidate_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    fields.update({check_id: (False, review_package.get(field)) for check_id, field in false_checks.items()})
    fields.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review_package.get("predictive_usefulness")),
            "profitability_not_accepted": (NOT_ACCEPTED, review_package.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, review_package.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, review_package.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, review_package.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, review_package.get("broker_execution")),
        }
    )
    return [_check(check_id, *fields[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(
            item.get("status") == FAIL and item.get("severity") == BLOCKER
            for item in checklist
        ),
        "ready_for_operator_assessment": failed == 0,
        "ready_for_feature_label_refinement_execution_approval": False,
        "ready_for_feature_label_refinement_execution": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def feature_label_refinement_execution_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    payload = deepcopy(review_package)
    payload.pop(
        "feature_label_refinement_execution_candidate_review_package_digest", None
    )
    return semantic_digest(payload)


def build_feature_label_refinement_execution_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build the review package from the exact offline execution candidate."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "feature_label_refinement_execution_candidate_review_package_digest"
    ] = feature_label_refinement_execution_candidate_review_package_digest_v1(
        review_package
    )
    validate_feature_label_refinement_execution_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expected_candidate() -> dict[str, Any]:
    candidate = candidate_service.build_feature_label_refinement_execution_candidate_v1()
    _expect(
        candidate["feature_label_refinement_execution_candidate_digest"],
        EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "expected execution candidate digest",
    )
    return candidate


def _validate_per_ticker_entries(review_package: dict[str, Any]) -> None:
    entries = review_package.get("per_ticker_execution_candidate_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "per-ticker execution candidate review entries missing"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    _expect(entries, _per_ticker_review_entries(_expected_candidate()), "per-ticker entries")
    for entry in entries:
        candidate_digest = entry.get(
            "per_ticker_feature_label_refinement_execution_candidate_digest"
        )
        review_digest = entry.get(
            "per_ticker_feature_label_refinement_execution_candidate_review_digest"
        )
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
                "per-ticker execution candidate digest missing"
            )
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
                "per-ticker execution candidate review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_feature_label_refinement_execution_candidate_review_digest_v1(
                entry
            ),
            "per-ticker execution candidate review digest",
        )


def validate_feature_label_refinement_execution_candidate_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless the package is the exact review-only artifact."""
    if not isinstance(review_package, dict):
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "feature/label refinement execution candidate review must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    binding_mode = review_package.get("execution_candidate_binding_mode")
    if binding_mode not in {
        EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING,
        EXECUTION_CANDIDATE_OBJECT_BINDING,
    }:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "execution_candidate_binding_mode mismatch"
        )
    expected_base = _base_review_package(_expected_candidate(), binding_mode)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    _validate_per_ticker_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "feature_label_refinement_execution_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "feature label refinement execution candidate review digest missing"
        )
    _expect(
        digest,
        feature_label_refinement_execution_candidate_review_package_digest_v1(
            review_package
        ),
        "feature label refinement execution candidate review package digest",
    )
    return {
        "status": "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_label_refinement_execution_candidate_review_package_digest": digest,
        "reviewed_feature_label_refinement_execution_candidate_digest": (
            EXPECTED_EXECUTION_CANDIDATE_DIGEST
        ),
        "ready_for_operator_assessment": expected_summary[
            "ready_for_operator_assessment"
        ],
        "blocker_count": expected_summary["blocker_count"],
        "feature_label_refinement_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_execution_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the review package."""
    validation = validate_feature_label_refinement_execution_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    basis = review_package["reviewed_readiness_failure_basis"]
    profile = review_package["reviewed_execution_candidate_profile"]
    lines = [
        "# MarketFlow Feature/Label Refinement Execution Candidate Review Package Status",
        "",
        "## Title",
        "- Feature/Label Refinement Execution Candidate Review Package v1.",
        "",
        "## Feature/Label Refinement Execution Candidate Review Package",
        f"- Artifact: `{review_package['artifact_kind']}`",
        f"- Status: `{review_package['review_status']}`",
        f"- Review digest: `{validation['feature_label_refinement_execution_candidate_review_package_digest']}`",
        "",
        "## Reviewed Execution Candidate",
        f"- Kind: `{review_package['reviewed_feature_label_refinement_execution_candidate_kind']}`",
        f"- Status: `{review_package['reviewed_feature_label_refinement_execution_candidate_status']}`",
        f"- Digest: `{review_package['reviewed_feature_label_refinement_execution_candidate_digest']}`",
        f"- Candidate checks/blockers: `{review_package['reviewed_feature_label_refinement_execution_candidate_checklist_passed']} / {review_package['reviewed_feature_label_refinement_execution_candidate_blocker_count']}`",
        "",
        "## Source Plan Approval",
        f"- Plan approval digest: `{review_package['feature_label_refinement_plan_approval_digest']}`",
        f"- Plan candidate review digest: `{review_package['feature_label_refinement_plan_candidate_review_package_digest']}`",
        f"- Plan candidate digest: `{review_package['feature_label_refinement_plan_candidate_digest']}`",
        "",
        "## Execution Candidate Objective",
        f"- Objective: `{review_package['feature_label_refinement_execution_candidate_objective']}`",
        f"- Scope: `{review_package['feature_label_refinement_execution_candidate_scope']}`",
        f"- Authority: `{review_package['feature_label_refinement_execution_authority_status']}`",
        "",
        "## Readiness Failure Basis",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in basis.items())
    lines.extend(["", "## Execution Candidate Profile"])
    lines.extend(f"- {key}: `{value}`" for key, value in profile.items())
    for heading, key, id_field in (
        ("Reviewed Planned Execution Steps", "reviewed_planned_execution_steps", "step_id"),
        ("Reviewed Label Refinement Execution Groups", "reviewed_label_refinement_execution_groups", "group_id"),
        ("Reviewed Feature Refinement Execution Groups", "reviewed_feature_refinement_execution_groups", "group_id"),
        ("Reviewed Protocol Refinement Execution Groups", "reviewed_protocol_refinement_execution_groups", "group_id"),
        ("Reviewed Model Comparison Execution Groups", "reviewed_model_comparison_execution_groups", "group_id"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_field]}`" for item in review_package[key])
    lines.extend(["", "## Per-Ticker Execution Candidate Review Entries"])
    lines.extend(
        f"- `{item['ticker']}`: `{item['historical_record_count']}` records; "
        f"`{item['feature_label_refinement_execution_candidate_review_status']}`"
        for item in review_package["per_ticker_execution_candidate_review_entries"]
    )
    for heading, values in (
        ("Future Execution Chain", review_package["reviewed_future_execution_chain"]),
        ("Future Gates", review_package["reviewed_future_gates"]),
        ("Risk Controls", review_package["reviewed_risk_controls"]),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {value}" for value in values)
    lines.extend(
        [
            "",
            "## Execution Boundary",
            "- Review only; refinement execution remains not approved, not authorized, and not performed.",
            "",
            "## Predictive Usefulness Boundary",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            "",
            "## Profitability Boundary",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Guardrails",
            "- No provider request, acquisition, dataset regeneration, predictive rerun, label/feature generation, metrics recomputation, refinement execution, or model comparison occurs.",
            "- No additional evidence candidate, predictive/profitability acceptance, runtime activation, strategy scoring, or trade recommendation is created.",
            "- META remains exactly 913 records; all other tickers remain exactly 1003 records.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_label_refinement_execution_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON once; an existing output fails closed."""
    review_package = (
        build_feature_label_refinement_execution_candidate_review_package_v1(
            candidate
        )
    )
    validation = (
        validate_feature_label_refinement_execution_candidate_review_package_v1(
            review_package
        )
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or (
        "feature_label_refinement_execution_candidate_review_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise FeatureLabelRefinementExecutionCandidateReviewPackageError(
            "feature label refinement execution candidate review output already exists"
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
