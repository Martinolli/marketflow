"""Offline approval ceremony for post-identity-freeze registry inventory."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    post_identity_freeze_registry_inventory_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED"
)
SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_V1 = (
    "post_identity_freeze_registry_inventory_approval_v1"
)
POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED = (
    "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED"
)
IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY = (
    "IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY"
)
OPERATOR_DECISION_APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY = (
    "APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY"
)
OPERATOR_ATTESTATION_VERSION_V1 = (
    "post_identity_freeze_registry_inventory_approval_operator_attestation_v1"
)
REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE POST IDENTITY FREEZE REGISTRY INVENTORY MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ WMT CAT LMT IDENTITY_AUTHORITY_INVENTORY_ONLY"
)

EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "d35861b3bb19d361241df0e6ba080306e647116cf5b12815ce1ddf2fb48cf51c"
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST = (
    review_service.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
)
APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY = (
    "APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY"
)
APPROVED = "APPROVED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

VALIDATION_TARGET_UNIVERSE = list(review_service.VALIDATION_TARGET_UNIVERSE)
INVENTORY_FIELD_GROUPS = list(review_service.INVENTORY_FIELD_GROUPS)
INVENTORY_LIMITATIONS = list(review_service.INVENTORY_LIMITATIONS)
FUTURE_CHAIN = [
    "Corporate-action authority plan candidate.",
    "Split event authority candidate/review/freeze per ticker.",
    "Dividend event authority candidate/review/freeze per ticker.",
    "Acquisition generation candidate only after identity and corporate-action authority.",
    "Canonical dataset candidate only after acquisition generation freeze.",
    "Research registry approval only after canonical dataset freeze.",
]
FUTURE_GATES = [
    "corporate_action_authority_plan_candidate",
    "split_event_authority_candidate",
    "dividend_event_authority_candidate",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
RISK_CONTROLS = list(review_service.RISK_CONTROLS)

OPERATOR_BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_identity_authority_scope_identity_only",
    "operator_confirms_registry_inventory_scope_identity_inventory_only",
    "operator_confirms_registry_inventory_entries_reviewed",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_validation_rerun",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_corporate_action_authority",
    "operator_confirms_no_split_event_authority",
    "operator_confirms_no_dividend_event_authority",
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

REQUIRED_CHECK_IDS = [
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_registry_inventory_review_digest_matches",
    "operator_registry_inventory_candidate_digest_matches",
    "operator_identity_freeze_digest_matches",
    "operator_target_universe_matches",
    "operator_target_count_12",
    "operator_confirms_identity_authority_scope_identity_only",
    "operator_confirms_registry_inventory_scope_identity_inventory_only",
    "operator_confirms_registry_inventory_entries_reviewed",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_validation_rerun",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_corporate_action_authority",
    "operator_confirms_no_split_event_authority",
    "operator_confirms_no_dividend_event_authority",
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
    "approval_scope_identity_authority_inventory_only",
    "post_identity_freeze_registry_inventory_candidate_created_true",
    "post_identity_freeze_registry_inventory_review_created_true",
    "post_identity_freeze_registry_inventory_approved_true",
    "identity_authority_created_true",
    "identity_authority_frozen_true",
    "new_ticker_identity_authority_created_true",
    "authority_scope_identity_only",
    "registry_inventory_review_digest_bound",
    "registry_inventory_candidate_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_review_package",
    "registry_inventory_objective_matches",
    "registry_inventory_scope_identity_inventory_only",
    "registry_inventory_approval_status_approved",
    "per_ticker_registry_inventory_approval_entries_12",
    "per_ticker_registry_inventory_approval_digests_present",
    "per_ticker_entries_approved_for_future_corporate_action_planning_only",
    "unavailable_fields_preserved_as_unavailable",
    "no_unavailable_fields_fabricated",
    "provider_requests_made_in_approval_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_approval_false",
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


class PostIdentityFreezeRegistryInventoryApprovalError(ValueError):
    """Raised when the registry inventory approval ceremony is invalid."""


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
        raise PostIdentityFreezeRegistryInventoryApprovalError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PostIdentityFreezeRegistryInventoryApprovalError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PostIdentityFreezeRegistryInventoryApprovalError(f"{field_name} must be false")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def build_post_identity_freeze_registry_inventory_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_registry_inventory_candidate_review_package_digest: str,
    operator_confirms_registry_inventory_candidate_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_identity_authority_scope_identity_only: bool,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_registry_inventory_scope_identity_inventory_only: bool,
    operator_confirms_registry_inventory_entries_reviewed: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_live_validation_rerun: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_corporate_action_authority: bool,
    operator_confirms_no_split_event_authority: bool,
    operator_confirms_no_dividend_event_authority: bool,
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
    operator_decision: str = OPERATOR_DECISION_APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY,
    operator_attestation_version: str = OPERATOR_ATTESTATION_VERSION_V1,
) -> dict[str, Any]:
    """Build the non-secret operator attestation required for approval."""
    return {
        "operator_decision": operator_decision,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": operator_attestation_version,
        "operator_reference": operator_reference,
        "operator_confirms_registry_inventory_candidate_review_package_digest": (
            operator_confirms_registry_inventory_candidate_review_package_digest
        ),
        "operator_confirms_registry_inventory_candidate_digest": (
            operator_confirms_registry_inventory_candidate_digest
        ),
        "operator_confirms_identity_freeze_digest": operator_confirms_identity_freeze_digest,
        "operator_confirms_identity_authority_scope_identity_only": (
            operator_confirms_identity_authority_scope_identity_only
        ),
        "operator_confirms_target_universe": list(operator_confirms_target_universe),
        "operator_confirms_target_count": operator_confirms_target_count,
        "operator_confirms_registry_inventory_scope_identity_inventory_only": (
            operator_confirms_registry_inventory_scope_identity_inventory_only
        ),
        "operator_confirms_registry_inventory_entries_reviewed": (
            operator_confirms_registry_inventory_entries_reviewed
        ),
        "operator_confirms_no_provider_requests_in_approval": (
            operator_confirms_no_provider_requests_in_approval
        ),
        "operator_confirms_no_live_validation_rerun": operator_confirms_no_live_validation_rerun,
        "operator_confirms_no_live_provider_transport_enabled": (
            operator_confirms_no_live_provider_transport_enabled
        ),
        "operator_confirms_no_corporate_action_authority": (
            operator_confirms_no_corporate_action_authority
        ),
        "operator_confirms_no_split_event_authority": (
            operator_confirms_no_split_event_authority
        ),
        "operator_confirms_no_dividend_event_authority": (
            operator_confirms_no_dividend_event_authority
        ),
        "operator_confirms_no_acquisition_authority": operator_confirms_no_acquisition_authority,
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
        "operator_confirms_no_runtime_activation": operator_confirms_no_runtime_activation,
        "operator_confirms_no_paper_trading": operator_confirms_no_paper_trading,
        "operator_confirms_no_broker_execution": operator_confirms_no_broker_execution,
        "operator_confirms_no_trade_recommendations": (
            operator_confirms_no_trade_recommendations
        ),
        "operator_confirms_no_api_key_storage_or_printing": (
            operator_confirms_no_api_key_storage_or_printing
        ),
        "operator_confirms_no_raw_payload_commit": operator_confirms_no_raw_payload_commit,
    }


def _review_package_for_binding(
    registry_inventory_review_package: dict[str, Any] | None,
) -> dict[str, Any]:
    package = (
        review_service.build_post_identity_freeze_registry_inventory_candidate_review_package_v1()
        if registry_inventory_review_package is None
        else deepcopy(registry_inventory_review_package)
    )
    review_service.validate_post_identity_freeze_registry_inventory_candidate_review_package_v1(
        package
    )
    return package


def _expected_attestation_values(review_package: dict[str, Any]) -> dict[str, Any]:
    return {
        "operator_decision": (
            OPERATOR_DECISION_APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY
        ),
        "operator_attestation_phrase": (
            REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_V1,
        "operator_confirms_registry_inventory_candidate_review_package_digest": (
            review_package[
                "post_identity_freeze_registry_inventory_candidate_review_package_digest"
            ]
        ),
        "operator_confirms_registry_inventory_candidate_digest": (
            review_package["post_identity_freeze_registry_inventory_candidate_digest"]
        ),
        "operator_confirms_identity_freeze_digest": (
            review_package["identity_authority_freeze_digest"]
        ),
        "operator_confirms_target_universe": VALIDATION_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
    }


def _validate_operator_attestation(
    operator_attestation: dict[str, Any],
    review_package: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(operator_attestation, dict):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "operator_attestation must be a JSON object"
        )
    if not operator_attestation.get("operator_reference"):
        raise PostIdentityFreezeRegistryInventoryApprovalError("operator_reference missing")
    if not operator_attestation.get("operator_attestation_timestamp_utc"):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "operator_attestation_timestamp_utc missing"
        )
    for field, expected in _expected_attestation_values(review_package).items():
        _expect(operator_attestation.get(field), expected, field)
    for field in OPERATOR_BOOLEAN_CONFIRMATION_FIELDS:
        _expect_true(operator_attestation.get(field), field)
    return deepcopy(operator_attestation)


def _per_ticker_approval_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_registry_inventory_approval_digest", None)
    return payload


def per_ticker_registry_inventory_approval_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for one approved inventory entry."""
    return semantic_digest(_per_ticker_approval_digest_payload(entry))


def _approval_entries(review_package: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source in review_package.get("per_ticker_registry_inventory_review_entries", []):
        entry = deepcopy(source)
        entry["registry_inventory_entry_status"] = (
            APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        )
        entry["post_identity_freeze_registry_inventory_approved"] = True
        entry["per_ticker_registry_inventory_approval_digest"] = (
            per_ticker_registry_inventory_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _entries(approved_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    entries = approved_artifact.get("per_ticker_registry_inventory_approval_entries")
    return entries if isinstance(entries, list) else []


def _digests_present(entries: list[dict[str, Any]], field_name: str) -> bool:
    return all(isinstance(entry.get(field_name), str) and len(entry[field_name]) == 64 for entry in entries)


def _unavailable_fields_not_fabricated(approved_artifact: dict[str, Any]) -> bool:
    for entry in _entries(approved_artifact):
        summary = entry.get("unavailable_fields_summary")
        if not isinstance(summary, dict):
            return False
        unavailable = summary.get("unavailable_fields")
        if not isinstance(unavailable, list):
            return False
        if entry.get("unavailable_fields_preserved_as_unavailable") is not True:
            return False
    return True


def _checklist(approved_artifact: dict[str, Any]) -> list[dict[str, Any]]:
    attestation = approved_artifact.get("operator_attestation", {})
    entries = _entries(approved_artifact)
    not_authorized = review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    return [
        _check("operator_decision_approved", OPERATOR_DECISION_APPROVE_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY, attestation.get("operator_decision")),
        _check("operator_attestation_phrase_matches", REQUIRED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_ATTESTATION_PHRASE, attestation.get("operator_attestation_phrase")),
        _check("operator_registry_inventory_review_digest_matches", approved_artifact.get("post_identity_freeze_registry_inventory_candidate_review_package_digest"), attestation.get("operator_confirms_registry_inventory_candidate_review_package_digest")),
        _check("operator_registry_inventory_candidate_digest_matches", approved_artifact.get("post_identity_freeze_registry_inventory_candidate_digest"), attestation.get("operator_confirms_registry_inventory_candidate_digest")),
        _check("operator_identity_freeze_digest_matches", approved_artifact.get("identity_authority_freeze_digest"), attestation.get("operator_confirms_identity_freeze_digest")),
        _check("operator_target_universe_matches", VALIDATION_TARGET_UNIVERSE, attestation.get("operator_confirms_target_universe")),
        _check("operator_target_count_12", 12, attestation.get("operator_confirms_target_count")),
        *[_check(field, True, attestation.get(field)) for field in OPERATOR_BOOLEAN_CONFIRMATION_FIELDS],
        _check("approval_scope_identity_authority_inventory_only", IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY, approved_artifact.get("approval_scope")),
        _check("post_identity_freeze_registry_inventory_candidate_created_true", True, approved_artifact.get("post_identity_freeze_registry_inventory_candidate_created")),
        _check("post_identity_freeze_registry_inventory_review_created_true", True, approved_artifact.get("post_identity_freeze_registry_inventory_review_created")),
        _check("post_identity_freeze_registry_inventory_approved_true", True, approved_artifact.get("post_identity_freeze_registry_inventory_approved")),
        _check("identity_authority_created_true", True, approved_artifact.get("identity_authority_created")),
        _check("identity_authority_frozen_true", True, approved_artifact.get("identity_authority_frozen")),
        _check("new_ticker_identity_authority_created_true", True, approved_artifact.get("new_ticker_identity_authority_created")),
        _check("authority_scope_identity_only", review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY, approved_artifact.get("authority_scope")),
        _check("registry_inventory_review_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST, approved_artifact.get("post_identity_freeze_registry_inventory_candidate_review_package_digest")),
        _check("registry_inventory_candidate_digest_bound", EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST, approved_artifact.get("post_identity_freeze_registry_inventory_candidate_digest")),
        _check("identity_freeze_digest_bound", review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, approved_artifact.get("identity_authority_freeze_digest")),
        _check("target_universe_count_12", 12, approved_artifact.get("target_universe_count")),
        _check("target_universe_matches_review_package", VALIDATION_TARGET_UNIVERSE, approved_artifact.get("target_universe")),
        _check("registry_inventory_objective_matches", review_service.candidate_service.REGISTRY_INVENTORY_OBJECTIVE, approved_artifact.get("registry_inventory_objective")),
        _check("registry_inventory_scope_identity_inventory_only", review_service.candidate_service.REGISTRY_INVENTORY_SCOPE, approved_artifact.get("registry_inventory_scope")),
        _check("registry_inventory_approval_status_approved", APPROVED, approved_artifact.get("registry_inventory_approval_status")),
        _check("per_ticker_registry_inventory_approval_entries_12", 12, len(entries)),
        _check("per_ticker_registry_inventory_approval_digests_present", True, _digests_present(entries, "per_ticker_registry_inventory_approval_digest")),
        _check("per_ticker_entries_approved_for_future_corporate_action_planning_only", True, all(entry.get("registry_inventory_entry_status") == APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY for entry in entries)),
        _check("unavailable_fields_preserved_as_unavailable", True, all(entry.get("unavailable_fields_preserved_as_unavailable") is True for entry in entries)),
        _check("no_unavailable_fields_fabricated", True, _unavailable_fields_not_fabricated(approved_artifact)),
        _check("provider_requests_made_in_approval_false", False, approved_artifact.get("provider_requests_made_in_approval")),
        _check("live_validation_rerun_performed_false", False, approved_artifact.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_approval_false", False, approved_artifact.get("live_provider_transport_enabled_in_approval")),
        _check("corporate_action_authority_created_false", False, approved_artifact.get("corporate_action_authority_created")),
        _check("split_event_authority_created_false", False, approved_artifact.get("split_event_authority_created")),
        _check("dividend_event_authority_created_false", False, approved_artifact.get("dividend_event_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, approved_artifact.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, approved_artifact.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, approved_artifact.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, approved_artifact.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, approved_artifact.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, approved_artifact.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, approved_artifact.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, approved_artifact.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, approved_artifact.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, approved_artifact.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, approved_artifact.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, approved_artifact.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, approved_artifact.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, approved_artifact.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, approved_artifact.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, approved_artifact.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, approved_artifact.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, approved_artifact.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, approved_artifact.get("profitability")),
        _check("profitability_acceptance_ready_false", False, approved_artifact.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, approved_artifact.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, approved_artifact.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, approved_artifact.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, approved_artifact.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, approved_artifact.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", not_authorized, approved_artifact.get("runtime_use")),
        _check("strategy_use_not_authorized", not_authorized, approved_artifact.get("strategy_use")),
        _check("paper_trading_not_authorized", not_authorized, approved_artifact.get("paper_trading")),
        _check("broker_execution_not_authorized", not_authorized, approved_artifact.get("broker_execution")),
        _check("automatic_stitching_false", False, approved_artifact.get("automatic_stitching")),
        _check("no_corporate_action_authority_artifact_created", False, approved_artifact.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, approved_artifact.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, approved_artifact.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, approved_artifact.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, approved_artifact.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, approved_artifact.get("runtime_migration_approval_created")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item["status"] != PASS]
    blockers = [item for item in failed if item["severity"] == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "registry_inventory_approved_by_operator": not failed,
        "approval_scope": IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY,
        "ready_for_corporate_action_authority_plan_candidate": not failed,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _approval_digest_payload(approved_artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approved_artifact)
    payload.pop("post_identity_freeze_registry_inventory_approval_digest", None)
    return payload


def post_identity_freeze_registry_inventory_approval_digest_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval artifact."""
    return semantic_digest(_approval_digest_payload(approved_artifact))


def build_post_identity_freeze_registry_inventory_approved_v1(
    *,
    registry_inventory_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    """Build an offline identity-inventory-only approval artifact."""
    review_package = _review_package_for_binding(registry_inventory_review_package)
    attestation = _validate_operator_attestation(operator_attestation, review_package)
    not_authorized = review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    approved_artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED,
        "schema_version": SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_V1,
        "approval_status": POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED,
        "approval_scope": IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_approval": False,
        "post_identity_freeze_registry_inventory_candidate_created": True,
        "post_identity_freeze_registry_inventory_review_created": True,
        "post_identity_freeze_registry_inventory_approved": True,
        "per_ticker_identity_authority_frozen": True,
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "new_ticker_identity_authority_created": True,
        "authority_scope": review_package["authority_scope"],
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
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": review_package[
            "post_identity_freeze_registry_inventory_candidate_review_package_digest"
        ],
        "post_identity_freeze_registry_inventory_candidate_digest": review_package[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": review_package["identity_authority_freeze_digest"],
        "identity_authority_candidate_review_package_digest": review_package[
            "identity_authority_candidate_review_package_digest"
        ],
        "identity_authority_candidate_digest": review_package[
            "identity_authority_candidate_digest"
        ],
        "identity_authority_plan_candidate_review_package_digest": review_package[
            "identity_authority_plan_candidate_review_package_digest"
        ],
        "identity_authority_plan_candidate_digest": review_package[
            "identity_authority_plan_candidate_digest"
        ],
        "live_ticker_validation_results_review_package_digest": review_package[
            "live_ticker_validation_results_review_package_digest"
        ],
        "live_ticker_validation_execution_digest": review_package[
            "live_ticker_validation_execution_digest"
        ],
        "live_ticker_validation_approval_digest": review_package[
            "live_ticker_validation_approval_digest"
        ],
        "ticker_universe_selection_approval_digest": review_package[
            "ticker_universe_selection_approval_digest"
        ],
        "target_universe": list(review_package["target_universe"]),
        "frozen_identity_universe": list(review_package["frozen_identity_universe"]),
        "target_universe_count": review_package["target_universe_count"],
        "registry_inventory_objective": review_package["registry_inventory_objective"],
        "registry_inventory_scope": review_package["registry_inventory_scope"],
        "registry_inventory_approval_status": APPROVED,
        "approved_inventory_entry_status": (
            APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        ),
        "per_ticker_registry_inventory_approval_entries": _approval_entries(review_package),
        "inventory_field_groups": list(review_package["inventory_field_groups"]),
        "inventory_limitations": list(review_package["inventory_limitations"]),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }
    checklist = _checklist(approved_artifact)
    approved_artifact["approval_checklist"] = checklist
    approved_artifact["approval_summary"] = _summary(checklist)
    approved_artifact["post_identity_freeze_registry_inventory_approval_digest"] = (
        post_identity_freeze_registry_inventory_approval_digest_v1(approved_artifact)
    )
    validate_post_identity_freeze_registry_inventory_approved_v1(approved_artifact)
    return approved_artifact


def _validate_approval_entries(approved_artifact: dict[str, Any]) -> None:
    entries = _entries(approved_artifact)
    if len(entries) != 12:
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "per_ticker_registry_inventory_approval_entries mismatch"
        )
    _expect(
        [entry.get("ticker") for entry in entries],
        VALIDATION_TARGET_UNIVERSE,
        "per_ticker_registry_inventory_approval_entries tickers",
    )
    not_authorized = review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(
            entry.get("identity_freeze_status"),
            review_service.candidate_service.freeze_service.IDENTITY_FREEZE_STATUS_FROZEN,
            f"{ticker}.identity_freeze_status",
        )
        _expect(
            entry.get("identity_authority_scope"),
            review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
            f"{ticker}.identity_authority_scope",
        )
        _expect_true(entry.get("identity_authority_created"), f"{ticker}.identity_authority_created")
        _expect_true(entry.get("identity_authority_frozen"), f"{ticker}.identity_authority_frozen")
        _expect(
            entry.get("registry_inventory_entry_status"),
            APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY,
            f"{ticker}.registry_inventory_entry_status",
        )
        _expect_true(
            entry.get("post_identity_freeze_registry_inventory_approved"),
            f"{ticker}.post_identity_freeze_registry_inventory_approved",
        )
        _expect_false(entry.get("corporate_action_authority_created"), f"{ticker}.corporate_action_authority_created")
        _expect_false(entry.get("acquisition_authority_created"), f"{ticker}.acquisition_authority_created")
        _expect_false(entry.get("dataset_generation_authorized"), f"{ticker}.dataset_generation_authorized")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), not_authorized, f"{ticker}.{field}")
        for field in (
            "source_per_ticker_identity_freeze_digest",
            "source_per_ticker_identity_candidate_digest",
            "source_per_ticker_identity_review_digest",
            "per_ticker_registry_inventory_digest",
            "per_ticker_registry_inventory_review_digest",
            "per_ticker_registry_inventory_approval_digest",
        ):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64:
                raise PostIdentityFreezeRegistryInventoryApprovalError(f"{field} missing")
        for field in (
            "frozen_identity_fields_summary",
            "unavailable_fields_summary",
            "identity_evidence_limitations",
        ):
            if field not in entry:
                raise PostIdentityFreezeRegistryInventoryApprovalError(f"{field} missing")
        _expect(
            entry["per_ticker_registry_inventory_approval_digest"],
            per_ticker_registry_inventory_approval_digest_v1(entry),
            f"{ticker}.per_ticker_registry_inventory_approval_digest",
        )
    if not _unavailable_fields_not_fabricated(approved_artifact):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "unavailable fields must not be fabricated"
        )


def validate_post_identity_freeze_registry_inventory_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    """Validate the registry inventory approval ceremony artifact."""
    if not isinstance(approved_artifact, dict):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "approved_artifact must be a JSON object"
        )
    _expect(
        approved_artifact.get("artifact_kind"),
        ARTIFACT_KIND_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED,
        "artifact_kind",
    )
    _expect(
        approved_artifact.get("schema_version"),
        SCHEMA_VERSION_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_V1,
        "schema_version",
    )
    _expect(
        approved_artifact.get("approval_status"),
        POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED,
        "approval_status",
    )
    _expect(
        approved_artifact.get("approval_scope"),
        IDENTITY_AUTHORITY_INVENTORY_APPROVAL_ONLY,
        "approval_scope",
    )
    for field in (
        "created_offline",
        "post_identity_freeze_registry_inventory_candidate_created",
        "post_identity_freeze_registry_inventory_review_created",
        "post_identity_freeze_registry_inventory_approved",
        "per_ticker_identity_authority_frozen",
        "identity_authority_created",
        "identity_authority_frozen",
        "new_ticker_identity_authority_created",
        "research_only",
    ):
        _expect_true(approved_artifact.get(field), field)
    for field in (
        "provider_requests_made_in_approval",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_approval",
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
        _expect_false(approved_artifact.get(field), field)
    not_authorized = review_service.candidate_service.freeze_service.candidate_service.plan_review.plan.NOT_AUTHORIZED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(approved_artifact.get(field), not_authorized, field)
    for field, expected in {
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": (
            EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "post_identity_freeze_registry_inventory_candidate_digest": (
            EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_CANDIDATE_DIGEST
        ),
        "identity_authority_freeze_digest": (
            review_service.candidate_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
        ),
        "identity_authority_candidate_review_package_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_candidate_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_CANDIDATE_DIGEST
        ),
        "identity_authority_plan_candidate_review_package_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "identity_authority_plan_candidate_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_IDENTITY_AUTHORITY_PLAN_CANDIDATE_DIGEST
        ),
        "live_ticker_validation_results_review_package_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "live_ticker_validation_execution_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_EXECUTION_DIGEST
        ),
        "live_ticker_validation_approval_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
        ),
        "ticker_universe_selection_approval_digest": (
            review_service.candidate_service.freeze_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "target_universe": VALIDATION_TARGET_UNIVERSE,
        "frozen_identity_universe": VALIDATION_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "authority_scope": review_service.candidate_service.freeze_service.IDENTITY_AUTHORITY_ONLY,
        "registry_inventory_objective": review_service.candidate_service.REGISTRY_INVENTORY_OBJECTIVE,
        "registry_inventory_scope": review_service.candidate_service.REGISTRY_INVENTORY_SCOPE,
        "registry_inventory_approval_status": APPROVED,
        "approved_inventory_entry_status": (
            APPROVED_FOR_FUTURE_CORPORATE_ACTION_PLANNING_ONLY
        ),
        "inventory_field_groups": INVENTORY_FIELD_GROUPS,
        "inventory_limitations": INVENTORY_LIMITATIONS,
        "future_chain": FUTURE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(approved_artifact.get(field), expected, field)
    if approved_artifact.get("target_universe") != approved_artifact.get("frozen_identity_universe"):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "target universe differs from frozen identity universe"
        )
    _validate_operator_attestation(
        approved_artifact.get("operator_attestation", {}),
        {
            "post_identity_freeze_registry_inventory_candidate_review_package_digest": approved_artifact.get(
                "post_identity_freeze_registry_inventory_candidate_review_package_digest"
            ),
            "post_identity_freeze_registry_inventory_candidate_digest": approved_artifact.get(
                "post_identity_freeze_registry_inventory_candidate_digest"
            ),
            "identity_authority_freeze_digest": approved_artifact.get(
                "identity_authority_freeze_digest"
            ),
        },
    )
    _validate_approval_entries(approved_artifact)
    checklist = approved_artifact.get("approval_checklist")
    if not isinstance(checklist, list):
        raise PostIdentityFreezeRegistryInventoryApprovalError("approval_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "approval_checklist check IDs",
    )
    expected_checklist = _checklist(approved_artifact)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            f"approval checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "approval_checklist")
    _expect(approved_artifact.get("approval_summary"), _summary(expected_checklist), "approval_summary")
    digest = approved_artifact.get("post_identity_freeze_registry_inventory_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "post_identity_freeze_registry_inventory_approval_digest missing"
        )
    _expect(
        digest,
        post_identity_freeze_registry_inventory_approval_digest_v1(approved_artifact),
        "post_identity_freeze_registry_inventory_approval_digest",
    )
    return {
        "status": "POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "approval_scope": approved_artifact["approval_scope"],
        "post_identity_freeze_registry_inventory_approval_digest": digest,
        "post_identity_freeze_registry_inventory_candidate_review_package_digest": (
            approved_artifact[
                "post_identity_freeze_registry_inventory_candidate_review_package_digest"
            ]
        ),
        "post_identity_freeze_registry_inventory_candidate_digest": approved_artifact[
            "post_identity_freeze_registry_inventory_candidate_digest"
        ],
        "identity_authority_freeze_digest": approved_artifact["identity_authority_freeze_digest"],
        "target_universe_count": approved_artifact["target_universe_count"],
        "per_ticker_registry_inventory_approval_entry_count": len(_entries(approved_artifact)),
        "total_checks": approved_artifact["approval_summary"]["total_checks"],
        "passed_checks": approved_artifact["approval_summary"]["passed_checks"],
        "failed_checks": approved_artifact["approval_summary"]["failed_checks"],
        "blocker_count": approved_artifact["approval_summary"]["blocker_count"],
        "registry_inventory_approved_by_operator": approved_artifact["approval_summary"][
            "registry_inventory_approved_by_operator"
        ],
        "ready_for_corporate_action_authority_plan_candidate": approved_artifact[
            "approval_summary"
        ]["ready_for_corporate_action_authority_plan_candidate"],
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def build_post_identity_freeze_registry_inventory_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    """Render a sanitized registry inventory approval status document."""
    validation = validate_post_identity_freeze_registry_inventory_approved_v1(
        approved_artifact
    )
    summary = approved_artifact["approval_summary"]
    attestation = approved_artifact["operator_attestation"]
    unavailable_fields = sorted(
        {
            field
            for entry in _entries(approved_artifact)
            for field in entry.get("unavailable_fields_summary", {}).get("unavailable_fields", [])
        }
    )
    lines = [
        "# MarketFlow Post-Identity-Freeze Registry Inventory Approval Status",
        "",
        "## Approved Post-Identity-Freeze Registry Inventory",
        f"- Artifact kind: `{approved_artifact['artifact_kind']}`",
        f"- Approval status: `{approved_artifact['approval_status']}`",
        f"- Approval scope: `{approved_artifact['approval_scope']}`",
        f"- Approval digest: `{validation['post_identity_freeze_registry_inventory_approval_digest']}`",
        "",
        "## Operator Attestation",
        f"- Operator reference: `{attestation['operator_reference']}`",
        f"- Operator decision: `{attestation['operator_decision']}`",
        f"- Attestation version: `{attestation['operator_attestation_version']}`",
        f"- Attestation timestamp UTC: `{attestation['operator_attestation_timestamp_utc']}`",
        "",
        "## Source Registry Inventory Review Package",
        f"- Review package digest: `{approved_artifact['post_identity_freeze_registry_inventory_candidate_review_package_digest']}`",
        f"- Candidate digest: `{approved_artifact['post_identity_freeze_registry_inventory_candidate_digest']}`",
        "",
        "## Source Identity Freeze",
        f"- Identity freeze digest: `{approved_artifact['identity_authority_freeze_digest']}`",
        f"- Identity authority scope: `{approved_artifact['authority_scope']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{approved_artifact['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in approved_artifact["target_universe"]),
        "",
        "## Approved Per-Ticker Identity Registry Inventory",
    ]
    lines.extend(
        f"- `{entry['ticker']}`: `{entry['registry_inventory_entry_status']}`, digest `{entry['per_ticker_registry_inventory_approval_digest']}`"
        for entry in _entries(approved_artifact)
    )
    lines.extend(["", "## Preserved Unavailable Fields and Limitations"])
    lines.extend(f"- `{field}`" for field in unavailable_fields)
    lines.extend(f"- `{item}`" for item in approved_artifact["inventory_limitations"])
    lines.extend(
        [
            "",
            "## Approval Scope",
            "- Identity authority inventory approval only.",
            "- Future corporate-action planning may begin as a separate candidate.",
            "- No downstream authority is created by this artifact.",
            "",
            "## Corporate-Action Boundary",
            f"- corporate_action_authority_created: `{approved_artifact['corporate_action_authority_created']}`",
            f"- split_event_authority_created: `{approved_artifact['split_event_authority_created']}`",
            f"- dividend_event_authority_created: `{approved_artifact['dividend_event_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{approved_artifact['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{approved_artifact['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{approved_artifact['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{approved_artifact['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{approved_artifact['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{approved_artifact['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{approved_artifact['predictive_usefulness']}`",
            f"- profitability: `{approved_artifact['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{approved_artifact['runtime_migration_approved']}`",
            f"- runtime_use: `{approved_artifact['runtime_use']}`",
            f"- strategy_use: `{approved_artifact['strategy_use']}`",
            f"- paper_trading: `{approved_artifact['paper_trading']}`",
            f"- broker_execution: `{approved_artifact['broker_execution']}`",
            "",
            "## Approval Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Registry inventory approved by operator: `{summary['registry_inventory_approved_by_operator']}`",
            f"- Ready for corporate-action authority plan candidate: `{summary['ready_for_corporate_action_authority_plan_candidate']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"- {step}" for step in approved_artifact["future_chain"])
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in approval.",
            "- No corporate-action, acquisition, dataset, predictive, profitability, runtime, paper-trading, broker, or trade-recommendation authorization was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_post_identity_freeze_registry_inventory_approved_v1(
    output_dir: str | Path,
    *,
    registry_inventory_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the registry inventory approval artifact JSON without overwriting."""
    approved_artifact = build_post_identity_freeze_registry_inventory_approved_v1(
        registry_inventory_review_package=registry_inventory_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_post_identity_freeze_registry_inventory_approved_v1(
        approved_artifact
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "post_identity_freeze_registry_inventory_approved_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "post identity freeze registry inventory approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PostIdentityFreezeRegistryInventoryApprovalError(
            "post identity freeze registry inventory approval output already exists"
        )
    payload = canonical_json_bytes(approved_artifact)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
