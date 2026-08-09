"""Offline operator review package for the ticker universe selection candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import ticker_universe_selection_candidate_service as candidate_service


ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE = (
    "TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_V1 = (
    "ticker_universe_selection_candidate_review_v1"
)
TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY"
)
TICKER_UNIVERSE_SELECTION_CANDIDATE_STATUS_BINDING = (
    "TICKER_UNIVERSE_SELECTION_CANDIDATE_STATUS_BINDING"
)
TICKER_UNIVERSE_SELECTION_CANDIDATE_OBJECT_BINDING = (
    "TICKER_UNIVERSE_SELECTION_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST = (
    "6baeb13550814f8c0d3d0a815a797e2f7b46552fa2fa5aa3aa950a7f6d5fce01"
)
EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_TOTAL = 64
EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_PASSED = 64
EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_BLOCKER_COUNT = 0

EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST = (
    candidate_service.EXPECTED_ACCEPTANCE_READINESS_CANDIDATE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
)
EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST = (
    candidate_service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
)

EXISTING_BASELINE_TICKER = candidate_service.EXISTING_BASELINE_TICKER
DEFAULT_PROPOSED_TICKER_UNIVERSE = list(candidate_service.DEFAULT_PROPOSED_TICKER_UNIVERSE)
CANDIDATE_TICKER_LIST_STATUS = candidate_service.CANDIDATE_TICKER_LIST_STATUS
INTENDED_DIVERSITY_TAGS_STATUS = candidate_service.INTENDED_DIVERSITY_TAGS_STATUS
PROPOSED_UNVALIDATED = candidate_service.PROPOSED_UNVALIDATED
NOT_PERFORMED = candidate_service.NOT_PERFORMED
NOT_VERIFIED = candidate_service.NOT_VERIFIED
NOT_CREATED = candidate_service.NOT_CREATED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PLANNED_NOT_GENERATED = candidate_service.PLANNED_NOT_GENERATED
RESEARCH_ONLY_NON_ACTIONABLE = candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
FUTURE_VALIDATION_GATES = list(candidate_service.FUTURE_VALIDATION_GATES)
FUTURE_AUTHORITY_CHAIN_STEPS = list(candidate_service.FUTURE_AUTHORITY_CHAIN_STEPS)
PLANNED_OUTPUT_IDS = list(candidate_service.PLANNED_OUTPUT_IDS)
SELECTION_RATIONALE = list(candidate_service.SELECTION_RATIONALE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "ticker_selection_candidate_kind_matches",
    "ticker_selection_candidate_status_ready_for_review",
    "ticker_selection_candidate_digest_matches",
    "ticker_selection_candidate_checklist_zero_blockers",
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
    "provider_requests_made_in_review_false",
    "candidate_entries_status_unvalidated",
    "candidate_entries_listing_not_verified",
    "candidate_entries_security_type_not_verified",
    "candidate_entries_exchange_not_verified",
    "candidate_entries_authority_not_created",
    "candidate_entries_runtime_not_authorized",
    "intended_diversity_tags_unverified",
    "selection_rationale_research_only",
    "future_validation_gates_13",
    "future_authority_chain_15_steps",
    "planned_outputs_7",
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


class TickerUniverseSelectionCandidateReviewPackageError(ValueError):
    """Raised when the ticker universe selection candidate review package is invalid."""


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
        raise TickerUniverseSelectionCandidateReviewPackageError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise TickerUniverseSelectionCandidateReviewPackageError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise TickerUniverseSelectionCandidateReviewPackageError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_ticker_entries() -> list[dict[str, Any]]:
    return candidate_service._candidate_ticker_entries(DEFAULT_PROPOSED_TICKER_UNIVERSE)


def _future_authority_chain() -> list[dict[str, Any]]:
    return candidate_service._future_authority_chain()


def _planned_outputs() -> list[dict[str, Any]]:
    return candidate_service._planned_outputs()


def _recorded_ticker_universe_selection_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": candidate_service.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE,
        "candidate_status": candidate_service.TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW,
        "ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "selection_summary": {
            "total_checks": EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_TOTAL,
            "passed_checks": EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_PASSED,
            "failed_checks": EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_FAILED,
            "blocker_count": EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_BLOCKER_COUNT,
            "ready_for_operator_review": True,
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
        },
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
        "proposed_candidate_ticker_universe": list(DEFAULT_PROPOSED_TICKER_UNIVERSE),
        "proposed_candidate_ticker_count": len(DEFAULT_PROPOSED_TICKER_UNIVERSE),
        "candidate_ticker_list_status": CANDIDATE_TICKER_LIST_STATUS,
        "approved_expanded_ticker_universe": [],
        "approved_expanded_ticker_count": 0,
        "candidate_ticker_entries": _candidate_ticker_entries(),
        "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
        "selection_rationale": list(SELECTION_RATIONALE),
        "selection_rationale_status": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_validation_gates": list(FUTURE_VALIDATION_GATES),
        "future_validation_gate_count": len(FUTURE_VALIDATION_GATES),
        "future_ticker_authority_chain": _future_authority_chain(),
        "future_ticker_authority_chain_step_count": len(FUTURE_AUTHORITY_CHAIN_STEPS),
        "planned_outputs": _planned_outputs(),
        "planned_output_count": len(PLANNED_OUTPUT_IDS),
    }


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            _recorded_ticker_universe_selection_candidate(),
            TICKER_UNIVERSE_SELECTION_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_ticker_universe_selection_candidate_v1(candidate)
    return deepcopy(candidate), TICKER_UNIVERSE_SELECTION_CANDIDATE_OBJECT_BINDING


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["selection_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_V1,
        "review_status": TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "ticker_universe_selection_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
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
        "ready_for_ticker_universe_selection_approval": False,
        "ready_for_live_ticker_validation": False,
        "ready_for_new_ticker_authority_chain": False,
        "ready_for_acquisition": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "ready_for_predictive_usefulness_acceptance_candidate": False,
        "ticker_universe_selection_approval_created": False,
        "expanded_ticker_universe_approval_created": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_artifact_created": False,
        "runtime_migration_approval_artifact_created": False,
        "reviewed_ticker_universe_selection_candidate_kind": candidate["artifact_kind"],
        "reviewed_ticker_universe_selection_candidate_status": candidate["candidate_status"],
        "reviewed_ticker_universe_selection_candidate_digest": candidate[
            "ticker_universe_selection_candidate_digest"
        ],
        "reviewed_ticker_universe_selection_candidate_checklist_total": summary["total_checks"],
        "reviewed_ticker_universe_selection_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_ticker_universe_selection_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_ticker_universe_selection_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": candidate[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest": (
            candidate["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"]
        ),
        "predictive_usefulness_acceptance_readiness_candidate_digest": candidate[
            "predictive_usefulness_acceptance_readiness_candidate_digest"
        ],
        "predictive_experiment_results_review_package_digest": candidate[
            "predictive_experiment_results_review_package_digest"
        ],
        "predictive_experiment_execution_digest": candidate[
            "predictive_experiment_execution_digest"
        ],
        "predictive_experiment_execution_approval_digest": candidate[
            "predictive_experiment_execution_approval_digest"
        ],
        "existing_baseline_ticker": candidate["existing_baseline_ticker"],
        "proposed_candidate_ticker_universe": list(
            candidate["proposed_candidate_ticker_universe"]
        ),
        "proposed_candidate_ticker_count": candidate["proposed_candidate_ticker_count"],
        "candidate_ticker_list_status": candidate["candidate_ticker_list_status"],
        "approved_expanded_ticker_universe": list(candidate["approved_expanded_ticker_universe"]),
        "approved_expanded_ticker_count": candidate["approved_expanded_ticker_count"],
        "candidate_ticker_entries": deepcopy(candidate["candidate_ticker_entries"]),
        "intended_diversity_tags_status": candidate["intended_diversity_tags_status"],
        "selection_rationale": list(candidate["selection_rationale"]),
        "selection_rationale_status": candidate["selection_rationale_status"],
        "future_validation_gates": list(candidate["future_validation_gates"]),
        "future_validation_gate_count": candidate["future_validation_gate_count"],
        "future_ticker_authority_chain": deepcopy(candidate["future_ticker_authority_chain"]),
        "future_ticker_authority_chain_step_count": candidate[
            "future_ticker_authority_chain_step_count"
        ],
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": candidate["planned_output_count"],
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }


def _all_entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("candidate_ticker_entries")
    return entries if isinstance(entries, list) else []


def _entries_have(expected_field: str, expected_value: Any, review_package: dict[str, Any]) -> bool:
    entries = _all_entries(review_package)
    return bool(entries) and all(entry.get(expected_field) == expected_value for entry in entries)


def _entry_authorities_not_created(review_package: dict[str, Any]) -> bool:
    fields = (
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    )
    entries = _all_entries(review_package)
    return bool(entries) and all(
        entry.get(field) == NOT_CREATED for entry in entries for field in fields
    )


def _entry_uses_not_authorized(review_package: dict[str, Any]) -> bool:
    fields = ("research_use_status", "runtime_use", "strategy_use", "broker_execution", "paper_trading")
    entries = _all_entries(review_package)
    return bool(entries) and all(
        entry.get(field) == NOT_AUTHORIZED for entry in entries for field in fields
    )


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    tickers = review_package.get("proposed_candidate_ticker_universe", [])
    planned_outputs = review_package.get("planned_outputs", [])
    return [
        _check("ticker_selection_candidate_kind_matches", candidate_service.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE, review_package.get("reviewed_ticker_universe_selection_candidate_kind")),
        _check("ticker_selection_candidate_status_ready_for_review", candidate_service.TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_ticker_universe_selection_candidate_status")),
        _check("ticker_selection_candidate_digest_matches", EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST, review_package.get("reviewed_ticker_universe_selection_candidate_digest")),
        _check("ticker_selection_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_ticker_universe_selection_candidate_blocker_count")),
        _check("scope_expansion_review_digest_bound", EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_evidence_scope_expansion_plan_candidate_review_package_digest")),
        _check("scope_expansion_candidate_digest_bound", EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST, review_package.get("predictive_evidence_scope_expansion_plan_candidate_digest")),
        _check("additional_predictive_evidence_review_digest_bound", EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST, review_package.get("additional_predictive_evidence_plan_candidate_review_package_digest")),
        _check("readiness_review_digest_bound", EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_usefulness_acceptance_readiness_candidate_review_package_digest")),
        _check("predictive_experiment_results_review_digest_bound", EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("predictive_experiment_results_review_package_digest")),
        _check("existing_baseline_ticker_aapl_bound", EXISTING_BASELINE_TICKER, review_package.get("existing_baseline_ticker")),
        _check("proposed_candidate_ticker_count_12", 12, review_package.get("proposed_candidate_ticker_count")),
        _check("proposed_candidate_tickers_unique", True, len(tickers) == len(set(tickers))),
        _check("aapl_not_in_proposed_candidate_universe", True, EXISTING_BASELINE_TICKER not in tickers),
        _check("candidate_ticker_list_unvalidated", CANDIDATE_TICKER_LIST_STATUS, review_package.get("candidate_ticker_list_status")),
        _check("approved_expanded_ticker_universe_empty", [], review_package.get("approved_expanded_ticker_universe")),
        _check("approved_expanded_ticker_count_zero", 0, review_package.get("approved_expanded_ticker_count")),
        _check("live_ticker_validation_performed_false", False, review_package.get("live_ticker_validation_performed")),
        _check("final_ticker_selection_performed_false", False, review_package.get("final_ticker_selection_performed")),
        _check("ticker_universe_selection_approved_false", False, review_package.get("ticker_universe_selection_approved")),
        _check("scope_expansion_authorized_false", False, review_package.get("scope_expansion_authorized")),
        _check("expanded_ticker_universe_approved_false", False, review_package.get("expanded_ticker_universe_approved")),
        _check("new_ticker_authority_created_false", False, review_package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("candidate_entries_status_unvalidated", True, _entries_have("candidate_entry_status", PROPOSED_UNVALIDATED, review_package)),
        _check("candidate_entries_listing_not_verified", True, _entries_have("listing_status", NOT_VERIFIED, review_package)),
        _check("candidate_entries_security_type_not_verified", True, _entries_have("security_type_status", NOT_VERIFIED, review_package)),
        _check("candidate_entries_exchange_not_verified", True, _entries_have("exchange_status", NOT_VERIFIED, review_package)),
        _check("candidate_entries_authority_not_created", True, _entry_authorities_not_created(review_package)),
        _check("candidate_entries_runtime_not_authorized", True, _entry_uses_not_authorized(review_package)),
        _check("intended_diversity_tags_unverified", INTENDED_DIVERSITY_TAGS_STATUS, review_package.get("intended_diversity_tags_status")),
        _check("selection_rationale_research_only", RESEARCH_ONLY_NON_ACTIONABLE, review_package.get("selection_rationale_status")),
        _check("future_validation_gates_13", 13, review_package.get("future_validation_gate_count")),
        _check("future_authority_chain_15_steps", 15, review_package.get("future_ticker_authority_chain_step_count")),
        _check("planned_outputs_7", 7, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("additional_predictive_evidence_execution_authorized_false", False, review_package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, review_package.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, review_package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, review_package.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, review_package.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, review_package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_ticker_universe_selection_approval_created", False, review_package.get("ticker_universe_selection_approval_created")),
        _check("no_expanded_ticker_universe_approval_created", False, review_package.get("expanded_ticker_universe_approval_created")),
        _check("no_new_ticker_authority_created", False, review_package.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_artifact_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_artifact_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_artifact_created")),
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
        "ready_for_operator_assessment": failed == 0,
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


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("ticker_universe_selection_candidate_review_package_digest", None)
    return payload


def ticker_universe_selection_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for the ticker universe candidate review package."""
    return semantic_digest(_digest_payload(review_package))


def build_ticker_universe_selection_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline review package without approving the ticker universe."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package["ticker_universe_selection_candidate_review_package_digest"] = (
        ticker_universe_selection_candidate_review_package_digest_v1(review_package)
    )
    validate_ticker_universe_selection_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_artifact_values = {
        "TICKER_UNIVERSE_SELECTION_APPROVED",
        "EXPANDED_TICKER_UNIVERSE_APPROVED",
        "TICKER_UNIVERSE_SELECTION_APPROVAL_CEREMONY",
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
        "provider_requests_made_in_review",
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
        "ready_for_ticker_universe_selection_approval",
        "ready_for_live_ticker_validation",
        "ready_for_new_ticker_authority_chain",
        "ready_for_acquisition",
        "ready_for_additional_predictive_evidence_execution_candidate",
        "ready_for_predictive_usefulness_acceptance_candidate",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in forbidden_artifact_values:
            raise TickerUniverseSelectionCandidateReviewPackageError(
                f"{current_path} must not emit {value}"
            )
        if key in forbidden_true_fields and value is True:
            raise TickerUniverseSelectionCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise TickerUniverseSelectionCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise TickerUniverseSelectionCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if key == "approved_expanded_ticker_universe" and value:
            raise TickerUniverseSelectionCandidateReviewPackageError(
                f"{current_path} must be empty"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_candidate_entries(review_package: dict[str, Any]) -> None:
    tickers = review_package.get("proposed_candidate_ticker_universe")
    entries = review_package.get("candidate_ticker_entries")
    if not isinstance(tickers, list) or not tickers:
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "proposed_candidate_ticker_universe missing"
        )
    if EXISTING_BASELINE_TICKER in tickers:
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "proposed ticker universe must not contain AAPL"
        )
    if len(tickers) != len(set(tickers)):
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "proposed ticker universe contains duplicates"
        )
    if not isinstance(entries, list) or len(entries) != len(tickers):
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "candidate_ticker_entries mismatch"
        )
    for entry in entries:
        ticker = entry.get("ticker")
        if ticker not in tickers:
            raise TickerUniverseSelectionCandidateReviewPackageError(
                "candidate ticker entry mismatch"
            )
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


def validate_ticker_universe_selection_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package without approving the ticker universe."""
    if not isinstance(review_package, dict):
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("ticker_universe_selection_candidate_binding_mode") not in {
        TICKER_UNIVERSE_SELECTION_CANDIDATE_STATUS_BINDING,
        TICKER_UNIVERSE_SELECTION_CANDIDATE_OBJECT_BINDING,
    }:
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "ticker_universe_selection_candidate_binding_mode mismatch"
        )
    for field in ("operator_decision_required", "created_offline", "research_only"):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
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
        "ready_for_ticker_universe_selection_approval",
        "ready_for_live_ticker_validation",
        "ready_for_new_ticker_authority_chain",
        "ready_for_acquisition",
        "ready_for_additional_predictive_evidence_execution_candidate",
        "ready_for_predictive_usefulness_acceptance_candidate",
        "ticker_universe_selection_approval_created",
        "expanded_ticker_universe_approval_created",
        "new_ticker_authority_artifact_created",
        "acquisition_authorization_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_artifact_created",
        "runtime_migration_approval_artifact_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_ticker_universe_selection_candidate_kind": (
            candidate_service.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE
        ),
        "reviewed_ticker_universe_selection_candidate_status": (
            candidate_service.TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_ticker_universe_selection_candidate_digest": (
            EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "reviewed_ticker_universe_selection_candidate_checklist_total": (
            EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_ticker_universe_selection_candidate_checklist_passed": (
            EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_ticker_universe_selection_candidate_checklist_failed": (
            EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_ticker_universe_selection_candidate_blocker_count": (
            EXPECTED_REVIEWED_TICKER_UNIVERSE_SELECTION_CANDIDATE_BLOCKER_COUNT
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
        "predictive_experiment_results_review_package_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_experiment_execution_digest": EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST,
        "predictive_experiment_execution_approval_digest": (
            EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "existing_baseline_ticker": EXISTING_BASELINE_TICKER,
        "proposed_candidate_ticker_universe": DEFAULT_PROPOSED_TICKER_UNIVERSE,
        "proposed_candidate_ticker_count": 12,
        "candidate_ticker_list_status": CANDIDATE_TICKER_LIST_STATUS,
        "approved_expanded_ticker_universe": [],
        "approved_expanded_ticker_count": 0,
        "intended_diversity_tags_status": INTENDED_DIVERSITY_TAGS_STATUS,
        "selection_rationale": SELECTION_RATIONALE,
        "selection_rationale_status": RESEARCH_ONLY_NON_ACTIONABLE,
        "future_validation_gates": FUTURE_VALIDATION_GATES,
        "future_validation_gate_count": 13,
        "future_ticker_authority_chain": _future_authority_chain(),
        "future_ticker_authority_chain_step_count": 15,
        "planned_outputs": _planned_outputs(),
        "planned_output_count": 7,
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }.items():
        value = review_package.get(field)
        if field in {"future_validation_gates", "future_ticker_authority_chain", "planned_outputs"} and not value:
            raise TickerUniverseSelectionCandidateReviewPackageError(f"{field} missing")
        _expect(value, expected, field)
    _validate_candidate_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise TickerUniverseSelectionCandidateReviewPackageError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise TickerUniverseSelectionCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("ticker_universe_selection_candidate_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "ticker_universe_selection_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        ticker_universe_selection_candidate_review_package_digest_v1(review_package),
        "ticker_universe_selection_candidate_review_package_digest",
    )
    return {
        "status": "TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "ticker_universe_selection_candidate_review_package_digest": digest,
        "reviewed_ticker_universe_selection_candidate_digest": review_package[
            "reviewed_ticker_universe_selection_candidate_digest"
        ],
        "proposed_candidate_ticker_count": review_package["proposed_candidate_ticker_count"],
        "candidate_ticker_list_status": review_package["candidate_ticker_list_status"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
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


def build_ticker_universe_selection_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized ticker universe selection candidate review summary."""
    validation = validate_ticker_universe_selection_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Ticker Universe Selection Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Ticker Universe Selection Candidate Operator Review Package v1.",
        "",
        "## Reviewed Ticker Universe Selection Candidate",
        f"- Candidate kind: `{review_package['reviewed_ticker_universe_selection_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_ticker_universe_selection_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_ticker_universe_selection_candidate_digest']}`",
        f"- Review package digest: `{validation['ticker_universe_selection_candidate_review_package_digest']}`",
        "",
        "## Source Scope Expansion Evidence",
        f"- Scope expansion review package digest: `{review_package['predictive_evidence_scope_expansion_plan_candidate_review_package_digest']}`",
        f"- Scope expansion candidate digest: `{review_package['predictive_evidence_scope_expansion_plan_candidate_digest']}`",
        "",
        "## Proposed Unvalidated Candidate Ticker Universe",
        f"- Existing baseline ticker: `{review_package['existing_baseline_ticker']}`",
        f"- Candidate ticker list status: `{review_package['candidate_ticker_list_status']}`",
        f"- Proposed candidate ticker count: `{review_package['proposed_candidate_ticker_count']}`",
    ]
    lines.extend(f"- `{ticker}`" for ticker in review_package["proposed_candidate_ticker_universe"])
    lines.extend(
        [
            "",
            "## Intended Diversity Tags",
            f"- intended_diversity_tags_status: `{review_package['intended_diversity_tags_status']}`",
            "",
            "## Selection Rationale",
        ]
    )
    lines.extend(f"- `{item}`" for item in review_package["selection_rationale"])
    lines.extend(["", "## Future Validation Required"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_validation_gates"])
    lines.extend(["", "## Future Per-Ticker Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: `{step['authority_step']}`"
        for step in review_package["future_ticker_authority_chain"]
    )
    lines.extend(["", "## Planned Outputs"])
    lines.extend(
        f"- `{item['output_id']}`: `{item['generation_status']}`, `{item['actionability_label']}`"
        for item in review_package["planned_outputs"]
    )
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- ticker_universe_selection_approved: `{review_package['ticker_universe_selection_approved']}`",
            f"- expanded_ticker_universe_approved: `{review_package['expanded_ticker_universe_approved']}`",
            f"- approved_expanded_ticker_universe: `{review_package['approved_expanded_ticker_universe']}`",
            f"- live_ticker_validation_performed: `{review_package['live_ticker_validation_performed']}`",
            f"- final_ticker_selection_performed: `{review_package['final_ticker_selection_performed']}`",
            f"- new_ticker_authority_created: `{review_package['new_ticker_authority_created']}`",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- ready_for_operator_assessment: `{summary['ready_for_operator_assessment']}`",
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


def write_ticker_universe_selection_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the ticker universe selection candidate review package without overwriting."""
    review_package = build_ticker_universe_selection_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_ticker_universe_selection_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "ticker_universe_selection_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "ticker universe selection candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise TickerUniverseSelectionCandidateReviewPackageError(
            "ticker universe selection candidate review output already exists"
        )
    payload = canonical_json_bytes(review_package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
