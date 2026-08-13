"""Offline approval ceremony for dividend policy reconciliation decisions."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_policy_reconciliation_review_service as review


ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_APPROVED = (
    "DIVIDEND_POLICY_RECONCILIATION_APPROVED"
)
SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1 = (
    "dividend_policy_reconciliation_approval_v1"
)
DIVIDEND_POLICY_RECONCILIATION_APPROVED = "DIVIDEND_POLICY_RECONCILIATION_APPROVED"
DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY = (
    "DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION = (
    "APPROVE_DIVIDEND_POLICY_RECONCILIATION"
)
OPERATOR_ATTESTATION_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1 = (
    "dividend_policy_reconciliation_approval_operator_attestation_v1"
)
REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE DIVIDEND POLICY RECONCILIATION MSFT NVDA AMZN GOOGL META TSLA JPM "
    "XOM JNJ WMT CAT LMT DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY"
)

EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST = (
    "fd671ad814765dabacb06bcd51627efe2052bf10d8d0cf40e37b862a75e02ff0"
)
EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    review.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    review.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST = (
    review.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST
)
EXPECTED_TARGET_UNIVERSE = list(review.EXPECTED_TARGET_UNIVERSE)
ZERO_DIVIDEND_TICKERS = list(review.ZERO_DIVIDEND_TICKERS)
PASS = review.PASS
FAIL = review.FAIL
BLOCKER = review.BLOCKER
NOT_AUTHORIZED = review.NOT_AUTHORIZED

OPERATOR_BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_zero_dividend_tickers_amzn_tsla",
    "operator_confirms_policy_approval_scope_only",
    "operator_confirms_total_return_not_assumed",
    "operator_confirms_dividend_reinvestment_not_assumed",
    "operator_confirms_dataset_generation_not_authorized",
    "operator_confirms_predictive_use_not_authorized",
    "operator_confirms_ready_for_dividend_authority_freeze",
    "operator_confirms_no_dividend_authority_created",
    "operator_confirms_no_dividend_authority_frozen",
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
REQUIRED_APPROVAL_CHECK_IDS = [
    "dividend_policy_reconciliation_review_digest_matches_expected",
    "dividend_policy_reconciliation_review_has_zero_blockers",
    "dividend_evidence_results_review_digest_bound",
    "dividend_provider_evidence_execution_digest_bound",
    "dividend_provider_evidence_request_approval_digest_bound",
    "dividend_policy_reconciliation_report_digest_bound",
    "dividend_candidate_review_digest_bound",
    "split_authority_freeze_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_policy_review_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_zero_dividend_tickers_amzn_tsla",
    "operator_confirms_dividend_evidence_collected_count_10",
    "operator_confirms_no_dividend_events_returned_count_2",
    "policy_approval_scope_only",
    "dividend_policy_reconciliation_approved_true",
    "ready_for_dividend_event_authority_freeze_true",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "dataset_generation_not_authorized",
    "predictive_use_not_authorized",
    "per_ticker_policy_approval_entries_12",
    "per_ticker_policy_approval_digests_present",
    "zero_dividend_policy_for_amzn_tsla_approved_for_freeze_input_only",
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
    "no_dividend_event_authority_freeze_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class DividendPolicyReconciliationApprovalError(ValueError):
    """Raised when policy approval evidence or attestations are invalid."""


def build_dividend_policy_reconciliation_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_dividend_policy_reconciliation_review_package_digest: str,
    operator_confirms_dividend_evidence_results_review_package_digest: str,
    operator_confirms_dividend_provider_evidence_execution_digest: str,
    operator_confirms_dividend_provider_evidence_request_approval_digest: str,
    operator_confirms_dividend_policy_reconciliation_report_digest: str,
    operator_confirms_dividend_candidate_review_digest: str,
    operator_confirms_split_authority_freeze_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_zero_dividend_tickers_amzn_tsla: bool,
    operator_confirms_dividend_evidence_collected_count: int,
    operator_confirms_no_dividend_events_returned_count: int,
    operator_confirms_policy_approval_scope_only: bool,
    operator_confirms_total_return_not_assumed: bool,
    operator_confirms_dividend_reinvestment_not_assumed: bool,
    operator_confirms_dataset_generation_not_authorized: bool,
    operator_confirms_predictive_use_not_authorized: bool,
    operator_confirms_ready_for_dividend_authority_freeze: bool,
    operator_confirms_no_dividend_authority_created: bool,
    operator_confirms_no_dividend_authority_frozen: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION,
) -> dict[str, Any]:
    """Build a non-secret operator attestation; approval validates it fail-closed."""
    return {name: value for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "operator_confirms_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "operator_confirms_dividend_policy_reconciliation_report_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "operator_confirms_dividend_candidate_review_digest": review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": review.approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": review.approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def _validated_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise DividendPolicyReconciliationApprovalError("operator_attestation must be an object")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION,
        "operator_attestation_phrase": REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1,
        "operator_confirms_target_universe": EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_dividend_evidence_collected_count": 10,
        "operator_confirms_no_dividend_events_returned_count": 2,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        if attestation.get(field) != value:
            raise DividendPolicyReconciliationApprovalError(f"{field} mismatch")
    for field in OPERATOR_BOOLEAN_CONFIRMATION_FIELDS:
        if attestation.get(field) is not True:
            raise DividendPolicyReconciliationApprovalError(f"{field} must be true")
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise DividendPolicyReconciliationApprovalError(f"{field} required")
    return deepcopy(attestation)


def _entry_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    clone = deepcopy(entry)
    clone.pop("per_ticker_dividend_policy_reconciliation_approval_digest", None)
    return clone


def per_ticker_dividend_policy_reconciliation_approval_digest_v1(entry: dict[str, Any]) -> str:
    return semantic_digest(_entry_digest_payload(entry))


def _approval_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for row in source["per_ticker_policy_review"]:
        ticker = row["ticker"]
        entry = {
            "ticker": ticker,
            "dividend_evidence_status": row["dividend_evidence_status"],
            "dividend_event_count": row["dividend_event_count"],
            "policy_reconciliation_approval_status": "APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY",
            "dividend_absence_policy_status": (
                "ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY"
                if ticker in ZERO_DIVIDEND_TICKERS
                else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
            ),
            "dividend_adjustment_policy_status": "APPROVED_FOR_FREEZE_INPUT_ONLY",
            "total_return_policy_status": "NOT_ASSUMED",
            "dividend_reinvestment_policy_status": "NOT_ASSUMED",
            "canonical_dataset_impact_status": "NOT_AUTHORIZED_FOR_DATASET_GENERATION",
            "predictive_label_impact_status": "NOT_AUTHORIZED_FOR_PREDICTIVE_USE",
            "dividend_event_authority_status": "NOT_CREATED",
            "dividend_event_freeze_status": "NOT_FROZEN",
            "split_event_authority_status": "FROZEN",
            "corporate_action_authority_created": False,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_per_ticker_policy_review_digest": row["per_ticker_dividend_policy_reconciliation_review_digest"],
        }
        entry["per_ticker_dividend_policy_reconciliation_approval_digest"] = (
            per_ticker_dividend_policy_reconciliation_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id, "status": status, "expected": expected, "actual": actual,
        "severity": BLOCKER,
        "message": "approval evidence matches" if status == PASS else "approval evidence mismatch",
    }


def _approval_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = artifact["operator_attestation"]
    entries = artifact["per_ticker_policy_approval_entries"]
    all_digests = all(
        attestation.get(field) == value for field, value in _expected_digest_confirmations().items()
    )
    zero_policy = all(
        row["dividend_absence_policy_status"] == "ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY"
        for row in entries if row["ticker"] in ZERO_DIVIDEND_TICKERS
    )
    values = {
        "dividend_policy_reconciliation_review_digest_matches_expected": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_policy_reconciliation_review_package_digest")),
        "dividend_policy_reconciliation_review_has_zero_blockers": (0, artifact.get("source_policy_review_blocker_count")),
        "dividend_evidence_results_review_digest_bound": (EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_evidence_results_review_package_digest")),
        "dividend_provider_evidence_execution_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST, artifact.get("dividend_provider_evidence_execution_digest")),
        "dividend_provider_evidence_request_approval_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, artifact.get("dividend_provider_evidence_request_approval_digest")),
        "dividend_policy_reconciliation_report_digest_bound": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST, artifact.get("dividend_policy_reconciliation_report_digest")),
        "dividend_candidate_review_digest_bound": (review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, artifact.get("dividend_event_authority_candidate_review_package_digest")),
        "split_authority_freeze_digest_bound": (review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("split_event_authority_freeze_digest")),
        "corporate_action_plan_approval_digest_bound": (review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, artifact.get("corporate_action_authority_plan_approval_digest")),
        "identity_freeze_digest_bound": (review.approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_policy_review_universe": (EXPECTED_TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_DIVIDEND_POLICY_RECONCILIATION, attestation.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all_digests),
        "operator_confirms_zero_dividend_tickers_amzn_tsla": (True, attestation.get("operator_confirms_zero_dividend_tickers_amzn_tsla")),
        "operator_confirms_dividend_evidence_collected_count_10": (10, attestation.get("operator_confirms_dividend_evidence_collected_count")),
        "operator_confirms_no_dividend_events_returned_count_2": (2, attestation.get("operator_confirms_no_dividend_events_returned_count")),
        "policy_approval_scope_only": (DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY, artifact.get("approval_scope")),
        "dividend_policy_reconciliation_approved_true": (True, artifact.get("dividend_policy_reconciliation_approved")),
        "ready_for_dividend_event_authority_freeze_true": (True, artifact.get("ready_for_dividend_event_authority_freeze")),
        "total_return_not_assumed": (False, artifact.get("total_return_assumed")),
        "dividend_reinvestment_not_assumed": (False, artifact.get("dividend_reinvestment_assumed")),
        "dataset_generation_not_authorized": (False, artifact.get("dataset_generation_authorized")),
        "predictive_use_not_authorized": (False, artifact.get("predictive_use_authorized")),
        "per_ticker_policy_approval_entries_12": (12, len(entries)),
        "per_ticker_policy_approval_digests_present": (True, len(entries) == 12 and all(len(row.get("per_ticker_dividend_policy_reconciliation_approval_digest", "")) == 64 for row in entries)),
        "zero_dividend_policy_for_amzn_tsla_approved_for_freeze_input_only": (True, zero_policy),
    }
    boolean_expectations = {
        "dividend_event_authority_created_false": (False, "dividend_event_authority_created"),
        "dividend_event_authority_frozen_false": (False, "dividend_event_authority_frozen"),
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
        "no_dividend_event_authority_artifact_created": (False, "dividend_event_authority_artifact_created"),
        "no_dividend_event_authority_freeze_created": (False, "dividend_event_authority_freeze_created"),
        "no_corporate_action_authority_artifact_created": (False, "corporate_action_authority_artifact_created"),
        "no_acquisition_authorization_created": (False, "acquisition_authorization_created"),
        "no_dataset_generation_authorization_created": (False, "dataset_generation_authorization_created"),
        "no_predictive_usefulness_acceptance_artifact_created": (False, "predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": (False, "profitability_acceptance_created"),
        "no_runtime_migration_approval_created": (False, "runtime_migration_approval_created"),
    }
    for check_id, (expected, field) in boolean_expectations.items():
        values[check_id] = (expected, artifact.get(field))
    values.update({
        "predictive_usefulness_not_accepted": (acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (acquisition.PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
    })
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_APPROVAL_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "dividend_policy_reconciliation_approved_by_operator": not failed,
        "approval_scope": DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY,
        "ready_for_dividend_event_authority_freeze": not failed,
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


def _digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    clone = deepcopy(artifact)
    clone.pop("dividend_policy_reconciliation_approval_digest", None)
    return clone


def dividend_policy_reconciliation_approval_digest_v1(artifact: dict[str, Any]) -> str:
    return semantic_digest(_digest_payload(artifact))


def build_dividend_policy_reconciliation_approved_v1(
    *,
    dividend_policy_reconciliation_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build approval only after exact offline operator attestation validation."""
    source = (
        dividend_policy_reconciliation_review_package
        if dividend_policy_reconciliation_review_package is not None
        else review.build_dividend_policy_reconciliation_review_package_v1()
    )
    validation = review.validate_dividend_policy_reconciliation_review_package_v1(source)
    if source.get("dividend_policy_reconciliation_review_package_digest") != EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST:
        raise DividendPolicyReconciliationApprovalError("source policy review digest mismatch")
    if validation.get("blocker_count") != 0:
        raise DividendPolicyReconciliationApprovalError("source policy review has blockers")
    attestation = _validated_attestation(operator_attestation)
    entries = _approval_entries(source)
    artifact = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "schema_version": SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1,
        "approval_status": DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "approval_scope": DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "dividend_provider_evidence_rerun_performed": False,
        "dividend_provider_evidence_request_authorized": True,
        "dividend_provider_evidence_executed": True,
        "dividend_provider_evidence_results_created": True,
        "dividend_evidence_results_review_created": True,
        "dividend_policy_reconciliation_review_created": True,
        "dividend_policy_reconciliation_approved": True,
        "ready_for_dividend_event_authority_freeze": True,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "split_provider_evidence_rerun_performed": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
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
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_report_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": review.approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": review.approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": review.approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": review.approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": review.approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": review.approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": review.approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": review.approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_policy_review_blocker_count": 0,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": list(ZERO_DIVIDEND_TICKERS),
        "dividend_reinvestment_assumed": False,
        "total_return_assumed": False,
        "dividend_adjusted_price_policy_approved_for_freeze_input": True,
        "cash_dividend_treatment_policy_approved_for_freeze_input": True,
        "special_dividend_treatment_policy_approved_for_freeze_input": True,
        "zero_dividend_absence_policy_approved_for_freeze_input": True,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "operator_attestation": attestation,
        "per_ticker_policy_approval_entries": entries,
        "dividend_event_authority_artifact_created": False,
        "dividend_event_authority_freeze_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "next_required_task": "DIVIDEND_EVENT_AUTHORITY_FREEZE_CEREMONY",
    }
    checklist = _approval_checklist(artifact)
    artifact["approval_checklist"] = checklist
    artifact["approval_summary"] = _summary(checklist)
    artifact["dividend_policy_reconciliation_approval_digest"] = (
        dividend_policy_reconciliation_approval_digest_v1(artifact)
    )
    validate_dividend_policy_reconciliation_approved_v1(artifact)
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise DividendPolicyReconciliationApprovalError(f"{field} mismatch")


def validate_dividend_policy_reconciliation_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate exact approval scope while rejecting downstream authorization."""
    if not isinstance(approved_artifact, dict):
        raise DividendPolicyReconciliationApprovalError("approved_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "schema_version": SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_V1,
        "approval_status": DIVIDEND_POLICY_RECONCILIATION_APPROVED,
        "approval_scope": DIVIDEND_POLICY_RECONCILIATION_APPROVAL_ONLY,
        "dividend_policy_reconciliation_approved": True,
        "ready_for_dividend_event_authority_freeze": True,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": ZERO_DIVIDEND_TICKERS,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "dividend_reinvestment_assumed": False,
        "total_return_assumed": False,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "predictive_use_authorized": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(approved_artifact.get(field), value, field)
    true_fields = (
        "created_offline", "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed", "dividend_provider_evidence_results_created",
        "dividend_evidence_results_review_created", "dividend_policy_reconciliation_review_created",
        "dividend_event_authority_candidate_created", "dividend_event_authority_review_created",
        "corporate_action_authority_plan_approved", "research_only",
        "dividend_adjusted_price_policy_approved_for_freeze_input",
        "cash_dividend_treatment_policy_approved_for_freeze_input",
        "special_dividend_treatment_policy_approved_for_freeze_input",
        "zero_dividend_absence_policy_approved_for_freeze_input",
    )
    for field in true_fields:
        _expect(approved_artifact.get(field), True, field)
    false_fields = (
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "dividend_provider_evidence_rerun_performed", "dividend_event_authority_created",
        "dividend_event_authority_frozen", "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created", "new_ticker_acquisition_authorized",
        "dataset_generation_authorized", "acquisition_generation_authorized",
        "canonical_dataset_authorized", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "dividend_event_authority_artifact_created", "dividend_event_authority_freeze_created",
        "corporate_action_authority_artifact_created", "acquisition_authorization_created",
        "dataset_generation_authorization_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    )
    for field in false_fields:
        _expect(approved_artifact.get(field), False, field)
    _validated_attestation(approved_artifact.get("operator_attestation"))
    entries = approved_artifact.get("per_ticker_policy_approval_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise DividendPolicyReconciliationApprovalError("per_ticker_policy_approval_entries mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected_absence = (
            "ZERO_ROW_RESPONSE_APPROVED_FOR_DIVIDEND_AUTHORITY_FREEZE_INPUT_ONLY"
            if ticker in ZERO_DIVIDEND_TICKERS
            else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
        )
        _expect(row.get("dividend_absence_policy_status"), expected_absence, f"{ticker}.dividend_absence_policy_status")
        digest = row.get("per_ticker_dividend_policy_reconciliation_approval_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise DividendPolicyReconciliationApprovalError(f"{ticker}.per_ticker digest missing")
        _expect(digest, per_ticker_dividend_policy_reconciliation_approval_digest_v1(row), f"{ticker}.per_ticker digest")
    _expect([row.get("check_id") for row in approved_artifact.get("approval_checklist", [])], REQUIRED_APPROVAL_CHECK_IDS, "approval checklist check IDs")
    if any(row.get("status") != PASS for row in approved_artifact["approval_checklist"]):
        raise DividendPolicyReconciliationApprovalError("approval checklist failed")
    _expect(approved_artifact.get("approval_summary"), _summary(approved_artifact["approval_checklist"]), "approval_summary")
    digest = approved_artifact.get("dividend_policy_reconciliation_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DividendPolicyReconciliationApprovalError("dividend_policy_reconciliation_approval_digest missing")
    _expect(digest, dividend_policy_reconciliation_approval_digest_v1(approved_artifact), "dividend_policy_reconciliation_approval_digest")
    return {
        "status": "DIVIDEND_POLICY_RECONCILIATION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "dividend_policy_reconciliation_approval_digest": digest,
        **{key: approved_artifact["approval_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_dividend_policy_reconciliation_approved_markdown_v1(artifact: dict[str, Any]) -> str:
    validation = validate_dividend_policy_reconciliation_approved_v1(artifact)
    lines = [
        "# MarketFlow Dividend Policy Reconciliation Approval Status", "",
        "## Approved Dividend Policy Reconciliation",
        f"- Artifact/status/scope: `{artifact['artifact_kind']}` / `{artifact['approval_status']}` / `{artifact['approval_scope']}`",
        f"- Approval digest: `{validation['dividend_policy_reconciliation_approval_digest']}`", "",
        "## Operator Attestation",
        f"- Decision/reference/timestamp: `{artifact['operator_attestation']['operator_decision']}` / `{artifact['operator_attestation']['operator_reference']}` / `{artifact['operator_attestation']['operator_attestation_timestamp_utc']}`", "",
        "## Source Dividend Policy Reconciliation Review",
        f"- Review digest: `{artifact['dividend_policy_reconciliation_review_package_digest']}`", "",
        "## Target Universe", "- " + ", ".join(f"`{ticker}`" for ticker in artifact["target_universe"]), "",
        "## Approved Per-Ticker Dividend Policy Entries",
    ]
    lines.extend(f"- `{row['ticker']}`: `{row['policy_reconciliation_approval_status']}`, absence `{row['dividend_absence_policy_status']}`" for row in artifact["per_ticker_policy_approval_entries"])
    lines.extend([
        "", "## Zero-Dividend Response Absence Policy",
        "- AMZN and TSLA zero-row responses are accepted only as source-specific future freeze input, not standalone no-dividend authority.", "",
        "## Adjusted vs Unadjusted Price Policy",
        "- Approved for future dividend-authority freeze input only.", "",
        "## Cash and Special Dividend Treatment",
        "- Approved for future dividend-authority freeze input only.", "",
        "## Total Return and Reinvestment Boundary",
        "- Total return and dividend reinvestment remain not assumed.", "",
        "## Canonical Dataset Impact Boundary", "- Dataset generation is not authorized.", "",
        "## Predictive Label Impact Boundary", "- Predictive use is not authorized.", "",
        "## Dividend Authority Boundary", "- No dividend authority or freeze is created by this approval.", "",
        "## Split Authority Boundary", "- Split authority remains frozen and unchanged.", "",
        "## Corporate-Action Authority Boundary", "- Corporate-action authority remains not created.", "",
        "## Acquisition Boundary", "- Acquisition remains not authorized.", "",
        "## Dataset Boundary", "- Dataset generation remains not authorized.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain not authorized.", "",
        "## Approval Checklist Summary",
        f"- Total/passed/failed/blockers: `{artifact['approval_summary']['total_checks']} / {artifact['approval_summary']['passed_checks']} / {artifact['approval_summary']['failed_checks']} / {artifact['approval_summary']['blocker_count']}`", "",
        "## Remaining Required Tasks", "- Dividend event authority freeze ceremony.", "- Combined split/dividend corporate-action readiness review.", "",
        "## Guardrails", "- No provider request, evidence rerun, dividend freeze, or downstream authority was created.",
    ])
    return "\n".join(lines) + "\n"


def write_dividend_policy_reconciliation_approved_v1(
    output_dir: str | Path,
    *,
    dividend_policy_reconciliation_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    artifact = build_dividend_policy_reconciliation_approved_v1(
        dividend_policy_reconciliation_review_package=dividend_policy_reconciliation_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_dividend_policy_reconciliation_approved_v1(artifact)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "dividend_policy_reconciliation_approved_v1.json"
    if path.exists():
        raise DividendPolicyReconciliationApprovalError("dividend policy reconciliation approval output already exists")
    payload = canonical_json_bytes(artifact)
    path.write_bytes(payload)
    return {
        "path": str(path), "artifact_kind": artifact["artifact_kind"],
        "approval_status": artifact["approval_status"],
        "dividend_policy_reconciliation_approval_digest": validation["dividend_policy_reconciliation_approval_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
