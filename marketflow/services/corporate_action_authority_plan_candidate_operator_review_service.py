"""Offline operator review package for the corporate-action authority plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import corporate_action_authority_plan_candidate_service as plan


ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1 = (
    "corporate_action_authority_plan_candidate_review_v1"
)
CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING"
)
CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING = (
    "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    "3ab988e647eebf01ea489dd3e9da2a1edf7b9c8a50b26a54995d39cc3115753a"
)
EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_TOTAL = 79
EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_PASSED = 79
EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_BLOCKER_COUNT = 0

READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(plan.VALIDATION_TARGET_UNIVERSE)
CORPORATE_ACTION_EVIDENCE_REQUIREMENTS = list(
    plan.CORPORATE_ACTION_EVIDENCE_REQUIREMENTS
)
CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY = deepcopy(
    plan.CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY
)
FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN = list(plan.FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN)
FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN = list(plan.FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN)
FUTURE_CORPORATE_ACTION_READINESS_CHAIN = list(
    plan.FUTURE_CORPORATE_ACTION_READINESS_CHAIN
)
FUTURE_GATES = list(plan.FUTURE_GATES)
RISK_CONTROLS = list(plan.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "corporate_action_plan_candidate_kind_matches",
    "corporate_action_plan_candidate_status_ready_for_review",
    "corporate_action_plan_candidate_digest_matches",
    "corporate_action_plan_candidate_checklist_zero_blockers",
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
    "target_universe_matches_identity_inventory_universe",
    "identity_authority_frozen_true",
    "registry_inventory_approved_true",
    "corporate_action_plan_objective_reviewed",
    "corporate_action_plan_scope_planning_only",
    "corporate_action_plan_mode_candidate_only_not_authority",
    "corporate_action_authority_creation_status_not_created",
    "plan_scope_reviewed",
    "per_ticker_corporate_action_plan_entries_12",
    "per_ticker_corporate_action_plan_review_entries_12",
    "per_ticker_identity_status_frozen",
    "per_ticker_registry_inventory_approved_for_future_corporate_action_planning",
    "per_ticker_split_event_authority_not_created",
    "per_ticker_dividend_event_authority_not_created",
    "per_ticker_corporate_action_plan_digests_present",
    "per_ticker_corporate_action_plan_review_digests_present",
    "corporate_action_evidence_requirements_reviewed",
    "corporate_action_evidence_requirements_not_fetched",
    "split_event_authority_chain_reviewed",
    "dividend_event_authority_chain_reviewed",
    "corporate_action_readiness_chain_reviewed",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_9",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "corporate_action_authority_plan_approved_false",
    "corporate_action_authority_created_false",
    "split_event_authority_candidate_created_false",
    "split_event_authority_review_created_false",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "dividend_event_authority_candidate_created_false",
    "dividend_event_authority_review_created_false",
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


class CorporateActionAuthorityPlanCandidateReviewPackageError(ValueError):
    """Raised when the corporate-action authority plan review package is invalid."""


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
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            plan.build_corporate_action_authority_plan_candidate_v1(),
            CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING,
        )
    plan.validate_corporate_action_authority_plan_candidate_v1(candidate)
    return deepcopy(candidate), CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_corporate_action_plan_review_digest", None)
    return payload


def per_ticker_corporate_action_plan_review_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one per-ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in candidate.get("per_ticker_corporate_action_plan_entries", []):
        entry = deepcopy(source)
        entry["corporate_action_plan_review_status"] = READY_FOR_OPERATOR_ASSESSMENT
        entry["per_ticker_corporate_action_plan_review_digest"] = (
            per_ticker_corporate_action_plan_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _plan_entry_from_review_entry(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("corporate_action_plan_review_status", None)
    payload.pop("per_ticker_corporate_action_plan_review_digest", None)
    return payload


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["plan_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1,
        "review_status": CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "corporate_action_authority_plan_candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "corporate_action_authority_plan_candidate_created": True,
        "corporate_action_authority_plan_review_created": True,
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
        "authority_scope": candidate["authority_scope"],
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
        "runtime_use": candidate["runtime_use"],
        "strategy_use": candidate["strategy_use"],
        "paper_trading": candidate["paper_trading"],
        "broker_execution": candidate["broker_execution"],
        "automatic_stitching": False,
        "operator_review_required": True,
        "reviewed_corporate_action_authority_plan_candidate_kind": candidate[
            "artifact_kind"
        ],
        "reviewed_corporate_action_authority_plan_candidate_status": candidate[
            "candidate_status"
        ],
        "reviewed_corporate_action_authority_plan_candidate_digest": candidate[
            "corporate_action_authority_plan_candidate_digest"
        ],
        "reviewed_corporate_action_authority_plan_candidate_checklist_total": summary[
            "total_checks"
        ],
        "reviewed_corporate_action_authority_plan_candidate_checklist_passed": summary[
            "passed_checks"
        ],
        "reviewed_corporate_action_authority_plan_candidate_checklist_failed": summary[
            "failed_checks"
        ],
        "reviewed_corporate_action_authority_plan_candidate_blocker_count": summary[
            "blocker_count"
        ],
        "corporate_action_authority_plan_candidate_digest": candidate[
            "corporate_action_authority_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": candidate[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": candidate[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": candidate["identity_authority_candidate_digest"],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": candidate[
            "live_ticker_validation_execution_digest"
        ],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "identity_inventory_universe": list(candidate["identity_inventory_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "corporate_action_authority_plan_objective": candidate[
            "corporate_action_authority_plan_objective"
        ],
        "corporate_action_authority_plan_scope": candidate[
            "corporate_action_authority_plan_scope"
        ],
        "corporate_action_authority_plan_mode": candidate[
            "corporate_action_authority_plan_mode"
        ],
        "corporate_action_authority_creation_status": candidate[
            "corporate_action_authority_creation_status"
        ],
        "plan_scope": list(candidate["plan_scope"]),
        "per_ticker_corporate_action_plan_entries": deepcopy(
            candidate["per_ticker_corporate_action_plan_entries"]
        ),
        "per_ticker_corporate_action_plan_review_entries": _review_entries(candidate),
        "corporate_action_evidence_requirements": list(
            candidate["corporate_action_evidence_requirements"]
        ),
        "corporate_action_evidence_requirement_policy": deepcopy(
            candidate["corporate_action_evidence_requirement_policy"]
        ),
        "future_split_event_authority_chain": list(
            candidate["future_split_event_authority_chain"]
        ),
        "future_dividend_event_authority_chain": list(
            candidate["future_dividend_event_authority_chain"]
        ),
        "future_corporate_action_readiness_chain": list(
            candidate["future_corporate_action_readiness_chain"]
        ),
        "future_gates": list(candidate["future_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": plan.PLANNED_NOT_GENERATED,
        "planned_outputs_label": plan.RESEARCH_ONLY_NON_ACTIONABLE,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_corporate_action_plan_entries")
    return entries if isinstance(entries, list) else []


def _review_entries_from_package(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_corporate_action_plan_review_entries")
    return entries if isinstance(entries, list) else []


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _all_entry_field(entries: list[dict[str, Any]], field: str, expected: Any) -> bool:
    return len(entries) == 12 and all(entry.get(field) == expected for entry in entries)


def _planned_outputs_not_generated(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and all(
        item.get("generation_status") == plan.PLANNED_NOT_GENERATED for item in outputs
    )


def _planned_outputs_research_only(review_package: dict[str, Any]) -> bool:
    outputs = review_package.get("planned_outputs")
    return isinstance(outputs, list) and all(
        item.get("actionability") == plan.RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    not_authorized = plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    return [
        _check("corporate_action_plan_candidate_kind_matches", plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE, review_package.get("reviewed_corporate_action_authority_plan_candidate_kind")),
        _check("corporate_action_plan_candidate_status_ready_for_review", plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_corporate_action_authority_plan_candidate_status")),
        _check("corporate_action_plan_candidate_digest_matches", EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST, review_package.get("reviewed_corporate_action_authority_plan_candidate_digest")),
        _check("corporate_action_plan_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_corporate_action_authority_plan_candidate_blocker_count")),
        _check("registry_inventory_approval_digest_bound", plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, review_package.get("post_identity_freeze_registry_inventory_approval_digest")),
        _check("registry_inventory_review_digest_bound", plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, review_package.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, review_package.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, review_package.get("identity_authority_candidate_digest")),
        _check("live_validation_results_review_digest_bound", plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("live_ticker_validation_results_review_package_digest")),
        _check("live_validation_execution_digest_bound", plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST, review_package.get("live_ticker_validation_execution_digest")),
        _check("ticker_universe_selection_approval_digest_bound", plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, review_package.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check("target_universe_matches_identity_inventory_universe", True, review_package.get("target_universe") == review_package.get("identity_inventory_universe") == VALIDATION_TARGET_UNIVERSE),
        _check("identity_authority_frozen_true", True, review_package.get("identity_authority_frozen")),
        _check("registry_inventory_approved_true", True, review_package.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_plan_objective_reviewed", plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE, review_package.get("corporate_action_authority_plan_objective")),
        _check("corporate_action_plan_scope_planning_only", plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE, review_package.get("corporate_action_authority_plan_scope")),
        _check("corporate_action_plan_mode_candidate_only_not_authority", plan.CORPORATE_ACTION_AUTHORITY_PLAN_MODE, review_package.get("corporate_action_authority_plan_mode")),
        _check("corporate_action_authority_creation_status_not_created", plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS, review_package.get("corporate_action_authority_creation_status")),
        _check("plan_scope_reviewed", plan.PLAN_SCOPE, review_package.get("plan_scope")),
        _check("per_ticker_corporate_action_plan_entries_12", 12, len(entries)),
        _check("per_ticker_corporate_action_plan_review_entries_12", 12, len(review_entries)),
        _check("per_ticker_identity_status_frozen", True, _all_entry_field(review_entries, "identity_authority_status", plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN)),
        _check("per_ticker_registry_inventory_approved_for_future_corporate_action_planning", True, _all_entry_field(review_entries, "registry_inventory_status", plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY)),
        _check("per_ticker_split_event_authority_not_created", True, _all_entry_field(review_entries, "split_event_authority_status", plan.NOT_CREATED)),
        _check("per_ticker_dividend_event_authority_not_created", True, _all_entry_field(review_entries, "dividend_event_authority_status", plan.NOT_CREATED)),
        _check("per_ticker_corporate_action_plan_digests_present", True, _digests_present(review_entries, "per_ticker_corporate_action_plan_digest")),
        _check("per_ticker_corporate_action_plan_review_digests_present", True, _digests_present(review_entries, "per_ticker_corporate_action_plan_review_digest")),
        _check("corporate_action_evidence_requirements_reviewed", CORPORATE_ACTION_EVIDENCE_REQUIREMENTS, review_package.get("corporate_action_evidence_requirements")),
        _check("corporate_action_evidence_requirements_not_fetched", plan.CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY, review_package.get("corporate_action_evidence_requirement_policy")),
        _check("split_event_authority_chain_reviewed", FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN, review_package.get("future_split_event_authority_chain")),
        _check("dividend_event_authority_chain_reviewed", FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN, review_package.get("future_dividend_event_authority_chain")),
        _check("corporate_action_readiness_chain_reviewed", FUTURE_CORPORATE_ACTION_READINESS_CHAIN, review_package.get("future_corporate_action_readiness_chain")),
        _check("future_gates_defined", FUTURE_GATES, review_package.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review_package.get("risk_controls")),
        _check("planned_outputs_9", 9, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", True, _planned_outputs_not_generated(review_package)),
        _check("planned_outputs_research_only", True, _planned_outputs_research_only(review_package)),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, review_package.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_review_false", False, review_package.get("live_provider_transport_enabled_in_review")),
        _check("corporate_action_authority_plan_approved_false", False, review_package.get("corporate_action_authority_plan_approved")),
        _check("corporate_action_authority_created_false", False, review_package.get("corporate_action_authority_created")),
        _check("split_event_authority_candidate_created_false", False, review_package.get("split_event_authority_candidate_created")),
        _check("split_event_authority_review_created_false", False, review_package.get("split_event_authority_review_created")),
        _check("split_event_authority_created_false", False, review_package.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, review_package.get("split_event_authority_frozen")),
        _check("dividend_event_authority_candidate_created_false", False, review_package.get("dividend_event_authority_candidate_created")),
        _check("dividend_event_authority_review_created_false", False, review_package.get("dividend_event_authority_review_created")),
        _check("dividend_event_authority_created_false", False, review_package.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, review_package.get("dividend_event_authority_frozen")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, review_package.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, review_package.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, review_package.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, review_package.get("registry_approval_created")),
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
        _check("runtime_use_not_authorized", not_authorized, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", not_authorized, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", not_authorized, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", not_authorized, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, review_package.get("corporate_action_authority_artifact_created")),
        _check("no_split_event_authority_artifact_created", False, review_package.get("split_event_authority_artifact_created")),
        _check("no_dividend_event_authority_artifact_created", False, review_package.get("dividend_event_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, review_package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blockers = [item for item in failed if item["severity"] == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_assessment": not failed,
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


def _review_package_digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("corporate_action_authority_plan_candidate_review_package_digest", None)
    return payload


def corporate_action_authority_plan_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_review_package_digest_payload(review_package))


def build_corporate_action_authority_plan_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline corporate-action authority plan candidate review package."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["corporate_action_authority_plan_candidate_review_package_digest"] = (
        corporate_action_authority_plan_candidate_review_package_digest_v1(review_package)
    )
    validate_corporate_action_authority_plan_candidate_review_package_v1(review_package)
    return review_package


def _validate_review_entries(review_package: dict[str, Any]) -> None:
    entries = _review_entries_from_package(review_package)
    if len(entries) != 12:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "per_ticker_corporate_action_plan_review_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_corporate_action_plan_review_entries tickers",
    )
    not_authorized = plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_authority_status"),
            plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            f"{ticker}.identity_authority_status",
        )
        _expect(
            entry.get("registry_inventory_status"),
            plan.approval_service.APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            f"{ticker}.registry_inventory_status",
        )
        _expect(entry.get("corporate_action_plan_status"), plan.PLANNED_NOT_CREATED, f"{ticker}.corporate_action_plan_status")
        _expect(entry.get("corporate_action_plan_review_status"), READY_FOR_OPERATOR_ASSESSMENT, f"{ticker}.corporate_action_plan_review_status")
        _expect(entry.get("split_event_authority_status"), plan.NOT_CREATED, f"{ticker}.split_event_authority_status")
        _expect(entry.get("dividend_event_authority_status"), plan.NOT_CREATED, f"{ticker}.dividend_event_authority_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect(entry.get("acquisition_precondition_status"), plan.BLOCKED_UNTIL_CORPORATE_ACTION_AUTHORITY_FROZEN, f"{ticker}.acquisition_precondition_status")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), not_authorized, f"{ticker}.{field}")
        for field in (
            "source_identity_freeze_digest",
            "source_registry_inventory_approval_digest",
            "source_per_ticker_registry_inventory_approval_digest_if_available",
            "per_ticker_corporate_action_plan_digest",
            "per_ticker_corporate_action_plan_review_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise CorporateActionAuthorityPlanCandidateReviewPackageError(
                    f"{field} missing"
                )
        _expect(
            entry["per_ticker_corporate_action_plan_digest"],
            plan.per_ticker_corporate_action_plan_digest_v1(
                _plan_entry_from_review_entry(entry)
            ),
            f"{ticker}.per_ticker_corporate_action_plan_digest",
        )
        _expect(
            entry["per_ticker_corporate_action_plan_review_digest"],
            per_ticker_corporate_action_plan_review_digest_v1(entry),
            f"{ticker}.per_ticker_corporate_action_plan_review_digest",
        )


def validate_corporate_action_authority_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the corporate-action authority plan candidate review package."""
    if not isinstance(review_package, dict):
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    if review_package.get("corporate_action_authority_plan_candidate_binding_mode") not in {
        CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING,
        CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING,
    }:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "corporate_action_authority_plan_candidate_binding_mode mismatch"
        )
    for field in (
        "created_offline",
        "corporate_action_authority_plan_candidate_created",
        "corporate_action_authority_plan_review_created",
        "post_identity_freeze_registry_inventory_approved",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
        _expect_false(review_package.get(field), field)
    not_authorized = plan.approval_service.review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), not_authorized, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_corporate_action_authority_plan_candidate_kind": plan.ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE,
        "reviewed_corporate_action_authority_plan_candidate_status": plan.CORPORATE_ACTION_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW,
        "reviewed_corporate_action_authority_plan_candidate_digest": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "reviewed_corporate_action_authority_plan_candidate_checklist_total": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_corporate_action_authority_plan_candidate_checklist_passed": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_corporate_action_authority_plan_candidate_checklist_failed": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_corporate_action_authority_plan_candidate_blocker_count": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_BLOCKER_COUNT,
        "corporate_action_authority_plan_candidate_digest": EXPECTED_REVIEWED_CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": plan.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "post_identity_freeze_registry_inventory_candidate_digest": plan.approval_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST,
        "identity_authority_freeze_digest": plan.approval_service.review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "ticker_universe_selection_approval_digest": plan.approval_service.review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "identity_inventory_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": plan.approval_service.review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "corporate_action_authority_plan_objective": plan.CORPORATE_ACTION_AUTHORITY_PLAN_OBJECTIVE,
        "corporate_action_authority_plan_scope": plan.CORPORATE_ACTION_AUTHORITY_PLAN_SCOPE,
        "corporate_action_authority_plan_mode": plan.CORPORATE_ACTION_AUTHORITY_PLAN_MODE,
        "corporate_action_authority_creation_status": plan.CORPORATE_ACTION_AUTHORITY_CREATION_STATUS,
        "plan_scope": plan.PLAN_SCOPE,
        "corporate_action_evidence_requirements": CORPORATE_ACTION_EVIDENCE_REQUIREMENTS,
        "corporate_action_evidence_requirement_policy": CORPORATE_ACTION_EVIDENCE_REQUIREMENT_POLICY,
        "future_split_event_authority_chain": FUTURE_SPLIT_EVENT_AUTHORITY_CHAIN,
        "future_dividend_event_authority_chain": FUTURE_DIVIDEND_EVENT_AUTHORITY_CHAIN,
        "future_corporate_action_readiness_chain": FUTURE_CORPORATE_ACTION_READINESS_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_output_count": 9,
        "planned_outputs_status": plan.PLANNED_NOT_GENERATED,
        "planned_outputs_label": plan.RESEARCH_ONLY_NON_ACTIONABLE,
    }.items():
        if field in {
            "corporate_action_evidence_requirements",
            "future_split_event_authority_chain",
            "future_dividend_event_authority_chain",
            "future_corporate_action_readiness_chain",
            "future_gates",
            "risk_controls",
        } and not review_package.get(field):
            raise CorporateActionAuthorityPlanCandidateReviewPackageError(
                f"{field} missing"
            )
        _expect(review_package.get(field), expected, field)
    if review_package.get("target_universe") != review_package.get("identity_inventory_universe"):
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "target universe differs from identity inventory universe"
        )
    if len(_entries(review_package)) != 12:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "per_ticker_corporate_action_plan_entries mismatch"
        )
    _validate_review_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "review_checklist check IDs")
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    _expect(review_package.get("review_summary"), _summary(expected_checklist), "review_summary")
    digest = review_package.get(
        "corporate_action_authority_plan_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "corporate_action_authority_plan_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        corporate_action_authority_plan_candidate_review_package_digest_v1(
            review_package
        ),
        "corporate_action_authority_plan_candidate_review_package_digest",
    )
    return {
        "status": "CORPORATE_ACTION_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "corporate_action_authority_plan_candidate_review_package_digest": digest,
        "reviewed_corporate_action_authority_plan_candidate_digest": review_package[
            "reviewed_corporate_action_authority_plan_candidate_digest"
        ],
        "post_identity_freeze_registry_inventory_approval_digest": review_package[
            "post_identity_freeze_registry_inventory_approval_digest"
        ],
        "identity_authority_freeze_digest": review_package[
            "identity_authority_freeze_digest"
        ],
        "target_universe_count": review_package["target_universe_count"],
        "per_ticker_corporate_action_plan_review_entry_count": len(
            _review_entries_from_package(review_package)
        ),
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
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


def build_corporate_action_authority_plan_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized corporate-action authority plan review status document."""
    validation = validate_corporate_action_authority_plan_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Corporate-Action Authority Plan Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Corporate-Action Authority Plan Candidate Operator Review Package v1.",
        "",
        "## Reviewed Corporate-Action Authority Plan Candidate",
        f"- Candidate kind: `{review_package['reviewed_corporate_action_authority_plan_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_corporate_action_authority_plan_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_corporate_action_authority_plan_candidate_digest']}`",
        f"- Review package digest: `{validation['corporate_action_authority_plan_candidate_review_package_digest']}`",
        "",
        "## Source Registry Inventory Approval",
        f"- Approval digest: `{review_package['post_identity_freeze_registry_inventory_approval_digest']}`",
        f"- Review package digest: `{review_package['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        f"- Candidate digest: `{review_package['post_identity_freeze_registry_inventory_candidate_digest']}`",
        f"- Identity freeze digest: `{review_package['identity_authority_freeze_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        "",
        "## Corporate-Action Authority Plan Objective",
        f"- corporate_action_authority_plan_objective: `{review_package['corporate_action_authority_plan_objective']}`",
        f"- corporate_action_authority_plan_scope: `{review_package['corporate_action_authority_plan_scope']}`",
        f"- corporate_action_authority_plan_mode: `{review_package['corporate_action_authority_plan_mode']}`",
        f"- corporate_action_authority_creation_status: `{review_package['corporate_action_authority_creation_status']}`",
        "",
        "## Per-Ticker Corporate-Action Plan Review",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['corporate_action_plan_review_status']}`, plan digest `{entry['per_ticker_corporate_action_plan_digest']}`, review digest `{entry['per_ticker_corporate_action_plan_review_digest']}`"
        for entry in review_package["per_ticker_corporate_action_plan_review_entries"]
    )
    lines.extend(["", "## Corporate-Action Evidence Requirements"])
    lines.extend(f"- `{item}`" for item in review_package["corporate_action_evidence_requirements"])
    lines.extend(["", "## Future Split Event Authority Chain"])
    lines.extend(f"- {item}" for item in review_package["future_split_event_authority_chain"])
    lines.extend(["", "## Future Dividend Event Authority Chain"])
    lines.extend(f"- {item}" for item in review_package["future_dividend_event_authority_chain"])
    lines.extend(["", "## Future Corporate-Action Readiness Chain"])
    lines.extend(f"- {item}" for item in review_package["future_corporate_action_readiness_chain"])
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_plan_review_created: `{review_package['corporate_action_authority_plan_review_created']}`",
            f"- corporate_action_authority_plan_approved: `{review_package['corporate_action_authority_plan_approved']}`",
            f"- corporate_action_authority_created: `{review_package['corporate_action_authority_created']}`",
            f"- split_event_authority_created: `{review_package['split_event_authority_created']}`",
            f"- dividend_event_authority_created: `{review_package['dividend_event_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{review_package['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{review_package['canonical_dataset_authorized']}`",
            f"- registry_approval_created: `{review_package['registry_approval_created']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
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
            f"- Ready for operator assessment: `{summary['ready_for_operator_assessment']}`",
            f"- Ready for corporate-action authority plan approval: `{summary['ready_for_corporate_action_authority_plan_approval']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in review.",
            "- No corporate-action authority approval, split-event authority, dividend-event authority, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_corporate_action_authority_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the review package JSON without overwriting an existing artifact."""
    review_package = build_corporate_action_authority_plan_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_corporate_action_authority_plan_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "corporate_action_authority_plan_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "corporate-action authority plan candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise CorporateActionAuthorityPlanCandidateReviewPackageError(
            "corporate-action authority plan candidate review output already exists"
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
