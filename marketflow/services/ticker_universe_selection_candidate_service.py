"""Offline ticker universe selection candidate for operator review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    predictive_evidence_scope_expansion_plan_candidate_operator_review_service as scope_review,
)


ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE = "TICKER_UNIVERSE_SELECTION_CANDIDATE"
SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_V1 = (
    "ticker_universe_selection_candidate_v1"
)
TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW = (
    "TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW"
)

DEFAULT_PROPOSED_TICKER_UNIVERSE = [
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

EXISTING_BASELINE_TICKER = "AAPL"
TARGET_ADDITIONAL_TICKER_COUNT_RANGE = "5_to_12"
CANDIDATE_TICKER_LIST_STATUS = (
    "CANDIDATE_UNVALIDATED_REQUIRES_FUTURE_OPERATOR_REVIEW_AND_LIVE_VALIDATION"
)
INTENDED_DIVERSITY_TAGS_STATUS = "INTENDED_DIVERSITY_TAGS_UNVERIFIED"
PROPOSED_UNVALIDATED = "PROPOSED_UNVALIDATED"
NOT_PERFORMED = "NOT_PERFORMED"
NOT_VERIFIED = "NOT_VERIFIED"
NOT_CREATED = "NOT_CREATED"
NOT_AUTHORIZED = scope_review.NOT_AUTHORIZED
PLANNED_NOT_GENERATED = scope_review.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = scope_review.RESEARCH_ONLY_NON_ACTIONABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST = (
    "c94fd093f1e221e9dca127e44a3a788880602c570e9051b6e19666f1db142156"
)
EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST = (
    scope_review.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST = (
    scope_review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    scope_review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    scope_review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    scope_review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    scope_review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    scope_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    scope_review.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = scope_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    scope_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

SCOPE_EXPANSION_OBJECTIVE = scope_review.SCOPE_EXPANSION_OBJECTIVE
FUTURE_AUTHORITY_CHAIN_STEPS = list(scope_review.FUTURE_TICKER_AUTHORITY_CHAIN)

INTENDED_DIVERSITY_TAGS_BY_TICKER = {
    "MSFT": ["large_cap_technology_or_software_like"],
    "NVDA": ["semiconductor_or_hardware_like", "high_beta_growth_like"],
    "AMZN": ["consumer_or_ecommerce_like", "internet_or_platform_like"],
    "GOOGL": ["internet_or_platform_like"],
    "META": ["internet_or_platform_like", "high_beta_growth_like"],
    "TSLA": ["high_beta_growth_like", "consumer_or_ecommerce_like"],
    "JPM": ["financial_like"],
    "XOM": ["energy_or_commodity_sensitive_like"],
    "JNJ": ["healthcare_or_defensive_like"],
    "WMT": ["retail_or_consumer_staples_like"],
    "CAT": ["industrial_or_machinery_like"],
    "LMT": ["aerospace_defense_or_industrial_like"],
}

SELECTION_RATIONALE = [
    "address_single_ticker_scope",
    "increase_cross_profile_replication",
    "increase_regime_diversity",
    "support_future_generalization_assessment",
    "support_future_multi_ticker_predictive_evidence",
]

FUTURE_VALIDATION_GATES = [
    "ticker_universe_selection_candidate_operator_review",
    "ticker_universe_selection_approval_ceremony",
    "live_ticker_validation_authority",
    "security_type_validation",
    "exchange_listing_validation",
    "identity_segment_authority_per_ticker",
    "corporate_action_audit_chain_per_ticker",
    "acquisition_generation_authority_per_ticker",
    "canonical_dataset_authority_per_ticker",
    "research_registry_approval_per_ticker",
    "dataset_file_availability_verification_per_ticker",
    "multi_ticker_research_campaign_authority",
    "multi_ticker_predictive_experiment_authority",
]

PLANNED_OUTPUT_IDS = [
    "ticker_universe_selection_candidate_manifest",
    "unvalidated_candidate_ticker_list",
    "ticker_selection_rationale_report",
    "intended_diversity_tag_matrix",
    "future_validation_gate_plan",
    "per_ticker_authority_chain_requirement_report",
    "scope_expansion_operator_review_summary",
]

REQUIRED_CHECK_IDS = [
    "scope_expansion_review_digest_bound",
    "scope_expansion_candidate_digest_bound",
    "additional_predictive_evidence_review_digest_bound",
    "readiness_review_digest_bound",
    "predictive_experiment_results_review_digest_bound",
    "existing_baseline_ticker_aapl_bound",
    "proposed_candidate_ticker_count_12",
    "proposed_candidate_tickers_unique",
    "aapl_not_in_proposed_candidate_universe",
    "candidate_ticker_list_unvalidated",
    "approved_expanded_ticker_universe_empty",
    "approved_expanded_ticker_count_zero",
    "live_ticker_validation_performed_false",
    "final_ticker_selection_performed_false",
    "ticker_universe_selection_approved_false",
    "scope_expansion_authorized_false",
    "expanded_ticker_universe_approved_false",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "provider_requests_made_false",
    "candidate_entries_status_unvalidated",
    "candidate_entries_listing_not_verified",
    "candidate_entries_security_type_not_verified",
    "candidate_entries_exchange_not_verified",
    "candidate_entries_authority_not_created",
    "candidate_entries_runtime_not_authorized",
    "intended_diversity_tags_unverified",
    "selection_rationale_research_only",
    "future_validation_gates_defined",
    "future_authority_chain_15_steps",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "predictive_experiment_rerun_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_recommended_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "no_ticker_universe_selection_approval_created",
    "no_expanded_ticker_universe_approval_created",
    "no_new_ticker_authority_created",
    "no_acquisition_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class TickerUniverseSelectionCandidateError(ValueError):
    """Raised when the ticker universe selection candidate is invalid."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
    message: str | None = None,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise TickerUniverseSelectionCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise TickerUniverseSelectionCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise TickerUniverseSelectionCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _normalize_proposed_tickers(proposed_tickers: list[str] | None) -> list[str]:
    tickers = list(DEFAULT_PROPOSED_TICKER_UNIVERSE if proposed_tickers is None else proposed_tickers)
    return [str(ticker).upper() for ticker in tickers]


def _candidate_ticker_entries(tickers: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "ticker": ticker,
            "candidate_entry_status": PROPOSED_UNVALIDATED,
            "live_validation_status": NOT_PERFORMED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "sector_status": NOT_VERIFIED,
            "liquidity_status": NOT_VERIFIED,
            "market_cap_status": NOT_VERIFIED,
            "corporate_action_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
            "intended_diversity_tags": list(INTENDED_DIVERSITY_TAGS_BY_TICKER.get(ticker, [])),
        }
        for ticker in tickers
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _future_authority_chain() -> list[dict[str, Any]]:
    return [
        {
            "step_number": index,
            "authority_step": step,
            "performed_in_this_task": False,
            "required_before_acquisition": True,
        }
        for index, step in enumerate(FUTURE_AUTHORITY_CHAIN_STEPS, start=1)
    ]


def _base_candidate(proposed_tickers: list[str]) -> dict[str, Any]:
    entries = _candidate_ticker_entries(proposed_tickers)
    return {
        "artifact_kind": ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_V1,
        "candidate_status": TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_ticker_validation_performed": False,
        "final_ticker_selection_performed": False,
        "ticker_universe_selection_approved": False,
        "ticker_universe_selection_candidate_created": True,
        "scope_expansion_authorized": False,
        "expanded_ticker_universe_approved": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
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
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
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
        "operator_review_required": True,
        "selection_approval_requires_operator_ceremony": True,
        "ticker_universe_selection_approval_created": False,
        "expanded_ticker_universe_approval_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST,
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "existing_baseline_ticker": EXISTING_BASELINE_TICKER,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "proposed_candidate_ticker_universe": proposed_tickers,
        "proposed_candidate_ticker_count": len(proposed_tickers),
        "target_additional_ticker_count_range": TARGET_ADDITIONAL_TICKER_COUNT_RANGE,
        "candidate_ticker_list_status": CANDIDATE_TICKER_LIST_STATUS,
        "approved_expanded_ticker_universe": [],
        "approved_expanded_ticker_count": 0,
        "candidate_ticker_entries": entries,
        "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
        "intended_diversity_tags": deepcopy(INTENDED_DIVERSITY_TAGS_BY_TICKER),
        "selection_rationale": list(SELECTION_RATIONALE),
        "selection_rationale_status": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_validation_gates": list(FUTURE_VALIDATION_GATES),
        "future_validation_gate_count": len(FUTURE_VALIDATION_GATES),
        "future_ticker_authority_chain": _future_authority_chain(),
        "future_ticker_authority_chain_step_count": len(FUTURE_AUTHORITY_CHAIN_STEPS),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
    }


def _all_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("candidate_ticker_entries")
    return entries if isinstance(entries, list) else []


def _entries_have(expected_field: str, expected_value: Any, candidate: dict[str, Any]) -> bool:
    entries = _all_entries(candidate)
    return bool(entries) and all(entry.get(expected_field) == expected_value for entry in entries)


def _entry_authorities_not_created(candidate: dict[str, Any]) -> bool:
    fields = (
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    entries = _all_entries(candidate)
    return bool(entries) and all(entry.get(field) == NOT_CREATED for entry in entries for field in fields)


def _entry_uses_not_authorized(candidate: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "broker_execution", "paper_trading")
    entries = _all_entries(candidate)
    return bool(entries) and all(entry.get(field) == NOT_AUTHORIZED for entry in entries for field in fields)


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    tickers = candidate.get("proposed_candidate_ticker_universe", [])
    planned_outputs = candidate.get("planned_outputs", [])
    entries = _all_entries(candidate)
    return [
        _check("scope_expansion_review_digest_bound", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_evidence_scope_expansion_plan_candidate_review_package_digest")),
        _check("scope_expansion_candidate_digest_bound", EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST, candidate.get("predictive_evidence_scope_expansion_plan_candidate_digest")),
        _check("additional_predictive_evidence_review_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST, candidate.get("additional_predictive_evidence_plan_candidate_review_package_digest")),
        _check("readiness_review_digest_bound", EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_experiment_results_review_package_digest")),
        _check("existing_baseline_ticker_aapl_bound", EXISTING_BASELINE_TICKER, candidate.get("existing_baseline_ticker")),
        _check("proposed_candidate_ticker_count_12", 12, candidate.get("proposed_candidate_ticker_count")),
        _check("proposed_candidate_tickers_unique", True, len(tickers) == len(set(tickers))),
        _check("aapl_not_in_proposed_candidate_universe", True, EXISTING_BASELINE_TICKER not in tickers),
        _check("candidate_ticker_list_unvalidated", CANDIDATE_TICKER_LIST_STATUS, candidate.get("candidate_ticker_list_status")),
        _check("approved_expanded_ticker_universe_empty", [], candidate.get("approved_expanded_ticker_universe")),
        _check("approved_expanded_ticker_count_zero", 0, candidate.get("approved_expanded_ticker_count")),
        _check("live_ticker_validation_performed_false", False, candidate.get("live_ticker_validation_performed")),
        _check("final_ticker_selection_performed_false", False, candidate.get("final_ticker_selection_performed")),
        _check("ticker_universe_selection_approved_false", False, candidate.get("ticker_universe_selection_approved")),
        _check("scope_expansion_authorized_false", False, candidate.get("scope_expansion_authorized")),
        _check("expanded_ticker_universe_approved_false", False, candidate.get("expanded_ticker_universe_approved")),
        _check("new_ticker_authority_created_false", False, candidate.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("candidate_entries_status_unvalidated", True, _entries_have("candidate_entry_status", PROPOSED_UNVALIDATED, candidate)),
        _check("candidate_entries_listing_not_verified", True, _entries_have("listing_status", NOT_VERIFIED, candidate)),
        _check("candidate_entries_security_type_not_verified", True, _entries_have("security_type_status", NOT_VERIFIED, candidate)),
        _check("candidate_entries_exchange_not_verified", True, _entries_have("exchange_status", NOT_VERIFIED, candidate)),
        _check("candidate_entries_authority_not_created", True, _entry_authorities_not_created(candidate)),
        _check("candidate_entries_runtime_not_authorized", True, _entry_uses_not_authorized(candidate)),
        _check("intended_diversity_tags_unverified", INTENDED_DIVERSITY_TAGS_STATUS, candidate.get("intended_diversity_tags_status")),
        _check("selection_rationale_research_only", RESEARCH_ONLY_NON_ACTIONABLE, candidate.get("selection_rationale_status")),
        _check("future_validation_gates_defined", FUTURE_VALIDATION_GATES, candidate.get("future_validation_gates")),
        _check("future_authority_chain_15_steps", 15, candidate.get("future_ticker_authority_chain_step_count")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("additional_predictive_evidence_execution_authorized_false", False, candidate.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, candidate.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, candidate.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, candidate.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, candidate.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, candidate.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, candidate.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, candidate.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, candidate.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, candidate.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_ticker_universe_selection_approval_created", False, candidate.get("ticker_universe_selection_approval_created")),
        _check("no_expanded_ticker_universe_approval_created", False, candidate.get("expanded_ticker_universe_approval_created")),
        _check("no_new_ticker_authority_created", False, candidate.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_artifact_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_artifact_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": failed == 0,
        "ready_for_ticker_universe_selection_approval": False,
        "ready_for_live_ticker_validation": False,
        "ready_for_new_ticker_authority_chain": False,
        "ready_for_acquisition": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("ticker_universe_selection_candidate_digest", None)
    return payload


def ticker_universe_selection_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic digest for the ticker universe selection candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_ticker_universe_selection_candidate_v1(
    proposed_tickers: list[str] | None = None,
) -> dict[str, Any]:
    """Build an offline unvalidated ticker universe selection candidate."""
    candidate = _base_candidate(_normalize_proposed_tickers(proposed_tickers))
    candidate["selection_checklist"] = _checklist(candidate)
    candidate["selection_summary"] = _summary(candidate["selection_checklist"])
    candidate["ticker_universe_selection_candidate_digest"] = (
        ticker_universe_selection_candidate_digest_v1(candidate)
    )
    validate_ticker_universe_selection_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    forbidden_artifact_values = {
        "TICKER_UNIVERSE_SELECTION_APPROVED",
        "EXPANDED_TICKER_UNIVERSE_APPROVED",
        "NEW_TICKER_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true_fields = {
        "provider_requests_made",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_approved",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
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
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_artifact_values:
            raise TickerUniverseSelectionCandidateError(f"{current_path} must not emit {value}")
        if key in forbidden_true_fields and value is True:
            raise TickerUniverseSelectionCandidateError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise TickerUniverseSelectionCandidateError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise TickerUniverseSelectionCandidateError(f"{current_path} must not be accepted")
        if key == "approved_expanded_ticker_universe" and value:
            raise TickerUniverseSelectionCandidateError(f"{current_path} must be empty")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_candidate_entries(candidate: dict[str, Any]) -> None:
    tickers = candidate.get("proposed_candidate_ticker_universe")
    entries = candidate.get("candidate_ticker_entries")
    if not isinstance(tickers, list) or not tickers:
        raise TickerUniverseSelectionCandidateError("proposed_candidate_ticker_universe missing")
    if EXISTING_BASELINE_TICKER in tickers:
        raise TickerUniverseSelectionCandidateError("proposed ticker universe must not contain AAPL")
    if len(tickers) != len(set(tickers)):
        raise TickerUniverseSelectionCandidateError("proposed ticker universe contains duplicates")
    if not isinstance(entries, list) or len(entries) != len(tickers):
        raise TickerUniverseSelectionCandidateError("candidate_ticker_entries mismatch")
    for entry in entries:
        ticker = entry.get("ticker")
        if ticker not in tickers:
            raise TickerUniverseSelectionCandidateError("candidate ticker entry mismatch")
        for field, expected in {
            "candidate_entry_status": PROPOSED_UNVALIDATED,
            "live_validation_status": NOT_PERFORMED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "sector_status": NOT_VERIFIED,
            "liquidity_status": NOT_VERIFIED,
            "market_cap_status": NOT_VERIFIED,
            "corporate_action_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
        }.items():
            _expect(entry.get(field), expected, f"candidate_ticker_entries.{ticker}.{field}")


def validate_ticker_universe_selection_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the candidate while preserving offline, unapproved boundaries."""
    if not isinstance(candidate, dict):
        raise TickerUniverseSelectionCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline",
        "ticker_universe_selection_candidate_created",
        "research_only",
        "operator_review_required",
        "selection_approval_requires_operator_ceremony",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_approved",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
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
        "ticker_universe_selection_approval_created",
        "expanded_ticker_universe_approval_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "scope_expansion_objective": SCOPE_EXPANSION_OBJECTIVE,
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": (
            EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
        ),
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST,
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "existing_baseline_ticker": EXISTING_BASELINE_TICKER,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
        "target_additional_ticker_count_range": TARGET_ADDITIONAL_TICKER_COUNT_RANGE,
        "candidate_ticker_list_status": CANDIDATE_TICKER_LIST_STATUS,
        "approved_expanded_ticker_universe": [],
        "approved_expanded_ticker_count": 0,
        "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
        "selection_rationale": SELECTION_RATIONALE,
        "selection_rationale_status": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_validation_gates": FUTURE_VALIDATION_GATES,
        "future_validation_gate_count": len(FUTURE_VALIDATION_GATES),
        "future_ticker_authority_chain": _future_authority_chain(),
        "future_ticker_authority_chain_step_count": len(FUTURE_AUTHORITY_CHAIN_STEPS),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
    }.items():
        value = candidate.get(field)
        if field in {"future_validation_gates", "future_ticker_authority_chain", "planned_outputs"} and not value:
            raise TickerUniverseSelectionCandidateError(f"{field} missing")
        _expect(value, expected, field)
    _validate_candidate_entries(candidate)
    checklist = candidate.get("selection_checklist")
    if not isinstance(checklist, list):
        raise TickerUniverseSelectionCandidateError("selection_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "selection_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise TickerUniverseSelectionCandidateError(
            f"selection checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "selection_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("selection_summary"), expected_summary, "selection_summary")
    digest = candidate.get("ticker_universe_selection_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise TickerUniverseSelectionCandidateError("ticker_universe_selection_candidate_digest missing")
    _expect(digest, ticker_universe_selection_candidate_digest_v1(candidate), "ticker_universe_selection_candidate_digest")
    return {
        "status": "TICKER_UNIVERSE_SELECTION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "ticker_universe_selection_candidate_digest": digest,
        "proposed_candidate_ticker_count": candidate["proposed_candidate_ticker_count"],
        "candidate_ticker_list_status": candidate["candidate_ticker_list_status"],
        "ready_for_operator_review": candidate["selection_summary"]["ready_for_operator_review"],
        "ready_for_ticker_universe_selection_approval": False,
        "ready_for_live_ticker_validation": False,
        "ready_for_new_ticker_authority_chain": False,
        "ready_for_acquisition": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_ticker_universe_selection_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized ticker universe selection candidate summary."""
    validation = validate_ticker_universe_selection_candidate_v1(candidate)
    summary = candidate["selection_summary"]
    lines = [
        "# MarketFlow Ticker Universe Selection Candidate Status",
        "",
        "## Title",
        "- Ticker Universe Selection Candidate v1.",
        "",
        "## Purpose",
        "- Propose an offline, unvalidated ticker universe for operator review.",
        "- This candidate does not approve tickers, validate live listings, create authority, acquire data, execute experiments, score strategies, or authorize runtime use.",
        "",
        "## Source Scope Expansion Evidence",
        f"- Scope expansion review package digest: `{candidate['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        f"- Scope expansion candidate digest: `{candidate['predictive_evidence_scope_expansion_plan_candidate_digest']}`",
        f"- Candidate digest: `{validation['ticker_universe_selection_candidate_digest']}`",
        "",
        "## Proposed Unvalidated Candidate Ticker Universe",
        f"- Existing baseline ticker: `{candidate['existing_baseline_ticker']}`",
        f"- Candidate ticker list status: `{candidate['candidate_ticker_list_status']}`",
        f"- Proposed candidate ticker count: `{candidate['proposed_candidate_ticker_count']}`",
    ]
    lines.extend(f"- `{ticker}`" for ticker in candidate["proposed_candidate_ticker_universe"])
    lines.extend(
        [
            "",
            "## Intended Diversity Tags",
            f"- intended_diversity_tags_status: `{candidate['intended_diversity_tags_status']}`",
            "- Tags are planning labels only, not validated classifications.",
            "",
            "## Selection Rationale",
        ]
    )
    lines.extend(f"- `{item}`" for item in candidate["selection_rationale"])
    lines.extend(["", "## Future Validation Required"])
    lines.extend(f"- `{gate}`" for gate in candidate["future_validation_gates"])
    lines.extend(["", "## Future Per-Ticker Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: `{step['authority_step']}`"
        for step in candidate["future_ticker_authority_chain"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in candidate["planned_outputs"]
    )
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- ticker_universe_selection_approved: `{candidate['ticker_universe_selection_approved']}`",
            f"- expanded_ticker_universe_approved: `{candidate['expanded_ticker_universe_approved']}`",
            f"- approved_expanded_ticker_universe: `{candidate['approved_expanded_ticker_universe']}`",
            f"- live_ticker_validation_performed: `{candidate['live_ticker_validation_performed']}`",
            f"- final_ticker_selection_performed: `{candidate['final_ticker_selection_performed']}`",
            f"- new_ticker_authority_created: `{candidate['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{candidate['new_ticker_acquisition_authorized']}`",
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- ready_for_operator_review: `{summary['ready_for_operator_review']}`",
            f"- ready_for_ticker_universe_selection_approval: `{summary['ready_for_ticker_universe_selection_approval']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation or current listing verification occurred.",
            "- No final ticker selection or approved ticker universe was created.",
            "- No new ticker authority, acquisition authority, dataset generation, experiment execution, strategy scoring, or runtime activation occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_ticker_universe_selection_candidate_v1(
    output_dir: str | Path,
    *,
    proposed_tickers: list[str] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the ticker universe selection candidate without overwriting output."""
    candidate = build_ticker_universe_selection_candidate_v1(proposed_tickers=proposed_tickers)
    validation = validate_ticker_universe_selection_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "ticker_universe_selection_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise TickerUniverseSelectionCandidateError(
            "ticker universe selection candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise TickerUniverseSelectionCandidateError(
            "ticker universe selection candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
