"""Offline predictive-usefulness acceptance-readiness review (not acceptance)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_review_service as reassessment_service


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_V1 = (
    "predictive_usefulness_acceptance_readiness_review_v1"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_COMPLETED = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_COMPLETED"
)
PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
)

EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST = (
    "71a1456fdef4ed9845c1a5264bc56eb9e362e43e88f2316d6700efe2d6f2bfab"
)
EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    reassessment_service.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CANDIDATE_DIGEST = reassessment_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST = (
    reassessment_service.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_EXECUTION_DIGEST = reassessment_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    reassessment_service.EXPECTED_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    reassessment_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    reassessment_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
)
EXPECTED_RECORDS_DIGEST = reassessment_service.EXPECTED_RECORDS_DIGEST

TARGET_UNIVERSE = list(reassessment_service.TARGET_UNIVERSE)
NOT_ACCEPTED = reassessment_service.NOT_ACCEPTED
NOT_AUTHORIZED = reassessment_service.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = reassessment_service.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = reassessment_service.PLANNED_NOT_GENERATED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_MET = "FAIL_OR_NOT_MET"

READINESS_CRITERIA = [
    "leakage_controls_pass_required",
    "no_failed_controls_required",
    "minimum_evidence_review_completion_required",
    "stability_consistency_required",
    "baseline_outperformance_consistency_required",
    "operator_acceptance_boundary_required",
    "profitability_separation_required",
    "runtime_separation_required",
]

READINESS_FINDING_RESULTS = {
    "leakage_controls_pass_required": PASS,
    "no_failed_controls_required": PASS,
    "minimum_evidence_review_completion_required": PASS,
    "stability_consistency_required": NOT_MET,
    "baseline_outperformance_consistency_required": NOT_MET,
    "operator_acceptance_boundary_required": PASS,
    "profitability_separation_required": PASS,
    "runtime_separation_required": PASS,
}

FUTURE_IMPROVEMENT_CHAIN = [
    "Predictive evidence improvement candidate, if desired.",
    "Additional feature/label refinement candidate, if desired.",
    "Additional predictive evidence execution candidate, if new evidence is proposed.",
    "Additional predictive evidence execution approval and execution, if separately approved.",
    "Additional predictive evidence results review.",
    "Predictive usefulness reassessment review rerun, if new evidence exists.",
    "Predictive usefulness acceptance readiness review rerun.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "predictive_evidence_improvement_candidate_if_desired",
    "additional_predictive_evidence_execution_candidate_if_new_evidence_proposed",
    "additional_predictive_evidence_results_review_if_executed",
    "predictive_usefulness_reassessment_review_rerun_if_new_evidence_exists",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_acceptance_when_readiness_not_met",
    "no_predictive_usefulness_acceptance_without_positive_readiness_decision",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_predictive_evidence_without_new_approval",
    "mixed_signal_requires_improvement_or_additional_review",
    "all_outputs_labeled_research_only",
]

PLANNED_OUTPUT_NAMES = [
    "predictive_evidence_improvement_candidate_template",
    "additional_feature_label_refinement_plan_template",
    "future_readiness_rerun_template",
    "acceptance_candidate_template_if_ready_later",
    "operator_review_summary_template",
]


class PredictiveUsefulnessAcceptanceReadinessReviewError(ValueError):
    """Raised when the readiness review violates its non-accepting contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(f"{field} mismatch")


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


def _source_reassessment_review(
    reassessment_review_package: dict | None,
) -> dict[str, Any]:
    source = (
        reassessment_service.build_predictive_usefulness_reassessment_review_package_v1()
        if reassessment_review_package is None
        else deepcopy(reassessment_review_package)
    )
    reassessment_service.validate_predictive_usefulness_reassessment_review_package_v1(
        source
    )
    _expect(
        source.get("predictive_usefulness_reassessment_review_package_digest"),
        EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST,
        "source reassessment review package digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_predictive_usefulness_acceptance_readiness_digest", None)
    return payload


def per_ticker_predictive_usefulness_acceptance_readiness_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker readiness entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_reassessment_review_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "predictive_evidence_results_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_review_status": (
                "REASSESSMENT_REVIEW_COMPLETED_RESEARCH_ONLY"
            ),
            "predictive_usefulness_acceptance_readiness_status": "NOT_READY",
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_predictive_usefulness_reassessment_review_package_digest": (
                source["predictive_usefulness_reassessment_review_package_digest"]
            ),
            "source_per_ticker_predictive_usefulness_reassessment_review_digest": (
                source_entry[
                    "per_ticker_predictive_usefulness_reassessment_review_digest"
                ]
            ),
        }
        entry["per_ticker_predictive_usefulness_acceptance_readiness_digest"] = (
            per_ticker_predictive_usefulness_acceptance_readiness_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _readiness_findings() -> list[dict[str, str]]:
    return [
        {"criterion_id": criterion_id, "result": READINESS_FINDING_RESULTS[criterion_id]}
        for criterion_id in READINESS_CRITERIA
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


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_V1,
        "review_status": PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_COMPLETED,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY,
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
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "predictive_usefulness_reassessment_candidate_created": True,
        "predictive_usefulness_reassessment_candidate_review_created": True,
        "predictive_usefulness_reassessment_review_created": True,
        "predictive_usefulness_reassessment_review_ready": True,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ceremony_ready": False,
        "ready_for_predictive_usefulness_improvement_or_additional_evidence_planning": True,
        "predictive_usefulness": NOT_ACCEPTED,
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
        "predictive_usefulness_reassessment_review_package_digest": source[
            "predictive_usefulness_reassessment_review_package_digest"
        ],
        "predictive_usefulness_reassessment_candidate_review_package_digest": source[
            "predictive_usefulness_reassessment_candidate_review_package_digest"
        ],
        "predictive_usefulness_reassessment_candidate_digest": source[
            "predictive_usefulness_reassessment_candidate_digest"
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
        "readiness_review_input_facts": {
            **deepcopy(source["evidence_summary"]),
            **deepcopy(source["performance_interpretation"]),
            "reassessment_review_status": source["reassessment_review_status"],
            "evidence_quality_for_acceptance_readiness": source[
                "evidence_quality_for_acceptance_readiness"
            ],
            "predictive_signal_consistency": source["predictive_signal_consistency"],
            "baseline_outperformance_consistency": source[
                "baseline_outperformance_consistency"
            ],
            "leakage_control_assessment": source["leakage_control_assessment"],
            "data_quality_assessment": source["data_quality_assessment"],
        },
        "readiness_criteria": deepcopy(READINESS_CRITERIA),
        "readiness_findings": _readiness_findings(),
        "readiness_reason": (
            "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
        ),
        "acceptance_candidate_allowed": False,
        "acceptance_ceremony_allowed": False,
        "additional_evidence_or_model_improvement_required": True,
        "per_ticker_readiness_entries": _per_ticker_entries(source),
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
    ("reassessment_review_digest_bound", EXPECTED_REASSESSMENT_REVIEW_PACKAGE_DIGEST, "predictive_usefulness_reassessment_review_package_digest"),
    ("candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST, "predictive_usefulness_reassessment_candidate_review_package_digest"),
    ("candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "predictive_usefulness_reassessment_candidate_digest"),
    ("results_review_digest_bound", EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST, "additional_predictive_evidence_results_review_package_digest"),
    ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, "additional_predictive_evidence_execution_digest"),
    ("execution_approval_digest_bound", EXPECTED_EXECUTION_APPROVAL_DIGEST, "additional_predictive_evidence_execution_approval_digest"),
    ("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, "research_registry_approval_digest"),
    ("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, "canonical_dataset_freeze_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_count_12", 12, "target_universe_count"),
    ("target_universe_matches_reassessment_review_universe", TARGET_UNIVERSE, "target_universe"),
    ("additional_predictive_evidence_executed_true", True, "additional_predictive_evidence_executed"),
    ("additional_predictive_evidence_results_review_ready_true", True, "additional_predictive_evidence_results_review_ready"),
    ("predictive_usefulness_reassessment_review_created_true", True, "predictive_usefulness_reassessment_review_created"),
    ("predictive_usefulness_reassessment_review_ready_true", True, "predictive_usefulness_reassessment_review_ready"),
    ("acceptance_readiness_review_created_true", True, "predictive_usefulness_acceptance_readiness_review_created"),
    ("acceptance_readiness_review_completed_true", True, "predictive_usefulness_acceptance_readiness_review_completed"),
    ("leakage_controls_pass_required_pass", PASS, "finding_leakage_controls_pass_required"),
    ("no_failed_controls_required_pass", PASS, "finding_no_failed_controls_required"),
    ("minimum_evidence_review_completion_required_pass", PASS, "finding_minimum_evidence_review_completion_required"),
    ("stability_consistency_required_not_met", NOT_MET, "finding_stability_consistency_required"),
    ("baseline_outperformance_consistency_required_not_met", NOT_MET, "finding_baseline_outperformance_consistency_required"),
    ("operator_acceptance_boundary_required_pass", PASS, "finding_operator_acceptance_boundary_required"),
    ("profitability_separation_required_pass", PASS, "finding_profitability_separation_required"),
    ("runtime_separation_required_pass", PASS, "finding_runtime_separation_required"),
    ("readiness_decision_not_ready", PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY, "readiness_decision"),
    ("readiness_reason_mixed_stability_and_insufficient_baseline_outperformance", "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE", "readiness_reason"),
    ("acceptance_candidate_allowed_false", False, "acceptance_candidate_allowed"),
    ("acceptance_ceremony_allowed_false", False, "acceptance_ceremony_allowed"),
    ("additional_evidence_or_model_improvement_required_true", True, "additional_evidence_or_model_improvement_required"),
    ("per_ticker_readiness_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_readiness_digests_present", True, "per_ticker_digests_valid"),
    ("future_improvement_chain_defined", FUTURE_IMPROVEMENT_CHAIN, "future_improvement_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
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


def _derived_check_fields(review: dict[str, Any]) -> dict[str, Any]:
    findings = review.get("readiness_findings", [])
    entries = review.get("per_ticker_readiness_entries", [])
    values = {
        f"finding_{item.get('criterion_id')}": item.get("result")
        for item in findings
        if isinstance(item, dict)
    }
    values.update(
        {
            "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
            "per_ticker_digests_valid": isinstance(entries, list)
            and all(
                isinstance(item, dict)
                and isinstance(
                    item.get(
                        "per_ticker_predictive_usefulness_acceptance_readiness_digest"
                    ),
                    str,
                )
                and item[
                    "per_ticker_predictive_usefulness_acceptance_readiness_digest"
                ]
                == per_ticker_predictive_usefulness_acceptance_readiness_digest_v1(item)
                for item in entries
            ),
        }
    )
    return values


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    values = dict(review)
    values.update(_derived_check_fields(review))
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
        "acceptance_readiness_review_completed": True,
        "readiness_decision": PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "ready_for_improvement_or_additional_evidence_planning": blockers == 0,
    }


def _digest_payload(review: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review)
    payload.pop("predictive_usefulness_acceptance_readiness_review_digest", None)
    return payload


def predictive_usefulness_acceptance_readiness_review_digest_v1(
    review: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the readiness review."""
    return semantic_digest(_digest_payload(review))


def build_predictive_usefulness_acceptance_readiness_review_v1(
    *, reassessment_review_package: dict | None = None
) -> dict:
    """Build a not-ready decision from the exact reviewed mixed evidence."""
    source = _source_reassessment_review(reassessment_review_package)
    review = _base_review(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["predictive_usefulness_acceptance_readiness_review_digest"] = (
        predictive_usefulness_acceptance_readiness_review_digest_v1(review)
    )
    validate_predictive_usefulness_acceptance_readiness_review_v1(review)
    return review


def _reject_forbidden_values(value: Any, *, path: str = "review") -> None:
    forbidden_artifacts = {
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
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ceremony_ready",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "acceptance_candidate_allowed",
        "acceptance_ceremony_allowed",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise PredictiveUsefulnessAcceptanceReadinessReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise PredictiveUsefulnessAcceptanceReadinessReviewError(
                    f"{current} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise PredictiveUsefulnessAcceptanceReadinessReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise PredictiveUsefulnessAcceptanceReadinessReviewError(
                    f"{current} must not be accepted"
                )
            if key == "readiness_decision" and item != PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY:
                raise PredictiveUsefulnessAcceptanceReadinessReviewError(
                    f"{current} must remain {PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY}"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_predictive_usefulness_acceptance_readiness_review_v1(
    review: dict,
) -> dict:
    """Validate exact evidence binding and reject any implied acceptance."""
    if not isinstance(review, dict):
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            "acceptance readiness review must be a JSON object"
        )
    _reject_forbidden_values(review)
    expected_source = (
        reassessment_service.build_predictive_usefulness_reassessment_review_package_v1()
    )
    expected_base = _base_review(expected_source)
    for field, expected in expected_base.items():
        _expect(review.get(field), expected, field)
    checklist = review.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            "review_checklist missing"
        )
    _expect(
        [row.get("check_id") for row in checklist if isinstance(row, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [row for row in expected_checklist if row.get("status") != PASS]
    if failed:
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review.get("review_summary"), expected_summary, "review_summary")
    digest = review.get("predictive_usefulness_acceptance_readiness_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            "predictive usefulness acceptance readiness review digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_acceptance_readiness_review_digest_v1(review),
        "predictive_usefulness_acceptance_readiness_review_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "readiness_decision": review["readiness_decision"],
        "predictive_usefulness_acceptance_readiness_review_digest": digest,
        "source_reassessment_review_package_digest": review[
            "predictive_usefulness_reassessment_review_package_digest"
        ],
        "per_ticker_readiness_entry_count": len(review["per_ticker_readiness_entries"]),
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
        "ready_for_improvement_or_additional_evidence_planning": True,
    }


def build_predictive_usefulness_acceptance_readiness_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown summary of the not-ready decision."""
    validation = validate_predictive_usefulness_acceptance_readiness_review_v1(review)
    metadata = review["registry_approved_dataset_metadata"]
    summary = review["review_summary"]
    lines = [
        "# MarketFlow Predictive Usefulness Acceptance Readiness Review Status",
        "",
        "## Title",
        "- Predictive Usefulness Acceptance Readiness Review v1.",
        "",
        "## Predictive Usefulness Acceptance Readiness Review",
        f"- Artifact/status: `{review['artifact_kind']}` / `{review['review_status']}`",
        f"- Digest: `{validation['predictive_usefulness_acceptance_readiness_review_digest']}`",
        "",
        "## Source Reassessment Review",
        f"- Reassessment-review digest: `{review['predictive_usefulness_reassessment_review_package_digest']}`",
        f"- Candidate-review digest: `{review['predictive_usefulness_reassessment_candidate_review_package_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset/scope: `{metadata['dataset_name']}` / `{metadata['dataset_scope']}`",
        f"- Records/digest: `{metadata['total_canonical_record_count']}` / `{metadata['records_digest']}`",
        "",
        "## Target Universe",
        f"- `{', '.join(review['target_universe'])}`",
        "",
        "## Readiness Criteria",
    ]
    lines.extend(f"- `{criterion}`" for criterion in review["readiness_criteria"])
    lines.extend(["", "## Readiness Findings"])
    lines.extend(
        f"- `{finding['criterion_id']}`: `{finding['result']}`"
        for finding in review["readiness_findings"]
    )
    lines.extend(
        [
            "",
            "## Readiness Decision",
            f"- Decision/reason: `{review['readiness_decision']}` / `{review['readiness_reason']}`.",
            f"- Acceptance candidate/ceremony allowed: `{review['acceptance_candidate_allowed']}` / `{review['acceptance_ceremony_allowed']}`.",
            "",
            "## Per-Ticker Readiness Entries",
            f"- Entry count: `{len(review['per_ticker_readiness_entries'])}`; META remains 913 records and every other ticker remains 1003.",
            "",
            "## Future Improvement Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(review["future_improvement_chain"], start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review["risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            f"- Predictive usefulness/readiness: `{review['predictive_usefulness']}` / `{review['predictive_usefulness_acceptance_ready']}`.",
            "",
            "## Profitability Boundary",
            f"- Profitability: `{review['profitability']}`.",
            "",
            "## Runtime Boundary",
            f"- Runtime/strategy/paper/broker: `{review['runtime_use']}` / `{review['strategy_use']}` / `{review['paper_trading']}` / `{review['broker_execution']}`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- The mixed evidence is not ready for acceptance. No provider request, acquisition, regeneration, rerun, recomputation, scoring, recommendation, acceptance, or runtime activation occurred.",
            "- Planned outputs remain not generated and research-only; future evidence work requires its own approval chain.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_acceptance_readiness_review_v1(
    output_dir: str | Path,
    *,
    reassessment_review_package: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write canonical readiness-review JSON once without overwriting."""
    review = build_predictive_usefulness_acceptance_readiness_review_v1(
        reassessment_review_package=reassessment_review_package
    )
    validation = validate_predictive_usefulness_acceptance_readiness_review_v1(review)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_acceptance_readiness_review_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            "predictive usefulness acceptance readiness review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessAcceptanceReadinessReviewError(
            "predictive usefulness acceptance readiness review output already exists"
        )
    payload = canonical_json_bytes(review)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
