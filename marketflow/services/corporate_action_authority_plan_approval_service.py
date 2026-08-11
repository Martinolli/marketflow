"""Offline approval ceremony for the corporate-action authority plan."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    corporate_action_authority_plan_candidate_operator_review_service as review,
)


ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED"
)
SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_V1 = (
    "corporate_action_authority_plan_approval_v1"
)
CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED = "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED"
CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN = (
    "APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "corporate_action_authority_plan_approval_operator_attestation_v1"
)
REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE CORPORATE ACTION AUTHORITY PLAN MSFT NVDA AMZN GOOGL META TSLA JPM "
    "XOM JNJ WMT CAT LMT CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY"
)

APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY = (
    "APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY"
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "6d0acf97fb36e5302d62c4077ef0dd902a36dc9bf88c7f0234fef07c516bf9c1"
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    review.EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
)
EXPECTED_REVIEW_CHECKLIST_TOTAL = len(review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_PASSED = len(review.REQUIRED_CHECK_IDS)
EXPECTED_REVIEW_CHECKLIST_FAILED = 0
EXPECTED_REVIEW_BLOCKER_COUNT = 0

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
INFO = "INFO"

OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_plan_approval_scope_only",
    "operator_confirms_ready_for_split_event_authority_candidate",
    "operator_confirms_ready_for_dividend_event_authority_candidate",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_validation_rerun",
    "operator_confirms_no_live_provider_transport",
    "operator_confirms_no_corporate_action_authority_created",
    "operator_confirms_no_split_authority_created",
    "operator_confirms_no_dividend_authority_created",
    "operator_confirms_no_acquisition_authority",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_additional_predictive_evidence_execution",
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

REMAINING_ROADMAP_AFTER_PLAN_APPROVAL = [
    "Split event authority candidate.",
    "Dividend event authority candidate.",
    "Combined corporate-action readiness review after split and dividend freeze.",
    "Acquisition generation chain only after corporate-action authority.",
    "Canonical dataset chain only after acquisition generation freeze.",
    "Research registry approval only after canonical dataset freeze.",
]

REQUIRED_APPROVAL_CHECK_IDS = [
    "corporate_action_plan_review_digest_matches_expected",
    "corporate_action_plan_review_has_zero_blockers",
    "corporate_action_plan_candidate_digest_matches_expected",
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
    "target_universe_matches_expected",
    "corporate_action_plan_objective_matches",
    "corporate_action_plan_scope_planning_only",
    "approval_scope_plan_approval_only",
    "corporate_action_authority_creation_status_not_created",
    "per_ticker_corporate_action_plan_approval_entries_12",
    "per_ticker_plan_status_approved_for_future_candidates_only",
    "per_ticker_identity_status_frozen",
    "per_ticker_registry_inventory_approved_for_future_corporate_action_planning",
    "per_ticker_split_event_authority_not_created",
    "per_ticker_dividend_event_authority_not_created",
    "per_ticker_acquisition_precondition_blocked_until_authority",
    "per_ticker_dataset_generation_authorized_false",
    "per_ticker_runtime_use_not_authorized",
    "per_ticker_strategy_use_not_authorized",
    "per_ticker_paper_trading_not_authorized",
    "per_ticker_broker_execution_not_authorized",
    "per_ticker_source_plan_digests_present",
    "per_ticker_source_review_digests_present",
    "per_ticker_approval_digests_present",
    "corporate_action_evidence_requirements_preserved",
    "split_event_authority_chain_preserved",
    "dividend_event_authority_chain_preserved",
    "future_gates_preserved",
    "risk_controls_preserved",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_plan_review_digest_confirmation_matches",
    "operator_plan_candidate_digest_confirmation_matches",
    "operator_registry_inventory_approval_digest_confirmation_matches",
    "operator_identity_freeze_digest_confirmation_matches",
    "operator_target_universe_confirmation_matches",
    "operator_target_count_confirmation_matches",
    "operator_confirms_plan_approval_scope_only",
    "operator_confirms_ready_for_split_event_authority_candidate",
    "operator_confirms_ready_for_dividend_event_authority_candidate",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_validation_rerun",
    "operator_confirms_no_live_provider_transport",
    "operator_confirms_no_corporate_action_authority_created",
    "operator_confirms_no_split_authority_created",
    "operator_confirms_no_dividend_authority_created",
    "operator_confirms_no_acquisition_authority",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_additional_predictive_evidence_execution",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_runtime_activation",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
    "corporate_action_authority_plan_approved_true",
    "ready_for_split_event_authority_candidate_true",
    "ready_for_dividend_event_authority_candidate_true",
    "provider_requests_made_in_approval_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_approval_false",
    "corporate_action_authority_created_false",
    "corporate_action_authority_artifact_created_false",
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
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CorporateActionAuthorityPlanApprovalError(ValueError):
    """Raised when the corporate-action authority plan approval violates guardrails."""


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
        raise CorporateActionAuthorityPlanApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise CorporateActionAuthorityPlanApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise CorporateActionAuthorityPlanApprovalError(f"{field_name} must be false")


def build_corporate_action_authority_plan_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_corporate_action_plan_review_package_digest: str,
    operator_confirms_corporate_action_plan_candidate_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_plan_approval_scope_only: bool,
    operator_confirms_ready_for_split_event_authority_candidate: bool,
    operator_confirms_ready_for_dividend_event_authority_candidate: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_live_validation_rerun: bool,
    operator_confirms_no_live_provider_transport: bool,
    operator_confirms_no_corporate_action_authority_created: bool,
    operator_confirms_no_split_authority_created: bool,
    operator_confirms_no_dividend_authority_created: bool,
    operator_confirms_no_acquisition_authority: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_additional_predictive_evidence_execution: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build a non-secret operator attestation for plan approval only."""
    return {
        "operator_reference": operator_reference,
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_confirms_corporate_action_plan_review_package_digest": (
            operator_confirms_corporate_action_plan_review_package_digest
        ),
        "operator_confirms_corporate_action_plan_candidate_digest": (
            operator_confirms_corporate_action_plan_candidate_digest
        ),
        "operator_confirms_registry_inventory_approval_digest": (
            operator_confirms_registry_inventory_approval_digest
        ),
        "operator_confirms_identity_freeze_digest": operator_confirms_identity_freeze_digest,
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_plan_approval_scope_only": (
            operator_confirms_plan_approval_scope_only
        ),
        "operator_confirms_ready_for_split_event_authority_candidate": (
            operator_confirms_ready_for_split_event_authority_candidate
        ),
        "operator_confirms_ready_for_dividend_event_authority_candidate": (
            operator_confirms_ready_for_dividend_event_authority_candidate
        ),
        "operator_confirms_no_provider_requests_in_approval": (
            operator_confirms_no_provider_requests_in_approval
        ),
        "operator_confirms_no_live_validation_rerun": (
            operator_confirms_no_live_validation_rerun
        ),
        "operator_confirms_no_live_provider_transport": (
            operator_confirms_no_live_provider_transport
        ),
        "operator_confirms_no_corporate_action_authority_created": (
            operator_confirms_no_corporate_action_authority_created
        ),
        "operator_confirms_no_split_authority_created": (
            operator_confirms_no_split_authority_created
        ),
        "operator_confirms_no_dividend_authority_created": (
            operator_confirms_no_dividend_authority_created
        ),
        "operator_confirms_no_acquisition_authority": (
            operator_confirms_no_acquisition_authority
        ),
        "operator_confirms_no_dataset_generation_authorization": (
            operator_confirms_no_dataset_generation_authorization
        ),
        "operator_confirms_no_additional_predictive_evidence_execution": (
            operator_confirms_no_additional_predictive_evidence_execution
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
        "operator_confirms_no_runtime_activation": (
            operator_confirms_no_runtime_activation
        ),
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": (
            operator_confirms_no_broker_execution
        ),
        "operator_confirms_no_trade_recommendations": (
            operator_confirms_no_trade_recommendations
        ),
        "operator_confirms_no_api_key_storage_or_printing": (
            operator_confirms_no_api_key_storage_or_printing
        ),
        "operator_confirms_no_raw_payload_commit": (
            operator_confirms_no_raw_payload_commit
        ),
    }


def _source_review_package(review_package: dict[str, Any] | None) -> dict[str, Any]:
    source_review = (
        deepcopy(review_package)
        if review_package is not None
        else review.build_corporate_action_authority_plan_candidate_review_package_v1()
    )
    try:
        validation = (
            review.validate_corporate_action_authority_plan_candidate_review_package_v1(
                source_review
            )
        )
    except review.CorporateActionAuthorityPlanCandidateReviewPackageError as exc:
        raise CorporateActionAuthorityPlanApprovalError(
            f"source review package invalid: {exc}"
        ) from exc
    _expect(
        validation["corporate_action_authority_plan_candidate_review_package_digest"],
        EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source corporate_action_authority_plan_candidate_review_package_digest",
    )
    _expect(validation["blocker_count"], EXPECTED_REVIEW_BLOCKER_COUNT, "source review blocker_count")
    return source_review


def _review_evidence(source_review: dict[str, Any]) -> dict[str, Any]:
    summary = source_review["review_summary"]
    return {
        "source_corporate_action_plan_review_package_kind": source_review["artifact_kind"],
        "source_corporate_action_plan_review_status": source_review["review_status"],
        "source_corporate_action_plan_review_package_digest": source_review[
            "corporate_action_authority_plan_candidate_review_package_digest"
        ],
        "source_corporate_action_plan_review_checklist_total": summary["total_checks"],
        "source_corporate_action_plan_review_checklist_passed": summary["passed_checks"],
        "source_corporate_action_plan_review_checklist_failed": summary["failed_checks"],
        "source_corporate_action_plan_review_blocker_count": summary["blocker_count"],
        "source_corporate_action_plan_candidate_kind": source_review[
            "reviewed_corporate_action_authority_plan_candidate_kind"
        ],
        "source_corporate_action_plan_candidate_status": source_review[
            "reviewed_corporate_action_authority_plan_candidate_status"
        ],
        "source_corporate_action_plan_candidate_digest": source_review[
            "reviewed_corporate_action_authority_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": source_review[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": source_review[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": source_review[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": source_review["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": source_review[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": source_review[
            "identity_authority_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": source_review[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": source_review[
            "live_ticker_validation_execution_digest"
        ],
        "ticker_universe_selection_approval_digest": source_review[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(source_review["target_universe"]),
        "identity_inventory_universe": list(source_review["identity_inventory_universe"]),
        "target_universe_count": source_review["target_universe_count"],
        "authority_scope": source_review["authority_scope"],
        "corporate_action_authority_plan_objective": source_review[
            "corporate_action_authority_plan_objective"
        ],
        "corporate_action_authority_plan_scope": source_review[
            "corporate_action_authority_plan_scope"
        ],
        "corporate_action_authority_plan_mode": source_review[
            "corporate_action_authority_plan_mode"
        ],
        "corporate_action_authority_creation_status": source_review[
            "corporate_action_authority_creation_status"
        ],
        "plan_scope": list(source_review["plan_scope"]),
        "per_ticker_corporate_action_plan_entries": deepcopy(
            source_review["per_ticker_corporate_action_plan_entries"]
        ),
        "per_ticker_corporate_action_plan_review_entries": deepcopy(
            source_review["per_ticker_corporate_action_plan_review_entries"]
        ),
        "corporate_action_evidence_requirements": list(
            source_review["corporate_action_evidence_requirements"]
        ),
        "corporate_action_evidence_requirement_policy": deepcopy(
            source_review["corporate_action_evidence_requirement_policy"]
        ),
        "future_split_event_authority_chain": list(
            source_review["future_split_event_authority_chain"]
        ),
        "future_dividend_event_authority_chain": list(
            source_review["future_dividend_event_authority_chain"]
        ),
        "future_corporate_action_readiness_chain": list(
            source_review["future_corporate_action_readiness_chain"]
        ),
        "future_gates": list(source_review["future_gates"]),
        "risk_controls": list(source_review["risk_controls"]),
        "planned_outputs": deepcopy(source_review["planned_outputs"]),
        "planned_output_count": source_review["planned_output_count"],
        "planned_outputs_status": source_review["planned_outputs_status"],
        "planned_outputs_label": source_review["planned_outputs_label"],
    }


def _approval_entry_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_corporate_action_plan_approval_digest", None)
    return payload


def per_ticker_corporate_action_plan_approval_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker approval entry."""
    return semantic_digest(_approval_entry_digest_payload(entry))


def _approval_entries(source_review: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in source_review["per_ticker_corporate_action_plan_review_entries"]:
        entry = deepcopy(source)
        entry["source_corporate_action_plan_status"] = entry.pop(
            "corporate_action_plan_status"
        )
        entry["source_corporate_action_plan_review_status"] = entry[
            "corporate_action_plan_review_status"
        ]
        entry["corporate_action_plan_status"] = (
            APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY
        )
        entry["source_per_ticker_corporate_action_plan_digest"] = entry[
            "per_ticker_corporate_action_plan_digest"
        ]
        entry["source_per_ticker_corporate_action_plan_review_digest"] = entry[
            "per_ticker_corporate_action_plan_review_digest"
        ]
        entry["per_ticker_corporate_action_plan_approval_digest"] = (
            per_ticker_corporate_action_plan_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _all_entry_field(entries: list[dict[str, Any]], field_name: str, expected: Any) -> bool:
    return len(entries) == 12 and all(entry.get(field_name) == expected for entry in entries)


def _planned_outputs_not_generated(approved: dict[str, Any]) -> bool:
    outputs = approved.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        item.get("generation_status") == review.plan.PLANNED_NOT_GENERATED
        for item in outputs
    )


def _planned_outputs_research_only(approved: dict[str, Any]) -> bool:
    outputs = approved.get("planned_outputs")
    return isinstance(outputs, list) and bool(outputs) and all(
        item.get("actionability") == review.plan.RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _attestation_checks(attestation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(attestation, dict):
        return [
            _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN, None),
            _check("operator_attestation_phrase_matches", REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE, None),
            _check("operator_plan_review_digest_confirmation_matches", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, None),
            _check("operator_plan_candidate_digest_confirmation_matches", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, None),
            _check("operator_registry_inventory_approval_digest_confirmation_matches", review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, None),
            _check("operator_identity_freeze_digest_confirmation_matches", review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, None),
            _check("operator_target_universe_confirmation_matches", review.VALIDATION_TARGET_UNIVERSE, None),
            _check("operator_target_count_confirmation_matches", 12, None),
            *[_check(field, True, None) for field in OPERATOR_CONFIRMATION_FIELDS],
        ]
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY_PLAN, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_plan_review_digest_confirmation_matches", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, attestation.get("operator_confirms_corporate_action_plan_review_package_digest")),
        _check("operator_plan_candidate_digest_confirmation_matches", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, attestation.get("operator_confirms_corporate_action_plan_candidate_digest")),
        _check("operator_registry_inventory_approval_digest_confirmation_matches", review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, attestation.get("operator_confirms_registry_inventory_approval_digest")),
        _check("operator_identity_freeze_digest_confirmation_matches", review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, attestation.get("operator_confirms_identity_freeze_digest")),
        _check("operator_target_universe_confirmation_matches", review.VALIDATION_TARGET_UNIVERSE, attestation.get("operator_confirms_target_universe")),
        _check("operator_target_count_confirmation_matches", 12, attestation.get("operator_confirms_target_count")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_CONFIRMATION_FIELDS],
    ]


def _validated_operator_attestation(attestation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise CorporateActionAuthorityPlanApprovalError(
            "operator_attestation must be a JSON object"
        )
    for field in (
        "operator_reference",
        "operator_attestation_timestamp_utc",
        "operator_attestation_version",
    ):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise CorporateActionAuthorityPlanApprovalError(
                f"{field} must be a non-empty string"
            )
    failed = [item for item in _attestation_checks(attestation) if item["status"] != PASS]
    if failed:
        raise CorporateActionAuthorityPlanApprovalError(
            f"operator attestation failed: {failed[0]['check_id']}"
        )
    return deepcopy(attestation)


def _approval_checklist(approved: dict[str, Any]) -> list[dict[str, Any]]:
    entries = approved.get("per_ticker_corporate_action_plan_approval_entries")
    entries = entries if isinstance(entries, list) else []
    not_authorized = review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    return [
        _check("corporate_action_plan_review_digest_matches_expected", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("source_corporate_action_plan_review_package_digest")),
        _check("corporate_action_plan_review_has_zero_blockers", EXPECTED_REVIEW_BLOCKER_COUNT, approved.get("source_corporate_action_plan_review_blocker_count")),
        _check("corporate_action_plan_candidate_digest_matches_expected", EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, approved.get("source_corporate_action_plan_candidate_digest")),
        _check("registry_inventory_approval_digest_bound", review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, approved.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("registry_inventory_review_digest_bound", review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, approved.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, approved.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, approved.get("identity_authority_candidate_digest")),
        _check("live_validation_results_review_digest_bound", review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, approved.get("live_ticker_validation_results_review_package_digest")),
        _check("live_validation_execution_digest_bound", review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST, approved.get("live_ticker_validation_execution_digest")),
        _check("ticker_universe_selection_approval_digest_bound", review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, approved.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, approved.get("target_universe_count")),
        _check("target_universe_matches_expected", review.VALIDATION_TARGET_UNIVERSE, approved.get("target_universe")),
        _check("corporate_action_plan_objective_matches", review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE, approved.get("corporate_action_authority_plan_objective")),
        _check("corporate_action_plan_scope_planning_only", review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE, approved.get("corporate_action_authority_plan_scope")),
        _check("approval_scope_plan_approval_only", CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY, approved.get("approval_scope")),
        _check("corporate_action_authority_creation_status_not_created", review.plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS, approved.get("corporate_action_authority_creation_status")),
        _check("per_ticker_corporate_action_plan_approval_entries_12", 12, len(entries)),
        _check("per_ticker_plan_status_approved_for_future_candidates_only", True, _all_entry_field(entries, "corporate_action_plan_status", APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY)),
        _check("per_ticker_identity_status_frozen", True, _all_entry_field(entries, "identity_authority_status", review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN)),
        _check("per_ticker_registry_inventory_approved_for_future_corporate_action_planning", True, _all_entry_field(entries, "registry_inventory_status", review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY)),
        _check("per_ticker_split_event_authority_not_created", True, _all_entry_field(entries, "split_event_authority_status", review.plan.NOT_CREATED)),
        _check("per_ticker_dividend_event_authority_not_created", True, _all_entry_field(entries, "dividend_event_authority_status", review.plan.NOT_CREATED)),
        _check("per_ticker_acquisition_precondition_blocked_until_authority", True, _all_entry_field(entries, "acquisition_precondition_status", review.plan.BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN)),
        _check("per_ticker_dataset_generation_authorized_false", True, _all_entry_field(entries, "dataset_generation_authorized", False)),
        _check("per_ticker_runtime_use_not_authorized", True, _all_entry_field(entries, "runtime_use", not_authorized)),
        _check("per_ticker_strategy_use_not_authorized", True, _all_entry_field(entries, "strategy_use", not_authorized)),
        _check("per_ticker_paper_trading_not_authorized", True, _all_entry_field(entries, "paper_trading", not_authorized)),
        _check("per_ticker_broker_execution_not_authorized", True, _all_entry_field(entries, "broker_execution", not_authorized)),
        _check("per_ticker_source_plan_digests_present", True, _digests_present(entries, "source_per_ticker_corporate_action_plan_digest")),
        _check("per_ticker_source_review_digests_present", True, _digests_present(entries, "source_per_ticker_corporate_action_plan_review_digest")),
        _check("per_ticker_approval_digests_present", True, _digests_present(entries, "per_ticker_corporate_action_plan_approval_digest")),
        _check("corporate_action_evidence_requirements_preserved", review.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS, approved.get("corporate_action_evidence_requirements")),
        _check("split_event_authority_chain_preserved", review.FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN, approved.get("future_split_event_authority_chain")),
        _check("dividend_event_authority_chain_preserved", review.FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN, approved.get("future_dividend_event_authority_chain")),
        _check("future_gates_preserved", review.FUTURE_GATES, approved.get("future_gates")),
        _check("risk_controls_preserved", review.RISK_CONTROLS, approved.get("risk_controls")),
        *_attestation_checks(approved.get("operator_attestation") if isinstance(approved.get("operator_attestation"), dict) else None),
        _check("corporate_action_authority_plan_approved_true", True, approved.get("corporate_action_authority_plan_approved")),
        _check("ready_for_split_event_authority_candidate_true", True, approved.get("ready_for_split_event_authority_candidate")),
        _check("ready_for_dividend_event_authority_candidate_true", True, approved.get("ready_for_dividend_event_authority_candidate")),
        _check("provider_requests_made_in_approval_false", False, approved.get("provider_requests_made_in_approval")),
        _check("live_validation_rerun_performed_false", False, approved.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_approval_false", False, approved.get("live_provider_transport_enabled_in_approval")),
        _check("corporate_action_authority_created_false", False, approved.get("corporate_action_authority_created")),
        _check("corporate_action_authority_artifact_created_false", False, approved.get("corporate_action_authority_artifact_created")),
        _check("split_event_authority_candidate_created_false", False, approved.get("split_event_authority_candidate_created")),
        _check("split_event_authority_created_false", False, approved.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, approved.get("split_event_authority_frozen")),
        _check("dividend_event_authority_candidate_created_false", False, approved.get("dividend_event_authority_candidate_created")),
        _check("dividend_event_authority_created_false", False, approved.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, approved.get("dividend_event_authority_frozen")),
        _check("new_ticker_acquisition_authorized_false", False, approved.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, approved.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, approved.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, approved.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, approved.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, approved.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, approved.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, approved.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, approved.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, approved.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, approved.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, approved.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, approved.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, approved.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved.get("predictive_usefulness"), severity=INFO),
        _check("predictive_usefulness_acceptance_ready_false", False, approved.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, approved.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, approved.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved.get("profitability"), severity=INFO),
        _check("profitability_acceptance_ready_false", False, approved.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, approved.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, approved.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, approved.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", not_authorized, approved.get("runtime_use")),
        _check("strategy_use_not_authorized", not_authorized, approved.get("strategy_use")),
        _check("paper_trading_not_authorized", not_authorized, approved.get("paper_trading")),
        _check("broker_execution_not_authorized", not_authorized, approved.get("broker_execution")),
        _check("automatic_stitching_false", False, approved.get("automatic_stitching")),
        _check("no_acquisition_authorization_created", False, approved.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, approved.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, approved.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, approved.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, approved.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blockers = [item for item in failed if item["severity"] == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "corporate_action_authority_plan_approved_by_operator": not failed,
        "approval_scope": CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "ready_for_split_event_authority_candidate": not failed,
        "ready_for_dividend_event_authority_candidate": not failed,
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


def _digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("corporate_action_authority_plan_approval_digest", None)
    return payload


def corporate_action_authority_plan_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the plan approval artifact."""
    return semantic_digest(_digest_payload(approved_artifact))


def build_corporate_action_authority_plan_approved_v1(
    *,
    corporate_action_plan_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline approval artifact for plan approval only."""
    source_review = _source_review_package(corporate_action_plan_review_package)
    attestation = _validated_operator_attestation(operator_attestation)
    not_authorized = review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    approved = {
        "artifact_kind": ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "schema_version": SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_V1,
        "approval_status": CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "approval_scope": CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "corporate_action_authority_plan_approved": True,
        "ready_for_split_event_authority_candidate": True,
        "ready_for_dividend_event_authority_candidate": True,
        "research_only": True,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_approval": False,
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
        "operator_attestation": attestation,
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_PLAN_APPROVAL),
        **_review_evidence(source_review),
    }
    approved["per_ticker_corporate_action_plan_approval_entries"] = (
        _approval_entries(source_review)
    )
    checklist = _approval_checklist(approved)
    approved["approval_checklist"] = checklist
    approved["approval_summary"] = _summary(checklist)
    approved["corporate_action_authority_plan_approval_digest"] = (
        corporate_action_authority_plan_approval_digest_v1(approved)
    )
    validate_corporate_action_authority_plan_approved_v1(approved)
    return approved


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "approved_artifact") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "CORPORATE_ACTION_AUTHORITY_CREATED",
            "SPLIT_EVENT_AUTHORITY_CREATED",
            "DIVIDEND_EVENT_AUTHORITY_CREATED",
            "ACQUISITION_GENERATION_AUTHORIZED",
            "DATASET_GENERATION_AUTHORIZED",
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise CorporateActionAuthorityPlanApprovalError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made_in_approval",
            "live_validation_rerun_performed",
            "live_provider_transport_enabled_in_approval",
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
            "generated",
            "execution_performed",
            "output_generated",
        } and value is True:
            raise CorporateActionAuthorityPlanApprovalError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise CorporateActionAuthorityPlanApprovalError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise CorporateActionAuthorityPlanApprovalError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_approval_entries(approved_artifact: dict[str, Any]) -> None:
    entries = approved_artifact.get("per_ticker_corporate_action_plan_approval_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CorporateActionAuthorityPlanApprovalError(
            "per_ticker_corporate_action_plan_approval_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        review.VALIDATION_TARGET_UNIVERSE,
        "per_ticker_corporate_action_plan_approval_entries tickers",
    )
    not_authorized = review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_authority_status"),
            review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            f"{ticker}.identity_authority_status",
        )
        _expect(
            entry.get("registry_inventory_status"),
            review.plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            f"{ticker}.registry_inventory_status",
        )
        _expect(
            entry.get("source_corporate_action_plan_status"),
            review.plan.PLANNED_NOT_CREATED,
            f"{ticker}.source_corporate_action_plan_status",
        )
        _expect(
            entry.get("source_corporate_action_plan_review_status"),
            review.READY_FOR_OPERATOR_ASSESSMENT,
            f"{ticker}.source_corporate_action_plan_review_status",
        )
        _expect(
            entry.get("corporate_action_plan_status"),
            APPROVED_FOR_FUTURE_SPLIT_AND_DIVIDEND_AUTHORITY_CANDIDATES_ONLY,
            f"{ticker}.corporate_action_plan_status",
        )
        _expect(entry.get("split_event_authority_status"), review.plan.NOT_CREATED, f"{ticker}.split_event_authority_status")
        _expect(entry.get("dividend_event_authority_status"), review.plan.NOT_CREATED, f"{ticker}.dividend_event_authority_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect(entry.get("acquisition_precondition_status"), review.plan.BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN, f"{ticker}.acquisition_precondition_status")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), not_authorized, f"{ticker}.{field}")
        for field in (
            "source_identity_freeze_digest",
            "source_registry_inventory_approval_digest",
            "source_per_ticker_registry_inventory_approval_digest_if_available",
            "per_ticker_corporate_action_plan_digest",
            "per_ticker_corporate_action_plan_review_digest",
            "source_per_ticker_corporate_action_plan_digest",
            "source_per_ticker_corporate_action_plan_review_digest",
            "per_ticker_corporate_action_plan_approval_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise CorporateActionAuthorityPlanApprovalError(f"{field} missing")
        _expect(
            entry["source_per_ticker_corporate_action_plan_digest"],
            entry["per_ticker_corporate_action_plan_digest"],
            f"{ticker}.source_per_ticker_corporate_action_plan_digest",
        )
        _expect(
            entry["source_per_ticker_corporate_action_plan_review_digest"],
            entry["per_ticker_corporate_action_plan_review_digest"],
            f"{ticker}.source_per_ticker_corporate_action_plan_review_digest",
        )
        _expect(
            entry["per_ticker_corporate_action_plan_approval_digest"],
            per_ticker_corporate_action_plan_approval_digest_v1(entry),
            f"{ticker}.per_ticker_corporate_action_plan_approval_digest",
        )


def validate_corporate_action_authority_plan_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate plan approval while preserving every downstream guardrail."""
    if not isinstance(approved_artifact, dict):
        raise CorporateActionAuthorityPlanApprovalError(
            "approved artifact must be a JSON object"
        )
    _reject_forbidden_values(approved_artifact)
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED,
        "approval_status",
    )
    for field in (
        "corporate_action_authority_plan_approved",
        "ready_for_split_event_authority_candidate",
        "ready_for_dividend_event_authority_candidate",
        "research_only",
        "created_offline",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_approval",
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
        _expect_false(approved_artifact.get(field), field)
    not_authorized = review.plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), not_authorized, field)
    for field, expected in {
        "approval_scope": CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY,
        "source_corporate_action_plan_review_package_kind": review.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "source_corporate_action_plan_review_status": review.CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "source_corporate_action_plan_review_package_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source_corporate_action_plan_review_checklist_total": EXPECTED_REVIEW_CHECKLIST_TOTAL,
        "source_corporate_action_plan_review_checklist_passed": EXPECTED_REVIEW_CHECKLIST_PASSED,
        "source_corporate_action_plan_review_checklist_failed": EXPECTED_REVIEW_CHECKLIST_FAILED,
        "source_corporate_action_plan_review_blocker_count": EXPECTED_REVIEW_BLOCKER_COUNT,
        "source_corporate_action_plan_candidate_kind": review.plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE,
        "source_corporate_action_plan_candidate_status": review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW,
        "source_corporate_action_plan_candidate_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": review.plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_digest": review.plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST,
        "identity_authority_freeze_digest": review.plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "ticker_universe_selection_approval_digest": review.plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": review.VALIDATION_TARGET_UNIVERSE,
        "identity_inventory_universe": review.VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": review.plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "corporate_action_authority_plan_objective": review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE,
        "corporate_action_authority_plan_scope": review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE,
        "corporate_action_authority_plan_mode": review.plan.CORPORATE_ACTION_AUTHORITY_PLAN_MODE,
        "corporate_action_authority_creation_status": review.plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS,
        "plan_scope": review.plan.PLAN_SCOPE,
        "corporate_action_evidence_requirements": review.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS,
        "corporate_action_evidence_requirement_policy": review.CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY,
        "future_split_event_authority_chain": review.FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN,
        "future_dividend_event_authority_chain": review.FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN,
        "future_corporate_action_readiness_chain": review.FUTURE_CORPORATE_ACTION_READINESS_CHAIN,
        "future_gates": review.FUTURE_GATES,
        "risk_controls": review.RISK_CONTROLS,
        "planned_output_count": 9,
        "planned_outputs_status": review.plan.PLANNED_NOT_GENERATED,
        "planned_outputs_label": review.plan.RESEARCH_ONLY_NON_ACTIONABLE,
        "remaining_roadmap": REMAINING_ROADMAP_AFTER_PLAN_APPROVAL,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    if approved_artifact.get("target_universe") != approved_artifact.get("identity_inventory_universe"):
        raise CorporateActionAuthorityPlanApprovalError(
            "target universe differs from identity inventory universe"
        )
    if not _planned_outputs_not_generated(approved_artifact):
        raise CorporateActionAuthorityPlanApprovalError("planned_outputs must not be generated")
    if not _planned_outputs_research_only(approved_artifact):
        raise CorporateActionAuthorityPlanApprovalError("planned_outputs must be research only")
    _validate_approval_entries(approved_artifact)
    _validated_operator_attestation(approved_artifact.get("operator_attestation"))
    checklist = _approval_checklist(approved_artifact)
    _expect([item["check_id"] for item in checklist], REQUIRED_APPROVAL_CHECK_IDS, "approval_checklist check IDs")
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise CorporateActionAuthorityPlanApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(approved_artifact.get("approval_checklist"), checklist, "approval_checklist")
    summary = _summary(checklist)
    _expect(approved_artifact.get("approval_summary"), summary, "approval_summary")
    _expect_true(
        summary.get("corporate_action_authority_plan_approved_by_operator"),
        "corporate_action_authority_plan_approved_by_operator",
    )
    _expect_true(
        summary.get("ready_for_split_event_authority_candidate"),
        "ready_for_split_event_authority_candidate",
    )
    _expect_true(
        summary.get("ready_for_dividend_event_authority_candidate"),
        "ready_for_dividend_event_authority_candidate",
    )
    for field in (
        "corporate_action_authority_authorized",
        "split_event_authority_authorized",
        "dividend_event_authority_authorized",
        "acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "predictive_usefulness_accepted",
        "profitability_accepted",
        "runtime_migration_authorized",
        "software_runtime_activation_authorized",
    ):
        _expect_false(summary.get(field), field)
    digest = approved_artifact.get("corporate_action_authority_plan_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise CorporateActionAuthorityPlanApprovalError(
            "corporate_action_authority_plan_approval_digest missing"
        )
    _expect(
        digest,
        corporate_action_authority_plan_approval_digest_v1(approved_artifact),
        "corporate_action_authority_plan_approval_digest",
    )
    return {
        "status": "CORPORATE_ACTION_AUTHORITY_PLAN_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "corporate_action_authority_plan_approval_digest": digest,
        "source_corporate_action_plan_review_package_digest": (
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "source_corporate_action_plan_candidate_digest": (
            EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "post_identity_freeze_registry_inventory_approval_digest": approved_artifact[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": approved_artifact[
            "identity_authority_freeze_digest"
        ],
        "target_universe_count": approved_artifact["target_universe_count"],
        "per_ticker_corporate_action_plan_approval_entry_count": len(
            approved_artifact["per_ticker_corporate_action_plan_approval_entries"]
        ),
        "corporate_action_authority_plan_approved": True,
        "ready_for_split_event_authority_candidate": True,
        "ready_for_dividend_event_authority_candidate": True,
        "corporate_action_authority_created": False,
        "split_event_authority_created": False,
        "dividend_event_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": not_authorized,
        "strategy_use": not_authorized,
        "paper_trading": not_authorized,
        "broker_execution": not_authorized,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
    }


def build_corporate_action_authority_plan_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized corporate-action authority plan approval status document."""
    validation = validate_corporate_action_authority_plan_approved_v1(approved_artifact)
    attestation = approved_artifact["operator_attestation"]
    summary = approved_artifact["approval_summary"]
    lines = [
        "# MarketFlow Corporate-Action Authority Plan Approval Status",
        "",
        "## Title",
        "- Corporate-Action Authority Plan Approval Ceremony v1.",
        "",
        "## Approved Plan Scope",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Corporate-action authority plan approved: `{approved_artifact['corporate_action_authority_plan_approved']}`",
        f"- Ready for split event authority candidate: `{approved_artifact['ready_for_split_event_authority_candidate']}`",
        f"- Ready for dividend event authority candidate: `{approved_artifact['ready_for_dividend_event_authority_candidate']}`",
        f"- Approval digest: `{validation['corporate_action_authority_plan_approval_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        "",
        "## Source Review Package",
        f"- Review package kind: `{approved_artifact['source_corporate_action_plan_review_package_kind']}`",
        f"- Review status: `{approved_artifact['source_corporate_action_plan_review_status']}`",
        f"- Review package digest: `{approved_artifact['source_corporate_action_plan_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['source_corporate_action_plan_candidate_digest']}`",
        f"- Review blockers: `{approved_artifact['source_corporate_action_plan_review_blocker_count']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{approved_artifact['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in approved_artifact["target_universe"]),
        "",
        "## Source Evidence Digests",
        f"- Registry inventory approval digest: `{approved_artifact['post_identity_freeze_registry_inventory_approval_digest']}`",
        f"- Registry inventory review package digest: `{approved_artifact['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        f"- Registry inventory candidate digest: `{approved_artifact['post_identity_freeze_registry_inventory_candidate_digest']}`",
        f"- Identity freeze digest: `{approved_artifact['identity_authority_freeze_digest']}`",
        f"- Identity candidate review package digest: `{approved_artifact['identity_authority_candidate_review_package_digest']}`",
        f"- Identity candidate digest: `{approved_artifact['identity_authority_candidate_digest']}`",
        f"- Live validation results review package digest: `{approved_artifact['live_ticker_validation_results_review_package_digest']}`",
        f"- Live validation execution digest: `{approved_artifact['live_ticker_validation_execution_digest']}`",
        f"- Ticker universe selection approval digest: `{approved_artifact['ticker_universe_selection_approval_digest']}`",
        "",
        "## Approval Boundary",
        f"- provider_requests_made_in_approval: `{approved_artifact['provider_requests_made_in_approval']}`",
        f"- live_validation_rerun_performed: `{approved_artifact['live_validation_rerun_performed']}`",
        f"- live_provider_transport_enabled_in_approval: `{approved_artifact['live_provider_transport_enabled_in_approval']}`",
        f"- corporate_action_authority_created: `{approved_artifact['corporate_action_authority_created']}`",
        f"- split_event_authority_candidate_created: `{approved_artifact['split_event_authority_candidate_created']}`",
        f"- dividend_event_authority_candidate_created: `{approved_artifact['dividend_event_authority_candidate_created']}`",
        f"- new_ticker_acquisition_authorized: `{approved_artifact['new_ticker_acquisition_authorized']}`",
        f"- dataset_generation_authorized: `{approved_artifact['dataset_generation_authorized']}`",
        "",
        "## Runtime And Research Boundary",
        f"- runtime_migration_approved: `{approved_artifact['runtime_migration_approved']}`",
        f"- runtime_migration_active: `{approved_artifact['runtime_migration_active']}`",
        f"- strategy_runtime_migration: `{approved_artifact['strategy_runtime_migration']}`",
        f"- runtime_use: `{approved_artifact['runtime_use']}`",
        f"- strategy_use: `{approved_artifact['strategy_use']}`",
        f"- paper_trading: `{approved_artifact['paper_trading']}`",
        f"- broker_execution: `{approved_artifact['broker_execution']}`",
        f"- trade_recommendations_generated: `{approved_artifact['trade_recommendations_generated']}`",
        f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
        f"- profitability: `{approved_artifact['profitability']}`",
        "",
        "## Per-Ticker Approval Summary",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['corporate_action_plan_status']}`, approval digest `{entry['per_ticker_corporate_action_plan_approval_digest']}`"
        for entry in approved_artifact["per_ticker_corporate_action_plan_approval_entries"]
    )
    lines.extend(
        [
            "",
            "## Approval Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Corporate-action authority plan approved by operator: `{summary['corporate_action_authority_plan_approved_by_operator']}`",
            f"- Ready for split event authority candidate: `{summary['ready_for_split_event_authority_candidate']}`",
            f"- Ready for dividend event authority candidate: `{summary['ready_for_dividend_event_authority_candidate']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(approved_artifact["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Approval scope is `CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_ONLY`.",
            "- No corporate-action authority, split authority, or dividend authority was created.",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition or dataset generation authorization was created.",
            "- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_corporate_action_authority_plan_approved_v1(
    output_dir: str | Path,
    *,
    corporate_action_plan_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the plan approval JSON artifact without overwriting output."""
    approved = build_corporate_action_authority_plan_approved_v1(
        corporate_action_plan_review_package=corporate_action_plan_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_corporate_action_authority_plan_approved_v1(approved)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "corporate_action_authority_plan_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise CorporateActionAuthorityPlanApprovalError(
            "corporate-action authority plan approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise CorporateActionAuthorityPlanApprovalError(
            "corporate-action authority plan approval output already exists"
        )
    payload = canonical_json_bytes(approved)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
