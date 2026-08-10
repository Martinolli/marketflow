"""Offline operator review package for the post-identity-freeze registry inventory candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import post_identity_freeze_registry_inventory_candidate_service as candidate_service


ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_V1 = (
    "post_identity_freeze_registry_inventory_candidate_review_v1"
)
POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY"
)
POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING"
)
POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_OBJECT_BINDING = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_OBJECT_BINDING"
)

EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST = (
    "459f20151cf531b32de91defb7d0a676b20ad68a13b4f391840a0e1db921ea34"
)
EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_TOTAL = 72
EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_PASSED = 72
EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_FAILED = 0
EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_BLOCKER_COUNT = 0

READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
REVIEW_ONLY_NOT_APPROVAL = "REVIEW_ONLY_NOT_APPROVAL"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(candidate_service.VALIDATION_TARGET_UNIVERSE)
INVENTORY_FIELD_GROUPS = list(candidate_service.INVENTORY_FIELD_GROUPS)
INVENTORY_LIMITATIONS = list(candidate_service.INVENTORY_LIMITATIONS)
FUTURE_CHAIN = list(candidate_service.FUTURE_CHAIN[1:])
FUTURE_GATES = list(candidate_service.FUTURE_GATES[1:])
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "registry_inventory_candidate_kind_matches",
    "registry_inventory_candidate_status_ready_for_review",
    "registry_inventory_candidate_digest_matches",
    "registry_inventory_candidate_checklist_zero_blockers",
    "identity_freeze_digest_bound",
    "identity_candidate_review_digest_bound",
    "identity_candidate_digest_bound",
    "identity_plan_review_digest_bound",
    "live_validation_results_review_digest_bound",
    "ticker_universe_selection_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_frozen_identity_universe",
    "identity_authority_frozen_true",
    "authority_scope_identity_only",
    "registry_inventory_objective_matches",
    "registry_inventory_scope_identity_inventory_only",
    "registry_inventory_mode_candidate_only_not_approved",
    "registry_inventory_approval_status_not_approved",
    "per_ticker_registry_inventory_entries_12",
    "per_ticker_registry_inventory_review_entries_12",
    "per_ticker_inventory_entries_frozen_identity_only",
    "source_per_ticker_identity_freeze_digests_bound",
    "source_per_ticker_identity_candidate_digests_bound",
    "source_per_ticker_identity_review_digests_bound",
    "per_ticker_registry_inventory_digests_present",
    "per_ticker_registry_inventory_review_digests_present",
    "unavailable_fields_preserved_as_unavailable",
    "no_unavailable_fields_fabricated",
    "inventory_field_groups_reviewed",
    "inventory_limitations_recorded",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_7",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "post_identity_freeze_registry_inventory_approved_false",
    "corporate_action_authority_created_false",
    "split_event_authority_created_false",
    "dividend_event_authority_created_false",
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
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(ValueError):
    """Raised when the registry inventory candidate review package is invalid."""


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
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            f"{field_name} mismatch"
        )


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            f"{field_name} must be true"
        )


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            f"{field_name} must be false"
        )


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _candidate_for_binding(candidate: dict[str, Any] | None) -> tuple[dict[str, Any], str]:
    if candidate is None:
        return (
            candidate_service.build_post_identity_freeze_registry_inventory_candidate_v1(),
            POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING,
        )
    candidate_service.validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)
    return deepcopy(candidate), POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_OBJECT_BINDING


def _per_ticker_review_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_registry_inventory_review_digest", None)
    return payload


def per_ticker_registry_inventory_review_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one registry inventory review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in candidate.get("per_ticker_registry_inventory_entries", []):
        entry = deepcopy(source)
        entry["registry_inventory_review_status"] = READY_FOR_OPERATOR_ASSESSMENT
        entry["post_identity_freeze_registry_inventory_approved"] = False
        entry["per_ticker_registry_inventory_review_digest"] = (
            per_ticker_registry_inventory_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review_package(candidate: dict[str, Any], binding_mode: str) -> dict[str, Any]:
    summary = candidate["inventory_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_V1,
        "review_status": POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY,
        "registry_inventory_candidate_binding_mode": binding_mode,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "post_identity_freeze_registry_inventory_candidate_created": True,
        "post_identity_freeze_registry_inventory_review_created": True,
        "post_identity_freeze_registry_inventory_approved": False,
        "per_ticker_identity_authority_frozen": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": candidate["authority_scope"],
        "corporate_action_authority_created": False,
        "corporate_action_authority_artifact_created": False,
        "split_event_authority_created": False,
        "dividend_event_authority_created": False,
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
        "runtime_use": candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "strategy_use": candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "paper_trading": candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "broker_execution": candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "reviewed_registry_inventory_candidate_kind": candidate["artifact_kind"],
        "reviewed_registry_inventory_candidate_status": candidate["candidate_status"],
        "reviewed_registry_inventory_candidate_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "reviewed_registry_inventory_candidate_checklist_total": summary["total_checks"],
        "reviewed_registry_inventory_candidate_checklist_passed": summary["passed_checks"],
        "reviewed_registry_inventory_candidate_checklist_failed": summary["failed_checks"],
        "reviewed_registry_inventory_candidate_blocker_count": summary["blocker_count"],
        "post_identity_freeze_registry_inventory_candidate_digest": candidate[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": candidate[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": candidate["identity_authority_candidate_digest"],
        "identity_authority_plan_candidate_review_package_digest": candidate[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "identity_authority_plan_candidate_digest": candidate[
            "identity_authority_plan_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": candidate[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": candidate[
            "live_ticker_validation_execution_digest"
        ],
        "live_ticker_validation_approval_digest": candidate[
            "live_ticker_validation_approval_digest"
        ],
        "ticker_universe_selection_approval_digest": candidate[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(candidate["target_universe"]),
        "frozen_identity_universe": list(candidate["frozen_identity_universe"]),
        "target_universe_count": candidate["target_universe_count"],
        "registry_inventory_objective": candidate["registry_inventory_objective"],
        "registry_inventory_scope": candidate["registry_inventory_scope"],
        "registry_inventory_mode": candidate["registry_inventory_mode"],
        "registry_inventory_approval_status": candidate["registry_inventory_approval_status"],
        "per_ticker_registry_inventory_entries": deepcopy(
            candidate["per_ticker_registry_inventory_entries"]
        ),
        "per_ticker_registry_inventory_review_entries": _review_entries(candidate),
        "inventory_field_groups": list(candidate["inventory_field_groups"]),
        "inventory_limitations": list(candidate["inventory_limitations"]),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(candidate["risk_controls"]),
        "planned_outputs": deepcopy(candidate["planned_outputs"]),
        "planned_output_count": len(candidate["planned_outputs"]),
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
    }


def _entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_registry_inventory_entries")
    return entries if isinstance(entries, list) else []


def _review_entries_from_package(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review_package.get("per_ticker_registry_inventory_review_entries")
    return entries if isinstance(entries, list) else []


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _unavailable_fields_not_fabricated(review_package: dict[str, Any]) -> bool:
    for entry in _review_entries_from_package(review_package):
        summary = entry.get("unavailable_fields_summary")
        if not isinstance(summary, dict) or not isinstance(summary.get("unavailable_fields"), list):
            return False
    return True


def _checklist(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    expected_candidate_digest = (
        EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        if review_package.get("registry_inventory_candidate_binding_mode")
        == POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING
        else review_package.get("post_identity_freeze_registry_inventory_candidate_digest")
    )
    return [
        _check("registry_inventory_candidate_kind_matches", candidate_service.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE, review_package.get("reviewed_registry_inventory_candidate_kind")),
        _check("registry_inventory_candidate_status_ready_for_review", candidate_service.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW, review_package.get("reviewed_registry_inventory_candidate_status")),
        _check("registry_inventory_candidate_digest_matches", expected_candidate_digest, review_package.get("reviewed_registry_inventory_candidate_digest")),
        _check("registry_inventory_candidate_checklist_zero_blockers", 0, review_package.get("reviewed_registry_inventory_candidate_blocker_count")),
        _check("identity_freeze_digest_bound", candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, review_package.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, review_package.get("identity_authority_candidate_digest")),
        _check("identity_plan_review_digest_bound", candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, review_package.get("identity_authority_plan_candidate_review_package_digest")),
        _check("live_validation_results_review_digest_bound", candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, review_package.get("live_ticker_validation_results_review_package_digest")),
        _check("ticker_universe_selection_approval_digest_bound", candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, review_package.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, review_package.get("target_universe_count")),
        _check("target_universe_matches_frozen_identity_universe", VALIDATION_TARGET_UNIVERSE, review_package.get("target_universe")),
        _check("identity_authority_frozen_true", True, review_package.get("identity_authority_frozen")),
        _check("authority_scope_identity_only", candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY, review_package.get("authority_scope")),
        _check("registry_inventory_objective_matches", candidate_service.REGISTRY_INVENTORY_OBJECTIVE, review_package.get("registry_inventory_objective")),
        _check("registry_inventory_scope_identity_inventory_only", candidate_service.REGISTRY_INVENTORY_SCOPE, review_package.get("registry_inventory_scope")),
        _check("registry_inventory_mode_candidate_only_not_approved", candidate_service.REGISTRY_INVENTORY_MODE, review_package.get("registry_inventory_mode")),
        _check("registry_inventory_approval_status_not_approved", candidate_service.REGISTRY_INVENTORY_APPROVAL_STATUS, review_package.get("registry_inventory_approval_status")),
        _check("per_ticker_registry_inventory_entries_12", 12, len(entries)),
        _check("per_ticker_registry_inventory_review_entries_12", 12, len(review_entries)),
        _check("per_ticker_inventory_entries_frozen_identity_only", True, all(entry.get("identity_authority_scope") == candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY and entry.get("identity_freeze_status") == candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN for entry in review_entries)),
        _check("source_per_ticker_identity_freeze_digests_bound", True, _digests_present(review_entries, "source_per_ticker_identity_freeze_digest")),
        _check("source_per_ticker_identity_candidate_digests_bound", True, _digests_present(review_entries, "source_per_ticker_identity_candidate_digest")),
        _check("source_per_ticker_identity_review_digests_bound", True, _digests_present(review_entries, "source_per_ticker_identity_review_digest")),
        _check("per_ticker_registry_inventory_digests_present", True, _digests_present(review_entries, "per_ticker_registry_inventory_digest")),
        _check("per_ticker_registry_inventory_review_digests_present", True, _digests_present(review_entries, "per_ticker_registry_inventory_review_digest")),
        _check("unavailable_fields_preserved_as_unavailable", True, all(entry.get("unavailable_fields_preserved_as_unavailable") is True for entry in review_entries)),
        _check("no_unavailable_fields_fabricated", True, _unavailable_fields_not_fabricated(review_package)),
        _check("inventory_field_groups_reviewed", INVENTORY_FIELD_GROUPS, review_package.get("inventory_field_groups")),
        _check("inventory_limitations_recorded", INVENTORY_LIMITATIONS, review_package.get("inventory_limitations")),
        _check("future_chain_defined", FUTURE_CHAIN, review_package.get("future_chain")),
        _check("future_gates_defined", FUTURE_GATES, review_package.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, review_package.get("risk_controls")),
        _check("planned_outputs_7", 7, review_package.get("planned_output_count")),
        _check("planned_outputs_not_generated", candidate_service.PLANNED_NOT_GENERATED, review_package.get("planned_outputs_status")),
        _check("planned_outputs_research_only", candidate_service.RESEARCH_ONLY_NON_ACTIONABLE, review_package.get("planned_outputs_label")),
        _check("provider_requests_made_in_review_false", False, review_package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, review_package.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_review_false", False, review_package.get("live_provider_transport_enabled_in_review")),
        _check("post_identity_freeze_registry_inventory_approved_false", False, review_package.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_authority_created_false", False, review_package.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, review_package.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, review_package.get("dividend_event_authority_created")),
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
        _check("runtime_use_not_authorized", candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("runtime_use")),
        _check("strategy_use_not_authorized", candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("strategy_use")),
        _check("paper_trading_not_authorized", candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("paper_trading")),
        _check("broker_execution_not_authorized", candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, review_package.get("broker_execution")),
        _check("automatic_stitching_false", False, review_package.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, review_package.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, review_package.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, review_package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, review_package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, review_package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, review_package.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    blockers = [item for item in failed if item.get("severity") == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_assessment": not failed,
        "ready_for_registry_inventory_approval": False,
        "ready_for_corporate_action_authority_plan": False,
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
    payload.pop("post_identity_freeze_registry_inventory_candidate_review_package_digest", None)
    return payload


def post_identity_freeze_registry_inventory_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the registry inventory review package."""
    return semantic_digest(_digest_payload(review_package))


def build_post_identity_freeze_registry_inventory_candidate_review_package_v1(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline registry inventory candidate review package."""
    bound_candidate, binding_mode = _candidate_for_binding(candidate)
    review_package = _base_review_package(bound_candidate, binding_mode)
    checklist = _checklist(review_package)
    review_package["review_checklist"] = checklist
    review_package["review_summary"] = _summary(checklist)
    review_package["post_identity_freeze_registry_inventory_candidate_review_package_digest"] = (
        post_identity_freeze_registry_inventory_candidate_review_package_digest_v1(review_package)
    )
    validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(review_package)
    return review_package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
        "post_identity_freeze_registry_inventory_approved",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key == "artifact_kind" and path != "review_package":
            raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_review_entries(review_package: dict[str, Any]) -> None:
    entries = _entries(review_package)
    review_entries = _review_entries_from_package(review_package)
    if len(entries) != 12:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "per_ticker_registry_inventory_entries mismatch"
        )
    if len(review_entries) != 12:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "per_ticker_registry_inventory_review_entries mismatch"
        )
    _expect([entry.get("ticker") for entry in review_entries], VALIDATION_TARGET_UNIVERSE, "per_ticker_registry_inventory_review_entries tickers")
    for entry in review_entries:
        ticker = entry.get("ticker")
        _expect(entry.get("identity_freeze_status"), candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN, f"{ticker}.identity_freeze_status")
        _expect(entry.get("identity_authority_scope"), candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY, f"{ticker}.identity_authority_scope")
        _expect_true(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect_true(entry.get("identity_authority_frozen"), f"{ticker}.identity_authority_frozen")
        _expect(entry.get("registry_inventory_entry_status"), candidate_service.INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW, f"{ticker}.registry_inventory_entry_status")
        _expect(entry.get("registry_inventory_review_status"), READY_FOR_OPERATOR_ASSESSMENT, f"{ticker}.registry_inventory_review_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect_false(entry.get("acquisition_authority_created"), f"{ticker}.acquisition_authority_created")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, f"{ticker}.{field}")
        for field in (
            "source_per_ticker_identity_freeze_digest",
            "source_per_ticker_identity_candidate_digest",
            "source_per_ticker_identity_review_digest",
            "per_ticker_registry_inventory_digest",
            "per_ticker_registry_inventory_review_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
                    f"{field} missing"
                )
        _expect(
            entry["per_ticker_registry_inventory_review_digest"],
            per_ticker_registry_inventory_review_digest_v1(entry),
            f"{ticker}.per_ticker_registry_inventory_review_digest",
        )
    if not _unavailable_fields_not_fabricated(review_package):
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "unavailable fields must not be fabricated"
        )


def validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the registry inventory candidate review package."""
    if not isinstance(review_package, dict):
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "review_package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    if review_package.get("registry_inventory_candidate_binding_mode") not in {
        POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING,
        POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_OBJECT_BINDING,
    }:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "registry_inventory_candidate_binding_mode mismatch"
        )
    expected_candidate_digest = (
        EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        if review_package.get("registry_inventory_candidate_binding_mode")
        == POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_STATUS_BINDING
        else review_package.get("post_identity_freeze_registry_inventory_candidate_digest")
    )
    if not isinstance(expected_candidate_digest, str) or len(expected_candidate_digest) != 64:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "post_identity_freeze_registry_inventory_candidate_digest missing"
        )
    _expect(review_package.get("reviewed_registry_inventory_candidate_digest"), expected_candidate_digest, "reviewed_registry_inventory_candidate_digest")
    _expect(review_package.get("post_identity_freeze_registry_inventory_candidate_digest"), expected_candidate_digest, "post_identity_freeze_registry_inventory_candidate_digest")
    for field in (
        "created_offline",
        "post_identity_freeze_registry_inventory_candidate_created",
        "post_identity_freeze_registry_inventory_review_created",
        "per_ticker_identity_authority_frozen",
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
        "post_identity_freeze_registry_inventory_approved",
        "corporate_action_authority_created",
        "corporate_action_authority_artifact_created",
        "split_event_authority_created",
        "dividend_event_authority_created",
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
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "reviewed_registry_inventory_candidate_kind": candidate_service.ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE,
        "reviewed_registry_inventory_candidate_status": candidate_service.POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW,
        "reviewed_registry_inventory_candidate_checklist_total": EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_TOTAL,
        "reviewed_registry_inventory_candidate_checklist_passed": EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_PASSED,
        "reviewed_registry_inventory_candidate_checklist_failed": EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_CHECKLIST_FAILED,
        "reviewed_registry_inventory_candidate_blocker_count": EXPECTED_REVIEWED_REGISTRY_INVENTORY_CANDIDATE_BLOCKER_COUNT,
        "identity_authority_freeze_digest": candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_candidate_digest": candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST,
        "identity_authority_plan_candidate_review_package_digest": candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "identity_authority_plan_candidate_digest": candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST,
        "live_ticker_validation_results_review_package_digest": candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST,
        "live_ticker_validation_execution_digest": candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST,
        "live_ticker_validation_approval_digest": candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "ticker_universe_selection_approval_digest": candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "frozen_identity_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "registry_inventory_objective": candidate_service.REGISTRY_INVENTORY_OBJECTIVE,
        "registry_inventory_scope": candidate_service.REGISTRY_INVENTORY_SCOPE,
        "registry_inventory_mode": candidate_service.REGISTRY_INVENTORY_MODE,
        "registry_inventory_approval_status": candidate_service.REGISTRY_INVENTORY_APPROVAL_STATUS,
        "inventory_field_groups": INVENTORY_FIELD_GROUPS,
        "inventory_limitations": INVENTORY_LIMITATIONS,
        "future_chain": FUTURE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_output_count": 7,
        "planned_outputs_status": candidate_service.PLANNED_NOT_GENERATED,
        "planned_outputs_label": candidate_service.RESEARCH_ONLY_NON_ACTIONABLE,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(review_package.get(field), expected, field)
    if review_package.get("target_universe") != review_package.get("frozen_identity_universe"):
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "target universe differs from frozen identity universe"
        )
    _validate_review_entries(review_package)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "review_checklist missing"
        )
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "review_checklist check IDs")
    expected_checklist = _checklist(review_package)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            f"review checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    _expect(review_package.get("review_summary"), _summary(expected_checklist), "review_summary")
    digest = review_package.get(
        "post_identity_freeze_registry_inventory_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "post_identity_freeze_registry_inventory_candidate_review_package_digest missing"
        )
    _expect(
        digest,
        post_identity_freeze_registry_inventory_candidate_review_package_digest_v1(
            review_package
        ),
        "post_identity_freeze_registry_inventory_candidate_review_package_digest",
    )
    return {
        "status": "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": digest,
        "reviewed_registry_inventory_candidate_digest": review_package[
            "reviewed_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": review_package["identity_authority_freeze_digest"],
        "target_universe_count": review_package["target_universe_count"],
        "per_ticker_registry_inventory_review_entry_count": len(_review_entries_from_package(review_package)),
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": review_package["review_summary"]["ready_for_operator_assessment"],
        "ready_for_registry_inventory_approval": False,
        "ready_for_corporate_action_authority_plan": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_post_identity_freeze_registry_inventory_candidate_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized registry inventory candidate review status document."""
    validation = validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    unavailable_fields = sorted(
        {
            field
            for entry in _review_entries_from_package(review_package)
            for field in entry.get("unavailable_fields_summary", {}).get("unavailable_fields", [])
        }
    )
    lines = [
        "# MarketFlow Post-Identity-Freeze Registry Inventory Candidate Operator Review Package Status",
        "",
        "## Title",
        "- Post-Identity-Freeze Registry Inventory Candidate Operator Review Package v1.",
        "",
        "## Reviewed Post-Identity-Freeze Registry Inventory Candidate",
        f"- Candidate kind: `{review_package['reviewed_registry_inventory_candidate_kind']}`",
        f"- Candidate status: `{review_package['reviewed_registry_inventory_candidate_status']}`",
        f"- Candidate digest: `{review_package['reviewed_registry_inventory_candidate_digest']}`",
        f"- Review package digest: `{validation['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        "",
        "## Source Identity Freeze",
        f"- Identity freeze digest: `{review_package['identity_authority_freeze_digest']}`",
        f"- Candidate review digest: `{review_package['identity_authority_candidate_review_package_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        "",
        "## Per-Ticker Identity Registry Inventory Review",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['registry_inventory_review_status']}`, digest `{entry['per_ticker_registry_inventory_review_digest']}`"
        for entry in _review_entries_from_package(review_package)
    )
    lines.extend(["", "## Inventory Field Groups"])
    lines.extend(f"- `{group}`" for group in review_package["inventory_field_groups"])
    lines.extend(["", "## Preserved Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in review_package["inventory_limitations"])
    lines.extend(["", "## Future Chain"])
    lines.extend(f"- `{index}`: {step}" for index, step in enumerate(review_package["future_chain"], start=1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in review_package["risk_controls"])
    lines.extend(
        [
            "",
            "## Corporate-Action Boundary",
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
            f"- Ready for registry inventory approval: `{summary['ready_for_registry_inventory_approval']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in review.",
            "- No registry inventory approval was created.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_post_identity_freeze_registry_inventory_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the registry inventory candidate review package JSON without overwriting."""
    review_package = build_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        candidate=candidate
    )
    validation = validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        review_package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "post_identity_freeze_registry_inventory_candidate_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "post identity freeze registry inventory candidate review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PostIdentityFreezeRegistryInventoryCandidateReviewPackageError(
            "post identity freeze registry inventory candidate review output already exists"
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
