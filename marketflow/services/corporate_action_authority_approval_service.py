"""Offline operator ceremony for corporate-action-only authority approval."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import (
    combined_split_dividend_corporate_action_readiness_review_service as readiness,
)


ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_APPROVED = "CORPORATE_ACTION_AUTHORITY_APPROVED"
SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1 = (
    "corporate_action_authority_approval_v1"
)
CORPORATE_ACTION_AUTHORITY_APPROVED = "CORPORATE_ACTION_AUTHORITY_APPROVED"
CORPORATE_ACTION_AUTHORITY_ONLY = "CORPORATE_ACTION_AUTHORITY_ONLY"
OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY = (
    "APPROVE_CORPORATE_ACTION_AUTHORITY"
)
OPERATOR_ATTESTATION_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1 = (
    "corporate_action_authority_approval_operator_attestation_v1"
)
REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE CORPORATE ACTION AUTHORITY MSFT NVDA AMZN GOOGL META TSLA JPM XOM JNJ "
    "WMT CAT LMT CORPORATE_ACTION_AUTHORITY_ONLY"
)

EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST = (
    "ee425cb1ee8b9e513d3ed4bc5ddc05ca7498a3003bc5820c5a2b5014f799d621"
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    readiness.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    readiness.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    readiness.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    readiness.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST = (
    readiness.EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST
)
EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST = (
    readiness.EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    readiness.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST = (
    readiness.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
)
EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST = (
    readiness.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    readiness.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    readiness.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)

TARGET_UNIVERSE = list(readiness.TARGET_UNIVERSE)
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_AUTHORIZED = readiness.NOT_AUTHORIZED
NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

LIMITATIONS = [
    "corporate_action_authority_is_authority_only",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
    "canonical_dataset_not_authorized",
    "registry_approval_not_created",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "operator_approval_required_before_acquisition_generation_chain",
]
NEXT_GATES = [
    "acquisition_generation_chain_candidate",
    "acquisition_generation_candidate_operator_review",
    "acquisition_generation_approval_ceremony_if_required",
    "canonical_dataset_chain_candidate",
    "canonical_dataset_candidate_operator_review",
    "canonical_dataset_freeze_ceremony",
    "research_registry_chain_candidate",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

OPERATOR_BOOLEAN_CONFIRMATION_FIELDS = [
    "operator_confirms_authority_scope_corporate_action_only",
    "operator_confirms_ready_for_acquisition_generation_chain_candidate",
    "operator_confirms_no_provider_requests_in_approval",
    "operator_confirms_no_live_provider_transport_enabled",
    "operator_confirms_no_split_provider_evidence_rerun",
    "operator_confirms_no_dividend_provider_evidence_rerun",
    "operator_confirms_split_authority_frozen",
    "operator_confirms_dividend_authority_frozen",
    "operator_confirms_no_acquisition_authority",
    "operator_confirms_no_dataset_generation_authorization",
    "operator_confirms_no_canonical_dataset_authorization",
    "operator_confirms_no_registry_approval",
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

REQUIRED_APPROVAL_CHECK_IDS = [
    "combined_readiness_review_digest_matches_expected",
    "combined_readiness_review_has_zero_blockers",
    "split_authority_freeze_digest_bound",
    "dividend_authority_freeze_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "registry_inventory_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_combined_readiness_universe",
    "operator_decision_approved",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_source_digests",
    "operator_confirms_authority_scope_corporate_action_only",
    "operator_confirms_ready_for_acquisition_chain_candidate",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "dividend_event_authority_created_true",
    "dividend_event_authority_frozen_true",
    "corporate_action_authority_created_true",
    "corporate_action_authority_approved_true",
    "corporate_action_authority_scope_corporate_action_only",
    "per_ticker_corporate_action_authority_entries_12",
    "per_ticker_corporate_action_authority_approval_digests_present",
    "ready_for_acquisition_generation_chain_candidate_true",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "acquisition_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "registry_approval_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "provider_requests_made_in_approval_false",
    "live_provider_transport_enabled_in_approval_false",
    "split_provider_evidence_rerun_performed_false",
    "dividend_provider_evidence_rerun_performed_false",
    "corporate_action_authority_creates_acquisition_authority_false",
    "corporate_action_authority_creates_dataset_generation_authority_false",
    "corporate_action_authority_creates_predictive_evidence_authority_false",
    "corporate_action_authority_creates_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CorporateActionAuthorityApprovalError(ValueError):
    """Raised when corporate-action approval evidence or attestation is invalid."""


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CorporateActionAuthorityApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CorporateActionAuthorityApprovalError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CorporateActionAuthorityApprovalError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CorporateActionAuthorityApprovalError(f"{field} missing")


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_combined_readiness_review_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_split_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_dividend_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "operator_confirms_corporate_action_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "operator_confirms_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "operator_confirms_identity_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
    }


def build_corporate_action_authority_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_combined_readiness_review_digest: str,
    operator_confirms_split_authority_freeze_digest: str,
    operator_confirms_dividend_authority_freeze_digest: str,
    operator_confirms_corporate_action_plan_approval_digest: str,
    operator_confirms_registry_inventory_approval_digest: str,
    operator_confirms_identity_freeze_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_authority_scope_corporate_action_only: bool,
    operator_confirms_ready_for_acquisition_generation_chain_candidate: bool,
    operator_confirms_no_provider_requests_in_approval: bool,
    operator_confirms_no_live_provider_transport_enabled: bool,
    operator_confirms_no_split_provider_evidence_rerun: bool,
    operator_confirms_no_dividend_provider_evidence_rerun: bool,
    operator_confirms_split_authority_frozen: bool,
    operator_confirms_dividend_authority_frozen: bool,
    operator_confirms_no_acquisition_authority: bool,
    operator_confirms_no_dataset_generation_authorization: bool,
    operator_confirms_no_canonical_dataset_authorization: bool,
    operator_confirms_no_registry_approval: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_runtime_activation: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY,
) -> dict[str, Any]:
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1
    }


def _validate_operator_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise CorporateActionAuthorityApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY,
        "operator_attestation_phrase": REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in OPERATOR_BOOLEAN_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise CorporateActionAuthorityApprovalError(f"{field} required")


def _validate_source(source: Mapping[str, Any]) -> None:
    if not isinstance(source, dict):
        raise CorporateActionAuthorityApprovalError("combined_readiness_review_package missing")
    validation = readiness.validate_combined_split_dividend_corporate_action_readiness_review_package_v1(
        source
    )
    _expect(
        validation.get(
            "combined_split_dividend_corporate_action_readiness_review_package_digest"
        ),
        EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "source.combined readiness digest",
    )
    _expect(validation.get("blocker_count"), 0, "source.blocker_count")
    _expect(source.get("ready_for_corporate_action_authority_approval"), True, "source.ready")


def per_ticker_corporate_action_authority_approval_digest_v1(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("per_ticker_corporate_action_authority_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_row in source["per_ticker_combined_readiness"]:
        entry = {
            "ticker": source_row["ticker"],
            "corporate_action_authority_status": "APPROVED",
            "corporate_action_authority_scope": CORPORATE_ACTION_AUTHORITY_ONLY,
            "split_event_authority_status": "FROZEN",
            "split_event_authority_classification": source_row[
                "split_event_authority_classification"
            ],
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_classification": source_row[
                "dividend_event_authority_classification"
            ],
            "dividend_event_count": source_row["dividend_event_count"],
            "corporate_action_authority_created": True,
            "corporate_action_authority_approved": True,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_per_ticker_combined_readiness_review_digest": source_row[
                "per_ticker_combined_readiness_review_digest"
            ],
        }
        entry["per_ticker_corporate_action_authority_approval_digest"] = (
            per_ticker_corporate_action_authority_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_artifact(source: Mapping[str, Any], attestation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_APPROVED,
        "schema_version": SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1,
        "approval_status": CORPORATE_ACTION_AUTHORITY_APPROVED,
        "authority_scope": CORPORATE_ACTION_AUTHORITY_ONLY,
        "created_offline": True,
        "provider_requests_made_in_approval": False,
        "live_provider_transport_enabled_in_approval": False,
        "split_provider_evidence_rerun_performed": False,
        "dividend_provider_evidence_rerun_performed": False,
        "combined_corporate_action_readiness_review_created": True,
        "combined_corporate_action_readiness_review_ready": True,
        "ready_for_corporate_action_authority_approval": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": readiness.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": readiness.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_frozen": False,
        "corporate_action_authority_artifact_created": True,
        "ready_for_acquisition_generation_chain_candidate": True,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "acquisition_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_policy_reconciliation_approval_digest": EXPECTED_DIVIDEND_POLICY_RECONCILIATION_APPROVAL_DIGEST,
        "dividend_event_evidence_results_review_package_digest": EXPECTED_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "source_combined_readiness_review_blocker_count": source["review_summary"][
            "blocker_count"
        ],
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "per_ticker_corporate_action_authority": _per_ticker_entries(source),
        "combined_split_dividend_authorities_available": True,
        "split_authority_frozen": True,
        "dividend_authority_frozen": True,
        "corporate_action_authority_approved_by_operator": True,
        "corporate_action_authority_creates_acquisition_authority": False,
        "corporate_action_authority_creates_dataset_generation_authority": False,
        "corporate_action_authority_creates_predictive_evidence_authority": False,
        "corporate_action_authority_creates_runtime_authority": False,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "operator_attestation": deepcopy(dict(attestation)),
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _approval_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    operator = artifact["operator_attestation"]
    entries = artifact["per_ticker_corporate_action_authority"]
    digests_present = len(entries) == 12 and all(
        len(row.get("per_ticker_corporate_action_authority_approval_digest", "")) == 64
        for row in entries
    )
    values: dict[str, tuple[Any, Any]] = {
        "combined_readiness_review_digest_matches_expected": (EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST, artifact.get("combined_split_dividend_corporate_action_readiness_review_package_digest")),
        "combined_readiness_review_has_zero_blockers": (0, artifact.get("source_combined_readiness_review_blocker_count")),
        "split_authority_freeze_digest_bound": (EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("split_event_authority_freeze_digest")),
        "dividend_authority_freeze_digest_bound": (EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST, artifact.get("dividend_event_authority_freeze_digest")),
        "corporate_action_plan_approval_digest_bound": (EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, artifact.get("corporate_action_authority_plan_approval_digest")),
        "registry_inventory_approval_digest_bound": (EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST, artifact.get("post_identity_freeze_registry_inventory_approval_digest")),
        "identity_freeze_digest_bound": (EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, artifact.get("identity_authority_freeze_digest")),
        "target_universe_count_12": (12, artifact.get("target_universe_count")),
        "target_universe_matches_combined_readiness_universe": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "operator_decision_approved": (OPERATOR_DECISION_APPROVE_CORPORATE_ACTION_AUTHORITY, operator.get("operator_decision")),
        "operator_attestation_phrase_matches": (REQUIRED_CORPORATE_ACTION_AUTHORITY_APPROVAL_ATTESTATION_PHRASE, operator.get("operator_attestation_phrase")),
        "operator_confirms_all_source_digests": (True, all(operator.get(field) == value for field, value in _expected_digest_confirmations().items())),
        "operator_confirms_authority_scope_corporate_action_only": (True, operator.get("operator_confirms_authority_scope_corporate_action_only")),
        "operator_confirms_ready_for_acquisition_chain_candidate": (True, operator.get("operator_confirms_ready_for_acquisition_generation_chain_candidate")),
        "split_event_authority_created_true": (True, artifact.get("split_event_authority_created")),
        "split_event_authority_frozen_true": (True, artifact.get("split_event_authority_frozen")),
        "dividend_event_authority_created_true": (True, artifact.get("dividend_event_authority_created")),
        "dividend_event_authority_frozen_true": (True, artifact.get("dividend_event_authority_frozen")),
        "corporate_action_authority_created_true": (True, artifact.get("corporate_action_authority_created")),
        "corporate_action_authority_approved_true": (True, artifact.get("corporate_action_authority_approved")),
        "corporate_action_authority_scope_corporate_action_only": (CORPORATE_ACTION_AUTHORITY_ONLY, artifact.get("authority_scope")),
        "per_ticker_corporate_action_authority_entries_12": (12, len(entries)),
        "per_ticker_corporate_action_authority_approval_digests_present": (True, digests_present),
        "ready_for_acquisition_generation_chain_candidate_true": (True, artifact.get("ready_for_acquisition_generation_chain_candidate")),
        "limitations_recorded": (LIMITATIONS, artifact.get("limitations")),
        "next_gates_defined": (NEXT_GATES, artifact.get("next_gates")),
    }
    booleans = {
        "new_ticker_acquisition_authorized_false": (False, "new_ticker_acquisition_authorized"),
        "dataset_generation_authorized_false": (False, "dataset_generation_authorized"),
        "acquisition_generation_authorized_false": (False, "acquisition_generation_authorized"),
        "canonical_dataset_authorized_false": (False, "canonical_dataset_authorized"),
        "registry_approval_created_false": (False, "registry_approval_created"),
        "additional_predictive_evidence_execution_authorized_false": (False, "additional_predictive_evidence_execution_authorized"),
        "additional_predictive_evidence_executed_false": (False, "additional_predictive_evidence_executed"),
        "predictive_experiment_rerun_authorized_false": (False, "predictive_experiment_rerun_authorized"),
        "new_strategy_scoring_performed_false": (False, "new_strategy_scoring_performed"),
        "trade_recommendations_generated_false": (False, "trade_recommendations_generated"),
        "runtime_migration_approved_false": (False, "runtime_migration_approved"),
        "automatic_stitching_false": (False, "automatic_stitching"),
        "provider_requests_made_in_approval_false": (False, "provider_requests_made_in_approval"),
        "live_provider_transport_enabled_in_approval_false": (False, "live_provider_transport_enabled_in_approval"),
        "split_provider_evidence_rerun_performed_false": (False, "split_provider_evidence_rerun_performed"),
        "dividend_provider_evidence_rerun_performed_false": (False, "dividend_provider_evidence_rerun_performed"),
        "corporate_action_authority_creates_acquisition_authority_false": (False, "corporate_action_authority_creates_acquisition_authority"),
        "corporate_action_authority_creates_dataset_generation_authority_false": (False, "corporate_action_authority_creates_dataset_generation_authority"),
        "corporate_action_authority_creates_predictive_evidence_authority_false": (False, "corporate_action_authority_creates_predictive_evidence_authority"),
        "corporate_action_authority_creates_runtime_authority_false": (False, "corporate_action_authority_creates_runtime_authority"),
        "no_acquisition_authorization_created": (False, "acquisition_authorization_created"),
        "no_dataset_generation_authorization_created": (False, "dataset_generation_authorization_created"),
        "no_predictive_usefulness_acceptance_artifact_created": (False, "predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": (False, "profitability_acceptance_created"),
        "no_runtime_migration_approval_created": (False, "runtime_migration_approval_created"),
    }
    values.update({check: (expected, artifact.get(field)) for check, (expected, field) in booleans.items()})
    values.update({
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, artifact.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, artifact.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, artifact.get("broker_execution")),
    })
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_APPROVAL_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row["severity"] == BLOCKER for row in failed),
        "corporate_action_authority_approved_by_operator": not failed,
        "authority_scope": CORPORATE_ACTION_AUTHORITY_ONLY,
        "ready_for_acquisition_generation_chain_candidate": not failed,
        "corporate_action_authority_authorized": not failed,
        "split_event_authority_authorized": True,
        "split_event_authority_frozen": True,
        "dividend_event_authority_authorized": True,
        "dividend_event_authority_frozen": True,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("corporate_action_authority_approval_digest", None)
    return payload


def corporate_action_authority_approval_digest_v1(artifact: dict[str, Any]) -> str:
    return semantic_digest(_digest_payload(artifact))


def build_corporate_action_authority_approved_v1(
    *,
    combined_readiness_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    source = (
        combined_readiness_review_package
        if combined_readiness_review_package is not None
        else readiness.build_combined_split_dividend_corporate_action_readiness_review_package_v1()
    )
    _validate_source(source)
    _validate_operator_attestation(operator_attestation)
    artifact = _base_artifact(source, operator_attestation)
    checklist = _approval_checklist(artifact)
    artifact["approval_checklist"] = checklist
    artifact["approval_summary"] = _summary(checklist)
    artifact["corporate_action_authority_approval_digest"] = (
        corporate_action_authority_approval_digest_v1(artifact)
    )
    validate_corporate_action_authority_approved_v1(artifact)
    return artifact


def _validate_per_ticker(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_corporate_action_authority")
    if not isinstance(entries, list) or len(entries) != 12:
        raise CorporateActionAuthorityApprovalError("per_ticker entries mismatch")
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per_ticker tickers")
    expected_source = {row["ticker"]: row for row in readiness._per_ticker_entries()}
    for row in entries:
        ticker = row["ticker"]
        expected = {
            "corporate_action_authority_status": "APPROVED",
            "corporate_action_authority_scope": CORPORATE_ACTION_AUTHORITY_ONLY,
            "split_event_authority_status": "FROZEN",
            "split_event_authority_classification": expected_source[ticker]["split_event_authority_classification"],
            "dividend_event_authority_status": "FROZEN",
            "dividend_event_authority_classification": expected_source[ticker]["dividend_event_authority_classification"],
            "dividend_event_count": expected_source[ticker]["dividend_event_count"],
            "corporate_action_authority_created": True,
            "corporate_action_authority_approved": True,
            "acquisition_authorized": False,
            "dataset_generation_authorized": False,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
        }
        for field, value in expected.items():
            _expect(row.get(field), value, f"{ticker}.{field}")
        _expect_digest(row.get("source_per_ticker_combined_readiness_review_digest"), f"{ticker}.source digest")
        digest = row.get("per_ticker_corporate_action_authority_approval_digest")
        _expect_digest(digest, f"{ticker}.approval digest")
        _expect(digest, per_ticker_corporate_action_authority_approval_digest_v1(row), f"{ticker}.approval digest")


def validate_corporate_action_authority_approved_v1(
    approved_artifact: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(approved_artifact, dict):
        raise CorporateActionAuthorityApprovalError("approved_artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_CORPORATE_ACTION_AUTHORITY_APPROVED,
        "schema_version": SCHEMA_VERSION_CORPORATE_ACTION_AUTHORITY_APPROVAL_V1,
        "approval_status": CORPORATE_ACTION_AUTHORITY_APPROVED,
        "authority_scope": CORPORATE_ACTION_AUTHORITY_ONLY,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "corporate_action_authority_plan_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "split_event_authority_scope": readiness.split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "dividend_event_authority_scope": readiness.dividend_freeze.DIVIDEND_EVENT_AUTHORITY_ONLY,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(approved_artifact.get(field), value, field)
    true_fields = (
        "created_offline", "combined_corporate_action_readiness_review_created",
        "combined_corporate_action_readiness_review_ready", "ready_for_corporate_action_authority_approval",
        "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen",
        "corporate_action_authority_plan_approved", "corporate_action_authority_created",
        "corporate_action_authority_approved", "corporate_action_authority_artifact_created",
        "ready_for_acquisition_generation_chain_candidate", "research_only",
        "combined_split_dividend_authorities_available", "split_authority_frozen",
        "dividend_authority_frozen", "corporate_action_authority_approved_by_operator",
    )
    false_fields = (
        "provider_requests_made_in_approval", "live_provider_transport_enabled_in_approval",
        "split_provider_evidence_rerun_performed", "dividend_provider_evidence_rerun_performed",
        "corporate_action_authority_frozen", "new_ticker_acquisition_authorized",
        "dataset_generation_authorized", "acquisition_generation_authorized",
        "canonical_dataset_authorized", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "corporate_action_authority_creates_acquisition_authority",
        "corporate_action_authority_creates_dataset_generation_authority",
        "corporate_action_authority_creates_predictive_evidence_authority",
        "corporate_action_authority_creates_runtime_authority", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "acquisition_authorization_created",
        "dataset_generation_authorization_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    )
    for field in true_fields:
        _expect_true(approved_artifact.get(field), field)
    for field in false_fields:
        _expect_false(approved_artifact.get(field), field)
    _validate_operator_attestation(approved_artifact.get("operator_attestation", {}))
    _validate_per_ticker(approved_artifact)
    _expect([row.get("check_id") for row in approved_artifact.get("approval_checklist", [])], REQUIRED_APPROVAL_CHECK_IDS, "approval checklist")
    if any(row.get("status") != PASS for row in approved_artifact["approval_checklist"]):
        raise CorporateActionAuthorityApprovalError("approval checklist failed")
    _expect(approved_artifact.get("approval_summary"), _summary(approved_artifact["approval_checklist"]), "approval_summary")
    digest = approved_artifact.get("corporate_action_authority_approval_digest")
    _expect_digest(digest, "corporate_action_authority_approval_digest")
    _expect(digest, corporate_action_authority_approval_digest_v1(approved_artifact), "corporate_action_authority_approval_digest")
    return {
        "status": "CORPORATE_ACTION_AUTHORITY_APPROVED_VALID",
        "artifact_kind": approved_artifact["artifact_kind"],
        "approval_status": approved_artifact["approval_status"],
        "authority_scope": approved_artifact["authority_scope"],
        "corporate_action_authority_approval_digest": digest,
        **{key: approved_artifact["approval_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_corporate_action_authority_approved_markdown_v1(
    approved_artifact: dict[str, Any],
) -> str:
    validation = validate_corporate_action_authority_approved_v1(approved_artifact)
    lines = [
        "# MarketFlow Corporate-Action Authority Approval Status", "",
        "## Title", "- Corporate-Action Authority Approval Ceremony v1.", "",
        "## Approved Corporate-Action Authority",
        f"- Artifact/status/scope: `{approved_artifact['artifact_kind']}` / `{approved_artifact['approval_status']}` / `{approved_artifact['authority_scope']}`.",
        f"- Approval digest: `{validation['corporate_action_authority_approval_digest']}`.", "",
        "## Operator Attestation",
        f"- Decision/reference/timestamp: `{approved_artifact['operator_attestation']['operator_decision']}` / `{approved_artifact['operator_attestation']['operator_reference']}` / `{approved_artifact['operator_attestation']['operator_attestation_timestamp_utc']}`.", "",
        "## Source Combined Readiness Review",
        f"- Review digest: `{approved_artifact['combined_split_dividend_corporate_action_readiness_review_package_digest']}`.", "",
        "## Source Split Authority Freeze",
        f"- Freeze digest: `{approved_artifact['split_event_authority_freeze_digest']}`.", "",
        "## Source Dividend Authority Freeze",
        f"- Freeze digest: `{approved_artifact['dividend_event_authority_freeze_digest']}`.", "",
        "## Target Universe", "- " + ", ".join(f"`{ticker}`" for ticker in TARGET_UNIVERSE), "",
        "## Approved Per-Ticker Corporate-Action Authority Summary",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['corporate_action_authority_status']}`; split/dividend frozen; acquisition and dataset generation not authorized."
        for row in approved_artifact["per_ticker_corporate_action_authority"]
    )
    lines.extend([
        "", "## Authority Scope", f"- `{CORPORATE_ACTION_AUTHORITY_ONLY}`; no acquisition authority is created.",
        "", "## Acquisition Boundary", "- Acquisition remains not authorized; only readiness for a future chain candidate is set.",
        "", "## Dataset Boundary", "- Dataset generation and canonical dataset authorization remain not authorized.",
        "", "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.",
        "", "## Runtime Boundary", "- Runtime, strategy, paper trading, and broker execution remain not authorized.",
        "", "## Approval Checklist Summary",
        f"- Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`.",
        "", "## Remaining Required Tasks",
    ])
    lines.extend(f"- `{gate}`." for gate in NEXT_GATES)
    lines.extend(["", "## Guardrails", "- No provider request, evidence rerun, acquisition, dataset generation, predictive acceptance, or runtime activation occurred."])
    return "\n".join(lines) + "\n"


def write_corporate_action_authority_approved_v1(
    output_dir: str | Path,
    *,
    combined_readiness_review_package: dict[str, Any] | None = None,
    operator_attestation: dict[str, Any],
) -> dict[str, Any]:
    artifact = build_corporate_action_authority_approved_v1(
        combined_readiness_review_package=combined_readiness_review_package,
        operator_attestation=operator_attestation,
    )
    output_path = Path(output_dir)
    json_path = output_path / "corporate_action_authority_approved_v1.json"
    markdown_path = output_path / "corporate_action_authority_approved_v1.md"
    if json_path.exists() or markdown_path.exists():
        raise CorporateActionAuthorityApprovalError("corporate-action approval output already exists")
    output_path.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes(canonical_json_bytes(artifact))
    markdown_path.write_text(build_corporate_action_authority_approved_markdown_v1(artifact), encoding="utf-8")
    return {
        "artifact": artifact,
        "validation": validate_corporate_action_authority_approved_v1(artifact),
        "json_path": json_path.as_posix(),
        "markdown_path": markdown_path.as_posix(),
    }
