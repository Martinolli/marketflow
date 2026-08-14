"""Offline operator ceremony freezing approved acquisition-generation decisions."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_approval_service as approval


ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
SCHEMA_VERSION_ACQUISITION_GENERATION_FREEZE_V1 = "acquisition_generation_freeze_v1"
ACQUISITION_GENERATION_FROZEN = "ACQUISITION_GENERATION_FROZEN"
ACQUISITION_GENERATION_FREEZE_ONLY = "ACQUISITION_GENERATION_FREEZE_ONLY"
OPERATOR_DECISION_FREEZE_ACQUISITION_GENERATION = "FREEZE_ACQUISITION_GENERATION"
OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_FREEZE_V1 = (
    "acquisition_generation_freeze_operator_attestation_v1"
)
REQUIRED_ACQUISITION_GENERATION_FREEZE_ATTESTATION_PHRASE = (
    "FREEZE ACQUISITION GENERATION MSFT NVDA AMZN GOOGL META TSLA JPM XOM "
    "JNJ WMT CAT LMT ACQUISITION_GENERATION_FREEZE_ONLY"
)

EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST = (
    "9ce3949432707a33ca652ec267a4228540f9575ad1003661e774ea199fb88869"
)
EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    approval.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST = (
    approval.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST
)
EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
PASS = approval.PASS
FAIL = approval.FAIL
BLOCKER = approval.BLOCKER
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_ACCEPTED = approval.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = approval.PROFITABILITY_NOT_ACCEPTED
ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY = approval.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY
FROZEN_FOR_CANONICAL_DATASET_CHAIN_INPUT_ONLY = "FROZEN_FOR_CANONICAL_DATASET_CHAIN_INPUT_ONLY"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_failed_provider_response_count_zero",
    "operator_confirms_meta_reduced_bar_count_preserved",
    "operator_confirms_freeze_scope_acquisition_generation_only",
    "operator_confirms_acquisition_generation_authorized",
    "operator_confirms_acquisition_generation_approved",
    "operator_confirms_ready_for_canonical_dataset_chain_candidate",
    "operator_confirms_no_acquisition_generation_execution",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_canonical_dataset_authorization",
    "operator_confirms_no_canonical_dataset_candidate",
    "operator_confirms_no_canonical_dataset_freeze",
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
    "freeze_is_not_dataset_generation",
    "freeze_is_not_canonical_dataset_creation",
    "freeze_is_not_registry_approval",
    "provider_evidence_is_read_only_snapshot",
    "meta_reduced_bar_count_requires_preservation_in_canonical_dataset_chain",
    "dataset_generation_not_authorized",
    "canonical_dataset_not_authorized",
    "registry_approval_not_created",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "operator_approval_required_before_canonical_dataset_chain",
]
NEXT_GATES = [
    "canonical_dataset_chain_candidate",
    "canonical_dataset_candidate_operator_review",
    "canonical_dataset_approval_if_required",
    "canonical_dataset_freeze",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

REQUIRED_CHECK_IDS = [
    "acquisition_generation_approval_digest_matches_expected",
    "acquisition_generation_approval_has_zero_blockers",
    "acquisition_evidence_results_review_digest_bound",
    "acquisition_provider_evidence_execution_digest_bound",
    "acquisition_provider_evidence_request_approval_digest_bound",
    "acquisition_chain_candidate_review_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_acquisition_generation_approval_universe",
    "operator_decision_freeze",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_historical_bar_evidence_collected_count_12",
    "operator_confirms_provider_request_count_12",
    "operator_confirms_successful_response_count_12",
    "operator_confirms_failed_response_count_zero",
    "operator_confirms_meta_reduced_bar_count_preserved",
    "freeze_scope_acquisition_generation_only",
    "new_ticker_acquisition_authorized_true",
    "acquisition_generation_authorized_true",
    "acquisition_generation_approved_true",
    "acquisition_generation_frozen_true",
    "ready_for_canonical_dataset_chain_candidate_true",
    "acquisition_generation_executed_false",
    "acquisition_generation_results_created_false",
    "per_ticker_acquisition_generation_freeze_entries_12",
    "per_ticker_acquisition_generation_freeze_digests_present",
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
    "provider_requests_made_in_freeze_false",
    "live_provider_transport_enabled_in_freeze_false",
    "market_data_acquisition_performed_in_freeze_false",
    "acquisition_provider_evidence_rerun_performed_false",
    "freeze_creates_dataset_authority_false",
    "freeze_creates_canonical_dataset_authority_false",
    "freeze_creates_registry_approval_false",
    "freeze_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AcquisitionGenerationFreezeError(ValueError):
    """Raised when freeze evidence or an authority boundary is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AcquisitionGenerationFreezeError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationFreezeError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationFreezeError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionGenerationFreezeError(f"{field} missing")


def build_acquisition_generation_freeze_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_acquisition_generation_approval_digest: str,
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
    operator_confirms_freeze_scope_acquisition_generation_only: bool,
    operator_confirms_acquisition_generation_authorized: bool,
    operator_confirms_acquisition_generation_approved: bool,
    operator_confirms_ready_for_canonical_dataset_chain_candidate: bool,
    operator_confirms_no_acquisition_generation_execution: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_canonical_dataset_authorization: bool,
    operator_confirms_no_canonical_dataset_candidate: bool,
    operator_confirms_no_canonical_dataset_freeze: bool,
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
    operator_decision: str = OPERATOR_DECISION_FREEZE_ACQUISITION_GENERATION,
) -> dict[str, Any]:
    """Build a non-secret operator attestation; validation occurs at freeze."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_FREEZE_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "operator_confirms_acquisition_evidence_results_review_digest": EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "operator_confirms_acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "operator_confirms_acquisition_chain_candidate_review_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise AcquisitionGenerationFreezeError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_FREEZE_ACQUISITION_GENERATION,
        "operator_attestation_phrase": REQUIRED_ACQUISITION_GENERATION_FREEZE_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_ACQUISITION_GENERATION_FREEZE_V1,
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
            raise AcquisitionGenerationFreezeError(f"{field} required")


def _source_approval_attestation() -> dict[str, Any]:
    """Reproduce the saved approval artifact described by its checked-in status."""
    return approval.build_acquisition_generation_approval_attestation_v1(
        operator_reference="USER_REQUEST_6D45A73A",
        operator_attestation_timestamp_utc="2026-08-14T12:23:21Z",
        operator_attestation_phrase=approval.REQUIRED_ACQUISITION_GENERATION_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_acquisition_evidence_results_review_digest=EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_acquisition_provider_evidence_execution_digest=EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        operator_confirms_acquisition_provider_evidence_request_approval_digest=EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        operator_confirms_acquisition_chain_candidate_review_digest=EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_target_universe=list(TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_historical_bar_evidence_collected_count=12,
        operator_confirms_provider_request_count=12,
        operator_confirms_successful_provider_response_count=12,
        operator_confirms_failed_provider_response_count_zero=True,
        operator_confirms_meta_reduced_bar_count_preserved=True,
        operator_confirms_approval_scope_acquisition_generation_only=True,
        operator_confirms_new_ticker_acquisition_authorized=True,
        operator_confirms_acquisition_generation_authorized=True,
        operator_confirms_ready_for_acquisition_generation_freeze=True,
        operator_confirms_no_acquisition_generation_execution=True,
        operator_confirms_no_acquisition_generation_freeze=True,
        operator_confirms_no_dataset_generation_authorization=True,
        operator_confirms_no_canonical_dataset_authorization=True,
        operator_confirms_no_registry_approval=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_runtime_activation=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


def _source_approval(source: dict[str, Any] | None) -> dict[str, Any]:
    artifact = (
        approval.build_acquisition_generation_approved_v1(
            operator_attestation=_source_approval_attestation()
        )
        if source is None
        else deepcopy(source)
    )
    try:
        validation = approval.validate_acquisition_generation_approved_v1(artifact)
    except approval.AcquisitionGenerationApprovalError as exc:
        raise AcquisitionGenerationFreezeError(f"source acquisition generation approval invalid: {exc}") from exc
    _expect(validation.get("acquisition_generation_approval_digest"), EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST, "source approval digest")
    _expect(validation.get("blocker_count"), 0, "source approval blocker_count")
    return artifact


def per_ticker_acquisition_generation_freeze_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_acquisition_generation_freeze_digest", None)
    return semantic_digest(payload)


def _per_ticker_freezes(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_acquisition_generation_approvals"]:
        entry = {
            "ticker": row["ticker"],
            "acquisition_generation_freeze_status": FROZEN_FOR_CANONICAL_DATASET_CHAIN_INPUT_ONLY,
            "historical_bar_evidence_status": row["historical_bar_evidence_status"],
            "historical_bar_count": row["historical_bar_count"],
            "meta_reduced_bar_count_flag": row["meta_reduced_bar_count_flag"],
            "acquisition_generation_executed": False,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "canonical_dataset_candidate_created": False,
            "canonical_dataset_frozen": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_acquisition_generation_freeze_digest"] = (
            per_ticker_acquisition_generation_freeze_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_artifact(source: dict[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    copied_fields = [
        "acquisition_provider_request_authorized", "acquisition_provider_evidence_executed",
        "acquisition_provider_evidence_results_created", "acquisition_evidence_results_review_created",
        "acquisition_evidence_results_review_ready", "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized", "acquisition_generation_approved",
        "acquisition_generation_chain_candidate_created", "acquisition_generation_chain_candidate_review_created",
        "corporate_action_authority_created", "corporate_action_authority_approved",
        "corporate_action_authority_scope", "split_event_authority_created", "split_event_authority_frozen",
        "split_event_authority_scope", "dividend_event_authority_created", "dividend_event_authority_frozen",
        "dividend_event_authority_scope", "identity_authority_created", "identity_authority_frozen",
        "acquisition_evidence_results_review_package_digest", "acquisition_provider_evidence_execution_digest",
        "acquisition_provider_evidence_request_approval_digest",
        "acquisition_generation_chain_candidate_review_package_digest",
        "acquisition_generation_chain_candidate_digest", "corporate_action_authority_approval_digest",
        "combined_split_dividend_corporate_action_readiness_review_package_digest",
        "split_event_authority_freeze_digest", "dividend_event_authority_freeze_digest",
        "identity_authority_freeze_digest", "ticker_universe_selection_approval_digest",
        "target_universe", "target_universe_count", "historical_bar_evidence_collected_count",
        "provider_request_count", "successful_provider_response_count", "failed_provider_response_count",
        "meta_reduced_bar_count_preserved",
    ]
    artifact = {field: deepcopy(source[field]) for field in copied_fields}
    artifact.update({
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_FREEZE_V1,
        "freeze_status": ACQUISITION_GENERATION_FROZEN,
        "freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "live_provider_transport_enabled_in_freeze": False,
        "market_data_acquisition_performed_in_freeze": False,
        "acquisition_provider_evidence_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "acquisition_generation_frozen": True,
        "acquisition_generation_executed": False,
        "acquisition_generation_results_created": False,
        "ready_for_canonical_dataset_chain_candidate": True,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
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
        "acquisition_generation_approval_digest": source["acquisition_generation_approval_digest"],
        "source_acquisition_generation_approval_blocker_count": source["approval_summary"]["blocker_count"],
        "per_ticker_acquisition_generation_freezes": _per_ticker_freezes(source),
        "acquisition_generation_frozen_by_operator": True,
        "acquisition_generation_freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "acquisition_generation_freeze_creates_dataset_authority": False,
        "acquisition_generation_freeze_creates_canonical_dataset_authority": False,
        "acquisition_generation_freeze_creates_registry_approval": False,
        "acquisition_generation_freeze_creates_predictive_evidence_authority": False,
        "acquisition_generation_freeze_creates_runtime_authority": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "operator_attestation": deepcopy(dict(attestation)),
        "dataset_generation_authorization_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    })
    return artifact


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
    entries = artifact["per_ticker_acquisition_generation_freezes"]
    values: dict[str, tuple[Any, Any]] = {
        "acquisition_generation_approval_digest_matches_expected": (EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST, artifact.get("acquisition_generation_approval_digest")),
        "acquisition_generation_approval_has_zero_blockers": (0, artifact.get("source_acquisition_generation_approval_blocker_count")),
        "acquisition_evidence_results_review_digest_bound": (EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("acquisition_evidence_results_review_package_digest")),
        "acquisition_provider_evidence_execution_digest_bound": (EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST, artifact.get("acquisition_provider_evidence_execution_digest")),
        "acquisition_provider_evidence_request_approval_digest_bound": (EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, artifact.get("acquisition_provider_evidence_request_approval_digest")),
        "acquisition_chain_candidate_review_digest_bound": (EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("acquisition_generation_chain_candidate_review_package_digest")),
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, artifact.get("corporate_action_authority_approval_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_acquisition_generation_approval_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_freeze": (OPERATOR_DECISION_FREEZE_ACQUISITION_GENERATION, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_ACQUISITION_GENERATION_FREEZE_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(operator.get(field) == value for field, value in _expected_digest_confirmations().items())),
        "operator_confirms_historical_bar_evidence_collected_count_12": (12, operator.get("operator_confirms_historical_bar_evidence_collected_count")),
        "operator_confirms_provider_request_count_12": (12, operator.get("operator_confirms_provider_request_count")),
        "operator_confirms_successful_response_count_12": (12, operator.get("operator_confirms_successful_provider_response_count")),
        "operator_confirms_failed_response_count_zero": (True, operator.get("operator_confirms_failed_provider_response_count_zero")),
        "operator_confirms_meta_reduced_bar_count_preserved": (True, operator.get("operator_confirms_meta_reduced_bar_count_preserved")),
        "freeze_scope_acquisition_generation_only": (ACQUISITION_GENERATION_FREEZE_ONLY, artifact.get("freeze_scope")),
        "new_ticker_acquisition_authorized_true": (True, artifact.get("new_ticker_acquisition_authorized")),
        "acquisition_generation_authorized_true": (True, artifact.get("acquisition_generation_authorized")),
        "acquisition_generation_approved_true": (True, artifact.get("acquisition_generation_approved")),
        "acquisition_generation_frozen_true": (True, artifact.get("acquisition_generation_frozen")),
        "ready_for_canonical_dataset_chain_candidate_true": (True, artifact.get("ready_for_canonical_dataset_chain_candidate")),
        "per_ticker_acquisition_generation_freeze_entries_12": (12, len(entries)),
        "per_ticker_acquisition_generation_freeze_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_acquisition_generation_freeze_digest"), str) and len(row["per_ticker_acquisition_generation_freeze_digest"]) == 64 for row in entries)),
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
        "acquisition_generation_results_created_false": "acquisition_generation_results_created",
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
        "provider_requests_made_in_freeze_false": "provider_requests_made_in_freeze",
        "live_provider_transport_enabled_in_freeze_false": "live_provider_transport_enabled_in_freeze",
        "market_data_acquisition_performed_in_freeze_false": "market_data_acquisition_performed_in_freeze",
        "acquisition_provider_evidence_rerun_performed_false": "acquisition_provider_evidence_rerun_performed",
        "freeze_creates_dataset_authority_false": "acquisition_generation_freeze_creates_dataset_authority",
        "freeze_creates_canonical_dataset_authority_false": "acquisition_generation_freeze_creates_canonical_dataset_authority",
        "freeze_creates_registry_approval_false": "acquisition_generation_freeze_creates_registry_approval",
        "freeze_creates_runtime_authority_false": "acquisition_generation_freeze_creates_runtime_authority",
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
        "acquisition_generation_frozen_by_operator": not failed,
        "freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "new_ticker_acquisition_authorized": not failed,
        "acquisition_generation_authorized": not failed,
        "acquisition_generation_approved": not failed,
        "acquisition_generation_frozen": not failed,
        "ready_for_canonical_dataset_chain_candidate": not failed,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def acquisition_generation_freeze_digest_v1(artifact: dict[str, Any]) -> str:
    payload = deepcopy(artifact)
    payload.pop("acquisition_generation_freeze_digest", None)
    return semantic_digest(payload)


def build_acquisition_generation_frozen_v1(
    *,
    acquisition_generation_approval_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Freeze approved decisions offline without execution or provider access."""
    source = _source_approval(acquisition_generation_approval_artifact)
    _validate_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    artifact["freeze_checklist"] = _checklist(artifact)
    artifact["freeze_summary"] = _summary(artifact["freeze_checklist"])
    artifact["acquisition_generation_freeze_digest"] = acquisition_generation_freeze_digest_v1(artifact)
    validate_acquisition_generation_frozen_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_acquisition_generation_freezes")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AcquisitionGenerationFreezeError("per_ticker freezes mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "acquisition_generation_freeze_status": FROZEN_FOR_CANONICAL_DATASET_CHAIN_INPUT_ONLY,
            "historical_bar_evidence_status": ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
            "historical_bar_count": 913 if ticker == "META" else 1003,
            "meta_reduced_bar_count_flag": ticker == "META",
            "acquisition_generation_executed": False,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "canonical_dataset_candidate_created": False,
            "canonical_dataset_frozen": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_acquisition_generation_freeze_digest")
        _expect_digest(digest, f"{ticker}.freeze digest")
        _expect(digest, per_ticker_acquisition_generation_freeze_digest_v1(row), f"{ticker}.freeze digest")


def validate_acquisition_generation_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate source bindings, attestation, freeze, and closed downstream gates."""
    if not isinstance(frozen_artifact, dict):
        raise AcquisitionGenerationFreezeError("frozen_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_FREEZE_V1,
        "freeze_status": ACQUISITION_GENERATION_FROZEN,
        "freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "acquisition_generation_freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "acquisition_generation_approval_digest": EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
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
        "source_acquisition_generation_approval_blocker_count": 0,
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
        _expect(frozen_artifact.get(field), value, field)
    for field in (
        "created_offline", "acquisition_provider_request_authorized", "acquisition_provider_evidence_executed",
        "acquisition_provider_evidence_results_created", "acquisition_evidence_results_review_created",
        "acquisition_evidence_results_review_ready", "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized", "acquisition_generation_approved", "acquisition_generation_frozen",
        "ready_for_canonical_dataset_chain_candidate", "acquisition_generation_chain_candidate_created",
        "acquisition_generation_chain_candidate_review_created", "corporate_action_authority_created",
        "corporate_action_authority_approved", "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen", "identity_authority_created",
        "identity_authority_frozen", "research_only", "meta_reduced_bar_count_preserved",
        "acquisition_generation_frozen_by_operator",
    ):
        _expect_true(frozen_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_freeze", "live_provider_transport_enabled_in_freeze",
        "market_data_acquisition_performed_in_freeze", "acquisition_provider_evidence_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed", "acquisition_generation_executed",
        "acquisition_generation_results_created", "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_candidate_created", "canonical_dataset_frozen", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed", "trade_recommendations_generated",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "acquisition_generation_freeze_creates_dataset_authority",
        "acquisition_generation_freeze_creates_canonical_dataset_authority",
        "acquisition_generation_freeze_creates_registry_approval",
        "acquisition_generation_freeze_creates_predictive_evidence_authority",
        "acquisition_generation_freeze_creates_runtime_authority", "dataset_generation_authorization_created",
        "canonical_dataset_artifact_created", "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(frozen_artifact.get(field), field)
    _validate_attestation(frozen_artifact.get("operator_attestation", {}))
    _validate_per_ticker(frozen_artifact)
    checklist = frozen_artifact.get("freeze_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationFreezeError("freeze_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "freeze checklist ids")
    for row in checklist:
        _expect(row.get("status"), PASS, f"{row.get('check_id')}.status")
        _expect(row.get("severity"), BLOCKER, f"{row.get('check_id')}.severity")
    _expect(checklist, _checklist(frozen_artifact), "freeze checklist")
    _expect(frozen_artifact.get("freeze_summary"), _summary(checklist), "freeze summary")
    digest = frozen_artifact.get("acquisition_generation_freeze_digest")
    _expect_digest(digest, "acquisition_generation_freeze_digest")
    _expect(digest, acquisition_generation_freeze_digest_v1(frozen_artifact), "acquisition_generation_freeze_digest")
    return {
        "status": ACQUISITION_GENERATION_FROZEN,
        "freeze_scope": ACQUISITION_GENERATION_FREEZE_ONLY,
        "acquisition_generation_freeze_digest": digest,
        "total_checks": frozen_artifact["freeze_summary"]["total_checks"],
        "passed_checks": frozen_artifact["freeze_summary"]["passed_checks"],
        "failed_checks": frozen_artifact["freeze_summary"]["failed_checks"],
        "blocker_count": frozen_artifact["freeze_summary"]["blocker_count"],
    }


def build_acquisition_generation_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    validation = validate_acquisition_generation_frozen_v1(frozen_artifact)
    summary = frozen_artifact["freeze_summary"]
    operator = frozen_artifact["operator_attestation"]
    lines = [
        "# MarketFlow Acquisition Generation Freeze v1", "", "## Frozen Acquisition Generation",
        f"- Artifact/status: `{frozen_artifact['artifact_kind']}` / `{frozen_artifact['freeze_status']}`.",
        f"- Freeze digest: `{validation['acquisition_generation_freeze_digest']}`.", "",
        "## Operator Attestation", f"- Decision/reference/timestamp: `{operator['operator_decision']}` / `{operator['operator_reference']}` / `{operator['operator_attestation_timestamp_utc']}`.",
        f"- Exact phrase: `{operator['operator_attestation_phrase']}`.", "",
        "## Source Acquisition Generation Approval", f"- Approval digest: `{frozen_artifact['acquisition_generation_approval_digest']}`; source blockers: `0`.", "",
        "## Source Acquisition Evidence Results Review", f"- Review/execution digests: `{frozen_artifact['acquisition_evidence_results_review_package_digest']}` / `{frozen_artifact['acquisition_provider_evidence_execution_digest']}`.", "",
        "## Target Universe", "- " + ", ".join(f"`{ticker}`" for ticker in frozen_artifact["target_universe"]) + ".", "",
        "## Frozen Per-Ticker Acquisition Generation Summary",
    ]
    lines.extend(f"- `{row['ticker']}`: `{row['acquisition_generation_freeze_status']}`, bars `{row['historical_bar_count']}`." for row in frozen_artifact["per_ticker_acquisition_generation_freezes"])
    lines.extend([
        "", "## META Reduced Bar Count Preservation", "- META remains at `913` bars; all other tickers remain at `1003`.", "",
        "## Freeze Scope", f"- `{frozen_artifact['freeze_scope']}` freezes future canonical-dataset-chain input decisions only.", "",
        "## Dataset Boundary", "- Freeze is not dataset generation; dataset generation remains unauthorized.", "",
        "## Canonical Dataset Boundary", "- No canonical dataset candidate, authorization, or freeze was created.", "",
        "## Registry Boundary", "- No registry approval was created.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.", "",
        "## Freeze Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']} / {summary['passed_checks']} / {summary['failed_checks']} / {summary['blocker_count']}`.", "",
        "## Remaining Required Tasks", *[f"- `{item}`" for item in frozen_artifact["next_gates"]], "",
        "## Guardrails", *[f"- `{item}`" for item in frozen_artifact["limitations"]],
        "- No provider request, acquisition rerun, dataset generation, raw-payload commit, API-key handling, or runtime activation occurred.",
    ])
    return "\n".join(lines) + "\n"


def write_acquisition_generation_frozen_v1(
    output_dir: str | Path,
    *,
    acquisition_generation_approval_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write canonical freeze JSON without overwriting an existing artifact."""
    artifact = build_acquisition_generation_frozen_v1(
        acquisition_generation_approval_artifact=acquisition_generation_approval_artifact,
        operator_attestation=operator_attestation,
    )
    validation = validate_acquisition_generation_frozen_v1(artifact)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "acquisition_generation_frozen_v1.json"
    if path.exists():
        raise AcquisitionGenerationFreezeError("acquisition generation freeze output already exists")
    payload = canonical_json_bytes(artifact)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": artifact["artifact_kind"],
        "freeze_status": artifact["freeze_status"], "freeze_scope": artifact["freeze_scope"],
        "acquisition_generation_freeze_digest": validation["acquisition_generation_freeze_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
