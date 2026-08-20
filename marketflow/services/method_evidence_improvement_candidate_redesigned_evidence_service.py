"""Offline method/evidence improvement candidate using redesigned evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    predictive_usefulness_acceptance_readiness_review_redesigned_evidence_service as readiness,
)


ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE = (
    "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1 = (
    "method_evidence_improvement_candidate_using_redesigned_evidence_v1"
)
METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW = (
    "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_READINESS_REVIEW_DIGEST = "6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da"
EXPECTED_REASSESSMENT_DIGEST = "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985"
EXPECTED_RESULTS_REVIEW_DIGEST = "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed"
EXPECTED_EXECUTION_DIGEST = "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"

EXPECTED_TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in EXPECTED_TARGET_UNIVERSE
}

SOURCE_ARTIFACT_KIND = (
    readiness.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE
)
SOURCE_REVIEW_STATUS = (
    readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED
)
SOURCE_READINESS_DECISION = (
    readiness.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE
)
SOURCE_READINESS_DECISION_REASON = readiness.READINESS_DECISION_REASON

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE = (
    "PREPARE_METHOD_AND_EVIDENCE_IMPROVEMENT_OPTIONS_AFTER_NOT_READY_REDESIGNED_EVIDENCE_DECISION"
)
METHOD_EVIDENCE_IMPROVEMENT_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
METHOD_EVIDENCE_IMPROVEMENT_MODE = PLANNED_NOT_EXECUTED
METHOD_EVIDENCE_IMPROVEMENT_AUTHORITY_STATUS = NOT_AUTHORIZED

IMPROVEMENT_THEME_IDS = [
    "IMPROVEMENT_THEME_LABEL_OBJECTIVE_REFINEMENT",
    "IMPROVEMENT_THEME_FEATURE_FAMILY_REVIEW",
    "IMPROVEMENT_THEME_MODEL_FAMILY_EXPANSION",
    "IMPROVEMENT_THEME_BASELINE_OUTPERFORMANCE_CRITERIA",
    "IMPROVEMENT_THEME_STABILITY_PROTOCOL_REVIEW",
    "IMPROVEMENT_THEME_CALIBRATION_REVIEW",
    "IMPROVEMENT_THEME_CROSS_SECTIONAL_SIGNAL_REVIEW",
    "IMPROVEMENT_THEME_PER_TICKER_DIAGNOSTIC_REVIEW",
    "IMPROVEMENT_THEME_META_LIMITATION_HANDLING",
    "IMPROVEMENT_THEME_OPTIONAL_MODEL_COVERAGE",
    "IMPROVEMENT_THEME_ACCEPTANCE_THRESHOLD_POLICY",
]

IMPROVEMENT_OPTION_IDS = [
    "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION",
    "OPTION_B_REVIEW_FEATURE_SIGNAL_DESIGN",
    "OPTION_C_REVIEW_MODEL_FAMILY_COVERAGE",
    "OPTION_D_REVIEW_WALK_FORWARD_AND_STABILITY_PROTOCOL",
    "OPTION_E_REVIEW_CALIBRATION_AND_BRIER_CRITERIA",
    "OPTION_F_REVIEW_ACCEPTANCE_THRESHOLD_POLICY",
    "OPTION_G_COLLECT_ADDITIONAL_RESEARCH_EVIDENCE",
    "OPTION_H_RETAIN_CURRENT_EVIDENCE_AND_STOP_ACCEPTANCE_PATH",
]
RECOMMENDED_NEXT_OPTION = "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION"
RECOMMENDED_NEXT_OPTION_RATIONALE = (
    "LABEL_OBJECTIVE_AND_SIGNAL_DEFINITION_SHOULD_BE_RECHECKED_BEFORE_MORE_EXECUTION_BECAUSE_"
    "OOS_EDGE_IS_SMALL_AND_LOCAL_MODEL_MATCHES_MAJORITY"
)

DIAGNOSTIC_QUESTIONS = [
    "does_current_label_objective_reward_tradeable_signal_or_majority_class_structure",
    "does_cross_sectional_edge_generalize_by_ticker_and_regime",
    "does_feature_set_explain_label_family_variation",
    "are_horizons_and thresholds too broad_or_too_noisy",
    "does_calibration_support_confidence_sensitive_use",
    "does_walk_forward_stability_support_acceptance_thresholds",
    "are_optional_model_families_needed_before_readiness_can_pass",
    "does_meta_limitation_materially_affect_cross_sectional_evidence",
    "should_acceptance_thresholds_be_made_explicit_before_any_future_candidate",
    "should_candidate_path_stop_until_stronger_evidence_is_generated",
]

PLANNED_OUTPUT_NAMES = [
    "method_evidence_improvement_candidate_manifest",
    "label_objective_diagnostic_template",
    "feature_signal_diagnostic_template",
    "model_family_coverage_review_template",
    "walk_forward_stability_review_template",
    "calibration_brier_review_template",
    "acceptance_threshold_policy_template",
    "additional_evidence_planning_template",
    "per_ticker_method_diagnostic_template",
    "operator_review_summary_template",
]

NEXT_CHAIN = [
    "Method / Evidence Improvement Candidate Operator Review Using Redesigned Evidence v1.",
    "Method / Evidence Improvement Path Selection Using Redesigned Evidence v1, if selected.",
    "Optional label-objective, feature, model, calibration, or evidence-planning candidate depending on selected option.",
    "Optional approval and execution of improved research evidence, if separately approved.",
    "Predictive usefulness reassessment rerun, if new evidence is created.",
    "Predictive usefulness acceptance-readiness rerun, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "method_evidence_improvement_candidate_operator_review_using_redesigned_evidence",
    "method_evidence_improvement_path_selection_using_redesigned_evidence_if_selected",
    "label_objective_or_feature_or_model_or_calibration_improvement_candidate_if_selected",
    "improved_evidence_planning_candidate_if_selected",
    "improved_evidence_execution_approval_if_required",
    "improved_evidence_execution_if_approved",
    "predictive_usefulness_reassessment_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_after_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "candidate_does_not_approve_improvement",
    "candidate_does_not_execute_improvement",
    "candidate_does_not_generate_new_evidence",
    "candidate_does_not_rerun_predictive_evidence",
    "candidate_does_not_retrain_models",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_create_acceptance_candidate",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

PROBLEM_BASIS = {
    "readiness_decision": SOURCE_READINESS_DECISION,
    "readiness_decision_reason": SOURCE_READINESS_DECISION_REASON,
    "oos_cross_sectional_delta_vs_majority": "0.00309917",
    "oos_local_model_delta_vs_majority": "0.00000000",
    "predictive_signal_readiness": "NOT_READY",
    "baseline_outperformance_readiness": "NOT_READY",
    "local_model_readiness": "NOT_READY",
    "stability_readiness": "NOT_READY",
    "calibration_readiness": "REQUIRES_OPERATOR_REVIEW",
    "optional_model_coverage_sufficiency": "FAIL_OR_NOT_MET",
    "additional_evidence_or_method_improvement_required": True,
}

REQUIRED_CHECK_IDS = [
    "readiness_review_digest_bound", "reassessment_digest_bound", "results_review_digest_bound",
    "execution_digest_bound", "matrix_digest_bound", "feature_values_digest_bound",
    "label_values_digest_bound", "research_registry_digest_bound", "records_digest_bound",
    "target_universe_12_preserved", "records_digest_preserved", "meta_913_preserved",
    "source_readiness_decision_not_ready", "additional_improvement_ready_true",
    "candidate_created_true", "candidate_ready_for_operator_review_true",
    "method_evidence_improvement_approved_false", "method_evidence_improvement_authorized_false",
    "method_evidence_improvement_executed_false", "improved_evidence_planning_candidate_created_false",
    "predictive_usefulness_not_accepted", "acceptance_ready_false", "acceptance_recommended_false",
    "acceptance_candidate_created_false", "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized", "trade_recommendations_false",
    "problem_basis_preserved", "improvement_objective_defined", "improvement_themes_defined",
    "improvement_options_defined", "recommended_option_defined", "diagnostic_questions_defined",
    "planned_outputs_not_generated", "planned_outputs_research_only", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false", "market_data_acquisition_false",
    "dataset_regeneration_false", "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_candidate_false",
    "model_training_in_candidate_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "next_chain_defined", "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]


class MethodEvidenceImprovementCandidateRedesignedEvidenceError(ValueError):
    """Raised when the candidate violates its offline, non-authorizing contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError(f"{field} must be false")


def _source_readiness_review() -> dict[str, Any]:
    source = readiness.build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1()
    readiness.validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(source)
    _expect(
        source.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        EXPECTED_READINESS_REVIEW_DIGEST,
        "source readiness review digest",
    )
    return source


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_method_evidence_improvement_candidate_digest", None)
    return payload


def per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one per-ticker candidate entry."""
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
            "acceptance_readiness_status": "NOT_READY",
            "method_evidence_improvement_candidate_status": "PLANNED_READY_FOR_OPERATOR_REVIEW",
            "improvement_note": (
                "PRESERVE_META_LIMITATION_IN_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE"
                if is_meta
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_readiness_review_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        }
        entry["per_ticker_method_evidence_improvement_candidate_digest"] = (
            per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _improvement_themes() -> list[dict[str, Any]]:
    return [
        {
            "theme_id": theme_id,
            "theme_status": PLANNED_NOT_EXECUTED,
            "approval_required_before_execution": True,
            "execution_authorized": False,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for theme_id in IMPROVEMENT_THEME_IDS
    ]


def _improvement_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "option_status": "AVAILABLE_FOR_OPERATOR_REVIEW",
            "selected": False,
            "approved": False,
            "executed": False,
            "creates_acceptance_candidate": False,
            "research_only": True,
            "non_actionable": True,
        }
        for option_id in IMPROVEMENT_OPTION_IDS
    ]


def _diagnostic_questions() -> list[dict[str, Any]]:
    return [
        {
            "question": question,
            "status": "NOT_ANSWERED",
            "requires_separate_review_or_execution": True,
            "research_only": True,
            "non_actionable": True,
        }
        for question in DIAGNOSTIC_QUESTIONS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_name": output_name,
            "output_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "candidate_status": METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_readiness_review_artifact_kind": SOURCE_ARTIFACT_KIND,
        "source_readiness_review_status": SOURCE_REVIEW_STATUS,
        "source_readiness_decision": SOURCE_READINESS_DECISION,
        "source_readiness_decision_reason": SOURCE_READINESS_DECISION_REASON,
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_created": True,
        "predictive_usefulness_acceptance_readiness_review_completed": True,
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_created": True,
        "method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_authorized": False,
        "method_evidence_improvement_executed": False,
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
        "provider_requests_made_in_candidate": False,
        "live_provider_transport_enabled_in_candidate": False,
        "market_data_acquisition_performed_in_candidate": False,
        "dataset_generation_performed_in_candidate": False,
        "canonical_dataset_regenerated_in_candidate": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_candidate": False,
        "model_training_performed_in_candidate": False,
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
        "problem_basis": deepcopy(PROBLEM_BASIS),
        "method_evidence_improvement_objective": METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE,
        "method_evidence_improvement_scope": METHOD_EVIDENCE_IMPROVEMENT_SCOPE,
        "method_evidence_improvement_mode": METHOD_EVIDENCE_IMPROVEMENT_MODE,
        "method_evidence_improvement_authority_status": METHOD_EVIDENCE_IMPROVEMENT_AUTHORITY_STATUS,
        "improvement_themes": _improvement_themes(),
        "improvement_options": _improvement_options(),
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "recommended_next_option_rationale": RECOMMENDED_NEXT_OPTION_RATIONALE,
        "planned_diagnostic_questions": _diagnostic_questions(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_improvement_candidate_entries": _per_ticker_entries(),
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
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _checklist(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    themes = candidate.get("improvement_themes", [])
    options = candidate.get("improvement_options", [])
    questions = candidate.get("planned_diagnostic_questions", [])
    outputs = candidate.get("planned_outputs", [])
    entries = candidate.get("per_ticker_improvement_candidate_entries", [])
    actuals = {
        "readiness_review_digest_bound": candidate.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
        "reassessment_digest_bound": candidate.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
        "results_review_digest_bound": candidate.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
        "execution_digest_bound": candidate.get("additional_predictive_evidence_execution_using_redesigned_labels_digest"),
        "matrix_digest_bound": candidate.get("feature_label_matrix_digest"),
        "feature_values_digest_bound": candidate.get("feature_values_digest"),
        "label_values_digest_bound": candidate.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": candidate.get("research_registry_approval_digest"),
        "records_digest_bound": candidate.get("records_digest"),
        "target_universe_12_preserved": candidate.get("target_universe_count"),
        "records_digest_preserved": candidate.get("records_digest"),
        "meta_913_preserved": candidate.get("meta_record_count"),
        "source_readiness_decision_not_ready": candidate.get("source_readiness_decision"),
        "additional_improvement_ready_true": candidate.get("ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"),
        "candidate_created_true": candidate.get("method_evidence_improvement_candidate_using_redesigned_evidence_created"),
        "candidate_ready_for_operator_review_true": candidate.get("method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review"),
        "method_evidence_improvement_approved_false": candidate.get("method_evidence_improvement_approved"),
        "method_evidence_improvement_authorized_false": candidate.get("method_evidence_improvement_authorized"),
        "method_evidence_improvement_executed_false": candidate.get("method_evidence_improvement_executed"),
        "improved_evidence_planning_candidate_created_false": candidate.get("improved_evidence_planning_candidate_created"),
        "predictive_usefulness_not_accepted": candidate.get("predictive_usefulness"),
        "acceptance_ready_false": candidate.get("predictive_usefulness_acceptance_ready"),
        "acceptance_recommended_false": candidate.get("predictive_usefulness_acceptance_recommended"),
        "acceptance_candidate_created_false": candidate.get("predictive_usefulness_acceptance_candidate_created"),
        "profitability_not_accepted": candidate.get("profitability"),
        "runtime_not_authorized": candidate.get("runtime_use"),
        "strategy_not_authorized": candidate.get("strategy_use"),
        "broker_not_authorized": candidate.get("broker_execution"),
        "trade_recommendations_false": candidate.get("trade_recommendations_generated"),
        "problem_basis_preserved": candidate.get("problem_basis"),
        "improvement_objective_defined": candidate.get("method_evidence_improvement_objective"),
        "improvement_themes_defined": [row.get("theme_id") for row in themes],
        "improvement_options_defined": [row.get("option_id") for row in options],
        "recommended_option_defined": candidate.get("recommended_next_option"),
        "diagnostic_questions_defined": [row.get("question") for row in questions],
        "planned_outputs_not_generated": all(row.get("output_status") == PLANNED_NOT_GENERATED for row in outputs) and len(outputs) == len(PLANNED_OUTPUT_NAMES),
        "planned_outputs_research_only": all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs) and len(outputs) == len(PLANNED_OUTPUT_NAMES),
        "per_ticker_entries_12": len(entries),
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_method_evidence_improvement_candidate_digest"), str) and len(row["per_ticker_method_evidence_improvement_candidate_digest"]) == 64 for row in entries),
        "provider_requests_made_false": candidate.get("provider_requests_made_in_candidate"),
        "market_data_acquisition_false": candidate.get("market_data_acquisition_performed_in_candidate"),
        "dataset_regeneration_false": candidate.get("dataset_generation_performed_in_candidate"),
        "redesigned_label_regeneration_false": candidate.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": candidate.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": candidate.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_candidate_false": candidate.get("metric_recomputation_performed_in_candidate"),
        "model_training_in_candidate_false": candidate.get("model_training_performed_in_candidate"),
        "no_predictive_usefulness_acceptance_artifact_created": candidate.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": candidate.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": candidate.get("runtime_migration_approval_created"),
        "next_chain_defined": candidate.get("next_chain"),
        "next_gates_defined": candidate.get("next_gates"),
        "risk_controls_defined": candidate.get("risk_controls"),
        "no_tracked_marketflow_files": candidate.get("no_tracked_marketflow_files"),
    }
    expected = {
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
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": 913,
        "source_readiness_decision_not_ready": SOURCE_READINESS_DECISION,
        "additional_improvement_ready_true": True,
        "candidate_created_true": True,
        "candidate_ready_for_operator_review_true": True,
        "method_evidence_improvement_approved_false": False,
        "method_evidence_improvement_authorized_false": False,
        "method_evidence_improvement_executed_false": False,
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
        "problem_basis_preserved": PROBLEM_BASIS,
        "improvement_objective_defined": METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE,
        "improvement_themes_defined": IMPROVEMENT_THEME_IDS,
        "improvement_options_defined": IMPROVEMENT_OPTION_IDS,
        "recommended_option_defined": RECOMMENDED_NEXT_OPTION,
        "diagnostic_questions_defined": DIAGNOSTIC_QUESTIONS,
        "planned_outputs_not_generated": True,
        "planned_outputs_research_only": True,
        "per_ticker_entries_12": 12,
        "per_ticker_digests_present": True,
        "provider_requests_made_false": False,
        "market_data_acquisition_false": False,
        "dataset_regeneration_false": False,
        "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False,
        "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_candidate_false": False,
        "model_training_in_candidate_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False,
        "no_runtime_migration_approval_created": False,
        "next_chain_defined": NEXT_CHAIN,
        "next_gates_defined": NEXT_GATES,
        "risk_controls_defined": RISK_CONTROLS,
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
        "method_evidence_improvement_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "method_evidence_improvement_approved": False,
        "method_evidence_improvement_executed": False,
        "improved_evidence_planning_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(candidate: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(candidate))
    payload.pop("method_evidence_improvement_candidate_using_redesigned_evidence_digest", None)
    return payload


def method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(
    candidate: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_method_evidence_improvement_candidate_using_redesigned_evidence_v1() -> dict:
    """Build the offline candidate without executing or approving improvement work."""
    _source_readiness_review()
    candidate = _base_candidate()
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate["method_evidence_improvement_candidate_using_redesigned_evidence_digest"] = (
        method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(candidate)
    )
    validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(candidate)
    return candidate


def validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(
    candidate: dict,
) -> dict:
    """Validate all evidence bindings and closed authority boundaries."""
    if not isinstance(candidate, dict):
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("candidate must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_V1,
        "candidate_status": METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "source_readiness_review_artifact_kind": SOURCE_ARTIFACT_KIND,
        "source_readiness_review_status": SOURCE_REVIEW_STATUS,
        "source_readiness_decision": SOURCE_READINESS_DECISION,
        "source_readiness_decision_reason": SOURCE_READINESS_DECISION_REASON,
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
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "problem_basis": PROBLEM_BASIS,
        "method_evidence_improvement_objective": METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE,
        "method_evidence_improvement_scope": METHOD_EVIDENCE_IMPROVEMENT_SCOPE,
        "method_evidence_improvement_mode": METHOD_EVIDENCE_IMPROVEMENT_MODE,
        "method_evidence_improvement_authority_status": METHOD_EVIDENCE_IMPROVEMENT_AUTHORITY_STATUS,
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "recommended_next_option_rationale": RECOMMENDED_NEXT_OPTION_RATIONALE,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    true_fields = (
        "created_offline", "research_only", "operator_review_required",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_readiness_review_completed",
        "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence",
        "method_evidence_improvement_candidate_using_redesigned_evidence_created",
        "method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review",
        "meta_reduced_record_count_preserved", "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(candidate.get(field), field)
    false_fields = (
        "method_evidence_improvement_approved", "method_evidence_improvement_authorized",
        "method_evidence_improvement_executed", "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "profitability_acceptance_created", "runtime_migration_approved", "runtime_migration_active",
        "runtime_migration_approval_created", "automatic_stitching", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "provider_requests_made_in_candidate",
        "live_provider_transport_enabled_in_candidate", "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate", "canonical_dataset_regenerated_in_candidate",
        "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed", "metric_recomputation_performed_in_candidate",
        "model_training_performed_in_candidate", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(candidate.get(field), field)

    themes = candidate.get("improvement_themes")
    if not isinstance(themes, list) or [row.get("theme_id") for row in themes] != IMPROVEMENT_THEME_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("improvement themes mismatch")
    for row in themes:
        _expect(row.get("theme_status"), PLANNED_NOT_EXECUTED, "theme status")
        _expect_true(row.get("approval_required_before_execution"), "theme approval required")
        _expect_false(row.get("execution_authorized"), "theme execution authorized")
        _expect_false(row.get("execution_performed"), "theme execution performed")
        _expect_true(row.get("research_only"), "theme research only")
        _expect_true(row.get("non_actionable"), "theme non actionable")

    options = candidate.get("improvement_options")
    if not isinstance(options, list) or [row.get("option_id") for row in options] != IMPROVEMENT_OPTION_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("improvement options mismatch")
    for row in options:
        _expect(row.get("option_status"), "AVAILABLE_FOR_OPERATOR_REVIEW", "option status")
        for field in ("selected", "approved", "executed", "creates_acceptance_candidate"):
            _expect_false(row.get(field), f"option {field}")
        _expect_true(row.get("research_only"), "option research only")
        _expect_true(row.get("non_actionable"), "option non actionable")

    questions = candidate.get("planned_diagnostic_questions")
    if not isinstance(questions, list) or [row.get("question") for row in questions] != DIAGNOSTIC_QUESTIONS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("diagnostic questions mismatch")
    for row in questions:
        _expect(row.get("status"), "NOT_ANSWERED", "diagnostic status")
        _expect_true(row.get("requires_separate_review_or_execution"), "diagnostic separate review")
        _expect_true(row.get("research_only"), "diagnostic research only")
        _expect_true(row.get("non_actionable"), "diagnostic non actionable")

    outputs = candidate.get("planned_outputs")
    if not isinstance(outputs, list) or [row.get("output_name") for row in outputs] != PLANNED_OUTPUT_NAMES:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("planned outputs mismatch")
    for row in outputs:
        _expect(row.get("output_status"), PLANNED_NOT_GENERATED, "planned output status")
        _expect(row.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "planned output label")

    entries = candidate.get("per_ticker_improvement_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("per-ticker entries mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("acceptance_readiness_status"), "NOT_READY", f"{ticker} readiness")
        _expect(entry.get("method_evidence_improvement_candidate_status"), "PLANNED_READY_FOR_OPERATOR_REVIEW", f"{ticker} candidate status")
        _expect(entry.get("source_readiness_review_digest"), EXPECTED_READINESS_REVIEW_DIGEST, f"{ticker} source digest")
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
        digest = entry.get("per_ticker_method_evidence_improvement_candidate_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise MethodEvidenceImprovementCandidateRedesignedEvidenceError(f"{ticker} digest missing")
        _expect(
            digest,
            per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(entry),
            f"{ticker} digest",
        )

    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("candidate checklist mismatch")
    _expect(checklist, _checklist(candidate), "candidate checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("candidate checklist failed")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate summary")

    digest = candidate.get("method_evidence_improvement_candidate_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("candidate digest missing")
    _expect(
        digest,
        method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(candidate),
        "candidate digest",
    )
    return {
        "status": "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "method_evidence_improvement_candidate_using_redesigned_evidence_digest": digest,
        **{
            key: candidate["candidate_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_method_evidence_improvement_candidate_using_redesigned_evidence_markdown_v1(
    candidate: dict,
) -> str:
    """Render a sanitized Markdown view of the validated candidate."""
    validation = validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(candidate)
    sections = [
        ("Title", ["Method / Evidence Improvement Candidate Using Redesigned Evidence"]),
        ("Method / Evidence Improvement Candidate Using Redesigned Evidence", [
            f"Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
            f"Digest: `{validation['method_evidence_improvement_candidate_using_redesigned_evidence_digest']}`.",
        ]),
        ("Source Readiness Review", [
            f"Artifact/status: `{candidate['source_readiness_review_artifact_kind']}` / `{candidate['source_readiness_review_status']}`.",
            f"Decision/reason: `{candidate['source_readiness_decision']}` / `{candidate['source_readiness_decision_reason']}`.",
        ]),
        ("Bound Evidence", [
            f"Readiness/reassessment: `{candidate['predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest']}` / `{candidate['predictive_usefulness_reassessment_using_redesigned_evidence_digest']}`.",
            f"Results/execution/matrix: `{candidate['additional_predictive_evidence_results_review_using_redesigned_labels_digest']}` / `{candidate['additional_predictive_evidence_execution_using_redesigned_labels_digest']}` / `{candidate['feature_label_matrix_digest']}`.",
        ]),
        ("Dataset and Universe", [
            f"Dataset/records: `{candidate['dataset_name']}` / `{candidate['total_canonical_record_count']}`.",
            "Universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]) + ".",
            "META remains `913`; every other ticker remains `1003`.",
        ]),
        ("Problem Basis", [f"`{key}`: `{value}`" for key, value in candidate["problem_basis"].items()]),
        ("Improvement Objective", [
            f"Objective: `{candidate['method_evidence_improvement_objective']}`.",
            f"Scope/mode/authority: `{candidate['method_evidence_improvement_scope']}` / `{candidate['method_evidence_improvement_mode']}` / `{candidate['method_evidence_improvement_authority_status']}`.",
        ]),
        ("Improvement Themes", [f"`{row['theme_id']}`: `{row['theme_status']}`." for row in candidate["improvement_themes"]]),
        ("Improvement Options", [f"`{row['option_id']}`: `{row['option_status']}`; selected `{row['selected']}`." for row in candidate["improvement_options"]] + [f"Recommended: `{candidate['recommended_next_option']}` — `{candidate['recommended_next_option_rationale']}`."]),
        ("Diagnostic Questions", [f"`{row['question']}`: `{row['status']}`." for row in candidate["planned_diagnostic_questions"]]),
        ("Planned Outputs", [f"`{row['output_name']}`: `{row['output_status']}` / `{row['output_label']}`." for row in candidate["planned_outputs"]]),
        ("Per-Ticker Candidate Entries", [f"`{row['ticker']}`: records `{row['historical_record_count']}`, status `{row['method_evidence_improvement_candidate_status']}`, digest `{row['per_ticker_method_evidence_improvement_candidate_digest']}`." for row in candidate["per_ticker_improvement_candidate_entries"]]),
        ("Next Chain", candidate["next_chain"]),
        ("Next Gates", candidate["next_gates"]),
        ("Risk Controls", candidate["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; no acceptance candidate was created."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{candidate['candidate_summary']['total_checks']} / {candidate['candidate_summary']['passed_checks']} / {candidate['candidate_summary']['failed_checks']} / {candidate['candidate_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, execution rerun, metric recomputation, model training, approval, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# Method / Evidence Improvement Candidate Using Redesigned Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_method_evidence_improvement_candidate_using_redesigned_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical candidate JSON without overwriting an existing artifact."""
    candidate = build_method_evidence_improvement_candidate_using_redesigned_evidence_v1()
    validation = validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "method_evidence_improvement_candidate_using_redesigned_evidence_v1.json"
    if path.exists():
        raise MethodEvidenceImprovementCandidateRedesignedEvidenceError("candidate output already exists")
    payload = canonical_json_bytes(candidate)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "method_evidence_improvement_candidate_using_redesigned_evidence_digest": validation[
            "method_evidence_improvement_candidate_using_redesigned_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
