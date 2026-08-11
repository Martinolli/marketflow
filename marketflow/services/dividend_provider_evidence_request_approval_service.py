"""Offline approval ceremony for future read-only dividend provider evidence requests."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_event_authority_candidate_operator_review_service as dividend_review
from marketflow.services import split_event_authority_freeze_service as split_freeze


ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1 = (
    "dividend_event_provider_evidence_request_approval_v1"
)
DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED = (
    "DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED"
)
READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY = (
    "READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST = (
    "APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST"
)
OPERATOR_ATTESTATION_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1 = (
    "dividend_provider_evidence_request_approval_operator_attestation_v1"
)
REQUIRED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE DIVIDEND PROVIDER EVIDENCE REQUEST MSFT NVDA AMZN GOOGL META TSLA JPM "
    "XOM JNJ WMT CAT LMT READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY"
)

EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "cf120d55beaa22f1fbd4f27d9a7a6539583e5cd67f3d0ffe5a186f318f27a104"
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    dividend_review.EXPECTED_REVIEWED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    "37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303"
)
EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    split_freeze.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    split_freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    split_freeze.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    split_freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    split_freeze.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    split_freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    split_freeze.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = split_freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    split_freeze.approval.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    split_freeze.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(dividend_review.VALIDATION_TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_AUTHORIZED = split_freeze.NOT_AUTHORIZED
NOT_CREATED = "NOT_CREATED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_FROZEN = "NOT_FROZEN"
AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

DIVIDEND_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE = (
    "AUTHORIZE_READ_ONLY_DIVIDEND_EVENT_PROVIDER_EVIDENCE_REQUEST_FOR_EXPANDED_UNIVERSE"
)
DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE = (
    "READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY"
)
DIVIDEND_PROVIDER_EVIDENCE_AUTHORITY_SCOPE = (
    "EVIDENCE_REQUEST_ONLY_NOT_DIVIDEND_AUTHORITY"
)
DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_STATUS = NOT_EXECUTED

READ_ONLY_REQUEST_POLICY = {
    "allowed_future_request_type": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE,
    "provider_request_endpoint_plan": (
        "DIVIDEND_EVENT_ENDPOINT_TO_BE_SELECTED_BY_EXECUTION_SERVICE_OR_FAIL_CLOSED"
    ),
    "api_key_handling": "DO_NOT_STORE_KEYS_OR_PRINT_KEYS",
    "raw_payload_policy": "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS",
    "sanitized_status_doc_required": True,
    "rate_limit_policy": "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED",
    "provider_result_authority": "DIVIDEND_EVENT_EVIDENCE_ONLY_NOT_DIVIDEND_AUTHORITY",
}
PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES = [
    "dividend_provider_evidence_run_manifest",
    "dividend_provider_request_receipts_sanitized",
    "dividend_event_results_sanitized",
    "dividend_event_absence_inventory",
    "dividend_policy_reconciliation_report",
    "dividend_event_failure_reason_inventory",
    "operator_review_summary",
]
REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_request_scope_read_only_dividend_event_evidence_only",
    "operator_confirms_ready_for_dividend_provider_evidence_execution",
    "operator_confirms_no_provider_requests_made_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_dividend_provider_evidence_executed",
    "operator_confirms_no_dividend_provider_evidence_results_created",
    "operator_confirms_no_dividend_event_authority_created",
    "operator_confirms_no_dividend_event_authority_frozen",
    "operator_confirms_split_event_authority_frozen",
    "operator_confirms_no_split_provider_evidence_rerun",
    "operator_confirms_no_corporate_action_authority_created",
    "operator_confirms_no_acquisition_authority",
    "operator_confirms_no_dataset_generation_authorization",
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
REQUIRED_APPROVAL_CHECK_IDS = [
    "dividend_candidate_review_digest_matches_expected",
    "dividend_candidate_review_has_zero_blockers",
    "dividend_candidate_digest_matches_expected",
    "split_event_authority_freeze_digest_bound",
    "split_evidence_results_review_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "registry_inventory_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_dividend_candidate_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_dividend_candidate_review_digest",
    "operator_confirms_dividend_candidate_digest",
    "operator_confirms_split_authority_freeze_digest",
    "operator_confirms_split_evidence_results_review_digest",
    "operator_confirms_corporate_action_plan_approval_digest",
    "operator_confirms_registry_inventory_approval_digest",
    "operator_confirms_identity_freeze_digest",
    "operator_confirms_target_universe",
    "operator_confirms_request_scope_read_only_dividend_event_evidence_only",
    "operator_confirms_ready_for_dividend_provider_evidence_execution",
    "dividend_provider_evidence_request_authorized_true",
    "ready_for_dividend_provider_evidence_execution_true",
    "dividend_provider_evidence_executed_false",
    "dividend_provider_evidence_results_created_false",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "dividend_event_authority_created_false",
    "dividend_event_authority_frozen_false",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "split_provider_evidence_rerun_performed_false",
    "corporate_action_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "acquisition_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "registry_approval_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "predictive_experiment_rerun_performed_false",
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
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "no_dividend_provider_evidence_execution_created",
    "no_dividend_event_authority_artifact_created",
    "no_dividend_event_authority_freeze_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]
REMAINING_REQUIRED_TASKS = [
    "dividend_provider_evidence_execution",
    "dividend_event_evidence_results_review_package",
    "dividend_policy_reconciliation_review",
    "dividend_event_authority_freeze_ceremony",
    "combined_corporate_action_readiness_review",
]


class DividendProviderEvidenceRequestApprovalError(ValueError):
    """Raised when the dividend provider evidence request approval is invalid."""


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


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DividendProviderEvidenceRequestApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DividendProviderEvidenceRequestApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DividendProviderEvidenceRequestApprovalError(f"{field_name} must be false")


def _expect_digest(actual: Any, field_name: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise DividendProviderEvidenceRequestApprovalError(f"{field_name} missing")


def build_dividend_provider_evidence_request_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_dividend_candidate_review_package_digest: str,
    operator_confirms_dividend_candidate_digest: str,
    operator_confirms_split_event_authority_freeze_digest: str,
    operator_confirms_split_evidence_results_review_package_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_request_scope_read_only_dividend_event_evidence_only: bool,
    operator_confirms_ready_for_dividend_provider_evidence_execution: bool,
    operator_confirms_no_provider_requests_made_in_approval: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_dividend_provider_evidence_executed: bool,
    operator_confirms_no_dividend_provider_evidence_results_created: bool,
    operator_confirms_no_dividend_event_authority_created: bool,
    operator_confirms_no_dividend_event_authority_frozen: bool,
    operator_confirms_split_event_authority_frozen: bool,
    operator_confirms_no_split_provider_evidence_rerun: bool,
    operator_confirms_no_corporate_action_authority_created: bool,
    operator_confirms_no_acquisition_authority: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST,
) -> dict[str, Any]:
    """Build the non-secret operator attestation for approval."""
    return {
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "operator_reference": operator_reference,
        "operator_confirms_dividend_candidate_review_package_digest": operator_confirms_dividend_candidate_review_package_digest,
        "operator_confirms_dividend_candidate_digest": operator_confirms_dividend_candidate_digest,
        "operator_confirms_split_event_authority_freeze_digest": operator_confirms_split_event_authority_freeze_digest,
        "operator_confirms_split_evidence_results_review_package_digest": operator_confirms_split_evidence_results_review_package_digest,
        "operator_confirms_corporate_action_plan_approval_digest": operator_confirms_corporate_action_plan_approval_digest,
        "operator_confirms_registry_inventory_approval_digest": operator_confirms_registry_inventory_approval_digest,
        "operator_confirms_identity_freeze_digest": operator_confirms_identity_freeze_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_request_scope_read_only_dividend_event_evidence_only": operator_confirms_request_scope_read_only_dividend_event_evidence_only,
        "operator_confirms_ready_for_dividend_provider_evidence_execution": operator_confirms_ready_for_dividend_provider_evidence_execution,
        "operator_confirms_no_provider_requests_made_in_approval": operator_confirms_no_provider_requests_made_in_approval,
        "operator_confirms_no_live_provider_transport_enabled": operator_confirms_no_live_provider_transport_enabled,
        "operator_confirms_no_dividend_provider_evidence_executed": operator_confirms_no_dividend_provider_evidence_executed,
        "operator_confirms_no_dividend_provider_evidence_results_created": operator_confirms_no_dividend_provider_evidence_results_created,
        "operator_confirms_no_dividend_event_authority_created": operator_confirms_no_dividend_event_authority_created,
        "operator_confirms_no_dividend_event_authority_frozen": operator_confirms_no_dividend_event_authority_frozen,
        "operator_confirms_split_event_authority_frozen": operator_confirms_split_event_authority_frozen,
        "operator_confirms_no_split_provider_evidence_rerun": operator_confirms_no_split_provider_evidence_rerun,
        "operator_confirms_no_corporate_action_authority_created": operator_confirms_no_corporate_action_authority_created,
        "operator_confirms_no_acquisition_authority": operator_confirms_no_acquisition_authority,
        "operator_confirms_no_dataset_generation_authorization": operator_confirms_no_dataset_generation_authorization,
        "operator_confirms_no_predictive_usefulness_acceptance": operator_confirms_no_predictive_usefulness_acceptance,
        "operator_confirms_no_profitability_acceptance": operator_confirms_no_profitability_acceptance,
        "operator_confirms_no_runtime_migration_approval": operator_confirms_no_runtime_migration_approval,
        "operator_confirms_no_runtime_activation": operator_confirms_no_runtime_activation,
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
        "operator_confirms_no_trade_recommendations": operator_confirms_no_trade_recommendations,
        "operator_confirms_no_api_key_storage_or_printing": operator_confirms_no_api_key_storage_or_printing,
        "operator_confirms_no_raw_payload_commit": operator_confirms_no_raw_payload_commit,
    }


def _validate_operator_attestation(operator_attestation: Mapping[str, Any]) -> None:
    if not isinstance(operator_attestation, Mapping):
        raise DividendProviderEvidenceRequestApprovalError("operator_attestation missing")
    _expect(
        operator_attestation.get("operator_decision"),
        OPERATOR_DECISION_APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST,
        "operator_decision",
    )
    _expect(
        operator_attestation.get("operator_attestation_phrase"),
        REQUIRED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_phrase",
    )
    _expect(
        operator_attestation.get("operator_attestation_version"),
        OPERATOR_ATTESTATION_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "operator_attestation_version",
    )
    if not operator_attestation.get("operator_reference"):
        raise DividendProviderEvidenceRequestApprovalError("operator_reference missing")
    if not operator_attestation.get("operator_attestation_timestamp_utc"):
        raise DividendProviderEvidenceRequestApprovalError("operator_attestation_timestamp_utc missing")
    expected_digest_fields = {
        "operator_confirms_dividend_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "operator_confirms_split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_split_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    for field, expected in expected_digest_fields.items():
        _expect(operator_attestation.get(field), expected, field)
    _expect(operator_attestation.get("operator_confirms_target_universe"), TARGET_UNIVERSE, "operator_confirms_target_universe")
    _expect(operator_attestation.get("operator_confirms_target_count"), 12, "operator_confirms_target_count")
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(operator_attestation.get(field), field)


def _source_split_freeze_binding_artifact() -> dict[str, Any]:
    return {
        "artifact_kind": split_freeze.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN,
        "freeze_status": split_freeze.SPLIT_EVENT_AUTHORITY_FROZEN,
        "authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_provider_evidence_rerun_performed": False,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
    }


def _validate_dividend_candidate_review_package(package: Mapping[str, Any]) -> None:
    if not isinstance(package, Mapping):
        raise DividendProviderEvidenceRequestApprovalError("dividend_candidate_review_package missing")
    expected = {
        "artifact_kind": dividend_review.ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE,
        "review_status": dividend_review.DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_READY,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    for field, expected_value in expected.items():
        _expect(package.get(field), expected_value, f"dividend_review.{field}")
    summary = package.get("review_summary")
    if not isinstance(summary, Mapping) or summary.get("blocker_count") != 0:
        raise DividendProviderEvidenceRequestApprovalError("dividend_review.review_summary blocker_count mismatch")
    _expect_false(package.get("provider_requests_made_in_review"), "dividend_review.provider_requests_made_in_review")
    _expect_false(package.get("live_provider_transport_enabled_in_review"), "dividend_review.live_provider_transport_enabled_in_review")
    _expect_false(package.get("dividend_event_authority_created"), "dividend_review.dividend_event_authority_created")
    _expect_false(package.get("dividend_event_authority_frozen"), "dividend_review.dividend_event_authority_frozen")
    entries = package.get("per_ticker_dividend_event_review_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise DividendProviderEvidenceRequestApprovalError("dividend_review.per_ticker_dividend_event_review_entries mismatch")
    _expect([item.get("ticker") for item in entries], TARGET_UNIVERSE, "dividend_review.per_ticker tickers")


def _validate_split_authority_freeze_artifact(artifact: Mapping[str, Any]) -> None:
    if not isinstance(artifact, Mapping):
        raise DividendProviderEvidenceRequestApprovalError("split_authority_freeze_artifact missing")
    expected = {
        "artifact_kind": split_freeze.ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN,
        "freeze_status": split_freeze.SPLIT_EVENT_AUTHORITY_FROZEN,
        "authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, f"split_freeze.{field}")
    _expect_true(artifact.get("split_event_authority_created"), "split_freeze.split_event_authority_created")
    _expect_true(artifact.get("split_event_authority_frozen"), "split_freeze.split_event_authority_frozen")
    _expect_false(artifact.get("split_provider_evidence_rerun_performed"), "split_freeze.split_provider_evidence_rerun_performed")


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "generated": False,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES
    ]


def per_ticker_dividend_provider_evidence_request_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_dividend_provider_evidence_request_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_request_entries(
    dividend_candidate_review_package: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_entries = dividend_candidate_review_package.get("per_ticker_dividend_event_review_entries", [])
    entries: list[dict[str, Any]] = []
    for source in source_entries:
        ticker = source["ticker"]
        entry = {
            "ticker": ticker,
            "dividend_event_candidate_status": dividend_review.candidate_service.DIVIDEND_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "dividend_event_review_status": dividend_review.READY_FOR_OPERATOR_ASSESSMENT,
            "dividend_provider_evidence_request_status": AUTHORIZED_NOT_EXECUTED,
            "dividend_provider_evidence_execution_status": NOT_EXECUTED,
            "dividend_provider_evidence_results_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "dividend_event_freeze_status": NOT_FROZEN,
            "split_event_authority_status": "FROZEN",
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_dividend_event_candidate_digest": source["per_ticker_dividend_event_candidate_digest"],
            "source_dividend_event_review_digest": source["per_ticker_dividend_event_review_digest"],
            "source_split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
            "source_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        }
        entry["per_ticker_dividend_provider_evidence_request_approval_digest"] = (
            per_ticker_dividend_provider_evidence_request_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    blockers = [item for item in failed if item.get("severity") == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "dividend_provider_evidence_request_authorized_by_operator": not failed,
        "ready_for_dividend_provider_evidence_execution": not failed,
        "dividend_provider_evidence_executed": False,
        "dividend_event_authority_authorized": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_authorized": True,
        "split_event_authority_frozen": True,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _base_artifact(
    *,
    dividend_candidate_review_package: Mapping[str, Any],
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "schema_version": SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1,
        "approval_status": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED,
        "approval_scope": READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "dividend_provider_evidence_request_authorized": True,
        "ready_for_dividend_provider_evidence_execution": True,
        "dividend_provider_evidence_executed": False,
        "dividend_provider_evidence_results_created": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": True,
        "split_provider_evidence_request_authorized": True,
        "split_provider_evidence_executed": True,
        "split_provider_evidence_results_created": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_provider_evidence_rerun_performed": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "post_identity_freeze_registry_inventory_approved": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "identity_authority_scope": "IDENTITY_AUTHORITY_ONLY",
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "acquisition_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "walk_forward_rerun_performed": False,
        "label_regeneration_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "live_ticker_validation_results_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "dividend_provider_evidence_request_objective": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "dividend_provider_evidence_request_scope": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "dividend_provider_evidence_authority_scope": DIVIDEND_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "dividend_provider_evidence_execution_status": DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_STATUS,
        "read_only_request_policy": deepcopy(READ_ONLY_REQUEST_POLICY),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "per_ticker_dividend_provider_evidence_request_approvals": _per_ticker_request_entries(
            dividend_candidate_review_package
        ),
        "operator_attestation": deepcopy(operator_attestation),
        "dividend_provider_evidence_execution_created": False,
        "dividend_event_authority_artifact_created": False,
        "dividend_event_authority_freeze_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }


def _planned_outputs_not_generated(artifact: Mapping[str, Any]) -> bool:
    outputs = artifact.get("planned_outputs")
    return isinstance(outputs, list) and len(outputs) == len(PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES) and all(
        item.get("generation_status") == PLANNED_NOT_GENERATED and item.get("generated") is False
        for item in outputs
    )


def _planned_outputs_research_only(artifact: Mapping[str, Any]) -> bool:
    outputs = artifact.get("planned_outputs")
    return isinstance(outputs, list) and len(outputs) == len(PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES) and all(
        item.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs
    )


def _approval_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact.get("operator_attestation", {})
    entries = artifact.get("per_ticker_dividend_provider_evidence_request_approvals", [])
    digests_present = isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(item.get("per_ticker_dividend_provider_evidence_request_approval_digest"), str)
        and len(item["per_ticker_dividend_provider_evidence_request_approval_digest"]) == 64
        for item in entries
    )
    return [
        _check("dividend_candidate_review_digest_matches_expected", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_authority_candidate_review_package_digest")),
        _check("dividend_candidate_review_has_zero_blockers", 0, artifact.get("source_dividend_candidate_review_blocker_count")),
        _check("dividend_candidate_digest_matches_expected", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, artifact.get("dividend_event_authority_candidate_digest")),
        _check("split_event_authority_freeze_digest_bound", EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("split_event_authority_freeze_digest")),
        _check("split_evidence_results_review_digest_bound", EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("split_event_evidence_results_review_package_digest")),
        _check("corporate_action_plan_approval_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, artifact.get("corporate_action_authority_plan_approval_digest")),
        _check("registry_inventory_approval_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, artifact.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("identity_freeze_digest_bound", EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        _check("target_universe_count_12", 12, artifact.get("target_universe_count")),
        _check("target_universe_matches_dividend_candidate_universe", TARGET_UNIVERSE, artifact.get("target_universe")),
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_DIVIDEND_PROVIDER_EVIDENCE_REQUEST, operator.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        _check("operator_confirms_dividend_candidate_review_digest", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, operator.get("operator_confirms_dividend_candidate_review_package_digest")),
        _check("operator_confirms_dividend_candidate_digest", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, operator.get("operator_confirms_dividend_candidate_digest")),
        _check("operator_confirms_split_authority_freeze_digest", EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, operator.get("operator_confirms_split_event_authority_freeze_digest")),
        _check("operator_confirms_split_evidence_results_review_digest", EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, operator.get("operator_confirms_split_evidence_results_review_package_digest")),
        _check("operator_confirms_corporate_action_plan_approval_digest", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, operator.get("operator_confirms_corporate_action_plan_approval_digest")),
        _check("operator_confirms_registry_inventory_approval_digest", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, operator.get("operator_confirms_registry_inventory_approval_digest")),
        _check("operator_confirms_identity_freeze_digest", EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, operator.get("operator_confirms_identity_freeze_digest")),
        _check("operator_confirms_target_universe", TARGET_UNIVERSE, operator.get("operator_confirms_target_universe")),
        _check("operator_confirms_request_scope_read_only_dividend_event_evidence_only", True, operator.get("operator_confirms_request_scope_read_only_dividend_event_evidence_only")),
        _check("operator_confirms_ready_for_dividend_provider_evidence_execution", True, operator.get("operator_confirms_ready_for_dividend_provider_evidence_execution")),
        _check("dividend_provider_evidence_request_authorized_true", True, artifact.get("dividend_provider_evidence_request_authorized")),
        _check("ready_for_dividend_provider_evidence_execution_true", True, artifact.get("ready_for_dividend_provider_evidence_execution")),
        _check("dividend_provider_evidence_executed_false", False, artifact.get("dividend_provider_evidence_executed")),
        _check("dividend_provider_evidence_results_created_false", False, artifact.get("dividend_provider_evidence_results_created")),
        _check("provider_requests_made_in_approval_false", False, artifact.get("provider_requests_made_in_approval")),
        _check("live_provider_transport_enabled_in_approval_false", False, artifact.get("live_provider_transport_enabled_in_approval")),
        _check("dividend_event_authority_created_false", False, artifact.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, artifact.get("dividend_event_authority_frozen")),
        _check("split_event_authority_created_true", True, artifact.get("split_event_authority_created")),
        _check("split_event_authority_frozen_true", True, artifact.get("split_event_authority_frozen")),
        _check("split_provider_evidence_rerun_performed_false", False, artifact.get("split_provider_evidence_rerun_performed")),
        _check("corporate_action_authority_created_false", False, artifact.get("corporate_action_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, artifact.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, artifact.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, artifact.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, artifact.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, artifact.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, artifact.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, artifact.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, artifact.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, artifact.get("predictive_experiment_rerun_performed")),
        _check("feature_matrix_regeneration_performed_false", False, artifact.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, artifact.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, artifact.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        _check("profitability_not_accepted", PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        _check("runtime_migration_approved_false", False, artifact.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, artifact.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, artifact.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, artifact.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, artifact.get("broker_execution")),
        _check("automatic_stitching_false", False, artifact.get("automatic_stitching")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(artifact)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(artifact)),
        _check("no_dividend_provider_evidence_execution_created", False, artifact.get("dividend_provider_evidence_execution_created")),
        _check("no_dividend_event_authority_artifact_created", False, artifact.get("dividend_event_authority_artifact_created")),
        _check("no_dividend_event_authority_freeze_created", False, artifact.get("dividend_event_authority_freeze_created")),
        _check("no_corporate_action_authority_artifact_created", False, artifact.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, artifact.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, artifact.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, artifact.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, artifact.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, artifact.get("runtime_migration_approval_created")),
    ]


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("dividend_provider_evidence_request_approval_digest", None)
    return payload


def dividend_provider_evidence_request_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic digest for the approval artifact."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_dividend_provider_evidence_request_approved_v1(
    *,
    dividend_candidate_review_package: dict[str, Any] | None = None,
    split_authority_freeze_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the read-only dividend evidence request approval artifact."""
    source_review = (
        dividend_candidate_review_package
        if dividend_candidate_review_package is not None
        else dividend_review.build_dividend_event_authority_candidate_review_package_v1()
    )
    source_split_freeze = (
        split_authority_freeze_artifact
        if split_authority_freeze_artifact is not None
        else _source_split_freeze_binding_artifact()
    )
    _validate_dividend_candidate_review_package(source_review)
    _validate_split_authority_freeze_artifact(source_split_freeze)
    _validate_operator_attestation(operator_attestation)
    artifact = _base_artifact(
        dividend_candidate_review_package=source_review,
        operator_attestation=operator_attestation,
    )
    artifact["source_dividend_candidate_review_blocker_count"] = source_review["review_summary"]["blocker_count"]
    artifact["source_dividend_candidate_review_total_checks"] = source_review["review_summary"].get("total_checks")
    artifact["source_dividend_candidate_review_passed_checks"] = source_review["review_summary"].get("passed_checks")
    checklist = _approval_checklist(artifact)
    artifact["approval_checklist"] = checklist
    artifact["approval_summary"] = _summary(checklist)
    artifact["dividend_provider_evidence_request_approval_digest"] = (
        dividend_provider_evidence_request_approval_digest_v1(artifact)
    )
    validate_dividend_provider_evidence_request_approved_v1(artifact)
    return artifact


def _validate_per_ticker_entries(approved_artifact: dict[str, Any]) -> None:
    entries = approved_artifact.get("per_ticker_dividend_provider_evidence_request_approvals")
    if not isinstance(entries, list) or len(entries) != 12:
        raise DividendProviderEvidenceRequestApprovalError("per_ticker_dividend_provider_evidence_request_approvals mismatch")
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for entry in entries:
        ticker = entry["ticker"]
        expected = {
            "dividend_event_candidate_status": dividend_review.candidate_service.DIVIDEND_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "dividend_event_review_status": dividend_review.READY_FOR_OPERATOR_ASSESSMENT,
            "dividend_provider_evidence_request_status": AUTHORIZED_NOT_EXECUTED,
            "dividend_provider_evidence_execution_status": NOT_EXECUTED,
            "dividend_provider_evidence_results_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "dividend_event_freeze_status": NOT_FROZEN,
            "split_event_authority_status": "FROZEN",
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
            "source_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        }
        for field, expected_value in expected.items():
            _expect(entry.get(field), expected_value, f"{ticker}.{field}")
        for field in ("corporate_action_authority_created", "acquisition_authorized", "dataset_generation_authorized"):
            _expect_false(entry.get(field), f"{ticker}.{field}")
        _expect_digest(entry.get("source_dividend_event_candidate_digest"), f"{ticker}.source_dividend_event_candidate_digest")
        _expect_digest(entry.get("source_dividend_event_review_digest"), f"{ticker}.source_dividend_event_review_digest")
        _expect_digest(
            entry.get("per_ticker_dividend_provider_evidence_request_approval_digest"),
            f"{ticker}.per_ticker_dividend_provider_evidence_request_approval_digest",
        )
        _expect(
            entry["per_ticker_dividend_provider_evidence_request_approval_digest"],
            per_ticker_dividend_provider_evidence_request_approval_digest_v1(entry),
            f"{ticker}.per_ticker_dividend_provider_evidence_request_approval_digest",
        )


def validate_dividend_provider_evidence_request_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate the dividend provider request approval and closed boundaries."""
    if not isinstance(approved_artifact, dict):
        raise DividendProviderEvidenceRequestApprovalError("approved_artifact must be a JSON object")
    _expect(approved_artifact.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED, "artifact_kind")
    _expect(approved_artifact.get("schema_version"), SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_V1, "schema_version")
    _expect(approved_artifact.get("approval_status"), DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED, "approval_status")
    _expect(approved_artifact.get("approval_scope"), READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY, "approval_scope")
    for field in (
        "created_offline",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_provider_evidence_request_authorized",
        "ready_for_dividend_provider_evidence_execution",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "corporate_action_authority_plan_approved",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_provider_transport_enabled_in_approval",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "dividend_provider_evidence_execution_created",
        "dividend_event_authority_artifact_created",
        "dividend_event_authority_freeze_created",
        "corporate_action_authority_artifact_created",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    expected_fields = {
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "identity_authority_scope": "IDENTITY_AUTHORITY_ONLY",
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "live_ticker_validation_results_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "dividend_provider_evidence_request_objective": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_OBJECTIVE,
        "dividend_provider_evidence_request_scope": DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE,
        "dividend_provider_evidence_authority_scope": DIVIDEND_PROVIDER_EVIDENCE_AUTHORITY_SCOPE,
        "dividend_provider_evidence_execution_status": DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_STATUS,
        "read_only_request_policy": READ_ONLY_REQUEST_POLICY,
        "planned_output_count": len(PLANNED_DIVIDEND_EVIDENCE_OUTPUT_NAMES),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }
    for field, expected in expected_fields.items():
        _expect(approved_artifact.get(field), expected, field)
    if not _planned_outputs_not_generated(approved_artifact):
        raise DividendProviderEvidenceRequestApprovalError("planned_outputs_not_generated mismatch")
    if not _planned_outputs_research_only(approved_artifact):
        raise DividendProviderEvidenceRequestApprovalError("planned_outputs_research_only mismatch")
    _validate_operator_attestation(approved_artifact.get("operator_attestation", {}))
    _validate_per_ticker_entries(approved_artifact)
    if [item.get("check_id") for item in approved_artifact.get("approval_checklist", [])] != REQUIRED_APPROVAL_CHECK_IDS:
        raise DividendProviderEvidenceRequestApprovalError("approval_checklist check IDs mismatch")
    failed = [item for item in approved_artifact["approval_checklist"] if item.get("status") != PASS]
    if failed:
        raise DividendProviderEvidenceRequestApprovalError(f"approval checklist failed: {failed[0]['check_id']}")
    _expect(approved_artifact.get("approval_summary"), _summary(approved_artifact["approval_checklist"]), "approval_summary")
    digest = approved_artifact.get("dividend_provider_evidence_request_approval_digest")
    _expect_digest(digest, "dividend_provider_evidence_request_approval_digest")
    _expect(digest, dividend_provider_evidence_request_approval_digest_v1(approved_artifact), "dividend_provider_evidence_request_approval_digest")
    return {
        "status": "DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "dividend_provider_evidence_request_approval_digest": digest,
        "target_universe_count": approved_artifact["target_universe_count"],
        "total_checks": approved_artifact["approval_summary"]["total_checks"],
        "passed_checks": approved_artifact["approval_summary"]["passed_checks"],
        "failed_checks": approved_artifact["approval_summary"]["failed_checks"],
        "blocker_count": approved_artifact["approval_summary"]["blocker_count"],
    }


def build_dividend_provider_evidence_request_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized Markdown status view for the approval artifact."""
    validation = validate_dividend_provider_evidence_request_approved_v1(approved_artifact)
    lines = [
        "# MarketFlow Dividend Provider Evidence Request Approval Status",
        "",
        "## Title",
        "- Dividend Provider Evidence Request Approval Ceremony v1.",
        "",
        "## Approved Dividend Provider Evidence Request",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval digest: `{validation['dividend_provider_evidence_request_approval_digest']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        "",
        "## Operator Attestation",
        f"- Operator decision: `{approved_artifact['operator_attestation']['operator_decision']}`",
        f"- Operator reference: `{approved_artifact['operator_attestation']['operator_reference']}`",
        "- Operator attestation phrase matched exactly.",
        "",
        "## Source Dividend Candidate Review Package",
        f"- Review digest: `{approved_artifact['dividend_event_authority_candidate_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['dividend_event_authority_candidate_digest']}`",
        "",
        "## Source Split Authority Freeze",
        f"- Split freeze digest: `{approved_artifact['split_event_authority_freeze_digest']}`",
        f"- Split evidence review digest: `{approved_artifact['split_event_evidence_results_review_package_digest']}`",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Approval Scope",
        f"- `{READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUEST_APPROVAL_ONLY}`.",
        "",
        "## Read-Only Provider Request Boundary",
        "- This approves a future read-only dividend evidence request only.",
        "- No provider request was made in this approval.",
        "",
        "## Dividend Evidence Execution Boundary",
        "- Dividend provider evidence execution remains `NOT_EXECUTED`.",
        "",
        "## Dividend Authority Boundary",
        "- Dividend event authority remains not created and not frozen.",
        "",
        "## Split Authority Boundary",
        "- Split event authority remains frozen and unchanged.",
        "",
        "## Corporate-Action Authority Boundary",
        "- Corporate-action authority remains not created.",
        "",
        "## Acquisition Boundary",
        "- Acquisition remains not authorized.",
        "",
        "## Dataset Boundary",
        "- Dataset generation remains not authorized.",
        "",
        "## Predictive/Profitability Boundary",
        "- Predictive usefulness and profitability remain not accepted.",
        "",
        "## Runtime Boundary",
        "- Runtime, strategy, paper trading, and broker execution remain not authorized.",
        "",
        "## Approval Checklist Summary",
        f"- Total checks: `{approved_artifact['approval_summary']['total_checks']}`",
        f"- Passed checks: `{approved_artifact['approval_summary']['passed_checks']}`",
        f"- Failed checks: `{approved_artifact['approval_summary']['failed_checks']}`",
        f"- Blocker count: `{approved_artifact['approval_summary']['blocker_count']}`",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"- {item}." for item in REMAINING_REQUIRED_TASKS)
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No live provider transport was enabled.",
            "- No dividend provider evidence execution occurred.",
            "- No dividend authority or freeze was created.",
            "- No API key or raw provider payload is stored by this artifact.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_dividend_provider_evidence_request_approved_v1(
    output_dir: str | Path,
    *,
    dividend_candidate_review_package: dict[str, Any] | None = None,
    split_authority_freeze_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write the approval artifact and Markdown status without overwriting files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    approved_artifact = build_dividend_provider_evidence_request_approved_v1(
        dividend_candidate_review_package=dividend_candidate_review_package,
        split_authority_freeze_artifact=split_authority_freeze_artifact,
        operator_attestation=operator_attestation,
    )
    json_path = output_path / "dividend_provider_evidence_request_approved.json"
    markdown_path = output_path / "dividend_provider_evidence_request_approved.md"
    if json_path.exists() or markdown_path.exists():
        raise DividendProviderEvidenceRequestApprovalError("dividend provider evidence request approval output already exists")
    json_path.write_bytes(canonical_json_bytes(approved_artifact))
    markdown_path.write_text(
        build_dividend_provider_evidence_request_approved_markdown_v1(approved_artifact),
        encoding="utf-8",
    )
    validation = validate_dividend_provider_evidence_request_approved_v1(approved_artifact)
    return {
        "artifact": approved_artifact,
        "validation": validation,
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
