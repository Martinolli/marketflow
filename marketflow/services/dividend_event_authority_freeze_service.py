"""Offline dividend-event-only authority freeze ceremony for the expanded universe."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_policy_reconciliation_approval_service as approval


ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN = "DIVIDEND_EVENT_AUTHORITY_FROZEN"
SCHEMA_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1 = "dividend_event_authority_freeze_v1"
DIVIDEND_EVENT_AUTHORITY_FROZEN = "DIVIDEND_EVENT_AUTHORITY_FROZEN"
DIVIDEND_EVENT_AUTHORITY_ONLY = "DIVIDEND_EVENT_AUTHORITY_ONLY"
OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY = "FREEZE_DIVIDEND_EVENT_AUTHORITY"
OPERATOR_ATTESTATION_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1 = (
    "dividend_event_authority_freeze_attestation_v1"
)
REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE = (
    "FREEZE DIVIDEND EVENT AUTHORITY MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ "
    "WMT CAT LMT DIVIDEND_EVENT_AUTHORITY_ONLY"
)

EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST = (
    "96f146e4ce0257c8cf84c8b6d26e620ba485a8c3c575e4335c42be36e3870d62"
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    approval.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    approval.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST = (
    approval.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    approval.review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    approval.review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    approval.review.approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    approval.review.approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    approval.review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    approval.review.approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    approval.review.approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    approval.review.approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(approval.EXPECTED_TARGET_UNIVERSE)
ZERO_DIVIDEND_TICKERS = list(approval.ZERO_DIVIDEND_TICKERS)
EXPECTED_PER_TICKER = dict(approval.review.evidence.EXPECTED_PER_TICKER)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE = (
    "DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE"
)
DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY = (
    "DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY"
)
ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY = (
    "ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY"
)
DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE = (
    "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
)

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_authority_scope_dividend_event_only",
    "operator_confirms_zero_dividend_tickers_amzn_tsla",
    "operator_confirms_total_return_not_assumed",
    "operator_confirms_dividend_reinvestment_not_assumed",
    "operator_confirms_dataset_generation_not_authorized",
    "operator_confirms_predictive_use_not_authorized",
    "operator_confirms_no_dividend_authority_provider_rerun",
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_split_authority_remains_frozen",
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

REQUIRED_FREEZE_CHECK_IDS = [
    "dividend_policy_reconciliation_approval_digest_matches_expected",
    "dividend_policy_reconciliation_approval_has_zero_blockers",
    "dividend_policy_reconciliation_review_digest_bound",
    "dividend_evidence_results_review_digest_bound",
    "dividend_provider_evidence_execution_digest_bound",
    "dividend_provider_evidence_request_approval_digest_bound",
    "dividend_policy_reconciliation_report_digest_bound",
    "dividend_candidate_review_digest_bound",
    "dividend_candidate_digest_bound",
    "split_authority_freeze_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "registry_inventory_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_dividend_policy_approval_universe",
    "operator_decision_freeze",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_authority_scope_dividend_event_only",
    "operator_confirms_zero_dividend_tickers_amzn_tsla",
    "operator_confirms_dividend_evidence_collected_count_10",
    "operator_confirms_no_dividend_events_returned_count_2",
    "operator_confirms_total_return_not_assumed",
    "operator_confirms_dividend_reinvestment_not_assumed",
    "authority_scope_dividend_event_only",
    "dividend_event_authority_created_true",
    "dividend_event_authority_frozen_true",
    "per_ticker_dividend_authority_entries_12",
    "per_ticker_dividend_authority_freeze_digests_present",
    "zero_dividend_policy_for_amzn_tsla_preserved",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "dataset_generation_not_authorized",
    "predictive_use_not_authorized",
    "provider_requests_made_in_freeze_false",
    "live_provider_transport_enabled_in_freeze_false",
    "dividend_provider_evidence_rerun_performed_false",
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
    "ready_for_combined_corporate_action_readiness_review_true",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

REMAINING_REQUIRED_TASKS = [
    "combined_split_dividend_corporate_action_readiness_review_package",
    "corporate_action_authority_approval_if_separately_required",
    "acquisition_and_dataset_authority_chain",
]


class DividendEventAuthorityFreezeError(ValueError):
    """Raised when dividend authority freeze evidence or attestations are invalid."""


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


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise DividendEventAuthorityFreezeError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise DividendEventAuthorityFreezeError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise DividendEventAuthorityFreezeError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise DividendEventAuthorityFreezeError(f"{field} missing")


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "operator_confirms_dividend_policy_reconciliation_review_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_evidence_results_review_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "operator_confirms_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "operator_confirms_dividend_candidate_review_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def build_dividend_event_authority_freeze_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_dividend_policy_reconciliation_approval_digest: str,
    operator_confirms_dividend_policy_reconciliation_review_digest: str,
    operator_confirms_dividend_evidence_results_review_digest: str,
    operator_confirms_dividend_provider_evidence_execution_digest: str,
    operator_confirms_dividend_provider_evidence_request_approval_digest: str,
    operator_confirms_dividend_candidate_review_digest: str,
    operator_confirms_dividend_candidate_digest: str,
    operator_confirms_split_authority_freeze_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_authority_scope_dividend_event_only: bool,
    operator_confirms_zero_dividend_tickers_amzn_tsla: bool,
    operator_confirms_dividend_evidence_collected_count: int,
    operator_confirms_no_dividend_events_returned_count: int,
    operator_confirms_total_return_not_assumed: bool,
    operator_confirms_dividend_reinvestment_not_assumed: bool,
    operator_confirms_dataset_generation_not_authorized: bool,
    operator_confirms_predictive_use_not_authorized: bool,
    operator_confirms_no_dividend_authority_provider_rerun: bool,
    operator_confirms_no_provider_requests_in_freeze: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_split_authority_remains_frozen: bool,
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
    operator_decision: str = OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY,
) -> dict[str, Any]:
    """Build the non-secret operator attestation required for the freeze."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1
    }


def _validate_operator_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise DividendEventAuthorityFreezeError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY,
        "operator_attestation_phrase": REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dividend_evidence_collected_count": 10,
        "operator_confirms_no_dividend_events_returned_count": 2,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise DividendEventAuthorityFreezeError(f"{field} required")


def _build_expected_policy_approval_artifact() -> dict[str, Any]:
    """Reconstruct the already-approved source offline when it is not injected."""
    values: dict[str, Any] = {
        "operator_reference": "USER_REQUEST",
        "operator_attestation_timestamp_utc": "2026-08-13T02:57:04Z",
        "operator_attestation_phrase": approval.REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE,
        **approval._expected_digest_confirmations(),
        "operator_confirms_target_universe": approval.EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dividend_evidence_collected_count": 10,
        "operator_confirms_no_dividend_events_returned_count": 2,
        **{field: True for field in approval.OPERATOR_BOOLEAN_CONFIRMATION_FIELDS},
        "operator_decision": approval.OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION,
    }
    return approval.build_dividend_policy_reconciliation_approved_v1(
        operator_attestation=approval.build_dividend_policy_reconciliation_approval_attestation_v1(
            **values
        )
    )


def _validate_source_approval(source: Mapping[str, Any]) -> None:
    if not isinstance(source, dict):
        raise DividendEventAuthorityFreezeError(
            "dividend_policy_reconciliation_approval_artifact missing"
        )
    validation = approval.validate_dividend_policy_reconciliation_approved_v1(source)
    _expect(
        source.get("dividend_policy_reconciliation_approval_digest"),
        EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "source_approval.dividend_policy_reconciliation_approval_digest",
    )
    _expect(
        validation.get("dividend_policy_reconciliation_approval_digest"),
        EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "source_approval.dividend_policy_reconciliation_approval_digest",
    )
    _expect(validation.get("blocker_count"), 0, "source_approval.blocker_count")
    expected = {
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": ZERO_DIVIDEND_TICKERS,
        "total_return_assumed": False,
        "dividend_reinvestment_assumed": False,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
    }
    for field, value in expected.items():
        _expect(source.get(field), value, f"source_approval.{field}")


def per_ticker_dividend_event_authority_freeze_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_dividend_event_authority_freeze_digest", None)
    return semantic_digest(payload)


def _per_ticker_authority_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = source["per_ticker_policy_approval_entries"]
    rows_by_ticker = {row["ticker"]: row for row in source_rows}
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        source_row = rows_by_ticker[ticker]
        evidence_status, event_count = EXPECTED_PER_TICKER[ticker]
        zero_row = ticker in ZERO_DIVIDEND_TICKERS
        entry = {
            "ticker": ticker,
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_scope": DIVIDEND_EVENT_AUTHORITY_ONLY,
            "dividend_event_authority_classification": (
                DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY
                if zero_row
                else DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE
            ),
            "dividend_event_authority_created": True,
            "dividend_event_authority_frozen": True,
            "dividend_evidence_status": evidence_status,
            "dividend_event_count": event_count,
            "dividend_absence_policy_status": (
                ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY
                if zero_row
                else DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE
            ),
            "dividend_policy_reconciliation_status": "APPROVED_FOR_FREEZE_INPUT_ONLY",
            "total_return_policy_status": "NOT_ASSUMED",
            "dividend_reinvestment_policy_status": "NOT_ASSUMED",
            "canonical_dataset_impact_status": "NOT_AUTHORIZED_FOR_DATASET_GENERATION",
            "predictive_label_impact_status": "NOT_AUTHORIZED_FOR_PREDICTIVE_USE",
            "source_dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
            "source_dividend_evidence_results_review_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
            "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
            "source_dividend_event_candidate_review_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_dividend_event_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
            "source_per_ticker_policy_approval_digest": source_row[
                "per_ticker_dividend_policy_reconciliation_approval_digest"
            ],
            "split_event_authority_status": "FROZEN",
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_dividend_event_authority_freeze_digest"] = (
            per_ticker_dividend_event_authority_freeze_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_artifact(
    source: Mapping[str, Any], operator_attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1,
        "freeze_status": DIVIDEND_EVENT_AUTHORITY_FROZEN,
        "authority_scope": DIVIDEND_EVENT_AUTHORITY_ONLY,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "live_provider_transport_enabled_in_freeze": False,
        "dividend_provider_evidence_rerun_performed": False,
        "split_provider_evidence_rerun_performed": False,
        "dividend_provider_evidence_request_authorized": True,
        "dividend_provider_evidence_executed": True,
        "dividend_provider_evidence_results_created": True,
        "dividend_evidence_results_review_created": True,
        "dividend_policy_reconciliation_review_created": True,
        "dividend_policy_reconciliation_approved": True,
        "ready_for_dividend_event_authority_freeze": True,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "ready_for_combined_corporate_action_readiness_review": True,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "acquisition_generation_authorized": False,
        "canonical_dataset_authorized": False,
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
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_report_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_dividend_policy_reconciliation_approval_blocker_count": source[
            "approval_summary"
        ]["blocker_count"],
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": list(ZERO_DIVIDEND_TICKERS),
        "total_return_assumed": False,
        "dividend_reinvestment_assumed": False,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "per_ticker_dividend_event_authority": _per_ticker_authority_entries(source),
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "dividend_event_authority_frozen_by_operator": not failed,
        "authority_scope": DIVIDEND_EVENT_AUTHORITY_ONLY,
        "ready_for_combined_corporate_action_readiness_review": not failed,
        "dividend_event_authority_authorized": not failed,
        "dividend_event_authority_frozen": not failed,
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


def _freeze_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = artifact["operator_attestation"]
    entries = artifact["per_ticker_dividend_event_authority"]
    all_source_digests = all(
        attestation.get(field) == expected
        for field, expected in _expected_digest_confirmations().items()
    )
    digests_present = len(entries) == 12 and all(
        len(row.get("per_ticker_dividend_event_authority_freeze_digest", "")) == 64
        for row in entries
    )
    zero_policy = all(
        row["dividend_absence_policy_status"]
        == ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY
        for row in entries
        if row["ticker"] in ZERO_DIVIDEND_TICKERS
    )
    values: dict[str, tuple[Any, Any]] = {
        "dividend_policy_reconciliation_approval_digest_matches_expected": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST, artifact.get("dividend_policy_reconciliation_approval_digest")),
        "dividend_policy_reconciliation_approval_has_zero_blockers": (0, artifact.get("source_dividend_policy_reconciliation_approval_blocker_count")),
        "dividend_policy_reconciliation_review_digest_bound": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_policy_reconciliation_review_package_digest")),
        "dividend_evidence_results_review_digest_bound": (EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_evidence_results_review_package_digest")),
        "dividend_provider_evidence_execution_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST, artifact.get("dividend_provider_evidence_execution_digest")),
        "dividend_provider_evidence_request_approval_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, artifact.get("dividend_provider_evidence_request_approval_digest")),
        "dividend_policy_reconciliation_report_digest_bound": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST, artifact.get("dividend_policy_reconciliation_report_digest")),
        "dividend_candidate_review_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_authority_candidate_review_package_digest")),
        "dividend_candidate_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, artifact.get("dividend_event_authority_candidate_digest")),
        "split_authority_freeze_digest_bound": (EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("split_event_authority_freeze_digest")),
        "corporate_action_plan_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, artifact.get("corporate_action_authority_plan_approval_digest")),
        "registry_inventory_approval_digest_bound": (EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, artifact.get("post_identity_freeze_registry_inventory_approval_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_dividend_policy_approval_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_freeze": (OPERATOR_DECISION_FREEZE_DIVIDEND_EVENT_AUTHORITY, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_DIVIDEND_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all_source_digests),
        "operator_confirms_authority_scope_dividend_event_only": (True, attestation.get("operator_confirms_authority_scope_dividend_event_only")),
        "operator_confirms_zero_dividend_tickers_amzn_tsla": (True, attestation.get("operator_confirms_zero_dividend_tickers_amzn_tsla")),
        "operator_confirms_dividend_evidence_collected_count_10": (10, attestation.get("operator_confirms_dividend_evidence_collected_count")),
        "operator_confirms_no_dividend_events_returned_count_2": (2, attestation.get("operator_confirms_no_dividend_events_returned_count")),
        "operator_confirms_total_return_not_assumed": (True, attestation.get("operator_confirms_total_return_not_assumed")),
        "operator_confirms_dividend_reinvestment_not_assumed": (True, attestation.get("operator_confirms_dividend_reinvestment_not_assumed")),
        "authority_scope_dividend_event_only": (DIVIDEND_EVENT_AUTHORITY_ONLY, artifact.get("authority_scope")),
        "dividend_event_authority_created_true": (True, artifact.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_true": (True, artifact.get("dividend_event_authority_frozen")),
        "per_ticker_dividend_authority_entries_12": (12, len(entries)),
        "per_ticker_dividend_authority_freeze_digests_present": (True, digests_present),
        "zero_dividend_policy_for_amzn_tsla_preserved": (True, zero_policy),
        "total_return_not_assumed": (False, artifact.get("total_return_assumed")),
        "dividend_reinvestment_not_assumed": (False, artifact.get("dividend_reinvestment_assumed")),
        "dataset_generation_not_authorized": (False, artifact.get("dataset_generation_authorized")),
        "predictive_use_not_authorized": (False, artifact.get("predictive_use_authorized")),
    }
    boolean_checks = {
        "provider_requests_made_in_freeze_false": (False, "provider_requests_made_in_freeze"),
        "live_provider_transport_enabled_in_freeze_false": (False, "live_provider_transport_enabled_in_freeze"),
        "dividend_provider_evidence_rerun_performed_false": (False, "dividend_provider_evidence_rerun_performed"),
        "split_event_authority_created_true": (True, "split_event_authority_created"),
        "split_event_authority_frozen_true": (True, "split_event_authority_frozen"),
        "split_provider_evidence_rerun_performed_false": (False, "split_provider_evidence_rerun_performed"),
        "corporate_action_authority_created_false": (False, "corporate_action_authority_created"),
        "new_ticker_acquisition_authorized_false": (False, "new_ticker_acquisition_authorized"),
        "dataset_generation_authorized_false": (False, "dataset_generation_authorized"),
        "acquisition_generation_authorized_false": (False, "acquisition_generation_authorized"),
        "canonical_dataset_authorized_false": (False, "canonical_dataset_authorized"),
        "registry_approval_created_false": (False, "registry_approval_created"),
        "additional_predictive_evidence_execution_authorized_false": (False, "additional_predictive_evidence_execution_authorized"),
        "additional_predictive_evidence_executed_false": (False, "additional_predictive_evidence_executed"),
        "predictive_experiment_rerun_authorized_false": (False, "predictive_experiment_rerun_authorized"),
        "new_strategy_scoring_performed_false": (False, "new_strategy_scoring_performed"),
        "trade_recommendations_generated_false": (False, "trade_recommendations_generated"),
        "runtime_migration_approved_false": (False, "runtime_migration_approved"),
        "automatic_stitching_false": (False, "automatic_stitching"),
        "ready_for_combined_corporate_action_readiness_review_true": (True, "ready_for_combined_corporate_action_readiness_review"),
        "no_corporate_action_authority_artifact_created": (False, "corporate_action_authority_artifact_created"),
        "no_acquisition_authorization_created": (False, "acquisition_authorization_created"),
        "no_dataset_generation_authorization_created": (False, "dataset_generation_authorization_created"),
        "no_predictive_usefulness_acceptance_artifact_created": (False, "predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": (False, "profitability_acceptance_created"),
        "no_runtime_migration_approval_created": (False, "runtime_migration_approval_created"),
    }
    values.update(
        {check_id: (expected, artifact.get(field)) for check_id, (expected, field) in boolean_checks.items()}
    )
    values.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
            "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
        }
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_FREEZE_CHECK_IDS]


def _digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("dividend_event_authority_freeze_digest", None)
    return payload


def dividend_event_authority_freeze_digest_v1(artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the freeze artifact."""
    return semantic_digest(_digest_payload(artifact))


def build_dividend_event_authority_frozen_v1(
    *,
    dividend_policy_reconciliation_approval_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build dividend-event-only authority after validating prior approval and attestation."""
    source = (
        dividend_policy_reconciliation_approval_artifact
        if dividend_policy_reconciliation_approval_artifact is not None
        else _build_expected_policy_approval_artifact()
    )
    _validate_source_approval(source)
    _validate_operator_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    checklist = _freeze_checklist(artifact)
    artifact["freeze_checklist"] = checklist
    artifact["freeze_summary"] = _summary(checklist)
    artifact["dividend_event_authority_freeze_digest"] = (
        dividend_event_authority_freeze_digest_v1(artifact)
    )
    validate_dividend_event_authority_frozen_v1(artifact)
    return artifact


def _validate_per_ticker_entries(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_dividend_event_authority")
    if not isinstance(entries, list) or len(entries) != 12:
        raise DividendEventAuthorityFreezeError(
            "per_ticker_dividend_event_authority mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        evidence_status, event_count = EXPECTED_PER_TICKER[ticker]
        zero_row = ticker in ZERO_DIVIDEND_TICKERS
        expected = {
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_scope": DIVIDEND_EVENT_AUTHORITY_ONLY,
            "dividend_event_authority_classification": (
                DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY
                if zero_row
                else DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE
            ),
            "dividend_event_authority_created": True,
            "dividend_event_authority_frozen": True,
            "dividend_evidence_status": evidence_status,
            "dividend_event_count": event_count,
            "dividend_absence_policy_status": (
                ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY
                if zero_row
                else DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE
            ),
            "dividend_policy_reconciliation_status": "APPROVED_FOR_FREEZE_INPUT_ONLY",
            "total_return_policy_status": "NOT_ASSUMED",
            "dividend_reinvestment_policy_status": "NOT_ASSUMED",
            "canonical_dataset_impact_status": "NOT_AUTHORIZED_FOR_DATASET_GENERATION",
            "predictive_label_impact_status": "NOT_AUTHORIZED_FOR_PREDICTIVE_USE",
            "source_dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
            "source_dividend_evidence_results_review_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
            "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
            "source_dividend_event_candidate_review_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_dividend_event_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
            "split_event_authority_status": "FROZEN",
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        _expect_digest(
            row.get("source_per_ticker_policy_approval_digest"),
            f"{ticker}.source_per_ticker_policy_approval_digest",
        )
        digest = row.get("per_ticker_dividend_event_authority_freeze_digest")
        _expect_digest(digest, f"{ticker}.per_ticker_dividend_event_authority_freeze_digest")
        _expect(
            digest,
            per_ticker_dividend_event_authority_freeze_digest_v1(row),
            f"{ticker}.per_ticker_dividend_event_authority_freeze_digest",
        )


def validate_dividend_event_authority_frozen_v1(
    frozen_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate the dividend authority freeze and every closed adjacent boundary."""
    if not isinstance(frozen_artifact, dict):
        raise DividendEventAuthorityFreezeError("frozen_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_AUTHORITY_FROZEN,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_AUTHORITY_FREEZE_V1,
        "freeze_status": DIVIDEND_EVENT_AUTHORITY_FROZEN,
        "authority_scope": DIVIDEND_EVENT_AUTHORITY_ONLY,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_report_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": ZERO_DIVIDEND_TICKERS,
        "total_return_assumed": False,
        "dividend_reinvestment_assumed": False,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }
    for field, value in expected.items():
        _expect(frozen_artifact.get(field), value, field)
    true_fields = (
        "created_offline",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "dividend_evidence_results_review_created",
        "dividend_policy_reconciliation_review_created",
        "dividend_policy_reconciliation_approved",
        "ready_for_dividend_event_authority_freeze",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "corporate_action_authority_plan_approved",
        "ready_for_combined_corporate_action_readiness_review",
        "research_only",
    )
    false_fields = (
        "provider_requests_made_in_freeze",
        "live_provider_transport_enabled_in_freeze",
        "dividend_provider_evidence_rerun_performed",
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
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "corporate_action_authority_artifact_created",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    )
    for field in true_fields:
        _expect_true(frozen_artifact.get(field), field)
    for field in false_fields:
        _expect_false(frozen_artifact.get(field), field)
    _validate_operator_attestation(frozen_artifact.get("operator_attestation", {}))
    _validate_per_ticker_entries(frozen_artifact)
    _expect(
        [row.get("check_id") for row in frozen_artifact.get("freeze_checklist", [])],
        REQUIRED_FREEZE_CHECK_IDS,
        "freeze_checklist check IDs",
    )
    if any(row.get("status") != PASS for row in frozen_artifact["freeze_checklist"]):
        raise DividendEventAuthorityFreezeError("freeze checklist failed")
    _expect(
        frozen_artifact.get("freeze_summary"),
        _summary(frozen_artifact["freeze_checklist"]),
        "freeze_summary",
    )
    digest = frozen_artifact.get("dividend_event_authority_freeze_digest")
    _expect_digest(digest, "dividend_event_authority_freeze_digest")
    _expect(
        digest,
        dividend_event_authority_freeze_digest_v1(frozen_artifact),
        "dividend_event_authority_freeze_digest",
    )
    return {
        "status": "DIVIDEND_EVENT_AUTHORITY_FROZEN_VALID",
        "artifact_kind": frozen_artifact["artifact_kind"],
        "freeze_status": frozen_artifact["freeze_status"],
        "authority_scope": frozen_artifact["authority_scope"],
        "dividend_event_authority_freeze_digest": digest,
        "target_universe_count": frozen_artifact["target_universe_count"],
        "dividend_evidence_collected_count": frozen_artifact[
            "dividend_evidence_collected_count"
        ],
        "no_dividend_events_returned_count": frozen_artifact[
            "no_dividend_events_returned_count"
        ],
        **{
            key: frozen_artifact["freeze_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_dividend_event_authority_frozen_markdown_v1(
    frozen_artifact: dict[str, Any],
) -> str:
    """Render a sanitized Markdown status for the dividend authority freeze."""
    validation = validate_dividend_event_authority_frozen_v1(frozen_artifact)
    lines = [
        "# MarketFlow Dividend Event Authority Freeze Status",
        "",
        "## Title",
        "- Dividend Event Authority Freeze Ceremony v1.",
        "",
        "## Frozen Dividend Event Authority",
        f"- Artifact/status/scope: `{frozen_artifact['artifact_kind']}` / `{frozen_artifact['freeze_status']}` / `{frozen_artifact['authority_scope']}`",
        f"- Freeze digest: `{validation['dividend_event_authority_freeze_digest']}`",
        "",
        "## Operator Attestation",
        f"- Decision/reference/timestamp: `{frozen_artifact['operator_attestation']['operator_decision']}` / `{frozen_artifact['operator_attestation']['operator_reference']}` / `{frozen_artifact['operator_attestation']['operator_attestation_timestamp_utc']}`",
        "",
        "## Source Dividend Policy Reconciliation Approval",
        f"- Approval digest: `{frozen_artifact['dividend_policy_reconciliation_approval_digest']}`",
        "",
        "## Source Dividend Evidence Results",
        f"- Review/execution digests: `{frozen_artifact['dividend_event_evidence_results_review_package_digest']}` / `{frozen_artifact['dividend_provider_evidence_execution_digest']}`",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Frozen Per-Ticker Dividend Authority Summary",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['dividend_event_authority_classification']}`, `{row['dividend_event_count']}` events."
        for row in frozen_artifact["per_ticker_dividend_event_authority"]
    )
    lines.extend(
        [
            "",
            "## Zero-Dividend Response Absence Policy",
            "- AMZN and TSLA are frozen with the approved source-specific zero-row absence policy; no broader standalone absence authority is created.",
            "",
            "## Total Return and Reinvestment Boundary",
            "- Total return and dividend reinvestment remain not assumed.",
            "",
            "## Canonical Dataset Impact Boundary",
            "- Dataset generation and canonical dataset impact remain not authorized.",
            "",
            "## Predictive Label Impact Boundary",
            "- Predictive label/use impact remains not authorized.",
            "",
            "## Authority Scope",
            f"- `{DIVIDEND_EVENT_AUTHORITY_ONLY}`.",
            "",
            "## Split Authority Boundary",
            "- Split authority remains frozen and unchanged; no split evidence rerun occurred.",
            "",
            "## Corporate-Action Authority Boundary",
            "- Corporate-action authority remains not created.",
            "",
            "## Acquisition Boundary",
            "- New ticker acquisition remains not authorized.",
            "",
            "## Dataset Boundary",
            "- Dataset and acquisition generation remain not authorized.",
            "",
            "## Predictive/Profitability Boundary",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Runtime Boundary",
            "- Runtime, strategy, paper trading, and broker execution remain not authorized.",
            "",
            "## Freeze Checklist Summary",
            f"- Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`.",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"- {task}." for task in REMAINING_REQUIRED_TASKS)
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider request, evidence rerun, raw payload commit, API-key handling, downstream authority, or runtime activation occurred in this freeze.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_dividend_event_authority_frozen_v1(
    output_dir: str | Path,
    *,
    dividend_policy_reconciliation_approval_artifact: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write JSON and Markdown freeze evidence without overwriting either output."""
    artifact = build_dividend_event_authority_frozen_v1(
        dividend_policy_reconciliation_approval_artifact=(
            dividend_policy_reconciliation_approval_artifact
        ),
        operator_attestation=operator_attestation,
    )
    output_path = Path(output_dir)
    json_path = output_path / "dividend_event_authority_frozen_v1.json"
    markdown_path = output_path / "dividend_event_authority_frozen_v1.md"
    if json_path.exists() or markdown_path.exists():
        raise DividendEventAuthorityFreezeError(
            "dividend event authority freeze output already exists"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(artifact))
    markdown_path.write_text(
        build_dividend_event_authority_frozen_markdown_v1(artifact), encoding="utf-8"
    )
    return {
        "artifact": artifact,
        "validation": validate_dividend_event_authority_frozen_v1(artifact),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
