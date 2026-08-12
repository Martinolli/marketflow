"""Offline dividend policy reconciliation review package."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_event_evidence_results_review_service as evidence
from marketflow.services import dividend_provider_evidence_request_approval_service as approval


ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE = (
    "DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE"
)
SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_REVIEW_V1 = (
    "dividend_policy_reconciliation_review_v1"
)
DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY = (
    "DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY"
)
DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_MISSING_OR_INVALID_EVIDENCE = (
    "DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_MISSING_OR_INVALID_EVIDENCE"
)

EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "ce32ad46c0a48be9a763ea1570aef0c9ba6b4ef3c96d1ea82f2884aaf7fd9007"
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    evidence.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    evidence.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST = (
    evidence.EXPECTED_OUTPUT_DIGESTS["dividend_policy_reconciliation_report.json"]
)
EXPECTED_TARGET_UNIVERSE = list(evidence.EXPECTED_TARGET_UNIVERSE)
EXPECTED_OUTPUT_DIGESTS = dict(evidence.EXPECTED_OUTPUT_DIGESTS)
EXPECTED_RESULT_FACTS = dict(evidence.EXPECTED_RESULT_FACTS)
RESEARCH_ONLY_NON_ACTIONABLE = evidence.RESEARCH_ONLY_NON_ACTIONABLE
NOT_AUTHORIZED = evidence.NOT_AUTHORIZED
PASS = evidence.PASS
FAIL = evidence.FAIL
BLOCKER = evidence.BLOCKER

POLICY_DOMAINS = [
    "adjusted_vs_unadjusted_price_policy",
    "cash_dividend_treatment_policy",
    "special_dividend_treatment_policy",
    "dividend_reinvestment_not_assumed",
    "total_return_not_assumed_unless_later_authorized",
    "dividend_adjustment_impact_on_canonical_dataset",
    "dividend_adjustment_impact_on_predictive_labels",
    "dividend_absence_policy",
    "zero_dividend_response_policy",
    "provider_snapshot_policy",
]
LIMITATIONS = [
    "dividend_evidence_read_only_provider_snapshot_at_execution_time",
    "zero_dividend_events_returned_requires_explicit_absence_policy_review",
    "dividend_adjustment_policy_not_approved",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "canonical_dataset_adjustment_policy_not_authorized",
    "predictive_label_adjustment_policy_not_authorized",
    "dividend_authority_not_created",
    "dividend_freeze_not_created",
    "corporate_action_authority_not_created",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
    "operator_approval_required_before_dividend_authority_freeze",
]
NEXT_GATES = [
    "dividend_policy_reconciliation_operator_assessment",
    "dividend_policy_reconciliation_approval_ceremony_if_required",
    "dividend_event_discrepancy_triage_if_required",
    "dividend_event_authority_freeze_ceremony",
    "combined_split_dividend_corporate_action_readiness_review",
    "corporate_action_authority_approval_if_required",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
ZERO_DIVIDEND_TICKERS = ["AMZN", "TSLA"]
REQUIRED_CHECK_IDS = [
    "dividend_evidence_results_review_digest_bound",
    "dividend_provider_evidence_execution_digest_bound",
    "dividend_provider_evidence_request_approval_digest_bound",
    "dividend_policy_reconciliation_report_digest_bound",
    "dividend_candidate_review_digest_bound",
    "dividend_candidate_digest_bound",
    "split_authority_freeze_digest_bound",
    "split_evidence_results_review_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_dividend_evidence_universe",
    "provider_request_count_12",
    "successful_provider_response_count_12",
    "failed_provider_response_count_zero",
    "dividend_evidence_collected_count_10",
    "no_dividend_events_returned_count_2",
    "zero_dividend_tickers_amzn_tsla",
    "policy_domains_reviewed",
    "adjusted_vs_unadjusted_price_policy_reviewed",
    "cash_dividend_treatment_policy_reviewed",
    "special_dividend_treatment_policy_reviewed",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "dividend_adjusted_price_policy_not_approved",
    "canonical_dataset_impact_not_authorized",
    "predictive_label_impact_not_authorized",
    "per_ticker_policy_review_entries_12",
    "per_ticker_policy_review_digests_present",
    "policy_reconciliation_requires_operator_review_true",
    "ready_for_dividend_event_authority_freeze_false",
    "outputs_research_only_non_actionable",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "provider_requests_made_in_review_false",
    "dividend_provider_evidence_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
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
    "dividend_policy_supports_future_dividend_authority_planning_true",
    "dividend_policy_creates_dividend_authority_false",
    "dividend_policy_creates_corporate_action_authority_false",
    "dividend_policy_creates_acquisition_authority_false",
    "dividend_policy_creates_dataset_generation_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_dividend_event_authority_artifact_created",
    "no_dividend_event_authority_freeze_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class DividendPolicyReconciliationReviewError(ValueError):
    """Raised when policy review evidence or authority boundaries are invalid."""


def _digest_payload(payload: dict[str, Any], digest_field: str) -> dict[str, Any]:
    clone = deepcopy(payload)
    clone.pop(digest_field, None)
    return clone


def dividend_policy_reconciliation_review_package_digest_v1(package: dict[str, Any]) -> str:
    return semantic_digest(
        _digest_payload(package, "dividend_policy_reconciliation_review_package_digest")
    )


def per_ticker_dividend_policy_reconciliation_review_digest_v1(entry: dict[str, Any]) -> str:
    return semantic_digest(
        _digest_payload(entry, "per_ticker_dividend_policy_reconciliation_review_digest")
    )


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "dividend_provider_evidence_rerun_performed": False,
        "source_dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "source_dividend_policy_reconciliation_report_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_REPORT_DIGEST,
        "dividend_provider_evidence_request_authorized": True,
        "dividend_provider_evidence_executed": True,
        "dividend_provider_evidence_results_created": True,
        "dividend_evidence_results_review_created": True,
        "dividend_policy_reconciliation_review_created": True,
        "dividend_policy_reconciliation_approved": False,
        "dividend_policy_reconciliation_requires_operator_review": True,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "ready_for_dividend_event_authority_freeze": False,
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
        "operator_review_required": True,
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2,
        "zero_dividend_tickers": list(ZERO_DIVIDEND_TICKERS),
        "policy_domains": list(POLICY_DOMAINS),
        "dividend_reinvestment_assumed": False,
        "total_return_assumed": False,
        "dividend_adjusted_price_policy_approved": False,
        "operator_policy_review_required": True,
        "canonical_dataset_impact_authorized": False,
        "predictive_label_impact_authorized": False,
        "dividend_policy_reconciliation_review_available": True,
        "dividend_policy_reconciliation_supports_future_dividend_authority_planning": True,
        "dividend_policy_reconciliation_requires_operator_approval_before_freeze": True,
        "dividend_policy_reconciliation_creates_dividend_authority": False,
        "dividend_policy_reconciliation_creates_corporate_action_authority": False,
        "dividend_policy_reconciliation_creates_acquisition_authority": False,
        "dividend_policy_reconciliation_creates_dataset_generation_authority": False,
        "dividend_policy_reconciliation_creates_predictive_evidence_authority": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "dividend_event_authority_artifact_created": False,
        "dividend_event_authority_freeze_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _blocked(reason: str) -> dict[str, Any]:
    package = _base_package()
    package.update({
        "review_status": DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_MISSING_OR_INVALID_EVIDENCE,
        "output_file_inspection_performed": False,
        "policy_evidence_verified": False,
        "blocked_reason": reason,
        "per_ticker_policy_review": [],
        "review_checklist": [],
        "review_summary": _summary([]),
    })
    package["dividend_policy_reconciliation_review_package_digest"] = (
        dividend_policy_reconciliation_review_package_digest_v1(package)
    )
    return package


def _policy_entry(evidence_row: Mapping[str, Any], policy_row: Mapping[str, Any]) -> dict[str, Any]:
    ticker = evidence_row.get("ticker")
    entry = {
        "ticker": ticker,
        "dividend_evidence_status": evidence_row.get("dividend_provider_evidence_status"),
        "dividend_event_count": evidence_row.get("dividend_event_count"),
        "policy_reconciliation_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
        "dividend_absence_policy_status": (
            "ZERO_ROW_RESPONSE_REQUIRES_OPERATOR_ABSENCE_POLICY_REVIEW"
            if ticker in ZERO_DIVIDEND_TICKERS
            else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
        ),
        "dividend_adjustment_policy_status": policy_row.get("cash_dividend_adjustment_policy"),
        "total_return_policy_status": policy_row.get("total_return_assumption"),
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
    }
    entry["per_ticker_dividend_policy_reconciliation_review_digest"] = (
        per_ticker_dividend_policy_reconciliation_review_digest_v1(entry)
    )
    return entry


def build_dividend_policy_reconciliation_review_package_v1(
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build policy review from already-sanitized local evidence only."""
    root = Path(output_root) if output_root is not None else evidence.execution.OUTPUT_ROOT
    digests = dict(expected_output_digests or EXPECTED_OUTPUT_DIGESTS)
    try:
        payloads, _ = evidence._verified_outputs(root, expected_output_digests=digests)
        policy_rows = payloads["dividend_policy_reconciliation_report.json"].get(
            "dividend_policy_reconciliation_report"
        )
        evidence_rows = evidence._per_ticker_summary(
            payloads["dividend_event_results_sanitized.json"]
        )
        run_summary = payloads["dividend_provider_evidence_run_manifest.json"].get(
            "execution_summary"
        )
        if not isinstance(policy_rows, list) or len(policy_rows) != 12:
            raise DividendPolicyReconciliationReviewError("policy reconciliation rows missing")
        if not isinstance(run_summary, Mapping):
            raise DividendPolicyReconciliationReviewError("execution summary missing")
        policy_by_ticker = {
            row.get("ticker"): row for row in policy_rows if isinstance(row, Mapping)
        }
        if list(policy_by_ticker) != EXPECTED_TARGET_UNIVERSE:
            raise DividendPolicyReconciliationReviewError("policy target universe mismatch")
        if any(
            row.get("dividend_policy_reconciliation_status") != "REQUIRES_OPERATOR_REVIEW"
            or row.get("cash_dividend_adjustment_policy") != "REQUIRES_OPERATOR_REVIEW"
            or row.get("total_return_assumption") != "NOT_ASSUMED"
            or row.get("authority_created") is not False
            for row in policy_rows
        ):
            raise DividendPolicyReconciliationReviewError("policy reconciliation boundary mismatch")
        entries = [
            _policy_entry(row, policy_by_ticker[row["ticker"]]) for row in evidence_rows
        ]
    except (evidence.DividendEventEvidenceResultsReviewError, DividendPolicyReconciliationReviewError, KeyError) as exc:
        return _blocked(str(exc))

    package = _base_package()
    package.update({
        "review_status": DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY,
        "output_root": root.as_posix(),
        "output_file_inspection_performed": True,
        "policy_evidence_verified": True,
        "expected_output_digests": digests,
        "source_dividend_policy_reconciliation_report_digest": digests["dividend_policy_reconciliation_report.json"],
        "provider_request_count": run_summary.get("provider_request_count"),
        "successful_provider_response_count": run_summary.get("successful_provider_response_count"),
        "failed_provider_response_count": run_summary.get("failed_provider_response_count"),
        "dividend_evidence_collected_count": run_summary.get("dividend_evidence_collected_count"),
        "no_dividend_events_returned_count": run_summary.get("no_dividend_events_returned_count"),
        "per_ticker_policy_review": entries,
        "ready_for_dividend_event_discrepancy_triage": False,
        "next_required_task": "DIVIDEND_POLICY_RECONCILIATION_OPERATOR_ASSESSMENT",
    })
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["dividend_policy_reconciliation_review_package_digest"] = (
        dividend_policy_reconciliation_review_package_digest_v1(package)
    )
    validate_dividend_policy_reconciliation_review_package_v1(package)
    return package


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "policy review evidence matches" if status == PASS else "policy review evidence mismatch",
    }


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "ready_for_operator_review": not failed,
        "ready_for_dividend_policy_reconciliation_approval": not failed,
        "ready_for_dividend_event_authority_freeze": False,
        "ready_for_dividend_event_discrepancy_triage": False,
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


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = package.get("per_ticker_policy_review", [])
    values = {
        "dividend_evidence_results_review_digest_bound": (EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("source_dividend_event_evidence_results_review_package_digest")),
        "dividend_provider_evidence_execution_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST, package.get("source_dividend_provider_evidence_execution_digest")),
        "dividend_provider_evidence_request_approval_digest_bound": (EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, package.get("source_dividend_provider_evidence_request_approval_digest")),
        "dividend_policy_reconciliation_report_digest_bound": (package.get("expected_output_digests", {}).get("dividend_policy_reconciliation_report.json"), package.get("source_dividend_policy_reconciliation_report_digest")),
        "dividend_candidate_review_digest_bound": (approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("dividend_event_authority_candidate_review_package_digest")),
        "dividend_candidate_digest_bound": (approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, package.get("dividend_event_authority_candidate_digest")),
        "split_authority_freeze_digest_bound": (approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, package.get("split_event_authority_freeze_digest")),
        "split_evidence_results_review_digest_bound": (approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("split_event_evidence_results_review_package_digest")),
        "corporate_action_plan_approval_digest_bound": (approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, package.get("corporate_action_authority_plan_approval_digest")),
        "identity_freeze_digest_bound": (approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, package.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, package.get("target_universe_count")),
        "target_universe_matches_dividend_evidence_universe": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "provider_request_count_12": (12, package.get("provider_request_count")),
        "successful_provider_response_count_12": (12, package.get("successful_provider_response_count")),
        "failed_provider_response_count_zero": (0, package.get("failed_provider_response_count")),
        "dividend_evidence_collected_count_10": (10, package.get("dividend_evidence_collected_count")),
        "no_dividend_events_returned_count_2": (2, package.get("no_dividend_events_returned_count")),
        "zero_dividend_tickers_amzn_tsla": (ZERO_DIVIDEND_TICKERS, package.get("zero_dividend_tickers")),
        "policy_domains_reviewed": (POLICY_DOMAINS, package.get("policy_domains")),
        "adjusted_vs_unadjusted_price_policy_reviewed": (True, "adjusted_vs_unadjusted_price_policy" in package.get("policy_domains", [])),
        "cash_dividend_treatment_policy_reviewed": (True, "cash_dividend_treatment_policy" in package.get("policy_domains", [])),
        "special_dividend_treatment_policy_reviewed": (True, "special_dividend_treatment_policy" in package.get("policy_domains", [])),
        "total_return_not_assumed": (False, package.get("total_return_assumed")),
        "dividend_reinvestment_not_assumed": (False, package.get("dividend_reinvestment_assumed")),
        "dividend_adjusted_price_policy_not_approved": (False, package.get("dividend_adjusted_price_policy_approved")),
        "canonical_dataset_impact_not_authorized": (False, package.get("canonical_dataset_impact_authorized")),
        "predictive_label_impact_not_authorized": (False, package.get("predictive_label_impact_authorized")),
        "per_ticker_policy_review_entries_12": (12, len(entries)),
        "per_ticker_policy_review_digests_present": (True, len(entries) == 12 and all(isinstance(row.get("per_ticker_dividend_policy_reconciliation_review_digest"), str) and len(row["per_ticker_dividend_policy_reconciliation_review_digest"]) == 64 for row in entries)),
        "policy_reconciliation_requires_operator_review_true": (True, package.get("dividend_policy_reconciliation_requires_operator_review")),
        "ready_for_dividend_event_authority_freeze_false": (False, package.get("ready_for_dividend_event_authority_freeze")),
        "outputs_research_only_non_actionable": (True, package.get("research_only")),
        "raw_provider_payloads_not_committed": (False, package.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, package.get("api_keys_stored_or_printed")),
        "provider_requests_made_in_review_false": (False, package.get("provider_requests_made_in_review")),
        "dividend_provider_evidence_rerun_performed_false": (False, package.get("dividend_provider_evidence_rerun_performed")),
        "live_provider_transport_enabled_in_review_false": (False, package.get("live_provider_transport_enabled_in_review")),
        "dividend_event_authority_created_false": (False, package.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_false": (False, package.get("dividend_event_authority_frozen")),
        "split_event_authority_created_true": (True, package.get("split_event_authority_created")),
        "split_event_authority_frozen_true": (True, package.get("split_event_authority_frozen")),
        "split_provider_evidence_rerun_performed_false": (False, package.get("split_provider_evidence_rerun_performed")),
        "corporate_action_authority_created_false": (False, package.get("corporate_action_authority_created")),
        "new_ticker_acquisition_authorized_false": (False, package.get("new_ticker_acquisition_authorized")),
        "dataset_generation_authorized_false": (False, package.get("dataset_generation_authorized")),
        "acquisition_generation_authorized_false": (False, package.get("acquisition_generation_authorized")),
        "canonical_dataset_authorized_false": (False, package.get("canonical_dataset_authorized")),
        "registry_approval_created_false": (False, package.get("registry_approval_created")),
        "additional_predictive_evidence_execution_authorized_false": (False, package.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, package.get("additional_predictive_evidence_executed")),
        "predictive_experiment_rerun_authorized_false": (False, package.get("predictive_experiment_rerun_authorized")),
        "predictive_experiment_rerun_performed_false": (False, package.get("predictive_experiment_rerun_performed")),
        "feature_matrix_regeneration_performed_false": (False, package.get("feature_matrix_regeneration_performed")),
        "new_strategy_scoring_performed_false": (False, package.get("new_strategy_scoring_performed")),
        "trade_recommendations_generated_false": (False, package.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package.get("predictive_usefulness")),
        "profitability_not_accepted": (acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        "runtime_migration_approved_false": (False, package.get("runtime_migration_approved")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, package.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        "automatic_stitching_false": (False, package.get("automatic_stitching")),
        "dividend_policy_supports_future_dividend_authority_planning_true": (True, package.get("dividend_policy_reconciliation_supports_future_dividend_authority_planning")),
        "dividend_policy_creates_dividend_authority_false": (False, package.get("dividend_policy_reconciliation_creates_dividend_authority")),
        "dividend_policy_creates_corporate_action_authority_false": (False, package.get("dividend_policy_reconciliation_creates_corporate_action_authority")),
        "dividend_policy_creates_acquisition_authority_false": (False, package.get("dividend_policy_reconciliation_creates_acquisition_authority")),
        "dividend_policy_creates_dataset_generation_authority_false": (False, package.get("dividend_policy_reconciliation_creates_dataset_generation_authority")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
        "no_dividend_event_authority_artifact_created": (False, package.get("dividend_event_authority_artifact_created")),
        "no_dividend_event_authority_freeze_created": (False, package.get("dividend_event_authority_freeze_created")),
        "no_corporate_action_authority_artifact_created": (False, package.get("corporate_action_authority_artifact_created")),
        "no_acquisition_authorization_created": (False, package.get("acquisition_authorization_created")),
        "no_dataset_generation_authorization_created": (False, package.get("dataset_generation_authorization_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, package.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, package.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, package.get("runtime_migration_approval_created")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise DividendPolicyReconciliationReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise DividendPolicyReconciliationReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise DividendPolicyReconciliationReviewError(f"{field} must be false")


def validate_dividend_policy_reconciliation_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate policy conclusions, source bindings, and closed authorities."""
    if not isinstance(review_package, dict):
        raise DividendPolicyReconciliationReviewError("review_package must be an object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_DIVIDEND_POLICY_RECONCILIATION_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_MISSING_OR_INVALID_EVIDENCE:
        _expect_false(review_package.get("output_file_inspection_performed"), "output_file_inspection_performed")
        _expect_false(review_package.get("policy_evidence_verified"), "policy_evidence_verified")
        digest = review_package.get("dividend_policy_reconciliation_review_package_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise DividendPolicyReconciliationReviewError("dividend_policy_reconciliation_review_package_digest missing")
        _expect(digest, dividend_policy_reconciliation_review_package_digest_v1(review_package), "dividend_policy_reconciliation_review_package_digest")
        return {"status": "DIVIDEND_POLICY_RECONCILIATION_REVIEW_BLOCKED_VALID"}
    _expect(review_package.get("review_status"), DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_READY, "review_status")
    for field in (
        "created_offline", "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed", "dividend_provider_evidence_results_created",
        "dividend_evidence_results_review_created", "dividend_policy_reconciliation_review_created",
        "dividend_policy_reconciliation_requires_operator_review", "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created", "split_event_authority_created",
        "split_event_authority_frozen", "corporate_action_authority_plan_approved", "research_only",
        "operator_review_required", "operator_policy_review_required", "output_file_inspection_performed",
        "policy_evidence_verified", "dividend_policy_reconciliation_review_available",
        "dividend_policy_reconciliation_supports_future_dividend_authority_planning",
        "dividend_policy_reconciliation_requires_operator_approval_before_freeze",
    ):
        _expect_true(review_package.get(field), field)
    false_fields = (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "dividend_provider_evidence_rerun_performed", "dividend_policy_reconciliation_approved",
        "dividend_event_authority_created", "dividend_event_authority_frozen",
        "ready_for_dividend_event_authority_freeze", "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created", "new_ticker_acquisition_authorized",
        "dataset_generation_authorized", "acquisition_generation_authorized",
        "canonical_dataset_authorized", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "dividend_reinvestment_assumed", "total_return_assumed",
        "dividend_adjusted_price_policy_approved", "canonical_dataset_impact_authorized",
        "predictive_label_impact_authorized", "dividend_policy_reconciliation_creates_dividend_authority",
        "dividend_policy_reconciliation_creates_corporate_action_authority",
        "dividend_policy_reconciliation_creates_acquisition_authority",
        "dividend_policy_reconciliation_creates_dataset_generation_authority",
        "dividend_policy_reconciliation_creates_predictive_evidence_authority",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "dividend_event_authority_artifact_created", "dividend_event_authority_freeze_created",
        "corporate_action_authority_artifact_created", "acquisition_authorization_created",
        "dataset_generation_authorization_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    )
    for field in false_fields:
        _expect_false(review_package.get(field), field)
    expected = {
        "source_dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE, "target_universe_count": 12,
        "provider_request_count": 12, "successful_provider_response_count": 12,
        "failed_provider_response_count": 0, "dividend_evidence_collected_count": 10,
        "no_dividend_events_returned_count": 2, "zero_dividend_tickers": ZERO_DIVIDEND_TICKERS,
        "policy_domains": POLICY_DOMAINS, "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS, "next_gates": NEXT_GATES,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    expected_digests = review_package.get("expected_output_digests")
    if not isinstance(expected_digests, dict) or sorted(expected_digests) != sorted(EXPECTED_OUTPUT_DIGESTS):
        raise DividendPolicyReconciliationReviewError("expected_output_digests mismatch")
    _expect(review_package.get("source_dividend_policy_reconciliation_report_digest"), expected_digests["dividend_policy_reconciliation_report.json"], "source_dividend_policy_reconciliation_report_digest")
    entries = review_package.get("per_ticker_policy_review")
    if not isinstance(entries, list) or len(entries) != 12:
        raise DividendPolicyReconciliationReviewError("per_ticker_policy_review mismatch")
    _expect([row.get("ticker") for row in entries], EXPECTED_TARGET_UNIVERSE, "per_ticker tickers")
    for row in entries:
        ticker = row["ticker"]
        expected_absence = "ZERO_ROW_RESPONSE_REQUIRES_OPERATOR_ABSENCE_POLICY_REVIEW" if ticker in ZERO_DIVIDEND_TICKERS else "DIVIDEND_EVENTS_PRESENT_PROVIDER_EVIDENCE_AVAILABLE"
        _expect(row.get("dividend_absence_policy_status"), expected_absence, f"{ticker}.dividend_absence_policy_status")
        _expect(row.get("dividend_adjustment_policy_status"), "REQUIRES_OPERATOR_REVIEW", f"{ticker}.dividend_adjustment_policy_status")
        _expect(row.get("total_return_policy_status"), "NOT_ASSUMED", f"{ticker}.total_return_policy_status")
        _expect(row.get("dividend_reinvestment_policy_status"), "NOT_ASSUMED", f"{ticker}.dividend_reinvestment_policy_status")
        _expect(row.get("canonical_dataset_impact_status"), "NOT_AUTHORIZED_FOR_DATASET_GENERATION", f"{ticker}.canonical_dataset_impact_status")
        _expect(row.get("predictive_label_impact_status"), "NOT_AUTHORIZED_FOR_PREDICTIVE_USE", f"{ticker}.predictive_label_impact_status")
        digest = row.get("per_ticker_dividend_policy_reconciliation_review_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise DividendPolicyReconciliationReviewError(f"{ticker}.per_ticker digest missing")
        _expect(digest, per_ticker_dividend_policy_reconciliation_review_digest_v1(row), f"{ticker}.per_ticker digest")
    _expect([row.get("check_id") for row in review_package.get("review_checklist", [])], REQUIRED_CHECK_IDS, "review checklist check IDs")
    if any(row.get("status") != PASS for row in review_package["review_checklist"]):
        raise DividendPolicyReconciliationReviewError("review checklist failed")
    _expect(review_package.get("review_summary"), _summary(review_package["review_checklist"]), "review_summary")
    digest = review_package.get("dividend_policy_reconciliation_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise DividendPolicyReconciliationReviewError("dividend_policy_reconciliation_review_package_digest missing")
    _expect(digest, dividend_policy_reconciliation_review_package_digest_v1(review_package), "dividend_policy_reconciliation_review_package_digest")
    return {
        "status": "DIVIDEND_POLICY_RECONCILIATION_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "dividend_policy_reconciliation_review_package_digest": digest,
        **{key: review_package["review_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_dividend_policy_reconciliation_review_markdown_v1(package: dict[str, Any]) -> str:
    """Render sanitized policy review Markdown."""
    validation = validate_dividend_policy_reconciliation_review_package_v1(package)
    lines = [
        "# MarketFlow Dividend Policy Reconciliation Review Status", "",
        "## Reviewed Dividend Policy Reconciliation",
        f"- Artifact/status: `{package['artifact_kind']}` / `{package['review_status']}`",
        f"- Review package digest: `{validation['dividend_policy_reconciliation_review_package_digest']}`", "",
        "## Source Dividend Evidence Results Review",
        f"- Evidence review digest: `{package['source_dividend_event_evidence_results_review_package_digest']}`",
        f"- Execution digest: `{package['source_dividend_provider_evidence_execution_digest']}`",
        f"- Policy report digest: `{package['source_dividend_policy_reconciliation_report_digest']}`", "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in package["target_universe"]), "",
        "## Per-Ticker Dividend Policy Review",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['dividend_adjustment_policy_status']}`, absence `{row['dividend_absence_policy_status']}`"
        for row in package["per_ticker_policy_review"]
    )
    lines.extend([
        "", "## Zero-Dividend Response Absence Policy",
        "- AMZN and TSLA require explicit operator absence-policy review; zero rows do not create no-dividend authority.", "",
        "## Adjusted vs Unadjusted Price Policy",
        "- Reviewed but not approved; operator assessment remains required.", "",
        "## Cash Dividend Treatment Policy",
        "- Requires operator assessment before any dividend freeze.", "",
        "## Special Dividend Treatment Policy",
        "- Requires operator assessment before any dividend freeze.", "",
        "## Total Return and Reinvestment Boundary",
        "- Total return and dividend reinvestment are not assumed.", "",
        "## Canonical Dataset Impact Boundary",
        "- Dataset generation and dividend-adjustment policy are not authorized.", "",
        "## Predictive Label Impact Boundary",
        "- Predictive-label regeneration and predictive evidence execution are not authorized.", "",
        "## Limitations", *[f"- `{item}`" for item in package["limitations"]], "",
        "## Next Gates", *[f"- `{item}`" for item in package["next_gates"]], "",
        "## Dividend Authority Boundary",
        f"- Created/frozen: `{package['dividend_event_authority_created']} / {package['dividend_event_authority_frozen']}`", "",
        "## Split Authority Boundary",
        f"- Created/frozen: `{package['split_event_authority_created']} / {package['split_event_authority_frozen']}`, unchanged.", "",
        "## Corporate-Action Authority Boundary",
        f"- Created: `{package['corporate_action_authority_created']}`", "",
        "## Acquisition Boundary", f"- Authorized: `{package['new_ticker_acquisition_authorized']}`", "",
        "## Dataset Boundary", f"- Authorized: `{package['dataset_generation_authorized']}`", "",
        "## Predictive/Profitability Boundary",
        f"- `{package['predictive_usefulness']} / {package['profitability']}`", "",
        "## Runtime Boundary",
        f"- `{package['runtime_use']} / {package['strategy_use']} / {package['paper_trading']} / {package['broker_execution']}`", "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{package['review_summary']['total_checks']} / {package['review_summary']['passed_checks']} / {package['review_summary']['failed_checks']} / {package['review_summary']['blocker_count']}`", "",
        "## Guardrails",
        "- No provider request, evidence rerun, or live transport occurred in review.",
        "- No dividend freeze or downstream authority was created.",
    ])
    return "\n".join(lines) + "\n"


def write_dividend_policy_reconciliation_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    package = build_dividend_policy_reconciliation_review_package_v1(
        output_root=output_root, expected_output_digests=expected_output_digests
    )
    validation = validate_dividend_policy_reconciliation_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "dividend_policy_reconciliation_review_package_v1.json"
    if path.exists():
        raise DividendPolicyReconciliationReviewError("dividend policy reconciliation review package output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "dividend_policy_reconciliation_review_package_digest": validation.get("dividend_policy_reconciliation_review_package_digest"),
        "payload_sha256": sha256_bytes(payload),
    }
