"""Offline acquisition-generation chain candidate for authority-approved tickers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import corporate_action_authority_approval_service as authority


ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE = (
    "ACQUISITION_GENERATION_CHAIN_CANDIDATE"
)
SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_V1 = (
    "acquisition_generation_chain_candidate_v1"
)
ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW = (
    "ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    "93524b9bdc4641de4c6eb1cc8343b848ceff316241c92edab57a2062b8640644"
)
EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = (
    authority.EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    authority.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    authority.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    authority.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    authority.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    authority.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST = (
    authority.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    authority.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    authority.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    authority.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    authority.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    authority.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(authority.TARGET_UNIVERSE)
ACQUISITION_GENERATION_CHAIN_OBJECTIVE = (
    "PLAN_ACQUISITION_GENERATION_CHAIN_FOR_CORPORATE_ACTION_AUTHORITY_APPROVED_EXPANDED_UNIVERSE"
)
ACQUISITION_GENERATION_CHAIN_SCOPE = "CHAIN_CANDIDATE_ONLY_NOT_AUTHORIZATION"
ACQUISITION_GENERATION_MODE = "PLANNED_NOT_EXECUTED"
ACQUISITION_GENERATION_AUTHORITY_STATUS = "NOT_AUTHORIZED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
MARKET_DATA_ACQUISITION_NOT_EXECUTED = "NOT_EXECUTED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
NOT_AUTHORIZED = authority.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ACQUISITION_PLANNING_DIMENSIONS = [
    "ticker_identity_authority_bound",
    "corporate_action_authority_bound",
    "provider_selection_policy",
    "market_data_endpoint_selection_policy",
    "historical_price_bar_acquisition_policy",
    "historical_volume_acquisition_policy",
    "adjusted_unadjusted_price_policy_binding",
    "split_adjustment_policy_binding",
    "dividend_adjustment_policy_binding",
    "trading_calendar_policy",
    "session_filter_policy",
    "timeframe_policy",
    "data_quality_validation_policy",
    "sanitized_output_policy",
    "raw_payload_policy",
    "digest_manifest_policy",
]

FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY = {
    "future_acquisition_provider_request_policy_status": "PLANNED_REQUIRES_SEPARATE_APPROVAL",
    "allowed_future_request_type": "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY",
    "api_key_handling": "DO_NOT_STORE_KEYS_OR_PRINT_KEYS",
    "raw_payload_policy": "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS",
    "sanitized_status_doc_required": True,
    "rate_limit_policy": "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED",
    "provider_result_authority": "ACQUISITION_EVIDENCE_ONLY_NOT_DATASET_AUTHORITY",
}

FUTURE_ACQUISITION_CHAIN = [
    "Acquisition generation chain candidate operator review package.",
    "Acquisition provider request approval ceremony, if live provider access is required.",
    "Acquisition provider evidence execution.",
    "Acquisition results/evidence review package.",
    "Acquisition generation approval ceremony, if required.",
    "Acquisition generation freeze ceremony.",
    "Canonical dataset chain candidate.",
    "Canonical dataset candidate operator review.",
    "Canonical dataset freeze ceremony.",
    "Research registry approval chain.",
]

FUTURE_GATES = [
    "acquisition_generation_chain_candidate_operator_review",
    "acquisition_provider_request_approval_if_required",
    "acquisition_provider_evidence_execution",
    "acquisition_results_review",
    "acquisition_generation_approval_if_required",
    "acquisition_generation_freeze",
    "canonical_dataset_chain_candidate",
    "canonical_dataset_candidate_operator_review",
    "canonical_dataset_freeze",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "no_acquisition_execution_without_operator_approval",
    "no_acquisition_freeze_without_results_review",
    "no_dataset_generation_without_acquisition_freeze",
    "no_canonical_dataset_without_dataset_candidate_review",
    "no_registry_approval_without_canonical_dataset_freeze",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "all_outputs_labeled_research_only",
    "operator_approval_required_before_any_acquisition_provider_request",
]

PLANNED_OUTPUT_NAMES = [
    "acquisition_generation_chain_manifest",
    "per_ticker_acquisition_requirement_matrix",
    "acquisition_provider_request_policy_template",
    "acquisition_evidence_result_template",
    "acquisition_failure_reason_inventory_template",
    "acquisition_digest_manifest_template",
    "acquisition_results_review_template",
    "canonical_dataset_chain_candidate_template",
    "operator_review_summary_template",
]

REQUIRED_CHECK_IDS = [
    "corporate_action_authority_approval_digest_bound",
    "combined_readiness_review_digest_bound",
    "split_authority_freeze_digest_bound",
    "dividend_authority_freeze_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_corporate_action_authority_universe",
    "corporate_action_authority_created_true",
    "corporate_action_authority_approved_true",
    "corporate_action_authority_scope_corporate_action_only",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "dividend_event_authority_created_true",
    "dividend_event_authority_frozen_true",
    "ready_for_acquisition_generation_chain_candidate_true",
    "acquisition_generation_chain_candidate_created_true",
    "acquisition_chain_scope_candidate_only",
    "acquisition_generation_authority_status_not_authorized",
    "per_ticker_acquisition_chain_entries_12",
    "per_ticker_acquisition_chain_digests_present",
    "future_acquisition_chain_defined",
    "future_provider_request_policy_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_provider_transport_enabled_false",
    "market_data_acquisition_performed_false",
    "new_ticker_acquisition_authorized_false",
    "acquisition_generation_authorized_false",
    "acquisition_generation_executed_false",
    "dataset_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "canonical_dataset_frozen_false",
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
    "no_acquisition_authorization_artifact_created",
    "no_acquisition_execution_artifact_created",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AcquisitionGenerationChainCandidateError(ValueError):
    """Raised when acquisition-chain candidate evidence is invalid."""


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
        raise AcquisitionGenerationChainCandidateError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationChainCandidateError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationChainCandidateError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionGenerationChainCandidateError(f"{field} missing")


def per_ticker_acquisition_generation_chain_candidate_digest_v1(
    entry: dict[str, Any],
) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_acquisition_generation_chain_candidate_digest", None)
    return semantic_digest(payload)


def _source_authority_entries() -> list[dict[str, Any]]:
    readiness = (
        authority.readiness.build_combined_split_dividend_corporate_action_readiness_review_package_v1()
    )
    return authority._per_ticker_entries(readiness)


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in _source_authority_entries():
        entry = {
            "ticker": source["ticker"],
            "identity_authority_status": "FROZEN",
            "split_event_authority_status": "FROZEN",
            "split_event_authority_classification": source[
                "split_event_authority_classification"
            ],
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_classification": source[
                "dividend_event_authority_classification"
            ],
            "dividend_event_count": source["dividend_event_count"],
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_chain_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "acquisition_authorized": False,
            "acquisition_generation_authorized": False,
            "acquisition_generation_executed": False,
            "market_data_acquisition_status": MARKET_DATA_ACQUISITION_NOT_EXECUTED,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_per_ticker_corporate_action_authority_approval_digest": source[
                "per_ticker_corporate_action_authority_approval_digest"
            ],
        }
        entry["per_ticker_acquisition_generation_chain_candidate_digest"] = (
            per_ticker_acquisition_generation_chain_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "output_name": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_V1,
        "candidate_status": ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "acquisition_generation_chain_candidate_created": True,
        "acquisition_generation_chain_ready_for_operator_review": True,
        "ready_for_acquisition_generation_chain_candidate": True,
        "acquisition_generation_chain_approved": False,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "acquisition_generation_results_created": False,
        "acquisition_generation_frozen": False,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": authority.CORPORATE_ACTION_AUTHORITY_ONLY,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": authority.readiness.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": authority.readiness.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
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
        "operator_review_required": True,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "acquisition_generation_chain_objective": ACQUISITION_GENERATION_CHAIN_OBJECTIVE,
        "acquisition_generation_chain_scope": ACQUISITION_GENERATION_CHAIN_SCOPE,
        "acquisition_generation_mode": ACQUISITION_GENERATION_MODE,
        "acquisition_generation_authority_status": ACQUISITION_GENERATION_AUTHORITY_STATUS,
        "acquisition_planning_dimensions": list(ACQUISITION_PLANNING_DIMENSIONS),
        "future_acquisition_provider_request_policy": deepcopy(
            FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY
        ),
        "per_ticker_acquisition_generation_chain_candidates": _per_ticker_entries(),
        "future_acquisition_chain": list(FUTURE_ACQUISITION_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "acquisition_authorization_artifact_created": False,
        "acquisition_execution_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_acquisition_generation_chain_candidates", [])
    outputs = candidate.get("planned_outputs", [])
    values: dict[str, tuple[Any, Any]] = {
        "corporate_action_authority_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, candidate.get("corporate_action_authority_approval_digest")),
        "combined_readiness_review_digest_bound": (EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST, candidate.get("combined_split_dividend_corporate_action_readiness_review_package_digest")),
        "split_authority_freeze_digest_bound": (EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, candidate.get("split_event_authority_freeze_digest")),
        "dividend_authority_freeze_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST, candidate.get("dividend_event_authority_freeze_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, candidate.get("target_universe_count")),
        "target_universe_matches_corporate_action_authority_universe": (TARGET_UNIVERSE, candidate.get("target_universe")),
        "corporate_action_authority_created_true": (True, candidate.get("corporate_action_authority_created")),
        "corporate_action_authority_approved_true": (True, candidate.get("corporate_action_authority_approved")),
        "corporate_action_authority_scope_corporate_action_only": (authority.CORPORATE_ACTION_AUTHORITY_ONLY, candidate.get("corporate_action_authority_scope")),
        "split_event_authority_created_true": (True, candidate.get("split_event_authority_created")),
        "split_event_authority_frozen_true": (True, candidate.get("split_event_authority_frozen")),
        "dividend_event_authority_created_true": (True, candidate.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_true": (True, candidate.get("dividend_event_authority_frozen")),
        "ready_for_acquisition_generation_chain_candidate_true": (True, candidate.get("ready_for_acquisition_generation_chain_candidate")),
        "acquisition_generation_chain_candidate_created_true": (True, candidate.get("acquisition_generation_chain_candidate_created")),
        "acquisition_chain_scope_candidate_only": (ACQUISITION_GENERATION_CHAIN_SCOPE, candidate.get("acquisition_generation_chain_scope")),
        "acquisition_generation_authority_status_not_authorized": (ACQUISITION_GENERATION_AUTHORITY_STATUS, candidate.get("acquisition_generation_authority_status")),
        "per_ticker_acquisition_chain_entries_12": (12, len(entries)),
        "per_ticker_acquisition_chain_digests_present": (True, len(entries) == 12 and all(isinstance(row.get("per_ticker_acquisition_generation_chain_candidate_digest"), str) and len(row["per_ticker_acquisition_generation_chain_candidate_digest"]) == 64 for row in entries)),
        "future_acquisition_chain_defined": (FUTURE_ACQUISITION_CHAIN, candidate.get("future_acquisition_chain")),
        "future_provider_request_policy_defined": (FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY, candidate.get("future_acquisition_provider_request_policy")),
        "future_gates_defined": (FUTURE_GATES, candidate.get("future_gates")),
        "risk_controls_defined": (RISK_CONTROLS, candidate.get("risk_controls")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("generation_status") == PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, candidate.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, candidate.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, candidate.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, candidate.get("broker_execution")),
    }
    false_checks = {
        "provider_requests_made_false": "provider_requests_made",
        "live_provider_transport_enabled_false": "live_provider_transport_enabled",
        "market_data_acquisition_performed_false": "market_data_acquisition_performed",
        "new_ticker_acquisition_authorized_false": "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized_false": "acquisition_generation_authorized",
        "acquisition_generation_executed_false": "acquisition_generation_executed",
        "dataset_generation_authorized_false": "dataset_generation_authorized",
        "canonical_dataset_authorized_false": "canonical_dataset_authorized",
        "canonical_dataset_frozen_false": "canonical_dataset_frozen",
        "registry_approval_created_false": "registry_approval_created",
        "additional_predictive_evidence_execution_authorized_false": "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed_false": "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized_false": "predictive_experiment_rerun_authorized",
        "new_strategy_scoring_performed_false": "new_strategy_scoring_performed",
        "trade_recommendations_generated_false": "trade_recommendations_generated",
        "runtime_migration_approved_false": "runtime_migration_approved",
        "automatic_stitching_false": "automatic_stitching",
        "no_acquisition_authorization_artifact_created": "acquisition_authorization_artifact_created",
        "no_acquisition_execution_artifact_created": "acquisition_execution_artifact_created",
        "no_dataset_generation_authorization_created": "dataset_generation_authorization_created",
        "no_canonical_dataset_artifact_created": "canonical_dataset_artifact_created",
        "no_registry_approval_created": "registry_approval_artifact_created",
        "no_predictive_usefulness_acceptance_artifact_created": "predictive_usefulness_acceptance_artifact_created",
        "no_profitability_acceptance_created": "profitability_acceptance_created",
        "no_runtime_migration_approval_created": "runtime_migration_approval_created",
    }
    values.update(
        {check_id: (False, candidate.get(field)) for check_id, field in false_checks.items()}
    )
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "ready_for_operator_review": not failed,
        "ready_for_acquisition_provider_request_approval": False,
        "ready_for_acquisition_generation_approval": False,
        "ready_for_acquisition_generation_freeze": False,
        "ready_for_canonical_dataset_chain_candidate": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def acquisition_generation_chain_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    payload = deepcopy(candidate)
    payload.pop("acquisition_generation_chain_candidate_digest", None)
    return semantic_digest(payload)


def build_acquisition_generation_chain_candidate_v1() -> dict[str, Any]:
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["acquisition_generation_chain_candidate_digest"] = (
        acquisition_generation_chain_candidate_digest_v1(candidate)
    )
    validate_acquisition_generation_chain_candidate_v1(candidate)
    return candidate


def _validate_per_ticker(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_acquisition_generation_chain_candidates")
    if not isinstance(entries, list) or len(entries) != 12:
        raise AcquisitionGenerationChainCandidateError("per_ticker entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    expected_sources = {row["ticker"]: row for row in _source_authority_entries()}
    for row in entries:
        ticker = row["ticker"]
        source = expected_sources[ticker]
        expected = {
            "identity_authority_status": "FROZEN",
            "split_event_authority_status": "FROZEN",
            "split_event_authority_classification": source["split_event_authority_classification"],
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_classification": source["dividend_event_authority_classification"],
            "dividend_event_count": source["dividend_event_count"],
            "corporate_action_authority_status": "APPROVED",
            "acquisition_generation_chain_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "acquisition_authorized": False,
            "acquisition_generation_authorized": False,
            "acquisition_generation_executed": False,
            "market_data_acquisition_status": MARKET_DATA_ACQUISITION_NOT_EXECUTED,
            "dataset_generation_authorized": False,
            "canonical_dataset_authorized": False,
            "registry_approval_created": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_per_ticker_corporate_action_authority_approval_digest": source["per_ticker_corporate_action_authority_approval_digest"],
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        digest = row.get("per_ticker_acquisition_generation_chain_candidate_digest")
        _expect_digest(digest, f"{ticker}.candidate digest")
        _expect(
            digest,
            per_ticker_acquisition_generation_chain_candidate_digest_v1(row),
            f"{ticker}.candidate digest",
        )


def validate_acquisition_generation_chain_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise AcquisitionGenerationChainCandidateError("candidate must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CHAIN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CHAIN_CANDIDATE_V1,
        "candidate_status": ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW,
        "corporate_action_authority_scope": authority.CORPORATE_ACTION_AUTHORITY_ONLY,
        "split_event_authority_scope": authority.readiness.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_scope": authority.readiness.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "acquisition_generation_chain_objective": ACQUISITION_GENERATION_CHAIN_OBJECTIVE,
        "acquisition_generation_chain_scope": ACQUISITION_GENERATION_CHAIN_SCOPE,
        "acquisition_generation_mode": ACQUISITION_GENERATION_MODE,
        "acquisition_generation_authority_status": ACQUISITION_GENERATION_AUTHORITY_STATUS,
        "acquisition_planning_dimensions": ACQUISITION_PLANNING_DIMENSIONS,
        "future_acquisition_provider_request_policy": FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY,
        "future_acquisition_chain": FUTURE_ACQUISITION_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(candidate.get(field), value, field)
    true_fields = (
        "created_offline",
        "acquisition_generation_chain_candidate_created",
        "acquisition_generation_chain_ready_for_operator_review",
        "ready_for_acquisition_generation_chain_candidate",
        "corporate_action_authority_created",
        "corporate_action_authority_approved",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "research_only",
        "operator_review_required",
    )
    false_fields = (
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "acquisition_generation_chain_approved",
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
        "acquisition_generation_results_created",
        "acquisition_generation_frozen",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_candidate_created",
        "canonical_dataset_frozen",
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
        "acquisition_authorization_artifact_created",
        "acquisition_execution_artifact_created",
        "dataset_generation_authorization_created",
        "canonical_dataset_artifact_created",
        "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    )
    for field in true_fields:
        _expect_true(candidate.get(field), field)
    for field in false_fields:
        _expect_false(candidate.get(field), field)
    outputs = candidate.get("planned_outputs")
    if not isinstance(outputs, list) or [row.get("output_name") for row in outputs] != PLANNED_OUTPUT_NAMES:
        raise AcquisitionGenerationChainCandidateError("planned_outputs mismatch")
    if any(row.get("generation_status") != PLANNED_NOT_GENERATED for row in outputs):
        raise AcquisitionGenerationChainCandidateError("planned output generated")
    if any(row.get("actionability") != RESEARCH_ONLY_NON_ACTIONABLE for row in outputs):
        raise AcquisitionGenerationChainCandidateError("planned output actionable")
    _validate_per_ticker(candidate)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationChainCandidateError("candidate_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise AcquisitionGenerationChainCandidateError("candidate checklist failed")
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get("acquisition_generation_chain_candidate_digest")
    _expect_digest(digest, "acquisition_generation_chain_candidate_digest")
    _expect(
        digest,
        acquisition_generation_chain_candidate_digest_v1(candidate),
        "acquisition_generation_chain_candidate_digest",
    )
    return {
        "status": "ACQUISITION_GENERATION_CHAIN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "acquisition_generation_chain_candidate_digest": digest,
        **{
            key: candidate["candidate_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_acquisition_generation_chain_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    validation = validate_acquisition_generation_chain_candidate_v1(candidate)
    lines = [
        "# MarketFlow Acquisition Generation Chain Candidate Status",
        "",
        "## Title",
        "- Acquisition Generation Chain Candidate v1.",
        "",
        "## Acquisition Generation Chain Candidate",
        f"- Artifact/status: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}`.",
        f"- Digest: `{validation['acquisition_generation_chain_candidate_digest']}`.",
        "",
        "## Source Corporate-Action Authority Approval",
        f"- Approval digest: `{candidate['corporate_action_authority_approval_digest']}`.",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE),
        "",
        "## Per-Ticker Acquisition Chain Candidate Entries",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['acquisition_generation_chain_status']}`; acquisition `{row['market_data_acquisition_status']}`."
        for row in candidate["per_ticker_acquisition_generation_chain_candidates"]
    )
    lines.extend(["", "## Acquisition Planning Dimensions"])
    lines.extend(f"- `{item}`." for item in ACQUISITION_PLANNING_DIMENSIONS)
    lines.extend(["", "## Future Provider Request Policy"])
    lines.extend(
        f"- `{key}`: `{value}`."
        for key, value in FUTURE_ACQUISITION_PROVIDER_REQUEST_POLICY.items()
    )
    lines.extend(["", "## Future Acquisition Chain"])
    lines.extend(
        f"{index}. {item}" for index, item in enumerate(FUTURE_ACQUISITION_CHAIN, start=1)
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`." for item in FUTURE_GATES)
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`." for item in RISK_CONTROLS)
    lines.extend(
        [
            "",
            "## Acquisition Boundary",
            "- Candidate only; acquisition is neither authorized nor executed.",
            "",
            "## Dataset Boundary",
            "- Dataset generation remains not authorized.",
            "",
            "## Canonical Dataset Boundary",
            "- No canonical dataset candidate, authorization, or freeze was created.",
            "",
            "## Registry Boundary",
            "- No registry approval was created.",
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
            "- No provider request, acquisition, dataset generation, predictive execution, or runtime activation occurred.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_acquisition_generation_chain_candidate_v1(
    output_dir: str | Path,
) -> dict[str, Any]:
    candidate = build_acquisition_generation_chain_candidate_v1()
    output_path = Path(output_dir)
    json_path = output_path / "acquisition_generation_chain_candidate_v1.json"
    markdown_path = output_path / "acquisition_generation_chain_candidate_v1.md"
    if json_path.exists() or markdown_path.exists():
        raise AcquisitionGenerationChainCandidateError(
            "acquisition-generation chain candidate output already exists"
        )
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(candidate))
    markdown_path.write_text(
        build_acquisition_generation_chain_candidate_markdown_v1(candidate),
        encoding="utf-8",
    )
    return {
        "candidate": candidate,
        "validation": validate_acquisition_generation_chain_candidate_v1(candidate),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
