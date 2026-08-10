"""Offline operator review package for the expanded-universe identity plan candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    expanded_universe_per_ticker_identity_authority_plan_candidate_service as plan,
)


ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1 = (
    "expanded_universe_per_ticker_identity_authority_plan_candidate_review_v1"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING"
)
EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING = (
    "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST = (
    "210b0a534589a8021f4dcd23eca835bc4cc7b3e0f72b6d3916ee7f5693861981"
)
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_TOTAL = 71
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_PASSED = 71
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_BLOCKER_COUNT = 0

VALIDATION_TARGET_UNIVERSE = list(plan.VALIDATION_TARGET_UNIVERSE)
IDENTITY_FIELDS_TO_BIND = list(plan.IDENTITY_FIELDS_TO_BIND)
IDENTITY_FIELD_GROUPS = deepcopy(plan.IDENTITY_FIELD_GROUPS)
IDENTITY_EVIDENCE_LIMITATIONS = list(plan.IDENTITY_EVIDENCE_LIMITATIONS)
FUTURE_GATES = list(plan.FUTURE_GATES)
RISK_CONTROLS = list(plan.RISK_CONTROLS)
PLANNED_OUTPUT_IDS = list(plan.PLANNED_OUTPUT_IDS)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "identity_authority_plan_candidate_kind_matches",
    "identity_authority_plan_candidate_status_ready_for_review",
    "identity_authority_plan_candidate_digest_matches",
    "identity_authority_plan_candidate_checklist_zero_blockers",
    "live_validation_results_review_digest_bound",
    "live_validation_execution_digest_bound",
    "live_validation_approval_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "scope_expansion_review_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_validated_universe",
    "all_targets_validated_read_only",
    "validation_supports_future_authority_chain_planning_true",
    "validation_creates_new_ticker_authority_false",
    "identity_plan_objective_matches",
    "identity_authority_plan_mode_planned_not_created",
    "identity_authority_creation_status_not_created",
    "identity_freeze_status_not_frozen",
    "per_ticker_identity_plan_entries_12",
    "per_ticker_identity_candidate_not_created",
    "per_ticker_identity_review_not_created",
    "per_ticker_identity_freeze_not_created",
    "identity_fields_to_bind_defined",
    "identity_field_classification_defined",
    "identity_evidence_limitations_recorded",
    "future_identity_authority_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_9",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "corporate_action_authority_created_false",
    "split_event_authority_created_false",
    "dividend_event_authority_created_false",
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
    "no_identity_authority_candidate_created",
    "no_identity_authority_review_created",
    "no_identity_authority_freeze_created",
    "no_corporate_action_authority_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(ValueError):
    """Raised when the expanded-universe identity plan review package is invalid."""


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
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            plan.build_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(),
            EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING,
        )
    plan.validate_expanded_universe_per_ticker_identity_authority_plan_candidate_v1(candidate)
    return (
        deepcopy(candidate),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING,
    )


def _future_identity_authority_chain(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return deepcopy(candidate["future_identity_authority_chain"])


def _planned_outputs(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return deepcopy(candidate["planned_outputs"])


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["plan_summary"]
    return {
        "artifact_kind": (
            ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE
        ),
        "schema_version": (
            SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1
        ),
        "review_status": (
            EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY
        ),
        "identity_authority_plan_candidate_binding_mode": binding_mode,
        "operator_decision_required": True,
        "operator_decision": None,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "identity_authority_plan_candidate_review_created": True,
        "identity_authority_plan_candidate_created": True,
        "per_ticker_identity_authority_candidate_created": False,
        "per_ticker_identity_authority_review_created": False,
        "per_ticker_identity_authority_frozen": False,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "corporate_action_authority_created": False,
        "split_event_authority_created": False,
        "dividend_event_authority_created": False,
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
        "runtime_use": plan.NOT_AUTHORIZED,
        "strategy_use": plan.NOT_AUTHORIZED,
        "paper_trading": plan.NOT_AUTHORIZED,
        "broker_execution": plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "reviewed_identity_authority_plan_candidate_kind": candidate["artifact_kind"],
        "reviewed_identity_authority_plan_candidate_status": candidate["candidate_status"],
        "reviewed_identity_authority_plan_candidate_digest": candidate[
            "expanded_universe_per_ticker_identity_authority_plan_candidate_digest"
        ],
        "reviewed_identity_authority_plan_candidate_checklist_total": summary["total_checks"],
        "reviewed_identity_authority_plan_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_identity_authority_plan_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_identity_authority_plan_candidate_blocker_count": summary["blocker_count"],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": candidate[
            "live_ticker_validation_execution_digest"
        ],
        "live_ticker_validation_approval_digest": candidate["live_ticker_validation_approval_digest"],
        "live_ticker_validation_candidate_digest": candidate["live_ticker_validation_candidate_digest"],
        "live_ticker_validation_candidate_review_package_digest": candidate[
            "live_ticker_validation_candidate_review_package_digest"
        ],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "ticker_universe_selection_candidate_digest": candidate[
            "ticker_universe_selection_candidate_digest"
        ],
        "ticker_universe_selection_candidate_review_package_digest": candidate[
            "ticker_universe_selection_candidate_review_package_digest"
        ],
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            candidate["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"]
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": candidate[
            "predictive_evidence_scope_expansion_plan_candidate_digest"
        ],
        "additional_predictive_evidence_plan_candidate_review_package_digest": candidate[
            "additional_predictive_evidence_plan_candidate_review_package_digest"
        ],
        "additional_predictive_evidence_plan_candidate_digest": candidate[
            "additional_predictive_evidence_plan_candidate_digest"
        ],
        "target_universe": list(candidate["validation_target_universe"]),
        "validated_universe": list(candidate["validation_target_universe"]),
        "target_universe_count": candidate["validation_target_count"],
        "all_targets_validated_read_only": candidate["all_targets_validated_read_only"],
        "validated_read_only_count": candidate["validation_target_count"],
        "provider_request_count": candidate["provider_request_count"],
        "successful_provider_response_count": candidate["successful_provider_response_count"],
        "failed_provider_response_count": candidate["failed_provider_response_count"],
        "validation_supports_future_authority_chain_planning": candidate[
            "validation_supports_future_authority_chain_planning"
        ],
        "validation_creates_new_ticker_authority": candidate[
            "validation_creates_new_ticker_authority"
        ],
        "validation_creates_acquisition_authority": candidate[
            "validation_creates_acquisition_authority"
        ],
        "validation_creates_dataset_generation_authority": candidate[
            "validation_creates_dataset_generation_authority"
        ],
        "validation_creates_predictive_evidence_authority": candidate[
            "validation_creates_predictive_evidence_authority"
        ],
        "identity_authority_plan_objective": candidate["identity_authority_plan_objective"],
        "identity_authority_plan_mode": candidate["identity_authority_plan_mode"],
        "identity_authority_creation_status": candidate["identity_authority_creation_status"],
        "identity_freeze_status": candidate["identity_freeze_status"],
        "identity_authority_created": False,
        "identity_authority_frozen": False,
        "identity_fields_to_bind": list(candidate["identity_fields_to_bind"]),
        "identity_field_groups": deepcopy(candidate["identity_field_groups"]),
        "identity_evidence_limitations": list(candidate["identity_evidence_limitations"]),
        "per_ticker_identity_plan_entries": deepcopy(candidate["per_ticker_identity_plan_entries"]),
        "future_identity_authority_chain": _future_identity_authority_chain(candidate),
        "future_gates": list(candidate["future_gates"]),
        "risk_controls": list(candidate["risk_controls"]),
        "planned_outputs": _planned_outputs(candidate),
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": plan.PLANNED_NOT_GENERATED,
        "planned_outputs_label": plan.RESEARCH_ONLY_NON_ACTIONABLE,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorization_created": False,
        "acquisition_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _per_ticker_entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_identity_plan_entries")
    return entries if isinstance(entries, list) else []


def _all_per_ticker_field(review_package: dict[str, Any], field: str, expected: Any) -> bool:
    entries = _per_ticker_entries(review_package)
    return len(entries) == 12 and all(entry.get(field) == expected for entry in entries)


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    per_ticker_entries = _per_ticker_entries(review_package)
    return [
        _check(
            "identity_authority_plan_candidate_kind_matches",
            plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE,
            review_package.get("reviewed_identity_authority_plan_candidate_kind"),
        ),
        _check(
            "identity_authority_plan_candidate_status_ready_for_review",
            plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW,
            review_package.get("reviewed_identity_authority_plan_candidate_status"),
        ),
        _check(
            "identity_authority_plan_candidate_digest_matches",
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST,
            review_package.get("reviewed_identity_authority_plan_candidate_digest"),
        ),
        _check(
            "identity_authority_plan_candidate_checklist_zero_blockers",
            0,
            review_package.get("reviewed_identity_authority_plan_candidate_blocker_count"),
        ),
        _check(
            "live_validation_results_review_digest_bound",
            plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
            review_package.get("live_ticker_validation_results_review_package_digest"),
        ),
        _check(
            "live_validation_execution_digest_bound",
            plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
            review_package.get("live_ticker_validation_execution_digest"),
        ),
        _check(
            "live_validation_approval_digest_bound",
            plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
            review_package.get("live_ticker_validation_approval_digest"),
        ),
        _check(
            "ticker_universe_selection_approval_digest_bound",
            plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
            review_package.get("ticker_universe_selection_approval_digest"),
        ),
        _check(
            "scope_expansion_review_digest_bound",
            plan.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            review_package.get(
                "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
            ),
        ),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check(
            "target_universe_matches_validated_universe",
            True,
            review_package.get("target_universe")
            == review_package.get("validated_universe")
            == VALIDATION_TARGET_UNIVERSE,
        ),
        _check(
            "all_targets_validated_read_only",
            True,
            review_package.get("all_targets_validated_read_only"),
        ),
        _check(
            "validation_supports_future_authority_chain_planning_true",
            True,
            review_package.get("validation_supports_future_authority_chain_planning"),
        ),
        _check(
            "validation_creates_new_ticker_authority_false",
            False,
            review_package.get("validation_creates_new_ticker_authority"),
        ),
        _check(
            "identity_plan_objective_matches",
            plan.IDENTITY_AUTHORITY_PLAN_OBJECTIVE,
            review_package.get("identity_authority_plan_objective"),
        ),
        _check(
            "identity_authority_plan_mode_planned_not_created",
            plan.PLANNED_NOT_CREATED,
            review_package.get("identity_authority_plan_mode"),
        ),
        _check(
            "identity_authority_creation_status_not_created",
            plan.NOT_CREATED,
            review_package.get("identity_authority_creation_status"),
        ),
        _check(
            "identity_freeze_status_not_frozen",
            plan.NOT_FROZEN,
            review_package.get("identity_freeze_status"),
        ),
        _check("per_ticker_identity_plan_entries_12", 12, len(per_ticker_entries)),
        _check(
            "per_ticker_identity_candidate_not_created",
            True,
            _all_per_ticker_field(review_package, "identity_candidate_status", plan.NOT_CREATED),
        ),
        _check(
            "per_ticker_identity_review_not_created",
            True,
            _all_per_ticker_field(review_package, "identity_review_status", plan.NOT_CREATED),
        ),
        _check(
            "per_ticker_identity_freeze_not_created",
            True,
            _all_per_ticker_field(review_package, "identity_freeze_status", plan.NOT_FROZEN),
        ),
        _check("identity_fields_to_bind_defined", IDENTITY_FIELDS_TO_BIND, review_package.get("identity_fields_to_bind")),
        _check(
            "identity_field_classification_defined",
            IDENTITY_FIELD_GROUPS,
            review_package.get("identity_field_groups"),
        ),
        _check(
            "identity_evidence_limitations_recorded",
            IDENTITY_EVIDENCE_LIMITATIONS,
            review_package.get("identity_evidence_limitations"),
        ),
        _check(
            "future_identity_authority_chain_defined",
            True,
            isinstance(review_package.get("future_identity_authority_chain"), list)
            and len(review_package.get("future_identity_authority_chain", [])) == 9,
        ),
        _check("future_gates_defined", FUTURE_GATES, review_package.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review_package.get("risk_controls")),
        _check("planned_outputs_9", 9, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", plan.PLANNED_NOT_GENERATED, review_package.get("planned_outputs_status")),
        _check("planned_outputs_research_only", plan.RESEARCH_ONLY_NON_ACTIONABLE, review_package.get("planned_outputs_label")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, review_package.get("live_validation_rerun_performed")),
        _check(
            "live_provider_transport_enabled_in_review_false",
            False,
            review_package.get("live_provider_transport_enabled_in_review"),
        ),
        _check("new_ticker_authority_created_false", False, review_package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, review_package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, review_package.get("dataset_generation_authorized")),
        _check("corporate_action_authority_created_false", False, review_package.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, review_package.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, review_package.get("dividend_event_authority_created")),
        _check("acquisition_generation_authorized_false", False, review_package.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, review_package.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, review_package.get("registry_approval_created")),
        _check(
            "additional_predictive_evidence_execution_authorized_false",
            False,
            review_package.get("additional_predictive_evidence_execution_authorized"),
        ),
        _check(
            "additional_predictive_evidence_executed_false",
            False,
            review_package.get("additional_predictive_evidence_executed"),
        ),
        _check("predictive_experiment_rerun_authorized_false", False, review_package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, review_package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, review_package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, review_package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, review_package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, review_package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, review_package.get("trade_recommendations_generated")),
        _check(
            "predictive_usefulness_not_accepted",
            acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            review_package.get("predictive_usefulness"),
        ),
        _check("predictive_usefulness_acceptance_ready_false", False, review_package.get("predictive_usefulness_acceptance_ready")),
        _check(
            "predictive_usefulness_acceptance_recommended_false",
            False,
            review_package.get("predictive_usefulness_acceptance_recommended"),
        ),
        _check(
            "predictive_usefulness_acceptance_candidate_created_false",
            False,
            review_package.get("predictive_usefulness_acceptance_candidate_created"),
        ),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, review_package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, review_package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, review_package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, review_package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, review_package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, review_package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, review_package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", plan.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", plan.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", plan.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", plan.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check(
            "no_identity_authority_candidate_created",
            False,
            review_package.get("per_ticker_identity_authority_candidate_created"),
        ),
        _check(
            "no_identity_authority_review_created",
            False,
            review_package.get("per_ticker_identity_authority_review_created"),
        ),
        _check(
            "no_identity_authority_freeze_created",
            False,
            review_package.get("per_ticker_identity_authority_frozen"),
        ),
        _check("no_corporate_action_authority_created", False, review_package.get("corporate_action_authority_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_created")),
        _check(
            "no_dataset_generation_authorization_created",
            False,
            review_package.get("dataset_generation_authorization_created"),
        ),
        _check(
            "no_predictive_usefulness_acceptance_artifact_created",
            False,
            review_package.get("predictive_usefulness_acceptance_artifact_created"),
        ),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blocker_count = sum(1 for item in failed if item.get("severity") == BLOCKER)
    ready = not failed
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": blocker_count,
        "ready_for_operator_assessment": ready,
        "ready_for_per_ticker_identity_authority_candidate": False,
        "identity_authority_created": False,
        "identity_authority_frozen": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop(
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest",
        None,
    )
    return payload


def expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate review package."""
    return semantic_digest(_digest_payload(review_package))


def build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline review package without creating identity authority."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package[
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    ] = expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1(
        review_package
    )
    validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "per_ticker_identity_authority_candidate_created",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
        "identity_authority_created",
        "identity_authority_frozen",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key == "artifact_kind" and path != "review_package":
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_per_ticker_entries(review_package: dict[str, Any]) -> None:
    entries = review_package.get("per_ticker_identity_plan_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "per_ticker_identity_plan_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_identity_plan_entries tickers",
    )
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("live_validation_status"),
            plan.VALIDATED_READ_ONLY,
            f"{ticker}.live_validation_status",
        )
        _expect(
            entry.get("identity_authority_plan_status"),
            plan.PLANNED_NOT_CREATED,
            f"{ticker}.identity_authority_plan_status",
        )
        _expect(entry.get("identity_candidate_status"), plan.NOT_CREATED, f"{ticker}.identity_candidate_status")
        _expect(entry.get("identity_review_status"), plan.NOT_CREATED, f"{ticker}.identity_review_status")
        _expect(entry.get("identity_freeze_status"), plan.NOT_FROZEN, f"{ticker}.identity_freeze_status")
        _expect_false(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect(entry.get("identity_fields_to_bind"), IDENTITY_FIELDS_TO_BIND, f"{ticker}.identity_fields_to_bind")
        _expect(entry.get("identity_evidence_source"), plan.IDENTITY_EVIDENCE_SOURCE, f"{ticker}.identity_evidence_source")
        _expect(
            entry.get("identity_evidence_limitations"),
            IDENTITY_EVIDENCE_LIMITATIONS,
            f"{ticker}.identity_evidence_limitations",
        )
        _expect(
            entry.get("next_required_identity_gate"),
            plan.NEXT_REQUIRED_IDENTITY_GATE,
            f"{ticker}.next_required_identity_gate",
        )


def validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the review package without creating identity authority or runtime rights."""
    if not isinstance(review_package, dict):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    if review_package.get("identity_authority_plan_candidate_binding_mode") not in {
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_STATUS_BINDING,
        EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_OBJECT_BINDING,
    }:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "identity_authority_plan_candidate_binding_mode mismatch"
        )
    for field in (
        "operator_decision_required",
        "created_offline",
        "identity_authority_plan_candidate_review_created",
        "identity_authority_plan_candidate_created",
        "research_only",
    ):
        _expect_true(review_package.get(field), field)
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    for field in (
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "per_ticker_identity_authority_candidate_created",
        "per_ticker_identity_authority_review_created",
        "per_ticker_identity_authority_frozen",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "corporate_action_authority_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
        "identity_authority_created",
        "identity_authority_frozen",
        "corporate_action_authority_authorized",
        "acquisition_authorized",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_identity_authority_plan_candidate_kind": (
            plan.ARTIFACT_KIND_EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE
        ),
        "reviewed_identity_authority_plan_candidate_status": (
            plan.EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_READY_FOR_OPERATOR_REVIEW
        ),
        "reviewed_identity_authority_plan_candidate_digest": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "reviewed_identity_authority_plan_candidate_checklist_total": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_TOTAL
        ),
        "reviewed_identity_authority_plan_candidate_checklist_passed": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_PASSED
        ),
        "reviewed_identity_authority_plan_candidate_checklist_failed": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_CHECKLIST_FAILED
        ),
        "reviewed_identity_authority_plan_candidate_blocker_count": (
            EXPECTED_REVIEWED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_BLOCKER_COUNT
        ),
        "live_ticker_validation_results_review_package_digest": (
            plan.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": plan.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "live_ticker_validation_approval_digest": plan.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": (
            plan.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            plan.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_candidate_digest": (
            plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
        ),
        "ticker_universe_selection_candidate_review_package_digest": (
            plan.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest": (
            plan.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_evidence_scope_expansion_plan_candidate_digest": (
            plan.EXPECTED_PREDICTIVE_EVIDENCE_SCOPE_EXPANSION_PLAN_CANDIDATE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_review_package_digest": (
            plan.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "additional_predictive_evidence_plan_candidate_digest": (
            plan.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_CANDIDATE_DIGEST
        ),
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "validated_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "all_targets_validated_read_only": True,
        "validated_read_only_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "validation_supports_future_authority_chain_planning": True,
        "validation_creates_new_ticker_authority": False,
        "validation_creates_acquisition_authority": False,
        "validation_creates_dataset_generation_authority": False,
        "validation_creates_predictive_evidence_authority": False,
        "identity_authority_plan_objective": plan.IDENTITY_AUTHORITY_PLAN_OBJECTIVE,
        "identity_authority_plan_mode": plan.PLANNED_NOT_CREATED,
        "identity_authority_creation_status": plan.NOT_CREATED,
        "identity_freeze_status": plan.NOT_FROZEN,
        "identity_fields_to_bind": IDENTITY_FIELDS_TO_BIND,
        "identity_field_groups": IDENTITY_FIELD_GROUPS,
        "identity_evidence_limitations": IDENTITY_EVIDENCE_LIMITATIONS,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": plan._planned_outputs(),
        "planned_output_count": 9,
        "planned_outputs_status": plan.PLANNED_NOT_GENERATED,
        "planned_outputs_label": plan.RESEARCH_ONLY_NON_ACTIONABLE,
    }.items():
        if field in {
            "identity_fields_to_bind",
            "identity_field_groups",
            "identity_evidence_limitations",
            "future_gates",
            "risk_controls",
            "planned_outputs",
        } and not review_package.get(field):
            raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
                f"{field} missing"
            )
        _expect(review_package.get(field), expected, field)
    if review_package.get("target_universe") != review_package.get("validated_universe"):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "target_universe differs from validated_universe"
        )
    future_chain = review_package.get("future_identity_authority_chain")
    if not isinstance(future_chain, list) or len(future_chain) != 9:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "future_identity_authority_chain missing"
        )
    _expect(future_chain, plan._future_identity_authority_chain(), "future_identity_authority_chain")
    _validate_per_ticker_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest_v1(
            review_package
        ),
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest",
    )
    return {
        "status": (
            "EXPANDED_UNIVERSE_PER_TICKER_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_VALID"
        ),
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest": (
            digest
        ),
        "reviewed_identity_authority_plan_candidate_digest": review_package[
            "reviewed_identity_authority_plan_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": review_package[
            "live_ticker_validation_results_review_package_digest"
        ],
        "target_universe_count": review_package["target_universe_count"],
        "per_ticker_identity_plan_entry_count": len(_per_ticker_entries(review_package)),
        "ready_for_operator_assessment": review_package["review_summary"][
            "ready_for_operator_assessment"
        ],
        "ready_for_per_ticker_identity_authority_candidate": False,
        "identity_authority_created": False,
        "identity_authority_frozen": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
    }


def build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized expanded-universe identity plan review package summary."""
    validation = validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Expanded Universe Per-Ticker Identity Authority Plan Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Expanded Universe Per-Ticker Identity Authority Plan Candidate Operator Review Package v1.",
        "",
        "## Reviewed Expanded Universe Identity Authority Plan Candidate",
        f"- Candidate kind: `{review_package['reviewed_identity_authority_plan_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_identity_authority_plan_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_identity_authority_plan_candidate_digest']}`",
        f"- Review package digest: `{validation['expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_digest']}`",
        "",
        "## Source Live Ticker Validation Results",
        f"- Results review package digest: `{review_package['live_ticker_validation_results_review_package_digest']}`",
        f"- Execution digest: `{review_package['live_ticker_validation_execution_digest']}`",
        f"- Approval digest: `{review_package['live_ticker_validation_approval_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        f"- All targets validated read-only: `{review_package['all_targets_validated_read_only']}`",
        "",
        "## Identity Authority Plan Objective",
        f"- identity_authority_plan_objective: `{review_package['identity_authority_plan_objective']}`",
        f"- identity_authority_plan_mode: `{review_package['identity_authority_plan_mode']}`",
        f"- identity_authority_creation_status: `{review_package['identity_authority_creation_status']}`",
        f"- identity_freeze_status: `{review_package['identity_freeze_status']}`",
        "",
        "## Per-Ticker Identity Plan Entries",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: validation `{entry['live_validation_status']}`, plan `{entry['identity_authority_plan_status']}`, candidate `{entry['identity_candidate_status']}`, review `{entry['identity_review_status']}`, freeze `{entry['identity_freeze_status']}`"
        for entry in review_package["per_ticker_identity_plan_entries"]
    )
    lines.extend(["", "## Identity Fields to Bind"])
    lines.extend(f"- `{field}`" for field in review_package["identity_fields_to_bind"])
    lines.extend(["", "## Evidence Limitations"])
    lines.extend(f"- `{item}`" for item in review_package["identity_evidence_limitations"])
    lines.extend(["", "## Future Identity Authority Chain"])
    lines.extend(
        f"- `{step['step_number']}`: {step['authority_step']}"
        for step in review_package["future_identity_authority_chain"]
    )
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_authority_created: `{review_package['identity_authority_created']}`",
            f"- per_ticker_identity_authority_candidate_created: `{review_package['per_ticker_identity_authority_candidate_created']}`",
            f"- per_ticker_identity_authority_frozen: `{review_package['per_ticker_identity_authority_frozen']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{review_package['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{review_package['canonical_dataset_authorized']}`",
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
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in review.",
            "- No identity authority candidate, identity review package, or identity freeze was created.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the review package JSON without overwriting an existing artifact."""
    review_package = build_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename
        or "expanded_universe_per_ticker_identity_authority_plan_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "expanded universe identity authority plan candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise ExpandedUniversePerTickerIdentityAuthorityPlanCandidateReviewPackageError(
            "expanded universe identity authority plan candidate review output already exists"
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
