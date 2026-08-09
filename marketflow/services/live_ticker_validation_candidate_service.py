"""Offline live ticker validation candidate for operator review."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import ticker_universe_selection_approval_service as selection_approval


ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE = "LIVE_TICKER_VALIDATION_CANDIDATE"
SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_V1 = (
    "live_ticker_validation_candidate_v1"
)
LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW = (
    "LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW"
)
APPROVED_FOR_FUTURE_VALIDATION_ONLY = "APPROVED_FOR_FUTURE_VALIDATION_ONLY"
PLANNED_REQUIRES_SEPARATE_APPROVAL = "PLANNED_REQUIRES_SEPARATE_APPROVAL"
READ_ONLY_VALIDATION_REQUESTS_ONLY = "READ_ONLY_VALIDATION_REQUESTS_ONLY"
DO_NOT_STORE_KEYS_OR_PRINT_KEYS = "DO_NOT_STORE_KEYS_OR_PRINT_KEYS"
DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS = "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS"
RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED = "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED"
VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY = (
    "VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY"
)
NOT_REQUESTED = "NOT_REQUESTED"
NOT_PERFORMED = selection_approval.NOT_PERFORMED
NOT_VERIFIED = selection_approval.NOT_VERIFIED
NOT_CREATED = selection_approval.NOT_CREATED
NOT_AUTHORIZED = selection_approval.NOT_AUTHORIZED
PLANNED_NOT_GENERATED = selection_approval.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = selection_approval.RESEARCH_ONLY_NON_ACTIONABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    "e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c"
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE = (
    selection_approval.TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST = (
    selection_approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    selection_approval.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST = (
    selection_approval.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST = (
    selection_approval.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST = (
    selection_approval.candidate_review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    selection_approval.candidate_review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    selection_approval.candidate_review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    selection_approval.candidate_review.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)

APPROVED_EXPANDED_TICKER_UNIVERSE = list(selection_approval.APPROVED_EXPANDED_TICKER_UNIVERSE)

PLANNED_VALIDATION_CHECKS = [
    (
        "ticker_symbol_recognized_by_provider",
        "Confirm the future provider can recognize the approved ticker symbol.",
    ),
    ("security_type_check", "Confirm the future provider reports the expected security type."),
    ("primary_exchange_check", "Confirm the future provider reports a primary exchange."),
    ("listing_active_status_check", "Confirm active listing status during future validation."),
    (
        "delisting_or_inactive_status_check",
        "Check whether future provider metadata reports delisting or inactive status.",
    ),
    (
        "historical_data_availability_check",
        "Confirm future historical aggregate availability without acquiring data authority.",
    ),
    (
        "corporate_action_endpoint_availability_check",
        "Confirm future corporate action endpoint availability without freezing events.",
    ),
    ("split_data_availability_check", "Confirm future split data availability."),
    ("dividend_data_availability_check", "Confirm future dividend data availability."),
    (
        "data_range_coverage_feasibility_check",
        "Assess future feasibility for required date-range coverage.",
    ),
    (
        "provider_symbol_mapping_consistency_check",
        "Compare future provider symbol mapping against approved ticker identity.",
    ),
]

PLANNED_OUTPUT_IDS = [
    "live_ticker_validation_request_manifest",
    "planned_validation_checklist",
    "provider_request_plan",
    "ticker_validation_result_template",
    "validation_failure_reason_inventory_template",
    "operator_review_summary_template",
]

FUTURE_GATES = [
    "live_ticker_validation_candidate_operator_review",
    "live_ticker_validation_approval_ceremony",
    "api_key_handling_confirmation",
    "provider_request_boundary_confirmation",
    "raw_payload_non_commitment_confirmation",
    "live_validation_execution",
    "live_validation_results_operator_review",
    "per_ticker_identity_authority_candidate",
    "per_ticker_corporate_action_authority_candidate",
    "per_ticker_acquisition_authority_candidate",
]

RISK_CONTROLS = [
    "no_provider_request_without_approval",
    "no_api_key_storage",
    "no_raw_payload_commit",
    "no_acquisition_authority_from_validation",
    "no_dataset_generation_authority_from_validation",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "all_outputs_labeled_research_only",
    "operator_approval_required_before_live_validation",
]

REQUIRED_CHECK_IDS = [
    "ticker_universe_selection_approval_digest_bound",
    "ticker_universe_selection_candidate_digest_bound",
    "ticker_universe_selection_review_digest_bound",
    "scope_expansion_review_digest_bound",
    "approved_ticker_count_12",
    "approved_tickers_match_selection_approval",
    "validation_target_entries_12",
    "validation_targets_status_future_validation_only",
    "provider_requests_made_false",
    "provider_request_authorized_false",
    "live_provider_transport_enabled_false",
    "live_ticker_validation_authorized_false",
    "live_ticker_validation_performed_false",
    "validation_targets_not_requested",
    "validation_targets_live_validation_not_performed",
    "validation_targets_listing_not_verified",
    "validation_targets_security_type_not_verified",
    "validation_targets_exchange_not_verified",
    "validation_targets_active_status_not_verified",
    "validation_targets_authority_not_created",
    "validation_targets_runtime_not_authorized",
    "planned_validation_checks_defined",
    "planned_validation_checks_not_performed",
    "provider_request_policy_requires_separate_approval",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "future_gates_defined",
    "risk_controls_defined",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
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
    "no_live_ticker_validation_artifact_created",
    "no_live_validation_results_created",
    "no_new_ticker_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class LiveTickerValidationCandidateError(ValueError):
    """Raised when the live ticker validation candidate is invalid."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": f"{check_id} passed" if status == PASS else f"{check_id} failed",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise LiveTickerValidationCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise LiveTickerValidationCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise LiveTickerValidationCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _validation_target_entries(tickers: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "ticker": ticker,
            "validation_target_status": APPROVED_FOR_FUTURE_VALIDATION_ONLY,
            "live_validation_status": NOT_PERFORMED,
            "provider_request_status": NOT_REQUESTED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "active_status": NOT_VERIFIED,
            "delisting_status": NOT_VERIFIED,
            "tradability_status": NOT_VERIFIED,
            "corporate_action_data_availability_status": NOT_VERIFIED,
            "historical_aggregate_data_availability_status": NOT_VERIFIED,
            "identity_authority_status": NOT_CREATED,
            "split_event_authority_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for ticker in tickers
    ]


def _planned_validation_checks() -> list[dict[str, Any]]:
    return [
        {
            "check_name": check_name,
            "purpose": purpose,
            "planned_provider_interaction_required": True,
            "performed_now": False,
            "operator_approval_required_before_execution": True,
        }
        for check_name, purpose in PLANNED_VALIDATION_CHECKS
    ]


def _provider_request_policy() -> dict[str, Any]:
    return {
        "future_provider_request_policy_status": PLANNED_REQUIRES_SEPARATE_APPROVAL,
        "allowed_future_request_type": READ_ONLY_VALIDATION_REQUESTS_ONLY,
        "api_key_handling": DO_NOT_STORE_KEYS_OR_PRINT_KEYS,
        "raw_payload_policy": DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS,
        "sanitized_status_doc_required": True,
        "rate_limit_policy": RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED,
        "provider_result_authority": VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY,
    }


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_id": output_id,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _all_targets(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("validation_target_entries")
    return entries if isinstance(entries, list) else []


def _targets_have(field: str, expected: Any, candidate: dict[str, Any]) -> bool:
    targets = _all_targets(candidate)
    return bool(targets) and all(target.get(field) == expected for target in targets)


def _target_authorities_not_created(candidate: dict[str, Any]) -> bool:
    fields = (
        "identity_authority_status",
        "split_event_authority_status",
        "dividend_event_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    targets = _all_targets(candidate)
    return bool(targets) and all(
        target.get(field) == NOT_CREATED for target in targets for field in fields
    )


def _target_uses_not_authorized(candidate: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "paper_trading", "broker_execution")
    targets = _all_targets(candidate)
    return bool(targets) and all(
        target.get(field) == NOT_AUTHORIZED for target in targets for field in fields
    )


def _planned_checks_valid(candidate: dict[str, Any]) -> bool:
    checks = candidate.get("planned_validation_checks")
    expected_names = [name for name, _purpose in PLANNED_VALIDATION_CHECKS]
    if not isinstance(checks, list) or len(checks) != len(expected_names):
        return False
    return (
        [item.get("check_name") for item in checks if isinstance(item, dict)] == expected_names
        and all(item.get("planned_provider_interaction_required") is True for item in checks)
        and all(item.get("performed_now") is False for item in checks)
        and all(item.get("operator_approval_required_before_execution") is True for item in checks)
    )


def _planned_outputs_valid(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return (
        isinstance(outputs, list)
        and len(outputs) == len(PLANNED_OUTPUT_IDS)
        and [item.get("output_id") for item in outputs if isinstance(item, dict)] == PLANNED_OUTPUT_IDS
        and all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs)
        and all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)
    )


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    targets = _all_targets(candidate)
    target_tickers = [target.get("ticker") for target in targets if isinstance(target, dict)]
    return [
        _check("ticker_universe_selection_approval_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, candidate.get("ticker_universe_selection_approval_digest")),
        _check("ticker_universe_selection_candidate_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, candidate.get("ticker_universe_selection_candidate_digest")),
        _check("ticker_universe_selection_review_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("ticker_universe_selection_candidate_review_package_digest")),
        _check("scope_expansion_review_digest_bound", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, candidate.get("predictive_evidence_scope_expansion_plan_candidate_review_package_digest")),
        _check("approved_ticker_count_12", 12, candidate.get("approved_expanded_ticker_count")),
        _check("approved_tickers_match_selection_approval", APPROVED_EXPANDED_TICKER_UNIVERSE, candidate.get("approved_expanded_ticker_universe")),
        _check("validation_target_entries_12", 12, candidate.get("validation_target_count")),
        _check("validation_targets_status_future_validation_only", True, _targets_have("validation_target_status", APPROVED_FOR_FUTURE_VALIDATION_ONLY, candidate)),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("provider_request_authorized_false", False, candidate.get("provider_request_authorized")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("live_ticker_validation_authorized_false", False, candidate.get("live_ticker_validation_authorized")),
        _check("live_ticker_validation_performed_false", False, candidate.get("live_ticker_validation_performed")),
        _check("validation_targets_not_requested", True, _targets_have("provider_request_status", NOT_REQUESTED, candidate)),
        _check("validation_targets_live_validation_not_performed", True, _targets_have("live_validation_status", NOT_PERFORMED, candidate)),
        _check("validation_targets_listing_not_verified", True, _targets_have("listing_status", NOT_VERIFIED, candidate)),
        _check("validation_targets_security_type_not_verified", True, _targets_have("security_type_status", NOT_VERIFIED, candidate)),
        _check("validation_targets_exchange_not_verified", True, _targets_have("exchange_status", NOT_VERIFIED, candidate)),
        _check("validation_targets_active_status_not_verified", True, _targets_have("active_status", NOT_VERIFIED, candidate)),
        _check("validation_targets_authority_not_created", True, _target_authorities_not_created(candidate)),
        _check("validation_targets_runtime_not_authorized", True, _target_uses_not_authorized(candidate)),
        _check("planned_validation_checks_defined", True, _planned_checks_valid(candidate)),
        _check("planned_validation_checks_not_performed", True, all(item.get("performed_now") is False for item in candidate.get("planned_validation_checks", []))),
        _check("provider_request_policy_requires_separate_approval", PLANNED_REQUIRES_SEPARATE_APPROVAL, candidate.get("provider_request_policy", {}).get("future_provider_request_policy_status") if isinstance(candidate.get("provider_request_policy"), dict) else None),
        _check("planned_outputs_not_generated", True, _planned_outputs_valid(candidate)),
        _check("planned_outputs_research_only", True, _planned_outputs_valid(candidate)),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("new_ticker_authority_created_false", False, candidate.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, candidate.get("dataset_generation_authorized")),
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
        _check("no_live_ticker_validation_artifact_created", False, candidate.get("live_ticker_validation_artifact_created")),
        _check("no_live_validation_results_created", False, candidate.get("live_validation_results_created")),
        _check("no_new_ticker_authority_artifact_created", False, candidate.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_artifact_created")),
        _check("no_dataset_generation_authorization_created", False, candidate.get("dataset_generation_authorization_created")),
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
        "ready_for_live_ticker_validation_approval": False,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "new_ticker_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _base_candidate() -> dict[str, Any]:
    tickers = list(APPROVED_EXPANDED_TICKER_UNIVERSE)
    return {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_V1,
        "candidate_status": LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "provider_request_authorized": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_candidate_created": True,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
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
        "validation_execution_requires_operator_approval": True,
        "live_ticker_validation_artifact_created": False,
        "live_validation_results_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "ticker_universe_selection_approval_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_scope": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE
        ),
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
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
        "approved_expanded_ticker_universe": tickers,
        "approved_expanded_ticker_count": len(tickers),
        "validation_target_entries": _validation_target_entries(tickers),
        "validation_target_count": len(tickers),
        "planned_validation_checks": _planned_validation_checks(),
        "planned_validation_check_count": len(PLANNED_VALIDATION_CHECKS),
        "provider_request_policy": _provider_request_policy(),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
        "future_gates": list(FUTURE_GATES),
        "future_gate_count": len(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "risk_control_count": len(RISK_CONTROLS),
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("live_ticker_validation_candidate_digest", None)
    return payload


def live_ticker_validation_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic digest for the live ticker validation candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_live_ticker_validation_candidate_v1() -> dict[str, Any]:
    """Build an offline live ticker validation candidate without performing validation."""
    candidate = _base_candidate()
    candidate["validation_checklist"] = _checklist(candidate)
    candidate["validation_summary"] = _summary(candidate["validation_checklist"])
    candidate["live_ticker_validation_candidate_digest"] = (
        live_ticker_validation_candidate_digest_v1(candidate)
    )
    validate_live_ticker_validation_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    forbidden_artifact_values = {
        "LIVE_TICKER_VALIDATION_APPROVED",
        "LIVE_TICKER_VALIDATION_PERFORMED",
        "LIVE_TICKER_VALIDATION_RESULTS",
        "NEW_TICKER_AUTHORITY_APPROVED",
        "NEW_TICKER_ACQUISITION_AUTHORIZED",
        "ACQUISITION_GENERATION_AUTHORIZED",
        "CANONICAL_DATASET_AUTHORIZED",
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
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_artifact_values:
            raise LiveTickerValidationCandidateError(f"{current_path} must not emit {value}")
        if key in forbidden_true_fields and value is True:
            raise LiveTickerValidationCandidateError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise LiveTickerValidationCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise LiveTickerValidationCandidateError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_validation_targets(candidate: dict[str, Any]) -> None:
    tickers = candidate.get("approved_expanded_ticker_universe")
    targets = candidate.get("validation_target_entries")
    if tickers != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise LiveTickerValidationCandidateError("approved ticker universe mismatch")
    if candidate.get("approved_expanded_ticker_count") != len(APPROVED_EXPANDED_TICKER_UNIVERSE):
        raise LiveTickerValidationCandidateError("approved_expanded_ticker_count mismatch")
    if not isinstance(targets, list) or len(targets) != len(APPROVED_EXPANDED_TICKER_UNIVERSE):
        raise LiveTickerValidationCandidateError("validation_target_entries mismatch")
    if candidate.get("validation_target_count") != len(APPROVED_EXPANDED_TICKER_UNIVERSE):
        raise LiveTickerValidationCandidateError("validation_target_count mismatch")
    if [target.get("ticker") for target in targets] != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise LiveTickerValidationCandidateError("validation target tickers mismatch")
    for target in targets:
        ticker = target.get("ticker")
        for field, expected in {
            "validation_target_status": APPROVED_FOR_FUTURE_VALIDATION_ONLY,
            "live_validation_status": NOT_PERFORMED,
            "provider_request_status": NOT_REQUESTED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "active_status": NOT_VERIFIED,
            "delisting_status": NOT_VERIFIED,
            "tradability_status": NOT_VERIFIED,
            "corporate_action_data_availability_status": NOT_VERIFIED,
            "historical_aggregate_data_availability_status": NOT_VERIFIED,
            "identity_authority_status": NOT_CREATED,
            "split_event_authority_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }.items():
            _expect(target.get(field), expected, f"validation_target_entries.{ticker}.{field}")


def _validate_planning_sections(candidate: dict[str, Any]) -> None:
    if not _planned_checks_valid(candidate):
        raise LiveTickerValidationCandidateError("planned_validation_checks mismatch")
    _expect(
        candidate.get("planned_validation_check_count"),
        len(PLANNED_VALIDATION_CHECKS),
        "planned_validation_check_count",
    )
    _expect(candidate.get("provider_request_policy"), _provider_request_policy(), "provider_request_policy")
    if not _planned_outputs_valid(candidate):
        raise LiveTickerValidationCandidateError("planned_outputs mismatch")
    _expect(candidate.get("planned_output_count"), len(PLANNED_OUTPUT_IDS), "planned_output_count")
    _expect(candidate.get("future_gates"), FUTURE_GATES, "future_gates")
    _expect(candidate.get("future_gate_count"), len(FUTURE_GATES), "future_gate_count")
    _expect(candidate.get("risk_controls"), RISK_CONTROLS, "risk_controls")
    _expect(candidate.get("risk_control_count"), len(RISK_CONTROLS), "risk_control_count")


def validate_live_ticker_validation_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the candidate while ensuring no live validation or authority is created."""
    if not isinstance(candidate, dict):
        raise LiveTickerValidationCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_LIVE_TICKER_VALIDATION_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_LIVE_TICKER_VALIDATION_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline",
        "live_ticker_validation_candidate_created",
        "ticker_universe_selection_approved",
        "expanded_ticker_universe_approved",
        "research_only",
        "operator_review_required",
        "validation_execution_requires_operator_approval",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "provider_request_authorized",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
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
        "live_ticker_validation_artifact_created",
        "live_validation_results_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
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
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "ticker_universe_selection_approval_scope": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_SCOPE,
        "ticker_universe_selection_candidate_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST,
        "ticker_universe_selection_candidate_review_package_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST,
        "predictive_evidence_scope_expansion_plan_candidate_digest": EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST,
        "additional_predictive_evidence_plan_candidate_review_package_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST,
        "additional_predictive_evidence_plan_candidate_digest": EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST,
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST,
        "predictive_usefulness_acceptance_readiness_candidate_digest": EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST,
    }.items():
        _expect(candidate.get(field), expected, field)
    _validate_validation_targets(candidate)
    _validate_planning_sections(candidate)
    checklist = candidate.get("validation_checklist")
    if not isinstance(checklist, list):
        raise LiveTickerValidationCandidateError("validation_checklist missing")
    expected_checklist = _checklist(candidate)
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "validation_checklist check IDs")
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise LiveTickerValidationCandidateError(
            f"validation checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "validation_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("validation_summary"), expected_summary, "validation_summary")
    digest = candidate.get("live_ticker_validation_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LiveTickerValidationCandidateError("live_ticker_validation_candidate_digest missing")
    _expect(digest, live_ticker_validation_candidate_digest_v1(candidate), "live_ticker_validation_candidate_digest")
    return {
        "status": "LIVE_TICKER_VALIDATION_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "live_ticker_validation_candidate_digest": digest,
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "approved_expanded_ticker_universe": list(candidate["approved_expanded_ticker_universe"]),
        "approved_expanded_ticker_count": candidate["approved_expanded_ticker_count"],
        "validation_target_count": candidate["validation_target_count"],
        "provider_requests_made": False,
        "provider_request_authorized": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "total_checks": expected_summary["total_checks"],
        "passed_checks": expected_summary["passed_checks"],
        "failed_checks": expected_summary["failed_checks"],
        "blocker_count": expected_summary["blocker_count"],
        "ready_for_operator_review": expected_summary["ready_for_operator_review"],
        "ready_for_live_ticker_validation_approval": False,
    }


def build_live_ticker_validation_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized live ticker validation candidate status document."""
    validation = validate_live_ticker_validation_candidate_v1(candidate)
    summary = candidate["validation_summary"]
    lines = [
        "# MarketFlow Live Ticker Validation Candidate Status",
        "",
        "## Title",
        "- Live Ticker Validation Candidate v1.",
        "",
        "## Purpose",
        "- Define an offline request package for future live ticker validation.",
        "- This candidate does not authorize provider requests or perform live validation.",
        "",
        "## Source Ticker Universe Approval",
        f"- Approval digest: `{candidate['ticker_universe_selection_approval_digest']}`",
        f"- Approval scope: `{candidate['ticker_universe_selection_approval_scope']}`",
        "",
        "## Validation Target Universe",
        f"- Approved ticker count: `{candidate['approved_expanded_ticker_count']}`",
        f"- Validation target count: `{candidate['validation_target_count']}`",
    ]
    lines.extend(f"- `{ticker}`" for ticker in candidate["approved_expanded_ticker_universe"])
    lines.extend(["", "## Planned Validation Checks"])
    lines.extend(
        f"- `{item['check_name']}`: performed_now `{item['performed_now']}`"
        for item in candidate["planned_validation_checks"]
    )
    policy = candidate["provider_request_policy"]
    lines.extend(
        [
            "",
            "## Provider Request Policy",
            f"- future_provider_request_policy_status: `{policy['future_provider_request_policy_status']}`",
            f"- allowed_future_request_type: `{policy['allowed_future_request_type']}`",
            f"- api_key_handling: `{policy['api_key_handling']}`",
            f"- raw_payload_policy: `{policy['raw_payload_policy']}`",
            f"- provider_result_authority: `{policy['provider_result_authority']}`",
            "",
            "## Planned Outputs",
        ]
    )
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in candidate["planned_outputs"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Validation Boundary",
            f"- provider_requests_made: `{candidate['provider_requests_made']}`",
            f"- provider_request_authorized: `{candidate['provider_request_authorized']}`",
            f"- live_provider_transport_enabled: `{candidate['live_provider_transport_enabled']}`",
            f"- live_ticker_validation_authorized: `{candidate['live_ticker_validation_authorized']}`",
            f"- live_ticker_validation_performed: `{candidate['live_ticker_validation_performed']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_authority_created: `{candidate['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{candidate['new_ticker_acquisition_authorized']}`",
            f"- dataset_generation_authorized: `{candidate['dataset_generation_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{candidate['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
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
            f"- ready_for_live_ticker_validation_approval: `{summary['ready_for_live_ticker_validation_approval']}`",
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation or current listing verification occurred.",
            "- No live provider transport was enabled.",
            "- No new ticker authority, acquisition authority, or dataset-generation authority was created.",
            "- No predictive experiment, walk-forward, label, feature-matrix, or strategy-scoring rerun occurred.",
            "- Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    _expect(validation["ready_for_live_ticker_validation_approval"], False, "ready_for_live_ticker_validation_approval")
    return "\n".join(lines)


def write_live_ticker_validation_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the live ticker validation candidate JSON without overwriting output."""
    candidate = build_live_ticker_validation_candidate_v1()
    validation = validate_live_ticker_validation_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "live_ticker_validation_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LiveTickerValidationCandidateError(
            "live ticker validation candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LiveTickerValidationCandidateError(
            "live ticker validation candidate output already exists"
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
