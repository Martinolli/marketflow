"""Offline operator review of the feature/label refinement plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_label_refinement_plan_candidate_service as candidate_service


ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_V1 = (
    "feature_label_refinement_plan_candidate_review_v1"
)
FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)

EXPECTED_CANDIDATE_DIGEST = (
    "96266cb3869885c4c33025422b7730f4c3e1399967ef541dc0b0eb808480daf8"
)
EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST
)
EXPECTED_READINESS_REVIEW_DIGEST = candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_REVIEW_DIGEST = candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = candidate_service.EXPECTED_EXECUTION_DIGEST
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
PLANNED_NOT_EXECUTED = candidate_service.PLANNED_NOT_EXECUTED
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class FeatureLabelRefinementPlanCandidateReviewError(ValueError):
    """Raised when the review package violates its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureLabelRefinementPlanCandidateReviewError(f"{field} mismatch")


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
        candidate_service.build_feature_label_refinement_plan_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    try:
        candidate_service.validate_feature_label_refinement_plan_candidate_v1(source)
    except candidate_service.FeatureLabelRefinementPlanCandidateError as exc:
        raise FeatureLabelRefinementPlanCandidateReviewError(
            "source feature/label refinement plan candidate is invalid"
        ) from exc
    _expect(
        source.get("feature_label_refinement_plan_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source feature/label refinement plan candidate digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_label_refinement_plan_candidate_review_digest", None)
    return payload


def per_ticker_feature_label_refinement_plan_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_refinement_plan_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "readiness_status": source_entry["readiness_status"],
            "feature_label_refinement_plan_status": source_entry[
                "feature_label_refinement_plan_status"
            ],
            "feature_label_refinement_plan_review_status": (
                "READY_FOR_OPERATOR_ASSESSMENT"
            ),
            "refinement_authorized": False,
            "refinement_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_label_refinement_plan_candidate_digest": source[
                "feature_label_refinement_plan_candidate_digest"
            ],
            "per_ticker_feature_label_refinement_plan_candidate_digest": source_entry[
                "per_ticker_feature_label_refinement_plan_candidate_digest"
            ],
        }
        if source_entry["ticker"] == "META":
            entry["refinement_note"] = source_entry["refinement_note"]
        entry["per_ticker_feature_label_refinement_plan_candidate_review_digest"] = (
            per_ticker_feature_label_refinement_plan_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    source_summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_V1,
        "review_status": FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
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
        "feature_label_refinement_plan_ready_for_operator_review": True,
        "feature_label_refinement_plan_approved": False,
        "feature_label_refinement_authorized": False,
        "feature_label_refinement_executed": False,
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
        "reviewed_feature_label_refinement_plan_candidate_kind": source[
            "artifact_kind"
        ],
        "reviewed_feature_label_refinement_plan_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_feature_label_refinement_plan_candidate_digest": source[
            "feature_label_refinement_plan_candidate_digest"
        ],
        "reviewed_feature_label_refinement_plan_candidate_checklist_total": (
            source_summary["total_checks"]
        ),
        "reviewed_feature_label_refinement_plan_candidate_checklist_passed": (
            source_summary["passed_checks"]
        ),
        "reviewed_feature_label_refinement_plan_candidate_checklist_failed": (
            source_summary["failed_checks"]
        ),
        "reviewed_feature_label_refinement_plan_candidate_blocker_count": (
            source_summary["blocker_count"]
        ),
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
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "records_digest": source["records_digest"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "registry_approved_dataset_metadata": deepcopy(
            source["registry_approved_dataset_metadata"]
        ),
        "feature_label_refinement_plan_objective": source[
            "feature_label_refinement_plan_objective"
        ],
        "feature_label_refinement_plan_scope": source[
            "feature_label_refinement_plan_scope"
        ],
        "feature_label_refinement_plan_mode": source[
            "feature_label_refinement_plan_mode"
        ],
        "feature_label_refinement_authority_status": source[
            "feature_label_refinement_authority_status"
        ],
        "reviewed_readiness_failure_basis": deepcopy(
            source["readiness_failure_summary"]
        ),
        "reviewed_evidence_basis": deepcopy(source["evidence_basis"]),
        "reviewed_label_refinement_groups": deepcopy(
            source["planned_label_refinement_groups"]
        ),
        "reviewed_feature_refinement_groups": deepcopy(
            source["planned_feature_refinement_groups"]
        ),
        "reviewed_protocol_refinement_groups": deepcopy(
            source["planned_protocol_refinement_groups"]
        ),
        "reviewed_model_comparison_groups": deepcopy(
            source["planned_model_comparison_groups"]
        ),
        "reviewed_refinement_priority": deepcopy(source["refinement_priority"]),
        "per_ticker_refinement_plan_review_entries": _per_ticker_review_entries(
            source
        ),
        "reviewed_future_refinement_chain": deepcopy(
            source["future_refinement_chain"]
        ),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "planned_output_count": len(source["planned_outputs"]),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "feature_label_refinement_plan_approval_created": False,
        "feature_label_refinement_execution_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE, "reviewed_feature_label_refinement_plan_candidate_kind"),
    ("candidate_status_ready_for_review", candidate_service.FEATURE_LABEL_REFINEMENT_PLAN_READY_FOR_OPERATOR_REVIEW, "reviewed_feature_label_refinement_plan_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "reviewed_feature_label_refinement_plan_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "reviewed_feature_label_refinement_plan_candidate_blocker_count"),
    ("feature_label_refinement_plan_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "feature_label_refinement_plan_candidate_digest"),
    ("improvement_candidate_review_digest_bound", EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST, "predictive_evidence_improvement_candidate_review_package_digest"),
    ("improvement_candidate_digest_bound", EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST, "predictive_evidence_improvement_candidate_digest"),
    ("readiness_review_digest_bound", EXPECTED_READINESS_REVIEW_DIGEST, "predictive_usefulness_acceptance_readiness_review_digest"),
    ("reassessment_review_digest_bound", EXPECTED_REASSESSMENT_REVIEW_DIGEST, "predictive_usefulness_reassessment_review_package_digest"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_candidate_universe", TARGET_UNIVERSE, "target_universe"),
    ("readiness_decision_not_ready", "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY", "readiness_decision"),
    ("readiness_reason_mixed_stability_and_insufficient_baseline_outperformance", "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", "readiness_reason"),
    ("stability_consistency_required_not_met", "FAIL_OR_NOT_MET", "stability_consistency_required"),
    ("baseline_outperformance_consistency_required_not_met", "FAIL_OR_NOT_MET", "baseline_outperformance_consistency_required"),
    ("feature_label_refinement_plan_candidate_created_true", True, "feature_label_refinement_plan_candidate_created"),
    ("feature_label_refinement_plan_candidate_review_created_true", True, "feature_label_refinement_plan_candidate_review_created"),
    ("feature_label_refinement_plan_scope_candidate_only", candidate_service.PLAN_SCOPE, "feature_label_refinement_plan_scope"),
    ("feature_label_refinement_authority_status_not_authorized", NOT_AUTHORIZED, "feature_label_refinement_authority_status"),
    ("label_refinement_groups_reviewed", candidate_service.LABEL_REFINEMENT_GROUP_IDS, "label_refinement_group_ids"),
    ("feature_refinement_groups_reviewed", candidate_service.FEATURE_REFINEMENT_GROUP_IDS, "feature_refinement_group_ids"),
    ("protocol_refinement_groups_reviewed", candidate_service.PROTOCOL_REFINEMENT_GROUP_IDS, "protocol_refinement_group_ids"),
    ("model_comparison_groups_reviewed", candidate_service.MODEL_COMPARISON_GROUP_IDS, "model_comparison_group_ids"),
    ("refinement_priority_reviewed", candidate_service.REFINEMENT_PRIORITY, "reviewed_refinement_priority"),
    ("per_ticker_refinement_plan_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_refinement_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_refinement_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("future_refinement_chain_reviewed", candidate_service.FUTURE_REFINEMENT_CHAIN, "reviewed_future_refinement_chain"),
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
    ("label_refinement_execution_performed_false", False, "label_refinement_execution_performed"),
    ("feature_refinement_execution_performed_false", False, "feature_refinement_execution_performed"),
    ("protocol_refinement_execution_performed_false", False, "protocol_refinement_execution_performed"),
    ("model_comparison_performed_false", False, "model_comparison_performed"),
    ("refined_label_generation_authorized_false", False, "refined_label_generation_authorized"),
    ("refined_label_generation_performed_false", False, "refined_label_generation_performed"),
    ("refined_feature_generation_authorized_false", False, "refined_feature_generation_authorized"),
    ("refined_feature_generation_performed_false", False, "refined_feature_generation_performed"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("additional_predictive_evidence_execution_authorized_false", False, "additional_predictive_evidence_execution_authorized"),
    ("additional_predictive_evidence_executed_false", False, "additional_predictive_evidence_executed"),
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
    ("no_feature_label_refinement_approval_created", False, "feature_label_refinement_plan_approval_created"),
    ("no_feature_label_refinement_execution_created", False, "feature_label_refinement_execution_created"),
    ("no_additional_predictive_evidence_execution_candidate_created", False, "additional_predictive_evidence_execution_candidate_created"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
]
REQUIRED_CHECK_IDS = [item[0] for item in CHECK_FIELD_SPECS]


def _derived_check_fields(review_package: dict[str, Any]) -> dict[str, Any]:
    failure = review_package.get("reviewed_readiness_failure_basis", {})
    label_groups = review_package.get("reviewed_label_refinement_groups", [])
    feature_groups = review_package.get("reviewed_feature_refinement_groups", [])
    protocol_groups = review_package.get("reviewed_protocol_refinement_groups", [])
    model_groups = review_package.get("reviewed_model_comparison_groups", [])
    entries = review_package.get("per_ticker_refinement_plan_review_entries", [])
    return {
        "readiness_decision": failure.get("readiness_decision"),
        "readiness_reason": failure.get("readiness_reason"),
        "stability_consistency_required": failure.get(
            "stability_consistency_required"
        ),
        "baseline_outperformance_consistency_required": failure.get(
            "baseline_outperformance_consistency_required"
        ),
        "label_refinement_group_ids": [
            row.get("group_id") for row in label_groups if isinstance(row, dict)
        ],
        "feature_refinement_group_ids": [
            row.get("group_id") for row in feature_groups if isinstance(row, dict)
        ],
        "protocol_refinement_group_ids": [
            row.get("group_id") for row in protocol_groups if isinstance(row, dict)
        ],
        "model_comparison_group_ids": [
            row.get("group_id") for row in model_groups if isinstance(row, dict)
        ],
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": isinstance(entries, list)
        and all(
            isinstance(row, dict)
            and isinstance(
                row.get(
                    "per_ticker_feature_label_refinement_plan_candidate_digest"
                ),
                str,
            )
            and len(
                row["per_ticker_feature_label_refinement_plan_candidate_digest"]
            )
            == 64
            for row in entries
        ),
        "per_ticker_review_digests_valid": isinstance(entries, list)
        and all(
            isinstance(row, dict)
            and isinstance(
                row.get(
                    "per_ticker_feature_label_refinement_plan_candidate_review_digest"
                ),
                str,
            )
            and row[
                "per_ticker_feature_label_refinement_plan_candidate_review_digest"
            ]
            == per_ticker_feature_label_refinement_plan_candidate_review_digest_v1(row)
            for row in entries
        ),
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review_package)
    values.update(_derived_check_fields(review_package))
    return [
        _check(check_id, expected, values.get(field))
        for check_id, expected, field in CHECK_FIELD_SPECS
    ]


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
        "ready_for_feature_label_refinement_plan_approval": False,
        "ready_for_feature_label_refinement_execution_candidate": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("feature_label_refinement_plan_candidate_review_package_digest", None)
    return payload


def feature_label_refinement_plan_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    return semantic_digest(_digest_payload(review_package))


def build_feature_label_refinement_plan_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build an offline operator review of the exact refinement plan candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["feature_label_refinement_plan_candidate_review_package_digest"] = (
        feature_label_refinement_plan_candidate_review_package_digest_v1(
            review_package
        )
    )
    validate_feature_label_refinement_plan_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "FEATURE_LABEL_REFINEMENT_PLAN_APPROVED",
        "FEATURE_LABEL_REFINEMENT_EXECUTED",
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
        "label_refinement_execution_performed",
        "feature_refinement_execution_performed",
        "protocol_refinement_execution_performed",
        "model_comparison_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "feature_label_refinement_plan_approved",
        "feature_label_refinement_authorized",
        "feature_label_refinement_executed",
        "refined_label_generation_authorized",
        "refined_label_generation_performed",
        "refined_feature_generation_authorized",
        "refined_feature_generation_performed",
        "refined_walk_forward_validation_authorized",
        "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_authorized",
        "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_authorized",
        "refined_metrics_recomputation_performed",
        "model_comparison_authorized",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
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
        "refinement_authorized",
        "refinement_executed",
        "feature_label_refinement_plan_approval_created",
        "feature_label_refinement_execution_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise FeatureLabelRefinementPlanCandidateReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise FeatureLabelRefinementPlanCandidateReviewError(
                    f"{current} must be false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise FeatureLabelRefinementPlanCandidateReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise FeatureLabelRefinementPlanCandidateReviewError(
                    f"{current} must not be accepted"
                )
            if key in {
                "feature_label_refinement_authority_status",
                "authorization_status",
            } and item != NOT_AUTHORIZED:
                raise FeatureLabelRefinementPlanCandidateReviewError(
                    f"{current} must remain {NOT_AUTHORIZED}"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_feature_label_refinement_plan_candidate_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate the exact review package and keep every later gate closed."""
    if not isinstance(review_package, dict):
        raise FeatureLabelRefinementPlanCandidateReviewError(
            "feature/label refinement plan candidate review must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    expected_source = candidate_service.build_feature_label_refinement_plan_candidate_v1()
    expected_base = _base_review(expected_source)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise FeatureLabelRefinementPlanCandidateReviewError(
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
        raise FeatureLabelRefinementPlanCandidateReviewError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "feature_label_refinement_plan_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureLabelRefinementPlanCandidateReviewError(
            "feature label refinement plan candidate review package digest missing"
        )
    _expect(
        digest,
        feature_label_refinement_plan_candidate_review_package_digest_v1(
            review_package
        ),
        "feature_label_refinement_plan_candidate_review_package_digest",
    )
    return {
        "status": "FEATURE_LABEL_REFINEMENT_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "feature_label_refinement_plan_candidate_review_package_digest": digest,
        "reviewed_candidate_digest": review_package[
            "reviewed_feature_label_refinement_plan_candidate_digest"
        ],
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_refinement_plan_review_entries"]
        ),
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_assessment": True,
        "feature_label_refinement_authorized": False,
        "feature_label_refinement_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_feature_label_refinement_plan_candidate_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized operator-facing candidate-review summary."""
    validation = validate_feature_label_refinement_plan_candidate_review_package_v1(
        review_package
    )
    failure = review_package["reviewed_readiness_failure_basis"]
    evidence = review_package["reviewed_evidence_basis"]
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Feature/Label Refinement Plan Candidate Operator Review Status",
        "",
        "## Title",
        "- Feature/Label Refinement Plan Candidate Operator Review Package v1.",
        "",
        "## Feature/Label Refinement Plan Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`",
        f"- Review digest: `{validation['feature_label_refinement_plan_candidate_review_package_digest']}`",
        "",
        "## Reviewed Candidate",
        f"- Candidate artifact/status: `{review_package['reviewed_feature_label_refinement_plan_candidate_kind']}` / `{review_package['reviewed_feature_label_refinement_plan_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_feature_label_refinement_plan_candidate_digest']}`",
        "",
        "## Source Improvement Candidate Review",
        f"- Improvement candidate review digest: `{review_package['predictive_evidence_improvement_candidate_review_package_digest']}`",
        f"- Improvement candidate digest: `{review_package['predictive_evidence_improvement_candidate_digest']}`",
        "",
        "## Readiness Failure Basis",
        f"- Decision/reason: `{failure['readiness_decision']}` / `{failure['readiness_reason']}`",
        f"- Stability/baseline: `{failure['stability_consistency_required']}` / `{failure['baseline_outperformance_consistency_required']}`",
        f"- Walk-forward/OOS majority/Brier: `{evidence['walk_forward_accuracy_range']}` / `{evidence['oos_majority_accuracy']}` / `{evidence['oos_brier_score']}`",
        "",
        "## Reviewed Label Refinements",
    ]
    lines.extend(
        f"- `{row['group_id']}`"
        for row in review_package["reviewed_label_refinement_groups"]
    )
    lines.extend(["", "## Reviewed Feature Refinements"])
    lines.extend(
        f"- `{row['group_id']}`"
        for row in review_package["reviewed_feature_refinement_groups"]
    )
    lines.extend(["", "## Reviewed Protocol Refinements"])
    lines.extend(
        f"- `{row['group_id']}`"
        for row in review_package["reviewed_protocol_refinement_groups"]
    )
    lines.extend(["", "## Reviewed Model Comparison Groups"])
    lines.extend(
        f"- `{row['group_id']}`"
        for row in review_package["reviewed_model_comparison_groups"]
    )
    lines.extend(["", "## Refinement Priority"])
    for tier, values in review_package["reviewed_refinement_priority"].items():
        lines.append(f"- `{tier}`: {', '.join(f'`{value}`' for value in values)}")
    lines.extend(
        [
            "",
            "## Per-Ticker Refinement Plan Review Entries",
            f"- Entry count: `{len(review_package['per_ticker_refinement_plan_review_entries'])}`; META preserves 913 records and all other tickers preserve 1003.",
            "",
            "## Future Refinement Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(
            review_package["reviewed_future_refinement_chain"], start=1
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
            "- Review built offline from the exact candidate. No provider request, acquisition, regeneration, rerun, refinement execution, model comparison, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Reviewed groups and planned outputs remain research-only, non-actionable, and non-authorizing.",
            "",
        ]
    )
    return "\n".join(lines)


def write_feature_label_refinement_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical operator-review JSON once without overwriting."""
    review_package = build_feature_label_refinement_plan_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_feature_label_refinement_plan_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "feature_label_refinement_plan_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureLabelRefinementPlanCandidateReviewError(
            "feature label refinement plan candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise FeatureLabelRefinementPlanCandidateReviewError(
            "feature label refinement plan candidate review output already exists"
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
