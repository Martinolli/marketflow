"""Offline operator approval for future acquisition generation freeze input."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_evidence_results_review_service as evidence_review


ARTIFACT_KIND_ACQUISITION_GENERATION_APPROVED = "ACQUISITION_GENERATION_APPROVED"
SCHEMA_VERSION_ACQUISITION_GENERATION_APPROVAL_V1 = "acquisition_generation_approval_v1"
ACQUISITION_GENERATION_APPROVED = "ACQUISITION_GENERATION_APPROVED"
ACQUISITION_GENERATION_APPROVAL_ONLY = "ACQUISITION_GENERATION_APPROVAL_ONLY"
OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION = "APPROVE_ACQUISITION_GENERATION"
OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_APPROVAL_V1 = (
    "acquisition_generation_approval_operator_attestation_v1"
)
REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE ACQUISITION GENERATION MSFT NVDA AMZN GOOGL META TSLA JPM XOM "
    "JNJ WMT CAT LMT ACQUISITION_GENERATION_APPROVAL_ONLY"
)

EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415"
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    evidence_review.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    evidence_review.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    evidence_review.execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST = (
    evidence_review.execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    evidence_review.execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = (
    evidence_review.execution.EXPECTED_COMBINED_READINESS_REVIEW_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    evidence_review.execution.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    evidence_review.execution.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    evidence_review.execution.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    evidence_review.execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(evidence_review.EXPECTED_TARGET_UNIVERSE)
PASS = evidence_review.PASS
FAIL = evidence_review.FAIL
BLOCKER = evidence_review.BLOCKER
NOT_AUTHORIZED = evidence_review.NOT_AUTHORIZED
NOT_ACCEPTED = evidence_review.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = evidence_review.PROFITABILITY_NOT_ACCEPTED
ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY = (
    evidence_review.execution.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY
)
APPROVED_FOR_ACQUISITION_GENERATION_FREEZE_INPUT_ONLY = (
    "APPROVED_FOR_ACQUISITION_GENERATION_FREEZE_INPUT_ONLY"
)

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_failed_provider_response_count_zero",
    "operator_confirms_meta_reduced_bar_count_preserved",
    "operator_confirms_approval_scope_acquisition_generation_only",
    "operator_confirms_new_ticker_acquisition_authorized",
    "operator_confirms_acquisition_generation_authorized",
    "operator_confirms_ready_for_acquisition_generation_freeze",
    "operator_confirms_no_acquisition_generation_execution",
    "operator_confirms_no_acquisition_generation_freeze",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_canonical_dataset_authorization",
    "operator_confirms_no_registry_approval",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

LIMITATIONS = [
    "approval_is_not_execution",
    "approval_is_not_freeze",
    "provider_evidence_is_read_only_snapshot",
    "meta_reduced_bar_count_requires_preservation_in_freeze",
    "dataset_generation_not_authorized",
    "canonical_dataset_not_authorized",
    "registry_approval_not_created",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "operator_approval_required_before_dataset_generation_chain",
]
NEXT_GATES = [
    "acquisition_generation_freeze_ceremony",
    "canonical_dataset_chain_candidate",
    "canonical_dataset_candidate_operator_review",
    "canonical_dataset_freeze",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

REQUIRED_CHECK_IDS = [
    "acquisition_evidence_results_review_digest_matches_expected",
    "acquisition_evidence_results_review_has_zero_blockers",
    "acquisition_provider_evidence_execution_digest_bound",
    "acquisition_provider_evidence_request_approval_digest_bound",
    "acquisition_chain_candidate_review_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_acquisition_evidence_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_historical_bar_evidence_collected_count_12",
    "operator_confirms_provider_request_count_12",
    "operator_confirms_successful_response_count_12",
    "operator_confirms_failed_response_count_zero",
    "operator_confirms_meta_reduced_bar_count_preserved",
    "approval_scope_acquisition_generation_only",
    "new_ticker_acquisition_authorized_true",
    "acquisition_generation_authorized_true",
    "acquisition_generation_approved_true",
    "ready_for_acquisition_generation_freeze_true",
    "acquisition_generation_executed_false",
    "acquisition_generation_frozen_false",
    "per_ticker_acquisition_generation_approval_entries_12",
    "per_ticker_acquisition_generation_approval_digests_present",
    "dataset_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "canonical_dataset_candidate_created_false",
    "canonical_dataset_frozen_false",
    "registry_approval_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
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
    "acquisition_provider_evidence_rerun_performed_false",
    "approval_creates_dataset_authority_false",
    "approval_creates_canonical_dataset_authority_false",
    "approval_creates_registry_approval_false",
    "approval_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_acquisition_generation_execution_artifact_created",
    "no_acquisition_generation_freeze_artifact_created",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AcquisitionGenerationApprovalError(ValueError):
    """Raised when acquisition generation approval evidence is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AcquisitionGenerationApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationApprovalError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationApprovalError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionGenerationApprovalError(f"{field} missing")


def build_acquisition_generation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_acquisition_evidence_results_review_digest: str,
    operator_confirms_acquisition_provider_evidence_execution_digest: str,
    operator_confirms_acquisition_provider_evidence_request_approval_digest: str,
    operator_confirms_acquisition_chain_candidate_review_digest: str,
    operator_confirms_corporate_action_authority_approval_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_historical_bar_evidence_collected_count: int,
    operator_confirms_provider_request_count: int,
    operator_confirms_successful_provider_response_count: int,
    operator_confirms_failed_provider_response_count_zero: bool,
    operator_confirms_meta_reduced_bar_count_preserved: bool,
    operator_confirms_approval_scope_acquisition_generation_only: bool,
    operator_confirms_new_ticker_acquisition_authorized: bool,
    operator_confirms_acquisition_generation_authorized: bool,
    operator_confirms_ready_for_acquisition_generation_freeze: bool,
    operator_confirms_no_acquisition_generation_execution: bool,
    operator_confirms_no_acquisition_generation_freeze: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_canonical_dataset_authorization: bool,
    operator_confirms_no_registry_approval: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION,
) -> dict[str, Any]:
    """Build a non-secret operator attestation; validation occurs at approval."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_APPROVAL_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_acquisition_evidence_results_review_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "operator_confirms_acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "operator_confirms_acquisition_chain_candidate_review_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise AcquisitionGenerationApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION,
        "operator_attestation_phrase": REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_historical_bar_evidence_collected_count": 12,
        "operator_confirms_provider_request_count": 12,
        "operator_confirms_successful_provider_response_count": 12,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise AcquisitionGenerationApprovalError(f"{field} required")


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        evidence_review.build_acquisition_evidence_results_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    validation = evidence_review.validate_acquisition_evidence_results_review_package_v1(package)
    _expect(
        package.get("acquisition_evidence_results_review_package_digest"),
        EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source acquisition evidence results review digest",
    )
    _expect(package.get("review_status"), evidence_review.ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY, "source review status")
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source review blocker_count")
    _expect(validation.get("acquisition_evidence_results_review_package_digest"), EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, "validated source review digest")
    return package


def per_ticker_acquisition_generation_approval_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_acquisition_generation_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for row in source["per_ticker_acquisition_evidence_summary"]:
        entry = {
            "ticker": row["ticker"],
            "acquisition_generation_approval_status": APPROVED_FOR_ACQUISITION_GENERATION_FREEZE_INPUT_ONLY,
            "historical_bar_evidence_status": row["acquisition_provider_evidence_status"],
            "historical_bar_count": row["historical_bar_count"],
            "meta_reduced_bar_count_flag": row["ticker"] == "META",
            "acquisition_generation_executed": False,
            "acquisition_generation_frozen": False,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_acquisition_generation_approval_digest"] = (
            per_ticker_acquisition_generation_approval_digest_v1(entry)
        )
        approvals.append(entry)
    return approvals


def _base_artifact(source: dict[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_APPROVED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_APPROVAL_V1,
        "approval_status": ACQUISITION_GENERATION_APPROVED,
        "approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "acquisition_provider_evidence_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "acquisition_provider_request_authorized": True,
        "acquisition_provider_evidence_executed": True,
        "acquisition_provider_evidence_results_created": True,
        "acquisition_evidence_results_review_created": True,
        "acquisition_evidence_results_review_ready": True,
        "new_ticker_acquisition_authorized": True,
        "acquisition_generation_authorized": True,
        "acquisition_generation_approved": True,
        "ready_for_acquisition_generation_freeze": True,
        "acquisition_generation_executed": False,
        "acquisition_generation_results_created": False,
        "acquisition_generation_frozen": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "acquisition_generation_chain_candidate_created": True,
        "acquisition_generation_chain_candidate_review_created": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_acquisition_evidence_results_review_blocker_count": source["review_summary"]["blocker_count"],
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "historical_bar_evidence_collected_count": source["historical_bar_evidence_collected_count"],
        "provider_request_count": source["provider_request_count"],
        "successful_provider_response_count": source["successful_provider_response_count"],
        "failed_provider_response_count": source["failed_provider_response_count"],
        "meta_reduced_bar_count_preserved": source["meta_reduced_bar_count_recorded"],
        "per_ticker_acquisition_generation_approvals": _per_ticker_approvals(source),
        "acquisition_generation_approved_by_operator": True,
        "acquisition_generation_approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "acquisition_generation_execution_authorized_by_this_artifact": False,
        "acquisition_generation_freeze_created_by_this_artifact": False,
        "dataset_generation_authorized_by_this_artifact": False,
        "canonical_dataset_authorized_by_this_artifact": False,
        "registry_approval_created_by_this_artifact": False,
        "predictive_evidence_authorized_by_this_artifact": False,
        "runtime_authorized_by_this_artifact": False,
        "approval_creates_dataset_authority": False,
        "approval_creates_canonical_dataset_authority": False,
        "approval_creates_registry_approval": False,
        "approval_creates_runtime_authority": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "operator_attestation": deepcopy(dict(attestation)),
        "acquisition_generation_execution_artifact_created": False,
        "acquisition_generation_freeze_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
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
    operator = artifact["operator_attestation"]
    entries = artifact["per_ticker_acquisition_generation_approvals"]
    values: dict[str, tuple[Any, Any]] = {
        "acquisition_evidence_results_review_digest_matches_expected": (EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("acquisition_evidence_results_review_package_digest")),
        "acquisition_evidence_results_review_has_zero_blockers": (0, artifact.get("source_acquisition_evidence_results_review_blocker_count")),
        "acquisition_provider_evidence_execution_digest_bound": (EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST, artifact.get("acquisition_provider_evidence_execution_digest")),
        "acquisition_provider_evidence_request_approval_digest_bound": (EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, artifact.get("acquisition_provider_evidence_request_approval_digest")),
        "acquisition_chain_candidate_review_digest_bound": (EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("acquisition_generation_chain_candidate_review_package_digest")),
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, artifact.get("corporate_action_authority_approval_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_acquisition_evidence_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_ACQUISITION_GENERATION, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(operator.get(field) == value for field, value in _expected_digest_confirmations().items())),
        "operator_confirms_historical_bar_evidence_collected_count_12": (12, operator.get("operator_confirms_historical_bar_evidence_collected_count")),
        "operator_confirms_provider_request_count_12": (12, operator.get("operator_confirms_provider_request_count")),
        "operator_confirms_successful_response_count_12": (12, operator.get("operator_confirms_successful_provider_response_count")),
        "operator_confirms_failed_response_count_zero": (True, operator.get("operator_confirms_failed_provider_response_count_zero")),
        "operator_confirms_meta_reduced_bar_count_preserved": (True, operator.get("operator_confirms_meta_reduced_bar_count_preserved")),
        "approval_scope_acquisition_generation_only": (ACQUISITION_GENERATION_APPROVAL_ONLY, artifact.get("approval_scope")),
        "new_ticker_acquisition_authorized_true": (True, artifact.get("new_ticker_acquisition_authorized")),
        "acquisition_generation_authorized_true": (True, artifact.get("acquisition_generation_authorized")),
        "acquisition_generation_approved_true": (True, artifact.get("acquisition_generation_approved")),
        "ready_for_acquisition_generation_freeze_true": (True, artifact.get("ready_for_acquisition_generation_freeze")),
        "per_ticker_acquisition_generation_approval_entries_12": (12, len(entries)),
        "per_ticker_acquisition_generation_approval_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_acquisition_generation_approval_digest"), str) and len(row["per_ticker_acquisition_generation_approval_digest"]) == 64 for row in entries)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        "limitations_recorded": (LIMITATIONS, artifact.get("limitations")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
    }
    false_checks = {
        "acquisition_generation_executed_false": "acquisition_generation_executed",
        "acquisition_generation_frozen_false": "acquisition_generation_frozen",
        "dataset_generation_authorized_false": "dataset_generation_authorized",
        "canonical_dataset_authorized_false": "canonical_dataset_authorized",
        "canonical_dataset_candidate_created_false": "canonical_dataset_candidate_created",
        "canonical_dataset_frozen_false": "canonical_dataset_frozen",
        "registry_approval_created_false": "registry_approval_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized_false": "predictive_experiment_rerun_authorized",
        "feature_matrix_regeneration_performed_false": "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "provider_requests_made_in_approval_false": "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval_false": "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval_false": "market_data_acquisition_performed_in_approval",
        "acquisition_provider_evidence_rerun_performed_false": "acquisition_provider_evidence_rerun_performed",
        "approval_creates_dataset_authority_false": "approval_creates_dataset_authority",
        "approval_creates_canonical_dataset_authority_false": "approval_creates_canonical_dataset_authority",
        "approval_creates_registry_approval_false": "approval_creates_registry_approval",
        "approval_creates_runtime_authority_false": "approval_creates_runtime_authority",
        "no_acquisition_generation_execution_artifact_created": "acquisition_generation_execution_artifact_created",
        "no_acquisition_generation_freeze_artifact_created": "acquisition_generation_freeze_artifact_created",
        "no_dataset_generation_authorization_created": "dataset_generation_authorization_created",
        "no_canonical_dataset_artifact_created": "canonical_dataset_artifact_created",
        "no_registry_approval_created": "registry_approval_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update({check_id: (False, artifact.get(field)) for check_id, field in false_checks.items()})
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "acquisition_generation_approved_by_operator": not failed,
        "approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "new_ticker_acquisition_authorized": not failed,
        "acquisition_generation_authorized": not failed,
        "ready_for_acquisition_generation_freeze": not failed,
        "acquisition_generation_executed": False,
        "acquisition_generation_frozen": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def acquisition_generation_approval_digest_v1(artifact: dict[str, Any]) -> str:
    payload = deepcopy(artifact)
    payload.pop("acquisition_generation_approval_digest", None)
    return semantic_digest(payload)


def build_acquisition_generation_approved_v1(
    *,
    acquisition_evidence_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build approval from reviewed saved evidence without provider access."""
    source = _source_review(acquisition_evidence_results_review_package)
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["approval_checklist"] = _checklist(artifact)
    artifact["approval_summary"] = _summary(artifact["approval_checklist"])
    artifact["acquisition_generation_approval_digest"] = acquisition_generation_approval_digest_v1(artifact)
    validate_acquisition_generation_approved_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_acquisition_generation_approvals")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AcquisitionGenerationApprovalError("per_ticker approvals mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "acquisition_generation_approval_status": APPROVED_FOR_ACQUISITION_GENERATION_FREEZE_INPUT_ONLY,
            "historical_bar_evidence_status": ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
            "historical_bar_count": 913 if ticker == "META" else 1003,
            "meta_reduced_bar_count_flag": ticker == "META",
            "acquisition_generation_executed": False,
            "acquisition_generation_frozen": False,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_acquisition_generation_approval_digest")
        _expect_digest(digest, f"{ticker}.approval digest")
        _expect(digest, per_ticker_acquisition_generation_approval_digest_v1(row), f"{ticker}.approval digest")


def validate_acquisition_generation_approved_v1(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate source bindings, attestation, approval, and closed downstream gates."""
    if not isinstance(approved_artifact, dict):
        raise AcquisitionGenerationApprovalError("approved_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_APPROVED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_APPROVAL_V1,
        "approval_status": ACQUISITION_GENERATION_APPROVED,
        "approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "acquisition_generation_approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "acquisition_evidence_results_review_package_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_acquisition_evidence_results_review_blocker_count": 0,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "historical_bar_evidence_collected_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, value in expected.items():
        _expect(approved_artifact.get(field), value, field)
    for field in (
        "created_offline", "acquisition_provider_request_authorized",
        "acquisition_provider_evidence_executed", "acquisition_provider_evidence_results_created",
        "acquisition_evidence_results_review_created", "acquisition_evidence_results_review_ready",
        "new_ticker_acquisition_authorized", "acquisition_generation_authorized",
        "acquisition_generation_approved", "ready_for_acquisition_generation_freeze",
        "acquisition_generation_chain_candidate_created", "acquisition_generation_chain_candidate_review_created",
        "corporate_action_authority_created", "corporate_action_authority_approved",
        "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen",
        "identity_authority_created", "identity_authority_frozen", "research_only",
        "meta_reduced_bar_count_preserved", "acquisition_generation_approved_by_operator",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "market_data_acquisition_performed_in_approval", "acquisition_provider_evidence_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "acquisition_generation_executed", "acquisition_generation_results_created",
        "acquisition_generation_frozen", "dataset_generation_authorized",
        "canonical_dataset_authorized", "canonical_dataset_candidate_created",
        "canonical_dataset_frozen", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "acquisition_generation_execution_authorized_by_this_artifact",
        "acquisition_generation_freeze_created_by_this_artifact", "dataset_generation_authorized_by_this_artifact",
        "canonical_dataset_authorized_by_this_artifact", "registry_approval_created_by_this_artifact",
        "predictive_evidence_authorized_by_this_artifact", "runtime_authorized_by_this_artifact",
        "approval_creates_dataset_authority", "approval_creates_canonical_dataset_authority",
        "approval_creates_registry_approval", "approval_creates_runtime_authority",
        "acquisition_generation_execution_artifact_created", "acquisition_generation_freeze_artifact_created",
        "dataset_generation_authorization_created", "canonical_dataset_artifact_created",
        "registry_approval_artifact_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    _validate_attestation(approved_artifact.get("operator_attestation", {}))
    _validate_per_ticker(approved_artifact)
    checklist = approved_artifact.get("approval_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationApprovalError("approval_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "approval checklist ids")
    for row in checklist:
        _expect(row.get("status"), PASS, f"{row.get('check_id')}.status")
        _expect(row.get("severity"), BLOCKER, f"{row.get('check_id')}.severity")
    _expect(checklist, _checklist(approved_artifact), "approval checklist")
    _expect(approved_artifact.get("approval_summary"), _summary(checklist), "approval summary")
    digest = approved_artifact.get("acquisition_generation_approval_digest")
    _expect_digest(digest, "acquisition_generation_approval_digest")
    _expect(digest, acquisition_generation_approval_digest_v1(approved_artifact), "acquisition_generation_approval_digest")
    return {
        "status": ACQUISITION_GENERATION_APPROVED,
        "approval_scope": ACQUISITION_GENERATION_APPROVAL_ONLY,
        "acquisition_generation_approval_digest": digest,
        "total_checks": approved_artifact["approval_summary"]["total_checks"],
        "passed_checks": approved_artifact["approval_summary"]["passed_checks"],
        "failed_checks": approved_artifact["approval_summary"]["failed_checks"],
        "blocker_count": approved_artifact["approval_summary"]["blocker_count"],
    }


def build_acquisition_generation_approved_markdown_v1(approved_artifact: dict[str, Any]) -> str:
    validation = validate_acquisition_generation_approved_v1(approved_artifact)
    summary = approved_artifact["approval_summary"]
    operator = approved_artifact["operator_attestation"]
    lines = [
        "# MarketFlow Acquisition Generation Approval v1", "",
        "## Approved Acquisition Generation",
        f"- Artifact/status: `{approved_artifact['artifact_kind']}` / `{approved_artifact['approval_status']}`.",
        f"- Approval digest: `{validation['acquisition_generation_approval_digest']}`.", "",
        "## Operator Attestation",
        f"- Decision/reference/timestamp: `{operator['operator_decision']}` / `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}`.",
        f"- Exact phrase: `{operator['operator_attestation_phrase']}`.", "",
        "## Source Acquisition Evidence Results Review",
        f"- Review digest: `{approved_artifact['acquisition_evidence_results_review_package_digest']}`; source blockers: `{approved_artifact['source_acquisition_evidence_results_review_blocker_count']}`.", "",
        "## Source Provider Evidence Execution",
        f"- Execution/request approval digests: `{approved_artifact['acquisition_provider_evidence_execution_digest']}` / `{approved_artifact['acquisition_provider_evidence_request_approval_digest']}`.", "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in approved_artifact["target_universe"]) + ".", "",
        "## Approved Per-Ticker Acquisition Generation Summary",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['acquisition_generation_approval_status']}`, bars `{row['historical_bar_count']}`."
        for row in approved_artifact["per_ticker_acquisition_generation_approvals"]
    )
    lines.extend([
        "", "## META Reduced Bar Count Preservation", "- META remains recorded at `913` bars; all other tickers remain at `1003`.", "",
        "## Approval Scope", f"- `{approved_artifact['approval_scope']}` authorizes future acquisition-generation freeze input only.", "",
        "## Acquisition Execution Boundary", "- Approval is not execution; acquisition generation remains unexecuted.", "",
        "## Acquisition Freeze Boundary", "- Approval is not freeze; a separate freeze ceremony is required.", "",
        "## Dataset Boundary", "- Dataset generation remains unauthorized.", "",
        "## Canonical Dataset Boundary", "- No canonical dataset candidate, authorization, or freeze was created.", "",
        "## Registry Boundary", "- No registry approval was created.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.", "",
        "## Approval Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`.", "",
        "## Remaining Required Tasks", *[f"- `{item}`" for item in approved_artifact["next_gates"]], "",
        "## Guardrails", *[f"- `{item}`" for item in approved_artifact["limitations"]],
        "- No provider request, evidence rerun, live transport, raw payload commit, or API-key handling occurred in approval.",
    ])
    return "\n".join(lines) + "\n"


def write_acquisition_generation_approved_v1(
    output_dir: str | Path,
    *,
    acquisition_evidence_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write canonical approval JSON without overwriting an existing artifact."""
    artifact = build_acquisition_generation_approved_v1(
        acquisition_evidence_results_review_package=acquisition_evidence_results_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_acquisition_generation_approved_v1(artifact)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "acquisition_generation_approved_v1.json"
    if path.exists():
        raise AcquisitionGenerationApprovalError("acquisition generation approval output already exists")
    payload = canonical_json_bytes(artifact)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": artifact["artifact_kind"],
        "approval_status": artifact["approval_status"],
        "approval_scope": artifact["approval_scope"],
        "acquisition_generation_approval_digest": validation["acquisition_generation_approval_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
