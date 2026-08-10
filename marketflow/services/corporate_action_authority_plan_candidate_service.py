"""Offline corporate-action authority plan candidate for identity-approved tickers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import post_identity_freeze_registry_inventory_approval_service as approval_service


ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE"
)
SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_V1 = (
    "corporate_action_authority_plan_candidate_v1"
)
CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    "c380dd016035289d11b79723daafc6bdec694928233ff464ec386239ea820c82"
)

CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE = (
    "PLAN_SPLIT_AND_DIVIDEND_AUTHORITY_CHAINS_FOR_IDENTITY_APPROVED_EXPANDED_UNIVERSE"
)
CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE = "CORPORATE_ACTION_AUTHORITY_PLANNING_ONLY"
CORPORATE_ACTION_AUTHORITY_PLAN_MODE = "CANDIDATE_ONLY_NOT_AUTHORITY"
CORPORATE_ACTION_AUTHORITY_CREATION_STATUS = "NOT_CREATED"
PLANNED_NOT_CREATED = "PLANNED_NOT_CREATED"
NOT_CREATED = "NOT_CREATED"
BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN = (
    "BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN"
)
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(approval_service.VALIDATION_TARGET_UNIVERSE)

PLAN_SCOPE = [
    "split_event_authority_chain",
    "dividend_event_authority_chain",
    "corporate_action_evidence_reconciliation",
    "corporate_action_discrepancy_triage",
    "future_acquisition_preconditions",
]

CORPORATE_ACTION_EVIDENCE_REQUIREMENTS = [
    "split_event_history",
    "split_ratio",
    "split_execution_date",
    "split_ex_date",
    "split_provider_event_id_if_available",
    "split_adjustment_implication",
    "dividend_event_history",
    "cash_dividend_amount",
    "dividend_currency",
    "dividend_ex_date",
    "dividend_record_date_if_available",
    "dividend_pay_date_if_available",
    "dividend_provider_event_id_if_available",
    "dividend_adjustment_implication",
    "corporate_action_source_endpoint",
    "provider_response_digest",
    "sanitized_event_digest",
]
CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY = {
    "requirements_status": "PLANNED_REQUIREMENTS_ONLY_NOT_FETCHED",
    "provider_requests_made": False,
    "future_unavailable_fields_policy": "MARK_UNAVAILABLE_IN_FUTURE_CANDIDATE",
    "fabrication_policy": "NO_FIELD_MAY_BE_FABRICATED",
}

FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN = [
    "Split event authority candidate.",
    "Split provider evidence request approval, if live provider access is required.",
    "Split provider evidence execution.",
    "Split event authority candidate review package.",
    "Split event discrepancy triage, if required.",
    "Split event authority freeze ceremony.",
]

FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN = [
    "Dividend event authority candidate.",
    "Dividend provider evidence request approval, if live provider access is required.",
    "Dividend provider evidence execution.",
    "Dividend event authority candidate review package.",
    "Dividend policy reconciliation, including adjusted/unadjusted data implication.",
    "Dividend event discrepancy triage, if required.",
    "Dividend event authority freeze ceremony.",
]

FUTURE_CORPORATE_ACTION_READINESS_CHAIN = [
    "Combined corporate-action readiness review after split and dividend freeze.",
    "Corporate-action authority approval ceremony, if required.",
    "Acquisition generation candidate only after identity and corporate-action authority.",
    "Canonical dataset candidate only after acquisition generation freeze.",
    "Research registry approval only after canonical dataset freeze.",
]

FUTURE_GATES = [
    "corporate_action_authority_plan_operator_review",
    "corporate_action_authority_plan_approval_if_required",
    "split_event_authority_candidate",
    "split_event_provider_evidence_approval_if_required",
    "split_event_provider_evidence_execution",
    "split_event_authority_candidate_review",
    "split_event_authority_freeze",
    "dividend_event_authority_candidate",
    "dividend_event_provider_evidence_approval_if_required",
    "dividend_event_provider_evidence_execution",
    "dividend_event_authority_candidate_review",
    "dividend_policy_reconciliation",
    "dividend_event_authority_freeze",
    "combined_corporate_action_readiness_review",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]

RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "no_split_event_authority_without_operator_review",
    "no_dividend_event_authority_without_operator_review",
    "no_corporate_action_authority_without_split_and_dividend_freeze_or_explicit_policy",
    "no_acquisition_authority_without_identity_and_corporate_action_authority",
    "no_dataset_generation_without_acquisition_freeze",
    "no_runtime_source_switch",
    "no_automatic_stitching",
    "no_broker_execution",
    "no_paper_trading",
    "no_trade_recommendations",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "all_outputs_labeled_research_only",
    "operator_approval_required_before_any_provider_corporate_action_evidence_request",
]

PLANNED_OUTPUT_NAMES = [
    "corporate_action_authority_plan_manifest",
    "per_ticker_corporate_action_requirement_matrix",
    "split_event_authority_candidate_template",
    "dividend_event_authority_candidate_template",
    "corporate_action_provider_request_policy_template",
    "corporate_action_discrepancy_triage_template",
    "dividend_policy_reconciliation_template",
    "combined_corporate_action_readiness_template",
    "operator_review_summary_template",
]

REQUIRED_CHECK_IDS = [
    "registry_inventory_approval_digest_bound",
    "registry_inventory_review_digest_bound",
    "registry_inventory_candidate_digest_bound",
    "identity_freeze_digest_bound",
    "identity_candidate_review_digest_bound",
    "live_validation_results_review_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_identity_inventory_universe",
    "identity_authority_frozen_true",
    "registry_inventory_approved_true",
    "corporate_action_plan_objective_defined",
    "corporate_action_plan_scope_planning_only",
    "corporate_action_plan_mode_candidate_only_not_authority",
    "corporate_action_authority_creation_status_not_created",
    "plan_scope_defined",
    "per_ticker_corporate_action_plan_entries_12",
    "per_ticker_identity_status_frozen",
    "per_ticker_registry_inventory_approved_for_future_corporate_action_planning",
    "per_ticker_split_event_authority_not_created",
    "per_ticker_dividend_event_authority_not_created",
    "per_ticker_corporate_action_plan_digests_present",
    "corporate_action_evidence_requirements_defined",
    "corporate_action_evidence_requirements_not_fetched",
    "split_event_authority_chain_defined",
    "dividend_event_authority_chain_defined",
    "corporate_action_readiness_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_false",
    "corporate_action_authority_plan_approved_false",
    "corporate_action_authority_created_false",
    "split_event_authority_candidate_created_false",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "dividend_event_authority_candidate_created_false",
    "dividend_event_authority_created_false",
    "dividend_event_authority_frozen_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "acquisition_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "registry_approval_created_false",
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
    "no_corporate_action_authority_artifact_created",
    "no_split_event_authority_artifact_created",
    "no_dividend_event_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CorporateActionAuthorityPlanCandidateError(ValueError):
    """Raised when the corporate-action authority plan candidate is invalid."""


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
        raise CorporateActionAuthorityPlanCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise CorporateActionAuthorityPlanCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise CorporateActionAuthorityPlanCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _default_registry_inventory_approval_artifact() -> dict[str, Any]:
    attestation = approval_service.build_post_identity_freeze_registry_inventory_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-10T00:00:00Z",
        operator_attestation_phrase=(
            approval_service.REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE
        ),
        operator_confirms_registry_inventory_candidate_review_package_digest=(
            approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        operator_confirms_registry_inventory_candidate_digest=(
            approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        ),
        operator_confirms_identity_freeze_digest=(
            approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        operator_confirms_identity_authority_scope_identity_only=True,
        operator_confirms_target_universe=approval_service.VALIDATION_TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_registry_inventory_scope_identity_inventory_only=True,
        operator_confirms_registry_inventory_entries_reviewed=True,
        operator_confirms_no_provider_requests_in_approval=True,
        operator_confirms_no_live_validation_rerun=True,
        operator_confirms_no_live_provider_transport_enabled=True,
        operator_confirms_no_corporate_action_authority=True,
        operator_confirms_no_split_event_authority=True,
        operator_confirms_no_dividend_event_authority=True,
        operator_confirms_no_acquisition_authority=True,
        operator_confirms_no_dataset_generation_authorization=True,
        operator_confirms_no_additional_predictive_evidence_execution=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_runtime_activation=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )
    return approval_service.build_post_identity_freeze_registry_inventory_approved_v1(
        operator_attestation=attestation
    )


def _approval_for_binding(
    registry_inventory_approval_artifact: dict[str, Any] | None,
) -> dict[str, Any]:
    artifact = (
        _default_registry_inventory_approval_artifact()
        if registry_inventory_approval_artifact is None
        else deepcopy(registry_inventory_approval_artifact)
    )
    approval_service.validate_post_identity_freeze_registry_inventory_approved_v1(artifact)
    return artifact


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "planned_output": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _per_ticker_plan_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_corporate_action_plan_digest", None)
    return payload


def per_ticker_corporate_action_plan_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker plan entry."""
    return semantic_digest(_per_ticker_plan_digest_payload(entry))


def _per_ticker_plan_entries(approval_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    approval_digest = approval_artifact["post_identity_freeze_registry_inventory_approval_digest"]
    identity_digest = approval_artifact["identity_authority_freeze_digest"]
    for source in approval_artifact.get("per_ticker_registry_inventory_approval_entries", []):
        entry = {
            "ticker": source.get("ticker"),
            "identity_authority_status": approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            "registry_inventory_status": (
                approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
            ),
            "corporate_action_plan_status": PLANNED_NOT_CREATED,
            "split_event_authority_status": NOT_CREATED,
            "dividend_event_authority_status": NOT_CREATED,
            "corporate_action_authority_created": False,
            "acquisition_precondition_status": (
                BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN
            ),
            "dataset_generation_authorized": False,
            "runtime_use": approval_artifact["runtime_use"],
            "strategy_use": approval_artifact["strategy_use"],
            "paper_trading": approval_artifact["paper_trading"],
            "broker_execution": approval_artifact["broker_execution"],
            "source_identity_freeze_digest": identity_digest,
            "source_registry_inventory_approval_digest": approval_digest,
            "source_per_ticker_registry_inventory_approval_digest_if_available": (
                source.get("per_ticker_registry_inventory_approval_digest")
            ),
        }
        entry["per_ticker_corporate_action_plan_digest"] = (
            per_ticker_corporate_action_plan_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_corporate_action_plan_entries")
    return entries if isinstance(entries, list) else []


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _planned_outputs_not_generated(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and all(
        item.get("generation_status") == PLANNED_NOT_GENERATED for item in outputs
    )


def _planned_outputs_research_only(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and all(
        item.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE for item in outputs
    )


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _entries(candidate)
    not_authorized = approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    return [
        _check("registry_inventory_approval_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, candidate.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("registry_inventory_review_digest_bound", approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, candidate.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("identity_authority_candidate_review_package_digest")),
        _check("live_validation_results_review_digest_bound", approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("live_ticker_validation_results_review_package_digest")),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check("target_universe_matches_identity_inventory_universe", VALIDATION_TARGET_UNIVERSE, candidate.get("target_universe")),
        _check("identity_authority_frozen_true", True, candidate.get("identity_authority_frozen")),
        _check("registry_inventory_approved_true", True, candidate.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_plan_objective_defined", CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE, candidate.get("corporate_action_authority_plan_objective")),
        _check("corporate_action_plan_scope_planning_only", CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE, candidate.get("corporate_action_authority_plan_scope")),
        _check("corporate_action_plan_mode_candidate_only_not_authority", CORPORATE_ACTION_AUTHORITY_PLAN_MODE, candidate.get("corporate_action_authority_plan_mode")),
        _check("corporate_action_authority_creation_status_not_created", CORPORATE_ACTION_AUTHORITY_CREATION_STATUS, candidate.get("corporate_action_authority_creation_status")),
        _check("plan_scope_defined", PLAN_SCOPE, candidate.get("plan_scope")),
        _check("per_ticker_corporate_action_plan_entries_12", 12, len(entries)),
        _check("per_ticker_identity_status_frozen", True, all(entry.get("identity_authority_status") == approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN for entry in entries)),
        _check("per_ticker_registry_inventory_approved_for_future_corporate_action_planning", True, all(entry.get("registry_inventory_status") == approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY for entry in entries)),
        _check("per_ticker_split_event_authority_not_created", True, all(entry.get("split_event_authority_status") == NOT_CREATED for entry in entries)),
        _check("per_ticker_dividend_event_authority_not_created", True, all(entry.get("dividend_event_authority_status") == NOT_CREATED for entry in entries)),
        _check("per_ticker_corporate_action_plan_digests_present", True, _digests_present(entries, "per_ticker_corporate_action_plan_digest")),
        _check("corporate_action_evidence_requirements_defined", CORPORATE_ACTION_EVIDENCE_REQUIREMENTS, candidate.get("corporate_action_evidence_requirements")),
        _check("corporate_action_evidence_requirements_not_fetched", False, candidate.get("corporate_action_evidence_requirement_policy", {}).get("provider_requests_made")),
        _check("split_event_authority_chain_defined", FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN, candidate.get("future_split_event_authority_chain")),
        _check("dividend_event_authority_chain_defined", FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN, candidate.get("future_dividend_event_authority_chain")),
        _check("corporate_action_readiness_chain_defined", FUTURE_CORPORATE_ACTION_READINESS_CHAIN, candidate.get("future_corporate_action_readiness_chain")),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(candidate)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(candidate)),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_validation_rerun_performed_false", False, candidate.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("corporate_action_authority_plan_approved_false", False, candidate.get("corporate_action_authority_plan_approved")),
        _check("corporate_action_authority_created_false", False, candidate.get("corporate_action_authority_created")),
        _check("split_event_authority_candidate_created_false", False, candidate.get("split_event_authority_candidate_created")),
        _check("split_event_authority_created_false", False, candidate.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, candidate.get("split_event_authority_frozen")),
        _check("dividend_event_authority_candidate_created_false", False, candidate.get("dividend_event_authority_candidate_created")),
        _check("dividend_event_authority_created_false", False, candidate.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, candidate.get("dividend_event_authority_frozen")),
        _check("new_ticker_acquisition_authorized_false", False, candidate.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, candidate.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, candidate.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, candidate.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, candidate.get("registry_approval_created")),
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
        _check("runtime_use_not_authorized", not_authorized, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", not_authorized, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", not_authorized, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", not_authorized, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, candidate.get("corporate_action_authority_artifact_created")),
        _check("no_split_event_authority_artifact_created", False, candidate.get("split_event_authority_artifact_created")),
        _check("no_dividend_event_authority_artifact_created", False, candidate.get("dividend_event_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, candidate.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blockers = [item for item in failed if item["severity"] == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_review": not failed,
        "ready_for_corporate_action_authority_plan_approval": False,
        "ready_for_split_event_authority_candidate": False,
        "ready_for_dividend_event_authority_candidate": False,
        "corporate_action_authority_authorized": False,
        "split_event_authority_authorized": False,
        "dividend_event_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _candidate_digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("corporate_action_authority_plan_candidate_digest", None)
    return payload


def corporate_action_authority_plan_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the plan candidate."""
    return semantic_digest(_candidate_digest_payload(candidate))


def build_corporate_action_authority_plan_candidate_v1(
    *,
    registry_inventory_approval_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline corporate-action authority plan candidate."""
    approval_artifact = _approval_for_binding(registry_inventory_approval_artifact)
    not_authorized = approval_artifact["runtime_use"]
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE,
        "schema_version": SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_V1,
        "candidate_status": CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled": False,
        "corporate_action_authority_plan_candidate_created": True,
        "corporate_action_authority_plan_review_created": False,
        "corporate_action_authority_plan_approved": False,
        "corporate_action_authority_created": False,
        "corporate_action_authority_artifact_created": False,
        "split_event_authority_candidate_created": False,
        "split_event_authority_review_created": False,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "split_event_authority_artifact_created": False,
        "dividend_event_authority_candidate_created": False,
        "dividend_event_authority_review_created": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "dividend_event_authority_artifact_created": False,
        "post_identity_freeze_registry_inventory_approved": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": approval_artifact["authority_scope"],
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
        "runtime_use": not_authorized,
        "strategy_use": not_authorized,
        "paper_trading": not_authorized,
        "broker_execution": not_authorized,
        "automatic_stitching": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "post_identity_freeze_registry_inventory_approval_digest": approval_artifact[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": approval_artifact[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": approval_artifact[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": approval_artifact["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": approval_artifact[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": approval_artifact[
            "identity_authority_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": approval_artifact[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": approval_artifact[
            "live_ticker_validation_execution_digest"
        ],
        "ticker_universe_selection_approval_digest": approval_artifact[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(approval_artifact["target_universe"]),
        "identity_inventory_universe": list(approval_artifact["target_universe"]),
        "target_universe_count": approval_artifact["target_universe_count"],
        "corporate_action_authority_plan_objective": CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE,
        "corporate_action_authority_plan_scope": CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE,
        "corporate_action_authority_plan_mode": CORPORATE_ACTION_AUTHORITY_PLAN_MODE,
        "corporate_action_authority_creation_status": CORPORATE_ACTION_AUTHORITY_CREATION_STATUS,
        "plan_scope": list(PLAN_SCOPE),
        "per_ticker_corporate_action_plan_entries": _per_ticker_plan_entries(approval_artifact),
        "corporate_action_evidence_requirements": list(CORPORATE_ACTION_EVIDENCE_REQUIREMENTS),
        "corporate_action_evidence_requirement_policy": deepcopy(
            CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY
        ),
        "future_split_event_authority_chain": list(FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN),
        "future_dividend_event_authority_chain": list(FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN),
        "future_corporate_action_readiness_chain": list(FUTURE_CORPORATE_ACTION_READINESS_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
    }
    checklist = _checklist(candidate)
    candidate["plan_checklist"] = checklist
    candidate["plan_summary"] = _summary(checklist)
    candidate["corporate_action_authority_plan_candidate_digest"] = (
        corporate_action_authority_plan_candidate_digest_v1(candidate)
    )
    validate_corporate_action_authority_plan_candidate_v1(candidate)
    return candidate


def _validate_entries(candidate: dict[str, Any]) -> None:
    entries = _entries(candidate)
    if len(entries) != 12:
        raise CorporateActionAuthorityPlanCandidateError(
            "per_ticker_corporate_action_plan_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_corporate_action_plan_entries tickers",
    )
    not_authorized = approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_authority_status"),
            approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            f"{ticker}.identity_authority_status",
        )
        _expect(
            entry.get("registry_inventory_status"),
            approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            f"{ticker}.registry_inventory_status",
        )
        _expect(entry.get("corporate_action_plan_status"), PLANNED_NOT_CREATED, f"{ticker}.corporate_action_plan_status")
        _expect(entry.get("split_event_authority_status"), NOT_CREATED, f"{ticker}.split_event_authority_status")
        _expect(entry.get("dividend_event_authority_status"), NOT_CREATED, f"{ticker}.dividend_event_authority_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect(entry.get("acquisition_precondition_status"), BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN, f"{ticker}.acquisition_precondition_status")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), not_authorized, f"{ticker}.{field}")
        for field in (
            "source_identity_freeze_digest",
            "source_registry_inventory_approval_digest",
            "source_per_ticker_registry_inventory_approval_digest_if_available",
            "per_ticker_corporate_action_plan_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise CorporateActionAuthorityPlanCandidateError(f"{field} missing")
        _expect(
            entry["per_ticker_corporate_action_plan_digest"],
            per_ticker_corporate_action_plan_digest_v1(entry),
            f"{ticker}.per_ticker_corporate_action_plan_digest",
        )


def validate_corporate_action_authority_plan_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the corporate-action authority plan candidate."""
    if not isinstance(candidate, dict):
        raise CorporateActionAuthorityPlanCandidateError("candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline",
        "corporate_action_authority_plan_candidate_created",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
        "corporate_action_authority_plan_review_created",
        "corporate_action_authority_plan_approved",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
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
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(candidate.get(field), field)
    not_authorized = approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), not_authorized, field)
    for field, expected in {
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_digest": approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST,
        "identity_authority_freeze_digest": approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "ticker_universe_selection_approval_digest": approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "identity_inventory_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "corporate_action_authority_plan_objective": CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE,
        "corporate_action_authority_plan_scope": CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE,
        "corporate_action_authority_plan_mode": CORPORATE_ACTION_AUTHORITY_PLAN_MODE,
        "corporate_action_authority_creation_status": CORPORATE_ACTION_AUTHORITY_CREATION_STATUS,
        "plan_scope": PLAN_SCOPE,
        "corporate_action_evidence_requirements": CORPORATE_ACTION_EVIDENCE_REQUIREMENTS,
        "corporate_action_evidence_requirement_policy": CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY,
        "future_split_event_authority_chain": FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN,
        "future_dividend_event_authority_chain": FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN,
        "future_corporate_action_readiness_chain": FUTURE_CORPORATE_ACTION_READINESS_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": _planned_outputs(),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(candidate.get(field), expected, field)
    if candidate.get("target_universe") != candidate.get("identity_inventory_universe"):
        raise CorporateActionAuthorityPlanCandidateError(
            "target universe differs from identity inventory universe"
        )
    _validate_entries(candidate)
    checklist = candidate.get("plan_checklist")
    if not isinstance(checklist, list):
        raise CorporateActionAuthorityPlanCandidateError("plan_checklist missing")
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "plan_checklist check IDs")
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise CorporateActionAuthorityPlanCandidateError(
            f"plan checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "plan_checklist")
    _expect(candidate.get("plan_summary"), _summary(expected_checklist), "plan_summary")
    digest = candidate.get("corporate_action_authority_plan_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise CorporateActionAuthorityPlanCandidateError(
            "corporate_action_authority_plan_candidate_digest missing"
        )
    _expect(
        digest,
        corporate_action_authority_plan_candidate_digest_v1(candidate),
        "corporate_action_authority_plan_candidate_digest",
    )
    return {
        "status": "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "corporate_action_authority_plan_candidate_digest": digest,
        "post_identity_freeze_registry_inventory_approval_digest": candidate[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "target_universe_count": candidate["target_universe_count"],
        "per_ticker_corporate_action_plan_entry_count": len(_entries(candidate)),
        "total_checks": candidate["plan_summary"]["total_checks"],
        "passed_checks": candidate["plan_summary"]["passed_checks"],
        "failed_checks": candidate["plan_summary"]["failed_checks"],
        "blocker_count": candidate["plan_summary"]["blocker_count"],
        "ready_for_operator_review": candidate["plan_summary"]["ready_for_operator_review"],
        "ready_for_corporate_action_authority_plan_approval": False,
        "ready_for_split_event_authority_candidate": False,
        "ready_for_dividend_event_authority_candidate": False,
        "corporate_action_authority_authorized": False,
        "split_event_authority_authorized": False,
        "dividend_event_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_corporate_action_authority_plan_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized corporate-action authority plan candidate status document."""
    validation = validate_corporate_action_authority_plan_candidate_v1(candidate)
    summary = candidate["plan_summary"]
    lines = [
        "# MarketFlow Corporate-Action Authority Plan Candidate Status",
        "",
        "## Title",
        "- Corporate-Action Authority Plan Candidate v1.",
        "",
        "## Purpose",
        f"- Objective: `{candidate['corporate_action_authority_plan_objective']}`",
        f"- Scope: `{candidate['corporate_action_authority_plan_scope']}`",
        f"- Mode: `{candidate['corporate_action_authority_plan_mode']}`",
        "",
        "## Source Identity Registry Inventory Approval",
        f"- Approval digest: `{candidate['post_identity_freeze_registry_inventory_approval_digest']}`",
        f"- Review package digest: `{candidate['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        f"- Candidate digest: `{candidate['post_identity_freeze_registry_inventory_candidate_digest']}`",
        f"- Identity freeze digest: `{candidate['identity_authority_freeze_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{candidate['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]),
        "",
        "## Corporate-Action Authority Plan Objective",
        f"- `{candidate['corporate_action_authority_plan_objective']}`",
        "",
        "## Per-Ticker Corporate-Action Plan Entries",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['corporate_action_plan_status']}`, split `{entry['split_event_authority_status']}`, dividend `{entry['dividend_event_authority_status']}`, digest `{entry['per_ticker_corporate_action_plan_digest']}`"
        for entry in _entries(candidate)
    )
    lines.extend(["", "## Corporate-Action Evidence Requirements"])
    lines.extend(f"- `{item}`" for item in candidate["corporate_action_evidence_requirements"])
    lines.extend(["", "## Future Split Event Authority Chain"])
    lines.extend(f"- {item}" for item in candidate["future_split_event_authority_chain"])
    lines.extend(["", "## Future Dividend Event Authority Chain"])
    lines.extend(f"- {item}" for item in candidate["future_dividend_event_authority_chain"])
    lines.extend(["", "## Future Corporate-Action Readiness Chain"])
    lines.extend(f"- {item}" for item in candidate["future_corporate_action_readiness_chain"])
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_plan_approved: `{candidate['corporate_action_authority_plan_approved']}`",
            f"- corporate_action_authority_created: `{candidate['corporate_action_authority_created']}`",
            f"- split_event_authority_created: `{candidate['split_event_authority_created']}`",
            f"- dividend_event_authority_created: `{candidate['dividend_event_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{candidate['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{candidate['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{candidate['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{candidate['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{candidate['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{candidate['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{candidate['predictive_usefulness']}`",
            f"- profitability: `{candidate['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
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
            f"- Ready for operator review: `{summary['ready_for_operator_review']}`",
            f"- Ready for corporate-action authority plan approval: `{summary['ready_for_corporate_action_authority_plan_approval']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled.",
            "- No corporate-action, split-event, dividend-event, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
            f"- Candidate digest: `{validation['corporate_action_authority_plan_candidate_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_corporate_action_authority_plan_candidate_v1(
    output_dir: str | Path,
    *,
    registry_inventory_approval_artifact: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the corporate-action authority plan candidate JSON without overwriting."""
    candidate = build_corporate_action_authority_plan_candidate_v1(
        registry_inventory_approval_artifact=registry_inventory_approval_artifact
    )
    validation = validate_corporate_action_authority_plan_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "corporate_action_authority_plan_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise CorporateActionAuthorityPlanCandidateError(
            "corporate-action authority plan candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise CorporateActionAuthorityPlanCandidateError(
            "corporate-action authority plan candidate output already exists"
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
