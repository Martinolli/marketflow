"""Offline operator review of the additional predictive evidence execution candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_execution_candidate_service as candidate_service


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_V1 = (
    "additional_predictive_evidence_execution_candidate_review_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY"
)
EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING"
)
EXECUTION_CANDIDATE_OBJECT_BINDING = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    "d7f83a8b7be2be3a663ddb04097bf08b346071f70c9e770dd8f25e9fd9f4947e"
)
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_TOTAL = 69
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_PASSED = 69
EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_EXECUTION_CANDIDATE_BLOCKER_COUNT = 0

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
APPROVED_REGISTRY_METADATA = deepcopy(candidate_service.APPROVED_REGISTRY_METADATA)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "execution_candidate_kind_matches",
    "execution_candidate_status_ready_for_review",
    "execution_candidate_digest_matches_expected",
    "execution_candidate_checklist_zero_blockers",
    "chain_candidate_review_digest_bound",
    "chain_candidate_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_candidate_universe",
    "registry_approval_created_true",
    "research_registry_approved_true",
    "additional_predictive_evidence_chain_candidate_review_created_true",
    "additional_predictive_evidence_execution_candidate_created_true",
    "additional_predictive_evidence_execution_candidate_review_created_true",
    "execution_candidate_scope_candidate_only",
    "execution_authority_status_not_authorized",
    "canonical_dataset_generated_true",
    "canonical_dataset_frozen_true",
    "total_canonical_record_count_11946",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "planned_labels_7_reviewed",
    "planned_features_10_reviewed",
    "planned_execution_protocol_reviewed",
    "planned_split_profile_reviewed",
    "planned_metric_families_reviewed",
    "planned_baselines_reviewed",
    "future_execution_outputs_15_reviewed",
    "future_execution_outputs_not_generated",
    "future_execution_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
    "canonical_dataset_regenerated_in_review_false",
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
    "additional_predictive_evidence_execution_approved_false",
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

FORBIDDEN_ARTIFACT_VALUES = set(candidate_service.FORBIDDEN_ARTIFACT_VALUES)


class AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(ValueError):
    """Raised when an execution-candidate review violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
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


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        bound = candidate_service.build_additional_predictive_evidence_execution_candidate_v1()
        binding_mode = EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING
    else:
        candidate_service.validate_additional_predictive_evidence_execution_candidate_v1(
            candidate
        )
        bound = deepcopy(candidate)
        binding_mode = EXECUTION_CANDIDATE_OBJECT_BINDING
    _expect(
        bound.get("additional_predictive_evidence_execution_candidate_digest"),
        EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "execution candidate digest",
    )
    return bound, binding_mode


def per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one ticker review entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_review_digest",
        None,
    )
    return semantic_digest(payload)


def _per_ticker_review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source in candidate["per_ticker_execution_candidate_entries"]:
        entry = deepcopy(source)
        entry["additional_predictive_evidence_execution_candidate_review_status"] = (
            READY_FOR_OPERATOR_ASSESSMENT
        )
        entry["source_additional_predictive_evidence_execution_candidate_digest"] = (
            candidate["additional_predictive_evidence_execution_candidate_digest"]
        )
        entry[
            "per_ticker_additional_predictive_evidence_execution_candidate_review_digest"
        ] = per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_V1,
        "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "execution_candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_approved": True,
        "registry_approval_created": True,
        "ready_for_additional_predictive_evidence_chain_candidate": True,
        "additional_predictive_evidence_chain_candidate_created": True,
        "additional_predictive_evidence_chain_candidate_review_created": True,
        "additional_predictive_evidence_chain_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_review_created": True,
        "additional_predictive_evidence_execution_candidate_ready_for_operator_review": True,
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
        "reviewed_additional_predictive_evidence_execution_candidate_kind": candidate[
            "artifact_kind"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_status": candidate[
            "candidate_status"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_digest": candidate[
            "additional_predictive_evidence_execution_candidate_digest"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_total": summary[
            "total_checks"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_additional_predictive_evidence_execution_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "additional_predictive_evidence_execution_candidate_digest": candidate[
            "additional_predictive_evidence_execution_candidate_digest"
        ],
        "additional_predictive_evidence_chain_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_chain_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_chain_candidate_digest": candidate[
            "additional_predictive_evidence_chain_candidate_digest"
        ],
        "research_registry_approval_digest": candidate["research_registry_approval_digest"],
        "research_registry_candidate_review_package_digest": candidate[
            "research_registry_candidate_review_package_digest"
        ],
        "research_registry_candidate_digest": candidate["research_registry_candidate_digest"],
        "canonical_dataset_freeze_digest": candidate["canonical_dataset_freeze_digest"],
        "canonical_dataset_results_review_package_digest": candidate[
            "canonical_dataset_results_review_package_digest"
        ],
        "canonical_dataset_generation_digest": candidate[
            "canonical_dataset_generation_digest"
        ],
        "records_digest": candidate["records_digest"],
        "acquisition_generation_freeze_digest": candidate[
            "acquisition_generation_freeze_digest"
        ],
        "corporate_action_authority_approval_digest": candidate[
            "corporate_action_authority_approval_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "reviewed_registry_approved_dataset_metadata": deepcopy(
            candidate["approved_registry_metadata"]
        ),
        "total_canonical_record_count": candidate["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(candidate["per_ticker_record_counts"]),
        "per_ticker_execution_candidate_review_entries": _per_ticker_review_entries(
            candidate
        ),
        "additional_predictive_evidence_execution_candidate_objective": candidate[
            "additional_predictive_evidence_execution_candidate_objective"
        ],
        "additional_predictive_evidence_execution_candidate_scope": candidate[
            "additional_predictive_evidence_execution_candidate_scope"
        ],
        "additional_predictive_evidence_execution_mode": candidate[
            "additional_predictive_evidence_execution_mode"
        ],
        "additional_predictive_evidence_execution_authority_status": candidate[
            "additional_predictive_evidence_execution_authority_status"
        ],
        "reviewed_execution_candidate_profile": deepcopy(
            candidate["execution_candidate_profile"]
        ),
        "reviewed_planned_label_set": deepcopy(candidate["planned_label_set"]),
        "reviewed_planned_feature_set": deepcopy(candidate["planned_feature_set"]),
        "reviewed_planned_execution_protocol": deepcopy(
            candidate["planned_execution_protocol"]
        ),
        "reviewed_planned_split_profile": deepcopy(candidate["planned_split_profile"]),
        "reviewed_planned_metric_families": deepcopy(
            candidate["planned_metric_families"]
        ),
        "reviewed_planned_baselines": deepcopy(candidate["planned_baselines"]),
        "reviewed_future_execution_outputs": deepcopy(
            candidate["future_execution_outputs"]
        ),
        "reviewed_future_execution_chain": list(candidate["future_execution_chain"]),
        "reviewed_future_gates": list(candidate["future_gates"]),
        "reviewed_risk_controls": list(candidate["risk_controls"]),
        "additional_predictive_evidence_execution_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    counts = review_package.get("per_ticker_record_counts", {})
    outputs = review_package.get("reviewed_future_execution_outputs", [])
    return [
        _check("execution_candidate_kind_matches", candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_kind")),
        _check("execution_candidate_status_ready_for_review", candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_status")),
        _check("execution_candidate_digest_matches_expected", EXPECTED_EXECUTION_CANDIDATE_DIGEST, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_digest")),
        _check("execution_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_additional_predictive_evidence_execution_candidate_blocker_count")),
        _check("chain_candidate_review_digest_bound", candidate_service.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("additional_predictive_evidence_chain_candidate_review_package_digest")),
        _check("chain_candidate_digest_bound", candidate_service.EXPECTED_CHAIN_CANDIDATE_DIGEST, review_package.get("additional_predictive_evidence_chain_candidate_digest")),
        _check("research_registry_approval_digest_bound", candidate_service.chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, review_package.get("research_registry_approval_digest")),
        _check("canonical_dataset_freeze_digest_bound", candidate_service.chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, review_package.get("canonical_dataset_freeze_digest")),
        _check("canonical_dataset_generation_digest_bound", candidate_service.chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, review_package.get("canonical_dataset_generation_digest")),
        _check("records_digest_bound", candidate_service.chain_service.EXPECTED_RECORDS_DIGEST, review_package.get("records_digest")),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check("target_universe_matches_execution_candidate_universe", TARGET_UNIVERSE, review_package.get("target_universe")),
        _check("registry_approval_created_true", True, review_package.get("registry_approval_created")),
        _check("research_registry_approved_true", True, review_package.get("research_registry_approved")),
        _check("additional_predictive_evidence_chain_candidate_review_created_true", True, review_package.get("additional_predictive_evidence_chain_candidate_review_created")),
        _check("additional_predictive_evidence_execution_candidate_created_true", True, review_package.get("additional_predictive_evidence_execution_candidate_created")),
        _check("additional_predictive_evidence_execution_candidate_review_created_true", True, review_package.get("additional_predictive_evidence_execution_candidate_review_created")),
        _check("execution_candidate_scope_candidate_only", candidate_service.EXECUTION_CANDIDATE_SCOPE, review_package.get("additional_predictive_evidence_execution_candidate_scope")),
        _check("execution_authority_status_not_authorized", NOT_AUTHORIZED, review_package.get("additional_predictive_evidence_execution_authority_status")),
        _check("canonical_dataset_generated_true", True, review_package.get("canonical_dataset_generated")),
        _check("canonical_dataset_frozen_true", True, review_package.get("canonical_dataset_frozen")),
        _check("total_canonical_record_count_11946", 11946, review_package.get("total_canonical_record_count")),
        _check("meta_record_count_913_preserved", 913, counts.get("META")),
        _check("non_meta_record_counts_1003_preserved", True, all(counts.get(ticker) == 1003 for ticker in TARGET_UNIVERSE if ticker != "META")),
        _check("planned_labels_7_reviewed", 7, len(review_package.get("reviewed_planned_label_set", []))),
        _check("planned_features_10_reviewed", 10, len(review_package.get("reviewed_planned_feature_set", []))),
        _check("planned_execution_protocol_reviewed", candidate_service._planned_protocol(), review_package.get("reviewed_planned_execution_protocol")),
        _check("planned_split_profile_reviewed", candidate_service.PLANNED_SPLIT_PROFILE, review_package.get("reviewed_planned_split_profile")),
        _check("planned_metric_families_reviewed", candidate_service._planned_metrics(), review_package.get("reviewed_planned_metric_families")),
        _check("planned_baselines_reviewed", candidate_service._planned_baselines(), review_package.get("reviewed_planned_baselines")),
        _check("future_execution_outputs_15_reviewed", 15, len(outputs)),
        _check("future_execution_outputs_not_generated", True, bool(outputs) and all(item.get("generation_status") == candidate_service.PLANNED_NOT_GENERATED for item in outputs)),
        _check("future_execution_chain_reviewed", candidate_service.FUTURE_EXECUTION_CHAIN, review_package.get("reviewed_future_execution_chain")),
        _check("future_gates_defined", candidate_service.FUTURE_GATES, review_package.get("reviewed_future_gates")),
        _check("risk_controls_defined", candidate_service.RISK_CONTROLS, review_package.get("reviewed_risk_controls")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_provider_transport_enabled_in_review_false", False, review_package.get("live_provider_transport_enabled_in_review")),
        _check("market_data_acquisition_performed_in_review_false", False, review_package.get("market_data_acquisition_performed_in_review")),
        _check("dataset_generation_performed_in_review_false", False, review_package.get("dataset_generation_performed_in_review")),
        _check("canonical_dataset_regenerated_in_review_false", False, review_package.get("canonical_dataset_regenerated_in_review")),
        _check("label_generation_authorized_false", False, review_package.get("label_generation_authorized")),
        _check("label_generation_performed_false", False, review_package.get("label_generation_performed")),
        _check("feature_matrix_generation_authorized_false", False, review_package.get("feature_matrix_generation_authorized")),
        _check("feature_matrix_generation_performed_false", False, review_package.get("feature_matrix_generation_performed")),
        _check("walk_forward_validation_authorized_false", False, review_package.get("walk_forward_validation_authorized")),
        _check("walk_forward_validation_performed_false", False, review_package.get("walk_forward_validation_performed")),
        _check("out_of_sample_evaluation_authorized_false", False, review_package.get("out_of_sample_evaluation_authorized")),
        _check("out_of_sample_evaluation_performed_false", False, review_package.get("out_of_sample_evaluation_performed")),
        _check("baseline_comparison_authorized_false", False, review_package.get("baseline_comparison_authorized")),
        _check("baseline_comparison_performed_false", False, review_package.get("baseline_comparison_performed")),
        _check("signal_quality_metrics_performed_false", False, review_package.get("signal_quality_metrics_performed")),
        _check("stability_analysis_performed_false", False, review_package.get("stability_analysis_performed")),
        _check("leakage_control_review_performed_false", False, review_package.get("leakage_control_review_performed")),
        _check("additional_predictive_evidence_execution_approved_false", False, review_package.get("additional_predictive_evidence_execution_approved")),
        _check("additional_predictive_evidence_execution_authorized_false", False, review_package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, review_package.get("additional_predictive_evidence_executed")),
        _check("additional_predictive_evidence_results_created_false", False, review_package.get("additional_predictive_evidence_results_created")),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, review_package.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", NOT_ACCEPTED, review_package.get("profitability")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_additional_predictive_evidence_execution_artifact_created", False, review_package.get("additional_predictive_evidence_execution_artifact_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
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
        "ready_for_operator_assessment": failed == 0,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "ready_for_additional_predictive_evidence_execution": False,
        "ready_for_predictive_usefulness_reassessment": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def additional_predictive_evidence_execution_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    payload = deepcopy(review_package)
    payload.pop(
        "additional_predictive_evidence_execution_candidate_review_package_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline review package without creating execution authority."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "additional_predictive_evidence_execution_candidate_review_package_digest"
    ] = additional_predictive_evidence_execution_candidate_review_package_digest_v1(
        review_package
    )
    validate_additional_predictive_evidence_execution_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expected_candidate() -> dict[str, Any]:
    candidate = candidate_service.build_additional_predictive_evidence_execution_candidate_v1()
    _expect(
        candidate["additional_predictive_evidence_execution_candidate_digest"],
        EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "expected execution candidate digest",
    )
    return candidate


def _validate_per_ticker_entries(
    review_package: dict[str, Any], candidate: dict[str, Any]
) -> None:
    entries = review_package.get("per_ticker_execution_candidate_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "per-ticker review entries missing"
        )
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    _expect(entries, _per_ticker_review_entries(candidate), "per-ticker review entries")
    for entry in entries:
        candidate_digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_digest"
        )
        review_digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_review_digest"
        )
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
                "per-ticker execution candidate digest missing"
            )
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
                "per-ticker execution candidate review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(
                entry
            ),
            "per-ticker execution candidate review digest",
        )


def validate_additional_predictive_evidence_execution_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the package is a complete non-authorizing review."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    candidate = _expected_candidate()
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    if review_package.get("execution_candidate_binding_mode") not in {
        EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING,
        EXECUTION_CANDIDATE_OBJECT_BINDING,
    }:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "execution_candidate_binding_mode mismatch"
        )
    for field in (
        "created_offline", "research_registry_approved", "registry_approval_created",
        "ready_for_additional_predictive_evidence_chain_candidate",
        "additional_predictive_evidence_chain_candidate_created",
        "additional_predictive_evidence_chain_candidate_review_created",
        "additional_predictive_evidence_chain_ready_for_operator_review",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_review_created",
        "additional_predictive_evidence_execution_candidate_ready_for_operator_review",
        "canonical_dataset_generated", "canonical_dataset_frozen", "research_only",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "additional_predictive_evidence_execution_approved",
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
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    expected_fields = {
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "reviewed_additional_predictive_evidence_execution_candidate_kind": candidate["artifact_kind"],
        "reviewed_additional_predictive_evidence_execution_candidate_status": candidate["candidate_status"],
        "reviewed_additional_predictive_evidence_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_total": EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_passed": EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_additional_predictive_evidence_execution_candidate_checklist_failed": EXPECTED_EXECUTION_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_additional_predictive_evidence_execution_candidate_blocker_count": EXPECTED_EXECUTION_CANDIDATE_BLOCKER_COUNT,
        "additional_predictive_evidence_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "additional_predictive_evidence_chain_candidate_review_package_digest": candidate["additional_predictive_evidence_chain_candidate_review_package_digest"],
        "additional_predictive_evidence_chain_candidate_digest": candidate["additional_predictive_evidence_chain_candidate_digest"],
        "research_registry_approval_digest": candidate["research_registry_approval_digest"],
        "research_registry_candidate_review_package_digest": candidate["research_registry_candidate_review_package_digest"],
        "research_registry_candidate_digest": candidate["research_registry_candidate_digest"],
        "canonical_dataset_freeze_digest": candidate["canonical_dataset_freeze_digest"],
        "canonical_dataset_results_review_package_digest": candidate["canonical_dataset_results_review_package_digest"],
        "canonical_dataset_generation_digest": candidate["canonical_dataset_generation_digest"],
        "records_digest": candidate["records_digest"],
        "acquisition_generation_freeze_digest": candidate["acquisition_generation_freeze_digest"],
        "corporate_action_authority_approval_digest": candidate["corporate_action_authority_approval_digest"],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "ticker_universe_selection_approval_digest": candidate["ticker_universe_selection_approval_digest"],
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "reviewed_registry_approved_dataset_metadata": APPROVED_REGISTRY_METADATA,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "additional_predictive_evidence_execution_candidate_objective": candidate_service.EXECUTION_CANDIDATE_OBJECTIVE,
        "additional_predictive_evidence_execution_candidate_scope": candidate_service.EXECUTION_CANDIDATE_SCOPE,
        "additional_predictive_evidence_execution_mode": candidate_service.EXECUTION_MODE,
        "additional_predictive_evidence_execution_authority_status": NOT_AUTHORIZED,
        "reviewed_execution_candidate_profile": candidate["execution_candidate_profile"],
        "reviewed_planned_label_set": candidate["planned_label_set"],
        "reviewed_planned_feature_set": candidate["planned_feature_set"],
        "reviewed_planned_execution_protocol": candidate["planned_execution_protocol"],
        "reviewed_planned_split_profile": candidate["planned_split_profile"],
        "reviewed_planned_metric_families": candidate["planned_metric_families"],
        "reviewed_planned_baselines": candidate["planned_baselines"],
        "reviewed_future_execution_outputs": candidate["future_execution_outputs"],
        "reviewed_future_execution_chain": candidate["future_execution_chain"],
        "reviewed_future_gates": candidate["future_gates"],
        "reviewed_risk_controls": candidate["risk_controls"],
    }
    for field, expected in expected_fields.items():
        value = review_package.get(field)
        if isinstance(expected, (list, dict)) and not value:
            raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
                f"{field} missing"
            )
        _expect(value, expected, field)
    _validate_per_ticker_entries(review_package, candidate)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
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
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "additional_predictive_evidence_execution_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "review package digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_review_package_digest_v1(
            review_package
        ),
        "review package digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "additional_predictive_evidence_execution_candidate_review_package_digest": digest,
        "reviewed_additional_predictive_evidence_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "ready_for_operator_assessment": expected_summary["ready_for_operator_assessment"],
        "blocker_count": expected_summary["blocker_count"],
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized Markdown execution-candidate review summary."""
    validation = validate_additional_predictive_evidence_execution_candidate_review_package_v1(
        review_package
    )
    metadata = review_package["reviewed_registry_approved_dataset_metadata"]
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Operator Review",
        "", "## Title", "- Additional Predictive Evidence Execution Candidate Operator Review Package v1.",
        "", "## Additional Predictive Evidence Execution Candidate Review Package",
        f"- Artifact: `{review_package['artifact_kind']}`",
        f"- Status: `{review_package['review_status']}`",
        f"- Review digest: `{validation['additional_predictive_evidence_execution_candidate_review_package_digest']}`",
        "", "## Reviewed Execution Candidate",
        f"- Candidate digest: `{review_package['reviewed_additional_predictive_evidence_execution_candidate_digest']}`",
        f"- Candidate checks/blockers: `{review_package['reviewed_additional_predictive_evidence_execution_candidate_checklist_passed']} / {review_package['reviewed_additional_predictive_evidence_execution_candidate_blocker_count']}`",
        "", "## Source Chain Candidate Review",
        f"- Chain review digest: `{review_package['additional_predictive_evidence_chain_candidate_review_package_digest']}`",
        f"- Chain candidate digest: `{review_package['additional_predictive_evidence_chain_candidate_digest']}`",
        "", "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in metadata.items())
    lines.extend(["", "## Target Universe", f"- `{' '.join(review_package['target_universe'])}`"])
    lines.extend(["", "## Per-Ticker Execution Candidate Review Entries"])
    lines.extend(f"- `{item['ticker']}`: `{item['historical_record_count']}` records; `{item['additional_predictive_evidence_execution_candidate_review_status']}`" for item in review_package["per_ticker_execution_candidate_review_entries"])
    lines.extend(["", "## Reviewed Label Set"])
    lines.extend(f"- `{item['label_family']}`: `{item['execution_candidate_status']}`" for item in review_package["reviewed_planned_label_set"])
    lines.extend(["", "## Reviewed Feature Set"])
    lines.extend(f"- `{item['feature_family']}`: `{item['execution_candidate_status']}`" for item in review_package["reviewed_planned_feature_set"])
    lines.extend(["", "## Reviewed Execution Protocol"])
    lines.extend(f"- `{item['protocol_item']}`: `{item['execution_status']}`" for item in review_package["reviewed_planned_execution_protocol"])
    lines.extend(["", "## Reviewed Split Profile"])
    lines.extend(f"- {key}: `{value}`" for key, value in review_package["reviewed_planned_split_profile"].items())
    for heading, key, id_field in (
        ("Reviewed Metric Families", "reviewed_planned_metric_families", "metric_family"),
        ("Reviewed Baselines", "reviewed_planned_baselines", "baseline"),
        ("Reviewed Future Execution Outputs", "reviewed_future_execution_outputs", "output_id"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_field]}`" for item in review_package[key])
    for heading, values in (
        ("Future Execution Chain", review_package["reviewed_future_execution_chain"]),
        ("Future Gates", review_package["reviewed_future_gates"]),
        ("Risk Controls", review_package["reviewed_risk_controls"]),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {value}" for value in values)
    lines.extend([
        "", "## Predictive Usefulness Boundary", f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
        "", "## Profitability Boundary", f"- profitability: `{review_package['profitability']}`",
        "", "## Runtime Boundary", f"- runtime_use: `{review_package['runtime_use']}`", f"- strategy_use: `{review_package['strategy_use']}`", f"- paper_trading: `{review_package['paper_trading']}`", f"- broker_execution: `{review_package['broker_execution']}`",
        "", "## Checklist Summary", f"- Total checks: `{summary['total_checks']}`", f"- Passed checks: `{summary['passed_checks']}`", f"- Failed checks: `{summary['failed_checks']}`", f"- Blocker count: `{summary['blocker_count']}`",
        "", "## Guardrails", "- Review only; no predictive evidence execution is approved, authorized, or performed.", "- No labels, features, metrics, baselines, walk-forward validation, or out-of-sample evaluation are generated or computed.", "- No provider request, dataset regeneration, predictive/profitability acceptance, runtime activation, or trading action occurs.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON once; existing output fails closed."""
    review_package = build_additional_predictive_evidence_execution_candidate_review_package_v1(
        candidate
    )
    validation = validate_additional_predictive_evidence_execution_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "additional_predictive_evidence_execution_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError(
            "review output already exists"
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
