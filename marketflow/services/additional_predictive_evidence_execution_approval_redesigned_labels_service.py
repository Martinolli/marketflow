"""Offline approval for future predictive evidence using redesigned labels."""

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
    additional_predictive_evidence_execution_candidate_redesigned_labels_operator_review_service as review_service,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "additional_predictive_evidence_execution_approval_using_redesigned_labels_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS = (
    "APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS"
)
OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1 = (
    "additional_predictive_evidence_execution_approval_using_redesigned_labels_operator_attestation_v1"
)
REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE = (
    "APPROVE ADDITIONAL PREDICTIVE EVIDENCE EXECUTION USING REDESIGNED LABELS "
    "MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY"
)

DEFAULT_BRANCH = (
    "feature/additional-predictive-evidence-execution-approval-redesigned-labels-v1"
)
DEFAULT_BASE_COMMIT = "2451c47579a59339ba84e74fc4c3fd5d9112e316"

EXPECTED_CANDIDATE_REVIEW_DIGEST = (
    "dc4ae33cd0f40d84de33ce7e195d35696443fa5cd5dcb52dee4ce0c649ac06ec"
)
EXPECTED_CANDIDATE_DIGEST = (
    "f11550ab63f21f2f08b896296324e0f0b1cb99a27ae186cfc347028e5ddf9cd5"
)
EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST = (
    "e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3"
)
EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST = (
    "d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f"
)
EXPECTED_FEATURE_VALUES_DIGEST = (
    "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
)
EXPECTED_FEATURE_GENERATION_APPROVAL_DIGEST = (
    "595bb9685936979810cfe6e3a814ea9ef38e0e3d89b804426a2d540ec77471c1"
)
EXPECTED_FEATURE_GENERATION_CANDIDATE_REVIEW_DIGEST = (
    "d16cbdf42e44cbd95a5fa59fbb3dca5c00b6a888e8583f440369fa9a828d3a15"
)
EXPECTED_FEATURE_GENERATION_CANDIDATE_DIGEST = (
    "21b3bc905f3d553f4ec74bd70f758bbbc9be02ae906af1732c3b4fb5aaf12d1e"
)
EXPECTED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_DIGEST = (
    "6f4c1ce989e76e2b2ee835056e146f362b6d7c70b44bb6fc864f3f125c9dc54d"
)
EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST = (
    "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
)
EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST = (
    "0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506"
)
EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST = (
    "280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)
EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST = (
    "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
)

TARGET_UNIVERSE = [
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "JPM",
    "XOM",
    "JNJ",
    "WMT",
    "CAT",
    "LMT",
]
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE
}

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
AUTHORIZED_NOT_GENERATED = "AUTHORIZED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
APPROVED_FOR_FUTURE_PREDICTIVE_EVIDENCE_EXECUTION_ONLY = (
    "APPROVED_FOR_FUTURE_PREDICTIVE_EVIDENCE_EXECUTION_ONLY"
)
NOT_REGENERATED = "NOT_REGENERATED"

EXECUTION_OBJECTIVE = (
    "EXECUTE_ADDITIONAL_PREDICTIVE_EVIDENCE_USING_REDESIGNED_LABELS_AND_FEATURES"
)
EXECUTION_MODE = AUTHORIZED_NOT_EXECUTED
EXECUTION_AUTHORITY_STATUS = (
    "AUTHORIZED_FOR_FUTURE_RESEARCH_ONLY_PREDICTIVE_EVIDENCE_EXECUTION"
)

SOURCE_INPUT_IDS = list(review_service.candidate_service.SOURCE_INPUT_IDS)
APPROVED_EXECUTION_ACTIVITY_IDS = list(
    review_service.candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
)
MODEL_BASELINE_FAMILY_IDS = list(
    review_service.candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS
)
METRIC_FAMILY_IDS = list(review_service.candidate_service.PLANNED_METRIC_FAMILY_IDS)
FUTURE_OUTPUT_IDS = [
    "additional_predictive_evidence_execution_manifest",
    "source_feature_label_binding_manifest",
    "feature_label_matrix",
    "chronological_split_profile",
    "walk_forward_results",
    "oos_holdout_results",
    "baseline_model_comparison_results",
    "metric_family_results",
    "calibration_stability_report",
    "leakage_quality_control_report",
    "per_ticker_cross_sectional_review",
    "operator_review_summary",
    "digest_manifest",
]

APPROVED_SPLITS = {
    "training_window": "2022-01-01 through 2023-12-31",
    "validation_window": "2024-01-01 through 2024-12-31",
    "oos_window": "2025-01-01 through 2025-12-31",
    "shuffle_allowed": False,
    "chronological_order_required": True,
    "embargo_policy": "APPROVED_FOR_FUTURE_EXECUTION_REVIEW",
}
APPROVED_SOURCE_REDESIGNED_LABEL_PROFILE = {
    "label_value_row_count": 143352,
    "available_label_value_count": 142200,
    "unavailable_label_value_count": 1152,
    "label_family_count": 10,
    "threshold_strategy_count": 7,
    "horizon_strategy_count": 5,
    "redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
}
APPROVED_SOURCE_FEATURE_PROFILE = {
    "feature_output_count": 12,
    "feature_output_status": "REVIEWED_AND_VERIFIED",
    "feature_family_count": 10,
    "feature_group_count": 17,
    "feature_schema_field_count": 16,
    "feature_value_row_count": 203082,
    "available_feature_value_count": 190848,
    "unavailable_feature_value_count": 12234,
    "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
}

NEXT_CHAIN = [
    "Additional Predictive Evidence Execution Using Redesigned Labels v1.",
    "Additional Predictive Evidence Results Review Using Redesigned Labels v1.",
    "Predictive Usefulness Reassessment Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "additional_predictive_evidence_execution_using_redesigned_labels",
    "additional_predictive_evidence_results_review_using_redesigned_labels",
    "predictive_usefulness_reassessment_using_redesigned_evidence",
    "predictive_usefulness_acceptance_readiness_using_redesigned_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "approval_does_not_execute_predictive_evidence_now",
    "approval_does_not_train_models_now",
    "approval_does_not_compute_metrics_now",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "preserve_meta_record_limitation",
    "no_runtime_without_separate_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

DIGEST_CONFIRMATIONS = {
    "operator_confirms_additional_predictive_evidence_execution_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "operator_confirms_additional_predictive_evidence_execution_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
    "operator_confirms_feature_generation_results_review_digest": EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST,
    "operator_confirms_feature_generation_execution_digest": EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST,
    "operator_confirms_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
    "operator_confirms_redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
    "operator_confirms_research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "operator_confirms_records_digest": EXPECTED_RECORDS_DIGEST,
}
VALUE_CONFIRMATIONS = {
    "operator_confirms_target_universe": TARGET_UNIVERSE,
    "operator_confirms_target_count": 12,
    "operator_confirms_meta_record_count": 913,
    "operator_confirms_non_meta_record_count": 1003,
}
BOOLEAN_CONFIRMATIONS = [
    "operator_confirms_source_feature_profile",
    "operator_confirms_source_label_profile",
    "operator_confirms_predictive_evidence_execution_approval_scope_only",
    "operator_confirms_predictive_evidence_execution_authorized",
    "operator_confirms_ready_for_predictive_evidence_execution",
    "operator_confirms_no_predictive_evidence_execution_performed",
    "operator_confirms_no_predictive_evidence_results_created",
    "operator_confirms_no_metric_recomputation_performed",
    "operator_confirms_no_model_training_performed",
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


class AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(ValueError):
    """Raised when approval evidence or authority boundaries are invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
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


def build_additional_predictive_evidence_execution_approval_using_redesigned_labels_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_additional_predictive_evidence_execution_candidate_review_digest: str,
    operator_confirms_additional_predictive_evidence_execution_candidate_digest: str,
    operator_confirms_feature_generation_results_review_digest: str,
    operator_confirms_feature_generation_execution_digest: str,
    operator_confirms_feature_values_digest: str,
    operator_confirms_redesigned_label_values_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_source_feature_profile: bool,
    operator_confirms_source_label_profile: bool,
    operator_confirms_predictive_evidence_execution_approval_scope_only: bool,
    operator_confirms_predictive_evidence_execution_authorized: bool,
    operator_confirms_ready_for_predictive_evidence_execution: bool,
    operator_confirms_no_predictive_evidence_execution_performed: bool,
    operator_confirms_no_predictive_evidence_results_created: bool,
    operator_confirms_no_metric_recomputation_performed: bool,
    operator_confirms_no_model_training_performed: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS,
) -> dict[str, Any]:
    """Build a complete, non-secret operator attestation object."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1
    }


def _attestation_checks(attestation: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    values = attestation if isinstance(attestation, Mapping) else {}
    checks = [
        _check(
            "operator_decision_matches",
            OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS,
            values.get("operator_decision"),
        ),
        _check(
            "operator_attestation_phrase_matches",
            REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
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


def _validated_attestation(attestation: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, Mapping):
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            "operator_attestation must be a JSON object"
        )
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS,
        "operator_attestation_phrase": REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1,
        **DIGEST_CONFIRMATIONS,
        **VALUE_CONFIRMATIONS,
    }
    for field, expected_value in expected.items():
        _expect(attestation.get(field), expected_value, field)
    for field in BOOLEAN_CONFIRMATIONS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
                f"{field} required"
            )
    return deepcopy(dict(attestation))


def _source_review(candidate_review_package: dict[str, Any] | None) -> dict[str, Any]:
    source = (
        review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1()
        if candidate_review_package is None
        else deepcopy(candidate_review_package)
    )
    try:
        review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
            source
        )
    except review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError as exc:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            "source candidate review package is invalid"
        ) from exc
    _expect(
        source.get(
            "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"
        ),
        EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate review digest",
    )
    _expect(
        source.get(
            "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"
        ),
        EXPECTED_CANDIDATE_DIGEST,
        "candidate digest",
    )
    _expect(source.get("review_summary", {}).get("total_checks"), 56, "review total")
    _expect(source.get("review_summary", {}).get("passed_checks"), 56, "review passed")
    _expect(source.get("review_summary", {}).get("failed_checks"), 0, "review failed")
    _expect(source.get("review_summary", {}).get("blocker_count"), 0, "review blockers")
    return source


def _approved_source_inputs() -> list[dict[str, Any]]:
    return [
        {
            "source_input": source_input,
            "approval_status": APPROVED_FOR_FUTURE_PREDICTIVE_EVIDENCE_EXECUTION_ONLY,
            "generation_status": NOT_REGENERATED,
            "research_only": True,
            "non_actionable": True,
        }
        for source_input in SOURCE_INPUT_IDS
    ]


def _approved_execution_activities() -> list[dict[str, Any]]:
    return [
        {
            "activity_id": activity_id,
            "authorization_status": AUTHORIZED_NOT_EXECUTED,
            "execution_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for activity_id in APPROVED_EXECUTION_ACTIVITY_IDS
    ]


def _approved_feature_label_matrix() -> dict[str, Any]:
    return {
        "matrix_status": AUTHORIZED_NOT_GENERATED,
        "feature_values_digest_bound": True,
        "redesigned_label_values_digest_bound": True,
        "records_digest_bound": True,
        "feature_row_count": 203082,
        "label_row_count": 143352,
        "target_universe_count": 12,
        "feature_label_join_strategy": "TICKER_DATE_HORIZON_AND_LABEL_FAMILY_ALIGNMENT_APPROVED_FOR_FUTURE_EXECUTION",
        "join_execution_performed": False,
        "matrix_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _approved_model_baseline_families() -> list[dict[str, Any]]:
    return [
        {
            "model_or_baseline_family": family,
            "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_EVALUATION_ONLY",
            "model_or_baseline_status": "AUTHORIZED_NOT_EVALUATED",
            "training_performed": False,
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family in MODEL_BASELINE_FAMILY_IDS
    ]


def _approved_metric_families() -> list[dict[str, Any]]:
    return [
        {
            "metric_family": family,
            "approval_status": "APPROVED_FOR_FUTURE_RESEARCH_METRIC_COMPUTATION_ONLY",
            "metric_status": "AUTHORIZED_NOT_COMPUTED",
            "metric_computation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for family in METRIC_FAMILY_IDS
    ]


def _approved_future_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "output_status": AUTHORIZED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
        }
        for output_id in FUTURE_OUTPUT_IDS
    ]


def per_ticker_additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker approval entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_approval_digest", None
    )
    return semantic_digest(payload)


def _per_ticker_approval_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    source_by_ticker = {
        row["ticker"]: row for row in source.get("per_ticker_review_entries", [])
    }
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        row = source_by_ticker[ticker]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "additional_predictive_evidence_execution_candidate_status": "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT",
            "additional_predictive_evidence_execution_approval_status": "APPROVED_FOR_FUTURE_RESEARCH_EXECUTION_ONLY",
            "feature_values_created": True,
            "predictive_evidence_execution_authorized": True,
            "predictive_evidence_execution_performed": False,
            "metric_recomputation_performed": False,
            "model_training_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_additional_predictive_evidence_execution_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "source_additional_predictive_evidence_execution_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        }
        _expect(
            row.get("historical_record_count"),
            EXPECTED_RECORD_COUNTS[ticker],
            f"{ticker} source record count",
        )
        if ticker == "META":
            entry["planning_note"] = (
                "PRESERVE_META_LIMITATION_IN_PREDICTIVE_EVIDENCE_APPROVAL"
            )
        entry[
            "per_ticker_additional_predictive_evidence_execution_approval_digest"
        ] = per_ticker_additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


FALSE_BOUNDARY_FIELDS = [
    "provider_requests_made",
    "live_provider_transport_enabled",
    "market_data_acquisition_performed",
    "dataset_generation_performed",
    "canonical_dataset_regenerated",
    "redesigned_label_regeneration_performed",
    "feature_regeneration_performed",
    "additional_predictive_evidence_executed",
    "predictive_evidence_results_created",
    "metric_recomputation_performed",
    "model_training_performed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_artifact_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "profitability_acceptance_created",
    "runtime_migration_approved",
    "runtime_migration_active",
    "runtime_migration_approval_created",
    "automatic_stitching",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "additional_predictive_evidence_execution_created",
]


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(entry, dict)
        and entry.get(
            "per_ticker_additional_predictive_evidence_execution_approval_digest"
        )
        == per_ticker_additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
            entry
        )
        for entry in entries
    )


def _approval_checklist(approval: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = approval.get("operator_attestation", {})
    digest_confirmations_valid = all(
        attestation.get(field) == expected
        for field, expected in DIGEST_CONFIRMATIONS.items()
    )
    expected_fields: dict[str, tuple[Any, Any]] = {
        "candidate_review_digest_bound": (EXPECTED_CANDIDATE_REVIEW_DIGEST, approval.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest")),
        "candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, approval.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest")),
        "feature_generation_results_review_digest_bound": (EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST, approval.get("feature_generation_results_review_using_redesigned_labels_digest")),
        "feature_generation_execution_digest_bound": (EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST, approval.get("feature_generation_execution_using_redesigned_labels_digest")),
        "feature_values_digest_bound": (EXPECTED_FEATURE_VALUES_DIGEST, approval.get("feature_values_digest")),
        "redesigned_label_values_digest_bound": (EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, approval.get("redesigned_label_values_digest")),
        "research_registry_digest_bound": (EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST, approval.get("research_registry_approval_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, approval.get("records_digest")),
        "target_universe_12_preserved": (12, approval.get("target_universe_count")),
        "target_universe_matches_review_universe": (TARGET_UNIVERSE, approval.get("target_universe")),
        "records_digest_preserved": (EXPECTED_RECORDS_DIGEST, approval.get("records_digest")),
        "label_values_digest_preserved": (EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, approval.get("redesigned_label_values_digest")),
        "feature_values_digest_preserved": (EXPECTED_FEATURE_VALUES_DIGEST, approval.get("feature_values_digest")),
        "meta_913_preserved": (913, approval.get("meta_record_count")),
        "operator_decision_matches": (OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "operator_confirms_all_required_digests": (True, digest_confirmations_valid),
        "operator_confirms_source_feature_profile": (True, attestation.get("operator_confirms_source_feature_profile")),
        "operator_confirms_source_label_profile": (True, attestation.get("operator_confirms_source_label_profile")),
        "approval_scope_predictive_evidence_execution_only": (ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY, approval.get("approval_scope")),
        "additional_predictive_evidence_execution_approved_true": (True, approval.get("additional_predictive_evidence_execution_approved")),
        "additional_predictive_evidence_execution_approval_created_true": (True, approval.get("additional_predictive_evidence_execution_approval_created")),
        "additional_predictive_evidence_execution_authorized_true": (True, approval.get("additional_predictive_evidence_execution_authorized")),
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels_true": (True, approval.get("ready_for_additional_predictive_evidence_execution_using_redesigned_labels")),
        "predictive_evidence_execution_performed_false": (False, approval.get("additional_predictive_evidence_executed")),
        "predictive_evidence_results_created_false": (False, approval.get("predictive_evidence_results_created")),
        "metric_recomputation_false": (False, approval.get("metric_recomputation_performed")),
        "model_training_false": (False, approval.get("model_training_performed")),
        "approved_source_inputs_12": (12, len(approval.get("approved_source_inputs", []))),
        "approved_execution_activities_13": (13, len(approval.get("approved_execution_activities", []))),
        "approved_feature_label_matrix": (_approved_feature_label_matrix(), approval.get("approved_feature_label_matrix")),
        "approved_splits": (APPROVED_SPLITS, approval.get("approved_splits")),
        "approved_model_baseline_families_9": (9, len(approval.get("approved_model_baseline_families", []))),
        "approved_metric_families_10": (10, len(approval.get("approved_metric_families", []))),
        "approved_future_outputs": (_approved_future_outputs(), approval.get("approved_future_outputs")),
        "per_ticker_approval_entries_12": (12, len(approval.get("per_ticker_approval_entries", []))),
        "per_ticker_approval_digests_present": (True, _per_ticker_digests_valid(approval.get("per_ticker_approval_entries"))),
        "next_chain_defined": (NEXT_CHAIN, approval.get("next_chain")),
        "next_gates_defined": (NEXT_GATES, approval.get("next_gates")),
        "risk_controls_defined": (RISK_CONTROLS, approval.get("risk_controls")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, approval.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, approval.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, approval.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, approval.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, approval.get("paper_trading")),
        "broker_not_authorized": (NOT_AUTHORIZED, approval.get("broker_execution")),
        "trade_recommendations_false": (False, approval.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, approval.get("provider_requests_made")),
        "market_data_acquisition_false": (False, approval.get("market_data_acquisition_performed")),
        "dataset_regeneration_false": (False, approval.get("dataset_generation_performed")),
        "redesigned_label_regeneration_false": (False, approval.get("redesigned_label_regeneration_performed")),
        "feature_regeneration_false": (False, approval.get("feature_regeneration_performed")),
        "raw_provider_payloads_not_committed": (False, approval.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, approval.get("api_keys_stored_or_printed")),
        "no_predictive_evidence_execution_created": (False, approval.get("additional_predictive_evidence_execution_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, approval.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, approval.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, approval.get("runtime_migration_approval_created")),
        "no_tracked_marketflow_files": (True, approval.get("no_tracked_marketflow_files")),
    }
    return [
        _check(check_id, expected, actual)
        for check_id, (expected, actual) in expected_fields.items()
    ]


def additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
    approval: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the complete approval."""
    payload = deepcopy(approval)
    payload.pop(
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Authorize a future research-only execution without performing it."""
    source = _source_review(candidate_review_package)
    attestation = _validated_attestation(operator_attestation)
    approval: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "operator_attestation": attestation,
        "source_candidate_review_kind": source["artifact_kind"],
        "source_candidate_review_status": source["review_status"],
        "source_candidate_review_checklist_total": source["review_summary"]["total_checks"],
        "source_candidate_review_checklist_passed": source["review_summary"]["passed_checks"],
        "source_candidate_review_checklist_failed": source["review_summary"]["failed_checks"],
        "source_candidate_review_blocker_count": source["review_summary"]["blocker_count"],
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_APPROVAL_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": EXPECTED_FEATURE_GENERATION_CANDIDATE_REVIEW_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "approved_source_redesigned_label_profile": deepcopy(
            APPROVED_SOURCE_REDESIGNED_LABEL_PROFILE
        ),
        "approved_source_feature_profile": deepcopy(APPROVED_SOURCE_FEATURE_PROFILE),
        "feature_generation_approved": True,
        "feature_generation_authorized": True,
        "redesigned_feature_generation_authorized": True,
        "feature_generation_performed": True,
        "redesigned_feature_generation_performed": True,
        "feature_values_created": True,
        "feature_generation_results_created": True,
        "feature_generation_results_review_created": True,
        "feature_generation_results_review_ready": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": True,
        "additional_predictive_evidence_execution_candidate_created": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_created": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created": True,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_approval_created": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "additional_predictive_evidence_execution_objective": EXECUTION_OBJECTIVE,
        "additional_predictive_evidence_execution_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
        "additional_predictive_evidence_execution_authority_status": EXECUTION_AUTHORITY_STATUS,
        "approved_source_inputs": _approved_source_inputs(),
        "approved_execution_activities": _approved_execution_activities(),
        "approved_feature_label_matrix": _approved_feature_label_matrix(),
        "approved_splits": deepcopy(APPROVED_SPLITS),
        "approved_model_baseline_families": _approved_model_baseline_families(),
        "approved_metric_families": _approved_metric_families(),
        "approved_future_outputs": _approved_future_outputs(),
        "per_ticker_approval_entries": _per_ticker_approval_entries(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        **{field: False for field in FALSE_BOUNDARY_FIELDS},
    }
    checklist = _approval_checklist(approval)
    failed = [item for item in checklist if item["status"] == FAIL]
    approval["approval_checklist"] = checklist
    approval["approval_summary"] = {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(
            1 for item in failed if item.get("severity") == BLOCKER
        ),
        "additional_predictive_evidence_execution_approved_by_operator": True,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "predictive_evidence_execution_performed": False,
        "predictive_evidence_results_created": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }
    approval[
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"
    ] = additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
        approval
    )
    validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
        approval
    )
    return approval


FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden(value: Any, path: str = "approval") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in FALSE_BOUNDARY_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
                    f"{child} must be false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
                    f"{child} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
                    f"{child} must not be accepted"
                )
            _reject_forbidden(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden(item, f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
    approval: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is approval-only and not executed."""
    if not isinstance(approval, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            "approval must be a JSON object"
        )
    _reject_forbidden(approval)
    expected = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1,
        "approval_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_APPROVAL_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": EXPECTED_FEATURE_GENERATION_CANDIDATE_REVIEW_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_digest": EXPECTED_FEATURE_GENERATION_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "approved_source_redesigned_label_profile": APPROVED_SOURCE_REDESIGNED_LABEL_PROFILE,
        "approved_source_feature_profile": APPROVED_SOURCE_FEATURE_PROFILE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "additional_predictive_evidence_execution_objective": EXECUTION_OBJECTIVE,
        "additional_predictive_evidence_execution_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_mode": EXECUTION_MODE,
        "additional_predictive_evidence_execution_authority_status": EXECUTION_AUTHORITY_STATUS,
        "approved_source_inputs": _approved_source_inputs(),
        "approved_execution_activities": _approved_execution_activities(),
        "approved_feature_label_matrix": _approved_feature_label_matrix(),
        "approved_splits": APPROVED_SPLITS,
        "approved_model_baseline_families": _approved_model_baseline_families(),
        "approved_metric_families": _approved_metric_families(),
        "approved_future_outputs": _approved_future_outputs(),
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(approval.get(field), expected_value, field)
    for field in (
        "created_offline",
        "research_only",
        "operator_review_required",
        "meta_reduced_record_count_preserved",
        "feature_generation_approved",
        "feature_generation_authorized",
        "redesigned_feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "feature_generation_results_created",
        "feature_generation_results_review_created",
        "feature_generation_results_review_ready",
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_created",
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review",
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels",
        "no_tracked_marketflow_files",
    ):
        _expect_true(approval.get(field), field)
    for field in FALSE_BOUNDARY_FIELDS:
        _expect_false(approval.get(field), field)
    _validated_attestation(approval.get("operator_attestation"))
    expected_entries = _per_ticker_approval_entries(
        _source_review(None)
    )
    _expect(approval.get("per_ticker_approval_entries"), expected_entries, "per_ticker_approval_entries")
    _expect_true(
        _per_ticker_digests_valid(approval.get("per_ticker_approval_entries")),
        "per-ticker approval digests",
    )
    checklist = _approval_checklist(approval)
    _expect(approval.get("approval_checklist"), checklist, "approval_checklist")
    summary = approval.get("approval_summary")
    if not isinstance(summary, dict):
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            "approval_summary must be a JSON object"
        )
    _expect(summary.get("total_checks"), len(checklist), "summary total")
    _expect(summary.get("passed_checks"), len(checklist), "summary passed")
    _expect(summary.get("failed_checks"), 0, "summary failed")
    _expect(summary.get("blocker_count"), 0, "summary blockers")
    expected_summary_boundaries = {
        "additional_predictive_evidence_execution_approved_by_operator": True,
        "approval_scope": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "predictive_evidence_execution_performed": False,
        "predictive_evidence_results_created": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }
    for field, expected_value in expected_summary_boundaries.items():
        _expect(summary.get(field), expected_value, f"approval_summary.{field}")
    digest = approval.get(
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"
    )
    if not isinstance(digest, str) or not digest:
        raise AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError(
            "approval digest required"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_approval_using_redesigned_labels_digest_v1(
            approval
        ),
        "approval digest",
    )
    return {
        "valid": True,
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS,
        "artifact_kind": approval["artifact_kind"],
        "approval_scope": approval["approval_scope"],
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": digest,
        "total_checks": len(checklist),
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_additional_predictive_evidence_execution_approved_using_redesigned_labels_markdown_v1(
    approval: dict,
) -> str:
    """Render approval evidence without implying execution or acceptance."""
    validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
        approval
    )
    summary = approval["approval_summary"]
    lines = [
        "# Additional Predictive Evidence Execution Approval Using Redesigned Labels",
        "",
        "## Title",
        "- Additional Predictive Evidence Execution Approval Using Redesigned Labels v1.",
        "",
        "## Additional Predictive Evidence Execution Approval Using Redesigned Labels",
        f"- Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.",
        f"- Digest: `{approval['additional_predictive_evidence_execution_approval_using_redesigned_labels_digest']}`.",
        "",
        "## Operator Attestation",
        f"- Reference/timestamp: `{approval['operator_attestation']['operator_reference']}` / `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`.",
        f"- Decision: `{approval['operator_attestation']['operator_decision']}`.",
        "",
        "## Bound Evidence",
        f"- Candidate review/candidate: `{approval['additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest']}` / `{approval['additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest']}`.",
        f"- Feature review/execution/values: `{approval['feature_generation_results_review_using_redesigned_labels_digest']}` / `{approval['feature_generation_execution_using_redesigned_labels_digest']}` / `{approval['feature_values_digest']}`.",
        f"- Label values/records: `{approval['redesigned_label_values_digest']}` / `{approval['records_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{approval['dataset_name']}` has `{approval['total_canonical_record_count']}` records across the ordered 12-ticker universe; META remains `{approval['meta_record_count']}`.",
        "",
        "## Approved Source Redesigned Label Profile",
        f"- Rows available/unavailable: `{approval['approved_source_redesigned_label_profile']['label_value_row_count']}` / `{approval['approved_source_redesigned_label_profile']['available_label_value_count']}` / `{approval['approved_source_redesigned_label_profile']['unavailable_label_value_count']}`.",
        "",
        "## Approved Source Feature Profile",
        f"- Rows available/unavailable: `{approval['approved_source_feature_profile']['feature_value_row_count']}` / `{approval['approved_source_feature_profile']['available_feature_value_count']}` / `{approval['approved_source_feature_profile']['unavailable_feature_value_count']}`.",
        "",
        "## Approved Source Inputs",
        *[f"- `{row['source_input']}`: `{row['approval_status']}`." for row in approval["approved_source_inputs"]],
        "",
        "## Approved Execution Activities",
        *[f"- `{row['activity_id']}`: `{row['authorization_status']}`." for row in approval["approved_execution_activities"]],
        "",
        "## Approved Feature / Label Matrix",
        f"- `{approval['approved_feature_label_matrix']['matrix_status']}`; matrix created: `{approval['approved_feature_label_matrix']['matrix_created']}`.",
        "",
        "## Approved Splits",
        f"- Training/validation/OOS: `{approval['approved_splits']['training_window']}` / `{approval['approved_splits']['validation_window']}` / `{approval['approved_splits']['oos_window']}`.",
        "",
        "## Approved Model and Baseline Families",
        *[f"- `{row['model_or_baseline_family']}`: `{row['model_or_baseline_status']}`." for row in approval["approved_model_baseline_families"]],
        "",
        "## Approved Metric Families",
        *[f"- `{row['metric_family']}`: `{row['metric_status']}`." for row in approval["approved_metric_families"]],
        "",
        "## Approved Future Outputs",
        *[f"- `{row['output_id']}`: `{row['output_status']}`." for row in approval["approved_future_outputs"]],
        "",
        "## Per-Ticker Approval Entries",
        *[f"- `{row['ticker']}`: `{row['historical_record_count']}` records; `{row['additional_predictive_evidence_execution_approval_status']}`." for row in approval["per_ticker_approval_entries"]],
        "",
        "## Next Chain",
        *[f"{index}. {item}" for index, item in enumerate(approval["next_chain"], 1)],
        "",
        "## Next Gates",
        *[f"- `{item}`" for item in approval["next_gates"]],
        "",
        "## Risk Controls",
        *[f"- `{item}`" for item in approval["risk_controls"]],
        "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "",
        "## Guardrails",
        "- This approval authorizes only future research-only predictive evidence execution.",
        "- It does not execute evidence, compute metrics, train models, create recommendations, accept predictive usefulness or profitability, or authorize runtime, strategy, paper-trading, or broker use.",
        "",
    ]
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict[str, Any]:
    """Write deterministic JSON and Markdown without overwriting evidence."""
    approval = build_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    json_path = root / "additional_predictive_evidence_execution_approval_using_redesigned_labels_v1.json"
    markdown_path = root / "additional_predictive_evidence_execution_approval_using_redesigned_labels_v1.md"
    for path in (json_path, markdown_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite existing artifact: {path}")
    json_bytes = canonical_json_bytes(approval)
    json_path.write_bytes(json_bytes)
    markdown_path.write_text(
        build_additional_predictive_evidence_execution_approved_using_redesigned_labels_markdown_v1(
            approval
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "approval": approval,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "json_sha256": sha256_bytes(json_bytes),
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": approval[
            "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"
        ],
    }
