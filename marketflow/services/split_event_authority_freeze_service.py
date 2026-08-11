"""Offline split event authority freeze ceremony for the expanded universe."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import split_event_evidence_results_review_service as review
from marketflow.services import split_provider_evidence_request_approval_service as approval


ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN = "SPLIT_EVENT_AUTHORITY_FROZEN"
SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1 = "split_event_authority_freeze_v1"
SPLIT_EVENT_AUTHORITY_FROZEN = "SPLIT_EVENT_AUTHORITY_FROZEN"
SPLIT_EVENT_AUTHORITY_ONLY = "SPLIT_EVENT_AUTHORITY_ONLY"
OPERATOR_DECISION_FREEZE_SPLIT_EVENT_AUTHORITY = "FREEZE_SPLIT_EVENT_AUTHORITY"
OPERATOR_ATTESTATION_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1 = (
    "split_event_authority_freeze_attestation_v1"
)
REQUIRED_SPLIT_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE = (
    "FREEZE SPLIT EVENT AUTHORITY MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT "
    "SPLIT_EVENT_AUTHORITY_ONLY"
)

EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "98797d5bbcbd9754fe2f064a77e6acbe047d3841d82b8a38114935c734f2aac3"
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    review.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(review.EXPECTED_TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_AUTHORIZED = review.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

SPLIT_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_SPLIT_EVIDENCE = (
    "SPLIT_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_SPLIT_EVIDENCE"
)
SPLIT_EVENT_AUTHORITY_FROZEN_WITH_NO_SPLIT_EVENTS_RETURNED_POLICY = (
    "SPLIT_EVENT_AUTHORITY_FROZEN_WITH_NO_SPLIT_EVENTS_RETURNED_POLICY"
)
APPLIED_IF_NO_SPLIT_EVENTS_RETURNED = "APPLIED_IF_NO_SPLIT_EVENTS_RETURNED"
NOT_APPLIED_PROVIDER_SPLIT_EVIDENCE_COLLECTED = (
    "NOT_APPLIED_PROVIDER_SPLIT_EVIDENCE_COLLECTED"
)

PER_TICKER_SPLIT_AUTHORITY_CLASSIFICATION = {
    ticker: (
        SPLIT_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_SPLIT_EVIDENCE
        if status == review.execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY
        else SPLIT_EVENT_AUTHORITY_FROZEN_WITH_NO_SPLIT_EVENTS_RETURNED_POLICY
    )
    for ticker, status in review.EXPECTED_PER_TICKER_STATUS.items()
}

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_authority_scope_split_event_only",
    "operator_confirms_no_split_authority_provider_rerun",
    "operator_confirms_no_provider_requests_in_freeze",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_dividend_provider_evidence_request_authorized",
    "operator_confirms_no_dividend_event_authority_created",
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
    "split_evidence_results_review_digest_matches_expected",
    "split_evidence_results_review_has_zero_blockers",
    "split_provider_evidence_execution_digest_matches_expected",
    "split_provider_evidence_request_approval_digest_matches_expected",
    "split_candidate_review_digest_matches_expected",
    "split_candidate_digest_matches_expected",
    "dividend_candidate_review_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "registry_inventory_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_reviewed_evidence",
    "operator_decision_freeze",
    "operator_attestation_phrase_matches",
    "operator_confirms_split_evidence_results_review_digest",
    "operator_confirms_split_provider_evidence_execution_digest",
    "operator_confirms_split_request_approval_digest",
    "operator_confirms_split_candidate_review_digest",
    "operator_confirms_split_candidate_digest",
    "operator_confirms_dividend_candidate_review_digest",
    "operator_confirms_authority_scope_split_event_only",
    "operator_confirms_split_evidence_collected_count_7",
    "operator_confirms_no_split_events_returned_count_5",
    "authority_scope_split_event_only",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "per_ticker_split_authority_entries_12",
    "per_ticker_split_authority_freeze_digests_present",
    "split_evidence_collected_count_7",
    "no_split_events_returned_count_5",
    "no_split_events_absence_policy_preserved",
    "provider_requests_made_in_freeze_false",
    "live_provider_transport_enabled_in_freeze_false",
    "split_provider_evidence_rerun_performed_false",
    "dividend_provider_evidence_request_authorized_false",
    "dividend_provider_evidence_executed_false",
    "dividend_event_authority_created_false",
    "dividend_event_authority_frozen_false",
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
    "no_dividend_event_authority_artifact_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]

REMAINING_REQUIRED_TASKS = [
    "dividend_provider_evidence_request_approval",
    "dividend_provider_evidence_execution",
    "dividend_event_authority_freeze_ceremony",
    "combined_corporate_action_readiness_review",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
]


class SplitEventAuthorityFreezeError(ValueError):
    """Raised when the split event authority freeze artifact is invalid."""


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
        raise SplitEventAuthorityFreezeError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventAuthorityFreezeError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventAuthorityFreezeError(f"{field_name} must be false")


def _expect_digest(actual: Any, field_name: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise SplitEventAuthorityFreezeError(f"{field_name} missing")


def build_split_event_authority_freeze_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_split_evidence_results_review_package_digest: str,
    operator_confirms_split_provider_evidence_execution_digest: str,
    operator_confirms_split_provider_evidence_request_approval_digest: str,
    operator_confirms_split_candidate_review_package_digest: str,
    operator_confirms_split_candidate_digest: str,
    operator_confirms_dividend_candidate_review_package_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_authority_scope_split_event_only: bool,
    operator_confirms_split_evidence_collected_count: int,
    operator_confirms_no_split_events_returned_count: int,
    operator_confirms_no_split_authority_provider_rerun: bool,
    operator_confirms_no_provider_requests_in_freeze: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_dividend_provider_evidence_request_authorized: bool,
    operator_confirms_no_dividend_event_authority_created: bool,
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
    operator_decision: str = OPERATOR_DECISION_FREEZE_SPLIT_EVENT_AUTHORITY,
) -> dict[str, Any]:
    """Build the non-secret operator attestation required for the freeze."""
    return {
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1,
        "operator_reference": operator_reference,
        "operator_confirms_split_evidence_results_review_package_digest": operator_confirms_split_evidence_results_review_package_digest,
        "operator_confirms_split_provider_evidence_execution_digest": operator_confirms_split_provider_evidence_execution_digest,
        "operator_confirms_split_provider_evidence_request_approval_digest": operator_confirms_split_provider_evidence_request_approval_digest,
        "operator_confirms_split_candidate_review_package_digest": operator_confirms_split_candidate_review_package_digest,
        "operator_confirms_split_candidate_digest": operator_confirms_split_candidate_digest,
        "operator_confirms_dividend_candidate_review_package_digest": operator_confirms_dividend_candidate_review_package_digest,
        "operator_confirms_corporate_action_plan_approval_digest": operator_confirms_corporate_action_plan_approval_digest,
        "operator_confirms_registry_inventory_approval_digest": operator_confirms_registry_inventory_approval_digest,
        "operator_confirms_identity_freeze_digest": operator_confirms_identity_freeze_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_authority_scope_split_event_only": operator_confirms_authority_scope_split_event_only,
        "operator_confirms_split_evidence_collected_count": operator_confirms_split_evidence_collected_count,
        "operator_confirms_no_split_events_returned_count": operator_confirms_no_split_events_returned_count,
        "operator_confirms_no_split_authority_provider_rerun": operator_confirms_no_split_authority_provider_rerun,
        "operator_confirms_no_provider_requests_in_freeze": operator_confirms_no_provider_requests_in_freeze,
        "operator_confirms_no_live_provider_transport_enabled": operator_confirms_no_live_provider_transport_enabled,
        "operator_confirms_no_dividend_provider_evidence_request_authorized": operator_confirms_no_dividend_provider_evidence_request_authorized,
        "operator_confirms_no_dividend_event_authority_created": operator_confirms_no_dividend_event_authority_created,
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
        raise SplitEventAuthorityFreezeError("operator_attestation missing")
    _expect(
        operator_attestation.get("operator_decision"),
        OPERATOR_DECISION_FREEZE_SPLIT_EVENT_AUTHORITY,
        "operator_decision",
    )
    _expect(
        operator_attestation.get("operator_attestation_phrase"),
        REQUIRED_SPLIT_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE,
        "operator_attestation_phrase",
    )
    _expect(
        operator_attestation.get("operator_attestation_version"),
        OPERATOR_ATTESTATION_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1,
        "operator_attestation_version",
    )
    if not operator_attestation.get("operator_reference"):
        raise SplitEventAuthorityFreezeError("operator_reference missing")
    if not operator_attestation.get("operator_attestation_timestamp_utc"):
        raise SplitEventAuthorityFreezeError("operator_attestation_timestamp_utc missing")
    expected_digest_fields = {
        "operator_confirms_split_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "operator_confirms_split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "operator_confirms_split_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "operator_confirms_dividend_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }
    for field, expected in expected_digest_fields.items():
        _expect(operator_attestation.get(field), expected, field)
    _expect(operator_attestation.get("operator_confirms_target_universe"), TARGET_UNIVERSE, "operator_confirms_target_universe")
    _expect(operator_attestation.get("operator_confirms_target_count"), 12, "operator_confirms_target_count")
    _expect(
        operator_attestation.get("operator_confirms_split_evidence_collected_count"),
        7,
        "operator_confirms_split_evidence_collected_count",
    )
    _expect(
        operator_attestation.get("operator_confirms_no_split_events_returned_count"),
        5,
        "operator_confirms_no_split_events_returned_count",
    )
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(operator_attestation.get(field), field)


def _validate_source_review_package(package: Mapping[str, Any]) -> None:
    if not isinstance(package, Mapping):
        raise SplitEventAuthorityFreezeError("split_evidence_results_review_package missing")
    expected = {
        "artifact_kind": review.ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "review_status": review.SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "failure_count": 0,
        "warning_count": 12,
    }
    for field, expected_value in expected.items():
        _expect(package.get(field), expected_value, f"source_review.{field}")
    _expect_false(package.get("provider_requests_made_in_review"), "source_review.provider_requests_made_in_review")
    _expect_false(
        package.get("split_provider_evidence_rerun_performed"),
        "source_review.split_provider_evidence_rerun_performed",
    )
    _expect_false(
        package.get("live_provider_transport_enabled_in_review"),
        "source_review.live_provider_transport_enabled_in_review",
    )
    summary = package.get("review_summary")
    if not isinstance(summary, Mapping) or summary.get("blocker_count") != 0:
        raise SplitEventAuthorityFreezeError("source_review.review_summary blocker_count mismatch")
    per_ticker = package.get("per_ticker_split_evidence_summary")
    if not isinstance(per_ticker, list) or len(per_ticker) != 12:
        raise SplitEventAuthorityFreezeError("source_review.per_ticker_split_evidence_summary mismatch")
    _expect([item.get("ticker") for item in per_ticker], TARGET_UNIVERSE, "source_review.per_ticker tickers")
    _expect(
        {item.get("ticker"): item.get("split_provider_evidence_status") for item in per_ticker},
        review.EXPECTED_PER_TICKER_STATUS,
        "source_review.per_ticker statuses",
    )


def per_ticker_split_event_authority_freeze_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_split_event_authority_freeze_digest", None)
    return semantic_digest(payload)


def _per_ticker_authority_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        provider_status = review.EXPECTED_PER_TICKER_STATUS[ticker]
        no_split = provider_status == review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
        entry = {
            "ticker": ticker,
            "split_event_authority_status": "FROZEN",
            "split_event_authority_scope": SPLIT_EVENT_AUTHORITY_ONLY,
            "split_event_authority_classification": PER_TICKER_SPLIT_AUTHORITY_CLASSIFICATION[ticker],
            "split_event_authority_created": True,
            "split_event_authority_frozen": True,
            "split_provider_evidence_status": provider_status,
            "split_absence_policy_status": (
                APPLIED_IF_NO_SPLIT_EVENTS_RETURNED
                if no_split
                else NOT_APPLIED_PROVIDER_SPLIT_EVIDENCE_COLLECTED
            ),
            "source_split_evidence_results_review_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
            "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
            "source_split_event_candidate_review_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "source_split_event_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
            "dividend_event_authority_status": "NOT_CREATED",
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_split_event_authority_freeze_digest"] = (
            per_ticker_split_event_authority_freeze_digest_v1(entry)
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
        "split_event_authority_frozen_by_operator": not failed,
        "authority_scope": SPLIT_EVENT_AUTHORITY_ONLY,
        "ready_for_dividend_provider_evidence_request_approval": not failed,
        "ready_for_corporate_action_readiness_review": False,
        "dividend_event_authority_authorized": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _base_artifact(operator_attestation: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1,
        "freeze_status": SPLIT_EVENT_AUTHORITY_FROZEN,
        "authority_scope": SPLIT_EVENT_AUTHORITY_ONLY,
        "created_offline": True,
        "provider_requests_made_in_freeze": False,
        "live_provider_transport_enabled_in_freeze": False,
        "split_provider_evidence_rerun_performed": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": True,
        "split_provider_evidence_request_authorized": True,
        "split_provider_evidence_executed": True,
        "split_provider_evidence_results_created": True,
        "split_event_evidence_results_review_created": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_provider_evidence_executed": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
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
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source_split_evidence_results_review_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "source_split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "failure_count": 0,
        "warning_count": 12,
        "per_ticker_split_event_authority": _per_ticker_authority_entries(),
        "operator_attestation": deepcopy(operator_attestation),
        "dividend_event_authority_artifact_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }


def _freeze_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact.get("operator_attestation", {})
    entries = artifact.get("per_ticker_split_event_authority", [])
    no_split_entries = [
        item
        for item in entries
        if item.get("split_provider_evidence_status")
        == review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER
    ]
    digest_present = all(
        isinstance(item.get("per_ticker_split_event_authority_freeze_digest"), str)
        and len(item["per_ticker_split_event_authority_freeze_digest"]) == 64
        for item in entries
    )
    absence_policy_preserved = all(
        item.get("split_absence_policy_status") == APPLIED_IF_NO_SPLIT_EVENTS_RETURNED
        for item in no_split_entries
    )
    return [
        _check("split_evidence_results_review_digest_matches_expected", EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("split_event_evidence_results_review_package_digest")),
        _check("split_evidence_results_review_has_zero_blockers", 0, artifact.get("source_split_evidence_results_review_blocker_count")),
        _check("split_provider_evidence_execution_digest_matches_expected", EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST, artifact.get("split_provider_evidence_execution_digest")),
        _check("split_provider_evidence_request_approval_digest_matches_expected", EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, artifact.get("split_provider_evidence_request_approval_digest")),
        _check("split_candidate_review_digest_matches_expected", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("split_event_authority_candidate_review_package_digest")),
        _check("split_candidate_digest_matches_expected", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, artifact.get("split_event_authority_candidate_digest")),
        _check("dividend_candidate_review_digest_bound", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_authority_candidate_review_package_digest")),
        _check("corporate_action_plan_approval_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, artifact.get("corporate_action_authority_plan_approval_digest")),
        _check("registry_inventory_approval_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, artifact.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("identity_freeze_digest_bound", EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        _check("target_universe_count_12", 12, artifact.get("target_universe_count")),
        _check("target_universe_matches_reviewed_evidence", TARGET_UNIVERSE, artifact.get("target_universe")),
        _check("operator_decision_freeze", OPERATOR_DECISION_FREEZE_SPLIT_EVENT_AUTHORITY, operator.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_SPLIT_EVENT_AUTHORITY_FREEZE_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        _check("operator_confirms_split_evidence_results_review_digest", EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, operator.get("operator_confirms_split_evidence_results_review_package_digest")),
        _check("operator_confirms_split_provider_evidence_execution_digest", EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST, operator.get("operator_confirms_split_provider_evidence_execution_digest")),
        _check("operator_confirms_split_request_approval_digest", EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, operator.get("operator_confirms_split_provider_evidence_request_approval_digest")),
        _check("operator_confirms_split_candidate_review_digest", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, operator.get("operator_confirms_split_candidate_review_package_digest")),
        _check("operator_confirms_split_candidate_digest", EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, operator.get("operator_confirms_split_candidate_digest")),
        _check("operator_confirms_dividend_candidate_review_digest", EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, operator.get("operator_confirms_dividend_candidate_review_package_digest")),
        _check("operator_confirms_authority_scope_split_event_only", True, operator.get("operator_confirms_authority_scope_split_event_only")),
        _check("operator_confirms_split_evidence_collected_count_7", 7, operator.get("operator_confirms_split_evidence_collected_count")),
        _check("operator_confirms_no_split_events_returned_count_5", 5, operator.get("operator_confirms_no_split_events_returned_count")),
        _check("authority_scope_split_event_only", SPLIT_EVENT_AUTHORITY_ONLY, artifact.get("authority_scope")),
        _check("split_event_authority_created_true", True, artifact.get("split_event_authority_created")),
        _check("split_event_authority_frozen_true", True, artifact.get("split_event_authority_frozen")),
        _check("per_ticker_split_authority_entries_12", 12, len(entries) if isinstance(entries, list) else None),
        _check("per_ticker_split_authority_freeze_digests_present", True, digest_present),
        _check("split_evidence_collected_count_7", 7, artifact.get("split_evidence_collected_count")),
        _check("no_split_events_returned_count_5", 5, artifact.get("no_split_events_returned_count")),
        _check("no_split_events_absence_policy_preserved", True, absence_policy_preserved),
        _check("provider_requests_made_in_freeze_false", False, artifact.get("provider_requests_made_in_freeze")),
        _check("live_provider_transport_enabled_in_freeze_false", False, artifact.get("live_provider_transport_enabled_in_freeze")),
        _check("split_provider_evidence_rerun_performed_false", False, artifact.get("split_provider_evidence_rerun_performed")),
        _check("dividend_provider_evidence_request_authorized_false", False, artifact.get("dividend_provider_evidence_request_authorized")),
        _check("dividend_provider_evidence_executed_false", False, artifact.get("dividend_provider_evidence_executed")),
        _check("dividend_event_authority_created_false", False, artifact.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, artifact.get("dividend_event_authority_frozen")),
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
        _check("no_dividend_event_authority_artifact_created", False, artifact.get("dividend_event_authority_artifact_created")),
        _check("no_corporate_action_authority_artifact_created", False, artifact.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, artifact.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, artifact.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, artifact.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, artifact.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, artifact.get("runtime_migration_approval_created")),
    ]


def _digest_payload(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(frozen_artifact)
    payload.pop("split_event_authority_freeze_digest", None)
    return payload


def split_event_authority_freeze_digest_v1(frozen_artifact: dict[str, Any]) -> str:
    """Return the deterministic digest for the frozen split event authority artifact."""
    return semantic_digest(_digest_payload(frozen_artifact))


def build_split_event_authority_frozen_v1(
    *,
    split_evidence_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build the split-event-only authority freeze artifact."""
    source_review = (
        split_evidence_results_review_package
        if split_evidence_results_review_package is not None
        else review.build_split_event_evidence_results_review_package_v1()
    )
    _validate_source_review_package(source_review)
    _validate_operator_attestation(operator_attestation)
    artifact = _base_artifact(operator_attestation)
    artifact["source_split_evidence_results_review_blocker_count"] = source_review["review_summary"]["blocker_count"]
    artifact["source_split_evidence_results_review_total_checks"] = source_review["review_summary"].get("total_checks")
    artifact["source_split_evidence_results_review_passed_checks"] = source_review["review_summary"].get("passed_checks")
    checklist = _freeze_checklist(artifact)
    artifact["freeze_checklist"] = checklist
    artifact["freeze_summary"] = _summary(checklist)
    artifact["split_event_authority_freeze_digest"] = split_event_authority_freeze_digest_v1(artifact)
    validate_split_event_authority_frozen_v1(artifact)
    return artifact


def _validate_per_ticker_entries(frozen_artifact: dict[str, Any]) -> None:
    entries = frozen_artifact.get("per_ticker_split_event_authority")
    if not isinstance(entries, list) or len(entries) != 12:
        raise SplitEventAuthorityFreezeError("per_ticker_split_event_authority mismatch")
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per_ticker tickers")
    for entry in entries:
        ticker = entry["ticker"]
        _expect(entry.get("split_event_authority_status"), "FROZEN", f"{ticker}.split_event_authority_status")
        _expect(entry.get("split_event_authority_scope"), SPLIT_EVENT_AUTHORITY_ONLY, f"{ticker}.split_event_authority_scope")
        _expect_true(entry.get("split_event_authority_created"), f"{ticker}.split_event_authority_created")
        _expect_true(entry.get("split_event_authority_frozen"), f"{ticker}.split_event_authority_frozen")
        _expect(
            entry.get("split_provider_evidence_status"),
            review.EXPECTED_PER_TICKER_STATUS[ticker],
            f"{ticker}.split_provider_evidence_status",
        )
        if entry["split_provider_evidence_status"] == review.execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER:
            _expect(entry.get("split_absence_policy_status"), APPLIED_IF_NO_SPLIT_EVENTS_RETURNED, f"{ticker}.split_absence_policy_status")
        _expect(entry.get("source_split_evidence_results_review_digest"), EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, f"{ticker}.source_split_evidence_results_review_digest")
        _expect(entry.get("source_split_provider_evidence_execution_digest"), EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST, f"{ticker}.source_split_provider_evidence_execution_digest")
        _expect(entry.get("source_split_event_candidate_review_digest"), EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, f"{ticker}.source_split_event_candidate_review_digest")
        _expect(entry.get("source_split_event_candidate_digest"), EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, f"{ticker}.source_split_event_candidate_digest")
        _expect(entry.get("dividend_event_authority_status"), "NOT_CREATED", f"{ticker}.dividend_event_authority_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect_false(entry.get("acquisition_authorized"), f"{ticker}.acquisition_authorized")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker}.{field}")
        _expect_digest(
            entry.get("per_ticker_split_event_authority_freeze_digest"),
            f"{ticker}.per_ticker_split_event_authority_freeze_digest",
        )
        _expect(
            entry["per_ticker_split_event_authority_freeze_digest"],
            per_ticker_split_event_authority_freeze_digest_v1(entry),
            f"{ticker}.per_ticker_split_event_authority_freeze_digest",
        )


def validate_split_event_authority_frozen_v1(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the split event authority freeze artifact and closed boundaries."""
    if not isinstance(frozen_artifact, dict):
        raise SplitEventAuthorityFreezeError("frozen_artifact must be a JSON object")
    _expect(frozen_artifact.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_FROZEN, "artifact_kind")
    _expect(frozen_artifact.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_FREEZE_V1, "schema_version")
    _expect(frozen_artifact.get("freeze_status"), SPLIT_EVENT_AUTHORITY_FROZEN, "freeze_status")
    _expect(frozen_artifact.get("authority_scope"), SPLIT_EVENT_AUTHORITY_ONLY, "authority_scope")
    for field in (
        "created_offline",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_event_evidence_results_review_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "corporate_action_authority_plan_approved",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
    ):
        _expect_true(frozen_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_freeze",
        "live_provider_transport_enabled_in_freeze",
        "split_provider_evidence_rerun_performed",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
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
        "dividend_event_authority_artifact_created",
        "corporate_action_authority_artifact_created",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(frozen_artifact.get(field), field)
    expected_fields = {
        "identity_authority_scope": "IDENTITY_AUTHORITY_ONLY",
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source_split_evidence_results_review_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "source_split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "failure_count": 0,
        "warning_count": 12,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }
    for field, expected in expected_fields.items():
        _expect(frozen_artifact.get(field), expected, field)
    _validate_operator_attestation(frozen_artifact.get("operator_attestation", {}))
    _validate_per_ticker_entries(frozen_artifact)
    if [item.get("check_id") for item in frozen_artifact.get("freeze_checklist", [])] != REQUIRED_FREEZE_CHECK_IDS:
        raise SplitEventAuthorityFreezeError("freeze_checklist check IDs mismatch")
    failed = [item for item in frozen_artifact["freeze_checklist"] if item.get("status") != PASS]
    if failed:
        raise SplitEventAuthorityFreezeError(f"freeze checklist failed: {failed[0]['check_id']}")
    _expect(frozen_artifact.get("freeze_summary"), _summary(frozen_artifact["freeze_checklist"]), "freeze_summary")
    digest = frozen_artifact.get("split_event_authority_freeze_digest")
    _expect_digest(digest, "split_event_authority_freeze_digest")
    _expect(digest, split_event_authority_freeze_digest_v1(frozen_artifact), "split_event_authority_freeze_digest")
    return {
        "status": "SPLIT_EVENT_AUTHORITY_FROZEN_VALID",
        "artifact_kind": frozen_artifact["artifact_kind"],
        "freeze_status": frozen_artifact["freeze_status"],
        "split_event_authority_freeze_digest": digest,
        "authority_scope": frozen_artifact["authority_scope"],
        "target_universe_count": frozen_artifact["target_universe_count"],
        "split_evidence_collected_count": frozen_artifact["split_evidence_collected_count"],
        "no_split_events_returned_count": frozen_artifact["no_split_events_returned_count"],
        "total_checks": frozen_artifact["freeze_summary"]["total_checks"],
        "passed_checks": frozen_artifact["freeze_summary"]["passed_checks"],
        "failed_checks": frozen_artifact["freeze_summary"]["failed_checks"],
        "blocker_count": frozen_artifact["freeze_summary"]["blocker_count"],
    }


def build_split_event_authority_frozen_markdown_v1(frozen_artifact: dict[str, Any]) -> str:
    """Render a sanitized Markdown status view for the split authority freeze."""
    validation = validate_split_event_authority_frozen_v1(frozen_artifact)
    lines = [
        "# MarketFlow Split Event Authority Freeze Status",
        "",
        "## Title",
        "- Split Event Authority Freeze Ceremony v1.",
        "",
        "## Frozen Split Event Authority",
        f"- Artifact kind: `{frozen_artifact['artifact_kind']}`",
        f"- Freeze status: `{frozen_artifact['freeze_status']}`",
        f"- Freeze digest: `{validation['split_event_authority_freeze_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator decision: `{frozen_artifact['operator_attestation']['operator_decision']}`",
        f"- Operator reference: `{frozen_artifact['operator_attestation']['operator_reference']}`",
        "- Operator attestation phrase matched exactly.",
        "",
        "## Source Split Evidence Results Review",
        f"- Review digest: `{frozen_artifact['split_event_evidence_results_review_package_digest']}`",
        "",
        "## Source Split Provider Evidence Execution",
        f"- Execution digest: `{frozen_artifact['split_provider_evidence_execution_digest']}`",
        f"- Request approval digest: `{frozen_artifact['split_provider_evidence_request_approval_digest']}`",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Frozen Per-Ticker Split Authority Summary",
    ]
    for entry in frozen_artifact["per_ticker_split_event_authority"]:
        lines.append(
            f"- `{entry['ticker']}`: `{entry['split_event_authority_classification']}` / "
            f"`{entry['split_provider_evidence_status']}`"
        )
    lines.extend(
        [
            "",
            "## No-Split Event Absence Policy",
            f"- No-split responses: `{frozen_artifact['no_split_events_returned_count']}`.",
            f"- Policy: `{APPLIED_IF_NO_SPLIT_EVENTS_RETURNED}` for no-split provider responses.",
            "",
            "## Authority Scope",
            f"- `{SPLIT_EVENT_AUTHORITY_ONLY}`.",
            "",
            "## Dividend Boundary",
            "- Dividend provider evidence and dividend event authority remain not authorized and not created.",
            "",
            "## Corporate-Action Authority Boundary",
            "- Corporate-action authority remains not created.",
            "",
            "## Acquisition Boundary",
            "- New ticker acquisition and acquisition generation remain not authorized.",
            "",
            "## Dataset Boundary",
            "- Dataset generation and canonical dataset authorization remain not authorized.",
            "",
            "## Predictive/Profitability Boundary",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Runtime Boundary",
            "- Runtime, strategy, paper trading, and broker execution remain not authorized.",
            "",
            "## Freeze Checklist Summary",
            f"- Total checks: `{frozen_artifact['freeze_summary']['total_checks']}`",
            f"- Passed checks: `{frozen_artifact['freeze_summary']['passed_checks']}`",
            f"- Failed checks: `{frozen_artifact['freeze_summary']['failed_checks']}`",
            f"- Blocker count: `{frozen_artifact['freeze_summary']['blocker_count']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"- {item}." for item in REMAINING_REQUIRED_TASKS)
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No provider request was made in this freeze.",
            "- No live provider transport was enabled in this freeze.",
            "- No split provider evidence rerun was performed.",
            "- No API key or raw provider payload is stored by this artifact.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_split_event_authority_frozen_v1(
    output_dir: str | Path,
    *,
    split_evidence_results_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Write the freeze artifact and Markdown status without overwriting files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    frozen_artifact = build_split_event_authority_frozen_v1(
        split_evidence_results_review_package=split_evidence_results_review_package,
        operator_attestation=operator_attestation,
    )
    json_path = output_path / "split_event_authority_frozen.json"
    markdown_path = output_path / "split_event_authority_frozen.md"
    if json_path.exists() or markdown_path.exists():
        raise SplitEventAuthorityFreezeError("split event authority freeze output already exists")
    json_path.write_bytes(canonical_json_bytes(frozen_artifact))
    markdown_path.write_text(
        build_split_event_authority_frozen_markdown_v1(frozen_artifact),
        encoding="utf-8",
    )
    validation = validate_split_event_authority_frozen_v1(frozen_artifact)
    return {
        "artifact": frozen_artifact,
        "validation": validation,
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
