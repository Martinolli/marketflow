"""Offline candidate for post-identity-freeze registry inventory."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import expanded_universe_per_ticker_identity_authority_freeze_service as freeze_service


ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE"
)
SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_V1 = (
    "post_identity_freeze_registry_inventory_candidate_v1"
)
POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW"
)

EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    "55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30"
)
REGISTRY_INVENTORY_OBJECTIVE = (
    "INVENTORY_FROZEN_IDENTITY_AUTHORITY_FOR_EXPANDED_UNIVERSE"
)
REGISTRY_INVENTORY_SCOPE = "IDENTITY_AUTHORITY_INVENTORY_ONLY"
REGISTRY_INVENTORY_MODE = "CANDIDATE_ONLY_NOT_APPROVED"
REGISTRY_INVENTORY_APPROVAL_STATUS = "NOT_APPROVED"
INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW = (
    "INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
)
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(freeze_service.VALIDATION_TARGET_UNIVERSE)
INVENTORY_FIELD_GROUPS = [
    "core_symbol_identity_fields",
    "provider_reference_identity_fields",
    "security_classification_fields",
    "exchange_and_market_fields",
    "provider_cross_reference_fields",
    "audit_digest_fields",
    "limitation_fields",
]
INVENTORY_LIMITATIONS = [
    "reference_details_only",
    "corporate_action_availability_not_evaluated_by_selected_endpoint",
    "historical_aggregate_availability_not_evaluated_by_selected_endpoint",
    "registry_inventory_candidate_not_approved",
    "corporate_action_authority_not_created",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
]
FUTURE_CHAIN = [
    "Post-identity-freeze registry inventory candidate operator review package.",
    "Post-identity-freeze registry inventory approval ceremony, if required.",
    "Corporate-action authority plan candidate.",
    "Split event authority candidate/review/freeze per ticker.",
    "Dividend event authority candidate/review/freeze per ticker.",
    "Acquisition generation candidate only after identity and corporate-action authority.",
    "Canonical dataset candidate only after acquisition generation freeze.",
    "Research registry approval only after canonical dataset freeze.",
]
FUTURE_GATES = [
    "post_identity_freeze_registry_inventory_operator_review",
    "post_identity_freeze_registry_inventory_approval_if_required",
    "corporate_action_authority_plan_candidate",
    "split_event_authority_candidate",
    "dividend_event_authority_candidate",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
RISK_CONTROLS = [
    "no_provider_refresh_without_authority",
    "no_raw_provider_payload_commit",
    "no_api_key_storage_or_printing",
    "no_registry_inventory_approval_without_operator_review",
    "no_corporate_action_authority_without_identity_inventory_review",
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
    "operator_approval_required_before_registry_inventory_approval",
]
PLANNED_OUTPUT_NAMES = [
    "post_identity_freeze_registry_inventory_manifest",
    "per_ticker_identity_registry_inventory_matrix",
    "frozen_identity_digest_inventory",
    "unavailable_identity_field_inventory",
    "identity_inventory_limitation_report",
    "corporate_action_chain_precondition_report",
    "operator_review_summary_template",
]
REQUIRED_CHECK_IDS = [
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
    "registry_inventory_objective_defined",
    "registry_inventory_scope_identity_inventory_only",
    "registry_inventory_mode_candidate_only_not_approved",
    "registry_inventory_approval_status_not_approved",
    "per_ticker_registry_inventory_entries_12",
    "per_ticker_inventory_entries_frozen_identity_only",
    "source_per_ticker_identity_freeze_digests_bound",
    "source_per_ticker_identity_candidate_digests_bound",
    "source_per_ticker_identity_review_digests_bound",
    "per_ticker_registry_inventory_digests_present",
    "unavailable_fields_preserved_as_unavailable",
    "no_unavailable_fields_fabricated",
    "inventory_field_groups_defined",
    "inventory_limitations_recorded",
    "future_chain_defined",
    "future_gates_defined",
    "risk_controls_defined",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "provider_requests_made_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_false",
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


class PostIdentityFreezeRegistryInventoryCandidateError(ValueError):
    """Raised when the post-identity-freeze registry inventory candidate is invalid."""


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
        raise PostIdentityFreezeRegistryInventoryCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PostIdentityFreezeRegistryInventoryCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PostIdentityFreezeRegistryInventoryCandidateError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _default_identity_freeze_artifact() -> dict[str, Any]:
    attestation = freeze_service.build_expanded_universe_per_ticker_identity_authority_freeze_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-10T00:00:00Z",
        operator_attestation_phrase=freeze_service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        operator_confirms_identity_candidate_review_package_digest=(
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        operator_confirms_identity_candidate_digest=(
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        ),
        operator_confirms_identity_plan_review_package_digest=(
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        operator_confirms_live_validation_results_review_digest=(
            freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        operator_confirms_target_universe=freeze_service.VALIDATION_TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_authority_scope_identity_only=True,
        operator_confirms_per_ticker_identity_entries_reviewed=True,
        operator_confirms_no_provider_requests_in_freeze=True,
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
    return freeze_service.build_expanded_universe_per_ticker_identity_authority_frozen_v1(
        operator_attestation=attestation
    )


def _freeze_for_binding(identity_freeze_artifact: dict[str, Any] | None) -> dict[str, Any]:
    artifact = (
        _default_identity_freeze_artifact()
        if identity_freeze_artifact is None
        else deepcopy(identity_freeze_artifact)
    )
    freeze_service.validate_expanded_universe_per_ticker_identity_authority_frozen_v1(artifact)
    return artifact


def _per_ticker_registry_inventory_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_registry_inventory_digest", None)
    return payload


def per_ticker_registry_inventory_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one registry inventory entry."""
    return semantic_digest(_per_ticker_registry_inventory_digest_payload(entry))


def _unavailable_fields_summary(identity_fields: dict[str, Any]) -> dict[str, list[str]]:
    unavailable = sorted(
        field_name
        for field_name, field in identity_fields.items()
        if isinstance(field, dict)
        and field.get("status") == freeze_service.candidate_service.UNAVAILABLE_IN_SOURCE
    )
    available = sorted(
        field_name
        for field_name, field in identity_fields.items()
        if isinstance(field, dict)
        and field.get("status") == freeze_service.candidate_service.AVAILABLE_FROM_SOURCE
    )
    return {"available_fields": available, "unavailable_fields": unavailable}


def _frozen_identity_fields_summary(identity_fields: dict[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for field in identity_fields.values():
        if isinstance(field, dict):
            status = field.get("status")
            if isinstance(status, str):
                status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "field_count": len(identity_fields),
        "status_counts": dict(sorted(status_counts.items())),
        "fields": sorted(identity_fields),
    }


def _inventory_entries(freeze_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in freeze_artifact.get("per_ticker_frozen_identity_entries", []):
        identity_fields = deepcopy(source.get("frozen_identity_fields", {}))
        entry = {
            "ticker": source.get("ticker"),
            "identity_freeze_status": freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            "identity_authority_scope": freeze_service.IDENTITY_AUTHORITY_ONLY,
            "identity_authority_created": True,
            "identity_authority_frozen": True,
            "registry_inventory_entry_status": INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW,
            "corporate_action_authority_created": False,
            "acquisition_authority_created": False,
            "dataset_generation_authorized": False,
            "runtime_use": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "strategy_use": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "paper_trading": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "broker_execution": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
            "source_per_ticker_identity_freeze_digest": source.get(
                "per_ticker_identity_freeze_digest"
            ),
            "source_per_ticker_identity_candidate_digest": source.get(
                "source_per_ticker_identity_candidate_digest"
            ),
            "source_per_ticker_identity_review_digest": source.get(
                "source_per_ticker_identity_review_digest"
            ),
            "frozen_identity_fields_summary": _frozen_identity_fields_summary(identity_fields),
            "unavailable_fields_summary": _unavailable_fields_summary(identity_fields),
            "unavailable_fields_preserved_as_unavailable": True,
            "identity_evidence_limitations": list(INVENTORY_LIMITATIONS),
        }
        entry["per_ticker_registry_inventory_digest"] = per_ticker_registry_inventory_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _planned_outputs() -> list[dict[str, str]]:
    return [
        {
            "planned_output": name,
            "generation_status": PLANNED_NOT_GENERATED,
            "actionability": RESEARCH_ONLY_NON_ACTIONABLE,
        }
        for name in PLANNED_OUTPUT_NAMES
    ]


def _entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = candidate.get("per_ticker_registry_inventory_entries")
    return entries if isinstance(entries, list) else []


def _unavailable_fields_not_fabricated(candidate: dict[str, Any]) -> bool:
    for entry in _entries(candidate):
        summary = entry.get("unavailable_fields_summary")
        if not isinstance(summary, dict):
            return False
        unavailable = summary.get("unavailable_fields")
        if not isinstance(unavailable, list):
            return False
    return True


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = _entries(candidate)
    planned_outputs = candidate.get("planned_outputs", [])
    return [
        _check("identity_freeze_digest_bound", EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, candidate.get("identity_authority_freeze_digest")),
        _check("identity_candidate_review_digest_bound", freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("identity_authority_candidate_review_package_digest")),
        _check("identity_candidate_digest_bound", freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST, candidate.get("identity_authority_candidate_digest")),
        _check("identity_plan_review_digest_bound", freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST, candidate.get("identity_authority_plan_candidate_review_package_digest")),
        _check("live_validation_results_review_digest_bound", freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("live_ticker_validation_results_review_package_digest")),
        _check("ticker_universe_selection_approval_digest_bound", freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, candidate.get("ticker_universe_selection_approval_digest")),
        _check("target_universe_count_12", 12, candidate.get("target_universe_count")),
        _check("target_universe_matches_frozen_identity_universe", VALIDATION_TARGET_UNIVERSE, candidate.get("target_universe")),
        _check("identity_authority_frozen_true", True, candidate.get("identity_authority_frozen")),
        _check("authority_scope_identity_only", freeze_service.IDENTITY_AUTHORITY_ONLY, candidate.get("authority_scope")),
        _check("registry_inventory_objective_defined", REGISTRY_INVENTORY_OBJECTIVE, candidate.get("registry_inventory_objective")),
        _check("registry_inventory_scope_identity_inventory_only", REGISTRY_INVENTORY_SCOPE, candidate.get("registry_inventory_scope")),
        _check("registry_inventory_mode_candidate_only_not_approved", REGISTRY_INVENTORY_MODE, candidate.get("registry_inventory_mode")),
        _check("registry_inventory_approval_status_not_approved", REGISTRY_INVENTORY_APPROVAL_STATUS, candidate.get("registry_inventory_approval_status")),
        _check("per_ticker_registry_inventory_entries_12", 12, len(entries)),
        _check("per_ticker_inventory_entries_frozen_identity_only", True, all(entry.get("identity_authority_scope") == freeze_service.IDENTITY_AUTHORITY_ONLY and entry.get("identity_freeze_status") == freeze_service.IDENTITY_FREEZE_STATUS_FROZEN for entry in entries)),
        _check("source_per_ticker_identity_freeze_digests_bound", True, _digests_present(entries, "source_per_ticker_identity_freeze_digest")),
        _check("source_per_ticker_identity_candidate_digests_bound", True, _digests_present(entries, "source_per_ticker_identity_candidate_digest")),
        _check("source_per_ticker_identity_review_digests_bound", True, _digests_present(entries, "source_per_ticker_identity_review_digest")),
        _check("per_ticker_registry_inventory_digests_present", True, _digests_present(entries, "per_ticker_registry_inventory_digest")),
        _check("unavailable_fields_preserved_as_unavailable", True, all(entry.get("unavailable_fields_preserved_as_unavailable") is True for entry in entries)),
        _check("no_unavailable_fields_fabricated", True, _unavailable_fields_not_fabricated(candidate)),
        _check("inventory_field_groups_defined", INVENTORY_FIELD_GROUPS, candidate.get("inventory_field_groups")),
        _check("inventory_limitations_recorded", INVENTORY_LIMITATIONS, candidate.get("inventory_limitations")),
        _check("future_chain_defined", FUTURE_CHAIN, candidate.get("future_chain")),
        _check("future_gates_defined", FUTURE_GATES, candidate.get("future_gates")),
        _check("risk_controls_defined", RISK_CONTROLS, candidate.get("risk_controls")),
        _check("planned_outputs_not_generated", True, all(item.get("generation_status") == PLANNED_NOT_GENERATED for item in planned_outputs)),
        _check("planned_outputs_research_only", True, all(item.get("actionability") == RESEARCH_ONLY_NON_ACTIONABLE for item in planned_outputs)),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("live_validation_rerun_performed_false", False, candidate.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_false", False, candidate.get("live_provider_transport_enabled")),
        _check("post_identity_freeze_registry_inventory_approved_false", False, candidate.get("post_identity_freeze_registry_inventory_approved")),
        _check("corporate_action_authority_created_false", False, candidate.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, candidate.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, candidate.get("dividend_event_authority_created")),
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
        _check("runtime_use_not_authorized", freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, candidate.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, candidate.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, candidate.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, candidate.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, candidate.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, candidate.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    blockers = [item for item in failed if item.get("severity") == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_review": not failed,
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


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("post_identity_freeze_registry_inventory_candidate_digest", None)
    return payload


def post_identity_freeze_registry_inventory_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the registry inventory candidate."""
    return semantic_digest(_digest_payload(candidate))


def _base_candidate(freeze_artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE,
        "schema_version": SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_V1,
        "candidate_status": POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled": False,
        "post_identity_freeze_registry_inventory_candidate_created": True,
        "post_identity_freeze_registry_inventory_review_created": False,
        "post_identity_freeze_registry_inventory_approved": False,
        "per_ticker_identity_authority_frozen": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": freeze_service.IDENTITY_AUTHORITY_ONLY,
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
        "runtime_use": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "strategy_use": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "paper_trading": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "broker_execution": freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "operator_review_required": True,
        "identity_authority_freeze_digest": freeze_artifact[
            "expanded_universe_per_ticker_identity_authority_freeze_digest"
        ],
        "identity_authority_candidate_review_package_digest": freeze_artifact[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": freeze_artifact[
            "identity_authority_candidate_digest"
        ],
        "identity_authority_plan_candidate_review_package_digest": freeze_artifact[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "identity_authority_plan_candidate_digest": freeze_artifact[
            "identity_authority_plan_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": freeze_artifact[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": freeze_artifact[
            "live_ticker_validation_execution_digest"
        ],
        "live_ticker_validation_approval_digest": freeze_artifact[
            "live_ticker_validation_approval_digest"
        ],
        "ticker_universe_selection_approval_digest": freeze_artifact[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(freeze_artifact["target_universe"]),
        "frozen_identity_universe": list(freeze_artifact["target_universe"]),
        "target_universe_count": freeze_artifact["target_universe_count"],
        "registry_inventory_objective": REGISTRY_INVENTORY_OBJECTIVE,
        "registry_inventory_scope": REGISTRY_INVENTORY_SCOPE,
        "registry_inventory_mode": REGISTRY_INVENTORY_MODE,
        "registry_inventory_approval_status": REGISTRY_INVENTORY_APPROVAL_STATUS,
        "per_ticker_registry_inventory_entries": _inventory_entries(freeze_artifact),
        "inventory_field_groups": list(INVENTORY_FIELD_GROUPS),
        "inventory_limitations": list(INVENTORY_LIMITATIONS),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "planned_outputs": _planned_outputs(),
    }


def build_post_identity_freeze_registry_inventory_candidate_v1(
    identity_freeze_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the offline post-identity-freeze registry inventory candidate."""
    freeze_artifact = _freeze_for_binding(identity_freeze_artifact)
    candidate = _base_candidate(freeze_artifact)
    checklist = _checklist(candidate)
    candidate["inventory_checklist"] = checklist
    candidate["inventory_summary"] = _summary(checklist)
    candidate["post_identity_freeze_registry_inventory_candidate_digest"] = (
        post_identity_freeze_registry_inventory_candidate_digest_v1(candidate)
    )
    validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    forbidden_true_fields = {
        "provider_requests_made",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled",
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
        if key == "artifact_kind" and path != "candidate":
            raise PostIdentityFreezeRegistryInventoryCandidateError(
                f"{current_path} must not create another artifact kind"
            )
        if key in forbidden_true_fields and value is True:
            raise PostIdentityFreezeRegistryInventoryCandidateError(
                f"{current_path} must be false"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"}:
            if value == "AUTHORIZED":
                raise PostIdentityFreezeRegistryInventoryCandidateError(
                    f"{current_path} must not be AUTHORIZED"
                )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PostIdentityFreezeRegistryInventoryCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def _validate_entries(candidate: dict[str, Any]) -> None:
    entries = _entries(candidate)
    if len(entries) != 12:
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "per_ticker_registry_inventory_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_registry_inventory_entries tickers",
    )
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("identity_freeze_status"), freeze_service.IDENTITY_FREEZE_STATUS_FROZEN, f"{ticker}.identity_freeze_status")
        _expect(entry.get("identity_authority_scope"), freeze_service.IDENTITY_AUTHORITY_ONLY, f"{ticker}.identity_authority_scope")
        _expect_true(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect_true(entry.get("identity_authority_frozen"), f"{ticker}.identity_authority_frozen")
        _expect(entry.get("registry_inventory_entry_status"), INVENTORY_CANDIDATE_READY_FOR_OPERATOR_REVIEW, f"{ticker}.registry_inventory_entry_status")
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect_false(entry.get("acquisition_authority_created"), f"{ticker}.acquisition_authority_created")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, f"{ticker}.{field}")
        for field in (
            "source_per_ticker_identity_freeze_digest",
            "source_per_ticker_identity_candidate_digest",
            "source_per_ticker_identity_review_digest",
            "per_ticker_registry_inventory_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise PostIdentityFreezeRegistryInventoryCandidateError(f"{field} missing")
        _expect(
            entry["per_ticker_registry_inventory_digest"],
            per_ticker_registry_inventory_digest_v1(entry),
            f"{ticker}.per_ticker_registry_inventory_digest",
        )
    if not _unavailable_fields_not_fabricated(candidate):
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "unavailable fields must not be fabricated"
        )


def validate_post_identity_freeze_registry_inventory_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate the post-identity-freeze registry inventory candidate."""
    if not isinstance(candidate, dict):
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "candidate must be a JSON object"
        )
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_V1,
        "schema_version",
    )
    _expect(
        candidate.get("candidate_status"),
        POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_READY_FOR_OPERATOR_REVIEW,
        "candidate_status",
    )
    for field in (
        "created_offline",
        "post_identity_freeze_registry_inventory_candidate_created",
        "per_ticker_identity_authority_frozen",
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
        "post_identity_freeze_registry_inventory_review_created",
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
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED, field)
    for field, expected in {
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_candidate_review_package_digest": (
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_candidate_digest": (
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        ),
        "identity_authority_plan_candidate_review_package_digest": (
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "frozen_identity_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": freeze_service.IDENTITY_AUTHORITY_ONLY,
        "registry_inventory_objective": REGISTRY_INVENTORY_OBJECTIVE,
        "registry_inventory_scope": REGISTRY_INVENTORY_SCOPE,
        "registry_inventory_mode": REGISTRY_INVENTORY_MODE,
        "registry_inventory_approval_status": REGISTRY_INVENTORY_APPROVAL_STATUS,
        "inventory_field_groups": INVENTORY_FIELD_GROUPS,
        "inventory_limitations": INVENTORY_LIMITATIONS,
        "future_chain": FUTURE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "planned_outputs": _planned_outputs(),
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(candidate.get(field), expected, field)
    if candidate.get("target_universe") != candidate.get("frozen_identity_universe"):
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "target universe differs from frozen identity universe"
        )
    _validate_entries(candidate)
    checklist = candidate.get("inventory_checklist")
    if not isinstance(checklist, list):
        raise PostIdentityFreezeRegistryInventoryCandidateError("inventory_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "inventory_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            f"inventory checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "inventory_checklist")
    _expect(candidate.get("inventory_summary"), _summary(expected_checklist), "inventory_summary")
    digest = candidate.get("post_identity_freeze_registry_inventory_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "post_identity_freeze_registry_inventory_candidate_digest missing"
        )
    _expect(
        digest,
        post_identity_freeze_registry_inventory_candidate_digest_v1(candidate),
        "post_identity_freeze_registry_inventory_candidate_digest",
    )
    return {
        "status": "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "post_identity_freeze_registry_inventory_candidate_digest": digest,
        "identity_authority_freeze_digest": candidate["identity_authority_freeze_digest"],
        "target_universe_count": candidate["target_universe_count"],
        "per_ticker_registry_inventory_entry_count": len(_entries(candidate)),
        "total_checks": candidate["inventory_summary"]["total_checks"],
        "passed_checks": candidate["inventory_summary"]["passed_checks"],
        "failed_checks": candidate["inventory_summary"]["failed_checks"],
        "blocker_count": candidate["inventory_summary"]["blocker_count"],
        "ready_for_operator_review": candidate["inventory_summary"]["ready_for_operator_review"],
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


def build_post_identity_freeze_registry_inventory_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized registry inventory candidate status document."""
    validation = validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)
    summary = candidate["inventory_summary"]
    unavailable_fields = sorted(
        {
            field
            for entry in _entries(candidate)
            for field in entry.get("unavailable_fields_summary", {}).get("unavailable_fields", [])
        }
    )
    lines = [
        "# MarketFlow Post-Identity-Freeze Registry Inventory Candidate Status",
        "",
        "## Title",
        "- Post-Identity-Freeze Registry Inventory Candidate v1.",
        "",
        "## Purpose",
        f"- Objective: `{candidate['registry_inventory_objective']}`",
        f"- Scope: `{candidate['registry_inventory_scope']}`",
        f"- Mode: `{candidate['registry_inventory_mode']}`",
        "",
        "## Source Identity Freeze",
        f"- Identity freeze digest: `{candidate['identity_authority_freeze_digest']}`",
        f"- Candidate review digest: `{candidate['identity_authority_candidate_review_package_digest']}`",
        f"- Candidate digest: `{candidate['identity_authority_candidate_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{candidate['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in candidate["target_universe"]),
        "",
        "## Per-Ticker Identity Registry Inventory",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['registry_inventory_entry_status']}`, freeze `{entry['identity_freeze_status']}`, digest `{entry['per_ticker_registry_inventory_digest']}`"
        for entry in _entries(candidate)
    )
    lines.extend(["", "## Inventory Field Groups"])
    lines.extend(f"- `{group}`" for group in candidate["inventory_field_groups"])
    lines.extend(["", "## Preserved Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in candidate["inventory_limitations"])
    lines.extend(["", "## Future Chain"])
    lines.extend(f"- `{index}`: {step}" for index, step in enumerate(candidate["future_chain"], start=1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{gate}`" for gate in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in candidate["risk_controls"])
    lines.extend(
        [
            "",
            "## Corporate-Action Boundary",
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
            f"- Ready for registry inventory approval: `{summary['ready_for_registry_inventory_approval']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled.",
            "- No registry inventory approval was created.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
            f"- Candidate digest: `{validation['post_identity_freeze_registry_inventory_candidate_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_post_identity_freeze_registry_inventory_candidate_v1(
    output_dir: str | Path,
    *,
    identity_freeze_artifact: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the registry inventory candidate JSON without overwriting output."""
    candidate = build_post_identity_freeze_registry_inventory_candidate_v1(
        identity_freeze_artifact=identity_freeze_artifact
    )
    validation = validate_post_identity_freeze_registry_inventory_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "post_identity_freeze_registry_inventory_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "post identity freeze registry inventory filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PostIdentityFreezeRegistryInventoryCandidateError(
            "post identity freeze registry inventory output already exists"
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
