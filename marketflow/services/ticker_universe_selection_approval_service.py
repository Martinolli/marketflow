"""Offline approval ceremony for ticker universe selection."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    ticker_universe_selection_candidate_operator_review_service as candidate_review,
)


ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED = "TICKER_UNIVERSE_SELECTION_APPROVED"
SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_APPROVAL_V1 = (
    "ticker_universe_selection_approval_v1"
)
TICKER_UNIVERSE_SELECTION_APPROVED = "TICKER_UNIVERSE_SELECTION_APPROVED"
OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION = (
    "APPROVE_TICKER_UNIVERSE_SELECTION"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "ticker_universe_selection_approval_operator_attestation_v1"
)
TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY = (
    "TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY"
)
FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY = (
    "FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY"
)
REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE TICKER UNIVERSE SELECTION MSFT NVDA AMZN GOOGL META TSLA JPM XOM "
    "JNJ WMT CAT LMT FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY"
)

APPROVED_EXPANDED_TICKER_UNIVERSE = list(candidate_review.DEFAULT_PROPOSED_TICKER_UNIVERSE)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST = (
    candidate_review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "df63f64a3b145740a650ecf7db703356f3ee24e0dbdfdc4ac27a1812b75dcf4a"
)
EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST = (
    candidate_review.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST = (
    candidate_review.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
)
EXPECTED_REVIEW_CHECKLIST_TOTAL = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_PASSED = len(candidate_review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

EXISTING_BASELINE_TICKER = candidate_review.EXISTING_BASELINE_TICKER
NOT_PERFORMED = candidate_review.NOT_PERFORMED
NOT_VERIFIED = candidate_review.NOT_VERIFIED
NOT_CREATED = candidate_review.NOT_CREATED
NOT_AUTHORIZED = candidate_review.NOT_AUTHORIZED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_review.RESEARCH_ONLY_NON_ACTIONABLE
PLANNED_NOT_GENERATED = candidate_review.PLANNED_NOT_GENERATED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_future_validation_and_authority_chain_planning_only",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_ticker_validation_authorized",
    "operator_confirms_no_live_ticker_validation_performed",
    "operator_confirms_no_new_ticker_authority_created",
    "operator_confirms_no_new_ticker_acquisition_authorized",
    "operator_confirms_no_dataset_generation_authorized",
    "operator_confirms_no_additional_predictive_evidence_execution_authorized",
    "operator_confirms_no_additional_predictive_evidence_executed",
    "operator_confirms_no_predictive_experiment_rerun",
    "operator_confirms_no_walk_forward_rerun",
    "operator_confirms_no_label_regeneration",
    "operator_confirms_no_feature_matrix_regeneration",
    "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_strategy_runtime_migration",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_automatic_stitching",
]

REMAINING_REQUIRED_TASKS = [
    "Live ticker validation candidate and approval.",
    "Per-ticker identity, exchange calendar, split, and dividend authority chain.",
    "Per-ticker acquisition generation authority chain.",
    "Per-ticker canonical dataset and registry authority chain.",
    "Dataset file availability verification for approved tickers.",
    "Separate research campaign and predictive evidence authority chain.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "source_candidate_review_digest_matches_expected",
    "source_candidate_review_has_zero_blockers",
    "source_candidate_digest_matches_expected",
    "source_scope_expansion_review_digest_matches_expected",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_candidate_digest_confirmation_matches",
    "operator_candidate_review_digest_confirmation_matches",
    "operator_scope_expansion_review_digest_confirmation_matches",
    "operator_approved_ticker_universe_confirmation_matches",
    "operator_approved_ticker_count_confirmation_matches",
    *OPERATOR_CONFIRMATION_FIELDS,
    "approval_scope_exact",
    "ticker_universe_selection_approved_true",
    "expanded_ticker_universe_approved_true",
    "approved_expanded_ticker_universe_matches",
    "approved_expanded_ticker_count_12",
    "live_ticker_validation_authorized_false",
    "live_ticker_validation_performed_false",
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
    "provider_requests_made_in_approval_false",
    "approved_entries_live_validation_not_performed",
    "approved_entries_listing_not_verified",
    "approved_entries_authority_not_created",
    "approved_entries_runtime_not_authorized",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
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
    "no_new_ticker_authority_artifact_created",
    "no_acquisition_authorization_artifact_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_artifact_created",
    "no_runtime_migration_approval_artifact_created",
]


class TickerUniverseSelectionApprovalError(ValueError):
    """Raised when ticker universe selection approval violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, severity: str = BLOCKER) -> dict[str, Any]:
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
        raise TickerUniverseSelectionApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise TickerUniverseSelectionApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise TickerUniverseSelectionApprovalError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def build_ticker_universe_selection_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_candidate_digest: str,
    operator_confirms_candidate_review_package_digest: str,
    operator_confirms_scope_expansion_review_digest: str,
    operator_confirms_approved_ticker_universe: list[str],
    operator_confirms_approved_ticker_count: int,
    operator_confirms_future_validation_and_authority_chain_planning_only: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_live_ticker_validation_authorized: bool,
    operator_confirms_no_live_ticker_validation_performed: bool,
    operator_confirms_no_new_ticker_authority_created: bool,
    operator_confirms_no_new_ticker_acquisition_authorized: bool,
    operator_confirms_no_dataset_generation_authorized: bool,
    operator_confirms_no_additional_predictive_evidence_execution_authorized: bool,
    operator_confirms_no_additional_predictive_evidence_executed: bool,
    operator_confirms_no_predictive_experiment_rerun: bool,
    operator_confirms_no_walk_forward_rerun: bool,
    operator_confirms_no_label_regeneration: bool,
    operator_confirms_no_feature_matrix_regeneration: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_strategy_runtime_migration: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_automatic_stitching: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for ticker universe selection approval."""
    confirmation_values = {
        "operator_confirms_future_validation_and_authority_chain_planning_only": (
            operator_confirms_future_validation_and_authority_chain_planning_only
        ),
        "operator_confirms_no_provider_requests_in_approval": (
            operator_confirms_no_provider_requests_in_approval
        ),
        "operator_confirms_no_live_ticker_validation_authorized": (
            operator_confirms_no_live_ticker_validation_authorized
        ),
        "operator_confirms_no_live_ticker_validation_performed": (
            operator_confirms_no_live_ticker_validation_performed
        ),
        "operator_confirms_no_new_ticker_authority_created": (
            operator_confirms_no_new_ticker_authority_created
        ),
        "operator_confirms_no_new_ticker_acquisition_authorized": (
            operator_confirms_no_new_ticker_acquisition_authorized
        ),
        "operator_confirms_no_dataset_generation_authorized": (
            operator_confirms_no_dataset_generation_authorized
        ),
        "operator_confirms_no_additional_predictive_evidence_execution_authorized": (
            operator_confirms_no_additional_predictive_evidence_execution_authorized
        ),
        "operator_confirms_no_additional_predictive_evidence_executed": (
            operator_confirms_no_additional_predictive_evidence_executed
        ),
        "operator_confirms_no_predictive_experiment_rerun": (
            operator_confirms_no_predictive_experiment_rerun
        ),
        "operator_confirms_no_walk_forward_rerun": operator_confirms_no_walk_forward_rerun,
        "operator_confirms_no_label_regeneration": operator_confirms_no_label_regeneration,
        "operator_confirms_no_feature_matrix_regeneration": (
            operator_confirms_no_feature_matrix_regeneration
        ),
        "operator_confirms_no_strategy_scoring": operator_confirms_no_strategy_scoring,
        "operator_confirms_no_trade_recommendations": (
            operator_confirms_no_trade_recommendations
        ),
        "operator_confirms_no_predictive_usefulness_acceptance": (
            operator_confirms_no_predictive_usefulness_acceptance
        ),
        "operator_confirms_no_profitability_acceptance": (
            operator_confirms_no_profitability_acceptance
        ),
        "operator_confirms_no_runtime_migration_approval": (
            operator_confirms_no_runtime_migration_approval
        ),
        "operator_confirms_no_runtime_activation": operator_confirms_no_runtime_activation,
        "operator_confirms_no_strategy_runtime_migration": (
            operator_confirms_no_strategy_runtime_migration
        ),
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
        "operator_confirms_no_automatic_stitching": operator_confirms_no_automatic_stitching,
    }
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_candidate_digest": operator_confirms_candidate_digest,
        "operator_confirms_candidate_review_package_digest": (
            operator_confirms_candidate_review_package_digest
        ),
        "operator_confirms_scope_expansion_review_digest": (
            operator_confirms_scope_expansion_review_digest
        ),
        "operator_confirms_approved_ticker_universe": list(
            operator_confirms_approved_ticker_universe
        ),
        "operator_confirms_approved_ticker_count": operator_confirms_approved_ticker_count,
        **confirmation_values,
    }


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else candidate_review.build_ticker_universe_selection_candidate_review_package_v1()
    )
    try:
        validation = candidate_review.validate_ticker_universe_selection_candidate_review_package_v1(
            source_review
        )
    except candidate_review.TickerUniverseSelectionCandidateReviewPackageError as exc:
        raise TickerUniverseSelectionApprovalError(
            f"source ticker universe selection review package invalid: {exc}"
        ) from exc
    _expect(
        validation["ticker_universe_selection_candidate_review_package_digest"],
        EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source ticker universe selection review package digest",
    )
    _expect(
        source_review["review_summary"]["failed_checks"],
        0,
        "source ticker universe selection review failed check count",
    )
    _expect(
        source_review["review_summary"]["blocker_count"],
        0,
        "source ticker universe selection review blocker count",
    )
    return source_review


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_candidate_kind": source_review["reviewed_ticker_universe_selection_candidate_kind"],
        "source_candidate_status": source_review[
            "reviewed_ticker_universe_selection_candidate_status"
        ],
        "source_candidate_digest": source_review[
            "reviewed_ticker_universe_selection_candidate_digest"
        ],
        "source_candidate_review_package_kind": source_review["artifact_kind"],
        "source_candidate_review_status": source_review["review_status"],
        "source_candidate_review_package_digest": source_review[
            "ticker_universe_selection_candidate_review_package_digest"
        ],
        "source_candidate_review_checklist_total": source_review["review_summary"][
            "total_checks"
        ],
        "source_candidate_review_checklist_passed": source_review["review_summary"][
            "passed_checks"
        ],
        "source_candidate_review_checklist_failed": source_review["review_summary"][
            "failed_checks"
        ],
        "source_candidate_review_blocker_count": source_review["review_summary"][
            "blocker_count"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": source_review[
            "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_digest": source_review[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": source_review[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": source_review[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            source_review["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"]
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": source_review[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": source_review[
            "predictive_experiment_results_review_package_digest"
        ],
        "predictive_experiment_execution_digest": source_review[
            "predictive_experiment_execution_digest"
        ],
        "predictive_experiment_execution_approval_digest": source_review[
            "predictive_experiment_execution_approval_digest"
        ],
        "existing_baseline_ticker": source_review["existing_baseline_ticker"],
        "reviewed_candidate_ticker_list_status": source_review["candidate_ticker_list_status"],
        "source_future_validation_gates": list(source_review["future_validation_gates"]),
        "source_future_validation_gate_count": source_review["future_validation_gate_count"],
        "source_future_ticker_authority_chain": deepcopy(
            source_review["future_ticker_authority_chain"]
        ),
        "source_future_ticker_authority_chain_step_count": source_review[
            "future_ticker_authority_chain_step_count"
        ],
        "source_planned_outputs": deepcopy(source_review["planned_outputs"]),
        "source_planned_output_count": source_review["planned_output_count"],
    }


def _approved_ticker_entries(tickers: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "ticker": ticker,
            "selection_approved": True,
            "approval_entry_scope": FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
            "live_validation_status": NOT_PERFORMED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "sector_status": NOT_VERIFIED,
            "liquidity_status": NOT_VERIFIED,
            "market_cap_status": NOT_VERIFIED,
            "identity_authority_status": NOT_CREATED,
            "corporate_action_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
        }
        for ticker in tickers
    ]


def _all_entries(approved_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries = approved_artifact.get("approved_ticker_entries")
    return entries if isinstance(entries, list) else []


def _entries_have(field: str, expected: Any, approved_artifact: dict[str, Any]) -> bool:
    entries = _all_entries(approved_artifact)
    return bool(entries) and all(entry.get(field) == expected for entry in entries)


def _entry_authorities_not_created(approved_artifact: dict[str, Any]) -> bool:
    fields = (
        "identity_authority_status",
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    entries = _all_entries(approved_artifact)
    return bool(entries) and all(
        entry.get(field) == NOT_CREATED for entry in entries for field in fields
    )


def _entry_uses_not_authorized(approved_artifact: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "broker_execution", "paper_trading")
    entries = _all_entries(approved_artifact)
    return bool(entries) and all(
        entry.get(field) == NOT_AUTHORIZED for entry in entries for field in fields
    )


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION, None),
            _check("operator_attestation_phrase_matches", REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_candidate_digest_confirmation_matches", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, None),
            _check("operator_candidate_review_digest_confirmation_matches", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_scope_expansion_review_digest_confirmation_matches", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_approved_ticker_universe_confirmation_matches", APPROVED_EXPANDED_TICKER_UNIVERSE, None),
            _check("operator_approved_ticker_count_confirmation_matches", len(APPROVED_EXPANDED_TICKER_UNIVERSE), None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_TICKER_UNIVERSE_SELECTION_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_candidate_digest_confirmation_matches", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, attestation.get("operator_confirms_candidate_digest")),
        _check("operator_candidate_review_digest_confirmation_matches", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_candidate_review_package_digest")),
        _check("operator_scope_expansion_review_digest_confirmation_matches", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_scope_expansion_review_digest")),
        _check("operator_approved_ticker_universe_confirmation_matches", APPROVED_EXPANDED_TICKER_UNIVERSE, attestation.get("operator_confirms_approved_ticker_universe")),
        _check("operator_approved_ticker_count_confirmation_matches", len(APPROVED_EXPANDED_TICKER_UNIVERSE), attestation.get("operator_confirms_approved_ticker_count")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise TickerUniverseSelectionApprovalError("operator_attestation must be a JSON object")
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_phrase",
        "operator_attestation_version",
    ):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise TickerUniverseSelectionApprovalError(f"{field} must be a non-empty string")
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise TickerUniverseSelectionApprovalError(
            f"operator attestation check failed: {failed[0]['check_id']}"
        )
    return deepcopy(attestation)


def _approval_checklist(approved_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = approved_artifact.get("operator_attestation")
    return [
        _check("source_candidate_review_digest_matches_expected", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved_artifact.get("source_candidate_review_package_digest")),
        _check("source_candidate_review_has_zero_blockers", 0, approved_artifact.get("source_candidate_review_blocker_count")),
        _check("source_candidate_digest_matches_expected", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, approved_artifact.get("source_candidate_digest")),
        _check("source_scope_expansion_review_digest_matches_expected", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, approved_artifact.get("predictive_evidence_scope_expansion_plan_candidate_review_package_digest")),
        *_attestation_checks(attestation if isinstance(attestation, dict) else None),
        _check("approval_scope_exact", TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY, approved_artifact.get("approval_scope")),
        _check("ticker_universe_selection_approved_true", True, approved_artifact.get("ticker_universe_selection_approved")),
        _check("expanded_ticker_universe_approved_true", True, approved_artifact.get("expanded_ticker_universe_approved")),
        _check("approved_expanded_ticker_universe_matches", APPROVED_EXPANDED_TICKER_UNIVERSE, approved_artifact.get("approved_expanded_ticker_universe")),
        _check("approved_expanded_ticker_count_12", len(APPROVED_EXPANDED_TICKER_UNIVERSE), approved_artifact.get("approved_expanded_ticker_count")),
        _check("live_ticker_validation_authorized_false", False, approved_artifact.get("live_ticker_validation_authorized")),
        _check("live_ticker_validation_performed_false", False, approved_artifact.get("live_ticker_validation_performed")),
        _check("new_ticker_authority_created_false", False, approved_artifact.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, approved_artifact.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, approved_artifact.get("dataset_generation_authorized")),
        _check("additional_predictive_evidence_execution_authorized_false", False, approved_artifact.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, approved_artifact.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, approved_artifact.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, approved_artifact.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, approved_artifact.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, approved_artifact.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, approved_artifact.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, approved_artifact.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, approved_artifact.get("trade_recommendations_generated")),
        _check("provider_requests_made_in_approval_false", False, approved_artifact.get("provider_requests_made_in_approval")),
        _check("approved_entries_live_validation_not_performed", True, _entries_have("live_validation_status", NOT_PERFORMED, approved_artifact)),
        _check("approved_entries_listing_not_verified", True, _entries_have("listing_status", NOT_VERIFIED, approved_artifact)),
        _check("approved_entries_authority_not_created", True, _entry_authorities_not_created(approved_artifact)),
        _check("approved_entries_runtime_not_authorized", True, _entry_uses_not_authorized(approved_artifact)),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved_artifact.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, approved_artifact.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved_artifact.get("profitability")),
        _check("profitability_acceptance_ready_false", False, approved_artifact.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, approved_artifact.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, approved_artifact.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved_artifact.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved_artifact.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, approved_artifact.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, approved_artifact.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, approved_artifact.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, approved_artifact.get("broker_execution")),
        _check("automatic_stitching_false", False, approved_artifact.get("automatic_stitching")),
        _check("no_live_ticker_validation_artifact_created", False, approved_artifact.get("live_ticker_validation_artifact_created")),
        _check("no_new_ticker_authority_artifact_created", False, approved_artifact.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_artifact_created", False, approved_artifact.get("acquisition_authorization_artifact_created")),
        _check("no_dataset_generation_authorization_created", False, approved_artifact.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, approved_artifact.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_artifact_created", False, approved_artifact.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_artifact_created", False, approved_artifact.get("runtime_migration_approval_artifact_created")),
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
        "ticker_universe_selection_approved_by_operator": failed == 0,
        "approval_scope": FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
        "ready_for_live_ticker_validation_candidate": failed == 0,
        "live_ticker_validation_authorized": False,
        "new_ticker_authority_authorized": False,
        "acquisition_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("ticker_universe_selection_approval_digest", None)
    return payload


def ticker_universe_selection_approval_digest_v1(approved_artifact: dict[str, Any]) -> str:
    """Return the deterministic digest for the ticker universe selection approval."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_ticker_universe_selection_approved_v1(
    *,
    operator_attestation: dict[str, Any],
    ticker_universe_selection_candidate_review_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline approval artifact for future validation planning only."""
    source_review = _source_review_package(ticker_universe_selection_candidate_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    approved_tickers = list(APPROVED_EXPANDED_TICKER_UNIVERSE)
    approved_artifact = {
        "artifact_kind": ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED,
        "schema_version": SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_APPROVAL_V1,
        "approval_status": TICKER_UNIVERSE_SELECTION_APPROVED,
        "created_offline": True,
        "research_only": True,
        "operator_decision": OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION,
        "operator_attestation": attestation,
        "approval_scope": (
            TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY
        ),
        "approval_entry_scope": FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
        "approved_expanded_ticker_universe": approved_tickers,
        "approved_expanded_ticker_count": len(approved_tickers),
        "approved_ticker_entries": _approved_ticker_entries(approved_tickers),
        "live_ticker_validation_authorized": False,
        "live_ticker_validation_performed": False,
        "final_ticker_selection_performed": False,
        "scope_expansion_authorized": False,
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
        "provider_requests_made": False,
        "provider_requests_made_in_approval": False,
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
        "ticker_universe_selection_approval_created": True,
        "expanded_ticker_universe_approval_created": True,
        "live_ticker_validation_artifact_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
        **_review_evidence(source_review),
    }
    approved_artifact["approval_checklist"] = _approval_checklist(approved_artifact)
    approved_artifact["approval_summary"] = _summary(approved_artifact["approval_checklist"])
    approved_artifact["ticker_universe_selection_approval_digest"] = (
        ticker_universe_selection_approval_digest_v1(approved_artifact)
    )
    validate_ticker_universe_selection_approved_v1(approved_artifact)
    return approved_artifact


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "approved_artifact") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "LIVE_TICKER_VALIDATION_AUTHORIZED",
            "LIVE_TICKER_VALIDATION_PERFORMED",
            "NEW_TICKER_AUTHORITY_CREATED",
            "NEW_TICKER_ACQUISITION_AUTHORIZED",
            "DATASET_GENERATION_AUTHORIZED",
            "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise TickerUniverseSelectionApprovalError(f"{current_path} must not emit {value}")
        if key in {
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
            "provider_requests_made",
            "provider_requests_made_in_approval",
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
            "new_ticker_authority_artifact_created",
            "acquisition_authorization_artifact_created",
            "dataset_generation_authorization_created",
            "predictive_usefulness_acceptance_artifact_created",
            "profitability_acceptance_artifact_created",
            "runtime_migration_approval_artifact_created",
            "generated",
            "execution_performed",
            "output_generated",
        } and value is True:
            raise TickerUniverseSelectionApprovalError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise TickerUniverseSelectionApprovalError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise TickerUniverseSelectionApprovalError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_approved_ticker_entries(approved_artifact: dict[str, Any]) -> None:
    tickers = approved_artifact.get("approved_expanded_ticker_universe")
    entries = approved_artifact.get("approved_ticker_entries")
    if tickers != APPROVED_EXPANDED_TICKER_UNIVERSE:
        raise TickerUniverseSelectionApprovalError("approved ticker universe mismatch")
    if EXISTING_BASELINE_TICKER in tickers:
        raise TickerUniverseSelectionApprovalError("approved ticker universe must not contain AAPL")
    if len(tickers) != len(set(tickers)):
        raise TickerUniverseSelectionApprovalError("approved ticker universe contains duplicates")
    if not isinstance(entries, list) or len(entries) != len(tickers):
        raise TickerUniverseSelectionApprovalError("approved_ticker_entries mismatch")
    for entry in entries:
        ticker = entry.get("ticker")
        if ticker not in tickers:
            raise TickerUniverseSelectionApprovalError("approved ticker entry mismatch")
        _expect_true(entry.get("selection_approved"), f"approved_ticker_entries.{ticker}.selection_approved")
        for field, expected in {
            "approval_entry_scope": FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
            "live_validation_status": NOT_PERFORMED,
            "listing_status": NOT_VERIFIED,
            "security_type_status": NOT_VERIFIED,
            "exchange_status": NOT_VERIFIED,
            "sector_status": NOT_VERIFIED,
            "liquidity_status": NOT_VERIFIED,
            "market_cap_status": NOT_VERIFIED,
            "identity_authority_status": NOT_CREATED,
            "corporate_action_authority_status": NOT_CREATED,
            "acquisition_authority_status": NOT_CREATED,
            "canonical_dataset_authority_status": NOT_CREATED,
            "registry_approval_status": NOT_CREATED,
            "research_use_status": NOT_AUTHORIZED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
        }.items():
            _expect(entry.get(field), expected, f"approved_ticker_entries.{ticker}.{field}")


def validate_ticker_universe_selection_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate ticker universe approval while preserving downstream guardrails."""
    if not isinstance(approved_artifact, dict):
        raise TickerUniverseSelectionApprovalError("approved artifact must be a JSON object")
    _reject_forbidden_values(approved_artifact)
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        TICKER_UNIVERSE_SELECTION_APPROVED,
        "approval_status",
    )
    for field in (
        "created_offline",
        "research_only",
        "ticker_universe_selection_approved",
        "expanded_ticker_universe_approved",
        "ticker_universe_selection_approval_created",
        "expanded_ticker_universe_approval_created",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "scope_expansion_authorized",
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
        "provider_requests_made",
        "provider_requests_made_in_approval",
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
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(approved_artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "operator_decision": OPERATOR_DECISION_APPROVE_TICKER_UNIVERSE_SELECTION,
        "approval_scope": TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
        "approval_entry_scope": FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY,
        "approved_expanded_ticker_universe": APPROVED_EXPANDED_TICKER_UNIVERSE,
        "approved_expanded_ticker_count": len(APPROVED_EXPANDED_TICKER_UNIVERSE),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "source_candidate_kind": candidate_review.candidate_service.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE,
        "source_candidate_status": candidate_review.candidate_service.TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW,
        "source_candidate_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST,
        "source_candidate_review_package_kind": candidate_review.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE,
        "source_candidate_review_status": candidate_review.TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_candidate_review_package_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_candidate_review_checklist_total": EXPECTED_REVIEW_CHECKLIST_TOTAL,
        "source_candidate_review_checklist_passed": EXPECTED_REVIEW_CHECKLIST_PASSED,
        "source_candidate_review_checklist_failed": EXPECTED_REVIEW_CHECKLIST_FAILED,
        "source_candidate_review_blocker_count": EXPECTED_REVIEW_BLOCKER_COUNT,
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST,
        "predictive_evidence_scope_expansion_plan_candidate_digest": EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST,
        "existing_baseline_ticker": EXISTING_BASELINE_TICKER,
        "reviewed_candidate_ticker_list_status": candidate_review.CANDIDATE_TICKER_LIST_STATUS,
        "source_future_validation_gates": candidate_review.FUTURE_VALIDATION_GATES,
        "source_future_validation_gate_count": 13,
        "source_future_ticker_authority_chain_step_count": 15,
        "source_planned_output_count": 7,
        "remaining_required_tasks": REMAINING_REQUIRED_TASKS,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    _validate_approved_ticker_entries(approved_artifact)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise TickerUniverseSelectionApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("ticker_universe_selection_approved_by_operator"),
        "ticker_universe_selection_approved_by_operator",
    )
    for field in (
        "live_ticker_validation_authorized",
        "new_ticker_authority_authorized",
        "acquisition_authorized",
        "additional_predictive_evidence_execution_authorized",
        "predictive_usefulness_accepted",
        "profitability_accepted",
        "runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(summary.get(field), field)
    digest = approved_artifact.get("ticker_universe_selection_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise TickerUniverseSelectionApprovalError(
            "ticker_universe_selection_approval_digest missing"
        )
    _expect(
        digest,
        ticker_universe_selection_approval_digest_v1(approved_artifact),
        "ticker_universe_selection_approval_digest",
    )
    return {
        "status": "TICKER_UNIVERSE_SELECTION_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "ticker_universe_selection_approval_digest": digest,
        "approval_scope": approved_artifact["approval_scope"],
        "approved_expanded_ticker_universe": approved_artifact[
            "approved_expanded_ticker_universe"
        ],
        "approved_expanded_ticker_count": approved_artifact[
            "approved_expanded_ticker_count"
        ],
        "source_candidate_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST,
        "source_candidate_review_package_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "scope_expansion_review_package_digest": EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
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
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_ticker_universe_selection_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized ticker universe selection approval status document."""
    validation = validate_ticker_universe_selection_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Ticker Universe Selection Approval Status",
        "",
        "## Title",
        "- Ticker Universe Selection Approval Ceremony v1.",
        "",
        "## Approved Ticker Universe",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['ticker_universe_selection_approval_digest']}`",
        f"- Approved expanded ticker count: `{approved_artifact['approved_expanded_ticker_count']}`",
        f"- Approved expanded ticker universe: `{', '.join(approved_artifact['approved_expanded_ticker_universe'])}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Review Package",
        f"- Review package kind: `{approved_artifact['source_candidate_review_package_kind']}`",
        f"- Review status: `{approved_artifact['source_candidate_review_status']}`",
        f"- Review package digest: `{approved_artifact['source_candidate_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['source_candidate_digest']}`",
        f"- Review blockers: `{approved_artifact['source_candidate_review_blocker_count']}`",
        "",
        "## Source Scope Expansion Evidence",
        f"- Scope expansion review package digest: `{approved_artifact['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        f"- Scope expansion candidate digest: `{approved_artifact['predictive_evidence_scope_expansion_plan_candidate_digest']}`",
        "",
        "## Authority Boundary",
        f"- ticker_universe_selection_approved: `{approved_artifact['ticker_universe_selection_approved']}`",
        f"- expanded_ticker_universe_approved: `{approved_artifact['expanded_ticker_universe_approved']}`",
        f"- live_ticker_validation_authorized: `{approved_artifact['live_ticker_validation_authorized']}`",
        f"- live_ticker_validation_performed: `{approved_artifact['live_ticker_validation_performed']}`",
        f"- new_ticker_authority_created: `{approved_artifact['new_ticker_authority_created']}`",
        f"- new_ticker_acquisition_authorized: `{approved_artifact['new_ticker_acquisition_authorized']}`",
        f"- dataset_generation_authorized: `{approved_artifact['dataset_generation_authorized']}`",
        f"- additional_predictive_evidence_execution_authorized: `{approved_artifact['additional_predictive_evidence_execution_authorized']}`",
        f"- additional_predictive_evidence_executed: `{approved_artifact['additional_predictive_evidence_executed']}`",
        f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- profitability: `{approved_artifact['profitability']}`",
        f"- runtime_use: `{approved_artifact['runtime_use']}`",
        f"- strategy_use: `{approved_artifact['strategy_use']}`",
        f"- paper_trading: `{approved_artifact['paper_trading']}`",
        f"- broker_execution: `{approved_artifact['broker_execution']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- ready_for_live_ticker_validation_candidate: `{summary['ready_for_live_ticker_validation_candidate']}`",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(
        f"{index}. {task}"
        for index, task in enumerate(approved_artifact["remaining_required_tasks"], start=1)
    )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- The approved ticker universe is approved only for future validation and authority-chain planning.",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation or current listing verification occurred.",
            "- No new ticker authority, acquisition authority, or dataset-generation authority was created.",
            "- No additional predictive evidence execution was authorized or performed.",
            "- No predictive experiment, walk-forward, label, feature-matrix, or strategy-scoring rerun occurred.",
            "- Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_ticker_universe_selection_approved_v1(
    output_dir: str | Path,
    *,
    operator_attestation: dict[str, Any],
    ticker_universe_selection_candidate_review_package: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the ticker universe selection approval JSON without overwriting output."""
    approved = build_ticker_universe_selection_approved_v1(
        operator_attestation=operator_attestation,
        ticker_universe_selection_candidate_review_package=(
            ticker_universe_selection_candidate_review_package
        ),
    )
    validation = validate_ticker_universe_selection_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "ticker_universe_selection_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise TickerUniverseSelectionApprovalError(
            "ticker universe selection approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise TickerUniverseSelectionApprovalError(
            "ticker universe selection approval output already exists"
        )
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
