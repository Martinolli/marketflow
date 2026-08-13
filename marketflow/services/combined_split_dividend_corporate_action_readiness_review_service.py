"""Offline readiness review for frozen split and dividend event authorities."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_event_authority_freeze_service as dividend_freeze
from marketflow.services import split_event_authority_freeze_service as split_freeze


ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE = (
    "COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_V1 = (
    "combined_split_dividend_corporate_action_readiness_review_v1"
)
COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY = (
    "COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY"
)
READY_FOR_CORPORATE_ACTION_AUTHORITY_APPROVAL = (
    "READY_FOR_CORPORATE_ACTION_AUTHORITY_APPROVAL"
)

EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    "37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303"
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    "98b7e740b750701eb1e63e6e0ad88ffd4d665c44ece2e0e85e0a15e4a2a4d6ae"
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
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST = (
    dividend_freeze.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    dividend_freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    dividend_freeze.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    dividend_freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    dividend_freeze.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(dividend_freeze.TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_AUTHORIZED = dividend_freeze.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

LIMITATIONS = [
    "combined_readiness_is_review_only",
    "corporate_action_authority_not_created",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
    "canonical_dataset_not_authorized",
    "registry_approval_not_created",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "operator_approval_required_before_corporate_action_authority",
]
NEXT_GATES = [
    "combined_corporate_action_readiness_operator_assessment",
    "corporate_action_authority_approval_ceremony",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

REQUIRED_REVIEW_CHECK_IDS = [
    "split_authority_freeze_digest_bound",
    "dividend_authority_freeze_digest_bound",
    "split_evidence_results_review_digest_bound",
    "dividend_evidence_results_review_digest_bound",
    "dividend_policy_approval_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_split_and_dividend_authority_universe",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "split_event_authority_scope_split_only",
    "dividend_event_authority_created_true",
    "dividend_event_authority_frozen_true",
    "dividend_event_authority_scope_dividend_only",
    "per_ticker_combined_readiness_entries_12",
    "per_ticker_combined_readiness_digests_present",
    "combined_readiness_status_ready_for_corporate_action_authority_approval",
    "combined_split_dividend_authorities_available_true",
    "ready_for_corporate_action_authority_approval_true",
    "corporate_action_authority_created_false",
    "corporate_action_authority_frozen_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "acquisition_generation_authorized_false",
    "canonical_dataset_authorized_false",
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
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "split_provider_evidence_rerun_performed_false",
    "dividend_provider_evidence_rerun_performed_false",
    "combined_readiness_creates_corporate_action_authority_false",
    "combined_readiness_creates_acquisition_authority_false",
    "combined_readiness_creates_dataset_generation_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CombinedCorporateActionReadinessReviewError(ValueError):
    """Raised when the combined readiness package violates its review contract."""


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
        raise CombinedCorporateActionReadinessReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CombinedCorporateActionReadinessReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CombinedCorporateActionReadinessReviewError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CombinedCorporateActionReadinessReviewError(f"{field} missing")


def per_ticker_combined_readiness_review_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_combined_readiness_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        split_classification = split_freeze.PER_TICKER_SPLIT_AUTHORITY_CLASSIFICATION[ticker]
        dividend_status, dividend_count = dividend_freeze.EXPECTED_PER_TICKER[ticker]
        dividend_classification = (
            dividend_freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_ZERO_ROW_ABSENCE_POLICY
            if ticker in dividend_freeze.ZERO_DIVIDEND_TICKERS
            else dividend_freeze.DIVIDEND_EVENT_AUTHORITY_FROZEN_WITH_PROVIDER_DIVIDEND_EVIDENCE
        )
        entry = {
            "ticker": ticker,
            "split_event_authority_status": "FROZEN",
            "split_event_authority_classification": split_classification,
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_classification": dividend_classification,
            "dividend_evidence_status": dividend_status,
            "dividend_event_count": dividend_count,
            "combined_corporate_action_readiness_status": READY_FOR_CORPORATE_ACTION_AUTHORITY_APPROVAL,
            "corporate_action_authority_status": "NOT_CREATED",
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        entry["per_ticker_combined_readiness_review_digest"] = (
            per_ticker_combined_readiness_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_V1,
        "review_status": COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "split_provider_evidence_rerun_performed": False,
        "dividend_provider_evidence_rerun_performed": False,
        "combined_corporate_action_readiness_review_created": True,
        "combined_corporate_action_readiness_review_ready": True,
        "ready_for_corporate_action_authority_approval": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "corporate_action_authority_frozen": False,
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
        "operator_review_required": True,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "per_ticker_combined_readiness": _per_ticker_entries(),
        "combined_split_dividend_authorities_available": True,
        "split_authority_frozen": True,
        "dividend_authority_frozen": True,
        "combined_corporate_action_readiness_review_supports_future_corporate_action_authority_approval": True,
        "combined_corporate_action_readiness_review_creates_corporate_action_authority": False,
        "combined_corporate_action_readiness_review_creates_acquisition_authority": False,
        "combined_corporate_action_readiness_review_creates_dataset_generation_authority": False,
        "combined_corporate_action_readiness_review_creates_predictive_evidence_authority": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = package["per_ticker_combined_readiness"]
    digests_present = len(entries) == 12 and all(
        len(row.get("per_ticker_combined_readiness_review_digest", "")) == 64
        for row in entries
    )
    values: dict[str, tuple[Any, Any]] = {
        "split_authority_freeze_digest_bound": (EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, package.get("split_event_authority_freeze_digest")),
        "dividend_authority_freeze_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST, package.get("dividend_event_authority_freeze_digest")),
        "split_evidence_results_review_digest_bound": (EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("split_event_evidence_results_review_package_digest")),
        "dividend_evidence_results_review_digest_bound": (EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("dividend_event_evidence_results_review_package_digest")),
        "dividend_policy_approval_digest_bound": (EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST, package.get("dividend_policy_reconciliation_approval_digest")),
        "corporate_action_plan_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, package.get("corporate_action_authority_plan_approval_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, package.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, package.get("target_universe_count")),
        "target_universe_matches_split_and_dividend_authority_universe": (TARGET_UNIVERSE, package.get("target_universe")),
        "split_event_authority_created_true": (True, package.get("split_event_authority_created")),
        "split_event_authority_frozen_true": (True, package.get("split_event_authority_frozen")),
        "split_event_authority_scope_split_only": (split_freeze.SPLIT_EVENT_AUTHORITY_ONLY, package.get("split_event_authority_scope")),
        "dividend_event_authority_created_true": (True, package.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_true": (True, package.get("dividend_event_authority_frozen")),
        "dividend_event_authority_scope_dividend_only": (dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY, package.get("dividend_event_authority_scope")),
        "per_ticker_combined_readiness_entries_12": (12, len(entries)),
        "per_ticker_combined_readiness_digests_present": (True, digests_present),
        "combined_readiness_status_ready_for_corporate_action_authority_approval": (True, all(row.get("combined_corporate_action_readiness_status") == READY_FOR_CORPORATE_ACTION_AUTHORITY_APPROVAL for row in entries)),
        "combined_split_dividend_authorities_available_true": (True, package.get("combined_split_dividend_authorities_available")),
        "ready_for_corporate_action_authority_approval_true": (True, package.get("ready_for_corporate_action_authority_approval")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
    }
    boolean_checks = {
        "corporate_action_authority_created_false": (False, "corporate_action_authority_created"),
        "corporate_action_authority_frozen_false": (False, "corporate_action_authority_frozen"),
        "new_ticker_acquisition_authorized_false": (False, "new_ticker_acquisition_authorized"),
        "dataset_generation_authorized_false": (False, "dataset_generation_authorized"),
        "acquisition_generation_authorized_false": (False, "acquisition_generation_authorized"),
        "canonical_dataset_authorized_false": (False, "canonical_dataset_authorized"),
        "registry_approval_created_false": (False, "registry_approval_created"),
        "additional_predictive_evidence_execution_authorized_false": (False, "additional_predictive_evidence_execution_authorized"),
        "additional_predictive_evidence_executed_false": (False, "additional_predictive_evidence_executed"),
        "predictive_experiment_rerun_authorized_false": (False, "predictive_experiment_rerun_authorized"),
        "feature_matrix_regeneration_performed_false": (False, "feature_matrix_regeneration_performed"),
        "new_strategy_scoring_performed_false": (False, "new_strategy_scoring_performed"),
        "trade_recommendations_generated_false": (False, "trade_recommendations_generated"),
        "runtime_migration_approved_false": (False, "runtime_migration_approved"),
        "automatic_stitching_false": (False, "automatic_stitching"),
        "provider_requests_made_in_review_false": (False, "provider_requests_made_in_review"),
        "live_provider_transport_enabled_in_review_false": (False, "live_provider_transport_enabled_in_review"),
        "split_provider_evidence_rerun_performed_false": (False, "split_provider_evidence_rerun_performed"),
        "dividend_provider_evidence_rerun_performed_false": (False, "dividend_provider_evidence_rerun_performed"),
        "combined_readiness_creates_corporate_action_authority_false": (False, "combined_corporate_action_readiness_review_creates_corporate_action_authority"),
        "combined_readiness_creates_acquisition_authority_false": (False, "combined_corporate_action_readiness_review_creates_acquisition_authority"),
        "combined_readiness_creates_dataset_generation_authority_false": (False, "combined_corporate_action_readiness_review_creates_dataset_generation_authority"),
        "no_corporate_action_authority_artifact_created": (False, "corporate_action_authority_artifact_created"),
        "no_acquisition_authorization_created": (False, "acquisition_authorization_created"),
        "no_dataset_generation_authorization_created": (False, "dataset_generation_authorization_created"),
        "no_predictive_usefulness_acceptance_artifact_created": (False, "predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": (False, "profitability_acceptance_created"),
        "no_runtime_migration_approval_created": (False, "runtime_migration_approval_created"),
    }
    values.update(
        {check_id: (expected, package.get(field)) for check_id, (expected, field) in boolean_checks.items()}
    )
    values.update(
        {
            "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
            "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
            "runtime_use_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
            "strategy_use_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
            "paper_trading_not_authorized": (NOT_AUTHORIZED, package.get("paper_trading")),
            "broker_execution_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        }
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_REVIEW_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    blocker_count = sum(row["severity"] == BLOCKER for row in failed)
    ready = blocker_count == 0
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_corporate_action_authority_approval": ready,
        "corporate_action_authority_authorized": False,
        "corporate_action_authority_frozen": False,
        "split_event_authority_authorized": True,
        "split_event_authority_frozen": True,
        "dividend_event_authority_authorized": True,
        "dividend_event_authority_frozen": True,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("combined_split_dividend_corporate_action_readiness_review_package_digest", None)
    return payload


def combined_split_dividend_corporate_action_readiness_review_package_digest_v1(
    package: dict[str, Any],
) -> str:
    return semantic_digest(_digest_payload(package))


def build_combined_split_dividend_corporate_action_readiness_review_package_v1() -> dict[str, Any]:
    """Build a deterministic review-only package without provider or freeze execution."""
    package = _base_package()
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    if package["review_summary"]["blocker_count"] != 0:
        package["combined_corporate_action_readiness_review_ready"] = False
        package["ready_for_corporate_action_authority_approval"] = False
    package["combined_split_dividend_corporate_action_readiness_review_package_digest"] = (
        combined_split_dividend_corporate_action_readiness_review_package_digest_v1(package)
    )
    validate_combined_split_dividend_corporate_action_readiness_review_package_v1(package)
    return package


def _validate_per_ticker_entries(package: dict[str, Any]) -> None:
    entries = package.get("per_ticker_combined_readiness")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CombinedCorporateActionReadinessReviewError(
            "per_ticker_combined_readiness mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    expected_rows = {row["ticker"]: row for row in _per_ticker_entries()}
    for row in entries:
        ticker = row["ticker"]
        expected = expected_rows[ticker]
        for field, value in expected.items():
            if field != "per_ticker_combined_readiness_review_digest":
                _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_combined_readiness_review_digest")
        _expect_digest(digest, f"{ticker}.per_ticker_combined_readiness_review_digest")
        _expect(
            digest,
            per_ticker_combined_readiness_review_digest_v1(row),
            f"{ticker}.per_ticker_combined_readiness_review_digest",
        )


def validate_combined_split_dividend_corporate_action_readiness_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate review readiness while rejecting all downstream authorization."""
    if not isinstance(review_package, dict):
        raise CombinedCorporateActionReadinessReviewError("review_package must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_V1,
        "review_status": COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_READY,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_scope": dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_policy_reconciliation_review_package_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    true_fields = (
        "created_offline",
        "combined_corporate_action_readiness_review_created",
        "combined_corporate_action_readiness_review_ready",
        "ready_for_corporate_action_authority_approval",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "corporate_action_authority_plan_approved",
        "research_only",
        "operator_review_required",
        "combined_split_dividend_authorities_available",
        "split_authority_frozen",
        "dividend_authority_frozen",
        "combined_corporate_action_readiness_review_supports_future_corporate_action_authority_approval",
    )
    false_fields = (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "split_provider_evidence_rerun_performed",
        "dividend_provider_evidence_rerun_performed",
        "corporate_action_authority_created",
        "corporate_action_authority_frozen",
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
        "combined_corporate_action_readiness_review_creates_corporate_action_authority",
        "combined_corporate_action_readiness_review_creates_acquisition_authority",
        "combined_corporate_action_readiness_review_creates_dataset_generation_authority",
        "combined_corporate_action_readiness_review_creates_predictive_evidence_authority",
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
        _expect_true(review_package.get(field), field)
    for field in false_fields:
        _expect_false(review_package.get(field), field)
    _validate_per_ticker_entries(review_package)
    _expect(
        [row.get("check_id") for row in review_package.get("review_checklist", [])],
        REQUIRED_REVIEW_CHECK_IDS,
        "review_checklist check IDs",
    )
    if any(row.get("status") != PASS for row in review_package["review_checklist"]):
        raise CombinedCorporateActionReadinessReviewError("review checklist failed")
    _expect(
        review_package.get("review_summary"),
        _summary(review_package["review_checklist"]),
        "review_summary",
    )
    digest = review_package.get(
        "combined_split_dividend_corporate_action_readiness_review_package_digest"
    )
    _expect_digest(
        digest,
        "combined_split_dividend_corporate_action_readiness_review_package_digest",
    )
    _expect(
        digest,
        combined_split_dividend_corporate_action_readiness_review_package_digest_v1(
            review_package
        ),
        "combined_split_dividend_corporate_action_readiness_review_package_digest",
    )
    return {
        "status": "COMBINED_SPLIT_DIVIDEND_CORPORATE_ACTION_READINESS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "combined_split_dividend_corporate_action_readiness_review_package_digest": digest,
        "target_universe_count": review_package["target_universe_count"],
        **{
            key: review_package["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_combined_split_dividend_corporate_action_readiness_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    validation = validate_combined_split_dividend_corporate_action_readiness_review_package_v1(
        review_package
    )
    lines = [
        "# MarketFlow Combined Split/Dividend Corporate-Action Readiness Review Status",
        "",
        "## Title",
        "- Combined Split/Dividend Corporate-Action Readiness Review Package v1.",
        "",
        "## Combined Split/Dividend Corporate-Action Readiness Review",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Review digest: `{validation['combined_split_dividend_corporate_action_readiness_review_package_digest']}`.",
        "",
        "## Source Split Authority Freeze",
        f"- Freeze digest: `{review_package['split_event_authority_freeze_digest']}`.",
        "",
        "## Source Dividend Authority Freeze",
        f"- Freeze digest: `{review_package['dividend_event_authority_freeze_digest']}`.",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Per-Ticker Combined Readiness Summary",
    ]
    lines.extend(
        f"- `{row['ticker']}`: split `{row['split_event_authority_classification']}`; dividend `{row['dividend_event_authority_classification']}` ({row['dividend_event_count']} events); `{row['combined_corporate_action_readiness_status']}`."
        for row in review_package["per_ticker_combined_readiness"]
    )
    lines.extend(
        [
            "",
            "## Readiness Conclusion",
            "- Both event authorities are frozen in their separate scopes; the package supports a future, separately attested corporate-action authority approval ceremony.",
            "",
            "## Limitations",
        ]
    )
    lines.extend(f"- `{item}`." for item in LIMITATIONS)
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`." for item in NEXT_GATES)
    lines.extend(
        [
            "",
            "## Corporate-Action Authority Boundary",
            "- Corporate-action authority is not created or frozen by this review.",
            "",
            "## Acquisition Boundary",
            "- Acquisition remains not authorized.",
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
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`.",
            "",
            "## Guardrails",
            "- No provider request, evidence rerun, authority creation, acquisition, dataset generation, predictive acceptance, or runtime activation occurred.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_combined_split_dividend_corporate_action_readiness_review_package_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    package = build_combined_split_dividend_corporate_action_readiness_review_package_v1()
    output_path = Path(output_dir)
    json_path = output_path / "combined_split_dividend_corporate_action_readiness_review_package_v1.json"
    markdown_path = output_path / "combined_split_dividend_corporate_action_readiness_review_package_v1.md"
    if json_path.exists() or markdown_path.exists():
        raise CombinedCorporateActionReadinessReviewError(
            "combined readiness review output already exists"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(package))
    markdown_path.write_text(
        build_combined_split_dividend_corporate_action_readiness_review_markdown_v1(
            package
        ),
        encoding="utf-8",
    )
    return {
        "package": package,
        "validation": validate_combined_split_dividend_corporate_action_readiness_review_package_v1(
            package
        ),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
