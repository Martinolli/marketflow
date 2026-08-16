"""Offline approval ceremony for future predictive work using refined evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_for_refined_evidence_operator_review_service as candidate_review,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_V1 = (
    "additional_predictive_evidence_execution_approval_for_refined_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY"
)
OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE = (
    "APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "additional_predictive_evidence_execution_approval_for_refined_evidence_operator_attestation_v1"
)
REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ATTESTATION_PHRASE = (
    "APPROVE ADDITIONAL PREDICTIVE EVIDENCE EXECUTION FOR REFINED EVIDENCE MSFT NVDA "
    "AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY"
)

EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "5cee77990a1f40689ee45ab2f65e2adda070e79970e12d52169f7e88236f6e04"
)
EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST = (
    "dce3a92d05eaba5c2b9307c08799c27bbadb69e804c27c157c7290eec705c340"
)
EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST = (
    "00604008d3c647f45896cd8b6707de519ed6eda4e32566b3c99910441ec6cc79"
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST = (
    "377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36"
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST = (
    "1b98237ae9156875ca703396b6e1fabf2acf31ab607789247f8af2391d8b5c20"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST = (
    "167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8"
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST = (
    "61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    "02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

TARGET_UNIVERSE = list(candidate_review.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_review.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    candidate_review.candidate_service.REGISTRY_APPROVED_DATASET_METADATA
)
NOT_ACCEPTED = candidate_review.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

EXECUTION_OBJECTIVE = (
    "EXECUTE_ADDITIONAL_PREDICTIVE_EVIDENCE_USING_REVIEWED_REFINED_FEATURE_LABEL_EVIDENCE"
)
EXECUTION_MODE = AUTHORIZED_NOT_EXECUTED
EXECUTION_AUTHORITY_STATUS = "AUTHORIZED_FOR_FUTURE_REFINED_EVIDENCE_EXECUTION_ONLY"
SOURCE_REFINEMENT_OUTPUT_ROOT = ".marketflow/feature_label_refinement/expanded_universe_v1/"

APPROVED_EXECUTION_ACTIVITY_IDS = list(
    candidate_review.candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
)
FUTURE_EXECUTION_OUTPUT_IDS = list(candidate_review.candidate_service.PLANNED_OUTPUT_IDS)
NEXT_CHAIN = [
    "Additional Predictive Evidence Execution for Refined Evidence.",
    "Additional Predictive Evidence Results Review for Refined Evidence.",
    "Predictive Usefulness Reassessment Review rerun using refined evidence.",
    "Predictive Usefulness Acceptance Readiness Review rerun.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "additional_predictive_evidence_execution_for_refined_evidence",
    "additional_predictive_evidence_results_review_for_refined_evidence",
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence",
    "predictive_usefulness_acceptance_readiness_review_rerun",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_approval_does_not_execute_refined_evidence",
    "no_predictive_usefulness_acceptance_from_execution_approval",
    "no_acceptance_when_readiness_not_met",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "do_not_mutate_frozen_canonical_dataset",
    "do_not_rerun_refinement_outputs_without_new_approval",
    "preserve_meta_reduced_record_count",
    "all_outputs_labeled_research_only",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
]

DIGEST_CONFIRMATIONS = {
    "operator_confirms_refined_evidence_candidate_review_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST,
    "operator_confirms_refined_evidence_candidate_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST,
    "operator_confirms_feature_label_refinement_results_review_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
    "operator_confirms_feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
    "operator_confirms_feature_label_refinement_execution_approval_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
    "operator_confirms_additional_predictive_evidence_results_review_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST,
    "operator_confirms_additional_predictive_evidence_execution_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST,
    "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
}
VALUE_CONFIRMATIONS = {
    "operator_confirms_target_universe": TARGET_UNIVERSE,
    "operator_confirms_target_count": 12,
    "operator_confirms_meta_record_count": 913,
    "operator_confirms_non_meta_record_count": 1003,
    "operator_confirms_refined_label_family_count": 7,
    "operator_confirms_refined_feature_group_count": 9,
    "operator_confirms_refined_feature_field_count": 19,
    "operator_confirms_refined_protocol_group_count": 6,
    "operator_confirms_model_comparison_group_count": 5,
    "operator_confirms_refined_leakage_status": PASS,
}
BOOLEAN_CONFIRMATIONS = [
    "operator_confirms_execution_approval_scope_only",
    "operator_confirms_execution_authorized",
    "operator_confirms_no_execution_performed",
    "operator_confirms_no_results_created",
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


class AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(ValueError):
    """Raised when the approval-only contract is not satisfied."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
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


def build_additional_predictive_evidence_execution_approval_for_refined_evidence_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_refined_evidence_candidate_review_digest: str,
    operator_confirms_refined_evidence_candidate_digest: str,
    operator_confirms_feature_label_refinement_results_review_digest: str,
    operator_confirms_feature_label_refinement_execution_digest: str,
    operator_confirms_feature_label_refinement_execution_approval_digest: str,
    operator_confirms_additional_predictive_evidence_results_review_digest: str,
    operator_confirms_additional_predictive_evidence_execution_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_refined_label_family_count: int,
    operator_confirms_refined_feature_group_count: int,
    operator_confirms_refined_feature_field_count: int,
    operator_confirms_refined_protocol_group_count: int,
    operator_confirms_model_comparison_group_count: int,
    operator_confirms_refined_leakage_status: str,
    operator_confirms_execution_approval_scope_only: bool,
    operator_confirms_execution_authorized: bool,
    operator_confirms_no_execution_performed: bool,
    operator_confirms_no_results_created: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build the complete non-secret operator attestation."""
    return deepcopy(locals())


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    values = attestation if isinstance(attestation, dict) else {}
    checks = [
        _check(
            "operator_decision_approved",
            OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE,
            values.get("operator_decision"),
        ),
        _check(
            "operator_attestation_phrase_matches",
            REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ATTESTATION_PHRASE,
            values.get("operator_attestation_phrase"),
        ),
    ]
    checks.extend(
        _check(f"attestation_{field}", expected, values.get(field))
        for field, expected in {**DIGEST_CONFIRMATIONS, **VALUE_CONFIRMATIONS}.items()
    )
    checks.extend(
        _check(f"attestation_{field}", True, values.get(field))
        for field in BOOLEAN_CONFIRMATIONS
    )
    return checks


def _validated_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            "operator_attestation must be a JSON object"
        )
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
                f"{field} must be a non-empty string"
            )
    failures = [item for item in _attestation_checks(attestation) if item["status"] == FAIL]
    if failures:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            f"operator attestation failed: {failures[0]['check_id']}"
        )
    return deepcopy(attestation)


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        deepcopy(review_package)
        if review_package is not None
        else candidate_review.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1()
    )
    candidate_review.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        source
    )
    _expect(
        source.get(
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"
        ),
        EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "refined evidence candidate review digest",
    )
    _expect(
        source.get(
            "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        ),
        EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST,
        "refined evidence candidate digest",
    )
    _expect(source.get("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_blocker_count"), 0, "source review blocker count")
    return source


def per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(
    entry: dict[str, Any],
) -> str:
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest",
        None,
    )
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        count = EXPECTED_RECORD_COUNTS[ticker]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": count,
            "meta_reduced_record_count_flag": ticker == "META",
            "feature_label_refinement_results_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_for_refined_evidence_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "additional_predictive_evidence_execution_for_refined_evidence_approval_status": "APPROVED_FOR_FUTURE_REFINED_EVIDENCE_EXECUTION_ONLY",
            "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
            "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST,
        }
        if ticker == "META":
            entry["refinement_note"] = (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_REFINED_EVIDENCE_CHAIN"
            )
        entry[
            "per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
        ] = per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _execution_activities() -> list[dict[str, Any]]:
    return [
        {
            "activity_id": activity_id,
            "authorization_status": AUTHORIZED_NOT_EXECUTED,
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for activity_id in APPROVED_EXECUTION_ACTIVITY_IDS
    ]


def _future_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "authorization_status": AUTHORIZED_NOT_GENERATED,
            "output_status": AUTHORIZED_NOT_GENERATED,
            "registry_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
        }
        for output_id in FUTURE_EXECUTION_OUTPUT_IDS
    ]


def _source_fields(source: dict[str, Any]) -> dict[str, Any]:
    names = [
        "feature_label_refinement_results_review_package_digest",
        "feature_label_refinement_execution_digest",
        "feature_label_refinement_execution_approval_digest",
        "additional_predictive_evidence_results_review_package_digest",
        "additional_predictive_evidence_execution_digest",
        "research_registry_approval_digest",
        "canonical_dataset_freeze_digest",
        "records_digest",
        "registry_approved_dataset_metadata",
        "dataset_name",
        "total_canonical_record_count",
        "per_ticker_record_counts",
        "meta_record_count",
        "non_meta_record_count",
        "source_refinement_output_root",
        "source_refinement_output_count",
        "source_refinement_output_status",
        "source_refinement_results_review_ready",
        "refined_label_family_count",
        "refined_label_coverage_entries",
        "refined_label_available_values",
        "refined_label_unavailable_values",
        "refined_label_generation_digest",
        "refined_feature_group_count",
        "refined_feature_category_count",
        "refined_feature_field_count",
        "refined_feature_rows",
        "refined_feature_null_or_unavailable_values",
        "refined_feature_generation_digest",
        "refined_protocol_group_count",
        "chronological_splits",
        "one_session_embargo",
        "no_shuffle",
        "no_lookahead",
        "refined_walk_forward_fold_count",
        "refined_walk_forward_evaluation_rows",
        "refined_oos_evaluation_rows",
        "refined_oos_accuracy_range",
        "model_comparison_group_count",
        "deterministic_comparisons_evaluated",
        "unavailable_model_family_requests",
        "unavailable_model_family_status",
        "refined_leakage_status",
        "failed_leakage_controls",
        "data_quality_status",
    ]
    return {
        "source_refined_evidence_candidate_review_package_kind": source["artifact_kind"],
        "source_refined_evidence_candidate_review_status": source["review_status"],
        "source_refined_evidence_candidate_review_checklist_total": source["review_summary"]["total_checks"],
        "source_refined_evidence_candidate_review_checklist_passed": source["review_summary"]["passed_checks"],
        "source_refined_evidence_candidate_review_checklist_failed": source["review_summary"]["failed_checks"],
        "source_refined_evidence_candidate_review_blocker_count": source["review_summary"]["blocker_count"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": source["additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"],
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": source["reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"],
        **{name: deepcopy(source[name]) for name in names},
    }


FALSE_BOUNDARY_FIELDS = [
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "feature_label_refinement_execution_rerun_performed",
    "refined_label_generation_rerun_performed",
    "refined_feature_generation_rerun_performed",
    "refined_walk_forward_validation_rerun_performed",
    "refined_out_of_sample_evaluation_rerun_performed",
    "refined_metrics_recomputation_performed",
    "model_comparison_rerun_performed",
    "additional_predictive_evidence_execution_performed",
    "additional_predictive_evidence_execution_for_refined_evidence_executed",
    "additional_predictive_evidence_results_for_refined_evidence_created",
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
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "additional_predictive_evidence_execution_for_refined_evidence_artifact_created",
    "predictive_usefulness_acceptance_artifact_created",
    "profitability_acceptance_created",
    "runtime_migration_approval_created",
]


def _approval_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    expected_fields = {
        "refined_evidence_candidate_review_digest_matches_expected": (EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest")),
        "refined_evidence_candidate_review_has_zero_blockers": (0, artifact.get("source_refined_evidence_candidate_review_blocker_count")),
        "refined_evidence_candidate_digest_bound": (EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST, artifact.get("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest")),
        "feature_label_refinement_results_review_digest_bound": (EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST, artifact.get("feature_label_refinement_results_review_package_digest")),
        "feature_label_refinement_execution_digest_bound": (EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST, artifact.get("feature_label_refinement_execution_digest")),
        "feature_label_refinement_execution_approval_digest_bound": (EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST, artifact.get("feature_label_refinement_execution_approval_digest")),
        "additional_predictive_evidence_results_review_digest_bound": (EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST, artifact.get("additional_predictive_evidence_results_review_package_digest")),
        "additional_predictive_evidence_execution_digest_bound": (EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST, artifact.get("additional_predictive_evidence_execution_digest")),
        "research_registry_approval_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, artifact.get("research_registry_approval_digest")),
        "canonical_dataset_freeze_digest_bound": (EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, artifact.get("canonical_dataset_freeze_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_review_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "approval_scope_refined_evidence_execution_only": (ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY, artifact.get("approval_scope")),
        "additional_predictive_evidence_execution_for_refined_evidence_approved_true": (True, artifact.get("additional_predictive_evidence_execution_for_refined_evidence_approved")),
        "additional_predictive_evidence_execution_for_refined_evidence_authorized_true": (True, artifact.get("additional_predictive_evidence_execution_for_refined_evidence_authorized")),
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence_true": (True, artifact.get("ready_for_additional_predictive_evidence_execution_for_refined_evidence")),
        "approved_refined_execution_activities_11": (11, len(artifact.get("approved_refined_evidence_execution_activities", []))),
        "future_outputs_10_authorized_not_generated": (10, len(artifact.get("future_refined_execution_outputs", []))),
        "per_ticker_execution_approval_entries_12": (12, len(artifact.get("per_ticker_execution_approval_entries", []))),
        "per_ticker_execution_approval_digests_present": (True, _per_ticker_digests_valid(artifact.get("per_ticker_execution_approval_entries", []))),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "limitations_recorded": (True, "preserve_meta_reduced_record_count" in artifact.get("risk_controls", [])),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
    }
    checks.extend(_check(check_id, expected, actual) for check_id, (expected, actual) in expected_fields.items())
    checks.extend(_attestation_checks(artifact.get("operator_attestation")))
    checks.extend(
        _check(f"{field}_false", False, artifact.get(field))
        for field in FALSE_BOUNDARY_FIELDS
    )
    return checks


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and bool(entries) and all(
        isinstance(entry, dict)
        and entry.get("per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest")
        == per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(entry)
        for entry in entries
    )


def additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    payload = deepcopy(approved_artifact)
    payload.pop(
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
    *,
    refined_evidence_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Authorize a future research-only run without performing it."""
    source = _source_review_package(refined_evidence_candidate_review_package)
    attestation = _validated_attestation(operator_attestation)
    artifact = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY,
        "created_offline": True,
        "feature_label_refinement_execution_approved": True,
        "feature_label_refinement_execution_authorized": True,
        "feature_label_refinement_executed": True,
        "feature_label_refinement_results_created": True,
        "feature_label_refinement_results_review_created": True,
        "feature_label_refinement_results_review_ready": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created": True,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_for_refined_evidence_approved": True,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "research_only": True,
        "operator_review_required": True,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "additional_predictive_evidence_execution_for_refined_evidence_objective": EXECUTION_OBJECTIVE,
        "additional_predictive_evidence_execution_for_refined_evidence_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY,
        "additional_predictive_evidence_execution_for_refined_evidence_mode": EXECUTION_MODE,
        "additional_predictive_evidence_execution_for_refined_evidence_authority_status": EXECUTION_AUTHORITY_STATUS,
        "approved_refined_evidence_execution_activities": _execution_activities(),
        "future_refined_execution_outputs": _future_outputs(),
        "per_ticker_execution_approval_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "operator_attestation": attestation,
        **{field: False for field in FALSE_BOUNDARY_FIELDS},
        **_source_fields(source),
    }
    checklist = _approval_checklist(artifact)
    artifact["approval_checklist"] = checklist
    failed = [item for item in checklist if item["status"] == FAIL]
    artifact["approval_summary"] = {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for item in failed if item["severity"] == BLOCKER),
        "additional_predictive_evidence_execution_for_refined_evidence_approved_by_operator": True,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY,
        "additional_predictive_evidence_execution_for_refined_evidence_authorized": True,
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence": True,
        "additional_predictive_evidence_execution_for_refined_evidence_executed": False,
        "additional_predictive_evidence_results_for_refined_evidence_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }
    artifact[
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
    ] = additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(
        artifact
    )
    validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
        artifact
    )
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden(value: Any, path: str = "approved_artifact") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in FALSE_BOUNDARY_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
                    f"{child} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
                    f"{child} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
                    f"{child} must not be accepted"
                )
            _reject_forbidden(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden(item, f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless this is an approval-only, not-executed artifact."""
    if not isinstance(approved_artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            "approved_artifact must be a JSON object"
        )
    _reject_forbidden(approved_artifact)
    expected = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "refined_label_family_count": 7,
        "refined_feature_group_count": 9,
        "refined_feature_field_count": 19,
        "refined_protocol_group_count": 6,
        "model_comparison_group_count": 5,
        "refined_leakage_status": PASS,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST,
        "feature_label_refinement_results_review_package_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "registry_approved_dataset_metadata": REGISTRY_APPROVED_DATASET_METADATA,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "source_refinement_output_root": SOURCE_REFINEMENT_OUTPUT_ROOT,
        "source_refinement_output_count": 12,
        "source_refinement_output_status": "REVIEWED_AND_VERIFIED",
        "source_refinement_results_review_ready": True,
        "refined_label_coverage_entries": 84,
        "refined_label_available_values": 82698,
        "refined_label_unavailable_values": 924,
        "refined_label_generation_digest": "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8",
        "refined_feature_category_count": 11,
        "refined_feature_rows": 11946,
        "refined_feature_null_or_unavailable_values": 1128,
        "refined_feature_generation_digest": "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00",
        "chronological_splits": True,
        "one_session_embargo": True,
        "no_shuffle": True,
        "no_lookahead": True,
        "refined_walk_forward_fold_count": 4,
        "refined_walk_forward_evaluation_rows": 3024,
        "refined_oos_evaluation_rows": 2988,
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "deterministic_comparisons_evaluated": 7,
        "unavailable_model_family_requests": 3,
        "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "failed_leakage_controls": 0,
        "data_quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "approved_refined_evidence_execution_activities": _execution_activities(),
        "future_refined_execution_outputs": _future_outputs(),
        "per_ticker_execution_approval_entries": _per_ticker_entries(),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(approved_artifact.get(field), expected_value, field)
    for field in (
        "created_offline",
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "feature_label_refinement_results_review_created",
        "feature_label_refinement_results_review_ready",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review",
        "additional_predictive_evidence_execution_for_refined_evidence_approved",
        "additional_predictive_evidence_execution_for_refined_evidence_authorized",
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in FALSE_BOUNDARY_FIELDS:
        _expect_false(approved_artifact.get(field), field)
    _validated_attestation(approved_artifact.get("operator_attestation"))
    _expect_true(_per_ticker_digests_valid(approved_artifact.get("per_ticker_execution_approval_entries")), "per-ticker approval digests")
    checklist = _approval_checklist(approved_artifact)
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = approved_artifact.get("approval_summary")
    if not isinstance(summary, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            "approval_summary must be a JSON object"
        )
    _expect(summary.get("total_checks"), len(checklist), "approval_summary.total_checks")
    _expect(summary.get("passed_checks"), len(checklist), "approval_summary.passed_checks")
    _expect(summary.get("failed_checks"), 0, "approval_summary.failed_checks")
    _expect(summary.get("blocker_count"), 0, "approval_summary.blocker_count")
    digest = approved_artifact.get(
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
    )
    if not isinstance(digest, str) or not digest:
        raise AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError(
            "approval digest is required"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_approval_for_refined_evidence_digest_v1(
            approved_artifact
        ),
        "approval digest",
    )
    return {
        "valid": True,
        "validation_status": "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_VALID",
        "total_checks": len(checklist),
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_additional_predictive_evidence_execution_approved_for_refined_evidence_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
        approved_artifact
    )
    summary = approved_artifact["approval_summary"]
    lines = [
        "# Additional Predictive Evidence Execution Approval for Refined Evidence",
        "",
        "## Approved Additional Predictive Evidence Execution for Refined Evidence",
        f"- Artifact: `{approved_artifact['artifact_kind']}`",
        f"- Status: `{approved_artifact['approval_status']}`",
        f"- Scope: `{approved_artifact['approval_scope']}`",
        f"- Digest: `{approved_artifact['additional_predictive_evidence_execution_approval_for_refined_evidence_digest']}`",
        "",
        "## Operator Attestation",
        f"- Reference: `{approved_artifact['operator_attestation']['operator_reference']}`",
        f"- Timestamp: `{approved_artifact['operator_attestation']['operator_attestation_timestamp_utc']}`",
        "",
        "## Source Refined-Evidence Candidate Review",
        f"- Review digest: `{approved_artifact['additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['additional_predictive_evidence_execution_candidate_for_refined_evidence_digest']}`",
        "",
        "## Source Feature/Label Refinement Results Review",
        f"- Review digest: `{approved_artifact['feature_label_refinement_results_review_package_digest']}`",
        f"- Execution digest: `{approved_artifact['feature_label_refinement_execution_digest']}`",
        "",
        "## Registry-Approved Dataset Metadata",
        f"- Dataset: `{approved_artifact['dataset_name']}`",
        f"- Records: `{approved_artifact['total_canonical_record_count']}`",
        "",
        "## Target Universe",
        "- " + ", ".join(approved_artifact["target_universe"]),
        "",
        "## Approved Refined Evidence Source Profile",
        f"- Root: `{approved_artifact['source_refinement_output_root']}`",
        f"- Outputs: `{approved_artifact['source_refinement_output_count']}`",
        "",
        "## Approved Refined Evidence Facts",
        f"- Label families: `{approved_artifact['refined_label_family_count']}`",
        f"- Feature groups/fields: `{approved_artifact['refined_feature_group_count']}` / `{approved_artifact['refined_feature_field_count']}`",
        f"- Leakage: `{approved_artifact['refined_leakage_status']}`",
        "",
        "## Approved Execution Activities",
        *[f"- `{item['activity_id']}`: `{item['authorization_status']}`" for item in approved_artifact["approved_refined_evidence_execution_activities"]],
        "",
        "## Future Execution Outputs",
        *[f"- `{item['output_id']}`: `{item['output_status']}`" for item in approved_artifact["future_refined_execution_outputs"]],
        "",
        "## Per-Ticker Approval Entries",
        *[f"- `{item['ticker']}`: `{item['historical_record_count']}` records" for item in approved_artifact["per_ticker_execution_approval_entries"]],
        "",
        "## Execution Boundary",
        "Approval authorizes only future refined-evidence research execution; no execution or results were created.",
        "",
        "## Predictive Usefulness Boundary",
        "Predictive usefulness remains not accepted.",
        "",
        "## Profitability Boundary",
        "Profitability remains not accepted.",
        "",
        "## Runtime Boundary",
        "Runtime, strategy, paper-trading, and broker use remain NOT_AUTHORIZED.",
        "",
        "## Checklist Summary",
        f"- `{summary['passed_checks']}/{summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "",
        "## Remaining Required Tasks",
        *[f"- {item}" for item in approved_artifact["next_chain"]],
        "",
        "## Guardrails",
        *[f"- `{item}`" for item in approved_artifact["risk_controls"]],
        "",
    ]
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
    output_dir: str | Path,
    *,
    refined_evidence_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write deterministic JSON and Markdown without overwriting existing files."""
    artifact = build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
        refined_evidence_candidate_review_package=refined_evidence_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    json_path = root / "additional_predictive_evidence_execution_approved_for_refined_evidence_v1.json"
    markdown_path = root / "additional_predictive_evidence_execution_approved_for_refined_evidence_v1.md"
    for path in (json_path, markdown_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite existing artifact: {path}")
    json_bytes = canonical_json_bytes(artifact)
    json_path.write_bytes(json_bytes)
    markdown_path.write_text(
        build_additional_predictive_evidence_execution_approved_for_refined_evidence_markdown_v1(
            artifact
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "approved_artifact": artifact,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "json_sha256": sha256_bytes(json_bytes),
    }
