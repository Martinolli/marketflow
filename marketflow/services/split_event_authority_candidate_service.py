"""Offline split-event authority candidate for identity-approved expanded-universe tickers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import corporate_action_authority_plan_approval_service as approval


ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE = "SPLIT_EVENT_AUTHORITY_CANDIDATE"
SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_V1 = (
    "split_event_authority_candidate_v1"
)
SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW = (
    "SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW"
)
SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE = (
    "CREATE_SPLIT_EVENT_AUTHORITY_CANDIDATE_FOR_IDENTITY_APPROVED_EXPANDED_UNIVERSE"
)
SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_AUTHORITY"
SPLIT_EVENT_AUTHORITY_CREATION_STATUS = "NOT_CREATED"
SPLIT_EVENT_AUTHORITY_FREEZE_STATUS = "NOT_FROZEN"
NOT_CREATED = "NOT_CREATED"
NOT_FROZEN = "NOT_FROZEN"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_FETCHED = "NOT_FETCHED"
NOT_EVALUATED = "NOT_EVALUATED"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
BLOCKED_UNTIL_SPLIT_AND_DIVIDEND_AUTHORITY_FROZEN_OR_EXPLICIT_POLICY = (
    "BLOCKED_UNTIL_SPLIT_AND_DIVIDEND_AUTHORITY_FROZEN_OR_EXPLICIT_POLICY"
)

EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    "bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f"
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
)

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

VALIDATION_TARGET_UNIVERSE = list(approval.review.VALIDATION_TARGET_UNIVERSE)

SPLIT_EVENT_EVIDENCE_REQUIREMENTS = [
    "split_event_history",
    "split_ratio",
    "split_execution_date",
    "split_ex_date",
    "split_provider_event_id_if_available",
    "split_adjustment_implication",
    "split_adjusted_price_impact_policy",
    "split_reverse_split_flag_if_available",
    "split_source_endpoint",
    "provider_response_digest",
    "sanitized_split_event_digest",
    "split_event_absence_policy_if_no_splits_returned",
]

SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY = {
    "requirements_status": "PLANNED_REQUIREMENTS_ONLY_NOT_FETCHED",
    "provider_requests_made": False,
    "future_unavailable_fields_policy": "MARK_UNAVAILABLE_IN_FUTURE_EVIDENCE_OR_CANDIDATE",
    "fabrication_policy": "NO_FIELD_MAY_BE_FABRICATED",
}

FUTURE_SPLIT_PROVIDER_REQUEST_POLICY = {
    "future_split_provider_request_policy_status": "PLANNED_REQUIRES_SEPARATE_APPROVAL",
    "allowed_future_request_type": "READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY",
    "api_key_handling": "DO_NOT_STORE_KEYS_OR_PRINT_KEYS",
    "raw_payload_policy": "DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS",
    "sanitized_status_doc_required": True,
    "rate_limit_policy": "RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED",
    "provider_result_authority": "SPLIT_EVENT_EVIDENCE_ONLY_NOT_SPLIT_AUTHORITY",
}

FUTURE_SPLIT_AUTHORITY_CHAIN = [
    "Split event authority candidate operator review package.",
    "Split provider evidence request approval ceremony, if live provider access is required.",
    "Split provider evidence execution.",
    "Split event evidence/results review package.",
    "Split event authority candidate update or discrepancy triage, if required.",
    "Split event authority freeze ceremony.",
]

FUTURE_CORPORATE_ACTION_READINESS_CHAIN = [
    "Dividend event authority candidate.",
    "Dividend event authority review/freeze chain.",
    "Combined split/dividend corporate-action readiness review.",
    "Corporate-action authority approval ceremony, if required.",
    "Acquisition generation candidate only after identity and corporate-action authority.",
    "Canonical dataset candidate only after acquisition generation freeze.",
    "Research registry approval only after canonical dataset freeze.",
]

FUTURE_GATES = [
    "split_event_authority_candidate_operator_review",
    "split_provider_evidence_request_approval_if_required",
    "split_provider_evidence_execution",
    "split_event_evidence_results_review",
    "split_event_discrepancy_triage_if_required",
    "split_event_authority_freeze",
    "dividend_event_authority_candidate",
    "dividend_event_authority_candidate_review",
    "combined_corporate_action_readiness_review",
    "corporate_action_authority_approval_if_required",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]

RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "no_split_event_authority_without_operator_review",
    "no_split_event_freeze_without_evidence_review_or_explicit_no_split_policy",
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
    "operator_approval_required_before_any_provider_split_evidence_request",
]

PLANNED_OUTPUT_NAMES = [
    "split_event_authority_candidate_operator_review_package",
    "split_provider_evidence_request_approval_ceremony_if_required",
    "split_provider_evidence_execution",
    "split_event_evidence_results_review_package",
    "split_event_discrepancy_triage_if_required",
    "split_event_authority_freeze_ceremony",
]

REQUIRED_CHECK_IDS = [
    "corporate_action_plan_approval_digest_bound",
    "corporate_action_plan_review_digest_bound",
    "corporate_action_plan_candidate_digest_bound",
    "registry_inventory_approval_digest_bound",
    "registry_inventory_review_digest_bound",
    "registry_inventory_candidate_digest_bound",
    "identity_freeze_digest_bound",
    "identity_candidate_review_digest_bound",
    "identity_candidate_digest_bound",
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_corporate_action_plan_universe",
    "identity_authority_frozen_true",
    "registry_inventory_approved_true",
    "corporate_action_plan_approved_true",
    "ready_for_split_event_authority_candidate_true",
    "split_event_candidate_objective_defined",
    "split_event_candidate_scope_candidate_only",
    "split_event_authority_creation_status_not_created",
    "split_event_authority_freeze_status_not_frozen",
    "per_ticker_split_event_candidate_entries_12",
    "per_ticker_split_event_candidate_status_ready",
    "per_ticker_split_event_authority_not_created",
    "per_ticker_split_event_freeze_not_frozen",
    "per_ticker_provider_evidence_request_not_authorized",
    "per_ticker_provider_evidence_execution_not_executed",
    "per_ticker_split_history_not_fetched",
    "per_ticker_split_event_candidate_digests_present",
    "split_event_evidence_requirements_defined",
    "future_split_provider_request_policy_defined",
    "future_split_authority_chain_defined",
    "future_corporate_action_readiness_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_false",
    "split_event_authority_review_created_false",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "split_provider_evidence_request_authorized_false",
    "split_provider_evidence_executed_false",
    "split_provider_evidence_results_created_false",
    "dividend_event_authority_candidate_created_false",
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
    "no_split_event_authority_artifact_created",
    "no_split_event_authority_freeze_created",
    "no_dividend_event_authority_artifact_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class SplitEventAuthorityCandidateError(ValueError):
    """Raised when the split-event authority candidate violates guardrails."""


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
        raise SplitEventAuthorityCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventAuthorityCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventAuthorityCandidateError(f"{field_name} must be false")


def _not_authorized() -> str:
    return approval.review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED


def _authority_scope() -> str:
    return approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY


def _source_binding(approval_artifact: dict[str, Any] | None) -> dict[str, Any]:
    if approval_artifact is not None:
        try:
            validation = approval.validate_corporate_action_authority_plan_approved_v1(
                approval_artifact
            )
        except approval.CorporateActionAuthorityPlanApprovalError as exc:
            raise SplitEventAuthorityCandidateError(
                f"source plan approval invalid: {exc}"
            ) from exc
        _expect(
            validation["corporate_action_authority_plan_approval_digest"],
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
            "corporate_action_authority_plan_approval_digest",
        )
        return deepcopy(approval_artifact)
    return {
        "artifact_kind": approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "approval_status": approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "approval_scope": approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "corporate_action_authority_plan_approval_digest": (
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "source_corporate_action_plan_review_package_digest": (
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "source_corporate_action_plan_candidate_digest": (
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "post_identity_freeze_registry_inventory_approval_digest": (
            approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": (
            approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "post_identity_freeze_registry_inventory_candidate_digest": (
            approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        ),
        "identity_authority_freeze_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "identity_authority_candidate_review_package_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_candidate_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "authority_scope": _authority_scope(),
    }


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "output_name": output_name,
            "generation_status": PLANNED_NOT_GENERATED,
            "generated": False,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for output_name in PLANNED_OUTPUT_NAMES
    ]


def _split_entry_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_split_event_candidate_digest", None)
    return payload


def per_ticker_split_event_candidate_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker split candidate entry."""
    return semantic_digest(_split_entry_digest_payload(entry))


def _per_ticker_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in source["target_universe"]:
        entry = {
            "ticker": ticker,
            "identity_authority_status": (
                approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN
            ),
            "registry_inventory_status": (
                approval.review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
            ),
            "corporate_action_plan_status": (
                approval.APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY
            ),
            "split_event_candidate_status": SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "split_event_authority_status": NOT_CREATED,
            "split_event_freeze_status": NOT_FROZEN,
            "provider_evidence_request_status": NOT_AUTHORIZED,
            "provider_evidence_execution_status": NOT_EXECUTED,
            "split_history_status": NOT_FETCHED,
            "split_event_count_status": NOT_EVALUATED,
            "corporate_action_authority_created": False,
            "acquisition_precondition_status": (
                BLOCKED_UNTIL_SPLIT_AND_DIVIDEND_AUTHORITY_FROZEN_OR_EXPLICIT_POLICY
            ),
            "dataset_generation_authorized": False,
            "runtime_use": _not_authorized(),
            "strategy_use": _not_authorized(),
            "paper_trading": _not_authorized(),
            "broker_execution": _not_authorized(),
            "source_identity_freeze_digest": source["identity_authority_freeze_digest"],
            "source_registry_inventory_approval_digest": source[
                "post_identity_freeze_registry_inventory_approval_digest"
            ],
            "source_corporate_action_plan_approval_digest": source[
                "corporate_action_authority_plan_approval_digest"
            ],
        }
        entry["per_ticker_split_event_candidate_digest"] = (
            per_ticker_split_event_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _all_entry_field(entries: list[dict[str, Any]], field_name: str, expected: Any) -> bool:
    return len(entries) == 12 and all(entry.get(field_name) == expected for entry in entries)


def _planned_outputs_not_generated(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        output.get("generation_status") == PLANNED_NOT_GENERATED
        and output.get("generated") is False
        for output in outputs
    )


def _planned_outputs_research_only(candidate: dict[str, Any]) -> bool:
    outputs = candidate.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        output.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE
        for output in outputs
    )


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_split_event_candidate_entries")
    entries = entries if isinstance(entries, list) else []
    return [
        _check("corporate_action_plan_approval_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, candidate.get("corporate_action_authority_plan_approval_digest")),
        _check("corporate_action_plan_review_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("corporate_action_authority_plan_candidate_review_package_digest")),
        _check("corporate_action_plan_candidate_digest_bound", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, candidate.get("corporate_action_authority_plan_candidate_digest")),
        _check("registry_inventory_approval_digest_bound", approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, candidate.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("registry_inventory_review_digest_bound", approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, candidate.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, candidate.get("identity_authority_candidate_digest")),
        _check("live_validation_results_review_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("live_ticker_validation_results_review_package_digest")),
        _check("live_validation_execution_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST, candidate.get("live_ticker_validation_execution_digest")),
        _check("ticker_universe_selection_approval_digest_bound", approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, candidate.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check("target_universe_matches_corporate_action_plan_universe", True, candidate.get("target_universe") == candidate.get("corporate_action_plan_universe") == VALIDATION_TARGET_UNIVERSE),
        _check("identity_authority_frozen_true", True, candidate.get("identity_authority_frozen")),
        _check("registry_inventory_approved_true", True, candidate.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_plan_approved_true", True, candidate.get("corporate_action_authority_plan_approved")),
        _check("ready_for_split_event_authority_candidate_true", True, candidate.get("ready_for_split_event_authority_candidate")),
        _check("split_event_candidate_objective_defined", SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE, candidate.get("split_event_authority_candidate_objective")),
        _check("split_event_candidate_scope_candidate_only", SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE, candidate.get("split_event_authority_candidate_scope")),
        _check("split_event_authority_creation_status_not_created", SPLIT_EVENT_AUTHORITY_CREATION_STATUS, candidate.get("split_event_authority_creation_status")),
        _check("split_event_authority_freeze_status_not_frozen", SPLIT_EVENT_AUTHORITY_FREEZE_STATUS, candidate.get("split_event_authority_freeze_status")),
        _check("per_ticker_split_event_candidate_entries_12", 12, len(entries)),
        _check("per_ticker_split_event_candidate_status_ready", True, _all_entry_field(entries, "split_event_candidate_status", SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW)),
        _check("per_ticker_split_event_authority_not_created", True, _all_entry_field(entries, "split_event_authority_status", NOT_CREATED)),
        _check("per_ticker_split_event_freeze_not_frozen", True, _all_entry_field(entries, "split_event_freeze_status", NOT_FROZEN)),
        _check("per_ticker_provider_evidence_request_not_authorized", True, _all_entry_field(entries, "provider_evidence_request_status", NOT_AUTHORIZED)),
        _check("per_ticker_provider_evidence_execution_not_executed", True, _all_entry_field(entries, "provider_evidence_execution_status", NOT_EXECUTED)),
        _check("per_ticker_split_history_not_fetched", True, _all_entry_field(entries, "split_history_status", NOT_FETCHED)),
        _check("per_ticker_split_event_candidate_digests_present", True, _digests_present(entries, "per_ticker_split_event_candidate_digest")),
        _check("split_event_evidence_requirements_defined", SPLIT_EVENT_EVIDENCE_REQUIREMENTS, candidate.get("split_event_evidence_requirements")),
        _check("future_split_provider_request_policy_defined", FUTURE_SPLIT_PROVIDER_REQUEST_POLICY, candidate.get("future_split_provider_request_policy")),
        _check("future_split_authority_chain_defined", FUTURE_SPLIT_AUTHORITY_CHAIN, candidate.get("future_split_authority_chain")),
        _check("future_corporate_action_readiness_chain_defined", FUTURE_CORPORATE_ACTION_READINESS_CHAIN, candidate.get("future_corporate_action_readiness_chain")),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(candidate)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(candidate)),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_validation_rerun_performed_false", False, candidate.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("split_event_authority_review_created_false", False, candidate.get("split_event_authority_review_created")),
        _check("split_event_authority_created_false", False, candidate.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, candidate.get("split_event_authority_frozen")),
        _check("split_provider_evidence_request_authorized_false", False, candidate.get("split_provider_evidence_request_authorized")),
        _check("split_provider_evidence_executed_false", False, candidate.get("split_provider_evidence_executed")),
        _check("split_provider_evidence_results_created_false", False, candidate.get("split_provider_evidence_results_created")),
        _check("dividend_event_authority_candidate_created_false", False, candidate.get("dividend_event_authority_candidate_created")),
        _check("dividend_event_authority_created_false", False, candidate.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, candidate.get("dividend_event_authority_frozen")),
        _check("corporate_action_authority_created_false", False, candidate.get("corporate_action_authority_created")),
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
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness"), severity=INFO),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, candidate.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, candidate.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability"), severity=INFO),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, candidate.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", _not_authorized(), candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", _not_authorized(), candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", _not_authorized(), candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", _not_authorized(), candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_split_event_authority_artifact_created", False, candidate.get("split_event_authority_artifact_created")),
        _check("no_split_event_authority_freeze_created", False, candidate.get("split_event_authority_freeze_created")),
        _check("no_dividend_event_authority_artifact_created", False, candidate.get("dividend_event_authority_artifact_created")),
        _check("no_corporate_action_authority_artifact_created", False, candidate.get("corporate_action_authority_artifact_created")),
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
        "ready_for_split_event_provider_evidence_request_approval": False,
        "ready_for_split_event_authority_freeze": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
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


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("split_event_authority_candidate_digest", None)
    return payload


def split_event_authority_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the split-event candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_split_event_authority_candidate_v1(
    *,
    corporate_action_plan_approval_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline split-event authority candidate."""
    source = _source_binding(corporate_action_plan_approval_artifact)
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_V1,
        "candidate_status": SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": False,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "split_event_authority_artifact_created": False,
        "split_event_authority_freeze_created": False,
        "split_provider_evidence_request_authorized": False,
        "split_provider_evidence_executed": False,
        "split_provider_evidence_results_created": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "corporate_action_authority_artifact_created": False,
        "ready_for_split_event_authority_candidate": True,
        "ready_for_dividend_event_authority_candidate": True,
        "ready_for_split_event_provider_evidence_request_approval": False,
        "ready_for_split_event_authority_freeze": False,
        "dividend_event_authority_candidate_created": False,
        "dividend_event_authority_review_created": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "dividend_event_authority_artifact_created": False,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_provider_evidence_executed": False,
        "post_identity_freeze_registry_inventory_approved": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": source["authority_scope"],
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
        "runtime_use": _not_authorized(),
        "strategy_use": _not_authorized(),
        "paper_trading": _not_authorized(),
        "broker_execution": _not_authorized(),
        "automatic_stitching": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "source_corporate_action_plan_approval_kind": source["artifact_kind"],
        "source_corporate_action_plan_approval_status": source["approval_status"],
        "source_corporate_action_plan_approval_scope": source["approval_scope"],
        "corporate_action_authority_plan_approval_digest": source[
            "corporate_action_authority_plan_approval_digest"
        ],
        "corporate_action_authority_plan_candidate_review_package_digest": source[
            "source_corporate_action_plan_review_package_digest"
        ],
        "corporate_action_authority_plan_candidate_digest": source[
            "source_corporate_action_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": source[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": source[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": source[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": source["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": source[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": source[
            "identity_authority_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": source[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": source[
            "live_ticker_validation_execution_digest"
        ],
        "ticker_universe_selection_approval_digest": source[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(source["target_universe"]),
        "corporate_action_plan_universe": list(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "split_event_authority_candidate_objective": SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE,
        "split_event_authority_candidate_scope": SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE,
        "split_event_authority_creation_status": SPLIT_EVENT_AUTHORITY_CREATION_STATUS,
        "split_event_authority_freeze_status": SPLIT_EVENT_AUTHORITY_FREEZE_STATUS,
        "split_event_evidence_requirements": list(SPLIT_EVENT_EVIDENCE_REQUIREMENTS),
        "split_event_evidence_requirement_policy": deepcopy(
            SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY
        ),
        "future_split_provider_request_policy": deepcopy(
            FUTURE_SPLIT_PROVIDER_REQUEST_POLICY
        ),
        "future_split_authority_chain": list(FUTURE_SPLIT_AUTHORITY_CHAIN),
        "future_corporate_action_readiness_chain": list(
            FUTURE_CORPORATE_ACTION_READINESS_CHAIN
        ),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
    }
    candidate["per_ticker_split_event_candidate_entries"] = _per_ticker_entries(source)
    candidate["planned_output_count"] = len(candidate["planned_outputs"])
    candidate["planned_outputs_status"] = PLANNED_NOT_GENERATED
    candidate["planned_outputs_label"] = RESEARCH_ONLY_NON_ACTIONABLE
    checklist = _checklist(candidate)
    candidate["candidate_checklist"] = checklist
    candidate["candidate_summary"] = _summary(checklist)
    candidate["split_event_authority_candidate_digest"] = (
        split_event_authority_candidate_digest_v1(candidate)
    )
    validate_split_event_authority_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "SPLIT_EVENT_AUTHORITY_APPROVED",
            "SPLIT_EVENT_AUTHORITY_FROZEN",
            "SPLIT_EVENT_PROVIDER_EVIDENCE_REQUEST_APPROVED",
            "SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED",
            "DIVIDEND_EVENT_AUTHORITY_CANDIDATE",
            "DIVIDEND_EVENT_AUTHORITY_APPROVED",
            "DIVIDEND_EVENT_AUTHORITY_FROZEN",
            "CORPORATE_ACTION_AUTHORITY_APPROVED",
            "NEW_TICKER_ACQUISITION_AUTHORIZED",
            "ACQUISITION_GENERATION_AUTHORIZED",
            "CANONICAL_DATASET_AUTHORIZED",
            "REGISTRY_APPROVAL_CREATED",
            "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
            "TRADE_RECOMMENDATIONS",
        }:
            raise SplitEventAuthorityCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
            "live_validation_rerun_performed",
            "live_provider_transport_enabled",
            "split_event_authority_review_created",
            "split_event_authority_created",
            "split_event_authority_frozen",
            "split_event_authority_artifact_created",
            "split_event_authority_freeze_created",
            "split_provider_evidence_request_authorized",
            "split_provider_evidence_executed",
            "split_provider_evidence_results_created",
            "dividend_event_authority_candidate_created",
            "dividend_event_authority_review_created",
            "dividend_event_authority_created",
            "dividend_event_authority_frozen",
            "dividend_event_authority_artifact_created",
            "dividend_provider_evidence_request_authorized",
            "dividend_provider_evidence_executed",
            "corporate_action_authority_created",
            "corporate_action_authority_artifact_created",
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
            "generated",
        } and value is True:
            raise SplitEventAuthorityCandidateError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise SplitEventAuthorityCandidateError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise SplitEventAuthorityCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_entries(candidate: dict[str, Any]) -> None:
    entries = candidate.get("per_ticker_split_event_candidate_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise SplitEventAuthorityCandidateError(
            "per_ticker_split_event_candidate_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_split_event_candidate_entries tickers",
    )
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_authority_status"),
            approval.review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            f"{ticker}.identity_authority_status",
        )
        _expect(
            entry.get("registry_inventory_status"),
            approval.review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            f"{ticker}.registry_inventory_status",
        )
        _expect(
            entry.get("corporate_action_plan_status"),
            approval.APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY,
            f"{ticker}.corporate_action_plan_status",
        )
        _expect(entry.get("split_event_candidate_status"), SPLIT_EVENT_CANDIDATE_READY_FOR_OPERATOR_REVIEW, f"{ticker}.split_event_candidate_status")
        _expect(entry.get("split_event_authority_status"), NOT_CREATED, f"{ticker}.split_event_authority_status")
        _expect(entry.get("split_event_freeze_status"), NOT_FROZEN, f"{ticker}.split_event_freeze_status")
        _expect(entry.get("provider_evidence_request_status"), NOT_AUTHORIZED, f"{ticker}.provider_evidence_request_status")
        _expect(entry.get("provider_evidence_execution_status"), NOT_EXECUTED, f"{ticker}.provider_evidence_execution_status")
        _expect(entry.get("split_history_status"), NOT_FETCHED, f"{ticker}.split_history_status")
        _expect(entry.get("split_event_count_status"), NOT_EVALUATED, f"{ticker}.split_event_count_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect(
            entry.get("acquisition_precondition_status"),
            BLOCKED_UNTIL_SPLIT_AND_DIVIDEND_AUTHORITY_FROZEN_OR_EXPLICIT_POLICY,
            f"{ticker}.acquisition_precondition_status",
        )
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), _not_authorized(), f"{ticker}.{field}")
        for field in (
            "source_identity_freeze_digest",
            "source_registry_inventory_approval_digest",
            "source_corporate_action_plan_approval_digest",
            "per_ticker_split_event_candidate_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise SplitEventAuthorityCandidateError(f"{field} missing")
        _expect(
            entry["source_identity_freeze_digest"],
            candidate["identity_authority_freeze_digest"],
            f"{ticker}.source_identity_freeze_digest",
        )
        _expect(
            entry["source_registry_inventory_approval_digest"],
            candidate["post_identity_freeze_registry_inventory_approval_digest"],
            f"{ticker}.source_registry_inventory_approval_digest",
        )
        _expect(
            entry["source_corporate_action_plan_approval_digest"],
            candidate["corporate_action_authority_plan_approval_digest"],
            f"{ticker}.source_corporate_action_plan_approval_digest",
        )
        _expect(
            entry["per_ticker_split_event_candidate_digest"],
            per_ticker_split_event_candidate_digest_v1(entry),
            f"{ticker}.per_ticker_split_event_candidate_digest",
        )


def validate_split_event_authority_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the split-event candidate while preserving all downstream guardrails."""
    if not isinstance(candidate, dict):
        raise SplitEventAuthorityCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_AUTHORITY_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_AUTHORITY_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), SPLIT_EVENT_AUTHORITY_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    for field in (
        "created_offline",
        "split_event_authority_candidate_created",
        "corporate_action_authority_plan_approved",
        "ready_for_split_event_authority_candidate",
        "ready_for_dividend_event_authority_candidate",
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
        "split_event_authority_review_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "ready_for_split_event_provider_evidence_request_approval",
        "ready_for_split_event_authority_freeze",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "dividend_event_authority_artifact_created",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
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
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), _not_authorized(), field)
    for field, expected in {
        "source_corporate_action_plan_approval_kind": approval.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "source_corporate_action_plan_approval_status": approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "source_corporate_action_plan_approval_scope": approval.CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "corporate_action_authority_plan_candidate_review_package_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_candidate_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_digest": approval.review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST,
        "identity_authority_freeze_digest": approval.review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "ticker_universe_selection_approval_digest": approval.review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "corporate_action_plan_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": _authority_scope(),
        "split_event_authority_candidate_objective": SPLIT_EVENT_AUTHORITY_CANDIDATE_OBJECTIVE,
        "split_event_authority_candidate_scope": SPLIT_EVENT_AUTHORITY_CANDIDATE_SCOPE,
        "split_event_authority_creation_status": SPLIT_EVENT_AUTHORITY_CREATION_STATUS,
        "split_event_authority_freeze_status": SPLIT_EVENT_AUTHORITY_FREEZE_STATUS,
        "split_event_evidence_requirements": SPLIT_EVENT_EVIDENCE_REQUIREMENTS,
        "split_event_evidence_requirement_policy": SPLIT_EVENT_EVIDENCE_REQUIREMENT_POLICY,
        "future_split_provider_request_policy": FUTURE_SPLIT_PROVIDER_REQUEST_POLICY,
        "future_split_authority_chain": FUTURE_SPLIT_AUTHORITY_CHAIN,
        "future_corporate_action_readiness_chain": FUTURE_CORPORATE_ACTION_READINESS_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_output_count": len(PLANNED_OUTPUT_NAMES),
        "planned_outputs_status": PLANNED_NOT_GENERATED,
        "planned_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        if field in {
            "split_event_evidence_requirements",
            "future_split_provider_request_policy",
            "future_split_authority_chain",
            "future_corporate_action_readiness_chain",
            "future_gates",
            "risk_controls",
        } and not candidate.get(field):
            raise SplitEventAuthorityCandidateError(f"{field} missing")
        _expect(candidate.get(field), expected, field)
    if candidate.get("target_universe") != candidate.get("corporate_action_plan_universe"):
        raise SplitEventAuthorityCandidateError(
            "target universe differs from corporate-action plan universe"
        )
    if not _planned_outputs_not_generated(candidate):
        raise SplitEventAuthorityCandidateError("planned_outputs must not be generated")
    if not _planned_outputs_research_only(candidate):
        raise SplitEventAuthorityCandidateError("planned_outputs must be research only")
    _validate_entries(candidate)
    checklist = _checklist(candidate)
    _expect([item["check_id"] for item in checklist], REQUIRED_CHECK_IDS, "candidate_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise SplitEventAuthorityCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(candidate.get("candidate_checklist"), checklist, "candidate_checklist")
    summary = _summary(checklist)
    _expect(candidate.get("candidate_summary"), summary, "candidate_summary")
    _expect_true(summary.get("ready_for_operator_review"), "ready_for_operator_review")
    for field in (
        "ready_for_split_event_provider_evidence_request_approval",
        "ready_for_split_event_authority_freeze",
        "split_event_authority_authorized",
        "split_event_authority_frozen",
        "dividend_event_authority_authorized",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "predictive_usefulness_accepted",
        "profitability_accepted",
        "runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(summary.get(field), field)
    digest = candidate.get("split_event_authority_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise SplitEventAuthorityCandidateError(
            "split_event_authority_candidate_digest missing"
        )
    _expect(
        digest,
        split_event_authority_candidate_digest_v1(candidate),
        "split_event_authority_candidate_digest",
    )
    return {
        "status": "SPLIT_EVENT_AUTHORITY_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "split_event_authority_candidate_digest": digest,
        "corporate_action_authority_plan_approval_digest": candidate[
            "corporate_action_authority_plan_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": candidate[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "target_universe_count": candidate["target_universe_count"],
        "per_ticker_split_event_candidate_entry_count": len(
            candidate["per_ticker_split_event_candidate_entries"]
        ),
        "split_event_authority_candidate_created": True,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "split_provider_evidence_request_authorized": False,
        "split_provider_evidence_executed": False,
        "dividend_event_authority_candidate_created": False,
        "corporate_action_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": _not_authorized(),
        "strategy_use": _not_authorized(),
        "paper_trading": _not_authorized(),
        "broker_execution": _not_authorized(),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_split_event_authority_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized split-event authority candidate status document."""
    validation = validate_split_event_authority_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Split Event Authority Candidate Status",
        "",
        "## Title",
        "- Split Event Authority Candidate v1.",
        "",
        "## Purpose",
        "- Create an offline, digest-bound split event authority candidate for the identity-frozen expanded universe.",
        "- This candidate does not create split event authority or fetch provider split evidence.",
        "",
        "## Source Corporate-Action Plan Approval",
        f"- Approval digest: `{candidate['corporate_action_authority_plan_approval_digest']}`",
        f"- Plan review package digest: `{candidate['corporate_action_authority_plan_candidate_review_package_digest']}`",
        f"- Plan candidate digest: `{candidate['corporate_action_authority_plan_candidate_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{candidate['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]),
        "",
        "## Split Event Authority Candidate Objective",
        f"- split_event_authority_candidate_objective: `{candidate['split_event_authority_candidate_objective']}`",
        f"- split_event_authority_candidate_scope: `{candidate['split_event_authority_candidate_scope']}`",
        f"- split_event_authority_creation_status: `{candidate['split_event_authority_creation_status']}`",
        f"- split_event_authority_freeze_status: `{candidate['split_event_authority_freeze_status']}`",
        f"- Candidate digest: `{validation['split_event_authority_candidate_digest']}`",
        "",
        "## Per-Ticker Split Event Candidate Entries",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['split_event_candidate_status']}`, split authority `{entry['split_event_authority_status']}`, digest `{entry['per_ticker_split_event_candidate_digest']}`"
        for entry in candidate["per_ticker_split_event_candidate_entries"]
    )
    lines.extend(["", "## Split Event Evidence Requirements"])
    lines.extend(f"- `{item}`" for item in candidate["split_event_evidence_requirements"])
    lines.extend(["", "## Future Split Provider Request Policy"])
    lines.extend(
        f"- `{key}`: `{value}`"
        for key, value in candidate["future_split_provider_request_policy"].items()
    )
    lines.extend(["", "## Future Split Authority Chain"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(candidate["future_split_authority_chain"], start=1)
    )
    lines.extend(["", "## Future Corporate-Action Readiness Chain"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(
            candidate["future_corporate_action_readiness_chain"], start=1
        )
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Split Authority Boundary",
            f"- split_event_authority_candidate_created: `{candidate['split_event_authority_candidate_created']}`",
            f"- split_event_authority_review_created: `{candidate['split_event_authority_review_created']}`",
            f"- split_event_authority_created: `{candidate['split_event_authority_created']}`",
            f"- split_event_authority_frozen: `{candidate['split_event_authority_frozen']}`",
            f"- split_provider_evidence_request_authorized: `{candidate['split_provider_evidence_request_authorized']}`",
            f"- split_provider_evidence_executed: `{candidate['split_provider_evidence_executed']}`",
            "",
            "## Dividend Boundary",
            f"- dividend_event_authority_candidate_created: `{candidate['dividend_event_authority_candidate_created']}`",
            f"- dividend_event_authority_created: `{candidate['dividend_event_authority_created']}`",
            f"- dividend_event_authority_frozen: `{candidate['dividend_event_authority_frozen']}`",
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_created: `{candidate['corporate_action_authority_created']}`",
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
            f"- trade_recommendations_generated: `{candidate['trade_recommendations_generated']}`",
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
            f"- Ready for operator review: `{summary['ready_for_operator_review']}`",
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- No Massive.com / Polygon provider split evidence was fetched.",
            "- No split event authority, freeze, or provider evidence request authorization was created.",
            "- Dividend authority, corporate-action authority, acquisition, and dataset generation remain unauthorized.",
            "- Runtime, strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_split_event_authority_candidate_v1(
    output_dir: str | Path,
    *,
    corporate_action_plan_approval_artifact: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the split-event authority candidate JSON artifact without overwriting output."""
    candidate = build_split_event_authority_candidate_v1(
        corporate_action_plan_approval_artifact=corporate_action_plan_approval_artifact
    )
    validation = validate_split_event_authority_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "split_event_authority_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SplitEventAuthorityCandidateError(
            "split event authority candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise SplitEventAuthorityCandidateError(
            "split event authority candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
