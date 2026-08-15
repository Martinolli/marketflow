"""Offline approval ceremony for future additional predictive evidence execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_operator_review_service as candidate_review,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_V1 = (
    "additional_predictive_evidence_execution_approval_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION = (
    "APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "additional_predictive_evidence_execution_approval_operator_attestation_v1"
)
REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE ADDITIONAL PREDICTIVE EVIDENCE EXECUTION MSFT NVDA AMZN GOOGL META "
    "TSLA JPM XOM JNJ WMT CAT LMT ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)

EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "ab41b9e28693ca770c85a7e872d640f04b7c59c97b3b8eb40b28c9b101652ff7"
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    "d7f83a8b7be2be3a663ddb04097bf08b346071f70c9e770dd8f25e9fd9f4947e"
)
EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "41e7b4db107a056790b1caa749b789d434698c6416333328297b894fa0832c82"
)
EXPECTED_CHAIN_CANDIDATE_DIGEST = (
    "672b6d8d6299078df718247f3accea1250ea0c0228fa5315738d6e9ad7e055cf"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST = (
    "02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc"
)
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    "9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)

TARGET_UNIVERSE = list(candidate_review.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_review.EXPECTED_RECORD_COUNTS)
APPROVED_REGISTRY_METADATA = deepcopy(candidate_review.APPROVED_REGISTRY_METADATA)
EXPECTED_REVIEW_CHECKLIST_TOTAL = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_PASSED = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
APPROVED_FOR_FUTURE_EXECUTION_ONLY = "APPROVED_FOR_FUTURE_EXECUTION_ONLY"
NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED = (
    "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED"
)
NOT_ACCEPTED = candidate_review.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

APPROVED_LABEL_FAMILIES = list(candidate_review.candidate_service.PLANNED_LABEL_FAMILIES)
APPROVED_FEATURE_FAMILIES = list(candidate_review.candidate_service.PLANNED_FEATURE_FAMILIES)
APPROVED_EXECUTION_PROTOCOL_IDS = list(
    candidate_review.candidate_service.PLANNED_EXECUTION_PROTOCOL_IDS
)
APPROVED_METRIC_FAMILY_IDS = list(
    candidate_review.candidate_service.PLANNED_METRIC_FAMILY_IDS
)
APPROVED_BASELINE_IDS = list(candidate_review.candidate_service.PLANNED_BASELINE_IDS)
FUTURE_EXECUTION_OUTPUT_IDS = list(
    candidate_review.candidate_service.FUTURE_EXECUTION_OUTPUT_IDS
)

APPROVED_SPLIT_PROFILE = {
    "training_window": "2022-01-01 to 2023-12-31",
    "validation_window": "2024-01-01 to 2024-12-31",
    "out_of_sample_window": "2025-01-01 to 2025-12-31",
    "embargo_gap_policy": "TO_BE_APPLIED_DURING_EXECUTION",
    "walk_forward_policy": (
        "EXPANDING_OR_ROLLING_WINDOWS_TO_BE_FINALIZED_DURING_EXECUTION_WITH_STATUS_RECORD"
    ),
}

FUTURE_EXECUTION_CHAIN = [
    "Additional predictive evidence execution.",
    "Additional predictive evidence results review package.",
    "Predictive usefulness reassessment candidate.",
    "Predictive usefulness reassessment candidate review package.",
    "Predictive usefulness acceptance readiness review.",
    "Predictive usefulness acceptance ceremony, only if evidence is sufficient.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "additional_predictive_evidence_execution",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_candidate",
    "predictive_usefulness_reassessment_review",
    "predictive_usefulness_acceptance_readiness_review",
    "predictive_usefulness_acceptance_ceremony_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "execution_approval_does_not_execute",
    "no_predictive_usefulness_acceptance_without_results_review",
    "no_profitability_acceptance_without_separate_review",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "preserve_meta_reduced_record_count",
    "do_not_mutate_frozen_canonical_dataset",
    "all_outputs_labeled_research_only",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
]

DIGEST_CONFIRMATION_EXPECTATIONS = {
    "operator_confirms_execution_candidate_review_digest": (
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    ),
    "operator_confirms_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
    "operator_confirms_chain_candidate_review_digest": (
        EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
    ),
    "operator_confirms_research_registry_approval_digest": (
        EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
    ),
    "operator_confirms_canonical_dataset_freeze_digest": (
        EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
    ),
    "operator_confirms_canonical_dataset_generation_digest": (
        EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    ),
    "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
}
BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_meta_reduced_record_count_preserved",
    "operator_confirms_approval_scope_execution_only",
    "operator_confirms_execution_authorized",
    "operator_confirms_label_generation_authorized",
    "operator_confirms_feature_matrix_generation_authorized",
    "operator_confirms_walk_forward_validation_authorized",
    "operator_confirms_out_of_sample_evaluation_authorized",
    "operator_confirms_baseline_comparison_authorized",
    "operator_confirms_signal_quality_metrics_authorized",
    "operator_confirms_stability_analysis_authorized",
    "operator_confirms_leakage_control_review_authorized",
    "operator_confirms_predictive_experiment_rerun_authorized",
    "operator_confirms_no_execution_performed",
    "operator_confirms_no_results_created",
    "operator_confirms_no_label_generation_performed",
    "operator_confirms_no_feature_matrix_generation_performed",
    "operator_confirms_no_walk_forward_validation_performed",
    "operator_confirms_no_out_of_sample_evaluation_performed",
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

REQUIRED_APPROVAL_CHECK_IDS = [
    "execution_candidate_review_digest_matches_expected",
    "execution_candidate_review_has_zero_blockers",
    "execution_candidate_digest_bound",
    "chain_candidate_review_digest_bound",
    "research_registry_approval_digest_bound",
    "canonical_dataset_freeze_digest_bound",
    "canonical_dataset_generation_digest_bound",
    "records_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_candidate_review_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_target_universe",
    "operator_confirms_target_count",
    "operator_confirms_dataset_name",
    "operator_confirms_total_canonical_record_count_11946",
    *[f"attestation_{field}" for field in DIGEST_CONFIRMATION_EXPECTATIONS],
    *[f"attestation_{field}" for field in BOOLEAN_CONFIRMATION_FIELDS],
    "approval_scope_additional_predictive_execution_only",
    "additional_predictive_evidence_execution_approved_true",
    "additional_predictive_evidence_execution_authorized_true",
    "ready_for_additional_predictive_evidence_execution_true",
    "label_generation_authorized_true",
    "feature_matrix_generation_authorized_true",
    "walk_forward_validation_authorized_true",
    "out_of_sample_evaluation_authorized_true",
    "baseline_comparison_authorized_true",
    "signal_quality_metrics_authorized_true",
    "stability_analysis_authorized_true",
    "leakage_control_review_authorized_true",
    "predictive_experiment_rerun_authorized_true",
    "additional_predictive_evidence_executed_false",
    "additional_predictive_evidence_results_created_false",
    "label_generation_performed_false",
    "feature_matrix_generation_performed_false",
    "walk_forward_validation_performed_false",
    "out_of_sample_evaluation_performed_false",
    "baseline_comparison_performed_false",
    "signal_quality_metrics_performed_false",
    "stability_analysis_performed_false",
    "leakage_control_review_performed_false",
    "predictive_experiment_rerun_performed_false",
    "per_ticker_execution_approval_entries_12",
    "per_ticker_execution_approval_digests_present",
    "approved_label_families_7",
    "approved_feature_families_10",
    "approved_execution_protocol_items_9",
    "approved_metric_families_9",
    "approved_baselines_6",
    "future_outputs_15_authorized_not_generated",
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
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "market_data_acquisition_performed_in_approval_false",
    "dataset_generation_performed_in_approval_false",
    "canonical_dataset_regenerated_in_approval_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "approval_creates_predictive_usefulness_acceptance_false",
    "approval_creates_profitability_acceptance_false",
    "approval_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_additional_predictive_evidence_execution_artifact_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AdditionalPredictiveEvidenceExecutionApprovalError(ValueError):
    """Raised when execution approval evidence violates the guarded contract."""


def _check(
    check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(f"{field} must be false")


def build_additional_predictive_evidence_execution_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_execution_candidate_review_digest: str,
    operator_confirms_execution_candidate_digest: str,
    operator_confirms_chain_candidate_review_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_canonical_dataset_freeze_digest: str,
    operator_confirms_canonical_dataset_generation_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_dataset_name: str,
    operator_confirms_total_canonical_record_count: int,
    operator_confirms_meta_reduced_record_count_preserved: bool,
    operator_confirms_approval_scope_execution_only: bool,
    operator_confirms_execution_authorized: bool,
    operator_confirms_label_generation_authorized: bool,
    operator_confirms_feature_matrix_generation_authorized: bool,
    operator_confirms_walk_forward_validation_authorized: bool,
    operator_confirms_out_of_sample_evaluation_authorized: bool,
    operator_confirms_baseline_comparison_authorized: bool,
    operator_confirms_signal_quality_metrics_authorized: bool,
    operator_confirms_stability_analysis_authorized: bool,
    operator_confirms_leakage_control_review_authorized: bool,
    operator_confirms_predictive_experiment_rerun_authorized: bool,
    operator_confirms_no_execution_performed: bool,
    operator_confirms_no_results_created: bool,
    operator_confirms_no_label_generation_performed: bool,
    operator_confirms_no_feature_matrix_generation_performed: bool,
    operator_confirms_no_walk_forward_validation_performed: bool,
    operator_confirms_no_out_of_sample_evaluation_performed: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for future execution approval."""
    return deepcopy(locals())


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    values = attestation if isinstance(attestation, dict) else {}
    return [
        _check(
            "operator_decision_approved",
            OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION,
            values.get("operator_decision"),
        ),
        _check(
            "operator_attestation_phrase_matches",
            REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ATTESTATION_PHRASE,
            values.get("operator_attestation_phrase"),
        ),
        _check(
            "operator_confirms_target_universe",
            TARGET_UNIVERSE,
            values.get("operator_confirms_target_universe"),
        ),
        _check(
            "operator_confirms_target_count",
            len(TARGET_UNIVERSE),
            values.get("operator_confirms_target_count"),
        ),
        _check(
            "operator_confirms_dataset_name",
            APPROVED_REGISTRY_METADATA["dataset_name"],
            values.get("operator_confirms_dataset_name"),
        ),
        _check(
            "operator_confirms_total_canonical_record_count_11946",
            11946,
            values.get("operator_confirms_total_canonical_record_count"),
        ),
        *[
            _check(f"attestation_{field}", expected, values.get(field))
            for field, expected in DIGEST_CONFIRMATION_EXPECTATIONS.items()
        ],
        *[
            _check(f"attestation_{field}", True, values.get(field))
            for field in BOOLEAN_CONFIRMATION_FIELDS
        ],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            "operator_attestation must be a JSON object"
        )
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AdditionalPredictiveEvidenceExecutionApprovalError(
                f"{field} must be a non-empty string"
            )
    failed = [check for check in _attestation_checks(attestation) if check["status"] != PASS]
    if failed:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            f"operator attestation failed: {failed[0]['check_id']}"
        )
    return deepcopy(attestation)


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        deepcopy(review_package)
        if review_package is not None
        else candidate_review.build_additional_predictive_evidence_execution_candidate_review_package_v1()
    )
    try:
        validation = candidate_review.validate_additional_predictive_evidence_execution_candidate_review_package_v1(
            source
        )
    except candidate_review.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError as exc:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            f"source execution candidate review package invalid: {exc}"
        ) from exc
    _expect(
        validation[
            "additional_predictive_evidence_execution_candidate_review_package_digest"
        ],
        EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source execution candidate review package digest",
    )
    _expect(validation["blocker_count"], 0, "source execution candidate review blocker count")
    return source


def per_ticker_additional_predictive_evidence_execution_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one approved per-ticker execution entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_additional_predictive_evidence_execution_approval_digest", None)
    return semantic_digest(payload)


def _approved_per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "additional_predictive_evidence_execution_approval_status": (
                APPROVED_FOR_FUTURE_EXECUTION_ONLY
            ),
            "additional_predictive_evidence_execution_authorized": True,
            "additional_predictive_evidence_executed": False,
            "label_generation_authorized": True,
            "label_generation_performed": False,
            "feature_matrix_generation_authorized": True,
            "feature_matrix_generation_performed": False,
            "walk_forward_validation_authorized": True,
            "walk_forward_validation_performed": False,
            "out_of_sample_evaluation_authorized": True,
            "out_of_sample_evaluation_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_additional_predictive_evidence_execution_candidate_review_digest": (
                EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
            "source_additional_predictive_evidence_execution_candidate_digest": (
                EXPECTED_EXECUTION_CANDIDATE_DIGEST
            ),
        }
        entry[
            "per_ticker_additional_predictive_evidence_execution_approval_digest"
        ] = per_ticker_additional_predictive_evidence_execution_approval_digest_v1(entry)
        entries.append(entry)
    return entries


def _approved_label_set() -> list[dict[str, Any]]:
    return [
        {
            "label_family": label,
            "label_generation_authorized": True,
            "label_generation_performed": False,
            "execution_status": AUTHORIZED_NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for label in APPROVED_LABEL_FAMILIES
    ]


def _approved_feature_set() -> list[dict[str, Any]]:
    return [
        {
            "feature_family": feature,
            "feature_matrix_generation_authorized": True,
            "feature_matrix_generation_performed": False,
            "execution_status": AUTHORIZED_NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for feature in APPROVED_FEATURE_FAMILIES
    ]


def _approved_execution_protocol() -> list[dict[str, Any]]:
    return [
        {
            "protocol_item": protocol,
            "authorized": True,
            "performed": False,
            "execution_status": AUTHORIZED_NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for protocol in APPROVED_EXECUTION_PROTOCOL_IDS
    ]


def _approved_metric_families() -> list[dict[str, Any]]:
    return [
        {
            "metric_family": metric,
            "authorized": True,
            "performed": False,
            "execution_status": AUTHORIZED_NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for metric in APPROVED_METRIC_FAMILY_IDS
    ]


def _approved_baselines() -> list[dict[str, Any]]:
    return [
        {
            "baseline": baseline,
            "authorized": True,
            "performed": False,
            "acceptance_evidence_status": NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED,
            "research_only": True,
            "non_actionable": True,
        }
        for baseline in APPROVED_BASELINE_IDS
    ]


def _future_execution_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output,
            "authorized_for_future_generation": True,
            "generated": False,
            "generation_status": AUTHORIZED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output in FUTURE_EXECUTION_OUTPUT_IDS
    ]


def _all_per_ticker_digests_valid(entries: Any) -> bool:
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        return False
    return all(
        isinstance(entry, dict)
        and isinstance(
            entry.get("per_ticker_additional_predictive_evidence_execution_approval_digest"),
            str,
        )
        and len(
            entry["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        )
        == 64
        and entry["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        == per_ticker_additional_predictive_evidence_execution_approval_digest_v1(entry)
        for entry in entries
    )


def _future_outputs_valid(outputs: Any) -> bool:
    return isinstance(outputs, list) and outputs == _future_execution_outputs()


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = approved.get("operator_attestation")
    checklist = [
        _check(
            "execution_candidate_review_digest_matches_expected",
            EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            approved.get("additional_predictive_evidence_execution_candidate_review_package_digest"),
        ),
        _check(
            "execution_candidate_review_has_zero_blockers",
            0,
            approved.get("source_execution_candidate_review_blocker_count"),
        ),
        _check("execution_candidate_digest_bound", EXPECTED_EXECUTION_CANDIDATE_DIGEST, approved.get("additional_predictive_evidence_execution_candidate_digest")),
        _check("chain_candidate_review_digest_bound", EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("additional_predictive_evidence_chain_candidate_review_package_digest")),
        _check("research_registry_approval_digest_bound", EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, approved.get("research_registry_approval_digest")),
        _check("canonical_dataset_freeze_digest_bound", EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST, approved.get("canonical_dataset_freeze_digest")),
        _check("canonical_dataset_generation_digest_bound", EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, approved.get("canonical_dataset_generation_digest")),
        _check("records_digest_bound", EXPECTED_RECORDS_DIGEST, approved.get("records_digest")),
        _check("target_universe_count_12", 12, approved.get("target_universe_count")),
        _check("target_universe_matches_execution_candidate_review_universe", TARGET_UNIVERSE, approved.get("target_universe")),
        *_attestation_checks(attestation if isinstance(attestation, dict) else None),
        _check("approval_scope_additional_predictive_execution_only", ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY, approved.get("approval_scope")),
        _check("additional_predictive_evidence_execution_approved_true", True, approved.get("additional_predictive_evidence_execution_approved")),
        _check("additional_predictive_evidence_execution_authorized_true", True, approved.get("additional_predictive_evidence_execution_authorized")),
        _check("ready_for_additional_predictive_evidence_execution_true", True, approved.get("ready_for_additional_predictive_evidence_execution")),
    ]
    for field in (
        "label_generation_authorized",
        "feature_matrix_generation_authorized",
        "walk_forward_validation_authorized",
        "out_of_sample_evaluation_authorized",
        "baseline_comparison_authorized",
        "signal_quality_metrics_authorized",
        "stability_analysis_authorized",
        "leakage_control_review_authorized",
        "predictive_experiment_rerun_authorized",
    ):
        checklist.append(_check(f"{field}_true", True, approved.get(field)))
    for field in (
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "label_generation_performed",
        "feature_matrix_generation_performed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "baseline_comparison_performed",
        "signal_quality_metrics_performed",
        "stability_analysis_performed",
        "leakage_control_review_performed",
        "predictive_experiment_rerun_performed",
    ):
        checklist.append(_check(f"{field}_false", False, approved.get(field)))
    entries = approved.get("approved_per_ticker_execution_entries")
    checklist.extend(
        [
            _check("per_ticker_execution_approval_entries_12", 12, len(entries) if isinstance(entries, list) else None),
            _check("per_ticker_execution_approval_digests_present", True, _all_per_ticker_digests_valid(entries)),
            _check("approved_label_families_7", _approved_label_set(), approved.get("approved_label_set")),
            _check("approved_feature_families_10", _approved_feature_set(), approved.get("approved_feature_set")),
            _check("approved_execution_protocol_items_9", _approved_execution_protocol(), approved.get("approved_execution_protocol")),
            _check("approved_metric_families_9", _approved_metric_families(), approved.get("approved_metric_families")),
            _check("approved_baselines_6", _approved_baselines(), approved.get("approved_baselines")),
            _check("future_outputs_15_authorized_not_generated", True, _future_outputs_valid(approved.get("future_execution_outputs"))),
            _check("new_strategy_scoring_performed_false", False, approved.get("new_strategy_scoring_performed")),
            _check("trade_recommendations_generated_false", False, approved.get("trade_recommendations_generated")),
            _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, approved.get("predictive_usefulness"), severity=INFO),
            _check("predictive_usefulness_acceptance_candidate_created_false", False, approved.get("predictive_usefulness_acceptance_candidate_created")),
            _check("profitability_not_accepted", NOT_ACCEPTED, approved.get("profitability"), severity=INFO),
            _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
            _check("runtime_use_not_authorized", NOT_AUTHORIZED, approved.get("runtime_use")),
            _check("strategy_use_not_authorized", NOT_AUTHORIZED, approved.get("strategy_use")),
            _check("paper_trading_not_authorized", NOT_AUTHORIZED, approved.get("paper_trading")),
            _check("broker_execution_not_authorized", NOT_AUTHORIZED, approved.get("broker_execution")),
            _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
            _check("provider_requests_made_in_approval_false", False, approved.get("provider_requests_made_in_approval")),
            _check("live_provider_transport_enabled_in_approval_false", False, approved.get("live_provider_transport_enabled_in_approval")),
            _check("market_data_acquisition_performed_in_approval_false", False, approved.get("market_data_acquisition_performed_in_approval")),
            _check("dataset_generation_performed_in_approval_false", False, approved.get("dataset_generation_performed_in_approval")),
            _check("canonical_dataset_regenerated_in_approval_false", False, approved.get("canonical_dataset_regenerated_in_approval")),
            _check("raw_provider_payloads_not_committed", False, approved.get("raw_provider_payloads_committed")),
            _check("api_keys_not_stored_or_printed", False, approved.get("api_keys_stored_or_printed")),
            _check("approval_creates_predictive_usefulness_acceptance_false", False, approved.get("execution_approval_creates_predictive_usefulness_acceptance")),
            _check("approval_creates_profitability_acceptance_false", False, approved.get("execution_approval_creates_profitability_acceptance")),
            _check("approval_creates_runtime_authority_false", False, approved.get("execution_approval_creates_runtime_authority")),
            _check("limitations_recorded", RISK_CONTROLS, approved.get("risk_controls")),
            _check("next_gates_defined", NEXT_GATES, approved.get("next_gates")),
            _check("no_additional_predictive_evidence_execution_artifact_created", False, approved.get("additional_predictive_evidence_execution_artifact_created")),
            _check("no_predictive_usefulness_acceptance_artifact_created", False, approved.get("predictive_usefulness_acceptance_artifact_created")),
            _check("no_profitability_acceptance_created", False, approved.get("profitability_acceptance_created")),
            _check("no_runtime_migration_approval_created", False, approved.get("runtime_migration_approval_created")),
        ]
    )
    return checklist


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item["status"] == PASS)
    failed = total - passed
    blockers = sum(
        1
        for item in checklist
        if item["status"] == FAIL and item["severity"] == BLOCKER
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "additional_predictive_evidence_execution_approved_by_operator": failed == 0,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_authorized": failed == 0,
        "ready_for_additional_predictive_evidence_execution": failed == 0,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _source_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_execution_candidate_review_package_kind": source["artifact_kind"],
        "source_execution_candidate_review_status": source["review_status"],
        "source_execution_candidate_review_checklist_total": source["review_summary"]["total_checks"],
        "source_execution_candidate_review_checklist_passed": source["review_summary"]["passed_checks"],
        "source_execution_candidate_review_checklist_failed": source["review_summary"]["failed_checks"],
        "source_execution_candidate_review_blocker_count": source["review_summary"]["blocker_count"],
        "additional_predictive_evidence_execution_candidate_review_package_digest": source[
            "additional_predictive_evidence_execution_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_execution_candidate_digest": source[
            "additional_predictive_evidence_execution_candidate_digest"
        ],
        "additional_predictive_evidence_chain_candidate_review_package_digest": source[
            "additional_predictive_evidence_chain_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_chain_candidate_digest": source[
            "additional_predictive_evidence_chain_candidate_digest"
        ],
        "research_registry_approval_digest": source["research_registry_approval_digest"],
        "research_registry_candidate_review_package_digest": source[
            "research_registry_candidate_review_package_digest"
        ],
        "research_registry_candidate_digest": source["research_registry_candidate_digest"],
        "canonical_dataset_freeze_digest": source["canonical_dataset_freeze_digest"],
        "canonical_dataset_results_review_package_digest": source[
            "canonical_dataset_results_review_package_digest"
        ],
        "canonical_dataset_generation_digest": source["canonical_dataset_generation_digest"],
        "records_digest": source["records_digest"],
        "acquisition_generation_freeze_digest": source["acquisition_generation_freeze_digest"],
        "corporate_action_authority_approval_digest": source[
            "corporate_action_authority_approval_digest"
        ],
        "identity_authority_freeze_digest": source["identity_authority_freeze_digest"],
        "ticker_universe_selection_approval_digest": source[
            "ticker_universe_selection_approval_digest"
        ],
    }


def additional_predictive_evidence_execution_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for an execution approval artifact."""
    payload = deepcopy(approved_artifact)
    payload.pop("additional_predictive_evidence_execution_approval_digest", None)
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_approved_v1(
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Approve only a future research execution; perform no predictive work."""
    source = _source_review_package(execution_candidate_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "canonical_dataset_regenerated_in_approval": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "research_registry_approved": True,
        "registry_approval_created": True,
        "additional_predictive_evidence_chain_candidate_created": True,
        "additional_predictive_evidence_chain_candidate_review_created": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_review_created": True,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution": True,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": True,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "predictive_experiment_rerun_authorized": True,
        "predictive_experiment_rerun_performed": False,
        "label_generation_authorized": True,
        "label_generation_performed": False,
        "feature_matrix_generation_authorized": True,
        "feature_matrix_generation_performed": False,
        "walk_forward_validation_authorized": True,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_authorized": True,
        "out_of_sample_evaluation_performed": False,
        "baseline_comparison_authorized": True,
        "baseline_comparison_performed": False,
        "signal_quality_metrics_authorized": True,
        "signal_quality_metrics_performed": False,
        "stability_analysis_authorized": True,
        "stability_analysis_performed": False,
        "leakage_control_review_authorized": True,
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
        "additional_predictive_evidence_execution_approved_by_operator": True,
        "execution_approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "execution_approval_authorizes_future_label_generation": True,
        "execution_approval_authorizes_future_feature_matrix_generation": True,
        "execution_approval_authorizes_future_walk_forward_validation": True,
        "execution_approval_authorizes_future_out_of_sample_evaluation": True,
        "execution_approval_authorizes_future_baseline_comparison": True,
        "execution_approval_authorizes_future_signal_quality_metrics": True,
        "execution_approval_authorizes_future_stability_analysis": True,
        "execution_approval_authorizes_future_leakage_control_review": True,
        "execution_approval_authorizes_future_predictive_experiment_rerun": True,
        "execution_approval_performs_execution": False,
        "execution_approval_creates_results": False,
        "execution_approval_creates_predictive_usefulness_acceptance": False,
        "execution_approval_creates_profitability_acceptance": False,
        "execution_approval_creates_runtime_authority": False,
        "execution_approval_creates_strategy_authority": False,
        "execution_approval_creates_trade_recommendations": False,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "registry_approved_dataset_metadata": deepcopy(APPROVED_REGISTRY_METADATA),
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "approved_per_ticker_execution_entries": _approved_per_ticker_entries(),
        "approved_label_set": _approved_label_set(),
        "approved_feature_set": _approved_feature_set(),
        "approved_execution_protocol": _approved_execution_protocol(),
        "approved_split_profile": deepcopy(APPROVED_SPLIT_PROFILE),
        "approved_metric_families": _approved_metric_families(),
        "approved_baselines": _approved_baselines(),
        "future_execution_outputs": _future_execution_outputs(),
        "future_execution_chain": list(FUTURE_EXECUTION_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "additional_predictive_evidence_execution_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_attestation": attestation,
        **_source_evidence(source),
    }
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["additional_predictive_evidence_execution_approval_digest"] = (
        additional_predictive_evidence_execution_approval_digest_v1(approved)
    )
    validate_additional_predictive_evidence_execution_approved_v1(approved)
    return approved


FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "LABEL_GENERATION_EXECUTED",
    "FEATURE_MATRIX_GENERATION_EXECUTED",
    "WALK_FORWARD_VALIDATION_EXECUTED",
    "OUT_OF_SAMPLE_EVALUATION_EXECUTED",
    "BASELINE_COMPARISON_EXECUTED",
    "SIGNAL_QUALITY_METRICS_EXECUTED",
    "STABILITY_ANALYSIS_EXECUTED",
    "LEAKAGE_CONTROL_REVIEW_EXECUTED",
    "PREDICTIVE_EXPERIMENT_RERUN_EXECUTED",
    "NEW_STRATEGY_SCORING_EXECUTED",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}
FORBIDDEN_TRUE_FIELDS = {
    "additional_predictive_evidence_executed",
    "additional_predictive_evidence_results_created",
    "label_generation_performed",
    "feature_matrix_generation_performed",
    "walk_forward_validation_performed",
    "out_of_sample_evaluation_performed",
    "baseline_comparison_performed",
    "signal_quality_metrics_performed",
    "stability_analysis_performed",
    "leakage_control_review_performed",
    "predictive_experiment_rerun_performed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_candidate_created",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "provider_requests_made_in_approval",
    "live_provider_transport_enabled_in_approval",
    "market_data_acquisition_performed_in_approval",
    "dataset_generation_performed_in_approval",
    "canonical_dataset_regenerated_in_approval",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "performed",
    "generated",
}


def _reject_forbidden_values(value: Any, *, path: str = "approved_artifact") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            current_path = f"{path}.{key}"
            if key in FORBIDDEN_TRUE_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionApprovalError(
                    f"{current_path} must be false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionApprovalError(
                    f"{current_path} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionApprovalError(
                    f"{current_path} must not be accepted"
                )
            _reject_forbidden_values(item, path=current_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _validate_per_ticker_entries(entries: Any) -> None:
    expected = _approved_per_ticker_entries()
    _expect(entries, expected, "approved_per_ticker_execution_entries")
    _expect_true(_all_per_ticker_digests_valid(entries), "per-ticker approval digests")


def validate_additional_predictive_evidence_execution_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the artifact authorizes future execution only."""
    if not isinstance(approved_artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            "approved artifact must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    expected_values = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "canonical_dataset_freeze_scope": "CANONICAL_DATASET_FREEZE_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "execution_approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "registry_approved_dataset_metadata": APPROVED_REGISTRY_METADATA,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "approved_label_set": _approved_label_set(),
        "approved_feature_set": _approved_feature_set(),
        "approved_execution_protocol": _approved_execution_protocol(),
        "approved_split_profile": APPROVED_SPLIT_PROFILE,
        "approved_metric_families": _approved_metric_families(),
        "approved_baselines": _approved_baselines(),
        "future_execution_outputs": _future_execution_outputs(),
        "future_execution_chain": FUTURE_EXECUTION_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "source_execution_candidate_review_package_kind": candidate_review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE,
        "source_execution_candidate_review_status": candidate_review.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_execution_candidate_review_checklist_total": EXPECTED_REVIEW_CHECKLIST_TOTAL,
        "source_execution_candidate_review_checklist_passed": EXPECTED_REVIEW_CHECKLIST_PASSED,
        "source_execution_candidate_review_checklist_failed": EXPECTED_REVIEW_CHECKLIST_FAILED,
        "source_execution_candidate_review_blocker_count": EXPECTED_REVIEW_BLOCKER_COUNT,
        "additional_predictive_evidence_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "additional_predictive_evidence_chain_candidate_review_package_digest": EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_chain_candidate_digest": EXPECTED_CHAIN_CANDIDATE_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }
    for field, expected in expected_values.items():
        _expect(approved_artifact.get(field), expected, field)
    for field in (
        "created_offline",
        "research_registry_approved",
        "registry_approval_created",
        "additional_predictive_evidence_chain_candidate_created",
        "additional_predictive_evidence_chain_candidate_review_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_review_created",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "ready_for_additional_predictive_evidence_execution",
        "canonical_dataset_generated",
        "canonical_dataset_frozen",
        "predictive_experiment_rerun_authorized",
        "label_generation_authorized",
        "feature_matrix_generation_authorized",
        "walk_forward_validation_authorized",
        "out_of_sample_evaluation_authorized",
        "baseline_comparison_authorized",
        "signal_quality_metrics_authorized",
        "stability_analysis_authorized",
        "leakage_control_review_authorized",
        "research_only",
        "additional_predictive_evidence_execution_approved_by_operator",
        "execution_approval_authorizes_future_label_generation",
        "execution_approval_authorizes_future_feature_matrix_generation",
        "execution_approval_authorizes_future_walk_forward_validation",
        "execution_approval_authorizes_future_out_of_sample_evaluation",
        "execution_approval_authorizes_future_baseline_comparison",
        "execution_approval_authorizes_future_signal_quality_metrics",
        "execution_approval_authorizes_future_stability_analysis",
        "execution_approval_authorizes_future_leakage_control_review",
        "execution_approval_authorizes_future_predictive_experiment_rerun",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval",
        "canonical_dataset_regenerated_in_approval",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "predictive_experiment_rerun_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "baseline_comparison_performed",
        "signal_quality_metrics_performed",
        "stability_analysis_performed",
        "leakage_control_review_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "execution_approval_performs_execution",
        "execution_approval_creates_results",
        "execution_approval_creates_predictive_usefulness_acceptance",
        "execution_approval_creates_profitability_acceptance",
        "execution_approval_creates_runtime_authority",
        "execution_approval_creates_strategy_authority",
        "execution_approval_creates_trade_recommendations",
        "additional_predictive_evidence_execution_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    _validate_per_ticker_entries(approved_artifact.get("approved_per_ticker_execution_entries"))
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    digest = approved_artifact.get(
        "additional_predictive_evidence_execution_approval_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            "additional_predictive_evidence_execution_approval_digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_approval_digest_v1(approved_artifact),
        "additional_predictive_evidence_execution_approval_digest",
    )
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "additional_predictive_evidence_execution_approval_digest": digest,
        "source_execution_candidate_review_package_digest": EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_execution_candidate_digest": EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "additional_predictive_evidence_execution_authorized": True,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_additional_predictive_evidence_execution_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized execution approval status document."""
    validation = validate_additional_predictive_evidence_execution_approved_v1(
        approved_artifact
    )
    attestation = approved_artifact["operator_attestation"]
    metadata = approved_artifact["registry_approved_dataset_metadata"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Approval Status",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution Approval Ceremony v1.",
        "",
        "## Approved Additional Predictive Evidence Execution",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['additional_predictive_evidence_execution_approval_digest']}`",
        f"- Execution authorized/performed: `{approved_artifact['additional_predictive_evidence_execution_authorized']}` / `{approved_artifact['additional_predictive_evidence_executed']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Execution Candidate Review",
        f"- Review digest: `{approved_artifact['additional_predictive_evidence_execution_candidate_review_package_digest']}`",
        f"- Execution candidate digest: `{approved_artifact['additional_predictive_evidence_execution_candidate_digest']}`",
        f"- Review blockers: `{approved_artifact['source_execution_candidate_review_blocker_count']}`",
        "",
        "## Registry-Approved Dataset Metadata",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in metadata.items())
    lines.extend(["", "## Target Universe", f"- `{' '.join(approved_artifact['target_universe'])}`"])
    lines.extend(["", "## Approved Per-Ticker Execution Summary"])
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['historical_record_count']}` records; `{entry['additional_predictive_evidence_execution_approval_status']}`"
        for entry in approved_artifact["approved_per_ticker_execution_entries"]
    )
    for heading, key, id_field in (
        ("Approved Label Set", "approved_label_set", "label_family"),
        ("Approved Feature Set", "approved_feature_set", "feature_family"),
        ("Approved Execution Protocol", "approved_execution_protocol", "protocol_item"),
        ("Approved Metrics and Baselines", "approved_metric_families", "metric_family"),
    ):
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_field]}`: `{AUTHORIZED_NOT_EXECUTED}`" for item in approved_artifact[key])
    lines.extend(f"- Baseline `{item['baseline']}`: `{AUTHORIZED_NOT_EXECUTED}`" for item in approved_artifact["approved_baselines"])
    lines.extend(["", "## Future Execution Outputs"])
    lines.extend(f"- `{item['output_id']}`: `{item['generation_status']}`" for item in approved_artifact["future_execution_outputs"])
    lines.extend(
        [
            "",
            "## Execution Boundary",
            "- This approval authorizes a future research-only execution and performs no execution.",
            f"- Results created: `{approved_artifact['additional_predictive_evidence_results_created']}`",
            "",
            "## Predictive Usefulness Boundary",
            f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
            "",
            "## Profitability Boundary",
            f"- profitability: `{approved_artifact['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_use: `{approved_artifact['runtime_use']}`",
            f"- strategy_use: `{approved_artifact['strategy_use']}`",
            f"- paper_trading: `{approved_artifact['paper_trading']}`",
            f"- broker_execution: `{approved_artifact['broker_execution']}`",
            "",
            "## Approval Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(
        f"{index}. {task}"
        for index, task in enumerate(approved_artifact["future_execution_chain"], start=1)
    )
    lines.extend(["", "## Guardrails"])
    lines.extend(f"- `{control}`" for control in approved_artifact["risk_controls"])
    lines.extend(
        [
            "- No provider request, market-data acquisition, dataset regeneration, label/feature generation, experiment execution, strategy scoring, or runtime activation occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_approved_v1(
    output_dir: str | Path,
    *,
    execution_candidate_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write canonical approval JSON once; existing output fails closed."""
    approved = build_additional_predictive_evidence_execution_approved_v1(
        execution_candidate_review_package=execution_candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_additional_predictive_evidence_execution_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "additional_predictive_evidence_execution_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            "approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise AdditionalPredictiveEvidenceExecutionApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
