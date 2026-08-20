"""Offline operator review of the redesigned-evidence improvement candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import method_evidence_improvement_candidate_redesigned_evidence_service as candidate_service


ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE = (
    "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1 = (
    "method_evidence_improvement_candidate_using_redesigned_evidence_review_v1"
)
METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY"
)

EXPECTED_CANDIDATE_DIGEST = "78685469c41b5103ec4d497b1902f0d172e852949378cd5802f7a84a767dfad7"
EXPECTED_READINESS_REVIEW_DIGEST = candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
EXPECTED_REASSESSMENT_DIGEST = candidate_service.EXPECTED_REASSESSMENT_DIGEST
EXPECTED_RESULTS_REVIEW_DIGEST = candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST
EXPECTED_EXECUTION_DIGEST = candidate_service.EXPECTED_EXECUTION_DIGEST
EXPECTED_MATRIX_DIGEST = candidate_service.EXPECTED_MATRIX_DIGEST
EXPECTED_FEATURE_VALUES_DIGEST = candidate_service.EXPECTED_FEATURE_VALUES_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = candidate_service.EXPECTED_LABEL_VALUES_DIGEST
EXPECTED_RESEARCH_REGISTRY_DIGEST = candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST
EXPECTED_RECORDS_DIGEST = candidate_service.EXPECTED_RECORDS_DIGEST

EXPECTED_TARGET_UNIVERSE = list(candidate_service.EXPECTED_TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
SOURCE_CANDIDATE_ARTIFACT_KIND = (
    candidate_service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE
)
SOURCE_CANDIDATE_STATUS = (
    candidate_service.METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW
)
SOURCE_READINESS_DECISION = candidate_service.SOURCE_READINESS_DECISION
SOURCE_READINESS_DECISION_REASON = candidate_service.SOURCE_READINESS_DECISION_REASON
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = candidate_service.PLANNED_NOT_EXECUTED
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE

IMPROVEMENT_THEME_IDS = list(candidate_service.IMPROVEMENT_THEME_IDS)
IMPROVEMENT_OPTION_IDS = list(candidate_service.IMPROVEMENT_OPTION_IDS)
DIAGNOSTIC_QUESTIONS = list(candidate_service.DIAGNOSTIC_QUESTIONS)
PLANNED_OUTPUT_NAMES = list(candidate_service.PLANNED_OUTPUT_NAMES)
RECOMMENDED_NEXT_OPTION = candidate_service.RECOMMENDED_NEXT_OPTION
RECOMMENDED_NEXT_OPTION_RATIONALE = candidate_service.RECOMMENDED_NEXT_OPTION_RATIONALE
PROBLEM_BASIS = deepcopy(candidate_service.PROBLEM_BASIS)
NEXT_CHAIN = list(candidate_service.NEXT_CHAIN)
NEXT_GATES = list(candidate_service.NEXT_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches", "candidate_status_ready_for_review", "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers", "method_evidence_improvement_candidate_digest_bound",
    "readiness_review_digest_bound", "reassessment_digest_bound", "results_review_digest_bound",
    "execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "target_universe_matches_candidate_universe",
    "records_digest_preserved", "meta_913_preserved", "source_readiness_decision_not_ready",
    "additional_improvement_ready_true", "candidate_created_true", "candidate_review_created_true",
    "candidate_ready_for_operator_review_true", "method_evidence_improvement_approved_false",
    "method_evidence_improvement_authorized_false", "method_evidence_improvement_executed_false",
    "method_evidence_improvement_path_selected_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_recommended_false",
    "acceptance_candidate_created_false", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "problem_basis_reviewed", "improvement_objective_reviewed", "improvement_themes_reviewed",
    "improvement_options_reviewed", "recommended_option_reviewed", "diagnostic_questions_reviewed",
    "planned_outputs_not_generated", "planned_outputs_research_only", "per_ticker_entries_12",
    "per_ticker_candidate_digests_present", "per_ticker_review_digests_present",
    "provider_requests_made_false", "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_review_false",
    "model_training_in_review_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_reviewed", "next_gates_reviewed", "risk_controls_reviewed",
    "no_tracked_marketflow_files",
]


class MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(ValueError):
    """Raised when the review package violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            f"{field} must be false"
        )


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_method_evidence_improvement_candidate_using_redesigned_evidence_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(source)
    _expect(
        source.get("method_evidence_improvement_candidate_using_redesigned_evidence_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    _expect(source["candidate_summary"].get("blocker_count"), 0, "source candidate blockers")
    return source


def _per_ticker_review_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_method_evidence_improvement_candidate_review_digest", None)
    return payload


def per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_improvement_candidate_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry["meta_reduced_record_count_flag"],
            "acceptance_readiness_status": source_entry["acceptance_readiness_status"],
            "method_evidence_improvement_candidate_status": source_entry[
                "method_evidence_improvement_candidate_status"
            ],
            "method_evidence_improvement_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "improvement_note": source_entry["improvement_note"],
            "predictive_usefulness": source_entry["predictive_usefulness"],
            "predictive_usefulness_acceptance_ready": source_entry[
                "predictive_usefulness_acceptance_ready"
            ],
            "predictive_usefulness_acceptance_candidate_created": source_entry[
                "predictive_usefulness_acceptance_candidate_created"
            ],
            "profitability": source_entry["profitability"],
            "runtime_use": source_entry["runtime_use"],
            "strategy_use": source_entry["strategy_use"],
            "paper_trading": source_entry["paper_trading"],
            "broker_execution": source_entry["broker_execution"],
            "source_method_evidence_improvement_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_method_evidence_improvement_candidate_digest": source_entry[
                "per_ticker_method_evidence_improvement_candidate_digest"
            ],
        }
        entry["per_ticker_method_evidence_improvement_candidate_review_digest"] = (
            per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_review_digest_v1(
                entry
            )
        )
        entries.append(entry)
    return entries


def _base_review_package(source: Mapping[str, Any]) -> dict[str, Any]:
    summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_candidate_artifact_kind": source["artifact_kind"],
        "source_candidate_status": source["candidate_status"],
        "source_candidate_digest": source[
            "method_evidence_improvement_candidate_using_redesigned_evidence_digest"
        ],
        "source_candidate_checklist_total": summary["total_checks"],
        "source_candidate_checklist_passed": summary["passed_checks"],
        "source_candidate_checklist_failed": summary["failed_checks"],
        "source_candidate_blocker_count": summary["blocker_count"],
        "source_candidate_target_universe": deepcopy(source["target_universe"]),
        "method_evidence_improvement_candidate_using_redesigned_evidence_digest": source[
            "method_evidence_improvement_candidate_using_redesigned_evidence_digest"
        ],
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": source[
            "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"
        ],
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": source[
            "predictive_usefulness_reassessment_using_redesigned_evidence_digest"
        ],
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": source[
            "additional_predictive_evidence_results_review_using_redesigned_labels_digest"
        ],
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": source[
            "additional_predictive_evidence_execution_using_redesigned_labels_digest"
        ],
        "feature_label_matrix_digest": source["feature_label_matrix_digest"],
        "feature_values_digest": source["feature_values_digest"],
        "redesigned_label_values_digest": source["redesigned_label_values_digest"],
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "records_digest": source["records_digest"],
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_created": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_created": True,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_authorized": False,
        "method_evidence_improvement_executed": False,
        "method_evidence_improvement_path_selected": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
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
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source["meta_reduced_record_count_preserved"],
        "source_readiness_decision": source["source_readiness_decision"],
        "source_readiness_decision_reason": source["source_readiness_decision_reason"],
        "reviewed_problem_basis": deepcopy(source["problem_basis"]),
        "reviewed_method_evidence_improvement_objective": source[
            "method_evidence_improvement_objective"
        ],
        "reviewed_method_evidence_improvement_scope": source[
            "method_evidence_improvement_scope"
        ],
        "reviewed_method_evidence_improvement_mode": source[
            "method_evidence_improvement_mode"
        ],
        "reviewed_method_evidence_improvement_authority_status": source[
            "method_evidence_improvement_authority_status"
        ],
        "reviewed_improvement_themes": deepcopy(source["improvement_themes"]),
        "reviewed_improvement_options": deepcopy(source["improvement_options"]),
        "recommended_next_option": source["recommended_next_option"],
        "recommended_next_option_rationale": source["recommended_next_option_rationale"],
        "reviewed_diagnostic_questions": deepcopy(source["planned_diagnostic_questions"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "next_chain": deepcopy(source["next_chain"]),
        "next_gates": deepcopy(source["next_gates"]),
        "risk_controls": deepcopy(source["risk_controls"]),
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
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(review_package: Mapping[str, Any]) -> list[dict[str, Any]]:
    themes = review_package.get("reviewed_improvement_themes", [])
    options = review_package.get("reviewed_improvement_options", [])
    questions = review_package.get("reviewed_diagnostic_questions", [])
    outputs = review_package.get("reviewed_planned_outputs", [])
    entries = review_package.get("per_ticker_review_entries", [])
    actuals = {
        "candidate_kind_matches": review_package.get("source_candidate_artifact_kind"),
        "candidate_status_ready_for_review": review_package.get("source_candidate_status"),
        "candidate_digest_matches_expected": review_package.get("source_candidate_digest"),
        "candidate_checklist_zero_blockers": review_package.get("source_candidate_blocker_count"),
        "method_evidence_improvement_candidate_digest_bound": review_package.get("method_evidence_improvement_candidate_using_redesigned_evidence_digest"),
        "readiness_review_digest_bound": review_package.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": review_package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": review_package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": review_package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": review_package.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": review_package.get("feature_values_digest"),
        "label_values_digest_bound": review_package.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": review_package.get("research_registry_approval_digest"),
        "records_digest_bound": review_package.get("records_digest"),
        "target_universe_12_preserved": review_package.get("target_universe_count"),
        "target_universe_matches_candidate_universe": review_package.get("target_universe") == review_package.get("source_candidate_target_universe"),
        "records_digest_preserved": review_package.get("records_digest"),
        "meta_913_preserved": review_package.get("meta_record_count"),
        "source_readiness_decision_not_ready": review_package.get("source_readiness_decision"),
        "additional_improvement_ready_true": review_package.get("ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"),
        "candidate_created_true": review_package.get("method_evidence_improvement_candidate_using_redesigned_evidence_created"),
        "candidate_review_created_true": review_package.get("method_evidence_improvement_candidate_using_redesigned_evidence_review_created"),
        "candidate_ready_for_operator_review_true": review_package.get("method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review"),
        "method_evidence_improvement_approved_false": review_package.get("method_evidence_improvement_approved"),
        "method_evidence_improvement_authorized_false": review_package.get("method_evidence_improvement_authorized"),
        "method_evidence_improvement_executed_false": review_package.get("method_evidence_improvement_executed"),
        "method_evidence_improvement_path_selected_false": review_package.get("method_evidence_improvement_path_selected"),
        "improved_evidence_planning_candidate_created_false": review_package.get("improved_evidence_planning_candidate_created"),
        "predictive_usefulness_not_accepted": review_package.get("predictive_usefulness"),
        "acceptance_ready_false": review_package.get("predictive_usefulness_acceptance_ready"),
        "acceptance_recommended_false": review_package.get("predictive_usefulness_acceptance_recommended"),
        "acceptance_candidate_created_false": review_package.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": review_package.get("profitability"),
        "runtime_not_authorized": review_package.get("runtime_use"),
        "strategy_not_authorized": review_package.get("strategy_use"),
        "broker_not_authorized": review_package.get("broker_execution"),
        "trade_recommendations_false": review_package.get("trade_recommendations_generated"),
        "problem_basis_reviewed": review_package.get("reviewed_problem_basis"),
        "improvement_objective_reviewed": review_package.get("reviewed_method_evidence_improvement_objective"),
        "improvement_themes_reviewed": [row.get("theme_id") for row in themes],
        "improvement_options_reviewed": [row.get("option_id") for row in options],
        "recommended_option_reviewed": review_package.get("recommended_next_option"),
        "diagnostic_questions_reviewed": [row.get("question") for row in questions],
        "planned_outputs_not_generated": len(outputs) == len(PLANNED_OUTPUT_NAMES) and all(row.get("output_status") == PLANNED_NOT_GENERATED for row in outputs),
        "planned_outputs_research_only": len(outputs) == len(PLANNED_OUTPUT_NAMES) and all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs),
        "per_ticker_entries_12": len(entries),
        "per_ticker_candidate_digests_present": all(isinstance(row.get("per_ticker_method_evidence_improvement_candidate_digest"), str) and len(row["per_ticker_method_evidence_improvement_candidate_digest"]) == 64 for row in entries),
        "per_ticker_review_digests_present": all(isinstance(row.get("per_ticker_method_evidence_improvement_candidate_review_digest"), str) and len(row["per_ticker_method_evidence_improvement_candidate_review_digest"]) == 64 for row in entries),
        "provider_requests_made_false": review_package.get("provider_requests_made_in_review"),
        "market_data_acquisition_false": review_package.get("market_data_acquisition_performed_in_review"),
        "dataset_regeneration_false": review_package.get("dataset_generation_performed_in_review"),
        "redesigned_label_regeneration_false": review_package.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": review_package.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": review_package.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_review_false": review_package.get("metric_recomputation_performed_in_review"),
        "model_training_in_review_false": review_package.get("model_training_performed_in_review"),
        "no_predictive_usefulness_acceptance_artifact_created": review_package.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": review_package.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": review_package.get("runtime_migration_approval_created"),
        "next_chain_reviewed": review_package.get("next_chain"),
        "next_gates_reviewed": review_package.get("next_gates"),
        "risk_controls_reviewed": review_package.get("risk_controls"),
        "no_tracked_marketflow_files": review_package.get("no_tracked_marketflow_files"),
    }
    expected = {
        "candidate_kind_matches": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "candidate_status_ready_for_review": SOURCE_CANDIDATE_STATUS,
        "candidate_digest_matches_expected": EXPECTED_CANDIDATE_DIGEST,
        "candidate_checklist_zero_blockers": 0,
        "method_evidence_improvement_candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST,
        "readiness_review_digest_bound": EXPECTED_READINESS_REVIEW_DIGEST,
        "reassessment_digest_bound": EXPECTED_REASSESSMENT_DIGEST,
        "results_review_digest_bound": EXPECTED_RESULTS_REVIEW_DIGEST,
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12,
        "target_universe_matches_candidate_universe": True,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913,
        "source_readiness_decision_not_ready": SOURCE_READINESS_DECISION,
        "additional_improvement_ready_true": True,
        "candidate_created_true": True,
        "candidate_review_created_true": True,
        "candidate_ready_for_operator_review_true": True,
        "method_evidence_improvement_approved_false": False,
        "method_evidence_improvement_authorized_false": False,
        "method_evidence_improvement_executed_false": False,
        "method_evidence_improvement_path_selected_false": False,
        "improved_evidence_planning_candidate_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED,
        "acceptance_ready_false": False,
        "acceptance_recommended_false": False,
        "acceptance_candidate_created_false": False,
        "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED,
        "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED,
        "trade_recommendations_false": False,
        "problem_basis_reviewed": PROBLEM_BASIS,
        "improvement_objective_reviewed": candidate_service.METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE,
        "improvement_themes_reviewed": IMPROVEMENT_THEME_IDS,
        "improvement_options_reviewed": IMPROVEMENT_OPTION_IDS,
        "recommended_option_reviewed": RECOMMENDED_NEXT_OPTION,
        "diagnostic_questions_reviewed": DIAGNOSTIC_QUESTIONS,
        "planned_outputs_not_generated": True,
        "planned_outputs_research_only": True,
        "per_ticker_entries_12": 12,
        "per_ticker_candidate_digests_present": True,
        "per_ticker_review_digests_present": True,
        "provider_requests_made_false": False,
        "market_data_acquisition_false": False,
        "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_review_false": False,
        "model_training_in_review_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False,
        "next_chain_reviewed": NEXT_CHAIN,
        "next_gates_reviewed": NEXT_GATES,
        "risk_controls_reviewed": RISK_CONTROLS,
        "no_tracked_marketflow_files": True,
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
        "ready_for_operator_assessment": not failed,
        "ready_for_method_evidence_improvement_path_selection": False,
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_executed": False,
        "improved_evidence_planning_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _review_digest_payload(review_package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review_package))
    payload.pop(
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest",
        None,
    )
    return payload


def method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review package."""
    return semantic_digest(_review_digest_payload(review_package))


def build_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build the offline review package without selecting or executing a path."""
    source = _source_candidate(candidate)
    review_package = _base_review_package(source)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package[
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"
    ] = method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest_v1(
        review_package
    )
    validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    return review_package


def _validate_reviewed_structures(review_package: Mapping[str, Any]) -> None:
    themes = review_package.get("reviewed_improvement_themes")
    if not isinstance(themes, list) or [row.get("theme_id") for row in themes] != IMPROVEMENT_THEME_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "reviewed improvement themes mismatch"
        )
    for row in themes:
        _expect(row.get("theme_status"), PLANNED_NOT_EXECUTED, "theme status")
        _expect_true(row.get("approval_required_before_execution"), "theme approval required")
        _expect_false(row.get("execution_authorized"), "theme execution authorized")
        _expect_false(row.get("execution_performed"), "theme execution performed")
        _expect_true(row.get("research_only"), "theme research only")
        _expect_true(row.get("non_actionable"), "theme non actionable")

    options = review_package.get("reviewed_improvement_options")
    if not isinstance(options, list) or [row.get("option_id") for row in options] != IMPROVEMENT_OPTION_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "reviewed improvement options mismatch"
        )
    for row in options:
        _expect(row.get("option_status"), "AVAILABLE_FOR_OPERATOR_REVIEW", "option status")
        for field in ("selected", "approved", "executed", "creates_acceptance_candidate"):
            _expect_false(row.get(field), f"option {field}")
        _expect_true(row.get("research_only"), "option research only")
        _expect_true(row.get("non_actionable"), "option non actionable")

    questions = review_package.get("reviewed_diagnostic_questions")
    if not isinstance(questions, list) or [row.get("question") for row in questions] != DIAGNOSTIC_QUESTIONS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "reviewed diagnostic questions mismatch"
        )
    for row in questions:
        _expect(row.get("status"), "NOT_ANSWERED", "diagnostic status")
        _expect_true(row.get("requires_separate_review_or_execution"), "diagnostic separate review")
        _expect_true(row.get("research_only"), "diagnostic research only")
        _expect_true(row.get("non_actionable"), "diagnostic non actionable")

    outputs = review_package.get("reviewed_planned_outputs")
    if not isinstance(outputs, list) or [row.get("output_name") for row in outputs] != PLANNED_OUTPUT_NAMES:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "reviewed planned outputs mismatch"
        )
    for row in outputs:
        _expect(row.get("output_status"), PLANNED_NOT_GENERATED, "planned output status")
        _expect(row.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "planned output label")


def validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate candidate bindings and every closed review boundary."""
    if not isinstance(review_package, dict):
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "review_package must be an object"
        )
    expected = {
        "artifact_kind": ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "source_candidate_artifact_kind": SOURCE_CANDIDATE_ARTIFACT_KIND,
        "source_candidate_status": SOURCE_CANDIDATE_STATUS,
        "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "source_candidate_checklist_total": 54,
        "source_candidate_checklist_passed": 54,
        "source_candidate_checklist_failed": 0,
        "source_candidate_blocker_count": 0,
        "source_candidate_target_universe": EXPECTED_TARGET_UNIVERSE,
        "method_evidence_improvement_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "source_readiness_decision": SOURCE_READINESS_DECISION,
        "source_readiness_decision_reason": SOURCE_READINESS_DECISION_REASON,
        "reviewed_problem_basis": PROBLEM_BASIS,
        "reviewed_method_evidence_improvement_objective": candidate_service.METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE,
        "reviewed_method_evidence_improvement_scope": candidate_service.METHOD_EVIDENCE_IMPROVEMENT_SCOPE,
        "reviewed_method_evidence_improvement_mode": candidate_service.METHOD_EVIDENCE_IMPROVEMENT_MODE,
        "reviewed_method_evidence_improvement_authority_status": candidate_service.METHOD_EVIDENCE_IMPROVEMENT_AUTHORITY_STATUS,
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "recommended_next_option_rationale": RECOMMENDED_NEXT_OPTION_RATIONALE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    true_fields = (
        "created_offline", "research_only", "operator_review_required",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_readiness_review_completed",
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence",
        "method_evidence_improvement_candidate_using_redesigned_evidence_created",
        "method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review",
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_created",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(review_package.get(field), field)
    false_fields = (
        "method_evidence_improvement_approved", "method_evidence_improvement_authorized",
        "method_evidence_improvement_executed", "method_evidence_improvement_path_selected",
        "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review", "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review", "canonical_dataset_regenerated_in_review",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed", "metric_recomputation_performed_in_review",
        "model_training_performed_in_review", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(review_package.get(field), field)

    _validate_reviewed_structures(review_package)

    entries = review_package.get("per_ticker_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "per-ticker review entries mismatch"
        )
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("acceptance_readiness_status"), "NOT_READY", f"{ticker} readiness")
        _expect(entry.get("method_evidence_improvement_candidate_status"), "PLANNED_READY_FOR_OPERATOR_REVIEW", f"{ticker} candidate status")
        _expect(entry.get("method_evidence_improvement_candidate_review_status"), "READY_FOR_OPERATOR_ASSESSMENT", f"{ticker} review status")
        _expect(entry.get("source_method_evidence_improvement_candidate_digest"), EXPECTED_CANDIDATE_DIGEST, f"{ticker} source candidate digest")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} predictive usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        for field in ("predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created"):
            _expect_false(entry.get(field), f"{ticker} {field}")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        expected_note = (
            "PRESERVE_META_LIMITATION_IN_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE"
            if ticker == "META"
            else "STANDARD_RECORD_COUNT_PRESERVED"
        )
        _expect(entry.get("improvement_note"), expected_note, f"{ticker} improvement note")
        candidate_digest = entry.get("per_ticker_method_evidence_improvement_candidate_digest")
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
                f"{ticker} candidate digest missing"
            )
        review_digest = entry.get("per_ticker_method_evidence_improvement_candidate_review_digest")
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
                f"{ticker} review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_review_digest_v1(entry),
            f"{ticker} review digest",
        )

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "review checklist mismatch"
        )
    _expect(checklist, _checklist(review_package), "review checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "review checklist failed"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")

    digest = review_package.get(
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest_v1(
            review_package
        ),
        "review digest",
    )
    return {
        "status": "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": digest,
        **{
            key: review_package["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_method_evidence_improvement_candidate_using_redesigned_evidence_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a sanitized Markdown view of the validated review package."""
    validation = validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    sections = [
        ("Title", ["Method / Evidence Improvement Candidate Review Using Redesigned Evidence"]),
        ("Method / Evidence Improvement Candidate Review Using Redesigned Evidence", [
            f"Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
            f"Digest: `{validation['method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest']}`.",
        ]),
        ("Reviewed Candidate", [
            f"Artifact/status: `{review_package['source_candidate_artifact_kind']}` / `{review_package['source_candidate_status']}`.",
            f"Digest/checks: `{review_package['source_candidate_digest']}` / `{review_package['source_candidate_checklist_passed']} of {review_package['source_candidate_checklist_total']}`.",
        ]),
        ("Source Readiness Review", [
            f"Decision/reason: `{review_package['source_readiness_decision']}` / `{review_package['source_readiness_decision_reason']}`.",
            f"Digest: `{review_package['predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest']}`.",
        ]),
        ("Bound Evidence", [
            f"Reassessment/results: `{review_package['predictive_usefulness_reassessment_using_redesigned_evidence_digest']}` / `{review_package['additional_predictive_evidence_results_review_using_redesigned_labels_digest']}`.",
            f"Execution/matrix: `{review_package['additional_predictive_evidence_execution_using_redesigned_labels_digest']}` / `{review_package['feature_label_matrix_digest']}`.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: `{review_package['dataset_name']}` / `{review_package['total_canonical_record_count']}`.",
            "Universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + ".",
            "META remains `913`; every other ticker remains `1003`.",
        ]),
        ("Reviewed Problem Basis", [f"`{key}`: `{value}`" for key, value in review_package["reviewed_problem_basis"].items()]),
        ("Reviewed Improvement Objective", [
            f"Objective: `{review_package['reviewed_method_evidence_improvement_objective']}`.",
            f"Scope/mode/authority: `{review_package['reviewed_method_evidence_improvement_scope']}` / `{review_package['reviewed_method_evidence_improvement_mode']}` / `{review_package['reviewed_method_evidence_improvement_authority_status']}`.",
        ]),
        ("Reviewed Improvement Themes", [f"`{row['theme_id']}`: `{row['theme_status']}`." for row in review_package["reviewed_improvement_themes"]]),
        ("Reviewed Improvement Options", [f"`{row['option_id']}`: `{row['option_status']}`; selected `{row['selected']}`." for row in review_package["reviewed_improvement_options"]] + [f"Recommended: `{review_package['recommended_next_option']}` — `{review_package['recommended_next_option_rationale']}`."]),
        ("Reviewed Diagnostic Questions", [f"`{row['question']}`: `{row['status']}`." for row in review_package["reviewed_diagnostic_questions"]]),
        ("Reviewed Planned Outputs", [f"`{row['output_name']}`: `{row['output_status']}` / `{row['output_label']}`." for row in review_package["reviewed_planned_outputs"]]),
        ("Per-Ticker Review Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['method_evidence_improvement_candidate_review_status']}`, digest `{row['per_ticker_method_evidence_improvement_candidate_review_digest']}`." for row in review_package["per_ticker_review_entries"]]),
        ("Next Chain", review_package["next_chain"]),
        ("Next Gates", review_package["next_gates"]),
        ("Risk Controls", review_package["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{review_package['review_summary']['total_checks']} / {review_package['review_summary']['passed_checks']} / {review_package['review_summary']['failed_checks']} / {review_package['review_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, execution rerun, metric recomputation, model training, path selection, approval, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Method / Evidence Improvement Candidate Review Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict:
    """Write canonical review JSON without overwriting an existing artifact."""
    review_package = (
        build_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
            candidate
        )
    )
    validation = validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = (
        directory
        / "method_evidence_improvement_candidate_using_redesigned_evidence_review_v1.json"
    )
    if path.exists():
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError(
            "review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest": validation[
            "method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
